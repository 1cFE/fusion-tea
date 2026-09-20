# Bounded steam-generator admission research

Date:2026-09-19 local. Researcher:T-003 continuing model-facing reader. Status: named screening scenario for fresh independent review, not implementation or canonical plant-design adoption. This follows recommendationB of `../../physical-interface-review.md`. The original proposal/report and their images remain unchanged. The earlier provisional eighteen-circuit numerical scale is preserved under `historical-selected18/`; primary results below use the current integrated fourteen-circuit baseline.

## Findings

- [AGENT] A consistent6.2MPa/171°C feedwater/445°C steam state set admits the modeled3306.889099MW salt heat with minimum20K temperature difference. The boiling pinch is29.960531K. These results use a whole segmented variable-water-property profile rather than a hot-end check alone.
- [AGENT] Required total effectiveUA is47.786926MW/K. This is a thermal sizing demand, not proof of installed hardware, qualified flow arrangement, acceptable pressure loss, cost coverage or operating reliability.
- [AGENT]10/20/30K hot approaches produce455/445/435°C steam. The10K case fails the separately proposed20K minimum local approach. No threshold was changed to make it pass.
- [AGENT] The retained conditional445°C fit demands93.9244% of the exergy gained by the water as electricity. Passing heat-admission and reversible-ceiling checks does not validate that efficiency for this pressure, feedwater and sink scenario.

## Inputs and custody

[INHERITED: baseline] The authoritative current-baseline record is `work/orchestration/goals/current-model-comparison-readiness/evidence/entering-validation/baseline/baseline_result.json`. Its SHA256 is3332263abee71cae76abd9b50c5056af198f4bbea0fd48d69b8758b5ab57c644; executable identity isb032da4a3971979792bc024bf9cd1a41a2d83d340bad5b59ef3e1a9aeaa77236. The baseline point explicitly suppliesR12.7m,a1.3m and availability_direct0.0; other inputs resolve from `exploration/stellarator_e2e/generated/inputs/stellarator_plant_params.json`, SHAebed292a07ebfe4e840927d27851809ffd005353a32360a2dfb0a09125ad3b15, copied unchanged as `entering-effective-defaults.json`.

[INHERITED: effective defaults and native channels] Fourteen circuits;40m salt head; pump/motor efficiencies0.75/0.95; helium inlet573.15K and rise200K; saltcp1560J/kg/K. Current native values: reactor source3125.932277082506MW; helium compression175.280934404488MW; IHX duty3301.213211486994MW; salt shaft5.675887361899MW; salt electric5.974618275683MW; SG duty3306.889098848892MW; total salt flow10852.114436183412kg/s. Source flow per circuit775.151031155958kg/s times14 independently agrees. The script verifies duty, salt shaft and cold temperature against the native record; it does not execute or modify the plant.

[AGENT] Pressure6.2MPa, feedwater171°C and illustrative sink42°C are NASA-inspired screening inputs. Steam445°C is465°C salt minus proposed20K hot approach. The proposed minimum local20K requirement applies only to this steam-generator screen. It is not a new global heat-exchanger acceptance criterion. Current helium/salt IHX hot/cold approaches35/18.785365844964K and required/installed per-unit areas9189.666995/10310.691255m² remain their existing checks. The primary helium compressor suction is288.785365845°C, not300°C.

## Property authority and original inspection

[INHERITED: NIST] Two native registered sources contain the original HTML data tables and references to the IAPWS1995 equation of state:

| Grid | Registered source directory | Original HTML SHA256 |
|---|---|---|
|1K|`knowledge/sources/nist_webbook_water6_2mpa171to455c_state_table/`|2ce732b34c9b483369f8d4cb00a9c742f48f4d23b7bc3e3bef19725904600230|
|0.5K|`knowledge/sources/nist_webbook_water6_2mpa171to455c_halfk_state_table/`|46fc6b313bb2a25fee3cc161b8de989a1601dbc549b27f07b0f28f437c432234|

Official query endpoint is `https://webbook.nist.gov/cgi/fluid.cgi`. Exact parameters: `Action=Load&Wide=on&ID=C7732185&Type=IsoBar&Digits=8&P=6.2&TLow=171&THigh=455&TInc=1&RefState=DEF&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm`; the second query changes onlyTInc to0.5. The native registration receipts retain complete URLs. `Action=Data` produces the original downloadable TSV files retained here as `nist-original-1K.tsv` and `nist-original-halfK.tsv`. All14fields in all287/571rows match their corresponding captured HTML exactly. No lossy browser extraction supplied the numeric data. The phase labels and duplicated saturation temperature are preserved.

Original1K HTML locators: headers and171°C row nearline319; saturated-liquid/vapor rows426/427;435/445/455°C rows585/595/605. Exact source rows should be found by their temperature and phase rather than assuming these line numbers in the separate half-K artifact. Entropy andcp columns useJ/g/K, numerically identical tokJ/kg/K. Enthalpy iskJ/kg. Source reference choices cancel in the enthalpy/entropy differences used here.

| State | Temperature°C | EnthalpykJ/kg | EntropykJ/kg/K |
|---|---:|---:|---:|
|Feedwater|171|726.40880|2.0446026|
|Saturated liquid|277.73289|1225.0579|3.0475566|
|Saturated vapor|277.73289|2782.3705|5.8744960|
|435°C steam|435|3263.0211|6.6519964|
|445°C steam|445|3287.7317|6.6866472|
|455°C steam|455|3312.2463|6.7205477|

Original rendered rows were inspected in `source-images-verified/feedwater171.png`, `saturation.png`, and `steam445.png`. Their JSON sidecars retain thirteen missing/local-resource console errors and one unavailableSVG helper error because the captured HTML was rendered viafile://; the static property rows and column headers render intact. An initial browser launch was sandbox-blocked; an escalated launch worked. The first selector was incorrect and timed out; that failed screenshot/session remains under `source-images/`. The corrected exact text selector succeeded. No table content was edited for screenshots.

[INHERITED: earlier original sources] NASAFigure8-1 is the previously inspected `../nasa-p143.png`, printed8-6, with62bar/427°C turbine inlet,171°C feedwater,42°C condenser. Its Figure8-4 boiling curve near255°C is not reused. Earlier registered NISTIR5078Table2, `../nist-saturation.png`, confirms6.2MPa saturation277.733°C to its printed precision. Its enthalpies1225.1/2782.4 agree with the fresh table's higher-precision values. The original NASA source supports a separate preheater, natural-circulation boiler/drum and superheater, but does not validate this target's duties or efficiency.

## Equations and numerical method

[AGENT] No external heat loss, fixed water pressure, countercurrent arrangement and constant saltcp are explicit screening assumptions. Water properties vary with temperature. No water-side pressure loss or added steam-line temperature loss is solved. Total salt heat capacity rate isCs=mdot_salt*cp_salt. The salt pump increases temperature by`g*head/(eta_p*cp_salt)=0.335270085470K`. With270°C after pumping, SGreturnC=269.664729914530°C and supplyH=465°C. ThusQ_SG=Cs*(H−C)=Q_IHX+W_salt. Motor losses are excluded from this heat credit and remain separately rejected.

Letq=Q_SG inMW, h0=feedwater enthalpy, hf/hg=saturation enthalpies, h3=outlet-steam enthalpy inkJ/kg. Steam flow is`1000*q/(h3−h0)`kg/s. Economizer/evaporator/superheater duties are respectively`mdot_steam*(hf−h0)/1000`, `mdot_steam*(hg−hf)/1000`, `mdot_steam*(h3−hg)/1000`. Along cumulative water enthalpyh, salt temperature is`C+(H−C)*(h−h0)/(h3−h0)`. Water temperatureT(h) is interpolated separately within liquid and vapor branches; the latent section is isothermal at277.73289°C. Interpolating through the latent jump as though it were a continuous liquidcp would be wrong.

Define local gapg(h)=Tsalt(h)−Twater(h). Every tabulated interval is piecewise linear inenthalpy. Its minimum therefore occurs at one of its endpoints; all endpoints, phase junctions and full segment slopes are checked. At445°C, nonboiling gap slopes range−0.33004244 to−0.11436438K/(kJ/kg), always decreasing; the boiling gap increases. This proves the reported minima within the declared interpolant, not arbitrary unmeasured property behavior. Property refinements quantify observed interpolation sensitivity separately.

Required effective thermal conductance is`UA=∫dQ/g`. For each interval of enthalpy widthdh and endpoint gapsg1,g2, the exact piecewise-linear contribution is`(mdot_steam/1000)*dh*ln(g2/g1)/(g2−g1)`MW/K, with equal-gap limit`(mdot_steam/1000)*dh/g1`. Nonpositive gaps raise an explicit error. This integral replaces one terminalLMTD per single-phase section because watercp changes. It assumes countercurrent effective conductance; a real multi-pass design needs its own correction. Area isUA/Uonly if an appropriate effectiveU is selected.

## Current fourteen-circuit results

[AGENT] At445°C, steam flow is1291.086375266817kg/s, or0.390423245738kg/s perMW ofSGheat. Duty fractions are0.194684200106/0.608011039920/0.197304759974. Salt junction temperatures from cold to hot are269.664729914530,307.693420723634,426.459421421361,465°C. Feedwater-side cold gap is98.664729914530K, boiling inlet pinch29.960530723633K, superheater cold gap148.726531421361K, steam hot gap20K.

| Section | DutyMW | MinimumgapK | RequiredUAMW/K | RequiredUA perMW heat,1/K |
|---|---:|---:|---:|---:|
|Economizer|643.799059049061|29.960530723633|11.495310822623|0.003476170648|
|Evaporator|2010.625079891343|29.960530723633|27.124602663523|0.008202453077|
|Superheater|652.464959908489|20|9.167012791080|0.002772095621|
|Total|3306.889098848892|20|47.786926277226|0.014450719346|

[AGENT] Optional area illustration uses NASAeffectiveU1.13/1.28/0.993kW/m²/K, with flow-arrangement effects assumed absorbed. Areas are10172.84/21191.10/9231.63m², total40595.57m². This source-to-target transfer is unqualified. No installed SGcapacity, number of SGtrains, metal mass, steam-side hydraulic loss, pressure qualification or purchase price follows. The current fourteen helium/salt loops do not by themselves establish fourteen installed steam generators.

| HotapproachK | Steam°C | Steamflowkg/s | Economizer/boiler minK | Superheater minK | TotalUAMW/K |20Kcriterion|
|---|---:|---:|---:|---:|---:|---|
|10|455|1278.846446789055|29.600006079796|10|50.314289228104|violated|
|20|445|1291.086375266817|29.960530723633|20|47.786926277226|satisfied|
|30|435|1303.663590549053|30.330990082798|30|46.322170996181|satisfied|

The scenario order is fixed, not searched for an optimum. Heat duty remains constant; increasing hot approach reduces steam temperature and surrogate efficiency, increases required steam mass flow and reduces required conductance here. The20Kcase exactly meets the proposedminimum, without additional design contingency. This proposed screen is distinct from all current plant engineering verdicts, which remain untouched.

## Exergy and conditional efficiency

[AGENT derivation] For an incompressible constantcp salt stream coolingH_K→C_K, reversible heat exergy at an illustrative sinkT0=315.15K is`E_salt=Q_SG*[1−T0*ln(H_K/C_K)/(H_K−C_K)]`. This is a necessary heat-conversion ceiling, not a predicted engine efficiency. At current salt temperatures it is50.4080911133% or1666.939669965043MW. Pump/motor electricity is not free output; this ceiling refers only to thermal admission.

[AGENT derivation] The water's exergy gain across an adiabatic, shaft-work-freeSGat fixed pressure is`E_water=mdot_steam*[(h3−h0)−T0*(s3−s0)]/1000`. At445°C it is1418.106737789542MW, or42.8834078011% ofSGheat. The difference248.832932175501MW is modeled heat-transfer exergy destruction. A downstream cycle receiving only this heat and rejecting atT0 cannot turn more than this gain into net work; other external heat inputs would need a separate boundary.

[INHERITED+AGENT] The existing Kovari correlation yieldsη0.402779816342490, so at unchangedQSGit would produce1331.948183899339MW before external auxiliaries. This is93.9243957035% ofE_water. It passes necessary energy/exergy inequalities, but the small remaining allowance for turbine, regeneration, pumping and generator irreversibility is a material applicability warning. This task does not assert that the named62bar cycle attains that efficiency. The displayed power is conditional heat-times-fit arithmetic, not a newly executed plant/net-power/LCOE result.

[INHERITED: Kovari originalTable4 and bibliography] The fit remains for384–642°C turbine inlet, literal273 logarithm offset, helium-primary superheated Rankine with the embedded0.0179 benchmark adjustment. Its separate low-temperature-divertor penalty is keptzero only under the inherited heat partition. Original reference6 is Porton etal., Assessment of DEMO relevant helium-cooled balance of plant technology, EFDA2M4XFP(2012); reference10 is Dostal etal., MIT-ANP-TR-100(2004). The inspected source does not specify the pressure/regeneration/sink assumptions needed to identify its fitted cycle with this62bar screeningcase. Those references were considered as possible follow-on evidence but not acquired in this bounded property-screening task. No assertion that they are inaccessible follows. Full-load design-point evaluation is the only supported operating mode; NASA's bypass discussion does not validate a constant-efficiency part-load model.

## Offline reuse and verification

Run `.codex-test/run python work/orchestration/goals/current-model-comparison-readiness/evidence/physical-research/screening/calculate.py` to regenerate numeric results from the captured HTML. Run `MPLCONFIGDIR=/tmp/physical-screen-mpl .codex-test/run python work/orchestration/goals/current-model-comparison-readiness/evidence/physical-research/screening/check_and_plot.py` to compare originalTSV/HTML, independently integrate heat-transfer and entropy relations, preserve failures and rebuild the plots. No property package was installed and the runtime environment was not modified.

`water-properties-halfK.csv` is a reusable normalized derivative with columnsT°C,pMPa,hkJ/kg,skJ/kg/K,cpkJ/kg/K,phase. Its source is the captured half-KHTML, not an independent authority. `manifest.json` hashes scripts, outputs, originalTSV and normalizedCSV. Future native code should retain the phase split and exact fixed6.2MPa scope; do not extrapolate pressure or beyond171–455°C. The physical saturation pair is included explicitly. The three named outlet states are exact source rows. If selecting other states, document the interpolator and enforce its domain rather than silently extrapolating.

`verification.json` records exact correspondence of all14columns across both raw formats; independentSimpsonquadrature agreement inUA within1.71e−13relative; entropy-integration discrepancy at most1.23e−7kJ/kg/K; strictly negative single-phase gap slopes; and the preserved10Kcriterionfailure. A synthetic nonpositive-gap input raises instead of clipping. All common1K/0.5Krows agree exactly. At interveninghalf-Krows, the largest enthalpy discrepancy from1Klinear interpolation is0.0118kJ/kg and the largest inverse-temperature discrepancy is0.00240944K. Across10/20/30Kcases, totalUA refinement differences are4.41e−8/2.47e−7/3.28e−7relative; worst section change is2.97e−6relative. These are observed interpolation checks, not confidence bounds or equipment uncertainty.

`current-baseline-first-check-failure.json` preserves a research checker failure: an exact-zero energy-residual assertion rejected floating-point summation residue4.55e−13MW at the current baseline. The checker now requires1e−14relative closure and still exports the raw residuals. No plant result, engineering predicate or scientific acceptance criterion was changed. This numerical-check repair is separate from the genuine10Ktemperature-criterion failure.

## Native research return and remaining decisions

Request `knowledge/research/requests/REQ-COMPARISON-STEAM-ADMISSION.json`; native run `knowledge/research/requests/runs/REQ-COMPARISON-STEAM-ADMISSION/20260920T003233454917/return.json` returnsREGISTERED with the twoNISTsources, no queue. One targeted endpoint search and two source captures were used. Capture used authorized network escalation after sandbox DNS limitations seen during the previous task. New source tables were screened by the native holdout operation; only water-state data and references were read. No barred materials, model edits, test edits, commits, broad search, coolant substitutions or cost tuning occurred.

[AGENT] Recommend fresh review of these source rows, calculations and applicability limits before substantial implementation. The bounded admission screen is now concrete. Remaining canonical decisions are whether62bar/171°C/20Kminimum are adopted as design assumptions, whether the conditional Kovari transfer sufficiently answers the current comparison question, and whether any additional SGcost is later priced underCAS23. Missing SGprice is retained as permitted scoped limitation; no unsupported deduction from the existing turbine coefficient is introduced. These choices do not change the existing P2depth target or comparison acceptance bands.
