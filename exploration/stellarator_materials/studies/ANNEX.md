# Stellarator material variants study annex

This package evaluates supplied Stellaris-plant designs for two conductor materials, REBCO tape at 20 K and Nb₃Sn strand cable at 4.5 K, beside an untouched reference instance of the Stellaris plant, and reports LCOE, statuses and their decomposition per design. Model authority is the reviewed design `work/active/WI-100_stellarator-material-variants/design.md` (with its § 8 review changes and § 9 coordinator amendments A1–A8) and its `implementation-notes.md`, under the released plant contract `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md` (r5). The contract's stated limits (§ 10) remain part of that authority.

## Package and execution

Three units, three generated packages, one staged source set (`exploration/stellarator_materials/build.py`; design K21 fallback, probe P2: codegen refuses two `'MFE Power Plant'` instances in one package):

| Unit | Package | Entry-key prefix | Entry keys | Channels | Constraints |
|---|---|---|---|---|---|
| reference | `units/reference/stellarator_materials_reference_tea` | `stellarator_09__stellaris__` | 707 | 1,353 | 67 |
| rebco | `units/rebco/stellarator_materials_rebco_tea` | `stellarator_09_materials__rebco_material__` | 764 | 1,429 | 73 |
| nb3sn | `units/nb3sn/stellarator_materials_nb3sn_tea` | `stellarator_09_materials__nb3sn_material__` | 764 | 1,429 | 73 |

A case names one unit and evaluates one plant. The three-unit split is a route fact, not glue: nothing is harness-supplied because of it, and the unselected material instance does not run, so design D4's fill-and-witness has nothing to witness.

`studies/study_route.py` uses the stock strict `ProvisionalPackageLoader`, `PreparedEvaluator`, `StudyRunner`, `PreparedListStrategy`, `StudyStore` and `StudyQuery` (`run_points`). A proposal is a partial entry map; the runner completes it from the package defaults, which equal the interface baseline point of each unit (except the Nb₃Sn strain, which the route requires in every Nb₃Sn proposal, K6). The route refuses keys outside the unit, reference keys off their pin, the two final keys (K11) and an Nb₃Sn proposal without `magnet__conductor__eps_intrinsic_in`. It performs no physical calculation.

**Never evaluate the Nb₃Sn unit on its generated defaults.** The default design refuses (`EvaluationFailed: module_execution: ValueError: nonpositive IHX terminal approach`, design K22), and `eps_intrinsic_in` defaults to the neutral 0.0 because a negative design literal is not an entry point. Every study goes through a declared case or the record manifest's point.

**Case-to-proposal mapping.** Every Nb₃Sn case in `studies/cases.json` also carries `magnet__eps_min = −0.01`, a package constant (the channel `magnet__eps_min__eps_min`, not an entry key). A study drops it after checking the value equals the package constant; the oracle holds the same value. No other case key falls outside its unit's entry map.

**Stock manifests.** `studies/{reference,rebco}/manifest.json` name the oracle module `exploration.stellarator_materials.studies.oracle_entry`, which was never written (implementation notes deviation 6), and no Nb₃Sn manifest exists (deviation 4). A study writes its own per-unit manifests and binds the oracle in its record (see Oracle).

## Baseline pin

- **reference:** the WI-080 pin's 704 inputs plus the three declared new keys at neutral values (`rebco_law_enabled` 1, `arm_slope` 0, `arm_x_ref` 0). Headline `stellarator_09__stellaris__lcoe_calc__lcoe` = 318.7377471541504; violated `divertor_heat_ok`, `facility_occupancy_ok`, `reference_conductor_current_ok`, `tbr_ok`, `water_electric_capacity_ok`, `wp_fit_ok`, as pinned.
- **rebco:** the basis-bridge default (the Stellaris design on the REBCO-material instance, count `1.5 × parallel_tapes_set` = 170.609, A6). Headline 412.4334208430638; violated additionally `acceptance_ok` (expected at the bridge) and `pack_area_ok` (K15 boundary; 0.35 mm² per turn, the 0.991 factor).
- **nb3sn:** no generated default evaluates. The record manifest pins the offer policy's first evaluable Nb₃Sn design, the case the case-file header names as the K22 candidate: `anchored-1-nb3sn-12T-R12.7-a1.3-reference-none` (anchored × f_ren 1.0, 12 T target, R 12.7 m, 147 turns, power-short at 18 keV). Headline pinned from the oracle: −196.89511818207208 (negative because net power is negative); violated `divertor_heat_ok`, `net_positive`, `recirc_ok`, `tbr_ok`.

## Declared ties

None. Every attribute emits exactly one entry key per unit, so each axis group is a plain fan-out list. The case generator coordinates attributes (a design's turns, pack, allocation and re-supplied plant offer); these are policy choices recorded in every case, not physical identities between keys.

## Oracle

`exploration/stellarator_materials/oracle_glue.py` is the independent oracle (T-015 separate author, from the design and contract r4; `oracle-notes.md`, `oracle-reuse.json`). `evaluate_material_case(inputs, material)` composes the plant oracle's function-level pieces with re-derived inline equations, Round 1's oracle (`exploration/magnet_materials/oracle.py`) for the conductor, area, inventory, cold-stage and refrigeration channels, and the glue calcs; `evaluate_reference_case` delegates to the plant oracle unchanged. It differs by method where the implementer had a choice, notably the Nb₃Sn current-sharing temperature: Brent–Dekker to 1e−13 K in the oracle (`exploration/magnet_materials/oracle.py:45`) against bisection to 1e−10 K in the package's Round 1 body (`units/nb3sn/.../handwritten/magnet_conductor_alternatives/nb3sn_cable_critical_surface_impl.py:23`).

A study record binds it through its own `oracle_entry.py` (names only): unit from the key prefix; the five non-negative NIST coefficient keys `cryoplant__nist_k_{b,c,e,f,h}` and the zero `magnet__inventory__manufacturing_per_m_in` are dropped after checking they equal the constants the oracle holds (G1, N4); operand bindings keyed by each package's constraint ids. Two constraints: import the binding only by its dotted name, never as a bare `oracle_entry` (the oracle imports the plant seam `exploration/stellarator_e2e/studies/oracle_entry.py` under that top-level name), and give `scripts/study/verify.py` one module per unit, because it reads a module's `operand_bindings()` as the whole table for the package it verifies.

Constant channels, excluded from comparison: `cryoplant__nist_k_{a,d,g,i}__nist_k_*` on both material units and `magnet__eps_min__eps_min` on Nb₃Sn (negative design literals). Two published material channels have no oracle leg: `cryoplant__static_loads__nuclear_density_eff` and `cryoplant__static_loads__q_structure_nuclear` (the A2 structure-nuclear term, added after the oracle was written; `q_nuc_structure` is held at 0 in every declared case).

Tolerance: contract r5 § 9, every recorded channel of every case at relative 1e−9. The oracle author's own tests add an absolute floor of 1e−12 for channels that are zero to rounding (`tests/models/test_stellarator_materials_oracle.py:155-158`; the matched-cycle and cooling-water closure residuals, of order 1e−13). The Nb₃Sn Tcs-derived margins are an open question for this clause: see the record of study `20260930-magnet-material-plant-map`.

## Candidate range and validity masks

The candidate set is the declared case list `studies/cases.json` (2,921 cases, sha256 `f07133acdd561610287ff9dea01f641bf48b1562ec417254c85484ea8645e583`; gitignored, regenerates with `declare_cases.py --cache-dir`), written by `declare_cases.py` from `offer_policy.py` under contract r5 § 5: nine cells ({anchored, HELIAS-class, pack-size arm} × f_ren {1.0, 1.4, 1.8}); seven sizes; Nb₃Sn 10–13 T and REBCO 10–12 T (equal duty) and 18–24.9 T targets; driven companions of ignited designs; MR-7 insufficient and generous element offers on the reference cell; design variants (strain −0.6 %, common-P, `k_link` 0.95, 86 kA) and re-evaluation variants (prices 30 and 10, CPI 2021→2026, Nb₃Sn price 5.4 and 13.5, structure mass ×0.5 and ×2, purchase exponent 0.5 and 1.0). Every case is executed and retained whatever its status.

No validity mask is applied. The window is engineered: it is the contract's declared design grid and variants, not a sourced operating envelope, and no continuous boundary or optimum is claimed from it.

## Era pin

None. The packages run on stock TEAx at the checkout's revision (`8d877460ac4f6f264561d916e40c1708adb13397` on 2026-09-30).

## Accounting and claim limits

Conductor purchase is Round 1's basis (supplied element count × turns × coils × turn length × USD2021/m); refrigeration is Round 1's staged chain with Green capital; structure, heating, packages and power classes are re-supplied per design by the declared policy with the [U] scalings of contract § 5; everything else is the plant's. Money years are mixed (contract § 6 F12, K14), with the CPI variant as the stated check. `tbr_ok` and `divertor_heat_ok` are open plant gaps carried with their margins on every design; `peak_field_ok` is the supplied `B_max` envelope flag. A supported design is a screening pass, not a qualified reactor (contract § 10).
