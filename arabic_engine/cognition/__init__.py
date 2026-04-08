"""Cognition layer — الإدراك: evaluation, time/space, world model, inference.

Public sub-modules
------------------
* :mod:`arabic_engine.cognition.evaluation` — Proposition construction
  (judgment, التعريف 7) and truth/guidance evaluation (التعريف 8).
* :mod:`arabic_engine.cognition.time_space` — Temporal and spatial
  anchoring for propositions.
* :mod:`arabic_engine.cognition.world_model` — In-memory knowledge base
  of world facts used to adjust evaluation confidence.
* :mod:`arabic_engine.cognition.inference_rules` — Forward-chaining
  rule engine for deriving new propositions.
* :mod:`arabic_engine.cognition.mafhum` — Mafhūm (implied meaning)
  analysis — minimal types (Ch. 21).
"""

__all__ = [
    "evaluation",
    "time_space",
    "world_model",
    "inference_rules",
    "mafhum",
]
