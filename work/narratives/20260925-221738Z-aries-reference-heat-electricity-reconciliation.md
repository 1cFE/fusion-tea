# Narrative: aries-reference-heat-electricity-reconciliation

This note summarizes cited records for the write-up. It is not evidence, goal state or a decision record. If it disagrees with a cited source, the source wins.

- **Goal status:** Open; no owner close is recorded at this cutoff. Five rounds are complete. The agent recommends closure as partially answered. [Trail](../orchestration/goals/aries-reference-heat-electricity-reconciliation/trail.md)
- **Narrative cutoff:** 2026-09-25 22:17:38 UTC, commit `7786bc29d2e3594bc2f30d3a81d80d584f8848d2`. Cited goal files are clean; unrelated write-up edits are excluded.
- **Review status:** Model design and implementation reviews passed; source and round reviews returned findings that the goal records as applied. This narrative has not been independently reviewed. [Review inventory](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#9-independent-reviews)

## At a glance

- **We investigated a specific disagreement:** with published fusion power supplied, our model calculated 796 MW net electricity against ARIES's reported 1000 MW. It also left 159 MW of heat unremoved, so that calculation did not describe steady operation. [Starting results](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#3-baseline-and-revised-heat--electricity-tables)
- **We corrected our model and input mapping:** the heat exchangers were connected incorrectly, and several inputs needed correction or consistent scaling between papers. [Attribution](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#4-quantitative-attribution)
- **We found an unresolved heat-transfer question:** the published duties and temperatures cannot all hold under the stated exchanger assumptions. The obtained cycle references do not explain how ARIES combined its three heat streams. This does not establish that the actual design could not reach its reported output. [Research findings](../orchestration/goals/aries-reference-heat-electricity-reconciliation/learnings.md)
- **An explicit alternative runs at 891 MW:** increased cycle flow and compressor rating allow complete heat removal and pass the evaluated checks. Its changed equipment has not yet been costed. It is neither a reconstruction of ARIES nor an upper bound on achievable output. [Alternative and limits](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#3-baseline-and-revised-heat--electricity-tables)

## Starting point and motivation

An earlier goal connected the component models and demonstrated studies. That did not establish agreement with the published plant. This goal therefore supplied the published fusion power and asked the downstream model to explain the heat balance and electricity output. Supplying fusion power isolates that question; it earns no credit for predicting plasma performance. [Goal contract](../orchestration/goals/aries-reference-heat-electricity-reconciliation/goal.md)

The test required an explanation of material differences, not tuning to the reported output. A numerical electricity result was insufficient if heat accumulated in the reactor. [Completion condition](../orchestration/goals/aries-reference-heat-electricity-reconciliation/goal.md#answered-when)

## Story in one picture

This sequence shows the consequences of successive changes. Electrical output and unremoved thermal power are separate quantities; they must not be added.

| Configuration | Net electricity, MW | Unremoved heat, MW | What it establishes |
|---|---:|---:|---|
| Original source-input case | 796.0 | 158.7 | Model runs, but cannot sustain the specified heat load. |
| Corrected inputs, original exchanger connections | 842.7 | 151.0 | Input corrections improve the result but do not resolve heat removal. |
| Corrected inputs and published exchanger connections | 879.7 | 109.9 | Correcting connections removes about 41 MW of the remaining heat shortfall. |
| Above case with primary flows scaled consistently between papers | 892.4 | 95.7 | Mapping correction helps, but this remains an inadequate heat-removal case. |
| Explicit higher-flow, higher-rated-compressor alternative | 891.0 | 0 | Best tested steady alternative; evaluated checks pass. |
| Published ARIES systems reference | 1000 | 0 | Comparison target, not reproduced. |

Source: [case tables and flow-scaling study](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#3-baseline-and-revised-heat--electricity-tables). The alternative uses 1700 kg/s cycle flow and a 1700 MW compressor rating. A rating is selected equipment capacity, not an extra electrical load to subtract from net output. The model calculates operating demand separately.

The evaluated checks do not establish full engineering feasibility. [Check scope](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#3-baseline-and-revised-heat--electricity-tables)

## Research learnings

### Cycle efficiency and heat delivery are different questions

The obtained cycle method calculates performance with turbine inlet temperature supplied as an input. Our connected model must also calculate whether the reactor's heat streams can produce that temperature. The obtained references do not provide the missing multi-loop calculation. [Accepted source findings, L-013](../orchestration/goals/aries-reference-heat-electricity-reconciliation/learnings.md)

The useful physical example is the blanket-helium loop. Its hot inlet is only 456 °C, yet it carries about 42% of the published heat. With the stated exchanger temperature difference, it can cover only about 21% of the specified cycle temperature rise. That mismatch constrains heat transfer even when total thermal power looks sufficient. [Thermal review finding, L-010](../orchestration/goals/aries-reference-heat-electricity-reconciliation/learnings.md)

This supports an inconsistency under the stated exchanger assumptions. It does not establish how the original ARIES calculation treated the exchangers, or what the actual design could achieve. Interpreting the source sketch as one lumped heat source remains an inference. [Qualified findings, L-010 and L-013](../orchestration/goals/aries-reference-heat-electricity-reconciliation/learnings.md)

### The source search reached a documented stopping point

Two older cycle-method papers were obtained. The more directly relevant blanket-coupling paper could not be obtained through permitted access. The owner subsequently accepted the older papers for this investigation, retained the mirror-access violation in the record, and deferred purchasing the coupling paper. [Owner rulings after round 5](../orchestration/goals/aries-reference-heat-electricity-reconciliation/trail.md#owner-rulings-after-round-5--2026-09-25)

## Model changes

- **Correct the exchanger connections.** The inherited assembly put all three exchangers in series. The published arrangement heats the cycle gas in the blanket-helium exchanger first, then divides it between the PbLi and divertor exchangers before mixing it again. The new alternative preserves exact replay of the old arrangement. [Implementation and reuse](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#8-reuse-and-model-changes)
- **Correct inputs and their mapping.** Changes covered heat partition, recuperation, flow and auxiliary accounting. We also corrected a cross-paper mapping that scaled heat duties without scaling primary flows. [Attribution](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#4-quantitative-attribution), [mapping finding, L-011](../orchestration/goals/aries-reference-heat-electricity-reconciliation/learnings.md)
- **Keep hardware choices explicit.** The larger compressor is a separately selected alternative, not automatic resizing hidden inside evaluation. Existing cycle equations and cost machinery were reused; Stellaris remained unchanged. [Reuse](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#8-reuse-and-model-changes), [preservation](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#10-stellaris-preservation)

## Study results

The higher-flow alternative removes all modeled heat at a turbine inlet of 628 °C. It produces 1143 MW gross and 891 MW net, compared with the published 1253 MW gross and 1000 MW net. Within our model, the electricity gap follows from the lower conversion efficiency. Why the published descriptions imply a different attainable temperature remains unresolved. [Quantitative attribution](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#4-quantitative-attribution)

More flow does not mean more electricity. Increasing cycle flow further to 1800 kg/s also removes all the heat, but lowers turbine inlet temperature and gives about 804 MW net. A second alternative with lower recuperator effectiveness removes all heat at about 760 MW net. These are tested alternatives, not an optimization result. [Study table](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#3-baseline-and-revised-heat--electricity-tables)

## Outcome and follow-on issues

**The reconciliation is partially answered.** We corrected errors and demonstrated an alternative satisfying modeled heat removal and equipment checks. We did not reproduce the published plant. Remaining unknowns include its detailed exchanger coupling, terminal temperatures and flow split, the composition of the reported thermal power, and whether its exchanger design supplies the reported turbine inlet temperature. [Current answer](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md#13-owner-gates-and-next-actions)

**Write-up interpretation [AGENT]:** the connected model made the assumed link between reactor heat and cycle efficiency testable. It also exposed errors in our own assembly and source mapping. That is evidence of useful engineering diagnosis, not numerical validation of the whole generalized stellarator model. Basis: the corrections and remaining discrepancy above.

**Proposed next goal [AGENT]: evaluate the cost and LCOE of the explicitly modified 891 MW alternative.** This is a new economic question, consistent with the owner's direction to handle costing separately. [Owner ruling](../orchestration/goals/aries-reference-heat-electricity-reconciliation/trail.md#owner-rulings-after-round-5--2026-09-25)

- Replay and identify the exact steady configuration before costing it.
- Reuse the equipment and lifecycle machinery, checking that selected ratings, purchase amounts and operating demand correspond to this configuration.
- Account for the changed flow and compressor, including affected equipment whose cost cannot yet be supported. Keep assumptions and unsupported costs explicit.
- Calculate LCOE under separately named tritium-supply assumptions. Explain differences from published ARIES economics by electricity output, capital, fuel, operation and financial conventions; do not force agreement.
- Use targeted studies to show which uncertain assumptions materially change the result.
- Stop when the alternative has internally consistent equipment, costs and lifecycle accounting, with each material comparison gap quantified or explicitly unresolved. This would complete a conditional economic assessment, not certify ARIES reproduction or physical feasibility.

These bullets are a proposed scope for an owner-reviewed goal prompt, not authorization to start a goal.

## Evidence and visual index

- [Goal contract](../orchestration/goals/aries-reference-heat-electricity-reconciliation/goal.md): original question and completion condition.
- [Answer](../orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md): numerical tables, attribution, reviews, limitations and replay commands.
- [Learnings](../orchestration/goals/aries-reference-heat-electricity-reconciliation/learnings.md): accepted findings and qualifications.
- [Trail](../orchestration/goals/aries-reference-heat-electricity-reconciliation/trail.md): rounds, owner rulings and WI-092 closure; formal goal closure remains pending.
- **Visual ready for the write-up:** the configuration table above distinguishes higher numerical output from adequate heat removal. It should accompany any account of the progression toward the 891 MW alternative.
