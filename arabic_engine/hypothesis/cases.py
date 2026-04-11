"""Case hypotheses — فرضيات الحالة الإعرابية.

Generates case (i'rāb) hypotheses from role + factor hypotheses.
Case is treated as a *stabilisation decision* — not a direct lookup.
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.enums import ActivationStage, HypothesisStatus
from arabic_engine.core.types import HypothesisNode

_ROLE_CASE_MAP: dict[str, str] = {
    "فاعل": "رفع",
    "مبتدأ": "رفع",
    "خبر": "رفع",
    "مفعول": "نصب",
    "حرف_جر": "مبني",
    "فعل": "مبني",
}


def generate(
    role_hypotheses: List[HypothesisNode],
    factor_hypotheses: List[HypothesisNode],
) -> List[HypothesisNode]:
    """Generate case hypotheses from paired role + factor hypotheses.

    Parameters
    ----------
    role_hypotheses : list[HypothesisNode]
        Role hypotheses in sentence order.
    factor_hypotheses : list[HypothesisNode]
        Factor hypotheses (parallel to role hypotheses).

    Returns
    -------
    list[HypothesisNode]
        Case hypotheses, one per role/factor pair.
    """
    hypotheses: List[HypothesisNode] = []
    for role_h, factor_h in zip(role_hypotheses, factor_hypotheses):
        role = str(role_h.get("role", ""))
        factor = str(factor_h.get("factor", ""))
        case_state = _ROLE_CASE_MAP.get(role, "غير_محدد")
        justification = f"{role} + {factor} → {case_state}"

        hypotheses.append(
            HypothesisNode(
                node_id=f"CASE_{role_h.node_id}",
                hypothesis_type="case",
                stage=ActivationStage.CASE,
                source_refs=(role_h.node_id, factor_h.node_id),
                payload=(
                    ("case_state", case_state),
                    ("role", role),
                    ("factor", factor),
                    ("justification", justification),
                ),
                confidence=min(role_h.confidence, factor_h.confidence),
                status=HypothesisStatus.ACTIVE,
            )
        )
    return hypotheses
