"""Signified layer — المدلول: ontological mapping.

Public sub-modules
------------------
* :mod:`arabic_engine.signified.ontology` — Maps lexical closures to
  typed ontological concept nodes (التعريف 5).
* :mod:`arabic_engine.signified.signified_record` — Signified Ontology
  v1.0 registry, factory, and validation.
"""

from .signified_record import (  # noqa: F401 -- intentional re-exports
    SIGNIFIED_DB as SIGNIFIED_DB,
)
from .signified_record import (
    batch_signified as batch_signified,
)
from .signified_record import (
    make_signified as make_signified,
)
from .signified_record import (
    validate_signified as validate_signified,
)

__all__ = [
    "ontology",
    "signified_record",
    "SIGNIFIED_DB",
    "make_signified",
    "batch_signified",
    "validate_signified",
]
