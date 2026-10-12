# Stellarator demo write-up: feedback and resolution strategy

Created: 2026-09-29

Status: Editorial strategies for all seven items accepted on 2026-09-29. Main-post revisions drafted in `archive/write-up/main-post-draft.md` for owner review; supporting HTML edits pending. The item decisions below preserve the accepted strategy; their article-pending labels predate this draft.

Status, 2026-09-30: the main post's Part 4 closing and Part 5 were revised with the owner in session. The supporting pages were audited against the revised post and the edits are recorded, with proposed wording and line numbers, in [support-page-audit.md](support-page-audit.md); the owner directed that they be applied. One premise question is open there (the paper's 50 MW read as steady operating heating).

## Purpose and authority

[OWNER] Walk through each feedback item and decide how much to change the write-up and how much to address the underlying study defect.

[OWNER] A possible strategy is to acknowledge reasoning mistakes made by the agents. The owner did not push the agents on the specifics during the original work.

The passages and reviewer feedback below are verbatim payload from the owner's message. Their force is material to review, not established technical findings or approved corrections. Reviewer claims, including replacement numbers, have not been independently verified in this capture. Proposed next steps are [AGENT] suggestions, not settled decisions.

The project notes reference `docs/write-up/stellaris-evolution.md`, but `docs/write-up/` is absent from this checkout. The quoted passages therefore remain the source for this record; exact article locations can be added when available. (2026-09-30: the published pages are under `docs/exploratory-modeling/`; Part 4a is built from `src/model_viz/evolution/part-4a-modeling-stellaris.md`.)

## Presentation strategies

[OWNER-VERBATIM] Two possible strategies, neither selected:

> We try to fix up the studies and analysis so that they read as defensible and reasonably credible. and acknowledge it took some hand-holding.

> We report these as the analyses produced by agents directly, and then present a meta-analysis (acknowledge mistakes / bad assumptions in the study)

[AGENT] The first strategy requires evidence for the repaired claims and a clear account of human intervention. The second requires distinguishing the original agent conclusions from what subsequent review exposed. Both can acknowledge specific reasoning mistakes once established. We can choose the treatment per item while keeping the overall story clear.

## 1. Ignition framed as a feasibility or control failure

### Original passage

> Make the model push back. In one sweep, most of the "feasible" designs (1,113 of 1,839) turned out to be ignited plasmas the model had no way to control. That became the next goal and a new constraint.

### Reviewer feedback

> ??  Consider rewording.  Many stellarator designs plan to operate in the ignited condition.

### Resolution to discuss

- [AGENT] Write-up route: distinguish the model's missing treatment of an operating regime from a claim that ignition itself makes a stellarator design infeasible or uncontrollable. Recheck what the 1,113 cases actually demonstrate before retaining the count in that argument.
- [AGENT] Study route: inspect the new constraint and its rationale. Determine whether it excludes ignition by assumption, tests a documented operating requirement, or represents control capability. Decide whether the study needs an explicit ignited operating regime and revised feasibility checks.
- [AGENT] Evidence needed: original sweep, definition of feasibility, ignition classification, successor constraint, and sources for the intended operating/control strategy.

Decision: Editorial strategy accepted, 2026-09-29. [AGENT] (ratified by owner, 2026-09-29) Characterize the check as power-balance consistency under the model's assumptions, acknowledge missing burn-control coverage, and retain the constraint without relaxation. [OWNER] Say points are marked as failing, rather than excluded. The article edit remains pending. Resolution evidence: [Constraint investigation](ignition-constraint-investigation.md).

## 2. Cooling-system cost and the assumed plant configuration

### Original passage

> Make cost follow the design. The cooling system's $205M allowance became $8.2B of sized pumps, piping and exchangers once cost had to follow the hardware.

### Reviewer feedback

> Hey @Reid this number was suspicious to me and I did some digging.  Turns out the SysML model is assuming a fully helium-cooled blanket, which is causing the pipes and heat exchangers to be huge.  Stellaris uses a helium/ pressurized water split, which results in significantly lower system cost. Also, the benefit of helium (higher coolant outlet temperature for better turbine performance) isn’t being realized because of the EUROFER temperature constraint.   So it’s a fixed, suboptimal design.  The cost account also doesn’t apply any learning rates to adjust to a NOAK basis.  When I had Claude model a cooling configuration closer to what Stellaris actually plans to use, the cooling system cost drops to ~0.8B (LCOE ~ $165/MWh).

### Resolution to discuss

- [AGENT] Write-up route: state the configuration and cost basis behind $8.2B, and revisit whether the passage mistakes an assumption-driven result for a credible Stellaris cost estimate. Explain any established agent mistake explicitly.
- [AGENT] Study route: investigate the helium/water split, material temperature limits, equipment sizing, and nth-of-a-kind (NOAK) cost treatment. Compare a sourced alternative with the original configuration using consistent cost boundaries and financial assumptions.
- [AGENT] Evidence needed: cooling architecture sources; original sizing and cost accounts; learning-rate basis; and the reviewer's alternate model, inputs, and results. The reported ~0.8B and ~$165/MWh are unverified comparison results, not adopted targets.

Decision: Editorial strategy accepted, 2026-09-29. [AGENT] (ratified by owner, 2026-09-29) Retain the cooling example as an explanation of the selected configuration's cost drivers and assumptions. Explain that detailed accounting alone does not establish a credible Stellaris cost. No cooling redesign is required for this write-up. Article edit pending. Evidence: [historical cost breakdown](../../../../work/orchestration/goals/installed-cooling-equipment-costs/answer.md:26).

### Accepted direction for replacement wording

[AGENT] Draft supporting the ratified strategy; final article wording remains editable:

> **Make cost assumptions inspectable.** Replacing the cooling allowance with an equipment breakdown raised the modeled estimate from $205M to $8.2B. About $7.4B came from primary piping and heat exchangers in the selected helium/salt configuration, using assumed dimensions and nuclear fabrication prices. That exposed the importance of the cooling architecture and construction assumptions; it did not establish what Stellaris’s cooling system should cost.

## 3. ARIES turbine inlet temperature and net-power gap

### Original passage

> Power: about 11% low. From ARIES's 2,436 MW of fusion power, our model produces 891 MW of net electricity against the published 1,000 MW. Most of the gap is temperature: our turbine inlet reaches 628 °C, against 708 °C in ARIES.

### Reviewer feedback

> why is turbine inlet temperature lower than ARIES?

### Resolution to discuss

- [AGENT] Write-up route: explain the traced cause of the 628 °C result and establish whether temperature actually accounts for most of the net-power gap. The present wording names a difference without explaining its origin.
- [AGENT] Study route: trace source temperatures, exchanger assumptions, temperature drops, and cycle inputs against the ARIES configuration. Correct mismatches if found and recompute the power comparison.
- [AGENT] Evidence needed: provenance of both turbine inlet temperatures and a power-balance comparison that separates conversion performance from pumping, heating, and other auxiliary loads.

Decision: Editorial strategy accepted, 2026-09-29. [AGENT] (ratified by owner, 2026-09-29) Explain the temperature mechanism and present the result as an unresolved reconciliation. The 628°C / 891 MW result is the best tested steady modeled alternative, with 1,700 kg/s cycle flow and a larger assumed compressor. At lower tested flow the exchanger system cannot accept all the available heat; the increased flow accepts it but gives a lower turbine inlet temperature under the coupled cycle balance. A substantial heat fraction arrives through the relatively cool blanket-helium circuit. The reconciliation could not make the published duties, temperatures and exchanger assumptions agree. Its cited cycle-method investigation did not establish how ARIES combined its heat sources. The earlier exchanger-connection mistake in our model was corrected; the remaining discrepancy survived that correction. Further study requires a specific missing source or new hypothesis; no additional sweep is selected for the write-up. Article edit pending. Evidence: [answer, tables and limitations](../../../../work/orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md:5), [thermal-cycle review](../../../../work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/q1-thermal-cycle-review.md:21).

### Accepted direction for replacement wording

[AGENT] Draft supporting the ratified strategy; final article wording remains editable:

> **Power: an unresolved gap.** At the published fusion power, our best tested steady alternative produces 891 MW net. Transferring all the reactor heat requires increased cycle flow and a larger compressor; the resulting turbine inlet temperature is 628°C, versus the published 708°C. We could not reconcile the published heat-source and exchanger data with that higher temperature, so this remains a modeled alternative rather than a reproduction of ARIES.

## 4. ARIES discount rate

### Original passage

> (we get about $59/MWh at a 5% discount rate; ARIES doesn't publish its rate)

### Reviewer feedback

> Looks like it’s 4.35%  https://www.osti.gov/servlets/purl/6570291
> (I checked and this # recreates the 77.6 #)

### Resolution to discuss

- [AGENT] Write-up route: verify the supplied source and correct the claim that ARIES does not publish its rate if the reported rate applies. Record the page, rate definition, and financial basis.
- [AGENT] Study route: reproduce the reported 77.6 result and evaluate our comparison at the applicable rate, checking that the remaining financial assumptions align.
- [AGENT] Evidence needed: the reviewer-supplied [OSTI document](https://www.osti.gov/servlets/purl/6570291), the relevant passage/table, and the calculation behind the reported reproduction. Source inspection is pending.

Decision: Editorial strategy and wording accepted, 2026-09-29. [AGENT] (ratified by owner, 2026-09-29) Use the short correction below and retain the detailed reconciliation in supporting notes. No further study is required for this correction. Article edit pending. Evidence: [discount-rate investigation](discount-rate-investigation.md).

> We get about $59/MWh using our assumed 5% discount rate. Historical ARIES costing uses 4.35%, though other financial assumptions also differ.

## 5. Conversion-equipment cost: steam versus helium Brayton

### Original passage

> Components: steam vs helium Brayton. The cheaper conversion equipment gave the more expensive electricity.

### Reviewer feedback

> brayton cycle is more expensive per kW

### Resolution to discuss

- [AGENT] Write-up route: specify what “cheaper” compares: total equipment cost, cost per gross kW, or cost per net kW. Recheck the sentence against the actual comparison before retaining it.
- [AGENT] Study route: compare equipment scope, capacity, currency year, and cost maturity on consistent bases. Repair the costing if a mismatch explains the apparent result.
- [AGENT] Evidence needed: both equipment cost breakdowns, gross and net output, and the basis for the reviewer's per-kW comparison.

Decision: Editorial strategy accepted, 2026-09-29. [AGENT] (ratified by owner, 2026-09-29) Keep the narrowed steam-versus-Brayton component example. Remove the “cheaper equipment, more expensive electricity” framing. Give approximately $2,720/kW for steam and $2,750/kW for Brayton when discussing specific cost, with conversion-subsystem net capacity explicitly identified as the denominator. Article and HTML edits pending. Evidence: [conversion study](../../../../work/orchestration/goals/design-study-component-alternatives/answer.md) and [replacement evaluation](magnet-study-evaluation/evaluation.md).

## 6. Cycle comparison at 500 °C, low net output, and steady-state heating

### Original passage

> The physical reason is temperature: the reactor delivers helium at 500 °C, so the Brayton turbine runs at about 413 °C, against 708 °C in ARIES, and its compressors eat most of the turbine's output.

### Reviewer feedback

> This is kind of a flawed study because you're comparing steam vs. brayton, but the fixed config inherently favors steam (given the 500C heat source).
> Also net power looks suspiciously low in these configs — possibly because of the full-helium cooling assumption?  Also, there should be virtually no heating power required in steady state.

### Resolution to discuss

- [AGENT] Write-up route: make the question and fixed source conditions explicit, and limit the conclusion to what that comparison supports. Address the criticism that the agents presented a configuration-dependent outcome as evidence about cycle choice.
- [AGENT] Study route: decide whether the intended question is which cycle suits this fixed heat source or which plant/cycle combinations are credible alternatives. For the latter, define and evaluate appropriate source conditions for each alternative.
- [AGENT] Study route: separately inspect the net-power balance, including primary coolant circulation, cycle compression, and steady-state heating. Check whether the heating assumption matches the plasma operating regime before changing it.
- [AGENT] Evidence needed: the comparison contract, thermal states, gross generation, each recirculating load, and the heating/control assumptions. Resolve alongside items 1, 2, and 5 so changes are consistent.

Decision: Editorial strategy accepted, 2026-09-29. [AGENT] (ratified by owner, 2026-09-29) Frame the question as how the tested conversion options compare given the fixed 500°C heat supply, which favors steam. State the finite catalog, unequal optimization opportunities, and supplied steady-state heating assumptions. The result supports no general technology ranking. No new conversion study is required for this editorial correction. Article and HTML edits pending. Evidence: [conversion study](../../../../work/orchestration/goals/design-study-component-alternatives/answer.md), [whole-plant power budget](../../../../work/orchestration/goals/design-study-whole-plant-conversion/answer.md), and the briefing below.

## 7. Conclusion and magnet optimization callback

### Original passage

> I wouldn't make a design decision from any of these study outcomes. What I would take from them is that the model points at the right kinds of questions:

### Reviewer feedback

> consider calling back to the magnet optimization here

### Resolution to discuss

- [AGENT] Write-up route: revisit the magnet optimization and determine what specific, supported result belongs in the conclusion. Tie the closing claim to that evidence and to the chosen presentation strategy.
- [AGENT] Study route: inspect the existing magnet result before deciding whether further work is needed. The feedback itself requests an editorial callback.
- [AGENT] Evidence needed: the magnet optimization passage, underlying results, and their stated limitations.

Decision: Editorial strategy accepted, 2026-09-29. [AGENT] (ratified by owner, 2026-09-29) Use the conductor story in the main post's model-execution discussion, Part 2, and the concluding callback. Explain how changing conductor inventory propagates into fit and other model checks. Correct Part 2 §2.7.1 to distinguish historical automatic sizing from the current evaluation of explicitly supplied winding choices; retain the historical version context. Avoid claims of a qualified magnet, a successful optimum, or a demonstrated defect in Stellaris. Keep the new unsealed refrigerator/building replay findings out of public passages. No new study is required for this editorial correction. Evidence: [evaluation](magnet-study-evaluation/evaluation.md) and [narrative proposal](magnet-study-evaluation/narrative-proposal.md). These decisions approve the editorial strategy, not every sentence of the proposed drafts.

Placement, 2026-09-30: [OWNER] the main post carries the conductor comparison (REBCO vs Nb₃Sn, goal `magnet-material-comparison` round 1) in Part 5 as the systems-level-intuition example, and the Part 4 model-execution sizing paragraph was cut as redundant with it. The Part 2 §2.7.1 correction is item P2-1 in [support-page-audit.md](support-page-audit.md).

## Walkthrough and decision record

### Reviewer follow-up supplied by owner

Verbatim reviewer payload, 2026-09-29; advice to consider, not an owner decision or independently verified general claim about conversion cycles:

> yea I think it's fine to release the model as it stands and just explain WHY the model thinks cooling costs would increase from 205M to 8.2B, for example.
> For the power conversion trade, I'd get rid of the "Brayton is cheaper but produces less electricity" phrasing because that stood out to me as wrong (Brayton cycle, when properly optimized, produces more electricity and generally costs more per kW)
> The magnet study you linked to seemed interesting - you could possibly take out the power conversion bit and instead talk more about the conductor sizing?

[AGENT] Initial cooling-record check: the historical selected case used eighteen primary helium circuits and an intermediate HITEC salt loop. Its $8.205B total comprises $3.824B primary piping/fittings, $3.621B exchangers, $0.460B helium circulators, and about $0.300B other equipment/inventories/spares. Thus about 91% is primary piping and exchangers. The record prices fixed representative geometry per circuit, including assumed wall thicknesses and routing; it does not establish an optimized cooling design. Finished nuclear stainless fabrication prices and installation assumptions amplify the construction-mass assumptions. See [equipment and cost breakdown](../../../../work/orchestration/goals/installed-cooling-equipment-costs/answer.md:9) and [sensitivities and limitations](../../../../work/orchestration/goals/installed-cooling-equipment-costs/answer.md:78).

[AGENT] Item-2 strategy ratified by owner, 2026-09-29: retain the result as an explanation of what the selected architecture, equipment geometry, and costing assumptions produce; revise the implication that detail alone established a credible Stellaris cooling cost. No cooling redesign is required for this write-up. The claimed helium/water alternative and ~$0.8B result remain unverified, as does the magnitude of any NOAK learning adjustment.

[AGENT] Walk through items 1–7 with the owner. For each, record the established issue, the chosen treatment, the supporting evidence, and any remaining claim limits. Items 1, 2, 5, and 6 share assumptions; revisit their decisions together before executing study changes.

| Item | Verified finding | Chosen write-up treatment | Chosen study work | Resolution evidence |
|---|---|---|---|---|
| 1. Ignition/control | Exact zero passes; negative required heating fails; no demonstrated controllability | Accepted: power-balance check marks points as failing under model assumptions; article edit pending | Retain constraint; no study repair selected | [Investigation](ignition-constraint-investigation.md) |
| 2. Cooling configuration/cost | About 91% of the historical $8.205B estimate is primary piping and exchangers under selected geometry and cost assumptions | Accepted: explain configuration, cost drivers and limitations; article edit pending | No cooling redesign required for write-up | [Cost breakdown](../../../../work/orchestration/goals/installed-cooling-equipment-costs/answer.md:26) |
| 3. ARIES temperature gap | Retained reconciliation explains lower temperature through cycle flow and heat-source limits; published comparison remains unresolved | Accepted: explain mechanism and identify 891 MW as modeled alternative; article edit pending | No additional sweep selected; further investigation needs missing evidence or a new hypothesis | [Reconciliation](../../../../work/orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md) |
| 4. Discount rate | Historical methodology publishes 4.35%; other financial assumptions differ | Accepted: short factual correction; detailed diagnostics stay in supporting notes; article edit pending | No further study required for correction | [Investigation](discount-rate-investigation.md) |
| 5. Equipment cost comparison | Conversion-subsystem specific costs are about $2,720/kW steam and $2,750/kW Brayton | Accepted: keep narrowed component example; remove misleading total-cost framing | No new study required for editorial correction | [Conversion study](../../../../work/orchestration/goals/design-study-component-alternatives/answer.md) |
| 6. Cycle study and net power | Fixed 500°C source, finite catalog, and assumed upstream/heating loads limit interpretation | Accepted: state conditional question and assumptions; no general ranking | No new study required for editorial correction | [Whole-plant study](../../../../work/orchestration/goals/design-study-whole-plant-conversion/answer.md) |
| 7. Magnet callback | Existing study varies sizing of one conductor; historical automatic sizing was later removed | Accepted: main-post callback and Part 2 correction; retain historical context | Unsealed replay remains supporting investigation; future material study discussed separately | [Evaluation](magnet-study-evaluation/evaluation.md) |

[AGENT] This file tracks the editorial resolution discussion. Any selected modeling work should be managed in the modeling workflow and linked here as evidence.

## Briefing on items 5–7: conversion comparison and conductor sizing

[AGENT] The retained conversion comparison uses a fixed 500°C primary helium supply and a finite equipment catalog with different operating freedoms for the two branches. At 2,500 MW source heat, its conversion-only result has steam capital $2.548B and net output 937.579 MW, versus Brayton $1.541B and 559.493 MW. “Cheaper” refers to total purchases; divided by each subsystem's net output, these rounded numbers give roughly $2,720/kW for steam and $2,750/kW for Brayton. The original phrasing obscures that distinction. These specific offers do not establish a general technology ranking. [Conversion study](../../../../work/orchestration/goals/design-study-component-alternatives/answer.md).

[AGENT] The subsequent whole-plant comparison retains 50 MW deposited auxiliary heating and 100 MW electrical heating demand as supplied assumptions. At 2,500 MW heat, both branches carry 273.6 MW upstream electrical demand. Thus low plant net output includes assumed reactor loads as well as cycle performance. The supplied-source comparison does not establish that this steady-state heating is required by an ignited plasma. [Whole-plant boundary and power budget](../../../../work/orchestration/goals/design-study-whole-plant-conversion/answer.md:7).

[AGENT] (ratified by owner, 2026-09-29) Retain the conditional conversion comparison as the component-choice example. The investigated magnet replacement uses the same REBCO conductor throughout, duplicates Part 2, and relies on historical automatic sizing later removed from the model. Use it for the model-execution narrative and conclusion, with the Part 2 historical-sizing correction specified above. [Evaluation](magnet-study-evaluation/evaluation.md).

## Possible future magnet-material study

[OWNER] Requested discussion of the viability of launching a proper magnet study, including fetching the required data, after recording the editorial decisions. No new modeling goal has been launched. Scope and data sufficiency remain to be discussed; the editorial corrections above do not depend on completing that future study.
