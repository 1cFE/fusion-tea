# Route Equivalence — GSTH Item 6 — goal `p-pump-fence` round 1

**Date:** 2026-08-29. **Agent route:** the round 1 run recorded in `work/orchestration/goals/p-pump-fence/trail.md` (round agent session `489425a1`; administrator `885bf5c5`; checkpoint critic `b7049ac1`; reviewer `88437945`). **Hand route:** a fresh session (`ab39378e`) playing a human operator following `work/orchestration/GOAL_RUNBOOK.md` literally, in an isolated worktree detached at `c4c7d723` (removed after this comparison; the hand administrator's synthesis is preserved beside this file as `route_equivalence_hand_synthesis.md` — a recorded deviation from "only this file survives", kept for audit). Its first launch was killed by a harness fault mid-`integrate` and relaunched clean — an environment incident, not route evidence.

## Isolation design (as planned, plan § Phase 6)

Worktree parallel to the repo; every hand-route write inside it; zero commits either tree; main tree verified clean at exit. `integrate` invoked **for real** (ADR-009 makes a re-run return the same identity — the sameness is the point). `study.execute` **fixture-substituted** by the committed record — the declared limit. `study.read` run **for real** by hand.

## The declared limit, plainly

The hand route proves equivalence for grounding, `integrate`, `study.read`, and the checkpoint/review gates. For `study.execute` it proves a hand operator re-derives the same declarations and finds every step-1–6 deposit where the runbook says it lands; it does **not** prove a hand operator would have produced the same 906 points. Steps 7–15 of the study runbook were not walked.

## The five dimensions — verdicts

| Dimension | Verdict | Decisive evidence |
|---|---|---|
| 1. Required artifact set | **same contract** | Hand route produced/located every obligation: independent grounding verdict, seam return JSON, re-derived axis declaration matching `axes.json` before opening it, step-3/4/6 deposits confirmed, independent `synthesis-hand.md` |
| 2. Native end states | **identical** | `integrate` → `CANDIDATE`, exit 0, ten gates pass, pin `20c2c364…`, fingerprints `f08daa7b…`/`f97f0848…` **byte-identical** to the agent route's; tree git-clean after the run; grounding → same `grounded` verdict |
| 3. Gates | **same contract** | Ten seam gates re-run by hand; six preflight gates verified; framing gate's owner rulings found recorded before points ran; checkpoint cap arithmetic (2 of 3) confirmed against `goal.md` § Limits; four distinct session ids across the four roles; append-only verified mechanically (eleven trail commits, zero removed lines) |
| 4. Return classes | **identical** | `CANDIDATE`; reading `ANSWERED` reached independently — and every headline reproduced: 333.0670332813743 baseline, +21.0 %, 370/352/183/1 verdict combinations, 370/906 feasible, best 225.72504 at (20.0, 1.65), 42 excluded (−154.411…−0.899 MW), fence table at all nineteen `a` values |
| 5. Reviewer-visible evidence | **same contract** | Same artifact shapes left for a fresh reviewer, including a synthesis with a mandatory what-the-record-does-not-support section |

Unlooked-for cross-route confirmations: the record's preflight identity digest = the hand seam run's executable fingerprint; `indicators.json`'s digest = the hand run's pin; `sha256sum snapshot.json` = record § 16.

## Divergences (all with stated reasons; none contract-breaking)

1. First hand `integrate` invocation refused at gate 1a `toolchain-drift` — an environment-path artifact of the isolated checkout, not drift (see F-1). Resolved, then identical results.
2. Hand axis derivation from `goal.md` alone reached `R`(+tie) and `a` but not the two declined axes — those come from runbook step 3 plus comparand precedent. A note on what the goal determines vs the study runbook, not a defect.
3. The hand synthesis lists five limits the committed § 17 does not — most substantively that the comparand's 1.0 MW numbers sit outside the record directory, so half the headline comparison is unverifiable at the administrator's declared scope. Difference in reach, not contradiction.

## Findings — operator-kind carve-outs the documents need

- **F-1 (significant): gate 1a maps "different checkout" to `toolchain-drift`, and the operator guide maps that to `STRATEGY_BLOCKER`.** The wheels hashed correctly; the failing assertion was a path (`STOP_PARSER_WHEEL_TARGET` hard-coded to the main tree in `integration.env`), and the guide's mitigation sentence doesn't cover that variable. An operator trusting the guide's table would have **mis-closed the round as a strategy blocker when nothing had moved.** The guide needs a checkout-kind carve-out at that row.
- **F-2: `uv run` cannot be made to honour the sealed environment from a second checkout** (`integrate.py` launches producers via `sys.executable`; `--no-sync` insufficient). The hand operator had to invoke the sealed interpreter directly — the one place the written pattern is not hand-followable, contradicting CLAUDE.md's always-uv rule and the guide's copy-paste invocation.
- **F-3: a record addendum inside the administrator's read scope means no second administrator of this record can be blind** — it cites the first synthesis's findings by number. Process finding against the record contract (step 15), not against this record.
- **F-4: grounding has a stated hollowness tell for one field class of five**; and the runbook doesn't say whether an operator re-derives the `grounded` verdict or reads the assertion. The hand operator re-derived; the runbook should say to.

Routing: F-1–F-4 carry to `epic_evidence.md` as observed failures/carve-outs (hardening-rule evidence, epic SC 7); F-1 and F-2 name `docs/integration_seam_operator_guide.md` and the env contract as their fix homes. None promotes control-plane machinery.

## Conclusion

One runbook, two operators, one contract: **met on all five dimensions, with byte-identical native identity** — and the exercise earned its cost by finding the two places (F-1, F-2) where the written pattern is not yet hand-reproducible from a fresh checkout.
