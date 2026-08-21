# Product-lens ledger — stellarator-model-migration

Append-only. Verdict blocks from `~/.claude/scripts/product-lens.md` runs; dispositions recorded beneath each.

## spec — 2026-08-21 — rev 7ee0c22a · `.project/active/stellarator-model-migration/spec.md`
Epic: none

Point (re-derived): Regenerate the stellarator package on the stock route so the era adapter and its glue retire whole (no partial retirement, no dormant branch), RUN-STUDY Item 6 then runs on stock teax; the MFE models return to `models/` with the spine test reshaped in the same PR; the six scalar-function sites are rewritten now, filed upstream, and reverted via a `BACKLOG.md` row; every model change is tracked, classified, and given a rationale without slowing the work.   [source: `.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` § Decisions Q1–Q3, grade: owner; owner-verbatim quote in spec Known Requirements, grade: owner; `.project/backlog/epic_run_study_capability.md` Success Criteria "stock-teax execution", grade: owner; `exploration/stellarator_e2e/studies/ANNEX.md` § Deletion condition and epic Item 4 "absent rather than dormant", grade: agent/ratified]
Falsifier: After the item closes, `era_adapter.py`, `promotion_equivalence.py`, or any `fa0e06a`/`teax-v1-era` dependency still sits on a study or test path (or Item 6 would write its record under a non-sealed identity); or the MFE models are not in `models/` / the spine test is skipped or IFE-only; or a model edit exists with no ledger row.
Findings:
- spec-F1 [DON'T] The spec grades "teax main `744745f`, toolchain fixed" as `[HARD]`, but the source is an agent lookup (Q5 "resolved by lookup"; fusion-tea pins no teax commit — only the sysml-codegen `8a758e92` pin is real, `pyproject.toml:37`), and the spec's own open question still asks which teax the after-route tests use. — research plan § Decisions Q5 (AGENT) — disposition: DISPOSE — regrade the teax half to `[INFERRED]` (or record a teax pin as a decision); keep `[HARD]` for the codegen pin only.
- spec-F2 [DO]    No modeling-requirement obligation is carried into acceptance: R5/SC8 do not require `Source`/`Ref`/`Basis` on values the edits introduce (calc-def rewrites, the absorbed CAS28 5.0 M$ constant, the `n_mod` default, cross-part CAS27), and SC11 omits `agentic-mbse validate models/` and `scripts/trace_audit.py`. — `modeling_project/REQUIREMENTS.md` MR-4; `modeling_project/OVERVIEW.md` "Done" criterion 4 and Stage 2 exit criteria (INHERITED) — disposition: DISPOSE — add a citation column to the SC8 ledger and validation + trace-audit to SC11.
- spec-F3 [DO]    R5's three classes do not name the glue-absorption edits that SC2–SC4 presuppose (CAS28 constant, `n_mod` default, cross-part CAS27 wiring, BOP alias repoint moving from `era_adapter.py` into the model); an executor can read Class C (stop) or the Non-Goal "no cost-constant changes" against them and stall the adapter's retirement. — `ANNEX.md` § Loader exception and glue + Deletion condition (agent/ratified), inference that retirement requires the model to supply what the glue supplied (AGENT) — disposition: DISPOSE — state in R5 that glue absorption is a ledgered, no-stop class and exempt it from the cost-constant Non-Goal.
Smells: None.
Gate: DISPOSED (spec-F1, spec-F2, spec-F3)

### Dispositions applied 2026-08-21 (spec rev after this ledger entry)
- spec-F1 → applied: codegen pin stays `[HARD]`; teax `744745f` regraded to `[INFERRED]` with the open question pointing at design.
- spec-F2 → applied with one correction: SC8 gains an MR-4 `Source`/`Ref`/`Basis` column; SC11 gains `uv run agentic-mbse validate models/`. `scripts/trace_audit.py` does not exist (CLAUDE.md names it aspirationally; `traceability-system` is a paused spec), so MR-4 citations are checked by review, stated as such in SC11.
- spec-F3 → applied with a premise correction: the five glue values are *already in the model* (file:line cited in R5) and the pinned codegen resolves them (research § 4 probe), so absorption needs no model edit. R5 now says so, makes "regenerated package lacks one of them" a Class C surface rather than a reason to re-add glue, and clarifies the cost-constant Non-Goal.

## audit — 2026-08-21 — rev f8bf4f01
Point (re-derived): Migrate the stellarator model to stock generation and teax execution without semantic drift, promote both model families honestly, durably file the temporary rewrites upstream, and leave RUN-STUDY Item 6 on the stock route. [source: `.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` § Decisions Q1–Q3; `.project/concepts/stellarator-mbse-demo.md` criteria 1, 2, 5, grade: owner]
Falsifier: A clean checkout cannot generate/seal/load both families at contract 2.0.0, reproduce LCOE `275.2642200420774` and five satisfied verdicts, or locate the required upstream filings.
Findings:
- audit-F1 [DO] The required sysml-codegen filings exist only as an uncommitted sibling-worktree diff, so revision `f8bf4f01` does not durably deliver the six-site motivating case upstream. — `.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` § Decisions Q3 (owner) — falsifier: a clean sysml-codegen checkout lacks the filings — disposition: BLOCK
- audit-F2 [DON'T] Canonical and exploration SysML trees are manually copied and guarded by byte-equality tests; editing the documented canonical source without copying its twin fails the family spine. — `README.md` model organization (`[INHERITED]`; inference `[AGENT]`) — disposition: DISPOSE-and-proceed
- audit-F3 [DON'T] The retired-route guard exempts executable `handshake_1costingfe.py` as “historical” although it still contains glue and targets deleted 1.0.0 files; the green test depends on that interpretation. — `.project/backlog/epic_run_study_capability.md` temporary-route integrity (agent/ratified) — falsifier: remove the historical whitelist and the passing guard reports `patch_bop_wiring`; execute it and the deleted pipeline/input paths fail — disposition: DISPOSE-and-proceed
Smells: **1. Two representations must be manually kept synchronized** (`audit-F2`); **3. A special category exempts a case whose user-visible meaning is unchanged** and **6. A test passes only because it selects one duplicate, one route, or one interpretation** (`audit-F3`).
Gate: BLOCKED (audit-F1)

## audit resolution — 2026-08-21 — rev 56c587f6
Resolves:
- audit-F1: DEFERRED — authority: owner — basis: `/_my_ask_me` Q3, recorded in `plan.md:595,603`, explicitly permits the sysml-codegen rows to remain uncommitted for the owner's later commit.
Gate: DISPOSED (audit-F1, audit-F2, audit-F3)

## audit — 2026-08-21 — rev worktree B2/B4/B5 repairs atop c4c48ebe

Point (re-derived): Stock-route study and single-point commands must fail closed; incomplete execution or a failed numerical gate must never publish valid-looking evidence or report success. [source: `.project/concepts/stellarator-mbse-demo.md`; `.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md`, grade: owner]

Falsifier: A missing result/verdict, failed study case, or failed single-point comparison still produces or replaces a CSV, or exits successfully.

Findings: None.

Smells: No unresolved smell in the repaired surface. Contract-derived verdict identities clear smell 4; shared pre-publication validation and command-level failure tests clear the B4 manifestation of smell 6.

Resolves:
- `audit-F1`: DEFERRED — authority: owner — basis: prior structured resolution in `product-lens.md` rev `56c587f6`.
- `audit-F2`: DEFERRED — authority: owner — basis: `audit.md` § B1 retains synchronized exploration copies only until the demo epics finish.
- `audit-F3`: DEFERRED — authority: owner — basis: `audit.md` Q2 disposition retains the historical handshake with a backlog rewrite.

Gate: CLEAR
