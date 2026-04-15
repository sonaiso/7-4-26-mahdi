"""Root-rank state machine — Layer 4.

Transitions::

    R0_UNRANKED → R1_RANK_CANDIDATE → {R2_FA | R3_AYN | R4_LAM}
                                            → R5_RANK_VALIDATED

Ambiguity (score difference < 0.05) leads to R6_RANK_DEFERRED.
"""

from __future__ import annotations

from typing import Any, Dict

from arabic_engine.core.enums import LayerEvent, RootRankState
from arabic_engine.core.formulas import (
    RANK_AMBIGUITY_THRESHOLD,
    RANK_SCORE_THRESHOLD,
    ROOT_FITNESS_THRESHOLD,
    compute_rank_score,
)
from arabic_engine.core.state_machine import (
    StateMachine,
    StateMachineConfig,
    StateTransition,
)
from arabic_engine.core.types import RankScoreComponents, RootSlot

# ── guards ──────────────────────────────────────────────────────────

_E = LayerEvent
_R = RootRankState


def g_context(ctx: Dict[str, Any]) -> bool:
    return ctx.get("root_pattern") is not None


def g_fa(ctx: Dict[str, Any]) -> bool:
    return ctx.get("fa_fitness", 0.0) >= ROOT_FITNESS_THRESHOLD


def g_ayn(ctx: Dict[str, Any]) -> bool:
    return ctx.get("ayn_fitness", 0.0) >= ROOT_FITNESS_THRESHOLD


def g_lam(ctx: Dict[str, Any]) -> bool:
    return ctx.get("lam_fitness", 0.0) >= ROOT_FITNESS_THRESHOLD


def g_rank(ctx: Dict[str, Any]) -> bool:
    return ctx.get("rank_score", 0.0) >= RANK_SCORE_THRESHOLD


def g_ambiguous(ctx: Dict[str, Any]) -> bool:
    diff = ctx.get("rank_diff", 1.0)
    return diff < RANK_AMBIGUITY_THRESHOLD


# ── config ──────────────────────────────────────────────────────────

ROOT_RANK_TRANSITIONS = (
    StateTransition(_R.R0_UNRANKED, _E.EV_ROOT_CONTEXT_FOUND, _R.R1_RANK_CANDIDATE,
                    guard=g_context, guard_name="g_context",
                    priority=1),
    StateTransition(_R.R1_RANK_CANDIDATE, _E.EV_FA_SCORE_MAX, _R.R2_FA_CANDIDATE,
                    guard=g_fa, guard_name="g_fa",
                    threshold=ROOT_FITNESS_THRESHOLD, priority=1),
    StateTransition(_R.R1_RANK_CANDIDATE, _E.EV_AYN_SCORE_MAX, _R.R3_AYN_CANDIDATE,
                    guard=g_ayn, guard_name="g_ayn",
                    threshold=ROOT_FITNESS_THRESHOLD, priority=1),
    StateTransition(_R.R1_RANK_CANDIDATE, _E.EV_LAM_SCORE_MAX, _R.R4_LAM_CANDIDATE,
                    guard=g_lam, guard_name="g_lam",
                    threshold=ROOT_FITNESS_THRESHOLD, priority=1),
    # Confirmation from any candidate slot.
    StateTransition(_R.R2_FA_CANDIDATE, _E.EV_RANK_CONFIRMED, _R.R5_RANK_VALIDATED,
                    guard=g_rank, guard_name="g_rank",
                    threshold=RANK_SCORE_THRESHOLD, priority=1),
    StateTransition(_R.R3_AYN_CANDIDATE, _E.EV_RANK_CONFIRMED, _R.R5_RANK_VALIDATED,
                    guard=g_rank, guard_name="g_rank",
                    threshold=RANK_SCORE_THRESHOLD, priority=1),
    StateTransition(_R.R4_LAM_CANDIDATE, _E.EV_RANK_CONFIRMED, _R.R5_RANK_VALIDATED,
                    guard=g_rank, guard_name="g_rank",
                    threshold=RANK_SCORE_THRESHOLD, priority=1),
    # Ambiguity deferral from candidate state.
    StateTransition(_R.R1_RANK_CANDIDATE, _E.EV_RANK_AMBIGUOUS, _R.R6_RANK_DEFERRED,
                    guard=g_ambiguous, guard_name="g_ambiguous",
                    threshold=RANK_AMBIGUITY_THRESHOLD, priority=0),
    StateTransition(_R.R2_FA_CANDIDATE, _E.EV_RANK_AMBIGUOUS, _R.R6_RANK_DEFERRED,
                    guard=g_ambiguous, guard_name="g_ambiguous",
                    threshold=RANK_AMBIGUITY_THRESHOLD, priority=0),
    StateTransition(_R.R3_AYN_CANDIDATE, _E.EV_RANK_AMBIGUOUS, _R.R6_RANK_DEFERRED,
                    guard=g_ambiguous, guard_name="g_ambiguous",
                    threshold=RANK_AMBIGUITY_THRESHOLD, priority=0),
    StateTransition(_R.R4_LAM_CANDIDATE, _E.EV_RANK_AMBIGUOUS, _R.R6_RANK_DEFERRED,
                    guard=g_ambiguous, guard_name="g_ambiguous",
                    threshold=RANK_AMBIGUITY_THRESHOLD, priority=0),
)

ROOT_RANK_MACHINE_CONFIG = StateMachineConfig(
    name="RootRankMachine",
    initial_state=_R.R0_UNRANKED,
    transitions=ROOT_RANK_TRANSITIONS,
    accept_states=frozenset({_R.R5_RANK_VALIDATED}),
    reject_states=frozenset({_R.R6_RANK_DEFERRED}),
)


# ── convenience wrapper ────────────────────────────────────────────


class RootRankMachine:
    """Layer 4 root-rank machine that produces :class:`RootSlot`."""

    def __init__(self) -> None:
        self._sm = StateMachine(ROOT_RANK_MACHINE_CONFIG)

    @property
    def engine(self) -> StateMachine:
        return self._sm

    def process(self, ctx: Dict[str, Any]) -> RootSlot | None:
        """Run the root-rank pipeline.

        The caller should supply ``rank_score_components`` in *ctx* as
        a dict with keys matching :class:`RankScoreComponents` fields,
        or a pre-computed ``rank_score``.
        """
        # Auto-compute rank_score if components are provided.
        comps = ctx.get("rank_score_components")
        if comps is not None and "rank_score" not in ctx:
            if isinstance(comps, dict):
                comps = RankScoreComponents(**comps)
            ctx["rank_score"] = compute_rank_score(comps)

        # Determine which position event to fire.
        fa = ctx.get("fa_fitness", 0.0)
        ayn = ctx.get("ayn_fitness", 0.0)
        lam = ctx.get("lam_fitness", 0.0)
        best = max(fa, ayn, lam)
        if best > 0 and (max(fa, ayn, lam) - sorted([fa, ayn, lam])[-2]) < RANK_AMBIGUITY_THRESHOLD:
            position_event = _E.EV_RANK_AMBIGUOUS
        elif fa == best:
            position_event = _E.EV_FA_SCORE_MAX
        elif ayn == best:
            position_event = _E.EV_AYN_SCORE_MAX
        else:
            position_event = _E.EV_LAM_SCORE_MAX

        events = [
            (_E.EV_ROOT_CONTEXT_FOUND, None),
            (position_event, None),
            (_E.EV_RANK_CONFIRMED, None),
        ]
        snap = self._sm.run_to_completion(events, initial_context=ctx)
        if self._sm.is_accepted(snap.current_state):
            position_map = {
                _R.R2_FA_CANDIDATE: "fa",
                _R.R3_AYN_CANDIDATE: "ayn",
                _R.R4_LAM_CANDIDATE: "lam",
            }
            # Look back in history to find the position state.
            pos = ""
            for _, _, tgt in snap.history:
                if tgt in position_map:
                    pos = position_map[tgt]
            return RootSlot(
                slot_id=ctx.get("slot_id", ""),
                root_ref=ctx.get("root_ref", ""),
                position=pos,
                rank_score=ctx.get("rank_score", 0.0),
                components=comps if isinstance(comps, RankScoreComponents) else None,
            )
        return None
