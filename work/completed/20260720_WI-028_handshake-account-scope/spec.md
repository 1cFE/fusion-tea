---
Status: completed
Scale: standard
Owner: reidw
Created: 2026-07-20
Updated: '2026-07-20'
---

# WI-028 — Handshake account scope: CAS22 tail + CAS40/50/60

**STELLARATOR-DEMO epic Item 3 (standalone WI-028, P0).**
**Governing frame:** `.project/concepts/stellarator-mbse-demo.md`, criterion 3 (Anchor A). This spec is judged against the ratified anchor-acceptance bars in `.project/active/demo-anchor-acceptance-spec/spec.md` (A-2/A-3/A-4/A-5/A-6 + the G-8 amendment).
**Required Reading:** `knowledge/holdout/aries-cs/PROTOCOL.md` — §3 barred paths absolute, quarantine sealed. No barred artifact is read for this work; the whole account scope sources from 1costingFE (the ARIES-lineage exception already scoped in PROTOCOL §3) and the model's own computed powers/geometry.

---

## Overview

The 1costingFE handshake (Anchor A) currently forward-computes 12 cost accounts and leaves the reactor-plant cost tail and the owner / supplementary / financing accounts **structurally absent** — the larger share of the −31% structural LCOE gap. This item forward-computes those accounts from the model's own powers and geometry, reproducing 1costingFE's formulas, so they come under the A-2 per-account bar and stop being a hole in the rollup.

In scope: the CAS22 tail (8 sub-accounts, ~$1.094B at the 1 GWe point), CAS40 (owner, $41.2M), CAS50 (supplementary, $578.6M), and the CAS60 IDC line ($2223.7M) reconciled with the model's DCF convention. Not in scope: CAS70/80 and LCOE levelization construction (Item 4); CAS21/CAS10/CAS70 are already forward-computed (WI-025) and are **not** re-modeled.

---

## Goals & Context

- **Serves:** demo criterion 3 (1costingFE handshake). The bar, per the [OWNER] criterion-3 ruling (2026-07-18), is *explaining and closing errors*: remaining discrepancies after Items 3–4 are itemized and explained; anything shown to be an error is closed; full structural-gap closure is **not** required.
- **Judged against** the ratified anchor spec:
  - **A-2** — per-account pass bar |relative deviation| ≤ 1e-6 vs 1costingFE's float32 runtime, no grandfathering for newly-brought accounts.
  - **A-3** — the authoritative target account list (authoritative over the epic's Item-3 prose, which omits C220600 "other" and the aux-cooling term).
  - **A-4** — any account that cannot come under A-2 becomes itemized-and-explained remainder with signed magnitudes; the residual gap reconciles to the itemized sum.
  - **A-5** — every new field mapping gets an assertion in the handshake; new traps added to the trap table.
  - **A-6** — 1costingFE pinned at `0254385`, drift-asserted at run; pin bumps are owner-only.
  - **G-8 amendment (in force)** — for account-scope items the WI-024 empty-diff successor bar is superseded: `handshake_comparison.json` moves are **expected** and re-baselined as an explicit commit; comparison *logic* stays untouched (only what feeds it changes).

---

## Current State — harness survey (A-3 list vs the current harness)

The current harness is the post-lifecycle-Item-10 single-pass route (WI-027 close state): runner `exploration/stellarator_e2e/run_stellaris_single.py`; handshake driver `exploration/stellarator_e2e/handshake_1costingfe.py`; 1cfe point emitted by `emit_1cfe_point.py` at pinned commit `0254385`. Generation via public CLI `sysml-codegen generate --from-snapshot`; no bridge, no rollup glue.

### What the handshake computes today (`handshake_1costingfe.py`)

- **Forward-computed powercore (8):** magnet, heating, divertor, blanket, shield, structure, vessel, power_supplies → 1cfe `C220101`–`C220108` (`POWERCORE_MAP`, `handshake_1costingfe.py:99`).
- **Forward-computed BOP (4):** turbine, electric, heat_rejection, misc → 1cfe `cas23`/`cas24`/`cas26`/`cas25` (`BOP_MAP`, `:105`).
- **Forward-computed (WI-025), shown as rollup rows:** CAS21 buildings, CAS10 preconstruction — computed at 1cfe's fed powers, no longer pass-throughs.
- **Injected design input:** CAS27 special_materials, fed 1cfe's value into the direct-capital aggregation (`:253`). This is the only genuinely-injected value still in the rollup; it stays injected and is out of scope here.

### What A-3 targets, and where it stands in the harness

| A-3 target account | 1cfe value @ 1 GWe (M$) | 1cfe key | Harness state today |
|---|---|---|---|
| C220110 remote handling | 151.872 | `cas22_detail` | **structurally absent** |
| C220111 installation | 509.599 | `cas22_detail` | **structurally absent** |
| C220200 coolant | 202.045 | `cas22_detail` | **structurally absent** |
| C220300 aux cooling + cryoplant | 18.921 | `cas22_detail` | **structurally absent** |
| C220400 waste | 5.525 | `cas22_detail` | **structurally absent** |
| C220500 fuel handling | 120.000 | `cas22_detail` | **structurally absent** |
| C220600 other | 11.500 | `cas22_detail` | **structurally absent** |
| C220700 I&C | 73.849 | `cas22_detail` | **structurally absent** |
| **CAS22 tail subtotal** | **~1093.31** | — | absent (≈ the $1094.03M diagnostic gap) |
| CAS40 owner | 41.200 | `costs_musd.cas40` | **structurally absent** |
| CAS50 supplementary | 578.584 | `costs_musd.cas50` | **structurally absent** |
| CAS60 IDC | 2223.688 | `costs_musd.cas60` | **absent as a line** (model folds IDC into DCF — see reserved gate) |

Values from `exploration/stellarator_e2e/onecfe_point.json` (`cas22_detail_musd`, `costs_musd`).

### Mismatches to surface

1. **"Absent," not "injected" — the G-8 shrinkage clause has little to shrink here.** The G-8 amendment frames account-scope work as replacing *injected* values with computed ones and documenting each account "as it leaves the injection map." For the A-3 targets there is **nothing in the injection map to remove** — they are structurally absent (the tail appears only in the diagnostic `cas22_gap_musd.unmodeled_musd = 1094.03` aggregate; CAS40/50/60 do not appear in `handshake_comparison.json` at all). Item 3's move is therefore **absent → forward-computed**, which is exactly the re-baseline the G-8 amendment expects (comparison JSON moves, total_capital and LCOE rise) — but the "name each account as it leaves the injection map" documentation clause is satisfied trivially (no map entries to name for these accounts). The only injected value in the rollup, CAS27 special, is untouched. This is recorded so the re-baseline commit is not read as a shrinkage it is not.
2. **The comparison currently has no rows for these accounts.** `handshake_comparison.json`'s `rollup` section carries only contingency / indirect / direct / total_capital / lcoe / net_electric; the tail lives only as one aggregate diagnostic. A-4 (itemize with signed magnitudes) and A-5 (assert every new mapping) require Item 3 to **add explicit comparison rows** for each of the 8 tail accounts plus CAS40/CAS50/CAS60.
3. **A-3 is authoritative over the epic prose.** The epic's Item-3 scope text omits C220600 "other" and the aux-cooling term; A-3 lists all 8 tail accounts and both are present in `cas22_detail`. Follow A-3.
4. **C220106_pump ($0.721M) is the standing documented remainder.** The SysML vessel calc is the shell term only; 1cfe's canonical C220106 additionally carries a gas-load pumping sub-term (`handshake_1costingfe.py:99` note). It stays an itemized-and-explained remainder under A-4, not a new modeled account.

### Model-side state that Item 3 builds on

- Library calc defs live in `models/library/cost_structure/` and `models/library/analyses/`; the Stellaris instance binds them in `models/designs/stellarator_09/stellarator_plant.sysml` (MR-3).
- The model already assembles the CAS20 direct rollup, CAS30 indirect, and contingency — the aggregate chain CAS50 depends on already exists.
- The model's LCOE core (`models/library/analyses/mfe_lcoe_dcf.sysml`) already carries an IDC term as a DCF multiplier (`idc_factor = (1+d)^(Yc/2)`, `mfe_lcoe_dcf.sysml:47`) applied to total_capital inside the annualized capital charge. This is the crux of the CAS60 reserved gate below.
- Current executed headline (design point, WI-027, bit-exact vs oracle rel 1e-9): total **$12,638,857,665.74**, LCOE **$203.647152/MWh**, p_net 915.081088 MW, q_eng 6.606662, magnet $6,323,469,946.33 (50.03%).

---

## 1costingFE formula survey (@ `0254385`) and forward-computability classification

All 1cfe formulas return M$; the handshake feeds M$ coefficients ×1e6 so the SysML produces $. Inputs classify as **[COMPUTED]** (a plant power-table / geometry quantity the model already produces), **[CONST]** (a 1cfe cost-config constant / literal — a unit-cost base or fraction to introduce and source per MR-4), or **[SCALAR]** (a top-level input already in the point: n_mod, interest_rate, construction_time_yr). At the target point **n_mod = 1**, so per-module and plant-total powers coincide numerically — but the formulas differ structurally (plant-wide accounts added once; equipment ×n_mod; labor multi-unit factor), which the design must honor so the model generalizes and which A-5 must assert.

| Account | 1cfe formula (file:line) | Inputs | Class |
|---|---|---|---|
| C220110 remote handling | `rh_base[fuel] * concept_scale * (p_et/ref_gross)^0.5` (`cas22.py:631-645`) | p_et [COMPUTED, per-module]; rh_base, concept_scale=1.0, ref_gross [CONST] | **forward-computable** (new CONST bases) |
| C220111 installation | `installation_frac * Σ(C220101..C220110)` (`cas22.py:652-664`) | reactor_subtotal [COMPUTED via modeled accounts]; installation_frac=0.14 [CONST] | **forward-computable** (downstream aggregation; multi-unit labor factor inert at n_mod=1) |
| C220200 coolant | `166.0*(p_net_tot/ref_net) + 40.6*(p_th_tot/3500)^0.55` (`cas22.py:684-686`) | p_net, p_th [COMPUTED, ×n_mod]; literals, ref_net [CONST] | **forward-computable** |
| C220300 aux + cryoplant | `1.10e-3*p_th_tot + 200.0*(p_cryo/30)^0.7` (`cas22.py:693-695`) | p_th [COMPUTED ×n_mod], p_cryo [COMPUTED, per-module]; literals [CONST] | **forward-computable** (model produces p_cryo via the cryo_elec chain) |
| C220400 waste | `1.96*(p_th_tot/1000)` (`cas22.py:702`) | p_th [COMPUTED ×n_mod]; literals [CONST] | **forward-computable** |
| C220500 fuel handling | `fuel_handling_base[fuel]*(p_net_tot/ref_net)^0.7` (`cas22.py:712-718`) | p_net [COMPUTED ×n_mod]; fuel base, ref_net [CONST] | **forward-computable** (new CONST base) |
| C220600 other | `11.5*(p_net_tot/ref_net)^0.8` (`cas22.py:724`) | p_net [COMPUTED ×n_mod]; literals [CONST] | **forward-computable** |
| C220700 I&C | `85.0*(p_th_tot/3500)^0.65` (`cas22.py:731`) | p_th [COMPUTED ×n_mod]; literals [CONST] | **forward-computable** |
| CAS40 owner | `owner_cost(fuel)*(p_net*n_mod/ref_net)^0.5` (`costs.py:239-256`) | p_net [COMPUTED]; owner base, ref_net [CONST]; n_mod [SCALAR] | **forward-computable** (new CONST base) |
| CAS50 supplementary | shipping·cas20 + spares·cas23‥28 + tax·cas20 + insurance·(cas20+cas30) + startup_fuel·(p_net_tot/ref) + decom·(p_net_tot/ref), then ×(1+contingency) (`costs.py:259-283`) | cas20/cas23‥28/cas30 aggregates [COMPUTED, already assembled]; six fracs + bases [CONST]; p_net [COMPUTED]; n_mod, noak [SCALAR] | **forward-computable** (wire to the existing CAS20/CAS30 aggregate chain) |
| CAS60 IDC | `f_idc = ((1+i)^T − 1)/(i·T) − 1; CAS60 = f_idc·overnight_cost` (`costs.py:286-297`) | overnight_cost [COMPUTED aggregate = CAS10+20+30+40+50]; i, T [SCALAR] | **mechanically forward-computable (closed form); placement is a reserved convention gate** |

**Result of the classification: every A-3 target is forward-computable.** None requires a plant quantity the model does not already compute — the only "new inputs" are 1cfe cost-config **constants** (unit-cost bases and fractions: remote-handling/fuel-handling/owner bases, `installation_frac`, the CAS50 fractions), which are introduced as sourced design inputs per MR-4, not new physics. The single **remainder-candidate** is the standing **C220106_pump** ($0.721M), already documented. (C220109 and C220112 are structurally zero for this concept, not remainders.)

---

## Modeling Requirements

Each requirement traces to the anchor-spec bar or the 1cfe formula it derives from. IDs are MR-WI028-N.

**MR-WI028-1 — CAS22 tail forward-computed.** [Functional] [P0]
The model SHALL forward-compute the eight CAS22 tail accounts (C220110, C220111, C220200, C220300, C220400, C220500, C220600, C220700) as concept-agnostic library calc defs reproducing the 1costingFE formulas (`cas22.py:631-731`), fed the model's computed powers (p_th, p_net, p_et, p_cryo) and bound at the Stellaris instance.
- *Rationale:* closes the ~$1.094B tail share of the −31% gap (A-3).
- *Validation:* each account's end-to-end handshake value vs 1cfe under the A-2 bar (SV-034).
- *Source:* A-3; `cas22.py:631-731`.

**MR-WI028-2 — CAS40 owner + CAS50 supplementary forward-computed.** [Functional] [P0]
The model SHALL forward-compute CAS40 (`costs.py:239-256`) and CAS50 (`costs.py:259-283`), CAS50 wired to the model's already-assembled CAS20 / CAS23‥28 / CAS30 aggregate chain, bound at the Stellaris instance.
- *Rationale:* $41.2M + $578.6M of the structural gap (A-3).
- *Validation:* A-2 per-account bar (SV-034).
- *Source:* A-3; `costs.py:239-283`, assembly at `model.py:1487-1497`.

**MR-WI028-3 — CAS60 IDC documented mapping.** [Functional / Constraint] [P0]
The model SHALL produce a documented mapping between 1costingFE's CAS60 closed-form IDC (`f_idc = ((1+i)^T−1)/(iT) − 1` on overnight cost, `costs.py:286-297`) and the model's DCF IDC convention (`idc_factor = (1+d)^(Yc/2)` inside the annualized capital charge, `mfe_lcoe_dcf.sysml:47`). Where reconciling the two is a genuine convention *choice* (the evidence below indicates it is), it is a **reserved owner gate** — parked for owner ruling, not resolved by an agent; where it falls out mechanically, it is recorded and proceeds. **The design settles which**; this spec states no mechanism (see "CAS60/IDC reserved gate").
- *Rationale:* "a documented mapping, not a fudge" (A-3); Align ruling 3 (2026-07-20).
- *Validation:* mapping documented; if a line-item comparison is chosen, A-2 bar; reserved-gate disposition recorded.
- *Source:* A-3; Align ruling 3; `costs.py:286-297`, `mfe_lcoe_dcf.sysml:47`.

**MR-WI028-4 — A-2 per-account bar, no grandfathering.** [Quality] [P0]
Every account newly brought under scope by MR-WI028-1/2 SHALL meet |relative deviation| ≤ 1e-6 against 1costingFE's float32 runtime at the handshake point, at first measurement.
- *Rationale:* A-2 (ceiling, not a shared floor; real errors show at percent scale).
- *Validation:* SV-034 records each account's `rel_dev`.
- *Source:* A-2.

**MR-WI028-5 — A-4 itemized remainder.** [Constraint] [P0]
Any account that cannot come under the A-2 bar SHALL be itemized with its 1cfe value, the model value (or "structurally absent"), the signed dollar gap, and a one-line reason (closed-as-error or explained-and-kept). C220106_pump ($0.721M) is carried as an explained remainder. The residual LCOE gap SHALL reconcile to the itemized-remainder sum within the aggregate tolerance (A-4).
- *Rationale:* makes every dollar accountable per the criterion-3 ruling.
- *Validation:* itemized signed-magnitude table in the handshake report.
- *Source:* A-4.

**MR-WI028-6 — A-5 trap discipline for new mappings.** [Constraint] [P0]
Each new field mapping SHALL be asserted in the handshake (never left to a default) and added to the trap table. At minimum: plant-total vs per-module power (tail plant-wide accounts use `n_mod·p_th`/`n_mod·p_net` and are summed once; C220110 uses per-module p_et; C220300 cryoplant uses per-module p_cryo); the reference-power split (`ref_gross_power_mwe` for C220110 vs `ref_net_power_mwe` elsewhere); `installation_frac` applied to the C220101‥110 subtotal; fuel-keyed bases.
- *Rationale:* a silent mapping is a latent handshake failure (the f_shape −20.6% precedent).
- *Validation:* each trap asserted in `handshake_1costingfe.py` / `emit_1cfe_point.py`; trap-table entry added.
- *Source:* A-5.

**MR-WI028-7 — Traceability (MR-3 / MR-4).** [Traceability] [P0]
Every new quantitative value (unit-cost bases, fractions, reference powers) SHALL carry an MR-4 structured citation resolving to the 1costingFE source at pin `0254385`. New calc defs SHALL be concept-agnostic in `models/library/`; concept-specific bindings SHALL live in `models/designs/stellarator_09/` (MR-3).
- *Rationale:* durable traceability; library/designs separation.
- *Validation:* citation audit; library defs carry no Stellaris-specific literals.
- *Source:* MR-3, MR-4.

**MR-WI028-8 — G-8 re-baseline, comparison logic untouched.** [Constraint] [P0]
The handshake SHALL be re-run; `handshake_comparison.json` SHALL gain explicit rows for the 8 tail accounts and CAS40/CAS50/CAS60, and its moved values SHALL be re-baselined as a deliberate committed step. The comparison *logic* SHALL NOT change — only what feeds it. The re-baseline commit SHALL record which accounts moved absent→computed and the signed magnitude of each; it SHALL note that the injection map itself does not shrink for these accounts (they were absent, not injected).
- *Rationale:* G-8 amendment (in force) for account-scope items.
- *Validation:* diff of `handshake_comparison.json` matches the documented move list; comparison machinery unchanged.
- *Source:* G-8 amendment.

**MR-WI028-9 — Design-point headline WILL move (re-baseline, not regression).** [Quality] [P0]
Bringing the new real accounts into the rollup SHALL raise the Stellaris design-point total_capital and LCOE. This is a re-baseline like WI-025, **not** a regression. SV-034 SHALL record the new design-point headline; the standing oracle bar (rel 1e-9 bit-exact vs the pure-Python oracle) SHALL hold on every executed channel at the new point.
- *Rationale:* new accounts enter the design-point rollup, not just the handshake.
- *Validation:* SV-034; oracle bit-exact at the new headline.
- *Source:* [AGENT orientation, brief]; WI-025 precedent.

**MR-WI028-10 — Standing bars carried.** [Constraint] [P0]
All standing validation bars SHALL hold (see "Standing bars"). Where a bar is superseded for this item (the handshake empty-diff bar, by G-8; the IFE Run C leg, by owner ruling), the supersession is recorded, not silently dropped.
- *Rationale:* the demo's credibility rests on the bars holding across every item.
- *Source:* WI-027 close state; anchor spec; PROTOCOL.

---

## CAS60 / IDC reserved gate (surfaced, not resolved)

Per `capture-fidelity` §4, a premise conflict is surfaced, not resolved silently. The design and (if it is a genuine choice) the owner rule; this spec only names it.

**The two conventions.**
- **1costingFE:** IDC is a **capital account line**. `overnight_cost = CAS10+20+30+40+50`; `CAS60 = f_idc · overnight_cost` with `f_idc = ((1+i)^T−1)/(iT) − 1`; `total_capital = overnight_cost + CAS60`; then `CAS90 = CRF · total_capital`; and `LCOE = (CAS90 + CAS70 + CAS80)/annual_energy` (`model.py:1498-1604`, `economics.py:78-92`). At the target point `f_idc ≈ 0.2825`, giving CAS60 = $2223.7M.
- **The model:** IDC is a **DCF multiplier inside LCOE**. `annual_capital = total_capital · idc_factor · crf` with `idc_factor = (1+d)^(Yc/2)` (`mfe_lcoe_dcf.sysml:47-52`), where the model's `total_capital` is overnight only (no CAS60 line today).

**Why this is a genuine convention choice, not a mechanical fall-out (the evidence):**
1. **The IDC formulas differ.** 1cfe's uniform-spend `((1+i)^T−1)/(iT) − 1 ≈ 0.2825` is not the model's `(1+d)^(Yc/2) − 1 = (1.07)^4 − 1 ≈ 0.3108`. They are different financing conventions and produce different IDC magnitudes.
2. **Double-count hazard.** If Item 3 adds CAS60 into `total_capital` **and** the model's LCOE keeps multiplying by `idc_factor`, IDC is counted twice. Avoiding that requires a deliberate choice: adopt 1cfe's CAS60-line convention and drop the model's `idc_factor`, or keep the model's DCF `idc_factor` and map CAS60 as a documented equivalence (not a second line), or something else. That choice is a convention decision, and it also touches Item 4 (whose scope explicitly includes "IDC treatment reconciled with the model's DCF convention"). Item 3 produces the CAS60 mapping; Item 4 consumes it.

**Disposition:** MR-WI028-3 requires the design to survey these two conventions and rule whether the reconciliation is mechanical or a genuine choice. The evidence above points to a genuine choice — in which case it is parked as a **reserved owner gate** and the dependent LCOE conclusion is held until the owner rules. No mechanism is chosen here.

---

## Scope Boundaries

**In scope:**
- Library calc defs + Stellaris bindings for: CAS22 tail (C220110/111/200/300/400/500/600/700), CAS40, CAS50 (MR-WI028-1/2).
- CAS60 IDC documented mapping and reserved-gate disposition (MR-WI028-3).
- Handshake re-run, new comparison rows, re-baseline commit, trap-table additions (MR-WI028-6/8).
- SV-034 (MR-WI028-4/9).

**Out of scope:**
- **CAS70 O&M levelization into LCOE and CAS80 fuel** — Item 4. CAS70 unlevelized is already delivered (WI-025).
- **CAS21 buildings, CAS10 preconstruction, CAS70** — already forward-computed (WI-025); **not re-modeled** here. "Injected in the handshake" never meant "unmodeled" for these.
- **CAS27 special_materials** — stays a fed design input.
- **Changes to 1costingFE** — [OWNER] non-goal; gaps found there are filed as findings, not fixed.
- **Closing the gap to zero regardless of cost** — the bar is the criterion-3 ruling: explain the remainder, close errors.
- **Any barred artifact** (PROTOCOL §3).

---

## Success Criteria

- [ ] The 8 CAS22 tail accounts + CAS40 + CAS50 are forward-computed as library calc defs, bound at the Stellaris instance, sourced per MR-4 at pin `0254385` (MR-WI028-1/2/7).
- [ ] Each newly-brought account meets the A-2 bar (|rel dev| ≤ 1e-6) at the handshake point, recorded per account; any that cannot is itemized remainder with a signed magnitude (MR-WI028-4/5). Recorded as **SV-034**.
- [ ] CAS60/IDC mapping is documented; reserved-gate disposition (mechanical vs owner-gated convention choice) recorded (MR-WI028-3).
- [ ] Handshake re-run; `handshake_comparison.json` gains explicit rows for all target accounts and is re-baselined as an explicit commit; comparison logic untouched; new traps asserted and table-added (MR-WI028-6/8).
- [ ] Design-point headline moves and is recorded as a re-baseline (not a regression), with the oracle bit-exact bar holding at the new point (MR-WI028-9).
- [ ] All standing bars hold (below), supersessions recorded (MR-WI028-10).

**SV-034 (VALIDATION_MATRIX, status pending):** new-account handshake + design-point re-baseline — the 8 tail accounts + CAS40/CAS50 (and CAS60 per the reserved-gate disposition) forward-computed and each under the A-2 1e-6 bar vs 1cfe float32; comparison JSON re-baselined; design-point total_capital and LCOE recorded at the new headline with the oracle rel-1e-9 bar holding.

---

## Standing bars (carried from WI-027 close state)

- **Oracle:** bit-exact rel **1e-9** vs the pure-Python oracle on every executed channel, at the new design-point headline.
- **Handshake empty-diff bar:** **superseded for this item** by the G-8 amendment — `handshake_comparison.json` moves are expected and re-baselined; comparison logic untouched (MR-WI028-8).
- **WI-022 handwritten impl:** `dt_fusion_power_impl.py` sha256 `8d2357…794a9f` survives regen (`preserve_handwritten` via the Item-10 route).
- **IFE anchors:** Runs A/B byte-exact (252.29996307 / 68.69020165 / 270.12 as applicable), Meier 4.735. **IFE Run C leg out-of-scope by [OWNER] ruling 2026-07-20** (teax-vs-HIF-package validator skew, routed to the lifecycle epic); Runs A/B byte-exact is the live expectation.
- **pytest:** tally **11/18/14/0**.
- **Regen stability;** L1 = 0, offender list = the 6 pre-existing.
- **MR-3** (library concept-agnostic / designs concept-specific) and **MR-4** (structured citations, mandatory for every new quantitative value).
- **PROTOCOL:** §3 barred paths absolute; quarantine sealed; Required Reading honored.
- **Toolchain pins (verify liveness at design, record this item's pins):** sysml-codegen `06d95f8` (Item 10 certified `1c85042`), agentic-mbse `4c18d61`, teax `07eb0ac`; 1costingFE `0254385` (drift-asserted). Upstream lifecycle epic in flight — adopt movement deliberately, never implicitly.
- **Exec venv:** `exploration/pipeline_spike/.venv-exec/bin/python`; `SYSIDE_LICENSE_KEY` via `set -a && source ~/1cfe/fusion-tea/.env && set +a`; parse check `uv run python -m syside check`.

---

## Assumptions & Risks

1. **[Assumption, high confidence]** Every A-3 target is forward-computable from already-computed powers (survey above). Risk if wrong: an account drops to itemized remainder under A-4 — bounded, not a failure.
2. **[Risk, medium]** CAS50 depends on the CAS20/CAS23‥28/CAS30 aggregate chain; wiring it into a concept-agnostic calc def without leaking Stellaris specifics (MR-3) needs care. Mitigation: the aggregates already exist in the rollup; the calc def consumes them as inputs.
3. **[Risk, medium]** The CAS60/IDC double-count hazard: adding a CAS60 line while the DCF `idc_factor` remains would double-count. Mitigation: the reserved gate — no line is added until the convention is settled (design, then owner if it is a genuine choice).
4. **[Risk, low]** n_mod = 1 hides the per-module vs plant-total structural distinction at the handshake point; a design that hard-codes the point would fail at n_mod > 1. Mitigation: MR-WI028-6 asserts the structure; the trap table records it.
5. **[Risk, low]** Float32 noise: a tail account could sit near the A-2 ceiling. Anchor-spec basis notes most new accounts have less float32 noise, not more; no grandfathering (A-2). Mitigation: measure and, if it legitimately cannot meet 1e-6, itemize under A-4.

---

## Traceability

- **Source requirements:** anchor spec A-2/A-3/A-4/A-5/A-6 + G-8 (`.project/active/demo-anchor-acceptance-spec/spec.md`); Align rulings (`work/orchestration/handshake-account-scope.md`); criterion-3 ruling (2026-07-18).
- **1costingFE formulas (pin `0254385`):** `src/costingfe/layers/cas22.py:631-754` (tail); `src/costingfe/layers/costs.py:239-297` (CAS40/50/60); assembly `src/costingfe/model.py:1483-1605`; LCOE `src/costingfe/layers/economics.py:78-92`.
- **Model-side:** `models/library/cost_structure/`, `models/library/analyses/mfe_account_costs.sysml`, `models/library/analyses/mfe_lcoe_dcf.sysml:47-52`, `models/designs/stellarator_09/stellarator_plant.sysml`.
- **Harness:** `exploration/stellarator_e2e/handshake_1costingfe.py`, `emit_1cfe_point.py`, `handshake_comparison.json`, `onecfe_point.json`.
- **Downstream impact:** Item 4 (CAS70/80 + LCOE levelization) consumes this item's CAS60 mapping; Item 7 (Anchor B) needs cost-account coverage (B-2) that this item advances.
- **Applicable project requirements:** MR-3 (library/designs separation), MR-4 (structured citations).

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_stellarator_mbse_demo.md` (Item 3).
- **Orchestration brief:** `work/orchestration/handshake-account-scope.md`.
- **Governing concept:** `.project/concepts/stellarator-mbse-demo.md` (criterion 3).
- **Ratified bars:** `.project/active/demo-anchor-acceptance-spec/spec.md`.
- **G-8 amendment home:** `work/orchestration/stale-basis-recompute.md` (ruling-3).
- **Required Reading:** `knowledge/holdout/aries-cs/PROTOCOL.md`.
- **Design / Plan:** to be created (`/design-model` → `/plan-model`).
