"""Tests for the Universal / Particular Constitution v1.

Validates:
  * Enum completeness for all 4 new enums.
  * classify_universality — scope / domain / is_universal derivation.
  * evaluate_boundary — valid and invalid boundary checks.
  * validate_fractal_law — well-formed and broken fractal trees.
  * compute_minimum_completeness — minimal viable structure.
  * build_constitution_result — end-to-end constitution verdicts.
  * acceptance_criteria — ACCEPTED / REJECTED / INCOMPLETE outcomes.
  * batch_classify — convenience batch wrapper.
  * Re-exports from arabic_engine.core.
"""

from __future__ import annotations

import pytest

from arabic_engine.core.enums import (
    BoundaryType,
    ConceptRelationType,
    SemanticType,
    UniversalityScope,
    UniversalParticularDomain,
    UPConstitutionOutcome,
)
from arabic_engine.core.types import (
    BoundaryRecord,
    Concept,
    ConceptRelation,
    UPConstitutionResult,
)
from arabic_engine.signified.universal_particular_v1 import (
    acceptance_criteria,
    batch_classify,
    build_constitution_result,
    classify_universality,
    compute_minimum_completeness,
    evaluate_boundary,
    validate_fractal_law,
)

# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════


def _concept(
    cid: int,
    label: str,
    stype: SemanticType = SemanticType.ENTITY,
) -> Concept:
    return Concept(concept_id=cid, label=label, semantic_type=stype)


# ═══════════════════════════════════════════════════════════════════════
# Phase 1: Enum completeness
# ═══════════════════════════════════════════════════════════════════════


class TestEnumCompleteness:
    """Verify member counts for all 4 new enums."""

    def test_universality_scope_has_4_members(self) -> None:
        assert len(UniversalityScope) == 4

    def test_universality_scope_members(self) -> None:
        assert {m.name for m in UniversalityScope} == {
            "GENUS", "SPECIES", "INDIVIDUAL", "UNRESOLVED",
        }

    def test_universal_particular_domain_has_2_members(self) -> None:
        assert len(UniversalParticularDomain) == 2

    def test_universal_particular_domain_members(self) -> None:
        assert {m.name for m in UniversalParticularDomain} == {
            "ENTITY", "ATTRIBUTE",
        }

    def test_boundary_type_has_5_members(self) -> None:
        assert len(BoundaryType) == 5

    def test_boundary_type_members(self) -> None:
        assert {m.name for m in BoundaryType} == {
            "ENTITY_ATTRIBUTE",
            "UNIVERSAL_PARTICULAR",
            "GENUS_SPECIES",
            "SPECIES_INDIVIDUAL",
            "GENERAL_DESCRIPTION_SPECIFIC_FORM",
        }

    def test_up_constitution_outcome_has_3_members(self) -> None:
        assert len(UPConstitutionOutcome) == 3

    def test_up_constitution_outcome_members(self) -> None:
        assert {m.name for m in UPConstitutionOutcome} == {
            "ACCEPTED", "REJECTED", "INCOMPLETE",
        }


# ═══════════════════════════════════════════════════════════════════════
# Phase 2: Classification tests
# ═══════════════════════════════════════════════════════════════════════


class TestClassifyUniversality:
    """Test classify_universality() for various concept types."""

    # ── Entity-domain genus ─────────────────────────────────────────

    def test_entity_genus_hayawan(self) -> None:
        c = _concept(1, "حيوان")
        rec = classify_universality(c)
        assert rec.scope is UniversalityScope.GENUS
        assert rec.domain is UniversalParticularDomain.ENTITY
        assert rec.is_universal is True
        assert rec.fractal_depth == 0

    def test_entity_genus_jism(self) -> None:
        c = _concept(2, "جسم")
        rec = classify_universality(c)
        assert rec.scope is UniversalityScope.GENUS
        assert rec.is_universal is True

    # ── Entity-domain species ───────────────────────────────────────

    def test_entity_species_insan(self) -> None:
        c = _concept(3, "إنسان")
        rec = classify_universality(c)
        assert rec.scope is UniversalityScope.SPECIES
        assert rec.domain is UniversalParticularDomain.ENTITY
        assert rec.is_universal is True
        assert rec.fractal_depth == 1

    def test_entity_species_faras(self) -> None:
        c = _concept(4, "فرس")
        rec = classify_universality(c)
        assert rec.scope is UniversalityScope.SPECIES

    # ── Entity-domain individual ────────────────────────────────────

    def test_entity_individual_zayd(self) -> None:
        c = _concept(5, "زيد")
        rec = classify_universality(c)
        assert rec.scope is UniversalityScope.INDIVIDUAL
        assert rec.domain is UniversalParticularDomain.ENTITY
        assert rec.is_universal is False
        assert rec.fractal_depth == 2

    def test_entity_individual_demonstrative(self) -> None:
        c = _concept(6, "هذا الرجل")
        rec = classify_universality(c)
        assert rec.scope is UniversalityScope.INDIVIDUAL
        assert rec.is_universal is False

    # ── Attribute-domain genus ──────────────────────────────────────

    def test_attribute_genus_lawn(self) -> None:
        c = _concept(7, "لون", SemanticType.ATTRIBUTE)
        rec = classify_universality(c)
        assert rec.scope is UniversalityScope.GENUS
        assert rec.domain is UniversalParticularDomain.ATTRIBUTE
        assert rec.is_universal is True
        assert BoundaryType.ENTITY_ATTRIBUTE in rec.boundary_markers

    # ── Attribute-domain species ────────────────────────────────────

    def test_attribute_species_ahmar(self) -> None:
        c = _concept(8, "أحمر", SemanticType.ATTRIBUTE)
        rec = classify_universality(c)
        assert rec.scope is UniversalityScope.SPECIES
        assert rec.domain is UniversalParticularDomain.ATTRIBUTE
        assert rec.is_universal is True

    # ── Attribute-domain individual ─────────────────────────────────

    def test_attribute_individual_specific_redness(self) -> None:
        c = _concept(9, "هذا اللون", SemanticType.ATTRIBUTE)
        rec = classify_universality(c)
        assert rec.scope is UniversalityScope.INDIVIDUAL
        assert rec.domain is UniversalParticularDomain.ATTRIBUTE
        assert rec.is_universal is False

    # ── Mathematical is_universal derivation ────────────────────────

    def test_is_universal_true_for_genus(self) -> None:
        rec = classify_universality(_concept(10, "حيوان"))
        assert rec.is_universal is True

    def test_is_universal_true_for_species(self) -> None:
        rec = classify_universality(_concept(11, "إنسان"))
        assert rec.is_universal is True

    def test_is_universal_false_for_individual(self) -> None:
        rec = classify_universality(_concept(12, "زيد"))
        assert rec.is_universal is False

    # ── Custom parameters ───────────────────────────────────────────

    def test_custom_record_id(self) -> None:
        rec = classify_universality(_concept(13, "حيوان"), record_id="MY_01")
        assert rec.record_id == "MY_01"

    def test_custom_genus_species_ids(self) -> None:
        rec = classify_universality(
            _concept(14, "إنسان"), genus_id=1, species_id=None,
        )
        assert rec.genus_id == 1

    def test_custom_fractal_depth(self) -> None:
        rec = classify_universality(
            _concept(15, "حيوان"), fractal_depth=5,
        )
        assert rec.fractal_depth == 5

    # ── Record frozen ───────────────────────────────────────────────

    def test_record_is_frozen(self) -> None:
        rec = classify_universality(_concept(16, "حيوان"))
        with pytest.raises(AttributeError):
            rec.scope = UniversalityScope.SPECIES  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════
# Phase 3: Boundary evaluation tests
# ═══════════════════════════════════════════════════════════════════════


class TestEvaluateBoundary:
    """Test evaluate_boundary() for various boundary types."""

    def test_valid_genus_species_boundary(self) -> None:
        genus = _concept(1, "حيوان")
        species = _concept(2, "إنسان")
        br = evaluate_boundary(genus, species, BoundaryType.GENUS_SPECIES)
        assert br.is_valid is True
        assert br.violation_reason is None

    def test_valid_species_individual_boundary(self) -> None:
        species = _concept(1, "إنسان")
        individual = _concept(2, "زيد")
        br = evaluate_boundary(species, individual, BoundaryType.SPECIES_INDIVIDUAL)
        assert br.is_valid is True

    def test_invalid_same_level_crossing(self) -> None:
        genus1 = _concept(1, "حيوان")
        genus2 = _concept(2, "نبات")
        br = evaluate_boundary(genus1, genus2, BoundaryType.GENUS_SPECIES)
        assert br.is_valid is False
        assert br.violation_reason is not None

    def test_entity_attribute_boundary_valid(self) -> None:
        entity = _concept(1, "حيوان", SemanticType.ENTITY)
        attr = _concept(2, "لون", SemanticType.ATTRIBUTE)
        br = evaluate_boundary(entity, attr, BoundaryType.ENTITY_ATTRIBUTE)
        assert br.is_valid is True

    def test_entity_attribute_boundary_invalid_same_domain(self) -> None:
        c1 = _concept(1, "حيوان", SemanticType.ENTITY)
        c2 = _concept(2, "جسم", SemanticType.ENTITY)
        br = evaluate_boundary(c1, c2, BoundaryType.ENTITY_ATTRIBUTE)
        assert br.is_valid is False

    def test_general_description_specific_form_valid(self) -> None:
        general = _concept(1, "حيوان")  # genus
        specific = _concept(2, "زيد")  # individual
        br = evaluate_boundary(
            general, specific, BoundaryType.GENERAL_DESCRIPTION_SPECIFIC_FORM,
        )
        assert br.is_valid is True

    def test_custom_boundary_id(self) -> None:
        genus = _concept(1, "حيوان")
        species = _concept(2, "إنسان")
        br = evaluate_boundary(
            genus, species, BoundaryType.GENUS_SPECIES, boundary_id="BD_CUSTOM",
        )
        assert br.boundary_id == "BD_CUSTOM"

    def test_boundary_record_is_frozen(self) -> None:
        genus = _concept(1, "حيوان")
        species = _concept(2, "إنسان")
        br = evaluate_boundary(genus, species, BoundaryType.GENUS_SPECIES)
        with pytest.raises(AttributeError):
            br.is_valid = False  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════
# Phase 4: Fractal law tests
# ═══════════════════════════════════════════════════════════════════════


class TestFractalLaw:
    """Test validate_fractal_law()."""

    def test_valid_fractal_tree(self) -> None:
        records = [
            classify_universality(_concept(1, "حيوان")),   # depth 0
            classify_universality(_concept(2, "إنسان")),   # depth 1
            classify_universality(_concept(3, "زيد")),      # depth 2
        ]
        assert validate_fractal_law(records) is True

    def test_empty_records(self) -> None:
        assert validate_fractal_law([]) is True

    def test_broken_tree_individual_only(self) -> None:
        """An individual with no universal above → should fail."""
        records = [
            classify_universality(_concept(1, "زيد")),  # depth 2, no genus/species
        ]
        assert validate_fractal_law(records) is False

    def test_genus_only_no_children(self) -> None:
        """A genus with no children → fractal law requires descendants."""
        records = [
            classify_universality(_concept(1, "حيوان")),  # depth 0, no depth 1
        ]
        assert validate_fractal_law(records) is False

    def test_deep_nesting_valid(self) -> None:
        """Sub-genera work when depth chain is complete."""
        records = [
            classify_universality(_concept(1, "حيوان"), fractal_depth=0),
            classify_universality(_concept(2, "إنسان"), fractal_depth=1),
            classify_universality(_concept(3, "زيد"), fractal_depth=2),
        ]
        assert validate_fractal_law(records) is True


# ═══════════════════════════════════════════════════════════════════════
# Phase 5: Minimum completeness tests
# ═══════════════════════════════════════════════════════════════════════


class TestMinimumCompleteness:
    """Test compute_minimum_completeness()."""

    def test_complete_structure(self) -> None:
        records = [
            classify_universality(_concept(1, "حيوان")),
            classify_universality(_concept(2, "إنسان")),
            classify_universality(_concept(3, "زيد")),
        ]
        assert compute_minimum_completeness(records) is True

    def test_missing_species(self) -> None:
        records = [
            classify_universality(_concept(1, "حيوان")),
            classify_universality(_concept(2, "زيد")),
        ]
        assert compute_minimum_completeness(records) is False

    def test_missing_individual(self) -> None:
        records = [
            classify_universality(_concept(1, "حيوان")),
            classify_universality(_concept(2, "إنسان")),
        ]
        assert compute_minimum_completeness(records) is False

    def test_genus_only(self) -> None:
        records = [
            classify_universality(_concept(1, "حيوان")),
        ]
        assert compute_minimum_completeness(records) is False

    def test_empty_records(self) -> None:
        assert compute_minimum_completeness([]) is False


# ═══════════════════════════════════════════════════════════════════════
# Phase 6: End-to-end constitution tests
# ═══════════════════════════════════════════════════════════════════════


class TestBuildConstitutionResult:
    """Test build_constitution_result() end-to-end."""

    def test_full_valid_constitution_accepted(self) -> None:
        concepts = [
            _concept(1, "حيوان"),
            _concept(2, "إنسان"),
            _concept(3, "زيد"),
        ]
        relations = [
            ConceptRelation(
                source_id=2, target_id=1,
                relation_type=ConceptRelationType.IS_A,
            ),
            ConceptRelation(
                source_id=3, target_id=2,
                relation_type=ConceptRelationType.INSTANTIATES,
            ),
        ]
        result = build_constitution_result(concepts, relations)
        assert result.outcome is UPConstitutionOutcome.ACCEPTED
        assert len(result.records) == 3
        assert result.fractal_depth_max == 2
        assert not result.errors

    def test_boundary_violation_rejected(self) -> None:
        """Two genera linked as genus→species should produce an invalid boundary."""
        concepts = [
            _concept(1, "حيوان"),
            _concept(2, "نبات"),
        ]
        relations = [
            ConceptRelation(
                source_id=2, target_id=1,
                relation_type=ConceptRelationType.IS_A,
            ),
        ]
        result = build_constitution_result(concepts, relations)
        # genus→genus boundary should be invalid
        assert any(not b.is_valid for b in result.boundaries)
        assert result.outcome is UPConstitutionOutcome.REJECTED

    def test_incomplete_structure(self) -> None:
        """Genus + species only → INCOMPLETE."""
        concepts = [
            _concept(1, "حيوان"),
            _concept(2, "إنسان"),
        ]
        relations = [
            ConceptRelation(
                source_id=2, target_id=1,
                relation_type=ConceptRelationType.IS_A,
            ),
        ]
        result = build_constitution_result(concepts, relations)
        # May be INCOMPLETE because no individual
        assert result.outcome in (
            UPConstitutionOutcome.INCOMPLETE,
            UPConstitutionOutcome.REJECTED,
        )

    def test_custom_result_id(self) -> None:
        result = build_constitution_result([], [], result_id="MY_CR_001")
        assert result.result_id == "MY_CR_001"

    def test_unknown_concept_in_relation(self) -> None:
        concepts = [_concept(1, "حيوان")]
        relations = [
            ConceptRelation(
                source_id=99, target_id=1,
                relation_type=ConceptRelationType.IS_A,
            ),
        ]
        result = build_constitution_result(concepts, relations)
        assert len(result.errors) > 0

    def test_cross_domain_boundary_entity_attribute(self) -> None:
        concepts = [
            _concept(1, "حيوان", SemanticType.ENTITY),
            _concept(2, "إنسان", SemanticType.ENTITY),
            _concept(3, "زيد", SemanticType.ENTITY),
            _concept(4, "لون", SemanticType.ATTRIBUTE),
            _concept(5, "أحمر", SemanticType.ATTRIBUTE),
            _concept(6, "هذا اللون", SemanticType.ATTRIBUTE),
        ]
        relations = [
            ConceptRelation(
                source_id=2, target_id=1,
                relation_type=ConceptRelationType.IS_A,
            ),
            ConceptRelation(
                source_id=3, target_id=2,
                relation_type=ConceptRelationType.INSTANTIATES,
            ),
            ConceptRelation(
                source_id=5, target_id=4,
                relation_type=ConceptRelationType.IS_A,
            ),
            ConceptRelation(
                source_id=6, target_id=5,
                relation_type=ConceptRelationType.INSTANTIATES,
            ),
        ]
        result = build_constitution_result(concepts, relations)
        # Should have at least one entity↔attribute boundary
        ea_boundaries = [
            b for b in result.boundaries
            if b.boundary_type is BoundaryType.ENTITY_ATTRIBUTE
        ]
        assert len(ea_boundaries) >= 1
        # The entity↔attribute boundary should be valid
        assert all(b.is_valid for b in ea_boundaries)

    def test_result_is_frozen(self) -> None:
        result = build_constitution_result([], [])
        with pytest.raises(AttributeError):
            result.outcome = UPConstitutionOutcome.ACCEPTED  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════
# Phase 7: Acceptance criteria tests
# ═══════════════════════════════════════════════════════════════════════


class TestAcceptanceCriteria:
    """Test acceptance_criteria()."""

    def test_accepted(self) -> None:
        concepts = [
            _concept(1, "حيوان"),
            _concept(2, "إنسان"),
            _concept(3, "زيد"),
        ]
        relations = [
            ConceptRelation(
                source_id=2, target_id=1,
                relation_type=ConceptRelationType.IS_A,
            ),
            ConceptRelation(
                source_id=3, target_id=2,
                relation_type=ConceptRelationType.INSTANTIATES,
            ),
        ]
        result = build_constitution_result(concepts, relations)
        assert acceptance_criteria(result) is UPConstitutionOutcome.ACCEPTED

    def test_rejected_with_errors(self) -> None:
        result = UPConstitutionResult(
            result_id="test",
            records=(),
            boundaries=(),
            outcome=UPConstitutionOutcome.REJECTED,
            errors=("some error",),
        )
        assert acceptance_criteria(result) is UPConstitutionOutcome.REJECTED

    def test_rejected_with_invalid_boundary(self) -> None:
        result = UPConstitutionResult(
            result_id="test",
            records=(),
            boundaries=(
                BoundaryRecord(
                    boundary_id="BD_001",
                    boundary_type=BoundaryType.GENUS_SPECIES,
                    left_concept_id=1,
                    right_concept_id=2,
                    is_valid=False,
                    violation_reason="test violation",
                ),
            ),
            outcome=UPConstitutionOutcome.REJECTED,
        )
        assert acceptance_criteria(result) is UPConstitutionOutcome.REJECTED

    def test_incomplete_no_records(self) -> None:
        result = UPConstitutionResult(
            result_id="test",
            records=(),
            boundaries=(),
            outcome=UPConstitutionOutcome.INCOMPLETE,
        )
        assert acceptance_criteria(result) is UPConstitutionOutcome.INCOMPLETE


# ═══════════════════════════════════════════════════════════════════════
# Phase 8: Batch classify tests
# ═══════════════════════════════════════════════════════════════════════


class TestBatchClassify:
    """Test batch_classify()."""

    def test_batch_empty(self) -> None:
        assert batch_classify([]) == []

    def test_batch_multiple(self) -> None:
        concepts = [
            _concept(1, "حيوان"),
            _concept(2, "إنسان"),
            _concept(3, "زيد"),
        ]
        records = batch_classify(concepts)
        assert len(records) == 3
        assert records[0].scope is UniversalityScope.GENUS
        assert records[1].scope is UniversalityScope.SPECIES
        assert records[2].scope is UniversalityScope.INDIVIDUAL

    def test_batch_preserves_order(self) -> None:
        concepts = [
            _concept(1, "زيد"),
            _concept(2, "حيوان"),
        ]
        records = batch_classify(concepts)
        assert records[0].concept_id == 1
        assert records[1].concept_id == 2


# ═══════════════════════════════════════════════════════════════════════
# Phase 9: Re-export tests
# ═══════════════════════════════════════════════════════════════════════


class TestReExports:
    """Verify new symbols are accessible from arabic_engine.core."""

    def test_universality_scope_reexport(self) -> None:
        from arabic_engine.core import UniversalityScope as US
        assert US.GENUS is not None

    def test_universal_particular_domain_reexport(self) -> None:
        from arabic_engine.core import UniversalParticularDomain as UPD
        assert UPD.ENTITY is not None

    def test_boundary_type_reexport(self) -> None:
        from arabic_engine.core import BoundaryType as BT
        assert BT.GENUS_SPECIES is not None

    def test_up_constitution_outcome_reexport(self) -> None:
        from arabic_engine.core import UPConstitutionOutcome as UCO
        assert UCO.ACCEPTED is not None

    def test_universal_particular_record_reexport(self) -> None:
        from arabic_engine.core import UniversalParticularRecord as UPR
        assert UPR is not None

    def test_boundary_record_reexport(self) -> None:
        from arabic_engine.core import BoundaryRecord as BR
        assert BR is not None

    def test_up_constitution_result_reexport(self) -> None:
        from arabic_engine.core import UPConstitutionResult as UCR
        assert UCR is not None


# ═══════════════════════════════════════════════════════════════════════
# Phase 10: Domain mapping tests
# ═══════════════════════════════════════════════════════════════════════


class TestDomainMapping:
    """Test domain mapping from SemanticType."""

    def test_entity_maps_to_entity_domain(self) -> None:
        rec = classify_universality(_concept(1, "حيوان", SemanticType.ENTITY))
        assert rec.domain is UniversalParticularDomain.ENTITY

    def test_event_maps_to_entity_domain(self) -> None:
        rec = classify_universality(_concept(2, "زيد", SemanticType.EVENT))
        assert rec.domain is UniversalParticularDomain.ENTITY

    def test_attribute_maps_to_attribute_domain(self) -> None:
        rec = classify_universality(_concept(3, "لون", SemanticType.ATTRIBUTE))
        assert rec.domain is UniversalParticularDomain.ATTRIBUTE

    def test_relation_maps_to_entity_domain(self) -> None:
        rec = classify_universality(_concept(4, "زيد", SemanticType.RELATION))
        assert rec.domain is UniversalParticularDomain.ENTITY

    def test_norm_maps_to_entity_domain(self) -> None:
        rec = classify_universality(_concept(5, "زيد", SemanticType.NORM))
        assert rec.domain is UniversalParticularDomain.ENTITY


# ═══════════════════════════════════════════════════════════════════════
# Phase 11: Boundary marker tests
# ═══════════════════════════════════════════════════════════════════════


class TestBoundaryMarkers:
    """Test boundary_markers field on records."""

    def test_genus_has_genus_species_marker(self) -> None:
        rec = classify_universality(_concept(1, "حيوان"))
        assert BoundaryType.GENUS_SPECIES in rec.boundary_markers
        assert BoundaryType.UNIVERSAL_PARTICULAR in rec.boundary_markers

    def test_species_has_both_markers(self) -> None:
        rec = classify_universality(_concept(2, "إنسان"))
        assert BoundaryType.GENUS_SPECIES in rec.boundary_markers
        assert BoundaryType.SPECIES_INDIVIDUAL in rec.boundary_markers

    def test_individual_has_species_individual_marker(self) -> None:
        rec = classify_universality(_concept(3, "زيد"))
        assert BoundaryType.SPECIES_INDIVIDUAL in rec.boundary_markers

    def test_attribute_domain_has_entity_attribute_marker(self) -> None:
        rec = classify_universality(_concept(4, "لون", SemanticType.ATTRIBUTE))
        assert BoundaryType.ENTITY_ATTRIBUTE in rec.boundary_markers
