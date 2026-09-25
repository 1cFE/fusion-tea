# Owner brief — 2026-09-25 (verbatim)

[OWNER-VERBATIM] The owner's message issuing this goal, quoted in full. The `run-goal` skill was invoked with `ground a new goal: aries-reconciled-alternative-economics`.

> Use the run-goal workflow to evaluate the equipment costs and LCOE of the 891 MW modeled alternative produced by the ARIES heat/electricity reconciliation.
>
> Proposed goal slug: aries-reconciled-alternative-economics
>
> Question
> What does this explicitly modified plant cost, what is its LCOE under stated fuel-supply assumptions, and what explains its economic differences from the published ARIES estimate?
>
> This is a fresh economic assessment. The 891 MW configuration is a modeled alternative, not a reconstructed ARIES reference. Agreement with the published LCOE is not a tuning target.
>
> Start from authoritative records
> - work/orchestration/goals/aries-reference-heat-electricity-reconciliation/{goal,trail,learnings,answer}.md
> - Its reference-case contract, discrepancy ledger, sealed studies and owner rulings.
> - work/orchestration/goals/aries-integrated-equipment-costs/answer.md
> - work/orchestration/goals/aries-integrated-lcoe/answer.md
> - work/orchestration/goals/aries-integrated-design-studies/answer.md
> - modeling_project/REQUIREMENTS.md, especially MR-7.
>
> The write-up progress note under work/narratives/ is orientation only. Ground decisions and calculations in the underlying records.
>
> 1. Establish the exact configuration before costing it
>
> Identify and replay the best tested steady alternative:
> - Approximately 891 MW net electricity.
> - 1700 kg/s cycle flow.
> - Explicitly selected 1700 MW compressor rating.
> - Published series-then-parallel exchanger arrangement.
> - The corrected cross-paper mapping of primary flows and heat duties.
>
> Read the actual case inputs; do not reconstruct the configuration from these headline numbers. Record its package identity, full inputs, selected equipment, operating demands, heat balance and evaluated checks.
>
> Distinguish equipment rating from operating power. Confirm that the higher flow and selected equipment are represented consistently throughout the assembly.
>
> Preserve the original failing cases and historical studies. Report any replay discrepancy before dependent economic work.
>
> 2. Audit the equipment and cost bindings
>
> Determine which purchases, operating expenses and replacements change for this configuration.
>
> At minimum examine the compressor, turbine, recuperator, primary and cycle-side heat transport, heat rejection, electrical equipment and affected auxiliary loads. Determine which are actually affected; do not assume they all require enlargement.
>
> For each material item, record:
> - Selected equipment quantity, rating or purchase amount.
> - Calculated operating demand and the corresponding adequacy check.
> - Cost basis, units, currency year and applicability.
> - Whether its cost is supported, assumed or unresolved.
>
> Reuse existing definitions and lifecycle machinery wherever their meaning remains appropriate. Make the smallest justified corrections where bindings are inconsistent.
>
> Follow MR-7: supplied equipment choices remain supplied choices. Do not silently resize hardware or substitute operating demand for purchased capacity. If different equipment is needed, declare a separate alternative with explicit inputs.
>
> Where performance maps or price data are missing, use clearly identified assumptions and sensitivity ranges. Do not imply vendor qualification or invent evidence.
>
> 3. Run interim checks before calculating headline LCOE
>
> Use targeted cases to verify:
> - The canonical configuration reproduces the heat/electricity result.
> - Changed operating demand reaches the relevant equipment checks.
> - Selected purchase amounts affect costs through the intended bindings.
> - Inadequate selections remain visible as failures.
> - Capital, annual operation, replacements and terminal costs are counted once.
>
> Preserve the existing financial treatment where justified, including financing once and replacement cashflows without duplicate reserves. Recheck applicability to this configuration rather than assuming the earlier 423 MW assessment transfers unchanged.
>
> Declare numerical tolerances before interpreting the study results.
>
> 4. Calculate lifecycle costs under explicit fuel scenarios
>
> Recalculate fuel demand for this configuration. Do not reuse the earlier baseline's annual quantities without verification.
>
> Retain separately named scenarios covering:
> - No breeding credit, with required external tritium purchases.
> - The previously used assumed new-tritium-feed scenario, with its quantity, price, availability and accounting meaning stated explicitly.
>
> Keep exhaust recycling separate from new tritium supply. Supply capability remains assumed unless independently supported. Report shortfalls and residual purchases.
>
> For each scenario, report:
> - Net generation and annual delivered electricity.
> - Overnight and financed capital.
> - Annual operating costs, including fuel.
> - Replacement and terminal cashflows.
> - LCOE contributions and total LCOE.
> - Failed engineering checks and scientific qualification limits.
>
> 5. Explain the comparison with published ARIES economics
>
> Establish the comparison's accounting basis before interpreting a difference:
> - Currency year.
> - Net versus gross electricity.
> - Availability and lifetime.
> - Financing and construction treatment.
> - Capital scope and contingency.
> - Fuel, replacement and decommissioning assumptions.
>
> Separate a comparison using aligned accounting conventions from our independently evaluated alternative.
>
> Attribute material differences to electricity output, selected equipment, fuel supply, other operating costs and financial assumptions. Show interactions where a simple additive attribution would mislead. Mark differences that cannot be resolved from available evidence.
>
> Never substitute published electricity or cost totals into a result described as an independent prediction. Any diagnostic substitution must be separately labeled.
>
> 6. Run a bounded sensitivity study
>
> Choose a small set of uncertainties that could materially change the economic conclusion, including the changed equipment's cost and tritium-supply assumptions. Justify the ranges.
>
> The purpose is to determine which conclusions survive those assumptions, not to optimize until the result resembles published ARIES economics. Retain failed cases and explain where numerical evaluability or scientific support ends.
>
> Completion condition
>
> Deliver a replayable economic assessment of the exact modeled alternative with:
> - Consistent selected equipment, operating demand and costs.
> - Verified lifecycle accounting.
> - Explicit fuel scenarios.
> - A quantified comparison with published ARIES economics.
> - Each material discrepancy either explained, bounded by a justified sensitivity, or explicitly unresolved with the missing evidence named.
>
> Assess completion honestly. An unsupported material cost that prevents a useful comparison is grounds for a partially answered result, not an invented estimate presented as established.
>
> Process and preservation
>
> - Write the goal contract and persistent round plan before implementation.
> - Use subagents for bounded equipment/cost audits, source checks and independent reviews. Give each a clear ownership boundary.
> - Follow the existing modeling, research, integration and study workflows.
> - Respect source-access restrictions and the exact scope of prior owner exceptions. Do not bypass a restriction through mirrors. Ask before purchasing access.
> - Keep a findings log useful for the write-up: what was reused, what changed, why, numerical consequences and remaining assumptions.
> - Commit coherent increments and preserve unsuccessful attempts.
> - Keep Stellaris, shared behavior it consumes, historical packages and sealed results unchanged. Preserve unrelated workspace edits.
> - Do not reopen the unresolved thermal-source investigation unless a concrete finding is necessary for this economic assessment; surface that dependency rather than expanding scope silently.
> - Finish with an independently reviewed answer, evidence links and replay commands.
> - Leave formal closure to me. No push, merge or external messages.
