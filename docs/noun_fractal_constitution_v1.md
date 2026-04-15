# Noun Fractal Constitution v1 — دستور الاسم الفراكتالي

## Overview

This document describes the implementation of the Noun Fractal
Constitution v1, which formalises the Arabic noun (الاسم) as a
self-contained fractal structure for:

- **Designation** (تعيين)
- **Classification** (تصنيف)
- **Reference** (إحالة)
- **Compositional readiness** (جاهزية تركيبية)

## Mathematical Formula (Art. 73)

```
N = (M, WT, D, T, Ref, Num, Gen, Def, Ready)
```

| Symbol | Field | Arabic |
|--------|-------|--------|
| M | material / lemma | المادة |
| WT | pattern type | الوزن الجامد / القالب |
| D | direction | الجهة الاسمية |
| T | conceptual type | النوع المفهومي |
| Ref | classification (universality + genus) | الكلي والجزئي |
| Num | number | الوحدة والكثرة |
| Gen | gender | التذكير والتأنيث |
| Def | definiteness | المعرفة والنكرة |
| Ready | readiness score | الجاهزية |

## Readiness Formula (Art. 75)

```
Ready_N = (Dir + Type + Ref + Num + Gen + Def + Recover) / 7
```

A noun is considered *ready* for composition when `Ready_N ≥ 0.7`.

## Enumerations

| Enum | Arabic | Article | Members |
|------|--------|---------|---------|
| `NounDirection` | الجهة الاسمية | 4, 12, 14 | 10 |
| `NounUniversality` | الكلي والجزئي | 24-28 | 3 |
| `NounGenusLevel` | الجنس والنوع والفرد | 29-33 | 4 |
| `ProperNounKind` | أنواع العلم | 34-37 | 9 |
| `NominalAttributeKind` | نوع الصفة الاسمية | 38-40 | 9 |
| `NounNumber` | الوحدة والكثرة | 41-44 | 6 |
| `NounGender` | التذكير والتأنيث | 45-47 | 6 |
| `NounDefiniteness` | المعرفة والنكرة | 48-50 | 8 |
| `NounComposition` | المركب الاسمي والمزجي | 51-53 | 4 |
| `NounOrigin` | المقترض | 54-55 | 4 |
| `NounPatternType` | الوزن الجامد | 56-58 | 4 |
| `NounSignificationType` | المطابقة والتضمن والالتزام | 59-62 | 3 |
| `NounFractalStage` | القانون الفراكتالي | 63-69 | 6 |
| `NounReadiness` | الجاهزية الاسمية | 70-72 | 3 |
| `NounExistentialAspect` | جهة الموجود | 21-23 | 7 |

## Data Types

| Type | Arabic | Article |
|------|--------|---------|
| `NounMinimumRecord` | الحد الأدنى المكتمل | 11-19 |
| `NounMorphologyRecord` | المادة والوزن | 15, 56-58 |
| `NounClassificationRecord` | التصنيف | 24-33 |
| `NounAttributeRecord` | الصفة الاسمية | 38-40 |
| `NounInflectionRecord` | الصرف | 41-50 |
| `NounCompositionRecord` | المركب والمقترض | 51-55 |
| `NounSignificationRecord` | المطابقة والتضمن والالتزام | 59-62 |
| `NounFractalRecord` | البنية الفراكتالية المكتملة | 73-75 |
| `NounValidationResult` | القبول والرفض | 76-77 |

## Public API

```python
from arabic_engine.noun import (
    build_noun_fractal,      # Master factory (Art. 73-74)
    validate_noun_fractal,   # Acceptance/rejection (Art. 76-77)
    batch_build,             # Batch factory
    classify_noun_direction,  # Art. 4, 64
    classify_universality,    # Art. 24-28
    classify_genus_level,     # Art. 29-33
    classify_proper_noun,     # Art. 34-37
    classify_nominal_attribute, # Art. 38-40
    determine_inflection,     # Art. 41-50
    determine_composition,    # Art. 51-55
    determine_morphology,     # Art. 56-58
    compute_signification,    # Art. 59-62
    check_minimum,            # Art. 11-19
    compute_readiness,        # Art. 75
)
```

## Fractal Law Cycle (Art. 63)

```
تعيين → حفظ → ربط → حكم → انتقال → رد
```

The cycle is encoded as `NounFractalStage` but execution is deferred to
the Composition / Syntax Constitution v1.

## Next Steps

This constitution is directly followed by:

- Verb Fractal Constitution v1
- Particle Fractal Constitution v1
- Composition / Syntax Constitution v1
