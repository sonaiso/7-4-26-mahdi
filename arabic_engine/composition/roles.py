"""باب الأدوار — Composition role assignment (Articles 39–41).

Pure functions that assign and realize composition roles for units
within the syntactic structure.
"""

from __future__ import annotations

from arabic_engine.core.enums import POS, CompositionRoleType, RoleStatus
from arabic_engine.core.types import CompositionRole, CompositionUnit


def assign_role(
    unit: CompositionUnit,
    context: dict[str, str] | None = None,
) -> CompositionRole:
    """Assign a candidate role to *unit* based on POS and context.

    Parameters
    ----------
    unit:
        The composition unit.
    context:
        Optional hints, e.g. ``{"position": "subject"}``.
    """
    if context is None:
        context = {}

    role_type = _infer_role_type(unit, context)
    return CompositionRole(
        unit_id=unit.unit_id,
        role_type=role_type,
        status=RoleStatus.CANDIDATE,
        confidence=0.8 if unit.admitted else 0.3,
    )


def realize_role(candidate: CompositionRole) -> CompositionRole:
    """Transition a CANDIDATE role to REALIZED.

    Only transitions if the role is currently CANDIDATE.
    """
    if candidate.status == RoleStatus.REALIZED:
        return candidate
    return CompositionRole(
        unit_id=candidate.unit_id,
        role_type=candidate.role_type,
        status=RoleStatus.REALIZED,
        confidence=min(1.0, candidate.confidence + 0.1),
    )


# ── Internals ───────────────────────────────────────────────────────


def _infer_role_type(
    unit: CompositionUnit,
    context: dict[str, str],
) -> CompositionRoleType:
    """Heuristic inference of role type from POS and context."""
    position = context.get("position", "")

    if position == "subject" or (unit.pos == POS.ISM and position != "predicate"):
        return CompositionRoleType.MUSNAD_ILAYH

    if position == "predicate" or unit.pos == POS.FI3L:
        return CompositionRoleType.MUSNAD

    if unit.pos == POS.SIFA:
        return CompositionRoleType.TABI3

    if unit.pos == POS.HARF:
        return CompositionRoleType.RABIT

    if unit.pos == POS.ZARF:
        return CompositionRoleType.QAYD

    return CompositionRoleType.MUFASSIR
