# Magnet study as a replacement for the component-choice example: evaluation

Created: 2026-09-29

Status: Investigation complete; recommendation for owner decision. No article, supporting HTML, model, study or acceptance limit was changed. Item 5–7 decisions remain open in the [feedback tracker](../feedback-resolution.md).

[OWNER-VERBATIM] “I want to make sure it actually meets the intent for this category of ‘study’ before committing to it (as well as making sure the numbers and details hold up)”

The companion [narrative proposal](narrative-proposal.md) drafts the prose and figures for the recommended route.

## Verdict

[AGENT] **The magnet study does not fit the component/material category, and no other existing magnet study does.** Its numbers reproduce exactly, and its physical sequence survives the later design-choice repair, but it is a parameter-and-constraint story. It belongs where it already sits (Part 2 §2.7.1), not in Part 4b's component slot.

The unresolved material issues, most important first:

1. **Category mismatch.** Every case uses the same REBCO tape at 20 K. What changes is how much tape, how much space and, in the original study, which calculation policy chose the tape. None is an alternative component or material definition.
2. **Premise conflict with the page it would join.** The 15 September study's central mechanism is the automatic sizing that Part 4b §2 describes removing on 20 September, and that MR-7 names as its example of a hidden design-selection rule. Placing it in Part 4b §4.2 would contradict §2 on the same page. Part 2 §2.7.1 already carries a milder version of this conflict (see [Chronology](#chronology-and-the-mr-7-conflict)).
3. **The “limits” it exposes are the old design's own values.** The 24.9 T field ceiling is Stellaris's published peak field, and the model was calibrated so the reference sits exactly on it. Under today's model, the cryoplant and building checks the larger winding also fails start at exactly zero margin. Any change that raises demand fails them by construction.
4. **The field step's sign is not established.** The field calculation keeps only a coil-position factor. It omits the winding-size term of its source equation, which pushes the other way. If that term carries more than about 5% of the field's configuration term, the enlarged design would sit below the 24.9 T reference field, not above it.
5. **Duplication.** Part 2 §2.7.1 already presents the same three cases, figures and conclusion.

[AGENT] Recommendation: keep a narrowed conversion comparison as the component example (fixing items 5–6), and give the conductor-sizing story more room where it fits. That means the main post's model-execution section, a revised Part 2 §2.7.1, and the item-7 callback. A genuine magnet material comparison is possible but needs a new conductor model. See [Options](#options-and-recommendation).

## 1. What the component category promises

The promise appears in four places, and they agree:

- **Part 2 §1.1** (`docs/exploratory-modeling/part-2-model-execution.html:366-397`): component and material choices “are categorical: we select one alternative or another… an alternative may bring different properties, equations, and engineering limits… We can create alternative definitions and select which one a design uses.”
- **Main post** (`archive/write-up/main-post-draft.md:45,68`): “We can vary categorical decisions (Material A vs B, Component C vs D)” and “swap one component model for another and compare them, A/B.”
- **Part 4b §1 and §4** (`part-4b-aries-test.html:201-215,1374-1386`): Question 2 asks whether the *combined* Stellaris/ARIES library can explore designs neither plant covers, with “one study for each kind of design change… a component choice.”
- **The original goal** ([component-alternatives goal](../../../../work/orchestration/goals/design-study-component-alternatives/goal.md)): matched alternatives on the same source, explicit offered equipment for both branches, “No automatic resizing or demand-derived purchases” (MR-7), and failures preserved.

[AGENT] From these, a component example must pass five tests. The engineering acceptance bar of the conversion goal is not inherited; only its editorial promise and MR-7 invariant are.

| Test | What it means |
|---|---|
| T1 Categorical | The alternatives are different component or material definitions with their own properties, equations or limits. |
| T2 Matched | Both are evaluated on the same held design and compared on the same basis. |
| T3 Designer choice | Each alternative is a supplied design evaluated as given (MR-7), not a sizing policy's output. |
| T4 Part 4b fit | It uses the combined library to answer Question 2, after the reveal and repair. |
| T5 New to the reader | It shows something Part 2 has not already shown. |

## 2. Which study the reviewer meant

[INHERITED: reviewer, via owner] “The magnet study you linked to seemed interesting - you could possibly take out the power conversion bit and instead talk more about the conductor sizing?” Item 7 separately asks for a callback to “the magnet optimization.”

[AGENT] The main post links to Part 2 as the walkthrough “from one magnet equation to a map of which designs pass” (`main-post-draft.md:73`). Part 2 holds two magnet studies:

- **§2.7.1, 15 September joint magnet sizing.** This is “conductor sizing” literally: size the tape for the current, then find room for it. It is the most likely referent.
- **§2.7.2, 17 September radius–current map.** This is the closest thing to “magnet optimization” (a feasible band with costs). It also ran with current-driven sizing on (`part-2-model-execution.html`, “Held inputs for the map”: multiplier 1.01).

The exact referent cannot be confirmed without asking the reviewer. Both studies share the same pre-repair sizing and are Stellaris-only. Neither is an optimization: the study runner evaluates grids and lists, with no adaptive search. The evaluation below uses §2.7.1 and notes where §2.7.2 differs.

## 3. Category fit of the joint-sizing study

Source: [answer](../../../../work/orchestration/goals/joint-magnet-sizing-feasibility/answer.md), [report](../../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/report.md), native results.

| Aspect | Joint-sizing study, 15 September |
|---|---|
| Question | [OWNER-VERBATIM] “Can a magnet carry the required current at the selected operating margin, fit inside an explicitly allocated casing, and satisfy the existing plant constraints under one consistent set of construction and performance assumptions?” |
| Alternatives | Entering inventory (mode 0) versus current-sized inventory (mode 1, `sizing_mode` flag), then a larger casing allocation. Also R, a, ampere-turns and allocation over a 324-case grid. |
| What changes in the model | A numeric mode flag inside one definition (`models/library/analyses/mfe_conductor_current.sysml:39-45`), plus input values. There is no alternative part or material definition. |
| Held | REBCO tape, 6 mm × 56 µm, 20 K; 50 kA per turn; 0.8 allowable fraction; 9% tape fraction; square pack; 24.9 T ceiling. |
| Compared | Current, fit and field verdicts; tape, magnet subtotal, LCOE; all 20 predicates. |
| “Material” sensitivities | Material 1.10/1.35, orientation 2 and retention 0.9³ are numeric multipliers on the same tape law, not alternative materials. |

Against the tests:

- **T1 fails.** One conductor definition throughout. The only categorical-looking switch is a calculation policy, and the owner rejected that policy five days later.
- **T2 partly passes.** The cases share assumptions, but the comparison is a sequence of changes to one design.
- **T3 fails as recorded.** Installed tapes = required × 1.01 is MR-7's own example of an automatic selection rule (`capacity = required * margin`, bound as installed). The replay below shows the same windings can be evaluated as supplied designs, so this is repairable in the telling.
- **T4 fails.** It is Stellaris-only and ran before the ARIES library, the reveal and the repair. It does not address Question 2.
- **T5 fails.** Part 2 §2.7.1 already shows all three cases (Figure 10) with the same takeaway.

[AGENT] This is a parameter study plus a model-capability change. Relabeling it would present an ordinary sizing sequence as a categorical comparison, which the owner asked us not to do.

## 4. Other magnet studies

[AGENT] Surveyed and spot-checked. None is a genuine categorical comparison. There is no Nb3Sn or 4 K conductor definition anywhere in `models/`. (Superseded 2026-09-30: WI-099, commit 2869c34aa, added Nb₃Sn and REBCO conductor definitions in `models/library/analyses/magnet_conductor_alternatives.sysml`; not wired into the plant model.)

| Study (date) | What differed | Categorical? | Status |
|---|---|---|---|
| `20260823-magnet-technology-ab` | Owner asked for “REBCO vs Nb3Sn”. Implemented as four input values in one package: cost per kA·m (50/7), temperature (20/4.5 K), field ceiling (24.9/13 T), cold volume (136.56/390 m³) (`study.py:44-48`). | Question yes, implementation no | Ran before field, current-law, fit and sizing work. On-axis field input since retired; “not reproducible as written” (`work/orchestration/goals/magnet-closure/trail.md:403`). |
| `magnet-design-transfer` (09-13) | Field envelope 20–30 T for one REBCO construction | No | Grade calculation removed by the repair |
| `magnet-coil-realism`, `tape-procurement-consistency`, `winding-pack-casing-fit`, `absolute-conductor-current-margin`, `magnet-manufacturing-cost-completeness` (09-14/15) | Repairs and added checks | No | Current |
| WI-057 swap demonstration (09-13) | A real alternative definition, `'NI HTS Magnet System' :> 'Magnet System'`, selected by retyping | Mechanism yes, content no | Unsourced stand-in formula in a scratch prototype, not in `models/` |
| ARIES post-reveal | Magnets priced as supplied-mass purchases; no conductor model added | No | The ARIES conductor gap is still open (`main-post-draft.md:151`) |

The magnet A/B study is the only one that asked a categorical question. It answered with four numbers, predates all the conductor physics now in the model, and cannot be replayed on the current package. It cannot stand in for the category.

## 5. Chronology and the MR-7 conflict

| Date | Event | Evidence |
|---|---|---|
| 15 Sep | Joint-sizing study adds optional current-driven sizing. Hypothesis H2: “current sizing belongs inside the model.” Supported. | [report.md](../../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/report.md) “Hypotheses” |
| 17 Sep | Radius–current map runs with current-driven sizing on | Part 2 §2.7.2 held inputs |
| 20 Sep | ARIES false start fails in the sizing node (`current_sizing`, mode 1) at 56.6 T | `git show 829539f5:.project/active/aries-comparison-preparation/current-readiness/revealed-results/c3/native-store-inspection.json` |
| 20 Sep | [OWNER-VERBATIM] “As soon as you start introducing ‘sizing’, then you are basically pre-defining which design parameters are ‘free’ and which are ‘derived’. this is explicitly what we wanted to avoid.” MR-7 adopted. | `modeling_project/REQUIREMENTS.md` MR-7 |
| 20 Sep | Repair (WI-075): pack side, turns, support and casing masses become supplied; `current_sizing`, `wp_sizing`, `conductor_grade`, `sizing_mode`, `inventory_multiplier` and `j_wp` leave the evaluation graph. The repair inventory marks *both* old modes “Violated”. | [binding plan](../../../../work/orchestration/goals/preserve-model-design-choices/evidence/magnet-binding-plan.md), [inventory](../../../../work/orchestration/goals/preserve-model-design-choices/evidence/magnet-inventory.md):5-7; current `pipeline.yaml` has 0 matches |
| 26–27 Sep | Part 4b studies on the combined, repaired library. The component study's reactor uses a reworked supplied magnet: 0.54 m pack, 1.30 m transverse cavity, 48 kA, 40/60 kW cryoplant. | [48 kA capture](../../../../work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-capture/report.md) |

What stays valid:

- **The physical sequence.** Supplied to today's model as designer choices, the three windings reproduce every magnet quantity exactly: tapes, fit margins, field, tape length, stored energy. The magnet subtotal differs only in the enlarged case (−0.6%, support mass now supplied) ([comparison](data/sept15-vs-replay.csv)).
- **The lesson.** A local change propagates through geometry into other checks.

What cannot represent current design evaluation:

- The framing “the model sized the conductor for the current.” That option was removed.
- The costs and LCOE. The same windings now give $318.74, $340.71 and $344.53/MWh against $144.75, $163.19 and $166.74 in September, because of later breeding, cooling and facility cost work.
- The claim that nothing else breaks. Today's model adds checks that the larger winding fails (next section).

[AGENT] Premise conflict, surfaced rather than resolved: Part 2 §2.7.1 presents “Size the conductor supply for the required current” as an ordinary design change, and §2.7.2 lists “current-driven sizing on” as a held input. Part 4b §2 presents removing such sizing as a repair. A careful reader of both pages can fairly ask which pattern the model follows. Expanding the magnet story without addressing this would amplify it. A small fix is drafted in the narrative proposal. It keeps the historical study and says the same windings are now supplied, with the same results.

## 6. Do the numbers and physics hold up?

[AGENT] Full table: [claim-evidence.csv](data/claim-evidence.csv). Scripts: [extract_joint_sizing.py](extract_joint_sizing.py) (reads the sealed record), [replay_supplied_windings.py](replay_supplied_windings.py) (current model), [compare_replay.py](compare_replay.py).

**Arithmetic: reproduced exactly.**

- Tape current 263.039 A = 200 A × (6/4) × (24.9/20)^−0.6.
- Required tapes 237.608 = 50,000 / (0.8 × 263.039). Installed 239.984 = 1.01 × required. Entering 112.709.
- Pack side 0.525 m, fit margins and densities match to 2e−16.
- Field 25.2973 T = 24.9 × (12.7 − 3.15)/(12.7 − 3.30). The coil-centre radius moves out by half the added 0.30 m.
- 0 of 324 default cases pass all 20 checks, recounted from raw verdicts with an independent cohort rule that matches all 324 flagged cases. Divertor fails 247, loop capacity 232, burn hold 190, fit 170, field 157.
- Snapshot SHA-256 matches the answer (`330e0ac2…`).
- A constant $6.32B “magnet cost” channel in the native store is an unconsumed 1costingFE comparison export. LCOE reads the priced rollup (`pipeline.yaml:1108`).

**Physical interpretation: conditional, with five qualifications the prose must carry.**

1. **More tape, not better tape.** Current capacity rises only by buying about 2.13× the tape at unchanged per-tape performance. Conductor length is unchanged. The material, orientation and retention scenarios are hypothetical multipliers, not demonstrated gains.
2. **“The reference can't carry its current” is a disagreement with the published design, not a finding about Stellaris.** The entering 118.8 A/mm² is Stellaris's published worst-coil density (Table 8). The shortfall follows from our assumptions: a 200 A per 4 mm tape inferred from 175 A × 1.13 (not a measured product), 9% tape fraction, 0.8 allowable fraction, and a law extrapolated above 24 T (native flag set at the reference).
3. **The fit failure starts before any change.** The entering model's 0.30 m radial allocation cannot hold Stellaris's own 0.36 m pack (margin −0.120 m). The allocation is an assumption, not a sourced space limit.
4. **The field ceiling is the published design value, with zero margin by construction.** `B_max = 24.9` is “Stellaris design envelope retained… not a certified critical-field or absolute operating-margin test” (`stellarator_plant.sysml:431-437`). The anchor ratio was written so the reference reads exactly 24.9 T (`:234-246`); the margin is 3.6e−15 T. After resizing, the conductor still carries its current at 25.30 T. Under today's supplied framing, the unchanged winding keeps only 23 A of margin at 25.30 T.
5. **Only the bore factor responds.** The source equation (Lion 2021 eq. 39) has a winding-pack term, R·a1/√A_wp, that the model omits because its coefficient is unprinted (`mfe_plasma_scaling.sysml:420-447`). The pack area grows from 0.130 to 0.279 m², which shrinks that term by 32%. If it is ≥4.9% of the configuration term at the reference, the enlarged design's net field ends below the reference. The model cannot say which way the real field moves.

Also carried: all three cases fail the divertor heat limit, so none is a feasible plant; magnet costs have mixed price bases and unpriced manufacturing; transverse space carries no casing mass, thermal or cost response.

**What the current model adds (targeted replay, 4 cases, [summary](replay/summary.json), [CSV](data/replay-supplied-windings.csv)).** Package fingerprint `83ea3b6c…`; 530 protected model/package files unchanged ([preservation](replay/preservation.json)). This is a development evaluation, not a sealed or independently reviewed study.

| Supplied design | Current | Fit | Field | Cryoplant cold / intercept | Building | LCOE |
|---|---|---|---|---|---|---|
| Published winding, 0.36 m, 0.30/0.40 m space | fail (op. fraction 1.69) | fail (−0.120 m) | 24.90 T pass | 0 / 0 W margin | 0 m margin | $318.74 |
| 2.13× tape, 0.525 m side, same space | pass (+500 A) | fail (−0.285 m) | 24.90 T pass | **fail** (−5,553 / −873 W) | pass | $340.71 |
| Same winding, 0.60/0.60 m space | pass (+23 A) | pass (+0.015 m) | **25.30 T fail** | fail (−6,061 / −1,056 W) | **fail** (−0.6 m) | $344.12 |

[AGENT] Under the current model, the larger winding's extra cold mass (136.6 → 290.8 m³) also exceeds the refrigerator chosen for the original magnet. The enlarged coils then exceed the building. Both capacities sit at exactly zero margin for the published winding: they equal the original design's demand. These are genuine evaluations of fixed equipment, which is what MR-7 intends. But the honest wording is “equipment chosen for the old magnet is too small”, not “a physical limit was reached.” The WI-098 48 kA capture shows the designer's next move: lower the current to 48 kA (23.9 T, no extrapolation) and buy a 40/60 kW cryoplant. The local magnet checks then pass, but the plasma operating point changes and other plant checks fail. It also uses a flat 0.19-aspect pack in a 1.30 m transverse cavity. That relies on the unmodeled transverse casing response, so it should not headline without that limit stated.

## Options and recommendation

The decision: what stands in Part 4b's component slot, and where the conductor-sizing story goes. Four options:

**A. Keep a narrowed conversion comparison in §4.2; expand conductor sizing where it fits.** [AGENT recommended]
- Covers items 5–6 with wording: a fixed 500 °C source that favours steam, “cheaper” defined per kW, and the assumed heating load.
- Moves the reviewer-suggested expansion to the main post's model-execution section, with a corrected Part 2 §2.7.1 and the item-7 callback.
- Cost: editorial; the figures largely exist. It keeps the only genuinely categorical, sealed and verified example, and it resolves the MR-7 conflict.
- Risk: the reviewer suggested dropping conversion. The narrowed claim (steam suits a 500 °C source) is unsurprising to specialists. The section's value becomes the mechanism and the whole-plant accounting lesson, not a technology insight.

**B. Drop the component study from the main post and Part 4b.**
- Say plainly that only two of three kinds were demonstrated on the combined library, and point to Part 2 §2.5 for the component mechanism.
- Cost: editorial, plus edits to Figure 1, the §4 table, §4.4 and §5. It honestly weakens the “one study per kind” claim.

**C. Commission a genuine magnet material study** (REBCO at 20 K against Nb3Sn at about 4 K as alternative definitions).
- Needs a sourced Nb3Sn critical-current law in field, temperature and strain; 4 K refrigeration; conductor pricing; and a swap seam for the conductor law. The current law's outputs are bound with `=`, and the 20 K check refuses other temperatures.
- The design point is also a problem. Nb3Sn cannot reach Stellaris's 24.9 T, so a fair comparison needs a lower-field, larger design (a coupled redesign), and the field model does not transfer to ARIES geometry.
- This is a major new physical model: a multi-round goal. It is disproportionate to the write-up.

**D. Place the joint-sizing study in §4.2 as proposed.** [AGENT not recommended] It fails T1, T3 (as recorded), T4 and T5, and it contradicts Part 4b §2.

[AGENT] I recommend A. It keeps the category promise with the one example that meets it, and it gives the reviewer's interest in conductor sizing more room where it is true to the evidence.

Supporting work under A:
- **Required: none.** The narrative can use the historical record's magnet quantities, which the current model reproduces exactly.
- **Optional, small:** promote the 4-case replay to a sealed study record with independent verification. This is needed only if the page should quote current-model consequences (cryoplant and building failures, current-scope LCOE). Estimate: one short native study run and review.
- **Optional, larger:** the transverse-casing response and the omitted field term. These are model repairs, not write-up work.

## Impact on neighbouring material

| Location | Under A | Under B | Under D |
|---|---|---|---|
| Main post Q2 (`main-post-draft.md:157,165-169`), figure `post-images/steam-vs-brayton.png` | Shorten to the narrowed claim or a one-line pointer; keep or drop the figure (renderer `archive/write-up/main-post-assets/render_figures.py:71`) | Remove paragraph and figure; change “one study for each of the three types” | Replace paragraph and figure |
| Main post §2 (`:68-73`) | Add the conductor-sizing paragraph | Same | — |
| Main post conclusion (`:183`) | Magnet callback added; conversion phrase narrowed or dropped | Magnet callback replaces conversion | Callback |
| Part 4b §4.2 (`part-4b-aries-test.html:2771-4773`, Figures 8–10) | Narrowed prose; figures kept with corrected captions | Remove; renumber Figures 11–12 | Replace |
| Part 4b Figure 1, §4 table, §4.4, §5 (`:211, 1383-1384, 5236-5246, 5248+`) | Wording only | Edit all four | Edit all four; §4 fuel paragraph changes |
| Part 2 §2.7.1 (Figure 10, `magnet-sizing-comparison.csv`, `page-fit-case-*.svg`) | MR-7 note; relabel Change 1; optional current-model row | Same | Duplicated in Part 4b |
| Part 2 §2.7.2 held inputs | One-line note that sizing was later removed | Same | Same |
