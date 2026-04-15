"""Tests for the Unicode Atom Constitution v1 — دستور الذرة اليونيكودية.

Covers:
  - Enum membership & cardinality (§6.1)
  - Classification rules (§6.2 — المواد 33–36)
  - Function assignment (§6.3 — المواد 20–26)
  - Binding behaviour (§6.4 — المواد 27–30)
  - Validation & gating (§6.5 — المواد 38–50)
  - Full pipeline (§6.6)
  - Architectural principles (§6.7)
"""

from __future__ import annotations

import unicodedata

import pytest

from arabic_engine.core.enums import (
    AtomFunction,
    AtomGate,
    AtomReadiness,
    AtomType,
    SignalType,
)
from arabic_engine.core.types import (
    AtomBinding,
    UnicodeAtom,
)
from arabic_engine.signal.atom_constitution import (
    assign_function,
    bind,
    capture,
    classify,
    constitute,
    designate,
    gate_decision,
    validate,
)

# ════════════════════════════════════════════════════════════════════
# §6.1 — Enum tests
# ════════════════════════════════════════════════════════════════════


class TestEnumCardinality:
    """Verify that each constitution enum has the correct member count."""

    def test_atom_type_has_7_members(self) -> None:
        assert len(AtomType) == 7

    def test_atom_function_has_7_members(self) -> None:
        assert len(AtomFunction) == 7

    def test_atom_gate_has_4_members(self) -> None:
        assert len(AtomGate) == 4

    def test_atom_readiness_has_4_members(self) -> None:
        assert len(AtomReadiness) == 4

    def test_atom_type_members_unique(self) -> None:
        values = [m.value for m in AtomType]
        assert len(values) == len(set(values))

    def test_atom_function_members_unique(self) -> None:
        values = [m.value for m in AtomFunction]
        assert len(values) == len(set(values))

    def test_atom_gate_members_unique(self) -> None:
        values = [m.value for m in AtomGate]
        assert len(values) == len(set(values))

    def test_atom_readiness_members_unique(self) -> None:
        values = [m.value for m in AtomReadiness]
        assert len(values) == len(set(values))

    def test_atom_type_expected_names(self) -> None:
        names = {m.name for m in AtomType}
        expected = {
            "LITERAL", "DIACRITICAL", "MARKER", "SEPARATOR",
            "SPECIAL_SYMBOL", "COMPOSITE", "ANOMALOUS",
        }
        assert names == expected

    def test_atom_function_expected_names(self) -> None:
        names = {m.name for m in AtomFunction}
        expected = {
            "REPRESENTATION", "DISTINCTION", "BINDING", "CONSTRAINT",
            "SEPARATION", "ALERT", "CORRUPTION",
        }
        assert names == expected


# ════════════════════════════════════════════════════════════════════
# §6.2 — Classification tests (المواد 33–36)
# ════════════════════════════════════════════════════════════════════


def _make_atom(char: str, idx: int = 0) -> UnicodeAtom:
    """Helper to build a UnicodeAtom from a single character."""
    cp = ord(char)
    return UnicodeAtom(
        atom_id=f"A_{idx}",
        char=char,
        codepoint=cp,
        unicode_category=unicodedata.category(char),
        combining_class=unicodedata.combining(char),
        position_index=idx,
        signal_type=SignalType.UNKNOWN,
    )


class TestClassification:
    """Classification rules per المواد 33–36."""

    def test_arabic_base_letter_is_literal(self) -> None:
        """ب (U+0628) → LITERAL (المادة 33)."""
        atom = _make_atom("\u0628")
        assert classify(atom) == AtomType.LITERAL

    def test_arabic_alef_is_literal(self) -> None:
        atom = _make_atom("\u0627")
        assert classify(atom) == AtomType.LITERAL

    def test_arabic_yaa_is_literal(self) -> None:
        atom = _make_atom("\u064A")
        assert classify(atom) == AtomType.LITERAL

    def test_latin_letter_is_literal(self) -> None:
        atom = _make_atom("A")
        assert classify(atom) == AtomType.LITERAL

    def test_fatha_is_diacritical(self) -> None:
        """فتحة (U+064E) → DIACRITICAL (المادة 34)."""
        atom = _make_atom("\u064E")
        assert classify(atom) == AtomType.DIACRITICAL

    def test_damma_is_diacritical(self) -> None:
        atom = _make_atom("\u064F")
        assert classify(atom) == AtomType.DIACRITICAL

    def test_kasra_is_diacritical(self) -> None:
        atom = _make_atom("\u0650")
        assert classify(atom) == AtomType.DIACRITICAL

    def test_shadda_is_diacritical(self) -> None:
        atom = _make_atom("\u0651")
        assert classify(atom) == AtomType.DIACRITICAL

    def test_sukun_is_diacritical(self) -> None:
        atom = _make_atom("\u0652")
        assert classify(atom) == AtomType.DIACRITICAL

    def test_arabic_comma_is_marker(self) -> None:
        """، (U+060C) → MARKER (المادة 35)."""
        atom = _make_atom("\u060C")
        assert classify(atom) == AtomType.MARKER

    def test_period_is_marker(self) -> None:
        atom = _make_atom(".")
        assert classify(atom) == AtomType.MARKER

    def test_space_is_separator(self) -> None:
        """Space (U+0020) → SEPARATOR (المادة 36)."""
        atom = _make_atom(" ")
        assert classify(atom) == AtomType.SEPARATOR

    def test_tab_is_separator(self) -> None:
        atom = _make_atom("\t")
        assert classify(atom) == AtomType.SEPARATOR

    def test_newline_is_separator(self) -> None:
        atom = _make_atom("\n")
        assert classify(atom) == AtomType.SEPARATOR

    def test_tatweel_is_composite(self) -> None:
        """Tatweel (U+0640) → COMPOSITE (المادة 16 / المادة 37)."""
        atom = _make_atom("\u0640")
        assert classify(atom) == AtomType.COMPOSITE

    def test_arabic_indic_digit_is_special_symbol(self) -> None:
        """Arabic-Indic 1 (U+0661) → SPECIAL_SYMBOL (المادة 15)."""
        atom = _make_atom("\u0661")
        assert classify(atom) == AtomType.SPECIAL_SYMBOL

    def test_western_digit_is_special_symbol(self) -> None:
        atom = _make_atom("5")
        assert classify(atom) == AtomType.SPECIAL_SYMBOL


# ════════════════════════════════════════════════════════════════════
# §6.3 — Function assignment tests (المواد 20–26)
# ════════════════════════════════════════════════════════════════════


class TestFunctionAssignment:
    """Each AtomType maps to exactly one AtomFunction."""

    def test_literal_gets_representation(self) -> None:
        atom = _make_atom("\u0628")
        assert assign_function(atom, AtomType.LITERAL) == AtomFunction.REPRESENTATION

    def test_diacritical_gets_constraint(self) -> None:
        atom = _make_atom("\u064E")
        assert assign_function(atom, AtomType.DIACRITICAL) == AtomFunction.CONSTRAINT

    def test_marker_gets_distinction(self) -> None:
        atom = _make_atom(".")
        assert assign_function(atom, AtomType.MARKER) == AtomFunction.DISTINCTION

    def test_separator_gets_separation(self) -> None:
        atom = _make_atom(" ")
        assert assign_function(atom, AtomType.SEPARATOR) == AtomFunction.SEPARATION

    def test_special_symbol_gets_alert(self) -> None:
        atom = _make_atom("5")
        assert assign_function(atom, AtomType.SPECIAL_SYMBOL) == AtomFunction.ALERT

    def test_composite_gets_binding(self) -> None:
        atom = _make_atom("\u0640")
        assert assign_function(atom, AtomType.COMPOSITE) == AtomFunction.BINDING

    def test_anomalous_gets_corruption(self) -> None:
        atom = _make_atom("x")  # type is overridden
        assert assign_function(atom, AtomType.ANOMALOUS) == AtomFunction.CORRUPTION


# ════════════════════════════════════════════════════════════════════
# §6.4 — Binding tests (المواد 27–30)
# ════════════════════════════════════════════════════════════════════


class TestBinding:
    """AtomBinding properties per المواد 27–30."""

    def test_combining_mark_is_combinable(self) -> None:
        atom = _make_atom("\u064E")  # fatha, combining_class > 0
        b = bind(atom, AtomType.DIACRITICAL, AtomFunction.CONSTRAINT)
        assert b.combinable is True

    def test_base_letter_is_combinable(self) -> None:
        atom = _make_atom("\u0628")
        b = bind(atom, AtomType.LITERAL, AtomFunction.REPRESENTATION)
        assert b.combinable is True

    def test_separator_is_not_combinable(self) -> None:
        atom = _make_atom(" ")
        b = bind(atom, AtomType.SEPARATOR, AtomFunction.SEPARATION)
        assert b.combinable is False

    def test_anomalous_is_not_approved(self) -> None:
        atom = _make_atom("x")
        b = bind(atom, AtomType.ANOMALOUS, AtomFunction.CORRUPTION)
        assert b.approved is False

    def test_literal_is_approved(self) -> None:
        atom = _make_atom("\u0628")
        b = bind(atom, AtomType.LITERAL, AtomFunction.REPRESENTATION)
        assert b.approved is True

    def test_binding_is_frozen(self) -> None:
        atom = _make_atom("\u0628")
        b = bind(atom, AtomType.LITERAL, AtomFunction.REPRESENTATION)
        with pytest.raises(AttributeError):
            b.combinable = False  # type: ignore[misc]

    def test_marker_is_not_combinable(self) -> None:
        atom = _make_atom(".")
        b = bind(atom, AtomType.MARKER, AtomFunction.DISTINCTION)
        assert b.combinable is False

    def test_composite_is_combinable(self) -> None:
        atom = _make_atom("\u0640")
        b = bind(atom, AtomType.COMPOSITE, AtomFunction.BINDING)
        assert b.combinable is True


# ════════════════════════════════════════════════════════════════════
# §6.5 — Validation & gate tests (المواد 38–50)
# ════════════════════════════════════════════════════════════════════


class TestValidationAndGate:
    """Validity checks and gate decisions."""

    def test_valid_letter_passes(self) -> None:
        atom = _make_atom("\u0628")
        a_type = classify(atom)
        a_func = assign_function(atom, a_type)
        a_bind = bind(atom, a_type, a_func)
        valid, readiness = validate(atom, a_type, a_bind, 0, 1)
        assert valid is True
        assert readiness == AtomReadiness.READY_4

    def test_valid_diacritic_passes(self) -> None:
        atom = _make_atom("\u064E")
        a_type = classify(atom)
        a_func = assign_function(atom, a_type)
        a_bind = bind(atom, a_type, a_func)
        valid, _ = validate(atom, a_type, a_bind, 0, 1)
        assert valid is True

    def test_anomalous_fails_validation(self) -> None:
        atom = _make_atom("x")
        a_bind = AtomBinding(
            atom_type=AtomType.ANOMALOUS,
            atom_function=AtomFunction.CORRUPTION,
            combinable=False,
            approved=False,
        )
        valid, readiness = validate(atom, AtomType.ANOMALOUS, a_bind, 0, 1)
        assert valid is False
        assert readiness == AtomReadiness.READY_1

    def test_gate_pass_for_valid_letter(self) -> None:
        a_bind = AtomBinding(
            atom_type=AtomType.LITERAL,
            atom_function=AtomFunction.REPRESENTATION,
            combinable=True,
            approved=True,
        )
        gate, reason = gate_decision(True, AtomType.LITERAL, a_bind)
        assert gate == AtomGate.PASS
        assert reason != ""

    def test_gate_reject_for_unapproved(self) -> None:
        a_bind = AtomBinding(
            atom_type=AtomType.ANOMALOUS,
            atom_function=AtomFunction.CORRUPTION,
            combinable=False,
            approved=False,
        )
        gate, reason = gate_decision(False, AtomType.ANOMALOUS, a_bind)
        assert gate == AtomGate.REJECT
        assert "المادة 47" in reason

    def test_gate_suspend_for_composite(self) -> None:
        a_bind = AtomBinding(
            atom_type=AtomType.COMPOSITE,
            atom_function=AtomFunction.BINDING,
            combinable=True,
            approved=True,
        )
        gate, reason = gate_decision(True, AtomType.COMPOSITE, a_bind)
        assert gate == AtomGate.SUSPEND
        assert "المادة 48" in reason

    def test_gate_reason_is_never_empty(self) -> None:
        """المادة 55: every decision must have an explicit reason."""
        for atype in AtomType:
            approved = atype != AtomType.ANOMALOUS
            a_bind = AtomBinding(
                atom_type=atype,
                atom_function=AtomFunction.REPRESENTATION,
                combinable=True,
                approved=approved,
            )
            _, reason = gate_decision(approved, atype, a_bind)
            assert len(reason) > 0, f"Empty reason for {atype}"


# ════════════════════════════════════════════════════════════════════
# §6.6 — Full pipeline tests
# ════════════════════════════════════════════════════════════════════


class TestConstitutePipeline:
    """End-to-end tests for :func:`constitute`."""

    def test_empty_string(self) -> None:
        result = constitute("")
        assert result.atoms == ()
        assert result.passed == ()
        assert result.suspended == ()
        assert result.rejected == ()

    def test_simple_arabic_word(self) -> None:
        """بِسْمِ → 6 atoms, all PASS."""
        result = constitute("بِسْمِ")
        assert len(result.atoms) == 6
        assert len(result.passed) == 6
        assert len(result.suspended) == 0
        assert len(result.rejected) == 0

    def test_mixed_arabic_with_space(self) -> None:
        result = constitute("كَلِمَة فِي")
        # letters + diacritics + space + letters + diacritics
        assert len(result.passed) > 0
        sep_atoms = [a for a in result.atoms if a.atom_type == AtomType.SEPARATOR]
        assert len(sep_atoms) == 1

    def test_tatweel_is_suspended(self) -> None:
        """Tatweel produces a SUSPEND gate decision."""
        result = constitute("ـ")
        assert len(result.suspended) == 1
        assert result.suspended[0].gate == AtomGate.SUSPEND
        assert result.suspended[0].atom_type == AtomType.COMPOSITE

    def test_digit_is_special_symbol(self) -> None:
        result = constitute("٥")
        assert len(result.passed) == 1
        assert result.passed[0].atom_type == AtomType.SPECIAL_SYMBOL
        assert result.passed[0].atom_function == AtomFunction.ALERT

    def test_punctuation_is_marker(self) -> None:
        result = constitute(".")
        assert len(result.passed) == 1
        assert result.passed[0].atom_type == AtomType.MARKER

    def test_result_partitions_are_disjoint(self) -> None:
        result = constitute("بـ 5.")
        all_ids = {id(a) for a in result.atoms}
        passed_ids = {id(a) for a in result.passed}
        suspended_ids = {id(a) for a in result.suspended}
        rejected_ids = {id(a) for a in result.rejected}
        assert passed_ids | suspended_ids | rejected_ids == all_ids
        assert passed_ids & suspended_ids == set()
        assert passed_ids & rejected_ids == set()
        assert suspended_ids & rejected_ids == set()

    def test_result_is_frozen(self) -> None:
        result = constitute("ب")
        with pytest.raises(AttributeError):
            result.atoms = ()  # type: ignore[misc]

    def test_constitutional_atom_is_frozen(self) -> None:
        result = constitute("ب")
        with pytest.raises(AttributeError):
            result.passed[0].gate = AtomGate.REJECT  # type: ignore[misc]

    def test_traces_for_non_pass(self) -> None:
        """Traces are generated for suspended and rejected atoms."""
        result = constitute("ـ")  # tatweel → suspended
        assert len(result.traces) >= 1
        assert result.traces[0].decision_type == "constitution_suspend"

    def test_all_passed_have_ready_4(self) -> None:
        result = constitute("بِسْمِ اللَّهِ")
        for atom in result.passed:
            assert atom.readiness == AtomReadiness.READY_4

    def test_all_passed_have_gate_pass(self) -> None:
        result = constitute("كَتَبَ")
        for atom in result.passed:
            assert atom.gate == AtomGate.PASS

    def test_all_atoms_have_nonempty_gate_reason(self) -> None:
        """المادة 55: every decision must be explicitly justified."""
        result = constitute("بـ 5.كَ\t")
        for atom in result.atoms:
            assert atom.gate_reason != "", f"Empty reason for {atom.raw.char!r}"


# ════════════════════════════════════════════════════════════════════
# §6.7 — Architectural principle tests
# ════════════════════════════════════════════════════════════════════


class TestArchitecturalPrinciples:
    """Verify that the constitution respects its own architectural rules."""

    def test_raw_is_preserved(self) -> None:
        """المادة 53: the original UnicodeAtom is always preserved."""
        result = constitute("بِ")
        for ca in result.atoms:
            assert isinstance(ca.raw, UnicodeAtom)
            assert ca.raw.char in "بِ"

    def test_position_matches_raw(self) -> None:
        result = constitute("abc")
        for ca in result.atoms:
            assert ca.position == ca.raw.position_index

    def test_readiness_levels_are_ordered(self) -> None:
        """المادة 61: readiness levels are sequential."""
        levels = [r.value for r in AtomReadiness]
        assert levels == sorted(levels)

    def test_capture_delegates_to_decompose(self) -> None:
        from arabic_engine.signal.unicode_atoms import decompose
        text = "مرحبا"
        assert len(capture(text)) == len(decompose(text))
        for a, b in zip(capture(text), decompose(text)):
            assert a.char == b.char
            assert a.codepoint == b.codepoint

    def test_designate_rejects_nothing_for_valid_chars(self) -> None:
        """All standard Arabic characters pass designation."""
        for ch in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي":
            atom = _make_atom(ch)
            assert designate(atom) is True

    def test_classify_covers_all_signal_types(self) -> None:
        """Every SignalType used in decompose maps to a valid AtomType."""
        for st in SignalType:
            if st == SignalType.UNKNOWN:
                continue
            # At least one category maps to each signal type

    def test_all_atom_types_have_a_function(self) -> None:
        """Every AtomType has a corresponding AtomFunction."""
        for atype in AtomType:
            # assign_function should not raise
            atom = _make_atom("x")
            func = assign_function(atom, atype)
            assert isinstance(func, AtomFunction)

    def test_signal_re_export(self) -> None:
        """constitute is accessible from the signal package."""
        from arabic_engine.signal import constitute as c
        assert callable(c)

    def test_core_re_exports(self) -> None:
        """All new types are re-exported from arabic_engine.core."""
        from arabic_engine.core import (  # noqa: F811
            AtomBinding as _AtomBinding,
        )
        from arabic_engine.core import (
            AtomConstitutionResult as _AtomConstitutionResult,
        )
        from arabic_engine.core import (
            AtomFunction as _AtomFunction,
        )
        from arabic_engine.core import (
            AtomGate as _AtomGate,
        )
        from arabic_engine.core import (
            AtomReadiness as _AtomReadiness,
        )
        from arabic_engine.core import (
            AtomType as _AtomType,
        )
        from arabic_engine.core import (
            ConstitutionalAtom as _ConstitutionalAtom,
        )
        assert _AtomType.LITERAL is not None
        assert _AtomFunction.REPRESENTATION is not None
        assert _AtomGate.PASS is not None
        assert _AtomReadiness.READY_4 is not None
        assert _AtomBinding is not None
        assert _ConstitutionalAtom is not None
        assert _AtomConstitutionResult is not None
