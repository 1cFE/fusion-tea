# Freshness record — every run there was

**Status:** skeleton, opened 2026-08-27 at Phase 0. Rows are appended as runs happen; the closing statement is written at Phase 12.

**The enumeration rule, in force from Phase 1 to the end.** *Every* run — kept, aborted, discarded, crashed — gets a `sessions/NN-<role>/` directory with whatever it produced and a row here. There is no such thing as a run that did not happen.

Nothing about an owner gate is mirrored here. Where this record needs to point at a park, it cites the `trail.md` entry **by heading and date** (R-F5).

## Runs

| Run | Role | Session | Brief | Transcript | Session id | Kept / discarded | Reason |
|---|---|---|---|---|---|---|---|
| 01 | Grounding turn 1 | new | `sessions/01-grounding/brief.md` | `sessions/01-grounding/transcript.jsonl` | `b56a1223-b046-4341-a0f3-366c4598286d` | kept | Completed successfully (exit 0, 26 turns, 25 tool calls). Wrote `goal.md` to `draft` and put five numbered questions to the owner. Fence sweep CLEAN |
| 02 | Grounding turn 2 | resume of 01 | `sessions/02-grounding/brief.md` | `sessions/02-grounding/transcript.jsonl` | `b56a1223-b046-4341-a0f3-366c4598286d` | kept | Completed (exit 0). goal.md → `Status: grounded` (C-GROUND `b8a791ce`). Owner charter verbatim. Fence sweep pending Phase 13 |
| 03 | Round agent, T-001 | new | `sessions/03-round-agent/brief.md` | `sessions/03-round-agent/transcript.jsonl` | `a94a3ddd-5202-4988-90b7-20b64bee85cb` | kept | Completed (exit 0, 57 turns). T-001 `COMPLETE` (C-T001 `71d2abe8`), proposed dispositions, handoff stop. Fence sweep pending Phase 13 |

| 04 | Checkpoint critic r1 | new | `sessions/04-checkpoint/brief.md` | `sessions/04-checkpoint/transcript.jsonl` | see meta.md | kept | Verdict: does not pass — three required changes; re-derived all arithmetic; C-001.r1 in trail |
| 05 | Round agent r2 revision | resume of 03 | `sessions/05-round-agent-r2/brief.md` | `sessions/05-round-agent-r2/transcript.jsonl` | `a94a3ddd-5202-4988-90b7-20b64bee85cb` | kept | Revised return+dispositions r2; disputes critic ACT1/ACT2 assignment; handoff to C-001.r2 |
| 04b | Checkpoint critic r2 | new | `sessions/04b-checkpoint-r2/brief.md` | `sessions/04b-checkpoint-r2/transcript.jsonl` | see meta.md | kept | Verdict: PASSES — all RC applied; ACT dispute adjudicated for the revision; three carry-forwards to round result/review |
| 07 | Round agent close | resume of 03 | `sessions/07-round-agent-close/brief.md` | `sessions/07-round-agent-close/transcript.jsonl` | `a94a3ddd-5202-4988-90b7-20b64bee85cb` | kept | Joined rows #3/#5 landed; Round 1 result trigger 6; owner recommendation 3 rulings; handoff to review |
| 08 | Round reviewer | new | `sessions/08-reviewer/brief.md` | `sessions/08-reviewer/transcript.jsonl` | see meta.md | kept | Verdict FINDINGS (citation line, Ruling-3 tension); counter-reading rejected with one point kept; learnings appended in this commit |
| 05a | Round agent T-002 (seam) | — never run | `sessions/05a-round-agent-t002/brief.draft.md` | — none | — | drafted, never used | Drafted at Phase 0 per design de-risk; T-001 returned COMPLETE so the research seam was never invoked. Committed post-window as a record |

## Closing statement

These twelve session entries — 01, 02, 03, 04, 04b, 05 (r2 revision), 07, 08 kept; 05a drafted and never run; no session aborted, discarded, or crashed — are all the runs there were. Session numbering follows the design's table; 06 (gate-b turn) never existed because the advance path never opened. No other input existed: no context injection, no prior turn beyond the recorded resume turns (02 resumed 01; 05 and 07 resumed 03), and no verbal hint from the operator — every operator input is a committed brief, listed above, delivered on stdin. The transcripts were teed in-repo per the authorized deviation recorded in operator-notes.md; each is committed beside its brief.
