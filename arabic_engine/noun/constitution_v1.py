"""Noun Fractal Constitution v1 — دستور الاسم الفراكتالي v1.0.

Implements the noun (الاسم) as a self-contained fractal structure for
designation (تعيين), classification (تصنيف), reference (إحالة), and
compositional readiness (جاهزية تركيبية).

Mathematical formula (Art. 73):
    N = (M, WT, D, T, Ref, Num, Gen, Def, Ready)

Readiness formula (Art. 75):
    Ready_N = (Dir + Type + Ref + Num + Gen + Def + Recover) / 7

Public API
----------
classify_noun_direction(closure, concept) → NounDirection
classify_universality(concept) → NounUniversality
classify_genus_level(concept, direction) → NounGenusLevel
classify_proper_noun(closure) → Optional[ProperNounKind]
classify_nominal_attribute(closure) → NounAttributeRecord
determine_inflection(closure) → NounInflectionRecord
determine_composition(closure) → NounCompositionRecord
determine_morphology(closure) → NounMorphologyRecord
compute_signification(concept, direction) → NounSignificationRecord
check_minimum(morph, classif, attr, infl, comp, signif) → NounMinimumRecord
compute_readiness(direction, type_, classif, number, gender, def_, recoverable) → float
build_noun_fractal(closure, concept, *, noun_id=None) → NounFractalRecord
validate_noun_fractal(fractal) → NounValidationResult
batch_build(closures, concepts) → List[NounFractalRecord]
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from arabic_engine.core.enums import (
    POS,
    NominalAttributeKind,
    NounComposition,
    NounDefiniteness,
    NounDirection,
    NounExistentialAspect,
    NounFractalStage,
    NounGender,
    NounGenusLevel,
    NounNumber,
    NounOrigin,
    NounPatternType,
    NounReadiness,
    NounUniversality,
    ProperNounKind,
    SemanticType,
)
from arabic_engine.core.types import (
    Concept,
    LexicalClosure,
    NounAttributeRecord,
    NounClassificationRecord,
    NounCompositionRecord,
    NounFractalRecord,
    NounInflectionRecord,
    NounMinimumRecord,
    NounMorphologyRecord,
    NounSignificationRecord,
    NounValidationResult,
)

# ── Internal counter for auto-generated IDs ──────────────────────────

_nf_counter = 0

# Readiness threshold (Art. 74-75).  A noun with Ready_N >= θ_RN is
# considered *ready* for composition.
_READINESS_THRESHOLD = 0.7


def _next_id() -> str:
    """Return the next sequential noun-fractal ID (``NF_001``, …)."""
    global _nf_counter
    _nf_counter += 1
    return f"NF_{_nf_counter:03d}"


def _score_component(value: object, *unknowns: object) -> float:
    """Return 1.0 if *value* is set (not in *unknowns*), else 0.0."""
    return 0.0 if value in unknowns else 1.0


# ── Classification helpers ───────────────────────────────────────────

# SemanticType → NounDirection mapping
_STYPE_TO_DIRECTION = {
    SemanticType.ENTITY: NounDirection.DHAT,
    SemanticType.ATTRIBUTE: NounDirection.SIFA_ISMIYYA,
    SemanticType.RELATION: NounDirection.MAFHUM_ISMI,
    SemanticType.NORM: NounDirection.MAFHUM_ISMI,
    SemanticType.EVENT: NounDirection.MARJI3,
}

# SemanticType → NounExistentialAspect mapping
_STYPE_TO_EXISTENTIAL = {
    SemanticType.ENTITY: NounExistentialAspect.DHAT,
    SemanticType.ATTRIBUTE: NounExistentialAspect.SHAY2,
    SemanticType.RELATION: NounExistentialAspect.MARJI3,
    SemanticType.NORM: NounExistentialAspect.MARJI3,
    SemanticType.EVENT: NounExistentialAspect.SHAY2,
}

# POS tag → NominalAttributeKind (only for adjective-like POS tags)
_POS_TO_ATTR_KIND = {
    POS.SIFA: NominalAttributeKind.SIFA_MUSHABBAHA,
}

# Feature keys that the LexicalClosure.features dict may carry.
_FEAT_NUMBER = "number"
_FEAT_GENDER = "gender"
_FEAT_DEFINITENESS = "definiteness"
_FEAT_PROPER = "proper"
_FEAT_COMPOUND = "compound"
_FEAT_BORROWED = "borrowed"
_FEAT_DERIVED = "derived"
_FEAT_ATTR_KIND = "attr_kind"

# ── Number feature → NounNumber mapping
_NUMBER_MAP = {
    "singular": NounNumber.MUFRAD,
    "mufrad": NounNumber.MUFRAD,
    "dual": NounNumber.MUTHANNA,
    "muthanna": NounNumber.MUTHANNA,
    "plural": NounNumber.JAM3,
    "jam3": NounNumber.JAM3,
    "collective": NounNumber.ISM_JAM3,
    "ism_jam3": NounNumber.ISM_JAM3,
    "collective_genus": NounNumber.ISM_JINS_JAM3I,
    "ism_jins_jam3i": NounNumber.ISM_JINS_JAM3I,
}

# ── Gender feature → NounGender mapping
_GENDER_MAP = {
    "masculine": NounGender.MUDHAKKAR,
    "mudhakkar": NounGender.MUDHAKKAR,
    "feminine": NounGender.MU2ANNATH_HAQIQI,
    "mu2annath_haqiqi": NounGender.MU2ANNATH_HAQIQI,
    "feminine_figurative": NounGender.MU2ANNATH_MAJAZI,
    "mu2annath_majazi": NounGender.MU2ANNATH_MAJAZI,
    "feminine_lexical": NounGender.MU2ANNATH_LAFZI,
    "mu2annath_lafzi": NounGender.MU2ANNATH_LAFZI,
    "feminine_semantic": NounGender.MU2ANNATH_MA3NAWI,
    "mu2annath_ma3nawi": NounGender.MU2ANNATH_MA3NAWI,
}

# ── Definiteness feature → NounDefiniteness mapping
_DEF_MAP = {
    "proper": NounDefiniteness.MA3RIFA_3ALAM,
    "ma3rifa_3alam": NounDefiniteness.MA3RIFA_3ALAM,
    "pronoun": NounDefiniteness.MA3RIFA_DAMIR,
    "ma3rifa_damir": NounDefiniteness.MA3RIFA_DAMIR,
    "demonstrative": NounDefiniteness.MA3RIFA_ISHARA,
    "ma3rifa_ishara": NounDefiniteness.MA3RIFA_ISHARA,
    "relative": NounDefiniteness.MA3RIFA_MAWSUL,
    "ma3rifa_mawsul": NounDefiniteness.MA3RIFA_MAWSUL,
    "construct": NounDefiniteness.MA3RIFA_IDAFA,
    "ma3rifa_idafa": NounDefiniteness.MA3RIFA_IDAFA,
    "definite": NounDefiniteness.MA3RIFA_3AHD,
    "ma3rifa_3ahd": NounDefiniteness.MA3RIFA_3AHD,
    "indefinite": NounDefiniteness.NAKIRA,
    "nakira": NounDefiniteness.NAKIRA,
}

# ── Proper noun kind feature → ProperNounKind mapping
_PROPER_MAP = {
    "personal": ProperNounKind.SHAKHSI,
    "shakhsi": ProperNounKind.SHAKHSI,
    "place": ProperNounKind.MAKAN,
    "makan": ProperNounKind.MAKAN,
    "time": ProperNounKind.ZAMAN,
    "zaman": ProperNounKind.ZAMAN,
    "title": ProperNounKind.LAQAB,
    "laqab": ProperNounKind.LAQAB,
    "kunya": ProperNounKind.KUNYA,
    "transferred": ProperNounKind.MANQUL,
    "manqul": ProperNounKind.MANQUL,
    "compound": ProperNounKind.MURAKKAB,
    "murakkab": ProperNounKind.MURAKKAB,
    "borrowed": ProperNounKind.MUQTARAD,
    "muqtarad": ProperNounKind.MUQTARAD,
}

# ── Attribute kind feature → NominalAttributeKind mapping
_ATTR_KIND_MAP = {
    "sifa_mushabbaha": NominalAttributeKind.SIFA_MUSHABBAHA,
    "ism_fa3il": NominalAttributeKind.ISM_FA3IL,
    "ism_maf3ul": NominalAttributeKind.ISM_MAF3UL,
    "wasf_jamid": NominalAttributeKind.WASF_JAMID,
    "nisba": NominalAttributeKind.NISBA,
    "lawn": NominalAttributeKind.LAWN,
    "ayb": NominalAttributeKind.AYB,
    "qabiliyya": NominalAttributeKind.QABILIYYA,
}


# ═══════════════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════════════


def classify_noun_direction(
    closure: LexicalClosure,
    concept: Concept,
) -> NounDirection:
    """Determine the noun's primary direction (جهة اسمية — Art. 4, 64).

    Uses the concept's :attr:`semantic_type` as the primary signal, with
    the closure's POS as a secondary disambiguator.
    """
    # Proper noun → FARD (individual)
    if closure.features.get(_FEAT_PROPER):
        return NounDirection.FARD

    # Adjective-like POS → nominal attribute
    if closure.pos is POS.SIFA:
        return NounDirection.SIFA_ISMIYYA

    return _STYPE_TO_DIRECTION.get(
        concept.semantic_type, NounDirection.UNKNOWN
    )


def classify_universality(concept: Concept) -> NounUniversality:
    """Determine if the noun is universal or particular (Art. 24-28).

    A concept with ``properties["particular"] == True`` is treated as
    particular (جزئي); otherwise it is universal (كلي) since most
    common nouns denote kinds that apply to many instances.
    """
    if concept.properties.get("particular"):
        return NounUniversality.JUZ2I
    return NounUniversality.KULLI


def classify_genus_level(
    concept: Concept,
    direction: NounDirection,
) -> NounGenusLevel:
    """Determine genus / species / individual level (Art. 29-33)."""
    if direction is NounDirection.FARD:
        return NounGenusLevel.FARD

    # Concepts explicitly tagged with "genus" or "species" in properties
    level = concept.properties.get("genus_level", "")
    if level == "genus":
        return NounGenusLevel.JINS
    if level == "species":
        return NounGenusLevel.NAW3
    if level == "individual":
        return NounGenusLevel.FARD

    # Default heuristic: ENTITY with universality → NAW3 (species)
    if concept.semantic_type is SemanticType.ENTITY:
        return NounGenusLevel.NAW3

    return NounGenusLevel.UNKNOWN


def classify_proper_noun(
    closure: LexicalClosure,
) -> Optional[ProperNounKind]:
    """If the noun is a proper noun, classify its sub-type (Art. 34-37).

    Returns ``None`` when the closure does not represent a proper noun.
    """
    proper_val = closure.features.get(_FEAT_PROPER)
    if not proper_val:
        return None

    # If the feature value is a string, map it to the enum
    if isinstance(proper_val, str):
        return _PROPER_MAP.get(proper_val.lower(), ProperNounKind.UNKNOWN)

    # Boolean True with no further detail → personal
    return ProperNounKind.SHAKHSI


def classify_nominal_attribute(
    closure: LexicalClosure,
) -> NounAttributeRecord:
    """Determine if the noun is a nominal attribute (Art. 38-40)."""
    # Explicit attribute kind in features
    attr_str = closure.features.get(_FEAT_ATTR_KIND, "")
    if isinstance(attr_str, str) and attr_str:
        kind = _ATTR_KIND_MAP.get(attr_str.lower())
        if kind is not None:
            return NounAttributeRecord(
                attribute_kind=kind,
                is_nominal_attribute=True,
            )

    # POS-based heuristic
    if closure.pos in _POS_TO_ATTR_KIND:
        return NounAttributeRecord(
            attribute_kind=_POS_TO_ATTR_KIND[closure.pos],
            is_nominal_attribute=True,
        )

    return NounAttributeRecord(
        attribute_kind=None,
        is_nominal_attribute=False,
    )


def determine_inflection(
    closure: LexicalClosure,
) -> NounInflectionRecord:
    """Extract number, gender, and definiteness (Art. 41-50)."""
    num_str = closure.features.get(_FEAT_NUMBER, "")
    gen_str = closure.features.get(_FEAT_GENDER, "")
    def_str = closure.features.get(_FEAT_DEFINITENESS, "")

    number = (
        _NUMBER_MAP.get(num_str.lower(), NounNumber.UNKNOWN)
        if isinstance(num_str, str) and num_str
        else NounNumber.UNKNOWN
    )
    gender = (
        _GENDER_MAP.get(gen_str.lower(), NounGender.UNKNOWN)
        if isinstance(gen_str, str) and gen_str
        else NounGender.UNKNOWN
    )
    definiteness = (
        _DEF_MAP.get(def_str.lower(), NounDefiniteness.UNKNOWN)
        if isinstance(def_str, str) and def_str
        else NounDefiniteness.UNKNOWN
    )

    return NounInflectionRecord(
        number=number,
        gender=gender,
        definiteness=definiteness,
    )


def determine_composition(
    closure: LexicalClosure,
) -> NounCompositionRecord:
    """Determine composition type and origin (Art. 51-55)."""
    comp_val = closure.features.get(_FEAT_COMPOUND, "")
    if isinstance(comp_val, str) and comp_val:
        comp_lower = comp_val.lower()
        if comp_lower in ("mazji", "blend"):
            composition = NounComposition.MURAKKAB_MAZJI
        elif comp_lower in ("ismi", "compound", "true"):
            composition = NounComposition.MURAKKAB_ISMI
        else:
            composition = NounComposition.BASIT
    else:
        composition = NounComposition.BASIT

    borrowed_val = closure.features.get(_FEAT_BORROWED, "")
    if isinstance(borrowed_val, str) and borrowed_val:
        b_lower = borrowed_val.lower()
        if b_lower in ("settled", "mustaqirr", "true"):
            origin = NounOrigin.MUQTARAD_MUSTAQIRR
        elif b_lower in ("unsettled", "ghayr_mustaqirr"):
            origin = NounOrigin.MUQTARAD_GHAYR_MUSTAQIRR
        else:
            origin = NounOrigin.ASIL
    elif borrowed_val is True:
        origin = NounOrigin.MUQTARAD_MUSTAQIRR
    else:
        origin = NounOrigin.ASIL

    return NounCompositionRecord(
        composition=composition,
        origin=origin,
    )


def determine_morphology(
    closure: LexicalClosure,
) -> NounMorphologyRecord:
    """Extract material, pattern type, and root (Art. 56-58)."""
    derived_val = closure.features.get(_FEAT_DERIVED, "")
    if isinstance(derived_val, str) and derived_val:
        d_lower = derived_val.lower()
        if d_lower in ("true", "mushtaqq", "derived"):
            pattern_type = NounPatternType.WAZN_MUSHTAQQ
        elif d_lower in ("fixed", "thabit"):
            pattern_type = NounPatternType.QALIB_THABIT
        else:
            pattern_type = NounPatternType.WAZN_JAMID
    elif derived_val is True:
        pattern_type = NounPatternType.WAZN_MUSHTAQQ
    else:
        pattern_type = NounPatternType.WAZN_JAMID

    return NounMorphologyRecord(
        material=closure.lemma,
        pattern_type=pattern_type,
        pattern=closure.pattern,
        root=closure.root,
    )


def compute_signification(
    concept: Concept,
    direction: NounDirection,
) -> NounSignificationRecord:
    """Compute مطابقة / تضمن / التزام for the noun (Art. 59-62).

    * **mutabaqa** — the concept label (exact denotation).
    * **tadammun** — conceptual constituents the name includes.
    * **iltizam** — necessary concomitants implied by the name.
    """
    mutabaqa = concept.label

    # Tadammun: if the concept has properties, each key is an included
    # aspect of the noun's meaning.
    tadammun: Tuple[str, ...] = tuple(
        sorted(str(k) for k in concept.properties if k != "particular" and k != "genus_level")
    )

    # Iltizam: derive concomitants from the semantic type and direction.
    iltizam_parts: list[str] = []
    if concept.semantic_type is SemanticType.ENTITY:
        iltizam_parts.append("existence")
    if direction is NounDirection.FARD:
        iltizam_parts.append("individuation")
    if direction is NounDirection.SIFA_ISMIYYA:
        iltizam_parts.append("qualification")
    iltizam: Tuple[str, ...] = tuple(iltizam_parts)

    return NounSignificationRecord(
        mutabaqa=mutabaqa,
        tadammun=tadammun,
        iltizam=iltizam,
    )


def check_minimum(
    morph: NounMorphologyRecord,
    classif: NounClassificationRecord,
    attr: NounAttributeRecord,
    infl: NounInflectionRecord,
    comp: NounCompositionRecord,
    signif: NounSignificationRecord,
) -> NounMinimumRecord:
    """Verify the eight minimum-completeness conditions (Art. 11-19)."""
    # 1. الثبوت — the noun has a stable lexical form
    thubut = bool(morph.material)

    # 2. الحد — distinguished from verb / particle / non-independent part
    hadd = morph.pattern_type is not NounPatternType.UNKNOWN

    # 3. الامتداد — lexical, classificatory, referential extent
    imtidad = classif.universality is not NounUniversality.UNKNOWN

    # 4. المقوِّم — material + pattern + direction + type + referability
    muqawwim = bool(morph.material and morph.root)

    # 5. العلاقة البنائية — structural relation (ref / universality etc.)
    alaqa = classif.genus_level is not NounGenusLevel.UNKNOWN

    # 6. الانتظام — not mere phonetic juxtaposition
    intizam = bool(morph.pattern)

    # 7. الوحدة — the lexeme is one identifiable nominal unit
    wahda = comp.composition is not NounComposition.UNKNOWN

    # 8. قابلية التعيين — can be judged for type, ref, etc.
    qabiliyyat = (
        infl.number is not NounNumber.UNKNOWN
        or infl.gender is not NounGender.UNKNOWN
        or infl.definiteness is not NounDefiniteness.UNKNOWN
        or attr.is_nominal_attribute
        or bool(signif.mutabaqa)
    )

    return NounMinimumRecord(
        thubut=thubut,
        hadd=hadd,
        imtidad=imtidad,
        muqawwim=muqawwim,
        alaqa_binaiyya=alaqa,
        intizam=intizam,
        wahda=wahda,
        qabiliyyat_ta3yin=qabiliyyat,
    )


def compute_readiness(
    direction: NounDirection,
    type_: SemanticType,
    classif: NounClassificationRecord,
    number: NounNumber,
    gender: NounGender,
    def_: NounDefiniteness,
    recoverable: bool,
) -> float:
    """Compute Ready_N = (Dir+Type+Ref+Num+Gen+Def+Recover) / 7 (Art. 75)."""
    dir_score = _score_component(direction, NounDirection.UNKNOWN)
    type_score = 1.0  # SemanticType has no UNKNOWN member
    ref_score = _score_component(
        classif.universality, NounUniversality.UNKNOWN
    )
    num_score = _score_component(number, NounNumber.UNKNOWN)
    gen_score = _score_component(gender, NounGender.UNKNOWN)
    def_score = _score_component(def_, NounDefiniteness.UNKNOWN)
    recover_score = 1.0 if recoverable else 0.0

    total = (
        dir_score + type_score + ref_score
        + num_score + gen_score + def_score + recover_score
    )
    return round(total / 7.0, 4)


def _determine_existential_aspect(
    concept: Concept,
) -> NounExistentialAspect:
    """Map a concept to an existential aspect (Art. 21-23)."""
    return _STYPE_TO_EXISTENTIAL.get(
        concept.semantic_type, NounExistentialAspect.UNKNOWN
    )


def build_noun_fractal(
    closure: LexicalClosure,
    concept: Concept,
    *,
    noun_id: Optional[str] = None,
) -> NounFractalRecord:
    """Build a complete :class:`NounFractalRecord` (Art. 73-74).

    This is the primary public entry point.  It composes all sub-records
    from the raw ``LexicalClosure`` + ``Concept`` pair.
    """
    nid = noun_id or _next_id()

    direction = classify_noun_direction(closure, concept)
    universality_val = classify_universality(concept)
    genus = classify_genus_level(concept, direction)
    proper = classify_proper_noun(closure)
    attr = classify_nominal_attribute(closure)
    infl = determine_inflection(closure)
    comp = determine_composition(closure)
    morph = determine_morphology(closure)
    signif = compute_signification(concept, direction)

    classif = NounClassificationRecord(
        universality=universality_val,
        genus_level=genus,
        proper_noun_kind=proper,
    )

    minimum = check_minimum(morph, classif, attr, infl, comp, signif)

    # Recoverability: can the noun be traced to its root / pattern?
    recoverable = bool(morph.root and morph.pattern)

    readiness_score = compute_readiness(
        direction,
        concept.semantic_type,
        classif,
        infl.number,
        infl.gender,
        infl.definiteness,
        recoverable,
    )

    if readiness_score >= _READINESS_THRESHOLD:
        readiness = NounReadiness.READY
    elif readiness_score > 0.0:
        readiness = NounReadiness.PARTIAL
    else:
        readiness = NounReadiness.NOT_READY

    existential = _determine_existential_aspect(concept)

    return NounFractalRecord(
        noun_id=nid,
        lemma=closure.lemma,
        surface=closure.surface,
        direction=direction,
        conceptual_type=concept.semantic_type,
        morphology=morph,
        classification=classif,
        attribute=attr,
        inflection=infl,
        composition=comp,
        signification=signif,
        minimum=minimum,
        fractal_stage=NounFractalStage.TA3YIN,
        readiness=readiness,
        readiness_score=readiness_score,
        existential_aspect=existential,
    )


def validate_noun_fractal(
    fractal: NounFractalRecord,
) -> NounValidationResult:
    """Validate a :class:`NounFractalRecord` (Art. 76-77).

    Acceptance criteria:
      1. Material is not empty.
      2. Pattern type is not UNKNOWN.
      3. Direction is not UNKNOWN.
      4. Conceptual type is set (always true — no UNKNOWN in SemanticType).
      5. Classification universality is not UNKNOWN.
      6. Inflection axes are not all UNKNOWN.
      7. The noun can be recovered to its root.
      8. Readiness score ≥ θ_RN.
    """
    errors: list[str] = []

    if not fractal.morphology.material:
        errors.append("material_empty")
    if fractal.morphology.pattern_type is NounPatternType.UNKNOWN:
        errors.append("pattern_type_unknown")
    if fractal.direction is NounDirection.UNKNOWN:
        errors.append("direction_unknown")
    if fractal.classification.universality is NounUniversality.UNKNOWN:
        errors.append("universality_unknown")
    if (
        fractal.inflection.number is NounNumber.UNKNOWN
        and fractal.inflection.gender is NounGender.UNKNOWN
        and fractal.inflection.definiteness is NounDefiniteness.UNKNOWN
    ):
        errors.append("inflection_all_unknown")
    if not fractal.morphology.root:
        errors.append("root_empty")
    if fractal.readiness_score < _READINESS_THRESHOLD:
        errors.append("readiness_below_threshold")

    return NounValidationResult(
        valid=len(errors) == 0,
        errors=tuple(errors),
        readiness_score=fractal.readiness_score,
    )


def batch_build(
    closures: List[LexicalClosure],
    concepts: List[Concept],
) -> List[NounFractalRecord]:
    """Build :class:`NounFractalRecord` for each (closure, concept) pair.

    Both lists must have the same length.  Only closures with
    ``pos == POS.ISM`` are processed; others are silently skipped.
    """
    if len(closures) != len(concepts):
        msg = (
            f"closures ({len(closures)}) and concepts ({len(concepts)}) "
            f"must have the same length"
        )
        raise ValueError(msg)

    results: list[NounFractalRecord] = []
    for closure, concept in zip(closures, concepts):
        if closure.pos is POS.ISM:
            results.append(build_noun_fractal(closure, concept))
    return results
