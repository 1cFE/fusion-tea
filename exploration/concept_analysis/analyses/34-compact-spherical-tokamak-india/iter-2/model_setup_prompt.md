# 1costingfe Model Update: Compact Spherical Tokamak - India

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/34-compact-spherical-tokamak-india/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/34-compact-spherical-tokamak-india/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: New arXiv preprint provides first published Pranos plasma device parameters
- **Target:** Section 1 (Availability of Data) and Section 8 (Sources)
- **Category:** analysis
- **Finding:** The analysis states "Peer-reviewed publications: None found for Pranos Fusion specifically" and treats no machine parameters as published. The new source (arxiv-2603-11549, submitted March 2026) is a technical paper on PRAGYA — India's first privately developed low-aspect-ratio tokamak by Pranos Fusion — that provides confirmed design parameters: major radius R₀ = 0.4 m, minor radius a > 0.18 m (aspect ratio ≈ 2.2), toroidal field B_T = 0.1 T, and plasma current up to 25 kA. These are experimental-device parameters (not the commercial 50 MW target), but they are the first published technical specifications for any Pranos hardware. The analysis's Section 1 data confidence ratings and "no publications" claim are now outdated.
- **Recommendation:** Update Section 1 to register arxiv-2603-11549 as Source 3 and note it as a preprint (not yet peer-reviewed). Add a sentence clarifying that the published parameters describe PRAGYA (the experimental precursor device, not the commercial 50 MW module). Update Section 8 with a full citation entry. Revise the "Peer-reviewed publications: None found" statement to "Peer-reviewed publications: None found; one arXiv preprint (arxiv-2603-11549, March 2026) describes the PRAGYA experimental device." Add PRAGYA's parameters to Section 5 as a new row block for the experimental baseline.
- **Priority:** important

### F-2: TRL assessment for plasma physics and magnet system understates current Pranos progress
- **Target:** Section 3 (Maturity of Key Subsystems) — Plasma Physics Experimental Basis and Magnet System entries
- **Category:** analysis
- **Finding:** Section 3 rates Plasma Physics Experimental Basis at TRL 1–2 based on "working with plasma in a glass globe" and rates the Magnet System at TRL 2–3. The arXiv paper describes PRAGYA as in "final design phase" with 3D finite element structural analysis complete for the vacuum vessel (combined self-weight, atmospheric pressure, thermal stress) and confirms required safety margins are satisfied, with the device ready for "subsequent plasma operations." This is meaningfully higher than the glass-globe characterization — it describes a complete engineering design validated for fabrication and near-term plasma commissioning. The analysis's "Demonstrated / On paper only / Missing at scale" breakdown in Section 3 does not reflect this engineering milestone.
- **Recommendation:** Update the Plasma Physics Experimental Basis entry to note that PRAGYA (R₀ = 0.4 m ST) is in final engineering design with structural validation complete and plasma commissioning imminent — revise the TRL range to 2–3 for the experimental device. Update the Magnet System entry similarly (structural FEM complete = TRL 3 for the device under development). Maintain the caveat that PRAGYA is a low-field experimental device (0.1 T) far from a commercial operating point and that TRL for the commercial 50 MW concept remains TRL 1.
- **Priority:** important

### F-3: Section 5 parameter table should include PRAGYA experimental design point
- **Target:** Section 5 (LCOE-Relevant Parameters) — Available Parameters table
- **Category:** model
- **Finding:** Section 5's parameter table has no entry for any Pranos machine geometry, listing R, A, and B_T as blocking gaps. The arXiv paper fills this gap for the experimental device: R₀ = 0.4 m, a > 0.18 m, A ≈ 2.2, B_T = 0.1 T, Ip ≤ 25 kA. While these parameters do not anchor the commercial 50 MW LCOE model (the experimental device operates at a tiny fraction of commercial scale and field), they establish the ST family membership (A ≈ 2.2 confirms spherical tokamak classification) and provide the first physics baseline for the company's design trajectory. The aspect ratio is an important parameter for cost structure comparisons against the nearest neighbor (21-spherical-tokamak-hts, A ≈ 2.3).
- **Recommendation:** Add a row block to the Section 5 Available Parameters table for PRAGYA experimental device parameters (R₀, a, A, B_T, Ip) with source arxiv-2603-11549, confidence "medium" (preprint), and a Notes column entry: "Experimental precursor device; not the commercial 50 MW target. B_T = 0.1 T is far below any commercial operating point. A ≈ 2.2 confirms ST family classification consistent with nearest-neighbor comparison." Update the Missing Parameters table to change the R, A, B_T gap from "proprietary / not-yet-published" to "experimental baseline known (PRAGYA); commercial design point truly-unknown."
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Plasma parameters have zero elasticity — model cannot test the concept's primary risk
- **Target:** Model sensitivity sweep / model_setup.py
- **Category:** model
- **Finding:** The analysis correctly identifies unknown machine parameters as the single most critical gap (Challenge 2, Impact: Critical). The sensitivity sweep shows that T_e, n_e, B, plasma_volume, q95, Z_eff, tau_ratio, and all disruption parameters have 0.0 elasticity. Plasma physics inputs do not propagate through to LCOE. The model is computing cost from assumed fixed values rather than deriving fusion power from plasma state — meaning the model cannot test how uncertainty in plasma parameters (the analysis's #1 blocking gap) translates to LCOE uncertainty. This renders the sensitivity table uninformative for the concept's most important unknowns.
- **Recommendation:** Wire plasma parameters into the fusion power calculation so that T_e, n_e, and B_T drive fusion power → thermal power → net electric → LCOE. At minimum, the sensitivity sweep should show non-zero elasticity for T_e, n_e, and magnetic field strength. The goal is not precision (all values are analogues) but to make the model capable of propagating uncertainty in the parameters the analysis identifies as blocking gaps.
- **Priority:** blocking

### F-2: Model overnight cost exceeds stated analogue range by ~60%
- **Target:** Section 5 parameter table / model_output.txt
- **Category:** model
- **Finding:** Section 5 states the analogue specific capital cost is "$10,000–$30,000/kWe" based on ARIES-ST scaling applied to a 50 MWe unit. The model output reports overnight cost of $47,754/kWe — exceeding the stated upper bound by approximately 60%. This internal inconsistency means the model's cost structure is not calibrated against the analysis's own stated analogue range. A reader relying on Section 5 would have materially incorrect expectations about the model result. (If $47,754/kWe represents total capital including IDC rather than overnight, the output label is also misleading — IDC of $525.9 M on a $1,862 M overnight base is a large fraction that should be broken out clearly.)
- **Recommendation:** Reconcile the discrepancy. Either (a) update the Section 5 analogue range to reflect the actual model output and explain why the modeled cost exceeds prior ARIES-ST estimates (e.g., additional indirect cost fractions, India regulatory penalty, or different cost account coverage), or (b) identify and correct the cost inputs driving the model above the analogue range. If the $47,754/kWe figure includes IDC, relabel the model output line clearly as "Total capital (incl. IDC)" and state overnight separately.
- **Priority:** important

### F-3: Section 2 challenges are framed as unknowns, not testable model hypotheses
- **Target:** Section 2 (Challenges) / Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Goal 4 requires key hypotheses stated as testable propositions. Section 2 correctly ranks challenges by impact but frames them as unknowns to be resolved ("magnet type unknown," "Q value unknown," "no heating method disclosed"). This is useful for a gap inventory but does not produce testable propositions that the cost model can confirm or refute. For example: what would the model show if the magnet choice is resistive copper rather than HTS? What is the LCOE break-even factory learning rate that makes the modular fleet thesis viable? Without hypotheses in this form, the analysis cannot identify what scenario branches the model should explore.
- **Recommendation:** Add 2–3 explicit model hypotheses to Section 2 or Section 7, stated as "IF [assumption], THEN [cost implication], testable by [parameter sweep or scenario branch]." Candidates: (H1) HTS vs. resistive copper magnet scenario — if copper chosen, recirculating power fraction rises to 30–40% of gross electric, materially degrading Q_eng; (H2) Factory learning threshold — the 50 MWe modular fleet is LCOE-competitive only if cumulative production learning delivers ≥20% cost reduction per doubling of units produced; (H3) India regulatory scenario — applying the Stewart & Shirvan 2.2× building cost multiplier pushes LCOE above $1,000/MWh. Each hypothesis should be reflected as a named scenario or sensitivity branch in model_setup.py.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/34-compact-spherical-tokamak-india/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_tokamak.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/34-compact-spherical-tokamak-india/iter-2/model_setup.py`
