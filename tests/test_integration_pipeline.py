"""Integration test — full pipeline from input to validated judgment.

Simulates the processing of the Arabic word "كَتَبَ" (kataba — he wrote)
through all seven layers.
"""

from __future__ import annotations

from arabic_engine.core.types import MCIScores
from arabic_engine.runtime.layer_orchestrator import LayerOrchestrator


def test_kataba_full_pipeline():
    """Simulate كَتَبَ through all layers."""
    ctx = {
        # Layer 0 — identity
        "has_identity": True,
        "identity_score": 0.90,
        "seed_id": "SEED_KTB",
        "unit_label": "كَتَبَ",
        "rank_hint": "verb_past",
        # Layer 1 — sound
        "event_id": "SE_KTB",
        "energy": 0.75,
        "boundary_score": 0.80,
        "phase_count": 3,
        "cohesion_score": 0.85,
        "unity_score": 0.90,
        "mci_scores": MCIScores(
            boundary=0.85,
            unity=0.90,
            cohesion=0.85,
            extension=0.70,
            phase_order=0.80,
            orderliness=0.85,
        ),
        "position": 0,
        "interception_type": "direct",
        # Layer 2 — MCI
        "candidate_id": "PC_KTB",
        "symbol": "كتب",
        # Layer 2.5 — haraka
        "unit_id": "HU_KTB",
        "sonority_score": 0.75,
        "attachment_target": "kaf",
        "mobility_score": 0.70,
        # Layer 3 — syllable
        "has_nucleus": True,
        "pattern_shape": "CVC",
        "weight_class": 2,
        "nucleus_ref": "fatha_1",
        "syllable_score": 0.80,
        # Layer 4 — root rank
        "slot_id": "RS_KTB",
        "root_ref": "R_KTB",
        "root_pattern": True,
        "fa_fitness": 0.90,   # كاف is fa
        "ayn_fitness": 0.85,  # تاء is ayn
        "lam_fitness": 0.80,  # باء is lam
        "rank_score": 0.85,
        # Layer 5 — transform
        "constitutiveness_score": 0.90,
        "inflection_stability_score": 0.85,
        "transform_score": 0.85,
        "source_root_ref": "R_KTB",
        "recoverability_score": 0.80,
        # Layer 6 — judgment
        "judgment_id": "JG_KTB",
        "judgment_score": 0.85,
        "evidence_strength": 0.80,
        "validation_score": 0.85,
        "trace_clarity": 0.80,
        "evidence_refs": ["E_QURAN_KTB", "E_DICT_KTB"],
    }

    orch = LayerOrchestrator()
    result = orch.run(ctx)

    # All layers must pass
    assert result.stopped_at_layer is None
    assert len(result.trace) == 8
    assert all(outcome == "accepted" for _, outcome in result.trace)

    # Layer 0 — identity seed
    assert result.concept_seed is not None
    assert result.concept_seed.seed_id == "SEED_KTB"
    assert result.concept_seed.unit_label == "كَتَبَ"

    # Layer 1 — phonetic event
    assert result.phonetic_event is not None
    assert result.phonetic_event.energy == 0.75

    # Layer 2 — phoneme candidate
    assert result.phoneme_candidate is not None
    assert result.phoneme_candidate.mci_result is not None
    assert result.phoneme_candidate.mci_result.mci_value >= 0.65

    # Layer 2.5 — haraka
    assert result.haraka_unit is not None
    assert result.haraka_unit.sonority_score == 0.75

    # Layer 3 — syllable
    assert result.syllable_unit is not None
    assert result.syllable_unit.pattern_shape == "CVC"

    # Layer 4 — root rank
    assert result.root_slot is not None
    assert result.root_slot.position == "fa"  # kaf has highest fitness

    # Layer 5 — transform
    assert result.transform_candidate is not None
    assert result.transform_candidate.transform_type == "ORIGINAL"  # no transform

    # Layer 6 — judgment
    assert result.validated_judgment is not None
    assert result.validated_judgment.is_approved
    assert result.validated_judgment.final_approval >= 0.75
    assert "E_QURAN_KTB" in result.validated_judgment.evidence_refs
