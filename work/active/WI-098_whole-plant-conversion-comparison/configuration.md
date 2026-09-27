# WI-098 configuration, account and variable-role contract

Companion to [design.md](design.md). All proposals are [AGENT] choices; inherited numbers are identified below. Default dollar amounts become USD2025 under the stated quotation convention. `plant.` below expands to `whole_plant_conversion::plant`; generated public keys use double underscores.

## Fixed inventory and native capture

| Quantity | Selected value / binding | Role and authority |
|---|---|---|
| Reactor geometry | R=12.7 m, a=1.3 m, kappa=1; blanket .8 m, reflector .2, shield .2, structure .15, vessel .1, gap .1, first wall .05 | Supplied fixed inventory, inherited upstream-accounting.md and WI-080 baseline |
| Magnet reference | 48 coils; 308 turns; circumference 25 m; radial coil thickness .30 m; coil centre 3.15 m; support mass 11615604.482575 kg | Fixed inherited inventory |
| New magnet offer | `magnet__winding_pack__wp_side=.54 m`; `fit_aspect_ratio=.19`; `magnet__casing__interior_y=1.30 m`; effective turn current 48000 A | Explicit selected alternate, not demand-sized; remaining full map from magnet-probe baseline; locate and record exact existing current input key during capture |
| Excitation | 14.784 MA-turn; axis 8.64 T; peak 23.904 T | Calculated with inherited field equations; field domain 20–24 T; never set extrapolation flag to false without calculation |
| Cryoplant | `rated_cold_W=40000`; `rated_intercept_W=60000`; cold20 K/intercept77 K/ambient300 K; direct rating0 MW; `purchase_cost_per_module=62957384.24217385` | Independently selected offer at twice old quote; hypothetical USD2025 procurement; inherited old ratings21933.902368719853/41599.953939961626 W and quote31478692.121086925 |
| Magnet cost capture | Tape at20 USD2025/m; existing non-tape/insulation rates explicitly requoted USD2025; winding-operation escalation321.9/130.7 instead334.4/130.7; any rate actually stated2026 converted321.9/334.4 | Price convention, held physical quantities; save each rate and sum; larger-pack50 kA mixed-dollar total2642377329.65 is evidence, not final USD2025 quote |
| Nuclear envelope | Fixed fusion2652.5632625175904 MW maximum for captured nuclear cryogenic demand; source heat maximum3125.9322770825056 MW inherited reference | Supplied conditional upper envelope; ranked source demand must be below it; 48 kA thermal capture uses this envelope independently of plasma sustainment |
| Source operating inputs | `source_basis.q_source_MW`2500/2800/3000; `deposited_heating_MW=50`; `neutron_multiplier=1.2` | Supplied operating conditions; calculated fusion and primary work remain outputs |
| Primary |14 paths,8 MPa,573.15 K inlet,200 K rise,cp5193 J/kg/K,gamma5/3,reference/rated pathflow225.07777777778 kg/s,lossfactor1.1,reference dp329187.1856931558 Pa,eta_is .772796639536644,eta_drive1 | Inherited conversion primary calculation; pressure rating300319.8958872855 Pa (use exact conversion-authoritative offer value, record minor full-plant capture difference); no binding from demand to rating |
| Heating | Coupled capacity50 MW, wall capacity100 MW; eta_source.5,eta_coupling1 | Selected capability and operation; calculated wall demand |
| Fuel | Stock5 kg T; processing .00015 kg D+T/s; burnfraction.05,recycle.99; extraction1 | Chosen inventories/capabilities; full startup and flow calculations determine margins |
| Fuel residence | feed1200 s,process14400 s,blanket86400 s,extract86400 s,buffer0,reservefraction.25,reservetime86400 s,shutdown86400 s,startupext0,growth0 | Inherited Fuel Inventory inputs; native outputs authoritative |
| Fuel constants | MeV_J1.602176634e-13; Tmass5.008267663228036e-27 kg; Dmass3.3435837768e-27 kg; decay1.782785958230312e-9/s; year31536000 s | Inherited definitions |
| Fuel plasma inventory | density1.9256443867349644e20/m³,volume425.0000143721807 m³,alpha fraction.33 | Frozen small inventory term only, no plasma qualification |
| Breeding | Mean1.1980739195540366; lower1.1861455810023918 | Conditional inherited transport surrogate; external feed closes shortfall; self-sufficiency flag separate |
| Auxiliary rejection |200 MW inclusive duty rating,2 MW selected draw,25°C supplied water condition,50M USD2025 installed quote | New finite conditional vendor offer; chosen values fixed across source loads |
| Residual source allowance |200M USD2025 installed;5 MW online electric allowance | Assumed wider casing/support/civil/extraction/storage scope beyond inherited procurement; sensitivities0/200/1000M and0/5/20MW; no physical qualification claim |

## Common initial capital leaves

Every row becomes a concrete `Supplied Plant Account :> Costed Component` leaf under `source_accounts`, with selected `quote_USD2025`, `quantity=1`, `capital_cost=quote*quantity`, documented `cas_code`, and category sum binding. Fixed numeric prices do not imply newly sourced quotations. Evidence is [upstream-accounting.md](../../orchestration/goals/design-study-whole-plant-conversion/evidence/upstream-accounting.md), especially its source-channel table; final native capture replaces only the magnet/cryo channels named here.

| Leaf | Default USD2025 | Scope / provenance |
|---|---:|---|
| `land` |16901536.908759248|CAS10 legacy amount, newly assumed2025 quote |
| `facilities` |799758795.940320015|CAS21 fixed inventory/CPI proxy; inherited facility occupancy defects remain disclosed |
| `magnet` |Captured repriced offer|Tape/material/insulation/winding/support purchase breakdown retained as child accounts |
| `heating` |264145000|Selected ECRH equipment |
| `divertor` |109109123.155930519|Selected divertor |
| `blanket` |719155016.196642518|Selected blanket |
| `shield` |452529516.994486034|Selected shield |
| `structure` |32373952.820015125|Nonmagnetic residual structure |
| `vessel` |113317730.127626330|Selected vessel |
| `power_supplies` |86013482.741806164|Fixed TF/PF supply inventory; captured drive demand must satisfy capacity |
| `remote_handling` |157969959.252817959|Fixed remote handling |
| `installation` |509887983.296871185|Inherited selected core assembly; extra casing/install scope separately allowed below |
| `primary_circulators` |442174444.749116242|Selected active vendor/design/install scope |
| `primary_pipes` |2974043934.375750542|Installed piping, steel310USD2017/kg escalated321.9/245.1;240/360 source price sensitivities |
| `primary_spares` |12020446.033021579|Supplied spares |
| `primary_helium` |1409367.527367595|Initial stock |
| `cryoplant` |62957384.242173850|New selected40/60 kW offer |
| `auxiliary_rejection` |50000000|Replaces inherited3637578.008733779 auxiliary-cooling residual; includes connection/install/pump |
| `waste` |6481502.633743829|Fixed plant thermal procurement class |
| `fuel_processing` |22811717.720117148|Selected TSTA-type capacity procurement; added extraction/storage scope in residual allowance |
| `other_reactor` |10098565.144581091|Inherited residual |
| `reactor_controls` |81921417.185930178|Common central controls |
| `shared_electrical` |105407841.903247327|CAS24 grid/switchgear quote assumed to exclude branch generators/local drives |
| `miscellaneous` |64159703.769580752|CAS26 residual |
| `pbl_initial` |23815042.059888843|Initial PbLi inventory |
| `owner` |37985982.203505553|Owner initial scope |
| `digital_twin` |5000000|Selected owner/model operation setup |
| `source_installation_allowance` |200000000|Explicit unqualified extra casing/support/civil/fuel extraction/storage installed allowance |
| `tritium_initial` |5*selected T price|Selected5 kg purchase, no separate calculated-startup purchase |

Legacy CAS22 amounts with unknown year are explicitly assumed2025 quotes. Steel/primary/CPI-proxy scopes keep their documented conversion. Never add old whole coolant cost6471347145.807992, obsolete coolant180463075.174766, old total overnight17.751B, old steam247464428.83859593, old heat rejection115939531.80564217, or old top-level totals to this sum.

## Branch purchase leaves and recurring/event ownership

| Owner | Initial scope | Annual / replacement / terminal |
|---|---|---|
| `steam_accounts` |Existing steam ledger slots1–10 pluscontroller; salt exchanger/secondary machine/install/pipes/spares, salt stock, inclusive steam generation247464428.83859593, rejection115939531.80564217; no primary helium machinery/pipes |Existing2% service, salt makeup.001, explicit machine10-year and bundle15-year events plus generic20% year15 on eligible remainder, inherited exclusions |
| `gas_accounts` |Existing slots3 compressor,4 turbine,5 generator,6 HX,7 interface,8 services,9 secondary transport85933000USD2004,10 rejection,controller10MUSD2025; ARIES factors321.9/188.9 exactly once |Existing2% service and20%year15 eligible replacement; no second compressor-work subtraction |
| `source_lifecycle.routine` |None |.8*50617243.276030459/year new reactor routine-service allocation; .5/.8/1 allocation sensitivity; conversion service separately owned |
| `source_lifecycle.blanket` |Initial blanket/divertor/PbLi above |Every18/qwall FPY; event=blanket+divertor+1*PbLi+10%*(blanket+divertor) removal/labour; outage7/12yr/event |
| `source_lifecycle.magnet` |Initial captured magnet above |Every10FPY; event1.1*captured magnet; outage1yr/event with.5/1/2 sensitivity |
| `source_lifecycle.primary` |Initial active machines above |Every10calendar years; vendor336572488.924604+install104960130.671138+removal104960130.671138; helium makeup.001*initialstock/year; pipes plant-life assumption |
| `source_lifecycle.other` |Other eligible equipment above |5% capital overhaul year20; exclude land/buildings/stocks, blanket/divertor, magnet, primary machines and all conversion; other outage allowance.5yr total |
| `fuel_accounts` |Selected T stock purchase once |External T shortfall*price plus D/Li6 purchases; T price0/10/30/100MUSD2004/kg*321.9/188.9, default30; D2175USD2025/kg and Li61000USD2025/kg explicitly assumed quotes |
| `whole.terminal` |No initial decommission reserve |10% initial overnight dismantling minus2% initial eligible hardware salvage at year30; stocks/land/owner excluded from salvage; both fractions sensitivities |
| `whole.imports` |No separate unpriced equipment |Offline fixed refrigeration+house+aux-sink load; purchased electricity50USD2025/MWh default |

## Electrical roles and binding contract

| Public part/field | Role and input/output binding |
|---|---|
| `source_basis.q_source_MW`, `deposited_heating_MW`, `neutron_multiplier` |Chosen operating inputs; qsource binds existing `primary_loop.q_source`; fusion/heatclosure/wall/divertor outputs are calculated |
| `supplied_core.capture_id` and fixed capture fields |Fixed versioned supplied offer; use numeric capture discriminator if generated interface cannot carry strings; identity/hash remains external manifest; supported/fit/current/cryo margins are assertions, not writable pass bits |
| `primary_offer.pressure_rating_Pa`, `flow_rating_kg_s` |Chosen capacity; compare calculated primary demand; default pricing/account leaves remain fixed under load changes |
| `fuel_accounts.stock_kg`, `processing_capacity_kg_s`, `tbr`, `tritium_price`, `deuterium_price`, `li6_price` |Chosen inventory/capacity/conditional transport and price assumptions; flow/startup/annualexternal outputs calculated |
| `finance.rate`, `years`, `availability`, `construction_years` |One shared owner; branch old rate/years/availability inputs become bindings; migration requires paired equality |
| `source_accounts.*.quote_USD2025` |Selected prices; native leaf cost quote*quantity; group price factors explicit, never source-demand dependent |
| `source_lifecycle.*` |Chosen lives, fractions and durations; dates/count/PV/outage margin calculated |
| `supplied_core.coil_drive_MW`, `refrigeration_MW`, `cold_W`, `intercept_W` |Fixed conservative native-captured demands at selected offer/envelope; public outputs retained, no main-study demand override |
| `source_basis.heating_wall_MW` |Calculated50/(.5*1)=100; subtract whole50MW deposited heat when finding auxiliary waste heat |
| `supplied_core.tf_cooling_MW=15`, `pf_cooling_MW=0` |Inherited fixed operating demand |
| `source_basis.fuel_vacuum_MW=10` |New assumed inclusive processing/vacuum allocation based inherited fuel allowance; no separate vacuum electricity double count |
| `source_basis.house_MW=4` |Inherited fixed house demand |
| `source_basis.reactor_controls_MW=36.5999451053` |Selected fixed central demand based old.03*1219.998MW procurement class; new explicit scope excludes branch localcontrollers;0/half/full sensitivity |
| `source_basis.residual_MW=5` |Selected assumed common source electric allowance;0/5/20 sensitivity; heat joins auxiliary sink |
| `auxiliary_rejection.rated_MW=200`, `electric_MW=2`, `water_C=25` |Chosen finite offer; calculated thermal demand/margin, costed once |
| `steam_whole`, `gas_whole` |Calculated complete ledgers; import price50 and terminal fractions .1/.02 chosen shared assumptions |

## Mandatory invariants

- Changing source load alone changes fusion/fuel/primary demand, heat accepted, lifetime exposure and net output, while selected inventory, capacities and initial costs remain fixed.
- Increasing a price changes costs only. A changed performance capability requires an explicit separately identified offer and quote.
- No fixed captured hardware field may be silently replaced by a calculated requirement. Any inconsistent capture field map fails preparation.
- No branch-specific finance can survive migration. Conversion event PV and whole-plant events share one rate/horizon/availability.
- Failed field/property/capacity/net checks remain excluded; source qualification remains a visible condition, never a manufactured feasibility claim.
