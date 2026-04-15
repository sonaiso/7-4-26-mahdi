"""Tests for symbolic encoding — ترميز الحرف والحركة.

Validates the refined axiom::

    Ess(x) = ⟨Slot, Value⟩
    Valid(x) ⟺ Ess(x) ∧ Ω_x

And the Match / Containment / Commitment model::

    Representable(x) ⟺ M(x) ∧ T(x)
    Usable(x)        ⟺ M(x) ∧ T(x) ∧ Q(x)
"""

from __future__ import annotations

import pytest

from arabic_engine.core.enums import (
    ConstraintKind,
    OntologicalLayer,
    PhonGroup,
    SymbolicStatus,
    UnitType,
)
from arabic_engine.core.types import LetterRecord, VowelRecord
from arabic_engine.signifier.symbolic_encoding import (
    constraint_check,
    containment,
    filter_usable,
    filter_valid,
    format_record_table,
    is_representable,
    is_usable,
    make_letter,
    make_vowel,
    match,
    validate,
    validate_batch,
)

# ── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def dal_letter() -> LetterRecord:
    """The letter Dāl (د) — a valid consonant with no blocking constraint."""
    return make_letter(
        record_id="LR_DAL",
        slot_position=4,
        slot_label="أسناني-لثوي / chain position 4",
        value_vector=(0x062F, 1, 0, 0, 1),
        value_label="دال — consonantal identity + syllabic potential",
        phonetic_group=PhonGroup.ASN_LTH,
        syllabic_weight=1,
        constraints=frozenset({ConstraintKind.POSITIONAL, ConstraintKind.ADJACENCY}),
        constraint_omega=1.0,
    )


@pytest.fixture
def ba_letter() -> LetterRecord:
    """The letter Bā' (ب) — valid consonant."""
    return make_letter(
        record_id="LR_BA",
        slot_position=2,
        slot_label="شفوي / chain position 2",
        value_vector=(0x0628, 1, 0, 0, 1),
        value_label="باء — consonantal identity",
        phonetic_group=PhonGroup.SHF,
        syllabic_weight=1,
        constraints=frozenset({ConstraintKind.POSITIONAL}),
        constraint_omega=1.0,
    )


@pytest.fixture
def blocked_letter() -> LetterRecord:
    """A letter with constraint_omega = 0 — blocked by context."""
    return make_letter(
        record_id="LR_BLOCKED",
        slot_position=5,
        slot_label="blocked position",
        value_vector=(0x062F, 1, 0, 0, 1),
        value_label="blocked dāl",
        constraint_omega=0.0,
        constraints=frozenset({ConstraintKind.ADJACENCY}),
    )


@pytest.fixture
def fatha_vowel() -> VowelRecord:
    """The vowel Fatḥa (◌َ) — a valid short vowel attached to a carrier."""
    return make_vowel(
        record_id="VR_FATHA",
        slot_position=4,
        slot_label="dependent on carrier LR_DAL",
        value_vector=(0x064E, 1, 0),
        value_label="فتحة — short open vowel",
        carrier_id="LR_DAL",
        constraints=frozenset({ConstraintKind.CARRIER, ConstraintKind.SYLLABIC}),
        constraint_omega=1.0,
    )


@pytest.fixture
def damma_vowel() -> VowelRecord:
    """The vowel Ḍamma (◌ُ) — valid short vowel."""
    return make_vowel(
        record_id="VR_DAMMA",
        slot_position=4,
        slot_label="dependent on carrier LR_DAL",
        value_vector=(0x064F, 1, 0),
        value_label="ضمة — short close vowel",
        carrier_id="LR_DAL",
        constraints=frozenset({ConstraintKind.CARRIER}),
        constraint_omega=1.0,
    )


@pytest.fixture
def blocked_vowel() -> VowelRecord:
    """A vowel with no carrier — constraint blocked."""
    return make_vowel(
        record_id="VR_BLOCKED",
        slot_position=4,
        slot_label="no carrier",
        value_vector=(0x064E, 1, 0),
        value_label="blocked fatha",
        carrier_id=None,
        constraint_omega=0.0,
        constraints=frozenset({ConstraintKind.CARRIER}),
    )


# ── Enum tests ───────────────────────────────────────────────────────

class TestEnums:
    """Validate new enums exist and have correct members."""

    def test_unit_type_has_letter_and_vowel(self):
        assert UnitType.LETTER.value
        assert UnitType.VOWEL.value
        assert UnitType.LETTER is not UnitType.VOWEL

    def test_symbolic_status_values(self):
        assert SymbolicStatus.REPRESENTABLE.value
        assert SymbolicStatus.VALID.value
        assert SymbolicStatus.PROMOTABLE.value
        assert len(SymbolicStatus) == 3

    def test_constraint_kind_values(self):
        expected = {"POSITIONAL", "ADJACENCY", "CARRIER", "SYLLABIC", "LAYER"}
        actual = {c.name for c in ConstraintKind}
        assert actual == expected


# ── SymbolicRecord core tests ────────────────────────────────────────

class TestSymbolicRecordCore:
    """Test the generic SymbolicRecord essence / constraint / validation."""

    def test_core_returns_slot_and_value(self, dal_letter):
        slot, value = dal_letter.core
        assert slot == 4
        assert value == (0x062F, 1, 0, 0, 1)

    def test_is_representable_true(self, dal_letter):
        assert dal_letter.is_representable is True

    def test_is_representable_false_negative_slot(self):
        rec = make_letter(
            record_id="X", slot_position=-1, slot_label="bad",
            value_vector=(1,), value_label="bad",
        )
        assert rec.is_representable is False

    def test_is_representable_false_empty_value(self):
        rec = make_letter(
            record_id="X", slot_position=0, slot_label="ok",
            value_vector=(), value_label="empty",
        )
        assert rec.is_representable is False

    def test_constraint_satisfied_true(self, dal_letter):
        assert dal_letter.constraint_satisfied is True

    def test_constraint_satisfied_false(self, blocked_letter):
        assert blocked_letter.constraint_satisfied is False

    def test_is_valid_true(self, dal_letter):
        assert dal_letter.is_valid is True

    def test_is_valid_false_when_blocked(self, blocked_letter):
        assert blocked_letter.is_valid is False

    def test_is_valid_false_bad_essence(self):
        rec = make_letter(
            record_id="X", slot_position=-1, slot_label="bad",
            value_vector=(1,), value_label="bad", constraint_omega=1.0,
        )
        assert rec.is_valid is False

    def test_frozen(self, dal_letter):
        with pytest.raises(AttributeError):
            dal_letter.record_id = "changed"  # type: ignore[misc]


# ── Match / Containment / Usability ─────────────────────────────────

class TestMatchContainment:
    """Test the M(x), T(x), Q(x) predicates."""

    def test_match_true(self, dal_letter):
        assert match(dal_letter) is True

    def test_containment_true(self, dal_letter):
        assert containment(dal_letter) is True

    def test_constraint_check_true(self, dal_letter):
        assert constraint_check(dal_letter) is True

    def test_constraint_check_false(self, blocked_letter):
        assert constraint_check(blocked_letter) is False

    def test_usable_when_all_true(self, dal_letter):
        assert is_usable(dal_letter) is True

    def test_not_usable_when_constraint_false(self, blocked_letter):
        assert is_usable(blocked_letter) is False

    def test_representable_but_not_usable(self, blocked_letter):
        """A blocked letter is representable but not usable."""
        assert is_representable(blocked_letter) is True
        assert is_usable(blocked_letter) is False


# ── LetterRecord tests ───────────────────────────────────────────────

class TestLetterRecord:
    """Test letter-specific encoding."""

    def test_unit_type_is_letter(self, dal_letter):
        assert dal_letter.unit_type is UnitType.LETTER

    def test_phonetic_group(self, dal_letter):
        assert dal_letter.phonetic_group is PhonGroup.ASN_LTH

    def test_syllabic_weight(self, dal_letter):
        assert dal_letter.syllabic_weight == 1

    def test_wrong_unit_type_raises(self):
        with pytest.raises(ValueError, match="UnitType.LETTER"):
            LetterRecord(
                record_id="X", unit_type=UnitType.VOWEL,
                slot_position=0, slot_label="x",
                value_vector=(1,), value_label="x",
            )

    def test_status_valid_when_omega_positive(self, dal_letter):
        assert dal_letter.status is SymbolicStatus.VALID

    def test_status_representable_when_omega_zero(self, blocked_letter):
        assert blocked_letter.status is SymbolicStatus.REPRESENTABLE

    def test_to_row_keys(self, dal_letter):
        row = dal_letter.to_row()
        expected_keys = {
            "Record_ID", "Unit_Type", "Slot_Position", "Slot_Label",
            "Value_Vector", "Value_Label", "Constraints", "Constraint_Omega",
            "Layer", "Status", "Core", "Is_Valid", "Is_Usable",
        }
        assert set(row.keys()) == expected_keys

    def test_to_row_is_valid(self, dal_letter):
        assert dal_letter.to_row()["Is_Valid"] is True

    def test_to_row_blocked(self, blocked_letter):
        row = blocked_letter.to_row()
        assert row["Is_Valid"] is False
        assert row["Is_Usable"] is False

    def test_dal_full_example(self, dal_letter):
        """مثال 1: الدال — end-to-end."""
        assert dal_letter.is_representable is True
        assert dal_letter.constraint_satisfied is True
        assert dal_letter.is_valid is True
        assert dal_letter.is_usable is True


# ── VowelRecord tests ────────────────────────────────────────────────

class TestVowelRecord:
    """Test vowel-specific encoding."""

    def test_unit_type_is_vowel(self, fatha_vowel):
        assert fatha_vowel.unit_type is UnitType.VOWEL

    def test_carrier_id(self, fatha_vowel):
        assert fatha_vowel.carrier_id == "LR_DAL"

    def test_is_long_default_false(self, fatha_vowel):
        assert fatha_vowel.is_long is False

    def test_long_vowel(self):
        v = make_vowel(
            record_id="VR_LONG", slot_position=4,
            slot_label="madd", value_vector=(0x0627, 1, 1),
            value_label="ألف مد", is_long=True, carrier_id="LR_DAL",
        )
        assert v.is_long is True

    def test_wrong_unit_type_raises(self):
        with pytest.raises(ValueError, match="UnitType.VOWEL"):
            VowelRecord(
                record_id="X", unit_type=UnitType.LETTER,
                slot_position=0, slot_label="x",
                value_vector=(1,), value_label="x",
            )

    def test_blocked_vowel_not_valid(self, blocked_vowel):
        assert blocked_vowel.is_valid is False
        assert blocked_vowel.is_usable is False
        assert blocked_vowel.is_representable is True

    def test_fatha_full_example(self, fatha_vowel):
        """مثال 2: الفتحة — end-to-end."""
        assert fatha_vowel.is_representable is True
        assert fatha_vowel.constraint_satisfied is True
        assert fatha_vowel.is_valid is True
        assert fatha_vowel.is_usable is True


# ── Module-level function tests ──────────────────────────────────────

class TestModuleFunctions:
    """Test the module-level validation / query functions."""

    def test_validate_true(self, dal_letter):
        assert validate(dal_letter) is True

    def test_validate_false(self, blocked_letter):
        assert validate(blocked_letter) is False

    def test_is_representable_function(self, dal_letter):
        assert is_representable(dal_letter) is True

    def test_match_function(self, dal_letter):
        assert match(dal_letter) is True

    def test_containment_function(self, dal_letter):
        assert containment(dal_letter) is True

    def test_validate_batch(self, dal_letter, blocked_letter, fatha_vowel):
        result = validate_batch([dal_letter, blocked_letter, fatha_vowel])
        assert result == {
            "LR_DAL": True,
            "LR_BLOCKED": False,
            "VR_FATHA": True,
        }

    def test_filter_valid(self, dal_letter, blocked_letter, fatha_vowel):
        valid = filter_valid([dal_letter, blocked_letter, fatha_vowel])
        ids = [r.record_id for r in valid]
        assert "LR_DAL" in ids
        assert "VR_FATHA" in ids
        assert "LR_BLOCKED" not in ids

    def test_filter_usable(
        self, dal_letter, blocked_letter, fatha_vowel, blocked_vowel,
    ):
        usable = filter_usable(
            [dal_letter, blocked_letter, fatha_vowel, blocked_vowel]
        )
        ids = [r.record_id for r in usable]
        assert "LR_DAL" in ids
        assert "VR_FATHA" in ids
        assert "LR_BLOCKED" not in ids
        assert "VR_BLOCKED" not in ids


# ── Format table ─────────────────────────────────────────────────────

class TestFormatTable:
    """Test the human-readable table formatter."""

    def test_empty_returns_marker(self):
        assert format_record_table([]) == "(empty)"

    def test_table_has_header(self, dal_letter):
        table = format_record_table([dal_letter])
        assert "ID" in table
        assert "Type" in table
        assert "Ω" in table

    def test_table_contains_record(self, dal_letter):
        table = format_record_table([dal_letter])
        assert "LR_DAL" in table

    def test_table_multiple_records(self, dal_letter, fatha_vowel):
        table = format_record_table([dal_letter, fatha_vowel])
        assert "LR_DAL" in table
        assert "VR_FATHA" in table


# ── Edge cases ───────────────────────────────────────────────────────

class TestEdgeCases:
    """Boundary / edge-case tests."""

    def test_slot_zero_is_valid(self):
        """Slot position 0 is valid (first position)."""
        rec = make_letter(
            record_id="E0", slot_position=0, slot_label="first",
            value_vector=(1,), value_label="ok",
        )
        assert rec.is_representable is True
        assert rec.is_valid is True

    def test_fractional_omega(self):
        """Fractional Ω > 0 still counts as satisfied."""
        rec = make_letter(
            record_id="E1", slot_position=1, slot_label="frac",
            value_vector=(1,), value_label="ok", constraint_omega=0.01,
        )
        assert rec.constraint_satisfied is True
        assert rec.is_valid is True

    def test_omega_exactly_zero_blocks(self):
        rec = make_letter(
            record_id="E2", slot_position=1, slot_label="zero",
            value_vector=(1,), value_label="ok", constraint_omega=0.0,
        )
        assert rec.constraint_satisfied is False
        assert rec.is_valid is False

    def test_layer_defaults_to_cell(self, dal_letter):
        assert dal_letter.layer is OntologicalLayer.CELL

    def test_vowel_no_carrier(self):
        """Vowel without carrier is representable but we can still create it."""
        v = make_vowel(
            record_id="NC", slot_position=0, slot_label="no carrier",
            value_vector=(0x064E, 1, 0), value_label="fatha",
            carrier_id=None, constraint_omega=1.0,
        )
        assert v.carrier_id is None
        assert v.is_valid is True

    def test_empty_constraints_frozenset(self):
        rec = make_letter(
            record_id="EC", slot_position=1, slot_label="ec",
            value_vector=(1,), value_label="ok",
        )
        assert rec.constraints == frozenset()

    def test_multiple_constraints(self):
        rec = make_letter(
            record_id="MC", slot_position=1, slot_label="mc",
            value_vector=(1,), value_label="ok",
            constraints=frozenset({
                ConstraintKind.POSITIONAL,
                ConstraintKind.ADJACENCY,
                ConstraintKind.LAYER,
            }),
        )
        assert len(rec.constraints) == 3
        assert ConstraintKind.LAYER in rec.constraints
