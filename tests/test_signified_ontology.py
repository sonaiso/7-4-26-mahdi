"""Tests for the Arabic Signified Ontology v1.0.

Covers:
  - Enum completeness and distinctness
  - SignifiedRecord frozen/hashable
  - Seed data loading (30 entries, no missing fields)
  - make_signified() fallback for unknown closures
  - validate_signified() constraint checking
  - batch_signified() length invariant
  - Pipeline integration with analyze_signified=True
  - Specialized subtype records
"""

from __future__ import annotations

import pytest

from arabic_engine.core.enums import (
    POS,
    CompositionDegree,
    ContextRequirement,
    DependencyDegree,
    ExistenceMode,
    FunctionalSubtype,
    LogicalStatus,
    LogicalSubtype,
    Modality,
    OntologicalSubtype,
    Polarity,
    PragmaticSubtype,
    PrimarySignifiedType,
    PropositionalSubtype,
    ReferentialSubtype,
    RelationalSubtype,
    RhetoricalStatus,
    RhetoricalSubtype,
    SignifiedTemporalStatus,
    SpecificityDegree,
)
from arabic_engine.core.types import (
    LexicalClosure,
    OntologicalSignified,
    PropositionalSignified,
    ReferentialSignified,
    RelationalSignified,
    RhetoricalSignified,
    SignifiedRecord,
)
from arabic_engine.signified.signified_record import (
    SIGNIFIED_DB,
    batch_signified,
    make_signified,
    validate_signified,
)

# ── Phase 1 tests: Enum completeness ────────────────────────────────


class TestEnumCompleteness:
    """All 8 PrimarySignifiedType values are distinct and present."""

    def test_primary_signified_has_8_values(self):
        assert len(PrimarySignifiedType) == 8

    def test_primary_signified_names(self):
        expected = {
            "ONTOLOGICAL",
            "RELATIONAL",
            "PROPOSITIONAL",
            "REFERENTIAL",
            "FUNCTIONAL",
            "PRAGMATIC",
            "LOGICAL",
            "RHETORICAL",
        }
        actual = {m.name for m in PrimarySignifiedType}
        assert actual == expected

    def test_ontological_subtype_has_25_values(self):
        assert len(OntologicalSubtype) == 25

    def test_relational_subtype_has_14_values(self):
        assert len(RelationalSubtype) == 14

    def test_propositional_subtype_has_9_values(self):
        assert len(PropositionalSubtype) == 9

    def test_referential_subtype_has_11_values(self):
        assert len(ReferentialSubtype) == 11

    def test_functional_subtype_has_9_values(self):
        assert len(FunctionalSubtype) == 9

    def test_pragmatic_subtype_has_7_values(self):
        assert len(PragmaticSubtype) == 7

    def test_logical_subtype_has_12_values(self):
        assert len(LogicalSubtype) == 12

    def test_rhetorical_subtype_has_8_values(self):
        assert len(RhetoricalSubtype) == 8

    def test_dependency_degree_has_6_values(self):
        assert len(DependencyDegree) == 6

    def test_existence_mode_has_6_values(self):
        assert len(ExistenceMode) == 6

    def test_specificity_degree_has_6_values(self):
        assert len(SpecificityDegree) == 6

    def test_composition_degree_has_4_values(self):
        assert len(CompositionDegree) == 4

    def test_signified_temporal_status_has_7_values(self):
        assert len(SignifiedTemporalStatus) == 7

    def test_logical_status_has_5_values(self):
        assert len(LogicalStatus) == 5

    def test_rhetorical_status_has_5_values(self):
        assert len(RhetoricalStatus) == 5

    def test_context_requirement_has_4_values(self):
        assert len(ContextRequirement) == 4

    def test_polarity_has_3_values(self):
        assert len(Polarity) == 3

    def test_modality_has_4_values(self):
        assert len(Modality) == 4

    def test_all_primary_values_unique(self):
        values = [m.value for m in PrimarySignifiedType]
        assert len(values) == len(set(values))


# ── Phase 2 tests: SignifiedRecord type ─────────────────────────────


class TestSignifiedRecord:
    """SignifiedRecord is frozen and hashable."""

    @pytest.fixture()
    def sample_record(self):
        return SignifiedRecord(
            id="SIG-TEST-001",
            label_ar="تجربة",
            label_en="test",
            definition="A test signified",
            primary_type=PrimarySignifiedType.ONTOLOGICAL,
            secondary_type="EntityMeaning.GenericEntity",
            dependency_degree=DependencyDegree.INDEPENDENT,
            existence_mode=ExistenceMode.EXTERNAL,
            specificity_degree=SpecificityDegree.UNDEFINED,
            composition_degree=CompositionDegree.SIMPLE,
            context_requirement=ContextRequirement.NONE,
            logical_status=LogicalStatus.NON_PROPOSITIONAL,
            rhetorical_status=RhetoricalStatus.LITERAL,
            temporal_status=SignifiedTemporalStatus.ATEMPORAL,
        )

    def test_frozen(self, sample_record):
        with pytest.raises(AttributeError):
            sample_record.id = "SIG-CHANGED"  # type: ignore[misc]

    def test_hashable(self, sample_record):
        h = hash(sample_record)
        assert isinstance(h, int)

    def test_equality(self, sample_record):
        other = SignifiedRecord(
            id="SIG-TEST-001",
            label_ar="تجربة",
            label_en="test",
            definition="A test signified",
            primary_type=PrimarySignifiedType.ONTOLOGICAL,
            secondary_type="EntityMeaning.GenericEntity",
            dependency_degree=DependencyDegree.INDEPENDENT,
            existence_mode=ExistenceMode.EXTERNAL,
            specificity_degree=SpecificityDegree.UNDEFINED,
            composition_degree=CompositionDegree.SIMPLE,
            context_requirement=ContextRequirement.NONE,
            logical_status=LogicalStatus.NON_PROPOSITIONAL,
            rhetorical_status=RhetoricalStatus.LITERAL,
            temporal_status=SignifiedTemporalStatus.ATEMPORAL,
        )
        assert sample_record == other

    def test_default_examples_empty(self, sample_record):
        assert sample_record.examples == ()

    def test_default_constraints_empty(self, sample_record):
        assert sample_record.constraints == ()

    def test_default_referential_status_none(self, sample_record):
        assert sample_record.referential_status is None


# ── Phase 2 tests: Specialized subtypes ─────────────────────────────


class TestSpecializedSubtypes:
    """Specialized SignifiedRecord subtypes carry extra fields."""

    def _base_kwargs(self):
        return dict(
            id="SIG-SUB-001",
            label_ar="فرعي",
            label_en="sub",
            definition="Subtype test",
            primary_type=PrimarySignifiedType.ONTOLOGICAL,
            secondary_type="EntityMeaning.GenericEntity",
            dependency_degree=DependencyDegree.INDEPENDENT,
            existence_mode=ExistenceMode.EXTERNAL,
            specificity_degree=SpecificityDegree.UNDEFINED,
            composition_degree=CompositionDegree.SIMPLE,
            context_requirement=ContextRequirement.NONE,
            logical_status=LogicalStatus.NON_PROPOSITIONAL,
            rhetorical_status=RhetoricalStatus.LITERAL,
            temporal_status=SignifiedTemporalStatus.ATEMPORAL,
        )

    def test_ontological_signified(self):
        rec = OntologicalSignified(
            **self._base_kwargs(),
            ontological_subtype=OntologicalSubtype.INDIVIDUAL_ENTITY,
            is_countable=True,
            is_named=True,
        )
        assert rec.ontological_subtype is OntologicalSubtype.INDIVIDUAL_ENTITY
        assert rec.is_named is True
        assert isinstance(rec, SignifiedRecord)

    def test_relational_signified(self):
        kwargs = self._base_kwargs()
        kwargs["primary_type"] = PrimarySignifiedType.RELATIONAL
        kwargs["secondary_type"] = "SpatialRelation"
        rec = RelationalSignified(**kwargs, arity=3, symmetry=True)
        assert rec.arity == 3
        assert rec.symmetry is True

    def test_propositional_signified(self):
        kwargs = self._base_kwargs()
        kwargs["primary_type"] = PrimarySignifiedType.PROPOSITIONAL
        kwargs["secondary_type"] = "NegationMeaning"
        rec = PropositionalSignified(
            **kwargs,
            truth_evaluable=True,
            polarity=Polarity.NEGATIVE,
            modality=Modality.CERTAIN_MOD,
        )
        assert rec.truth_evaluable is True
        assert rec.polarity is Polarity.NEGATIVE

    def test_referential_signified(self):
        kwargs = self._base_kwargs()
        kwargs["primary_type"] = PrimarySignifiedType.REFERENTIAL
        kwargs["secondary_type"] = "PronounReference"
        rec = ReferentialSignified(
            **kwargs,
            reference_source="text",
            definiteness=True,
            anaphora_direction="backward",
        )
        assert rec.reference_source == "text"
        assert rec.definiteness is True

    def test_rhetorical_signified(self):
        kwargs = self._base_kwargs()
        kwargs["primary_type"] = PrimarySignifiedType.RHETORICAL
        kwargs["secondary_type"] = "MetaphoricalMeaning"
        kwargs["rhetorical_status"] = RhetoricalStatus.FIGURATIVE_RHET
        rec = RhetoricalSignified(
            **kwargs,
            literal_base="أسد",
            figurative_projection="رجل شجاع",
            deviation_degree=0.8,
        )
        assert rec.literal_base == "أسد"
        assert rec.deviation_degree == 0.8


# ── Phase 5 tests: Seed data ────────────────────────────────────────


class TestSeedData:
    """Seed database loads correctly with all 30 entries."""

    def test_seed_loads_30_entries(self):
        assert len(SIGNIFIED_DB) == 30

    def test_all_entries_are_signified_records(self):
        for rec in SIGNIFIED_DB.values():
            assert isinstance(rec, SignifiedRecord)

    def test_no_empty_ids(self):
        for rec in SIGNIFIED_DB.values():
            assert rec.id, f"Empty id for {rec.label_ar}"

    def test_no_empty_labels(self):
        for rec in SIGNIFIED_DB.values():
            assert rec.label_ar, f"Empty label_ar for {rec.id}"
            assert rec.label_en, f"Empty label_en for {rec.id}"

    def test_no_empty_definitions(self):
        for rec in SIGNIFIED_DB.values():
            assert rec.definition, f"Empty definition for {rec.id}"

    def test_all_primary_types_valid(self):
        for rec in SIGNIFIED_DB.values():
            assert isinstance(rec.primary_type, PrimarySignifiedType)

    def test_known_entry_hatha(self):
        rec = SIGNIFIED_DB["هذا"]
        assert rec.primary_type is PrimarySignifiedType.REFERENTIAL
        assert rec.referential_status is ReferentialSubtype.DEICTIC
        assert rec.specificity_degree is SpecificityDegree.DEICTICALLY_FIXED

    def test_known_entry_kataba(self):
        rec = SIGNIFIED_DB["كتب"]
        assert rec.primary_type is PrimarySignifiedType.ONTOLOGICAL
        assert rec.temporal_status is SignifiedTemporalStatus.PAST_SIG

    def test_known_entry_fi(self):
        rec = SIGNIFIED_DB["في"]
        assert rec.primary_type is PrimarySignifiedType.RELATIONAL

    def test_known_entry_huwa(self):
        rec = SIGNIFIED_DB["هو"]
        assert rec.primary_type is PrimarySignifiedType.REFERENTIAL
        assert rec.referential_status is ReferentialSubtype.PRONOUN

    def test_known_entry_inna(self):
        rec = SIGNIFIED_DB["إنّ"]
        assert rec.primary_type is PrimarySignifiedType.PROPOSITIONAL

    def test_known_entry_asad(self):
        rec = SIGNIFIED_DB["أسد"]
        assert rec.primary_type is PrimarySignifiedType.RHETORICAL
        assert rec.rhetorical_status is RhetoricalStatus.FIGURATIVE_RHET

    def test_all_examples_are_tuples(self):
        for rec in SIGNIFIED_DB.values():
            assert isinstance(rec.examples, tuple), f"{rec.id} examples not tuple"

    def test_all_constraints_are_tuples(self):
        for rec in SIGNIFIED_DB.values():
            assert isinstance(rec.constraints, tuple), f"{rec.id} constraints not tuple"


# ── Phase 3.1 tests: make_signified ─────────────────────────────────


class TestMakeSignified:
    """make_signified() factory produces correct records."""

    def _make_closure(self, lemma, pos=POS.ISM):
        return LexicalClosure(
            surface=lemma,
            lemma=lemma,
            root=(),
            pattern="",
            pos=pos,
        )

    def test_known_lemma_returns_seed(self):
        cl = self._make_closure("هذا")
        rec = make_signified(cl)
        assert rec.id == "SIG-024"
        assert rec.primary_type is PrimarySignifiedType.REFERENTIAL

    def test_unknown_ism_returns_ontological(self):
        cl = self._make_closure("شجرة", POS.ISM)
        rec = make_signified(cl)
        assert rec.primary_type is PrimarySignifiedType.ONTOLOGICAL
        assert "EntityMeaning" in rec.secondary_type

    def test_unknown_fi3l_returns_event(self):
        cl = self._make_closure("أكل", POS.FI3L)
        rec = make_signified(cl)
        assert rec.primary_type is PrimarySignifiedType.ONTOLOGICAL
        assert "EventMeaning" in rec.secondary_type

    def test_unknown_harf_returns_functional(self):
        cl = self._make_closure("لـ", POS.HARF)
        rec = make_signified(cl)
        assert rec.primary_type is PrimarySignifiedType.FUNCTIONAL

    def test_unknown_damir_returns_referential(self):
        cl = self._make_closure("أنا", POS.DAMIR)
        rec = make_signified(cl)
        assert rec.primary_type is PrimarySignifiedType.REFERENTIAL

    def test_unknown_sifa_returns_property(self):
        cl = self._make_closure("عظيم", POS.SIFA)
        rec = make_signified(cl)
        assert "PropertyMeaning" in rec.secondary_type

    def test_unknown_zarf_returns_relational(self):
        cl = self._make_closure("تحت", POS.ZARF)
        rec = make_signified(cl)
        assert rec.primary_type is PrimarySignifiedType.RELATIONAL

    def test_auto_id_prefix(self):
        cl = self._make_closure("مجهول", POS.UNKNOWN)
        rec = make_signified(cl)
        assert rec.id.startswith("SIG-GEN-")

    def test_auto_record_is_frozen(self):
        cl = self._make_closure("مجهول2", POS.UNKNOWN)
        rec = make_signified(cl)
        with pytest.raises(AttributeError):
            rec.id = "changed"  # type: ignore[misc]


# ── Phase 3.1 tests: batch_signified ────────────────────────────────


class TestBatchSignified:
    """batch_signified() preserves input length."""

    def test_empty_list(self):
        assert batch_signified([]) == []

    def test_length_matches(self):
        closures = [
            LexicalClosure(surface="كتب", lemma="كتب", root=(), pattern="", pos=POS.FI3L),
            LexicalClosure(surface="زيد", lemma="زيد", root=(), pattern="", pos=POS.ISM),
            LexicalClosure(surface="هو", lemma="هو", root=(), pattern="", pos=POS.DAMIR),
        ]
        result = batch_signified(closures)
        assert len(result) == 3

    def test_all_are_signified_records(self):
        closures = [
            LexicalClosure(surface="x", lemma="x", root=(), pattern="", pos=POS.UNKNOWN),
        ]
        result = batch_signified(closures)
        assert all(isinstance(r, SignifiedRecord) for r in result)


# ── Phase 3.1 tests: validate_signified ─────────────────────────────


class TestValidateSignified:
    """validate_signified() catches constraint violations."""

    def _base_kwargs(self):
        return dict(
            id="SIG-V-001",
            label_ar="صحيح",
            label_en="valid",
            definition="A valid test signified",
            primary_type=PrimarySignifiedType.ONTOLOGICAL,
            secondary_type="EntityMeaning.GenericEntity",
            dependency_degree=DependencyDegree.INDEPENDENT,
            existence_mode=ExistenceMode.EXTERNAL,
            specificity_degree=SpecificityDegree.UNDEFINED,
            composition_degree=CompositionDegree.SIMPLE,
            context_requirement=ContextRequirement.NONE,
            logical_status=LogicalStatus.NON_PROPOSITIONAL,
            rhetorical_status=RhetoricalStatus.LITERAL,
            temporal_status=SignifiedTemporalStatus.ATEMPORAL,
        )

    def test_valid_record_no_violations(self):
        rec = SignifiedRecord(**self._base_kwargs())
        violations = validate_signified(rec)
        assert violations == []

    def test_empty_id_violation(self):
        kwargs = self._base_kwargs()
        kwargs["id"] = ""
        rec = SignifiedRecord(**kwargs)
        violations = validate_signified(rec)
        assert any("id" in v for v in violations)

    def test_empty_label_violation(self):
        kwargs = self._base_kwargs()
        kwargs["label_ar"] = ""
        rec = SignifiedRecord(**kwargs)
        violations = validate_signified(rec)
        assert any("label_ar" in v for v in violations)

    def test_empty_definition_violation(self):
        kwargs = self._base_kwargs()
        kwargs["definition"] = ""
        rec = SignifiedRecord(**kwargs)
        violations = validate_signified(rec)
        assert any("definition" in v for v in violations)

    def test_c3_referential_needs_referential_status(self):
        kwargs = self._base_kwargs()
        kwargs["primary_type"] = PrimarySignifiedType.REFERENTIAL
        kwargs["secondary_type"] = "PronounReference"
        # referential_status defaults to None
        rec = SignifiedRecord(**kwargs)
        violations = validate_signified(rec)
        assert any("C3" in v for v in violations)

    def test_c3_referential_with_status_passes(self):
        kwargs = self._base_kwargs()
        kwargs["primary_type"] = PrimarySignifiedType.REFERENTIAL
        kwargs["secondary_type"] = "PronounReference"
        kwargs["referential_status"] = ReferentialSubtype.PRONOUN
        rec = SignifiedRecord(**kwargs)
        violations = validate_signified(rec)
        assert not any("C3" in v for v in violations)

    def test_c5_rhetorical_needs_non_literal(self):
        kwargs = self._base_kwargs()
        kwargs["primary_type"] = PrimarySignifiedType.RHETORICAL
        kwargs["secondary_type"] = "MetaphoricalMeaning"
        kwargs["rhetorical_status"] = RhetoricalStatus.LITERAL
        rec = SignifiedRecord(**kwargs)
        violations = validate_signified(rec)
        assert any("C5" in v for v in violations)

    def test_c5_rhetorical_with_figurative_passes(self):
        kwargs = self._base_kwargs()
        kwargs["primary_type"] = PrimarySignifiedType.RHETORICAL
        kwargs["secondary_type"] = "MetaphoricalMeaning"
        kwargs["rhetorical_status"] = RhetoricalStatus.FIGURATIVE_RHET
        rec = SignifiedRecord(**kwargs)
        violations = validate_signified(rec)
        assert not any("C5" in v for v in violations)

    def test_all_seed_records_valid(self):
        """Every seed record should pass validation."""
        for label, rec in SIGNIFIED_DB.items():
            violations = validate_signified(rec)
            assert violations == [], f"{label} ({rec.id}): {violations}"


# ── Phase 3.2 tests: ontology bridge ────────────────────────────────


class TestOntologyBridge:
    """map_signified() in ontology.py delegates correctly."""

    def test_map_signified_returns_record(self):
        from arabic_engine.signified.ontology import map_signified

        cl = LexicalClosure(
            surface="هذا", lemma="هذا", root=(), pattern="", pos=POS.ISM
        )
        rec = map_signified(cl)
        assert isinstance(rec, SignifiedRecord)
        assert rec.label_ar == "هذا"


# ── Phase 4 tests: Pipeline integration ─────────────────────────────


class TestPipelineIntegration:
    """Pipeline run() with analyze_signified parameter."""

    def test_default_no_signified(self):
        from arabic_engine.pipeline import run

        result = run("كَتَبَ زَيْد رِسَالَة")
        assert result.signified_records == []

    def test_analyze_signified_populates(self):
        from arabic_engine.pipeline import run

        result = run("كَتَبَ زَيْد رِسَالَة", analyze_signified=True)
        assert len(result.signified_records) > 0
        assert len(result.signified_records) == len(result.closures)
        for rec in result.signified_records:
            assert isinstance(rec, SignifiedRecord)

    def test_backward_compatibility_concepts(self):
        """Existing concepts field still works."""
        from arabic_engine.pipeline import run

        result = run("كَتَبَ زَيْد رِسَالَة", analyze_signified=True)
        assert len(result.concepts) == len(result.closures)


# ── Re-export tests ─────────────────────────────────────────────────


class TestReExports:
    """Key symbols importable from arabic_engine.core and arabic_engine.signified."""

    def test_core_exports_primary_signified_type(self):
        from arabic_engine.core import PrimarySignifiedType as PST

        assert len(PST) == 8

    def test_core_exports_signified_record(self):
        from arabic_engine.core import SignifiedRecord as SR

        assert SR is SignifiedRecord

    def test_signified_module_exports(self):
        from arabic_engine.signified import (
            SIGNIFIED_DB,
            batch_signified,
            make_signified,
            validate_signified,
        )

        assert callable(make_signified)
        assert callable(batch_signified)
        assert callable(validate_signified)
        assert isinstance(SIGNIFIED_DB, dict)
