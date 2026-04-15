"""Tests for Prior Informational Stock Proof v1.

Validates:
  * All 7 new enums are complete (correct member counts).
  * StockEntry and PriorInformationalStock creation and frozenness.
  * evaluate_stock_sufficiency — empty / partial / full stock.
  * evaluate_perceptual_readiness — Ready₁ with/without stock.
  * evaluate_compositional_readiness — Ready₂ prerequisite + scoring.
  * evaluate_propositional_readiness — Ready₃ prerequisite + scoring.
  * build_informational_stock_record — full pipeline integration.
  * batch_evaluate — parallel processing.
  * Readiness ordering — constitutional ordering from Article 21.
  * FractalStage enum completeness.
  * Re-exports from arabic_engine.core.
"""

from __future__ import annotations

import pytest

from arabic_engine.cognition.prior_info_stock_v1 import (
    batch_evaluate,
    build_informational_stock_record,
    evaluate_compositional_readiness,
    evaluate_perceptual_readiness,
    evaluate_propositional_readiness,
    evaluate_stock_sufficiency,
)
from arabic_engine.core.enums import (
    FractalStage,
    InterpretationSource,
    PerceptualGapReason,
    ReadinessLevel,
    ReadinessStatus,
    StockComponent,
    StockSufficiency,
)
from arabic_engine.core.types import (
    CompositionalReadinessResult,
    InformationalStockRecord,
    PerceptualReadinessResult,
    PriorInformationalStock,
    ReadinessGate,
    StockEntry,
)

# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════


def _entry(
    component: StockComponent,
    content: str = "test",
    source: InterpretationSource = InterpretationSource.REALITY,
    weight: float = 1.0,
    entry_id: str = "",
) -> StockEntry:
    eid = entry_id or f"E_{component.name}"
    return StockEntry(
        entry_id=eid,
        component=component,
        content=content,
        source=source,
        weight=weight,
    )


def _full_stock(stock_id: str = "STK_FULL") -> PriorInformationalStock:
    """Build a stock with all 7 components represented."""
    entries = tuple(
        _entry(
            comp,
            content=f"info for {comp.name}",
            source=(
                InterpretationSource.UTTERANCE
                if comp == StockComponent.PRIMARY_LANGUAGE
                else InterpretationSource.REALITY
            ),
        )
        for comp in StockComponent
    )
    return PriorInformationalStock(stock_id=stock_id, entries=entries)


def _empty_stock(stock_id: str = "STK_EMPTY") -> PriorInformationalStock:
    return PriorInformationalStock(stock_id=stock_id, entries=())


def _partial_stock(
    components: list[StockComponent],
    stock_id: str = "STK_PARTIAL",
) -> PriorInformationalStock:
    entries = tuple(
        _entry(
            comp,
            source=(
                InterpretationSource.UTTERANCE
                if comp == StockComponent.PRIMARY_LANGUAGE
                else InterpretationSource.REALITY
            ),
        )
        for comp in components
    )
    return PriorInformationalStock(stock_id=stock_id, entries=entries)


# ═══════════════════════════════════════════════════════════════════════
# 1. Enum completeness
# ═══════════════════════════════════════════════════════════════════════


class TestEnumCompleteness:
    """Verify all 7 new enums have expected member counts."""

    def test_stock_component_count(self) -> None:
        assert len(StockComponent) == 7

    def test_stock_component_members(self) -> None:
        names = {m.name for m in StockComponent}
        assert "REALITY_INFO" in names
        assert "PRIOR_CLASSIFICATION" in names
        assert "PRIMARY_LANGUAGE" in names
        assert "CATEGORY_BOUNDARY" in names
        assert "REFERENCE_KNOWLEDGE" in names
        assert "PREDICATION_CRITERION" in names
        assert "USAGE_MODE_CRITERION" in names

    def test_readiness_level_count(self) -> None:
        assert len(ReadinessLevel) == 3

    def test_readiness_level_members(self) -> None:
        names = {m.name for m in ReadinessLevel}
        assert names == {"PERCEPTUAL", "COMPOSITIONAL", "PROPOSITIONAL"}

    def test_readiness_status_count(self) -> None:
        assert len(ReadinessStatus) == 3

    def test_readiness_status_members(self) -> None:
        names = {m.name for m in ReadinessStatus}
        assert names == {"MET", "UNMET", "PARTIAL"}

    def test_perceptual_gap_reason_count(self) -> None:
        assert len(PerceptualGapReason) == 4

    def test_perceptual_gap_reason_members(self) -> None:
        names = {m.name for m in PerceptualGapReason}
        assert names == {"AMBIGUOUS", "POLYSEMOUS", "UNCLASSIFIED", "UNFIT_FOR_COMPOSITION"}

    def test_interpretation_source_count(self) -> None:
        assert len(InterpretationSource) == 7

    def test_interpretation_source_members(self) -> None:
        names = {m.name for m in InterpretationSource}
        expected = {
            "REALITY", "UTTERANCE", "CONCEPT", "REFERENCE",
            "ROLE", "TRUTH_OR_TRANSFER", "CONVENTION",
        }
        assert names == expected

    def test_fractal_stage_count(self) -> None:
        assert len(FractalStage) == 6

    def test_fractal_stage_members(self) -> None:
        names = {m.name for m in FractalStage}
        expected = {
            "DESIGNATION", "PRESERVATION", "LINKING",
            "JUDGMENT", "TRANSITION", "RETURN",
        }
        assert names == expected

    def test_stock_sufficiency_count(self) -> None:
        assert len(StockSufficiency) == 3

    def test_stock_sufficiency_members(self) -> None:
        names = {m.name for m in StockSufficiency}
        assert names == {"SUFFICIENT", "INSUFFICIENT", "UNDETERMINED"}


# ═══════════════════════════════════════════════════════════════════════
# 2. StockEntry / PriorInformationalStock records
# ═══════════════════════════════════════════════════════════════════════


class TestStockEntryRecord:
    """Test StockEntry and PriorInformationalStock creation and frozenness."""

    def test_stock_entry_creation(self) -> None:
        e = _entry(StockComponent.REALITY_INFO, content="world fact")
        assert e.component == StockComponent.REALITY_INFO
        assert e.content == "world fact"
        assert e.weight == 1.0

    def test_stock_entry_frozen(self) -> None:
        e = _entry(StockComponent.REALITY_INFO)
        with pytest.raises(AttributeError):
            e.content = "changed"  # type: ignore[misc]

    def test_stock_entry_custom_weight(self) -> None:
        e = _entry(StockComponent.PRIMARY_LANGUAGE, weight=0.8)
        assert e.weight == 0.8

    def test_prior_informational_stock_creation(self) -> None:
        stock = _full_stock()
        assert stock.stock_id == "STK_FULL"
        assert len(stock.entries) == 7
        assert stock.sufficiency == StockSufficiency.UNDETERMINED

    def test_prior_informational_stock_frozen(self) -> None:
        stock = _full_stock()
        with pytest.raises(AttributeError):
            stock.stock_id = "changed"  # type: ignore[misc]

    def test_empty_stock(self) -> None:
        stock = _empty_stock()
        assert len(stock.entries) == 0


# ═══════════════════════════════════════════════════════════════════════
# 3. evaluate_stock_sufficiency
# ═══════════════════════════════════════════════════════════════════════


class TestEvaluateStockSufficiency:
    """Test stock sufficiency evaluation."""

    def test_empty_stock_insufficient(self) -> None:
        stock = _empty_stock()
        assert evaluate_stock_sufficiency(stock) == StockSufficiency.INSUFFICIENT

    def test_full_stock_sufficient(self) -> None:
        stock = _full_stock()
        assert evaluate_stock_sufficiency(stock) == StockSufficiency.SUFFICIENT

    def test_partial_stock_missing_extension(self) -> None:
        # Missing REALITY_INFO (required for extension)
        stock = _partial_stock([
            StockComponent.PRIOR_CLASSIFICATION,
            StockComponent.PRIMARY_LANGUAGE,
            StockComponent.CATEGORY_BOUNDARY,
        ])
        assert evaluate_stock_sufficiency(stock) == StockSufficiency.INSUFFICIENT

    def test_partial_stock_missing_constituent(self) -> None:
        # Has extension requirements but missing PRIOR_CLASSIFICATION
        stock = _partial_stock([
            StockComponent.REALITY_INFO,
            StockComponent.PRIMARY_LANGUAGE,
            StockComponent.REFERENCE_KNOWLEDGE,
            StockComponent.PREDICATION_CRITERION,
            StockComponent.USAGE_MODE_CRITERION,
        ])
        assert evaluate_stock_sufficiency(stock) == StockSufficiency.INSUFFICIENT

    def test_partial_stock_undetermined(self) -> None:
        # Has extension + constituent requirements but not all 7
        stock = _partial_stock([
            StockComponent.REALITY_INFO,
            StockComponent.PRIMARY_LANGUAGE,
            StockComponent.REFERENCE_KNOWLEDGE,
            StockComponent.PREDICATION_CRITERION,
            StockComponent.PRIOR_CLASSIFICATION,
            StockComponent.CATEGORY_BOUNDARY,
        ])
        assert evaluate_stock_sufficiency(stock) == StockSufficiency.UNDETERMINED


# ═══════════════════════════════════════════════════════════════════════
# 4. evaluate_perceptual_readiness
# ═══════════════════════════════════════════════════════════════════════


class TestPerceptualReadiness:
    """Test perceptual readiness (Ready₁) evaluation."""

    def test_full_stock_met(self) -> None:
        stock = _full_stock()
        result = evaluate_perceptual_readiness("P001", stock)
        assert result.gate.status == ReadinessStatus.MET
        assert result.gate.level == ReadinessLevel.PERCEPTUAL
        assert result.gate.score >= result.gate.threshold
        assert result.interpreted_concept is not None

    def test_empty_stock_unmet(self) -> None:
        stock = _empty_stock()
        result = evaluate_perceptual_readiness("P002", stock)
        assert result.gate.status == ReadinessStatus.UNMET
        assert result.gate.score == 0.0
        assert result.interpreted_concept is None
        assert len(result.gate.gap_reasons) > 0

    def test_partial_stock_with_gaps(self) -> None:
        # Only has REALITY_INFO, missing language/classification/boundary
        stock = _partial_stock([StockComponent.REALITY_INFO])
        result = evaluate_perceptual_readiness("P003", stock)
        assert result.gate.status == ReadinessStatus.UNMET
        assert result.interpreted_concept is None

    def test_high_threshold_not_met(self) -> None:
        stock = _partial_stock([
            StockComponent.REALITY_INFO,
            StockComponent.PRIMARY_LANGUAGE,
        ])
        result = evaluate_perceptual_readiness("P004", stock, threshold=0.9)
        assert result.gate.status == ReadinessStatus.UNMET

    def test_low_threshold_partial(self) -> None:
        # Two components → ~2/7 coverage, but gaps present → PARTIAL
        stock = _partial_stock([
            StockComponent.REALITY_INFO,
            StockComponent.PRIMARY_LANGUAGE,
        ])
        result = evaluate_perceptual_readiness("P005", stock, threshold=0.2)
        # Has score above threshold but still has gaps
        assert result.gate.status == ReadinessStatus.PARTIAL

    def test_percept_id_preserved(self) -> None:
        stock = _full_stock()
        result = evaluate_perceptual_readiness("MY_PERCEPT", stock)
        assert result.percept_id == "MY_PERCEPT"


# ═══════════════════════════════════════════════════════════════════════
# 5. evaluate_compositional_readiness
# ═══════════════════════════════════════════════════════════════════════


class TestCompositionalReadiness:
    """Test compositional readiness (Ready₂) evaluation."""

    def test_ready1_met_with_ref_and_role(self) -> None:
        stock = _full_stock()
        r1 = evaluate_perceptual_readiness("P010", stock)
        r2 = evaluate_compositional_readiness("P010", r1, "REF_001", "AGENT")
        assert r2.gate.status == ReadinessStatus.MET
        assert r2.gate.level == ReadinessLevel.COMPOSITIONAL
        assert r2.assigned_role == "AGENT"
        assert r2.reference_resolved is True

    def test_ready1_unmet_blocks_ready2(self) -> None:
        stock = _empty_stock()
        r1 = evaluate_perceptual_readiness("P011", stock)
        r2 = evaluate_compositional_readiness("P011", r1, "REF_001", "AGENT")
        assert r2.gate.status == ReadinessStatus.UNMET
        assert r2.gate.score == 0.0
        assert "Ready₁" in r2.gate.gap_reasons[0]

    def test_missing_reference(self) -> None:
        stock = _full_stock()
        r1 = evaluate_perceptual_readiness("P012", stock)
        r2 = evaluate_compositional_readiness("P012", r1, "", "AGENT")
        assert r2.reference_resolved is False
        assert any("reference" in reason for reason in r2.gate.gap_reasons)

    def test_missing_role(self) -> None:
        stock = _full_stock()
        r1 = evaluate_perceptual_readiness("P013", stock)
        r2 = evaluate_compositional_readiness("P013", r1, "REF_001", "")
        assert r2.assigned_role is None
        assert any("role" in reason for reason in r2.gate.gap_reasons)

    def test_percept_id_propagated(self) -> None:
        stock = _full_stock()
        r1 = evaluate_perceptual_readiness("P014", stock)
        r2 = evaluate_compositional_readiness("P014", r1, "R", "ROLE")
        assert r2.percept_id == "P014"


# ═══════════════════════════════════════════════════════════════════════
# 6. evaluate_propositional_readiness
# ═══════════════════════════════════════════════════════════════════════


class TestPropositionalReadiness:
    """Test propositional readiness (Ready₃) evaluation."""

    def test_all_conditions_met(self) -> None:
        stock = _full_stock()
        r1 = evaluate_perceptual_readiness("P020", stock)
        r2 = evaluate_compositional_readiness("P020", r1, "REF", "AGENT")
        r3 = evaluate_propositional_readiness(r2, True, True)
        assert r3.status == ReadinessStatus.MET
        assert r3.level == ReadinessLevel.PROPOSITIONAL
        assert r3.score >= r3.threshold

    def test_ready2_unmet_blocks_ready3(self) -> None:
        stock = _empty_stock()
        r1 = evaluate_perceptual_readiness("P021", stock)
        r2 = evaluate_compositional_readiness("P021", r1, "", "")
        r3 = evaluate_propositional_readiness(r2, True, True)
        assert r3.status == ReadinessStatus.UNMET
        assert r3.score == 0.0
        assert "Ready₂" in r3.gap_reasons[0]

    def test_predicate_not_closed(self) -> None:
        stock = _full_stock()
        r1 = evaluate_perceptual_readiness("P022", stock)
        r2 = evaluate_compositional_readiness("P022", r1, "REF", "AGENT")
        r3 = evaluate_propositional_readiness(r2, False, True)
        assert r3.status != ReadinessStatus.MET
        assert any("predicate" in reason for reason in r3.gap_reasons)

    def test_conflict_not_resolved(self) -> None:
        stock = _full_stock()
        r1 = evaluate_perceptual_readiness("P023", stock)
        r2 = evaluate_compositional_readiness("P023", r1, "REF", "AGENT")
        r3 = evaluate_propositional_readiness(r2, True, False)
        assert r3.status != ReadinessStatus.MET
        assert any("conflict" in reason for reason in r3.gap_reasons)

    def test_neither_closed_nor_resolved(self) -> None:
        stock = _full_stock()
        r1 = evaluate_perceptual_readiness("P024", stock)
        r2 = evaluate_compositional_readiness("P024", r1, "REF", "AGENT")
        r3 = evaluate_propositional_readiness(r2, False, False)
        assert r3.status != ReadinessStatus.MET


# ═══════════════════════════════════════════════════════════════════════
# 7. build_informational_stock_record
# ═══════════════════════════════════════════════════════════════════════


class TestBuildInformationalStockRecord:
    """Test full pipeline integration via build_informational_stock_record."""

    def test_full_pipeline_all_met(self) -> None:
        stock = _full_stock()
        record = build_informational_stock_record(
            "P030", stock, "noun", "subject", "REF", "AGENT",
            predicate_closed=True, conflict_resolved=True,
        )
        assert isinstance(record, InformationalStockRecord)
        assert record.percept_id == "P030"
        assert record.stock is stock
        assert record.classification == "noun"
        assert record.linguistic_direction == "subject"
        assert record.reference == "REF"
        assert record.candidate_role == "AGENT"
        assert record.ready_1.level == ReadinessLevel.PERCEPTUAL
        assert record.ready_2.level == ReadinessLevel.COMPOSITIONAL
        assert record.ready_3.level == ReadinessLevel.PROPOSITIONAL

    def test_all_three_gates_met(self) -> None:
        stock = _full_stock()
        record = build_informational_stock_record(
            "P031", stock, "noun", "subject", "REF", "AGENT",
            predicate_closed=True, conflict_resolved=True,
        )
        assert record.ready_1.status == ReadinessStatus.MET
        assert record.ready_2.status == ReadinessStatus.MET
        assert record.ready_3.status == ReadinessStatus.MET

    def test_empty_stock_all_unmet(self) -> None:
        stock = _empty_stock()
        record = build_informational_stock_record(
            "P032", stock, "?", "?", "?", "?",
            predicate_closed=True, conflict_resolved=True,
        )
        assert record.ready_1.status == ReadinessStatus.UNMET
        assert record.ready_2.status == ReadinessStatus.UNMET
        assert record.ready_3.status == ReadinessStatus.UNMET

    def test_auto_generated_id(self) -> None:
        stock = _full_stock()
        record = build_informational_stock_record(
            "P033", stock, "cl", "ln", "ref", "role",
        )
        assert record.record_id.startswith("IS_")

    def test_custom_id(self) -> None:
        stock = _full_stock()
        record = build_informational_stock_record(
            "P034", stock, "cl", "ln", "ref", "role",
            record_id="CUSTOM_001",
        )
        assert record.record_id == "CUSTOM_001"

    def test_nine_tuple_structure(self) -> None:
        """Verify the record has all 9 IS-tuple fields."""
        stock = _full_stock()
        record = build_informational_stock_record(
            "X", stock, "Cl", "Ln", "Ref", "Role",
            predicate_closed=True, conflict_resolved=True,
        )
        # IS = (X, K, Cl, Ln, Ref, Role, Ready₁, Ready₂, Ready₃)
        assert record.percept_id == "X"
        assert record.stock == stock
        assert record.classification == "Cl"
        assert record.linguistic_direction == "Ln"
        assert record.reference == "Ref"
        assert record.candidate_role == "Role"
        assert isinstance(record.ready_1, ReadinessGate)
        assert isinstance(record.ready_2, ReadinessGate)
        assert isinstance(record.ready_3, ReadinessGate)


# ═══════════════════════════════════════════════════════════════════════
# 8. batch_evaluate
# ═══════════════════════════════════════════════════════════════════════


class TestBatchEvaluate:
    """Test batch processing."""

    def test_multiple_inputs(self) -> None:
        stock = _full_stock()
        inputs = [
            ("P040", stock, "n", "s", "R", "A", True, True),
            ("P041", stock, "v", "p", "R2", "B", False, False),
        ]
        results = batch_evaluate(inputs)
        assert len(results) == 2
        assert results[0].percept_id == "P040"
        assert results[1].percept_id == "P041"

    def test_empty_list(self) -> None:
        results = batch_evaluate([])
        assert results == []

    def test_single_input(self) -> None:
        stock = _full_stock()
        inputs = [("P042", stock, "cl", "ln", "ref", "role", True, True)]
        results = batch_evaluate(inputs)
        assert len(results) == 1
        assert results[0].ready_1.status == ReadinessStatus.MET


# ═══════════════════════════════════════════════════════════════════════
# 9. Readiness ordering (Article 21)
# ═══════════════════════════════════════════════════════════════════════


class TestReadinessOrdering:
    """Validate constitutional ordering: Ready₁ → Ready₂ → Ready₃."""

    def test_cannot_have_ready2_met_without_ready1_met(self) -> None:
        """Ready₂ cannot be MET if Ready₁ is UNMET."""
        stock = _empty_stock()
        r1 = evaluate_perceptual_readiness("P050", stock)
        assert r1.gate.status == ReadinessStatus.UNMET
        r2 = evaluate_compositional_readiness("P050", r1, "REF", "AGENT")
        assert r2.gate.status == ReadinessStatus.UNMET

    def test_cannot_have_ready3_met_without_ready2_met(self) -> None:
        """Ready₃ cannot be MET if Ready₂ is UNMET."""
        stock = _empty_stock()
        r1 = evaluate_perceptual_readiness("P051", stock)
        r2 = evaluate_compositional_readiness("P051", r1, "REF", "AGENT")
        assert r2.gate.status == ReadinessStatus.UNMET
        r3 = evaluate_propositional_readiness(r2, True, True)
        assert r3.status == ReadinessStatus.UNMET

    def test_ordering_preserved_in_full_pipeline(self) -> None:
        """Full stock: Ready₁ MET → Ready₂ MET → Ready₃ MET."""
        stock = _full_stock()
        record = build_informational_stock_record(
            "P052", stock, "cl", "ln", "ref", "role",
            predicate_closed=True, conflict_resolved=True,
        )
        assert record.ready_1.status == ReadinessStatus.MET
        assert record.ready_2.status == ReadinessStatus.MET
        assert record.ready_3.status == ReadinessStatus.MET

    def test_cascade_failure(self) -> None:
        """If Ready₁ fails, all subsequent gates fail."""
        stock = _empty_stock()
        record = build_informational_stock_record(
            "P053", stock, "?", "?", "?", "?",
            predicate_closed=True, conflict_resolved=True,
        )
        assert record.ready_1.status == ReadinessStatus.UNMET
        assert record.ready_2.status == ReadinessStatus.UNMET
        assert record.ready_3.status == ReadinessStatus.UNMET


# ═══════════════════════════════════════════════════════════════════════
# 10. FractalStage enum (Article 41)
# ═══════════════════════════════════════════════════════════════════════


class TestFractalLawCycle:
    """Verify FractalStage enum completeness (6 stages)."""

    def test_six_stages(self) -> None:
        assert len(FractalStage) == 6

    def test_stage_order(self) -> None:
        stages = list(FractalStage)
        names = [s.name for s in stages]
        assert names == [
            "DESIGNATION", "PRESERVATION", "LINKING",
            "JUDGMENT", "TRANSITION", "RETURN",
        ]


# ═══════════════════════════════════════════════════════════════════════
# 11. Re-exports
# ═══════════════════════════════════════════════════════════════════════


class TestReExports:
    """Verify new symbols are re-exported from arabic_engine.core."""

    def test_enum_reexports(self) -> None:
        from arabic_engine.core import (
            FractalStage as FS,
        )
        from arabic_engine.core import (
            InterpretationSource as IS,
        )
        from arabic_engine.core import (
            PerceptualGapReason as PGR,
        )
        from arabic_engine.core import (
            ReadinessLevel as RL,
        )
        from arabic_engine.core import (
            ReadinessStatus as RS,
        )
        from arabic_engine.core import (
            StockComponent as SC,
        )
        from arabic_engine.core import (
            StockSufficiency as SS,
        )
        assert len(SC) == 7
        assert len(RL) == 3
        assert len(RS) == 3
        assert len(PGR) == 4
        assert len(IS) == 7
        assert len(FS) == 6
        assert len(SS) == 3

    def test_type_reexports(self) -> None:
        from arabic_engine.core import (
            CompositionalReadinessResult as CRR,
        )
        from arabic_engine.core import (
            InformationalStockRecord as ISR,
        )
        from arabic_engine.core import (
            PerceptualReadinessResult as PRR,
        )
        from arabic_engine.core import (
            PriorInformationalStock as PIS,
        )
        from arabic_engine.core import (
            ReadinessGate as RG,
        )
        from arabic_engine.core import (
            StockEntry as SE,
        )
        # Verify they are the same types
        assert CRR is CompositionalReadinessResult
        assert ISR is InformationalStockRecord
        assert PRR is PerceptualReadinessResult
        assert PIS is PriorInformationalStock
        assert RG is ReadinessGate
        assert SE is StockEntry
