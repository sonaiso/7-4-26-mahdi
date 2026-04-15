"""Transform state machine — Layer 5 morphological transformation.

Priority order (lower number = preferred)::

    1. Idgham (assimilation)
    2. Illal (weakness)
    3. Substitution
    4. Deletion
    5. Augmented
    6. Original

The "original" verdict is only reached after exhausting all
transform evidence.
"""

from __future__ import annotations

from typing import Any, Dict

from arabic_engine.core.enums import LayerEvent, TransformState
from arabic_engine.core.formulas import (
    AUGMENTED_AUGMENTATION_THRESHOLD,
    AUGMENTED_DEPENDENCY_THRESHOLD,
    IDGHAM_CONFIDENCE_THRESHOLD,
    ILLAL_CONFIDENCE_THRESHOLD,
    ORIGINAL_CONSTITUTIVENESS_THRESHOLD,
    ORIGINAL_INFLECTION_STABILITY_THRESHOLD,
    SUBSTITUTION_RECOVERABILITY_THRESHOLD,
    TRANSFORM_VALIDATION_THRESHOLD,
)
from arabic_engine.core.state_machine import (
    StateMachine,
    StateMachineConfig,
    StateTransition,
)
from arabic_engine.core.types import TransformCandidate

# ── guards ──────────────────────────────────────────────────────────

_E = LayerEvent
_T = TransformState


def g_idgham(ctx: Dict[str, Any]) -> bool:
    return ctx.get("idgham_confidence", 0.0) >= IDGHAM_CONFIDENCE_THRESHOLD


def g_illal(ctx: Dict[str, Any]) -> bool:
    return ctx.get("illal_confidence", 0.0) >= ILLAL_CONFIDENCE_THRESHOLD


def g_substitution(ctx: Dict[str, Any]) -> bool:
    return (
        ctx.get("recoverability_score", 0.0) >= SUBSTITUTION_RECOVERABILITY_THRESHOLD
        and ctx.get("changed_material", False)
    )


def g_deletion(ctx: Dict[str, Any]) -> bool:
    return (
        ctx.get("surface_presence") is False
        and ctx.get("underlying_presence") is True
    )


def g_augmented(ctx: Dict[str, Any]) -> bool:
    return (
        ctx.get("dependency_score", 0.0) >= AUGMENTED_DEPENDENCY_THRESHOLD
        and ctx.get("augmentation_score", 0.0) >= AUGMENTED_AUGMENTATION_THRESHOLD
    )


def g_original(ctx: Dict[str, Any]) -> bool:
    return (
        ctx.get("constitutiveness_score", 0.0) >= ORIGINAL_CONSTITUTIVENESS_THRESHOLD
        and ctx.get("inflection_stability_score", 0.0)
        >= ORIGINAL_INFLECTION_STABILITY_THRESHOLD
    )


def g_transform_validated(ctx: Dict[str, Any]) -> bool:
    return ctx.get("transform_score", 0.0) >= TRANSFORM_VALIDATION_THRESHOLD


# ── config ──────────────────────────────────────────────────────────

TRANSFORM_TRANSITIONS = (
    # From T0 — ordered by priority (1=highest).
    StateTransition(_T.T0_NONE, _E.EV_ASSIMILATION_DETECTED, _T.T6_IDGHAM,
                    guard=g_idgham, guard_name="g_idgham",
                    threshold=IDGHAM_CONFIDENCE_THRESHOLD, priority=1),
    StateTransition(_T.T0_NONE, _E.EV_WEAKNESS_PATTERN_DETECTED, _T.T5_ILLAL,
                    guard=g_illal, guard_name="g_illal",
                    threshold=ILLAL_CONFIDENCE_THRESHOLD, priority=2),
    StateTransition(_T.T0_NONE, _E.EV_MATERIAL_CHANGED, _T.T3_SUBSTITUTION,
                    guard=g_substitution, guard_name="g_substitution",
                    threshold=SUBSTITUTION_RECOVERABILITY_THRESHOLD, priority=3),
    StateTransition(_T.T0_NONE, _E.EV_SURFACE_ABSENT, _T.T4_DELETION,
                    guard=g_deletion, guard_name="g_deletion",
                    priority=4),
    StateTransition(_T.T0_NONE, _E.EV_DEPENDENT_FUNCTIONAL, _T.T2_AUGMENT,
                    guard=g_augmented, guard_name="g_augmented",
                    threshold=AUGMENTED_DEPENDENCY_THRESHOLD, priority=5),
    StateTransition(_T.T0_NONE, _E.EV_CONSTITUTIVE_STABLE, _T.T1_ORIGINAL,
                    guard=g_original, guard_name="g_original",
                    threshold=ORIGINAL_CONSTITUTIVENESS_THRESHOLD, priority=6),
    # Validation from any candidate state.
    StateTransition(_T.T1_ORIGINAL, _E.EV_TRANSFORM_VALIDATED, _T.T7_VALIDATED,
                    guard=g_transform_validated, guard_name="g_transform_score",
                    threshold=TRANSFORM_VALIDATION_THRESHOLD, priority=1),
    StateTransition(_T.T2_AUGMENT, _E.EV_TRANSFORM_VALIDATED, _T.T7_VALIDATED,
                    guard=g_transform_validated, guard_name="g_transform_score",
                    threshold=TRANSFORM_VALIDATION_THRESHOLD, priority=1),
    StateTransition(_T.T3_SUBSTITUTION, _E.EV_TRANSFORM_VALIDATED, _T.T7_VALIDATED,
                    guard=g_transform_validated, guard_name="g_transform_score",
                    threshold=TRANSFORM_VALIDATION_THRESHOLD, priority=1),
    StateTransition(_T.T4_DELETION, _E.EV_TRANSFORM_VALIDATED, _T.T7_VALIDATED,
                    guard=g_transform_validated, guard_name="g_transform_score",
                    threshold=TRANSFORM_VALIDATION_THRESHOLD, priority=1),
    StateTransition(_T.T5_ILLAL, _E.EV_TRANSFORM_VALIDATED, _T.T7_VALIDATED,
                    guard=g_transform_validated, guard_name="g_transform_score",
                    threshold=TRANSFORM_VALIDATION_THRESHOLD, priority=1),
    StateTransition(_T.T6_IDGHAM, _E.EV_TRANSFORM_VALIDATED, _T.T7_VALIDATED,
                    guard=g_transform_validated, guard_name="g_transform_score",
                    threshold=TRANSFORM_VALIDATION_THRESHOLD, priority=1),
)

TRANSFORM_MACHINE_CONFIG = StateMachineConfig(
    name="TransformMachine",
    initial_state=_T.T0_NONE,
    transitions=TRANSFORM_TRANSITIONS,
    accept_states=frozenset({_T.T7_VALIDATED}),
    reject_states=frozenset(),  # no hard reject — stays in T0 if nothing matches
)

# Map intermediate states to TransformJudgment names.
_STATE_TO_JUDGMENT = {
    _T.T1_ORIGINAL: "ORIGINAL",
    _T.T2_AUGMENT: "AUGMENTED",
    _T.T3_SUBSTITUTION: "SUBSTITUTED",
    _T.T4_DELETION: "DELETED",
    _T.T5_ILLAL: "WEAKENED",
    _T.T6_IDGHAM: "ASSIMILATED",
}


# ── convenience wrapper ────────────────────────────────────────────


class TransformMachine:
    """Layer 5 transform machine producing :class:`TransformCandidate`."""

    def __init__(self) -> None:
        self._sm = StateMachine(TRANSFORM_MACHINE_CONFIG)

    @property
    def engine(self) -> StateMachine:
        return self._sm

    def process(self, ctx: Dict[str, Any]) -> TransformCandidate | None:
        """Evaluate all transform events and return the best candidate."""
        # Fire all candidate events — the priority system picks the best.
        candidate_events = [
            _E.EV_ASSIMILATION_DETECTED,
            _E.EV_WEAKNESS_PATTERN_DETECTED,
            _E.EV_MATERIAL_CHANGED,
            _E.EV_SURFACE_ABSENT,
            _E.EV_DEPENDENT_FUNCTIONAL,
            _E.EV_CONSTITUTIVE_STABLE,
        ]
        snap = self._sm.start(ctx)
        for ev in candidate_events:
            snap = self._sm.send(snap, ev)
            if snap.current_state != _T.T0_NONE:
                break  # first match wins (priority-ordered)

        if snap.current_state == _T.T0_NONE:
            return None

        # Determine transform type from intermediate state.
        transform_type = _STATE_TO_JUDGMENT.get(snap.current_state, "")

        # Now validate.
        snap = self._sm.send(snap, _E.EV_TRANSFORM_VALIDATED)
        if self._sm.is_accepted(snap.current_state):
            return TransformCandidate(
                candidate_id=ctx.get("candidate_id", ""),
                transform_type=transform_type,
                confidence=ctx.get("transform_score", 0.0),
                source_root_ref=ctx.get("source_root_ref", ""),
                recoverability_score=ctx.get("recoverability_score", 0.0),
            )
        return None
