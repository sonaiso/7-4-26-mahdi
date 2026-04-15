// ============================================================
// Knowledge Episode Graph — Bootstrap / Seed Data
// Run once after schema.cypher to populate reference nodes.
// ============================================================

// ---------- Methods ----------
MERGE (m1:Method {id: 'method:rational'})
SET m1.method_family = 'rational',
    m1.scope = 'general cognition',
    m1.requires_experiment = false,
    m1.requires_formal_proof = false,
    m1.requires_linguistic_anchor = false;

MERGE (m2:Method {id: 'method:scientific'})
SET m2.method_family = 'scientific',
    m2.scope = 'empirical material inquiry',
    m2.requires_experiment = true,
    m2.requires_formal_proof = false,
    m2.requires_linguistic_anchor = false;

MERGE (m3:Method {id: 'method:linguistic'})
SET m3.method_family = 'linguistic',
    m3.scope = 'utterance/concept analysis',
    m3.requires_experiment = false,
    m3.requires_formal_proof = false,
    m3.requires_linguistic_anchor = true;

MERGE (m4:Method {id: 'method:mathematical'})
SET m4.method_family = 'mathematical',
    m4.scope = 'formal symbolic proof',
    m4.requires_experiment = false,
    m4.requires_formal_proof = true,
    m4.requires_linguistic_anchor = false;

MERGE (m5:Method {id: 'method:physical'})
SET m5.method_family = 'physical',
    m5.scope = 'physical law and measurement',
    m5.requires_experiment = true,
    m5.requires_formal_proof = true,
    m5.requires_linguistic_anchor = false;

// ---------- Default Conflict Rule ----------
MERGE (c1:ConflictRule {id: 'conflict:default'})
SET c1.rule_name = 'default_conflict_v1',
    c1.priority_order = 'Reality > Valid Proof > Concept specialization > Utterance > Suspend',
    c1.action_on_conflict = 'downgrade_or_reject';
