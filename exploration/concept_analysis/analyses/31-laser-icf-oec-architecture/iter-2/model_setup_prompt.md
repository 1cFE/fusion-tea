# 1costingfe Model Update: Laser ICF OEC Architecture (BLF)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\31-laser-icf-oec-architecture\iter-2\model_setup.py`.

**Your task**: Read the existing model at `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\31-laser-icf-oec-architecture\iter-2\model_setup.py` and apply
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

### F-1: Zero overrides for Low archetype-fit when comparable-derived bracketing data exists
- **Target:** Section 5b (Override Candidates) and model_setup.py overrides list
- **Category:** analysis
- **Finding:** The analysis concludes zero enabled overrides and defends this as a data-availability problem, but the family-delta prose in Section 7 itself cites published $/J figures for comparable laser drivers — Inertia DPSSL at $700–1000/J (concept 26) and Xcimer KrF at $60–80/J (concept 17a). The BLF paper provides the total laser energy (5 MJ) and beam count (500), which combined with these comparable brackets could produce a derived override for C220104 (primary pulsed driver) — the account the analysis identifies as "most likely to warrant an override." Similarly, the analysis cites LLNL IFE target costing studies and Goodin et al. (2004) in the data-gap table as source recommendations for C220108 (target factory), suggesting published IFE target cost frameworks exist. A Low archetype-fit concept with 0 overrides against an expected 6–12 band means the model runs entirely on library defaults designed for a different IFE driver architecture — precisely the situation overrides are meant to address.
- **Recommendation:** Add at least a derived override for C220104 using the comparable $/J bracket from Section 7 (e.g., Xcimer $60–80/J as low bound, Inertia $700–1000/J as high bound, applied to 5 MJ), with provenance `derived` and explicit arithmetic showing the range. Consider whether target factory (C220108) can similarly be bracketed from IFE target costing literature cited in the data-gap table. The goal is not to guess BLF's actual cost but to replace a generic library default with the narrower range that the dossier's own cross-concept data supports.
- **Priority:** blocking

### F-2: Unmodeled DEC channel creates a structural power-conversion error acknowledged but not surfaced as a model limitation
- **Target:** model_setup.py spec comments and analysis Section 2.4
- **Category:** model
- **Finding:** The BLF design routes 30% of fusion power through direct energy conversion at η_DEC = 0.44, but the LASER_IFE archetype uses pulsed_conversion=thermal mode, which models 100% thermal conversion. The model_setup.py comments acknowledge this ("BLF's 30% DEC channel is a modeling gap — no hybrid thermal+DEC mode exists") but the model output shows no scenario or sensitivity that quantifies the impact. Since the thermal and DEC efficiencies happen to be equal (both 0.44), the net η_e is the same either way for this specific design point, making the error numerically small at native scale. However, this coincidental equality masks a real structural mismatch: without DEC, the concept's economics at different operating points (e.g., if η_DEC ≠ η_th) would diverge. The model should at minimum include a sensitivity scenario showing the DEC-off case (η_e drops from 0.44 to ~0.31, recirculating fraction rises sharply) to bound the economic impact of DEC availability risk, which the analysis calls out as TRL ~2.
- **Recommendation:** Add a sensitivity scenario in model_setup.py that runs the model with q_eng recalculated for the no-DEC case (where all fusion energy goes through thermal conversion at η_th = 0.44, but the 30% charged-particle fraction that was destined for DEC now has lower capture efficiency or is lost). Alternatively, recalculate q_eng for η_e ≈ 0.31 (thermal-only on the 30% DEC channel) and show the LCOE delta. Document this as a named scenario (e.g., "DEC unavailable") rather than leaving it as a comment-only acknowledgment.
- **Priority:** important

### F-3: Generic and native columns are identical, obscuring the effect of spec departures from YAML defaults
- **Target:** model_setup.py and model_output.txt
- **Category:** model
- **Finding:** The model output shows generic = native for every CAS account ($15,010.8M total for both). The three-forward contract defines "generic" as overrides-OFF at native scale and "native" as overrides-ON at native scale. With zero overrides, the two are trivially identical. This is mechanically correct but means the model output provides no information about how the spec-level departures (plasma_t = 9.0 vs. default 4.0, q_eng = 4.7 vs. default 4.0) affect cost relative to the pure archetype default. A more informative generic forward would use YAML defaults for spec as well (plasma_t = 4.0, q_eng = 4.0) so the reader can see the cost impact of BLF's larger chamber and higher engineering gain, separate from any override effects. This is not a contract violation — the helper function defines generic as spec-on/overrides-off — but the result is that the two non-1GWe columns carry no differential information.
- **Recommendation:** This is an informational gap rather than an error. No code change is required if the three-forward contract intentionally includes spec in the generic forward. However, if the analysis adds overrides per F-1, the generic/native divergence will appear naturally and this finding resolves itself.
- **Priority:** minor


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\31-laser-icf-oec-architecture\analysis.md`
- **Example (pattern):** `\home\reid\1cfe\1costingfe\examples\dt_tokamak.py`
- **README:** `\home\reid\1cfe\1costingfe\README.md`
- **Costing Constants:** `\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.LASER_IFE`, `Fuel.DT`

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
Write changes to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\31-laser-icf-oec-architecture\iter-2\model_setup.py`
