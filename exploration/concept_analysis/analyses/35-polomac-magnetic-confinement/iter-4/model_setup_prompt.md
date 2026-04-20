# Free-Form Model Update: PoloMac Magnetic Confinement

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/35-polomac-magnetic-confinement/iter-4/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/35-polomac-magnetic-confinement/iter-4/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Specific performance predictions absent from Section 5 parameter table
- **Target:** Section 5 (LCOE-Relevant Parameters) and Modeling Approach Rationale
- **Category:** analysis
- **Finding:** The full JTSP 2024 paper (previously only the abstract was available) contains specific quantitative performance predictions for D-D operation that are entirely absent from the analysis: predicted confinement time of 20–40 s, plasma temperature of 100–200 keV, plasma density of 10²¹ m⁻³, and a refined magnetic field claim of "half magnetic field, i.e. 2–3 T rather than 5.3 T" (more specific than the "3× weaker" abstract claim). These are Deutelio's own unvalidated projections, but they are the company's stated scenario basis and belong in the parameter table. The Modeling Approach Rationale section discusses scenario bounds without reference to these claimed values, making the scenario framing appear entirely invented rather than anchored to the company's own claims. The 20–40 s confinement prediction is especially notable: it would exceed ITER's predicted 4–5 s by 4–10×, which frames the extraordinary nature of the physics claim.
- **Recommendation:** Add a "Company predictions (unvalidated)" row block to the Section 5 parameter table covering confinement time (20–40 s), D-D temperature target (100–200 keV), density target (10²¹ m⁻³), and refined DT field claim (2–3 T). Mark confidence as "very low — company claim, no experimental or physics basis." In the Modeling Approach Rationale, add a sentence noting that the high-Q scenario (Q ≥ 10) corresponds to Deutelio's own projections and that these predictions are extraordinary relative to any validated experiment.
- **Priority:** important

### F-2: Heating method gap is partially resolved — prototype uses ECH; analysis states "truly-unknown"
- **Target:** Section 2 (challenge #2: "No plasma heating method specified"), Section 6 (Gap #1), and Section 3 (Plasma Confinement and Heating TRL 1)
- **Category:** analysis
- **Finding:** The analysis lists "No heating method specified" as blocking gap #1 (Section 6) and "truly-unknown" throughout. The full JTSP 2024 paper specifies that the prototype will use 5–10 kW microwave heating at 4 GHz electron cyclotron frequency (ECH). This establishes that ECH is the chosen approach for the prototype phase, and by extension is the likely near-term development direction for a commercial design. The gap is not fully closed — commercial heating power and integration are still unspecified — but characterizing the heating method as "truly-unknown" is no longer accurate. The distinction matters for TRL assessment: an ECH-based approach has a mature technology base (4 GHz microwave sources are commercially available), whereas an unspecified heating method cannot be assessed at all.
- **Recommendation:** Update Section 2 challenge #2 to reflect that ECH/microwave heating is the specified prototype approach (5–10 kW at 4 GHz), and reframe the remaining gap as "commercial-scale heating power and integration unspecified." Update Section 6 Gap #1 from "truly-unknown" to "partially known: ECH for prototype, commercial scale unspecified." Update Section 3 Plasma Confinement TRL to note that the heating approach (ECH) is established at prototype scale, which removes one unknown from the TRL-1 confinement assessment.
- **Priority:** important

### F-3: Prototype design complete — analysis incorrectly states "no prototype exists at any scale"
- **Target:** Section 3 (In-Vessel Dipole Coil with Magnetic Tunnel Supports — TRL 2) and Section 1 (Availability of Data)
- **Category:** analysis
- **Finding:** Section 3 states "No prototype exists at any scale" and the TRL 2 assessment is based on FEA analysis only. The full JTSP 2024 paper describes a fully specified prototype design: 30 cm diameter central cylinder, 1 m outer diameter, 90 cm height, 150 dm³ plasma volume, 960 m copper conductor, 2500 A maximum coil current, 750 kW ohmic losses, 304L steel vessel at 400 kg. Construction is described as imminent (1 year build time). This is a complete engineering design ready for fabrication — TRL 3 (experimental proof of concept) rather than TRL 2 (technology concept formulated). The analysis also includes prototype field strength (0.2–0.3 T) from the company profile, but attributes it as already-built hardware; it is actually the design target for the unbuilt prototype.
- **Recommendation:** Update Section 3 (In-Vessel Dipole Coil) to reflect that a fully detailed prototype design exists with specified dimensions, field strength, heating approach, and materials, with construction planned within ~1 year of the October 2024 report. Revise the TRL assessment from TRL 2 to TRL 2–3 (design complete, construction planned). Update Section 1 to note that the full JTSP paper contains prototype engineering specifications, not just abstract claims. Clarify in Section 5 that the 0.2–0.3 T field is the design target for a planned prototype, not an achieved result.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Analysis describes D-T scenario as a model gap, but model already includes it
- **Target:** Section 2 (Modeling Approach Rationale, proposition 3)
- **Category:** analysis
- **Finding:** The analysis explicitly states "This is a model-level gap: the current D-D-only model cannot address the central TEA tradeoff between Deutelio's two claimed operating modes." But the iter-3 model output already includes a full D-T vs D-D comparison across three scenarios. Because the analysis text was not updated to reflect this, the analysis fails to discuss the model's actual strategic finding: at equivalent scenario assumptions, D-T costs *more* than D-D (moderate: $1122 vs $946/MWh; optimistic: $277 vs $230/MWh). This reverses the usual assumption — the blanket cost penalty ($200–400M) exceeds any Q-threshold benefit when Q is held equal across fuel types. This is a meaningful conclusion that directly bears on Goal 3 (TEA implications of differentiators) and Goal 5 (risk framing), and it is currently absent from the analysis narrative.
- **Recommendation:** Remove the statement that D-T scenario comparison is a model gap. Add a paragraph in Section 2 discussing what the D-T comparison shows: at equivalent Q, D-T appears more expensive due to blanket cost, which implies that Deutelio's near-term D-T path (at "3× weaker field") does not automatically reduce cost relative to the D-D target — the field advantage claim must translate to higher Q, not just lower field, to yield a cost benefit. This should also be reflected in proposition 3, which currently frames the comparison as a future test rather than a completed finding.
- **Priority:** blocking

### F-2: Differentiator table omits cost implications; shield cost as dominant component not surfaced
- **Target:** Section 2 (Key Differentiators table and surrounding prose)
- **Category:** analysis
- **Finding:** The differentiator table classifies each row as Novel/Borrowed/Shared but does not state cost implications. Several differentiators have no stated cost impact anywhere in the analysis: (a) the large plasma volume (~3990 m³ in the model vs ~840 m³ for ITER) is noted but not called out as a direct cost penalty on shield, structure, and vacuum vessel; (b) steady-state operation is listed as "Shared (claimed)" with no cost implication; (c) remote handling is flagged as "more complex" but no cost magnitude is discussed. Most importantly, the model shows that shield cost ($804M, C220102) is the single largest reactor equipment component — exceeding the SC coil ($500M) and first wall ($247M) — driven directly by the large plasma volume. This is not surfaced in the analysis as a cost penalty of the dipole geometry (Goal 3: each key differentiator should have a stated cost implication).
- **Recommendation:** Add a "Cost Implication" column to the differentiator table with one of: advantage / penalty / neutral + brief reason. For the plasma volume / vacuum vessel / shield rows specifically, note that the large enclosed volume required for dipole confinement drives shield cost to ~$800M in the model — making it the dominant reactor equipment cost, not the SC coil. Add a sentence in the cross-concept notes or modeling rationale explaining that shield cost scaling with plasma volume is the primary geometric cost penalty of the dipole topology relative to tokamaks.
- **Priority:** important

### F-3: In-vessel coil maintenance challenge not connected to capacity factor sensitivity
- **Target:** Section 2 (Challenge 5: in-vessel coil maintenance) and Section 3 (O&M)
- **Category:** analysis
- **Finding:** The analysis identifies in-vessel coil maintenance as a severity-important challenge in Section 2 and notes it in Section 3, but never connects this to the capacity factor parameter in the model. The CF sensitivity sweep shows one of the largest LCOE swings in the model: CF=0.4 → 157 ¢/kWh vs CF=0.9 → 76 ¢/kWh — a 2× range. The in-vessel coil maintenance schedule (coil must be removed and replaced inside an activated, neutron-irradiated vessel through the magnetic tunnel geometry) is the primary driver of forced outage rate and therefore the primary lever on CF. Without this connection, a reader cannot identify which technical failure mode creates the highest LCOE risk. The analysis also uses CF=0.70 as the baseline without explaining why, given that the coil replacement challenge makes low CF a plausible scenario.
- **Recommendation:** In Section 2 Challenge 5 (or the O&M paragraph in Section 3), add an explicit statement connecting in-vessel coil maintenance to capacity factor risk: e.g., "If coil replacement requires extended vessel access (weeks to months per replacement cycle, analogous to major overhaul in levitated dipole designs), CF could plausibly fall to 0.4–0.5, which the model shows drives LCOE above 130 ¢/kWh — representing the primary downside scenario for this concept." The baseline CF=0.70 assumption should be flagged as optimistic given the unresolved maintenance scheme, and a CF=0.5 scenario should be noted as the lower bound until a maintenance design exists.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/35-polomac-magnetic-confinement/analysis.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/35-polomac-magnetic-confinement/iter-4/model_setup.py`
