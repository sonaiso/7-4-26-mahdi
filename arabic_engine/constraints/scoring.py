"""Constraint scoring — تقييم الدعم.

Assigns support scores to hypotheses based on inter-layer consistency.
"""

from __future__ import annotations

from typing import List

from arabic_engine.core.types import HypothesisNode, SupportEdge


def score_support(hypotheses: List[HypothesisNode]) -> List[SupportEdge]:
    """Create support edges between hypotheses that share source refs.

    When two hypotheses at different stages reference the same upstream
    node, a support edge is created linking them.  This is the simplest
    form of support scoring: shared provenance = mutual support.

    Parameters
    ----------
    hypotheses : list[HypothesisNode]
        All hypotheses across all stages.

    Returns
    -------
    list[SupportEdge]
        Support edges between hypotheses with overlapping sources.
    """
    edges: List[SupportEdge] = []
    idx = 0

    # Build a reverse index: source_ref → list of node_ids
    source_index: dict[str, list[str]] = {}
    for h in hypotheses:
        for ref in h.source_refs:
            source_index.setdefault(ref, []).append(h.node_id)

    # For each shared source, create support edges between the nodes
    for source_ref, node_ids in source_index.items():
        for i in range(len(node_ids)):
            for j in range(i + 1, len(node_ids)):
                edges.append(
                    SupportEdge(
                        edge_id=f"SUP_{idx}",
                        supporter_ref=node_ids[i],
                        target_ref=node_ids[j],
                        weight=1.0,
                        justification=f"shared source {source_ref}",
                    )
                )
                idx += 1

    return edges


def build_constraint_edges(
    hypotheses: List[HypothesisNode],
) -> list:
    """Build constraint edges from hypothesis relationships.

    Currently returns an empty list — cross-layer constraint creation
    is reserved for Phase D iteration 2.

    Parameters
    ----------
    hypotheses : list[HypothesisNode]
        All hypotheses across all stages.

    Returns
    -------
    list[ConstraintEdge]
        Constraint edges (empty in this iteration).
    """
    return []
