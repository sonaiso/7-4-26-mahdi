"""Enumerations used across the Arabic engine.

Each enum encodes a discrete, finite category so that every linguistic
label in the system is a computable integer — not a free-form string.
"""

from __future__ import annotations

from enum import Enum, auto

# ── Part of Speech ──────────────────────────────────────────────────

class POS(Enum):
    """Arabic part-of-speech tags (اسم / فعل / حرف + sub-types)."""
    ISM = auto()        # اسم
    FI3L = auto()       # فعل
    HARF = auto()       # حرف
    SIFA = auto()       # صفة
    ZARF = auto()       # ظرف
    DAMIR = auto()      # ضمير
    UNKNOWN = auto()


# ── Semantic (ontological) type ─────────────────────────────────────

class SemanticType(Enum):
    """High-level concept categories (التعريف 5 — ontological mapping)."""
    ENTITY = auto()     # ذات
    EVENT = auto()      # حدث
    ATTRIBUTE = auto()  # صفة
    RELATION = auto()   # علاقة
    NORM = auto()       # حكم شرعي / قاعدة


# ── Dalāla (signification) type ─────────────────────────────────────

class DalalaType(Enum):
    """Kinds of signification linking signifier → signified."""
    MUTABAQA = auto()   # مطابقة – exact denotation
    TADAMMUN = auto()   # تضمن  – inclusion (part of meaning)
    ILTIZAM = auto()    # التزام – implication (necessary concomitant)
    ISNAD = auto()      # إسناد – predication
    TAQYID = auto()     # تقييد – restriction / qualification
    IDAFA = auto()      # إضافة – genitive construction
    IHALA = auto()      # إحالة – referential link


# ── Truth state ─────────────────────────────────────────────────────

class TruthState(Enum):
    """Epistemic status of a proposition (التعريف 8)."""
    CERTAIN = auto()    # قطعي
    PROBABLE = auto()   # ظني راجح
    POSSIBLE = auto()   # ممكن
    DOUBTFUL = auto()   # مشكوك
    FALSE = auto()      # باطل
    UNKNOWN = auto()


# ── Guidance state ──────────────────────────────────────────────────

class GuidanceState(Enum):
    """Normative/actionable status derived from evaluation."""
    OBLIGATORY = auto()   # واجب
    RECOMMENDED = auto()  # مستحب
    PERMISSIBLE = auto()  # مباح
    DISLIKED = auto()     # مكروه
    FORBIDDEN = auto()    # حرام
    NOT_APPLICABLE = auto()


# ── I'rāb (syntactic inflection) ────────────────────────────────────

class IrabCase(Enum):
    """Grammatical case markers."""
    RAF3 = auto()       # رفع
    NASB = auto()       # نصب
    JARR = auto()       # جر
    JAZM = auto()       # جزم
    SUKUN = auto()      # سكون (مبني)
    UNKNOWN = auto()


class IrabRole(Enum):
    """Syntactic role in the sentence."""
    FA3IL = auto()      # فاعل
    MAF3UL_BIH = auto() # مفعول به
    MUBTADA = auto()    # مبتدأ
    KHABAR = auto()     # خبر
    FI3L = auto()       # فعل
    MUDAF = auto()      # مضاف
    MUDAF_ILAYH = auto()# مضاف إليه
    SIFA = auto()       # صفة
    HAL = auto()        # حال
    TAMYIZ = auto()     # تمييز
    ZARF = auto()       # ظرف
    JARR_MAJRUR = auto()# جار ومجرور
    UNKNOWN = auto()


# ── Time / Space references (v2) ────────────────────────────────────

class TimeRef(Enum):
    """Temporal anchors for propositions."""
    PAST = auto()       # ماض
    PRESENT = auto()    # حاضر
    FUTURE = auto()     # مستقبل
    ETERNAL = auto()    # أزلي / دائم
    UNSPECIFIED = auto()


class SpaceRef(Enum):
    """Spatial anchors for propositions."""
    HERE = auto()       # هنا
    THERE = auto()      # هناك
    NAMED = auto()      # مكان محدد بالاسم
    UNSPECIFIED = auto()


# ── Mafhūm types (Ch. 21) ───────────────────────────────────────────

class ConstraintType(Enum):
    """Structural constraint types in the Manṭūq (أنواع القيد البنيوي).

    Each constraint type generates a corresponding Mafhūm type when
    combined with a mental counterpart and a transition rule.
    """
    SHART = auto()      # شرط — condition (تعليق الحكم)
    GHAYA = auto()      # غاية — goal / endpoint (تحديد المنتهى)
    ADAD = auto()       # عدد — number (التحديد الكمي)
    WASF = auto()       # وصف — description (التقييد الوصفي)
    ISHARA = auto()     # إشارة — reference / deixis (التخصيص الإحالي)


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
    SHART = auto()      # مفهوم الشرط
    GHAYA = auto()      # مفهوم الغاية
    ADAD = auto()       # مفهوم العدد
    WASF = auto()       # مفهوم الوصف
    ISHARA = auto()     # مفهوم الإشارة


# ── D_min Phonological layer ─────────────────────────────────────────
# Implements: D_min(x) = (u, c, g, f, t)
# where every field maps to a computable integer, making the full
# 5-tuple a numeric vector over ℕ⁵.

class PhonCategory(Enum):
    """Major phonological category — الفئة الكبرى (c in D_min)."""
    CONSONANT = auto()      # صامت
    SEMI_VOWEL = auto()     # شبه صامت / صائت ذو تحولات (و ي)
    LONG_VOWEL = auto()     # صائت طويل / حامل كتابي (ا)
    SHORT_VOWEL = auto()    # صائت قصير (فتحة ضمة كسرة)
    SUKUN = auto()          # علامة انعدام حركة (ْ)
    SHADDA = auto()         # علامة بنيوية / تضعيف (ّ)
    TANWIN = auto()         # حركة/علامة مركبة / تنوين (ً ٌ ٍ)
    SPECIAL_MARK = auto()   # علامة مدّ/همز خاصة (ٰ ٓ)


class PhonGroup(Enum):
    """Phonological/articulatory group — المجموعة الكبرى (g in D_min)."""
    # ── Consonant articulation groups (مجموعات الصوامت) ────────────
    HNJ_MZM = auto()        # حنجري/مزمَري — ء
    HNJ_HLQ = auto()        # حنجري/حلقي   — ه
    HLQ = auto()            # حلقي          — ح ع غ
    HLQ_LHW = auto()        # حلقي/لهوي     — خ
    LHW = auto()            # لهوي          — ق
    TBQ_LHW = auto()        # طبقي/لهوي     — ك
    SHJR = auto()           # شجري/حنكي     — ج ش
    ASN_LTH = auto()        # أسناني-لثوي   — ت د
    ASN_LTH_MTPQ = auto()   # أسناني-لثوي مطبق — ط
    BAYNASN = auto()        # بين-أسناني    — ث ذ
    BAYNASN_MTPQ = auto()   # بين-أسناني مطبق — ظ
    LTH = auto()            # لثوي          — ر ل ن (with feature distinctions)
    LTH_MTPQ = auto()       # لثوي مطبق     — ض
    ASLI = auto()           # أسلي/صفيري    — ز س
    ASLI_MTPQ = auto()      # أسلي مطبق     — ص
    SHF = auto()            # شفوي          — ب م (with feature distinctions)
    SHF_ASN = auto()        # شفوي-أسناني   — ف
    SHF_LYN = auto()        # شفوي لين      — و (semi-vowel)
    HNK_LYN = auto()        # حنكي لين      — ي (semi-vowel)
    # ── Long vowel (الصوائت الطويلة) ──────────────────────────────
    ALF_LV = auto()         # ألف           — ا
    # ── Short vowel / diacritic groups (الحركات والعلامات) ─────────
    FTH = auto()            # فتح           — َ (U+064E)
    DMM = auto()            # ضم            — ُ (U+064F)
    KSR = auto()            # كسر           — ِ (U+0650)
    SKN_GRP = auto()        # سكون          — ْ (U+0652)
    SHD_GRP = auto()        # شدة           — ّ (U+0651)
    TAN_FTH = auto()        # تنوين فتح     — ً (U+064B)
    TAN_DMM = auto()        # تنوين ضم      — ٌ (U+064C)
    TAN_KSR = auto()        # تنوين كسر     — ٍ (U+064D)
    ALF_KHNJ = auto()       # ألف خنجرية    — ٰ (U+0670)
    MDD_GRP = auto()        # مدة           — ٓ (U+0653)


class PhonFeature(Enum):
    """Minimal phonological features — السمات الدنيا (f in D_min).

    Each value is a unique power-of-two bit-position, enabling a compact
    integer bitmask: feature_mask = Σ 2^(f.value-1) for f in features.
    """
    # Manner of articulation (طريقة النطق)
    SHADID = auto()         # شديد   — stop / plosive
    RAKHW = auto()          # رخو    — fricative / continuant
    MURAKKAB = auto()       # مركب   — affricate
    MUTAWASSIT = auto()     # متوسط  — intermediate manner
    TAKRIR = auto()         # مكرر   — trill / vibrant
    MUNHARIF = auto()       # منحرف  — lateral
    TAFSHI = auto()         # تفشٍّ  — diffuse / spread
    # Voicing (الجهر والهمس)
    MAJHUR = auto()         # مجهور  — voiced
    MAHMOUS = auto()        # مهموس  — voiceless
    # Secondary articulation (الصفات الثانوية)
    ITBAQ = auto()          # مطبق   — pharyngealization / emphatic
    MSTALI = auto()         # مستعلٍ — dorsal elevation
    SAFIR = auto()          # صفيري  — sibilant / whistling
    ANFI = auto()           # أنفي   — nasal
    GHUNNA = auto()         # غنّي   — nasality / resonance
    LAYIN = auto()          # لين    — sonorant
    ASTTALA = auto()        # استطالة — prolongation (ض)
    HMZ = auto()            # همزي   — hamza-bearing
    # Vowel / nucleus features (الصوائت)
    NUWAWI = auto()         # نووي   — nuclear / syllabic
    QASIR = auto()          # قصير   — short vowel
    TAWIL = auto()          # طويل   — long vowel
    ITLAL = auto()          # اعتلال — defective / weak
    # Mark features (العلامات)
    SIFR_HARAKA = auto()    # صفر حركة — zero-vowel
    QAFIL = auto()          # قفل      — syllable closure
    TADFIF = auto()         # تضعيف   — gemination mark
    MD_KHAS = auto()        # مدّ خاص  — special extension mark


class PhonTransform(Enum):
    """Minimal transformations and functions — التحولات/الوظائف الدنيا (t in D_min).

    Each value is a unique power-of-two bit-position enabling a bitmask:
    transform_mask = Σ 2^(t.value-1) for t in transforms.
    """
    # Phonological processes (العمليات الصوتية)
    TAHQIQ = auto()             # تحقيق       — full realization
    TASHIL = auto()             # تسهيل       — facilitation / weakening
    IBDAL = auto()              # إبدال       — phonemic substitution
    HADHF = auto()              # حذف         — deletion / elision
    HAMLI_HAMZI = auto()        # حمل همزي    — hamza hosting
    IDGHAM = auto()             # إدغام       — assimilation / merging
    IDGHAM_SHAMSI = auto()      # إدغام شمسي  — solar (regressive) assimilation
    IZHAR_QAMARI = auto()       # إظهار قمري  — lunar clarity
    IZHAR = auto()              # إظهار       — clear articulation
    IKHFAA = auto()             # إخفاء       — nasalized concealment
    IQLAB = auto()              # إقلاب       — metamorphosis (ن → م before ب)
    TAFKHIM = auto()            # تفخيم       — velarization / emphasis
    TARQIQ = auto()             # ترقيق       — thinning / palatalization
    TAKRIR_TR = auto()          # تكرير       — trill articulation
    TAFSHI_TR = auto()          # تفشٍّ صوتي  — acoustic diffusion
    TAMATHUL = auto()           # تماثل       — progressive assimilation
    MADD = auto()               # مدّ         — vowel lengthening
    ITLAL_TR = auto()           # اعتلال      — weak-letter process
    ASTTALA_TR = auto()         # استطالة     — prolongation process
    # Morphological functions (الوظائف الصرفية)
    ASAL_JADHARI = auto()       # أصل جذري    — root-radical origin
    ZIYADA = auto()             # زيادة       — morphological augmentation
    BINA_SARFI = auto()         # بنية صرفية  — morphological structure
    BINA_ISHTIQAQI = auto()     # بناء اشتقاقي — derivational structure
    WAZIFA_SARFIYYA = auto()    # وظيفة صرفية — morphological function marker
    WAZN = auto()               # بناء وزني   — prosodic-pattern building
    # Syntactic / grammatical functions (الوظائف النحوية)
    TAAREF = auto()             # تعريف       — definiteness (لام التعريف)
    TAWKID = auto()             # توكيد       — emphasis marker
    TANWIN_FUNC = auto()        # تنوين       — nunation function
    JAZM = auto()               # جزم         — apocopation / jussive
    IIRAB = auto()              # إعراب       — grammatical case marking
    TANKIR = auto()             # تنكير       — indefiniteness
    JAM = auto()                # جمع         — pluralization marker
    ATAF = auto()               # عطف         — coordination marker
    NISBAH = auto()             # نسبة        — relational adjective marker
    MUTAKALLIM = auto()         # متكلم       — first-person marker
    DAMIR_FUNC = auto()         # هاء ضمير    — pronoun function
    TADFIF_TR = auto()          # تضعيف       — gemination function
    MAQTAA = auto()             # بناء مقطع مغلق — closed-syllable building
    HAMZA_CARRIER = auto()      # حامل كتابي  — orthographic hamza carrier


# ── Transition Engine — قانون الانتقال بين الخانات ──────────────────

class TransitionType(Enum):
    """الأنواع الكبرى للانتقال — the four major classes of cell transition."""
    FUNCTIONAL = auto()         # انتقال وظيفي    — same element, changed function
    RANK = auto()               # انتقال رتبي     — movement between phonetic tiers
    CONTEXTUAL = auto()         # انتقال تجاوري   — neighbour-driven transition
    MORPHO_STRUCTURAL = auto()  # انتقال بنيوي صرفي — pattern/template-driven


class TransitionLaw(Enum):
    """القوانين الجزئية للانتقال — the seven partial transition laws."""
    ITLAL = auto()      # اعتلال  — weak-letter transformation (ا و ي)
    IDGHAM = auto()     # إدغام   — gemination: C+C → Shadda
    IBDAL = auto()      # إبدال   — substitution within phonetic family
    HADHF = auto()      # حذف     — deletion from surface to deep structure
    WAQF = auto()       # وقف     — pause-final phonological reduction
    ZIYADA = auto()     # زيادة   — root element re-slotted as augment
    INZILAQ = auto()    # انزلاق  — glide ↔ long-vowel transition (و / ي)


class TransitionCondition(Enum):
    """شروط الانتقال — the five conditions required for a valid transition."""
    STRUCTURAL_VALIDITY = auto()    # بقاء داخل الأنماط المسموحة
    PHONETIC_BALANCE = auto()       # التخفيف دون الإفساد
    ROOT_PRESERVATION = auto()      # إمكان استرجاع الجذر بعد الانتقال
    FUNCTION_PRESERVATION = auto()  # وضوح الوظيفة بعد الانتقال
    NON_CONTRADICTION = auto()      # عدم الوقوع في صورة ممنوعة


class SyllablePosition(Enum):
    """موضع العنصر في المقطع — element's position inside the syllable."""
    ONSET = auto()      # بداية المقطع  — syllable onset (C)
    NUCLEUS = auto()    # نواة المقطع   — syllable nucleus (V)
    CODA = auto()       # نهاية المقطع  — syllable coda (C)
    INTER_WORD = auto() # حدّ الكلمة    — word boundary


class FunctionRole(Enum):
    """الدور الوظيفي للعنصر — element's morpho-syntactic role in the word."""
    ROOT_RADICAL = auto()   # أصل جذري   — part of the tri-literal root
    AUGMENT = auto()        # زيادة      — morphological augment
    VOWEL_CARRIER = auto()  # حامل صائتي — vowel / nucleus carrier
    CASE_MARKER = auto()    # علامة إعراب — case / mood marker
    DEFINITENESS = auto()   # أداة تعريف  — definiteness particle
    PRONOUN = auto()        # ضمير       — pronominal clitic
    UNKNOWN = auto()        # غير محدد   — undetermined


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
    PHONOLOGICAL = auto()    # صوتي
    MORPHOLOGICAL = auto()   # صرفي
    ORTHOGRAPHIC = auto()    # إملائي / وقفي
    CAUSAL = auto()          # سببي
    TEMPORAL = auto()        # زمني
    EXISTENTIAL = auto()     # وجودي
    ABSTRACTIVE = auto()     # تجريدي


class EvidenceType(Enum):
    """نوع الدليل — the kind of evidence supporting a transition record."""
    LEXICAL = auto()              # معجمي
    PATTERN = auto()              # نمطي / وزني
    PHONOLOGICAL_CONTEXT = auto() # سياق صوتي
    MORPH_CONTEXT = auto()        # سياق صرفي
    SURFACE_ONLY = auto()         # سطحي فقط
    DEEP_ANALYSIS = auto()        # تحليل عميق


class ReversibleValue(Enum):
    """قابلية الانتقال للعكس — whether a transition can be reversed."""
    YES = auto()         # قابل للعكس دائمًا
    NO = auto()          # غير قابل للعكس
    CONDITIONAL = auto() # قابل للعكس بشرط


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
