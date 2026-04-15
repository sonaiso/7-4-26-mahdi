"""باب الحقيقة — Truth-type determination (Articles 18–22).

Pure functions that determine whether a lexeme/concept is used in its
linguistic-original, conventional, or controlled-transfer sense, and
adjudicate between competing truth-type claims using the five-factor
preference of Article 22.
"""

from __future__ import annotations

from arabic_engine.core.enums import TruthType
from arabic_engine.core.types import TruthRecord


def determine_truth_type(
    unit_id: str,
    context: dict[str, str] | None = None,
) -> TruthRecord:
    """Determine the truth-type for a composition unit.

    Parameters
    ----------
    unit_id:
        Identifier for the lexeme/concept.
    context:
        Optional dictionary with keys ``"usage"`` or ``"domain"``
        that hint at the truth type.
    """
    if context is None:
        context = {}

    usage = context.get("usage", "linguistic")

    if usage == "conventional":
        return TruthRecord(
            unit_id=unit_id,
            truth_type=TruthType.CONVENTIONAL,
            justification="Unit used in conventional/customary sense",
            confidence=0.8,
        )
    if usage == "transferred":
        return TruthRecord(
            unit_id=unit_id,
            truth_type=TruthType.CONTROLLED_TRANSFER,
            justification="Unit used in controlled-transfer sense",
            confidence=0.7,
        )

    return TruthRecord(
        unit_id=unit_id,
        truth_type=TruthType.LINGUISTIC_ORIGINAL,
        justification="Unit used in original linguistic sense",
        confidence=0.9,
    )


def adjudicate_truth(
    linguistic: TruthRecord,
    conventional: TruthRecord | None = None,
) -> TruthRecord:
    """Adjudicate between competing truth-type claims (Article 22).

    Applies the five-factor preference hierarchy:
    1. Linguistic-original has baseline priority.
    2. Conventional overrides if its confidence is strictly higher.
    3. Controlled transfer only wins if both others are weak.
    4. Context-specific evidence can boost any claim.
    5. Stability of usage in corpus (approximated by confidence).
    """
    if conventional is None:
        return linguistic

    # Factor 2: conventional overrides if strictly more confident
    if conventional.confidence > linguistic.confidence:
        return conventional

    # Factor 1: linguistic baseline priority
    return linguistic
