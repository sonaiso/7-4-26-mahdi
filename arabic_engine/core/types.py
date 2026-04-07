"""Data types (named tuples / dataclasses) for the Arabic engine.

Every stage of the pipeline produces and consumes typed records so that
all data flowing through the system is a *discrete, numerically-encoded*
structure — satisfying the computability proof in the README.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .enums import (
    POS,
    SemanticType,
    DalalaType,
    TruthState,
    GuidanceState,
    IrabCase,
    IrabRole,
    TimeRef,
    SpaceRef,
    ConstraintType,
    MafhumType,
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
