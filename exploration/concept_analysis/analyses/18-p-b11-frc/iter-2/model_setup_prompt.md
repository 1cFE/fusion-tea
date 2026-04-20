# Free-Form LCOE Model: p-B11 FRC

You are building a standalone LCOE model for **p-B11 FRC** (TAE Technologies).
This concept does not map cleanly to any standard 1costingfe ConfinementConcept,
so you will build a self-contained model from first principles following the
CAS cost accounting structure.

## Your Task

Write a self-contained Python script that computes LCOE from first principles.
No external dependencies beyond the standard library. The script must be directly
runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/analysis.md`
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

### F-1: Capacity factor and recirculating power treated as independent gaps rather than compounding risk
- **Target:** Section 2 (Challenge 3: NBI recirculating power fraction) and Section 5 (Gap #13: capacity factor)
- **Category:** analysis
- **Finding:** The new source (arxiv-2103-12451, a general fusion plant economics paper) frames recirculated power fraction and capacity factor as interdependent: when a plant operates below rated power, recirculated power remains near its full-load level, so the *effective* recirculating power fraction rises. The current analysis derives the minimum Q_plasma requirement in Section 2 at rated power only, and lists capacity factor separately as a data gap. It does not analyze how sub-unity capacity factor tightens the Q_plasma floor — a compounding penalty that is particularly acute for first-generation plants. For p-B11 FRC, this matters because: (a) CW FRC operation is undemonstrated (current pulse duration ~30–40 ms), so early Da Vinci capacity factor could be substantially below 90%; and (b) NBI must be on continuously for plasma stability, meaning the recirculating load does not scale down proportionally with output. The Section 2 derivation showing "Q_plasma >> 10 required" is a best-case figure that worsens under realistic capacity factor assumptions.
- **Recommendation:** In Section 2 (Challenge 3), add a sentence or short paragraph noting that the Q_plasma floor derived at rated power is a lower bound — that sub-unity capacity factor (plausible for a first-generation FRC with undemonstrated CW operation) raises the effective recirculating power fraction and tightens the requirement further. In Section 5 missing parameters table, add an explicit note to Gap #13 (capacity factor) cross-referencing the Q_plasma sensitivity derived in Section 2: the two gaps interact multiplicatively, not independently. In the modeling parameters, consider flagging capacity factor as a sensitivity axis specifically for its interaction with NBI recirculating power, not just as a standalone uncertainty.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: No modeling approach recommendation
- **Target:** Section 2 (Challenges) — modeling approach recommendation
- **Category:** analysis
- **Finding:** The analysis never states whether 1costingfe or free-form modeling is appropriate for this concept, nor explains why. The checklist requires this explicitly. Given that the analysis documents 6 "blocking" data gaps, zero demonstrated Q_plasma > 1, and a physics-unknown (not engineering-unknown) barrier to any LCOE, the appropriate answer is almost certainly "free-form with scenario branches" — but it is left entirely implicit. The model agent cannot make a principled modeling choice without this framing, and it is non-trivial: this is the only concept in the pipeline where the fundamental question is whether a positive LCOE exists at all, not what its value is.
- **Recommendation:** Add a brief modeling approach paragraph to Section 2 or a dedicated subsection before Section 5. It should (a) state that 1costingfe is inappropriate because the physics floor (Q_plasma > 1 for p-B11) is not established, (b) recommend free-form scenario modeling with at least two branches — "physics succeeds" (Q_plasma achievable, thermal conversion baseline) and "ICC upgrade" (Q_plasma achievable, direct conversion at >90% efficiency), and (c) note that a third branch ("physics fails") has no LCOE output and should be flagged explicitly in the model as a non-viable outcome.
- **Priority:** blocking

### F-2: Challenges stated as unknowns, not testable hypotheses
- **Target:** Section 2 (Challenges) and Section 5 (Parameters)
- **Category:** model
- **Finding:** The analysis correctly identifies the critical challenges (bremsstrahlung power balance, NBI recirculating power fraction, temperature extrapolation) but frames them all as open physics questions rather than as testable propositions with economic thresholds. Goal 4 requires "key hypotheses stated as testable propositions — not just open questions." The NBI Q_eng derivation in Section 2 is the closest thing to a testable proposition, but it is presented as an illustration of the challenge, not as a structured hypothesis the model should evaluate. Without explicit threshold conditions, the model cannot set up meaningful sensitivity sweeps or scenario branches.
- **Recommendation:** Convert the top 2–3 challenges into IF-THEN propositions. For example: "IF Q_plasma > 15 AND NBI wall-plug efficiency > 55%, THEN net electricity is achievable at Da Vinci's 50 MWe scale with thermal conversion; otherwise the concept does not produce net electricity and has no LCOE." Add these propositions explicitly to Section 2 and ensure the model's sensitivity sweep spans the Q_plasma and NBI efficiency parameter space around the viability threshold — not just within a narrow range of assumed-viable values. The Section 5 "Missing Parameters" table already lists the right parameters (Q_plasma, NBI wall-plug efficiency); they need associated threshold conditions so the model has something to test.
- **Priority:** important

### F-3: p-B11 aneutronic concept peers absent from nearest-neighbor comparison
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** The analysis identifies Helion FRC (08-frc-w-direct-conversion) as the closest near-neighbor, which is appropriate for the FRC confinement topology comparison. However, the concept landscape contains at least four other p-B11 aneutronic concepts — 06-magnetic-mirror (Pale Blue Fusion, p-B11), 04-laser-icf (HB11 Energy, p-B11 fast ignition), 23-laser-icf-nanostructured-target (Marvel Fusion, p-B11), and 24-dense-plasma-focus (LPPFusion, p-B11) — none of which appear in Section 7. Goal 1 asks "What family does it belong to, and what are the nearest neighbors?" The nearest neighbors on the fuel dimension are entirely missing. This matters for TEA positioning: the aneutronic fuel advantage (no tritium, minimal neutrons, hands-on maintenance) is shared by all four of these concepts — what distinguishes the FRC NBI-driven approach from the mirror, DPF, or laser approaches to p-B11 is not discussed.
- **Recommendation:** Expand Section 7 with a 2–3 paragraph comparison covering the p-B11 concept peer group. For each peer, note: (1) the shared aneutronic TEA advantages (same cost structure relief as TAE), (2) the different physics approach and what that means for the bremsstrahlung challenge (DPF and laser ICF take a compressed/pulsed path; mirror takes a different steady-state path), and (3) whether TAE's NBI-driven FRC has a structural advantage or disadvantage vs. these alternatives in achieving the required ion temperatures. The Helion comparison should be reframed as a confinement-topology neighbor, with the p-B11 peers framed as fuel-dimension neighbors. The two dimensions are complementary, not redundant.
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

Follow the MagLIF exemplar's 5-layer structure adapted for p-B11 FRC:

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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/iter-2/model_setup.py`
