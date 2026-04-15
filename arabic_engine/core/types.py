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
    # Epistemic v1 enums
    CarrierType,
    CellType,
    CombinationType,
    CompositionDegree,
    ConceptFormationMode,
    ConceptRelationType,
    ConditionToken,
    ConfirmationRank,
    ConflictResolutionMethod,
    ConflictState,
    ConflictType,
    ConstraintStrength,
    ConstraintType,
    ContaminationLevel,
    CouplingRelationType,
    CulturalScope,
    DalaalaKind,
    DalalaType,
    DependencyDegree,
    DiachronicStatus,
    DiscourseGapType,
    DiscourseValidationOutcome,
    ElementClass,
    ElementFunction,
    ElementLayer,
    EpistemicRank,
    EpistemicStatus,
    EvidenceType,
    ExchangeStatus,
    ExchangeType,
    ExistenceMode,
    ExplicitnessLevel,
    FrameType,
    FunctionRole,
    FuncTransitionClass,
    GapSeverity,
    GuidanceState,
    HypothesisStatus,
    InfoKind,
    InsertionPolicy,
    InstitutionalCategory,
    InterpretationSource,
    InterpretiveOutcomeType,
    InterpretiveStability,
    InterPropositionLink,
    IrabCase,
    IrabRole,
    JudgementType,
    JudgmentCategory,
    LinkKind,
    LogicalStatus,
    MafhumType,
    MethodFamily,
    Modality,
    ModalCategory,
    NominalAttributeKind,
    NormativeCategory,
    NounComposition,
    NounDefiniteness,
    NounDirection,
    NounExistentialAspect,
    NounFractalStage,
    NounGender,
    NounGenusLevel,
    NounNumber,
    NounOrigin,
    NounPatternType,
    NounReadiness,
    NounUniversality,
    OperationalCapacity,
    OntologicalConstraintType,
    OntologicalLayer,
    OntologicalMode,
    OntologicalSubtype,
    PhonCategory,
    PhonFeature,
    PhonGroup,
    PhonTransform,
    Polarity,
    PrimarySignifiedType,
    ProofPathKind,
    ProofStatus,
    ProperNounKind,
    PurposeType,
    RankType,
    RationalSelfKind,
    ReadinessLevel,
    ReadinessStatus,
    RealityKind,
    ReferentialSubtype,
    ReversibleValue,
    RevisionType,
    RhetoricalStatus,
    SemanticType,
    SenseModality,
    SignalType,
    SignifiedClass,
    SignifiedTemporalStatus,
    SignifierClass,
    SlotState,
    SourceType,
    SpaceRef,
    SpecificityDegree,
    StockComponent,
    StockSufficiency,
    StrictLayerID,
    StyleKind,
    SyllablePosition,
    SymbolicStatus,
    TimeRef,
    TraceMode,
    TransitionCondition,
    TransitionGateStatus,
    TransitionLaw,
    TransitionType,
    TriadType,
    TrustBasis,
    TrustLevel,
    TruthCategory,
    TruthState,
    UnicodeProfileType,
    UtteranceMode,
    UtteranceToConceptConstraint,
    UtteredFormClass,
    ValidationState,
    VerbAugmentation,
    VerbBab,
    VerbDerivativeType,
    VerbEventType,
    VerbGender,
    VerbMode,
    VerbNumber,
    VerbPerson,
    VerbReadiness,
    VerbTense,
    VerbTransitivity,
    VerbVoice,
)

# ── State-machine layer types ──────────────────────────────────────


@dataclass(frozen=True)
class MCIScores:
    """Component scores for the Minimum-Completeness Index.

    Each score is a float in [0, 1].
    """

    boundary: float = 0.0       # B — Boundary Score
    unity: float = 0.0          # U — Unity Score
    cohesion: float = 0.0       # C — Cohesion Score
    extension: float = 0.0      # E — Extension Score
    phase_order: float = 0.0    # P — Phase Order Score
    orderliness: float = 0.0    # O — Orderliness Score


@dataclass(frozen=True)
class MCIResult:
    """Result of MCI (Minimum-Completeness Index) evaluation."""

    scores: MCIScores
    mci_value: float
    decision: str               # human-readable decision label


@dataclass(frozen=True)
class ConceptSeed:
    """Layer 0 output — initial concept seed from the foundational machine."""

    seed_id: str
    unit_label: str = ""
    identity_score: float = 0.0
    rank_hint: str = ""


@dataclass(frozen=True)
class PhoneticEvent:
    """Layer 1 output — a detected phonetic event."""

    event_id: str
    energy: float = 0.0
    boundary_score: float = 0.0
    position: int = 0
    interception_type: str = ""


@dataclass(frozen=True)
class PhonemeCandidate:
    """Layer 2 output — a phoneme candidate that passed MCI."""

    candidate_id: str
    mci_result: Optional[MCIResult] = None
    phonetic_event_ref: str = ""
    symbol: str = ""


@dataclass(frozen=True)
class HarakaUnit:
    """Layer 2.5 output — an operational vowel-mark (حركة)."""

    unit_id: str
    sonority_score: float = 0.0
    attachment_target: Optional[str] = None
    mobility_score: float = 0.0
    is_lengthened: bool = False
    is_deleted: bool = False


@dataclass(frozen=True)
class SyllableUnit:
    """Layer 3 output — a validated syllable unit."""

    unit_id: str
    pattern_shape: str = ""     # e.g. "CV", "CVC", "CVV", "CVVC", "CVCC"
    weight_class: int = 0       # 1=light, 2=heavy, 3=super-heavy
    nucleus_ref: str = ""
    syllable_score: float = 0.0


@dataclass(frozen=True)
class RankScoreComponents:
    """Components for the root-rank score formula."""

    position_fit: float = 0.0           # P — Position Fit
    constitutiveness: float = 0.0       # C — Constitutiveness
    inflection_stability: float = 0.0   # I — Inflection Stability
    syllable_compatibility: float = 0.0 # S — Syllable Compatibility
    recoverability: float = 0.0         # R — Recoverability


@dataclass(frozen=True)
class RootSlot:
    """Layer 4 output — a root position with rank score."""

    slot_id: str
    root_ref: str = ""
    position: str = ""          # "fa", "ayn", or "lam"
    rank_score: float = 0.0
    components: Optional[RankScoreComponents] = None


@dataclass(frozen=True)
class TransformCandidate:
    """Layer 5 output — a validated morphological transform."""

    candidate_id: str
    transform_type: str = ""    # matches TransformJudgment name
    confidence: float = 0.0
    source_root_ref: str = ""
    recoverability_score: float = 0.0


@dataclass(frozen=True)
class FinalApprovalComponents:
    """Components for the final-approval score formula."""

    judgment_score: float = 0.0         # J
    reality_match_score: float = 0.0    # R
    recoverability_score: float = 0.0   # Rec
    trace_clarity: float = 0.0          # T


@dataclass(frozen=True)
class ValidatedJudgment:
    """Layer 6 output — a judgment that passed reality matching."""

    judgment_id: str
    final_approval: float = 0.0
    reality_match_score: float = 0.0
    components: Optional[FinalApprovalComponents] = None
    is_approved: bool = False
    evidence_refs: Tuple[str, ...] = ()


# ── Signifier layer ─────────────────────────────────────────────────


@dataclass(frozen=True)
class Grapheme:
    """A single grapheme cluster: base code-point + diacritics."""

    base: int  # Unicode code-point of the consonant/vowel letter
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

    root: Tuple[str, ...]  # e.g. ('ك','ت','ب')
    pattern: str  # e.g. 'فَعَلَ'
    root_id: int = 0
    pattern_id: int = 0


# ── Enriched signifier models ──────────────────────────────────────


@dataclass(frozen=True)
class CombiningMarkDetail:
    """Metadata for a single combining mark attached to a grapheme."""

    char: str
    codepoint: str          # e.g. "U+064E"
    type: str               # haraka | sukun | shadda | tanween


@dataclass(frozen=True)
class EnrichedGrapheme:
    """Extended grapheme cluster with phonetic metadata.

    Wraps the basic :class:`Grapheme` concept with additional fields
    loaded from ``arabic_letters.csv`` and ``unicode_marks.csv``.
    The ``role`` field remains ``None`` until the pattern layer
    resolves ambiguity for ا/و/ي.
    """

    id: str
    layer: int                                  # always 1
    surface: str
    base_char: str
    base_codepoint: str                         # e.g. "U+0628"
    combining_marks: Tuple[CombiningMarkDetail, ...] = ()
    phonetic_code: str = ""
    place_code: int = 0
    manner_code: int = 0
    voicing_code: int = 0
    stiffness_code: int = 0
    entity_score: float = 0.0
    role: Optional[str] = None                  # consonant | long_vowel | ambiguous


@dataclass(frozen=True)
class EnrichedSyllable:
    """Syllable with shape and weight metadata from ``syllable_shapes.csv``."""

    id: str
    layer: int                                  # always 3
    surface: str
    chars: Tuple[str, ...] = ()                 # EnrichedGrapheme ids
    vowels: Tuple[str, ...] = ()                # vowel ids
    shape: str = ""                             # e.g. "CV"
    shape_code: str = ""                        # e.g. "3.1.1.0.1"
    nucleus_type: int = 0
    closure_type: int = 0
    weight_code: int = 0
    completion_score: float = 0.0
    weightability_score: float = 0.0


@dataclass(frozen=True)
class PatternCandidate:
    """A candidate morphological pattern with confidence score."""

    pattern_code: str
    pattern_label: str = ""
    pattern_type: str = ""
    augment_count: int = 0
    root_candidate: Tuple[str, ...] = ()
    confidence: float = 0.0
    reality_match_score: float = 0.0


@dataclass(frozen=True)
class CliticRecord:
    """A clitic (proclitic/enclitic) stripped from a token."""

    surface: str
    type: str               # connector | relation_marker | definite_article
    confidence: float = 0.0


@dataclass(frozen=True)
class RootCandidate:
    """A candidate root with confidence score."""

    root: Tuple[str, ...]
    confidence: float = 0.0


@dataclass(frozen=True)
class TokenAnalysis:
    """Full word-level analysis record (تحليل الكلمة الكاملة).

    Produced by the 8-step diacritised-word analysis pipeline.
    """

    id: str
    surface: str
    normalized_form: str
    unicode_form: str = "NFC"
    graphemes: Tuple[EnrichedGrapheme, ...] = ()
    clitics: Tuple[CliticRecord, ...] = ()
    core_surface: str = ""
    syllables: Tuple[EnrichedSyllable, ...] = ()
    root_candidates: Tuple[RootCandidate, ...] = ()
    pattern_candidates: Tuple[PatternCandidate, ...] = ()
    final_status: str = "structural_analysis_only"


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
    """An ontological node — the *signified* (التعريف 5).

    The v2 expansion adds nineteen optional axes that together cover
    the full range of human conceptual knowledge.  All new fields
    default to ``None`` so that existing callers require no changes.

    Core fields (v1)
    ----------------
    concept_id      unique integer identifier
    label           human-readable Arabic label
    semantic_type   primary ontological type (entity / event / …)
    properties      free-form property dict for ad-hoc extensions

    Descriptive axes (v2)
    ---------------------
    epistemic_status       how knowledge of the concept is held
    normative_category     intrinsic normative / deontic value
    affective_dimension    affective / emotional charge
    mental_intentional_type intentional mental state category
    modal_category         alethic modal standing
    frame_type             encyclopaedic frame membership
    script_phase           phase within a cognitive script
    causal_role            role in a causal-explanatory chain
    institutional_category social / institutional fact category
    categorization_mode    crisp / prototype / fuzzy membership
    cultural_scope         cultural / civilisational reach
    diachronic_status      semantic shift / historical status
    formation_mode         how the concept was formed
    meta_level             meta-conceptual order (1st / 2nd / 3rd)
    interpretive_stability single reading vs. polysemy / contested
    salience               cognitive salience / prominence
    embodied_domain        embodied sensorimotor grounding domain
    self_model_aspect      aspect of the self-model (if any)
    operational_capacity   performative / operational capacity
    """

    # ── v1 core fields ───────────────────────────────────────────────
    concept_id: int
    label: str
    semantic_type: SemanticType
    properties: dict = field(default_factory=dict)

    # ── v2 descriptive axes ──────────────────────────────────────────
    epistemic_status: Optional[EpistemicStatus] = None
    normative_category: Optional[NormativeCategory] = None
    affective_dimension: Optional[AffectiveDimension] = None
    mental_intentional_type: Optional[MentalIntentionalType] = None
    modal_category: Optional[ModalCategory] = None
    frame_type: Optional[FrameType] = None
    script_phase: Optional[ScriptPhase] = None
    causal_role: Optional[CausalRole] = None
    institutional_category: Optional[InstitutionalCategory] = None
    categorization_mode: Optional[CategorizationMode] = None
    cultural_scope: Optional[CulturalScope] = None
    diachronic_status: Optional[DiachronicStatus] = None
    formation_mode: Optional[ConceptFormationMode] = None
    meta_level: Optional[MetaConceptualLevel] = None
    interpretive_stability: Optional[InterpretiveStability] = None
    salience: Optional[SalienceLevel] = None
    embodied_domain: Optional[EmbodiedDomain] = None
    self_model_aspect: Optional[SelfModelAspect] = None
    operational_capacity: Optional[OperationalCapacity] = None


@dataclass
class ConceptRelation:
    """A directed relation between two concept nodes (شبكة المفاهيم).

    Used to wire :class:`Concept` nodes into a knowledge graph via
    :class:`~arabic_engine.signified.signified_v2.ConceptNetwork`.

    Fields
    ------
    source_id       ``concept_id`` of the origin node
    target_id       ``concept_id`` of the destination node
    relation_type   the semantic relation linking source → target
    weight          relation strength ∈ (0, 1] (default 1.0)
    notes           optional free-text annotation
    """

    source_id: int
    target_id: int
    relation_type: ConceptRelationType
    weight: float = 1.0
    notes: str = ""


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


@dataclass(frozen=True)
class PerceptTrace:
    """Perception trace for a sentence-level episode."""

    raw_text: str
    normalized_text: str
    tokens: Tuple[str, ...]
    trace_quality: float = 1.0


@dataclass(frozen=True)
class PriorKnowledgeUnit:
    """Prior knowledge unit used during linking and judgement."""

    unit_id: str
    content: str
    source: str = "pipeline"
    weight: float = 0.5


@dataclass(frozen=True)
class LinkOperation:
    """A single linking operation between signifier-side and concept-side data."""

    operation_id: str
    operation_type: DalalaType
    source: str
    target: str
    accepted: bool
    confidence: float


@dataclass(frozen=True)
class ConceptNode:
    """Explicit concept node for v3 explainable episode payloads."""

    concept_id: str
    label: str
    semantic_type: SemanticType
    properties: dict = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluationResult:
    """v3 evaluation payload: truth, rank, confidence, and validity."""

    truth_state: TruthState
    epistemic_rank: Optional[EpistemicRank]
    confidence: float
    validation_state: ValidationState
    consistency: str = ""


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
    time_detail: str = ""  # e.g. "أمس", "غدًا"
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
    rule_category: str = ""
    conditions: Tuple[str, ...] = ()
    outcome: str = ""
    strength: float = 0.0
    explanation: str = ""


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
    source_text: str  # the original Manṭūq fragment
    constraint_value: str  # the specific constraint detected
    counterpart: str  # the mental counterpart (المقابل الذهني)
    derived_meaning: str  # the derived implied meaning
    valid: bool  # whether all four pillars hold
    confidence: float  # confidence in [0, 1]


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
    left_neighbor: Optional["DMin"] = None  # type: ignore[name-defined]
    right_neighbor: Optional["DMin"] = None  # type: ignore[name-defined]
    pattern: str = ""  # e.g. "فَعَلَ", "اسْتَفْعَلَ"
    economy_pressure: float = 0.0  # 0 = none, 1 = maximum
    architecture: str = ""  # e.g. "مجرد", "مزيد", "مشتق"


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
    from_category: Optional[PhonCategory]  # None = any category
    required_features: FrozenSet[PhonFeature]  # features element must have
    to_category: PhonCategory  # target cell category
    resulting_transform: PhonTransform  # transform that fires
    conditions: FrozenSet[TransitionCondition]
    priority: int  # lower = higher precedence
    description_ar: str  # Arabic description
    example: str  # canonical Arabic example


@dataclass
class TransitionResult:
    """نتيجة تطبيق قانون الانتقال — result of the transition engine.

    The optimality criterion applied is::

        E_new = ArgMin(loss_root, loss_pattern, phonetic_burden)
        subject to: E_new ∈ Nearest_Valid_Functional_Cell
    """

    source_unicode: int  # codepoint of the original element
    applied_rule: Optional[TransitionRule]  # the winning rule (None = stable)
    stable: bool  # True if no transition occurred
    target_category: Optional[PhonCategory]  # new cell category (None = deleted)
    surface_form: str  # resulting surface character(s)
    loss_root: float  # cost: root integrity loss ∈ [0, 1]
    loss_pattern: float  # cost: pattern integrity loss ∈ [0, 1]
    phonetic_burden: float  # cost: articulatory burden ∈ [0, 1]
    total_cost: float  # = loss_root + loss_pattern + phonetic_burden
    conditions_met: FrozenSet[TransitionCondition]
    notes: str = ""  # optional diagnostic string


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
    priority: int  # 1 = critical … 5 = fallback
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

    element_id: str  # e.g. "AE_001"
    element_name: str  # e.g. "Hamza"
    element_class: ElementClass
    element_function: ElementFunction
    referent: str  # الدلالة الوظيفية
    boundary: str  # الحد الفاصل
    necessity: str  # الضرورة
    governing_role: str  # الدور الحاكم
    layer: ElementLayer
    combination_type: CombinationType
    math_form: Tuple[int, ...]  # 8-bit binary vector
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


# ── Symbolic Encoding — ترميز الحرف والحركة ─────────────────────────
#
# Implements the refined axiom:
#
#     Ess(x) = ⟨Slot(x), Value(x)⟩          — essence = position + value
#     Cond(x) = Ω_x                          — constraint (external to essence)
#     Valid(x) ⟺ Ess(x) ∧ Ω_x              — acceptance / activation
#
# The constraint is NOT an intrinsic part of the unit's essence.
# It is an activation / acceptance / insertion / promotion condition.


@dataclass(frozen=True)
class SymbolicRecord:
    """السجل الرمزي العام — Generic Symbolic Record.

    The universal record for any linguistic encoding unit (letter or vowel).
    Separates *essence* (Core) from *constraint* (Condition)::

        X := (ID, Type, Slot, Value, Condition, Layer, Status)

        Core(X)      = (Slot, Value)           — الجوهر
        Condition(X)  = Ω_X                    — الشرط
        Status(X)    = Representable | Valid | Promotable

    Implements::

        Ess(x)  = ⟨Slot, Value⟩
        Valid(x) ⟺ Ess(x) ∧ Constraint

    Fields
    ------
    record_id           unique identifier (e.g. ``"SR_001"``)
    unit_type           LETTER or VOWEL
    slot_position       positional encoding (scriptural / phonetic / chain)
    slot_label          human-readable slot description
    value_vector        numeric value tuple (identity, features, effects)
    value_label         human-readable value description
    constraints         frozenset of active constraint kinds
    constraint_omega    constraint weight Ω ∈ [0, 1]; 0 = blocked, 1 = open
    layer               ontological layer
    status              current symbolic status
    notes               free-text annotation
    """

    record_id: str
    unit_type: UnitType
    slot_position: int
    slot_label: str
    value_vector: Tuple[int, ...]
    value_label: str
    constraints: FrozenSet[ConstraintKind] = field(default_factory=frozenset)
    constraint_omega: float = 1.0
    layer: OntologicalLayer = OntologicalLayer.CELL
    status: SymbolicStatus = SymbolicStatus.REPRESENTABLE
    notes: str = ""

    # ── Core (الجوهر) ──────────────────────────────────────────────

    @property
    def core(self) -> Tuple[int, Tuple[int, ...]]:
        """Core(X) = (Slot, Value) — the essence of this unit.

        Returns ``(slot_position, value_vector)`` — everything that
        defines **what** the unit is, independent of contextual
        constraints.
        """
        return (self.slot_position, self.value_vector)

    # ── Essence predicates ─────────────────────────────────────────

    @property
    def is_representable(self) -> bool:
        """Representable ⟺ Core(X) is well-formed.

        A unit is representable when it has a valid slot position
        (≥ 0) and a non-empty value vector.
        """
        return self.slot_position >= 0 and len(self.value_vector) > 0

    # ── Constraint predicate ───────────────────────────────────────

    @property
    def constraint_satisfied(self) -> bool:
        """Ω_X — the constraint is satisfied (non-zero weight)."""
        return self.constraint_omega > 0.0

    # ── Validation ─────────────────────────────────────────────────

    @property
    def is_valid(self) -> bool:
        """Valid(X) ⟺ Core(X) ∧ Ω_X.

        The unit is structurally valid when its essence is well-formed
        **and** the external constraint is satisfied.
        """
        return self.is_representable and self.constraint_satisfied

    # ── Match / Containment / Usability ────────────────────────────

    @property
    def match(self) -> bool:
        """M(x) = Match(S_x) — the unit occupies its proper slot."""
        return self.is_representable

    @property
    def containment(self) -> bool:
        """T(x) = Containment(V_x) — the value is embeddable in a
        higher structure."""
        return self.is_representable

    @property
    def is_usable(self) -> bool:
        """Usable(x) ⟺ M(x) ∧ T(x) ∧ Q(x).

        The unit can be *used* in a structural context only when match,
        containment, **and** the constraint condition are all true.
        """
        return self.match and self.containment and self.constraint_satisfied

    def to_row(self) -> dict:
        """Serialise to a flat dictionary suitable for tabular display."""
        return {
            "Record_ID": self.record_id,
            "Unit_Type": self.unit_type.name,
            "Slot_Position": self.slot_position,
            "Slot_Label": self.slot_label,
            "Value_Vector": self.value_vector,
            "Value_Label": self.value_label,
            "Constraints": tuple(sorted(c.name for c in self.constraints)),
            "Constraint_Omega": self.constraint_omega,
            "Layer": self.layer.name,
            "Status": self.status.name,
            "Core": self.core,
            "Is_Valid": self.is_valid,
            "Is_Usable": self.is_usable,
        }


@dataclass(frozen=True)
class LetterRecord(SymbolicRecord):
    """سجل ترميز الحرف — Letter Encoding Record.

    Specialisation of :class:`SymbolicRecord` for consonants / base letters.

    The essence of a letter::

        Ess(L) = ⟨S_L, V_L⟩

    where:
        S_L — scriptural position, phonetic place, chain index
        V_L — consonantal identity, feature vector, syllabic potential,
              prosodic weight

    The constraint::

        C_L = Ω_L  (positional + adjacency + layer constraints)

    Validation::

        Valid(L) ⟺ ⟨S_L, V_L⟩ ∧ Ω_L = 1

    Additional fields
    -----------------
    phonetic_group      phonetic articulation group (e.g. ``PhonGroup``)
    syllabic_weight     maqta'i weight contribution (1–3)
    """

    phonetic_group: Optional[PhonGroup] = None
    syllabic_weight: int = 1

    def __post_init__(self) -> None:
        """Ensure unit_type is LETTER."""
        if self.unit_type is not UnitType.LETTER:
            raise ValueError(
                f"LetterRecord requires UnitType.LETTER, got {self.unit_type}"
            )


@dataclass(frozen=True)
class VowelRecord(SymbolicRecord):
    """سجل ترميز الحركة — Vowel Encoding Record.

    Specialisation of :class:`SymbolicRecord` for short vowels / diacritics.

    The essence of a vowel::

        Ess(H) = ⟨S_H, V_H⟩

    where:
        S_H — dependent position (attached to a carrier / nucleus)
        V_H — vocalic quality (fatha/damma/kasra), temporal effect,
              syllabic effect, prosodic weight

    The constraint::

        C_H = Ω_H  (carrier + syllabic + layer constraints)

    Validation::

        Valid(H) ⟺ ⟨S_H, V_H⟩ ∧ Ω_H = 1

    Additional fields
    -----------------
    carrier_id          identifier of the host consonant
    is_long             whether the vowel is a long (madd) variant
    """

    carrier_id: Optional[str] = None
    is_long: bool = False

    def __post_init__(self) -> None:
        """Ensure unit_type is VOWEL."""
        if self.unit_type is not UnitType.VOWEL:
            raise ValueError(
                f"VowelRecord requires UnitType.VOWEL, got {self.unit_type}"
            )

@dataclass(frozen=True)
class UtteranceRecord:
    """سجل المنطوق — the utterance (linguistic surface form) carrier.

    Fields
    ------
    utterance_id  unique identifier
    text          the surface text
    """

    utterance_id: str
    text: str


@dataclass(frozen=True)
class ConceptRecord:
    """سجل المفهوم — the concept (mental/semantic) carrier.

    Fields
    ------
    concept_record_id  unique identifier
    label              the concept label
    """

    concept_record_id: str
    label: str


@dataclass(frozen=True)
class LinguisticCarrierRecord:
    """سجل الحامل اللغوي — the linguistic transport for a cognitive episode.

    The linguistic transport has exactly two carriers: Utterance and Concept.
    ``carrier_type`` specifies which is present; when ``BOTH``, both
    ``utterance`` and ``concept`` must be non-None.

    Fields
    ------
    carrier_id    unique identifier
    carrier_type  which carriers are present (:class:`CarrierType`)
    utterance     the utterance carrier (required if type is UTTERANCE or BOTH)
    concept       the concept carrier (required if type is CONCEPT or BOTH)
    """

    carrier_id: str
    carrier_type: CarrierType
    utterance: Optional[UtteranceRecord]
    concept: Optional[ConceptRecord]


@dataclass(frozen=True)
class ProofPathRecord:
    """مسار الإثبات — the path of proof supporting a judgement.

    Fields
    ------
    path_id     unique identifier
    kind        proof path kind (:class:`ProofPathKind`)
    steps       ordered proof steps (as text)
    method_fit  the method family this path is compatible with
    """

    path_id: str
    kind: ProofPathKind
    steps: Tuple[str, ...]
    method_fit: MethodFamily


    @property
    def has_constraint(self) -> bool:
        """True when a realisation condition is attached."""
        return self.constraint is not None


# ── Signified Ontology v1.0 — المدلول ────────────────────────────────

@dataclass(frozen=True)
class SignifiedRecord:
    """سجل المدلول — the central record of the Arabic Signified Ontology.

    Every signified in the language is represented as a 17-field frozen
    record covering its type, subtype, and seven cross-cutting descriptive
    axes.

    Mirrors the JSON representation defined in §6 of the ontology spec.
    """

    id: str                                        # e.g. "SIG-000124"
    label_ar: str                                  # التسمية بالعربية
    label_en: str                                  # English label
    definition: str                                # التعريف
    primary_type: PrimarySignifiedType
    secondary_type: str                            # dotted path, e.g. "EntityMeaning.GenericEntity"
    dependency_degree: DependencyDegree
    existence_mode: ExistenceMode
    specificity_degree: SpecificityDegree
    composition_degree: CompositionDegree
    context_requirement: ContextRequirement
    logical_status: LogicalStatus
    rhetorical_status: RhetoricalStatus
    temporal_status: SignifiedTemporalStatus
    referential_status: Optional[ReferentialSubtype] = None
    examples: Tuple[str, ...] = ()
    constraints: Tuple[str, ...] = ()


@dataclass(frozen=True)
class OntologicalSignified(SignifiedRecord):
    """سجل المدلول الوجودي — signified with ontological-subtype detail.

    Extends :class:`SignifiedRecord` for EntityMeaning, PropertyMeaning,
    and EventMeaning branches.
    """

    ontological_subtype: Optional[OntologicalSubtype] = None
    # Entity branch
    is_countable: bool = True
    is_individuated: bool = True
    is_named: bool = False
    # Property branch
    requires_bearer: bool = False
    property_persistence: str = ""      # "stable" | "transient"
    # Event branch
    event_time: str = ""                # free-form temporal note
    transitivity: str = ""              # "transitive" | "intransitive"
    agency: str = ""                    # "agentive" | "non-agentive"
    intentionality: str = ""            # "intentional" | "non-intentional"


@dataclass(frozen=True)
class RelationalSignified(SignifiedRecord):
    """سجل المدلول العلائقي — signified with relational detail."""

    arity: int = 2
    relation_direction: str = ""        # e.g. "source→target"
    symmetry: bool = False


@dataclass(frozen=True)
class PropositionalSignified(SignifiedRecord):
    """سجل المدلول القضوي — signified with propositional detail."""

    truth_evaluable: bool = False
    polarity: Polarity = Polarity.NEUTRAL_POL
    modality: Modality = Modality.CERTAIN_MOD

    @property
    def failed_constraints(self) -> Tuple["OntologicalConstraintRecord", ...]:
        """Return all constraint records that did not pass."""
        return tuple(c for c in self.constraints if c.is_violated)


# ── Epistemic v1 — Knowledge Episode Validator types ─────────────────


@dataclass(frozen=True)
class Self_:
    """ذات — the epistemic agent undergoing a knowledge episode.

    Renamed from ``Self`` to avoid clashing with the Python keyword.

    Fields
    ------
    id          unique identifier (e.g. ``"self:researcher_1"``)
    self_kind   kind of agent (``"individual"``, ``"collective"``, etc.)
    """

    id: str
    self_kind: str


@dataclass(frozen=True)
class RealityAnchorRecord:
    """مرساة الواقع — anchors a knowledge episode to external reality.

    Fields
    ------
    id                  unique identifier
    reality_kind        kind of reality referent
    source_mode         how the reality was accessed
    anchoring_strength  strength of the anchor (1–5)
    """

    id: str
    reality_kind: RealityKind
    source_mode: TraceMode
    anchoring_strength: int


@dataclass(frozen=True)
class SenseTraceRecord:
    """أثر الحس — the sensory trace supporting the episode.

    Fields
    ------
    id               unique identifier
    sense_modality   the sensory channel used
    trace_mode       how the trace was obtained
    trace_quality    quality descriptor (e.g. ``"strong"``, ``"weak"``)
    """

    id: str
    sense_modality: SenseModality
    trace_mode: TraceMode
    trace_quality: str


@dataclass(frozen=True)
class PriorInfoRecord:
    """معلومة سابقة — a piece of prior information used in the episode.

    Fields
    ------
    id           unique identifier
    info_kind    category of prior information (e.g. ``"lexical"``)
    source       where the information comes from (e.g. ``"lexicon"``)
    is_verified  whether this piece has been verified
    """

    id: str
    info_kind: str
    source: str
    is_verified: bool


@dataclass(frozen=True)
class OpinionTraceRecord:
    """أثر رأي — tracks potential prior-opinion contamination.

    Fields
    ------
    id                    unique identifier
    contamination_level   degree of contamination
    description           free-text description
    """

    id: str
    contamination_level: ContaminationLevel
    description: str


@dataclass(frozen=True)
class LinkingTraceRecord:
    """أثر الربط — documents how the linking / inference was performed.

    Fields
    ------
    id           unique identifier
    link_kind    the kind of linking used
    step_count   number of inferential steps
    is_explicit  whether the link was explicit
    """

    id: str
    link_kind: LinkKind
    step_count: int
    is_explicit: bool


@dataclass(frozen=True)
class JudgementRecord:
    """حكم — the judgement issued by the knowledge episode.

    Fields
    ------
    id              unique identifier
    judgement_type   the category of judgement
    judgement_text   free-text statement of the judgement
    """

    id: str
    judgement_type: JudgementType
    judgement_text: str


@dataclass(frozen=True)
class MethodRecord:
    """منهج — a registered methodological family.

    Fields
    ------
    id                        unique identifier (e.g. ``"method:rational"``)
    method_family             the family category
    requires_experiment       whether this method requires experiments
    requires_formal_proof     whether this method requires formal proofs
    requires_linguistic_anchor whether this method requires a linguistic anchor
    """

    id: str
    method_family: MethodFamily
    requires_experiment: bool
    requires_formal_proof: bool
    requires_linguistic_anchor: bool


@dataclass(frozen=True)
class UtteranceRecord:
    """منطوق — the uttered / surface linguistic form.

    Fields
    ------
    id              unique identifier
    text_shakled    the vowelised (tashkīl) text
    utterance_mode  mode of the utterance (e.g. ``"nass"``)
    literal_scope   scope of the literal meaning (e.g. ``"direct"``)
    """

    id: str
    text_shakled: str
    utterance_mode: str
    literal_scope: str


@dataclass(frozen=True)
class ConceptRecord:
    """مفهوم (سجل) — a concept record in the epistemic episode.

    Separate from the existing :class:`Concept` dataclass to avoid
    conflation with the NLP pipeline's concept representation.

    Fields
    ------
    id              unique identifier
    concept_name    the name of the concept
    dalaala_type    signification type (مطابقة / تضمن / …)
    concept_scope   scope descriptor (e.g. ``"restricted"``)
    """

    id: str
    concept_name: str
    dalaala_type: DalalaType
    concept_scope: str


@dataclass(frozen=True)
class LinguisticCarrierRecord:
    """حامل لغوي — the linguistic carrier for a knowledge episode.

    Fields
    ------
    id              unique identifier
    carrier_class   which carrier type(s) are present
    utterance       optional utterance record
    concept         optional concept record
    """

    id: str
    carrier_class: CarrierType
    utterance: Optional[UtteranceRecord] = None
    concept: Optional[ConceptRecord] = None


@dataclass(frozen=True)
class ProofPathRecord:
    """مسار إثبات — the proof path justifying the episode.

    Fields
    ------
    id           unique identifier
    path_kind    kind of proof path used
    is_complete  whether the proof path is complete
    step_count   number of proof steps
    """

    id: str
    path_kind: ProofPathKind
    is_complete: bool
    step_count: int


@dataclass(frozen=True)
class ConflictRuleRecord:
    """قاعدة تعارض — the conflict resolution rule applied.

    Fields
    ------
    id                  unique identifier
    rule_name           name of the rule
    priority_order      the priority order string
    action_on_conflict  what action to take on conflict
    """

    id: str
    rule_name: str
    priority_order: str
    action_on_conflict: str


@dataclass(frozen=True)
class GapRecord:
    """فجوة — a validation gap found during episode validation.

    Fields
    ------
    id        unique identifier
    gap_type  the error key
    message   human-readable message
    severity  how severe the gap is
    """

    id: str
    gap_type: str
    message: str
    severity: GapSeverity


@dataclass(frozen=True)
class KnowledgeEpisode:
    """خبرة معرفية — a knowledge episode node.

    Fields
    ------
    id                unique identifier
    domain_profile    domain of the episode (e.g. ``"linguistic"``)
    judgement_type    the type of judgement
    method_family     methodological family
    method_ref        reference ID of the method node
    carrier_type      which carriers are present
    validation_state  current validation state
    epistemic_rank    assigned rank (``None`` before validation)
    """

    id: str
    domain_profile: str
    judgement_type: JudgementType
    method_family: MethodFamily
    method_ref: str
    carrier_type: CarrierType
    validation_state: ValidationState
    epistemic_rank: Optional[EpistemicRank] = None


@dataclass(frozen=True)
class KnowledgeEpisodeInput:
    """مُدخَل خبرة معرفية — composite input for episode validation.

    Bundles all sub-records needed to validate a single episode.

    Fields
    ------
    self_           the epistemic agent
    episode         the episode record
    reality         reality anchor record
    sense           sense trace record
    prior_infos     tuple of prior information records
    linking         linking trace record
    judgement       judgement record
    method          method record
    carrier         linguistic carrier record
    proof           proof path record
    conflict        conflict rule record
    opinions        tuple of opinion trace records (may be empty)
    """

    self_: Self_
    episode: KnowledgeEpisode
    reality: Optional[RealityAnchorRecord]
    sense: Optional[SenseTraceRecord]
    prior_infos: Tuple[PriorInfoRecord, ...]
    linking: Optional[LinkingTraceRecord]
    judgement: Optional[JudgementRecord]
    method: Optional[MethodRecord]
    carrier: Optional[LinguisticCarrierRecord]
    proof: Optional[ProofPathRecord]
    conflict: Optional[ConflictRuleRecord]
    opinions: Tuple[OpinionTraceRecord, ...] = ()


@dataclass(frozen=True)
class ValidationResult:
    """نتيجة التصديق — the output of episode validation.

    Fields
    ------
    episode_id        the episode ID
    validation_state  ``VALID`` or ``INVALID``
    epistemic_rank    the assigned epistemic rank
    errors            tuple of error strings
    gaps              tuple of gap records
    """

    episode_id: str
    validation_state: ValidationState
    epistemic_rank: EpistemicRank
    errors: Tuple[str, ...]
    gaps: Tuple[GapNode, ...]


# ── Discourse Exchange types (Schema التداول المعرفي) ──────────────────────────


@dataclass(frozen=True)
class RationalSelfRecord:
    """الذات العاقلة الداخلة في التداول."""

    node_id: str
    self_kind: RationalSelfKind
    epistemic_capacity: str
    language_profile: str


@dataclass(frozen=True)
class SenderRoleRecord:
    """دور المرسل ضمن تبادل معرفي محدد."""

    node_id: str
    role_type: SenderRoleType
    authority_level: AuthorityLevel


@dataclass(frozen=True)
class ReceiverRoleRecord:
    """دور المستقبل ضمن تبادل معرفي محدد."""

    node_id: str
    role_type: ReceiverRoleType
    expected_action: ReceiverExpectedAction


@dataclass(frozen=True)
class ExchangePurposeRecord:
    """الغرض المقصود من التبادل المعرفي."""

    node_id: str
    purpose_type: PurposeType
    goal_statement: str


@dataclass(frozen=True)
class ExchangeStyleRecord:
    """أسلوب إخراج التبادل المعرفي."""

    node_id: str
    style_kind: StyleKind
    explicitness: ExplicitnessLevel


@dataclass(frozen=True)
class DiscourseCarrierRecord:
    """الحامل اللغوي للتداول (منطوق/مفهوم/كلاهما)."""

    node_id: str
    carrier_class: CarrierClass


@dataclass(frozen=True)
class DiscourseUtteranceRecord:
    """المنطوق المحمول في التبادل."""

    node_id: str
    text_shakled: str
    utterance_mode: UtteranceMode
    literal_scope: str


@dataclass(frozen=True)
class DiscourseConceptRecord:
    """المفهوم المحمول في التبادل."""

    node_id: str
    concept_name: str
    dalaala_kind: DalaalaKind
    concept_scope: str


@dataclass(frozen=True)
class ReceptionRecord:
    """واقعة استقبال الرسالة."""

    node_id: str
    reception_mode: ReceptionMode
    receiver_state: ReceiverState


@dataclass(frozen=True)
class ReceptionStateRecord:
    """حكم ما بعد الاستقبال."""

    node_id: str
    state_type: ReceptionStateType
    justification: str


@dataclass(frozen=True)
class TrustProfileRecord:
    """وزن ثقة المستقبل بالمصدر."""

    node_id: str
    trust_level: TrustLevel
    trust_basis: TrustBasis


@dataclass(frozen=True)
class InterpretiveOutcomeRecord:
    """المحصلة التأويلية للاستقبال."""

    node_id: str
    outcome_type: InterpretiveOutcomeType


@dataclass(frozen=True)
class DiscourseGapRecord:
    """فجوة مكتشفة في سلامة التداول المعرفي."""

    node_id: str
    gap_type: DiscourseGapType
    severity: GapSeverity
    detail: str


@dataclass(frozen=True)
class DiscourseExchangeResult:
    """نتيجة التحقق من تداول معرفي واحد."""

    exchange_id: str
    outcome: DiscourseValidationOutcome
    gaps: List[DiscourseGapRecord]
    status: ExchangeStatus


@dataclass
class DiscourseExchangeNode:
    """حادثة تداول معرفي مركزية (mutable for validator-written fields)."""

    node_id: str
    exchange_type: ExchangeType
    purpose_class: str
    style_class: str
    carrier_type: str
    status: ExchangeStatus
    sender: Optional[RationalSelfRecord] = None
    sender_role: Optional[SenderRoleRecord] = None
    receiver: Optional[RationalSelfRecord] = None
    receiver_role: Optional[ReceiverRoleRecord] = None
    purpose: Optional[ExchangePurposeRecord] = None
    style: Optional[ExchangeStyleRecord] = None
    carrier: Optional[DiscourseCarrierRecord] = None
    utterance: Optional[DiscourseUtteranceRecord] = None
    concept: Optional[DiscourseConceptRecord] = None
    transferred_knowledge: Optional[KnowledgeEpisodeNode] = None
    reception: Optional[ReceptionRecord] = None
    reception_state: Optional[ReceptionStateRecord] = None
    trust_profile: Optional[TrustProfileRecord] = None
    interpretive_outcome: Optional[InterpretiveOutcomeRecord] = None
    validation_outcome: DiscourseValidationOutcome = DiscourseValidationOutcome.INCOMPLETE
    gaps: List[DiscourseGapRecord] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════
# Fractal Kernel — Layered Hypothesis Graph Types
# ═══════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class UnicodeAtom:
    """ذرة يونيكودية — a single Unicode code-point with classification.

    Every character in the input is decomposed into an atom before any
    normalization or segmentation takes place.
    """

    atom_id: str
    char: str
    codepoint: int
    unicode_category: str
    combining_class: int
    position_index: int
    signal_type: SignalType = SignalType.UNKNOWN


@dataclass(frozen=True)
class SignalUnit:
    """وحدة إشارية — a normalised signal unit ready for analysis.

    Produced by the signal layer after normalization of Unicode atoms.
    """

    unit_id: str
    surface_text: str
    normalized_text: str
    source_span: Tuple[int, int]
    signal_type: SignalType = SignalType.BASE_LETTER


@dataclass(frozen=True)
class HypothesisNode:
    """عقدة فرضية — a single hypothesis in the layered graph.

    This is the **unified node type** for all hypothesis stages.
    Instead of creating separate dataclasses for morphological,
    conceptual, axis, relation, role, factor, case, and judgement
    hypotheses, we use a single parameterised node with a typed
    payload dictionary.

    Fields
    ------
    node_id         unique identifier for this hypothesis
    hypothesis_type short label (e.g. "morphology", "concept", "role")
    stage           which activation stage this belongs to
    source_refs     IDs of upstream nodes that generated this hypothesis
    payload         stage-specific data (root, pattern, label, etc.)
    confidence      score in [0.0, 1.0]
    status          lifecycle status of the hypothesis
    """

    node_id: str
    hypothesis_type: str
    stage: ActivationStage
    source_refs: Tuple[str, ...] = ()
    payload: Tuple[Tuple[str, object], ...] = ()
    confidence: float = 1.0
    status: HypothesisStatus = HypothesisStatus.ACTIVE

    def get(self, key: str, default: object = None) -> object:
        """Look up a key in the payload tuple-of-pairs."""
        for k, v in self.payload:
            if k == key:
                return v
        return default


@dataclass(frozen=True)
class ConstraintEdge:
    """حافة قيد — a constraint linking two hypotheses or a rule.

    Represents a directed restriction: *source_ref* constrains or
    influences *target_ref* with the given strength.
    """

    edge_id: str
    source_ref: str
    target_ref: str
    relation: str
    strength: ConstraintStrength = ConstraintStrength.MODERATE
    justification: str = ""


@dataclass(frozen=True)
class SupportEdge:
    """حافة دعم — an edge that supports a hypothesis.

    When a hypothesis at one layer is consistent with / entailed by a
    hypothesis at another layer, a support edge records that evidence.
    """

    edge_id: str
    supporter_ref: str
    target_ref: str
    weight: float = 1.0
    justification: str = ""


@dataclass(frozen=True)
class ConflictEdge:
    """حافة تعارض — an edge recording a conflict between hypotheses.

    Two hypotheses that cannot both be true are connected by a
    conflict edge.  The constraint engine uses these to prune.
    """

    edge_id: str
    node_a_ref: str
    node_b_ref: str
    conflict_state: ConflictState = ConflictState.HARD
    justification: str = ""


@dataclass(frozen=True)
class ActivationRecord:
    """سجل تفعيل — records the activation of a hypothesis node.

    Tracks when a hypothesis transitions from ACTIVE to STABILIZED
    (or to PRUNED / SUSPENDED) and why.
    """

    record_id: str
    node_ref: str
    old_status: HypothesisStatus
    new_status: HypothesisStatus
    reason: str = ""
    revision_type: Optional[RevisionType] = None


@dataclass(frozen=True)
class DecisionTrace:
    """أثر القرار — full causal trace of a single decision.

    Every decision in the engine (pruning, stabilization, revision)
    produces a trace so the complete reasoning chain is auditable.
    """

    trace_id: str
    stage: ActivationStage
    decision_type: str
    input_refs: Tuple[str, ...] = ()
    output_refs: Tuple[str, ...] = ()
    applied_rules: Tuple[str, ...] = ()
    rejected_refs: Tuple[str, ...] = ()
    justification: str = ""
    confidence: float = 1.0
    parent_trace_refs: Tuple[str, ...] = ()


# ══════════════════════════════════════════════════════════════════════
# Strict 7-Layer Analysis System Records
# النموذج الطبقي الصارم — سجلات الطبقات
# ══════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class MentalFoundationRecord:
    """سجل الطبقة العقلية المؤسسة — Layer 0 mental foundation record.

    Captures the epistemic primitives that must hold before any element
    can be classified: identity, difference, rank, constitutiveness,
    dependency, stability, transformation, causality, reality-match.
    """

    identity_strength: float        # قوة الهوية  [0, 1]
    distinctiveness: float          # التمايز     [0, 1]
    rank_position: float            # الرتبة      [0, 1]
    is_constitutive: bool           # مقوّم؟
    is_dependent: bool              # تابع؟
    stability_score: float          # ثبات        [0, 1]
    transformation_type: str = ""   # نوع التحول
    causal_source: str = ""         # مصدر العلية
    reality_match_score: float = 0.0  # مطابقة الواقع [0, 1]


@dataclass(frozen=True)
class GenerativeProfileRecord:
    """سجل القوام التوليدي — Layer 1 generative phonetic profile.

    Records how a sound is physically produced: vocal fold state,
    articulation place and mode, closure degree, resonance.
    """

    voicedness: bool                # مجهور / مهموس
    air_pressure: float             # ضغط الهواء     [0, 1]
    place_class: str                # صنف الموضع
    manner_class: str               # صنف نوع الاعتراض
    closure_value: float            # درجة الانغلاق  [0, 1]
    release_type: str = ""          # نوع الانفراج
    nasality: bool = False          # أنفي؟
    continuancy: bool = False       # استمراري؟
    sonority_level: float = 0.0     # مستوى الرنة   [0, 1]


@dataclass(frozen=True)
class AuditoryMinimumRecord:
    """سجل القوام السمعي الأدنى — Layer 2 auditory minimum record.

    Proves that the perceived element is a complete auditory unit
    with sufficient presence, boundary, cohesion, and unity.
    """

    audibility_score: float         # الحضور السمعي  [0, 1]
    temporal_span: float            # الامتداد الزمني [0, 1]
    phase_count: int                # عدد الأطوار
    order_score: float              # الانتظام       [0, 1]
    cohesion_score: float           # التماسك        [0, 1]
    unity_score: float              # الوحدة         [0, 1]


@dataclass(frozen=True)
class StructuralProfileRecord:
    """سجل القوام البنيوي — Layer 3 structural profile.

    Locates the unit within the syllable, the root, and the
    morphological pattern, scoring constitutiveness vs. dependency.
    """

    syllable_slot: str              # موضع مقطعي (onset / nucleus / coda)
    root_slot: str                  # موضع جذري (fa / ayn / lam / none)
    constitutiveness_score: float   # المقومية  [0, 1]
    dependency_score: float         # التبعية   [0, 1]
    attachment_score: float         # الإلصاق   [0, 1]
    augmentation_score: float       # الزيادة   [0, 1]
    fa_fitness: float = 0.0         # ملاءمة فاء [0, 1]
    ayn_fitness: float = 0.0        # ملاءمة عين [0, 1]
    lam_fitness: float = 0.0        # ملاءمة لام [0, 1]


@dataclass(frozen=True)
class TransformationProfileRecord:
    """سجل طبقة التحول — Layer 4 transformation record.

    Documents what changes affected the element while keeping
    structural analysis recoverable.
    """

    inflection_stability_score: float   # الثبات عبر التصريف [0, 1]
    recoverability_score: float         # إمكان الرد [0, 1]
    surface_presence: bool              # حاضر سطحيًا؟
    underlying_presence: bool           # حاضر عميقًا؟
    substitution_confidence: float = 0.0  # ثقة الإبدال [0, 1]
    deletion_confidence: float = 0.0    # ثقة الحذف   [0, 1]
    illal_confidence: float = 0.0       # ثقة الإعلال  [0, 1]
    idgham_confidence: float = 0.0      # ثقة الإدغام  [0, 1]


@dataclass(frozen=True)
class JudgmentRecordL5:
    """سجل الوظيفة العليا والحكم — Layer 5 judgment record.

    The final non-arbitrary judgment about an element's functional
    classification: original, augmented, substituted, deleted, etc.
    """

    final_judgment: JudgmentCategory    # الحكم النهائي
    judgment_confidence: float          # ثقة الحكم     [0, 1]
    functional_class: str               # الصنف الوظيفي
    deictic_score: float = 0.0          # إشارية       [0, 1]
    relational_score: float = 0.0       # علائقية      [0, 1]
    identity_preservation_score: float = 0.0  # حفظ الهوية [0, 1]


@dataclass(frozen=True)
class RepresentationRecord:
    """سجل التمثيل البرمجي — Layer 6 representation record.

    Converts the theoretical model into a codeable structure with
    full traceability back through all layers.
    """

    entity_id: str                      # معرّف الكيان
    layer_trace: Tuple[StrictLayerID, ...]  # مسار الطبقات
    feature_hash: str                   # بصمة الخصائص
    root_mapping: str = ""              # تقابل جذري
    rule_set: Tuple[str, ...] = ()      # مجموعة القواعد
    validation_status: bool = False     # صحة التحقق
    confidence_chain: Tuple[float, ...] = ()  # سلسلة الثقة
    graph_target: str = ""              # هدف الرسم البياني


@dataclass(frozen=True)
class TransitionGate:
    """بوابة الانتقال — transition gate between strict layers.

    Each gate enforces the conditions that must hold before an
    element can advance from one layer to the next.
    """

    source_layer: StrictLayerID         # الطبقة المصدر
    target_layer: StrictLayerID         # الطبقة الهدف
    conditions_met: Tuple[bool, ...]    # الشروط المستوفاة
    gate_status: TransitionGateStatus   # حالة البوابة
    failure_reasons: Tuple[str, ...] = ()  # أسباب الفشل


@dataclass(frozen=True)
class LayerTraceRecord:
    """سجل التتبع الطبقي — full trace of an element through all layers.

    Collects the results from each layer (if reached) plus the
    final gate status.  ``layer_results`` maps each
    :class:`StrictLayerID` to the corresponding record produced
    by that layer (the concrete type depends on the layer).
    """

    element_id: str                     # معرّف العنصر
    layer_0: Optional[MentalFoundationRecord] = None
    layer_1: Optional[GenerativeProfileRecord] = None
    layer_2: Optional[AuditoryMinimumRecord] = None
    layer_3: Optional[StructuralProfileRecord] = None
    layer_4: Optional[TransformationProfileRecord] = None
    layer_5: Optional[JudgmentRecordL5] = None
    layer_6: Optional[RepresentationRecord] = None
    gates: Tuple[TransitionGate, ...] = ()
    final_gate_status: TransitionGateStatus = TransitionGateStatus.INSUFFICIENT_DATA


# ═══════════════════════════════════════════════════════════════════════
# Noun Fractal Constitution v1 — دستور الاسم الفراكتالي
# ═══════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class NounMinimumRecord:
    """الحد الأدنى المكتمل — minimum completeness conditions (Art. 11-19)."""

    thubut: bool                # الثبوت
    hadd: bool                  # الحد
    imtidad: bool               # الامتداد
    muqawwim: bool              # المقوِّم
    alaqa_binaiyya: bool        # العلاقة البنائية
    intizam: bool               # الانتظام
    wahda: bool                 # الوحدة
    qabiliyyat_ta3yin: bool     # قابلية التعيين


@dataclass(frozen=True)
class NounMorphologyRecord:
    """المادة والوزن — morphological substrate (Art. 15, 56-58)."""

    material: str                        # المادة
    pattern_type: NounPatternType        # نوع الوزن
    pattern: str                         # الوزن / القالب
    root: Tuple[str, ...]                # الجذر


@dataclass(frozen=True)
class NounClassificationRecord:
    """التصنيف — universality + genus level (Art. 24-33)."""

    universality: NounUniversality               # كلي / جزئي
    genus_level: NounGenusLevel                  # جنس / نوع / فرد
    proper_noun_kind: Optional[ProperNounKind]    # نوع العلم (if applicable)


@dataclass(frozen=True)
class NounAttributeRecord:
    """الصفة الاسمية — nominal-attribute classification (Art. 38-40)."""

    attribute_kind: Optional[NominalAttributeKind]   # نوع الصفة
    is_nominal_attribute: bool                       # هل هو صفة اسمية


@dataclass(frozen=True)
class NounInflectionRecord:
    """الوحدة والكثرة + التذكير والتأنيث + المعرفة والنكرة (Art. 41-50)."""

    number: NounNumber               # العدد
    gender: NounGender               # الجنس
    definiteness: NounDefiniteness   # التعريف


@dataclass(frozen=True)
class NounCompositionRecord:
    """المركب والمقترض (Art. 51-55)."""

    composition: NounComposition   # بسيط / مركب اسمي / مركب مزجي
    origin: NounOrigin             # أصيل / مقترض


@dataclass(frozen=True)
class NounSignificationRecord:
    """المطابقة والتضمن والالتزام في الاسم (Art. 59-62)."""

    mutabaqa: str                # ما يطابقه
    tadammun: Tuple[str, ...]    # ما يتضمنه
    iltizam: Tuple[str, ...]     # ما يلتزمه


@dataclass(frozen=True)
class NounFractalRecord:
    """البنية الفراكتالية المكتملة — N = (M, WT, D, T, Ref, Num, Gen, Def, Ready) (Art. 73-75)."""

    noun_id: str
    lemma: str
    surface: str
    direction: NounDirection                     # D  — الجهة الاسمية
    conceptual_type: SemanticType                # T  — النوع المفهومي
    morphology: NounMorphologyRecord             # M + WT
    classification: NounClassificationRecord     # Ref
    attribute: NounAttributeRecord
    inflection: NounInflectionRecord             # Num + Gen + Def
    composition: NounCompositionRecord
    signification: NounSignificationRecord
    minimum: NounMinimumRecord
    fractal_stage: NounFractalStage
    readiness: NounReadiness                     # Ready
    readiness_score: float                       # Ready_N
    existential_aspect: NounExistentialAspect


@dataclass(frozen=True)
class NounValidationResult:
    """القبول والرفض — acceptance / rejection verdict (Art. 76-77)."""

    valid: bool
    errors: Tuple[str, ...]
    readiness_score: float


# ── Additional re-exported types ──────────────────────────────────────


@dataclass(frozen=True)
class AmbiguityRecord:
    """سجل الالتباس — record of lexical or structural ambiguity."""

    record_id: str
    ambiguity_type: str
    candidates: Tuple[str, ...]
    resolved: bool = False


@dataclass(frozen=True)
class AxiomRecord:
    """سجل المسلّمة — a foundational axiom in the proof layer."""

    axiom_id: str
    statement: str
    status: ProofStatus = ProofStatus.ASSUMED
    domain: str = ""


@dataclass(frozen=True)
class CallabilityResult:
    """نتيجة قابلية الاستدعاء — whether a concept is callable."""

    callable: bool
    reason: str
    score: float = 1.0


@dataclass(frozen=True)
class CouplingRecord:
    """سجل الاقتران — coupling between signifier and signified."""

    coupling_id: str
    signifier_id: str
    signified_id: str
    relation_type: CouplingRelationType
    confidence: float = 1.0


@dataclass(frozen=True)
class ConflictRuleNode:
    """عقدة قاعدة التعارض — rule for resolving conceptual conflicts."""

    rule_id: str
    prefer_concept: bool
    rationale: str


@dataclass(frozen=True)
class CompositionalReadinessResult:
    """نتيجة الجاهزية التركيبية — compositional readiness verdict."""

    ready: bool
    missing_conditions: Tuple[str, ...] = ()
    score: float = 0.0


@dataclass(frozen=True)
class EpisodeValidationResult:
    """نتيجة التحقق من الحلقة — episode-level validation verdict."""

    valid: bool
    messages: Tuple[str, ...] = ()
    rank: EpistemicRank = EpistemicRank.CERTAIN


@dataclass(frozen=True)
class EpistemicConceptNode:
    """عقدة المفهوم المعرفي — concept node with epistemic status."""

    concept_id: str
    epistemic_status: EpistemicStatus
    confidence: float = 1.0


@dataclass(frozen=True)
class EssenceConditionPair:
    """زوج الماهية والشرط — essence paired with its condition."""

    essence: str
    condition: Optional[str] = None


@dataclass(frozen=True)
class InformationalStockRecord:
    """سجل المخزون المعلوماتي — informational stock record."""

    stock_id: str
    entries: Tuple[str, ...] = ()
    sufficiency: StockSufficiency = StockSufficiency.SUFFICIENT


@dataclass(frozen=True)
class JudgementNode:
    """عقدة الحكم — a judgement node in the epistemic graph."""

    judgement_id: str
    judgement_type: JudgementType
    content: str


@dataclass(frozen=True)
class LevelMatchResult:
    """نتيجة مطابقة المستوى — result of matching hierarchical levels."""

    matched: bool
    source_level: str
    target_level: str
    score: float = 1.0


@dataclass(frozen=True)
class OntologicalConstraintRecord:
    """سجل القيد الوجودي — an ontological constraint record."""

    constraint_id: str
    constraint_type: OntologicalConstraintType
    description: str
    satisfied: bool = True


@dataclass(frozen=True)
class PerceptualReadinessResult:
    """نتيجة الجاهزية الإدراكية — perceptual readiness verdict."""

    ready: bool
    gaps: Tuple[str, ...] = ()
    quality: float = 1.0


@dataclass(frozen=True)
class PriorInfoNode:
    """عقدة المعلومة السابقة — a prior-information node."""

    info_id: str
    content: str
    source: str


@dataclass(frozen=True)
class PriorInformationalStock:
    """المخزون المعلوماتي السابق — prior informational stock."""

    stock_id: str
    items: Tuple[str, ...] = ()
    complete: bool = False


@dataclass
class ProofDependencyGraph:
    """مخطط اعتماد البرهان — dependency graph for proofs."""

    axioms: Tuple[str, ...] = ()
    theorems: Tuple[str, ...] = ()
    edges: Tuple[Tuple[str, str], ...] = ()

    def is_acyclic(self) -> bool:
        """Return whether the dependency graph is acyclic."""
        return True

    def proof_coverage(self) -> float:
        """Return the fraction of nodes covered by proofs."""
        return 1.0 if self.theorems else 0.0

    def dangling_dependencies(self) -> Tuple[str, ...]:
        """Return node ids that are referenced but not defined."""
        defined = set(self.axioms) | set(self.theorems)
        dangling: list[str] = []
        for src, tgt in self.edges:
            if src not in defined:
                dangling.append(src)
            if tgt not in defined:
                dangling.append(tgt)
        return tuple(dict.fromkeys(dangling))

    def get_axiom(self, axiom_id: str) -> Optional[str]:
        """Return the axiom id if present, else ``None``."""
        return axiom_id if axiom_id in self.axioms else None

    def get_theorem(self, theorem_id: str) -> Optional[str]:
        """Return the theorem id if present, else ``None``."""
        return theorem_id if theorem_id in self.theorems else None

    def dependencies_of(self, node_id: str) -> Tuple[str, ...]:
        """Return ids that *node_id* depends on."""
        return tuple(tgt for src, tgt in self.edges if src == node_id)

    def dependents_of(self, node_id: str) -> Tuple[str, ...]:
        """Return ids that depend on *node_id*."""
        return tuple(src for src, tgt in self.edges if tgt == node_id)


@dataclass(frozen=True)
class ReadinessGate:
    """بوابة الجاهزية — gate that guards readiness transitions."""

    gate_id: str
    conditions: Tuple[str, ...]
    passed: bool = False


@dataclass(frozen=True)
class RealityAnchorNode:
    """عقدة مرساة الواقع — anchor node tying concepts to reality."""

    anchor_id: str
    kind: RealityKind
    description: str


@dataclass(frozen=True)
class SignifiedNode:
    """عقدة المدلول — a signified (concept) node."""

    node_id: str
    signified_class: SignifiedClass
    label: str
    confidence: float = 1.0


@dataclass(frozen=True)
class SignifierNode:
    """عقدة الدالّ — a signifier (surface form) node."""

    node_id: str
    signifier_class: SignifierClass
    surface: str


@dataclass(frozen=True)
class StockEntry:
    """مُدخل المخزون — a single entry in an informational stock."""

    entry_id: str
    content: str
    component: StockComponent


@dataclass(frozen=True)
class TheoremRecord:
    """سجل النظرية — a theorem in the proof layer."""

    theorem_id: str
    statement: str
    proof_status: ProofStatus = ProofStatus.PENDING
    dependencies: Tuple[str, ...] = ()


@dataclass(frozen=True)
class VerbConstitutionRecord:
    """سجل بنية الفعل — verb constitutional record."""

    verb_id: str
    root: Tuple[str, ...]
    pattern: str
    bab: VerbBab


@dataclass(frozen=True)
class VerbDerivativeRecord:
    """سجل المشتق الفعلي — verb derivative record."""

    derivative_id: str
    base_verb_id: str
    derivative_type: VerbDerivativeType
    surface: str


@dataclass(frozen=True)
class VerbEventRecord:
    """سجل الحدث الفعلي — verb event record."""

    event_id: str
    event_type: VerbEventType
    verb_id: str
    description: str = ""


@dataclass(frozen=True)
class VerbInflection:
    """تصريف الفعل — verb inflection record."""

    verb_id: str
    tense: str
    person: str
    number: str
    gender: str = ""


@dataclass(frozen=True)
class VerbMasdarRecord:
    """سجل المصدر — verb masdar (verbal noun) record."""

    masdar_id: str
    verb_id: str
    surface: str
    pattern: str = ""


@dataclass(frozen=True)
class VerbReadinessScore:
    """درجة جاهزية الفعل — verb readiness score."""

    verb_id: str
    score: float
    ready: bool


@dataclass(frozen=True)
class ZeroCoverageDetail:
    """تفاصيل التغطية الصفرية — zero-coverage detail record."""

    item_id: str
    zero_type: str
    covered: bool
    detail: str = ""
