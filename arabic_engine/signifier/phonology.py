"""Phonological analysis — consonant / vowel classification and syllabification.

Builds the *signifier graph* at the phonological level (التعريف 3).
"""

from __future__ import annotations

from typing import List, Tuple

from arabic_engine.core.types import Grapheme, Syllable

# ── Arabic consonant and vowel sets (code-points) ───────────────────

# Short vowels (combining marks)
_FATHA = 0x064E
_DAMMA = 0x064F
_KASRA = 0x0650
_SUKUN = 0x0652
_SHADDA = 0x0651
_SHORT_VOWELS = {_FATHA, _DAMMA, _KASRA}

# Long-vowel letters
_ALEF = 0x0627
_WAW = 0x0648
_YA = 0x064A
_LONG_VOWELS = {_ALEF, _WAW, _YA}

# Tanwin marks
_FATHATAN = 0x064B
_DAMMATAN = 0x064C
_KASRATAN = 0x064D
_TANWIN = {_FATHATAN, _DAMMATAN, _KASRATAN}


def is_consonant(g: Grapheme) -> bool:
    """Return True if the grapheme represents a consonant."""
    return g.base not in _LONG_VOWELS


def is_vowel_mark(cp: int) -> bool:
    """Return True if *cp* is a short-vowel combining mark."""
    return cp in _SHORT_VOWELS


def has_shadda(g: Grapheme) -> bool:
    """Return True if the grapheme carries a shaddah (gemination)."""
    return _SHADDA in g.marks


def get_short_vowel(g: Grapheme) -> int | None:
    """Return the short-vowel mark on *g*, or None."""
    for m in g.marks:
        if m in _SHORT_VOWELS:
            return m
    return None


def syllabify(graphemes: List[Grapheme]) -> List[Syllable]:
    """Produce a list of syllables from a grapheme sequence.

    Simplified model:
      • CV  → light  (weight 1)
      • CVC → heavy  (weight 2)
      • CVCC / CVV → super-heavy (weight 3)
    """
    syllables: List[Syllable] = []
    i = 0
    n = len(graphemes)
    while i < n:
        onset: Tuple[int, ...] = (graphemes[i].base,)
        vowel = get_short_vowel(graphemes[i])
        nucleus: Tuple[int, ...]
        coda: Tuple[int, ...] = ()
        weight = 1

        if vowel is not None:
            nucleus = (vowel,)
            # Check for long vowel (next grapheme is a vowel letter)
            if i + 1 < n and graphemes[i + 1].base in _LONG_VOWELS:
                nucleus = (vowel, graphemes[i + 1].base)
                weight = 3
                i += 1
            # Check for coda consonant: next grapheme has no vowel
            # and is not the onset of a following syllable
            elif (
                i + 1 < n
                and get_short_vowel(graphemes[i + 1]) is None
                and (i + 2 >= n or get_short_vowel(graphemes[i + 2]) is not None)
            ):
                coda = (graphemes[i + 1].base,)
                weight = 2  # CVC = heavy
                i += 1
        else:
            nucleus = ()
            weight = 1

        syllables.append(Syllable(
            onset=onset,
            nucleus=nucleus,
            coda=coda,
            weight=weight,
        ))
        i += 1

    return syllables
