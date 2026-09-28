---
Status: complete
Created: 2026-09-25
Updated: '2026-09-25'
---

# Design — network heat-driven closure

Related Artifacts: spec.md; plan.md; goal round-2 strategy in `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/trail.md`. All choices are [AGENT] unless attributed; source facts are graded in the goal's reference-case contract. Revised 2026-09-25 after the fresh design review r1 (`evidence/design-review.md` under the goal); corrections are marked `[r1]`. Revised again after the fresh implementation review (`evidence/implementation-review.md`, PASS with notes); those corrections are marked `[ir]`.

## Architecture

Add `calc def 'Network Heat Driven Closure'` to `models/library/analyses/integrated_heat_electricity.sysml`, next to the retained `'Heat Driven Closure'`. Its inputs are the 23 inputs of the reviewed closure plus `network_mode_in` (0 = series as reviewed, 1 = published network) and `pbli_split_in` (fraction of cycle flow through the PbLi stage in mode 1). Its outputs are the 40 reviewed outputs plus `pbli_stream_out`, `divertor_stream_out`, `mixed_outlet`, `network_mode_used` and `pbli_split_used` `[ir]` (the two echo outputs were named `network_mode` and `pbli_split` in r1; a calc output may not share the name of the part's input attribute, the generator refuses the clash, so they carry the `_used` suffix). The completion `network_heat_driven_closure_impl.py` reproduces the reviewed stage and closure equations for mode 0 equation for equation (the reviewed loop refactored into one stage helper with the cycle-side capacity rate as a parameter), bit-exact on replay `[ir]`, and adds the mode-1 network; it is a new file under `exploration/aries_integrated/native_completions/`, built through the unchanged `build.py` route (typed adapter, fixed-point regeneration).

In `models/designs/aries_cs_integrated/plant.sysml` the `heat_exchangers` part gains `attribute network_mode : Real = 0.0;` and `attribute pbli_split_fraction : Real = 0.85;`, rebinds `calc evaluate : 'Network Heat Driven Closure'` with the two new inputs, and exposes the five new outputs. Every existing consumer (turbine, recuperator, precooler, plant ledger, capacity screens) keeps binding the same attribute names; no other part changes.

## Equations

Notation as in the WI-089 design: `C = flow·cp/1e6` (cycle capacity rate, MW/K), `k` the expansion factor, `R(Tt) = Tc + ε_r·max(k·Tt − Tc, 0)` the heater inlet, and for a stage with primary capacity rate `Ch`, conductance `UA`, cycle-side capacity rate `Cs`: `Cmin = min(Ch, Cs)`, `Cr = Cmin/max(Ch, Cs)`, `NTU = UA/Cmin`, counterflow effectiveness `ε = (1 − e^{−NTU(1−Cr)})/(1 − Cr·e^{−NTU(1−Cr)})` (or `NTU/(1+NTU)` at `Cr = 1`), coefficient `K = ε·Cmin ≤ Cs`, capability `qcap = K·max(L − Tin, 0)`, transfer `q = min(Q, qcap)`, cycle-side outlet `Tin + q/Cs`, primary hot inlet `Tin + q/K` and return `hot − q/Ch` when defined.

Mode 0 (series, copied): stages visited helium → divertor → PbLi with `Cs = C` for each, `Tin` chained; equation for equation the reviewed completion and bit-exact on replay of all 31 mode-0 points (`evidence/migration-report.json`) `[ir]`.

Mode 1 (network): helium stage with `Cs = C` from `R` to `T1`; PbLi stage with `Cs = s·C` from `T1` to `Tp = T1 + q_p/(s·C)`; divertor stage with `Cs = (1 − s)·C` from `T1` to `Td = T1 + q_d/((1 − s)·C)`; adiabatic mixing `Tmix = s·Tp + (1 − s)·Td = T1 + (q_p + q_d)/C`. Residual `F(Tt) = C·(Tt − R(Tt)) − (q_he + q_p + q_d)`; at the root `Tt = Tmix`. Monotonicity: each `q` is nonincreasing in its inlet, `T1` is nondecreasing in `R`, and `R` has slope below one in `Tt`, so `F` is strictly increasing; the bracket `[Tc, max(Tc, L_he, L_pbli, L_div)]` has opposite signs by the same argument as WI-089. Bisection, tolerances and iteration cap unchanged (1e-8 MW, 1e-10 K, 100). Domain `[r1]`: `0 < s < 1` is required in both modes and refused otherwise (one rule); in mode 0 the value has no effect on the result. Both parallel stages see `T1` as inlet; the published cycle helium enters the train at one temperature and the two streams are at the helium-stage outlet pressure (no branch pressure-loss model).

Outputs in mode 1: `he_secondary_out = T1`; `pbli_secondary_in = divertor_secondary_in = T1`; `pbli_secondary_out = Tp`, `divertor_secondary_out = Td` (per-stream outlets; the series identity `pbli_secondary_out = turbine_temperature` no longer holds); the per-stage terminal differences use the stream's own `Cs` `[r1]`; `pbli_stream_out = Tp`, `divertor_stream_out = Td`, `mixed_outlet = Tmix`; `turbine_temperature = Tt`. In mode 0 the three new temperature outputs equal the corresponding series values (`pbli_secondary_out`, `divertor_secondary_out`, `turbine_temperature`) so downstream reporting is uniform.

**Consumers under mode 1** `[r1]` (inspected in `plant.sysml` and `integrated_plant_ledger_impl.py`): the turbine, recuperator and precooler bind only `turbine_temperature` (and the recuperator the compressor outlet), so their meaning is unchanged; `heater_inlet` stays the whole-flow inlet to the first stage, so the ledger's recuperator state residual (`recuperator_cold_out − heater_inlet`) and turbine state residual (`turbine_exhaust − k·turbine_temperature`) hold; the ledger reads only `accepted_heat`, `unmet_heat`, `turbine_temperature`, `expansion_factor`, `heater_inlet` and `closure_residual`; `heat_removal_ok` reads `unmet_heat`; the three heat-duty capacity screens read the coolant `delivered_heat` (available duty, not stage transfer); the pumps read the primary flows. No consumer reads a per-stage channel or assumes chaining.

## MR-7 variable roles (affected quantities only)

| Quantity | Units | Role before | Role after | Binding | Authority |
|---|---|---|---|---|---|
| `heat_exchangers.network_mode` | code 0/1 | (absent; series implied) | supplied analysis-mode choice; default 0 | assembly attribute → closure input | [AGENT] this design; owner brief permits the reviewed architecture alternative |
| `heat_exchangers.pbli_split_fraction` | 1 | (absent) | supplied operating choice (flow-distribution setting), nominal 0.85, range 0.5–0.95 for study | assembly attribute → closure input | [AGENT] N1; no control law claimed |
| Cycle flow, cp, γ, pressures, efficiencies, ε_r | as before | chosen | unchanged | unchanged | WI-089 A3/S3 |
| Primary flows, cp, UA (= area × U), hot-side bounds | as before | chosen | unchanged | unchanged | WI-089 A4, WI-090 E2 |
| Per-stage transferred/unmet heat, stream and mixed temperatures, turbine inlet, primary states | MW, K | calculated | calculated (new stream/mixed outputs added) | closure outputs → turbine/recuperator/ledger | this design |
| Offered ratings and capacity screens | as before | chosen / calculated margin | unchanged | unchanged | WI-089 A6 |

No quantity becomes an installed capacity or is derived from demand. The split does not size anything: a wrong split leaves heat unremoved in one stream (reported), it never enlarges an exchanger. `s` stands in for the unmodelled branch hydraulic balance, and its 0.85 default was informed by the available-heat proportion at the C3 inputs (≈ 0.886), not fitted to any output `[r1]`. Direction test for R3 `[r1]` (the model does not fully transfer the PbLi heat at C3 inputs in any mode, because above `s ≈ Ch_pbli/C ≈ 0.61` the PbLi stage is bounded by its primary capacity rate and the helium stage binds as the turbine temperature rises): at C3 inputs in mode 1 the scratch check gives PbLi unmet ≈ 197 MW at `s = 0.55`, ≈ 56 MW at `s = 0.85` (with ≈ 54 MW helium unmet), and divertor unmet ≈ 149 MW at `s = 0.98`, hardware identical across the three; the implementation must reproduce that ordering with the native package.

## Migration and preservation

Public inputs gain `aries_integrated_plant__heat_exchangers__network_mode` (default 0) and `aries_integrated_plant__heat_exchangers__pbli_split_fraction` (default 0.85). The interface also gains five outputs (`pbli_stream_out`, `divertor_stream_out`, `mixed_outlet`, `network_mode_used`, `pbli_split_used` `[ir]`; 546 → 551 numeric outputs per point) and the bound calc type of `heat_exchangers.evaluate` changes `[r1]`. Existing full maps are migrated by adding the defaults; a machine-readable migration report lists the two keys, the five outputs, the type change, and the exact mode-0 replay comparison for the four canonical maps and the 27 sealed points (every numeric output at relative ≤ 1e-12, exactly-zero outputs compared absolutely at 1e-12, every verdict identical). The live study manifest is re-pinned with `prepare_metadata.py --pin-manifest` after a clean-package check; frozen records are untouched. The reviewed `Heat Driven Closure` definition and its completion remain in the library and in `native_completions/` unchanged; they are no longer bound by the live assembly. The same disclosure sentence goes into the new calc def's doc comment and the completion's docstring `[r1]`.

**Disclosure wording `[ir]`.** As committed at `6828df18`, the calc-def doc comment and the completion docstring state the same three facts in different wording (mode 0 reproduces the reviewed equations; the split is an operating choice, never a sizing rule; `0 < split < 1` in both modes) and both say "line for line" where "equation for equation, bit-exact on replay" is the accurate claim. Both texts are part of the sealed package identity, so the wording is corrected here and in `evidence/implementation-review-notes.md` and will be applied to the package at its next edit, not as a wording-only rebuild.

## Assumptions

| ID | Assumption | Range / replacement condition |
|---|---|---|
| N1 | Split 0.85 nominal, a fixed flow-distribution setting [AGENT]; the available-heat proportion at the C3 inputs is ≈ 0.886 | 0.5–0.95 study window; replace with an explicit control policy (e.g., equal stream outlets) if a source states one |
| N2 | Adiabatic ideal mixing of the two streams; no mixing pressure loss | Replace with a branch pressure-loss model when hydraulics exist |
| N3 | Both parallel stages at the helium-stage outlet state; no branch pressure drop | Same |
| N4 | Same ε-NTU counterflow, constant-property approximation per stage as WI-089 | As WI-089 A4 |

## Validation plan

Development checks through the stock route: (a) mode-0 exact replay of the four canonical maps and the 27 sealed points; (b) mode-1 at C3 inputs compared with the independent scratch check (`evidence/parallel-network-scratch.py`: turbine 919.46 K, unmet 113.68 MW at s = 0.8) to 1e-6; (c) the R3 direction triple (split 0.55 / 0.85 / 0.98 at fixed hardware); (d) refusals for s ∉ (0,1), mode ∉ {0,1}; (e) zero-UA definedness in mode 1; (f) energy ledger residual below tolerance in every evaluated case. Then fixed-point regeneration, scoped validation, preservation manifest, isolated Stellaris replay, independent implementation review and the integration seam.
