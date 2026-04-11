"""Judgement hypotheses — فرضيات الحكم.

Produces a judgement hypothesis from the stabilised case hypotheses.
The judgement is the final output of the hypothesis graph.
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.enums import ActivationStage, HypothesisStatus
from arabic_engine.core.types import HypothesisNode


def generate(case_hypotheses: List[HypothesisNode]) -> List[HypothesisNode]:
    """Generate a single judgement hypothesis from case hypotheses.

    Parameters
    ----------
    case_hypotheses : list[HypothesisNode]
        Case hypotheses (one per token).

    Returns
    -------
    list[HypothesisNode]
        A singleton list containing the judgement hypothesis.
    """
    if not case_hypotheses:
        return [
            HypothesisNode(
                node_id="JUDG_0",
                hypothesis_type="judgement",
                stage=ActivationStage.JUDGEMENT,
                payload=(
                    ("proposition_type", "غير محدد"),
                    ("rank", "غير محدد"),
                ),
                confidence=0.0,
                status=HypothesisStatus.ACTIVE,
            )
        ]

    avg_conf = sum(h.confidence for h in case_hypotheses) / len(case_hypotheses)
    source_refs = tuple(h.node_id for h in case_hypotheses)

    return [
        HypothesisNode(
            node_id="JUDG_0",
            hypothesis_type="judgement",
            stage=ActivationStage.JUDGEMENT,
            source_refs=source_refs,
            payload=(
                ("proposition_type", "تقريرية"),
                ("rank", "إخبار"),
                ("case_count", len(case_hypotheses)),
            ),
            confidence=round(avg_conf, 4),
            status=HypothesisStatus.ACTIVE,
        )
    ]
