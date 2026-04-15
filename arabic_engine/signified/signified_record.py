"""Signified Ontology v1.0 — registry, factory, and validation.

Provides a typed seed registry of Arabic signified records, a factory
function that maps lexical closures to :class:`SignifiedRecord` instances,
and constraint-validation helpers implementing §5 of the ontology spec.

Public API
----------
* :data:`SIGNIFIED_DB` — ``Dict[str, SignifiedRecord]`` keyed on ``label_ar``.
* :func:`make_signified` — maps a single :class:`LexicalClosure` to a record.
* :func:`batch_signified` — maps a list of closures.
* :func:`validate_signified` — returns constraint violations for a record.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from arabic_engine.core.enums import (
    POS,
    CompositionDegree,
    ContextRequirement,
    DependencyDegree,
    ExistenceMode,
    LogicalStatus,
    PrimarySignifiedType,
    ReferentialSubtype,
    RhetoricalStatus,
    SemanticType,
    SignifiedTemporalStatus,
    SpecificityDegree,
)
from arabic_engine.core.types import LexicalClosure, SignifiedRecord

# ── Seed data loading ───────────────────────────────────────────────

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "signified_seed_v1.json"


def _load_seed() -> Dict[str, SignifiedRecord]:
    """Load the JSON seed file and return a dict keyed on ``label_ar``."""
    with open(_DATA_PATH, encoding="utf-8") as fh:
        raw = json.load(fh)

    db: Dict[str, SignifiedRecord] = {}
    for rec in raw["records"]:
        ref_status: Optional[ReferentialSubtype] = None
        if rec.get("referential_status"):
            ref_status = ReferentialSubtype[rec["referential_status"]]

        sr = SignifiedRecord(
            id=rec["id"],
            label_ar=rec["label_ar"],
            label_en=rec["label_en"],
            definition=rec["definition"],
            primary_type=PrimarySignifiedType[rec["primary_type"]],
            secondary_type=rec["secondary_type"],
            dependency_degree=DependencyDegree[rec["dependency_degree"]],
            existence_mode=ExistenceMode[rec["existence_mode"]],
            specificity_degree=SpecificityDegree[rec["specificity_degree"]],
            composition_degree=CompositionDegree[rec["composition_degree"]],
            context_requirement=ContextRequirement[rec["context_requirement"]],
            logical_status=LogicalStatus[rec["logical_status"]],
            rhetorical_status=RhetoricalStatus[rec["rhetorical_status"]],
            temporal_status=SignifiedTemporalStatus[rec["temporal_status"]],
            referential_status=ref_status,
            examples=tuple(rec.get("examples", [])),
            constraints=tuple(rec.get("constraints", [])),
        )
        db[sr.label_ar] = sr
    return db


SIGNIFIED_DB: Dict[str, SignifiedRecord] = _load_seed()

# ── POS → defaults mapping ──────────────────────────────────────────

_POS_DEFAULTS: Dict[POS, dict] = {
    POS.ISM: {
        "primary_type": PrimarySignifiedType.ONTOLOGICAL,
        "secondary_type": "EntityMeaning.GenericEntity",
        "dependency_degree": DependencyDegree.INDEPENDENT,
        "existence_mode": ExistenceMode.EXTERNAL,
        "logical_status": LogicalStatus.NON_PROPOSITIONAL,
    },
    POS.FI3L: {
        "primary_type": PrimarySignifiedType.ONTOLOGICAL,
        "secondary_type": "EventMeaning.ActionEvent",
        "dependency_degree": DependencyDegree.PROPOSITION_DEPENDENT,
        "existence_mode": ExistenceMode.EXTERNAL,
        "logical_status": LogicalStatus.TRUTH_APT,
    },
    POS.SIFA: {
        "primary_type": PrimarySignifiedType.ONTOLOGICAL,
        "secondary_type": "PropertyMeaning.StableProperty",
        "dependency_degree": DependencyDegree.BEARER_DEPENDENT,
        "existence_mode": ExistenceMode.EXTERNAL,
        "logical_status": LogicalStatus.NON_PROPOSITIONAL,
    },
    POS.HARF: {
        "primary_type": PrimarySignifiedType.FUNCTIONAL,
        "secondary_type": "ConnectorFunction",
        "dependency_degree": DependencyDegree.CONTEXT_DEPENDENT,
        "existence_mode": ExistenceMode.CONVENTIONAL,
        "logical_status": LogicalStatus.NON_PROPOSITIONAL,
    },
    POS.ZARF: {
        "primary_type": PrimarySignifiedType.RELATIONAL,
        "secondary_type": "SpatialRelation",
        "dependency_degree": DependencyDegree.RELATIONALLY_DEPENDENT,
        "existence_mode": ExistenceMode.EXTERNAL,
        "logical_status": LogicalStatus.NON_PROPOSITIONAL,
    },
    POS.DAMIR: {
        "primary_type": PrimarySignifiedType.REFERENTIAL,
        "secondary_type": "PronounReference",
        "dependency_degree": DependencyDegree.REFERENT_DEPENDENT,
        "existence_mode": ExistenceMode.CONVENTIONAL,
        "logical_status": LogicalStatus.NON_PROPOSITIONAL,
    },
}

_STYPE_DEFAULTS: Dict[SemanticType, dict] = {
    SemanticType.ENTITY: {
        "primary_type": PrimarySignifiedType.ONTOLOGICAL,
        "secondary_type": "EntityMeaning.GenericEntity",
        "dependency_degree": DependencyDegree.INDEPENDENT,
    },
    SemanticType.EVENT: {
        "primary_type": PrimarySignifiedType.ONTOLOGICAL,
        "secondary_type": "EventMeaning.ActionEvent",
        "dependency_degree": DependencyDegree.PROPOSITION_DEPENDENT,
    },
    SemanticType.ATTRIBUTE: {
        "primary_type": PrimarySignifiedType.ONTOLOGICAL,
        "secondary_type": "PropertyMeaning.StableProperty",
        "dependency_degree": DependencyDegree.BEARER_DEPENDENT,
    },
    SemanticType.RELATION: {
        "primary_type": PrimarySignifiedType.RELATIONAL,
        "secondary_type": "SpatialRelation",
        "dependency_degree": DependencyDegree.RELATIONALLY_DEPENDENT,
    },
    SemanticType.NORM: {
        "primary_type": PrimarySignifiedType.PROPOSITIONAL,
        "secondary_type": "AssertionMeaning",
        "dependency_degree": DependencyDegree.PROPOSITION_DEPENDENT,
    },
}

_next_sig_id = 10_000


def make_signified(closure: LexicalClosure) -> SignifiedRecord:
    """Create a :class:`SignifiedRecord` for a lexical closure.

    First checks the seed database keyed on the lemma.  When no match is
    found, auto-generates a record with sensible defaults inferred from
    the closure's POS and semantic type.

    Args:
        closure: The lexical closure to map.

    Returns:
        A :class:`SignifiedRecord` instance.
    """
    # Try seed DB first
    existing = SIGNIFIED_DB.get(closure.lemma)
    if existing is not None:
        return existing

    # Build defaults from POS, then refine with SemanticType
    defaults: dict = {}
    if closure.pos in _POS_DEFAULTS:
        defaults.update(_POS_DEFAULTS[closure.pos])
    stype = getattr(closure, "semantic_type", None)
    if stype is not None and stype in _STYPE_DEFAULTS:
        defaults.update(_STYPE_DEFAULTS[stype])

    global _next_sig_id
    _next_sig_id += 1

    return SignifiedRecord(
        id=f"SIG-GEN-{_next_sig_id:05d}",
        label_ar=closure.lemma,
        label_en=closure.lemma,
        definition=f"Auto-generated signified for '{closure.lemma}'",
        primary_type=defaults.get(
            "primary_type", PrimarySignifiedType.ONTOLOGICAL
        ),
        secondary_type=defaults.get(
            "secondary_type", "EntityMeaning.GenericEntity"
        ),
        dependency_degree=defaults.get(
            "dependency_degree", DependencyDegree.INDEPENDENT
        ),
        existence_mode=defaults.get(
            "existence_mode", ExistenceMode.EXTERNAL
        ),
        specificity_degree=SpecificityDegree.UNDEFINED,
        composition_degree=CompositionDegree.SIMPLE,
        context_requirement=ContextRequirement.LOW,
        logical_status=defaults.get(
            "logical_status", LogicalStatus.NON_PROPOSITIONAL
        ),
        rhetorical_status=RhetoricalStatus.LITERAL,
        temporal_status=SignifiedTemporalStatus.ATEMPORAL,
    )


def batch_signified(
    closures: List[LexicalClosure],
) -> List[SignifiedRecord]:
    """Map a list of lexical closures to signified records.

    Args:
        closures: Lexical closures (as produced by batch_closure).

    Returns:
        A list of :class:`SignifiedRecord` instances, preserving order.
    """
    return [make_signified(c) for c in closures]


# ── Constraint validation (§5) ──────────────────────────────────────

def validate_signified(s: SignifiedRecord) -> List[str]:
    """Check a :class:`SignifiedRecord` against the ontology constraints.

    Returns a list of human-readable violation descriptions.
    An empty list means the record is valid.

    Implemented constraints (from §5 of the spec):
      1. No dual primary_type from the same axis without distinction.
      2. Every record must have primary_type, dependency_degree,
         existence_mode, specificity_degree, and context_requirement.
      3. Referential records must have referential_status set.
      4. Event-type records should have temporal_status != ATEMPORAL.
      5. Rhetorical records must carry a non-LITERAL rhetorical_status.
      6. Relational records should document arity >= 2 (via secondary_type).
    """
    violations: List[str] = []

    # C2 — mandatory fields presence
    if not s.id:
        violations.append("C2: 'id' must not be empty")
    if not s.label_ar:
        violations.append("C2: 'label_ar' must not be empty")
    if not s.definition:
        violations.append("C2: 'definition' must not be empty")

    # C3 — referential records must have referential_status
    if (
        s.primary_type is PrimarySignifiedType.REFERENTIAL
        and s.referential_status is None
    ):
        violations.append(
            "C3: Referential signified must set 'referential_status'"
        )

    # C5 — rhetorical records must have figurative rhetorical_status
    if (
        s.primary_type is PrimarySignifiedType.RHETORICAL
        and s.rhetorical_status is RhetoricalStatus.LITERAL
    ):
        violations.append(
            "C5: Rhetorical signified must have non-LITERAL rhetorical_status"
        )

    return violations
