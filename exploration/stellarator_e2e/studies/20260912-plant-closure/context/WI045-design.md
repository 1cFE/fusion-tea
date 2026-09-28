---
Status: active
Created: 2026-09-08
Updated: 2026-09-08
Related Artifacts:
  Spec: ./spec.md
---

# WI-045 Design — the primary coolant loop and the temperature-compatible cycle

A representative helium circuit anchored to the Moscato 2017 reference computes the loop flow, pressure loss, compressor work and IHX duty from the reactor's source heat; a handwritten calc computes the cycle efficiency from the loop outlet by the printed Kovari 2016 fit; the power balance takes the loop's electrical draw and recovered heat where it took the held scalars, in a form whose dormant mode reproduces the entering pin bit-for-bit. Written under goal `plant-closure` round 1, task T-003 (`work/orchestration/goals/plant-closure/trail.md` § T-003 scope); the form is `[AGENT] — proposed under the owner's direction of 2026-09-08` (`goal.md` § Reserved gates 2, 3, 6). The arithmetic is prototyped in `prototype/proto.py` (`proto_results.json`); no model file is touched by this design.

## Overview

Today `p_pump` 195 MW, `eta_p` 0.5 and `eta_th` 0.333 are instance scalars the power balance reads (spec § Current state). After this item:

- a new `'Reactor Source Heat'` publishes `q_source = mn·p_n + p_α + p_coupled`, the reactor's heat with no pump credit;
- a new `'Primary Coolant Loop'` (flat arithmetic) sizes the flow from `q_source` at a held 200 K blanket rise, computes the per-loop flow at a held loop count, the per-path pressure loss by a constant loss coefficient anchored to the reference circuit, the compressor inlet temperature from the pressure ratio, the fluid work, the electrical draw and the IHX duty — and forms the two quantities the power balance consumes, each with its dormant term inside the calc: `p_pump_total = loop_live·p_elec + p_pump_direct` and `q_recovered_total = loop_live·w_fluid + eta_p_direct·p_pump_direct`;
- a new `'Power Cycle Efficiency'` (handwritten) computes `eta_th = cycle_live·eta_fit + eta_th_direct` from the loop outlet less a 20 °C approach by the printed helium-primary Rankine fit, with the fit's domain margins;
- `'MFE Power Balance Calc'` takes `q_recovered_in` and `p_pump_total_in` at the exact positions `eta_p_in·p_pump_in` and `p_pump_in` occupied;
- three verdicts appear: `loop_pressure_ok`, `loop_capacity_ok`, `cycle_domain_ok`.

In held mode (`loop_live` 0, `cycle_live` 0, `p_pump_direct` 195, `eta_p_direct` 0.5, `eta_th_direct` 0.333) every existing channel is bit-identical (§ Expected baseline behaviour; the prototype's `==` checks all `True`). In live mode the design point reads 175.44 MW of loop electricity, 0.41136 cycle efficiency, `p_net` 1012.36 MW and LCOE 237.25 $/MWh at the held availability 0.85 (§ Expected baseline behaviour). Off the design point the capacity fence bites at the first step: the design point is sized 4.5 % under the rated per-loop flow, so a plasma one step fatter (a 1.4) and the committed cheapest machine both exceed it at 14 loops — the cheapest machine's loop then draws 1448 MW and its recirculating fraction 0.527 breaks `recirc_ok`, and re-sizing the count to 27 by the same rule restores every verdict at 381 MW and LCOE 171.23 (§ Off-design predictions). That is the Row-7 "coolant choices push back" mechanism in numbers, and it is why the round's study carries the loop count as a lever.

## Research findings

- **The calibration must be solved on the calc's own compressor form.** The probe (`evidence/grounding_probe/summary.md`) derived `eta_is` 0.7766 as `dT_isentropic / dT_actual` with the isentropic drop taken from the outlet end (`T_in·(1 − r^−k)`); the calc evaluates compression from the inlet end (`T_in = T1·(1 + (r^k − 1)/eta_is)`), for which the closed form is `eta_is = (r^k − 1)·T1 / dT_actual` with `T1 = T_in − dT_actual`. On the wrong form the reference reconstruction misses its own energy check by 0.62 MW (`proto_results.json` first run, superseded); on the calc's form it reproduces 129.4 MW to −1.4e-13 MW (§ Validation report). The packet § 7's 174.60 MW and the spec's table therefore move to **175.44 MW** at the design point; nothing else in the probe changes. Recorded here for the packet's next amendment.
- **The reference numbers, from the extraction and the renders** (`knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md@891b95bc` lines 79–81, 89–91, Table 1 at 105–113, Table 2 at 128–130, Table 3 at 151–154; `evidence/grounding_sources/moscato_p6_tables2_3.png`): 8 MPa, 300 → 500 °C, 2101.7 MW at 2025.7 kg/s over 9 loops (3 IB + 6 OB); IB path 214 + 62 + 87.9 = 363.9 kPa, OB path 174 + 56.6 + 85.1 = 315.7 kPa; IHX 208.1 / 267.8 MW per loop, 2231.1 MW in all; circulators 6.8 / 7.5 MW per unit, two per loop, 130.8 MW in all. The implied `cp` 5187.6 J/(kg K) is 0.10 % under ideal helium's 5193.1 (NIST 20.786 J/(mol K) over 4.002602 g/mol); the calc binds 5193.0 and the reconstruction reports the discrepancy.
- **The fit, from the registered source** (`knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md` line 355; `evidence/grounding_sources/kovari2016_p9_table4.png`): helium-primary steam Rankine `0.1802 ln(T2 + 273) − 0.7823 − Δη`, `T2` 384–642 °C, `T1 − T2` 20 °C, `T3` 150 °C; sCO2 `0.4347 ln(T2 + 273) − 2.5043`, 135–750 °C. The text beside it: Dostal's Rankine modelling with a 0.0179 benchmark adjustment already inside the printed fit (not to be subtracted again); the divertor heat used in a separate feedwater preheater for Rankine (the Δη correction) — not modelled here, Δη 0.
- **The codegen envelope and the module graph.** `+ - * / ** ^` only (`~/1cfe/sysml-codegen/src/sysml_codegen/extraction/calc_compat_renderer.py`); a chain of `out attribute`s referencing earlier outputs and one non-out intermediate is emitted in source order (`'MFE Radial Build'`, `'Conductor Peak Field'` after WI-044). A multi-output `manual_required` calc declares its outputs without expressions and the generated caller unpacks the impl's tuple in the caller's own order (`generated/modules/mfe_plasma_sustainment/plasma_sustainment.py:685`, seventeen outputs); a single-output one returns a float (`levelized_replacement_cost.py:329`). The `Input` model is `stellarator_tea.modules.<package>.<calc_snake>.<Calc_Name>Input`.
- **A dependency cycle, avoided.** The packet named `pb__q_source` (a power-balance output) as the loop's input; but the power balance also consumes the loop's recovered heat, so `pb → loop → pb` would be a cycle in the module graph. The source heat is therefore its own calc, upstream of the loop (D3), and the channel is `source_heat__q_source`.
- **A plant-level aggregation is not a reliable producer.** `mfe_account_costs.sysml` (the `'Annual Cost Rollup'` note) and WI-028: a plant attribute that sums calc-output exposures classifies without a part root and may mint no channel. The two dormant aggregations the packet wrote at plant level (`q_recovered`, `p_pump_total`) are therefore outputs of the loop calc, which takes the two direct terms as inputs (D9); the channel names become `loop__q_recovered_total` and `loop__p_pump_total`.
- **The recirculating fence is `rec_frac ≤ 0.5`** (`mfe_viability.sysml:21–38`, default threshold). At `c2823` on 14 loops the live `rec_frac` is 0.527, so the loop's cubic draw breaks `recirc_ok` there as well as `loop_capacity_ok`.
- **The oracle is rewritten by model items** (WI-039, WI-041, WI-042, WI-044 precedent); its `IN` carries `eta_th`, `eta_p` (`verify_stellaris.py:234`), `p_pump` (247); `compute()` forms `p_th` at 479–480 and `recirculating` at 490. The seam maps `eta_th` at `oracle_entry.py:121`; `p_pump` and `eta_p` are unmapped.

## Design decisions

### D1 — The reference per-path loss is the flow-weighted mean of the IB and OB paths, 329.1871856931558 kPa. `[AGENT]`
The representative circuit is one path; the reference has two. Weighting by IHX duty (3 × 208.1 against 6 × 267.8) is weighting by flow share at the common 200 K rise, so the weighted loss is the loss the reference's average kilogram sees. The OB path alone (315.7 kPa, 0.7402 by the same calibration) and the IB path (363.9, 0.8570) are reconstructed beside it (`proto_results.json` `reference.paths`); the design point's draw would read 175.44 on any of the three because the calibration absorbs the choice at the reference — the choice matters only through the pressure ratio's small nonlinearity off design (under 0.1 % between the paths). Rejected: the OB path as "the majority path" — it under-weights the IB loops' higher loss for no physical reason.

### D2 — `eta_is` is the exact double 0.772796639536644, solved on the calc's compressor form; the 1.4 MW printed-versus-fluid residual is left as the check's own discrepancy. `[AGENT]`
Closed form `(r^k − 1)·(T_in − ΔT)/ΔT` with `r` = 8 / (8 − 0.3291871856931558) MPa, `k` = 0.4, `ΔT` = 129.4e6 / (2025.7 × 5193) = 12.301011531951204 K (§ Research findings). Bound as that double, not rounded: the reconstruction returns `w_fluid` 129.4000000000004 MW (−1.4e-13 MW); no neighbouring double within ±4 ulps hits 129.4 exactly, so the residual is stated rather than searched away. The 130.8 MW printed circulator total stands 1.4 MW above the fluid work and is not folded into the calibration: it is the source's own bookkeeping residual and the reason the electrical boundary is disclosed as a lower bound (spec MR-WI045-5). Labelled a source-point calibration in the instance doc and in the SV row; never cited as validation (MR-WI045-4).

### D3 — The source heat is its own calc, `'Reactor Source Heat'` in `mfe_power_balance.sysml`, wired as `source_heat` upstream of the loop. `[AGENT]`
Avoids the `pb ↔ loop` cycle (§ Research findings). Its expression `mn_in * p_neutron + p_alpha + p_input_in` is the power balance's own partial sum in the same order, so `q_source` equals the float the power balance forms internally. Channel `source_heat__q_source` (the packet's `pb__q_source` renamed; reported to the round).

### D4 — One approach, on the loop outlet: `T_hot_in = loop.T_out`, `dT_approach` 20 °C; no intermediate loop. `[AGENT]`
Kovari's `T1 − T2` is the one approach the fit's contract defines. The reference's HITEC intermediate circuit (270 → 465 °C) would add a second approach and a low-grade convention before any first evidence; not modelled, and the cycle doc says so (the research's "one temperature-compatible cycle, then a matched-heat second arm").

### D5 — The verdict operands are calc outputs: `loop.p_loop_margin`, `loop.mdot_loop` against the instance's `mdot_loop_ref`, `cycle.domain_product`. `[AGENT]`
Calc outputs are producer channels and bind cleanly (the WI-041 lesson). `'Loop Capacity'` takes the per-loop flow and the rated flow as two formals so the fence reads the instance's reference figure directly (the same attribute the loop's loss law is anchored to). A `capacity_margin` output is published beside it for the study.

### D6 — The off-design points are the design column at `a` 1.4 (P1), the committed cheapest machine `c2823` at the instance's 14 loops (P3) and the same machine with the count re-sized by the sizing rule to 27 (P4). `[AGENT]`
The design point is sized with 4.5 % headroom (215.05 against 225.08 kg/s per loop), so the capacity fence catches P1 (228.14) and P3 (431.30); P3 also breaks `recirc_ok` (0.527) because the draw is cubic in the per-loop flow. P4 shows the lever: at 27 loops (223.64 per loop) every verdict is satisfied and the draw is 380.77 MW. Three points, three different fence outcomes; the plasma and magnet channels at each are the entering pin's, so any move is the loop's or the cycle's. The consequence for the round's study, stated here so the study scopes it: at a held count of 14 almost every committed point off the design column violates `loop_capacity_ok`; the study needs an arm whose loop count is re-sized per point by the same rule (a proposal-side computation, not a model `ceil`), and the counts under the old ten verdicts stand beside both readings.

### D7 — The seam's levers: `loop_live`, `cycle_live`, `p_pump_direct`, `eta_p_direct`, `eta_th_direct`, `n_loops`, `dT_blanket`, `T_in`, `f_loss`, `dT_approach`; the fit coefficients and domain are not levers. `[AGENT]`
A study that wants the sCO2 row swaps `a_fit`, `b_fit`, `T2_min`, `T2_max` together through a declared arm binding, never one coefficient alone (spec open decision 7). `eta_th` retires from the map (it is a channel now); `eta_p` and `p_pump` were never mapped.

### D8 — Two new library files, `mfe_primary_loop.sysml` and `mfe_power_cycle.sysml`; the plant imports both. `[AGENT]`
One package per calc family, as `mfe_heating_chain` and `mfe_cryo_plant` are; the handwritten stage's directory follows the package name (`generated/handwritten/mfe_power_cycle/`).

### D9 — The two dormant aggregations live inside the loop calc as outputs, with the direct terms as loop inputs. `[AGENT]`
`q_recovered_total = loop_live_in * w_fluid + eta_p_direct_in * p_pump_direct_in` and `p_pump_total = loop_live_in * p_elec + p_pump_direct_in`. In held mode `0.0 * w_fluid` is exactly `0.0` (finite `w_fluid`; the largest committed plasma gives 2011 MW, finite — `proto_results.json` `window_extreme_c3598`), `0.0 + 97.5` is `97.5` and `0.0 + 195.0` is `195.0`, so the power balance receives the held scalars to the bit and its sums are unchanged in every operand and position (§ Expected baseline behaviour, `held_mode_identity` all `True`). Rejected: plant-level aggregations (not reliable producers, § Research findings).

### D10 — The five flags and directs carry dormant defaults 0.0 on the generic plant; every circuit and fit fact is unbound there and bound by the one concrete instance (the WI-044 D6 convention). `[AGENT]`
A concept that binds nothing reads "no loop, zero efficiency" and must bind its own directs — the WI-039 EI-5 lesson, stated in the plant doc. The abstract plant compiles unbound; the IFE designs do not import it; the tokamak half of epic Item 3 binds its own circuit as it binds its own magnet facts.

### D11 — The three constraint defs in `mfe_viability.sysml`: `'Loop Pressure Margin'` (`p_loop_margin_in > 0.0`), `'Loop Capacity'` (`mdot_loop_in <= mdot_loop_rated_in`), `'Cycle Fit Domain'` (`domain_product_in >= 0.0`). `[AGENT]`
The `'Burn Hold'` form (packet § 1). The domain product is one constraint for the two-sided bound, valid because `T2_min < T2_max` is a fact of the bound row.

### D12 — The oracle derives the loop and the cycle from this design's equations, in both modes; the seam publishes twenty channels and three bindings. `[AGENT]`
`verify_stellaris.py`: `IN` drops `eta_th`, `eta_p`, `p_pump`; gains the five flags/directs, the eleven circuit facts and the seven fit facts; `compute()` forms `q_source`, the loop chain, the cycle chain, then `p_th = mn·p_n + p_α + heat_coupled + q_recovered_total` and `recirculating = p_coils + p_pump_total + …` — written from § Proposed design, not from the generated modules. `oracle_entry.py`: the entry-key map −3 +23, the channel map +11, `OPERAND_BINDINGS` +3 with the constraint ids read from `generated/contracts/model_contract.json` at implementation.

### D13 — The cycle impl returns a six-tuple in the regenerated caller's unpack order, which the implementation reads from the stencil before restoring the body. `[AGENT]`
The stencil's `inputs.<field>` names and the caller's tuple order are facts of the regeneration, not of this design (WI-042's "verified at the regeneration"). A non-positive fit argument raises (`math.log`), which is the fail-closed behaviour the spec asks for; no clamp.

### D14 — Commit order A / B / C, and WI-045 integrates first on the shared files. `[AGENT]`
Commit A: the model edits, the twins, spec, design, plan (with the MR-WI045-16 restatement and the predictions), `prototype/`, `evidence/baseline_before/`. Commit B: the regenerated package, the handwritten impl, the oracle, the seam, the single runner, the re-pin, the fixtures and count sites, SV and trace rows, `evidence/baseline_after/`, `evidence/compat_mode/`, `evidence/offdesign_points/`. Commit C: the `tests/study` run of record. WI-046's plan starts from commit C's tree (packet § 9).

### D15 — Two instance comments corrected in the same edit: `eta_th`'s "Stellaris steam-cycle thermal efficiency" and the turbine part's "Stellaris uses a steam (Rankine) cycle". `[AGENT]`
The source assumes a simple 1/3 conversion and names no cycle (spec § Current state; the WI-031 research). The Rankine reading now rests on Kovari's helium-primary row, chosen by this design, and the text says so; the turbine's per-MW rate keeps its 1costingFE RANKINE-preset basis.

## Proposed design

### New: `calc def 'Reactor Source Heat'` — `models/library/analyses/mfe_power_balance.sysml` (D3)

```sysml
    calc def 'Reactor Source Heat' {
        doc /*
        The reactor's heat with no pump credit (WI-045, goal plant-closure):
          q_source = mn * p_neutron + p_alpha + p_input
        the first three terms of 'MFE Power Balance Calc''s thermal sum in the
        same order, published as its own producer so the primary loop can size
        its flow from it without a dependency cycle (the power balance consumes
        the loop's recovered heat). The alpha/neutron split is the inlined D-T
        ratio 3.52/17.58 exactly as the power balance forms it, so q_source
        equals the power balance's own partial sum to the bit.
        **Source**: models/library/analyses/mfe_power_balance.sysml ('MFE Power Balance Calc', p_th)
        **Ref**: WI-019 collapse p_th = mn*p_neutron + p_alpha + p_input + (recovered pump heat)
        **Basis**: reactor source heat before the loop's own recovered work; the heat ledger's one source (packet § 5)
        */
        in attribute p_nrl : Real;
        in attribute p_input_in : Real;
        in attribute mn_in : Real;
        attribute p_alpha : Real = (3.52 / 17.58) * p_nrl;
        attribute p_neutron : Real = p_nrl - p_alpha;
        out attribute q_source : Real = mn_in * p_neutron + p_alpha + p_input_in;
    }
```

### Changed: `calc def 'MFE Power Balance Calc'` — same file (D9)

Formals `eta_p_in` (line 60) and `p_pump_in` (69) retire; two replace them at the same places in the declaration:

```sysml
        // Recovered pump heat entering the thermal sum [MW] (WI-045): the loop's
        // fluid work when the loop is live, or eta_p_direct * p_pump_direct when
        // it is dormant -- formed inside 'Primary Coolant Loop' so that in the
        // dormant mode the value is exactly the old eta_p * p_pump scalar.
        in attribute q_recovered_in : Real;
        // Primary pump electrical draw entering the recirculating sum [MW]
        // (WI-045): loop_live * p_elec + p_pump_direct, formed in the loop calc.
        in attribute p_pump_total_in : Real;
```

and the two sums keep their operands and order with the new formals at the old positions:

```sysml
        out attribute p_th : Real =
            mn_in * p_neutron + p_alpha + p_input_in + q_recovered_in;
        ...
        attribute recirculating : Real =
            p_coils + p_pump_total_in + p_sub + p_aux + p_cool + p_cryo
            + p_wallplug_in;
```

`p_the = eta_th_in * p_th` is unchanged; `eta_th_in` now arrives from the cycle calc. The doc's "Thermal power derivation" paragraph gains the WI-045 note (the recovered term is the loop's, the credit's meaning unchanged in the dormant mode).

### New: `calc def 'Primary Coolant Loop'` — `models/library/analyses/mfe_primary_loop.sysml` (D1, D5, D9)

```sysml
package mfe_primary_loop {
    private import ScalarValues::*;

    calc def 'Primary Coolant Loop' {
        doc /*
        Representative helium primary circuit in sized-flow mode (WI-045, goal
        plant-closure; the research 20260907-163520_primary-loop-cycle-closure-prework
        section 2). One hydraulic path stands for the circuit; the loop count
        scales it. Dependency order: source heat -> flow -> per-path loss at the
        reference's nominal density -> compressor -> fluid work -> electrical
        draw -> IHX duty. There is no edge from the plant's thermal power back to
        the flow.

          mdot        = q_source * 1e6 / (cp * dT_blanket)            [kg/s]
          T_out       = T_in + dT_blanket                             [K]
          mdot_loop   = mdot / n_loops                                [kg/s]
          dp_loop     = f_loss * dp_loop_ref * (mdot_loop/mdot_loop_ref)^2  [Pa]
          r_comp      = p_loop / (p_loop - dp_loop)                   [1]
          T_comp_in   = T_in / (1 + (r_comp^((gamma-1)/gamma) - 1)/eta_is)  [K]
          w_fluid     = mdot * cp * (T_in - T_comp_in) / 1e6          [MW]
          p_elec      = w_fluid / eta_drive                           [MW]
          q_ihx       = q_source + w_fluid                            [MW]
          p_pump_total       = loop_live * p_elec + p_pump_direct     [MW]
          q_recovered_total  = loop_live * w_fluid + eta_p_direct * p_pump_direct [MW]

        THE LOSS LAW is a constant loss coefficient about the reference layout
        at its nominal density: the reference's per-path loss scaled by the
        square of the per-loop flow ratio, rho_ref/rho taken as 1 (the loop is
        held at the reference's pressure and temperature window). It computes
        loss from flow; it is NOT a fraction of thermal power (the form the
        owner rejected 2026-08-28). A broad R/a extrapolation of the law is
        unsupported: the circuit's geometry is the reference's, held.

        THE COMPRESSOR is isentropic compression from the compressor inlet at
        the isentropic efficiency eta_is, with the blanket inlet T_in held by
        the secondary-side cooling; T_comp_in is what the IHX must deliver, not
        evidence that it can (the exchanger is not sized here).

        ALL FLUID WORK IS RECOVERED into the IHX duty (the reference's own
        energy check: IHX duty 2231.1 - blanket heat 2101.7 = 129.4 MW against
        130.8 MW printed circulator power). eta_drive converts fluid work to
        electrical draw; an instance binding it to 1.0 reads the source's
        printed circulator figure as the boundary and its draw as a LOWER
        BOUND on the true electrical draw (drive losses a surfaced missing input).

        DORMANCY (packet section 3): loop_live 0 with the direct terms at the
        old held scalars gives p_pump_total = 0.0 * p_elec + p_pump_direct and
        q_recovered_total = 0.0 * w_fluid + eta_p_direct * p_pump_direct, which
        are the old scalars to the bit for finite p_elec and w_fluid; the power
        balance then reproduces the pre-WI-045 accounting exactly. The chain
        always evaluates; only what it hands to the power balance is switched.

        Constant ideal-gas helium properties (cp, gamma) over the reference
        window; the reference's own implied cp is 0.10 % under ideal helium.

        **Source**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md
            (Moscato et al., EUROfusion WPBOP-CPR(18) 20276); NASA compressor thermodynamics
            (w = cp T_in (r^((gamma-1)/gamma) - 1)/eta_is); NIST helium cp
        **Ref**: output.md:79 (8 MPa, 300-500 C), :81 (2101.7 MW, 2025.7 kg/s), :89-91 (9 loops),
            Table 1 :105-113 (two compressors per loop), Table 2 :128 (IHX duties), Table 3 :151-154
            (per-path losses, circulator power); raw.pdf p. 6 Table 3 (kPa basis)
        **Basis**: sized-flow representative circuit with a constant loss coefficient and an
            isentropic compressor; concept-agnostic (MR-3) -- every fact bound by instances
        */

        // reactor source heat, no pump credit [MW]
        in attribute q_source_in : Real;
        // blanket inlet (compressor discharge) temperature [K]
        in attribute T_in_in : Real;
        // blanket temperature rise [K], > 0
        in attribute dT_blanket_in : Real;
        // coolant specific heat [J/(kg K)], > 0
        in attribute cp_in : Real;
        // ratio of specific heats [1]
        in attribute gamma_in : Real;
        // loop nominal (compressor discharge) pressure [Pa], > dp_loop
        in attribute p_loop_in : Real;
        // number of parallel loops [1], an instance integer sized at the design point
        in attribute n_loops_in : Real;
        // reference per-loop flow [kg/s] -- the loss law's anchor and the rated capacity
        in attribute mdot_loop_ref_in : Real;
        // reference per-path pressure loss at the reference per-loop flow [Pa]
        in attribute dp_loop_ref_in : Real;
        // loss multiplier [1] (a study lever; 1.0 is the reference)
        in attribute f_loss_in : Real default 1.0;
        // compressor isentropic efficiency [1], 0 < eta_is <= 1
        in attribute eta_is_in : Real;
        // fluid-work to electrical-draw conversion [1], 0 < eta_drive <= 1
        in attribute eta_drive_in : Real default 1.0;
        // 1.0 = the loop feeds the power balance; 0.0 = dormant
        in attribute loop_live_in : Real default 0.0;
        // dormant-mode pump electrical draw [MW]
        in attribute p_pump_direct_in : Real default 0.0;
        // dormant-mode recovered fraction of that draw [1]
        in attribute eta_p_direct_in : Real default 0.0;

        out attribute mdot : Real = q_source_in * 1.0e6 / (cp_in * dT_blanket_in);
        out attribute T_out : Real = T_in_in + dT_blanket_in;
        out attribute mdot_loop : Real = mdot / n_loops_in;
        out attribute dp_loop : Real =
            f_loss_in * dp_loop_ref_in * (mdot_loop / mdot_loop_ref_in) ** 2;
        out attribute p_loop_margin : Real = p_loop_in - dp_loop;
        out attribute r_comp : Real = p_loop_in / (p_loop_in - dp_loop);
        attribute k_isen : Real = (gamma_in - 1.0) / gamma_in;
        out attribute T_comp_in : Real =
            T_in_in / (1.0 + (r_comp ** k_isen - 1.0) / eta_is_in);
        out attribute w_fluid : Real = mdot * cp_in * (T_in_in - T_comp_in) / 1.0e6;
        out attribute p_elec : Real = w_fluid / eta_drive_in;
        out attribute q_ihx : Real = q_source_in + w_fluid;
        out attribute capacity_margin : Real = mdot_loop_ref_in - mdot_loop;
        out attribute p_pump_total : Real = loop_live_in * p_elec + p_pump_direct_in;
        out attribute q_recovered_total : Real =
            loop_live_in * w_fluid + eta_p_direct_in * p_pump_direct_in;
    }
}
```

### New: `calc def 'Power Cycle Efficiency'` — `models/library/analyses/mfe_power_cycle.sysml` (D4, D13; handwritten stage)

```sysml
package mfe_power_cycle {
    private import ScalarValues::*;

    calc def 'Power Cycle Efficiency' {
        doc /*
        Secondary-cycle efficiency from the primary loop's outlet temperature by a
        printed fit (WI-045, goal plant-closure):

          T2_C           = T_hot - dT_approach - 273.15          [C]  (physical conversion)
          eta_fit        = a_fit * ln(T2_C + T_offset_fit) - b_fit - delta_eta   [1]
          eta_th         = cycle_live * eta_fit + eta_th_direct  [1]
          margin_low     = T2_C - T2_min                         [C]
          margin_high    = T2_max - T2_C                         [C]
          domain_product = margin_low * margin_high              [C^2]

        THE FIT'S VERSION CONTRACT: the printed Kovari et al. 2016 Table 4 form
        uses the literal 273 inside the logarithm (T_offset_fit); the physical
        273.15 converts the loop's kelvin outlet to the fit's Celsius argument.
        They are different numbers on purpose (the research section D). The
        fit is used literally; delta_eta is the printed low-temperature-divertor
        correction, bound 0 by an instance that carries no divertor loop, said so
        at the binding. The fit is a correlation on other codes' cycle modelling
        (Dostal, with the 0.0179 benchmark adjustment already inside the printed
        coefficients), not a measured plant efficiency.

        FAIL CLOSED: outside [T2_min, T2_max] the paired 'Cycle Fit Domain'
        constraint reads violated on domain_product; eta_fit is still published,
        never clamped or extrapolated silently. A non-positive logarithm argument
        raises in the executable.

        DORMANCY (packet section 3): cycle_live 0 with eta_th_direct at the old
        held efficiency gives eta_th = 0.0 * eta_fit + eta_th_direct, the old
        scalar to the bit.

        EXECUTABLE SEMANTIC (Rung B, the WI-029 CAS72 pattern): the logarithm is
        outside the codegen arithmetic envelope (+ - * / ** only), so this calc
        routes to the handwritten codegen stage (manual_required). The generated
        handwritten impl is normative and is guarded bit-exact (rel 1e-9) by the
        oracle mirror in verify_stellaris.py. The outputs are declared without
        expressions (a manual interface); the chain above is the model-resident
        statement.

        **Source**: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md
            (Kovari et al. 2016, FED 104, 9-20, DOI 10.1016/j.fusengdes.2016.01.007)
        **Ref**: output.md:355 (Table 4: the fitting functions, T2 ranges, T1-T2 approach);
            journal p. 17 render work/orchestration/goals/plant-closure/evidence/grounding_sources/kovari2016_p9_table4.png
        **Basis**: printed secondary-cycle efficiency correlation on the turbine-inlet temperature;
            concept-agnostic (MR-3) -- coefficients, domain and approach bound by instances
        */

        // primary loop outlet temperature [K]
        in attribute T_hot_in : Real;
        // primary-to-secondary approach at the hot end [K]
        in attribute dT_approach_in : Real;
        // fit slope [1]
        in attribute a_fit_in : Real;
        // fit intercept [1]
        in attribute b_fit_in : Real;
        // the fit's literal Kelvin offset [1] (273 as printed)
        in attribute T_offset_fit_in : Real;
        // fit domain, lower turbine-inlet temperature [C]
        in attribute T2_min_in : Real;
        // fit domain, upper turbine-inlet temperature [C]
        in attribute T2_max_in : Real;
        // low-temperature divertor correction [1] (0 when no divertor loop is modelled)
        in attribute delta_eta_in : Real default 0.0;
        // 1.0 = the fit feeds the power balance; 0.0 = dormant
        in attribute cycle_live_in : Real default 0.0;
        // dormant-mode thermal efficiency [1]
        in attribute eta_th_direct_in : Real default 0.0;

        // Manual interface on the exact route (see EXECUTABLE SEMANTIC in the doc).
        out attribute T2_C : Real;
        out attribute eta_fit : Real;
        out attribute eta_th : Real;
        out attribute margin_low : Real;
        out attribute margin_high : Real;
        out attribute domain_product : Real;
    }
}
```

### New: three `constraint def`s — `models/library/analyses/mfe_viability.sysml` (D11)

```sysml
    constraint def 'Loop Pressure Margin' {
        doc /*
        Primary-loop pressure domain (WI-045): the per-path pressure loss must
        stay below the loop's nominal pressure, so the compressor pressure ratio
        p_loop / (p_loop - dp_loop) is finite and positive. A domain condition of
        the constant-loss-coefficient law, not a sourced operating limit; the
        operand is computed by 'Primary Coolant Loop'.
        **Source**: models/library/analyses/mfe_primary_loop.sysml
        **Ref**: r_comp = p_loop / (p_loop - dp_loop)
        **Basis**: p_loop - dp_loop > 0, the law's own domain
        */
        // loop pressure less the per-path loss [Pa] (computed)
        in attribute p_loop_margin_in : Real;
        p_loop_margin_in > 0.0
    }

    constraint def 'Loop Capacity' {
        doc /*
        Primary-loop capacity (WI-045): the per-loop mass flow must not exceed
        the rated per-loop flow -- the reference circuit's own per-loop flow, at
        which its compressors and exchangers were sized. A plant whose source heat
        outgrows its loop count must add loops (a study lever) rather than run
        each loop past its rating; the draw is cubic in the per-loop flow, so this
        is the fence through which coolant choices push back on feasibility (rubric
        Row 7's P3 anchor). Both operands are the loop's: the computed per-loop
        flow and the instance's rated flow.
        **Source**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md
        **Ref**: output.md:81 (2025.7 kg/s), :89-91 (9 loops): 225.08 kg/s per loop
        **Basis**: mdot_loop <= the reference per-loop flow
        */
        // computed per-loop mass flow [kg/s]
        in attribute mdot_loop_in : Real;
        // rated per-loop mass flow [kg/s]
        in attribute mdot_loop_rated_in : Real;
        mdot_loop_in <= mdot_loop_rated_in
    }

    constraint def 'Cycle Fit Domain' {
        doc /*
        Secondary-cycle fit domain (WI-045): the turbine-inlet temperature must
        lie inside the printed fit's range, read as the product of the two margins
        (T2 - T2_min)(T2_max - T2) >= 0 -- one constraint for a two-sided bound,
        valid because T2_min < T2_max. Outside the domain the fit is not evidence;
        the point reads violated and its efficiency is published, never clamped.
        **Source**: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md
        **Ref**: output.md:355 (Table 4 T2 ranges: 384-642 C helium Rankine; 135-750 C sCO2)
        **Basis**: the fit's stated validity interval
        */
        // (T2 - T2_min) * (T2_max - T2) [C^2] (computed)
        in attribute domain_product_in : Real;
        domain_product_in >= 0.0
    }
```

### Changed: `models/designs/generic_mfe/mfe_plant.sysml` (D9, D10)

Imports gain `private import mfe_primary_loop::*;` and `private import mfe_power_cycle::*;`. At lines 413–421 the attributes `eta_th`, `eta_p`, `p_pump` retire and this block replaces them (the `mn` and `f_sub` attributes stay):

```sysml
        // ---- Primary loop and cycle (WI-045, goal plant-closure) ----
        // The loop and the cycle are computed producers; the five attributes
        // below select the mode. Dormant defaults: a concept that binds no
        // circuit reads no loop and zero efficiency and MUST bind its own direct
        // terms (the WI-039 EI-5 lesson) -- the mode is selected by the flags,
        // never by a fact. Every circuit and fit fact is unbound here (the
        // WI-044 D6 convention) and bound by the concrete instance.
        attribute loop_live : Real default 0.0;
        attribute cycle_live : Real default 0.0;
        attribute p_pump_direct : Real default 0.0;
        attribute eta_p_direct : Real default 0.0;
        attribute eta_th_direct : Real default 0.0;
        // circuit facts (instance-bound)
        attribute loop_T_in : Real;
        attribute loop_dT_blanket : Real;
        attribute loop_cp : Real;
        attribute loop_gamma : Real;
        attribute loop_p : Real;
        attribute n_loops : Real;
        attribute mdot_loop_ref : Real;
        attribute dp_loop_ref : Real;
        attribute f_loss : Real default 1.0;
        attribute eta_is : Real;
        attribute eta_drive : Real default 1.0;
        // fit facts (instance-bound)
        attribute dT_approach : Real;
        attribute a_fit : Real;
        attribute b_fit : Real;
        attribute T_offset_fit : Real;
        attribute T2_min : Real;
        attribute T2_max : Real;
        attribute delta_eta : Real default 0.0;

        calc source_heat : 'Reactor Source Heat' {
            in p_nrl = fusion.p_fus;
            in p_input_in = heat.p_coupled;
            in mn_in = mn;
        }
        calc loop : 'Primary Coolant Loop' {
            in q_source_in = source_heat.q_source;
            in T_in_in = loop_T_in;
            in dT_blanket_in = loop_dT_blanket;
            in cp_in = loop_cp;
            in gamma_in = loop_gamma;
            in p_loop_in = loop_p;
            in n_loops_in = n_loops;
            in mdot_loop_ref_in = mdot_loop_ref;
            in dp_loop_ref_in = dp_loop_ref;
            in f_loss_in = f_loss;
            in eta_is_in = eta_is;
            in eta_drive_in = eta_drive;
            in loop_live_in = loop_live;
            in p_pump_direct_in = p_pump_direct;
            in eta_p_direct_in = eta_p_direct;
        }
        calc cycle : 'Power Cycle Efficiency' {
            in T_hot_in = loop.T_out;
            in dT_approach_in = dT_approach;
            in a_fit_in = a_fit;
            in b_fit_in = b_fit;
            in T_offset_fit_in = T_offset_fit;
            in T2_min_in = T2_min;
            in T2_max_in = T2_max;
            in delta_eta_in = delta_eta;
            in cycle_live_in = cycle_live;
            in eta_th_direct_in = eta_th_direct;
        }
```

The `pb` usage at 489–504 changes three lines: `in eta_th_in = cycle.eta_th;`, `in q_recovered_in = loop.q_recovered_total;` (replacing `in eta_p_in = eta_p;`), `in p_pump_total_in = loop.p_pump_total;` (replacing `in p_pump_in = p_pump;`). Beside the existing asserts (1054–1077):

```sysml
        // WI-045: the loop's two domain/capacity fences and the cycle's domain fence.
        assert constraint loop_pressure_ok : 'Loop Pressure Margin' {
            in p_loop_margin_in = loop.p_loop_margin;
        }
        assert constraint loop_capacity_ok : 'Loop Capacity' {
            in mdot_loop_in = loop.mdot_loop;
            in mdot_loop_rated_in = mdot_loop_ref;
        }
        assert constraint cycle_domain_ok : 'Cycle Fit Domain' {
            in domain_product_in = cycle.domain_product;
        }
```

### Changed: `models/designs/stellarator_09/stellarator_plant.sysml` (D1, D2, D10, D15)

Lines 779–808 (`eta_th`, `eta_p`, `p_pump` with the WI-033 doc) are replaced by the block below; the WI-033 doc's substance moves to `p_pump_direct`'s comment where the held value now lives.

```sysml
        // ---- Primary loop and cycle (WI-045, goal plant-closure) ----
        // LIVE: the loop and the fit feed the power balance. The compatibility
        // arm of the round's study sets loop_live 0, cycle_live 0, p_pump_direct
        // 195.0, eta_p_direct 0.5, eta_th_direct 0.333 and reproduces the
        // WI-044 pin bit-for-bit (goal plant-closure, packet section 3).
        :>> loop_live = 1.0;
        :>> cycle_live = 1.0;
        :>> p_pump_direct = 0.0 {  // the held 195.0 MW lives here in the dormant mode.
            doc /*
            Dormant-mode primary pump electrical draw [MW]. Zero while the loop
            is live. The value the compatibility arm binds is the WI-033 held
            figure, 195.0 MW -- 6 % of the then-baseline p_th 3238.1 MW, landed
            rounded [OWNER 2026-08-28] as a HELD, SETTABLE INPUT (goal p-pump-basis
            Ruling 2: a fraction of p_th would assert a linearity across swept
            (R, a) no source establishes), with ~130 MW the documented lower bound
            (Ruling 3; Moscato's near-term 8-loop layout). WI-045 replaces the
            held scalar by a hydraulic law (mdot^3 / n_loops^2 at fixed count) --
            not the rejected fraction -- under the concept correction
            [OWNER 2026-09-01] that a real loop calculation needs no reopening of
            WI-033; the 195.0 MW stays as this term and as the study's named
            historical comparison arm.
            **Source**: work/orchestration/goals/p-pump-basis/trail.md (Goal close, Rulings 2-3);
                .project/concepts/stellarator-demo-maturation.md (Corrections 2026-09-01)
            **Ref**: WI-033 spec line 22 (the reason of record); Moscato output.md:145-154
            **Basis**: the pre-WI-045 held value, kept for the attribution bridge
            */
        }
        :>> eta_p_direct = 0.0 {  // the held 0.5 lives here in the dormant mode.
            doc /* **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml **Ref**: steady_state_stellarator.yaml:14 (eta_p = 0.5) **Basis**: the pre-WI-045 pumping-heat capture fraction; zero while the loop recovers its own fluid work */
        }
        :>> eta_th_direct = 0.0 {  // the held 0.333 lives here in the dormant mode.
            doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md **Ref**: line 251 (single-element conversion efficiency 1/3) **Basis**: the source's simple 1/3 assumption -- it names no cycle (the earlier comment's "steam-cycle" overstated it); the pre-WI-045 held efficiency, kept for the attribution bridge */
        }
        // The representative circuit: EU DEMO HCPB's (Moscato 2017), transferred
        // at fixed circuit with the loop count sized at the design point. NOT
        // Stellaris' layout: the paper's own thermal statement is local -- 350 C
        // inlet and under 370 C outlet on one plasma-facing first-wall segment
        // (raw PDF p. 16 sec. 2.7, Fig. 27) -- and its conclusion lists pumping
        // estimates as future work (p. 31). HCPB's PHTS is representative of
        // HCLL (Cismondi output.md:172), Stellaris' blanket class.
        :>> loop_T_in = 573.15 {  // 300 C blanket inlet [K].
            doc /* **Source**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md **Ref**: output.md:79 (helium at 8 MPa and 300 C ... outlet manifold at 500 C; the 300-500 C EUROFER window) **Basis**: the reference circuit's blanket inlet */
        }
        :>> loop_dT_blanket = 200.0 {  // 300 -> 500 C [K].
            doc /* **Source**: same **Ref**: output.md:79 **Basis**: the reference circuit's blanket rise; held, so the outlet is 500 C by construction and the flow follows the heat */
        }
        :>> loop_cp = 5193.0 {  // ideal helium [J/(kg K)].
            doc /* **Source**: NIST JANAF helium (cp 20.786 J/(mol K)); NIST WebBook (M 4.002602 g/mol) **Ref**: research 20260907-163520_primary-loop-cycle-closure-prework.md section D line 86 **Basis**: ideal-gas helium; the reference's own implied cp is 5187.6 (0.10 % under), reported by the reconstruction, not fitted */
        }
        :>> loop_gamma = 1.6666666666666667 {  // monatomic ideal gas [1].
            doc /* **Source**: NASA compressor thermodynamics **Ref**: research section D line 84 **Basis**: gamma = 5/3 for helium */
        }
        :>> loop_p = 8000000.0 {  // 8 MPa [Pa].
            doc /* **Source**: Moscato output.md **Ref**: output.md:79 **Basis**: the reference circuit's pressure */
        }
        :>> n_loops = 14.0 {  // sized at the design point, then held.
            doc /*
            The smallest integer for which the design point's per-loop flow does
            not exceed the reference per-loop flow: 3010.64 / 225.08 = 13.38 -> 14
            (per-loop 215.05 kg/s, 4.5 % under the rating). A settable input and a
            study lever, never a computed ceil (outside the codegen envelope and a
            size optimizer the goal does not authorize). Off the design point a
            bigger plant exceeds the rating at this count and must add loops:
            the committed cheapest machine c2823 needs 27.
            **Source**: prototype/proto.py (the sizing rule on the reference's 2025.7 kg/s over 9 loops)
            **Ref**: Moscato output.md:81, :89-91
            **Basis**: capacity by count, sized once at the design point
            */
        }
        :>> mdot_loop_ref = 225.07777777777778 {  // 2025.7 / 9 [kg/s], the rated per-loop flow.
            doc /* **Source**: Moscato output.md **Ref**: output.md:81 (2025.7 kg/s), :89-91 (9 loops) **Basis**: the reference per-loop flow; the loss law's anchor and 'Loop Capacity''s rating */
        }
        :>> dp_loop_ref = 329187.1856931558 {  // flow-weighted per-path loss [Pa].
            doc /*
            The IB path 214 + 62 + 87.9 = 363.9 kPa and the OB path 174 + 56.6 +
            85.1 = 315.7 kPa (in-vessel, ex-vessel piping, IHX -- Table 3's kPa
            basis; Table 2 prints the IHX row's unit as MPa, the source's own
            inconsistency, cited not corrected), weighted by IHX duty over 3 IB
            and 6 OB loops (weighting by flow share at the common 200 K rise):
            (3*208.1*363.9 + 6*267.8*315.7) / 2231.1 = 329.187 kPa. Each path is
            a serial sum; the two paths are parallel and never added.
            **Source**: Moscato output.md; raw.pdf p. 6
            **Ref**: Table 3 :151-154; Table 2 :128
            **Basis**: the representative path's loss at the reference per-loop flow (design D1)
            */
        }
        :>> f_loss = 1.0;
        :>> eta_is = 0.772796639536644 {  // SOURCE-POINT CALIBRATION, not a validation.
            doc /*
            The isentropic efficiency at which the reference circuit's fluid work
            on this calc's own compressor form equals the source's energy check:
            IHX duty 2231.1 - blanket heat 2101.7 = 129.4 MW at 2025.7 kg/s, i.e.
            a 12.301 K compressor rise from 560.85 K to 573.15 K against the
            isentropic 9.506 K at pressure ratio 8 / (8 - 0.3292):
            eta_is = (r^0.4 - 1) * T1 / dT = 0.772796639536644. The same number
            fits this efficiency and is therefore NOT evidence for it; the
            reconstruction (SV row) is a reconstruction of the source's arithmetic
            at the source's point. The 130.8 MW printed circulator total stands
            1.4 MW above the fluid work and is not folded in (design D2).
            **Source**: Moscato output.md
            **Ref**: Table 2 :128 (IHX duties), :81 (blanket heat, flow), Table 3 :151-154
            **Basis**: source-point calibration on the reference's own energy check
            */
        }
        :>> eta_drive = 1.0 {  // the source's printed circulator boundary; a LOWER BOUND.
            doc /*
            The source prints one circulator figure per unit (6.8 IB / 7.5 OB MW)
            whose motor/shaft boundary it does not resolve; the total 130.8 MW
            agrees with the fluid work (129.4 MW) within 1.4 MW, so the printed
            figure is read as the fluid-work boundary and the electrical draw is
            the fluid work -- a lower bound on the true draw (drive losses are a
            surfaced missing input; retrieval target: Moscato's preliminary
            circulator design). The WI-033 documented-lower-bound pattern.
            **Source**: Moscato output.md
            **Ref**: Table 3 :154 (circulator power 6.8 / 7.5 MW)
            **Basis**: printed boundary; no admissible drive efficiency
            */
        }
        // The cycle: Kovari et al. 2016 Table 4, helium-primary steam Rankine row.
        :>> dT_approach = 20.0 {  // T1 - T2 [K].
            doc /* **Source**: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md **Ref**: output.md:355 (Table 4, T1-T2 = 20 C for the helium row); render kovari2016_p9_table4.png **Basis**: the fit's stated primary-to-secondary approach; one approach only -- the reference's HITEC intermediate loop is not modelled (design D4) */
        }
        :>> a_fit = 0.1802 {
            doc /* **Source**: same **Ref**: output.md:355 (0.1802 ln(T2 + 273) - 0.7823 - delta_eta) **Basis**: the printed helium-primary Rankine fit, used literally */
        }
        :>> b_fit = 0.7823 {
            doc /* **Source**: same **Ref**: output.md:355 **Basis**: as a_fit */
        }
        :>> T_offset_fit = 273.0 {  // the fit's literal, not the physical 273.15.
            doc /* **Source**: same **Ref**: output.md:355 (ln(T2 + 273)) **Basis**: the printed fit convention (research section D: "the literal 273 is a fit convention, not a replacement for physical Celsius-to-kelvin conversion elsewhere") */
        }
        :>> T2_min = 384.0 {
            doc /* **Source**: same **Ref**: output.md:355 (T2 range 384-642 C) **Basis**: the fit's stated domain */
        }
        :>> T2_max = 642.0 {
            doc /* **Source**: same **Ref**: output.md:355 **Basis**: the fit's stated domain */
        }
        :>> delta_eta = 0.0 {  // no low-temperature divertor loop in the model.
            doc /* **Source**: same **Ref**: output.md:355 (the -delta_eta term; the text: divertor heat used in a separate feedwater preheater for Rankine) **Basis**: not applied -- the model carries no divertor coolant loop; the sCO2 row (0.4347 ln(T2 + 273) - 2.5043, 135-750 C) is a study arm on the same heat, not a second live cycle */
        }
```

The turbine part's doc (line 421) is corrected to "The per-MW rate is the 1costingFE RANKINE preset's; the cycle's efficiency is computed by 'Power Cycle Efficiency' on Kovari 2016's helium-primary Rankine row (WI-045) — the Stellaris paper assumes a simple 1/3 and names no cycle." One disclosure block is added beside the circuit facts, carrying spec MR-WI045-14 (a)–(g) in one place.

### Twins

`exploration/stellarator_e2e/models/analyses/{mfe_power_balance,mfe_primary_loop,mfe_power_cycle,mfe_viability}.sysml`, `designs/generic_mfe/mfe_plant.sysml`, `designs/stellarator_09/stellarator_plant.sysml` — copied byte-for-byte (plan phase 1).

### New: `exploration/stellarator_e2e/generated/handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py` (D13; the normative body, restored over the stencil)

```python
"""Handwritten implementation for Power_Cycle_Efficiency (WI-045, goal plant-closure; Rung B).

AUTO_IMPLEMENTED = False  (hand-written, normative -- do not regenerate over
this file; the bridge sets preserve_handwritten=True. When the calc's
interface changes the generator re-stencils it and this body is restored by
hand, then the package is regenerated a second time -- WI-041's recipe.)

SysML Source: models/analyses/mfe_power_cycle.sysml ('Power Cycle Efficiency')

Executable semantic (normative, per the calc doc):

  T2_C           = T_hot - dT_approach - 273.15          [C]  physical conversion
  eta_fit        = a_fit * ln(T2_C + T_offset_fit) - b_fit - delta_eta
  eta_th         = cycle_live * eta_fit + eta_th_direct
  margin_low     = T2_C - T2_min
  margin_high    = T2_max - T2_C
  domain_product = margin_low * margin_high

THE FIT IS USED LITERALLY: T_offset_fit is the printed 273 inside the
logarithm (Kovari et al. 2016 Table 4), a fit convention distinct from the
physical 273.15 that converts the loop's kelvin outlet to Celsius. Nothing is
clamped: outside the domain 'Cycle Fit Domain' reads violated on
domain_product and eta_fit is still published; a non-positive logarithm
argument raises (fail closed, never a plausible number).

DORMANCY: cycle_live 0 gives eta_th = 0.0 * eta_fit + eta_th_direct, the
pre-WI-045 held scalar to the bit.

The oracle mirror in verify_stellaris.py re-derives this chain independently
and run_stellaris_single.py asserts agreement at rel 1e-9.

Return-tuple order matches the regenerated caller's unpack
(modules/mfe_power_cycle/power_cycle_efficiency.py) -- read from the stencil
at the regeneration and verified there (the WI-042 precedent).

Source: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md
Ref:    output.md:355 (Table 4); journal p. 17
Basis:  printed secondary-cycle efficiency correlation on the turbine-inlet temperature
"""

import math

from stellarator_tea.modules.mfe_power_cycle.power_cycle_efficiency import (
    Power_Cycle_EfficiencyInput,
)

AUTO_IMPLEMENTED = False


def power_cycle_efficiency(
    T_hot: float,
    dT_approach: float,
    a_fit: float,
    b_fit: float,
    T_offset_fit: float,
    T2_min: float,
    T2_max: float,
    delta_eta: float,
    cycle_live: float,
    eta_th_direct: float,
) -> tuple[float, float, float, float, float, float]:
    """The fit, its dormant form and its domain margins. Pure float64; no clamping."""
    T2_C = T_hot - dT_approach - 273.15
    eta_fit = a_fit * math.log(T2_C + T_offset_fit) - b_fit - delta_eta
    eta_th = cycle_live * eta_fit + eta_th_direct
    margin_low = T2_C - T2_min
    margin_high = T2_max - T2_C
    domain_product = margin_low * margin_high
    return (T2_C, eta_fit, eta_th, margin_low, margin_high, domain_product)


def run_power_cycle_efficiency(inputs: Power_Cycle_EfficiencyInput):
    """Execute Power_Cycle_Efficiency -- returns the six outputs in the caller's order."""
    return power_cycle_efficiency(
        T_hot=inputs.T_hot_in,
        dT_approach=inputs.dT_approach_in,
        a_fit=inputs.a_fit_in,
        b_fit=inputs.b_fit_in,
        T_offset_fit=inputs.T_offset_fit_in,
        T2_min=inputs.T2_min_in,
        T2_max=inputs.T2_max_in,
        delta_eta=inputs.delta_eta_in,
        cycle_live=inputs.cycle_live_in,
        eta_th_direct=inputs.eta_th_direct_in,
    )
```

The tuple order `(T2_C, eta_fit, eta_th, margin_low, margin_high, domain_product)` is the declaration order; if the regenerated caller unpacks in another order the return is reordered to the caller's, never the caller edited.

### Changed: `exploration/stellarator_e2e/verify_stellaris.py`, `studies/oracle_entry.py` (D12; plan phase 3)

`IN`: −`eta_th`, `eta_p`, `p_pump`; +`loop_live=1.0, cycle_live=1.0, p_pump_direct=0.0, eta_p_direct=0.0, eta_th_direct=0.0`, +`loop_T_in=573.15, loop_dT_blanket=200.0, loop_cp=5193.0, loop_gamma=1.6666666666666667, loop_p=8.0e6, n_loops=14.0, mdot_loop_ref=225.07777777777778, dp_loop_ref=329187.1856931558, f_loss=1.0, eta_is=0.772796639536644, eta_drive=1.0`, +`dT_approach=20.0, a_fit=0.1802, b_fit=0.7823, T_offset_fit=273.0, T2_min=384.0, T2_max=642.0, delta_eta=0.0`. `compute()` between the heating chain and `p_th`: `q_source = p["mn"] * p_neutron + p_alpha + heat_coupled`; the loop chain and the cycle chain written from § Proposed design (the prototype's `loop()` and `cycle()` are the same statements); then `p_th = p["mn"] * p_neutron + p_alpha + heat_coupled + q_recovered_total`, `p_the = eta_th * p_th`, `recirculating = p_coils + p_pump_total + p_sub + p_aux + p_cool + p_cryo + heat_wallplug_total`. The return dict gains `q_source`, `loop_mdot`, `loop_T_out`, `loop_mdot_loop`, `loop_dp_loop`, `loop_p_loop_margin`, `loop_r_comp`, `loop_T_comp_in`, `loop_w_fluid`, `loop_p_elec`, `loop_q_ihx`, `loop_capacity_margin`, `loop_p_pump_total`, `loop_q_recovered_total`, `cycle_T2_C`, `cycle_eta_fit`, `cycle_eta_th`, `cycle_margin_low`, `cycle_margin_high`, `cycle_domain_product`. `oracle_entry.py`: `ENTRY_KEY_TO_ORACLE_INPUT` −`eta_th` +the 23 keys (D7 marks which are study levers in its comment); `ORACLE_OUTPUT_TO_CHANNEL` +the channels above under `source_heat__`, `loop__`, `cycle__`; `OPERAND_BINDINGS` +`loop_pressure_ok` (`p_loop_margin_in` → `loop__p_loop_margin`), `loop_capacity_ok` (`mdot_loop_in` → `loop__mdot_loop`; `mdot_loop_rated_in` → input `mdot_loop_ref`), `cycle_domain_ok` (`domain_product_in` → `cycle__domain_product`), ids from the contract.

### Re-derived (plan phase 4)

`stellarator.snapshot.json`; `studies/manifest.json` (three fingerprints; `baseline.verdicts` +3 = 13; `baseline.headline.value` re-pinned from the live execution, expected 237.25280024209582); `tests/models/data/mfe_census.json` (expect 229); the six `tests/study/data/*.expected.json`; `test_known_answers.py`; the count sites; `generated/**`.

## Cross-file bindings

| Input | Bound to | Source file |
|---|---|---|
| `source_heat.{p_nrl, p_input_in, mn_in}` | `fusion.p_fus`, `heat.p_coupled`, `mn` | `mfe_plant.sysml` |
| `loop.q_source_in` | `source_heat.q_source` | `mfe_plant.sysml` |
| `loop.{T_in_in … eta_drive_in}` | the eleven circuit attributes | instance bindings |
| `loop.{loop_live_in, p_pump_direct_in, eta_p_direct_in}` | `loop_live`, `p_pump_direct`, `eta_p_direct` | instance (live) / study levers (held) |
| `cycle.T_hot_in` | `loop.T_out` | `mfe_plant.sysml` |
| `cycle.{dT_approach_in … delta_eta_in}` | the seven fit attributes | instance bindings |
| `cycle.{cycle_live_in, eta_th_direct_in}` | `cycle_live`, `eta_th_direct` | instance / levers |
| `pb.eta_th_in` | `cycle.eta_th` | `mfe_plant.sysml` |
| `pb.q_recovered_in` | `loop.q_recovered_total` | `mfe_plant.sysml` |
| `pb.p_pump_total_in` | `loop.p_pump_total` | `mfe_plant.sysml` |
| `loop_pressure_ok.p_loop_margin_in` | `loop.p_loop_margin` | `mfe_plant.sysml` |
| `loop_capacity_ok.{mdot_loop_in, mdot_loop_rated_in}` | `loop.mdot_loop`, `mdot_loop_ref` | `mfe_plant.sysml` |
| `cycle_domain_ok.domain_product_in` | `cycle.domain_product` | `mfe_plant.sysml` |

Dataflow: `fusion`, `heat` → `source_heat` → `loop` → `cycle` → `pb` → the cost spine and `net_positive` / `recirc_ok`. No edge from `pb` back to the loop.

## Expected baseline behaviour (MR-WI045-10, -11; stated before regeneration; `prototype/proto_results.json`)

**Held mode** (the compatibility proposal: `loop_live` 0.0, `cycle_live` 0.0, `p_pump_direct` 195.0, `eta_p_direct` 0.5, `eta_th_direct` 0.333, every other lever at the instance's value): `loop__q_recovered_total = 97.5` and `loop__p_pump_total = 195.0` and `cycle__eta_th = 0.333` exactly (`held_mode_identity`: `q_recovered_eq`, `p_pump_total_eq`, `eta_th_eq` all `True`); `pb__p_th = 3224.352676294579`, `recirculating` and `q_eng` equal to the entering pin's (`p_th_new_vs_oracle`, `recirc_eq`, `q_eng_eq` `True`); **every one of the entering pin's 106 channels bit-identical, the old ten verdicts unchanged, LCOE 322.31843948570247**; the three new verdicts read on the live-computed loop and cycle: `loop_pressure_ok` satisfied, `loop_capacity_ok` satisfied, `cycle_domain_ok` satisfied. New channels present: `source_heat__q_source = 3126.852676294579`, the loop's and the cycle's (below).

**Live mode** (the instance as bound; the manifest's baseline after this item):

| Channel | Value |
|---|---|
| `source_heat__q_source` | 3126.852676294579 MW |
| `loop__mdot` / `loop__mdot_loop` / `loop__capacity_margin` | 3010.6418989934327 / 215.04584992810234 / 10.03192784967544 kg/s |
| `loop__T_out` / `loop__T_comp_in` | 773.15 / 561.9287138794313 K |
| `loop__dp_loop` / `loop__p_loop_margin` / `loop__r_comp` | 300496.77482532675 / 7699503.225174673 Pa / 1.0390280731155237 |
| `loop__w_fluid` = `loop__p_elec` = `loop__p_pump_total` = `loop__q_recovered_total` | 175.4365426878376 MW (5.61 % of `q_source`) |
| `loop__q_ihx` = `pb__p_th` | 3302.2892189824165 MW |
| `cycle__T2_C` / `cycle__eta_fit` = `cycle__eta_th` | 480.0 °C / 0.41135655404954075 |
| `cycle__margin_low` / `cycle__margin_high` / `cycle__domain_product` | 96.0 / 162.0 / 15552.0 |
| `pb__p_et` / `pb__p_net` / `pb__q_eng` / `pb__rec_frac` | 1358.4183135955561 / 1012.3648698998519 / 3.9254581578158096 / 0.2547473338899163 |
| `cas72_calc__cost` / `total_capital` | 128437178.4450173 $/yr / 14955212350.386 $ |
| `lcoe_calc__lcoe` / `lcoe_1cfe_calc__lcoe` | **237.25280024209582** / 232.72488725077486 $/MWh (held availability 0.85) |
| loop only / cycle only (oracle, for the attribution) | 305.8147241377531 / 247.70504890284698 $/MWh |
| sCO2 arm on the same heat | `eta_fit` 0.37518115452461354 (margins 345 / 270) |
| Verdicts | thirteen satisfied; `net_positive` and `recirc_ok` gain margin; `wall_load_peak`, `B_peak`, `beta`, `p_aux_required` bit-identical to the pin |

The energy check closes (`q_ihx == q_source + w_fluid`; `p_elec == w_fluid`). If any existing channel differs in held mode, the implementation stops and derives why; nothing is tuned (`goal.md` § Invariants).

## Off-design predictions (MR-WI045-11; `prototype/proto_results.json`; the implementation executes them, live mode)

| Point | Levers | `q_source` [MW] | `mdot_loop` [kg/s] | `dp_loop` [kPa] | `p_elec` [MW] | `eta_th` | `p_net` [MW] | `rec_frac` | LCOE live / held [$/MWh] | New verdicts | Other fences that move |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 design column, `a` 1.4 | R 12.7, a 1.4, 15.4 MA, the baseline's `n_e0`, `T_i0`, 100 MW; 14 loops | 3317.267553799019 | 228.1414234683378 | 338.2096364963469 | 209.66570510819685 | 0.41135655404954075 | 1067.7722416861886 | 0.26402516671983356 | 231.32525675570017 / 304.8952318776791 | `loop_capacity_ok` **violated** (margin −3.06); pressure, domain satisfied | none (`peak_field_ok` violated as at the pin, 25.163 T) |
| P3 `c2823`, 14 loops | R 15.7, a 2.2, 13 MA, 13 keV, n 1.0×, 100 MW | 6271.340445165246 | 431.30453393065153 | 1208.7757277886579 | 1447.9729180478694 | 0.41135655404954075 | 1502.2763876461277 | 0.5269002172397199 | 250.52954946775412 / 202.16521550623165 | `loop_capacity_ok` **violated** (−206.23); pressure (6.79 MPa margin), domain satisfied | `recirc_ok` **violated** (0.527 > 0.5) |
| P4 `c2823`, 27 loops | as P3 with `n_loops` 27 (⌈6038.26 / 225.08⌉) | 6271.340445165246 | 223.63938796404156 | 324.9931997895433 | 380.7670505420672 | 0.41135655404954075 | 2143.6501908768514 | 0.21661322229463523 | 171.23178310298275 / 202.16521550623165 | all three satisfied (margin +1.44) | none |

At every point the plasma, wall and magnet channels equal the entering pin's at the same coordinates (`p_fus`, `wall_load_peak`, `B_peak`, `beta`, `p_aux_required` identical in the prototype's held and live evaluations); the moves are the loop's and the cycle's. The capacity threshold at 14 loops is `q_source` 3272.72 MW (4.66 % above the design point): the fence catches almost every committed point off the design column at the instance's count, and the round's study must carry the count as a lever (D6).

## Validation plan

1. Levels 1–3 on `models/` with no new Level 2 warning; Levels 4–6 residue equal to the pre-change run (Level 6: 236 issues / 207 design attrs at WI-044) or the delta explained (23 new design attrs expected).
2. `tests/models` after the twin sync: 48 / 13 or better with every delta explained (the census test will fail on the fingerprint until phase 4).
3. Regeneration: `New: 4` (source heat, loop, cycle modules and the cycle stencil), `Regenerated` on the power balance and the plant (interfaces changed) — every existing handwritten impl preserved byte-identical, then the cycle stencil restored and the package regenerated a second time (`New: 0, Regenerated: 0`, no `backup/`, seal clean); the WI-044 stale-stencil checker run over every AUTO stencil (0 stale) because the power balance's expressions changed with its interface.
4. The held-mode identity: the compatibility proposal through `study_route.run_points` at the baseline levers, every entering-pin channel bit-identical, the old ten verdicts unchanged (`evidence/compat_mode/`).
5. The live baseline: `execute_baseline` → every channel at the table above to 1e-9 relative; the single runner 13 / `full_satisfaction` with the oracle gate bit-exact on every channel including the twenty new ones.
6. P1, P3, P4 through `run_points`; the loop and cycle channels at the predictions to 1e-9; the oracle seam at 0.0 relative deviation; the three new verdicts and `recirc_ok` re-derived through `OPERAND_BINDINGS` agree with the package.
7. The reference reconstruction in the oracle's own arithmetic (a function beside `compute()`): 2101.7 MW at 2025.7 kg/s over 200 K with `cp` 5193 (the 0.10 % discrepancy reported), 363.9 / 315.7 / 329.187 kPa, 2231.1 MW, 129.4 against 130.8 printed, `w_fluid` 129.4 at `eta_is` 0.772796639536644 to 1e-12 MW.
8. Synthetic fail-closed cases in the oracle and the package: `T_hot` 623.15 K (the Stellaris local 350 °C) → `domain_product` −16848 → `cycle_domain_ok` violated with `eta_fit` 0.3713 published; `n_loops` 7 → `capacity_margin` −205.01 → `loop_capacity_ok` violated with `p_elec` 717.77.
9. Re-pin by producers; census 229; fixtures re-derived; `tests/study` green apart from the known fail-closed set (86 at entry).
10. SV-063 (held-mode identity), SV-064 (the reference reconstruction), SV-065 (the live baseline and P1 / P3 / P4 with oracle parity and verdict re-derivation) `passing`; trace rows for the three calcs, the three constraints and each instance-bound fact.

## Validation report (prototype, 2026-09-08)

- `prototype/proto.py` → `proto_results.json`: the reference reconstruction closes (`w_fluid_reproduced_MW` 129.4000000000004, residual −1.4e-13; `cp_discrepancy` −0.00104; the OB and IB paths' calibrations 0.7402 / 0.8570 beside the weighted 0.7728); `held_mode_identity` every check `True` (`q_recovered_eq`, `p_pump_total_eq`, `eta_th_eq`, `p_th_new_vs_oracle`, `p_th_old_form_eq`, `recirc_eq`, `q_eng_eq`); the live design point, P1, P3, P4 as tabled; the synthetic cases; the largest committed plasma (`c3598`, `q_source` 6978.9 MW) finite in every loop channel, so the dormant `0.0 · x` is exactly 0.0 everywhere on the window. No SysML was validated (no model file is touched by this task); the codegen envelope facts rest on the renderer's operator map and the WI-044 precedent (`** 0.78`, chained outputs, one intermediate).
- Files created: `design.md`, `prototype/proto.py`, `prototype/proto_results.json`, `plan.md`.

## Implementation checklist (phased; the plan carries the checkboxes)

1. The model edits from § Proposed design in the tracked tree; Levels 1–3; twins synced; `tests/models`.
2. The MR-WI045-16 restatement and the predictions in the plan; `evidence/baseline_before/`; commit A.
3. Regeneration (twice, the stencil restored between); the stale-stencil check; the oracle and the seam (D12); the single runner (13, +3 expected verdicts); the held-mode identity; the live baseline diff; P1 / P3 / P4; the synthetic cases.
4. Re-pin (snapshot → manifest → census → fixtures → single runner); the count sites; batteries; SV and trace rows; commit B.
5. `tests/study` run of record; commit C.

## Risks

1. **The dormant `0.0 · x` meets a non-finite `x`.** *Likelihood: very low on the window* (the largest committed plasma is finite); `dp_loop ≥ p_loop` needs a per-loop flow 5.16× the design point's at 14 loops (`synthetic.dp_at_p_loop_margin_zero_flow_multiple`). A non-finite loop value would read as a moved channel in the compatibility arm — a premise surprise, stopped, never tuned.
2. **Codegen orders the modules by dependency and the cycle is broken by D3.** *Confidence: high.* If the generator still reports a cycle, that is a `PREREQUISITE` naming codegen, not a scope change.
3. **The power balance's AUTO stencil is preserved stale** (its expression changed with its interface — the WI-044 § 10 finding was expression-only; here the interface also changes, so re-stencilling is expected). *Mitigation:* the stale-stencil checker after every regeneration.
4. **The fractional power with a computed exponent (`r_comp ** k_isen`).** *Confidence: high* (`**` with an attribute operand is inside the map). Settled by the first Level-3 / regeneration pass.
5. **The manifest's baseline headline moves twice more in the round** (WI-046, WI-047). *Mitigation:* each item re-pins by the producer; the study's compatibility arm, not the manifest, is the bridge to the entering pin.
6. **A reader takes the capacity fence at 14 loops as a bound on plant size.** *Mitigation:* D6 and the instance doc say the count is a lever sized once; the study's re-sized arm reports feasibility under the sizing rule beside the held-count reading.

## Approval

The owner delegated the modelling judgement at grounding (`goal.md` § Reserved gates); this design proceeds to its plan under that delegation, as WI-043 and WI-044 did. The fresh round review is the independent check. Two things go back to the round rather than the owner: the packet's `pb__q_source` becomes `source_heat__q_source` and its plant-level aggregations become loop outputs (D3, D9); the packet § 7 loop draw becomes 175.44 MW on the corrected calibration (§ Research findings).
