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
    MafhumType,
    OntologicalLayer,
    PhonCategory,
    PhonFeature,
    PhonGroup,
    PhonTransform,
    ProofStatus,
    ReversibleValue,
    SemanticType,
    SlotState,
    SpaceRef,
    SyllablePosition,
    TimeRef,
    TransitionCondition,
    TransitionLaw,
    TransitionType,
    TruthState,
    UnicodeProfileType,
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
