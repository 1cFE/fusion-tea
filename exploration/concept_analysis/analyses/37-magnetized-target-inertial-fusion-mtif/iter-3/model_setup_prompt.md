# 1costingfe Model Update: MTIF (Magneto-Inertial Fusion Technologies)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\37-magnetized-target-inertial-fusion-mtif\iter-3\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\37-magnetized-target-inertial-fusion-mtif\iter-3\model_setup.py` and apply
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

### F-1: Provenance mismatch between analysis and model for C220107
- **Target:** Section 5b (Override Candidates) — C220107 entry provenance field
- **Category:** analysis
- **Finding:** The analysis Section 5b YAML shows C220107 with `provenance: derived`, but the coherence flags report "provenance mismatch — C220107 (model_setup=derived, analysis.md=direct)". Reading the YAML at lines 444–451, the `provenance` field correctly states `derived`. However, the coherence checker detected a mismatch, suggesting either a parsing error or the analysis text elsewhere (not in the YAML registry) refers to C220107 as direct-provenance. The rationale at lines 449–451 confirms this is analyst-derived ("derived from railgun efficiency analogies and capacitor industry pricing, not from NearStar-published data"), not company-published.
- **Recommendation:** Verify that no prose in Section 5b or elsewhere in the analysis text refers to C220107 as "direct" or "company-published". If the YAML is already correct (as it appears to be), this may be a false positive from the coherence checker; if so, note this discrepancy in the assessment but do not change the analysis. If there is conflicting prose, align it to `derived` throughout.
- **Priority:** minor

### F-2: Override count (0 enabled) below Med archetype-fit band (expected 3–8)
- **Target:** Section 5b (Override Candidates) — override registry and justification narrative
- **Category:** analysis
- **Finding:** The concept is graded Med archetype-fit (expected 3–8 enabled overrides per the rubric), but the analysis enables zero. The count-vs-grade check in the coherence flags confirms: "Med archetype fit with 0 enabled overrides (expected 3–8)". The analysis acknowledges this at lines 461–462: "Zero enabled overrides. Expected band for Med archetype-fit is 3–8. The discrepancy reflects the extreme opacity of NearStar's public materials." While transparency about data gaps is appropriate, Med archetype-fit implies the library's MAG_TARGET defaults architecturally match NearStar's stated approach, yet the analysis identifies two plausible override candidates (C220107 capacitor bank at $20M, CAS21 retrofit savings 30%) and disables both. The C220107 rationale (lines 449–451) states actual cost "could be factor of 2–3× different" — but a factor-of-2 uncertainty is not unusual for early-stage concepts and does not necessarily disqualify an override if the midpoint estimate is better-grounded than the library default. The analysis does not explicitly compare the $20M derived figure to what the library default assumes for C220107 (pulsed-power capacitor bank).
- **Recommendation:** Either: (a) enable C220107 at the $20M derived midpoint (acknowledging ±factor-of-2 uncertainty in sensitivity analysis), bringing the count to 1 (closer to the 3–8 band), and justify why this derived figure is more credible than the library's MAG_TARGET default for a 1 Hz, 5–10 MJ railgun capacitor bank; OR (b) retain zero enabled overrides but strengthen the narrative justification in Section 5b to explicitly state why the library's MAG_TARGET defaults (calibrated to what reference?) are trusted over the derived railgun analogies, despite Med (not High) archetype-fit. Currently, the analysis disables overrides due to "insufficient company data" but does not argue that the library default is better-grounded — it may be equally or less grounded.
- **Priority:** important

### F-3: Model 1 GWe LCOE (56.6 $/MWh) implausibly optimistic given data opacity and D-D penalty
- **Target:** model_setup.py — interpretation of output plausibility
- **Category:** model
- **Finding:** The model output shows 1 GWe NOAK LCOE = 56.6 $/MWh, which is competitive with best-case tokamak projections (Commonwealth ARC ~60 $/MWh) and lower than most surveyed fusion concepts. This is implausible for a concept with: (1) no published target gain or fusion yield, (2) D-D fuel carrying a 6× reactivity penalty vs. D-T, (3) undemonstrated railgun component lifetime at 1 Hz, and (4) paper-concept maturity with no experimental validation. The analysis (Section 2) lists target gain and driver cost as "BLOCKING" gaps, yet the model produces a competitive LCOE. This suggests the MAG_TARGET library defaults are encoding optimistic assumptions (low driver cost, high gain, low O&M) that are not validated for NearStar's hypervelocity-projectile + D-D architecture. The native LCOE (155.0 $/MWh at 50 MWe) is 2.7× higher than the 1 GWe projection, indicating strong economies of scale, but the analysis does not explain why a 50 MWe pulsed-MIF plant should scale favorably to 1 GWe when railgun component replacement (Section 4, lines 283–286: 10–100 rail sets/year at $50k–500k/year) may scale unfavorably with plant size. The CAS breakdown shows CAS22 (reactor equipment) scaling from $155M at 50 MWe to $2,702M at 1 GWe (17× increase for 20× power scale), but CAS70 (O&M + component replacement) scales only from $13.2M/yr to $25.0M/yr (1.9×), which seems inconsistent with the rail-lifetime concerns articulated in the analysis.
- **Recommendation:** Add a model-plausibility caveat in the analysis Section 5 or Section 8 stating that the 56.6 $/MWh 1 GWe LCOE is a library-default artifact and should not be interpreted as a credible estimate for NearStar's concept until target gain, driver cost, and component lifetime are disclosed. The model output is useful for identifying what *would* need to be true for LCOE competitiveness (e.g., target gain >X, railgun CAPEX <$Y, rail lifetime >Z shots), but it is not a validated projection. Alternatively, if sensitivity analysis on target gain, driver efficiency, or component lifetime is feasible, run it to bound the LCOE range under pessimistic vs. optimistic assumptions and report that range instead of the single 56.6 $/MWh figure.
- **Priority:** important


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
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\37-magnetized-target-inertial-fusion-mtif\iter-3\model_setup.py`
