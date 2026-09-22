# Early WI-089 binding review

[AGENT] 2026-09-22. Bounded inspection during implementation, before acceptance evidence. Canonical identities inspected: `models/library/analyses/integrated_heat_electricity.sysml` SHA256 `ad0288542e3cecd81e8a21db2ba4f8381af8208d0255421599d140ae78efe8b9`; `models/designs/aries_cs_integrated/plant.sysml` SHA256 `c985f4f92b566cec6cc2cee53c16ab316333fd6ce81d68a22552eb3236b205af`. The author is still editing. This record does not certify execution.

[AGENT] Source-selected power feeds both the unchanged fuel occurrence and new deposition calculation. A single transfer feeds helium with plus sign and PbLi with minus sign; absent directions consume a generated zero. Calculated delivered branch heat feeds the closure, whose solved inlet feeds the unchanged turbine. Actual compressor and turbine work feed the electrical calculation. Shared flow, primary flows, UA, stage ratios and all eight ratings remain supplied attributes. Heat-duty screens use full branch duty rather than the capacity-limited transferred heat. Unmet duty has its own asserted constraint. These inspected bindings preserve the intended evaluation direction.

[AGENT] Scientific support outputs are native ledger outputs, distinct from assumed scalar-screen support inputs. Their implementations remain subject to final review. Comparison targets enter only the ledger. The observed code computes source differences without using them to select flow, equipment or turbine temperature. The selected-power completion rejects zero before publishing the fuel/heat input.

## Findings sent to author and coordinator

- **E1 — physical electrical owner missing.** `plant.sysml:353` places generator conversion, motor import and auxiliary demand laws entirely inside `plant_ledger`, rather than providing the accepted `Generator/auxiliaries → plant ledger` interface. Give these functions real component calculation ownership and feed their EXPOSE terms into the residual ledger. This is a bounded ownership repair, not a request for another plant solver.
- **E2 — advertised outputs absent.** The accepted design promises separate fixed/variable fuel-electric contributions and each exchanger's available hot-bound margin. The initial interface exposes total fuel electricity and primary temperatures but no computed variable contribution or hot-bound margins. Add graph-owned outputs or identify exact equivalent interfaces.
- **E3 — zero-transfer primary state can be fictitious.** In `native_completions/heat_driven_closure_impl.py`, `evaluate()` reports primary `hot=secondary` and `state_defined=1` whenever K is positive, including `secondary>=hot_limit` where q is zero. That state can exceed the supplied primary limit even though the exchanger is bypassed. Mark such primary states undefined with a documented carrier, or expose and explicitly classify the violated bound. Native terminal temperature differences need the same definedness treatment.

[AGENT] MR-7 is compliant for the inspected selected-versus-calculated binding direction. Native sufficient/insufficient behavior, generated-entry preservation, full support propagation and integrated upstream-to-net response remain unverified. Final review must examine the corrected identities and actual execution evidence.

## Corrective disposition

[AGENT] E1–E3 are resolved at executable fingerprint `469191fd32c624ccf70e0b4ebc1065b34920df8174c37a09e8f45ecfb241a7d7`. The corrective inspection, native bypass replay, exact canonical identities and final bounded verdict are recorded in `implementation-review.md`.
