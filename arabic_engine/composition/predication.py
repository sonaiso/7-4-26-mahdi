"""باب الإسناد — Predication builder (Articles 26–29).

Pure functions that construct and classify predication records
connecting musnad_ilayh (المسند إليه) to musnad (المسند).
"""

from __future__ import annotations

from arabic_engine.core.enums import POS
from arabic_engine.core.types import CompositionUnit, PredicationRecord

# Valid predication sub-types
_PREDICATION_TYPES = (
    "essential/descriptive",
    "essential/eventive",
    "essential/existential",
)


def build_predication(
    musnad_ilayh: CompositionUnit,
    musnad: CompositionUnit,
) -> PredicationRecord:
    """Build a predication record from two composition units.

    Parameters
    ----------
    musnad_ilayh:
        The subject/topic unit (المسند إليه).
    musnad:
        The predicate/comment unit (المسند).

    Returns
    -------
    PredicationRecord
        Valid if both units are admitted; predication_type is
        auto-classified.
    """
    valid = musnad_ilayh.admitted and musnad.admitted
    pred_type = classify_predication_type(musnad_ilayh, musnad)

    return PredicationRecord(
        musnad_ilayh_id=musnad_ilayh.unit_id,
        musnad_id=musnad.unit_id,
        predication_type=pred_type,
        valid=valid,
        confidence=0.9 if valid else 0.0,
    )


def classify_predication(record: PredicationRecord) -> str:
    """Return the predication sub-type label."""
    return record.predication_type


def classify_predication_type(
    musnad_ilayh: CompositionUnit,
    musnad: CompositionUnit,
) -> str:
    """Auto-classify predication sub-type from unit POS/semantics."""
    if musnad.pos == POS.FI3L:
        return "essential/eventive"
    if musnad.pos == POS.SIFA:
        return "essential/descriptive"
    return "essential/existential"
