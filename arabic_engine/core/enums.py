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

    LIMITAL = auto()  # حدّي — limit-dominant
    CAPACITIVE = auto()  # سعوي — capacity-dominant
    TRANSITIONAL = auto()  # انتقالي — balanced / transitional


# ── Signified v2.0 — طبقة المدلول الموسّعة ──────────────────────────
# The twenty axes below extend the signified layer so that a Concept
# can encode not just its ontological *type* but also its epistemic
# standing, normative weight, affective charge, causal role, cultural
# scope, and every other dimension required to represent the full range
# of human conceptual knowledge.


class EpistemicStatus(Enum):
    """الوضع الإبستيمي — how knowledge of the concept is held (1/20).

    Complements :class:`TruthState` (which applies to propositions).
    ``EpistemicStatus`` applies to the *concept itself* and captures the
    epistemic grade at which the concept is known or postulated.
    """
    CERTAIN = auto()        # يقيني — known with certainty
    PROBABLE = auto()       # ظني    — probably true / held with high confidence
    DOUBTFUL = auto()       # مشكوك  — genuinely doubtful
    IMAGINED = auto()       # متخيَّل — constructed by imagination
    PRESUMED = auto()       # مفترض  — assumed without full proof
    NECESSARY = auto()      # ضروري  — necessarily true (cannot be otherwise)
    POSSIBLE = auto()       # ممكن   — possible but not certain
    IMPOSSIBLE = auto()     # ممتنع  — logically / ontologically impossible
    AXIOMATIC = auto()      # بديهي  — self-evident / axiomatic
    THEORETICAL = auto()    # نظري   — derived by theoretical reasoning


class NormativeCategory(Enum):
    """الجهة المعيارية المستقلة — normative / deontic category (2/20).

    Independent of :class:`GuidanceState` (which is a procedural
    evaluation output).  ``NormativeCategory`` encodes the *intrinsic*
    normative meaning carried by the concept.
    """
    OBLIGATORY = auto()     # واجب   — morally / legally required
    PERMISSIBLE = auto()    # مباح   — allowed without positive recommendation
    FORBIDDEN = auto()      # محظور  — prohibited
    RECOMMENDED = auto()    # مستحب  — recommended / praiseworthy
    DISAPPROVED = auto()    # مكروه  — disapproved / discouraged
    GOOD = auto()           # حسن    — ethically good
    BAD = auto()            # قبيح   — ethically bad
    JUST = auto()           # عادل   — just / fair
    UNJUST = auto()         # ظالم   — unjust / unfair
    NEUTRAL = auto()        # محايد  — normatively neutral


class AffectiveDimension(Enum):
    """البُعد الوجداني — the affective / emotional dimension (3/20).

    Concepts carry affective charge that shapes human understanding
    beyond purely rational classification.
    """
    LOVE = auto()           # محبة       — love / affection
    FEAR = auto()           # خوف        — fear / dread
    TRANQUILITY = auto()    # طمأنينة    — inner peace / tranquility
    ANXIETY = auto()        # قلق        — anxiety / worry
    AWE = auto()            # هيبة       — awe / reverence
    SHAME = auto()          # حياء/خجل   — shame / modesty
    HATE = auto()           # كراهية     — hatred / aversion
    INTIMACY = auto()       # أُنس       — intimacy / familiarity
    ALIENATION = auto()     # اغتراب     — alienation / estrangement
    JOY = auto()            # فرح        — joy / happiness
    GRIEF = auto()          # حزن        — grief / sorrow
    NEUTRAL = auto()        # محايد      — affectively neutral


class MentalIntentionalType(Enum):
    """نوع العقل القصدي الداخلي — intentional mental state type (4/20).

    Covers the inner mental life: concepts that are *about* other
    states (intentionality) rather than just representing external facts.
    """
    BELIEF = auto()         # اعتقاد   — propositional belief
    DESIRE = auto()         # رغبة     — desire / want
    INTENTION = auto()      # نية/قصد  — intention / purpose
    ATTENTION = auto()      # انتباه   — focal attention
    MEMORY = auto()         # تذكر     — memory / recollection
    EXPECTATION = auto()    # توقع     — expectation / anticipation
    DECISION = auto()       # قرار     — decision / resolution
    IMAGINATION = auto()    # تخيّل    — imagination / mental imagery
    PERCEPTION = auto()     # إدراك    — perceptual experience
    AWARENESS = auto()      # وعي      — consciousness / awareness


class ModalCategory(Enum):
    """الجهة المنطقية — alethic modal category (5/20).

    Encodes what is possible, necessary, impossible, or merely
    hypothetical — including counterfactual reasoning.
    """
    POSSIBLE = auto()           # ممكن           — possibly the case
    NECESSARY = auto()          # ضروري          — necessarily the case
    IMPOSSIBLE = auto()         # ممتنع          — impossible
    COUNTERFACTUAL = auto()     # مضاد للواقع    — contrary-to-fact
    HYPOTHETICAL = auto()       # افتراضي        — supposed for argument's sake
    ACTUAL = auto()             # واقعي          — actually obtaining


class FrameType(Enum):
    """نوع الإطار المفاهيمي — conceptual frame / scene type (6/20).

    Many concepts are only intelligible within a background frame
    (Charles Fillmore's frame semantics).  This enum names the most
    common encyclopaedic frames.
    """
    COMMERCIAL = auto()     # تجاري   — buying, selling, price, goods
    JOURNEY = auto()        # سفر     — traveller, path, destination, vehicle
    KINSHIP = auto()        # قرابة   — parent, child, sibling, lineage
    CONFLICT = auto()       # صراع   — adversary, battle, victory, defeat
    TEACHING = auto()       # تعليم   — teacher, student, lesson, assessment
    GOVERNANCE = auto()     # حكم    — ruler, law, authority, subject
    RELIGIOUS = auto()      # ديني   — worship, ritual, sacred, obligation
    MEDICAL = auto()        # طبي    — patient, symptom, diagnosis, treatment
    DOMESTIC = auto()       # منزلي  — household, family, dwelling, routine
    NONE = auto()           # لا إطار — no particular frame


class ScriptPhase(Enum):
    """مرحلة السيناريو الإجرائي — phase within a cognitive script (7/20).

    Schank & Abelson-style scripts: stereotyped event sequences.
    A concept may be located at a particular phase in such a sequence.
    """
    PRECONDITION = auto()   # شرط سابق    — must hold before script begins
    INITIATION = auto()     # بدء         — script-opening action
    DEVELOPMENT = auto()    # تطور        — main body of the script
    CLIMAX = auto()         # ذروة        — peak / pivotal moment
    RESOLUTION = auto()     # حلّ         — outcome / resolution
    POSTCONDITION = auto()  # نتيجة لاحقة — state that holds after script
    NONE = auto()           # لا سيناريو  — not script-bound


class CausalRole(Enum):
    """الدور السببي-التفسيري — causal / explanatory role (8/20).

    Human knowledge is built on causal models.  This enum labels
    the role a concept plays inside a causal-explanatory chain.
    """
    CAUSE = auto()      # سبب       — direct cause
    CONDITION = auto()  # شرط       — necessary / sufficient condition
    ENABLER = auto()    # مُمكِّن   — enables without directly causing
    BLOCKER = auto()    # مانع      — prevents / blocks an effect
    MECHANISM = auto()  # آلية      — the *how* of causation
    MEDIATOR = auto()   # وسيط      — intermediary in a causal chain
    EFFECT = auto()     # أثر/نتيجة — downstream effect
    GOAL = auto()       # غاية      — final cause / telos
    LAW = auto()        # قانون     — governing regularity / nomic law
    NONE = auto()       # لا دور    — no causal role assigned


class InstitutionalCategory(Enum):
    """التصنيف المؤسسي الاجتماعي — social / institutional category (9/20).

    Searle-style institutional facts: realities that exist only through
    collective acceptance (X counts as Y in context C).
    """
    STATE = auto()          # دولة     — state / sovereign entity
    LAW = auto()            # قانون    — legal rule or statute
    PROPERTY = auto()       # ملكية    — ownership right
    CONTRACT = auto()       # عقد      — binding agreement
    POSITION = auto()       # منصب     — social role / office
    INSTITUTION = auto()    # مؤسسة   — established organisation
    CURRENCY = auto()       # عملة     — medium of exchange
    NORM = auto()           # معيار    — social / conventional norm
    RITUAL = auto()         # طقس      — ceremonial practice
    NONE = auto()           # لا تصنيف — not an institutional fact


class CategorizationMode(Enum):
    """نمط التصنيف المفاهيمي — how the concept belongs to its category (10/20).

    Classical categories have crisp boundaries; prototype-based and
    fuzzy categories admit degrees of membership (Rosch, Zadeh).
    """
    CLASSICAL = auto()              # كلاسيكي        — necessary & sufficient conditions
    PROTOTYPE_BASED = auto()        # نموذجي         — graded membership around prototype
    FUZZY_BOUNDED = auto()          # ضبابي الحدود   — membership by degree (fuzzy sets)
    GRADIENT_MEMBERSHIP = auto()    # عضوية متدرجة   — continuous membership scale
    RADIAL = auto()                 # شعاعي          — radial network of related senses


class CulturalScope(Enum):
    """النطاق الثقافي الحضاري — cultural / civilisational scope (11/20).

    Marks whether a concept is universal or specific to a particular
    cultural, religious, or domain tradition.
    """
    UNIVERSAL = auto()          # كوني         — applies across all cultures
    CULTURE_SPECIFIC = auto()   # ثقافي خاص    — specific to one culture
    CIVILIZATIONAL = auto()     # حضاري        — shared within a civilisation
    DOMAIN_SPECIFIC = auto()    # تخصصي        — confined to a specialised domain
    RELIGIOUS_SPECIFIC = auto() # ديني خاص     — specific to a religious tradition


class DiachronicStatus(Enum):
    """الوضع التاريخي الدلالي — diachronic / historical semantic status (12/20).

    Tracks whether a concept has drifted, narrowed, broadened, or
    specialised relative to its original meaning.
    """
    ORIGINAL = auto()       # أصلي        — meaning as originally used
    SHIFTED = auto()        # منتقل       — meaning has shifted
    NARROWED = auto()       # ضيّق        — meaning has narrowed
    BROADENED = auto()      # موسَّع      — meaning has broadened
    SPECIALIZED = auto()    # تخصّص       — moved to technical domain
    GENERALIZED = auto()    # عمّ         — moved from technical to general use
    OBSOLETE = auto()       # متقادم      — no longer in active use


class ConceptFormationMode(Enum):
    """طريقة تكوين المفهوم — how the concept was formed (13/20).

    Distinguishes primitive atomic concepts from derived, composed,
    blended, or metaphorically extended ones.
    """
    PRIMITIVE = auto()              # أصلي بسيط       — irreducible primitive
    DERIVED = auto()                # مشتق            — derived from another concept
    COMPOSED = auto()               # مركّب           — composed from parts
    BLENDED = auto()                # ممزوج           — conceptual blend (Fauconnier)
    ANALOGICALLY_EXTENDED = auto()  # تمديد قياسي     — extended by analogy
    METAPHORICAL = auto()           # مجازي           — grounded in metaphor


class MetaConceptualLevel(Enum):
    """المستوى فوق المفاهيمي — meta-conceptual order (14/20).

    First-order concepts are *about* the world; second-order concepts
    are about first-order concepts; third-order are about the system
    of concepts itself.
    """
    FIRST_ORDER = auto()    # مستوى أول  — concepts about entities / events
    SECOND_ORDER = auto()   # مستوى ثان  — concepts about first-order concepts
    THIRD_ORDER = auto()    # مستوى ثالث — concepts about the conceptual system


class InterpretiveStability(Enum):
    """استقرار التفسير — interpretive stability / polysemy status (15/20).

    Some concepts have a single stable reading; others are ambiguous,
    polysemous, or actively contested.
    """
    STABLE = auto()             # ثابت           — single, stable interpretation
    AMBIGUOUS = auto()          # ملتبس          — genuinely ambiguous
    POLYSEMOUS = auto()         # متعدد المعاني  — multiple related senses
    CONTEXT_RESOLVED = auto()   # محدَّد بالسياق — disambiguation requires context
    CONTESTED = auto()          # متنازع عليه    — meaning is socially contested


class SalienceLevel(Enum):
    """مستوى البروز الإدراكي — cognitive salience / prominence level (16/20).

    In human cognition not all features / concepts are equally salient.
    This enum captures the prominence profile of a concept.
    """
    CENTRAL = auto()        # مركزي    — highly salient, prototype-like
    PERIPHERAL = auto()     # هامشي    — low salience, atypical
    FOREGROUNDED = auto()   # بارز     — brought to focal attention
    BACKGROUNDED = auto()   # خلفي     — presupposed, not in focus
    UNEXPECTED = auto()     # مفاجئ    — surprises the interpreter
    EXPECTED = auto()       # متوقع    — predicted by context


class EmbodiedDomain(Enum):
    """المجال الإدراكي المتجسد — embodied / perceptual domain (17/20).

    Lakoff & Johnson: many abstract concepts are grounded in
    embodied sensorimotor experience.  This enum names the source
    domain of that grounding.
    """
    VISUAL = auto()         # بصري       — sight / visual experience
    AUDITORY = auto()       # سمعي       — hearing / sound
    TACTILE = auto()        # لمسي       — touch / texture
    BALANCE = auto()        # توازن      — bodily balance / equilibrium
    MOTION = auto()         # حركة       — kinesthetic / movement
    FORCE = auto()          # قوة/جهد    — force / effort / resistance
    CONTAINMENT = auto()    # احتواء     — in/out container schema
    PROXIMITY = auto()      # قرب/بُعد   — near/far spatial experience
    VERTICAL_AXIS = auto()  # محور عمودي — up/down orientation
    NONE = auto()           # لا تجسيد   — not grounded in embodied experience


class SelfModelAspect(Enum):
    """جانب النموذج الذاتي — aspect of the self-model (18/20).

    Concepts involved in self-awareness, personal identity, and
    first-person perspective.
    """
    EGO = auto()                    # الأنا              — the ego / subjective centre
    SELF_IMAGE = auto()             # صورة الذات        — self-conception / self-image
    SELF_AWARENESS = auto()         # وعي الذات         — reflective self-awareness
    OTHER_DISTINCTION = auto()      # تمييز الذات من الغير — self vs. other
    PERSONAL_CONTINUITY = auto()    # الاستمرار الشخصي  — identity over time
    FIRST_PERSON = auto()           # منظور أول         — first-person perspective
    NONE = auto()                   # لا جانب ذاتي      — not self-related


class OperationalCapacity(Enum):
    """القدرة الإجرائية — operational / performative capacity (19/20).

    Some concepts not only *mean* something but also *do* something:
    they enable actions, issue commands, create obligations, etc.
    (Austin / Searle speech-act inspired).
    """
    ENABLES = auto()    # يُمكِّن   — grants ability or access
    COMMANDS = auto()   # يأمر     — directive / command
    PROMISES = auto()   # يَعِد    — commissive / promise
    PERMITS = auto()    # يأذن     — declarative permission
    RESTRICTS = auto()  # يُقيِّد  — restricts / prohibits
    ACTIVATES = auto()  # يُنشِّط  — triggers a process or state
    NONE = auto()       # لا قدرة  — no operational capacity


class ConceptRelationType(Enum):
    """نوع العلاقة بين المفاهيم — inter-concept relation type (20/20).

    The top-level relation vocabulary for building a concept network.
    These relations are used in :class:`~arabic_engine.core.types.ConceptRelation`
    to wire concept nodes together into a full knowledge graph.
    """
    IS_A = auto()           # هو نوع من       — taxonomic (hyponymy)
    PART_OF = auto()        # جزء من          — meronymy / part–whole
    CAUSES = auto()         # يُسبِّب         — causal relation
    ENABLES = auto()        # يُمكِّن         — enabling (weaker than causes)
    OPPOSES = auto()        # يُعارض          — opposition / antonymy
    PRESUPPOSES = auto()    # يفترض مسبقًا    — logical presupposition
    SYMBOLIZES = auto()     # يرمز إلى        — symbolic / iconic link
    INSTANTIATES = auto()   # يُمثِّل نموذجًا — instance-of
    REALIZES = auto()       # يُجسِّد         — realisation / implementation
    REGULATES = auto()      # يَضبط           — regulatory / governance link


# ═══════════════════════════════════════════════════════════════════════
# GROUP A — Epistemic Enums
# ═══════════════════════════════════════════════════════════════════════


class EpistemicRank(Enum):
    """الرتبة المعرفية — epistemic rank of a knowledge episode.

    Four-level ranking from certain (*qaṭʿī*) knowledge down to
    impossibility (*muḥāl*).
    """
    CERTAIN = auto()              # قطعي           — certain knowledge
    TRUE_NON_CERTAIN = auto()     # صحيح غير قطعي  — true but not certain
    PROBABILISTIC_DOUBT = auto()  # ظني مشكوك      — probabilistic / doubtful
    IMPOSSIBLE = auto()           # محال            — logically impossible


class TrustLevel(Enum):
    """مستوى الثقة — degree of trust in a source or transmission."""
    LOW = auto()        # منخفض
    MEDIUM = auto()     # متوسط
    HIGH = auto()       # عالي


class TrustBasis(Enum):
    """أساس الثقة — the ground on which trust is established."""
    EXPERTISE = auto()         # خبرة
    AUTHORITY = auto()         # حجية
    FAMILIARITY = auto()       # ألفة
    TESTIMONY_CHAIN = auto()   # سلسلة شهادة
    NONE = auto()              # لا أساس


class ValidationOutcome(Enum):
    """نتيجة التحقق — outcome of an epistemic validation step."""
    VALID = auto()                       # صالح
    PENDING = auto()                     # معلق
    INVALID = auto()                     # غير صالح
    REJECTED_METHODOLOGICALLY = auto()   # مرفوض منهجيًا


class ValidationState(Enum):
    """حالة التحقق — overall validation state."""
    VALID = auto()    # صالح
    PENDING = auto()  # معلق
    INVALID = auto()  # غير صالح


class InfoKind(Enum):
    """نوع المعلومة — kind of information carried."""
    LEXICAL = auto()       # معجمي
    SYNTACTIC = auto()     # نحوي
    SEMANTIC = auto()      # دلالي
    PRAGMATIC = auto()     # تداولي
    CONTEXTUAL = auto()    # سياقي
    INFERENTIAL = auto()   # استدلالي


class DecisionCode(Enum):
    """رمز القرار — machine-readable codes for epistemic gap decisions."""
    EPI001_MISSING_REALITY = auto()
    EPI002_MISSING_SENSE = auto()
    EPI003_MISSING_PRIOR_INFO = auto()
    EPI004_OPINION_CONTAMINATION = auto()
    EPI005_MISSING_LINKING = auto()
    EPI006_MISSING_JUDGEMENT = auto()
    EPI007_MISSING_METHOD = auto()
    EPI008_METHOD_FIT_FAILURE = auto()
    EPI009_CARRIER_INVALID = auto()
    EPI010_MISSING_PROOF_PATH = auto()
    EPI011_MISSING_CONFLICT_RULE = auto()
    EPI012_CARRIER_BOTH_MISSING = auto()
    EPI013_PROOF_METHOD_MISMATCH = auto()
    EPI014_UTTERANCE_CONCEPT_CONFLICT = auto()


class InsertionPolicy(Enum):
    """سياسة الإدراج — storage policy for a validated episode."""
    FOUNDATIONAL = auto()  # تأسيسي
    ADMISSIBLE = auto()    # مقبول
    GUARDED = auto()       # محروس
    BLOCKED = auto()       # محظور


# ═══════════════════════════════════════════════════════════════════════
# GROUP B — Cognitive / Conceptual Enums
# ═══════════════════════════════════════════════════════════════════════


class JudgementType(Enum):
    """نوع الحكم — the kind of epistemic judgement."""
    EXISTENCE = auto()              # وجودي
    ESSENCE = auto()                # ماهوي
    ATTRIBUTE = auto()              # وصفي
    RELATION = auto()               # علائقي
    INTERPRETIVE = auto()           # تفسيري
    FORMAL_CONTRADICTION = auto()   # تناقض صوري
    NORMATIVE = auto()              # معياري
    PURE_LINGUISTIC = auto()        # لغوي صرف
    METAPHYSICAL = auto()           # ما وراء الطبيعة
    CAUSAL = auto()                 # سببي
    FORMAL = auto()                 # صوري


class LinkKind(Enum):
    """نوع الربط — how a knowledge link connects nodes."""
    TEXTUAL_INFERENCE = auto()  # استدلال نصي
    CAUSAL = auto()             # سببي
    CONTEXTUAL = auto()         # سياقي
    ANALOGICAL = auto()         # قياسي
    REFERENTIAL = auto()        # إحالي


class DalaalaKind(Enum):
    """نوع الدلالة — fine-grained signification kind."""
    MUTABAQA = auto()    # مطابقة — exact denotation
    TADHAMMUN = auto()   # تضمن  — inclusion
    TADAMMUN = TADHAMMUN  # backward-compat alias for legacy spelling
    ILTIZAM = auto()     # التزام — necessary concomitant
    ISHARA = auto()      # إشارة — allusion / indication


class SenseModality(Enum):
    """الحاسة — sense modality for perception traces."""
    VISION = auto()    # بصر
    HEARING = auto()   # سمع
    TOUCH = auto()     # لمس
    SMELL = auto()     # شم
    TASTE = auto()     # ذوق
    INTUITION = auto() # حدس
    # backward-compat aliases
    VISUAL = VISION


class RealityKind(Enum):
    """نوع الواقع — ontological kind of reality anchor."""
    TEXT_OBJECT = auto()      # كائن نصي
    EVENT = auto()            # حدث
    MATERIAL = auto()         # مادي
    ABSTRACT = auto()         # مجرد
    SOCIAL = auto()           # اجتماعي
    HISTORICAL = auto()       # تاريخي
    PHYSICAL_OBJECT = auto()  # كائن مادي


class RationalSelfKind(Enum):
    """نوع الذات العاقلة — kind of rational self."""
    INDIVIDUAL = auto()       # فردي
    COLLECTIVE = auto()       # جماعي
    INSTITUTIONAL = auto()    # مؤسسي
    MODELED_AGENT = auto()    # وكيل مُنمذج


class TraceMode(Enum):
    """نمط التتبع — how a sense trace was acquired."""
    DIRECT = auto()              # مباشر
    MEDIATED = auto()            # بوساطة
    # backward-compat alias
    DIRECT_PERCEPTION = DIRECT


class TraceQuality(Enum):
    """جودة التتبع — quality assessment of a trace."""
    STRONG = auto()     # قوي
    MODERATE = auto()   # متوسط
    WEAK = auto()       # ضعيف


# ═══════════════════════════════════════════════════════════════════════
# GROUP C — Exchange / Discourse Enums
# ═══════════════════════════════════════════════════════════════════════


class ExchangeType(Enum):
    """نوع التبادل — kind of discourse exchange."""
    REPORT = auto()       # تقرير
    TEACHING = auto()     # تعليم
    QUESTION = auto()     # سؤال
    ANSWER = auto()       # جواب
    COMMAND = auto()      # أمر
    WARNING = auto()      # تحذير
    PERSUASION = auto()   # إقناع
    NEGOTIATION = auto()  # تفاوض
    TESTIMONY = auto()    # شهادة
    EXPLANATION = auto()  # شرح


class ExchangeStatus(Enum):
    """حالة التبادل — status of a discourse exchange."""
    DRAFTED = auto()       # مسودة
    TRANSMITTED = auto()   # مُرسَل
    RECEIVED = auto()      # مستلم
    INTERPRETED = auto()   # مُفسَّر
    ACCEPTED = auto()      # مقبول
    REJECTED = auto()      # مرفوض
    SUSPENDED = auto()     # معلق


class ExchangePurposeType(Enum):
    """نوع غرض التبادل — purpose classification of an exchange."""
    INFORM = auto()               # إعلام
    TEACH = auto()                # تعليم
    VERIFY = auto()               # تحقق
    GUIDE = auto()                # إرشاد
    BIND = auto()                 # إلزام
    PERSUADE = auto()             # إقناع
    WARN = auto()                 # تحذير
    REQUEST = auto()              # طلب
    TEST = auto()                 # اختبار
    PRESERVE_KNOWLEDGE = auto()   # حفظ المعرفة


class ExchangeStyleType(Enum):
    """نوع أسلوب التبادل — style classification of an exchange."""
    KHABARI = auto()         # خبري
    INSHAI = auto()          # إنشائي
    EXPLANATORY = auto()     # توضيحي
    ARGUMENTATIVE = auto()   # حجاجي
    DIRECTIVE = auto()       # توجيهي
    INTERROGATIVE = auto()   # استفهامي
    PEDAGOGICAL = auto()     # تعليمي
    TESTIMONIAL = auto()     # شهادي


class ReceptionMode(Enum):
    """نمط الاستقبال — how the message was received."""
    HEARD = auto()       # مسموع
    READ = auto()        # مقروء
    OBSERVED = auto()    # ملاحظ
    INFERRED = auto()    # مستنبط
    RECALLED = auto()    # مُستدعى


class ReceptionStateType(Enum):
    """نوع حالة الاستقبال — cognitive state after reception."""
    RECEIVED = auto()              # مُستلم
    UNDERSTOOD = auto()            # مفهوم
    MISUNDERSTOOD = auto()         # مُساء فهمه
    ACCEPTED = auto()              # مقبول
    REJECTED = auto()              # مرفوض
    SUSPENDED = auto()             # معلق
    PARTIALLY_UNDERSTOOD = auto()  # مفهوم جزئيًا


class ReceiverRoleType(Enum):
    """نوع دور المتلقي — receiver's role in discourse."""
    LISTENER = auto()     # مستمع
    LEARNER = auto()      # متعلم
    EXAMINER = auto()     # فاحص
    ADDRESSEE = auto()    # مخاطب
    RESPONDENT = auto()   # مجيب
    EVALUATOR = auto()    # مقيّم


class ReceiverState(Enum):
    """حالة المتلقي — receiver's cognitive readiness."""
    OPEN = auto()        # منفتح
    RESISTANT = auto()   # مقاوم
    BIASED = auto()      # منحاز
    UNCERTAIN = auto()   # غير متأكد
    ATTENTIVE = auto()   # يقظ


class ReceiverExpectedAction(Enum):
    """الإجراء المتوقع من المتلقي — expected action from receiver."""
    UNDERSTAND = auto()   # فهم
    VERIFY = auto()       # تحقق
    ACT = auto()          # فعل
    ANSWER = auto()       # إجابة
    PRESERVE = auto()     # حفظ
    RELAY = auto()        # نقل


class PurposeType(Enum):
    """نوع الغرض — communicative purpose of an exchange."""
    INFORM = auto()          # إعلام
    INSTRUCT = auto()        # تعليم
    PERSUADE = auto()        # إقناع
    TEST = auto()            # اختبار
    QUERY = auto()           # استفسار
    PRESERVE = auto()        # حفظ
    REFUTE = auto()          # دحض
    WARN = auto()            # تحذير
    REQUEST_ACTION = auto()  # طلب إجراء
    CLARIFY = auto()         # توضيح


class SenderRoleType(Enum):
    """نوع دور المرسل — sender's role in discourse."""
    SOURCE = auto()       # مصدر
    EXPLAINER = auto()    # شارح
    WITNESS = auto()      # شاهد
    TEACHER = auto()      # معلم
    COMMANDER = auto()    # آمر
    QUESTIONER = auto()   # سائل
    INTERPRETER = auto()  # مفسر


class UtteranceMode(Enum):
    """نمط المنطوق — mode of the utterance."""
    STATEMENT = auto()       # إخبار
    QUESTION = auto()        # سؤال
    COMMAND = auto()         # أمر
    REPORT = auto()          # تقرير
    EXPLANATION = auto()     # شرح
    DIALOGUE_TURN = auto()   # دور حواري


class StyleKind(Enum):
    """نوع الأسلوب — rhetorical style of discourse."""
    KHABAR = auto()        # خبر
    INSHA = auto()         # إنشاء
    QUESTION = auto()      # سؤال
    ANSWER = auto()        # جواب
    COMMAND = auto()       # أمر
    PROHIBITION = auto()   # نهي
    EXPLANATION = auto()   # شرح
    ARGUMENT = auto()      # حجاج
    TESTIMONY = auto()     # شهادة
    SYMBOLIC = auto()      # رمزي


# ═══════════════════════════════════════════════════════════════════════
# GROUP D — Structural / Constraint Enums
# ═══════════════════════════════════════════════════════════════════════


class MethodFamily(Enum):
    """عائلة المنهج — family of epistemic method."""
    RATIONAL = auto()       # عقلي
    SCIENTIFIC = auto()     # علمي
    LINGUISTIC = auto()     # لغوي
    MATHEMATICAL = auto()   # رياضي
    PHYSICAL = auto()       # فيزيائي
    TRADITIONAL = auto()    # نقلي


class PathKind(Enum):
    """نوع المسار — kind of proof / reasoning path."""
    AQLI = auto()        # عقلي       — rational path
    LINGUISTIC = auto()  # لغوي       — linguistic path
    HISSI = auto()       # حسي        — sensory path
    FORMAL = auto()      # صوري       — formal-logical path


class ProofPathKind(Enum):
    """نوع مسار البرهان — specific kind of proof path."""
    DIRECT_PROOF = auto()       # برهان مباشر
    INDIRECT_PROOF = auto()     # برهان غير مباشر
    BY_CONTRADICTION = auto()   # برهان خلف
    BY_INDUCTION = auto()       # استقراء


class ExplicitnessLevel(Enum):
    """مستوى الصراحة — how explicitly a concept is conveyed."""
    DIRECT = auto()        # مباشر
    SEMI_DIRECT = auto()   # شبه مباشر
    IMPLICIT = auto()      # ضمني


class OntologicalConstraintType(Enum):
    """نوع القيد الأنطولوجي — kinds of ontological constraint."""
    STRUCTURAL = auto()              # بنيوي
    LEXICAL_CONSTRAINT = auto()      # قيد معجمي
    CONTEXTUAL_CONSTRAINT = auto()   # قيد سياقي
    INTERPRETIVE_CONSTRAINT = auto() # قيد تفسيري
    RHETORICAL_CONSTRAINT = auto()   # قيد بلاغي
    REFERENTIAL_CONSTRAINT = auto()  # قيد إحالي
    LOGICAL_CONSTRAINT = auto()      # قيد منطقي
    TEMPORAL_CONSTRAINT = auto()     # قيد زمني
    SPATIAL_CONSTRAINT = auto()      # قيد مكاني
    MODAL_CONSTRAINT = auto()        # قيد جهوي
    PRAGMATIC_CONSTRAINT = auto()    # قيد تداولي
    DEONTIC_CONSTRAINT = auto()      # قيد إلزامي
    CAUSAL_CONSTRAINT = auto()       # قيد سببي


class UtteranceToConceptConstraint(Enum):
    """قيد المنطوق→المفهوم — constraints on the utterance-to-concept mapping."""
    SURFACE_VALIDITY = auto()            # صلاحية سطحية
    LEXICAL_ACCESS = auto()              # نفاذ معجمي
    CONTEXT_RESOLUTION = auto()          # حل سياقي
    CONCEPT_SELECTION = auto()           # اختيار مفهوم
    FIGURATIVE_DISAMBIGUATION = auto()   # إزالة لبس مجازي
    REFERENTIAL_RESOLUTION = auto()      # حل إحالي
    LOGICAL_COHERENCE = auto()           # اتساق منطقي


class AuthorityLevel(Enum):
    """مستوى الحجية — authority level of a source or argument."""
    HIGH = auto()     # عالي
    MEDIUM = auto()   # متوسط
    LOW = auto()      # منخفض


# ═══════════════════════════════════════════════════════════════════════
# GROUP E — Carrier / Representation Enums
# ═══════════════════════════════════════════════════════════════════════


class CarrierType(Enum):
    """نوع الحامل — what kind of carrier is present."""
    UTTERANCE = auto()  # منطوق
    CONCEPT = auto()    # مفهوم
    BOTH = auto()       # كلاهما


class CarrierClass(Enum):
    """صنف الحامل — classification of carrier."""
    UTTERANCE = auto()  # منطوق
    CONCEPT = auto()    # مفهوم
    BOTH = auto()       # كلاهما


class SignifierClass(Enum):
    """صنف الدال — classification of the signifier."""
    LEXICAL = auto()       # معجمي
    SYNTACTIC = auto()     # نحوي
    UTTERED_FORM = auto()  # صيغة ملفوظة
    MORPHOLOGICAL = auto() # صرفي
    PHONOLOGICAL = auto()  # صوتي
    RHETORICAL = auto()    # بلاغي
    PRAGMATIC = auto()     # تداولي
    CONTEXTUAL = auto()    # سياقي


class SignifiedClass(Enum):
    """صنف المدلول — classification of the signified."""
    CONCEPTUAL = auto()          # مفاهيمي
    RELATIONAL = auto()          # علائقي
    NORMATIVE = auto()           # معياري
    REFERENTIAL = auto()         # إحالي
    ONTOLOGICAL = auto()         # أنطولوجي
    META_CONCEPTUAL = auto()     # فوق مفاهيمي
    FUNCTIONAL = auto()          # وظيفي
    EPISTEMIC = auto()           # معرفي
    MODAL = auto()               # جهوي
    EVALUATIVE = auto()          # تقييمي
    TEMPORAL = auto()            # زماني
    SPATIAL = auto()             # مكاني
    CAUSAL = auto()              # سببي
    INSTITUTIONAL = auto()       # مؤسسي
    PERFORMATIVE = auto()        # إنجازي
    AFFECTIVE = auto()           # عاطفي
    CULTURAL = auto()            # ثقافي
    DEONTIC = auto()             # إلزامي
    EXPERIENTIAL = auto()        # خبراتي
    CLASSIFICATORY = auto()      # تصنيفي
    COMPOSITIONAL = auto()       # تركيبي
    METAPHORICAL = auto()        # مجازي


class ConceptualSignifiedClass(Enum):
    """صنف المدلول المفاهيمي — sub-classification of conceptual signified."""
    ENTITY_CONCEPT = auto()    # مفهوم ذات
    EVENT_CONCEPT = auto()     # مفهوم حدث
    PROPERTY_CONCEPT = auto()  # مفهوم صفة
    RELATION_CONCEPT = auto()  # مفهوم علاقة
    META_CONCEPT = auto()      # مفهوم فوقي
    STATE_CONCEPT = auto()     # مفهوم حالة
    PROCESS_CONCEPT = auto()   # مفهوم عملية
    ABSTRACT_CONCEPT = auto()  # مفهوم مجرد


class UtteredFormClass(Enum):
    """صنف الصيغة الملفوظة — classification of the uttered form."""
    WORD_UTTERANCE = auto()       # لفظ مفرد
    MARKED_UTTERANCE = auto()     # لفظ معلّم
    PHRASE_UTTERANCE = auto()     # عبارة
    SENTENCE_UTTERANCE = auto()   # جملة
    COMPOUND_UTTERANCE = auto()   # مركب


class CouplingRelationType(Enum):
    """نوع علاقة الاقتران — how signifier is coupled to signified."""
    DIRECT = auto()                # مباشر
    INFERENTIAL = auto()           # استدلالي
    COMPOSITIONAL = auto()         # تركيبي
    HIERARCHICAL = auto()          # هرمي
    REFERENTIAL_COUPLING = auto()  # اقتران إحالي
    FIGURATIVE = auto()            # مجازي
    METONYMIC = auto()             # كنائي
    CONTEXTUAL_COUPLING = auto()   # اقتران سياقي
    PRAGMATIC_COUPLING = auto()    # اقتران تداولي
    CONVENTIONAL = auto()          # عرفي


# ═══════════════════════════════════════════════════════════════════════
# GROUP F — Error / Gap / Validation Enums
# ═══════════════════════════════════════════════════════════════════════


class GapSeverity(Enum):
    """شدة الفجوة — how severe an epistemic gap is.

    Canonical members: FATAL, CRITICAL, MODERATE, MINOR.
    Legacy aliases HIGH/MEDIUM/LOW are kept for backward compatibility
    and should be considered deprecated in new code.
    """
    FATAL = auto()     # قاتلة
    CRITICAL = auto()  # حرجة
    MODERATE = auto()  # معتدلة
    MINOR = auto()     # طفيفة
    # backward-compat aliases (deprecated — prefer canonical names)
    HIGH = CRITICAL
    MEDIUM = MODERATE
    LOW = MINOR


class DiscourseGapType(Enum):
    """نوع فجوة الخطاب — specific kind of discourse gap."""
    MISSING_SENDER = auto()
    SENDER_PURPOSE_MISMATCH = auto()
    MISSING_RECEIVER = auto()
    MISSING_PURPOSE = auto()
    INVALID_STYLE_PURPOSE_FIT = auto()
    MISSING_STYLE = auto()
    MISSING_CARRIER = auto()
    INVALID_CARRIER = auto()
    MISSING_RECEPTION = auto()
    MISSING_RECEPTION_STATE = auto()
    RECEPTION_INCONSISTENCY = auto()
    MISSING_TRUST_PROFILE = auto()
    MISSING_TRANSFERRED_KNOWLEDGE = auto()
    INVALID_TRANSFERRED_KNOWLEDGE = auto()


class DiscourseValidationOutcome(Enum):
    """نتيجة التحقق من الخطاب — outcome of discourse validation."""
    VALID = auto()       # صالح
    INCOMPLETE = auto()  # ناقص
    INVALID = auto()     # غير صالح


class InterpretiveOutcomeType(Enum):
    """نوع النتيجة التفسيرية — outcome of interpretive analysis."""
    ALIGNED = auto()      # متوافق
    NARROWED = auto()     # مضيَّق
    EXPANDED = auto()     # موسَّع
    DISTORTED = auto()    # مشوّه
    CONFLICTING = auto()  # متعارض
    UNRESOLVED = auto()   # غير محسوم


class ContaminationLevel(Enum):
    """مستوى التلوث — degree of opinion contamination."""
    NONE = auto()    # لا تلوث
    LOW = auto()     # منخفض
    MEDIUM = auto()  # متوسط
    HIGH = auto()    # مرتفع


# ═══════════════════════════════════════════════════════════════════════
# Fractal Kernel — Layered Hypothesis Graph Architecture
# ═══════════════════════════════════════════════════════════════════════


class HypothesisStatus(Enum):
    """حالة الفرضية — status of a hypothesis node in the graph."""
    ACTIVE = auto()       # نشط — still under consideration
    PRUNED = auto()       # مقطوع — removed by constraint
    STABILIZED = auto()   # مستقر — accepted as decision
    SUSPENDED = auto()    # معلق — deferred pending more evidence
    REVISED = auto()      # مُعدَّل — modified after feedback


class ConstraintStrength(Enum):
    """قوة القيد — how strongly a constraint restricts candidates."""
    ABSOLUTE = auto()     # مطلق — violation is fatal
    STRONG = auto()       # قوي — almost always enforced
    MODERATE = auto()     # متوسط — enforced unless overridden
    WEAK = auto()         # ضعيف — advisory / preference
    TENTATIVE = auto()    # تجريبي — experimental, may be dropped


class ConflictState(Enum):
    """حالة التعارض — degree of conflict between hypotheses."""
    NONE = auto()         # لا تعارض
    SOFT = auto()         # تعارض خفيف — can coexist with scoring penalty
    HARD = auto()         # تعارض حاد — only one can survive
    UNRESOLVED = auto()   # غير محسوم — awaiting more evidence


class RevisionType(Enum):
    """نوع المراجعة — reason for a revision request."""
    CONFLICT_RESOLUTION = auto()   # حل تعارض
    AMBIGUITY_RESOLUTION = auto()  # حل التباس
    FEEDBACK_UPDATE = auto()       # تحديث من طبقة أعلى
    CONFIDENCE_SHIFT = auto()      # تغير في الثقة
    EXTERNAL_EVIDENCE = auto()     # دليل خارجي جديد


class SignalType(Enum):
    """نوع الإشارة — classification of a Unicode atom."""
    BASE_LETTER = auto()    # حرف أساسي
    DIACRITIC = auto()      # حركة / علامة
    PUNCTUATION = auto()    # ترقيم
    WHITESPACE = auto()     # مسافة
    NUMERAL = auto()        # رقم
    UNKNOWN = auto()        # غير معروف


class ActivationStage(Enum):
    """مرحلة التفعيل — which processing stage a hypothesis belongs to."""
    SIGNAL = auto()         # إشارة
    MORPHOLOGY = auto()     # صرف
    CONCEPT = auto()        # مفهوم
    AXIS = auto()           # محور
    RELATION = auto()       # علاقة
    ROLE = auto()           # دور
    FACTOR = auto()         # عامل
    CASE = auto()           # حالة إعرابية
    JUDGEMENT = auto()      # حكم


# ══════════════════════════════════════════════════════════════════════
# Strict 7-Layer Analysis System  —  النموذج الطبقي الصارم
# ══════════════════════════════════════════════════════════════════════


class StrictLayerID(Enum):
    """معرّف الطبقة الصارمة — strict layer identifier (Layer 0→6)."""

    MENTAL_FOUNDATION = auto()   # الأساس العقلي
    GENERATIVE = auto()          # القوام التوليدي
    AUDITORY_MINIMUM = auto()    # القوام السمعي الأدنى
    STRUCTURAL = auto()          # القوام البنيوي
    TRANSFORMATION = auto()      # التحول
    HIGHER_FUNCTION = auto()     # الوظيفة العليا والحكم
    PROGRAMMATIC = auto()        # التمثيل البرمجي


class MentalPrimitive(Enum):
    """أوليات الطبقة العقلية المؤسسة — Layer 0 mental primitives."""

    IDENTITY = auto()            # الهوية
    DIFFERENCE = auto()          # المغايرة
    RANK = auto()                # الرتبة
    CONSTITUTIVENESS = auto()    # المقومية
    DEPENDENCY = auto()          # التبعية
    STABILITY = auto()           # الثبات
    TRANSFORMATION = auto()      # التحول
    CAUSALITY = auto()           # العلية
    REALITY_MATCH = auto()       # مطابقة الواقع


class MentalEdgeType(Enum):
    """حواف الطبقة العقلية — Layer 0 edge types."""

    DISTINGUISHED_BY = auto()    # يتميز بـ
    ORDERED_AS = auto()          # يرتب كـ
    EVALUATED_FOR = auto()       # يُقيَّم لـ
    CONTRASTS_WITH = auto()      # يتقابل مع
    MEASURED_AGAINST = auto()    # يُقاس بـ
    EXPLAINS = auto()            # يفسّر
    VALIDATES = auto()           # يُصادِق


class GenerativeNode(Enum):
    """عقد القوام التوليدي — Layer 1 generative phonetic nodes."""

    ENERGY_SOURCE = auto()       # مصدر الطاقة
    VOCAL_FOLD_STATE = auto()    # حالة الأحبال الصوتية
    AIRFLOW_PATH = auto()        # مسار الهواء
    ARTICULATION_PLACE = auto()  # موضع التحقق
    ARTICULATION_MODE = auto()   # نوع الاعتراض
    CLOSURE_DEGREE = auto()      # درجة الانغلاق
    RELEASE_SHAPE = auto()       # هيئة الانفراج
    RESONANCE_PROFILE = auto()   # الرنين


class AuditoryNode(Enum):
    """عقد القوام السمعي الأدنى — Layer 2 auditory minimum nodes."""

    AUDITORY_PRESENCE = auto()   # الحضور السمعي
    BOUNDARY = auto()            # الحد
    EXTENSION = auto()           # الامتداد
    PHASE = auto()               # الطور
    ORDERLINESS = auto()         # الانتظام
    COHESION = auto()            # التماسك
    UNITY = auto()               # الوحدة


class StructuralNode(Enum):
    """عقد القوام البنيوي — Layer 3 structural nodes."""

    SYLLABIC_RANK = auto()       # الرتبة المقطعية
    ROOT_RANK = auto()           # الرتبة الجذرية
    CONSTITUTIVE_ROLE = auto()   # الدور المقوم
    DEPENDENT_ROLE = auto()      # الدور التابع
    ATTACHMENT_CAPACITY = auto()  # قابلية الإلصاق
    AUGMENTATION_CAPACITY = auto()  # قابلية الزيادة
    ROOT_POSITION_FA = auto()    # فاء
    ROOT_POSITION_AYN = auto()   # عين
    ROOT_POSITION_LAM = auto()   # لام


class TransformationNode(Enum):
    """عقد طبقة التحول — Layer 4 transformation nodes."""

    STABILITY_ACROSS_INFLECTION = auto()  # الثبات عبر التصريف
    RECOVERABILITY = auto()      # إمكان الرد إلى الأصل
    SUBSTITUTION = auto()        # الإبدال
    DELETION = auto()            # الحذف
    ILLAL = auto()               # الإعلال
    IDGHAM = auto()              # الإدغام
    SURFACE_ABSENCE = auto()     # الغياب السطحي
    UNDERLYING_PRESENCE = auto()  # الحضور العميق


class JudgmentCategory(Enum):
    """أحكام الوظيفة العليا — Layer 5 judgment categories."""

    ORIGINAL = auto()            # أصل
    AUGMENTED = auto()           # زائد
    SUBSTITUTED = auto()         # مبدل
    DELETED = auto()             # محذوف
    WEAKENED_TRANSFORMED = auto()  # معلول
    ASSIMILATED = auto()         # مدغم
    ATTACHED_MARKER = auto()     # عنصر إلصاق
    DEICTIC_BUILDER = auto()     # باني مبنيات
    RELATIONAL_CONNECTOR = auto()  # أداة ربط


class RepresentationNode(Enum):
    """عقد التمثيل البرمجي — Layer 6 representation nodes."""

    PHONEME_ENTITY = auto()      # كيان صوتي
    FEATURE_VECTOR = auto()      # متجه الخصائص
    SYLLABLE_NODE = auto()       # عقدة مقطعية
    ROOT_NODE = auto()           # عقدة جذرية
    TRANSFORMATION_RULE = auto()  # قاعدة تحول
    JUDGMENT_ENGINE = auto()     # محرك الحكم
    REALITY_VALIDATION = auto()  # تحقق الواقع
    LEXICAL_GRAPH = auto()       # رسم معجمي
    DEICTIC_GRAPH = auto()       # رسم إشاري
    RELATIONAL_GRAPH = auto()    # رسم علائقي


class LayerEdgeType(Enum):
    """أنواع الحواف بين طبقات النموذج الصارم — inter-layer edge types."""

    DRIVES = auto()              # يحرّك
    CONDITIONS = auto()          # يشترط
    PASSES_THROUGH = auto()      # يمر عبر
    REALIZED_AS = auto()         # يتحقق كـ
    QUANTIFIED_BY = auto()       # يُكَمَّم بـ
    ENDS_IN = auto()             # ينتهي بـ
    CONTRIBUTES_TO = auto()      # يسهم في
    BOUNDED_AS = auto()          # يُحَدّ بـ
    OCCUPIES = auto()            # يشغل
    DIVIDES_INTO = auto()        # ينقسم إلى
    ORGANIZED_AS = auto()        # ينتظم كـ
    STABILIZES = auto()          # يثبّت
    YIELDS = auto()              # ينتج
    PLACED_IN = auto()           # يوضع في
    MAPPED_TO = auto()           # يقابَل بـ
    MAY_BE = auto()              # يمكن أن يكون
    SUPPORTS = auto()            # يدعم
    INSTANTIATES = auto()        # يجسّد
    INFERS = auto()              # يستدل
    REALIZES_AS = auto()         # يتحقق كـ
    IMPLIES = auto()             # يستلزم
    HAS_FEATURES = auto()        # له خصائص
    BELONGS_TO = auto()          # ينتمي إلى
    MAPS_TO = auto()             # يقابل
    GOVERNED_BY = auto()         # يحكمه
    FEEDS = auto()               # يغذي
    CHECKED_BY = auto()          # يتحقق منه
    STORES_IF_VALID = auto()     # يخزّن إذا صحّ
    ROUTES_TO = auto()           # يوجّه إلى


class TransitionGateStatus(Enum):
    """حالة بوابة الانتقال — transition gate status between layers."""

    PASSED = auto()              # اجتاز
    BLOCKED = auto()             # مُنِعَ
    INSUFFICIENT_DATA = auto()   # بيانات غير كافية
