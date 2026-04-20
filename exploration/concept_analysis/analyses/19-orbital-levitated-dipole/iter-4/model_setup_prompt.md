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

### F-1: He3 self-breeding feasibility has no quantitative grounding
- **Target:** Section 2 (Key Technical Bets, hypothesis b) and Section 5 (Missing Parameters)
- **Category:** analysis
- **Finding:** The analysis correctly identifies He3 self-breeding as the single most critical binary risk and the largest LCOE sensitivity parameter — if self-breeding fails, market-purchase He3 at ~$30M/kg renders the concept non-viable. It notes (by analogy to Helion's FRC) that D-D side reactions produce tritium that decays to He3 over 12.3 years. But the analysis provides no physics analysis of whether this breeding rate can plausibly match the consumption rate in a dipole geometry. The feasibility depends on the ratio of D-D to D-He3 reaction rates at 50–100 keV center-of-mass — a ratio determinable from published cross-section data. The dipole geometry may also differ substantially from the FRC: different ion residence times and plasma densities change the effective D-D/D-He3 burn ratio. Without even an order-of-magnitude bound, the hypothesis cannot be evaluated at all — the concept might be categorically excluded from self-breeding by simple cross-section arithmetic, or the breeding rate might plausibly match consumption. The analysis does not distinguish these cases, which is the core question the hypothesis must answer.
- **Recommendation:** Add a quantitative breeding feasibility calculation to Section 2 hypothesis (b). Use published D-D and D-He3 fusion cross-section data at 50–100 keV to estimate the D-D/D-He3 reaction rate ratio under nominal operating conditions. Derive the implied He3 production rate (via T decay at t₁/₂ = 12.3 yr) and compare to the He3 consumption rate at the target fusion power. Flag whether the 12.3-year decay timescale is compatible with commercial fuel inventory logistics. Note any geometry-specific differences between FRC and dipole that would change the burn ratio. The conclusion need not be precise — the goal is to establish whether self-breeding is physically plausible in principle, or categorically infeasible, before asserting it as the key binary scenario branch.
- **Priority:** blocking

### F-2: No rough LCOE calculation for the recommended scenarios
- **Target:** Section 7 (Modeling Approach Recommendation)
- **Category:** model
- **Finding:** The analysis defines two specific scenarios — pessimistic (market-purchase He3 at ~$30M/kg, Falcon 9 at $2,700/kg, beaming at 20%) and optimistic (self-bred He3 near-zero cost, Starship at $200/kg, beaming at 50%) — and asserts that competitive thresholds are $50–150/MWh (terrestrial fusion parity) and $200–500/MWh (SPS parity). But no LCOE estimate is given for either scenario, leaving the competitive threshold claims ungrounded. A rough calculation is feasible from the parameters already in the table: at 1 MWe delivered, Q=10, and 20% end-to-end beaming efficiency, approximately 7 MW fusion power is needed. D-He3 He3 consumption at 7 MW fusion is roughly 0.38 kg/yr. At $30M/kg, He3 fuel cost alone is ~$11M/yr — against 1 MWe × 8,760 hr = 8,760 MWh/yr. Fuel cost LCOE contribution alone: ~$1,260/MWh, roughly 8–25× terrestrial parity before any capital or O&M. The optimistic scenario (self-bred He3, Starship launch) brings capital + O&M to perhaps $500/MWh, approaching SPS parity. Without showing this arithmetic, the claim that "below ~20% efficiency the concept cannot compete" is asserted but not demonstrated, and the modeler building the free-form model has no sanity check on the cost skeleton.
- **Recommendation:** Add a rough LCOE skeleton calculation for both scenarios to Section 7. Assume an explicit notional output (e.g., 1 MWe delivered), spacecraft mass range (5,000–15,000 kg), and use the He3 consumption derivation, launch cost from Section 4, and the SPS-analogue rectenna cost ($2M/MW) already in Section 5. Amortize capital over 10 years and add an O&M fraction. The goal is internal consistency — the calculation should confirm that He3 fuel cost and beaming efficiency dominate in the pessimistic case, and that even the optimistic scenario lands near SPS parity rather than terrestrial fusion parity, setting realistic expectations for the free-form model.
- **Priority:** important

### F-3: Proton deceleration efficiency is missing from the end-to-end efficiency chain
- **Target:** Section 2 (Challenge 1, hypothesis c) and Section 5 (Available Parameters, power beaming rows)
- **Category:** analysis
- **Finding:** Hypothesis (c) explicitly defines the efficiency chain as "fusion power → proton deceleration → DC → microwave transmitter → atmosphere → rectenna → AC grid" and sets a >30% threshold. But the Section 2 calculation — "product of <20% × 89% × 80% = ~14% or less" — covers only the three beaming sub-stages (transmitter → atmosphere → rectenna) and implicitly assumes 100% efficiency for the proton deceleration step. The 14.7 MeV proton from D-He3 presents a qualitatively different deceleration challenge than the low-energy ions for which the Venetian blind DEC (50–65%) was characterized: 14.7 MeV protons have a range of ~1.4 mm in water, requiring very large electrode gaps or dense deceleration media not present in the original DEC design. Even a pessimistic direct conversion efficiency of 50% (applying the Venetian blind figure) reduces the total end-to-end efficiency to <7%, not <14%. This makes hypothesis (c)'s 30% threshold roughly twice as hard to achieve as the calculation implies, and changes the failure mode framing.
- **Recommendation:** Update the Section 2 end-to-end efficiency calculation to include the proton deceleration step explicitly. Apply the Venetian blind DEC efficiency (50–65%, labeled as "non-fusion ion analogue, likely optimistic for 14.7 MeV protons") as the first factor: (50–65%) × (<20%) × (89%) × (>80%) ≈ 7–9% realistic end-to-end. Note that the 14.7 MeV proton deceleration physics differs from the DEC design basis and that actual efficiency at this energy is unknown (cite as "truly-unknown"). Update the hypothesis (c) failure mode threshold accordingly — the current ">30%" is based on beaming-only efficiency, but the correct threshold when the full chain is included would be lower (since the proton deceleration step is not under the operator's control to improve independently of plasma physics).
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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/iter-4/model_setup.py`
