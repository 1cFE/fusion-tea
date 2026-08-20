# Gaps — the cold read against the record contract

**Date:** 2026-08-20
**Read:** `synthesis.md` (scratch copy; lands at `exploration/stellarator_e2e/study/synthesis.md` in Phase 5), 20 entries under "What the record does not support"
**Contract:** `.claude/skills/run-study/record-template.md` (17 sections + `snapshot.json` appendix), `runbook.md`, plus the Item 3/4 result schemas under `scripts/study/schemas/` that a compliant `results/` carries

This file is a one-time check of the contract and nothing more. Each absence the reader reported is either a **limitation** (the contract already requires the fact; the old study predates it — cite the section) or a **gap** (the write-up needed it and nothing in the contract requires it). It does not route model findings anywhere; those are in the synthesis § 5 with their cites and stop there.

## § Absences

One row per reader entry (`synthesis.md` § 6 numbering).

| # | Required fact the reader could not find | Bucket | Where the contract already requires it |
|---|---|---|---|
| 1 | Owner intake, verbatim | limitation | template § 2; runbook step 1 |
| 2 | Study id, package, date, executor | limitation | template § 1; snapshot `study_id`, `package.*` |
| 3 | Framing per axis, proposed and judged | limitation | template § 5; runbook steps 4, 11 |
| 4 | Indicator results | limitation | template § 8 + `indicators.json`; runbook step 3 |
| 5 | User rulings on `no_constraint_response` axes | limitation | template § 8; runbook step 4 (fails closed without one) |
| 6 | Pre-execution critique and review outcomes | limitation | template § 14; runbook steps 4, 12 |
| 7 | Qualified constraint identities | limitation | template § 4; runbook step 9 (`constraint_id` + `source_local_identity`, never the short name) |
| 8 | Constraint bounds as values | limitation, with a note | `indicators.json` `bounds` per reachable constraint (Appendix A); `verification_summary.json` `oracle.operand_bindings_digest`. Note: a constraint no declared axis reaches has its bound recorded nowhere. Such a constraint cannot change status in the study, so the bound is not needed to recover any outcome. Not load-bearing; no edit. |
| 9 | Preflight gate outcomes as observations, not success literals | limitation | template § 9 detail column; `preflight_results.v1` records every gate and the digests of the documents it read; `results/baseline_result.json` holds what the baseline gate observed |
| 10 | Snapshot values (fingerprints, tuples, digests, revisions) | limitation | snapshot appendix, all of it; runbook step 14 |
| 11 | **Oracle identity: its source digest** | **gap → template** | Not required anywhere. `verification_summary.v1` `oracle` carries `kind, sys_path, module, callable, operand_bindings_digest` — the bindings' digest, not the oracle's. Snapshot `manifest.content_used.oracle` carries `kind, module, callable, note`. `tools[]` digests the generic tools only. See G1. |
| 12 | Verification sample membership | limitation | `verification_summary.v1` `stores[].sampling.sampled_case_ids`, `seed`, `seed_source` |
| 13 | Per-point store not committed | limitation | template § 4 + runbook step 9 put the qualified verdicts into the record without the store; snapshot `stores[].path` + `compatibility_tuple` name the store |
| 14 | Glue ledger as values | limitation | snapshot `arms[].glue_ledger`, `effective_executable_fingerprint.inputs.allowed_modified_files` |
| 15 | Window provenance as a value, and the scan | limitation | snapshot `arms[].window`; template § 11; runbook step 7 |
| 16 | Cause of the availability kink (a mechanism claim in prose) | not an absence | A mechanism claim is the executor's argument and lives in § 6 prose under the contract too. The administrator never sees the model and cannot check mechanism; marking it "not checkable from the directory" is the synthesis doing its job. No contract change. |
| 17 | Cross-fingerprint nil | limitation | template § 12 explicit-nil rule |
| 18 | Finding ids, dispositions, homes | limitation | template § 15; runbook step 15 |
| 19 | The model's constraint set stated independently of the output | limitation | snapshot `manifest.content_used.baseline.verdicts`; `indicators.json` per-constraint entries |
| 20 | Evidence the scripts ran as written | limitation | snapshot `artifacts[]` digests, `tools[]` source digests, `package.repo_commit`, `stores[].compatibility_tuple` (carries the study-definition identity), `arms[].verification.command` |

Also checked, from outside the reader's list:

| — | The skill refuses a non-record directory | **gap → skill text** | `SKILL.md` "confirm it is a record directory before reading it as one" has no pre-capability allowance; the design expects administer mode on pre-capability directories. This read needed a waiver in the brief. See G2. |

## § Gaps

**G1 — the oracle's own source digest is not snapshotted.**
- *Why the write-up needed it:* the verification claim rests on the oracle being an independent implementation. The reader could name the oracle (`verify_stellaris.py`) but had no way to say *which* oracle — no digest, no revision. Every other piece of code the study leans on is digested (tools, adapter, allowed-modified files, verifier); the one whose independence underwrites the result is not.
- *Load-bearing?* **No.** Framing, LCOE, constraint outcomes, and findings are all recoverable without it. It affects how far the verification outcome can be trusted by a later reader, not whether it can be read.
- *Smallest edit if applied:* one field, `source_digest`, on the snapshot's `manifest.content_used.oracle` block, resolved at snapshot time over the oracle module files (`record-template.md` appendix). The verification summary schema is Item 4's and is closed (`additionalProperties: false`); it does not need to change, the snapshot is the right home because it is resolved at commit and never cites a live file.
- *Disposition:* `applied: record-template.md appendix, manifest.content_used.oracle gains source_digest (tool-source-digest/v1)` — `[OWNER]` 2026-08-20, applied despite not being load-bearing.
- *Owner note, carried to plan.md:* the oracle is a dev-process mechanism, not part of what a "study" is in general. For fusion-tea it may always be available; the general capability should not assume one. Whether runbook step 10 (verification, fails closed without an oracle) stays a mandatory gate is to be revisited altogether, not settled here.

**G2 — `SKILL.md` has no allowance for administering a pre-capability directory.**
- *Why the write-up needed it:* without the brief's waiver the skill's own text tells the reader to stop.
- *Load-bearing?* **No.** Every record from Item 6 onward is compliant; the waiver lives in a brief if a pre-capability read is ever needed again.
- *Disposition:* `not applied: the case does not recur under the capability; a brief-level waiver is the right weight for a one-time read.`

## § Reader misses

Facts that are inside the tracked files and the reader did not report. Evidence about the reader, not the contract.

- **Qualified objective channel name.** The `CHANNELS` map in `run_design_search.py` names the LCOE channel by its qualified key; the synthesis reports LCOE values but never states the channel name (template § 3 asks for it). Minor.
- **Declined axis, inconsistently handled.** The report's caveats state that interest rate was deliberately not swept and why. The synthesis carries that content in § 5 as a model finding, but § 6 entry 4 says "whether any axis was proposed and declined" is absent. Half-recovered: the reader found the fact and did not connect it to the template's declined-axis row. Minor.

Neither miss hides a gap: both facts are required by the template already.

## § Cross-check against `dry-run.md`

`dry-run.md` (Item 2's fill) sourced eight of its seventeen verdicts at least partly from `demo-proof-of-life/plan.md`, which is outside the directory. Read directory-only, four of those eight still recover, because the report's "What this does not prove" section carries them: the declined interest-rate axis with its reason, the engineered window and the oracle pre-scan, the era pin, and the findings' content (missing confinement-scaling constraint, levelization guard). Two do not: the owner's intake words (§ 2) and the four review-pass outcomes (§ 14). Those two are the facts whose only home was a work-item artifact, and both are template sections now. No `dry-run.md` NO-SOURCE entry was recovered by the reader, and nothing the reader recovered contradicts `dry-run.md`.

One thing the reader saw that the fill did not: `verification_summary.json`'s `verdicts_rederived` and `package_git_clean` are literals the script writes on success, not observations. Item 4's `preflight_results.v1` and `verification_summary.v1` already record observations and document digests, so the contract had closed this before the reader found it.

## § Zero-gap statement

Not applicable — two gaps found, neither load-bearing. Of the reader's 20 entries, 18 are limitations the contract already covers, one is not an absence, and one (G1) is a real gap in the snapshot. The template's seventeen headings survived the read unchanged; no heading was found that no compliant study could fill, and no fact the reader needed was found to lack a heading.
