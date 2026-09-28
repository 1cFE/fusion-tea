# Stellarator study evidence for the execution explainer

This is an agent-authored presentation reading of retained native study records, prepared on 2026-09-19. It does not modify those records, run new cases, or claim an independent scientific audit. Numerical extracts retain candidate identities and source hashes in [study-evidence.json](study-evidence.json). The extraction script reads only the named study directories.

## Recommended figures

[AGENT] Use the 17 September radius/current map as the main study figure. It has one fixed configuration, a clear band of passing samples, adjacent failures and electricity cost. Pair it with the 15 September three-case magnet comparison if a second figure is useful. Together they explain why repeatedly evaluating a connected engineering model matters: satisfying the current calculation can increase material inventory, the required space and cost; more space can then violate a different constraint.

[AGENT] Date both figures and label the quantities as conditional model results. These are historical model snapshots. Later breeding and cost-model work changes their interpretation. Neither plot represents the latest complete plant estimate, a demonstrated device, or an economic optimum.

## Figure 1: sampled constraints and electricity cost

**Plot data:** [feasibility-cost-map.csv](feasibility-cost-map.csv). It contains all 256 map locations, including failures. `R_m` and `current_MAturn` are the independent axes; `classification` distinguishes 44 passes, 210 ordinary failures and two invalid power accounts. `LCOE_dollars_MWh` is the recorded output of `stellarator_09__stellaris__lcoe_calc__lcoe`. The 44 passing samples span $149.765148–152.356509/MWh. Do not use the invalid-account costs as economically interpretable estimates.

[AGENT] A two-panel figure works well: the same radius/current locations on both panels, with constraint outcome on the left and cost on the right. For the cost panel, color the 44 passing samples and retain failed/invalid locations in a muted style. This keeps cost conditional on the stated model checks without concealing rejected candidates. Plot points rather than an interpolated filled feasible region. The two invalid-account cases need their own marker or legend category. An alternative is one scatter plot with color for passing-case cost, crosses for failed screens and squares for invalid accounts.

The map holds minor radius at 1.4908855301929713 m, peak electron density at 4.8924678194274265e20 m⁻³, peak ion temperature at 14.035595515748351 keV, radial exterior allocation and transverse clear cavity at 0.65 m each, and cooling circuits at 18. Current-driven inventory uses a 1.01 multiplier, meaning physical conductor reserve. Density and temperature profile exponents remain 0.35 and 1.2. Full-precision explicit fixed inputs are in the metadata JSON; the remaining defaults are retained in the source record's `preparation/resolved-defaults.json`. The extractor verifies that only radius and coil ampere-turns change among these 256 native input dictionaries.

The entire study has 334 selected native cases, of which 103 pass; the map is a 256-case fixed-configuration subset, not the complete campaign. Its separate local-neighborhood checks have 43 passes among 45 perturbations. These are different cohorts and should not be interchanged in a caption. Native outputs and original per-constraint verdicts are joined by candidate ID; the presentation extract verifies all 20 verdicts and the account classification rather than inferring feasibility from a plotted margin.

**Recorded limits:** Passing means the twenty screens implemented in that executable passed, and the power account is valid. The held achieved breeding ratio is 1.074 while the calculated fuel requirement is 1.190; passing the then-authored 1.05 floor does not establish tritium self-sufficiency. Magnetic topology/shape, conductor field-angle transfer, stress/strain proxies, divertor deposition and cooling qualification remain conditional. The reported anchor field exceeds the approximate 24 T extent of the cited conductor measurements. Installed cooling equipment, larger transverse accommodation and complete manufacturing were not fully priced in this snapshot. Prices also retain mixed monetary bases.

**Possible caption:** “A 256-point radius/current sweep in the 17 September stellarator model. Forty-four samples pass all twenty then-implemented screens with a valid power account; 210 fail a screen and two have invalid power accounts. Color shows conditional electricity cost for passing samples. Other inputs are held fixed. These sampled results are not a qualified plant design or a complete cost estimate.”

Sources within the retained study:

- [Record, including question, axis framing, verification scope and limitations](../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/record.md).
- [Study report, including map counts, fixed assumptions and cost limits](../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/report.md).
- [Original plotted coordinates and classifications](../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/map-data.csv).
- [Native cases with inputs, output channels and exact verdicts](../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/native-cases.json).
- [Analysis quantities and signed margins](../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/analysis.json).
- [Executable and study snapshot](../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/snapshot.json), package commit `d53d6ec5748442833ff44bc179bb988bce726486`, integration pin `6e427038e8515501e9c42c39823f85e3b0bcbd9f54f830b2779a792851f02551`.

## Figure 2: satisfying one constraint exposes another

**Plot data:** [magnet-sizing-comparison.csv](magnet-sizing-comparison.csv). These three matched reference cases belong to the same 15 September native executable. They are not a comparison between different model versions. All hold major radius at 12.7 m, minor radius at 1.3 m and coil ampere-turns at 15.4 million. The first change enables current-driven sizing with a 1% physical conductor reserve. The second increases the independently allocated radial exterior and transverse cavity. The material-performance factors and 24.9 T field ceiling stay unchanged.

| Reference case | Tape length, million m | Priced magnet subtotal, $billion | LCOE, $/MWh | Current | Fits cavity | Peak field |
|---|---:|---:|---:|---|---|---|
| Original inventory and allocation | 36.578571 | 1.707443 | 144.747431 | Fail | Fail | Pass |
| Current-sized inventory, original allocation | 77.884488 | 2.552054 | 163.194229 | Pass | Fail | Pass |
| Current-sized inventory, enlarged allocation | 82.372011 | 2.695285 | 166.743923 | Pass | Pass | Fail |

The original radial exterior/transverse cavity is 0.30/0.40 m. The enlarged choice is 0.60/0.60 m. Casing walls occupy 0.025 m on each radial side, so the clear radial cavity is the exterior minus 0.05 m. The required clear dimensions after current sizing are 0.535309 × 0.548441 m at the original allocation. Larger allocation changes the coil geometry and raises peak field from 24.900000 to 25.297340 T, which exceeds the unchanged 24.9 T ceiling. Its required clear dimensions change to 0.537810 × 0.551005 m. All three cases also violate the divertor criterion and fail the full plant screen.

[AGENT] Show three bars for conditional LCOE, with a compact current/fit/field status row below each. A second material-quantity row can show purchased tape length. The field failure after enlarging the allocation is the point: the same connected calculation updates every downstream consequence. Do not color the third case as fully feasible just because current and fit pass.

The full study has 347 unique native cases. Its 324 default-performance candidates produce no all-screen pass. The one all-screen pass in the whole study is a historical 30 T/orientation-factor-3 control outside the main assumptions; it is not in this extract. The three selected cases therefore make a clearer physical comparison than ranking every row together. Manufacturing, structural and local conductor qualification gaps remain. Mixed monetary bases and unresolved manufacturing scope prevent reading the subtotals as complete procurement quotations.

**Possible caption:** “Three matched reference cases from the 15 September stellarator model. Purchasing enough conductor to meet the current screen raises tape inventory and cost. Enlarging the allocated casing makes that conductor fit, but changes geometry enough to exceed the peak-field limit. All three still fail the divertor screen. The figures are conditional estimates from that model snapshot.”

Sources within the retained study:

- [Study record](../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/record.md).
- [Native cases](../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/results/native-cases.json), candidates `c0000`, `c0005` and `c0007` under that study ID.
- [Analysis and report aliases](../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/results/analysis.json), aliases `reference`, `reference-sized` and `reference-accommodated`.
- [Executable and study snapshot](../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/snapshot.json), package commit `a8589d6b5aebbb42c525f7bab9a036a474fc8e6b`, integration pin `0a1c038663c848e11cff933215a8d15eb96b6650319003b9cf092ecbbc40e52c`.

## Why the newer records matter

The later [installed-cooling study report](../../../exploration/stellarator_e2e/studies/20260918-installed-cooling-equipment-costs/report.md) retains the selected eighteen-circuit case as three explicit modes. Its old-allowance LCOE is $150.429542/MWh, the equipment-cost-only result is $309.554789/MWh, and adding the intermediate salt-pump energy effects gives $310.632663/MWh. The same report now records a breeding-screen failure at that selected point. All 34 study cases fail at least one whole-plant predicate. These facts prevent presenting the older map as current demonstrated feasibility or its cost as a complete estimate.

The subsequent [facilities study report](../../../exploration/stellarator_e2e/studies/20260918-layout-based-facilities/report.md) compares the same retained eighteen-circuit context with the old and new building account: $310.633 to $314.182/MWh. It adds five facility checks. Twenty-eight of its 48 cases pass all five facility screens, but no case passes every plant predicate. The account selector comparison holds physical/layout quantities and all 25 predicate statuses fixed. It is a cost-scope comparison, not physical design improvement.

[AGENT] Keep this later-work qualification near the historical figures in the article. A sentence is sufficient: “These are snapshots of the model at the time; later work on breeding, cooling equipment and facilities added constraints and substantially increased the estimated cost.” The article can still use the map to demonstrate execution and search without turning a historical model result into a current engineering claim.

The earlier [winding-pack fit record](../../../exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/record.md) was considered but not selected. It contains 116 unique cases: 45 pass the old eighteen screens and twelve also pass the new fit screen. Its cheapest retained pass relies on an increased current-density assumption and extrapolated 30 T envelope, with absolute current margin still unknown. The joint-sizing study resolves the current/fit coupling more directly and avoids using those historical passes as the main illustration.

## Study runner capabilities

The current study runner evaluates grids and prepared candidate lists. An external optimizer can call the same prepared evaluator, but adaptive optimization within the native study runner requires further implementation. The article's examples demonstrate retained candidate evaluations, not a native adaptive optimization run.

## Held inputs for the radius–current map

For the illustrated slice, minor radius is held at about 1.491 m, peak ion temperature at 14.036 keV, and peak electron density at 4.892 × 10²⁰ m⁻³. The scenario also holds eighteen representative helium loops, 0.65 m radial allocation and transverse cavity, and a 1.01 conductor-inventory multiplier. The [study record](../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/record.md) preserves the full-precision inputs and other held assumptions. The map's feasibility and cost results are conditional on those settings.

## Reproduction and verification scope

Run `.codex-test/run python docs/write-up/sysml-codegen-assets/extract_study_evidence.py` from the repository root. It regenerates the two CSV files and metadata JSON from the retained source artifacts. Assertions verify candidate joins, 256 unique map coordinates, the 44/210/2 classifications, twenty native predicates per map case, unchanged explicit fixed inputs, native LCOE equality, and each magnet case's native LCOE and field values. The metadata includes SHA256 hashes of every JSON/CSV read by extraction. This is presentation-data verification; it does not repeat the original model validation or confer physical qualification.
