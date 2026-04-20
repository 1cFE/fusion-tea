# Free-Form LCOE Model: Orbital Levitated Dipole (D-He3)

You are building a standalone LCOE model for **Orbital Levitated Dipole (D-He3)** (Zephyr Fusion).
This concept does not map cleanly to any standard 1costingfe ConfinementConcept,
so you will build a self-contained model from first principles following the
CAS cost accounting structure.

## Your Task

Write a self-contained Python script that computes LCOE from first principles.
No external dependencies beyond the standard library. The script must be directly
runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/analysis.md`
Section 5 has the quantitative values. Section 2 has the key uncertainties.

### 2. Exemplar: MagLIF Free-Form Model (pattern to follow)
`/home/reid/1cfe/tea-models/maglif/maglif_lcoe_model.py`
This is your structural template. Follow its architecture exactly:
- `@dataclass` with source-annotated docstrings on EVERY parameter
- Five `_compute_*()` methods: power → geometry → cas22 → costs → economics
- CAS-structured accounting (CAS10-90)
- `print_results()` function with full CAS breakdown
- `sensitivity_sweep()` function for single-parameter sweeps
- Scenario comparison table in `main()`

### 3. CAS Account Reference (for cost scaling laws)
`/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`
Use the scaling laws and unit costs from 1costingfe as reference values,
even though you're not using the API. Document which scaling laws you adopt.


## Assessment Feedback

The following findings were raised by the most recent assessment. Not all
findings require model changes — address findings that affect what the model
computes, sweeps, or parameterizes. Findings tagged `Category: analysis` may
still have model implications (e.g., a new parameter identified in the analysis
text that should also appear in a sensitivity sweep).

### F-1: Power beaming efficiency bottleneck is transmitter-side DC-RF conversion, not atmospheric propagation

- **Target:** Section 2 (Challenge 1) and Section 5 (parameter table, microwave power beaming row)
- **Category:** analysis
- **Finding:** The analysis cites "~40–60% efficiency from transmitter to rectenna" for microwave power beaming (Section 2, Challenge 1; Section 5 parameter table). The Shinohara SPS workshop source (NSS, ~2005) disaggregates this into sub-components and shows the bottleneck is not the atmospheric propagation leg: rectenna RF-DC conversion exceeds 80% (world record ~90%); beam collection efficiency is ~89% for a properly designed GEO SPS geometry. The critical efficiency loss is on the transmitter side — DC-RF conversion with phased array beam steering drops to below 20% due to 4–6 dB phase shifter losses per element. Historical end-to-end DC-DC demonstrations range from 6.67% (1975 Goldstone field, 1-mile range) to 54% (1975 Raytheon lab). The 40–60% figure in the analysis is ambiguous about which sub-component it represents and does not identify the transmitter-side phased array steering efficiency as the primary risk — which is where performance degrades most severely in real systems. This matters for the power beaming efficiency hypothesis (Section 2c), which sets a >30% end-to-end threshold without distinguishing where losses occur.
- **Recommendation:** Update Section 2 Challenge 1 to identify DC-RF conversion with phased array beam steering as the dominant efficiency bottleneck (potentially <20–40% for the transmitter side alone), distinct from the atmospheric/rectenna leg (~70–80% combined). Update the Section 5 parameter table to replace the single 40–60% row with disaggregated sub-components: (a) transmitter DC-RF conversion — ~70–80% without beam steering, <20–40% with active phased-array steering; (b) beam collection efficiency — ~89% for optimal geometry (1 km transmitter, 10 km rectenna, appropriate frequency); (c) RF-DC rectenna conversion — >80%, up to 90%. Add Shinohara (NSS SPS workshop) as a source in Section 8. Note that the model's 15–60% end-to-end range (Section 7 modeling recommendation) already captures this correctly; the fix is to the Section 2 framing and Section 5 labeling, not the model scenario structure.
- **Priority:** important

---

### F-2: Ground rectenna infrastructure cost anchor now available from NASA SPS feasibility study

- **Target:** Section 5 (missing parameters table, row "Capital cost (spacecraft + launch + ground infrastructure)"); Section 6 (Gap #4); Section 2 (Challenge 6)
- **Category:** analysis
- **Finding:** The analysis lists ground infrastructure cost (rectenna + grid connection) as "truly-unknown / blocking" in both Section 5 and Gap #4 in Section 6, with the note "no SSP system has been commercially deployed." The Smitherman NASA NTRS source (2012, NTRS 20140003205) provides a concrete cost anchor from a NASA/DOE feasibility study: a GW-class GEO SPS rectenna costs approximately $2B for a 10×13 km elliptical receiving field (34 km² total land area including keep-out zone), equivalent to roughly $2M/MW of delivered power for the ground segment alone. The same source also provides the NASA/DOE feasibility conclusion — "Large SPS concepts in GEO for power transfer to Earth do not appear to be practical at this time" — noting that launch cost is not the only problem and that the competing infrastructure scale makes GEO SPS uncompetitive against CSP at $2.1B/GW. Neither the cost anchor nor the feasibility conclusion appears in the analysis. The cost anchor directly addresses the "truly-unknown" gap and allows the rectenna infrastructure cost to be moved from the missing parameter table to an analogue-anchored estimate with stated caveats. The feasibility conclusion strengthens the risk framing in Section 2 Challenge 6.
- **Recommendation:** In Section 5, move rectenna infrastructure cost from the missing parameter table to the available parameters table as an SPS analogue value: "$2B for GW-class GEO SPS rectenna (10×13 km receiving field, 34 km² land area); ~$2M/MW" with explicit caveats that this is GEO (not LEO), solar (not fusion), and GW-scale (not MW-scale). Note that LEO geometry would allow a smaller rectenna footprint due to shorter transmission distance. In Section 2 Challenge 6, add the Smitherman source as evidence that detailed NASA/DOE feasibility studies concluded GEO SPS is not currently practical, and that ground infrastructure cost alone (not just launch cost) was identified as a barrier. Add Smitherman (2012, NTRS 20140003205) and Shinohara (NSS SPS workshop) to Section 8 sources.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Differentiator table lacks cost implication column
- **Target:** Section 7 (differentiator table)
- **Category:** analysis
- **Finding:** The differentiator table in Section 7 has "Category" (Novel/Borrowed/Shared) and "Nearest concept" columns, but no TEA impact column. Goal 3 requires each differentiator to have a stated cost sign (advantage / penalty / neutral) with reasoning. Most implications are recoverable by hunting through the narrative, but "Levitated HTS dipole confinement geometry" has no cost discussion anywhere in the analysis — it's unclear whether the dipole topology itself (vs. tokamak) is an advantage, penalty, or neutral for CAS costs. A model agent reading the table cannot determine cost sign for all entries without tracing across multiple sections.
- **Recommendation:** Add a "TEA Impact" column to the differentiator table. Each row should state a one-line cost implication and sign (e.g., "Advantage — eliminates CAS 21-26 blanket/vacuum vessel costs" or "Neutral — confinement geometry changes power balance but not cost structure relative to tokamak"). For the levitated HTS dipole topology row specifically, note whether the coil complexity, plasma control hardware, or MHD stability requirements change the cost structure compared to a conventional tokamak.
- **Priority:** important

### F-2: SPS not benchmarked as competitive reference for orbital power delivery
- **Target:** Section 7 (cross-concept positioning)
- **Category:** analysis
- **Finding:** The analysis positions the concept against ITER (~$650M/MW) and ISS solar (~$1B/MW), both figures sourced from Zephyr's own YC page. Space solar power (SPS) is the natural competitive reference for orbital-to-grid power delivery and has independent LCOE estimates (typically $200–500/MWh in optimistic feasibility studies). Without the SPS benchmark, Goal 1 (concept positioning) is incomplete: it is unclear whether the concept aims to undercut terrestrial fusion ($50–150/MWh), orbital solar ($200–500/MWh), or simply demonstrate net energy gain. The competitive threshold matters because it sets the tolerable range for beaming efficiency and spacecraft mass before the concept becomes uncompetitive with its own closest non-fusion analogue.
- **Recommendation:** Add a paragraph in Section 7 benchmarking against SPS economics. Note the SPS LCOE range from at least one feasibility study and clarify how orbital fusion would need to be positioned relative to it — e.g., fusion offers higher power density per kg than photovoltaics but requires He3 fuel and is at TRL 1–2 vs. TRL 4–5 for SPS components. Clarify whether the stated competitive target is terrestrial fusion parity, SPS parity, or solely net energy gain — the three thresholds imply meaningfully different beaming efficiency and launch cost requirements.
- **Priority:** important

### F-3: Direct conversion hardware cost absent from Section 5 missing parameters
- **Target:** Section 5 (missing parameters table)
- **Category:** model
- **Finding:** The proposed free-form cost framework in Section 7 names "power conversion hardware" as one of five cost categories, and Section 4 explicitly identifies direct conversion hardware as a first-of-kind development challenge with no commercial supply chain. However, the Section 5 missing parameters table has no row for direct conversion hardware unit cost (e.g., $/kW of rated conversion capacity). The entire spacecraft capital cost is bundled into one row ("Capital cost — blocking"). Direct conversion hardware cost is structurally distinct from launch cost: it scales with rated power output, not spacecraft mass, and has independent uncertainty (no commercial procurement data, no space-qualified precedent). Bundling it obscures a distinct cost driver for the model agent.
- **Recommendation:** Add a row to the Section 5 missing parameters table for "Direct conversion hardware unit cost ($/kW rated output)" with gap type "truly-unknown" and criticality "blocking." Note that the only historical reference point is the Venetian blind DEC (1970s, never manufactured at scale, never space-qualified) and that modern electrostatic decelerator proposals remain research concepts with no commercial procurement data.
- **Priority:** minor


## Power Standardization (CRITICAL)

All concept models MUST include a `scaled_headline` dict at module level for
cross-concept LCOE comparison at a normalized 1000 MWe reference.

Since freeform models derive power from physics (not as an input), use post-hoc
cost scaling:

- Keep the physics-derived power balance EXACTLY as-is. Do NOT change p_fus,
  rep_rate, n_mod, Q_sci, or any plasma physics parameters.
- The module-level `results` stays at native power.
- After `results` computation, add:
  ```python
  _ALPHA = 0.6  # economy-of-scale exponent
  _p_native = results["power"].get("p_net_plant", results["power"]["p_net"])
  _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)
  _overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native

  scaled_headline = {
      "p_net_mw": 1000.0,
      "lcoe_per_mwh": results["economics"]["lcoe_USD_per_MWh"] * _factor,
      "overnight_per_kw": _overnight * _factor,
  }
  ```
- If the concept's native power IS 1000 MWe, `scaled_headline` may be omitted.
- Document the scaling exponent (α=0.6) in the script's docstring.

## Model Architecture

Follow the MagLIF exemplar's 5-layer structure adapted for Orbital Levitated Dipole (D-He3):

### Layer 1: Power Balance (`_compute_power()`)
- Concept-specific energy flow: driver → plasma → fusion → energy recovery
- Net electric = gross electric - recirculating power
- Engineering Q and recirculating fraction

### Layer 2: Geometry (`_compute_geometry()`)
- Concept-appropriate geometry (spherical for IFE/MIF, cylindrical for linear, toroidal for MFE)
- Shell volumes for blanket, shield, structure, vessel

### Layer 3: CAS22 Reactor Plant Equipment (`_compute_cas22()`)
- Per-module sub-accounts (C220101-C220112) using 1costingfe scaling laws
- Override sub-accounts that are concept-specific (with detailed comments)
- Plant-wide accounts (C220200-C220700)

### Layer 4: Capital Costs (`_compute_costs()`)
- CAS10-60 following 1costingfe structure
- Power-scaling for buildings, turbine plant, electric plant, etc.

### Layer 5: Economics (`_compute_economics()`)
- CRF-based annualization
- O&M (CAS70), fuel/consumables (CAS80), capital charge (CAS90)
- LCOE = annual revenue requirement / annual energy production

## Parameter Documentation (CRITICAL)

Every parameter in the `@dataclass` MUST have a docstring with:
```python
driver_stored_energy_MJ: float = 130.0
"""Stored electrical energy per shot [MJ].
Source: Sandia estimates ~130 MJ stored for high-yield targets.
Ref: SAND2006-7148, analysis.md §Section 5.
HIGH UNCERTAINTY."""
```

Mark uncertainty levels:
- No tag = well-established value with source
- `MODERATE UNCERTAINTY` = reasonable estimate from analogues
- `HIGH UNCERTAINTY` = speculative or poorly constrained

## Sensitivity Analysis

Include in `main()`:
1. Baseline scenario with `print_results()`
2. Single-parameter sensitivity sweeps for the 5-7 most impactful parameters
3. Scenario comparison table (conservative, moderate, optimistic)
4. Brief "Key Binding Constraints" narrative for the top 3 LCOE drivers

## Output Interface (CRITICAL)
The concept explorer consumes module-level variables for cross-concept
comparison. You MUST expose the following at module level (outside `main()`
or any other function):

```python
# After defining the dataclass and before main():
params = YourDataclass(...)     # The @dataclass instance with all plant parameters
results = params.compute()      # The full output dict from compute()
```

The extractor reads `params` and `results` directly — no additional mapping
functions needed. Your `compute()` method MUST return a dict with these sub-dicts
using the exact key names shown:

- `"costs"`: `CAS10` through `CAS60`, `CAS20`, `total_capital`, `overnight_capital` (all in M$)
- `"economics"`: `CAS70`, `CAS71`, `CAS72`, `CAS80`, `CAS90`, `lcoe_USD_per_MWh`
- `"cas22"`: `C220101` through `C220112`, `C220200` through `C220700` (all in M$)
- `"power"`: `p_fus`, `p_th`, `p_et`, `p_net`, `Q_eng`, `Q_sci`, `recirc_fraction` (per-module, in MW)

For multi-module concepts, also include `p_net_plant`, `p_et_plant`, `p_th_plant`
in the `"power"` dict.

## Anti-Hallucination
- Parameter values MUST come from the analysis or documented analogues
- Scaling laws MUST come from 1costingfe or published fusion engineering references
- Mark ANY assumed value that is not in the analysis with `# ASSUMED: ...`
- If a subsystem has no cost data, use 1costingfe defaults with `# DEFAULT: ...`

## Usage Comment
Include this at the top of the generated script's docstring:
```
Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
```

## Output
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/iter-3/model_setup.py`
