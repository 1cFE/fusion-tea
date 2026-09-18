## 1. Study header

- **Study id:** 20260918-computed-tritium-breeding
- **Package:** stellarator_tea
- **Date executed:** 2026-09-18.
- **Executor:** delegated transport/study author under the goal coordinator.
- **Mode:** execute.
- **Arms:** arm-native.

## 2. Intake

[OWNER-VERBATIM]

> Run a focused study showing how supported blanket choices affect breeding and other affected plant quantities. Preserve failed cases and disclose extrapolation and uncertainty. Do not tune the model to recover previously passing designs.

[OWNER-VERBATIM]

> listen, you are in charge here. you have the goal -- use research to collect data as needed, and otherwise use your best judgement

[AGENT] Frame the work as a thickness sensitivity with three unsupported-domain diagnostics. Hold the current authored plant defaults and preserve unrelated failures. Use the independently reviewed transport response only inside its physical domain. No extra recovery/extraction axis is needed to show the existing conditional requirement.

## 3. Objective and result

- **LCOE objective channel:** `stellarator_09__stellaris__lcoe_calc__lcoe`.
- **LCOE result:** $134.126–156.000/MWh over the supported thickness sensitivity; $144.747/MWh at the 0.80 m reference point.

Greater supported blanket thickness increases computed breeding and represented capital cost. The sampled 0.825 m case clears the numerical breeding screen but newly fails peak field. Every case retains other failed plant screens, so this is no economic optimum or feasible design. [Report](report.md) and [complete points](results/points.csv) retain the results.

## 4. Constraint outcomes

All 20 executing predicates are retained, including unrelated failures. The complete pointwise map is in [native cases](results/native-cases.json).

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | violated | Violated all13; retained unchanged. |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | mixed | Violated at supported0.60–0.80 m and all3 undefined diagnostics; satisfied at sampled0.825–1.00 m. Undefined is not physical deficit. |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | mixed | Violated at sampled supported0.825–1.00 m and unsupported1.05 m; satisfied elsewhere. |
| `stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0` | `reference_conductor_current_ok` | violated | Violated all13; native and oracle agree. No reserve change made. |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339` | `wp_fit_ok` | violated | Violated all13; retained unchanged. |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | satisfied | Satisfied all13. |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | satisfied | Satisfied all13. |

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| blanket__blanket_t | sensitivity | Supported build response and native cost/adequacy consequences. |
| plasma__R | sensitivity | One unsupported-domain diagnostic. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| blanket__blanket_t | sensitivity | no | Observed breeding/cost/field tradeoff; no whole-plant feasible point or boundary search. |
| plasma__R | sensitivity | no | Changed radius makes breeding undefined; no physical radius response inferred. |

## 6. Per-axis account

#### blanket__blanket_t — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### blanket__blanket_t — observed response (sensitivity framing)

**Applies:** Yes. Mean breeding and cost rise across the supported samples. The numerical breeding screen fails at sampled0.60–0.80 m and passes at sampled0.825–1.00 m; peak field fails at the latter samples. Divertor heat, reference conductor current and winding-pack fit fail throughout. Both unsupported thicknesses have undefined breeding; the1.05 m diagnostic also fails peak field. No continuous boundary or optimum is claimed.

#### plasma__R — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### plasma__R — observed response (sensitivity framing)

**Applies:** Yes. At R=12.71 m and thickness0.80 m, breeding is undefined and the TBR predicate fails closed. Divertor heat, reference conductor current and winding-pack fit remain violated. Unrelated outputs remain available. This one diagnostic supports no physical breeding response or radius boundary claim.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| blanket__blanket_t | `stellarator_09__stellaris__blanket__blanket_t` | fan_out | Complete public authored thickness key. |
| plasma__R | `stellarator_09__stellaris__plasma__R` | fan_out | Complete public authored radius key. |

[Declaration](axes.json). No ties or retired held-TBR key are used.

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| blanket__blanket_t | constraints_reachable | Not applicable: no no-constraint-response result. | Swept; declared graph paths exist. |
| plasma__R | constraints_reachable | Not applicable: no no-constraint-response result. | One diagnostic; declared graph paths exist. |

Both groups were traced without a subset and have no sibling warnings. [Indicators](indicators.json) establish possible paths, not observed constraint response. Monotonicity, same-quantity identity across different names and intra-module operand dependency are not derivable. No no-constraint-response model-gap finding is owed because neither axis has that result.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | Two complete keys across two groups. |
| Suffix-sibling scan | pass | No undeclared suffix siblings. |
| Baseline gate | pass | `results/baseline_result.json`; headline relative deviation0, all20 pinned verdicts match. |
| Executable identity | pass | `results/package_identity.json`; sealed bytes match, no adapter. |
| Manifest currency | pass | Both package fingerprints match. |
| Package cleanliness | pass | Before and after native execution. |

[Full gates](results/preflight_results.json); [post-run check](results/post-run-clean.json). No gate was skipped.

## 10. Execution route and why

- **Route:** study-local direct API using stock `StudyRunner` and `PreparedListStrategy`.
- **Why this route:** the exact released baseline and all gates passed before the fixed finite list executed. It preserves supported sensitivities and undefined diagnostics in one native store.

Glue ledger: none; no adapter or harness-supplied model quantity. Launcher import setup only exposes the pinned teax runtime. The harness copies native outputs and masks undefined breeding-derived carriers for display, retaining their raw values. [Environment receipt](results/execution-environment.json) records the existing serializer warning; no execution phase refused or failed.

## 11. Study definition and window provenance

The window is engineered from the upstream validated thickness domain, with interior sensitivity samples and three explicit unsupported diagnostics. After the released baseline and gates, the independent oracle evaluated all13 proposed cases and confirmed expected applicability. The full list was then retained without exclusions in `preparation/proposals.json`; [window check](reviews/window-selection.md) records that decision. The study cannot establish a continuous feasible boundary or optimum. No model, allowance or limit was tuned to restore a passing point.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint; no cross-arm correlation is needed. Historical studies are not rewritten or treated as evaluations of this package.

## 13. Verification

All mapped software values and all authored predicate outcomes agree at every case. The generic verifier passes without boundary exceptions. Its receipt labels the teax revision “unrecorded”; the snapshot records the actual git revision checked against the integration pin. [All-point verification](results/oracle-all-points.json) and [generic verification](results/verification_summary.json) retain the evidence.

All261 native numeric outputs are retained;16 lie outside the245-channel oracle map. Shared transport-table data are identical by construction and receive no independent physical-verification credit. The copied physical reviews support the bounded conceptual scenario and disclose approximate benchmark reconstruction, material/source sensitivities and absence of actual stellarator qualification.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Independent physical/data/interface release | PASS for conditional conceptual integration | [Copied review](reviews/table-release-review.md) applies to the unchanged frozen response and scenario, with benchmark/material/geometry limitations. |
| Native integration | CANDIDATE; all10 gates pass | [Return](preparation/integration-return.json) and [coordinator release](preparation/execution-release.json) pin the executed candidate. |
| Framing and window | Executor check passed under coordinator delegation | All proposed cases retained after oracle scan; no optimization or feasible-boundary claim. |
| Final independent study/goal review | Pending coordinator review | This record is executor-authored; no independent final approval is asserted. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| 20260918-computed-tritium-breeding#1 | model | Thicker supported breeder clears the sampled breeding screen while incurring peak-field failure and higher cost; all cases retain other failures. | Conditional sampled tradeoff, no whole-plant feasible point. | `report.md` |
| 20260918-computed-tritium-breeding#2 | model | Native CAS22 blanket volume aggregates full-shell first wall, breeder and reflector; transport removes3% of breeder/reflector/shield. | Retain quantified inventory/cost convention; no identical-inventory or installed-cost claim. | `report.md` |
| 20260918-computed-tritium-breeding#3 | model | Unsupported thickness or fixed-geometry change yields undefined breeding while unrelated outputs and independent fuel-account terms remain available. | Keep native failed TBR screen and raw carriers; null only derived display fields. | `report.md` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `4ed3597f081ada28a208b11dd9f6276fde0e065631fb92e2f06d89ecbe7b9b02`
- **Schema version:** `1`

## 17. What this record does not contain

No whole-plant feasible design, continuous feasible boundary, economic optimum, actual stellarator qualification or full physical uncertainty bound is supplied. Large nuclear-data/statepoint/source-bank binaries are absent; compact transport evidence and its original hashes are retained. The copied transport report’s original plot is not copied, but its numerical tables are present. The generated-study plot is retained separately. This record contains no post-execution model repair, independent final study reading or coordinator commit; those are coordinator-owned next steps.
