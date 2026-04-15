"""Particle Fractal Constitution v1 — دستور الحرف الفراكتالي v1.0.

Implements the Particle (حرف) as a complete fractal structure — the third
foundational building block alongside Noun (اسم) and Verb (فعل).

The fifteen chapters (أبواب) of the constitution are realised here as
pure functions that classify, validate, and trace particles through the
fractal law (تعيين → حفظ → ربط → حكم → انتقال → رد).

Public API
----------
classify_particle(material) → ParticleRecord
check_minimum(particle) → ParticleMinimum
validate_particle(particle, minimum) → ParticleValidation
trace_fractal_law(particle) → ParticleFractalTrace
compute_readiness(particle) → float
analyze_dalala(particle) → ParticleDalala
build_particle(material) → Tuple[ParticleRecord, ParticleValidation, ParticleFractalTrace]
batch_build(materials) → List[Tuple[ParticleRecord, ParticleValidation, ParticleFractalTrace]]
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from arabic_engine.core.enums import (
    ParticleDalala,
    ParticleDirection,
    ParticleEffect,
    ParticleKind,
    ParticleReadiness,
    ParticleScope,
)
from arabic_engine.core.types import (
    ParticleFractalTrace,
    ParticleMinimum,
    ParticleRecord,
    ParticleValidation,
)

# ── Threshold constants ─────────────────────────────────────────────

_PARTICLE_ACCEPTANCE_THRESHOLD: float = 0.6   # θ_P  (المادة 53)
_READINESS_THRESHOLD: float = 0.6             # θ_RP (المادة 54)

# ── Internal counters for auto-generated IDs ─────────────────────────

_prt_counter = 0
_pmn_counter = 0
_pvl_counter = 0
_pft_counter = 0


def _next_id(prefix: str) -> str:
    """Return the next sequential ID for *prefix*."""
    global _prt_counter, _pmn_counter, _pvl_counter, _pft_counter
    if prefix == "PRT":
        _prt_counter += 1
        return f"PRT_{_prt_counter:03d}"
    if prefix == "PMN":
        _pmn_counter += 1
        return f"PMN_{_pmn_counter:03d}"
    if prefix == "PVL":
        _pvl_counter += 1
        return f"PVL_{_pvl_counter:03d}"
    _pft_counter += 1
    return f"PFT_{_pft_counter:03d}"


# ── Material → ParticleKind mapping ─────────────────────────────────

_MATERIAL_TO_KIND: Dict[str, ParticleKind] = {
    # نسبة — prepositions (حروف الجر)
    "من": ParticleKind.NISBA,
    "في": ParticleKind.NISBA,
    "على": ParticleKind.NISBA,
    "إلى": ParticleKind.NISBA,
    "عن": ParticleKind.NISBA,
    "ب": ParticleKind.NISBA,
    "ل": ParticleKind.NISBA,
    "ك": ParticleKind.NISBA,
    "منذ": ParticleKind.NISBA,
    "مذ": ParticleKind.NISBA,
    # ربط — linking particles
    "أنّ": ParticleKind.RABT,
    "أن": ParticleKind.RABT,
    # تقييد — restrictive particles
    "إنّما": ParticleKind.TAQYID,
    "فقط": ParticleKind.TAQYID,
    # تحويل — transformational particles
    "قد": ParticleKind.TAHWIL,
    "سوف": ParticleKind.TAHWIL,
    "سَ": ParticleKind.TAHWIL,
    # شرط — conditional particles
    "إذا": ParticleKind.SHART,
    "لو": ParticleKind.SHART,
    "إن": ParticleKind.SHART,
    "لولا": ParticleKind.SHART,
    "لمّا": ParticleKind.SHART,
    # نفي — negation particles
    "لا": ParticleKind.NAFY,
    "لم": ParticleKind.NAFY,
    "لن": ParticleKind.NAFY,
    "ما": ParticleKind.NAFY,
    "ليس": ParticleKind.NAFY,
    # عطف — conjunctions
    "و": ParticleKind.ATF,
    "ف": ParticleKind.ATF,
    "ثم": ParticleKind.ATF,
    "أو": ParticleKind.ATF,
    "لكن": ParticleKind.ATF,
    "لكنّ": ParticleKind.ATF,
    "بل": ParticleKind.ATF,
    "أم": ParticleKind.ATF,
    # استفهام — interrogative particles
    "هل": ParticleKind.ISTIFHAM,
    "أ": ParticleKind.ISTIFHAM,
    # توكيد — emphatic particles
    "إنّ": ParticleKind.TAWKID,
    "لام": ParticleKind.TAWKID,
    "كأنّ": ParticleKind.TAWKID,
    "كأن": ParticleKind.TAWKID,
    # غاية — purpose / goal particles
    "حتى": ParticleKind.GHAYA,
    "كي": ParticleKind.GHAYA,
    # استثناء — exception particles
    "إلا": ParticleKind.ISTITHNAA,
    "غير": ParticleKind.ISTITHNAA,
    "سوى": ParticleKind.ISTITHNAA,
    # ابتداء — inception / vocative particles
    "يا": ParticleKind.IBTIDAA,
    "أيّها": ParticleKind.IBTIDAA,
    "ألا": ParticleKind.IBTIDAA,
    "أما": ParticleKind.IBTIDAA,
}

# ── Default mappings per ParticleKind ────────────────────────────────

_KIND_TO_DEFAULT_DIRECTION: Dict[ParticleKind, ParticleDirection] = {
    ParticleKind.NISBA: ParticleDirection.ZARFIYYA,
    ParticleKind.RABT: ParticleDirection.RABT_HUKM,
    ParticleKind.TAQYID: ParticleDirection.MULABASA,
    ParticleKind.TAHWIL: ParticleDirection.RABT_HUKM,
    ParticleKind.SHART: ParticleDirection.SABABIYYA,
    ParticleKind.NAFY: ParticleDirection.RABT_HUKM,
    ParticleKind.ATF: ParticleDirection.RABT_HUKM,
    ParticleKind.ISTIFHAM: ParticleDirection.IBTIDAAIYYA,
    ParticleKind.TAWKID: ParticleDirection.RABT_HUKM,
    ParticleKind.GHAYA: ParticleDirection.INTIHAAIYYA,
    ParticleKind.ISTITHNAA: ParticleDirection.MULABASA,
    ParticleKind.IBTIDAA: ParticleDirection.IBTIDAAIYYA,
}

_KIND_TO_DEFAULT_SCOPE: Dict[ParticleKind, ParticleScope] = {
    ParticleKind.NISBA: ParticleScope.MUFRAD,
    ParticleKind.RABT: ParticleScope.JUMLA,
    ParticleKind.TAQYID: ParticleScope.MUFRAD,
    ParticleKind.TAHWIL: ParticleScope.JIHA,
    ParticleKind.SHART: ParticleScope.QADIYYA,
    ParticleKind.NAFY: ParticleScope.JUMLA,
    ParticleKind.ATF: ParticleScope.MURAKKAB,
    ParticleKind.ISTIFHAM: ParticleScope.JUMLA,
    ParticleKind.TAWKID: ParticleScope.JUMLA,
    ParticleKind.GHAYA: ParticleScope.MUFRAD,
    ParticleKind.ISTITHNAA: ParticleScope.MUFRAD,
    ParticleKind.IBTIDAA: ParticleScope.MUFRAD,
}

_KIND_TO_DEFAULT_EFFECT: Dict[ParticleKind, ParticleEffect] = {
    ParticleKind.NISBA: ParticleEffect.JARR,
    ParticleKind.RABT: ParticleEffect.NASB,
    ParticleKind.TAQYID: ParticleEffect.FATH_MAWDI,
    ParticleKind.TAHWIL: ParticleEffect.TAHWIL_JIHA,
    ParticleKind.SHART: ParticleEffect.JAZM,
    ParticleKind.NAFY: ParticleEffect.TAHWIL_JIHA,
    ParticleKind.ATF: ParticleEffect.RABT_WASL,
    ParticleKind.ISTIFHAM: ParticleEffect.FATH_MAWDI,
    ParticleKind.TAWKID: ParticleEffect.NASB,
    ParticleKind.GHAYA: ParticleEffect.NASB,
    ParticleKind.ISTITHNAA: ParticleEffect.FATH_MAWDI,
    ParticleKind.IBTIDAA: ParticleEffect.FATH_MAWDI,
}

# ── Material-specific direction overrides ────────────────────────────

_MATERIAL_DIRECTION_OVERRIDE: Dict[str, ParticleDirection] = {
    "من": ParticleDirection.IBTIDAAIYYA,
    "إلى": ParticleDirection.INTIHAAIYYA,
    "عن": ParticleDirection.MULABASA,
    "ل": ParticleDirection.SABABIYYA,
    "ب": ParticleDirection.MUSAHABA,
}


# ── Public functions ─────────────────────────────────────────────────


def classify_particle(
    material: str,
    *,
    particle_id: str | None = None,
) -> ParticleRecord:
    """Classify a particle string into a :class:`ParticleRecord`.

    Looks up the *material* in the canonical mapping dictionary to
    determine its kind, direction, scope, and effect.  Unknown materials
    receive default values with ``INCOMPLETE`` readiness.

    Args:
        material:    The Arabic particle string (e.g. ``"من"``, ``"و"``).
        particle_id: Optional explicit ID; auto-generated if omitted.

    Returns:
        A frozen :class:`ParticleRecord`.
    """
    pid = particle_id or _next_id("PRT")
    kind = _MATERIAL_TO_KIND.get(material)

    if kind is None:
        # Unknown particle — assign defaults with INCOMPLETE readiness
        return ParticleRecord(
            particle_id=pid,
            material=material,
            direction=ParticleDirection.RABT_HUKM,
            kind=ParticleKind.RABT,
            scope=ParticleScope.MUFRAD,
            effect=ParticleEffect.FATH_MAWDI,
            readiness=ParticleReadiness.INCOMPLETE,
            readiness_score=0.0,
        )

    direction = _MATERIAL_DIRECTION_OVERRIDE.get(
        material,
        _KIND_TO_DEFAULT_DIRECTION[kind],
    )
    scope = _KIND_TO_DEFAULT_SCOPE[kind]
    effect = _KIND_TO_DEFAULT_EFFECT[kind]

    # Compute readiness score
    score = _compute_readiness_score(
        has_direction=True,
        has_kind=True,
        has_scope=True,
        has_effect=True,
        is_recoverable=True,
    )
    readiness = (
        ParticleReadiness.READY
        if score >= _READINESS_THRESHOLD
        else ParticleReadiness.INCOMPLETE
    )

    return ParticleRecord(
        particle_id=pid,
        material=material,
        direction=direction,
        kind=kind,
        scope=scope,
        effect=effect,
        readiness=readiness,
        readiness_score=score,
    )


def check_minimum(particle: ParticleRecord) -> ParticleMinimum:
    """Evaluate the 8 minimum-completeness conditions (المادة 11-19).

    Args:
        particle: The particle record to check.

    Returns:
        A frozen :class:`ParticleMinimum` with each field set.
    """
    has_material = bool(particle.material and particle.material.strip())
    is_known = particle.material in _MATERIAL_TO_KIND

    return ParticleMinimum(
        # 1. الثبوت — stable lexical form with relational direction
        thuboot=has_material and particle.direction is not None,
        # 2. الحد — distinguishable from ISM / FI3L / other HARF
        hadd=is_known,
        # 3. الامتداد — lexical + semantic + functional + potential-syntactic
        imtidad=has_material and particle.kind is not None,
        # 4. المقوِّم — has material + direction + scope + conditions + effect
        muqawwim=(
            has_material
            and particle.direction is not None
            and particle.scope is not None
            and particle.effect is not None
        ),
        # 5. العلاقة البنائية — the particle *is* its relation
        alaqa_binyawiyya=particle.kind is not None,
        # 6. الانتظام — belongs to a recognised particle door
        intizam=is_known,
        # 7. الوحدة — all constituents form a single particle identity
        wahda=has_material and is_known,
        # 8. قابلية التعيين — can be assigned to a specific door
        qabiliyyat_ta3yin=is_known,
    )


def validate_particle(
    particle: ParticleRecord,
    minimum: ParticleMinimum,
) -> ParticleValidation:
    """Compute acceptance/rejection for a particle (المادة 53-56).

    Args:
        particle: The particle record to validate.
        minimum:  The minimum-completeness result from :func:`check_minimum`.

    Returns:
        A frozen :class:`ParticleValidation`.
    """
    reasons: list[str] = []

    # المادة 55: acceptance criteria
    if not minimum.thuboot:
        reasons.append("فقد الثبوت — missing stable lexical form or direction")
    if not minimum.hadd:
        reasons.append("فقد الحد — indistinguishable from other word classes")
    if not minimum.imtidad:
        reasons.append("فقد الامتداد — no lexical/semantic extension")
    if not minimum.muqawwim:
        reasons.append("فقد المقوِّم — missing constituent (direction/scope/effect)")
    if not minimum.alaqa_binyawiyya:
        reasons.append("فقد العلاقة البنائية — no structural relation")
    if not minimum.intizam:
        reasons.append("فقد الانتظام — not in a recognised particle door")
    if not minimum.wahda:
        reasons.append("فقد الوحدة — identity not unified")
    if not minimum.qabiliyyat_ta3yin:
        reasons.append("فقد قابلية التعيين — cannot be assigned to a door")

    # المادة 56: additional rejection criteria
    if particle.readiness is ParticleReadiness.INVALID:
        reasons.append("الحرف مرفوض — particle explicitly marked invalid")

    # Compute acceptance score: fraction of minimum checks passed
    checks = [
        minimum.thuboot,
        minimum.hadd,
        minimum.imtidad,
        minimum.muqawwim,
        minimum.alaqa_binyawiyya,
        minimum.intizam,
        minimum.wahda,
        minimum.qabiliyyat_ta3yin,
    ]
    score = sum(checks) / len(checks)

    is_valid = score >= _PARTICLE_ACCEPTANCE_THRESHOLD and len(reasons) == 0

    return ParticleValidation(
        particle_id=particle.particle_id,
        is_valid=is_valid,
        minimum=minimum,
        acceptance_score=score,
        rejection_reasons=tuple(reasons),
    )


def trace_fractal_law(particle: ParticleRecord) -> ParticleFractalTrace:
    """Evaluate the 6-step fractal law (المادة 42-48).

    Steps: تعيين → حفظ → ربط → حكم → انتقال → رد

    Args:
        particle: The particle record to trace.

    Returns:
        A frozen :class:`ParticleFractalTrace`.
    """
    is_known = particle.material in _MATERIAL_TO_KIND
    has_material = bool(particle.material and particle.material.strip())

    # تعيين — assigned type/kind/scope/effect (المادة 43)
    ta3yin = is_known and particle.kind is not None

    # حفظ — identity preserved: relational identity + scope + effect (المادة 44)
    hifz = ta3yin and particle.direction is not None and particle.scope is not None

    # ربط — linking function established (المادة 45)
    rabt = hifz and particle.effect is not None

    # حكم — judgeable as particle (المادة 46)
    hukm = rabt and has_material

    # انتقال — ready for syntactic transition (المادة 47)
    intiqal = hukm and particle.readiness is ParticleReadiness.READY

    # رد — reducible to origin type/kind (المادة 48)
    radd = intiqal and is_known

    return ParticleFractalTrace(
        particle_id=particle.particle_id,
        ta3yin=ta3yin,
        hifz=hifz,
        rabt=rabt,
        hukm=hukm,
        intiqal=intiqal,
        radd=radd,
    )


def compute_readiness(particle: ParticleRecord) -> float:
    """Compute the readiness score (المادة 54).

    Formula: Ready_P = (Dir + Kind + Scope + Effect + Recover) / 5

    Each component is 1.0 if present/valid, 0.0 otherwise.

    Args:
        particle: The particle record to evaluate.

    Returns:
        A float in [0.0, 1.0].
    """
    return _compute_readiness_score(
        has_direction=particle.direction is not None,
        has_kind=particle.material in _MATERIAL_TO_KIND,
        has_scope=particle.scope is not None,
        has_effect=particle.effect is not None,
        is_recoverable=particle.material in _MATERIAL_TO_KIND,
    )


def analyze_dalala(particle: ParticleRecord) -> ParticleDalala:
    """Determine the signification type of a particle (المادة 38-40).

    * مطابقة — the particle directly denotes its relational direction
      (e.g. prepositions with clear, singular scope).
    * تضمن — the particle includes its relation type + scope + conditions
      as parts of its meaning.
    * التزام — the particle implies derived effects (case assignment,
      modality change) beyond its primary relational content.

    Args:
        particle: The particle record to analyse.

    Returns:
        A :class:`ParticleDalala` value.
    """
    # Particles whose effect is a direct case-marking (jarr/nasb/jazm)
    # match their denotation exactly → مطابقة
    direct_effects = {
        ParticleEffect.JARR,
        ParticleEffect.NASB,
        ParticleEffect.JAZM,
    }
    if particle.effect in direct_effects:
        return ParticleDalala.MUTABAQA

    # Particles that link or open slots contain their relation implicitly
    if particle.effect is ParticleEffect.RABT_WASL:
        return ParticleDalala.TADAMMUN

    # All others (modality change, slot opening) imply derived effects
    return ParticleDalala.ILTIZAM


def build_particle(
    material: str,
) -> Tuple[ParticleRecord, ParticleValidation, ParticleFractalTrace]:
    """End-to-end particle analysis pipeline.

    classify → check minimum → validate → trace fractal law

    Args:
        material: The Arabic particle string.

    Returns:
        A tuple of (ParticleRecord, ParticleValidation, ParticleFractalTrace).
    """
    record = classify_particle(material)
    minimum = check_minimum(record)
    validation = validate_particle(record, minimum)
    trace = trace_fractal_law(record)
    return record, validation, trace


def batch_build(
    materials: Sequence[str],
) -> List[Tuple[ParticleRecord, ParticleValidation, ParticleFractalTrace]]:
    """Batch particle analysis for multiple materials.

    Args:
        materials: Sequence of Arabic particle strings.

    Returns:
        A list of (ParticleRecord, ParticleValidation, ParticleFractalTrace)
        tuples, one per input material.
    """
    return [build_particle(m) for m in materials]


# ── Internal helpers ─────────────────────────────────────────────────


def _compute_readiness_score(
    *,
    has_direction: bool,
    has_kind: bool,
    has_scope: bool,
    has_effect: bool,
    is_recoverable: bool,
) -> float:
    """Compute Ready_P = (Dir + Kind + Scope + Effect + Recover) / 5."""
    components = [
        float(has_direction),
        float(has_kind),
        float(has_scope),
        float(has_effect),
        float(is_recoverable),
    ]
    return sum(components) / len(components)
