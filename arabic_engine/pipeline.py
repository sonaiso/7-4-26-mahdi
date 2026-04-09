"""Main pipeline — orchestrates all layers of the Arabic engine.

Pipeline (v2):
  Normalize → Tokenize → Lexical Closure → Syntax → Ontology
  → Dalāla Validation → Judgment → Time/Space → Evaluation
  → Inference → World-Model check

Each step is a pure(ish) function operating on typed records, so the
full composition F is computable (see README proof).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from arabic_engine.cognition.evaluation import build_proposition, evaluate
from arabic_engine.cognition.inference_rules import InferenceEngine
from arabic_engine.cognition.time_space import tag as time_space_tag
from arabic_engine.cognition.world_model import WorldModel
from arabic_engine.core.contracts import verify_contracts  # noqa: F401 — re-export
from arabic_engine.core.types import (
    Concept,
    DalalaLink,
    EvalResult,
    InferenceResult,
    LexicalClosure,
    Proposition,
    SyntaxNode,
    TimeSpaceTag,
    WordZeroCoverageReport,
)
from arabic_engine.linkage.dalala import full_validation
from arabic_engine.signified.ontology import batch_map
from arabic_engine.signified.zero_coverage import analyze_word_zero_coverage
from arabic_engine.signifier.root_pattern import batch_closure
from arabic_engine.signifier.unicode_norm import normalize, tokenize
from arabic_engine.syntax.syntax import analyse as syntax_analyse

# ── Pipeline result ─────────────────────────────────────────────────

@dataclass
class PipelineResult:
    """Container for the full analysis of a single sentence.

    Every field maps directly to the output of a named pipeline layer,
    so the object forms a complete audit trail of the computation.

    Attributes:
        raw: The original, unmodified input string.
        normalised: The string after Unicode normalisation (L0).
        tokens: Whitespace-delimited tokens (L1).
        closures: Lexical closures for each token (L2).
        syntax_nodes: I'rāb-annotated syntax nodes (L3).
        concepts: Ontological concept nodes for each closure (L4).
        dalala_links: Signification (dalāla) validation links (L5).
        proposition: The structured judgment built from the sentence (L6).
        time_space: Temporal and spatial anchoring tag (L7).
        eval_result: Truth/guidance/confidence evaluation vector (L8).
        inferences: Derived propositions from the rule engine (L9).
            Empty list when no inference engine was provided.
        world_adjustment: Confidence multiplier from the world model (L10).
            Defaults to ``0.5`` when no world model was provided.
        word_zero_coverage: Per-token linguistic-zero coverage reports (L11).
            Empty list when ``analyze_zeros=False`` (the default).
    """

    raw: str
    normalised: str
    tokens: List[str]
    closures: List[LexicalClosure]
    syntax_nodes: List[SyntaxNode]
    concepts: List[Concept]
    dalala_links: List[DalalaLink]
    proposition: Proposition
    time_space: TimeSpaceTag
    eval_result: EvalResult
    inferences: List[InferenceResult] = field(default_factory=list)
    world_adjustment: float = 0.5
    word_zero_coverage: List[WordZeroCoverageReport] = field(default_factory=list)


# ── Pipeline ────────────────────────────────────────────────────────

def run(
    text: str,
    *,
    world: Optional[WorldModel] = None,
    inference_engine: Optional[InferenceEngine] = None,
    analyze_zeros: bool = False,
) -> PipelineResult:
    """Execute the full v2 pipeline on *text*.

    The pipeline runs up to twelve sequential layers (L0–L11):

    * L0  — Unicode normalisation
    * L1  — Tokenisation
    * L2  — Lexical closure (root/pattern extraction)
    * L3  — Syntax (i'rāb assignment and dependency linking)
    * L4  — Ontological mapping (signifier → signified)
    * L5  — Dalāla validation (signification links)
    * L6  — Judgment / proposition construction
    * L7  — Time/space anchoring
    * L8  — Truth and guidance evaluation
    * L9  — Inference rule application (optional)
    * L10 — World-model confidence adjustment (optional)
    * L11 — Linguistic-zero coverage analysis (optional)

    Args:
        text: Raw Arabic input (may include tashkīl).
        world: An external world model for confidence adjustment.
            When ``None``, the world-adjustment factor defaults to 0.5.
        inference_engine: A rule engine for deriving new propositions.
            When ``None``, the ``inferences`` list in the result is empty.
        analyze_zeros: When ``True``, run L11 and populate
            ``word_zero_coverage`` with one report per token.
            Defaults to ``False``.

    Returns:
        A :class:`PipelineResult` containing the outputs of all pipeline
        layers.
    """
    # L0 — Normalise
    normalised = normalize(text)

    # L1 — Tokenize
    tokens = tokenize(text)

    # L2 — Lexical Closure
    closures = batch_closure(tokens)

    # L3 — Syntax (v2)
    syntax_nodes = syntax_analyse(closures)

    # L4 — Ontological Mapping
    concepts = batch_map(closures)

    # L5 — Dalāla Validation
    links = full_validation(closures, concepts)

    # L6 — Judgment
    proposition = build_proposition(closures, concepts, links)

    # L7 — Time/Space (v2)
    ts_tag = time_space_tag(closures, proposition)

    # L8 — Evaluation
    eval_result = evaluate(proposition, links)

    # L9 — Inference (v2)
    inferences: List[InferenceResult] = []
    if inference_engine is not None:
        inferences = inference_engine.run([proposition])

    # L10 — World-Model adjustment (v2)
    adjustment = 0.5
    if world is not None:
        adjustment = world.confidence_adjustment(proposition)
        # Blend world-model confidence with dalāla confidence
        eval_result.confidence = round(
            eval_result.confidence * adjustment, 4
        )

    # L11 — Linguistic-zero coverage (optional)
    zero_coverage: List[WordZeroCoverageReport] = []
    if analyze_zeros:
        zero_coverage = [analyze_word_zero_coverage(tok) for tok in tokens]

    return PipelineResult(
        raw=text,
        normalised=normalised,
        tokens=tokens,
        closures=closures,
        syntax_nodes=syntax_nodes,
        concepts=concepts,
        dalala_links=links,
        proposition=proposition,
        time_space=ts_tag,
        eval_result=eval_result,
        inferences=inferences,
        world_adjustment=adjustment,
        word_zero_coverage=zero_coverage,
    )
