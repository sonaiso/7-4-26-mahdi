"""Tests for the Sound Machine (Layer 1/2)."""

from __future__ import annotations

from arabic_engine.core.enums import LayerEvent, SoundState
from arabic_engine.core.state_machine import StateMachine
from arabic_engine.core.types import MCIScores
from arabic_engine.signal.sound_machine import SOUND_MACHINE_CONFIG, SoundMachine


class TestSoundMachineConfig:
    def test_initial_state(self):
        assert SOUND_MACHINE_CONFIG.initial_state == SoundState.S0_UNOBSERVED

    def test_accept_states(self):
        assert SoundState.S5_STABLE_UNIT in SOUND_MACHINE_CONFIG.accept_states

    def test_reject_states(self):
        assert SoundState.S6_REJECTED in SOUND_MACHINE_CONFIG.reject_states


class TestSoundMachineFlow:
    def _passing_ctx(self):
        return {
            "event_id": "SE1",
            "energy": 0.50,
            "boundary_score": 0.60,
            "phase_count": 2,
            "cohesion_score": 0.70,
            "unity_score": 0.80,
            "mci_scores": MCIScores(0.8, 0.8, 0.8, 0.8, 0.8, 0.8),
        }

    def test_full_pass(self):
        sm = SoundMachine()
        result = sm.process(self._passing_ctx())
        assert result is not None
        assert result.event_id == "SE1"
        assert result.energy == 0.50

    def test_low_energy_rejects(self):
        ctx = self._passing_ctx()
        ctx["energy"] = 0.10  # below threshold
        sm = SoundMachine()
        result = sm.process(ctx)
        assert result is None

    def test_low_boundary_rejects(self):
        ctx = self._passing_ctx()
        ctx["boundary_score"] = 0.20
        sm = SoundMachine()
        result = sm.process(ctx)
        assert result is None

    def test_low_cohesion_rejects(self):
        ctx = self._passing_ctx()
        ctx["cohesion_score"] = 0.30
        sm = SoundMachine()
        result = sm.process(ctx)
        assert result is None

    def test_low_mci_rejects(self):
        ctx = self._passing_ctx()
        ctx["mci_scores"] = MCIScores(0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
        sm = SoundMachine()
        result = sm.process(ctx)
        assert result is None

    def test_confidence_fail_from_s0(self):
        sm = StateMachine(SOUND_MACHINE_CONFIG)
        snap = sm.start({"confidence_failed": True})
        snap = sm.send(snap, LayerEvent.EV_CONFIDENCE_FAILED)
        assert snap.current_state == SoundState.S6_REJECTED
