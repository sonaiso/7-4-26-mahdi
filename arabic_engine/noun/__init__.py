"""Noun Fractal Constitution v1 — دستور الاسم الفراكتالي.

Public sub-modules
------------------
* :mod:`arabic_engine.noun.constitution_v1` — Complete noun fractal
  analysis: classification, inflection, morphology, signification,
  readiness, and factory functions.
"""

from .constitution_v1 import batch_build as batch_build
from .constitution_v1 import build_noun_fractal as build_noun_fractal
from .constitution_v1 import check_minimum as check_minimum
from .constitution_v1 import classify_genus_level as classify_genus_level
from .constitution_v1 import classify_nominal_attribute as classify_nominal_attribute
from .constitution_v1 import classify_noun_direction as classify_noun_direction
from .constitution_v1 import classify_proper_noun as classify_proper_noun
from .constitution_v1 import classify_universality as classify_universality
from .constitution_v1 import compute_readiness as compute_readiness
from .constitution_v1 import compute_signification as compute_signification
from .constitution_v1 import determine_composition as determine_composition
from .constitution_v1 import determine_inflection as determine_inflection
from .constitution_v1 import determine_morphology as determine_morphology
from .constitution_v1 import validate_noun_fractal as validate_noun_fractal
