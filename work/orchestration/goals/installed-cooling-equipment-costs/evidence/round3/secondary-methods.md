# T-008 — HITEC secondary-loop methods

[OWNER: round3 brief] Retain primary8MPa helium and use HITEC270–465°C intermediate cooling. [AGENT] The acquired evidence supports concrete flow/inventory sizing, a declared molten-salt pump cost analogy, and a particularly useful salt-to-steam-generator thermal anchor near the chosen temperatures. A complete heat-to-power chain includes that steam generator. The coordinator/reviewer now assigns it once to Row8, with CAS23 inclusion unverified; the narrower Row7 equipment boundary ends at the salt supply/return interface. No new steam-generator price or unsupported CAS23 deduction is proposed here.

## Native record and source custody

Request `knowledge/research/requests/REQ-COOL-HITEC-COMPLETION.json`; run `knowledge/research/requests/runs/REQ-COOL-HITEC-COMPLETION/20260918T223846110192/`. Nine actual queries were logged before execution. Original limit18queries/4captures; coordinator authorized one additional capture solely to retry official SSC code as renderedHTML after text/plain capture failed. The request and run record retain the amendment. No model edits or domain insights.

New sources, all independently screened before substantive reading:

- [S1] `knowledge/sources/ornl_tm3777_heat_transfer_salt_for_high_temperature_steam/`: ORNL-TM-3777, E.G.Bohlmann, December1972. Includes original assessment and quoted DuPont manufacturer-property appendix.
- [S2] `knowledge/sources/inl_2022_thermal_storage_coupling_for_advanced_nuclear/`: INL/RPT-22-67671, June2022. Salt price quantity/year/grade evidence; LWR equipment curves explicitly not transferable to HTGR.
- [S3] `knowledge/sources/mcdonnell_douglas_1979_small_power_system_volume5/`: NASA-CR-162376/MDC G7833, May1979, supporting analyses. Industrial salt operating canvass and explicit salt-steam-generator thermal design.
- [S4] `knowledge/sources/nrel_ssc_heat_transfer_fluid_property_implementation/`: official SSC `tcs/htf_props.cpp`, mutable develop snapshot retained by rawSHAe5355b5fcc0e1e87cb830360f0d30fd32ef74d0522d08aa3b9508b65688f6dfb. **Extraction caveat:** `output.md` contains page chrome, while `raw.html` contains the complete895-line code in embedded JSON `rawLines`. Parsed and checked original source lines320,413,501 there; these are the authoritative equation locator, not the extracted prose.

Previously registered Seider2009Chapter22/23, ANL2018 and NETL2002 sources retain their Round2 locators. Standalone Coastal bulletin mirrors failed403/DNS or returnedHTML. A broad `helios` screen initially flagged a solar thesis andS3; a content-free count resolved every hit as `heliostat` (4/139 respectively), with zero ARIES-CS/Najmabadi/Waganer/standaloneHelios matches. No barred content was viewed. The thesis was not used. S1 supplies the original manufacturer data without relying on the inaccessible modern mirror.

## HITEC properties and operating scope

[INHERITED: S3Table10-1, printed10-2, PDF185, image checked] HITEC here is40wt%NaNO2+7wt%NaNO3+53wt%KNO3, melting142°C, cp1560J/(kgK). It is not binary solar salt or HITECXL. Tabulated density1890kg/m³ at260°C and1680 at540°C; viscosity4.3mPa·s at260°C and1.2 at540°C. These numerical anchors agree closely withS1's manufacturer density chart and viscosity curve.

[INHERITED: S4source] For a reproducible property scenario, with `TC = TK−273.15`: `cp=1560 J/(kgK)`; `rho=max(2080−0.733*TC,1000) kg/m³`; `mu=max(0.00622−0.0000102*TC,1e−6) Pa·s`. Within270–465°C neither floor binds. These are source implementation equations, not a new fit or a measured uncertainty interval.

| Temperature°C | rho kg/m³ | mu mPa·s | nu mm²/s |
|---|---:|---:|---:|
|270|1882.090|3.4660|1.84157|
|367.5|1810.6225|2.4715|1.36500|
|465|1739.155|1.4770|0.84926|

[INHERITED: S1printed23–28] Manufacturer heat-content slopes give molten cp0.373cal/(g°C), approximately1561J/(kgK), consistent with the1560 simplification. Its viscosity measurements cover300–820°F(149–438°C); the curve above820°F is explicitly extrapolated. At465°C, viscosity is therefore not directly measured by that old dataset. The SSC linear approximation differs from the original curve near the cold endpoint: source-graph approximately3.9mPa·s at270°C versusSSC3.466. Preserve this method difference; no probability bound has been established. Density is approximately1885/1740kg/m³ at270/465°C from the original chart.

[INHERITED: S1summary/printed7 and S3§10.1] Austenitic stainless construction is recommended above850°F(454°C).465°C crosses that carbon-steel guidance. Nitrogen cover limits oxidation/carbonation and freezing-point drift. The142°C fresh-salt freezing point requires startup/shutdown heating or drainability;270°C normaloperation margin does not remove stopped-line freeze protection. S1 records an eight-year unchanged batch at843°F under nitrogen and separate higher-temperature experience, but this does not establish a465°C replacement interval. Its0.5%/day nitrite decomposition estimate is for1100°F(593°C), not465°C; do not transfer that loss rate.

[AGENT] Choose stainless wetted secondary hardware as an explicit construction assumption and separate actual salt-side pressure from primary8MPa. A low-pressure expansion/drain tank plus head-driven circuit is consistent with low salt vapor pressure; use a declared finite pressure schedule and NPSH allowance, not zero pressure or an assumed8MPa salt operating condition. Source evidence establishes engineering plausibility, not a pressure rating.

## Flow, head and liquid-pump price

[AGENT] `mdot_salt=Qihx/(cp*(465−270))`. At167.439719MW perselected circuit this is550.426427kg/s. Volumetric flow is0.2924549m³/s at270°C and0.3164907m³/s at465°C. At an illustrative3m/s pipe velocity, cold/hot bores are0.3523/0.3665m; choose finite pipe schedule/geometry explicitly rather than silently pricing arbitrary continuous diameters. Secondary pumping adds electrical demand; its shaft heat and losses need one energy owner. The formula above uses entering IHX duty before that additional heat is assigned.

[INHERITED: Seiderprinted560–563] Radial centrifugal pump size `S=Q_gpm*sqrt(H_ft)`. Base purchased pump atCE500(identified2006average): `CB=exp(9.7171−0.6019*ln(S)+0.0519*ln(S)^2)`, range400≤S≤100000. Multiply type factor and stainless factor2.0. Pump cost includes baseplate and coupling, excludes motor. Type table1800rpm single-stage VSC usesFT1.5,50–3500gpm,50–200ft and200hpmaximum. **VSC means vertical case split, not vertical shaft/cantilever construction.** Do not treat that acronym as proof of salt-service geometry.

[INHERITED: Seiderprinted562–563] Pump efficiency `etaP=−0.316+0.24015*ln(Qgpm)−0.01199*ln(Qgpm)^2`, valid50–5000gpm. Motor efficiency `etaM=0.80+0.0319*ln(Pbrake_hp)−0.00182*ln(Pbrake_hp)^2`, valid1–1500brakehp. Motor base `exp(5.8259+0.13141*l+0.053255*l²+0.028628*l³−0.0035549*l⁴)`, `l=ln(Pelectric_hp)`,1–700hp.1800rpm totally-enclosed-fan-cooled factor1.3 covers1–250hp.

[EXAMPLE; AGENT proposed pump case] Two active equal parallel cold-side pumps per167.44MW circuit;40m salt head, usingS4properties. Perpump2317.752gpm,131.2336ft,S26551.53; etaP0.824924,etaM0.916245; electric191.540hp=142.832kW. Purchased SS pump23623.71USDCE500 plus TEFCmotor16204.41USDCE500; total39828.12 perunit,79656.25 percircuit. Two pumps were chosen to stay inside the cited duty/type ranges; their topology is an explicit conceptual choice, not a recovered source specification. Head40m is an assumption requiring a disjoint pressure-loss budget for both exchangers, pipe/friction, fittings and elevation effects. A closed loop has no net static lift absent open-tank level differences.

[INHERITED: S3§10.2.2/3, printed10-3, image checked] Industrial molten-salt pumps are submerged vertical centrifugal, frequently cantilever to keep salt away from bearings/packing. This supports the pump-family selection. It does not supply a cost premium for a long shaft, hot bearing arrangement, seals, heating or shaft support. Seider is therefore a declared generic-liquid hardware analogy; its numerical domain fit is real, its thermal-construction cost transfer is uncalibrated. These extra components may be explicitly inventoried and priced; they must not be implied free or require a vendor quote as the only possible resolution.

## Salt inventory and residual installation

[INHERITED: S2printed30/Figure20, image checked] Reported industrial-bulk HITEC baseline is1.23USD/kg2011, sourced to priorNREL work;0.93USD/kg2003 is another historical baseline. The2021bulk-industrial point is an **extrapolation**, approximately1.8USD/kg from the figure; the small-quantity/high-purity endpoint is approximately2.53USD/kg2021 from vendor data. These are different grade/quantity cases, not lower/upper statistical bounds. The report labels quantities≤10millionkg as small. Do not automatically grant a few-thousand-tonne circuit the bulk-price category without declaring that procurement analogy. The cleanest exact numeric source-year choice is1.23USD/kg2011 plus a separately declared purchasing-power escalation; a higher small-quantity/grade scenario can remain separate.

[AGENT] Initial inventory is the sum of filled pipe, IHXshell, salt-steam-generator shell, pump pot, expansion tank and drain/rundown working inventories, each at its fill-state density. Count a drained charge once: a spare full-capacity empty drain tank is vessel capital, not a second operating salt charge. Price `Mfill*c_salt` separately from equipment. Add explicit initial makeup/spare salt only if selected. Expansion sizing must use the cold/hot density change: for equalmass, hot volume is1.08218times cold volume, before operational freeboard.

[INHERITED: S3§10.2.2] The industrial source reports welded joints where practical, valves, line trace heating, calcium-silicate insulation and temperature instrumentation. This identifies necessary scope. Its historical asbestos-gasket detail is not current material guidance and is not adopted. No valve count, support spacing or present installed unit price follows from the text.

[INHERITED: NETLTable4, printed42] Liquid/slurry installation factors give material%ofbareequipment and labor%ofthatmaterial. Below150psig: foundations5/133, structuralsteel4/50, buildings3/100, insulation1/150, instruments6/40, electrical8/75, piping30/50, paint0.5/300, miscellaneous4/80. Above150psig the corresponding values are6/133,5/50,3/100,3/150,7/40,9/75,35/50,0.5/300,5/80. Use the chosen pressure scenario. These published categories can form explicit conceptual allowances; no factor by itself establishes a complete molten-salt bill. Remove piping material and its associated labor when adding separately priced pipes/fittings. Structuralsteel/supports, buildingfoundation and controls also need disjoint account ownership. Thermaltrace equipment/energy and valve bodies need an explicit category or inventory; no additional arbitrary multiplier is supported here.

## Salt-to-steam generator: useful direct thermal anchor

[INHERITED: S3§8.3/Table8-3, printed8-9 through8-12, originalPDF146–148 image checked] The3.5-year program uses HITEC, a separate preheater, natural-recirculation boiler with steam drum, and superheater. Water/steam is inside tubes; salt is shell-side. Figure8-4 shows approximately260–460°C salt,~165°C feedwater,~255°C boiling and427°C steam outlet. Figure8-3 identifies62bar steam. These are source design conditions, close to but distinct from the approved270–465°C salt case.

| Section | DutyMW | Outside tube aream² | LMTDK | Effective reportedU kW/(m²K) |
|---|---:|---:|---:|---:|
|Preheater|0.89|11.6|67|1.13|
|Boiler|2.67|22.1|94|1.28|
|Superheater|0.68|8.4|81|0.993|
|Total|4.24|42.1|—|—|

[AGENT] Source headers incorrectly print an extra `/hr` with kW; the pairedBtu/(hrft²°F) values and `Q≈UAΔT` check identify intendedU units above. This is a preliminary design, not independently testedU. It is nevertheless a concrete conceptual sizing anchor. ReusingU and an explicitly assumed steam state/duty split allows stagewiseLMTD and area recalculation at270–465°C. A simple sourcearea/duty comparison is9.929245m²/MW, about1662.55m² at167.439719MW; this freezes duty fractions and terminal driving forces, so label it a comparison scenario rather than a newly solved steamcycle. No mass or fabrication price is given by that table. Use an explicit tube/shell/head/sheet bill and ANL's already reviewed nuclear exchanger material/fabrication route; no Seider area extrapolation is required.

[AGENT] This exchanger is separate from helium/HITECIHX. Assign it either to an explicit intermediate account or an identified heat-admission component ofCAS23, exactly once. Its steam conditions and suppliedthermal duty form the boundary to existingpowerconversion. Source steamout427°C cannot be silently equated to an unspecified higher-temperature turbine basis; preserve the conversion efficiency as an explicit inherited surrogate or resolve that interface. A new turbine design is not required merely to price the salt-side equipment, but unexplained double counting or an incompatible thermal interface would invalidate a fullplant estimate.

## Lifecycle treatment

[INHERITED: S3§10.2.3] The surveyed plants reported limited maintenance; submerged-bearing pumps could require annual withdrawal/repacking, associated especially with steam cover gas. This supports including a service event, not annual completepump replacement. S1's multi-year salt examples support makeup-basedinventory accounting as a possible scenario, not a guaranteed lifetime at465°C. No source establishes universal replacement intervals for secondarypumps, salt orSGtubes at these conditions.

[INHERITED: SeiderTable23.1 andmaintenance discussion] A generic fluidhandling plant maintenance method is wages/benefits3.5%of **total depreciable capital**, plus25%salary,100%materials/services and5%overhead relative to thosewages: total8.05%ofthatcapital. This plant-wide method includes repair/replacementparts; it is not a component replacementlaw. Do not add it to currentCAS71 or apply it to a narrowpurchasecost denominator while calling it the source method. If used as a declared allocation/sensitivity, reconcile its labor/material scope with existingO&M and separately scheduledreplacements.

[AGENT] Minimal honest lifecycle scenario: initialsaltcharge; explicit annualmakeupfraction as assumption; pumpservice labor/material allowance as assumption with source eventmotivation; separate actualcomponent replacementclock if selected; freezeprotection electricity/heat at assumedstoppedhours. Keep initialspares, operationalservice and replacementpurchases disjoint. Reliability qualification is unnecessary, but unpricedmaintenance cannot become zero by omission.

## Remaining small decisions

[AGENT] Properties and a near-temperature steamgenerator thermalbasis are now usable. Select secondarypressure/head, realpumpconstruction inventory, finitepipegeometry/lengths, salt-filled equipmentvolumes, traceheating/drainage arrangement, and disjointvalve/support/installation allowances. Select the steam-interface assumption and a transparentlifecycle scenario. The originals permit a conditionalconceptual estimate; missing constructiondetails should be exposed as assumptions and sensitivities rather than upgraded into vendor-qualification prerequisites.

[AGENT] Native run closed REGISTERED: four registered sources. Its queued list retains the failed raw-text SSC URL because receipts are immutable; the approved renderedHTML registration resolves retrieval of the same source content, with exact code in its storedrawHTML. No operator needs to recover that raw URL again. The SG material above remains future Row8 interface evidence, not a price added to Row7.

## Requested common-year inputs

[INHERITED: `knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/output.md`, source year rows2011/2024/2025] Annual CPI values are224.9,313.7 and321.9 respectively. [AGENT arithmetic] For the existing2025CPI purchasing-power proxy, multiply a2011salt price by321.9/224.9=1.4313028012449975;1.23USD/kg2011 becomes1.760502445531347USD/kg2025proxy. Multiply a2024helium price by321.9/313.7=1.0261396238444374. These are monetary normalization proxies, not chemical-specific price forecasts or currentprocurement quotes. The1.23bulkprice still needs its quantity/grade transfer assumption.
