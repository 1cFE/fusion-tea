# Trail: computed tritium breeding

## Round 1 — establish-physical-basis

### Strategy revision — 2026-09-18

- **Approach:** [AGENT] Trace the existing production/requirement/geometry interfaces and investigate admissible neutronics evidence for the retained blanket technology. Choose the simplest demonstrably predictive method after independent review.
- **Assumptions:** Existing sources or accessible independent calculations may support a bounded method; earlier deferral is not a technical impossibility proof.
- **Abandonment conditions:** No justified transferable relation/benchmark, missing essential physical inputs, or a material scientific choice requiring owner judgment.
- **Intended model increment:** Configuration-derived achieved breeding and an explicit adequacy predicate, conditional on evidence.
- **Intended study question:** Which supported blanket choices change breeding and plant consequences, and which satisfy the justified requirement?

### T-001 scope

- **Objective:** Establish current interfaces and the admissible physical-method evidence before choosing implementation.
- **Why now:** The grounding evidence identifies held achieved breeding and inconsistent requirement semantics.
- **Scope:** Read current model, generated implementation and admissible sources; research additional evidence through native procedures if required. No model edits in this task.
- **Inputs:** `goal.md`; owner-named grounding evidence; source registry, knowledge index and native research records.
- **Done when:** An evidence-backed method and validation proposal, a precise evidence gap, or a material owner decision is established.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-001 start — 2026-09-18

T-001 · native research and current-model trace · evidence report and method proposal. Independent read-only tracing and source research may run concurrently because neither changes shared interfaces; coordinator owns goal records and integrates findings sequentially.

### Research execution note — 2026-09-18

[AGENT] T-001's broad native request `REQ-computed-tritium-breeding-01` reached its six-query/three-capture bound after two registrations and one failed URL extraction. Its native return retains the failed URL as queued, although local-PDF registration resolved that same acquisition; this is bookkeeping residue, not a request for owner retrieval. A newly identified specific HCLL-surrogate thesis warrants the narrower `REQ-computed-tritium-breeding-02` (one capture, no additional search planned). This investigates a concrete candidate rather than declaring the initial limited search proof that no method exists. No model implementation is authorized by these source registrations alone.

### T-001 return — 2026-09-18

- **Outcome:** OWNER_GATE for plant integration; authorized source-domain research completed.
- **Evidence:** `knowledge/research/pending/20260918-130310_computed-tritium-breeding-methods.md`; native requests `REQ-computed-tritium-breeding-01` and `-02`; `evidence/current-trace.md`, `internal-source-assessment.md`, `hcll-surrogate-assessment.md`, `hcll_surrogate_probe.py`, `hcll-surrogate-probe-results.txt`, `threshold-check.json` and `method-review.md` (currently unpinned; no native digest).
- **Reading:** A recoverable, material-sensitive reduced model exists. Its physical validation and input domain do not cover the retained stellarator assembly. Missing transport software is not a blocker to source-domain reproduction. Integrating its output now would conceal extrapolation or change the blanket. The physical recovery interpretation remains conditional.
- **Decision:** New surrogate evidence overturns a presumed missing-executable obstacle · recover and test the source example without calibration · execution detail · coordinator · research probe and assessment above.
- **Decision:** Independent applicability review identifies current geometry outside the surrogate domain · park plant implementation and surface physical target selection · reserved gate · owner pending · question asks retained helium/PbLi build versus explicitly authorized redesign versus original water/PbLi target; no model, package, historical study or limit changed.
- **Decision:** Cost-derived recovery does not establish isotope recovery · preserve the conditional balance and old floor separately in the evidence, without changing either to create a pass · premise surprise already documented in the inherited model · coordinator · threshold diagnostic and research report.

### Round 1 result — 2026-09-18

- **Intent:** Met for identifying and testing a physical-method candidate; unmet for configuration-derived breeding in the retained plant and R2c.P3.
- **Task sequence:** T-001 research/trace → OWNER_GATE for integration, with source-domain prototype completed. No native modeling work item was created because no physical design was selected. Generation/integration/study stages do not yet apply; their scientific prerequisite remains unresolved.
- **Last semantic outcome:** OWNER_GATE.
- **Stop reason:** OWNER_GATE plus unresolved physical-target question → round closes on an owner gate that is not resolved.
- **Evidence refs:** Native research report and requests cited in T-001 return; original source paths and source hashes are carried by the native registration records. Current model refs remain at e78099cb93ab36b57debf70045cc9c4e7bcfcdd8. No pins or plant studies were promoted.
- **Learning delta:** Proposed: a published executable HCLL surrogate is available and responds to configuration, but its validated domain excludes the current build; source-domain reproduction does not qualify stellarator breeding. Proposed: fuel-balance semantics still prevent interpreting the old floor pass as self-sufficiency.
- **Finding dispositions:** No committed study discovery rows were consumed or modified. New findings live in the native research report. The owner's starting reports remain evidence; unrelated files and the frozen r2 archive remain untouched.

### Stop — 2026-09-18

- **Kind:** owner gate.
- **What is true on disk:** Grounded goal, completed research round, three native source registrations, executable source-domain probe and independent preimplementation review. No stellarator model or generated executable changes. Research report remains pending; no domain insight was promoted without owner review.
- **What the owner must see:** The physical-target question is pending. Retaining the present build needs matching material/geometry evidence; changing build or coolant is a reserved decision. Neither choice alone validates transfer. Fresh round assurance and a current R2c.P grade are being obtained on this result.

### Round 1 review — 2026-09-18

- **Reviewer:** Fresh non-author `/root/method_review`; continuing independent source/math/probe coverage reused within its unchanged scope.
- **Verdict:** PASS for the accurately bounded research result; OWNER_GATE and unmet goal remain.
- **Checks:** `evidence/round1-review-and-grade.md` verifies original source evidence, task scope, acquisition-recovery classification, native request returns, unchanged model/generated consumers, absence of plant study claims, and accepted learning delta. No consumed discovery rows needed disposition. The fresh unchanged-rubric grade is R2c.P1; P2 and P3 are both unmet.
- **Evidence reuse:** `evidence/method-review.md` and its source-probe addendum; reproducible original-C++ comparison at `evidence/verify_hcll_original_cpp.py` and `evidence/hcll-original-cpp-verification.json`.
- **Next:** Owner physical-target decision, then a new round with a matching strategy. No goal closure recommendation and no blanket substitution by the coordinator.

### Evidence checkpoint — 2026-09-18

Native research, registrations, probe, reviews and answer are committed at `f61c0b92`. Cite those paths at this revision to resolve the earlier unpinned-at-review evidence. The current model remains at the entering revision; no model/generated-package diff exists. Source-registry verification reports zero faults and three pre-existing legacy entries. Unrelated working-tree edits remain preserved; the new CURRENT_WORK entry is left unstaged with the owner's existing changes. No merge or push.

### Owner delegation — 2026-09-18

The owner delegates research and scientific judgment within the goal; see goal.md amendment. The previous physical-target gate no longer blocks execution. Round1 remains closed. Its finding that direct surrogate transfer is unsupported remains valid; the next strategy addresses that evidence gap.

## Round 2 — calculate-retained-blanket

### Strategy revision — 2026-09-18

- **Approach:** [AGENT] Retain helium/PbLi and the actual generic radial build. Pursue a reproducible fixed-source neutron-transport calculation with explicit materials and geometry, using source-domain benchmarks to measure physical approximation error before integrating the model.
- **Assumptions:** A public transport engine and evaluated nuclear data can be provisioned independently of the sealed plant runtime; sources can specify representative helium/PbLi internals. The current model's geometric abstraction may permit a bounded transport representation with measurable approximation error.
- **Abandonment conditions:** Benchmarks fail without defensible resolution, missing nuclear data/geometry prevents an attributable calculation, or approximation errors cannot justify any supported configuration.
- **Intended model increment:** Calculated breeding driven by actual blanket inputs, separately reported applicability/uncertainty, and an explicit conditional adequacy constraint using the retained fuel balance and design floor.
- **Intended study question:** How do supported thickness/enrichment/material choices change breeding adequacy and the affected build/cost/power quantities, including insufficient cases?

### T-002 scope

- **Objective:** Establish a reproducible transport route and a source-supported retained-blanket/benchmark specification.
- **Why now:** Round1 recovered a surrogate but demonstrated its domain excludes the current build. Owner delegates the next scientific choice.
- **Scope:** Research prototype only: isolate public transport tooling and nuclear data; recover source benchmark/material/geometry inputs; run bounded benchmark calculations if specification permits. Preserve sealed runtime, production models and archives.
- **Inputs:** goal.md amended authority; Round1 registered sources, method review and runtime probe; native research/source procedures.
- **Done when:** A runnable transport setup and reviewable benchmark/current-assembly method, or a concrete technical obstacle with attempted remedies.
- **Stop when:** Prerequisite, strategy blocker, genuine reserved gate or declared limit.

### T-002 start — 2026-09-18

T-002 · native research prototypes · transport setup and physical-method specification. Runtime provisioning and source/benchmark recovery are independent: tooling worker owns only isolated runtime/provisioning evidence; physics worker owns only source specification evidence; coordinator owns registrations, goal records and later integration.

### Round 2 execution note — 2026-09-18

T-002 continues. Isolated OpenMC 0.15.2 and pinned ENDF/B-VIII.0 processed data pass a plumbing smoke test (`evidence/round2/transport-runtime.md`); this is not physical validation. Fresh independent `method-precheck.md` releases transport prototype implementation with material, geometry/source/tally and benchmark acceptance conditions. The outer torus transmits into exterior void, avoiding erroneous loss of neutrons crossing the central hole. Research request03 acquires original IAEA sphere evidence and preserves two retrieval limitations: a migrated landing-page capture and unsupported text/plain resolved by a transparent mechanical PDF rendering. The native return retains a stale queued URL failure; the original text is now acquired and no owner retrieval is required.

[AGENT] WI-066 is registered with requirements and a persistent execution checklist at `work/active/WI-066_computed-tritium-breeding/spec.md`. Production implementation remains dependent on the scientific prototype acceptance. No model, generated package or historical result has changed.

### T-002 return — 2026-09-18

- **Outcome:** SUCCESS for the bounded method/runtime/benchmark task, not breeding-gap completion.
- **Evidence:** `evidence/round2/transport-runtime.md`, `physical-method-proposal.md`, `material-manifest-proposal.md/.json`, `method-precheck.md`, `benchmark/report.md`, `benchmark-and-interface-review.md`; native requests03/04/06. The independent review accepts limited integral experimental consistency and the conditional interface design. Exact experimental casing/penetrations and shaped-stellarator bias remain unresolved.
- **Results:** Approximate Li sphere0.697859 ±0.000489 versus measured0.685 ±0.03836; Pb/Li sphere0.504131 ±0.000478 versus measured0.530 ±0.03180. Errors are standard deviations with different meanings (Monte Carlo versus experiment). Eighteen cases retain the predeclared low-density Pb/Li comparison failure; no correction factor is fitted. These comparisons do not establish a plant uncertainty bound.
- **Decision:** Use a source-defined finite-torus transport scenario and a narrow validated thickness response at fixed70% Li-6 · delegated scientific judgment · coordinator. Pilot throughput motivates one supported executable lever; enrichment remains direct-transport sensitivity. No blanket technology or acceptance requirement changes.

### T-003 scope

- **Objective:** Implement and verify configuration-derived breeding and conditional adequacy through native WI-066, then produce a separately identified integrated package.
- **Why now:** Runtime, material cards, approximate independent integral checks and method/interface review are available. Numerical response release and plant applicability remain task acceptance conditions.
- **Scope:** Freeze an explicit opening/material/source scenario; direct-transport thickness nodes and withheld validation; physical sensitivities; canonical/twin SysML, generated executable, independent software oracle, guarded applicability, production/recovery/loss account, current metadata and targeted regression; independent completion assessment and native integration.
- **Inputs:** T-002 evidence and independent reviews; WI-066 spec/design; retained entering model and current consumers.
- **Done when:** Reviewed model evidence and a native integration CANDIDATE identify the supported package, or a precise unresolved blocker prevents that result.
- **Stop when:** Scientific validation fails without defensible remedy, applicable workflow prerequisite cannot be met, or a genuine reserved decision is encountered.

### T-003 start — 2026-09-18

T-003 · WI-066 native modeling · independently prechecked physics/interface. Transport author owns numerical evidence and immutable response data; model author owns canonical and twin SysML; coordinator owns generated/manual implementation, consumer integration and goal records. No transport result is accepted merely because the prototype executes. Expensive transport is bounded to the declared grid and sensitivities; failures are retained.

### T-003 implementation checkpoint — 2026-09-18

The independent physical/table release accepts the fixed-scenario thickness response; all five nodes and six withheld checks pass declared numerical criteria. Full scenario metadata travels inside the generated manual implementation and canonical asset. Strict fresh generation repeats exactly, with 27 prior manual implementations preserved and two added. The held achieved input retires; all 20 predicate identities remain. All 245 independent baseline oracle channels match; only the old fuel margin and TBR verdict change among existing baseline outputs. The reference numerical lower estimate1.186145581 fails the conditional1.190 requirement.

Focused verification passes117 breeding tests,93 affected model/consumer checks,19 compound-predicate checks and3 dependency checks. Static validation remains failed at Levels2/6; all32 newly added Level6 diagnostic identities are explicitly checked against actual generated bindings by the independent reviewer. The study-tool prerequisite now traces and independently re-derives conjunctions; both branches must supply evidence. The precommit full-verifier probe refuses package dirtiness, correctly; its receipt is retained and clean-package verification follows the audited commit. Research report `knowledge/research/pending/20260918-140121_computed-tritium-breeding-transport.md` and requests03/04/06/07 preserve sources, quantitative evidence and acquisition failures. No P3 or integration claim yet.
