---
Status: complete
Created: 2026-08-30
Updated: '2026-09-01'
Related Artifacts:
  Spec: ./spec.md
---

# WI-035 Design: Magnet Closure — Derived Field, Structural Limit, Decomposed Cost Accounts

**Approved 2026-08-30** `[AGENT] (approval delegated by owner 2026-08-30 — "manage it per your best judgement")`. Proceeds to `/plan-model`.

Design for the three moves the spec requires, under the checkpoint ruling (`spec.md` § Open decisions, ruled 2026-08-30): **inversion** — coil current is the design lever, the field is computed. Every quantitative basis below is image-verified or pinned-code-verified; the § Research findings section records where the text extraction was wrong and the image overrode it.

## Overview

Today the instance holds `B = 9.0` and every magnet quantity hangs off it. Afterward: the plant computes `B_axis` from the coil-set current, `B_peak` and beta respond to it, a winding-pack stress constraint with a computed operand pushes back on coil current and winding-pack sizing, and the magnet capital splits into a winding-pack account (real winding length) plus a casing-structure account, with the old conductor-proxy lump kept alive as a 1cfe-form comparison channel. One new library calc file, three touched library files, plant rewiring, instance rebinds, twins mirrored.

## Research findings

**Image verification caught real corruption.** Per `SOURCE_INDEX.md`, the iter-01 text tables are corrupted LLM reconstructions; every table value here was read from the page images (`knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/`):

- **Table 2** (`page_002_table_0.png`): axis av. field **9.0 T**, peak conductor field **24.9 T**, **peak coil current (single coil) 15.4 MA**, **48** toroidal field coils, R 12.7 m, stored energy 111 GJ. The field path below is built entirely from this one printed set.
- **Table 8** (`page_022_table_0.png`): per-coil ampere-turns **15.4 / 14.6 / 13.8 / 12.9 / 12.5 / 11.2 MA** (the text extraction printed 14.4 and 12.9 for coils 1 and 4 — wrong); sum × 8 occurrences = **643.2 MA-turns** total. J_WP 119/112/120/112/122/124 A/mm². Cross-section side lengths **360/360/340/340/320/300 mm**. Coil masses (no casing) 24.2/25.4/21.6/21.5/19.0/17.0 t (the text showed 44.5–55.4 t — wrong; the image set × 8 = 1029.6 t matches the WI-024 `vol_cold_cryo` cross-check). **Peak stress on WP: <650 MPa** (a single spanning value; the text showed em-dashes). Max WP linear force 174 MN/m (coil 0). Total energy 110.58 GJ.
- **Table 7** (`page_021_table_0.png`): winding-pack material fractions **tape 9 / Cu 35 / solder 12 / steel 36 / He 8 %** (the text's 15/10/45/26/4 is wrong).
- **§ 2.9 prose** (raw.pdf-backed): typical coil circumference **25 m**; turn current capped at 50 kA; **NI coils are passively quench-protected** ("self-protecting mechanism without complex external systems") — the printed basis for costing no separate quench-protection account.
- **§ 2.10 prose + Fig 49**: support structure = casings + inter-coil plates + inner support rings, AISI 316LN; design stress limit **800 MPa** (von Mises proxy for membrane+bending, ASME BPVC VIII-2 / Eurocode framing; yield ~1000 MPa at 20–30 K); winding-pack peak ~600–650 MPa, casings <700 MPa; **casing cast parts 63–200 t**; plates ≤58 t; rings ~200 t each. No total structure mass is printed.
- **1costingFE at pin `0254385`**: `coil_cu_fab_markup = 3.5` ("winding, insulation, cooling, jointing, test", `costing_constants.yaml:50`); `coil_steel_price_per_kg = 6.0`, `coil_steel_fab_markup = 3.0` ("coil-case / inter-coil support fabrication", `:52-53`); the stellarator `coil_markup = 5.87` documented as tokamak 3.09 (SPARC-calibrated) × 1.9 (NCSX non-planar production overrun), with the longer winding path handled *separately* by the ×2 path factor inside `G = 8π²` (`:60-72`); "conductor is ~10-15% of finished magnet cost" (`cas22.py:34`).
- **The linkage physics** (WI-032, closed): Ampère's law on the axis gives 571.5 MA-turns; the printed coil set carries 643.2 — the ~12.5% excess is the shaping current that does not link the axis. Any field↔current relation for this coil set carries a held linkage fact.
- **The codegen envelope**: reference redefinitions survive the pinned codegen — `:>> r_coil = rb.r_coil` and the four WI-021 volume bindings (`mfe_plant.sysml:51,64-76`) flow through `generated/pipelines/pipeline.yaml:85-90`. Arithmetic redefinition expressions are dropped (WI-030 gotcha) — instance bindings stay literal.

## Design decisions

**D1 — Lever set (ruled).** The design lever is `I_coil`, the peak single-coil current (15.4 MA, Table 2). `magnet__B` retires as an entry point. Held coil-set facts (all float64 of printed pairs, the WI-030 `peak_ratio` convention): `k_link`, `f_set`, `k_sigma` below.

**D2 — Field path.** New calc `'Coil Set Axis Field'`:

```
B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)
```

`k_link = 0.7731331164622419` — the float64 of (2π·R0·B/μ0)/(n_coils·I_coil) at the Table-2 set (9.0 T, 12.7 m, 48, 15.4 MA). It bundles two printed facts, both disclosed in the binding doc: the per-coil current distribution (Table 8: mean/peak = 643.2/739.2 = 0.870) × the axis-linkage of the total (571.5/643.2 = 0.888, the modular-coil shaping current WI-032 identified). **Exact roundtrip to 9.0 is unattainable in float64** — a ±6-ulp search finds no `k_link` giving exactly 9.0; the chosen value yields `B_axis = 8.999999999999998` (1 ulp low) and `B_peak = 24.899999999999995` — *below* the 24.9 ceiling, so `peak_field_ok` is satisfied with a real (if tiny) margin instead of margin-0-by-construction, and the low side is chosen deliberately so the verdict cannot flip on rounding. Design-point tolerance: ≤ 1 ulp on `B_axis` (SV-038); all committed comparison gates operate at rel 1e-9.

Wiring: the plant computes `field_calc` and EXPOSEs it into the magnet part — `:>> B = field_calc.B_axis` — the proven WI-021 reference-redefinition pattern, so `beta_calc`, `peak_field_calc`, and `magnet_cost` keep their existing `magnet.B` reads unchanged. The instance deletes its `:>> B = 9.0` binding.

**D3 — The limit: winding-pack stress (not J-margin, not turn-current).** New calc `'Winding Pack Stress'` and constraint `'Winding Pack Stress Limit'`:

```
sigma_wp = k_sigma * I_coil * B_peak / wp_side        assert: sigma_wp <= sigma_allow
```

The J×B×d form: force density (current × field) over the load-bearing dimension — the standard mean-stress scale for a winding. `k_sigma = 0.6102331403536223` — float64 anchored at the printed worst-coil pair (σ = 650 MPa at I 15.4 MA, B_peak 24.9 T, side 0.36 m; Table 8's "<650" bound taken *as* the value, conservative). `sigma_allow = 800e6` Pa (§2.10 design limit for cryogenic AISI 316LN). Design point: σ = **650.0 MPa exactly** (float64 roundtrip verified), margin **150 MPa** — nonzero, not by construction. Push-back: σ ∝ I·B_peak/side ∝ **I²/(R0·side)** — it resists raising coil current (field choice) and shrinking the winding pack (coil sizing), which is precisely the Row-3 P3 anchor. It is not redundant with `peak_field_ok`: the field ceiling binds on I alone; stress also binds on `wp_side` and R0, axes the ceiling cannot see.

Rejected: **J_op/J_crit ≤ 0.8** — the source prints ratios per coil but no J_crit(24.9 T, 20 K) number to bind as the limit; **turn-current ≤ 50 kA** — fully printed but the design point sits 0.4% under it, which would freeze every upward current move and swamp the fence structure; recorded as a candidate second fence for a later item, not asserted here.

**D4 — Winding-pack cost account.** New calc `'Winding Pack Cost'`:

```
kAm_wind = n_coils * I_coil * f_set * c_coil / 1000        cost = kAm_wind * cost_per_kAm * f_wp_fab
```

`f_set = 0.8701298701298701` (Table 8 set-mean over peak, 643.2/739.2); `c_coil = 25.0` m (§2.9 typical circumference — the same disclosed weak link `vol_cold_cryo` carries); `cost_per_kAm = 50.0` (existing REBCO binding); `f_wp_fab = 6.65` = 3.5 (cu-fab content: winding, insulation, cooling, jointing, **test** — content-matched appropriation from the pin, applied to the conductor cost base) × 1.9 (the documented NCSX non-planar fabrication penalty). Quench protection: $0 as a separate item — NI passive protection, printed (§2.9). Design point: `kAm_wind = 1.608e7` kA·m, conductor $0.804B, account **$5.3466B**. Cross-check: the conductor base is 12.7% of the old lump — inside the pin's own "conductor ~10–15% of finished magnet cost" band.

**D5 — Magnet structure (casing) account.** New calc `'Magnet Structure Cost'`:

```
cost = n_coils * m_casing * steel_price * f_steel_fab
```

`m_casing = 63000` kg — the **printed floor** of the §2.10 cast-part range (63–200 t), bound as a knowing lower bound with the seam named in the doc (the WI-024 `f_uplift_cryo` precedent) and the band [$54.4M, $172.8M] disclosed; `steel_price = 6.0` $/kg and `f_steel_fab = 3.0` from the pin (`coil_steel_*`, whose own comment names "coil-case" fabrication). Design point: **$54.4M**. Boundary against double-counting: this account is **casings only**; inter-coil plates, rings, and legs remain C220105's documented content (`'Structure Cost'`, $30.9M at baseline, untouched). Cross-check: the virial minimum structural mass ρE/σ = 7900 × 110.58 GJ / 800 MPa ≈ 1092 t < the 3024 t casing floor — consistent.

**D6 — Rollup and the comparison channel.** `magnet.capital_cost = winding_pack_cost.cost + magnet_structure_cost.cost` = **$5.4010B** at the design point, −14.6% against the $6.3235B lump. The delta is explained, not fitted (goal invariant): conductor quantity ×0.7463 (real current 643.2 vs 571.5 MA-turns, +12.5%; real length 25 m vs the 4π·r_coil = 37.7 m proxy, −33.7%) × markup recomposition 6.65/5.87 (+13.3%), plus $54M structure. `'Magnet Coil Cost'` **stays wired** (its B input now computed): its output is exposed as `magnet_capital_1cfe`, the 1cfe-form comparison channel, exactly the `lcoe`/`lcoe_1cfe` precedent — the errata history and A/B comparability survive as a live channel while the rollup moves to the decomposed accounts.

**D7 — Cryoplant sub-account visibility.** `'Aux Cooling Cost'` gains two additive outputs (`aux_cost`, `cryo_cost`; `cost` unchanged as their sum); the plant exposes `cryoplant_capital = aux_cooling.cryo_cost` — the separately-sized cryoplant account (power-law in the *computed* `p_cryo`), now visible as its own channel. `vol_cold_cryo` stays a held settable input (WI-032 R3 ruling; spec MR-WI035-6).

**D8 — Contract and committed-study restatement (MR-WI035-7).** Retired entry point: `stellarator_09__stellaris__magnet__B`. New entry points (all `design_attribute`): `magnet__n_coils`, `magnet__I_coil`, `magnet__k_link`, `magnet__f_set`, `magnet__c_coil`, `magnet__wp_side`, `magnet__k_sigma`, `magnet__sigma_allow`, `magnet__f_wp_fab`, `magnet__m_casing`, `magnet__steel_price`, `magnet__f_steel_fab`. Kept: `magnet__G`, `magnet__coil_markup`, `magnet__cost_per_kAm` (feed the comparison channel), `magnet__peak_ratio`, `magnet__B_max`. Committed studies, restated before any regeneration:

- `20260823-magnet-technology-ab` — **not reproducible as written**: its 74-value `B` axis retires (STUDY_POLICY §2.3). Replacement lever: `I_coil`; at fixed R0 the mapping is linear (B = k·I), so the swept window translates, but the arm definitions and case grid do not replay byte-for-byte.
- `20260829-p-pump-fence` — **not reproducible as written**: its (R, a) sweep held B = 9.0; post-inversion, `B_axis ∝ I_coil/R0`, so an R sweep at held current moves the field — physically intended (shrinking the machine at fixed ampere-turns raises the field), but the committed record's points mean something else.
- `20260821-power-cycle-ab` — axes untouched; its design point reproduces up to the 1-ulp field shift, but the package identity changes regardless.

Per the goal invariant (one promoted pin per round), all forward comparisons run against the new pin; the old records stand as history.

## Proposed design — elements and locations

| Element | Kind | File | Notes |
|---|---|---|---|
| `'Coil Set Axis Field'` | calc def (NEW) | `models/library/analyses/mfe_magnet_field.sysml` (NEW) | D2; μ0, 2π defaulted constants declared last |
| `'Winding Pack Stress'` | calc def (NEW) | `mfe_magnet_field.sysml` | D3 operand |
| `'Winding Pack Stress Limit'` | constraint def (NEW) | `models/library/analyses/mfe_viability.sysml` | D3; bindings-only assert pattern |
| `'Winding Pack Cost'`, `'Magnet Structure Cost'` | calc defs (NEW) | `models/library/analyses/mfe_magnet_cost.sysml` | D4/D5; `'Magnet Coil Cost'` kept, doc updated to comparison-form |
| `'Aux Cooling Cost'` split outputs | calc def edit | `models/library/analyses/mfe_account_costs.sysml` | D7, additive only |
| `'Magnet System'` new attributes | part def edit | `models/library/cost_structure/mfe_power_core.sysml` | 12 new attributes (D8 list); `B` stays declared (plant binds it) |
| `field_calc`, `wp_stress`, `wp_stress_ok`, cost calcs, EXPOSE, rollup, `magnet_capital_1cfe`, `cryoplant_capital` | plant edits | `models/designs/generic_mfe/mfe_plant.sysml` | structure only, no concept values (MR-WI035-4) |
| binding swaps + citations | instance edits | `models/designs/stellarator_09/stellarator_plant.sysml` | remove `:>> B`; add 12 literal bindings, each with image-verified Source/Ref/Basis |
| twins | mirror | `exploration/stellarator_e2e/models/**` | byte-identical edits |

All values live in the instance; library defs carry only defaulted physical constants (MR-WI035-4). Prototype stencils for every new def and the wiring shape are in the validated prototype (below).

## Cross-file bindings (plant)

| Input | Bound from |
|---|---|
| `field_calc.{n_coils, I_coil, k_link, R0}` | `magnet.*` |
| `magnet.B` | `field_calc.B_axis` (EXPOSE, reference redefinition) |
| `wp_stress.{I_coil, wp_side, k_sigma}` | `magnet.*` |
| `wp_stress.B_peak_in` | `peak_field_calc.B_peak` |
| `wp_stress_ok.{sigma_in, sigma_allow_in}` | `wp_stress.sigma_wp`, `magnet.sigma_allow` |
| `winding_pack_cost.{n_coils, I_coil, f_set, c_coil, cost_per_kAm, f_wp_fab}` | `magnet.*` |
| `magnet_structure_cost.{n_coils, m_casing, steel_price, f_steel_fab}` | `magnet.*` |
| `magnet.capital_cost` | `winding_pack_cost.cost + magnet_structure_cost.cost` |

Dataflow stays unidirectional: `magnet` inputs → `field_calc` → (`beta_calc`, `peak_field_calc`, `magnet_cost` comparison) → `wp_stress` → constraint; costs read inputs and computed field only. No cycles: `field_calc` reads only literal-bound magnet attributes; `magnet.B` is written by, never read by, `field_calc`.

## Expected design-point values (verification targets)

| Quantity | Expected | Basis |
|---|---|---|
| `B_axis` | 8.999999999999998 (9.0 − 1 ulp) | D2 float64 search |
| `B_peak` | 24.899999999999995 | × peak_ratio |
| `peak_field_ok` | satisfied, margin +5.3e-15 | vs B_max 24.9 |
| `sigma_wp` | 650.0 MPa exactly | D3 roundtrip verified |
| `wp_stress_ok` | satisfied, margin 150 MPa | vs 800 MPa |
| `kAm_wind` | 1.608e7 kA·m | D4 |
| winding-pack account | $5.3466B | D4 |
| magnet structure account | $54.432M | D5 |
| `magnet.capital_cost` | $5.401032B (−14.6% vs lump) | D6 |
| `magnet_capital_1cfe` | $6.3235B ± ulp-level | comparison channel, B now computed |
| beta, p_fus, powers | shift ≤ rel ~4e-16 | B moves 1 ulp |
| six existing verdicts | all satisfied | no operand crosses a fence at ulp scale |

Headline capital and LCOE move down materially (magnet −$0.92B → overnight ≈ −5.7%); recorded and explained at implement, not fitted (goal invariant; SV-016 stays `pending`, power balance untouched).

## Validation plan

- **L1**: `uv run python -m syside check` on every touched file, both trees (note: the `syside` console script is absent from this venv — invoke as `python -m syside`; license via `set -a; source ~/1cfe/agentic-mbse/.env; set +a`).
- **L2/L3**: offender list must equal the 6 pre-existing; zero new.
- **SV-038**: `B_axis`/`B_peak` at the table above (≤1 ulp); then a one-axis probe (I_coil ±10%) shows the field, beta, stress, and both magnet channels respond.
- **SV-039**: `wp_stress_ok` margin +150 MPa at design; verdict flips within an I_coil or wp_side sweep (stress fence at I·B_peak/side × k_sigma = 800 MPa, ≈ +11% in I at fixed geometry).
- **SV-040**: rollup identity `magnet.capital_cost = winding + structure` exact; markup-only path absent from the rollup (grep); `magnet_capital_1cfe` present as comparison.
- **Regen/verify/pin**: the `integrate` seam, invoked separately after implement (out of this item, per spec).

## Validation report (design-stage prototype)

Prototype `proto_magnet_closure.sysml` (scratchpad `wi035_proto/`): all four new calc defs, the constraint def, and the load-bearing wiring shape — a part-usage EXPOSE `:>> B = field_calc.B_axis` plus a bindings-only `assert constraint` — **"Checks passed!"** under `uv run python -m syside check` (syside 0.8.4). The EXPOSE pattern is additionally proven in production by WI-021's `:>> r_coil = rb.r_coil` (`mfe_plant.sysml:51`) surviving the pinned codegen into `pipeline.yaml:88`. Float64 roundtrips for `k_sigma` (650.0 exact) and `k_link` (1 ulp, low side chosen) verified numerically this session.

## Implementation checklist

1. Library: `mfe_magnet_field.sysml` (new), `mfe_viability.sysml` (+constraint), `mfe_magnet_cost.sysml` (+2 calcs, doc update), `mfe_account_costs.sysml` (split outputs), `mfe_power_core.sysml` (+12 attributes).
2. Plant: calcs, EXPOSE, assert, rollup rebind, two new exposed attributes.
3. Instance: delete `:>> B = 9.0`; add 12 literal bindings with image-verified citations (every Table-8/Table-2 value cites its page image; `m_casing` doc names the floor-bound seam; `k_link`/`k_sigma`/`f_set` docs show the printed-pair arithmetic).
4. Mirror both trees byte-identically; L1–L3.
5. Verify the generated module preserves the `magnet.B` EXPOSE and the constraint predicate; check expected-values table; record headline delta with the D6 decomposition.
6. Restate D8 in the item record **before** any regeneration.

## Risks

1. **Codegen drops the EXPOSE** (WI-030 gotcha class) — mitigated: reference redefinitions are the proven WI-021 pattern (checked in `pipeline.yaml`); fallback recorded: rebind the three B consumers directly to `field_calc.B_axis` and retire `B` from the part def.
2. **Ulp-level design point** — `B_axis` is 1 ulp under 9.0; chosen low so `peak_field_ok` cannot flip; all committed gates compare at rel 1e-9. Disclosed in SV-038.
3. **`m_casing` floor honesty** — the printed range is wide (63–200 t/casing); the floor is a knowing lower bound with the seam named and the band disclosed; the account is ≤0.03% of overnight capital either way.
4. **Markup content mapping contestable** (3.5 × 1.9 on the conductor base) — the delta vs the lump is fully decomposed in D6 and the lump survives as a live comparison channel; a reviewer can re-derive every factor at the pin.
5. **`c_coil = 25 m` approximate** — the same printed weak link `vol_cold_cryo` already carries, disclosed the same way.
6. **Expression-order dependence of the float64 roundtrips** — the emitted statement form must match the evaluation order used in the search; verified at implement against the generated module (tolerance is 1 ulp, not exact-match).
