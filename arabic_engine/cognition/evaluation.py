"""Judgment construction and evaluation (التعريفان 7 و 8).

J : G_s × G_m × D → P   (judgment)
E : P × W → V            (evaluation)

The separation between *judgment* and *evaluation* mirrors the
manuscript's distinction: judging that something *exists* may be
certain, but judging its *truth or quality* is fallible and revisable.
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.enums import (
    DalalaType,
    GuidanceState,
    POS,
    SemanticType,
    TruthState,
    TimeRef,
    SpaceRef,
)
from arabic_engine.core.types import (
    Concept,
    DalalaLink,
    EvalResult,
    LexicalClosure,
    Proposition,
)


# ── Judgment ────────────────────────────────────────────────────────

def build_proposition(
    closures: List[LexicalClosure],
    concepts: List[Concept],
    links: List[DalalaLink],
) -> Proposition:
    """Compose a :class:`Proposition` from the analysis layers.

    Minimal heuristic:
      • first verb  → predicate
      • first noun  → subject (فاعل)
      • second noun → object  (مفعول به)
    """
    subject = ""
    predicate = ""
    obj = ""
    time = TimeRef.UNSPECIFIED
    polarity = True

    for cl in closures:
        if cl.pos == POS.FI3L and not predicate:
            predicate = cl.lemma
            # Simple tense detection from pattern
            if cl.pattern in ("فَعَلَ",):
                time = TimeRef.PAST
            elif cl.pattern in ("يَفْعَلُ",):
                time = TimeRef.PRESENT
        elif cl.pos == POS.ISM and not subject:
            subject = cl.lemma
        elif cl.pos == POS.ISM and not obj:
            obj = cl.lemma

    return Proposition(
        subject=subject,
        predicate=predicate,
        obj=obj,
        time=time,
        polarity=polarity,
    )


# ── Evaluation ──────────────────────────────────────────────────────

def evaluate(
    proposition: Proposition,
    links: List[DalalaLink],
) -> EvalResult:
    """Evaluate a proposition, producing truth/guidance/confidence.

    • Confidence is the average of dalāla-link confidences.
    • Truth state is derived from confidence thresholds.
    • Guidance state defaults to NOT_APPLICABLE for declaratives.
    """
    if links:
        avg_conf = sum(lk.confidence for lk in links) / len(links)
    else:
        avg_conf = 0.0

    if avg_conf >= 0.9:
        truth = TruthState.CERTAIN
    elif avg_conf >= 0.7:
        truth = TruthState.PROBABLE
    elif avg_conf >= 0.4:
        truth = TruthState.POSSIBLE
    else:
        truth = TruthState.DOUBTFUL

    return EvalResult(
        proposition=proposition,
        truth_state=truth,
        guidance_state=GuidanceState.NOT_APPLICABLE,
        confidence=round(avg_conf, 4),
    )
