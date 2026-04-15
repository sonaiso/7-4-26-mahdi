"""Tests for arabic_engine.cognition.epistemic_v1.

Covers the full ten-point validation, epistemic rank assignment,
linguistic-carrier validation, conflict resolution hints, and
batch validation ordering.
"""

from __future__ import annotations

from arabic_engine.cognition.epistemic_v1 import (
    DEFAULT_CONFLICT_RULE,
    SEED_METHODS,
    conflict_resolution_hint,
    validate_batch,
    validate_episode,
    validate_linguistic_carrier,
)
from arabic_engine.core.enums import (
    CarrierType,
    ContaminationLevel,
    DalalaType,
    EpistemicRank,
    GapSeverity,
    JudgementType,
    LinkKind,
    MethodFamily,
    ProofPathKind,
    RealityKind,
    SenseModality,
    TraceMode,
    ValidationState,
)
from arabic_engine.core.types import (
    ConceptRecord,
    ConflictRuleRecord,
    JudgementRecord,
    KnowledgeEpisodeInput,
    LinguisticCarrierRecord,
    LinkingTraceRecord,
    MethodRecord,
    OpinionTraceRecord,
    PriorInfoRecord,
    ProofPathRecord,
    RealityAnchorRecord,
    Self_,
    SenseTraceRecord,
    UtteranceRecord,
)

# ── Fixtures ────────────────────────────────────────────────────────


def _make_self() -> Self_:
    return Self_(id="self:test_1", self_kind="individual")


def _make_reality() -> RealityAnchorRecord:
    return RealityAnchorRecord(
        id="ra:001",
        reality_kind=RealityKind.TEXT_OBJECT,
        source_mode=TraceMode.DIRECT_PERCEPTION,
        anchoring_strength=5,
    )


def _make_sense() -> SenseTraceRecord:
    return SenseTraceRecord(
        id="st:001",
        sense_modality=SenseModality.VISION,
        trace_mode=TraceMode.DIRECT_PERCEPTION,
        trace_quality="strong",
    )


def _make_prior_infos() -> tuple[PriorInfoRecord, ...]:
    return (
        PriorInfoRecord(
            id="pi:001",
            info_kind="lexical",
            source="lexicon",
            is_verified=True,
        ),
    )


def _make_linking() -> LinkingTraceRecord:
    return LinkingTraceRecord(
        id="lt:001",
        link_kind=LinkKind.TEXTUAL_INFERENCE,
        step_count=2,
        is_explicit=True,
    )


def _make_judgement(
    jtype: JudgementType = JudgementType.EXISTENCE,
) -> JudgementRecord:
    return JudgementRecord(
        id="j:001",
        judgement_type=jtype,
        judgement_text="test judgement",
    )


def _make_method(
    family: MethodFamily = MethodFamily.RATIONAL,
) -> MethodRecord:
    return MethodRecord(
        id=f"method:{family.name.lower()}",
        method_family=family,
        requires_experiment=family is MethodFamily.SCIENTIFIC,
        requires_formal_proof=family is MethodFamily.MATHEMATICAL,
        requires_linguistic_anchor=family is MethodFamily.LINGUISTIC,
    )


def _make_utterance() -> UtteranceRecord:
    return UtteranceRecord(
        id="u:001",
        text_shakled="هٰذَا نَصٌّ",
        utterance_mode="nass",
        literal_scope="direct",
    )


def _make_concept() -> ConceptRecord:
    return ConceptRecord(
        id="c:001",
        concept_name="test_concept",
        dalaala_type=DalalaType.MUTABAQA,
        concept_scope="general",
    )


def _make_carrier(
    ctype: CarrierType = CarrierType.BOTH,
    utterance: UtteranceRecord | None = None,
    concept: ConceptRecord | None = None,
) -> LinguisticCarrierRecord:
    if ctype is CarrierType.BOTH:
        u = utterance or _make_utterance()
        c = concept or _make_concept()
    elif ctype is CarrierType.UTTERANCE:
        u = utterance or _make_utterance()
        c = concept  # may be None
    else:
        u = utterance  # may be None
        c = concept or _make_concept()
    return LinguisticCarrierRecord(
        id="lc:001", carrier_class=ctype, utterance=u, concept=c,
    )


def _make_proof(
    kind: ProofPathKind = ProofPathKind.AQLI,
) -> ProofPathRecord:
    return ProofPathRecord(
        id="pp:001",
        path_kind=kind,
        is_complete=True,
        step_count=3,
    )


def _make_conflict() -> ConflictRuleRecord:
    return DEFAULT_CONFLICT_RULE


def _make_episode(
    jtype: JudgementType = JudgementType.EXISTENCE,
    mfamily: MethodFamily = MethodFamily.RATIONAL,
    ctype: CarrierType = CarrierType.BOTH,
    ep_id: str = "ke:001",
) -> KnowledgeEpisode:
    return KnowledgeEpisode(
        id=ep_id,
        domain_profile="test",
        judgement_type=jtype,
        method_family=mfamily,
        method_ref=f"method:{mfamily.name.lower()}",
        carrier_type=ctype,
        validation_state=ValidationState.PENDING,
    )


def _make_full_input(
    jtype: JudgementType = JudgementType.EXISTENCE,
    mfamily: MethodFamily = MethodFamily.RATIONAL,
    ctype: CarrierType = CarrierType.BOTH,
    ep_id: str = "ke:001",
    proof_kind: ProofPathKind = ProofPathKind.AQLI,
    opinions: tuple[OpinionTraceRecord, ...] = (),
    reality: RealityAnchorRecord | None = None,
    sense: SenseTraceRecord | None = None,
    prior_infos: tuple[PriorInfoRecord, ...] | None = None,
    linking: LinkingTraceRecord | None = None,
    judgement: JudgementRecord | None = None,
    method: MethodRecord | None = None,
    carrier: LinguisticCarrierRecord | None = None,
    proof: ProofPathRecord | None = None,
    conflict: ConflictRuleRecord | None = None,
) -> KnowledgeEpisodeInput:
    return KnowledgeEpisodeInput(
        self_=_make_self(),
        episode=_make_episode(jtype, mfamily, ctype, ep_id),
        reality=reality if reality is not None else _make_reality(),
        sense=sense if sense is not None else _make_sense(),
        prior_infos=(
            prior_infos if prior_infos is not None else _make_prior_infos()
        ),
        linking=linking if linking is not None else _make_linking(),
        judgement=judgement if judgement is not None else _make_judgement(jtype),
        method=method if method is not None else _make_method(mfamily),
        carrier=carrier if carrier is not None else _make_carrier(ctype),
        proof=proof if proof is not None else _make_proof(proof_kind),
        conflict=conflict if conflict is not None else _make_conflict(),
        opinions=opinions,
    )


# ── Test: valid episode → CERTAIN ───────────────────────────────────


class TestValidEpisodeCertain:
    """A fully valid existence episode with aqli proof → CERTAIN."""

    def test_valid_existence_aqli(self):
        inp = _make_full_input(
            jtype=JudgementType.EXISTENCE,
            proof_kind=ProofPathKind.AQLI,
        )
        result = validate_episode(inp)
        assert result.validation_state is ValidationState.VALID
        assert result.epistemic_rank is EpistemicRank.CERTAIN
        assert len(result.errors) == 0
        assert len(result.gaps) == 0

    def test_valid_existence_hissi(self):
        inp = _make_full_input(
            jtype=JudgementType.EXISTENCE,
            proof_kind=ProofPathKind.HISSI,
        )
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.CERTAIN

    def test_valid_existence_formal(self):
        inp = _make_full_input(
            jtype=JudgementType.EXISTENCE,
            proof_kind=ProofPathKind.FORMAL,
        )
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.CERTAIN


# ── Test: valid episode → TRUE_NON_CERTAIN ──────────────────────────


class TestValidEpisodeTrueNonCertain:
    """Valid episode with interpretive judgement → TRUE_NON_CERTAIN."""

    def test_interpretive(self):
        inp = _make_full_input(jtype=JudgementType.INTERPRETIVE)
        result = validate_episode(inp)
        assert result.validation_state is ValidationState.VALID
        assert result.epistemic_rank is EpistemicRank.TRUE_NON_CERTAIN

    def test_essence(self):
        inp = _make_full_input(jtype=JudgementType.ESSENCE)
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.TRUE_NON_CERTAIN

    def test_attribute(self):
        inp = _make_full_input(jtype=JudgementType.ATTRIBUTE)
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.TRUE_NON_CERTAIN

    def test_relation(self):
        inp = _make_full_input(jtype=JudgementType.RELATION)
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.TRUE_NON_CERTAIN

    def test_causal(self):
        inp = _make_full_input(jtype=JudgementType.CAUSAL)
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.TRUE_NON_CERTAIN

    def test_formal(self):
        inp = _make_full_input(jtype=JudgementType.FORMAL)
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.TRUE_NON_CERTAIN


# ── Test: missing fields → REJECTED_METHODOLOGICALLY ────────────────


class TestMissingFieldsRejected:
    """Missing foundational checks cause REJECTED_METHODOLOGICALLY."""

    def test_missing_reality_anchor(self):
        inp = KnowledgeEpisodeInput(
            self_=_make_self(),
            episode=_make_episode(),
            reality=None,
            sense=_make_sense(),
            prior_infos=_make_prior_infos(),
            linking=_make_linking(),
            judgement=_make_judgement(),
            method=_make_method(),
            carrier=_make_carrier(),
            proof=_make_proof(),
            conflict=_make_conflict(),
        )
        result = validate_episode(inp)
        assert result.validation_state is ValidationState.INVALID
        assert result.epistemic_rank is EpistemicRank.REJECTED_METHODOLOGICALLY
        assert "Missing RealityAnchor" in result.errors
        # gap severity
        gap = next(g for g in result.gaps if g.gap_type == "Missing RealityAnchor")
        assert gap.severity is GapSeverity.FATAL

    def test_missing_sense_trace(self):
        inp = KnowledgeEpisodeInput(
            self_=_make_self(),
            episode=_make_episode(),
            reality=_make_reality(),
            sense=None,
            prior_infos=_make_prior_infos(),
            linking=_make_linking(),
            judgement=_make_judgement(),
            method=_make_method(),
            carrier=_make_carrier(),
            proof=_make_proof(),
            conflict=_make_conflict(),
        )
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.REJECTED_METHODOLOGICALLY
        assert "Missing SenseTrace" in result.errors

    def test_missing_prior_info(self):
        inp = _make_full_input(prior_infos=())
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.REJECTED_METHODOLOGICALLY
        assert "Missing PriorInfo" in result.errors

    def test_high_contamination_opinion(self):
        inp = _make_full_input(
            opinions=(
                OpinionTraceRecord(
                    id="ot:001",
                    contamination_level=ContaminationLevel.HIGH,
                    description="strong bias",
                ),
            ),
        )
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.REJECTED_METHODOLOGICALLY
        assert "Opinion contamination" in result.errors

    def test_medium_contamination_opinion(self):
        inp = _make_full_input(
            opinions=(
                OpinionTraceRecord(
                    id="ot:002",
                    contamination_level=ContaminationLevel.MEDIUM,
                    description="moderate bias",
                ),
            ),
        )
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.REJECTED_METHODOLOGICALLY

    def test_low_contamination_passes(self):
        inp = _make_full_input(
            opinions=(
                OpinionTraceRecord(
                    id="ot:003",
                    contamination_level=ContaminationLevel.LOW,
                    description="minor influence",
                ),
            ),
        )
        result = validate_episode(inp)
        assert result.validation_state is ValidationState.VALID


# ── Test: method-fit → IMPOSSIBLE ───────────────────────────────────


class TestMethodFitImpossible:
    """Scientific method with normative/pure_linguistic/metaphysical → IMPOSSIBLE."""

    def test_scientific_normative(self):
        inp = _make_full_input(
            jtype=JudgementType.NORMATIVE,
            mfamily=MethodFamily.SCIENTIFIC,
        )
        result = validate_episode(inp)
        assert result.validation_state is ValidationState.INVALID
        assert result.epistemic_rank is EpistemicRank.IMPOSSIBLE
        assert any("not suitable" in e for e in result.errors)

    def test_scientific_pure_linguistic(self):
        inp = _make_full_input(
            jtype=JudgementType.PURE_LINGUISTIC,
            mfamily=MethodFamily.SCIENTIFIC,
        )
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.IMPOSSIBLE

    def test_scientific_metaphysical(self):
        inp = _make_full_input(
            jtype=JudgementType.METAPHYSICAL,
            mfamily=MethodFamily.SCIENTIFIC,
        )
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.IMPOSSIBLE

    def test_scientific_existence_ok(self):
        inp = _make_full_input(
            jtype=JudgementType.EXISTENCE,
            mfamily=MethodFamily.SCIENTIFIC,
        )
        result = validate_episode(inp)
        assert result.validation_state is ValidationState.VALID


# ── Test: linguistic carrier mismatch ───────────────────────────────


class TestLinguisticCarrierMismatch:
    """carrier_class=UTTERANCE but no UtteranceRecord → invalid."""

    def test_utterance_class_no_utterance(self):
        carrier = LinguisticCarrierRecord(
            id="lc:bad",
            carrier_class=CarrierType.UTTERANCE,
            utterance=None,
            concept=_make_concept(),
        )
        inp = _make_full_input(
            ctype=CarrierType.UTTERANCE,
            carrier=carrier,
        )
        result = validate_episode(inp)
        assert result.validation_state is ValidationState.INVALID
        assert "Invalid LinguisticCarrier" in result.errors

    def test_concept_class_no_concept(self):
        carrier = LinguisticCarrierRecord(
            id="lc:bad2",
            carrier_class=CarrierType.CONCEPT,
            utterance=_make_utterance(),
            concept=None,
        )
        inp = _make_full_input(
            ctype=CarrierType.CONCEPT,
            carrier=carrier,
        )
        result = validate_episode(inp)
        assert "Invalid LinguisticCarrier" in result.errors

    def test_both_class_missing_concept(self):
        carrier = LinguisticCarrierRecord(
            id="lc:bad3",
            carrier_class=CarrierType.BOTH,
            utterance=_make_utterance(),
            concept=None,
        )
        inp = _make_full_input(
            ctype=CarrierType.BOTH,
            carrier=carrier,
        )
        result = validate_episode(inp)
        assert "Invalid LinguisticCarrier" in result.errors


# ── Test: validate_linguistic_carrier ───────────────────────────────


class TestValidateLinguisticCarrier:
    def test_utterance_ok(self):
        carrier = _make_carrier(CarrierType.UTTERANCE)
        assert validate_linguistic_carrier(
            "ke:001", carrier, carrier.utterance, carrier.concept,
        ) == "ok"

    def test_concept_ok(self):
        carrier = _make_carrier(CarrierType.CONCEPT)
        assert validate_linguistic_carrier(
            "ke:001", carrier, carrier.utterance, carrier.concept,
        ) == "ok"

    def test_both_ok(self):
        carrier = _make_carrier(CarrierType.BOTH)
        assert validate_linguistic_carrier(
            "ke:001", carrier, carrier.utterance, carrier.concept,
        ) == "ok"

    def test_none_carrier_invalid(self):
        assert validate_linguistic_carrier(
            "ke:001", None, None, None,
        ) == "invalid"

    def test_utterance_missing_record(self):
        carrier = LinguisticCarrierRecord(
            id="lc:x", carrier_class=CarrierType.UTTERANCE,
        )
        assert validate_linguistic_carrier(
            "ke:001", carrier, None, None,
        ) == "invalid"


# ── Test: conflict_resolution_hint ──────────────────────────────────


class TestConflictResolutionHint:
    def test_no_conflict_utterance_absent(self):
        hint = conflict_resolution_hint(
            "ke:001", None, _make_concept(), _make_reality(), _make_proof(),
        )
        assert hint == "no_internal_conflict_check"

    def test_no_conflict_concept_absent(self):
        hint = conflict_resolution_hint(
            "ke:001", _make_utterance(), None, _make_reality(), _make_proof(),
        )
        assert hint == "no_internal_conflict_check"

    def test_prefer_grounded(self):
        hint = conflict_resolution_hint(
            "ke:001",
            _make_utterance(),
            _make_concept(),
            _make_reality(),
            _make_proof(ProofPathKind.AQLI),
        )
        assert hint == "prefer_grounded_reading"

    def test_review_needed_no_reality(self):
        hint = conflict_resolution_hint(
            "ke:001",
            _make_utterance(),
            _make_concept(),
            None,
            _make_proof(ProofPathKind.AQLI),
        )
        assert hint == "review_needed"

    def test_review_needed_composite_proof(self):
        hint = conflict_resolution_hint(
            "ke:001",
            _make_utterance(),
            _make_concept(),
            _make_reality(),
            _make_proof(ProofPathKind.COMPOSITE),
        )
        assert hint == "review_needed"


# ── Test: batch validator ───────────────────────────────────────────


class TestBatchValidator:
    def test_ordering(self):
        inp_valid = _make_full_input(
            jtype=JudgementType.EXISTENCE, ep_id="ke:valid_001",
        )
        inp_invalid = _make_full_input(
            jtype=JudgementType.NORMATIVE,
            mfamily=MethodFamily.SCIENTIFIC,
            ep_id="ke:invalid_001",
        )
        inp_valid_2 = _make_full_input(
            jtype=JudgementType.INTERPRETIVE,
            ep_id="ke:valid_002",
        )
        results = validate_batch([inp_valid, inp_invalid, inp_valid_2])
        assert len(results) == 3
        # Invalid comes first
        assert results[0].validation_state is ValidationState.INVALID
        # Valid ones come after
        assert results[1].validation_state is ValidationState.VALID
        assert results[2].validation_state is ValidationState.VALID

    def test_batch_empty(self):
        assert validate_batch([]) == []


# ── Test: seed constants ────────────────────────────────────────────


class TestSeedConstants:
    def test_seed_methods_count(self):
        assert len(SEED_METHODS) == 5

    def test_seed_method_families(self):
        families = {m.method_family for m in SEED_METHODS}
        assert families == {
            MethodFamily.RATIONAL,
            MethodFamily.SCIENTIFIC,
            MethodFamily.LINGUISTIC,
            MethodFamily.MATHEMATICAL,
            MethodFamily.PHYSICAL,
        }

    def test_default_conflict_rule(self):
        assert DEFAULT_CONFLICT_RULE.rule_name == "default_conflict_v1"
        assert DEFAULT_CONFLICT_RULE.action_on_conflict == "downgrade_or_reject"


# ── Test: gap record fields ─────────────────────────────────────────


class TestGapRecordFields:
    def test_gap_has_correct_id_format(self):
        inp = KnowledgeEpisodeInput(
            self_=_make_self(),
            episode=_make_episode(ep_id="ke:gap_test"),
            reality=None,
            sense=_make_sense(),
            prior_infos=_make_prior_infos(),
            linking=_make_linking(),
            judgement=_make_judgement(),
            method=_make_method(),
            carrier=_make_carrier(),
            proof=_make_proof(),
            conflict=_make_conflict(),
        )
        result = validate_episode(inp)
        gap = result.gaps[0]
        assert gap.id == "ke:gap_test::Missing_RealityAnchor"
        assert gap.gap_type == "Missing RealityAnchor"
        assert gap.severity is GapSeverity.FATAL


# ── Test: missing method / proof / conflict ─────────────────────────


class TestMissingOptionalParts:
    def test_missing_method(self):
        inp = _make_full_input(method=MethodRecord(
            id="dummy", method_family=MethodFamily.RATIONAL,
            requires_experiment=False, requires_formal_proof=False,
            requires_linguistic_anchor=False,
        ))
        # Replace method with None manually
        inp2 = KnowledgeEpisodeInput(
            self_=inp.self_,
            episode=inp.episode,
            reality=inp.reality,
            sense=inp.sense,
            prior_infos=inp.prior_infos,
            linking=inp.linking,
            judgement=inp.judgement,
            method=None,
            carrier=inp.carrier,
            proof=inp.proof,
            conflict=inp.conflict,
            opinions=inp.opinions,
        )
        result = validate_episode(inp2)
        assert "Missing MethodFit" in result.errors

    def test_missing_proof(self):
        inp2 = KnowledgeEpisodeInput(
            self_=_make_self(),
            episode=_make_episode(),
            reality=_make_reality(),
            sense=_make_sense(),
            prior_infos=_make_prior_infos(),
            linking=_make_linking(),
            judgement=_make_judgement(),
            method=_make_method(),
            carrier=_make_carrier(),
            proof=None,
            conflict=_make_conflict(),
        )
        result = validate_episode(inp2)
        assert "Missing ProofPath" in result.errors

    def test_missing_conflict(self):
        inp2 = KnowledgeEpisodeInput(
            self_=_make_self(),
            episode=_make_episode(),
            reality=_make_reality(),
            sense=_make_sense(),
            prior_infos=_make_prior_infos(),
            linking=_make_linking(),
            judgement=_make_judgement(),
            method=_make_method(),
            carrier=_make_carrier(),
            proof=_make_proof(),
            conflict=None,
        )
        result = validate_episode(inp2)
        assert "Missing ConflictRule" in result.errors


# ── Test: existence with composite proof → PROBABILISTIC_DOUBT ──────


class TestProbabilisticDoubt:
    def test_existence_composite_proof(self):
        inp = _make_full_input(
            jtype=JudgementType.EXISTENCE,
            proof_kind=ProofPathKind.COMPOSITE,
        )
        result = validate_episode(inp)
        assert result.validation_state is ValidationState.VALID
        # COMPOSITE is not in the CERTAIN proof kinds
        assert result.epistemic_rank is EpistemicRank.PROBABILISTIC_DOUBT

    def test_existence_linguistic_proof(self):
        inp = _make_full_input(
            jtype=JudgementType.EXISTENCE,
            proof_kind=ProofPathKind.LINGUISTIC,
        )
        result = validate_episode(inp)
        assert result.epistemic_rank is EpistemicRank.PROBABILISTIC_DOUBT
