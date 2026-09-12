---
Status: draft
Created: 2026-09-08
Updated: 2026-09-08
Related Artifacts:
  Spec: ./spec.md
---

# WI-047 Design — the fuel, divertor-heat and vacuum reduced flows

Three flat-arithmetic library calcs read channels the package already computes (fusion power, the sustainment chain's alpha heating, core radiation and requirement, the installed coupled heating) and publish tritium flows with a required breeding ratio, a divertor surface-heat ledger with one fence, and the gas load after recombination; every input the corpus does not print is surfaced at its binding. Written under goal `plant-closure` round 1, task T-003; the form is `[AGENT] — proposed under the owner's direction of 2026-09-08` (`goal.md` § Reserved gates 5, 6). Prototyped in `prototype/proto.py` (pure Python; `proto_results.json`); no model file is touched by this design — the integration is the round's later task, third on the shared files (basis packet § 9).

## Overview

Today Rows 10, 5, 6 and 2c have no physical quantity (spec § Current state). After this item:

- `'Fuel Cycle Flows'` computes the tritium burn from fusion power, the injected and exhausted streams from the burn fraction, the permanently unrecovered stream from a recovery fraction, the required breeding ratio and its margin against the source-conditioned achieved TBR, and the burn mass per full-power year;
- `'Divertor Heat Ledger'` computes the absorbed heating (installed basis), the separatrix power, the derived edge radiated fraction, the non-radiated target load, the peak target flux at the source's fixed geometry, an R-scaled shadow, the margin, and the operating-minus-installed heating difference; `divertor_heat_ok` asserts the peak against the adopted 10 MW/m²;
- `'Vacuum Gas Load'` counts molecules after recombination and publishes the throughput and the required effective speed at a declared exhaust pressure.

At the entering pin every existing channel is bit-identical (the calcs read, they do not feed); the verdict list gains exactly `divertor_heat_ok: violated` (10.535 against 10 on the pessimistic case, by the model's absorbed heating 554.49 MW against the source's 500). The breeding margin reads −0.116 under the reading of 0.99 as physical recovery and is a channel, not a fence.

## Research findings

- **The channels the ledger reads exist and are wired.** `'Plasma Sustainment'` (`models/library/analyses/mfe_plasma_sustainment.sysml:4-238`) outputs `p_rad` (`:224`), `p_alpha_heat` (`:226`; `f_alpha × ash_frac × p_fus` per the doc at `:87`, with `ash_frac_in` defaulting to 0.2002 at `:193` and `f_alpha_in = f_alpha_fast = 0.95` bound at `mfe_plant.sysml:251` / instance `:687`) and `p_aux_required` (`:228`); the plant usage is `sustain` (`mfe_plant.sysml:239-257`). The prototype checks `0.95 × 0.2002 × 2652.5632625175904 = 504.49100689822046` against the pinned channel to better than 1e-9 — so at any point the ledger's alpha term is recoverable from `p_fus` alone, which is how the off-design predictions below are made where the committed CSV carries `p_fus` but not `p_rad`.
- **The heating chain's `heat.p_coupled`** (`mfe_plant.sysml:481-487`) is the thermal sum's own operand (`:491`), 50.0 at the pin; the basis packet § 5 fixes it as the ledger's heating basis in round 1 and the operating-minus-installed difference as a reported channel.
- **The instance already carries every fuel constant the burn needs:** `fuel_q_eff = 17.58` MeV (`stellarator_plant.sysml:1154`), `mev_to_joules = 1.6021766339999998e-13` (`:1157`), `burn_fraction = 0.05` (`:1160`), `fuel_recovery = 0.99` (`:1163`), `tbr = 1.074` (`:1295`); `E_fus = 2.817e-12` J (`:614`) is the sustainment chain's own per-event energy and is *not* reused here — the fuel calc takes `fuel_q_eff × mev_to_joules` so the burn rate and the fuel cost count the same reactions (the cost's `annual_raw` divides by the same product, `mfe_account_costs.sysml:771-773`).
- **The library precedent for an SI constant with a default:** `'Volume-Averaged Beta'` carries `in attribute mu0 : Real default 1.25663706212e-6;` (`mfe_plasma_scaling.sysml:413`) with its CODATA citation — a physical constant may carry a library default; a source-derived number (the half-life, the burn fraction) may not (MR-3).
- **The source case, read from the render** (`evidence/grounding_sources/stellaris_p15_divertor.png`; text `stellaris-design-details.md:1219-1246`): 90 % of the net core heating radiated; 500 MW → 50 MW to the divertor; (100 eV, 3 m²/s) captures 97 % with a 5 MW/m² peak; (200 eV, 1 m²/s) captures 99 % with 9.5 MW/m²; both "remain below 10 MW m⁻²"; ~200 mm strike width; the values "strongly hinge on the assumed radiated power fraction". The two transport cases share the same 50 MW, so at fixed geometry and transport the peak is linear in the non-radiated load — the reduced response the breadth report proposes (`20260907-163520_demo-breadth-disposition-prework.md:105`).
- **`(1 − f) × p` does not reproduce the source's 50 MW to the double** (`0.1 × 500 = 49.999999999999986` in float64) while `p − f × p` does (`500 − 450 = 50` exactly, `9.5 × 50 / 50 = 9.5` exactly). The prototype's first run showed it; the design takes the exact form (D4).
- **The committed cheapest machine** at 100 MW is `20260907-minor-radius:c2823` (committed id `20260907-burn-control:c2823`; R 15.7, a 2.2, 13 MA, 13 keV, n 5.06e20, `p_fus` 5363.434926736221, LCOE 202.165, `p_aux_required` 33.34 from the oracle column); the highest-fusion ten-verdict feasible point at 100 MW is `c3598` (R 17.2, a 2.2, 14 MA, 13 keV, `p_fus` 5973.456, LCOE 205.39). The CSV has no `p_rad` column, so `p_sep` and `f_rad_edge` at those points are read at execution; the peak needs only `p_fus` and `p_coupled`.
- **The codegen envelope** (`+ - * / **`) admits every form here; no manual stage; no logarithm (the decay constant is an input, its `ln 2` folded at the instance).
- **The constraint-def pattern** (`mfe_viability.sysml:60-81`, `'Neutron Wall Load Limit'`): a doc, two `in attribute`s, one comparison; the plant asserts it with two `in` bindings.

## Design decisions

### D1 — The deuterium exhaust stream equals the tritium stream; the vacuum calc takes both as formals. `[AGENT]`
A 50/50 D-T fuel injects and exhausts deuterium and tritium in equal numbers at every point of the sweep (the fuel calc has no D-T asymmetry lever). The plant binds `vacuum.exhaust_rate_D_in = fuel.exhaust_rate` and `exhaust_rate_T_in = fuel.exhaust_rate`; the calc keeps two formals so a concept with a stated asymmetry can bind two streams without a library change. Rejected: a separate deuterium calc (a second copy of the same arithmetic). Closes spec open decision 1.

### D2 — The decay constant, the atomic mass unit, the tritium mass, the seconds per full-power year and Boltzmann's constant: where each lives. `[AGENT]`
`lambda_T` is an **instance** input bound to the exact double `math.log(2.0) / (4500.0 × 86400.0) = 1.782785958230312e-9` s⁻¹ with the NIST derivation in its doc — a source-derived number, never a library default (MR-3). `m_T_kg` is an instance input bound to `3.01604928 × 1.66053906892e-27` (the tritium atomic mass in u times the atomic mass unit the instance already uses for Li-6 in `fuel_cost_per_rxn`'s doc, `stellarator_plant.sysml:1142-1152`) with its derivation. `s_per_fpy` is a library default `31536000.0` (8760 h × 3600 s — the model's own year, the `8760.0` of `'LCOE DCF'` and the `3600.0 × 8760.0` of `'DT Fuel Cost'`), so the burn mass per full-power year is on the same year every other annual quantity uses; the breadth report's 365.25 d is not adopted (it would put the fuel on a different year than the energy). `k_B` is a library default `1.380649e-23` (exact SI, the `mu0` precedent) with the citation. Closes spec open decision 2.

### D3 — `tbr_available_in` binds to the existing `tbr` attribute; no second copy of 1.074. `[AGENT]`
The plant binds `fuel.tbr_available_in = tbr`, the same attribute `tbr_ok` reads (`stellarator_plant.sysml:1295`, `:1318`). One producer, one entry point; the margin and the held fence read the same number. Closes spec open decision 3.

### D4 — The non-radiated load is written `p_heat_abs − f_rad_total × p_heat_abs`, and the source case reproduces to the double. `[AGENT]`
See the research finding above: `500 − 450 = 50` exactly and `9.5 × 50 / 50 = 9.5` exactly, so SV "the source case reproduced with no fitted adjustment" is an exact test, not a tolerance test. At the design point the two forms agree to the ulp (55.449100689822046 either way).

### D5 — The reference pair is bound as `q_target_ref = 9.5`, `p_nonrad_ref = 50.0` (the pessimistic transport case); the low case is a study lever on the same two formals. `[AGENT]`
The source's most pessimistic reading is the one the paper itself reports "remain below 10" against; taking it makes the fence conservative and the disclosed baseline violation honest. The study arm sets `q_target_ref = 5.0` (same `p_nonrad_ref`), so the low case is a lever, not a second calc. Rejected: binding both cases and asserting on the mean (invents a case the source does not print). Per basis packet § 8 item 7.

### D6 — The verdict operand is the fixed-geometry peak; the R-scaled shadow is a separate output and nothing reads it. `[AGENT]`
`q_target_peak_area_scaled = q_target_peak × R_ref / R` publishes what a target whose wetted length grows with the machine would read; no source supports it, so it is reported and never asserted (basis packet § 6). `R_in` is the plant's `R`; `R_ref_in` is a new instance anchor `R_ref_divertor = 12.7` — named with its own suffix because `magnet.R_ref` (WI-044) is a magnet-chain anchor with its own meaning, and one attribute must not serve two chains' anchors unannounced.

### D7 — `f_rad_edge` is reported, never clamped, with an in-range channel beside it. `[AGENT]`
`f_rad_edge_in_range = f_rad_edge × (1 − f_rad_edge)` is nonnegative exactly when `f_rad_edge ∈ [0, 1]`, so the study can count inconsistent-assumption points (a core radiation above 90 % of the absorbed heating) without a fence. At the design point 0.834366 and 0.138199. Closes spec open decision 5 as its default.

### D8 — The two off-design verification points are `c2823` and `c3598`, predicted from `p_fus` alone. `[AGENT]`
`c2823` is the committed cheapest machine (`goal.md` § Answered when (d) names it); `c3598` is the highest-fusion ten-verdict feasible point at 100 MW — the point where the fixed-geometry fence bites hardest inside the old feasible set. Both are executed at the committed levers and their `p_sep`, `f_rad_edge` read at execution (D8 note above). Closes spec open decision 4.

### D9 — The constraint def is `'Divertor Target Heat Limit'` in `mfe_viability.sysml`, after `'Neutron Wall Load Limit'`; the assert is `divertor_heat_ok`. `[AGENT]`
The breadth report's name; beside the wall-load limit because both are surface-load bounds on the same page of the source. Closes spec open decision 6.

### D10 — Dormant-safe defaults on the generic plant: a concept binding nothing gets a satisfied fence and finite channels. `[AGENT]`
The generic plant declares the divertor and vacuum facts with defaults that make the chains inert: `f_rad_total 0.0`, `q_target_ref 0.0`, `p_nonrad_ref 1.0`, `q_target_limit 1.0`, `R_ref_divertor 1.0` (so `q_target_peak = 0 × p / 1 = 0 ≤ 1`, satisfied; no division by zero), `t_recycle 1.0`, `eta_extract 1.0`, `I_total 0.0`, `G_stock 0.0`, `lambda_T 0.0`, `m_T_kg 0.0`, `p_exhaust 1.0`, `T_gas 1.0` — the WI-024 / WI-039 dormancy shape (the mode selected by a value that makes the chain inert, never by an efficiency). The formals `p_fus`, `burn_fraction`, `tbr` are the plant's existing attributes (every MFE instance binds them). The IFE designs do not import the MFE plant and are untouched. Rejected: no defaults (the tokamak half of epic Item 3 would need to bind fourteen facts before it compiles — the WI-044 D6 choice was right for anchors every instance must state; these are dormant facts a concept may honestly lack).

### D11 — The oracle derives the three chains from this design's equations; the seam adds nine levers and one binding. `[AGENT]`
`verify_stellaris.py`: `IN` gains `t_recycle`, `eta_extract`, `I_total`, `G_stock`, `lambda_T`, `m_T_kg`, `f_rad_total`, `q_target_ref`, `p_nonrad_ref`, `q_target_limit`, `R_ref_divertor`, `T_gas`, `p_exhaust` (the instance's doubles); `compute()` adds the fuel block after `p_fus`, the ledger after the sustainment call, the gas load after the fuel block; the return dict gains the seventeen channels of basis packet § 2 plus `f_rad_edge_in_range`. `oracle_entry.py`: `ENTRY_KEY_TO_ORACLE_INPUT` gains the thirteen keys; `ORACLE_OUTPUT_TO_CHANNEL` gains the eighteen channels; `OPERAND_BINDINGS` gains one entry for `divertor_heat_ok` (`q_target_peak_in` ← the `divheat__q_target_peak` channel, `q_target_limit_in` ← the input key) with its constraint id read from `generated/contracts/model_contract.json` at implementation, never guessed.

### D12 — The restatement, the predictions and `evidence/baseline_before/` commit before regeneration; this item's baseline diff is against the package as WI-046 left it. `[AGENT]`
The WI-044 D8 shape. Because WI-047 lands third, its "before" is WI-046's "after" (the packet § 9 order); the identity claimed is on that package's channel set, and the plan records the pin it started from.

## Proposed design

### New: `models/library/analyses/mfe_fuel_cycle.sysml` (prototyped)

```sysml
package mfe_fuel_cycle {
    private import ScalarValues::*;

    calc def 'Fuel Cycle Flows' {
        doc /*
        Tritium flows of a D-T plant, reduced to conservation (WI-047):

          burn_rate       = p_fus * 1e6 / E_fus_J                       [atoms/s]
          inject_rate     = burn_rate / burn_fraction                    [atoms/s]
          exhaust_rate    = inject_rate - burn_rate                      [atoms/s]
          loss_rate       = (1 - t_recycle) * exhaust_rate               [atoms/s]
          tbr_required    = (burn_rate + loss_rate + lambda_T * I_total + G_stock)
                            / (eta_extract * burn_rate)                  [1]
          tbr_margin      = tbr_available - tbr_required                 [1]
          burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy               [kg per full-power year]

        One D-T reaction burns one tritium atom; the fusion power fixes the burn,
        the single-pass burn fraction fixes the circulating stream, and the recovery
        of the unburned stream fixes the permanent loss. The required breeding ratio
        is the tritium that must be bred per atom burned to replace burn, permanent
        loss, decay of the held inventory and any stock growth, divided by the
        extraction efficiency from breeder to usable supply. The margin against the
        ACHIEVED ratio a concept binds is a REPORTED adequacy quantity: no fence reads
        it (the achieved ratio is a source-conditioned input at the source's own
        geometry, and the recovery semantics are an open owner decision -- see the
        instance binding of t_recycle).

        Inventory and startup stock are NOT computed here: I_total, G_stock and
        eta_extract are dormant (0, 0, 1) until residence times, extraction
        efficiency and a reserve policy have an admissible source (retrieval target:
        Lord et al., UKAEA-STEP-PR(24)12). A duty factor multiplies operating burns
        and flows in the plant (the calendar's productive time); stock decays through
        calendar time too -- the two clocks are the lifecycle calc's, not this one's.

        This calc computes REQUIRED breeding, never achieved neutronics: rubric Row
        2c stays bounded at the source geometry. 'DT Fuel Cost' (mfe_account_costs)
        keeps its own burn correction on the same burn_fraction and the same
        recovery number read as a feedstock cost factor; the two calcs read the
        same inputs and mean different things, and say so.

        Flat-Real (+ - * /) -- lowers to generated arithmetic; no manual stage.

        **Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
        **Ref**: lines 43-54 (the conservation equations in T atoms/s), 56 (the NIST
            half-life 4500 +/- 8 d, Lucas and Unterweger, J. Res. NIST 105 (2000) 541),
            58 (startup as a residence-time balance, not computed here), 60 (the
            conditional 1.19 finding)
        **Basis**: Tritium conservation on the burned, circulating and bred streams
        */

        // fusion power [MW]
        in attribute p_fus : Real;
        // energy per D-T reaction [J] -- the plant passes fuel_q_eff * mev_to_joules
        in attribute E_fus_J : Real;
        // single-pass burn fraction [1], 0 < burn_fraction <= 1
        in attribute burn_fraction : Real;
        // recovery fraction of the unburned tritium stream [1], 0 <= t_recycle <= 1
        in attribute t_recycle : Real;
        // achieved tritium breeding ratio [1] (a concept's source-conditioned value)
        in attribute tbr_available : Real;
        // breeder-to-supply extraction efficiency [1], 0 < eta_extract <= 1 (dormant 1.0)
        in attribute eta_extract : Real;
        // tritium decay constant [1/s] (an instance input derived from the half-life)
        in attribute lambda_T : Real;
        // total held tritium inventory [atoms] (dormant 0.0: residence times unsourced)
        in attribute I_total : Real;
        // required stock growth [atoms/s] (dormant 0.0: a single mature plant)
        in attribute G_stock : Real;
        // tritium atomic mass [kg] (an instance input with its derivation)
        in attribute m_T_kg : Real;
        // seconds per full-power year [s]: 8760 h x 3600 s, the model's own year
        // ('LCOE DCF' 8760.0; 'DT Fuel Cost' 3600.0 * 8760.0)
        in attribute s_per_fpy : Real default 31536000.0;

        out attribute burn_rate : Real = p_fus * 1.0e6 / E_fus_J;
        out attribute inject_rate : Real = burn_rate / burn_fraction;
        out attribute exhaust_rate : Real = inject_rate - burn_rate;
        out attribute loss_rate : Real = (1.0 - t_recycle) * exhaust_rate;
        out attribute tbr_required : Real =
            (burn_rate + loss_rate + lambda_T * I_total + G_stock) / (eta_extract * burn_rate);
        out attribute tbr_margin : Real = tbr_available - tbr_required;
        out attribute burn_kg_per_fpy : Real = burn_rate * m_T_kg * s_per_fpy;
    }
}
```

### New: `models/library/analyses/mfe_divertor_heat.sysml` (prototyped)

```sysml
package mfe_divertor_heat {
    private import ScalarValues::*;

    calc def 'Divertor Heat Ledger' {
        doc /*
        Divertor surface-heat ledger, reduced to conservation and one sourced
        fixed-geometry case (WI-047):

          p_heat_abs        = p_alpha_heat + p_coupled                       [MW]
          p_sep             = p_heat_abs - p_rad_core                         [MW]
          f_rad_edge        = (f_rad_total * p_heat_abs - p_rad_core) / p_sep  [1]
          f_rad_edge_in_range = f_rad_edge * (1 - f_rad_edge)                 [1] (>= 0 iff in [0, 1])
          p_target_nonrad   = p_heat_abs - f_rad_total * p_heat_abs           [MW]
          q_target_peak     = q_target_ref * p_target_nonrad / p_nonrad_ref   [MW/m^2]
          q_target_peak_area_scaled = q_target_peak * R_ref / R               [MW/m^2] (reported shadow)
          q_target_margin   = q_target_limit - q_target_peak                  [MW/m^2]
          p_heat_operating_minus_installed = p_aux_required - p_coupled       [MW]

        The absorbed heating is the alpha heating retained in the plasma plus the
        coupled auxiliary heating on the plant's INSTALLED basis -- the same operand
        the thermal sum uses (round 1 of goal plant-closure; the operating-versus-
        installed difference is the last output, reported and never blended in).
        Radiation is a DESTINATION of that heating, never added to it: the core
        radiation the sustainment chain composes leaves through the first wall; the
        source's radiated fraction f_rad_total is a TOTAL (core plus edge), so the
        edge share is derived and reported, not clamped -- a value outside [0, 1]
        means the held total and the computed core radiation are inconsistent at
        that point, and the in-range channel lets a study count such points.

        The peak target flux is the source's own case scaled linearly in the
        non-radiated load at FIXED target geometry and transport (q_target_ref at
        p_nonrad_ref): no target area, wetted fraction, emissivity, view factor,
        erosion or transient enters. A machine of another size keeps the source's
        target; the R-scaled output publishes what a target whose wetted length grows
        with the major radius would read, and nothing asserts on it. The limit a
        concept binds is an adopted steady-state threshold, not an irradiated-
        component lifetime. The source's divertor case (a total radiated fraction)
        and its first-wall cooling case (100 % radiated) are two load cases and are
        never summed. Written p_heat_abs - f * p_heat_abs so the source's own numbers
        reproduce to the double (500 - 450 = 50).

        Flat-Real (+ - * /) -- no manual stage.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: lines 1219-1246 (90 % of the net core heating radiated; 500 MW ->
            50 MW; the two transport cases (100 eV, 3 m^2/s) 97 % / 5 MW/m^2 and
            (200 eV, 1 m^2/s) 99 % / 9.5 MW/m^2; "remain below 10 MW/m^2"; ~200 mm
            strike width); 1135-1137 (recycling, ash removal, neutral compression and
            erosion left for later work); 1244-1250 (the values hinge on the radiated
            fraction; transients for future study); 1284 (the first-wall case at
            100 %, a different load case); page render
            work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p15_divertor.png
        **Basis**: Heat conservation from absorbed heating to the target on the
            source's fixed-geometry case, scaled in load only
        */

        // alpha heating retained in the plasma [MW] (the sustainment chain's)
        in attribute p_alpha_heat : Real;
        // plasma-coupled auxiliary heating on the installed basis [MW] (the thermal sum's operand)
        in attribute p_coupled : Real;
        // required sustained coupled heating [MW] (the sustainment chain's; reported difference only)
        in attribute p_aux_required : Real;
        // composed core radiation [MW] (bremsstrahlung + line + synchrotron)
        in attribute p_rad_core : Real;
        // total radiated fraction of the absorbed heating [1], 0 <= f <= 1 (a source assumption)
        in attribute f_rad_total : Real;
        // the source case's peak target flux [MW/m^2] at p_nonrad_ref
        in attribute q_target_ref : Real;
        // the source case's non-radiated load [MW], > 0
        in attribute p_nonrad_ref : Real;
        // adopted steady-state target-flux threshold [MW/m^2]
        in attribute q_target_limit : Real;
        // major radius [m] and the source case's major radius [m], > 0 (the shadow only)
        in attribute R : Real;
        in attribute R_ref : Real;

        out attribute p_heat_abs : Real = p_alpha_heat + p_coupled;
        out attribute p_sep : Real = p_heat_abs - p_rad_core;
        out attribute f_rad_edge : Real = (f_rad_total * p_heat_abs - p_rad_core) / p_sep;
        out attribute f_rad_edge_in_range : Real = f_rad_edge * (1.0 - f_rad_edge);
        out attribute p_target_nonrad : Real = p_heat_abs - f_rad_total * p_heat_abs;
        out attribute q_target_peak : Real = q_target_ref * p_target_nonrad / p_nonrad_ref;
        out attribute q_target_peak_area_scaled : Real = q_target_peak * R_ref / R;
        out attribute q_target_margin : Real = q_target_limit - q_target_peak;
        out attribute p_heat_operating_minus_installed : Real = p_aux_required - p_coupled;
    }
}
```

### New: `models/library/analyses/mfe_vacuum.sysml` (prototyped)

```sysml
package mfe_vacuum {
    private import ScalarValues::*;

    calc def 'Vacuum Gas Load' {
        doc /*
        Torus exhaust gas load after recombination (WI-047):

          n_molecules    = (exhaust_rate_D + exhaust_rate_T) / 2 + helium_rate   [molecules/s]
          Q_total        = n_molecules * k_B * T_gas                            [Pa m^3/s]
          S_eff_required = Q_total / p_exhaust                                  [m^3/s]

        Hydrogen isotopes leave as diatomic molecules (D2, T2 and DT each carry two
        nuclei, so the molecule count is the atom count over two, whatever the
        pairing); helium ash is atomic. The throughput is the ideal-gas pV rate at
        the stated gas temperature; the required effective speed is that throughput
        divided by the pressure at the exhaust boundary. The pressure is a boundary
        condition at a stated location -- neither the plasma pressure nor the pre-shot
        base vacuum -- and no admissible source prints it for this machine; a concept
        that declares one says so at the binding. Pump-inlet speed and effective
        speed differ by duct conductance (1/S_eff = 1/S_pump + 1/C in the molecular,
        linear-conductance case); ducts, species-dependent speeds, regeneration duty,
        puff and seeding bypass, leakage and outgassing are not modelled. Nothing
        here maps a neutron load to a target load, and neither the vessel volume nor
        the coolant pumping power stands in for the gas load.

        Flat-Real (+ - * /) -- no manual stage.

        **Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
        **Ref**: lines 124-130 (species-resolved throughput after recombination,
            Q = dN k_B T, S_eff = Q / p, conductance in series; Franchetti, CERN
            Vacuum I, slides 24-27 and 43-46, as cited there; ITER vacuum-system
            scope separation)
        **Basis**: Gas conservation at the exhaust boundary; ideal-gas throughput
        */

        // deuterium and tritium atoms leaving the plasma [atoms/s]
        in attribute exhaust_rate_D : Real;
        in attribute exhaust_rate_T : Real;
        // helium ash produced [atoms/s] (one per D-T reaction)
        in attribute helium_rate : Real;
        // Boltzmann constant [J/K], exact SI (2019 redefinition)
        in attribute k_B : Real default 1.380649e-23;
        // gas temperature at the exhaust boundary [K], > 0
        in attribute T_gas : Real;
        // pressure at the exhaust boundary [Pa], > 0
        in attribute p_exhaust : Real;

        out attribute n_molecules : Real = (exhaust_rate_D + exhaust_rate_T) / 2.0 + helium_rate;
        out attribute Q_total : Real = n_molecules * k_B * T_gas;
        out attribute S_eff_required : Real = Q_total / p_exhaust;
    }
}
```

### Changed: `models/library/analyses/mfe_viability.sysml` — one constraint def after `'Neutron Wall Load Limit'` (prototyped)

```sysml
    constraint def 'Divertor Target Heat Limit' {
        doc /*
        Divertor target steady-state heat-flux bound (WI-047; goal plant-closure):
        the PEAK target flux computed by 'Divertor Heat Ledger' (mfe_divertor_heat)
        -- the source's fixed-geometry transport case scaled in the non-radiated
        load -- must stay at or below the adopted steady-state threshold. The
        operand responds to every lever that moves the alpha heating, the coupled
        heating or the core radiation, so the fence pushes back on the operating
        point through a modelled response, not through a held value. It says
        nothing about detachment control, erosion, transients or the irradiated
        allowable, which the source leaves for later work; the R-scaled shadow the
        ledger also publishes is NOT this operand. Pair with 'Neutron Wall Load
        Limit': two surface loads, two fences, never one mapped onto the other.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: lines 1239-1246 ("These values remain below 10 MW m^-2, which is a
            commonly applied threshold for steady-state heat fluxes in divertor
            designs"); page render
            work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p15_divertor.png
        **Basis**: Peak target heat flux must not exceed the adopted steady-state threshold
        */

        // peak target heat flux [MW/m^2] (computed)
        in attribute q_target_peak_in : Real;
        // adopted steady-state threshold [MW/m^2]
        in attribute q_target_limit_in : Real;

        q_target_peak_in <= q_target_limit_in
    }
```

### Changed: `models/designs/generic_mfe/mfe_plant.sysml` (prototyped)

Three imports added beside the existing analysis imports (`mfe_fuel_cycle`, `mfe_divertor_heat`, `mfe_vacuum`). After the CAS80 fuel block (after line 936, `cas80_annual`), a fuel-flows block; after it the ledger and the gas load; the assert beside the other viability asserts (after `cond_strain_ok`, line 1077):

```sysml
        // ---- Fuel-cycle flows (WI-047): conservation on the same reactions the
        // cost prices; the margin is reported, never asserted (the recovery
        // semantics are an owner decision -- see the instance). Dormant-safe by
        // the WI-024 pattern: a concept binding nothing gets a lossless loop.
        // recovery fraction of the unburned tritium stream [1]
        attribute t_recycle : Real default 1.0;
        // breeder-to-supply extraction efficiency [1]
        attribute eta_extract : Real default 1.0;
        // tritium decay constant [1/s]
        attribute lambda_T : Real default 0.0;
        // held tritium inventory [atoms]
        attribute I_total : Real default 0.0;
        // required stock growth [atoms/s]
        attribute G_stock : Real default 0.0;
        // tritium atomic mass [kg]
        attribute m_T_kg : Real default 0.0;
        calc fuel : 'Fuel Cycle Flows' {
            in p_fus = fusion.p_fus;
            in E_fus_J = fuel_q_eff * mev_to_joules;
            in burn_fraction = burn_fraction;
            in t_recycle = t_recycle;
            in tbr_available = tbr;
            in eta_extract = eta_extract;
            in lambda_T = lambda_T;
            in I_total = I_total;
            in G_stock = G_stock;
            in m_T_kg = m_T_kg;
        }

        // ---- Divertor surface-heat ledger (WI-047) on the INSTALLED heating
        // basis (the thermal sum's own operand) -- round 1 of goal plant-closure.
        // Dormant-safe: q_target_ref 0 and p_nonrad_ref 1 give a zero peak and a
        // satisfied fence for a concept binding nothing.
        attribute f_rad_total : Real default 0.0;
        attribute q_target_ref : Real default 0.0;
        attribute p_nonrad_ref : Real default 1.0;
        attribute q_target_limit : Real default 1.0;
        attribute R_ref_divertor : Real default 1.0;
        calc divheat : 'Divertor Heat Ledger' {
            in p_alpha_heat = sustain.p_alpha_heat;
            in p_coupled = heat.p_coupled;
            in p_aux_required = sustain.p_aux_required;
            in p_rad_core = sustain.p_rad;
            in f_rad_total = f_rad_total;
            in q_target_ref = q_target_ref;
            in p_nonrad_ref = p_nonrad_ref;
            in q_target_limit = q_target_limit;
            in R = R;
            in R_ref = R_ref_divertor;
        }

        // ---- Torus exhaust gas load (WI-047): a 50/50 D-T fuel exhausts equal
        // deuterium and tritium streams; the helium ash is one atom per reaction.
        attribute T_gas : Real default 1.0;
        attribute p_exhaust : Real default 1.0;
        calc vacuum : 'Vacuum Gas Load' {
            in exhaust_rate_D = fuel.exhaust_rate;
            in exhaust_rate_T = fuel.exhaust_rate;
            in helium_rate = fuel.burn_rate;
            in T_gas = T_gas;
            in p_exhaust = p_exhaust;
        }
```

```sysml
        // WI-047: the divertor target peak (fixed-geometry source case, scaled in
        // load) against the adopted threshold. EXPECTED VIOLATED at the Stellaris
        // baseline on the pessimistic case (10.535 against 10: the model's absorbed
        // heating 554.49 MW is 10.9 % above the source's 500) -- the disclosed,
        // explained verdict change of WI-047, never tuned (the WI-041 precedent).
        assert constraint divertor_heat_ok : 'Divertor Target Heat Limit' {
            in q_target_peak_in = divheat.q_target_peak;
            in q_target_limit_in = q_target_limit;
        }
```

`E_fus_J = fuel_q_eff * mev_to_joules` is a plant-level product of two instance attributes; if the exact route refuses a derived expression on a calc input (the WI-028 bare-alias class), the fallback is a plant attribute `fuel_E_fus_J : Real = fuel_q_eff * mev_to_joules;` — the plan's phase 1 checks which form the codegen accepts and records it.

### Changed: `models/designs/stellarator_09/stellarator_plant.sysml` (prototyped)

After the CAS80 fuel-chemistry block (after `fuel_recovery`, line 1165):

```sysml
        // ---- WI-047 fuel-cycle flows: the recovery semantics SURFACED ----
        :>> t_recycle = 0.99 {  // recovery of the unburned tritium stream [1] -- READ FROM THE COST FACTOR.
            doc /*
            This is the existing fuel_recovery (0.99) read as the PHYSICAL recovery
            of the unburned tritium stream. It was sourced as a NOAK feedstock cost
            factor (1costingFE steady_state_stellarator.yaml:65), not as an isotope-
            recovery measurement. Under this reading, at a 5 % single-pass burn the
            required breeding ratio is 1 + 0.95/0.05 x 0.01 = 1.19 against the
            source-conditioned achieved 1.074: a margin of -0.116, published as
            fuel.tbr_margin and asserted by NOTHING. The zero-margin recovery is
            1 - (1.074 - 1) x 0.05/0.95 = 0.99611. This is a conditional semantics
            conflict put to the owner (goal plant-closure, goal.md section Reserved
            gates 5; basis packet section 6), not a proven physical deficit; a
            separate physical-recovery input, if minted, replaces this binding, and
            the value is never raised to erase the finding.
            **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml
            **Ref**: steady_state_stellarator.yaml:65 (fuel_recovery = 0.99); knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md:23, :60
            **Basis**: The existing 0.99 read as physical recovery, disclosed as a reading
            */
        }
        :>> eta_extract = 1.0 {  // breeder-to-supply extraction efficiency [1] -- DORMANT, unsourced.
            doc /* **Source**: none admissible **Ref**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md:56, :64 (retrieval target: Lord et al., UKAEA-STEP-PR(24)12) **Basis**: lossless extraction as the declared dormant value; inventory and startup stock are not computed until residence times, extraction efficiency and a reserve policy are sourced */
        }
        :>> I_total = 0.0 {  // held tritium inventory [atoms] -- DORMANT, residence times unsourced.
            doc /* **Source**: none admissible **Ref**: as eta_extract **Basis**: no inventory; the decay term is zero until residence times exist */
        }
        :>> G_stock = 0.0 {  // required stock growth [atoms/s] -- a single mature plant.
            doc /* **Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md:56 **Ref**: "G_stock is a deliberately specified stock-growth requirement, zero for a single mature plant that only sustains itself" **Basis**: self-sustaining plant */
        }
        :>> lambda_T = 1.782785958230312e-09 {  // tritium decay constant [1/s].
            doc /* ln 2 / (4500 d x 86400 s/d) = 1.782785958230312e-09 s^-1; the half-life 4500 +/- 8 d (8 d a standard uncertainty). **Source**: Lucas and Unterweger, J. Res. NIST 105 (2000) 541 (https://nvlpubs.nist.gov/nistpubs/jres/105/4/j54luc2.pdf) **Ref**: p. 541, the evaluated half-life; cited via knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md:56 **Basis**: NIST evaluated tritium half-life */
        }
        :>> m_T_kg = 5.008267663228036e-27 {  // tritium atomic mass [kg].
            doc /* 3.01604928 u x 1.66053906892e-27 kg/u (the atomic mass unit fuel_cost_per_rxn above already uses). **Source**: CODATA 2018 (the unit; the instance's fuel_cost_per_rxn doc); the tritium atomic mass 3.01604928 u (AME, as commonly tabulated) **Ref**: fuel_cost_per_rxn doc above (_ATOMIC_MASS) **Basis**: tritium atomic mass */
        }
```

After the TBR block (after `tbr_floor`, line 1301):

```sysml
        // ---- WI-047 divertor surface heat: the source's fixed-geometry case ----
        :>> f_rad_total = 0.9 {  // total radiated fraction of the absorbed heating [1].
            doc /* "we assume that 90% of the net heating power in the plasma core is radiated before reaching the divertor region" -- a TOTAL fraction (core plus edge); the first-wall cooling case on the same page assumes 100 % and is a different load case, never summed with this one. **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md **Ref**: lines 1219-1222; page render work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p15_divertor.png **Basis**: Stellaris section 2.6 operating assumption */
        }
        :>> q_target_ref = 9.5 {  // the pessimistic transport case's peak target flux [MW/m^2].
            doc /* The (T_LCFS 200 eV, chi_perp 1 m^2/s) case: 99 % captured, peak 9.5 MW/m^2 at 50 MW non-radiated. The low case (100 eV, 3 m^2/s; 97 %; 5 MW/m^2 at the same 50 MW) is a study arm on this same attribute, not a second binding; the two are a paired assumption/result set and are never mixed. Fixed target geometry and transport: the peak is scaled in load only. **Source**: stellaris-design-details.md **Ref**: lines 1223-1240; the render stellaris_p15_divertor.png **Basis**: Stellaris section 2.6, the most pessimistic printed case */
        }
        :>> p_nonrad_ref = 50.0 {  // the source case's non-radiated load [MW].
            doc /* "for a total of 500 MW of heating power, the divertor must be capable of handling 50 MW". **Source**: stellaris-design-details.md **Ref**: lines 1221-1222; the render **Basis**: Stellaris section 2.6 */
        }
        :>> q_target_limit = 10.0 {  // adopted steady-state target-flux threshold [MW/m^2].
            doc /* "a commonly applied threshold for steady-state heat fluxes in divertor designs" -- an adopted threshold, not an irradiated-component lifetime or an erosion limit. **Source**: stellaris-design-details.md **Ref**: lines 1243-1246; the render **Basis**: Stellaris section 2.6 */
        }
        :>> R_ref_divertor = 12.7 {  // the source case's major radius [m] -- the R-scaled SHADOW only.
            doc /* The shadow q_target_peak_area_scaled = q_target_peak x R_ref / R publishes what a target whose wetted length grows with R would read; no source supports the scaling (retrieval target: new transport / geometry cases), so nothing asserts on it. Named apart from magnet.R_ref (WI-044), a different chain's anchor. **Source**: stellaris-design-details.md **Ref**: Table 2 image (R 12.7) **Basis**: the source geometry of the divertor case */
        }
        // ---- WI-047 exhaust gas load: the boundary pressure DECLARED, not sourced ----
        :>> T_gas = 300.0 {  // gas temperature at the exhaust boundary [K] -- a convention.
            doc /* Room-temperature neutral gas, stated as a convention for the pV throughput; the actual exhaust gas temperature, duct conductance and species-dependent pumping speeds are missing inputs (retrieval targets: the W7-X pumping and neutral-compression work Stellaris section 2.6 cites; the ITER torus cryopump technical specifications). **Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md:124-128 **Basis**: declared convention */
        }
        :>> p_exhaust = 1.0 {  // pressure at the exhaust boundary [Pa] -- DECLARED, no admissible source.
            doc /* No admissible source prints this machine's exhaust boundary pressure. At 1 Pa the required effective speed equals the throughput's own numerical value per pascal, so vacuum.S_eff_required is the throughput restated, not a pumping specification; a study reads speeds at declared pressures. Retrieval targets as T_gas. **Source**: none admissible **Ref**: basis packet section 6 **Basis**: declared value, labelled */
        }
```

The `tbr` binding's comment gains one sentence: "WI-047: also read by 'Fuel Cycle Flows' as the achieved ratio the required ratio is compared with; the margin is reported, this fence is unchanged."

### Twins: `exploration/stellarator_e2e/models/analyses/{mfe_fuel_cycle,mfe_divertor_heat,mfe_vacuum,mfe_viability}.sysml`, `designs/generic_mfe/mfe_plant.sysml`, `designs/stellarator_09/stellarator_plant.sysml` — copied byte-for-byte (implementation phase 1).

### Changed: `exploration/stellarator_e2e/verify_stellaris.py`, `studies/oracle_entry.py` (D11; implementation phase 3); `run_stellaris_single.py` (`EXPECTED_VERDICTS["divertor_heat_ok"] = "violated"` with its comment; `EXPECTED_VERDICT_COUNT` 13 → 14); `studies/study_route.py` (`EXPECTED_CONSTRAINT_COUNT` 14).

### Re-derived (D12): `stellarator.snapshot.json`, `studies/manifest.json` (fingerprints; `baseline.verdicts` gains `{"source_local_identity": "divertor_heat_ok", "expected": "violated"}`; the headline unchanged from WI-046's pin), `tests/models/data/mfe_census.json` (+14 entry points: `t_recycle`, `eta_extract`, `lambda_T`, `I_total`, `G_stock`, `m_T_kg`, `f_rad_total`, `q_target_ref`, `p_nonrad_ref`, `q_target_limit`, `R_ref_divertor`, `T_gas`, `p_exhaust`, plus `fuel__s_per_fpy` / `vacuum__k_B` if the census counts calc-formal defaults as entry points — the plan records the actual delta), the six `tests/study/data/*.expected.json`, `test_known_answers.py`, the three count-site tests, `generated/**`.

## Cross-file bindings

| Input | Bound to | Source file |
|---|---|---|
| `fuel.p_fus` | `fusion.p_fus` | `mfe_plant.sysml` |
| `fuel.E_fus_J` | `fuel_q_eff * mev_to_joules` (instance 17.58 MeV, 1.6021766339999998e-13) | `mfe_plant.sysml` ← instance |
| `fuel.burn_fraction`, `fuel.tbr_available` | `burn_fraction`, `tbr` (existing attributes; instance 0.05, 1.074) | `mfe_plant.sysml` |
| `fuel.{t_recycle, eta_extract, lambda_T, I_total, G_stock, m_T_kg}` | the six new plant attributes | instance bindings |
| `divheat.{p_alpha_heat, p_aux_required, p_rad_core}` | `sustain.p_alpha_heat`, `sustain.p_aux_required`, `sustain.p_rad` | `mfe_plant.sysml` ← `'Plasma Sustainment'` |
| `divheat.p_coupled` | `heat.p_coupled` | `mfe_plant.sysml` ← `'Heating Power Chain'` |
| `divheat.{f_rad_total, q_target_ref, p_nonrad_ref, q_target_limit}`, `divheat.R_ref` | the five new plant attributes | instance bindings |
| `divheat.R` | `R` | `mfe_plant.sysml` |
| `vacuum.{exhaust_rate_D, exhaust_rate_T}` | `fuel.exhaust_rate` (both) | `mfe_plant.sysml` |
| `vacuum.helium_rate` | `fuel.burn_rate` | `mfe_plant.sysml` |
| `vacuum.{T_gas, p_exhaust}` | the two new plant attributes | instance bindings |
| `divertor_heat_ok.q_target_peak_in`, `q_target_limit_in` | `divheat.q_target_peak`, `q_target_limit` | `mfe_plant.sysml` |

Dataflow stays unidirectional: plasma (`fusion`, `sustain`, `heat`) → `fuel` → `vacuum`; plasma → `divheat` → the fence. Nothing here feeds the power balance, the calendar, a cost account or an existing fence.

## Expected baseline behaviour (MR-WI047-6; stated before regeneration)

At the design point of whatever pin WI-046 leaves (R 12.7, a 1.3, `p_fus` 2652.5632625175904, `sustain__p_alpha_heat` 504.49100689822046, `sustain__p_rad` 219.7216452237653, `sustain__p_aux_required` 49.07960078792678, `heat__p_coupled` 50.0 — unchanged by WI-045 / WI-046, which touch nothing upstream of the plasma):

- **Every existing channel bit-identical** — the three calcs read and do not feed; the LCOE, the power balance, CAS72, the fuel cost and every verdict operand are untouched.
- `fuel__burn_rate` 9.41752… × 10²⁰ (exact: `2652.5632625175904e6 / (17.58 × 1.6021766339999998e-13)`); `inject_rate` 1.88350 × 10²²; `exhaust_rate` 1.78933 × 10²²; `loss_rate` 1.78933 × 10²⁰; `tbr_required` 1.1900000000000002; `tbr_margin` −0.1160000000000001; `burn_kg_per_fpy` 148.741.
- `divheat__p_heat_abs` 554.4910068982204; `p_sep` 334.7693616744551; `f_rad_edge` 0.8343662621559043; `f_rad_edge_in_range` 0.138199…; `p_target_nonrad` 55.449100689822046; `q_target_peak` **10.53532913106619**; `q_target_peak_area_scaled` 10.53532913106619 (R = R_ref); `q_target_margin` −0.535329…; `p_heat_operating_minus_installed` −0.92039921207322.
- `vacuum__n_molecules` 1.8835037171313755 × 10²²; `Q_total` 78.0137257066115 Pa·m³/s; `S_eff_required` 78.0137257066115 m³/s.
- **Verdicts:** every existing verdict unchanged; **`divertor_heat_ok` VIOLATED** (10.535 against 10). On the low-case arm (`q_target_ref` 5.0) the peak reads 5.544910068982205 and the fence is satisfied.
- `p_fus` reconstructed from the burn rate equals the channel to the ulp (the prototype's identity check).

Exact doubles are in `prototype/proto_results.json` (`P0_design_point`); the plan copies them as the prediction of record. If any existing channel differs, the implementation stops and derives why.

## Off-design predictions (D8; `prototype/proto_results.json`; the implementation executes them)

| Point | `p_fus` [MW] | `p_heat_abs` [MW] | `q_target_peak` pessimistic / low [MW/m²] | R-scaled shadow | `divertor_heat_ok` | `tbr_required` |
|---|---|---|---|---|---|---|
| P0 design point | 2652.563 | 554.491 | 10.535 / 5.545 | 10.535 | **violated** (low: satisfied) | 1.19 |
| P3 `c2823` (R 15.7, a 2.2, 13 MA, 13 keV, n 5.06e20, 100 MW; LCOE 202.165) | 5363.435 | 1070.07 | 20.331 / 10.701 | 16.446 | **violated** (low: violated; shadow: violated) | 1.19 |
| P4 `c3598` (R 17.2, a 2.2, 14 MA, 13 keV, 100 MW; the highest-fusion feasible point) | 5973.456 | 1186.01 | 22.536 / 11.861 | 16.639 | **violated** on every reading | 1.19 |

The absorbed heating at which the pessimistic fence is exactly satisfied at fixed geometry is 526.32 MW (`10 × 50 / (9.5 × 0.1)`); on the low case 1000 MW. `p_sep` and `f_rad_edge` at P3 / P4 are read at execution (no `p_rad` column in the committed CSV); the peak, the fuel flows and the gas load need only `p_fus` and `p_coupled`, so they are predicted here. `tbr_required` is 1.19 at every point (it depends on `burn_fraction` and `t_recycle` only, at zero inventory). The reading the study must carry: **at the source's own fixed geometry the pessimistic fence closes every committed cheap machine** — those machines' larger plasmas carry two to four times the design point's alpha heating onto the same target; the low case and the R-scaled shadow do not rescue `c2823` either (10.70 and 16.45). That is the fixed-geometry limitation stated as a number, not a bound the source places on the machine (`goal.md` § Invariants; spec risk 1).

## Validation plan

1. Levels 1–3 pass on `models/` with no new Level 2 warning; Levels 4–6 residue compared with the WI-046 run. *To be done at integration (this design touches no model file).*
2. `tests/models` after the twin sync: the count as WI-046 left it or better, every delta explained.
3. Regeneration: `New: 3` calc modules + 1 constraint module, `Regenerated` only on the plant; no manual stage touched; every handwritten impl preserved byte-identical; no `backup/`; seal clean.
4. The baseline diff (MR-WI047-6): every existing channel bit-identical; eighteen new channels at the predicted doubles; the verdict list gains exactly `divertor_heat_ok: violated`; single-runner parity 14 / (no longer `full_satisfaction` — the runner's expected-state message restated); the oracle gate passes on the new channels at rel 1e-9.
5. P3 and P4 executed through `study_route.run_points` at the committed levers; the predicted channels equal the execution to 1e-9 relative; the oracle re-derives all eighteen channels and the verdict through `OPERAND_BINDINGS` with 0.0 relative deviation; the source case reproduced by the oracle with `p_heat_abs` 500, `p_rad_core` 0: `p_target_nonrad` 50.0 and peaks 9.5 / 5.0 exactly; doubling the load doubles the peak (19.0).
6. The fuel identities: `t_recycle = 1` gives `loss_rate` 0 and `tbr_required` 1.0 at burn fractions 0.01 / 0.05 / 0.2 (the prototype's `lossless_check`); `burn_fraction` halved leaves `burn_rate` unchanged and doubles `inject_rate` and `exhaust_rate`; the 0.99611 zero-margin threshold reproduced on the transect; the molecule count is the atom count / 1.95 at the design point (2 U / 2 + B over 2 U + B) and doubling every rate doubles `S_eff_required`.
7. Re-pin by producers; census +13 (or +15) with the actual delta recorded; fixtures re-derived; the four count sites at 14; `tests/study` green apart from the branch's known fail-closed set, every other delta explained.
8. SV rows `passing`: the source case reproduced exactly; the 1.19 identity and the 0.99611 threshold; the molecule count; the baseline's disclosed verdict with every existing channel identical and oracle parity 0.0. Trace rows for the three calcs, the constraint def and the thirteen instance facts.

## Validation report (prototype, 2026-09-08)

- `prototype/proto.py` → `proto_results.json`, run with `uv run python`: the P0 channels above; the source case `p_target_nonrad` 50.0, peaks 9.5 / 5.0, doubled 19.0 exactly (after D4; the `(1 − f) × p` form read 49.999999999999986 / 9.499999999999998, which is why D4 exists); `tbr_required` 1.1900000000000002 at 0.99; threshold 0.9961052631578947; `lossless_check` — loss 0.0 and `tbr_required` 1.0 at every burn fraction; `vacuum_checks` — atoms/molecules 1.95, doubled 2.0; P3 / P4 as tabled; `p_alpha_heat = 0.95 × 0.2002 × p_fus` reproduces the pinned channel to better than 1e-9.
- No model file, oracle, test or generated file was touched; no validation run (nothing to validate until the integration copies the text in).

## Implementation checklist (phased; the plan carries the checkboxes)

1. The three new library files and the constraint def written from § Proposed design; the plant and the instance edited; the `E_fus_J` binding form checked against the codegen; Levels 1–3; twins synced; `tests/models`.
2. The MR-WI047 restatement (one verdict; the count 13 → 14; the census delta; the committed studies untouched in meaning) and the predictions in the plan; `evidence/baseline_before/` from WI-046's package; commit A.
3. Regeneration; the oracle and the seam (D11); the single runner and the route restated; the baseline diff; P3 and P4 executed and deposited.
4. Re-pin (snapshot → manifest → census → fixtures → single runner); batteries; SV and trace rows; commit B.
5. `tests/study` run of record; commit C.

## Risks

1. **The pessimistic fence closes the whole inherited window at fixed geometry** (P3 and P4 both violated, and every committed cheap machine has more alpha heating than either). *This is a measurement the study makes, not a defect*; the strategy names it an adverse-but-valid reading. *Mitigation:* the study reports the ten- and fourteen-verdict sets side by side, the low-case arm and the R-scaled shadow as columns; nothing is moved to open it.
2. **The codegen refuses `fuel_q_eff * mev_to_joules` as a calc-input expression.** *Likelihood: medium* (the WI-028 bare-alias class). *Mitigation:* the plant-attribute fallback named under the plant edit; phase 1 records which form landed.
3. **`p_sep` is zero or negative at some sweep point** (core radiation at or above the absorbed heating) → `f_rad_edge` divides by zero or reads outside [0, 1]. *Handling:* the exact route publishes a nonfinite or out-of-range value; the study's exporter refuses a nonfinite before any CSV byte (ANNEX § Numeric publication) and the in-range channel counts the rest; no clamp. The plan's off-design execution checks `p_sep > 0` at P3 / P4 (expected: the sustainment chain's radiation stays well under the absorbed heating on the feasible set).
4. **A reader takes 10.535 as "the source's divertor fails".** *Mitigation:* the assert's comment and the instance text: the model's absorbed heating exceeds the source's 500 MW by 10.9 % (its alpha heating on its own fusion power plus the installed 50 MW), and the fence is the source's most pessimistic case scaled in load — a disclosed consequence of the model's own numbers, on the WI-041 precedent.
5. **The census counts the two library defaults (`s_per_fpy`, `k_B`) as entry points.** *Mitigation:* the plan records the actual delta; either count is correct as long as it is the producers'.
6. **Fourteen new entry points move the fixture contract on axes that reach `p_fus`** (R, a, I_coil, n_e0, T_i0 all reach `fuel__*` and `divheat__*` now). *Mitigation:* re-derived from the indicator report; the plan says what it was.

## Approval

The owner delegated the modelling judgement at grounding (`goal.md` § Reserved gates); this design proceeds to the plan under that delegation, as WI-043 and WI-044 did. The recovery-semantics reading (D3, the `t_recycle` binding) is put to the owner as a reserved gate, not decided here: the design carries the reading the packet fixed and publishes its consequence as a channel. The fresh round review is the independent check.
