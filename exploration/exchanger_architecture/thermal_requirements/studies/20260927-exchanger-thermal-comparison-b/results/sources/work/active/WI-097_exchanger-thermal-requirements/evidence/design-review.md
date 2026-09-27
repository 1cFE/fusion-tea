# WI-097 independent design review

2026-09-27. [AGENT] Continuing independent reviewer. Reviewed the amended spec, design, both retained development probes, the delegated thermal contract and `r3-cost-boundary.md`. Reused the original-page source review. No production code or main study was changed or executed.

**Verdict: FINDINGS. F1 requires correction before implementation of the oracle/failure-state path.** The controlled physics, offered-equipment boundary and matched passing development evidence are otherwise accepted. The owner's delegation resolves the earlier approach decision; no new owner gate is introduced.

## F1 — Preserve finite transfer when a terminal gap rounds to zero

The independent-oracle paragraph currently treats nonpositive terminal differences as non-transferring/failing domains. This combines two different situations: a genuinely absent hot-to-cold driving temperature, and a positive but extremely small terminal difference lost when two approximately equal float temperatures are subtracted.

The first development probe already contains 249 finite-transfer branch states whose calculated cold-terminal gap rounds to zero or a tiny negative number. For example, original inventory at 1650 MW source, series flow 1100 kg/s, transfers 276.5 MW in the divertor with bypass 0.6172088525331203 and hot-terminal gap 229.78786290651692 K, but reports cold gap 0.0 K. This candidate legitimately fails the 30 K requirement. It must remain an executed finite-transfer failure with verifiable control and energy states.

Required correction: specify log-domain or sufficiently precise LMTD reconstruction for both near-zero hot and cold gaps; preserve finite transferred duty, bypass and temperatures; compare rounded native outputs using declared numerical tolerances. A rounded zero must not make the oracle substitute zero heat, mark an active state undefined, or refuse the whole case. Keep genuinely zero duty/UA/positive-drive absence as separate domains. Add a saturated-gap original-inventory fixture to acceptance evidence, alongside ordinary positive-gap and equal-gap fixtures. This changes numerical verification behavior, not the engineering minimum or equipment selection.

## Physics and closure assessment

- `H_required = R_target + Q_delivered/C_total` uses full source duty including recovered pump heat once. It remains fixed when an inadequate exchanger accepts less. With bypass, the calculated mixed return is `H_required − q/C_total`; its excess above target equals unmet duty divided by total heat-capacity rate. That is an honest failing source-loop state, not a secretly enforced return.
- The bypass changes active primary flow and recomputes effectiveness using full installed UA. Actual cold-terminal temperature is the active HX outlet, and actual hot-terminal temperature uses the branch secondary outlet before network mixing. Neither mixed return nor mixed turbine inlet substitutes for an exchanger terminal.
- The accepted-heat function is continuous across capability saturation. Each passive stage's secondary outlet is a nondecreasing function of inlet, with slope between zero and one; the network's weighted mixing preserves that property. The recuperator feedback has gain at most `e*k < 1`. These relationships support the proposed bracketed cycle closure and prevent a hidden positive-feedback branch. The endpoint bracket from compressor outlet to maximum required hot temperature is sound in the stated domain.
- An over-cap hot state or required bypass beyond its supplied bound remains explicitly inadmissible. Its computed heat/electricity is diagnostic and cannot enter passing economics. Native implementation must preserve these distinctions, state guards and all accepted/unmet heat consumers.

## Development evidence independently checked

Using separate LMTD root equations, I reconstructed active flow/bypass and cold-terminal gaps for every passing branch in both probes: 2310 branch states across 73 first-probe and 697 follow-up passing cases. Maximum discrepancy was 4.4e-11 K or dimensionless fraction. All 770 passing cases also close full-duty cycle energy and topology mixing within 9.1e-13 MW or K. These are development checks, not complete equipment/economic qualification.

The original-inventory failure proof is correct: finite full-UA operation with both gaps at least 30 K requires `Q >= UA*30`. Original divertor UA 50 MW/K therefore needs at least 1500 MW, but its fixed return, flow and hot cap allow only 329.7555 MW. Primary bypass cannot repair that contradiction. The proposed smaller inventories have actual passing probe pairs and are not manufactured by changing a requirement threshold.

## MR-7 and costs

Compliant in the proposed scope. Areas, prices, caps and ratings are supplied; solved bypass is an operating control; area selection remains outside the physical model. Main offers A and B both book 174,977,100 USD2004 for the three exchangers. I checked the native price-factor normalization and linear sensitivities, 30,329,364 and 44,327,532 USD2004. Ratios 0.24/0.24/0.04 and 0.36/0.36/0.04 must retain extrapolation flags. The retained budget is an agent price assumption, not a quote or proved procurement bound.

The separate cost boundary correctly includes potential additions for both architectures and explains why a common unknown control cost does not cancel from LCOE at different outputs. Preserve that two-sided formulation in reporting. No pump-power credit follows merely from lower active HX flow. Explicitly retain the assumption that U is held constant despite changing active flow; the existing model contains no U-versus-flow law. Conductance uncertainty therefore remains material to the eventual comparison.

## Release after correction

Once F1 is corrected, the isolated controlled package may be implemented. Required release evidence remains the design's legacy replay, native partial-duty failures, independently verified new channels/predicates, explicit purchase invariants, boundary fixtures and integration checks. The development probes do not waive these obligations. The refined study may rank only cases passing the complete thermal/equipment contract and must retain resolution uncertainty and failed candidates.

## Corrective recheck — 2026-09-27

**Final design verdict: PASS. F1 resolved; implementation may proceed.** The amended oracle section explicitly distinguishes rounded terminal cancellation from absent physical drive, requires log-domain or high-precision reconstruction with precision/convergence evidence, and prohibits changing finite duty, state validity or cycle outputs merely because a gap rounds to zero. Mandatory acceptance now includes original-UA saturated-gap cases and the equal-capacity limit with neighboring points. This is the requested correction; physical thresholds remain unchanged.

The design now explicitly states constant U under changed active primary flow, with conductance uncertainty retained as a conditional assumption. Its refined-study handoff matches the coordinator's tighter contract: 0.1 kg/s flow and 0.001 split brackets, followed by halving checks against 0.2 MW and 0.1 USD2004/MWh. These changes preserve the reviewed physical and procurement scope.

The passing verdict approves this implementation design, not unbuilt executable behavior or a study winner. The native acceptance and integration obligations above remain required before the main study.
