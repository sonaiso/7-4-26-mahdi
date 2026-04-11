"""Role hypotheses — فرضيات الأدوار النحوية.

Generates grammatical role hypotheses from concept hypotheses.
Uses positional and type-based heuristics similar to the legacy
pipeline but emits hypothesis nodes instead of deterministic
assignments.
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.enums import ActivationStage, HypothesisStatus
from arabic_engine.core.types import HypothesisNode

_PREP_TOKENS = frozenset({"إلى", "من", "في", "على", "عن", "ب"})


def generate(concept_hypotheses: List[HypothesisNode]) -> List[HypothesisNode]:
    """Generate role hypotheses for each concept hypothesis.

    Parameters
    ----------
    concept_hypotheses : list[HypothesisNode]
        Concept hypotheses in sentence order.

    Returns
    -------
    list[HypothesisNode]
        Role hypotheses, one per concept.
    """
    hypotheses: List[HypothesisNode] = []
    verb_seen = False
    subject_seen = False

    for i, concept in enumerate(concept_hypotheses):
        stype = str(concept.get("semantic_type", ""))
        label = str(concept.get("label", ""))

        role, conf = _infer_role(stype, label, i, verb_seen, subject_seen)

        if stype == "EVENT":
            verb_seen = True
        elif stype == "ENTITY" and verb_seen and not subject_seen:
            subject_seen = True

        hypotheses.append(
            HypothesisNode(
                node_id=f"ROLE_{concept.node_id}",
                hypothesis_type="role",
                stage=ActivationStage.ROLE,
                source_refs=(concept.node_id,),
                payload=(
                    ("role", role),
                    ("token_label", label),
                ),
                confidence=concept.confidence * conf,
                status=HypothesisStatus.ACTIVE,
            )
        )
    return hypotheses


def _infer_role(
    stype: str, label: str, position: int, verb_seen: bool, subject_seen: bool
) -> tuple[str, float]:
    """Infer role and confidence (heuristic)."""
    if stype == "EVENT":
        return ("فعل", 0.95)
    if label in _PREP_TOKENS:
        return ("حرف_جر", 0.95)
    if stype == "ENTITY" and verb_seen and not subject_seen:
        return ("فاعل", 0.9)
    if stype == "ENTITY" and verb_seen and subject_seen:
        return ("مفعول", 0.85)
    if stype == "ENTITY" and not verb_seen and position == 0:
        return ("مبتدأ", 0.85)
    if stype == "ENTITY" and not verb_seen:
        return ("خبر", 0.8)
    return ("غير_محدد", 0.5)
