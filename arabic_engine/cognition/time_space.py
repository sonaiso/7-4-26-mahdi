"""Time and space tagging for propositions (v2).

Enriches a :class:`Proposition` with temporal and spatial anchoring
derived from verb morphology, adverbs, and explicit place names.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from arabic_engine.core.enums import POS, SpaceRef, TimeRef
from arabic_engine.core.types import (
    LexicalClosure,
    Proposition,
    TimeSpaceTag,
)

# ── Temporal patterns ───────────────────────────────────────────────

_PAST_PATTERNS = {"فَعَلَ", "فَعِلَ", "فَعُلَ", "اِفْتَعَلَ", "تَفَعَّلَ"}
_PRESENT_PATTERNS = {"يَفْعَلُ", "يَفْعِلُ", "يَفْعُلُ"}
_FUTURE_MARKERS = {"سَ", "سَوْفَ"}

# ── Temporal adverbs (v2) ───────────────────────────────────────────

_TEMPORAL_ADVERBS = {
    "أَمْس": TimeRef.PAST,
    "أَمْسِ": TimeRef.PAST,
    "أمس": TimeRef.PAST,
    "الْيَوْمَ": TimeRef.PRESENT,
    "اليوم": TimeRef.PRESENT,
    "غَدًا": TimeRef.FUTURE,
    "غدا": TimeRef.FUTURE,
    "غَد": TimeRef.FUTURE,
}

# ── Spatial markers (demo set) ──────────────────────────────────────

_SPATIAL_NOUNS = {
    "هُنَا": SpaceRef.HERE,
    "هُنَاكَ": SpaceRef.THERE,
    "هنا": SpaceRef.HERE,
    "هناك": SpaceRef.THERE,
}


def detect_time(closures: List[LexicalClosure]) -> Tuple[TimeRef, str]:
    """Infer temporal reference from verb patterns, particles, and adverbs.

    Returns a (TimeRef, detail_string) tuple.
    """
    time_detail = ""

    # Check adverbs first — they give the most explicit signal
    for cl in closures:
        if cl.pos == POS.ZARF:
            ref = _TEMPORAL_ADVERBS.get(cl.surface) or _TEMPORAL_ADVERBS.get(cl.lemma)
            if ref is not None:
                return ref, cl.lemma

    # Fall back to verb morphology
    for cl in closures:
        if cl.pos == POS.FI3L:
            if cl.pattern in _PAST_PATTERNS:
                return TimeRef.PAST, cl.surface
            if cl.pattern in _PRESENT_PATTERNS:
                return TimeRef.PRESENT, cl.surface
        if cl.surface in _FUTURE_MARKERS:
            return TimeRef.FUTURE, cl.surface
    return TimeRef.UNSPECIFIED, time_detail


def detect_space(closures: List[LexicalClosure]) -> Tuple[SpaceRef, str]:
    """Infer spatial reference from adverbs and place nouns.

    Returns a (SpaceRef, detail_string) tuple.
    """
    for cl in closures:
        ref = _SPATIAL_NOUNS.get(cl.surface) or _SPATIAL_NOUNS.get(cl.lemma)
        if ref is not None:
            return ref, cl.lemma
    return SpaceRef.UNSPECIFIED, ""


def tag(
    closures: List[LexicalClosure],
    proposition: Optional[Proposition] = None,
) -> TimeSpaceTag:
    """Return a :class:`TimeSpaceTag` for the given closures.

    If a *proposition* is supplied its ``time`` and ``space`` fields
    are updated in-place as well.
    """
    t, t_detail = detect_time(closures)
    s, s_detail = detect_space(closures)

    ts_tag = TimeSpaceTag(
        time_ref=t,
        space_ref=s,
        time_detail=t_detail,
        space_detail=s_detail,
    )

    if proposition is not None:
        # Propositions are mutable dataclasses
        proposition.time = t
        proposition.space = s

    return ts_tag
