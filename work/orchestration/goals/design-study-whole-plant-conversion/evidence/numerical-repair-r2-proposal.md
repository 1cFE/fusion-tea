# R2 numerical diagnosis and bounded proposal

[AGENT] 2026-09-27. Status: native diagnosis and independent high-precision adjudication complete; focused review remains required before changing the oracle. No native-body repair is justified. The native package, bodies, oracle and comparison tolerances are unchanged.

## Finding

The observed cooler discrepancy does not establish a native solver defect. The native solve reaches adjacent binary64 outlet temperatures and selects the endpoint with the smaller conductance residual. The independent oracle currently stops Brent's method at an absolute temperature tolerance of `1e-11` K. The failed point has a minimum approach of only `1.42318e-4` K, where its conductance changes rapidly with outlet temperature. The discrepancy is consistent with insufficient oracle root accuracy at that point.

The full forensic census is [verification-failure-r1/discrepancies.json](verification-failure-r1/discrepancies.json): 2,496 cases, 2,975,232 scalar comparisons, 312,000 predicate comparisons, 11 scalar mismatches on five cases, zero predicate mismatches and zero evaluation errors. Three scalar mismatches belong to the cooler case; eight are cryogenic margins on the four extremely close capacity-bracket points. Failed verification remains failed.

## Native cooler reproduction

The exact retained case is `gas-favourable::gas-q2500-m2500-r1.8-ua40-40-60`, candidate `20260927-design-study-whole-plant-conversion:c1868`. Inputs and outputs are in the failed record's `results/cases.json`; the executed body is preserved in its `results/sources/exploration/whole_plant_conversion/bodies/component_alternatives_thermal/finite_water_cooler_impl.py`. The live body inspected is `exploration/whole_plant_conversion/bodies/component_alternatives_thermal/finite_water_cooler_impl.py:11–60`; its installed-body SHA256 is `0aa69c46492edb2db43688832ba16d9c19065928c4a59e22ce5201c69c9376d4`.

A read-only local probe obtained actual calculation operands from the retained complete point and native pipeline bindings, called the unchanged body, and captured its final local bracket. All 18 returned outputs match the original native receipt exactly. The retained [native probe](verification-failure-r1/native-diagnosis/native-cooler-diagnosis.py) and [complete diagnostic return](verification-failure-r1/native-diagnosis/native-cooler-diagnosis.json) preserve the reproduction. The decision-carrying inputs and observations are also retained below.

| Operand | Native value |
|---|---:|
| Gas inlet K |312.2683428927496|
| Gas outlet K |308.15|
| Gas heat into fluid MW |−53.466386605122175|
| Installed UA MW/K |60|
| Reservoir water °C |25|
| Pump head m |20|
| Pump / motor efficiencies |0.8 / 0.95|
| Flow rating kg/s |100000|
| Electric rating MW |30|
| Duty rating MW |2000|

| Native observation | Value |
|---|---:|
| Water inlet after pump °C |25.06171436763265|
| Final lower outlet °C |39.11820057461562|
| Final upper outlet °C |39.11820057461563|
| Final bracket width K |7.105427357601002e-15|
| Adjacent binary64 endpoints |true|
| Lower endpoint UA MW/K |59.99999999997155|
| Upper endpoint UA MW/K |60.00000000023905|
| Selected endpoint |lower|
| Selected UA residual MW/K |−2.845013113983441e-11|
| Minimum profile approach K |0.00014231813401721638|
| Water flow kg/s |909.9133017969382|
| Pump electricity MW |0.23482108634386692|
| Energy residual MW |3.969047313034935e-15|
| Bisection iterations |52|

## Original equations and conditioning

[INHERITED: native body and reviewed WI-096 design] Let `Q` be the positive gas cooling duty in MW, and use the retained piecewise-linear liquid-water enthalpy table `h(T)` in kJ/kg. The pump adds specific electric work `e = g H/(eta_p eta_motor)/1000`, giving `h_a = h(T_reservoir)+e` and `T_a = T(h_a)`. For a trial outlet `T_b`, water flow is `m = 1000 Q/(h(T_b)-h_a)`.

The native calculation traverses transferred heat `z` in MW. Gas temperature is `T_g(z)=T_g,cold+(T_g,hot−T_g,cold)z/Q`; water temperature is `T_w(z)=T(h_a+1000z/m)`. The profile approach is `G(z)=T_g(z)−T_w(z)`. Within each water-property segment the gap is linear. The exact segment contribution is `(z_b−z_a) log(G_b/G_a)/(G_b−G_a)`, with the equal-gap limit `(z_b−z_a)/G_a`. Native uses `log1p` and `math.fsum`, and solves the sum equal to the selected UA. Nonpositive gaps refuse evaluation; unbracketed positive-duty offers retain failed receipts.

The native root is bracketed from `T_a+1e-7` to `min(T_g,hot,60°C)−1e-7`. It continues until the bracket endpoints are adjacent representable floats and selects their smaller absolute UA residual. The `1e-7` inward bounds are retained numerical-domain policy, not a physical approach requirement or a new hardware choice.

At this point the gas hot end is `39.11834289274964°C`, so the water outlet lies within `0.00014231813401721638 K` of it. A symmetric diagnostic difference of the unchanged native conductance function at outlet offsets of `±1e-10 K` gives `dUA/dT_b ≈ 37792.2432 MW/K²`. This is a local sensitivity check, not a new model equation. A `1.96e-12 K` root error therefore corresponds to about `7.4e-8 MW/K` of conductance error, matching the observed discrepancy's scale.

The stock comparison demands relative error below `1e-9` for the small minimum-gap output, with zero absolute tolerance. Its temperature-error budget is about `1.42e-13 K`. The `1e-8 MW/K` absolute tolerance on the UA residual gives about `2.65e-13 K` of outlet-error budget at this derivative. Both are much tighter than the oracle's declared `xtol=1e-11 K`. Merely increasing native iteration count would not help: its final bracket is already one binary64 step wide.

## Independent-oracle question

`exploration/whole_plant_conversion/oracle_thermal.py:107–171` independently integrates over water-temperature segments and uses a Brent root with `xtol=1e-11`, `rtol=1e-14`. Its reported UA residual is `−7.41399830417322e-8 MW/K`, whereas native is `−2.845013113983441e-11 MW/K`. Independent adjudication in [verification-failure-r1/high-precision-cooler.json](verification-failure-r1/high-precision-cooler.json) confirms identical native/oracle intermediate input maps. Its 80-digit reference outlet is `39.11820057461559871919686°C`. Native differs by `+2.20046e-14 K`; the original oracle differs by `−1.93909e-12 K`. The diagnostic independent Brent candidate uses `xtol=5e-324` and `rtol=4*epsilon=8.881784197001252e-16`, returns a UA residual near `−2.835e-11 MW/K`, and passes all 1192 scalar and 125 predicate comparisons for the exact case under unchanged rules. This confirms an oracle stopping-accuracy defect, not a native-body defect.

## Proposed bounded disposition

1. Keep the failed original record and exact `c1868` input map. Keep the native cooler body and package unchanged; independent high-precision evidence supports their current result.
2. Request focused review of an oracle numerical-accuracy correction only: retain its independent water-temperature equations and Brent method, but tighten outlet convergence enough to satisfy its own published output contracts at the demonstrated near-pinch condition. Validate the returned UA residual and gap against the high-precision reference. Do not copy native arithmetic, loosen comparison tolerances, discard this offer, or force oracle outputs to equal selected UA.
3. Rerun the exact failing point and the complete retained point set under the unchanged stock numerical/predicate checks. Re-run legacy controls because the independent oracle's numerical behavior changes, even if model science does not. Record any generated comparison-identity change honestly; the native executable need not change if only verifier accuracy changes.
4. Treat the cryogenic brackets separately. The four original cases have margins about `±0.0030726 W`; different valid binary64 sum orderings produce `7.3e-12–1.46e-11 W` discrepancies. Those are relatively larger than `1e-9` only because the reported margin is so close to zero. The coordinator's proposed wider symmetric bracket is a study-resolution correction, not a physics or tolerance change. The actual proposed replacement uses offsets of `±0.01 W/m³` around the same independently calculated threshold, giving margin magnitudes about `3.0726 W`. The [conditioning probe](verification-failure-r1/conditioning-probe.json) supports this spacing under the existing tolerance. Preserve all four original closer points and their failures; review the replacement bracket and re-evaluate it natively.

No scientific conclusion or ranking is released by this proposal. Its purpose is to identify the smallest justified numerical correction while retaining failed evidence and the exact supported/failed engineering semantics.
