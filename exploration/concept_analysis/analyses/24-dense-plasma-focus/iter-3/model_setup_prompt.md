# 1costingfe Model Update: Dense Plasma Focus (LPP Fusion)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\24-dense-plasma-focus\iter-3\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\24-dense-plasma-focus\iter-3\model_setup.py` and apply
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

### F-1: CAS80 enabled/disabled status disagrees between analysis and model
- **Target:** model_setup.py overrides list (CAS80 entry)
- **Category:** model
- **Finding:** The analysis Section 5b YAML block lists CAS80 with `enabled: true` and the Override Count Check explicitly counts it among the 6 enabled overrides. However, `model_setup.py` sets CAS80 `enabled: False` with a comment citing the same framework limitation as CAS70 (operating-cost accounts bypass `co.get()`). The coherence flag reports only 5 enabled overrides, matching the model but not the analysis. This is a cross-artifact discrepancy: either the analysis YAML should mark CAS80 as disabled (matching the model and adding a framework-limitation note parallel to CAS70's), or the model should enable it if the framework actually supports it. As written, the analysis claims 6 enabled overrides (within the Low-fit 6–12 band) while the model implements only 5 (below band), and the flag correctly catches the shortfall.
- **Recommendation:** Synchronize the two artifacts. If the framework truly cannot inject CAS80 overrides (same limitation as CAS70), update the analysis Section 5b YAML to `enabled: false` with the same framework-limitation note used for CAS70, and revise the Override Count Check paragraph to state 5 enabled overrides, acknowledging the count falls just below the Low-fit band floor. If the framework does support CAS80 overrides, enable it in `model_setup.py`.
- **Priority:** important

### F-2: Section 7 family-delta prose does not engage fixed comparables — the comparables list is empty
- **Target:** Section 7 (Family-Delta vs Comparables)
- **Category:** analysis
- **Finding:** The frontmatter declares `Comparables: []` and Section 7 opens with "No comparable concept in the corpus for this design point." The section then provides useful qualitative positioning against the MFE family, pulsed concepts, and other p-B11 concepts — but none of these are fixed upstream comparables. The analysis goal (Section 7's purpose) is to articulate cost deltas against the *fixed* comparables list, naming specific subsystems and cost directions. With an empty comparables list, the family-delta contract is structurally unmet: there is no fixed baseline to delta against, so the prose is generic positioning rather than subsystem-level costed comparison. The upstream pipeline should either assign at least one comparable (even a distant one, with caveats) or the analysis should explicitly state that no delta can be articulated because no comparable was assigned, rather than filling the section with substitute comparisons that bypass the contract's intent.
- **Recommendation:** If the upstream pipeline permits an empty comparables list as valid (acknowledging that DPF is truly sui generis), add a brief explicit statement that the family-delta contract is satisfied vacuously — no comparables were assigned, so no subsystem-level cost delta can be computed, and the qualitative positioning that follows is supplementary context only. If the pipeline should have assigned a comparable (e.g., the nearest pulsed concept like Zap Energy's sheared-flow Z-pinch, or a p-B11 concept like TAE), flag this as an upstream gap for the pipeline maintainer.
- **Priority:** important

### F-3: Override count below Low-fit band floor — 5 enabled overrides vs. expected 6–12
- **Target:** Section 5b (Override Candidates) and model_setup.py overrides list
- **Category:** analysis
- **Finding:** The coherence flag correctly identifies that only 5 overrides are actually enabled in the model (CAS21, CAS23, CAS24, CAS26, CAS27), falling below the Low-fit band floor of 6. The analysis claims 6 by counting CAS80 as enabled, but the model disables it (see F-1). Beyond the CAS80 synchronization issue, the analysis identifies several accounts where the concept is radically different from library defaults but declines to override due to lack of company-grounded data — notably C220104/C220107 (pulsed driver / capacitor bank), C220109 (direct energy converter), and C220105 (primary structure). For a Low-fit concept, the rubric expects more corrections precisely because the library defaults are a poor match. The analysis's reasoning (no company-published cost figure) is principled, but for accounts where the concept structurally eliminates or radically reduces a subsystem (e.g., C220105 primary structure for a 3-tonne device, or C220110 remote handling for a contact-maintained aneutronic device), a derived override with an order-of-magnitude scaling factor — parallel to the CAS21 and CAS26 treatment — would be more faithful to the concept than accepting the full library default.
- **Recommendation:** Consider adding derived overrides for at least 1–2 accounts where the concept structurally eliminates or radically reduces the subsystem (C220105 primary structure and/or C220110 remote handling are the strongest candidates, given that the analysis prose already explains why these costs are negligible). This would bring the enabled count into the 6–12 band and better represent the concept's actual cost structure. Each new override should follow the same pattern used for CAS21/CAS26 — a scaling fraction of the generic value with analyst rationale.
- **Priority:** important


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\24-dense-plasma-focus\analysis.md`
- **Example (pattern):** `\home\reid\1cfe\1costingfe\examples\dt_tokamak.py`
- **README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing Constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.DENSE_PLASMA_FOCUS`, `Fuel.PB11`

### Canonical account schema (for any new/changed override)

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | primary pulsed driver (laser/accelerator/gun) on $/J of driver energy; electrical-drive concepts cost it in C220107 |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | pulsed-power capacitor bank on $/J stored — usually the dominant driver cost for electrically-driven pulsed schemes |
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
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\24-dense-plasma-focus\iter-3\model_setup.py`
