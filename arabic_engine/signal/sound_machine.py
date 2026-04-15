"""Sound state machine — Layer 1/2 phonetic detection pipeline.

Transitions::

    S0_UNOBSERVED → S1_DETECTED → S2_BOUNDED → S3_SEGMENTED →
    S4_COHERENT → S5_STABLE_UNIT

Any state may fall to S6_REJECTED on confidence failure.
"""

from __future__ import annotations

from typing import Any, Dict

from arabic_engine.core.enums import LayerEvent, SoundState
from arabic_engine.core.formulas import (
    BOUNDARY_THRESHOLD,
    COHESION_THRESHOLD,
    ENERGY_THRESHOLD,
    MCI_THRESHOLD,
    UNITY_THRESHOLD,
)
from arabic_engine.core.mci import compute_mci
from arabic_engine.core.state_machine import (
    StateMachine,
    StateMachineConfig,
    StateTransition,
)
from arabic_engine.core.types import MCIScores, PhoneticEvent

# ── guards ──────────────────────────────────────────────────────────


def g_energy(ctx: Dict[str, Any]) -> bool:
    return ctx.get("energy", 0.0) > ENERGY_THRESHOLD


def g_boundary(ctx: Dict[str, Any]) -> bool:
    return ctx.get("boundary_score", 0.0) >= BOUNDARY_THRESHOLD


def g_segmentation(ctx: Dict[str, Any]) -> bool:
    return ctx.get("phase_count", 0) >= 1


def g_cohesion(ctx: Dict[str, Any]) -> bool:
    return ctx.get("cohesion_score", 0.0) >= COHESION_THRESHOLD


def g_unity_and_mci(ctx: Dict[str, Any]) -> bool:
    if ctx.get("unity_score", 0.0) < UNITY_THRESHOLD:
        return False
    scores = ctx.get("mci_scores")
    if scores is None:
        return False
    if isinstance(scores, dict):
        scores = MCIScores(**scores)
    return compute_mci(scores) >= MCI_THRESHOLD


def g_confidence_failed(ctx: Dict[str, Any]) -> bool:
    return ctx.get("confidence_failed", False)


# ── config ──────────────────────────────────────────────────────────

_E = LayerEvent
_S = SoundState

SOUND_TRANSITIONS = (
    StateTransition(_S.S0_UNOBSERVED, _E.EV_SIGNAL_DETECTED, _S.S1_DETECTED,
                    guard=g_energy, guard_name="g_energy",
                    threshold=ENERGY_THRESHOLD, priority=1),
    StateTransition(_S.S1_DETECTED, _E.EV_BOUNDARY_CONFIRMED, _S.S2_BOUNDED,
                    guard=g_boundary, guard_name="g_boundary",
                    threshold=BOUNDARY_THRESHOLD, priority=1),
    StateTransition(_S.S2_BOUNDED, _E.EV_PHASE_SEGMENTED, _S.S3_SEGMENTED,
                    guard=g_segmentation, guard_name="g_segmentation",
                    threshold=1.0, priority=1),
    StateTransition(_S.S3_SEGMENTED, _E.EV_COHESION_PASSED, _S.S4_COHERENT,
                    guard=g_cohesion, guard_name="g_cohesion",
                    threshold=COHESION_THRESHOLD, priority=1),
    StateTransition(_S.S4_COHERENT, _E.EV_UNITY_PASSED, _S.S5_STABLE_UNIT,
                    guard=g_unity_and_mci, guard_name="g_unity+g_mci",
                    threshold=UNITY_THRESHOLD, priority=1),
    # Global rejection (priority 0 = highest).
    StateTransition(_S.S0_UNOBSERVED, _E.EV_CONFIDENCE_FAILED, _S.S6_REJECTED,
                    guard=g_confidence_failed, guard_name="confidence_fail",
                    priority=0),
    StateTransition(_S.S1_DETECTED, _E.EV_CONFIDENCE_FAILED, _S.S6_REJECTED,
                    guard=g_confidence_failed, guard_name="confidence_fail",
                    priority=0),
    StateTransition(_S.S2_BOUNDED, _E.EV_CONFIDENCE_FAILED, _S.S6_REJECTED,
                    guard=g_confidence_failed, guard_name="confidence_fail",
                    priority=0),
    StateTransition(_S.S3_SEGMENTED, _E.EV_CONFIDENCE_FAILED, _S.S6_REJECTED,
                    guard=g_confidence_failed, guard_name="confidence_fail",
                    priority=0),
    StateTransition(_S.S4_COHERENT, _E.EV_CONFIDENCE_FAILED, _S.S6_REJECTED,
                    guard=g_confidence_failed, guard_name="confidence_fail",
                    priority=0),
)

SOUND_MACHINE_CONFIG = StateMachineConfig(
    name="SoundMachine",
    initial_state=_S.S0_UNOBSERVED,
    transitions=SOUND_TRANSITIONS,
    accept_states=frozenset({_S.S5_STABLE_UNIT}),
    reject_states=frozenset({_S.S6_REJECTED}),
)


# ── convenience wrapper ────────────────────────────────────────────


class SoundMachine:
    """Layer 1–2 sound machine that produces :class:`PhoneticEvent`."""

    def __init__(self) -> None:
        self._sm = StateMachine(SOUND_MACHINE_CONFIG)

    @property
    def engine(self) -> StateMachine:
        return self._sm

    def process(self, ctx: Dict[str, Any]) -> PhoneticEvent | None:
        """Run the full sound pipeline and return a PhoneticEvent or None."""
        events = [
            (_E.EV_SIGNAL_DETECTED, None),
            (_E.EV_BOUNDARY_CONFIRMED, None),
            (_E.EV_PHASE_SEGMENTED, None),
            (_E.EV_COHESION_PASSED, None),
            (_E.EV_UNITY_PASSED, None),
        ]
        snap = self._sm.run_to_completion(events, initial_context=ctx)
        if self._sm.is_accepted(snap.current_state):
            return PhoneticEvent(
                event_id=ctx.get("event_id", ""),
                energy=ctx.get("energy", 0.0),
                boundary_score=ctx.get("boundary_score", 0.0),
                position=ctx.get("position", 0),
                interception_type=ctx.get("interception_type", ""),
            )
        return None
