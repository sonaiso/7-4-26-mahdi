"""Tests for Composition / Syntax Constitution v1.

Covers:
- Enum completeness (all 16 new enums)
- Disambiguation layer (ambiguity, conflict, transfer, truth)
- Structural composition (predication, restriction, dependency)
- Roles
- Propositions
- Gates (all 8)
- Readiness
- End-to-end composition (accepted / rejected / pending)
- Batch composition
- Fractal law cycle
"""

from __future__ import annotations

from arabic_engine.core.enums import (
    AmbiguityResolution,
    AmbiguityType,
    CompositionGate,
    CompositionRelation,
    CompositionRole,
    CompositionVerdict,
    ConflictResolutionMethod,
    ConflictType,
    DependencyType,
    InterPropositionLink,
    PredicationType,
    PropositionType,
    RestrictionType,
    RoleStatus,
    TransferType,
    TruthCategory,
)
from arabic_engine.core.types import (
    AmbiguityRecord,
    CompositionRecord,
    CompositionRoleRecord,
    DependencyRecord,
    DisambiguationResult,
    GateResult,
    PredicationRecord,
    PropositionRecord,
)
from arabic_engine.syntax.composition_v1 import (
    assign_role,
    assign_truth_category,
    batch_compose,
    build_composition,
    build_dependency,
    build_predication,
    build_proposition,
    build_restriction,
    check_gate,
    classify_transfer,
    compute_readiness,
    disambiguate,
    resolve_ambiguity,
    resolve_conflict,
)

# ── Test helpers ────────────────────────────────────────────────────


def _predication(
    subj: str = "زيد",
    pred: str = "قائم",
    ptype: PredicationType = PredicationType.ESSENTIAL_DESCRIPTIVE,
) -> PredicationRecord:
    return build_predication(subj, pred, ptype)


def _roles_realized(
    unit_a: str = "زيد",
    unit_b: str = "قائم",
) -> tuple[CompositionRoleRecord, ...]:
    return (
        assign_role(unit_a, CompositionRole.MUSNAD_ILAYH, realized=True),
        assign_role(unit_b, CompositionRole.MUSNAD, realized=True),
    )


def _proposition(
    *,
    closed: bool = True,
    ptype: PropositionType = PropositionType.NOMINAL,
) -> PropositionRecord:
    pred = _predication()
    roles = _roles_realized() if closed else ()
    return build_proposition(pred, (), (), roles, ptype)


def _disambiguation_ok() -> DisambiguationResult:
    return DisambiguationResult(all_resolved=True)


def _disambiguation_with_records(
    units: list[str],
) -> DisambiguationResult:
    ambs = [
        resolve_ambiguity(u, AmbiguityType.LEXICAL_PURE, AmbiguityResolution.SEMANTIC_CLUE)
        for u in units
    ]
    truths = [
        assign_truth_category(u, TruthCategory.LINGUISTIC_TRUTH) for u in units
    ]
    return disambiguate(units, ambiguities=ambs, truth_assignments=truths)


# ═════════════════════════════════════════════════════════════════════
# 1. Enum completeness
# ═════════════════════════════════════════════════════════════════════


class TestEnumCompleteness:
    """Verify member counts and names for all composition enums."""

    def test_ambiguity_type_count(self) -> None:
        assert len(AmbiguityType) == 4

    def test_ambiguity_type_members(self) -> None:
        names = {m.name for m in AmbiguityType}
        assert names == {
            "LEXICAL_PURE",
            "SEMANTIC_DUAL_BEARING",
            "TRUTH_VS_TRANSFER",
            "LINGUISTIC_VS_CONVENTIONAL",
        }

    def test_ambiguity_resolution_count(self) -> None:
        assert len(AmbiguityResolution) == 6

    def test_ambiguity_resolution_members(self) -> None:
        names = {m.name for m in AmbiguityResolution}
        assert "SEMANTIC_CLUE" in names
        assert "OPEN_PENDING" in names

    def test_conflict_type_count(self) -> None:
        assert len(ConflictType) == 5

    def test_conflict_resolution_method_count(self) -> None:
        assert len(ConflictResolutionMethod) == 5

    def test_transfer_type_count(self) -> None:
        assert len(TransferType) == 6

    def test_truth_category_count(self) -> None:
        assert len(TruthCategory) == 3

    def test_predication_type_count(self) -> None:
        assert len(PredicationType) == 3

    def test_restriction_type_count(self) -> None:
        assert len(RestrictionType) == 6

    def test_dependency_type_count(self) -> None:
        assert len(DependencyType) == 4

    def test_composition_relation_count(self) -> None:
        assert len(CompositionRelation) == 6

    def test_composition_role_count(self) -> None:
        assert len(CompositionRole) == 6

    def test_role_status_count(self) -> None:
        assert len(RoleStatus) == 2

    def test_proposition_type_count(self) -> None:
        assert len(PropositionType) == 4

    def test_inter_proposition_link_count(self) -> None:
        assert len(InterPropositionLink) == 6

    def test_composition_gate_count(self) -> None:
        assert len(CompositionGate) == 8

    def test_composition_verdict_count(self) -> None:
        assert len(CompositionVerdict) == 3


# ═════════════════════════════════════════════════════════════════════
# 2. Resolve ambiguity
# ═════════════════════════════════════════════════════════════════════


class TestResolveAmbiguity:
    """Art. 6-9: ambiguity resolution."""

    def test_lexical_pure_resolved(self) -> None:
        rec = resolve_ambiguity("U1", AmbiguityType.LEXICAL_PURE, AmbiguityResolution.SEMANTIC_CLUE)
        assert isinstance(rec, AmbiguityRecord)
        assert rec.resolved is True
        assert rec.ambiguity_type == AmbiguityType.LEXICAL_PURE
        assert rec.resolution == AmbiguityResolution.SEMANTIC_CLUE

    def test_semantic_dual_bearing(self) -> None:
        rec = resolve_ambiguity(
            "U2", AmbiguityType.SEMANTIC_DUAL_BEARING,
            AmbiguityResolution.REFERENTIAL_CLUE,
        )
        assert rec.resolved is True

    def test_truth_vs_transfer(self) -> None:
        rec = resolve_ambiguity(
            "U3", AmbiguityType.TRUTH_VS_TRANSFER,
            AmbiguityResolution.SYNTACTIC_CLUE,
        )
        assert rec.resolved is True

    def test_linguistic_vs_conventional(self) -> None:
        rec = resolve_ambiguity(
            "U4", AmbiguityType.LINGUISTIC_VS_CONVENTIONAL,
            AmbiguityResolution.WEIGHT_PRIORITY,
        )
        assert rec.resolved is True

    def test_conventional_priority(self) -> None:
        rec = resolve_ambiguity(
            "U5", AmbiguityType.LEXICAL_PURE,
            AmbiguityResolution.CONVENTIONAL_PRIORITY,
        )
        assert rec.resolved is True

    def test_open_pending_is_unresolved(self) -> None:
        rec = resolve_ambiguity("U6", AmbiguityType.LEXICAL_PURE, AmbiguityResolution.OPEN_PENDING)
        assert rec.resolved is False

    def test_none_clue_is_unresolved(self) -> None:
        rec = resolve_ambiguity("U7", AmbiguityType.SEMANTIC_DUAL_BEARING, None)
        assert rec.resolved is False

    def test_id_prefix(self) -> None:
        rec = resolve_ambiguity("U8", AmbiguityType.LEXICAL_PURE, AmbiguityResolution.SEMANTIC_CLUE)
        assert rec.ambiguity_id.startswith("AMB_")

    def test_frozen(self) -> None:
        rec = resolve_ambiguity("U9", AmbiguityType.LEXICAL_PURE, AmbiguityResolution.SEMANTIC_CLUE)
        try:
            rec.resolved = True  # type: ignore[misc]
            assert False, "should be frozen"
        except AttributeError:
            pass


# ═════════════════════════════════════════════════════════════════════
# 3. Resolve conflict
# ═════════════════════════════════════════════════════════════════════


class TestResolveConflict:
    """Art. 10-13: conflict resolution."""

    def test_essential_vs_descriptive(self) -> None:
        rec = resolve_conflict(
            "U1", ConflictType.ESSENTIAL_VS_DESCRIPTIVE,
            ConflictResolutionMethod.RANK_DISTINCTION,
        )
        assert rec.resolved is True

    def test_universal_vs_particular(self) -> None:
        rec = resolve_conflict(
            "U2", ConflictType.UNIVERSAL_VS_PARTICULAR,
            ConflictResolutionMethod.CONTEXT_DISTINCTION,
        )
        assert rec.resolved is True

    def test_referential_vs_predicative(self) -> None:
        rec = resolve_conflict(
            "U3", ConflictType.REFERENTIAL_VS_PREDICATIVE,
            ConflictResolutionMethod.ORIGIN_VS_FOLLOWER,
        )
        assert rec.resolved is True

    def test_dual_role(self) -> None:
        rec = resolve_conflict(
            "U4", ConflictType.DUAL_ROLE,
            ConflictResolutionMethod.FIGURATIVE_RECLASSIFY,
        )
        assert rec.resolved is True

    def test_truth_vs_transfer(self) -> None:
        rec = resolve_conflict(
            "U5", ConflictType.TRUTH_VS_TRANSFER,
            ConflictResolutionMethod.RANK_DISTINCTION,
        )
        assert rec.resolved is True

    def test_block_transition_is_unresolved(self) -> None:
        rec = resolve_conflict(
            "U6", ConflictType.DUAL_ROLE,
            ConflictResolutionMethod.BLOCK_TRANSITION,
        )
        assert rec.resolved is False

    def test_none_method_is_unresolved(self) -> None:
        rec = resolve_conflict("U7", ConflictType.DUAL_ROLE, None)
        assert rec.resolved is False

    def test_id_prefix(self) -> None:
        rec = resolve_conflict(
            "U8", ConflictType.DUAL_ROLE,
            ConflictResolutionMethod.RANK_DISTINCTION,
        )
        assert rec.conflict_id.startswith("CNF_")


# ═════════════════════════════════════════════════════════════════════
# 4. Classify transfer
# ═════════════════════════════════════════════════════════════════════


class TestClassifyTransfer:
    """Art. 14-17: semantic transfer."""

    def test_internal_linguistic_stable(self) -> None:
        rec = classify_transfer("U1", TransferType.INTERNAL_LINGUISTIC, "أصل", "فرع", stable=True)
        assert rec.stable is True
        assert rec.transfer_type == TransferType.INTERNAL_LINGUISTIC

    def test_conventional(self) -> None:
        rec = classify_transfer("U2", TransferType.CONVENTIONAL, stable=True)
        assert rec.stable is True

    def test_terminological(self) -> None:
        rec = classify_transfer("U3", TransferType.TERMINOLOGICAL, stable=True)
        assert rec.stable is True

    def test_descriptive_to_referential(self) -> None:
        rec = classify_transfer("U4", TransferType.DESCRIPTIVE_TO_REFERENTIAL, stable=True)
        assert rec.stable is True

    def test_event_to_nominal(self) -> None:
        rec = classify_transfer("U5", TransferType.EVENT_TO_NOMINAL, stable=True)
        assert rec.stable is True

    def test_essential_to_relational(self) -> None:
        rec = classify_transfer("U6", TransferType.ESSENTIAL_TO_RELATIONAL, stable=True)
        assert rec.stable is True

    def test_unstable(self) -> None:
        rec = classify_transfer("U7", TransferType.CONVENTIONAL, stable=False)
        assert rec.stable is False

    def test_id_prefix(self) -> None:
        rec = classify_transfer("U8", TransferType.CONVENTIONAL, stable=True)
        assert rec.transfer_id.startswith("TRF_")


# ═════════════════════════════════════════════════════════════════════
# 5. Assign truth category
# ═════════════════════════════════════════════════════════════════════


class TestAssignTruthCategory:
    """Art. 18-22: truth category assignment."""

    def test_linguistic_truth(self) -> None:
        rec = assign_truth_category("U1", TruthCategory.LINGUISTIC_TRUTH)
        assert rec.category == TruthCategory.LINGUISTIC_TRUTH
        assert rec.confidence == 1.0

    def test_conventional_truth(self) -> None:
        rec = assign_truth_category("U2", TruthCategory.CONVENTIONAL_TRUTH, 0.8)
        assert rec.category == TruthCategory.CONVENTIONAL_TRUTH
        assert rec.confidence == 0.8

    def test_controlled_transfer(self) -> None:
        rec = assign_truth_category("U3", TruthCategory.CONTROLLED_TRANSFER, 0.5)
        assert rec.category == TruthCategory.CONTROLLED_TRANSFER

    def test_confidence_clamped_high(self) -> None:
        rec = assign_truth_category("U4", TruthCategory.LINGUISTIC_TRUTH, 2.0)
        assert rec.confidence == 1.0

    def test_confidence_clamped_low(self) -> None:
        rec = assign_truth_category("U5", TruthCategory.LINGUISTIC_TRUTH, -0.5)
        assert rec.confidence == 0.0

    def test_id_prefix(self) -> None:
        rec = assign_truth_category("U6", TruthCategory.LINGUISTIC_TRUTH)
        assert rec.truth_id.startswith("TRT_")


# ═════════════════════════════════════════════════════════════════════
# 6. Disambiguate
# ═════════════════════════════════════════════════════════════════════


class TestDisambiguate:
    """Art. 4-22: aggregate disambiguation."""

    def test_all_resolved(self) -> None:
        units = ["U1", "U2"]
        ambs = [
            resolve_ambiguity(u, AmbiguityType.LEXICAL_PURE, AmbiguityResolution.SEMANTIC_CLUE)
            for u in units
        ]
        truths = [assign_truth_category(u, TruthCategory.LINGUISTIC_TRUTH) for u in units]
        res = disambiguate(units, ambiguities=ambs, truth_assignments=truths)
        assert isinstance(res, DisambiguationResult)
        assert res.all_resolved is True

    def test_unresolved_ambiguity(self) -> None:
        units = ["U1"]
        ambs = [resolve_ambiguity("U1", AmbiguityType.LEXICAL_PURE, None)]
        truths = [assign_truth_category("U1", TruthCategory.LINGUISTIC_TRUTH)]
        res = disambiguate(units, ambiguities=ambs, truth_assignments=truths)
        assert res.all_resolved is False

    def test_unresolved_conflict(self) -> None:
        units = ["U1"]
        confs = [resolve_conflict("U1", ConflictType.DUAL_ROLE, None)]
        truths = [assign_truth_category("U1", TruthCategory.LINGUISTIC_TRUTH)]
        res = disambiguate(units, conflicts=confs, truth_assignments=truths)
        assert res.all_resolved is False

    def test_unstable_transfer(self) -> None:
        units = ["U1"]
        trs = [classify_transfer("U1", TransferType.CONVENTIONAL, stable=False)]
        truths = [assign_truth_category("U1", TruthCategory.LINGUISTIC_TRUTH)]
        res = disambiguate(units, transfers=trs, truth_assignments=truths)
        assert res.all_resolved is False

    def test_missing_truth_assignment(self) -> None:
        units = ["U1", "U2"]
        truths = [assign_truth_category("U1", TruthCategory.LINGUISTIC_TRUTH)]
        res = disambiguate(units, truth_assignments=truths)
        assert res.all_resolved is False

    def test_empty_units(self) -> None:
        res = disambiguate([])
        assert res.all_resolved is True

    def test_frozen(self) -> None:
        res = disambiguate([])
        try:
            res.all_resolved = False  # type: ignore[misc]
            assert False, "should be frozen"
        except AttributeError:
            pass


# ═════════════════════════════════════════════════════════════════════
# 7. Build predication
# ═════════════════════════════════════════════════════════════════════


class TestBuildPredication:
    """Art. 26-29: predication."""

    def test_essential_descriptive(self) -> None:
        rec = build_predication("زيد", "قائم", PredicationType.ESSENTIAL_DESCRIPTIVE)
        assert isinstance(rec, PredicationRecord)
        assert rec.valid is True
        assert rec.predication_type == PredicationType.ESSENTIAL_DESCRIPTIVE

    def test_essential_event(self) -> None:
        rec = build_predication("زيد", "ذهب", PredicationType.ESSENTIAL_EVENT)
        assert rec.valid is True
        assert rec.predication_type == PredicationType.ESSENTIAL_EVENT

    def test_essential_existential_copula(self) -> None:
        rec = build_predication("هو", "موجود", PredicationType.ESSENTIAL_EXISTENTIAL_COPULA)
        assert rec.valid is True

    def test_same_subject_predicate_invalid(self) -> None:
        rec = build_predication("زيد", "زيد", PredicationType.ESSENTIAL_DESCRIPTIVE)
        assert rec.valid is False

    def test_empty_subject_invalid(self) -> None:
        rec = build_predication("", "قائم", PredicationType.ESSENTIAL_DESCRIPTIVE)
        assert rec.valid is False

    def test_empty_predicate_invalid(self) -> None:
        rec = build_predication("زيد", "", PredicationType.ESSENTIAL_DESCRIPTIVE)
        assert rec.valid is False

    def test_id_prefix(self) -> None:
        rec = build_predication("أ", "ب", PredicationType.ESSENTIAL_DESCRIPTIVE)
        assert rec.predication_id.startswith("PRD_")


# ═════════════════════════════════════════════════════════════════════
# 8. Build restriction
# ═════════════════════════════════════════════════════════════════════


class TestBuildRestriction:
    """Art. 30-32: restriction."""

    def test_description(self) -> None:
        rec = build_restriction("كتاب", "جديد", RestrictionType.DESCRIPTION)
        assert rec.valid is True
        assert rec.restriction_type == RestrictionType.DESCRIPTION

    def test_adverbial(self) -> None:
        rec = build_restriction("ذهب", "أمس", RestrictionType.ADVERBIAL)
        assert rec.valid is True

    def test_state(self) -> None:
        rec = build_restriction("زيد", "راكبًا", RestrictionType.STATE)
        assert rec.valid is True

    def test_specification(self) -> None:
        rec = build_restriction("عشرون", "رجلًا", RestrictionType.SPECIFICATION)
        assert rec.valid is True

    def test_annexation(self) -> None:
        rec = build_restriction("باب", "المسجد", RestrictionType.ANNEXATION)
        assert rec.valid is True

    def test_numeral(self) -> None:
        rec = build_restriction("طلاب", "عشرة", RestrictionType.NUMERAL)
        assert rec.valid is True

    def test_same_units_invalid(self) -> None:
        rec = build_restriction("كتاب", "كتاب", RestrictionType.DESCRIPTION)
        assert rec.valid is False

    def test_empty_base_invalid(self) -> None:
        rec = build_restriction("", "جديد", RestrictionType.DESCRIPTION)
        assert rec.valid is False

    def test_id_prefix(self) -> None:
        rec = build_restriction("أ", "ب", RestrictionType.DESCRIPTION)
        assert rec.restriction_id.startswith("RST_")


# ═════════════════════════════════════════════════════════════════════
# 9. Build dependency
# ═════════════════════════════════════════════════════════════════════


class TestBuildDependency:
    """Art. 33-35: dependency."""

    def test_adjective(self) -> None:
        rec = build_dependency("الرجل", "الكريم", DependencyType.ADJECTIVE, "صفة")
        assert isinstance(rec, DependencyRecord)
        assert rec.dependency_type == DependencyType.ADJECTIVE

    def test_substitution(self) -> None:
        rec = build_dependency("زيد", "أخوك", DependencyType.SUBSTITUTION, "بدل")
        assert rec.dependency_type == DependencyType.SUBSTITUTION

    def test_emphasis(self) -> None:
        rec = build_dependency("الكتاب", "نفسه", DependencyType.EMPHASIS, "توكيد")
        assert rec.dependency_type == DependencyType.EMPHASIS

    def test_conjunctive_following(self) -> None:
        rec = build_dependency("زيد", "عمرو", DependencyType.CONJUNCTIVE_FOLLOWING, "عطف")
        assert rec.dependency_type == DependencyType.CONJUNCTIVE_FOLLOWING

    def test_id_prefix(self) -> None:
        rec = build_dependency("أ", "ب", DependencyType.ADJECTIVE)
        assert rec.dependency_id.startswith("DEP_")


# ═════════════════════════════════════════════════════════════════════
# 10. Assign role
# ═════════════════════════════════════════════════════════════════════


class TestAssignRole:
    """Art. 39-41: compositional roles."""

    def test_musnad_ilayh_candidate(self) -> None:
        rec = assign_role("زيد", CompositionRole.MUSNAD_ILAYH)
        assert rec.status == RoleStatus.CANDIDATE
        assert rec.role == CompositionRole.MUSNAD_ILAYH

    def test_musnad_realized(self) -> None:
        rec = assign_role("قائم", CompositionRole.MUSNAD, realized=True)
        assert rec.status == RoleStatus.REALIZED

    def test_qayd(self) -> None:
        rec = assign_role("أمس", CompositionRole.QAYD)
        assert rec.role == CompositionRole.QAYD

    def test_tabi(self) -> None:
        rec = assign_role("الكريم", CompositionRole.TABI)
        assert rec.role == CompositionRole.TABI

    def test_rabit(self) -> None:
        rec = assign_role("و", CompositionRole.RABIT)
        assert rec.role == CompositionRole.RABIT

    def test_mufassir(self) -> None:
        rec = assign_role("أي", CompositionRole.MUFASSIR)
        assert rec.role == CompositionRole.MUFASSIR

    def test_id_prefix(self) -> None:
        rec = assign_role("U", CompositionRole.MUSNAD)
        assert rec.role_id.startswith("ROL_")


# ═════════════════════════════════════════════════════════════════════
# 11. Build proposition
# ═════════════════════════════════════════════════════════════════════


class TestBuildProposition:
    """Art. 42-44: propositions."""

    def test_nominal_closed(self) -> None:
        pred = _predication()
        roles = _roles_realized()
        prop = build_proposition(pred, (), (), roles, PropositionType.NOMINAL)
        assert prop.closed is True
        assert prop.proposition_type == PropositionType.NOMINAL

    def test_verbal_closed(self) -> None:
        pred = build_predication("الولد", "كتب", PredicationType.ESSENTIAL_EVENT)
        roles = _roles_realized("الولد", "كتب")
        prop = build_proposition(pred, (), (), roles, PropositionType.VERBAL)
        assert prop.closed is True
        assert prop.proposition_type == PropositionType.VERBAL

    def test_copular(self) -> None:
        pred = build_predication("هو", "عالم", PredicationType.ESSENTIAL_EXISTENTIAL_COPULA)
        roles = _roles_realized("هو", "عالم")
        prop = build_proposition(pred, (), (), roles, PropositionType.COPULAR)
        assert prop.closed is True

    def test_conditional(self) -> None:
        pred = _predication()
        roles = _roles_realized()
        prop = build_proposition(pred, (), (), roles, PropositionType.CONDITIONAL)
        assert prop.proposition_type == PropositionType.CONDITIONAL

    def test_unclosed_no_roles(self) -> None:
        pred = _predication()
        prop = build_proposition(pred, (), (), (), PropositionType.NOMINAL)
        assert prop.closed is False

    def test_unclosed_candidate_roles(self) -> None:
        pred = _predication()
        roles = (
            assign_role("زيد", CompositionRole.MUSNAD_ILAYH),
            assign_role("قائم", CompositionRole.MUSNAD),
        )
        prop = build_proposition(pred, (), (), roles, PropositionType.NOMINAL)
        assert prop.closed is False  # roles are CANDIDATE

    def test_unclosed_invalid_predication(self) -> None:
        pred = build_predication("", "قائم", PredicationType.ESSENTIAL_DESCRIPTIVE)
        roles = _roles_realized()
        prop = build_proposition(pred, (), (), roles, PropositionType.NOMINAL)
        assert prop.closed is False

    def test_unclosed_invalid_restriction(self) -> None:
        pred = _predication()
        roles = _roles_realized()
        rests = (build_restriction("", "x", RestrictionType.DESCRIPTION),)
        prop = build_proposition(pred, rests, (), roles, PropositionType.NOMINAL)
        assert prop.closed is False

    def test_with_dependencies(self) -> None:
        pred = _predication()
        roles = _roles_realized()
        deps = (build_dependency("الرجل", "الكريم", DependencyType.ADJECTIVE),)
        prop = build_proposition(pred, (), deps, roles)
        assert prop.closed is True
        assert len(prop.dependencies) == 1

    def test_id_prefix(self) -> None:
        prop = _proposition()
        assert prop.proposition_id.startswith("PRP_")


# ═════════════════════════════════════════════════════════════════════
# 12. Check gate
# ═════════════════════════════════════════════════════════════════════


class TestCheckGate:
    """Art. 64-72: all 8 gates."""

    def test_disambiguation_pass(self) -> None:
        ctx = {"disambiguation": _disambiguation_ok()}
        g = check_gate(CompositionGate.DISAMBIGUATION, ctx)
        assert isinstance(g, GateResult)
        assert g.passed is True

    def test_disambiguation_fail(self) -> None:
        ctx = {"disambiguation": DisambiguationResult(all_resolved=False)}
        g = check_gate(CompositionGate.DISAMBIGUATION, ctx)
        assert g.passed is False

    def test_reference_stability_pass(self) -> None:
        g = check_gate(CompositionGate.REFERENCE_STABILITY, {"reference_stable": True})
        assert g.passed is True

    def test_reference_stability_fail(self) -> None:
        g = check_gate(CompositionGate.REFERENCE_STABILITY, {})
        assert g.passed is False

    def test_predicate_readiness_pass(self) -> None:
        g = check_gate(CompositionGate.PREDICATE_READINESS, {"predicate_ready": True})
        assert g.passed is True

    def test_predicate_readiness_fail(self) -> None:
        g = check_gate(CompositionGate.PREDICATE_READINESS, {})
        assert g.passed is False

    def test_role_assignment_pass(self) -> None:
        roles = _roles_realized()
        g = check_gate(CompositionGate.ROLE_ASSIGNMENT, {"roles": roles})
        assert g.passed is True

    def test_role_assignment_fail_no_roles(self) -> None:
        g = check_gate(CompositionGate.ROLE_ASSIGNMENT, {"roles": ()})
        assert g.passed is False

    def test_role_assignment_fail_candidate(self) -> None:
        roles = (assign_role("U1", CompositionRole.MUSNAD_ILAYH),)
        g = check_gate(CompositionGate.ROLE_ASSIGNMENT, {"roles": roles})
        assert g.passed is False

    def test_relation_validity_pass(self) -> None:
        g = check_gate(CompositionGate.RELATION_VALIDITY, {"relations_valid": True})
        assert g.passed is True

    def test_relation_validity_fail(self) -> None:
        g = check_gate(CompositionGate.RELATION_VALIDITY, {})
        assert g.passed is False

    def test_conflict_resolution_pass(self) -> None:
        ctx = {"disambiguation": _disambiguation_ok()}
        g = check_gate(CompositionGate.CONFLICT_RESOLUTION, ctx)
        assert g.passed is True

    def test_conflict_resolution_fail(self) -> None:
        dis = disambiguate(
            ["U1"],
            conflicts=[resolve_conflict("U1", ConflictType.DUAL_ROLE, None)],
            truth_assignments=[assign_truth_category("U1", TruthCategory.LINGUISTIC_TRUTH)],
        )
        g = check_gate(CompositionGate.CONFLICT_RESOLUTION, {"disambiguation": dis})
        assert g.passed is False

    def test_proposition_closure_pass(self) -> None:
        props = [_proposition(closed=True)]
        g = check_gate(CompositionGate.PROPOSITION_CLOSURE, {"propositions": props})
        assert g.passed is True

    def test_proposition_closure_fail(self) -> None:
        props = [_proposition(closed=False)]
        g = check_gate(CompositionGate.PROPOSITION_CLOSURE, {"propositions": props})
        assert g.passed is False

    def test_proposition_closure_fail_empty(self) -> None:
        g = check_gate(CompositionGate.PROPOSITION_CLOSURE, {"propositions": ()})
        assert g.passed is False

    def test_interproposition_link_single(self) -> None:
        g = check_gate(
            CompositionGate.INTERPROPOSITION_LINK,
            {"propositions": [_proposition()], "links": ()},
        )
        assert g.passed is True  # single prop needs no link

    def test_interproposition_link_multi_pass(self) -> None:
        g = check_gate(
            CompositionGate.INTERPROPOSITION_LINK,
            {
                "propositions": [_proposition(), _proposition()],
                "links": [InterPropositionLink.CONJUNCTION],
            },
        )
        assert g.passed is True

    def test_interproposition_link_multi_fail(self) -> None:
        g = check_gate(
            CompositionGate.INTERPROPOSITION_LINK,
            {"propositions": [_proposition(), _proposition()], "links": ()},
        )
        assert g.passed is False


# ═════════════════════════════════════════════════════════════════════
# 13. Compute readiness
# ═════════════════════════════════════════════════════════════════════


class TestComputeReadiness:
    """Art. 75: readiness formula."""

    def test_perfect(self) -> None:
        assert compute_readiness(1, 1, 1, 1, 1, 1) == 1.0

    def test_zero(self) -> None:
        assert compute_readiness(0, 0, 0, 0, 0, 0) == 0.0

    def test_threshold_exact(self) -> None:
        r = compute_readiness(0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        assert r == 0.5

    def test_below_threshold(self) -> None:
        r = compute_readiness(0.3, 0.3, 0.3, 0.3, 0.3, 0.3)
        assert r < 0.5

    def test_above_threshold(self) -> None:
        r = compute_readiness(0.8, 0.8, 0.8, 0.8, 0.8, 0.8)
        assert r > 0.5

    def test_mixed(self) -> None:
        r = compute_readiness(1.0, 1.0, 0.0, 0.0, 1.0, 1.0)
        expected = (1 + 1 + 0 + 0 + 1 + 1) / 6
        assert abs(r - expected) < 1e-9


# ═════════════════════════════════════════════════════════════════════
# 14. Build composition (end-to-end)
# ═════════════════════════════════════════════════════════════════════


class TestBuildComposition:
    """Art. 73-78: full composition."""

    def test_accepted(self) -> None:
        prop = _proposition(closed=True)
        rec = build_composition(
            ["زيد", "قائم"],
            [prop],
            [],
            disambiguation=_disambiguation_ok(),
        )
        assert isinstance(rec, CompositionRecord)
        assert rec.verdict == CompositionVerdict.ACCEPTED
        assert rec.readiness >= 0.5

    def test_rejected_disambiguation_fail(self) -> None:
        prop = _proposition(closed=True)
        dis = DisambiguationResult(all_resolved=False)
        rec = build_composition(
            ["زيد", "قائم"],
            [prop],
            [],
            disambiguation=dis,
        )
        assert rec.verdict == CompositionVerdict.REJECTED

    def test_rejected_unclosed_proposition(self) -> None:
        prop = _proposition(closed=False)
        rec = build_composition(
            ["زيد", "قائم"],
            [prop],
            [],
            disambiguation=_disambiguation_ok(),
        )
        assert rec.verdict == CompositionVerdict.REJECTED

    def test_with_inter_proposition_links(self) -> None:
        p1 = _proposition(closed=True)
        p2 = _proposition(closed=True)
        rec = build_composition(
            ["زيد", "قائم", "عمرو", "جالس"],
            [p1, p2],
            [InterPropositionLink.CONJUNCTION],
            disambiguation=_disambiguation_ok(),
        )
        assert rec.verdict == CompositionVerdict.ACCEPTED
        assert InterPropositionLink.CONJUNCTION in rec.links

    def test_rejected_multi_no_link(self) -> None:
        p1 = _proposition(closed=True)
        p2 = _proposition(closed=True)
        rec = build_composition(
            ["U1", "U2", "U3", "U4"],
            [p1, p2],
            [],  # missing links
            disambiguation=_disambiguation_ok(),
        )
        assert rec.verdict == CompositionVerdict.REJECTED

    def test_relations_inferred(self) -> None:
        prop = _proposition(closed=True)
        rec = build_composition(["U1", "U2"], [prop])
        assert CompositionRelation.PREDICATION in rec.relations

    def test_roles_collected(self) -> None:
        prop = _proposition(closed=True)
        rec = build_composition(["U1", "U2"], [prop])
        assert len(rec.roles) >= 2

    def test_id_prefix(self) -> None:
        prop = _proposition(closed=True)
        rec = build_composition(["U1"], [prop])
        assert rec.composition_id.startswith("CMP_")

    def test_gates_populated(self) -> None:
        prop = _proposition(closed=True)
        rec = build_composition(["U1"], [prop])
        assert len(rec.gates) == 8


# ═════════════════════════════════════════════════════════════════════
# 15. Batch compose
# ═════════════════════════════════════════════════════════════════════


class TestBatchCompose:
    """Batch composition factory."""

    def test_single_group(self) -> None:
        prop = _proposition(closed=True)
        results = batch_compose([(["U1", "U2"], [prop], [])])
        assert len(results) == 1
        assert isinstance(results[0], CompositionRecord)

    def test_multiple_groups(self) -> None:
        p1 = _proposition(closed=True)
        p2 = _proposition(closed=True)
        results = batch_compose([
            (["U1", "U2"], [p1], []),
            (["U3", "U4"], [p2], []),
        ])
        assert len(results) == 2

    def test_empty(self) -> None:
        results = batch_compose([])
        assert results == []


# ═════════════════════════════════════════════════════════════════════
# 16. Fractal law cycle
# ═════════════════════════════════════════════════════════════════════


class TestFractalLaw:
    """Art. 57-63: تعيين → حفظ → ربط → حكم → انتقال → رد."""

    def test_cycle_integrity(self) -> None:
        """The CompositionRecord captures the full fractal cycle."""
        prop = _proposition(closed=True)
        rec = build_composition(
            ["زيد", "قائم"],
            [prop],
            [],
            disambiguation=_disambiguation_ok(),
        )

        # تعيين — units identified
        assert len(rec.units) == 2

        # حفظ — gates preserve boundaries
        assert len(rec.gates) == 8

        # ربط — relations established
        assert CompositionRelation.PREDICATION in rec.relations

        # حكم — verdict issued
        assert rec.verdict == CompositionVerdict.ACCEPTED

        # انتقال — propositions generated (transition from unit → proposition)
        assert len(rec.propositions) >= 1

        # رد — traceable back to units, roles, gates
        assert all(isinstance(g, GateResult) for g in rec.gates)
        assert all(isinstance(r, CompositionRoleRecord) for r in rec.roles)

    def test_cycle_rejected_blocks_transition(self) -> None:
        """When gates fail, the cycle does not reach انتقال/حكم=ACCEPTED."""
        prop = _proposition(closed=False)
        rec = build_composition(["U1"], [prop])
        assert rec.verdict == CompositionVerdict.REJECTED
