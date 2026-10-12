# Support pages: audit against the revised main post

Created 2026-09-30. Four read-only audits, one per page, run after the main post's Part 4 and Part 5 revisions. [AGENT] throughout: findings and proposed wording are agent output, checked against the post (`archive/write-up/main-post-draft.md`), the ratified decisions in [feedback-resolution.md](feedback-resolution.md), and the cited records. Nothing on the pages was edited. Proposed wording follows [writing-prompt.md](../../../archive/write-up/writing-prompt.md); the owner may reword.

Severity: **must** contradicts the post or a ratified decision; **should** stale or misleading; **optional** as marked.

**Applied 2026-09-30** by four Opus agents, one per page, on the owner's instruction to apply all of the above while keeping voice, flow and logic. Every must and should item is in; optionals as noted per page. Verified after application: no rejected phrasing remains on any page (grep for each), every in-page anchor resolves, each page loads with zero console messages and zero page errors, and Part 4a's suite passes (38). Diff: 8 files, +68/−58; the main post was not touched. Wording adjustments from the proposals are recorded in the agents' reports and are visible in the diff.

Left open after application:

- **Owner decision 1 stands.** The clause "Stellaris plans to run ignited" was held back on both Part 3 and Part 4a so the pages and the post treat the 50 MW premise the same way. If the owner rules that the paper's Point A runs with zero operating heating, the post's Part 3 example, Part 3 §4, Part 4a theme 5 and Part 4b line 4754 move together.
- **Part 4b figure renderer.** `render_page_figures.py:18` sets `PAGE` to the deleted `archive/write-up/aries-model-transfer-outline.html`, so a plain run silently skips the page, and the README's run path points at the nonexistent `docs/write-up/`. Figure 5 was re-rendered through a scratch wrapper and the two-line diff copied in. Fix the paths before the next render; a plain run will also regenerate the archived `page-*.svg` files (the archived `page-how-close.svg` still says "not published").
- **Small residues, not changed:** Part 4b §4.4 says "within the physics and prices we represent" and two paragraphs later "conditional on the represented physics and assumed prices"; the §4 table row and §4.2 heading still read "steam or helium Brayton conversion?" while the opening question was reworded; Part 3 §7's next paragraph still opens "These checks show that the work is consistent…" right after the softened review sentence; Part 4a frame results at frames.json:115, 587 and 665 still say "now", covered only by the preamble sentence; Part 4a's three "Frame 28 made…" mentions are plain text because the page may carry only one frame-28 link.

## Summary

| Page | Must | Should | Where to edit |
|---|---|---|---|
| Part 2 | 2 | 3 | HTML directly |
| Part 3 | 2 | 1 | HTML directly |
| Part 4a | 5 | 2 | `src/model_viz/evolution/part-4a-modeling-stellaris.md`, `frames.json`, `build.py`; then rebuild |
| Part 4b | 9 | 6 | HTML directly, except the Figure 5 label in `archive/write-up/aries-study-assets/render_page_figures.py` |

Two things need an owner decision before editing; see [Owner decisions](#owner-decisions).

## Owner decisions

1. **Steady heating premise (post, Part 3, Part 4b).** The post (Part 3 example) and Part 3 §4 read the Stellaris paper's 50 MW as steady operating heating, so 49.1 MW required is "just inside what's installed". Two records read the paper differently: `work/orchestration/goals/burn-control/goal.md:22` and `stellaris-plasma-power-balance/answer.md` say Point A needs zero auxiliary heating at operation and the 50 MW is what is installed to reach it. Reviewer item 6 raised the same premise for the cycle study. If changed, the post and Part 3 move together; Part 4b line 4754 (the 100 MW electric draw as a supplied assumption) is the same premise. Surfaced, not resolved.
2. **Part 2 §2.3 and §2.6.1 (finding P2-2).** Outside the ratified item-7 scope, which named only §2.7.1. The removed sizing chain is the worked example for the whole pipeline walkthrough, in present tense. Either add the dating note proposed below or accept the page as a dated snapshot with the version note corrected.

## Part 2 — `docs/exploratory-modeling/part-2-model-execution.html`

**P2-1 (must). §2.7.1 presents automatic sizing as current behaviour and a Stellaris defect as fact.** Line 1699 and card labels at 1740, 1768, 1787, 1840. Item 7 requires distinguishing historical automatic sizing from the current supplied-winding evaluation, and avoiding a claimed defect in Stellaris. Part 4b §2 already calls this sizing a repaired design pattern, so the two pages disagree. Proposed replacement for line 1699, two paragraphs:

> With the tape performance we assume, the published Stellaris winding cannot carry its current: its tape would run at about 1.7 times its estimated critical current, where we allow 0.8. The winding also does not fit the radial space our model allocates for it. The 15 September joint magnet-sizing study [report] evaluated two changes intended to fix this: enough tape to carry the current, then more space for the larger winding.
>
> In that study, the model chose the amount of tape from the current requirement. We removed that option on 20 September, because a calculation that sizes equipment takes the choice away from the designer ([Part 4b, section 2](part-4b-aries-test.html#2-one-false-start-before-the-main-assessment)). The model now evaluates the winding a designer supplies, its size and the space allocated for it, and reports any shortfall instead of resizing it. The three cases below are the September study's results: the original design, a design with enough tape to carry the current, and a design with more space for that tape.

Facts: operating fraction 1.687 against allowable 0.8 (sealed record); the Part 4b anchor exists at its line 226. Do not add the narrative proposal's "supplied to today's model, the same three windings give the same results" sentence: it rests on the unsealed replay.

**P2-2 (must, owner decision 2). §2.3 and §2.6.1 use the removed sizing chain as the pipeline's worked example in present tense.** Lines 685, 909, 961, 1480–1495 (Figure 8), 1579. Only lines 464 and 880 date the snapshot (19 September). The version note at 1575 mentions only the ampere-turn change and wrongly says the field entry "no longer appears" (it is `pipeline.yaml:294`, reading `I_coil` from `winding_state`). Current pipeline: 269 entries, no `current_sizing` or `wp_sizing`; `wp_side` is a supplied input read by `wp_fit` and `wp_volume`. Proposed insert after line 911:

> This graph is the model as it stood on 19 September. The next day we removed the two sizing calculations, because they chose the winding's size from the current instead of evaluating a size the designer supplies (section 2.7.1). The pack side is now a supplied input: the fit, volume and cost calculations read it directly, and the current check reports whether that winding carries its current. Codegen resolves and orders those connections the same way.

Proposed line 685: "…and in the version shown here it calculated those dimensions from how much conductor the current needed." Proposed replacement for line 1575:

> The package has grown since: the current generated pipeline holds 269 entries. After the 20 September model changes, the coil ampere-turns are calculated from the supplied turns and current per turn, so this entry now reads them from that calculation, and the pack-sizing entry above no longer exists: the pack side is a supplied input. The excerpts on this page are the 17 September package, the one the studies in section 2.7 ran.

**P2-3 (should). Figure 10 caption, line 1814.** "The second sizes the conductor supply for the required current, with a 1% reserve." → "The second lets the model size the conductor supply for the required current, with a 1% reserve, an option since removed."

**P2-4 (should). The 24.9 T "limit" needs its qualification.** Lines 1780 and 1840. 24.9 T is Stellaris's published peak field, held as a ceiling with the reference calibrated onto it at zero margin (`stellarator_plant.sysml:436-437`); the field calculation omits the winding-pack term of Lion eq. 39 (`mfe_plasma_scaling.sysml:430-442`). Proposed after line 1840: "The 24.9 T limit is Stellaris's published peak field, held as a ceiling; the model is calibrated so the published design sits exactly on it, so any rise fails. The field calculation also responds only to coil position and leaves out a term that would lower the field for a larger winding, so the model does not establish which way the real field moves."

**P2-5 (should). §2.7.2 held input, line 14113.** "Conductor inventory multiplier (current-driven sizing on) 1.01" without saying the option was removed. Proposed note after the held-inputs table: "This map also ran with the since-removed tape-sizing option on. Its passing samples reflect that snapshot's checks and costs."

**P2-6 (optional). Line 1744** calls the required envelope "the pack" (0.370 × 0.379 → 0.535 × 0.548 are required-envelope dimensions; the pack side goes 0.36 → 0.525 m). → "The required envelope grows from…".

**P2-7 (optional). "DAG".** The post uses the term and points to Part 2; Part 2 never uses it. Proposed addition at line 913: "(a directed acyclic graph, or DAG). The direction also fixes which values a study can set: a value one calculation produces cannot also be supplied as a design choice."

Checked, no change: §2.5 component/material selection claims no material substitution; nothing conflicts with the post's Part 5 conductor comparison; the three study types and the constraint framing match. Side note for the post: line 67 says "plant radius and coil current"; Part 2 sweeps coil ampere-turns and separates them from conductor current (its line 558).

## Part 3 — `docs/exploratory-modeling/part-3-harness.html`

**P3-1 (must). §4 still uses the rejected ignition framing.** Lines 918, 919, 956. Facts are right (681 driven points, 510 now negative, per `20260905-stored-energy-basis/synthesis.md:31,85`); the framing names them "ignited" and makes control the missing piece. Proposed:

- Line 918: "Most of the earlier driven points now have more self-heating than the modeled losses."
- Line 919: "The earlier study had classed 681 points as driven, meaning they need some external heating within what the design supplies. At the new pin, 510 of them produce more fusion self-heating than the modeled losses at their selected temperature and density, so the heating they require is negative. The model checked only that the required heating was no more than the design supplies, so these points still passed. It did not check whether there was too much heat to balance. Stellaris is meant to run ignited, and evaluating these points with burn control would need mechanisms the model does not represent."
- Line 956: "The points with more self-heating than the modeled losses became the next goal, `burn-control`, which added a check that marks them as failing under the model's assumptions. The minor-radius edge became the goal after that, `minor-radius`." Optional: append ", narrowing the passing points in this study from 1,839 to 726" (726 is the study's feasible-driven count, synthesis line 59).

**P3-2 (must). §8 calls the analysis "credible".** Lines 1569 and 1572. The post now says the studies are imperfect and colleagues found mistakes. Proposed:

- Line 1569: "…and its analysis still needs a domain expert and has leaned on a published design to check against."
- Line 1572: "**Its analysis still needs a domain expert, and it has leaned on ground truth.** Colleagues reviewing this write-up found mistakes in the model's assumptions and in how results were read. Many of the issues we caught were found by comparing the model with a published design, such as the Stellaris paper."

**P3-3 (should). §7 summary, line 1564.** "The agent reviews show that the study's design and its conclusions fit the evidence, and on this goal they produced the corrections that mattered." The goal's "ignited" reading passed those reviews and was later questioned. → "The agent reviews check whether the study's design and its conclusions fit the evidence, and on this goal they caught the errors described above."

**P3-4 (optional). Line 1387** "its heating and ignition results change meaning" uses the study's own label; acceptable. If uniform vocabulary is wanted: "its heating results change meaning."

Checked, no change: heating example (90.6 MW, 50 MW, ash share, 49.08 MW, nothing tuned); 95%, four ARIES goals, seven rounds (1+2+1+3 in the four `aries-integrated-*` trails); no Part 4 result claims; links and anchors resolve; main-post link is `https://1cf.energy/exploratory-modeling/`.

## Part 4a — sources under `src/model_viz/evolution/`

The HTML is byte-identical to a fresh build from current sources, so every fix is a source edit plus rebuild. Theme prose: `part-4a-modeling-stellaris.md`. Per-frame text: `frames.json` (`title`, `question`, `result`, `result_source` are displayed). Six highlighted passages, the frame-record preamble and the viewer intro are hard-coded in `build.py` (452–459, 537, 584).

**P4a-1 (must). Ignition bullet, md:27 (HTML 203).** Current: "Most feasible points, 1,113 of 1,839, were ignited plasmas the model has no way to hold. We added a burn-control constraint (frame 8, …)." Proposed: "Operating points kept passing even when plasma self-heating exceeded the modeled losses, because the model checked that the installed heating was enough but not whether there was already too much heat to balance. We added a power-balance check under the model's assumptions. It marks 1,113 of the 1,839 passing sampled points as failing, leaving 726, and the failing points stay in the results. The check does not rule out ignition: a point that needs exactly zero heating passes, and Stellaris plans to run ignited. Evaluating the failing points properly would need burn-control mechanisms the model does not represent (frame 8, [record](../../../work/orchestration/goals/burn-control/trail.md))."

**P4a-2 (must). Cooling bullet, md:35 (HTML 207).** Current gives $8.2B with no drivers, configuration or limit. Proposed: "Cooling: replacing a single $205M allowance with priced circulators, pumps, piping and heat exchangers raised the estimate to $8.2B, and LCOE from 150 to 311 $/MWh, on the 18-circuit study case. About $7.4B of that is primary piping and heat exchangers, priced from assumed dimensions and nuclear-grade stainless fabrication. We had modeled an all-helium blanket, while a reviewer pointed to a helium/water split in Stellaris, so the figure shows what drives cost in the configuration we chose, not what Stellaris's cooling should cost (frame 22, [answer](…))." Basis: $3.824B piping + $3.621B exchangers, `installed-cooling-equipment-costs/answer.md`; 150.430 → 310.633 $/MWh.

**P4a-3 (must). Cost theme intro presents sizing-by-demand as the goal, md:33 (HTML 206) and build.py:455.** Contradicts MR-7 and theme 4 on the same page (md:42). Proposed: "We wanted each account to follow the equipment, priced by quantity, with installation and, for equipment that wears out, spares and replacements. The early goals also sized that equipment from the calculated demand, like heat exchangers from heat load; since frame 28 the equipment is a supplied choice, checked against that demand." Change build.py:455 to the new first sentence at the same time (it is a highlighted passage; `test_article.py:115` requires exactly 6).

**P4a-4 (must). Automatic winding-pack sizing as current behaviour, md:26 (HTML 203).** Current: "Now the winding pack is sized from the current, so more current means a bigger, more stressed coil and a larger cold mass." Pack side is a supplied input (`stellarator_plant.sysml:448`). Proposed: "More coil current was free. The goal sized the winding pack from the current, so more current meant a bigger, more stressed coil and a larger cold mass. Since frame 28 the pack is a supplied design choice, and more current raises its stress and current density instead of its size (frame 5, [record](…))."

**P4a-5 (must). Frame 8 title and result, frames.json:191 and :201 (HTML 221).** Title "Ruling out plasmas the heating cannot hold" → "Checking that the plasma power balance closes". Result "…the new check failed exactly the ignited ones." → "…the new check failed exactly those whose self-heating exceeded their modeled losses, and a point needing zero heating passes." Leave frame 8's `question`: it is a graded verbatim quote from goal.md.

**P4a-6 (should). Frame 9 casing mass, md:28.** Casing mass is supplied since frame 28 (`stellarator_plant.sysml:518`); peak field is still calculated. Proposed: "The goal made the coil bore set the peak field and casing mass, and the fattest plasmas at the paper's radius failed the conductor limit. The bore still sets the peak field; casing mass has been a supplied input since frame 28 (frame 9, …)."

**P4a-7 (should). "Stellaris fails both", md:29.** Item 7 says avoid a claimed defect in Stellaris; the fit answer calls the dimensions engineering scenarios, not measured casing dimensions. Proposed: "The reference design fails both under the assumed casing walls, insulation and tape performance: 370 mm of pack in 250 mm of casing, …" Keep the substring "370 mm of pack in 250 mm of casing" (`test_article.py:55`).

**P4a-8 (optional). Frame records that say "now" about things frame 28 changed** (frames.json:115, 587, 665). One sentence in the preamble at build.py:537 covers them: "Each result describes the model as that frame left it; frame 28 later made magnet, facility, fuel-processing and cooling sizes supplied inputs."

**P4a-9 (optional, model not page).** The check is shown as `burn_hold_ok` / 'Burn Hold'; its model description (`mfe_viability.sysml:416-435`) still says "HOLD condition… the installed heating system can hold". Needs a model change, already suggested by the ignition investigation. Nothing on the page.

Checked, no change: 55→199, 6→67, 14→76, 28 goals, 90.6→49.1 MW; theme 1; frame 28 bullet in theme 4; main-post link.

Rebuild: `uv run --no-sync python src/model_viz/evolution/build.py --article src/model_viz/evolution/part-4a-modeling-stellaris.md -o docs/exploratory-modeling/part-4a-modeling-stellaris.html`. Tests: `uv run python -m pytest tests/model_viz_evolution` (run alone). Tests check structure not wording: six themes, the "370 mm…" substring, exactly 6 highlighted passages, the "If a sweep shows" passage, no bold in themes. A highlighted passage that stops matching loses its highlight silently; lowercase "frame N" becomes a link; a relative link to a missing file makes the build refuse.

## Part 4b — `docs/exploratory-modeling/part-4b-aries-test.html`

**P4b-1 (must, item 3). Power bullet §3.3, lines 1305 and 1308.** Current: "about 11% less electricity…"; "The remaining gap is the cycle temperature…". Proposed 1305: "**Power: an unresolved gap.** Given ARIES's 2,436 MW of fusion power, our best tested steady alternative produced **891 MW net against the published 1,000 MW**." Line 1307 stays. Proposed 1308: "The higher flow carries the same heat in more helium, so the turbine inlet reached 628 °C against the published 708 °C. A large share of the heat, about 42%, arrives through the relatively cool blanket-helium circuit. An independent reviewer found that the published circuit heat loads and temperatures cannot all hold under the paper's stated exchanger temperature differences, and our sources do not say how ARIES reached its temperature. The gap remains unresolved."

**P4b-2 (must, item 3). Answer to question 1, lines 1368–1369.** Current: "largely yes once we added what ARIES needed… power is 11% low because our power cycle runs cooler…". Proposed 1368: "**Not with the library as built, and only partly once we added what ARIES needed.** [change list and highlighted sentence unchanged] The remaining differences matter. Our best tested steady case produces 891 MW net against ARIES's 1,000 MW, and we could not reconcile the published heat and temperature data with ARIES's 708 °C turbine inlet. Our cost comes near ARIES's only once we adopt its assumption that the blanket breeds its own tritium." Proposed 1369: "We then stopped, for time, before closing every gap. The ARIES magnets and conductor, breeding for the ARIES geometry and the cycle-temperature reconciliation remain open, and the financial comparison differs in more than the discount rate. Each is recorded with what it would take to close. And because we made the comparison after reading ARIES, it describes the differences rather than predicting them blind."

**P4b-3 (must, item 4). Cost sub-bullet, line 1313.** Current: "…its financing rate is not published…". Proposed: "With that assumption and ARIES's other accounting conventions, we calculate about **$59/MWh at our assumed 5% real discount rate**, and $32 to $105/MWh between 0 and 10%. Historical ARIES costing uses 4.35%, though other financial assumptions also differ, so the remaining difference is unresolved." Optional, from [discount-rate-investigation.md](discount-rate-investigation.md): "Changing only our rate to 4.35% gives about $55/MWh, so the rate alone does not explain the difference." (That record keeps $55 as a diagnostic, not a reproduction.)

**P4b-4 (must, item 4). Figure 5 label and aria-label, lines 1281 and 663.** "its discount rate is not published" → "historical ARIES costing uses 4.35%". Aria-label ending → "against ARIES's published 77.6. Historical ARIES costing uses a 4.35% discount rate, with other financial assumptions that differ." **Fix at the source:** `archive/write-up/aries-study-assets/render_page_figures.py` lines 191 and 459 rewrite the inline figure copies (its README line 16), so a direct HTML edit is overwritten on the next render. Change there and re-render.

**P4b-5 (must, item 4). Cost evidence panel, line 1361.** Current says the financing rate is "not recoverable from the printed pages"; the investigation found 4.35% in the registered ARIES cost documentation (Waganer, Table 31). Proposed: "Historical ARIES costing uses a 4.35% real discount rate. How ARIES-CS applied its financing, its decommissioning allowance, an independent operating cost and its treatment of tritium are not recoverable from the printed pages."

**P4b-6 (must, item 5). "Cheaper equipment" sentence, line 3172.** Proposed: "Steam's conversion equipment cost $2.55 billion, against $1.54 billion for Brayton. Per kilowatt the two cost about the same: about $2,720 for steam and $2,750 for Brayton, dividing each by its conversion subsystem's net output of 938 and 559 MW. An earlier version of this study, which costed the conversion equipment alone, likewise found the two within $5/MWh of each other. Both plants also needed the same $10.23 billion of other purchases, and steam spread those common costs, and later reactor replacements, over more than twice as many MWh. So the LCOE gap comes from Brayton's lower output at this source temperature, not from its equipment price." Arithmetic checked: 2,548/937.6 = $2,718/kW; 1,541/559.5 = $2,754/kW.

**P4b-7 (must, item 6). §4.2 question framing, lines 2772–2773 and after 2785.** Current question: "Which power-conversion system gives cheaper electricity from the same reactor?" Proposed opening for 2772: "How do the tested steam and helium Brayton options compare on a reactor that supplies helium at a fixed 500 °C? At that temperature steam works well and a Brayton turbine needs a hotter source, so this comparison favors steam." Rest of 2772 stays minus the "whose primary helium leaves at 500 °C" clause. Proposed 2773: "**At this 500 °C source, steam gave the lower LCOE at both supported heat loads, because it exported more than twice as much electricity.**" Add after 2785: "Each option was chosen from a finite list of priced offers, and the two had different freedoms: the steam turbine was held at its supported temperatures, while the Brayton cycle's flow and pressure ratio could vary. So neither was optimized on equal terms, and the result does not rank the two technologies in general." Source: `design-study-component-alternatives/answer.md:13`.

**P4b-8 (must, item 6). Heating assumption, line 2786.** After "…leaving 664 MW and 286 MW to sell." add: "That 274 MW includes 100 MW of electricity for plasma heating, which we supplied as an assumption. A burning plasma may not need it."

**P4b-9 (must, item 6). Components bullet in §4.4, line 5240.** Current: "conversion options that tie when their equipment is costed alone differ by more than 2× in LCOE once the whole plant is counted." Proposed: "**Components:** the conversion system can be swapped with its own equipment and evaluated as a whole plant. On a fixed 500 °C source, which favors steam, steam exported more than twice as much electricity and so gave the lower LCOE. This does not rank the technologies in general."

**P4b-10 (should, item 3). Power evidence panel, line 1336.** "The remaining 109 MW is all thermal efficiency…" The reconciliation record says this too; the post dropped the attribution by editorial choice. Proposed: "**The remaining 109 MW is in conversion efficiency:** 0.391 against ARIES's 0.43. Auxiliary power and total heat agree within the comparison's tolerances. Our turbine inlet is 628 °C against 708 °C. The extra flow needed to accept all the heat lowers it, and the published data do not show how ARIES reached 708 °C."

**P4b-11 (should). Architecture pressure loss, lines 5208–5209.** The page can read as if the model calculates the loss. It is supplied (`loss_fraction = 0.045`, `models/designs/aries_cs_integrated/plant.sysml:237`). Add after the first sentence of 5208: "The model does not calculate this loss from the piping. Each layout's loss is a supplied fraction, 4.5% in the nominal case, so calculating it is the next step." Proposed 5209 second sentence: "The study gives the gain and the supplied loss that would erase it: a reason to prefer the network, and a concrete thing to calculate before choosing it."

**P4b-12 (should). Section 5, lines 5249–5260.** Gives only positive indications; omits three of the post's four closing points. Proposed 5252 addition: "Much of the component library did not carry over: ARIES needed new plasma, blanket, conversion and cost definitions, and still lacks its own magnet and conductor models." Add before 5254: "The studies are imperfect. Reviewers found mistakes in our assumptions and in how we read the results, and many of the issues we caught came from comparing the model with a published design. Whether the harness's own checks are enough where there is no published design to compare against is still open."

**P4b-13 (should). §4.4 "Yes", line 5237.** → "**Yes, within the physics and prices we represent.** Each study evaluated a design question across the whole plant and showed what limits the result:"

**P4b-14 (should). §4.2 sensitivity paragraph, line 3604.** "What would change the choice?" → "What would change the result at this 500 °C source?" Add at the end: "The next study is to design each cycle for its own source temperature and to settle the heating assumption."

**P4b-15 (should, owner decision 1). Reactor evidence panel, line 4754.** "Its 50 MW of deposited heating draws 100 MW of electricity." → "Its 50 MW of deposited heating, drawing 100 MW of electricity, is a supplied assumption. It is not established that a burning plasma needs it."

Optional: line 2754 "The components study below shows what that costs" points across studies with different plants and dollar years (the page warns against this at 1388) → "shows the same effect on a different plant"; append to 2754 "The exchanger was fixed equipment in this sweep, so sizing it is the next step" (panel at 2763 supports it); line 279 "three steps" vs the post's "two steps"; line 5260 "a force of leverage" is an idiom; `archive/write-up/aries-model-transfer-outline.md:75` still has the "not published" text (drafting record only).

Checked, no change: parameter study numbers (427→621, 45%, exchanger limit at 1393, 2054, 5239); no claim that magnets or conductor were added for ARIES (650, 658, 1369, 5257).

## Stale records noted in passing

- [feedback-resolution.md](feedback-resolution.md) item 7 says the conductor story goes in the model-execution discussion and the closing callback; the post now carries it in Part 5 and the sizing paragraph was cut from Modeling Stellaris.
- `magnet-study-evaluation/evaluation.md:80` says no Nb₃Sn or 4 K conductor definition exists in `models/`; WI-099 (commit 2869c34aa) added one.
- The `docs/write-up/` path in feedback-resolution.md does not exist; Part 4a's source is `src/model_viz/evolution/part-4a-modeling-stellaris.md`.
