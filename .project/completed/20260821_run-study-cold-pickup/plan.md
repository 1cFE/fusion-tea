# Implementation Plan: Cold-Pickup Administrator Exercise

**Status:** Complete — approved by owner 2026-08-20
**Created:** 2026-08-20
**Last Updated:** 2026-08-20

## Source Documents
- **Spec:** `.project/active/run-study-cold-pickup/spec.md`
- **Design:** none — skipped (`[OWNER]` 2026-08-20: nothing here has competing mechanisms; the one mechanism that matters, reader isolation, is Phase 1 of this plan)
- **Contract under test:** `.claude/skills/run-study/SKILL.md`, `runbook.md § Administer`, `record-template.md`
- **Prior fill, for Phase 3 only:** `.project/active/run-study-contract/dry-run.md`

## The Point

The run-study design claims the committed record is the only handoff between the agent who ran a study and the agent who writes it up; if the write-up needs a fact the record doesn't carry, the record contract is defective. Nobody has tested that with a reader. This item has a fresh reader attempt the write-up from the proof-of-life directory alone, then asks one question of each fact the reader couldn't find: does the template already require it (old study predates it, no action) or not (a contract gap, fix the template before Item 6 spends a real run)? `gaps.md` is that one-time check and nothing more. Model findings the old study recorded are reported in the synthesis with their cites and not acted on here.

## Implementation Strategy

**Phasing rationale.** The exercise is only worth anything if the reader is genuinely cold, so isolation comes first and is checked mechanically before any read happens. The read is one subagent call. Everything after is the Item 5 session's own work: separate reader misses from real absences, classify, edit, commit.

**Critical path.** Scratch copy → brief → reader → synthesis → comparison → `gaps.md` → template edits → commit.

**First proof point.** A scratch directory that contains exactly the git-tracked files of the study directory and nothing else, and a brief that names no fact about the study.

**Validation approach.** No code is written, so "tests" are shell checks: set equality on the scratch copy, grep on the brief, grep on the synthesis's citations, a section-presence check on the synthesis. Each phase has its checks listed.

---

## Phase 1: Isolate the evidence and write the brief

### Goal
Make it physically impossible for the reader to see `_work/`, `dry-run.md`, `demo-proof-of-life/plan.md`, or anything else outside the committed record, and write a brief that tells the reader nothing about the study.

### Assumption Under Test
The tracked contents of `exploration/stellarator_e2e/study/` are a complete, self-contained evidence surface that can be copied out and read in place without anything else in the repo.

### Check Stencil (run before Phase 2)
```bash
SCRATCH=/tmp/claude-1000/-home-reid-1cfe-fusion-tea-stellarator-mbse-demo/78142d13-cf26-498f-afd5-1ff93cebc6a8/scratchpad/cold-pickup/study
# 1. tracked set == scratch set, nothing extra
diff <(git ls-files exploration/stellarator_e2e/study | sed 's#^exploration/stellarator_e2e/study/##' | sort) \
     <(cd "$SCRATCH" && find . -type f | sed 's#^\./##' | sort) && echo "SET OK"
# 2. no _work, no pycache
! find "$SCRATCH" -name '_work' -o -name '__pycache__' | grep . && echo "CLEAN OK"
# 3. brief names no study fact
! grep -iE 'wall.?load|availability|LCOE|275\.|209\.|R, ?a|major radius|CAS7|glue|era pin|fa0e06a' brief.md && echo "BRIEF OK"
```

### Changes Required
- [x] Create the scratch directory and copy exactly the files `git ls-files exploration/stellarator_e2e/study` lists (`.gitignore` included; it is tracked and harmless).
- [x] Write `.project/active/run-study-cold-pickup/brief.md`, the reader's full instruction. It carries only:
  - the absolute scratch path, and the absolute path to `.claude/skills/run-study/`;
  - "invoke the run-study skill in **administer** mode on this directory";
  - the waiver: this directory predates the record contract and has no `record.md`; the skill's "confirm it is a record directory" rule is waived for this read; proceed and report missing structure as missing (`runbook.md § Administer`, step 4);
  - the synthesis shape by reference to `runbook.md § synthesis.md` (header stamps administrator, date, and the `snapshot.json` digest read — state nil if none);
  - the prohibition: read nothing outside the scratch directory and the skill directory; cite only paths inside the scratch directory; where a fact is not in the directory, write that it is not recorded, do not infer it;
  - output: write `synthesis.md` into the scratch directory, nothing else.
- [x] The brief contains no statement about what the study swept, found, or assumed. Check 3 above enforces the obvious words; read it once more by eye.

### Validation
- [x] Checks 1–3 print OK.
- [x] `brief.md` read once by eye for any study fact the grep would not catch.

**What we know works after this phase:** the reader can be handed a path and a skill and nothing else.

---

## Phase 2: Run the reader

### Goal
Produce `synthesis.md` from a context with no execution memory.

### Assumption Under Test
A cold reader, given the directory and the skill, produces a write-up with the four fresh-administrator facts attempted and a non-empty "What the record does not support" section, rather than refusing or producing an account of nothing.

### Check Stencil (run on the output)
```bash
SYN="$SCRATCH/synthesis.md"
# required sections present (runbook § synthesis.md)
for h in "set out to do" "found" "framing" "constraint" "findings" "does not support"; do
  grep -qi "$h" "$SYN" || echo "MISSING SECTION: $h"; done
# flag repo or excluded-path mentions for review
grep -nE '\.project/|exploration/|plan\.md|dry-run\.md|_work/|manifest\.json|ANNEX' "$SYN" || true
# flag named files absent from the scratch directory for review
grep -oE '`[A-Za-z_./-]+\.(csv|json|py|html)`' "$SYN" | tr -d '`' | sort -u | while read f; do
  [ -e "$SCRATCH/$(basename $f)" ] || echo "ABSENT FILE MENTION: $f"; done
# Review every hit in context. It passes when the mention reports an exclusion or
# absence rather than using an outside or absent file as evidence for a claim.
```

### Changes Required
- [x] Spawn one **fresh** subagent (`subagent_type: general-purpose`, never `fork` — a fork inherits this session's context, which is exactly the contamination the exercise exists to exclude). Its prompt is the contents of `brief.md`, verbatim, and nothing else.
- [x] Do not answer questions from the reader with study facts. If it asks something the brief should have covered, amend the brief, note the amendment in Phase 2's completion notes, and re-run from a clean scratch copy.
- [x] Do not edit `synthesis.md`. If the checks fail on form (a missing section), re-run with the brief amended; if they fail on a citation outside the directory, the read is contaminated and is re-run.

### Validation
- [x] All section checks pass; every flagged path or absent-file mention was reviewed in context; each reports an exclusion or absence, and no claim uses an outside or absent file as evidence.
- [x] "What the record does not support" is non-empty (it will be — the directory predates the contract).
- [x] Spot-read: no sentence states a fact the directory does not carry (the quickest tells: a qualified constraint id, an owner quote, a teax commit, a window rationale — none of these exist in the tracked files).

**What we know works after this phase:** a cold read exists and its citations are clean.

---

## Phase 3: Separate reader misses from real absences

### Goal
Make sure every absence the synthesis claims is a real absence from the committed directory, not something the reader overlooked.

### Assumption Under Test
`dry-run.md`'s entries split cleanly into "sourced from inside the directory" and "sourced from `plan.md`"; the first set is the oracle for reader misses.

### Check Stencil
```
# table built by hand, one row per dry-run.md entry:
# section | dry-run verdict | dry-run source file | inside directory? | synthesis recovered it?
# A row with inside=yes and recovered=no  -> READER MISS (not a gap; note it)
# A row with inside=no  and recovered=no  -> real absence, goes to Phase 4
# A row with inside=yes and recovered=yes -> fine
```

### Changes Required
- [x] Read `dry-run.md` now (first time this item opens it). For each of its seventeen section verdicts, note whether the cited source is inside the directory (`run_design_search.py`, `make_report.py`, the CSVs, `verification_summary.json`, `report.html`) or outside (`plan.md`).
- [x] Cross each inside-sourced fact against the synthesis. Record reader misses in `gaps.md § Reader misses` — they are evidence about the reader, not the contract, and they do not become gaps.
- [x] Record any fact the synthesis recovered that `dry-run.md` marked NO SOURCE — it means the directory carried more than the fill found; note it.

### Validation
- [x] The table covers all seventeen sections.
- [x] Every absence carried into Phase 4 has `inside = no`.

**What we know works after this phase:** the absence list going into classification is clean of reader error.

---

## Phase 4: Write `gaps.md`

### Goal
Sort every real absence into one of the epic's three buckets and give each gap a disposition.

### Assumption Under Test
The template's seventeen headings plus the runbook's administer steps already require nearly everything the reader needed; the gap bucket is short, possibly empty.

### Check Stencil
```
# gaps.md shape:
# § Absences — table: required fact | where the reader looked | bucket (template | runbook | limitation)
# § Gaps — one entry per template/runbook row: the fact, why the write-up needed it,
#          load-bearing? (would Item 6's administrator lose framing / LCOE / constraint outcomes / findings?),
#          disposition: `applied: <edit>` | `not applied: <reason>`
# § Reader misses — from Phase 3
# § Zero-gap statement — present iff § Gaps is empty
```

### Changes Required
- [x] Write `.project/active/run-study-cold-pickup/gaps.md` in that shape. The test for "limitation": the template or runbook already requires the fact (cite the section or step). The test for "gap": the write-up needed it and nothing in the contract requires it.
- [x] Include the known friction as a row: `SKILL.md` tells an administrator to refuse a non-record directory while the design expects administer mode on pre-capability directories. Classify it honestly (it is a skill-text question, not a template one) and give it a disposition.
- [x] Include the two-studies-in-one-directory observation only if the reader tripped on it; otherwise it is already recorded in `dry-run.md` and needs no second home.
- [x] Keep it short. A limitation is one line. A long gap list means limitations were counted as gaps; re-check against the template before moving on.

### Validation
- [x] Every absence from Phase 3 has exactly one bucket.
- [x] Every gap has a load-bearing verdict and a disposition.
- [x] No row routes a model finding anywhere (spec Non-Goals).

**What we know works after this phase:** the set of edits to make, if any, is decided and justified.

---

## Phase 5: Apply, place, commit

### Goal
Land the load-bearing edits, put the synthesis where it belongs, close the item's checklist.

### Assumption Under Test
Each applied gap is one small local edit to `record-template.md` or `runbook.md` that does not change the seventeen-heading structure or any Item 3 field name.

### Check Stencil
```bash
# template invariants survive the edits
grep -cE '^## [0-9]+\. ' .claude/skills/run-study/record-template.md   # expect 17
! grep -n '<[^>]*<' .claude/skills/run-study/record-template.md && echo "NO NESTED TOKENS"
uv run python -m pytest tests/study -q                               # still green, untouched
git status --porcelain exploration/stellarator_e2e/study/            # only synthesis.md added
```

### Changes Required
- [x] For each `applied` gap: one edit, one commit, message citing `gaps.md` and the gap's row. No edit to a section's heading text; no rename of an `(Item 3)` field.
- [x] Copy `synthesis.md` from the scratch directory to `exploration/stellarator_e2e/study/synthesis.md`, unmodified. Nothing else in that directory changes.
- [x] Commit `spec.md`, `plan.md`, `brief.md`, `gaps.md`, `product-lens.md`, and the synthesis.
- [x] Tick Item 5's four success-criteria boxes in `.project/backlog/epic_run_study_capability.md` with a one-line evidence note each; update the epic's Status and Next Action lines; update `.project/CURRENT_WORK.md`.

### Validation
- [x] Heading count 17; no nested tokens; `tests/study` green; study directory shows only `synthesis.md` added.
- [x] `git log` shows one commit per applied gap.
- [x] Epic Item 5 boxes ticked with evidence; criteria 1–4 of the epic still marked as landing with Item 6.

**What we know works after this phase:** Item 6 starts against a template that has survived one cold reader.

---

## Risk Management

- **Contaminated read.** The reader sees something outside the directory (repo paths are reachable even from the scratch dir). Mitigation: physical scratch copy, explicit prohibition in the brief, citation grep in Phase 2, re-run on any outside citation. Residual: a reader could read and not cite; the Phase 2 spot-read for facts the directory cannot carry is the backstop.
- **Limitations counted as gaps.** The failure mode that produces a long, unread `gaps.md`. Mitigation: the bucket test in Phase 4 cites the template section or runbook step that already requires the fact; the zero-gap outcome is stated as legitimate.
- **Over-editing the template.** A gap fix that reshapes a section or renames an Item 3 field. Mitigation: Phase 5 invariants (17 headings, no nested tokens, field names untouched), one commit per edit.
- **Reader refuses the directory.** `SKILL.md`'s non-record rule. Mitigation: the waiver in the brief; the friction itself is filed in `gaps.md`.

## Revisit — verification as a mandatory study step

**`[OWNER]` 2026-08-20, during the Phase 5 pause and confirmed during the audit walkthrough.** The oracle (`verify_stellaris.py`, the hand-written second implementation the study is checked against) is a development-process mechanism for the generated package, not part of what a "study" is in general. For fusion-tea it may always be available; the general run-study capability should not assume every package has one. Runbook step 10 currently makes verification a gate that fails closed when no oracle exists, and the manifest requires an oracle command. **Revisit this decision altogether** — whether verification is a mandatory study obligation, a package-conditional step, or a dev-time check outside the study contract. G1's existing field is provisional; its exact shape is not refined in Item 5 and follows the future decision about the oracle's role.

## Implementation Notes

*(filled during implementation)*

### Phase 1 Completion
**Completed:** 2026-08-20 06:42
**Changes made:** scratch copy at `<scratchpad>/cold-pickup/study/` built from `git ls-files` (7 files incl. `.gitignore`); `brief.md` written.
**Checks:** SET OK, CLEAN OK. Check 3 hit once on the repo's own name in the skill path (`fusion-tea-stellarator-mbse-demo`) — domain name, not a study fact, and visible in the CSV key names regardless; accepted. Brief read by eye: no study fact.
**Deviations:** none.
### Phase 2 Completion
**Completed:** 2026-08-20 06:50
**Changes made:** one fresh `general-purpose` subagent, prompt = `brief.md` verbatim; `synthesis.md` (141 lines, 20 "does not support" entries) written into the scratch copy. Not edited.
**Checks:** all six sections present. Citation grep hit twice on `_work/` — both are the reader citing the directory's own `.gitignore`, not an outside read. Three "cited but absent" files are `snapshot.json`, `indicators.json`, and the oracle script, each named by the reader as *missing* — the intended behavior. Spot-read: no qualified constraint id, owner quote, or window story beyond what the report states; clean.
**Deviations:** none. The reader did not ask questions.
### Phase 3 Completion
**Completed:** 2026-08-20 06:58
**Changes made:** the 17-section comparison table is preserved in `gaps.md § Cross-check`, completed during the audit walkthrough from `dry-run.md`, the unchanged synthesis, and the tracked study-directory files. Mixed inside/outside rows stay mixed rather than being forced into a false binary. The cold reader was not rerun.
**Result:** three reader misses (qualified objective channel name; declined-axis row half-recovered; two prose bounds overclaimed as absent), none hiding a gap. No absence carried to Phase 4 has `inside = yes`.
**Deviations:** none.
### Phase 4 Completion
**Completed:** 2026-08-20 07:05
**Changes made:** `gaps.md` written. 20 reader entries → 18 limitations, 1 not-an-absence (mechanism claim in prose), 1 gap (G1: oracle source digest not snapshotted). Plus G2 (SKILL.md pre-capability allowance) from the known friction. Neither gap is load-bearing.
**Checked against Item 4 schemas:** `verification_summary.v1` already carries sampled case ids, oracle module/callable, and the verifier's source digest; `preflight_results.v1` records gate observations and document digests — so reader entries 9, 11 (partly), and 12 are covered. The oracle's own source digest is the one thing no schema or snapshot field holds.
**Deviations:** none. Paused here for the owner per instruction before Phase 5.
### Phase 5 Completion
**Completed:** 2026-08-20 07:20
**Changes made:** G1 applied to `record-template.md` (`316fc3a0`); `synthesis.md` copied byte-identical into `exploration/stellarator_e2e/study/` and committed with the item artifacts (`5ec1dbe1`); epic Item 5 boxes ticked with evidence; CURRENT_WORK updated.
**Checks:** 17 headings; no nested tokens; `tests/study` 273 green (the one transient failure was the git-clean gate seeing the not-yet-committed `synthesis.md`; green after commit); study dir shows only `synthesis.md` added.
**Deviations:** G1 applied although not load-bearing — owner decision at the pause, with the § Revisit note recorded above.

---

**Status**: Complete — approved by owner 2026-08-20 (`audit.md`)
