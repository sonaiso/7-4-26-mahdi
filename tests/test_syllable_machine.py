"""Tests for the Syllable Machine (Layer 3)."""

from __future__ import annotations

from arabic_engine.core.enums import LayerEvent, SyllableState
from arabic_engine.core.state_machine import StateMachine
from arabic_engine.signifier.syllable_machine import (
    SYLLABLE_MACHINE_CONFIG,
    VALID_SHAPES,
    SyllableMachine,
)


class TestSyllableMachineConfig:
    def test_initial_state(self):
        assert SYLLABLE_MACHINE_CONFIG.initial_state == SyllableState.Y0_NONE

    def test_accept_states(self):
        assert SyllableState.Y5_VALIDATED in SYLLABLE_MACHINE_CONFIG.accept_states

    def test_valid_shapes(self):
        assert "CV" in VALID_SHAPES
        assert "CVC" in VALID_SHAPES
        assert "CVV" in VALID_SHAPES
        assert "CVVC" in VALID_SHAPES
        assert "CVCC" in VALID_SHAPES


class TestSyllableMachineFlow:
    def _passing_ctx(self):
        return {
            "unit_id": "SY1",
            "has_nucleus": True,
            "pattern_shape": "CVC",
            "weight_class": 2,
            "nucleus_ref": "N1",
            "syllable_score": 0.80,
        }

    def test_full_pass(self):
        sm = SyllableMachine()
        result = sm.process(self._passing_ctx())
        assert result is not None
        assert result.unit_id == "SY1"
        assert result.pattern_shape == "CVC"
        assert result.weight_class == 2

    def test_no_nucleus_rejects(self):
        ctx = self._passing_ctx()
        ctx["has_nucleus"] = False
        sm = SyllableMachine()
        result = sm.process(ctx)
        assert result is None

    def test_invalid_shape_rejects(self):
        ctx = self._passing_ctx()
        ctx["pattern_shape"] = "CCVC"  # not in valid shapes
        sm = SyllableMachine()
        result = sm.process(ctx)
        assert result is None

    def test_no_weight_rejects(self):
        ctx = self._passing_ctx()
        ctx["weight_class"] = None
        sm = SyllableMachine()
        result = sm.process(ctx)
        assert result is None

    def test_low_syllable_score_rejects(self):
        ctx = self._passing_ctx()
        ctx["syllable_score"] = 0.40
        sm = SyllableMachine()
        result = sm.process(ctx)
        assert result is None

    def test_all_valid_shapes_accepted(self):
        for shape in VALID_SHAPES:
            ctx = self._passing_ctx()
            ctx["pattern_shape"] = shape
            sm = SyllableMachine()
            result = sm.process(ctx)
            assert result is not None, f"Shape {shape} should be accepted"

    def test_confidence_fail_to_rejected(self):
        sm = StateMachine(SYLLABLE_MACHINE_CONFIG)
        snap = sm.start({"syllable_score": 0.20})
        snap = sm.send(snap, LayerEvent.EV_CONFIDENCE_FAILED)
        assert snap.current_state == SyllableState.Y6_REJECTED
