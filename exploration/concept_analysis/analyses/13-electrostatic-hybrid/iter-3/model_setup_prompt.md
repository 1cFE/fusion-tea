# Free-Form LCOE Model: Electrostatic Hybrid (D-T)

You are building a standalone LCOE model for **Electrostatic Hybrid (D-T)** (Avalanche Energy).
This concept does not map cleanly to any standard 1costingfe ConfinementConcept,
so you will build a self-contained model from first principles following the
CAS cost accounting structure.

## Your Task

Write a self-contained Python script that computes LCOE from first principles.
No external dependencies beyond the standard library. The script must be directly
runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/13-electrostatic-hybrid/analysis.md`
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

### F-1: Tritium Breeding "No Approach Disclosed" Claim Overstated
- **Target:** Section 2 (Challenge #4), Section 3 (Tritium Fuel Cycle TRL 1–2), Section 6 (Gap #9)
- **Category:** analysis
- **Finding:** Both new FusionWERX sources (NEI Magazine and PRNewswire, April 2025) report a Memorandum of Understanding between Avalanche Energy and Fusion Fuel Cycles (FFC) that explicitly covers tritium breeding blankets and D-T fuel cycle systems. The analysis currently states "no breeding approach has been disclosed" (Section 2) and lists Gap #9 as "none disclosed." An MoU naming breeding blankets as a collaboration target is a disclosed approach direction — not a design, but meaningfully beyond "no approach at all."
- **Recommendation:** Update Section 2 Challenge #4 and Section 3 Tritium subsection to note the FFC MoU and qualify the "no breeding approach disclosed" language: Avalanche has disclosed a collaboration intent with an external D-T fuel cycle partner, but no blanket design, timeline, or technical specification has been published. Gap #9 in Section 6 should be updated similarly. The fundamental gap severity (no design, no timeline) is unchanged — only the framing of disclosure needs correction.
- **Priority:** minor

### F-2: FusionWERX Capability Understated — Hot Cells and Tritium Recycling Not Captured
- **Target:** Section 3 (Tritium Fuel Cycle TRL 1–2), Section 2 (Challenge #6 O&M)
- **Category:** analysis
- **Finding:** The new sources describe FusionWERX as including (a) hot cells for activated material handling and (b) integrated tritium management with extraction, purification, and recycling — capabilities beyond the analysis's characterization of "tritium handling capabilities" and "advanced tritium handling." The hot cells directly address the neutron activation concern raised in Challenge #6 (O&M), indicating prototype-scale activated component management infrastructure is being built. The tritium recycling system implies a partial closed fuel cycle for the neutron source application (recovered tritium can be reused, reducing consumable costs at that scale).
- **Recommendation:** Update Section 3 Tritium Fuel Cycle subsection to note recycling/extraction capability specifically — this upgrades the demonstrated capability description from "storage and use" to "extraction, purification, and recycling." Update Section 2 Challenge #6 to acknowledge hot cells as existing activated material management infrastructure at the facility level. The commercial-scale O&M uncertainty is unchanged; this is a facility-level capability, not a module design. The TRL rating for the tritium subsystem does not change.
- **Priority:** minor

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Q break-even threshold is wrong in analysis text; baseline model scenario produces negative net power
- **Target:** Section 2 (High-leverage parameters) and model_setup.py (OrbitronPlantParams defaults, scenario comparison table)
- **Category:** model
- **Finding:** Section 2 states "LCOE is undefined below Q_engineering ≈ 2–3 for any thermal cycle," but the correct net-power break-even is Q = 1/η. At the thermoelectric baseline (η=12%), break-even requires Q ≈ 8.3, not 2–3. At turbine-array efficiency (η=30%), break-even is Q ≈ 3.3. The "2–3" floor is only valid at η > 33–50%, which is an optimistic assumption. Consequently, the default baseline scenario (Q=5, η=12%) produces negative net power per module (p_et ≈ 0.6 kWe vs p_recirc ≈ 1.12 kWe) and the model prints "LCOE = UNDEFINED" — the opposite of a useful reference case. The "Q=5, thermoelectric" row in the scenario comparison table has the same problem. This error propagates directly into the analysis's stated primary conclusion: the minimum Q threshold that determines Orbitron viability is substantially higher than the analysis claims.
- **Recommendation:** Correct the Q break-even in Section 2 to read Q ≈ 8–9 (thermoelectric, η=12%) and Q ≈ 3–4 (turbine array, η=30%). Set the default baseline in model_setup.py to a physically feasible case — either Q=10 at η=12%, or Q=5 at η=30%. Update the scenario comparison table so all rows represent achievable (positive net power) configurations. The key quantitative conclusion in Section 7 — the minimum Q required for commercial viability — should then be stated explicitly using the corrected values the model computes.
- **Priority:** blocking

### F-2: Back-solve LCOE surface has mislabeled capital-cost axis
- **Target:** model_setup.py `back_solve_lcoe_surface()` function
- **Category:** model
- **Finding:** The back-solve table labels its columns as "LCOE $/MWh @$2k/kW" and "LCOE $/MWh @$5k/kW," implying these are specific capital $/kWe scenarios. The implementation varies `hv_power_supply_cost_per_kW_USD` (200 vs 800 $/kW_input) without computing or printing the actual resulting specific capital $/kWe. Because HV supply cost is only one of many capital accounts, the actual $/kWe at each sweep point is unknown and likely differs from the labeled targets. The primary model output — the (Q, $/kWe) viability map described in Section 7 — is uninterpretable without verified axis values.
- **Recommendation:** Modify `back_solve_lcoe_surface()` to print the computed specific capital $/kWe for each scenario column, so readers can verify the axis labels. Alternatively, restructure the sweep to directly target $/kWe by scaling all per-module cost accounts together. The goal is a table where both axes (Q and $/kWe) are quantities actually computed by the model, not assumed from one input parameter.
- **Priority:** important

### F-3: Key hypotheses stated as methodology steps, not testable propositions
- **Target:** Section 7 (TEA pipeline recommendation, modeling steps 1–5)
- **Category:** analysis
- **Finding:** Section 7 outlines five modeling steps for the back-solve but frames each as an action item rather than a falsifiable proposition. Goal 4 requires hypotheses the model can confirm or refute. The analysis identifies the right structure but stops short of committing to specific claims, leaving the back-solve output as an open question rather than a conditional conclusion. For example, the critical question — whether Coulomb collision physics makes the required Q unachievable and therefore renders LCOE ≤ $100/MWh structurally impossible — is framed as a comparison to "make" rather than a claim to test.
- **Recommendation:** After correcting the Q break-even (F-1), rewrite the modeling recommendation in Section 7 as 2–3 explicit conditional propositions, e.g.: "H1: Under thermoelectric conversion (η=12%), LCOE ≤ $100/MWh requires Q_engineering > [X computed by model] — a value not achievable if Coulomb collisions limit Q below that threshold." "H2: Even under turbine-array conversion (η=30%), viability requires Q_engineering > [Y] and specific capital < [Z $/kWe] simultaneously — a combination that requires demonstrating space-charge-mitigated density and a plant architecture that does not yet exist." The model output then confirms or refutes each proposition with specific numbers.
- **Priority:** important


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

Follow the MagLIF exemplar's 5-layer structure adapted for Electrostatic Hybrid (D-T):

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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/13-electrostatic-hybrid/iter-3/model_setup.py`
