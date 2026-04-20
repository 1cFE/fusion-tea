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

### F-1: He3 export controls and dual-use regulatory barriers absent from challenge and risk coverage

- **Target:** Section 2 (He3 supply challenge) and Section 6 (Gap 14)
- **Category:** analysis
- **Finding:** The analysis thoroughly covers He3 as an economic and market-availability problem but treats the supply constraint as purely a physical scarcity issue. CRS R41419 establishes that He3 and tritium are export-controlled dual-use materials subject to inter-agency oversight (DOE, DHS, DOD, NSC) and nonproliferation scrutiny. Procurement for a commercial program requires government-to-company supply agreements subject to political and policy constraints — including rationing decisions by the Interagency Policy Committee (which in 2009–2011 actively cut allocations to science programs to prioritize security uses). This is a distinct risk dimension from the physical scarcity already described. The current Section 6 Gap 14 covers only nuclear operations in LEO (IAEA/COPUOS); He3/tritium procurement controls are a separate regulatory track not mentioned anywhere in the analysis.
- **Recommendation:** Add a sentence to the Section 2 He3 supply discussion noting that commercial He3 procurement also faces export control regulatory complexity: He3 and tritium are dual-use controlled materials; U.S. government allocation has historically been rationed and prioritized for security over science; international procurement faces analogous restrictions. Update Gap 14 in Section 6 to distinguish two regulatory tracks — (1) nuclear safety in LEO (already covered) and (2) He3/tritium export controls and dual-use procurement regulations (add CRS R41419 as the source reference). This adds a policy-risk dimension to the already-blocking He3 supply challenge.
- **Priority:** important

---

### F-2: He3 fuel cost scenario range is too narrow — production cost alternatives are absent from the parameter table

- **Target:** Section 5 (LCOE-Relevant Parameters) and Section 2 (He3 supply challenge)
- **Category:** model
- **Finding:** The analysis parametrizes He3 cost at a single market price point (~$5,000–6,000/std L) without a scenario range. CRS R41419 provides a production cost range from alternative supply pathways: ~$300/liter incremental extraction from existing natural gas processing infrastructure (lowest credible long-run supply cost if scaled), to ~$12,000/liter full-cost natural gas extraction, to $11,000–18,000/liter for unsubsidized new tritium production. The lower bound ($300/liter) differs from the current market price by roughly 15–20×. For LCOE scenario modeling — even as a sensitivity parameter — this range matters: if long-run commercial He3 production infrastructure were established, it would substantially change the D-He3 fuel cost outlook relative to current market price. The current Section 5 table presents only one number and does not acknowledge that production cost and market allocation price are different quantities. Note: CRS data is from 2011 and current costs will differ; the order-of-magnitude spread remains relevant for scenario bounding.
- **Recommendation:** Add a second He3 cost row in Section 5 distinguishing market price (current, ~$5,000–6,000/std L) from estimated long-run production cost range ($300–18,000/liter from CRS R41419, 2011 basis). Add a note in Section 2 that the fuel cost sensitivity depends on whether commercial He3 production infrastructure is ever developed: the $300/liter lower bound (incremental natural gas extraction) versus $5,000+ market allocation price defines a scenario branch in the LCOE model, not just a single uncertain parameter. This gives the model a defensible range for He3 fuel cost scenarios rather than a single point.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: No modeling approach recommendation and no top-sensitivity parameter identification
- **Target:** Section 2 (Challenges) and modeling recommendations (Goal 4)
- **Category:** model
- **Finding:** The analysis correctly observes that the standard CAS framework does not apply to an orbital concept and that "a new cost framework is needed" (Section 7), but never translates this into a modeling recommendation. Section 2 ranks challenges by impact but does not identify the 2–3 parameters with highest LCOE sensitivity for a sensitivity sweep. There is no statement of whether 1costingfe or free-form modeling is appropriate, nor which parameters (e.g., power beaming end-to-end efficiency, He3 supply cost, launch cost per installed MW) would drive the greatest LCOE variation. Without this, the analysis provides excellent diagnosis but no actionable modeling path.
- **Recommendation:** Add a modeling recommendation paragraph to Section 2 or Section 7 that: (1) states free-form modeling is required because the orbital concept has no CAS analogue in the 1costingfe framework; (2) identifies the 2–3 parameters with highest LCOE leverage — candidates are power beaming efficiency (40–60% vs. plausible lows of 10–20% in early-deployment scenarios), He3 supply cost (market purchase ~$30M/kg vs. self-bred near-zero), and launch cost per MW installed (which folds spacecraft mass and power output together); and (3) states the recommended scenario structure (e.g., a pessimistic scenario assuming market He3 and today's launch pricing vs. an optimistic scenario assuming self-breeding and Starship-era launch costs). These do not require new data — they follow directly from the gap analysis already in the text.
- **Priority:** blocking

### F-2: Key differentiators from conventional tokamak not explicitly listed
- **Target:** Section 7 (Cross-Concept Notes) — Goals 1–2
- **Category:** analysis
- **Finding:** Differentiators from a conventional tokamak are distributed across Sections 2, 3, 4, and 7 but never consolidated into an explicit list. The analysis notes that the CAS cost structure "has almost no overlap," that D-He3 replaces D-T, that there is no blanket or thermal cycle, and that the platform is orbital — but a reader cannot quickly identify the complete set of differentiators or which are novel vs. borrowed vs. shared with other non-tokamak concepts. The 35-polomac-magnetic-confinement concept (also a dipole, D-D, internal coil) appears in the concept landscape but is not referenced; its absence means the analysis does not distinguish what is specific to *orbital* dipoles vs. levitated dipoles in general.
- **Recommendation:** Add a structured differentiator table or bulleted list in Section 7 with three columns: (1) Differentiator, (2) Category [Novel / Borrowed / Shared], (3) Nearest concept sharing this feature. At minimum, cover: orbital deployment (Novel), D-He3 aneutronic fuel (Shared with 08-frc-w-direct-conversion), no vacuum vessel or blanket (Novel), direct conversion + power beaming instead of thermal cycle (Novel), levitated HTS dipole geometry (Shared with 12-levitated-dipole and 35-polomac), no tritium breeding (Shared with all aneutronic concepts), no 14 MeV neutron shielding requirement (Shared with D-He3 and p-B11 concepts). Also add a one-sentence positioning note distinguishing Zephyr from 35-polomac on the orbital vs. terrestrial and D-He3 vs. D-D axes.
- **Priority:** important

### F-3: Technical bets framed as gaps, not as testable hypotheses with explicit failure modes
- **Target:** Section 6 (Data Gap Inventory) and Section 3 (Maturity) — Goal 5
- **Category:** analysis
- **Finding:** The analysis identifies key technical risks clearly but frames them exclusively as data gaps and unknowns. The checklist requires that key technical bets be stated as testable propositions: what is the hypothesis, and what does concept failure look like if the hypothesis is wrong? For example, the τₑ ~ R² confinement scaling claim (the physical basis for why orbital deployment is advantageous) is flagged as unverified but not framed as a falsifiable hypothesis. The He3 self-breeding pathway is identified as missing but its failure mode (concept is fuel-supply-constrained at commercial scale regardless of plasma physics) is not stated as a consequence. The result is a risk section that diagnoses problems without anchoring what a negative result means for the concept's viability.
- **Recommendation:** For the 2–3 highest-stakes technical bets, add an explicit hypothesis statement and failure mode. Suggested structure: (a) Confinement scaling — "Hypothesis: τₑ ~ R² scaling reaches Q > 1 at meter-scale dipole radius in D-He3 conditions. Failure mode: if τₑ scaling is weaker than R² (as seen in some tokamak edge-mode analogues), net power is unachievable at commercially relevant device mass and no orbital advantage compensates." (b) He3 self-breeding — "Hypothesis: D-D side reactions in a dipole geometry can breed He3 at a rate sufficient to sustain commercial fuel supply. Failure mode: if self-breeding is insufficient, the concept depends on market He3 at ~$30M/kg, making fuel cost alone non-competitive with any D-T concept." (c) Power beaming — "Hypothesis: end-to-end power beaming efficiency (conversion → transmitter → atmosphere → rectenna) exceeds ~30% at multi-MW scale. Failure mode: if beaming efficiency is <20%, the delivered-electricity LCOE cannot compete with terrestrial alternatives regardless of fusion performance." These framings require no new data and directly address Goal 5.
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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/iter-2/model_setup.py`
