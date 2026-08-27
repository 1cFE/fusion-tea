# Staged edits 1–4 — `.claude/skills/run-study/runbook.md`

Four mechanical find-and-replace edits, from `.project/active/goal-harness-contract/plan.md` Phase 5. Written here because this session cannot write under `.claude/`.

**Apply against:** `.claude/skills/run-study/runbook.md` at `f83a9742` (branch `feat/run-study-first-consumer`). Verified unchanged since `ad2fb4ea`.

**Wrap:** this file is hard-wrapped at ~90 columns. Every replacement below is pre-wrapped to match. Do not reflow.

**Do not change the schema table.** `tests/study/test_records.py` reads the `Record` column at index 3 (design I9). The six columns keep their order: `Date | Kind | Record | Finding | Disposition | Home`.

## Disjointness from Item 6 — checked 2026-08-25

Item 6 has landed none of its four pending runbook sentences. The newest commit touching this file is `ad2fb4ea` ("Item 6 Phase 1: ratify and move the study policy; G1 template fix; briefs") — Phase 1, not Phase 4.

| Pending Item 6 sentence | Its home | Touched by these edits? |
|---|---|---|
| study 1 `#10` — oracle operands emitted as a labelled artifact before verification | steps 5 / 7 | No |
| study 1 `#11` — study stores beside the record directory, not inside it | step 5 / study-definition convention | No |
| study 2 `#10` — re-run preflight whenever `axes.json` changes | step 6 | No |
| study 2 `#6` — export `case_id` in `points.csv` | step 9 / study-definition convention | No |

These edits touch **step 14**, the **administrator paragraph**, and **§ `DISCOVERY_LOG.md`**. Disjoint from all four homes. If Item 6 lands any of them before you apply these, apply these *around* the new sentences, never through them.

---

## Edit 1 — step 14, the sole-writer sentence

**Find** (lines 220–221, inside § 14 "Register the findings and append the discovery-log rows"):

```text
same `<study-id>#<n>` id. The executor is the sole writer of the log. This happens
```

**Replace with:**

```text
same `<study-id>#<n>` id. The executor is the sole writer of first-sighting rows. A
goal round may later append a joined disposition row under the same `<study-id>#<n>`
id; it never edits a first-sighting row and never mints a new id
(`work/orchestration/GOAL_RUNBOOK.md`). This happens
```

The find string continues an existing sentence and the trailing `This happens` runs on into `before the record is committed, so § 15 is filled when step 15 freezes it.` on the next line, which is untouched.

## Edit 2 — the administrator prohibition

**Find** (lines 270–271, end of § Administer):

```text
The sequence ends there. An administrator does not append to `DISCOVERY_LOG.md` — a
finding from a synthesis is filed by whoever acts on the synthesis.
```

**Replace with:**

```text
The sequence ends there. An administrator does not append to `DISCOVERY_LOG.md` — a
finding from a synthesis is filed by whoever acts on the synthesis. The goal round's
joined disposition append is not an administrator act — the administrator stays
read-only.
```

The existing sentence is kept whole; the new one is appended after it.

## Edit 3 — § `DISCOVERY_LOG.md` prose, the cardinality rule

**Find** (lines 290–292):

```text
One file per package at `exploration/<pkg>/studies/DISCOVERY_LOG.md`. An append-only
index, newest row last — one row per finding, never a second copy of the finding's
account.
```

**Replace with:**

```text
One file per package at `exploration/<pkg>/studies/DISCOVERY_LOG.md`. An append-only
index, newest row last — one row per finding *sighting*, plus any joined disposition
rows a goal round later appends under the same id — never a second copy of the
finding's account.
```

"Never a second copy of the finding's account" is deliberately untouched. A disposition row carries a disposition, not a restatement of the finding.

## Edit 4 — a sentence under the schema table

**Find** (lines 298–299, the two lines immediately after the schema table):

```text
`<study-id>#<n>` is the id the record's § 15 uses, so log and record join without
ambiguity.
```

**Replace with:**

```text
`<study-id>#<n>` is the id the record's § 15 uses, so log and record join without
ambiguity. A row is either a first sighting, written by the executor at step 14, or a
joined disposition update, written by a goal round. `Disposition` and `Home` carry
that row's own state; for an id with more than one row, the newest row is its current
state — scan for the id rather than stopping at the first row that matches.
```

The table itself and its header row are not touched.

---

## After applying

- `uv run python -m pytest tests/study -q` → expect 232 passed, 43 skipped. In particular `test_findings_join_the_discovery_log` and `test_record_is_closed` must be unaffected.
- `grep -c '^|' exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` → unchanged. These edits add no rows.
- The runbook diff should be exactly three prose edits plus one appended sentence under the table. Nothing else.

**Edits 5 and 6 are not in this file and are not applied.** Edit 5 (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` header) and edit 6 (`CLAUDE.md:73`) are unblocked in my session and land when I resume, together with Phase 5's validation. Until all six are in, the five homes disagree — so the amendment is not finished by applying these four alone.
