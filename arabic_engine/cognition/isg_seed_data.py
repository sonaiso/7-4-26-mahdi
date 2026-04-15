"""ISG seed data — البذرة: bootstrap thresholds and rules for ISG governance.

This module defines the default governance thresholds (θ₀, θ₁, θ₂) from
المادة 75–77, the default conflict priority order (المادة 47), and the
readiness criteria (المادة 51).

Usage::

    from arabic_engine.cognition.isg_seed_data import (
        DEFAULT_GOVERNANCE_THRESHOLDS,
        DEFAULT_CONFLICT_PRIORITY_ORDER,
        DEFAULT_READINESS_CRITERIA,
    )
"""

from __future__ import annotations

# ── Governance thresholds (المادة 74–78) ──────────────────────────────

#: θ₀ — minimum validation score for atom to be eligible for interpretation
#: θ₁ — minimum callability score for atom to be summoned
#: θ₂ — minimum entry score for atom to cross into the lexeme system
DEFAULT_GOVERNANCE_THRESHOLDS: dict[str, float] = {
    "theta_0": 0.5,   # Valid_0 ≥ θ₀ → atom eligible (المادة 75)
    "theta_1": 0.6,   # Callable ≥ θ₁ → atom may be summoned (المادة 76)
    "theta_2": 0.7,   # Entry_Lexeme ≥ θ₂ → atom crosses to lexeme (المادة 77)
    "min_trust_degree": 0.3,  # Minimum trust for source acceptance
    "min_context_fit": 0.2,   # Minimum context fit for callability
}

# ── Default conflict priority order (المادة 47) ──────────────────────

#: Priority order for resolving internal conflicts, from highest to lowest.
DEFAULT_CONFLICT_PRIORITY_ORDER: str = (
    "ConfirmationRank > Domain > InputRelevance > Context > RuleRank "
    "> Specialisation > Suspend"
)

# ── Readiness criteria (المادة 51) ───────────────────────────────────

#: The 9 elements that must be satisfied for the first readiness level.
DEFAULT_READINESS_CRITERIA: tuple[str, ...] = (
    "input_normalisation",          # تطبيع المدخل
    "stock_recall",                 # استدعاء مخزون مناسب
    "initial_type_assignment",      # تعيين النوع الأولي
    "domain_assignment",            # تعيين المجال
    "context_assignment",           # تعيين السياق
    "transfer_test",                # اختبار النقل/الحقيقة/العرف
    "ambiguity_test",               # اختبار الاشتراك والإبهام
    "initial_meaning_assignment",   # تعيين الدلالة الأولية
    "continuation_eligibility",     # تعيين صلاحية الاستمرار
)
