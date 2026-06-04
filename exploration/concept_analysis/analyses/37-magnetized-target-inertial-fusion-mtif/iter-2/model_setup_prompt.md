# 1costingfe Model Update: MTIF (Magneto-Inertial Fusion Technologies)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\37-magnetized-target-inertial-fusion-mtif\iter-2\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\37-magnetized-target-inertial-fusion-mtif\iter-2\model_setup.py` and apply
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

### F-1: Override registry cross-artifact inconsistency
- **Target:** model_setup.py overrides list
- **Category:** model
- **Finding:** The analysis Section 5b documents two disabled override candidates (C220107 capacitor bank at $20M, CAS21 retrofit savings at 0.70× generic) with complete six-field entries (account, value, enabled: false, provenance: derived, source, rationale). The model_setup.py overrides list is empty with only a comment stating "All overrides disabled due to insufficient company-grounded data." While both artifacts agree that zero overrides are *enabled*, the analysis registry captures disabled candidates for traceability and the model does not. This breaks the cross-artifact consistency requirement: disabled overrides should appear in both locations with identical account codes and provenance labels.
- **Recommendation:** Copy the two disabled override entries from analysis Section 5b into the model_setup.py overrides list as Python dictionaries. Preserve all six fields (account, value, enabled: False, provenance: "derived", source, rationale) for each entry. The comment about insufficient data can remain above the list.
- **Priority:** important

### F-2: Med archetype-fit with zero enabled overrides requires explicit justification
- **Target:** Section 5b (Override Candidates) — closing paragraph
- **Category:** analysis
- **Finding:** The coherence flags correctly report "Med archetype fit with 0 enabled overrides (expected 3–8) — a poorer-fit concept with this few corrections suggests the library default is being trusted where the archetype says it shouldn't be." The analysis closing paragraph acknowledges the discrepancy ("Zero enabled overrides. Expected band for Med archetype-fit is 3–8") and attributes it to "extreme opacity of NearStar's public materials," stating "Almost no quantitative cost, performance, or engineering data has been disclosed." While this is factually accurate, the justification does not address *why Med archetype-fit was assigned* if the data is too opaque to support even the minimum expected corrections. A Med-fit concept should have *some* company-grounded deltas from the library default; if the company has published nothing, the archetype-fit grade itself may be too generous, or the library's MAG_TARGET defaults are accidentally well-aligned with NearStar's unpublished design.
- **Recommendation:** Add one sentence to the closing paragraph explicitly addressing why Med archetype-fit is appropriate despite zero overrides. Options: (1) "The Med fit reflects that the MAG_TARGET library defaults (pulsed MIF at ~1 Hz, D-D fuel option, liquid-metal first wall) architecturally match NearStar's stated approach, even though no company-specific cost or performance data has been published to warrant corrections," or (2) if the archetype-fit is upstream-fixed and not revisable, state "The upstream-assigned Med fit anticipates future disclosure; the current zero-override state will shift to 3–8 enabled overrides once NearStar publishes driver cost, target fabrication, or chamber engineering data."
- **Priority:** important

### F-3: Section 7 comparables engagement is incomplete due to empty comparables list
- **Target:** Section 7 (Family-Delta vs Comparables)
- **Category:** analysis
- **Finding:** The section opens with "No comparable concept in the corpus for this design point" and proceeds to describe deltas against MIF/IFE analogs (MagLIF, laser ICF, General Fusion pneumatic MTF). The analysis correctly identifies that NearStar's hypervelocity railgun-driven MTIF is architecturally unique and engages the closest neighbors. However, the comparables list in frontmatter is empty (`Comparables: []`), and the section does not explain *why* the fixed comparables list is empty or whether the upstream comparison-status (`costingfe-asterisked`) means the comparable-set assignment is deferred. If the empty list is intentional (no sufficiently similar concept exists), the section should state this upfront before proceeding to the analogs. If the list is incomplete and will be populated later, state that.
- **Recommendation:** Add one sentence immediately after the opening "No comparable concept" statement: "The upstream comparables list is empty because no other surveyed concept combines hypervelocity projectile impact, magnetized target compression, and D-D fuel — the three defining architectural choices that drive NearStar's cost structure. The analogs discussed below (MagLIF, laser ICF, pneumatic MTF) share subsets of these features but diverge on driver technology or fuel cycle, making direct cost comparison inappropriate without company-disclosed data."
- **Priority:** minor


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\37-magnetized-target-inertial-fusion-mtif\analysis.md`
- **Example (pattern):** `\home\reid\1cfe\1costingfe\examples\dt_tokamak.py`
- **README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing Constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.MAG_TARGET`, `Fuel.DD`

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
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\37-magnetized-target-inertial-fusion-mtif\iter-2\model_setup.py`
