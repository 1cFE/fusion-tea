---
Status: proposed
Created: 2026-09-18
Updated: 2026-09-18
Related Artifacts: spec.md; evidence/layout_capacity_probe.py; evidence/layout_capacity_probe.json
---

# Layout and maintenance capacity design

## Decision and scope

[AGENT] Use a deliberately conservative cross-shaped maintenance arrangement: a central reactor hall and four straight radial wings, one per reactor sector. Each wing contains a ground-level sector service bay, a clean component preparation annex and a physically separated dirty processing/storage annex. A separate cooling hall uses the executed circuit count. This avoids inventing a loaded-sector turning maneuver or lifting a 7000-tonne assembly by overhead crane. It is a conceptual bounding layout, not a recovered source floor plan.

This design supplies numerical geometry, capacities and conflict checks for reactor and maintenance functions and cooling equipment. The other building functions remain named residual allowances unless defensible equipment envelopes are obtained. This hybrid does **not** establish that the entire building set meets R9.S3. That gap must be included in preimplementation review rather than inferred away from the hot-cell depth.

All proposed dimensions, task times and resource choices below are [AGENT] unless expressly identified as source-supported or computed from an existing producer. They are reviewable scenarios, not settled requirements. No cost rates are selected here.

## Original source checks

The original rendered Stellaris pages were inspected at `work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p28_maintenance.png` and `stellaris_p29_maintenance.png`. Fig.54 was inspected at `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/stellaris-high-field-quasi-isodynamic-stellarator.pdf-29-0.png`. Admissibility and extraction pointers are in goal `evidence/internal-sources.md`.

Source-supported facts are four symmetric splitting interfaces, extraction of a complete field-period sector by a single radial translation, ground transport on rails, and an estimated drained-sector mass around 7000 tonnes. Approximately 5 m by 3 m are **vessel-end openings**, through which smaller blanket segments are removed. The paper does not define those segments' complete envelopes or number. Source assumptions include thirty-day initial preparation/cooldown, thirty-day final recommissioning, and a provisional seven-month total outage estimate. The five-month intervention period is a target, not an achieved duration. The proposed 125 Pa containment depression does not determine airflow or shielding.

Fig.54 supports receipt, inspection/preassembly, system testing, clean reassembly/testing, sector transfer, in-vessel removal, cleaning/repair/disassembly, size reduction, separation, containerization, dirty storage, waste transfer and outgoing waste. Its unscaled proportions are not used for dimensions. Its explicit need for further dirty/clean separation design remains unresolved by the source.

## Geometry and physical arrangement

Let R be live major radius and r be the sum of live minor radius and radial layers through the low-temperature shield. At actual defaults R=12.7 m and r=3.55 m. Let e=2 m be an assumed exterior allowance per minor-radius direction for unmodeled cryostat, supports and penetrations. It is not a measured exterior envelope; study e=1/2/4 m without optimizing it. Let b=R+r+e.

A 90-degree sector oriented about its radial bisector fits within Ls=b, Ws=sqrt(2)*b, Hs=2*(r+e). The length is conservative: it includes the entire radial interval from the machine center to its exterior rather than subtracting the inner toroidal void. This box bounds the circular-torus approximation only. Four source sectors motivate the quarter-sector approximation; nonaxisymmetric exterior geometry and interface extraction remain unqualified. Current bounds are 18.25 m ×25.809 m ×11.1 m. The 7000-tonne source datum is a current-source load reference, not a live mass scaling law; changed-geometry handling-load qualification must report unknown.

Each sector wing points along its extraction bisector. Its sector lane width is Ws+2*(l_component+c), with assumed component pull length l_component=2 m and residual servicing clearance c=2 m. This reserves withdrawal zones on both sides of the sector box. The minimum bay length is Ls+2*(l_component+c). A 3 m overhead service allowance gives hall/sector height Hs+3; it does not imply whole-sector crane lifting. Source vessel openings are oriented at the sector ends, so the actual end-interface rail axes must fit these withdrawal zones before detailed design; the conservative rectangular allowance is a screen, not a clash proof.

Clean and dirty annexes each use four rows of package positions with two independent 6 m aisles. The transverse sequence is 4 m rack depth, 6 m aisle, 4 m rack, 4 m rack, 6 m aisle, 4 m rack: total 28 m. A package position has 6 m longitudinal pitch and 4 m depth, sufficient for an assumed 4 m ×2 m plan envelope plus 1 m edge allowances. Each rack row is aisle-accessible without moving another package. An additional 6 m end cross-aisle connects the rows. A 6 m aisle clears the package's 4.472 m plan diagonal plus an assumed 1.5 m handling allowance. This is a small-component maneuver allowance, not proof of a transporter turning radius.

For K positions, annex length is `6*ceil(K/4)+6` metres. Clean K equals one campaign's component count per wing plus two dedicated positions for preassembly/testing and the clean transfer airlock. Dirty K equals peak unprocessed queue plus peak packaged storage plus four dedicated positions for an integrated processing cell, dirty transfer airlock and two outgoing transfer positions. Counts are conservative separate maxima; no credit is taken for storage/queue sharing when their peaks differ.

Each wing is a full rectangle of length `max(minimum bay length, clean annex length, dirty annex length)` and width `sector lane width+56`. Both annexes and the central transfer/service lane occupy that full length; unused length in the shorter functional strip is reserved space and is charged if the eventual rate uses whole-building volume. Do not silently cost only occupied equipment patches.

Let Ww and Lw be wing width and length. The central hall half-side is `h=max(b+Ls+c, Ww/2+c)`. Reactor hall footprint is the square [-h,h]². East wing occupies [h,h+Lw] ×[-Ww/2,Ww/2]; other wings are its 90/180/270-degree rotations. These rectangles do not overlap, and adjacent wing ends have at least the declared clearance c from the corner boundary. The hall reserves radial translation of at least Ls+c beyond the initial exterior in all four directions. Loaded sectors travel straight from torus to wing and straight back; the empty transport equipment changes wings through the hall. A source-compatible ground transfer onto bay supports is assumed, with its structural design and load distribution unresolved.

Clean goods enter each annex from its exterior end, pass inspection/preassembly and testing, then reach the sector bay through the clean airlock. Removed components go only to the dirty-side airlock, integrated processing cell, storage and separate outgoing transfer positions. The source's two-end removal paths lie inside the sector service lane. During removal, both ends are dirty. Before installing clean components, a seven-day bay/vessel cleaning and setup stage closes the dirty transfer boundary and admits new components through the clean supply boundary. Thus the **same sector bay changes operating state**; no clean and dirty component movements share it simultaneously. The sector bay stays radiologically controlled and shielded throughout removal and remote reassembly. Clean supply means unused components, not removal of activation, dose clearance or human access. The transition still requires an unsourced contamination-control procedure. Permanent walls separate clean annexes from dirty operations; wall shielding/containment ratings remain cost/source questions.

Place the cooling hall beyond the east wing with an assumed 10 m separation strip and independently accessible exterior doors. This is a separation scenario, not a nuclear/fire-code prescription. Do not treat the rectangular developed area or its enclosing parcel as a complete licensed site boundary. All other retained facilities remain outside this explicit placement until their inventories are resolved.

## Component quantities and conservation

The blanket producer reports 1013.4060451 m³ at current defaults. Use 4 m width ×2 m height ×2 m length as an **assumed handling package**, which passes a 5 m ×3 m vessel opening with 0.5 m clearance per side. It is not a source module design. With material-volume occupancy f=0.5, each package represents at most 8 m³ of modeled blanket material. Equal sector batches require `Nb=ceil(Vblanket/(4*f*16))`: 32 blanket packages per sector, or 128 total. The represented capacity 1024 m³ exceeds the modeled 1013.406 m³; report the 10.594 m³ unused capacity rather than changing model material inventory.

Add four divertor packages per sector as a visibly separate segmentation assumption because no individual divertor geometry/quantity exists. These use the same conservative handling envelope but do not claim a material-volume derivation. Total campaign demand is therefore 36 packages per sector, 144 across the plant. Study f=0.25/0.5/0.75 and divertor packages=2/4/8 per sector. Changing count alone must not change blanket/divertor cost or material inventory.

After processing, retain one same-envelope storage package per incoming package. No volume-reduction credit is taken for cutting or material separation. This ignores additional secondary waste and packaging growth: expose a package-yield parameter ≥1 and flag its unsupported basis; no waste classification or disposal qualification is established. The source list of size reduction, separation and containerization remains an integrated cell's task sequence, not omitted functions.

## Resource-constrained maintenance schedule

The existing calendar remains the only authority for campaign dates and availability. The prototype invokes the **existing** `lifecycle_calendar_live` implementation on the current-default native replay's peak wall load and event cost. It checks the returned availability against the replay. Current events begin at years 4.523926, 9.631185, 14.738445, 19.845704 and 24.952964; availability remains 0.9027777777777779. The interval between campaigns is about 5.10726 years including outage. No independent schedule approximation is substituted into plant economics.

Each campaign uses four offered sector bays, two service teams and one ground transport resource. An assigned team occupies its sector continuously through removal, cleaning, installation and test; a waiting sector occupies its own bay. Each component removal and installation takes 0.5 day, cleaning/setup seven days and final testing seven days. Source-supported thirty-day preparation and thirty-day recommissioning bound the intervention. Splitting/preparation beyond cooldown takes an additional assumed seven days; final joining takes seven days. Each outbound or return sector transport reserves two days. Task times are calendar-day scenarios, not derived crew shift productivity.

Dispatch the four outbound sectors after splitting in sector order. Assign service to the earliest available of the two teams. Dispatch returns in service-completion order using the same transport resource. Rejoin only after every sector returns, then recommission. This policy is deterministic and conservative; it is not a schedule optimizer.

| Sector | Outbound completion | Service interval | Return completion |
|---|---:|---|---:|
| 1 | Day39 | 39–89 | Day91 |
| 2 | Day41 | 41–91 | Day93 |
| 3 | Day43 | 89–139 | Day141 |
| 4 | Day45 | 91–141 | Day143 |

Joining finishes day150 and recommissioning day180. The offered seven-month window is 213.0625 days using 365.25 days/year. Therefore this particular scenario has 33.0625 days margin. It does not validate the assumed times or release a new availability value. A bay-count input less than four fails this layout policy; do not silently queue an unprovided sector on the transport route.

A dirty integrated processing station in each wing serially performs disassembly/cleaning, cutting, separation and containerization at an assumed one day per incoming package in total. Each of those four stages receives a quarter-day allocation for inspectability; this is not literature-derived task evidence. Arrival times follow the corresponding sector's actual removal sequence at 0.5-day intervals. Jobs start at max(arrival, previous completion). The resource remains occupied until completion. Unprocessed inventory consists of arrived jobs not yet started; packaged storage runs from completion until a declared hold time expires. Sweep interval endpoints with departures processed before arrivals at identical times.

For a one-year hold, the current baseline peak is 18 unprocessed packages and 36 stored packages per wing, or 144 stored packages across the plant. Processing continues after sector reassembly without consuming a reactor service team; that independent crew/resource is counted explicitly. All four wings therefore need one processing resource each in addition to the two sector service teams.

Clean receipt occurs ninety days before each campaign, with one complete campaign supplied then. One inspection/preassembly/testing station per wing processes one package/day; all 36 are ready by day-54. The peak total incoming/prepared clean inventory is 36 per wing, not twice 36 as packages change status. Incoming stock for one campaign can overlap retained clean stock only if actual dates or increased processing time demand it; the implementation must count event intervals rather than infer one campaign forever.

Storage at the end of the thirty-year plant horizon remains occupied until its hold interval ends. Do not truncate retained waste to zero at plant shutdown. Handling its demolition/disposal cost belongs to the explicit decommissioning boundary, not this capacity calculation.

## Numerical capacity and geometry contrasts

The kept prototype and JSON provide a numerical design probe, not production integration or independent validation. Run with `.codex-test/run python work/active/WI-068_layout-based-facilities/evidence/layout_capacity_probe.py`.

| Scenario | Outage days required | Seven-month compatibility | Storage peak per wing | Unprocessed peak per wing |
|---|---:|---|---:|---:|
| Baseline two teams, 0.5 day/removal and installation, one-year hold | 180 | Pass under assumptions |36|18|
| One service team |278|Fail|36|18|
| 0.75 day/removal and installation |216|Fail|36|9|
| Double blanket material demand, same package definition |244|Fail|68|34|
| Six-year storage hold |180|Outage passes; original storage capacity fails|72|18|
| 0.25 day/removal and installation |144|Outage passes; original dirty buffer capacity fails|36|27|

The double-material probe is a demand stress case, not a supported alternate reactor geometry. The faster schedule illustrates why a throughput improvement can require more buffer space. These are fixed-offered-capacity contrasts: retain baseline 18 buffer and 36 storage positions for verdicts. Separately report how many extra positions and how much area a resized facility would require; never use automatic resizing to conceal a failed offered layout.

At current defaults the baseline layout computes reactor hall 93.809 m square (8800.203 m²), four wings each 96 m long ×89.809 m wide, and 14.1 m clear sector/hall height. Each clean or dirty annex occupies 2688 m² per wing; the sector service/transfer strip occupies 3245.702 m². The large dimensions follow the no-stacking, aisle-accessible, four-radial-wing policy and the allowance for an entire quarter-sector assembly. They are not source measurements or calibrated estimates. Reviewing a more compact arrangement is legitimate if it preserves demonstrated paths, resources and inventories.

## Cooling equipment and servicing

Read circuit count and existing exchanger dimensions from their cooling producer: shell bore3.2 m, wall0.2 m, shell length13 m and tube length11.6 m. The cylindrical OD is computed3.6 m. Add a provisional2 m axial head/nozzle allowance at each end, a separate11.6 m tube-pull zone and2 m clearances at each axial end. Add a12 m machine-service strip per circuit. Two provisional helium packages of6 m ×3 m ×4 m and two provisional salt pump/motor packages of3 m ×2 m ×3 m occupy that strip in separate rows. A9 m circuit-cell width clears the paired helium widths plus3 m total side/intermachine spacing; the salt row is narrower. No source or sizing calculation currently supports these package dimensions.

Thus each circuit cell is44.6 m ×9 m. Place two banks facing a5 m central service aisle; each bank contains ceil(n/2) cells. Odd circuit counts leave one vacant cell, explicitly charged. The hall is94.2 m by `9*ceil(n/2)` m with9 m provisional height. Fourteen circuits gives5934.6 m²; eighteen gives7630.2 m². Each exchanger pulls axially into its own reserved zone, without blocking the central aisle. The machine rows and exchanger pull zone are disjoint portions of a cell. Clearance/domain checks must be recalculated if any envelope changes.

Additional cooling maintenance storage and service space is **not included in those circuit-cell areas**. Allocate a separately identified service annex from one machine-event receipt batch, one bundle-event batch and two initial spare machines. Machine dates remain ten and twenty years; bundle date remains fifteen years. At14 circuits there are28 helium and28 salt machines per machine event and14 bundles per bundle event. Provisionally use two machine stations at2 days/unit (56 days/event) and two bundle stations at5 days/bundle (35 days/event). One-year stored retirement batches are conservative capacity scenarios, not a radioactive classification. Preserve separate cooling dates and combine their storage intervals if machine/bundle lifetime sensitivities make them coincide.

Use individual envelope positions: helium6×3 m, salt3×2 m, bundle11.6×3.2 m before explicit packaging/aisle allowances; the spare count is one helium and one salt unit for the plant. Require an explicit configured cooling-annex storage/servicing layout before crediting complete cooling maintenance facilities. Contamination classification, transport mass, isolation, replacement outage duration and simultaneous online operability remain unresolved. These provisional machine service durations do not authorize adding or subtracting outages from the existing calendar. A `cooling_outage_basis_resolved` status remains false; a facility-space capacity pass cannot be reported as whole-plant maintenance feasibility.

## Remaining building set and costs

| Named existing function | Proposed dimensional treatment | Residual at this design stage |
|---|---|---|
| Reactor building | Computed bounding hall | Exterior envelope, heavy foundation and shielding qualification |
| Hot cell, module servicing and dirty storage | Computed radial wings and event-capacity annexes | Contamination-release basis, radiation/decay data, secondary waste yield |
| Assembly hall and maintenance building | Clean preparation/testing and ground sector service mapped explicitly into wings; eliminate replaced duplicate floor functions only after account review | Separate conventional shop/spares functions remain retained |
| Heat-exchanger building | Computed fixed-equipment cells driven by live circuit count | Cooling service annex still needs explicit configured geometry |
| Reactor auxiliaries and ventilation/HVAC | Identify as services serving the modeled reactor/dirty volumes | No supported flows, radiation basis or separate services quantities; preserve pricing only under reviewed scope |
| Site improvements and site services | Explicit developed cross and cooling footprint available | Road/utilities/security setbacks and whole-site parcel unavailable; retain existing residuals |
| Fuel storage/tritium buildings | Existing fuel inventory/flow interface | No supported process-equipment dimensions or segregation basis; residual allowance |
| Cryogenics | Existing thermal/cold-inventory interface | No cold-box/compressor/dewar envelopes; residual allowance |
| Turbine building, service water | Existing power/interface producers | Turbine/condenser/tank envelopes unavailable; residual allowance |
| Power supply, onsite AC/control/security/administration | Named functional residuals | Equipment rack populations, staff occupancy basis and electrical separation unavailable |

Costing must receive gross enclosed volume and floor area by reactor, sector-service, clean non-active and dirty/active function; external and internal wall areas; explicitly configured wall thickness/material if priced separately; door/airlock counts/envelopes; ground-transport bay loads; processing resource counts; and installed-services boundary. Rates that already include services, shielding or foundations must not be combined with a duplicate material or service allowance. No numerical wall thickness is proposed without a source/assumption decision. Keep cooling equipment installation, reactor shielding, routine staffing, replacement purchases and decommissioning provisions under their existing owners.

## Executable ownership and checks

Put reusable geometry, event-occupancy and scheduling definitions in library analyses. Give the physical facilities identifiable component occurrences with exposed dimensions/capacities and disjoint cost owners. Stellarator instance binds sector policy, envelopes, clearance, segmentation and task assumptions. Radial build owns computed radii/material volume. Cooling owns shell/tube dimensions, counts, masses and lifecycle inputs. Facilities read exposed producer attributes rather than reaching into calc internals.

Follow `.agentic-mbse/patterns/adr002-calculations.md`, `plant-idiom.md` section “Binding a modelled value into a calculation”, and `expose-pattern.md`: library calculations own arithmetic on producer outputs; local input names differ from owner attributes; cross-part bindings name the actual occurrence. Preserve acyclic dependencies: calendar→maintenance demand→facility capacity→facility costs→plant cost. Facility capacity must not write calendar inputs.

The event scheduler needs loops, ceil and occupancy sweeps beyond simple generated arithmetic. Use the established guarded handwritten-completion route, with normative equations and independent references, rather than pretending a direct formula covers resource contention. Prefer extending the existing calendar's diagnostic exposure or sharing its actual pure event function; do not fork its logic into a second independently maintained clock. Preserve default-disabled behavior for other inherited MFE instances.

Reject nonfinite/negative geometry or durations, noninteger counts, unsupported sectors other than four in this layout, invalid packing fractions, negative hold times, nonpositive throughput, packages exceeding openings, and zero required resources. Zero calendar events is valid and produces zero recurring-waste inventory, with initial equipment assembly needs retained. Return finite dimensions and false compatibility for insufficient offered bays/storage/teams/clearances; malformed arithmetic inputs raise. Explicitly flag unsourced exterior geometry, ground-load qualification, contamination control and cooling outage basis separately from calculated capacity verdicts.

Independent checks must cover rectangle separation, straight extraction stroke, actual end-opening/component envelopes, aisle access for every position, material-volume capacity, no resource overlap, queue/storage endpoint conventions, campaign overlap, zero-event cases, a deliberately inadequate bay/buffer configuration, actual default versus selected18 and calendar bit-preservation. The numerical probe checks schedule failures and storage growth but does not supply those independent geometric/contamination or integration checks.

## Decisions still requiring scientific review

The major scientific bets are the circular quarter-sector exterior allowance, assumed small-component segmentation, bay decontamination transition, task times and one-year waste hold. They are explicit and broad sensitivities exist; none is validated by the inherited cost or source availability target. The absence of qualified cooling replacement downtime and most balance-of-plant equipment envelopes prevents a whole-plant capacity claim. A fresh reviewer should decide whether conditional conceptual sizing with these disclosed inputs is sufficient for implementation toward the target, or whether any of those missing inputs must be researched or taken to the owner first. Cost-source selection and complete-building-set acceptance remain with the coordinator and independent reviewer.

## Complete-set alternative for coordinator review

[AGENT] The simplest path to a wholly dimensioned conceptual set is to replace each remaining opaque room-cost group with a visibly **provisional occupied-envelope input**, then calculate its building shell using the same transparent clearance rule. This adds no claim that subsystem engineering has produced those dimensions. Prefer this over treating missing geometry as a zero area or implying that power is a layout dimension. The preceding residual table describes the inventory state; this alternative is a proposed implementation scenario to be selected explicitly in the combined design.

For an equipment envelope L×W×H and clearance c=2 m, the room shell is `(L+2c)*(W+2c)*(H+3)`; use two distinct envelopes when a function needs independently accessible machines. Baseline candidate inputs below are deliberately round spatial scenarios selected only to make the interface executable. They are not industry norms, lower bounds, quotations or source-supported dimensions. For source uncertainty study each dimensional multiplier0.5/1/2, with no optimization or claim the range is a confidence interval. Interface users must replace them when upstream dimensions arrive. These provisional dimension sensitivities are separate from supported geometry studies.

| Facility function | Proposed provisional contained-equipment L×W×H, m | Quantity driver and boundary |
|---|---|---|
| Turbine/condenser/feedwater hall |60×20×15|One conversion train per current module; keep separate purchased conversion equipment owner. No unverified geometry scaling with MW.|
| Cryogenics |Cold box20×12×10 plus compressor train30×12×8|Two independently accessible zones per module; building only. Existing magnet/coolant inventories are not turned into package dimensions.|
| Fuel storage and processing |30×20×8|One contained train per module; compartment/airlock allowance remains explicit. Source tritium quantities do not qualify this envelope.|
| Reactor auxiliaries |30×20×10|One room per module for remaining vacuum/heating diagnostic packages; explicit aggregation assumption. If specific heating/vacuum envelopes are added, retire their share of this envelope to avoid duplicate space.|
| Power-supply equipment |20×10×8|One supply group per module; omit already represented cooling pump local drives.|
| Onsite AC/switchgear |16×8×6|One distribution group per module; distinct from reactor power supply.|
| Service water |20×15×8|One pump/treatment group per module; ultimate heat-rejection outdoor plant remains separately identified.|
| Conventional maintenance shop/spares |20×15×8|One clean non-active shop; does not repurchase sector/component processing space.|
| Site services |20×10×6|Utilities/grounds support workshop only; roads and service trenches counted outside enclosed volume.|
| Ultimate heat-rejection structures |100×60 m outdoor occupied plot,12 m equipment height|One provisional outdoor installation per module. Do not charge full enclosed-building volume for this plot. Equipment cost remains CAS25.|

For occupancy-based buildings use explicit headcount scenarios instead of invented machine packages. Administration:200 concurrent occupants ×12 m²/person ×1.3 circulation allowance=3120 m², 4 m height. Control:30 occupants ×15 m²/person ×1.3=585 m², 4 m height. Security:10 occupants ×12 m²/person ×1.3=156 m², 4 m height. These headcounts do not change existing O&M payroll or imply total workforce; their relationship to shift staffing remains unverified. Use single-floor aspect ratio2:1, `L=sqrt(2A), W=sqrt(A/2)`. These are configurable planning scenarios, not occupancy-code claims. Main assembly/hot-cell/maintenance functions remain driven by equipment and campaign capacity rather than these headcounts.

A complete provisional cooling service annex can also use deterministic accessible rows. Reserve separate clean and dirty stores for each equipment type, with the existing one initial spare of each machine type added to clean inventory. At14 circuits, clean capacities are29 helium packages,29 salt packages and14 tube bundles; dirty capacities are28,28,14. The clean capacities include one entire replacement receipt batch; dirty capacities retain one entire retirement batch. Separating the maxima deliberately avoids reliance on swapping dirty and clean floor locations. At overlapping cooling events, obtain those capacities from actual dated intervals and increase required positions; hold offered counts fixed for compatibility verdicts.

For each equipment type with envelope length L and depth W, use two single-depth rows separated by a6 m aisle; position pitch L+2 m and row depth W+2 m. A store with K positions has width `2*(W+2)+6` and length `ceil(K/2)*(L+2)+6`. Bundles retain their11.6×3.2 m envelope before these allowances. Put the three type stores side-by-side behind separate clean/dirty boundaries. Give two machine overhaul stations10×7 m each and two bundle stations15.6×7.2 m each, in two station rows separated by a6 m aisle: service rectangle31.6×20.4 m, added to the dirty side. Count receipt/dispatch airlocks separately as occupied positions if their dwell is nonzero. This is an explicit conservative area procedure; it is now executed in the probe and still requires independent checking before integration.

Conventional buildings may be placed as a separate campus row south of the south wing: long edges parallel to the row,10 m spacing between room shells, a separate12 m access strip, and independent entrances. Its starting y coordinate lies at least10 m beyond the south wing extent. The row contains the provisional support rooms and outdoor heat-rejection plot; neither overlaps the four radial paths. The complete parcel bounding rectangle must include that row, the cooling hall/annex and the maintenance cross. It is a conceptual developed-land scenario only; qualified radiation/fire/security separation remains unresolved and must be an explicit assumption rather than a claim of compliance.

This alternative trades unknown old room prices for unknown but inspectable equipment envelopes plus a common sourced civil-cost method. It can demonstrate executable accounting and functional coverage. Whether that degree of provisional geometry is sufficient for the unchanged S3 criterion remains a fresh review decision. The combined design should choose this complete provisional scenario or the disclosed residual hybrid explicitly; it should not blend their claims.


## Final prototype additions and construction handoff

The prototype now computes the complete provisional conventional-room register, a cooling service annex and explicit room-placement rectangles. The cooling annex is126 m ×113.2 m clear plan area (14263.2 m²). Its clean stores occupy46.4 m total width; its dirty stores occupy46.4 m plus the20.4 m overhaul-service strip. All strips are charged to the common126 m length, preserving empty reserve space. Two distinct clean/dirty containment zones retain the separate incoming and retired component inventories. This is intentionally conservative; no no-stacking space credit is taken for changing stored contamination class. A9 m clear height is provisional for the annex and does not imply lifting-load qualification.

Current clear-plan campus rectangles are recorded in `evidence/layout_capacity_probe.json`, together with an enclosing parcel of298857.755 m² including a12 m external access strip. This is a **zero-wall clear-space skeleton**, not final external building footprints or a land purchase recommendation. Its rectangle check verifies conventional/cooling rooms against one another; final physical-layout verification must also include the expanded cross, walls and transfer links below. The current task schedule and volume inputs are unaffected by later wall construction choices.

For a construction-ready conceptual costing geometry, use distinct hall and wing shells separated by a10 m clear controlled transfer link in each radial direction. The links are straight, ground-transport corridors with sector-lane clear width and sector-bay clear height; they have no internal staging credit. They add four floor/roof strips and eight side walls, plus connections through openings in the hall/wing end walls. All reactor-sector paths remain straight; the four links add transport distance within the declared two-day task rather than silently changing task duration. Report sensitivity or infeasibility if a subsequently justified transport-speed model cannot cover that distance.

Let t be the separately chosen wall thickness. The three-strip wing external width is `Wsector+Wclean+Wdirty+4t`: two exterior walls and two partition walls. External wing length is Lw+2t. Hall external side is its clear side+2t. Recompute the hall clear half-side as `max(b+Ls+c, external_wing_width/2+c)` before placement, so expansion cannot make adjacent wings collide. A wing near external face is ten metres beyond the hall external face; its clear interior begins another t beyond that. The link's10 m length is measured exterior-face to exterior-face and its exterior width is sector-lane clear width+2t. Recompute campus and cooling coordinates from the resulting outside faces, maintaining the stated10 m separation. Enclose those external footprints and their12 m access strip for any final site-area consequence.

Cost hall and wing exterior walls once each, subtracting their respective full link-opening areas. A transfer link has two side walls and no end caps. Partition wall area belongs only to the wing, once. Clean/dirty annex wall boundaries, doorway thickness and interior usable areas remain explicit; never cost full independent annex shells in addition to the shared wing shell. Floor slab and roof construction thickness are independent inputs; clear height excludes both. The worker implementing the final construction scenario must output net usable area, gross exterior area, floor/roof area, wall area and volume separately. The present prototype does not select t or qualify shielding; the coordinator's cost/construction design supplies it.

Processing station availability now persists across campaign boundaries in the prototype, and clean preparation uses a persistent per-wing resource with readiness and peak inventory checks. Empty occupancy intervals are discarded; equal-time releases precede arrivals. The current case's results are unchanged. Long processing campaigns therefore cannot reset station availability at the next event, although production must still add explicit task-level resource and storage counterexamples independently.
