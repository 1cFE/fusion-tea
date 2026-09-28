# Pre-reveal feasible neighborhood — native study record

## 1. Study header

Study id: 20260917-pre-reveal-feasible-neighborhood. Package: stellarator_tea. Date: 2026-09-17. Executor: /root. Mode: execute. Single arm: arm-native; controls and scenario families share the unchanged executable.

## 2. Intake

[OWNER-VERBATIM] “Can the current Stellaris-based model produce a verified neighborhood of designs that passes its implemented engineering screens under defensible assumptions, or can we explain which limits prevent that within a clearly declared search?”

[AGENT, adopted for this run] The owner authorized the campaign scope, caps and reserved gates preserved in preparation/goal-at-authority.md. Execution choices and scientific conclusions remain agent-originated. protocol.md declares axes/bounds/held assumptions before evaluation. No expectation about ARIES is evidence.

## 3. Objective and result

[AGENT] The reported objective channel is stellarator_09__stellaris__lcoe_calc__lcoe. Anchor conditional LCOE is $150.42954/MWh; comparison-form LCOE is separately retained. Selection maximizes engineering margin, not cost. 103 of 334 selected native cases pass all predicates with a valid power account. Results are in report.md and results/analysis.json; incomplete installed costs prevent an economic optimum claim.

## 4. Constraint outcomes

| constraint_id | source_local_identity | Status counts | Note |
|---|---|---|---|
|`stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0`|`wp_stress_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60`|`cond_strain_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b`|`recirc_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3`|`cycle_domain_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__beta_ok__82b78aad420730d5`|`beta_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7`|`heating_couple_positive_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7`|`divertor_heat_ok`|{'violated': 95, 'satisfied': 239}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f`|`heating_source_upper_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__net_positive__484521d56c02667a`|`net_positive`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58`|`burn_hold_ok`|{'satisfied': 331, 'violated': 3}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb`|`wall_load_ok`|{'satisfied': 331, 'violated': 3}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__tbr_ok__2cd198f674d413e4`|`tbr_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650`|`heating_couple_upper_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5`|`peak_field_ok`|{'satisfied': 199, 'violated': 135}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0`|`reference_conductor_current_ok`|{'violated': 3, 'satisfied': 331}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__sustainment_ok__77add152ed8eafce`|`sustainment_ok`|{'satisfied': 285, 'violated': 49}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852`|`loop_capacity_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339`|`wp_fit_ok`|{'violated': 3, 'satisfied': 331}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5`|`heating_source_positive_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|
|`stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945`|`loop_pressure_ok`|{'satisfied': 334}|Raw native verdicts; no tolerance changes|

## 5. Framing

[AGENT] At intake, the eight continuous/integer design axes were search-framed and inventory was a discrete sensitivity for attribution. Judged framing remains the same: native verdict structure exists on the joint domain, while held inventory scenarios preserve raw boundary behavior. Conservative reachability is not proof of independent response. No source-qualified continuous feasibility region or economic optimum is inferred.

The native feasible fraction is 0.3083832335329341. This is the policy H1 numeric metric for the selected native set; it is selection-biased. The original space-filling screen found only five passes among 512 candidates, with refusals retained, and cannot support a large feasible-volume claim. H2: omissions and qualification gaps remain declared seams, with no new inequality or repair authorized. H3: no new solve or cross-module cycle was introduced.

## 6. Per-axis account

#### plasma__R — feasible structure (search framing)

**Applies:** yes.

The exact individual/combined neighborhood results and signed margins are retained in results/neighborhood-summary.json; joint failures and fixed-slice boundaries are in results/analysis.json and map-data.csv. This finite search does not establish a global boundary.

#### plasma__R — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

The search-framed account above applies.

#### plasma__a — feasible structure (search framing)

**Applies:** yes.

The exact individual/combined neighborhood results and signed margins are retained in results/neighborhood-summary.json; joint failures and fixed-slice boundaries are in results/analysis.json and map-data.csv. This finite search does not establish a global boundary.

#### plasma__a — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

The search-framed account above applies.

#### magnet__coil__I_coil — feasible structure (search framing)

**Applies:** yes.

The exact individual/combined neighborhood results and signed margins are retained in results/neighborhood-summary.json; joint failures and fixed-slice boundaries are in results/analysis.json and map-data.csv. This finite search does not establish a global boundary.

#### magnet__coil__I_coil — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

The search-framed account above applies.

#### plasma__n_e0 — feasible structure (search framing)

**Applies:** yes.

The exact individual/combined neighborhood results and signed margins are retained in results/neighborhood-summary.json; joint failures and fixed-slice boundaries are in results/analysis.json and map-data.csv. This finite search does not establish a global boundary.

#### plasma__n_e0 — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

The search-framed account above applies.

#### plasma__T_i0 — feasible structure (search framing)

**Applies:** yes.

The exact individual/combined neighborhood results and signed margins are retained in results/neighborhood-summary.json; joint failures and fixed-slice boundaries are in results/analysis.json and map-data.csv. This finite search does not establish a global boundary.

#### plasma__T_i0 — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

The search-framed account above applies.

#### magnet__coil__coil_t — feasible structure (search framing)

**Applies:** yes.

The exact individual/combined neighborhood results and signed margins are retained in results/neighborhood-summary.json; joint failures and fixed-slice boundaries are in results/analysis.json and map-data.csv. This finite search does not establish a global boundary.

#### magnet__coil__coil_t — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

The search-framed account above applies.

#### magnet__casing__interior_y — feasible structure (search framing)

**Applies:** yes.

The exact individual/combined neighborhood results and signed margins are retained in results/neighborhood-summary.json; joint failures and fixed-slice boundaries are in results/analysis.json and map-data.csv. This finite search does not establish a global boundary.

#### magnet__casing__interior_y — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

The search-framed account above applies.

#### heat_transport__n_loops — feasible structure (search framing)

**Applies:** yes.

The exact individual/combined neighborhood results and signed margins are retained in results/neighborhood-summary.json; joint failures and fixed-slice boundaries are in results/analysis.json and map-data.csv. This finite search does not establish a global boundary.

#### heat_transport__n_loops — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

The search-framed account above applies.

#### magnet__winding_pack__inventory_multiplier — feasible structure (search framing)

**Applies:** not applicable — discrete sensitivity scenario.

No continuous inventory boundary is claimed.

#### magnet__winding_pack__inventory_multiplier — observed response (sensitivity framing)

**Applies:** yes.

Matched inventory 1.0/1.01 controls preserve cost/dimension/current consequences and near-zero numerical exceptions. No tolerance or material law is changed.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
|plasma__R|`stellarator_09__stellaris__plasma__R`|fan_out|Complete public design-attribute entry; downstream bindings retained|
|plasma__a|`stellarator_09__stellaris__plasma__a`|fan_out|Complete public design-attribute entry; downstream bindings retained|
|magnet__coil__I_coil|`stellarator_09__stellaris__magnet__coil__I_coil`|fan_out|Complete public design-attribute entry; downstream bindings retained|
|plasma__n_e0|`stellarator_09__stellaris__plasma__n_e0`|fan_out|Complete public design-attribute entry; downstream bindings retained|
|plasma__T_i0|`stellarator_09__stellaris__plasma__T_i0`|fan_out|Complete public design-attribute entry; downstream bindings retained|
|magnet__coil__coil_t|`stellarator_09__stellaris__magnet__coil__coil_t`|fan_out|Complete public design-attribute entry; downstream bindings retained|
|magnet__casing__interior_y|`stellarator_09__stellaris__magnet__casing__interior_y`|fan_out|Complete public design-attribute entry; downstream bindings retained|
|heat_transport__n_loops|`stellarator_09__stellaris__heat_transport__n_loops`|fan_out|Complete public design-attribute entry; downstream bindings retained|
|magnet__winding_pack__inventory_multiplier|`stellarator_09__stellaris__magnet__winding_pack__inventory_multiplier`|fan_out|Complete public design-attribute entry; downstream bindings retained|

preparation/axis-contract-check.json checks the original contract and pipeline. No ties or computed axes.

## 8. Indicators and rulings

All nine groups report constraints_reachable; no no_constraint_response owner ruling is needed. Transverse accommodation reaches only fit and no objective, so its missing cost/structural resistance limits interpretation. Loops retain hydraulic/power resistance but incomplete installed cost. Peak density/temperature remain authored inputs with internal ash/confinement closure.

Not derivable: monotonicity or sign, same-quantity identity across different key names, or intra-module operand dependency. Reachability is only a possible path. Native data, not these indicators, establish the observed responses.

## 9. Preflight results

Fresh exact manifest baseline and all preflight gates pass; original receipts are results/package_identity.json, baseline_result.json and preflight_results.json. Package cleanliness is checked before and after candidate execution. Two prior standalone launch failures occurred before model evaluation and are retained in baseline.log/baseline-retry1.log; baseline-retry2.log records the successful documented import-path correction. All three runtime provenance tests passed. No environment was installed or synchronized. Integration regeneration is not rerun: preparation/continuity.json establishes unchanged audited sources/package/oracle/route/manifest from the pinned study; the copied integration return and its limitations are reused.

## 10. Execution route and why

Study-local direct API: stock StudyRunner plus PreparedListStrategy through the unchanged package-owned study_route.py. The exact baseline exercised this route before preflight and selection. Coordinated input blocks require this route. Glue ledger: none; no adapter or outer physics solver. execution/reproduce.sh documents the retained launcher/import prerequisites. Two importer failures consumed the mechanical retry cap without model calls.

## 11. Study definition and window provenance

The initial domain was engineered before screening, as declared in protocol.md. 512 seeded Latin-hypercube geometry/current/density/temperature coordinates at fixed accommodation and loops found five oracle passes; four controls provided attribution. The retained maximum-minimum variable-margin choice selected the local anchor. Finite refinement candidates and an R/current lattice were deposited before evaluation. The original bound set did not grow. Exact candidates, selection rule, seed and local map values are retained in preparation/. Domain refusals and invalid accounts are not discarded or counted as physical failures. No external solve or adaptive native runner was used.

## 12. Cross-fingerprint correlation and what it means

Single unchanged executable and semantic fingerprint. No cross-fingerprint correlation is needed. Exact r2 controls agree byte-for-byte in 242 scalar values and 20 verdicts; preparation/r2-control-provenance.json pins their original evidence. Source-conditioned Table5 geometry/field has no independent prediction credit.

## 13. Verification

All 75484 mapped scalar comparisons pass the retained relative/absolute 1e-9 comparison. 6 strict-relative near-zero differences remain visible; all are reviewed separately. Of 6680 independent oracle verdict comparisons, 3 exact-current-boundary sign exceptions remain raw. All 6680 native-operand reconstructions agree. The generic stratified verifier reports refused-known-exact-boundary; its unmodified receipt is retained and is not relabeled a strict pass. The all-point check scopes every disagreement in results/oracle-all-points.json. No tolerance, predicate or native classification is changed.

All 242 native numeric channels are retained, but 16 are outside the oracle map (identities in oracle-all-points.json). Native-operand reconstruction checks classifier arithmetic, not independent scientific equations. Oracle agreement checks implementation, not physical source validity. Existing static L2/L6, integration read-set and broad-consumer limitations remain inherited. Exact r2 reproduction is numerical attribution, not source ignition reproduction.

## 14. Review outcomes

Fresh independent reviewer /root/reviewer: pre-execution PASS in reviews/preexecution-check.md, followed by result assurance PASS in reviews/result-assurance.md. The same reviewer checked all original store joins, every retained scalar/predicate comparison, exact controls, bounds, neighborhood, matched mechanisms, plot data/PNG and archive/comparison preservation. Eight fresh verification-only oracle calls at existing coordinates reproduce retained channels exactly; the receipt and review program are frozen under reviews/. No native review evaluation or new screening coordinate occurred. There are no unresolved corrective findings. Final scoped-commit/snapshot/trail assurance remains a goal-layer review after publication; it reuses this scientific coverage.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260917-pre-reveal-feasible-neighborhood#1` | model | Sampled screen-passing neighborhood and fixed-slice tradeoff are retained with failed neighbors. | declared seam — bounded result; no certified continuum or buildability claim | `report.md` |
| `20260917-pre-reveal-feasible-neighborhood#2` | model | Multiplier1.0 retains signed near-zero current-boundary disagreements; reserve1.01 buys inventory and margin. | declared seam — preserve raw failures, dimensions and price; no tolerance relaxation | `results/oracle-all-points.json` |
| `20260917-pre-reveal-feasible-neighborhood#3` | model | Geometry, conductor, cooling, achieved breeding and omitted costs limit engineering/economic interpretation. | declared seam — requirements quantified; hardware qualification and installed prices remain open | `report.md` |
| `20260917-pre-reveal-feasible-neighborhood#4` | model | Oracle domain refusals and native invalid power accounts remain distinct from valid failed screens. | declared seam — retain all results and finite-domain scope | `results/oracle-scan.json` |
| `20260917-pre-reveal-feasible-neighborhood#5` | process | Two standalone import-path failures used the retry cap before any model evaluation. | declared seam — documented launcher paths; no runtime replacement | `execution/reproduce.sh` |

## 16. Snapshot

snapshot.json SHA256: faaae353f5d5f7cb91c39ae0d87d65714fffae2c34f93d2e4e846c07031a3c13. Schema version 1. All values were resolved at freeze; later readers need no live manifest for record content.

## 17. What this record does not contain

No full generated executable or licensed environment is embedded in this record; the unchanged r2 archive and retained runtime are reproduction prerequisites. No new source extraction, magnetic equilibrium, neutronics, conductor qualification, installed equipment quote or global-search proof is present. Every failed/invalid evaluated point and oracle refusal is retained. The baseline has its own native store; the selected candidate arm names the main store. Independent final review and executor synthesis are later append-only records.
