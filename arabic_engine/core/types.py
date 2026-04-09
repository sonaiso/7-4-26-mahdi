"""Data types (named tuples / dataclasses) for the Arabic engine.

Every stage of the pipeline produces and consumes typed records so that
all data flowing through the system is a *discrete, numerically-encoded*
structure — satisfying the computability proof in the README.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, List, Optional, Tuple

from .enums import (
    POS,
    CellType,
    CombinationType,
    ConditionToken,
    ConstraintType,
    DalalaType,
    ElementClass,
    ElementFunction,
    ElementLayer,
    EvidenceType,
    FunctionRole,
    FuncTransitionClass,
    GuidanceState,
    IrabCase,
    IrabRole,
    LinguisticZeroType,
    MafhumType,
    OntologicalLayer,
    OntologicalMode,
    PhonCategory,
    PhonFeature,
    PhonGroup,
    PhonTransform,
    ProofStatus,
    RankType,
    ReversibleValue,
    SemanticType,
    SlotState,
    SpaceRef,
    SyllablePosition,
    TimeRef,
    TransitionCondition,
    TransitionLaw,
    TransitionType,
    TriadType,
    TruthState,
    UnicodeProfileType,
    WordClass,
    ZeroCoverage,
)

# ── Signifier layer ─────────────────────────────────────────────────

@dataclass(frozen=True)
class Grapheme:
    """A single grapheme cluster: base code-point + diacritics."""
    base: int               # Unicode code-point of the consonant/vowel letter
    marks: Tuple[int, ...]  # code-points of combining marks (tashkīl)

    @property
    def char(self) -> str:
        return chr(self.base) + "".join(chr(m) for m in self.marks)


@dataclass(frozen=True)
class Syllable:
    """Phonological syllable: onset, nucleus, coda, weight."""
    onset: Tuple[int, ...]
    nucleus: Tuple[int, ...]
    coda: Tuple[int, ...]
    weight: int  # 1 = light, 2 = heavy, 3 = super-heavy


@dataclass(frozen=True)
class RootPattern:
    """Extracted root and morphological pattern."""
    root: Tuple[str, ...]        # e.g. ('ك','ت','ب')
    pattern: str                 # e.g. 'فَعَلَ'
    root_id: int = 0
    pattern_id: int = 0


# ── Lexical Closure ─────────────────────────────────────────────────

@dataclass
class LexicalClosure:
    """Full morphological + lexical record for a token (التعريف 4)."""
    surface: str
    lemma: str
    root: Tuple[str, ...]
    pattern: str
    pos: POS
    lemma_id: int = 0
    root_id: int = 0
    pattern_id: int = 0
    pos_id: int = 0
    features: dict = field(default_factory=dict)
    # ── v2 fields ───────────────────────────────────────────────
    case_mark: IrabCase = IrabCase.UNKNOWN
    syntax_role: IrabRole = IrabRole.UNKNOWN
    temporal: TimeRef = TimeRef.UNSPECIFIED
    spatial: SpaceRef = SpaceRef.UNSPECIFIED
    confidence: float = 1.0


# ── Signified layer ─────────────────────────────────────────────────

@dataclass
class Concept:
    """An ontological node — the *signified* (التعريف 5)."""
    concept_id: int
    label: str
    semantic_type: SemanticType
    properties: dict = field(default_factory=dict)


# ── Linkage layer ───────────────────────────────────────────────────

@dataclass
class DalalaLink:
    """A validated signification link (التعريف 6)."""
    source_lemma: str
    target_concept_id: int
    dalala_type: DalalaType
    accepted: bool
    confidence: float  # ∈ [0, 1]


# ── Cognition layer ─────────────────────────────────────────────────

@dataclass
class Proposition:
    """A structured judgment / proposition (التعريف 7)."""
    subject: str
    predicate: str
    obj: str
    time: TimeRef = TimeRef.UNSPECIFIED
    space: SpaceRef = SpaceRef.UNSPECIFIED
    polarity: bool = True  # True = affirmative


@dataclass
class EvalResult:
    """Final evaluation vector (التعريف 8)."""
    proposition: Proposition
    truth_state: TruthState
    guidance_state: GuidanceState
    confidence: float


# ── Syntax layer (v2) ───────────────────────────────────────────────

@dataclass
class SyntaxNode:
    """A node in the i'rāb (syntactic) tree."""
    token: str
    lemma: str
    pos: POS
    case: IrabCase
    role: IrabRole
    governor: Optional[str] = None  # the word that governs this node
    dependents: List[str] = field(default_factory=list)


# ── Time / Space tag (v2) ───────────────────────────────────────────

@dataclass
class TimeSpaceTag:
    """Temporal and spatial anchoring for a proposition."""
    time_ref: TimeRef
    space_ref: SpaceRef
    time_detail: str = ""   # e.g. "أمس", "غدًا"
    space_detail: str = ""  # e.g. "المدينة"


# ── World model fact (v2) ───────────────────────────────────────────

@dataclass
class WorldFact:
    """A fact held in the world-model knowledge base."""
    fact_id: int
    subject: str
    predicate: str
    obj: str
    truth_state: TruthState = TruthState.CERTAIN
    source: str = "axiom"


# ── Inference result (v2) ───────────────────────────────────────────

@dataclass
class InferenceResult:
    """Result of applying an inference rule."""
    rule_name: str
    premises: List[Proposition]
    conclusion: Proposition
    confidence: float
    valid: bool


# ── Mafhūm layer (Ch. 21) ──────────────────────────────────────────

@dataclass
class MafhumPillar:
    """The four pillars (أركان) required for a Mafhūm to hold.

    A Mafhūm is valid only when all four pillars are present:
      1. closed_mantuq   — the Manṭūq is closed (منطوق مغلق)
      2. constraint_type — a structural constraint exists (قيد بنيوي)
      3. mental_counterpart — a mental counterpart can be formed (مقابل ذهني)
      4. transition_rule — a transition rule applies (قاعدة انتقال)
    """
    closed_mantuq: bool
    constraint_type: ConstraintType
    mental_counterpart: str
    transition_rule: str


@dataclass
class MafhumResult:
    """Result of Mafhūm (implied meaning) analysis (Ch. 21).

    Captures the derivation of an implied concept from the explicit
    text (Manṭūq) via one of the five minimal Mafhūm types.
    """
    mafhum_type: MafhumType
    constraint_type: ConstraintType
    pillars: MafhumPillar
    source_text: str           # the original Manṭūq fragment
    constraint_value: str      # the specific constraint detected
    counterpart: str           # the mental counterpart (المقابل الذهني)
    derived_meaning: str       # the derived implied meaning
    valid: bool                # whether all four pillars hold
    confidence: float          # confidence in [0, 1]


# ── D_min — Minimal Complete Phonological Representation ────────────

@dataclass(frozen=True)
class DMin:
    """Minimal Complete Representation — الأدنى المكتمل.

    Implements the mathematical function::

        D_min(x) = (u, c, g, f, t)

    where every field maps to a computable integer, making the full
    5-tuple a numeric vector in ℕ⁵:

    =========  ======================  ================================
    Field       Type                    Encoding
    =========  ======================  ================================
    unicode     int                     u — Unicode code-point
    category    PhonCategory            c — enum integer value
    group       PhonGroup               g — enum integer value
    features    FrozenSet[PhonFeature]  f — bitmask (2^(v-1) per bit)
    transforms  FrozenSet[PhonTransform] t — bitmask (2^(v-1) per bit)
    =========  ======================  ================================

    The ``code`` field holds the human-readable MinCode string
    (e.g. ``'C:SHF:SHD:MJH'``) and is not part of the numeric vector.
    """

    unicode: int
    category: PhonCategory
    group: PhonGroup
    features: FrozenSet[PhonFeature]
    transforms: FrozenSet[PhonTransform]
    code: str = ""

    # ── Derived string / numeric properties ─────────────────────────

    @property
    def char(self) -> str:
        """Unicode character for this phonological unit."""
        return chr(self.unicode)

    @property
    def feature_mask(self) -> int:
        """Integer bitmask encoding ``features``.

        Bit ``f.value - 1`` is set for each ``f`` in ``self.features``,
        so the result is a unique integer in ``[0, 2^|PhonFeature| - 1]``.
        """
        mask = 0
        for f in self.features:
            mask |= 1 << (f.value - 1)
        return mask

    @property
    def transform_mask(self) -> int:
        """Integer bitmask encoding ``transforms``."""
        mask = 0
        for t in self.transforms:
            mask |= 1 << (t.value - 1)
        return mask

    @property
    def vector(self) -> Tuple[int, int, int, int, int]:
        """Numeric 5-vector ``(u, c, g, f_mask, t_mask) ∈ ℕ⁵``.

        This is the core numeric encoding of ``D_min(x)``:

        * ``u``      — Unicode code-point (identity)
        * ``c``      — ``PhonCategory`` ordinal
        * ``g``      — ``PhonGroup`` ordinal
        * ``f_mask`` — feature bitmask
        * ``t_mask`` — transform bitmask
        """
        return (
            self.unicode,
            self.category.value,
            self.group.value,
            self.feature_mask,
            self.transform_mask,
        )


# ── Transition Engine — قانون الانتقال بين الخانات ──────────────────

@dataclass(frozen=True)
class TransitionContext:
    """السياق الذي يحكم الانتقال — contextual inputs to the transition function.

    Implements the parameters of::

        T_r(E) = f(P, N, F, W, Ec, M)

    ============  ========================  ===================================
    Parameter      Field                    Description
    ============  ========================  ===================================
    P              position                 syllable position of the element
    N              left_neighbor /          adjacent DMin units (or None)
                   right_neighbor
    F              function_role            morpho-syntactic role
    W              pattern                  prosodic / morphological pattern
    Ec             economy_pressure         phonetic economy demand (0–1)
    M              architecture             macro-architecture type label
    ============  ========================  ===================================
    """

    position: SyllablePosition
    function_role: FunctionRole
    left_neighbor: Optional["DMin"] = None   # type: ignore[name-defined]
    right_neighbor: Optional["DMin"] = None  # type: ignore[name-defined]
    pattern: str = ""                        # e.g. "فَعَلَ", "اسْتَفْعَلَ"
    economy_pressure: float = 0.0            # 0 = none, 1 = maximum
    architecture: str = ""                   # e.g. "مجرد", "مزيد", "مشتق"


@dataclass(frozen=True)
class TransitionRule:
    """قاعدة انتقال واحدة — a single row in the formal transition matrix.

    Represents a directed transition::

        from_category [from_features] → to_category [to_features]
        | law | transition_type | conditions | priority | example

    A rule is *applicable* to an element E in context C when:
      * E.category matches ``from_category`` (None = any)
      * E.features ⊇ ``required_features``
      * the transition law is compatible with C
    """

    law: TransitionLaw
    transition_type: TransitionType
    from_category: Optional[PhonCategory]                # None = any category
    required_features: FrozenSet[PhonFeature]            # features element must have
    to_category: PhonCategory                            # target cell category
    resulting_transform: PhonTransform                   # transform that fires
    conditions: FrozenSet[TransitionCondition]
    priority: int                                        # lower = higher precedence
    description_ar: str                                  # Arabic description
    example: str                                         # canonical Arabic example


@dataclass
class TransitionResult:
    """نتيجة تطبيق قانون الانتقال — result of the transition engine.

    The optimality criterion applied is::

        E_new = ArgMin(loss_root, loss_pattern, phonetic_burden)
        subject to: E_new ∈ Nearest_Valid_Functional_Cell
    """

    source_unicode: int               # codepoint of the original element
    applied_rule: Optional[TransitionRule]  # the winning rule (None = stable)
    stable: bool                      # True if no transition occurred
    target_category: Optional[PhonCategory]  # new cell category (None = deleted)
    surface_form: str                 # resulting surface character(s)
    loss_root: float                  # cost: root integrity loss ∈ [0, 1]
    loss_pattern: float               # cost: pattern integrity loss ∈ [0, 1]
    phonetic_burden: float            # cost: articulatory burden ∈ [0, 1]
    total_cost: float                 # = loss_root + loss_pattern + phonetic_burden
    conditions_met: FrozenSet[TransitionCondition]
    notes: str = ""                   # optional diagnostic string


# ── Functional Transition Schema types ──────────────────────────────

@dataclass(frozen=True)
class FunctionalTransitionRecord:
    """سجل الانتقال الوظيفي — a single record in the functional transition dataset.

    This type mirrors the JSON Schema defined in
    ``arabic_engine/data/transition_record.schema.json`` and the seed data
    in ``arabic_engine/data/transitions_seed_v1.json``.

    The ``preconditions`` and ``blocking_conditions`` fields use
    :class:`~arabic_engine.core.enums.ConditionToken` values, giving a
    typed, computable DSL instead of free-form strings.

    Fields
    ------
    transition_id       ``TR_NNN`` identifier (e.g. ``"TR_001"``)
    source_cell         source :class:`~arabic_engine.core.enums.CellType`
    target_cell         target :class:`~arabic_engine.core.enums.CellType`
    transition_class    broad class of the transition
    preconditions       frozenset of activating :class:`ConditionToken` values
    blocking_conditions frozenset of blocking :class:`ConditionToken` values
    priority            1 (critical) … 5 (fallback)
    reversible          reversibility status
    surface_form        human-readable surface description
    deep_form           human-readable deep-structure description
    evidence_type       kind of evidence supporting this record (optional)
    notes               free-text annotation (optional)
    """

    transition_id: str
    source_cell: CellType
    target_cell: CellType
    transition_class: FuncTransitionClass
    preconditions: FrozenSet[ConditionToken]
    blocking_conditions: FrozenSet[ConditionToken]
    priority: int                        # 1 = critical … 5 = fallback
    reversible: ReversibleValue
    surface_form: str
    deep_form: str
    evidence_type: Optional[EvidenceType] = None
    notes: str = ""


# ── AEU — Alphabetic Encoding Unit ─────────────────────────────────

@dataclass(frozen=True)
class AEU:
    """وحدة الترميز الأبجدي — a single entry in the AEU periodic table.

    Implements the 16-field record::

        AEU = {ID, Name, Class, Function, Referent, Boundary, Necessity,
               Governing_Role, Layer, Combination_Type, Math_Form,
               Unicode_Codepoint, Unicode_Profile, Depends_On, Unlocks,
               Proof_Status}

    The ``math_form`` is an 8-position binary vector ``{0,1}⁸``.
    """

    element_id: str                            # e.g. "AE_001"
    element_name: str                          # e.g. "Hamza"
    element_class: ElementClass
    element_function: ElementFunction
    referent: str                              # الدلالة الوظيفية
    boundary: str                              # الحد الفاصل
    necessity: str                             # الضرورة
    governing_role: str                        # الدور الحاكم
    layer: ElementLayer
    combination_type: CombinationType
    math_form: Tuple[int, ...]                 # 8-bit binary vector
    unicode_codepoint: int
    unicode_profile: UnicodeProfileType
    depends_on: Tuple[str, ...] = ()
    unlocks: Tuple[str, ...] = ()
    proof_status: ProofStatus = ProofStatus.PENDING

    @property
    def char(self) -> str:
        """Unicode character for this element."""
        return chr(self.unicode_codepoint)

    @property
    def math_vector(self) -> Tuple[int, ...]:
        """The 8-position binary math form vector."""
        return self.math_form

    def is_proven(self) -> bool:
        """Return True if the element's proof status is PROVEN."""
        return self.proof_status is ProofStatus.PROVEN

    def to_row(self) -> dict:
        """Serialise to a flat dictionary suitable for tabular display.

        Returns the 16 canonical columns with Pascal_Case keys::

            Element_ID, Name, Class, Function, Referent, Boundary,
            Necessity, Governing_Role, Layer, Combination_Type,
            Math_Form, Unicode_Codepoint, Unicode_Profile,
            Depends_On, Unlocks, Proof_Status
        """
        return {
            "Element_ID": self.element_id,
            "Name": self.element_name,
            "Class": self.element_class.name,
            "Function": self.element_function.name,
            "Referent": self.referent,
            "Boundary": self.boundary,
            "Necessity": self.necessity,
            "Governing_Role": self.governing_role,
            "Layer": self.layer.name,
            "Combination_Type": self.combination_type.name,
            "Math_Form": self.math_form,
            "Unicode_Codepoint": f"U+{self.unicode_codepoint:04X}",
            "Unicode_Profile": self.unicode_profile.name,
            "Depends_On": self.depends_on,
            "Unlocks": self.unlocks,
            "Proof_Status": self.proof_status.name,
        }


# ── Axiom Types — الأصول الخمسة ─────────────────────────────────────

# A1/A2 — أصل الموضع الصفري والتحقق الموجب الأول

@dataclass(frozen=True)
class ZeroSlotRecord:
    """الموضع الصفري البنيوي — a structural zero-slot (A1) that can admit
    a first positive occupancy (A2).

    Implements the axioms::

        A1. ∃z (ZeroSlot(z) ∧ Fillable(z))
        A2. ∀z (ZeroSlot(z) ∧ Fillable(z) → ∃x Occupies(x,z))

    And the consequence::

        C1. ZeroSlot ≠ ∅   (the zero-slot is not absolute nothingness)
        C2. OneBase = FirstPositiveOccupancy(ZeroSlot)

    Fields
    ------
    slot_id             unique identifier (e.g. ``"ZS_001"``)
    label               human-readable name (Arabic or English)
    state               current state — EMPTY, OCCUPIED, or BLOCKED
    layer               ontological layer this slot belongs to
    occupant_id         identifier of the first positive occupancy
                        (``None`` while the slot is empty)
    parent_cell         optional :class:`CellType` this slot is attached to
    constraint_token    the :class:`ConditionToken` that gates filling
                        (``None`` if unconstrained)
    notes               free-text annotation
    """

    slot_id: str
    label: str
    state: SlotState
    layer: OntologicalLayer
    occupant_id: Optional[str] = None
    parent_cell: Optional[CellType] = None
    constraint_token: Optional[ConditionToken] = None
    notes: str = ""

    # ── Derived properties ──────────────────────────────────────────

    @property
    def is_fillable(self) -> bool:
        """A1 — the slot is structurally fillable (not blocked)."""
        return self.state is not SlotState.BLOCKED

    @property
    def is_occupied(self) -> bool:
        """A2 — a first positive occupancy has been realised."""
        return self.state is SlotState.OCCUPIED and self.occupant_id is not None

    @property
    def is_zero(self) -> bool:
        """C1 — the slot is empty-but-fillable (≠ ∅)."""
        return self.state is SlotState.EMPTY


# A3 — أصل التمييز الثلاثي

@dataclass(frozen=True)
class TriadicBlockRecord:
    """كتلة ثلاثية — a triadic distinction block (A3).

    Implements the axiom::

        A3. CompleteDistinction(x, y) → ∃t ≠ x, y
            MinimalCompleteDistinction = 3

    And the consequence::

        C3. PairOnly(x, y) → IncompleteRankJudgment

    A ``TriadicBlockRecord`` sits *above* a binary transition (which has
    only ``source`` and ``target``) and adds a third ``apex`` element
    that completes the minimal distinction.

    Fields
    ------
    block_id            unique identifier (e.g. ``"TB_001"``)
    apex                the third, completing element identifier
    left                first element of the base pair
    right               second element of the base pair
    layer               ontological layer of the block
    complete            whether the triadic distinction is satisfied
    governing_transition
                        optional ``Transition_ID`` that this block extends
    notes               free-text annotation
    """

    block_id: str
    apex: str
    left: str
    right: str
    layer: OntologicalLayer
    complete: bool = True
    governing_transition: Optional[str] = None
    notes: str = ""

    # ── Derived properties ──────────────────────────────────────────

    @property
    def members(self) -> Tuple[str, str, str]:
        """Return the ordered triple ``(apex, left, right)``."""
        return (self.apex, self.left, self.right)

    @property
    def is_degenerate(self) -> bool:
        """True if any two members coincide — violating A3."""
        apex, left, right = self.members
        return apex == left or apex == right or left == right


# A4 — أصل الترقية الطبقية

@dataclass(frozen=True)
class LayerPromotionRule:
    """قاعدة الترقية الطبقية — a layer-promotion rule (A4).

    Implements the axiom::

        A4. L_n ≢ L_{n+1}
            Complete(x ∈ L_n) → RequiresHigherContext(x)

    And the consequence::

        C4. Letter → Requires(SyllabicOrHigherContext)

    A ``LayerPromotionRule`` encodes an explicit promotion path from one
    :class:`OntologicalLayer` to the next, together with a
    :class:`ConditionToken` guard and an optional completeness check.

    Fields
    ------
    rule_id             unique identifier (e.g. ``"LP_001"``)
    source_layer        the starting layer
    target_layer        the promoted layer (must be higher)
    condition           :class:`ConditionToken` that gates promotion
    description         human-readable description (Arabic or English)
    requires_completeness
                        whether the source must be complete before promotion
    notes               free-text annotation
    """

    rule_id: str
    source_layer: OntologicalLayer
    target_layer: OntologicalLayer
    condition: ConditionToken
    description: str
    requires_completeness: bool = True
    notes: str = ""

    # ── Derived properties ──────────────────────────────────────────

    @property
    def layer_gap(self) -> int:
        """Number of ontological layers spanned by this promotion."""
        return self.target_layer.value - self.source_layer.value

    @property
    def is_valid(self) -> bool:
        """A4 — target layer must be strictly higher than source."""
        return self.target_layer.value > self.source_layer.value


# ── Structural Slot — الموضع البنيوي الحقيقي ────────────────────────

@dataclass(frozen=True)
class StructuralSlot:
    """الموضع البنيوي الحقيقي — the true structural zero.

    This is **not** a letter, a vowel mark, or a written sukun.  It is a
    position-that-can-be-filled — the ontological precondition for any
    linguistic value to exist.

    Clarifies the distinction::

        ZeroStruct = EmptySlot       (structural possibility)
        Sukun      = ZeroVocalicMark (a specific realisation)

    Implements::

        A1′. StructuralSlot ≠ letter ∧ StructuralSlot ≠ vowel
        Law 1. Slot ≺ Value   (position precedes content)

    Fields
    ------
    slot_id         unique identifier (e.g. ``"SS_001"``)
    label           human-readable name
    layer           ontological layer the slot belongs to
    mode            always ``OntologicalMode.SLOT``
    fillable        whether the slot can currently accept a value
    occupant_id     id of the element occupying the slot (``None`` if empty)
    constraint      optional :class:`ConditionToken` gating occupancy
    notes           free-text annotation
    """

    slot_id: str
    label: str
    layer: OntologicalLayer
    mode: OntologicalMode = OntologicalMode.SLOT
    fillable: bool = True
    occupant_id: Optional[str] = None
    constraint: Optional[ConditionToken] = None
    notes: str = ""

    @property
    def is_empty(self) -> bool:
        """True when the slot has no occupant."""
        return self.occupant_id is None

    @property
    def is_occupied(self) -> bool:
        """True when the slot holds a value."""
        return self.occupant_id is not None


# ── Vocalic Zero — الصفر الحركي المخصوص ─────────────────────────────

@dataclass(frozen=True)
class VocalicZero:
    """الصفر الحركي المخصوص — sukun as a specific vocalic-zero mark.

    The vocalic zero is a *manifestation* (تمظهر) inside the vowel
    layer, **not** the absolute structural zero.  It records the
    absence-of-vowel on a specific consonant slot.

    Clarifies::

        Sukun ≠ ZeroStruct
        Sukun  = 0_V   (a zero *within* the vocalic domain)

    Fields
    ------
    zero_id         unique identifier (e.g. ``"VZ_001"``)
    host_slot_id    the :class:`StructuralSlot` or consonant this zero
                    is attached to
    layer           always CELL (it lives at the phonological cell level)
    mode            always ``OntologicalMode.MODIFIER``
    explicit        whether the sukun is written on the surface
    notes           free-text annotation
    """

    zero_id: str
    host_slot_id: str
    layer: OntologicalLayer = OntologicalLayer.CELL
    mode: OntologicalMode = OntologicalMode.MODIFIER
    explicit: bool = True
    notes: str = ""

    @property
    def is_structural_zero(self) -> bool:
        """Always False — this is a vocalic zero, not a structural one."""
        return False

    @property
    def is_vocalic_zero(self) -> bool:
        """Always True — this is a zero within the vocalic domain."""
        return True


# ── Triad Record — سجل الثلاثية ──────────────────────────────────────

@dataclass(frozen=True)
class TriadRecord:
    """سجل ثلاثي منضبط — a formally typed triadic record.

    Every triad must declare its :class:`TriadType` before entering
    any computation (Law of Triad Type / قانون نوع المثلث).

    Implements::

        Triad = (Members, Type)
        Type ∈ {Distinctive, Hierarchical, Generative}

    And the Minimum Triad Law::

        MinArabicStructure = (Slot, Value, Constraint)

    Fields
    ------
    triad_id        unique identifier (e.g. ``"TD_001"``)
    triad_type      the formal type of this triad
    node_a          first member (slot / apex / base)
    node_b          second member (value / left-branch / motion)
    node_c          third member (constraint / right-branch / constraint)
    layer           ontological layer
    decision_rule   optional decision function identifier
    notes           free-text annotation
    """

    triad_id: str
    triad_type: TriadType
    node_a: str
    node_b: str
    node_c: str
    layer: OntologicalLayer = OntologicalLayer.CELL
    decision_rule: Optional[str] = None
    notes: str = ""

    @property
    def members(self) -> Tuple[str, str, str]:
        """Return the ordered triple ``(node_a, node_b, node_c)``."""
        return (self.node_a, self.node_b, self.node_c)

    @property
    def is_degenerate(self) -> bool:
        """True if any two members coincide — violating the triad law."""
        a, b, c = self.members
        return a == b or a == c or b == c

    @property
    def has_decision_rule(self) -> bool:
        """True when a decision function is attached (Law 2)."""
        return self.decision_rule is not None


# ── Rank Decision — قرار الرتبة ──────────────────────────────────────

@dataclass(frozen=True)
class RankDecision:
    """قرار الرتبة — the limit/capacity rank decision for an element.

    Implements Law 3 (قانون الحد والسعة)::

        L(x) = LimitScore,  C(x) = CapacityScore
        L ≫ C → LIMITAL
        C ≫ L → CAPACITIVE
        L ≈ C → TRANSITIONAL

    And Law 4 (قانون القيد السابق على التفسير)::

        Ω(x) = 0 → NoInterpretation(x)

    Fields
    ------
    decision_id         unique identifier (e.g. ``"RD_001"``)
    element_id          the element this decision is about
    limit_score         حدّية — how much the element acts as a boundary
    capacity_score      سعة — how much the element acts as a container
    rank_type           derived :class:`RankType`
    omega               constraint weight (Ω) — 0 means no interpretation
    promotion_target    optional next-layer target for promotion (Law 5)
    notes               free-text annotation
    """

    decision_id: str
    element_id: str
    limit_score: float
    capacity_score: float
    rank_type: RankType
    omega: float = 1.0
    promotion_target: Optional[OntologicalLayer] = None
    notes: str = ""

    @property
    def is_limital(self) -> bool:
        """True when limit dominates capacity."""
        return self.rank_type is RankType.LIMITAL

    @property
    def is_capacitive(self) -> bool:
        """True when capacity dominates limit."""
        return self.rank_type is RankType.CAPACITIVE

    @property
    def is_transitional(self) -> bool:
        """True when limit and capacity are balanced."""
        return self.rank_type is RankType.TRANSITIONAL

    @property
    def has_interpretation(self) -> bool:
        """Law 4 — Ω(x) = 0 → no interpretation possible."""
        return self.omega != 0.0

    @property
    def requires_promotion(self) -> bool:
        """Law 5 — whether a promotion target is specified."""
        return self.promotion_target is not None


# ── Axiom & Theorem Records — السجلات البرهانية ──────────────────────

@dataclass(frozen=True)
class AxiomRecord:
    """سجل بديهية — a formally registered axiom of the system.

    Each axiom is a foundational statement that is *assumed* true and
    upon which theorems depend.  Recording axioms as typed objects
    allows:

    * lookup by identifier
    * dependency tracking
    * proof-coverage analysis

    Implements the requirement::

        ∀ axiom ∈ Foundation:
            axiom.id ∈ Registry
            axiom.formal_statement is well-formed
            axiom.implemented_by ⊆ Codebase

    Fields
    ------
    axiom_id            unique identifier (e.g. ``"AX_001"``)
    name                human-readable name (Arabic or English)
    formal_statement    the symbolic / logical statement
    natural_language    plain-language description
    layer               the :class:`OntologicalLayer` this axiom governs
    dependencies        IDs of prior axioms this one depends on
    implemented_by      names of types/functions that embody this axiom
    status              current :class:`ProofStatus`
    notes               free-text annotation
    """

    axiom_id: str
    name: str
    formal_statement: str
    natural_language: str
    layer: OntologicalLayer
    dependencies: Tuple[str, ...] = ()
    implemented_by: Tuple[str, ...] = ()
    status: ProofStatus = ProofStatus.ASSUMED
    notes: str = ""


@dataclass(frozen=True)
class TheoremRecord:
    """سجل مبرهنة — a formally registered theorem derived from axioms.

    A theorem is a statement *derived* from one or more axioms (and
    possibly other theorems).  Recording them as typed objects enables
    traceability from any claim back to its foundational assumptions.

    Implements the requirement::

        ∀ thm ∈ Theorems:
            thm.axiom_deps ⊆ Axioms
            thm.theorem_deps ⊆ Theorems
            thm.proof_sketch ≠ ""

    Fields
    ------
    theorem_id          unique identifier (e.g. ``"TH_001"``)
    name                human-readable name
    formal_statement    the symbolic / logical statement
    natural_language    plain-language description
    axiom_dependencies  IDs of axioms this theorem depends on
    theorem_dependencies IDs of prior theorems this theorem depends on
    proof_sketch        concise proof outline
    status              current :class:`ProofStatus`
    test_reference      name of the test that verifies this theorem
    notes               free-text annotation
    """

    theorem_id: str
    name: str
    formal_statement: str
    natural_language: str
    axiom_dependencies: Tuple[str, ...] = ()
    theorem_dependencies: Tuple[str, ...] = ()
    proof_sketch: str = ""
    status: ProofStatus = ProofStatus.PENDING
    test_reference: str = ""
    notes: str = ""

    @property
    def all_dependencies(self) -> Tuple[str, ...]:
        """Return all dependency IDs (axiom + theorem)."""
        return self.axiom_dependencies + self.theorem_dependencies

    @property
    def is_proven(self) -> bool:
        """True when the theorem has been formally proven."""
        return self.status is ProofStatus.PROVEN


@dataclass(frozen=True)
class ProofDependencyGraph:
    """رسم بياني للاعتماد البرهاني — the proof-dependency DAG.

    Collects all :class:`AxiomRecord` and :class:`TheoremRecord` instances
    and provides navigation / validation helpers.

    Key invariants::

        1. The graph must be acyclic (is_acyclic)
        2. Every theorem dependency must reference existing axioms/theorems
        3. proof_coverage ∈ [0, 1]

    Fields
    ------
    axioms      all registered axioms
    theorems    all registered theorems
    """

    axioms: Tuple[AxiomRecord, ...]
    theorems: Tuple[TheoremRecord, ...]

    # ── Lookup ─────────────────────────────────────────────────────

    def get_axiom(self, axiom_id: str) -> Optional[AxiomRecord]:
        """Return the axiom with the given ID, or ``None``."""
        for ax in self.axioms:
            if ax.axiom_id == axiom_id:
                return ax
        return None

    def get_theorem(self, theorem_id: str) -> Optional[TheoremRecord]:
        """Return the theorem with the given ID, or ``None``."""
        for th in self.theorems:
            if th.theorem_id == theorem_id:
                return th
        return None

    # ── Dependency queries ─────────────────────────────────────────

    def dependencies_of(self, theorem_id: str) -> Tuple[str, ...]:
        """Return all dependency IDs for a theorem (axiom + theorem)."""
        th = self.get_theorem(theorem_id)
        if th is None:
            return ()
        return th.all_dependencies

    def dependents_of(self, axiom_id: str) -> Tuple[str, ...]:
        """Return IDs of all theorems that depend on the given axiom."""
        return tuple(
            th.theorem_id
            for th in self.theorems
            if axiom_id in th.axiom_dependencies
        )

    # ── Structural validation ──────────────────────────────────────

    def _all_ids(self) -> "frozenset[str]":
        """Return all axiom and theorem IDs."""
        ax_ids = frozenset(ax.axiom_id for ax in self.axioms)
        th_ids = frozenset(th.theorem_id for th in self.theorems)
        return ax_ids | th_ids

    def dangling_dependencies(self) -> Tuple[str, ...]:
        """Return dependency IDs that don't match any axiom or theorem."""
        known = self._all_ids()
        dangling: "list[str]" = []
        for th in self.theorems:
            for dep in th.all_dependencies:
                if dep not in known:
                    dangling.append(dep)
        return tuple(sorted(set(dangling)))

    def is_acyclic(self) -> bool:
        """Return ``True`` if the theorem dependency graph is a DAG.

        Uses iterative topological-sort (Kahn's algorithm) restricted
        to theorem-to-theorem edges.
        """
        th_ids = [th.theorem_id for th in self.theorems]
        adj: "dict[str, list[str]]" = {tid: [] for tid in th_ids}
        in_deg: "dict[str, int]" = {tid: 0 for tid in th_ids}
        for th in self.theorems:
            for dep in th.theorem_dependencies:
                if dep in adj:
                    adj[dep].append(th.theorem_id)
                    in_deg[th.theorem_id] += 1

        queue = [tid for tid, d in in_deg.items() if d == 0]
        visited = 0
        while queue:
            node = queue.pop(0)
            visited += 1
            for child in adj[node]:
                in_deg[child] -= 1
                if in_deg[child] == 0:
                    queue.append(child)
        return visited == len(th_ids)

    def proof_coverage(self) -> float:
        """Fraction of theorems whose status is PROVEN.

        Returns 0.0 when there are no theorems.
        """
        if not self.theorems:
            return 0.0
        proven = sum(1 for th in self.theorems if th.is_proven)
        return proven / len(self.theorems)

    def all_proven(self) -> bool:
        """True when every theorem has been proven."""
        return bool(self.theorems) and all(
            th.is_proven for th in self.theorems
        )


# ── Essence / Condition — الجوهر والشرط ──────────────────────────────

@dataclass(frozen=True)
class EssenceConditionPair:
    """ثنائية الجوهر والشرط — separates *what* an element is from the
    constraint that gates its realisation.

    Implements the principle::

        Core(x) = (Slot, Value)
        Cond(x) = Constraint      (شرط تحقق ≠ جزء من الماهية)

    This allows treating the constraint as an *external guard* rather
    than an intrinsic part of the element's essence.

    Fields
    ------
    element_id      identifier of the linguistic element
    slot            the structural position (موضع)
    value           the content occupying the slot (قيمة)
    constraint      optional :class:`ConditionToken` gating realisation
    layer           ontological layer
    notes           free-text annotation
    """

    element_id: str
    slot: str
    value: str
    constraint: Optional[ConditionToken] = None
    layer: OntologicalLayer = OntologicalLayer.CELL
    notes: str = ""

    @property
    def core(self) -> Tuple[str, str]:
        """Return ``(slot, value)`` — the essence, without constraint."""
        return (self.slot, self.value)

    @property
    def has_constraint(self) -> bool:
        """True when a realisation condition is attached."""
        return self.constraint is not None


# ── Linguistic-Zero Coverage types ──────────────────────────────────


@dataclass(frozen=True)
class ZeroCoverageDetail:
    """تفصيل تغطية الصفر — coverage status for a single zero-type axis.

    Fields
    ------
    zero_type   the linguistic-zero axis (Z1–Z20)
    coverage    whether the word covers, partially covers, or misses this axis
    """

    zero_type: LinguisticZeroType
    coverage: ZeroCoverage

    @property
    def zero_code(self) -> str:
        """Return the Z-code string, e.g. ``'Z1'``."""
        return self.zero_type.name

    @property
    def zero_name(self) -> str:
        """Return the Arabic name of this zero axis."""
        return self.zero_type.arabic_name


@dataclass(frozen=True)
class WordZeroCoverageReport:
    """تقرير تغطية الصفر اللغوي — full zero-coverage analysis for one word.

    Fields
    ------
    word        surface form of the word (may be empty string for pure analysis)
    word_class  morpho-semantic class (:class:`WordClass`)
    pattern     morphological pattern string, e.g. ``'فاعل'`` (or ``''``)
    root        tuple of root letters, e.g. ``('ك', 'ت', 'ب')`` (or empty)
    covers      tuple of Z-codes fully covered by this word
    partial     tuple of Z-codes partially covered
    uncovered   tuple of Z-codes not covered at all
    details     one :class:`ZeroCoverageDetail` per axis (Z1–Z20, in order)
    notes       explanatory notes produced during analysis
    """

    word: str
    word_class: WordClass
    pattern: str
    root: Tuple[str, ...]
    covers: Tuple[str, ...]
    partial: Tuple[str, ...]
    uncovered: Tuple[str, ...]
    details: Tuple[ZeroCoverageDetail, ...]
    notes: Tuple[str, ...]
