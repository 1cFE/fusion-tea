---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-14
Updated: '2026-07-14'
---

# WI-019: Faithful MFE Power Balance

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — this is a stellarator-demo model-development item. The ARIES-CS hold-out is sealed; the §3 barred paths must not be read. Admissible sources for this item: 1costingFE (pinned `0254385`) for all physics/engineering formulas, plus the existing WI-009/010/018 models.

## Overview

Fix the thermal-power formula in `'MFE Power Balance Calc'` so it recovers the charged-particle (alpha) power, matching 1costingFE's forward power balance. Today the calc drops ~19% of thermal power (547 MW at the handshake point), which shrinks every power-scaled cost account by 8–16% and net electric — the LCOE denominator — by 23.5%. This is item 3 of the demo-deepening plan (handoff 2026-07-14), ranked first: independent of the other items and the single highest-leverage fix identified by the Anchor A handshake.

## Goals & Context

**Research questions served**:
- RQ-2 (credible LCOE range): net electric power is the LCOE denominator; the current balance understates it by 23.5% at the handshake point.
- RQ-1 (dominant cost drivers): every power-scaled account (blanket, shield, divertor, structure, vessel, power supplies, all four BOP accounts) scales with `p_th`/`p_et`; a −16.4% power error distorts the cost-driver picture.

**Demo context**: The stellarator MBSE demo (`.project/concepts/stellarator-mbse-demo.md`) Stage-3 backlog ranks this fix first (`.project/CURRENT_WORK.md`, "Stage-3 backlog"). The Anchor A handshake (`exploration/stellarator_e2e/HANDSHAKE_REPORT.md`) isolated it as the single root cause of the end-to-end power gap: with the power divergence stripped out (formula isolation), every reproduced cost account matches 1costingFE to ~1e-8.

**Epic context**: Edits the WI-009 library file `models/library/analyses/mfe_power_balance.sysml`. Consumed by WI-010 (`models/designs/generic_mfe/mfe_plant.sysml`) and WI-018 (`models/designs/stellarator_09/stellarator_plant.sysml`); both need rebinding because the calc's input interface changes (see MR-WI019-2).

## Current State

`models/library/analyses/mfe_power_balance.sysml:85-87` computes

```
p_th = mn·p_neutron + p_input + eta_th·(fpcppf·eta_p + f_sub)·(mn·p_neutron)
```

(an archived-PyFECONS DEC-free form). 1costingFE (`physics.py:303`, step 7) computes

```
p_th = mn·p_neutron + p_rad + p_wall + eta_p·p_pump
```

The SysML form omits the alpha + radiation power reaching the wall — 547 MW (~19% of `p_th`) at the handshake point — and adds only `p_input` (30 MW) plus a small pumping-recovery term. Measured consequence (HANDSHAKE_REPORT.md, "Power balance" table): `p_th`/`p_the`/`p_et` −16.42%, `p_net` −23.52%, `q_eng` −39.95%; power-scaled accounts −8.6% to −16.4%.

Two secondary deviations in the same calc:
- Pumping power is modeled as a fraction of thermal-electric power (`p_pump = fpcppf·p_the`, line 98); 1costingFE takes `p_pump` as an absolute input (no `fpcppf` counterpart exists — HANDSHAKE_REPORT.md discrepancy 9).
- The inlined D-T alpha fraction is the rounded literal `0.2002` (line 67); 1costingFE computes `ash_frac = (17.58 − 14.06)/17.58 ≈ 0.2002275` (`physics.py:32-34,177`). The rounding error (~1.4e-4 relative on `p_alpha`) is invisible today but would dominate the residual once `p_alpha` enters `p_th` directly.

The LCOE calc itself is already correct: `mfe_plant.sysml:320` binds `net_electric_mw = pb.p_net`, so fixing `p_net` fixes the LCOE denominator with no change to `'LCOE DCF'`.

## Key Derivation — why no radiation model is needed

1costingFE's steps 4–7 (`physics.py:290-303`) are, with the demo's standing simplifications (no direct energy conversion, `f_dec = 0`; non-radiation-limited regime, `p_input_eff = p_input`):

```
p_transport = p_ash + p_input − p_rad          (step 4, energy balance)
p_wall      = p_transport                       (step 6, f_dec = 0)
p_th        = mn·p_neutron + p_rad + p_wall + eta_p·p_pump   (step 7)
            = mn·p_neutron + p_ash + p_input + eta_p·p_pump   (p_rad cancels)
```

`p_rad` cancels exactly: whether charged-particle power reaches the wall as radiation or as transport, it is recovered thermally either way. So the faithful DEC-free thermal power needs **no radiation model** — it is flat `+ · ` arithmetic over quantities the calc already has, plus one new input (`p_pump`).

Verified numerically against the emitted 1costingFE point (`exploration/stellarator_e2e/onecfe_point.json`): `p_rad + p_wall = 25.680 + 521.321 = 547.001 = p_ash + p_input = 517.001 + 30.0` ✓, and `p_th − p_ash − p_input − eta_p·p_pump = 2271.57 = 1.100 × p_neutron` (mn = 1.1) ✓.

The regime condition for this collapse is `p_rad − p_ash ≤ p_input` (else 1costingFE raises heating to sustain the plasma, `physics.py:290`). At the handshake point the margin is enormous (`p_rad` 25.7 vs `p_ash` 517 MW); D-T machines sit deep in this regime. See MR-WI019-4.

## Modeling Requirements

### Functional

#### MR-WI019-1: Faithful thermal power

The `'MFE Power Balance Calc'` SHALL compute thermal power as `p_th = mn·p_neutron + p_ash + p_input + eta_p·p_pump`, algebraically equal to 1costingFE `physics.py` step 7 in the DEC-free (`f_dec = 0`), non-radiation-limited (`p_input_eff = p_input`) regime.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: RQ-1, RQ-2; HANDSHAKE_REPORT.md discrepancy 1 (dominant driver of every end-to-end cost divergence)
- **Validation**: SV-025 (power channels match 1costingFE at the handshake point)

> Source: `/home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py`
> Ref: physics.py:290-303 (steps 4–7: p_input_eff, p_transport, p_wall, p_th)
> Basis: DEC-free, non-radiation-limited algebraic reduction of the 1costingFE forward power balance (derivation above)

#### MR-WI019-2: Absolute pumping power input

The calc SHALL take pumping power `p_pump` [MW] as a direct input, replacing the `fpcppf` fraction input, and SHALL use it in both the thermal-recovery term (`eta_p·p_pump`) and the recirculating sum. The concept-09 instance SHALL bind `p_pump = 1.0` from the 1costingFE stellarator default.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: HANDSHAKE_REPORT.md discrepancy 9 (`fpcppf` has no 1costingFE counterpart); faithfulness to physics.py's input contract
- **Validation**: SV-025; L1 parse of all three edited models

> Source: `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml`
> Ref: steady_state_stellarator.yaml:21 (p_pump = 1.0 MW)
> Basis: 1costingFE stellarator primary-coolant pumping power, absolute

#### MR-WI019-3: Exact alpha fraction and aligned subsystem power

The calc SHALL express the D-T alpha (ash) fraction at full precision as the ratio `3.52 / 17.58` (not the rounded literal `0.2002`), and SHALL compute subsystem power as `p_sub = f_sub·p_et` (aligning to `physics.py:315`; numerically identical to the current `f_sub·p_the` while `p_et = p_the`).

- **Type**: Functional
- **Priority**: Must
- **Derives from**: MR-WI019-1's match target — the 0.2002 rounding (~1.4e-4 rel on `p_alpha`) would dominate the SV-025 residual once `p_alpha` enters `p_th` directly
- **Validation**: SV-025

> Source: `/home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py`
> Ref: physics.py:32-34 (E_ALPHA_DT = 3.52, Q_DT = 17.58), physics.py:177 (ash_frac)
> Basis: D-T event energetics; ash fraction = E_alpha/Q = 3.52/17.58

#### MR-WI019-4: Regime assumption documented

The calc's doc comment SHALL state the two regime conditions under which it equals 1costingFE — `f_dec = 0` (no direct energy conversion; standing WI-009 deviation) and `p_rad − p_ash ≤ p_input` (non-radiation-limited; `physics.py:290`) — and record that enforcement of the radiation-limit condition as a viability constraint is deferred to the predictive-physics item (handoff item 2), which is where `p_rad` first becomes available in the model.

- **Type**: Constraint
- **Priority**: Must
- **Derives from**: capture-fidelity surfacing rule; no-fallbacks rule (do not invent a `p_rad` input just to guard a regime the model cannot yet populate)
- **Validation**: doc-comment inspection at review

### Constraint

#### MR-WI019-5: Codegen envelope

All changes SHALL stay inside the proven codegen envelope: flat `Real` attributes, `out attribute` outputs, arithmetic restricted to `+ − * /` (and `**` if needed), no nested calc invocations, no conditionals or `max()`.

- **Type**: Constraint
- **Priority**: Must
- **Derives from**: epic risk 1; `exploration/stellarator_e2e/CODEGEN_FINDINGS.md`
- **Validation**: snapshot → V11-bridge codegen succeeds; SV-025 runs through the generated pipeline

#### MR-WI019-6: Downstream consumers updated coherently

The interface change (drop `fpcppf`, add `p_pump`) SHALL be propagated in the same change to every consumer: `models/designs/generic_mfe/mfe_plant.sysml` (plant attribute + `pb` binding block, lines 123-155), `models/designs/stellarator_09/stellarator_plant.sysml` (replace the `:>> fpcppf = 0.06` binding at line 310 with `:>> p_pump = 1.0`, cited per MR-WI019-2), the codegen-adapted staged copies under `exploration/stellarator_e2e/models/`, the regenerated pipeline, and the pure-Python oracle `exploration/stellarator_e2e/verify_stellaris.py`.

- **Type**: Constraint
- **Priority**: Must
- **Derives from**: MR-WI019-2; the canonical-vs-staged split (staged copies are deliberate codegen adaptations, not to be back-ported into `models/`)
- **Validation**: L1–L6 pass on canonical models; `run_stellaris.py` oracle agreement; SV-025/SV-026

### Traceability

#### MR-WI019-7: Citations

Every changed formula and value SHALL carry an MR-4 `Source / Ref / Basis` citation resolving to 1costingFE at pin `0254385` (file:line) or to an admissible repo file. No ARIES-CS-informed source may be cited (PROTOCOL.md §3).

- **Type**: Traceability
- **Priority**: Must
- **Derives from**: MR-4, PR-series traceability rules; PROTOCOL.md
- **Validation**: citation inspection at review

## Scope Boundaries

**In scope**
- `models/library/analyses/mfe_power_balance.sysml` — the formula fix (MR-WI019-1/2/3/4).
- `models/designs/generic_mfe/mfe_plant.sysml`, `models/designs/stellarator_09/stellarator_plant.sysml` — interface rebinding only.
- `exploration/stellarator_e2e/` — staged copies, regenerated pipeline, oracle update, handshake re-run, refreshed HANDSHAKE_REPORT numbers, new Stellaris headline (p_net / LCOE will change).
- `modeling_project/VALIDATION_MATRIX.md` — SV-025/SV-026 (created by this spec, status pending).

**Out of scope**
- Radiation model (`p_rad`: bremsstrahlung/synchrotron/impurities) and the radiation-limited `max()` branch — deferred to handoff item 2 (predictive physics), per MR-WI019-4.
- Direct energy conversion (`f_dec`, `eta_de`) — standing WI-009 deviation 1, unchanged.
- The unmodeled CAS22 tail, CAS40/50/60, and LCOE construction differences (CAS70 O&M levelization, CAS80 fuel, IDC-as-CAS60) — separate Stage-3 backlog items; the IDC question is an open owner decision (handoff Open Questions).
- Geometry (torus volume) and `sigma_v` back-solve — handoff items 4 and 2.
- Any change to `'LCOE DCF'` — the denominator fix arrives through `pb.p_net` automatically.

## Success Criteria

1. **SV-025 (formula isolation, the faithful-balance test)**: fed 1costingFE's own inputs at the Anchor A point, the generated power balance reproduces the 1costingFE power table — `p_th` = 2819.07, `p_the` = `p_et` = 1127.63, `p_net` = 1000.0 MW, `q_eng` = 8.835 — within 1e-5 relative (the reference table is JAX float32, ~1e-7 floor; 1e-5 leaves headroom for the float32 emission).
2. **SV-026 (end-to-end gap collapse)**: re-running `handshake_1costingfe.py`, every power-scaled account's end-to-end deviation collapses from −8.6…−16.4% to ≤0.1%, leaving only the documented structural gaps (vessel gas-load sub-term ~0.8%, unmodeled accounts, rollup/LCOE construction).
3. Validation Levels 1–6 pass on the canonical models; the IFE anchor regression (SV-023) still passes; `run_stellaris.py` remains bit-exact against the updated oracle.
4. The new Stellaris design-point headline (fusion power unchanged at 2700 MW; new p_th, p_net, LCOE, account shares) is recorded in the work item and `.project/CURRENT_WORK.md`.

## Assumptions & Risks

1. **Non-radiation-limited regime holds for all demo design points** (confidence: high for D-T; margin at the handshake point is 517 vs 25.7 MW). If a future design point violates it, the calc overstates nothing silently — the deferred item-2 constraint will guard it; until then it is a documented assumption (MR-WI019-4).
2. **float32 reference precision** (likelihood: certain, impact: low): 1costingFE's emitted power table carries ~1e-7 relative noise; SV-025's 1e-5 tolerance absorbs it. Formula-isolation residuals at ~1e-8 remain the codegen-machinery evidence.
3. **Interface-change ripple** (likelihood: medium, impact: low): dropping `fpcppf` breaks any unnoticed consumer. Mitigation: MR-WI019-6 enumerates consumers; L1 parse across `models/` catches stragglers.
4. **Viability constraints shift numerically** (likelihood: certain, impact: low): `q_eng` rises ~40%, `rec_frac` falls; the WI-009 viability constraints (net electric > 0, rec_frac bound) move further into the passing region. SV-016's "Q_eng ~10–40" reasonableness band should be checked against the corrected value at the Stellaris point during implementation (the 1costingFE 1 GWe point gives 8.8 — just below the band's stated floor; flag at review if the Stellaris point lands similarly).

## Traceability

**Sources**
- `/home/reid/1cfe/1costingfe` @ `0254385`: `src/costingfe/layers/physics.py:290-328` (steps 4–14), `physics.py:32-34,177` (D-T energetics), `src/costingfe/data/defaults/steady_state_stellarator.yaml:21` (p_pump).
- `exploration/stellarator_e2e/HANDSHAKE_REPORT.md` — quantified gap and discrepancy inventory (items 1, 9).
- `exploration/stellarator_e2e/onecfe_point.json` — the numeric verification point.

**Downstream impacts**: WI-010 plant, WI-018 instance, staged e2e models/pipeline/oracle/handshake, VALIDATION_MATRIX SV-025/026, Stellaris headline numbers quoted in `.project/CURRENT_WORK.md` and the demo concept doc.

**Applicable project rules**: MR-4 (citations), MR-3 (library stays concept-agnostic — `p_pump` is a generic input; the 1.0 MW value binds in the instance), PROTOCOL.md (clean-room), no-fallbacks (no invented `p_rad`).

## Related Artifacts

- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Handoff (item 3): `/tmp/handoff-20260714-214343.md`
- Handshake: `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`
- Design: `work/active/WI-019_faithful-mfe-power-balance/design.md` (to be created after owner checkpoint)
- Plan: `work/active/WI-019_faithful-mfe-power-balance/plan.md` (to be created)
