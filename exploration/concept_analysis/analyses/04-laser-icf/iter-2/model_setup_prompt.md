# 1costingfe Model Update: Laser ICF (HB11 Energy)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\iter-2\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\iter-2\model_setup.py` and apply
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

### F-1: CAS80 override is not taking effect — fuel cost unchanged from generic
- **Target:** model_setup.py overrides list (CAS80 entry)
- **Category:** model
- **Finding:** The analysis specifies a CAS80 override of $0.5M/yr (raw fuel is earth-abundant p-B11, target fabrication cost allocated to C220108). The model_setup.py dutifully includes this override with `"value": 0.5, "enabled": True`. However, the model output shows CAS80 = 154.5 for both generic and native — identical values, meaning the override is not being applied. At the 1 GWe projection CAS80 doubles to 309.0 (pure power-scaling of the generic default), confirming the override has no effect. This inflates LCOE by carrying a DT-scale fuel cost that the analysis explicitly argues is inapplicable. The fuel cost at $154.5M for a concept using industrial-commodity boron and hydrogen (no tritium) is implausible on its face.
- **Recommendation:** Investigate whether the CostModel framework supports CAS80 overrides through the standard override mechanism. If CAS80 is a top-level annual cost that routes differently from CAS22 sub-accounts, the override may need to be applied via the `spec` dict or a different parameter. Confirm the override takes effect in the output (native CAS80 should differ from generic CAS80 when the override is enabled) and re-run the model.
- **Priority:** blocking

### F-2: CAS70 override appears ineffective — O&M cost unchanged from generic
- **Target:** model_setup.py overrides list (CAS70 entry)
- **Category:** model
- **Finding:** The same pattern as CAS80: the analysis specifies CAS70 at 50% of generic ($0.50 * generic.costs.cas70`), and the model_setup.py includes this override, but the model output shows CAS70 = 38.6 for both generic and native — identical. The 1 GWe value (52.8) is consistent with pure power-scaling of generic, not a 50% reduction. The analysis narrative emphasizes that elimination of neutron-activated component replacement is a major economic advantage of the p-B11 fuel cycle; the model does not reflect this. Both CAS70 and CAS80 are likely top-level cost accounts that the override mechanism doesn't reach, which means two of the nine overrides are silently ineffective, and the LCOE is overstated relative to the analysis intent.
- **Recommendation:** Same root cause as F-1 — determine how CAS70 and CAS80 are handled in the cost model framework and apply the reductions through the correct mechanism. If these accounts cannot be overridden via the standard list, document this as a framework limitation and adjust the native LCOE commentary accordingly.
- **Priority:** blocking

### F-3: CAS21 override appears ineffective — buildings cost unchanged from generic at 1 GWe
- **Target:** model_setup.py overrides list (CAS21 entry)
- **Category:** model
- **Finding:** The CAS21 override is set to `0.50 * generic.costs.cas21` and the native output does show CAS21 = 139.9 vs. generic 279.9 — the override takes effect at native scale. However, at 1 GWe the CAS21 value is also 139.9, identical to native, while most other accounts scale upward from native to 1 GWe (e.g., CAS22: 677.9 → 1307.6, CAS23: 131.8 → 263.5). This suggests the 1 GWe projection is carrying the native CAS21 value without applying power-law scaling, or the override's absolute value is being carried forward as a constant rather than scaling with plant size. This inconsistency means the 1 GWe LCOE may undercount buildings cost relative to the scaling convention applied to other accounts, or the framework intentionally holds CAS21 constant — either way, it should be verified and documented.
- **Recommendation:** Verify whether CAS21 is expected to scale with plant power in the 1 GWe projection. If it should scale (as CAS22, CAS23, CAS24, CAS25, CAS26 all do), the override value expression may need to reference the 1 GWe generic rather than the native generic. If CAS21 is intentionally held constant (site-dependent, not power-dependent), add a comment in model_setup.py explaining this behavior.
- **Priority:** important


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\analysis.md`
- **Example (pattern):** `\home\reid\1cfe\1costingfe\examples\dt_tokamak.py`
- **README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing Constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.LASER_IFE`, `Fuel.PB11`

### Canonical account schema (for any new/changed override)

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | primary pulsed driver (laser/accelerator/gun) on $/J of driver energy; electrical-drive concepts cost it in C220107 |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | pulsed-power capacitor bank on $/J stored — usually the dominant driver cost for electrically-driven pulsed schemes |
| `C220108` | Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing) | high-rep-rate target manufacturing factory (IFE/MIF) |
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
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\04-laser-icf\iter-2\model_setup.py`
