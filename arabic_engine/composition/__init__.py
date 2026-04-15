"""التركيب / دستور التركيب — Composition / Syntax Constitution v1.

This package implements the composition layer of the Arabic engine,
following the fractal-structured community model where completed
lexemes and concepts enter predication, restriction, dependency,
relations, roles, propositions, and inter-proposition links.

Public API
----------
.. autosummary::

    compose
    compute_readiness
    validate_composition
    decompose
    detect_ambiguity
    resolve_ambiguity
    detect_conflict
    resolve_conflict
    detect_transfer
    validate_transfer
    determine_truth_type
    adjudicate_truth
    check_admission
    build_predication
    classify_predication
    build_restriction
    validate_restriction
    build_dependency
    validate_dependency
    build_relation
    classify_relation
    assign_role
    realize_role
    build_proposition
    close_proposition
    classify_proposition
    link_propositions
    validate_link
    run_all_gates
"""

from .admission import check_admission as check_admission
from .composition import compose as compose
from .composition import compute_readiness as compute_readiness
from .composition import decompose as decompose
from .composition import validate_composition as validate_composition
from .conflict import detect_conflict as detect_conflict
from .conflict import resolve_conflict as resolve_conflict
from .dependency import build_dependency as build_dependency
from .dependency import validate_dependency as validate_dependency
from .disambiguation import detect_ambiguity as detect_ambiguity
from .disambiguation import resolve_ambiguity as resolve_ambiguity
from .gates import run_all_gates as run_all_gates
from .inter_proposition import link_propositions as link_propositions
from .inter_proposition import validate_link as validate_link
from .predication import build_predication as build_predication
from .predication import classify_predication as classify_predication
from .proposition import build_proposition as build_proposition
from .proposition import classify_proposition as classify_proposition
from .proposition import close_proposition as close_proposition
from .relations import build_relation as build_relation
from .relations import classify_relation as classify_relation
from .restriction import build_restriction as build_restriction
from .restriction import validate_restriction as validate_restriction
from .roles import assign_role as assign_role
from .roles import realize_role as realize_role
from .transfer import detect_transfer as detect_transfer
from .transfer import validate_transfer as validate_transfer
from .truth_type import adjudicate_truth as adjudicate_truth
from .truth_type import determine_truth_type as determine_truth_type

__all__ = [
    "adjudicate_truth",
    "assign_role",
    "build_dependency",
    "build_predication",
    "build_proposition",
    "build_relation",
    "build_restriction",
    "check_admission",
    "classify_predication",
    "classify_proposition",
    "classify_relation",
    "close_proposition",
    "compose",
    "compute_readiness",
    "decompose",
    "detect_ambiguity",
    "detect_conflict",
    "detect_transfer",
    "determine_truth_type",
    "link_propositions",
    "realize_role",
    "resolve_ambiguity",
    "resolve_conflict",
    "run_all_gates",
    "validate_composition",
    "validate_dependency",
    "validate_link",
    "validate_restriction",
    "validate_transfer",
]
