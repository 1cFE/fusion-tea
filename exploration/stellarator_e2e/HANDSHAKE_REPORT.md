# Anchor A — 1costingFE Machinery Handshake

> **Updated 2026-07-14 (WI-019).** The faithful power balance landed: the SysML
> thermal power now recovers the alpha power (collapsed form of physics.py
> steps 4–7), `p_pump` is the same absolute input as 1costingFE, and the alpha
> fraction is exact. Result: every power channel and every power-scaled account
> now matches 1costingFE end-to-end at the float32 floor (≤1e-7). The remaining
> end-to-end gap is purely the documented structural scope (unmodeled CAS22
> tail, CAS40/50/60, LCOE construction). Numbers below are the re-run; the
> pre-WI-019 numbers are quoted inline where the delta is the story.

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

This is a genuinely different machine from the Stellaris SysML defaults (Stellaris: R=12.7 m, b_center=5.86 T; post-WI-019: p_net=786 MW, LCOE 189). The handshake uses 1costingFE's point throughout.

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

The primary table is the end-to-end SysML pipeline output vs 1costingFE. The last column is the **formula-isolation** check: the SysML cost formula fed 1costingFE's OWN p_th/p_et. Pre-WI-019 these two differed (the power balance diverged −16.4%); **after WI-019 the end-to-end run IS at 1costingFE's power, so both columns sit at the float32 floor.**

| account | 1costingFE ($) | SysML pipeline ($) | end-to-end rel | formula-iso rel | note (pre-WI-019 end-to-end) |
|---|---:|---:|---:|---:|---|
| magnet (C220103) | 2,129,952,695 | 2,129,952,694 | −5.4e-10 | −5.4e-10 | power-independent; residual = mu0 constant precision (was −0.00%) |
| heating (C220104) | 158,487,000 | 158,487,000 | 0 | 0 | ECRH, fixed p_ecrh; exact (was +0.00%) |
| divertor (C220108) | 100,740,562 | 100,740,562 | −6.5e-9 | −3.8e-8 | (p_th/1000)^0.5 (was −8.58%) |
| blanket (C220101) | 570,419,556 | 570,419,597 | +7.3e-8 | +3.6e-8 | (p_th/2500)^0.6 (was −10.20%) |
| shield (C220102) | 333,281,464 | 333,281,488 | +7.3e-8 | +3.5e-8 | (p_th/2500)^0.6 (was −10.20%) |
| structure (C220105) | 25,523,571 | 25,523,570 | −4.5e-8 | −7.6e-8 | (p_et/1100)^0.5 (was −8.58%) |
| vessel (C220106_vessel) | 87,590,721 | 87,590,726 | +5.5e-8 | +1.7e-8 | (p_et/1100)^0.6 (was −10.20%). SysML models the vessel shell only; 1cfe C220106 also adds a 0.72 M$ gas-load pump sub-term |
| power_supplies (C220107) | 81,401,321 | 81,401,324 | +2.7e-8 | −1.7e-8 | (p_et/1100)^0.7 (was −11.80%). ARIES-CS-derived base (see footnote) |
| turbine (CAS23) | 228,728,241 | 228,728,262 | +9.0e-8 | (linear) | n_mod·p_the·rate (was −16.42%) |
| electric (CAS24) | 97,427,139 | 97,427,144 | +4.4e-8 | (linear) | n_mod·p_et·rate (was −16.42%) |
| heat_rejection (CAS26) | 98,836,670 | 98,836,680 | +1.0e-7 | (linear) | n_mod·p_th·rate (was −16.42%) |
| misc (CAS25) | 59,302,006 | 59,302,008 | +3.6e-8 | (linear) | n_mod·p_et·rate (was −16.42%) |

**Every account now matches 1costingFE end-to-end at 1costingFE's own numerical floor** (worst: heat_rejection +1.0e-7; the reference power table is JAX float32, ~1e-7 relative precision). The magnet, on the pure-float64 path, matches to 5.4e-10, its only residual the mu0 constant precision. **Codegen faithfulness (formula isolation) was already proven pre-WI-019; the end-to-end match is the new WI-019 result (SV-025/SV-026).**

Classification: all 12 accounts above are **formula-reproduced** (the real machinery test).

## Power balance — RESOLVED by WI-019 (was the single root cause of the end-to-end gap)

The SysML power balance now matches 1costingFE channel-for-channel at the reference's float32 floor:

| channel | 1costingFE | SysML pipeline | rel dev | (pre-WI-019 rel dev) |
|---|---:|---:|---:|---:|
| p_th | 2819.07 | 2819.07 | +6.2e-8 | −16.42% |
| p_the | 1127.63 | 1127.63 | +6.2e-8 | −16.42% |
| p_et | 1127.63 | 1127.63 | +6.2e-8 | −16.42% |
| p_net | 1000.00 | 1000.00 | +4.6e-8 | −23.52% |
| q_eng | 8.835 | 8.835 | +3.4e-8 | −39.95% |
| rec_frac | 0.1132 | 0.1132 | −4.3e-8 | +39.95% |

The fix (WI-019, `models/library/analyses/mfe_power_balance.sysml`): thermal power is the collapsed faithful form of 1costingFE steps 4–7 — `p_th = mn·p_neutron + p_alpha + p_input + eta_p·p_pump`, exact in the DEC-free, non-radiation-limited regime because `p_rad + p_wall = p_alpha + p_input` identically (radiated and transported charged-particle power are both recovered at the wall). The pre-WI-019 form omitted the alpha term (547 MW at this point, ~19% of p_th). Also part of the fix: `p_pump` is 1costingFE's absolute input (the former `fpcppf` fraction had no 1cfe counterpart) and the alpha fraction is the exact ratio 3.52/17.58. This satisfies SV-025 (≤1e-5 required; measured ≤6.3e-8).

## Pass-through accounts (tautological)

The SysML takes these as harness inputs; feeding 1costingFE's values makes them match trivially. They are **not a real test** of the machinery.

| account | 1costingFE ($) | SysML ($) | rel dev |
|---|---:|---:|---:|
| buildings (CAS21) | 619,435,486 | 619,435,486 | 0% |
| preconstruction (CAS10) | 18,500,000 | 18,500,000 | 0% |
| special_materials (CAS27) | 20,787,933 | 20,787,933 | 0% |

## Rollup + LCOE (SysML simplified model vs 1costingFE)

| line | 1costingFE | SysML | rel dev | (pre-WI-019) |
|---|---:|---:|---:|---:|
| contingency (CAS29) | 0 | 0 | 0% (both NOAK) | 0% |
| indirect (CAS30) | 1,522,919,189 | 1,234,777,193 | −18.92% | −22.44% |
| direct / CAS20 | 5,710,946,289 | 4,630,414,472 | −18.92% | −22.44% |
| total capital | 10,095,837,891 | 5,865,191,665 | −41.90% | −44.43% |
| LCOE ($/MWh) | 123.74 | 85.55 | −30.87% | −13.22% |
| net electric (MW) | 1000.0 | 1000.0 | +0.00% | −23.52% |

The rollup and LCOE gaps are **acknowledged SysML simplifications**, and after WI-019 they have exactly one cause left:

1. ~~Power-balance shrinkage~~ — **resolved by WI-019** (every power-scaled account now at the float floor).
2. **Reduced account set (structural).** The SysML CAS22 models only the 8 powercore lines (C220101–C220108). 1costingFE's full CAS22 (4581 M$) additionally carries **1093 M$ of unmodeled reactor-plant lines** the SysML has no calc for: C220110 remote handling 151.9, C220111 installation labor 509.6, C220200 coolant 202.0, C220300 aux cooling+cryoplant 18.9, C220400 waste 5.5, C220500 fuel handling 120.0, C220600 other 11.5, C220700 I&C 73.8 (plus the 0.72 vessel pump sub-term). Above CAS22 the SysML also omits CAS40 owner (41.2), CAS50 supplementary (578.6), and CAS60 IDC (2224). The SysML instead folds construction financing into the LCOE via an `idc_factor`.

LCOE construction also differs structurally. 1costingFE `LCOE = (CAS90 + CAS70 + CAS80)·1e6 / (8760·p_net·avail)` with CAS90 = CRF·total_capital, CAS70 an inflation-levelized O&M annuity, and CAS80 fuel. The SysML uses `LCOE = (total_capital·idc_factor·CRF + annual_om) / (8760·p_net·avail)` — a single CRF·IDC on total capital plus a flat O&M, no fuel term.

**Why the LCOE gap GREW from −13% to −31%: a cancellation was removed, not a regression introduced.** Pre-WI-019 the understated net electric (−23.5%, the LCOE denominator) pushed LCOE *up* while the understated capital pushed it *down*; the −13% was the accident of those two errors partly offsetting. With the denominator now exact, the LCOE gap honestly shows the missing capital scope (unmodeled accounts + LCOE construction). The −31% is the true structural distance, and it is the measured target for the Stage-3 account-scope items (CAS22 tail, CAS40/50/60, CAS70/80, IDC treatment).

## Itemized discrepancies, with cause

1. **RESOLVED (WI-019). Power balance −16.4% on p_th (and downstream)** — the SysML balance now recovers the alpha power (collapsed physics.py steps 4–7); all six power channels ≤6.3e-8 (SV-025).
2. **RESOLVED (WI-019). Power-scaled powercore accounts −8.6% to −11.8%** — pure consequence of (1); now ≤7.3e-8 end-to-end (SV-026).
3. **RESOLVED (WI-019). BOP accounts −16.4%** — pure consequence of (1); now ≤1.0e-7 end-to-end (SV-026).
4. **magnet −5.4e-10** — mu0 constant precision (SysML literal `1.25663706212e-6` vs 1cfe `4π·1e-7`). Trivial; noted, not fixed (it is the codegen'd model constant). Not blocking.
5. **vessel: SysML omits the C220106 gas-load pump sub-term** (0.72 M$, ~0.8% of the vessel account here). Documented simplification. Not blocking.
6. **CAS22 reduced account set: 1093 M$ unmodeled** (C220110/111/200/300/400/500/600/700). Structural — the initial SysML models only the 8 powercore lines. Not blocking.
7. **Rollup omits CAS40/50/60** (41.2 / 578.6 / 2224 M$) — structural SysML simplification. Not blocking.
8. **LCOE construction differs** (single CRF·IDC + flat O&M, no CAS70 levelization, no CAS80 fuel). Structural. Not blocking. Now fully visible as the −31% LCOE gap (see rollup section).
9. **RESOLVED (WI-019). fpcppf has no 1costingFE counterpart** — the calc now takes 1costingFE's absolute `p_pump` [MW] directly; the mapping trap no longer exists.

No discrepancy was a blocking discovery. The machinery test — codegen faithfulness of the reproduced formulas — passes cleanly (formula-isolation ~1e-8, at 1costingFE's float32 floor).

## Mapping traps (handled)

- **Fusion power GIVEN** — injected via solved sigma_v; SysML reproduced 1cfe p_fus to rel 0.
- **b_center vs B** — fed 1cfe's `b_center` = 6.0 T (coil-cost field) to the magnet `B` input, NOT the radiation `B` = 5.0 T.
- **r_coil** — fed 1cfe's `vessel_or` = 3.5 m.
- **G / coil_markup / cost_per_kAm** — confirmed from 1cfe: G = 8π² = 78.9568 (stellarator path_factor 2), markup 5.87, REBCO 50 $/kA·m.
- **Money unit** — every 1cfe M$ coefficient (unit costs, per-MW rates, bases) fed ×1e6 so the SysML rolls up in $; magnet cost_per_kAm fed as-is ($, the SysML magnet omits the /1e6). Compared in $.
- **Power-balance params** — mn, eta_th, eta_p, eta_pin(effective 0.5), f_sub, p_pump, p_trit, p_house, p_cryo mapped directly (p_pump direct since WI-019; see item 9). p_coils→p_tf (p_pf=0), p_cool→p_tfcool (p_pfcool=0).

## Footnotes

- **C220107 power supplies is ARIES-CS-derived.** It is INCLUDED here (this handshake is not the hold-out blind), and matches to the float32 floor when fed 1cfe power. It must be excluded/footnoted in the later ARIES-CS hold-out comparison. No ARIES-CS source was read; only 1costingFE's computed value (81.40 M$) is used.
- No barred hold-out paths were read.
