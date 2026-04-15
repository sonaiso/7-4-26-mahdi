"""بوابات التركيب — All 8 composition gates (Articles 64–72).

Pure functions implementing each gate of the composition pipeline.
Each gate returns a :class:`CompositionGateResult` indicating whether
the composition may proceed.
"""

from __future__ import annotations

from arabic_engine.core.enums import (
    AmbiguityResolution,
    CompositionGate,
    CompositionGateStatus,
    RoleStatus,
)
from arabic_engine.core.types import (
    CompositionGateResult,
    CompositionProposition,
    CompositionRelation,
    CompositionRole,
    CompositionUnit,
    InterPropositionLink,
    SemanticConflictRecord,
)


def gate_disambiguation(
    units: tuple[CompositionUnit, ...],
) -> CompositionGateResult:
    """Gate 1 — all units must have resolved ambiguity."""
    blocked = [
        u.unit_id
        for u in units
        if u.disambiguation is not None
        and u.disambiguation.resolution == AmbiguityResolution.OPEN_PENDING
    ]
    if blocked:
        return CompositionGateResult(
            gate=CompositionGate.DISAMBIGUATION,
            status=CompositionGateStatus.BLOCKED,
            details=f"Unresolved ambiguity in {len(blocked)} unit(s)",
            failure_reasons=tuple(blocked),
        )
    return CompositionGateResult(
        gate=CompositionGate.DISAMBIGUATION,
        status=CompositionGateStatus.PASSED,
        details="All units disambiguated",
    )


def gate_reference_stability(
    units: tuple[CompositionUnit, ...],
) -> CompositionGateResult:
    """Gate 2 — all transfers must be accepted."""
    blocked = [
        u.unit_id
        for u in units
        if u.transfer is not None and not u.transfer.accepted
    ]
    if blocked:
        return CompositionGateResult(
            gate=CompositionGate.REFERENCE_STABILITY,
            status=CompositionGateStatus.BLOCKED,
            details=f"Unstable reference in {len(blocked)} unit(s)",
            failure_reasons=tuple(blocked),
        )
    return CompositionGateResult(
        gate=CompositionGate.REFERENCE_STABILITY,
        status=CompositionGateStatus.PASSED,
        details="All references stable",
    )


def gate_predicate_readiness(
    units: tuple[CompositionUnit, ...],
) -> CompositionGateResult:
    """Gate 3 — all conflicts must be resolved."""
    blocked = [
        u.unit_id
        for u in units
        if u.conflict is not None and not u.conflict.resolved
    ]
    if blocked:
        return CompositionGateResult(
            gate=CompositionGate.PREDICATE_READINESS,
            status=CompositionGateStatus.BLOCKED,
            details=f"Unresolved conflict in {len(blocked)} unit(s)",
            failure_reasons=tuple(blocked),
        )
    return CompositionGateResult(
        gate=CompositionGate.PREDICATE_READINESS,
        status=CompositionGateStatus.PASSED,
        details="All predicates ready",
    )


def gate_role_assignment(
    roles: tuple[CompositionRole, ...],
) -> CompositionGateResult:
    """Gate 4 — at least one role must be realized."""
    if not roles:
        return CompositionGateResult(
            gate=CompositionGate.ROLE_ASSIGNMENT,
            status=CompositionGateStatus.INSUFFICIENT_DATA,
            details="No roles assigned",
            failure_reasons=("No roles",),
        )
    realized = [r for r in roles if r.status == RoleStatus.REALIZED]
    if not realized:
        return CompositionGateResult(
            gate=CompositionGate.ROLE_ASSIGNMENT,
            status=CompositionGateStatus.BLOCKED,
            details="No realized roles",
            failure_reasons=("All roles are CANDIDATE",),
        )
    return CompositionGateResult(
        gate=CompositionGate.ROLE_ASSIGNMENT,
        status=CompositionGateStatus.PASSED,
        details=f"{len(realized)} role(s) realized",
    )


def gate_relation_validity(
    relations: tuple[CompositionRelation, ...],
) -> CompositionGateResult:
    """Gate 5 — all relations must have positive confidence."""
    if not relations:
        return CompositionGateResult(
            gate=CompositionGate.RELATION_VALIDITY,
            status=CompositionGateStatus.PASSED,
            details="No relations to validate",
        )
    invalid = [r.relation_id for r in relations if r.confidence <= 0.0]
    if invalid:
        return CompositionGateResult(
            gate=CompositionGate.RELATION_VALIDITY,
            status=CompositionGateStatus.BLOCKED,
            details=f"{len(invalid)} invalid relation(s)",
            failure_reasons=tuple(invalid),
        )
    return CompositionGateResult(
        gate=CompositionGate.RELATION_VALIDITY,
        status=CompositionGateStatus.PASSED,
        details="All relations valid",
    )


def gate_conflict_resolution(
    conflicts: tuple[SemanticConflictRecord, ...],
) -> CompositionGateResult:
    """Gate 6 — all conflicts must be resolved."""
    if not conflicts:
        return CompositionGateResult(
            gate=CompositionGate.CONFLICT_RESOLUTION,
            status=CompositionGateStatus.PASSED,
            details="No conflicts",
        )
    unresolved = [c.unit_id for c in conflicts if not c.resolved]
    if unresolved:
        return CompositionGateResult(
            gate=CompositionGate.CONFLICT_RESOLUTION,
            status=CompositionGateStatus.BLOCKED,
            details=f"{len(unresolved)} unresolved conflict(s)",
            failure_reasons=tuple(unresolved),
        )
    return CompositionGateResult(
        gate=CompositionGate.CONFLICT_RESOLUTION,
        status=CompositionGateStatus.PASSED,
        details="All conflicts resolved",
    )


def gate_proposition_closure(
    proposition: CompositionProposition | None,
) -> CompositionGateResult:
    """Gate 7 — proposition must be closed."""
    if proposition is None:
        return CompositionGateResult(
            gate=CompositionGate.PROPOSITION_CLOSURE,
            status=CompositionGateStatus.INSUFFICIENT_DATA,
            details="No proposition",
            failure_reasons=("No proposition provided",),
        )
    if not proposition.closed:
        return CompositionGateResult(
            gate=CompositionGate.PROPOSITION_CLOSURE,
            status=CompositionGateStatus.BLOCKED,
            details="Proposition not closed",
            failure_reasons=("Proposition closure conditions not met",),
        )
    return CompositionGateResult(
        gate=CompositionGate.PROPOSITION_CLOSURE,
        status=CompositionGateStatus.PASSED,
        details="Proposition closed",
    )


def gate_inter_proposition_link(
    links: tuple[InterPropositionLink, ...],
) -> CompositionGateResult:
    """Gate 8 — all inter-proposition links must be valid."""
    if not links:
        return CompositionGateResult(
            gate=CompositionGate.INTER_PROPOSITION_LINK,
            status=CompositionGateStatus.PASSED,
            details="No inter-proposition links",
        )
    invalid = [
        f"{lnk.source_prop_id}->{lnk.target_prop_id}"
        for lnk in links
        if not lnk.valid
    ]
    if invalid:
        return CompositionGateResult(
            gate=CompositionGate.INTER_PROPOSITION_LINK,
            status=CompositionGateStatus.BLOCKED,
            details=f"{len(invalid)} invalid link(s)",
            failure_reasons=tuple(invalid),
        )
    return CompositionGateResult(
        gate=CompositionGate.INTER_PROPOSITION_LINK,
        status=CompositionGateStatus.PASSED,
        details="All links valid",
    )


def run_all_gates(
    units: tuple[CompositionUnit, ...],
    roles: tuple[CompositionRole, ...],
    relations: tuple[CompositionRelation, ...],
    conflicts: tuple[SemanticConflictRecord, ...],
    proposition: CompositionProposition | None,
    links: tuple[InterPropositionLink, ...],
) -> tuple[CompositionGateResult, ...]:
    """Run all 8 composition gates and return results."""
    return (
        gate_disambiguation(units),
        gate_reference_stability(units),
        gate_predicate_readiness(units),
        gate_role_assignment(roles),
        gate_relation_validity(relations),
        gate_conflict_resolution(conflicts),
        gate_proposition_closure(proposition),
        gate_inter_proposition_link(links),
    )
