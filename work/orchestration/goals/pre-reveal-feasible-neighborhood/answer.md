# Pre-reveal feasibility: a sampled passing neighborhood

[AGENT] **Yes. The unchanged model has a verified sampled neighborhood passing all twenty implemented screens with a valid power account.** This does not establish a buildable stellarator. The result uses the permitted, separately labeled 1.01 conductor-inventory scenario; the exact r2 multiplier-1.0 controls keep their failures. [Independent result and final-round review](evidence/independent-review.md) pass this bounded conclusion. [OWNER] Formally closed on 2026-09-17: “ok please close the goal”. See the closure entry in [trail.md](trail.md).

Of 334 deliberately selected native cases,103 pass. Around the chosen anchor,43 of 45 tested perturbations pass. There are passing points on both sides of all seven continuous design axes, at both adjacent integer loop counts, and at all sixteen tested combined perturbations. The two failed neighbors are retained: reducing major radius by 2% fails peak field; increasing it by 2% fails divertor heat. Passing radius changes of±1% show that this is more than an isolated boundary point. These samples do not certify every point in a box.

## Exact configuration and margins

| Choice | Anchor |
|---|---:|
| Major radius |11.2517482167 m|
| Minor radius |1.49088553019 m|
| Coil ampere-turns |12.2171844080 MA-turn|
| Peak electron density |4.89246781943 ×10²⁰ m⁻³|
| Peak ion temperature |14.0355955157 keV|
| Radial exterior allocation |0.65 m|
| Transverse clear cavity |0.65 m|
| Representative helium loops |18|
| Current-sized conductor inventory |1.01 multiplier|

The fuel-density/temperature profile exponents are held at 0.35/1.2. Plasma closure, cooling, cycle and calendar calculations are live. Material performance, transport/radiation assumptions, calibration, installed heating, financial inputs and acceptance limits are unchanged. Full-precision overrides and all held defaults are retained in the [native record](../../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/record.md).

| Screen margin | Anchor | Minimum among the 43 passing tested neighbors |
|---|---:|---:|
| Peak field below 24.9 T |0.513786 T|0.026062 T|
| Divertor peak below 10 MW/m² |0.291669 MW/m²|0.031533 MW/m²|
| Installed heating headroom |12.894671 MW|3.358450 MW|
| Positive auxiliary demand |37.105329 MW|28.140226 MW|
| Local pack/cavity fit |125.032 mm|112.149 mm|
| Per-loop flow headroom |68.503 kg/s|58.343 kg/s|
| Current operating-fraction margin below 0.8 |0.00792079|0.00792079|

The smallest field and divertor margins are narrow. The current reserve buys physical conductor and propagates its procurement, dimensions and fit consequences; it is not improved material performance. At this same anchor with multiplier 1.0, the raw native current predicate fails on its near-zero signed margin. That result has not been promoted to a pass.

## What the two-dimensional map means

![Fixed-configuration feasibility map](../../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/feasibility-map.png)

The map holds minor radius, density, temperature, accommodation, loops and inventory at the reported anchor settings. Its 256 evaluated locations contain 44 valid passing points,210 ordinary failing points and 2 invalid-power-account points. All are native evaluations. No domain refusal occurs on this local slice; the broader screen's 121 refusal calls are retained separately. Colored points establish sampled outcomes, not a filled feasible area. The r2 marker is a projection whose other inputs differ. [Plot data](../../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/map-data.csv) and [standalone SVG](../../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/feasibility-map.svg) are retained.

The simultaneous limits explain the band. Smaller major radius at held current raises peak field. Larger radius reduces the available field and changes confinement/heating, eventually exceeding divertor load or installed heating. Changing density and temperature alters fusion and target power as well as auxiliary demand. Matched native cases make these dependencies explicit:

| Restore one anchor choice to its r2 value | Result |
|---|---|
| Major radius 12.7 m |109.895 MW auxiliary demand; divertor, wall-load and heating failures|
| Minor radius 1.3 m |108.525 MW auxiliary demand; heating failure|
| Coil ampere-turns 15.4 MA-turn |30.739 T peak field and negative auxiliary demand; field/burn failures|
| Peak density 5.06 ×10²⁰ m⁻³ |10.151 MW/m² divertor peak; divertor failure|
| Peak ion temperature 14.63 keV |10.274 MW/m² divertor peak; divertor and wall-load failures|

This is why the earlier fixed-operating-assumption negative search did not settle the current question. The new result changes geometry and actual operating choices under the exact-profile convention. It does not revise that earlier search or tune physical coefficients.

## What remains uncertain

The model holds topology, shape and transport assumptions while geometry changes; it does not solve a new magnetic equilibrium or qualify a coil design. The anchor's 24.386 T peak field exceeds the cited conductor measurements' approximate 24 T extent. Local field-angle/construction transfer, structural and manufacturing qualification, divertor transport and radiation deposition, cooling equipment/layout, calendar reliability and the source-water/model-helium correspondence remain conditional.

The breeding gap is material: held achieved TBR 1.074 passes the authored 1.05 floor, while the calculated requirement is 1.190. Passing this predicate does not demonstrate tritium self-sufficiency. The chosen 18 loops are an explicit scenario, not a proved equipment optimum; matched 14-loop and neighboring 17/19-loop cases also pass the represented screens.

The declared search bounds are engineered exploration around the admitted reference, not source-qualified validity intervals. The campaign screened 835 unique coordinates in 837 oracle calls, including 121 refused calls. It performed 335 unique native evaluations:334 selected cases plus one baseline. Selection favored informative cases and passing neighborhoods, so 103/334 is not an estimate of the feasible fraction of design space. No global feasibility or domain-exhaustion claim follows.

## Cost meaning, verification and reveal recommendation

Anchor modeled net output is 1010.112 MW and conditional LCOE is**$150.43/MWh**. The represented 18-loop system implies 36 circulators,18 heat exchangers and 3013.915 MW total exchanger duty, or 167.440 MW per loop. These are model equipment requirements, not qualified ratings or installed quotes. Complete manufacturing, larger accommodation and added cooling installation remain unpriced. Mixed-year cost inputs and held financial/calendar assumptions remain. The LCOE is neither a complete plant price nor a demonstrated economic optimum.

All 75,484 mapped scalar comparisons pass the retained relative/absolute 1e-9 check. Six strict-relative near-zero current differences and three native/oracle current-predicate disagreements remain explicit, all at multiplier 1.0. The generic strict verifier stops on the unchanged r2 control; its refusal is retained, not relabeled a pass. All 6,680 predicate reconstructions from native operands agree. Sixteen native scalar channels remain outside the independent oracle map. Software agreement establishes implementation consistency within that scope, not physical qualification. Native r2 forward and separately Table 5-conditioned controls reproduce their frozen 242 output values and 20 raw verdicts exactly.

[AGENT] **Proceeding to the already-prepared conditional ARIES comparison remains worthwhile.** We can now show a separate sampled model-screen neighborhood and explain its limits. Keep the published r2 package and comparison rules unchanged; this study cannot retrospectively improve its result. ARIES remains sealed. Reveal and any replacement freeze remain owner decisions.

Native evidence: `exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood@1394d43d1cfd362dfa608225455c823bf977e632`; snapshot SHA256 `faaae353f5d5f7cb91c39ae0d87d65714fffae2c34f93d2e4e846c07031a3c13`. The [executor reading](../../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/synthesis.md) is explicitly authored by the study executor.
