# 1costingfe Model Update: Spherical Tokamak CS-Free PB11 (ENN)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\39-spherical-tokamak-cs-free-p-b11\iter-2\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\39-spherical-tokamak-cs-free-p-b11\iter-2\model_setup.py` and apply
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

### F-1: Model LCOE contradicts analysis narrative on physics penalties
- **Target:** model_output.txt LCOE values and model_setup.py exploratory-status commentary
- **Category:** model
- **Finding:** The model outputs LCOE = 37.0 $/MWh (1 GWe) and 45.8 $/MWh (native 500 MWe), but the analysis extensively documents that p-B11 physics imposes severe penalties: 15× worse Lawson criterion (neτT ≥ 1.5×10²² m⁻³s vs D-T's ~10²¹), 200-300 keV operating temperature (vs D-T's 10-20 keV), and critical physics feasibility questioned by arXiv 2406.15495. Section 7 family-delta concludes "likely 50-200% LCOE penalty vs D-T HTS spherical tokamaks" and "NET: likely 50-150% LCOE penalty vs D-T HTS spherical tokamaks at same P_net." A D-T HTS tokamak baseline LCOE is typically 60-100 $/MWh, so the expected penalty would place this concept at 90-300 $/MWh, not 37-46 $/MWh. The model's low LCOE appears to use library defaults that do not reflect the physics constraints the analysis identifies as dominant.
- **Recommendation:** Update the exploratory-status commentary block in model_setup.py (lines 99-139) to explicitly state that the model outputs do NOT reflect the p-B11 physics penalties documented in the analysis (15× Lawson, 200-300 keV operation, questioned Q_eng), and that the library's generic PB11 TOKAMAK defaults likely underestimate LCOE by failing to capture the confinement scaling, auxiliary heating recirculating power, and low Q_eng implied by the analysis. Add a warning that realistic LCOE is likely 2-4× higher than the model output based on the family-delta analysis.
- **Priority:** important

### F-2: P_native exploratory value lacks upstream design-point context
- **Target:** Analysis Design Point section (lines 15-17) and model_setup.py P_native declaration (line 66)
- **Category:** analysis
- **Finding:** The analysis Design Point block states "(No design-point row for this concept yet — selection is upstream-pending. Do not invent one.)" and correctly does not fabricate a design point. However, the model uses P_native = 500.0 MWe as an "EXPLORATORY" value (model_setup.py line 66) to satisfy the three-forward contract. The analysis does not explain in the Design Point section why no design point exists or that an exploratory value will be used downstream — the reader encounters "upstream-pending" with no further context until reaching Section 5 ("No design point exists for this concept"). The Design Point section should clarify that the concept has no commercial plant design (as documented in Sections 1, 2, 5) and that downstream modeling uses exploratory stand-in values for framework compliance.
- **Recommendation:** Replace the Design Point section placeholder (lines 15-17) with 2-3 sentences stating: (1) ENN has not published a commercial plant design; EHL-2 is a physics experiment with P_net = 0 MWe, (2) no design-point parameters (P_net, R0 commercial, B commercial, Q_eng, capacity factor) are available from company sources, and (3) the quantitative model uses EHL-2's experimental geometry and an exploratory P_native = 500 MWe as stand-ins to demonstrate library defaults, but outputs should not be interpreted as grounded in ENN's actual commercial plans. This context prepares the reader for the exploratory nature of Section 5 and the model.
- **Priority:** important

### F-3: Comparables-list mismatch between frontmatter and Section 7 framing
- **Target:** Frontmatter Comparables field (line 12) and Section 7 family-delta narrative (lines 295-361)
- **Category:** analysis
- **Finding:** The frontmatter declares `Comparables: []` (empty list), but Section 7 states "No comparable concept in the corpus for this design point" (line 297) and then articulates the family-delta "against the **generic D-T spherical tokamak** archetype, drawing on ARIES-ST and Tokamak Energy design studies as reference points" (lines 298-304). The section proceeds to name specific deltas with cost magnitudes by comparing to D-T spherical tokamaks (e.g., "ARIES-AT FLiBe inventory ~$90M" line 311, "ARIES-AT HTS coils ~$400M" line 325). The comparables list being empty is technically correct for the 39-concept corpus (no other MFE p-B11 entry), but the family-delta uses external comparables (ARIES-ST, ARIES-AT) not reflected in the frontmatter. This creates a metadata-vs-content inconsistency where the frontmatter says "no comparables" but the delta narrative relies on comparables from outside the corpus.
- **Recommendation:** The frontmatter `Comparables: []` is correct for the corpus (no in-corpus comparable), so no change needed there. However, in Section 7 line 297-304, add a clarifying sentence after "No comparable concept in the corpus for this design point." stating: "The family-delta is therefore articulated against external reference designs (ARIES-ST D-T spherical tokamak, ARIES-AT advanced tokamak) to establish the cost implications of p-B11 fuel and CS-free operation relative to D-T baseline, since no in-corpus concept shares this combination of MFE confinement, spherical tokamak geometry, and aneutronic fuel." This resolves the apparent contradiction and makes explicit that the comparables are external.
- **Priority:** minor


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\39-spherical-tokamak-cs-free-p-b11\analysis.md`
- **Example (pattern):** `\home\reid\1cfe\1costingfe\examples\dt_tokamak.py`
- **README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing Constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.TOKAMAK`, `Fuel.PB11`

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

### Canonical `spec` field glossary (for any new/changed spec key)

If your edit touches the `spec` dict (adding/renaming/replacing a field),
the new key MUST come from the glossary below. Read the "Common confusions"
block before editing — most prior errors (concept 05/09 fusion-vs-heating
mix-up, dipole `plasma_volume` regression, kJ-vs-MJ driver-energy mistakes)
trace back to ignoring these warnings.

{{canonical_spec_keys}}

## Output
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\39-spherical-tokamak-cs-free-p-b11\iter-2\model_setup.py`
