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
