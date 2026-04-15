"""Tests for arabic_engine.signified.zero_coverage — تغطية الصفر اللغوي."""

from __future__ import annotations

import json
import os
import tempfile

import pytest

from arabic_engine.core.enums import LinguisticZeroType, WordClass, ZeroCoverage
from arabic_engine.core.types import WordZeroCoverageReport, ZeroCoverageDetail
from arabic_engine.signified.zero_coverage import (
    analyze_word_zero_coverage,
    generate_coverage_report,
    report_to_csv,
    report_to_json,
)

# ── helpers ──────────────────────────────────────────────────────────


def _coverage_set(report: WordZeroCoverageReport, cov: ZeroCoverage) -> set[str]:
    return {d.zero_code for d in report.details if d.coverage is cov}


# ── Phase 1: decision-matrix — each WordClass ────────────────────────


class TestDecisionMatrixJamid:
    def setup_method(self):
        self.report = generate_coverage_report(WordClass.JAMID, word="رجل")

    def test_word_class(self):
        assert self.report.word_class is WordClass.JAMID

    def test_covers(self):
        assert {"Z1", "Z2", "Z3", "Z14", "Z15", "Z16"} <= set(self.report.covers)

    def test_partial(self):
        assert {"Z4", "Z17"} <= set(self.report.partial)

    def test_uncovered_includes_event(self):
        assert "Z6" in self.report.uncovered

    def test_details_count(self):
        assert len(self.report.details) == 20


class TestDecisionMatrixMasdar:
    def setup_method(self):
        self.report = generate_coverage_report(WordClass.MASDAR, word="كتابة")

    def test_covers_event(self):
        assert "Z6" in self.report.covers

    def test_partial_agent(self):
        assert "Z9" in self.report.partial

    def test_uncovered_nominal_identity(self):
        assert "Z1" in self.report.uncovered


class TestDecisionMatrixDerived:
    def setup_method(self):
        self.report = generate_coverage_report(WordClass.DERIVED, word="مكتوب")

    def test_covers_derivation(self):
        assert "Z13" in self.report.covers

    def test_partial_event(self):
        assert "Z6" in self.report.partial

    def test_uncovered_nominal_identity(self):
        assert "Z1" in self.report.uncovered


class TestDecisionMatrixReferentialBuiltins:
    def setup_method(self):
        self.report = generate_coverage_report(WordClass.REFERENTIAL_BUILTINS, word="هذا")

    def test_covers_reference(self):
        assert "Z4" in self.report.covers

    def test_partial_includes_definiteness(self):
        assert "Z3" in self.report.partial

    def test_uncovered_event(self):
        assert "Z6" in self.report.uncovered


class TestDecisionMatrixRelationalTools:
    def setup_method(self):
        self.report = generate_coverage_report(WordClass.RELATIONAL_TOOLS, word="من")

    def test_covers_relation(self):
        assert "Z5" in self.report.covers

    def test_partial_reference(self):
        assert "Z4" in self.report.partial

    def test_uncovered_nominal_identity(self):
        assert "Z1" in self.report.uncovered


class TestDecisionMatrixNominalCompetent:
    def setup_method(self):
        self.report = generate_coverage_report(WordClass.NOMINAL_COMPETENT, word="الكتاب")

    def test_covers_nominal_competence(self):
        assert "Z17" in self.report.covers

    def test_partial_nominal_identity(self):
        assert "Z1" in self.report.partial

    def test_uncovered_event(self):
        assert "Z6" in self.report.uncovered


class TestDecisionMatrixVerbalCompetent:
    def setup_method(self):
        self.report = generate_coverage_report(WordClass.VERBAL_COMPETENT, word="كتب")

    def test_covers_event_time_agent(self):
        for code in ("Z6", "Z7", "Z9", "Z18"):
            assert code in self.report.covers

    def test_partial_patient(self):
        assert "Z10" in self.report.partial

    def test_uncovered_nominal_identity(self):
        assert "Z1" in self.report.uncovered


class TestDecisionMatrixVerbalCopular:
    def setup_method(self):
        self.report = generate_coverage_report(WordClass.VERBAL_COPULAR, word="كان")

    def test_covers_predicative(self):
        assert "Z19" in self.report.covers

    def test_partial_event(self):
        assert "Z6" in self.report.partial

    def test_uncovered_nominal_identity(self):
        assert "Z1" in self.report.uncovered


class TestDecisionMatrixNominalCopular:
    def setup_method(self):
        self.report = generate_coverage_report(WordClass.NOMINAL_COPULAR, word="إن")

    def test_covers_assertion(self):
        assert "Z20" in self.report.covers

    def test_partial_nominal_competence(self):
        assert "Z17" in self.report.partial

    def test_uncovered_event(self):
        assert "Z6" in self.report.uncovered


# ── Phase 2: all 20 axes present ────────────────────────────────────


def test_all_zero_types_present_in_details():
    report = generate_coverage_report(WordClass.JAMID)
    codes = {d.zero_code for d in report.details}
    expected = {z.name for z in LinguisticZeroType}
    assert codes == expected


def test_details_partition_covers_partial_uncovered():
    """covers + partial + uncovered must partition all 20 Z-codes."""
    report = generate_coverage_report(WordClass.VERBAL_COMPETENT)
    all_from_summary = set(report.covers) | set(report.partial) | set(report.uncovered)
    all_codes = {z.name for z in LinguisticZeroType}
    assert all_from_summary == all_codes
    # No overlaps
    assert len(report.covers) + len(report.partial) + len(report.uncovered) == 20


# ── Phase 3: pattern hints ───────────────────────────────────────────


class TestPatternHintFa3il:
    """Pattern 'فاعل' should promote Z9 to covers."""

    def test_promote_z9_to_covers(self):
        # DERIVED base: Z9 is in partial
        base = generate_coverage_report(WordClass.DERIVED)
        assert "Z9" in base.partial or "Z9" in base.uncovered

        with_hint = generate_coverage_report(WordClass.DERIVED, pattern="فاعل")
        assert "Z9" in with_hint.covers

    def test_note_mentions_pattern(self):
        report = generate_coverage_report(WordClass.DERIVED, pattern="فاعل")
        assert any("فاعل" in note for note in report.notes)


class TestPatternHintMaf3ul:
    """Pattern 'مفعول' should promote Z10 to covers."""

    def test_promote_z10_to_covers(self):
        with_hint = generate_coverage_report(WordClass.DERIVED, pattern="مفعول")
        assert "Z10" in with_hint.covers


class TestPatternHintMasdar:
    """Pattern 'مصدر' should promote Z6 to covers."""

    def test_promote_z6_to_covers(self):
        report = generate_coverage_report(WordClass.MASDAR, pattern="مصدر")
        assert "Z6" in report.covers


class TestPatternHintFa3Ala:
    """Pattern 'فعّل' promotes Z13 to covers."""

    def test_promote_z13_to_covers(self):
        report = generate_coverage_report(WordClass.DERIVED, pattern="فعّل")
        assert "Z13" in report.covers

    def test_promote_z9_z10_to_partial(self):
        # start from JAMID (no coverage of Z9/Z10)
        base = generate_coverage_report(WordClass.JAMID)
        assert "Z9" in base.uncovered
        with_hint = generate_coverage_report(WordClass.JAMID, pattern="فعّل")
        assert "Z9" in with_hint.partial
        assert "Z10" in with_hint.partial


class TestPatternHintIftaCala:
    def test_promote_z13_to_covers(self):
        report = generate_coverage_report(WordClass.DERIVED, pattern="افتعل")
        assert "Z13" in report.covers

    def test_promote_z11_z12_to_partial_when_uncovered(self):
        # JAMID has Z11/Z12 uncovered; افتعل should raise them to partial
        report = generate_coverage_report(WordClass.JAMID, pattern="افتعل")
        assert "Z11" in report.partial
        assert "Z12" in report.partial


# ── Phase 4: promote_to_covers never downgrades existing covers ───────


def test_covers_never_downgraded_by_pattern_hint():
    """A 'promote_to_partial' hint must not lower a COVERS status."""
    # VERBAL_COMPETENT covers Z6; hint 'مصدر' also promotes Z6 to covers
    # → should remain COVERS, not become PARTIAL
    report = generate_coverage_report(WordClass.VERBAL_COMPETENT, pattern="مصدر")
    assert "Z6" in report.covers


# ── Phase 5: analyze_word_zero_coverage ─────────────────────────────


class TestAnalyzeWordAutoInference:
    def test_hatha_inferred_as_referential(self):
        report = analyze_word_zero_coverage("هذا")
        assert report.word_class is WordClass.REFERENTIAL_BUILTINS
        assert "Z4" in report.covers

    def test_kana_inferred_as_verbal_copular(self):
        report = analyze_word_zero_coverage("كان")
        assert report.word_class is WordClass.VERBAL_COPULAR
        assert "Z19" in report.covers

    def test_inna_inferred_as_nominal_copular(self):
        report = analyze_word_zero_coverage("إن")
        assert report.word_class is WordClass.NOMINAL_COPULAR
        assert "Z20" in report.covers

    def test_kataba_uses_lexicon(self):
        """'كتب' is in the mini-lexicon → POS.FI3L → VERBAL_COMPETENT."""
        report = analyze_word_zero_coverage("كتب")
        assert report.word_class is WordClass.VERBAL_COMPETENT
        assert report.root == ("ك", "ت", "ب")

    def test_unknown_word_returns_jamid(self):
        report = analyze_word_zero_coverage("خلخلنجي")
        assert isinstance(report, WordZeroCoverageReport)
        assert len(report.details) == 20
        assert report.word_class is WordClass.JAMID


class TestAnalyzeWordExplicitOverrides:
    def test_explicit_class_overrides_inference(self):
        report = analyze_word_zero_coverage("هذا", class_name="JAMID")
        assert report.word_class is WordClass.JAMID

    def test_explicit_pattern_applied(self):
        report = analyze_word_zero_coverage("كتب", class_name="DERIVED", pattern="فاعل")
        assert report.word_class is WordClass.DERIVED
        assert "Z9" in report.covers

    def test_explicit_root_preserved(self):
        report = analyze_word_zero_coverage(
            "مكتوب", class_name="DERIVED", root=("ك", "ت", "ب")
        )
        assert report.root == ("ك", "ت", "ب")

    def test_class_name_case_insensitive(self):
        report = analyze_word_zero_coverage("رجل", class_name="jamid")
        assert report.word_class is WordClass.JAMID

    def test_invalid_class_name_raises(self):
        with pytest.raises(KeyError):
            analyze_word_zero_coverage("رجل", class_name="NOTACLASS")


# ── Phase 6: ZeroCoverageDetail properties ───────────────────────────


def test_zero_coverage_detail_zero_code():
    detail = ZeroCoverageDetail(
        zero_type=LinguisticZeroType.Z6,
        coverage=ZeroCoverage.COVERS,
    )
    assert detail.zero_code == "Z6"


def test_zero_coverage_detail_zero_name():
    detail = ZeroCoverageDetail(
        zero_type=LinguisticZeroType.Z1,
        coverage=ZeroCoverage.PARTIAL,
    )
    assert detail.zero_name == "هوية اسمية"


def test_all_zero_types_have_arabic_name():
    for z in LinguisticZeroType:
        assert isinstance(z.arabic_name, str)
        assert len(z.arabic_name) > 0


# ── Phase 7: export — JSON ───────────────────────────────────────────


class TestReportToJson:
    def setup_method(self):
        self.report = generate_coverage_report(
            WordClass.VERBAL_COMPETENT,
            pattern="فعل",
            root=("ك", "ت", "ب"),
            word="كتب",
        )
        self.data = json.loads(report_to_json(self.report))

    def test_input_keys(self):
        assert set(self.data["input"].keys()) == {"word", "word_class", "pattern", "root"}

    def test_word_class_name(self):
        assert self.data["input"]["word_class"] == "VERBAL_COMPETENT"

    def test_coverage_keys(self):
        assert set(self.data["coverage"].keys()) == {"covers", "partial", "uncovered"}

    def test_zero_details_count(self):
        assert len(self.data["zero_details"]) == 20

    def test_zero_details_fields(self):
        first = self.data["zero_details"][0]
        assert set(first.keys()) == {"zero_code", "zero_name", "coverage"}

    def test_coverage_values_are_lowercase(self):
        for item in self.data["zero_details"]:
            assert item["coverage"] in ("covers", "partial", "uncovered")

    def test_notes_is_list(self):
        assert isinstance(self.data["notes"], list)
        assert len(self.data["notes"]) > 0

    def test_root_is_list(self):
        assert self.data["input"]["root"] == ["ك", "ت", "ب"]

    def test_ensure_ascii_false_preserves_arabic(self):
        s = report_to_json(self.report, ensure_ascii=False)
        assert "كتب" in s

    def test_ensure_ascii_true_escapes_arabic(self):
        s = report_to_json(self.report, ensure_ascii=True)
        assert "\\u" in s


# ── Phase 8: export — CSV ────────────────────────────────────────────


class TestReportToCsv:
    def setup_method(self):
        self.report = generate_coverage_report(
            WordClass.JAMID,
            word="رجل",
            root=("ر", "ج", "ل"),
        )

    def test_csv_file_created(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            path = tmp.name
        try:
            report_to_csv(self.report, path)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_csv_has_z_columns(self):
        import csv as _csv

        with tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False, mode="w"
        ) as tmp:
            path = tmp.name
        try:
            report_to_csv(self.report, path)
            with open(path, encoding="utf-8-sig") as fh:
                reader = _csv.DictReader(fh)
                headers = reader.fieldnames or []
            for i in range(1, 21):
                assert f"Z{i}" in headers
        finally:
            os.unlink(path)

    def test_csv_word_class_value(self):
        import csv as _csv

        with tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False, mode="w"
        ) as tmp:
            path = tmp.name
        try:
            report_to_csv(self.report, path)
            with open(path, encoding="utf-8-sig") as fh:
                reader = _csv.DictReader(fh)
                row = next(reader)
            assert row["word_class"] == "JAMID"
            assert row["word"] == "رجل"
        finally:
            os.unlink(path)

    def test_csv_root_joined_with_dash(self):
        import csv as _csv

        with tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False, mode="w"
        ) as tmp:
            path = tmp.name
        try:
            report_to_csv(self.report, path)
            with open(path, encoding="utf-8-sig") as fh:
                reader = _csv.DictReader(fh)
                row = next(reader)
            assert row["root"] == "ر-ج-ل"
        finally:
            os.unlink(path)


# ── Phase 9: pipeline integration ───────────────────────────────────


def test_pipeline_analyze_zeros_false():
    from arabic_engine.pipeline import run

    result = run("زيد كتب الرسالة")
    assert result.word_zero_coverage == []


def test_pipeline_analyze_zeros_true():
    from arabic_engine.pipeline import run

    result = run("زيد كتب الرسالة", analyze_zeros=True)
    assert len(result.word_zero_coverage) == len(result.tokens)
    for rep in result.word_zero_coverage:
        assert isinstance(rep, WordZeroCoverageReport)
        assert len(rep.details) == 20


def test_pipeline_zero_coverage_reports_are_typed():
    from arabic_engine.pipeline import run

    result = run("كتب", analyze_zeros=True)
    assert len(result.word_zero_coverage) == 1
    rep = result.word_zero_coverage[0]
    assert rep.word == "كتب"
    assert isinstance(rep.word_class, WordClass)


# ── Phase 10: core re-exports ────────────────────────────────────────


def test_core_reexports_enums():
    from arabic_engine.core import LinguisticZeroType as LZT
    from arabic_engine.core import WordClass as WC
    from arabic_engine.core import ZeroCoverage as ZC

    assert LZT.Z1.value == 1
    assert WC.JAMID is WordClass.JAMID
    assert ZC.COVERS is ZeroCoverage.COVERS


def test_core_reexports_types():
    from arabic_engine.core import WordZeroCoverageReport as WZCR
    from arabic_engine.core import ZeroCoverageDetail as ZCD

    assert WZCR is WordZeroCoverageReport
    assert ZCD is ZeroCoverageDetail


def test_signified_reexport():
    from arabic_engine.signified import analyze_word_zero_coverage as awzc

    assert callable(awzc)
    report = awzc("هذا")
    assert report.word_class is WordClass.REFERENTIAL_BUILTINS
