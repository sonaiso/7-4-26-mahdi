"""باب التقييد — Restriction builder (Articles 30–32).

Pure functions that construct and validate restriction records
representing qualifier/narrowing relations on base units.
"""

from __future__ import annotations

from arabic_engine.core.types import CompositionUnit, RestrictionRecord

# Known restriction kinds
RESTRICTION_KINDS = (
    "description",
    "adverb",
    "hal",
    "tamyiz",
    "idafa",
    "number",
)


def build_restriction(
    base: CompositionUnit,
    qualifier: CompositionUnit,
    *,
    restriction_kind: str = "description",
) -> RestrictionRecord:
    """Build a restriction record.

    Parameters
    ----------
    base:
        The restricted (base) unit.
    qualifier:
        The restricting (qualifier) unit.
    restriction_kind:
        Classification of the restriction.
    """
    valid = (
        base.admitted
        and qualifier.admitted
        and restriction_kind in RESTRICTION_KINDS
    )
    return RestrictionRecord(
        base_id=base.unit_id,
        qualifier_id=qualifier.unit_id,
        restriction_kind=restriction_kind,
        valid=valid,
    )


def validate_restriction(record: RestrictionRecord) -> bool:
    """Return whether a restriction is valid."""
    return record.valid and record.restriction_kind in RESTRICTION_KINDS
