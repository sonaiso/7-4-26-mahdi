"""Layer orchestrator — connects the six state machines in sequence.

Pipeline order::

    Layer 0  (identity)        → ConceptSeed
    Layer 1  (sound)           → PhoneticEvent
    Layer 2  (MCI)             → PhonemeCandidate
    Layer 2.5 (haraka)         → HarakaUnit
    Layer 3  (syllable)        → SyllableUnit
    Layer 4  (root rank)       → RootSlot
    Layer 5  (transform)       → TransformCandidate
    Layer 6  (judgment)        → ValidatedJudgment

If any layer rejects its input the pipeline stops early and returns
``None``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from arabic_engine.cognition.judgment_machine import JudgmentMachine
from arabic_engine.core.mci import evaluate_mci
from arabic_engine.core.types import (
    ConceptSeed,
    HarakaUnit,
    MCIScores,
    PhonemeCandidate,
    PhoneticEvent,
    RootSlot,
    SyllableUnit,
    TransformCandidate,
    ValidatedJudgment,
)
from arabic_engine.signal.sound_machine import SoundMachine
from arabic_engine.signifier.haraka_machine import HarakaMachine
from arabic_engine.signifier.root_rank_machine import RootRankMachine
from arabic_engine.signifier.syllable_machine import SyllableMachine
from arabic_engine.signifier.transform_machine import TransformMachine

# ── pipeline result ─────────────────────────────────────────────────

LayerOutput = (
    ConceptSeed
    | PhoneticEvent
    | PhonemeCandidate
    | HarakaUnit
    | SyllableUnit
    | RootSlot
    | TransformCandidate
    | ValidatedJudgment
)


@dataclass
class LayerPipelineResult:
    """Aggregated result of running the full layer pipeline."""

    concept_seed: Optional[ConceptSeed] = None
    phonetic_event: Optional[PhoneticEvent] = None
    phoneme_candidate: Optional[PhonemeCandidate] = None
    haraka_unit: Optional[HarakaUnit] = None
    syllable_unit: Optional[SyllableUnit] = None
    root_slot: Optional[RootSlot] = None
    transform_candidate: Optional[TransformCandidate] = None
    validated_judgment: Optional[ValidatedJudgment] = None
    stopped_at_layer: Optional[str] = None
    trace: List[Tuple[str, str]] = field(default_factory=list)
    """List of (layer_name, outcome) pairs."""


# ── orchestrator ───────────────────────────────────────────────────


class LayerOrchestrator:
    """Runs the full layer pipeline (Layers 0–6) for a single unit.

    Each machine is instantiated once and reused for multiple calls.
    """

    def __init__(self) -> None:
        self._sound = SoundMachine()
        self._haraka = HarakaMachine()
        self._syllable = SyllableMachine()
        self._root_rank = RootRankMachine()
        self._transform = TransformMachine()
        self._judgment = JudgmentMachine()

    # -- Layer 0: identity seed -----------------------------------

    @staticmethod
    def _run_layer0(ctx: Dict[str, Any]) -> Optional[ConceptSeed]:
        """Produce a ConceptSeed if identity conditions are met."""
        if (
            ctx.get("has_identity", False)
            and ctx.get("identity_score", 0.0) >= 0.60
        ):
            return ConceptSeed(
                seed_id=ctx.get("seed_id", ""),
                unit_label=ctx.get("unit_label", ""),
                identity_score=ctx.get("identity_score", 0.0),
                rank_hint=ctx.get("rank_hint", ""),
            )
        return None

    # -- Layer 2: MCI gate ----------------------------------------

    @staticmethod
    def _run_layer2(
        ctx: Dict[str, Any],
        phonetic_ref: str,
    ) -> Optional[PhonemeCandidate]:
        """Evaluate MCI and produce a PhonemeCandidate if accepted."""
        scores_dict = ctx.get("mci_scores")
        if scores_dict is None:
            return None
        if isinstance(scores_dict, dict):
            scores = MCIScores(**scores_dict)
        else:
            scores = scores_dict
        result = evaluate_mci(scores)
        if result.mci_value >= 0.65:
            return PhonemeCandidate(
                candidate_id=ctx.get("candidate_id", ""),
                mci_result=result,
                phonetic_event_ref=phonetic_ref,
                symbol=ctx.get("symbol", ""),
            )
        return None

    # -- full pipeline --------------------------------------------

    def run(self, ctx: Dict[str, Any]) -> LayerPipelineResult:
        """Execute the complete layer pipeline.

        *ctx* should contain all necessary context keys for every
        layer.  Missing keys cause the corresponding machine to fail
        gracefully (returning ``None``).
        """
        result = LayerPipelineResult()

        # Layer 0 — identity seed
        seed = self._run_layer0(ctx)
        result.concept_seed = seed
        if seed is None:
            result.stopped_at_layer = "L0_identity"
            result.trace.append(("L0_identity", "rejected"))
            return result
        result.trace.append(("L0_identity", "accepted"))

        # Layer 1 — sound machine
        phonetic = self._sound.process(ctx)
        result.phonetic_event = phonetic
        if phonetic is None:
            result.stopped_at_layer = "L1_sound"
            result.trace.append(("L1_sound", "rejected"))
            return result
        result.trace.append(("L1_sound", "accepted"))

        # Layer 2 — MCI gate
        phoneme = self._run_layer2(ctx, phonetic.event_id)
        result.phoneme_candidate = phoneme
        if phoneme is None:
            result.stopped_at_layer = "L2_mci"
            result.trace.append(("L2_mci", "rejected"))
            return result
        result.trace.append(("L2_mci", "accepted"))

        # Layer 2.5 — haraka machine
        haraka = self._haraka.process(ctx)
        result.haraka_unit = haraka
        if haraka is None:
            result.stopped_at_layer = "L2.5_haraka"
            result.trace.append(("L2.5_haraka", "rejected"))
            return result
        result.trace.append(("L2.5_haraka", "accepted"))

        # Layer 3 — syllable machine
        syllable = self._syllable.process(ctx)
        result.syllable_unit = syllable
        if syllable is None:
            result.stopped_at_layer = "L3_syllable"
            result.trace.append(("L3_syllable", "rejected"))
            return result
        result.trace.append(("L3_syllable", "accepted"))

        # Layer 4 — root rank machine
        root_slot = self._root_rank.process(ctx)
        result.root_slot = root_slot
        if root_slot is None:
            result.stopped_at_layer = "L4_root_rank"
            result.trace.append(("L4_root_rank", "rejected"))
            return result
        result.trace.append(("L4_root_rank", "accepted"))

        # Layer 5 — transform machine
        transform = self._transform.process(ctx)
        result.transform_candidate = transform
        if transform is None:
            result.stopped_at_layer = "L5_transform"
            result.trace.append(("L5_transform", "rejected"))
            return result
        result.trace.append(("L5_transform", "accepted"))

        # Layer 6 — judgment machine
        judgment = self._judgment.process(ctx)
        result.validated_judgment = judgment
        if judgment is None:
            result.stopped_at_layer = "L6_judgment"
            result.trace.append(("L6_judgment", "rejected"))
            return result
        result.trace.append(("L6_judgment", "accepted"))

        return result
