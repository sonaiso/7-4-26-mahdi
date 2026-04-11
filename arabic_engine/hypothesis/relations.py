"""Relation hypotheses — فرضيات علاقية.

Generates relation hypothesis nodes from concept hypotheses.
Each adjacent pair of concepts produces a candidate relation.
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.enums import ActivationStage, HypothesisStatus
from arabic_engine.core.types import HypothesisNode

_PREP_TOKENS = frozenset({"إلى", "من", "في", "على", "عن", "ب"})


def generate(concept_hypotheses: List[HypothesisNode]) -> List[HypothesisNode]:
    """Generate relation hypotheses for adjacent concept pairs.

    Parameters
    ----------
    concept_hypotheses : list[HypothesisNode]
        Concept hypotheses in sentence order.

    Returns
    -------
    list[HypothesisNode]
        Relation hypotheses, one per adjacent pair.
    """
    hypotheses: List[HypothesisNode] = []
    for i in range(len(concept_hypotheses) - 1):
        src = concept_hypotheses[i]
        tgt = concept_hypotheses[i + 1]
        src_type = str(src.get("semantic_type", ""))
        tgt_type = str(tgt.get("semantic_type", ""))
        src_label = str(src.get("label", ""))

        if src_type == "EVENT" and tgt_type == "ENTITY":
            rel = "إسناد"
        elif src_label in _PREP_TOKENS:
            rel = "ظرفية"
        else:
            rel = "تقييد"

        hypotheses.append(
            HypothesisNode(
                node_id=f"REL_{src.node_id}_{tgt.node_id}",
                hypothesis_type="relation",
                stage=ActivationStage.RELATION,
                source_refs=(src.node_id, tgt.node_id),
                payload=(
                    ("relation_type", rel),
                    ("source_label", src_label),
                    ("target_label", str(tgt.get("label", ""))),
                ),
                confidence=min(src.confidence, tgt.confidence),
                status=HypothesisStatus.ACTIVE,
            )
        )
    return hypotheses
