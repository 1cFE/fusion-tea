# T-003 v2: Consistent steam-generator admission screening

[AGENT] The named62bar/171°C-feedwater/445°C-steam scenario passes a finite20K minimum temperature-difference screen across the entire modeled steam generator. Consistent water properties replace the conflicting NASA boiling curve. This supports heat admission under stated assumptions, not installed hardware capacity or validation of the retained40.278% efficiency fit. Fresh independent review and canonical-assumption/adoption decisions remain pending. No model implementation occurred.

## Current baseline and source basis

[INHERITED: current entering baseline] Primary results use the fourteen-circuit integrated baseline in `evidence/entering-validation/baseline/baseline_result.json`, executable identity `b032da4a3971979792bc024bf9cd1a41a2d83d340bad5b59ef3e1a9aeaa77236`. Helium is300/500°C. Source heat3125.932277MW plus175.280934MW helium compression gives3301.213211MW at the IHX. Salt shaft work5.675887MW gives3306.889099MW at the steam generator; salt electricity5.974618MW is separately consumed. Salt supply465°C, return to the pump269.664730°C, and return to the IHX270°C remain distinct.

[INHERITED: NASA Figure8-1]62bar,171°C feedwater and42°C condenser motivate a named screening basis. [AGENT]445°C is a proposed20K salt-to-steam hot approach. A separate20K minimum local approach applies to the steam generator only. These are declared design assumptions, not source-established salt-generator limits. Current helium/salt IHX approaches35K/18.785K and its own area check remain unchanged.

[INHERITED: registered NIST WebBook original tables] At6.2MPa, feedwater171°C has726.40880kJ/kg enthalpy; saturation277.73289°C has1225.0579/2782.3705kJ/kg liquid/vapor enthalpies;445°C steam has3287.7317kJ/kg. Two original grids,1K and0.5K, are registered and retained offline. They resolve the earlier source conflict without adopting NASA's roughly255°C boiling plot or its inconsistent duty fractions. Exact source paths, images, query parameters, hashes and calculation are in `physical-research/screening/README.md`.

## Finite heat-transfer result

[AGENT] Assume countercurrent exchange, fixed6.2MPa water pressure, no external heat loss, constant existing1560J/kg/K salt heat capacity and variable water properties. Compute steam flow from `Q_SG/(h_steam−h_feed)` with consistent units; at this baseline it is1291.086375kg/s. Each section duty follows its water enthalpy increment. Salt temperatures follow cumulative heat, giving269.664730→307.693421→426.459421→465°C along the cold-to-hot profile.

| Section | Heat duty, MW | Minimum local difference, K | Required effective UA, MW/K |
|---|---:|---:|---:|
| Economizer |643.799059|29.960531|11.495311|
| Evaporator |2010.625080|29.960531|27.124603|
| Superheater |652.464960|20.000000|9.167013|
| Total |3306.889099|20.000000|47.786926|

[AGENT] The calculation integrates `UA=∫dQ/(Tsalt−Twater)` through the phase-aware variable-property profile. Every interpolation interval is checked; there is no missed interior pinch in that declared interpolation. Independent quadrature agrees within1.71e−13 relative. Halving the property spacing changes totalUA by2.48e−7 relative for445°C. The largest observed midpoint temperature-interpolation discrepancy is0.00241K; this is numerical evidence, not a bound on engineering uncertainty. The hot-end20K equality has no design contingency margin.

[AGENT] NASA's effective-U values would imply about40595.6m² total area only under an explicit source-to-target heat-transfer transfer and an absorbed flow-arrangement correction. Report UA as the primary required capacity. No installed steam-generator area, train arrangement or cost is established.

## Bounded alternatives and efficiency applicability

| Hot approach | Steam temperature | Minimum local difference |20K admission screen|Conditional fit efficiency|
|---|---:|---:|---|---:|
|10K|455°C|10K|Fails|40.5272%|
|20K|445°C|20K|Passes|40.2780%|
|30K|435°C|30K|Passes|40.0252%|

[AGENT] Preserve the10K failure. Required totalUA is50.3143/47.7869/46.3222MW/K respectively. This is not optimization or a part-load map; salt states and baseline heat are held.

[AGENT] At the illustrative42°C sink, salt heat exergy gives a50.4081% reversible ceiling. For445°C, the water gains1418.106738MW exergy, or42.8834% of heat; exchanger irreversibility consumes248.832932MW. The retained fit would yield1331.948184MW before external plant auxiliaries, requiring93.9244% of that water exergy gain to become electricity. It is below both necessary ceilings, but this demanding transfer is not validated by the admission screen. Kovari's pressure, regeneration, sink and internal-work assumptions have not been matched to this NASA-inspired basis. Preserve the fit's384–642°C domain, literal273 convention and existing zero-divertor-penalty disclosure; claim no validated part-load efficiency.

## Proposed implementation boundary

[AGENT] If released, bind conversion temperature to salt supply minus an explicit positive hot approach; publish the segmented admission results and separate flags for physical screening, source-fit applicability and installed capacity. Recompute electricity and power-scaled costs without tuning rates. Keep primary/salt work accounting once and the distinct helium/salt IHX inCAS220200. Salt/steam-generator ownership remainsCAS23; inclusion in its retained turbine coefficient is unverified, so missing price remains disclosed. This preserves the existing steam Rankine/HITEC concept and P2 target. Whether the conditional fit and named assumptions suffice for comparison adoption remains owner-held; the screen does not settle it.
