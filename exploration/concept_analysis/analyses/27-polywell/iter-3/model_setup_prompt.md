# 1costingfe Model Update: Polywell (EMC2)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\27-polywell\iter-3\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\27-polywell\iter-3\model_setup.py` and apply
**targeted edits** based on the assessment findings below. Use the Edit tool — do
NOT rewrite the file from scratch, and do NOT restructure conforming code.

## Preserve the three-forward contract

The file already follows the canonical shape; keep it:
1. `spec` dict (design-point inputs only) + `P_native`
2. `model = CostModel(...)`
3. `generic = generic_reference(model, spec, P_native)` — the mandatory
   overrides-off forward (forward 1), the reference a relative override is written against
4. `overrides = [ ... ]` — six-field registry entries
5. `native, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`

with `model`, `generic`, `native`, `result_1gw` at module level and the
`print_cas_breakdown(generic, native, result_1gw, overrides)` call retained. Do
not convert the helper call into an inline two-knob `forward()` (the contract
validator rejects it), do not drop the mandatory `generic` line, and do not
re-introduce `# DEFAULT:` comments or the uniform financial parameters
(`availability`, `lifetime_yr`, `interest_rate`, `inflation_rate`) into `spec`.
**Do not re-introduce power-conversion efficiencies (`eta_th`, `eta_de`,
`eta_dec`) into `spec`** — these are ENUM-driven; the way to express a
different value is to add an upstream ENUM member in costingfe, not a per-
concept override. `f_dec` (DEC fraction) MAY appear in `spec` with provenance —
it's a physics+architecture property, not a hardware-efficiency claim.
A relative override references `generic` (never `native` or `result_1gw`).

**Low archetype-fit concepts: do not empty `spec`.** When the frontmatter
declares `Archetype-Fit: Low`, the prior model may still have a populated `spec`
expressing the concept's actual geometry / physics using canonical kwargs (even
where the archetype isn't a perfect cost match). **Preserve those entries** and
only edit specific fields if a finding calls for it. Replacing a populated
low-fit `spec` with `spec = dict()` is a regression — the library would fall
back to pure archetype YAML defaults that carry zero signal for this concept's
actual machine. Cost-side overrides (the registry below) are where the "Low
fit" caveat properly lives.

**Archetype-specific spec key blocklist (library-bug workarounds).** Until library issues are
fixed, some spec keys must not be passed for specific archetypes — even when the published design
point has a value for them. If the prior model contains any of these keys in `spec`, **remove
them** as part of this edit:
- **DIPOLE**: remove `plasma_volume` if present. The MFE radiation calc treats `plasma_volume`
  as a uniform integrator and over-counts radiation for dipole-peaked profiles. Library issue:
  **1cFE/1costingfe#24**. Document the removal with a brief comment citing the issue.

**Override values are M$, never raw dollars** (validator rejects `|value| > 5e4`).
**Derived rollup accounts cannot be overridden**: C220111, C220000, C220100,
C220200, C220300, C220400, C220500, C220600, C220700. To express "this concept
assembles more simply," override `installation_frac` via `costing_overrides`,
not the C220111 dollar amount.
**Disabled overrides must carry a `blocked_by` field** matching `<org>/<repo>#<NN>`
(e.g. `"1cFE/1costingfe#42"`) so library-side findings route to a tracker
instead of dying in the rationale text.
**Every override must declare `cost_basis: "noak"` (strict).** The framework runs
`noak=True`; any other vintage (`foak`, `conceptual_design`, `vendor_target`,
`unspecified`) is rejected. If your source publishes a non-NOAK value, either
(a) disable + `blocked_by`, (b) apply a documented learning-curve adjustment in
`rationale` and declare `cost_basis: "noak"`, or (c) file a tracker issue.

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

### F-1: Model uses wrong fuel type (PB11 instead of DT)
- **Target:** model_setup.py line 61
- **Category:** model
- **Finding:** The model instantiates `CostModel(concept=ConfinementConcept.POLYWELL, fuel=Fuel.PB11)` but the entire analysis describes a D-T design point (Park et al. 2025 D-T reactor scaling study). The analysis explicitly states "50:50 D-T fuel mixture" (Section 5), discusses tritium breeding blanket requirements (Sections 2, 4, 6), references 14.1 MeV neutrons throughout, and derives thermal power from neutron energy capture. Using `Fuel.PB11` fundamentally misrepresents the concept's cost structure — D-T requires tritium breeding (blanket cost, fuel cycle cost, tritium inventory) while p-B11 is aneutronic.
- **Recommendation:** Change line 61 to `model = CostModel(concept=ConfinementConcept.POLYWELL, fuel=Fuel.DT)` to match the D-T design point the analysis documents.
- **Priority:** blocking

### F-2: Override count (0) significantly below Med archetype-fit band without adequate upstream justification
- **Target:** Analysis Section 5b and frontmatter Archetype-Fit grade
- **Category:** analysis
- **Finding:** The concept is graded `Archetype-Fit: Med` (expected 3-8 enabled overrides per rubric) but proposes zero overrides. While Section 5b acknowledges this discrepancy and provides local justification ("Park et al. 2025 provides only physics scaling parameters, not engineering cost data"), the frontmatter `Archetype-Fit: Med` grade is inconsistent with zero-override reality. The analysis argues this reflects "data availability gap" rather than true archetype fit, but the upstream grade should reflect current state, not anticipated future data. A Med-fit concept implies the archetype's cost structure reasonably matches the design's known features; zero overrides means the design has no company-grounded cost differentiators from a generic POLYWELL library template.
- **Recommendation:** Add an explicit note in Section 5b stating that the effective archetype-fit for cost modeling purposes is **Low** (library defaults only) despite the upstream Med grade, and that the Med grade anticipates future data availability if EMC2 publishes an engineering design. Alternatively, recommend upstream re-grading to Low to reflect current data availability for cost modeling.
- **Priority:** important

### F-3: P_native derivation carries ±60% uncertainty but model does not capture this via sensitivity analysis
- **Target:** model_setup.py and analysis Section 5
- **Category:** model
- **Finding:** The analysis Section 5 explicitly states that P_native = 290 MWe has "uncertainty ±60%" due to the γ=0.1 loss reduction factor assumption (line 216: "If γ=0.2, net electric drops to ~193 MWe... If γ=0.05, net electric increases to ~368 MWe"). The model_setup.py comments acknowledge this (lines 57-58: "CAUTION: uncertainty ±60% due to γ=0.1 assumption") but the model produces only point estimates (42.0 $/MWh native LCOE) with no sensitivity sweep showing the cost impact of this massive parameter uncertainty. For a concept where the core confinement mechanism has "never been validated experimentally" (Section 2, Challenge 1), the cost model should bound the range by running scenarios at γ=0.05, 0.1, and 0.2.
- **Recommendation:** Add a sensitivity sweep in model_setup.py testing P_native at 193 MWe (pessimistic, γ=0.2), 290 MWe (baseline), and 368 MWe (optimistic, γ=0.05) to show how the unvalidated physics assumption propagates to LCOE uncertainty. Emit the range in the output so the cost estimate reflects the analysis's honest uncertainty framing.
- **Priority:** minor


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\27-polywell\analysis.md`
- **Example (pattern):** `\home\reid\1cfe\1costingfe\examples\dt_tokamak.py`
- **README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing Constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.POLYWELL`, `Fuel.PB11`

### Canonical account schema (for any new/changed override)

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220103` | Confinement magnets / coils (HTS-REBCO conductor + winding + cryostat) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | primary pulsed driver (laser/accelerator/gun) on $/J of driver energy; electrical-drive concepts cost it in C220107 |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | pulsed-power capacitor bank on $/J stored — usually the dominant driver cost for electrically-driven pulsed schemes |
| `C220108` | Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing) | high-rep-rate target manufacturing factory (IFE/MIF) |
| `C220109` | Direct energy converter (electrostatic for mirror/FRC exhaust, or inductive DEC on a pulsed driver) | only if the design point uses direct energy conversion (directed axial exhaust or an inductive DEC stage) |
| `C220110` | Remote handling & maintenance equipment (rad-hardening tier x vessel geometry) | always (for this archetype) |
| `C220111` | Reactor-equipment installation & assembly (fraction of the CAS22 subtotal) | always (for this archetype) |
| `CAS21` | Buildings & site structures (reactor, turbine, hot cell, balance-of-plant) | always (for this archetype) |
| `CAS23` | Turbine plant equipment (thermal cycle; zero for direct-conversion / eta_th=0 plants) | zero if the design point is direct-conversion (no thermal cycle) |
| `CAS24` | Electric plant equipment (switchyard, transformers, plant distribution) | always (for this archetype) |
| `CAS26` | Heat rejection system (cooling towers, circulating water) | always (for this archetype) |
| `CAS27` | Special materials — initial reactor material inventory / blanket fill (distinct from C220101 structure) | always (for this archetype) |
| `CAS70` | Annualized O&M + scheduled component replacement (staffing-based) | always (for this archetype) |
| `CAS80` | Annualized fuel cost — consumables and enriched-isotope procurement | always (for this archetype) |

### Canonical `spec` field glossary (for any new/changed spec key)

If your edit touches the `spec` dict (adding/renaming/replacing a field),
the new key MUST come from the glossary below. Read the "Common confusions"
block before editing — most prior errors (concept 05/09 fusion-vs-heating
mix-up, dipole `plasma_volume` regression, kJ-vs-MJ driver-energy mistakes)
trace back to ignoring these warnings.

{{canonical_spec_keys}}

## Output
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\27-polywell\iter-3\model_setup.py`
