# Round 1 review — 2026-09-15

**Verdict: FINDINGS.** The winding-length result and landed dispositions retain their reviewed support. Two errors in the closure account need append-only corrections, and the learning wording needs the corrections below. The comparison premise remains an **OWNER_GATE**. It does not block independent cryogenic source research. The post-record battery is still coordinator-owned and pending; this review does not certify its outcome.

**Reviewer:** fresh non-author session dispatched under `evidence/round1_review_resume_prompt.md`; no inherited author conversation. Owns this file only. No models, studies, trail, discoveries or learnings edited; no study execution, battery, commit or quarantine access. Review follows `GOAL_RUNBOOK.md` sections What “fresh” means, Review scope and evidence reuse, The fresh review, and When a cited artifact moves. The continuation brief supersedes the original broad audit instructions.

## Findings and concrete corrections

1. **F1 — the result erases a measured minimum shift.** `trail.md` Round 1 result, Intent says the interior minimum and fences “do not move.” The passed r2 reading and original `results/a-minima.json@8ad7e913` say the design-column price minimum remains at 2.0 m, while both cheap-column price minima move from 2.2 to 2.1 m. These minima violate predicates; the sole all-eighteen-predicate feasible point on each cheap transect remains at 1.7 m. Append an amendment distinguishing the price minima from the feasible minima. The proposed demo paragraph already bounds its cheapest-point statement to the transects and does not require a numerical correction.
2. **F2 — the trail misstates the first execution's fate.** T-003 return and the result's retry explanation say a turn boundary killed the first matched-window run. Original `execution/execute-attempt-1.log@8ad7e913` reports all 159 rows and exit 0 at 20:57:43. `execution/attempt-2-lease-refused.log@8ad7e913` reports the second launch refused at 20:57:24 because another PID held the lease. Record § 10 explicitly says the executor wrongly inferred the first run had died. Append a correction: the second launch followed that mistaken inference; attempt 1 completed and was superseded to satisfy the shared-store contract. A completed run must not be retold as a killed run.
3. **F3 — learning acceptance needs narrower evidence and meaning.** Adopt the corrected L-001–L-003 below. In particular, predicates exclude the unconstrained price minima; they do not establish where those price minima are located. The defective export and dropped commit were not retained. L-003 must keep their historical status as executor-reported and must not enact the candidate runbook change.

These are record corrections. They require no new scientific run or repeated model audit. The coordinator can check the corrective text against the exact evidence above. The round remains closed.

## Reused evidence and remaining closure coverage

- **WI-058 audit reused:** `work/active/WI-058_coil-winding-length-from-bore/audit.md@a6286a55`, including the final recheck after `aea4025e`. It covers source/form interpretation, the model and twin diff, exact anchor reproduction (177 channels, eighteen verdicts, LCOE 142.50725862880648, circumference 25.0), consumer restatement by identity, integration inputs, and 893 model passes / thirteen skips plus 969 study passes / one skip. Its limits remain: fixed-bore historical replays do not test the shipped off-design winding form; source geometry does not qualify a real coil configuration; uniform-scaling comments remain carried corrections. Audit repairs precede T-002's `1d08fb85` pin.
- **C-001.r2 reused:** `evidence/round1_C-001_checkpoint_r2.md@7d2e1da0` accepts the r2 proposal at `bf0980aa` against original results and the r1 numerical recount. This covers bore scaling, price changes, 1,944 matched verdict comparisons, the two reachable transect predicates, the five feasible transfer cases, cryogenic shares and signed capital changes. I have not represented those reused recounts as new calculations. I opened the original minima and R-invariance artifacts for the closure and learning checks.
- **Revision validity:** git history and diffs show no change after the T-002 pin to models, generated package, WI-058 records, study manifest, census or expected indicator fixtures. No rubric change appears in this interval. Since the study commit, its only changed tracked files are the new synthesis and 29 appended lines in `record.md`; results and snapshot remain unchanged. The r1 proposal is unchanged. Working-tree status showed no modification to these evidence paths. These establish reuse for the reviewed revision; they do not establish the pending battery's result in today's runtime.
- **Disposition landing:** the discovery diff from `8ad7e913` to `7d2e1da0` consists of exactly ten added rows and no removed or edited row. The six new findings and four older IDs match the passed proposal's classes, status, actor and next home. Wall-and-heating #3 remains closed; minor-radius #2 remains a declared seam; both transfer seams remain open; no priced-levers #2 row was added. Finding #1 retains both owner routes, #2 is a reading, and #5 remains a candidate. The future Round 2 heading and unaccepted learning are explicitly prospective homes, not evidence that those actions occurred.
- **Landing notes:** the T-003 reading explicitly limits the no-flip claim to the two reachable predicates; the landed #1 row corrects the control-arm home to the protocol's Arms section; T-003 now supplies the dropped-commit account. The account is disclosed but its assertion that nobody read the dropped commit remains testimony, as the Addendum states.
- **Retry classification:** the study attempts kept the scientific proposals, pin and question. The second launch was a lease refusal; the shared-store rerun and coordinate-export repair corrected execution/publication. They did not select a new scientific strategy or promote another pin. Zero goal-level retries is defensible once F2 is corrected. The masked-red commit and soft reset were a disclosed local history rewrite, not merely a scheduling failure. Their unretained state prevents an independent reconstruction. WI-058 regeneration, consumer repairs and audit recheck remained inside T-001, with no subsequent pin change.
- **Goal scope:** one model increment, one pin and one study satisfy this round's bounded strategy. Reused native evidence supports (a)1 as the adopted, disclosed bore-coupled model form. It does not turn PROCESS into a source for circumference proportional to plasma minor radius. The already-discovered fixed-layer-stack counterexample also corrects the historical uniform-scaling sentence in `goal.md`; cite the audit in the next append-only goal amendment. Items (a)2 and (a)3, the last-pin reading (b), and the owner-accepted final paragraph (c) remain owed unless the owner rules on the explicit alternative outcome.

## Learning delta — corrected and accepted for append

### L-001 — Bore pricing leaves the sampled feasible minor radius unchanged — 2026-09-15

[AGENT] At the winding-length pin, the cheap transects still have exactly one point satisfying all eighteen predicates, at `a = 1.7 m`; their unconstrained price minima move from 2.2 to 2.1 m and violate the burn and loop predicates. The design-column price minimum stays at 2.0 m and violates four predicates. A price minimum and a feasible minimum must therefore be reported separately.

- **Evidence:** study `results/a-minima.json@8ad7e913`; passed C-001.r2 reading at `7d2e1da0`.
- **Scope:** these three transects at pin `2a89b163…`, with their held transport, wall-peak and heating assumptions; before values are entering-pin oracle references. The plant-closure window and the older minor-radius goal's own columns were not rerun.
- **Implication:** later chain changes must report both minima and their predicate sets; this result does not settle the window optimum.
- **Supersedes:** none; corrects proposed L-001 before acceptance.
- **Accepted-by:** this fresh Round 1 review, 2026-09-15.

### L-002 — Historical fixed-bore radius sweeps carry the retired winding dependence — 2026-09-15

[AGENT] The retired major-radius form and the bore form agree only when their normalized bore and major-radius ratios agree. The fixed 1.85 m radial stack prevents fixed aspect ratio alone from ensuring this. At `a = 1.3 m`, the WI-058 replacement changes magnet capital by approximately −$371.0M at `R = 15.7 m` and +$157.0M at `R = 11.43 m`, relative to the entering form.

- **Evidence:** WI-058 audit § 1 and final recheck at `a6286a55`; study `results/R-invariance.json`, `preparation/before-entering-pin-oracle-transects.csv` at `8ad7e913`; signed differences independently recounted in C-001.r2.
- **Scope:** the quoted amounts belong to this entering-to-WI-058 comparison. Earlier fixed-bore radius readings using the retired form between WI-036 and this replacement carry that dependence, with amounts determined by their own pins. The sign of new-minus-old at the design bore is opposite to `R − 12.7`.
- **Implication:** reinterpret an earlier radius sweep using its actual winding basis and pin; do not transplant these dollar corrections or infer fixed-aspect-ratio equivalence.
- **Supersedes:** none; clarifies proposed L-002 before acceptance.
- **Accepted-by:** this fresh Round 1 review, 2026-09-15.

### L-003 — Store verification does not establish an export's joins — 2026-09-15

[AGENT] Checking native store values does not establish that a derived export associated those values with the correct study coordinates. This record's corrected analysis joins by coordinates and compares every exported point with the oracle; the reported earlier label-join defect is not independently reproducible because its export was overwritten.

- **Evidence:** study record § 10 and Addendum items 6–7 at `e44d5e5f`; `execution/analyze.py`, `results/points.csv` and `results/oracle-all-points.json@8ad7e913`; synthesis § 5 finding #5 at `8056ef20`.
- **Scope:** this study's export path; the reported 45 bad joins are executor testimony. The log's runbook-step proposal remains a candidate.
- **Implication:** assess the exported coordinate/value association separately when trusting a derived report. This accepted learning does not edit the runbook or create a universal publication requirement.
- **Supersedes:** none; corrects proposed L-003 before acceptance.
- **Accepted-by:** this fresh Round 1 review, 2026-09-15.

## Recommendation and gates

Open Round 2 with bounded source research for the cryogenic inventory under grounded (a)2. Resolve the 20 K current-lead basis, shield area/load basis, support conduction, the relation to held `p_tfcool`, and the meaning of the remaining uplift. Missing coefficients need named options and source evidence. This research is independent of the open plant-closure comparison ruling and the pending battery, so it can proceed now. Do not execute a new model or study while the coordinator's uncovered validation and applicable gates remain unresolved.

Finding #1 remains owner-held: choose the proposed attribution amendment or the alternative control route before dependent comparison work. It does not veto source acquisition. Demo acceptance, rubric consequences, attached fence repairs, coolant premise, merge/push and native or goal close remain reserved; WI-058 is still active on disk with backlog registry status. Carry the disclosed model/test comment correction into the next relevant regeneration, retain the transfer limitations, and keep quarantined material excluded.

Before recording closure assurance complete, append F1/F2 corrections, append the accepted learning delta, and cite the coordinator's completed post-record test result. If that battery fails on a new scientific or integration issue, broaden review only for that concrete failure. No such outcome is claimed here.

## Corrective-diff recheck — 2026-09-15

**Verdict on corrective text: PASS.** The same fresh reviewer inspected only the working-tree additions to `trail.md` and `learnings.md`; no counts, tests or scientific runs repeated. The appended amendment corrects F1 with both price-minimum shifts and the separate feasible point, and corrects F2 with the original logs' completion/refusal ordering and mistaken death inference. It preserves the evidence limits on the dropped commit and overwritten export. All three learning entries reproduce the accepted corrected wording, satisfying F3. The review entry does not claim the pending battery passed.

The new Round 2 strategy and T-004 scope permit independent source acquisition and cooling-slot interpretation, with model/study execution parked and missing inputs surfaced. This is consistent with the review's recommendation and does not resolve the owner comparison gate. The historical uniform-scaling sentence in `goal.md` still needs its separately carried factual amendment; it is not authority for the research or for a future model form. The battery result and owner-held comparison ruling remain outstanding. No fresh defect in this corrective diff requires another audit.
