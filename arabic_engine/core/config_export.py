"""Config export — serialise machine configs to dict / JSON / YAML.

This module can export the transition tables and threshold constants
for every layer machine so they can be loaded from external config
files or inspected as data.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from arabic_engine.cognition.judgment_machine import JUDGMENT_MACHINE_CONFIG
from arabic_engine.core import formulas as F
from arabic_engine.core.mci import (
    B_WEIGHT,
    C_WEIGHT,
    E_WEIGHT,
    MCI_ACCEPT_THRESHOLD,
    MCI_REJECT_THRESHOLD,
    MCI_SUSPEND_THRESHOLD,
    O_WEIGHT,
    P_WEIGHT,
    TOTAL_WEIGHT,
    U_WEIGHT,
)
from arabic_engine.core.state_machine import StateMachine, StateMachineConfig
from arabic_engine.signal.sound_machine import SOUND_MACHINE_CONFIG
from arabic_engine.signifier.haraka_machine import HARAKA_MACHINE_CONFIG
from arabic_engine.signifier.root_rank_machine import ROOT_RANK_MACHINE_CONFIG
from arabic_engine.signifier.syllable_machine import SYLLABLE_MACHINE_CONFIG
from arabic_engine.signifier.transform_machine import TRANSFORM_MACHINE_CONFIG

# ── registry ───────────────────────────────────────────────────────

_ALL_CONFIGS: Dict[str, StateMachineConfig] = {
    "sound": SOUND_MACHINE_CONFIG,
    "haraka": HARAKA_MACHINE_CONFIG,
    "syllable": SYLLABLE_MACHINE_CONFIG,
    "root_rank": ROOT_RANK_MACHINE_CONFIG,
    "transform": TRANSFORM_MACHINE_CONFIG,
    "judgment": JUDGMENT_MACHINE_CONFIG,
}


# ── helpers ─────────────────────────────────────────────────────────


def _config_to_dict(cfg: StateMachineConfig) -> Dict[str, Any]:
    sm = StateMachine(cfg)
    return {
        "name": cfg.name,
        "initial_state": cfg.initial_state.name,
        "accept_states": sorted(s.name for s in cfg.accept_states),
        "reject_states": sorted(s.name for s in cfg.reject_states),
        "transitions": sm.transition_table(),
    }


# ── public API ──────────────────────────────────────────────────────


def export_machine_config(machine_name: str) -> Dict[str, Any]:
    """Export a single machine config as a plain dict.

    Raises ``KeyError`` if *machine_name* is not registered.
    """
    return _config_to_dict(_ALL_CONFIGS[machine_name])


def export_all_configs() -> Dict[str, Any]:
    """Export all machine configs and global thresholds."""
    machines: Dict[str, Any] = {}
    for name, cfg in _ALL_CONFIGS.items():
        machines[name] = _config_to_dict(cfg)

    thresholds: Dict[str, float] = {
        "energy": F.ENERGY_THRESHOLD,
        "boundary": F.BOUNDARY_THRESHOLD,
        "cohesion": F.COHESION_THRESHOLD,
        "unity": F.UNITY_THRESHOLD,
        "mci": F.MCI_THRESHOLD,
        "sonority": F.SONORITY_THRESHOLD,
        "mobility": F.MOBILITY_THRESHOLD,
        "syllable_score": F.SYLLABLE_SCORE_THRESHOLD,
        "root_fitness": F.ROOT_FITNESS_THRESHOLD,
        "rank_score": F.RANK_SCORE_THRESHOLD,
        "rank_ambiguity": F.RANK_AMBIGUITY_THRESHOLD,
        "transform_confidence": F.TRANSFORM_CONFIDENCE_THRESHOLD,
        "transform_validation": F.TRANSFORM_VALIDATION_THRESHOLD,
        "judgment_score": F.JUDGMENT_SCORE_THRESHOLD,
        "evidence_strength": F.EVIDENCE_STRENGTH_THRESHOLD,
        "validation_score": F.VALIDATION_SCORE_THRESHOLD,
        "final_approval": F.FINAL_APPROVAL_THRESHOLD,
    }

    mci_weights: Dict[str, float] = {
        "B": B_WEIGHT,
        "U": U_WEIGHT,
        "C": C_WEIGHT,
        "E": E_WEIGHT,
        "P": P_WEIGHT,
        "O": O_WEIGHT,
        "total": TOTAL_WEIGHT,
    }

    mci_thresholds: Dict[str, float] = {
        "reject": MCI_REJECT_THRESHOLD,
        "suspend": MCI_SUSPEND_THRESHOLD,
        "accept": MCI_ACCEPT_THRESHOLD,
    }

    return {
        "machines": machines,
        "thresholds": thresholds,
        "mci_weights": mci_weights,
        "mci_thresholds": mci_thresholds,
    }


def to_json(config: Dict[str, Any], *, indent: int = 2) -> str:
    """Serialise a config dict to a JSON string."""
    return json.dumps(config, indent=indent, ensure_ascii=False)


def to_yaml(config: Dict[str, Any]) -> str:
    """Serialise a config dict to a YAML string (pure-Python fallback).

    Uses ``yaml.dump`` if PyYAML is available, otherwise falls back to
    a minimal JSON-based representation.
    """
    try:
        import yaml  # type: ignore[import-untyped]

        return yaml.dump(config, allow_unicode=True, default_flow_style=False)
    except ImportError:  # pragma: no cover
        return json.dumps(config, indent=2, ensure_ascii=False)


def available_machines() -> List[str]:
    """Return the names of all registered machines."""
    return list(_ALL_CONFIGS.keys())
