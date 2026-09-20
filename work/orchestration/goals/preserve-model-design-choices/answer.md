# Preserve model design choices — technical answer

[AGENT] **Technical completion criteria are met for the independently reviewed scope.** No confirmed MR-7 violation remains open in that scope. Fresh non-author [final review](evidence/final-review.md) is PASS. Formal goal closure remains owner-held; the goal stays grounded.

## Preserved choices

| Area | Before | Current supported evaluation |
|---|---|---|
| Magnets | Current and adequacy policies selected pack geometry, inventory and structural masses. | Supplied pack side, installed turns, support mass and casing mass survive evaluation. Operating turn current determines excitation; selected geometry and inventory determine represented material, thermal loads and cost. |
| Facilities | Demand could select room dimensions, storage positions, parcel and package segmentation. | Supplied dimensions, positions, packages per sector, partitions and parcel survive evaluation. Requirements and signed fit/capacity margins remain separate. Signed parcel offsets preserve translation within the declared coordinate frame. |
| Processor | Exhaust demand times a margin set installed throughput and price. | Supplied per-module throughput determines price. Running exhaust determines capacity margin; price-source applicability is separate. |
| Cooling | Running duty set procurement price points and purchased coolant stock. | Selected machine price points and purchased stocks remain fixed as demand changes. Offered loop flow ceiling is separate from hydraulic calibration; represented fill is checked against supplied stock. |

These are explicit, reviewed calculation directions. Optional magnet selection helpers remain separate from the mandatory plant evaluator. Residual geometry identities, scenario policies and demand-based cost proxies have specific reviewed meanings in [WI-074 residual dispositions](../../../active/WI-074_design-choice-inventory-and-evaluation-contract/residual-dispositions.md).

## Interface and migration

The current package has 597 public inputs, 1,149 numeric outputs, 35 structured outputs and 34 predicates. The inventory reconciles 609 entering/current rows: 499 retained, 98 introduced and 12 retired, with zero unconsumed current inputs. [Interface migration](../../../active/WI-074_design-choice-inventory-and-evaluation-contract/interface-migration.md) records the changed controls. Current study axes are `exploration/stellarator_e2e/studies/axes.supplied_design.json`; the old axis declaration and frozen packages remain unchanged. Retired automatic-selection controls are explicitly refused by the current route.

## Evidence

- All ten native integration gates pass and return CANDIDATE. The first attempt correctly rejected an obsolete axis request; the corrected request uses the same source/package checkpoint. [Retained integration evidence](../../../active/WI-075_supplied-magnet-design-evaluation/integration/seam-retention.json) maps native scratch paths to independently hashed durable copies.
- The broad model sweep returned 2,440 passed, five failed, 13 skipped and one existing expected failure. All five stale-test failures were corrected; complete affected-file reruns passed 42 and nine tests. Independent review accepts this composite evidence with zero unresolved failures. The original full sweep was not green. [Exact accounting](../../../active/WI-075_supplied-magnet-design-evaluation/integration/regression-accounting.json) preserves the node mapping.
- Separate native/independent checks compare all 1,149 numeric channels and 34 predicates across six scenarios. Supplied insufficient/sufficient designs, fixed hardware under changed demand, unsupported conductor conditions and strictly negative near-zero margins are exercised. Counts from overlapping suites are not added.
- The seam's single baseline has no checked verdict mismatches or unverified listed predicates; worst checked relative deviation is `2.409591420195442e-15`. It is not the six-scenario coverage suite.

## Limits

The model does not qualify arbitrary pump/compressor off-design performance, full coolant inventory, arbitrary exchanger/pipe performance, supplied support strength, arbitrary facility topology, offered active fuel stock or actual vacuum equipment. Generic direct-heating consistency remains outside the active stellarator contract. Demand-based and hybrid cost estimates retain explicit disclosure; they do not certify independently supplied equipment capacity.

Conductor validity remains 20–32 T, with explicit extrapolation permission required above 24 T and existing temperature/source conditions retained. Physical inadequacy, unsupported performance conditions and conditional prices remain distinct. Baseline facility occupancy, divertor heat, breeding, conductor current and winding fit screens fail; whole-plant feasibility and lower cost were not acceptance conditions. No tolerance snapped the small negative occupancy margin to zero.

Existing integration tooling does not execute `assert_read_set_covered`; the ten-gate result does not prove read-set completeness. The verification summary does not locally record TEAx revision, while the enclosing seam checks revision `8d877460ac4f6f264561d916e40c1708adb13397`.

## Exact identity and disposition

- Pre-reveal code baseline: `86712a0d080d745802c1bcc57a30d3eca00458c3`.
- Entering enforcement checkpoint: `0223c73785713400633b857183e6a7f5f103aa95`.
- Implemented and integrated source checkpoint: `b11567eb693a4fd6f45a487f75dc5244fb433774`.
- Candidate pin: `84b82ef338093eb6d6f142360b3ded2b575b6f79397e6a719a6cb6dcf0154bc6`.
- Semantic fingerprint: `5a76ffbe2c1457b8abd5e8e9203331959baf68af65d7e12f9f49bb09d0bf071c`.
- Executable fingerprint: `04d3af1627885ce7a68d726b1d36026777eccc5d4976b15d693b6c8ec438f227`.

The delivery-record commit is the commit introducing this answer; it includes the two tested regression corrections and retained integration evidence, without changing the integrated model/package bytes. Concurrent unrelated write-up commit `35c0fd15` is preserved. No reference comparison, reference-based tuning, replacement freeze, push or merge was performed. This is post-reveal repair from pre-reveal code, not a restored blind test.
