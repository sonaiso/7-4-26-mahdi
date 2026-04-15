"""باب التبعية — Dependency builder (Articles 33–35).

Pure functions that construct and validate follower–principal dependency
records (نعت، بدل، توكيد، عطف).
"""

from __future__ import annotations

from arabic_engine.core.types import CompositionUnit, DependencyRecord

# Known dependency kinds
DEPENDENCY_KINDS = ("na3t", "badal", "tawkid", "3atf")


def build_dependency(
    principal: CompositionUnit,
    follower: CompositionUnit,
    kind: str,
    *,
    dependency_face: str = "",
) -> DependencyRecord:
    """Build a dependency record.

    Parameters
    ----------
    principal:
        The principal (المتبوع) unit.
    follower:
        The follower (التابع) unit.
    kind:
        One of ``na3t``, ``badal``, ``tawkid``, ``3atf``.
    dependency_face:
        Optional aspect of following.
    """
    valid = (
        principal.admitted
        and follower.admitted
        and kind in DEPENDENCY_KINDS
    )
    return DependencyRecord(
        principal_id=principal.unit_id,
        follower_id=follower.unit_id,
        dependency_kind=kind,
        dependency_face=dependency_face,
        valid=valid,
    )


def validate_dependency(record: DependencyRecord) -> bool:
    """Return whether a dependency record is valid."""
    return record.valid and record.dependency_kind in DEPENDENCY_KINDS
