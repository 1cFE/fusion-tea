# Free-Form Model Update: Levitated Dipole (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/iter-4/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/iter-4/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: "No divertor" advantage stated but not closed as a TEA hypothesis
- **Target:** Section 7 (Cross-Concept Notes) and Section 5 (Missing Parameters)
- **Finding:** The analysis correctly identifies "no disruptions → no divertor component replacement schedule" as a cost advantage over inductive tokamaks (Goal 3), but stops short of completing the argument. A levitated dipole with no divertor must handle particle exhaust somewhere — the outer vessel wall is the effective exhaust surface. The consequence for TEA is ambiguous: if steady-state edge heat flux falls on the first wall rather than a dedicated divertor, first wall thermal load and replacement frequency become cost-relevant items. The analysis lists "first wall thermal load and material choice" as a data gap (Sections 5 and 6) without connecting it to the "no divertor" narrative. As written, the advantage claim is structurally incomplete: it identifies the cost avoided (divertor scheduled replacement) but does not address what, if anything, takes on that function — or bound the scenario in which the first wall itself becomes a significant scheduled replacement item that offsets part of the claimed advantage.
- **Recommendation:** Add a paragraph in Section 7 (or Section 2) that closes this loop: explain that a levitated dipole has no dedicated divertor geometry, that particle exhaust falls on the outer wall, and frame the TEA implication as a testable hypothesis — if steady-state first-wall heat flux is lower than divertor heat flux in a comparable tokamak, the "no divertor" advantage is real; if wall loading is comparable, the advantage shrinks or disappears. This turns an incomplete assertion into a testable proposition consistent with Goal 5.
- **Priority:** important

### F-2: ICRH coupling failure mode not stated as a testable proposition
- **Target:** Section 2 (Key Hypotheses) and Section 3 (ICRH subsystem)
- **Finding:** The analysis identifies ICRH coupling in dipole geometry as a challenge (Sections 2, 3) and a data gap (Section 6, gap #5: "truly-unknown, important"). However, unlike the three key hypotheses at the end of Section 2, the ICRH bet is not stated with an explicit failure-mode consequence (Goal 5). The ICRH efficiency assumption (70% wall-plug) is a meaningful TEA lever: ICRH at 70% vs. fallback ECRH at ~50–55% changes wall-plug heating power by ~25%, raising recirculating power fraction and lowering net electrical output. If ICRH coupling in dipole geometry fails, this is a continuous cost penalty with a quantifiable LCOE impact — not a binary viability threshold like the confinement scaling bet — but the analysis currently leaves the consequence implicit.
- **Recommendation:** Add one sentence to the Key Hypotheses block in Section 2 stating the failure-mode consequence: if ICRH coupling in dipole geometry is unachievable and the design falls back to ECRH (~50% wall-plug efficiency), heating wall-plug power rises by approximately X MW, increasing recirculating fraction by Y% and elevating LCOE proportionally. This makes the bet explicit and testable, consistent with how the confinement scaling and coil replacement cost hypotheses are treated.
- **Priority:** minor


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/analysis.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/iter-4/model_setup.py`
