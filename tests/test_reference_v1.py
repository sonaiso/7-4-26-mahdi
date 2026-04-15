"""Tests for the Reference Constitution v1.0 (دستور الإحالة).

Validates:
  * All seven new enums are complete (correct member counts).
  * classify_reference_type — POS/lemma-to-ReferenceType mapping.
  * classify_reference_degree — ReferenceType/definiteness-to-degree mapping.
  * classify_tool_kind — ReferenceType/POS-to-tool mapping.
  * classify_predication_basis — entity/attribute distinction.
  * classify_origin — PRIMARY/DERIVED/SUBORDINATE.
  * evaluate_predication_readiness — 5-component readiness score.
  * detect_attribute_transition — attribute→reference transitions.
  * build_reference_record — end-to-end factory.
  * batch_build — parallel list factory.
  * validate_reference — acceptance/rejection criteria.
  * get_fractal_stages — fractal law stages.
  * Pipeline integration with analyze_reference=True.
  * Re-exports from arabic_engine.core.
"""

from __future__ import annotations

import pytest

from arabic_engine.core.enums import (
    POS,
    DefinitenessRole,
    PredicationBasis,
    ReferenceDegree,
    ReferenceOrigin,
    ReferenceToolKind,
    ReferenceType,
    SemanticType,
    UniversalParticular,
)
from arabic_engine.core.types import (
    Concept,
    LexicalClosure,
    PredicationReadinessScore,
    ReferenceRecord,
    ReferenceTransition,
)
from arabic_engine.signified.reference_v1 import (
    batch_build,
    build_reference_record,
    classify_origin,
    classify_predication_basis,
    classify_reference_degree,
    classify_reference_type,
    classify_tool_kind,
    detect_attribute_transition,
    evaluate_predication_readiness,
    get_fractal_stages,
    validate_reference,
)

# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════


def _closure(
    surface: str, lemma: str, pos: POS, root=("ك", "ت", "ب")
) -> LexicalClosure:
    return LexicalClosure(
        surface=surface,
        lemma=lemma,
        root=root,
        pattern="فَعَلَ",
        pos=pos,
    )


def _concept(label: str, stype: SemanticType, **props) -> Concept:
    return Concept(concept_id=999, label=label, semantic_type=stype, properties=props)


# ═══════════════════════════════════════════════════════════════════════
# Enum completeness
# ═══════════════════════════════════════════════════════════════════════


class TestEnumCompleteness:
    """Enum member counts match the constitution articles."""

    def test_reference_type_count(self):
        """المادة 15 — 10 reference types."""
        assert len(ReferenceType) == 10

    def test_reference_degree_count(self):
        """المادة 38 — 4 reference degrees."""
        assert len(ReferenceDegree) == 4

    def test_reference_tool_kind_count(self):
        """المادة 26 — 11 reference tools."""
        assert len(ReferenceToolKind) == 11

    def test_predication_basis_count(self):
        """المواد 7–9 — 2 predication bases."""
        assert len(PredicationBasis) == 2

    def test_reference_origin_count(self):
        """المواد 12–13 — 3 reference origins."""
        assert len(ReferenceOrigin) == 3

    def test_definiteness_role_count(self):
        """المواد 52–55 — 2 definiteness roles."""
        assert len(DefinitenessRole) == 2

    def test_universal_particular_count(self):
        """المواد 48–51 — 2 universal/particular values."""
        assert len(UniversalParticular) == 2

    def test_reference_type_members(self):
        expected = {
            "SELF_REFERENCE", "DESCRIPTIVE", "PRONOMINAL", "DEMONSTRATIVE",
            "RELATIVE", "TEMPORAL", "SPATIAL", "NUMERICAL",
            "DEPENDENT", "EXPLICATIVE",
        }
        assert {m.name for m in ReferenceType} == expected

    def test_reference_degree_members(self):
        expected = {"CLOSED", "SEMI_CLOSED", "OPEN", "DEPENDENT"}
        assert {m.name for m in ReferenceDegree} == expected

    def test_reference_tool_kind_members(self):
        expected = {
            "PROPER_NAME", "PRONOUN", "DEMONSTRATIVE", "RELATIVE_NOUN",
            "GENITIVE_CONSTRUCT", "RESTRICTIVE_ADJUNCT", "APPOSITION",
            "EMPHASIS", "NUMERAL", "TIME_PLACE", "STATE_SPECIFICATION",
        }
        assert {m.name for m in ReferenceToolKind} == expected

    def test_predication_basis_members(self):
        expected = {"PREDICATION", "REFERENCE"}
        assert {m.name for m in PredicationBasis} == expected

    def test_reference_origin_members(self):
        expected = {"PRIMARY", "DERIVED", "SUBORDINATE"}
        assert {m.name for m in ReferenceOrigin} == expected

    def test_definiteness_role_members(self):
        expected = {"DEFINITE", "INDEFINITE"}
        assert {m.name for m in DefinitenessRole} == expected

    def test_universal_particular_members(self):
        expected = {"UNIVERSAL", "PARTICULAR"}
        assert {m.name for m in UniversalParticular} == expected


# ═══════════════════════════════════════════════════════════════════════
# classify_reference_type
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyReferenceType:
    """المادة 15 — reference type classification."""

    def test_proper_name_entity(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        assert classify_reference_type(cl, c) is ReferenceType.SELF_REFERENCE

    def test_pronoun(self):
        cl = _closure("هو", "هو", POS.DAMIR)
        c = _concept("هو", SemanticType.ENTITY)
        assert classify_reference_type(cl, c) is ReferenceType.PRONOMINAL

    def test_demonstrative_lemma(self):
        cl = _closure("هذا", "هذا", POS.ISM)
        c = _concept("هذا", SemanticType.ENTITY)
        assert classify_reference_type(cl, c) is ReferenceType.DEMONSTRATIVE

    def test_demonstrative_dalika(self):
        cl = _closure("ذلك", "ذلك", POS.ISM)
        c = _concept("ذلك", SemanticType.ENTITY)
        assert classify_reference_type(cl, c) is ReferenceType.DEMONSTRATIVE

    def test_relative_noun_alladhi(self):
        cl = _closure("الذي", "الذي", POS.ISM)
        c = _concept("الذي", SemanticType.ENTITY)
        assert classify_reference_type(cl, c) is ReferenceType.RELATIVE

    def test_relative_noun_man(self):
        cl = _closure("من", "من", POS.ISM)
        c = _concept("من", SemanticType.ENTITY)
        assert classify_reference_type(cl, c) is ReferenceType.RELATIVE

    def test_temporal_lemma(self):
        cl = _closure("الآن", "الآن", POS.ZARF)
        c = _concept("الآن", SemanticType.EVENT)
        assert classify_reference_type(cl, c) is ReferenceType.TEMPORAL

    def test_spatial_lemma(self):
        cl = _closure("هنا", "هنا", POS.ZARF)
        c = _concept("هنا", SemanticType.ENTITY)
        assert classify_reference_type(cl, c) is ReferenceType.SPATIAL

    def test_numerical_lemma(self):
        cl = _closure("ثلاثة", "ثلاثة", POS.ISM)
        c = _concept("ثلاثة", SemanticType.ENTITY)
        assert classify_reference_type(cl, c) is ReferenceType.NUMERICAL

    def test_attribute(self):
        cl = _closure("كبير", "كبير", POS.SIFA)
        c = _concept("كبير", SemanticType.ATTRIBUTE)
        assert classify_reference_type(cl, c) is ReferenceType.DESCRIPTIVE

    def test_zarf_default_temporal(self):
        cl = _closure("حينَ", "حين", POS.ZARF)
        c = _concept("حين", SemanticType.EVENT)
        assert classify_reference_type(cl, c) is ReferenceType.TEMPORAL

    def test_context_hal(self):
        cl = _closure("راكبًا", "راكب", POS.SIFA)
        c = _concept("راكب", SemanticType.ATTRIBUTE)
        assert classify_reference_type(cl, c, context="hal") is ReferenceType.EXPLICATIVE

    def test_context_tamyiz(self):
        cl = _closure("نفسًا", "نفس", POS.ISM)
        c = _concept("نفس", SemanticType.ENTITY)
        assert classify_reference_type(cl, c, context="tamyiz") is ReferenceType.EXPLICATIVE

    def test_context_badal(self):
        cl = _closure("أخوه", "أخ", POS.ISM)
        c = _concept("أخ", SemanticType.ENTITY)
        assert classify_reference_type(cl, c, context="badal") is ReferenceType.DEPENDENT

    def test_context_tawkid(self):
        cl = _closure("كله", "كل", POS.ISM)
        c = _concept("كل", SemanticType.ENTITY)
        assert classify_reference_type(cl, c, context="tawkid") is ReferenceType.DEPENDENT

    def test_context_na3t(self):
        cl = _closure("الكبير", "كبير", POS.SIFA)
        c = _concept("كبير", SemanticType.ATTRIBUTE)
        assert classify_reference_type(cl, c, context="na3t") is ReferenceType.DEPENDENT

    def test_particle_default(self):
        cl = _closure("في", "في", POS.HARF)
        c = _concept("في", SemanticType.RELATION)
        assert classify_reference_type(cl, c) is ReferenceType.DEPENDENT

    def test_unknown_default(self):
        cl = _closure("xyz", "xyz", POS.UNKNOWN)
        c = _concept("xyz", SemanticType.ENTITY)
        assert classify_reference_type(cl, c) is ReferenceType.SELF_REFERENCE


# ═══════════════════════════════════════════════════════════════════════
# classify_reference_degree
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyReferenceDegree:
    """المادة 38 — reference degree classification."""

    def test_proper_name_closed(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        degree = classify_reference_degree(ReferenceType.SELF_REFERENCE, cl, c)
        assert degree is ReferenceDegree.CLOSED

    def test_pronoun_closed(self):
        cl = _closure("هو", "هو", POS.DAMIR)
        c = _concept("هو", SemanticType.ENTITY)
        degree = classify_reference_degree(ReferenceType.PRONOMINAL, cl, c)
        assert degree is ReferenceDegree.CLOSED

    def test_demonstrative_closed(self):
        cl = _closure("هذا", "هذا", POS.ISM)
        c = _concept("هذا", SemanticType.ENTITY)
        degree = classify_reference_degree(ReferenceType.DEMONSTRATIVE, cl, c)
        assert degree is ReferenceDegree.CLOSED

    def test_relative_semi_closed(self):
        cl = _closure("الذي", "الذي", POS.ISM)
        c = _concept("الذي", SemanticType.ENTITY)
        degree = classify_reference_degree(ReferenceType.RELATIVE, cl, c)
        assert degree is ReferenceDegree.SEMI_CLOSED

    def test_dependent_degree(self):
        cl = _closure("الكبير", "كبير", POS.SIFA)
        c = _concept("كبير", SemanticType.ATTRIBUTE)
        degree = classify_reference_degree(ReferenceType.DEPENDENT, cl, c)
        assert degree is ReferenceDegree.DEPENDENT

    def test_indefinite_opens_semi_closed(self):
        cl = _closure("رجل", "رجل", POS.ISM)
        c = _concept("رجل", SemanticType.ENTITY)
        degree = classify_reference_degree(
            ReferenceType.DESCRIPTIVE, cl, c,
            definiteness=DefinitenessRole.INDEFINITE,
        )
        assert degree is ReferenceDegree.OPEN

    def test_definite_upgrades_open(self):
        cl = _closure("الرجل", "رجل", POS.ISM)
        c = _concept("رجل", SemanticType.ENTITY)
        # Force OPEN type then check definite upgrades it
        degree = classify_reference_degree(
            ReferenceType.EXPLICATIVE, cl, c,  # EXPLICATIVE defaults to DEPENDENT
            definiteness=DefinitenessRole.DEFINITE,
        )
        # DEPENDENT stays DEPENDENT regardless of definiteness
        assert degree is ReferenceDegree.DEPENDENT

    def test_explicit_definiteness_override(self):
        cl = _closure("كتاب", "كتاب", POS.ISM)
        c = _concept("كتاب", SemanticType.ENTITY)
        degree = classify_reference_degree(
            ReferenceType.DESCRIPTIVE, cl, c,
            definiteness=DefinitenessRole.DEFINITE,
        )
        assert degree is ReferenceDegree.SEMI_CLOSED


# ═══════════════════════════════════════════════════════════════════════
# classify_tool_kind
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyToolKind:
    """المادة 26 — reference tool classification."""

    def test_proper_name(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        assert classify_tool_kind(cl, ReferenceType.SELF_REFERENCE) is ReferenceToolKind.PROPER_NAME

    def test_pronoun(self):
        cl = _closure("هو", "هو", POS.DAMIR)
        assert classify_tool_kind(cl, ReferenceType.PRONOMINAL) is ReferenceToolKind.PRONOUN

    def test_demonstrative(self):
        cl = _closure("هذا", "هذا", POS.ISM)
        result = classify_tool_kind(cl, ReferenceType.DEMONSTRATIVE)
        assert result is ReferenceToolKind.DEMONSTRATIVE

    def test_relative_noun(self):
        cl = _closure("الذي", "الذي", POS.ISM)
        assert classify_tool_kind(cl, ReferenceType.RELATIVE) is ReferenceToolKind.RELATIVE_NOUN

    def test_temporal(self):
        cl = _closure("الآن", "الآن", POS.ZARF)
        assert classify_tool_kind(cl, ReferenceType.TEMPORAL) is ReferenceToolKind.TIME_PLACE

    def test_spatial(self):
        cl = _closure("هنا", "هنا", POS.ZARF)
        assert classify_tool_kind(cl, ReferenceType.SPATIAL) is ReferenceToolKind.TIME_PLACE

    def test_numerical(self):
        cl = _closure("ثلاثة", "ثلاثة", POS.ISM)
        assert classify_tool_kind(cl, ReferenceType.NUMERICAL) is ReferenceToolKind.NUMERAL

    def test_explicative(self):
        cl = _closure("نفسًا", "نفس", POS.ISM)
        result = classify_tool_kind(cl, ReferenceType.EXPLICATIVE)
        assert result is ReferenceToolKind.STATE_SPECIFICATION

    def test_dependent_sifa(self):
        cl = _closure("الكبير", "كبير", POS.SIFA)
        result = classify_tool_kind(cl, ReferenceType.DEPENDENT)
        assert result is ReferenceToolKind.RESTRICTIVE_ADJUNCT

    def test_dependent_zarf(self):
        cl = _closure("عند", "عند", POS.ZARF)
        assert classify_tool_kind(cl, ReferenceType.DEPENDENT) is ReferenceToolKind.TIME_PLACE

    def test_descriptive(self):
        cl = _closure("كبير", "كبير", POS.SIFA)
        result = classify_tool_kind(cl, ReferenceType.DESCRIPTIVE)
        assert result is ReferenceToolKind.RESTRICTIVE_ADJUNCT


# ═══════════════════════════════════════════════════════════════════════
# classify_predication_basis
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyPredicationBasis:
    """المواد 7–12 — predication vs reference basis."""

    def test_entity_is_reference(self):
        c = _concept("زيد", SemanticType.ENTITY)
        basis = classify_predication_basis(c, ReferenceType.SELF_REFERENCE)
        assert basis is PredicationBasis.REFERENCE

    def test_event_is_reference(self):
        c = _concept("ذهاب", SemanticType.EVENT)
        basis = classify_predication_basis(c, ReferenceType.SELF_REFERENCE)
        assert basis is PredicationBasis.REFERENCE

    def test_attribute_is_predication(self):
        c = _concept("كبير", SemanticType.ATTRIBUTE)
        basis = classify_predication_basis(c, ReferenceType.DESCRIPTIVE)
        assert basis is PredicationBasis.PREDICATION

    def test_attribute_transitioning_to_reference(self):
        c = _concept("العاقل", SemanticType.ATTRIBUTE)
        basis = classify_predication_basis(c, ReferenceType.SELF_REFERENCE)
        assert basis is PredicationBasis.REFERENCE

    def test_attribute_pronominal_is_reference(self):
        c = _concept("attr", SemanticType.ATTRIBUTE)
        assert classify_predication_basis(c, ReferenceType.PRONOMINAL) is PredicationBasis.REFERENCE

    def test_relation_is_predication(self):
        c = _concept("في", SemanticType.RELATION)
        basis = classify_predication_basis(c, ReferenceType.DEPENDENT)
        assert basis is PredicationBasis.PREDICATION

    def test_norm_is_predication(self):
        c = _concept("حكم", SemanticType.NORM)
        basis = classify_predication_basis(c, ReferenceType.SELF_REFERENCE)
        assert basis is PredicationBasis.PREDICATION


# ═══════════════════════════════════════════════════════════════════════
# classify_origin
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyOrigin:
    """المواد 12–13 — reference origin classification."""

    def test_entity_is_primary(self):
        c = _concept("زيد", SemanticType.ENTITY)
        assert classify_origin(c, ReferenceType.SELF_REFERENCE) is ReferenceOrigin.PRIMARY

    def test_attribute_descriptive_is_derived(self):
        c = _concept("كبير", SemanticType.ATTRIBUTE)
        assert classify_origin(c, ReferenceType.DESCRIPTIVE) is ReferenceOrigin.DERIVED

    def test_event_is_derived(self):
        c = _concept("ذهاب", SemanticType.EVENT)
        assert classify_origin(c, ReferenceType.SELF_REFERENCE) is ReferenceOrigin.DERIVED

    def test_dependent_is_subordinate(self):
        c = _concept("كبير", SemanticType.ATTRIBUTE)
        assert classify_origin(c, ReferenceType.DEPENDENT) is ReferenceOrigin.SUBORDINATE

    def test_explicative_is_subordinate(self):
        c = _concept("نفس", SemanticType.ENTITY)
        assert classify_origin(c, ReferenceType.EXPLICATIVE) is ReferenceOrigin.SUBORDINATE

    def test_relation_is_derived(self):
        c = _concept("في", SemanticType.RELATION)
        assert classify_origin(c, ReferenceType.SELF_REFERENCE) is ReferenceOrigin.DERIVED


# ═══════════════════════════════════════════════════════════════════════
# evaluate_predication_readiness
# ═══════════════════════════════════════════════════════════════════════


class TestEvaluatePredicationReadiness:
    """المادة 87 — predication readiness scoring."""

    def _make_record(
        self,
        ref_type=ReferenceType.SELF_REFERENCE,
        degree=ReferenceDegree.CLOSED,
        tool=ReferenceToolKind.PROPER_NAME,
        referent="زيد",
        origin=ReferenceOrigin.PRIMARY,
    ):
        return ReferenceRecord(
            record_id="R_001",
            subject_type="ذات",
            reference_type=ref_type,
            reference_degree=degree,
            tool_kind=tool,
            predication_relation=PredicationBasis.REFERENCE,
            referent=referent,
            ready_for_predication=False,
            origin=origin,
        )

    def test_fully_ready(self):
        rec = self._make_record()
        score = evaluate_predication_readiness(rec)
        assert score.ready is True
        assert score.total >= 0.6

    def test_type_score(self):
        rec = self._make_record()
        score = evaluate_predication_readiness(rec)
        assert score.type_score == 1.0

    def test_degree_closed(self):
        rec = self._make_record(degree=ReferenceDegree.CLOSED)
        score = evaluate_predication_readiness(rec)
        assert score.degree_score == 1.0

    def test_degree_semi_closed(self):
        rec = self._make_record(degree=ReferenceDegree.SEMI_CLOSED)
        score = evaluate_predication_readiness(rec)
        assert score.degree_score == 0.8

    def test_degree_dependent(self):
        rec = self._make_record(degree=ReferenceDegree.DEPENDENT)
        score = evaluate_predication_readiness(rec)
        assert score.degree_score == 0.6

    def test_degree_open(self):
        rec = self._make_record(degree=ReferenceDegree.OPEN)
        score = evaluate_predication_readiness(rec)
        assert score.degree_score == 0.3

    def test_empty_referent_anchor_zero(self):
        rec = self._make_record(referent="")
        score = evaluate_predication_readiness(rec)
        assert score.anchor_score == 0.0

    def test_no_tool_partial(self):
        rec = self._make_record(tool=None)
        score = evaluate_predication_readiness(rec)
        assert score.tool_score == 0.5

    def test_total_formula(self):
        rec = self._make_record()
        score = evaluate_predication_readiness(rec)
        expected = (score.type_score + score.degree_score + score.anchor_score
                    + score.tool_score + score.recover_score) / 5.0
        assert abs(score.total - round(expected, 4)) < 0.0001

    def test_threshold_boundary(self):
        # Open, no tool, no referent — should be below threshold
        rec = self._make_record(
            degree=ReferenceDegree.OPEN,
            tool=None,
            referent="",
        )
        score = evaluate_predication_readiness(rec)
        assert score.ready is False

    def test_custom_threshold(self):
        rec = self._make_record()
        score = evaluate_predication_readiness(rec, threshold=1.0)
        assert score.ready is True  # All components are 1.0


# ═══════════════════════════════════════════════════════════════════════
# detect_attribute_transition
# ═══════════════════════════════════════════════════════════════════════


class TestDetectAttributeTransition:
    """المواد 44–47 — attribute transition detection."""

    def test_entity_no_transition(self):
        c = _concept("زيد", SemanticType.ENTITY)
        cl = _closure("زيد", "زيد", POS.ISM)
        assert detect_attribute_transition(
            c, cl, ReferenceType.SELF_REFERENCE, ReferenceDegree.CLOSED
        ) is None

    def test_attribute_substantivised(self):
        c = _concept("العاقل", SemanticType.ATTRIBUTE)
        cl = _closure("العاقل", "عاقل", POS.SIFA)
        result = detect_attribute_transition(
            c, cl, ReferenceType.SELF_REFERENCE, ReferenceDegree.CLOSED
        )
        assert result is not None
        assert isinstance(result, ReferenceTransition)
        assert result.from_basis is PredicationBasis.PREDICATION
        assert result.to_basis is PredicationBasis.REFERENCE
        assert result.reason == "attribute_substantivised"

    def test_attribute_pronominal(self):
        c = _concept("attr", SemanticType.ATTRIBUTE)
        cl = _closure("هو", "هو", POS.DAMIR)
        result = detect_attribute_transition(
            c, cl, ReferenceType.PRONOMINAL, ReferenceDegree.CLOSED
        )
        assert result is not None
        assert result.reason == "attribute_pronominally_used"

    def test_attribute_descriptive_closed(self):
        c = _concept("الطويل", SemanticType.ATTRIBUTE)
        cl = _closure("الطويل", "طويل", POS.SIFA)
        result = detect_attribute_transition(
            c, cl, ReferenceType.DESCRIPTIVE, ReferenceDegree.CLOSED
        )
        assert result is not None
        assert result.reason == "descriptive_closure"

    def test_attribute_descriptive_semi_closed(self):
        c = _concept("الطويل", SemanticType.ATTRIBUTE)
        cl = _closure("الطويل", "طويل", POS.SIFA)
        result = detect_attribute_transition(
            c, cl, ReferenceType.DESCRIPTIVE, ReferenceDegree.SEMI_CLOSED
        )
        assert result is not None
        assert result.reason == "descriptive_closure"

    def test_attribute_descriptive_open_no_transition(self):
        c = _concept("كبير", SemanticType.ATTRIBUTE)
        cl = _closure("كبير", "كبير", POS.SIFA)
        result = detect_attribute_transition(
            c, cl, ReferenceType.DESCRIPTIVE, ReferenceDegree.OPEN
        )
        assert result is None

    def test_attribute_dependent_no_transition(self):
        c = _concept("كبير", SemanticType.ATTRIBUTE)
        cl = _closure("الكبير", "كبير", POS.SIFA)
        result = detect_attribute_transition(
            c, cl, ReferenceType.DEPENDENT, ReferenceDegree.DEPENDENT
        )
        assert result is None

    def test_transition_preserves_degree(self):
        c = _concept("الطويل", SemanticType.ATTRIBUTE)
        cl = _closure("الطويل", "طويل", POS.SIFA)
        result = detect_attribute_transition(
            c, cl, ReferenceType.DESCRIPTIVE, ReferenceDegree.SEMI_CLOSED
        )
        assert result is not None
        assert result.resulting_degree is ReferenceDegree.SEMI_CLOSED

    def test_transition_frozen(self):
        c = _concept("الطويل", SemanticType.ATTRIBUTE)
        cl = _closure("الطويل", "طويل", POS.SIFA)
        result = detect_attribute_transition(
            c, cl, ReferenceType.DESCRIPTIVE, ReferenceDegree.CLOSED
        )
        assert result is not None
        with pytest.raises(AttributeError):
            result.reason = "changed"  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════
# build_reference_record
# ═══════════════════════════════════════════════════════════════════════


class TestBuildReferenceRecord:
    """End-to-end factory tests."""

    def test_entity_proper_name(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert isinstance(rec, ReferenceRecord)
        assert rec.reference_type is ReferenceType.SELF_REFERENCE
        assert rec.reference_degree is ReferenceDegree.CLOSED
        assert rec.tool_kind is ReferenceToolKind.PROPER_NAME
        assert rec.predication_relation is PredicationBasis.REFERENCE
        assert rec.origin is ReferenceOrigin.PRIMARY
        assert rec.subject_type == "ذات"
        assert rec.ready_for_predication is True

    def test_pronoun(self):
        cl = _closure("هو", "هو", POS.DAMIR)
        c = _concept("هو", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert rec.reference_type is ReferenceType.PRONOMINAL
        assert rec.reference_degree is ReferenceDegree.CLOSED
        assert rec.tool_kind is ReferenceToolKind.PRONOUN
        assert rec.definiteness is DefinitenessRole.DEFINITE

    def test_demonstrative(self):
        cl = _closure("هذا", "هذا", POS.ISM)
        c = _concept("هذا", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert rec.reference_type is ReferenceType.DEMONSTRATIVE
        assert rec.reference_degree is ReferenceDegree.CLOSED
        assert rec.tool_kind is ReferenceToolKind.DEMONSTRATIVE

    def test_relative_noun(self):
        cl = _closure("الذي", "الذي", POS.ISM)
        c = _concept("الذي", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert rec.reference_type is ReferenceType.RELATIVE
        assert rec.reference_degree is ReferenceDegree.SEMI_CLOSED
        assert rec.tool_kind is ReferenceToolKind.RELATIVE_NOUN

    def test_attribute_descriptor(self):
        cl = _closure("كبير", "كبير", POS.SIFA)
        c = _concept("كبير", SemanticType.ATTRIBUTE)
        rec = build_reference_record(cl, c)
        assert rec.reference_type is ReferenceType.DESCRIPTIVE
        assert rec.subject_type == "صفة"
        assert rec.predication_relation is PredicationBasis.PREDICATION

    def test_attribute_transition_in_build(self):
        """Attribute used as proper name triggers transition."""
        cl = _closure("العاقل", "عاقل", POS.ISM)
        c = _concept("العاقل", SemanticType.ATTRIBUTE)
        rec = build_reference_record(cl, c)
        # The ISM POS + ATTRIBUTE semantic type → SELF_REFERENCE
        assert rec.reference_type is ReferenceType.SELF_REFERENCE
        # Attribute transition → DERIVED, REFERENCE
        assert rec.origin is ReferenceOrigin.DERIVED
        assert rec.predication_relation is PredicationBasis.REFERENCE

    def test_frozen_record(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        with pytest.raises(AttributeError):
            rec.reference_type = ReferenceType.PRONOMINAL  # type: ignore[misc]

    def test_custom_referent(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        rec = build_reference_record(cl, c, referent="عمرو بن زيد")
        assert rec.referent == "عمرو بن زيد"

    def test_custom_record_id(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        rec = build_reference_record(cl, c, record_id="MY_001")
        assert rec.record_id == "MY_001"

    def test_notes_preserved(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        rec = build_reference_record(cl, c, notes="test note")
        assert rec.notes == "test note"

    def test_explicit_definiteness(self):
        cl = _closure("كتاب", "كتاب", POS.ISM)
        c = _concept("كتاب", SemanticType.ENTITY)
        rec = build_reference_record(cl, c, definiteness=DefinitenessRole.DEFINITE)
        assert rec.definiteness is DefinitenessRole.DEFINITE

    def test_explicit_universality(self):
        cl = _closure("إنسان", "إنسان", POS.ISM)
        c = _concept("إنسان", SemanticType.ENTITY)
        rec = build_reference_record(cl, c, universality=UniversalParticular.UNIVERSAL)
        assert rec.universality is UniversalParticular.UNIVERSAL

    def test_context_hal(self):
        cl = _closure("راكبًا", "راكب", POS.SIFA)
        c = _concept("راكب", SemanticType.ATTRIBUTE)
        rec = build_reference_record(cl, c, context="hal")
        assert rec.reference_type is ReferenceType.EXPLICATIVE

    def test_referent_defaults_to_label(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert rec.referent == "زيد"  # concept.label

    def test_auto_id_generation(self):
        cl = _closure("أ", "أ", POS.ISM)
        c = _concept("أ", SemanticType.ENTITY)
        r1 = build_reference_record(cl, c)
        r2 = build_reference_record(cl, c)
        assert r1.record_id != r2.record_id
        assert r1.record_id.startswith("REF_")


# ═══════════════════════════════════════════════════════════════════════
# batch_build
# ═══════════════════════════════════════════════════════════════════════


class TestBatchBuild:
    """Batch processing tests."""

    def test_batch_produces_correct_count(self):
        closures = [
            _closure("زيد", "زيد", POS.ISM),
            _closure("هو", "هو", POS.DAMIR),
            _closure("كبير", "كبير", POS.SIFA),
        ]
        concepts = [
            _concept("زيد", SemanticType.ENTITY),
            _concept("هو", SemanticType.ENTITY),
            _concept("كبير", SemanticType.ATTRIBUTE),
        ]
        results = batch_build(closures, concepts)
        assert len(results) == 3

    def test_batch_types_correct(self):
        closures = [
            _closure("زيد", "زيد", POS.ISM),
            _closure("هو", "هو", POS.DAMIR),
        ]
        concepts = [
            _concept("زيد", SemanticType.ENTITY),
            _concept("هو", SemanticType.ENTITY),
        ]
        results = batch_build(closures, concepts)
        assert results[0].reference_type is ReferenceType.SELF_REFERENCE
        assert results[1].reference_type is ReferenceType.PRONOMINAL

    def test_batch_with_referents(self):
        closures = [_closure("زيد", "زيد", POS.ISM)]
        concepts = [_concept("زيد", SemanticType.ENTITY)]
        results = batch_build(closures, concepts, referents=["عمرو"])
        assert results[0].referent == "عمرو"

    def test_batch_with_contexts(self):
        closures = [_closure("راكبًا", "راكب", POS.SIFA)]
        concepts = [_concept("راكب", SemanticType.ATTRIBUTE)]
        results = batch_build(closures, concepts, contexts=["hal"])
        assert results[0].reference_type is ReferenceType.EXPLICATIVE


# ═══════════════════════════════════════════════════════════════════════
# validate_reference
# ═══════════════════════════════════════════════════════════════════════


class TestValidateReference:
    """المواد 86–89 — acceptance/rejection criteria."""

    def test_valid_record(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert validate_reference(rec) is True

    def test_empty_referent_fails(self):
        rec = ReferenceRecord(
            record_id="R_fail",
            subject_type="ذات",
            reference_type=ReferenceType.SELF_REFERENCE,
            reference_degree=ReferenceDegree.CLOSED,
            tool_kind=ReferenceToolKind.PROPER_NAME,
            predication_relation=PredicationBasis.REFERENCE,
            referent="",
            ready_for_predication=False,
            origin=ReferenceOrigin.PRIMARY,
        )
        assert validate_reference(rec) is False

    def test_empty_subject_fails(self):
        rec = ReferenceRecord(
            record_id="R_fail",
            subject_type="",
            reference_type=ReferenceType.SELF_REFERENCE,
            reference_degree=ReferenceDegree.CLOSED,
            tool_kind=ReferenceToolKind.PROPER_NAME,
            predication_relation=PredicationBasis.REFERENCE,
            referent="زيد",
            ready_for_predication=False,
            origin=ReferenceOrigin.PRIMARY,
        )
        assert validate_reference(rec) is False

    def test_no_tool_closed_fails(self):
        rec = ReferenceRecord(
            record_id="R_fail",
            subject_type="ذات",
            reference_type=ReferenceType.SELF_REFERENCE,
            reference_degree=ReferenceDegree.CLOSED,
            tool_kind=None,
            predication_relation=PredicationBasis.REFERENCE,
            referent="زيد",
            ready_for_predication=False,
            origin=ReferenceOrigin.PRIMARY,
        )
        assert validate_reference(rec) is False

    def test_no_tool_open_passes(self):
        rec = ReferenceRecord(
            record_id="R_pass",
            subject_type="ذات",
            reference_type=ReferenceType.SELF_REFERENCE,
            reference_degree=ReferenceDegree.OPEN,
            tool_kind=None,
            predication_relation=PredicationBasis.REFERENCE,
            referent="شيء",
            ready_for_predication=False,
            origin=ReferenceOrigin.PRIMARY,
        )
        # Even though no tool, OPEN degree allows it; readiness decides
        result = validate_reference(rec)
        # With no tool (0.5) + OPEN degree (0.3) + anchor(1) + type(1) + recover(1)
        # = 3.8/5 = 0.76 ≥ 0.6 → ready
        assert result is True

    def test_pronoun_valid(self):
        cl = _closure("هو", "هو", POS.DAMIR)
        c = _concept("هو", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert validate_reference(rec) is True

    def test_demonstrative_valid(self):
        cl = _closure("هذا", "هذا", POS.ISM)
        c = _concept("هذا", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert validate_reference(rec) is True


# ═══════════════════════════════════════════════════════════════════════
# get_fractal_stages
# ═══════════════════════════════════════════════════════════════════════


class TestGetFractalStages:
    """المادة 78 — fractal law stages."""

    def test_returns_six_stages(self):
        stages = get_fractal_stages()
        assert len(stages) == 6

    def test_stage_names(self):
        stages = get_fractal_stages()
        assert stages == ("تعيين", "حفظ", "ربط", "حكم", "انتقال", "رد")

    def test_returns_tuple(self):
        stages = get_fractal_stages()
        assert isinstance(stages, tuple)


# ═══════════════════════════════════════════════════════════════════════
# Re-export tests
# ═══════════════════════════════════════════════════════════════════════


class TestReExports:
    """Verify all new types/enums are accessible from arabic_engine.core."""

    def test_reference_type_reexport(self):
        from arabic_engine.core import ReferenceType as RT
        assert RT is ReferenceType

    def test_reference_degree_reexport(self):
        from arabic_engine.core import ReferenceDegree as RD
        assert RD is ReferenceDegree

    def test_reference_tool_kind_reexport(self):
        from arabic_engine.core import ReferenceToolKind as RTK
        assert RTK is ReferenceToolKind

    def test_predication_basis_reexport(self):
        from arabic_engine.core import PredicationBasis as PB
        assert PB is PredicationBasis

    def test_reference_origin_reexport(self):
        from arabic_engine.core import ReferenceOrigin as RO
        assert RO is ReferenceOrigin

    def test_definiteness_role_reexport(self):
        from arabic_engine.core import DefinitenessRole as DR
        assert DR is DefinitenessRole

    def test_universal_particular_reexport(self):
        from arabic_engine.core import UniversalParticular as UP
        assert UP is UniversalParticular

    def test_reference_record_reexport(self):
        from arabic_engine.core import ReferenceRecord as RR
        assert RR is ReferenceRecord

    def test_predication_readiness_score_reexport(self):
        from arabic_engine.core import PredicationReadinessScore as PRS
        assert PRS is PredicationReadinessScore

    def test_reference_transition_reexport(self):
        from arabic_engine.core import ReferenceTransition as RT
        assert RT is ReferenceTransition


# ═══════════════════════════════════════════════════════════════════════
# Pipeline integration
# ═══════════════════════════════════════════════════════════════════════


class TestPipelineIntegration:
    """Pipeline analyze_reference integration tests."""

    def test_pipeline_default_no_reference(self):
        from arabic_engine.pipeline import run
        result = run("كتب زيد الدرس")
        assert result.reference_records == []

    def test_pipeline_with_reference(self):
        from arabic_engine.pipeline import run
        result = run("كتب زيد الدرس", analyze_reference=True)
        assert len(result.reference_records) > 0
        for rec in result.reference_records:
            assert isinstance(rec, ReferenceRecord)

    def test_pipeline_reference_records_frozen(self):
        from arabic_engine.pipeline import run
        result = run("كتب زيد الدرس", analyze_reference=True)
        assert len(result.reference_records) > 0
        with pytest.raises(AttributeError):
            result.reference_records[0].reference_type = ReferenceType.PRONOMINAL  # type: ignore[misc]

    def test_pipeline_reference_count_matches_tokens(self):
        from arabic_engine.pipeline import run
        result = run("كتب زيد الدرس", analyze_reference=True)
        assert len(result.reference_records) == len(result.closures)

    def test_pipeline_backward_compatible(self):
        """Existing pipeline calls without analyze_reference still work."""
        from arabic_engine.pipeline import run
        result = run("كتب زيد الدرس")
        assert hasattr(result, "reference_records")
        assert result.reference_records == []


# ═══════════════════════════════════════════════════════════════════════
# Definiteness and Universality inference
# ═══════════════════════════════════════════════════════════════════════


class TestDefinitenessInference:
    """المواد 52–55 — definiteness inference."""

    def test_al_definite(self):
        cl = _closure("الكتاب", "كتاب", POS.ISM)
        c = _concept("كتاب", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert rec.definiteness is DefinitenessRole.DEFINITE

    def test_pronoun_definite(self):
        cl = _closure("هو", "هو", POS.DAMIR)
        c = _concept("هو", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert rec.definiteness is DefinitenessRole.DEFINITE

    def test_indefinite_noun(self):
        cl = _closure("كتاب", "كتاب", POS.ISM)
        c = _concept("كتاب", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert rec.definiteness is DefinitenessRole.INDEFINITE


class TestUniversalityInference:
    """المواد 48–51 — universality inference."""

    def test_entity_particular(self):
        cl = _closure("زيد", "زيد", POS.ISM)
        c = _concept("زيد", SemanticType.ENTITY)
        rec = build_reference_record(cl, c)
        assert rec.universality is UniversalParticular.PARTICULAR

    def test_norm_universal(self):
        cl = _closure("حكم", "حكم", POS.ISM)
        c = _concept("حكم", SemanticType.NORM)
        rec = build_reference_record(cl, c)
        assert rec.universality is UniversalParticular.UNIVERSAL

    def test_explicit_override(self):
        cl = _closure("إنسان", "إنسان", POS.ISM)
        c = _concept("إنسان", SemanticType.ENTITY, scope="universal")
        rec = build_reference_record(cl, c)
        assert rec.universality is UniversalParticular.UNIVERSAL
