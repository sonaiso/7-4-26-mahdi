"""Reference Constitution v1 — دستور الإحالة v1.0.

Implements the Reference (إحالة) system as a pre-compositional conceptual
structure that governs how entities (ذات) and attributes (صفة) bind to
referents, how reference tools work, and how referential closure degrees
are determined — all before syntax/composition.

الإحالة شرط إمكان للمفهوم المفرد قبل التركيب، لأنها تضبط كيف يرتبط المفهوم
بمرجع مخصوص أو بدائرة مرجعية، وكيف تختلف الذات عن الصفة من جهة الإحالة،
وكيف تتدرج الإحالة بين المغلق وشبه المغلق والمفتوح والتابع، وكيف تعمل
أدواتها. ولا يعتمد هذا النظام حتى يستوفي الحد الأدنى المكتمل ويخضع للقانون
الفراكتالي من التعيين والحفظ والربط والحكم والانتقال والرد. وبذلك يصير المفهوم
المفرد جاهزًا للإسناد قبل التركيب.

Public API
----------
classify_reference_type(closure, concept, *, context) → ReferenceType
classify_reference_degree(ref_type, closure, concept, *, definiteness) → ReferenceDegree
classify_tool_kind(closure, ref_type) → Optional[ReferenceToolKind]
classify_predication_basis(concept, ref_type) → PredicationBasis
classify_origin(concept, ref_type) → ReferenceOrigin
evaluate_predication_readiness(ref_record) → PredicationReadinessScore
detect_attribute_transition(concept, closure, ref_type, ref_degree) → Optional[ReferenceTransition]
build_reference_record(closure, concept, ...) → ReferenceRecord
batch_build(closures, concepts, ...) → List[ReferenceRecord]
validate_reference(ref_record) → bool
get_fractal_stages() → Tuple[str, ...]
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from arabic_engine.core.enums import (
    POS,
    DefinitenessRole,
    PredicationBasis,
    ReferenceDegree,
    ReferenceOrigin,
    ReferenceToolKind,
    ReferenceType,
    SemanticType,
    UniversalParticular,
)
from arabic_engine.core.types import (
    Concept,
    LexicalClosure,
    PredicationReadinessScore,
    ReferenceRecord,
    ReferenceTransition,
)

# ── Internal counters for auto-generated IDs ─────────────────────────

_ref_counter = 0

_READINESS_THRESHOLD = 0.6


def _next_ref_id() -> str:
    """Return the next sequential reference record ID."""
    global _ref_counter
    _ref_counter += 1
    return f"REF_{_ref_counter:03d}"


# ── POS → ReferenceType mapping ──────────────────────────────────────

_POS_TO_REF_TYPE: Dict[POS, ReferenceType] = {
    POS.DAMIR: ReferenceType.PRONOMINAL,
    POS.SIFA: ReferenceType.DESCRIPTIVE,
    POS.ZARF: ReferenceType.TEMPORAL,
    POS.ISM: ReferenceType.SELF_REFERENCE,
    POS.FI3L: ReferenceType.DESCRIPTIVE,
    POS.HARF: ReferenceType.DEPENDENT,
    POS.UNKNOWN: ReferenceType.SELF_REFERENCE,
}

# ── POS → ReferenceToolKind mapping ──────────────────────────────────

_POS_TO_TOOL: Dict[POS, ReferenceToolKind] = {
    POS.DAMIR: ReferenceToolKind.PRONOUN,
    POS.SIFA: ReferenceToolKind.RESTRICTIVE_ADJUNCT,
    POS.ZARF: ReferenceToolKind.TIME_PLACE,
    POS.ISM: ReferenceToolKind.PROPER_NAME,
    POS.FI3L: ReferenceToolKind.STATE_SPECIFICATION,
    POS.HARF: ReferenceToolKind.GENITIVE_CONSTRUCT,
}

# ── ReferenceType → default ReferenceDegree mapping ──────────────────

_REF_TYPE_TO_DEGREE: Dict[ReferenceType, ReferenceDegree] = {
    ReferenceType.SELF_REFERENCE: ReferenceDegree.CLOSED,
    ReferenceType.PRONOMINAL: ReferenceDegree.CLOSED,
    ReferenceType.DEMONSTRATIVE: ReferenceDegree.CLOSED,
    ReferenceType.RELATIVE: ReferenceDegree.SEMI_CLOSED,
    ReferenceType.DESCRIPTIVE: ReferenceDegree.SEMI_CLOSED,
    ReferenceType.TEMPORAL: ReferenceDegree.SEMI_CLOSED,
    ReferenceType.SPATIAL: ReferenceDegree.SEMI_CLOSED,
    ReferenceType.NUMERICAL: ReferenceDegree.SEMI_CLOSED,
    ReferenceType.DEPENDENT: ReferenceDegree.DEPENDENT,
    ReferenceType.EXPLICATIVE: ReferenceDegree.DEPENDENT,
}

# ── Demonstrative lemmas (أسماء الإشارة) ─────────────────────────────

_DEMONSTRATIVE_LEMMAS = frozenset({
    "هذا", "هذه", "ذلك", "تلك", "هؤلاء", "أولئك",
    "ذاك", "هاتان", "هذان",
})

# ── Relative noun lemmas (الأسماء الموصولة) ──────────────────────────

_RELATIVE_LEMMAS = frozenset({
    "الذي", "التي", "اللذان", "اللتان", "الذين", "اللاتي",
    "اللواتي", "من", "ما",
})

# ── Spatial lemmas ───────────────────────────────────────────────────

_SPATIAL_LEMMAS = frozenset({
    "هنا", "هناك", "هنالك", "حيث", "فوق", "تحت",
    "أمام", "خلف", "يمين", "شمال",
})

# ── Temporal lemmas ──────────────────────────────────────────────────

_TEMPORAL_LEMMAS = frozenset({
    "الآن", "أمس", "غدًا", "غداً", "حين", "عندما",
    "إذ", "بعد", "قبل", "منذ",
})

# ── Number-related lemmas ────────────────────────────────────────────

_NUMBER_LEMMAS = frozenset({
    "واحد", "اثنان", "ثلاث", "ثلاثة", "أربع", "أربعة",
    "خمس", "خمسة", "ست", "ستة", "سبع", "سبعة",
    "ثمان", "ثمانية", "تسع", "تسعة", "عشر", "عشرة",
    "مائة", "مئة", "ألف",
})


# ── Internal helpers ─────────────────────────────────────────────────


def _infer_definiteness(closure: LexicalClosure) -> DefinitenessRole:
    """Infer definiteness from the surface form (المواد 52–55)."""
    surface = closure.surface.strip()
    # Proper name marker or definite article
    if surface.startswith("ال") or surface.startswith("أل"):
        return DefinitenessRole.DEFINITE
    # Pronouns and demonstratives are inherently definite
    if closure.pos in (POS.DAMIR,):
        return DefinitenessRole.DEFINITE
    lemma = closure.lemma.strip() if closure.lemma else ""
    if lemma in _DEMONSTRATIVE_LEMMAS or lemma in _RELATIVE_LEMMAS:
        return DefinitenessRole.DEFINITE
    return DefinitenessRole.INDEFINITE


def _infer_universality(concept: Concept) -> UniversalParticular:
    """Infer universal/particular from concept properties (المواد 48–51)."""
    props = concept.properties or {}
    if props.get("scope") == "particular":
        return UniversalParticular.PARTICULAR
    if props.get("scope") == "universal":
        return UniversalParticular.UNIVERSAL
    # Entities default to particular; norms/relations default to universal
    if concept.semantic_type in (SemanticType.ENTITY,):
        return UniversalParticular.PARTICULAR
    if concept.semantic_type in (SemanticType.NORM, SemanticType.RELATION):
        return UniversalParticular.UNIVERSAL
    # Attributes and events: check for generality
    return UniversalParticular.UNIVERSAL


# ── Public functions ─────────────────────────────────────────────────


def classify_reference_type(
    closure: LexicalClosure,
    concept: Concept,
    *,
    context: Optional[str] = None,
) -> ReferenceType:
    """Determine the reference type from POS, semantic type, and context (المادة 15).

    Maps POS tags and lexical clues to one of the ten reference types.

    Args:
        closure: The lexical closure to classify.
        concept: The ontological concept node.
        context: Optional context string for disambiguation.

    Returns:
        The inferred :class:`ReferenceType`.
    """
    lemma = closure.lemma.strip() if closure.lemma else ""

    # Check demonstrative lemmas first
    if lemma in _DEMONSTRATIVE_LEMMAS:
        return ReferenceType.DEMONSTRATIVE

    # Check relative noun lemmas
    if lemma in _RELATIVE_LEMMAS:
        return ReferenceType.RELATIVE

    # Check spatial lemmas
    if lemma in _SPATIAL_LEMMAS:
        return ReferenceType.SPATIAL

    # Check temporal lemmas
    if lemma in _TEMPORAL_LEMMAS:
        return ReferenceType.TEMPORAL

    # Check number lemmas
    if lemma in _NUMBER_LEMMAS:
        return ReferenceType.NUMERICAL

    # POS-based mapping
    if closure.pos == POS.ZARF:
        # ZARF can be temporal or spatial — default to temporal
        return ReferenceType.TEMPORAL

    # Context-based overrides
    if context == "hal":
        return ReferenceType.EXPLICATIVE
    if context == "tamyiz":
        return ReferenceType.EXPLICATIVE
    if context == "badal":
        return ReferenceType.DEPENDENT
    if context == "tawkid":
        return ReferenceType.DEPENDENT
    if context == "na3t":
        return ReferenceType.DEPENDENT

    return _POS_TO_REF_TYPE.get(closure.pos, ReferenceType.SELF_REFERENCE)


def classify_reference_degree(
    ref_type: ReferenceType,
    closure: LexicalClosure,
    concept: Concept,
    *,
    definiteness: Optional[DefinitenessRole] = None,
) -> ReferenceDegree:
    """Determine the referential closure degree (المادة 38).

    Uses the reference type, definiteness, and universality to infer
    how closed or open the referent is.

    Args:
        ref_type:      The reference type.
        closure:       The lexical closure.
        concept:       The concept node.
        definiteness:  Optional explicit definiteness override.

    Returns:
        The inferred :class:`ReferenceDegree`.
    """
    # Explicit definiteness adjustment
    defn = definiteness or _infer_definiteness(closure)

    # Start with default from reference type
    degree = _REF_TYPE_TO_DEGREE.get(ref_type, ReferenceDegree.OPEN)

    # Indefinite overrides semi-closed → open for non-pronouns/non-demonstratives
    if defn is DefinitenessRole.INDEFINITE and degree is ReferenceDegree.SEMI_CLOSED:
        degree = ReferenceDegree.OPEN

    # Definite can upgrade open → semi-closed
    if defn is DefinitenessRole.DEFINITE and degree is ReferenceDegree.OPEN:
        degree = ReferenceDegree.SEMI_CLOSED

    return degree


def classify_tool_kind(
    closure: LexicalClosure,
    ref_type: ReferenceType,
) -> Optional[ReferenceToolKind]:
    """Map the lexical closure to a reference tool kind (المادة 26).

    Args:
        closure:  The lexical closure.
        ref_type: The reference type.

    Returns:
        The inferred :class:`ReferenceToolKind`, or ``None`` if no tool
        applies.
    """
    # Reference-type based mapping
    _type_to_tool: Dict[ReferenceType, ReferenceToolKind] = {
        ReferenceType.SELF_REFERENCE: ReferenceToolKind.PROPER_NAME,
        ReferenceType.PRONOMINAL: ReferenceToolKind.PRONOUN,
        ReferenceType.DEMONSTRATIVE: ReferenceToolKind.DEMONSTRATIVE,
        ReferenceType.RELATIVE: ReferenceToolKind.RELATIVE_NOUN,
        ReferenceType.TEMPORAL: ReferenceToolKind.TIME_PLACE,
        ReferenceType.SPATIAL: ReferenceToolKind.TIME_PLACE,
        ReferenceType.NUMERICAL: ReferenceToolKind.NUMERAL,
        ReferenceType.EXPLICATIVE: ReferenceToolKind.STATE_SPECIFICATION,
    }
    tool = _type_to_tool.get(ref_type)
    if tool is not None:
        return tool

    # For DEPENDENT, use POS to disambiguate
    if ref_type is ReferenceType.DEPENDENT:
        return _POS_TO_TOOL.get(closure.pos, ReferenceToolKind.RESTRICTIVE_ADJUNCT)

    # For DESCRIPTIVE, use the adjunct tool
    if ref_type is ReferenceType.DESCRIPTIVE:
        return ReferenceToolKind.RESTRICTIVE_ADJUNCT

    return _POS_TO_TOOL.get(closure.pos)


def classify_predication_basis(
    concept: Concept,
    ref_type: ReferenceType,
) -> PredicationBasis:
    """Determine predication vs reference basis (المواد 7–12).

    Entities are originally referential (أصل في الإحالة).
    Attributes are originally predicational (أصل في الحمل).

    Args:
        concept:  The concept node.
        ref_type: The reference type.

    Returns:
        :class:`PredicationBasis`.
    """
    # Entities and proper-name references are fundamentally referential
    if concept.semantic_type in (SemanticType.ENTITY, SemanticType.EVENT):
        return PredicationBasis.REFERENCE

    # Attributes are fundamentally predicational
    if concept.semantic_type is SemanticType.ATTRIBUTE:
        # Unless they have transitioned to reference
        if ref_type in (
            ReferenceType.SELF_REFERENCE,
            ReferenceType.PRONOMINAL,
            ReferenceType.DEMONSTRATIVE,
        ):
            return PredicationBasis.REFERENCE
        return PredicationBasis.PREDICATION

    # Relations and norms are predicational by default
    return PredicationBasis.PREDICATION


def classify_origin(
    concept: Concept,
    ref_type: ReferenceType,
) -> ReferenceOrigin:
    """Determine whether the concept is originally referential (المواد 12–13).

    Args:
        concept:  The concept node.
        ref_type: The reference type.

    Returns:
        :class:`ReferenceOrigin`.
    """
    # Dependent and explicative references are subordinate regardless of semantic type
    if ref_type in (ReferenceType.DEPENDENT, ReferenceType.EXPLICATIVE):
        return ReferenceOrigin.SUBORDINATE

    # Entities are primary referents
    if concept.semantic_type is SemanticType.ENTITY:
        return ReferenceOrigin.PRIMARY

    # Attributes, events, etc. that function as references are derived
    if concept.semantic_type in (
        SemanticType.ATTRIBUTE,
        SemanticType.EVENT,
        SemanticType.RELATION,
        SemanticType.NORM,
    ):
        return ReferenceOrigin.DERIVED

    return ReferenceOrigin.PRIMARY


def evaluate_predication_readiness(
    ref_record: ReferenceRecord,
    *,
    threshold: float = _READINESS_THRESHOLD,
) -> PredicationReadinessScore:
    """Compute the 5-component predication readiness score (المادة 87).

    Ready_Ref = (Type + Degree + Anchor + Tool + Recover) / 5

    Each component ∈ [0.0, 1.0], ready iff total ≥ threshold.

    Args:
        ref_record: The reference record to evaluate.
        threshold:  Readiness threshold (default 0.6).

    Returns:
        A :class:`PredicationReadinessScore`.
    """
    # Type: is the reference type set?
    type_score = 1.0 if ref_record.reference_type is not None else 0.0

    # Degree: is the degree known and not just OPEN?
    if ref_record.reference_degree is ReferenceDegree.CLOSED:
        degree_score = 1.0
    elif ref_record.reference_degree is ReferenceDegree.SEMI_CLOSED:
        degree_score = 0.8
    elif ref_record.reference_degree is ReferenceDegree.DEPENDENT:
        degree_score = 0.6
    else:
        degree_score = 0.3  # OPEN

    # Anchor: is the referent non-empty?
    anchor_score = 1.0 if ref_record.referent.strip() else 0.0

    # Tool: is the tool specified?
    tool_score = 1.0 if ref_record.tool_kind is not None else 0.5

    # Recover: can the record be traced back to origin?
    recover_score = 1.0 if ref_record.origin is not None else 0.0

    total = (type_score + degree_score + anchor_score + tool_score + recover_score) / 5.0
    ready = total >= threshold

    return PredicationReadinessScore(
        type_score=type_score,
        degree_score=degree_score,
        anchor_score=anchor_score,
        tool_score=tool_score,
        recover_score=recover_score,
        total=round(total, 4),
        ready=ready,
    )


def detect_attribute_transition(
    concept: Concept,
    closure: LexicalClosure,
    ref_type: ReferenceType,
    ref_degree: ReferenceDegree,
) -> Optional[ReferenceTransition]:
    """Detect if an attribute has transitioned from predication to reference (المواد 44–47).

    A transition occurs when an attribute (صفة):
    - is used as a proper name (استقلت اسميًا)
    - restricts the referent so tightly it becomes identifying
    - stands in place of the entity

    Args:
        concept:    The concept node.
        closure:    The lexical closure.
        ref_type:   The classified reference type.
        ref_degree: The classified reference degree.

    Returns:
        A :class:`ReferenceTransition` if transition detected, else ``None``.
    """
    # Only attributes can transition
    if concept.semantic_type is not SemanticType.ATTRIBUTE:
        return None

    # Transition: attribute used as self-reference (substantivised adjective)
    if ref_type is ReferenceType.SELF_REFERENCE:
        return ReferenceTransition(
            source_concept_id=concept.concept_id,
            from_basis=PredicationBasis.PREDICATION,
            to_basis=PredicationBasis.REFERENCE,
            reason="attribute_substantivised",
            resulting_degree=ref_degree,
        )

    # Transition: attribute used pronominally
    if ref_type is ReferenceType.PRONOMINAL:
        return ReferenceTransition(
            source_concept_id=concept.concept_id,
            from_basis=PredicationBasis.PREDICATION,
            to_basis=PredicationBasis.REFERENCE,
            reason="attribute_pronominally_used",
            resulting_degree=ref_degree,
        )

    # Transition: descriptive attribute that became closed
    if (
        ref_type is ReferenceType.DESCRIPTIVE
        and ref_degree in (ReferenceDegree.CLOSED, ReferenceDegree.SEMI_CLOSED)
    ):
        return ReferenceTransition(
            source_concept_id=concept.concept_id,
            from_basis=PredicationBasis.PREDICATION,
            to_basis=PredicationBasis.REFERENCE,
            reason="descriptive_closure",
            resulting_degree=ref_degree,
        )

    return None


def build_reference_record(
    closure: LexicalClosure,
    concept: Concept,
    *,
    record_id: Optional[str] = None,
    referent: str = "",
    context: Optional[str] = None,
    definiteness: Optional[DefinitenessRole] = None,
    universality: Optional[UniversalParticular] = None,
    notes: str = "",
) -> ReferenceRecord:
    """Build a complete :class:`ReferenceRecord` from a closure/concept pair.

    Follows the fractal law pattern (المادة 78):
    تعيين → حفظ → ربط → حكم → انتقال → رد

    Args:
        closure:       The lexical closure (signifier surface form).
        concept:       The ontological concept node.
        record_id:     Optional explicit record ID; auto-generated if omitted.
        referent:      The referent string (المرجع).
        context:       Optional context hint for disambiguation.
        definiteness:  Optional explicit definiteness.
        universality:  Optional explicit universality.
        notes:         Free-text annotation.

    Returns:
        A frozen :class:`ReferenceRecord`.
    """
    rid = record_id or _next_ref_id()

    # Stage 1: تعيين — Determine reference type
    ref_type = classify_reference_type(closure, concept, context=context)

    # Stage 2: حفظ — Determine degree and tools
    defn = definiteness or _infer_definiteness(closure)
    ref_degree = classify_reference_degree(ref_type, closure, concept, definiteness=defn)
    tool = classify_tool_kind(closure, ref_type)

    # Stage 3: ربط — Link to predication basis
    basis = classify_predication_basis(concept, ref_type)

    # Stage 4: حكم — Judge origin
    origin = classify_origin(concept, ref_type)

    # Infer universality if not provided
    univ = universality or _infer_universality(concept)

    # Determine referent: use provided or derive from surface/label
    ref_str = referent or concept.label or closure.surface

    # Determine subject type from semantic type
    _stype_to_subject: Dict[SemanticType, str] = {
        SemanticType.ENTITY: "ذات",
        SemanticType.ATTRIBUTE: "صفة",
        SemanticType.EVENT: "حدث",
        SemanticType.RELATION: "علاقة",
        SemanticType.NORM: "حكم",
    }
    subject_type = _stype_to_subject.get(concept.semantic_type, "ذات")

    # Stage 5: انتقال — Check for attribute transition
    transition = detect_attribute_transition(concept, closure, ref_type, ref_degree)
    if transition is not None:
        basis = PredicationBasis.REFERENCE
        origin = ReferenceOrigin.DERIVED

    # Stage 6: رد — Build final record
    # Preliminary record for readiness evaluation
    preliminary = ReferenceRecord(
        record_id=rid,
        subject_type=subject_type,
        reference_type=ref_type,
        reference_degree=ref_degree,
        tool_kind=tool,
        predication_relation=basis,
        referent=ref_str,
        ready_for_predication=False,
        origin=origin,
        definiteness=defn,
        universality=univ,
        confidence=1.0,
        notes=notes,
    )
    readiness = evaluate_predication_readiness(preliminary)

    return ReferenceRecord(
        record_id=rid,
        subject_type=subject_type,
        reference_type=ref_type,
        reference_degree=ref_degree,
        tool_kind=tool,
        predication_relation=basis,
        referent=ref_str,
        ready_for_predication=readiness.ready,
        origin=origin,
        definiteness=defn,
        universality=univ,
        confidence=1.0,
        notes=notes,
    )


def batch_build(
    closures: List[LexicalClosure],
    concepts: List[Concept],
    *,
    referents: Optional[List[str]] = None,
    contexts: Optional[List[Optional[str]]] = None,
    definiteness_flags: Optional[List[Optional[DefinitenessRole]]] = None,
    universality_flags: Optional[List[Optional[UniversalParticular]]] = None,
) -> List[ReferenceRecord]:
    """Build a list of :class:`ReferenceRecord` from parallel input lists.

    Args:
        closures:           Lexical closures (signifiers).
        concepts:           Concept nodes, parallel to *closures*.
        referents:          Per-item referent; defaults to empty string.
        contexts:           Per-item context hint; defaults to None.
        definiteness_flags: Per-item definiteness; defaults to None.
        universality_flags: Per-item universality; defaults to None.

    Returns:
        A list of :class:`ReferenceRecord` objects, one per input pair.
    """
    n = len(closures)
    refs = referents or [""] * n
    ctxs = contexts or [None] * n
    defs = definiteness_flags or [None] * n
    univs = universality_flags or [None] * n
    return [
        build_reference_record(
            closures[i],
            concepts[i],
            referent=refs[i],
            context=ctxs[i],
            definiteness=defs[i],
            universality=univs[i],
        )
        for i in range(n)
    ]


def validate_reference(ref_record: ReferenceRecord) -> bool:
    """Validate a reference record against acceptance criteria (المواد 86–89).

    A reference is valid iff:
    1. Reference type is set
    2. Reference degree is set
    3. Tool kind is set or the record is OPEN
    4. Referent is non-empty
    5. Entity/attribute distinction is clear (subject_type is set)
    6. Predication/reference basis is set
    7. Predication readiness is achieved

    Args:
        ref_record: The reference record to validate.

    Returns:
        ``True`` if the record passes all checks, ``False`` otherwise.
    """
    # 1. Reference type must be set
    if ref_record.reference_type is None:
        return False

    # 2. Reference degree must be set
    if ref_record.reference_degree is None:
        return False

    # 3. Tool kind: must be set unless reference degree is OPEN
    if ref_record.tool_kind is None and ref_record.reference_degree is not ReferenceDegree.OPEN:
        return False

    # 4. Referent must be non-empty
    if not ref_record.referent.strip():
        return False

    # 5. Subject type must be set
    if not ref_record.subject_type.strip():
        return False

    # 6. Predication relation must be set
    if ref_record.predication_relation is None:
        return False

    # 7. Readiness
    readiness = evaluate_predication_readiness(ref_record)
    return readiness.ready


def get_fractal_stages() -> Tuple[str, ...]:
    """Return the 6 fractal law stages (المادة 78).

    Returns:
        A tuple of the six stage names in Arabic.
    """
    return ("تعيين", "حفظ", "ربط", "حكم", "انتقال", "رد")
