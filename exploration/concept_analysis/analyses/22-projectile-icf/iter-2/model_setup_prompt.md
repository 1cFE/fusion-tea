# 1costingfe Model Update: Projectile ICF (First Light Fusion)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\22-projectile-icf\iter-2\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\22-projectile-icf\iter-2\model_setup.py` and apply
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

### F-1: Override count below Low-fit band, and the analysis's justification conflates "no data" with "no departure"
- **Target:** Section 5b (Override Candidates)
- **Category:** analysis
- **Finding:** The concept has Low archetype-fit (HEAVY_ION archetype applied to an electromagnetic-gun, sub-Hz, liquid-lithium-curtain design) yet enables only 4 overrides against an expected band of 6–12. The analysis justifies this by saying additional overrides would require "inventing values not supported by the dossier." But Low archetype-fit means the library defaults are systematically wrong for this concept — the absence of company-published data does not mean the library default is correct. Several accounts have qualitative evidence that the library default is structurally inapplicable, yet no override was attempted: C220101/C220102 (liquid lithium curtain replaces solid blanket/shield — the analysis itself notes these are functionally merged and the vessel is claimed to be lifetime-of-plant), C220200 (heat transport via liquid lithium EM pumps — fundamentally different from the heavy-ion archetype's FLiBe loop), and C220110 (remote handling substantially reduced if no first-wall replacement). These accounts deserve at minimum a derived override with an analogue-based estimate or an explicit `enabled: false` entry documenting why the library default is being accepted despite known structural mismatch.
- **Recommendation:** Add override candidate entries for C220101, C220102, C220200, and C220110 — either enabled with analogue-derived values (e.g., HYLIFE-II scaling for the lithium system) or disabled with an explicit rationale explaining the structural mismatch and why no quantitative correction is possible. The goal is 6–8 total entries (enabled or documented-disabled) that demonstrate the analysis has engaged with the archetype mismatch rather than defaulting to silence.
- **Priority:** important

### F-2: Section 7 (Family-Delta) does not engage the fixed comparables list and instead compares against arbitrary neighbours
- **Target:** Section 7 (Family-Delta vs Comparables)
- **Category:** analysis
- **Finding:** The frontmatter shows `Comparables: []` (empty list), and Section 7 opens with "No comparable concept in the corpus for this design point." The section then proceeds to compare informally against "Laser ICF concepts (Xcimer, Inertia, Focused Energy)" and "MagLIF/Pulsed power (Pacific Fusion)" — none of which are assigned comparables. With an empty comparables list, the section should either (a) state that no family-delta analysis is possible because no comparables are assigned and limit itself to the "unique features" subsection, or (b) engage the HEAVY_ION archetype (concept 25, Heavy-Ion Beam ICF) as the archetype reference to articulate the structural delta. Currently, the informal comparisons to laser ICF and MagLIF are useful context but are framed as if they substitute for the prescribed family-delta exercise against fixed comparables. The driver cost comparison ("30x reduction in driver cost per joule") is made against laser ICF, not against the HEAVY_ION archetype that actually supplies the library defaults.
- **Recommendation:** Restructure Section 7 to first acknowledge the empty comparables list, then articulate the delta against the HEAVY_ION archetype (the library reference that actually governs the generic forward). Name the specific subsystem divergences (EM gun vs. heavy-ion accelerator driver, sub-Hz vs. 5–10 Hz rep rate, liquid lithium curtain vs. FLiBe jets, no beam-transport magnets) and state the cost direction for each. The informal laser ICF and MagLIF comparisons can remain as supplementary context but should not substitute for the archetype-delta analysis.
- **Priority:** important

### F-3: C220111 installation cost is $1,854.6M in the native run — 45% of total plant cost — due to the library computing it from the pre-override reactor subtotal, making the native LCOE implausibly high
- **Target:** model_setup.py overrides list
- **Category:** model
- **Finding:** The model output shows C220111 (installation labor, 14% of reactor subtotal) at $1,854.6M for the native run — identical to the generic run. This is because the library computes C220111 from the pre-override reactor subtotal ($13,247M, dominated by the generic C220104 = $12,591M), not from the post-override subtotal ($363M). After overrides reduce C220104 from $12,591M to $200M and C220107 from $420M to $0, the physically meaningful installation cost should be ~$51M (14% of $363M), not $1,855M. The $1,804M phantom cost inflates the native overnight from a plausible ~$15,500/kW to $27,495/kW, and the native LCOE from a plausible ~$170/MWh to $311.9/MWh. This is a known library behavior (C220111 generic = native across most concepts), but for this concept the override magnitude is so large (98.4% reduction in C220104) that the artifact is material — installation labor exceeds the driver it is notionally installing by 9×. Add an override for C220111 with the corrected value (~$51M, derived as 14% of the post-override reactor subtotal) to make the native LCOE physically meaningful.
- **Recommendation:** Add an enabled override for C220111 with value ~51.0 (derived: 14% of the post-override reactor subtotal of $363.3M), with provenance `derived` and rationale explaining the library's pre-override computation artifact. This corrects the native LCOE to a plausible range and ensures the 1 GWe projection is not distorted by phantom installation costs. The same correction should be reflected in the analysis Section 5b override registry.
- **Priority:** blocking


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\22-projectile-icf\analysis.md`
- **Example (pattern):** `\home\reid\1cfe\1costingfe\examples\dt_tokamak.py`
- **README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing Constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.HEAVY_ION`, `Fuel.DT`

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
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\22-projectile-icf\iter-2\model_setup.py`
