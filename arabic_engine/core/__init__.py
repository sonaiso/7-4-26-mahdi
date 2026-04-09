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
    ConstraintType as ConstraintType,
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
    SlotState as SlotState,
)
from .enums import (
    POS,
    DalalaType,
    GuidanceState,
    IrabCase,
    IrabRole,
    SemanticType,
    SpaceRef,
    TimeRef,
    TruthState,
)
from .types import (
    Concept,
    DalalaLink,
    EvalResult,
    Grapheme,
    InferenceResult,
    LexicalClosure,
    Proposition,
    RootPattern,
    Syllable,
    SyntaxNode,
    TimeSpaceTag,
    WorldFact,
)

__all__ = [
    "POS",
    "DalalaType",
    "GuidanceState",
    "IrabCase",
    "IrabRole",
    "SemanticType",
    "SpaceRef",
    "TimeRef",
    "TruthState",
    "Concept",
    "DalalaLink",
    "EvalResult",
    "Grapheme",
    "InferenceResult",
    "LexicalClosure",
    "Proposition",
    "RootPattern",
    "Syllable",
    "SyntaxNode",
    "TimeSpaceTag",
    "WorldFact",
]
