"""Cross-layer constraint propagation — نشر القيود عبر الطبقات.

In this first iteration, propagation is limited to:

1. Score all support edges.
2. Mark conflicts between incompatible hypotheses at the same stage.
3. Return updated edges for the hypothesis state.

Full cross-layer propagation with iterative tightening is reserved
for future iterations.
"""

from __future__ import annotations

from typing import List

from arabic_engine.constraints.scoring import score_support
from arabic_engine.core.enums import ConflictState
from arabic_engine.core.types import ConflictEdge, HypothesisNode, SupportEdge


def propagate(
    hypotheses: List[HypothesisNode],
) -> tuple[list[SupportEdge], list[ConflictEdge]]:
    """Run one pass of constraint propagation.

    Parameters
    ----------
    hypotheses : list[HypothesisNode]
        All hypotheses across all stages.

    Returns
    -------
    tuple[list[SupportEdge], list[ConflictEdge]]
        Support edges and conflict edges discovered during propagation.
    """
    support = score_support(hypotheses)
    conflicts = _detect_conflicts(hypotheses)
    return support, conflicts


def _detect_conflicts(hypotheses: List[HypothesisNode]) -> List[ConflictEdge]:
    """Detect hard conflicts between hypotheses at the same stage.

    Two hypotheses conflict if they occupy the same stage and share
    the same source_refs but propose incompatible values.  In this
    first iteration, we only flag hypotheses that share exact
    source_refs within a stage.

    Parameters
    ----------
    hypotheses : list[HypothesisNode]
        All hypotheses.

    Returns
    -------
    list[ConflictEdge]
        Conflict edges between incompatible hypotheses.
    """
    conflicts: List[ConflictEdge] = []
    idx = 0

    # Group by (stage, source_refs)
    groups: dict[tuple, list[HypothesisNode]] = {}
    for h in hypotheses:
        key = (h.stage, h.source_refs)
        groups.setdefault(key, []).append(h)

    for key, group in groups.items():
        if len(group) <= 1:
            continue
        # If multiple hypotheses exist for the same source at the same stage,
        # they are in soft conflict (only one should be stabilised).
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                conflicts.append(
                    ConflictEdge(
                        edge_id=f"CONF_{idx}",
                        node_a_ref=group[i].node_id,
                        node_b_ref=group[j].node_id,
                        conflict_state=ConflictState.SOFT,
                        justification=f"Same source at stage {key[0].name}",
                    )
                )
                idx += 1

    return conflicts
