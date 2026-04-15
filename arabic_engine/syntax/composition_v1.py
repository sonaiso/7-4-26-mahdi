"""Composition / Syntax Constitution v1 — دستور التركيب v1.0.

Implements the compositional society (المجتمع التركيبي) where fully-formed
lexemes and concepts enter predication, restriction, dependency, relations,
roles, propositions, and inter-propositional links — **after** semantic
disambiguation of ambiguity, conflict, transfer, and truth-category.

Public API
----------
resolve_ambiguity(unit_id, ambiguity_type, clue) → AmbiguityRecord
resolve_conflict(unit_id, conflict_type, method) → ConflictRecord
classify_transfer(unit_id, transfer_type, original, transferred) → TransferRecord
assign_truth_category(unit_id, category, confidence) → TruthRecord
disambiguate(units) → DisambiguationResult
build_predication(musnad_ilayh, musnad, pred_type) → PredicationRecord
build_restriction(base, restrictor, restriction_type) → RestrictionRecord
build_dependency(followed, follower, dep_type, aspect) → DependencyRecord
assign_role(unit_id, role) → CompositionRoleRecord
build_proposition(predication, restrictions, dependencies, roles, prop_type) → PropositionRecord
check_gate(gate, context) → GateResult
compute_readiness(units, disambiguation, relations, roles, closure, recover) → float
build_composition(units, propositions, links) → CompositionRecord
batch_compose(unit_groups) → List[CompositionRecord]
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from arabic_engine.core.enums import (
    AmbiguityResolution,
    AmbiguityType,
    CompositionGate,
    CompositionRelation,
    CompositionRole,
    CompositionVerdict,
    ConflictResolutionMethod,
    ConflictType,
    DependencyType,
    InterPropositionLink,
    PredicationType,
    PropositionType,
    RestrictionType,
    RoleStatus,
    TransferType,
    TruthCategory,
)
from arabic_engine.core.types import (
    AmbiguityRecord,
    CompositionRecord,
    CompositionRoleRecord,
    ConflictRecord,
    DependencyRecord,
    DisambiguationResult,
    GateResult,
    PredicationRecord,
    PropositionRecord,
    RestrictionRecord,
    TransferRecord,
    TruthRecord,
)

# ── Internal counters for auto-generated IDs ─────────────────────────

_amb_counter = 0
_cnf_counter = 0
_trf_counter = 0
_trt_counter = 0
_dis_counter = 0
_prd_counter = 0
_rst_counter = 0
_dep_counter = 0
_rol_counter = 0
_prp_counter = 0
_gat_counter = 0
_cmp_counter = 0

# Readiness threshold (θ_RS) — Art. 75
_READINESS_THRESHOLD = 0.5


def _next_id(prefix: str) -> str:
    """Return the next sequential ID for *prefix*."""
    global _amb_counter, _cnf_counter, _trf_counter, _trt_counter
    global _dis_counter, _prd_counter, _rst_counter, _dep_counter
    global _rol_counter, _prp_counter, _gat_counter, _cmp_counter

    if prefix == "AMB":
        _amb_counter += 1
        return f"AMB_{_amb_counter:03d}"
    if prefix == "CNF":
        _cnf_counter += 1
        return f"CNF_{_cnf_counter:03d}"
    if prefix == "TRF":
        _trf_counter += 1
        return f"TRF_{_trf_counter:03d}"
    if prefix == "TRT":
        _trt_counter += 1
        return f"TRT_{_trt_counter:03d}"
    if prefix == "DIS":
        _dis_counter += 1
        return f"DIS_{_dis_counter:03d}"
    if prefix == "PRD":
        _prd_counter += 1
        return f"PRD_{_prd_counter:03d}"
    if prefix == "RST":
        _rst_counter += 1
        return f"RST_{_rst_counter:03d}"
    if prefix == "DEP":
        _dep_counter += 1
        return f"DEP_{_dep_counter:03d}"
    if prefix == "ROL":
        _rol_counter += 1
        return f"ROL_{_rol_counter:03d}"
    if prefix == "PRP":
        _prp_counter += 1
        return f"PRP_{_prp_counter:03d}"
    if prefix == "GAT":
        _gat_counter += 1
        return f"GAT_{_gat_counter:03d}"
    # CMP
    _cmp_counter += 1
    return f"CMP_{_cmp_counter:03d}"


# ═════════════════════════════════════════════════════════════════════
# Disambiguation layer — فضّ الاضطراب الدلالي  (Art. 4-22)
# ═════════════════════════════════════════════════════════════════════


def resolve_ambiguity(
    unit_id: str,
    ambiguity_type: AmbiguityType,
    clue: Optional[AmbiguityResolution] = None,
) -> AmbiguityRecord:
    """Resolve (or leave open) a semantic ambiguity on *unit_id*.

    If *clue* is ``None`` or ``OPEN_PENDING`` the ambiguity is recorded as
    unresolved and the unit **must not** enter the compositional society.

    Args:
        unit_id: Identifier of the lexical / conceptual unit.
        ambiguity_type: The kind of ambiguity (Art. 8).
        clue: The resolution method (Art. 9), or ``None`` to leave open.

    Returns:
        A frozen :class:`AmbiguityRecord`.
    """
    resolved = clue is not None and clue != AmbiguityResolution.OPEN_PENDING
    return AmbiguityRecord(
        ambiguity_id=_next_id("AMB"),
        unit_id=unit_id,
        ambiguity_type=ambiguity_type,
        resolution=clue,
        resolved=resolved,
        details=f"type={ambiguity_type.name}, clue={clue.name if clue else 'NONE'}",
    )


def resolve_conflict(
    unit_id: str,
    conflict_type: ConflictType,
    method: Optional[ConflictResolutionMethod] = None,
) -> ConflictRecord:
    """Resolve (or block) a pre-composition conflict on *unit_id*.

    If *method* is ``None`` or ``BLOCK_TRANSITION`` the conflict remains
    blocking and the unit **must not** enter composition.

    Args:
        unit_id: Identifier of the unit with the conflict.
        conflict_type: The kind of conflict (Art. 12).
        method: Resolution method (Art. 13), or ``None``.

    Returns:
        A frozen :class:`ConflictRecord`.
    """
    resolved = method is not None and method != ConflictResolutionMethod.BLOCK_TRANSITION
    return ConflictRecord(
        conflict_id=_next_id("CNF"),
        unit_id=unit_id,
        conflict_type=conflict_type,
        resolution_method=method,
        resolved=resolved,
        details=f"type={conflict_type.name}, method={method.name if method else 'NONE'}",
    )


def classify_transfer(
    unit_id: str,
    transfer_type: TransferType,
    original: str = "",
    transferred: str = "",
    *,
    stable: bool = True,
) -> TransferRecord:
    """Classify a semantic transfer for *unit_id* (Art. 14-17).

    A transfer is accepted only when *stable* is ``True``, indicating
    that the transfer has recognised stability and can be traced back
    to its original direction.

    Args:
        unit_id: Identifier of the unit.
        transfer_type: The kind of transfer (Art. 15).
        original: Description of the original semantic direction.
        transferred: Description of the transferred semantic direction.
        stable: Whether the transfer is considered stable.

    Returns:
        A frozen :class:`TransferRecord`.
    """
    return TransferRecord(
        transfer_id=_next_id("TRF"),
        unit_id=unit_id,
        transfer_type=transfer_type,
        stable=stable,
        original_direction=original,
        transferred_direction=transferred,
    )


def assign_truth_category(
    unit_id: str,
    category: TruthCategory,
    confidence: float = 1.0,
) -> TruthRecord:
    """Assign a truth category (linguistic / conventional / transfer) to *unit_id*.

    Args:
        unit_id: Identifier of the unit.
        category: The truth category (Art. 21).
        confidence: Confidence level in ``[0, 1]``.

    Returns:
        A frozen :class:`TruthRecord`.
    """
    return TruthRecord(
        truth_id=_next_id("TRT"),
        unit_id=unit_id,
        category=category,
        confidence=max(0.0, min(1.0, confidence)),
    )


def disambiguate(
    units: Sequence[str],
    *,
    ambiguities: Sequence[AmbiguityRecord] = (),
    conflicts: Sequence[ConflictRecord] = (),
    transfers: Sequence[TransferRecord] = (),
    truth_assignments: Sequence[TruthRecord] = (),
) -> DisambiguationResult:
    """Aggregate disambiguation check for a set of *units* (Art. 4-22).

    The result carries ``all_resolved=True`` **only** when every ambiguity
    and conflict is resolved, every transfer is stable, and every unit has
    a truth assignment.

    Args:
        units: Identifiers of all units about to enter composition.
        ambiguities: Pre-computed ambiguity records.
        conflicts: Pre-computed conflict records.
        transfers: Pre-computed transfer records.
        truth_assignments: Pre-computed truth records.

    Returns:
        A frozen :class:`DisambiguationResult`.
    """
    amb_ok = all(a.resolved for a in ambiguities)
    cnf_ok = all(c.resolved for c in conflicts)
    trf_ok = all(t.stable for t in transfers)
    trt_ok = len(truth_assignments) >= len(units) if units else True

    return DisambiguationResult(
        ambiguities=tuple(ambiguities),
        conflicts=tuple(conflicts),
        transfers=tuple(transfers),
        truth_assignments=tuple(truth_assignments),
        all_resolved=amb_ok and cnf_ok and trf_ok and trt_ok,
    )


# ═════════════════════════════════════════════════════════════════════
# Structural composition — الإسناد والتقييد والتبعية  (Art. 26-35)
# ═════════════════════════════════════════════════════════════════════


def build_predication(
    musnad_ilayh: str,
    musnad: str,
    predication_type: PredicationType,
) -> PredicationRecord:
    """Build a predication record (Art. 26-29).

    The predication is valid when both *musnad_ilayh* and *musnad* are
    non-empty and distinct.

    Args:
        musnad_ilayh: The subject (المسند إليه).
        musnad: The predicate (المسند).
        predication_type: Type of predication (Art. 28).

    Returns:
        A frozen :class:`PredicationRecord`.
    """
    valid = bool(musnad_ilayh) and bool(musnad) and musnad_ilayh != musnad
    return PredicationRecord(
        predication_id=_next_id("PRD"),
        musnad_ilayh=musnad_ilayh,
        musnad=musnad,
        predication_type=predication_type,
        valid=valid,
    )


def build_restriction(
    base_unit: str,
    restrictor: str,
    restriction_type: RestrictionType,
) -> RestrictionRecord:
    """Build a restriction record (Art. 30-32).

    The restriction is valid when both identifiers are non-empty, they
    differ, and the restrictor does not replace the predication itself.

    Args:
        base_unit: The base unit being restricted.
        restrictor: The restricting unit.
        restriction_type: The kind of restriction (Art. 31).

    Returns:
        A frozen :class:`RestrictionRecord`.
    """
    valid = bool(base_unit) and bool(restrictor) and base_unit != restrictor
    return RestrictionRecord(
        restriction_id=_next_id("RST"),
        base_unit=base_unit,
        restrictor=restrictor,
        restriction_type=restriction_type,
        valid=valid,
    )


def build_dependency(
    followed: str,
    follower: str,
    dependency_type: DependencyType,
    aspect: str = "",
) -> DependencyRecord:
    """Build a dependency record (Art. 33-35).

    Args:
        followed: The unit being followed (المتبوع).
        follower: The follower unit (التابع).
        dependency_type: The kind of dependency (Art. 34).
        aspect: Description of the dependency aspect.

    Returns:
        A frozen :class:`DependencyRecord`.
    """
    return DependencyRecord(
        dependency_id=_next_id("DEP"),
        followed=followed,
        follower=follower,
        dependency_type=dependency_type,
        aspect=aspect,
    )


# ═════════════════════════════════════════════════════════════════════
# Roles — الأدوار  (Art. 39-41)
# ═════════════════════════════════════════════════════════════════════


def assign_role(
    unit_id: str,
    role: CompositionRole,
    *,
    realized: bool = False,
) -> CompositionRoleRecord:
    """Assign a compositional role to *unit_id* (Art. 39-41).

    By default the role starts as ``CANDIDATE``; pass ``realized=True``
    to promote it to ``REALIZED``.

    Args:
        unit_id: Identifier of the unit.
        role: The compositional role (Art. 40).
        realized: Whether the role is already realised.

    Returns:
        A frozen :class:`CompositionRoleRecord`.
    """
    return CompositionRoleRecord(
        role_id=_next_id("ROL"),
        unit_id=unit_id,
        role=role,
        status=RoleStatus.REALIZED if realized else RoleStatus.CANDIDATE,
    )


# ═════════════════════════════════════════════════════════════════════
# Propositions — القضايا  (Art. 42-44)
# ═════════════════════════════════════════════════════════════════════


def build_proposition(
    predication: PredicationRecord,
    restrictions: Sequence[RestrictionRecord] = (),
    dependencies: Sequence[DependencyRecord] = (),
    roles: Sequence[CompositionRoleRecord] = (),
    proposition_type: PropositionType = PropositionType.NOMINAL,
) -> PropositionRecord:
    """Build a proposition from its components (Art. 42-44).

    A proposition is *closed* (Art. 43) when:
    1. Predication is valid.
    2. All restrictions are valid.
    3. At least two roles are present (musnad_ilayh + musnad).
    4. All roles are REALIZED.

    Args:
        predication: The predication record.
        restrictions: Optional restriction records.
        dependencies: Optional dependency records.
        roles: Compositional role records.
        proposition_type: The kind of proposition (Art. 44).

    Returns:
        A frozen :class:`PropositionRecord`.
    """
    restrictions_valid = all(r.valid for r in restrictions)
    roles_realized = all(r.status == RoleStatus.REALIZED for r in roles)
    has_min_roles = len(roles) >= 2
    closed = (
        predication.valid
        and restrictions_valid
        and has_min_roles
        and roles_realized
    )
    return PropositionRecord(
        proposition_id=_next_id("PRP"),
        predication=predication,
        restrictions=tuple(restrictions),
        dependencies=tuple(dependencies),
        roles=tuple(roles),
        proposition_type=proposition_type,
        closed=closed,
    )


# ═════════════════════════════════════════════════════════════════════
# Gates — البوابات  (Art. 64-72)
# ═════════════════════════════════════════════════════════════════════


def _gate_disambiguation(ctx: Dict[str, object]) -> GateResult:
    """Gate_Disambiguation (Art. 65): ambiguity + truth resolved."""
    dis = ctx.get("disambiguation")
    if isinstance(dis, DisambiguationResult) and dis.all_resolved:
        return GateResult(
            gate=CompositionGate.DISAMBIGUATION,
            passed=True,
            reason="all ambiguities and conflicts resolved",
        )
    return GateResult(
        gate=CompositionGate.DISAMBIGUATION,
        passed=False,
        reason="unresolved ambiguity or conflict blocks composition",
    )


def _gate_reference_stability(ctx: Dict[str, object]) -> GateResult:
    """Gate_Reference_Stability (Art. 66): referential units stable."""
    stable = ctx.get("reference_stable", False)
    return GateResult(
        gate=CompositionGate.REFERENCE_STABILITY,
        passed=bool(stable),
        reason="references stable" if stable else "unstable references",
    )


def _gate_predicate_readiness(ctx: Dict[str, object]) -> GateResult:
    """Gate_Predicate_Readiness (Art. 67): predication units ready."""
    ready = ctx.get("predicate_ready", False)
    return GateResult(
        gate=CompositionGate.PREDICATE_READINESS,
        passed=bool(ready),
        reason="predicates ready" if ready else "predicates not ready",
    )


def _gate_role_assignment(ctx: Dict[str, object]) -> GateResult:
    """Gate_Role_Assignment (Art. 68): roles transitioned to REALIZED."""
    roles = ctx.get("roles", ())
    if not roles:
        return GateResult(
            gate=CompositionGate.ROLE_ASSIGNMENT,
            passed=False,
            reason="no roles assigned",
        )
    if isinstance(roles, (list, tuple)):
        all_realized = all(
            getattr(r, "status", None) == RoleStatus.REALIZED for r in roles
        )
    else:
        all_realized = False
    return GateResult(
        gate=CompositionGate.ROLE_ASSIGNMENT,
        passed=all_realized,
        reason="all roles realized" if all_realized else "some roles still candidate",
    )


def _gate_relation_validity(ctx: Dict[str, object]) -> GateResult:
    """Gate_Relation_Validity (Art. 69): relations are well-formed."""
    valid = ctx.get("relations_valid", False)
    return GateResult(
        gate=CompositionGate.RELATION_VALIDITY,
        passed=bool(valid),
        reason="relations valid" if valid else "invalid relations",
    )


def _gate_conflict_resolution(ctx: Dict[str, object]) -> GateResult:
    """Gate_Conflict_Resolution (Art. 70): no blocking conflict."""
    dis = ctx.get("disambiguation")
    if isinstance(dis, DisambiguationResult):
        conflicts_ok = all(c.resolved for c in dis.conflicts)
    else:
        conflicts_ok = ctx.get("conflicts_resolved", False)
    return GateResult(
        gate=CompositionGate.CONFLICT_RESOLUTION,
        passed=bool(conflicts_ok),
        reason="conflicts resolved" if conflicts_ok else "blocking conflict",
    )


def _gate_proposition_closure(ctx: Dict[str, object]) -> GateResult:
    """Gate_Proposition_Closure (Art. 71): propositions closed."""
    props = ctx.get("propositions", ())
    if not props:
        return GateResult(
            gate=CompositionGate.PROPOSITION_CLOSURE,
            passed=False,
            reason="no propositions",
        )
    if isinstance(props, (list, tuple)):
        all_closed = all(getattr(p, "closed", False) for p in props)
    else:
        all_closed = False
    return GateResult(
        gate=CompositionGate.PROPOSITION_CLOSURE,
        passed=all_closed,
        reason="all propositions closed" if all_closed else "unclosed propositions",
    )


def _gate_interproposition_link(ctx: Dict[str, object]) -> GateResult:
    """Gate_InterProposition_Link (Art. 72): inter-proposition links valid."""
    links = ctx.get("links", ())
    props = ctx.get("propositions", ())
    # Only required when more than one proposition exists
    if isinstance(props, (list, tuple)) and len(props) <= 1:
        return GateResult(
            gate=CompositionGate.INTERPROPOSITION_LINK,
            passed=True,
            reason="single proposition, no link required",
        )
    has_links = bool(links)
    return GateResult(
        gate=CompositionGate.INTERPROPOSITION_LINK,
        passed=has_links,
        reason="links present" if has_links else "missing inter-proposition links",
    )


_GATE_DISPATCH: Dict[CompositionGate, object] = {
    CompositionGate.DISAMBIGUATION: _gate_disambiguation,
    CompositionGate.REFERENCE_STABILITY: _gate_reference_stability,
    CompositionGate.PREDICATE_READINESS: _gate_predicate_readiness,
    CompositionGate.ROLE_ASSIGNMENT: _gate_role_assignment,
    CompositionGate.RELATION_VALIDITY: _gate_relation_validity,
    CompositionGate.CONFLICT_RESOLUTION: _gate_conflict_resolution,
    CompositionGate.PROPOSITION_CLOSURE: _gate_proposition_closure,
    CompositionGate.INTERPROPOSITION_LINK: _gate_interproposition_link,
}


def check_gate(gate: CompositionGate, context: Dict[str, object]) -> GateResult:
    """Evaluate a single composition gate (Art. 64-72).

    Args:
        gate: Which gate to evaluate.
        context: A dictionary carrying the data needed by the gate.

    Returns:
        A frozen :class:`GateResult`.
    """
    fn = _GATE_DISPATCH.get(gate)
    if fn is None:
        return GateResult(gate=gate, passed=False, reason="unknown gate")
    return fn(context)  # type: ignore[operator]


# ═════════════════════════════════════════════════════════════════════
# Readiness — الجاهزية  (Art. 75)
# ═════════════════════════════════════════════════════════════════════


def compute_readiness(
    units: float,
    disambiguation: float,
    relations: float,
    roles: float,
    closure: float,
    recover: float,
) -> float:
    """Compute composition readiness score (Art. 75).

    .. math::

        Ready_S = \\frac{Units + Disambiguation + Relations
                         + Roles + Closure + Recover}{6}

    Each component should be in ``[0, 1]``.  The composition is
    considered *ready* when ``Ready_S >= θ_RS`` (default 0.5).

    Args:
        units: Normalised score for unit completeness.
        disambiguation: Score for disambiguation completeness.
        relations: Score for relation validity.
        roles: Score for role assignment.
        closure: Score for proposition closure.
        recover: Score for recoverability / traceability.

    Returns:
        The readiness score in ``[0, 1]``.
    """
    total = units + disambiguation + relations + roles + closure + recover
    return total / 6.0


# ═════════════════════════════════════════════════════════════════════
# Composition — التركيب  (Art. 73-78)
# ═════════════════════════════════════════════════════════════════════


def _collect_relations(
    propositions: Sequence[PropositionRecord],
) -> Tuple[CompositionRelation, ...]:
    """Infer the set of composition relations present."""
    rels: list[CompositionRelation] = []
    for p in propositions:
        if p.predication.valid:
            rels.append(CompositionRelation.PREDICATION)
        for r in p.restrictions:
            if r.valid:
                rels.append(CompositionRelation.RESTRICTION)
        if p.dependencies:
            rels.append(CompositionRelation.DEPENDENCY)
    # De-duplicate while preserving order
    seen: set[CompositionRelation] = set()
    unique: list[CompositionRelation] = []
    for r in rels:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    return tuple(unique)


def _collect_roles(
    propositions: Sequence[PropositionRecord],
) -> Tuple[CompositionRoleRecord, ...]:
    """Aggregate all roles from propositions."""
    roles: list[CompositionRoleRecord] = []
    for p in propositions:
        roles.extend(p.roles)
    return tuple(roles)


def build_composition(
    units: Sequence[str],
    propositions: Sequence[PropositionRecord],
    links: Sequence[InterPropositionLink] = (),
    *,
    disambiguation: Optional[DisambiguationResult] = None,
    reference_stable: bool = True,
    predicate_ready: bool = True,
    relations_valid: bool = True,
) -> CompositionRecord:
    """Build a full composition record (Art. 73-78).

    Runs all eight gates in order (Art. 64).  The **verdict** is:

    * ``ACCEPTED`` — all gates pass **and** readiness ≥ θ_RS.
    * ``REJECTED`` — at least one gate fails.
    * ``PENDING``  — all gates pass but readiness < θ_RS.

    Args:
        units: Identifiers of entering units.
        propositions: Built proposition records.
        links: Inter-proposition link types.
        disambiguation: Pre-computed disambiguation result.
        reference_stable: Whether references are stable.
        predicate_ready: Whether predicates are ready.
        relations_valid: Whether relations are valid.

    Returns:
        A frozen :class:`CompositionRecord`.
    """
    roles = _collect_roles(propositions)
    relations = _collect_relations(propositions)

    # Build gate context
    ctx: Dict[str, object] = {
        "disambiguation": disambiguation or DisambiguationResult(all_resolved=True),
        "reference_stable": reference_stable,
        "predicate_ready": predicate_ready,
        "roles": roles,
        "relations_valid": relations_valid,
        "propositions": propositions,
        "links": links,
    }

    gate_results: list[GateResult] = []
    for g in CompositionGate:
        gate_results.append(check_gate(g, ctx))

    all_passed = all(gr.passed for gr in gate_results)

    # Readiness computation
    dis_obj = ctx["disambiguation"]
    dis_score = 1.0 if (isinstance(dis_obj, DisambiguationResult) and dis_obj.all_resolved) else 0.0
    unit_score = 1.0 if units else 0.0
    rel_score = 1.0 if relations else 0.0
    role_score = 1.0 if (roles and all(r.status == RoleStatus.REALIZED for r in roles)) else 0.0
    close_score = 1.0 if (propositions and all(p.closed for p in propositions)) else 0.0
    recover_score = 1.0  # traceability always available via record structure
    readiness = compute_readiness(
        unit_score, dis_score, rel_score, role_score, close_score, recover_score,
    )

    if all_passed and readiness >= _READINESS_THRESHOLD:
        verdict = CompositionVerdict.ACCEPTED
    elif not all_passed:
        verdict = CompositionVerdict.REJECTED
    else:
        verdict = CompositionVerdict.PENDING

    return CompositionRecord(
        composition_id=_next_id("CMP"),
        units=tuple(units),
        gates=tuple(gate_results),
        relations=relations,
        roles=roles,
        propositions=tuple(propositions),
        links=tuple(links),
        verdict=verdict,
        readiness=readiness,
    )


def batch_compose(
    unit_groups: Sequence[
        Tuple[
            Sequence[str],
            Sequence[PropositionRecord],
            Sequence[InterPropositionLink],
        ]
    ],
) -> List[CompositionRecord]:
    """Compose multiple groups of units in batch.

    Each element of *unit_groups* is a 3-tuple of
    ``(units, propositions, links)``.

    Args:
        unit_groups: Sequence of composition inputs.

    Returns:
        A list of :class:`CompositionRecord`, one per group.
    """
    return [
        build_composition(units, props, links)
        for units, props, links in unit_groups
    ]
