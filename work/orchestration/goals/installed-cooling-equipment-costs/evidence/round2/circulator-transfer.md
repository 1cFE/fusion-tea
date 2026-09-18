# T-006 helium circulator transfer evidence

[AGENT] Three original sources now establish two separately priced helium circulator references, package boundaries, and a manufacturer-derived conceptual capacity-scaling practice. This replaces the previous absence of any inspectable helium price anchor. It supports review of a conditional conceptual estimate. It does not establish a validated large-machine curve, a statistical cost bound, a replacement interval, or a model implementation release.

## Native evidence

Request: `knowledge/research/requests/REQ-COOL-CIRCULATOR-TRANSFER.json`. Run: `knowledge/research/requests/runs/REQ-COOL-CIRCULATOR-TRANSFER/20260918T220746639517/`. Prospective bounds:15 individually prelogged searches,3 captures,45 substantive calls; administrative completion waits excluded from the last bound. Twelve searches were executed. Three full original PDFs were captured and registered. No prior exhausted exact-title query or broken Round1 download was repeated. No external messaging, paid access, model changes or domain insights occurred.

All retrieved originals were screened in full for ARIES-CS spelling variants, barred host and sealed-paper stems before content inspection. No match occurred and no barred content was encountered. Screen plus subject-context review remains a limited admissibility check, not proof against unnamed derivatives. Critical quote, conditions and scaling pages were inspected as rendered images; retained copies are in `evidence/round2/circulator-images/`.

| Registered original | Original URL | Raw SHA256 |
|---|---|---|
| `knowledge/sources/bnl_nureg_cr1006_preliminary_design_study_of_a_large_scale/` | `https://www.osti.gov/servlets/purl/5714353` | `c28be58088c7153bbe95da784bb735dc3cb740812e806af594031543c4f41952` |
| `knowledge/sources/ornl_fedc87_1_cooldown_of_the_compact_ignition_tokamak_1987/` | `https://www.osti.gov/servlets/purl/5706252` | `600c6ad7048753e0b7932ee3e6e9fa9772c5e6254666abad68fe20739fb427d8` |
| `knowledge/sources/general_atomic_ga8439_reactor_arrangement_studies_for_a/` | `https://www.osti.gov/servlets/purl/4785937` | `b8baa2fa5b4098bbc7a5c2a22540927b8939aae3093126aedeb560af0c3b4cfb` |

## Brookhaven: directly relevant pressure ratio and package definition

[INHERITED: BNL NUREG/CR-1006, August1979, §2.5 printed6/PDF15, image checked] Mechanical Technology Incorporated proposed a single-stage centrifugal helium compressor with gas bearings, hermetically enclosed in a stainless-steel ASME SectionVIII vessel, and a helium-cooled140hp,24000rpm induction motor. Stainless grade and casing design temperature are not specified. Quoted inlet conditions are735psia,1000°F and600actualft³/min; discharge760psia. These correspond to5.068MPa inlet,5.240MPa discharge,172.37kPa pressure rise,810.93K inlet and pressure ratio1.034014. This establishes that centrifugal helium circulation at such a low ratio is a real engineering class. Seider's description of compressors being widely used above ratio2 is therefore not a universal validity prohibition; service transfer still requires justification.

| Quote component | Original USD | Scope |
|---|---:|---|
| Circulator and motor |550000|Gas-bearing machine and140hp motor within the quoted hermetic concept|
| Power supply |110000|Separate from machine/motor|
| Fabrication, assembly, testing and delivery total |660000|Includes preceding two rows; do not add them again|
| Engineering design, layout, detailed drawings and report |130000|Separate cost-plus-fixed-fee estimate, about6months|

[INHERITED: same source §6 printed21/PDF30, image checked] Costs are budgetary finished-component costs delivered to BNL. They exclude assembling the loop and operating/maintenance labor, engineering, administration and overhead. The quote is not a completed purchase or a field-installed total. No magnetic bearing is included; the quote specifies gas bearings. No separate seal, isolation valve or catcher-bearing line is given, so those target requirements cannot be claimed included by name.

[INHERITED: same source references1–2 printed24/PDF33] The vendor proposal is MTI G9-567, dated December15,1978; the accompanying temperature discussion is a December14,1978 telephone conversation. Use late1978 quote provenance. The registration caveat's provisional report-date assumption was written before checking these references and is superseded by this explicit date. The report gives dollars and US vendor/customer context, but does not state an independently rebased constant-dollar index year. Any normalization should identify its1978-index convention and not present that convention as a reported rebasing.

[INHERITED: §2.5] MTI attributed substantial cost to the motor size and pressure vessel enclosing it, and estimated less than10% savings from lowering inlet temperature from1000°F to200°F while retaining the same compressor concept. This supports temperature sensitivity within that quoted design family. It is not a universal helium-temperature correction or proof of target motor insulation suitability.

### What the original pressure scaling actually says

[INHERITED: BNL §6.2 and Tables5.1/6.1, printed20–22/PDF29–31, image checked] For the low-pressure alternative, the authors assumed half the circulator/motor cost was material and scaled that fraction with operating pressure and pumping power raised to0.28. The other half stayed fixed. A faithful algebraic reconstruction is:

`C_alt = C_nom * [0.5 + 0.5*(p_alt/p_nom)*(W_alt/W_nom)^0.28]`.

With source values `C_nom=550000`, `p_alt/p_nom=50/735`, `W_alt/W_nom=115/50`, this gives298621USD, matching the rounded300000USD alternative table. The corresponding source power-supply estimates are110000 and140000USD; their scaling is not specified. Engineering remains130000USD in both source cases.

[AGENT] The50hp nominal pumping power in Table5.1 is not the140hp manufacturer motor rating in §2.5. Nor is Table5.1's922cfm test-section flow the600ACFM circulator-inlet flow. Preserve both location and rating distinctions. The0.28 exponent acts on one assumed cost fraction during a pressure reduction. Applying it to total machine cost or treating it as a calibrated140-to8000hp law would misstate the source.

## Oak Ridge: larger independent price anchor

[INHERITED: ORNL/FEDC-87/1, Cooldown of the Compact Ignition Tokamak, August1987; printed18/PDF23 and Table3.2 printed24/PDF29, image checked] The reference helium circulator raises pressure from7atm to8atm at12kg/s with about1.25MW input. Its suction is maintained near room temperature. Table3.2 gives1millionUSD vendor cost, identified as the high side of three vendor quotes, and approximate envelope2×2.5×5m. The circulator line does not explicitly itemize motor, power electronics, bearing type or seals.

[INHERITED: Table3.2] Whole-system vendor cost is2.116millionUSD; procurement adds15.5%, installation27% of hardware, engineering35% of hardware and contingency27.5% of the subtotal. These rows establish that the1million circulator price is not the final installed system cost. The percentages are CIT project assumptions for its whole cooling system, not transferable machine setting factors. Buildings and CIT structural effects are excluded by surrounding prose. The original1987 report date supplies the price-era anchor; no quote date or index rebasing is stated.

[AGENT] This reference narrows power extrapolation relative to BNL, but requires much larger casing-pressure transfer,7atm≈0.709MPa to8MPa, and hotter inlet service. It is an independent analogy/sensitivity, not a direct target quote. Its higher pressure ratio,8/7≈1.143, also differs from the retained1.02–1.04.

## General Atomic: original conceptual scaling and its scope

[INHERITED: GA-8439Rev, Reactor Arrangement Studies for a Large HTGR Plant, July31,1969, printed32/PDF36, image checked] Gulf General Atomic's manufacturing division supplied helium circulator production costs. The study assumed each circulator cost varied with capacity to the0.6 power. The design comparison changed from12reference machines to6machines of twice the capacity. Printed2/11 describe axial, steam-turbine-driven machines with water-lubricated bearings; these are not the BNL electric hermetic machines. Printed34 separates bearing/seal testing and design engineering from production capital.

[AGENT] This is primary evidence that capacity-based scaling can be a legitimate conceptual helium estimate; vendor qualification is not a prerequisite to every cost estimate. It supplies a defensible sensitivity exponent candidate, not an electric-motor-power law. Equating capacity with electrical power requires similar head and efficiency and an explicit analogy. Extrapolating23–57times in motor power from BNL goes far beyond the source's factor-two comparison.

## Conditional transfer for review

[AGENT] A reviewable reference-based scenario can start from the BNL550000USD machine-plus-motor, keep its110000USD power supply and130000USD nonrecurring engineering separate, and explicitly vary machine capacity scaling and pressure-containing cost. Retain source dollars until an independently sourced index convention is applied. Target conditions are8MPa casing, about567K inlet, low pressure ratio and assumed parallel-machine powers3232.5/7962hp. Their flow and head must remain explicit rather than being hidden by the power-only comparison.

[AGENT: proposed sensitivity, not source equation] One transparent hybrid scenario is `C_machine = 550000*(P_hp/140)^n*[0.5+0.5*(p_abs/5.06765MPa)]`. This uses the BNL component price, its assumed half pressure-sensitive allocation, and a declared size/power exponent. Taking `n=0.6` as the GA capacity analogy and `n=0.8` as the Seider purchased-compressor power analogy gives4.664/8.739millionUSD per3232.5hp machine and8.011/17.974millionUSD per7962hp machine, in unnormalized late1978 quote dollars. These arithmetic scenarios omit power supply, target-specific accessories, installation and engineering. They are not a confidence interval, a proven lower/upper bound, or a recommended point estimate. The0.6–0.8 sensitivity spans two documented modeling practices, while the pressure allocation and target application remain agent assumptions.

[AGENT] Do not combine the above hybrid pressure allocation with BNL's0.28 power adjustment: that would double-count the assumed size effect. Do not apply a stainless factor again to the stainless BNL package. Do not automatically multiply the nonrecurring130000USD design fee by every identical machine. If a repeated-unit design benefit is assumed, state its ownership and what recurring engineering/testing remains. Historical technology, modern procurement, magnetic bearings versus gas bearings, motor controls, seals/valves, design margins and large-machine fabrication remain uncertainty dimensions without sourced numerical distributions.

[AGENT] The source evidence is sufficient to formulate and independently review an explicitly conditional reference-based conceptual estimate. A strong numerical bound still needs a justified extrapolation treatment, inflation convention, package accessories and installation allocation. Whether that conditional model meets the goal's acceptance requirements belongs to the coordinator and independent reviewer; this research grants no implementation release. No source found here supplies priced circulator maintenance or replacement intervals.

## Other leads and stopping rule

[AGENT] The newly found GA911107 full-report URL returned404 and is queued natively; cached search numbers were not admitted. Downloaded, clean-screened INL/EXT-08-14054 and the2024 Birmingham-hosted pressure/cost paper were inspected for relevance but not registered: the former adds engineering maturity rather than a price coefficient; the latter holds fluid, power, temperature and pressure ratio fixed in its similarity argument and does not directly resolve the target package transfer. Modern vendor announcements bundle several nuclear systems and do not isolate a machine price. The2025 compressor-correlation paper was a bibliography lead only; no original full text was obtained or used.

[AGENT] Search ended after12queries because all3capture slots were used for the highest-value direct helium sources. No bounded-negative claim is appropriate when useful sources were registered and a named original remains queued.

Native closure returned `REGISTERED` with all3new source identities, one queued GA911107 retrieval failure and no negative. Although closure was requested with `adequacy=limit_reached` after using the3capture budget, the returned `limit_reached` field is `null`; preserve the native output as written rather than correcting its bookkeeping by hand.
