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
| 8 | Resolved, checkable constraint bounds | limitation, with a reader correction | `report.html` records two executor claims: wall load ≤ 4.05 MW/m² and Q_eng ≥ 2. Those prose values are present and are not absences. What is missing is resolved, source-pinned bound evidence plus the beta and TBR values. The current contract supplies reachable bounds in `indicators.json` and pins the verification operands through `verification_summary.json` `oracle.operand_bindings_digest`. Not load-bearing; no edit. |
| 9 | Preflight gate outcomes as observations, not success literals | limitation | template § 9 detail column; `preflight_results.v1` records every gate and the digests of the documents it read; `results/baseline_result.json` holds what the baseline gate observed |
| 10 | Snapshot values (fingerprints, tuples, digests, revisions) | limitation | snapshot appendix, all of it; runbook step 15 |
| 11 | **Oracle identity: its source digest** | **gap → template** | Not required anywhere. `verification_summary.v1` `oracle` carries `kind, sys_path, module, callable, operand_bindings_digest` — the bindings' digest, not the oracle's. Snapshot `manifest.content_used.oracle` carries `kind, module, callable, note`. `tools[]` digests the generic tools only. See G1. |
| 12 | Verification sample membership | limitation | `verification_summary.v1` `stores[].sampling.sampled_case_ids`, `seed`, `seed_source` |
| 13 | Per-point store not committed | limitation | template § 4 + runbook step 9 put the qualified verdicts into the record without the store; snapshot `stores[].path` + `compatibility_tuple` name the store |
| 14 | Glue ledger as values | limitation | snapshot `arms[].glue_ledger`, `effective_executable_fingerprint.inputs.allowed_modified_files` |
| 15 | Window provenance as a value, and the scan | limitation | snapshot `arms[].window`; template § 11; runbook step 7 |
| 16 | Cause of the availability kink (a mechanism claim in prose) | not an absence | A mechanism claim is the executor's argument and lives in § 6 prose under the contract too. The administrator never sees the model and cannot check mechanism; marking it "not checkable from the directory" is the synthesis doing its job. No contract change. |
| 17 | Cross-fingerprint nil | limitation | template § 12 explicit-nil rule |
| 18 | Finding ids, dispositions, homes | limitation | template § 15; runbook step 14 |
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
- *Audit disposition:* `[OWNER]` 2026-08-20 — no further Item 5 work. The oracle's role and resulting evidence contract are deferred to the future Align discussion; the exact fingerprint shape is not an Item 5 certification condition.

**G2 — `SKILL.md` has no allowance for administering a pre-capability directory.**
- *Why the write-up needed it:* without the brief's waiver the skill's own text tells the reader to stop.
- *Load-bearing?* **No.** Every record from Item 6 onward is compliant; the waiver lives in a brief if a pre-capability read is ever needed again.
- *Disposition:* `not applied: the case does not recur under the capability; a brief-level waiver is the right weight for a one-time read.`

## § Reader misses

Facts that are inside the tracked files and the reader did not report. Evidence about the reader, not the contract.

- **Qualified objective channel name.** The `CHANNELS` map in `run_design_search.py` names the LCOE channel by its qualified key; the synthesis reports LCOE values but never states the channel name (template § 3 asks for it). Minor.
- **Declined axis, inconsistently handled.** The report's caveats state that interest rate was deliberately not swept and why. The synthesis carries that content in § 5 as a model finding, but § 6 entry 4 says "whether any axis was proposed and declined" is absent. Half-recovered: the reader found the fact and did not connect it to the template's declined-axis row. Minor.
- **Two bounds overclaimed as absent.** `report.html` states wall load ≤ 4.05 MW/m² and Q_eng ≥ 2. The synthesis acknowledges both in § 4, then § 6 entry 8 groups them with the genuinely absent beta and TBR values and says the bounds were never written to the directory. The prose claims are recorded; resolved, source-pinned evidence is not. Minor, and corrected in § Absences row 8 without editing the preserved synthesis.

None of the three misses hides a gap: the contract already requires the facts or the
resolved evidence that would replace the legacy prose claims.

## § Cross-check against `dry-run.md`

Completed during the 2026-08-20 audit walkthrough from the committed `dry-run.md`, the
unchanged cold-reader synthesis, and the tracked study-directory files. The cold read was
not rerun. "Inside" below means the dry-run fact has support in the tracked legacy study
directory; "outside" means its only stated support is `demo-proof-of-life/plan.md`.
Several sections are mixed, so forcing one evidence grade per section would erase the
distinction this comparison exists to preserve.

| Section | Dry-run evidence surface | What the synthesis recovered | Phase 3 result |
|---|---|---|---|
| §1 Study header | Mixed: internal ids in `run_design_search.py`; date, executor, and package path from the outside plan | Internal ids and the report date; no contract study id, executor, or resolved package identity | Clean: inside facts recovered; outside facts remain missing |
| §2 Intake | Outside only | States that owner intake is not recorded | Real absence, not a reader miss |
| §3 Objective and result | Mixed: objective channel and baseline pin inside; one optimum account in the outside plan | LCOE baseline and best feasible result, but not the qualified objective channel | **Reader miss:** qualified objective channel |
| §4 Constraint outcomes | Inside: CSV verdicts, report prose bounds, and the truncating export code | Short-name outcomes and the loss of qualified identity; §6 later overstates two prose bounds as absent | **Reader miss:** wall-load and recirculation prose bounds were present; resolved bound evidence remains absent |
| §5 Framing | Historical framing only in the outside plan; executor language and data inside | Keeps historical framing missing and supplies a labeled administrator reading | Clean under the owner-confirmed interpretation rule |
| §6 Per-axis account | Mixed: result structure in CSV/report; some execution narrative outside | Feasible structure and availability response from inside evidence; no-boundary judgment labeled as the administrator's | Clean |
| §7 Axis groups | Inside: `AXES` and `R_TIE` in `run_design_search.py` | Names all three axes and carries the hand-declared R tie in the findings | Clean for the synthesis contract; a synthesis is not a full template replay |
| §8 Indicators and rulings | Mixed: indicator artifacts absent; declined interest-rate axis appears in the report as well as the outside plan; name-based limitation in the script | Correctly reports indicators and rulings missing; carries the declined-axis reason in findings but calls the declined-axis fact absent in §6 | **Reader miss:** declined axis was found but not connected to the missing-evidence account |
| §9 Preflight results | Mixed: checks in the script and success literals in JSON; observed gate outcomes outside or absent | Distinguishes executed assertions and literals from captured observations | Clean |
| §10 Execution route and why | Mixed: direct-API route and glue ledger inside; route rationale also outside | Recovers stock study-layer execution, the era route, seal exception, and glue limitations | Clean |
| §11 Definition and window | Mixed: window constants and engineered pre-scan statement inside; fuller scan account outside | Recovers both windows, engineered provenance, and its interpretive limit | Clean |
| §12 Cross-fingerprint correlation | Inside procedure shows one prepared fingerprint; no resolved fingerprint or explicit nil is recorded | Correctly reports that no fingerprint value or explicit correlation nil was recorded | Clean: procedure is not a resolved record value |
| §13 Verification | Mixed: summary JSON inside; full review-pass evidence outside | Recovers sampling method, tolerance, result, and stated coverage limit from the JSON | Clean |
| §14 Review outcomes | Outside only | Correctly reports named reviews and dispositions missing | Real absence, not a reader miss |
| §15 Findings | Mixed: finding content in report/script and outside plan; ids, dispositions, and homes absent | Recovers the inside finding content and reports its structure and routing metadata missing | Clean |
| §16 Snapshot | No source | Reports `snapshot.json` and its resolved values missing | Real absence |
| §17 Missing-evidence section | Mixed: caveat content inside report and outside plan; no dedicated legacy section | Extracts the inside caveats and supplies the required missing-evidence section | Clean |

The comparison finds the three reader misses recorded above and no additional
contract gap. Every absence carried into § Absences is supported as absent from the
tracked directory. Facts supported only by the outside plan remain missing. Facts with
inside support are either recovered or recorded as one of the three reader misses, never
misclassified as a contract gap.

One thing the reader saw that the fill did not: `verification_summary.json`'s
`verdicts_rederived` and `package_git_clean` are literals the script writes on success,
not observations. Item 4's `preflight_results.v1` and `verification_summary.v1` already
record observations and document digests, so the contract had closed this before the
reader found it.

## § Zero-gap statement

Not applicable — two gaps found, neither load-bearing. Of the reader's 20 entries, 18 are limitations the contract already covers, one is not an absence, and one (G1) is a real gap in the snapshot. The template's seventeen headings survived the read unchanged; no heading was found that no compliant study could fill, and no fact the reader needed was found to lack a heading.
