"""Diacritised word analysis pipeline (تحليل الكلمة المشكولة).

Provides an 8-step pipeline that takes a diacritised Arabic word
(or multi-word text) and produces a :class:`TokenAnalysis` record
with enriched graphemes, syllable shapes, and pattern candidates.

Steps
-----
1. Normalise Unicode (NFC, tatweel removal).
2. Split into grapheme clusters.
3. Enrich graphemes with metadata from ``arabic_letters.csv``.
4. Map combining marks to ``unicode_marks.csv`` / ``arabic_vowels.csv``.
5. Strip and record clitics from ``closed_connectors.csv``.
6. Build syllables and match shapes from ``syllable_shapes.csv``.
7. Match morphological patterns from ``pattern_codes.csv`` and the
   mini-lexicon in :mod:`arabic_engine.signifier.root_pattern`.
8. Emit a :class:`TokenAnalysis` record.
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.types import (
    CliticRecord,
    CombiningMarkDetail,
    EnrichedGrapheme,
    EnrichedSyllable,
    PatternCandidate,
    RootCandidate,
    TokenAnalysis,
)
from arabic_engine.data.loader import (
    load_arabic_letters,
    load_arabic_vowels,
    load_closed_connectors,
    load_pattern_codes,
    load_syllable_shapes,
    load_unicode_marks,
)
from arabic_engine.signifier.phonology import syllabify
from arabic_engine.signifier.root_pattern import extract_root_pattern
from arabic_engine.signifier.unicode_norm import normalize, to_graphemes, tokenize

# ── Counters for ID generation ──────────────────────────────────────

_token_counter = 0
_char_counter = 0
_syll_counter = 0


def _next_token_id() -> str:
    global _token_counter
    _token_counter += 1
    return f"token_{_token_counter:04d}"


def _next_char_id() -> str:
    global _char_counter
    _char_counter += 1
    return f"char_{_char_counter:04d}"


def _next_syll_id() -> str:
    global _syll_counter
    _syll_counter += 1
    return f"syll_{_syll_counter:04d}"


def _codepoint_str(cp: int) -> str:
    """Format an integer code-point as ``U+XXXX``."""
    return f"U+{cp:04X}"


# ── Step 3–4: enrich graphemes ──────────────────────────────────────


def _enrich_grapheme(base: int, marks: tuple[int, ...]) -> EnrichedGrapheme:
    """Build an :class:`EnrichedGrapheme` from raw base + marks."""
    letters = load_arabic_letters()
    unicode_marks = load_unicode_marks()
    vowels = load_arabic_vowels()

    base_cp = _codepoint_str(base)
    base_char = chr(base)
    surface = base_char + "".join(chr(m) for m in marks)

    # Look up letter record
    letter_rec = letters.get(base_cp, {})
    phonetic_code = letter_rec.get("phonetic_code", "")
    place_code = int(letter_rec.get("place_code", 0))
    manner_code = int(letter_rec.get("manner_code", 0))
    voicing_code = int(letter_rec.get("voicing_code", 0))
    stiffness_code = int(letter_rec.get("stiffness_code", 0))
    entity_score = float(letter_rec.get("entity_score", 0.0))

    # Build combining mark details
    mark_details: list[CombiningMarkDetail] = []
    for m in marks:
        m_cp = _codepoint_str(m)
        m_info = unicode_marks.get(m_cp, {})
        v_info = vowels.get(m_cp, {})
        mark_type = m_info.get("type", v_info.get("type", "unknown"))
        mark_details.append(CombiningMarkDetail(
            char=chr(m),
            codepoint=m_cp,
            type=mark_type,
        ))

    # Determine role for ambiguous letters (ا و ي)
    _LONG_VOWELS = {0x0627, 0x0648, 0x064A}
    role: str | None = None
    if base in _LONG_VOWELS:
        role = "ambiguous"
    elif letter_rec:
        role = "consonant"

    return EnrichedGrapheme(
        id=_next_char_id(),
        layer=1,
        surface=surface,
        base_char=base_char,
        base_codepoint=base_cp,
        combining_marks=tuple(mark_details),
        phonetic_code=phonetic_code,
        place_code=place_code,
        manner_code=manner_code,
        voicing_code=voicing_code,
        stiffness_code=stiffness_code,
        entity_score=entity_score,
        role=role,
    )


# ── Step 5: detect and strip clitics ────────────────────────────────


def _detect_clitics(surface: str) -> tuple[list[CliticRecord], str]:
    """Detect leading clitics and return (clitics, core_surface)."""
    connectors = load_closed_connectors()
    clitics: list[CliticRecord] = []
    remaining = surface

    # Sort connectors by surface length descending to match longest first
    sorted_conn = sorted(connectors, key=lambda c: len(c["surface"]), reverse=True)

    # Repeatedly strip leading clitics
    changed = True
    while changed:
        changed = False
        for conn in sorted_conn:
            conn_surface = conn["surface"]
            if remaining.startswith(conn_surface) and len(remaining) > len(conn_surface):
                clitics.append(CliticRecord(
                    surface=conn_surface,
                    type=conn["type"],
                    confidence=0.95,
                ))
                remaining = remaining[len(conn_surface):]
                changed = True
                break

    return clitics, remaining


# ── Step 6: syllable shape matching ─────────────────────────────────


def _classify_syllable_shape(
    onset: tuple[int, ...],
    nucleus: tuple[int, ...],
    coda: tuple[int, ...],
) -> str:
    """Determine the shape label (CV, CVC, CVV, etc.) from components."""
    c_count = len(onset)
    v_count = len(nucleus)
    coda_count = len(coda)

    if c_count == 0 and v_count > 0 and coda_count == 0:
        return "V"
    if c_count == 0 and v_count > 0 and coda_count > 0:
        return "VC"

    label = "C" * c_count
    if v_count == 1:
        label += "V"
    elif v_count >= 2:
        label += "VV"
    label += "C" * coda_count
    return label


# ── Main pipeline functions ─────────────────────────────────────────


def analyze_word(text: str) -> TokenAnalysis:
    """Analyse a single diacritised Arabic word.

    Executes the 8-step pipeline:

    1. Normalise Unicode.
    2. Split graphemes.
    3. Enrich graphemes with letter metadata.
    4. Map combining marks to vowel records.
    5. Detect and strip clitics.
    6. Build syllables and match shapes.
    7. Match morphological patterns.
    8. Emit :class:`TokenAnalysis`.

    Args:
        text: A single Arabic word (may include clitics and diacritics).

    Returns:
        A fully populated :class:`TokenAnalysis` record.
    """
    shapes = load_syllable_shapes()
    patterns = load_pattern_codes()

    # Step 1: normalise
    normalised = normalize(text)

    # Step 2: grapheme decomposition
    raw_graphemes = to_graphemes(normalised)

    # Step 3–4: enrich graphemes
    enriched: list[EnrichedGrapheme] = [
        _enrich_grapheme(g.base, g.marks) for g in raw_graphemes
    ]

    # Step 5: detect clitics
    clitics, core_surface = _detect_clitics(normalised)

    # Step 6: build syllables from raw graphemes, then match shapes
    syllables_raw = syllabify(raw_graphemes)
    enriched_syllables: list[EnrichedSyllable] = []
    for syll in syllables_raw:
        shape_label = _classify_syllable_shape(syll.onset, syll.nucleus, syll.coda)
        shape_rec = shapes.get(shape_label, {})
        surface_str = "".join(chr(cp) for cp in (*syll.onset, *syll.nucleus, *syll.coda))
        enriched_syllables.append(EnrichedSyllable(
            id=_next_syll_id(),
            layer=3,
            surface=surface_str,
            shape=shape_label,
            shape_code=shape_rec.get("shape_code", ""),
            nucleus_type=int(shape_rec.get("nucleus_type", 0)),
            closure_type=int(shape_rec.get("closure_type", 0)),
            weight_code=int(shape_rec.get("weight_code", 0)),
            completion_score=0.78 if shape_rec else 0.0,
            weightability_score=0.55 if shape_rec else 0.0,
        ))

    # Step 7: pattern matching via mini-lexicon
    root_candidates: list[RootCandidate] = []
    pattern_candidates: list[PatternCandidate] = []

    rp = extract_root_pattern(normalised)
    if rp is not None:
        root_candidates.append(RootCandidate(
            root=rp.root,
            confidence=0.87,
        ))
        # Try to find a matching pattern_code
        for code, pat_rec in patterns.items():
            if pat_rec.get("pattern_type") == "mujarrad" and len(rp.root) == 3:
                pattern_candidates.append(PatternCandidate(
                    pattern_code=code,
                    pattern_label=pat_rec.get("pattern_label", ""),
                    pattern_type=pat_rec.get("pattern_type", ""),
                    augment_count=int(pat_rec.get("augment_count", 0)),
                    root_candidate=rp.root,
                    confidence=0.73,
                    reality_match_score=0.79,
                ))
                break

    return TokenAnalysis(
        id=_next_token_id(),
        surface=text,
        normalized_form=normalised,
        unicode_form="NFC",
        graphemes=tuple(enriched),
        clitics=tuple(clitics),
        core_surface=core_surface,
        syllables=tuple(enriched_syllables),
        root_candidates=tuple(root_candidates),
        pattern_candidates=tuple(pattern_candidates),
        final_status="structural_analysis_only",
    )


def analyze_text(text: str) -> List[TokenAnalysis]:
    """Analyse multi-word diacritised Arabic text.

    Tokenises the input and runs :func:`analyze_word` on each token.

    Args:
        text: Arabic text (may contain multiple whitespace-separated
            words with diacritics).

    Returns:
        A list of :class:`TokenAnalysis` records, one per token.
    """
    tokens = tokenize(text)
    return [analyze_word(tok) for tok in tokens]
