"""Main pipeline — orchestrates all layers of the Arabic engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from arabic_engine.cognition.epistemic_v1 import validate_episode
from arabic_engine.cognition.evaluation import build_proposition, evaluate
from arabic_engine.cognition.explanation import build_explanation
from arabic_engine.cognition.inference_rules import InferenceEngine
from arabic_engine.cognition.isg_v1 import govern as isg_govern
from arabic_engine.cognition.isg_v1 import identify_atom as _isg_identify
from arabic_engine.cognition.time_space import tag as time_space_tag
from arabic_engine.cognition.world_model import WorldModel
from arabic_engine.core.contracts import verify_contracts  # noqa: F401 — re-export
from arabic_engine.core.enums import (
    CarrierType,
    ConfirmationRank,
    EpistemicEntryKind,
    JudgementType,
    KnowledgeAtomType,
    LinkKind,
    MethodFamily,
    ProofPathKind,
    RealityKind,
    SenseModality,
    SourceType,
    TraceMode,
    ValidationOutcome,
    ValidationState,
)
from arabic_engine.core.types import (
    Concept,
    ConceptNode,
    ConceptRecord,
    ConflictRuleRecord,
    DalalaLink,
    EvalResult,
    EvaluationResult,
    InferenceResult,
    ISGValidationResult,
    JudgementRecord,
    KnowledgeEpisode,
    KnowledgeEpisodeInput,
    LayerTraceRecord,
    LexicalClosure,
    LinguisticCarrierRecord,
    LinkingTraceRecord,
    LinkOperation,
    MethodRecord,
    PerceptTrace,
    PriorInfoRecord,
    PriorKnowledgeUnit,
    ProofPathRecord,
    Proposition,
    RealityAnchorRecord,
    ReferenceRecord,
    SenseTraceRecord,
    SyntaxNode,
    TimeSpaceTag,
    WordZeroCoverageReport,
)
from arabic_engine.linkage.dalala import full_validation
from arabic_engine.linkage.semantic_roles import derive_semantic_roles
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
    percept_trace: PerceptTrace
    prior_knowledge: List[PriorKnowledgeUnit]
    link_operations: List[LinkOperation]
    concept_nodes: List[ConceptNode]
    semantic_roles: Dict[str, str]
    knowledge_episode: KnowledgeEpisode
    evaluation_result: EvaluationResult
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

    # L2b — Optional strict 7-layer element analysis
    layer_traces: List[LayerTraceRecord] = []
    if analyze_layers:
        from arabic_engine.layers.layer_pipeline import analyze_word as _analyze_word
        from arabic_engine.signifier.root_pattern import extract_root_pattern

        for closure in closures:
            rp = extract_root_pattern(closure.surface)
            traces = _analyze_word(closure.surface, root_pattern=rp)
            layer_traces.extend(traces)

    # L3 — Syntax (v2)
    syntax_nodes = syntax_analyse(closures)

    # L4 — Ontological Mapping
    concepts = batch_map(closures)

    # L4b — Optional reference analysis
    reference_records: List[ReferenceRecord] = []
    if analyze_reference:
        from arabic_engine.signified.reference_v1 import batch_build as _ref_batch_build

        reference_records = _ref_batch_build(closures, concepts)

    # L5 — Dalāla Validation
    links = full_validation(closures, concepts)

    # L6 — Judgment
    proposition = build_proposition(closures, concepts, links)

    # L7 — Time/Space (v2)
    ts_tag = time_space_tag(closures, proposition)

    # L7b — Semantic roles
    semantic_roles = derive_semantic_roles(closures, syntax_nodes)

    # L8 — Evaluation
    eval_result = evaluate(proposition, links)

    # L8b — Build epistemic knowledge episode
    episode = _build_knowledge_episode(text, proposition, semantic_roles)
    episode_input = KnowledgeEpisodeInput(
        episode_id=episode.episode_id,
        reality_anchor=episode.reality_anchor,
        sense_trace=episode.sense_trace,
        prior_infos=episode.prior_infos,
        opinion_traces=episode.opinion_traces,
        linking_trace=episode.linking_trace,
        judgement=episode.judgement,
        method=episode.method,
        carrier=episode.carrier,
        proof_path=episode.proof_path,
        conflict_rule=episode.conflict_rule,
    )
    validation = validate_episode(episode_input)
    validation_state = _to_validation_state(validation.outcome)
    evaluation_result = EvaluationResult(
        truth_state=eval_result.truth_state,
        epistemic_rank=validation.rank,
        confidence=eval_result.confidence,
        validation_state=validation_state,
        consistency="; ".join(validation.messages),
    )

    # L9 — Inference (v2)
    inferences: List[InferenceResult] = []
    if inference_engine is not None:
        inferences = inference_engine.run([proposition])

    # L10 — World-Model adjustment (v2)
    adjustment = 0.5
    world_update: Dict[str, object] = {
        "applied": False,
        "reason": "no_world_model",
        "fact_id": None,
    }
    if world is not None:
        adjustment = world.confidence_adjustment(proposition)
        # Blend world-model confidence with dalāla confidence
        eval_result.confidence = round(
            eval_result.confidence * adjustment, 4
        )
        evaluation_result = EvaluationResult(
            truth_state=evaluation_result.truth_state,
            epistemic_rank=evaluation_result.epistemic_rank,
            confidence=eval_result.confidence,
            validation_state=evaluation_result.validation_state,
            consistency=evaluation_result.consistency,
        )
        world_update = world.apply_validated_proposition(
            proposition,
            validation_state=evaluation_result.validation_state,
            source="pipeline.v3",
        )

    explanation = build_explanation(
        proposition=proposition,
        semantic_roles=semantic_roles,
        evaluation=evaluation_result,
        inferences=inferences,
        world_update=world_update,
    )

    link_operations = [
        LinkOperation(
            operation_id=f"LO_{idx}",
            operation_type=link.dalala_type,
            source=link.source_lemma,
            target=str(link.target_concept_id),
            accepted=link.accepted,
            confidence=link.confidence,
        )
        for idx, link in enumerate(links, start=1)
    ]
    concept_nodes = [
        ConceptNode(
            concept_id=f"C_{concept.concept_id}",
            label=concept.label,
            semantic_type=concept.semantic_type,
            properties=concept.properties,
        )
        for concept in concepts
    ]
    prior_knowledge = [
        PriorKnowledgeUnit(
            unit_id=f"PK_{idx}",
            content=f"Token '{cl.surface}' -> lemma '{cl.lemma}'",
            source="lexical_closure",
            weight=cl.confidence,
        )
        for idx, cl in enumerate(closures, start=1)
    ]
    percept_trace = PerceptTrace(
        raw_text=text,
        normalized_text=normalised,
        tokens=tuple(tokens),
        trace_quality=1.0 if tokens else 0.0,
    )

    # L-ISG — Informational Stock Governance (ISG Constitution v1)
    isg_atoms = []
    for pk in prior_knowledge:
        try:
            atom = _isg_identify(
                label=pk.content,
                atom_type=KnowledgeAtomType.LEXICAL,
                knowledge_level="token",
                domain="linguistic",
                source=pk.source,
                source_type=SourceType.PRIMARY,
                confirmation_rank=ConfirmationRank.ESTABLISHED,
                context=normalised,
                entry_kind=EpistemicEntryKind.INFORMATION,
            )
            isg_atoms.append(atom)
        except ValueError:
            pass
    isg_result: Optional[ISGValidationResult] = None
    if isg_atoms:
        isg_result = isg_govern(
            isg_atoms,
            input_id=f"pipeline:{normalised[:40]}",
            input_level="token",
            input_domain="linguistic",
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
        percept_trace=percept_trace,
        prior_knowledge=prior_knowledge,
        link_operations=link_operations,
        concept_nodes=concept_nodes,
        semantic_roles=semantic_roles,
        knowledge_episode=episode,
        evaluation_result=evaluation_result,
        inferences=inferences,
        world_adjustment=adjustment,
        word_zero_coverage=zero_coverage,
    )
