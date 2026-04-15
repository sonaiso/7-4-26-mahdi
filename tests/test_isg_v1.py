"""Tests for Informational Stock Governance (ISG) Constitution v1.

Covers:
  - Enum completeness (§7.1)
  - Knowledge atom lifecycle (§7.2)
  - Source verification (§7.3)
  - Level matching (§7.4)
  - Callability evaluation (§7.5)
  - Conflict resolution (§7.6)
  - Gate decisions (§7.7)
  - End-to-end govern() (§7.8)
  - Opinion separation (§7.9)
  - Pipeline integration (§7.10)
"""

from __future__ import annotations

import pytest

from arabic_engine.cognition.isg_seed_data import (
    DEFAULT_CONFLICT_PRIORITY_ORDER,
    DEFAULT_GOVERNANCE_THRESHOLDS,
    DEFAULT_READINESS_CRITERIA,
)
from arabic_engine.cognition.isg_v1 import (
    check_level_match,
    classify_atom,
    evaluate_callability,
    evaluate_gate,
    govern,
    identify_atom,
    resolve_internal_conflict,
    separate_opinions,
    verify_source,
)
from arabic_engine.core.enums import (
    CallabilityStatus,
    ConfirmationRank,
    EpistemicEntryKind,
    GateDecision,
    InternalConflictType,
    ISGConflictResolution,
    KnowledgeAtomType,
    LevelMatchStatus,
    PriorKnowledgeType,
    ReadinessLevel,
    SourceType,
    VerificationStatus,
)
from arabic_engine.core.types import (
    CallabilityResult,
    GovernanceGateResult,
    InternalConflictRecord,
    ISGValidationResult,
    KnowledgeAtom,
    LevelMatchResult,
    SourceRecord,
)

# ── Helpers ──────────────────────────────────────────────────────────


def _atom(
    *,
    atom_id: str = "KA_test",
    label: str = "test_atom",
    atom_type: KnowledgeAtomType = KnowledgeAtomType.LEXICAL,
    knowledge_level: str = "token",
    domain: str = "linguistic",
    source: str = "test_source",
    source_type: SourceType = SourceType.PRIMARY,
    confirmation_rank: ConfirmationRank = ConfirmationRank.ESTABLISHED,
    context: str = "test_context",
    entry_kind: EpistemicEntryKind = EpistemicEntryKind.INFORMATION,
    verification: VerificationStatus = VerificationStatus.VERIFIED,
    relations: tuple[str, ...] = (),
) -> KnowledgeAtom:
    return KnowledgeAtom(
        atom_id=atom_id,
        atom_type=atom_type,
        label=label,
        knowledge_level=knowledge_level,
        domain=domain,
        source=source,
        source_type=source_type,
        confirmation_rank=confirmation_rank,
        context=context,
        relations=relations,
        entry_kind=entry_kind,
        verification=verification,
    )


def _source_record(
    *,
    source_id: str = "SR_test",
    source_type: SourceType = SourceType.PRIMARY,
    transmitter: str = "test_transmitter",
    confirmation_rank: ConfirmationRank = ConfirmationRank.ESTABLISHED,
    trust_degree: float = 1.0,
    review_status: VerificationStatus = VerificationStatus.VERIFIED,
) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        source_type=source_type,
        transmitter=transmitter,
        confirmation_rank=confirmation_rank,
        trust_degree=trust_degree,
        review_status=review_status,
    )


# ═══════════════════════════════════════════════════════════════════════
# §7.1 — Enum completeness
# ═══════════════════════════════════════════════════════════════════════


class TestEnumCompleteness:
    """Verify exact member count and member names for all 12 ISG enums."""

    def test_knowledge_atom_type_count(self):
        assert len(KnowledgeAtomType) == 10

    def test_knowledge_atom_type_members(self):
        names = {m.name for m in KnowledgeAtomType}
        expected = {
            "LEXICAL", "SEMANTIC", "CLASSIFICATORY", "REFERENTIAL",
            "RELATIONAL", "NORMATIVE_RULE", "CONTEXTUAL", "CRITERION",
            "SYMBOLIC", "MATHEMATICAL",
        }
        assert names == expected

    def test_prior_knowledge_type_count(self):
        assert len(PriorKnowledgeType) == 10

    def test_prior_knowledge_type_members(self):
        names = {m.name for m in PriorKnowledgeType}
        expected = {
            "DEFINITIONAL", "CLASSIFICATORY", "RELATIONAL", "LINGUISTIC",
            "CONVENTIONAL", "INTERPRETIVE", "RULE_BASED", "NORMATIVE",
            "SYMBOLIC", "MATHEMATICAL",
        }
        assert names == expected

    def test_epistemic_entry_kind_count(self):
        assert len(EpistemicEntryKind) == 5

    def test_epistemic_entry_kind_members(self):
        names = {m.name for m in EpistemicEntryKind}
        expected = {"INFORMATION", "OPINION", "HYPOTHESIS", "ESTIMATE", "PRIOR_POSITION"}
        assert names == expected

    def test_confirmation_rank_count(self):
        assert len(ConfirmationRank) == 5

    def test_confirmation_rank_members(self):
        names = {m.name for m in ConfirmationRank}
        expected = {"ESTABLISHED", "PREPONDERANT", "PROBABLE", "SUSPENDED", "REJECTED"}
        assert names == expected

    def test_source_type_count(self):
        assert len(SourceType) == 6

    def test_source_type_members(self):
        names = {m.name for m in SourceType}
        expected = {
            "PRIMARY", "SECONDARY", "DERIVED",
            "CONTEXTUAL_SOURCE", "INFERENTIAL", "TERMINOLOGICAL",
        }
        assert names == expected

    def test_level_match_status_count(self):
        assert len(LevelMatchStatus) == 7

    def test_level_match_status_members(self):
        names = {m.name for m in LevelMatchStatus}
        expected = {
            "MATCHED", "EXCESSIVELY_BROAD", "EXCESSIVELY_NARROW",
            "WRONG_LAYER", "DIFFERENT_DOMAIN",
            "UNJUSTIFIED_GENERALISATION", "UNJUSTIFIED_PARTICULARISATION",
        }
        assert names == expected

    def test_callability_status_count(self):
        assert len(CallabilityStatus) == 3

    def test_callability_status_members(self):
        names = {m.name for m in CallabilityStatus}
        expected = {"CALLABLE", "BLOCKED", "CONDITIONAL"}
        assert names == expected

    def test_internal_conflict_type_count(self):
        assert len(InternalConflictType) == 6

    def test_internal_conflict_type_members(self):
        names = {m.name for m in InternalConflictType}
        expected = {
            "INFO_VS_INFO", "RULE_VS_RULE", "USAGE_VS_USAGE",
            "LITERAL_VS_CONVENTIONAL", "NARRATION_VS_NARRATION",
            "CONTEXT_VS_CONTEXT",
        }
        assert names == expected

    def test_isg_conflict_resolution_count(self):
        assert len(ISGConflictResolution) == 7

    def test_isg_conflict_resolution_members(self):
        names = {m.name for m in ISGConflictResolution}
        expected = {
            "BY_CONFIRMATION_RANK", "BY_DOMAIN", "BY_INPUT_RELEVANCE",
            "BY_CONTEXT_PRIORITY", "BY_RULE_RANK", "BY_SPECIALISATION",
            "SUSPENDED_UNRESOLVED",
        }
        assert names == expected

    def test_gate_decision_count(self):
        assert len(GateDecision) == 4

    def test_gate_decision_members(self):
        names = {m.name for m in GateDecision}
        expected = {"PASS", "REJECT", "SUSPEND", "COMPLETE"}
        assert names == expected

    def test_readiness_level_count(self):
        assert len(ReadinessLevel) == 3

    def test_readiness_level_members(self):
        names = {m.name for m in ReadinessLevel}
        expected = {"FIRST", "SECOND", "THIRD"}
        assert names == expected

    def test_verification_status_count(self):
        assert len(VerificationStatus) == 4

    def test_verification_status_members(self):
        names = {m.name for m in VerificationStatus}
        expected = {"VERIFIED", "UNVERIFIED", "UNDER_REVIEW", "DISQUALIFIED"}
        assert names == expected


# ═══════════════════════════════════════════════════════════════════════
# §7.2 — Knowledge Atom tests
# ═══════════════════════════════════════════════════════════════════════


class TestIdentifyAtom:
    """Step 1 — identify_atom."""

    def test_valid_atom_creation(self):
        atom = identify_atom(
            label="كتاب",
            atom_type=KnowledgeAtomType.LEXICAL,
            knowledge_level="token",
            domain="linguistic",
            source="lexicon",
            source_type=SourceType.PRIMARY,
            confirmation_rank=ConfirmationRank.ESTABLISHED,
            context="sentence",
        )
        assert atom.label == "كتاب"
        assert atom.atom_type == KnowledgeAtomType.LEXICAL
        assert atom.verification == VerificationStatus.UNVERIFIED

    def test_auto_id_generation(self):
        a1 = identify_atom(
            label="a", atom_type=KnowledgeAtomType.SEMANTIC,
            knowledge_level="concept", domain="ontology",
            source="db", source_type=SourceType.PRIMARY,
            confirmation_rank=ConfirmationRank.PROBABLE,
            context="ctx",
        )
        a2 = identify_atom(
            label="b", atom_type=KnowledgeAtomType.SEMANTIC,
            knowledge_level="concept", domain="ontology",
            source="db", source_type=SourceType.PRIMARY,
            confirmation_rank=ConfirmationRank.PROBABLE,
            context="ctx",
        )
        assert a1.atom_id != a2.atom_id
        assert a1.atom_id.startswith("KA_")
        assert a2.atom_id.startswith("KA_")

    def test_custom_atom_id(self):
        atom = identify_atom(
            label="x", atom_type=KnowledgeAtomType.MATHEMATICAL,
            knowledge_level="formal", domain="math",
            source="axiom", source_type=SourceType.PRIMARY,
            confirmation_rank=ConfirmationRank.ESTABLISHED,
            context="proof", atom_id="CUSTOM_001",
        )
        assert atom.atom_id == "CUSTOM_001"

    def test_empty_label_raises(self):
        with pytest.raises(ValueError, match="label"):
            identify_atom(
                label="", atom_type=KnowledgeAtomType.LEXICAL,
                knowledge_level="token", domain="ling",
                source="s", source_type=SourceType.PRIMARY,
                confirmation_rank=ConfirmationRank.ESTABLISHED,
                context="c",
            )

    def test_empty_domain_raises(self):
        with pytest.raises(ValueError, match="domain"):
            identify_atom(
                label="x", atom_type=KnowledgeAtomType.LEXICAL,
                knowledge_level="token", domain="",
                source="s", source_type=SourceType.PRIMARY,
                confirmation_rank=ConfirmationRank.ESTABLISHED,
                context="c",
            )

    def test_empty_source_raises(self):
        with pytest.raises(ValueError, match="source"):
            identify_atom(
                label="x", atom_type=KnowledgeAtomType.LEXICAL,
                knowledge_level="token", domain="d",
                source="", source_type=SourceType.PRIMARY,
                confirmation_rank=ConfirmationRank.ESTABLISHED,
                context="c",
            )

    def test_empty_context_raises(self):
        with pytest.raises(ValueError, match="context"):
            identify_atom(
                label="x", atom_type=KnowledgeAtomType.LEXICAL,
                knowledge_level="token", domain="d",
                source="s", source_type=SourceType.PRIMARY,
                confirmation_rank=ConfirmationRank.ESTABLISHED,
                context="",
            )

    def test_empty_knowledge_level_raises(self):
        with pytest.raises(ValueError, match="knowledge_level"):
            identify_atom(
                label="x", atom_type=KnowledgeAtomType.LEXICAL,
                knowledge_level="", domain="d",
                source="s", source_type=SourceType.PRIMARY,
                confirmation_rank=ConfirmationRank.ESTABLISHED,
                context="c",
            )

    def test_default_entry_kind_is_information(self):
        atom = identify_atom(
            label="x", atom_type=KnowledgeAtomType.LEXICAL,
            knowledge_level="token", domain="d",
            source="s", source_type=SourceType.PRIMARY,
            confirmation_rank=ConfirmationRank.ESTABLISHED,
            context="c",
        )
        assert atom.entry_kind == EpistemicEntryKind.INFORMATION


class TestClassifyAtom:
    """Step 2 — classify_atom."""

    def test_classify_returns_frozen_copy(self):
        atom = _atom()
        result = classify_atom(atom)
        assert result == atom
        assert result is not atom  # new frozen copy

    @pytest.mark.parametrize("atype", list(KnowledgeAtomType))
    def test_classify_all_valid_types(self, atype):
        atom = _atom(atom_type=atype)
        result = classify_atom(atom)
        assert result.atom_type == atype


# ═══════════════════════════════════════════════════════════════════════
# §7.3 — Source verification tests
# ═══════════════════════════════════════════════════════════════════════


class TestVerifySource:
    """Step 3 — verify_source."""

    def test_verified_source(self):
        atom = _atom(verification=VerificationStatus.UNVERIFIED)
        src = _source_record()
        result = verify_source(atom, src)
        assert result.verification == VerificationStatus.VERIFIED

    def test_unknown_source_disqualified(self):
        atom = _atom()
        src = _source_record(source_id="", transmitter="")
        result = verify_source(atom, src)
        assert result.verification == VerificationStatus.DISQUALIFIED

    def test_rank_mismatch_under_review(self):
        atom = _atom(confirmation_rank=ConfirmationRank.ESTABLISHED)
        src = _source_record(confirmation_rank=ConfirmationRank.PROBABLE)
        result = verify_source(atom, src)
        assert result.verification == VerificationStatus.UNDER_REVIEW

    def test_low_trust_disqualified(self):
        atom = _atom()
        src = _source_record(trust_degree=0.1)
        result = verify_source(atom, src)
        assert result.verification == VerificationStatus.DISQUALIFIED

    def test_disqualified_source_propagates(self):
        atom = _atom()
        src = _source_record(review_status=VerificationStatus.DISQUALIFIED)
        result = verify_source(atom, src)
        assert result.verification == VerificationStatus.DISQUALIFIED

    @pytest.mark.parametrize("rank", list(ConfirmationRank))
    def test_all_confirmation_ranks(self, rank):
        atom = _atom(confirmation_rank=rank)
        src = _source_record(confirmation_rank=rank)
        result = verify_source(atom, src)
        # If source is verified and ranks match, should be verified
        assert result.verification == VerificationStatus.VERIFIED


# ═══════════════════════════════════════════════════════════════════════
# §7.4 — Level matching tests
# ═══════════════════════════════════════════════════════════════════════


class TestCheckLevelMatch:
    """Step 3b — check_level_match."""

    def test_matched_same_level(self):
        atom = _atom(knowledge_level="token")
        result = check_level_match(atom, "IN_001", "token", "linguistic")
        assert result.status == LevelMatchStatus.MATCHED

    def test_matched_empty_input_level(self):
        atom = _atom(knowledge_level="any_level")
        result = check_level_match(atom, "IN_001", "", "linguistic")
        assert result.status == LevelMatchStatus.MATCHED

    def test_different_domain(self):
        atom = _atom(domain="linguistic")
        result = check_level_match(atom, "IN_001", "token", "mathematics")
        assert result.status == LevelMatchStatus.DIFFERENT_DOMAIN

    def test_unjustified_generalisation(self):
        atom = _atom(knowledge_level="general")
        result = check_level_match(atom, "IN_001", "specific", "linguistic")
        assert result.status == LevelMatchStatus.UNJUSTIFIED_GENERALISATION

    def test_unjustified_particularisation(self):
        atom = _atom(knowledge_level="specific")
        result = check_level_match(atom, "IN_001", "general", "linguistic")
        assert result.status == LevelMatchStatus.UNJUSTIFIED_PARTICULARISATION

    def test_excessively_broad(self):
        atom = _atom(knowledge_level="broad")
        result = check_level_match(atom, "IN_001", "token", "linguistic")
        assert result.status == LevelMatchStatus.EXCESSIVELY_BROAD

    def test_excessively_narrow(self):
        atom = _atom(knowledge_level="narrow")
        result = check_level_match(atom, "IN_001", "token", "linguistic")
        assert result.status == LevelMatchStatus.EXCESSIVELY_NARROW

    def test_wrong_layer_fallback(self):
        atom = _atom(knowledge_level="layer_x")
        result = check_level_match(atom, "IN_001", "layer_y", "linguistic")
        assert result.status == LevelMatchStatus.WRONG_LAYER

    def test_empty_input_domain_matches(self):
        atom = _atom(domain="anything", knowledge_level="anything")
        result = check_level_match(atom, "IN_001", "anything", "")
        assert result.status == LevelMatchStatus.MATCHED


# ═══════════════════════════════════════════════════════════════════════
# §7.5 — Callability tests
# ═══════════════════════════════════════════════════════════════════════


class TestEvaluateCallability:
    """Step 4 — evaluate_callability."""

    def test_callable_verified_information(self):
        atom = _atom(
            entry_kind=EpistemicEntryKind.INFORMATION,
            verification=VerificationStatus.VERIFIED,
            confirmation_rank=ConfirmationRank.ESTABLISHED,
        )
        result = evaluate_callability(atom, "IN_001")
        assert result.status == CallabilityStatus.CALLABLE

    def test_blocked_low_context_fit(self):
        atom = _atom()
        result = evaluate_callability(atom, "IN_001", context_fit=0.1)
        assert result.status == CallabilityStatus.BLOCKED
        assert "Context fit" in result.reason

    def test_conditional_conflict_state(self):
        atom = _atom()
        result = evaluate_callability(atom, "IN_001", conflict_state=True)
        assert result.status == CallabilityStatus.CONDITIONAL

    def test_blocked_opinion_contamination(self):
        atom = _atom(
            entry_kind=EpistemicEntryKind.OPINION,
            verification=VerificationStatus.UNVERIFIED,
        )
        result = evaluate_callability(atom, "IN_001")
        assert result.status == CallabilityStatus.BLOCKED
        assert "Opinion" in result.reason

    def test_blocked_rejected_rank(self):
        atom = _atom(
            confirmation_rank=ConfirmationRank.REJECTED,
            entry_kind=EpistemicEntryKind.INFORMATION,
        )
        result = evaluate_callability(atom, "IN_001")
        assert result.status == CallabilityStatus.BLOCKED

    def test_conditional_suspended_rank(self):
        atom = _atom(confirmation_rank=ConfirmationRank.SUSPENDED)
        result = evaluate_callability(atom, "IN_001")
        assert result.status == CallabilityStatus.CONDITIONAL

    def test_blocked_disqualified_verification(self):
        atom = _atom(verification=VerificationStatus.DISQUALIFIED)
        result = evaluate_callability(atom, "IN_001")
        assert result.status == CallabilityStatus.BLOCKED

    def test_priority_established_higher_than_probable(self):
        a_est = _atom(confirmation_rank=ConfirmationRank.ESTABLISHED)
        a_prob = _atom(confirmation_rank=ConfirmationRank.PROBABLE)
        r_est = evaluate_callability(a_est, "IN_001")
        r_prob = evaluate_callability(a_prob, "IN_001")
        assert r_est.priority > r_prob.priority

    def test_priority_high_context_fit(self):
        atom = _atom()
        r_high = evaluate_callability(atom, "IN_001", context_fit=1.0)
        r_low = evaluate_callability(atom, "IN_001", context_fit=0.3)
        assert r_high.priority > r_low.priority


# ═══════════════════════════════════════════════════════════════════════
# §7.6 — Conflict resolution tests
# ═══════════════════════════════════════════════════════════════════════


class TestResolveInternalConflict:
    """Step 5 — resolve_internal_conflict."""

    def test_by_confirmation_rank_a_wins(self):
        a = _atom(atom_id="A", confirmation_rank=ConfirmationRank.ESTABLISHED)
        b = _atom(atom_id="B", confirmation_rank=ConfirmationRank.PROBABLE)
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.BY_CONFIRMATION_RANK,
        )
        assert result.resolved
        assert result.winner_id == "A"

    def test_by_confirmation_rank_b_wins(self):
        a = _atom(atom_id="A", confirmation_rank=ConfirmationRank.PROBABLE)
        b = _atom(atom_id="B", confirmation_rank=ConfirmationRank.ESTABLISHED)
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.BY_CONFIRMATION_RANK,
        )
        assert result.resolved
        assert result.winner_id == "B"

    def test_by_confirmation_rank_tie_unresolved(self):
        a = _atom(atom_id="A", confirmation_rank=ConfirmationRank.PROBABLE)
        b = _atom(atom_id="B", confirmation_rank=ConfirmationRank.PROBABLE)
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.BY_CONFIRMATION_RANK,
        )
        assert not result.resolved

    def test_by_domain_different_domains(self):
        a = _atom(atom_id="A", domain="linguistics")
        b = _atom(atom_id="B", domain="mathematics")
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.BY_DOMAIN,
        )
        assert result.resolved
        assert result.winner_id == "A"

    def test_by_domain_same_domain_unresolved(self):
        a = _atom(atom_id="A", domain="same")
        b = _atom(atom_id="B", domain="same")
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.BY_DOMAIN,
        )
        assert not result.resolved

    def test_by_input_relevance(self):
        a = _atom(atom_id="A", verification=VerificationStatus.VERIFIED)
        b = _atom(atom_id="B", verification=VerificationStatus.UNVERIFIED)
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.BY_INPUT_RELEVANCE,
        )
        assert result.resolved
        assert result.winner_id == "A"

    def test_by_context_priority(self):
        a = _atom(atom_id="A", context="has_context")
        b = _atom(atom_id="B", context="")
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.BY_CONTEXT_PRIORITY,
        )
        assert result.resolved
        assert result.winner_id == "A"

    def test_by_rule_rank(self):
        a = _atom(atom_id="A", atom_type=KnowledgeAtomType.NORMATIVE_RULE)
        b = _atom(atom_id="B", atom_type=KnowledgeAtomType.LEXICAL)
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.BY_RULE_RANK,
        )
        assert result.resolved
        assert result.winner_id == "A"

    def test_by_specialisation(self):
        a = _atom(atom_id="A", domain="ling")
        b = _atom(atom_id="B", domain="linguistics_general")
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.BY_SPECIALISATION,
        )
        assert result.resolved
        assert result.winner_id == "A"

    def test_suspended_unresolved(self):
        a = _atom(atom_id="A")
        b = _atom(atom_id="B")
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.SUSPENDED_UNRESOLVED,
        )
        assert not result.resolved
        assert result.winner_id is None

    @pytest.mark.parametrize("ctype", list(InternalConflictType))
    def test_all_conflict_types(self, ctype):
        a = _atom(atom_id="A")
        b = _atom(atom_id="B")
        result = resolve_internal_conflict(
            a, b, ISGConflictResolution.SUSPENDED_UNRESOLVED,
            conflict_type=ctype,
        )
        assert result.conflict_type == ctype

    def test_auto_conflict_id(self):
        a = _atom(atom_id="A")
        b = _atom(atom_id="B")
        r1 = resolve_internal_conflict(
            a, b, ISGConflictResolution.SUSPENDED_UNRESOLVED,
        )
        r2 = resolve_internal_conflict(
            a, b, ISGConflictResolution.SUSPENDED_UNRESOLVED,
        )
        assert r1.conflict_id != r2.conflict_id
        assert r1.conflict_id.startswith("ICR_")


# ═══════════════════════════════════════════════════════════════════════
# §7.7 — Gate decision tests
# ═══════════════════════════════════════════════════════════════════════


class TestEvaluateGate:
    """Step 6 — evaluate_gate."""

    def _match(self, status=LevelMatchStatus.MATCHED):
        return LevelMatchResult(
            atom_id="A", input_id="IN", status=status, reason="test",
        )

    def _call(self, status=CallabilityStatus.CALLABLE):
        return CallabilityResult(
            atom_id="A", input_id="IN", status=status,
            priority=50, reason="test",
        )

    def test_pass_all_ok(self):
        atom = _atom(verification=VerificationStatus.VERIFIED)
        gate = evaluate_gate(atom, "IN", self._match(), self._call())
        assert gate.decision == GateDecision.PASS
        assert gate.readiness == ReadinessLevel.FIRST

    def test_reject_disqualified(self):
        atom = _atom(verification=VerificationStatus.DISQUALIFIED)
        gate = evaluate_gate(atom, "IN", self._match(), self._call())
        assert gate.decision == GateDecision.REJECT

    def test_reject_rejected_rank(self):
        atom = _atom(confirmation_rank=ConfirmationRank.REJECTED)
        gate = evaluate_gate(atom, "IN", self._match(), self._call())
        assert gate.decision == GateDecision.REJECT

    def test_reject_different_domain(self):
        atom = _atom()
        gate = evaluate_gate(
            atom, "IN",
            self._match(LevelMatchStatus.DIFFERENT_DOMAIN),
            self._call(),
        )
        assert gate.decision == GateDecision.REJECT

    def test_reject_blocked_callability(self):
        atom = _atom()
        gate = evaluate_gate(
            atom, "IN", self._match(),
            self._call(CallabilityStatus.BLOCKED),
        )
        assert gate.decision == GateDecision.REJECT

    def test_suspend_unresolved_conflict(self):
        atom = _atom()
        conflict = InternalConflictRecord(
            conflict_id="ICR_test",
            atom_a_id="A", atom_b_id="B",
            conflict_type=InternalConflictType.INFO_VS_INFO,
            resolved=False,
        )
        gate = evaluate_gate(
            atom, "IN", self._match(), self._call(), conflict=conflict,
        )
        assert gate.decision == GateDecision.SUSPEND

    def test_suspend_level_mismatch(self):
        atom = _atom()
        gate = evaluate_gate(
            atom, "IN",
            self._match(LevelMatchStatus.EXCESSIVELY_BROAD),
            self._call(),
        )
        assert gate.decision == GateDecision.SUSPEND

    def test_suspend_conditional_callability(self):
        atom = _atom()
        gate = evaluate_gate(
            atom, "IN", self._match(),
            self._call(CallabilityStatus.CONDITIONAL),
        )
        assert gate.decision == GateDecision.SUSPEND

    def test_complete_under_review(self):
        atom = _atom(verification=VerificationStatus.UNDER_REVIEW)
        gate = evaluate_gate(atom, "IN", self._match(), self._call())
        assert gate.decision == GateDecision.COMPLETE

    def test_complete_unverified(self):
        atom = _atom(verification=VerificationStatus.UNVERIFIED)
        gate = evaluate_gate(atom, "IN", self._match(), self._call())
        assert gate.decision == GateDecision.COMPLETE

    def test_opinion_never_passes_as_information(self):
        """المادة 25: opinions must not pass as foundational information."""
        atom = _atom(
            entry_kind=EpistemicEntryKind.OPINION,
            verification=VerificationStatus.UNVERIFIED,
        )
        # Callability should block it
        call_result = evaluate_callability(atom, "IN")
        gate = evaluate_gate(atom, "IN", self._match(), call_result)
        assert gate.decision == GateDecision.REJECT


# ═══════════════════════════════════════════════════════════════════════
# §7.8 — End-to-end govern() tests
# ═══════════════════════════════════════════════════════════════════════


class TestGovern:
    """End-to-end ISG pipeline."""

    def test_single_valid_atom(self):
        atom = _atom(verification=VerificationStatus.VERIFIED)
        src = _source_record()
        result = govern(
            [atom], input_id="IN_001",
            input_level="token", input_domain="linguistic",
            source_records={"test_source": src},
        )
        assert isinstance(result, ISGValidationResult)
        assert result.passed >= 0
        assert result.passed + result.rejected + result.suspended + result.completing == 1

    def test_batch_mixed_results(self):
        good = _atom(atom_id="GOOD", verification=VerificationStatus.VERIFIED)
        bad = _atom(
            atom_id="BAD",
            confirmation_rank=ConfirmationRank.REJECTED,
            verification=VerificationStatus.DISQUALIFIED,
        )
        result = govern(
            [good, bad], input_id="IN_002",
            input_level="token", input_domain="linguistic",
        )
        assert result.passed + result.rejected + result.suspended + result.completing == 2

    def test_overall_ready_with_no_rejections(self):
        atom = _atom(verification=VerificationStatus.VERIFIED)
        src = _source_record()
        result = govern(
            [atom], input_id="IN_003",
            input_level="token", input_domain="linguistic",
            source_records={"test_source": src},
        )
        # If atom passes, overall_ready should be True
        if result.passed > 0 and result.rejected == 0:
            assert result.overall_ready

    def test_overall_not_ready_with_rejection(self):
        atom = _atom(
            confirmation_rank=ConfirmationRank.REJECTED,
            verification=VerificationStatus.DISQUALIFIED,
        )
        result = govern(
            [atom], input_id="IN_004",
            input_level="token", input_domain="linguistic",
        )
        assert not result.overall_ready

    def test_empty_batch(self):
        result = govern(
            [], input_id="IN_005",
            input_level="token", input_domain="linguistic",
        )
        assert result.passed == 0
        assert result.rejected == 0
        assert not result.overall_ready

    def test_gate_results_count(self):
        atoms = [_atom(atom_id=f"A_{i}") for i in range(5)]
        result = govern(
            atoms, input_id="IN_006",
            input_level="token", input_domain="linguistic",
        )
        assert len(result.gate_results) == 5

    def test_source_verification_in_govern(self):
        atom = _atom(
            atom_id="SRC_TEST",
            source="known_source",
            verification=VerificationStatus.UNVERIFIED,
        )
        src = _source_record(source_id="SR_1", transmitter="trusted")
        result = govern(
            [atom], input_id="IN_007",
            input_level="token", input_domain="linguistic",
            source_records={"known_source": src},
        )
        assert len(result.gate_results) == 1


# ═══════════════════════════════════════════════════════════════════════
# §7.9 — Opinion separation tests
# ═══════════════════════════════════════════════════════════════════════


class TestSeparateOpinions:
    """المادة 21–27: separate information from opinions."""

    def test_all_information(self):
        atoms = [_atom(entry_kind=EpistemicEntryKind.INFORMATION) for _ in range(3)]
        info, non = separate_opinions(atoms)
        assert len(info) == 3
        assert len(non) == 0

    def test_all_opinions(self):
        atoms = [
            _atom(entry_kind=EpistemicEntryKind.OPINION),
            _atom(entry_kind=EpistemicEntryKind.HYPOTHESIS),
            _atom(entry_kind=EpistemicEntryKind.ESTIMATE),
            _atom(entry_kind=EpistemicEntryKind.PRIOR_POSITION),
        ]
        info, non = separate_opinions(atoms)
        assert len(info) == 0
        assert len(non) == 4

    def test_mixed_separation(self):
        atoms = [
            _atom(atom_id="I1", entry_kind=EpistemicEntryKind.INFORMATION),
            _atom(atom_id="O1", entry_kind=EpistemicEntryKind.OPINION),
            _atom(atom_id="I2", entry_kind=EpistemicEntryKind.INFORMATION),
            _atom(atom_id="H1", entry_kind=EpistemicEntryKind.HYPOTHESIS),
        ]
        info, non = separate_opinions(atoms)
        assert len(info) == 2
        assert len(non) == 2
        assert all(a.entry_kind == EpistemicEntryKind.INFORMATION for a in info)

    def test_empty_input(self):
        info, non = separate_opinions([])
        assert len(info) == 0
        assert len(non) == 0

    def test_returns_tuples(self):
        atoms = [_atom()]
        info, non = separate_opinions(atoms)
        assert isinstance(info, tuple)
        assert isinstance(non, tuple)


# ═══════════════════════════════════════════════════════════════════════
# §7.10 — Pipeline integration test
# ═══════════════════════════════════════════════════════════════════════


class TestPipelineIntegration:
    """ISG result in the pipeline."""

    def test_pipeline_has_isg_result(self):
        from arabic_engine.pipeline import run
        result = run("كتب الرجل")
        # isg_result should be populated (not None)
        assert result.isg_result is not None
        assert isinstance(result.isg_result, ISGValidationResult)

    def test_pipeline_isg_gate_count(self):
        from arabic_engine.pipeline import run
        result = run("ذهب")
        if result.isg_result is not None:
            assert len(result.isg_result.gate_results) > 0


# ═══════════════════════════════════════════════════════════════════════
# §7.11 — Seed data tests
# ═══════════════════════════════════════════════════════════════════════


class TestSeedData:
    """Verify seed data constants."""

    def test_governance_thresholds_keys(self):
        assert "theta_0" in DEFAULT_GOVERNANCE_THRESHOLDS
        assert "theta_1" in DEFAULT_GOVERNANCE_THRESHOLDS
        assert "theta_2" in DEFAULT_GOVERNANCE_THRESHOLDS

    def test_governance_thresholds_range(self):
        for k, v in DEFAULT_GOVERNANCE_THRESHOLDS.items():
            assert 0.0 <= v <= 1.0, f"{k} out of range: {v}"

    def test_threshold_ordering(self):
        t0 = DEFAULT_GOVERNANCE_THRESHOLDS["theta_0"]
        t1 = DEFAULT_GOVERNANCE_THRESHOLDS["theta_1"]
        t2 = DEFAULT_GOVERNANCE_THRESHOLDS["theta_2"]
        assert t0 <= t1 <= t2

    def test_conflict_priority_order_non_empty(self):
        assert len(DEFAULT_CONFLICT_PRIORITY_ORDER) > 0

    def test_readiness_criteria_count(self):
        assert len(DEFAULT_READINESS_CRITERIA) == 9

    def test_readiness_criteria_unique(self):
        assert len(DEFAULT_READINESS_CRITERIA) == len(set(DEFAULT_READINESS_CRITERIA))


# ═══════════════════════════════════════════════════════════════════════
# §7.12 — Frozen dataclass tests
# ═══════════════════════════════════════════════════════════════════════


class TestFrozenTypes:
    """Verify all ISG types are frozen."""

    def test_knowledge_atom_frozen(self):
        atom = _atom()
        with pytest.raises(AttributeError):
            atom.label = "changed"  # type: ignore[misc]

    def test_source_record_frozen(self):
        src = _source_record()
        with pytest.raises(AttributeError):
            src.source_id = "changed"  # type: ignore[misc]

    def test_level_match_result_frozen(self):
        r = LevelMatchResult(atom_id="A", input_id="IN", status=LevelMatchStatus.MATCHED)
        with pytest.raises(AttributeError):
            r.status = LevelMatchStatus.WRONG_LAYER  # type: ignore[misc]

    def test_callability_result_frozen(self):
        r = CallabilityResult(
            atom_id="A", input_id="IN", status=CallabilityStatus.CALLABLE,
        )
        with pytest.raises(AttributeError):
            r.status = CallabilityStatus.BLOCKED  # type: ignore[misc]

    def test_internal_conflict_record_frozen(self):
        r = InternalConflictRecord(
            conflict_id="ICR_1", atom_a_id="A", atom_b_id="B",
            conflict_type=InternalConflictType.INFO_VS_INFO,
        )
        with pytest.raises(AttributeError):
            r.resolved = True  # type: ignore[misc]

    def test_governance_gate_result_frozen(self):
        r = GovernanceGateResult(
            atom_id="A", input_id="IN", decision=GateDecision.PASS,
        )
        with pytest.raises(AttributeError):
            r.decision = GateDecision.REJECT  # type: ignore[misc]

    def test_isg_validation_result_frozen(self):
        r = ISGValidationResult(input_id="IN")
        with pytest.raises(AttributeError):
            r.passed = 99  # type: ignore[misc]
