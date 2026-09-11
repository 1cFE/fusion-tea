# Current MFE operating heating assessment — T-015

## Scope and result

[AGENT assessment] F04 remains open at current revision. The model computes a sustained heating requirement and tests that installed capacity can supply it, but prices thermal and electrical operation using all installed heating. Increasing reserve capacity changes the priced operating flow while the required heating and fusion output stay identical. This is current execution evidence, not a restatement of the September 7 audit.

- Executed the existing sealed stellarator package at its baseline and with installed wall-plug capacity increased from 100 to 120 MW. Only copied input and pipeline files changed under the adjacent evidence directory. No model, generated package, integration metadata, source, historical evidence, study, or pin changed.
- Required plasma-coupled heating is 49.079600788 MW at both points. Coupled heating priced by the plant rises from 50 to 60 MW; net generation falls by 17.029497549 MW. Installed heating capital correctly rises by $52.829 million, but the power penalty also prices the unused reserve as operating continuously.
- The issue reaches the primary coolant loop and divertor ledger as well as the electric balance. A correction limited to electric subtraction would leave inconsistent operating states.
- Both cases have 13 satisfied assertions and a violated divertor-heat assertion. Neither is an all-constraints-feasible plant. A satisfied heating-capacity pair does not establish operating-flow consistency.

This bounded analysis covers the generic-MFE assembly, its heating/sustainment/thermal/electrical/divertor/cost paths, and the current stellarator parameterization. Pending-comparison preservation choices are assessed separately in [the companion report](20260911-190740_mfe-pending-comparison-preservation.md). This report does not select a preservation option or accept an F04 residual.

## Current execution

Evidence: [probe and reproduction](20260911-190758_mfe-operating-state-evidence/probe.py), [results and identities](20260911-190758_mfe-operating-state-evidence/results.json), [execution log](20260911-190758_mfe-operating-state-evidence/execution.log). Source HEAD was `b14ed1b2f593f4fb8aba7259597c2524e43466ec`; strict-loaded executable fingerprint was `234d0b27d2b5327ede2cae1c05a2e1c1ead1d89337fd019782bdda03d841e81d`. The result records SHA256 digests of relevant model files. The reserve case uses the same generated implementations and wiring, with one copied parameter changed. The fingerprint identifies the unchanged executable package, not an independently sealed reserve case.

| Quantity | Baseline | Reserve counterexample |
|---|---:|---:|
| Installed wall-plug heating, MW | 100 | 120 |
| Installed delivered / coupled heating, MW | 50 / 50 | 60 / 60 |
| Required coupled heating, MW | 49.079600788 | 49.079600788 |
| Fusion power, MW | 2652.563262518 | 2652.563262518 |
| Reactor source heat, MW | 3126.852676295 | 3136.852676295 |
| Per-loop coolant flow, kg/s | 215.045849928 | 215.733588917 |
| Pump draw and recovered pump heat, MW each | 175.436542688 | 177.133186660 |
| Cycle efficiency | 0.411356554050 | 0.411356554050 |
| Total thermal power, MW | 3302.289218982 | 3313.985862955 |
| Gross electric power, MW | 1358.418313596 | 1363.229804754 |
| Net electric power, MW | 1012.364869900 | 995.335372351 |
| Heating capital, dollars | 264145000 | 316974000 |
| Total capital, dollars | 14955212350.386 | 15039989066.172 |
| Current-model LCOE, dollars/MWh | 224.609524728 | 229.541287969 |
| Divertor target peak, MW/m² | 10.535329131 | 10.725329131 |
| Operating-minus-installed heating diagnostic, MW | -0.920399212 | -10.920399212 |

The 20 MW additional electric heating draw is partly offset by 4.811491159 MW more gross power, then worsened by 1.696643973 MW more pump draw and the modeled subsystem fraction of gross generation. Thus the net loss is 17.029497549 MW. The resulting 4.931763241 dollars/MWh LCOE increase includes both capital and operating changes. It is not a pure operating-cost effect.

## Dependency structure

1. **Capacity production:** `models/designs/generic_mfe/mfe_plant.sysml:495` binds installed wall-plug power and two efficiencies into the library heating chain. That chain publishes delivered capacity for procurement, coupled capacity, and total wall-plug draw (`models/library/analyses/mfe_heating_chain.sysml:4`).
2. **Required operating state:** the sustainment chain independently computes required coupled heating. `models/designs/stellarator_09/stellarator_plant.sysml:1594` compares it to installed coupled capacity; line 1615 tests its nonnegative lower bound. Neither assertion routes required heating into operation. Negative required heating is a burn-hold violation, not a zero-heating operating point.
3. **Thermal and electrical flow:** `models/designs/generic_mfe/mfe_plant.sysml:524` supplies installed coupled heating to reactor source heat, then to the primary loop's flow, pressure loss, compressor work and recovered heat. Line 559 supplies installed coupled heating and installed wall-plug draw to power balance alongside computed loop/cycle outputs. The cycle efficiency stays fixed for these two cases because the selected temperatures stay fixed; pump power changes with flow.
4. **Cost propagation:** heating procurement uses installed delivered power at `models/designs/generic_mfe/mfe_plant.sysml:681`. Power-dependent cost accounts consume the power-balance outputs beginning at line 579, so changing the operating basis also changes those modeled costs and LCOE. Preserving installed heating capital alone is not the whole economic contract.
5. **Divertor coupling:** `models/designs/generic_mfe/mfe_plant.sysml:1056` deliberately feeds installed coupled heating into the heat ledger, while required-minus-installed is diagnostic only. `models/library/analyses/mfe_divertor_heat.sysml:19` documents that basis and the fixed target geometry/transport assumption. Operating heat, source heat and electric demand need a coherent basis; any separate capacity-sizing or startup case must retain its declared meaning.

The relevant reusable definitions remain in `models/library/analyses/`; the assembly lives in `models/designs/generic_mfe/`, and concept values live in `models/designs/stellarator_09/`. No orphan inventory or project-wide unused-definition finding is claimed by this focused inspection.

## Algebraic counterfactual, not a corrected model

[AGENT diagnostic] At the baseline, substituting the computed 49.079600788 MW demand for the 50 MW installed coupled term, using the existing constant efficiency 0.5, gives 98.159201576 MW operating electric heating. The retained mirror equations propagate this substitution through the loop and divertor. They give net electric power 1013.931932554 MW, a gain of 1.567062654 MW; pump draw falls by 0.155608283 MW. Divertor target peak becomes 10.517841546 MW/m² and remains above its 10 MW/m² threshold.

This is an algebraic evaluation of the existing equations with held efficiencies, not execution of a corrected generated package, a sourced part-load model, or an engineering prediction. The mirror also changes equipment sizing if its heating input changes, so its counterfactual cost and LCOE outputs are deliberately not published. A correction must retain the separate installed-capacity procurement path and decide which other costs represent capacity versus operation.

The original audit's 83.8495 MW zero-demand example used the older fixed cycle and pump treatment and was explicitly algebraic. It is not a current baseline delta. This assessment uses a reserve-capacity counterexample at a positive required heating value; it does not infer a feasible zero-heating point from negative demand.

## Sources and assumptions

[INHERITED evidence] The existing source registry identifies the Stellaris design paper and its KIT mirror at `knowledge/SOURCE_INDEX.md:179`. The design's installed heating citation at `models/designs/stellarator_09/stellarator_plant.sysml:714` carries the printed 50 MW coupled startup/access value and its conversion to 100 MW electrical capacity. Its sustained operating-point interpretation is documented beside the assertions at line 1588. This analysis did not independently re-extract or inspect those source images and makes no new table-transcription certification.

[INHERITED assumption] The design's source efficiency 0.50 is tied to the existing 1costingFE costing constants at `models/designs/stellarator_09/stellarator_plant.sysml:741`. The coupling fraction 1.00 is explicitly an optimistic idealization at line 744. The heating-chain doc cites the upstream two-stage efficiency and delivered-power procurement basis. These support tracing the current algebra; they do not establish an operating efficiency versus load curve. No transmission stage, minimum stable load, startup schedule, standby draw or new efficiency law is inferred here.

[INHERITED assumption] The divertor relation uses the source's fixed target case and total radiated fraction, documented in `models/library/analyses/mfe_divertor_heat.sysml:19`. The algebraic counterfactual holds that assumption. It does not establish radiation feedback, target resizing, transient loads or irradiated component lifetime.

## Compliance and health

| Rule or check | Finding within this scope |
|---|---|
| MR-1 / MR-2, CAS and cost interface | Heating remains CAS22.1.4 and supplies its costed component. No interface defect identified in this path. |
| MR-3, reusable definitions / concept values | Observed separation is consistent in the heating, thermal and divertor paths inspected. |
| MR-4, quantitative traceability | Existing citations and explicit efficiency/target assumptions identified above. Source validity and all transitive citation links were not re-audited. No new physical parameter introduced. |
| MR-5, comparable outputs | Outputs exist, but F04 prevents treating a capacity sweep as a consistent held-plasma operating comparison. No normalized cross-concept comparison certified. |
| MR-6 / PR-3, documented patterns | Existing dormant-chain and installed-basis patterns are documented. A new operating/capacity split needs an explicit design contract before mutation. |
| PR-1 / PR-2 / PR-4 / PR-5 | Taxonomy and concept selection are outside this assessment. Analysis is preserved in native artifacts; commit remains the coordinator's action. No process completion inferred. |
| AD-001 / AD-004 / AD-007 | Plain Real with documented units and library organization are retained; magnet ownership is untouched. Other AD rules are not assessed here. |
| Syntax / targeted structure | Existing `tests/models/test_power_balance.py` passes: 25 passed, no skips. This is scoped parser/interface coverage, not full validation Levels 1–6. |
| Execution / translation parity | Strict package loading succeeded, both full pipeline calls completed, and 11 explicitly mapped relevant baseline outputs agree with the existing mirror to at most 2.531e-16 relative error. This is translation parity, not independent physics validation. |
| Constraint coverage | All 14 generated assertions retained in case outputs: 13 satisfied and divertor heat violated for each case. The missing operating-flow equality is demonstrated by execution despite passing capacity bounds. |
| Existing validation matrix | SV-069 and SV-072 record prior divertor reproduction and installed-basis baseline checks. These remain historical records and do not resolve F04. No matrix status changed. |
| Debt / tests | No TODO/FIXME markers in the three inspected heating, power-balance and divertor library files. The executed counterexample supplies evidence absent from the parser/interface checks. Broad test coverage and source completeness are not claimed. |

Probe construction encountered two harness mapping errors before the final successful run: the legacy shared channel map includes `contingency`, absent from the current oracle dictionary; its `annual_om` label maps generated `om_cost.annual_om`, whereas the oracle assigns `annual_om = cas70_annual + cas80_annual` at `exploration/stellarator_e2e/verify_stellaris.py:821`. The latter naive comparison produced relative difference 0.7471887867473227. Final parity checks use 11 explicitly selected F04-relevant correspondences; no annual-O&M parity is claimed. These attempts and their correction are recorded here because rerunning the probe overwrites its execution log. No model output was adjusted to satisfy the probe.

## Recommendation and reproduction

[AGENT recommendation] Keep F04 open. After the owner's pending-comparison ruling, route an explicit sustained operating heating producer through the source-heat, loop, power-balance and divertor operating ledgers, while retaining installed capacity for heating procurement and capacity limits. Distinguish any capacity-sizing and startup/access cases from sustained generation. Carry constant efficiencies only as an explicit supported approximation; obtain evidence before claiming load-dependent performance. Preserve the nonnegative burn-hold check rather than silently clipping unsupported points to zero demand.

Acceptance evidence should include this unchanged-plasma reserve test, positive and zero demand, insufficient capacity, negative-demand rejection, heating-capital invariance under operating demand alone, and conservation through coupled thermal/electrical/divertor paths. Those are proposed verification criteria, not newly accepted project requirements. The owner's preservation choice remains the prerequisite for shared mutation.

From the repository root, run:

```bash
.codex-test/run python work/analysis/20260911-190758_mfe-operating-state-evidence/probe.py
.codex-test/run python -m pytest tests/models/test_power_balance.py -q
```

The probe writes copied inputs, copied pipelines and full outputs under its own evidence directory; the strict loader uses a temporary import link. It runs no integration seam and performs no regeneration. The adjacent `test-power-balance.log` records the targeted test result. Shared modeling and generated artifacts remain read-only.
