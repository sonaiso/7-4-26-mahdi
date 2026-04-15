"""Tests for Verb Fractal Constitution v1.

Covers:
  - Enum completeness (13 enums)
  - Dataclass construction and immutability (6 types)
  - All 8 public API functions
  - Nasikh, Mazid, and readiness threshold edge cases
  - Re-export verification
"""

from __future__ import annotations

import pytest

from arabic_engine.core.enums import (
    NasikhType,
    VerbAugmentation,
    VerbBab,
    VerbDerivativeType,
    VerbEventType,
    VerbGender,
    VerbMode,
    VerbNumber,
    VerbPerson,
    VerbReadiness,
    VerbTense,
    VerbTransitivity,
    VerbVoice,
)
from arabic_engine.core.types import (
    VerbConstitutionRecord,
    VerbDerivativeRecord,
    VerbEventRecord,
    VerbInflection,
    VerbMasdarRecord,
    VerbReadinessScore,
)
from arabic_engine.signified.verb_constitution import (
    batch_build,
    build_derivatives,
    build_masdar,
    build_verb_constitution,
    classify_verb_event,
    classify_verb_inflection,
    compute_readiness,
    validate_verb,
)

# ═══════════════════════════════════════════════════════════════════════
# 5.1 — Enum completeness
# ═══════════════════════════════════════════════════════════════════════


class TestEnumCompleteness:
    """Verify exact member counts for all 13 verb-related enums."""

    def test_verb_tense_count(self) -> None:
        assert len(VerbTense) == 3

    def test_verb_voice_count(self) -> None:
        assert len(VerbVoice) == 2

    def test_verb_person_count(self) -> None:
        assert len(VerbPerson) == 3

    def test_verb_number_count(self) -> None:
        assert len(VerbNumber) == 3

    def test_verb_gender_count(self) -> None:
        assert len(VerbGender) == 2

    def test_verb_transitivity_count(self) -> None:
        assert len(VerbTransitivity) == 4

    def test_verb_bab_count(self) -> None:
        assert len(VerbBab) == 7

    def test_verb_mode_count(self) -> None:
        assert len(VerbMode) == 3

    def test_verb_augmentation_count(self) -> None:
        assert len(VerbAugmentation) == 10

    def test_nasikh_type_count(self) -> None:
        assert len(NasikhType) == 3

    def test_verb_event_type_count(self) -> None:
        assert len(VerbEventType) == 6

    def test_verb_derivative_type_count(self) -> None:
        assert len(VerbDerivativeType) == 8

    def test_verb_readiness_count(self) -> None:
        assert len(VerbReadiness) == 3


# ═══════════════════════════════════════════════════════════════════════
# 5.2 — Dataclass construction & immutability
# ═══════════════════════════════════════════════════════════════════════


class TestDataclassConstruction:
    """Verify frozen dataclass creation and immutability."""

    def test_verb_inflection_construction(self) -> None:
        vi = VerbInflection(
            surface="كَتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        assert vi.surface == "كَتَبَ"
        assert vi.root == ("ك", "ت", "ب")
        assert vi.nasikh_type is None

    def test_verb_inflection_frozen(self) -> None:
        vi = VerbInflection(
            surface="كَتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        with pytest.raises(AttributeError):
            vi.surface = "x"  # type: ignore[misc]

    def test_verb_event_record_construction(self) -> None:
        ev = VerbEventRecord(event_type=VerbEventType.SIMPLE_OCCURRENCE)
        assert ev.event_type is VerbEventType.SIMPLE_OCCURRENCE
        assert ev.has_causality is False

    def test_verb_event_record_frozen(self) -> None:
        ev = VerbEventRecord(event_type=VerbEventType.SIMPLE_OCCURRENCE)
        with pytest.raises(AttributeError):
            ev.has_causality = True  # type: ignore[misc]

    def test_verb_derivative_record_construction(self) -> None:
        dr = VerbDerivativeRecord(
            derivative_type=VerbDerivativeType.ISM_FA3IL,
            form="كاتِب",
        )
        assert dr.form == "كاتِب"

    def test_verb_masdar_record_construction(self) -> None:
        mr = VerbMasdarRecord(masdar_form="كِتَابَة")
        assert mr.masdar_form == "كِتَابَة"
        assert mr.is_qiyasi is True

    def test_verb_readiness_score_construction(self) -> None:
        rs = VerbReadinessScore(
            direction_score=1.0,
            time_score=1.0,
            person_score=1.0,
            valence_score=1.0,
            mode_score=1.0,
            recover_score=1.0,
            total=1.0,
            status=VerbReadiness.READY,
        )
        assert rs.total == 1.0
        assert rs.status is VerbReadiness.READY

    def test_verb_constitution_record_construction(self) -> None:
        vi = VerbInflection(
            surface="كَتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        ev = VerbEventRecord(event_type=VerbEventType.SIMPLE_OCCURRENCE)
        rs = VerbReadinessScore(
            direction_score=1.0,
            time_score=1.0,
            person_score=1.0,
            valence_score=1.0,
            mode_score=1.0,
            recover_score=1.0,
            total=1.0,
            status=VerbReadiness.READY,
        )
        rec = VerbConstitutionRecord(
            record_id="VRC_001",
            inflection=vi,
            event=ev,
            masdar=None,
            derivatives=(),
            readiness=rs,
            fractal_cycle="تعيين → حفظ → ربط → حكم → انتقال → رد",
            valid=True,
        )
        assert rec.record_id == "VRC_001"
        assert rec.valid is True


# ═══════════════════════════════════════════════════════════════════════
# 5.3 — API function tests
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyVerbInflection:
    """Tests for classify_verb_inflection."""

    def test_kataba(self) -> None:
        vi = classify_verb_inflection(
            surface="كَتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        assert isinstance(vi, VerbInflection)
        assert vi.surface == "كَتَبَ"
        assert vi.bab is VerbBab.FA3ALA_YAF3ULU
        assert vi.tense is VerbTense.MADI
        assert vi.mode is VerbMode.MUJARRAD

    def test_yaktub(self) -> None:
        vi = classify_verb_inflection(
            surface="يَكْتُبُ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MUDARI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        assert vi.tense is VerbTense.MUDARI


class TestClassifyVerbEvent:
    """Tests for classify_verb_event."""

    def test_simple_occurrence(self) -> None:
        ev = classify_verb_event(VerbEventType.SIMPLE_OCCURRENCE)
        assert ev.event_type is VerbEventType.SIMPLE_OCCURRENCE
        assert ev.has_causality is False

    def test_causation(self) -> None:
        ev = classify_verb_event(
            VerbEventType.CAUSATION, has_causality=True
        )
        assert ev.has_causality is True

    def test_becoming(self) -> None:
        ev = classify_verb_event(VerbEventType.BECOMING)
        assert ev.event_type is VerbEventType.BECOMING

    def test_transformation(self) -> None:
        ev = classify_verb_event(VerbEventType.TRANSFORMATION)
        assert ev.event_type is VerbEventType.TRANSFORMATION

    def test_being_affected(self) -> None:
        ev = classify_verb_event(VerbEventType.BEING_AFFECTED, has_mutawa3a=True)
        assert ev.has_mutawa3a is True

    def test_linking(self) -> None:
        ev = classify_verb_event(VerbEventType.LINKING)
        assert ev.event_type is VerbEventType.LINKING


class TestBuildMasdar:
    """Tests for build_masdar."""

    def test_kitaba(self) -> None:
        mr = build_masdar("كِتَابَة")
        assert mr.masdar_form == "كِتَابَة"
        assert mr.is_qiyasi is True

    def test_samaa(self) -> None:
        mr = build_masdar("رَحْمَة", is_qiyasi=False, notes="سماعي")
        assert mr.is_qiyasi is False
        assert mr.notes == "سماعي"


class TestBuildDerivatives:
    """Tests for build_derivatives."""

    def test_katib_maktoob(self) -> None:
        ders = build_derivatives([
            (VerbDerivativeType.ISM_FA3IL, "كاتِب"),
            (VerbDerivativeType.ISM_MAF3UL, "مَكْتُوب"),
        ])
        assert len(ders) == 2
        assert ders[0].derivative_type is VerbDerivativeType.ISM_FA3IL
        assert ders[0].form == "كاتِب"
        assert ders[1].derivative_type is VerbDerivativeType.ISM_MAF3UL

    def test_empty(self) -> None:
        ders = build_derivatives([])
        assert ders == ()


class TestComputeReadiness:
    """Tests for compute_readiness."""

    def test_full_readiness(self) -> None:
        vi = classify_verb_inflection(
            surface="كَتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        ev = classify_verb_event(VerbEventType.SIMPLE_OCCURRENCE)
        rs = compute_readiness(vi, ev, None, ())
        assert rs.status is VerbReadiness.READY
        assert rs.total == pytest.approx(1.0)

    def test_partial_readiness_empty_root(self) -> None:
        vi = classify_verb_inflection(
            surface="كَتَبَ",
            root=(),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        ev = classify_verb_event(VerbEventType.SIMPLE_OCCURRENCE)
        rs = compute_readiness(vi, ev, None, ())
        # 5/6 ≈ 0.833 → READY (>= 0.8)
        assert rs.recover_score == 0.0
        assert rs.status is VerbReadiness.READY
        assert rs.total == pytest.approx(5.0 / 6.0)


class TestValidateVerb:
    """Tests for validate_verb."""

    def test_valid_mujarrad(self) -> None:
        vi = classify_verb_inflection(
            surface="كَتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        assert validate_verb(vi) is True

    def test_invalid_empty_surface(self) -> None:
        vi = classify_verb_inflection(
            surface="",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        assert validate_verb(vi) is False

    def test_invalid_empty_root(self) -> None:
        vi = classify_verb_inflection(
            surface="كَتَبَ",
            root=(),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        assert validate_verb(vi) is False

    def test_invalid_nasikh_missing_type(self) -> None:
        vi = classify_verb_inflection(
            surface="كانَ",
            root=("ك", "و", "ن"),
            bab=VerbBab.OTHER,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.LAZIM,
            mode=VerbMode.NASIKH,
            augmentation=VerbAugmentation.NONE,
            nasikh_type=None,
        )
        assert validate_verb(vi) is False

    def test_invalid_mazid_no_augmentation(self) -> None:
        vi = classify_verb_inflection(
            surface="أَكْتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.OTHER,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MAZID,
            augmentation=VerbAugmentation.NONE,
        )
        assert validate_verb(vi) is False

    def test_invalid_mujarrad_with_augmentation(self) -> None:
        vi = classify_verb_inflection(
            surface="كَتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.IF3AL,
        )
        assert validate_verb(vi) is False


class TestBuildVerbConstitution:
    """Tests for build_verb_constitution end-to-end."""

    def test_kataba_end_to_end(self) -> None:
        rec = build_verb_constitution(
            surface="كَتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
            event_type=VerbEventType.SIMPLE_OCCURRENCE,
            masdar_form="كِتَابَة",
            derivatives_data=[
                (VerbDerivativeType.ISM_FA3IL, "كاتِب"),
                (VerbDerivativeType.ISM_MAF3UL, "مَكْتُوب"),
            ],
        )
        assert isinstance(rec, VerbConstitutionRecord)
        assert rec.valid is True
        assert rec.inflection.surface == "كَتَبَ"
        assert rec.masdar is not None
        assert rec.masdar.masdar_form == "كِتَابَة"
        assert len(rec.derivatives) == 2
        assert rec.readiness.status is VerbReadiness.READY
        assert rec.fractal_cycle == "تعيين → حفظ → ربط → حكم → انتقال → رد"
        assert rec.record_id.startswith("VRC_")

    def test_with_explicit_record_id(self) -> None:
        rec = build_verb_constitution(
            surface="جَلَسَ",
            root=("ج", "ل", "س"),
            bab=VerbBab.FA3ALA_YAF3ILU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.LAZIM,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
            event_type=VerbEventType.SIMPLE_OCCURRENCE,
            record_id="VRC_CUSTOM_001",
        )
        assert rec.record_id == "VRC_CUSTOM_001"
        assert rec.valid is True

    def test_without_masdar_or_derivatives(self) -> None:
        rec = build_verb_constitution(
            surface="ذَهَبَ",
            root=("ذ", "ه", "ب"),
            bab=VerbBab.FA3ALA_YAF3ALU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.LAZIM,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
            event_type=VerbEventType.SIMPLE_OCCURRENCE,
        )
        assert rec.masdar is None
        assert rec.derivatives == ()
        assert rec.valid is True


class TestBatchBuild:
    """Tests for batch_build."""

    def test_multiple_verbs(self) -> None:
        specs = [
            {
                "surface": "كَتَبَ",
                "root": ("ك", "ت", "ب"),
                "bab": VerbBab.FA3ALA_YAF3ULU,
                "tense": VerbTense.MADI,
                "person": VerbPerson.THIRD,
                "number": VerbNumber.SINGULAR,
                "gender": VerbGender.MASCULINE,
                "voice": VerbVoice.ACTIVE,
                "transitivity": VerbTransitivity.MUTA3ADDI,
                "mode": VerbMode.MUJARRAD,
                "augmentation": VerbAugmentation.NONE,
                "event_type": VerbEventType.SIMPLE_OCCURRENCE,
            },
            {
                "surface": "جَلَسَ",
                "root": ("ج", "ل", "س"),
                "bab": VerbBab.FA3ALA_YAF3ILU,
                "tense": VerbTense.MADI,
                "person": VerbPerson.THIRD,
                "number": VerbNumber.SINGULAR,
                "gender": VerbGender.MASCULINE,
                "voice": VerbVoice.ACTIVE,
                "transitivity": VerbTransitivity.LAZIM,
                "mode": VerbMode.MUJARRAD,
                "augmentation": VerbAugmentation.NONE,
                "event_type": VerbEventType.SIMPLE_OCCURRENCE,
            },
        ]
        results = batch_build(specs)
        assert len(results) == 2
        assert results[0].inflection.surface == "كَتَبَ"
        assert results[1].inflection.surface == "جَلَسَ"

    def test_empty_batch(self) -> None:
        results = batch_build([])
        assert results == []


# ═══════════════════════════════════════════════════════════════════════
# 5.4 — Nasikh tests (Art. 46–50)
# ═══════════════════════════════════════════════════════════════════════


class TestNasikh:
    """Tests for copular (ناسخ) verbs."""

    def test_nasikh_kana(self) -> None:
        rec = build_verb_constitution(
            surface="كانَ",
            root=("ك", "و", "ن"),
            bab=VerbBab.OTHER,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.LAZIM,
            mode=VerbMode.NASIKH,
            augmentation=VerbAugmentation.NONE,
            event_type=VerbEventType.LINKING,
            nasikh_type=NasikhType.KANA,
        )
        assert rec.valid is True
        assert rec.inflection.nasikh_type is NasikhType.KANA
        assert rec.inflection.mode is VerbMode.NASIKH

    def test_nasikh_zanna(self) -> None:
        rec = build_verb_constitution(
            surface="ظَنَّ",
            root=("ظ", "ن", "ن"),
            bab=VerbBab.OTHER,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI_LI_ITHNAYN,
            mode=VerbMode.NASIKH,
            augmentation=VerbAugmentation.NONE,
            event_type=VerbEventType.LINKING,
            nasikh_type=NasikhType.ZANNA,
        )
        assert rec.valid is True
        assert rec.inflection.nasikh_type is NasikhType.ZANNA

    def test_nasikh_kada(self) -> None:
        rec = build_verb_constitution(
            surface="كادَ",
            root=("ك", "و", "د"),
            bab=VerbBab.OTHER,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.LAZIM,
            mode=VerbMode.NASIKH,
            augmentation=VerbAugmentation.NONE,
            event_type=VerbEventType.LINKING,
            nasikh_type=NasikhType.KADA,
        )
        assert rec.valid is True
        assert rec.inflection.nasikh_type is NasikhType.KADA


# ═══════════════════════════════════════════════════════════════════════
# 5.5 — Mazid tests (Art. 36–39)
# ═══════════════════════════════════════════════════════════════════════


class TestMazid:
    """Tests for augmented (مزيد) verbs."""

    def test_mazid_if3al(self) -> None:
        """إفعال — أَكْتَبَ"""
        rec = build_verb_constitution(
            surface="أَكْتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.OTHER,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MAZID,
            augmentation=VerbAugmentation.IF3AL,
            event_type=VerbEventType.CAUSATION,
            has_causality=True,
        )
        assert rec.valid is True
        assert rec.inflection.augmentation is VerbAugmentation.IF3AL
        assert rec.event.has_causality is True

    def test_mazid_tafa33ala(self) -> None:
        """تفعّل — تكسَّرَ"""
        rec = build_verb_constitution(
            surface="تكسَّرَ",
            root=("ك", "س", "ر"),
            bab=VerbBab.OTHER,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.LAZIM,
            mode=VerbMode.MAZID,
            augmentation=VerbAugmentation.TAFA33ALA,
            event_type=VerbEventType.TRANSFORMATION,
            has_mutawa3a=True,
        )
        assert rec.valid is True
        assert rec.inflection.augmentation is VerbAugmentation.TAFA33ALA
        assert rec.event.has_mutawa3a is True


# ═══════════════════════════════════════════════════════════════════════
# 5.6 — Readiness threshold tests (Art. 67)
# ═══════════════════════════════════════════════════════════════════════


class TestReadinessThreshold:
    """Test boundary values around θ_RV."""

    def test_threshold_exact(self) -> None:
        vi = classify_verb_inflection(
            surface="كَتَبَ",
            root=("ك", "ت", "ب"),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        ev = classify_verb_event(VerbEventType.SIMPLE_OCCURRENCE)
        # With custom threshold = 1.0, full root → total=1.0 → READY
        rs = compute_readiness(vi, ev, None, (), threshold=1.0)
        assert rs.status is VerbReadiness.READY

    def test_threshold_above(self) -> None:
        vi = classify_verb_inflection(
            surface="كَتَبَ",
            root=(),
            bab=VerbBab.FA3ALA_YAF3ULU,
            tense=VerbTense.MADI,
            person=VerbPerson.THIRD,
            number=VerbNumber.SINGULAR,
            gender=VerbGender.MASCULINE,
            voice=VerbVoice.ACTIVE,
            transitivity=VerbTransitivity.MUTA3ADDI,
            mode=VerbMode.MUJARRAD,
            augmentation=VerbAugmentation.NONE,
        )
        ev = classify_verb_event(VerbEventType.SIMPLE_OCCURRENCE)
        # 5/6 ≈ 0.833, threshold=0.9 → READY not met → PARTIAL
        rs = compute_readiness(vi, ev, None, (), threshold=0.9)
        assert rs.status is VerbReadiness.PARTIAL


# ═══════════════════════════════════════════════════════════════════════
# 5.7 — Re-export tests
# ═══════════════════════════════════════════════════════════════════════


class TestReExports:
    """Verify all new symbols are importable from arabic_engine.core."""

    def test_enum_re_exports(self) -> None:
        from arabic_engine.core import (
            NasikhType as NT,
        )
        from arabic_engine.core import (
            VerbAugmentation as VA,
        )
        from arabic_engine.core import (
            VerbBab as VB,
        )
        from arabic_engine.core import (
            VerbDerivativeType as VDT,
        )
        from arabic_engine.core import (
            VerbEventType as VET,
        )
        from arabic_engine.core import (
            VerbGender as VG,
        )
        from arabic_engine.core import (
            VerbMode as VM,
        )
        from arabic_engine.core import (
            VerbNumber as VN,
        )
        from arabic_engine.core import (
            VerbPerson as VP,
        )
        from arabic_engine.core import (
            VerbReadiness as VR,
        )
        from arabic_engine.core import (
            VerbTense as VTn,
        )
        from arabic_engine.core import (
            VerbTransitivity as VTr,
        )
        from arabic_engine.core import (
            VerbVoice as VV,
        )
        assert NT is NasikhType
        assert VA is VerbAugmentation
        assert VB is VerbBab
        assert VDT is VerbDerivativeType
        assert VET is VerbEventType
        assert VG is VerbGender
        assert VM is VerbMode
        assert VN is VerbNumber
        assert VP is VerbPerson
        assert VR is VerbReadiness
        assert VTn is VerbTense
        assert VTr is VerbTransitivity
        assert VV is VerbVoice

    def test_type_re_exports(self) -> None:
        from arabic_engine.core import (
            VerbConstitutionRecord as VCR,
        )
        from arabic_engine.core import (
            VerbDerivativeRecord as VDR,
        )
        from arabic_engine.core import (
            VerbEventRecord as VER,
        )
        from arabic_engine.core import (
            VerbInflection as VI,
        )
        from arabic_engine.core import (
            VerbMasdarRecord as VMR,
        )
        from arabic_engine.core import (
            VerbReadinessScore as VRS,
        )
        assert VCR is VerbConstitutionRecord
        assert VDR is VerbDerivativeRecord
        assert VER is VerbEventRecord
        assert VI is VerbInflection
        assert VMR is VerbMasdarRecord
        assert VRS is VerbReadinessScore
