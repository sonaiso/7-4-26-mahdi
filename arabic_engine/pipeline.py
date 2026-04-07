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
)
from arabic_engine.linkage.dalala import full_validation
from arabic_engine.signified.ontology import batch_map
from arabic_engine.signifier.root_pattern import batch_closure
from arabic_engine.signifier.unicode_norm import normalize, tokenize
from arabic_engine.syntax.syntax import analyse as syntax_analyse

# ── Pipeline result ─────────────────────────────────────────────────

@dataclass
class PipelineResult:
    """Container for the full analysis of a single sentence."""
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


# ── Pipeline ────────────────────────────────────────────────────────

def run(
    text: str,
    *,
    world: Optional[WorldModel] = None,
    inference_engine: Optional[InferenceEngine] = None,
) -> PipelineResult:
    """Execute the full v2 pipeline on *text*.

    Parameters
    ----------
    text : str
        Raw Arabic input (may include tashkīl).
    world : WorldModel, optional
        An external world model for confidence adjustment.
    inference_engine : InferenceEngine, optional
        A rule engine for deriving new propositions.
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
    )
