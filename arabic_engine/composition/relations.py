"""باب العلاقات — Composition relation builder (Articles 36–38).

Pure functions that construct typed, directed relations between
composition units and auto-classify relation types.
"""

from __future__ import annotations

import uuid

from arabic_engine.core.enums import POS, CompositionRelationType
from arabic_engine.core.types import CompositionRelation, CompositionUnit


def build_relation(
    source: CompositionUnit,
    target: CompositionUnit,
    rel_type: CompositionRelationType,
    *,
    sub_type: str = "",
) -> CompositionRelation:
    """Build a composition relation between two units.

    Parameters
    ----------
    source:
        The source unit.
    target:
        The target unit.
    rel_type:
        The major relation type.
    sub_type:
        Optional more-specific label.
    """
    return CompositionRelation(
        relation_id=f"R_{uuid.uuid4().hex[:8]}",
        source_id=source.unit_id,
        target_id=target.unit_id,
        relation_type=rel_type,
        sub_type=sub_type,
        confidence=0.9 if source.admitted and target.admitted else 0.3,
    )


def classify_relation(
    source: CompositionUnit,
    target: CompositionUnit,
) -> CompositionRelationType:
    """Auto-detect the relation type between *source* and *target*.

    Heuristic classification based on POS and semantic type.
    """
    # Verbal source + nominal target → predication
    if source.pos == POS.FI3L and target.pos == POS.ISM:
        return CompositionRelationType.PREDICATION

    # Both nominal → could be restriction or dependency
    if source.pos == POS.ISM and target.pos == POS.ISM:
        return CompositionRelationType.RESTRICTION

    # Particle → linking
    if source.pos == POS.HARF or target.pos == POS.HARF:
        return CompositionRelationType.LINKING

    # Adjective → dependency
    if target.pos == POS.SIFA:
        return CompositionRelationType.DEPENDENCY

    return CompositionRelationType.EXPLANATION
