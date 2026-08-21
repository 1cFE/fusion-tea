# Spec: Cold-Pickup Administrator Exercise

**Status:** Needs Work — audit 2026-08-20
**Owner:** Reid W
**Created:** 2026-08-20
**Complexity:** LOW
**Branch:** feat/stellarator-mbse-demo
**Epic:** RUN-STUDY, Item 5

---

## Problem

The run-study design rests on one claim: the committed record is the only thing that passes from the agent who ran a study to the agent who writes it up, so if the write-up needs anything the record does not carry, the record contract is defective (`run-study-skill-design.md`, "The record is the seam between roles"; `[OWNER-VERBATIM]` in the concept: "sufficient structure in the artifacts from the executing study agent ... so that another agent can effectively pick up the results and do the synthesis").

Nobody has tested that claim with a reader. Item 2 wrote the contract (`record-template.md`, 17 sections; `runbook.md § Administer`) and filled it once against the proof-of-life (`run-study-contract/dry-run.md`), but that fill was done by the template's own author, and it drew on `.project/active/demo-proof-of-life/plan.md`, which lives outside the study directory. It shows the template can be filled. It does not show that a reader with nothing but a study directory can do the administrator's job.

Item 6 will test the contract for real on a new record, but by then a real study run has been spent, and any gap found there costs a re-run or an addendum. The proof-of-life directory (`exploration/stellarator_e2e/study/`) is the one finished study we have, so it is the cheapest place to rehearse the read before the first real consumer.

What the exercise is testing is the **contract**, not the old study. The old study predates the contract and is expected to be missing most of the template. What matters is whether, in doing the write-up, the reader needs a fact the template never asked for.

**Two things get called "gap" and only one is this item's.** A *contract gap* is a fact the write-up needed that the template does not require. `gaps.md` is the one-time list of those, and its only use is to decide which edits the template or runbook get before Item 6. Once the edits land it is finished evidence in this directory; it is not a log and nothing downstream reads it (`[OWNER]` 2026-08-20: no discovery log for this). A *model gap* is something a study finds out about the model — the kind of finding `DISCOVERY_LOG.md` indexes when a study is executed. This item is not a study. It reports whatever findings the old study's own files carry, because recovering findings is part of the administrator's read, and it does nothing else with them.

## Success Criteria

- [ ] **A directory-only synthesis exists.** `exploration/stellarator_e2e/study/synthesis.md`, written by a context with no memory of the execution session, citing only files inside that directory. It states what the study set out to do, the LCOE result, each constraint's outcome, the framing verdict per axis, and the findings, each with the file it came from.
- [x] **Recorded facts, missing facts, and administrator interpretations are kept apart.** The synthesis's "What the record does not support" section lists every required fact the reader could not find in the directory. An administrator may state an evidence-backed interpretation when it is clearly labeled as the administrator's reading and cites the supporting record evidence. That interpretation must not be attributed to the executor or used to claim that a missing historical fact was recorded.
- [x] **`gaps.md` sorts every absence into one of three buckets** (record template, runbook, or stated pre-capability limitation), per the epic. An entry in the first two buckets is a contract gap: a fact the write-up needed that the contract does not require. An entry in the third is a limitation: a fact the contract already requires and the old study simply predates — one line, no action.
- [x] **Every gap carries a disposition, and every load-bearing gap is applied before Item 6 starts.** A load-bearing gap is applied as one edit to `record-template.md` or `runbook.md`, recorded once in `gaps.md` with the edit it produced. A gap is load-bearing when its absence from a new record would leave Item 6's administrator unable to recover one of the four fresh-administrator facts (framing per axis, LCOE, named constraint outcomes, evidence-backed findings). A gap that is real but not load-bearing does not need to be applied. If it is applied by explicit owner decision, `gaps.md` records the edit, reason, and authority; otherwise it records `not applied: <reason>`. **[OWNER] 2026-08-20, audit walkthrough:** optional application is allowed when recorded this way.
- [x] **A zero-gap result is reported as such.** If every absence is a limitation, `gaps.md` says so in a paragraph and the template is left alone. A long gap list is a signal that limitations were counted as gaps, not a sign of thoroughness.

## Known Requirements

- **[NEED]** The administrator uses no study evidence outside the record directory — not the package, not the manifest, not the discovery log, not this repository's work items. Owner-originated: concept Success Criterion 4, "given only the committed study record ... without consulting the executing session" (`run-study-skill.md`), carried into `runbook.md § Administer` step 1. For this exercise that includes `run-study-contract/dry-run.md` and `demo-proof-of-life/plan.md`, both of which describe the study from outside it. **[OWNER] 2026-08-20, audit walkthrough:** tool-generated cache or spill files containing an already-read record file are transport for the same evidence, not an outside evidence source.
- **[INFERRED]** The evidence surface is the **git-tracked** contents of `exploration/stellarator_e2e/study/`: the two CSVs, `verification_summary.json`, `report.html`, `run_design_search.py`, `make_report.py`. The gitignored `_work/` directory (sqlite stores and staged artifacts, regenerated locally on 2026-08-20 by Item 4's equivalence run) is not part of the committed record and is not read. The design's claim is about the *committed* record; a fresh clone would not have `_work/`. (Flagged: the stores hold the qualified constraint ids the CSVs dropped, so this choice decides whether that fact counts as recoverable. Recommendation is tracked-only.)
- **[INHERITED: runbook § synthesis.md]** The synthesis follows the runbook's synthesis shape: header stamping the administrator, the date, and the `snapshot.json` digest read (nil here, stated); sections for what the study set out to do, what it found, the framing verdict per axis, the constraint structure, findings carried forward, and the mandatory "What the record does not support".
- **[INHERITED: SKILL.md, Administrator role]** A missing fact is reported as missing, never recovered from elsewhere. A fact the administrator cannot recover is a defect in the record contract, not in the synthesis (`runbook.md § synthesis.md`, last sentence).
- **[OWNER] 2026-08-20, audit walkthrough.** Evidence-backed interpretation is part of synthesis. It is allowed when clearly labeled as the administrator's judgment and supported by in-directory evidence. Missing executor intent remains missing and must not be reconstructed or attributed to the executor.
- **[INHERITED: epic Item 5]** The legacy directory is the evidence surface only. Old CSVs, the report, the verification summary, and the scripts are not edited; no new study points run; the directory is not treated as capability-compliant or as the epic's final cold-pickup proof (that is Item 6's job on a new record).
- **[INFERRED]** Every absence claimed in `gaps.md` is verified to be a real absence from the committed directory, not a reader miss. (The natural check is a post-read comparison against `dry-run.md`, restricted to the entries `dry-run.md` sourced from inside the directory. How that comparison is run is design.)
- **[INFERRED]** The proof-of-life holds two studies in one directory — the (R, a) grid and the availability sweep — which the contract would treat as two records (`dry-run.md`, "One structural observation"). One synthesis covers both; each axis gets its own framing verdict and account.
- **[NEED]** The synthesis reports the findings the old study's committed files carry (e.g. the report's caveats), each with its file cite, because recovering findings is one of the four facts the administrator owes. Item 5 does not route, file, or log them, and does not create or write `DISCOVERY_LOG.md` (`[OWNER]` 2026-08-20; the log is Item 6's deliverable and the runbook bars the administrator from it).

## Non-Goals

- Retrofitting a `record.md`, `snapshot.json`, or `indicators.json` onto the proof-of-life. The directory stays pre-capability.
- Running the indicator tool, preflight, or verification against the legacy study to fill in what it did not record.
- Amending the policy. Policy-bound lessons are recorded and left for Item 6's Align.
- Building a record linter. `run-study-contract/design.md` names `record_lint.py` as the home if drift shows up; this item does not create it.
- Acting on model findings the synthesis reports — routing them to modeling or research items, or indexing them in a discovery log. The synthesis states them with their cites; that is where this item stops.
- Softening the template because the old study cannot fill it. A section no compliant study could fill would be a defect; a section the old study predates is not (`dry-run.md`, "A gap here is not a reason to soften the contract").

## Open Questions / Deferred to design

- **How the fresh context is produced.** A subagent spawned with a brief naming only the directory path and the skill, or a separate session. Design decides; the requirement is only that the reader has no execution memory and no access to the excluded files.
- **The skill's "confirm it is a record directory" rule.** `SKILL.md` tells an administrator to refuse a directory that is not a record. The design explicitly expects administer mode to run on the pre-capability directory and report missing structure. The brief has to carry that allowance for this exercise. Whether `SKILL.md` itself gains a one-line allowance for pre-capability directories is an output of the exercise, filed in `gaps.md` like any other.
- **Order of reading within the directory.** Whether the administrator is told to read `report.html` first, or the scripts, or nothing. Probably nothing: the order a cold reader picks is itself evidence about the record.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_run_study_capability.md` — Item 5
- **Required Reading:**
  - `.project/concepts/run-study-skill.md` — cold-pickup owner statements
  - `.project/concepts/run-study-skill-design.md` — record and administer mode
  - `.claude/skills/run-study/SKILL.md`, `runbook.md`, `record-template.md` — the Item 2 contract under test
  - `exploration/stellarator_e2e/study/` — the administrator's evidence surface, and nothing else for the administrator
- **Prior fill:** `.project/active/run-study-contract/dry-run.md` — Item 2's section-by-section fill of the template against the proof-of-life (used only for the post-read comparison, never by the administrator)
- **Product-lens:** `.project/active/run-study-cold-pickup/product-lens.md`
- **Design:** none — skipped by owner 2026-08-20; the isolation mechanism is in `plan.md` Phase 1

---

**Next Steps:** Resolve the findings in `audit.md`, then rerun `/_my_audit`.
