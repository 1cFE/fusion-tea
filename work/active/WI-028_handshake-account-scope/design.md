---
Status: approved
Created: 2026-07-20
Updated: 2026-07-20 (rev 3 — owner gates ruled: D1 full rebuild, D2 CAS60 Option C; approved)
Related Artifacts:
  Spec: ./spec.md
  Brief: ../../orchestration/handshake-account-scope.md
---

# WI-028 Design — Handshake account scope: CAS22 tail + CAS40/50/60

## Overview

The model forward-computes 12 cost accounts and leaves the rest of the reactor-plant tail, the owner/supplementary accounts, and the IDC line structurally absent — the larger share of the −31% structural LCOE gap. This design brings them in.

It adds seven concept-agnostic library calc defs serving eleven accounts (a shared power-law def covers five: the four flat tail accounts + CAS40; the rest are one-per-account — eight CAS22-tail, CAS50 supplementary, CAS60 IDC line), wires them into a **rebuilt overnight-capital assembly that mirrors 1costingFE exactly**, and binds the new unit-cost bases at the Stellaris instance as dollar conversions of the pinned 1cfe constants. The rebuild is the ruled path (owner, 2026-07-20): the model's current rollup does not match 1cfe's account structure, so it fixes a knowingly-wrong headline LCOE and closes three latent errors. A narrower isolated-aggregate option would also get CAS50 under A-2; it stays recorded as a rejected alternative in D2.

Both owner gates are **ruled** ([OWNER] 2026-07-20, `work/orchestration/handshake-account-scope.md` "Owner gate rulings"): the **overnight rebuild** is chosen over the narrow-shadow alternative (D2, unconditional), and **CAS60 is Option C** — a reported, A-2-checked line excluded from `total_capital`, with the DCF `idc_factor` untouched (D4). The narrow-shadow option stays recorded as a rejected alternative.

---

## Independent formula re-derivation (pin `0254385`)

Every 1cfe formula was re-read from source, not trusted from the spec survey, and the full assembly was reproduced against the emitted point (`onecfe_point.json`) to the cent. The spec survey is accurate; the discrepancies below are in the *1cfe source and the model*, not the survey.

### CAS22 tail (`cas22.py:631-731`) — all confirmed

| Account | Formula (verified) | Power scope | Ref |
|---|---|---|---|
| C220110 remote handling | `rh_base[fuel] * concept_scale * (p_et/1100)**0.5` | **per-module** p_et | `cas22.py:645` |
| C220111 installation | `0.14 * Σ(C220101..C220110)` | per-module subtotal | `cas22.py:652-664` |
| C220200 coolant | `166.0*(p_net_tot/1000) + 40.6*(p_th_tot/3500)**0.55` | **plant-total** (×n_mod) | `cas22.py:684-686` |
| C220300 aux+cryo | `1.10e-3*p_th_tot + 200.0*(p_cryo/30)**0.7` | p_th plant-total; **p_cryo per-module** | `cas22.py:693-695` |
| C220400 waste | `1.96*(p_th_tot/1000)` | plant-total | `cas22.py:702` |
| C220500 fuel handling | `fh_base[fuel]*(p_net_tot/1000)**0.7` | plant-total | `cas22.py:718` |
| C220600 other | `11.5*(p_net_tot/1000)**0.8` | plant-total | `cas22.py:724` |
| C220700 I&C | `85.0*(p_th_tot/3500)**0.65` | plant-total | `cas22.py:731` |

`p_th_total = n_mod * p_th`, `p_net_total = n_mod * p_net` (`cas22.py:681-682`). C220110 uses per-module `p_et`; C220300's cryoplant term uses per-module `p_cryo` (each module has its own cryoplant). This per-module-vs-plant-total split is inert at n_mod=1 but structural — the calc defs carry `n_mod` explicitly so they generalize, and A-5 asserts the split.

### CAS40 / CAS50 / CAS60 (`costs.py:239-297`) — confirmed, one 1cfe naming finding

- **CAS40** (`costs.py:256`): `owner_cost(fuel) * (p_net*n_mod/1000)**0.5`. Plant-total net. Same shape as the plant-power-law tail accounts.
- **CAS50** (`costs.py:259-283`): `(shipping·cas20 + spares·cas23_28 + tax·cas20 + insurance·(cas20+cas30) + startup·(p_net_tot/1000) + decom·(p_net_tot/1000)) · (1+contingency_rate)`. The startup and decom terms are **linear** in plant-total net (no exponent). The `contingency_rate` factor is CAS50's own internal contingency (c59).
- **CAS60** (`costs.py:286-297`): `f_idc = ((1+i)**T − 1)/(i·T) − 1; cost = f_idc · overnight`.

**FINDING F-1 (1cfe source, cosmetic):** CAS50's spares base parameter is *named* `cas22_to_28` in the function signature (`costs.py:259`), but `model.py:1492` feeds it `c23+c24+c25+c26+c27+c28` — i.e. **cas23‥28, excluding CAS22**. The spec survey's "cas23‥28" is correct; the 1cfe parameter name is misleading. Filed as a finding (no fix — 1cfe changes are an [OWNER] non-goal); the model's calc input is named `cas23_to_28` to reflect the real content.

### Full-assembly reproduction (`model.py:1483-1500`, `economics.py:78-92`)

Re-derived and matched against the emitted point to the cent:

```
cas2x_pre = c21 + c22 + c23 + c24 + c25 + c26 + c27 + c28   = 5710.946   (CAS10 NOT included)
c29       = contingency_rate * cas2x_pre                    = 0.0        (NOAK)
c20       = cas2x_pre + c29                                 = 5710.946
c30       = 0.20 * c20 * (8/6)                              = 1522.919   (indirect on c20, POST-contingency)
overnight = c10 + c20 + c30 + c40 + c50                     = 7872.149   (CAS10 added HERE, at overnight)
c60       = f_idc(0.07,8) * overnight = 0.282476 * 7872.15  = 2223.688
total_cap = overnight + c60                                 = 10095.837
c90       = CRF(0.07,30) * total_cap                        = 813.587
lcoe      = (c90+c70+c80)*1e6 / (8760*p_net*n_mod*avail)    = 123.743   (economics.py:90; n_mod explicit)
```

All eight rollup values reproduce bit-for-bit. Two structural facts drive the design:

1. **CAS10 is outside CAS20.** In 1cfe, preconstruction (CAS10) receives **neither CAS29 contingency nor CAS30 indirect** — it is added once at the overnight level.
2. **CAS30 indirect is on `c20` (post-contingency), not on the pre-contingency direct sum.** Masked at NOAK (c29=0) but structural.

---

## The model does not currently match this structure (findings F-2..F-4)

Existing rollup (`models/designs/generic_mfe/mfe_plant.sysml`, mapped this stage):

```
direct_capital  = powercore + bop + buildings(CAS21) + preconstruction(CAS10) + special(CAS27)   [:400-402]
contingency     = rate * direct_capital                                                            [:406-410]
indirect        = 0.20 * direct_capital * (ct/ref)                                                  [:415-420]
total_capital   = direct_capital + contingency + indirect                                          [:423-424]
```

Measured against 1cfe at the handshake point (existing `handshake_comparison.json`, WI-027 baseline):

| Row | 1cfe | model | rel dev |
|---|---|---|---|
| direct / cas20 | 5710.95 M$ | 4646.41 M$ | **−18.64%** |
| indirect | 1522.92 M$ | 1239.04 M$ | **−18.64%** |
| CAS10 (account) | 18.50 M$ | 34.50 M$ | **+86.5%** |

(All rel devs use the 1cfe value as denominator, for consistency across rows. The `handshake_comparison.json` machinery reports CAS10 as +46.4% with a symmetric max-magnitude denominator; the +86.5% here is `(34.5−18.5)/18.5`, same convention as the −18.64% rows.)

**FINDING F-2 — `direct_capital` ≠ 1cfe `cas20`.** The model's `direct_capital` folds in CAS10 (which 1cfe excludes from cas20) and omits `c28` (`cas28_digital_twin` = 5.0 M$, `model.py:1479`). Even after WI-028 adds the CAS22 tail (+1094 M$), `direct_capital` ≈ 5740 M$ vs 1cfe cas20 5711 M$ — off by +29.5 M$ = the wrong CAS10 (34.5, should be 0 in cas20) minus the missing c28 (5.0).

**FINDING F-3 — indirect base is wrong twice.** The model applies indirect (and contingency) to `direct_capital`, which (a) includes CAS10 that 1cfe excludes, and (b) is pre-contingency where 1cfe's indirect is on `c20` (post-contingency). Both masked at NOAK, both real.

**FINDING F-4 — CAS10 account itself diverges +86.5%** (34.5 vs 18.5 M$). Pre-existing WI-025 remainder, out of scope to fix here. But today it flows into `direct_capital` and contaminates contingency, indirect, and — after WI-028 — CAS50. Isolating it is a side benefit of the rebuild.

**Consequence for CAS50.** CAS50 consumes `cas20` and `cas30` as bases (`shipping·cas20`, `insurance·(cas20+cas30)`, …). Fed the model's inflated `direct_capital`-based channels, CAS50 diverges ≈0.2% (≈1.2 M$ on 578.58) — **far outside the A-2 1e-6 bar.** CAS50 therefore needs *faithful* cas20/cas30 as its inputs. There are two ways to supply them: (a) the full overnight rebuild (D2), or (b) a narrow isolated-aggregate — dedicated `cas20`/`cas30` shadow attributes feeding CAS40/CAS50 only, leaving the existing rollup untouched. Both satisfy A-2 for CAS50 (the A-2 bar tests the account *value*, not the headline rollup — the same value/wiring separation used for CAS60). The design recommends (a) and records (b) as a rejected alternative in D2; the owner gate chooses.

---

## Design

### D1 — Seven new library calc defs, serving eleven accounts (`models/library/analyses/mfe_account_costs.sysml` + staged twin)

Concept-agnostic, codegen-envelope-clean (flat Real arithmetic, `+ - * / **`, no `if`/lookup/sum/nested-calc), one calc per account except a shared power-law. Bases and fuel/concept-specific factors are inputs (MR-3: bound at the instance); reference powers and exponents are defaulted inputs carrying their 1cfe citation (MR-4). Full stencils are parse-validated in `prototype/mfe_tail_supplementary_costs.sysml` (see Validation Report). Summary:

| Calc def | Accounts it serves | Key inputs |
|---|---|---|
| `'Plant Power-Law Cost'` | C220400, C220500, C220600, C220700, **CAS40** | base, power, n_mod, ref_power, alpha → `base*(n_mod*power/ref)**alpha` |
| `'Remote Handling Cost'` | C220110 | base, concept_scale, p_et (per-module), ref 1100, α 0.5 |
| `'Installation Labor Cost'` | C220111 | installation_frac 0.14, reactor_subtotal |
| `'Coolant Cost'` | C220200 | primary_base, intermediate_base, p_net, p_th, n_mod, refs |
| `'Aux Cooling Cost'` | C220300 | aux_per_mw, p_th, cryo_base, p_cryo (per-module), n_mod |
| `'Supplementary Cost'` | CAS50 | six fracs/bases + cas20, cas23_to_28, cas30, p_net, n_mod |
| `'IDC Closed-Form Cost'` | CAS60 | interest_rate, construction_years, overnight_cost |

Reusing `'Plant Power-Law Cost'` for five accounts (four tail + CAS40) is exact: each is `base*(n_mod*power/ref)**alpha` with waste at α=1.0. Remote handling is kept separate (per-module p_et, no n_mod; concept_scale semantics). Coolant and aux are two-term sums that mix plant-total and per-module powers — kept as named defs for readability and trap discipline.

`concept_scale` (1.0 toroidal, 0.55 end-access) stays an **instance input**, not a library default — it is concept-specific (MR-3). `'IDC Closed-Form Cost'` uses a variable real exponent (`construction_years`); the model's existing `idc_factor = (1+d)**(construction_years/2)` at `mfe_lcoe_dcf.sysml:47` proves codegen handles variable exponents.

### D2 — Rebuilt overnight assembly (`mfe_plant.sysml`, both trees — see D2b)

Replace the flat `direct_capital → contingency/indirect → total` chain with one that mirrors 1cfe's overnight assembly. This is the risky cross-calc construct; it is parse-validated in `prototype/plant_chain_probe.sysml`.

```
cas22_tail_capital     = remote_handling.cost + installation.cost + coolant.cost
                         + aux_cooling.cost + waste.cost + fuel_handling.cost
                         + other_rpe.cost + inc_cost.cost
cas22_capital          = powercore_capital + cas22_tail_capital           # full CAS22
cas28_capital          = <fed input, 5.0e6>                               # NEW (F-2)
cas2x_pre_contingency  = buildings.capital_cost + cas22_capital + bop_capital
                         + special_materials_capital + cas28_capital      # 1cfe cas2x; NO CAS10
contingency.cost       = contingency_rate * cas2x_pre_contingency         # rebind :408
cas20_capital          = cas2x_pre_contingency + contingency.cost         # c20
indirect.cost          = indirect_fraction * cas20_capital * (ct/ref)     # rebind :417 -> cas20
cas30_capital          = indirect.cost
cas23_to_28_capital    = bop_capital + special_materials_capital + cas28_capital   # c23..c28
overnight_capital      = preconstruction_capital + cas20_capital + cas30_capital
                         + owner.cost + supplementary.cost                # CAS10 enters HERE
total_capital          = overnight_capital        # CAS60 Option C: idc.cost is a REPORTED line, NOT added here
```

What changes from today, and why each is correct against 1cfe:

- **CAS22 tail → inside `cas22_capital` → inside cas2x** → correctly receives CAS29 + CAS30 (c22 ∈ cas2x in 1cfe). ✓
- **`cas28_capital` added** (F-2): 5.0 M$ `cas28_digital_twin`, a fed design input with citation.
- **Contingency rebased** from `direct_capital` to `cas2x_pre_contingency` — drops CAS10 from the base (F-3). ✓
- **Indirect rebased** from `direct_capital` to `cas20_capital` (post-contingency) — matches 1cfe's `c30` on `c20` (F-3). ✓
- **CAS10 moves to the overnight level** — no longer contingency/indirect-scaled, matching 1cfe; isolates its own +86.5% error (F-4) so it no longer contaminates cas20/cas30/CAS50. ✓
- **CAS40 and CAS50 added at the overnight level, NOT into cas2x** — they receive no CAS29/CAS30 (correct: 1cfe adds c40/c50 at overnight; CAS50 carries its own c59 internally). ✓

After this, at the handshake point `cas20_capital → 5710.95`, `cas30_capital → 1522.92`, `overnight → 7872.15` — matching 1cfe, so CAS50 (which consumes them) comes under A-2.

**Rejected alternative — narrow isolated-aggregate (shadow cas20/cas30).** *(Owner ruled the full rebuild, 2026-07-20; this stays as a decision record, not an instruction.)* CAS50's A-2 needs only faithful `cas20`/`cas23_to_28`/`cas30` *as CAS50's inputs*. These could be built as dedicated shadow attributes feeding CAS40/CAS50 only, leaving `direct_capital`/contingency/indirect/`total_capital`/LCOE untouched. That is strictly less code and does not move the existing headline. **Rejected because:** it leaves two divergent notions of `cas20`/`cas30` coexisting in one model (the flat rollup's and CAS50's shadow), it leaves F-2/F-3/F-4 open as itemized A-4 remainders rather than closed errors (the criterion-3 ruling authorizes closing errors), and it keeps the model's headline LCOE knowingly wrong (indirect on a CAS10-inflated pre-contingency base). The full rebuild is one coherent 1cfe-faithful chain with a single `cas20`/`cas30`.

### D2b — Staged-twin propagation (codegen input; must not be skipped)

Codegen's actual input is not the canonical `models/` tree — it is the **staged twin** at `exploration/stellarator_e2e/models/`, from which `stellarator.snapshot.json` was captured (59 path refs into the staged tree; `snapshot()` at `handshake_1costingfe.py:128` reads the staged files). `sysml-codegen generate --from-snapshot` consumes that snapshot; the `.sysml` files matter only at capture time, and capture reads the staged tree. **If D1/D2/D5 land only on canonical `models/`, the recapture reads a stale twin and every A-2/A-4 result and the design-point re-baseline is computed against the old flat rollup — a silent wrong result, not a loud failure.** This is the WI-025/WI-027 pattern.

Therefore, as a first-class part of D1/D2/D5:

- **Edit both trees region-identical.** The 7 new defs land in the library twin `exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` (note: `models/analyses/`, not `models/library/analyses/`) as well as canonical; the D2 restructure lands in both `mfe_plant.sysml` copies; the D5 bindings land in both `stellarator_plant.sysml` copies.
- **Reconcile, do not blind-overwrite.** The staged `mfe_plant.sysml` carries extra "Item 10" comment lines and known WI-015 `DEMO-NOTE` divergences; apply the same *regions*, keeping those staged-only lines.
- **Mirroring diff gate.** Before recapture, a staged-vs-canonical region diff must show only the intended WI-028 edits plus the known Item-10 / DEMO-NOTE divergences — any other delta is a defect that blocks recapture.
- **Recapture from the staged tree.** After the twin carries the restructure, recapture `stellarator.snapshot.json` from `exploration/stellarator_e2e/models/`; that snapshot is what codegen consumes for every downstream A-2/A-4/oracle result.

### D3 — CAS50 wiring (the risky construct)

CAS50 consumes three derived aggregates — `cas20_capital`, `cas23_to_28_capital`, `cas30_capital` — where `cas30_capital` itself depends on `cas20_capital`, which depends on `contingency.cost`, which depends on `cas2x_pre_contingency`. A 4-deep cross-calc DAG.

This extends the **proven** WI-025 pattern (calc output → attribute sum → calc input: `direct_capital → contingency/indirect`) by one level, and the WI-010 SV-024 precedent shows cross-calc binding codegens. The parse check on `plant_chain_probe.sysml` confirms the exact shape resolves (calc → attribute → calc → attribute → calc, with `supplementary` reading both `cas20_capital` and `cas30_capital`). **Binding order is a codegen-topological-sort question that parse cannot fully settle** — a full codegen capture is the first plan-stage checkpoint (Validation Plan), not a design blocker, given the two precedents.

### D4 — CAS60 / IDC: Option C, ruled (MR-WI028-3)

**Ruling: genuine convention choice, not mechanical fall-out.** Both conventions reduce to `annual_capital = CRF · overnight · IDC_multiplier`, but the multiplier differs and the placement of the CAS60 line differs:

- **1cfe:** `IDC_mult = 1 + f_idc = 1.282476` (uniform-spend closed form); CAS60 is an explicit capital line; `total_capital = overnight + CAS60`; `CAS90 = CRF·total_capital`.
- **model:** `idc_factor = (1+d)**(Yc/2) = 1.07**4 = 1.310796` (even-spend midpoint); no CAS60 line; `annual_capital = total_capital(overnight) · idc_factor · CRF` inside LCOE (`mfe_lcoe_dcf.sysml:47-52`).

Different magnitudes (1.2825 vs 1.3108) and different financing conventions. **Double-count hazard:** adding CAS60 into `total_capital` while LCOE keeps multiplying by `idc_factor` counts IDC twice.

**Ruled: Option C** ([OWNER] 2026-07-20, `work/orchestration/handshake-account-scope.md` "Owner gate rulings"). CAS60 is computed as a **reported, A-2-checked line, EXCLUDED from `total_capital`**; the model's DCF `idc_factor` (`mfe_lcoe_dcf.sysml:47-52`) stays **untouched**. Concretely:

- The `'IDC Closed-Form Cost'` calc reproduces the 1cfe CAS60 line as a value and the handshake compares it under A-2 against `costs_musd.cas60` (exact closed-form on `overnight_capital`).
- `total_capital = overnight_capital` — the CAS60 line is **not** added in. No double-count: the model's LCOE keeps its `idc_factor`, and CAS60 is reported-only.
- The `total_capital` convention difference (1cfe folds CAS60 into `total_capital`; the model folds IDC into the LCOE `idc_factor`) is itemized under A-4 (D7).
- LCOE-side reconciliation of the two IDC conventions remains **Item 4 scope**, not touched here.

The design is CAS60-independent by construction: CAS22 tail, CAS40, CAS50 all feed a complete `overnight_capital`; Option C leaves that untouched and only adds a reported line.

### D5 — Handshake side (`emit_1cfe_point.py`, `handshake_1costingfe.py`)

The emitter already carries the reference values (`cas22_detail_musd` all eight tail accounts; `costs_musd.cas40/cas50/cas60/cas20/cas30`; `power_table.p_cryo`). Additions:

- **`emit_1cfe_point.py`:** add to `refs` the new CONST bases so the handshake can both feed them (×1e6) and assert them against 1cfe config (A-5): `remote_handling_dt_base` (150.0), `fuel_handling_dt_base` (120.0), `installation_frac` (0.14), `owner_cost_dt` (via `cc.owner_cost(DT)` = 41.2), `shipping_frac` (0.015), `spare_parts_frac_dt` (via `cc.spare_parts_frac(DT)` = 0.03), `tax_frac` (0.01), `construction_insurance_frac` (0.015), `startup_fuel_dt` (via `cc.startup_fuel(DT)` = 40.0), `decom_provision_dt` (via `cc.decom_provision(DT)` = 272.0), `cas28` (already in `costs_musd`), and `concept_scale` (1.0, stellarator).
- **`handshake_1costingfe.py`:** add SysML channels for the ten accounts + CAS60 line to `CH`; feed the new bases into the injection map (×1e6); add explicit comparison rows for C220110/111/200/300/400/500/600/700, CAS40, CAS50, CAS60 (MR-WI028-8, A-4); the comparison *logic* is unchanged — only new rows and inputs.

Instance bindings (`models/designs/stellarator_09/stellarator_plant.sysml` **and its staged twin — D2b**), all dollar conversions of pinned constants with MR-4 citations, placed next to the WI-025 building/precon bindings:

| Account | base (→ $) | ref/α | power |
|---|---|---|---|
| C220110 | 150.0e6, concept_scale 1.0 | 1100 / 0.5 | p_et (per-module) |
| C220111 | frac 0.14 | — | powercore_capital + remote_handling.cost |
| C220200 | 166.0e6, 40.6e6 | 1000, 3500 / 0.55 | p_net, p_th |
| C220300 | 1100.0 (aux/MW), 200.0e6 | 30 / 0.7 | p_th, cryo_elec.p_elec |
| C220400 | 1.96e6 | 1000 / 1.0 | p_th |
| C220500 | 120.0e6 | 1000 / 0.7 | p_net |
| C220600 | 11.5e6 | 1000 / 0.8 | p_net |
| C220700 | 85.0e6 | 3500 / 0.65 | p_th |
| CAS40 | 41.2e6 | 1000 / 0.5 | p_net |
| CAS50 | 0.015/0.01/0.015/0.03 fracs; 40.0e6/272.0e6 | 1000 | cas20/cas23_28/cas30, p_net |
| cas28 | 5.0e6 | — | — |

`p_cryo` binds from `cryo_elec.p_elec` (`mfe_plant.sysml:238` proves it is available as a cross-calc source).

### D6 — Trap assertions (MR-WI028-6 / A-5)

Every new mapping asserted in the handshake, added to the trap table:

1. **Plant-total vs per-module:** coolant/waste/fuel/other/I&C/aux-aux-term use `n_mod·power`; CAS40 uses `n_mod·p_net`; C220110 uses per-module `p_et` (no n_mod); C220300 cryoplant uses per-module `p_cryo`.
2. **Reference-power split:** C220110 → ref_gross 1100; coolant-primary / fuel / other / CAS40 → ref_net 1000; I&C / coolant-intermediate → 3500; waste → 1000; cryoplant → 30.
3. **Installation base:** `reactor_subtotal = Σ(C220101..C220110)` = powercore + remote_handling (excludes C220111/112; C220109 = 0 for this concept, documented).
4. **Fuel-keyed bases** match `cc` for DT: remote_handling 150, fuel_handling 120, owner 41.2, spares 0.03, startup 40, decom 272.
5. **F-2/F-3 structural asserts:** `cas28_capital` present (5.0); CAS10 at overnight (absent from cas2x / contingency / indirect base); indirect on `cas20_capital` (post-contingency).
6. **CAS60 Option C:** `total_capital == overnight_capital` (the CAS60 `idc.cost` line is reported but NOT summed into `total_capital`); the LCOE `idc_factor` is unchanged — guards the double-count hazard.

### D7 — A-4 itemized remainders after WI-028

- **C220106_pump** $0.721 M — standing, explained (SysML vessel calc is shell-only).
- **CAS10** model 34.5 vs 1cfe 18.5 M$ (+16.0 M$) — pre-existing WI-025 remainder (F-4), now isolated at the overnight level (no longer contaminates cas20/cas30/CAS50). Itemized, explained-and-kept.
- **CAS60 / total_capital convention** (Option C, ruled) — the CAS60 *account line* comes under A-2 (closed-form on `overnight_capital`), reported but excluded from `total_capital`. The `total_capital` row difference — 1cfe folds CAS60 into `total_capital` (10095.84 M$); the model keeps `total_capital = overnight_capital` (7872.15 M$) and folds IDC into the LCOE `idc_factor` — is itemized under A-4. LCOE-side reconciliation is Item 4 scope.

The residual LCOE gap reconciles to this itemized sum plus the CAS60/`total_capital` convention difference (A-4).

---

## Cross-file bindings

| Binding | Source | Consumer |
|---|---|---|
| `p_th`, `p_net`, `p_et` | `pb.*` aliases (`mfe_plant.sysml:244-246`) | tail account calcs |
| `p_cryo` | `cryo_elec.p_elec` (`mfe_plant.sysml:238` precedent) | aux_cooling calc |
| `powercore_capital` | `mfe_plant.sysml:389-392` | installation.reactor_subtotal, cas22_capital |
| `cas20_capital`, `cas23_to_28_capital`, `cas30_capital` | new attrs (D2) | supplementary calc |
| `overnight_capital` | new attr (D2) | idc calc (CAS60) |
| new unit-cost bases | `stellarator_plant.sysml` instance (both trees, D2b) | tail / owner / supplementary calcs |
| the whole D1/D2/D5 edit set | **canonical `models/` AND staged `exploration/stellarator_e2e/models/` (D2b)** | `stellarator.snapshot.json` recapture → codegen |

Dataflow stays unidirectional: powers/geometry → accounts → cas2x → contingency → cas20 → indirect → cas30 → overnight → (gated) total_capital → LCOE. No cycles.

---

## Validation Plan

1. **Parse (Level 1-3):** new calc defs and the restructured plant parse clean under `uv run python -m syside check`. **DONE this stage** (Validation Report).
2. **Codegen capture (first plan-stage checkpoint):** after the D2b staged-twin edit + mirroring diff gate, **recapture** `stellarator.snapshot.json` from `exploration/stellarator_e2e/models/`, then `sysml-codegen generate --from-snapshot`; confirm the 4-deep cas2x→…→supplementary chain compiles to instance-scoped aggregation producers in correct topological order (the WI-010/WI-025 precedent predicts pass; this is the explicit de-risk of D3). Every downstream step runs against the recaptured snapshot.
3. **A-2 per-account (SV-034):** run `handshake_1costingfe.py`; each of the eight tail accounts + CAS40 + CAS50 (+ CAS60 per gate) under |rel dev| ≤ 1e-6 vs 1cfe float32 at the handshake point.
4. **Rollup match:** `cas20_capital → 5710.95`, `cas30_capital → 1522.92`, `overnight → 7872.15` reproduce 1cfe (the direct/indirect rows move from −18.64% to ~0).
5. **Design-point re-baseline (MR-WI028-9):** record the new Stellaris headline; oracle bit-exact rel 1e-9 holds at the new point.
6. **G-8 re-baseline:** `handshake_comparison.json` gains the new rows, re-baselined as an explicit commit; comparison logic untouched.
7. **Standing bars (MR-WI028-10):** pytest 11/18/14/0; regen stability L1=0; WI-022 sha256 survives; IFE A/B byte-exact; PROTOCOL honored.

---

## Validation Report (design stage)

- **Parse:** `mfe_tail_supplementary_costs.sysml` (7 calc defs serving 11 accounts) — **Checks passed!**
- **Cross-calc chain:** `plant_chain_probe.sysml` (full cas2x→contingency→cas20→indirect→cas30→supplementary, with supplementary reading cas20 + cas30) parsed against the real `mfe_account_costs.sysml` deps — **Checks passed!** The several namespace-shadowing *warnings* (on `alpha` ×5, `cas20`, `cas23_to_28`, `cas30`, `p_net`) are all probe artifacts of the `in x = x` binding idiom; the real plant binds qualified names (`pb.p_net`, `cryo_elec.p_elec`) and does not trigger them.
- **Assembly reproduction:** the full 1cfe overnight/total/LCOE chain re-derived independently and matched to `onecfe_point.json` to the cent (see re-derivation section).
- **Codegen capture:** NOT run this stage (requires a full-plant snapshot+generate — a plan-stage activity). Scheduled as Validation Plan step 2. Not fabricated.
- **Prototype status:** PASS (parse + assembly-reproduction); codegen PENDING (plan step 1).

---

## Implementation Checklist (for `/plan-model`)

**Every `.sysml` edit lands region-identical in BOTH trees (D2b): canonical `models/` and staged `exploration/stellarator_e2e/models/`. The staged tree is what the snapshot recapture reads.**

1. **Library (both trees):** add the 7 calc defs to `models/library/analyses/mfe_account_costs.sysml` AND the staged twin `exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` (from `prototype/mfe_tail_supplementary_costs.sysml`).
2. **Generic plant (both trees):** restructure `mfe_plant.sysml` overnight assembly (D2) in canonical and staged copies: new tail account usages, `cas22_tail_capital`/`cas22_capital`/`cas28_capital`/`cas2x_pre_contingency`/`cas20_capital`/`cas30_capital`/`cas23_to_28_capital`/`overnight_capital`; rebind contingency → cas2x, indirect → cas20; add owner/supplementary at overnight; add idc (wiring per CAS60 gate). Reconcile the staged copy's Item-10 / DEMO-NOTE lines, don't blind-overwrite.
3. **Instance (both trees):** bind the new bases in `stellarator_plant.sysml` (D5 table) in canonical and staged copies, MR-4 citations, next to WI-025 bindings.
4. **Mirroring diff gate + recapture** (Validation Plan step 2): staged-vs-canonical region diff shows only the intended WI-028 edits + known Item-10/DEMO-NOTE divergences; then recapture `stellarator.snapshot.json` from the staged tree; codegen-capture checkpoint (confirm the 4-deep chain compiles) before proceeding.
5. **Harness:** `emit_1cfe_point.py` refs additions; `handshake_1costingfe.py` channels + rows + injection + traps (D5/D6).
6. **Re-baseline & validate:** SV-034 (against the recaptured snapshot); re-baseline `handshake_comparison.json` as an explicit commit; record design-point headline; oracle bit-exact; trap table.
7. **CAS60 (Option C, ruled):** wire the `idc` calc to read `overnight_capital` and expose its `cost` as a **reported channel**; keep `total_capital = overnight_capital` (idc NOT summed in). Leave `mfe_lcoe_dcf` `idc_factor` untouched (both trees). Add the CAS60 A-2 comparison row and the `total_capital`-convention A-4 itemization (D7); LCOE-side reconciliation is Item 4, out of scope here.

---

## Risks

1. **[Risk, low] CAS60 double-count if Option C is mis-implemented.** Mitigation: Option C is ruled — CAS60 is a reported line, `total_capital = overnight_capital` (idc NOT summed in), `idc_factor` untouched; the D6 traps assert CAS60 is excluded from `total_capital`.
2. **[Risk, high] Staged-twin skip (M1).** Codegen reads the staged twin, not canonical `models/`. If the D1/D2/D5 edits land only on canonical, every A-2/A-4/oracle result runs against the stale flat rollup — a silent wrong result. Mitigation: D2b makes twin propagation first-class — both trees edited region-identical, a staged-vs-canonical mirroring diff gate, recapture from the staged tree before any downstream step.
3. **[Risk, medium] Codegen binding order on the 4-deep chain.** Mitigation: parse validated; WI-010/WI-025 precedent; explicit codegen-capture checkpoint (against the recaptured snapshot) before the A-2 runs.
4. **[Risk, medium — scope] The overnight rebuild touches WI-025 contingency/indirect wiring.** Ruled in-bounds by the owner (2026-07-20): it closes F-2/F-3/F-4 (criterion-3 authorizes closing errors) and corrects the headline LCOE. It moves the design-point headline beyond just "adding accounts" — expected re-baseline (MR-WI028-9), verified by the oracle bit-exact bar at the new point.
5. **[Risk, low] n_mod=1 hides per-module vs plant-total.** Mitigation: n_mod explicit in every def; A-5 asserts the split.
6. **[Risk, low] Float32 near the A-2 ceiling.** Mitigation: measure; itemize under A-4 if any account legitimately cannot meet 1e-6.

---

## Toolchain pins (verified live this stage)

| Tool | Expected (WI-027 close) | Live HEAD | Pin status |
|---|---|---|---|
| 1costingFE | `0254385` | `0254385` (checked out) | ✓ on pin |
| agentic-mbse | `4c18d61` | `4c18d61` | ✓ on pin |
| sysml-codegen | `06d95f8` (cert `1c85042`) | `baf455d` | **moved** — `06d95f8` reachable |
| teax | `07eb0ac` | `c342b10` | **moved** — `07eb0ac` reachable |

sysml-codegen and teax HEADs have advanced past the WI-027 pins (upstream lifecycle epic in flight). Both WI-027 pins remain reachable. **This item pins to the WI-027 commits** (`sysml-codegen 06d95f8`, `teax 07eb0ac`) — movement is adopted deliberately, never implicitly (spec Standing bars). The plan/implement stage checks out these pins for codegen/exec; any adoption of the newer HEADs is an explicit owner-visible decision, not a side effect.

---

## Traceability

- **1cfe formulas (pin 0254385):** `cas22.py:631-731`, `costs.py:239-297`, `model.py:1479-1500`, `economics.py:78-92` — all re-read this stage.
- **Requirements:** MR-WI028-1..10 (spec); A-2/A-3/A-4/A-5/A-6 + G-8 (anchor spec); MR-3, MR-4.
- **Model (canonical):** `models/library/analyses/mfe_account_costs.sysml`, `mfe_lcoe_dcf.sysml:47-52`, `models/designs/generic_mfe/mfe_plant.sysml`, `models/designs/stellarator_09/stellarator_plant.sysml`.
- **Model (staged twin — codegen input, D2b):** `exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml`, `.../models/designs/generic_mfe/mfe_plant.sysml`, `.../models/designs/stellarator_09/stellarator_plant.sysml`; snapshot `exploration/stellarator_e2e/stellarator.snapshot.json` (recaptured from the staged tree).
- **Harness:** `exploration/stellarator_e2e/{emit_1cfe_point.py, handshake_1costingfe.py, handshake_comparison.json, onecfe_point.json}`.
- **Prototype:** `prototype/mfe_tail_supplementary_costs.sysml`, `prototype/plant_chain_probe.sysml`.
