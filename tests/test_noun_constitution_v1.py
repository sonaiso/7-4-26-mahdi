"""Tests for Noun Fractal Constitution v1.

Validates:
  * All 15 new enums are complete (correct member counts).
  * All 9 new dataclasses can be instantiated.
  * Classification functions produce correct outputs.
  * Readiness formula and validation logic.
  * Factory function (build_noun_fractal) end-to-end.
  * Batch builder.
  * Edge cases (unknown features, borrowed nouns, compound nouns).
  * Re-exports from arabic_engine.core.
"""

from __future__ import annotations

import pytest

from arabic_engine.core.enums import (
    POS,
    NominalAttributeKind,
    NounComposition,
    NounDefiniteness,
    NounDirection,
    NounExistentialAspect,
    NounFractalStage,
    NounGender,
    NounGenusLevel,
    NounNumber,
    NounOrigin,
    NounPatternType,
    NounReadiness,
    NounSignificationType,
    NounUniversality,
    ProperNounKind,
    SemanticType,
)
from arabic_engine.core.types import (
    Concept,
    LexicalClosure,
    NounAttributeRecord,
    NounClassificationRecord,
    NounCompositionRecord,
    NounFractalRecord,
    NounInflectionRecord,
    NounMinimumRecord,
    NounMorphologyRecord,
    NounSignificationRecord,
    NounValidationResult,
)
from arabic_engine.noun.constitution_v1 import (
    batch_build,
    build_noun_fractal,
    check_minimum,
    classify_genus_level,
    classify_nominal_attribute,
    classify_noun_direction,
    classify_proper_noun,
    classify_universality,
    compute_readiness,
    compute_signification,
    determine_composition,
    determine_inflection,
    determine_morphology,
    validate_noun_fractal,
)

# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════


def _closure(
    surface: str = "كتاب",
    lemma: str = "كتاب",
    pos: POS = POS.ISM,
    root: tuple = ("ك", "ت", "ب"),
    pattern: str = "فِعَال",
    **features,
) -> LexicalClosure:
    return LexicalClosure(
        surface=surface,
        lemma=lemma,
        root=root,
        pattern=pattern,
        pos=pos,
        features=features,
    )


def _concept(
    label: str = "كتاب",
    stype: SemanticType = SemanticType.ENTITY,
    **props,
) -> Concept:
    return Concept(
        concept_id=1,
        label=label,
        semantic_type=stype,
        properties=props,
    )


# ═══════════════════════════════════════════════════════════════════════
# Phase 6.1 — Enum completeness
# ═══════════════════════════════════════════════════════════════════════


class TestEnumCompleteness:
    def test_noun_direction_count(self):
        assert len(NounDirection) == 10

    def test_noun_direction_members(self):
        names = {m.name for m in NounDirection}
        assert "DHAT" in names
        assert "MARJI3" in names
        assert "KULLI" in names
        assert "FARD" in names
        assert "SIFA_ISMIYYA" in names
        assert "UNKNOWN" in names

    def test_noun_universality_count(self):
        assert len(NounUniversality) == 3

    def test_noun_genus_level_count(self):
        assert len(NounGenusLevel) == 4

    def test_proper_noun_kind_count(self):
        assert len(ProperNounKind) == 9

    def test_nominal_attribute_kind_count(self):
        assert len(NominalAttributeKind) == 9

    def test_noun_number_count(self):
        assert len(NounNumber) == 6

    def test_noun_gender_count(self):
        assert len(NounGender) == 6

    def test_noun_definiteness_count(self):
        assert len(NounDefiniteness) == 8

    def test_noun_composition_count(self):
        assert len(NounComposition) == 4

    def test_noun_origin_count(self):
        assert len(NounOrigin) == 4

    def test_noun_pattern_type_count(self):
        assert len(NounPatternType) == 4

    def test_noun_signification_type_count(self):
        assert len(NounSignificationType) == 3

    def test_noun_fractal_stage_count(self):
        assert len(NounFractalStage) == 6

    def test_noun_fractal_stage_members(self):
        names = {m.name for m in NounFractalStage}
        assert names == {"TA3YIN", "HIFZ", "RABT", "HUKM", "INTIQAL", "RADD"}

    def test_noun_readiness_count(self):
        assert len(NounReadiness) == 3

    def test_noun_existential_aspect_count(self):
        assert len(NounExistentialAspect) == 7


# ═══════════════════════════════════════════════════════════════════════
# Phase 6.2 — Dataclass instantiation
# ═══════════════════════════════════════════════════════════════════════


class TestDataclassInstantiation:
    def test_noun_minimum_record(self):
        rec = NounMinimumRecord(
            thubut=True, hadd=True, imtidad=True, muqawwim=True,
            alaqa_binaiyya=True, intizam=True, wahda=True,
            qabiliyyat_ta3yin=True,
        )
        assert rec.thubut is True
        assert rec.qabiliyyat_ta3yin is True

    def test_noun_morphology_record(self):
        rec = NounMorphologyRecord(
            material="كتاب", pattern_type=NounPatternType.WAZN_JAMID,
            pattern="فِعَال", root=("ك", "ت", "ب"),
        )
        assert rec.material == "كتاب"
        assert rec.root == ("ك", "ت", "ب")

    def test_noun_classification_record(self):
        rec = NounClassificationRecord(
            universality=NounUniversality.KULLI,
            genus_level=NounGenusLevel.NAW3,
            proper_noun_kind=None,
        )
        assert rec.universality is NounUniversality.KULLI
        assert rec.proper_noun_kind is None

    def test_noun_attribute_record(self):
        rec = NounAttributeRecord(
            attribute_kind=NominalAttributeKind.SIFA_MUSHABBAHA,
            is_nominal_attribute=True,
        )
        assert rec.is_nominal_attribute is True

    def test_noun_inflection_record(self):
        rec = NounInflectionRecord(
            number=NounNumber.MUFRAD,
            gender=NounGender.MUDHAKKAR,
            definiteness=NounDefiniteness.NAKIRA,
        )
        assert rec.number is NounNumber.MUFRAD

    def test_noun_composition_record(self):
        rec = NounCompositionRecord(
            composition=NounComposition.BASIT,
            origin=NounOrigin.ASIL,
        )
        assert rec.origin is NounOrigin.ASIL

    def test_noun_signification_record(self):
        rec = NounSignificationRecord(
            mutabaqa="كتاب",
            tadammun=("paper", "pages"),
            iltizam=("existence",),
        )
        assert rec.mutabaqa == "كتاب"

    def test_noun_fractal_record(self):
        rec = NounFractalRecord(
            noun_id="NF_001", lemma="كتاب", surface="الكتاب",
            direction=NounDirection.DHAT,
            conceptual_type=SemanticType.ENTITY,
            morphology=NounMorphologyRecord(
                material="كتاب", pattern_type=NounPatternType.WAZN_JAMID,
                pattern="فِعَال", root=("ك", "ت", "ب"),
            ),
            classification=NounClassificationRecord(
                universality=NounUniversality.KULLI,
                genus_level=NounGenusLevel.NAW3,
                proper_noun_kind=None,
            ),
            attribute=NounAttributeRecord(attribute_kind=None, is_nominal_attribute=False),
            inflection=NounInflectionRecord(
                number=NounNumber.MUFRAD,
                gender=NounGender.MUDHAKKAR,
                definiteness=NounDefiniteness.MA3RIFA_3AHD,
            ),
            composition=NounCompositionRecord(
                composition=NounComposition.BASIT, origin=NounOrigin.ASIL,
            ),
            signification=NounSignificationRecord(
                mutabaqa="كتاب", tadammun=(), iltizam=("existence",),
            ),
            minimum=NounMinimumRecord(
                thubut=True, hadd=True, imtidad=True, muqawwim=True,
                alaqa_binaiyya=True, intizam=True, wahda=True,
                qabiliyyat_ta3yin=True,
            ),
            fractal_stage=NounFractalStage.TA3YIN,
            readiness=NounReadiness.READY,
            readiness_score=1.0,
            existential_aspect=NounExistentialAspect.DHAT,
        )
        assert rec.noun_id == "NF_001"
        assert rec.readiness is NounReadiness.READY

    def test_noun_validation_result(self):
        rec = NounValidationResult(valid=True, errors=(), readiness_score=1.0)
        assert rec.valid is True
        assert rec.errors == ()

    def test_frozen_immutability(self):
        rec = NounMorphologyRecord(
            material="كتاب", pattern_type=NounPatternType.WAZN_JAMID,
            pattern="فِعَال", root=("ك", "ت", "ب"),
        )
        with pytest.raises(AttributeError):
            rec.material = "other"  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════
# Phase 6.3 — Classification function tests
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyNounDirection:
    def test_entity_gives_dhat(self):
        cl = _closure()
        co = _concept(stype=SemanticType.ENTITY)
        assert classify_noun_direction(cl, co) is NounDirection.DHAT

    def test_attribute_gives_sifa_ismiyya(self):
        cl = _closure()
        co = _concept(stype=SemanticType.ATTRIBUTE)
        assert classify_noun_direction(cl, co) is NounDirection.SIFA_ISMIYYA

    def test_relation_gives_mafhum_ismi(self):
        cl = _closure()
        co = _concept(stype=SemanticType.RELATION)
        assert classify_noun_direction(cl, co) is NounDirection.MAFHUM_ISMI

    def test_proper_noun_gives_fard(self):
        cl = _closure(proper="personal")
        co = _concept(stype=SemanticType.ENTITY)
        assert classify_noun_direction(cl, co) is NounDirection.FARD

    def test_sifa_pos_gives_sifa_ismiyya(self):
        cl = _closure(pos=POS.SIFA)
        co = _concept(stype=SemanticType.ENTITY)
        assert classify_noun_direction(cl, co) is NounDirection.SIFA_ISMIYYA

    def test_event_gives_marji3(self):
        cl = _closure()
        co = _concept(stype=SemanticType.EVENT)
        assert classify_noun_direction(cl, co) is NounDirection.MARJI3


class TestClassifyUniversality:
    def test_default_is_kulli(self):
        co = _concept()
        assert classify_universality(co) is NounUniversality.KULLI

    def test_particular_gives_juz2i(self):
        co = _concept(particular=True)
        assert classify_universality(co) is NounUniversality.JUZ2I


class TestClassifyGenusLevel:
    def test_fard_direction(self):
        co = _concept()
        assert classify_genus_level(co, NounDirection.FARD) is NounGenusLevel.FARD

    def test_genus_property(self):
        co = _concept(genus_level="genus")
        assert classify_genus_level(co, NounDirection.DHAT) is NounGenusLevel.JINS

    def test_species_property(self):
        co = _concept(genus_level="species")
        assert classify_genus_level(co, NounDirection.DHAT) is NounGenusLevel.NAW3

    def test_individual_property(self):
        co = _concept(genus_level="individual")
        assert classify_genus_level(co, NounDirection.DHAT) is NounGenusLevel.FARD

    def test_entity_default_naw3(self):
        co = _concept(stype=SemanticType.ENTITY)
        assert classify_genus_level(co, NounDirection.DHAT) is NounGenusLevel.NAW3

    def test_non_entity_unknown(self):
        co = _concept(stype=SemanticType.NORM)
        assert classify_genus_level(co, NounDirection.MAFHUM_ISMI) is NounGenusLevel.UNKNOWN


class TestClassifyProperNoun:
    def test_not_proper_returns_none(self):
        cl = _closure()
        assert classify_proper_noun(cl) is None

    def test_proper_personal(self):
        cl = _closure(proper="personal")
        assert classify_proper_noun(cl) is ProperNounKind.SHAKHSI

    def test_proper_place(self):
        cl = _closure(proper="place")
        assert classify_proper_noun(cl) is ProperNounKind.MAKAN

    def test_proper_time(self):
        cl = _closure(proper="time")
        assert classify_proper_noun(cl) is ProperNounKind.ZAMAN

    def test_proper_laqab(self):
        cl = _closure(proper="laqab")
        assert classify_proper_noun(cl) is ProperNounKind.LAQAB

    def test_proper_kunya(self):
        cl = _closure(proper="kunya")
        assert classify_proper_noun(cl) is ProperNounKind.KUNYA

    def test_proper_bool_true(self):
        cl = _closure(proper=True)
        assert classify_proper_noun(cl) is ProperNounKind.SHAKHSI

    def test_proper_unknown_string(self):
        cl = _closure(proper="exotic")
        assert classify_proper_noun(cl) is ProperNounKind.UNKNOWN


class TestClassifyNominalAttribute:
    def test_not_attribute(self):
        cl = _closure()
        rec = classify_nominal_attribute(cl)
        assert rec.is_nominal_attribute is False
        assert rec.attribute_kind is None

    def test_sifa_pos(self):
        cl = _closure(pos=POS.SIFA)
        rec = classify_nominal_attribute(cl)
        assert rec.is_nominal_attribute is True
        assert rec.attribute_kind is NominalAttributeKind.SIFA_MUSHABBAHA

    def test_explicit_attr_kind(self):
        cl = _closure(attr_kind="ism_fa3il")
        rec = classify_nominal_attribute(cl)
        assert rec.is_nominal_attribute is True
        assert rec.attribute_kind is NominalAttributeKind.ISM_FA3IL

    def test_explicit_nisba(self):
        cl = _closure(attr_kind="nisba")
        rec = classify_nominal_attribute(cl)
        assert rec.attribute_kind is NominalAttributeKind.NISBA


class TestDetermineInflection:
    def test_defaults_unknown(self):
        cl = _closure()
        rec = determine_inflection(cl)
        assert rec.number is NounNumber.UNKNOWN
        assert rec.gender is NounGender.UNKNOWN
        assert rec.definiteness is NounDefiniteness.UNKNOWN

    def test_singular_masculine_definite(self):
        cl = _closure(number="singular", gender="masculine", definiteness="definite")
        rec = determine_inflection(cl)
        assert rec.number is NounNumber.MUFRAD
        assert rec.gender is NounGender.MUDHAKKAR
        assert rec.definiteness is NounDefiniteness.MA3RIFA_3AHD

    def test_dual(self):
        cl = _closure(number="dual")
        rec = determine_inflection(cl)
        assert rec.number is NounNumber.MUTHANNA

    def test_plural(self):
        cl = _closure(number="plural")
        rec = determine_inflection(cl)
        assert rec.number is NounNumber.JAM3

    def test_feminine_haqiqi(self):
        cl = _closure(gender="feminine")
        rec = determine_inflection(cl)
        assert rec.gender is NounGender.MU2ANNATH_HAQIQI

    def test_indefinite(self):
        cl = _closure(definiteness="indefinite")
        rec = determine_inflection(cl)
        assert rec.definiteness is NounDefiniteness.NAKIRA

    def test_construct_state(self):
        cl = _closure(definiteness="construct")
        rec = determine_inflection(cl)
        assert rec.definiteness is NounDefiniteness.MA3RIFA_IDAFA

    def test_collective(self):
        cl = _closure(number="collective")
        rec = determine_inflection(cl)
        assert rec.number is NounNumber.ISM_JAM3


class TestDetermineComposition:
    def test_default_basit_asil(self):
        cl = _closure()
        rec = determine_composition(cl)
        assert rec.composition is NounComposition.BASIT
        assert rec.origin is NounOrigin.ASIL

    def test_compound_ismi(self):
        cl = _closure(compound="ismi")
        rec = determine_composition(cl)
        assert rec.composition is NounComposition.MURAKKAB_ISMI

    def test_compound_mazji(self):
        cl = _closure(compound="mazji")
        rec = determine_composition(cl)
        assert rec.composition is NounComposition.MURAKKAB_MAZJI

    def test_borrowed_settled(self):
        cl = _closure(borrowed="settled")
        rec = determine_composition(cl)
        assert rec.origin is NounOrigin.MUQTARAD_MUSTAQIRR

    def test_borrowed_unsettled(self):
        cl = _closure(borrowed="unsettled")
        rec = determine_composition(cl)
        assert rec.origin is NounOrigin.MUQTARAD_GHAYR_MUSTAQIRR

    def test_borrowed_true_bool(self):
        cl = _closure(borrowed=True)
        rec = determine_composition(cl)
        assert rec.origin is NounOrigin.MUQTARAD_MUSTAQIRR


class TestDetermineMorphology:
    def test_default_wazn_jamid(self):
        cl = _closure()
        rec = determine_morphology(cl)
        assert rec.pattern_type is NounPatternType.WAZN_JAMID
        assert rec.material == "كتاب"
        assert rec.root == ("ك", "ت", "ب")
        assert rec.pattern == "فِعَال"

    def test_derived(self):
        cl = _closure(derived="true")
        rec = determine_morphology(cl)
        assert rec.pattern_type is NounPatternType.WAZN_MUSHTAQQ

    def test_derived_bool(self):
        cl = _closure(derived=True)
        rec = determine_morphology(cl)
        assert rec.pattern_type is NounPatternType.WAZN_MUSHTAQQ

    def test_fixed_qalib(self):
        cl = _closure(derived="fixed")
        rec = determine_morphology(cl)
        assert rec.pattern_type is NounPatternType.QALIB_THABIT


# ═══════════════════════════════════════════════════════════════════════
# Phase 6.3b — Signification
# ═══════════════════════════════════════════════════════════════════════


class TestComputeSignification:
    def test_basic(self):
        co = _concept(label="كتاب")
        rec = compute_signification(co, NounDirection.DHAT)
        assert rec.mutabaqa == "كتاب"
        assert isinstance(rec.tadammun, tuple)
        assert "existence" in rec.iltizam

    def test_fard_iltizam(self):
        co = _concept(label="محمد")
        rec = compute_signification(co, NounDirection.FARD)
        assert "individuation" in rec.iltizam
        assert "existence" in rec.iltizam

    def test_sifa_iltizam(self):
        co = _concept(label="جميل", stype=SemanticType.ATTRIBUTE)
        rec = compute_signification(co, NounDirection.SIFA_ISMIYYA)
        assert "qualification" in rec.iltizam

    def test_props_in_tadammun(self):
        co = _concept(label="شجرة", stype=SemanticType.ENTITY, colour="green", height="tall")
        rec = compute_signification(co, NounDirection.DHAT)
        assert "colour" in rec.tadammun
        assert "height" in rec.tadammun


# ═══════════════════════════════════════════════════════════════════════
# Phase 6.4 — Readiness and validation
# ═══════════════════════════════════════════════════════════════════════


class TestCheckMinimum:
    def test_all_true(self):
        morph = NounMorphologyRecord("كتاب", NounPatternType.WAZN_JAMID, "فِعَال", ("ك", "ت", "ب"))
        classif = NounClassificationRecord(NounUniversality.KULLI, NounGenusLevel.NAW3, None)
        attr = NounAttributeRecord(None, False)
        infl = NounInflectionRecord(
            NounNumber.MUFRAD, NounGender.MUDHAKKAR, NounDefiniteness.NAKIRA,
        )
        comp = NounCompositionRecord(NounComposition.BASIT, NounOrigin.ASIL)
        signif = NounSignificationRecord("كتاب", (), ("existence",))
        rec = check_minimum(morph, classif, attr, infl, comp, signif)
        assert rec.thubut is True
        assert rec.hadd is True
        assert rec.imtidad is True
        assert rec.muqawwim is True
        assert rec.alaqa_binaiyya is True
        assert rec.intizam is True
        assert rec.wahda is True
        assert rec.qabiliyyat_ta3yin is True

    def test_empty_material(self):
        morph = NounMorphologyRecord("", NounPatternType.UNKNOWN, "", ())
        classif = NounClassificationRecord(NounUniversality.UNKNOWN, NounGenusLevel.UNKNOWN, None)
        attr = NounAttributeRecord(None, False)
        infl = NounInflectionRecord(
            NounNumber.UNKNOWN, NounGender.UNKNOWN, NounDefiniteness.UNKNOWN,
        )
        comp = NounCompositionRecord(NounComposition.UNKNOWN, NounOrigin.UNKNOWN)
        signif = NounSignificationRecord("", (), ())
        rec = check_minimum(morph, classif, attr, infl, comp, signif)
        assert rec.thubut is False
        assert rec.hadd is False
        assert rec.muqawwim is False


class TestComputeReadiness:
    def test_full_readiness(self):
        classif = NounClassificationRecord(NounUniversality.KULLI, NounGenusLevel.NAW3, None)
        score = compute_readiness(
            NounDirection.DHAT, SemanticType.ENTITY, classif,
            NounNumber.MUFRAD, NounGender.MUDHAKKAR,
            NounDefiniteness.NAKIRA, True,
        )
        assert score == 1.0

    def test_partial_readiness(self):
        classif = NounClassificationRecord(NounUniversality.UNKNOWN, NounGenusLevel.UNKNOWN, None)
        score = compute_readiness(
            NounDirection.DHAT, SemanticType.ENTITY, classif,
            NounNumber.UNKNOWN, NounGender.UNKNOWN,
            NounDefiniteness.UNKNOWN, False,
        )
        # Dir=1 + Type=1 + Ref=0 + Num=0 + Gen=0 + Def=0 + Recover=0 = 2/7
        assert score == pytest.approx(2 / 7, abs=0.001)

    def test_zero_readiness(self):
        classif = NounClassificationRecord(NounUniversality.UNKNOWN, NounGenusLevel.UNKNOWN, None)
        score = compute_readiness(
            NounDirection.UNKNOWN, SemanticType.ENTITY, classif,
            NounNumber.UNKNOWN, NounGender.UNKNOWN,
            NounDefiniteness.UNKNOWN, False,
        )
        # Dir=0 + Type=1 + Ref=0 + Num=0 + Gen=0 + Def=0 + Recover=0 = 1/7
        assert score == pytest.approx(1 / 7, abs=0.001)


class TestValidateNounFractal:
    def test_valid_fractal(self):
        cl = _closure(number="singular", gender="masculine", definiteness="indefinite")
        co = _concept()
        frac = build_noun_fractal(cl, co)
        result = validate_noun_fractal(frac)
        assert result.valid is True
        assert result.errors == ()
        assert result.readiness_score >= 0.7

    def test_invalid_fractal_unknown_everything(self):
        cl = _closure(surface="?", lemma="?", root=(), pattern="")
        co = _concept(label="?", stype=SemanticType.ENTITY)
        frac = build_noun_fractal(cl, co)
        result = validate_noun_fractal(frac)
        # Root is empty → root_empty error
        assert "root_empty" in result.errors

    def test_invalid_below_threshold(self):
        cl = _closure(surface="x", lemma="x")
        co = _concept(label="x")
        frac = build_noun_fractal(cl, co)
        result = validate_noun_fractal(frac)
        # No inflection features → readiness likely below threshold
        assert result.readiness_score < 1.0


# ═══════════════════════════════════════════════════════════════════════
# Phase 6.5 — Factory and integration tests
# ═══════════════════════════════════════════════════════════════════════


class TestBuildNounFractal:
    def test_kitab(self):
        """End-to-end: كتاب — common noun, entity, singular, masculine."""
        cl = _closure(
            surface="الكتاب", lemma="كتاب",
            number="singular", gender="masculine", definiteness="definite",
        )
        co = _concept(label="كتاب", stype=SemanticType.ENTITY)
        frac = build_noun_fractal(cl, co)

        assert frac.lemma == "كتاب"
        assert frac.surface == "الكتاب"
        assert frac.direction is NounDirection.DHAT
        assert frac.conceptual_type is SemanticType.ENTITY
        assert frac.inflection.number is NounNumber.MUFRAD
        assert frac.inflection.gender is NounGender.MUDHAKKAR
        assert frac.inflection.definiteness is NounDefiniteness.MA3RIFA_3AHD
        assert frac.classification.universality is NounUniversality.KULLI
        assert frac.composition.origin is NounOrigin.ASIL
        assert frac.morphology.root == ("ك", "ت", "ب")
        assert frac.readiness is NounReadiness.READY
        assert frac.readiness_score == 1.0
        assert frac.existential_aspect is NounExistentialAspect.DHAT
        assert frac.fractal_stage is NounFractalStage.TA3YIN

    def test_muhammad(self):
        """End-to-end: محمد — proper noun (علم شخصي)."""
        cl = _closure(
            surface="محمد", lemma="محمد",
            root=("ح", "م", "د"), pattern="مُفَعَّل",
            proper="personal",
            number="singular", gender="masculine", definiteness="proper",
        )
        co = _concept(label="محمد", stype=SemanticType.ENTITY, particular=True)
        frac = build_noun_fractal(cl, co)

        assert frac.direction is NounDirection.FARD
        assert frac.classification.universality is NounUniversality.JUZ2I
        assert frac.classification.genus_level is NounGenusLevel.FARD
        assert frac.classification.proper_noun_kind is ProperNounKind.SHAKHSI
        assert frac.inflection.definiteness is NounDefiniteness.MA3RIFA_3ALAM

    def test_madrasa(self):
        """End-to-end: مدرسة — feminine noun."""
        cl = _closure(
            surface="المدرسة", lemma="مدرسة",
            root=("د", "ر", "س"), pattern="مَفْعَلَة",
            number="singular", gender="feminine", definiteness="definite",
        )
        co = _concept(label="مدرسة", stype=SemanticType.ENTITY)
        frac = build_noun_fractal(cl, co)

        assert frac.inflection.gender is NounGender.MU2ANNATH_HAQIQI
        assert frac.readiness is NounReadiness.READY

    def test_asad(self):
        """End-to-end: أسد — common noun, animal genus."""
        cl = _closure(
            surface="أسد", lemma="أسد",
            root=("أ", "س", "د"), pattern="فَعَل",
            number="singular", gender="masculine", definiteness="indefinite",
        )
        co = _concept(
            label="أسد", stype=SemanticType.ENTITY, genus_level="genus",
        )
        frac = build_noun_fractal(cl, co)

        assert frac.classification.genus_level is NounGenusLevel.JINS
        assert frac.readiness is NounReadiness.READY

    def test_explicit_noun_id(self):
        cl = _closure()
        co = _concept()
        frac = build_noun_fractal(cl, co, noun_id="CUSTOM_001")
        assert frac.noun_id == "CUSTOM_001"

    def test_auto_id_increments(self):
        cl = _closure()
        co = _concept()
        f1 = build_noun_fractal(cl, co)
        f2 = build_noun_fractal(cl, co)
        assert f1.noun_id != f2.noun_id
        assert f1.noun_id.startswith("NF_")
        assert f2.noun_id.startswith("NF_")

    def test_signification_fields(self):
        cl = _closure()
        co = _concept(label="كتاب", stype=SemanticType.ENTITY)
        frac = build_noun_fractal(cl, co)
        assert frac.signification.mutabaqa == "كتاب"
        assert "existence" in frac.signification.iltizam


class TestBatchBuild:
    def test_basic_batch(self):
        closures = [
            _closure(surface="كتاب", pos=POS.ISM),
            _closure(surface="ذهب", pos=POS.FI3L),  # verb — should be skipped
            _closure(surface="رجل", pos=POS.ISM),
        ]
        concepts = [
            _concept(label="كتاب"),
            _concept(label="ذهب", stype=SemanticType.EVENT),
            _concept(label="رجل"),
        ]
        results = batch_build(closures, concepts)
        # Only ISM closures are processed
        assert len(results) == 2
        assert results[0].lemma == "كتاب"
        assert results[1].lemma == "كتاب"  # because default _closure lemma

    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError, match="same length"):
            batch_build([_closure()], [_concept(), _concept()])

    def test_empty_batch(self):
        assert batch_build([], []) == []


# ═══════════════════════════════════════════════════════════════════════
# Phase 6.6 — Edge cases
# ═══════════════════════════════════════════════════════════════════════


class TestEdgeCases:
    def test_all_unknown_not_ready(self):
        cl = _closure(surface="x", lemma="x", root=(), pattern="")
        co = _concept(label="x")
        frac = build_noun_fractal(cl, co)
        # With empty root and pattern, readiness should not be READY
        assert frac.readiness_score < 1.0

    def test_borrowed_noun(self):
        cl = _closure(borrowed="settled", compound="ismi")
        co = _concept()
        frac = build_noun_fractal(cl, co)
        assert frac.composition.origin is NounOrigin.MUQTARAD_MUSTAQIRR
        assert frac.composition.composition is NounComposition.MURAKKAB_ISMI

    def test_compound_mazji_noun(self):
        cl = _closure(compound="mazji")
        co = _concept()
        frac = build_noun_fractal(cl, co)
        assert frac.composition.composition is NounComposition.MURAKKAB_MAZJI

    def test_minimum_all_false_possible(self):
        """All minimum conditions can be False for a completely empty noun."""
        morph = NounMorphologyRecord("", NounPatternType.UNKNOWN, "", ())
        classif = NounClassificationRecord(NounUniversality.UNKNOWN, NounGenusLevel.UNKNOWN, None)
        attr = NounAttributeRecord(None, False)
        infl = NounInflectionRecord(
            NounNumber.UNKNOWN, NounGender.UNKNOWN, NounDefiniteness.UNKNOWN,
        )
        comp = NounCompositionRecord(NounComposition.UNKNOWN, NounOrigin.UNKNOWN)
        signif = NounSignificationRecord("", (), ())
        minimum = check_minimum(morph, classif, attr, infl, comp, signif)
        assert minimum.thubut is False
        assert minimum.hadd is False
        assert minimum.imtidad is False
        assert minimum.muqawwim is False
        assert minimum.alaqa_binaiyya is False
        assert minimum.intizam is False
        assert minimum.wahda is False
        assert minimum.qabiliyyat_ta3yin is False


# ═══════════════════════════════════════════════════════════════════════
# Re-exports
# ═══════════════════════════════════════════════════════════════════════


class TestReExports:
    def test_enums_from_core(self):
        """Noun enums must be importable from arabic_engine.core."""
        import arabic_engine.core as core

        assert hasattr(core, "NounDirection")
        assert hasattr(core, "NounUniversality")
        assert hasattr(core, "NounGenusLevel")
        assert hasattr(core, "ProperNounKind")
        assert hasattr(core, "NominalAttributeKind")
        assert hasattr(core, "NounNumber")
        assert hasattr(core, "NounGender")
        assert hasattr(core, "NounDefiniteness")
        assert hasattr(core, "NounComposition")
        assert hasattr(core, "NounOrigin")
        assert hasattr(core, "NounPatternType")
        assert hasattr(core, "NounSignificationType")
        assert hasattr(core, "NounFractalStage")
        assert hasattr(core, "NounReadiness")
        assert hasattr(core, "NounExistentialAspect")

    def test_types_from_core(self):
        """Noun types must be importable from arabic_engine.core."""
        import arabic_engine.core as core

        assert hasattr(core, "NounMinimumRecord")
        assert hasattr(core, "NounMorphologyRecord")
        assert hasattr(core, "NounClassificationRecord")
        assert hasattr(core, "NounAttributeRecord")
        assert hasattr(core, "NounInflectionRecord")
        assert hasattr(core, "NounCompositionRecord")
        assert hasattr(core, "NounSignificationRecord")
        assert hasattr(core, "NounFractalRecord")
        assert hasattr(core, "NounValidationResult")

    def test_functions_from_noun_package(self):
        """Public API must be importable from arabic_engine.noun."""
        import arabic_engine.noun as noun

        assert hasattr(noun, "build_noun_fractal")
        assert hasattr(noun, "validate_noun_fractal")
        assert hasattr(noun, "batch_build")
        assert hasattr(noun, "classify_noun_direction")
        assert hasattr(noun, "classify_universality")
        assert hasattr(noun, "classify_genus_level")
        assert hasattr(noun, "classify_proper_noun")
        assert hasattr(noun, "classify_nominal_attribute")
        assert hasattr(noun, "determine_inflection")
        assert hasattr(noun, "determine_composition")
        assert hasattr(noun, "determine_morphology")
        assert hasattr(noun, "compute_signification")
        assert hasattr(noun, "check_minimum")
        assert hasattr(noun, "compute_readiness")


# ═══════════════════════════════════════════════════════════════════════
# Pipeline integration
# ═══════════════════════════════════════════════════════════════════════


class TestPipelineIntegration:
    def test_pipeline_noun_fractals_default_empty(self):
        from arabic_engine.pipeline import run

        result = run("كتب المعلمُ الدرسَ")
        assert result.noun_fractals == []

    def test_pipeline_with_analyze_nouns(self):
        from arabic_engine.pipeline import run

        result = run("كتب المعلمُ الدرسَ", analyze_nouns=True)
        # There should be some noun fractals for ISM tokens
        assert isinstance(result.noun_fractals, list)
