"""Tests for Particle Fractal Constitution v1 — دستور الحرف الفراكتالي."""

from __future__ import annotations

import pytest

from arabic_engine.core.enums import (
    ParticleDalala,
    ParticleDirection,
    ParticleEffect,
    ParticleKind,
    ParticleReadiness,
    ParticleScope,
)
from arabic_engine.core.types import (
    ParticleFractalTrace,
    ParticleMinimum,
    ParticleRecord,
    ParticleValidation,
)
from arabic_engine.signified.particle_v1 import (
    analyze_dalala,
    batch_build,
    build_particle,
    check_minimum,
    classify_particle,
    compute_readiness,
    trace_fractal_law,
    validate_particle,
)

# ── 5.1 Enum completeness tests ─────────────────────────────────────


class TestEnumCompleteness:
    """Verify enum member counts match the constitution specification."""

    def test_particle_kind_count(self) -> None:
        assert len(ParticleKind) == 12

    def test_particle_direction_count(self) -> None:
        assert len(ParticleDirection) == 7

    def test_particle_scope_count(self) -> None:
        assert len(ParticleScope) == 5

    def test_particle_effect_count(self) -> None:
        assert len(ParticleEffect) == 6

    def test_particle_readiness_count(self) -> None:
        assert len(ParticleReadiness) == 3

    def test_particle_dalala_count(self) -> None:
        assert len(ParticleDalala) == 3


# ── 5.2 Classification tests ────────────────────────────────────────


class TestClassifyParticle:
    """Test classify_particle for known and unknown materials."""

    @pytest.mark.parametrize("material", ["من", "في", "على", "إلى", "عن", "ب", "ل", "ك"])
    def test_prepositions_are_nisba(self, material: str) -> None:
        rec = classify_particle(material)
        assert rec.kind is ParticleKind.NISBA

    @pytest.mark.parametrize("material", ["و", "ف", "ثم", "أو", "بل", "أم"])
    def test_conjunctions_are_atf(self, material: str) -> None:
        rec = classify_particle(material)
        assert rec.kind is ParticleKind.ATF

    @pytest.mark.parametrize("material", ["لا", "لم", "لن", "ما"])
    def test_negation_is_nafy(self, material: str) -> None:
        rec = classify_particle(material)
        assert rec.kind is ParticleKind.NAFY

    @pytest.mark.parametrize("material", ["إذا", "لو", "إن", "لولا"])
    def test_conditional_is_shart(self, material: str) -> None:
        rec = classify_particle(material)
        assert rec.kind is ParticleKind.SHART

    @pytest.mark.parametrize("material", ["هل", "أ"])
    def test_interrogative_is_istifham(self, material: str) -> None:
        rec = classify_particle(material)
        assert rec.kind is ParticleKind.ISTIFHAM

    @pytest.mark.parametrize("material", ["إنّ", "كأنّ", "كأن"])
    def test_emphatic_is_tawkid(self, material: str) -> None:
        rec = classify_particle(material)
        assert rec.kind is ParticleKind.TAWKID

    @pytest.mark.parametrize("material", ["إلا", "غير", "سوى"])
    def test_exception_is_istithnaa(self, material: str) -> None:
        rec = classify_particle(material)
        assert rec.kind is ParticleKind.ISTITHNAA

    @pytest.mark.parametrize("material", ["حتى", "كي"])
    def test_purpose_is_ghaya(self, material: str) -> None:
        rec = classify_particle(material)
        assert rec.kind is ParticleKind.GHAYA

    @pytest.mark.parametrize("material", ["يا", "أيّها"])
    def test_vocative_is_ibtidaa(self, material: str) -> None:
        rec = classify_particle(material)
        assert rec.kind is ParticleKind.IBTIDAA

    def test_unknown_material_is_incomplete(self) -> None:
        rec = classify_particle("مجهول")
        assert rec.readiness is ParticleReadiness.INCOMPLETE
        assert rec.readiness_score == 0.0

    def test_known_particle_is_ready(self) -> None:
        rec = classify_particle("من")
        assert rec.readiness is ParticleReadiness.READY
        assert rec.readiness_score == 1.0

    def test_record_is_frozen(self) -> None:
        rec = classify_particle("في")
        with pytest.raises(AttributeError):
            rec.material = "x"  # type: ignore[misc]

    def test_auto_id_generation(self) -> None:
        rec = classify_particle("من")
        assert rec.particle_id.startswith("PRT_")

    def test_explicit_id(self) -> None:
        rec = classify_particle("من", particle_id="MY_ID")
        assert rec.particle_id == "MY_ID"

    def test_direction_override_min(self) -> None:
        """من should have IBTIDAAIYYA direction (override, not default ZARFIYYA)."""
        rec = classify_particle("من")
        assert rec.direction is ParticleDirection.IBTIDAAIYYA

    def test_direction_override_ila(self) -> None:
        """إلى should have INTIHAAIYYA direction."""
        rec = classify_particle("إلى")
        assert rec.direction is ParticleDirection.INTIHAAIYYA

    def test_preposition_effect_is_jarr(self) -> None:
        rec = classify_particle("في")
        assert rec.effect is ParticleEffect.JARR

    def test_conjunction_effect_is_rabt_wasl(self) -> None:
        rec = classify_particle("و")
        assert rec.effect is ParticleEffect.RABT_WASL

    def test_conditional_effect_is_jazm(self) -> None:
        rec = classify_particle("لم")
        assert rec.effect is ParticleEffect.TAHWIL_JIHA


# ── 5.3 Minimum-completeness tests ──────────────────────────────────


class TestCheckMinimum:
    """Test the 8 minimum-completeness checks."""

    def test_valid_particle_all_true(self) -> None:
        rec = classify_particle("من")
        m = check_minimum(rec)
        assert m.thuboot is True
        assert m.hadd is True
        assert m.imtidad is True
        assert m.muqawwim is True
        assert m.alaqa_binyawiyya is True
        assert m.intizam is True
        assert m.wahda is True
        assert m.qabiliyyat_ta3yin is True

    def test_unknown_material_has_false_fields(self) -> None:
        rec = classify_particle("مجهول")
        m = check_minimum(rec)
        # thuboot is True (has material + direction)
        assert m.thuboot is True
        # hadd is False (not recognised)
        assert m.hadd is False
        # intizam is False (not in known door)
        assert m.intizam is False
        # qabiliyyat_ta3yin is False
        assert m.qabiliyyat_ta3yin is False

    def test_minimum_is_frozen(self) -> None:
        rec = classify_particle("في")
        m = check_minimum(rec)
        with pytest.raises(AttributeError):
            m.thuboot = False  # type: ignore[misc]


# ── 5.4 Validation tests ────────────────────────────────────────────


class TestValidateParticle:
    """Test acceptance/rejection logic."""

    def test_valid_particle_accepted(self) -> None:
        rec = classify_particle("من")
        m = check_minimum(rec)
        v = validate_particle(rec, m)
        assert v.is_valid is True
        assert v.acceptance_score == 1.0
        assert v.rejection_reasons == ()

    def test_unknown_particle_rejected(self) -> None:
        rec = classify_particle("مجهول")
        m = check_minimum(rec)
        v = validate_particle(rec, m)
        assert v.is_valid is False
        assert len(v.rejection_reasons) > 0

    def test_acceptance_score_range(self) -> None:
        rec = classify_particle("في")
        m = check_minimum(rec)
        v = validate_particle(rec, m)
        assert 0.0 <= v.acceptance_score <= 1.0

    def test_validation_is_frozen(self) -> None:
        rec = classify_particle("على")
        m = check_minimum(rec)
        v = validate_particle(rec, m)
        with pytest.raises(AttributeError):
            v.is_valid = False  # type: ignore[misc]

    def test_validation_particle_id_matches(self) -> None:
        rec = classify_particle("في")
        m = check_minimum(rec)
        v = validate_particle(rec, m)
        assert v.particle_id == rec.particle_id


# ── 5.5 Fractal law trace tests ─────────────────────────────────────


class TestTraceFractalLaw:
    """Test the 6-step fractal law trace."""

    def test_well_formed_particle_all_true(self) -> None:
        rec = classify_particle("من")
        t = trace_fractal_law(rec)
        assert t.ta3yin is True
        assert t.hifz is True
        assert t.rabt is True
        assert t.hukm is True
        assert t.intiqal is True
        assert t.radd is True

    def test_unknown_particle_incomplete_trace(self) -> None:
        rec = classify_particle("مجهول")
        t = trace_fractal_law(rec)
        assert t.ta3yin is False
        assert t.intiqal is False
        assert t.radd is False

    def test_trace_is_frozen(self) -> None:
        rec = classify_particle("و")
        t = trace_fractal_law(rec)
        with pytest.raises(AttributeError):
            t.ta3yin = False  # type: ignore[misc]

    def test_trace_particle_id_matches(self) -> None:
        rec = classify_particle("و")
        t = trace_fractal_law(rec)
        assert t.particle_id == rec.particle_id


# ── 5.6 Readiness score tests ───────────────────────────────────────


class TestComputeReadiness:
    """Test readiness score computation."""

    def test_known_particle_score_is_1(self) -> None:
        rec = classify_particle("من")
        score = compute_readiness(rec)
        assert score == 1.0

    def test_unknown_particle_score_below_threshold(self) -> None:
        rec = classify_particle("مجهول")
        score = compute_readiness(rec)
        assert score < 1.0

    def test_score_in_range(self) -> None:
        rec = classify_particle("في")
        score = compute_readiness(rec)
        assert 0.0 <= score <= 1.0


# ── 5.7 Dalala tests ────────────────────────────────────────────────


class TestAnalyzeDalala:
    """Test signification-type analysis."""

    def test_preposition_is_mutabaqa(self) -> None:
        """Prepositions directly denote their relation → مطابقة."""
        rec = classify_particle("من")
        assert analyze_dalala(rec) is ParticleDalala.MUTABAQA

    def test_conjunction_is_tadammun(self) -> None:
        """Conjunctions include relation implicitly → تضمن."""
        rec = classify_particle("و")
        assert analyze_dalala(rec) is ParticleDalala.TADAMMUN

    def test_modality_change_is_iltizam(self) -> None:
        """Modality-changing particles imply derived effects → التزام."""
        rec = classify_particle("قد")
        assert analyze_dalala(rec) is ParticleDalala.ILTIZAM

    def test_negation_is_iltizam(self) -> None:
        """Negation particles change modality → التزام."""
        rec = classify_particle("لا")
        assert analyze_dalala(rec) is ParticleDalala.ILTIZAM

    def test_emphatic_is_mutabaqa(self) -> None:
        """Emphatic particles with NASB effect → مطابقة."""
        rec = classify_particle("إنّ")
        assert analyze_dalala(rec) is ParticleDalala.MUTABAQA

    def test_conditional_is_mutabaqa(self) -> None:
        """Conditional particles with JAZM effect → مطابقة."""
        rec = classify_particle("إذا")
        assert analyze_dalala(rec) is ParticleDalala.MUTABAQA


# ── 5.8 End-to-end tests ────────────────────────────────────────────


class TestBuildParticle:
    """Test the convenience pipeline function."""

    def test_build_known_particle(self) -> None:
        rec, val, trace = build_particle("من")
        assert isinstance(rec, ParticleRecord)
        assert isinstance(val, ParticleValidation)
        assert isinstance(trace, ParticleFractalTrace)
        assert val.is_valid is True
        assert trace.radd is True

    def test_build_unknown_particle(self) -> None:
        rec, val, trace = build_particle("xyz")
        assert val.is_valid is False
        assert trace.ta3yin is False

    def test_build_returns_matching_ids(self) -> None:
        rec, val, trace = build_particle("في")
        assert val.particle_id == rec.particle_id
        assert trace.particle_id == rec.particle_id


class TestBatchBuild:
    """Test batch processing."""

    def test_batch_build_multiple(self) -> None:
        results = batch_build(["من", "و", "مجهول"])
        assert len(results) == 3
        # First two are valid, third is not
        assert results[0][1].is_valid is True
        assert results[1][1].is_valid is True
        assert results[2][1].is_valid is False

    def test_batch_build_empty(self) -> None:
        results = batch_build([])
        assert results == []

    def test_batch_build_single(self) -> None:
        results = batch_build(["في"])
        assert len(results) == 1
        assert results[0][0].kind is ParticleKind.NISBA


# ── Dataclass structural tests ──────────────────────────────────────


class TestDataclasses:
    """Verify dataclass structure and frozen-ness."""

    def test_particle_record_fields(self) -> None:
        rec = classify_particle("من")
        assert hasattr(rec, "particle_id")
        assert hasattr(rec, "material")
        assert hasattr(rec, "direction")
        assert hasattr(rec, "kind")
        assert hasattr(rec, "scope")
        assert hasattr(rec, "effect")
        assert hasattr(rec, "readiness")
        assert hasattr(rec, "readiness_score")

    def test_particle_minimum_defaults(self) -> None:
        m = ParticleMinimum()
        assert m.thuboot is False
        assert m.hadd is False

    def test_particle_validation_defaults(self) -> None:
        v = ParticleValidation(particle_id="test", is_valid=False, minimum=ParticleMinimum())
        assert v.acceptance_score == 0.0
        assert v.rejection_reasons == ()

    def test_particle_fractal_trace_defaults(self) -> None:
        t = ParticleFractalTrace(particle_id="test")
        assert t.ta3yin is False
        assert t.radd is False


# ── Import re-export tests ──────────────────────────────────────────


class TestReExports:
    """Verify core re-exports work."""

    def test_enums_from_core(self) -> None:
        from arabic_engine.core import (
            ParticleDalala,
            ParticleDirection,
            ParticleEffect,
            ParticleKind,
            ParticleReadiness,
            ParticleScope,
        )
        assert len(ParticleKind) == 12
        assert len(ParticleDirection) == 7
        assert len(ParticleScope) == 5
        assert len(ParticleEffect) == 6
        assert len(ParticleReadiness) == 3
        assert len(ParticleDalala) == 3

    def test_types_from_core(self) -> None:
        from arabic_engine.core import (
            ParticleFractalTrace,
            ParticleMinimum,
            ParticleRecord,
            ParticleValidation,
        )
        # Verify they are importable and are types
        assert ParticleRecord is not None
        assert ParticleMinimum is not None
        assert ParticleValidation is not None
        assert ParticleFractalTrace is not None
