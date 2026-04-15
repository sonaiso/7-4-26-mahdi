"""Verb Fractal Constitution v1 — دستور الفعل الفراكتالي v1.0.

Implements the 18-chapter verb fractal constitution covering:

    1. موضوع الوثيقة (Art. 1–3)
    2. تعريف الفعل (Art. 4–7)
    3. شرط الإمكان المعرفي (Art. 8–10)
    4. الحد الأدنى المكتمل (Art. 11–19)
    5. الحدث في الفعل (Art. 20–24)
    6. الزمن في الفعل (Art. 25–28)
    7. الشخص والإسناد (Art. 29–31)
    8. الأبواب الثلاثية المجردة (Art. 32–35)
    9. المزيد (Art. 36–39)
   10. المصدر (Art. 40–42)
   11. المشتقات الفعلية (Art. 43–45)
   12. الأفعال الناسخة (Art. 46–50)
   13. المطابقة والتضمن والالتزام (Art. 51–54)
   14. الفعل والقانون الفراكتالي (Art. 55–61)
   15. الجاهزية الفعلية للتركيب (Art. 62–64)
   16. الصياغة الرياضية (Art. 65–67)
   17. معايير القبول والرفض (Art. 68–69)
   18. الصيغة المختصرة المعتمدة (Art. 70–71)

Public API
----------
classify_verb_inflection(…) → VerbInflection
classify_verb_event(…)      → VerbEventRecord
build_masdar(…)             → VerbMasdarRecord
build_derivatives(…)        → Tuple[VerbDerivativeRecord, …]
compute_readiness(…)        → VerbReadinessScore
validate_verb(inflection)   → bool
build_verb_constitution(…)  → VerbConstitutionRecord
batch_build(verb_specs)     → List[VerbConstitutionRecord]
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from arabic_engine.core.enums import (
    NasikhType,
    VerbAugmentation,
    VerbBab,
    VerbDerivativeType,
    VerbEventType,
    VerbGender,
    VerbMode,
    VerbNumber,
    VerbPerson,
    VerbReadiness,
    VerbTense,
    VerbTransitivity,
    VerbVoice,
)
from arabic_engine.core.types import (
    VerbConstitutionRecord,
    VerbDerivativeRecord,
    VerbEventRecord,
    VerbInflection,
    VerbMasdarRecord,
    VerbReadinessScore,
)

# ── Internal counters for auto-generated IDs ─────────────────────────

_vif_counter = 0
_vev_counter = 0
_vmd_counter = 0
_vdr_counter = 0
_vrc_counter = 0


def _next_id(prefix: str) -> str:
    """Return the next sequential ID for *prefix*.

    Supported prefixes:
      VIF → verb inflection, VEV → verb event, VMD → verb masdar,
      VDR → verb derivative, VRC → verb constitution record.
    """
    global _vif_counter, _vev_counter, _vmd_counter, _vdr_counter, _vrc_counter
    if prefix == "VIF":
        _vif_counter += 1
        return f"VIF_{_vif_counter:03d}"
    if prefix == "VEV":
        _vev_counter += 1
        return f"VEV_{_vev_counter:03d}"
    if prefix == "VMD":
        _vmd_counter += 1
        return f"VMD_{_vmd_counter:03d}"
    if prefix == "VDR":
        _vdr_counter += 1
        return f"VDR_{_vdr_counter:03d}"
    _vrc_counter += 1
    return f"VRC_{_vrc_counter:03d}"


# ── Internal mapping dicts ───────────────────────────────────────────

_BAB_TO_SEMANTIC_TENDENCY: Dict[VerbBab, VerbEventType] = {
    VerbBab.FA3ALA_YAF3ULU: VerbEventType.SIMPLE_OCCURRENCE,
    VerbBab.FA3ALA_YAF3ILU: VerbEventType.SIMPLE_OCCURRENCE,
    VerbBab.FA3ALA_YAF3ALU: VerbEventType.SIMPLE_OCCURRENCE,
    VerbBab.FA3ILA_YAF3ALU: VerbEventType.BECOMING,
    VerbBab.FA3ULA_YAF3ULU: VerbEventType.BECOMING,
    VerbBab.FA3ILA_YAF3ILU: VerbEventType.SIMPLE_OCCURRENCE,
    VerbBab.OTHER: VerbEventType.SIMPLE_OCCURRENCE,
}

_AUGMENTATION_TO_EVENT: Dict[VerbAugmentation, VerbEventType] = {
    VerbAugmentation.IF3AL: VerbEventType.CAUSATION,
    VerbAugmentation.FA33ALA: VerbEventType.CAUSATION,
    VerbAugmentation.FA3ALA_III: VerbEventType.SIMPLE_OCCURRENCE,
    VerbAugmentation.INFA3ALA: VerbEventType.BEING_AFFECTED,
    VerbAugmentation.IFTA3ALA: VerbEventType.SIMPLE_OCCURRENCE,
    VerbAugmentation.TAFA33ALA: VerbEventType.TRANSFORMATION,
    VerbAugmentation.TAFA3ALA: VerbEventType.SIMPLE_OCCURRENCE,
    VerbAugmentation.IF3ALLA: VerbEventType.BECOMING,
    VerbAugmentation.ISTAF3ALA: VerbEventType.SIMPLE_OCCURRENCE,
    VerbAugmentation.NONE: VerbEventType.SIMPLE_OCCURRENCE,
}

# ── Fractal cycle constant (Art. 55–61) ──────────────────────────────

_FRACTAL_CYCLE = "تعيين → حفظ → ربط → حكم → انتقال → رد"

# ── Default readiness threshold (Art. 67) ────────────────────────────

_READINESS_THRESHOLD = 0.8


# ── Public functions ──────────────────────────────────────────────────


def classify_verb_inflection(
    surface: str,
    root: Tuple[str, ...],
    bab: VerbBab,
    tense: VerbTense,
    person: VerbPerson,
    number: VerbNumber,
    gender: VerbGender,
    voice: VerbVoice,
    transitivity: VerbTransitivity,
    mode: VerbMode,
    augmentation: VerbAugmentation,
    nasikh_type: Optional[NasikhType] = None,
) -> VerbInflection:
    """Classify a verb's full inflectional state (Art. 11–19, 32–50).

    Args:
        surface:       The surface form of the verb (e.g. "كَتَبَ").
        root:          Root letters as a tuple (e.g. ("ك", "ت", "ب")).
        bab:           Triliteral paradigm (الباب).
        tense:         Tense (الزمن).
        person:        Person (الشخص).
        number:        Number (العدد).
        gender:        Gender (الجنس).
        voice:         Voice (المبني).
        transitivity:  Transitivity (اللزوم/التعدي).
        mode:          Mode (مجرد/مزيد/ناسخ).
        augmentation:  Augmentation pattern (باب المزيد).
        nasikh_type:   Copular verb type, if applicable.

    Returns:
        A frozen :class:`VerbInflection`.
    """
    return VerbInflection(
        surface=surface,
        root=root,
        bab=bab,
        tense=tense,
        person=person,
        number=number,
        gender=gender,
        voice=voice,
        transitivity=transitivity,
        mode=mode,
        augmentation=augmentation,
        nasikh_type=nasikh_type,
    )


def classify_verb_event(
    event_type: VerbEventType,
    *,
    has_causality: bool = False,
    has_musha_raka: bool = False,
    has_mutawa3a: bool = False,
) -> VerbEventRecord:
    """Classify the event axis of a verb (Art. 20–24).

    Args:
        event_type:      The primary event type.
        has_causality:   Whether the verb carries causality (سببية).
        has_musha_raka:  Whether the verb carries participation (مشاركة).
        has_mutawa3a:    Whether the verb carries compliance (مطاوعة).

    Returns:
        A frozen :class:`VerbEventRecord`.
    """
    return VerbEventRecord(
        event_type=event_type,
        has_causality=has_causality,
        has_musha_raka=has_musha_raka,
        has_mutawa3a=has_mutawa3a,
    )


def build_masdar(
    masdar_form: str,
    *,
    is_qiyasi: bool = True,
    notes: str = "",
) -> VerbMasdarRecord:
    """Build a masdar record (Art. 40–42).

    Args:
        masdar_form:  The masdar surface form (e.g. "كِتَابَة").
        is_qiyasi:    Whether the masdar follows a regular pattern (قياسي).
        notes:        Optional notes.

    Returns:
        A frozen :class:`VerbMasdarRecord`.
    """
    return VerbMasdarRecord(
        masdar_form=masdar_form,
        is_qiyasi=is_qiyasi,
        notes=notes,
    )


def build_derivatives(
    derivatives_data: Sequence[Tuple[VerbDerivativeType, str]],
) -> Tuple[VerbDerivativeRecord, ...]:
    """Build derivative records from (type, form) pairs (Art. 43–45).

    Args:
        derivatives_data: A sequence of ``(derivative_type, form)`` pairs.

    Returns:
        A tuple of frozen :class:`VerbDerivativeRecord` objects.
    """
    return tuple(
        VerbDerivativeRecord(derivative_type=dt, form=form)
        for dt, form in derivatives_data
    )


def compute_readiness(
    inflection: VerbInflection,
    event: VerbEventRecord,
    masdar: Optional[VerbMasdarRecord],
    derivatives: Tuple[VerbDerivativeRecord, ...],
    *,
    threshold: float = _READINESS_THRESHOLD,
) -> VerbReadinessScore:
    """Compute the 6-axis readiness score for a verb (Art. 62–67).

    The six axes are:
      1. direction_score  — 1.0 if event_type is set (always true).
      2. time_score       — 1.0 if tense is set (always true).
      3. person_score     — 1.0 if person is set (always true).
      4. valence_score    — 1.0 if transitivity is set (always true).
      5. mode_score       — 1.0 if mode is set (always true).
      6. recover_score    — 1.0 if root is non-empty.

    A verb is ``READY`` when ``total >= threshold``, ``PARTIAL`` when
    ``total > 0`` but below threshold, and ``NOT_READY`` when ``total == 0``.

    Args:
        inflection:   The verb inflection record.
        event:        The verb event record.
        masdar:       Optional masdar record (not used in scoring).
        derivatives:  Derivative records (not used in scoring).
        threshold:    Readiness threshold θ_RV (default 0.8).

    Returns:
        A frozen :class:`VerbReadinessScore`.
    """
    direction_score = 1.0  # event_type is always set via enum
    time_score = 1.0       # tense is always set via enum
    person_score = 1.0     # person is always set via enum
    valence_score = 1.0    # transitivity is always set via enum
    mode_score = 1.0       # mode is always set via enum
    recover_score = 1.0 if len(inflection.root) > 0 else 0.0

    total = (
        direction_score + time_score + person_score
        + valence_score + mode_score + recover_score
    ) / 6.0

    if total >= threshold:
        status = VerbReadiness.READY
    elif total > 0:
        status = VerbReadiness.PARTIAL
    else:
        status = VerbReadiness.NOT_READY

    return VerbReadinessScore(
        direction_score=direction_score,
        time_score=time_score,
        person_score=person_score,
        valence_score=valence_score,
        mode_score=mode_score,
        recover_score=recover_score,
        total=total,
        status=status,
    )


def validate_verb(inflection: VerbInflection) -> bool:
    """Apply acceptance/rejection criteria to a verb (Art. 68–69).

    A verb is valid if:
      1. Its surface is non-empty.
      2. Its root is non-empty.
      3. If mode is NASIKH, nasikh_type must be set.
      4. If mode is MAZID, augmentation must not be NONE.
      5. If mode is MUJARRAD, augmentation must be NONE.

    Returns:
        ``True`` if the verb passes all acceptance criteria.
    """
    # Art. 68.1 — surface must exist
    if not inflection.surface.strip():
        return False

    # Art. 68.2 — root must exist
    if len(inflection.root) == 0:
        return False

    # Art. 68.6 — mode consistency checks
    if inflection.mode is VerbMode.NASIKH and inflection.nasikh_type is None:
        return False

    if inflection.mode is VerbMode.MAZID and inflection.augmentation is VerbAugmentation.NONE:
        return False

    if (
        inflection.mode is VerbMode.MUJARRAD
        and inflection.augmentation is not VerbAugmentation.NONE
    ):
        return False

    return True


def build_verb_constitution(
    surface: str,
    root: Tuple[str, ...],
    bab: VerbBab,
    tense: VerbTense,
    person: VerbPerson,
    number: VerbNumber,
    gender: VerbGender,
    voice: VerbVoice,
    transitivity: VerbTransitivity,
    mode: VerbMode,
    augmentation: VerbAugmentation,
    event_type: VerbEventType,
    *,
    nasikh_type: Optional[NasikhType] = None,
    masdar_form: Optional[str] = None,
    derivatives_data: Optional[Sequence[Tuple[VerbDerivativeType, str]]] = None,
    has_causality: bool = False,
    has_musha_raka: bool = False,
    has_mutawa3a: bool = False,
    record_id: Optional[str] = None,
    notes: str = "",
) -> VerbConstitutionRecord:
    """Build a complete verb constitution record (Art. 65–67).

    This is the top-level orchestrator that enforces the correct analysis
    order mandated by the fractal cycle (Art. 55–61)::

        تعيين → حفظ → ربط → حكم → انتقال → رد

    Args:
        surface:          Surface form of the verb.
        root:             Root letters.
        bab:              Triliteral paradigm.
        tense:            Tense.
        person:           Person.
        number:           Number.
        gender:           Gender.
        voice:            Voice.
        transitivity:     Transitivity.
        mode:             Mode (مجرد/مزيد/ناسخ).
        augmentation:     Augmentation pattern.
        event_type:       Primary event type.
        nasikh_type:      Copular verb type (if applicable).
        masdar_form:      Masdar surface form (if known).
        derivatives_data: Sequence of (type, form) pairs for derivatives.
        has_causality:    Whether the verb carries causality.
        has_musha_raka:   Whether the verb carries participation.
        has_mutawa3a:     Whether the verb carries compliance.
        record_id:        Optional explicit record ID.
        notes:            Free-text annotation.

    Returns:
        A frozen :class:`VerbConstitutionRecord`.
    """
    # Step 1: تعيين — classify inflection
    inflection = classify_verb_inflection(
        surface=surface,
        root=root,
        bab=bab,
        tense=tense,
        person=person,
        number=number,
        gender=gender,
        voice=voice,
        transitivity=transitivity,
        mode=mode,
        augmentation=augmentation,
        nasikh_type=nasikh_type,
    )

    # Step 2: حفظ — classify event
    event = classify_verb_event(
        event_type,
        has_causality=has_causality,
        has_musha_raka=has_musha_raka,
        has_mutawa3a=has_mutawa3a,
    )

    # Step 3: ربط — masdar
    masdar = build_masdar(masdar_form) if masdar_form else None

    # Step 4: حكم — derivatives
    derivatives = build_derivatives(derivatives_data) if derivatives_data else ()

    # Step 5: انتقال — compute readiness
    readiness = compute_readiness(inflection, event, masdar, derivatives)

    # Step 6: رد — validate
    valid = validate_verb(inflection) and readiness.status is VerbReadiness.READY

    rid = record_id or _next_id("VRC")

    return VerbConstitutionRecord(
        record_id=rid,
        inflection=inflection,
        event=event,
        masdar=masdar,
        derivatives=derivatives,
        readiness=readiness,
        fractal_cycle=_FRACTAL_CYCLE,
        valid=valid,
        notes=notes,
    )


def batch_build(
    verb_specs: List[Dict[str, Any]],
) -> List[VerbConstitutionRecord]:
    """Build multiple verb constitution records at once.

    Each dictionary in *verb_specs* is unpacked as keyword arguments to
    :func:`build_verb_constitution`.

    Args:
        verb_specs: A list of keyword-argument dictionaries.

    Returns:
        A list of :class:`VerbConstitutionRecord` objects.
    """
    return [build_verb_constitution(**spec) for spec in verb_specs]
