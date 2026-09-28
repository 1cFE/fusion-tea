---
Verdict: pass
Created: 2026-09-22
Related Artifacts:
  Design: ../../../../active/WI-089_aries-integrated-heat-and-electricity/design.md
  Spec: ../../../../active/WI-089_aries-integrated-heat-and-electricity/spec.md
---

# Independent pre-implementation review

[AGENT] **PASS for implementation readiness.** The corrected physical approximation and fixed-hardware evaluation are accepted. This review covers the WI-089 spec, design and plan; it does not certify generated bindings or executed plant behavior.

## Evidence and source judgment

[AGENT] Directly inspected the retained primary images `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p734.png`, WI-087 `evidence/raffray-p736.png` and `raffray-p737.png`, and WI-088 `evidence/lyon-p716.png`. Reused the earlier `power-conversion-review.md` and `heat-transport-review.md` only for unchanged equation/component semantics, and inspected the actual generic Brayton, branch-heat and fuel definitions. No web acquisition or source-policy change was needed.

[AGENT] Table II supports the reconstructed direct blanket deposition of 940 and 1555 MW, the internal 111-MW transfer, separate 141-MW recovered friction and 156-MW electric pumping, and the retained 1-MW deposition discrepancy. Table III supports the reported cycle efficiencies, pressure ratio, loss fraction and cold temperature. Lyon Table VII supports 2436 MW fusion, 1253 MW gross electricity, 43 percent efficiency and the 1-GW-electric table basis. These sources describe different configurations. Their combination is an assumption, as the design states. Figure 12 shows a different PbLi/divertor arrangement; the proposed three sequential heaters are a declared approximation. The source's 30-degree exchanger temperature difference is not established by the proposed UA choices. Actual modeled terminal differences must be reported as conditional calculated states, not source reconstruction.

## Independent equation and architecture judgment

[AGENT] The counterflow effectiveness formula and equal-capacity limit follow the constant-property two-stream energy balances. Positive capacity rates and nonnegative UA give `0 <= K <= min(Ch,C)`. Thus primary hot inlet `Ti+q/K` and return `Ti+q/K-q/Ch` satisfy both terminal non-crossing conditions for positive K. The supplied hot bound limits transfer; no equation derives installed UA or flow from demand. At K=0 the operating primary temperatures are undefined. This treatment is acceptable when unmet deposition remains an explicit failure and the temperatures are described as states of the removable portion.

[AGENT] The scalar feedback closure has a valid bracket and unique root under the stated turbine and recuperator domain. At the lower bracket, accepted heat makes F nonpositive; at the upper bracket, heater inlet plus staged heating cannot exceed the maximum hot bound. Each stage has outlet slope between zero and one with respect to its inlet because K/C is at most one. Accepted heat is consequently nonincreasing with recuperator outlet temperature, while `C*(Tt-R)` increases strictly. Bisection is an operating-state calculation with independently chosen equipment. Runtime finite/domain checks, bypass handling and the unchanged expander comparison remain required.

[AGENT] Deposition partitions neutron multiplication, charged energy and auxiliary heat once. Internal coolant transfer cancels; recovered pump work enters source heat once and full electric pump draw enters auxiliaries once. Algebraically, subtracting generator/motor, unrecovered pump/heater and auxiliary losses from cycle net work gives the stated whole-plant identity. Unremoved heat belongs in the bookkeeping residual reconciliation but is not a physical rejection path; a zero ledger residual cannot override thermal inadequacy. The literal source-accounting mode correctly retains its separate source-energy mismatch. Signed shaft import and undefined zero-heat efficiency are appropriate.

[AGENT] Proposed ownership is proportionate: physical branches retain their duties and hardware, unchanged compressor/turbine calculations retain their state/work meaning, and only the coupled exchanger/recuperation closure requires an internal scalar solver. This is acceptable as a typed native calculation, provided the implementation actually forwards its state and duty outputs through the named owners and binds the unchanged turbine to the solved inlet. A disconnected Python plant implementation would not satisfy this review.

## Material finding

- **F1 — resolved: integrated zero-power domain.** The unchanged `models/library/analyses/mfe_fuel_cycle.sysml`, `Fuel Cycle Flows`, divides by `burn_rate` in `tbr_required`. The corrected spec and selector contract require strictly positive selected fusion power before exposing it to fuel and deposition. The corrected plan requires selected-zero-power refusal, uses positive fusion power for zero-UA tests, retains cooling-only precooler refusals and separately exercises the ledger's zero-heat branch. No inherited fuel change is needed. The corrective diff resolves the finding.

[AGENT] Accepted document SHA256 identities: spec `c537b9c235655d42a92ccd4085f03b2270b0283a8a8b6305f511a64ee1926601`; design `3590b4f161c965c865b1d4e0a11aa913619ad295be62a800998860a740abe80e`; plan `421ac45dff4442d6685a98f4cd529cc09669af54e463921d46f81fd2a04eecd1`. Subsequent execution-status checkbox updates do not change this semantic scope.

## MR-7 and acceptance boundary

[AGENT] **MR-7 compliant at proposed-design scope:** selected flow, primary flow, UA, stage ratios and ratings remain independent; operating temperatures and accepted heat are solved quantities; insufficient heat removal and scalar equipment limits are reported without resizing. No inventory or cost calculation is introduced. **MR-7 unverified at implementation scope:** inspect actual public inputs and EXPOSE bindings, native insufficient/sufficient capacity outcomes, fixed-hardware density response through fuel/heat/net, and unsupported-result handling before completion. The plan covers these obligations. Scientific qualification of deposition, magnets, breeding, hydraulics, materials and machine maps remains unsupported, regardless of a successful native run.
