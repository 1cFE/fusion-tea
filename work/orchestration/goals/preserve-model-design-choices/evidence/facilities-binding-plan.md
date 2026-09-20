# Facilities supplied-design binding and acceptance plan

[AGENT] Proposed contract for independent review before production edits, 2026-09-20. Scope: facilities only. This follows MR-7 and the owner's quoted intent in `inventory-brief.md`; findings are in `facilities-fuel-inventory.md`. This plan has not been implemented or behaviorally validated. No reference outputs determine defaults or equations.

[INHERITED: coordinator task] Retain the existing four-wing topology explicitly; introduce independently supplied room dimensions, parcel, storage positions and blanket segmentation count. The coordinator's instruction is task scope, not additional owner-originated scientific authority. All variable names, geometric conventions and migration mechanics below are agent proposals.

## Evaluation contract

A facility evaluation consumes a supplied design and upstream operating/equipment requirements. It must not call a layout-selection policy. Required envelope, position demand and minimum blanket package count are outputs. Civil quantities, ventilation proxy and land price use the supplied design even when represented fit fails. In-domain insufficiency returns ordinary results plus failed constraints; malformed solids, nonfinite inputs and unsupported topology return explicit unsupported/invalid evaluation, never a pass.

The supported layout remains one module, four sector wings around the reactor hall, a cooling hall connected to one cooling annex, and the existing campus row. This is a declared topology choice. Room coordinates follow deterministic attachment rules from supplied room and link dimensions; they are not moved to eliminate collisions. Other topologies remain unsupported. Independent coordinates and arbitrary floorplans are outside this contract.

The evaluator neither buys additional packages nor invents storage positions. A new standalone proposal/migration helper may apply the entering layout policy once and return all supplied-design values. That helper is not a required execution path and must never run implicitly when fields are absent. The minimum-requirement calculations may be used by a later explicit search policy; no ongoing automatic sizing study is required for this repair.

## Exact public input and binding changes

### Room geometry

Add `selected_<room>_length`, `selected_<room>_width`, `selected_<room>_height`, all in metres, to `Buildings` in `models/designs/generic_mfe/mfe_subsystems.sysml`. Add matching `*_in` inputs to `Facility Layout` in `models/library/analyses/mfe_facilities.sysml`, with direct `in selected_<room>_<axis>_in = selected_<room>_<axis>` bindings. The exact 25 room stems are:

```text
reactor_hall
sector_wing_east
sector_wing_north
sector_wing_west
sector_wing_south
sector_link_east
sector_link_north
sector_link_west
sector_link_south
cooling_hall
cooling_annex
cooling_link
turbine_hall
cryo_coldbox
cryo_compressors
fuel_building
reactor_auxiliaries
power_supply_building
electrical_building
service_water_building
maintenance_shop
site_services_building
administration
control
security
```

Each existing output `<room>_clear_length/width/height` equals the corresponding selected input exactly. Existing `<room>_clear_area`, gross area, air volume and six sub/super commodity outputs retain their names and are computed from these dimensions and chosen wall/floor/roof/rebar properties. This preserves the 25 actual component bindings and cost rollup without treating output-derived dimensions as new selectors.

Add `selected_cooling_helium_store_width`, `selected_cooling_salt_store_width`, `selected_cooling_bundle_store_width` and `selected_cooling_annex_north_depth` (m). These specify the annex's existing three storage strips and the position of its transverse centerline. Without these fields, the current partition positions change with required equipment widths and still change concrete at fixed room dimensions. Annex service-strip width is the remaining selected width after the three selected strip widths and three partition thicknesses; south depth is selected total length minus selected north depth. Negative remainder or crossing partitions is invalid geometry, not an equipment shortfall. Existing airlock length, cross width and wall thickness define the fixed partition offsets from that centerline. No `max(required_depth, selected_depth)` occurs.

The four wings retain their existing 28 m clean and dirty bands and two partition walls as an explicit inherited floorplan. For each independently selected wing width W, its installed lane width is `W - 56 - 2*nuclear_wall`. Wing partition lengths follow that wing's selected length. Physical openings retain the existing six 6×6 m component airlocks and a sector passage across the selected lane. The sector passage height follows the selected wing height. A nonpositive lane or opening larger than its wall is malformed geometry; an ordinary positive lane narrower than the required sector is a failed fit. Retaining the 28 m/6 m topology constants does not establish qualified storage or transport. Their chosen values and meaning must be documented in the model contract.

Cooling hall has no new demand-driven walls: its outer dimensions are selected, and its existing cross opening uses the chosen cross width and selected height. Requirements for equipment cells and withdrawal space are calculated independently. Annex internal service-slot centers are diagnostic layout coordinates calculated within the selected service region; they do not enlarge the region. Two machine and two bundle service positions remain the declared topology capacity. The existing station-count request check is retained.

### Storage, packages and parcel

Keep the nine exact supplied position names: `clean_positions`, `dirty_buffer_positions`, `dirty_store_positions`, and `cooling_{clean,dirty}_{helium,salt,bundle}_positions`. They always bind unchanged to the corresponding `*_allocated` outputs. Delete `facilities_capacity_mode` from the repaired public interface, input schema, stellarator instance and output contract (`capacity_mode`). Its historical meaning is preserved only in historical packages and the one-shot migration helper. Do not silently retain a mode that ignores the supplied design. `facilities_cost_mode` remains the distinct legacy/layout accounting selector.

Add `selected_blanket_packages_per_sector` (integer count, zero permitted). Keep `divertor_packages_per_sector` as the existing independent chosen count. Set total scheduled packages to their sum; all removal/installation/preparation jobs and occupancy intervals use this chosen sum. Calculate `blanket_packages_required_per_sector = ceil(blanket_volume / (4*component_material_fraction*component_width*component_height*component_length))` as a requirement only. Existing `blanket_packages_per_sector` exposes the selected count; `material_capacity_volume = 4*selected_blanket_packages_per_sector*component_material_fraction*component_width*component_height*component_length`; existing `unused_material_capacity` remains its signed difference from blanket volume. Empty package schedules must be handled without `max(empty)` failures. Package solids/material capacity are conceptual packaging, not new physical segmentation qualification.

Add `selected_parcel_x_min`, `selected_parcel_y_min`, `selected_parcel_length`, `selected_parcel_width` (m). Existing `parcel_area` becomes exactly selected length×width. Length and width must be positive; signed coordinates may be any finite real. Existing external-access width remains the required perimeter-access allowance. Compute occupied campus bounds plus that allowance as a requirement; compare each edge against the selected parcel. Do not recenter, translate or enlarge the parcel to fit. Expose `required_parcel_x_min/y_min/x_max/y_max` and `parcel_fit_margin_m` (minimum signed edge clearance).

### Existing inputs that cease selecting buildings

Keep upstream major/minor radius, blanket volume, cooling counts and exchanger geometry as equipment/operating facts. They only calculate requirements and fit after this repair. Keep component envelope dimensions, clearance requirements, nuclear/conventional section properties, timing/resource policy, prices and calendar inputs with their existing meanings.

Keep the ten equipment-envelope input triples (`turbine`, `cryo_coldbox`, `cryo_compressors`, `fuel`, `reactor_aux`, `power_supply`, `onsite_ac`, `service_water`, `conventional_shop`, `site_services`), `provisional_envelope_scale`, occupancy counts/area/person/circulation/height and `exterior_allowance`, `sector_route_clearance`, `sector_headroom`, `hx_end_allowance`, cooling package margin/headroom/aisle/cross/airlock as declared envelope and clearance assumptions. They no longer overwrite room L/W/H. The current fixed equipment-room allowances of +4 m length/width and +3 m height remain explicit provisional clearance requirements; applying them does not qualify the equipment. `occupancy_aspect_ratio` becomes a proposal-only input and is removed from the evaluation interface: adequate office area/height is evaluated independently of the suggested proportion. `building_separation` remains the chosen campus-row gap; selected link lengths determine the gaps actually spanned by the five links.

## Geometry and minimum honest checks

Keep dimensioned checks separate: count shortfalls in `capacity_margin_units`, distances in `route_margin_m` or new geometric margin outputs, material volumes in `unused_material_capacity`, occupancy areas in a separate area output. Never mix m² or m³ into the count or distance minimum.

| Check | Required calculation | Supplied quantity / result |
|---|---|---|
| Blanket packaging | Existing volume/(four sectors×usable package volume), including integer requirement diagnostic | Selected package count; new `facility_material_capacity_ok` asserts `unused_material_capacity >= 0` |
| Storage operational peaks | Existing dated vessel/cooling interval logic | Nine selected allocations minus required counts; existing capacity predicate |
| Sector body and passages | Existing sector envelope `b`, `sqrt(2)*b`, and vertical envelope from upstream radii/allowance; clearance terms remain declared assumptions | Each wing's selected length/height/lane and each link's selected width/height, plus reactor hall footprint/height. Report negative margins; never set width from envelope. |
| Component storage fit | Current fixed four-column, 6 m pitch storage layout, with existing aisle/end allowances | Required length for selected clean and dirty allocation versus each selected wing length; compare package envelope to the inherited cell/door dimensions. A slot offer does not establish the slots fit inside a building. |
| Cooling operating hall | Existing circuit-cell requirement, equipment dimensions and bundle withdrawal envelope | Required hall length/width/height compared with selected hall; selected equipment itself remains unchanged |
| Cooling storage strips | Existing two-column pitch and row-count rule applied to selected clean/dirty offers, not calendar-required offers | Chosen strip width and available north/south depth after cross/airlock offsets; keep distinct signed width/depth margins |
| Cooling service and carrier route | Existing bundle/machine envelopes, declared aisles, doors and two service slots | Chosen service region and fixed route openings; reject insufficient fit through margin. Do not size service width from envelope. |
| Ten provisional rooms | Existing equipment-envelope scale and fixed declared clearance allowances | Per-room selected L/W/H minus requirement; preserve provisional status |
| Three occupancy rooms | Occupants×area/person×circulation and specified minimum height | Selected usable area and height; new `occupancy_area_margin_m2` plus distance margin. No hidden aspect selection. |
| Campus and parcel | Chosen room outer footprints, fixed attachment/row topology, chosen gaps, heat-rejection plot and access allowance | Signed overlap checks and selected parcel edge clearances; no collision-avoidance repositioning |

Add `geometry_fit_margin_m` and `occupancy_area_margin_m2`, with `facility_geometry_ok` and `facility_occupancy_ok` assertions. Add `facility_parcel_ok` on `parcel_fit_margin_m`. Preserve `facility_routes_ok` for route-specific margins. Keep a named diagnostic map of individual clearances so the aggregate predicate is auditable. Expose required L/W/H for every room as `<room>_required_length/width/height` only where all three are meaningful; occupancy rooms instead expose required area and height. None of these requirements feeds a selected attribute.

Attachment rules: locate reactor hall at the origin with its selected rectangular outer footprint. Attach each wing beyond its corresponding selected link length, with passage centerlines aligned to the relevant hall-side midpoint. Use actual selected wing/link widths, not one common wing width. Link outer L/W/H and wing passage width/height must be mutually compatible; report signed fit/connection diagnostics. Place cooling hall east of the actual easternmost wing boundary plus chosen campus gap; place annex beyond the selected cooling-link length. Arrange the unchanged campus row south of the actual southernmost reactor/wing boundary, using selected outer room sizes plus chosen gaps. These are explicit placement conventions, not an optimization. They may produce overlapping or disconnected designs; connection and overlap checks retain those failures. Only intended adjoining faces are allowed; nonzero overlapping footprint interiors fail.

For civil accounting, partition solids must be entirely contained in their selected room. Unsupported crossing partitions or impossible apertures are explicit invalid geometry, rather than a negative wall mass that propagates as a cheap design. Acceptance undersizing cases deliberately stay within this constructible-geometry domain. This domain restriction must not be used to reject every ordinary insufficient equipment-fit case.

Controlled ventilation volume must be recomputed from actual selected served regions: reactor hall, each selected wing's clean band and lane, sector links and fuel building, minus actual represented internal wall solids. Do not retain `4*((lane+28)*L*H)` once wings differ. Keep the existing ventilation cost law as an explicitly unqualified volume proxy. Land and preconstruction use selected parcel area. Six commodity prices, CPI/rate/tonne interpretation and shipping exclusions remain unchanged; prices follow selected solids even if equipment will not fit.

## File and interface implementation map

| File / surface | Required edit |
|---|---|
| `models/library/analyses/mfe_facilities.sysml` | Add 75 selected room inputs, four annex partition inputs, selected package count and four parcel inputs; remove evaluation capacity mode and occupancy aspect; add requirement/fit outputs and their unit comments; document fixed topology and explicit unsupported geometry. Civil and cost helper equations retain their current meanings. |
| `models/designs/generic_mfe/mfe_subsystems.sysml` | Declare each selector and bind one-to-one into layout. Expose new margins/requirements. Existing room outputs and 25 component commodity bindings remain. Replace any served-volume or parcel binding that still references requirements. |
| `models/designs/generic_mfe/mfe_plant.sysml` | Add material, geometry, occupancy and parcel assertions with correct dimensioned operands; preserve existing five predicates. |
| `models/designs/stellarator_09/stellarator_plant.sysml` | Replace capacity-mode choice with literal captured selected fields, selected package count and nine captured allocations. Add provenance of entering-design migration. No field remains an expression referencing required outputs. |
| `exploration/stellarator_e2e/generated/handwritten/mfe_facilities/facility_layout_impl.py` | Refactor `vessel_schedule` to use selected count; `geometry` to consume selected dimensions/partitions and compute requirements separately; `diagnostics` to preserve allocations; update validation, field catalogs and named diagnostic outputs. Preserve the calendar and queue algorithms unless a test exposes a bug. |
| `exploration/stellarator_e2e/models/` and generated modules/schemas/contracts | Use the prescribed staging/generation/integration process to regenerate from production SysML. Expected changed surfaces include layout module/input model, layout output schema, `stellarator_plant_params.py`, `model_contract.json`, generation manifest and native wiring. No manual editing of generated graph/contract substitutes for regeneration. |
| `exploration/stellarator_e2e/oracle_facilities.py` | Independently calculate selected solids, material/position/fit/parcel margins and price propagation from this reviewed contract. Replace current automatic `resize` branch and geometric selection; do not import production geometry or copy its output as expected data. Preserve source-price arithmetic. |
| `tests/models/test_layout_facilities.py`, `tests/models/test_facilities_oracle.py` | Replace old default policy assumptions with explicit fixture designs. Add native cases below and independent arithmetic comparisons. Existing historical WI-068 evidence contract JSON remains unchanged; new fixtures add selected values explicitly instead of rewriting historical evidence. |
| Current study/integration verification and indicator catalogs | Update contract-qualified keys, newly exposed outputs/predicates, supported aliases and oracle mappings. New package records declare breaking interface migration. Historical immutable packages/studies retain their original interfaces and evidence. |

`Facility Civil Component` in `models/library/structure/mfe_facilities_parts.sysml` already consumes explicit commodity inputs; no new price equation is needed. Any actual edit there should be limited to clarifying supplied-geometry provenance. Native integration must prove the unchanged rollup receives selected solids through all 25 occurrences.

## Entering-design migration and defaults

Capture the entering generated package identity and exact baseline input bundle before modification. Run the supported native evaluator and record every room's existing clear dimensions, nine allocated positions, existing blanket package count and parcel bounds. Also capture the four internal annex partition selections from entering diagnostics. Persist this as a versioned migration record with source commit/package/input hashes. The proposed new literal defaults reproduce the entering design, not a reference reactor and not the outputs of a later fit optimization.

The runtime path for this capture is the repository-prescribed `.codex-test/run` and native study route; read `.project/codex-test-setup.md` first. This plan does not claim capture has happened. Full-precision finite values must come from actual entering evaluation, not values manually inferred from rounded reports. The migration record stores quantities and units as well as qualified parameter keys. The entering auto policy may be invoked only during this explicit capture/proposal operation; subsequent evaluations accept the saved design without that policy.

Generic new selectors may use dormant-safe zero placeholders, but active facilities must require valid supplied geometry. Only the stellarator instance binds the captured active design. Missing active selectors must fail input/domain validation rather than call auto-selection. Zero selected package count and zero storage positions are valid offered capacities and must yield failed constraints when demand is positive. Removed capacity-mode and occupancy-aspect keys must be rejected by new-package admission with a documented migration message, not accepted and ignored. An independent study that wants a different design must supply it explicitly.

Baseline parity is a migration check, not a success target. Any new negative fit margins revealed in the captured design remain negative. Do not enlarge defaults to obtain a pass. Changes in previously computed concrete or served air volume caused by correcting inconsistent geometry must be individually explained; do not tune dimensions to recover old capital totals.

## Native acceptance matrix

Use the existing supported test route in `tests/models/test_layout_facilities.py:80`: prepare the regenerated candidate through `studies/study_route.py`, construct candidates with `simkit.study.bridge.CandidateBridge`, and evaluate actual store outputs and concrete constraint catalog entries. Every change uses qualified public inputs `stellarator_09__stellaris__buildings__<selector>`. Compare admitted entry values, outputs, predicates, component cost quantities and final capital/land/ventilation channels. Helper-level arithmetic tests supplement this route; they do not replace it.

| Case | Native change and required result |
|---|---|
| Entering-design replay | Supplied migration bundle reproduces selected dimensions/positions/package count exactly and reproduces baseline quantities/cost within documented numeric tolerances, apart from individually explained corrections. Report new failed checks honestly. |
| Blanket package shortfall / sufficient | Pick count immediately below and at the computed minimum, positive demand. Selected count is unchanged; signed material volume/predicate cross zero. Schedule jobs, occupancy demands and outage reflect chosen count. Building solids/land prices remain fixed. No claim that package procurement has a separate cost if the current model lacks one. |
| Nine position offers | For every offer, choose required−1 (where positive) and required, using room geometry large enough for the selected slots. Allocation echoes offer; capacity predicate changes. Fixed rooms/parcel and all geometry-only prices remain unchanged. |
| Wing or hall envelope shortfall / sufficient | Vary selected L/W/H across one represented requirement while keeping solids constructible. Output equals offer, fit predicate changes, commodity quantities and civil/ventilation price reflect offer. Include a pair that cannot pass by changing a clearance multiplier. |
| Fixed rooms, changed demand | Increase upstream reactor envelope or cooling hardware envelope/count through its actual public inputs while holding facility selectors fixed. Requirements/margins change; all selected room dimensions, civil commodities, served volume and land remain fixed. Other subsystem cost changes are allowed and isolated from facility accounts. |
| Fixed positions, changed calendar | Change hold time or process duration to increase occupancy demand. Offered positions and geometry/cost stay fixed; capacity/readiness/outage may fail. |
| Offered slots do not fit | Increase one selected allocation beyond its fixed strip/wing capacity. Operational capacity may improve while geometric fit fails; no room expansion. |
| Parcel shortfall / sufficient | Hold every building and occupied coordinate fixed. Shrink/expand one selected parcel edge across occupied+access bounds. Parcel predicate changes and land/preconstruction changes by selected area; civil and ventilation remain fixed. |
| Independent four-wing choices | Alter only one wing's selected dimension. That wing's civil outputs/served volume change; the other three selected dimensions and solids stay fixed. Recompute actual campus bounds and collisions without overwriting parcel. |
| Provisional/occupancy fit | Increase equipment envelope or occupants with fixed room dimensions. Required dimensions/area increase and relevant predicate fails while room solids and price remain fixed. Provisional qualification remains unchanged. |
| Unsupported/invalid | Four-wing/module/live-calendar guard, nonfinite selector, impossible partition, noninteger package count and invalid aperture remain explicitly unsupported/invalid. A moderate constructible undersized room must return failed fit rather than fall into this category. |
| Dormant and legacy account | Disabled layout retains documented neutral diagnostic behavior; enabled layout with legacy cost mode still evaluates supplied fit. Cost mode cannot bypass geometry validation or represent qualification. |
| Proposal replay independence | One-shot entering proposal produces a complete ordinary input bundle. Remove proposal helper from the execution path and evaluate that bundle unchanged; identical selectors, outputs and costs prove policy separation. |

Run affected facility and oracle tests, generated-interface/unit checks, native integration promotion/read-set checks and applicable financial/cooling regressions. Require an independent reviewer to inspect actual bindings and retained failures, including source/manual/oracle agreement that requirements never overwrite selections. Completion requires native evidence for material, storage, geometry and parcel checks and their actual downstream costs, not merely successful field generation.

## Limits and review risks

The existing simple package-count/usable-volume relation does not qualify blanket segmentation, lifting loads, shielding or contamination handling. Room and parcel comparisons establish only the explicitly represented geometric fit. Existing unresolved qualification flags remain unresolved. The retained layout constants and topology must be visible as choices in the contract; this repair does not claim arbitrary facility architecture support.

The principal implementation risk is hidden geometry selection inside internal partitions, controlled-air calculation and placement. Review must follow those quantities all the way to civil takeoff, not stop at newly independent outer dimensions. The plan therefore supplies annex partition dimensions explicitly and computes wing lanes from selected room widths. Another risk is classifying every bad fit as malformed civil geometry; native acceptance deliberately separates constructible insufficient rooms from invalid solids.
