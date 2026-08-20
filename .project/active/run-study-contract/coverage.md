# Spec coverage — where each mandatory record item lives

**Phase:** 6 of `.project/active/run-study-contract/plan.md`
**Date:** 2026-08-19
**Source of the item list:** `.project/active/run-study-contract/spec.md:71-100` — the fourteen items mandatory in every capability-compliant record.

Re-derived by reading the three written documents under `.claude/skills/run-study/`, not by copying `design.md`'s table forward. A design table proves only that the design agrees with itself.

## The map

| # | Spec item | Home | Deposited by |
|---|---|---|---|
| 1 | Objective and result | `record.md` §3 Objective and result | runbook step 8 |
| 2 | Constraint outcomes, by qualified identity, `satisfied \| violated \| indeterminate` | `record.md` §4 Constraint outcomes | runbook step 8 |
| 3 | Intake, the owner's words verbatim | `record.md` §2 Intake | runbook step 1 |
| 4 | Axis groups, per-key `fan_out \| tie` provenance | `record.md` §7 Axis groups | runbook step 2 |
| 5 | Indicators per proposed axis, the not-derivable disclosure, the user's ruling, and the model-development finding per `no_constraint_response` axis | `record.md` §8 Indicators and rulings | runbook steps 3 and 4 |
| 6 | Framing, as proposed and as judged | `record.md` §5 Framing | runbook steps 4 and 10 |
| 7 | Preflight results, pass or fail per gate | `record.md` §9 Preflight results | runbook step 5 |
| 8 | Execution route and why | `record.md` §10 Execution route and why | runbook step 7 |
| 9 | Compatibility tuples and cross-fingerprint correlation | **SPLIT** — values in `snapshot.json` `stores[].compatibility_tuple`; the correlation argument in `record.md` §12 | runbook steps 8 and 13 |
| 10 | Verification — command, sampling scheme, tolerance, outcome | **SPLIT** — command, sampling scheme, tolerance and summary digest in `snapshot.json` `arms[].verification`; outcome and what it licenses in `record.md` §13 | runbook step 9 |
| 11 | Review outcomes — each named lens, verdict, disposition | `record.md` §14 Review outcomes | runbook steps 4 and 11 |
| 12 | Findings, model and process, each with its routed home | `record.md` §15 Findings | runbook step 14 |
| 13 | Snapshot — the resolved-facts block | **SPLIT** — the resolved facts in `snapshot.json`; the window's "how it was chosen" clause in `record.md` §11. `record.md` §16 is a filename/digest/schema-version pointer, not a second copy | runbook steps 6 and 13 |
| 14 | Missing-evidence statement | `record.md` §17 What this record does not contain | runbook step 13 |

**Zero items with no home. Zero items with two homes that are not a declared split.**

## The three splits, and why each one is a split

Every split follows the same rule, stated once in `record-template.md`'s header: a fact a checker could evaluate is a value and lives in `snapshot.json`; the rest is an argument and lives in `record.md`. Neither file restates the other.

**Item 9.** A teax compatibility tuple is a value — a checker compares it. What it *means* that two arms sit on different fingerprints, which boundary was crossed, which `predicate_ir` differences were disclosed, and what the comparison therefore licenses is an argument no checker can evaluate. Tuples are stated once in `stores[]` and referenced by `store_id`, so two arms sharing a store cannot drift (SF5).

**Item 10.** The command, the sampling scheme, the tolerance, and the digest of `results/verification_summary.json` are values. Whether the outcome licenses the study's claims — and what verification did *not* cover, such as a glue-fed value identical by construction on both sides — is an argument (MF5).

**Item 13, the SF1 window clause.** The spec places "how it was chosen" inside the snapshot's study-definition bullet. The design surfaced the move rather than making it silently: the window's bounds and its `engineered | sourced` provenance stay snapshot values; how it was chosen is the argument and lands in `record.md` §11. This is the third split, and the plan named only two — recorded here rather than folded into the count. The design declares it under "Spec deviations surfaced", so it is a stated deviation, not a new one.

Phase 2's dry run tested exactly this seam and found it clean: the proof-of-life, with no contract telling it to, had already put the bounds (`run_design_search.py:123-125`) and the scan story (`demo-proof-of-life/plan.md`, Phase 1 result) in two different places.

## Cross-check against the snapshot bullet list

`spec.md:87-98` lists eleven snapshot bullets. All eleven have a home in `record-template.md`'s appendix:

| Spec snapshot bullet | Snapshot field |
|---|---|
| package path; sealed, model-contract, semantic fingerprints | `package.path`; `fingerprints` floor table |
| effective executable fingerprint + three inputs, or the no-adapter nil | `arms[].effective_executable_fingerprint` |
| manifest digest + the manifest content used | `manifest.digest`, `manifest.content_used` |
| each tool's path and revision/digest | `tools[]` |
| repository commit at execution; package git-clean result | `package.repo_commit`, `package.git_clean` |
| teax revision and the era pin | `teax` |
| glue ledger inline, one entry per rung, explicit "none" | `arms[].glue_ledger` + `glue_ledger_none` |
| study definition: `study_id`, `entry_models`, strategy, window + provenance | `study_id`, `arms[].entry_models`, `arms[].strategy`, `arms[].window` |
| store path(s) with the complete compatibility tuple | `stores[]` |
| result-artifact list with a digest per file | `arms[].artifacts` |
| `indicators.json` in the record directory, with its digest | `indicators` |

The one clause not in the appendix is the window's "how it was chosen", homed in §11 — the SF1 split above, and the only one.
