# Trail: Tape procurement consistency

## Round 1 — physical-tape-basis

### Strategy revision — 2026-09-15

- **Approach:** [AGENT] Derive purchased composite-tape length from the physical inventory and price that same quantity using an explicit construction and price basis.
- **Assumptions:** Existing fixed pack composition and envelope-relative sizing can support a coherent physical interpretation; evidence must establish the tape cross-section conversion.
- **Abandonment conditions:** Source construction is incompatible with the inventory meaning, or density cannot be assigned a supported interpretation without changing the objective. Surface the conflict and choose a defensible alternative within the owner's scope.
- **Intended model increment:** One shared tape quantity for procurement with one application of envelope scaling and separate non-tape/winding accounts.
- **Intended study question:** Does the corrected density response agree across native/package/oracle paths, including envelope, current and coil-length interactions, and what price/predicate consequences follow relative to the entering package?

### T-001 scope

- **Objective:** Establish tape construction, quantity conversion, compatible price basis and supported density interpretation.
- **Why now:** Entering procurement prices ampere-metres while physical inventory varies with reference density.
- **Scope:** Internal and clean external source research plus bounded formulation; no production mutation.
- **Inputs:** goal.md; entering WI-038/WI-040 source and audit records at ccb6d843; registered sources.
- **Done when:** A source-backed conversion and explicit assumptions can receive independent source/math review, or evidence supports a bounded negative.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-001 start — 2026-09-15

Research · native research seam and evidence/tape-basis-research.md · expected source-backed basis with construction, dimensions, price units and density mechanisms.

### T-002 scope

- **Objective:** Deliver the native tape quantity/cost correction through WI-060 with reviewed source/interface design and coherent model/package/oracle consumers.
- **Why now:** The entering definitions establish the mismatch independently of which supported construction the research selects.
- **Scope:** Native spec and dependency preparation may run alongside T-001; production implementation depends on completed source research and independent review. Model author owns models/twins, generation, oracle and affected consumer checks; researcher owns native source/request records; coordinator owns goal and later study records. Their preparation writes do not overlap and research cannot invalidate the need for the correction.
- **Inputs:** goal.md; WI-060 spec; entering revision ccb6d843; T-001 basis when returned.
- **Done when:** Reviewed implementation and validation supply one committed study-ready package.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-002 start — 2026-09-15

Native model · WI-060 · source-reviewed design, implemented correction and coherent executable evidence.

### Amendment — 2026-09-15 — T-002 recording order

[AGENT] The coordinator registered WI-060 and wrote its owner-derived spec before appending T-002 scope/start. That preparation-only bookkeeping preceded its trail scope; no production mutation occurred. This entry records the ordering defect rather than implying the scope was written first. The delegated author remains blocked on source/interface review before production changes.

### T-001 return — 2026-09-15

- **Outcome:** COMPLETE.
- **Evidence:** evidence/tape-basis-research.md and native REQ-TAPE-001 records at e4760057.
- **Reading:** Existing original sources support full composite-tape inventory conversion; a chosen width/thickness combination and absolute price remain explicit assumptions. Source grading replaces tape with stabilizer and cannot be imported into the fixed-fraction model as a free quantity discount.
- **Decision:** Trigger: alternative density mechanisms and price conventions. Decision: choose same-tape operating loading with unknown absolute current margin and direct $20/tape-metre scenario, rather than the researcher's fixed-margin technology and $30 illustrative recommendations; the simpler assumptions answer the physical inventory correction without assigning an unmodeled performance improvement. Tier: execution detail under the owner's delegated engineering judgment. Decided by: coordinator. Changed: WI-060 design; review pending.

### T-003 scope

- **Objective:** Prepare and execute a bounded native sensitivity study of the repaired tape quantity/cost response, then synthesize it.
- **Why now:** The entering comparison is preserved and candidate study coordinates can be prepared independently of production implementation.
- **Scope:** Preparation only until T-002 audited package and native integration candidate are accepted. Study author owns exploration/stellarator_e2e/studies/20260915-tape-procurement-consistency/ and its discovery rows; no production/model/oracle mutation. Candidate-specific scan, indicators and execution wait for package release. Model work cannot invalidate preparation's owner intake or native study scaffolding; dependent numerical work is held.
- **Inputs:** goal.md; evidence/entering/comparison.json@af777f44; candidate-proposals.json@af777f44; reviewed WI-060 design and integration when available.
- **Done when:** Committed native record verifies matched density/envelope/geometry/current response plus unit-price sensitivities, preserves all eighteen verdicts and supports a bounded reading with complete provenance.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-003 start — 2026-09-15

Native study preparation · 20260915-tape-procurement-consistency · intake and execution scaffolding now; candidate-specific work held for integration.

### T-002 source/interface gate — 2026-09-15

Independent reviewer /root/reviewer returns PASS in evidence/design-review.md (current working artifact; pin on next commit). Original construction images and PDF captions support the conversion. Set-average conductor loading is distinct from reference-coil loading because f_set and f_wp_vol have different source meanings. The coordinator accepts fixed-factor transfer as an explicit approximation and asks implementation to test separate factor perturbations. Production implementation is released against WI-060 design and this qualification. Price and density mechanism choices remain agent-originated assumptions; no claim of qualified current margin is made.

### T-002 return — 2026-09-15

- **Outcome:** COMPLETE.
- **Evidence:** WI-060 implementation.md@8fa7665c; independent evidence/implementation-review.md (pinned with this return); package implemented at9e22a0a6 and unchanged by final consumer repairs.
- **Reading:** The physical inventory now determines purchased tape metres and selected procurement cost. Independent review supports the source, equations, interfaces, coherent generated/oracle behavior and repaired affected consumers. Existing static-validator residue and unqualified current-margin/fit assumptions remain explicit.
- **Decision:** Trigger: completed reviewed implementation and resolved observed regressions. Decision: invoke native integration to prove one candidate before study execution. Tier: execution detail. Decided by: coordinator under owner authorization. Changed: WI-060 and current executable/consumer records; exact paths and tests in the native report.

### T-004 scope

- **Objective:** Prove one study-ready integration candidate for the reviewed WI-060 package.
- **Why now:** T-002 returns independently reviewed coherent implementation.
- **Scope:** Invoke native scripts/integrate.py with audited WI-060, declared package identity and sealed runtime; no seam repair or new model work.
- **Inputs:** goal.md; WI-060@8fa7665c; implementation-review.md; expected executable02463b0d430bc205ee01809086441bc8d736b52c798c28f41689b308cbb226d0 and semantic ef1f4c896cd50cdfcf28872693a042a07254a2f4be5b2a3a35a61b70f4ee3040; sealed teax8d877460ac4f6f264561d916e40c1708adb13397.
- **Done when:** One native CANDIDATE or named BLOCKER return is retained.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-004 start — 2026-09-15

Native integration · evidence/T-004_integration/ · expected ten-gate CANDIDATE return or named blocker.

### T-004 return — 2026-09-15

- **Outcome:** PREREQUISITE.
- **Evidence:** evidence/T-004_integration/integration_return.json and recaptured.snapshot.json (pin with next evidence commit).
- **Reading:** Runtime pin, regeneration and handwritten preservation pass; census-snapshot refuses because the tracked native snapshot was not refreshed. The recapture has438attributes versus435in the old tracked snapshot; authority fields are unchanged. Later integration gates did not run. No candidate is promoted.
- **Decision:** Trigger: snapshot-drift refusal. Decision: route missing native snapshot refresh and reproducible preparation recipe correction to WI-060. Tier: execution detail. Decided by: coordinator. Changed: bounded T-005; no seam implementation repair.

### T-005 scope

- **Objective:** Complete WI-060's native snapshot preparation and show its correspondence to the already reviewed unchanged model/package.
- **Why now:** T-004 refused stale native snapshot provenance.
- **Scope:** Native snapshot capture, producer preparation recipe and related item evidence only; production equations, price basis and runtime unchanged. Same reviewer checks the corrective diff.
- **Inputs:** goal.md; WI-060@8fa7665c; T-004recapture and refusal.
- **Done when:** Committed current snapshot and reproducible preparation recipe pass focused review, ready for a new integration invocation.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-005 start — 2026-09-15

Native model completion repair · WI-060 · current native snapshot and corrected preparation recipe, with unchanged reviewed package identity.

### T-005 return — 2026-09-15

- **Outcome:** COMPLETE.
- **Evidence:** WI-060 snapshot-repair.json and implementation.md@cf3002f6; implementation-review.md focused addendum (pinned with this return).
- **Reading:** Native capture now exactly matches the refused integration's recapture; the preparation recipe includes that native operation. Authority and309checked model/package files are unchanged. Same-reviewer focused PASS covers the correction.
- **Decision:** Trigger: reviewed provenance repair. Decision: rerun integration with current audited item revision; scientific comparison unchanged. Tier: execution detail. Decided by: coordinator. Changed: tracked snapshot, preparation recipe and native evidence only.

### T-006 scope

- **Objective:** Prove one study-ready candidate after native snapshot completion.
- **Why now:** T-005 resolves T-004's named producer prerequisite.
- **Scope:** Native integration invocation only; no model, seam or runtime mutation.
- **Inputs:** goal.md; audited WI-060@cf3002f6; focused review addendum; same expected executable, semantic and sealed runtime identities as T-004.
- **Done when:** One CANDIDATE or named BLOCKER native return is retained.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-006 start — 2026-09-15

Native integration · evidence/T-006_integration/ · expected candidate from the snapshot-complete reviewed package.
