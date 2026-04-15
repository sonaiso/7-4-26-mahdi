"""Final judgment state machine — Layer 6.

Transitions::

    J0_NONE → J1_NOMINATED → J2_SCORED → J3_REALITY_CHECKED →
                  J4_APPROVED  |  J5_REJECTED

Any state may move to J6_DEFERRED on insufficient evidence.

Approval formula::

    FinalApproval = 0.40·J + 0.35·R + 0.15·Rec + 0.10·T   (≥ 0.75)
"""

from __future__ import annotations

from typing import Any, Dict

from arabic_engine.core.enums import JudgmentState, LayerEvent
from arabic_engine.core.formulas import (
    EVIDENCE_STRENGTH_THRESHOLD,
    JUDGMENT_SCORE_THRESHOLD,
    VALIDATION_SCORE_THRESHOLD,
    compute_final_approval,
    is_approved,
)
from arabic_engine.core.state_machine import (
    StateMachine,
    StateMachineConfig,
    StateTransition,
)
from arabic_engine.core.types import FinalApprovalComponents, ValidatedJudgment

# ── guards ──────────────────────────────────────────────────────────

_E = LayerEvent
_J = JudgmentState


def g_always(_ctx: Dict[str, Any]) -> bool:
    return True


def g_score(ctx: Dict[str, Any]) -> bool:
    return ctx.get("judgment_score", 0.0) >= JUDGMENT_SCORE_THRESHOLD


def g_evidence(ctx: Dict[str, Any]) -> bool:
    return ctx.get("evidence_strength", 0.0) >= EVIDENCE_STRENGTH_THRESHOLD


def g_validation(ctx: Dict[str, Any]) -> bool:
    return ctx.get("validation_score", 0.0) >= VALIDATION_SCORE_THRESHOLD


def g_validation_failed(ctx: Dict[str, Any]) -> bool:
    return ctx.get("validation_score", 0.0) < VALIDATION_SCORE_THRESHOLD


def g_insufficient(ctx: Dict[str, Any]) -> bool:
    return ctx.get("insufficient_evidence", False)


# ── config ──────────────────────────────────────────────────────────

JUDGMENT_TRANSITIONS = (
    StateTransition(_J.J0_NONE, _E.EV_JUDGMENT_NOMINATED, _J.J1_NOMINATED,
                    guard=g_always, guard_name="—",
                    priority=1),
    StateTransition(_J.J1_NOMINATED, _E.EV_SCORE_COMPUTED, _J.J2_SCORED,
                    guard=g_score, guard_name="g_score",
                    threshold=JUDGMENT_SCORE_THRESHOLD, priority=1),
    StateTransition(_J.J2_SCORED, _E.EV_REALITY_EVIDENCE_FOUND, _J.J3_REALITY_CHECKED,
                    guard=g_evidence, guard_name="g_evidence",
                    threshold=EVIDENCE_STRENGTH_THRESHOLD, priority=1),
    StateTransition(_J.J3_REALITY_CHECKED, _E.EV_REALITY_MATCH_PASSED, _J.J4_APPROVED,
                    guard=g_validation, guard_name="g_validation",
                    threshold=VALIDATION_SCORE_THRESHOLD, priority=1),
    StateTransition(_J.J3_REALITY_CHECKED, _E.EV_REALITY_MATCH_FAILED, _J.J5_REJECTED,
                    guard=g_validation_failed, guard_name="—",
                    priority=0),
    # Insufficient evidence from any state.
    StateTransition(_J.J0_NONE, _E.EV_INSUFFICIENT_EVIDENCE, _J.J6_DEFERRED,
                    guard=g_insufficient, guard_name="—", priority=0),
    StateTransition(_J.J1_NOMINATED, _E.EV_INSUFFICIENT_EVIDENCE, _J.J6_DEFERRED,
                    guard=g_insufficient, guard_name="—", priority=0),
    StateTransition(_J.J2_SCORED, _E.EV_INSUFFICIENT_EVIDENCE, _J.J6_DEFERRED,
                    guard=g_insufficient, guard_name="—", priority=0),
    StateTransition(_J.J3_REALITY_CHECKED, _E.EV_INSUFFICIENT_EVIDENCE, _J.J6_DEFERRED,
                    guard=g_insufficient, guard_name="—", priority=0),
)

JUDGMENT_MACHINE_CONFIG = StateMachineConfig(
    name="JudgmentMachine",
    initial_state=_J.J0_NONE,
    transitions=JUDGMENT_TRANSITIONS,
    accept_states=frozenset({_J.J4_APPROVED}),
    reject_states=frozenset({_J.J5_REJECTED, _J.J6_DEFERRED}),
)


# ── convenience wrapper ────────────────────────────────────────────


class JudgmentMachine:
    """Layer 6 judgment machine producing :class:`ValidatedJudgment`."""

    def __init__(self) -> None:
        self._sm = StateMachine(JUDGMENT_MACHINE_CONFIG)

    @property
    def engine(self) -> StateMachine:
        return self._sm

    def process(self, ctx: Dict[str, Any]) -> ValidatedJudgment | None:
        """Run the judgment pipeline.

        Expected context keys:
        - ``judgment_score``, ``evidence_strength``, ``validation_score``
        - ``recoverability_score``, ``trace_clarity`` (for final approval)
        """
        events = [
            (_E.EV_JUDGMENT_NOMINATED, None),
            (_E.EV_SCORE_COMPUTED, None),
            (_E.EV_REALITY_EVIDENCE_FOUND, None),
            (_E.EV_REALITY_MATCH_PASSED, None),
        ]
        snap = self._sm.run_to_completion(events, initial_context=ctx)

        if self._sm.is_accepted(snap.current_state):
            comps = FinalApprovalComponents(
                judgment_score=ctx.get("judgment_score", 0.0),
                reality_match_score=ctx.get("validation_score", 0.0),
                recoverability_score=ctx.get("recoverability_score", 0.0),
                trace_clarity=ctx.get("trace_clarity", 0.0),
            )
            fa = compute_final_approval(comps)
            return ValidatedJudgment(
                judgment_id=ctx.get("judgment_id", ""),
                final_approval=fa,
                reality_match_score=ctx.get("validation_score", 0.0),
                components=comps,
                is_approved=is_approved(fa),
                evidence_refs=tuple(ctx.get("evidence_refs", ())),
            )
        return None
