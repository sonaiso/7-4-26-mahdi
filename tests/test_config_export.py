"""Tests for the config export module."""

from __future__ import annotations

import json

from arabic_engine.core.config_export import (
    available_machines,
    export_all_configs,
    export_machine_config,
    to_json,
    to_yaml,
)


class TestExportMachineConfig:
    def test_export_sound(self):
        cfg = export_machine_config("sound")
        assert cfg["name"] == "SoundMachine"
        assert "S5_STABLE_UNIT" in cfg["accept_states"]
        assert len(cfg["transitions"]) > 0

    def test_export_haraka(self):
        cfg = export_machine_config("haraka")
        assert cfg["name"] == "HarakaMachine"

    def test_export_syllable(self):
        cfg = export_machine_config("syllable")
        assert cfg["name"] == "SyllableMachine"

    def test_export_root_rank(self):
        cfg = export_machine_config("root_rank")
        assert cfg["name"] == "RootRankMachine"

    def test_export_transform(self):
        cfg = export_machine_config("transform")
        assert cfg["name"] == "TransformMachine"

    def test_export_judgment(self):
        cfg = export_machine_config("judgment")
        assert cfg["name"] == "JudgmentMachine"


class TestExportAllConfigs:
    def test_has_all_machines(self):
        data = export_all_configs()
        assert "machines" in data
        assert "thresholds" in data
        assert "mci_weights" in data
        assert "mci_thresholds" in data
        assert len(data["machines"]) == 6

    def test_thresholds_present(self):
        data = export_all_configs()
        assert data["thresholds"]["energy"] == 0.30
        assert data["thresholds"]["final_approval"] == 0.75

    def test_mci_weights(self):
        data = export_all_configs()
        assert data["mci_weights"]["B"] == 1.2
        assert data["mci_weights"]["total"] == 7.0


class TestSerialisation:
    def test_to_json(self):
        cfg = export_machine_config("sound")
        s = to_json(cfg)
        parsed = json.loads(s)
        assert parsed["name"] == "SoundMachine"

    def test_to_yaml(self):
        cfg = export_machine_config("sound")
        s = to_yaml(cfg)
        assert "SoundMachine" in s


class TestAvailableMachines:
    def test_list(self):
        names = available_machines()
        assert "sound" in names
        assert "haraka" in names
        assert "syllable" in names
        assert "root_rank" in names
        assert "transform" in names
        assert "judgment" in names
        assert len(names) == 6
