# Single Concept Constitution v1 — دستور المفهوم المفرد

## 1. المجال (Domain)

هذه الوثيقة تعالج **المفهوم المفرد** بوصفه وحدة معرفية-فراكتالية منضبطة، تقابل
اللفظ المفرد من جهة المطابقة، وتحمل فيه التضمن والالتزام، وتبلغ الحد الأدنى
المكتمل قبل الدخول في الإسناد والتقييد والتبعية والعلاقات والأدوار والقضية.

الوثيقة تقع بعد: Lexeme Fractal Constitution v2, Noun/Verb/Particle Constitutions,
Universal/Particular Constitution v1, Reference Constitution v1.

وهي سابقة مباشرة على: Composition / Syntax Constitution v1.

---

## 2. التعريفات (Definitions)

### المفهوم المفرد (Single Concept)

> وحدة معرفية متعينة، تدرك الذات العاقلة بها شيئًا واحدًا من جهة الوجود أو الصفة
> أو الحدث أو النسبة، على نحو مستقل نسبيًا، وقابل للتعريف والتصنيف والحمل والإحالة
> والرد.

### الصياغة الرياضية (Formal Model)

```
C = (Lx, Ty, Dir, UP, EA, Ref, Pred, Role, Ready)
```

| الرمز   | المعنى                    | النوع                        |
|---------|---------------------------|------------------------------|
| `Lx`   | اللفظ المقابل              | `str`                        |
| `Ty`   | النوع الأعلى               | `SingleConceptType`          |
| `Dir`  | الجهة المركزية             | `DalalaType`                 |
| `UP`   | الكلي / الجزئي             | `ConceptUniversalParticular` |
| `EA`   | الذات / الصفة              | `ConceptEntityAttribute`     |
| `Ref`  | الحمل الإحالي              | `float ∈ [0,1]`              |
| `Pred` | الحمل المسندي              | `float ∈ [0,1]`              |
| `Role` | الدور المرشح               | `CandidateRole`              |
| `Ready`| الجاهزية قبل التركيب       | `float ∈ [0,1]`              |

---

## 3. التصنيفات (Classifications)

### التصنيف الأعلى — `SingleConceptType` (المادة 28–32)

| القيمة        | المعنى   | المقابل في `SemanticType` |
|---------------|----------|---------------------------|
| `EXISTENTIAL` | وجودي    | `ENTITY`                  |
| `DESCRIPTIVE` | وصفي     | `ATTRIBUTE`               |
| `EVENTIVE`    | حدثي     | `EVENT`                   |
| `RELATIONAL`  | علائقي   | `RELATION`, `NORM`        |

### الكلي والجزئي — `ConceptUniversalParticular` (المادة 33)

| القيمة       | المعنى |
|--------------|--------|
| `UNIVERSAL`  | كلي    |
| `PARTICULAR` | جزئي   |

### الذات والصفة — `ConceptEntityAttribute` (المادة 34)

| القيمة      | المعنى |
|-------------|--------|
| `ENTITY`    | ذاتي   |
| `ATTRIBUTE` | وصفي   |

### الأدوار المرشحة — `CandidateRole` (المادة 47–53)

| القيمة         | المعنى             |
|----------------|--------------------|
| `MUSNAD_ILAYH` | مرشح للمسند إليه   |
| `MUSNAD`       | مرشح للمسند        |
| `QAYD`         | مرشح للقيد         |
| `TABI`         | مرشح للتابع        |
| `RABIT`        | مرشح للرابط        |
| `MUFASSIR`     | مرشح للمفسر/المميز |

---

## 4. التشاكل (Isomorphism — المادة 11–18)

خمسة محاور تحقق التناسب القانوني بين بنية اللفظ والمفهوم:

| المحور              | الوصف                                          |
|---------------------|-------------------------------------------------|
| `direction_match`   | تطابق الجهة بين النوع الدلالي ونوع المفهوم      |
| `type_match`        | تطابق نوع الكلمة (POS) مع نوع المفهوم المتوقع   |
| `boundary_match`    | وجود حدود واضحة (سطح ≠ فارغ، عنوان ≠ فارغ)     |
| `function_match`    | توافق النوع الدلالي مع وظيفة نحوية معترف بها     |
| `transition_match`  | جاهزية الانتقال (عنوان محدد + POS معلوم)         |

`all_match = True` إذا وفقط إذا تحققت المحاور الخمسة جميعًا.

---

## 5. البوابات الدنيا (Gates — المادة 59–67)

ثمان بوابات قابلة للبرمجة تفحص جاهزية المفهوم المفرد:

| البوابة                      | المادة | الفحص                                         |
|------------------------------|--------|------------------------------------------------|
| `GATE_TYPE`                  | 60     | هل تحدد النوع الأعلى؟                          |
| `GATE_DIRECTION`             | 61     | هل الجهة متطابقة مع اللفظ؟                     |
| `GATE_UNIVERSAL_PARTICULAR`  | 62     | هل تحدد الكلي/الجزئي؟                          |
| `GATE_ENTITY_ATTRIBUTE`      | 63     | هل فُصل الذاتي عن الوصفي؟                      |
| `GATE_REFERENCE_LOAD`        | 64     | هل الحمل الإحالي معتبر؟                        |
| `GATE_PREDICATIVE_LOAD`      | 65     | هل الحمل المسندي يؤهل للإسناد؟                 |
| `GATE_ROLE_READINESS`        | 66     | هل بلغ الدور المرشح عتبته؟                      |
| `GATE_RECOVERABILITY`        | 67     | هل يمكن رد المفهوم إلى لفظه وجهته ورتبته؟       |

### معيار الجاهزية (المادة 80)

```
Ready_C = count(PASSED gates) / total_gates
```

المفهوم المفرد جاهز إذا: `Ready_C ≥ θ_RC` (افتراضيًا `θ_RC = 0.7`)

---

## 6. المطابقة والتضمن والالتزام (المادة 54–57)

| المستوى    | التعريف                                           |
|------------|---------------------------------------------------|
| المطابقة   | تطابق المفهوم مع جهة اللفظ في أصل الاعتبار         |
| التضمن     | ما يدخل في بنية المفهوم من حدوده وعناصره ورتبته     |
| الالتزام   | ما يلزم عن المفهوم خارج حده المباشر من وظائف وآثار  |

---

## 7. التحقق البرمجي (Verification)

### ربط المواد بالشفرة

| المواد        | الملف                                        | الدالة / الصنف                    |
|---------------|----------------------------------------------|-----------------------------------|
| المادة 28–32  | `arabic_engine/core/enums.py`                | `SingleConceptType`               |
| المادة 33     | `arabic_engine/core/enums.py`                | `ConceptUniversalParticular`      |
| المادة 34     | `arabic_engine/core/enums.py`                | `ConceptEntityAttribute`          |
| المادة 36     | `arabic_engine/core/enums.py`                | `ConceptIndependence`             |
| المادة 37     | `arabic_engine/core/enums.py`                | `ConceptClosureStatus`            |
| المادة 47–53  | `arabic_engine/core/enums.py`                | `CandidateRole`                   |
| المادة 59–67  | `arabic_engine/core/enums.py`                | `ConceptGateID`                   |
| المادة 78     | `arabic_engine/core/types.py`                | `SingleConceptRecord`             |
| المادة 12–17  | `arabic_engine/core/types.py`                | `SingleConceptIsomorphism`        |
| المادة 54–57  | `arabic_engine/core/types.py`                | `SingleConceptDalala`             |
| المادة 58–67  | `arabic_engine/core/types.py`                | `SingleConceptGateResult`         |
| المادة 28–82  | `arabic_engine/signified/single_concept_v1.py` | `build_single_concept()`       |
| المادة 81–82  | `arabic_engine/signified/single_concept_v1.py` | `acceptance_summary()`         |

### مثال استخدام

```python
from arabic_engine.core.enums import POS, SemanticType, DalalaType
from arabic_engine.core.types import LexicalClosure, Concept
from arabic_engine.signified.single_concept_v1 import (
    build_single_concept,
    acceptance_summary,
)

closure = LexicalClosure(
    surface="الكِتَاب", lemma="كتاب",
    root=("ك", "ت", "ب"), pattern="فَعَلَ", pos=POS.ISM,
)
concept = Concept(
    concept_id=1, label="كتاب",
    semantic_type=SemanticType.ENTITY,
)

record = build_single_concept(closure, concept, DalalaType.MUTABAQA)
print(record.valid)             # True
print(record.readiness_score)   # 1.0
print(record.concept_type)      # SingleConceptType.EXISTENTIAL
print(record.candidate_role)    # CandidateRole.MUSNAD_ILAYH

summary = acceptance_summary(record)
print(summary)
# {'lexeme_match': True, 'type_established': True, ...}
```
