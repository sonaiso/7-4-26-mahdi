"""باب التعارض — Semantic conflict detection and resolution (Articles 10–13).

Pure functions that detect pre-composition conflicts between competing
predicates, roles, or semantic directions, and resolve them via the
five-rule hierarchy of Article 13.
"""

from __future__ import annotations

from arabic_engine.core.enums import ConflictResolutionMethod, ConflictType
from arabic_engine.core.types import SemanticConflictRecord


def detect_conflict(
    unit_id: str,
    competing_predicates: tuple[str, str],
    *,
    conflict_type: ConflictType = ConflictType.ESSENTIAL_VS_DESCRIPTIVE,
) -> SemanticConflictRecord:
    """Detect a semantic conflict for a composition unit.

    Parameters
    ----------
    unit_id:
        Identifier for the lexeme/concept.
    competing_predicates:
        The two competing semantic directions.
    conflict_type:
        The classification of the conflict.
    """
    return SemanticConflictRecord(
        unit_id=unit_id,
        conflict_type=conflict_type,
        conflicting_pair=competing_predicates,
        resolution=ConflictResolutionMethod.BLOCK_COMPOSITION,
        resolved=False,
        notes="",
    )


def resolve_conflict(
    record: SemanticConflictRecord,
    context: dict[str, str] | None = None,
) -> SemanticConflictRecord:
    """Attempt to resolve a semantic conflict (Article 13).

    The five-rule hierarchy:
    1. Rank distinction
    2. Context distinction
    3. Origin vs. follower
    4. Reduce to figurative
    5. Block composition

    Parameters
    ----------
    record:
        An unresolved ``SemanticConflictRecord``.
    context:
        Optional dictionary of resolution cues.
    """
    if record.resolved:
        return record

    if context is None:
        context = {}

    for method, key in (
        (ConflictResolutionMethod.RANK_DISTINCTION, "rank"),
        (ConflictResolutionMethod.CONTEXT_DISTINCTION, "context"),
        (ConflictResolutionMethod.ORIGIN_VS_FOLLOWER, "origin"),
        (ConflictResolutionMethod.REDUCE_TO_FIGURATIVE, "figurative"),
    ):
        if key in context:
            return SemanticConflictRecord(
                unit_id=record.unit_id,
                conflict_type=record.conflict_type,
                conflicting_pair=record.conflicting_pair,
                resolution=method,
                resolved=True,
                notes=context[key],
            )

    return SemanticConflictRecord(
        unit_id=record.unit_id,
        conflict_type=record.conflict_type,
        conflicting_pair=record.conflicting_pair,
        resolution=ConflictResolutionMethod.BLOCK_COMPOSITION,
        resolved=False,
        notes="No resolution cues available",
    )
