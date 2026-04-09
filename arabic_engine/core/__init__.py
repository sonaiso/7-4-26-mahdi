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

from .enums import (  # noqa: F401 -- intentional re-exports
    POS as POS,
)
from .enums import (
    CombinationType as CombinationType,
)
from .enums import (
    ConceptualSignifiedClass as ConceptualSignifiedClass,
)
from .enums import (
    ConstraintType as ConstraintType,
)
from .enums import (
    CouplingRelationType as CouplingRelationType,
)
from .enums import (
    DalalaType as DalalaType,
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
    GuidanceState as GuidanceState,
)
from .enums import (
    IrabCase as IrabCase,
)
from .enums import (
    IrabRole as IrabRole,
)
from .enums import (
    MafhumType as MafhumType,
)
from .enums import (
    OntologicalConstraintType as OntologicalConstraintType,
)
from .enums import (
    OntologicalLayer as OntologicalLayer,
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
    ProofStatus as ProofStatus,
)
from .enums import (
    SemanticType as SemanticType,
)
from .enums import (
    SignifiedClass as SignifiedClass,
)
from .enums import (
    SignifierClass as SignifierClass,
)
from .enums import (
    SlotState as SlotState,
)
from .enums import (
    SpaceRef as SpaceRef,
)
from .enums import (
    TimeRef as TimeRef,
)
from .enums import (
    TruthState as TruthState,
)
from .enums import (
    UnicodeProfileType as UnicodeProfileType,
)
from .enums import (
    UtteranceToConceptConstraint as UtteranceToConceptConstraint,
)
from .enums import (
    UtteredFormClass as UtteredFormClass,
)
from .types import (  # noqa: F401 -- intentional re-exports
    AEU as AEU,
)
from .types import (
    AxiomRecord as AxiomRecord,
)
from .types import (
    Concept as Concept,
)
from .types import (
    CouplingRecord as CouplingRecord,
)
from .types import (
    DalalaLink as DalalaLink,
)
from .types import (
    DMin as DMin,
)
from .types import (
    EssenceConditionPair as EssenceConditionPair,
)
from .types import (
    EvalResult as EvalResult,
)
from .types import (
    Grapheme as Grapheme,
)
from .types import (
    InferenceResult as InferenceResult,
)
from .types import (
    LayerPromotionRule as LayerPromotionRule,
)
from .types import (
    LexicalClosure as LexicalClosure,
)
from .types import (
    OntologicalConstraintRecord as OntologicalConstraintRecord,
)
from .types import (
    OntologyV1Record as OntologyV1Record,
)
from .types import (
    ProofDependencyGraph as ProofDependencyGraph,
)
from .types import (
    Proposition as Proposition,
)
from .types import (
    RootPattern as RootPattern,
)
from .types import (
    SignifiedNode as SignifiedNode,
)
from .types import (
    SignifierNode as SignifierNode,
)
from .types import (
    Syllable as Syllable,
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
    TriadicBlockRecord as TriadicBlockRecord,
)
from .types import (
    WorldFact as WorldFact,
)
from .types import (
    ZeroSlotRecord as ZeroSlotRecord,
)

__all__ = [
    # enums
    "POS",
    "CombinationType",
    "ConceptualSignifiedClass",
    "ConstraintType",
    "CouplingRelationType",
    "DalalaType",
    "ElementClass",
    "ElementFunction",
    "ElementLayer",
    "GuidanceState",
    "IrabCase",
    "IrabRole",
    "MafhumType",
    "OntologicalConstraintType",
    "OntologicalLayer",
    "PhonCategory",
    "PhonFeature",
    "PhonGroup",
    "PhonTransform",
    "ProofStatus",
    "SemanticType",
    "SignifiedClass",
    "SignifierClass",
    "SlotState",
    "SpaceRef",
    "TimeRef",
    "TruthState",
    "UnicodeProfileType",
    "UtteredFormClass",
    "UtteranceToConceptConstraint",
    # types
    "AEU",
    "Concept",
    "CouplingRecord",
    "DalalaLink",
    "DMin",
    "EvalResult",
    "Grapheme",
    "InferenceResult",
    "LayerPromotionRule",
    "LexicalClosure",
    "OntologicalConstraintRecord",
    "OntologyV1Record",
    "Proposition",
    "RootPattern",
    "SignifiedNode",
    "SignifierNode",
    "Syllable",
    "SyntaxNode",
    "TimeSpaceTag",
    "TriadicBlockRecord",
    "WorldFact",
    "ZeroSlotRecord",
]
