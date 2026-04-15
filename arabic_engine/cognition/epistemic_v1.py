"""Epistemic v1 — Knowledge Episode Validator.

Pure-function module that validates knowledge episodes against the
ten-point epistemological framework.  No database dependency — all
logic mirrors the Cypher validators in ``db/validate_episode.cypher``
but operates on in-memory dataclass records.

Public API
----------
validate_episode(inp)                → ValidationResult
validate_linguistic_carrier(...)     → str
conflict_resolution_hint(...)        → str
validate_batch(inputs)               → List[ValidationResult]

Constants
---------
SEED_METHODS            → Tuple[MethodRecord, ...]
DEFAULT_CONFLICT_RULE   → ConflictRuleRecord
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from arabic_engine.core.enums import (
    CarrierType,
    ContaminationLevel,
    EpistemicRank,
    GapSeverity,
    JudgementType,
    MethodFamily,
    ProofPathKind,
    ValidationState,
)
from arabic_engine.core.types import (
    ConflictRuleRecord,
    GapRecord,
    KnowledgeEpisodeInput,
    LinguisticCarrierRecord,
    MethodRecord,
    ProofPathRecord,
    RealityAnchorRecord,
    UtteranceRecord,
    ValidationResult,
)

# ── Seed constants ──────────────────────────────────────────────────

SEED_METHODS: Tuple[MethodRecord, ...] = (
    MethodRecord(
        id="method:rational",
        method_family=MethodFamily.RATIONAL,
        requires_experiment=False,
        requires_formal_proof=False,
        requires_linguistic_anchor=False,
    ),
    MethodRecord(
        id="method:scientific",
        method_family=MethodFamily.SCIENTIFIC,
        requires_experiment=True,
        requires_formal_proof=False,
        requires_linguistic_anchor=False,
    ),
    MethodRecord(
        id="method:linguistic",
        method_family=MethodFamily.LINGUISTIC,
        requires_experiment=False,
        requires_formal_proof=False,
        requires_linguistic_anchor=True,
    ),
    MethodRecord(
        id="method:mathematical",
        method_family=MethodFamily.MATHEMATICAL,
        requires_experiment=False,
        requires_formal_proof=True,
        requires_linguistic_anchor=False,
    ),
    MethodRecord(
        id="method:physical",
        method_family=MethodFamily.PHYSICAL,
        requires_experiment=True,
        requires_formal_proof=True,
        requires_linguistic_anchor=False,
    ),
)

DEFAULT_CONFLICT_RULE = ConflictRuleRecord(
    id="conflict:default",
    rule_name="default_conflict_v1",
    priority_order=(
        "Reality > Valid Proof > Concept specialization"
        " > Utterance > Suspend"
    ),
    action_on_conflict="downgrade_or_reject",
)


# ── Internal helpers ────────────────────────────────────────────────

_FATAL_ERRORS = frozenset({
    "Missing RealityAnchor",
    "Missing SenseTrace",
    "Missing PriorInfo",
    "Invalid LinguisticCarrier",
})

_CONTAMINATION_BLOCKING = frozenset({
    ContaminationLevel.MEDIUM,
    ContaminationLevel.HIGH,
})

_METHOD_FIT_BLOCKED_JUDGEMENTS = frozenset({
    JudgementType.NORMATIVE,
    JudgementType.PURE_LINGUISTIC,
    JudgementType.METAPHYSICAL,
})

_CERTAIN_PROOF_KINDS = frozenset({
    ProofPathKind.HISSI,
    ProofPathKind.AQLI,
    ProofPathKind.FORMAL,
})

_TRUE_NON_CERTAIN_JUDGEMENTS = frozenset({
    JudgementType.ESSENCE,
    JudgementType.ATTRIBUTE,
    JudgementType.RELATION,
    JudgementType.CAUSAL,
    JudgementType.INTERPRETIVE,
    JudgementType.FORMAL,
})


def _gap_severity(error: str) -> GapSeverity:
    """Return the severity level for a given error string."""
    if error in _FATAL_ERRORS:
        return GapSeverity.FATAL
    if error == "Opinion contamination":
        return GapSeverity.HIGH
    return GapSeverity.MEDIUM


def _collect_errors(inp: KnowledgeEpisodeInput) -> List[str]:
    """Run the ten-point check and return a list of error strings."""
    errors: List[str] = []

    # 1. Reality anchor
    if inp.reality is None:
        errors.append("Missing RealityAnchor")

    # 2. Sense trace
    if inp.sense is None:
        errors.append("Missing SenseTrace")

    # 3. Prior info
    if len(inp.prior_infos) == 0:
        errors.append("Missing PriorInfo")

    # 4. Opinion contamination
    if any(
        o.contamination_level in _CONTAMINATION_BLOCKING
        for o in inp.opinions
    ):
        errors.append("Opinion contamination")

    # 5. Linking trace
    if inp.linking is None:
        errors.append("Missing LinkingTrace")

    # 6. Judgement type
    if inp.judgement is None or inp.episode.judgement_type is None:
        errors.append("Missing JudgementType")

    # 7. Method + method-fit
    if inp.method is None:
        errors.append("Missing MethodFit")
    elif (
        inp.method.method_family is MethodFamily.SCIENTIFIC
        and inp.episode.judgement_type in _METHOD_FIT_BLOCKED_JUDGEMENTS
    ):
        errors.append(
            "MethodFit failed: scientific method not suitable"
        )

    # 8. Linguistic carrier
    carrier = inp.carrier
    if carrier is None:
        errors.append("Invalid LinguisticCarrier")
    elif inp.episode.carrier_type not in (
        CarrierType.UTTERANCE,
        CarrierType.CONCEPT,
        CarrierType.BOTH,
    ):
        errors.append("Invalid LinguisticCarrier")
    else:
        lc_status = validate_linguistic_carrier(
            inp.episode.id,
            carrier,
            carrier.utterance,
            carrier.concept,
        )
        if lc_status != "ok":
            errors.append("Invalid LinguisticCarrier")

    # 9. Proof path
    if inp.proof is None:
        errors.append("Missing ProofPath")

    # 10. Conflict rule
    if inp.conflict is None:
        errors.append("Missing ConflictRule")

    return errors


def _assign_rank(
    errors: List[str],
    judgement_type: Optional[JudgementType],
    proof: Optional[ProofPathRecord],
) -> EpistemicRank:
    """Assign the epistemic rank based on collected errors."""
    # REJECTED_METHODOLOGICALLY
    if any(e in _FATAL_ERRORS or e == "Opinion contamination" for e in errors):
        return EpistemicRank.REJECTED_METHODOLOGICALLY

    # IMPOSSIBLE
    if any("Conflict" in e or "not suitable" in e for e in errors):
        return EpistemicRank.IMPOSSIBLE

    # CERTAIN
    if (
        len(errors) == 0
        and judgement_type is JudgementType.EXISTENCE
        and proof is not None
        and proof.path_kind in _CERTAIN_PROOF_KINDS
    ):
        return EpistemicRank.CERTAIN

    # TRUE_NON_CERTAIN
    if (
        len(errors) == 0
        and judgement_type in _TRUE_NON_CERTAIN_JUDGEMENTS
    ):
        return EpistemicRank.TRUE_NON_CERTAIN

    return EpistemicRank.PROBABILISTIC_DOUBT


# ── Public API ──────────────────────────────────────────────────────


def validate_episode(inp: KnowledgeEpisodeInput) -> ValidationResult:
    """Validate a single knowledge episode.

    Runs the full ten-point check:

    1. Reality anchor present
    2. Sense trace present
    3. At least one prior info present
    4. No medium/high contamination opinion
    5. Linking trace present
    6. Judgement type set
    7. Method present and method-fit check
    8. Linguistic carrier valid
    9. Proof path present
    10. Conflict rule present

    Returns a :class:`ValidationResult` with the validation state,
    epistemic rank, list of errors, and gap records.
    """
    errors = _collect_errors(inp)

    validation_state = (
        ValidationState.VALID if len(errors) == 0 else ValidationState.INVALID
    )

    epistemic_rank = _assign_rank(
        errors,
        inp.episode.judgement_type,
        inp.proof,
    )

    gaps = tuple(
        GapRecord(
            id=f"{inp.episode.id}::{e.replace(' ', '_')}",
            gap_type=e,
            message=e,
            severity=_gap_severity(e),
        )
        for e in errors
    )

    return ValidationResult(
        episode_id=inp.episode.id,
        validation_state=validation_state,
        epistemic_rank=epistemic_rank,
        errors=tuple(errors),
        gaps=gaps,
    )


def validate_linguistic_carrier(
    episode_id: str,
    carrier: Optional[LinguisticCarrierRecord],
    utterance: Optional[UtteranceRecord],
    concept: Optional["ConceptRecord"],  # noqa: F821 — forward ref
) -> str:
    """Validate the linguistic carrier configuration.

    Returns ``"ok"`` when the carrier class matches the realised
    sub-records, or ``"invalid"`` otherwise.

    Rules:
    * ``UTTERANCE`` → utterance must be present
    * ``CONCEPT``   → concept must be present
    * ``BOTH``      → both must be present
    """
    if carrier is None:
        return "invalid"

    cc = carrier.carrier_class
    if cc is CarrierType.UTTERANCE and utterance is not None:
        return "ok"
    if cc is CarrierType.CONCEPT and concept is not None:
        return "ok"
    if (
        cc is CarrierType.BOTH
        and utterance is not None
        and concept is not None
    ):
        return "ok"

    return "invalid"


def conflict_resolution_hint(
    episode_id: str,
    utterance: Optional[UtteranceRecord],
    concept: Optional["ConceptRecord"],  # noqa: F821
    reality: Optional[RealityAnchorRecord],
    proof: Optional[ProofPathRecord],
) -> str:
    """Return a conflict-resolution hint for utterance/concept tension.

    Returns one of:
    * ``"no_internal_conflict_check"`` — no conflict possible (one is absent)
    * ``"prefer_grounded_reading"`` — grounded in reality + strong proof
    * ``"review_needed"`` — manual review required
    """
    if utterance is None or concept is None:
        return "no_internal_conflict_check"

    if (
        proof is not None
        and proof.path_kind in _CERTAIN_PROOF_KINDS
        and reality is not None
    ):
        return "prefer_grounded_reading"

    return "review_needed"


def validate_batch(
    inputs: List[KnowledgeEpisodeInput],
) -> List[ValidationResult]:
    """Validate a list of knowledge episodes.

    Returns results sorted by validation_state, then epistemic_rank,
    then episode_id — matching the Cypher batch query ordering.
    """
    results = [validate_episode(inp) for inp in inputs]

    _state_order = {
        ValidationState.INVALID: 0,
        ValidationState.PENDING: 1,
        ValidationState.VALID: 2,
    }
    _rank_order = {
        EpistemicRank.CERTAIN: 0,
        EpistemicRank.TRUE_NON_CERTAIN: 1,
        EpistemicRank.PROBABILISTIC_DOUBT: 2,
        EpistemicRank.IMPOSSIBLE: 3,
        EpistemicRank.REJECTED_METHODOLOGICALLY: 4,
    }

    results.sort(
        key=lambda r: (
            _state_order.get(r.validation_state, 99),
            _rank_order.get(r.epistemic_rank, 99),
            r.episode_id,
        )
    )
    return results
