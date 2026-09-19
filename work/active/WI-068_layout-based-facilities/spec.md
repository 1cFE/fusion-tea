---
Status: active
Scale: standard
Epic: standalone
Owner: reid
Created: 2026-09-18
Updated: 2026-09-18
---

# Layout-based facilities

## Problem and intended use

[NEED] Derive building and maintenance-facility sizes and costs from the equipment they contain and work they support. The owner requests the unchanged R9.S3 target before the ARIES comparison. Current CAS21 uses six grouped power/fixed/staff expressions; remote handling and radwaste retain separate equipment allowances. Source-supported sector splitting and newly dimensioned cooling exchangers provide physical drivers, while some envelopes and process times remain assumptions.

[NEED] Engineer-readable deliverables must distinguish a plausible conceptual layout from qualified construction/maintenance design and distinguish adding missing scope from changing design. Lower cost is not acceptance. Original authority: `work/orchestration/goals/layout-based-facilities/evidence/owner-prompt.md`.

## Required reading

- `knowledge/holdout/aries-cs/PROTOCOL.md`; no barred source/derivative or excluded concept may be read.
- `work/orchestration/goals/layout-based-facilities/goal.md` and its original owner prompt.
- Goal `evidence/inventory.md`, `evidence/internal-sources.md`, `evidence/entering-state.json` and forthcoming cost-source basis.
- `modeling_project/MODELING_PROCESS.md`, `MODELING_GUIDE.md`, `REQUIREMENTS.md`; `.agentic-mbse/codex.md`, `.project/codex-test-setup.md`.

## Requirements and acceptance

| ID | Requirement | Required evidence |
|---|---|---|
| LF-01 | [NEED] Define existing and proposed facility/account boundaries, preserving named functions and separating structures, shielding, services and handling equipment where evidence permits. | Replaced/retained/added account map including CAS10/21/22/29/30/50/71/72, reactor shielding, cooling installation and decommissioning. No duplicate charged scope. |
| LF-02 | [NEED] Derive an explicit conceptual layout from equipment dimensions, removal envelopes, access paths, assembly/service requirements and justified clearances. | Dimension equations and visible facility/route arrangement; every input marked calculated, source-supported or assumed. No precision inferred from unscaled diagrams. |
| LF-03 | [NEED] Calculate receipt/storage/processing/handling capacity from component sizes, replacement quantities and schedules. | Explicit process/dwell/simultaneity assumptions, peak inventory, resource occupancy and outage/throughput checks; hot cell and handling space respond to requirements. |
| LF-04 | [NEED] Connect facility geometry/functions to applicable sourced costs, keeping currency/year, installed/purchased scope and uncertainty. | Original-source/units/transfer review, arithmetic reconstruction and services/shielding treatment. An arbitrary volume coefficient is insufficient. |
| LF-05 | [NEED] Integrate dimensions and costs into model components and executable CAS/LCOE. | Normal supported inputs change facility size and cost; account totals reconcile; facilities consume actual equipment quantities and calendar interfaces. |
| LF-06 | [HARD] Preserve calendar availability and maintenance requirements. Report layout/schedule conflicts. | Unchanged calendar/energy outputs for cost-only matched cases; failing facility capacity is retained, never converted into lower maintenance needs. Cooling event dates remain distinct from bundled in-vessel events. |
| LF-07 | [NEED] Verify dimensions, capacity, costs and account totals independently and check affected consumers. | Original admissible example checks, geometric bounds, schedule/storage counterexamples, numerical/account identities, native validation and targeted regressions with limitations. |
| LF-08 | [NEED] Run focused matched study of equipment size and maintenance demand. | Current-default and informative selected cases, old/new cost-only attribution, supported geometry/demand contrasts, important assumptions and infeasible layouts; total plant cost and electricity cost consequences. No optimization on unsupported clearance or throughput. |
| LF-09 | [NEED] Obtain fresh preimplementation review and fresh independent unchanged R9.S assessment. | Reviewer inspects actual source/design assumptions, capacity logic, accounting and executed building/hot-cell/handling response. S3 verdict may be adverse. |
| LF-10 | [HARD] Preserve quarantine, physical limits, rubric and published r2/historical results. | Separate versioned model/study evidence and preservation hashes. No merge/push or owner-held formal closure/reveal/freeze replacement. |

## Scope, ownership and supported use

[INFERRED] One cohesive standard modeling item owns facility layout, capacity and resulting account integration. Reusable equations belong in library analyses; identifiable facilities and function-specific costs belong to component occurrences. Stellarator geometry/clearance/process assumptions belong in its instance. Calendar remains the sole producer of in-vessel replacement timing. Cooling remains the owner of its dimensions, counts and equipment/lifecycle costs; only necessary read-only exposures may be added.

[INFERRED] Expected affected consumers are generic MFE buildings/CAS21, remote-handling cost/CAS22 if a justified replacement is found, CAS10 site if layout land is adopted, cost rollups, all inherited MFE instances, generated model twins/package, oracle, census, manifest and study exports. Preserve legacy/default behavior for other concepts through an explicit dormant-safe mode if needed. Inspect actual inheritance before editing.

[NEED] Conceptual sizing does not establish licensed shielding, floor/rail structural qualification, complete nonaxisymmetric clearance, machine design or a full maintenance operating procedure. State unsupported upstream envelopes and residual costs clearly. Unqualified dimensions must not be silently treated as equipment calculations.

## Open design questions

- [INFERRED] Select a conservative sector/removal envelope tied to live radial geometry, with explicit allowance for unmodeled cryostat/support shape; preserve ground transport and clean/dirty separation.
- [INFERRED] Choose and justify component segmentation, process/storage scenarios and capacity policy. Required capacity and offered capacity must be distinguishable so impossible schedules remain reportable.
- [INFERRED] Resolve original facility rate basis, price year and scope before choosing cost method. Preserve retained residual allowances transparently; their presence is not proof every facility is sized.
- [INFERRED] Independently review any historical cost transfer and proposed interpretation of source maintenance functions before substantial implementation.

## Process and completion evidence

[INFERRED] Separate design and persistent plan are appropriate because source interpretation, new ownership and a coupled capacity/account model need review and interruption recovery. Source inventory completed under T-001; cost acquisition runs under T-002. Design and review are T-003. Native implementation, integration and study follow only on reviewed evidence. No approval of new domain insights is inferred from source registration.
