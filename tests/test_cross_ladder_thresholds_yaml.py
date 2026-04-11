from __future__ import annotations

from pathlib import Path

import yaml


def _load_matrix() -> dict:
    project_root = Path(__file__).resolve().parents[1]
    yaml_path = project_root / "arabic_engine" / "data" / "cross_ladder_thresholds.yaml"
    with yaml_path.open(encoding="utf-8") as stream:
        payload = yaml.safe_load(stream)
    return payload["matrix"]


def test_cross_ladder_yaml_exists() -> None:
    project_root = Path(__file__).resolve().parents[1]
    yaml_path = project_root / "arabic_engine" / "data" / "cross_ladder_thresholds.yaml"
    assert yaml_path.exists()


def test_cross_ladder_yaml_structure_and_counts() -> None:
    matrix = _load_matrix()
    thresholds = matrix["thresholds"]

    assert matrix["id"] == "cross_ladder_threshold_matrix_v1"
    assert len(thresholds) == 31
    assert [row["order"] for row in thresholds] == list(range(1, 32))


def test_cross_ladder_yaml_threshold_invariants() -> None:
    matrix = _load_matrix()
    thresholds = matrix["thresholds"]
    allowed_transformations = set(matrix["transformation_types"])
    allowed_revisions = set(matrix["revision_policies"])
    expected_revisions = {"none", "limited", "open"}

    threshold_names = [row["threshold"] for row in thresholds]
    assert len(threshold_names) == len(set(threshold_names))
    assert set(expected_revisions) == allowed_revisions

    for row in thresholds:
        assert row["transformation_type"] in allowed_transformations
        assert row["revision_policy"] in allowed_revisions
        assert isinstance(row["output_class"], list)
        assert row["output_class"]
        assert isinstance(row["lock"], list)
        assert row["lock"]
