"""Numeric formulas for rank scoring and final approval.

This module contains the two key weighted-sum equations used by the
layer pipeline:

1. **RankScore** (Layer 4 — root-rank machine)::

       RankScore = 0.30·P + 0.25·C + 0.20·I + 0.15·S + 0.10·R

2. **FinalApproval** (Layer 6 — judgment machine)::

       FinalApproval = 0.40·J + 0.35·R + 0.15·Rec + 0.10·T

It also defines the numeric *thresholds* referenced by every layer
machine's guard functions.
"""

from __future__ import annotations

from .types import FinalApprovalComponents, RankScoreComponents

# ── RankScore weights ───────────────────────────────────────────────

POSITION_FIT_WEIGHT: float = 0.30
CONSTITUTIVENESS_WEIGHT: float = 0.25
INFLECTION_STABILITY_WEIGHT: float = 0.20
SYLLABLE_COMPATIBILITY_WEIGHT: float = 0.15
RECOVERABILITY_WEIGHT: float = 0.10

# ── FinalApproval weights ──────────────────────────────────────────

JUDGMENT_SCORE_WEIGHT: float = 0.40
REALITY_MATCH_WEIGHT: float = 0.35
RECOVERABILITY_FA_WEIGHT: float = 0.15
TRACE_CLARITY_WEIGHT: float = 0.10

# ── layer thresholds ───────────────────────────────────────────────

ENERGY_THRESHOLD: float = 0.30
BOUNDARY_THRESHOLD: float = 0.55
COHESION_THRESHOLD: float = 0.60
UNITY_THRESHOLD: float = 0.65
MCI_THRESHOLD: float = 0.65
SONORITY_THRESHOLD: float = 0.50
MOBILITY_THRESHOLD: float = 0.55
SYLLABLE_SCORE_THRESHOLD: float = 0.65
ROOT_FITNESS_THRESHOLD: float = 0.60
RANK_SCORE_THRESHOLD: float = 0.65
RANK_AMBIGUITY_THRESHOLD: float = 0.05
TRANSFORM_CONFIDENCE_THRESHOLD: float = 0.65
TRANSFORM_VALIDATION_THRESHOLD: float = 0.70
JUDGMENT_SCORE_THRESHOLD: float = 0.70
EVIDENCE_STRENGTH_THRESHOLD: float = 0.60
VALIDATION_SCORE_THRESHOLD: float = 0.75
FINAL_APPROVAL_THRESHOLD: float = 0.75

# original threshold (constitutiveness / inflection stability)
ORIGINAL_CONSTITUTIVENESS_THRESHOLD: float = 0.70
ORIGINAL_INFLECTION_STABILITY_THRESHOLD: float = 0.70

# augmented threshold
AUGMENTED_DEPENDENCY_THRESHOLD: float = 0.60
AUGMENTED_AUGMENTATION_THRESHOLD: float = 0.60

# substituted threshold
SUBSTITUTION_RECOVERABILITY_THRESHOLD: float = 0.60

# illal / idgham thresholds
ILLAL_CONFIDENCE_THRESHOLD: float = 0.65
IDGHAM_CONFIDENCE_THRESHOLD: float = 0.65


# ── public API ──────────────────────────────────────────────────────


def compute_rank_score(components: RankScoreComponents) -> float:
    """Compute the weighted root-rank score."""
    return (
        POSITION_FIT_WEIGHT * components.position_fit
        + CONSTITUTIVENESS_WEIGHT * components.constitutiveness
        + INFLECTION_STABILITY_WEIGHT * components.inflection_stability
        + SYLLABLE_COMPATIBILITY_WEIGHT * components.syllable_compatibility
        + RECOVERABILITY_WEIGHT * components.recoverability
    )


def compute_final_approval(components: FinalApprovalComponents) -> float:
    """Compute the weighted final-approval score."""
    return (
        JUDGMENT_SCORE_WEIGHT * components.judgment_score
        + REALITY_MATCH_WEIGHT * components.reality_match_score
        + RECOVERABILITY_FA_WEIGHT * components.recoverability_score
        + TRACE_CLARITY_WEIGHT * components.trace_clarity
    )


def is_approved(final_approval: float) -> bool:
    """Return True if the final-approval score meets the threshold."""
    return final_approval >= FINAL_APPROVAL_THRESHOLD
