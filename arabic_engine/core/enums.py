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


# ── AEU Periodic-Table enums ────────────────────────────────────────

class ElementClass(Enum):
    """تصنيف العنصر — structural class of an alphabetic encoding unit."""
    BASE_LETTER = auto()              # حرف أساسي
    VOWEL_MARKER = auto()             # علامة حركة
    STRUCTURAL_MARKER = auto()        # علامة بنيوية
    CARRIER_RELATED_UNIT = auto()     # وحدة مرتبطة بحامل
    COMPOSITE_DECISION_UNIT = auto()  # وحدة قرار مركبة


class ElementLayer(Enum):
    """طبقة العنصر — the architectural layer an AEU belongs to."""
    PHONOLOGICAL = auto()   # صوتية
    ORTHOGRAPHIC = auto()   # كتابية
    STRUCTURAL = auto()     # بنيوية
    MIXED = auto()          # مختلطة


class ElementFunction(Enum):
    """وظيفة العنصر — the functional role an AEU carries."""
    IDENTITY_BEARING = auto()        # حامل هوية
    MOTION_BEARING = auto()          # حامل حركة
    LENGTH_BEARING = auto()          # حامل طول
    CLOSURE_BEARING = auto()         # حامل إغلاق
    DUPLICATION_BEARING = auto()     # حامل تضعيف
    INDEFINITENESS_BEARING = auto()  # حامل تنكير
    ENCODING_BEARING = auto()        # حامل ترميز


class CombinationType(Enum):
    """نوع الاندماج — how an AEU combines with neighbours."""
    STANDALONE = auto()         # مستقل
    ATTACHES_TO_BASE = auto()   # يلتصق بالأساس
    CLUSTER_INTERNAL = auto()   # داخل عنقود
    CONTEXT_DEPENDENT = auto()  # معتمد على السياق


class UnicodeProfileType(Enum):
    """نوع الملف الموحد — Unicode rendering profile of an AEU."""
    SINGLE_CODE_POINT = auto()    # نقطة رمز واحدة
    COMBINING_MARK = auto()       # علامة تجميعية
    CONTEXTUAL_RENDERING = auto() # عرض سياقي


class ProofStatus(Enum):
    """حالة الإثبات — proof/verification status of an AEU."""
    PROVEN = auto()     # مُثبَت
    PENDING = auto()    # قيد الإثبات
    ASSUMED = auto()    # مفترض — accepted without formal proof
    COMPOSITE = auto()  # مُركَّب


# ── Axiom-layer enums (الأصول الخمسة) ────────────────────────────────

class SlotState(Enum):
    """حالة الموضع — state of a structural slot (A1/A2)."""
    EMPTY = auto()      # فارغ قابل للامتلاء
    OCCUPIED = auto()   # مشغول بموجب أول
    BLOCKED = auto()    # محجوب بنيويًا


class OntologicalLayer(Enum):
    """الطبقة الوجودية — ontological rank for layer promotion (A4).

    Encodes the hierarchy: cell → transition → syllable → root → pattern.
    Each level requires the previous to be complete before promotion.
    """
    CELL = auto()        # خانة — atomic phonological cell
    TRANSITION = auto()  # انتقال — directed transition between cells
    SYLLABLE = auto()    # مقطع — syllable-level grouping
    ROOT = auto()        # جذر — root-level abstraction
    PATTERN = auto()     # وزن — morphological pattern


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
    SLOT = auto()        # موضع — structural position (Structural Zero)
    UNIT = auto()        # وحدة — base unit (consonant / letter)
    MODIFIER = auto()    # محمول — modifier (short vowel, sukun, shadda)
    COMPOSITE = auto()   # تركيب — composite (syllable, morpheme)
    STRUCTURE = auto()   # بنية — structural template (root, pattern)
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
    DISTINCTIVE = auto()    # تمييزي — سابق / مركز / لاحق
    HIERARCHICAL = auto()   # رتبي — قمة / ضلع / ضلع
    GENERATIVE = auto()     # توليدي — قاعدة / حركة / قيد


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
    PHONOLOGICAL = auto()   # دال صوتي
    MORPHOLOGICAL = auto()  # دال صرفي
    LEXICAL = auto()        # دال معجمي
    SYNTACTIC = auto()      # دال نحوي
    TEXTUAL = auto()        # دال نصي
    PRAGMATIC = auto()      # دال تداولي
    RHETORICAL = auto()     # دال بلاغي
    UTTERED_FORM = auto()   # منطوق — sub-class of signifier


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
    PHONETIC_UTTERANCE = auto()    # أداء صوتي
    WORD_UTTERANCE = auto()        # كلمة منطوقة
    EXPRESSION_UTTERANCE = auto()  # تركيب منطوق
    SENTENCE_UTTERANCE = auto()    # جملة قضوية
    MARKED_UTTERANCE = auto()      # منطوق مقيد بأداة


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
    ONTOLOGICAL = auto()            # مدلول وجودي
    PROPERTY = auto()               # مدلول وصفي
    EVENT = auto()                  # مدلول حدثي
    RELATIONAL = auto()             # مدلول علائقي
    PROPOSITIONAL = auto()          # مدلول حكمي
    REFERENTIAL = auto()            # مدلول إحالي
    FUNCTIONAL = auto()             # مدلول وظيفي
    PRAGMATIC_SIGNIFIED = auto()    # مدلول تداولي
    LOGICAL = auto()                # مدلول منطقي
    RHETORICAL_SIGNIFIED = auto()   # مدلول بلاغي
    EPISTEMIC = auto()              # مدلول معرفي
    NORMATIVE = auto()              # مدلول معياري
    AFFECTIVE = auto()              # مدلول وجداني
    MODAL = auto()                  # مدلول إمكاني/ضروري
    INSTITUTIONAL = auto()          # مدلول مؤسسي
    EMBODIED = auto()               # مدلول إدراكي متجسّد
    SELF_MODEL = auto()             # مدلول ذاتي هوياتي
    FRAME = auto()                  # مدلول إطاري
    SCRIPT = auto()                 # مدلول سيناريوي
    CAUSAL_EXPLANATORY = auto()     # مدلول سببي تفسيري
    META_CONCEPTUAL = auto()        # مدلول فوق-مفهومي
    CONCEPTUAL = auto()             # مفهوم — root for conceptual sub-class


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
    ENTITY_CONCEPT = auto()    # مفهوم ذات
    PROPERTY_CONCEPT = auto()  # مفهوم صفة
    EVENT_CONCEPT = auto()     # مفهوم حدث
    RELATION_CONCEPT = auto()  # مفهوم علاقة
    NORM_CONCEPT = auto()      # مفهوم معياري
    MENTAL_CONCEPT = auto()    # مفهوم ذهني
    ABSTRACT_CONCEPT = auto()  # مفهوم تجريدي
    META_CONCEPT = auto()      # مفهوم عن مفهوم


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
    DIRECT = auto()               # مباشر
    POLYSEMOUS = auto()           # متعدد الاحتمال
    COMPOSITIONAL = auto()        # تركيبي
    HIERARCHICAL = auto()         # طبقي
    CONTEXTUAL = auto()           # سياقي
    INFERENTIAL = auto()          # استلزامي
    FIGURATIVE = auto()           # مجازي
    PERFORMATIVE = auto()         # إنجازي
    FUNCTIONAL_COUPLING = auto()  # وظيفي بنائي
    REFERENTIAL_COUPLING = auto() # إحالي


class OntologicalConstraintType(Enum):
    """نوع القيد الأنطولوجي — constraint kind in the Ontology v1 model.

    Each constraint guards a different layer of the signifier→signified
    transition.  More specific than the classical ``ConstraintType`` (which
    covers only the five Mafhūm constraint kinds).

    ==========================  ================================================
    Member                       Description
    ==========================  ================================================
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
    STRUCTURAL = auto()                  # قيد بنيوي
    PHONOLOGICAL_CONSTRAINT = auto()     # قيد صوتي
    MORPHOLOGICAL_CONSTRAINT = auto()    # قيد صرفي
    LEXICAL_CONSTRAINT = auto()          # قيد معجمي
    SYNTACTIC_CONSTRAINT = auto()        # قيد نحوي
    REFERENTIAL_CONSTRAINT = auto()      # قيد إحالي
    CONTEXTUAL_CONSTRAINT = auto()       # قيد سياقي
    PRAGMATIC_CONSTRAINT = auto()        # قيد تداولي
    LOGICAL_CONSTRAINT = auto()          # قيد منطقي
    RHETORICAL_CONSTRAINT = auto()       # قيد بلاغي
    EPISTEMIC_CONSTRAINT = auto()        # قيد معرفي
    INSTITUTIONAL_CONSTRAINT = auto()    # قيد مؤسسي
    INTERPRETIVE_CONSTRAINT = auto()     # قيد تفسيري


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
    SURFACE_VALIDITY = auto()           # صحة البنية السطحية
    LEXICAL_ACCESS = auto()             # وجود مدخل معجمي
    CONTEXT_RESOLUTION = auto()         # كفاية السياق
    CONCEPT_SELECTION = auto()          # اختيار المفهوم الصحيح
    FIGURATIVE_DISAMBIGUATION = auto()  # وجود قرينة مجازية
    REFERENTIAL_RESOLUTION = auto()     # توفر المرجع الإحالي
    LOGICAL_COHERENCE = auto()          # تسق التفسير مع البنية


# ══════════════════════════════════════════════════════════════════════
# Knowledge Episode — طبقة الخبرة المعرفية
# ══════════════════════════════════════════════════════════════════════

class EpistemicRank(Enum):
    """الرتبة الإبستيمية — the epistemic status of a validated knowledge episode.

    ============================  ==============================================
    Member                         Arabic meaning
    ============================  ==============================================
    CERTAIN                        قطعي — all conditions met, existence judgement
    TRUE_NON_CERTAIN               صحيح غير قطعي — valid but revisable
    PROBABILISTIC_DOUBT            ظني — probable but not certain
    IMPOSSIBLE                     ممتنع — internally contradictory or method mismatch
    REJECTED_METHODOLOGICALLY      ساقط من أصل المنهج — fatal anchor/sense/prior missing
    ============================  ==============================================
    """
    CERTAIN = auto()                    # قطعي
    TRUE_NON_CERTAIN = auto()           # صحيح غير قطعي
    PROBABILISTIC_DOUBT = auto()        # ظني
    IMPOSSIBLE = auto()                 # ممتنع
    REJECTED_METHODOLOGICALLY = auto()  # ساقط من أصل المنهج


class ValidationState(Enum):
    """حالة صحة الخبرة المعرفية — lifecycle state of a KnowledgeEpisode."""
    PENDING = auto()   # pending — not yet validated
    VALID = auto()     # valid — all checks passed
    INVALID = auto()   # invalid — one or more checks failed


class JudgementType(Enum):
    """نوع الحكم — the category of judgement issued by a KnowledgeEpisode.

    ====================  ================================================
    Member                 Arabic meaning
    ====================  ================================================
    EXISTENCE              وجود — the episode asserts that something exists
    ESSENCE                حقيقة — the episode describes the nature of a thing
    ATTRIBUTE              صفة — the episode attributes a property
    RELATION               علاقة — the episode relates two things
    CAUSAL                 سببي — the episode asserts a causal link
    INTERPRETIVE           تفسيري — the episode interprets a text / utterance
    FORMAL                 صوري — the episode proves a formal/logical claim
    NORMATIVE              معياري — the episode makes a normative claim
    PURE_LINGUISTIC        لغوي بحت — purely linguistic / grammatical claim
    METAPHYSICAL           ميتافيزيقي — beyond empirical verification
    ====================  ================================================
    """
    EXISTENCE = auto()       # وجود
    ESSENCE = auto()         # حقيقة
    ATTRIBUTE = auto()       # صفة
    RELATION = auto()        # علاقة
    CAUSAL = auto()          # سببي
    INTERPRETIVE = auto()    # تفسيري
    FORMAL = auto()          # صوري
    NORMATIVE = auto()       # معياري
    PURE_LINGUISTIC = auto() # لغوي بحت
    METAPHYSICAL = auto()    # ميتافيزيقي


class MethodFamily(Enum):
    """عائلة المنهج — the broad family of epistemological method.

    ===========  ======================================================
    Member        Arabic meaning
    ===========  ======================================================
    RATIONAL      عقلي — general rational / logical reasoning
    SCIENTIFIC    علمي — empirical scientific method
    LINGUISTIC    لغوي — utterance / concept linguistic analysis
    MATHEMATICAL  رياضي — formal symbolic proof
    PHYSICAL      فيزيائي — physical law and measurement
    ===========  ======================================================
    """
    RATIONAL = auto()      # عقلي
    SCIENTIFIC = auto()    # علمي
    LINGUISTIC = auto()    # لغوي
    MATHEMATICAL = auto()  # رياضي
    PHYSICAL = auto()      # فيزيائي


class CarrierClass(Enum):
    """صنف الحامل اللغوي — whether the linguistic carrier is an utterance, concept, or both.

    The طبقة النقل اللغوي admits only two primitive carriers:
    UTTERANCE (المنطوق) and CONCEPT (المفهوم).  BOTH signals that the
    episode carries both at once (the common case for interpreted texts).
    """
    UTTERANCE = auto()  # منطوق فقط
    CONCEPT = auto()    # مفهوم فقط
    BOTH = auto()       # كلاهما


class SenseModality(Enum):
    """حاسة الأثر الحسي — the sensory channel through which reality is perceived."""
    VISION = auto()    # بصر
    HEARING = auto()   # سمع
    TOUCH = auto()     # لمس
    TASTE = auto()     # ذوق
    SMELL = auto()     # شم
    INTERNAL = auto()  # حس داخلي (وجداني / عقلي)


class RealityKind(Enum):
    """نوع الواقع — the ontological category of the reality anchor.

    ====================  ===================================
    Member                 Arabic meaning
    ====================  ===================================
    PHYSICAL_OBJECT        جسم مادي
    EVENT                  حدث
    RELATION               علاقة قائمة
    TEXT_OBJECT            نص / خطاب
    MENTAL_STATE           حالة ذهنية
    FORMAL_STRUCTURE       بنية صورية (رياضية أو منطقية)
    ====================  ===================================
    """
    PHYSICAL_OBJECT = auto()   # جسم مادي
    EVENT = auto()             # حدث
    RELATION = auto()          # علاقة
    TEXT_OBJECT = auto()       # نص / خطاب
    MENTAL_STATE = auto()      # حالة ذهنية
    FORMAL_STRUCTURE = auto()  # بنية صورية


class TraceMode(Enum):
    """طريقة أخذ الأثر الحسي — how the sense trace was obtained."""
    DIRECT_PERCEPTION = auto()  # مشاهدة مباشرة
    MEDIATED = auto()           # بواسطة
    REPORTED = auto()           # منقول
    INFERRED = auto()           # مستنبط


class TraceQuality(Enum):
    """جودة الأثر الحسي — reliability of the sense trace."""
    STRONG = auto()    # قوي
    MODERATE = auto()  # متوسط
    WEAK = auto()      # ضعيف


class InfoKind(Enum):
    """نوع المعلومة السابقة — the category of prior information.

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
    LEXICAL = auto()          # معجمي
    LINGUISTIC_RULE = auto()  # قاعدة لغوية
    EMPIRICAL = auto()        # تجريبي
    LOGICAL = auto()          # منطقي
    FORMAL = auto()           # صوري
    ANALOGICAL = auto()       # قياسي


class LinkKind(Enum):
    """نوع الربط — the kind of inferential link used in a LinkingTrace."""
    TEXTUAL_INFERENCE = auto()   # استنباط نصي
    LOGICAL_DEDUCTION = auto()   # استنتاج منطقي
    ANALOGICAL = auto()          # قياس
    CAUSAL = auto()              # ربط سببي
    EMPIRICAL = auto()           # استقراء تجريبي


class ContaminationLevel(Enum):
    """مستوى التلوث بالرأي السابق — degree to which prior opinion contaminates the episode."""
    NONE = auto()    # لا تلوث
    LOW = auto()     # تلوث خفيف
    MEDIUM = auto()  # تلوث متوسط
    HIGH = auto()    # تلوث عالٍ


class GapSeverity(Enum):
    """حدة الفجوة المعرفية — severity level of a detected knowledge gap."""
    FATAL = auto()   # قاتل — causes REJECTED_METHODOLOGICALLY
    HIGH = auto()    # عالٍ
    MEDIUM = auto()  # متوسط


class PathKind(Enum):
    """نوع مسار الإثبات — the nature of the proof path.

    =========  ===============================================
    Member      Arabic meaning
    =========  ===============================================
    HISSI       حسي — direct sensory evidence
    AQLI        عقلي — rational / logical proof
    LINGUISTIC  لغوي — linguistic / textual evidence
    FORMAL      صوري — formal mathematical / logical proof
    =========  ===============================================
    """
    HISSI = auto()      # حسي
    AQLI = auto()       # عقلي
    LINGUISTIC = auto() # لغوي
    FORMAL = auto()     # صوري
