# Verb Fractal Constitution v1 — دستور الفعل الفراكتالي

## Overview

The Verb Fractal Constitution defines the **verb** (الفعل) as a complete
fractal structure within the Arabic Engine.  It covers 71 articles across
18 chapters (أبواب) and complements the Noun Fractal Constitution.

## Code Locations

| Component | File |
|-----------|------|
| Enums (13) | `arabic_engine/core/enums.py` |
| Frozen dataclasses (6) | `arabic_engine/core/types.py` |
| Re-exports | `arabic_engine/core/__init__.py` |
| Module (8 public functions) | `arabic_engine/signified/verb_constitution.py` |
| Tests (~55 tests) | `tests/test_verb_constitution.py` |

## Enums

| Enum | Members | Article |
|------|---------|---------|
| `VerbTense` | MADI, MUDARI, AMR | 25–28 |
| `VerbVoice` | ACTIVE, PASSIVE | — |
| `VerbPerson` | FIRST, SECOND, THIRD | 29–31 |
| `VerbNumber` | SINGULAR, DUAL, PLURAL | — |
| `VerbGender` | MASCULINE, FEMININE | — |
| `VerbTransitivity` | LAZIM, MUTA3ADDI, MUTA3ADDI_LI_ITHNAYN, MUTA3ADDI_LI_THALATHA | 22 |
| `VerbBab` | FA3ALA_YAF3ULU, FA3ALA_YAF3ILU, FA3ALA_YAF3ALU, FA3ILA_YAF3ALU, FA3ULA_YAF3ULU, FA3ILA_YAF3ILU, OTHER | 32–35 |
| `VerbMode` | MUJARRAD, MAZID, NASIKH | 36–50 |
| `VerbAugmentation` | IF3AL, FA33ALA, FA3ALA_III, INFA3ALA, IFTA3ALA, TAFA33ALA, TAFA3ALA, IF3ALLA, ISTAF3ALA, NONE | 36–39 |
| `NasikhType` | KANA, KADA, ZANNA | 46–50 |
| `VerbEventType` | SIMPLE_OCCURRENCE, BECOMING, TRANSFORMATION, CAUSATION, BEING_AFFECTED, LINKING | 20–24 |
| `VerbDerivativeType` | ISM_FA3IL, ISM_MAF3UL, ISM_ZAMAN, ISM_MAKAN, ISM_HAY2A, ISM_ALA, MUBALAQA, MASDAR | 43 |
| `VerbReadiness` | READY, NOT_READY, PARTIAL | 62–64 |

## Types

| Type | Fields | Article |
|------|--------|---------|
| `VerbInflection` | surface, root, bab, tense, person, number, gender, voice, transitivity, mode, augmentation, nasikh_type | 11–19 |
| `VerbEventRecord` | event_type, has_causality, has_musha_raka, has_mutawa3a | 20–24 |
| `VerbDerivativeRecord` | derivative_type, form, notes | 43–45 |
| `VerbMasdarRecord` | masdar_form, is_qiyasi, notes | 40–42 |
| `VerbReadinessScore` | direction_score, time_score, person_score, valence_score, mode_score, recover_score, total, status | 62–67 |
| `VerbConstitutionRecord` | record_id, inflection, event, masdar, derivatives, readiness, fractal_cycle, valid, notes | 65–67 |

## Public API

```python
from arabic_engine.signified.verb_constitution import (
    classify_verb_inflection,   # Art. 11–19, 32–50
    classify_verb_event,        # Art. 20–24
    build_masdar,               # Art. 40–42
    build_derivatives,          # Art. 43–45
    compute_readiness,          # Art. 62–67
    validate_verb,              # Art. 68–69
    build_verb_constitution,    # Art. 65–67 (orchestrator)
    batch_build,                # Batch processing
)
```

## Mathematical Formalization (Art. 65–67)

The verb is represented as a 10-tuple:

```
V = (M, W, D, Tm, Prs, Val, Mode, Src, Der, Ready)
```

Readiness score:

```
Ready_V = (Dir + Time + Person + Val + Mode + Recover) / 6
```

A verb is accepted when `Ready_V ≥ θ_RV` (default threshold = 0.8).

## Fractal Cycle (Art. 55–61)

```
تعيين → حفظ → ربط → حكم → انتقال → رد
```

The `build_verb_constitution` function enforces this order:
1. **تعيين** — classify inflection
2. **حفظ** — classify event
3. **ربط** — build masdar
4. **حكم** — build derivatives
5. **انتقال** — compute readiness
6. **رد** — validate and produce final record
