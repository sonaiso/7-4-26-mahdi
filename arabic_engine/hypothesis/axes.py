"""Axis hypotheses — فرضيات محورية.

Generates axis hypothesis nodes from concept hypotheses.  Each concept
may activate zero or more semantic axes (e.g. definite/indefinite,
derived/frozen, temporal/spatial).
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.enums import ActivationStage, HypothesisStatus
from arabic_engine.core.types import HypothesisNode

_AXIS_NAMES = (
    "جامد/مشتق",
    "مبني/معرب",
    "معرفة/نكرة",
    "كلي/جزئي",
    "ثابت/متحول",
    "زمني/مكاني",
)


def generate(concept_hypotheses: List[HypothesisNode]) -> List[HypothesisNode]:
    """Generate axis hypotheses from concept hypotheses.

    For each concept, creates one axis hypothesis per axis name.

    Parameters
    ----------
    concept_hypotheses : list[HypothesisNode]
        Concept hypotheses (``hypothesis_type == "concept"``).

    Returns
    -------
    list[HypothesisNode]
        Axis hypotheses, ``len(concept_hypotheses) * len(_AXIS_NAMES)``
        in total.
    """
    hypotheses: List[HypothesisNode] = []
    for concept in concept_hypotheses:
        determination = concept.get("determination", "indefinite")
        for axis_name in _AXIS_NAMES:
            value = _resolve_axis(axis_name, str(determination))
            hypotheses.append(
                HypothesisNode(
                    node_id=f"AXIS_{concept.node_id}_{axis_name}",
                    hypothesis_type="axis",
                    stage=ActivationStage.AXIS,
                    source_refs=(concept.node_id,),
                    payload=(
                        ("axis_name", axis_name),
                        ("axis_value", value),
                    ),
                    confidence=concept.confidence,
                    status=HypothesisStatus.ACTIVE,
                )
            )
    return hypotheses


def _resolve_axis(axis_name: str, determination: str) -> str:
    """Resolve a single axis value (heuristic stub)."""
    if axis_name == "معرفة/نكرة":
        return "معرفة" if determination == "definite" else "نكرة"
    return "غير محدد"
