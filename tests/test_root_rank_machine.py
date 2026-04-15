"""Tests for the Root Rank Machine (Layer 4)."""

from __future__ import annotations

from arabic_engine.core.enums import RootRankState
from arabic_engine.signifier.root_rank_machine import (
    ROOT_RANK_MACHINE_CONFIG,
    RootRankMachine,
)


class TestRootRankMachineConfig:
    def test_initial_state(self):
        assert ROOT_RANK_MACHINE_CONFIG.initial_state == RootRankState.R0_UNRANKED

    def test_accept_states(self):
        assert RootRankState.R5_RANK_VALIDATED in ROOT_RANK_MACHINE_CONFIG.accept_states


class TestRootRankMachineFlow:
    def _passing_ctx(self):
        return {
            "slot_id": "RS1",
            "root_ref": "R_KTB",
            "root_pattern": True,
            "fa_fitness": 0.80,
            "ayn_fitness": 0.50,
            "lam_fitness": 0.40,
            "rank_score": 0.70,
        }

    def test_fa_candidate_passes(self):
        sm = RootRankMachine()
        result = sm.process(self._passing_ctx())
        assert result is not None
        assert result.position == "fa"
        assert result.rank_score == 0.70

    def test_ayn_candidate_passes(self):
        ctx = self._passing_ctx()
        ctx["fa_fitness"] = 0.30
        ctx["ayn_fitness"] = 0.80
        sm = RootRankMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.position == "ayn"

    def test_lam_candidate_passes(self):
        ctx = self._passing_ctx()
        ctx["fa_fitness"] = 0.30
        ctx["ayn_fitness"] = 0.30
        ctx["lam_fitness"] = 0.80
        sm = RootRankMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.position == "lam"

    def test_ambiguous_returns_none(self):
        ctx = self._passing_ctx()
        ctx["fa_fitness"] = 0.70
        ctx["ayn_fitness"] = 0.71  # difference < 0.05
        ctx["lam_fitness"] = 0.30
        sm = RootRankMachine()
        result = sm.process(ctx)
        assert result is None  # deferred

    def test_low_fitness_all_rejects(self):
        ctx = self._passing_ctx()
        ctx["fa_fitness"] = 0.30
        ctx["ayn_fitness"] = 0.30
        ctx["lam_fitness"] = 0.30
        sm = RootRankMachine()
        result = sm.process(ctx)
        assert result is None

    def test_no_root_pattern_rejects(self):
        ctx = self._passing_ctx()
        ctx["root_pattern"] = None
        sm = RootRankMachine()
        result = sm.process(ctx)
        assert result is None

    def test_auto_compute_rank_score(self):
        ctx = self._passing_ctx()
        del ctx["rank_score"]
        ctx["rank_score_components"] = {
            "position_fit": 0.9,
            "constitutiveness": 0.8,
            "inflection_stability": 0.7,
            "syllable_compatibility": 0.8,
            "recoverability": 0.6,
        }
        sm = RootRankMachine()
        result = sm.process(ctx)
        assert result is not None
        assert result.rank_score > 0.65
