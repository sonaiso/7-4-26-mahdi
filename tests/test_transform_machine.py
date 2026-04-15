"""Tests for the Transform Machine (Layer 5)."""

from __future__ import annotations

from arabic_engine.core.enums import TransformState
from arabic_engine.signifier.transform_machine import (
    TRANSFORM_MACHINE_CONFIG,
    TransformMachine,
)


class TestTransformMachineConfig:
    def test_initial_state(self):
        assert TRANSFORM_MACHINE_CONFIG.initial_state == TransformState.T0_NONE

    def test_accept_states(self):
        assert TransformState.T7_VALIDATED in TRANSFORM_MACHINE_CONFIG.accept_states


class TestTransformMachineFlow:
    def test_idgham_highest_priority(self):
        ctx = {
            "candidate_id": "TC1",
            "idgham_confidence": 0.80,
            "illal_confidence": 0.80,  # both high, but idgham priority=1
            "transform_score": 0.80,
        }
        sm = TransformMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.transform_type == "ASSIMILATED"

    def test_illal(self):
        ctx = {
            "candidate_id": "TC2",
            "illal_confidence": 0.70,
            "transform_score": 0.80,
        }
        sm = TransformMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.transform_type == "WEAKENED"

    def test_substitution(self):
        ctx = {
            "candidate_id": "TC3",
            "recoverability_score": 0.70,
            "changed_material": True,
            "transform_score": 0.80,
        }
        sm = TransformMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.transform_type == "SUBSTITUTED"

    def test_deletion(self):
        ctx = {
            "candidate_id": "TC4",
            "surface_presence": False,
            "underlying_presence": True,
            "transform_score": 0.80,
        }
        sm = TransformMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.transform_type == "DELETED"

    def test_augmented(self):
        ctx = {
            "candidate_id": "TC5",
            "dependency_score": 0.70,
            "augmentation_score": 0.70,
            "transform_score": 0.80,
        }
        sm = TransformMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.transform_type == "AUGMENTED"

    def test_original(self):
        ctx = {
            "candidate_id": "TC6",
            "constitutiveness_score": 0.80,
            "inflection_stability_score": 0.80,
            "transform_score": 0.80,
        }
        sm = TransformMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.transform_type == "ORIGINAL"

    def test_no_match_returns_none(self):
        ctx = {"candidate_id": "TC7"}  # no scores
        sm = TransformMachine()
        result = sm.process(ctx)
        assert result is None

    def test_low_transform_score_rejects(self):
        ctx = {
            "candidate_id": "TC8",
            "idgham_confidence": 0.80,
            "transform_score": 0.50,  # below validation threshold
        }
        sm = TransformMachine()
        result = sm.process(ctx)
        assert result is None

    def test_priority_order_idgham_over_original(self):
        """Idgham (priority=1) should beat Original (priority=6)."""
        ctx = {
            "candidate_id": "TC9",
            "idgham_confidence": 0.70,
            "constitutiveness_score": 0.80,
            "inflection_stability_score": 0.80,
            "transform_score": 0.80,
        }
        sm = TransformMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.transform_type == "ASSIMILATED"
