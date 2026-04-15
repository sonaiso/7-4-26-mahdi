"""Data loader for CSV/JSON reference files (البيانات المرجعية).

Provides cached loaders for Arabic phonological, morphological, and
Unicode reference data stored as CSV and JSON files under the
``arabic_engine/data/`` package.

All loaders return plain Python dicts/lists and cache their results
at module level so that repeated calls are essentially free.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List

# ── Package root for data files ─────────────────────────────────────

_DATA_ROOT = Path(__file__).resolve().parent

# ── Module-level caches ─────────────────────────────────────────────

_cache: Dict[str, Any] = {}


def _csv_path(*parts: str) -> Path:
    """Resolve a path relative to the data package root."""
    return _DATA_ROOT.joinpath(*parts)


def _load_csv(rel_path: str) -> List[Dict[str, str]]:
    """Load a CSV file and return a list of row dicts (cached)."""
    if rel_path in _cache:
        return _cache[rel_path]
    path = _DATA_ROOT / rel_path
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows: List[Dict[str, str]] = list(reader)
    _cache[rel_path] = rows
    return rows


def _load_json(rel_path: str) -> Any:
    """Load a JSON file and return the parsed object (cached)."""
    if rel_path in _cache:
        return _cache[rel_path]
    path = _DATA_ROOT / rel_path
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    _cache[rel_path] = data
    return data


# ── Public loaders ──────────────────────────────────────────────────


def load_unicode_marks() -> Dict[str, Dict[str, str]]:
    """Return Unicode combining marks keyed by codepoint (e.g. ``'U+064E'``).

    Each value is a dict with keys ``char``, ``codepoint``, ``name``,
    ``type``.
    """
    rows = _load_csv("unicode/unicode_marks.csv")
    return {row["codepoint"]: row for row in rows}


def load_arabic_letters() -> Dict[str, Dict[str, str]]:
    """Return Arabic letter records keyed by ``base_codepoint``.

    Each value contains ``id``, ``surface``, ``base_char``,
    ``base_codepoint``, ``combining_marks``, phonetic code fields,
    and ``entity_score``.
    """
    rows = _load_csv("phonology/arabic_letters.csv")
    return {row["base_codepoint"]: row for row in rows}


def load_arabic_vowels() -> Dict[str, Dict[str, str]]:
    """Return Arabic vowel/mark records keyed by ``codepoint``.

    Each value contains ``id``, ``char``, ``codepoint``, height/length/
    role codes, ``vowel_code``, and ``entity_score``.
    """
    rows = _load_csv("phonology/arabic_vowels.csv")
    return {row["codepoint"]: row for row in rows}


def load_syllable_shapes() -> Dict[str, Dict[str, str]]:
    """Return syllable shape records keyed by ``shape_label``.

    Each value contains ``shape_id``, ``shape_label``, ``shape_code``,
    ``nucleus_type``, ``closure_type``, ``weight_code``.
    """
    rows = _load_csv("phonology/syllable_shapes.csv")
    return {row["shape_label"]: row for row in rows}


def load_pattern_codes() -> Dict[str, Dict[str, str]]:
    """Return morphological pattern records keyed by ``pattern_code``.

    Each value contains ``id``, ``root_length``, ``pattern_label``,
    ``pattern_code``, ``augment_count``, ``pattern_type``.
    """
    rows = _load_csv("morphology/pattern_codes.csv")
    return {row["pattern_code"]: row for row in rows}


def load_closed_connectors() -> List[Dict[str, str]]:
    """Return closed connector/clitic records as a list of dicts.

    Each dict contains ``surface``, ``type``, ``codepoint_sequence``.
    """
    return _load_csv("morphology/closed_connectors.csv")


def load_closed_built_forms() -> List[Dict[str, str]]:
    """Return closed built-form records as a list of dicts.

    Each dict contains ``surface``, ``type``, ``codepoint_sequence``.
    """
    return _load_csv("morphology/closed_built_forms.csv")


def load_unicode_policy() -> Dict[str, Any]:
    """Return the Unicode normalisation policy configuration.

    The returned dict has a single top-level key ``unicode_policy``
    containing the normalisation settings.
    """
    return _load_json("unicode/unicode_policy.json")


def clear_cache() -> None:
    """Clear all cached data (mainly useful in tests)."""
    _cache.clear()
