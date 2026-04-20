# Free-Form Model Update: Muon-Catalyzed Fusion (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Alpha-sticking initial vs. effective distinction unresolved in analysis

- **Target:** Section 2 (Challenge 2: Alpha-sticking) and Section 5 (Parameters table, alpha-sticking rows)
- **Category:** analysis
- **Finding:** The arxiv source (Kamimura & Kino 2021, arXiv:2112.08399) is a theoretical calculation of the dtμ molecule that reports an *initial* sticking probability ω_S⁰ = 0.857% — which is significantly higher than the 0.3–0.5% cited throughout the analysis. These values are not contradictory (initial sticking is reduced to effective sticking by muon reactivation as the alpha particle decelerates), but the analysis nowhere explains this distinction. Section 2 describes sticking as "the ~0.3–0.5% probability that a muon attaches to the alpha particle" without clarifying whether this is initial or effective. Section 5's parameter table similarly labels both rows "Alpha-sticking probability" without the initial/effective qualifier. A reader comparing the analysis to the literature — which reports both ~0.86–0.93% initial values and ~0.3–0.6% effective values — will find an apparent contradiction that the analysis cannot resolve through its current text. This directly affects Goal 5 (Risks and Assumptions), where the sticking probability is the physics ceiling on fusions/muon — the ceiling derivation depends on which quantity is used.
- **Recommendation:** In Section 2, clarify that the 0.3–0.5% figure is the *effective* (post-reactivation) sticking probability — i.e., the fraction of muons permanently lost per fusion event after accounting for muon stripping from decelerated alphas. Add one sentence explaining the distinction: initial sticking (~0.86%) is partially reversed as the alpha decelerates, recovering muons via Auger transfer; the effective sticking (~0.3–0.5%) is what sets the fusions/muon ceiling. In Section 5, relabel the two parameter rows as "Alpha-sticking probability, initial (ω_S⁰)" and "Alpha-sticking probability, effective (post-reactivation)" and add arXiv:2112.08399 as a source for the initial value.
- **Priority:** minor

### F-2: Misfiled source must not be incorporated; flag for removal

- **Target:** Section 8 (Sources) and Section 6 (Data Gap #2 — accelerator capital cost analogues)
- **Category:** analysis
- **Finding:** The source osti-servlets-purl-1345779 is an ORNL paper on ten-year operational experience with the SNS spallation neutron source superconducting linac (Kim et al.). It contains zero muon-catalyzed fusion content — the words muon, catalysis, fusion energy, deuterium, and tritium do not appear. It was included in the iter-01 sources directory but is entirely off-topic for this concept. Separately, the SNS data it contains (972 MeV output, 1.4 MW beam power, 98% SCL availability, pulsed 60 Hz operation) describes a spallation neutron source at sub-GeV proton energy — a different machine class from the CW multi-GeV accelerator MCF requires. The existing analysis already identifies SNS ($1.4B, 1 GeV, 1.4 MW) as a capital cost upper-bound analogue in Data Gap #2 via separate citation. Incorporating this OSTI source would add nothing to the analysis and its SNS availability data (98%) would be misleading if presented as analogous to a CW muon source accelerator (SNS is pulsed, not CW; its availability metric reflects a different operational model).
- **Recommendation:** Do not add osti-servlets-purl-1345779 to Section 8. Flag it for removal from the concept research directory (it belongs, if anywhere, in a heavy-ion or spallation-neutron concept). No changes to the analysis text are needed — the SNS capital cost figure already cited in Data Gap #2 came from the existing source inventory and should remain as-is.
- **Priority:** minor

---

**Note on inis-records-zmph4-5p723**: This source (Fadeev & Solov'ev 1995, JINR-E--1-95-29, "The pion (muon) energy production cost in muon catalyzed fusion") is directly on-topic for the ~6 GeV conventional muon production cost claim — its title and abstract indicate it contains quantitative analysis of pion/muon yield vs. energy expenditure across accelerator configurations (4 tables). However, only the INIS bibliographic record was extracted; the PDF content is inaccessible. No finding is raised because the source content cannot be assessed. If the PDF is retrievable from R2, it should be re-extracted via the agentic-mbse pipeline before any further analysis passes — it may contain quantitative refinements to the muon energy cost parameter (currently cited as ~6 GeV with "high" confidence) that would improve or update Section 5.

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Analysis never states that Acceleron's operating point is an energy sink
- **Target:** Section 2 (Energy Balance discussion) and Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Section 2 correctly identifies energy balance as a Critical challenge and cites Kelly et al.'s 14%-net-output result. Section 7 notes the 47% recirculating fraction as a key differentiator. But neither section reaches the logical conclusion: at Acceleron's stated targets (2.5 GeV, 200 fusions/muon, η_th=50%), Q_sci=1.41 and gross/driver=0.78 — net-negative electricity under standard conversion efficiency assumptions. The model scenario table makes this explicit ("SINK"), but the analysis text never says it. This is the most important risk framing for this concept: a company whose self-reported operating point cannot produce net electricity (under independent assumptions) has a categorically different risk profile than one that achieves positive Q but high LCOE. The $0.025/kWh contour target must therefore assume either non-standard conversion efficiency or physics parameters not visible in the available sources — and the analysis should flag this explicitly as a discrepancy rather than treating Acceleron's LCOE target as a credible near-term anchor.
- **Recommendation:** Add a concluding paragraph to Section 2 (or a note to Section 7) stating: at Acceleron's stated operating point, independent analysis finds net-negative electricity output (Q_sci=1.41, gross/driver≈0.78 at η_th=50%); the $0.025/kWh ARPA-E target therefore either assumes undisclosed conversion efficiency gains or requires physics parameters beyond those stated. Frame this as a bifurcation in the risk landscape: the primary question is not LCOE level but whether net positive power is achievable at the stated operating point.
- **Priority:** blocking

### F-2: Only one nearest-neighbor concept named
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Section 7 names heavy-ion beam ICF (25-heavy-ion-beam-icf) as the only structural analogue, then correctly notes it is "distant." The analysis stops there. Goal 1 requires identifying 2–3 nearest neighbors with explicit comparison rationale. Even if no concept is a close structural twin, the concept landscape includes other driver-cost-dominated or non-plasma concepts worth positioning against — e.g., MagLIF (07-maglif) shares the large pulsed-power driver as dominant cost item and the same energy-sink-at-current-state problem; electrostatic hybrid (13-electrostatic-hybrid) is also classified Non-Standard with an external power input driving fusion. Naming only one concept as a "distant analogue" leaves the cross-concept comparison underdeveloped and makes it harder to assess whether cost modeling patterns from any existing analysis are reusable.
- **Recommendation:** Identify 2–3 nearest neighbors from the concept landscape. For each, state one specific TEA-relevant comparison (what can be borrowed, what cannot, and why). The comparison does not need to be structurally close — it should be TEA-relevant: which other concepts face the same "recirculating power fraction dominates LCOE" problem, and what does that literature say about the cost corridor?
- **Priority:** important

### F-3: Modeling approach choice not stated; sensitivity parameters not explicitly named
- **Target:** Section 2 and the analysis's modeling recommendations (Goal 4)
- **Category:** analysis
- **Finding:** The model header labels the approach "1cFE CAS-Structured Free-Form" but the analysis text never explains why free-form was chosen over 1costingfe. Section 2 ranks challenges by impact label (Critical / High / Moderate) but does not explicitly name the 2–3 parameters with highest LCOE sensitivity or frame them as model levers. The sensitivity analysis in the model output clearly shows that E_mu (muon energy cost), N_fus (fusions/muon), and accelerator capital cost are the three dominant parameters — but this hierarchy does not appear in the analysis narrative, leaving the connection between challenge ranking and modeling priorities implicit.
- **Recommendation:** Add a brief paragraph at the end of Section 2 (or as a new Section 2.5 "Modeling Approach") that: (1) states free-form modeling was chosen because the dominant cost item (particle accelerator) has no analog in 1costingfe's plasma-centric CAS accounts; (2) names E_mu, N_fus, and accelerator capital cost as the three parameters with the highest LCOE sensitivity; and (3) frames the key testable hypothesis as a proposition — e.g., "Commercial viability requires simultaneous achievement of E_mu ≤ X GeV and N_fus ≥ Y; the model tests whether any combination within the physics ceiling satisfies LCOE < $0.05/kWh."
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/analysis.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/iter-2/model_setup.py`
