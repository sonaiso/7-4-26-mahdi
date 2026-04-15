"""Tests for the Single Concept Constitution v1.0 model.

Validates:
  * All seven new enums are complete (correct member counts).
  * classify_concept_type — SemanticType → SingleConceptType mapping.
  * classify_candidate_role — concept type + POS → CandidateRole.
  * check_isomorphism — five isomorphism axes.
  * analyze_dalala — three-level signification record.
  * Gate checkers — all 8 gates (PASSED / BLOCKED / INSUFFICIENT_DATA).
  * compute_readiness — readiness score calculation.
  * build_single_concept — end-to-end for the four canonical concept types.
  * acceptance_summary — eight acceptance criteria.
  * build_single_concept_batch — parallel list factory.
  * Re-exports from arabic_engine.core.
"""

from __future__ import annotations

import pytest

from arabic_engine.core.enums import (
    POS,
    CandidateRole,
    ConceptClosureStatus,
    ConceptEntityAttribute,
    ConceptGateID,
    ConceptIndependence,
    ConceptUniversalParticular,
    DalalaType,
    SemanticType,
    SingleConceptType,
    TransitionGateStatus,
)
from arabic_engine.core.types import (
    Concept,
    LexicalClosure,
    SingleConceptDalala,
    SingleConceptGateResult,
    SingleConceptIsomorphism,
)
from arabic_engine.signified.single_concept_v1 import (
    acceptance_summary,
    analyze_dalala,
    build_single_concept,
    build_single_concept_batch,
    check_isomorphism,
    classify_candidate_role,
    classify_concept_type,
    compute_readiness,
)

# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════


def _closure(
    surface: str = "كِتَاب",
    lemma: str = "كتاب",
    pos: POS = POS.ISM,
    root: tuple = ("ك", "ت", "ب"),
) -> LexicalClosure:
    return LexicalClosure(
        surface=surface,
        lemma=lemma,
        root=root,
        pattern="فَعَلَ",
        pos=pos,
    )


def _concept(
    label: str = "كتاب",
    stype: SemanticType = SemanticType.ENTITY,
    **props: object,
) -> Concept:
    return Concept(
        concept_id=999,
        label=label,
        semantic_type=stype,
        properties=dict(props),
    )


# ═══════════════════════════════════════════════════════════════════════
# Enum completeness
# ═══════════════════════════════════════════════════════════════════════


class TestEnumCompleteness:
    """Verify all new enums have the expected member count."""

    def test_single_concept_type_count(self):
        assert len(SingleConceptType) == 4

    def test_concept_universal_particular_count(self):
        assert len(ConceptUniversalParticular) == 2

    def test_concept_entity_attribute_count(self):
        assert len(ConceptEntityAttribute) == 2

    def test_concept_closure_status_count(self):
        assert len(ConceptClosureStatus) == 4

    def test_concept_independence_count(self):
        assert len(ConceptIndependence) == 3

    def test_candidate_role_count(self):
        assert len(CandidateRole) == 6

    def test_concept_gate_id_count(self):
        assert len(ConceptGateID) == 8


# ═══════════════════════════════════════════════════════════════════════
# classify_concept_type
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyConceptType:
    """Test SemanticType → SingleConceptType mapping."""

    def test_entity_to_existential(self):
        c = _concept(stype=SemanticType.ENTITY)
        assert classify_concept_type(c) is SingleConceptType.EXISTENTIAL

    def test_event_to_eventive(self):
        c = _concept(stype=SemanticType.EVENT)
        assert classify_concept_type(c) is SingleConceptType.EVENTIVE

    def test_attribute_to_descriptive(self):
        c = _concept(stype=SemanticType.ATTRIBUTE)
        assert classify_concept_type(c) is SingleConceptType.DESCRIPTIVE

    def test_relation_to_relational(self):
        c = _concept(stype=SemanticType.RELATION)
        assert classify_concept_type(c) is SingleConceptType.RELATIONAL

    def test_norm_to_relational(self):
        c = _concept(stype=SemanticType.NORM)
        assert classify_concept_type(c) is SingleConceptType.RELATIONAL


# ═══════════════════════════════════════════════════════════════════════
# classify_candidate_role
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyCandidateRole:
    """Test concept type + POS → CandidateRole."""

    def test_existential_ism_default(self):
        """ENTITY noun → MUSNAD_ILAYH."""
        role = classify_candidate_role(SingleConceptType.EXISTENTIAL, _closure(pos=POS.ISM))
        assert role is CandidateRole.MUSNAD_ILAYH

    def test_descriptive_sifa_default(self):
        """DESCRIPTIVE adjective → MUSNAD (from concept type)."""
        role = classify_candidate_role(SingleConceptType.DESCRIPTIVE, _closure(pos=POS.SIFA))
        assert role is CandidateRole.MUSNAD

    def test_eventive_fi3l_default(self):
        """EVENTIVE verb → MUSNAD (from concept type)."""
        role = classify_candidate_role(SingleConceptType.EVENTIVE, _closure(pos=POS.FI3L))
        assert role is CandidateRole.MUSNAD

    def test_harf_override(self):
        """Particle always → RABIT regardless of concept type."""
        role = classify_candidate_role(SingleConceptType.RELATIONAL, _closure(pos=POS.HARF))
        assert role is CandidateRole.RABIT

    def test_zarf_override(self):
        """Adverb always → QAYD."""
        role = classify_candidate_role(SingleConceptType.DESCRIPTIVE, _closure(pos=POS.ZARF))
        assert role is CandidateRole.QAYD

    def test_damir_override(self):
        """Pronoun always → MUSNAD_ILAYH."""
        role = classify_candidate_role(SingleConceptType.EXISTENTIAL, _closure(pos=POS.DAMIR))
        assert role is CandidateRole.MUSNAD_ILAYH


# ═══════════════════════════════════════════════════════════════════════
# Isomorphism
# ═══════════════════════════════════════════════════════════════════════


class TestIsomorphism:
    """Test the five isomorphism axes."""

    def test_all_match_entity_noun(self):
        """Entity noun with ENTITY semantic type → all axes pass."""
        cl = _closure(pos=POS.ISM)
        co = _concept(stype=SemanticType.ENTITY)
        iso = check_isomorphism(cl, co, SingleConceptType.EXISTENTIAL)
        assert iso.direction_match is True
        assert iso.type_match is True
        assert iso.boundary_match is True
        assert iso.function_match is True
        assert iso.transition_match is True
        assert iso.all_match is True

    def test_type_mismatch(self):
        """Verb (FI3L) with ENTITY → type_match fails."""
        cl = _closure(pos=POS.FI3L)
        co = _concept(stype=SemanticType.ENTITY)
        iso = check_isomorphism(cl, co, SingleConceptType.EXISTENTIAL)
        assert iso.type_match is False
        assert iso.all_match is False

    def test_boundary_mismatch_empty_surface(self):
        """Empty surface → boundary_match fails."""
        cl = _closure(surface="")
        co = _concept(stype=SemanticType.ENTITY)
        iso = check_isomorphism(cl, co, SingleConceptType.EXISTENTIAL)
        assert iso.boundary_match is False
        assert iso.all_match is False

    def test_boundary_mismatch_empty_label(self):
        """Empty label → boundary_match fails."""
        cl = _closure()
        co = _concept(label="")
        iso = check_isomorphism(cl, co, SingleConceptType.EXISTENTIAL)
        assert iso.boundary_match is False
        assert iso.all_match is False

    def test_transition_mismatch_unknown_pos(self):
        """UNKNOWN POS → transition_match fails."""
        cl = _closure(pos=POS.UNKNOWN)
        co = _concept(stype=SemanticType.ENTITY)
        iso = check_isomorphism(cl, co, SingleConceptType.EXISTENTIAL)
        assert iso.transition_match is False
        assert iso.all_match is False

    def test_direction_mismatch(self):
        """ENTITY concept claimed as RELATIONAL → direction_match fails."""
        cl = _closure(pos=POS.ISM)
        co = _concept(stype=SemanticType.ENTITY)
        iso = check_isomorphism(cl, co, SingleConceptType.RELATIONAL)
        assert iso.direction_match is False

    def test_event_verb_all_match(self):
        """Event verb with EVENT semantic type → all match."""
        cl = _closure(pos=POS.FI3L)
        co = _concept(stype=SemanticType.EVENT)
        iso = check_isomorphism(cl, co, SingleConceptType.EVENTIVE)
        assert iso.all_match is True


# ═══════════════════════════════════════════════════════════════════════
# Dalala
# ═══════════════════════════════════════════════════════════════════════


class TestDalala:
    """Test three-level signification analysis."""

    def test_mutabaqa_content(self):
        cl = _closure(surface="أسد")
        co = _concept(label="أسد")
        d = analyze_dalala(cl, co, DalalaType.MUTABAQA)
        assert "أسد↔أسد" in d.mutabaqa

    def test_tadammun_contains_semantic_type(self):
        cl = _closure()
        co = _concept(stype=SemanticType.ENTITY)
        d = analyze_dalala(cl, co, DalalaType.TADAMMUN)
        assert "ENTITY" in d.tadammun

    def test_iltizam_contains_dalala_name(self):
        cl = _closure()
        co = _concept()
        d = analyze_dalala(cl, co, DalalaType.ILTIZAM)
        assert "ILTIZAM" in d.iltizam

    def test_tadammun_includes_properties(self):
        cl = _closure()
        co = _concept(animal="yes")
        d = analyze_dalala(cl, co, DalalaType.MUTABAQA)
        assert "animal=yes" in d.tadammun

    def test_iltizam_contains_pos(self):
        cl = _closure(pos=POS.FI3L)
        co = _concept()
        d = analyze_dalala(cl, co, DalalaType.MUTABAQA)
        assert "FI3L" in d.iltizam


# ═══════════════════════════════════════════════════════════════════════
# Gates
# ═══════════════════════════════════════════════════════════════════════


class TestGates:
    """Test each of the 8 gates individually."""

    def test_gate_type_passed(self):
        rec = build_single_concept(_closure(), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_TYPE)
        assert gate.status is TransitionGateStatus.PASSED

    def test_gate_direction_passed(self):
        rec = build_single_concept(_closure(), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_DIRECTION)
        assert gate.status is TransitionGateStatus.PASSED

    def test_gate_up_passed(self):
        rec = build_single_concept(_closure(), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_UNIVERSAL_PARTICULAR)
        assert gate.status is TransitionGateStatus.PASSED

    def test_gate_ea_passed(self):
        rec = build_single_concept(_closure(), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_ENTITY_ATTRIBUTE)
        assert gate.status is TransitionGateStatus.PASSED

    def test_gate_reference_load_passed(self):
        rec = build_single_concept(_closure(), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_REFERENCE_LOAD)
        assert gate.status is TransitionGateStatus.PASSED

    def test_gate_predicative_load_passed(self):
        rec = build_single_concept(_closure(), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_PREDICATIVE_LOAD)
        assert gate.status is TransitionGateStatus.PASSED

    def test_gate_role_readiness_passed(self):
        rec = build_single_concept(_closure(), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_ROLE_READINESS)
        assert gate.status is TransitionGateStatus.PASSED

    def test_gate_recoverability_passed(self):
        rec = build_single_concept(_closure(), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_RECOVERABILITY)
        assert gate.status is TransitionGateStatus.PASSED

    def test_gate_recoverability_blocked_empty_surface(self):
        """Empty surface → recoverability BLOCKED."""
        rec = build_single_concept(_closure(surface="  "), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_RECOVERABILITY)
        assert gate.status is TransitionGateStatus.BLOCKED

    def test_gate_recoverability_blocked_unknown_pos(self):
        """UNKNOWN POS → recoverability BLOCKED."""
        rec = build_single_concept(_closure(pos=POS.UNKNOWN), _concept())
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_RECOVERABILITY)
        assert gate.status is TransitionGateStatus.BLOCKED

    def test_gate_recoverability_blocked_empty_label(self):
        """Empty label → recoverability BLOCKED."""
        rec = build_single_concept(_closure(), _concept(label=""))
        gate = next(g for g in rec.gates if g.gate_id is ConceptGateID.GATE_RECOVERABILITY)
        assert gate.status is TransitionGateStatus.BLOCKED


# ═══════════════════════════════════════════════════════════════════════
# Readiness
# ═══════════════════════════════════════════════════════════════════════


class TestReadiness:
    """Test readiness score computation."""

    def test_all_passed(self):
        gates = tuple(
            SingleConceptGateResult(
                gate_id=gid,
                status=TransitionGateStatus.PASSED,
            )
            for gid in ConceptGateID
        )
        assert compute_readiness(gates) == 1.0

    def test_none_passed(self):
        gates = tuple(
            SingleConceptGateResult(
                gate_id=gid,
                status=TransitionGateStatus.BLOCKED,
            )
            for gid in ConceptGateID
        )
        assert compute_readiness(gates) == 0.0

    def test_half_passed(self):
        gates_list = list(ConceptGateID)
        gates = tuple(
            SingleConceptGateResult(
                gate_id=gid,
                status=(
                    TransitionGateStatus.PASSED
                    if i < len(gates_list) // 2
                    else TransitionGateStatus.BLOCKED
                ),
            )
            for i, gid in enumerate(gates_list)
        )
        assert compute_readiness(gates) == pytest.approx(0.5)

    def test_empty_gates(self):
        assert compute_readiness(()) == 0.0

    def test_threshold_boundary(self):
        """Entity noun with full data → readiness = 1.0 ≥ 0.7."""
        rec = build_single_concept(_closure(), _concept())
        assert rec.readiness_score >= 0.7
        assert rec.valid is True


# ═══════════════════════════════════════════════════════════════════════
# build_single_concept — end-to-end
# ═══════════════════════════════════════════════════════════════════════


class TestBuildSingleConcept:
    """End-to-end tests for the main factory."""

    def test_entity_noun(self):
        """Entity noun → valid existential concept."""
        rec = build_single_concept(
            _closure(surface="الكِتَاب", lemma="كتاب", pos=POS.ISM),
            _concept(label="كتاب", stype=SemanticType.ENTITY),
        )
        assert rec.valid is True
        assert rec.concept_type is SingleConceptType.EXISTENTIAL
        assert rec.candidate_role is CandidateRole.MUSNAD_ILAYH
        assert rec.universal_particular is ConceptUniversalParticular.UNIVERSAL
        assert rec.entity_attribute is ConceptEntityAttribute.ENTITY
        assert isinstance(rec.record_id, str)
        assert rec.record_id.startswith("SC_")

    def test_descriptive_adjective(self):
        """Descriptive adjective → valid descriptive concept."""
        rec = build_single_concept(
            _closure(surface="كَبِير", lemma="كبير", pos=POS.SIFA),
            _concept(label="كبير", stype=SemanticType.ATTRIBUTE),
        )
        assert rec.valid is True
        assert rec.concept_type is SingleConceptType.DESCRIPTIVE
        assert rec.candidate_role is CandidateRole.MUSNAD

    def test_event_verb(self):
        """Event verb → valid eventive concept."""
        rec = build_single_concept(
            _closure(surface="كَتَبَ", lemma="كتب", pos=POS.FI3L),
            _concept(label="كتب", stype=SemanticType.EVENT),
        )
        assert rec.valid is True
        assert rec.concept_type is SingleConceptType.EVENTIVE
        assert rec.candidate_role is CandidateRole.MUSNAD

    def test_relational_particle(self):
        """Relational particle → valid relational concept."""
        rec = build_single_concept(
            _closure(surface="فِي", lemma="في", pos=POS.HARF),
            _concept(label="في", stype=SemanticType.RELATION),
        )
        assert rec.valid is True
        assert rec.concept_type is SingleConceptType.RELATIONAL
        assert rec.candidate_role is CandidateRole.RABIT

    def test_invalid_empty_label(self):
        """Missing label → valid=False (boundaries fail)."""
        rec = build_single_concept(
            _closure(),
            _concept(label=""),
        )
        assert rec.valid is False

    def test_invalid_unknown_pos(self):
        """UNKNOWN POS → valid=False (transition match fails)."""
        rec = build_single_concept(
            _closure(pos=POS.UNKNOWN),
            _concept(),
        )
        assert rec.valid is False

    def test_custom_record_id(self):
        rec = build_single_concept(
            _closure(), _concept(), record_id="MY_001"
        )
        assert rec.record_id == "MY_001"

    def test_custom_overrides(self):
        rec = build_single_concept(
            _closure(), _concept(),
            universal_particular=ConceptUniversalParticular.PARTICULAR,
            entity_attribute=ConceptEntityAttribute.ATTRIBUTE,
            candidate_role=CandidateRole.QAYD,
            closure_status=ConceptClosureStatus.OPEN,
            independence=ConceptIndependence.SUBORDINATE,
        )
        assert rec.universal_particular is ConceptUniversalParticular.PARTICULAR
        assert rec.entity_attribute is ConceptEntityAttribute.ATTRIBUTE
        assert rec.candidate_role is CandidateRole.QAYD
        assert rec.closure_status is ConceptClosureStatus.OPEN
        assert rec.independence is ConceptIndependence.SUBORDINATE

    def test_notes(self):
        rec = build_single_concept(_closure(), _concept(), notes="test note")
        assert rec.notes == "test note"

    def test_dalala_type_iltizam(self):
        rec = build_single_concept(
            _closure(), _concept(),
            dalala_type=DalalaType.ILTIZAM,
        )
        assert rec.direction is DalalaType.ILTIZAM

    def test_frozen_record(self):
        rec = build_single_concept(_closure(), _concept())
        with pytest.raises(AttributeError):
            rec.valid = False  # type: ignore[misc]

    def test_loads_reflect_dalala(self):
        """MUTABAQA → ref_load=1.0, ILTIZAM → ref_load=0.3."""
        rec_m = build_single_concept(_closure(), _concept(), dalala_type=DalalaType.MUTABAQA)
        rec_i = build_single_concept(_closure(), _concept(), dalala_type=DalalaType.ILTIZAM)
        assert rec_m.reference_load == pytest.approx(1.0)
        assert rec_i.reference_load == pytest.approx(0.3)

    def test_isomorphism_attached(self):
        rec = build_single_concept(_closure(), _concept())
        assert isinstance(rec.isomorphism, SingleConceptIsomorphism)
        assert rec.isomorphism.all_match is True

    def test_dalala_attached(self):
        rec = build_single_concept(_closure(), _concept())
        assert isinstance(rec.dalala, SingleConceptDalala)
        assert rec.dalala.mutabaqa != ""

    def test_gates_count(self):
        rec = build_single_concept(_closure(), _concept())
        assert len(rec.gates) == 8


# ═══════════════════════════════════════════════════════════════════════
# Acceptance criteria (المادة 81–82)
# ═══════════════════════════════════════════════════════════════════════


class TestAcceptanceCriteria:
    """Test acceptance_summary for valid and invalid records."""

    def test_all_criteria_pass(self):
        rec = build_single_concept(_closure(), _concept())
        summary = acceptance_summary(rec)
        assert all(summary.values()), f"Failed criteria: {summary}"

    def test_lexeme_match_fails_on_mismatch(self):
        """Type mismatch (FI3L + ENTITY) → lexeme_match fails."""
        rec = build_single_concept(
            _closure(pos=POS.FI3L),
            _concept(stype=SemanticType.ENTITY),
        )
        summary = acceptance_summary(rec)
        assert summary["lexeme_match"] is False

    def test_readiness_threshold_false(self):
        rec = build_single_concept(_closure(pos=POS.UNKNOWN), _concept())
        summary = acceptance_summary(rec)
        assert summary["readiness_threshold"] is False

    def test_recoverable_false_on_empty_surface(self):
        rec = build_single_concept(_closure(surface="  "), _concept())
        summary = acceptance_summary(rec)
        assert summary["recoverable"] is False

    def test_all_eight_keys_present(self):
        rec = build_single_concept(_closure(), _concept())
        summary = acceptance_summary(rec)
        assert len(summary) == 8
        expected_keys = {
            "lexeme_match",
            "type_established",
            "direction_established",
            "up_ea_established",
            "load_established",
            "role_established",
            "recoverable",
            "readiness_threshold",
        }
        assert set(summary.keys()) == expected_keys


# ═══════════════════════════════════════════════════════════════════════
# Batch
# ═══════════════════════════════════════════════════════════════════════


class TestBatch:
    """Test batch processing."""

    def test_batch_returns_correct_count(self):
        pairs = [
            (_closure(), _concept()),
            (_closure(pos=POS.FI3L), _concept(stype=SemanticType.EVENT)),
            (_closure(pos=POS.HARF), _concept(stype=SemanticType.RELATION)),
        ]
        results = build_single_concept_batch(pairs)
        assert len(results) == 3

    def test_batch_types(self):
        pairs = [
            (_closure(), _concept()),
            (_closure(pos=POS.FI3L), _concept(stype=SemanticType.EVENT)),
        ]
        results = build_single_concept_batch(pairs)
        assert results[0].concept_type is SingleConceptType.EXISTENTIAL
        assert results[1].concept_type is SingleConceptType.EVENTIVE

    def test_batch_all_valid(self):
        pairs = [
            (_closure(), _concept()),
            (_closure(pos=POS.FI3L), _concept(label="كتب", stype=SemanticType.EVENT)),
        ]
        results = build_single_concept_batch(pairs)
        assert all(r.valid for r in results)

    def test_batch_empty(self):
        results = build_single_concept_batch([])
        assert results == []


# ═══════════════════════════════════════════════════════════════════════
# Re-exports
# ═══════════════════════════════════════════════════════════════════════


class TestReExports:
    """Verify that all new types are importable from arabic_engine.core."""

    def test_enums_from_core(self):
        import arabic_engine.core as _core
        assert hasattr(_core, "SingleConceptType")
        assert hasattr(_core, "CandidateRole")
        assert hasattr(_core, "ConceptClosureStatus")
        assert hasattr(_core, "ConceptEntityAttribute")
        assert hasattr(_core, "ConceptGateID")
        assert hasattr(_core, "ConceptIndependence")
        assert hasattr(_core, "ConceptUniversalParticular")
        assert len(_core.CandidateRole) == 6

    def test_types_from_core(self):
        import arabic_engine.core as _core
        assert hasattr(_core, "SingleConceptRecord")
        assert hasattr(_core, "SingleConceptGateResult")
        assert hasattr(_core, "SingleConceptIsomorphism")
        assert hasattr(_core, "SingleConceptDalala")

    def test_enum_in_all(self):
        from arabic_engine.core import __all__
        assert "SingleConceptType" in __all__
        assert "CandidateRole" in __all__
        assert "ConceptGateID" in __all__

    def test_types_in_all(self):
        from arabic_engine.core import __all__
        assert "SingleConceptRecord" in __all__
        assert "SingleConceptIsomorphism" in __all__
        assert "SingleConceptDalala" in __all__
        assert "SingleConceptGateResult" in __all__


# ═══════════════════════════════════════════════════════════════════════
# Isomorphism property
# ═══════════════════════════════════════════════════════════════════════


class TestIsomorphismProperty:
    """Test the all_match property on SingleConceptIsomorphism."""

    def test_all_true(self):
        iso = SingleConceptIsomorphism(
            direction_match=True,
            type_match=True,
            boundary_match=True,
            function_match=True,
            transition_match=True,
        )
        assert iso.all_match is True

    def test_one_false(self):
        iso = SingleConceptIsomorphism(
            direction_match=True,
            type_match=False,
            boundary_match=True,
            function_match=True,
            transition_match=True,
        )
        assert iso.all_match is False

    def test_all_false(self):
        iso = SingleConceptIsomorphism(
            direction_match=False,
            type_match=False,
            boundary_match=False,
            function_match=False,
            transition_match=False,
        )
        assert iso.all_match is False


# ═══════════════════════════════════════════════════════════════════════
# Frozen record immutability
# ═══════════════════════════════════════════════════════════════════════


class TestFrozenDataclasses:
    """Verify that all new dataclasses are frozen."""

    def test_gate_result_frozen(self):
        gr = SingleConceptGateResult(
            gate_id=ConceptGateID.GATE_TYPE,
            status=TransitionGateStatus.PASSED,
        )
        with pytest.raises(AttributeError):
            gr.status = TransitionGateStatus.BLOCKED  # type: ignore[misc]

    def test_isomorphism_frozen(self):
        iso = SingleConceptIsomorphism(
            direction_match=True,
            type_match=True,
            boundary_match=True,
            function_match=True,
            transition_match=True,
        )
        with pytest.raises(AttributeError):
            iso.type_match = False  # type: ignore[misc]

    def test_dalala_frozen(self):
        d = SingleConceptDalala(
            mutabaqa="a", tadammun="b", iltizam="c",
        )
        with pytest.raises(AttributeError):
            d.mutabaqa = "x"  # type: ignore[misc]
