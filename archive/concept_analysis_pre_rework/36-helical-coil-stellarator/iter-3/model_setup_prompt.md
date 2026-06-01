# 1costingfe Model Update: Helical Coil Stellarator

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: H Confinement Factor Risk Is Overstated Given W7-X Experimental Data
- **Target:** Section 2 (Challenge 2) and Section 5 (parameter row: H confinement improvement factor)
- **Category:** analysis
- **Finding:** The analysis frames HESTIA's H = 1.3 assumption as an unverified optimistic claim at risk of H = 1.0 (no improvement), with low confidence. The Helios preconceptual stellarator design study (arxiv-2512-08027, 2024) reports that W7-X has achieved H_ISS04 = 1.4 experimentally, which the Helios authors use as their own design baseline. HESTIA's assumed H = 1.3 is *below* W7-X's experimentally demonstrated performance, making it conservative relative to the state of the stellarator confinement database rather than an unjustified optimistic assumption.
- **Recommendation:** Update Section 2 Challenge 2 to note that W7-X experimental operation has validated H_ISS04 ≥ 1.4 (per Helios design study, arxiv-2512-08027), and that HESTIA's H = 1.3 assumption is therefore below recent stellarator experimental performance rather than above it. The residual risk is not that H = 1.3 is overoptimistic, but that HESTIA's heliotron geometry and plasma parameters differ from W7-X and may not transfer directly. Update the confidence rating in the Section 5 parameter table from "low" to "medium" with a note explaining the basis.
- **Priority:** important

### F-2: Contemporary Stellarator FPP Study Chose 40% Steam Rankine Over sCO₂
- **Target:** Section 2 (Challenge 4) and Section 3 (sCO₂ TRL subsystem)
- **Category:** analysis
- **Finding:** The analysis frames HESTIA's >50% sCO₂ target as an instance of a "field-wide unsolved design problem" but lacks a direct stellarator comparator. The Helios preconceptual design (arxiv-2512-08027, 2024) — a contemporary, well-documented stellarator FPP study — explicitly chose 40% steam Rankine cycle over sCO₂, achieving 390 MWe net output at a 40% efficiency assumption. This is a material comparator because it shows that a peer stellarator design study, working at the same time and with the same state of knowledge, concluded that 40% Rankine is the appropriate conservative power cycle assumption, while sCO₂ at >50% remains aspirational.
- **Recommendation:** Add a sentence to Section 2 Challenge 4 and Section 3 noting that the Helios stellarator design study (2024, arxiv-2512-08027) selected 40% steam Rankine as its baseline, explicitly not sCO₂. This strengthens the framing: HESTIA's >50% sCO₂ target is not merely behind the broader sCO₂ R&D field — it diverges from the contemporary stellarator design consensus on achievable power conversion efficiency. The analysis should acknowledge that a 40% Rankine fallback scenario (as used by Helios) would reduce Q_eng below 2.0 and must be modeled as a scenario branch.
- **Priority:** important

### F-3: GTI STEP Demo Provides Updated TRL Milestone for sCO₂ at MW Scale
- **Target:** Section 3 (sCO₂ Brayton Power Conversion at Fusion Outlet Temperature — TRL 3–4) and Section 6 (Gap #6)
- **Category:** analysis
- **Finding:** The analysis states sCO₂ is "commercial at MW-to-GW scale in fossil power and CSP plants" but does not reference the most recent large-scale demonstration milestone. GTI Energy's STEP Demo (October 2024) achieved 10 MWe at 500°C in Phase 1 and is targeting 715°C in Phase 2 — described as "the largest scale demonstration of the technology to date" and confirming "commercial readiness" of the basic sCO₂ cycle. HESTIA requires 800–1200 K (527–927°C); the GTI Phase 2 target of 715°C (988 K) falls within HESTIA's lower temperature range. This is a material TRL update: the technology is within experimental reach of fusion-relevant temperatures at MW scale as of 2024, which changes the TRL characterization from "commercial in CSP/fossil" (implying steady-state mature deployment) to "MW-scale demonstration advancing toward fusion-relevant temperatures."
- **Recommendation:** Update the Section 3 sCO₂ subsystem "Demonstrated" bullet to include the GTI STEP demo: 10 MWe achieved at 500°C (Phase 1 complete, October 2024), with Phase 2 targeting 715°C — the largest sCO₂ demonstration to date and approaching HESTIA's 800 K lower bound. Note that Phase 2 completion (715°C) would reduce the temperature gap from HESTIA's minimum requirement to ~85°C, making the near-term technology trajectory material to the TRL assessment. Also update Section 6 Gap #6 source recommendation to reference this milestone.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Coil cost — dominant cost item has no upper-bound scenario
- **Target:** Model output (C220103) and Section 7 (coil cost structure discussion)
- **Category:** model
- **Finding:** C220103 continuous helical coil cost ($2,322M) is 71% of RPE and ~34% of total capital. It is also the #1 LCOE sensitivity parameter (r_coil elasticity = 1.36). The model explicitly flags it as "DEFAULT — LOWER BOUND; cont. helical premium not captured." The analysis argues at length in Section 7 that HESTIA's continuous helical winding is more expensive than modular QI coil geometry, cites QI modular designs carrying a 1.5–5× manufacturing premium per unit fusion power over wound tokamaks, and concludes "the heliotron coil topology is expected to be a cost penalty relative to QI modular designs at FOAK." But this argument never produces a multiplier or scenario in the model. The LCOE output is described only as a lower bound with no upper bound specified — leaving the most important cost driver unbounded.
- **Recommendation:** Add a coil cost multiplier sweep to the model (e.g., 1×, 2×, 3× the DEFAULT C220103 value). The analysis's own Section 7 comparison to QI modular designs (1.5–5× manufacturing premium) provides a basis for the range. Report the resulting LCOE envelope alongside the base case. This directly tests the concept's central cost hypothesis and converts the current lower-bound-only output into a bounded range.
- **Priority:** blocking

### F-2: Primary LCOE output uses back-solved operating point inconsistent with design Q
- **Target:** Model output (top-line summary) vs. sCO₂ scenario sweep
- **Category:** model
- **Finding:** The top-line model reports P_net = 70.4 MWe and Q_eng = 1.71 at η_th = 50%, but the physics-forward sCO₂ scenario sweep (Q = 13 fixed, P_fus = 260 MW) gives P_net = 52.3 MWe and Q_eng = 1.53 at the same efficiency. The model's CRITICAL note acknowledges this: "Framework inverse balance at P_net = 70.4 MWe implies P_fus > 260 MW (Q_sci > 13)." The framework is back-solving to a higher plasma Q than the published design assumption to force the published net output. The headline LCOE of 1164 $/MWh is therefore for a plant requiring Q_sci > 13 — yet the analysis narrative and all challenge framing is built around Q~13. Cross-concept comparisons using the top-line figure embed this inconsistency without warning.
- **Recommendation:** Designate the physics-forward operating point (P_net ≈ 52 MWe at η_th = 50%, Q = 13 fixed) as the primary model output and report its LCOE as the design-point result. The sCO₂ scenario sweep already computes this; promote it. The current top-line (back-solved to 70.4 MWe) may be retained as a reference case, but must be clearly labeled as requiring Q_sci > 13 with the implied Q stated explicitly.
- **Priority:** important

### F-3: No upper-bound LCOE scenario anchored to published cost
- **Target:** Section 7 (cross-concept modeling note) and Section 2, Challenge 1
- **Category:** analysis
- **Finding:** The analysis correctly establishes that the ARIES-calibrated framework gives a structural lower bound because it cannot reproduce the inflation-adjusted $10B cost anchor (~$143B/GWe). Section 7 states "a proper LCOE comparison requires rebuilding the HESTIA cost structure from first principles" but gives no guidance on how to do this — no upper-bound scenario using the published cost is defined, and the analysis does not state why the framework is the appropriate modeling tool given the known divergence. The checklist criterion (whether free-form or parameterized modeling is appropriate and why) is not addressed. The result is that the analysis provides only a lower-bound LCOE with the upper bound entirely undefined.
- **Recommendation:** Add a scenario in Section 2 (Challenge 1) or Section 7 that computes an upper-bound LCOE directly from the inflation-adjusted $10B cost anchor: hold O&M, financing, and capacity factor at framework values, substitute $10B overnight cost, and report the resulting LCOE alongside the framework lower bound. State explicitly that the analysis recommends free-form modeling with the ARIES framework as a lower bound and the published-anchor scenario as an upper bound, and that cross-concept comparison requires both figures. This gives the concept an LCOE range rather than a floor with no ceiling.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_stellarator.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/iter-3/model_setup.py`
