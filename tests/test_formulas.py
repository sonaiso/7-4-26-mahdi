"""Tests for formula computations (rank score, final approval)."""

from __future__ import annotations

import pytest

from arabic_engine.core.formulas import (
    compute_final_approval,
    compute_rank_score,
    is_approved,
)
from arabic_engine.core.types import FinalApprovalComponents, RankScoreComponents


class TestRankScore:
    def test_all_zeros(self):
        c = RankScoreComponents()
        assert compute_rank_score(c) == pytest.approx(0.0)

    def test_all_ones(self):
        c = RankScoreComponents(1.0, 1.0, 1.0, 1.0, 1.0)
        assert compute_rank_score(c) == pytest.approx(1.0)

    def test_weighted(self):
        c = RankScoreComponents(position_fit=1.0)
        assert compute_rank_score(c) == pytest.approx(0.30)

    def test_balanced(self):
        c = RankScoreComponents(0.5, 0.5, 0.5, 0.5, 0.5)
        assert compute_rank_score(c) == pytest.approx(0.5)


class TestFinalApproval:
    def test_all_zeros(self):
        c = FinalApprovalComponents()
        assert compute_final_approval(c) == pytest.approx(0.0)

    def test_all_ones(self):
        c = FinalApprovalComponents(1.0, 1.0, 1.0, 1.0)
        assert compute_final_approval(c) == pytest.approx(1.0)

    def test_weighted(self):
        c = FinalApprovalComponents(judgment_score=1.0)
        assert compute_final_approval(c) == pytest.approx(0.40)

    def test_threshold(self):
        assert is_approved(0.75)
        assert is_approved(0.80)
        assert not is_approved(0.74)
        assert not is_approved(0.0)
