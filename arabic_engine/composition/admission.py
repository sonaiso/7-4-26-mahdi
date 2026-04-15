"""بوابات القبول — Admission gates (Articles 4–5, 64–68).

Pure functions that run all pre-composition gates on a unit and produce
an admitted or rejected :class:`CompositionUnit`.
"""

from __future__ import annotations

from arabic_engine.core.enums import (
    POS,
    AmbiguityResolution,
    CompositionGate,
    CompositionGateStatus,
    SemanticType,
)
from arabic_engine.core.types import (
    CompositionGateResult,
    CompositionUnit,
    DisambiguationRecord,
    SemanticConflictRecord,
    TransferRecord,
    TruthRecord,
)


def gate_disambiguation(unit: CompositionUnit) -> CompositionGateResult:
    """Gate 1 — check disambiguation status."""
    if unit.disambiguation is None:
        return CompositionGateResult(
            gate=CompositionGate.DISAMBIGUATION,
            status=CompositionGateStatus.PASSED,
            details="No ambiguity detected",
        )
    if unit.disambiguation.resolution != AmbiguityResolution.OPEN_PENDING:
        return CompositionGateResult(
            gate=CompositionGate.DISAMBIGUATION,
            status=CompositionGateStatus.PASSED,
            details=f"Resolved via {unit.disambiguation.resolution.name}",
        )
    return CompositionGateResult(
        gate=CompositionGate.DISAMBIGUATION,
        status=CompositionGateStatus.BLOCKED,
        details="Ambiguity unresolved",
        failure_reasons=("OPEN_PENDING ambiguity",),
    )


def gate_reference_stability(unit: CompositionUnit) -> CompositionGateResult:
    """Gate 2 — check referential stability."""
    if unit.transfer is not None and not unit.transfer.accepted:
        return CompositionGateResult(
            gate=CompositionGate.REFERENCE_STABILITY,
            status=CompositionGateStatus.BLOCKED,
            details="Transfer not validated",
            failure_reasons=("Unaccepted transfer",),
        )
    return CompositionGateResult(
        gate=CompositionGate.REFERENCE_STABILITY,
        status=CompositionGateStatus.PASSED,
        details="Reference stable",
    )


def gate_predicate_readiness(unit: CompositionUnit) -> CompositionGateResult:
    """Gate 3 — check predicate readiness."""
    if unit.conflict is not None and not unit.conflict.resolved:
        return CompositionGateResult(
            gate=CompositionGate.PREDICATE_READINESS,
            status=CompositionGateStatus.BLOCKED,
            details="Unresolved conflict",
            failure_reasons=("Conflict not resolved",),
        )
    return CompositionGateResult(
        gate=CompositionGate.PREDICATE_READINESS,
        status=CompositionGateStatus.PASSED,
        details="Predicate ready",
    )


def check_admission(
    unit_id: str,
    label: str,
    *,
    semantic_type: SemanticType = SemanticType.ENTITY,
    pos: POS = POS.UNKNOWN,
    disambiguation: DisambiguationRecord | None = None,
    conflict: SemanticConflictRecord | None = None,
    transfer: TransferRecord | None = None,
    truth: TruthRecord | None = None,
) -> CompositionUnit:
    """Run all pre-composition gates and produce an admitted/rejected unit.

    Returns a :class:`CompositionUnit` with ``admitted=True`` only if
    all three admission gates pass.
    """
    unit = CompositionUnit(
        unit_id=unit_id,
        label=label,
        semantic_type=semantic_type,
        pos=pos,
        disambiguation=disambiguation,
        conflict=conflict,
        transfer=transfer,
        truth=truth,
        admitted=False,
    )

    g1 = gate_disambiguation(unit)
    g2 = gate_reference_stability(unit)
    g3 = gate_predicate_readiness(unit)

    admitted = all(
        g.status == CompositionGateStatus.PASSED for g in (g1, g2, g3)
    )

    return CompositionUnit(
        unit_id=unit.unit_id,
        label=unit.label,
        semantic_type=unit.semantic_type,
        pos=unit.pos,
        disambiguation=unit.disambiguation,
        conflict=unit.conflict,
        transfer=unit.transfer,
        truth=unit.truth,
        admitted=admitted,
    )
