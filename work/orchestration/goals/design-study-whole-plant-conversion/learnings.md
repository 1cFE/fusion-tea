# Learnings: Whole-plant steam versus helium Brayton conversion

Append only after round review accepts the proposed learning delta.

## Round 1 — numerical diagnostic spacing

[AGENT] Accepted by independent round-1-review.md. For this unchanged cryogenic calculation and its relative-only margin comparison, capacity brackets need predeclared spacing that leaves a numerically resolved margin. This does not permit changing physical inequalities or verification tolerances, deleting failures, or treating the first mismatch as the only one. The complete forensic scan subsequently found an additional cooler precision discrepancy.

## Round 2 — accepted 2026-09-27

[AGENT] Accepted by the coordinator closure check using the independent final review and sealed study a7bd94ed9a9746e1866400f60be5792eab6842d8, snapshot 5db4b78627cadca525c02e29bf98e9c6bad173baf372e25cce9a4bf3effb124e.

- Whole-plant component selection depends on the electrical denominator as well as component purchases. Here steam's higher net electricity outweighs its extra conversion capital at both supported nominal loads. The result is conditional on the declared reactor and finite catalog; the tested combined efficiency/price case can favor Brayton.
- Independently adjudicate a numerical discrepancy before editing either implementation. The high-precision cooler reference supported the existing native answer and identified insufficient oracle root accuracy. Tighter oracle stopping precision passed the unchanged acceptance contract without altering native physics or prices.
- Choose a diagnostic spacing that resolves the capacity margin numerically. Wider cryogenic points preserve the same physical threshold and both passing/failing sides. Preserve the earlier failure; a successful replacement does not retroactively verify it.
- Use separate equipment selections and failed interface checks to explain nonmonotonic catalog minima. Higher source heat alone does not imply higher selected export when the lower-load winning offer becomes inadmissible.

Evidence: [answer](answer.md), [final independent review](evidence/final-results-review-r2.md), [numerical adjudication](evidence/verification-failure-r1/diagnosis.md), [replay comparison](evidence/native-replay-comparison.json).
