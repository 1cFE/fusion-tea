# Trail: layout-based facilities

## Round 1 — equipment-and-maintenance-layout

### Strategy revision — 2026-09-18

- **Approach:** [AGENT] Inventory current accounts and equipment/calendar evidence; use the simplest defensible parameterized facility layout supported by admissible source evidence, with explicit assumed clearances and process durations.
- **Assumptions:** Existing reactor/component geometry and replacement schedules can supply useful size and demand drivers; applicable sources may establish facility and handling cost boundaries.
- **Abandonment conditions:** Source evidence cannot justify essential facility/cost transfers; the necessary removal concept changes the plant concept; or capacity conflicts require an owner scientific decision.
- **Intended model increment:** Layout-driven buildings and maintenance facilities replace grouped power estimates where justified, with missing scope separately identified and priced only on an explicit basis.
- **Intended study question:** How do equipment dimensions and maintenance demand change facility size, capacity, plant cost and electricity cost under matched assumptions?

### T-001 scope

- **Objective:** Establish current facility accounts, equipment dimensions, maintenance inputs and admissible internal source coverage.
- **Why now:** The assessment predates completed cooling-equipment work; implementation must start from the actual entering model.
- **Scope:** Read-only model/history/source inventory and native evidence reports; no model changes or external acquisition yet.
- **Inputs:** `goal.md`, original prompt, assessment references, current model, cooling and plant-closure records, source registry; quarantine applies.
- **Done when:** Account/envelope/calendar map and specific evidence gaps support a defensible next task.
- **Stop when:** Barred-source exposure, conflicting active file ownership or a material premise decision needs escalation.

### T-001 start — 2026-09-18

Inventory current accounts and evidence · `evidence/inventory.md`, `evidence/internal-sources.md` · bounded fresh readers with disjoint output ownership. Readers may run in parallel because both are read-only on shared native state; neither may implement changes or acquire/register sources. Coordinator owns all goal records and integration.

### T-002 scope

- **Objective:** Establish an admissible original basis for volume/function facility costs and their installation/services/shielding boundaries.
- **Why now:** T-001 preliminary evidence identifies registered PROCESS defaults with mixed model vintages and inconsistent unit labels; adopting the numbers without tracing actual equations would be unsound.
- **Scope:** Native bounded research acquisition for building cost methods and primary reference basis; no model edits or invented rate calibration.
- **Inputs:** `goal.md`, registered PROCESS cost-variable source and T-001 source-reader findings; quarantine applies.
- **Done when:** Registered evidence supports applicable rates/boundaries with limitations, or a concrete source gap is documented.
- **Stop when:** Acquisition cap, barred candidate, required owner decision or seam prerequisite.

### T-002 start — 2026-09-18

Facility cost-source acquisition · `knowledge/research/requests/REQ-LBF-01.json` · native source/run receipts and `evidence/cost-source-basis.md`. Independent of T-001 read-only inventory; sole registry writer is the cost researcher, coordinator does not register concurrently.

### T-001 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/inventory.md`, `evidence/internal-sources.md`, `evidence/entering-state.json` (unpinned; no native digest).
- **Reading:** Current facility costs remain power-based after cooling and breeding advances. Source sector-splitting functions support a conceptual layout, while processing times, storage duration and some external equipment envelopes require explicit assumptions. Fourteen is the current circuit count; eighteen is a separately retained study case.
- **Decision:** Evidence supports a bounded native modeling item; [AGENT] coordinator chooses one cohesive facility-layout/capacity/account outcome, with substantial implementation parked pending source/design review. Tier: execution detail. New item/spec follows in T-003.

### T-003 scope

- **Objective:** Specify and design an executable conceptual facility layout, maintenance-capacity screen and cost-account replacement.
- **Why now:** T-001 established available equipment/calendar interfaces and missing inputs; T-002 is resolving the cost-source basis.
- **Scope:** Native work registration, written requirements, explicit proposed layout/capacity equations and assumption table, and a fresh preimplementation review. No substantial implementation until source interpretation and design are reviewed.
- **Inputs:** `goal.md`, T-001 reports, original Stellaris section2.11/Figure54 and relevant radial-build/calendar interfaces; incorporate T-002 when available.
- **Done when:** Reviewer confirms a defensible conceptual design with recorded limitations or identifies a concrete blocking scientific/scope decision.
- **Stop when:** Essential source/geometry/capacity evidence fails or owner judgment is required.

### T-003 start — 2026-09-18

Native facility modeling specification/design · new standard item under `work/active/` · spec, design, persistent implementation checklist and independent source/design review. Requirements can be captured while T-002 runs; cost-dependent conclusions remain provisional until its return.
