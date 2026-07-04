# Domain Knowledge

Curated domain insights that have passed through the research approval gate or been captured inline during modeling work. Each entry is a structured record of something we know about the domain that affects how we model it.

This file is the actionable feed for modeling work. Raw research lives in `knowledge/research/`; only approved, structured insights belong here.

---

*No entries yet. Domain insights (DI-XXX) will be derived from research conducted under the investigation-driven workflow.*

*Previous entries (DI-001 through DI-014) archived to `archive/knowledge/KNOWLEDGE.md`.*

### DI-001: IFE Fusion Cycle Gain Viability Threshold
- **Source**: EIF-1992, Accel-2013, Xcimer-2026
- **Context**: The product eta*G (driver efficiency times target gain) must exceed ~10 for economically viable IFE. This creates fundamentally different gain requirements by driver type: heavy-ion needs G>33 (at 30% eta), lasers need G>140 (at 7% eta), pulsers need G>100 (at 10% eta).
- **Model implications**: The gain requirement constraint should be a validation check in all IFE concept models
- **Analysis implications**: Concepts below the eta*G>10 threshold should be flagged as requiring breakthrough physics
- **Status**: captured

### DI-002: CAS22 is the IFE-MFE Divergence Point
- **Source**: ARIES-2013, PyFECONS, Hawker-2020
- **Context**: The CAS framework (20-99) is universal across fusion approaches. MFE and IFE share CAS20-21, 23-27, and 91-99. All concept-specific differences concentrate in CAS22 sub-accounts: 22.1.3 (magnets to driver), 22.1.4 (heating to ignition), 22.1.8 (divertor to target factory). PyFECONS confirms via polymorphic Union types.
- **Model implications**: Library components for CAS23-27 and indirect costs are fully reusable across MFE and IFE
- **Analysis implications**: Cross-concept comparison at CAS-level should normalize CAS22 sub-accounts by function
- **Status**: captured

### DI-003: IFE Target Cost is a Unique Operating Cost Category
- **Source**: Hawker-2020, HIF-1986, PyFECONS
- **Context**: IFE has a per-shot consumable cost (manufactured targets at $0.19-100 each) with no MFE parallel. Hawker shows target cost has stronger LCOE correlation (+0.186) than driver cost (+0.075), with a threshold effect: below ~$10/target, further reduction provides limited benefit.
- **Model implications**: IFE cost models must include target manufacturing as an operating cost separate from driver capital cost
- **Analysis implications**: The $10/target threshold is a key competitiveness indicator for IFE concepts
- **Status**: captured

### DI-004: IFE Driver Cost Reference Points
- **Source**: Hawker-2020, Xcimer-2026, AMPS-2025, HIF-1986
- **Context**: Driver cost per joule spans 3 orders of magnitude: NIF $9.5/J, DPSSL $700-1000/J (floor), Xcimer KrF-NLO $60-120/J FOAK, pulsed-power $1.7-6/J. Heavy-ion induction linacs fall in between. These reference points anchor cost model calibration.
- **Model implications**: Driver cost parameter ranges must be set per-driver-type, not as a single universal range
- **Analysis implications**: The $100/J threshold identified by Xcimer appears to be a rough dividing line between economically viable and non-viable laser IFE
- **Status**: captured

### DI-005: Hawker 14-Parameter IFE LCOE Model
- **Source**: Hawker-2020
- **Context**: Hawker identifies 14 technology-agnostic parameters sufficient to characterize IFE LCOE. Top sensitivities by Pearson correlation: discount rate (+0.247), plant cost (+0.210), target cost (+0.186), gain (-0.164), driver lifetime (-0.134), availability (-0.127). The frequency-yield trade-off is the most important interaction: high yield + low frequency unlocks the lowest LCOE designs.
- **Model implications**: All 14 parameters should be captured as model attributes with ranges; the model should support parametric variation across them
- **Analysis implications**: Sensitivity analysis should explore 2D interactions (especially frequency vs. yield), not just 1D parameter sweeps
- **Status**: captured

### DI-006: LCOE nonlinearity: center-of-range defaults ≠ center LCOE
- **Source**: work-item:WI-007/verify_ife_lcoe.py
- **Context**: Hawker's 14 Monte Carlo parameter defaults (center of uniform distributions) produce LCOE=$252.30/MWh — far above the $25-120/MWh range reported by Hawker. This is because LCOE is highly nonlinear: low frequency (0.2 Hz) yields a 44 MW plant where capital costs dominate. Realistic HIF parameters (f=5Hz, eta=0.25) give $68.69/MWh. *(Figures corrected 2026-07-04 — a digit corruption had dropped the leading "2"s; verified against `scripts/verify_ife_lcoe.py`. See WI-016 `retro_capture_hawker.md`.)*
- **Model implications**: SV-008 verified at realistic design points, not Monte Carlo centers. Default parameters in ife_cost_parameters.sysml represent distribution ranges for Monte Carlo, not an optimized design.
- **Analysis implications**: When running parametric sweeps, report LCOE distribution statistics rather than evaluating at parameter midpoints. Small plant sizes (<100 MW) amplify capital cost impact.
- **Status**: captured
