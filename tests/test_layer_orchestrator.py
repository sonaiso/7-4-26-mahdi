"""Tests for the Layer Orchestrator and run_with_layers."""

from __future__ import annotations

from arabic_engine.core.types import MCIScores
from arabic_engine.runtime.layer_orchestrator import LayerOrchestrator


def _full_context():
    """Return a context dict that passes all layers."""
    return {
        # Layer 0 — identity
        "has_identity": True,
        "identity_score": 0.80,
        "seed_id": "SEED_1",
        "unit_label": "كتب",
        "rank_hint": "verb",
        # Layer 1 — sound
        "event_id": "SE1",
        "energy": 0.60,
        "boundary_score": 0.70,
        "phase_count": 2,
        "cohesion_score": 0.75,
        "unity_score": 0.80,
        "mci_scores": MCIScores(0.8, 0.8, 0.8, 0.8, 0.8, 0.8),
        "position": 0,
        "interception_type": "direct",
        # Layer 2 — MCI
        "candidate_id": "PC1",
        "symbol": "ك",
        # Layer 2.5 — haraka
        "unit_id": "HU1",
        "sonority_score": 0.70,
        "attachment_target": "P1",
        "mobility_score": 0.65,
        # Layer 3 — syllable
        "has_nucleus": True,
        "pattern_shape": "CVC",
        "weight_class": 2,
        "nucleus_ref": "N1",
        "syllable_score": 0.80,
        # Layer 4 — root rank
        "slot_id": "RS1",
        "root_ref": "R_KTB",
        "root_pattern": True,
        "fa_fitness": 0.80,
        "ayn_fitness": 0.50,
        "lam_fitness": 0.40,
        "rank_score": 0.75,
        # Layer 5 — transform
        "constitutiveness_score": 0.80,
        "inflection_stability_score": 0.80,
        "transform_score": 0.80,
        "source_root_ref": "R_KTB",
        "recoverability_score": 0.70,
        # Layer 6 — judgment
        "judgment_id": "JG1",
        "judgment_score": 0.80,
        "evidence_strength": 0.75,
        "validation_score": 0.80,
        "trace_clarity": 0.80,
        "evidence_refs": ["E1", "E2"],
    }


class TestLayerOrchestrator:
    def test_full_pipeline_succeeds(self):
        orch = LayerOrchestrator()
        result = orch.run(_full_context())
        assert result.concept_seed is not None
        assert result.phonetic_event is not None
        assert result.phoneme_candidate is not None
        assert result.haraka_unit is not None
        assert result.syllable_unit is not None
        assert result.root_slot is not None
        assert result.transform_candidate is not None
        assert result.validated_judgment is not None
        assert result.stopped_at_layer is None
        assert len(result.trace) == 8

    def test_stops_at_layer0_on_no_identity(self):
        ctx = _full_context()
        ctx["has_identity"] = False
        orch = LayerOrchestrator()
        result = orch.run(ctx)
        assert result.concept_seed is None
        assert result.stopped_at_layer == "L0_identity"

    def test_stops_at_layer1_on_low_energy(self):
        ctx = _full_context()
        ctx["energy"] = 0.10
        orch = LayerOrchestrator()
        result = orch.run(ctx)
        assert result.concept_seed is not None
        assert result.phonetic_event is None
        assert result.stopped_at_layer == "L1_sound"

    def test_stops_at_layer2_on_low_mci(self):
        ctx = _full_context()
        ctx["mci_scores"] = MCIScores(0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
        orch = LayerOrchestrator()
        result = orch.run(ctx)
        # Sound machine also uses MCI, so it might stop at L1 or L2
        assert result.stopped_at_layer in ("L1_sound", "L2_mci")

    def test_stops_at_haraka_on_no_attachment(self):
        ctx = _full_context()
        ctx["attachment_target"] = None
        orch = LayerOrchestrator()
        result = orch.run(ctx)
        assert result.stopped_at_layer == "L2.5_haraka"

    def test_stops_at_syllable_on_invalid_shape(self):
        ctx = _full_context()
        ctx["pattern_shape"] = "CCCV"
        orch = LayerOrchestrator()
        result = orch.run(ctx)
        assert result.stopped_at_layer == "L3_syllable"

    def test_trace_records_outcomes(self):
        orch = LayerOrchestrator()
        result = orch.run(_full_context())
        assert all(outcome == "accepted" for _, outcome in result.trace)


class TestRunWithLayers:
    def test_convenience_function(self):
        from arabic_engine.runtime.orchestrator import run_with_layers

        result = run_with_layers(_full_context())
        assert result.validated_judgment is not None
