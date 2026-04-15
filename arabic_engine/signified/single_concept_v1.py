"""Single Concept Constitution v1 — دستور المفهوم المفرد v1.0.

Implements the complete, programmable representation for a single concept
(مفهوم مفرد) — the semantic unit that maps to a single lexeme (لفظ مفرد)
— before it enters into compositional/syntactic structures.

Public API
----------
classify_concept_type(concept) → SingleConceptType
classify_candidate_role(concept_type, closure) → CandidateRole
check_isomorphism(closure, concept, concept_type) → SingleConceptIsomorphism
analyze_dalala(closure, concept, dalala_type) → SingleConceptDalala
compute_readiness(gates) → float
build_single_concept(closure, concept, dalala_type, ...) → SingleConceptRecord
build_single_concept_batch(pairs, dalala_type, ...) → List[SingleConceptRecord]
acceptance_summary(record) → Dict[str, bool]
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from arabic_engine.core.enums import (
    POS,
    CandidateRole,
    ConceptClosureStatus,
    ConceptEntityAttribute,
    ConceptGateID,
    ConceptIndependence,
    ConceptUniversalParticular,
    DalalaType,
    SemanticType,
    SingleConceptType,
    TransitionGateStatus,
)
from arabic_engine.core.types import (
    Concept,
    LexicalClosure,
    SingleConceptDalala,
    SingleConceptGateResult,
    SingleConceptIsomorphism,
    SingleConceptRecord,
)

# ── Internal counter for auto-generated IDs ──────────────────────────

_sc_counter = 0


def _next_sc_id() -> str:
    """Return the next sequential ``SC_nnn`` identifier."""
    global _sc_counter
    _sc_counter += 1
    return f"SC_{_sc_counter:03d}"


# ── SemanticType → SingleConceptType mapping (المادة 28–32) ───────────

_STYPE_TO_CONCEPT_TYPE: Dict[SemanticType, SingleConceptType] = {
    SemanticType.ENTITY: SingleConceptType.EXISTENTIAL,
    SemanticType.EVENT: SingleConceptType.EVENTIVE,
    SemanticType.ATTRIBUTE: SingleConceptType.DESCRIPTIVE,
    SemanticType.RELATION: SingleConceptType.RELATIONAL,
    SemanticType.NORM: SingleConceptType.RELATIONAL,
}

# ── SingleConceptType → default CandidateRole (المادة 47–53) ─────────

_CONCEPT_TYPE_TO_ROLE: Dict[SingleConceptType, CandidateRole] = {
    SingleConceptType.EXISTENTIAL: CandidateRole.MUSNAD_ILAYH,
    SingleConceptType.DESCRIPTIVE: CandidateRole.MUSNAD,
    SingleConceptType.EVENTIVE: CandidateRole.MUSNAD,
    SingleConceptType.RELATIONAL: CandidateRole.RABIT,
}

# ── POS → ConceptEntityAttribute mapping ─────────────────────────────

_POS_TO_EA: Dict[POS, ConceptEntityAttribute] = {
    POS.ISM: ConceptEntityAttribute.ENTITY,
    POS.FI3L: ConceptEntityAttribute.ATTRIBUTE,
    POS.SIFA: ConceptEntityAttribute.ATTRIBUTE,
    POS.HARF: ConceptEntityAttribute.ATTRIBUTE,
    POS.ZARF: ConceptEntityAttribute.ATTRIBUTE,
    POS.DAMIR: ConceptEntityAttribute.ENTITY,
    POS.UNKNOWN: ConceptEntityAttribute.ENTITY,
}

# ── POS → ConceptUniversalParticular mapping ─────────────────────────

_POS_TO_UP: Dict[POS, ConceptUniversalParticular] = {
    POS.ISM: ConceptUniversalParticular.UNIVERSAL,
    POS.FI3L: ConceptUniversalParticular.UNIVERSAL,
    POS.SIFA: ConceptUniversalParticular.UNIVERSAL,
    POS.HARF: ConceptUniversalParticular.UNIVERSAL,
    POS.ZARF: ConceptUniversalParticular.UNIVERSAL,
    POS.DAMIR: ConceptUniversalParticular.PARTICULAR,
    POS.UNKNOWN: ConceptUniversalParticular.UNIVERSAL,
}

# ── SemanticType → SingleConceptType direction-mapping ───────────────

_STYPE_TO_DIRECTION_MATCH: Dict[SemanticType, SingleConceptType] = {
    SemanticType.ENTITY: SingleConceptType.EXISTENTIAL,
    SemanticType.EVENT: SingleConceptType.EVENTIVE,
    SemanticType.ATTRIBUTE: SingleConceptType.DESCRIPTIVE,
    SemanticType.RELATION: SingleConceptType.RELATIONAL,
    SemanticType.NORM: SingleConceptType.RELATIONAL,
}

# ── POS → expected SingleConceptType (for type isomorphism check) ────

_POS_TO_EXPECTED_CONCEPT_TYPE: Dict[POS, SingleConceptType] = {
    POS.ISM: SingleConceptType.EXISTENTIAL,
    POS.FI3L: SingleConceptType.EVENTIVE,
    POS.SIFA: SingleConceptType.DESCRIPTIVE,
    POS.HARF: SingleConceptType.RELATIONAL,
    POS.ZARF: SingleConceptType.DESCRIPTIVE,
    POS.DAMIR: SingleConceptType.EXISTENTIAL,
    POS.UNKNOWN: SingleConceptType.EXISTENTIAL,
}

# ── POS-based role overrides ─────────────────────────────────────────

_POS_ROLE_OVERRIDES: Dict[POS, CandidateRole] = {
    POS.HARF: CandidateRole.RABIT,
    POS.ZARF: CandidateRole.QAYD,
    POS.DAMIR: CandidateRole.MUSNAD_ILAYH,
}

# ── DalalaType → default reference/predicative loads ─────────────────

_DALALA_REF_LOAD: Dict[DalalaType, float] = {
    DalalaType.MUTABAQA: 1.0,
    DalalaType.TADAMMUN: 0.6,
    DalalaType.ILTIZAM: 0.3,
    DalalaType.ISNAD: 0.2,
    DalalaType.TAQYID: 0.4,
    DalalaType.IDAFA: 0.5,
    DalalaType.IHALA: 0.9,
}

_DALALA_PRED_LOAD: Dict[DalalaType, float] = {
    DalalaType.MUTABAQA: 0.2,
    DalalaType.TADAMMUN: 0.5,
    DalalaType.ILTIZAM: 0.7,
    DalalaType.ISNAD: 0.9,
    DalalaType.TAQYID: 0.8,
    DalalaType.IDAFA: 0.6,
    DalalaType.IHALA: 0.1,
}


# ═══════════════════════════════════════════════════════════════════════
# Classifiers
# ═══════════════════════════════════════════════════════════════════════


def classify_concept_type(concept: Concept) -> SingleConceptType:
    """Map a :class:`Concept`'s semantic type to a :class:`SingleConceptType`.

    Uses the four-genus classification of المادة 28–32:
    ENTITY → EXISTENTIAL, ATTRIBUTE → DESCRIPTIVE,
    EVENT → EVENTIVE, RELATION/NORM → RELATIONAL.
    """
    return _STYPE_TO_CONCEPT_TYPE.get(
        concept.semantic_type, SingleConceptType.EXISTENTIAL
    )


def classify_candidate_role(
    concept_type: SingleConceptType,
    closure: LexicalClosure,
) -> CandidateRole:
    """Determine the candidate syntactic role (المادة 47–53).

    Uses POS-specific overrides first, then falls back to the
    concept-type default mapping.
    """
    override = _POS_ROLE_OVERRIDES.get(closure.pos)
    if override is not None:
        return override
    return _CONCEPT_TYPE_TO_ROLE.get(concept_type, CandidateRole.MUSNAD_ILAYH)


# ═══════════════════════════════════════════════════════════════════════
# Isomorphism check (المادة 11–18)
# ═══════════════════════════════════════════════════════════════════════


def check_isomorphism(
    closure: LexicalClosure,
    concept: Concept,
    concept_type: SingleConceptType,
) -> SingleConceptIsomorphism:
    """Check the five isomorphism axes between lexeme and concept.

    1. **Direction match** — the concept's semantic type maps to the
       same ``SingleConceptType`` as ``concept_type``.
    2. **Type match** — the POS-expected concept type matches
       ``concept_type``.
    3. **Boundary match** — both the lexeme surface and the concept
       label are non-empty (boundaries are defined).
    4. **Function match** — the concept's semantic type is compatible
       with a recognisable syntactic function for the POS.
    5. **Transition match** — the concept label is non-empty and
       the closure has a known POS (not UNKNOWN), ensuring transition
       readiness.
    """
    # 1. Direction (الجهة)
    expected_dir = _STYPE_TO_DIRECTION_MATCH.get(concept.semantic_type)
    direction_match = expected_dir == concept_type

    # 2. Type (النوع)
    pos_expected = _POS_TO_EXPECTED_CONCEPT_TYPE.get(
        closure.pos, SingleConceptType.EXISTENTIAL
    )
    type_match = pos_expected == concept_type

    # 3. Boundary (الحدود)
    boundary_match = bool(closure.surface.strip()) and bool(concept.label.strip())

    # 4. Function (الوظيفة)
    function_match = concept.semantic_type in _STYPE_TO_CONCEPT_TYPE

    # 5. Transition (الانتقال)
    transition_match = bool(concept.label.strip()) and closure.pos is not POS.UNKNOWN

    return SingleConceptIsomorphism(
        direction_match=direction_match,
        type_match=type_match,
        boundary_match=boundary_match,
        function_match=function_match,
        transition_match=transition_match,
    )


# ═══════════════════════════════════════════════════════════════════════
# Dalāla analysis (المادة 54–57)
# ═══════════════════════════════════════════════════════════════════════


def analyze_dalala(
    closure: LexicalClosure,
    concept: Concept,
    dalala_type: DalalaType,
) -> SingleConceptDalala:
    """Build the three-level signification record.

    * **mutabaqa** — direct correspondence: surface ↔ label.
    * **tadammun** — internal inclusion: semantic type + concept properties.
    * **iltizam** — external implication: inferred commitments from POS/type.
    """
    mutabaqa = f"{closure.surface}↔{concept.label}"

    tadammun_parts = [concept.semantic_type.name]
    if concept.properties:
        tadammun_parts.extend(f"{k}={v}" for k, v in sorted(concept.properties.items()))
    tadammun = "; ".join(tadammun_parts)

    iltizam = f"dalala={dalala_type.name}; pos={closure.pos.name}"

    return SingleConceptDalala(
        mutabaqa=mutabaqa,
        tadammun=tadammun,
        iltizam=iltizam,
    )


# ═══════════════════════════════════════════════════════════════════════
# Gate checkers (المادة 59–67)
# ═══════════════════════════════════════════════════════════════════════


def _check_gate_type(
    concept: Concept,
    closure: LexicalClosure,
) -> SingleConceptGateResult:
    """Gate 1: النوع الأعلى — is the concept type determined? (المادة 60)."""
    if concept.semantic_type in _STYPE_TO_CONCEPT_TYPE:
        return SingleConceptGateResult(
            gate_id=ConceptGateID.GATE_TYPE,
            status=TransitionGateStatus.PASSED,
            detail=f"type={_STYPE_TO_CONCEPT_TYPE[concept.semantic_type].name}",
        )
    return SingleConceptGateResult(
        gate_id=ConceptGateID.GATE_TYPE,
        status=TransitionGateStatus.BLOCKED,
        detail=f"unrecognised semantic_type={concept.semantic_type.name}",
    )


def _check_gate_direction(
    concept: Concept,
    closure: LexicalClosure,
    concept_type: SingleConceptType,
) -> SingleConceptGateResult:
    """Gate 2: الجهة المركزية — direction/جهة match (المادة 61)."""
    expected = _STYPE_TO_DIRECTION_MATCH.get(concept.semantic_type)
    if expected == concept_type:
        return SingleConceptGateResult(
            gate_id=ConceptGateID.GATE_DIRECTION,
            status=TransitionGateStatus.PASSED,
            detail="direction aligned",
        )
    return SingleConceptGateResult(
        gate_id=ConceptGateID.GATE_DIRECTION,
        status=TransitionGateStatus.BLOCKED,
        detail=f"expected={expected}, got={concept_type.name}",
    )


def _check_gate_universal_particular(
    up: ConceptUniversalParticular,
) -> SingleConceptGateResult:
    """Gate 3: الكلي / الجزئي — UP classification determined (المادة 62)."""
    return SingleConceptGateResult(
        gate_id=ConceptGateID.GATE_UNIVERSAL_PARTICULAR,
        status=TransitionGateStatus.PASSED,
        detail=f"up={up.name}",
    )


def _check_gate_entity_attribute(
    ea: ConceptEntityAttribute,
) -> SingleConceptGateResult:
    """Gate 4: الذات / الصفة — EA classification determined (المادة 63)."""
    return SingleConceptGateResult(
        gate_id=ConceptGateID.GATE_ENTITY_ATTRIBUTE,
        status=TransitionGateStatus.PASSED,
        detail=f"ea={ea.name}",
    )


def _check_gate_reference_load(
    concept: Concept,
    closure: LexicalClosure,
    ref_load: float,
) -> SingleConceptGateResult:
    """Gate 5: الحمل الإحالي — referential load (المادة 64)."""
    if ref_load > 0.0 and bool(concept.label.strip()):
        return SingleConceptGateResult(
            gate_id=ConceptGateID.GATE_REFERENCE_LOAD,
            status=TransitionGateStatus.PASSED,
            detail=f"ref_load={ref_load:.2f}",
        )
    if ref_load == 0.0:
        return SingleConceptGateResult(
            gate_id=ConceptGateID.GATE_REFERENCE_LOAD,
            status=TransitionGateStatus.INSUFFICIENT_DATA,
            detail="ref_load=0.0",
        )
    return SingleConceptGateResult(
        gate_id=ConceptGateID.GATE_REFERENCE_LOAD,
        status=TransitionGateStatus.BLOCKED,
        detail=f"ref_load={ref_load:.2f}, label empty",
    )


def _check_gate_predicative_load(
    concept: Concept,
    pred_load: float,
) -> SingleConceptGateResult:
    """Gate 6: الحمل المسندي — predicative/attributive load (المادة 65)."""
    if pred_load > 0.0:
        return SingleConceptGateResult(
            gate_id=ConceptGateID.GATE_PREDICATIVE_LOAD,
            status=TransitionGateStatus.PASSED,
            detail=f"pred_load={pred_load:.2f}",
        )
    return SingleConceptGateResult(
        gate_id=ConceptGateID.GATE_PREDICATIVE_LOAD,
        status=TransitionGateStatus.INSUFFICIENT_DATA,
        detail="pred_load=0.0",
    )


def _check_gate_role_readiness(
    candidate_role: CandidateRole,
    concept_type: SingleConceptType,
) -> SingleConceptGateResult:
    """Gate 7: جاهزية الدور — role candidacy threshold (المادة 66)."""
    if candidate_role is not None:
        return SingleConceptGateResult(
            gate_id=ConceptGateID.GATE_ROLE_READINESS,
            status=TransitionGateStatus.PASSED,
            detail=f"role={candidate_role.name}",
        )
    return SingleConceptGateResult(
        gate_id=ConceptGateID.GATE_ROLE_READINESS,
        status=TransitionGateStatus.BLOCKED,
        detail="no candidate role assigned",
    )


def _check_gate_recoverability(
    concept: Concept,
    closure: LexicalClosure,
    concept_type: SingleConceptType,
) -> SingleConceptGateResult:
    """Gate 8: قابلية الرد — traceability (المادة 67)."""
    recoverable = (
        bool(closure.surface.strip())
        and bool(concept.label.strip())
        and concept.semantic_type in _STYPE_TO_CONCEPT_TYPE
        and closure.pos is not POS.UNKNOWN
    )
    if recoverable:
        return SingleConceptGateResult(
            gate_id=ConceptGateID.GATE_RECOVERABILITY,
            status=TransitionGateStatus.PASSED,
            detail="fully recoverable",
        )
    reasons = []
    if not closure.surface.strip():
        reasons.append("empty surface")
    if not concept.label.strip():
        reasons.append("empty label")
    if concept.semantic_type not in _STYPE_TO_CONCEPT_TYPE:
        reasons.append("unknown semantic_type")
    if closure.pos is POS.UNKNOWN:
        reasons.append("unknown POS")
    return SingleConceptGateResult(
        gate_id=ConceptGateID.GATE_RECOVERABILITY,
        status=TransitionGateStatus.BLOCKED,
        detail="; ".join(reasons),
    )


# ═══════════════════════════════════════════════════════════════════════
# Readiness score (المادة 75–77, 80)
# ═══════════════════════════════════════════════════════════════════════


def compute_readiness(gates: Tuple[SingleConceptGateResult, ...]) -> float:
    """Compute the readiness score Ready_C ∈ [0, 1].

    ``Ready_C = count(PASSED gates) / total_gates``

    The constitution (المادة 80) uses 7 components in its formula; this
    implementation counts all gates provided (typically 8).
    """
    if not gates:
        return 0.0
    passed = sum(1 for g in gates if g.status is TransitionGateStatus.PASSED)
    return passed / len(gates)


# ═══════════════════════════════════════════════════════════════════════
# Acceptance summary (المادة 81–82)
# ═══════════════════════════════════════════════════════════════════════


def acceptance_summary(record: SingleConceptRecord) -> Dict[str, bool]:
    """Return a dict with eight acceptance criteria and their pass/fail status.

    Criteria (المادة 81):
    1. lexeme_match — مطابقة معتبرة مع اللفظ المفرد
    2. type_established — ثبوت النوع الأعلى
    3. direction_established — ثبوت الجهة المركزية
    4. up_ea_established — ثبوت الكلي/الجزئي والذات/الصفة
    5. load_established — ثبوت الحمل أو الإحالة
    6. role_established — ثبوت الدور المرشح
    7. recoverable — قابلية الرد إلى الأصول
    8. readiness_threshold — بلوغ عتبة الجاهزية
    """
    gate_map: Dict[ConceptGateID, TransitionGateStatus] = {
        g.gate_id: g.status for g in record.gates
    }
    passed = TransitionGateStatus.PASSED
    return {
        "lexeme_match": record.isomorphism.all_match,
        "type_established": gate_map.get(ConceptGateID.GATE_TYPE) is passed,
        "direction_established": gate_map.get(ConceptGateID.GATE_DIRECTION) is passed,
        "up_ea_established": (
            gate_map.get(ConceptGateID.GATE_UNIVERSAL_PARTICULAR) is passed
            and gate_map.get(ConceptGateID.GATE_ENTITY_ATTRIBUTE) is passed
        ),
        "load_established": (
            gate_map.get(ConceptGateID.GATE_REFERENCE_LOAD) is passed
            or gate_map.get(ConceptGateID.GATE_PREDICATIVE_LOAD) is passed
        ),
        "role_established": gate_map.get(ConceptGateID.GATE_ROLE_READINESS) is passed,
        "recoverable": gate_map.get(ConceptGateID.GATE_RECOVERABILITY) is passed,
        "readiness_threshold": record.valid,
    }


# ═══════════════════════════════════════════════════════════════════════
# Main factory (المادة 78–82)
# ═══════════════════════════════════════════════════════════════════════


def build_single_concept(
    closure: LexicalClosure,
    concept: Concept,
    dalala_type: DalalaType = DalalaType.MUTABAQA,
    *,
    universal_particular: Optional[ConceptUniversalParticular] = None,
    entity_attribute: Optional[ConceptEntityAttribute] = None,
    candidate_role: Optional[CandidateRole] = None,
    closure_status: ConceptClosureStatus = ConceptClosureStatus.CLOSED,
    independence: ConceptIndependence = ConceptIndependence.ORIGINAL,
    threshold: float = 0.7,
    record_id: Optional[str] = None,
    notes: str = "",
) -> SingleConceptRecord:
    """Build a complete :class:`SingleConceptRecord` from a closure/concept pair.

    This is the top-level factory that enforces the evaluation order
    mandated by the Single Concept Constitution::

        تعيين → حفظ → ربط → حكم → انتقال → رد

    Args:
        closure:              The lexical closure (signifier surface form).
        concept:              The ontological concept node (signified).
        dalala_type:          The classical signification type for this pair.
        universal_particular: Override UP; inferred from POS if ``None``.
        entity_attribute:     Override EA; inferred from POS if ``None``.
        candidate_role:       Override role; inferred from type+POS if ``None``.
        closure_status:       Concept closure status (default CLOSED).
        independence:         Concept independence level (default ORIGINAL).
        threshold:            Readiness threshold θ_RC (default 0.7).
        record_id:            Optional explicit record ID; auto-generated if ``None``.
        notes:                Free-text annotation.

    Returns:
        A frozen :class:`SingleConceptRecord` with ``valid`` set to ``True``
        iff ``readiness_score >= threshold`` and all isomorphism axes hold.
    """
    # Step 1: Classify concept type (تعيين)
    concept_type = classify_concept_type(concept)

    # Step 2: Infer UP if not provided
    up = universal_particular or _POS_TO_UP.get(
        closure.pos, ConceptUniversalParticular.UNIVERSAL
    )

    # Step 3: Infer EA if not provided
    ea = entity_attribute or _POS_TO_EA.get(
        closure.pos, ConceptEntityAttribute.ENTITY
    )

    # Step 4: Infer candidate role if not provided
    role = candidate_role or classify_candidate_role(concept_type, closure)

    # Step 5: Check isomorphism (ربط)
    isomorphism = check_isomorphism(closure, concept, concept_type)

    # Step 6: Analyze dalala
    dalala = analyze_dalala(closure, concept, dalala_type)

    # Step 7: Compute loads
    ref_load = _DALALA_REF_LOAD.get(dalala_type, 0.5)
    pred_load = _DALALA_PRED_LOAD.get(dalala_type, 0.5)

    # Step 8: Run all 8 gates (حكم)
    gates: Tuple[SingleConceptGateResult, ...] = (
        _check_gate_type(concept, closure),
        _check_gate_direction(concept, closure, concept_type),
        _check_gate_universal_particular(up),
        _check_gate_entity_attribute(ea),
        _check_gate_reference_load(concept, closure, ref_load),
        _check_gate_predicative_load(concept, pred_load),
        _check_gate_role_readiness(role, concept_type),
        _check_gate_recoverability(concept, closure, concept_type),
    )

    # Step 9: Compute readiness score
    readiness = compute_readiness(gates)

    # Step 10: Determine validity
    valid = readiness >= threshold and isomorphism.all_match

    rid = record_id or _next_sc_id()

    return SingleConceptRecord(
        record_id=rid,
        lexeme_ref=closure.surface,
        concept_type=concept_type,
        direction=dalala_type,
        universal_particular=up,
        entity_attribute=ea,
        reference_load=ref_load,
        predicative_load=pred_load,
        candidate_role=role,
        closure_status=closure_status,
        independence=independence,
        isomorphism=isomorphism,
        dalala=dalala,
        gates=gates,
        readiness_score=readiness,
        valid=valid,
        notes=notes,
    )


def build_single_concept_batch(
    pairs: List[Tuple[LexicalClosure, Concept]],
    dalala_type: DalalaType = DalalaType.MUTABAQA,
    **kwargs: object,
) -> List[SingleConceptRecord]:
    """Build a list of :class:`SingleConceptRecord` from (closure, concept) pairs.

    Args:
        pairs:       List of ``(LexicalClosure, Concept)`` tuples.
        dalala_type: Default dalāla type for all pairs.
        **kwargs:    Forwarded to :func:`build_single_concept`.

    Returns:
        A list of :class:`SingleConceptRecord` objects, one per pair.
    """
    return [
        build_single_concept(cl, co, dalala_type, **kwargs)  # type: ignore[arg-type]
        for cl, co in pairs
    ]
