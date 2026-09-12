# Independent numerical review evidence

Reviewer: fresh agent `/root/mfe_financial_item/review`. Candidate: `design.md@239ca68e` and its committed prototype, against `spec.md@050054bd`. This evidence assesses the design; it does not certify production implementation.

Executed from `/tmp/fusion-mfe-financial-rate-limits` after inspecting `.codex-test/run`: `.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/stage-provenance/review_numerics.py`.

The retained probe passed 768 checks against independent 100-digit Decimal references constructed from the actual binary64 operands. Maximum relative errors were IDC `1.1054751446211056e-14`, CRF `2.461878639523745e-16`, periodic PV `4.3657868165225395e-15`, and annuity PV `1.9222914830872668e-15`. True-zero expectations use absolute error. The probe covers subannual and fractional durations, both binary64 neighbors of one, tiny signed rates, neighboring unequal represented rates, the positive numerical switch and its neighbors, and negative near-switch cases. The candidate's own separate probe covers the full specified signed switch grid.

An initial reviewer reference evaluated the generic IDC expression at exactly T=1 and produced a Decimal rounding residue around `3e-83`; relative comparison to that residue falsely rejected the candidate's exact zero. The retained reference uses the exact T=1 identity. This was a reference defect, not a candidate failure.

Source inspection confirmed that the calendar candidate changes only financial evaluation and package imports. Held clipping, the inner wall-load floor, count computation, the live event walk, strict restart condition, downtime, and energy-bin overlap/accumulation remain unchanged. The actual emitted annuity wrapper unpacks `(levelized, crf)` and the candidate manual body returns that order.

An additional reviewer command imported the actual prototype public modules through the existing local `prototype/link/wi052_probe` alias and the sealed runtime. Independent 90-digit references passed for both annuity output fields at `i=g=0.02, N=30, T=8, annual_cost=1e6`, tiny nonzero IDC cost at `i=1e-18, T=8.5, overnight_cost=1e9`, and the original zero-discount DCF referent. The command returned `PASS independent public annuity tuple fields, tiny nonzero IDC cost, zero-rate DCF`. No package loader, regeneration helper, or artifact writer was called.

The reviewer read `prototype/build.py`, `execute.py`, `generation.txt`, `execution.txt`, and `l2-differential.json`. Those author-produced records support native generation/manual preservation, public-module counterexamples, 72 calendar cases, and ten identical L2 warnings. The reviewer did not rerun generation or full native execution. Complete event-boundary tests, independent dated-energy-ratio checks, full baseline channel attribution, and the L6 issue-identity differential remain implementation work as the design explicitly states.

No production files, source registries, studies, pins, or external checkouts were changed. No quarantined material was read or hashed. This review adds only its native-item evidence.
