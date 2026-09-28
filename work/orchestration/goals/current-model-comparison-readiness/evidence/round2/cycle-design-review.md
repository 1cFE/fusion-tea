# Corrective physical and native design review

[AGENT; non-author `/root/cycle_physical_critic`; 2026-09-19] **PASS after corrections. Release bounded implementation of the reviewed WI-073 design, interface and plan.** This is a corrected submission, not an initial clean pass. No native scientific implementation, adoption, archive or reveal is certified.

The original physical findings are resolved: v2 removes the invented 95% quality fence, keeps the 3% allowance's historical scope unresolved, and specifies guarded conditional cooling water. Original proposal/prototype/results/check hashes match the first review; the native final pending record contains the exact corrected proposal. The independent six-case source/math evidence therefore remains applicable without rerunning unchanged arithmetic.

Two further documentation findings were raised during this review and corrected by the coordinator before release:

- The Round 1 agent-proposed minimum-20 K screen and its failed 10 K case remain historical scenario evidence. The new strict-positive-gap check tests heat-flow direction. It neither supersedes that earlier screen nor establishes installed equipment adequacy. The old implemented equipment test checked fit argument ≤465°C; it did not implement a 20 K minimum.
- Existing scalar comparison policy remains relative 1e−9/absolute 1e−6, with stricter historical quantity policies preserved. The unsupported new relative-1e−8 policy was removed. The separately justified 1e−6 relative author-quadrature UA comparison and explicit balance residual policies remain separate from strict physical inequalities.

## Released design and implementation conditions

The additive guarded calculation, named component/state aliases and downstream cooling-water owner form a coherent design. Fixed supported pressures, explicit phase/temperature/quality domains and refusal before interpolation prevent false property support. Condensate-pump outlet temperature/entropy remain undeclared. Component assumptions feed the solver; calculated states remain outputs. Required source heat, salt flow and branch duties join explicitly, including the per-circuit versus installed-pump distinction.

The retained old fit argument continues feeding the old equipment diagnostic, avoiding a dependency back-edge. Raw legacy fit-domain/interface failures stay observable with explicit applicability. Actual matched admission and cooling checks must execute and enter current reporting; inactive historical checks cannot be rewritten true. Eager upstream legacy execution remains a documented limitation and must be tested on production inputs.

Gross conversion retains its meaning for power balance and CAS23/24/26. Steam and cooling-water pumps enter recirculation once; CAS25 keeps total thermal input as its price driver. The full 3% allowance plus explicit pumps remains conditional. Zero/half/full overlap calculations are labeled hypotheses, not estimated uncertainty. The selected cooling-water reference remains site-unqualified, and its rejection is cycle-only. Raw adverse approaches may remain calculable diagnostics but cannot be reported as physically admissible heat rejection. Required UA remains distinct from installed capacity/cost.

Held efficiency must disable both new modules atomically, retain historical auxiliary meaning and mark unavailable state/pump predictions accordingly. The plan requires a separate independent oracle, every new primitive/status/binding, canonical/staged identity, stock regeneration, negative cases, affected regression, fresh depth review and native integration. These requirements are adequate; their execution remains pending.

## Evidence

I inspected probe source, generated dependency pipeline, entry points and execution receipts, then replayed the execution probe independently in `/tmp`. Disabled mode made zero property calls; active output and invalid-mode/property refusals matched. This proves the bounded toy route, not production integration. The first replay lacked the documented TEAx import path; the corrected replay passed without changing original artifacts.

Exact reviewed identities and replay receipt: [design-review-receipt.json](cycle-physical-receipts/design-review-receipt.json) and [design-probe-replay.json](cycle-physical-receipts/design-probe-replay.json). Final owner adoption remains a separate gate.
