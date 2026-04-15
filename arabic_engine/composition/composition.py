"""المنسق الرئيسي — Main composition orchestrator (Articles 48–63, 73–78).

Pure functions implementing the full fractal composition cycle:
تعيين → حفظ → ربط → حكم → انتقال → رد

The main entry point is :func:`compose`, which takes a sequence of
:class:`CompositionUnit` objects and runs them through the full
composition pipeline.
"""

from __future__ import annotations

from arabic_engine.core.enums import (
    CompositionGateStatus,
)
from arabic_engine.core.types import (
    CompositionGateResult,
    CompositionProposition,
    CompositionRelation,
    CompositionRole,
    CompositionStructure,
    CompositionUnit,
    PredicationRecord,
)

from .gates import run_all_gates
from .predication import build_predication as _build_predication
from .proposition import (
    build_proposition as _build_proposition,
)
from .proposition import (
    close_proposition as _close_proposition,
)
from .relations import build_relation as _build_relation
from .relations import classify_relation
from .roles import assign_role as _assign_role
from .roles import realize_role as _realize_role


def compose(
    units: tuple[CompositionUnit, ...],
    *,
    threshold: float = 0.6,
) -> CompositionStructure:
    """Main entry point — compose units into a full structure.

    Runs the fractal law cycle:
    1. **تعيين** (Designation) — assign roles to admitted units
    2. **حفظ** (Preservation) — build relations
    3. **ربط** (Linking) — construct predication and proposition
    4. **حكم** (Judgement) — close proposition and run gates
    5. **انتقال** (Transition) — compute readiness
    6. **رد** (Return) — validate and package

    Parameters
    ----------
    units:
        Tuple of composition units (should be pre-admitted).
    threshold:
        Readiness threshold for validity (Article 75).
    """
    admitted = tuple(u for u in units if u.admitted)

    if not admitted:
        return CompositionStructure(
            units=units,
            readiness=0.0,
            valid=False,
        )

    # 1. تعيين — Assign roles
    roles: list[CompositionRole] = []
    for i, u in enumerate(admitted):
        ctx = {"position": "subject" if i == 0 else "predicate" if i == 1 else ""}
        role = _assign_role(u, ctx)
        role = _realize_role(role)
        roles.append(role)

    roles_tuple = tuple(roles)

    # 2. حفظ — Build relations
    relations: list[CompositionRelation] = []
    for i in range(len(admitted) - 1):
        rel_type = classify_relation(admitted[i], admitted[i + 1])
        rel = _build_relation(admitted[i], admitted[i + 1], rel_type)
        relations.append(rel)

    relations_tuple = tuple(relations)

    # 3. ربط — Construct predication and proposition
    predication: PredicationRecord | None = None
    proposition: CompositionProposition | None = None

    if len(admitted) >= 2:
        predication = _build_predication(admitted[0], admitted[1])
        proposition = _build_proposition(
            predication=predication,
            roles=roles_tuple,
            relations=relations_tuple,
        )

    # 4. حكم — Close proposition and run gates
    if proposition is not None:
        proposition = _close_proposition(proposition)

    # Collect conflicts from units
    conflicts = tuple(
        u.conflict for u in admitted if u.conflict is not None
    )

    gate_results = run_all_gates(
        units=admitted,
        roles=roles_tuple,
        relations=relations_tuple,
        conflicts=conflicts,
        proposition=proposition,
        links=(),
    )

    propositions = (proposition,) if proposition is not None else ()

    # 5. انتقال — Compute readiness
    readiness = compute_readiness_from_gates(gate_results, admitted, propositions)

    # 6. رد — Validate and package
    valid = validate_composition_value(readiness, threshold)

    return CompositionStructure(
        units=units,
        gates=gate_results,
        relations=relations_tuple,
        roles=roles_tuple,
        propositions=propositions,
        inter_links=(),
        readiness=readiness,
        valid=valid,
    )


def compute_readiness(structure: CompositionStructure) -> float:
    """Compute the readiness score for a composition structure (Article 75).

    Formula: ``(Units + Disambiguation + Relations + Roles + Closure + Recover) / 6``
    """
    return compute_readiness_from_gates(
        structure.gates,
        structure.units,
        structure.propositions,
    )


def compute_readiness_from_gates(
    gates: tuple[CompositionGateResult, ...],
    units: tuple[CompositionUnit, ...],
    propositions: tuple[CompositionProposition, ...],
) -> float:
    """Compute readiness from gate results, units, and propositions."""
    if not units:
        return 0.0

    # Factor 1: Unit admission ratio
    admitted_count = sum(1 for u in units if u.admitted)
    unit_score = admitted_count / len(units) if units else 0.0

    # Factor 2: Disambiguation score
    disambig_score = 1.0
    if gates:
        disambig_gates = [
            g for g in gates if g.gate.name == "DISAMBIGUATION"
        ]
        if disambig_gates:
            passed = disambig_gates[0].status == CompositionGateStatus.PASSED
            disambig_score = 1.0 if passed else 0.0

    # Factor 3: Relation score
    relation_gates = [
        g for g in gates if g.gate.name == "RELATION_VALIDITY"
    ]
    rel_ok = not relation_gates or (
        relation_gates[0].status == CompositionGateStatus.PASSED
    )
    relation_score = 1.0 if rel_ok else 0.0

    # Factor 4: Role score
    role_gates = [
        g for g in gates if g.gate.name == "ROLE_ASSIGNMENT"
    ]
    role_ok = not role_gates or (
        role_gates[0].status == CompositionGateStatus.PASSED
    )
    role_score = 1.0 if role_ok else 0.0

    # Factor 5: Closure score
    closure_ok = propositions and all(p.closed for p in propositions)
    closure_score = 1.0 if closure_ok else 0.0

    # Factor 6: Recovery score (gate pass ratio)
    if gates:
        passed_n = sum(
            1 for g in gates
            if g.status == CompositionGateStatus.PASSED
        )
        recover_score = passed_n / len(gates)
    else:
        recover_score = 0.0

    total = (
        unit_score + disambig_score + relation_score
        + role_score + closure_score + recover_score
    )
    return round(total / 6, 4)


def validate_composition(
    structure: CompositionStructure,
    threshold: float = 0.6,
) -> bool:
    """Validate whether a composition structure meets the acceptance threshold (Article 74)."""
    return validate_composition_value(structure.readiness, threshold)


def validate_composition_value(readiness: float, threshold: float) -> bool:
    """Check readiness against threshold."""
    return readiness >= threshold


def decompose(
    structure: CompositionStructure,
) -> tuple[CompositionUnit, ...]:
    """الرد — Return the composition's units (Article 63).

    Decomposes the structure back to its constituent units.
    """
    return structure.units
