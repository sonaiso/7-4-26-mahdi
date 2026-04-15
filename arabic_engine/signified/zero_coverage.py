"""Linguistic-zero coverage analysis — تغطية الصفر اللغوي.

Implements the decision-matrix model that maps a word's morpho-semantic
class (and optional pattern hint) to a per-axis coverage profile across
the twenty linguistic-zero types (Z1–Z20).

Public API
----------
analyze_word_zero_coverage(word, class_name?, pattern?, root?)
    Main entry point — infers class/pattern/root when not supplied.

generate_coverage_report(word_class, pattern?, root?, word?)
    Core engine — builds the report from explicit inputs.

report_to_json(report, *, ensure_ascii?, indent?)
    Serialise a report to a JSON string.

report_to_csv(report, filepath)
    Write a report to a UTF-8 CSV file.

print_report(report)
    Print a human-readable report to stdout.
"""

from __future__ import annotations

import csv
import json
from typing import Dict, FrozenSet, List, Optional, Tuple

from arabic_engine.core.enums import (
    POS,
    LinguisticZeroType,
    WordClass,
    ZeroCoverage,
)
from arabic_engine.core.types import (
    WordZeroCoverageReport,
    ZeroCoverageDetail,
)
from arabic_engine.signifier.root_pattern import lexical_closure

# ── Internal type aliases ────────────────────────────────────────────

_ZSet = FrozenSet[LinguisticZeroType]

# ── Arabic-name map (shared with enum, kept local for fast lookup) ───

_ZERO_NAMES: Dict[LinguisticZeroType, str] = {z: z.arabic_name for z in LinguisticZeroType}

# ── Decision matrix ──────────────────────────────────────────────────
# Maps WordClass → {covers, partial, not_cover} sets of LinguisticZeroType.

_Z = LinguisticZeroType  # shorthand

_DECISION_MATRIX: Dict[WordClass, Dict[str, _ZSet]] = {
    WordClass.JAMID: {
        "covers":    frozenset({_Z.Z1, _Z.Z2, _Z.Z3, _Z.Z14, _Z.Z15, _Z.Z16}),
        "partial":   frozenset({_Z.Z4, _Z.Z17}),
        "not_cover": frozenset({
            _Z.Z5, _Z.Z6, _Z.Z7, _Z.Z8, _Z.Z9, _Z.Z10,
            _Z.Z11, _Z.Z12, _Z.Z13, _Z.Z18, _Z.Z19, _Z.Z20,
        }),
    },
    WordClass.MASDAR: {
        "covers":    frozenset({_Z.Z6}),
        "partial":   frozenset({_Z.Z7, _Z.Z8, _Z.Z9, _Z.Z10, _Z.Z11, _Z.Z12, _Z.Z18}),
        "not_cover": frozenset({
            _Z.Z1, _Z.Z2, _Z.Z3, _Z.Z4, _Z.Z5,
            _Z.Z13, _Z.Z14, _Z.Z15, _Z.Z16, _Z.Z17, _Z.Z19, _Z.Z20,
        }),
    },
    WordClass.DERIVED: {
        "covers":    frozenset({_Z.Z13}),
        "partial":   frozenset({_Z.Z6, _Z.Z7, _Z.Z8, _Z.Z9, _Z.Z10, _Z.Z11, _Z.Z12, _Z.Z18}),
        "not_cover": frozenset({
            _Z.Z1, _Z.Z2, _Z.Z3, _Z.Z4, _Z.Z5,
            _Z.Z14, _Z.Z15, _Z.Z16, _Z.Z17, _Z.Z19, _Z.Z20,
        }),
    },
    WordClass.REFERENTIAL_BUILTINS: {
        "covers":    frozenset({_Z.Z4}),
        "partial":   frozenset({_Z.Z2, _Z.Z3, _Z.Z5, _Z.Z20}),
        "not_cover": frozenset({
            _Z.Z1, _Z.Z6, _Z.Z7, _Z.Z8, _Z.Z9, _Z.Z10,
            _Z.Z11, _Z.Z12, _Z.Z13, _Z.Z14, _Z.Z15, _Z.Z16, _Z.Z17, _Z.Z18, _Z.Z19,
        }),
    },
    WordClass.RELATIONAL_TOOLS: {
        "covers":    frozenset({_Z.Z5}),
        "partial":   frozenset({
            _Z.Z4, _Z.Z7, _Z.Z8, _Z.Z9, _Z.Z10, _Z.Z11, _Z.Z12, _Z.Z19, _Z.Z20,
        }),
        "not_cover": frozenset({
            _Z.Z1, _Z.Z2, _Z.Z3, _Z.Z6,
            _Z.Z13, _Z.Z14, _Z.Z15, _Z.Z16, _Z.Z17, _Z.Z18,
        }),
    },
    WordClass.NOMINAL_COMPETENT: {
        "covers":    frozenset({_Z.Z17}),
        "partial":   frozenset({_Z.Z1, _Z.Z2, _Z.Z3, _Z.Z14, _Z.Z15, _Z.Z16}),
        "not_cover": frozenset({
            _Z.Z4, _Z.Z5, _Z.Z6, _Z.Z7, _Z.Z8, _Z.Z9, _Z.Z10,
            _Z.Z11, _Z.Z12, _Z.Z13, _Z.Z18, _Z.Z19, _Z.Z20,
        }),
    },
    WordClass.VERBAL_COMPETENT: {
        "covers":    frozenset({_Z.Z6, _Z.Z7, _Z.Z9, _Z.Z18}),
        "partial":   frozenset({_Z.Z5, _Z.Z8, _Z.Z10, _Z.Z11, _Z.Z12, _Z.Z13}),
        "not_cover": frozenset({
            _Z.Z1, _Z.Z2, _Z.Z3, _Z.Z4,
            _Z.Z14, _Z.Z15, _Z.Z16, _Z.Z17, _Z.Z19, _Z.Z20,
        }),
    },
    WordClass.VERBAL_COPULAR: {
        "covers":    frozenset({_Z.Z19}),
        "partial":   frozenset({_Z.Z6, _Z.Z7, _Z.Z9, _Z.Z10, _Z.Z11, _Z.Z12, _Z.Z18, _Z.Z20}),
        "not_cover": frozenset({
            _Z.Z1, _Z.Z2, _Z.Z3, _Z.Z4,
            _Z.Z14, _Z.Z15, _Z.Z16, _Z.Z17,
        }),
    },
    WordClass.NOMINAL_COPULAR: {
        "covers":    frozenset({_Z.Z20}),
        "partial":   frozenset({_Z.Z5, _Z.Z17, _Z.Z19}),
        "not_cover": frozenset({
            _Z.Z1, _Z.Z2, _Z.Z3, _Z.Z4, _Z.Z6, _Z.Z7, _Z.Z8,
            _Z.Z9, _Z.Z10, _Z.Z11, _Z.Z12, _Z.Z13,
            _Z.Z14, _Z.Z15, _Z.Z16, _Z.Z18,
        }),
    },
}

# ── Pattern hints ────────────────────────────────────────────────────
# Maps Arabic pattern string → promotion sets.

_PATTERN_HINTS: Dict[str, Dict[str, _ZSet]] = {
    "فعل": {
        "promote_to_covers":  frozenset({_Z.Z6, _Z.Z7}),
        "promote_to_partial": frozenset({_Z.Z9, _Z.Z10}),
    },
    "فاعل": {
        "promote_to_covers":  frozenset({_Z.Z9}),
        "promote_to_partial": frozenset({_Z.Z6, _Z.Z13}),
    },
    "مفعول": {
        "promote_to_covers":  frozenset({_Z.Z10}),
        "promote_to_partial": frozenset({_Z.Z6, _Z.Z13}),
    },
    "افتعل": {
        "promote_to_covers":  frozenset({_Z.Z13}),
        "promote_to_partial": frozenset({_Z.Z11, _Z.Z12}),
    },
    "تفعّل": {
        "promote_to_covers":  frozenset({_Z.Z13}),
        "promote_to_partial": frozenset({_Z.Z11, _Z.Z12, _Z.Z19}),
    },
    "فعّل": {
        "promote_to_covers":  frozenset({_Z.Z13}),
        "promote_to_partial": frozenset({_Z.Z11, _Z.Z12, _Z.Z9, _Z.Z10}),
    },
    "مصدر": {
        "promote_to_covers":  frozenset({_Z.Z6}),
        "promote_to_partial": frozenset({_Z.Z7, _Z.Z8, _Z.Z9, _Z.Z10, _Z.Z11, _Z.Z12}),
    },
}

# ── POS → WordClass bridge ───────────────────────────────────────────

_POS_TO_WORD_CLASS: Dict[POS, WordClass] = {
    POS.FI3L:  WordClass.VERBAL_COMPETENT,
    POS.ISM:   WordClass.NOMINAL_COMPETENT,
    POS.SIFA:  WordClass.DERIVED,
    POS.HARF:  WordClass.RELATIONAL_TOOLS,
    POS.ZARF:  WordClass.JAMID,
    POS.DAMIR: WordClass.REFERENTIAL_BUILTINS,
}

# ── Built-in word lists for heuristic inference ──────────────────────

_REFERENTIAL_WORDS = frozenset({
    "هذا", "هذه", "ذلك", "تلك", "هو", "هي", "هم", "هن",
    "أنت", "أنا", "الذي", "التي",
})
_RELATIONAL_WORDS = frozenset({
    "و", "ف", "ثم", "بل", "لكن", "إلى", "من", "على", "في", "عن", "ب", "ل",
})
_NOMINAL_COPULAR_WORDS = frozenset({
    "إن", "أن", "لكن", "ليت", "لعل", "كأن",
})
_VERBAL_COPULAR_WORDS = frozenset({
    "كان", "صار", "ليس", "أصبح", "أمسى", "ظل", "بات",
    "مازال", "ما برح", "ما انفك",
})

# ── Base-note map ────────────────────────────────────────────────────

_BASE_NOTES: Dict[WordClass, str] = {
    WordClass.JAMID:
        "يغطي الثابت الاسمي ولا يغطي الحدث أصلًا.",
    WordClass.MASDAR:
        "يغطي اللب الحدثي، ويمنح الفاعلية والمفعولية والسببية بالقوة لا بالتعيين الفردي.",
    WordClass.DERIVED:
        "يغطي التحول الاشتقاقي، ويرث بعض القيم من الجذر أو المصدر أو الوزن.",
    WordClass.REFERENTIAL_BUILTINS:
        "يغطي الإحالة، لا الثبات الاسمي الكامل ولا الحدث.",
    WordClass.RELATIONAL_TOOLS:
        "يغطي الربط والعلاقة، لا الهوية الذاتية.",
    WordClass.VERBAL_COMPETENT:
        "يغطي الحدث والزمن والفاعلية في الجملة الفعلية.",
    WordClass.NOMINAL_COMPETENT:
        "يغطي الجاهزية الاسمية التركيبية والإعرابية.",
    WordClass.VERBAL_COPULAR:
        "يغطي التحويل الإسنادي الزمني أو المعنوي.",
    WordClass.NOMINAL_COPULAR:
        "يغطي التوكيد أو الاستدراك أو الترجي أو التمني ونحوها.",
}

_TRAILING_NOTE = (
    "الحقيقة/المجاز، والمطابقة/التضمن/الالتزام، والمقام، "
    "وما فوق الجملة، ما تزال خارج هذا التقرير الأساسي."
)

# ── Helpers ───────────────────────────────────────────────────────────


def _strip_diacritics(text: str) -> str:
    """Remove Arabic diacritical marks (tashkīl) from *text*."""
    diacritics = frozenset("\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652")
    return "".join(ch for ch in text if ch not in diacritics)


def _infer_word_class_and_pattern(
    word: str,
) -> Tuple[WordClass, Optional[str]]:
    """Heuristic inference of :class:`WordClass` and pattern from *word*.

    This is a lightweight rule-based approximation, **not** a full
    morphological analyser.  Callers should prefer passing explicit
    ``class_name`` / ``pattern`` values when they are known.
    """
    bare = _strip_diacritics(word)

    if bare in _REFERENTIAL_WORDS:
        return WordClass.REFERENTIAL_BUILTINS, None
    if bare in _RELATIONAL_WORDS:
        return WordClass.RELATIONAL_TOOLS, None
    if bare in _NOMINAL_COPULAR_WORDS:
        return WordClass.NOMINAL_COPULAR, None
    if bare in _VERBAL_COPULAR_WORDS:
        return WordClass.VERBAL_COPULAR, None

    # مفعول pattern: starts with م, contains و, minimum 5 letters
    if bare.startswith("م") and "و" in bare and len(bare) >= 5:
        return WordClass.DERIVED, "مفعول"

    # فاعل pattern: 4 letters with alif (ا) in second position
    if len(bare) == 4 and bare[1] == "ا":
        return WordClass.DERIVED, "فاعل"

    # افتعل pattern: starts with ا, ت in positions 1–2, minimum 5 letters
    if bare.startswith("ا") and len(bare) >= 5 and "ت" in bare[1:3]:
        return WordClass.DERIVED, "افتعل"

    # تفعّل pattern: starts with ت, minimum 5 letters
    if bare.startswith("ت") and len(bare) >= 5:
        return WordClass.DERIVED, "تفعّل"

    # مصدر approximation: ends with ة (tāʾ marbūṭa), minimum 4 letters
    if bare.endswith("ة") and len(bare) >= 4:
        return WordClass.MASDAR, "مصدر"

    # Tri-literal verb: exactly 3 consonant letters
    if len(bare) == 3:
        return WordClass.VERBAL_COMPETENT, "فعل"

    return WordClass.JAMID, None


def _infer_root(word: str) -> Tuple[str, ...]:
    """Very rough extraction of a tri-literal root from *word*.

    Strips common affix letters and returns the first three consonants.
    """
    bare = _strip_diacritics(word)
    removable = frozenset("ماويتنة")
    letters = [ch for ch in bare if ch not in removable]
    if len(letters) >= 3:
        return tuple(letters[:3])
    return ()


def _build_status_map(
    word_class: WordClass,
) -> Dict[LinguisticZeroType, ZeroCoverage]:
    """Build a mutable status map from the decision matrix."""
    entry = _DECISION_MATRIX[word_class]
    status: Dict[LinguisticZeroType, ZeroCoverage] = {
        z: ZeroCoverage.UNCOVERED for z in LinguisticZeroType
    }
    for z in entry["covers"]:
        status[z] = ZeroCoverage.COVERS
    for z in entry["partial"]:
        if status[z] is not ZeroCoverage.COVERS:
            status[z] = ZeroCoverage.PARTIAL
    return status


def _apply_pattern_hints(
    status: Dict[LinguisticZeroType, ZeroCoverage],
    pattern: Optional[str],
) -> None:
    """Mutate *status* in place by applying pattern-hint promotions."""
    if not pattern:
        return
    hint = _PATTERN_HINTS.get(pattern)
    if not hint:
        return
    for z in hint.get("promote_to_partial", frozenset()):
        if status[z] is ZeroCoverage.UNCOVERED:
            status[z] = ZeroCoverage.PARTIAL
    for z in hint.get("promote_to_covers", frozenset()):
        status[z] = ZeroCoverage.COVERS


# ── Core engine ───────────────────────────────────────────────────────


def generate_coverage_report(
    word_class: WordClass,
    pattern: Optional[str] = None,
    root: Optional[Tuple[str, ...]] = None,
    word: str = "",
) -> WordZeroCoverageReport:
    """Build a :class:`WordZeroCoverageReport` from explicit inputs.

    Parameters
    ----------
    word_class:
        The morpho-semantic class of the word.
    pattern:
        Optional morphological pattern string (e.g. ``'فاعل'``).
    root:
        Optional tuple of root letters (e.g. ``('ك', 'ت', 'ب')``).
    word:
        Optional surface form (used only for labelling in the report).

    Returns
    -------
    WordZeroCoverageReport
        Frozen report with per-axis coverage details and summary lists.
    """
    status = _build_status_map(word_class)
    _apply_pattern_hints(status, pattern)

    covers_list: List[str] = []
    partial_list: List[str] = []
    uncovered_list: List[str] = []
    details: List[ZeroCoverageDetail] = []

    for z in LinguisticZeroType:
        cov = status[z]
        detail = ZeroCoverageDetail(zero_type=z, coverage=cov)
        details.append(detail)
        if cov is ZeroCoverage.COVERS:
            covers_list.append(z.name)
        elif cov is ZeroCoverage.PARTIAL:
            partial_list.append(z.name)
        else:
            uncovered_list.append(z.name)

    notes: List[str] = []
    base = _BASE_NOTES.get(word_class)
    if base:
        notes.append(base)
    if pattern:
        notes.append(
            f"استُخدم الوزن الصرفي '{pattern}' لرفع بعض المحاور "
            "من uncovered إلى partial أو covers."
        )
    notes.append(_TRAILING_NOTE)

    return WordZeroCoverageReport(
        word=word,
        word_class=word_class,
        pattern=pattern or "",
        root=root or (),
        covers=tuple(covers_list),
        partial=tuple(partial_list),
        uncovered=tuple(uncovered_list),
        details=tuple(details),
        notes=tuple(notes),
    )


def analyze_word_zero_coverage(
    word: str,
    class_name: Optional[str] = None,
    pattern: Optional[str] = None,
    root: Optional[Tuple[str, ...]] = None,
) -> WordZeroCoverageReport:
    """Analyse *word* and return its linguistic-zero coverage report.

    Resolution order
    ----------------
    1. Explicit ``class_name`` / ``pattern`` / ``root`` arguments take
       highest priority.
    2. The existing lexical-closure dictionary
       (:func:`~arabic_engine.signifier.root_pattern.lexical_closure`)
       is consulted for a POS match, which is bridged to :class:`WordClass`.
    3. If the word is unknown in the lexicon, lightweight heuristics are
       applied (see :func:`_infer_word_class_and_pattern`).

    Parameters
    ----------
    word:
        Surface form of the Arabic word to analyse.
    class_name:
        Optional :class:`WordClass` name string (e.g. ``'JAMID'``).
        Case-insensitive.
    pattern:
        Optional morphological pattern string.
    root:
        Optional tuple of root letters.

    Returns
    -------
    WordZeroCoverageReport
    """
    # Step 1 — Resolve word_class
    final_class: WordClass
    if class_name is not None:
        final_class = WordClass[class_name.upper()]
    else:
        # Try lexical closure first
        closure = lexical_closure(word)
        if closure.pos is not POS.UNKNOWN:
            final_class = _POS_TO_WORD_CLASS.get(closure.pos, WordClass.JAMID)
        else:
            final_class, _ = _infer_word_class_and_pattern(word)

    # Step 2 — Resolve pattern
    final_pattern: Optional[str]
    if pattern is not None:
        final_pattern = pattern
    else:
        closure = lexical_closure(word)
        if closure.pos is not POS.UNKNOWN and closure.pattern:
            final_pattern = closure.pattern
        else:
            _, inferred_pattern = _infer_word_class_and_pattern(word)
            final_pattern = inferred_pattern

    # Step 3 — Resolve root
    final_root: Tuple[str, ...]
    if root is not None:
        final_root = root
    else:
        closure = lexical_closure(word)
        if closure.root:
            final_root = closure.root
        else:
            final_root = _infer_root(word)

    return generate_coverage_report(
        word_class=final_class,
        pattern=final_pattern,
        root=final_root,
        word=word,
    )


# ── Export helpers ────────────────────────────────────────────────────


def report_to_dict(report: WordZeroCoverageReport) -> dict:
    """Convert *report* to a plain Python dict suitable for JSON output."""
    return {
        "input": {
            "word": report.word,
            "word_class": report.word_class.name,
            "pattern": report.pattern,
            "root": list(report.root),
        },
        "coverage": {
            "covers":    list(report.covers),
            "partial":   list(report.partial),
            "uncovered": list(report.uncovered),
        },
        "zero_details": [
            {
                "zero_code": d.zero_code,
                "zero_name": d.zero_name,
                "coverage":  d.coverage.name.lower(),
            }
            for d in report.details
        ],
        "notes": list(report.notes),
    }


def report_to_json(
    report: WordZeroCoverageReport,
    *,
    ensure_ascii: bool = False,
    indent: int = 2,
) -> str:
    """Serialise *report* to a JSON string.

    Parameters
    ----------
    report:
        The coverage report to serialise.
    ensure_ascii:
        When ``False`` (default) Arabic characters are kept as-is.
    indent:
        JSON indentation level (default 2).
    """
    return json.dumps(report_to_dict(report), ensure_ascii=ensure_ascii, indent=indent)


def report_to_csv(report: WordZeroCoverageReport, filepath: str) -> None:
    """Write *report* to a single-row UTF-8 CSV file at *filepath*.

    Columns: ``word``, ``word_class``, ``pattern``, ``root``,
    ``Z1``–``Z20``, ``notes``.
    """
    z_codes = [z.name for z in LinguisticZeroType]
    fieldnames = ["word", "word_class", "pattern", "root", *z_codes, "notes"]

    detail_map = {d.zero_code: d.coverage.name.lower() for d in report.details}
    row: dict = {
        "word":       report.word,
        "word_class": report.word_class.name,
        "pattern":    report.pattern,
        "root":       "-".join(report.root),
        "notes":      " | ".join(report.notes),
        **{z: detail_map[z] for z in z_codes},
    }

    with open(filepath, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)


def print_report(report: WordZeroCoverageReport) -> None:
    """Print a human-readable summary of *report* to stdout."""
    data = report_to_dict(report)

    print("=== INPUT ===")
    print(json.dumps(data["input"], ensure_ascii=False, indent=2))

    print("\n=== COVERAGE SUMMARY ===")
    print("covers   :", ", ".join(data["coverage"]["covers"])    or "—")
    print("partial  :", ", ".join(data["coverage"]["partial"])   or "—")
    print("uncovered:", ", ".join(data["coverage"]["uncovered"]) or "—")

    print("\n=== ZERO DETAILS ===")
    for item in data["zero_details"]:
        print(f"{item['zero_code']:>3} | {item['zero_name']:<30} | {item['coverage']}")

    print("\n=== NOTES ===")
    for note in data["notes"]:
        print("-", note)
