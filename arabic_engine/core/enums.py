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



# ── Dalāla kind ──────────────────────────────────────────────────────


class DalaalaKind(Enum):
    """نوع الدلالة — coarse-grained/classical signification categories.

    This enum intentionally overlaps with :class:`DalalaType`, but serves a
    different purpose: ``DalaalaKind`` captures the broad semantic family of
    signification in the classical sense, while ``DalalaType`` is the more
    specific operational/relational taxonomy used to model concrete links
    such as predication, restriction, genitive construction, and reference.
    Keep both enums so callers can choose between high-level classification
    and fine-grained relation typing without conflating the two.
    """

    MUTABAQA = auto()    # مطابقة  — full correspondence / exact match
    TADHAMMUN = auto()   # تضمن    — containment / partial inclusion
    TADAMMUN = TADHAMMUN  # Backward-compatible alias matching DalalaType
    ILTIZAM = auto()     # التزام  — implication / connotation
    ISHARA = auto()      # إشارة   — indication / indexical signification


# ── Authority level ──────────────────────────────────────────────────


class AuthorityLevel(Enum):
    """مستوى السلطة — epistemic authority / weight of a discourse source."""

    LOW = auto()        # منخفضة  — low authority
    MEDIUM = auto()     # معتدلة  — moderate authority
    HIGH = auto()       # عالية   — high authority


# ── Carrier class ────────────────────────────────────────────────────


class CarrierClass(Enum):
    """صنف الحامل — the class of the epistemic carrier (utterance/concept/both)."""

    UTTERANCE = auto()   # ملفوظ    — utterance-only carrier
    CONCEPT = auto()     # مفهوم    — concept-only carrier
    BOTH = auto()        # كلاهما   — both utterance and concept


# ── Carrier type ─────────────────────────────────────────────────────


class CarrierType(Enum):
    """نوع الحامل — the linguistic carrier type for an epistemic concept."""

    UTTERANCE = auto()   # ملفوظ    — utterance carrier
    CONCEPT = auto()     # مفهوم    — concept carrier
    BOTH = auto()        # كلاهما   — both carriers


# ── Conceptual signified class ───────────────────────────────────────


class ConceptualSignifiedClass(Enum):
    """صنف المدلول المفاهيمي — the ontological class of a conceptual signified."""

    ENTITY_CONCEPT = auto()       # مفهوم الذات     — entity concept
    EVENT_CONCEPT = auto()        # مفهوم الحدث     — event concept
    PROPERTY_CONCEPT = auto()     # مفهوم الخاصية   — property concept
    RELATIONAL_CONCEPT = auto()   # مفهوم العلاقة   — relational concept
    ABSTRACT_CONCEPT = auto()     # مفهوم مجرد      — abstract concept
    NORMATIVE_CONCEPT = auto()    # مفهوم معياري    — normative concept
    MODAL_CONCEPT = auto()        # مفهوم جهوي      — modal concept
    META_CONCEPT = auto()         # ميتا-مفهوم      — meta / higher-order concept


# ── Contamination level ──────────────────────────────────────────────


class ContaminationLevel(Enum):
    """مستوى التلوث — the degree of opinion contamination in a knowledge episode."""

    NONE = auto()    # معدوم   — no contamination
    LOW = auto()     # منخفض   — low contamination
    MEDIUM = auto()  # متوسط   — medium contamination
    HIGH = auto()    # عالٍ    — high contamination (opinion-driven)


# ── Coupling relation type ───────────────────────────────────────────


class CouplingRelationType(Enum):
    """نوع علاقة الاقتران — the type of coupling between a signifier and a signified."""

    DIRECT = auto()                # مباشر           — direct / literal coupling
    INFERENTIAL = auto()           # استنتاجي        — inferential coupling
    COMPOSITIONAL = auto()         # تركيبي          — compositional coupling
    HIERARCHICAL = auto()          # هرمي            — hierarchical coupling
    REFERENTIAL_COUPLING = auto()  # إحالي           — referential coupling
    FIGURATIVE = auto()            # مجازي           — figurative / metaphorical coupling
    METONYMIC = auto()             # مجاز مرسل       — metonymic coupling
    ANALOGICAL = auto()            # قياسي           — analogical coupling
    CAUSAL = auto()                # سببي            — causal coupling
    PRESUPPOSITIONAL = auto()      # افتراضي مسبق    — presuppositional coupling


# ── Decision code ────────────────────────────────────────────────────


class DecisionCode(Enum):
    """رمز القرار — a specific epistemic decision / failure code."""

    EPI001_MISSING_REALITY = auto()            # غياب المرساة الواقعية
    EPI002_MISSING_SENSE = auto()              # غياب أثر الحاسة
    EPI003_MISSING_PRIOR_INFO = auto()         # غياب المعلومة السابقة
    EPI004_OPINION_CONTAMINATION = auto()      # تلوث بالرأي
    EPI005_MISSING_LINKING = auto()            # غياب أثر الربط
    EPI006_MISSING_JUDGEMENT = auto()          # غياب الحكم
    EPI007_MISSING_METHOD = auto()             # غياب المنهج
    EPI008_METHOD_FIT_FAILURE = auto()         # عدم ملاءمة المنهج
    EPI009_CARRIER_INVALID = auto()            # حامل غير صالح
    EPI010_MISSING_PROOF_PATH = auto()         # غياب مسار الإثبات
    EPI011_MISSING_CONFLICT_RULE = auto()      # غياب قاعدة التعارض
    EPI012_CARRIER_BOTH_MISSING = auto()       # كلا الحاملين مفقود
    EPI013_PROOF_METHOD_MISMATCH = auto()      # تعارض مسار الإثبات مع المنهج
    EPI014_UTTERANCE_CONCEPT_CONFLICT = auto() # تعارض الملفوظ مع المفهوم


# ── Discourse gap type ───────────────────────────────────────────────


class DiscourseGapType(Enum):
    """نوع ثغرة الخطاب — the type of a gap detected in a discourse exchange."""

    MISSING_SENDER = auto()                    # غياب المرسِل
    MISSING_RECEIVER = auto()                  # غياب المتلقي
    MISSING_PURPOSE = auto()                   # غياب الغرض
    MISSING_STYLE = auto()                     # غياب الأسلوب
    INVALID_STYLE_PURPOSE_FIT = auto()         # عدم تناسب الأسلوب والغرض
    MISSING_CARRIER = auto()                   # غياب الحامل
    INVALID_CARRIER = auto()                   # حامل غير صالح
    MISSING_RECEPTION = auto()                 # غياب الاستقبال
    MISSING_RECEPTION_STATE = auto()           # غياب حالة الاستقبال
    MISSING_TRANSFERRED_KNOWLEDGE = auto()     # غياب المعرفة المنقولة
    INVALID_TRANSFERRED_KNOWLEDGE = auto()     # معرفة منقولة غير صالحة
    MISSING_TRUST_PROFILE = auto()             # غياب ملف الثقة
    RECEPTION_INCONSISTENCY = auto()           # تناقض الاستقبال
    SENDER_PURPOSE_MISMATCH = auto()           # تعارض دور المرسِل مع الغرض


# ── Discourse validation outcome ─────────────────────────────────────


class DiscourseValidationOutcome(Enum):
    """نتيجة التحقق من الخطاب — the outcome of a discourse exchange validation."""

    VALID = auto()       # صالح    — exchange is valid
    INVALID = auto()     # غير صالح — exchange is invalid
    INCOMPLETE = auto()  # ناقص    — exchange is incomplete


# ── Epistemic rank ───────────────────────────────────────────────────


class EpistemicRank(Enum):
    """الرتبة المعرفية — the epistemic rank assigned to a knowledge episode."""

    CERTAIN = auto()              # يقيني          — certain / definite knowledge
    TRUE_NON_CERTAIN = auto()     # صحيح غير يقيني — true but non-certain
    PROBABILISTIC_DOUBT = auto()  # ظني             — probabilistic / doubtful
    IMPOSSIBLE = auto()           # مستحيل          — impossible / contradictory


# ── Exchange purpose type ────────────────────────────────────────────


class ExchangePurposeType(Enum):
    """نوع غرض التبادل — the purpose type of a discourse exchange."""

    INFORM = auto()              # إعلام              — conveying information
    TEACH = auto()               # تعليم              — teaching / instruction
    VERIFY = auto()              # تحقق               — verification
    GUIDE = auto()               # إرشاد              — guidance
    BIND = auto()                # إلزام              — binding obligation
    PERSUADE = auto()            # إقناع              — persuasion
    WARN = auto()                # تحذير              — warning
    REQUEST = auto()             # طلب                — request
    TEST = auto()                # اختبار             — testing / examination
    PRESERVE_KNOWLEDGE = auto()  # حفظ المعرفة        — knowledge preservation


# ── Exchange status ──────────────────────────────────────────────────


class ExchangeStatus(Enum):
    """حالة التبادل — the current status of a discourse exchange."""

    DRAFTED = auto()       # مسودة     — drafted, not yet sent
    TRANSMITTED = auto()   # مُرسَل    — transmitted / sent
    RECEIVED = auto()      # مُستلَم   — received by addressee
    INTERPRETED = auto()   # مُفسَّر   — interpreted by addressee
    ACCEPTED = auto()      # مقبول     — accepted
    REJECTED = auto()      # مرفوض     — rejected
    SUSPENDED = auto()     # موقوف     — suspended


# ── Exchange style type ──────────────────────────────────────────────


class ExchangeStyleType(Enum):
    """نوع أسلوب التبادل — the rhetorical style of a discourse exchange."""

    KHABARI = auto()        # خبري        — informative / declarative
    INSHAI = auto()         # إنشائي      — performative / constructive
    EXPLANATORY = auto()    # توضيحي      — explanatory
    ARGUMENTATIVE = auto()  # جدلي        — argumentative
    DIRECTIVE = auto()      # توجيهي      — directive
    INTERROGATIVE = auto()  # استفهامي    — interrogative
    PEDAGOGICAL = auto()    # تعليمي      — pedagogical
    TESTIMONIAL = auto()    # شهادي       — testimonial


# ── Exchange type ────────────────────────────────────────────────────


class ExchangeType(Enum):
    """نوع التبادل الخطابي — the type of discourse exchange."""

    REPORT = auto()       # تقرير      — factual report
    TEACHING = auto()     # تعليم      — teaching session
    QUESTION = auto()     # سؤال       — question / inquiry
    ANSWER = auto()       # إجابة      — answer / response
    COMMAND = auto()      # أمر        — command / directive
    WARNING = auto()      # تحذير      — warning
    PERSUASION = auto()   # إقناع      — persuasion attempt
    NEGOTIATION = auto()  # تفاوض      — negotiation
    TESTIMONY = auto()    # شهادة      — testimony
    EXPLANATION = auto()  # شرح        — explanation


# ── Explicitness level ───────────────────────────────────────────────


class ExplicitnessLevel(Enum):
    """مستوى الصراحة — the degree of explicitness in an utterance."""

    DIRECT = auto()       # مباشر       — direct / explicit
    SEMI_DIRECT = auto()  # شبه مباشر   — semi-direct
    IMPLICIT = auto()     # ضمني        — implicit / indirect


# ── Gap severity ─────────────────────────────────────────────────────


class GapSeverity(Enum):
    """درجة الثغرة — the severity of a detected knowledge gap."""

    FATAL = auto()     # قاتل     — fatal / blocks all processing
    CRITICAL = 2       # حرج      — critical severity
    MODERATE = 3       # معتدل    — moderate severity
    MINOR = 4          # طفيف     — minor / informational

    # backward-compatibility aliases
    HIGH = CRITICAL    # alias for CRITICAL
    MEDIUM = MODERATE  # alias for MODERATE


# ── Info kind ────────────────────────────────────────────────────────


class InfoKind(Enum):
    """نوع المعلومة — the kind of prior information."""

    LEXICAL = auto()       # معجمي     — lexical / dictionary knowledge
    ENCYCLOPEDIC = auto()  # موسوعي    — encyclopedic knowledge
    PROCEDURAL = auto()    # إجرائي    — procedural / how-to knowledge
    CONTEXTUAL = auto()    # سياقي     — contextual knowledge
    EXPERIENTIAL = auto()  # تجريبي    — experiential knowledge
    NORMATIVE = auto()     # معياري    — normative / rule-based knowledge


# ── Insertion policy ─────────────────────────────────────────────────


class InsertionPolicy(Enum):
    """سياسة الإدراج — the storage / insertion policy for a knowledge episode."""

    FOUNDATIONAL = auto()  # أساسي    — certain knowledge, insert as foundation
    ADMISSIBLE = auto()    # مقبول    — non-certain but admissible
    GUARDED = auto()       # محمي     — doubtful, insert with caution
    BLOCKED = auto()       # محظور    — invalid / impossible, do not insert


# ── Interpretive outcome type ────────────────────────────────────────


class InterpretiveOutcomeType(Enum):
    """نوع نتيجة التأويل — the type of interpretive outcome."""

    ALIGNED = auto()      # متوافق     — interpretation aligns with intent
    NARROWED = auto()     # مُضيَّق    — interpretation is narrower than intent
    EXPANDED = auto()     # مُوسَّع    — interpretation is broader than intent
    DISTORTED = auto()    # مشوَّه     — interpretation is distorted
    CONFLICTING = auto()  # متعارض     — interpretation conflicts with source
    UNRESOLVED = auto()   # غير محلول  — interpretation not yet resolved


# ── Judgement type ───────────────────────────────────────────────────


class JudgementType(Enum):
    """نوع الحكم — the logical or normative type of a judgement."""

    EXISTENCE = auto()             # وجود            — affirms or denies existence
    ESSENCE = auto()               # ماهية           — about the essence of a thing
    ATTRIBUTE = auto()             # وصف             — attributes a property
    RELATION = auto()              # علاقة           — relational judgement
    CAUSAL = auto()                # سببي            — causal judgement
    NORMATIVE = auto()             # معياري          — normative / deontic
    INTERPRETIVE = auto()          # تأويلي          — interpretive judgement
    METAPHYSICAL = auto()          # ميتافيزيقي      — metaphysical judgement
    FORMAL = auto()                # شكلي            — formal / logical
    FORMAL_CONTRADICTION = auto()  # تناقض منطقي     — formal contradiction
    PURE_LINGUISTIC = auto()       # لغوي بحت        — purely linguistic


# ── Link kind ────────────────────────────────────────────────────────


class LinkKind(Enum):
    """نوع الرابط — the broad kind of a link between two nodes."""

    CAUSAL = auto()             # سببي              — causal link
    CONTEXTUAL = auto()         # سياقي             — contextual link
    TEXTUAL_INFERENCE = auto()  # استنتاج نصي       — textual inference link
    SEMANTIC = auto()           # دلالي             — semantic / meaning link
    STRUCTURAL = auto()         # بنيوي             — structural / formal link
    TEMPORAL = auto()           # زمني              — temporal ordering link
    EPISTEMIC = auto()          # معرفي             — epistemic / evidential link
    NORMATIVE = auto()          # معياري            — normative / deontic link


# ── Method family ────────────────────────────────────────────────────


class MethodFamily(Enum):
    """عائلة المنهج — the family / class of an inferential or proof method."""

    RATIONAL = auto()      # عقلي         — rational / a priori reasoning
    SCIENTIFIC = auto()    # تجريبي        — empirical / scientific method
    LINGUISTIC = auto()    # لغوي          — linguistic / philological method
    MATHEMATICAL = auto()  # رياضي         — mathematical / formal method
    PHYSICAL = auto()      # حسي           — sensory / physical observation
    DIALECTICAL = auto()   # جدلي          — dialectical / debate-based reasoning
    ANALOGICAL = auto()    # قياسي         — analogical / qiyās reasoning


# ── Ontological constraint type ──────────────────────────────────────


class OntologicalConstraintType(Enum):
    """نوع القيد الوجودي — the type of an ontological constraint."""

    STRUCTURAL = auto()               # بنيوي            — structural / form constraint
    LEXICAL_CONSTRAINT = auto()       # قيد معجمي        — lexical access constraint
    CONTEXTUAL_CONSTRAINT = auto()    # قيد سياقي        — contextual resolution constraint
    INTERPRETIVE_CONSTRAINT = auto()  # قيد تأويلي       — interpretive selection constraint
    RHETORICAL_CONSTRAINT = auto()    # قيد بلاغي        — rhetorical / figurative constraint
    REFERENTIAL_CONSTRAINT = auto()   # قيد إحالي        — referential resolution constraint
    LOGICAL_CONSTRAINT = auto()       # قيد منطقي        — logical coherence constraint
    MODAL_CONSTRAINT = auto()         # قيد جهوي         — modal constraint
    TEMPORAL_CONSTRAINT = auto()      # قيد زمني         — temporal constraint
    CAUSAL_CONSTRAINT = auto()        # قيد سببي         — causal constraint
    NORMATIVE_CONSTRAINT = auto()     # قيد معياري       — normative / deontic constraint
    PRAGMATIC_CONSTRAINT = auto()     # قيد تداولي       — pragmatic constraint
    ENCYCLOPEDIC_CONSTRAINT = auto()  # قيد موسوعي       — encyclopedic constraint


# ── Path kind ────────────────────────────────────────────────────────


class PathKind(Enum):
    """نوع المسار المعرفي — the kind of epistemic pathway."""

    HISSI = auto()      # حسي       — sensory / perceptual path
    AQLI = auto()       # عقلي      — rational / logical path
    LINGUISTIC = auto() # لغوي      — linguistic path
    FORMAL = auto()     # شكلي      — formal / mathematical path


# ── Proof path kind ──────────────────────────────────────────────────


class ProofPathKind(Enum):
    """نوع مسار الإثبات — the kind of reasoning path used in a proof."""

    DIRECT_PROOF = auto()      # إثبات مباشر     — direct proof
    INDIRECT_PROOF = auto()    # إثبات غير مباشر — indirect / reductio proof
    INDUCTIVE_PROOF = auto()   # إثبات استقرائي  — inductive proof
    ANALOGICAL_PROOF = auto()  # إثبات قياسي     — analogical / qiyās proof
    EMPIRICAL_PROOF = auto()   # إثبات تجريبي    — empirical proof


# ── Purpose type ─────────────────────────────────────────────────────


class PurposeType(Enum):
    """نوع الغرض — the communicative purpose of a discourse act."""

    INFORM = auto()          # إعلام       — inform / convey fact
    INSTRUCT = auto()        # تعليم       — instruct / teach
    PERSUADE = auto()        # إقناع       — persuade
    TEST = auto()            # اختبار      — test / examine
    QUERY = auto()           # استفسار     — query / ask
    PRESERVE = auto()        # حفظ         — preserve knowledge
    REFUTE = auto()          # رد          — refute / counter
    WARN = auto()            # تحذير       — warn
    REQUEST_ACTION = auto()  # طلب فعل     — request an action
    CLARIFY = auto()         # توضيح       — clarify / explain


# ── Rational self kind ───────────────────────────────────────────────


class RationalSelfKind(Enum):
    """نوع الذات العاقلة — the kind of rational agent."""

    INDIVIDUAL = auto()       # فردي          — individual agent
    COLLECTIVE = auto()       # جماعي         — collective agent
    INSTITUTIONAL = auto()    # مؤسسي         — institutional agent
    MODELED_AGENT = auto()    # عميل مُنمذَج  — modeled / simulated agent


# ── Reality kind ─────────────────────────────────────────────────────


class RealityKind(Enum):
    """نوع الواقع — the ontological kind of a reality anchor."""

    MATERIAL = auto()         # مادي           — material / physical reality
    ABSTRACT = auto()         # مجرد           — abstract reality
    SOCIAL = auto()           # اجتماعي        — social / institutional reality
    HISTORICAL = auto()       # تاريخي         — historical reality
    PHYSICAL_OBJECT = auto()  # جسم مادي       — physical object
    EVENT = auto()            # حدث            — event / occurrence
    TEXT_OBJECT = auto()      # نص             — text / discourse object


# ── Receiver expected action ─────────────────────────────────────────


class ReceiverExpectedAction(Enum):
    """الفعل المتوقع من المتلقي — the action expected of the receiver."""

    UNDERSTAND = auto()  # فهم      — understand the message
    VERIFY = auto()      # تحقق     — verify the claim
    ACT = auto()         # تصرف     — act on the directive
    ANSWER = auto()      # أجب      — answer the question
    PRESERVE = auto()    # احفظ     — preserve the knowledge
    RELAY = auto()       # أرسل     — relay / transmit to others


# ── Receiver role type ───────────────────────────────────────────────


class ReceiverRoleType(Enum):
    """نوع دور المتلقي — the communicative role of the discourse receiver."""

    LISTENER = auto()    # مستمع    — passive listener
    LEARNER = auto()     # متعلم    — active learner
    EXAMINER = auto()    # فاحص     — examiner / evaluator
    ADDRESSEE = auto()   # مُخاطَب  — direct addressee
    RESPONDENT = auto()  # مُجيب    — respondent / answerer
    EVALUATOR = auto()   # مُقيِّم  — evaluator / critic


# ── Receiver state ───────────────────────────────────────────────────


class ReceiverState(Enum):
    """حالة المتلقي — the cognitive / attitudinal state of the receiver."""

    OPEN = auto()        # منفتح    — open / receptive
    RESISTANT = auto()   # مقاوم    — resistant / opposed
    BIASED = auto()      # متحيز    — biased
    UNCERTAIN = auto()   # متردد    — uncertain / hesitant
    ATTENTIVE = auto()   # منتبه    — attentive / alert


# ── Reception mode ───────────────────────────────────────────────────


class ReceptionMode(Enum):
    """نمط الاستقبال — the mode by which a message is received."""

    HEARD = auto()      # سمعي     — received by hearing
    READ = auto()       # قرائي    — received by reading
    OBSERVED = auto()   # مرئي     — received by observation
    INFERRED = auto()   # استنتاجي — received by inference
    RECALLED = auto()   # استرجاعي — received by recall / memory


# ── Reception state type ─────────────────────────────────────────────


class ReceptionStateType(Enum):
    """نوع حالة الاستقبال — the state of the reception process."""

    RECEIVED = auto()              # مُستلَم              — received
    UNDERSTOOD = auto()            # مفهوم                — understood
    MISUNDERSTOOD = auto()         # مساء فهمه            — misunderstood
    ACCEPTED = auto()              # مقبول                — accepted
    REJECTED = auto()              # مرفوض                — rejected
    SUSPENDED = auto()             # موقوف                — suspended
    PARTIALLY_UNDERSTOOD = auto()  # مفهوم جزئيًا        — partially understood


# ── Sender role type ─────────────────────────────────────────────────


class SenderRoleType(Enum):
    """نوع دور المرسِل — the communicative role of the discourse sender."""

    SOURCE = auto()       # مصدر      — original source of information
    EXPLAINER = auto()    # شارح      — explainer / commentator
    WITNESS = auto()      # شاهد      — witness / testifier
    TEACHER = auto()      # مُعلِّم   — teacher / instructor
    COMMANDER = auto()    # آمر       — commander / authority
    QUESTIONER = auto()   # سائل      — questioner / inquirer
    INTERPRETER = auto()  # مُفسِّر   — interpreter / translator


# ── Sense modality ───────────────────────────────────────────────────


class SenseModality(Enum):
    """الحاسة / الوسيط الإدراكي — the sense modality of a linguistic carrier."""

    VISUAL = auto()    # بصري    — visual / seen channel
    AUDITORY = auto()  # سمعي    — auditory / heard channel
    TACTILE = auto()   # لمسي    — tactile / touch channel
    OLFACTORY = auto() # شمي     — olfactory / smell channel
    GUSTATORY = auto() # ذوقي    — gustatory / taste channel
    KINESTHETIC = auto() # حركي  — kinesthetic / motion channel

    # backward-compatibility aliases
    VISION = VISUAL        # alias for VISUAL
    HEARING = AUDITORY     # alias for AUDITORY
    TOUCH = TACTILE        # alias for TACTILE
    SMELL = OLFACTORY      # alias for OLFACTORY
    TASTE = GUSTATORY      # alias for GUSTATORY


# ── Signified class ──────────────────────────────────────────────────


class SignifiedClass(Enum):
    """صنف المدلول — the broad ontological class of a signified."""

    # Ontological group
    ONTOLOGICAL = auto()         # وجودي          — ontological signified
    REFERENTIAL = auto()         # إحالي          — referential signified
    CONCEPTUAL = auto()          # مفاهيمي        — conceptual signified
    META_CONCEPTUAL = auto()     # ميتا-مفاهيمي   — meta-conceptual signified
    RELATIONAL = auto()          # علائقي         — relational signified
    NORMATIVE = auto()           # معياري         — normative signified
    PROPOSITIONAL = auto()       # قضوي           — propositional signified
    MODAL = auto()               # جهوي           — modal signified
    # Entity subgroup
    ENTITY_CONCEPT = auto()      # مفهوم ذات      — entity concept
    EVENT_CONCEPT = auto()       # مفهوم حدث      — event concept
    PROPERTY_CONCEPT = auto()    # مفهوم خاصية    — property concept
    # Referential subgroup
    DEICTIC = auto()             # إشاري          — deictic / indexical
    ANAPHORIC = auto()           # إحالي سابق     — anaphoric
    CATAPHORIC = auto()          # إحالي لاحق     — cataphoric
    # Meta subgroup
    META_LINGUISTIC = auto()     # ميتا-لغوي      — meta-linguistic
    META_PROPOSITIONAL = auto()  # ميتا-قضوي      — meta-propositional
    # Additional
    ABSTRACT_ENTITY = auto()     # كيان مجرد      — abstract entity
    CONCRETE_ENTITY = auto()     # كيان محسوس     — concrete entity
    INSTITUTIONAL = auto()       # مؤسسي          — institutional fact
    CAUSAL = auto()              # سببي           — causal signified
    TEMPORAL = auto()            # زمني           — temporal signified
    SPATIAL = auto()             # مكاني          — spatial signified


# ── Signifier class ──────────────────────────────────────────────────


class SignifierClass(Enum):
    """صنف الدال — the broad class of the linguistic signifier."""

    LEXICAL = auto()        # معجمي       — lexical signifier
    SYNTACTIC = auto()      # نحوي        — syntactic signifier
    PHONOLOGICAL = auto()   # صوتي        — phonological signifier
    MORPHOLOGICAL = auto()  # صرفي        — morphological signifier
    UTTERED_FORM = auto()   # صيغة ملفوظة — uttered form signifier
    RHETORICAL = auto()     # بلاغي       — rhetorical signifier
    PRAGMATIC = auto()      # تداولي      — pragmatic signifier
    PROSODIC = auto()       # إيقاعي      — prosodic signifier


# ── Style kind ───────────────────────────────────────────────────────


class StyleKind(Enum):
    """نوع الأسلوب — the rhetorical / discourse style of an utterance."""

    KHABAR = auto()       # خبر           — declarative / informative (khabar)
    INSHA = auto()        # إنشاء         — performative / constructive (inshāʾ)
    QUESTION = auto()     # سؤال          — interrogative
    ANSWER = auto()       # جواب          — answer / response
    COMMAND = auto()      # أمر           — command / imperative
    PROHIBITION = auto()  # نهي           — prohibition
    EXPLANATION = auto()  # شرح           — explanation / elucidation
    ARGUMENT = auto()     # حجة           — argumentative
    TESTIMONY = auto()    # شهادة         — testimonial
    SYMBOLIC = auto()     # رمزي          — symbolic / allusive


# ── Trace mode ───────────────────────────────────────────────────────


class TraceMode(Enum):
    """نمط التتبع — the mode of an epistemic trace."""

    DIRECT = auto()    # مباشر      — direct sensory trace
    MEDIATED = auto()  # وسيط       — mediated trace
    INFERRED = auto()  # استنتاجي   — inferred trace
    RECALLED = auto()  # استرجاعي   — recalled from memory

    # backward-compatibility aliases
    DIRECT_PERCEPTION = DIRECT  # alias for DIRECT


# ── Trace quality ────────────────────────────────────────────────────


class TraceQuality(Enum):
    """جودة التتبع — the reliability / quality grade of an epistemic trace."""

    STRONG = auto()     # قوية       — strong / reliable trace
    MODERATE = auto()   # معتدلة     — moderate quality
    WEAK = auto()       # ضعيفة      — weak / unreliable trace
    UNVERIFIED = auto() # غير محقق   — unverified trace


# ── Trust basis ──────────────────────────────────────────────────────


class TrustBasis(Enum):
    """أساس الثقة — the basis on which trust in a source is established."""

    EXPERTISE = auto()          # خبرة             — expertise / track record
    AUTHORITY = auto()          # سلطة             — positional authority
    FAMILIARITY = auto()        # معرفة شخصية      — personal familiarity
    TESTIMONY_CHAIN = auto()    # سلسلة شهادة      — chain of testimony (isnād)
    NONE = auto()               # لا أساس          — no established trust basis


# ── Trust level ──────────────────────────────────────────────────────


class TrustLevel(Enum):
    """مستوى الثقة — the degree of trust assigned to a source or claim."""

    LOW = auto()       # منخفضة   — low trust
    MEDIUM = auto()    # معتدلة   — moderate trust
    HIGH = auto()      # عالية    — high trust


# ── Utterance mode ───────────────────────────────────────────────────


class UtteranceMode(Enum):
    """نمط الملفوظ — the illocutionary mode of an utterance."""

    STATEMENT = auto()       # إخبار        — declarative statement
    QUESTION = auto()        # سؤال         — interrogative
    COMMAND = auto()         # أمر          — command / directive
    REPORT = auto()          # تقرير        — report / narration
    EXPLANATION = auto()     # شرح          — explanation
    DIALOGUE_TURN = auto()   # دور حواري    — dialogue turn


# ── Utterance-to-concept constraint ─────────────────────────────────


class UtteranceToConceptConstraint(Enum):
    """قيد ربط الملفوظ بالمفهوم — constraint governing utterance→concept mapping."""

    SURFACE_VALIDITY = auto()          # صلاحية السطح       — surface form validity
    LEXICAL_ACCESS = auto()            # وصول معجمي         — lexical access check
    CONTEXT_RESOLUTION = auto()        # حل سياقي           — contextual resolution
    CONCEPT_SELECTION = auto()         # اختيار المفهوم     — concept selection
    FIGURATIVE_DISAMBIGUATION = auto() # إزالة غموض مجازي   — figurative disambiguation
    REFERENTIAL_RESOLUTION = auto()    # حل الإحالة         — referential resolution
    LOGICAL_COHERENCE = auto()         # تماسك منطقي        — logical coherence check


# ── Uttered form class ───────────────────────────────────────────────


class UtteredFormClass(Enum):
    """صنف الصيغة الملفوظة — the surface form class of an uttered expression."""

    WORD_UTTERANCE = auto()      # كلمة ملفوظة     — single word utterance
    SENTENCE_UTTERANCE = auto()  # جملة ملفوظة     — sentence utterance
    MARKED_UTTERANCE = auto()    # ملفوظ مُعلَّم   — marked / tagged utterance
    ELLIPTICAL = auto()          # حذف             — elliptical / elided utterance
    COMPOUND = auto()            # مركب            — compound / complex utterance


# ── Validation outcome ───────────────────────────────────────────────


class ValidationOutcome(Enum):
    """نتيجة التحقق — the outcome of a validation check."""

    VALID = auto()                       # صالح               — validation passed
    REJECTED_METHODOLOGICALLY = auto()   # مرفوض منهجيًا     — methodologically rejected
    INCOMPLETE = auto()                  # ناقص               — incomplete validation
    INVALID = auto()                     # غير صالح           — invalid
    PENDING = auto()                     # قيد الانتظار       — pending


# ── Validation state ─────────────────────────────────────────────────


class ValidationState(Enum):
    """حالة التحقق — the current state of an ongoing validation process."""

    PENDING = auto()   # قيد الانتظار — not yet started
    VALID = auto()     # صالح          — validated successfully
    INVALID = auto()   # غير صالح      — validation failed
