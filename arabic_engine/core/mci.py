"""Minimum-Completeness Index (MCI) computation.

The MCI aggregates six sub-scores into a single float that determines
whether a phonological unit is *complete enough* for structural analysis.

Formula::

    MCI = (1.2·B + 1.5·U + 1.3·C + 0.8·E + 1.0·P + 1.2·O) / 7.0

Decision thresholds::

    < 0.45         → REJECTED
    0.45 .. <0.65  → SUSPENDED (re-inspect)
    0.65 .. <0.80  → ANALYTICALLY_ACCEPTED (minimum)
    ≥ 0.80         → DIRECTLY_ACCEPTED (strong)
"""

from __future__ import annotations

from .enums import MCIDecision
from .types import MCIResult, MCIScores

# ── weights ─────────────────────────────────────────────────────────

B_WEIGHT: float = 1.2   # Boundary
U_WEIGHT: float = 1.5   # Unity
C_WEIGHT: float = 1.3   # Cohesion
E_WEIGHT: float = 0.8   # Extension
P_WEIGHT: float = 1.0   # Phase Order
O_WEIGHT: float = 1.2   # Orderliness
TOTAL_WEIGHT: float = 7.0

# ── thresholds ──────────────────────────────────────────────────────

MCI_REJECT_THRESHOLD: float = 0.45
MCI_SUSPEND_THRESHOLD: float = 0.65
MCI_ACCEPT_THRESHOLD: float = 0.80


# ── public API ──────────────────────────────────────────────────────


def compute_mci(scores: MCIScores) -> float:
    """Return the raw MCI value for the given sub-scores."""
    numerator = (
        B_WEIGHT * scores.boundary
        + U_WEIGHT * scores.unity
        + C_WEIGHT * scores.cohesion
        + E_WEIGHT * scores.extension
        + P_WEIGHT * scores.phase_order
        + O_WEIGHT * scores.orderliness
    )
    return numerator / TOTAL_WEIGHT


def classify_mci(mci: float) -> MCIDecision:
    """Map an MCI value to a categorical decision."""
    if mci < MCI_REJECT_THRESHOLD:
        return MCIDecision.REJECTED
    if mci < MCI_SUSPEND_THRESHOLD:
        return MCIDecision.SUSPENDED
    if mci < MCI_ACCEPT_THRESHOLD:
        return MCIDecision.ANALYTICALLY_ACCEPTED
    return MCIDecision.DIRECTLY_ACCEPTED


def evaluate_mci(scores: MCIScores) -> MCIResult:
    """Compute MCI and return a full :class:`MCIResult`."""
    value = compute_mci(scores)
    decision = classify_mci(value)
    return MCIResult(
        scores=scores,
        mci_value=value,
        decision=decision.name,
    )
