"""Dalāla (signification) validation (التعريف 6).

D : T × C → {0,1} × [0,1]

Validates the link between a signifier (lexical closure) and its
signified (concept), producing an acceptance flag and a confidence
score.  The three core dalāla modes from the manuscript are:

  • مطابقة (mutābaqa) — exact denotation
  • تضمن  (taḍammun) — part of the meaning
  • التزام (iltizām) — necessary concomitant

Additional structural links (إسناد، تقييد، إضافة، إحالة) connect
concepts within a proposition.
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.enums import POS, DalalaType
from arabic_engine.core.types import Concept, DalalaLink, LexicalClosure


def validate_link(
    closure: LexicalClosure,
    concept: Concept,
) -> DalalaLink:
    """Compute the dalāla link between *closure* and *concept*.

    Returns a :class:`DalalaLink` with acceptance and confidence.
    """
    # Primary denotation — mutābaqa
    if closure.lemma == concept.label:
        return DalalaLink(
            source_lemma=closure.lemma,
            target_concept_id=concept.concept_id,
            dalala_type=DalalaType.MUTABAQA,
            accepted=True,
            confidence=1.0,
        )

    # If root overlaps (shared semantic field) → taḍammun
    if closure.root and any(
        r in concept.label for r in closure.root
    ):
        return DalalaLink(
            source_lemma=closure.lemma,
            target_concept_id=concept.concept_id,
            dalala_type=DalalaType.TADAMMUN,
            accepted=True,
            confidence=0.75,
        )

    # Fallback — weak iltizām
    return DalalaLink(
        source_lemma=closure.lemma,
        target_concept_id=concept.concept_id,
        dalala_type=DalalaType.ILTIZAM,
        accepted=True,
        confidence=0.5,
    )


def build_isnad_links(
    closures: List[LexicalClosure],
    concepts: List[Concept],
) -> List[DalalaLink]:
    """Build predication (إسناد) links for a verb-subject-object structure.

    Assumes the first verb found is the predicate, and noun arguments
    are linked via ISNAD / TAQYID.
    """
    links: List[DalalaLink] = []
    verb_concept: Concept | None = None

    for cl, co in zip(closures, concepts):
        if cl.pos == POS.FI3L:
            verb_concept = co
            continue
        if verb_concept is not None and cl.pos == POS.ISM:
            links.append(DalalaLink(
                source_lemma=cl.lemma,
                target_concept_id=verb_concept.concept_id,
                dalala_type=DalalaType.ISNAD,
                accepted=True,
                confidence=0.95,
            ))

    return links


def full_validation(
    closures: List[LexicalClosure],
    concepts: List[Concept],
) -> List[DalalaLink]:
    """Run mutābaqa validation + isnād linking for a token list."""
    links = [validate_link(c, o) for c, o in zip(closures, concepts)]
    links.extend(build_isnad_links(closures, concepts))
    return links
