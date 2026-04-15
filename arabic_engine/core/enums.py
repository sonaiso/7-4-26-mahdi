"""Enumerations used across the Arabic engine.

Each enum encodes a discrete, finite category so that every linguistic
label in the system is a computable integer — not a free-form string.
"""

from __future__ import annotations

from enum import Enum, auto

# ── Part of Speech ──────────────────────────────────────────────────


class POS(Enum):
    """Arabic part-of-speech tags (اسم / فعل / حرف + sub-types)."""

    ISM = auto()  # اسم
    FI3L = auto()  # فعل
    HARF = auto()  # حرف
    SIFA = auto()  # صفة
    ZARF = auto()  # ظرف
    DAMIR = auto()  # ضمير
    UNKNOWN = auto()


# ── Semantic (ontological) type ─────────────────────────────────────


class SemanticType(Enum):
    """High-level concept categories (التعريف 5 — ontological mapping)."""

    ENTITY = auto()  # ذات
    EVENT = auto()  # حدث
    ATTRIBUTE = auto()  # صفة
    RELATION = auto()  # علاقة
    NORM = auto()  # حكم شرعي / قاعدة


# ── Dalāla (signification) type ─────────────────────────────────────


class DalalaType(Enum):
    """Kinds of signification linking signifier → signified."""

    MUTABAQA = auto()  # مطابقة – exact denotation
    TADAMMUN = auto()  # تضمن  – inclusion (part of meaning)
    ILTIZAM = auto()  # التزام – implication (necessary concomitant)
    ISNAD = auto()  # إسناد – predication
    TAQYID = auto()  # تقييد – restriction / qualification
    IDAFA = auto()  # إضافة – genitive construction
    IHALA = auto()  # إحالة – referential link


# ── Truth state ─────────────────────────────────────────────────────


class TruthState(Enum):
    """Epistemic status of a proposition (التعريف 8)."""

    CERTAIN = auto()  # قطعي
    PROBABLE = auto()  # ظني راجح
    POSSIBLE = auto()  # ممكن
    DOUBTFUL = auto()  # مشكوك
    FALSE = auto()  # باطل
    UNKNOWN = auto()


# ── Guidance state ──────────────────────────────────────────────────


class GuidanceState(Enum):
    """Normative/actionable status derived from evaluation."""

    OBLIGATORY = auto()  # واجب
    RECOMMENDED = auto()  # مستحب
    PERMISSIBLE = auto()  # مباح
    DISLIKED = auto()  # مكروه
    FORBIDDEN = auto()  # حرام
    NOT_APPLICABLE = auto()


# ── I'rāb (syntactic inflection) ────────────────────────────────────


class IrabCase(Enum):
    """Grammatical case markers."""

    RAF3 = auto()  # رفع
    NASB = auto()  # نصب
    JARR = auto()  # جر
    JAZM = auto()  # جزم
    SUKUN = auto()  # سكون (مبني)
    UNKNOWN = auto()


class IrabRole(Enum):
    """Syntactic role in the sentence."""

    FA3IL = auto()  # فاعل
    MAF3UL_BIH = auto()  # مفعول به
    MUBTADA = auto()  # مبتدأ
    KHABAR = auto()  # خبر
    FI3L = auto()  # فعل
    MUDAF = auto()  # مضاف
    MUDAF_ILAYH = auto()  # مضاف إليه
    SIFA = auto()  # صفة
    HAL = auto()  # حال
    TAMYIZ = auto()  # تمييز
    ZARF = auto()  # ظرف
    JARR_MAJRUR = auto()  # جار ومجرور
    UNKNOWN = auto()


# ── Time / Space references (v2) ────────────────────────────────────


class TimeRef(Enum):
    """Temporal anchors for propositions."""

    PAST = auto()  # ماض
    PRESENT = auto()  # حاضر
    FUTURE = auto()  # مستقبل
    ETERNAL = auto()  # أزلي / دائم
    UNSPECIFIED = auto()


class SpaceRef(Enum):
    """Spatial anchors for propositions."""

    HERE = auto()  # هنا
    THERE = auto()  # هناك
    NAMED = auto()  # مكان محدد بالاسم
    UNSPECIFIED = auto()


# ── Mafhūm types (Ch. 21) ───────────────────────────────────────────


class ConstraintType(Enum):
    """Structural constraint types in the Manṭūq (أنواع القيد البنيوي).

    Each constraint type generates a corresponding Mafhūm type when
    combined with a mental counterpart and a transition rule.
    """

    SHART = auto()  # شرط — condition (تعليق الحكم)
    GHAYA = auto()  # غاية — goal / endpoint (تحديد المنتهى)
    ADAD = auto()  # عدد — number (التحديد الكمي)
    WASF = auto()  # وصف — description (التقييد الوصفي)
    ISHARA = auto()  # إشارة — reference / deixis (التخصيص الإحالي)


class MafhumType(Enum):
    """Minimal types of Mafhūm (الأنواع الدنيا للمفهوم — Ch. 21).

    These are the five irreducible concept types that arise from the
    structure of the Manṭūq itself, each covering an independent domain:
      • SHART  — domain of suspension (تعليق)
      • GHAYA  — domain of limit / endpoint (حد ومنتهى)
      • ADAD   — domain of quantitative restriction (تحديد كمي)
      • WASF   — domain of qualitative restriction (تقييد نوعي)
      • ISHARA — domain of referential specification (تخصيص مرجعي)
    """

    SHART = auto()  # مفهوم الشرط
    GHAYA = auto()  # مفهوم الغاية
    ADAD = auto()  # مفهوم العدد
    WASF = auto()  # مفهوم الوصف
    ISHARA = auto()  # مفهوم الإشارة


# ── D_min Phonological layer ─────────────────────────────────────────
# Implements: D_min(x) = (u, c, g, f, t)
# where every field maps to a computable integer, making the full
# 5-tuple a numeric vector over ℕ⁵.


class PhonCategory(Enum):
    """Major phonological category — الفئة الكبرى (c in D_min)."""

    CONSONANT = auto()  # صامت
    SEMI_VOWEL = auto()  # شبه صامت / صائت ذو تحولات (و ي)
    LONG_VOWEL = auto()  # صائت طويل / حامل كتابي (ا)
    SHORT_VOWEL = auto()  # صائت قصير (فتحة ضمة كسرة)
    SUKUN = auto()  # علامة انعدام حركة (ْ)
    SHADDA = auto()  # علامة بنيوية / تضعيف (ّ)
    TANWIN = auto()  # حركة/علامة مركبة / تنوين (ً ٌ ٍ)
    SPECIAL_MARK = auto()  # علامة مدّ/همز خاصة (ٰ ٓ)


class PhonGroup(Enum):
    """Phonological/articulatory group — المجموعة الكبرى (g in D_min)."""

    # ── Consonant articulation groups (مجموعات الصوامت) ────────────
    HNJ_MZM = auto()  # حنجري/مزمَري — ء
    HNJ_HLQ = auto()  # حنجري/حلقي   — ه
    HLQ = auto()  # حلقي          — ح ع غ
    HLQ_LHW = auto()  # حلقي/لهوي     — خ
    LHW = auto()  # لهوي          — ق
    TBQ_LHW = auto()  # طبقي/لهوي     — ك
    SHJR = auto()  # شجري/حنكي     — ج ش
    ASN_LTH = auto()  # أسناني-لثوي   — ت د
    ASN_LTH_MTPQ = auto()  # أسناني-لثوي مطبق — ط
    BAYNASN = auto()  # بين-أسناني    — ث ذ
    BAYNASN_MTPQ = auto()  # بين-أسناني مطبق — ظ
    LTH = auto()  # لثوي          — ر ل ن (with feature distinctions)
    LTH_MTPQ = auto()  # لثوي مطبق     — ض
    ASLI = auto()  # أسلي/صفيري    — ز س
    ASLI_MTPQ = auto()  # أسلي مطبق     — ص
    SHF = auto()  # شفوي          — ب م (with feature distinctions)
    SHF_ASN = auto()  # شفوي-أسناني   — ف
    SHF_LYN = auto()  # شفوي لين      — و (semi-vowel)
    HNK_LYN = auto()  # حنكي لين      — ي (semi-vowel)
    # ── Long vowel (الصوائت الطويلة) ──────────────────────────────
    ALF_LV = auto()  # ألف           — ا
    # ── Short vowel / diacritic groups (الحركات والعلامات) ─────────
    FTH = auto()  # فتح           — َ (U+064E)
    DMM = auto()  # ضم            — ُ (U+064F)
    KSR = auto()  # كسر           — ِ (U+0650)
    SKN_GRP = auto()  # سكون          — ْ (U+0652)
    SHD_GRP = auto()  # شدة           — ّ (U+0651)
    TAN_FTH = auto()  # تنوين فتح     — ً (U+064B)
    TAN_DMM = auto()  # تنوين ضم      — ٌ (U+064C)
    TAN_KSR = auto()  # تنوين كسر     — ٍ (U+064D)
    ALF_KHNJ = auto()  # ألف خنجرية    — ٰ (U+0670)
    MDD_GRP = auto()  # مدة           — ٓ (U+0653)


class PhonFeature(Enum):
    """Minimal phonological features — السمات الدنيا (f in D_min).

    Each value is a unique power-of-two bit-position, enabling a compact
    integer bitmask: feature_mask = Σ 2^(f.value-1) for f in features.
    """

    # Manner of articulation (طريقة النطق)
    SHADID = auto()  # شديد   — stop / plosive
    RAKHW = auto()  # رخو    — fricative / continuant
    MURAKKAB = auto()  # مركب   — affricate
    MUTAWASSIT = auto()  # متوسط  — intermediate manner
    TAKRIR = auto()  # مكرر   — trill / vibrant
    MUNHARIF = auto()  # منحرف  — lateral
    TAFSHI = auto()  # تفشٍّ  — diffuse / spread
    # Voicing (الجهر والهمس)
    MAJHUR = auto()  # مجهور  — voiced
    MAHMOUS = auto()  # مهموس  — voiceless
    # Secondary articulation (الصفات الثانوية)
    ITBAQ = auto()  # مطبق   — pharyngealization / emphatic
    MSTALI = auto()  # مستعلٍ — dorsal elevation
    SAFIR = auto()  # صفيري  — sibilant / whistling
    ANFI = auto()  # أنفي   — nasal
    GHUNNA = auto()  # غنّي   — nasality / resonance
    LAYIN = auto()  # لين    — sonorant
    ASTTALA = auto()  # استطالة — prolongation (ض)
    HMZ = auto()  # همزي   — hamza-bearing
    # Vowel / nucleus features (الصوائت)
    NUWAWI = auto()  # نووي   — nuclear / syllabic
    QASIR = auto()  # قصير   — short vowel
    TAWIL = auto()  # طويل   — long vowel
    ITLAL = auto()  # اعتلال — defective / weak
    # Mark features (العلامات)
    SIFR_HARAKA = auto()  # صفر حركة — zero-vowel
    QAFIL = auto()  # قفل      — syllable closure
    TADFIF = auto()  # تضعيف   — gemination mark
    MD_KHAS = auto()  # مدّ خاص  — special extension mark


class PhonTransform(Enum):
    """Minimal transformations and functions — التحولات/الوظائف الدنيا (t in D_min).

    Each value is a unique power-of-two bit-position enabling a bitmask:
    transform_mask = Σ 2^(t.value-1) for t in transforms.
    """

    # Phonological processes (العمليات الصوتية)
    TAHQIQ = auto()  # تحقيق       — full realization
    TASHIL = auto()  # تسهيل       — facilitation / weakening
    IBDAL = auto()  # إبدال       — phonemic substitution
    HADHF = auto()  # حذف         — deletion / elision
    HAMLI_HAMZI = auto()  # حمل همزي    — hamza hosting
    IDGHAM = auto()  # إدغام       — assimilation / merging
    IDGHAM_SHAMSI = auto()  # إدغام شمسي  — solar (regressive) assimilation
    IZHAR_QAMARI = auto()  # إظهار قمري  — lunar clarity
    IZHAR = auto()  # إظهار       — clear articulation
    IKHFAA = auto()  # إخفاء       — nasalized concealment
    IQLAB = auto()  # إقلاب       — metamorphosis (ن → م before ب)
    TAFKHIM = auto()  # تفخيم       — velarization / emphasis
    TARQIQ = auto()  # ترقيق       — thinning / palatalization
    TAKRIR_TR = auto()  # تكرير       — trill articulation
    TAFSHI_TR = auto()  # تفشٍّ صوتي  — acoustic diffusion
    TAMATHUL = auto()  # تماثل       — progressive assimilation
    MADD = auto()  # مدّ         — vowel lengthening
    ITLAL_TR = auto()  # اعتلال      — weak-letter process
    ASTTALA_TR = auto()  # استطالة     — prolongation process
    # Morphological functions (الوظائف الصرفية)
    ASAL_JADHARI = auto()  # أصل جذري    — root-radical origin
    ZIYADA = auto()  # زيادة       — morphological augmentation
    BINA_SARFI = auto()  # بنية صرفية  — morphological structure
    BINA_ISHTIQAQI = auto()  # بناء اشتقاقي — derivational structure
    WAZIFA_SARFIYYA = auto()  # وظيفة صرفية — morphological function marker
    WAZN = auto()  # بناء وزني   — prosodic-pattern building
    # Syntactic / grammatical functions (الوظائف النحوية)
    TAAREF = auto()  # تعريف       — definiteness (لام التعريف)
    TAWKID = auto()  # توكيد       — emphasis marker
    TANWIN_FUNC = auto()  # تنوين       — nunation function
    JAZM = auto()  # جزم         — apocopation / jussive
    IIRAB = auto()  # إعراب       — grammatical case marking
    TANKIR = auto()  # تنكير       — indefiniteness
    JAM = auto()  # جمع         — pluralization marker
    ATAF = auto()  # عطف         — coordination marker
    NISBAH = auto()  # نسبة        — relational adjective marker
    MUTAKALLIM = auto()  # متكلم       — first-person marker
    DAMIR_FUNC = auto()  # هاء ضمير    — pronoun function
    TADFIF_TR = auto()  # تضعيف       — gemination function
    MAQTAA = auto()  # بناء مقطع مغلق — closed-syllable building
    HAMZA_CARRIER = auto()  # حامل كتابي  — orthographic hamza carrier


# ── Transition Engine — قانون الانتقال بين الخانات ──────────────────


class TransitionType(Enum):
    """الأنواع الكبرى للانتقال — the four major classes of cell transition."""

    FUNCTIONAL = auto()  # انتقال وظيفي    — same element, changed function
    RANK = auto()  # انتقال رتبي     — movement between phonetic tiers
    CONTEXTUAL = auto()  # انتقال تجاوري   — neighbour-driven transition
    MORPHO_STRUCTURAL = auto()  # انتقال بنيوي صرفي — pattern/template-driven


class TransitionLaw(Enum):
    """القوانين الجزئية للانتقال — the seven partial transition laws."""

    ITLAL = auto()  # اعتلال  — weak-letter transformation (ا و ي)
    IDGHAM = auto()  # إدغام   — gemination: C+C → Shadda
    IBDAL = auto()  # إبدال   — substitution within phonetic family
    HADHF = auto()  # حذف     — deletion from surface to deep structure
    WAQF = auto()  # وقف     — pause-final phonological reduction
    ZIYADA = auto()  # زيادة   — root element re-slotted as augment
    INZILAQ = auto()  # انزلاق  — glide ↔ long-vowel transition (و / ي)


class TransitionCondition(Enum):
    """شروط الانتقال — the five conditions required for a valid transition."""

    STRUCTURAL_VALIDITY = auto()  # بقاء داخل الأنماط المسموحة
    PHONETIC_BALANCE = auto()  # التخفيف دون الإفساد
    ROOT_PRESERVATION = auto()  # إمكان استرجاع الجذر بعد الانتقال
    FUNCTION_PRESERVATION = auto()  # وضوح الوظيفة بعد الانتقال
    NON_CONTRADICTION = auto()  # عدم الوقوع في صورة ممنوعة


class SyllablePosition(Enum):
    """موضع العنصر في المقطع — element's position inside the syllable."""

    ONSET = auto()  # بداية المقطع  — syllable onset (C)
    NUCLEUS = auto()  # نواة المقطع   — syllable nucleus (V)
    CODA = auto()  # نهاية المقطع  — syllable coda (C)
    INTER_WORD = auto()  # حدّ الكلمة    — word boundary


class FunctionRole(Enum):
    """الدور الوظيفي للعنصر — element's morpho-syntactic role in the word."""

    ROOT_RADICAL = auto()  # أصل جذري   — part of the tri-literal root
    AUGMENT = auto()  # زيادة      — morphological augment
    VOWEL_CARRIER = auto()  # حامل صائتي — vowel / nucleus carrier
    CASE_MARKER = auto()  # علامة إعراب — case / mood marker
    DEFINITENESS = auto()  # أداة تعريف  — definiteness particle
    PRONOUN = auto()  # ضمير       — pronominal clitic
    UNKNOWN = auto()  # غير محدد   — undetermined


# ── Functional Transition Schema — الانتقال الوظيفي المنضبط ──────────
# The following enums mirror the JSON Schema defined in
# arabic_engine/data/transition_record.schema.json and form the
# Python side of the formal functional-transition layer.


class CellType(Enum):
    """خانة الانتقال — cell identifier in the functional transition schema.

    Consonants (صوامت):
        C_ROOT_PLAIN       — plain root consonant (صامت جذري سهل)
        C_MULTI_FUNCTION   — multi-function / ambiguous consonant (صامت متعدد الوظائف)
        C_AUGMENTATIVE     — augmentative consonant (صامت زيادة)
        C_GLIDE_BACK       — back glide و (حرف لين خلفي)
        C_GLIDE_FRONT      — front glide ي (حرف لين أمامي)

    Long vowels (صوائت طويلة):
        V_LONG_A           — long /aː/ — ا
        V_LONG_W           — long /uː/ — و
        V_LONG_Y           — long /iː/ — ي

    Diacritics / short vowels (حركات):
        D_FATHA            — فتحة
        D_DAMMA            — ضمة
        D_KASRA            — كسرة
        D_SUKUN            — سكون
        D_SHADDA           — شدة
        D_TANWEEN_FATH     — تنوين فتح
        D_TANWEEN_DAMM     — تنوين ضم
        D_TANWEEN_KASR     — تنوين كسر

    Meta-cells (خانات بنيوية):
        CELL_ILLA                  — weak/defective letter structure (علّة)
        CELL_IMPLICIT              — deleted-but-recoverable element (ضمني)
        CELL_WAQF_COMPRESSED       — pause-compressed ending (وقف مضغوط)
        CELL_EXISTENTIAL           — pure existential state (وجود مطلق)
        CELL_EXISTENTIAL_TEMPORAL  — time-bound existential state (وجود زمني)
        CELL_EVENT_SOURCE          — abstract event / maṣdar source (حدث مصدري)
        CELL_EVENT_TEMPORAL        — temporalised event / verb form (حدث زمني)
        CELL_CAUSAL_INTERNAL       — self-contained causation (تسبب داخلي)
        CELL_CAUSAL_EXTERNAL       — external causation (تسبب خارجي)
    """

    # Consonants
    C_ROOT_PLAIN = auto()
    C_MULTI_FUNCTION = auto()
    C_AUGMENTATIVE = auto()
    C_GLIDE_BACK = auto()
    C_GLIDE_FRONT = auto()
    # Long vowels
    V_LONG_A = auto()
    V_LONG_W = auto()
    V_LONG_Y = auto()
    # Diacritics
    D_FATHA = auto()
    D_DAMMA = auto()
    D_KASRA = auto()
    D_SUKUN = auto()
    D_SHADDA = auto()
    D_TANWEEN_FATH = auto()
    D_TANWEEN_DAMM = auto()
    D_TANWEEN_KASR = auto()
    # Meta-cells
    CELL_ILLA = auto()
    CELL_IMPLICIT = auto()
    CELL_WAQF_COMPRESSED = auto()
    CELL_EXISTENTIAL = auto()
    CELL_EXISTENTIAL_TEMPORAL = auto()
    CELL_EVENT_SOURCE = auto()
    CELL_EVENT_TEMPORAL = auto()
    CELL_CAUSAL_INTERNAL = auto()
    CELL_CAUSAL_EXTERNAL = auto()


class FuncTransitionClass(Enum):
    """صنف الانتقال الوظيفي — broad classification of a functional transition."""

    PHONOLOGICAL = auto()  # صوتي
    MORPHOLOGICAL = auto()  # صرفي
    ORTHOGRAPHIC = auto()  # إملائي / وقفي
    CAUSAL = auto()  # سببي
    TEMPORAL = auto()  # زمني
    EXISTENTIAL = auto()  # وجودي
    ABSTRACTIVE = auto()  # تجريدي


class EvidenceType(Enum):
    """نوع الدليل — the kind of evidence supporting a transition record."""

    LEXICAL = auto()  # معجمي
    PATTERN = auto()  # نمطي / وزني
    PHONOLOGICAL_CONTEXT = auto()  # سياق صوتي
    MORPH_CONTEXT = auto()  # سياق صرفي
    SURFACE_ONLY = auto()  # سطحي فقط
    DEEP_ANALYSIS = auto()  # تحليل عميق


class ReversibleValue(Enum):
    """قابلية الانتقال للعكس — whether a transition can be reversed."""

    YES = auto()  # قابل للعكس دائمًا
    NO = auto()  # غير قابل للعكس
    CONDITIONAL = auto()  # قابل للعكس بشرط


class ConditionToken(Enum):
    """رمز الشرط — atomic DSL token for preconditions and blocking conditions.

    Each value is a computable, snake_case label that can be evaluated
    against a context object.  The tokens cover:
      * phonological structure conditions (بنية صوتية)
      * morphological and lexical conditions (صرف ومعجم)
      * syllabic / positional conditions (مقطع وموضع)
      * causal / temporal / existential conditions (سبب / زمن / وجود)
    """

    # Glide / vowel structure
    GLIDE_LOSES_CONSONANTAL_LOAD = auto()
    SEGMENT_BECOMES_VOCALIC_NUCLEUS = auto()
    SYLLABLE_STRUCTURE_ALLOWS_LENGTHENING = auto()
    SEGMENT_REQUIRED_AS_EXPLICIT_ONSET = auto()
    SEGMENT_ENTERS_CONSONANTAL_POSITION = auto()
    SURFACE_REQUIRES_GLIDE_LINKING = auto()
    # Weak / implicit structure
    WEAK_SEGMENT_DELETED_ON_SURFACE = auto()
    DEEP_STRUCTURE_PRESERVED = auto()
    PATTERN_RECOVERS_MISSING_SLOT = auto()
    DELETION_CAUSES_ROOT_AMBIGUITY = auto()
    # Vowel extension
    FATHA_EXTENDED = auto()
    DAMMA_EXTENDED = auto()
    KASRA_EXTENDED = auto()
    SEGMENT_FORMS_INDEPENDENT_LONG_NUCLEUS = auto()
    # Gemination / compression
    TWO_IDENTICAL_CONSONANTS_IN_SEQUENCE = auto()
    COMPRESSION_ALLOWED = auto()
    IDENTITY_NOT_PROVEN = auto()
    AUGMENTATIVE_CONSONANT_CONTACTS_SIMILAR_OR_IDENTICAL_SEGMENT = auto()
    MORPH_PATTERN_ALLOWS_ASSIMILATION = auto()
    STRONG_SIMILARITY_OR_IDENTITY = auto()
    SURFACE_COMPRESSION_PERMITTED = auto()
    # Vowel drop / resyllabification
    MORPHOLOGICAL_CHANGE_DROPS_SHORT_VOWEL = auto()
    DROPPING_VOWEL_BREAKS_ALLOWED_SYLLABLE_PATTERN = auto()
    SEGMENT_REQUIRES_OPENING = auto()
    PATTERN_OR_LINKING_REQUIRES_MOVEMENT = auto()
    SEGMENT_REQUIRES_BACK_ROUNDING = auto()
    SEGMENT_REQUIRES_FRONTING = auto()
    # Root / augment classification
    SEGMENT_FUNCTIONS_AS_AUGMENTATIVE_MARKER = auto()
    ROOT_SLOTS_IDENTIFIED_INDEPENDENTLY = auto()
    LEXICON_CONFIRMS_SEGMENT_IS_ROOT_MEMBER = auto()
    CONTEXT_FAVORS_AUGMENTATIVE_READING = auto()
    PATTERN_REQUIRES_NON_ROOT_FUNCTION = auto()
    LEXICON_CONFIRMS_ROOT_STATUS = auto()
    SEGMENT_REQUIRED_FOR_ROOT_IDENTITY = auto()
    # Glide-as-augment
    WAAW_FUNCTIONS_AS_NON_ROOT_INCREMENT = auto()
    PATTERN_SUPPORTS_INCREMENTAL_ROLE = auto()
    ROOT_MEMBERSHIP_OF_WAAW_PROVEN = auto()
    YAA_FUNCTIONS_AS_NON_ROOT_INCREMENT = auto()
    ROOT_MEMBERSHIP_OF_YAA_PROVEN = auto()
    # Pause / waqf
    WORD_FINAL_POSITION = auto()
    PAUSE_MODE_ENABLED = auto()
    WEAK_FINAL_STRUCTURE_COMPRESSIBLE = auto()
    # Surface deletion
    SURFACE_DELETION_ALLOWED = auto()
    DEEP_RECOVERABILITY_PRESERVED = auto()
    ROOT_IDENTITY_COLLAPSES = auto()
    # Causal
    EXTERNAL_TRANSFORMER_APPEARS = auto()
    EFFECT_MOVES_BEYOND_ACTOR = auto()
    EXTERNAL_TRANSFORMER_REMOVED = auto()
    EFFECT_COLLAPSES_BACK_TO_SUBJECT = auto()
    # Temporal / existential
    ABSTRACT_EVENT_LINKED_TO_TIME_REFERENCE = auto()
    TIME_REFERENCE_REMOVED = auto()
    TEMPORAL_OPERATOR_APPLIED = auto()
    EXISTENTIAL_STATE_BOUND_TO_TIME = auto()
    TEMPORAL_OPERATOR_REMOVED = auto()


# ── AEU Periodic-Table enums ────────────────────────────────────────


class ElementClass(Enum):
    """تصنيف العنصر — structural class of an alphabetic encoding unit."""

    BASE_LETTER = auto()  # حرف أساسي
    VOWEL_MARKER = auto()  # علامة حركة
    STRUCTURAL_MARKER = auto()  # علامة بنيوية
    CARRIER_RELATED_UNIT = auto()  # وحدة مرتبطة بحامل
    COMPOSITE_DECISION_UNIT = auto()  # وحدة قرار مركبة


class ElementLayer(Enum):
    """طبقة العنصر — the architectural layer an AEU belongs to."""

    PHONOLOGICAL = auto()  # صوتية
    ORTHOGRAPHIC = auto()  # كتابية
    STRUCTURAL = auto()  # بنيوية
    MIXED = auto()  # مختلطة


class ElementFunction(Enum):
    """وظيفة العنصر — the functional role an AEU carries."""

    IDENTITY_BEARING = auto()  # حامل هوية
    MOTION_BEARING = auto()  # حامل حركة
    LENGTH_BEARING = auto()  # حامل طول
    CLOSURE_BEARING = auto()  # حامل إغلاق
    DUPLICATION_BEARING = auto()  # حامل تضعيف
    INDEFINITENESS_BEARING = auto()  # حامل تنكير
    ENCODING_BEARING = auto()  # حامل ترميز


class CombinationType(Enum):
    """نوع الاندماج — how an AEU combines with neighbours."""

    STANDALONE = auto()  # مستقل
    ATTACHES_TO_BASE = auto()  # يلتصق بالأساس
    CLUSTER_INTERNAL = auto()  # داخل عنقود
    CONTEXT_DEPENDENT = auto()  # معتمد على السياق


class UnicodeProfileType(Enum):
    """نوع الملف الموحد — Unicode rendering profile of an AEU."""

    SINGLE_CODE_POINT = auto()  # نقطة رمز واحدة
    COMBINING_MARK = auto()  # علامة تجميعية
    CONTEXTUAL_RENDERING = auto()  # عرض سياقي


class ProofStatus(Enum):
    """حالة الإثبات — proof/verification status of an AEU."""

    PROVEN = auto()  # مُثبَت
    PENDING = auto()  # قيد الإثبات
    ASSUMED = auto()  # مفترض — accepted without formal proof
    COMPOSITE = auto()  # مُركَّب


# ── Axiom-layer enums (الأصول الخمسة) ────────────────────────────────


class SlotState(Enum):
    """حالة الموضع — state of a structural slot (A1/A2)."""

    EMPTY = auto()  # فارغ قابل للامتلاء
    OCCUPIED = auto()  # مشغول بموجب أول
    BLOCKED = auto()  # محجوب بنيويًا


class OntologicalLayer(Enum):
    """الطبقة الوجودية — ontological rank for layer promotion (A4).

    Encodes the hierarchy: cell → transition → syllable → root → pattern.
    Each level requires the previous to be complete before promotion.
    """

    CELL = auto()  # خانة — atomic phonological cell
    TRANSITION = auto()  # انتقال — directed transition between cells
    SYLLABLE = auto()  # مقطع — syllable-level grouping
    ROOT = auto()  # جذر — root-level abstraction
    PATTERN = auto()  # وزن — morphological pattern


class OntologicalMode(Enum):
    """النمط الوجودي — the mode of existence of a linguistic element.

    Separates ontological kinds so that elements from different modes
    cannot be compared directly (Rank Law / قانون الرتبة).

    =========  ==========================================
    Mode        Description (Arabic / English)
    =========  ==========================================
    SLOT        موضع قابل للامتلاء — fillable structural position
    UNIT        وحدة قاعدية — atomic base unit (letter)
    MODIFIER    محمول تشغيلي — operational modifier (vowel mark)
    COMPOSITE   تركيب — composite construct (syllable, word)
    STRUCTURE   بنية — structural template (root, pattern)
    CONSTRAINT  قيد — constraint or condition
    =========  ==========================================
    """

    SLOT = auto()  # موضع — structural position (Structural Zero)
    UNIT = auto()  # وحدة — base unit (consonant / letter)
    MODIFIER = auto()  # محمول — modifier (short vowel, sukun, shadda)
    COMPOSITE = auto()  # تركيب — composite (syllable, morpheme)
    STRUCTURE = auto()  # بنية — structural template (root, pattern)
    CONSTRAINT = auto()  # قيد — condition / constraint


class TriadType(Enum):
    """نوع الثلاثية — the formal type of a triadic block.

    Every triad must declare its type before entering computation
    (قانون نوع المثلث).

    ==============  ==============================================
    Type             Description
    ==============  ==============================================
    DISTINCTIVE      مثلث تمييزي — previous / centre / next
    HIERARCHICAL     مثلث رتبي — apex / left-branch / right-branch
    GENERATIVE       مثلث توليدي — base / motion / constraint
    ==============  ==============================================
    """

    DISTINCTIVE = auto()  # تمييزي — سابق / مركز / لاحق
    HIERARCHICAL = auto()  # رتبي — قمة / ضلع / ضلع
    GENERATIVE = auto()  # توليدي — قاعدة / حركة / قيد


class RankType(Enum):
    """نوع الرتبة — the rank classification derived from limit/capacity balance.

    Implements Law 3 (قانون الحد والسعة):
      * L ≫ C → LIMITAL   (حدّي)
      * C ≫ L → CAPACITIVE (سعوي)
      * L ≈ C → TRANSITIONAL (انتقالي)
    """
    LIMITAL = auto()        # حدّي — limit-dominant
    CAPACITIVE = auto()     # سعوي — capacity-dominant
    TRANSITIONAL = auto()   # انتقالي — balanced / transitional


# ── Signified Ontology v1.0 ─────────────────────────────────────────
# The following enums encode the Arabic Signified Ontology across
# 8 top-level axes and 7 cross-cutting descriptive dimensions.

class PrimarySignifiedType(Enum):
    """النوع الأعلى للمدلول — the 8 top-level signified classes."""
    ONTOLOGICAL = auto()      # وجودي — entity / property / event
    RELATIONAL = auto()       # علائقي — relation between terms
    PROPOSITIONAL = auto()    # قضوي — proposition-level meaning
    REFERENTIAL = auto()      # إحالي — reference / deixis
    FUNCTIONAL = auto()       # وظيفي — structural / functional
    PRAGMATIC = auto()        # تداولي — pragmatic / speech-act
    LOGICAL = auto()          # منطقي — logical entailment
    RHETORICAL = auto()       # بلاغي — figurative / rhetorical


class OntologicalSubtype(Enum):
    """الأنواع الفرعية الوجودية — subtypes under OntologicalType."""
    # EntityMeaning — الذات
    INDIVIDUAL_ENTITY = auto()      # ذات فردية
    GENERIC_ENTITY = auto()         # ذات نوعية
    GENUS_ENTITY = auto()           # ذات جنسية
    PROPER_NAMED_ENTITY = auto()    # ذات مسماة بعلم
    COLLECTIVE_ENTITY = auto()      # ذات جمعية
    MASS_ENTITY = auto()            # ذات مادية
    MENTAL_ENTITY = auto()          # ذات ذهنية
    EXTERNAL_ENTITY = auto()        # ذات خارجية
    # PropertyMeaning — الصفة
    STABLE_PROPERTY = auto()        # صفة ثابتة
    ACCIDENTAL_PROPERTY = auto()    # صفة عرضية
    STATE_PROPERTY = auto()         # صفة حالية
    QUANTITY_PROPERTY = auto()      # صفة كمية
    QUALITY_PROPERTY = auto()       # صفة كيفية
    EVALUATIVE_PROPERTY = auto()    # صفة تقييمية
    COMPARATIVE_PROPERTY = auto()   # صفة مقارنة
    # EventMeaning — الحدث
    ACTION_EVENT = auto()           # حدث فعلي
    ABSTRACT_EVENT = auto()         # حدث مجرد
    CHANGE_OF_STATE_EVENT = auto()  # حدث تغير حالة
    CAUSATIVE_EVENT = auto()        # حدث سببي
    AFFECTED_EVENT = auto()         # حدث انفعالي
    MOTION_EVENT = auto()           # حدث حركي
    STATIC_EVENT = auto()           # حدث سكوني
    MENTAL_EVENT = auto()           # حدث ذهني
    EMOTIONAL_EVENT = auto()        # حدث وجداني
    SPEECH_EVENT = auto()           # حدث كلامي


class RelationalSubtype(Enum):
    """الأنواع الفرعية العلائقية — subtypes under RelationalType."""
    SPATIAL = auto()            # مكاني
    TEMPORAL_REL = auto()       # زماني
    CAUSAL = auto()             # سببي
    FINAL = auto()              # غائي
    ACCOMPANIMENT = auto()      # معيّة
    INSTRUMENTAL = auto()       # أدائي
    POSSESSIVE = auto()         # ملكية
    CONDITIONAL = auto()        # شرطي
    EXCEPTIONAL = auto()        # استثنائي
    COMPARATIVE_REL = auto()    # مقارن
    PART_WHOLE = auto()         # جزئي-كلي
    ATTRIBUTIVE = auto()        # وصفي
    PREDICATIVE = auto()        # إسنادي
    DEPENDENCY = auto()         # تبعي


class PropositionalSubtype(Enum):
    """الأنواع الفرعية القضوية — subtypes under PropositionalType."""
    ASSERTION = auto()                  # إثبات
    NEGATION = auto()                   # نفي
    INTERROGATIVE = auto()              # استفهام
    PROBABILITY = auto()                # احتمال
    EMPHASIS = auto()                   # توكيد
    CONDITIONAL_PROP = auto()           # شرط قضوي
    RESTRICTION = auto()                # تقييد / حصر
    CORRECTION = auto()                 # تصحيح / استدراك
    REPORTIVE_CONFIRMATION = auto()     # تأكيد خبري


class ReferentialSubtype(Enum):
    """الأنواع الفرعية الإحالية — subtypes under ReferentialType."""
    PRONOUN = auto()            # ضمير
    DEICTIC = auto()            # إشاري
    RELATIVE = auto()           # موصول
    INTERROGATIVE_REF = auto()  # استفهامي
    VOCATIVE = auto()           # ندائي
    DEFINITE = auto()           # معرّف
    INDEFINITE = auto()         # نكرة
    ANAPHORIC = auto()          # عائد نصي
    CATAPHORIC = auto()         # عائد قبلي
    PRESENCE = auto()           # حضوري
    DISTANCE = auto()           # بعدي


class FunctionalSubtype(Enum):
    """الأنواع الفرعية الوظيفية — subtypes under FunctionalType."""
    CONNECTOR = auto()          # رابط
    SEPARATOR = auto()          # فاصل
    INITIALIZER = auto()        # مبتدئ
    STRUCTURAL_OP = auto()      # عامل بنيوي
    CASE_FUNC = auto()          # وظيفة إعرابية
    GOVERNANCE = auto()         # عمل نحوي
    ABROGATIVE = auto()         # ناسخ
    RANK_SHIFT = auto()         # تحويل رتبي
    DISCOURSE_LINKER = auto()   # رابط خطابي


class PragmaticSubtype(Enum):
    """الأنواع الفرعية التداولية — subtypes under PragmaticType."""
    INTENTIONAL = auto()                # قصدي
    CONTEXTUAL = auto()                 # مقامي
    INTERACTIONAL = auto()              # تفاعلي
    SPEECH_ACT = auto()                 # فعل كلامي
    PRESUPPOSITIONAL = auto()           # افتراضي
    CONVERSATIONAL_IMPLICATURE = auto() # استلزام حواري
    SOCIAL = auto()                     # اجتماعي


class LogicalSubtype(Enum):
    """الأنواع الفرعية المنطقية — subtypes under LogicalType."""
    DENOTATIVE = auto()             # دلالة مطابقة
    INCLUSIVE = auto()              # دلالة تضمن
    ENTAILED = auto()               # دلالة التزام
    PRESUPPOSED_LOGICAL = auto()    # اقتضاء منطقي
    CONDITIONAL_LOGICAL = auto()    # شرط منطقي
    NECESSARY = auto()              # لزوم
    CONTRADICTORY = auto()          # تناقض
    CONTRARY = auto()               # تضاد
    UNIVERSAL = auto()              # عموم
    PARTICULAR = auto()             # خصوص
    RESTRICTIVE = auto()            # تقييدي
    PREDICATIVE_LOGICAL = auto()    # حملي


class RhetoricalSubtype(Enum):
    """الأنواع الفرعية البلاغية — subtypes under RhetoricalType."""
    METAPHORICAL = auto()   # استعاري
    METONYMIC = auto()      # مجازي مرسل
    SYMBOLIC = auto()        # رمزي
    KINAYAH = auto()        # كنائي
    ALLUSIVE = auto()       # تلميحي
    IMAGISTIC = auto()      # تصويري
    AFFECTIVE = auto()      # انفعالي / وجداني
    AESTHETIC = auto()      # جمالي


# ── Cross-cutting axes (§3 — السمات العابرة المشتركة) ────────────────

class DependencyDegree(Enum):
    """درجة الاستقلال — how dependent a signified is on other elements."""
    INDEPENDENT = auto()                # مستقل
    BEARER_DEPENDENT = auto()           # محتاج لمحل
    REFERENT_DEPENDENT = auto()         # محتاج لمرجع
    RELATIONALLY_DEPENDENT = auto()     # محتاج لأطراف نسبة
    CONTEXT_DEPENDENT = auto()          # محتاج لسياق
    PROPOSITION_DEPENDENT = auto()      # محتاج لقضية


class ExistenceMode(Enum):
    """نمط الوجود — the mode of existence for the signified."""
    MENTAL = auto()             # ذهني
    EXTERNAL = auto()           # خارجي
    CONVENTIONAL = auto()       # عرفي
    INSTITUTIONAL = auto()      # مؤسسي
    IMAGINED = auto()           # متخيل
    FIGURATIVE = auto()         # مجازي


class SpecificityDegree(Enum):
    """درجة التعيين — how specific / determined the signified is."""
    UNDEFINED = auto()              # غير محدد
    INDEFINITE_SPEC = auto()        # نكرة
    DEFINITE_SPEC = auto()          # معرفة
    DEICTICALLY_FIXED = auto()      # معيّن إشاريًا
    ANAPHORICALLY_FIXED = auto()    # معيّن عائديًا
    PROPERLY_NAMED = auto()         # معيّن بالعلمية


class CompositionDegree(Enum):
    """درجة التركيب — structural complexity of the signified."""
    SIMPLE = auto()             # بسيط
    COMPOSITE = auto()          # مركب
    PREDICATIVE_COMP = auto()   # إسنادي
    NETWORKED = auto()          # شبكي


class SignifiedTemporalStatus(Enum):
    """الوضع الزمني للمدلول — temporal aspect of the signified.

    Prefixed with 'SIG' variants to avoid clashes with TimeRef.
    """
    SURFACE_VALIDITY = auto()           # صحة البنية السطحية
    LEXICAL_ACCESS = auto()             # وجود مدخل معجمي
    CONTEXT_RESOLUTION = auto()         # كفاية السياق
    CONCEPT_SELECTION = auto()          # اختيار المفهوم الصحيح
    FIGURATIVE_DISAMBIGUATION = auto()  # وجود قرينة مجازية
    REFERENTIAL_RESOLUTION = auto()     # توفر المرجع الإحالي
    LOGICAL_COHERENCE = auto()          # تسق التفسير مع البنية


# ── Epistemic v1 — Knowledge Episode Validator enums ─────────────────


class EpistemicRank(Enum):
    """الرتبة الإبستيمية — epistemic certainty tier of a validated episode.

    ==========================  =============================================
    Member                       Meaning
    ==========================  =============================================
    CERTAIN                      قطعي — existence + complete proof
    TRUE_NON_CERTAIN             صحيح غير قطعي — valid but revisable
    PROBABILISTIC_DOUBT          ظني — probable / uncertain
    IMPOSSIBLE                   ممتنع — method-fit failure or conflict
    REJECTED_METHODOLOGICALLY    ساقط منهجيًا — foundational condition missing
    ==========================  =============================================
    """
    CERTAIN = auto()
    TRUE_NON_CERTAIN = auto()
    PROBABILISTIC_DOUBT = auto()
    IMPOSSIBLE = auto()
    REJECTED_METHODOLOGICALLY = auto()


class ValidationState(Enum):
    """حالة التصديق — validation outcome of a knowledge episode.

    ==========  =============================
    Member       Meaning
    ==========  =============================
    VALID        صالح — all checks passed
    INVALID      غير صالح — one or more checks failed
    PENDING      قيد الفحص — not yet validated
    ==========  =============================
    """
    VALID = auto()
    INVALID = auto()
    PENDING = auto()


class JudgementType(Enum):
    """نوع الحكم — the type of judgement issued by a knowledge episode.

    ================  ==========================================
    Member             Meaning
    ================  ==========================================
    EXISTENCE          حكم وجودي — existence claim (قطعي عند تمامه)
    ESSENCE            حكم ماهوي — what-is-it claim
    ATTRIBUTE          حكم وصفي — attribute / quality claim
    RELATION           حكم علائقي — relational claim
    CAUSAL             حكم سببي — cause-effect claim
    INTERPRETIVE       حكم تفسيري — interpretation / hermeneutic
    FORMAL             حكم شكلي — formal / logical claim
    NORMATIVE          حكم معياري — obligation / value / rule
    PURE_LINGUISTIC    حكم لغوي صرف — purely linguistic claim
    METAPHYSICAL       حكم ما ورائي — metaphysical claim
    ================  ==========================================
    """
    EXISTENCE = auto()
    ESSENCE = auto()
    ATTRIBUTE = auto()
    RELATION = auto()
    CAUSAL = auto()
    INTERPRETIVE = auto()
    FORMAL = auto()
    NORMATIVE = auto()
    PURE_LINGUISTIC = auto()
    METAPHYSICAL = auto()


class MethodFamily(Enum):
    """عائلة المنهج — the methodological family used in an episode.

    ==============  ===========================================
    Member           Meaning
    ==============  ===========================================
    RATIONAL         عقلي — general rational cognition
    SCIENTIFIC       علمي تجريبي — empirical / experimental
    LINGUISTIC       لغوي — utterance / concept analysis
    MATHEMATICAL     رياضي — formal symbolic proof
    PHYSICAL         فيزيائي — physical law and measurement
    ==============  ===========================================
    """
    RATIONAL = auto()
    SCIENTIFIC = auto()
    LINGUISTIC = auto()
    MATHEMATICAL = auto()
    PHYSICAL = auto()


class CarrierType(Enum):
    """نوع الحامل اللغوي — which linguistic carrier(s) are present.

    ===========  ====================================
    Member        Meaning
    ===========  ====================================
    UTTERANCE     منطوق فقط — utterance only
    CONCEPT       مفهوم فقط — concept only
    BOTH          كلاهما — both utterance and concept
    ===========  ====================================
    """
    UTTERANCE = auto()
    CONCEPT = auto()
    BOTH = auto()


class RealityKind(Enum):
    """نوع الواقع — the kind of reality an anchor refers to.

    =================  =====================================
    Member              Meaning
    =================  =====================================
    MATERIAL_OBJECT     شيء مادي — tangible physical object
    TEXT_OBJECT          نص — written / spoken text
    EVENT                حدث — observable event
    ABSTRACT             مجرد — abstract entity
    FORMAL_STRUCTURE     بنية شكلية — formal / mathematical
    =================  =====================================
    """
    MATERIAL_OBJECT = auto()
    TEXT_OBJECT = auto()
    EVENT = auto()
    ABSTRACT = auto()
    FORMAL_STRUCTURE = auto()


class SenseModality(Enum):
    """الحاسة — the sensory modality of a trace.

    ================  ================================
    Member             Meaning
    ================  ================================
    VISION             بصر — sight
    HEARING            سمع — hearing
    TOUCH              لمس — touch
    PROPRIOCEPTION     حس داخلي — body awareness
    INTERNAL           إدراك ذهني — internal cognition
    ================  ================================
    """
    VISION = auto()
    HEARING = auto()
    TOUCH = auto()
    PROPRIOCEPTION = auto()
    INTERNAL = auto()


class TraceMode(Enum):
    """نمط الأثر — how the sensory trace was obtained.

    ===================  =====================================
    Member                Meaning
    ===================  =====================================
    DIRECT_PERCEPTION     إدراك مباشر — first-hand perception
    MEDIATED              بواسطة — mediated observation
    REPORTED              منقول — reported by another
    INFERRED              مستنبط — inferred, not observed
    ===================  =====================================
    """
    DIRECT_PERCEPTION = auto()
    MEDIATED = auto()
    REPORTED = auto()
    INFERRED = auto()


class LinkKind(Enum):
    """نوع الربط — the linking method used in the knowledge episode.

    ==================  =========================================
    Member               Meaning
    ==================  =========================================
    TEXTUAL_INFERENCE    استدلال نصي — inference from text
    CAUSAL               ربط سببي — causal link
    ANALOGY              قياس — analogical reasoning
    DEDUCTION            استنباط — deductive reasoning
    INDUCTION            استقراء — inductive reasoning
    ABDUCTION            استنتاج تفسيري — abductive reasoning
    ==================  =========================================
    """
    TEXTUAL_INFERENCE = auto()
    CAUSAL = auto()
    ANALOGY = auto()
    DEDUCTION = auto()
    INDUCTION = auto()
    ABDUCTION = auto()


class ProofPathKind(Enum):
    """نوع مسار الإثبات — the kind of proof path used.

    ===========  ==========================================
    Member        Meaning
    ===========  ==========================================
    HISSI         حسي — sense-based proof
    AQLI          عقلي — rational proof
    FORMAL        برهاني شكلي — formal / symbolic proof
    LINGUISTIC    لغوي — linguistic proof
    COMPOSITE     مركب — composite / multi-path proof
    ===========  ==========================================
    """
    HISSI = auto()
    AQLI = auto()
    FORMAL = auto()
    LINGUISTIC = auto()
    COMPOSITE = auto()


class GapSeverity(Enum):
    """خطورة الفجوة — severity level of a validation gap.

    ========  ===================================
    Member     Meaning
    ========  ===================================
    FATAL      قاتل — blocks validation entirely
    HIGH       عالٍ — serious but not blocking
    MEDIUM     متوسط — informational
    ========  ===================================
    """
    FATAL = auto()
    HIGH = auto()
    MEDIUM = auto()


class ContaminationLevel(Enum):
    """مستوى التلوث — degree of prior-opinion contamination.

    ========  =========================================
    Member     Meaning
    ========  =========================================
    NONE       لا تلوث — no contamination
    LOW        منخفض — minor influence, acceptable
    MEDIUM     متوسط — noticeable, causes rejection
    HIGH       عالٍ — severe contamination, rejection
    ========  =========================================
    """
    NONE = auto()
    SOFT = auto()
    HARD = auto()
    UNRESOLVED = auto()


class RevisionType(Enum):
    """نوع المراجعة — type of belief revision."""

    CONFLICT_RESOLUTION = auto()
    EXTERNAL_EVIDENCE = auto()
    EXPANSION = auto()
    CONTRACTION = auto()
    REVISION = auto()


class SignalType(Enum):
    """نوع الإشارة — type of signal in the kernel."""

    BASE_LETTER = auto()
    DIACRITIC = auto()
    NUMERAL = auto()
    WHITESPACE = auto()
    PUNCTUATION = auto()
    UNKNOWN = auto()


# ── Strict 7-Layer System enums ──────────────────────────────────────


class StrictLayerID(Enum):
    """معرّف الطبقة الصارمة — layer identifier in the strict 7-layer system."""

    MENTAL_FOUNDATION = auto()
    GENERATIVE = auto()
    AUDITORY_MINIMUM = auto()
    STRUCTURAL = auto()
    TRANSFORMATION = auto()
    HIGHER_FUNCTION = auto()
    PROGRAMMATIC = auto()


class AuditoryNode(Enum):
    """عقدة الطبقة السمعية — node type in the auditory/phonological layer."""

    PHONEME = auto()
    SYLLABLE = auto()
    WORD_FORM = auto()
    PROSODIC = auto()
    ONSET = auto()
    NUCLEUS = auto()
    CODA = auto()


class StructuralNode(Enum):
    """عقدة بنيوية — structural node type."""

    ROOT = auto()
    PATTERN = auto()
    MORPHEME = auto()
    WORD = auto()
    AFFIX = auto()
    PREFIX = auto()
    SUFFIX = auto()
    CLITIC = auto()
    STEM = auto()


class TransformationNode(Enum):
    """عقدة التحول — transformation node type."""

    INPUT = auto()
    RULE = auto()
    OUTPUT = auto()
    TRIGGER = auto()
    CONTEXT = auto()
    RESULT = auto()
    INTERMEDIATE = auto()
    EXCEPTION = auto()


class MentalPrimitive(Enum):
    """البدائي الذهني — mental primitive type."""

    CONCEPT = auto()
    RELATION = auto()
    SCHEMA = auto()
    SCRIPT = auto()
    EVENT = auto()
    PROPERTY = auto()
    INDIVIDUAL = auto()
    PROCESS = auto()
    FRAME = auto()


class MentalEdgeType(Enum):
    """نوع الحافة الذهنية — mental graph edge type."""

    ASSOCIATION = auto()
    CAUSAL = auto()
    HIERARCHICAL = auto()
    TEMPORAL = auto()
    SPATIAL = auto()
    INSTRUMENTAL = auto()
    CONDITIONAL = auto()


class LayerEdgeType(Enum):
    """نوع الحافة بين الطبقات — edge type between system layers."""

    PROJECTION = auto()
    REALIZATION = auto()
    CONSTRAINT = auto()
    FEEDBACK = auto()
    ACTIVATION = auto()
    INHIBITION = auto()
    SUPPORT = auto()
    CONFLICT = auto()
    INHERITANCE = auto()
    COMPOSITION = auto()
    DEPENDENCY = auto()
    ENTAILMENT = auto()
    ANALOGY = auto()
    REVISION = auto()
    ENDORSEMENT = auto()
    CONTRADICTION = auto()
    ELABORATION = auto()
    SPECIFICATION = auto()
    GENERALIZATION = auto()
    INSTANCE = auto()
    PART_OF = auto()
    CAUSE = auto()
    EFFECT = auto()
    CONDITION = auto()
    CONCESSION = auto()
    CONTRAST = auto()
    PARALLEL = auto()
    TEMPORAL = auto()
    SPATIAL = auto()


class JudgmentCategory(Enum):
    """فئة الحكم — judgment category in layer 5."""

    ORIGINAL = auto()
    AUGMENTED = auto()
    SUBSTITUTED = auto()
    DELETED = auto()
    WEAKENED_TRANSFORMED = auto()
    ASSIMILATED = auto()
    ATTACHED_MARKER = auto()
    DEICTIC_BUILDER = auto()
    RELATIONAL_CONNECTOR = auto()


class GenerativeNode(Enum):
    """عقدة توليدية — generative node type."""

    BASE = auto()
    DERIVED = auto()
    COMPOUND = auto()
    PATTERN = auto()
    BROKEN_PLURAL = auto()
    VERBAL_NOUN = auto()
    PARTICIPLE = auto()
    DIMINUTIVE = auto()


class RepresentationNode(Enum):
    """عقدة تمثيلية — representation node type."""

    LEXICAL = auto()
    MORPHOLOGICAL = auto()
    SYNTACTIC = auto()
    SEMANTIC = auto()
    PRAGMATIC = auto()
    PHONOLOGICAL = auto()
    GRAPHEMIC = auto()
    DIACRITIC = auto()
    PROSODIC = auto()
    DISCOURSE = auto()


# ── Verb Fractal Constitution v1 enums ──────────────────────────────


class VerbTense(Enum):
    """الزمن في الفعل — verb tense (Art. 25–28)."""

    MADI = auto()       # ماضٍ
    MUDARI = auto()     # مضارع
    AMR = auto()        # أمر


class VerbVoice(Enum):
    """المبني للمعلوم / المجهول — verb voice."""

    ACTIVE = auto()     # معلوم
    PASSIVE = auto()    # مجهول


class VerbPerson(Enum):
    """الشخص في الفعل — verb person (Art. 29–31)."""

    FIRST = auto()      # متكلم
    SECOND = auto()     # مخاطب
    THIRD = auto()      # غائب


class VerbNumber(Enum):
    """العدد في الفعل — verb number."""

    SINGULAR = auto()   # مفرد
    DUAL = auto()       # مثنى
    PLURAL = auto()     # جمع


class VerbGender(Enum):
    """الجنس في الفعل — verb gender."""

    MASCULINE = auto()  # مذكر
    FEMININE = auto()   # مؤنث


class VerbTransitivity(Enum):
    """اللزوم والتعدي — verb transitivity (Art. 22)."""

    LAZIM = auto()                  # لازم
    MUTA3ADDI = auto()              # متعدٍّ
    MUTA3ADDI_LI_ITHNAYN = auto()   # متعدٍّ لاثنين
    MUTA3ADDI_LI_THALATHA = auto()  # متعدٍّ لثلاثة


class VerbBab(Enum):
    """الباب الصرفي — triliteral verb paradigm (Art. 32–35)."""

    FA3ALA_YAF3ULU = auto()   # فَعَلَ يَفْعُلُ
    FA3ALA_YAF3ILU = auto()   # فَعَلَ يَفْعِلُ
    FA3ALA_YAF3ALU = auto()   # فَعَلَ يَفْعَلُ
    FA3ILA_YAF3ALU = auto()   # فَعِلَ يَفْعَلُ
    FA3ULA_YAF3ULU = auto()   # فَعُلَ يَفْعُلُ
    FA3ILA_YAF3ILU = auto()   # فَعِلَ يَفْعِلُ
    OTHER = auto()             # غير ذلك


class VerbMode(Enum):
    """المجرد / المزيد / الناسخ — verb mode (Art. 36–50)."""

    MUJARRAD = auto()   # مجرد
    MAZID = auto()      # مزيد
    NASIKH = auto()     # ناسخ


class VerbAugmentation(Enum):
    """أبواب المزيد — augmentation patterns (Art. 36–39)."""

    IF3AL = auto()       # إفعال
    FA33ALA = auto()     # فعّل
    FA3ALA_III = auto()  # فاعَل
    INFA3ALA = auto()    # انفعل
    IFTA3ALA = auto()    # افتعل
    TAFA33ALA = auto()   # تفعّل
    TAFA3ALA = auto()    # تفاعل
    IF3ALLA = auto()     # افعلّ
    ISTAF3ALA = auto()   # استفعل
    NONE = auto()        # لا زيادة


class NasikhType(Enum):
    """نوع الناسخ — copular verb type (Art. 46–50)."""

    KANA = auto()    # كان وأخواتها
    KADA = auto()    # كاد وأخواتها
    ZANNA = auto()   # ظن وأخواتها


class VerbEventType(Enum):
    """نوع الحدث في الفعل — verb event type (Art. 20–24)."""

    SIMPLE_OCCURRENCE = auto()   # وقوع بسيط
    BECOMING = auto()            # صيرورة
    TRANSFORMATION = auto()      # تحول
    CAUSATION = auto()           # إحداث
    BEING_AFFECTED = auto()      # تأثر
    LINKING = auto()             # ربط فعلي


class VerbDerivativeType(Enum):
    """المشتقات الفعلية — verb derivative types (Art. 43)."""

    ISM_FA3IL = auto()    # اسم الفاعل
    ISM_MAF3UL = auto()   # اسم المفعول
    ISM_ZAMAN = auto()    # اسم الزمان
    ISM_MAKAN = auto()    # اسم المكان
    ISM_HAY2A = auto()    # اسم الهيئة
    ISM_ALA = auto()      # اسم الآلة
    MUBALAQA = auto()     # صيغة مبالغة
    MASDAR = auto()        # مصدر


class VerbReadiness(Enum):
    """جاهزية الفعل للتركيب — verb readiness for composition (Art. 62–64)."""

    READY = auto()       # جاهز
    NOT_READY = auto()   # غير جاهز
    PARTIAL = auto()     # جزئي


class TransitionGateStatus(Enum):
    """حالة بوابة الانتقال — status of a transition gate."""

    PASSED = auto()
    BLOCKED = auto()
    INSUFFICIENT_DATA = auto()


# ═══════════════════════════════════════════════════════════════════════
# Noun Fractal Constitution v1 — دستور الاسم الفراكتالي
# ═══════════════════════════════════════════════════════════════════════


class NounDirection(Enum):
    """الجهة الاسمية — primary nominal direction (Art. 4, 12, 14)."""

    DHAT = auto()           # ذات
    MARJI3 = auto()         # مرجع
    KULLI = auto()          # كلي
    JUZ2I = auto()          # جزئي
    JINS = auto()           # جنس
    NAW3 = auto()           # نوع
    FARD = auto()           # فرد
    SIFA_ISMIYYA = auto()   # صفة اسمية
    MAFHUM_ISMI = auto()    # مفهوم اسمي
    UNKNOWN = auto()


class NounUniversality(Enum):
    """الكلي والجزئي — universal vs. particular (Art. 24-28)."""

    KULLI = auto()   # كلي — applies to many
    JUZ2I = auto()   # جزئي — particular / individual
    UNKNOWN = auto()


class NounGenusLevel(Enum):
    """الجنس والنوع والفرد — genus / species / individual (Art. 29-33)."""

    JINS = auto()    # جنس — genus
    NAW3 = auto()    # نوع — species
    FARD = auto()    # فرد — individual
    UNKNOWN = auto()


class ProperNounKind(Enum):
    """أنواع العلم — proper-noun sub-types (Art. 34-37)."""

    SHAKHSI = auto()    # شخصي
    MAKAN = auto()      # مكان
    ZAMAN = auto()      # زمان
    LAQAB = auto()      # لقب
    KUNYA = auto()      # كنية
    MANQUL = auto()     # منقول
    MURAKKAB = auto()   # مركب
    MUQTARAD = auto()   # مقترض
    UNKNOWN = auto()


class NominalAttributeKind(Enum):
    """نوع الصفة الاسمية — nominal-attribute sub-types (Art. 38-40)."""

    SIFA_MUSHABBAHA = auto()  # صفة مشبهة
    ISM_FA3IL = auto()        # اسم فاعل
    ISM_MAF3UL = auto()       # اسم مفعول
    WASF_JAMID = auto()       # وصف جامد
    NISBA = auto()            # نسبة
    LAWN = auto()             # لون
    AYB = auto()              # عيب
    QABILIYYA = auto()        # قابلية
    UNKNOWN = auto()


class NounNumber(Enum):
    """الوحدة والكثرة — number (Art. 41-44)."""

    MUFRAD = auto()          # مفرد
    MUTHANNA = auto()        # مثنى
    JAM3 = auto()            # جمع
    ISM_JAM3 = auto()        # اسم جمع
    ISM_JINS_JAM3I = auto()  # اسم جنس جمعي
    UNKNOWN = auto()


class NounGender(Enum):
    """التذكير والتأنيث — gender (Art. 45-47)."""

    MUDHAKKAR = auto()         # مذكر
    MU2ANNATH_HAQIQI = auto()  # مؤنث حقيقي
    MU2ANNATH_MAJAZI = auto()  # مؤنث مجازي
    MU2ANNATH_LAFZI = auto()   # مؤنث لفظي
    MU2ANNATH_MA3NAWI = auto() # مؤنث معنوي
    UNKNOWN = auto()


class NounDefiniteness(Enum):
    """المعرفة والنكرة — definiteness (Art. 48-50)."""

    MA3RIFA_3ALAM = auto()   # معرفة بعلم
    MA3RIFA_DAMIR = auto()   # معرفة بضمير
    MA3RIFA_ISHARA = auto()  # معرفة بإشارة
    MA3RIFA_MAWSUL = auto()  # معرفة بموصول
    MA3RIFA_IDAFA = auto()   # معرفة بإضافة
    MA3RIFA_3AHD = auto()    # معرفة بعهد
    NAKIRA = auto()          # نكرة
    UNKNOWN = auto()


class NounComposition(Enum):
    """المركب الاسمي والمزجي — composition type (Art. 51-53)."""

    BASIT = auto()           # بسيط
    MURAKKAB_ISMI = auto()   # مركب اسمي
    MURAKKAB_MAZJI = auto()  # مركب مزجي
    UNKNOWN = auto()


class NounOrigin(Enum):
    """المقترض — origin / borrowing status (Art. 54-55)."""

    ASIL = auto()                       # أصيل — native Arabic
    MUQTARAD_MUSTAQIRR = auto()         # مقترض مستقر — settled loan
    MUQTARAD_GHAYR_MUSTAQIRR = auto()   # مقترض غير مستقر — unsettled loan
    UNKNOWN = auto()


class NounPatternType(Enum):
    """الوزن الجامد — pattern type (Art. 56-58)."""

    WAZN_JAMID = auto()      # وزن جامد
    WAZN_MUSHTAQQ = auto()   # وزن مشتق
    QALIB_THABIT = auto()    # قالب ثابت
    UNKNOWN = auto()


class NounSignificationType(Enum):
    """المطابقة والتضمن والالتزام — noun-internal signification (Art. 59-62)."""

    MUTABAQA = auto()   # مطابقة
    TADAMMUN = auto()   # تضمن
    ILTIZAM = auto()    # التزام


class NounFractalStage(Enum):
    """القانون الفراكتالي — fractal law cycle (Art. 63-69)."""

    TA3YIN = auto()    # تعيين
    HIFZ = auto()      # حفظ
    RABT = auto()      # ربط
    HUKM = auto()      # حكم
    INTIQAL = auto()   # انتقال
    RADD = auto()      # رد


class NounReadiness(Enum):
    """الجاهزية الاسمية — compositional readiness (Art. 70-72)."""

    READY = auto()       # جاهز
    PARTIAL = auto()     # جزئي
    NOT_READY = auto()   # غير جاهز


class NounExistentialAspect(Enum):
    """جهة الموجود — existential aspect of the noun (Art. 21-23)."""

    DHAT = auto()         # ذات
    SHAY2 = auto()        # شيء
    MAWDI3 = auto()       # موضع
    ZAMAN_JAMID = auto()  # زمان جامد
    MARJI3 = auto()       # مرجع
    MIQDAR = auto()       # مقدار
    UNKNOWN = auto()
