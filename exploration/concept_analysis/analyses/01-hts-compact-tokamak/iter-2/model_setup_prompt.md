# 1costingfe Model Update: HTS Compact Tokamak (Commonwealth Fusion / ARC)

## Mode: Feedback Pass (Edit Existing Model)

An existing four-step model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/iter-2/model_setup.py` and apply
**targeted edits** based on the assessment findings below. Use the Edit tool — do
NOT rewrite the file from scratch, and do NOT restructure conforming code.

## Preserve the four-step contract

The file already follows the canonical shape; keep it:
1. `spec` dict (design-point inputs only) + `P_native`
2. `model = CostModel(...)`
3. `overrides = [ ... ]` — six-field registry entries
4. `result, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`

with `model`, `result`, `result_1gw` at module level and the `print_cas_breakdown(...)`
call retained. Do not convert the helper call into an inline two-knob `forward()`
(the contract validator rejects it), and do not re-introduce `# DEFAULT:` comments
or the uniform financial parameters (`availability`, `lifetime_yr`, `interest_rate`,
`inflation_rate`) into `spec`.

**Rules**:
- Preserve all existing sweeps, scenarios, and sensitivity analyses unless a
  finding specifically says to change them.
- Add content incrementally; every change must be traceable to a specific finding
  or a direct consequence of one.
- Any override you add or change uses a **canonical** account code (schema below)
  and the six-field shape; keep `provenance` honest and show derivation arithmetic
  in `rationale`.


## Assessment Findings

Focus on findings tagged `Category: model`. Findings tagged `Category: analysis`
are informational (the analysis agent handles prose), but you may adjust model
parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: The C220108 divertor override moves cost the wrong way on an admittedly-undesigned subsystem
- **Target:** Section 5b (Override Candidates) / `model_setup.py` overrides list
- **Category:** analysis
- **Finding:** The enabled C220108 override ($17.5M × 1.33 = $23.3M) *replaces the
  library default of $56.3M with a lower number* (model output: native library
  56.3 → projected 23.3). The analysis itself describes this figure as a "rough
  estimate" / "placeholder for an undesigned subsystem, not a costed design" and
  rates ARC's divertor difficulty as "between ITER and reactor designs" (i.e.
  likely *more* expensive than a generic scaling default, not less). Enabling it
  therefore departs from the library in the non-conservative direction on the
  basis of an explicitly incomplete number — the weakest of the four overrides,
  and one that lowers projected LCOE for a subsystem the narrative flags as a
  cost/feasibility unknown. This contradicts override discipline (a departure
  should be better-grounded than the default it replaces, not less complete).
- **Recommendation:** Disable the C220108 override and let the library default
  stand, carrying the divertor as the Section-6 data gap it already is (Gap #2),
  or — if a divertor figure must be present — frame it as an *upward* sensitivity
  toward ITER-class divertor cost rather than a downward point override. Do not
  use the deferred $17.5M placeholder to reduce the divertor account.
- **Priority:** important

### F-2: Headline 1 GWe LCOE / overnight cost is very high and is not reconciled with the "compactness advantage" narrative
- **Target:** Section 7 (Family-Delta) / Section 2 TEA framing
- **Category:** analysis
- **Finding:** The cross-concept number is 539 $/MWh at an overnight cost of
  51,674 $/kW (~$51.7/W) — roughly 10–20× the comparator point designs the
  analysis itself cites (ARIES-AT ≈ 50 $/MWh / 5 c/kWh; ALPHA re-costing 2.4
  $/W). This is the *honest* consequence of the well-grounded structure-dominated
  magnet override (do not deflate it), but it sits in unresolved tension with
  Section 7's claim of an "ARC capital-cost advantage per unit fusion power from
  compactness." A TEA reader sees a model that lands ARC among the most expensive
  concepts per kWe while the prose advertises a cost advantage; the two are
  reconcilable (the advantage is per-unit-*fusion*-power vs ITER's low-field
  path, eroded per-unit-*electric* by Qe = 3.5 and modular non-scaling of 4.3×
  233 MWe units) but the analysis never states it.
- **Recommendation:** Add an explicit reconciliation in Section 7 / Section 2:
  state that the compactness benefit is a fusion-power-density advantage versus
  the large low-field path, and that it does *not* translate into a low $/kWe
  once the structure-dominated magnet and low engineering gain are honestly
  costed — so the model's high LCOE is expected, not a discrepancy. This keeps
  the narrative and the headline number from reading as contradictory.
- **Priority:** minor


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md`
- **Example (pattern):** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.TOKAMAK`, `Fuel.DT`

### Canonical account schema (for any new/changed override)

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220103` | Confinement magnets / coils (HTS-REBCO conductor + winding + cryostat) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | supplementary heating (NBI/ICRF/ECRH/LHCD) per installed MW |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | DC magnet power supplies and switchgear |
| `C220108` | Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing) | divertor (W monoblock cassettes on CuCrZr heat sinks) |
| `C220110` | Remote handling & maintenance equipment (rad-hardening tier x vessel geometry) | always (for this archetype) |
| `C220111` | Reactor-equipment installation & assembly (fraction of the CAS22 subtotal) | always (for this archetype) |
| `CAS21` | Buildings & site structures (reactor, turbine, hot cell, balance-of-plant) | always (for this archetype) |
| `CAS23` | Turbine plant equipment (thermal cycle; zero for direct-conversion / eta_th=0 plants) | zero if the design point is direct-conversion (no thermal cycle) |
| `CAS24` | Electric plant equipment (switchyard, transformers, plant distribution) | always (for this archetype) |
| `CAS26` | Heat rejection system (cooling towers, circulating water) | always (for this archetype) |
| `CAS27` | Special materials — initial reactor material inventory / blanket fill (distinct from C220101 structure) | always (for this archetype) |
| `CAS70` | Annualized O&M + scheduled component replacement (staffing-based) | always (for this archetype) |
| `CAS80` | Annualized fuel cost — consumables and enriched-isotope procurement | always (for this archetype) |

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/iter-2/model_setup.py`
