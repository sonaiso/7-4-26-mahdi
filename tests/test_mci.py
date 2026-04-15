"""Tests for MCI computation."""

from __future__ import annotations

import pytest

from arabic_engine.core.enums import MCIDecision
from arabic_engine.core.mci import (
    classify_mci,
    compute_mci,
    evaluate_mci,
)
from arabic_engine.core.types import MCIScores


class TestComputeMCI:
    def test_all_zeros(self):
        s = MCIScores()
        assert compute_mci(s) == pytest.approx(0.0)

    def test_all_ones(self):
        s = MCIScores(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
        assert compute_mci(s) == pytest.approx(1.0)

    def test_partial_scores(self):
        s = MCIScores(boundary=0.5, unity=0.5, cohesion=0.5,
                      extension=0.5, phase_order=0.5, orderliness=0.5)
        assert compute_mci(s) == pytest.approx(0.5)

    def test_weighted_correctly(self):
        # Only boundary = 1.0, rest = 0.0 → 1.2/7.0
        s = MCIScores(boundary=1.0)
        assert compute_mci(s) == pytest.approx(1.2 / 7.0)


class TestClassifyMCI:
    def test_rejected(self):
        assert classify_mci(0.0) == MCIDecision.REJECTED
        assert classify_mci(0.44) == MCIDecision.REJECTED

    def test_suspended(self):
        assert classify_mci(0.45) == MCIDecision.SUSPENDED
        assert classify_mci(0.64) == MCIDecision.SUSPENDED

    def test_analytically_accepted(self):
        assert classify_mci(0.65) == MCIDecision.ANALYTICALLY_ACCEPTED
        assert classify_mci(0.79) == MCIDecision.ANALYTICALLY_ACCEPTED

    def test_directly_accepted(self):
        assert classify_mci(0.80) == MCIDecision.DIRECTLY_ACCEPTED
        assert classify_mci(1.0) == MCIDecision.DIRECTLY_ACCEPTED


class TestEvaluateMCI:
    def test_returns_mci_result(self):
        s = MCIScores(0.8, 0.8, 0.8, 0.8, 0.8, 0.8)
        result = evaluate_mci(s)
        assert result.mci_value == pytest.approx(0.8)
        assert result.decision == "DIRECTLY_ACCEPTED"
        assert result.scores is s

    def test_rejected_result(self):
        s = MCIScores(0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
        result = evaluate_mci(s)
        assert result.mci_value == pytest.approx(0.1)
        assert result.decision == "REJECTED"
