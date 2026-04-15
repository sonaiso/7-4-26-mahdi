# Informational Stock Governance (ISG) Constitution v1

> دستور حوكمة المخزون المعلوماتي — v1.0

## Overview

The ISG Constitution governs the **prior informational stock** (المخزون المعلوماتي السابق) — the pre-existing knowledge that precedes and enables perception. It sits **before** the Composition/Syntax Constitution v1 and before the Lexeme (المفرد), Concept (المفهوم), Referral (الإحالة), Proposition (القضية), and Normative (الحكمي) systems.

### Position in Architecture

```
ISG Constitution v1          ← THIS DOCUMENT
    ↓
Lexeme Admission Constitution v1
    ↓
Concept Admission Constitution v1
    ↓
Composition / Syntax Constitution v1
    ↓
Proposition Constitution v1
    ↓
Normative Gate Constitution v1
```

---

## Fractal Governance Law (المادة 67)

Every knowledge atom passes through a six-step pipeline:

```
تعيين → تصنيف → تحقق → استدعاء → فضّ → عبور/رد
Identify → Classify → Verify → Evaluate Callability → Resolve Conflicts → Gate
```

This law applies fractally at every level of the system.

---

## Constitution-to-Code Mapping

| الباب (Chapter) | Code Construct |
|------------------|---------------|
| الباب 1 (موضوع الوثيقة) | Module docstring in `isg_v1.py` |
| الباب 2 (الذرة المعرفية) | `KnowledgeAtom` type + `KnowledgeAtomType` enum |
| الباب 3 (تصنيف المعرفة السابقة) | `PriorKnowledgeType` enum + `classify_atom()` |
| الباب 4 (فصل المعلومات عن الآراء) | `EpistemicEntryKind` enum + `separate_opinions()` |
| الباب 5 (مطابقة المستوى) | `LevelMatchStatus` enum + `check_level_match()` |
| الباب 6 (التحقق من المصدر) | `SourceRecord` type + `SourceType`/`VerificationStatus` enums + `verify_source()` |
| الباب 7 (صلاحية الاستدعاء) | `CallabilityStatus` enum + `evaluate_callability()` |
| الباب 8 (فضّ التعارض) | `InternalConflictType`/`ISGConflictResolution` enums + `resolve_internal_conflict()` |
| الباب 9 (حدود الانتقال للمفرد) | `GovernanceGateResult` type + `evaluate_gate()` with PASS |
| الباب 10 (حدود الانتقال للحكمي) | `evaluate_gate()` with normative guard |
| الباب 11 (معايير الرد والتعليق) | `GateDecision` enum (REJECT/SUSPEND/COMPLETE) |
| الباب 12 (الجاهزية الدستورية) | `ReadinessLevel` enum + readiness checks |
| الباب 13 (القانون الفراكتالي) | `govern()` implementing the 6-step pipeline |
| الباب 14 (الصياغة الرياضية) | Threshold constants in `isg_seed_data.py` |
| الباب 15 (الصيغة المختصرة) | Module-level docstring |

---

## Enums (12 new — `arabic_engine/core/enums.py`)

| Enum | Members | المادة |
|------|---------|--------|
| `KnowledgeAtomType` | 10 | 8 |
| `PriorKnowledgeType` | 10 | 11 |
| `EpistemicEntryKind` | 5 | 21 |
| `ConfirmationRank` | 5 | 36 |
| `SourceType` | 6 | 35 |
| `LevelMatchStatus` | 7 | 30 |
| `CallabilityStatus` | 3 | 40–41 |
| `InternalConflictType` | 6 | 45 |
| `ISGConflictResolution` | 7 | 47 |
| `GateDecision` | 4 | 73/78 |
| `ReadinessLevel` | 3 | 62–66 |
| `VerificationStatus` | 4 | 34 |

---

## Types (7 new frozen dataclasses — `arabic_engine/core/types.py`)

| Type | Description | المادة |
|------|-------------|--------|
| `KnowledgeAtom` | The fundamental knowledge unit | 5–7 |
| `SourceRecord` | Verification metadata for a source | 34 |
| `LevelMatchResult` | Result of level matching | 28–32 |
| `CallabilityResult` | Callability evaluation result | 39–43 |
| `InternalConflictRecord` | Internal conflict record | 44–48 |
| `GovernanceGateResult` | Final gate decision | 73/78 |
| `ISGValidationResult` | Overall validation for a batch | — |

---

## Public API (`arabic_engine/cognition/isg_v1.py`)

### Step 1: `identify_atom(...)` → `KnowledgeAtom`

Creates and validates a knowledge atom with all required fields.

```python
from arabic_engine.cognition.isg_v1 import identify_atom
from arabic_engine.core.enums import *

atom = identify_atom(
    label="كتاب",
    atom_type=KnowledgeAtomType.LEXICAL,
    knowledge_level="token",
    domain="linguistic",
    source="lexicon",
    source_type=SourceType.PRIMARY,
    confirmation_rank=ConfirmationRank.ESTABLISHED,
    context="sentence",
)
```

### Step 2: `classify_atom(atom)` → `KnowledgeAtom`

Validates classification fields and returns a confirmed frozen copy.

### Step 3: `verify_source(atom, source_record)` → `KnowledgeAtom`

Validates source, confirmation rank, and opinion-freedom. Updates verification status.

### Step 3b: `check_level_match(atom, input_id, input_level, input_domain)` → `LevelMatchResult`

Checks epistemological level compatibility.

### Step 4: `evaluate_callability(atom, input_id, context_fit, conflict_state)` → `CallabilityResult`

Determines whether the atom may be summoned for interpretation.

### Step 5: `resolve_internal_conflict(atom_a, atom_b, method)` → `InternalConflictRecord`

Resolves conflicts between two atoms using the specified method.

### Step 6: `evaluate_gate(atom, input_id, level_match, callability, conflict)` → `GovernanceGateResult`

Makes the final gate decision: PASS, REJECT, SUSPEND, or COMPLETE.

### End-to-end: `govern(atoms, input_id, input_level, input_domain, source_records)` → `ISGValidationResult`

Runs all 6 steps for a batch and returns aggregate results.

### Utility: `separate_opinions(atoms)` → `(information, non_information)`

Separates information atoms from opinions/hypotheses/estimates/positions.

---

## Mathematical Formulation (المادة 74–78)

```
IG = (A, T, L, D, S, Rk, Cx, Rel, Val, Call, Res, Gate)
```

Where:
- **A**: Knowledge atom (`KnowledgeAtom`)
- **T**: Type (`KnowledgeAtomType`)
- **L**: Level (`knowledge_level`)
- **D**: Domain (`domain`)
- **S**: Source (`source` + `SourceType`)
- **Rk**: Confirmation rank (`ConfirmationRank`)
- **Cx**: Context (`context`)
- **Rel**: Relations (`relations`)
- **Val**: Verification (`VerificationStatus`)
- **Call**: Callability (`CallabilityStatus`)
- **Res**: Conflict resolution (`ISGConflictResolution`)
- **Gate**: Gate decision (`GateDecision`)

### Thresholds (`isg_seed_data.py`)

```python
θ₀ = 0.5  # Valid_0 ≥ θ₀ → atom eligible
θ₁ = 0.6  # Callable ≥ θ₁ → atom may be summoned
θ₂ = 0.7  # Entry_Lexeme ≥ θ₂ → atom crosses to lexeme system
```

---

## Pipeline Integration

The ISG stage is inserted in `arabic_engine/pipeline.py` after prior knowledge
construction and before the final result assembly. It wraps each
`PriorKnowledgeUnit` as a `KnowledgeAtom`, runs `govern()`, and records the
result in `PipelineResult.isg_result`.

```python
from arabic_engine.pipeline import run

result = run("كتب الرجل")
print(result.isg_result)  # ISGValidationResult with gate_results
```

---

## Seed Data (`arabic_engine/cognition/isg_seed_data.py`)

- `DEFAULT_GOVERNANCE_THRESHOLDS` — θ₀, θ₁, θ₂
- `DEFAULT_CONFLICT_PRIORITY_ORDER` — resolution priority chain
- `DEFAULT_READINESS_CRITERIA` — 9 elements for first readiness level

---

## Tests (`tests/test_isg_v1.py`)

127 test cases covering:
- Enum completeness (24 tests)
- Atom lifecycle (9 tests)
- Source verification (6 tests)
- Level matching (9 tests)
- Callability (9 tests)
- Conflict resolution (13 tests)
- Gate decisions (12 tests)
- End-to-end govern() (7 tests)
- Opinion separation (5 tests)
- Pipeline integration (2 tests)
- Seed data (6 tests)
- Frozen type verification (7 tests)
