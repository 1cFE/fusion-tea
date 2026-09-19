# Proposed facilities production contract

Date: 2026-09-18. Status: [AGENT] interface contract; T005 released at1e7fd0d7 and accepted by the coordinator. This artifact fixes names and ownership; reviewed `design.md` and `layout-capacity-design.md` govern equations. No production files were changed to prepare it. Read the latest B1/B2 repairs, especially initial demand, serialized internal carrier moves, corridor-side machines and class-specific wall/airlock offsets. The older preliminary footprint fields in the throwaway probe are not production outputs.

## Execution shape

Use three new manual-completion definitions: `Facility Layout`, `Facility Civil Cost`, and `Facility Shipping Scope`. The first owns the deterministic logistics, placement and material-quantity calculation. The second is a small reusable six-quantity/six-rate price calculation used by each building occurrence. The third validates and returns the combined shipping exclusions after CAS20 exists. Remaining selection, ventilation and aggregation arithmetic can use ordinary library expressions.

Keep the existing `stellaris.buildings` occurrence and its legacy `buildings_cost` calculation. Add the active layout there as `layout : 'Facility Layout'`. Every actual facility is a child occurrence of `buildings` with its own civil quantity attributes and `civil : 'Facility Civil Cost'`. `capital_cost` on each child is that child's normalized installed-direct civil price. The parent sums those modeled child capital costs. A hidden manual grand-total cost is not the CAS21 producer.

Proposed files are `models/library/analyses/mfe_facilities.sysml` for calculation/constraint definitions and `models/library/structure/mfe_facilities_parts.sysml` for `Facility Building` and `Facility Service Account`. `Facility Building` uses the existing costed-component interface. Existing generic `Buildings` receives the new occurrences/inputs; its existing capital-cost redefinition selects old versus new accounting after summation.

## Canonical occurrences

These names are exact. All are children of `stellaris.buildings`. Each row represents one separately inspectable costed occurrence; coincident dimensions do not permit replacing the four physical wings with an unexplained multiplier.

| Occurrence | Function / construction class |
|---|---|
| `reactor_hall` | Reactor hall; nuclear |
| `sector_wing_east`, `sector_wing_north`, `sector_wing_west`, `sector_wing_south` | Sector service, clean/dirty annexes and local airlocks; nuclear shared shell |
| `sector_link_east`, `sector_link_north`, `sector_link_west`, `sector_link_south` | Controlled radial transport links; nuclear |
| `cooling_hall` | Exchanger/machine cells and controlled carrier corridor; conventional construction assumption |
| `cooling_annex` | Clean/dirty stores, airlocks and overhaul stations; conventional construction assumption |
| `cooling_link` | Hall→annex controlled link; conventional construction assumption |
| `turbine_hall` | Provisional conversion envelope; conventional |
| `cryo_coldbox`, `cryo_compressors` | Separate provisional cryogenic equipment zones; conventional |
| `fuel_building` | Provisional fuel-processing/storage envelope; nuclear construction, controlled ventilation |
| `reactor_auxiliaries` | Provisional auxiliary-equipment room; conventional |
| `power_supply_building`, `electrical_building` | Distinct provisional electrical functions; conventional |
| `service_water_building` | Provisional water-service equipment; conventional |
| `maintenance_shop`, `site_services_building` | Conventional clean shop and site utilities |
| `administration`, `control`, `security` | Occupancy-based conventional buildings |
| `nuclear_ventilation` | Separate installed service cost; no civil shell |
| `site_improvements` | Explicit retained85MUSD allowance; no invented enclosed volume |

There are25 civil occurrences, plus the two non-civil accounts. `heat_rejection_plot` is a layout-only outdoor parcel, not a separately priced enclosed building. Existing CAS25 equipment cost remains its equipment owner.

## Input naming and defaults

Every scalar scenario attribute below lives on `buildings`; `Facility Layout` formal names append `_in` exactly. Physical data listed in the next section are read-only bindings, not duplicate study parameters. Unless noted Boolean, all are Real with normative units in comments. Every count must be integer-valued. Scenario names do not contain units, matching existing model style. Native generation lowers the two negative offsets `initial_sector_start_days=-120` and `cooling_initial_handoff_days=-30` as fixed-expression outputs, not entry parameters. Retain those fixed commissioning assumptions; do not sweep their computed channels. Receipt leads, task times, resource counts and storage holds remain public demand controls. [AGENT] This narrow interface clarification follows actual generation evidence and does not change either schedule.

Generic dormant defaults are `facilities_enabled=false`, `facilities_cost_mode=0`, `facilities_capacity_mode=0`. The stellarator active scenario sets true/1/1. Capacity mode0 holds offered positions fixed; mode1 sizes space to required positions. Neither mode changes crews, transport resources, component demand or calendar timing. Cost mode0 preserves old accounting while the enabled layout continues to calculate for matched comparisons. Validate the Boolean enable and both binary selectors first. Cost mode1 requires the layout enabled. Disabled/cost0 returns finite zero geometry/costs and satisfied dormant margins before checking unused geometry; capacity mode0 or1 is dormant-unused but must remain binary.

| Attributes | Stellarator scenario | Meaning |
|---|---|---|
| `facilities_enabled` |true|Boolean enable|
| `facilities_cost_mode`, `facilities_capacity_mode` |1,1|Binary selectors|
| `sector_count`, `sector_bays`, `sector_service_teams` |4,4,2|Supported topology and offered resources|
| `exterior_allowance`, `sector_route_clearance`, `sector_headroom` |2,6,3|m; provisional exterior envelope, package corridor/turn square, overhead room|
| `component_width`, `component_height`, `component_length` |4,2,2|m; assumed handling-package dimensions|
| `component_handling_margin`, `component_material_fraction` |0.5,0.5|m per face; fraction of blanket material occupying package volume|
| `divertor_packages_per_sector`, `waste_package_yield` |4,1|Separate assumed divertor segmentation; storage packages per removed unit|
| `component_remove_days`, `component_install_days` |0.5,0.5|Calendar days/unit|
| `sector_clean_days`, `sector_test_days` |7,7|Controlled-bay transition/setup and testing; no activation clearance|
| `sector_split_days`, `sector_join_days`, `sector_transport_days` |7,7,2|Calendar days; each loaded sector trip reserves transport|
| `cooldown_days`, `recommission_days` |30,30|Source assumptions already inside the offered outage|
| `initial_receipt_lead_days`, `initial_sector_start_days` |180,-120|Initial in-vessel receipt before day0; initial sector assembly start|
| `component_receipt_lead_days`, `component_prepare_days` |90,1|Recurring clean receipt lead; per-unit preparation|
| `component_process_days`, `component_hold_days` |1,365.25|Dirty integrated processing/unit; completed-storage hold|
| `clean_positions`, `dirty_buffer_positions`, `dirty_store_positions` |36,18,36|Per-wing fixed-offer positions|
| `cooling_initial_receipt_lead_days`, `cooling_initial_handoff_days` |180,-30|Initial cooling receipt and handoff campaign|
| `cooling_receipt_lead_days`, `cooling_hold_days` |90,365.25|Recurring lead; completed dirty hold|
| `cooling_prepare_stations`, `cooling_machine_stations`, `cooling_bundle_stations` |2,2,2|Persistent resources; helium/salt share machine stations|
| `cooling_prepare_machine_days`, `cooling_prepare_bundle_days` |0.5,1|Preparation/unit|
| `cooling_machine_process_days`, `cooling_bundle_process_days` |2,5|Dirty service/unit|
| `cooling_field_cycle_days`, `cooling_internal_move_days` |0.2,0.1|One serialized carrier; field paired cycle or internal move|
| `cooling_clean_helium_positions`, `cooling_clean_salt_positions`, `cooling_clean_bundle_positions` |29,29,14|Plant-total fixed clean offers, including one spare of each machine type|
| `cooling_dirty_helium_positions`, `cooling_dirty_salt_positions`, `cooling_dirty_bundle_positions` |28,28,14|Plant-total dirty bank offers; queue and finished inventory share these banks|
| `helium_package_length`, `helium_package_width`, `helium_package_height` |6,3,4|m; provisional package envelope|
| `salt_package_length`, `salt_package_width`, `salt_package_height` |3,2,3|m; provisional package envelope|
| `hx_end_allowance`, `cooling_package_margin`, `cooling_aisle_width`, `cooling_cross_width` |2,1,6,17|m; end allowance, per-face handling margin, longitudinal/cross route widths|
| `cooling_headroom`, `cooling_airlock_length` |9,17|m; clear building height and airlock length|
| `nuclear_wall`, `nuclear_floor`, `nuclear_roof`, `nuclear_rebar_density` |From combined construction table|m,m,m,kg/m³; one source of truth for layout and takeoff|
| `conventional_wall`, `conventional_floor`, `conventional_roof`, `conventional_rebar_density` |From combined construction table|m,m,m,kg/m³|
| `building_separation`, `external_access_width` |10,12|m; conceptual spacing/site-strip assumptions|
| `provisional_envelope_scale` |1|Uniform multiplier on provisional conventional equipment L/W/H only; not on calculated reactor/cooling dimensions|
| `administration_occupants`, `control_occupants`, `security_occupants` |200,30,10|Concurrent occupancy assumptions; no payroll change|
| `administration_area_per_person`, `control_area_per_person`, `security_area_per_person` |12,15,12|m²/person|
| `occupancy_circulation_factor`, `occupancy_height`, `occupancy_aspect_ratio` |1.3,4,2|fraction, m, L/W|

The fixed provisional conventional envelopes are also public attributes. For each stem `turbine`, `cryo_coldbox`, `cryo_compressors`, `fuel`, `reactor_aux`, `power_supply`, `onsite_ac`, `service_water`, `conventional_shop`, `site_services`, define exactly `<stem>_length`, `<stem>_width`, `<stem>_height` with the L/W/H values in the reviewed table. Define `heat_rejection_length=100`, `heat_rejection_width=60`. The source/assumption register must identify these as provisional, not equipment calculations. Constant aisle/rack arrangements from the design are normative geometry rules; do not create dozens of extra continuous optimization levers for them.

Price-only attributes are `sub_concrete_rate`, `sub_formwork_rate`, `sub_rebar_rate`, `super_concrete_rate`, `super_formwork_rate`, `super_rebar_rate`, `civil_cpi_ratio`, `civil_rate_multiplier`, `tonne_interpretation_kg`, `ventilation_coefficient`, `ventilation_exponent`, `ventilation_cpi_ratio`, `land_rate_per_acre`, `retained_site_improvements`. Bind exact reviewed source rates and CPI ratios in the stellarator instance; generic defaults are dormant-safe. `tonne_interpretation_kg` scales only the source TN→kg rate convention, relative to907.18474; it does not scale physical rebar mass. Price inputs do not feed layout, capacity or physical calendar calculations.

## Existing-owner inputs and necessary exposures

| `Facility Layout` formal | Binding/source |
|---|---|
| `n_mod_in` |Existing plant module count; active supports1|
| `major_radius_in`, `minor_outer_radius_in`, `blanket_volume_in` |Live plasma R; radial-build outer radius through low-temperature shield; existing blanket material volume|
| `calendar_q_in`, `calendar_fluence_in` |The exact peak wall-load/fluence operands used by the existing calendar|
| `calendar_years_in`, `calendar_outage_in`, `calendar_unplanned_in`, `calendar_mode_in` |Existing plant operational years, outage years, unplanned fraction, held/live switch|
| `calendar_life_in`, `calendar_count_in`, `calendar_availability_in` |Existing calendar output interfaces, for semantic-consistency assertions|
| `cooling_circuits_in`, `cooling_helium_count_in`, `cooling_salt_count_in`, `cooling_bundle_count_in` |Actual executed cooling circuit and equipment counts|
| `cooling_machine_life_in`, `cooling_bundle_life_in` |Existing cooling lifecycle assumptions; do not add independent facility lifetimes|
| `hx_shell_bore_in`, `hx_shell_wall_in`, `hx_shell_length_in`, `hx_tube_length_in` |Cooling's actual priced construction geometry; proposed pure exposures below|

Add pure producer exposures `radial_outer_radius` on the plant (from a new explicit `outer_radius` output of the existing radial build), `calendar_physical_life`, `calendar_replacement_count`, `calendar_availability` where a suitable existing sibling exposure is absent. Do not rename existing attributes. On heat transport expose `hx_shell_bore`, `hx_shell_wall`, `hx_shell_length`, `hx_tube_length`, `helium_machine_count`, `salt_machine_count`, `exchanger_count` from its actual equipment definition/calculation. If fixed geometry presently exists only as normative constants in the manual body, expose that same constant once at its owning definition and bind both pricing and facilities to it; do not maintain a second unverified13 m literal solely in facilities. This narrow upstream ABI change must preserve all existing equipment values and prices.

The production `Facility Layout` completion calls the existing `lifecycle_calendar_live` function for dates, using exactly the calendar's q, fluence, N, d and u; cost/discount/coil-life arguments can be neutral because they do not enter event timing. Compare returned life/count/availability to the bound owner outputs and raise on mismatch. The calendar loop is not copied. Active held-calendar mode is unsupported and raises. The independent oracle uses its own already-established calendar reference, not the production facilities helper.

## Layout scalar outputs

All native output stems below are exact. `buildings` exposes them unchanged as sibling attributes so consumers bind the producer occurrence. `Facility Layout` returns finite scalars only. Full rectangle, opening and event/job ledgers are deterministic diagnostics returned by a separately callable helper using the same inputs; study evidence writes them by native case ID and hashes the artifact. Do not truncate event lists to a fixed native-array length.

| Group | Output names |
|---|---|
| Scenario | `active`, `cost_mode`, `capacity_mode` |
| Geometry | `sector_length`, `sector_width`, `sector_height`, `parcel_area`, `controlled_air_volume`, `total_clear_area`, `total_gross_area`, `total_air_volume` |
| In-vessel quantities | `blanket_packages_per_sector`, `packages_per_sector`, `material_capacity_volume`, `unused_material_capacity`, `initial_clean_required`, `dirty_buffer_required`, `dirty_store_required` |
| Timing | `initial_ready_margin_days`, `replacement_ready_margin_days`, `outage_required_days`, `outage_allowed_days`, `outage_margin_days`, `calendar_event_count`, `calendar_first_event_year`, `calendar_last_event_year` |
| Cooling required stocks | `cooling_clean_helium_required`, `cooling_clean_salt_required`, `cooling_clean_bundle_required`, `cooling_dirty_helium_required`, `cooling_dirty_salt_required`, `cooling_dirty_bundle_required` |
| Cooling queue diagnostics | `cooling_helium_queue_peak`, `cooling_salt_queue_peak`, `cooling_bundle_queue_peak`, `cooling_initial_ready_margin_days`, `cooling_replacement_ready_margin_days`, `cooling_jobs_after_shutdown`, `cooling_last_release_year`, `cooling_carrier_moves` |
| Allocated space | `clean_positions_allocated`, `dirty_buffer_positions_allocated`, `dirty_store_positions_allocated`, `cooling_clean_helium_allocated`, `cooling_clean_salt_allocated`, `cooling_clean_bundle_allocated`, `cooling_dirty_helium_allocated`, `cooling_dirty_salt_allocated`, `cooling_dirty_bundle_allocated` |
| Native predicate operands | `initial_margin_days`, `readiness_margin_days`, `capacity_margin_units`, `route_margin_m` |
| Qualification disclosure | `exterior_envelope_qualified`, `sector_load_qualified`, `contamination_procedure_qualified`, `cooling_outage_basis_resolved`, `provisional_room_count` |

For no recurring events, first/last event and last-release outputs use0 with corresponding count0. Initial demand/readiness remains evaluated. No-event readiness margin uses the finite horizon length in days as its satisfied sentinel. Qualification outputs are0 in the current conceptual scenario; these are disclosures, not claims satisfied by an unrelated geometric margin.

`initial_margin_days` is the minimum in-vessel/cooling initial-readiness margin. `readiness_margin_days` is the minimum recurring clean-readiness margin. `capacity_margin_units` is the minimum allocated-minus-required margin across sector bays, clean/buffer/storage and all cooling banks. Fixed-offer mode allocates configured counts; resized mode allocates required storage counts, but sector bays/resources remain configured. `route_margin_m` is the minimum of required door/aisle/turning/linear clearance checks; any rectangle intrusion yields a negative margin. A lack of mechanical qualification remains a separate0 disclosure, not an invented positive clearance margin.

For each of the25 civil occurrence names C above, append each suffix in this exact list to form the output `<C>_<suffix>`:

`clear_length`, `clear_width`, `clear_height`, `clear_area`, `gross_area`, `air_volume`, `sub_concrete`, `super_concrete`, `sub_formwork`, `super_formwork`, `sub_rebar`, `super_rebar`.

Units are m, m, m, m², m², m³, m³, m³, m², m², kg, kg respectively. This Cartesian product is the complete300-name civil-output contract, not a choice of whichever quantities happen to generate. Parent pure EXPOSE attributes retain these names. Child C receives its twelve unprefixed properties from them. Whole-wing quantities include its shell, main partitions and actual airlock walls once; no extra costed annex child duplicates that material.

## Civil price and accounting interfaces

`Facility Civil Cost` inputs are `enabled_in`, the six quantity formals `sub_concrete_in`, `super_concrete_in`, `sub_formwork_in`, `super_formwork_in`, `sub_rebar_in`, `super_rebar_in`, and the six rates plus `civil_cpi_ratio_in`, `civil_rate_multiplier_in`, `tonne_interpretation_kg_in`. Outputs are `sub_cost_2018`, `super_cost_2018`, `cost_2018`, `cost_2025`. Enabled active quantities/rates must be finite/nonnegative; disabled returns zero before unused geometry/rate validation. Use exact source precision and the selected TN interpretation; no installation factor is added.

`Facility Ventilation Cost` is ordinary arithmetic with `served_volume_in`, `coefficient_in`, `exponent_in`, `cpi_ratio_in`; outputs `cost_1990`, `cost_2025`. The source empirical coefficient is not a linear volume price. `nuclear_ventilation.capital_cost=cost_2025`. Dormant served volume0 produces zero.

Expose on `buildings`: `civil_capital` as the sum of all25 civil children; `installed_facility_capital=civil_capital+nuclear_ventilation.capital_cost`; `layout_buildings_capital=installed_facility_capital+site_improvements.capital_cost`; `layout_land_cost` from parcel m²/4046.8564224 × inherited land price. Preserve the existing `buildings_cost.cost` as the legacy subtotal. The selected `buildings.capital_cost` is the binary old/new expression; no downstream manual grand total replaces the child sum.

On the generic plant, the existing preconstruction selection becomes legacy `precon_cost.cost` in mode0, and fixed preconstruction adders + `buildings.layout_land_cost` in mode1. Preserve its published `preconstruction_capital` name. Selected facility shipping exclusion is `facilities_cost_mode*(1+plant_contingency_rate)*buildings.installed_facility_capital`, excluding retained site improvements. Preserve the existing delivered-cooling exclusion unchanged.

Add `shipping_scope : 'Facility Shipping Scope'` after CAS20 exists. Inputs are `cas20_in`, `cooling_exclusion_in`, `facility_exclusion_in`. Outputs are `cooling_exclusion`, `facility_exclusion`, `remaining_shipping_base`. Validate finite nonnegative exclusions and `cooling+facility<=cas20`; raise on invalid scope, never clamp. Wire the validated facility exclusion into a new default-zero `facility_exclusion_in` on the existing `Supplementary Cost` calculation. Its shipping term becomes `shipping*(cas20 - cooling_delivered_in - facility_exclusion_in)`, with all other terms unchanged. The validated cooling output can replace the identical direct binding to enforce dependency order. This is downstream-only and cannot feed the CAS21 selector, avoiding a cycle.

## Native executable predicates

Define one reusable `Facility Nonnegative Margin` constraint with `margin_in : Real` and expression `margin_in >= 0.0`. Add these five exact assert occurrence names on the generic plant so the native catalog/store carries outcomes:

| Assert occurrence | Bound operand |
|---|---|
| `facility_initial_ready` |`buildings.initial_margin_days`|
| `facility_replacement_ready` |`buildings.readiness_margin_days`|
| `facility_outage_ok` |`buildings.outage_margin_days`|
| `facility_capacity_ok` |`buildings.capacity_margin_units`|
| `facility_routes_ok` |`buildings.route_margin_m`|

Dormant margins are1 so legacy other-family instances remain supported. Active shortages yield finite negative margins and native `violated` results. Do not put these tests only in detached diagnostic JSON. Do not add `qualification_complete` as a pretend engineering certification. Processing after shutdown and queue persistence are reported; they are not automatically infeasible if declared storage/resources support them. Preserve all existing physical predicates and their current adverse outcomes.

The native generated predicate operand references, type names and counts must be explicitly mapped in `studies/oracle_entry.py`, manifest contracts and the relevant tests. These names are semantic contract names; read actual generated wrapper output order rather than assuming declaration order. Record that order in `evidence/facilities-generated-abi.json` before implementation tuples are finalized.

## Independent consumer handoff

The independent author owns `exploration/stellarator_e2e/oracle_facilities.py`, `verify_stellaris.py` facility integration and `studies/oracle_entry.py` input/output/predicate mappings after explicit assignment by the coordinator. Do not import production `Facility Layout` or its internal geometry/scheduler into the oracle. Reuse the reviewed contract, exact source rows and the existing independently checked calendar oracle. Check count/occupancy/rectangle/material/account identities and counterexamples independently rather than only matching a copied formula.

Public entry paths follow the existing canonical form, for example `stellarator_09__stellaris__buildings__component_hold_days`. Layout output paths use `stellarator_09__stellaris__buildings__layout__dirty_store_required`; child costs use `stellarator_09__stellaris__buildings__reactor_hall__civil__cost_2025`. Map the complete declared outputs explicitly, including disabled mode and no-event sentinels. Reuse upstream R/a/circuit/calendar entry names so matched studies do not set two inconsistent copies.

## Affected files and controlled sequence

| Owner | Files |
|---|---|
| Model author | New analyses/structure files above; `models/designs/generic_mfe/mfe_subsystems.sysml`; `models/designs/generic_mfe/mfe_plant.sysml`; `models/designs/stellarator_09/stellarator_plant.sysml`; narrow exposure changes in radial-build/cooling definitions and their normative implementations |
| Model/generation author | `tests/model_families.py`; synchronized `exploration/stellarator_e2e/models/`; new generated facility wrappers/schemas and handwritten bodies; required updated cooling/radial wrappers; new WI-068 `evidence/regenerate.py`, `candidate-seeds.json`, `repin.py`, ABI evidence; `tests/models/current_mfe_regressions.py`; affected family-spine ABI expectations; focused `tests/models/test_layout_facilities.py` |
| Independent oracle author | `exploration/stellarator_e2e/oracle_facilities.py`, `verify_stellaris.py`, `studies/oracle_entry.py` |
| Coordinator/native producers | Goal records/study; manifest/census/snapshot regeneration and reviewed commits/integration. Do not hand-edit generated identity results. |

The new recipe must preserve31 entering normative bodies plus the three new manual definitions, while explicitly approving any necessary upstream exposure-body revision. The count is not a substitute for actual reviewed hashes. Use the generation handoff's current recipe pointer/ABI union changes and fresh two-run byte comparison. Test recipe pointer must move to WI-068. Run no generation or repinning under the old WI-067 recipe. Production released by the coordinator after the fresh review PASS.


[AGENT implementation clarification] The two negative phase offsets `initial_sector_start_days=-120` and `cooling_initial_handoff_days=-30` remain fixed instance expressions, because native generation lowers negative literals as output expressions. They remain layout formals but are excluded from public entry parameters. Other receipt/task/hold inputs remain public. Recurring in-vessel readiness compares batch preparation with campaign start, not later installation; see the reviewed clarification in `layout-capacity-design.md`.


[AGENT implementation clarification, coordinator accepted2026-09-18] The cooling service room offers two machine stations and two bundle stations. Capacity margin also includes `2-cooling_machine_stations` and `2-cooling_bundle_stations`; larger requested resources fail capacity without inventing space. Clean preparation resources work on occupied clean positions and are not subject to this service-room limit. `clear_length` and `clear_width` bound the inside of the whole shell; `clear_area` subtracts every actual internal wall footprint. The fixed hall margin is2m, separate from the6m sector corridor.


[AGENT reviewer hold repairs] `waste_package_yield>=1` is an active-domain condition; values below1 are rejected, not used to remove demanded waste storage. Initial cooling margin includes preparation by day-30 and final initial carrier return by day0. All helium/salt/bundle carried dimensions enter the common route/door/service-slot checks. Hall machine strip and service centers/depth follow the larger carried machine length, and service width follows the largest carried width. These corrections reuse existing native margin outputs; the production input/output names remain unchanged.


All six cooling clean/dirty helium/salt/bundle offered-position inputs are integer counts; fractional offered positions are rejected before layout allocation.
