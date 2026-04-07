"""Inference rules — simple forward-chaining rule engine (v2).

Applies syllogistic and modus-ponens-style inference rules to
propositions, producing derived conclusions with tracked provenance.
"""

from __future__ import annotations

from typing import Callable, List, Optional

from arabic_engine.core.types import InferenceResult, Proposition

# ── Rule type ───────────────────────────────────────────────────────

RuleFunc = Callable[[List[Proposition]], Optional[InferenceResult]]


# ── Built-in rules ──────────────────────────────────────────────────

def _transitivity_rule(propositions: List[Proposition]) -> Optional[InferenceResult]:
    """If A→B and B→C then A→C (simplified transitivity).

    Matches propositions where the object of one equals the subject
    of another sharing the same predicate.
    """
    for p1 in propositions:
        for p2 in propositions:
            if p1 is p2:
                continue
            if p1.obj == p2.subject and p1.predicate == p2.predicate:
                conclusion = Proposition(
                    subject=p1.subject,
                    predicate=p1.predicate,
                    obj=p2.obj,
                    time=p1.time,
                    polarity=p1.polarity and p2.polarity,
                )
                return InferenceResult(
                    rule_name="transitivity",
                    premises=[p1, p2],
                    conclusion=conclusion,
                    confidence=0.85,
                    valid=True,
                )
    return None


def _negation_rule(propositions: List[Proposition]) -> Optional[InferenceResult]:
    """If both P and ¬P exist, flag contradiction."""
    for p1 in propositions:
        for p2 in propositions:
            if p1 is p2:
                continue
            if (
                p1.subject == p2.subject
                and p1.predicate == p2.predicate
                and p1.obj == p2.obj
                and p1.polarity != p2.polarity
            ):
                return InferenceResult(
                    rule_name="contradiction",
                    premises=[p1, p2],
                    conclusion=p1,  # mark the affirmative as suspect
                    confidence=0.0,
                    valid=False,
                )
    return None


def _event_existence_rule(propositions: List[Proposition]) -> Optional[InferenceResult]:
    """Derive event_existence: if S did P to O, then the event P exists.

    From a proposition with subject, predicate, and object, conclude
    that the event denoted by the predicate actually took place.
    """
    for p in propositions:
        if p.subject and p.predicate and p.polarity:
            conclusion = Proposition(
                subject=p.predicate,
                predicate="وُجِدَ",     # "existed"
                obj="",
                time=p.time,
                space=p.space,
                polarity=True,
            )
            return InferenceResult(
                rule_name="event_existence",
                premises=[p],
                conclusion=conclusion,
                confidence=0.9,
                valid=True,
            )
    return None


# ── Rule engine ─────────────────────────────────────────────────────

_DEFAULT_RULES: List[RuleFunc] = [
    _event_existence_rule,
    _transitivity_rule,
    _negation_rule,
]


class InferenceEngine:
    """A simple forward-chaining inference engine."""

    def __init__(self, rules: Optional[List[RuleFunc]] = None) -> None:
        self.rules: List[RuleFunc] = rules if rules is not None else list(_DEFAULT_RULES)

    def run(self, propositions: List[Proposition]) -> List[InferenceResult]:
        """Apply all rules once and return derived results."""
        results: List[InferenceResult] = []
        for rule in self.rules:
            result = rule(propositions)
            if result is not None:
                results.append(result)
        return results

    def run_until_fixed(
        self,
        propositions: List[Proposition],
        max_iterations: int = 10,
    ) -> List[InferenceResult]:
        """Repeatedly apply rules until no new conclusions are derived."""
        all_results: List[InferenceResult] = []
        current = list(propositions)

        for _ in range(max_iterations):
            new_results = self.run(current)
            if not new_results:
                break
            all_results.extend(new_results)
            # Add derived conclusions as new propositions
            current.extend(r.conclusion for r in new_results if r.valid)

        return all_results
