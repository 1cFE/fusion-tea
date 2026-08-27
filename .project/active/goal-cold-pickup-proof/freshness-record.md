# Freshness record — every run there was

One row per run — kept, aborted, discarded, or crashed. Closed by a completeness statement,
not a count. Phase 0's de-risk checks are mechanism evidence, not cold runs, and are recorded
in `operator-notes.md` instead (they exercised no goal artifact and played no role).

| NN | Role | Session id | Brief (committed first) | Transcript | Kept? | Note |
|---|---|---|---|---|---|---|
| 01 | grounding turn 1 | 8fce7649-b573-4b1d-8a23-1a708ebe74b2 | sessions/01-grounding/brief.md | sessions/01-grounding/transcript.jsonl | kept | wrote goal.md, asked 6 operator questions |
| 02 | grounding turn 2 (resume of 01) | 8fce7649-b573-4b1d-8a23-1a708ebe74b2 | sessions/02-grounding/brief.md | sessions/02-grounding/transcript.jsonl | kept | goal.md finished, Status: grounded || 03 | gate probe p1 | 9ba9b61c-887b-4efc-a28c-e9a080bb903c | sessions/03-gate-p1/brief.md | sessions/03-gate-p1/transcript.jsonl | kept | verdict in gate-probe-record.md || 04a | gate probe p2, attempt 1 | 20aaccf7-db86-4256-815b-c550b4227548 | sessions/04-gate-p2/brief.md | sessions/04-gate-p2/attempt1-transcript.jsonl | discarded | killed by the orchestrator's own harness timeout on the batch script, not by the session; no output written to the main tree; re-run as 04b || 04b | gate probe p2 | 58675765-2634-4056-99d7-aa701f839e25 | sessions/04-gate-p2/brief.md | sessions/04-gate-p2/transcript.jsonl | kept | verdict in gate-probe-record.md |

## Closing statement

*(written in Phase 9; until then this enumeration is open)*
