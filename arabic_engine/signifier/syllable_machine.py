"""Syllable state machine — Layer 3.

Transitions::

    Y0_NONE → Y1_COLLECTING → Y2_NUCLEUS_FOUND → Y3_SHAPE_RESOLVED →
    Y4_WEIGHTED → Y5_VALIDATED

Rejection at any step leads to Y6_REJECTED.
"""

from __future__ import annotations

from typing import Any, Dict

from arabic_engine.core.enums import LayerEvent, SyllableState
from arabic_engine.core.formulas import SYLLABLE_SCORE_THRESHOLD
from arabic_engine.core.state_machine import (
    StateMachine,
    StateMachineConfig,
    StateTransition,
)
from arabic_engine.core.types import SyllableUnit

# ── constants ───────────────────────────────────────────────────────

VALID_SHAPES = frozenset({"CV", "CVC", "CVV", "CVVC", "CVCC"})

# ── guards ──────────────────────────────────────────────────────────

_E = LayerEvent
_Y = SyllableState


def g_always(_ctx: Dict[str, Any]) -> bool:
    """Unconditional guard — always passes."""
    return True


def g_nucleus(ctx: Dict[str, Any]) -> bool:
    return ctx.get("has_nucleus", False)


def g_shape(ctx: Dict[str, Any]) -> bool:
    return ctx.get("pattern_shape", "") in VALID_SHAPES


def g_weight(ctx: Dict[str, Any]) -> bool:
    return ctx.get("weight_class") is not None


def g_mci_syllable(ctx: Dict[str, Any]) -> bool:
    return ctx.get("syllable_score", 0.0) >= SYLLABLE_SCORE_THRESHOLD


def g_syllable_failed(ctx: Dict[str, Any]) -> bool:
    return ctx.get("syllable_score", 1.0) < 0.45


# ── config ──────────────────────────────────────────────────────────

SYLLABLE_TRANSITIONS = (
    StateTransition(_Y.Y0_NONE, _E.EV_PHONEME_ADDED, _Y.Y1_COLLECTING,
                    guard=g_always, guard_name="—",
                    priority=1),
    StateTransition(_Y.Y1_COLLECTING, _E.EV_NUCLEUS_DETECTED, _Y.Y2_NUCLEUS_FOUND,
                    guard=g_nucleus, guard_name="g_nucleus",
                    priority=1),
    StateTransition(_Y.Y2_NUCLEUS_FOUND, _E.EV_SHAPE_RESOLVED, _Y.Y3_SHAPE_RESOLVED,
                    guard=g_shape, guard_name="g_shape",
                    priority=1),
    StateTransition(_Y.Y3_SHAPE_RESOLVED, _E.EV_WEIGHT_COMPUTED, _Y.Y4_WEIGHTED,
                    guard=g_weight, guard_name="g_weight",
                    priority=1),
    StateTransition(_Y.Y4_WEIGHTED, _E.EV_SYLLABLE_VALIDATED, _Y.Y5_VALIDATED,
                    guard=g_mci_syllable, guard_name="g_mci_syllable",
                    threshold=SYLLABLE_SCORE_THRESHOLD, priority=1),
    # Rejection from any non-terminal state (priority 0 = highest).
    StateTransition(_Y.Y0_NONE, _E.EV_CONFIDENCE_FAILED, _Y.Y6_REJECTED,
                    guard=g_syllable_failed, guard_name="failure", priority=0),
    StateTransition(_Y.Y1_COLLECTING, _E.EV_CONFIDENCE_FAILED, _Y.Y6_REJECTED,
                    guard=g_syllable_failed, guard_name="failure", priority=0),
    StateTransition(_Y.Y2_NUCLEUS_FOUND, _E.EV_CONFIDENCE_FAILED, _Y.Y6_REJECTED,
                    guard=g_syllable_failed, guard_name="failure", priority=0),
    StateTransition(_Y.Y3_SHAPE_RESOLVED, _E.EV_CONFIDENCE_FAILED, _Y.Y6_REJECTED,
                    guard=g_syllable_failed, guard_name="failure", priority=0),
    StateTransition(_Y.Y4_WEIGHTED, _E.EV_CONFIDENCE_FAILED, _Y.Y6_REJECTED,
                    guard=g_syllable_failed, guard_name="failure", priority=0),
)

SYLLABLE_MACHINE_CONFIG = StateMachineConfig(
    name="SyllableMachine",
    initial_state=_Y.Y0_NONE,
    transitions=SYLLABLE_TRANSITIONS,
    accept_states=frozenset({_Y.Y5_VALIDATED}),
    reject_states=frozenset({_Y.Y6_REJECTED}),
)


# ── convenience wrapper ────────────────────────────────────────────


class SyllableMachine:
    """Layer 3 syllable machine that produces :class:`SyllableUnit`."""

    def __init__(self) -> None:
        self._sm = StateMachine(SYLLABLE_MACHINE_CONFIG)

    @property
    def engine(self) -> StateMachine:
        return self._sm

    def process(self, ctx: Dict[str, Any]) -> SyllableUnit | None:
        """Run the syllable pipeline and return a SyllableUnit or None."""
        events = [
            (_E.EV_PHONEME_ADDED, None),
            (_E.EV_NUCLEUS_DETECTED, None),
            (_E.EV_SHAPE_RESOLVED, None),
            (_E.EV_WEIGHT_COMPUTED, None),
            (_E.EV_SYLLABLE_VALIDATED, None),
        ]
        snap = self._sm.run_to_completion(events, initial_context=ctx)
        if self._sm.is_accepted(snap.current_state):
            return SyllableUnit(
                unit_id=ctx.get("unit_id", ""),
                pattern_shape=ctx.get("pattern_shape", ""),
                weight_class=ctx.get("weight_class", 0),
                nucleus_ref=ctx.get("nucleus_ref", ""),
                syllable_score=ctx.get("syllable_score", 0.0),
            )
        return None
