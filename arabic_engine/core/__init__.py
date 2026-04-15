"""Core enums and types used across the engine.

This package re-exports all public enumerations from
:mod:`arabic_engine.core.enums` and all dataclass types from
:mod:`arabic_engine.core.types` so that client code can import from a
single namespace::

    from arabic_engine.core import POS, LexicalClosure, DMin

The :mod:`arabic_engine.core.contracts` module is intentionally *not*
re-exported here because it is a utility/verification module, not a data
type.
"""

# ── Enum re-exports ─────────────────────────────────────────────────
from .enums import (
    POS as POS,
)

# Epistemic v1 enums
from .enums import (
    CarrierType as CarrierType,
)
from .enums import (
    CombinationType as CombinationType,
)
from .enums import (
    ConceptClosureStatus as ConceptClosureStatus,
)
from .enums import (
    ConceptEntityAttribute as ConceptEntityAttribute,
)
from .enums import (
    ConceptFormationMode as ConceptFormationMode,
)
from .enums import (
    ConceptGateID as ConceptGateID,
)
from .enums import (
    ConceptIndependence as ConceptIndependence,
)
from .enums import (
    ConceptRelationType as ConceptRelationType,
)
from .enums import (
    ConceptualSignifiedClass as ConceptualSignifiedClass,
)
from .enums import (
    ConceptUniversalParticular as ConceptUniversalParticular,
)
from .enums import (
    ConditionToken as ConditionToken,
)
from .enums import (
    ConfirmationRank as ConfirmationRank,
)
from .enums import (
    ConflictResolutionMethod as ConflictResolutionMethod,
)
from .enums import (
    ConflictState as ConflictState,
)
from .enums import (
    ConflictType as ConflictType,
)
from .enums import (
    ConstraintStrength as ConstraintStrength,
)
from .enums import (
    ConstraintType as ConstraintType,
)
from .enums import (
    ContaminationLevel as ContaminationLevel,
)
from .enums import (
    CouplingRelationType as CouplingRelationType,
)
from .enums import (
    CulturalScope as CulturalScope,
)
from .enums import (
    DalaalaKind as DalaalaKind,
)
from .enums import (
    DalalaType as DalalaType,
)
from .enums import (
    DecisionCode as DecisionCode,
)
from .enums import (
    DefinitenessRole as DefinitenessRole,
)
from .enums import (
    DiachronicStatus as DiachronicStatus,
)
from .enums import (
    DiscourseGapType as DiscourseGapType,
)
from .enums import (
    DiscourseValidationOutcome as DiscourseValidationOutcome,
)
from .enums import (
    ElementClass as ElementClass,
)
from .enums import (
    ElementFunction as ElementFunction,
)
from .enums import (
    ElementLayer as ElementLayer,
)
from .enums import (
    EpistemicRank as EpistemicRank,
)
from .enums import (
    EpistemicStatus as EpistemicStatus,
)
from .enums import (
    EvidenceType as EvidenceType,
)
from .enums import (
    ExchangePurposeType as ExchangePurposeType,
)
from .enums import (
    ExchangeStatus as ExchangeStatus,
)
from .enums import (
    ExchangeStyleType as ExchangeStyleType,
)
from .enums import (
    ExchangeType as ExchangeType,
)
from .enums import (
    ExplicitnessLevel as ExplicitnessLevel,
)
from .enums import (
    FractalStage as FractalStage,
)
from .enums import (
    FrameType as FrameType,
)
from .enums import (
    FunctionRole as FunctionRole,
)
from .enums import (
    FuncTransitionClass as FuncTransitionClass,
)
from .enums import (
    GapSeverity as GapSeverity,
)
from .enums import (
    GuidanceState as GuidanceState,
)
from .enums import (
    HarakaState as HarakaState,
)
from .enums import (
    HypothesisStatus as HypothesisStatus,
)
from .enums import (
    InfoKind as InfoKind,
)
from .enums import (
    InsertionPolicy as InsertionPolicy,
)
from .enums import (
    InstitutionalCategory as InstitutionalCategory,
)
from .enums import (
    InterpretationSource as InterpretationSource,
)
from .enums import (
    InterpretiveOutcomeType as InterpretiveOutcomeType,
)
from .enums import (
    InterpretiveStability as InterpretiveStability,
)
from .enums import (
    InterPropositionLink as InterPropositionLink,
)
from .enums import (
    IrabCase as IrabCase,
)
from .enums import (
    IrabRole as IrabRole,
)
from .enums import (
    JudgementType as JudgementType,
)
from .enums import (
    LinkKind as LinkKind,
)
from .enums import (
    MafhumType as MafhumType,
)
from .enums import (
    MethodFamily as MethodFamily,
)
from .enums import (
    OntologicalConstraintType as OntologicalConstraintType,
)
from .enums import (
    OntologicalLayer as OntologicalLayer,
)
from .enums import (
    OntologicalMode as OntologicalMode,
)
from .enums import (
    OperationalCapacity as OperationalCapacity,
)

# ── Particle Fractal Constitution v1 enum re-exports ────────────────
from .enums import (
    ParticleDalala as ParticleDalala,
)
from .enums import (
    NasikhType as NasikhType,
)
from .enums import (
    NormativeCategory as NormativeCategory,
)
from .enums import (
    ParticleEffect as ParticleEffect,
)
from .enums import (
    ParticleKind as ParticleKind,
)
from .enums import (
    ParticleReadiness as ParticleReadiness,
)
from .enums import (
    ParticleScope as ParticleScope,
)
from .enums import (
    PathKind as PathKind,
)
from .enums import (
    PerceptualGapReason as PerceptualGapReason,
)
from .enums import (
    PhonCategory as PhonCategory,
)
from .enums import (
    PhonFeature as PhonFeature,
)
from .enums import (
    PhonGroup as PhonGroup,
)
from .enums import (
    PhonTransform as PhonTransform,
)
from .enums import (
    ProofPathKind as ProofPathKind,
)
from .enums import (
    ProofStatus as ProofStatus,
)
from .enums import (
    RealityKind as RealityKind,
)
from .enums import (
    SemanticType as SemanticType,
)
from .enums import (
    SenseModality as SenseModality,
)
from .enums import (
    ReadinessLevel as ReadinessLevel,
)
from .enums import (
    ReadinessStatus as ReadinessStatus,
)
from .enums import (
    RealityKind as RealityKind,
)
from .enums import (
    SignifierClass as SignifierClass,
)
from .enums import (
    SingleConceptType as SingleConceptType,
)
from .enums import (
    SlotState as SlotState,
)
from .enums import (
    SourceType as SourceType,
)
from .enums import (
    SpaceRef as SpaceRef,
)
from .enums import (
    StrictLayerID as StrictLayerID,
)
from .enums import (
    StructuralNode as StructuralNode,
)
from .enums import (
    StyleKind as StyleKind,
)
from .enums import (
    SyllablePosition as SyllablePosition,
)
from .enums import (
    SyllableState as SyllableState,
)
from .enums import (
    TimeRef as TimeRef,
)
from .enums import (
    TraceMode as TraceMode,
)
from .enums import (
    TruthState as TruthState,
)
from .enums import (
    UnicodeProfileType as UnicodeProfileType,
)
from .enums import (
    UniversalParticular as UniversalParticular,
)
from .enums import (
    UtteranceMode as UtteranceMode,
)
from .enums import (
    UtteranceToConceptConstraint as UtteranceToConceptConstraint,
)
from .enums import (
    UtteredFormClass as UtteredFormClass,
)
from .enums import (
    ValidationState as ValidationState,
)
from .enums import (
    StockComponent as StockComponent,
)
from .enums import (
    StockSufficiency as StockSufficiency,
)
from .enums import (
    StrictLayerID as StrictLayerID,
)

# ── Fractal Kernel type re-exports ──────────────────────────────────
from .types import (
    ActivationRecord as ActivationRecord,
)

# ── Composition / Syntax Constitution v1 type re-exports ────────────
from .types import (
    AmbiguityRecord as AmbiguityRecord,
)

# ── Strict 7-Layer System type re-exports ─────────────────────────
from .types import (
    AuditoryMinimumRecord as AuditoryMinimumRecord,
)
from .types import (
    AxiomRecord as AxiomRecord,
)

# ── Informational Stock Governance (ISG) Constitution v1 type re-exports ──
from .types import (
    CallabilityResult as CallabilityResult,
)
from .types import (
    CliticRecord as CliticRecord,
)
from .types import (
    CombiningMarkDetail as CombiningMarkDetail,
)
from .types import (
    Concept as Concept,
)
from .enums import (
    LinguisticZeroType as LinguisticZeroType,
)
from .enums import (
    LogicalStatus as LogicalStatus,
)
from .enums import (
    LogicalSubtype as LogicalSubtype,
)
from .enums import (
    MafhumType as MafhumType,
)
from .enums import (
    Modality as Modality,
)
from .enums import (
    OntologicalLayer as OntologicalLayer,
)
from .enums import (
    OntologicalSubtype as OntologicalSubtype,
)
from .enums import (
    PhonCategory as PhonCategory,
)
from .types import (
    ConceptRecord as ConceptRecord,
)
from .enums import (
    VerbAugmentation as VerbAugmentation,
)
from .enums import (
    VerbBab as VerbBab,
)
from .enums import (
    VerbDerivativeType as VerbDerivativeType,
)
from .enums import (
    VerbEventType as VerbEventType,
)
from .enums import (
    VerbGender as VerbGender,
)
from .enums import (
    VerbMode as VerbMode,
)
from .enums import (
    VerbNumber as VerbNumber,
)
from .enums import (
    VerbPerson as VerbPerson,
)
from .enums import (
    VerbReadiness as VerbReadiness,
)
from .enums import (
    VerbTense as VerbTense,
)
from .enums import (
    VerbTransitivity as VerbTransitivity,
)
from .enums import (
    VerbVoice as VerbVoice,
)

# Epistemic v1 types
from .types import (
    ConflictRuleRecord as ConflictRuleRecord,
)
from .types import (
    CouplingRecord as CouplingRecord,
)
from .types import (
    ConflictRuleNode as ConflictRuleNode,
)
from .types import (
    ConflictRuleRecord as ConflictRuleRecord,
)
from .enums import (
    Polarity as Polarity,
)
from .enums import (
    PragmaticSubtype as PragmaticSubtype,
)
from .enums import (
    PrimarySignifiedType as PrimarySignifiedType,
)
from .enums import (
    ProofStatus as ProofStatus,
)
from .enums import (
    PropositionalSubtype as PropositionalSubtype,
)
from .enums import (
    ReferentialSubtype as ReferentialSubtype,
)
from .enums import (
    RelationalSubtype as RelationalSubtype,
)
from .enums import (
    RhetoricalStatus as RhetoricalStatus,
)
from .types import (
    CompositionalReadinessResult as CompositionalReadinessResult,
)
from .types import (
    Concept as Concept,
)
from .enums import (
    SemanticType as SemanticType,
)
from .enums import (
    SignifiedTemporalStatus as SignifiedTemporalStatus,
)
from .enums import (
    SlotState as SlotState,
)
from .types import (
    DecisionTrace as DecisionTrace,
)
from .enums import (
    SpecificityDegree as SpecificityDegree,
)
from .enums import (
    TimeRef as TimeRef,
)
from .enums import (
    WordClass as WordClass,
)
from .enums import (
    ZeroCoverage as ZeroCoverage,
)
from .types import (
    DiscourseConceptRecord as DiscourseConceptRecord,
)
from .types import (
    DiscourseExchangeNode as DiscourseExchangeNode,
)
from .types import (
    DiscourseExchangeResult as DiscourseExchangeResult,
)
from .types import (
    DiscourseGapRecord as DiscourseGapRecord,
)
from .types import (
    DiscourseUtteranceRecord as DiscourseUtteranceRecord,
)
from .types import (
    DMin as DMin,
)
from .types import (
    EnrichedGrapheme as EnrichedGrapheme,
)
from .types import (
    EnrichedSyllable as EnrichedSyllable,
)
from .types import (
    EpisodeValidationResult as EpisodeValidationResult,
)
from .types import (
    EpistemicConceptNode as EpistemicConceptNode,
)
from .types import (
    EssenceConditionPair as EssenceConditionPair,
)
from .types import (
    EvalResult as EvalResult,
)
from .types import (
    GapRecord as GapRecord,
)
from .types import (
    Grapheme as Grapheme,
)
from .types import (
    HarakaUnit as HarakaUnit,
)
from .types import (
    HypothesisNode as HypothesisNode,
)
from .types import (
    InferenceResult as InferenceResult,
)
from .types import (
    InformationalStockRecord as InformationalStockRecord,
)
from .types import (
    InterpretiveOutcomeRecord as InterpretiveOutcomeRecord,
)
from .types import (
    JudgementNode as JudgementNode,
)
from .types import (
    JudgementRecord as JudgementRecord,
)
from .types import (
    KnowledgeEpisode as KnowledgeEpisode,
)
from .types import (
    KnowledgeEpisodeInput as KnowledgeEpisodeInput,
)
from .types import (
    LayerPromotionRule as LayerPromotionRule,
)
from .types import (
    LayerTraceRecord as LayerTraceRecord,
)
from .types import (
    LevelMatchResult as LevelMatchResult,
)
from .types import (
    LinguisticCarrierRecord as LinguisticCarrierRecord,
)
from .types import (
    LinkingTraceRecord as LinkingTraceRecord,
)
from .types import (
    MethodRecord as MethodRecord,
)
from .types import (
    OntologicalConstraintRecord as OntologicalConstraintRecord,
)
from .types import (
    OntologicalSignified as OntologicalSignified,
)
from .types import (
    OpinionTraceRecord as OpinionTraceRecord,
)
from .types import (
    PerceptualReadinessResult as PerceptualReadinessResult,
)
from .types import (
    PriorInfoNode as PriorInfoNode,
)
from .types import (
    PriorInfoRecord as PriorInfoRecord,
)
from .types import (
    PriorInformationalStock as PriorInformationalStock,
)
from .types import (
    ProofDependencyGraph as ProofDependencyGraph,
)
from .types import (
    ProofPathRecord as ProofPathRecord,
)
from .types import (
    Proposition as Proposition,
)
from .types import (
    RationalSelfRecord as RationalSelfRecord,
)
from .types import (
    ReadinessGate as ReadinessGate,
)
from .types import (
    RealityAnchorNode as RealityAnchorNode,
)
from .types import (
    RealityAnchorRecord as RealityAnchorRecord,
)
from .types import (
    RootPattern as RootPattern,
)
from .types import (
    Self_ as Self_,
)
from .types import (
    SenseTraceRecord as SenseTraceRecord,
)
from .types import (
    SignifiedNode as SignifiedNode,
)
from .types import (
    SignifierNode as SignifierNode,
)
from .types import (
    StockEntry as StockEntry,
)
from .types import (
    StructuralProfileRecord as StructuralProfileRecord,
)
from .types import (
    Syllable as Syllable,
)
from .types import (
    SyllableUnit as SyllableUnit,
)
from .types import (
    SyntaxNode as SyntaxNode,
)
from .types import (
    TheoremRecord as TheoremRecord,
)
from .types import (
    TimeSpaceTag as TimeSpaceTag,
)
from .types import (
    TokenAnalysis as TokenAnalysis,
)
from .types import (
    TransformationProfileRecord as TransformationProfileRecord,
)
from .types import (
    TransitionGate as TransitionGate,
)
from .types import (
    TriadicBlockRecord as TriadicBlockRecord,
)
from .types import (
    UtteranceRecord as UtteranceRecord,
)
from .types import (
    ValidationResult as ValidationResult,
)
from .types import (
    VerbConstitutionRecord as VerbConstitutionRecord,
)
from .types import (
    VerbDerivativeRecord as VerbDerivativeRecord,
)
from .types import (
    VerbEventRecord as VerbEventRecord,
)
from .types import (
    VerbInflection as VerbInflection,
)
from .types import (
    VerbMasdarRecord as VerbMasdarRecord,
)
from .types import (
    VerbReadinessScore as VerbReadinessScore,
)
from .types import (
    WorldFact as WorldFact,
)
from .types import (
    ZeroCoverageDetail as ZeroCoverageDetail,
)
from .types import (
    ZeroSlotRecord as ZeroSlotRecord,
)

__all__ = [
    # ── enums ───────────────────────────────────────────────────────
    "POS",
    "AffectiveDimension",
    "AuthorityLevel",
    "CarrierClass",
    "CarrierType",
    "CategorizationMode",
    "CausalRole",
    "CellType",
    "CombinationType",
    "CompositionDegree",
    "ConstraintType",
    "ContextRequirement",
    "DalalaType",
    "DependencyDegree",
    "ElementClass",
    "ElementFunction",
    "ElementLayer",
    "EmbodiedDomain",
    "EpistemicRank",
    "EpistemicStatus",
    "EvidenceType",
    "ExchangeStatus",
    "ExchangePurposeType",
    "ExchangeStyleType",
    "ExchangeType",
    "ExplicitnessLevel",
    "FrameType",
    "FractalStage",
    "FuncTransitionClass",
    "FunctionRole",
    "GapSeverity",
    "GuidanceState",
    "HarakaState",
    "InfoKind",
    "InsertionPolicy",
    "InstitutionalCategory",
    "InterpretationSource",
    "InterpretiveOutcomeType",
    "InterpretiveStability",
    "IrabCase",
    "IrabRole",
    "LogicalStatus",
    "LogicalSubtype",
    "MafhumType",
    "Modality",
    "OntologicalLayer",
    "OntologicalMode",
    "OperationalCapacity",
    "PathKind",
    "PerceptualGapReason",
    "PhonCategory",
    "PhonFeature",
    "PhonGroup",
    "PhonTransform",
    "Polarity",
    "PragmaticSubtype",
    "PrimarySignifiedType",
    "ProofStatus",
    "PurposeType",
    "RankType",
    "RationalSelfKind",
    "RealityKind",
    "ReceiverExpectedAction",
    "ReceiverRoleType",
    "ReceiverState",
    "ReceptionMode",
    "ReceptionStateType",
    "ReadinessLevel",
    "ReadinessStatus",
    "ReversibleValue",
    "SalienceLevel",
    "ScriptPhase",
    "SelfModelAspect",
    "SemanticType",
    "SignifiedTemporalStatus",
    "SlotState",
    "SpaceRef",
    "StockComponent",
    "StockSufficiency",
    "StyleKind",
    "SyllablePosition",
    "TimeRef",
    "TraceMode",
    "TraceQuality",
    "TransitionCondition",
    "TransitionLaw",
    "TransitionType",
    "TransformJudgment",
    "TransformState",
    "TriadType",
    "TrustBasis",
    "TrustLevel",
    "TruthState",
    "UnicodeProfileType",
    "UtteranceMode",
    "UtteranceToConceptConstraint",
    # Epistemic v1 enums
    "CarrierType",
    "ContaminationLevel",
    "EpistemicRank",
    "GapSeverity",
    "JudgementType",
    "LinkKind",
    "MethodFamily",
    "ProofPathKind",
    "RealityKind",
    "SenseModality",
    "TraceMode",
    "ValidationState",
    # ── Verb Fractal Constitution v1 enums ────────────────────────
    "NasikhType",
    "VerbAugmentation",
    "VerbBab",
    "VerbDerivativeType",
    "VerbEventType",
    "VerbGender",
    "VerbMode",
    "VerbNumber",
    "VerbPerson",
    "VerbReadiness",
    "VerbTense",
    "VerbTransitivity",
    "VerbVoice",
    # ── Fractal Kernel enums ───────────────────────────────────────
    "ActivationStage",
    "ConflictState",
    "ConstraintStrength",
    "HypothesisStatus",
    "RevisionType",
    "SignalType",
    # ── kernel ──────────────────────────────────────────────────────
    "KERNEL_RELATION_PAIRS",
    "KERNEL_REQUIRED_FIELDS",
    "KernelDiscourseExchange",
    "KernelEdge",
    "KernelGraph",
    "KernelKnowledgeEpisode",
    "KernelLabel",
    "KernelLinguisticProfile",
    "KernelNode",
    "KernelRelation",
    "KernelReusableModel",
    "KernelUtterance",
    "KernelValidationResult",
    "derive_discourse_exchange",
    "derive_knowledge_episode",
    "derive_linguistic_profile",
    "derive_reusable_model",
    "derive_utterance_from_carrier",
    "validate_kernel_graph",
    # ── types ───────────────────────────────────────────────────────
    "AEU",
    "AxiomRecord",
    "Concept",
    "ConceptRelation",
    "CompositionalReadinessResult",
    "ConflictRuleNode",
    "ConceptSeed",
    "CouplingRecord",
    "DalalaLink",
    "DiscourseCarrierRecord",
    "DiscourseConceptRecord",
    "DiscourseExchangeNode",
    "DiscourseExchangeResult",
    "DiscourseGapRecord",
    "DiscourseUtteranceRecord",
    "DMin",
    "EpisodeValidationResult",
    "EpistemicConceptNode",
    "EssenceConditionPair",
    "EvalResult",
    "FinalApprovalComponents",
    "EvidenceNode",
    "ExchangePurposeRecord",
    "ExchangeStyleRecord",
    "GapNode",
    "GapRecord",
    "Grapheme",
    "HarakaUnit",
    "InferenceResult",
    "InformationalStockRecord",
    "InterpretiveOutcomeRecord",
    "JudgementNode",
    "JudgementRecord",
    "KnowledgeEpisode",
    "KnowledgeEpisodeInput",
    "KnowledgeEpisodeNode",
    "LayerPromotionRule",
    "LexicalClosure",
    "LinguisticCarrierNode",
    "LinguisticCarrierRecord",
    "LinkingTraceNode",
    "LinkingTraceRecord",
    "MethodNode",
    "MethodRecord",
    "OntologicalConstraintRecord",
    "OntologyV1Record",
    "OpinionTraceNode",
    "OpinionTraceRecord",
    "PerceptualReadinessResult",
    "PriorInfoNode",
    "PriorInfoRecord",
    "PriorInformationalStock",
    "ProofDependencyGraph",
    "ProofPathNode",
    "ProofPathRecord",
    "Proposition",
    "RationalSelfRecord",
    "RealityAnchorNode",
    "RealityAnchorRecord",
    "ReadinessGate",
    "ReceiverRoleRecord",
    "ReceptionRecord",
    "ReceptionStateRecord",
    "RootPattern",
    "SelfNode",
    "SenderRoleRecord",
    "SenseTraceNode",
    "SenseTraceRecord",
    "SignifiedNode",
    "SignifierNode",
    "StockEntry",
    "Syllable",
    "SyllableUnit",
    "SyntaxNode",
    "TheoremRecord",
    "TransformCandidate",
    "TimeSpaceTag",
    "TriadicBlockRecord",
    "TrustProfileRecord",
    "UtteranceNode",
    "UtteranceRecord",
    "ValidationResult",
    # ── Verb Fractal Constitution v1 types ────────────────────────
    "VerbConstitutionRecord",
    "VerbDerivativeRecord",
    "VerbEventRecord",
    "VerbInflection",
    "VerbMasdarRecord",
    "VerbReadinessScore",
    "WorldFact",
    "ZeroSlotRecord",
    # Epistemic v1 types
    "ConflictRuleRecord",
    "ConceptRecord",
    "GapRecord",
    "JudgementRecord",
    "KnowledgeEpisode",
    "KnowledgeEpisodeInput",
    "LinguisticCarrierRecord",
    "LinkingTraceRecord",
    "MethodRecord",
    "OpinionTraceRecord",
    "PriorInfoRecord",
    "ProofPathRecord",
    "RealityAnchorRecord",
    "Self_",
    "SenseTraceRecord",
    "UtteranceRecord",
    "ValidationResult",
]
