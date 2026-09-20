# Facilities, fuel, maintenance and heating inventory

[AGENT] Source-level inventory at HEAD `0223c73785713400633b857183e6a7f5f103aa95`, 2026-09-20. No production files changed or runtime checks executed. The statuses below establish architectural findings, not native acceptance. All proposed contracts are agent recommendations for independent review. No reference papers, holdout observations or later evidence commits were opened.

[OWNER-VERBATIM] “As soon as you start introducing ‘sizing’, then you are basically pre-defining which design parameters are ‘free’ and which are ‘derived’. this is explicitly what we wanted to avoid.” Controlling requirement: `modeling_project/REQUIREMENTS.md`, MR-7. The requirement permits directional evaluations and explicit policies; it does not authorize assigning every quantity independently or replacing an operating identity with an arbitrary input.

## Findings and proposed contracts

| Scope | Current status | Evidence and consequence | Proposed supported evaluation |
|---|---|---|---|
| Facility storage allocations | Violated in active stellarator mode; supplied positions supported in mode 0 | `generated/handwritten/mfe_facilities/facility_layout_impl.py:247` selects every allocated position count from calendar peaks when mode=1. Stellarator binds mode=1 at `models/designs/stellarator_09/stellarator_plant.sysml:1564`. Mode 0 preserves offers and tests `allocated-required`. | Explicit supplied position counts, independent calculated peaks and adequacy checks. Existing automatic allocation may become a separate proposal policy whose result is replayable as a supplied design. |
| Facility dimensions and parcel | Violated beyond the mode switch | `facility_layout_impl.py:144` computes wing length using a maximum of sector and storage requirements, hall size from these wings, cooling hall from circuit count/envelopes, annex from allocations/service dimensions, then parcel bounds around automatically placed buildings. These decisions remain active in mode 0. | A supplied facility design includes clear dimensions and layout/parcel choices; requirements and occupied envelopes stay separate. Preserve a restricted topology if declared, but evaluate undersized geometry without expanding it. Dimension-derived areas, concrete, formwork and rebar remain identities. |
| Provisional facility envelopes and occupancy rooms | Policy-selected geometry; no independent supplied building evaluation | `facility_layout_impl.py:193` sets ten rooms to equipment-envelope dimensions times a common scale plus fixed allowances, and three offices to occupants × area/person × circulation. | Distinguish equipment/occupancy demand from chosen room dimensions. Fixed allowances may remain explicit layout-policy assumptions in a proposal path. Do not represent provisional envelope adequacy as equipment qualification. |
| Facility routes and outages | Partly compliant | Fixed aisle, cross width, door, airlock and headroom checks can fail. Readiness and outage requirement are compared with supplied times; these are not enlarged. But several margins are guaranteed by geometry construction, including machine side and sector front. | Retain independent dimensions/times and failed margins. Recompute every fit margin from supplied geometry, including currently self-satisfied margins. Keep qualification flags separate. |
| Fuel processing | Violated | `generated/handwritten/mfe_fuel_cycle/fuel_processing_cost_impl.py:24` rejects margin<1; line 33 sets capacity=running exhaust×margin, then capital/install scale from that capacity. No independently supplied capacity or shortfall is exposed. | Supplied D+T processor rating in kg/s per module; compute running exhaust separately; expose signed rating-minus-demand and adequacy. Costs use supplied rating. Source interpretation flag remains separate. Optional margin policy produces a design outside the evaluator. |
| Fuel working hold-up | Conditional operating closure, not by itself a violation | `fuel_inventory_impl.py:71` computes stream×residence stocks and plasma density integral. These quantify fuel content under specified steady-state residence assumptions; they do not quantify vessel storage capacity. | Explicit residence-driven operating analysis remains supported. Name its result required/nominal process content. Do not claim supplied tank volume, stock limit or installed process capacity has been evaluated. An inventory-driven inverse analysis requires a separate contract and validation, not blanket substitution. |
| Fuel buffer/reserve and initial supply | Policy-bound selected stock; supplied-stock evaluation absent | Same function sets buffer=inject×tau_buffer and reserve=inject×reserve_fraction×tau_reserve; binds these as actual `Fuel Stock` masses and total held inventory. `held_inventory` is read only in dormant mode. Startup minimum/conservative supply are outputs with no offered-supply comparison. | Separate selected maintained buffer/reserve stocks from coverage requirements where independent evaluation is intended; total decay and breeding requirement use actual maintained stock. Startup requirement can remain a requirement-only calculation if that limitation is explicit, or compare it against supplied startup stock. Do not silently assert supply exists. |
| Replacement calendar | Explicit policy currently embedded with physical lifetime | `mfe_lifecycle.sysml:14` and `lifecycle_calendar_impl.py:107`: physical fluence life=fluence/q, replace immediately at that life, pause aging in supplied outage, apply residual unplanned fraction. Availability, event count and PV follow that policy. | Preserve named replace-at-fluence-limit analysis as an explicit policy. Physical limit and actual replacement schedule are different quantities. If arbitrary dates/early replacement are supported, accept schedule separately and check exposure. No basis to silently invent preventive replacement criteria. |
| Heating | Compliant source-level stellarator example; native verification outstanding | Chosen wall-plug capacity goes through fixed efficiency identities to installed coupled capacity and source-output capital cost. Operating demand is a separate inverse conversion. Sustainment compares demand with installed coupled power. | Retain chosen capacity and efficiencies; vary plasma demand while holding installed hardware/capital fixed. Check insufficient/sufficient capacity and domains through native execution. Generic direct-power path consistency is unverified and distinct from this stellarator conclusion. |

All generated paths above are relative to `exploration/stellarator_e2e/`.

## Public quantities, units and bindings

### Facilities

Authoritative public analysis interface: `models/library/analyses/mfe_facilities.sysml:4`. Owner part inputs and exact bindings are at `models/designs/generic_mfe/mfe_subsystems.sysml:740` and `:894`. The appendix inventories every input in declaration order. They are plain `Real` values; dimensional meaning is carried by contract and implementation rather than SysML quantity types.

| Quantity family (exact input stems) | Units | Current role / relationship |
|---|---|---|
| `facilities_enabled`, `facilities_cost_mode`, `facilities_capacity_mode` | Boolean / binary dimensionless | Activation, legacy/layout account selection, and offered/demand-selected storage policy. These three decisions are distinct. |
| `sector_count`, `sector_bays`, `sector_service_teams`; `cooling_prepare_stations`, `cooling_machine_stations`, `cooling_bundle_stations` | counts | Declared topology/capacity/resources. Active implementation requires one module, four sectors, live calendar. Two machine and two bundle service positions are the represented geometry; larger requested station counts yield failed capacity rather than automatic expansion. |
| `component_width/height/length`, `component_handling_margin`, `component_material_fraction`, `divertor_packages_per_sector`, `waste_package_yield` | m, dimensionless, counts | Chosen package description and conversion policies. Blanket packages per sector=ceil(blanket volume/(4×material fraction×package volume)); material capacity follows inferred package count. This selects segmentation and package inventory; it is not a supplied segmentation check. |
| `exterior_allowance`, `sector_route_clearance`, `sector_headroom`; helium/salt package dimensions, HX end allowance, cooling margin/aisle/cross/headroom/airlock | m | Envelope assumptions and route choices. Equipment-derived carrier dimensions and several minimum room dimensions are currently calculated. |
| All component/sector/cooling preparation, movement, processing, receipt, hold, cooldown/recommission timing inputs | days | Operational schedule policy and task duration assumptions. Calendar events generate occupancy intervals and queue peaks; deadlines/readiness/allowed outage are evaluated, not enlarged. Negative initial dates are pre-operation policy. |
| `clean_positions`, `dirty_buffer_positions`, `dirty_store_positions`, six `cooling_{clean,dirty}_{helium,salt,bundle}_positions` | counts | Supplied installed offers in mode 0; ignored for allocation in mode 1. Outputs `*_allocated` are actual quantities used to build rooms. |
| Nuclear/conventional wall/floor/roof and rebar density | m; kg/m³ | Chosen construction section properties; geometry identities produce concrete m³, formwork m², rebar kg. These do not qualify structure, shielding or loading. |
| Building separation, external access, provisional envelope scale; ten equipment room input triples; heat-rejection length/width | m; dimensionless scale | Layout policy or chosen provisional equipment envelopes. Building and parcel sizes still selected from them. |
| Administration/control/security occupants and area/person; circulation factor, height, aspect ratio | count, m²/person, dimensionless, m | Occupancy requirement and automatic room proportion policy. |
| `n_mod`, major/minor outer radius, blanket volume | count, m, m³ | Upstream supplied/derived plant and equipment facts; no facility authority to change them. |
| Calendar q/fluence/years/outage/unplanned/mode/life/count/availability | MW/m², MW·yr/m², yr, fraction, mode, FPY, count, fraction | Upstream calendar compatibility inputs. Layout reuses calendar logic; calendar mode/life/count/availability check coherence. |
| Cooling circuits/equipment counts, machine/bundle life, HX shell bore/wall/length/tube length | counts, years, m | Upstream installed cooling hardware and maintenance lives. Facilities derive storage demand and buildings from them. |

Complete output families: activation/modes; sector envelope dimensions (m); parcel and clear/gross areas (m²); controlled/total air volumes (m³); package counts and material volumes (m³); required/allocated storage counts; queue peaks/counts; calendar event count/first/last year; readiness/outage margins (days); storage capacity margin (count), route margin (m); four qualification/basis flags; provisional-room count; and, for each of the 25 civil components, clear L/W/H (m), clear/gross area (m²), air volume (m³), sub/super concrete (m³), formwork (m²) and rebar (kg). The 25 named components are reactor hall; four sector wings; four sector links; cooling hall, annex and link; turbine hall; cryo coldbox and compressors; fuel, reactor auxiliaries, power supply, electrical, service-water, maintenance-shop and site-services buildings; administration, control and security. Exact output declarations are `mfe_facilities.sysml:143` onward.

Binding/cost chain: `Buildings.layout` outputs → exposed building attributes → 25 `Facility Civil Component` occurrences → `civil.cost_2025` → `civil_rollup` → `facility_accounts` → building capital. Controlled air volume drives historical ventilation power-law price; parcel area drives land cost. `mfe_subsystems.sysml:1994`–2074 contains ventilation, rollup, site/land and account selection; `mfe_facilities_parts.sysml:30` binds the six commodities to prices. Price inputs are installed-direct USD rates per m³/m²/source tonne, CPI ratio, rate multiplier and tonne-to-kg interpretation; they are cost assumptions, not capacities. `mfe_facilities.sysml:507` onward exposes civil/shipping/ventilation/rollup/land/site/preconstruction helpers. Ventilation is explicitly a volume cost proxy, without airflow qualification. Land from a generated bounding rectangle is parcel selection, not proof that an offered site fits. Five plant facility predicates consume margins (`mfe_plant.sysml:67`); qualification flags must not be folded into those passes.

### Fuel and inventory

Exact public interfaces and output units are `models/library/analyses/mfe_fuel_cycle.sysml:53`, `:159`, and `:263`. Fuel-cycle owner attributes/bindings: `models/library/structure/mfe_plant_systems.sysml:430`–638.

| Quantity family | Units | Roles and binding |
|---|---|---|
| `p_fus`, `fuel_q_eff`, `mev_to_joules`; burn fraction, recycle fraction, TBR, extraction efficiency | MW, MeV/reaction, J/MeV; fractions / T atoms per reaction | Operating inputs → reaction burn B, injection F=B/burn fraction, exhaust U=F−B, recycle/loss and breeding/extraction streams. These are balances, not equipment choices. |
| `lambda_T`, `G_stock`, isotope masses; plasma volume, central T density, density exponent | s⁻¹, atoms/s, kg/atom; m³, atoms/m³, dimensionless | Decay/growth and plasma integral assumptions. Active inventory rejects nonzero growth. |
| `inventory_enabled`, `held_inventory`, `breeding_defined` | Boolean, T atoms, binary | Dormant compatibility selects held inventory. Active mode ignores held amount and derives total from modeled stocks. Breeding unsupported flag propagates to definedness. |
| `tau_feed/process/blanket/extract/buffer/reserve`, `reserve_fraction`, startup extension, shutdown duration | s, dimensionless | Residence-driven stock closure plus separate stock-coverage policy and startup horizon. Seven stock outputs each expose atoms and kg: feed, plasma, processor, blanket, extraction, buffer, reserve; aggregates working/total. |
| Prefill, startup deficit/minimum/decay allowance/conservative supply | atoms and kg T | Bounded commissioning requirements. Recycle delay, breeding delay, horizon (s); max decay residence (dimensionless); no offered-stock sufficiency check. |
| Availability and seconds/year | fraction, s/year | Operating rates converted to calendar throughputs. Burn/injection/exhaust/recycle/production/extracted/recycle-loss/extraction-loss each expose kg T/s, kg T/day, annual kg T. D+T injection/processor expose kg/s and kg/day. |
| Decay, signed makeup/external shortfall, calendar-average processor; annual counterparts, shutdown remaining/loss | kg T/s, kg T/year, kg T | Maintained-stock decay is calendar-wide; throughput is productive-time scaled. Shutdown passive decay is separate. No clamp on signed makeup; external shortfall is nonnegative requirement. |
| `processing_enabled`, `processing_source_conditions`, `processing_capacity_margin`, `processing_price_multiplier`, `processing_reference_flow`, exponent, target/source CPIs and four source capital/install pairs | flags, dimensionless, kg D+T/s, USD | Automatic capacity policy and conditional cost transfer. Rows: transfer, cleanup, distiller, containment. Rating per module and plant-total rating are outputs; all plant-total row costs scale with module count. |

`inventory.total_atoms` binds `fuel_cycle.I_total` (`mfe_plant_systems.sysml:448`), which feeds both fuel TBR requirement and stellarator breeding adequacy (`stellarator_plant.sysml:2079`). Thus reserve/buffer policy changes decay and breeding need, not just presentation. Stock part masses bind directly to inventory outputs (`mfe_plant_systems.sysml:526`). D+T exhaust binds `processing_cost.flow_in`; processor cost binds the exhaust-processor part and exposed fuel-handling capital; `mfe_plant.sysml:521` consumes it in capital rollup. Installation is also exposed for shipping exclusion. `DT Fuel Cost` remains reaction/annual-throughput based; do not assume selected reserve/startup stocks are purchased or priced there. No tank-capacity or independent startup procurement cost relation was found in this path.

### Maintenance policy and heating

The calendar's public inputs are q (MW/m²), fluence allowance (MW·yr/m²), operating years, outage years, unplanned fraction, event cost (USD), interest rate, coil life (FPY) and held availability. Outputs are physical life, replacement count, productive FPY, planned/unplanned/terminal years, availability, replacement PV (USD), annual CAS72 (USD/year), coil-life margin (FPY), and dated-energy ratio. Exact interface: `mfe_lifecycle.sysml:90`; implementation: `generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py:99`. Held-mode life clipping is an explicitly historical compatibility algorithm, not an unconstrained physical lifetime prediction. Facility queue/handling policy does not change the supplied calendar outage when it fails to finish; the model reports the failed outage margin. Calendar changes affect annual fuel and financial denominators even when equipment capital stays fixed.

Heating supplied quantities: installed wall-plug MW, source and coupling efficiencies, optional direct delivered/coupled MW, NBI/ICRF/LHCD installed MW and per-method USD/MW rates. Identity outputs are installed delivered MW, coupled MW, electrical MW and combined efficiency. `mfe_power_core.sysml:424`–487 binds these to the heating part and price; ECRH capital uses installed delivered power. Operating coupled demand is separate at `mfe_plant.sysml:358`; stellarator sustainment binds installed coupled ceiling at `stellarator_plant.sysml:2116`. Operating heat reaches blanket/divertor and electrical balance, while capital follows installed capacity. All efficiencies need positive ≤1 domains. Simultaneously inconsistent direct delivered/coupled values in the generic dormant path remain unverified; stellarator zeroes both direct terms.

## Generated and study consumers

The current generated tree carries `modules/mfe_facilities/facility_layout.py`, `modules/mfe_fuel_cycle/{fuel_inventory,fuel_processing_cost,fuel_cycle_flows}.py`, their handwritten implementations and matching output schemas. `generated/schemas/stellarator_plant_params.py:94`, `:215`, `:243` and `:296` expose `stellarator_09__stellaris__buildings__facilities_capacity_mode`, `...__fuel_cycle__processing_capacity_margin`, `...__fuel_cycle__tau_reserve`, and `...__heating__p_wallplug_heat`; all use the same nested-owner naming convention. The library files are copied into `exploration/stellarator_e2e/models/` for generation. Repair must update model source, regenerated interfaces, normative handwritten implementations and their integration promotion; merely modifying copied/generated files is insufficient.

Native study preflight reads the promoted package contract's qualified parameter names and rejects absent declared keys (`scripts/study/preflight.py:134`–175). Therefore changed public inputs require regenerated contracts and new study axis declarations. Historical packages/results should retain existing replay behavior. `tests/models/test_fuel_processing_costs.py:42`, `:112`, `:142` encode flow×margin scaling and rejection of insufficient margins; these expectations must change for independent rating. `tests/models/test_layout_facilities.py:45` already covers undersized offered positions and narrow routes, but later geometric assertions and oracle implementation must be checked for demand-matched room assumptions. Current oracle files `oracle_facilities.py`, `oracle_fuel_inventory.py`, `oracle_fuel_processing.py` are downstream consumers; no frozen historical study was edited or reinterpreted. Exact promoted-package identity and full native graph coverage remain coordinator/integration verification, not established by this static inventory.

## Decisions requiring explicit scope or scientific resolution

[AGENT] The supplied-design repair does not require a new physics equation for processor rating-minus-demand or rectangular room fit. It does require agreement on the supported facility design representation: retaining a declared four-wing topology can be adequate, but keeping every room automatically fitted is not. A separate proposal object must include dimensions, positions and stock/capacity choices needed for replay; freezing only storage counts misses the larger policy.

[AGENT] Fuel maintained stock requires explicit meaning. Flow×residence legitimately describes operating content; reserve coverage and available startup supply are design/policy questions. Decide which selected stocks the repaired public contract evaluates, whether stock coverage should be a constraint, and which inventory actually contributes decay. Independent tank volumes require storage physics or an explicit unsupported status. Current startup bound cannot establish continuous external availability or qualified commissioning reliability.

[AGENT] Physical fluence limit and elective replacement interval must remain distinct. An explicit existing replace-at-limit study is defensible without a new owner decision. Claiming arbitrary replacement-schedule evaluation requires implementation and constraints absent today. Likewise, existing source-conditions Boolean for the processing cost does not establish price validity over all chosen ratings; preserve the disclosed conditional cost scope and do not infer a new empirical interval from agreement with any reference.

[AGENT] Acceptance must exercise offered low/high processor rating and room/storage capacity, vary demand at fixed supplied equipment, check price/mass/geometry propagation, and distinguish failed capacity from unsupported domain. Fuel closure tests instead verify balances and stated stock policy; independent reserve/startup checks apply only once their offered-stock contract is adopted. Heating is a useful regression control: changed operating demand must not resize heating or change its installed-capacity price. No branch of this inventory is certified by runtime evidence.

## Exact facility input inventory

The following extraction preserves every public analysis input name, including upstream facts and policy controls; family roles and units are defined above.

```text
in attribute facilities_enabled_in : Boolean default := false;
in attribute facilities_cost_mode_in : Real default := 0.0;
in attribute facilities_capacity_mode_in : Real default := 0.0;
in attribute sector_count_in : Real default := 4.0;
in attribute sector_bays_in : Real default := 4.0;
in attribute sector_service_teams_in : Real default := 2.0;
in attribute exterior_allowance_in : Real default := 2.0;
in attribute sector_route_clearance_in : Real default := 6.0;
in attribute sector_headroom_in : Real default := 3.0;
in attribute component_width_in : Real default := 4.0;
in attribute component_height_in : Real default := 2.0;
in attribute component_length_in : Real default := 2.0;
in attribute component_handling_margin_in : Real default := 0.5;
in attribute component_material_fraction_in : Real default := 0.5;
in attribute divertor_packages_per_sector_in : Real default := 4.0;
in attribute waste_package_yield_in : Real default := 1.0;
in attribute component_remove_days_in : Real default := 0.5;
in attribute component_install_days_in : Real default := 0.5;
in attribute sector_clean_days_in : Real default := 7.0;
in attribute sector_test_days_in : Real default := 7.0;
in attribute sector_split_days_in : Real default := 7.0;
in attribute sector_join_days_in : Real default := 7.0;
in attribute sector_transport_days_in : Real default := 2.0;
in attribute cooldown_days_in : Real default := 30.0;
in attribute recommission_days_in : Real default := 30.0;
in attribute initial_receipt_lead_days_in : Real default := 180.0;
in attribute initial_sector_start_days_in : Real default := -120.0;
in attribute component_receipt_lead_days_in : Real default := 90.0;
in attribute component_prepare_days_in : Real default := 1.0;
in attribute component_process_days_in : Real default := 1.0;
in attribute component_hold_days_in : Real default := 365.25;
in attribute clean_positions_in : Real default := 36.0;
in attribute dirty_buffer_positions_in : Real default := 18.0;
in attribute dirty_store_positions_in : Real default := 36.0;
in attribute cooling_initial_receipt_lead_days_in : Real default := 180.0;
in attribute cooling_initial_handoff_days_in : Real default := -30.0;
in attribute cooling_receipt_lead_days_in : Real default := 90.0;
in attribute cooling_hold_days_in : Real default := 365.25;
in attribute cooling_prepare_stations_in : Real default := 2.0;
in attribute cooling_machine_stations_in : Real default := 2.0;
in attribute cooling_bundle_stations_in : Real default := 2.0;
in attribute cooling_prepare_machine_days_in : Real default := 0.5;
in attribute cooling_prepare_bundle_days_in : Real default := 1.0;
in attribute cooling_machine_process_days_in : Real default := 2.0;
in attribute cooling_bundle_process_days_in : Real default := 5.0;
in attribute cooling_field_cycle_days_in : Real default := 0.2;
in attribute cooling_internal_move_days_in : Real default := 0.1;
in attribute cooling_clean_helium_positions_in : Real default := 29.0;
in attribute cooling_clean_salt_positions_in : Real default := 29.0;
in attribute cooling_clean_bundle_positions_in : Real default := 14.0;
in attribute cooling_dirty_helium_positions_in : Real default := 28.0;
in attribute cooling_dirty_salt_positions_in : Real default := 28.0;
in attribute cooling_dirty_bundle_positions_in : Real default := 14.0;
in attribute helium_package_length_in : Real default := 6.0;
in attribute helium_package_width_in : Real default := 3.0;
in attribute helium_package_height_in : Real default := 4.0;
in attribute salt_package_length_in : Real default := 3.0;
in attribute salt_package_width_in : Real default := 2.0;
in attribute salt_package_height_in : Real default := 3.0;
in attribute hx_end_allowance_in : Real default := 2.0;
in attribute cooling_package_margin_in : Real default := 1.0;
in attribute cooling_aisle_width_in : Real default := 6.0;
in attribute cooling_cross_width_in : Real default := 17.0;
in attribute cooling_headroom_in : Real default := 9.0;
in attribute cooling_airlock_length_in : Real default := 17.0;
in attribute nuclear_wall_in : Real default := 2.0;
in attribute nuclear_floor_in : Real default := 1.0;
in attribute nuclear_roof_in : Real default := 1.0;
in attribute nuclear_rebar_density_in : Real default := 150.0;
in attribute conventional_wall_in : Real default := 0.3;
in attribute conventional_floor_in : Real default := 0.3;
in attribute conventional_roof_in : Real default := 0.2;
in attribute conventional_rebar_density_in : Real default := 100.0;
in attribute building_separation_in : Real default := 10.0;
in attribute external_access_width_in : Real default := 12.0;
in attribute provisional_envelope_scale_in : Real default := 1.0;
in attribute administration_occupants_in : Real default := 200.0;
in attribute control_occupants_in : Real default := 30.0;
in attribute security_occupants_in : Real default := 10.0;
in attribute administration_area_per_person_in : Real default := 12.0;
in attribute control_area_per_person_in : Real default := 15.0;
in attribute security_area_per_person_in : Real default := 12.0;
in attribute occupancy_circulation_factor_in : Real default := 1.3;
in attribute occupancy_height_in : Real default := 4.0;
in attribute occupancy_aspect_ratio_in : Real default := 2.0;
in attribute heat_rejection_length_in : Real default := 100.0;
in attribute heat_rejection_width_in : Real default := 60.0;
in attribute turbine_length_in : Real default := 60.0;
in attribute turbine_width_in : Real default := 20.0;
in attribute turbine_height_in : Real default := 15.0;
in attribute cryo_coldbox_length_in : Real default := 20.0;
in attribute cryo_coldbox_width_in : Real default := 12.0;
in attribute cryo_coldbox_height_in : Real default := 10.0;
in attribute cryo_compressors_length_in : Real default := 30.0;
in attribute cryo_compressors_width_in : Real default := 12.0;
in attribute cryo_compressors_height_in : Real default := 8.0;
in attribute fuel_length_in : Real default := 30.0;
in attribute fuel_width_in : Real default := 20.0;
in attribute fuel_height_in : Real default := 8.0;
in attribute reactor_aux_length_in : Real default := 30.0;
in attribute reactor_aux_width_in : Real default := 20.0;
in attribute reactor_aux_height_in : Real default := 10.0;
in attribute power_supply_length_in : Real default := 20.0;
in attribute power_supply_width_in : Real default := 10.0;
in attribute power_supply_height_in : Real default := 8.0;
in attribute onsite_ac_length_in : Real default := 16.0;
in attribute onsite_ac_width_in : Real default := 8.0;
in attribute onsite_ac_height_in : Real default := 6.0;
in attribute service_water_length_in : Real default := 20.0;
in attribute service_water_width_in : Real default := 15.0;
in attribute service_water_height_in : Real default := 8.0;
in attribute conventional_shop_length_in : Real default := 20.0;
in attribute conventional_shop_width_in : Real default := 15.0;
in attribute conventional_shop_height_in : Real default := 8.0;
in attribute site_services_length_in : Real default := 20.0;
in attribute site_services_width_in : Real default := 10.0;
in attribute site_services_height_in : Real default := 6.0;
in attribute n_mod_in : Real default := 0.0;
in attribute major_radius_in : Real default := 0.0;
in attribute minor_outer_radius_in : Real default := 0.0;
in attribute blanket_volume_in : Real default := 0.0;
in attribute calendar_q_in : Real default := 0.0;
in attribute calendar_fluence_in : Real default := 0.0;
in attribute calendar_years_in : Real default := 0.0;
in attribute calendar_outage_in : Real default := 0.0;
in attribute calendar_unplanned_in : Real default := 0.0;
in attribute calendar_mode_in : Real default := 0.0;
in attribute calendar_life_in : Real default := 0.0;
in attribute calendar_count_in : Real default := 0.0;
in attribute calendar_availability_in : Real default := 0.0;
in attribute cooling_circuits_in : Real default := 0.0;
in attribute cooling_helium_count_in : Real default := 0.0;
in attribute cooling_salt_count_in : Real default := 0.0;
in attribute cooling_bundle_count_in : Real default := 0.0;
in attribute cooling_machine_life_in : Real default := 0.0;
in attribute cooling_bundle_life_in : Real default := 0.0;
in attribute hx_shell_bore_in : Real default := 0.0;
in attribute hx_shell_wall_in : Real default := 0.0;
in attribute hx_shell_length_in : Real default := 0.0;
in attribute hx_tube_length_in : Real default := 0.0;
```
