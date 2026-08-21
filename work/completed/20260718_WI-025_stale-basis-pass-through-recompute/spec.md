---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-18
Updated: '2026-07-18'
---

# WI-025: STALE-BASIS Pass-Through Recompute

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — this is a stellarator-demo model-development item. The ARIES-CS hold-out is sealed; the §3 barred paths must not be read, cited, or opened. Admissible sources for this item: 1costingFE only (`/home/reid/1cfe/1costingfe`, pinned `0254385`) — cost formulas and constants, all admissible. No Stellaris physics sources are needed; no barred artifact was read at this spec.

**Alignment brief: `work/orchestration/stale-basis-recompute.md`** — objective, provenance grades, owner decisions, reserved checkpoint gates. This spec executes that brief. Related registration (same Align, deliberately **outside** this item's scope): WI-026 `Pytest Baseline Re-Record` (trivial, P3, standalone).

## Overview

The model carries three cost accounts as literals computed at powers the model no longer produces — the last three `STALE BASIS` annotations (grep-verified complete set). CAS21 buildings ($613.65 M) was computed at p_et 896.8 / p_th 2693.1 (pre-WI-019); CAS10 preconstruction ($33.896 M) and CAS70 annual O&M ($41.641 M/yr) at p_net 575.3 (WI-018). The executed p_net is now 915.081 MW, ~59% above that basis — the largest known honesty gap in the headline. This item rebinds all three as **forward-computed functions of the computed powers**, mirroring the 1costingFE formulas their doc comments already cite, and retires the STALE BASIS annotations.

**Settled, do not reopen** ([AGENT], ratified by owner 2026-07-18, Align): forward-computed, not point-recompute. Reasoning of record: literals would re-stale on the next power move, as already happened five times (575.3 → 786.1 → 578.0 → 804.1 → 915.1 → 915.081); powers are intermediate nodes, costs never feed back into the power balance (no cycle, no inversion); 1costingFE itself computes all three from powers; WI-021's CAS27 rebind is the in-model precedent. This supersedes the epic's recorded point-vs-forward alternative (epic WI-024 entry).

Unlike WI-023/024 (denominator-only), this item moves **total capital and the LCOE numerator**. The denominator does not move: costs do not feed the power balance, so p_net, q_eng, rec_frac, and SV-016 are untouched.

**Hard stop after this spec** ([OWNER] 2026-07-18, Align): nothing past spec runs until the owner checkpoint approves scope. Per the standing outcomes-at-spec ruling ([OWNER-VERBATIM], WI-024 checkpoint: "spec should capture the outcomes — how the model is built should be done with the expertise of SysML modeling"), mechanism is design's: slot placement, calc structure, grouped-vs-per-building CAS21 representation, parameter form, and computation route are all deferred to `/design-model`.

**Baseline moved from (WI-024 executed record, `work/completed/20260718_WI-024_recirc-power-derivation/`, commit `72f7d054`):** p_fus 2748.1, p_th 3238.1, p_et 1078.3, p_net 915.081088 MW; p_cryo 0.8643516, rec_frac 0.151362, q_eng 6.606662; LCOE $201.472065/MWh, total $12,601,519,645.07, magnet $6,323,469,946.33 (50.2%).

## Goals & Context

**Research questions served:**
- RQ-1 (dominant cost drivers): buildings is the third-largest direct account; carrying it at powers 20–59% below the executed point misstates the cost structure.
- RQ-2 (credible LCOE range): both LCOE terms currently understate — capital carries stale buildings/preconstruction, and annual O&M is scaled to a p_net 59% below executed. The recompute replaces "knowingly stale" with "tracks the computed powers".

**Owner decisions carried in (graded in the alignment brief) — do not reopen:**
- [OWNER-VERBATIM] 2026-07-18: "the ultimate goal is to have *engineering parameters* -> forward pass -> *outcome attributes*"; "for the *plant*, you could reasonably argue all the equipment is sized based on the power. that to me is forward."
- [AGENT, ratified 2026-07-18]: forward-computed rebind (above).
- [OWNER] 2026-07-18: pytest baseline re-record is out of scope (WI-026); this item's pytest bar is tally-unchanged vs **11 failed / 18 passed / 14 skipped / 0 errors** (twice-verified environmental baseline, WI-024 implement + audit).
- [OWNER] 2026-07-18 (WI-024 §Checkpoint Rulings, ruling 3 — standing successor bar): `handshake_1costingfe.py` may be edited only within `set_1cfe_inputs`'s injection map (no comparison-logic change); `git diff exploration/stellarator_e2e/handshake_comparison.json` must be empty after the run.
- [OWNER] standing: one item at a time; no-fallbacks; SV-016 stays `pending` — record against it, never fit it; owner holds close/archive.

**Epic context:** epic `work/backlog/epic-mfe-cost-modeling.md`, Deferred Decisions "STALE-BASIS pass-through recompute" entry (sequenced after WI-024 by [OWNER] ruling at WI-023 close-out, so the recompute happens at a settled p_net — that sequencing is now satisfied). Registered in `work/BACKLOG.md` as WI-025 under the epic.

## Current State

**The three stale bindings** (`models/designs/stellarator_09/stellarator_plant.sysml`; staged twin `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` mirrors all three regions):

1. **CAS21 buildings** — `part :>> buildings { :>> capital_cost = 613650000.0; }` (:262-281, literal at :280, STALE BASIS at :270). Doc records the stale basis (p_et 896.8, p_the 896.8, p_th 2693.1, p_fus 2700, n_mod 1) and the old objection: "the per-building fuel-keyed base costs + scaling bases are a dict loop (out of the codegen envelope), so the total is a pass-through here." That objection dissolves — see Evidence: the loop collapses exactly into 6 grouped terms, each linear in one scaling basis.
2. **CAS10 preconstruction** — `:>> preconstruction_capital = 33896000.0` (:594-614, STALE BASIS at :602). Doc records the deliberate convention: bound **without** CAS10's own contingency, so the plant's CAS29 applies contingency once (no double-count).
3. **CAS70 annual O&M** — `:>> annual_om = 41641000.0` (:643-660, STALE BASIS at :648). Doc records the formula (54.9 × sqrt(p_net/1000)) and that inflation + scheduled-replacement (CAS72) refinements are a Stage-3 item — this item does not add them.

**Consumers that carry the same stale values:**
- Oracle `exploration/stellarator_e2e/verify_stellaris.py`: `buildings_capital=613650000.0` (:102), `preconstruction_capital=33896000.0` (:103), `annual_om=41641000.0` (:108); rollup at :195-200, LCOE at :202-210.
- Runner `exploration/stellarator_e2e/run_stellaris.py`: harness constants `BUILDINGS`/`PRECON` (:93-94) fed into the rollup glue (:193); headline asserts "WI-024 HEADLINE CHECK" (:246-262: p_net 915.1, total 12.60, LCOE 201.5, magnet 6.32, etc.).
- Generated inputs: `exploration/stellarator_e2e/generated/inputs/system_design.json` carries `lcoe_calc__annual_om: 41641000.0` (regen-refreshed from the instance binding).
- Handshake `exploration/stellarator_e2e/handshake_1costingfe.py`: injects `lcoe_calc__annual_om` from 1cfe's own refs inside `set_1cfe_inputs` (:243); the rollup glue takes buildings/precon from 1cfe's own `costs_musd` (:369-370, **outside** the injection map) and reports them as tautological pass-through rows (:422-426). Anchor A is therefore *expected* structurally unaffected — but that is re-derived at design under the successor bar, not carried (alignment brief, premise caveats).
- Validation matrix: SV-030 and SV-031 `passing`, with executed-value records at the WI-023/024 headline (total $12,601,519,645.07, LCOE $201.458/$201.472065). Next free SV: **SV-032** (created `pending` by this spec).

## Evidence — Formula Verification (this spec, against the pinned 1costingFE)

All formulas read from 1costingFE at pin `0254385`: `src/costingfe/layers/costs.py` (`cas10_preconstruction` :52-80, `cas21_buildings` :83-144, `cas70_om` :319-357) and `src/costingfe/data/defaults/costing_constants.yaml` (CAS10 constants :8,15-23; `building_costs` table :175-197; `om_cost_dt` :272). Spec-stage arithmetic below is a verification record and an expected-value illustration — the binding forms are design's.

**Honesty check — all three bound literals reproduce from the formulas at their recorded stale bases:**

| Account | Formula at stale basis | Computed | Bound literal |
|---|---|---|---|
| CAS21 | building loop at p_et = p_the = 896.8, p_th 2693.1, p_fus 2700, n_mod 1, DT, cryogenics included (SC coils) | 613.6502 M$ | 613.650 M$ ✓ |
| CAS10 | 0.25·sqrt(575.3·1000)·10000/1e6 + (3+5+2+20+1+1), FOAK, pre-contingency | 33.8962 M$ | 33.896 M$ ✓ |
| CAS70 | 54.9·sqrt(575.3/1000) | 41.6408 M$/yr | 41.641 M$/yr ✓ |

The literals are the formula values rounded to 0.001 M$; the ~$200–500 rounding residues vanish when the accounts become computed (full-precision) values.

**Exact grouping (CAS21):** every one of the 18 buildings is linear in exactly one scaling basis, so the loop collapses **algebraically exactly** (not a fit) into 6 grouped terms with base-cost sums (DT, cryogenics included): fixed **168.5**, p_fus/2300 **288.0**, staff = sqrt(p_et/1100) **9.0**, p_the/1100 **58.0**, p_th/2500 **26.0**, p_et/1100 **29.0** (M$ at reference). Reference powers: p_et/p_the ref = `ref_gross_power_mwe` 1100 (yaml:12), p_th ref 2500 and p_fus ref 2300 hardcoded (`costs.py:105-106`). `p_the = p_et` for a no-DEC plant (`costs.py:104`); cryogenics building applies (superconducting coils, `costs.py:137`). Whether the model represents this grouped or per-building is a **design decision**.

**Frozen dimensions at the design point** (documented constants, not new degrees of freedom): fuel = DT (fuel_key "dt" — no ambiguity found, every fuel-keyed constant has a dt entry), FOAK (`plant_studies_foak = 20`), n_mod = 1.

**Conventions that must survive the rebind** (found honest at this sweep, no owner action expected — confirm at checkpoint):
- CAS10 binds the **pre-contingency subtotal**; `costs.py:79` adds CAS10's own contingency, which the model deliberately omits because CAS29 applies contingency over the whole direct sum (the doc says so; the reproduction above confirms 33.896 is the contingency-free subtotal).
- CAS70 binds the **unlevelized annual O&M**; `cas70_om` additionally levelizes with inflation (CAS71) and adds scheduled replacement (CAS72) — those remain out of scope, documented Stage-3 refinements, exactly as the current doc records.
- CAS21 is bound **raw** (pre-contingency), matching `costs.py:86-88` (CAS29 applies once over the direct sum).
- No unsourced constants: every constant in all three formulas lives in the pinned yaml or costs.py.

**Expected values at the executed powers (p_et = p_the = 1078.3, p_th 3238.1, p_fus 2748.1, p_net 915.081088):**

| Account | Stale bound | Forward at executed powers | Δ |
|---|---|---|---|
| CAS21 buildings | $613,650,000 | $640,480,665 | +26.83 M$ |
| CAS10 preconstruction | $33,896,000 | $34,391,497 | +0.495 M$ |
| CAS70 annual O&M | $41,641,000/yr | $52,517,269/yr | +10.88 M$/yr |

Rollup illustration (oracle formulas, `verify_stellaris.py:195-210`): Δdirect +$27.33 M; with contingency 0.10 and indirect 0.20 × (8/6), Δtotal +$37.35 M → total ≈ **$12,638,865,400** (+0.30%); ΔLCOE = (Δtotal × 0.105632 + ΔO&M) / 6,813,694 MWh ≈ **+$2.175/MWh** → LCOE ≈ **$203.65/MWh**. Magnet capital unchanged; magnet share ≈ 50.03%. p_net, q_eng, rec_frac unchanged. Actual values are recorded at implement, bit-exact vs the re-baselined oracle at rel 1e-9 — these illustrations set the expected surface, not targets to fit.

## Modeling Requirements

EARS format per the requirements-tracking skill. Mechanism-free by design: each requirement states an outcome; structure and placement are `/design-model`'s.

#### MR-WI025-1: Forward-computed, tracking the computed powers

The model SHALL compute the CAS21 buildings, CAS10 preconstruction, and CAS70 annual O&M accounts as functions of the model's computed powers (CAS21 from p_et/p_the/p_th/p_fus; CAS10 and CAS70 from p_net), mirroring the 1costingFE formulas at pin `0254385`, replacing the three literals; the three STALE BASIS annotations SHALL be retired.

- **Type**: Functional | **Priority**: Must | **Derives from**: [AGENT] ratified 2026-07-18 (forward, settled); [OWNER-VERBATIM] forward-pass goal; RQ-1/RQ-2
- **Validation**: SV-032; run_stellaris bit-exact vs oracle (rel 1e-9)

#### MR-WI025-2: Exactness — mirrors 1costingFE, not a fit

Each forward computation SHALL reproduce the pinned 1costingFE formula exactly: the CAS21 representation SHALL be algebraically exact against the 18-building loop (grouping, if used, is exact linear algebra, never a calibration), and the design SHALL prove agreement of all three accounts against a 1costingFE-side evaluation at the executed powers before implement.

- **Type**: Quality / Verification | **Priority**: Must | **Derives from**: alignment brief premise caveat ("must reproduce 1costingFE's loop exactly"); [AGENT] grouping verification (this spec, Evidence)
- **Validation**: design-stage 1cfe-side evaluation record; SV-032

#### MR-WI025-3: Conventions and frozen dimensions preserved

The rebind SHALL preserve the existing account conventions: CAS10 bound as the pre-contingency subtotal (CAS29 applies contingency once), CAS21 raw (pre-contingency), CAS70 as unlevelized annual O&M (inflation/CAS71 levelization and CAS72 scheduled replacement remain out of scope, documented as Stage-3 refinements). Fuel = DT, FOAK, and n_mod = 1 SHALL freeze at the design point as documented constants; `p_the = p_et` (no DEC) SHALL be documented where CAS21 consumes it.

- **Type**: Constraint | **Priority**: Must | **Derives from**: existing doc conventions (instance :594-614, :643-660); [AGENT] Align verification; this spec's Evidence sweep
- **Validation**: doc inspection at review; SV-032 exactness implies the conventions held

#### MR-WI025-4: Honest re-baselining of the numerator surface

The item SHALL re-baseline every consumer of the three accounts: the oracle (`verify_stellaris.py`) computes the accounts forward instead of carrying constants; the runner headline asserts move to the WI-025 headline; regenerated pipeline artifacts refresh (regen only, never hand-edited); SV-032 records the executed headline (the three account values, direct/total capital, LCOE). Prior SV executed-value records (SV-030/SV-031) are historical records of their items' executions and SHALL be treated per the checkpoint ruling (default: left standing, matrix precedent SV-027/SV-029). The docs of all three accounts SHALL state their post-WI-025 basis (which computed powers each tracks), so no future reader re-discovers the staleness question.

- **Type**: Functional / Traceability | **Priority**: Must | **Derives from**: alignment brief premise caveat (numerator blast radius); capture-fidelity law 3 (amend, never accrete)
- **Validation**: SV-032; runner output; doc inspection at review

#### MR-WI025-5: Standing bars hold; handshake under the successor bar

The change SHALL hold the inherited bars: L1 = 0 over the 22-file model set with the L2–L6 offender list exactly the 6 pre-existing (`mfe_plant.sysml:353/359/364`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205` — compare the offender list, not level-summary flags), zero new; regen via the sysml-codegen snapshot (HEAD `6db3212`, **no** `--design-path-filter`) + `bridge_v11_generate.py` with `preserve_handwritten=True` and the WI-022 handwritten reactivity impl surviving content-identical (sha256 `8d2357…794a9f`); `run_stellaris.py` bit-exact vs the re-baselined oracle at rel 1e-9 (executed via `/home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python`); IFE anchors unchanged (`run_anchors.py`: 252.30/68.69/270.12 $/MWh, Meier 4.735 c/kWh); pytest tally unchanged vs 11 failed / 18 passed / 14 skipped / 0 errors; canonical↔staged mirroring per-edit-region. The Anchor A handshake SHALL stay closed under the standing successor bar (`handshake_1costingfe.py` edited only within `set_1cfe_inputs`'s injection map, no comparison-logic change, `git diff exploration/stellarator_e2e/handshake_comparison.json` empty): Anchor A is expected structurally unaffected (the handshake feeds 1cfe's own cas21/cas10/annual_om), but the design SHALL re-derive handshake safety for the ratified structure — and SHALL surface to the owner before implement any edit the new structure would force **outside** the injection map (the rollup-glue pass-throughs at :369-371 are outside it), rather than absorb it.

- **Type**: Constraint | **Priority**: Must | **Derives from**: [INHERITED: handoff] WI-024-verified bars; [OWNER] successor bar (WI-024 ruling 3); alignment brief premise caveats
- **Validation**: SV-032; SV-025/026 byte-identical; L1–L6 offender-list compare; SV-023 unchanged; pytest tally

#### MR-WI025-6: Citations and clean-room

Every changed value and doc SHALL carry an MR-4 `Source / Ref / Basis` citation resolving to 1costingFE at `0254385` (costs.py / costing_constants.yaml file:line). No ARIES-CS-informed source may be read or cited (PROTOCOL.md §3); this item's admissible source set is 1costingFE only.

- **Type**: Traceability | **Priority**: Must | **Derives from**: MR-4; PROTOCOL.md §3; alignment brief [INHERITED: PROTOCOL]
- **Validation**: citation inspection at review

## Scope Boundaries

**In scope:**
- The three account rebinds + their docs in `models/designs/stellarator_09/stellarator_plant.sysml` (:262-281, :594-614, :643-660) and the staged twin (same regions), including STALE BASIS retirement and post-WI-025 basis statements.
- Any new calc structure the design rules (placement — library vs instance-local, grouped vs per-building — is design's; if the design places anything in `models/library/`, MR-3 concept-agnosticism applies).
- Oracle (`verify_stellaris.py`) forward computation of the three accounts; runner (`run_stellaris.py`) harness constants → channels/computed values and headline assert re-targeting; regenerated pipeline artifacts.
- `modeling_project/VALIDATION_MATRIX.md` — SV-032 (created by this spec, `pending`); SV-030/SV-031 record treatment per checkpoint ruling.
- Handshake edits only if forced, only within the successor bar; anything outside the injection map comes back to the owner first.
- `.project/CURRENT_WORK.md` headline at close.

**Out of scope:**
- Pytest baseline re-record — registered separately as WI-026 ([OWNER] 2026-07-18); this item's bar is tally-unchanged.
- CAS70 inflation/CAS71 levelization and CAS72 scheduled replacement (documented Stage-3 refinements — the unlevelized convention carries).
- CAS10/CAS29 contingency convention changes (the pre-contingency-subtotal convention carries).
- Every other account: CAS22/23/24/25/26/27 are already forward-computed; magnet, geometry, confinement, powers all settled by WI-019..024. No power-balance change of any kind — the denominator does not move.
- SV-016 band (untouched; q_eng does not move this item).
- Fuel/NOAK/n_mod as variables (frozen constants at the design point).

## Success Criteria

1. **SV-032 (created `pending` by this spec):** the three accounts are computed outputs tracking the model's computed powers, mirroring the pinned 1costingFE formulas exactly; executed values recorded at implement, bit-exact vs the re-baselined oracle at rel 1e-9. Expected at the executed powers (spec-stage arithmetic, Evidence above): CAS21 ≈ $640.481 M, CAS10 ≈ $34.391 M, CAS70 ≈ $52.517 M/yr; total capital ≈ $12.639 B (+0.30%), LCOE ≈ $203.65/MWh (+$2.18); p_net/q_eng/rec_frac and magnet capital unchanged. No value is a target to fit — the honest output is whatever the exact formulas compute.
2. **Exactness proven** (MR-WI025-2): design-stage 1cfe-side evaluation agrees with the forward forms at the executed powers before implement.
3. **Standing bars** (MR-WI025-5): L1–L6 offender list = the 6 pre-existing, zero new; regen with handwritten-impl survival; bit-exact rel 1e-9; IFE anchors and pytest tally unchanged; mirroring holds.
4. **Handshake:** SV-025/026 byte-identical under the successor bar; any forced edit outside the `set_1cfe_inputs` injection map surfaced to the owner before implement, not absorbed.
5. **Docs:** three STALE BASIS annotations retired; each account's doc states the powers it tracks and the preserved convention (MR-WI025-3/4); MR-4 citations to 1costingFE @ `0254385` throughout.

## Checkpoint Rulings ([OWNER] 2026-07-18 — "agreed on all counts")

1. **Scope confirmed:** the three accounts only, forward-computed, with the conventions preserved as found (CAS10 pre-contingency subtotal; CAS70 unlevelized, no inflation/CAS72; CAS21 raw; DT/FOAK/n_mod = 1 frozen as documented constants). The sweep found no unsourced constants and no fuel-key ambiguity — no honesty ruling needed.
2. **Re-baselined headline records confirmed (default):** SV-032 records the WI-025 executed headline; the runner's headline asserts re-target to it. SV-030/SV-031 executed-value records stand as historical records of their items' executions (matrix precedent: SV-027/SV-029); no annotation directed.
3. **Successor-bar escalation path confirmed:** design re-derives handshake safety for the ratified structure under the standing successor bar. Any handshake edit the new structure would force **outside** the `set_1cfe_inputs` injection map (the rollup-glue pass-throughs at :369-371 are outside it) comes back to the owner before implement — never absorbed.

(Grouped-vs-per-building CAS21 representation, slot/calc placement, and computation route are design's, not the checkpoint's — alignment brief, Parked section. Design → plan → implement → audit run without further planned owner stops; the ruling-3 escalation and any premise surprise still stop the line.)

## Assumptions & Risks

1. **Expected movement is fully characterized** (high confidence): all three literals reproduce from the pinned formulas at their recorded stale bases (Evidence), so the delta is pure basis-tracking, not a formula dispute. Illustration: total +$37.35 M (+0.30%), LCOE +$2.18/MWh. Actual recorded at implement.
2. **Handshake structurally unaffected** (expected, medium-confidence until design re-derives): the injection map already feeds 1cfe's own annual_om, and the glue feeds 1cfe's own cas21/cas10. Risk: a new computed channel forces glue edits outside the injection map — escalation path pre-agreed (checkpoint Q3), WI-024's D7 identity-injection pattern (zero the chain inputs, feed the 1cfe value through an inert path) is the in-repo precedent for staying inside the bar.
3. **Codegen envelope** (low): the old "dict loop out of the codegen envelope" objection dissolves under exact grouping; the forward forms are linear/sqrt terms already proven through regen (CAS22/23-26 precedent). Any unsupported construct is a finding, not a workaround.
4. **Rounding residue** (negligible, documented): the retired literals were 0.001 M$-rounded; forward computation carries full precision. Sub-$500 effects at the stale point, moot at the executed point.
5. **Numerator blast radius** (certain, managed): first capital/LCOE-numerator move since WI-023. The re-baselining surface is enumerated (MR-WI025-4); nothing else consumes the three accounts (grep-verified: model + twin, oracle, runner, generated inputs, handshake glue).

## Traceability

**Sources (all read at this spec, pin `0254385` — read-only):**
- `/home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py`: `cas10_preconstruction` :52-80 (land ∝ sqrt(p_net·n_mod·ref), five fixed adders + licensing; contingency at :79 deliberately not carried); `cas21_buildings` :83-144 (18-building loop, scale_map :121-130, refs :102-106, cryogenics SC-gate :137, fuel_key :114-119); `cas70_om` :319-357 (annual_om at :353 = om_cost(fuel) × (p_net·n_mod/ref)^0.5; CAS71/72 levelization not carried).
- `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`: :8 (`ref_net_power_mwe` 1000), :12 (`ref_gross_power_mwe` 1100), :15-23 (CAS10 constants incl. `land_intensity` 0.25, `land_cost` 10000, `plant_studies_foak` 20, `licensing_cost_dt` 5), :175-197 (`building_costs` table), :272 (`om_cost_dt` 54.9).
- Model/harness current state: `models/designs/stellarator_09/stellarator_plant.sysml` :262-281/:594-614/:643-660; `exploration/stellarator_e2e/verify_stellaris.py` :102-108/:195-210; `run_stellaris.py` :93-94/:193/:246-262; `handshake_1costingfe.py` :243/:369-371/:422-426; `generated/inputs/system_design.json` (annual_om).

**Downstream impacts:** WI-018 instance + staged twin, oracle/runner, regenerated pipeline artifacts, `VALIDATION_MATRIX.md` (SV-032; SV-030/031 record treatment), `.project/CURRENT_WORK.md` headline, the hold-out comparison (an honestly re-baselined headline is what gets graded at reveal).

**Applicable project rules:** MR-4 (citations), MR-3 (library concept-agnosticism, if design places structure in library), PROTOCOL.md §3 (clean-room — this spec read only 1costingFE and in-repo artifacts), no-fallbacks (no value invented; every number traces to the pinned formulas), capture-fidelity (provenance grades carried from the alignment brief; corrections amend, never accrete).

## Related Artifacts

- Alignment brief: `work/orchestration/stale-basis-recompute.md`
- Epic: `work/backlog/epic-mfe-cost-modeling.md` (Deferred Decisions entry; sequencing ruling in Item WI-024)
- Predecessor: `work/completed/20260718_WI-024_recirc-power-derivation/` (spec §Checkpoint Rulings carries the standing successor bar; executed baseline records)
- Validation: `modeling_project/VALIDATION_MATRIX.md` SV-032 (`pending`, created by this spec)
- Design: `work/active/WI-025_stale-basis-pass-through-recompute/design.md` (to be created after the owner checkpoint)
- Plan: `work/active/WI-025_stale-basis-pass-through-recompute/plan.md` (to be created)
