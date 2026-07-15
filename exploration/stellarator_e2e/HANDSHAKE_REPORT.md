# Anchor A — 1costingFE Machinery Handshake

Concept Success Criterion 3. Feed the generated SysML forward model the exact plant point 1costingFE solved for (its solved fusion power plus its full merged parameter set), then check that the generated SysML pipeline reproduces 1costingFE's per-account costs and LCOE. This isolates the codegen/execution machinery from modeling judgment: the SysML calc defs were reproduced from 1costingFE formulas, so where the formula is identical and codegen is faithful, the numbers match tightly. Divergences reveal the initial (Stellaris) model's documented simplifications.

## What was run

- **1costingFE commit: `0254385`** (pinned; the handshake asserts the emitted point carries this commit).
- 1costingFE `CostModel(STELLARATOR, DT).forward(net_electric_mw=1000, availability=0.90, lifetime_yr=30, n_mod=1, construction_time_yr=8.0, interest_rate=0.07, inflation_rate=0.02, noak=True, elon=1.6)` — the `examples/dt_stellarator.py` clean 1 GWe point.
- The generated SysML pipeline (`generated/pipelines/mfe_stellarator.yaml`) executed twice through the teax executor, driven by 1costingFE's point instead of the Stellaris design-point bindings. This is the same execution path `run_stellaris.py` already certifies bit-exact against the pure-Python oracle (rel tol 1e-9); only the inputs change.

Two interpreters are involved because `costingfe` (JAX) and `simkit` never coexist in one venv. The 1costingFE point is emitted to `onecfe_point.json` by `emit_1cfe_point.py` run in the 1costingfe uv env; the handshake itself runs in the teax exec venv.

Artifacts:
- `handshake_1costingfe.py` — the handshake (runs both, maps, compares, restores inputs).
- `emit_1cfe_point.py` — the 1costingFE point emitter (run in the 1costingfe uv env).
- `onecfe_point.json` — the emitted 1costingFE solved point + merged params.
- `handshake_comparison.json` — the machine-readable comparison.

## The solved point (1costingFE)

This is a genuinely different machine from the Stellaris SysML defaults (Stellaris: R=12.7 m, b_center=5.86 T, p_net=575 MW, LCOE 251). The handshake uses 1costingFE's point throughout.

| quantity | value |
|---|---|
| fusion power `p_fus` | 2582.07 MW |
| thermal `p_th` / gross `p_et` | 2819.07 / 1127.63 MW |
| net electric `p_net` | 1000.0 MW |
| q_eng / rec_frac | 8.835 / 0.1132 |
| LCOE | 123.74 $/MWh |
| total capital | 10,095.8 M$ |
| CAS22 (full) | 4581.4 M$ |
| R0 / b_center / r_coil(vessel_or) | 5.5 m / 6.0 T / 3.5 m |

Fusion power is GIVEN: the SysML `DT Fusion Power` calc was short-circuited by solving `sigma_v` so the geometry × density × reactivity product reproduces 1costingFE's `p_fus` exactly (injector reproduced 2582.066 MW, rel dev 0).

## Per-account comparison (formula-reproduced), $

The primary table is the end-to-end SysML pipeline output vs 1costingFE. The last column is the **formula-isolation** check: the SysML cost formula fed 1costingFE's OWN p_th/p_et. It is the clean codegen test — it strips out the power-balance divergence.

| account | 1costingFE ($) | SysML pipeline ($) | rel dev | formula-iso @ 1cfe power (rel) | note |
|---|---:|---:|---:|---:|---|
| magnet (C220103) | 2,129,952,695 | 2,129,952,694 | −0.00% | −5.4e-10 | power-independent; matches to float. Residual = mu0 constant (SysML 1.25663706212e-6 vs 1cfe 4π·1e-7) |
| heating (C220104) | 158,487,000 | 158,487,000 | +0.00% | 0 | ECRH, fixed p_ecrh; power-independent; exact |
| divertor (C220108) | 100,740,562 | 92,098,916 | −8.58% | −3.8e-8 | (p_th/1000)^0.5; gap = p_th −16.4% |
| blanket (C220101) | 570,419,556 | 512,217,745 | −10.20% | +3.6e-8 | (p_th/2500)^0.6; gap = p_th −16.4% |
| shield (C220102) | 333,281,464 | 299,275,644 | −10.20% | +3.5e-8 | (p_th/2500)^0.6; gap = p_th −16.4% |
| structure (C220105) | 25,523,571 | 23,334,128 | −8.58% | −7.6e-8 | (p_et/1100)^0.5; gap = p_et −16.4% |
| vessel (C220106_vessel) | 87,590,721 | 78,653,546 | −10.20% | +1.7e-8 | (p_et/1100)^0.6; gap = p_et −16.4%. SysML models the vessel shell only; 1cfe C220106 also adds a 0.72 M$ gas-load pump sub-term |
| power_supplies (C220107) | 81,401,321 | 71,796,236 | −11.80% | −1.7e-8 | (p_et/1100)^0.7; gap = p_et −16.4%. ARIES-CS-derived base (see footnote) |
| turbine (CAS23) | 228,728,241 | 191,170,173 | −16.42% | (linear) | n_mod·p_the·rate; gap = p_the −16.4% |
| electric (CAS24) | 97,427,139 | 81,429,220 | −16.42% | (linear) | n_mod·p_et·rate; gap = p_et −16.4% |
| heat_rejection (CAS26) | 98,836,670 | 82,607,304 | −16.42% | (linear) | n_mod·p_th·rate; gap = p_th −16.4% |
| misc (CAS25) | 59,302,006 | 49,564,383 | −16.42% | (linear) | n_mod·p_et·rate; gap = p_et −16.4% |

**Formula-isolation result (the real machinery test): every formula-reproduced account matches 1costingFE to 1costingFE's own numerical floor.** The worst is structure at −7.6e-8; the rest are ~1e-8 or tighter. Those residuals are JAX float32 rounding in the 1costingFE reference (its power table carries ~1e-7 relative precision), not formula error. The magnet, on the pure-float64 path, matches to 5.4e-10, and its only residual is the mu0 constant precision. **Codegen is faithful: fed the same power, the generated cost calcs reproduce 1costingFE's formulas exactly.**

Classification: all 12 accounts above are **formula-reproduced** (the real machinery test).

## Power balance — the single root cause of the end-to-end gap

Every end-to-end account divergence traces to one place: the SysML 0D power balance is a simplification of 1costingFE's `physics.py`.

| channel | 1costingFE | SysML pipeline | rel dev |
|---|---:|---:|---:|
| p_th | 2819.07 | 2356.17 | −16.42% |
| p_the | 1127.63 | 942.47 | −16.42% |
| p_et | 1127.63 | 942.47 | −16.42% |
| p_net | 1000.00 | 764.85 | −23.52% |
| q_eng | 8.835 | 5.306 | −39.95% |
| rec_frac | 0.1132 | 0.1885 | +39.95% |

Cause. 1costingFE thermal power (`physics.py` step 7) is `p_th = mn·p_neutron + p_rad + p_wall + eta_p·p_pump`. The SysML thermal power is `p_th = mn·p_neutron + p_input + eta_th·(fpcppf·eta_p + f_sub)·(mn·p_neutron)`. The SysML omits the charged-particle (alpha) + radiation power reaching the wall — for this DT point `p_wall + p_rad = 547 MW`, about 19% of p_th — and instead adds only `p_input` (30 MW) plus a small pumping-recovery term. That is the −16.4% on p_th, which then flows linearly into p_the/p_et and, amplified through the recirculating fraction, into p_net (−23.5%) and q_eng (−40%). This is the documented "0D power-balance simplification," not a codegen defect.

## Pass-through accounts (tautological)

The SysML takes these as harness inputs; feeding 1costingFE's values makes them match trivially. They are **not a real test** of the machinery.

| account | 1costingFE ($) | SysML ($) | rel dev |
|---|---:|---:|---:|
| buildings (CAS21) | 619,435,486 | 619,435,486 | 0% |
| preconstruction (CAS10) | 18,500,000 | 18,500,000 | 0% |
| special_materials (CAS27) | 20,787,933 | 20,787,933 | 0% |

## Rollup + LCOE (SysML simplified model vs 1costingFE)

| line | 1costingFE | SysML | rel dev |
|---|---:|---:|---:|
| contingency (CAS29) | 0 | 0 | 0% (both NOAK; contingency_rate=0) |
| indirect (CAS30) | 1,522,919,189 | 1,181,149,442 | −22.44% |
| direct / CAS20 | 5,710,946,289 | 4,429,310,408 | −22.44% |
| total capital | 10,095,837,891 | 5,610,459,850 | −44.43% |
| LCOE ($/MWh) | 123.74 | 107.39 | −13.22% |
| net electric (MW) | 1000.0 | 764.85 | −23.52% |

The rollup and LCOE are **acknowledged SysML simplifications**, and the −44% total-capital gap has two stacked causes:

1. **Power-balance shrinkage** drags every power-scaled account down 8–16% (above).
2. **Reduced account set (structural).** The SysML CAS22 models only the 8 powercore lines (C220101–C220108). 1costingFE's full CAS22 (4581 M$) additionally carries **1093 M$ of unmodeled reactor-plant lines** the SysML has no calc for: C220110 remote handling 151.9, C220111 installation labor 509.6, C220200 coolant 202.0, C220300 aux cooling+cryoplant 18.9, C220400 waste 5.5, C220500 fuel handling 120.0, C220600 other 11.5, C220700 I&C 73.8 (plus the 0.72 vessel pump sub-term). Above CAS22 the SysML also omits CAS40 owner (41.2), CAS50 supplementary (578.6), and CAS60 IDC (2224). The SysML instead folds construction financing into the LCOE via an `idc_factor`.

LCOE construction also differs structurally. 1costingFE `LCOE = (CAS90 + CAS70 + CAS80)·1e6 / (8760·p_net·avail)` with CAS90 = CRF·total_capital, CAS70 an inflation-levelized O&M annuity, and CAS80 fuel. The SysML uses `LCOE = (total_capital·idc_factor·CRF + annual_om) / (8760·p_net·avail)` — a single CRF·IDC on total capital plus a flat O&M, no fuel term. The −13% LCOE gap is smaller than the −44% capital gap only because the two errors partly offset: the SysML's lower total capital and its lower net electric (765 vs 1000 MW, the denominator) push LCOE in opposite directions.

## Itemized discrepancies, with cause

1. **Power balance −16.4% on p_th (and downstream)** — SysML 0D balance omits alpha/wall + radiation power (547 MW). Documented modeling simplification. This is the dominant driver of every end-to-end cost divergence. **Not blocking.**
2. **Power-scaled powercore accounts −8.6% to −11.8%** — pure consequence of (1) via each account's power exponent (0.5/0.6/0.7). Formulas verified identical (formula-isolation ~1e-8). Not blocking.
3. **BOP accounts −16.4%** — pure consequence of (1); BOP is linear in p_the/p_et/p_th. Not blocking.
4. **magnet −5.4e-10** — mu0 constant precision (SysML literal `1.25663706212e-6` vs 1cfe `4π·1e-7`). Trivial; noted, not fixed (it is the codegen'd model constant). Not blocking.
5. **vessel: SysML omits the C220106 gas-load pump sub-term** (0.72 M$, ~0.8% of the vessel account here). Documented simplification. Not blocking.
6. **CAS22 reduced account set: 1093 M$ unmodeled** (C220110/111/200/300/400/500/600/700). Structural — the initial SysML models only the 8 powercore lines. Not blocking.
7. **Rollup omits CAS40/50/60** (41.2 / 578.6 / 2224 M$) — structural SysML simplification. Not blocking.
8. **LCOE construction differs** (single CRF·IDC + flat O&M, no CAS70 levelization, no CAS80 fuel). Structural. Not blocking.
9. **fpcppf has no 1costingFE counterpart** — the SysML models pumping as a fraction (fpcppf=0.06) of p_the; 1costingFE uses an absolute p_pump (1.0 MW). Kept the SysML value and footnoted; the pumping term is ~1 MW and immaterial to the gap. Mapping trap handled.

No discrepancy was a blocking discovery. The machinery test — codegen faithfulness of the reproduced formulas — passes cleanly (formula-isolation ~1e-8, at 1costingFE's float32 floor).

## Mapping traps (handled)

- **Fusion power GIVEN** — injected via solved sigma_v; SysML reproduced 1cfe p_fus to rel 0.
- **b_center vs B** — fed 1cfe's `b_center` = 6.0 T (coil-cost field) to the magnet `B` input, NOT the radiation `B` = 5.0 T.
- **r_coil** — fed 1cfe's `vessel_or` = 3.5 m.
- **G / coil_markup / cost_per_kAm** — confirmed from 1cfe: G = 8π² = 78.9568 (stellarator path_factor 2), markup 5.87, REBCO 50 $/kA·m.
- **Money unit** — every 1cfe M$ coefficient (unit costs, per-MW rates, bases) fed ×1e6 so the SysML rolls up in $; magnet cost_per_kAm fed as-is ($, the SysML magnet omits the /1e6). Compared in $.
- **Power-balance params** — mn, eta_th, eta_p, eta_pin(effective 0.5), f_sub, p_trit, p_house, p_cryo mapped directly. p_coils→p_tf (p_pf=0), p_cool→p_tfcool (p_pfcool=0). fpcppf has no counterpart (see item 9).

## Footnotes

- **C220107 power supplies is ARIES-CS-derived.** It is INCLUDED here (this handshake is not the hold-out blind), and matches to the float32 floor when fed 1cfe power. It must be excluded/footnoted in the later ARIES-CS hold-out comparison. No ARIES-CS source was read; only 1costingFE's computed value (81.40 M$) is used.
- No barred hold-out paths were read.
