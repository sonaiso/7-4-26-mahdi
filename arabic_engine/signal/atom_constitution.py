"""Unicode Atom Constitution v1 — دستور الذرة اليونيكودية.

Implements the fractal-law pipeline (المادة 62):

    التقاط → تعيين → تصنيف → وظيفة → تشاكل → صلاحية → عبور/رد
    capture → designate → classify → function → bind → validate → gate

Every function in this module is **pure** — no side effects, no global
state — satisfying the testability principle (المادة 54).

The single public entry point is :func:`constitute`.

Example::

    >>> from arabic_engine.signal.atom_constitution import constitute
    >>> result = constitute("بِسْمِ")
    >>> len(result.passed) > 0
    True
"""

from __future__ import annotations

from typing import List, Tuple

from arabic_engine.core.enums import (
    ActivationStage,
    AtomFunction,
    AtomGate,
    AtomReadiness,
    AtomType,
)
from arabic_engine.core.types import (
    AtomBinding,
    AtomConstitutionResult,
    ConstitutionalAtom,
    DecisionTrace,
    UnicodeAtom,
)
from arabic_engine.signal.unicode_atoms import decompose

# ── Tatweel code-point — classified as COMPOSITE ────────────────────
_TATWEEL_CP = 0x0640

# ── Unicode general-category → AtomType mapping ────────────────────
_CATEGORY_TO_ATOM_TYPE: dict[str, AtomType] = {
    # Letters → LITERAL (المادة 11)
    "Lo": AtomType.LITERAL,
    "Ll": AtomType.LITERAL,
    "Lu": AtomType.LITERAL,
    "Lt": AtomType.LITERAL,
    "Lm": AtomType.LITERAL,
    # Combining marks → DIACRITICAL (المادة 12)
    "Mn": AtomType.DIACRITICAL,
    "Mc": AtomType.DIACRITICAL,
    "Me": AtomType.DIACRITICAL,
    # Punctuation / symbols → MARKER (المادة 13)
    "Po": AtomType.MARKER,
    "Pi": AtomType.MARKER,
    "Pf": AtomType.MARKER,
    "Ps": AtomType.MARKER,
    "Pe": AtomType.MARKER,
    "Pd": AtomType.MARKER,
    "Sm": AtomType.MARKER,
    "Sk": AtomType.MARKER,
    "So": AtomType.MARKER,
    "Sc": AtomType.MARKER,
    # Whitespace / control → SEPARATOR (المادة 14)
    "Zs": AtomType.SEPARATOR,
    "Zl": AtomType.SEPARATOR,
    "Zp": AtomType.SEPARATOR,
    "Cc": AtomType.SEPARATOR,
    "Cf": AtomType.SEPARATOR,
    # Numerals → SPECIAL_SYMBOL (المادة 15)
    "Nd": AtomType.SPECIAL_SYMBOL,
    "Nl": AtomType.SPECIAL_SYMBOL,
    "No": AtomType.SPECIAL_SYMBOL,
}

# ── AtomType → default AtomFunction mapping ─────────────────────────
_TYPE_TO_FUNCTION: dict[AtomType, AtomFunction] = {
    AtomType.LITERAL: AtomFunction.REPRESENTATION,
    AtomType.DIACRITICAL: AtomFunction.CONSTRAINT,
    AtomType.MARKER: AtomFunction.DISTINCTION,
    AtomType.SEPARATOR: AtomFunction.SEPARATION,
    AtomType.SPECIAL_SYMBOL: AtomFunction.ALERT,
    AtomType.COMPOSITE: AtomFunction.BINDING,
    AtomType.ANOMALOUS: AtomFunction.CORRUPTION,
}


# ════════════════════════════════════════════════════════════════════
# Pipeline stages (all pure functions)
# ════════════════════════════════════════════════════════════════════


def capture(text: str) -> List[UnicodeAtom]:
    """الالتقاط — capture raw text as Unicode atoms (المادة 63).

    Delegates to the existing :func:`decompose` function.
    """
    return decompose(text)


def designate(atom: UnicodeAtom) -> bool:
    """التعيين — determine if a raw unit qualifies as a Unicode atom (المادة 64).

    Returns ``True`` when the code-point is a valid, assigned Unicode
    character (not a surrogate, not unassigned ``Cn``).
    """
    cat = atom.unicode_category
    # Surrogates (Cs) and unassigned (Cn) are not valid atoms
    if cat in ("Cs", "Cn"):
        return False
    return True


def classify(atom: UnicodeAtom) -> AtomType:
    """التصنيف — classify the atom into a constitutional type (المادة 65).

    Special case: tatweel (U+0640) is classified as COMPOSITE because
    it has dual letter/separator nature (المادة 37).
    """
    # Special case: tatweel
    if atom.codepoint == _TATWEEL_CP:
        return AtomType.COMPOSITE

    cat = atom.unicode_category
    return _CATEGORY_TO_ATOM_TYPE.get(cat, AtomType.ANOMALOUS)


def assign_function(atom: UnicodeAtom, atom_type: AtomType) -> AtomFunction:
    """الوظيفة — assign the primary operational function (المادة 66)."""
    return _TYPE_TO_FUNCTION[atom_type]


def bind(
    atom: UnicodeAtom,
    atom_type: AtomType,
    atom_function: AtomFunction,
) -> AtomBinding:
    """التشاكل — create the initial operational binding (المادة 67).

    Determines *combinable* from the combining class and type:

    * Combining marks (``combining_class > 0``) → combinable.
    * Base letters (LITERAL) → combinable (can receive marks).
    * Composites → combinable.
    * Separators / anomalous → not combinable.

    *approved* is ``False`` only for ANOMALOUS atoms.
    """
    combinable: bool
    if atom.combining_class > 0:
        combinable = True
    elif atom_type in (AtomType.LITERAL, AtomType.COMPOSITE, AtomType.DIACRITICAL):
        combinable = True
    else:
        combinable = False

    approved = atom_type != AtomType.ANOMALOUS

    return AtomBinding(
        atom_type=atom_type,
        atom_function=atom_function,
        combinable=combinable,
        approved=approved,
    )


def _neighbor_relation(
    position: int,
    total: int,
    atom_type: AtomType,
) -> str:
    """Compute a preliminary neighbor-relation label."""
    if total <= 1:
        return "isolated"
    if position == 0:
        return "sequence_start"
    if position == total - 1:
        return "sequence_end"
    if atom_type == AtomType.DIACRITICAL:
        return "attached_to_preceding"
    return "interior"


def validate(
    atom: UnicodeAtom,
    atom_type: AtomType,
    binding: AtomBinding,
    position: int,
    total: int,
) -> Tuple[bool, AtomReadiness]:
    """الصلاحية — check constitutional validity conditions (المادة 68).

    The six conditions of المادة 39:

    1. Exists in the sequence (trivially true after capture).
    2. Classifiable into a recognised type.
    3. Initial binding is complete.
    4. Not a blocking anomaly.
    5. Has a valid position.
    6. Has an assigned function.

    Returns ``(valid, readiness_level)``.
    """
    # Condition 2: classifiable
    if atom_type == AtomType.ANOMALOUS:
        return False, AtomReadiness.READY_1

    # Condition 3: binding complete (always true here, but guard)
    if binding is None:  # pragma: no cover — defensive
        return False, AtomReadiness.READY_1

    # Condition 4: not a blocking anomaly
    if not binding.approved:
        return False, AtomReadiness.READY_2

    # Condition 5: valid position
    if position < 0 or position >= total:
        return False, AtomReadiness.READY_2

    # Condition 6: has an assigned function (binding always has one)
    # All checks passed
    return True, AtomReadiness.READY_4


def gate_decision(
    valid: bool,
    atom_type: AtomType,
    binding: AtomBinding,
) -> Tuple[AtomGate, str]:
    """العبور أو الرد — compute the gate decision (المادة 69).

    Priority (المادة 50):

    * **REJECT** — absolute corruption (surrogates, unassigned).
    * **SUSPEND** — ambiguous / composite needing context.
    * **COMPLETE** — fixable (unnormalised form).
    * **PASS** — all conditions met.
    """
    if not binding.approved:
        return AtomGate.REJECT, "atom is anomalous and unapproved (المادة 47)"

    if not valid:
        return AtomGate.REJECT, "atom failed validity checks (المادة 41)"

    if atom_type == AtomType.COMPOSITE:
        return AtomGate.SUSPEND, "composite atom requires contextual resolution (المادة 48)"

    return AtomGate.PASS, "all constitutional conditions met (المادة 45)"


# ════════════════════════════════════════════════════════════════════
# Public API
# ════════════════════════════════════════════════════════════════════


def constitute(text: str) -> AtomConstitutionResult:
    """دستور الذرة اليونيكودية — run the full constitution pipeline.

    Orchestrates the fractal-law stages (المادة 62):

    1. **Capture** — decompose text into raw atoms.
    2. **Designate** — verify each unit is a valid Unicode atom.
    3. **Classify** — assign a constitutional type.
    4. **Function** — assign a primary operational function.
    5. **Bind** — create the initial binding.
    6. **Validate** — check constitutional validity.
    7. **Gate** — pass / suspend / complete / reject.

    Parameters
    ----------
    text : str
        Raw input text (may be empty).

    Returns
    -------
    AtomConstitutionResult
        Partitioned atoms with decision traces.
    """
    if not text:
        return AtomConstitutionResult(
            atoms=(),
            passed=(),
            suspended=(),
            rejected=(),
            traces=(),
        )

    raw_atoms = capture(text)
    total = len(raw_atoms)

    constitutional: List[ConstitutionalAtom] = []
    passed: List[ConstitutionalAtom] = []
    suspended: List[ConstitutionalAtom] = []
    rejected: List[ConstitutionalAtom] = []
    traces: List[DecisionTrace] = []

    for atom in raw_atoms:
        pos = atom.position_index

        # Stage 1: designate
        is_designated = designate(atom)

        if not is_designated:
            # Undesignated → ANOMALOUS → REJECT
            a_type = AtomType.ANOMALOUS
            a_func = AtomFunction.CORRUPTION
            a_binding = AtomBinding(
                atom_type=a_type,
                atom_function=a_func,
                combinable=False,
                approved=False,
            )
            ca = ConstitutionalAtom(
                raw=atom,
                atom_type=a_type,
                atom_function=a_func,
                binding=a_binding,
                position=pos,
                neighbor_rel=_neighbor_relation(pos, total, a_type),
                valid=False,
                gate=AtomGate.REJECT,
                readiness=AtomReadiness.READY_1,
                gate_reason="unit failed designation — invalid code-point (المادة 64)",
            )
            constitutional.append(ca)
            rejected.append(ca)
            traces.append(
                DecisionTrace(
                    trace_id=f"CT_{pos}",
                    stage=ActivationStage.SIGNAL,
                    decision_type="constitution_reject",
                    input_refs=(atom.atom_id,),
                    output_refs=(),
                    applied_rules=("designation_failure",),
                    justification=ca.gate_reason,
                )
            )
            continue

        # Stage 2–4: classify → function → bind
        a_type = classify(atom)
        a_func = assign_function(atom, a_type)
        a_binding = bind(atom, a_type, a_func)

        # Stage 5: validate
        is_valid, readiness = validate(atom, a_type, a_binding, pos, total)

        # Stage 6: gate
        gate, reason = gate_decision(is_valid, a_type, a_binding)

        # Assemble the constitutional atom
        ca = ConstitutionalAtom(
            raw=atom,
            atom_type=a_type,
            atom_function=a_func,
            binding=a_binding,
            position=pos,
            neighbor_rel=_neighbor_relation(pos, total, a_type),
            valid=is_valid,
            gate=gate,
            readiness=readiness if is_valid else readiness,
            gate_reason=reason,
        )
        constitutional.append(ca)

        # Partition
        if gate == AtomGate.PASS:
            passed.append(ca)
        elif gate == AtomGate.SUSPEND:
            suspended.append(ca)
            traces.append(
                DecisionTrace(
                    trace_id=f"CT_{pos}",
                    stage=ActivationStage.SIGNAL,
                    decision_type="constitution_suspend",
                    input_refs=(atom.atom_id,),
                    output_refs=(),
                    applied_rules=("composite_contextual",),
                    justification=reason,
                )
            )
        else:  # REJECT or COMPLETE
            rejected.append(ca)
            traces.append(
                DecisionTrace(
                    trace_id=f"CT_{pos}",
                    stage=ActivationStage.SIGNAL,
                    decision_type="constitution_reject",
                    input_refs=(atom.atom_id,),
                    output_refs=(),
                    applied_rules=("validity_failure",),
                    justification=reason,
                )
            )

    return AtomConstitutionResult(
        atoms=tuple(constitutional),
        passed=tuple(passed),
        suspended=tuple(suspended),
        rejected=tuple(rejected),
        traces=tuple(traces),
    )
