"""Unicode normalisation for Arabic text (التعريف 2).

N : ℕ* → ℕ*

Removes tatweel, normalises whitespace, and optionally strips or
preserves tashkīl (diacritics) according to a policy flag.
"""

from __future__ import annotations

import re
import unicodedata
from typing import List

from arabic_engine.core.types import Grapheme

# Arabic Unicode ranges
_TATWEEL = "\u0640"
_COMBINING_RANGE = range(0x064B, 0x0670)  # Fathatan … Superscript Alef
_HAMZA_MAP = {
    "\u0622": "\u0627",  # آ → ا
    "\u0623": "\u0627",  # أ → ا
    "\u0625": "\u0627",  # إ → ا
}

_MULTI_SPACE = re.compile(r"\s+")


def normalize(text: str, *, strip_tashkil: bool = False) -> str:
    """Return a normalised copy of *text*.

    • Removes tatweel (kashida).
    • Collapses multiple whitespace to single space.
    • Optionally strips combining diacritics.
    • Applies NFC normalisation.
    """
    text = unicodedata.normalize("NFC", text)
    text = text.replace(_TATWEEL, "")
    if strip_tashkil:
        text = "".join(
            ch for ch in text if ord(ch) not in _COMBINING_RANGE
        )
    text = _MULTI_SPACE.sub(" ", text).strip()
    return text


def normalize_hamza(text: str) -> str:
    """Unify hamza-bearing alefs to bare alef."""
    for src, dst in _HAMZA_MAP.items():
        text = text.replace(src, dst)
    return text


def tokenize(text: str) -> List[str]:
    """Split normalised text into whitespace-delimited tokens."""
    return normalize(text).split()


def to_graphemes(token: str) -> List[Grapheme]:
    """Decompose a token into a sequence of :class:`Grapheme` clusters.

    Each cluster is (base_codepoint, tuple_of_mark_codepoints).
    """
    clusters: List[Grapheme] = []
    base: int | None = None
    marks: list[int] = []
    for ch in token:
        cp = ord(ch)
        if unicodedata.category(ch).startswith("M"):
            # combining mark — attach to current base
            marks.append(cp)
        else:
            if base is not None:
                clusters.append(Grapheme(base=base, marks=tuple(marks)))
            base = cp
            marks = []
    if base is not None:
        clusters.append(Grapheme(base=base, marks=tuple(marks)))
    return clusters
