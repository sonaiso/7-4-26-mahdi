"""Factor hypotheses — فرضيات العامل النحوي.

Determines the grammatical governor (عامل) for each role hypothesis.
"""

from __future__ import annotations

from typing import List, Optional

from arabic_engine.core.enums import ActivationStage, HypothesisStatus
from arabic_engine.core.types import HypothesisNode


def generate(
    role_hypotheses: List[HypothesisNode],
    concept_hypotheses: List[HypothesisNode],
) -> List[HypothesisNode]:
    """Generate factor hypotheses for each role hypothesis.

    Parameters
    ----------
    role_hypotheses : list[HypothesisNode]
        Role hypotheses in sentence order.
    concept_hypotheses : list[HypothesisNode]
        Concept hypotheses (for verb lookup).

    Returns
    -------
    list[HypothesisNode]
        Factor hypotheses, one per role.
    """
    # Find first verb concept label
    verb_label: Optional[str] = None
    for c in concept_hypotheses:
        if str(c.get("semantic_type", "")) == "EVENT":
            verb_label = str(c.get("label", ""))
            break

    hypotheses: List[HypothesisNode] = []
    for role_h in role_hypotheses:
        role = str(role_h.get("role", ""))
        factor, factor_type = _infer_factor(role, verb_label)

        hypotheses.append(
            HypothesisNode(
                node_id=f"FACT_{role_h.node_id}",
                hypothesis_type="factor",
                stage=ActivationStage.FACTOR,
                source_refs=(role_h.node_id,),
                payload=(
                    ("factor", factor),
                    ("factor_type", factor_type),
                    ("governed_role", role),
                ),
                confidence=role_h.confidence,
                status=HypothesisStatus.ACTIVE,
            )
        )
    return hypotheses


def _infer_factor(role: str, verb_label: Optional[str]) -> tuple[str, str]:
    """Determine factor and factor type from role (heuristic)."""
    if role == "فعل":
        return ("ذاتي", "فعل")
    if role == "فاعل":
        return (verb_label or "مقدر", "فعل")
    if role in ("مبتدأ", "خبر"):
        return ("ابتداء", "عامل_معنوي")
    if role == "حرف_جر":
        return ("ذاتي", "حرف_جر")
    return ("مقدر", "عامل_مقدر")
