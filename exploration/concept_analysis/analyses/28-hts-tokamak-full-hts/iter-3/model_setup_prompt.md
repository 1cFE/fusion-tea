# 1costingfe Model Update: HTS Tokamak Full HTS

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\28-hts-tokamak-full-hts\iter-3\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\28-hts-tokamak-full-hts\iter-3\model_setup.py` and apply
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

### F-1: Design Point block contradicts the selection requirement
- **Target:** Section "Design Point" (top of analysis.md)
- **Category:** analysis
- **Finding:** The Design Point block states "No design point selected upstream due to absence of HH380 specifications" and frames the entire analysis around placeholder analogue assumptions. However, the assessment contract requires that "the named design point (plant name, maturity, native net-electric power P_native, and grounding confidence) are all determined by the upstream tables and arrive through the analysis frontmatter." The block should either (a) present a formally selected design point with explicit analogue grounding-confidence labeling (e.g., "Design Point: HH380 [Analogue], Maturity: Planned (post-2030), P_native: 500 MWe [analogue-derived], Grounding: Low"), or (b) if truly no design point exists upstream, state this as a process blocker rather than proceeding with ad-hoc placeholder values.
- **Recommendation:** Rewrite the Design Point block to present a formally selected design point. Use "HH380" as the plant name (even though specifications are unknown), state maturity as "Planned (post-2030)", declare P_native = 500 MWe as an analogue-derived value (not company-disclosed), and set grounding confidence to "Low" with the explicit rationale that HH380 engineering specifications do not exist in public sources. The placeholder framing should be moved to a clarification note after the formal design-point declaration, not replace it. This preserves the contract requirement that every concept has a named design point while honestly reflecting the data limitation.
- **Priority:** important

### F-2: Override count justification needs elevation to Design Point context
- **Target:** Section 5b (Override Candidates)
- **Category:** analysis
- **Finding:** Section 5b correctly concludes zero enabled overrides and provides thorough per-account justification ("absence of company data for HH380"). However, the assessment rubric checks override count against archetype-fit grade (High → expect 0-4 enabled overrides). The zero-override count is technically within the band, but the justification is scattered throughout Section 5b. A reader unfamiliar with the concept's extreme data limitations might interpret zero overrides as "perfect library alignment" rather than "fundamental data absence." The Design Point block revision (F-1) will address this by declaring Low grounding confidence upfront, but Section 5b should also include a summary statement connecting the override count to the grounding limitation.
- **Recommendation:** Add a summary paragraph at the end of Section 5b (after the YAML block showing `overrides: []`) that explicitly states: "The zero-override count reflects fundamental data absence, not library alignment. This concept is graded High archetype-fit (expected 0-4 enabled overrides), and the count falls within that band. However, the analysis identifies C220103 (magnets) as the top override candidate when HH380 data becomes available, due to the full-HTS architectural difference from library defaults."
- **Priority:** minor

### F-3: Model output LCOE plausibility requires cross-check against stated corridor
- **Target:** Model validation (model_output.txt interpretation)
- **Category:** model
- **Finding:** The model output shows 1 GWe NOAK LCOE = 94.0 $/MWh and native (500 MWe FOAK) LCOE = 110.9 $/MWh. The analysis Section 2 states the expected corridor is "50-130 $/MWh" with the wide range reflecting "REBCO price trajectory uncertainty, deployment geography, and unresolved blanket design." The modeled LCOE (94 $/MWh) falls within this corridor and is close to the midpoint, which is plausible. However, the model output caveat text states "this concept's true 1 GWe LCOE could be ±50% from this library-default story," which implies a range of 47-141 $/MWh—slightly wider than the 50-130 $/MWh analysis corridor. This is a minor inconsistency but worth aligning for coherence. Additionally, the dominant cost driver in the model is CAS22 (Reactor Equipment) at $4065M for 1 GWe, which is consistent with the analysis emphasis on magnets (C220103: $411.9M) and heating (C220104: $600.5M) as major cost accounts. The model is internally coherent with the analysis narrative.
- **Recommendation:** In the model_setup.py caveat text (lines 185-187), revise the ±50% uncertainty statement to align with the analysis corridor. Replace "could be ±50% from this library-default story" with "could range from 50-130 $/MWh (the corridor stated in analysis.md Section 2), centered on this 94 $/MWh library-default estimate." This preserves the uncertainty message while improving cross-artifact coherence.
- **Priority:** minor


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\28-hts-tokamak-full-hts\analysis.md`
- **Example (pattern):** `\home\reid\1cfe\1costingfe\examples\dt_tokamak.py`
- **README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing Constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`
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

### Canonical `spec` field glossary (for any new/changed spec key)

If your edit touches the `spec` dict (adding/renaming/replacing a field),
the new key MUST come from the glossary below. Read the "Common confusions"
block before editing — most prior errors (concept 05/09 fusion-vs-heating
mix-up, dipole `plasma_volume` regression, kJ-vs-MJ driver-energy mistakes)
trace back to ignoring these warnings.

{{canonical_spec_keys}}

## Output
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\28-hts-tokamak-full-hts\iter-3\model_setup.py`
