# Product-Lens Ledger

## audit — 2026-09-13 — rev c6c04d32

Point (re-derived): Study verification must give operators faithful evidence of the audited package's numerical behavior. [source: README.md and docs/integration_seam_operator_guide.md, grade: INHERITED; domain agreement is AGENT inference supporting owner remediation request in work/orchestration/goals/fusion-audit-remediation/goal.md]

Falsifier: Identical conductor/cryo inputs produce an accepted oracle value while the public/native calculation rejects them, or accepted results disagree.

Findings: None within the bounded oracle correction and public/native agreement scope.

Smell disposition: “Two representations must be manually kept synchronized” applies to independently implemented oracle/native equations. The independent oracle is a verification witness, with no role supplying production numbers. Retain separate implementations and verify their agreement through domain probes and physical identities. This disposition is audit judgment [AGENT], not an owner-originated settled decision.

Evidence: Fresh no-history reviewer `/root/domain_auditor/product_lens`, dispatched from `audit-evidence/product-lens-brief.md`, ran all 27 consumer tests and independent public-module probes for baseline agreement and nine invalid temperature/clearance cases. Parameter restoration and unsupported-key rejection remain explicit. T-036 regression migration and global product certification were outside this review.

Gate: CLEAR

## audit supplement — 2026-09-13 — rev e2b68b67

Point (re-derived): Study verification must give operators faithful evidence of the audited package's numerical behavior. [source: README.md and docs/integration_seam_operator_guide.md, grade: INHERITED; numerical-domain agreement is AGENT inference supporting the owner remediation request in goal.md]

Falsifier: Current regressions pass while an exercised route accepts invalid clearance, preserves obsolete failure behavior, or bypasses numerical comparisons.

Findings:

- audit-supplement-F1 [DO] Test maintenance depends on historical driver source text and duplicated failure expectations. [source: product-lens independent assessment of operator usability and numerical-evidence purpose; maintenance obligation grade: AGENT] — disposition: retain the bounded current adaptation at e2b68b67 for the reasons below.

Smells: “Correctness depends on downstream knowledge of an internal representation” and “Two representations must be manually kept synchronized.” This finding is escalated and resolved explicitly in audit.md Product Judgment. The temporary adapter preserves the immutable historical witnesses while current callers assert the corrected behavior. Changed semantic replacements require exact-once matches, all routes execute, and outer checks independently require domain-error messages. Financial channels remain numerically compared at 1e-9. This supplies a bounded test-maintenance decision, not a new platform contract or owner-originated settled rule.

Resolves:

- audit-supplement-F1: DEFERRED — authority: AGENT — basis: accept the bounded historical-driver adaptation for this revision because it fails on semantic source drift, preserves original evidence, and independent outer assertions plus native/public probes verify current behavior; reassess it when historical-driver contracts change.

Evidence: Fresh no-history product-lens reviewer resumed its independently derived point to inspect all four committed regression files and their invoked code. This supplement adds no test execution or global certification claim.

Gate: DISPOSED (audit-supplement-F1)
