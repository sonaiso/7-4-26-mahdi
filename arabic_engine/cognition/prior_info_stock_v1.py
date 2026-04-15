"""prior_info_stock_v1 — إثبات ضرورة المخزون المعلوماتي السابق قبل التركيب

Proof of the Necessity of Prior Informational Stock Before Composition v1.

This module formalises the three ordered readiness conditions that a
percept must satisfy before entering syntactic composition:

    1. شرط الإمكان الإدراكي  — Perceptual Readiness   (Ready₁)
    2. شرط الإمكان التركيبي  — Compositional Readiness (Ready₂)
    3. شرط الإمكان القضوي   — Propositional Readiness (Ready₃)

The prior informational stock (المخزون المعلوماتي السابق) is the set of
pre-existing knowledge, classifications, and criteria that interpret a
raw percept/utterance into a concept fit for composition.

Mathematical model (Article 48)::

    IS = (X, K, Cl, Ln, Ref, Role, Ready₁, Ready₂, Ready₃)

Public API
----------
* :func:`evaluate_stock_sufficiency`
* :func:`evaluate_perceptual_readiness`
* :func:`evaluate_compositional_readiness`
* :func:`evaluate_propositional_readiness`
* :func:`build_informational_stock_record`
* :func:`batch_evaluate`
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from arabic_engine.core.enums import (
    InterpretationSource,
    PerceptualGapReason,
    ReadinessLevel,
    ReadinessStatus,
    StockComponent,
    StockSufficiency,
)
from arabic_engine.core.types import (
    CompositionalReadinessResult,
    InformationalStockRecord,
    PerceptualReadinessResult,
    PriorInformationalStock,
    ReadinessGate,
)

# ── Thresholds (θ₁, θ₂, θ₃) ───────────────────────────────────────────

_DEFAULT_PERCEPTUAL_THRESHOLD: float = 0.5
_DEFAULT_COMPOSITIONAL_THRESHOLD: float = 0.5
_DEFAULT_PROPOSITIONAL_THRESHOLD: float = 0.5

# ── Component weights ──────────────────────────────────────────────────

_COMPONENT_WEIGHTS: Dict[StockComponent, float] = {
    StockComponent.REALITY_INFO: 1.0,
    StockComponent.PRIOR_CLASSIFICATION: 1.0,
    StockComponent.PRIMARY_LANGUAGE: 1.0,
    StockComponent.CATEGORY_BOUNDARY: 1.0,
    StockComponent.REFERENCE_KNOWLEDGE: 1.0,
    StockComponent.PREDICATION_CRITERION: 1.0,
    StockComponent.USAGE_MODE_CRITERION: 1.0,
}

# Total number of stock components (Article 5)
_TOTAL_COMPONENTS = len(StockComponent)

# ── ID counters ─────────────────────────────────────────────────────────

_is_counter = 0


def _next_id(prefix: str) -> str:
    """Return the next sequential ID for *prefix*."""
    global _is_counter
    _is_counter += 1
    return f"{prefix}_{_is_counter:03d}"


# ── Private helpers ─────────────────────────────────────────────────────


def _score_stock_coverage(stock: PriorInformationalStock) -> float:
    """Compute the weighted coverage ratio of the 7 stock components.

    Returns a value in [0.0, 1.0] representing how many of the seven
    required stock components are represented in *stock*.
    """
    if not stock.entries:
        return 0.0

    present: set[StockComponent] = set()
    weighted_sum = 0.0
    total_weight = sum(_COMPONENT_WEIGHTS.values())

    for entry in stock.entries:
        if entry.component not in present:
            present.add(entry.component)
            weighted_sum += _COMPONENT_WEIGHTS.get(entry.component, 1.0)

    return weighted_sum / total_weight if total_weight > 0 else 0.0


def _check_perceptual_gaps(
    stock: PriorInformationalStock,
) -> Tuple[PerceptualGapReason, ...]:
    """Identify which perceptual-gap reasons apply given the stock.

    Returns a tuple of :class:`PerceptualGapReason` values describing
    why a percept would fail perceptual readiness.
    """
    gaps: list[PerceptualGapReason] = []
    present = {e.component for e in stock.entries}

    # No language knowledge → ambiguous interpretation
    if StockComponent.PRIMARY_LANGUAGE not in present:
        gaps.append(PerceptualGapReason.AMBIGUOUS)

    # No classification → unclassified
    if StockComponent.PRIOR_CLASSIFICATION not in present:
        gaps.append(PerceptualGapReason.UNCLASSIFIED)

    # No category boundaries → polysemous (cannot distinguish entity/attr/event)
    if StockComponent.CATEGORY_BOUNDARY not in present:
        gaps.append(PerceptualGapReason.POLYSEMOUS)

    # No reality info → unfit for composition
    if StockComponent.REALITY_INFO not in present:
        gaps.append(PerceptualGapReason.UNFIT_FOR_COMPOSITION)

    return tuple(gaps)


def _gap_reasons_to_strings(
    gaps: Tuple[PerceptualGapReason, ...],
) -> Tuple[str, ...]:
    """Convert gap-reason enums to human-readable strings."""
    _LABELS: Dict[PerceptualGapReason, str] = {
        PerceptualGapReason.AMBIGUOUS: "مبهم — ambiguous without language knowledge",
        PerceptualGapReason.UNCLASSIFIED: "غير مصنف — unclassified without prior classification",
        PerceptualGapReason.POLYSEMOUS: "مشترك — polysemous without category boundaries",
        PerceptualGapReason.UNFIT_FOR_COMPOSITION: "غير قابل للتركيب — unfit without reality info",
    }
    return tuple(_LABELS.get(g, g.name) for g in gaps)


# ── Public API ──────────────────────────────────────────────────────────


def evaluate_stock_sufficiency(
    stock: PriorInformationalStock,
) -> StockSufficiency:
    """Evaluate whether *stock* meets the 8 minimum completeness criteria.

    Articles 32-40 enumerate eight conditions:
      1. Existence (ثبوت)         — at least one entry exists
      2. Boundary (حد)           — entries are typed, not raw
      3. Extension (امتداد)       — covers reality, language, concept, etc.
      4. Constituent (مقوِّم)      — contains info, classifications, criteria
      5. Structural relation (علاقة) — entries linked to interpretation sources
      6. Regularity (انتظام)       — no contradictory duplicates
      7. Unity (وحدة)             — entries form a coherent interpretation
      8. Assignability (تعيين)     — coverage score ≥ 1.0 (all 7 components)

    Returns
    -------
    StockSufficiency
        SUFFICIENT if all criteria hold, INSUFFICIENT if the stock is
        empty or critically incomplete, UNDETERMINED otherwise.
    """
    # 1. Existence — must have at least one entry
    if not stock.entries:
        return StockSufficiency.INSUFFICIENT

    # Collect represented components
    present = {e.component for e in stock.entries}

    # 2. Boundary — every entry must have a typed component (guaranteed by enum)
    # 3. Extension — must cover reality, language, concept (ref knowledge),
    #    role (predication criterion)
    required_for_extension = {
        StockComponent.REALITY_INFO,
        StockComponent.PRIMARY_LANGUAGE,
        StockComponent.REFERENCE_KNOWLEDGE,
        StockComponent.PREDICATION_CRITERION,
    }

    # 4. Constituent — needs classification + criteria
    required_for_constituent = {
        StockComponent.PRIOR_CLASSIFICATION,
        StockComponent.CATEGORY_BOUNDARY,
    }

    # 5. Structural relation — at least one entry has a non-REALITY source
    has_structural_link = any(
        e.source != InterpretationSource.REALITY for e in stock.entries
    )

    # 6. Regularity — no contradictory duplicates (simplified: unique per component)
    # 7. Unity — coherent interpretation (simplified: positive weights)
    has_positive_weights = all(e.weight > 0 for e in stock.entries)

    # 8. Assignability — all 7 components present
    all_present = present == set(StockComponent)

    if all_present and has_structural_link and has_positive_weights:
        return StockSufficiency.SUFFICIENT

    # Check if critically incomplete
    missing_extension = required_for_extension - present
    missing_constituent = required_for_constituent - present

    if missing_extension or missing_constituent:
        return StockSufficiency.INSUFFICIENT

    return StockSufficiency.UNDETERMINED


def evaluate_perceptual_readiness(
    percept_id: str,
    stock: PriorInformationalStock,
    *,
    threshold: float = _DEFAULT_PERCEPTUAL_THRESHOLD,
) -> PerceptualReadinessResult:
    """Evaluate perceptual readiness (Ready₁) for a percept.

    Implements Ready₁ = f(X, K, Cl, Ln) from Article 49.

    A percept is perceptually ready when its prior informational stock
    provides sufficient coverage to interpret it beyond raw sense/utterance.

    Parameters
    ----------
    percept_id : str
        Identifier of the percept being evaluated.
    stock : PriorInformationalStock
        The prior informational stock.
    threshold : float
        Minimum score to achieve MET status (default 0.5).

    Returns
    -------
    PerceptualReadinessResult
        Contains the readiness gate and optional interpreted concept.
    """
    score = _score_stock_coverage(stock)
    gaps = _check_perceptual_gaps(stock)
    gap_strings = _gap_reasons_to_strings(gaps)

    if score >= threshold and not gaps:
        status = ReadinessStatus.MET
    elif score >= threshold:
        status = ReadinessStatus.PARTIAL
    else:
        status = ReadinessStatus.UNMET

    gate = ReadinessGate(
        level=ReadinessLevel.PERCEPTUAL,
        status=status,
        score=score,
        threshold=threshold,
        gap_reasons=gap_strings,
    )

    interpreted = percept_id if status == ReadinessStatus.MET else None

    return PerceptualReadinessResult(
        percept_id=percept_id,
        gate=gate,
        interpreted_concept=interpreted,
    )


def evaluate_compositional_readiness(
    percept_id: str,
    perceptual_result: PerceptualReadinessResult,
    reference: str,
    role: str,
    *,
    threshold: float = _DEFAULT_COMPOSITIONAL_THRESHOLD,
) -> CompositionalReadinessResult:
    """Evaluate compositional readiness (Ready₂) for a percept.

    Implements Ready₂ = g(Ready₁, Ref, Role) from Article 50.

    Requires Ready₁ ≥ θ₁ as a prerequisite (Article 12).

    Parameters
    ----------
    percept_id : str
        Identifier of the percept.
    perceptual_result : PerceptualReadinessResult
        Result of perceptual readiness evaluation.
    reference : str
        Reference / predication for the percept.
    role : str
        Candidate role for the percept.
    threshold : float
        Minimum score to achieve MET status (default 0.5).

    Returns
    -------
    CompositionalReadinessResult
        Contains the readiness gate and optional role / reference info.
    """
    gap_reasons: list[str] = []

    # Prerequisite: Ready₁ must be MET
    if perceptual_result.gate.status != ReadinessStatus.MET:
        gap_reasons.append(
            "Ready₁ prerequisite not met — perceptual readiness is "
            f"{perceptual_result.gate.status.name}"
        )
        gate = ReadinessGate(
            level=ReadinessLevel.COMPOSITIONAL,
            status=ReadinessStatus.UNMET,
            score=0.0,
            threshold=threshold,
            gap_reasons=tuple(gap_reasons),
        )
        return CompositionalReadinessResult(
            percept_id=percept_id,
            gate=gate,
        )

    # Compute score from Ready₁ score + reference + role presence
    base = perceptual_result.gate.score
    ref_bonus = 0.25 if reference else 0.0
    role_bonus = 0.25 if role else 0.0
    score = min(1.0, base * 0.5 + ref_bonus + role_bonus)

    if not reference:
        gap_reasons.append("reference not resolved")
    if not role:
        gap_reasons.append("candidate role not assigned")

    if score >= threshold and not gap_reasons:
        status = ReadinessStatus.MET
    elif score >= threshold:
        status = ReadinessStatus.PARTIAL
    else:
        status = ReadinessStatus.UNMET

    gate = ReadinessGate(
        level=ReadinessLevel.COMPOSITIONAL,
        status=status,
        score=score,
        threshold=threshold,
        gap_reasons=tuple(gap_reasons),
    )

    return CompositionalReadinessResult(
        percept_id=percept_id,
        gate=gate,
        assigned_role=role if role else None,
        reference_resolved=bool(reference),
    )


def evaluate_propositional_readiness(
    compositional_result: CompositionalReadinessResult,
    predicate_closed: bool,
    conflict_resolved: bool,
    *,
    threshold: float = _DEFAULT_PROPOSITIONAL_THRESHOLD,
) -> ReadinessGate:
    """Evaluate propositional readiness (Ready₃).

    Implements Ready₃ = h(Ready₂, PredicateClosure, ConflictResolution)
    from Article 51.

    Requires Ready₂ ≥ θ₂ as a prerequisite (Article 16).

    Parameters
    ----------
    compositional_result : CompositionalReadinessResult
        Result of compositional readiness evaluation.
    predicate_closed : bool
        Whether the predicate/attribution is closed.
    conflict_resolved : bool
        Whether any conflicts have been resolved.
    threshold : float
        Minimum score to achieve MET status (default 0.5).

    Returns
    -------
    ReadinessGate
        The propositional readiness gate.
    """
    gap_reasons: list[str] = []

    # Prerequisite: Ready₂ must be MET
    if compositional_result.gate.status != ReadinessStatus.MET:
        gap_reasons.append(
            "Ready₂ prerequisite not met — compositional readiness is "
            f"{compositional_result.gate.status.name}"
        )
        return ReadinessGate(
            level=ReadinessLevel.PROPOSITIONAL,
            status=ReadinessStatus.UNMET,
            score=0.0,
            threshold=threshold,
            gap_reasons=tuple(gap_reasons),
        )

    # Compute score
    base = compositional_result.gate.score
    pred_bonus = 0.3 if predicate_closed else 0.0
    conf_bonus = 0.2 if conflict_resolved else 0.0
    score = min(1.0, base * 0.5 + pred_bonus + conf_bonus)

    if not predicate_closed:
        gap_reasons.append("predicate not closed — attribution incomplete")
    if not conflict_resolved:
        gap_reasons.append("conflict not resolved")

    if score >= threshold and not gap_reasons:
        status = ReadinessStatus.MET
    elif score >= threshold:
        status = ReadinessStatus.PARTIAL
    else:
        status = ReadinessStatus.UNMET

    return ReadinessGate(
        level=ReadinessLevel.PROPOSITIONAL,
        status=status,
        score=score,
        threshold=threshold,
        gap_reasons=tuple(gap_reasons),
    )


def build_informational_stock_record(
    percept_id: str,
    stock: PriorInformationalStock,
    classification: str,
    linguistic_direction: str,
    reference: str,
    role: str,
    *,
    predicate_closed: bool = False,
    conflict_resolved: bool = False,
    record_id: str = "",
    perceptual_threshold: float = _DEFAULT_PERCEPTUAL_THRESHOLD,
    compositional_threshold: float = _DEFAULT_COMPOSITIONAL_THRESHOLD,
    propositional_threshold: float = _DEFAULT_PROPOSITIONAL_THRESHOLD,
) -> InformationalStockRecord:
    """Build the full IS 9-tuple record (Article 48).

    This is the main entry-point that evaluates all three readiness levels
    and assembles the ``IS = (X, K, Cl, Ln, Ref, Role, Ready₁, Ready₂, Ready₃)``
    tuple.

    Parameters
    ----------
    percept_id : str
        X — the percept / datum identifier.
    stock : PriorInformationalStock
        K — the prior informational stock.
    classification : str
        Cl — classification / interpretation result.
    linguistic_direction : str
        Ln — linguistic / semantic direction.
    reference : str
        Ref — reference / predication.
    role : str
        Role — candidate role.
    predicate_closed : bool
        Whether the predicate is closed for propositional readiness.
    conflict_resolved : bool
        Whether conflicts are resolved for propositional readiness.
    record_id : str
        Optional explicit record ID; auto-generated if empty.
    perceptual_threshold : float
        θ₁ threshold for perceptual readiness.
    compositional_threshold : float
        θ₂ threshold for compositional readiness.
    propositional_threshold : float
        θ₃ threshold for propositional readiness.

    Returns
    -------
    InformationalStockRecord
        The complete IS record with all three readiness gates evaluated.
    """
    # Step 1: Perceptual readiness  (Ready₁)
    r1 = evaluate_perceptual_readiness(
        percept_id, stock, threshold=perceptual_threshold
    )

    # Step 2: Compositional readiness (Ready₂)
    r2 = evaluate_compositional_readiness(
        percept_id, r1, reference, role, threshold=compositional_threshold
    )

    # Step 3: Propositional readiness (Ready₃)
    r3 = evaluate_propositional_readiness(
        r2, predicate_closed, conflict_resolved, threshold=propositional_threshold
    )

    rid = record_id or _next_id("IS")

    return InformationalStockRecord(
        record_id=rid,
        percept_id=percept_id,
        stock=stock,
        classification=classification,
        linguistic_direction=linguistic_direction,
        reference=reference,
        candidate_role=role,
        ready_1=r1.gate,
        ready_2=r2.gate,
        ready_3=r3,
    )


# ── Batch processing ───────────────────────────────────────────────────


def batch_evaluate(
    inputs: Sequence[
        tuple[str, PriorInformationalStock, str, str, str, str, bool, bool]
    ],
) -> List[InformationalStockRecord]:
    """Build IS records for multiple percepts.

    Each element of *inputs* is an 8-tuple:
      ``(percept_id, stock, classification, linguistic_direction,
        reference, role, predicate_closed, conflict_resolved)``

    Parameters
    ----------
    inputs : Sequence[tuple]
        Batch of input tuples.

    Returns
    -------
    List[InformationalStockRecord]
        One record per input.
    """
    return [
        build_informational_stock_record(
            percept_id=item[0],
            stock=item[1],
            classification=item[2],
            linguistic_direction=item[3],
            reference=item[4],
            role=item[5],
            predicate_closed=item[6],
            conflict_resolved=item[7],
        )
        for item in inputs
    ]
