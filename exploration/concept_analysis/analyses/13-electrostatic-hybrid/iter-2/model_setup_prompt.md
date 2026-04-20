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

### F-1: Core density-enhancement claim is simulation-only — "demonstrated" language overstates TRL in Section 3
- **Target:** Section 3 (Plasma Confinement and Ion Orbiting — TRL 3–4)
- **Category:** analysis
- **Finding:** The analysis states that "co-confinement of high-energy ions and electrons demonstrated" citing the AIP Advances paper, and rates this subsystem TRL 3–4. The OSTI source IS the AIP Advances 2024 full text. It shows that while ions and electrons are loaded simultaneously into the device (experimentally confirmed), the critical claim — that electron co-confinement provides a 50× density enhancement above the space-charge limit — is supported by PIC simulations only. The paper explicitly states proof-of-space-charge-mitigation experiments are "ongoing" at the time of writing. The paper's own language ("preliminary experiments ongoing," density enhancement "demonstrated" via simulation) places this closer to TRL 2–3. The analysis's current TRL 3–4 and "demonstrated" language conflates loading two species with validating the density-enhancement mechanism that the entire concept depends on.
- **Recommendation:** In Section 3, revise the "Demonstrated" bullet for Plasma Confinement to distinguish: (a) what is experimentally confirmed — ion and electron loading into the crossed-field geometry, ion energies >10 keV, co-presence of both species; and (b) what is simulation-only — the 50× density improvement over the space-charge limit that constitutes the concept's core physics claim. Lower the TRL for this subsystem to 2–3 and add the specific instability risks identified in the paper (diocotron instability observed in simulations; electron cyclotron drift instability flagged for higher densities). Update the "On paper only" bullet to explicitly include "space-charge-mitigated density regime (>10^10 cm^-3)."
- **Priority:** blocking

### F-2: SC magnet target field is 0.5 T in the full paper, not 0.3 T as stated throughout the analysis
- **Target:** Section 3 (Auxiliary Magnetic System), Section 4 (Superconducting Magnets), Section 5 (parameter table row: "Electron confinement field")
- **Category:** model
- **Finding:** The analysis consistently states 0.3 T as the target SC upgrade field (citing the CWFest 2023 blog and dossier). The OSTI source (AIP Advances 2024 full paper) states the planned upgrade is to 0.5 T using superconducting HTS coils. The 0.3 T figure appears to come from the CWFest blog's description of the operating point; the full paper's 0.5 T is the hardware target for the next device generation. This also changes the Section 4 supply chain discussion — 0.5 T with HTS coils is slightly more demanding than 0.3 T with NbTi, though still orders of magnitude below MFE requirements.
- **Recommendation:** Update every occurrence of "0.3 T (target)" or "0.4 T" in Sections 3, 4, and 5 to "0.5 T" and re-source to the AIP Advances paper. In Section 4, briefly note that HTS coils (not NbTi) are planned per the paper — the supply chain conclusion (modest, no REBCO bottleneck) remains directionally correct but the specific SC technology changes.
- **Priority:** important

### F-3: Neutron source rate target is 10^13 n/s in APS sources, 100× higher than the 10^11 n/s in the parameter table
- **Target:** Section 5 (parameter table row: "Target neutron rate"), Section 1 (FusionWERX neutron source characterization)
- **Category:** model
- **Finding:** The analysis parameter table cites "mid-to-high 10^11 n/s" as the neutron rate target from the CWFest 2023 blog, labeling it the "neutron source goal for FusionWERX." The 2023 APS DPP abstract (ui-2023aps-dppyo8010l) explicitly states a target of ">1×10^13 n/s" as the bright neutron source capability. The same APS abstract also reports that the 2023 conference experiments confirmed deuterium ions confined with energies >100 keV, which anchors the energy-confinement characterization. The 10^13 vs 10^11 discrepancy is two orders of magnitude and affects the credibility characterization of the FusionWERX neutron source application — 10^13 n/s would be a genuinely competitive research neutron source; 10^11 n/s is a much more modest capability.
- **Recommendation:** Update the "Target neutron rate" row in Section 5 to reflect both figures: the 10^11 n/s near-term operating point from the CWFest blog (Q≈1, 1 kW fusion) and the >10^13 n/s longer-term FusionWERX capability from the APS abstract. Cite both sources. Add a footnote to Section 1 noting that the APS 2023 abstract also experimentally confirmed >100 keV deuterium ion confinement, which partially fills gap #3 in the Data Gap table (ion energy characterization, though not density or confinement time).
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: CAS-level cost structure not mapped
- **Target:** Section 7 (Cross-Concept Notes, TEA divergences)
- **Category:** analysis
- **Finding:** The analysis correctly identifies that the Orbitron's capital cost structure "would look nothing like any prior D-T TEA" due to the absence of large magnets, breeding blanket, and plasma heating system (Goal 2). However, it stops there — it never maps these differences to CAS accounts (Goal 3). Which CAS accounts are near-zero or absent? Which are novel with no analogue? Which accounts (HV power supply, ion gun system, neutron shielding per module) become dominant in an Orbitron plant? The TEA implication of each structural differentiator is identified at a narrative level ("modular mass-manufacturing is the claimed cost mechanism") but never articulated at the account level, making the cost structure comparison with other D-T concepts unactionable.
- **Recommendation:** Add a CAS-level cost account summary to Section 7 (or a dedicated subsection). For each major CAS category (magnets/drivers, blanket/breeding, heating/CD, BOP, first wall/shielding, fuel cycle), state whether the Orbitron account is: negligible/absent, analogous to a named reference, or novel with no analogue. Flag which novel accounts have the highest cost uncertainty. Even order-of-magnitude placeholder reasoning (e.g., "HV power supply per module ≈ ~$X/kWe based on industrial 300 kV supply pricing") is more useful than a qualitative statement that the cost structure is categorically different.
- **Priority:** blocking

### F-2: Top LCOE sensitivity parameters not identified in Section 2
- **Target:** Section 2 (Challenges)
- **Category:** analysis
- **Finding:** Section 2 ranks six challenges by LCOE impact (Critical / High / Moderate), which is useful qualitative framing. But the checklist requires Section 2 to identify the 2–3 *parameters* with highest LCOE sensitivity — specific, model-ready variables, not challenge narratives (Goal 4). For the Orbitron, the back-solve modeling posture recommended in Section 7 makes this especially important: the sensitivity parameters define what the back-solve should sweep. The current section identifies Q>1 as critical but does not state Q_engineering as a sweep variable, nor does it identify capital cost per kWe or tritium consumed per MWh as the other two high-leverage parameters. The distinction between "this challenge matters" and "this parameter drives the model" is absent.
- **Recommendation:** Add a short closing paragraph to Section 2 (or a dedicated "High-Leverage Parameters" summary box) naming the 2–3 parameters with highest LCOE sensitivity for the Orbitron specifically. For a back-solve model, these are: (1) Q_engineering — the single dominant uncertainty, since LCOE is undefined below ~Q_engineering ≈ 2–3 for any thermal cycle; (2) overnight capital cost per kWe for a commercial module-stack plant — currently unbounded but is the central value proposition claim; (3) tritium consumption rate (a function of Q) — since no breeding blanket exists, this is a permanent OPEX driver unlike any other D-T concept in the portfolio. State explicitly that these are the axes the conditional viability model should sweep.
- **Priority:** important

### F-3: Back-solve viability thresholds not computed
- **Target:** Section 7 (TEA pipeline recommendation) and model_setup.py
- **Category:** model
- **Finding:** Section 7 recommends a "back-solve from commercial viability" modeling posture rather than a conventional LCOE model — a well-reasoned recommendation (Goal 4). But the back-solve is described as a methodology without any quantitative output: no minimum Q_engineering is computed, no minimum capital cost per kWe threshold is derived, and no comparison of those thresholds against the Polywell/Orbitron physics constraints is made. The recommendation says "if physics barriers are resolved, what does the cost structure look like" but never answers that question even approximately. This leaves the analysis's central modeling recommendation unanchored — it reads as a placeholder for future work rather than a D1+ modeling output.
- **Recommendation:** Implement the back-solve in model_setup.py. Parameterize Q_engineering (sweep 1–20) and capital cost per kWe (sweep $500–$10,000/kWe) and compute the LCOE surface using a thermal efficiency assumption appropriate for kWe-scale conversion (e.g., 10–20% thermoelectric, or 25–35% for a hypothetical multi-module turbine array). Identify the (Q_engineering, $/kWe) combinations that yield LCOE ≤ $100/MWh. State in Section 7 what minimum Q_engineering is required under each efficiency scenario — this is the key quantitative output that the conditional viability assessment needs to be useful. The tritium fuel cost as a function of Q should be included as a third axis or as a labeled contour on the LCOE surface.
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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/13-electrostatic-hybrid/iter-2/model_setup.py`
