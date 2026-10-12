# Depth Rubric v1 — Stellarator Demo Model

**Created:** 2026-08-30
**Status:** Draft until frozen (frozen = committed; the grading cites this file's `path@sha`)
**Spec:** `.project/active/demo-depth-rubric/spec.md` · **Concept:** `.project/concepts/stellarator-demo-maturation.md`
**Provenance:** format, row structure, and grading protocol ratified [OWNER 2026-08-30] (format Q1: option A; grading Q2: option A). Ladder wording, row anchors, and target levels are [AGENT] proposals built from the design-evidence research (`.project/research/20260830-141348_demo-depth-rubric-design-evidence.md`).

## What this measures

The question this item answers: **which parts of our model are furthest below what a serious design effort would compute, so the first goal targets the worst one.**

Each row scores one functional area of the plant model on two independent 0–4 ladders: **P** (physics self-consistency — what is held, what is computed, what pushes back, what closes a loop) and **S** (structural & costing depth — part decomposition, cost granularity, lifecycle logic). The two never average. Each row declares a **target** level; the gap is `target − score`, not `4 − score` — a systems-level conceptual study does not need level 4 everywhere.

**Firewall (concept Key Concept 4):** this rubric contains depth prescriptions only — what a serious study models and how deeply. It contains no ARIES-CS-specific values or design facts; the four sealed PDFs were not read.

## The ladders

### Physics self-consistency (P)

| Level | Meaning | Evidence test |
|---|---|---|
| P0 | Absent | The behavior is not represented anywhere |
| P1 | Held | A cited value, lookup, or pass-through; changing upstream design does not re-derive it |
| P2 | Calculated | A forward calculation derives the governing output from declared design inputs, and its executable result is verified |
| P3 | Constrained & coupled | An executable constraint compares a **computed** operand to a physical/engineering limit, and the subsystem's choices feed back into plant feasibility or the operating point |
| P4 | Design-closed | The interacting physics close across the subsystem boundary, exercised in a design search, independently checked, and treated over a justified range or uncertainty model |

### Structural & costing depth (S)

| Level | Meaning | Evidence test |
|---|---|---|
| S0 | Absent / unmapped | No recognizable subsystem structure or cost home |
| S1 | Named aggregate | A lump, analogy, or single aggregate relation with a CAS home |
| S2 | Parametric | Cost follows one or more engineered quantities or performance drivers, with explicit CAS rollup and source basis |
| S3 | Decomposed lifecycle | Independently sized child components or subaccounts, rolling up through quantity / fabrication / installation / spares / replacement / maintenance logic appropriate to the subsystem |
| S4 | Design-based estimate | Decomposition tied to the engineered design, covering procurement–fabrication–installation–maintenance boundaries, stated estimate uncertainty or maturity, validated against an appropriate reference |

The S3/S4 boundary follows the cost-account literature's own line between a preferred bottom-up estimate from design details and the conceptual-study fallback of representative installed unit costs (`knowledge/sources/aries_cost_account_documentation/output.md:1040-1047`).

### Scoring rules

- A score is the **highest level whose full evidence test is satisfied**. Integers only; no half points; no partial credit by intuition.
- Missing evidence → `ungraded`, never 0. A dimension that genuinely does not apply → `not_applicable` with a one-line rationale.
- A bound value checked against another bound value is **not** P3 (current TBR is the type case: `models/designs/stellarator_09/stellarator_plant.sysml:922` fed to `tbr_ok` at `:939`).
- A plant-level constraint that merely reads an unrelated downstream number does not raise a subsystem's score.
- A calc declared in SysML but implemented through the handwritten codegen seam needs **both** the declaration and the executable implementation cited before it earns P2.
- Broad CAS arithmetic alone is not S3; a child-part tree whose members all inherit one lump cost is not S3.
- An axis nothing pushes back on is model underdevelopment, not a harmless limitation — [OWNER-VERBATIM] "if the user asks to study something and nothing pushes back — a signal the model is underdeveloped" (`modeling_project/STUDY_POLICY.md` §9).

## Rows and B-2 mapping

Rows are functional areas, not the part tree's 13 leaves (`models/designs/generic_mfe/mfe_plant.sysml:44-103`) — the plasma spine is not a leaf part, and fuel/tritium and availability have no leaf at all. Every row names its hook into the ratified B-2 frame (`.project/completed/20260821_demo-anchor-acceptance-spec/spec.md`, B-2) so the eventual reveal can join cleanly; two rows have **no** B-2 home, which is itself recorded here so those gaps cannot vanish from the reveal frame silently.

| Row | Area | B-2 hook | Principal model homes |
|---|---|---|---|
| 1 | Plasma geometry, fusion performance, operating-point closure | plasma/physics | `models/library/analyses/mfe_plasma_scaling.sysml` |
| 2 | Radial build, first wall, blanket, shield, TBR, lifetime | blanket/shield + radial-build ordering | `mfe_plasma_scaling.sysml:44,221`; `mfe_account_costs.sysml:22,52,794` |
| 3 | Magnets, structures, power supplies, cryogenics | magnets | `mfe_magnet_cost.sysml`; `mfe_power_core.sysml:65`; instance cryo chain |
| 4 | Heating, current drive, fueling, plasma control | heating | `mfe_account_costs.sysml:196`; instance `:499,645-678` |
| 5 | Divertor and plasma-facing maintenance | blanket/shield | `mfe_account_costs.sysml:168,794` |
| 6 | Vacuum vessel and vacuum systems | vessel | `mfe_account_costs.sysml:108` |
| 7 | Primary heat transport and plant power balance | power conversion (cross-cutting) | `mfe_power_balance.sysml`; `mfe_account_costs.sysml:526,559` |
| 8 | Power conversion, electric plant, heat rejection, misc BOP | power conversion + BOP | `mfe_account_costs.sysml:226`; instance `:493` |
| 9 | Buildings, site, hot cell, remote handling | buildings | `mfe_account_costs.sysml:304,366,476,503` |
| 10 | Fuel and tritium cycle | **none — absent from B-2; flagged** | `mfe_account_costs.sysml:730`; instance fuel block |
| 11 | Availability, scheduled replacement, maintenance, decommissioning | **none — cross-cutting; flagged** | instance `:812`; `mfe_account_costs.sysml:403,794` |
| 12 | Integrated CAS rollup, financing, LCOE, estimate quality | cost-account coverage (B-2 item 3) | `cas_hierarchy.sysml`; `mfe_account_costs.sysml:255,276,643,670,943` |

Unqualified filenames above and below live in `models/library/analyses/`; "instance" is `models/designs/stellarator_09/stellarator_plant.sysml`.

---

## Row 1 — Plasma geometry, fusion performance, operating-point closure

**Target: P3 / S: not_applicable.** A systems study solves an achievable operating point — field and heating determine density and temperature through a confinement relation, with a limit pushing back — rather than prescribing profiles. The known study pathology this closes: field adds cost and limits but is never rewarded, so the objective drives to the lowest field beta permits (`exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/synthesis.md:89-93`). S is not applicable: the plasma has no hardware or cost account of its own; its structure is the calc spine, and its cost lives in rows 3/4. **Gate note:** confinement/τ_E was deliberately ruled out of scope ("Rung C", `mfe_plasma_scaling.sysml:163`); a goal at this row proposes reopening it to the owner, never assumes it (concept Non-Goals).

| Level | Physics anchor (this row) |
|---|---|
| 0 | No plasma representation |
| 1 | Fusion power, beta, or peak field held as cited numbers; geometry passes through |
| 2 | Fusion power, beta, wall load, peak field forward-computed from geometry, profiles, and field, verified in execution |
| 3 | An achievable operating point: a confinement/transport relation links field and heating to density and temperature, and a beta, density, or power limit pushes back on the choice |
| 4 | Operating point closed jointly with magnets and heating, exercised in a design search, independently checked, sensitivity over a justified range |

## Row 2 — Radial build, first wall, blanket, shield, TBR, material lifetime

**Target: P3 (each subcell) / S3.** This row scores **three physics subcells** — (2a) build & wall load, (2b) in-vessel material lifetime, (2c) tritium breeding — because one cell would lie: replacement lifetime is genuinely computed from fluence ÷ wall load (`mfe_account_costs.sysml:794`) while TBR is a held constant checked against a held floor (instance `:922,939`). S3 reflects the standard conceptual-study structure: replaceable first wall/blanket/divertor units distinct from life-of-plant shield and structure, with replacement cost following component life (`knowledge/sources/aries_cost_account_documentation/output.md:1002-1038`).

| Level | Physics anchor (per subcell) | Structure & cost anchor |
|---|---|---|
| 0 | The behavior absent | No blanket/shield cost home |
| 1 | Thickness, lifetime, or TBR held as cited values | Lump in-vessel cost with a CAS home |
| 2 | 2a: build radii and wall load computed from geometry and power · 2b: lifetime computed from fluence and wall load · 2c: TBR computed from blanket configuration | Costs follow engineered volumes/areas with source basis |
| 3 | 2a: wall-load limit pushes back on the design · 2b: lifetime feeds replacement schedule and availability · 2c: computed TBR vs floor pushes back on blanket/build choices | Replaceable units vs life-of-plant components separately sized; replacement logic follows computed life |
| 4 | Neutronics/damage closure across the build, searched and independently checked | Design-based estimate per component class with fabrication basis and stated uncertainty |

## Row 3 — Magnets, structures, power supplies, cryogenics

**Target: P3 / S3.** A systems study computes coil sizing with stress or current-density limits pushing back, and costs the winding pack, structure, and cryoplant as separate accounts; full coil optimization and vendor-grade estimates (P4/S4) exceed conceptual scope. Magnet capital is the largest component channel and moved $4.39B → $6.32B on a single field errata, so depth here is load-bearing (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json`; `studies/DISCOVERY_LOG.md`). Current cost is conductor quantity × markup, the markup explicitly swallowing winding, quench protection, cryostat, and testing (`mfe_magnet_cost.sysml:4-60`).

| Level | Physics anchor (this row) | Structure & cost anchor |
|---|---|---|
| 0 | No magnet representation | No magnet cost home |
| 1 | Field a cited input; nothing derives it | Single lump cost with a CAS home |
| 2 | Peak field computed from geometry and coil current; cryo load computed from winding-pack heat | Cost follows an engineered quantity (e.g. conductor kA·m) with source basis |
| 3 | A stress or current-density limit pushes back on coil sizing and field choice | Winding pack, structure, power supplies, cryoplant costed as separately sized sub-accounts |
| 4 | Coil set closed with confinement and geometry in a design search, independently checked | Design-based estimate incl. fabrication/installation and stated uncertainty |

## Row 4 — Heating, current drive, fueling, plasma control

**Target: P2 / S2.** The honest near-term bar: the wall-plug → coupled-power chain computed and verified, cost following installed power with a source basis. P3 (required heating solved from plasma response, port/geometry limits pushing back) rides on row 1's confinement closure, which is owner-gated — if row 1 reopens, revisit this target.

| Level | Physics anchor (this row) | Structure & cost anchor |
|---|---|---|
| 0 | No heating representation | No heating cost home |
| 1 | Injected power and efficiencies held as cited constants | Lump cost with a CAS home |
| 2 | Wall-plug → coupled-power chain computed with a stated deposition assumption, verified | Cost follows installed heating power with source basis |
| 3 | Required heating solved from the plasma's response; a port, coupling, or geometry limit pushes back | Sources, transmission, launchers costed separately; replaceable components carry replacement logic |
| 4 | Deposition and current-drive closure with the plasma, searched and checked | Design-based estimate with stated uncertainty |

## Row 5 — Divertor and plasma-facing maintenance

**Target: P3 / S2.** A divertor heat-flux estimate with a limit pushing back is standard systems-code content; the cost share is small enough that parametric costing (S2) suffices at this stage. Currently the divertor shares the wall-load/lifetime context but has no constraint of its own (`mfe_account_costs.sysml:168-194,794`).

| Level | Physics anchor (this row) | Structure & cost anchor |
|---|---|---|
| 0 | No divertor representation | No divertor cost home |
| 1 | Divertor loads held or implied by a fixed share | Lump cost with a CAS home |
| 2 | Divertor heat flux estimated from exhaust power and geometry, verified | Cost follows divertor thermal power or area with source basis |
| 3 | A heat-flux or erosion limit pushes back on operation or geometry | Targets/cassettes as replaceable units with replacement logic from computed life |
| 4 | Exhaust/detachment closure, searched and checked | Design-based estimate with stated uncertainty |

## Row 6 — Vacuum vessel and vacuum systems

**Target: P2 / S2.** Forward-computed vessel sizing and gas-load/pumping estimates; structural or pumping constraints (P3) are beyond what a conceptual systems model needs first. The current cost definition explicitly omits gas-load pumping (`mfe_account_costs.sysml:108-138`).

| Level | Physics anchor (this row) | Structure & cost anchor |
|---|---|---|
| 0 | No vessel representation | No vessel cost home |
| 1 | Vessel dimensions held; vacuum system absent | Lump or volume-lump cost with a CAS home |
| 2 | Shell volume from the radial build and a computed gas-load/pumping estimate, verified | Cost follows computed shell volume/mass with source basis |
| 3 | A structural (pressure/disruption) or pumping-capacity limit pushes back | Shell, ports, pumping train as separately sized subaccounts |
| 4 | Structural + vacuum closure with the build, searched and checked | Design-based estimate with stated uncertainty |

## Row 7 — Primary heat transport and plant power balance

**Target: P3 / S3.** The strongest error-history signal in the repo: re-basing held pumping from 1 → 195 MW moved LCOE 21%, expanded the recirculation fence from 32 to 184 violating points, and exposed an unevaluable negative-net region (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md:31-43`). P3 means the loop is closed enough that `recirc_ok` receives computed operands — pumping from loop pressure drop and flow, not a held constant. **Gate note:** the owner ruled `p_pump` stays held (WI-033); a goal here respects that ruling or explicitly reopens it. S3 per the cost-account literature's separate heat-transport account: pumps, piping, IHX as sized subaccounts.

| Level | Physics anchor (this row) | Structure & cost anchor |
|---|---|---|
| 0 | No power balance | No heat-transport cost home |
| 1 | Pumping, parasitics, efficiencies held as cited constants | Coolant/aux-cooling lumps with CAS homes |
| 2 | Pumping and parasitic loads forward-computed from loop flow and pressure drop, verified | Costs follow loop thermal power or flow quantities with source basis |
| 3 | The computed loop feeds the recirculation/net-power constraints so coolant choices push back on feasibility | Pumps, piping, heat exchangers as separately sized subaccounts |
| 4 | Thermal-hydraulic state closure across the loop, searched and checked | Design-based estimate with stated uncertainty |

## Row 8 — Power conversion, electric plant, heat rejection, misc BOP

**Target: P2 / S2.** Cycle efficiency moved LCOE 13–23% in feasible space while equipment-rate changes moved it ≤1.1% (`exploration/stellarator_e2e/studies/20260821-power-cycle-ab/synthesis.md:63-76`) — so the physics side (a computed cycle, P2) matters more than deeper costing here. Currently `eta_th = 0.333` is held (instance `:493`).

| Level | Physics anchor (this row) | Structure & cost anchor |
|---|---|---|
| 0 | No conversion representation | No BOP cost homes |
| 1 | Thermal efficiency held as a cited constant | Power-scaled lumps with CAS homes |
| 2 | Cycle efficiency computed from coolant outlet temperature and a stated cycle model, verified | Costs follow computed gross/net power with source basis |
| 3 | Cycle responds to blanket/coolant temperature with a materials or temperature limit pushing back | Turbine island, electrical plant, heat sink as separately sized subaccounts |
| 4 | Thermodynamic state closure with the primary loop, searched and checked | Design-based estimate with stated uncertainty |

## Row 9 — Buildings, site, hot cell, remote handling

**Target: P: not_applicable / S3.** Buildings carry no plasma physics; their depth is structural — a conceptual study sizes building volumes from what they must contain (power core dimensions, hot-cell throughput, RH equipment paths). Currently six grouped bases scale with power (`mfe_account_costs.sysml:304-364`). The known CAS10 negative-net evaluability defect is an evidence-integrity finding, not a depth level (see Grading protocol).

| Level | Structure & cost anchor (this row) |
|---|---|
| 0 | No buildings cost home |
| 1 | A single site lump |
| 2 | Grouped building bases scaled by plant power with source basis |
| 3 | Building set sized by volume/function from layout drivers, incl. hot cell and remote-handling facilities |
| 4 | Design-based estimate from layout with stated uncertainty |

## Row 10 — Fuel and tritium cycle

**Target: P2 / S2.** Currently annual fuel cost follows fusion energy with held burn fraction, recovery, and availability (`mfe_account_costs.sysml:730-792`); no inventory, startup, processing throughput, or decay exists anywhere. **Flag: this area has no B-2 home — a serious study models the fuel cycle; its absence from the reveal frame is recorded here so it cannot disappear by aggregation.** TBR feedback belongs to row 2c; self-sufficiency coupling (P3) would join the two.

| Level | Physics anchor (this row) | Structure & cost anchor |
|---|---|---|
| 0 | No fuel-cycle representation beyond a cost line | No fuel cost home |
| 1 | Annual feed from fusion energy with held burn/recovery fractions | Annual fuel cost line with a CAS home |
| 2 | Tritium inventory, startup requirement, and processing throughput forward-computed, verified | Processing-plant cost follows computed throughput with source basis |
| 3 | Self-sufficiency couples TBR, inventory, decay, and availability, and pushes back on feasibility | Processing subsystems as separately sized subaccounts |
| 4 | Full fuel-cycle closure, searched and checked | Design-based estimate with stated uncertainty |

## Row 11 — Availability, scheduled replacement, maintenance, decommissioning

**Target: P3 / S2.** The committed study finding: `availability` has `no_constraint_response` — nothing couples it to core life or replacement outage (`exploration/stellarator_e2e/studies/20260821-power-cycle-ab/synthesis.md:159-170`), while availability = 0.85 is held (instance `:812`). P3 closes exactly that: availability derived from the computed replacement schedule and outage durations, feeding the economics. The scheduled-component-replacement account with lifetime and availability factored in is standard conceptual-study content (`knowledge/sources/aries_cost_account_documentation/output.md:4431-4448`).

| Level | Physics anchor (this row) | Structure & cost anchor |
|---|---|---|
| 0 | No availability/maintenance representation | No replacement or O&M cost home |
| 1 | Availability held as a cited constant | O&M and replacement as lumps with CAS homes |
| 2 | Outage durations and replacement schedule computed from component lifetimes, verified | Levelized replacement follows computed component life |
| 3 | Availability derived from the maintenance/replacement schedule and feeds the economics, pushing back on design choices | Replacement per component class plus decomposed O&M and decommissioning |
| 4 | Maintenance sequence/logistics closure, searched and checked | Design-based lifecycle estimate with stated uncertainty |

## Row 12 — Integrated CAS rollup, financing, LCOE, estimate quality

**Target: P: not_applicable / S3.** The economics layer's depth is structural. Currently: 2-digit CAS coverage with contingency, indirects, IDC, levelization, and a comparison-form LCOE all computed (`mfe_account_costs.sysml:255-964`) — but deterministic point assumptions throughout, with no estimate class, parameter uncertainty, or schedule risk. S3 asks for 3-digit functional accounts where cost concentrates plus a stated estimate-maturity/uncertainty treatment, per the functional account structure the literature recommends (`knowledge/sources/aries_cost_account_documentation/output.md:239-253`).

| Level | Structure & cost anchor (this row) |
|---|---|
| 0 | No cost rollup |
| 1 | A top-level total only |
| 2 | 2-digit CAS coverage with computed contingency, indirects, IDC, levelization, and LCOE |
| 3 | 3-digit functional subaccounts where cost concentrates, plus a stated estimate class and uncertainty treatment |
| 4 | Bottom-up estimate with risk, correlation, and schedule treatment, validated against a reference |

---

## Grading protocol — [OWNER 2026-08-30, Q2: option A]

1. **Freeze first.** No score is recorded until this rubric is committed; every grading cites the rubric `path@sha`, the model commit, and — for any executed claim — the package identity of the current baseline (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json` or later equivalent).
2. **Fresh non-author grader.** A separate agent session that did not author this rubric produces the initial scores. The author supplies the evidence map (`evidence-map.md`, pointers only — no proposed scores). Merely knowing evidence exists is not reading it: the grader cites what it read.
3. **Evidence authority.** Canonical `models/` files prove declared structure and equations; the package contract and executed baseline/study artifacts prove runtime identity and values; the discovery log proves error history; source documents justify target anchors. Stale comments and superseded pins never override current executed evidence.
4. **Cell record.** Each cell records: `cell_id` (e.g. `R3.P`), `rubric_version` (path@sha), `model_version`, `score` (integer, `ungraded`, or `not_applicable`), `anchor_satisfied` (the exact anchor text met), `model_evidence` (path:line), `runtime_evidence` (where the claim requires behavior), `study_evidence` (where load-bearing behavior was observed), `why_not_next` (one sentence on the missing evidence for the next level), `grader`.
5. **Disagreements.** Preserved as `author_reading` / `grader_score` / `resolution`; resolved by applying the written anchor or by revising the rubric in a new version. Never averaged.
6. **Correctness defects** (e.g. the CAS10 negative-net masking, `.../20260829-p-pump-fence/synthesis.md:77-89`) do not block a score and do not become a level: they are recorded as evidence-integrity findings attached to the affected cells.
7. **Re-grades.** Same rubric sha + new model sha = a valid progress comparison. A new rubric version re-scores both old and new model states before claiming a delta. An old grading is never edited in place.

## Versioning

This is v1. Revision policy pre-reveal is an open owner decision (concept open question 6); until ruled, any change produces a new version committed at its own `path@sha` with deltas restated.
