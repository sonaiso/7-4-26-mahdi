"""Ontological mapping — from lexical closure to concepts (التعريف 5).

O : T → C

Maps each lexical entry to a *concept node* with a semantic type
(entity / event / attribute / relation / norm) and a property vector.
"""

from __future__ import annotations

from typing import Dict, List

from arabic_engine.core.enums import POS, SemanticType
from arabic_engine.core.types import Concept, LexicalClosure

# ── Concept registry (demo) ─────────────────────────────────────────

_CONCEPT_DB: Dict[str, Concept] = {
    "كَتَبَ": Concept(
        concept_id=101,
        label="كتابة",
        semantic_type=SemanticType.EVENT,
        properties={"transitivity": "muta3addi", "tense": "madi"},
    ),
    "زَيْد": Concept(
        concept_id=201,
        label="زَيْد",
        semantic_type=SemanticType.ENTITY,
        properties={"animacy": True, "proper_noun": True},
    ),
    "رِسَالَة": Concept(
        concept_id=301,
        label="رِسَالَة",
        semantic_type=SemanticType.ENTITY,
        properties={"animacy": False, "countable": True},
    ),
    # ── Time adverbs (v2) ───────────────────────────────────────
    "أَمْس": Concept(
        concept_id=401,
        label="أَمْس",
        semantic_type=SemanticType.ATTRIBUTE,
        properties={"temporal": True, "time_ref": "past"},
    ),
    "غَد": Concept(
        concept_id=402,
        label="غَد",
        semantic_type=SemanticType.ATTRIBUTE,
        properties={"temporal": True, "time_ref": "future"},
    ),
}

_POS_TO_STYPE = {
    POS.FI3L: SemanticType.EVENT,
    POS.ISM: SemanticType.ENTITY,
    POS.SIFA: SemanticType.ATTRIBUTE,
    POS.HARF: SemanticType.RELATION,
    POS.ZARF: SemanticType.ATTRIBUTE,
}

_next_concept_id = 900


def map_concept(closure: LexicalClosure) -> Concept:
    """Map a :class:`LexicalClosure` to a :class:`Concept`."""
    concept = _CONCEPT_DB.get(closure.lemma)
    if concept is not None:
        return concept

    global _next_concept_id
    _next_concept_id += 1
    return Concept(
        concept_id=_next_concept_id,
        label=closure.lemma,
        semantic_type=_POS_TO_STYPE.get(closure.pos, SemanticType.ENTITY),
    )


def batch_map(closures: List[LexicalClosure]) -> List[Concept]:
    """Map a list of closures to concepts."""
    return [map_concept(c) for c in closures]
