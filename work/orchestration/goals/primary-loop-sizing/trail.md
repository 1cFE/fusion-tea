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

### T-003 interpretation clarification — 2026-09-16

- **Trigger:** Native verification found that the inherited divertor capital correlation changes as loop pumping work changes plant thermal power, although divertor heat quantities and verdicts remain fixed.
- **Decision and reason:** Preserve and report that indirect cost response under the already scoped shared power/accounting consequences. Narrow the preservation statement to magnet outputs, divertor heat-account outputs and their predicates. No target redesign or realized equipment saving is inferred.
- **Tier:** execution detail; this is the existing thermal-power dependency, not changed comparison meaning.
- **Decided by:** coordinator, after study executor surfaced the observation.
- **What changed:** T-003 report/preservation checks clarify their claim; no model or input changes.

### T-003 return — 2026-09-16

- **Outcome:** COMPLETE.
- **Evidence:** Native study `exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/record.md@75772eba`, immutable snapshot/results at the same commit; executor `synthesis.md` (unpinned; no native digest until closure checkpoint); `evidence/commit-custody.json`.
- **Reading:** The frozen diagnostic quantifies the adopted capacity crossing and required equipment/duties while preserving separate failures. Full scalar/predicate comparison, native-store joins and artifact custody pass. Existing economic responses do not include a defensible installation price; source-backed qualification and cost gaps remain the result's boundary.
- **Decision:** Valid study reading obtained · close this round under the runbook and submit remaining integrated answer/dispositions for independent review · execution detail · coordinator · Round 1 result below.

### Round 1 result — 2026-09-16

- **Intent:** Met under the owner's accepted quantified-requirement/evidence-gap branch. Explicit native loop-count configurations were evaluated; physical routing/area and installed-price laws remain unsupported. No new model implementation was justified by the evidence.
- **Task sequence:** T-001 research/source review COMPLETE; T-002 independent package integration COMPLETE (ran alongside T-001); T-003 native study and executor reading COMPLETE. One verified pin and one committed study. The bounded research continuation used the documented local-PDF path after identifying DNS failure; no seam repair or scientific retry occurred.
- **Last semantic outcome:** COMPLETE, valid native study reading with conditional capacity requirement and named evidence gaps.
- **Stop reason:** Valid study reading plus no reached limit closes Round 1. Technical answer is ready for final assurance; formal goal close remains owner-held.
- **Evidence refs:** Source/integration checkpoint `df41ea97`; study `75772eba`; `answer.md`, executor synthesis, `evidence/finding-dispositions.md`, `prior-findings-map.json`, `commit-custody.json` and coordinator checks (new files unpinned; no native digest until closure checkpoint).
- **Learning delta:** Proposed L-001: sixteen average modules solve the informative reference-flow screen while the divertor still fails. Proposed L-002: current power-scaled coolant costs cannot price added loop equipment; annual break-even burden is a separate conditional diagnostic. Proposed L-003: nominal heterogeneous source circuits support a reduced count comparison, not a qualified geometry/area transfer or installed exchanger/compressor capacity.
- **Finding dispositions:** Four new study findings and fourteen earlier findings touched by the source/comparison evidence are mapped in `evidence/finding-dispositions.md`. Proposed routes retain all physical/cost residual gaps; append joined updates after final review. No new semantic follow-up executes from these dispositions.
- **Cited-ref liveness:** Model, package and prior native study evidence have not changed from the entering revision. Research registration and this goal's new artifacts are scoped work; pre-existing unrelated untracked user files remain untouched.

### Round 1 review — 2026-09-16

- **Reviewer:** Fresh independent source/math reviewer, continued for integrated assurance; `evidence/final-review.md`.
- **Verdict:** PASS for the owner's quantified-requirement/evidence-gap branch. This is not a priced or engineering-qualified installation.
- **Checks:** Source/math and cost coverage reused; all 168 snapshot artifact hashes and all 174 retained files checked against frozen study `75772eba`; baseline/twenty-case native stores joined; five entering controls exactly preserved; fresh 4520 scalar and 400 predicate comparisons; all twenty hydraulic/equipment/annual-cost accounts independently recomputed. No model/package mutation from entering revision; unchanged twenty constraints and source/qualification caveats retained. Sixteen numeric outputs outside oracle mapping and the integration read-set omission remain disclosed.
- **Learning delta:** L-001–L-003 accepted and appended to learnings.md. Four new and fourteen prior finding dispositions accepted; eighteen joined updates appended without editing first sightings. Study record receives only an addendum and retained review, with immutable results/snapshot untouched.
- **Next:** Technical work is complete under the accepted evidence-gap outcome. Recommend owner-held formal closure. Any later hardware qualification or installed pricing needs the missing evidence named in answer.md; no further round is needed to report this result.

## Goal close — 2026-09-16

- **Authority:** [OWNER-VERBATIM] “close it”. The owner authorizes formal goal closure after confirmation that independent review passed and that technical work was complete through the accepted evidence-gap outcome.
- **Decision:** Close `primary-loop-sizing` on the reviewed answer at `305cb0da`, with source checkpoint `df41ea97` and frozen native study `75772eba`. Independent final PASS is `evidence/final-review.md@305cb0da`.
- **Outcome:** The required representative-loop accommodation and its hydraulic/equipment consequences are quantified. Installed price and engineering qualification remain the explicit gaps recorded in `answer.md`; a loop-screen pass does not establish combined feasibility.
- **Recorded changes:** Goal status and project context updated. This is administrative closure; no new round, study, model change or native item archival is required.
