"""Tests for the Haraka Machine (Layer 2.5)."""

from __future__ import annotations

from arabic_engine.core.enums import HarakaState, LayerEvent
from arabic_engine.core.state_machine import StateMachine
from arabic_engine.signifier.haraka_machine import HARAKA_MACHINE_CONFIG, HarakaMachine


class TestHarakaMachineConfig:
    def test_initial_state(self):
        assert HARAKA_MACHINE_CONFIG.initial_state == HarakaState.H0_UNKNOWN

    def test_accept_states(self):
        assert HarakaState.H4_LENGTHENED in HARAKA_MACHINE_CONFIG.accept_states


class TestHarakaMachineFlow:
    def _passing_ctx(self):
        return {
            "unit_id": "HU1",
            "sonority_score": 0.60,
            "attachment_target": "P1",
            "mobility_score": 0.70,
            "duration": 0.5,
            "long_min": 1.0,
        }

    def test_full_pass_operational(self):
        sm = HarakaMachine()
        result = sm.process(self._passing_ctx())
        assert result is not None
        assert result.unit_id == "HU1"
        assert not result.is_lengthened

    def test_lengthened(self):
        ctx = self._passing_ctx()
        ctx["duration"] = 2.0
        ctx["long_min"] = 1.0
        sm = HarakaMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.is_lengthened

    def test_low_sonority_rejects(self):
        ctx = self._passing_ctx()
        ctx["sonority_score"] = 0.20
        sm = HarakaMachine()
        result = sm.process(ctx)
        assert result is None

    def test_no_attachment_rejects(self):
        ctx = self._passing_ctx()
        ctx["attachment_target"] = None
        sm = HarakaMachine()
        result = sm.process(ctx)
        assert result is None

    def test_low_mobility_rejects(self):
        ctx = self._passing_ctx()
        ctx["mobility_score"] = 0.30
        sm = HarakaMachine()
        result = sm.process(ctx)
        assert result is None

    def test_haraka_deleted_state(self):
        sm = StateMachine(HARAKA_MACHINE_CONFIG)
        snap = sm.start({"haraka_deleted": True})
        snap = sm.send(snap, LayerEvent.EV_HARAKA_DELETED)
        assert snap.current_state == HarakaState.H5_DELETED

    def test_haraka_invalid_state(self):
        sm = StateMachine(HARAKA_MACHINE_CONFIG)
        snap = sm.start({"haraka_invalid": True})
        snap = sm.send(snap, LayerEvent.EV_HARAKA_INVALID)
        assert snap.current_state == HarakaState.H6_REJECTED
