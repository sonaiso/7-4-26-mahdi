"""باب القضية — Proposition builder (Articles 42–44).

Pure functions that assemble composition propositions from predication,
roles, restrictions, dependencies, and relations; validate closure
conditions; and classify proposition types.
"""

from __future__ import annotations

import uuid

from arabic_engine.core.enums import PropositionType, RoleStatus
from arabic_engine.core.types import (
    CompositionProposition,
    CompositionRelation,
    CompositionRole,
    DependencyRecord,
    PredicationRecord,
    RestrictionRecord,
)


def build_proposition(
    predication: PredicationRecord,
    roles: tuple[CompositionRole, ...] = (),
    restrictions: tuple[RestrictionRecord, ...] = (),
    dependencies: tuple[DependencyRecord, ...] = (),
    relations: tuple[CompositionRelation, ...] = (),
) -> CompositionProposition:
    """Build a composition proposition from its components.

    The proposition starts as unclosed (``closed=False``).
    """
    prop_type = classify_proposition_from_predication(predication, roles)
    return CompositionProposition(
        proposition_id=f"P_{uuid.uuid4().hex[:8]}",
        proposition_type=prop_type,
        predication=predication,
        roles=roles,
        restrictions=restrictions,
        dependencies=dependencies,
        relations=relations,
        closed=False,
        confidence=predication.confidence if predication.valid else 0.0,
    )


def close_proposition(
    prop: CompositionProposition,
) -> CompositionProposition:
    """Validate closure conditions and close the proposition (Article 43).

    Closure requires:
    1. Valid predication.
    2. At least one realized role.
    3. All restrictions valid.
    4. All dependencies valid.
    """
    if prop.predication is None or not prop.predication.valid:
        return prop  # Cannot close without valid predication

    has_realized = any(
        r.status == RoleStatus.REALIZED for r in prop.roles
    )
    restrictions_ok = all(r.valid for r in prop.restrictions)
    deps_ok = all(d.valid for d in prop.dependencies)

    if has_realized and restrictions_ok and deps_ok:
        return CompositionProposition(
            proposition_id=prop.proposition_id,
            proposition_type=prop.proposition_type,
            predication=prop.predication,
            roles=prop.roles,
            restrictions=prop.restrictions,
            dependencies=prop.dependencies,
            relations=prop.relations,
            closed=True,
            confidence=prop.confidence,
        )
    return prop


def classify_proposition(
    prop: CompositionProposition,
) -> PropositionType:
    """Classify the proposition type from its structure."""
    return prop.proposition_type


def classify_proposition_from_predication(
    predication: PredicationRecord,
    roles: tuple[CompositionRole, ...] = (),
) -> PropositionType:
    """Classify proposition type from predication and roles."""
    if predication.predication_type == "essential/eventive":
        return PropositionType.VERBAL
    if predication.predication_type.startswith("essential/"):
        return PropositionType.NOMINAL
    # Check for copular pattern
    if any(r.role_type.name == "RABIT" for r in roles):
        return PropositionType.COPULAR
    return PropositionType.NOMINAL
