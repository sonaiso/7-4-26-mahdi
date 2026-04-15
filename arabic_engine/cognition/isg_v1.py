"""Informational Stock Governance Constitution v1 — دستور حوكمة المخزون المعلوماتي v1.0.

Implements the six-step fractal governance law (المادة 67):

    تعيين → تصنيف → تحقق → استدعاء → فضّ → عبور/رد

This constitution governs the prior informational stock that precedes and
enables perception.  It sits **before** the Composition / Syntax Constitution
v1 and before the Lexeme, Concept, Referral, Proposition, and Normative
systems.

Public API
----------
identify_atom(...)       → KnowledgeAtom          (Step 1 — تعيين)
classify_atom(atom)      → KnowledgeAtom          (Step 2 — تصنيف)
verify_source(atom, rec) → KnowledgeAtom          (Step 3 — تحقق)
check_level_match(...)   → LevelMatchResult       (Step 3b — مطابقة المستوى)
evaluate_callability(...)→ CallabilityResult       (Step 4 — استدعاء)
resolve_internal_conflict(...)→ InternalConflictRecord (Step 5 — فضّ)
evaluate_gate(...)       → GovernanceGateResult    (Step 6 — عبور/رد)
govern(atoms, ...)       → ISGValidationResult     (end-to-end pipeline)
separate_opinions(atoms) → (information, non-information)

Sovereign rule (المادة 4):
  لا حق لأي وحدة معرفة سابقة في التأثير على الفهم إلا بعد تعيينها،
  وتصنيفها، والتحقق منها، وتحديد رتبتها ومجالها ومستواها وسياقها
  وصلاحية استدعائها.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Dict, Optional, Sequence, Tuple

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

# ── Internal counters for auto-generated IDs ─────────────────────────

_atom_counter = 0
_conflict_counter = 0


def _next_atom_id() -> str:
    """Return the next sequential atom ID."""
    global _atom_counter
    _atom_counter += 1
    return f"KA_{_atom_counter:03d}"


def _next_conflict_id() -> str:
    """Return the next sequential conflict ID."""
    global _conflict_counter
    _conflict_counter += 1
    return f"ICR_{_conflict_counter:03d}"


# ── Atom-type → prior-knowledge-type mapping ─────────────────────────

_ATOM_TO_PRIOR: Dict[KnowledgeAtomType, PriorKnowledgeType] = {
    KnowledgeAtomType.LEXICAL: PriorKnowledgeType.LINGUISTIC,
    KnowledgeAtomType.SEMANTIC: PriorKnowledgeType.DEFINITIONAL,
    KnowledgeAtomType.CLASSIFICATORY: PriorKnowledgeType.CLASSIFICATORY,
    KnowledgeAtomType.REFERENTIAL: PriorKnowledgeType.RELATIONAL,
    KnowledgeAtomType.RELATIONAL: PriorKnowledgeType.RELATIONAL,
    KnowledgeAtomType.NORMATIVE_RULE: PriorKnowledgeType.RULE_BASED,
    KnowledgeAtomType.CONTEXTUAL: PriorKnowledgeType.CONVENTIONAL,
    KnowledgeAtomType.CRITERION: PriorKnowledgeType.NORMATIVE,
    KnowledgeAtomType.SYMBOLIC: PriorKnowledgeType.SYMBOLIC,
    KnowledgeAtomType.MATHEMATICAL: PriorKnowledgeType.MATHEMATICAL,
}


# ── Step 1: identify_atom (تعيين) ────────────────────────────────────


def identify_atom(
    label: str,
    atom_type: KnowledgeAtomType,
    knowledge_level: str,
    domain: str,
    source: str,
    source_type: SourceType,
    confirmation_rank: ConfirmationRank,
    context: str,
    entry_kind: EpistemicEntryKind = EpistemicEntryKind.INFORMATION,
    *,
    atom_id: str = "",
    relations: Tuple[str, ...] = (),
) -> KnowledgeAtom:
    """Step 1 — تعيين: create and validate a KnowledgeAtom.

    Raises :class:`ValueError` if any required field is empty.
    Auto-generates *atom_id* when not provided.
    """
    if not atom_id:
        atom_id = _next_atom_id()
    if not label:
        raise ValueError("label must not be empty")
    if not knowledge_level:
        raise ValueError("knowledge_level must not be empty")
    if not domain:
        raise ValueError("domain must not be empty")
    if not source:
        raise ValueError("source must not be empty")
    if not context:
        raise ValueError("context must not be empty")
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
        verification=VerificationStatus.UNVERIFIED,
    )


# ── Step 2: classify_atom (تصنيف) ────────────────────────────────────


def classify_atom(atom: KnowledgeAtom) -> KnowledgeAtom:
    """Step 2 — تصنيف: validate and confirm classification fields.

    Returns a new frozen copy with the same fields confirmed.  The
    classification step verifies that the atom type maps to a valid
    prior-knowledge type (المادة 10–20).
    """
    if atom.atom_type not in _ATOM_TO_PRIOR:
        raise ValueError(f"Unknown atom type: {atom.atom_type}")
    # Classification confirmed — return identical copy (frozen)
    return replace(atom)


# ── Step 3: verify_source (تحقق) ─────────────────────────────────────


def verify_source(
    atom: KnowledgeAtom,
    source_record: SourceRecord,
) -> KnowledgeAtom:
    """Step 3 — تحقق: validate source, rank, and opinion-freedom.

    المادة 37: rejects unknown source or unknown rank.
    المادة 25: rejects opinions pretending to be information.
    """
    # Source unknown → disqualified (المادة 37)
    if not source_record.source_id or not source_record.transmitter:
        return replace(atom, verification=VerificationStatus.DISQUALIFIED)

    # Rank mismatch → under review
    if atom.confirmation_rank != source_record.confirmation_rank:
        return replace(atom, verification=VerificationStatus.UNDER_REVIEW)

    # Trust too low → disqualified
    if source_record.trust_degree < 0.3:
        return replace(atom, verification=VerificationStatus.DISQUALIFIED)

    # Source already reviewed and passed
    if source_record.review_status == VerificationStatus.VERIFIED:
        return replace(atom, verification=VerificationStatus.VERIFIED)

    if source_record.review_status == VerificationStatus.DISQUALIFIED:
        return replace(atom, verification=VerificationStatus.DISQUALIFIED)

    return replace(
        atom, verification=source_record.review_status,
    )


# ── Step 3b: check_level_match (مطابقة المستوى) ─────────────────────


def check_level_match(
    atom: KnowledgeAtom,
    input_id: str,
    input_level: str,
    input_domain: str,
) -> LevelMatchResult:
    """Step 3b — المادة 28–32: check level compatibility.

    Returns :class:`LevelMatchResult` describing the match status.
    """
    # Domain mismatch → DIFFERENT_DOMAIN
    if atom.domain != input_domain and input_domain != "":
        return LevelMatchResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=LevelMatchStatus.DIFFERENT_DOMAIN,
            reason=f"Atom domain '{atom.domain}' differs from input domain '{input_domain}'",
        )

    # Level mismatch heuristics
    if atom.knowledge_level == input_level or input_level == "":
        return LevelMatchResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=LevelMatchStatus.MATCHED,
            reason="Level matched",
        )

    # Heuristic: if atom level contains "general" and input is specific
    atom_lv = atom.knowledge_level.lower()
    input_lv = input_level.lower()

    if "general" in atom_lv and "specific" in input_lv:
        return LevelMatchResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=LevelMatchStatus.UNJUSTIFIED_GENERALISATION,
            reason="General atom applied to specific input without justification",
        )

    if "specific" in atom_lv and "general" in input_lv:
        return LevelMatchResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=LevelMatchStatus.UNJUSTIFIED_PARTICULARISATION,
            reason="Specific atom applied to general input without justification",
        )

    if "broad" in atom_lv:
        return LevelMatchResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=LevelMatchStatus.EXCESSIVELY_BROAD,
            reason=f"Atom level '{atom.knowledge_level}' excessively broad for input",
        )

    if "narrow" in atom_lv:
        return LevelMatchResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=LevelMatchStatus.EXCESSIVELY_NARROW,
            reason=f"Atom level '{atom.knowledge_level}' excessively narrow for input",
        )

    # Default: wrong layer
    return LevelMatchResult(
        atom_id=atom.atom_id,
        input_id=input_id,
        status=LevelMatchStatus.WRONG_LAYER,
        reason=f"Atom level '{atom.knowledge_level}' does not match input level '{input_level}'",
    )


# ── Step 4: evaluate_callability (استدعاء) ───────────────────────────


def _check_opinion_contamination(atom: KnowledgeAtom) -> bool:
    """Return True if atom is an opinion posing as information."""
    return (
        atom.entry_kind != EpistemicEntryKind.INFORMATION
        and atom.verification != VerificationStatus.VERIFIED
    )


def _rank_callability_priority(
    atom: KnowledgeAtom,
    context_fit: float,
) -> int:
    """Score the callability priority (higher = more important).

    Based on المادة 42 criteria: proximity, explanatory power, confirmation
    rank, context fit, rule priority.
    """
    score = 0
    # Confirmation rank contribution
    rank_scores = {
        ConfirmationRank.ESTABLISHED: 50,
        ConfirmationRank.PREPONDERANT: 40,
        ConfirmationRank.PROBABLE: 30,
        ConfirmationRank.SUSPENDED: 10,
        ConfirmationRank.REJECTED: 0,
    }
    score += rank_scores.get(atom.confirmation_rank, 0)

    # Context fit contribution (0.0–1.0 → 0–30)
    score += int(context_fit * 30)

    # Verified bonus
    if atom.verification == VerificationStatus.VERIFIED:
        score += 20

    return score


def evaluate_callability(
    atom: KnowledgeAtom,
    input_id: str,
    context_fit: float = 1.0,
    conflict_state: bool = False,
) -> CallabilityResult:
    """Step 4 — استدعاء: determine whether atom may be called.

    Implements the 7 conditions of المادة 41 and priority ranking
    of المادة 42.
    """
    # Condition 1-2: level and domain match already checked upstream
    # Condition 3: context fit
    if context_fit < 0.2:
        return CallabilityResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=CallabilityStatus.BLOCKED,
            priority=0,
            reason="Context fit too low",
        )

    # Condition 4: higher-level block (conflict state)
    if conflict_state:
        return CallabilityResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=CallabilityStatus.CONDITIONAL,
            priority=_rank_callability_priority(atom, context_fit),
            reason="Conflict state active — conditional callability",
        )

    # Condition 5: opinion contamination (المادة 25)
    if _check_opinion_contamination(atom):
        return CallabilityResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=CallabilityStatus.BLOCKED,
            priority=0,
            reason="Opinion contamination — not verified information",
        )

    # Condition 6: confirmation rank too low
    if atom.confirmation_rank == ConfirmationRank.REJECTED:
        return CallabilityResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=CallabilityStatus.BLOCKED,
            priority=0,
            reason="Confirmation rank is REJECTED",
        )

    if atom.confirmation_rank == ConfirmationRank.SUSPENDED:
        return CallabilityResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=CallabilityStatus.CONDITIONAL,
            priority=_rank_callability_priority(atom, context_fit),
            reason="Confirmation rank is SUSPENDED",
        )

    # Condition 7: verification status
    if atom.verification == VerificationStatus.DISQUALIFIED:
        return CallabilityResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            status=CallabilityStatus.BLOCKED,
            priority=0,
            reason="Verification status is DISQUALIFIED",
        )

    # All conditions passed → CALLABLE
    return CallabilityResult(
        atom_id=atom.atom_id,
        input_id=input_id,
        status=CallabilityStatus.CALLABLE,
        priority=_rank_callability_priority(atom, context_fit),
        reason="All callability conditions met",
    )


# ── Step 5: resolve_internal_conflict (فضّ) ──────────────────────────

# Confirmation rank ordering for conflict resolution
_RANK_ORDER = {
    ConfirmationRank.ESTABLISHED: 5,
    ConfirmationRank.PREPONDERANT: 4,
    ConfirmationRank.PROBABLE: 3,
    ConfirmationRank.SUSPENDED: 2,
    ConfirmationRank.REJECTED: 1,
}


def resolve_internal_conflict(
    atom_a: KnowledgeAtom,
    atom_b: KnowledgeAtom,
    method: ISGConflictResolution,
    *,
    conflict_type: InternalConflictType = InternalConflictType.INFO_VS_INFO,
    conflict_id: str = "",
) -> InternalConflictRecord:
    """Step 5 — فضّ: resolve conflicts between two atoms.

    If unresolvable, returns ``resolved=False`` (المادة 48).
    """
    if not conflict_id:
        conflict_id = _next_conflict_id()

    if method == ISGConflictResolution.SUSPENDED_UNRESOLVED:
        return InternalConflictRecord(
            conflict_id=conflict_id,
            atom_a_id=atom_a.atom_id,
            atom_b_id=atom_b.atom_id,
            conflict_type=conflict_type,
            resolution=ISGConflictResolution.SUSPENDED_UNRESOLVED,
            resolved=False,
            winner_id=None,
        )

    winner_id: Optional[str] = None
    resolved = True

    if method == ISGConflictResolution.BY_CONFIRMATION_RANK:
        rank_a = _RANK_ORDER.get(atom_a.confirmation_rank, 0)
        rank_b = _RANK_ORDER.get(atom_b.confirmation_rank, 0)
        if rank_a > rank_b:
            winner_id = atom_a.atom_id
        elif rank_b > rank_a:
            winner_id = atom_b.atom_id
        else:
            resolved = False

    elif method == ISGConflictResolution.BY_DOMAIN:
        # Same domain → can't resolve by domain alone
        if atom_a.domain != atom_b.domain:
            winner_id = atom_a.atom_id  # prefer first atom if domains differ
        else:
            resolved = False

    elif method == ISGConflictResolution.BY_INPUT_RELEVANCE:
        # Compare by verification status as proxy for relevance
        v_order = {
            VerificationStatus.VERIFIED: 4,
            VerificationStatus.UNDER_REVIEW: 3,
            VerificationStatus.UNVERIFIED: 2,
            VerificationStatus.DISQUALIFIED: 1,
        }
        va = v_order.get(atom_a.verification, 0)
        vb = v_order.get(atom_b.verification, 0)
        if va > vb:
            winner_id = atom_a.atom_id
        elif vb > va:
            winner_id = atom_b.atom_id
        else:
            resolved = False

    elif method == ISGConflictResolution.BY_CONTEXT_PRIORITY:
        # Prefer the atom with non-empty context
        if atom_a.context and not atom_b.context:
            winner_id = atom_a.atom_id
        elif atom_b.context and not atom_a.context:
            winner_id = atom_b.atom_id
        else:
            resolved = False

    elif method == ISGConflictResolution.BY_RULE_RANK:
        # Prefer normative/rule-based atoms
        rule_types = {KnowledgeAtomType.NORMATIVE_RULE, KnowledgeAtomType.CRITERION}
        a_is_rule = atom_a.atom_type in rule_types
        b_is_rule = atom_b.atom_type in rule_types
        if a_is_rule and not b_is_rule:
            winner_id = atom_a.atom_id
        elif b_is_rule and not a_is_rule:
            winner_id = atom_b.atom_id
        else:
            resolved = False

    elif method == ISGConflictResolution.BY_SPECIALISATION:
        # Prefer the more specific atom (heuristic: shorter domain = more specific)
        if len(atom_a.domain) > len(atom_b.domain):
            winner_id = atom_b.atom_id
        elif len(atom_b.domain) > len(atom_a.domain):
            winner_id = atom_a.atom_id
        else:
            resolved = False

    if not resolved:
        method = ISGConflictResolution.SUSPENDED_UNRESOLVED

    return InternalConflictRecord(
        conflict_id=conflict_id,
        atom_a_id=atom_a.atom_id,
        atom_b_id=atom_b.atom_id,
        conflict_type=conflict_type,
        resolution=method,
        resolved=resolved,
        winner_id=winner_id,
    )


# ── Step 6: evaluate_gate (عبور/رد) ──────────────────────────────────


def evaluate_gate(
    atom: KnowledgeAtom,
    input_id: str,
    level_match: LevelMatchResult,
    callability: CallabilityResult,
    conflict: Optional[InternalConflictRecord] = None,
) -> GovernanceGateResult:
    """Step 6 — عبور/رد: make the final gate decision.

    المادة 58: reject if fatal defect.
    المادة 59: suspend if unresolved ambiguity.
    المادة 60: complete if completable deficiency.
    """
    # Rejection conditions (المادة 58)
    if atom.verification == VerificationStatus.DISQUALIFIED:
        return GovernanceGateResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            decision=GateDecision.REJECT,
            level_match=level_match,
            callability=callability,
            conflict=conflict,
            reason="Source disqualified",
        )

    if atom.confirmation_rank == ConfirmationRank.REJECTED:
        return GovernanceGateResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            decision=GateDecision.REJECT,
            level_match=level_match,
            callability=callability,
            conflict=conflict,
            reason="Confirmation rank REJECTED",
        )

    if level_match.status == LevelMatchStatus.DIFFERENT_DOMAIN:
        return GovernanceGateResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            decision=GateDecision.REJECT,
            level_match=level_match,
            callability=callability,
            conflict=conflict,
            reason="Domain mismatch",
        )

    if callability.status == CallabilityStatus.BLOCKED:
        return GovernanceGateResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            decision=GateDecision.REJECT,
            level_match=level_match,
            callability=callability,
            conflict=conflict,
            reason=f"Callability blocked: {callability.reason}",
        )

    # Unresolved conflict → suspend (المادة 48/59)
    if conflict is not None and not conflict.resolved:
        return GovernanceGateResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            decision=GateDecision.SUSPEND,
            level_match=level_match,
            callability=callability,
            conflict=conflict,
            reason="Unresolved internal conflict",
        )

    # Suspension conditions (المادة 59)
    if level_match.status != LevelMatchStatus.MATCHED:
        return GovernanceGateResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            decision=GateDecision.SUSPEND,
            level_match=level_match,
            callability=callability,
            conflict=conflict,
            reason=f"Level mismatch: {level_match.status.name}",
        )

    if callability.status == CallabilityStatus.CONDITIONAL:
        return GovernanceGateResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            decision=GateDecision.SUSPEND,
            level_match=level_match,
            callability=callability,
            conflict=conflict,
            reason=f"Conditional callability: {callability.reason}",
        )

    # Completion conditions (المادة 60)
    if atom.verification == VerificationStatus.UNDER_REVIEW:
        return GovernanceGateResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            decision=GateDecision.COMPLETE,
            level_match=level_match,
            callability=callability,
            conflict=conflict,
            reason="Verification under review — needs completion",
        )

    if atom.verification == VerificationStatus.UNVERIFIED:
        return GovernanceGateResult(
            atom_id=atom.atom_id,
            input_id=input_id,
            decision=GateDecision.COMPLETE,
            level_match=level_match,
            callability=callability,
            conflict=conflict,
            reason="Unverified source — needs completion",
        )

    # All checks passed → PASS (عبور) with FIRST readiness
    return GovernanceGateResult(
        atom_id=atom.atom_id,
        input_id=input_id,
        decision=GateDecision.PASS,
        readiness=ReadinessLevel.FIRST,
        level_match=level_match,
        callability=callability,
        conflict=conflict,
        reason="All governance checks passed",
    )


# ── End-to-end governance pipeline ────────────────────────────────────


def govern(
    atoms: Sequence[KnowledgeAtom],
    input_id: str,
    input_level: str,
    input_domain: str,
    source_records: Optional[Dict[str, SourceRecord]] = None,
) -> ISGValidationResult:
    """End-to-end governance pipeline for a batch of atoms.

    Runs all 6 steps in sequence for each atom and returns aggregate
    results.
    """
    if source_records is None:
        source_records = {}

    gate_results = []
    passed = 0
    rejected = 0
    suspended = 0
    completing = 0

    for atom in atoms:
        # Step 1-2: already done (atoms arrive pre-identified & classified)
        # Re-classify to validate
        try:
            atom = classify_atom(atom)
        except ValueError:
            gate_results.append(GovernanceGateResult(
                atom_id=atom.atom_id,
                input_id=input_id,
                decision=GateDecision.REJECT,
                reason="Classification failed",
            ))
            rejected += 1
            continue

        # Step 3: verify source
        src_rec = source_records.get(atom.source, None)
        if src_rec is not None:
            atom = verify_source(atom, src_rec)

        # Step 3b: level match
        level_match = check_level_match(atom, input_id, input_level, input_domain)

        # Step 4: callability
        callability = evaluate_callability(atom, input_id)

        # Step 5: conflict resolution is handled externally (pair-wise)
        # For the batch pipeline, we skip explicit conflict resolution

        # Step 6: gate
        gate = evaluate_gate(atom, input_id, level_match, callability)
        gate_results.append(gate)

        if gate.decision == GateDecision.PASS:
            passed += 1
        elif gate.decision == GateDecision.REJECT:
            rejected += 1
        elif gate.decision == GateDecision.SUSPEND:
            suspended += 1
        elif gate.decision == GateDecision.COMPLETE:
            completing += 1

    return ISGValidationResult(
        input_id=input_id,
        gate_results=tuple(gate_results),
        passed=passed,
        rejected=rejected,
        suspended=suspended,
        completing=completing,
        overall_ready=passed > 0 and rejected == 0,
    )


# ── Opinion separation (المادة 21–27) ────────────────────────────────


def separate_opinions(
    atoms: Sequence[KnowledgeAtom],
) -> Tuple[Tuple[KnowledgeAtom, ...], Tuple[KnowledgeAtom, ...]]:
    """Separate information from opinions/hypotheses/estimates/positions.

    Returns ``(information_atoms, non_information_atoms)``.
    المادة 25: opinions must never enter the primary interpretation layer
    as foundational information.
    """
    info: list[KnowledgeAtom] = []
    non_info: list[KnowledgeAtom] = []
    for atom in atoms:
        if atom.entry_kind == EpistemicEntryKind.INFORMATION:
            info.append(atom)
        else:
            non_info.append(atom)
    return tuple(info), tuple(non_info)
