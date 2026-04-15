"""Universal / Particular Constitution v1 — دستور الكلي والجزئي v1.0.

Implements the foundational constitutional model for the universal (كلي)
and particular (جزئي) distinction across entities (ذوات) and attributes
(صفات).

Mathematical formulation
------------------------
::

    U(x) = 1  iff  ∃y₁,y₂ (y₁≠y₂ ∧ Falls_Under(y₁,x) ∧ Falls_Under(y₂,x))
    P(x) = 1  iff  ¬U(x)

    Genus(x)      ⟺  U(x) ∧ ¬∃z(U(z) ∧ Falls_Under(x,z) ∧ z ≠ x)
    Species(x)    ⟺  U(x) ∧ ∃z(Genus(z) ∧ Falls_Under(x,z))
    Individual(x) ⟺  P(x) ∧ ∃s(Species(s) ∧ Falls_Under(x,s))

    Fractal Law:
      ∀n ∈ ℕ, Layer(n) = {x : depth(x)=n} ⟹
        ∀x∈Layer(n), U(x) → ∃y∈Layer(n+1), Falls_Under(y,x)

    Boundary(a,b,type) is valid iff:
      type=GENUS_SPECIES       → Genus(a)   ∧ Species(b)    ∧ Falls_Under(b,a)
      type=SPECIES_INDIVIDUAL  → Species(a) ∧ Individual(b) ∧ Falls_Under(b,a)
      type=ENTITY_ATTRIBUTE    → Domain(a)=ENTITY ∧ Domain(b)=ATTRIBUTE

Public API
----------
* :func:`classify_universality`
* :func:`evaluate_boundary`
* :func:`validate_fractal_law`
* :func:`compute_minimum_completeness`
* :func:`build_constitution_result`
* :func:`acceptance_criteria`
* :func:`batch_classify`
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

from arabic_engine.core.enums import (
    BoundaryType,
    ConceptRelationType,
    SemanticType,
    UniversalityScope,
    UniversalParticularDomain,
    UPConstitutionOutcome,
)
from arabic_engine.core.types import (
    BoundaryRecord,
    Concept,
    ConceptRelation,
    UniversalParticularRecord,
    UPConstitutionResult,
)

# ── Internal counters ────────────────────────────────────────────────

_up_counter = 0
_bd_counter = 0
_cr_counter = 0


def _next_id(prefix: str) -> str:
    """Return the next sequential ID for *prefix*."""
    global _up_counter, _bd_counter, _cr_counter
    if prefix == "UP":
        _up_counter += 1
        return f"UP_{_up_counter:03d}"
    if prefix == "BD":
        _bd_counter += 1
        return f"BD_{_bd_counter:03d}"
    _cr_counter += 1
    return f"CR_{_cr_counter:03d}"


# ── Domain mapping ──────────────────────────────────────────────────


def _domain_from_semantic_type(
    st: SemanticType,
) -> UniversalParticularDomain:
    """Map a :class:`SemanticType` to a UP domain.

    ENTITY and EVENT map to the entity domain; ATTRIBUTE maps to
    the attribute domain.  Everything else defaults to ENTITY.
    """
    if st is SemanticType.ATTRIBUTE:
        return UniversalParticularDomain.ATTRIBUTE
    return UniversalParticularDomain.ENTITY


# ── Scope heuristics ────────────────────────────────────────────────

# Well-known genus-level labels (highest universals)
_GENUS_LABELS: frozenset[str] = frozenset({
    "حيوان", "جسم", "نبات", "جماد", "كائن", "مادة",
    "لون", "شكل", "حجم", "صوت", "رائحة", "طعم",
    "خلق", "صفة",
})

# Well-known species-level labels (intermediate universals)
_SPECIES_LABELS: frozenset[str] = frozenset({
    "إنسان", "فرس", "أسد", "طائر", "سمك", "شجرة",
    "أحمر", "أبيض", "أسود", "أخضر", "أزرق", "أصفر",
    "طويل", "قصير", "كبير", "صغير",
    "دائري", "مربع", "مستطيل",
})

# Individual markers — proper nouns, demonstrative-prefixed descriptions
_INDIVIDUAL_PREFIXES: tuple[str, ...] = (
    "هذا ", "هذه ", "ذلك ", "تلك ",
)

# Maximum label length (in characters) for an individual heuristic.
# Labels longer than this without spaces are treated as descriptive
# phrases rather than proper-noun individuals.
_MAX_INDIVIDUAL_LABEL_LENGTH = 10


def _is_genus(concept: Concept) -> bool:
    """Return True if *concept* looks like a genus (جنس)."""
    return concept.label in _GENUS_LABELS


def _is_species(concept: Concept) -> bool:
    """Return True if *concept* looks like a species (نوع)."""
    return concept.label in _SPECIES_LABELS


def _is_individual(concept: Concept) -> bool:
    """Return True if *concept* looks like an individual (فرد).

    Individuals are identified by:
    - demonstrative prefixes ("هذا الرجل", "تلك الشجرة")
    - proper nouns (short labels not in genus/species lists that are
      capitalised or not recognised as universals)
    """
    label = concept.label
    for prefix in _INDIVIDUAL_PREFIXES:
        if label.startswith(prefix):
            return True
    # If label is not recognised as genus or species, and it's a
    # relatively short token, treat it as an individual.
    if label not in _GENUS_LABELS and label not in _SPECIES_LABELS:
        # Single-word labels that don't match patterns → individual
        if " " not in label and len(label) <= _MAX_INDIVIDUAL_LABEL_LENGTH:
            return True
    return False


def _infer_scope(concept: Concept) -> UniversalityScope:
    """Infer the :class:`UniversalityScope` of a concept."""
    if _is_genus(concept):
        return UniversalityScope.GENUS
    if _is_species(concept):
        return UniversalityScope.SPECIES
    if _is_individual(concept):
        return UniversalityScope.INDIVIDUAL
    return UniversalityScope.UNRESOLVED


# ── Public API ──────────────────────────────────────────────────────


def classify_universality(
    concept: Concept,
    *,
    record_id: Optional[str] = None,
    genus_id: Optional[int] = None,
    species_id: Optional[int] = None,
    fractal_depth: Optional[int] = None,
) -> UniversalParticularRecord:
    """Classify a single concept as universal or particular.

    Determines:
    - **domain** (ENTITY or ATTRIBUTE) from the concept's semantic type
    - **scope** (GENUS / SPECIES / INDIVIDUAL / UNRESOLVED) via heuristics
    - **is_universal** (True for GENUS and SPECIES; False otherwise)
    - **boundary_markers** — boundaries this concept touches

    Parameters
    ----------
    concept : Concept
        The concept node to classify.
    record_id : str, optional
        Explicit record ID; auto-generated if omitted.
    genus_id : int, optional
        ``concept_id`` of the genus this concept belongs to.
    species_id : int, optional
        ``concept_id`` of the species (if applicable).
    fractal_depth : int, optional
        Depth in the fractal tree; auto-derived from scope if omitted.

    Returns
    -------
    UniversalParticularRecord
    """
    rid = record_id or _next_id("UP")
    domain = _domain_from_semantic_type(concept.semantic_type)
    scope = _infer_scope(concept)

    is_universal = scope in (UniversalityScope.GENUS, UniversalityScope.SPECIES)

    # Derive fractal depth from scope if not provided
    if fractal_depth is None:
        if scope is UniversalityScope.GENUS:
            fractal_depth = 0
        elif scope is UniversalityScope.SPECIES:
            fractal_depth = 1
        elif scope is UniversalityScope.INDIVIDUAL:
            fractal_depth = 2
        else:
            fractal_depth = -1  # unresolved

    # Determine boundary markers
    markers: list[BoundaryType] = []
    if is_universal:
        markers.append(BoundaryType.UNIVERSAL_PARTICULAR)
    if scope is UniversalityScope.GENUS:
        markers.append(BoundaryType.GENUS_SPECIES)
    elif scope is UniversalityScope.SPECIES:
        markers.append(BoundaryType.GENUS_SPECIES)
        markers.append(BoundaryType.SPECIES_INDIVIDUAL)
    elif scope is UniversalityScope.INDIVIDUAL:
        markers.append(BoundaryType.SPECIES_INDIVIDUAL)
    if domain is UniversalParticularDomain.ATTRIBUTE:
        markers.append(BoundaryType.ENTITY_ATTRIBUTE)

    return UniversalParticularRecord(
        record_id=rid,
        concept_id=concept.concept_id,
        label=concept.label,
        domain=domain,
        scope=scope,
        is_universal=is_universal,
        boundary_markers=tuple(markers),
        genus_id=genus_id,
        species_id=species_id,
        fractal_depth=fractal_depth,
    )


def batch_classify(
    concepts: List[Concept],
) -> List[UniversalParticularRecord]:
    """Classify a list of concepts (convenience wrapper).

    Parameters
    ----------
    concepts : list[Concept]
        Concepts to classify.

    Returns
    -------
    list[UniversalParticularRecord]
    """
    return [classify_universality(c) for c in concepts]


# ── Boundary evaluation ─────────────────────────────────────────────

# Valid scope transitions for each boundary type
_VALID_BOUNDARY_SCOPES: Dict[
    BoundaryType,
    Set[Tuple[UniversalityScope, UniversalityScope]],
] = {
    BoundaryType.GENUS_SPECIES: {
        (UniversalityScope.GENUS, UniversalityScope.SPECIES),
    },
    BoundaryType.SPECIES_INDIVIDUAL: {
        (UniversalityScope.SPECIES, UniversalityScope.INDIVIDUAL),
    },
    BoundaryType.UNIVERSAL_PARTICULAR: {
        (UniversalityScope.GENUS, UniversalityScope.INDIVIDUAL),
        (UniversalityScope.SPECIES, UniversalityScope.INDIVIDUAL),
        (UniversalityScope.GENUS, UniversalityScope.SPECIES),
    },
    BoundaryType.ENTITY_ATTRIBUTE: set(),  # checked by domain, not scope
    BoundaryType.GENERAL_DESCRIPTION_SPECIFIC_FORM: {
        (UniversalityScope.GENUS, UniversalityScope.INDIVIDUAL),
        (UniversalityScope.SPECIES, UniversalityScope.INDIVIDUAL),
    },
}


def evaluate_boundary(
    left: Concept,
    right: Concept,
    boundary_type: BoundaryType,
    *,
    boundary_id: Optional[str] = None,
) -> BoundaryRecord:
    """Check whether two concepts correctly respect a given boundary.

    Parameters
    ----------
    left : Concept
        The "higher" or "left" side of the boundary.
    right : Concept
        The "lower" or "right" side of the boundary.
    boundary_type : BoundaryType
        The type of boundary to enforce.
    boundary_id : str, optional
        Explicit ID; auto-generated if omitted.

    Returns
    -------
    BoundaryRecord
    """
    bid = boundary_id or _next_id("BD")
    left_rec = classify_universality(left)
    right_rec = classify_universality(right)

    # Entity↔Attribute boundary: domains must differ
    if boundary_type is BoundaryType.ENTITY_ATTRIBUTE:
        valid = left_rec.domain is not right_rec.domain
        reason = None if valid else (
            f"Both concepts are in the same domain: {left_rec.domain.name}"
        )
        return BoundaryRecord(
            boundary_id=bid,
            boundary_type=boundary_type,
            left_concept_id=left.concept_id,
            right_concept_id=right.concept_id,
            is_valid=valid,
            violation_reason=reason,
        )

    # Scope-based boundaries
    pair = (left_rec.scope, right_rec.scope)
    valid_pairs = _VALID_BOUNDARY_SCOPES.get(boundary_type, set())
    valid = pair in valid_pairs
    reason = None if valid else (
        f"Scope pair ({left_rec.scope.name}, {right_rec.scope.name}) "
        f"is invalid for boundary {boundary_type.name}"
    )
    return BoundaryRecord(
        boundary_id=bid,
        boundary_type=boundary_type,
        left_concept_id=left.concept_id,
        right_concept_id=right.concept_id,
        is_valid=valid,
        violation_reason=reason,
    )


# ── Fractal law ─────────────────────────────────────────────────────


def validate_fractal_law(
    records: List[UniversalParticularRecord],
) -> bool:
    """Validate the fractal law across a set of UP records.

    The fractal law states:
    - Every universal at depth *n* must have at least one child at depth *n+1*
    - Every particular (individual) must trace back to a universal

    Parameters
    ----------
    records : list[UniversalParticularRecord]
        The classified records to check.

    Returns
    -------
    bool
        ``True`` if the fractal law holds.
    """
    if not records:
        return True

    # Group by depth
    by_depth: Dict[int, List[UniversalParticularRecord]] = {}
    for r in records:
        by_depth.setdefault(r.fractal_depth, []).append(r)

    # Every universal must have a descendant at the next depth level
    for depth, layer in sorted(by_depth.items()):
        next_layer = by_depth.get(depth + 1, [])
        for rec in layer:
            if rec.is_universal and rec.scope is not UniversalityScope.UNRESOLVED:
                # There must be at least one record at depth+1
                if not next_layer:
                    return False

    # Every individual must have a genus or species above it
    individuals = [r for r in records if r.scope is UniversalityScope.INDIVIDUAL]
    universals = [r for r in records if r.is_universal]
    for ind in individuals:
        if not universals:
            return False
        # At least one universal must exist at a shallower depth
        if not any(u.fractal_depth < ind.fractal_depth for u in universals):
            return False

    return True


# ── Minimum completeness ────────────────────────────────────────────


def compute_minimum_completeness(
    records: List[UniversalParticularRecord],
) -> bool:
    """Check whether the minimum viable structure exists.

    Minimum = at least one genus, at least one species, at least one
    individual, forming a chain genus → species → individual.

    Parameters
    ----------
    records : list[UniversalParticularRecord]

    Returns
    -------
    bool
    """
    has_genus = any(r.scope is UniversalityScope.GENUS for r in records)
    has_species = any(r.scope is UniversalityScope.SPECIES for r in records)
    has_individual = any(r.scope is UniversalityScope.INDIVIDUAL for r in records)
    return has_genus and has_species and has_individual


# ── Acceptance criteria ─────────────────────────────────────────────


def acceptance_criteria(
    result: UPConstitutionResult,
) -> UPConstitutionOutcome:
    """Derive the constitutional outcome from a result.

    - No boundary violations + fractal law + minimum completeness → ACCEPTED
    - Any boundary violation → REJECTED
    - Otherwise → INCOMPLETE

    Parameters
    ----------
    result : UPConstitutionResult

    Returns
    -------
    UPConstitutionOutcome
    """
    # Any boundary violation → REJECTED
    if any(not b.is_valid for b in result.boundaries):
        return UPConstitutionOutcome.REJECTED

    # Any errors → REJECTED
    if result.errors:
        return UPConstitutionOutcome.REJECTED

    records = list(result.records)
    fractal_ok = validate_fractal_law(records)
    complete = compute_minimum_completeness(records)

    if fractal_ok and complete:
        return UPConstitutionOutcome.ACCEPTED
    return UPConstitutionOutcome.INCOMPLETE


# ── End-to-end builder ──────────────────────────────────────────────


def build_constitution_result(
    concepts: List[Concept],
    relations: List[ConceptRelation],
    *,
    result_id: Optional[str] = None,
) -> UPConstitutionResult:
    """Build a full constitutional result from concepts and relations.

    Steps:
    1. Classify all concepts
    2. Build genus/species links from IS_A and INSTANTIATES relations
    3. Evaluate boundaries between linked concept pairs
    4. Check fractal law and completeness
    5. Return the verdict

    Parameters
    ----------
    concepts : list[Concept]
        All concepts in the analysis scope.
    relations : list[ConceptRelation]
        Inter-concept relations (IS_A, INSTANTIATES, etc.).
    result_id : str, optional
        Explicit ID; auto-generated if omitted.

    Returns
    -------
    UPConstitutionResult
    """
    rid = result_id or _next_id("CR")

    # Build a lookup by concept_id
    concept_by_id: Dict[int, Concept] = {c.concept_id: c for c in concepts}

    # Classify all concepts
    records = batch_classify(concepts)
    rec_by_id: Dict[int, UniversalParticularRecord] = {
        r.concept_id: r for r in records
    }

    # Evaluate boundaries from relations
    boundaries: list[BoundaryRecord] = []
    errors: list[str] = []

    for rel in relations:
        src = concept_by_id.get(rel.source_id)
        tgt = concept_by_id.get(rel.target_id)
        if src is None or tgt is None:
            errors.append(
                f"Relation references unknown concept: "
                f"{rel.source_id} -> {rel.target_id}"
            )
            continue

        src_rec = rec_by_id.get(rel.source_id)
        tgt_rec = rec_by_id.get(rel.target_id)
        if src_rec is None or tgt_rec is None:
            continue

        # Determine boundary type from relation + scopes
        if rel.relation_type is ConceptRelationType.IS_A:
            # IS_A: target is the genus/species, source is the sub-type
            if tgt_rec.scope is UniversalityScope.GENUS:
                btype = BoundaryType.GENUS_SPECIES
            else:
                btype = BoundaryType.UNIVERSAL_PARTICULAR
            boundaries.append(evaluate_boundary(tgt, src, btype))

        elif rel.relation_type is ConceptRelationType.INSTANTIATES:
            # INSTANTIATES: source is an individual of target (a species)
            btype = BoundaryType.SPECIES_INDIVIDUAL
            boundaries.append(evaluate_boundary(tgt, src, btype))

    # Cross-domain boundaries (entity ↔ attribute).
    # We only sample one representative pair because the entity↔attribute
    # boundary is domain-level (not concept-level): if one entity and one
    # attribute exist in different domains, the boundary holds for all.
    entity_concepts = [
        c for c in concepts
        if rec_by_id[c.concept_id].domain is UniversalParticularDomain.ENTITY
    ]
    attr_concepts = [
        c for c in concepts
        if rec_by_id[c.concept_id].domain is UniversalParticularDomain.ATTRIBUTE
    ]
    for ec in entity_concepts[:1]:
        for ac in attr_concepts[:1]:
            boundaries.append(
                evaluate_boundary(ec, ac, BoundaryType.ENTITY_ATTRIBUTE)
            )

    # Compute max fractal depth
    max_depth = max((r.fractal_depth for r in records), default=0)

    # Derive outcome
    fractal_ok = validate_fractal_law(records)
    complete = compute_minimum_completeness(records)

    if any(not b.is_valid for b in boundaries) or errors:
        outcome = UPConstitutionOutcome.REJECTED
    elif fractal_ok and complete:
        outcome = UPConstitutionOutcome.ACCEPTED
    else:
        outcome = UPConstitutionOutcome.INCOMPLETE

    return UPConstitutionResult(
        result_id=rid,
        records=tuple(records),
        boundaries=tuple(boundaries),
        outcome=outcome,
        fractal_depth_max=max_depth,
        errors=tuple(errors),
    )
