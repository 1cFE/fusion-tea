# 1costingfe Model Update: Projectile ICF (First Light Fusion)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\22-projectile-icf\iter-3\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\22-projectile-icf\iter-3\model_setup.py` and apply
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

### F-1: C220111 override is listed in analysis but handled differently in the model — value mismatch and circular sourcing
- **Target:** Section 5b (Override Candidates) — C220111 entry; and model_setup.py installation_frac derivation
- **Category:** analysis
- **Finding:** The analysis Section 5b lists C220111 as an enabled override at $51M with `provenance: derived` and `source: "model_output.txt §CAS22 sub-account detail"`. Two problems: (1) The source is circular — the override's evidence is the model's own output, not an external cost datum or engineering rationale. (2) The model does not carry C220111 as an override entry; instead it adjusts `installation_frac` in spec to produce $42.2M (not $51M) in the native column. The analysis summary claims "7 enabled overrides" but the coherence flag counts 6, matching the model's actual override list. The analysis YAML and the model implementation disagree on both the mechanism and the dollar value ($51M vs $42.2M).
- **Recommendation:** Remove C220111 from the analysis override registry (it is not an override — it is a spec-level correction). Document the `installation_frac` adjustment in a separate subsection or note under the override walkthrough, explaining that the model corrects the installation fraction to produce physically meaningful installation labor. Update the override count to 6 enabled (which remains within the Low-fit band of 6–12). If the $42.2M vs $51M difference matters, reconcile the arithmetic (the model's `_post_override_subtotal` calculation yields a different result than the analysis's manual estimate of $363.3M × 14%).
- **Priority:** important

### F-2: Section 7 family-delta prose does not engage fixed comparables — Comparables field is empty
- **Target:** Section 7 (Family-Delta vs Comparables)
- **Category:** analysis
- **Finding:** The frontmatter declares `Comparables: []` (empty list) and Section 7 opens with "No comparable concept in the corpus for this design point." The section then articulates deltas only against the HEAVY_ION archetype defaults and provides a "Supplementary Cross-Concept Context" section referencing laser ICF and MagLIF concepts that are not in the comparables list. The checklist requires that family-delta prose compare the design point against the *fixed* comparables list. An empty comparables list means the analysis never performs a structured cost-delta comparison against a concrete peer — only against the abstract archetype. The supplementary section partially fills this gap but is informal and does not name subsystem-level cost directions with the same rigor as the archetype delta table.
- **Recommendation:** If the upstream pipeline intentionally leaves Comparables empty for this concept (no IFE peer is close enough), state that explicitly in Section 7 and explain why — e.g., "No concept in the corpus shares the sub-Hz electromagnetic-gun driver architecture; the HEAVY_ION archetype is the only available reference frame." This makes the empty list a documented analytical decision rather than an omission. The supplementary cross-concept context (vs laser ICF, vs MagLIF) is useful but should not substitute for the formal comparables comparison; label it clearly as context outside the comparables framework.
- **Priority:** important

### F-3: C220108 target factory override is derived from an LCOE-target back-calculation, not from evidence of actual target cost
- **Target:** Section 5b (Override Candidates) — C220108 entry
- **Category:** analysis
- **Finding:** The C220108 override ($5.6M/year) is derived by computing the maximum target cost that keeps target expenditure below 10% of electricity revenue at the company's own LCOE target of $50/MWh. This is a viability constraint (what target cost *must* be for the concept to work), not evidence of what the target factory *will* cost. The analysis acknowledges "No published target cost exists" and Hawker's model "treats it parametrically." Using the company's aspirational LCOE to back-derive an override value embeds optimism — if targets actually cost $20/unit the concept is uneconomic, and the override would mask that. The provenance is labeled `derived`, which is technically correct, but the derivation is from a target (pun intended) rather than from engineering cost data.
- **Recommendation:** Either (a) disable C220108 and let the library default stand, flagging target cost as a sensitivity parameter with a range ($1–$20/target) in Section 6 / Section 8; or (b) keep it enabled but relabel the rationale to make explicit that this is a *viability-required ceiling* rather than an estimated cost, and add a sensitivity sweep in the model spanning at least the Hawker parametric range ($0.10–$100/target annualized). The current framing presents a viability requirement as if it were a cost estimate.
- **Priority:** important


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
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\22-projectile-icf\iter-3\model_setup.py`
