# T-021: major-radius ownership assessment

## Scope and conclusion

[INHERITED] Scope is T-021 at `work/orchestration/goals/fusion-audit-remediation/trail.md@c9442035`, under Round 5 strategy `model-owned-major-radius@eed3b976`. Assessed canonical model `b9d096f6`, current package consumers `676c7308`, WI-050 audit `55456198`, and original F06/F07 at `.project/reports/20260907-fusion-model-audit.md@e341dc34`. This is native `analyze-models` operational analysis, not an independent audit or a goal review. The host refused a fresh thread; the parent explicitly reused this earlier non-author design-review context. The parent performed the source/image assessment independently and supplied the evidence identified below.

- The two public radius inputs still describe two independently changeable halves of the intended machine. Plant-only and magnet-only changes execute but disagree with the direct oracle in 106 and 107 published channels respectively. The baseline and coordinated-radius case agree.
- The oracle's sustainment helper reads the wrong radius input. A temporary in-memory correction of that one operand restores all 141 shared published channels in all four successful cases, without changing either source or package.
- Existing source and model-intent evidence supports one major plasma/axis scale in the current supported toroidal plant. It does not establish that every real modular-coil reference surface is identical.
- [AGENT, ratified by parent 2026-09-11] Recommend a bounded F06 repair: one plant-owned radius binding, matching oracle wiring, retirement of the duplicate public input and update of affected live consumers. Preserve reusable standalone magnet inputs and fixed reference anchors.
- Broader F07 remains open. The original negative-peak component counterexample persists. Invalid full-plant probes fail execution; their failures must be retained and tested, not described as feasible designs or as complete domain enforcement. No general guard redesign is necessary merely to repair radius ownership.

No production, generated package, source registry, historical record or work item was changed. No integration, study, dependency installation, commit, alpha-basis change or financial change occurred. All Python commands used `.codex-test/run`; native execution used the existing TEAx runtime under the parent-specified environment.

## Current structure and dependencies

The reusable `Magnet System` owns a formal `R0`, documented as major radius, separately from the coil-bore `r_coil` (`models/library/cost_structure/mfe_power_core.sysml:65`). The generic plant instantiates this part (`models/designs/generic_mfe/mfe_plant.sysml:58`) and separately owns plant `R` (`:133`). The only concrete canonical MFE specialization binds both to independent 12.7 m literals (`models/designs/stellarator_09/stellarator_plant.sysml:139,528`). There is no producer binding or equality assertion between them.

| Public source | Exact generated direct consumers | Downstream effect |
|---|---|---|
| `stellarator_09__stellaris__R` | `geom.R_in`, `rb.R_in`, `sustain.R_in`, `divheat.R_in` | Plasma volume/aspect ratio, torus-shell volumes/wall area, confinement/radiation and its fuel/heat/power/cost consequences, divertor area-scaled shadow |
| `stellarator_09__stellaris__magnet__R0` | `field_calc.R0`, `peak_field_calc.R_in`, `stored_energy.R0`, `coil_length.R0`, `magnet_cost.R0` | Axis field, normalized bore field, stored energy/casing mass, winding length/cold volume, conductor quantity |

The exact full `(module, formal)` pairs, public parameter records and source hashes are retained in [inventory.json](20260911-230953_radius-ownership-evidence/inventory.json). Source wiring is visible at generic plant `:142–168,248–250,279–308,330–332,618,1101`. The generated graph confirms those bindings; it is not inferred only from attribute names.

The oracle uses plant `R` for geometry (`exploration/stellarator_e2e/verify_stellaris.py:512`) but `magnet_R0` in its sustainment helper (`:111`). Its field is separately calculated from `magnet_R0`. Thus the wrong helper operand changes confinement and radiation even when the field itself has the correct independently selected magnet radius. The live adapter maps both keys (`exploration/stellarator_e2e/studies/oracle_entry.py:53`), while the live route inserts a tie (`study_route.py:63,95`) and the manifest declares it (`manifest.json:102`). Coordinated studies conceal both defects.

There are 23 owned MFE logical model files; all 23 canonical/twin pairs are byte-identical in this assessment. `tests/model_families.py:58` defines the family boundary. No second concrete canonical MFE plant or another canonical `Magnet System` instance was found. Standalone reusable calculation definitions remain legitimate callers of explicit radius formals; changing their mathematical interfaces is unnecessary. IFE shares only foundation/CAS files, none implicated here.

## Existing source meaning

The parent's [source-meaning.md](20260911-230953_radius-ownership-evidence/source-meaning.md) records its direct image observations and exact hashes. The copied [Table 2 image](20260911-230953_radius-ownership-evidence/stellaris-table2.png) labels major plasma radius 12.7 m and minor plasma radius 1.3 m. The registered PDF hash matches the source index. This analyst did not independently repeat that source review.

[INHERITED: parent source assessment] Existing field-linkage documentation uses that same Table 2 radius; the magnet source distinguishes major radius from the coil-bore radius. The WI-032 interpretation names current linking the magnetic axis. No separately variable offset/reference-surface relation is declared for `magnet.R0` in this supported model. Consequently, joining its input to plant `R` expresses existing model intent rather than introducing a new empirical equality law. The source evidence does not supply an admissible radius envelope or certify the exact geometry of real modular coils.

Keep the reference parameters independent of the live producer: `magnet.R_ref`, `magnet.a_coil_ref`, `wall_peak_R_ref` and `R_ref_divertor` are fixed calibration/source-case anchors. Joining them to live `R` would erase intended off-design responses and exceed F06. Likewise, `r_coil = vessel_or` and `r_coil_centre = vessel_or + coil_t/2` are distinct minor-radius quantities and remain distinct.

## Native counterexamples

Read-only strict package execution used semantic fingerprint `8f4912c20870b8e0090f9836292403d9d05b0b0e6d46dabf53713772737666cf`, executable fingerprint `a9514eb6505dea1589f47cb20bd004e480d61b3be98e7d793bf195b1b2d773b0`, 247 public parameters and 18 named constraints. Temporary import links were created under `/tmp`. Complete outputs, verdicts, error messages and controls are in [results.json](20260911-230953_radius-ownership-evidence/results.json); executable reproduction is [probe.py](20260911-230953_radius-ownership-evidence/probe.py) and [probe.log](20260911-230953_radius-ownership-evidence/probe.log).

All controls other than the indicated radii remain at the current baseline. These points are diagnostic comparisons; none of the four successfully evaluated plants satisfies every existing constraint.

| Case | Plant R / magnet R0 [m] | Native volume [m^3] | Native axis field [T] | Native winding length [m] | Native required auxiliary [MW] | Oracle required auxiliary [MW] |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 12.7 / 12.7 | 425.000014 | 9.000000 | 25.000000 | 49.079601 | 49.079601 |
| Plant-only change | 14 / 12.7 | 468.503953 | 9.000000 | 25.000000 | 52.109835 | 99.726514 |
| Magnet-only change | 12.7 / 14 | 425.000014 | 8.164286 | 27.559055 | 107.903911 | 59.741320 |
| Coordinated change | 14 / 14 | 468.503953 | 8.164286 | 27.559055 | 116.053112 | 116.053112 |

| Case | Native net [MW] | Oracle net [MW] | Native headline LCOE [$/MWh] | Oracle headline LCOE [$/MWh] | Mismatched shared channels at 1e-9 relative/absolute |
|---|---:|---:|---:|---:|---:|
| Baseline | 1013.931933 | 1013.931933 | 224.269233 | 224.269233 | 0 |
| Plant-only change | 1096.105584 | 1072.510392 | 218.278356 | 235.064527 | 106 |
| Magnet-only change | 988.182972 | 1014.411652 | 255.872008 | 241.915934 | 107 |
| Coordinated change | 1061.048280 | 1061.048280 | 250.898322 | 250.898322 | 0 |

Baseline violates divertor heat. Plant-only R14 additionally violates sustainment and loop capacity. Magnet-only R14 and coordinated R14 violate divertor heat, wall load, sustainment and loop capacity. The aggregate `headline` response is also violated; it is not a nineteenth authored constraint.

[AGENT] Independent geometric checks use the equations' ratio identities, rather than treating oracle parity as the complete test: with minor geometry/current fixed, plasma volume scales with plant R; field and stored energy scale inversely with magnet R0; winding length scales with magnet R0; peak field scales inversely with `R0 - r_coil_centre`. All checks pass on the native outputs. The old conductor procurement channel is invariant because `B*R0` cancels at fixed current; this is a meaningful exception to a blanket expectation that every magnet cost must change. The decomposed magnet capital does change: $5.401032 billion baseline to $5.944337459 billion for magnet/coordinated R14, through winding/casing consequences.

The independent oracle-isolation experiment temporarily changes only the sustainment helper's local radius operand to plant R, restoring it afterwards. All 141 shared published channels then match native execution in baseline, plant-only, magnet-only and coordinated cases. [checks.py](20260911-230953_radius-ownership-evidence/checks.py), [checks.json](20260911-230953_radius-ownership-evidence/checks.json) and its log retain this evidence. This establishes the specific oracle mismatch; it does not repair the native split, recertify the physics or change the existing source bindings on disk.

## Directly implicated domain behavior

The current model's baseline vessel outer radius is 3.0000000000000004 m, coil-centre radius is 3.1500000000000004 m and complete outer build is 3.5500000000000003 m. These are different surfaces. The study route's `R > a + 2.25` mask corresponds to the outer build, not the peak-field singularity at the coil centre (`study_route.py:67`; `ANNEX.md:70`). It is a study-specific restriction, not an authored model guard.

| Probe | Observed result | Scope of conclusion |
|---|---|---|
| Original peak component: R=12.7, coil centre=13, valid reference | Generated B_peak = −792.6499999999979 T; comparison `B_peak <= 24.9` is true | Original F07 component failure persists. It is not a full-plant feasibility result. |
| Peak component: live coil centre=R=12.7 | `ZeroDivisionError` | Live normalization denominator is singular. |
| Peak component: reference coil centre=reference R=12.7 | `ZeroDivisionError` | Reference normalization has its own denominator. |
| Peak component: reference coil centre=13 > reference R=12.7 | B_peak = −0.7821989528795832 T, satisfying the upper comparison | Invalid reference geometry can also invert the sign. |
| Full plant: tied R=4 | `EvaluationFailed`, non-positive fuel density | Ordinary geometrically fitting point fails the existing sustainment evaluation; it produces no complete cost/verdict result. |
| Full plant: tied R=exact baseline coil-centre radius | `EvaluationFailed`, division by zero | Existing tied route already exposes the singularity that a unified radius can reach. |
| Full plant: tied R=3 | `EvaluationFailed`, non-positive fuel density | This below-bore full plant is rejected by another computation; it is not proof that every invalid-clearance point is rejected. |
| Full plant: plant-only R=0 / magnet-only R0=0 | `EvaluationFailed`, respectively zero raised to negative power / division by zero | Both public inputs already admit unsupported arithmetic domains. |
| Full plant: tied R=R0=−1 | `EvaluationFailed`, complex-number type failure | Unsupported negative-radius arithmetic, not a valid operating result. |

[AGENT, ratified by parent 2026-09-11] Keep F06 repair bounded to ownership and matching consumers. Joining the producer introduces no new equation; current coordinated-radius probes already execute the proposed coherent input combinations. Retaining explicit invalid-case failures is sufficient for this bounded dependency repair, provided implementation does not clip inputs, reinterpret errors as accepted operation, or claim general domain validity. The original component F07 defect remains an open adverse finding.

A new positive-clearance/domain assertion could be valuable, but would add model behavior, verdicts and consumer obligations. It is not automatically required to establish that F06 has one owner. If the implementation unexpectedly turns a rejected case into an apparently accepted point or exposes a new defect caused by the binding, stop and assess the directly necessary handling. Broad efficiency, thickness, cryogenic, current-density and other F07 guards remain outside this assessment. No owner residual acceptance or F07 closure is implied.

## Public interface, callers and coverage

[AGENT] The smallest supported repair binds the generic plant's magnet radius usage to plant R and removes the concrete stellarator's independent literal, while retaining `R0` as a reusable library formal. A concrete-instance-only binding is a possible narrower placement if design discovers a genuinely supported generic caller requiring independent surfaces; the present canonical inventory found none. Prototype the selected binding and verify producer edges through native generation. Expected public census is 247→246 if only the duplicate design input retires; this is a prediction to re-derive, not a replacement for the generated contract.

| Affected surface | Required bounded follow-through |
|---|---|
| Canonical generic/stellarator source and MFE twin | One producer reaches all nine listed direct radius consumers. Keep the standalone magnet definitions and all fixed reference anchors. Baseline scalar values should remain unchanged. |
| Generated contracts, inputs, pipeline, sealed identities | Retire `stellarator_09__stellaris__magnet__R0` as an independent entry; regenerate deterministically with normative handwritten implementations preserved. Confirm the remaining plant R reaches field, peak, stored energy, winding and cost inputs as well as geometry/sustainment. |
| `tests/models/data/mfe_census.json` and `test_model_family_spines.py:97,172` | Re-derive public entry inventory; add exact `(group,key)` to `(module,formal)` radius coverage rather than relying on suffixes or module reachability. Existing family tests focus on CAS28/blanket and do not assert this invariant. |
| `verify_stellaris.py:111`, live `oracle_entry.py:53,490` | Use plant R consistently for sustainment and magnet operation; remove the independent live public override. Test normal R-only mutation and obsolete/conflicting-key behavior explicitly. No silent input dropping or stale legacy default should recreate the split. |
| `run_stellaris.py` / `run_stellaris_single.py` | Preserve baseline channels and anchors, update any public-input/identity assumptions and execute plain R off baseline through both paths. |
| Live `studies/manifest.json:102`, `study_route.py:63,95`, `ANNEX.md:11` | Remove the now-redundant current-package tie and ensure ordinary R proposal construction works. Preserve the independent meaning of reference radii. |
| `tests/study/data/axes.known_answers.json`, `axes.extras.json`, `R.expected.json`, `R+tie.expected.json` | Re-derive current-package fixtures and replace package-specific reliance on an independent R0. Do not globally remove generic tie tests. |
| `tests/study/test_warnings.py`, `test_provenance.py`, `test_known_answers.py:295`, `test_operand_bindings.py:27`, `test_subset_flag.py` | Update changed current-package key/count/tie expectations; keep generic synthetic tie/provenance coverage. Reachability alone is insufficient: current tests explicitly acknowledge that plain R and tied R can have equal traced reach but different executed responses. |
| Historical studies, snapshots and context copies | Preserve their recorded keys, ties and fingerprints. They remain evidence at old packages, not callers to rewrite opportunistically. Later integration and a new study are separate tasks. |

The current peak-field structural test (`tests/models/test_beta_peak_field.py:61`) checks definition/formal presence and the upper comparison, not live/reference clearance. Traceability rows `data/traceability_matrix.csv:51,62–64` record the inherited field/bore relation, including its anchored approximation. Validation entries for the existing geometry/field increments document successful prior baselines, not the missing major-radius identity. A future Standard item should register verification of that invariant and ordinary-input counterexample explicitly.

## Compliance and current health

Project MR-3/6 and AD-004 support a plant-level usage binding with reusable calculations retained in the library. MR-4 supports preserving the existing source/basis and documenting one intended quantity; no new physical value is required. MR-1/2 cost interfaces and AD-003 financial expressions need no modification. This assessment proposes no new project requirement or supported concept/module expansion.

Broad validation was not rerun because this task made no model mutation. The positive bounded WI-050 audit at `55456198` is the entering evidence: Level 1 pass; Level 2 fail with ten inherited literal-placeholder findings; Level 3 pass; Level 4 reports 18 numerical assertions; Level 5 documents 86/86 elements; Level 6 fail with 229 findings, including the two explicitly assessed producer-default diagnostics. Its full model regression is 364 passed / 13 inherited skips. Those counts certify neither F06 nor broader F07. The current package-consumer audit additionally records 150 passed, 86 historical failures and one historical-store skip for its broad scoped run; this is not a green global suite.

The bounded execution performed here establishes the defect and its concrete consequences without repeating those broad checks. Future implementation still needs family isolation, exact public contract/edge checks, baseline preservation, ordinary R-only execution, independently derived geometric responses, live oracle parity, current consumer tests and fresh independent audit.

## Recommended next action

[AGENT, ratified by parent 2026-09-11] Open one Standard native modeling repair for F06 under the existing strategy. Its contract should require one supported plant radius producer, removal of the duplicate public degree of freedom, correction of the oracle operand and current live consumer updates. Before production changes, retain independent expectations: baseline unchanged; ordinary R14 after repair matches the present coordinated R14 diagnostic; the listed geometric ratios hold; retired-key proposals cannot silently recreate inconsistent geometry. Retain all invalid-case evidence and clearly carry F07 without accepting it.

No source-meaning blocker, second supported reference surface or required new financial convention was found. Native binding/generation remains a design-prototype question, not a capability claim supplied by this read-only assessment. No work item, integration candidate or study was created here.

[AGENT: parent sequencing] The parent proposes model/twin/generated ownership and direct model-caller tests first, followed by separate coding/certification of the live study oracle adapter and metadata, matching Round 4. This separation is mechanically viable: the dependency inventory reveals no requirement for an atomic edit across those stages. The model stage should publish the retired key, revised contract and direct-oracle expectation as an explicit handoff. Until the live study adapter/manifest/fixtures are updated and certified, current-study compatibility remains incomplete and integration/study execution cannot receive passing credit.
