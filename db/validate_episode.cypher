// ============================================================
// Knowledge Episode Graph — Episode Insertion & Validation
// ============================================================


// ── Section 1: MERGE pattern for inserting a KnowledgeEpisode ───────
// Expected parameters:
// $self, $episode, $reality, $sense, $priorInfos, $linking, $judgement,
// $carrier, $utterance, $concept, $proof, $conflict, $opinions

MERGE (s:Self {id: $self.id})
SET s += $self

MERGE (ep:KnowledgeEpisode {id: $episode.id})
SET ep += $episode

MERGE (s)-[:UNDERGOES]->(ep)

MERGE (ra:RealityAnchor {id: $reality.id})
SET ra += $reality
MERGE (ep)-[:HAS_REALITY_ANCHOR]->(ra)

MERGE (st:SenseTrace {id: $sense.id})
SET st += $sense
MERGE (ep)-[:HAS_SENSE_TRACE]->(st)

FOREACH (pi IN $priorInfos |
  MERGE (p:PriorInfo {id: pi.id})
  SET p += pi
  MERGE (ep)-[:USES_PRIOR_INFO]->(p)
)

MERGE (lt:LinkingTrace {id: $linking.id})
SET lt += $linking
MERGE (ep)-[:HAS_LINKING_TRACE]->(lt)

MERGE (j:Judgement {id: $judgement.id})
SET j += $judgement
MERGE (ep)-[:ISSUES]->(j)

MERGE (m:Method {id: $episode.method_ref})
MERGE (ep)-[:USES_METHOD]->(m)

MERGE (lc:LinguisticCarrier {id: $carrier.id})
SET lc += $carrier
MERGE (ep)-[:CARRIED_BY]->(lc)

FOREACH (_ IN CASE WHEN $utterance IS NULL THEN [] ELSE [1] END |
  MERGE (u:Utterance {id: $utterance.id})
  SET u += $utterance
  MERGE (lc)-[:REALIZED_AS]->(u)
)

FOREACH (_ IN CASE WHEN $concept IS NULL THEN [] ELSE [1] END |
  MERGE (c:Concept {id: $concept.id})
  SET c += $concept
  MERGE (lc)-[:REALIZED_AS]->(c)
)

FOREACH (_ IN CASE WHEN $utterance IS NULL OR $concept IS NULL THEN [] ELSE [1] END |
  MERGE (u2:Utterance {id: $utterance.id})
  MERGE (c2:Concept {id: $concept.id})
  MERGE (u2)-[:ANCHORS_TO]->(c2)
)

MERGE (pp:ProofPath {id: $proof.id})
SET pp += $proof
MERGE (ep)-[:JUSTIFIED_BY]->(pp)

MERGE (cr:ConflictRule {id: $conflict.id})
MERGE (ep)-[:VALIDATED_BY]->(cr)

FOREACH (op IN $opinions |
  MERGE (o:OpinionTrace {id: op.id})
  SET o += op
  MERGE (ep)-[:MUST_EXCLUDE]->(o)
);


// ── Section 2: Core per-episode validator ───────────────────────────
// Run after insertion.  Parameter: $episodeId

MATCH (ep:KnowledgeEpisode {id: $episodeId})

OPTIONAL MATCH (ep)-[:HAS_REALITY_ANCHOR]->(ra:RealityAnchor)
OPTIONAL MATCH (ep)-[:HAS_SENSE_TRACE]->(st:SenseTrace)
OPTIONAL MATCH (ep)-[:HAS_LINKING_TRACE]->(lt:LinkingTrace)
OPTIONAL MATCH (ep)-[:ISSUES]->(j:Judgement)
OPTIONAL MATCH (ep)-[:USES_METHOD]->(m:Method)
OPTIONAL MATCH (ep)-[:CARRIED_BY]->(lc:LinguisticCarrier)
OPTIONAL MATCH (ep)-[:JUSTIFIED_BY]->(pp:ProofPath)
OPTIONAL MATCH (ep)-[:VALIDATED_BY]->(cr:ConflictRule)
OPTIONAL MATCH (ep)-[:USES_PRIOR_INFO]->(pi:PriorInfo)
OPTIONAL MATCH (ep)-[:MUST_EXCLUDE]->(ot:OpinionTrace)

WITH ep, ra, st, lt, j, m, lc, pp, cr,
     collect(DISTINCT pi) AS priorInfos,
     collect(DISTINCT ot) AS opinions

WITH ep, ra, st, lt, j, m, lc, pp, cr, priorInfos, opinions,
     CASE WHEN ra IS NULL THEN ['Missing RealityAnchor'] ELSE [] END +
     CASE WHEN st IS NULL THEN ['Missing SenseTrace'] ELSE [] END +
     CASE WHEN size(priorInfos) = 0 THEN ['Missing PriorInfo'] ELSE [] END +
     CASE WHEN lt IS NULL THEN ['Missing LinkingTrace'] ELSE [] END +
     CASE WHEN j IS NULL OR ep.judgement_type IS NULL THEN ['Missing JudgementType'] ELSE [] END +
     CASE WHEN m IS NULL THEN ['Missing MethodFit'] ELSE [] END +
     CASE WHEN lc IS NULL OR ep.carrier_type NOT IN ['utterance','concept','both'] THEN ['Invalid LinguisticCarrier'] ELSE [] END +
     CASE WHEN pp IS NULL THEN ['Missing ProofPath'] ELSE [] END +
     CASE WHEN cr IS NULL THEN ['Missing ConflictRule'] ELSE [] END +
     CASE
       WHEN any(o IN opinions WHERE o.contamination_level IN ['medium','high'])
       THEN ['Opinion contamination']
       ELSE []
     END +
     CASE
       WHEN m IS NOT NULL
        AND m.method_family = 'scientific'
        AND ep.judgement_type IN ['normative','pure_linguistic','metaphysical']
       THEN ['MethodFit failed: scientific method not suitable']
       ELSE []
     END
     AS errors

SET ep.validation_state =
  CASE WHEN size(errors) = 0 THEN 'valid' ELSE 'invalid' END

SET ep.epistemic_rank =
  CASE
    WHEN any(e IN errors WHERE e IN [
      'Missing RealityAnchor',
      'Missing SenseTrace',
      'Missing PriorInfo',
      'Opinion contamination',
      'Invalid LinguisticCarrier'
    ]) THEN 'REJECTED_METHODOLOGICALLY'

    WHEN any(e IN errors WHERE e CONTAINS 'Conflict')
      OR any(e IN errors WHERE e CONTAINS 'not suitable')
    THEN 'IMPOSSIBLE'

    WHEN size(errors) = 0
      AND ep.judgement_type = 'existence'
      AND pp.path_kind IN ['hissi','aqli','formal']
    THEN 'CERTAIN'

    WHEN size(errors) = 0
      AND ep.judgement_type IN ['essence','attribute','relation','causal','interpretive','formal']
    THEN 'TRUE_NON_CERTAIN'

    ELSE 'PROBABILISTIC_DOUBT'
  END

WITH ep, errors
CALL {
  WITH ep, errors
  OPTIONAL MATCH (ep)-[r:HAS_GAP]->(oldGap:Gap)
  DELETE r
  WITH ep, errors
  UNWIND errors AS err
  MERGE (g:Gap {id: ep.id + '::' + replace(err,' ','_')})
  SET g.gap_type = err,
      g.message = err,
      g.severity = CASE
        WHEN err IN ['Missing RealityAnchor','Missing SenseTrace','Missing PriorInfo','Invalid LinguisticCarrier']
          THEN 'fatal'
        WHEN err = 'Opinion contamination'
          THEN 'high'
        ELSE 'medium'
      END
  MERGE (ep)-[:HAS_GAP]->(g)
  RETURN count(*) AS _
}
RETURN ep.id AS episode,
       ep.validation_state AS validation_state,
       ep.epistemic_rank AS epistemic_rank,
       errors;


// ── Section 3: Linguistic-carrier validator ─────────────────────────
// Parameter: $episodeId

MATCH (ep:KnowledgeEpisode {id: $episodeId})-[:CARRIED_BY]->(lc:LinguisticCarrier)
OPTIONAL MATCH (lc)-[:REALIZED_AS]->(u:Utterance)
OPTIONAL MATCH (lc)-[:REALIZED_AS]->(c:Concept)
WITH ep, lc, count(DISTINCT u) AS uCount, count(DISTINCT c) AS cCount
RETURN ep.id AS episode,
       lc.carrier_class AS carrier_class,
       uCount,
       cCount,
       CASE
         WHEN lc.carrier_class = 'utterance' AND uCount >= 1 THEN 'ok'
         WHEN lc.carrier_class = 'concept' AND cCount >= 1 THEN 'ok'
         WHEN lc.carrier_class = 'both' AND uCount >= 1 AND cCount >= 1 THEN 'ok'
         ELSE 'invalid'
       END AS linguistic_carrier_status;


// ── Section 4: Utterance/Concept conflict resolution ────────────────
// Parameter: $episodeId

MATCH (ep:KnowledgeEpisode {id: $episodeId})-[:CARRIED_BY]->(lc:LinguisticCarrier)
OPTIONAL MATCH (lc)-[:REALIZED_AS]->(u:Utterance)
OPTIONAL MATCH (lc)-[:REALIZED_AS]->(c:Concept)
OPTIONAL MATCH (ep)-[:HAS_REALITY_ANCHOR]->(ra:RealityAnchor)
OPTIONAL MATCH (ep)-[:JUSTIFIED_BY]->(pp:ProofPath)
RETURN ep.id AS episode,
       u.text_shakled AS utterance,
       c.concept_name AS concept,
       ra.reality_kind AS reality_kind,
       pp.path_kind AS proof_kind,
       CASE
         WHEN u IS NULL OR c IS NULL THEN 'no_internal_conflict_check'
         WHEN pp.path_kind IN ['aqli','formal','hissi'] AND ra IS NOT NULL THEN 'prefer_grounded_reading'
         ELSE 'review_needed'
       END AS conflict_resolution_hint;


// ── Section 5: Batch validator ──────────────────────────────────────

MATCH (ep:KnowledgeEpisode)
RETURN ep.id AS episodeId,
       ep.validation_state AS validation_state,
       ep.epistemic_rank AS epistemic_rank
ORDER BY ep.validation_state, ep.epistemic_rank, ep.id;
