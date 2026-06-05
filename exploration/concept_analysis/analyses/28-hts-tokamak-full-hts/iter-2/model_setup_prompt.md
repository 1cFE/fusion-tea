# 1costingfe Model Update: HTS Tokamak Full HTS

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\28-hts-tokamak-full-hts\iter-2\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\28-hts-tokamak-full-hts\iter-2\model_setup.py` and apply
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

### F-1: Missing Design Point block with upstream-selected parameters
- **Target:** Section "Design Point" (top of analysis body)
- **Category:** analysis
- **Finding:** The Design Point section (line 19-23) states "(No design-point row for this concept yet — selection is upstream-pending.)" and does not copy the required frontmatter fields (name, maturity, `P_native`, grounding). The analysis proceeds with placeholder values (500 MWe, analogue-based geometry) that are explicitly documented as "NOT company-grounded," but the Design Point block itself does not state which specific machine/maturity/power level was selected upstream. Without a formal design point selection, the analysis cannot satisfy the design-point coherence criterion even though it honestly documents the data limitation.
- **Recommendation:** If no design point was formally selected upstream (i.e., the frontmatter lacks `Design-Point-Name`, `Design-Point-Maturity`, `P_native`, and `Grounding-Confidence` fields), the analysis should state this explicitly in the Design Point block: "No design point selected upstream due to absence of HH380 specifications. The model uses placeholder scale (500 MWe) per Section 6 recommendation." If a design point WAS selected upstream but is missing from the analysis, copy those four fields verbatim into a Design Point block at the top of the body. The current phrasing "upstream-pending" creates ambiguity about whether the selection exists.
- **Priority:** blocking

### F-2: Frontmatter shows Comparison-Status as freeform-deferred, but analysis provides detailed family-delta prose
- **Target:** Frontmatter field `Comparison-Status` and Section 7
- **Category:** analysis
- **Finding:** The frontmatter shows `Comparison-Status: freeform-deferred`, suggesting that the family-delta analysis was deferred. However, Section 7 provides a thorough, concrete family-delta comparison against all four fixed comparables (01, 21, 29, 33), naming specific subsystems (full-HTS vs. TF-only HTS, supply chain geography, blanket technology), stating cost directions (ambiguous for C220103 magnets due to REBCO price trajectory, advantage for China construction costs), and quantifying magnitudes (±20-40% on C220103, $150M IDC saving from 2-year vs. 7-year construction). This is high-quality family-delta prose that satisfies the concreteness criterion. The `freeform-deferred` status appears to be stale or incorrect.
- **Recommendation:** If the family-delta analysis in Section 7 is considered complete and adequate, update the frontmatter `Comparison-Status` to `freeform-complete` to reflect the actual state. If the status is intentionally `freeform-deferred` for a different reason (e.g., awaiting a structured comparison format that has not yet been implemented), clarify in the frontmatter or in a note.
- **Priority:** minor

### F-3: Model output LCOE (94 $/MWh at 1 GWe) is within plausible range but analysis does not frame LCOE expectations
- **Target:** Analysis Section 2 (Challenges in Capturing System Function) and model output interpretation
- **Category:** analysis
- **Finding:** The model output shows LCOE = 94 $/MWh (1 GWe NOAK projection), which is plausible for a compact HTS tokamak (similar order of magnitude to CFS ARC and other HTS tokamak concepts). The analysis extensively documents uncertainties and data gaps but does not explicitly state what LCOE range is expected for this concept type or how the modeled result compares to comparables. This makes it harder to assess whether 94 $/MWh is reasonable without independent knowledge of HTS tokamak LCOE benchmarks.
- **Recommendation:** In the analysis (Section 2 or in a new subsection at the end), briefly frame LCOE expectations: "Compact HTS tokamaks in the comparables set (CFS ARC, Tokamak Energy ST80) model in the range of X–Y $/MWh at 1 GWe. This concept's library-default result (94 $/MWh) falls within / above / below that corridor, consistent with [architectural differences or data limitations]." This contextualization improves the reader's ability to interpret the model's plausibility without requiring cross-concept knowledge.
- **Priority:** important


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
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\28-hts-tokamak-full-hts\iter-2\model_setup.py`
