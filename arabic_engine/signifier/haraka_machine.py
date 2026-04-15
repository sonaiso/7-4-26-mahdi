"""Haraka (vowel-mark) state machine — Layer 2.5.

Transitions::

    H0_UNKNOWN → H1_CANDIDATE → H2_ATTACHED → H3_OPERATIONAL
    H3_OPERATIONAL → H4_LENGTHENED  (optional)

Any state may fall to H5_DELETED or H6_REJECTED.
"""

from __future__ import annotations

from typing import Any, Dict

from arabic_engine.core.enums import HarakaState, LayerEvent
from arabic_engine.core.formulas import MOBILITY_THRESHOLD, SONORITY_THRESHOLD
from arabic_engine.core.state_machine import (
    StateMachine,
    StateMachineConfig,
    StateTransition,
)
from arabic_engine.core.types import HarakaUnit

# ── guards ──────────────────────────────────────────────────────────

_E = LayerEvent
_H = HarakaState


def g_vocalic(ctx: Dict[str, Any]) -> bool:
    return ctx.get("sonority_score", 0.0) >= SONORITY_THRESHOLD


def g_attach(ctx: Dict[str, Any]) -> bool:
    return ctx.get("attachment_target") is not None


def g_operational(ctx: Dict[str, Any]) -> bool:
    return ctx.get("mobility_score", 0.0) >= MOBILITY_THRESHOLD


def g_length(ctx: Dict[str, Any]) -> bool:
    duration = ctx.get("duration", 0.0)
    long_min = ctx.get("long_min", 1.0)
    return duration >= long_min


def g_haraka_deleted(ctx: Dict[str, Any]) -> bool:
    return ctx.get("haraka_deleted", False)


def g_haraka_invalid(ctx: Dict[str, Any]) -> bool:
    return ctx.get("haraka_invalid", False)


# ── config ──────────────────────────────────────────────────────────

HARAKA_TRANSITIONS = (
    StateTransition(_H.H0_UNKNOWN, _E.EV_VOCALIC_TRACE_FOUND, _H.H1_CANDIDATE,
                    guard=g_vocalic, guard_name="g_vocalic",
                    threshold=SONORITY_THRESHOLD, priority=1),
    StateTransition(_H.H1_CANDIDATE, _E.EV_ATTACHED_TO_PHONEME, _H.H2_ATTACHED,
                    guard=g_attach, guard_name="g_attach",
                    threshold=0.0, priority=1),
    StateTransition(_H.H2_ATTACHED, _E.EV_SYLLABLE_ROLE_CONFIRMED, _H.H3_OPERATIONAL,
                    guard=g_operational, guard_name="g_operational",
                    threshold=MOBILITY_THRESHOLD, priority=1),
    StateTransition(_H.H3_OPERATIONAL, _E.EV_LENGTHENING_DETECTED, _H.H4_LENGTHENED,
                    guard=g_length, guard_name="g_length",
                    threshold=0.0, priority=2),
    # Deletion from any non-terminal state.
    StateTransition(_H.H0_UNKNOWN, _E.EV_HARAKA_DELETED, _H.H5_DELETED,
                    guard=g_haraka_deleted, guard_name="g_deleted", priority=1),
    StateTransition(_H.H1_CANDIDATE, _E.EV_HARAKA_DELETED, _H.H5_DELETED,
                    guard=g_haraka_deleted, guard_name="g_deleted", priority=1),
    StateTransition(_H.H2_ATTACHED, _E.EV_HARAKA_DELETED, _H.H5_DELETED,
                    guard=g_haraka_deleted, guard_name="g_deleted", priority=1),
    StateTransition(_H.H3_OPERATIONAL, _E.EV_HARAKA_DELETED, _H.H5_DELETED,
                    guard=g_haraka_deleted, guard_name="g_deleted", priority=1),
    # Rejection from any non-terminal state.
    StateTransition(_H.H0_UNKNOWN, _E.EV_HARAKA_INVALID, _H.H6_REJECTED,
                    guard=g_haraka_invalid, guard_name="g_invalid", priority=0),
    StateTransition(_H.H1_CANDIDATE, _E.EV_HARAKA_INVALID, _H.H6_REJECTED,
                    guard=g_haraka_invalid, guard_name="g_invalid", priority=0),
    StateTransition(_H.H2_ATTACHED, _E.EV_HARAKA_INVALID, _H.H6_REJECTED,
                    guard=g_haraka_invalid, guard_name="g_invalid", priority=0),
    StateTransition(_H.H3_OPERATIONAL, _E.EV_HARAKA_INVALID, _H.H6_REJECTED,
                    guard=g_haraka_invalid, guard_name="g_invalid", priority=0),
)

HARAKA_MACHINE_CONFIG = StateMachineConfig(
    name="HarakaMachine",
    initial_state=_H.H0_UNKNOWN,
    transitions=HARAKA_TRANSITIONS,
    accept_states=frozenset({_H.H4_LENGTHENED}),
    reject_states=frozenset({_H.H5_DELETED, _H.H6_REJECTED}),
)


# ── convenience wrapper ────────────────────────────────────────────


class HarakaMachine:
    """Layer 2.5 haraka machine that produces :class:`HarakaUnit`."""

    def __init__(self) -> None:
        self._sm = StateMachine(HARAKA_MACHINE_CONFIG)

    @property
    def engine(self) -> StateMachine:
        return self._sm

    def process(self, ctx: Dict[str, Any]) -> HarakaUnit | None:
        """Run the haraka pipeline and return a HarakaUnit or None."""
        snap = self._sm.start(ctx)

        # Drive through the core states.
        snap = self._sm.send(snap, _E.EV_VOCALIC_TRACE_FOUND)
        snap = self._sm.send(snap, _E.EV_ATTACHED_TO_PHONEME)
        snap = self._sm.send(snap, _E.EV_SYLLABLE_ROLE_CONFIRMED)

        # Optionally advance to lengthened (H3 → H4).
        if snap.current_state == _H.H3_OPERATIONAL:
            snap = self._sm.send(snap, _E.EV_LENGTHENING_DETECTED)

        if self._sm.is_accepted(snap.current_state) or snap.current_state == _H.H3_OPERATIONAL:
            return HarakaUnit(
                unit_id=ctx.get("unit_id", ""),
                sonority_score=ctx.get("sonority_score", 0.0),
                attachment_target=ctx.get("attachment_target"),
                mobility_score=ctx.get("mobility_score", 0.0),
                is_lengthened=(snap.current_state == _H.H4_LENGTHENED),
                is_deleted=False,
            )
        return None
