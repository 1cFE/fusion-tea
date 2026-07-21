---
Status: draft
Created: 2026-07-20
Updated: 2026-07-20
Related Artifacts:
  Spec: ./spec.md
  Brief: ../../orchestration/handshake-lcoe-construction.md
  Upstream: ../../completed/20260720_WI-028_handshake-account-scope/design.md
---

# WI-029 Design — Handshake LCOE construction: CAS70/80 + IDC

## Overview

WI-028 brought the model's overnight/total-capital assembly under the 1costingFE handshake and ruled CAS60 a reported Option-C line. What is still missing is the annual-cost side of LCOE. This design forward-computes it:

- **CAS71** (levelized O&M) — the WI-025 unlevelized annual O&M run through 1cfe's growing-annuity levelization. Flat-Real arithmetic → codegen.
- **CAS72** (levelized scheduled replacement of first-wall/blanket + divertor) — the larger half of CAS70 ($82.23M), absent from the model today. Its closed form is flat-Real **except one `ceil`**, so it lands on the WI-022 handwritten rung (manual_required + oracle mirror), forward-computed and under the A-2 bar.
- **CAS80** (levelized DT fuel) — small ($0.769M), flat-Real → codegen, reusing the CAS71 levelization wrapper.
- **CAS90 / IDC** — the model and 1cfe fold construction-period financing into the annual capital charge with **different multipliers** (model 1.310796 vs 1cfe 1.282476). Aligning the end-to-end LCOE is a **genuine convention choice**, not mechanical fall-out — a reserved gate parked for owner (Align ruling 3), with options and a recommendation below.
- **CAS10** — the pre-existing +$16.0M/+86.5% divergence resolves to **one clean error** (FOAK studies 20.0 frozen where the handshake runs NOAK 4.0); the bounded fix reconstructs 1cfe's 18.5 with zero residual. The owner stop condition does not fire.

The deliverable is the **criterion-3 verdict in the A-4 form** — every modeled account under A-2, the remainder itemized with signed magnitudes, the residual LCOE gap reconciling to that sum.

**One gate is open** (IDC/CAS90 convention). All IDC-independent design is complete; the gate is presented as a question in the final message, per the non-interactive protocol.

---

## Independent formula re-derivation (pin `0254385`)

Every 1cfe formula was re-read from source under `/home/reid/1cfe/1costingfe/src/costingfe/` (not the repo-root paths the spec cites shorthand) and reproduced by **importing and calling the actual functions** with the handshake point's inputs — the strongest check. Git HEAD is exactly `0254385`, clean tree. Every headline number in `onecfe_point.json` reproduces to float32 precision.

Handshake point: p_net 1000.0, availability **0.9**, n_mod 1, lifetime 30, construction_time 8, interest 0.07, inflation 0.02, `noak=true`, DT.

| Output | Formula (source) | Re-derived | 1cfe emitted | Match |
|---|---|---|---|---|
| CAS71 | `levelized_annual_cost(annual_om, i, g, n, Tc)` (`economics.py:13-50`) | 79.00363 | 79.00362 | ✓ (Δ 8e-6) |
| CAS72 | `levelized_replacement_cost(event, t_cal, i, n)` (`economics.py:53-75`) | 82.23002 | 82.22999 | ✓ (Δ 3e-5) |
| CAS70 | CAS71 + CAS72 | 161.23365 | 161.23361 | ✓ |
| CAS80 | `cas80_fuel(...)` DT branch (`costs.py:476-544`) | 0.76907 | 0.76907 | ✓ |
| CAS90 | `CRF(0.07,30) · total_capital` (`costs.py:547-556`) | 813.58727 | 813.58728 | ✓ |
| LCOE | `(cas90+cas70+cas80)·1e6/(8760·p_net·n_mod·avail)` (`economics.py:88-92`) | 123.74301 | 123.74301 | ✓ |

### CAS71 chain (the two findings)

`annual_om = om_cost_dt(54.9) · (p_net·n_mod/1000)^0.5`. Then `levelized_annual_cost`: `A1 = annual_om·(1+g)^Tc`; `PV = A1·(1−((1+g)/(1+i))^n)/(i−g)`; `cas71 = CRF(i,n)·PV`. At i=0.07, g=0.02, n=30, **Tc=8**:

- **Tc is 8 at NOAK.** `_total_project_time` (`costs.py:41-44`) adds `licensing_time(fuel)` **only when not NOAK**. NOAK → construction_time = 8; FOAK → 8 + 2 (DT licensing) = 10. Both handshake and design points are NOAK, so Tc=8 at both.

**FINDING D1-a — the "1.5043 levelization factor" claim is REFUTED. The true factor is 1.439.** The levelization is point-independent: `cas71 = annual_om · (1+g)^Tc · [(1−((1+g)/(1+i))^n)/(i−g)] · CRF`, and the bracket-plus-`(1+g)^Tc`-plus-CRF multiplier is a constant (1.02^8 × annuity/CRF ratio = **1.43905**) given i,g,n,Tc — it does not depend on `annual_om`. The spec's 1.5043 = 79.004 / 52.517 divided the **handshake-point** cas71 (annual_om at p_net=1000 → 54.900) by the **design-point** annual_om (p_net=915.08 → 52.517). It mixes two operating points and is meaningless. The correct handshake-point factor is 79.004 / **54.900** = 1.439.

**FINDING D1-b — annual_om at the handshake point is 54.900, not 52.517.** `onecfe_point.json` itself records `annual_om_unlevelized_musd: 54.900`. The 52.517 figure is the **design-point** value (p_net=915.08). This is the duty-7 trap in miniature: `annual_om` is p_net-dependent, so the handshake and design points carry different bases through the same 1.439 factor. Neither number is wrong; the spec attached the design-point base to the handshake-point cas71.

### CAS72 chain (full, since it drives the rung decision)

- `q_n = p_neutron/firstwall_area = 2065.065/660.079 = 3.12851` MW/m²
- `fluence_limit_dt = 18.0` (`defaults.py:291`); raw FPY = 18.0/3.12851 = **5.75354**
- `core_lifetime_FPY = clip(5.75354, 0.5, n·avail=27.0)` → **clip inert** (5.75 sits well inside), FPY = 5.75354
- `core_lifetime_cal = FPY/availability = 5.75354/0.9 = 6.39282` cal-yr  ← **availability enters here**
- `cost_per_event = (C220101 570.420 + C220108 100.741)·n_mod = 671.160` M$ (`defaults.py:299` replaceable = C220101, C220108)
- `s = (1+i)^(−t) = 1.07^(−6.39282) = 0.64887`; `n/t = 4.69277`, `ceil = 5`, **`n_rep = max(0, 5−1) = 4`**
- `pv = event·s·(1−s^n_rep)/(1−s) = 1020.396`; `cas72 = CRF·pv = 82.230` ✓
- DEC-grid/cap-bank/electrode/laser replacement terms are structural zero (steady-state RANKINE DT stellarator, p_dee=0).

### CAS80 chain

- `cost_per_rxn = M_D_KG·u_deuterium + M_Li6_KG·u_li6 = 3.34358e-27·2175 + 9.98835e-27·1000 = 1.72606e-23` $/rxn; `q_eff = Q_DT = 17.58` MeV
- `annual_raw = n_mod·p_fus·(3600·8760)·avail·cost_per_rxn/(q_eff·MEV_TO_JOULES) = 0.44910` M$/yr
- burn correction `×(1 + (1−burn)/burn·(1−recovery))` with burn=0.05, recovery=0.99 → **×1.19** → 0.53443; target-consumable term = 0 (MFE)
- levelized (same wrapper, Tc=8) → **cas80 = 0.769** ✓

---

## CAS72 codegen-envelope ruling (MR-WI029-2)

**The codegen allow-list is exactly `+ − * / **` (and `^`→`**`).** One dict in `sysml-codegen` — `calc_compat_renderer.py:39-46` `_ARITHMETIC_OPERATOR_MAP` — is the whole numeric dialect, plus unary `±` (`:118-122`). `**` operands may be arbitrary sub-expressions (why the variable exponent `(1+d)**(Yc/2)` codegens). **Any function call** — `ceil`, `floor`, `max`, `min`, `clip`, `sqrt`, `exp` — is an `InvocationNode` and hard-fails at `:76` (`unsupported node: invocation`), caught upstream and routed to `MANUAL_REQUIRED` (`expression_compiler.py:108,255-311`). There is no conditional/`where` node and no comparison operator. (These four lowering files are byte-identical between pin `06d95f8` and current HEAD, so what HEAD shows is what the pin lowers.)

**Per-piece rung assignment.** The CAS72 chain is flat-Real everywhere except one operation:

| Piece | Operation | Envelope? | Rung |
|---|---|---|---|
| `q_n = p_neutron / firstwall_area` | `/` | yes | A (codegen) |
| `core_lifetime_FPY = clip(fluence/q_n, 0.5, n·avail)` | `clip` **inert here** → `fluence/q_n` | yes (clip dropped as documented no-op) | A |
| `core_lifetime_cal = FPY / availability` | `/` | yes | A |
| `s = (1+i)^(−t)` | `**` variable real exponent | yes (proven `idc_factor` pattern) | A |
| `n_rep = max(0, ceil(n/t) − 1)` | `max` inert; **`ceil` live, not expressible** | **NO** | **B (handwritten)** |
| `pv`, `cas72 = CRF·pv` | `+ − * / **` | yes (given n_rep) | rides n_rep's rung |

**Only `ceil` breaks the envelope.** `clip`, both `max`s, and the inner `max(q_n,1e-6)` guard are all inert at the handshake point (numbers above). Risk 1's "ceil/clip/where/max" over-states the blocker set — `where` is in CAS71's `compute_om`, not CAS72; the real CAS72 blocker is `ceil` alone.

**Ruling: CAS72 → the WI-022 handwritten rung (Rung B), forward-computed and under A-2.** The `ceil` in `n_rep` forces the account onto the manual rung, but the account is fully computable, worth $82.23M / ≈10.4 $/MWh, and the handwritten-rung mechanism is established and honest:

- A calc def `'Levelized Replacement Cost'` (library) declares the closed form; the non-envelope `ceil` routes it to `MANUAL_REQUIRED` (WI-022 precedent: `'DT Fusion Power'` did this with `sqrt`/`exp`).
- Codegen emits a stub; a handwritten `..._impl.py` fills the exact Python closed form (doing the `ceil`), preserved across regen by `preserve_handwritten=True` (`cli/__init__.py:91,478`).
- An **oracle mirror** in `verify_stellaris.py` recomputes cas72 a second way; `run_stellaris.py` asserts the handwritten impl agrees bit-exact at rel 1e-9. This is what keeps the rung honest — it cannot drift silently.

**Do NOT freeze `n_rep` as a defaulted input.** It is a discontinuous step function of the live neutron/geometry chain: n/t = 4.693 here, and a ~10% move in neutron power or first-wall area flips n_rep to 3 or 5. Freezing it hides a real dependency that would fail **silently and discontinuously** if inputs move — the worst failure mode, and it collides with the project's no-fallbacks rule. The handwritten rung computes n_rep live every run, so it stays correct as the point moves.

**Rejected alternative — itemize CAS72 as a signed A-4 remainder** (MR-WI029-2's "or"). Legitimate under the criterion-3 ruling ("the bar is explaining"), and the honest last resort. Rejected because CAS72 *is* computable via the established rung; carrying the largest single account ($82M) as an unexplained remainder when the toolkit can compute it is strictly worse for the A-4 verdict. This stays a recorded decision, not an instruction.

**Clip caveat (surfaced, not silent).** Dropping `clip` from `core_lifetime_FPY` is valid **only because it is inert at this pinned point**. The floor (0.5) keeps the 1/q_n gradient finite; the cap (n·avail) stops replacement beyond plant life — both are real guards the envelope cannot express. Recorded as a documented no-op tied to this operating point; re-verify inertness if wall loading or lifetime move (per the premise-conflict rule). At the design point (avail 0.85, p_net 915) FPY is still well inside the bounds — re-checked, inert there too.

---

## CAS10 root-cause ruling (MR-WI029-6, owner stop condition)

**Ruling: CLEAN SINGLE ERROR. The stop condition does not fire.** The divergence resolves to one mis-set binding under an unambiguous basis, and the fix reconstructs 1cfe's 18.5 with **zero residual**.

**1cfe side** (`costs.py:52-80`, `defaults.py`): `CAS10 = (land + site_permits + licensing + plant_permits + studies + plant_reports + other_precon)·(1+contingency_rate)`. At the NOAK handshake point: land = 0.25·√(1000·1·1000)·10000/1e6 = **2.5**; adders = 3 + 5(DT) + 2 + **4(studies_noak)** + 1 + 1 = 16.0; contingency_rate_noak = **0.0**. CAS10 = 18.5·1.0 = **18.5**. Only `plant_studies` (foak 20 / noak 4) and `contingency_rate` (foak 0.10 / noak 0.0) are FOAK/NOAK-sensitive.

**Model side**: `'Preconstruction Cost'` (`mfe_account_costs.sysml:356-386`) = `land_intensity·(p_net·n_mod·ref)^0.5·land_cost + fixed_precon`; instance `precon_fixed_base = 32000000.0` (`stellarator_plant.sysml:631`), documented as `... + plant_studies_foak 20 (FOAK frozen) + ...`. So model CAS10 = land 2.5 + fixed 32.0 = **34.5**. The model applies no CAS10 contingency (deferred to CAS29, which is 0 at NOAK — already correct).

**Reconstruction test (decisive)**: change only `precon_fixed_base` 32.0 → 16.0 (studies 20→4) → CAS10 = 2.5 + 16.0 = **18.5, residual 0.0**.

**Why it is one error, not two.** Contingency is **0.0 on both sides** at NOAK — 1cfe (`contingency_rate_noak=0`) and the model (defers to CAS29=0). The model's contingency handling is already NOAK-correct; nothing is mis-set there. Of the two FOAK/NOAK-sensitive constants, only `plant_studies` is actually wrong in the numbers. The WI-025 "CAS10 = subtotal × 1.10 exactly" note (`mfe_account_costs.sysml:364`) is a stale FOAK doc note contributing zero residual — a documentation tail of the same single regime confusion, not an independent cause. The basis is unambiguous: one account was left at FOAK while every sibling runs NOAK.

**Bounded fix (both trees, D2b):** `precon_fixed_base` 32000000.0 → 16000000.0 in `models/designs/stellarator_09/stellarator_plant.sysml:631` **and** the staged twin; amend the FOAK doc notes there and at `mfe_account_costs.sysml:364` (+ twin `models/analyses/...:364`) to NOAK — documentation hygiene sweeping the same correction, changing no number. Recapture snapshot from the staged tree.

**Design-point consequence (a finding against MR-WI029-9):** `precon_fixed_base` is power-independent, so this fix reduces `overnight_capital = total_capital` by exactly **$16M at the design point too** (fixed adders don't scale with p_net; only the land term does). The spec's "total_capital stays $16.146B (Option C stands)" is *almost* right — Option C leaves the assembly *shape* unchanged, but the in-scope CAS10 correction lowers the number by $16M to ≈$16,129.7M. Small (0.1%) but real; recorded so the re-baseline is honest, not asserted-unchanged.

---

## IDC / LCOE reconciliation — RESERVED GATE (MR-WI029-4, Align ruling 3)

**Ruling: genuine convention choice, not mechanical fall-out. Parked for owner with options.** This mirrors WI-028's D4 finding (CAS60 was also ruled a genuine choice), and the reason is the same: the two sides fold construction-period financing into the annual capital charge with **different multipliers**, and Option C deliberately left the model's `idc_factor` untouched.

- **1cfe:** `total_capital = overnight + CAS60`, `CAS60 = f_idc·overnight`, `f_idc = ((1+i)^T−1)/(i·T)−1` (uniform-spend closed form) → IDC multiplier **1.282476**; `CAS90 = CRF·total_capital = 813.587`.
- **model:** `annual_capital = overnight · (1+d)^(Yc/2) · CRF` (even-spend midpoint) → IDC multiplier **1.310796**; the model's DCF LCOE keeps this (`mfe_lcoe_dcf.sysml:47-52`).

The multipliers differ by **+2.208%** on the capital charge (model DCF-equivalent CAS90 = 831.553 vs 1cfe 813.587) → ≈+1.8% on LCOE. This is not a mechanical consequence of the Option-C mapping — it is a real convention difference, and adopting 1cfe's form would change the model's own headline LCOE. **→ reserved gate.** The options and my recommendation are in the final message; the design below is built to satisfy either option (CAS71/72/80 are IDC-independent; only the CAS90/LCOE channel wiring depends on the pick).

---

## Design-point vs handshake-point (duty 7)

The handshake overrides the design-point instance bindings with the 1cfe point (injection map, `handshake_1costingfe.py:296` injects availability; power block drives p_net to 1000). So constants differ by point, and the bindings carry the difference:

| Constant | Design point (Stellaris instance) | Handshake point (injected) | What it moves |
|---|---|---|---|
| availability | 0.85 (`stellarator_plant.sysml:742`) | 0.9 (injected `:296`) | CAS72 (`core_lifetime_cal`), LCOE denominator |
| p_net | 915.08 (solved) | 1000.0 (injected) | annual_om base (52.517 vs 54.900), CAS72 `cost_per_event`, CAS80 |
| inflation_rate | 0.02 (NEW instance input) | 0.02 (injected, same) | CAS71/CAS80 levelization |
| Tc / regime | NOAK, Tc=8 | NOAK, Tc=8 | levelization factor (1.439, same both points) |
| plant_studies | 4 (NOAK, after CAS10 fix) | 4 (NOAK) | CAS10 (same both points) |

**The design point is NOAK, not FOAK.** Evidence: CAS29 contingency = 0 at the executed design point (WI-028). If it were FOAK, contingency would be 0.10 and Tc=10 (licensing_time added), changing the levelization factor to 1.02^10×ratio. Both points are NOAK, so the levelization factor (1.439), inflation_rate (0.02), and studies (4) are identical at both; only availability and p_net differ, and both flow through calc-def inputs. **CAS72 at the two points: 82.230 (handshake, avail 0.9) vs ≈78.2 (design, avail 0.85)** — the availability swing on `core_lifetime_cal` is real and carried correctly by the input. `n_rep = 4` at both points (checked), computed live in the handwritten rung.

*If the owner intends Stellaris as a genuine FOAK plant*, that is a separate, broader change — every FOAK constant would flip (studies 20, contingency 0.10, Tc=10, licensing), not just CAS10. Out of scope here; flagged. This item takes the design point as NOAK, consistent with WI-028.

---

## Proposed design

### D1 — Calc defs (`models/library/analyses/mfe_account_costs.sysml` + staged twin `models/analyses/...`)

Three new concept-agnostic defs. Two are flat-Real (Rung A, codegen); one is the handwritten rung (Rung B). Parse-validated (Validation Report).

| Calc def | Rung | Serves | Key inputs |
|---|---|---|---|
| `'Levelized Annual Cost'` | A (codegen) | **CAS71 and CAS80** (shared) | annual_cost, interest_rate, inflation_rate, operational_years, project_time → growing-annuity PV × CRF |
| `'DT Fuel Cost'` | A (codegen) | CAS80 raw annual | p_fus, n_mod, availability, cost_per_rxn, q_eff, mev_to_joules, burn_fraction, fuel_recovery |
| `'Levelized Replacement Cost'` | **B (handwritten)** | CAS72 | cost_per_event, core_lifetime_cal (or FPY inputs), interest_rate, operational_years |

- **`'Levelized Annual Cost'`** reproduces `levelized_annual_cost` (`economics.py:13-50`): `disc_pow_n=(1+i)^n`; `crf=i·disc_pow_n/(disc_pow_n−1)`; `a1=annual_cost·(1+g)^Tc`; `pv=a1·(1−((1+g)/(1+i))^n)/(i−g)`; `levelized=crf·pv`. Used **twice** — once with `annual_cost = om_cost.annual_om` (→ CAS71), once with `annual_cost = fuel_cost.annual_fuel` (→ CAS80). One def, two usages (MR-3 concept-agnostic).
- **`'DT Fuel Cost'`** reproduces the DT branch of `cas80_fuel` (`costs.py:476-544`): `annual_raw = n_mod·p_fus·(3600·8760)·avail·cost_per_rxn/(q_eff·mev_to_joules)`; `annual_fuel = annual_raw·(1+(1−burn)/burn·(1−recovery))`. Fuel constants are instance inputs (MR-3/MR-4).
- **`'Levelized Replacement Cost'`** reproduces `levelized_replacement_cost` + `_core_lifetime_fpy` (`economics.py:53-75`, `model.py:102-111`). Its body carries the `ceil` (via a standard-library invocation, following WI-022's non-envelope-function pattern), so codegen routes it to `MANUAL_REQUIRED`; the handwritten impl computes the full chain (q_n, FPY with the inert clip documented, cal, s, n_rep via `ceil`, pv, cas72) and the oracle mirror asserts it at rel 1e-9. The flat-Real pre-chain (q_n, cal) *could* be split into a codegen def feeding the handwritten `n_rep`/pv step, but keeping the whole account in one manual function keeps the `ceil` and its oracle mirror together and is simpler to verify — recommended.

### D2 — LCOE-side wiring (`mfe_plant.sysml` generic + instance, both trees)

Today `mfe_plant.sysml:571` binds `annual_om = om_cost.annual_om` (unlevelized) straight into `'LCOE DCF'`. New wiring:

```
cas71_calc : 'Levelized Annual Cost'   ( annual_cost = om_cost.annual_om, i, g, n, Tc )   -> cas71
fuel_calc  : 'DT Fuel Cost'            ( p_fus, avail, fuel consts )                       -> annual_fuel
cas80_calc : 'Levelized Annual Cost'   ( annual_cost = fuel_calc.annual_fuel, i, g, n, Tc )-> cas80
cas72_calc : 'Levelized Replacement Cost' ( cost_per_event, FPY inputs, i, n )             -> cas72   [handwritten]
cas70      = cas71 + cas72
```

`cost_per_event` for CAS72 sums the modeled replaceable accounts C220101 (blanket, `mfe_account_costs`) + C220108 (divertor) × n_mod — both are already modeled (WI-028 cas22 tail / core). The LCOE assembly then depends on the ruled IDC option:

- **Option (ii) — mapped comparison (recommended):** model headline LCOE keeps its DCF `idc_factor` untouched (Option C stands); a separate **1cfe-form CAS90 channel** = `CRF·(overnight + CAS60)` reuses WI-028's already-reported `'IDC Closed-Form Cost'` (CAS60) line; the handshake compares a 1cfe-form LCOE `= (cas90_1cfe + cas70 + cas80)·1e6/(8760·p_net·avail)` at the handshake point. Two LCOE channels: one headline (DCF), one comparison (1cfe-form). No model headline-convention change.
- **Option (i) — adopt 1cfe form:** the model drops `idc_factor`, sets `total_capital = overnight + CAS60`, `CAS90 = CRF·total_capital`; the model's own headline LCOE convention changes. Single channel.

Both are IDC-independent for CAS71/72/80; only the CAS90/LCOE tail differs. The design is complete for CAS71/72/80/CAS10 regardless; the CAS90/LCOE tail is one small wiring block selected by the gate.

### D2b — Staged-twin propagation (D2b inherited, binding)

Every `.sysml` edit lands **region-identical in both trees**: canonical `models/library/analyses/...`, `models/designs/.../*.sysml` and the staged twin `exploration/stellarator_e2e/models/analyses/...`, `.../models/designs/.../*.sysml` (note: staged path drops the `library/` segment). Codegen reads the **staged** snapshot, not canonical. Reconcile the twin's Item-10 / DEMO-NOTE lines (don't blind-overwrite); run the staged-vs-canonical mirroring diff gate (only intended WI-029 edits + known divergences); recapture `stellarator.snapshot.json` from the staged tree before any codegen/exec. A canonical-only edit is a silent wrong result.

### D3 — Handshake harness (`emit_1cfe_point.py`, `handshake_1costingfe.py`)

The emitter already solves the point **with inflation** and already emits `cas70/cas71/cas72/cas80/cas90` in `costs_musd` — the oracle values exist; they are simply not yet compared. Additions:

- **`emit_1cfe_point.py` `refs`:** add `inflation_rate` (0.02, currently only in `target`), the DT fuel constants (`cost_per_rxn` or its components `M_D_KG·u_deuterium`, `M_Li6_KG·u_li6`, `q_eff=Q_DT`, `MEV_TO_JOULES`, `burn_fraction`, `fuel_recovery`), and the CAS72 replacement params (`fluence_limit_dt`, replaceable-account ids) — each `float(cc.<attr>)` so the handshake both feeds them (×conversions) and asserts them against 1cfe config (A-5).
- **`handshake_1costingfe.py`:** add `CH` channels for `cas71`, `cas72`, `cas80` (and the 1cfe-form `cas90`/`lcoe` per gate); `lcoe` channel already exists. Add the injected inputs (`inflation_rate`, fuel constants) to the `set_1cfe_inputs` update blocks (same `f"{P}<module>__<input>"` pattern as availability at `:296`). Add A-2 comparison rows for cas71/cas72/cas80/cas90/lcoe. **Comparison logic untouched** — `rel(a,b)` and the row-loop machinery are generic (`:410-516`); only new rows + inputs.

### D4 — Trap assertions (A-5, MR-WI029-8)

Every new mapping asserted in the handshake trap table (`trap(name, ok, detail)` at `:577`):

1. **Levelization params:** g = inflation_rate = 0.02; Tc = construction_years = 8 (NOAK, not 10); i = interest_rate = 0.07; n = operational_years = 30. Assert the 1.439 factor materializes (cas71/annual_om at the handshake point).
2. **CAS72 replacement chain:** replaceable set = {C220101, C220108}; fluence_limit_dt = 18.0; q_n from modeled p_neutron/firstwall_area; **n_rep = 4** (assert the handwritten rung's computed integer); clip inert (assert FPY ∈ [0.5, n·avail]).
3. **Fuel constants:** cost_per_rxn = M_D·u_D + M_Li6·u_Li6; q_eff = Q_DT = 17.58; burn correction ×1.19; assert each against `cc`.
4. **Availability injection:** assert 0.9 (handshake) is injected over the model's 0.85 into CAS72 and the LCOE denominator — the duty-7 trap made explicit.
5. **IDC (per gate):** if Option (ii), assert `cas90_1cfe = CRF·(overnight+CAS60)` and that the model headline `idc_factor` is unchanged (guards double-count).

### D5 — CAS10 bounded fix

Per the CAS10 ruling: `precon_fixed_base` 32000000.0 → 16000000.0 (both trees), doc amendments to NOAK. Recorded as **closed-as-error with clean reconstruction** (residual 0.0) in the verdict.

### D6 — Criterion-3 verdict artifact (A-4 form)

Extend `HANDSHAKE_REPORT.md` (currently stale, dated Jul 18 / pre-WI-028 numbers — re-baseline it) or a named successor, referenced from epic Item 4 / criterion 3. It contains:

1. **Per-account A-2 pass table:** every modeled account (WI-025/WI-028 set + CAS71 + CAS80 + **CAS72 forward-computed** + CAS90 per gate) with |rel dev| vs 1cfe float32 and pass/fail at 1e-6.
2. **Signed-magnitude remainder itemization:** each non-bar account with 1cfe value, model value (or "structurally absent"), signed dollar gap, one-line reason. After this item the standing remainders are **C220106_pump $0.721M** (explained, shell-only vessel calc) and the **total_capital/CAS90 convention line** (per the IDC gate); **CAS10 closes as error**; **CAS72 leaves the remainder** (now forward-computed).
3. **Reconciliation arithmetic:** the residual end-to-end LCOE gap = the itemized-remainder sum within ≤1e-6 relative to LCOE — shown, not asserted.
4. **Verdict:** met or honestly failed.

---

## Cross-file bindings

| Binding | Source | Consumer |
|---|---|---|
| `inflation_rate` (NEW instance input, 0.02) | `stellarator_plant.sysml` + twin | `'Levelized Annual Cost'` g (CAS71, CAS80) |
| `om_cost.annual_om` | `mfe_plant.sysml:571` (existing) | CAS71 `annual_cost` |
| `fuel_calc.annual_fuel` | new `'DT Fuel Cost'` usage | CAS80 `annual_cost` |
| DT fuel constants (NEW instance inputs) | `stellarator_plant.sysml` + twin, MR-4 cited | `'DT Fuel Cost'` |
| `cost_per_event` = C220101 + C220108 (×n_mod) | modeled cas22 accounts | CAS72 `cost_per_event` |
| p_neutron, firstwall_area, fluence_limit_dt | modeled physics + NEW input | CAS72 core-lifetime chain |
| availability | instance 0.85 / injected 0.9 (`:296`) | CAS72 `core_lifetime_cal`, LCOE denom |
| overnight_capital, CAS60 line | WI-028 assembly (existing) | 1cfe-form CAS90 channel (Option ii) |
| whole D1/D2/D5 edit set | canonical **AND** staged twin (D2b) | snapshot recapture → codegen |

Dataflow unidirectional: physics/powers → fuel/replacement/O&M → levelization → cas70/80 → LCOE. No cycles. The handwritten CAS72 rung is a leaf producer (reads modeled inputs, writes cas72).

---

## Toolchain pins (verified live this stage — DRIFT on three of four)

| Tool | Pin | Live HEAD | Pin reachable | Ancestor of HEAD | Status |
|---|---|---|---|---|---|
| 1costingFE | `0254385` | `0254385` | ✓ | ✓ (HEAD==pin) | on pin |
| sysml-codegen | `06d95f8` | `936315c` | ✓ (object) | **NOT** | **drifted** |
| teax | `07eb0ac` | `fa0e06a` | ✓ (object) | **NOT** | **drifted** |
| agentic-mbse | `4c18d61` | `f4ebdce` | ✓ (object) | **NOT** | **drifted** |

Three repos have HEAD moved off a line where the pin is not in history; all pins remain reachable as objects. **`git worktree list` on sysml-codegen shows six worktrees — none at `06d95f8`** (main at `936315c`; others at `512786c`/`6db3212`). This is the exact off-pin drift WI-028 caught mid-run. **Plan/implement must create/checkout a worktree at each pin before any codegen/exec step**, per A-6; adopting the newer HEADs is an owner-visible decision, never a side effect. The lowering files are byte-identical `06d95f8`↔HEAD (verified), so codegen behavior is unchanged for this item — but the pin discipline still binds.

This item's pins: **sysml-codegen `06d95f8`, teax `07eb0ac`, agentic-mbse `4c18d61`, 1costingFE `0254385`**.

---

## Validation plan

1. **Parse (L1-3):** new calc defs + restructured plant parse clean. Flat-Real defs **DONE this stage** (Report). The handwritten-rung def parses (WI-022 precedent).
2. **Codegen capture (first plan checkpoint):** at the pins (worktree checkout), after the D2b twin edit + mirroring diff gate, recapture `stellarator.snapshot.json` from the staged tree; `sysml-codegen generate --from-snapshot`; confirm the two flat-Real defs lower and the CAS72 def routes to `MANUAL_REQUIRED` with a stub; fill the handwritten impl; confirm `preserve_handwritten` keeps it across regen.
3. **A-2 per-account (SV-035):** cas71, cas72, cas80 (+ cas90 per gate) under |rel dev| ≤ 1e-6 vs 1cfe float32 at the handshake point. CAS72's handwritten impl matches its oracle mirror at rel 1e-9.
4. **CAS10 closure:** model CAS10 → 18.5 exactly (residual 0) at the handshake point.
5. **Design-point re-baseline (MR-WI029-9):** record the new Stellaris headline — LCOE moves up (levelized O&M + CAS72 + CAS80 enter); total_capital moves down $16M (CAS10 fix); oracle bit-exact rel 1e-9 at the new point.
6. **G-8 re-baseline:** `handshake_comparison.json` gains the new rows, re-baselined as an explicit commit; comparison logic untouched.
7. **Standing bars:** oracle rel 1e-9; WI-022 sha256 `8d2357…794a9f` survives regen (now joined by the CAS72 impl's sha); IFE A/B byte-exact; pytest 11/18/14/0; L1=0; PROTOCOL sealed.

---

## Validation report (design stage)

- **Parse:** `prototype/wi029_lcoe_construction.sysml` — `'Levelized Annual Cost'` + `'DT Fuel Cost'` (the two flat-Real Rung-A defs) → **Checks passed!** (license sourced from `~/1cfe/fusion-tea/.env`).
- **Assembly reproduction:** all six 1cfe outputs (cas71/72/70/80/90/lcoe) re-derived independently by calling the pinned functions and matched to `onecfe_point.json` to float32 precision (re-derivation section).
- **CAS72 envelope:** codegen allow-list confirmed `+ − * / **` only (`calc_compat_renderer.py:39-46`); only `ceil` breaks it; clip/max inert at the point (numbers shown). Handwritten-rung mechanism confirmed against the WI-022 close (`preserve_handwritten`, oracle mirror).
- **CAS10:** reconstruction test residual 0.0 (studies 20→4).
- **Codegen capture:** NOT run this stage (requires full-plant snapshot+generate at the pins — a plan activity). Scheduled as Validation Plan step 2. Not fabricated.
- **Prototype status:** PASS (parse + assembly reproduction); codegen + handwritten-rung fill PENDING (plan step 2).

---

## Implementation checklist (for `/plan-model`)

**Every `.sysml` edit lands region-identical in BOTH trees (D2b). The staged tree is what the snapshot recapture reads.**

1. **Library (both trees):** add `'Levelized Annual Cost'`, `'DT Fuel Cost'`, `'Levelized Replacement Cost'` to `mfe_account_costs.sysml` + twin (`models/analyses/...`).
2. **Generic plant (both trees):** wire cas71_calc / fuel_calc / cas80_calc / cas72_calc into `mfe_plant.sysml`; `cas70 = cas71+cas72`; LCOE tail per the ruled IDC option.
3. **Instance (both trees):** bind `inflation_rate` (0.02), DT fuel constants, `fluence_limit_dt` in `stellarator_plant.sysml`, MR-4 cited; **CAS10 fix** `precon_fixed_base` 32M→16M + doc amendments.
4. **Pins + mirroring diff gate + recapture:** checkout worktrees at the four pins; staged-vs-canonical diff clean; recapture snapshot from staged tree; codegen-capture checkpoint (flat-Real lower; CAS72 → MANUAL_REQUIRED); fill + oracle-mirror the CAS72 handwritten impl.
5. **Harness:** `emit_1cfe_point.py` refs; `handshake_1costingfe.py` channels + injected inputs + rows + traps (D3/D4).
6. **Re-baseline & validate:** SV-035; `handshake_comparison.json` explicit re-baseline commit; design-point headline recorded; oracle bit-exact; verdict artifact (D6) in A-4 form with reconciliation arithmetic shown.

---

## Risks

1. **[medium] CAS72 handwritten rung fill + oracle mirror.** The `ceil` forces the manual rung; the impl must reproduce the closed form exactly and the oracle mirror must match at 1e-9. Mitigation: WI-022 precedent is the exact pattern; the full numeric chain is re-derived here to check against.
2. **[medium] IDC gate blocks the end-to-end verdict.** If the owner defers, the CAS90/LCOE row waits on the ruling. Mitigation: CAS71/72/80/CAS10 are IDC-independent and complete now; only the CAS90/LCOE tail is gated. Recommend Option (ii) (mapped comparison) — reuses Option C's CAS60 line, no headline-convention change, lowest risk.
3. **[high, inherited] Staged-twin skip.** Canonical-only edits → silent wrong result. Mitigation: D2b both-trees + mirroring diff gate + recapture from staged tree.
4. **[medium] Pin drift.** Three repos are off-pin with no worktree at the pin. Mitigation: explicit worktree checkout at the pins before codegen/exec (A-6); lowering files verified byte-identical to HEAD.
5. **[low] n_rep step-function at the design point.** Computed live in the handwritten rung (n_rep=4 at both points, checked); never frozen. Mitigation: oracle mirror recomputes each run.
6. **[low] CAS10 fix moves total_capital by $16M** (finding vs MR-WI029-9's "unchanged"). Mitigation: recorded in the re-baseline; oracle bit-exact bar catches any arithmetic error at the new point.

---

## Traceability

- **1cfe formulas (pin `0254385`, under `src/costingfe/`):** `layers/economics.py:6-92`, `layers/costs.py:41-80,319-556`, `model.py:102-112,1483-1605`, `defaults.py` (fuel consts, plant_studies, contingency, fluence_limit, replaceable_accounts:299).
- **Codegen envelope:** `sysml-codegen` `calc_compat_renderer.py:39-46,76,115`; `expression_compiler.py:108,255-311`; `cli/__init__.py:91,478` (preserve_handwritten). WI-022 close: `work/completed/20260718_WI-022_predictive-confinement/design.md`.
- **Model (canonical + staged twin, D2b):** `models/library/analyses/{mfe_account_costs,mfe_lcoe_dcf}.sysml`, `models/designs/{generic_mfe/mfe_plant,stellarator_09/stellarator_plant}.sysml` + `exploration/stellarator_e2e/models/...` twins; snapshot `.../stellarator.snapshot.json`.
- **Harness:** `exploration/stellarator_e2e/{emit_1cfe_point.py:296, handshake_1costingfe.py:410-616, handshake_comparison.json@feb13ff3, onecfe_point.json, HANDSHAKE_REPORT.md, verify_stellaris.py, run_stellaris.py}`.
- **Requirements:** MR-WI029-1..11; anchor A-2/A-3/A-4/A-5/A-6 + G-8; MR-3, MR-4; Align rulings 1–5.
- **Prototype:** `prototype/wi029_lcoe_construction.sysml`.
