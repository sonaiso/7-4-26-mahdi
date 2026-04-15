"""Signified layer — المدلول: ontological mapping.

Public sub-modules
------------------
* :mod:`arabic_engine.signified.ontology` — Maps lexical closures to
  typed ontological concept nodes (التعريف 5).
* :mod:`arabic_engine.signified.zero_coverage` — Linguistic-zero
  coverage analysis (تغطية الصفر اللغوي).
"""

from arabic_engine.signified.zero_coverage import (
    analyze_word_zero_coverage as analyze_word_zero_coverage,
)

__all__ = ["ontology", "zero_coverage"]
