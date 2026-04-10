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


# ── Ontology v1 — الجدول الأنطولوجي v1.0 ────────────────────────────


class SignifierClass(Enum):
    """صنف الدال — the major class of a signifier node (الدال).

    The hierarchy: every utterance (منطوق) is a signifier, but not every
    signifier is an utterance.  ``UTTERED_FORM`` marks the subtype whose
    surface has been actually realised in speech or writing.

    ==================  =====================================================
    Member               Description
    ==================  =====================================================
    PHONOLOGICAL         دال صوتي — phoneme, stress, intonation
    MORPHOLOGICAL        دال صرفي — root, pattern, augment
    LEXICAL              دال معجمي — word, lexical compound
    SYNTACTIC            دال نحوي — position, case-marker, governor
    TEXTUAL              دال نصي — textual reference, discourse connector
    PRAGMATIC            دال تداولي — intent, speech-situation, register
    RHETORICAL           دال بلاغي — metaphor, ellipsis, foregrounding
    UTTERED_FORM         منطوق — the realised surface form (فرع من الدال)
    ==================  =====================================================
    """

    PHONOLOGICAL = auto()  # دال صوتي
    MORPHOLOGICAL = auto()  # دال صرفي
    LEXICAL = auto()  # دال معجمي
    SYNTACTIC = auto()  # دال نحوي
    TEXTUAL = auto()  # دال نصي
    PRAGMATIC = auto()  # دال تداولي
    RHETORICAL = auto()  # دال بلاغي
    UTTERED_FORM = auto()  # منطوق — sub-class of signifier


class UtteredFormClass(Enum):
    """صنف المنطوق — sub-classification of an uttered / surface form.

    These are the five realisable shapes of the منطوق (uttered signifier).
    Only applicable when ``SignifierClass`` is ``UTTERED_FORM``.

    ===================  ====================================================
    Member                Description
    ===================  ====================================================
    PHONETIC_UTTERANCE    المنطوق من جهة الأداء الصوتي (stress, length, pause)
    WORD_UTTERANCE        المنطوق في صورة كلمة مفردة
    EXPRESSION_UTTERANCE  المنطوق في صورة تركيب / عبارة
    SENTENCE_UTTERANCE    المنطوق القضوي — full sentential unit
    MARKED_UTTERANCE      منطوق مقيّد بأداة بنيوية (إنّ، ما…إلا، etc.)
    ===================  ====================================================
    """

    PHONETIC_UTTERANCE = auto()  # أداء صوتي
    WORD_UTTERANCE = auto()  # كلمة منطوقة
    EXPRESSION_UTTERANCE = auto()  # تركيب منطوق
    SENTENCE_UTTERANCE = auto()  # جملة قضوية
    MARKED_UTTERANCE = auto()  # منطوق مقيد بأداة


class SignifiedClass(Enum):
    """صنف المدلول — the major class of a signified node (المدلول).

    The مفهوم (ConceptualSignified) is a sub-class of المدلول, so
    ``CONCEPTUAL`` marks the root under which all eight concept types fall.

    ======================  ================================================
    Member                   Description
    ======================  ================================================
    ONTOLOGICAL              مدلول وجودي — entity / substance
    PROPERTY                 مدلول وصفي — attribute / quality
    EVENT                    مدلول حدثي — action / occurrence
    RELATIONAL               مدلول علائقي — relation (above, with, because)
    PROPOSITIONAL            مدلول حكمي — assertion / negation / restriction
    REFERENTIAL              مدلول إحالي — deictic / anaphoric reference
    FUNCTIONAL               مدلول وظيفي — connector / structural function
    PRAGMATIC_SIGNIFIED      مدلول تداولي — illocutionary force
    LOGICAL                  مدلول منطقي — entailment / implication / inference
    RHETORICAL_SIGNIFIED     مدلول بلاغي — figurative / connotative meaning
    EPISTEMIC                مدلول معرفي — certainty / doubt / opinion
    NORMATIVE                مدلول معياري — obligation / permission / prohibition
    AFFECTIVE                مدلول وجداني — emotion / sentiment
    MODAL                    مدلول إمكاني/ضروري — possibility / necessity
    INSTITUTIONAL            مدلول مؤسسي — social / legal construct
    EMBODIED                 مدلول إدراكي متجسّد — sensorimotor grounding
    SELF_MODEL               مدلول ذاتي هوياتي — self / identity perspective
    FRAME                    مدلول إطاري — frame / scenario roles
    SCRIPT                   مدلول سيناريوي — procedural script / sequence
    CAUSAL_EXPLANATORY       مدلول سببي تفسيري — cause / condition / goal
    META_CONCEPTUAL          مدلول فوق-مفهومي — concept of concepts
    CONCEPTUAL               مفهوم — conceptual sub-class root
    ======================  ================================================
    """

    ONTOLOGICAL = auto()  # مدلول وجودي
    PROPERTY = auto()  # مدلول وصفي
    EVENT = auto()  # مدلول حدثي
    RELATIONAL = auto()  # مدلول علائقي
    PROPOSITIONAL = auto()  # مدلول حكمي
    REFERENTIAL = auto()  # مدلول إحالي
    FUNCTIONAL = auto()  # مدلول وظيفي
    PRAGMATIC_SIGNIFIED = auto()  # مدلول تداولي
    LOGICAL = auto()  # مدلول منطقي
    RHETORICAL_SIGNIFIED = auto()  # مدلول بلاغي
    EPISTEMIC = auto()  # مدلول معرفي
    NORMATIVE = auto()  # مدلول معياري
    AFFECTIVE = auto()  # مدلول وجداني
    MODAL = auto()  # مدلول إمكاني/ضروري
    INSTITUTIONAL = auto()  # مدلول مؤسسي
    EMBODIED = auto()  # مدلول إدراكي متجسّد
    SELF_MODEL = auto()  # مدلول ذاتي هوياتي
    FRAME = auto()  # مدلول إطاري
    SCRIPT = auto()  # مدلول سيناريوي
    CAUSAL_EXPLANATORY = auto()  # مدلول سببي تفسيري
    META_CONCEPTUAL = auto()  # مدلول فوق-مفهومي
    CONCEPTUAL = auto()  # مفهوم — root for conceptual sub-class


class ConceptualSignifiedClass(Enum):
    """صنف المفهوم — sub-classification of the conceptual signified (المفهوم).

    Applicable only when ``SignifiedClass`` is ``CONCEPTUAL``.

    ================  =========================================================
    Member             Description
    ================  =========================================================
    ENTITY_CONCEPT     مفهوم ذات — substance / individual
    PROPERTY_CONCEPT   مفهوم صفة — quality / attribute concept
    EVENT_CONCEPT      مفهوم حدث — action / occurrence concept
    RELATION_CONCEPT   مفهوم علاقة — relation / dependency concept
    NORM_CONCEPT       مفهوم معياري — obligation / value concept
    MENTAL_CONCEPT     مفهوم ذهني داخلي — intention / memory / imagination
    ABSTRACT_CONCEPT   مفهوم تجريدي — freedom / existence / possibility
    META_CONCEPT       مفهوم عن مفهوم — definition / genus / classification
    ================  =========================================================
    """

    ENTITY_CONCEPT = auto()  # مفهوم ذات
    PROPERTY_CONCEPT = auto()  # مفهوم صفة
    EVENT_CONCEPT = auto()  # مفهوم حدث
    RELATION_CONCEPT = auto()  # مفهوم علاقة
    NORM_CONCEPT = auto()  # مفهوم معياري
    MENTAL_CONCEPT = auto()  # مفهوم ذهني
    ABSTRACT_CONCEPT = auto()  # مفهوم تجريدي
    META_CONCEPT = auto()  # مفهوم عن مفهوم


class CouplingRelationType(Enum):
    """نوع علاقة الاقتران — how a signifier is bound to its signified.

    Sits one level above the classical ``DalalaType`` (which covers the
    intra-linguistic signification modes: مطابقة / تضمن / التزام / …).

    ====================  ====================================================
    Member                 Description
    ====================  ====================================================
    DIRECT                 اقتران مباشر — conventional / dictionary coupling
    POLYSEMOUS             اقتران متعدد — one form, multiple possible signifieds
    COMPOSITIONAL          اقتران تركيبي — meaning built from parts
    HIERARCHICAL           اقتران طبقي — multi-level (morpho-syntactic)
    CONTEXTUAL             اقتران سياقي — referent fixed by discourse context
    INFERENTIAL            اقتران استلزامي — signified implied, not stated
    FIGURATIVE             اقتران مجازي — metaphor / metonymy / synecdoche
    PERFORMATIVE           اقتران إنجازي — speech act with institutional force
    FUNCTIONAL_COUPLING    اقتران وظيفي — grammatical function word
    REFERENTIAL_COUPLING   اقتران إحالي — anaphoric / deictic resolution
    ====================  ====================================================
    """

    DIRECT = auto()  # مباشر
    POLYSEMOUS = auto()  # متعدد الاحتمال
    COMPOSITIONAL = auto()  # تركيبي
    HIERARCHICAL = auto()  # طبقي
    CONTEXTUAL = auto()  # سياقي
    INFERENTIAL = auto()  # استلزامي
    FIGURATIVE = auto()  # مجازي
    PERFORMATIVE = auto()  # إنجازي
    FUNCTIONAL_COUPLING = auto()  # وظيفي بنائي
    REFERENTIAL_COUPLING = auto()  # إحالي


class OntologicalConstraintType(Enum):
    """نوع القيد الأنطولوجي — constraint kind in the Ontology v1 model.

    Each constraint guards a different layer of the signifier→signified
    transition.  More specific than the classical ``ConstraintType`` (which
    covers only the five Mafhūm constraint kinds).

    ==========================  ================================================
    Member                       Description
    ==========================  ====٨============================================
    STRUCTURAL                   قيد بنيوي — syntactic well-formedness
    PHONOLOGICAL_CONSTRAINT      قيد صوتي — phonological legality
    MORPHOLOGICAL_CONSTRAINT     قيد صرفي — morphological pattern compatibility
    LEXICAL_CONSTRAINT           قيد معجمي — lexical convention
    SYNTACTIC_CONSTRAINT         قيد نحوي — syntactic position / case
    REFERENTIAL_CONSTRAINT       قيد إحالي — pronoun/deictic needs an antecedent
    CONTEXTUAL_CONSTRAINT        قيد سياقي — context required to fix reference
    PRAGMATIC_CONSTRAINT         قيد تداولي — speech-act conditions
    LOGICAL_CONSTRAINT           قيد منطقي — non-contradiction / coherence
    RHETORICAL_CONSTRAINT        قيد بلاغي — figurative reading needs a qarīna
    EPISTEMIC_CONSTRAINT         قيد معرفي — probabilistic/certainty tier
    INSTITUTIONAL_CONSTRAINT     قيد مؤسسي — performative requires authority
    INTERPRETIVE_CONSTRAINT      قيد تفسيري — disambiguation requires a tarjīḥ
    ==========================  ================================================
    """

    STRUCTURAL = auto()  # قيد بنيوي
    PHONOLOGICAL_CONSTRAINT = auto()  # قيد صوتي
    MORPHOLOGICAL_CONSTRAINT = auto()  # قيد صرفي
    LEXICAL_CONSTRAINT = auto()  # قيد معجمي
    SYNTACTIC_CONSTRAINT = auto()  # قيد نحوي
    REFERENTIAL_CONSTRAINT = auto()  # قيد إحالي
    CONTEXTUAL_CONSTRAINT = auto()  # قيد سياقي
    PRAGMATIC_CONSTRAINT = auto()  # قيد تداولي
    LOGICAL_CONSTRAINT = auto()  # قيد منطقي
    RHETORICAL_CONSTRAINT = auto()  # قيد بلاغي
    EPISTEMIC_CONSTRAINT = auto()  # قيد معرفي
    INSTITUTIONAL_CONSTRAINT = auto()  # قيد مؤسسي
    INTERPRETIVE_CONSTRAINT = auto()  # قيد تفسيري


class UtteranceToConceptConstraint(Enum):
    """قيود سلسلة المنطوق → المفهوم — the seven guards on the utterance-to-concept chain.

    These constraints are evaluated in order; any failure sets
    ``OntologicalConstraintRecord.passes = False``.

    ===========================  ==============================================
    Member                        Meaning
    ===========================  ==============================================
    SURFACE_VALIDITY              هل المنطوق سليم بنيويًا؟
    LEXICAL_ACCESS                هل يملك المنطوق مدخلًا معجميًا معتبرًا؟
    CONTEXT_RESOLUTION            هل السياق كافٍ لتعيين المقصود؟
    CONCEPT_SELECTION             هل اختير المفهوم الصحيح من بين الاحتمالات؟
    FIGURATIVE_DISAMBIGUATION     هل توجد قرينة تصرف عن الحقيقة إلى المجاز؟
    REFERENTIAL_RESOLUTION        هل المرجع متاح إذا كان المنطوق إحاليًا؟
    LOGICAL_COHERENCE             هل التفسير متسق مع بقية البنية؟
    ===========================  ==============================================
    """

    SURFACE_VALIDITY = auto()  # صحة البنية السطحية
    LEXICAL_ACCESS = auto()  # وجود مدخل معجمي
    CONTEXT_RESOLUTION = auto()  # كفاية السياق
    CONCEPT_SELECTION = auto()  # اختيار المفهوم الصحيح
    FIGURATIVE_DISAMBIGUATION = auto()  # وجود قرينة مجازية
    REFERENTIAL_RESOLUTION = auto()  # توفر المرجع الإحالي
    LOGICAL_COHERENCE = auto()  # تسق التفسير مع البنية


# ── Epistemic v1 — المنهج العقلي: الرتب والتحقق ──────────────────────


class EpistemicRank(Enum):
    """الرتبة الإبستيمية — the four-level ladder of rational judgement.

    Based on al-Nabhani's rational method: a valid cognitive episode grounds
    reality + sensed trace + prior information + linking, then produces one
    of exactly four ranks.  Methodological rejection is modelled separately
    in :class:`ValidationOutcome`.

    ==================  =======================================================
    Member               Meaning
    ==================  =======================================================
    CERTAIN              قطعي — grounded existence judgement with valid proof
    TRUE_NON_CERTAIN     حقيقي غير قطعي — valid essence / attribute / relation
    PROBABILISTIC_DOUBT  ظني — partially grounded, unresolved or incomplete
    IMPOSSIBLE           ممتنع — only for FORMAL_CONTRADICTION judgements
    ==================  =======================================================
    """

    CERTAIN = auto()  # قطعي
    TRUE_NON_CERTAIN = auto()  # حقيقي غير قطعي
    PROBABILISTIC_DOUBT = auto()  # ظني
    IMPOSSIBLE = auto()  # ممتنع


class ValidationOutcome(Enum):
    """نتيجة التحقق — outcome of the methodological validity check.

    Distinct from :class:`EpistemicRank`: a ``REJECTED_METHODOLOGICALLY``
    episode never reaches the rank ladder at all.

    ========================  ================================================
    Member                     Meaning
    ========================  ================================================
    VALID                      صالح — all conditions met
    INVALID                    غير صالح — conditions identified but not met
    PENDING                    معلّق — waiting for missing inputs
    REJECTED_METHODOLOGICALLY  مرفوض منهجيًا — foundational conditions absent
    ========================  ================================================
    """

    VALID = auto()  # صالح
    INVALID = auto()  # غير صالح
    PENDING = auto()  # معلّق
    REJECTED_METHODOLOGICALLY = auto()  # مرفوض منهجيًا


class DecisionCode(Enum):
    """رموز القرار — stable codes for every validator failure.

    Codes are stable across versions so that API consumers and tests can
    check ``result.codes`` without relying on human-readable messages.

    ========================  ================================================
    Code                       Meaning
    ========================  ================================================
    EPI001_MISSING_REALITY     لا مرساة واقع
    EPI002_MISSING_SENSE       لا أثر حسّي
    EPI003_MISSING_PRIOR_INFO  لا معلومة سابقة
    EPI004_OPINION_CONTAMINATION  تلوث الرأي المسبق فوق العتبة
    EPI005_MISSING_LINKING     لا أثر ربط
    EPI006_MISSING_JUDGEMENT   لا حكم
    EPI007_MISSING_METHOD      لا طريقة
    EPI008_METHOD_FIT_FAILURE  الطريقة لا تناسب المجال
    EPI009_CARRIER_INVALID     حامل لغوي غير صالح
    EPI010_MISSING_PROOF_PATH  لا مسار إثبات
    EPI011_MISSING_CONFLICT_RULE  لا قاعدة تعارض
    EPI012_CARRIER_BOTH_MISSING   النوع BOTH لكن أحد الطرفين غائب
    EPI013_PROOF_METHOD_MISMATCH  مسار الإثبات لا يتوافق مع الطريقة
    EPI014_UTTERANCE_CONCEPT_CONFLICT  تعارض المنطوق والمفهوم بلا قاعدة فصل
    ========================  ================================================
    """

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


class JudgementType(Enum):
    """نوع الحكم — the scope of a rational judgement.

    Determines which epistemic rank is reachable:
    * ``EXISTENCE`` with grounded proof → :attr:`EpistemicRank.CERTAIN`
    * ``ESSENCE``, ``ATTRIBUTE``, ``RELATION``, ``INTERPRETIVE`` →
      :attr:`EpistemicRank.TRUE_NON_CERTAIN` at best
    * ``FORMAL_CONTRADICTION`` → :attr:`EpistemicRank.IMPOSSIBLE`

    =====================  =================================================
    Member                  Meaning
    =====================  =================================================
    EXISTENCE               حكم على الوجود
    ESSENCE                 حكم على الحقيقة
    ATTRIBUTE               حكم على الصفة
    RELATION                حكم على العلاقة
    INTERPRETIVE            حكم على التفسير
    FORMAL_CONTRADICTION    حكم بتناقض صوري
    =====================  =================================================
    """

    EXISTENCE = auto()  # حكم على الوجود
    ESSENCE = auto()  # حكم على الحقيقة
    ATTRIBUTE = auto()  # حكم على الصفة
    RELATION = auto()  # حكم على العلاقة
    INTERPRETIVE = auto()  # حكم على التفسير
    FORMAL_CONTRADICTION = auto()  # حكم بتناقض صوري
    # restored for backward compatibility with episode_validator
    CAUSAL = auto()  # سببي — cause-effect judgement
    NORMATIVE = auto()  # معياري — obligation / permission / prohibition
    PURE_LINGUISTIC = auto()  # لغوي بحت — purely grammatical / structural
    METAPHYSICAL = auto()  # ميتافيزيقي — beyond empirical verification
    FORMAL = auto()  # صوري — formal / mathematical (non-contradiction)


class MethodFamily(Enum):
    """عائلة الطريقة — the epistemological family a method belongs to.

    Scientific method is a *branch* specialised for empirical material
    inquiry; it must not be treated as the universal basis of knowledge.

    ==========  ============================================================
    Member       Meaning
    ==========  ============================================================
    RATIONAL     عقلية — the universal basis: واقع + حس + معلومات سابقة + ربط
    SCIENTIFIC   علمية — empirical/material inquiry (branch of rational)
    TEXTUAL      نقلية — transmission-based (revelation, narration)
    DEDUCTIVE    استنباطية — formal deduction from axioms
    INDUCTIVE    استقرائية — induction from instances
    ==========  ============================================================
    """

    RATIONAL = auto()  # عقلية
    SCIENTIFIC = auto()  # علمية
    TEXTUAL = auto()  # نقلية
    DEDUCTIVE = auto()  # استنباطية
    INDUCTIVE = auto()  # استقرائية
    # restored for backward compatibility with episode_validator
    LINGUISTIC = auto()  # لغوي — utterance / concept linguistic analysis
    MATHEMATICAL = auto()  # رياضي — formal symbolic proof
    PHYSICAL = auto()  # فيزيائي — physical law and measurement


class CarrierType(Enum):
    """نوع الحامل اللغوي — the linguistic transport type.

    Only two carriers exist: Utterance (منطوق) and Concept (مفهوم).
    ``BOTH`` requires *both* carriers to be present.

    =========  ============================================================
    Member      Meaning
    =========  ============================================================
    UTTERANCE   منطوق فقط
    CONCEPT     مفهوم فقط
    BOTH        منطوق + مفهوم معًا
    =========  ============================================================
    """

    UTTERANCE = auto()  # منطوق
    CONCEPT = auto()  # مفهوم
    BOTH = auto()  # كلاهما


class RealityKind(Enum):
    """نوع الواقع — the ontological character of the reality anchor.

    ==========  ==============================================================
    Member       Meaning
    ==========  ==============================================================
    MATERIAL     مادي — physically perceptible object or event
    ABSTRACT     مجرد — logical / mathematical entity
    SOCIAL       اجتماعي — convention, norm, institution
    HISTORICAL   تاريخي — past event attested by transmission
    ==========  ==============================================================
    """

    MATERIAL = auto()  # مادي
    ABSTRACT = auto()  # مجرد
    SOCIAL = auto()  # اجتماعي
    HISTORICAL = auto()  # تاريخي
    # restored from episode_validator schema (backward compatibility)
    PHYSICAL_OBJECT = auto()  # جسم مادي
    EVENT = auto()  # حدث
    RELATION = auto()  # علاقة
    TEXT_OBJECT = auto()  # نص / خطاب
    MENTAL_STATE = auto()  # حالة ذهنية
    FORMAL_STRUCTURE = auto()  # بنية صورية


class SenseModality(Enum):
    """حاسة الأثر الحسي — the sensory channel of a sense trace.

    =======  ================================================================
    Member    Meaning
    =======  ================================================================
    VISUAL    بصري
    AUDITORY  سمعي
    TACTILE   لمسي
    OLFACTORY شمّي
    GUSTATORY ذوقي
    INTERNAL  داخلي (proprioception / interoception)
    =======  ================================================================
    """

    VISUAL = auto()  # بصري
    AUDITORY = auto()  # سمعي
    TACTILE = auto()  # لمسي
    OLFACTORY = auto()  # شمّي
    GUSTATORY = auto()  # ذوقي
    INTERNAL = auto()  # داخلي
    # backward-compatible aliases for old names (episode_validator compat)
    VISION = VISUAL  # alias → بصر
    HEARING = AUDITORY  # alias → سمع
    TOUCH = TACTILE  # alias → لمس
    SMELL = OLFACTORY  # alias → شم
    TASTE = GUSTATORY  # alias → ذوق


class TraceMode(Enum):
    """وضع الأثر — whether the trace is direct or indirect.

    ==========  ==============================================================
    Member       Meaning
    ==========  ==============================================================
    DIRECT       مباشر — first-hand sensory access
    REPORTED     منقول — attested by reliable report
    INFERRED     مستنتج — deduced from physical evidence
    ==========  ==============================================================
    """

    DIRECT = auto()  # مباشر
    REPORTED = auto()  # منقول
    INFERRED = auto()  # مستنتج
    MEDIATED = auto()  # بواسطة — restored for backward compatibility
    # backward-compatible alias
    DIRECT_PERCEPTION = DIRECT  # alias


class LinkKind(Enum):
    """نوع رابط الربط — the kind of linking used in the cognitive episode.

    =============  ===========================================================
    Member          Meaning
    =============  ===========================================================
    CAUSAL          سببي — cause-effect
    ANALOGICAL      قياسي — analogy
    DEFINITIONAL    تعريفي — by definition
    CONTEXTUAL      سياقي — contextual inference
    AUTHORITATIVE   نقلي — from authoritative text
    =============  ===========================================================
    """

    CAUSAL = auto()  # سببي
    ANALOGICAL = auto()  # قياسي
    DEFINITIONAL = auto()  # تعريفي
    CONTEXTUAL = auto()  # سياقي
    AUTHORITATIVE = auto()  # نقلي
    # restored for backward compatibility with episode_validator
    TEXTUAL_INFERENCE = auto()  # استنباط نصي
    LOGICAL_DEDUCTION = auto()  # استنتاج منطقي
    EMPIRICAL = auto()  # استقراء تجريبي


class ProofPathKind(Enum):
    """نوع مسار الإثبات — how the proof path is constructed.

    ===========  ===============================================================
    Member        Meaning
    ===========  ===============================================================
    DIRECT_PROOF  برهان مباشر
    BY_NEGATION   برهان بالنفي (reductio ad absurdum)
    BY_EXCLUSION  برهان بالحصر (elimination of alternatives)
    COMPOSITE     مركّب — combination of the above
    ===========  ===============================================================
    """

    DIRECT_PROOF = auto()  # برهان مباشر
    BY_NEGATION = auto()  # برهان بالنفي
    BY_EXCLUSION = auto()  # برهان بالحصر
    COMPOSITE = auto()  # مركّب


class GapSeverity(Enum):
    """درجة الفجوة — how serious a detected gap is.

    ========  =================================================================
    Member     Meaning
    ========  =================================================================
    MINOR      طفيف — does not change rank
    MODERATE   معتدل — may lower rank one step
    CRITICAL   حرج — forces PROBABILISTIC_DOUBT or worse
    FATAL      قاتل — forces REJECTED_METHODOLOGICALLY
    ========  =================================================================
    """

    MINOR = auto()  # طفيف
    MODERATE = auto()  # معتدل
    CRITICAL = auto()  # حرج
    FATAL = auto()  # قاتل
    # backward-compatible aliases for old names
    HIGH = CRITICAL  # alias → عالٍ
    MEDIUM = MODERATE  # alias → متوسط


class ContaminationLevel(Enum):
    """مستوى تلوث الرأي المسبق — how much prior opinion contaminates the episode.

    LOW is acceptable; MEDIUM triggers a warning; HIGH causes rejection.

    ======  ===================================================================
    Member   Meaning
    ======  ===================================================================
    NONE     لا تلوث
    LOW      تلوث منخفض — acceptable
    MEDIUM   تلوث متوسط — flagged, rank may be lowered
    HIGH     تلوث مرتفع — causes EPI004 rejection
    ======  ===================================================================
    """

    NONE = auto()  # لا تلوث
    LOW = auto()  # منخفض
    MEDIUM = auto()  # متوسط
    HIGH = auto()  # مرتفع


class InsertionPolicy(Enum):
    """سياسة الإدخال المعرفي — whether and how a validated episode may be stored.

    ===========  ===============================================================
    Member        Meaning
    ===========  ===============================================================
    FOUNDATIONAL  أساسي — unconditionally storable (CERTAIN rank)
    ADMISSIBLE    مقبول — storable with normal confidence (TRUE_NON_CERTAIN)
    GUARDED       محاط بحذر — storable with explicit uncertainty flag
    BLOCKED       محجوب — must not be stored (invalid or rejected)
    ===========  ===============================================================
    """

    FOUNDATIONAL = auto()  # أساسي
    ADMISSIBLE = auto()  # مقبول
    GUARDED = auto()  # محاط بحذر
    BLOCKED = auto()  # محجوب


# ── Backward-compatible enums (restored for episode_validator) ────────────────


class ValidationState(Enum):
    """حالة صحة الخبرة المعرفية — lifecycle state of a KnowledgeEpisode.

    Restored for backward compatibility with the episode_validator module.
    New code should prefer :class:`ValidationOutcome`.
    """

    PENDING = auto()  # pending — not yet validated
    VALID = auto()  # valid — all checks passed
    INVALID = auto()  # invalid — one or more checks failed


class CarrierClass(Enum):
    """صنف الحامل اللغوي — whether the carrier is utterance, concept, or both.

    Restored for backward compatibility with the episode_validator module.
    New code should prefer :class:`CarrierType`.
    """

    UTTERANCE = auto()  # منطوق فقط
    CONCEPT = auto()  # مفهوم فقط
    BOTH = auto()  # كلاهما


class PathKind(Enum):
    """نوع مسار الإثبات — the nature of the proof path.

    Restored for backward compatibility with the episode_validator module.
    New code should prefer :class:`ProofPathKind`.

    =========  ===============================================
    Member      Arabic meaning
    =========  ===============================================
    HISSI       حسي — direct sensory evidence
    AQLI        عقلي — rational / logical proof
    LINGUISTIC  لغوي — linguistic / textual evidence
    FORMAL      صوري — formal mathematical / logical proof
    =========  ===============================================
    """

    HISSI = auto()  # حسي
    AQLI = auto()  # عقلي
    LINGUISTIC = auto()  # لغوي
    FORMAL = auto()  # صوري


class TraceQuality(Enum):
    """جودة الأثر الحسي — reliability of the sense trace.

    Restored for backward compatibility with the episode_validator module.
    """

    STRONG = auto()  # قوي
    MODERATE = auto()  # متوسط
    WEAK = auto()  # ضعيف


class InfoKind(Enum):
    """نوع المعلومة السابقة — the category of prior information.

    Restored for backward compatibility with the episode_validator module.

    ====================  ===================================
    Member                 Arabic meaning
    ====================  ===================================
    LEXICAL                معجمي
    LINGUISTIC_RULE        قاعدة لغوية / دلالية
    EMPIRICAL              تجريبي / مُختبَر
    LOGICAL                منطقي / عقلي
    FORMAL                 صوري / رياضي
    ANALOGICAL             قياسي / تمثيلي
    ====================  ===================================
    """

    LEXICAL = auto()  # معجمي
    LINGUISTIC_RULE = auto()  # قاعدة لغوية
    EMPIRICAL = auto()  # تجريبي
    LOGICAL = auto()  # منطقي
    FORMAL = auto()  # صوري
    ANALOGICAL = auto()  # قياسي


# ── Discourse Exchange enums (Schema التداول المعرفي) ───────────────────────────


class ExchangeType(Enum):
    """نوع التداول المعرفي — high-level discourse exchange category."""

    REPORT = auto()
    TEACHING = auto()
    QUESTION = auto()
    ANSWER = auto()
    COMMAND = auto()
    WARNING = auto()
    PERSUASION = auto()
    NEGOTIATION = auto()
    TESTIMONY = auto()
    EXPLANATION = auto()


class ExchangePurposeType(Enum):
    """صنف غرض التبادل — coarse-grained purpose class."""

    INFORM = auto()
    TEACH = auto()
    VERIFY = auto()
    GUIDE = auto()
    BIND = auto()
    PERSUADE = auto()
    WARN = auto()
    REQUEST = auto()
    TEST = auto()
    PRESERVE_KNOWLEDGE = auto()


class ExchangeStyleType(Enum):
    """صنف أسلوب التبادل — coarse-grained discourse style class."""

    KHABARI = auto()
    INSHAI = auto()
    EXPLANATORY = auto()
    ARGUMENTATIVE = auto()
    DIRECTIVE = auto()
    INTERROGATIVE = auto()
    PEDAGOGICAL = auto()
    TESTIMONIAL = auto()


class ExchangeStatus(Enum):
    """حالة التبادل — lifecycle state of discourse exchange."""

    DRAFTED = auto()
    TRANSMITTED = auto()
    RECEIVED = auto()
    INTERPRETED = auto()
    ACCEPTED = auto()
    REJECTED = auto()
    SUSPENDED = auto()


class RationalSelfKind(Enum):
    """نوع الذات العاقلة الداخلة في التداول."""

    INDIVIDUAL = auto()
    COLLECTIVE = auto()
    INSTITUTIONAL = auto()
    MODELED_AGENT = auto()


class SenderRoleType(Enum):
    """نوع دور المرسل."""

    SOURCE = auto()
    EXPLAINER = auto()
    WITNESS = auto()
    TEACHER = auto()
    COMMANDER = auto()
    QUESTIONER = auto()
    INTERPRETER = auto()


class AuthorityLevel(Enum):
    """درجة سلطة المرسل ضمن سياق التداول."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class ReceiverRoleType(Enum):
    """نوع دور المستقبل."""

    LISTENER = auto()
    LEARNER = auto()
    EXAMINER = auto()
    ADDRESSEE = auto()
    RESPONDENT = auto()
    EVALUATOR = auto()


class ReceiverExpectedAction(Enum):
    """الفعل المتوقع من المستقبل بعد التداول."""

    UNDERSTAND = auto()
    VERIFY = auto()
    ACT = auto()
    ANSWER = auto()
    PRESERVE = auto()
    RELAY = auto()


class PurposeType(Enum):
    """الغرض التفصيلي للتداول."""

    INFORM = auto()
    INSTRUCT = auto()
    PERSUADE = auto()
    TEST = auto()
    QUERY = auto()
    PRESERVE = auto()
    REFUTE = auto()
    WARN = auto()
    REQUEST_ACTION = auto()
    CLARIFY = auto()


class ExplicitnessLevel(Enum):
    """درجة تصريح الأسلوب."""

    DIRECT = auto()
    SEMI_DIRECT = auto()
    IMPLICIT = auto()


class StyleKind(Enum):
    """النمط التفصيلي لأسلوب الخطاب."""

    KHABAR = auto()
    INSHA = auto()
    QUESTION = auto()
    ANSWER = auto()
    COMMAND = auto()
    PROHIBITION = auto()
    EXPLANATION = auto()
    ARGUMENT = auto()
    TESTIMONY = auto()
    SYMBOLIC = auto()


class UtteranceMode(Enum):
    """نمط المنطوق المتداول."""

    STATEMENT = auto()
    QUESTION = auto()
    COMMAND = auto()
    REPORT = auto()
    EXPLANATION = auto()
    DIALOGUE_TURN = auto()


class DalaalaKind(Enum):
    """نوع الدلالة في طبقة التداول (distinct alias from DalalaType)."""

    MUTABAQA = auto()
    TADHAMMUN = auto()
    ILTIZAM = auto()
    ISHARA = auto()


class ReceptionMode(Enum):
    """نمط استقبال الرسالة."""

    HEARD = auto()
    READ = auto()
    OBSERVED = auto()
    INFERRED = auto()
    RECALLED = auto()


class ReceiverState(Enum):
    """حالة المستقبل الذهنية عند الاستقبال."""

    OPEN = auto()
    RESISTANT = auto()
    BIASED = auto()
    UNCERTAIN = auto()
    ATTENTIVE = auto()


class ReceptionStateType(Enum):
    """مآل الاستقبال بعد الفهم/الحكم."""

    RECEIVED = auto()
    UNDERSTOOD = auto()
    MISUNDERSTOOD = auto()
    ACCEPTED = auto()
    REJECTED = auto()
    SUSPENDED = auto()
    PARTIALLY_UNDERSTOOD = auto()


class TrustLevel(Enum):
    """مستوى الثقة بالمصدر."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class TrustBasis(Enum):
    """أساس الثقة بالمصدر."""

    EXPERTISE = auto()
    AUTHORITY = auto()
    FAMILIARITY = auto()
    TESTIMONY_CHAIN = auto()
    NONE = auto()


class InterpretiveOutcomeType(Enum):
    """نتيجة التأويل عند المستقبل."""

    ALIGNED = auto()
    NARROWED = auto()
    EXPANDED = auto()
    DISTORTED = auto()
    CONFLICTING = auto()
    UNRESOLVED = auto()


class DiscourseGapType(Enum):
    """أنواع فجوات التداول المعرفي."""

    MISSING_SENDER = auto()
    MISSING_RECEIVER = auto()
    MISSING_PURPOSE = auto()
    MISSING_STYLE = auto()
    INVALID_STYLE_PURPOSE_FIT = auto()
    MISSING_CARRIER = auto()
    INVALID_CARRIER = auto()
    MISSING_RECEPTION = auto()
    MISSING_RECEPTION_STATE = auto()
    MISSING_TRANSFERRED_KNOWLEDGE = auto()
    INVALID_TRANSFERRED_KNOWLEDGE = auto()
    MISSING_TRUST_PROFILE = auto()
    RECEPTION_INCONSISTENCY = auto()
    SENDER_PURPOSE_MISMATCH = auto()


class DiscourseValidationOutcome(Enum):
    """نتيجة صلاحية التداول المعرفي."""

    VALID = auto()
    INVALID = auto()
    INCOMPLETE = auto()
