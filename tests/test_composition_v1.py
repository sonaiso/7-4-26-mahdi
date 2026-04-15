"""Tests for the Composition / Syntax Constitution v1 package.

Validates:
  * All 13 composition enums are complete and correctly named.
  * All 14 composition dataclasses are frozen as designed.
  * Disambiguation: detect + resolve ambiguity, 6-rule hierarchy.
  * Conflict: detect + resolve semantic conflicts, 5-rule hierarchy.
  * Transfer: detect + validate semantic transfer, 4-condition check.
  * Truth type: determine + adjudicate truth types, 5-factor preference.
  * Admission: three gates, check_admission factory.
  * Predication: build + classify predication records.
  * Restriction: build + validate restriction records.
  * Dependency: build + validate dependency records.
  * Relations: build + classify composition relations.
  * Roles: assign + realize composition roles.
  * Proposition: build + close + classify propositions.
  * Inter-proposition: link propositions + validate links.
  * Gates: all 8 composition gates.
  * Composition: orchestrator compose + readiness + decompose.
  * Re-exports from arabic_engine.core.
"""

from __future__ import annotations

import pytest

from arabic_engine.composition import (
    adjudicate_truth,
    assign_role,
    build_dependency,
    build_predication,
    build_proposition,
    build_relation,
    build_restriction,
    check_admission,
    classify_predication,
    classify_proposition,
    classify_relation,
    close_proposition,
    compose,
    compute_readiness,
    decompose,
    detect_ambiguity,
    detect_conflict,
    detect_transfer,
    determine_truth_type,
    link_propositions,
    realize_role,
    resolve_ambiguity,
    resolve_conflict,
    run_all_gates,
    validate_composition,
    validate_dependency,
    validate_link,
    validate_restriction,
    validate_transfer,
)
from arabic_engine.core.enums import (
    AmbiguityResolution,
    AmbiguityType,
    CompositionGate,
    CompositionGateStatus,
    CompositionRelationType,
    CompositionRoleType,
    ConflictResolutionMethod,
    ConflictType,
    InterPropositionLinkType,
    POS,
    PropositionType,
    RoleStatus,
    SemanticType,
    TransferType,
    TruthType,
)
from arabic_engine.core.types import (
    CompositionGateResult,
    CompositionProposition,
    CompositionRelation,
    CompositionRole,
    CompositionStructure,
    CompositionUnit,
    DependencyRecord,
    DisambiguationRecord,
    InterPropositionLink,
    PredicationRecord,
    RestrictionRecord,
    SemanticConflictRecord,
    TransferRecord,
    TruthRecord,
)


# ── Helpers ─────────────────────────────────────────────────────────


def _admitted_unit(
    unit_id: str = "U1",
    label: str = "كتاب",
    pos: POS = POS.ISM,
) -> CompositionUnit:
    """Create a minimal admitted CompositionUnit."""
    return check_admission(unit_id=unit_id, label=label, pos=pos)


def _verbal_unit(unit_id: str = "UV", label: str = "ذهب") -> CompositionUnit:
    """Create an admitted verbal unit."""
    return check_admission(unit_id=unit_id, label=label, pos=POS.FI3L)


def _two_admitted_units() -> tuple[CompositionUnit, CompositionUnit]:
    """Return (subject, predicate) admitted units."""
    return _admitted_unit("U1", "الطالب"), _verbal_unit("U2", "ذهب")


# =====================================================================
# 1. Enum completeness
# =====================================================================


class TestEnumCompleteness:
    """All 13 composition enums have the expected members."""

    def test_ambiguity_type_members(self):
        names = {m.name for m in AmbiguityType}
        assert "LEXICAL_PURE" in names
        assert "SEMANTIC_DUAL" in names
        assert len(names) >= 2

    def test_ambiguity_resolution_members(self):
        names = {m.name for m in AmbiguityResolution}
        expected = {
            "INTERNAL_SEMANTIC_CUE",
            "REFERENTIAL_CUE",
            "SYNTACTIC_CUE",
            "WEIGHT_PRIORITY",
            "CONVENTIONAL_PRIORITY",
            "OPEN_PENDING",
        }
        assert expected <= names

    def test_conflict_type_members(self):
        names = {m.name for m in ConflictType}
        assert "ESSENTIAL_VS_DESCRIPTIVE" in names
        assert len(names) >= 2

    def test_conflict_resolution_method_members(self):
        names = {m.name for m in ConflictResolutionMethod}
        expected = {
            "RANK_DISTINCTION",
            "CONTEXT_DISTINCTION",
            "ORIGIN_VS_FOLLOWER",
            "REDUCE_TO_FIGURATIVE",
            "BLOCK_COMPOSITION",
        }
        assert expected <= names

    def test_transfer_type_members(self):
        names = {m.name for m in TransferType}
        assert "INTERNAL_LINGUISTIC" in names
        assert len(names) >= 2

    def test_truth_type_members(self):
        names = {m.name for m in TruthType}
        expected = {
            "LINGUISTIC_ORIGINAL",
            "CONVENTIONAL",
            "CONTROLLED_TRANSFER",
        }
        assert expected <= names

    def test_composition_relation_type_members(self):
        names = {m.name for m in CompositionRelationType}
        expected = {
            "PREDICATION",
            "RESTRICTION",
            "DEPENDENCY",
            "LINKING",
            "EXPLANATION",
        }
        assert expected <= names

    def test_composition_role_type_members(self):
        names = {m.name for m in CompositionRoleType}
        expected = {
            "MUSNAD_ILAYH",
            "MUSNAD",
            "QAYD",
            "TABI3",
            "RABIT",
            "MUFASSIR",
        }
        assert expected <= names

    def test_role_status_members(self):
        names = {m.name for m in RoleStatus}
        assert "CANDIDATE" in names
        assert "REALIZED" in names

    def test_proposition_type_members(self):
        names = {m.name for m in PropositionType}
        expected = {"NOMINAL", "VERBAL", "COPULAR"}
        assert expected <= names

    def test_inter_proposition_link_type_members(self):
        names = {m.name for m in InterPropositionLinkType}
        expected = {
            "CONJUNCTION",
            "CONDITION",
            "CAUSATION",
            "TEMPORAL",
            "ADVERSATIVE",
            "OTHER",
        }
        assert expected <= names

    def test_composition_gate_members(self):
        names = {m.name for m in CompositionGate}
        expected = {
            "DISAMBIGUATION",
            "REFERENCE_STABILITY",
            "PREDICATE_READINESS",
            "ROLE_ASSIGNMENT",
            "RELATION_VALIDITY",
            "CONFLICT_RESOLUTION",
            "PROPOSITION_CLOSURE",
            "INTER_PROPOSITION_LINK",
        }
        assert expected <= names

    def test_composition_gate_status_members(self):
        names = {m.name for m in CompositionGateStatus}
        expected = {"PASSED", "BLOCKED", "INSUFFICIENT_DATA"}
        assert expected <= names


# =====================================================================
# 2. Dataclass frozen checks
# =====================================================================


class TestDataclassesFrozen:
    """All 14 composition dataclasses should be frozen."""

    @pytest.mark.parametrize(
        "cls",
        [
            DisambiguationRecord,
            SemanticConflictRecord,
            TransferRecord,
            TruthRecord,
            CompositionUnit,
            PredicationRecord,
            RestrictionRecord,
            DependencyRecord,
            CompositionRelation,
            CompositionRole,
            CompositionProposition,
            InterPropositionLink,
            CompositionGateResult,
            CompositionStructure,
        ],
    )
    def test_frozen(self, cls):
        assert cls.__dataclass_params__.frozen  # type: ignore[attr-defined]


# =====================================================================
# 3. Disambiguation tests
# =====================================================================


class TestDisambiguation:
    """Tests for detect_ambiguity and resolve_ambiguity."""

    def test_no_ambiguity_single_direction(self):
        rec = detect_ambiguity("U1", "كتاب", ("book",))
        assert rec.ambiguity_type is None
        assert rec.resolved_direction == "book"
        assert rec.confidence == 1.0
        assert rec.resolution == AmbiguityResolution.INTERNAL_SEMANTIC_CUE

    def test_no_ambiguity_empty_directions(self):
        rec = detect_ambiguity("U1", "x", ())
        assert rec.ambiguity_type is None
        assert rec.resolved_direction == ""
        assert rec.confidence == 1.0

    def test_ambiguity_two_directions(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring"))
        assert rec.ambiguity_type == AmbiguityType.SEMANTIC_DUAL
        assert rec.resolution == AmbiguityResolution.OPEN_PENDING
        assert rec.confidence == 0.0
        assert rec.candidates == ("eye", "spring")

    def test_ambiguity_three_directions(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring", "spy"))
        assert rec.ambiguity_type == AmbiguityType.LEXICAL_PURE

    def test_resolve_with_semantic_cue(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring"))
        resolved = resolve_ambiguity(rec, {"semantic": "eye"})
        assert resolved.resolution == AmbiguityResolution.INTERNAL_SEMANTIC_CUE
        assert resolved.resolved_direction == "eye"
        assert resolved.confidence == 0.95

    def test_resolve_with_referential_cue(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring"))
        resolved = resolve_ambiguity(rec, {"referential": "spring"})
        assert resolved.resolution == AmbiguityResolution.REFERENTIAL_CUE
        assert resolved.resolved_direction == "spring"
        assert resolved.confidence == 0.85

    def test_resolve_with_syntactic_cue(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring"))
        resolved = resolve_ambiguity(rec, {"syntactic": "eye"})
        assert resolved.resolution == AmbiguityResolution.SYNTACTIC_CUE
        assert resolved.confidence == 0.75

    def test_resolve_with_weight_priority(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring"))
        resolved = resolve_ambiguity(rec, {"weight": "eye"})
        assert resolved.resolution == AmbiguityResolution.WEIGHT_PRIORITY
        assert resolved.confidence == 0.65

    def test_resolve_with_conventional_priority(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring"))
        resolved = resolve_ambiguity(rec, {"conventional": "spring"})
        assert resolved.resolution == AmbiguityResolution.CONVENTIONAL_PRIORITY
        assert resolved.confidence == 0.55

    def test_resolve_hierarchy_prefers_semantic(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring"))
        resolved = resolve_ambiguity(
            rec, {"semantic": "eye", "syntactic": "spring"},
        )
        assert resolved.resolution == AmbiguityResolution.INTERNAL_SEMANTIC_CUE

    def test_resolve_no_cues_stays_open(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring"))
        resolved = resolve_ambiguity(rec)
        assert resolved.resolution == AmbiguityResolution.OPEN_PENDING

    def test_resolve_cue_not_in_candidates_stays_open(self):
        rec = detect_ambiguity("U1", "عين", ("eye", "spring"))
        resolved = resolve_ambiguity(rec, {"semantic": "rain"})
        assert resolved.resolution == AmbiguityResolution.OPEN_PENDING

    def test_resolve_already_resolved_no_change(self):
        rec = detect_ambiguity("U1", "كتاب", ("book",))
        resolved = resolve_ambiguity(rec, {"semantic": "book"})
        assert resolved.resolution == AmbiguityResolution.INTERNAL_SEMANTIC_CUE


# =====================================================================
# 4. Conflict tests
# =====================================================================


class TestConflict:
    """Tests for detect_conflict and resolve_conflict."""

    def test_detect_conflict_default_type(self):
        rec = detect_conflict("U1", ("essential", "descriptive"))
        assert rec.conflict_type == ConflictType.ESSENTIAL_VS_DESCRIPTIVE
        assert not rec.resolved
        assert rec.resolution == ConflictResolutionMethod.BLOCK_COMPOSITION

    def test_detect_conflict_custom_type(self):
        rec = detect_conflict(
            "U1",
            ("a", "b"),
            conflict_type=ConflictType.FIGURATIVE_VS_LITERAL,
        )
        assert rec.conflict_type == ConflictType.FIGURATIVE_VS_LITERAL

    def test_resolve_with_rank(self):
        rec = detect_conflict("U1", ("a", "b"))
        resolved = resolve_conflict(rec, {"rank": "a wins by rank"})
        assert resolved.resolved
        assert resolved.resolution == ConflictResolutionMethod.RANK_DISTINCTION
        assert resolved.notes == "a wins by rank"

    def test_resolve_with_context(self):
        rec = detect_conflict("U1", ("a", "b"))
        resolved = resolve_conflict(rec, {"context": "b wins by context"})
        assert resolved.resolved
        assert resolved.resolution == ConflictResolutionMethod.CONTEXT_DISTINCTION

    def test_resolve_with_origin(self):
        rec = detect_conflict("U1", ("a", "b"))
        resolved = resolve_conflict(rec, {"origin": "origin wins"})
        assert resolved.resolved
        assert resolved.resolution == ConflictResolutionMethod.ORIGIN_VS_FOLLOWER

    def test_resolve_with_figurative(self):
        rec = detect_conflict("U1", ("a", "b"))
        resolved = resolve_conflict(rec, {"figurative": "reduced"})
        assert resolved.resolved
        assert resolved.resolution == ConflictResolutionMethod.REDUCE_TO_FIGURATIVE

    def test_resolve_hierarchy_prefers_rank(self):
        rec = detect_conflict("U1", ("a", "b"))
        resolved = resolve_conflict(
            rec, {"rank": "rank", "figurative": "fig"},
        )
        assert resolved.resolution == ConflictResolutionMethod.RANK_DISTINCTION

    def test_resolve_no_cues_stays_blocked(self):
        rec = detect_conflict("U1", ("a", "b"))
        resolved = resolve_conflict(rec)
        assert not resolved.resolved
        assert resolved.resolution == ConflictResolutionMethod.BLOCK_COMPOSITION

    def test_resolve_already_resolved_no_change(self):
        rec = detect_conflict("U1", ("a", "b"))
        resolved = resolve_conflict(rec, {"rank": "r"})
        again = resolve_conflict(resolved, {"figurative": "f"})
        assert again.resolution == ConflictResolutionMethod.RANK_DISTINCTION


# =====================================================================
# 5. Transfer tests
# =====================================================================


class TestTransfer:
    """Tests for detect_transfer and validate_transfer."""

    def test_no_transfer_same_direction(self):
        rec = detect_transfer("U1", "meaning_a", "meaning_a")
        assert rec.accepted
        assert rec.stability == 1.0

    def test_transfer_detected(self):
        rec = detect_transfer("U1", "original", "transferred")
        assert not rec.accepted
        assert rec.stability == 0.0

    def test_transfer_custom_type(self):
        rec = detect_transfer(
            "U1", "a", "b",
            transfer_type=TransferType.CONVENTIONAL_SHIFT,
        )
        assert rec.transfer_type == TransferType.CONVENTIONAL_SHIFT

    def test_validate_already_accepted(self):
        rec = detect_transfer("U1", "a", "a")
        validated = validate_transfer(rec)
        assert validated.accepted
        assert validated.stability == 1.0

    def test_validate_unaccepted_with_both_directions(self):
        rec = detect_transfer("U1", "original", "transferred")
        validated = validate_transfer(rec)
        # 3 of 4 conditions met (both directions + relation, but stability < 0.5)
        assert validated.stability == 0.75
        assert not validated.accepted

    def test_validate_missing_original(self):
        rec = TransferRecord(
            unit_id="U1",
            transfer_type=TransferType.INTERNAL_LINGUISTIC,
            original_direction="",
            transferred_direction="new",
            stability=0.0,
            accepted=False,
        )
        validated = validate_transfer(rec)
        assert validated.stability == 0.25
        assert not validated.accepted

    def test_validate_empty_both(self):
        rec = TransferRecord(
            unit_id="U1",
            transfer_type=TransferType.INTERNAL_LINGUISTIC,
            original_direction="",
            transferred_direction="",
            stability=0.0,
            accepted=False,
        )
        validated = validate_transfer(rec)
        assert validated.stability == 0.0
        assert not validated.accepted


# =====================================================================
# 6. Truth type tests
# =====================================================================


class TestTruthType:
    """Tests for determine_truth_type and adjudicate_truth."""

    def test_default_linguistic_original(self):
        rec = determine_truth_type("U1")
        assert rec.truth_type == TruthType.LINGUISTIC_ORIGINAL
        assert rec.confidence == 0.9

    def test_conventional_usage(self):
        rec = determine_truth_type("U1", {"usage": "conventional"})
        assert rec.truth_type == TruthType.CONVENTIONAL
        assert rec.confidence == 0.8

    def test_transferred_usage(self):
        rec = determine_truth_type("U1", {"usage": "transferred"})
        assert rec.truth_type == TruthType.CONTROLLED_TRANSFER
        assert rec.confidence == 0.7

    def test_adjudicate_no_conventional(self):
        ling = determine_truth_type("U1")
        result = adjudicate_truth(ling)
        assert result.truth_type == TruthType.LINGUISTIC_ORIGINAL

    def test_adjudicate_linguistic_wins_when_equal_confidence(self):
        ling = determine_truth_type("U1")
        conv = determine_truth_type("U1", {"usage": "conventional"})
        result = adjudicate_truth(ling, conv)
        assert result.truth_type == TruthType.LINGUISTIC_ORIGINAL

    def test_adjudicate_conventional_wins_when_higher_confidence(self):
        ling = TruthRecord(
            unit_id="U1",
            truth_type=TruthType.LINGUISTIC_ORIGINAL,
            justification="",
            confidence=0.5,
        )
        conv = TruthRecord(
            unit_id="U1",
            truth_type=TruthType.CONVENTIONAL,
            justification="",
            confidence=0.9,
        )
        result = adjudicate_truth(ling, conv)
        assert result.truth_type == TruthType.CONVENTIONAL


# =====================================================================
# 7. Admission tests
# =====================================================================


class TestAdmission:
    """Tests for check_admission and individual gates."""

    def test_clean_unit_admitted(self):
        unit = check_admission("U1", "كتاب")
        assert unit.admitted
        assert unit.unit_id == "U1"
        assert unit.label == "كتاب"

    def test_unit_with_unresolved_ambiguity_rejected(self):
        dis = detect_ambiguity("U1", "عين", ("eye", "spring"))
        unit = check_admission("U1", "عين", disambiguation=dis)
        assert not unit.admitted

    def test_unit_with_resolved_ambiguity_admitted(self):
        dis = detect_ambiguity("U1", "عين", ("eye", "spring"))
        dis = resolve_ambiguity(dis, {"semantic": "eye"})
        unit = check_admission("U1", "عين", disambiguation=dis)
        assert unit.admitted

    def test_unit_with_unresolved_conflict_rejected(self):
        conflict = detect_conflict("U1", ("a", "b"))
        unit = check_admission("U1", "x", conflict=conflict)
        assert not unit.admitted

    def test_unit_with_resolved_conflict_admitted(self):
        conflict = detect_conflict("U1", ("a", "b"))
        conflict = resolve_conflict(conflict, {"rank": "ok"})
        unit = check_admission("U1", "x", conflict=conflict)
        assert unit.admitted

    def test_unit_with_unaccepted_transfer_rejected(self):
        transfer = detect_transfer("U1", "a", "b")
        unit = check_admission("U1", "x", transfer=transfer)
        assert not unit.admitted

    def test_unit_with_accepted_transfer_admitted(self):
        transfer = detect_transfer("U1", "a", "a")
        unit = check_admission("U1", "x", transfer=transfer)
        assert unit.admitted

    def test_custom_pos_and_semantic_type(self):
        unit = check_admission(
            "U1", "ذهب",
            semantic_type=SemanticType.EVENT,
            pos=POS.FI3L,
        )
        assert unit.admitted
        assert unit.pos == POS.FI3L
        assert unit.semantic_type == SemanticType.EVENT

    def test_truth_record_preserved(self):
        truth = determine_truth_type("U1")
        unit = check_admission("U1", "x", truth=truth)
        assert unit.truth is not None
        assert unit.truth.truth_type == TruthType.LINGUISTIC_ORIGINAL


# =====================================================================
# 8. Predication tests
# =====================================================================


class TestPredication:
    """Tests for build_predication and classify_predication."""

    def test_build_valid_predication(self):
        subj, pred = _two_admitted_units()
        rec = build_predication(subj, pred)
        assert rec.valid
        assert rec.musnad_ilayh_id == "U1"
        assert rec.musnad_id == "U2"
        assert rec.confidence == 0.9

    def test_build_invalid_when_not_admitted(self):
        subj = _admitted_unit()
        pred = CompositionUnit(
            unit_id="U2", label="x", admitted=False,
        )
        rec = build_predication(subj, pred)
        assert not rec.valid
        assert rec.confidence == 0.0

    def test_classify_eventive(self):
        subj = _admitted_unit("U1", pos=POS.ISM)
        pred = _verbal_unit("U2")
        rec = build_predication(subj, pred)
        assert classify_predication(rec) == "essential/eventive"

    def test_classify_descriptive(self):
        subj = _admitted_unit("U1", pos=POS.ISM)
        pred = _admitted_unit("U2", pos=POS.SIFA)
        rec = build_predication(subj, pred)
        assert classify_predication(rec) == "essential/descriptive"

    def test_classify_existential(self):
        subj = _admitted_unit("U1", pos=POS.ISM)
        pred = _admitted_unit("U2", pos=POS.ISM)
        rec = build_predication(subj, pred)
        assert classify_predication(rec) == "essential/existential"


# =====================================================================
# 9. Restriction tests
# =====================================================================


class TestRestriction:
    """Tests for build_restriction and validate_restriction."""

    def test_build_valid_restriction(self):
        base = _admitted_unit("U1")
        qual = _admitted_unit("U2", "جميل")
        rec = build_restriction(base, qual)
        assert rec.valid
        assert validate_restriction(rec)

    def test_build_restriction_unknown_kind(self):
        base = _admitted_unit("U1")
        qual = _admitted_unit("U2")
        rec = build_restriction(base, qual, restriction_kind="unknown")
        assert not rec.valid
        assert not validate_restriction(rec)

    def test_build_restriction_not_admitted(self):
        base = _admitted_unit("U1")
        qual = CompositionUnit(unit_id="U2", label="x", admitted=False)
        rec = build_restriction(base, qual)
        assert not rec.valid

    @pytest.mark.parametrize(
        "kind",
        ["description", "adverb", "hal", "tamyiz", "idafa", "number"],
    )
    def test_all_restriction_kinds(self, kind):
        base = _admitted_unit("U1")
        qual = _admitted_unit("U2")
        rec = build_restriction(base, qual, restriction_kind=kind)
        assert rec.valid
        assert validate_restriction(rec)


# =====================================================================
# 10. Dependency tests
# =====================================================================


class TestDependency:
    """Tests for build_dependency and validate_dependency."""

    def test_build_valid_dependency(self):
        principal = _admitted_unit("U1")
        follower = _admitted_unit("U2")
        rec = build_dependency(principal, follower, "na3t")
        assert rec.valid
        assert validate_dependency(rec)

    def test_build_dependency_unknown_kind(self):
        principal = _admitted_unit("U1")
        follower = _admitted_unit("U2")
        rec = build_dependency(principal, follower, "unknown")
        assert not rec.valid
        assert not validate_dependency(rec)

    def test_build_dependency_not_admitted(self):
        principal = _admitted_unit("U1")
        follower = CompositionUnit(unit_id="U2", label="x", admitted=False)
        rec = build_dependency(principal, follower, "na3t")
        assert not rec.valid

    @pytest.mark.parametrize("kind", ["na3t", "badal", "tawkid", "3atf"])
    def test_all_dependency_kinds(self, kind):
        principal = _admitted_unit("U1")
        follower = _admitted_unit("U2")
        rec = build_dependency(principal, follower, kind)
        assert rec.valid

    def test_dependency_face_preserved(self):
        principal = _admitted_unit("U1")
        follower = _admitted_unit("U2")
        rec = build_dependency(
            principal, follower, "badal", dependency_face="inclusive",
        )
        assert rec.dependency_face == "inclusive"


# =====================================================================
# 11. Relations tests
# =====================================================================


class TestRelations:
    """Tests for build_relation and classify_relation."""

    def test_build_relation_admitted(self):
        src = _admitted_unit("U1")
        tgt = _admitted_unit("U2")
        rel = build_relation(src, tgt, CompositionRelationType.PREDICATION)
        assert rel.relation_id.startswith("R_")
        assert rel.source_id == "U1"
        assert rel.target_id == "U2"
        assert rel.confidence == 0.9

    def test_build_relation_not_admitted(self):
        src = _admitted_unit("U1")
        tgt = CompositionUnit(unit_id="U2", label="x", admitted=False)
        rel = build_relation(src, tgt, CompositionRelationType.PREDICATION)
        assert rel.confidence == 0.3

    def test_classify_verb_noun_predication(self):
        src = _verbal_unit("U1")
        tgt = _admitted_unit("U2", pos=POS.ISM)
        assert classify_relation(src, tgt) == CompositionRelationType.PREDICATION

    def test_classify_noun_noun_restriction(self):
        src = _admitted_unit("U1", pos=POS.ISM)
        tgt = _admitted_unit("U2", pos=POS.ISM)
        assert classify_relation(src, tgt) == CompositionRelationType.RESTRICTION

    def test_classify_harf_linking(self):
        src = check_admission("U1", "في", pos=POS.HARF)
        tgt = _admitted_unit("U2", pos=POS.ISM)
        assert classify_relation(src, tgt) == CompositionRelationType.LINKING

    def test_classify_sifa_dependency(self):
        src = _verbal_unit("U1")
        tgt = _admitted_unit("U2", pos=POS.SIFA)
        assert classify_relation(src, tgt) == CompositionRelationType.DEPENDENCY

    def test_sub_type_preserved(self):
        src = _admitted_unit("U1")
        tgt = _admitted_unit("U2")
        rel = build_relation(
            src, tgt, CompositionRelationType.EXPLANATION, sub_type="detail",
        )
        assert rel.sub_type == "detail"


# =====================================================================
# 12. Roles tests
# =====================================================================


class TestRoles:
    """Tests for assign_role and realize_role."""

    def test_assign_default_role(self):
        unit = _admitted_unit("U1", pos=POS.ISM)
        role = assign_role(unit)
        assert role.unit_id == "U1"
        assert role.status == RoleStatus.CANDIDATE
        assert role.confidence == 0.8

    def test_assign_role_not_admitted(self):
        unit = CompositionUnit(unit_id="U1", label="x", admitted=False)
        role = assign_role(unit)
        assert role.confidence == 0.3

    def test_assign_subject_role(self):
        unit = _admitted_unit("U1", pos=POS.ISM)
        role = assign_role(unit, {"position": "subject"})
        assert role.role_type == CompositionRoleType.MUSNAD_ILAYH

    def test_assign_predicate_role(self):
        unit = _verbal_unit("U1")
        role = assign_role(unit, {"position": "predicate"})
        assert role.role_type == CompositionRoleType.MUSNAD

    def test_assign_verb_role(self):
        unit = _verbal_unit("U1")
        role = assign_role(unit)
        assert role.role_type == CompositionRoleType.MUSNAD

    def test_assign_sifa_role(self):
        unit = _admitted_unit("U1", pos=POS.SIFA)
        role = assign_role(unit, {"position": "predicate"})
        assert role.role_type == CompositionRoleType.MUSNAD

    def test_assign_harf_role(self):
        unit = check_admission("U1", "في", pos=POS.HARF)
        role = assign_role(unit)
        assert role.role_type == CompositionRoleType.RABIT

    def test_assign_zarf_role(self):
        unit = check_admission("U1", "أمام", pos=POS.ZARF)
        role = assign_role(unit)
        assert role.role_type == CompositionRoleType.QAYD

    def test_realize_candidate(self):
        unit = _admitted_unit("U1")
        role = assign_role(unit)
        assert role.status == RoleStatus.CANDIDATE
        realized = realize_role(role)
        assert realized.status == RoleStatus.REALIZED
        assert realized.confidence == min(1.0, role.confidence + 0.1)

    def test_realize_already_realized(self):
        unit = _admitted_unit("U1")
        role = realize_role(assign_role(unit))
        again = realize_role(role)
        assert again.status == RoleStatus.REALIZED
        assert again.confidence == role.confidence  # No double-bump


# =====================================================================
# 13. Proposition tests
# =====================================================================


class TestProposition:
    """Tests for build/close/classify_proposition."""

    def test_build_proposition(self):
        subj, pred = _two_admitted_units()
        predication = build_predication(subj, pred)
        role1 = realize_role(assign_role(subj, {"position": "subject"}))
        role2 = realize_role(assign_role(pred, {"position": "predicate"}))
        prop = build_proposition(predication, roles=(role1, role2))
        assert prop.proposition_id.startswith("P_")
        assert not prop.closed
        assert prop.proposition_type == PropositionType.VERBAL

    def test_close_proposition_valid(self):
        subj, pred = _two_admitted_units()
        predication = build_predication(subj, pred)
        role1 = realize_role(assign_role(subj, {"position": "subject"}))
        role2 = realize_role(assign_role(pred, {"position": "predicate"}))
        prop = build_proposition(predication, roles=(role1, role2))
        closed = close_proposition(prop)
        assert closed.closed

    def test_close_proposition_no_realized_roles(self):
        subj, pred = _two_admitted_units()
        predication = build_predication(subj, pred)
        role1 = assign_role(subj)  # CANDIDATE only
        prop = build_proposition(predication, roles=(role1,))
        closed = close_proposition(prop)
        assert not closed.closed

    def test_close_proposition_invalid_predication(self):
        subj = _admitted_unit()
        pred = CompositionUnit(unit_id="U2", label="x", admitted=False)
        predication = build_predication(subj, pred)
        prop = build_proposition(predication)
        closed = close_proposition(prop)
        assert not closed.closed

    def test_classify_verbal(self):
        subj = _admitted_unit("U1", pos=POS.ISM)
        pred = _verbal_unit("U2")
        predication = build_predication(subj, pred)
        prop = build_proposition(predication)
        assert classify_proposition(prop) == PropositionType.VERBAL

    def test_classify_nominal(self):
        subj = _admitted_unit("U1", pos=POS.ISM)
        pred = _admitted_unit("U2", pos=POS.ISM)
        predication = build_predication(subj, pred)
        prop = build_proposition(predication)
        assert classify_proposition(prop) == PropositionType.NOMINAL


# =====================================================================
# 14. Inter-proposition tests
# =====================================================================


class TestInterProposition:
    """Tests for link_propositions and validate_link."""

    def _make_closed_prop(self, prop_id: str = "P_a") -> CompositionProposition:
        subj, pred = _two_admitted_units()
        predication = build_predication(subj, pred)
        role1 = realize_role(assign_role(subj, {"position": "subject"}))
        role2 = realize_role(assign_role(pred, {"position": "predicate"}))
        prop = build_proposition(predication, roles=(role1, role2))
        return close_proposition(prop)

    def test_link_closed_propositions(self):
        p1 = self._make_closed_prop()
        p2 = self._make_closed_prop()
        link = link_propositions(p1, p2, "و")
        assert link.valid
        assert link.link_type == InterPropositionLinkType.CONJUNCTION
        assert link.particle == "و"

    def test_link_open_propositions_invalid(self):
        subj, pred = _two_admitted_units()
        predication = build_predication(subj, pred)
        p1 = build_proposition(predication)  # Not closed
        p2 = build_proposition(predication)
        link = link_propositions(p1, p2, "و")
        assert not link.valid

    def test_validate_valid_link(self):
        p1 = self._make_closed_prop()
        p2 = self._make_closed_prop()
        link = link_propositions(p1, p2, "و")
        assert validate_link(link)

    def test_validate_empty_particle(self):
        link = InterPropositionLink(
            source_prop_id="P1",
            target_prop_id="P2",
            link_type=InterPropositionLinkType.CONJUNCTION,
            particle="",
            valid=True,
        )
        assert not validate_link(link)

    @pytest.mark.parametrize(
        "particle,expected_type",
        [
            ("و", InterPropositionLinkType.CONJUNCTION),
            ("ف", InterPropositionLinkType.CONJUNCTION),
            ("ثم", InterPropositionLinkType.TEMPORAL),
            ("إذا", InterPropositionLinkType.CONDITION),
            ("إن", InterPropositionLinkType.CONDITION),
            ("لو", InterPropositionLinkType.CONDITION),
            ("لأن", InterPropositionLinkType.CAUSATION),
            ("بسبب", InterPropositionLinkType.CAUSATION),
            ("لكن", InterPropositionLinkType.ADVERSATIVE),
            ("بل", InterPropositionLinkType.ADVERSATIVE),
            ("قبل", InterPropositionLinkType.TEMPORAL),
            ("بعد", InterPropositionLinkType.TEMPORAL),
        ],
    )
    def test_particle_map(self, particle, expected_type):
        p1 = self._make_closed_prop()
        p2 = self._make_closed_prop()
        link = link_propositions(p1, p2, particle)
        assert link.link_type == expected_type

    def test_unknown_particle_maps_to_other(self):
        p1 = self._make_closed_prop()
        p2 = self._make_closed_prop()
        link = link_propositions(p1, p2, "xyz")
        assert link.link_type == InterPropositionLinkType.OTHER


# =====================================================================
# 15. Gates tests
# =====================================================================


class TestGates:
    """Tests for all 8 composition gates."""

    def test_gate_disambiguation_passed(self):
        units = (_admitted_unit(),)
        results = run_all_gates(units, (), (), (), None, ())
        gate = results[0]
        assert gate.gate == CompositionGate.DISAMBIGUATION
        assert gate.status == CompositionGateStatus.PASSED

    def test_gate_disambiguation_blocked(self):
        dis = detect_ambiguity("U1", "عين", ("eye", "spring"))
        unit = CompositionUnit(
            unit_id="U1", label="عين", disambiguation=dis, admitted=False,
        )
        results = run_all_gates((unit,), (), (), (), None, ())
        gate = results[0]
        assert gate.status == CompositionGateStatus.BLOCKED

    def test_gate_reference_stability_passed(self):
        units = (_admitted_unit(),)
        results = run_all_gates(units, (), (), (), None, ())
        gate = results[1]
        assert gate.gate == CompositionGate.REFERENCE_STABILITY
        assert gate.status == CompositionGateStatus.PASSED

    def test_gate_reference_stability_blocked(self):
        transfer = detect_transfer("U1", "a", "b")  # unaccepted
        unit = CompositionUnit(
            unit_id="U1", label="x", transfer=transfer, admitted=False,
        )
        results = run_all_gates((unit,), (), (), (), None, ())
        gate = results[1]
        assert gate.status == CompositionGateStatus.BLOCKED

    def test_gate_predicate_readiness_passed(self):
        units = (_admitted_unit(),)
        results = run_all_gates(units, (), (), (), None, ())
        gate = results[2]
        assert gate.gate == CompositionGate.PREDICATE_READINESS
        assert gate.status == CompositionGateStatus.PASSED

    def test_gate_predicate_readiness_blocked(self):
        conflict = detect_conflict("U1", ("a", "b"))
        unit = CompositionUnit(
            unit_id="U1", label="x", conflict=conflict, admitted=False,
        )
        results = run_all_gates((unit,), (), (), (), None, ())
        gate = results[2]
        assert gate.status == CompositionGateStatus.BLOCKED

    def test_gate_role_assignment_no_roles(self):
        results = run_all_gates((), (), (), (), None, ())
        gate = results[3]
        assert gate.gate == CompositionGate.ROLE_ASSIGNMENT
        assert gate.status == CompositionGateStatus.INSUFFICIENT_DATA

    def test_gate_role_assignment_candidate_only(self):
        unit = _admitted_unit()
        role = assign_role(unit)
        results = run_all_gates((), (role,), (), (), None, ())
        gate = results[3]
        assert gate.status == CompositionGateStatus.BLOCKED

    def test_gate_role_assignment_realized(self):
        unit = _admitted_unit()
        role = realize_role(assign_role(unit))
        results = run_all_gates((), (role,), (), (), None, ())
        gate = results[3]
        assert gate.status == CompositionGateStatus.PASSED

    def test_gate_relation_validity_no_relations(self):
        results = run_all_gates((), (), (), (), None, ())
        gate = results[4]
        assert gate.gate == CompositionGate.RELATION_VALIDITY
        assert gate.status == CompositionGateStatus.PASSED

    def test_gate_relation_validity_valid(self):
        src, tgt = _two_admitted_units()
        rel = build_relation(src, tgt, CompositionRelationType.PREDICATION)
        results = run_all_gates((), (), (rel,), (), None, ())
        gate = results[4]
        assert gate.status == CompositionGateStatus.PASSED

    def test_gate_conflict_resolution_no_conflicts(self):
        results = run_all_gates((), (), (), (), None, ())
        gate = results[5]
        assert gate.gate == CompositionGate.CONFLICT_RESOLUTION
        assert gate.status == CompositionGateStatus.PASSED

    def test_gate_conflict_resolution_unresolved(self):
        conflict = detect_conflict("U1", ("a", "b"))
        results = run_all_gates((), (), (), (conflict,), None, ())
        gate = results[5]
        assert gate.status == CompositionGateStatus.BLOCKED

    def test_gate_conflict_resolution_resolved(self):
        conflict = detect_conflict("U1", ("a", "b"))
        conflict = resolve_conflict(conflict, {"rank": "ok"})
        results = run_all_gates((), (), (), (conflict,), None, ())
        gate = results[5]
        assert gate.status == CompositionGateStatus.PASSED

    def test_gate_proposition_closure_none(self):
        results = run_all_gates((), (), (), (), None, ())
        gate = results[6]
        assert gate.gate == CompositionGate.PROPOSITION_CLOSURE
        assert gate.status == CompositionGateStatus.INSUFFICIENT_DATA

    def test_gate_proposition_closure_open(self):
        subj, pred = _two_admitted_units()
        predication = build_predication(subj, pred)
        prop = build_proposition(predication)
        results = run_all_gates((), (), (), (), prop, ())
        gate = results[6]
        assert gate.status == CompositionGateStatus.BLOCKED

    def test_gate_proposition_closure_closed(self):
        subj, pred = _two_admitted_units()
        predication = build_predication(subj, pred)
        r1 = realize_role(assign_role(subj, {"position": "subject"}))
        r2 = realize_role(assign_role(pred, {"position": "predicate"}))
        prop = close_proposition(build_proposition(predication, roles=(r1, r2)))
        results = run_all_gates((), (), (), (), prop, ())
        gate = results[6]
        assert gate.status == CompositionGateStatus.PASSED

    def test_gate_inter_proposition_no_links(self):
        results = run_all_gates((), (), (), (), None, ())
        gate = results[7]
        assert gate.gate == CompositionGate.INTER_PROPOSITION_LINK
        assert gate.status == CompositionGateStatus.PASSED

    def test_all_gates_count(self):
        results = run_all_gates((), (), (), (), None, ())
        assert len(results) == 8


# =====================================================================
# 16. Composition orchestrator tests
# =====================================================================


class TestComposition:
    """Tests for compose, compute_readiness, validate, decompose."""

    def test_compose_no_admitted_units(self):
        unit = CompositionUnit(unit_id="U1", label="x", admitted=False)
        result = compose((unit,))
        assert not result.valid
        assert result.readiness == 0.0

    def test_compose_empty_units(self):
        result = compose(())
        assert not result.valid
        assert result.readiness == 0.0

    def test_compose_single_admitted_unit(self):
        unit = _admitted_unit("U1")
        result = compose((unit,))
        # Single unit can't form predication, but may still be partially ready
        assert result.units == (unit,)
        assert isinstance(result.readiness, float)

    def test_compose_two_admitted_units(self):
        subj = _admitted_unit("U1", "الطالب", pos=POS.ISM)
        pred = _verbal_unit("U2", "ذهب")
        result = compose((subj, pred))
        assert result.valid
        assert result.readiness > 0.0
        assert len(result.roles) == 2
        assert len(result.relations) == 1
        assert len(result.propositions) == 1
        assert result.propositions[0].closed
        assert len(result.gates) == 8

    def test_compose_three_units(self):
        u1 = _admitted_unit("U1", "الطالب", pos=POS.ISM)
        u2 = _verbal_unit("U2", "ذهب")
        u3 = _admitted_unit("U3", "المدرسة", pos=POS.ISM)
        result = compose((u1, u2, u3))
        assert len(result.roles) == 3
        assert len(result.relations) == 2
        assert result.valid

    def test_compose_mixed_admitted_rejected(self):
        u1 = _admitted_unit("U1")
        u2 = CompositionUnit(unit_id="U2", label="x", admitted=False)
        result = compose((u1, u2))
        # Only one admitted unit → no predication
        assert len(result.units) == 2

    def test_compute_readiness(self):
        subj = _admitted_unit("U1", pos=POS.ISM)
        pred = _verbal_unit("U2")
        result = compose((subj, pred))
        readiness = compute_readiness(result)
        assert readiness == result.readiness

    def test_validate_composition_above_threshold(self):
        subj = _admitted_unit("U1", pos=POS.ISM)
        pred = _verbal_unit("U2")
        result = compose((subj, pred))
        assert validate_composition(result)

    def test_validate_composition_below_threshold(self):
        unit = CompositionUnit(unit_id="U1", label="x", admitted=False)
        result = compose((unit,))
        assert not validate_composition(result)

    def test_validate_composition_custom_threshold(self):
        subj = _admitted_unit("U1", pos=POS.ISM)
        pred = _verbal_unit("U2")
        result = compose((subj, pred))
        # Very high threshold should fail
        assert not validate_composition(result, threshold=1.0)

    def test_decompose(self):
        subj = _admitted_unit("U1")
        pred = _verbal_unit("U2")
        result = compose((subj, pred))
        units = decompose(result)
        assert len(units) == 2
        assert units[0].unit_id == "U1"
        assert units[1].unit_id == "U2"

    def test_compose_structure_is_frozen(self):
        subj = _admitted_unit("U1")
        pred = _verbal_unit("U2")
        result = compose((subj, pred))
        with pytest.raises(AttributeError):
            result.readiness = 999.0  # type: ignore[misc]


# =====================================================================
# 17. Re-export tests
# =====================================================================


class TestReExports:
    """Composition types and enums must be importable from arabic_engine.core."""

    @pytest.mark.parametrize(
        "name",
        [
            "AmbiguityResolution",
            "AmbiguityType",
            "CompositionGate",
            "CompositionGateStatus",
            "CompositionRelationType",
            "CompositionRoleType",
            "ConflictResolutionMethod",
            "ConflictType",
            "InterPropositionLinkType",
            "PropositionType",
            "RoleStatus",
            "TransferType",
            "TruthType",
        ],
    )
    def test_enum_reexported(self, name):
        import arabic_engine.core as core

        assert hasattr(core, name), f"{name} not in core"

    @pytest.mark.parametrize(
        "name",
        [
            "CompositionGateResult",
            "CompositionProposition",
            "CompositionRelation",
            "CompositionRole",
            "CompositionStructure",
            "CompositionUnit",
            "DependencyRecord",
            "DisambiguationRecord",
            "InterPropositionLink",
            "PredicationRecord",
            "RestrictionRecord",
            "SemanticConflictRecord",
            "TransferRecord",
            "TruthRecord",
        ],
    )
    def test_type_reexported(self, name):
        import arabic_engine.core as core

        assert hasattr(core, name), f"{name} not in core"


# =====================================================================
# 18. Package-level import tests
# =====================================================================


class TestPackageImports:
    """All public functions must be importable from arabic_engine.composition."""

    @pytest.mark.parametrize(
        "name",
        [
            "compose",
            "compute_readiness",
            "validate_composition",
            "decompose",
            "detect_ambiguity",
            "resolve_ambiguity",
            "detect_conflict",
            "resolve_conflict",
            "detect_transfer",
            "validate_transfer",
            "determine_truth_type",
            "adjudicate_truth",
            "check_admission",
            "build_predication",
            "classify_predication",
            "build_restriction",
            "validate_restriction",
            "build_dependency",
            "validate_dependency",
            "build_relation",
            "classify_relation",
            "assign_role",
            "realize_role",
            "build_proposition",
            "close_proposition",
            "classify_proposition",
            "link_propositions",
            "validate_link",
            "run_all_gates",
        ],
    )
    def test_function_importable(self, name):
        import arabic_engine.composition as comp

        assert hasattr(comp, name), f"{name} not in composition"
        assert name in comp.__all__
