"""باب الاشتراك — Ambiguity detection and resolution (Articles 6–9).

Pure functions that detect whether a lexeme/concept carries unresolved
semantic sharing (اشتراك) and attempt resolution via the six-rule
hierarchy specified in Article 9.
"""

from __future__ import annotations

from arabic_engine.core.enums import AmbiguityResolution, AmbiguityType
from arabic_engine.core.types import DisambiguationRecord


def detect_ambiguity(
    unit_id: str,
    label: str,
    semantic_directions: tuple[str, ...],
) -> DisambiguationRecord:
    """Detect whether *label* carries lexical/semantic ambiguity.

    Parameters
    ----------
    unit_id:
        Identifier for the lexeme/concept.
    label:
        Surface form or concept label.
    semantic_directions:
        Competing semantic directions the unit may carry.

    Returns
    -------
    DisambiguationRecord
        If only one direction exists, ``ambiguity_type`` is ``None``
        and the record is pre-resolved.
    """
    if len(semantic_directions) <= 1:
        return DisambiguationRecord(
            unit_id=unit_id,
            ambiguity_type=None,
            candidates=semantic_directions,
            resolution=AmbiguityResolution.INTERNAL_SEMANTIC_CUE,
            resolved_direction=semantic_directions[0] if semantic_directions else "",
            confidence=1.0,
        )

    # Heuristic classification of ambiguity type
    ambiguity_type = _classify_ambiguity(semantic_directions)
    return DisambiguationRecord(
        unit_id=unit_id,
        ambiguity_type=ambiguity_type,
        candidates=semantic_directions,
        resolution=AmbiguityResolution.OPEN_PENDING,
        resolved_direction="",
        confidence=0.0,
    )


def resolve_ambiguity(
    record: DisambiguationRecord,
    cues: dict[str, str] | None = None,
) -> DisambiguationRecord:
    """Attempt to resolve ambiguity using the 6-rule hierarchy (Article 9).

    Parameters
    ----------
    record:
        An existing ``DisambiguationRecord`` (typically OPEN_PENDING).
    cues:
        Optional dictionary of contextual cues, e.g.
        ``{"semantic": "direction_a", "syntactic": "direction_b"}``.

    Returns
    -------
    DisambiguationRecord
        Updated record with resolution strategy and winning direction.
    """
    if record.ambiguity_type is None or len(record.candidates) <= 1:
        return record

    if cues is None:
        cues = {}

    # Walk the hierarchy: semantic → referential → syntactic → weight → conventional → open
    for strategy, key in (
        (AmbiguityResolution.INTERNAL_SEMANTIC_CUE, "semantic"),
        (AmbiguityResolution.REFERENTIAL_CUE, "referential"),
        (AmbiguityResolution.SYNTACTIC_CUE, "syntactic"),
        (AmbiguityResolution.WEIGHT_PRIORITY, "weight"),
        (AmbiguityResolution.CONVENTIONAL_PRIORITY, "conventional"),
    ):
        if key in cues and cues[key] in record.candidates:
            return DisambiguationRecord(
                unit_id=record.unit_id,
                ambiguity_type=record.ambiguity_type,
                candidates=record.candidates,
                resolution=strategy,
                resolved_direction=cues[key],
                confidence=_confidence_for(strategy),
            )

    return DisambiguationRecord(
        unit_id=record.unit_id,
        ambiguity_type=record.ambiguity_type,
        candidates=record.candidates,
        resolution=AmbiguityResolution.OPEN_PENDING,
        resolved_direction="",
        confidence=0.0,
    )


# ── Internals ───────────────────────────────────────────────────────


def _classify_ambiguity(directions: tuple[str, ...]) -> AmbiguityType:
    """Heuristic classification of ambiguity type."""
    if len(directions) == 2:
        return AmbiguityType.SEMANTIC_DUAL
    return AmbiguityType.LEXICAL_PURE


def _confidence_for(strategy: AmbiguityResolution) -> float:
    """Map resolution strategy to a default confidence score."""
    _MAP = {
        AmbiguityResolution.INTERNAL_SEMANTIC_CUE: 0.95,
        AmbiguityResolution.REFERENTIAL_CUE: 0.85,
        AmbiguityResolution.SYNTACTIC_CUE: 0.75,
        AmbiguityResolution.WEIGHT_PRIORITY: 0.65,
        AmbiguityResolution.CONVENTIONAL_PRIORITY: 0.55,
    }
    return _MAP.get(strategy, 0.0)
