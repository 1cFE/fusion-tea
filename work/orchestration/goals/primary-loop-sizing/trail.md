# Trail: Explicit primary-loop cooling-system sizing

## Round 1 — size-the-representative-circuit

### Strategy revision — 2026-09-16

- **Approach:** Trace the representative helium circuit and separate its reference configuration from physical limits; use supported equipment replication or geometry changes to connect installed capacity to pumping and cost.
- **Assumptions:** The existing source and prior implementation can support at least a quantified accommodation requirement. Equipment sizing and pricing may have narrower evidence than the hydraulic law.
- **Abandonment conditions:** A source contradiction invalidates the representative circuit, an unresolved interpretation changes comparison meaning, or admissible evidence cannot support the proposed physical transfer.
- **Intended model increment:** Explicit supported cooling-system sizing and its consequences; unsupported options remain quantified requirements with evidence gaps.
- **Intended study question:** What accommodation does each named case need, what does it do to heat removal, pumping and cost, and which independent constraints still fail?

### T-001 scope

- **Objective:** Establish the existing hydraulic/equipment/cost chain and the evidence supporting capacity changes.
- **Why now:** The confirmed goal identifies a reference-configuration flow ceiling and asks for physically and economically consistent accommodation.
- **Scope:** Internal source and implementation trace; bounded external acquisition if the native evidence exposes a precise gap. No model changes in this task.
- **Inputs:** `goal.md`; entering model, prior loop implementation, registered source index and prior research cited there, all at entering revision `b9ddffb77527b982d438d41685c296e69a4a34de`.
- **Done when:** A source-linked account distinguishes supported sizing choices from quantified requirements and evidence gaps, with independent coverage of new source/math interpretations.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-001 start — 2026-09-16

T-001 · native research workflow and read-only implementation trace · expected source-linked research account and focused review.

### T-002 scope

- **Objective:** Verify the unchanged entering package as a candidate for the bounded cooling diagnostic.
- **Why now:** T-001 has established that loop count is already a native causal input. Package verification is independent of pending cost acquisition and scientific interpretation review.
- **Scope:** Invoke the native integration seam against the existing WI-065 audited package; no regeneration repair or model changes. T-001 owns research only, so there is no shared-write conflict with integration evidence.
- **Inputs:** `goal.md`; WI-065 audit and existing integration command at `b9ddffb77527b982d438d41685c296e69a4a34de`; current unchanged package/manifest/census.
- **Done when:** Ten native gates return one CANDIDATE or a named blocker.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-002 start — 2026-09-16

T-002 · scripts/integrate.py · expected evidence/T-002_integration/integration_return.json. Scientific execution remains dependent on T-001 review.

### T-002 return — 2026-09-16

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/T-002_integration/integration_return.json` and producer logs (unpinned; no native digest until checkpoint).
- **Reading:** All ten native gates pass for the unchanged entering package, pin `6e427038e8515501e9c42c39823f85e3b0bcbd9f54f830b2779a792851f02551`. The inherited integration read-set coverage omission remains explicitly unverified.
- **Decision:** Existing package already represents an integer loop-count choice and its heat/power consequences · use this one verified pin for a conditional diagnostic, while physical qualification and price remain research questions · execution detail · coordinator · T-003.

### T-003 scope

- **Objective:** Quantify required representative-loop accommodation and its hydraulic/power/accounting consequences at the named controls, separately from combined feasibility.
- **Why now:** Native count input exists; T-002 verifies its unchanged package. T-001 focused source review supports conditional count comparisons, subject to its account correction and recheck. Cost acquisition proceeds independently because no new price is used in this diagnostic.
- **Scope:** Native study at `exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/`, at most 25 points on one pin. Existing equations and all twenty constraints remain unchanged. Source-linked equipment counts and IHX duty requirements are explicitly conditional postprocessing. No qualified hardware design, area law or installed price is assumed.
- **Inputs:** `goal.md`; source-review and corrected hydraulic-source-account; T-002 CANDIDATE; five captured entering controls; `evidence/study-brief.md`.
- **Done when:** Frozen native study and synthesis quantify accommodation, preserve adverse predicates and distinguish aggregate model economics from missing equipment price.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-003 start — 2026-09-16

T-003 · native run-study workflow · expected study record, snapshot, result store and verification. Preparation may proceed; oracle/native evaluations wait for scientific recheck and coordinator release. Study worker owns only its new record and first-sighting rows; T-001 worker owns only research acquisition, so neither result can invalidate the other's declared numerical inputs and write scopes are disjoint.

### T-001 return — 2026-09-16

- **Outcome:** COMPLETE.
- **Evidence:** `knowledge/research/pending/20260916-064107_primary-loop-sizing.md`; `evidence/hydraulic-source-account.md`, `entering-cost-account.md`, `cost-research.md`, `source-review.md` (correction recheck PASS), `cost-review.md` (PASS); native REQ-LOOP-COST-01 and REQ-LOOP-COST-01-CONT returns and registered Barucca source (unpinned; no native digest until research checkpoint).
- **Reading:** Existing explicit loop count supports a conditional representative-circuit comparison. Nominal source flow is an adopted screen, not demonstrated maximum capacity; no changed allowance or new area law is warranted. Equipment topology, exchanger off-design qualification, drive losses and installed pricing remain unresolved. Original cost evidence identifies budgetary offers and the missing internal report, rather than a usable unit price. Initial opaque capture failures were diagnosed as DNS; bounded local-PDF continuation succeeded without seam repair.
- **Decision:** Existing model already carries supported count dependence, while geometry transfer and installed prices lack evidence · reuse its native input in T-003 and select the owner's quantified-requirement/evidence-gap outcome rather than invent a new sizing or cost law · execution detail · coordinator, with independent source/math coverage · no model change; T-003 and final answer.
- **Decision:** Native research report remains pending curation · do not mint or supersede domain insights without owner approval; registered sources remain directly citable · execution detail · coordinator · research report only.

### T-003 execution release — 2026-09-16

Coordinator inspected `exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/protocol.md`: eight complete groups all report constraints_reachable; no unresisted-axis ruling is needed. Source/math recheck PASS releases unchanged-equation count comparisons, and cost-review PASS releases only the optional annual break-even burden calculation under the existing generation convention. Execute baseline/preflight, scan integer counts 12–18 and select the engineered native window before running the twenty proposed cases. No new source equation, equipment price or acceptance threshold enters the package.
