---
Status: active
Scale: standard
Epic: standalone
Owner: agent
Created: 2026-09-18
Updated: 2026-09-18
---
# WI-066: Computed tritium breeding

## Contract

[NEED] Calculate tritium breeding ratio (TBR), the number of tritium atoms produced per fusion neutron, from supported choices in the retained helium/PbLi blanket. Verify the physical basis independently of software agreement. Make inadequate breeding constrain design feasibility, without requiring a physically adequate design. Owner authority: `work/orchestration/goals/computed-tritium-breeding/goal.md`, including the scientific-judgment delegation.

[NEED] Meet the unchanged R2c.P2 and P3 rubric at revision `dc0f0b6dc6512b29e1307da647f3a508a1f5356d`: “TBR computed from blanket configuration” and “computed TBR vs floor pushes back on blanket/build choices.” Preserve ARIES quarantine, excluded derivatives, frozen r2 and historical results. Do not tune limits or recovery to restore old passes. Formal goal closure, reveal, comparison replacement, merge and push remain reserved.

[INHERITED] Follow `modeling_project/REQUIREMENTS.md`, `MODELING_PROCESS.md`, `.project/codex-test-setup.md`, source registration and native integration/study workflows. Entering interfaces are traced in the goal's `evidence/current-trace.md`. The held 1.074 comes from a different water-cooled geometry and is not a validated prediction for this plant. The current fuel balance requires approximately 1.190 under its assumptions.

## Supported physical model

[AGENT] Use continuous-energy neutron transport in finite toroidal shells matching the retained generic build. Preserve declared material and source choices as scenario assumptions, with source-supported compositions and densities. Tally extractable breeder Li-6 and Li-7 tritium separately; exclude nonrecoverable production elsewhere from the fuel supply. The physical-method precheck at `evidence/round2/method-precheck.md` releases prototype implementation and defines the scientific acceptance conditions.

[AGENT] A narrow table interpolation may become the generated model calculation after direct transport, independent experimental comparison and withheld interpolation validation. The initial supported executable lever is breeder thickness at fixed 70% lithium-6 atomic enrichment. Enrichment variations remain separately identified direct-transport sensitivity cases. Every fixed geometry, material and coverage assumption is part of the applicability domain. Unsupported changes must be rejected or make applicability fail explicitly; no silent extrapolation or clamping. The concrete table, tolerance and interface design will be frozen after prototype evidence, before production implementation.

[AGENT] Report Monte Carlo statistical uncertainty, interpolation error, reconstruction/benchmark discrepancies and physical scenario sensitivities separately. Unresolved shaped-stellarator bias remains visible; a conceptual torus calculation does not qualify the actual stellarator. A near-threshold result whose assessed range crosses the criterion is unresolved adequacy.

## Adequacy account

[AGENT] Retain the existing 1.05 design floor as an explicit policy input. Compute the fuel-balance requirement from burn, exhaust recycle losses, extraction efficiency, radioactive decay and reserve growth, with distinct quantities and semantics. Use the stricter of the design floor and conditional fuel-balance requirement. This avoids adding an unexplained reserve twice. The inherited 0.99 recycle factor remains an assumed isotope-recovery scenario; its original cost-derived basis does not establish physical recovery. Unity extraction and zero inventory/growth are optimistic assumptions, not omitted terms silently judged negligible.

[NEED] The calculated achieved value must feed both production accounting and the adequacy comparison. A supported thickness change must also retain the existing volume, cost, coil-bore and associated plant consequences. The held neutron-energy multiplier remains a separately disclosed approximation unless transport supplies a verified replacement; breeding production must not silently change its meaning or double count energy.

## Consumers

[AGENT] Inspect and update canonical SysML and exploration twins, generated package interfaces/implementation, strict manual seed inventory if needed, independent oracle and operand/output mappings, live snapshot/census/manifest and affected tests. Preserve unrelated manual implementations. Current calculation and predicate counts are derived from generated contracts, with changed expectations justified before regeneration. Historical studies and the published r2 archive remain immutable.

## Persistent execution plan

- [x] Trace entering TBR, fuel balance, build and feasibility consumers; review source candidates and reject unsupported surrogate transfer.
- [x] Obtain fresh physical-method precheck before substantial implementation.
- [x] Freeze complete sourced material cards and run the declared approximate experimental reconstructions; independent benchmark-and-interface review accepts the limited consistency claim and retains reconstruction gaps and failures.
- [x] Verify transport geometry, source, isotope inventories, tally semantics and numerical convergence; quantify declared physical sensitivities.
- [x] Freeze concrete implementation design, table/domain and withheld validation; obtain changed-method review if warranted.
- [x] Implement SysML and executable calculation, requirement and applicability behavior; verify independent software oracle and dependency effects.
- [x] Run targeted validation; regenerate, recapture and repin. Independent audit covers implementation and explicitly disposes static-tool diagnostics; clean-package verifier/native integration remain next.
- [ ] Pass native integration and execute a focused native study preserving inadequate and unsupported cases.
- [ ] Obtain fresh unchanged-rubric P grade, evidence review and engineer-readable goal answer. Leave formal closure to owner.

## Acceptance evidence

Physical response release accepted by the independent table-release-review.md under the goal Round2 evidence. Five nodes and six withheld checks pass the frozen criteria; approximate integral benchmark consistency remains limited. Final generated-package, study and P2/P3 evidence is still pending.

## Native verification registry

SV-113 tracks physical/response evidence; SV-114 tracks conditional adequacy. Both remain pending until integrated evidence is accepted. Native registration reported two inherited malformed Type cells in the validation matrix; this work does not repair unrelated entries.

## Expected interface change before regeneration

[AGENT] The native interface probe derives exactly one retired public input, `stellarator_09__stellaris__blanket__tbr`, and no new independent geometry inputs. Existing owner geometry drives the response guards. Expected current package inputs313→312; numeric outputs242→261 (seven response and twelve adequacy outputs); complete contract outputs263→282 including existing response channels; independent oracle mappings226→245. All twenty constraint IDs remain unchanged, including `tbr_ok`. Its two operands become computed validity and numerical margin. Existing scalar predictions remain unchanged except the fuel breeding margin; new quantities and that changed margin must agree with the independent oracle. Baseline `tbr_ok` is expected to change from satisfied to violated because the declared numerical lower estimate falls below the conditional requirement. No historical archive or old result is restated.
