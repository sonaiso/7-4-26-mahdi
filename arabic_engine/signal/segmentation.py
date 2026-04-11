"""Segmentation — primary and optional alternate segmentations.

Produces segmentation candidates from signal units.  The default
implementation emits one primary segmentation (whitespace-based)
and does **not** attempt clitic splitting or morpheme segmentation
in this first iteration — those are reserved for future phases.

Architectural rule: **no segmentation without boundary basis**.
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.enums import ActivationStage, HypothesisStatus
from arabic_engine.core.types import HypothesisNode, SignalUnit


def segment(signal_units: List[SignalUnit]) -> List[HypothesisNode]:
    """Generate segmentation hypotheses from signal units.

    Each signal unit becomes a primary segmentation hypothesis with
    confidence 1.0.  In future iterations, clitic-split alternatives
    may be added as secondary hypotheses with lower confidence.

    Parameters
    ----------
    signal_units : list[SignalUnit]
        Output of :func:`~arabic_engine.signal.normalization.normalize_atoms`.

    Returns
    -------
    list[HypothesisNode]
        One hypothesis per signal unit (primary segmentation).
    """
    hypotheses: List[HypothesisNode] = []
    for unit in signal_units:
        hypotheses.append(
            HypothesisNode(
                node_id=f"SEG_{unit.unit_id}",
                hypothesis_type="segmentation",
                stage=ActivationStage.SIGNAL,
                source_refs=(unit.unit_id,),
                payload=(
                    ("token_text", unit.normalized_text),
                    ("boundary_basis", "whitespace"),
                    ("surface_text", unit.surface_text),
                ),
                confidence=1.0,
                status=HypothesisStatus.ACTIVE,
            )
        )
    return hypotheses
