"""Time and space tagging for propositions (v2).

Enriches a :class:`Proposition` with temporal and spatial anchoring
derived from verb morphology, adverbs, and explicit place names.
"""

from __future__ import annotations

from typing import List, Optional

from arabic_engine.core.enums import POS, TimeRef, SpaceRef
from arabic_engine.core.types import (
    LexicalClosure,
    Proposition,
    TimeSpaceTag,
)

# ── Temporal patterns ───────────────────────────────────────────────

_PAST_PATTERNS = {"فَعَلَ", "فَعِلَ", "فَعُلَ", "اِفْتَعَلَ", "تَفَعَّلَ"}
_PRESENT_PATTERNS = {"يَفْعَلُ", "يَفْعِلُ", "يَفْعُلُ"}
_FUTURE_MARKERS = {"سَ", "سَوْفَ"}

# ── Spatial markers (demo set) ──────────────────────────────────────

_SPATIAL_NOUNS = {
    "هُنَا": SpaceRef.HERE,
    "هُنَاكَ": SpaceRef.THERE,
    "هنا": SpaceRef.HERE,
    "هناك": SpaceRef.THERE,
}


def detect_time(closures: List[LexicalClosure]) -> TimeRef:
    """Infer temporal reference from verb patterns and particles."""
    for cl in closures:
        if cl.pos == POS.FI3L:
            if cl.pattern in _PAST_PATTERNS:
                return TimeRef.PAST
            if cl.pattern in _PRESENT_PATTERNS:
                return TimeRef.PRESENT
        if cl.surface in _FUTURE_MARKERS:
            return TimeRef.FUTURE
    return TimeRef.UNSPECIFIED


def detect_space(closures: List[LexicalClosure]) -> SpaceRef:
    """Infer spatial reference from adverbs and place nouns."""
    for cl in closures:
        ref = _SPATIAL_NOUNS.get(cl.surface) or _SPATIAL_NOUNS.get(cl.lemma)
        if ref is not None:
            return ref
    return SpaceRef.UNSPECIFIED


def tag(
    closures: List[LexicalClosure],
    proposition: Optional[Proposition] = None,
) -> TimeSpaceTag:
    """Return a :class:`TimeSpaceTag` for the given closures.

    If a *proposition* is supplied its ``time`` and ``space`` fields
    are updated in-place as well.
    """
    t = detect_time(closures)
    s = detect_space(closures)

    ts_tag = TimeSpaceTag(time_ref=t, space_ref=s)

    if proposition is not None:
        # Propositions are mutable dataclasses
        proposition.time = t
        proposition.space = s

    return ts_tag
