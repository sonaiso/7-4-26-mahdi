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
