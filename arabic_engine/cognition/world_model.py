"""World model — a minimal knowledge base of facts (v2).

Provides the *W* in the evaluation function  E : P × W → V.

The world model stores ground-truth facts and allows the evaluation
layer to compare incoming propositions against known reality, raising
or lowering confidence accordingly.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from arabic_engine.core.enums import TruthState
from arabic_engine.core.types import Proposition, WorldFact

_next_fact_id = 0


class WorldModel:
    """An in-memory fact store representing the current world state."""

    def __init__(self) -> None:
        self._facts: Dict[int, WorldFact] = {}
        self._index: Dict[str, List[int]] = {}  # subject → fact_ids

    # ── Mutation ─────────────────────────────────────────────────

    def add_fact(
        self,
        subject: str,
        predicate: str,
        obj: str,
        truth_state: TruthState = TruthState.CERTAIN,
        source: str = "axiom",
    ) -> WorldFact:
        """Insert a new fact and return it."""
        global _next_fact_id
        _next_fact_id += 1
        fact = WorldFact(
            fact_id=_next_fact_id,
            subject=subject,
            predicate=predicate,
            obj=obj,
            truth_state=truth_state,
            source=source,
        )
        self._facts[fact.fact_id] = fact
        self._index.setdefault(subject, []).append(fact.fact_id)
        return fact

    # ── Query ────────────────────────────────────────────────────

    def lookup(
        self,
        subject: str,
        predicate: Optional[str] = None,
    ) -> List[WorldFact]:
        """Return facts matching *subject* (and optionally *predicate*)."""
        ids = self._index.get(subject, [])
        results = [self._facts[fid] for fid in ids]
        if predicate is not None:
            results = [f for f in results if f.predicate == predicate]
        return results

    def matches(self, proposition: Proposition) -> Optional[WorldFact]:
        """Check if a proposition is supported by a known fact."""
        candidates = self.lookup(proposition.subject, proposition.predicate)
        for fact in candidates:
            if fact.obj == proposition.obj:
                return fact
        return None

    def confidence_adjustment(self, proposition: Proposition) -> float:
        """Return a confidence multiplier based on world-model support.

        • 1.0  if a matching fact is found and CERTAIN
        • 0.8  if PROBABLE
        • 0.5  if no evidence found
        • 0.1  if contradicted
        """
        fact = self.matches(proposition)
        if fact is None:
            return 0.5  # no evidence
        if fact.truth_state == TruthState.CERTAIN:
            return 1.0
        if fact.truth_state == TruthState.PROBABLE:
            return 0.8
        if fact.truth_state == TruthState.FALSE:
            return 0.1
        return 0.5

    @property
    def all_facts(self) -> List[WorldFact]:
        return list(self._facts.values())
