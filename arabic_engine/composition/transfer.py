"""باب النقل — Semantic transfer detection and validation (Articles 14–17).

Pure functions that detect whether a lexeme/concept has shifted from
its original semantic direction to a transferred one, and validate the
transfer against the four conditions of Article 17.
"""

from __future__ import annotations

from arabic_engine.core.enums import TransferType
from arabic_engine.core.types import TransferRecord


def detect_transfer(
    unit_id: str,
    original: str,
    current: str,
    *,
    transfer_type: TransferType = TransferType.INTERNAL_LINGUISTIC,
) -> TransferRecord:
    """Detect whether a semantic transfer has occurred.

    Parameters
    ----------
    unit_id:
        Identifier for the lexeme/concept.
    original:
        The original semantic direction.
    current:
        The current/transferred semantic direction.
    transfer_type:
        Classification of the transfer.
    """
    if original == current:
        return TransferRecord(
            unit_id=unit_id,
            transfer_type=transfer_type,
            original_direction=original,
            transferred_direction=current,
            stability=1.0,
            accepted=True,
        )

    return TransferRecord(
        unit_id=unit_id,
        transfer_type=transfer_type,
        original_direction=original,
        transferred_direction=current,
        stability=0.0,
        accepted=False,
    )


def validate_transfer(record: TransferRecord) -> TransferRecord:
    """Validate a transfer against the four conditions (Article 17).

    Conditions:
    1. The original direction is identifiable.
    2. The transferred direction is identifiable.
    3. There is a recognisable relation between original and transferred.
    4. The transfer has a minimum stability threshold (≥ 0.5).
    """
    if record.accepted:
        return record

    conditions_met = 0
    total_conditions = 4

    # Condition 1: original direction identifiable
    if record.original_direction:
        conditions_met += 1

    # Condition 2: transferred direction identifiable
    if record.transferred_direction:
        conditions_met += 1

    # Condition 3: relation between original and transferred
    if record.original_direction and record.transferred_direction:
        conditions_met += 1

    # Condition 4: stability threshold
    if record.stability >= 0.5:
        conditions_met += 1

    stability = conditions_met / total_conditions
    accepted = conditions_met == total_conditions

    return TransferRecord(
        unit_id=record.unit_id,
        transfer_type=record.transfer_type,
        original_direction=record.original_direction,
        transferred_direction=record.transferred_direction,
        stability=stability,
        accepted=accepted,
    )
