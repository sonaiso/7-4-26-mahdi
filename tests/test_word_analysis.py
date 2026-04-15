"""Tests for the word analysis pipeline and data loaders.

Covers:
- CSV data loading (row counts, key fields)
- JSON schema/policy loading
- Unicode grapheme enrichment
- Syllable shape matching
- Pattern code matching
- Full word analysis pipeline
- Multi-word text analysis
- Clitic detection
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

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
    clear_cache,
    load_arabic_letters,
    load_arabic_vowels,
    load_closed_built_forms,
    load_closed_connectors,
    load_pattern_codes,
    load_syllable_shapes,
    load_unicode_marks,
    load_unicode_policy,
)
from arabic_engine.signifier.word_analysis import (
    analyze_text,
    analyze_word,
)

# ── Fixtures ────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def _clear_data_cache():
    """Clear the data loader cache before each test."""
    clear_cache()
    yield
    clear_cache()


# Reset word_analysis ID counters between tests
@pytest.fixture(autouse=True)
def _reset_counters():
    import arabic_engine.signifier.word_analysis as wa
    wa._token_counter = 0
    wa._char_counter = 0
    wa._syll_counter = 0


# ── CSV loading tests ──────────────────────────────────────────────


class TestCSVLoading:
    """Verify that all CSV data files load correctly."""

    def test_unicode_marks_count(self):
        marks = load_unicode_marks()
        assert len(marks) == 8

    def test_unicode_marks_fatha(self):
        marks = load_unicode_marks()
        fatha = marks["U+064E"]
        assert fatha["name"] == "ARABIC FATHA"
        assert fatha["type"] == "haraka"

    def test_unicode_marks_shadda(self):
        marks = load_unicode_marks()
        shadda = marks["U+0651"]
        assert shadda["type"] == "shadda"

    def test_unicode_marks_tanween(self):
        marks = load_unicode_marks()
        fathatan = marks["U+064B"]
        assert fathatan["type"] == "tanween"

    def test_arabic_letters_count(self):
        letters = load_arabic_letters()
        assert len(letters) >= 4

    def test_arabic_letters_ba(self):
        letters = load_arabic_letters()
        ba = letters["U+0628"]
        assert ba["base_char"] == "\u0628"
        assert ba["phonetic_code"] == "1.1.1.1.3"
        assert float(ba["entity_score"]) == pytest.approx(0.81)

    def test_arabic_vowels_count(self):
        vowels = load_arabic_vowels()
        assert len(vowels) == 5

    def test_arabic_vowels_fatha(self):
        vowels = load_arabic_vowels()
        fatha = vowels["U+064E"]
        assert fatha["vowel_code"] == "2.1.1.1"
        assert float(fatha["entity_score"]) == pytest.approx(0.84)

    def test_syllable_shapes_count(self):
        shapes = load_syllable_shapes()
        assert len(shapes) == 10

    def test_syllable_shapes_cv(self):
        shapes = load_syllable_shapes()
        cv = shapes["CV"]
        assert cv["shape_code"] == "3.1.1.0.1"
        assert cv["weight_code"] == "1"

    def test_syllable_shapes_cvc(self):
        shapes = load_syllable_shapes()
        cvc = shapes["CVC"]
        assert cvc["shape_code"] == "3.2.1.1.2"
        assert cvc["weight_code"] == "2"

    def test_pattern_codes_count(self):
        patterns = load_pattern_codes()
        assert len(patterns) == 14

    def test_pattern_codes_mujarrad(self):
        patterns = load_pattern_codes()
        mujarrad = patterns["4.3.111.0.2"]
        assert mujarrad["pattern_label"] == "mujarrad_fa3ala"
        assert mujarrad["augment_count"] == "0"
        assert mujarrad["pattern_type"] == "mujarrad"

    def test_closed_connectors_count(self):
        connectors = load_closed_connectors()
        assert len(connectors) >= 5

    def test_closed_built_forms_count(self):
        forms = load_closed_built_forms()
        assert len(forms) >= 6


# ── JSON loading tests ─────────────────────────────────────────────


class TestJSONLoading:
    """Verify that JSON files load correctly."""

    def test_unicode_policy_structure(self):
        policy = load_unicode_policy()
        assert "unicode_policy" in policy

    def test_unicode_policy_nfc(self):
        policy = load_unicode_policy()
        assert policy["unicode_policy"]["normalization_form"] == "NFC"

    def test_unicode_policy_preserve_diacritics(self):
        policy = load_unicode_policy()
        assert policy["unicode_policy"]["preserve_diacritics"] is True

    def test_unicode_policy_hamza(self):
        policy = load_unicode_policy()
        hamza = policy["unicode_policy"]["hamza_policy"]
        assert hamza["preserve_surface_form"] is True
        assert hamza["store_abstract_hamza"] is True


# ── JSON Schema validation tests ───────────────────────────────────


class TestJSONSchemas:
    """Verify that JSON schema files are valid JSON."""

    _SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "arabic_engine" / "schemas"

    @pytest.mark.parametrize("name", [
        "grapheme.schema.json",
        "syllable.schema.json",
        "pattern.schema.json",
        "token.schema.json",
    ])
    def test_schema_is_valid_json(self, name):
        path = self._SCHEMAS_DIR / name
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        assert "$schema" in data
        assert "title" in data
        assert "type" in data

    def test_grapheme_schema_has_required_fields(self):
        path = self._SCHEMAS_DIR / "grapheme.schema.json"
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        required = data.get("required", [])
        assert "id" in required
        assert "base_char" in required

    def test_token_schema_has_required_fields(self):
        path = self._SCHEMAS_DIR / "token.schema.json"
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        required = data.get("required", [])
        assert "surface" in required
        assert "normalized_form" in required


# ── Enriched type construction tests ───────────────────────────────


class TestEnrichedTypes:
    """Verify enriched dataclass construction."""

    def test_combining_mark_detail(self):
        cmd = CombiningMarkDetail(char="\u064E", codepoint="U+064E", type="haraka")
        assert cmd.char == "\u064E"
        assert cmd.type == "haraka"

    def test_enriched_grapheme(self):
        eg = EnrichedGrapheme(
            id="char_0001",
            layer=1,
            surface="\u0628\u064E",
            base_char="\u0628",
            base_codepoint="U+0628",
            phonetic_code="1.1.1.1.3",
            entity_score=0.81,
        )
        assert eg.layer == 1
        assert eg.base_codepoint == "U+0628"

    def test_enriched_syllable(self):
        es = EnrichedSyllable(
            id="syll_0001",
            layer=3,
            surface="\u0628\u064E",
            shape="CV",
            shape_code="3.1.1.0.1",
            weight_code=1,
        )
        assert es.shape == "CV"
        assert es.weight_code == 1

    def test_pattern_candidate(self):
        pc = PatternCandidate(
            pattern_code="4.3.111.0.2",
            pattern_label="mujarrad_fa3ala",
            pattern_type="mujarrad",
            root_candidate=("\u0643", "\u062A", "\u0628"),
            confidence=0.73,
        )
        assert pc.pattern_type == "mujarrad"
        assert len(pc.root_candidate) == 3

    def test_clitic_record(self):
        cr = CliticRecord(surface="\u0648\u064E", type="connector", confidence=0.95)
        assert cr.type == "connector"

    def test_root_candidate(self):
        rc = RootCandidate(root=("\u0643", "\u062A", "\u0628"), confidence=0.87)
        assert len(rc.root) == 3

    def test_token_analysis(self):
        ta = TokenAnalysis(
            id="token_0001",
            surface="\u0643\u064E\u062A\u064E\u0628\u064E",
            normalized_form="\u0643\u064E\u062A\u064E\u0628\u064E",
        )
        assert ta.final_status == "structural_analysis_only"
        assert ta.unicode_form == "NFC"


# ── Word analysis pipeline tests ───────────────────────────────────


class TestAnalyzeWord:
    """Test the 8-step word analysis pipeline."""

    def test_kataba_graphemes(self):
        """كَتَبَ → 3 enriched graphemes."""
        result = analyze_word("\u0643\u064E\u062A\u064E\u0628\u064E")
        assert len(result.graphemes) == 3
        assert result.graphemes[0].base_char == "\u0643"
        assert result.graphemes[1].base_char == "\u062A"
        assert result.graphemes[2].base_char == "\u0628"

    def test_kataba_combining_marks(self):
        """Each grapheme in كَتَبَ has one fatha mark."""
        result = analyze_word("\u0643\u064E\u062A\u064E\u0628\u064E")
        for g in result.graphemes:
            assert len(g.combining_marks) == 1
            assert g.combining_marks[0].type == "haraka"
            assert g.combining_marks[0].codepoint == "U+064E"

    def test_kataba_syllables(self):
        """كَتَبَ → 3 CV syllables."""
        result = analyze_word("\u0643\u064E\u062A\u064E\u0628\u064E")
        assert len(result.syllables) == 3
        for syll in result.syllables:
            assert syll.shape == "CV"
            assert syll.shape_code == "3.1.1.0.1"
            assert syll.weight_code == 1

    def test_kataba_root(self):
        """كَتَبَ → root (ك, ت, ب)."""
        result = analyze_word("\u0643\u064E\u062A\u064E\u0628\u064E")
        assert len(result.root_candidates) == 1
        assert result.root_candidates[0].root == ("\u0643", "\u062A", "\u0628")

    def test_kataba_pattern(self):
        """كَتَبَ → pattern mujarrad_fa3ala."""
        result = analyze_word("\u0643\u064E\u062A\u064E\u0628\u064E")
        assert len(result.pattern_candidates) >= 1
        assert result.pattern_candidates[0].pattern_code == "4.3.111.0.2"
        assert result.pattern_candidates[0].pattern_label == "mujarrad_fa3ala"

    def test_kataba_normalized(self):
        """Normalized form preserves diacritics."""
        result = analyze_word("\u0643\u064E\u062A\u064E\u0628\u064E")
        assert result.normalized_form == "\u0643\u064E\u062A\u064E\u0628\u064E"
        assert result.unicode_form == "NFC"

    def test_kataba_id_format(self):
        """Token ID follows the token_NNNN pattern."""
        result = analyze_word("\u0643\u064E\u062A\u064E\u0628\u064E")
        assert result.id.startswith("token_")

    def test_kataba_core_surface(self):
        """No clitics → core_surface equals normalized form."""
        result = analyze_word("\u0643\u064E\u062A\u064E\u0628\u064E")
        assert result.core_surface == result.normalized_form
        assert len(result.clitics) == 0

    def test_ambiguous_waw_role(self):
        """و should be marked as 'ambiguous' role."""
        result = analyze_word("\u0648")
        assert len(result.graphemes) == 1
        assert result.graphemes[0].role == "ambiguous"

    def test_consonant_role(self):
        """ب should be marked as 'consonant' role."""
        result = analyze_word("\u0628\u064E")
        assert result.graphemes[0].role == "consonant"

    def test_unknown_token_no_root(self):
        """An unknown word should have no root candidates."""
        result = analyze_word("\u0645\u064E\u0644\u064E\u0643\u064E")
        assert len(result.root_candidates) == 0
        assert len(result.pattern_candidates) == 0

    def test_final_status(self):
        """Default final_status is 'structural_analysis_only'."""
        result = analyze_word("\u0643\u064E\u062A\u064E\u0628\u064E")
        assert result.final_status == "structural_analysis_only"


# ── Multi-word text analysis tests ─────────────────────────────────


class TestAnalyzeText:
    """Test batch text analysis."""

    def test_sentence(self):
        """كَتَبَ زَيْدٌ → 2 token analyses."""
        results = analyze_text(
            "\u0643\u064E\u062A\u064E\u0628\u064E \u0632\u064E\u064A\u0652\u062F\u064C"
        )
        assert len(results) == 2
        assert results[0].normalized_form == "\u0643\u064E\u062A\u064E\u0628\u064E"

    def test_empty_text(self):
        """Empty string → empty list."""
        results = analyze_text("")
        assert results == []

    def test_single_word(self):
        """Single word text → list of one."""
        results = analyze_text("\u0643\u064E\u062A\u064E\u0628\u064E")
        assert len(results) == 1


# ── Clitic detection tests ─────────────────────────────────────────


class TestCliticDetection:
    """Test clitic stripping from prefixed words."""

    def test_wa_connector(self):
        """وَكَتَبَ → clitic وَ detected."""
        result = analyze_word(
            "\u0648\u064E\u0643\u064E\u062A\u064E\u0628\u064E"
        )
        assert len(result.clitics) >= 1
        clitic_surfaces = [c.surface for c in result.clitics]
        assert "\u0648\u064E" in clitic_surfaces

    def test_core_surface_after_clitic(self):
        """Core surface after stripping وَ from وَكَتَبَ."""
        result = analyze_word(
            "\u0648\u064E\u0643\u064E\u062A\u064E\u0628\u064E"
        )
        # core_surface should not start with the clitic
        assert not result.core_surface.startswith("\u0648\u064E")

    def test_no_clitic_when_too_short(self):
        """A single-char word matching a clitic should not be stripped."""
        result = analyze_word("\u0648\u064E")
        # وَ alone is too short to strip (nothing remains)
        assert len(result.clitics) == 0


# ── Data cache tests ───────────────────────────────────────────────


class TestDataCache:
    """Verify that data loaders cache results."""

    def test_marks_cached(self):
        """The underlying CSV rows are cached (same list object)."""
        from arabic_engine.data.loader import _load_csv
        r1 = _load_csv("unicode/unicode_marks.csv")
        r2 = _load_csv("unicode/unicode_marks.csv")
        assert r1 is r2

    def test_clear_cache(self):
        m1 = load_unicode_marks()
        clear_cache()
        m2 = load_unicode_marks()
        assert m1 is not m2
        assert m1 == m2
