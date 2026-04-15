// ============================================================
// Knowledge Episode Graph — Schema Constraints
// Run once against a Neo4j instance to create all constraints.
// ============================================================

// ---------- Node keys ----------
CREATE CONSTRAINT ke_id IF NOT EXISTS
FOR (n:KnowledgeEpisode) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT self_id IF NOT EXISTS
FOR (n:Self) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT reality_id IF NOT EXISTS
FOR (n:RealityAnchor) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT sense_id IF NOT EXISTS
FOR (n:SenseTrace) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT prior_id IF NOT EXISTS
FOR (n:PriorInfo) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT opinion_id IF NOT EXISTS
FOR (n:OpinionTrace) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT linking_id IF NOT EXISTS
FOR (n:LinkingTrace) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT judgement_id IF NOT EXISTS
FOR (n:Judgement) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT method_id IF NOT EXISTS
FOR (n:Method) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT carrier_id IF NOT EXISTS
FOR (n:LinguisticCarrier) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT utterance_id IF NOT EXISTS
FOR (n:Utterance) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT concept_id IF NOT EXISTS
FOR (n:Concept) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT proof_id IF NOT EXISTS
FOR (n:ProofPath) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT conflict_id IF NOT EXISTS
FOR (n:ConflictRule) REQUIRE (n.id) IS NODE KEY;

CREATE CONSTRAINT gap_id IF NOT EXISTS
FOR (n:Gap) REQUIRE (n.id) IS NODE KEY;

// ---------- Required properties ----------
CREATE CONSTRAINT ke_domain_required IF NOT EXISTS
FOR (n:KnowledgeEpisode) REQUIRE n.domain_profile IS NOT NULL;

CREATE CONSTRAINT ke_judgement_required IF NOT EXISTS
FOR (n:KnowledgeEpisode) REQUIRE n.judgement_type IS NOT NULL;

CREATE CONSTRAINT ke_method_required IF NOT EXISTS
FOR (n:KnowledgeEpisode) REQUIRE n.method_family IS NOT NULL;

CREATE CONSTRAINT ke_carrier_required IF NOT EXISTS
FOR (n:KnowledgeEpisode) REQUIRE n.carrier_type IS NOT NULL;

CREATE CONSTRAINT ke_validation_required IF NOT EXISTS
FOR (n:KnowledgeEpisode) REQUIRE n.validation_state IS NOT NULL;

CREATE CONSTRAINT reality_kind_required IF NOT EXISTS
FOR (n:RealityAnchor) REQUIRE n.reality_kind IS NOT NULL;

CREATE CONSTRAINT sense_modality_required IF NOT EXISTS
FOR (n:SenseTrace) REQUIRE n.sense_modality IS NOT NULL;

CREATE CONSTRAINT prior_kind_required IF NOT EXISTS
FOR (n:PriorInfo) REQUIRE n.info_kind IS NOT NULL;

CREATE CONSTRAINT linking_kind_required IF NOT EXISTS
FOR (n:LinkingTrace) REQUIRE n.link_kind IS NOT NULL;

CREATE CONSTRAINT judgement_type_required IF NOT EXISTS
FOR (n:Judgement) REQUIRE n.judgement_type IS NOT NULL;

CREATE CONSTRAINT method_family_required IF NOT EXISTS
FOR (n:Method) REQUIRE n.method_family IS NOT NULL;

CREATE CONSTRAINT carrier_class_required IF NOT EXISTS
FOR (n:LinguisticCarrier) REQUIRE n.carrier_class IS NOT NULL;

CREATE CONSTRAINT utterance_text_required IF NOT EXISTS
FOR (n:Utterance) REQUIRE n.text_shakled IS NOT NULL;

CREATE CONSTRAINT concept_name_required IF NOT EXISTS
FOR (n:Concept) REQUIRE n.concept_name IS NOT NULL;

CREATE CONSTRAINT proof_kind_required IF NOT EXISTS
FOR (n:ProofPath) REQUIRE n.path_kind IS NOT NULL;

CREATE CONSTRAINT conflict_name_required IF NOT EXISTS
FOR (n:ConflictRule) REQUIRE n.rule_name IS NOT NULL;
