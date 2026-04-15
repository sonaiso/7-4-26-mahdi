"""Symbolic Encoding — ترميز الحرف والحركة قيمياً ورياضياً.

Implements the refined axiom that separates **essence** from **constraint**::

    Ess(x)  = ⟨Slot(x), Value(x)⟩      — the essence (position + value)
    Cond(x) = Ω_x                       — the constraint (activation condition)
    Valid(x) ⟺ Ess(x) ∧ Ω_x           — structural acceptance

The constraint is NOT part of the unit's identity.  It is an external
activation / acceptance / insertion condition.

Match / Containment / Commitment
---------------------------------
    M(x) = Match(S_x)           — the unit matches its slot
    T(x) = Containment(V_x)     — the value is embeddable in a higher structure
    Q(x) = Condition(x)         — the constraint is satisfied

    Representable(x) ⟺ M(x) ∧ T(x)
    Usable(x)        ⟺ M(x) ∧ T(x) ∧ Q(x)

Letter Encoding
---------------
A letter is encoded by its consonantal identity, not by its name::

    Ess(L) = ⟨S_L, V_L⟩   where S_L = position, V_L = features
    Valid(L) ⟺ Ess(L) ∧ Ω_L(context)

Vowel Encoding
--------------
A vowel is an operational value, not a base unit::

    Ess(H) = ⟨S_H, V_H⟩   where S_H = dependent position, V_H = quality
    Valid(H) ⟺ Ess(H) ∧ Ω_H(context)
"""

from __future__ import annotations

from typing import Dict, FrozenSet, List, Optional, Tuple

from arabic_engine.core.enums import (
    ConstraintKind,
    OntologicalLayer,
    PhonGroup,
    SymbolicStatus,
    UnitType,
)
from arabic_engine.core.types import LetterRecord, SymbolicRecord, VowelRecord

# ── Factory helpers ──────────────────────────────────────────────────

def make_letter(
    record_id: str,
    slot_position: int,
    slot_label: str,
    value_vector: Tuple[int, ...],
    value_label: str,
    *,
    phonetic_group: Optional[PhonGroup] = None,
    syllabic_weight: int = 1,
    constraints: FrozenSet[ConstraintKind] = frozenset(),
    constraint_omega: float = 1.0,
    layer: OntologicalLayer = OntologicalLayer.CELL,
    notes: str = "",
) -> LetterRecord:
    """Create a :class:`LetterRecord` with computed status.

    Status is derived automatically::

        REPRESENTABLE  if Core(X) is well-formed
        VALID          if Core(X) ∧ Ω_X
        PROMOTABLE     (set later by promotion engine)
    """
    status = _compute_status(slot_position, value_vector, constraint_omega)
    return LetterRecord(
        record_id=record_id,
        unit_type=UnitType.LETTER,
        slot_position=slot_position,
        slot_label=slot_label,
        value_vector=value_vector,
        value_label=value_label,
        constraints=constraints,
        constraint_omega=constraint_omega,
        layer=layer,
        status=status,
        notes=notes,
        phonetic_group=phonetic_group,
        syllabic_weight=syllabic_weight,
    )


def make_vowel(
    record_id: str,
    slot_position: int,
    slot_label: str,
    value_vector: Tuple[int, ...],
    value_label: str,
    *,
    carrier_id: Optional[str] = None,
    is_long: bool = False,
    constraints: FrozenSet[ConstraintKind] = frozenset(),
    constraint_omega: float = 1.0,
    layer: OntologicalLayer = OntologicalLayer.CELL,
    notes: str = "",
) -> VowelRecord:
    """Create a :class:`VowelRecord` with computed status."""
    status = _compute_status(slot_position, value_vector, constraint_omega)
    return VowelRecord(
        record_id=record_id,
        unit_type=UnitType.VOWEL,
        slot_position=slot_position,
        slot_label=slot_label,
        value_vector=value_vector,
        value_label=value_label,
        constraints=constraints,
        constraint_omega=constraint_omega,
        layer=layer,
        status=status,
        notes=notes,
        carrier_id=carrier_id,
        is_long=is_long,
    )


# ── Validation engine ────────────────────────────────────────────────

def validate(record: SymbolicRecord) -> bool:
    """Valid(x) ⟺ Ess(x) ∧ Ω_x.

    Returns True when the record's essence is well-formed **and** its
    constraint is satisfied.
    """
    return record.is_valid


def is_representable(record: SymbolicRecord) -> bool:
    """Representable(x) ⟺ M(x) ∧ T(x).

    Returns True when the record's essence (slot + value) is well-formed,
    regardless of whether the constraint is satisfied.
    """
    return record.is_representable


def is_usable(record: SymbolicRecord) -> bool:
    """Usable(x) ⟺ M(x) ∧ T(x) ∧ Q(x).

    Returns True when the record can actually be *used* in a structural
    context — essence well-formed **and** constraint satisfied.
    """
    return record.is_usable


def match(record: SymbolicRecord) -> bool:
    """M(x) = Match(S_x) — the unit matches its proper slot."""
    return record.match


def containment(record: SymbolicRecord) -> bool:
    """T(x) = Containment(V_x) — the value can enter a higher structure."""
    return record.containment


def constraint_check(record: SymbolicRecord) -> bool:
    """Q(x) = Condition(x) — the constraint is satisfied."""
    return record.constraint_satisfied


# ── Batch validation ─────────────────────────────────────────────────

def validate_batch(
    records: List[SymbolicRecord],
) -> Dict[str, bool]:
    """Validate a batch of records, returning a dict of id → validity."""
    return {r.record_id: validate(r) for r in records}


def filter_valid(records: List[SymbolicRecord]) -> List[SymbolicRecord]:
    """Return only valid records from a list."""
    return [r for r in records if validate(r)]


def filter_usable(records: List[SymbolicRecord]) -> List[SymbolicRecord]:
    """Return only usable records from a list."""
    return [r for r in records if is_usable(r)]


# ── Summary / formatting ────────────────────────────────────────────

def format_record_table(records: List[SymbolicRecord]) -> str:
    """Format a list of symbolic records as a human-readable table."""
    if not records:
        return "(empty)"
    header = (
        f"{'ID':<10} {'Type':<8} {'Slot':<6} {'Value':<20} "
        f"{'Ω':<6} {'Status':<14} {'Valid':<6} {'Usable':<6}"
    )
    sep = "─" * len(header)
    lines = [header, sep]
    for r in records:
        lines.append(
            f"{r.record_id:<10} {r.unit_type.name:<8} {r.slot_position:<6} "
            f"{str(r.value_vector):<20} {r.constraint_omega:<6.2f} "
            f"{r.status.name:<14} {str(r.is_valid):<6} "
            f"{str(r.is_usable):<6}"
        )
    return "\n".join(lines)


# ── Internal helpers ─────────────────────────────────────────────────

def _compute_status(
    slot_position: int,
    value_vector: Tuple[int, ...],
    constraint_omega: float,
) -> SymbolicStatus:
    """Derive the :class:`SymbolicStatus` from slot, value, and Ω."""
    has_essence = slot_position >= 0 and len(value_vector) > 0
    if not has_essence:
        return SymbolicStatus.REPRESENTABLE  # ill-formed but recorded
    if constraint_omega > 0.0:
        return SymbolicStatus.VALID
    return SymbolicStatus.REPRESENTABLE
