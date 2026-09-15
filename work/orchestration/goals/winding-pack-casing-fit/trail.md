# Trail: Winding-pack/casing fit

## Round 1 — conditional-local-cross-section

### Strategy revision — 2026-09-15

- **Approach:** Establish admissible local cross-section evidence, then test a declared available-space envelope independent of demand.
- **Assumptions:** A conditional two-dimensional local screen can be useful even without device drawings; independent review must check its represented geometry and ownership.
- **Abandonment conditions:** Evidence invalidates local-envelope use or the implementation cannot preserve old predicate/accounting meanings.
- **Intended model increment:** Explicit required/available dimensions, margins and fit predicate with domain checks.
- **Intended study question:** Which entering-reference and enlarged-pack cases fail fit, and does the sampled cheapest feasible choice change?

### T-001 scope

- **Objective:** Establish cross-section, insulation and clearance evidence sufficient to define a conditional fit screen.
- **Why now:** Entering tape-procurement answer identifies unknown fit after physical inventory enlargement.
- **Scope:** Admissible internal and bounded external reference geometry research; no production model changes.
- **Inputs:** `goal.md`; entering source and WI records cited there.
- **Done when:** Evidence distinguishes sourced geometry from engineering assumptions and identifies needed device measurements.
- **Stop when:** Strategy blocker, unresolved owner gate or declared limit.

### T-001 start — 2026-09-15

Research · `evidence/geometry-research.md` and native research requests/returns · admissible geometry basis and limitations.

### T-002 scope

- **Objective:** Prepare the native fit-screen requirement and interface design against current pack sizing.
- **Why now:** The affected ownership can be investigated independently of research values.
- **Scope:** Native PM registration, spec/design and dependency investigation only; production implementation waits for T-001 evidence and independent review.
- **Inputs:** `goal.md`, WI-038/040/059/060 records and current model/package.
- **Done when:** A reviewable design names geometry, domains, consumers and verification strategy.
- **Stop when:** Strategy blocker, owner gate or declared limit.

### T-002 start — 2026-09-15

Native model design · new standard work item · spec/design and consumer inventory. Parallel with T-001: research owns sources; design owns work-item records; neither writes production. Coordinator owns trail, entering capture, integration and study.

### T-001 return — 2026-09-15

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/geometry-research.md` (unpinned; no native digest until checkpoint); native `knowledge/research/requests/runs/REQ-FIT-01/20260915T194514322676/return.json` (same checkpoint pending).
- **Reading:** Source pack sizing and internal insulation have an unresolved inclusion convention; no device-specific cavity is established. The available allocation can be conditional without claiming qualified device fit.
- **Decision:** Missing cavity evidence · use explicit conditional geometry and sensitivity under owner delegation · execution detail · coordinator · WI-061 design. Registration-title defect and failed-attempt queue are disclosed in the report; captured source identity is explicit.
- **Decision:** Existing 0.30 m radial layer is smaller than nominal 0.36 m pack · interpret that held allocation conditionally as casing exterior and report its reference failure rather than enlarging it to pass · premise surprise · coordinator under owner's explicit instruction to use engineering judgment and report reference failure · WI-061 design. Device-specific fit claim remains parked pending drawings; conditional screen proceeds.

### Amendment 2026-09-15 — entering evidence extension

The entering comparison at `d64aea81` is preserved. Additional radial-allocation oracle comparisons are captured before production edits in `evidence/entering/allocation-comparison.json`; the capture-only mapping exposes the already public coil thickness input to an already existing oracle equation. These are oracle comparisons, not native old-package reruns. They permit causal accounting comparisons in allocation sensitivities as well as the original matched sample.

### T-002 return — 2026-09-15

- **Outcome:** COMPLETE.
- **Evidence:** `work/active/WI-061_winding-pack-casing-fit/design.md@677d6d31`; `evidence/design-review.md` (unpinned; no native digest until review checkpoint).
- **Reading:** Independent source/math/interface review accepts the conditional local-envelope design and expected reference failure. It does not qualify a real cavity, insulation inclusion, wall strength or unchanged thermal/stress proxy accuracy.
- **Decision:** New geometry/interface risk · independent reviewer checks original figures and arithmetic before production · execution detail · reviewer fit_reviewer, released by coordinator · design-review.md. Author will resolve editorial terminology before implementation; no new semantic choice is required.

### T-003 scope

- **Objective:** Implement and validate the reviewed fit screen through native WI-061.
- **Why now:** T-001 evidence and T-002 independent review support a bounded conditional screen.
- **Scope:** Reviewed canonical/twin model, generated package, native predicate, oracle and affected consumers; preserve old accounting and predicates.
- **Inputs:** `goal.md`; WI-061 at `677d6d31`; `evidence/design-review.md`; entering evidence at `d64aea81` and `1b521a71`.
- **Done when:** Native implementation and affected tests pass with declared residue and independent integrated coverage.
- **Stop when:** Prerequisite, strategy blocker, reserved gate or declared limit.

### T-003 start — 2026-09-15

Native implementation · WI-061 and its package consumers · reviewed implementation report and executable evidence. Author owns production/package/oracle/current tests; coordinator owns trail and integration; study preparation remains held.
