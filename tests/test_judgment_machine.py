"""Tests for the Judgment Machine (Layer 6)."""

from __future__ import annotations

from arabic_engine.cognition.judgment_machine import (
    JUDGMENT_MACHINE_CONFIG,
    JudgmentMachine,
)
from arabic_engine.core.enums import JudgmentState, LayerEvent
from arabic_engine.core.state_machine import StateMachine


class TestJudgmentMachineConfig:
    def test_initial_state(self):
        assert JUDGMENT_MACHINE_CONFIG.initial_state == JudgmentState.J0_NONE

    def test_accept_states(self):
        assert JudgmentState.J4_APPROVED in JUDGMENT_MACHINE_CONFIG.accept_states

    def test_reject_states(self):
        assert JudgmentState.J5_REJECTED in JUDGMENT_MACHINE_CONFIG.reject_states
        assert JudgmentState.J6_DEFERRED in JUDGMENT_MACHINE_CONFIG.reject_states


class TestJudgmentMachineFlow:
    def _passing_ctx(self):
        return {
            "judgment_id": "JG1",
            "judgment_score": 0.80,
            "evidence_strength": 0.70,
            "validation_score": 0.80,
            "recoverability_score": 0.70,
            "trace_clarity": 0.80,
            "evidence_refs": ["E1", "E2"],
        }

    def test_full_approval(self):
        sm = JudgmentMachine()
        result = sm.process(self._passing_ctx())
        assert result is not None
        assert result.is_approved
        assert result.final_approval >= 0.75
        assert result.judgment_id == "JG1"
        assert result.evidence_refs == ("E1", "E2")

    def test_low_judgment_score_rejects(self):
        ctx = self._passing_ctx()
        ctx["judgment_score"] = 0.40
        sm = JudgmentMachine()
        result = sm.process(ctx)
        assert result is None

    def test_low_evidence_rejects(self):
        ctx = self._passing_ctx()
        ctx["evidence_strength"] = 0.30
        sm = JudgmentMachine()
        result = sm.process(ctx)
        assert result is None

    def test_low_validation_rejects(self):
        ctx = self._passing_ctx()
        ctx["validation_score"] = 0.50
        sm = JudgmentMachine()
        result = sm.process(ctx)
        assert result is None

    def test_reality_match_failed(self):
        sm = StateMachine(JUDGMENT_MACHINE_CONFIG)
        snap = sm.start({
            "judgment_score": 0.80,
            "evidence_strength": 0.70,
            "validation_score": 0.50,
        })
        snap = sm.send(snap, LayerEvent.EV_JUDGMENT_NOMINATED)
        snap = sm.send(snap, LayerEvent.EV_SCORE_COMPUTED)
        snap = sm.send(snap, LayerEvent.EV_REALITY_EVIDENCE_FOUND)
        snap = sm.send(snap, LayerEvent.EV_REALITY_MATCH_FAILED)
        assert snap.current_state == JudgmentState.J5_REJECTED

    def test_insufficient_evidence_deferred(self):
        sm = StateMachine(JUDGMENT_MACHINE_CONFIG)
        snap = sm.start({"insufficient_evidence": True})
        snap = sm.send(snap, LayerEvent.EV_INSUFFICIENT_EVIDENCE)
        assert snap.current_state == JudgmentState.J6_DEFERRED

    def test_final_approval_components(self):
        sm = JudgmentMachine()
        result = sm.process(self._passing_ctx())
        assert result is not None
        assert result.components is not None
        assert result.components.judgment_score == 0.80
        assert result.components.reality_match_score == 0.80
