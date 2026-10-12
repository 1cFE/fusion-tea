# Conductor-sizing narrative: proposal

Created: 2026-09-29

Status: [AGENT] Proposal for owner review; nothing implemented. It follows recommended option A in [evaluation.md](evaluation.md#options-and-recommendation):
- Keep a narrowed conversion comparison as the component example.
- Give conductor sizing more room where it fits: the main post's model-execution section, Part 2 §2.7.1, and the conclusion callback.

All drafts below are editable. Numbers are from the sealed 15 September record unless marked **[replay]**. Those come from the 4-case current-model evaluation in `replay/`, which is not yet a sealed study. Use them only after it is promoted.

## 0. What changes, at a glance

| Place | Change | New evidence needed |
|---|---|---|
| Main post §2 | Add one conductor-sizing paragraph (1a) | None (version 1); sealed replay (version 2) |
| Main post Q2 | Narrow the conversion paragraph, drop its figure (1b) | None |
| Main post conclusion | Magnet callback (1c), answering item 7 | None |
| Part 2 §2.7.1 | Reframe as supplied designer choices; add “what each limit is measured against” (2) | None; optional refrigerator row needs the sealed replay |
| Part 2 §2.7.2 | One-sentence note on the sizing option | None |
| Part 4b §4.2 | Narrow the question and wording; keep figures (3) | None |

## 1. Main post

### 1a. Conductor-sizing paragraph in §2

Place it after the “Feasibility through constraints” bullet (`archive/write-up/main-post-draft.md:70`), before the Part 2 link. It shows what “the model pushes back” means, which is the reviewer's point of interest.

Version 1 uses only the historical record. Today's model reproduces all of these magnet quantities exactly.

> **An example of the model pushing back.** Our model of the Stellaris magnet started out short of conductor. With the tape performance we assumed, the published winding would run its superconducting tape at about 170% of its estimated capacity, where we allow 80%. Supplying about 2.1 times as much tape fixes that check, but the bigger winding no longer fits the space allocated for it. Making more room changes the coil geometry, and the calculated peak field on the conductor rises from 24.9 to 25.3 T, above the published design value we hold as the ceiling. Each fix changed something another check depends on. None of this says the real Stellaris magnet is short of conductor: the result rests on our tape assumptions, a simplified field calculation and the space we assumed. What it shows is the model carrying a local change through to every limit that depends on it.

Version 2 needs the sealed replay. Replace the second sentence's ending with:

> …but the bigger winding no longer fits the space allocated for it, and its extra cold mass is more than the refrigerator chosen for the original magnet can handle.

Checks on the wording:
- “About 170%” is operating fraction 1.687 (C5).
- “2.1 times” is the tape ratio 2.129 (C6).
- 24.9 → 25.3 T is C10/C11.
- The paragraph never says the model sized anything. It also quotes no LCOE, which avoids the stale September cost scope.

Optional figure: re-render `archive/write-up/sysml-codegen-assets/stellarator-magnet-tradeoff.png` with the spec in §2 (cards without LCOE). Otherwise link to Part 2 Figure 10.

### 1b. Component study in Q2, narrowed

This replaces `main-post-draft.md:165-169`. Drop the figure and caption and keep the full comparison in Part 4b. The reviewer's objection to “Brayton is cheaper but produces less electricity” is met by defining cost per kW.

> **Components: steam vs helium Brayton.** We put steam and helium Brayton conversion, each with its own exchangers and cooling equipment, on the same Stellaris-derived reactor. That reactor delivers helium at 500 °C, which suits steam: the Brayton turbine inlet reaches only about 413 °C, against 708 °C in ARIES, so its compressors take most of the turbine's output. Steam exported more than twice as much electricity and gave the lower cost per MWh. Per kilowatt of output, the two conversion systems cost about the same; Brayton's smaller bill reflects its smaller output. This is a result for this heat source, not a ranking of the two cycles.

Evidence:
- 413 °C, 708 °C and the compressor share are from the current Part 4b §4.2.
- Per net kW: steam $2.548B / 937.579 MW ≈ $2,720/kW; Brayton $1.541B / 559.493 MW ≈ $2,750/kW ([component answer](../../../../work/orchestration/goals/design-study-component-alternatives/answer.md):9,15).

If the owner follows the reviewer fully, a one-line pointer can replace the paragraph instead: “A component comparison, steam against helium Brayton conversion on this reactor's 500 °C helium, is in Part 4b with the conditions that decide it.” Line 157 (“one study for each of the three types”) then needs “two of them here; the third is in Part 4b.”

### 1c. Conclusion callback (item 7)

This replaces the list in `main-post-draft.md:183`:

> I wouldn't make a design decision from any of these study outcomes. What I would take from them is that the model points at the right *kinds* of questions: a magnet whose fix for current capacity broke its fit and field limits, a compressor setting limited by an exchanger elsewhere in the plant, a pressure-loss budget that decides a layout. That's the feedback we were after.

Avoid “magnet optimization”: no optimum was searched for or found.

## 2. Part 2 §2.7.1: the supporting magnet narrative

This keeps the section's place and three cases, and removes the conflict with Part 4b §2.

**Study question.** What happens if a designer adds enough tape to carry the current, then makes room for it?

**Opening paragraphs** (replace the first paragraph of §2.7.1):

> With the tape performance we assume, the published Stellaris winding cannot carry its current: the tape would run at about 1.7 times its estimated critical current, where we allow 0.8. The winding also does not fit the radial space our model allocates for it. What happens if a designer adds enough tape to carry the current, then makes room for it?
>
> The three cases below come from the 15 September joint magnet-sizing study. That study let the model choose the amount of tape from the current requirement. We later removed that option, because it takes the choice away from the designer ([Part 4b, section 2](part-4b-aries-test.html#2-one-false-start-before-the-main-assessment)). The model now evaluates the winding a designer supplies and reports any shortfall. Supplied to today's model, the same three windings give the same tape, fit and field results.

The last sentence rests on the replay. Cite the sealed record once promoted. Until then, cite this investigation or drop the sentence.

**Sequence** (Figure 10 cards, relabeled):

1. **Published winding.** 0.36 m winding; 0.30 m radial, 0.40 m transverse space. Current FAIL, fit FAIL (−0.120 m radial), field PASS (24.90 T), divertor FAIL.
2. Change 1: **add tape**, about 2.1× as much, enough for the current plus 1% spare. “Fixes the current check. The winding grows from 0.36 to 0.53 m across, so it fits even less. Magnet subtotal +$0.84 billion.”
3. **More tape.** Current PASS, fit FAIL (−0.285 m radial, −0.148 m transverse), field PASS, divertor FAIL.
4. Change 2: **make more room**, 0.60 m radial and 0.60 m transverse. “Fixes the fit. The thicker coils sit farther from the plasma, which on the inner side of the torus brings neighbouring coils closer together; the calculated peak field rises from 24.90 to 25.30 T, above the 24.9 T ceiling.”
5. **More tape and more room.** Current PASS, fit PASS (+0.012 / +0.049 m), field FAIL (25.30 T), divertor FAIL.

**Central comparison.** The three verdict rows (current, fit, field) side by side, with tape length and magnet subtotal. Drop LCOE from the cards: it reflects the September cost scope and roughly doubles under today's accounts. The record block can state it with that label.

**Takeaway** (replaces the two closing paragraphs):

> Each fix changes something another check depends on. More tape makes a bigger winding; room for it changes the coil geometry that sets the field. The model carries a local change to every limit that depends on it. Whether a real magnet has the same problem depends on what each limit is measured against.

**Limitations, as a compact table** (new; a short collapsed “In the record” block is enough):

| Check | Passes when | What the limit rests on |
|---|---|---|
| Conductor current | Tape runs at ≤ 80% of its estimated critical current | A 20 K REBCO law: 200 A per 4 mm tape at 20 T, inferred from a supplier figure, scaled as field^−0.6 and extrapolated above 24 T. Adding tape raises capacity; tape performance is unchanged. |
| Winding fit | Winding, insulation and clearance fit inside the casing | Space allocations are our assumptions. The published winding already exceeds the 0.30 m radial allocation. Extra transverse space carries no casing mass or cost in the model. |
| Peak field | ≤ 24.9 T | Stellaris's published peak field, held as a ceiling. The model is calibrated to reproduce it exactly, so the published design has zero margin and any rise fails. The field responds only to coil position. The source equation's winding-size term, which would lower the field for a larger winding, is not modeled, so the direction of the real change is not established. |
| Divertor heat | ≤ 10 MW/m² | Fails in all three cases, independent of the magnet change; none is a feasible plant. |
| Refrigerator capacity **[replay]** | Cold load within the supplied cryoplant | Supplied at exactly the published winding's load. The larger winding exceeds it by 5.6 kW at the cold stage and 0.9 kW at the intercept. |

Caption for revised Figure 10:

> Three windings evaluated with the same program: as published, with about 2.1× the tape, and with that tape and more space. Adding tape fixes the current check but not the fit; making room fixes the fit but raises the calculated peak field above the published design value. All three exceed the divertor heat-load limit. Values from the 15 September study; today's model gives the same magnet results for the same supplied windings. Data: archive/write-up/sysml-codegen-assets/magnet-sizing-comparison.csv.

**§2.7.2 note** (after the held-inputs table):

> This map also ran with the since-removed tape-sizing option on. Its passing samples reflect that snapshot's checks and costs.

### Figures and data

| Figure | Why it earns space | Data / units / legend | Status |
|---|---|---|---|
| Revised Figure 10 cards (reuse `page-fit-case-*.svg`) | The three-step consequence is the section's point | `magnet-sizing-comparison.csv`: tape length (million m), magnet subtotal ($ billion, mixed price bases), margins (m), field (T); PASS/FAIL per check | Existing evidence; relabel only |
| “What each limit rests on” table | Stops the reader taking a model ceiling for a physical limit | Text; cites `stellarator_plant.sysml:431-437`, `mfe_conductor_current.sysml:5`, `mfe_plasma_scaling.sysml:420-447` | Existing evidence |
| Main-post card figure (re-render `stellarator-magnet-tradeoff`) | A visual for the new main-post paragraph | Same CSV. Headline tape multiple ×1 / ×2.13 / ×2.25 instead of LCOE; labels “Published winding”, “Add tape”, “Add tape and room” | Existing evidence; renderer `archive/write-up/sysml-codegen-assets/render_figures.py` |
| Refrigerator row on cards | Shows the MR-7 pattern: supplied equipment, capacity check | `data/replay-supplied-windings.csv`: cold/intercept margin (W) | **Needs sealed replay** |
| Field-geometry sketch (optional) | Explains why more room raises the field | Coil-centre radius 3.15 → 3.30 m, inboard clearance 9.55 → 9.40 m, bore factor 1.016 (native `rb__r_coil_centre`) | Evidence exists; sketch not drawn. Must state the omitted winding-size term |

## 3. Part 4b §4.2, narrowed (items 5–6)

This is a bounded sketch. Items 5–6 remain owner decisions, and the tracker holds the reviewer's concerns.

**Question** (replace the section's first sentence): “For this reactor's 500 °C helium, which conversion system exports more electricity and at what cost per MWh?”

**Add after the source description:**

> That temperature favours steam. A helium Brayton cycle needs a hot turbine inlet to keep its compressors from consuming most of the turbine's work; ARIES runs its turbine at about 708 °C. We did not test a hotter reactor, so this compares the two cycles on this source, not the cycles in general.

**Replace “Steam's conversion equipment cost $2.55 billion, against $1.54 billion for Brayton… The cheaper conversion equipment produced the more expensive electricity.”** with:

> Steam's conversion equipment cost $2.55 billion, against $1.54 billion for Brayton. Per kilowatt of net output the two are close: about $2,720 for steam and $2,750 for Brayton. Brayton's total is lower because its output is lower. Both plants also needed the same $10.23 billion of other purchases, and steam spread those common costs over more than twice as many MWh.

**Add to the heating/loads paragraph:**

> Both plants carry 274 MW of reactor-side electrical load, including 100 MW to supply 50 MW of steady plasma heating. That heating is a held assumption; this study does not test whether the plasma's operating regime needs it. Removing it would raise both outputs by the same amount and narrow the cost gap without reversing the ranking.

The ranking claim is an [AGENT] scaling estimate from the published outputs (764 vs 386 MW net). It should be checked before publication or dropped.

**Section 4.4 bullet:** “Components: on this reactor's 500 °C helium, steam exports more than twice the electricity of the tested Brayton designs; the equipment-only view hid that difference.”

**Optional bridge to the magnet story** (in “The reactor held fixed”):

> Its magnets are a reworked supplied design: a larger winding at 48 kA per turn, with a larger refrigerator, chosen so the magnet's own current, fit and refrigeration checks pass (Part 2, section 2.7.1 shows why the published winding needed rework).

Evidence: [48 kA capture](../../../../work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-capture/report.md). That design relies on 1.30 m of transverse space, which the model does not cost, so say so if the bridge is used.

## 4. Decisions for the owner

1. **Route:** A (recommended), B (drop the component study) or C (commission a magnet material study). D is not recommended. See [evaluation](evaluation.md#options-and-recommendation).
2. **Main-post conversion paragraph:** the narrowed version (1b) or a one-line pointer.
3. **Refrigerator step:** leave it out, or promote the replay to a sealed study so the pages can quote it.
4. **Part 2 reframing:** accept the MR-7 note and relabeled cards. This fixes an existing inconsistency whatever route is chosen.
