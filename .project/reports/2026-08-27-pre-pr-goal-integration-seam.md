# Pre-PR branch gate — `feat/goal-integration-seam`

**Date**: 2026-08-27
**Branch**: `feat/goal-integration-seam` @ `85271287` → target `main` @ `8d6c443b`
**Declared scope (brief)**: GSTH Items 1, 3, 4
**Verdict**: **NOT READY — one blocker, owner decision required**

The mechanical gate is clean. Tests pass, no debug artifacts, no secrets, no product-lens
block outstanding. The blocker is scope: the branch does not contain what the brief says it
contains, and the two-PR ship shape the brief describes cannot happen from this branch as it
stands.

---

## Blocker — the branch carries two more bodies of work, both unclosed

`main..HEAD` is 174 commits and 384 files. Items 1, 3, and 4 account for part of it. The rest
is work from two other items that are still open in `.project/active/`.

**B1. Item 2's research seam is fully contained in this branch.**

`feat/goal-research-seam` is an ancestor of `HEAD` — every one of its commits is already here:

```
git merge-base --is-ancestor feat/goal-research-seam HEAD   → true
git log --oneline HEAD..feat/goal-research-seam             → empty
```

21 research-seam commits sit in `main..HEAD` (Phases 1–8 plus the audit fix pass `9637f1b7`),
along with the whole `tests/research/` suite (23 files, 2065 lines, new vs `main`).

Two consequences the brief's plan does not survive:

- Merging this branch merges Item 2. It is not "Item 2 follows separately after merge" — it
  is "Item 2 ships now, in this PR."
- After that merge, `feat/goal-research-seam` has zero commits left to PR.

Item 2 is **audited** (`.project/active/goal-research-seam/audit.md`) and its product-lens
gate reads CLEAR at the fix-pass hop, but it is **not closed** — still sitting unarchived in
`.project/active/goal-research-seam/`. `/_my_pre_pr` names this exact condition as one to
surface before proceeding.

**B2. Run-Study Item 6 Phases 1–3 are also on this branch, and Item 6 is neither audited nor
closed.**

Commits include `WI-030 audited and closed; WI-031 closed; Item 6 Phase 1 study scaffold`
(`ffa5c54c`), Item 6 Phase 2, and Item 6 Phase 3 (`829dda6d`, `d92c5316`, `79ba878c`). These
bring the branch's large artifacts:

| bytes | path |
|---|---|
| 2,355,920 | `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/results/points.csv` |
| 2,011,595 | `.../20260823-magnet-technology-ab/results/oracle_operands.csv` |
| 1,358,785 | `.../20260821-power-cycle-ab/results/points.csv` |
| 667,779 | `knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/raw.pdf` (+ 8 PNGs) |

`CURRENT_WORK.md:19` records Item 6's state as "Next: Phase 4 (close) — owner sequences merge
to `main` ... then `/_my_audit`." So this is work the owner intended to land, but it has not
been through audit or close. It is riding in this PR either way.

**What this needs is an owner ruling, not a fix from the gate.** Three shapes, and I'd
recommend the first:

1. **Ship the branch as one PR covering Items 1, 2, 3, 4 and Run-Study Item 6 Phases 1–3**,
   and delete `feat/goal-research-seam` as redundant. Cheapest, matches what is actually on
   disk. Cost: Item 2 and Item 6 merge before their close/audit stages, so their archives get
   written after the merge rather than before.
2. **Rebuild a narrow branch** carrying only Items 1/3/4 commits. Honors the stated two-PR
   shape. Cost: the three items' commits are interleaved with Item 2's and Item 6's across 174
   commits, so this is a substantial and error-prone rewrite for no product gain.
3. **Close Item 2 and audit+close Item 6 first**, then ship everything as one PR. Highest
   confidence, longest path.

Nothing below blocks. All of it is reportable and none of it is a regression against `main`.

---

## Checks run

### Tests — PASS

```
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env \
  python -m pytest tests/models tests/study tests/research tests/orchestration \
  tests/test_dependency_provenance.py
```

**570 passed, 14 skipped, 0 failed** in 6m24s (exit 0).

`tests/research/` was present and ran — it is on this branch (see B1), not absent as the brief
anticipated. The 570 therefore includes Item 2's suite.

Environment: `set -a` sourcing of `~/1cfe/agentic-mbse/.env` and `.venv/integration.env` was
needed, per the `CURRENT_WORK` note that the files do not export.

### Product-lens gate — CLEAR (fail-closed check passed)

All three declared items have a ledger, and every `BLOCK` in every block of each ledger is
resolved by a later block that cites it by name.

| item | ledger | blocks raised | final |
|---|---|---|---|
| Item 1 | `.project/completed/20260827_goal-harness-contract/product-lens.md` | spec-F1/F2, design-F1/F2, audit-F1/F2 | CLEAR at the audit-fix hop |
| Item 3 | `.project/completed/20260827_goal-integration-seam/product-lens.md` | spec-F1/F2, design-F1/F2 | CLEAR at the design revision hop |
| Item 4 | `.project/completed/20260827_goal-cold-pickup-proof/product-lens.md` | spec-F1/F2 | CLEAR at the implementation hop, earlier blocks cited |

Parent epic gate (`epic_goal_strategy_task_harness.md` § Product-Lens, line 78): `epic-plan-F1`
and `epic-plan-F2` both raised BLOCK, both resolved by owner disposition 2026-08-25 —
**Gate: CLEAR**. No live epic-level block.

Item 2's ledger (`.project/active/goal-research-seam/product-lens.md`) is also CLEAR at its
fix-pass hop, which matters given B1.

### Hygiene — clean

- No `breakpoint()`, `pdb`, or debug prints in any added or modified `.py`.
- No `TODO`/`FIXME` introduced in new Python, in `scripts/integrate.py`, in the operator
  guide, or in `GOAL_RUNBOOK.md`.
- No secret-shaped files (`.env`, `.pem`, keys, credentials) in the diff.
- Large binaries are the Item 6 study CSVs and the one registered source PDF listed in B2 —
  intentional artifacts, not strays, but they belong to the B2 scope question.

### Lint and format — pre-existing condition, not a branch regression

Ruff is configured (`pyproject.toml:39`, line-length 100, `select = ["E","F","I","W"]`) but is
**not enforced in CI** — `.github/workflows/` holds only `notify_visualization.yml`. `main` is
already non-compliant: 29 of 44 files under `tests/study` + `scripts` would reformat on `main`
today.

The 50 Python files this branch adds carry 63 lint errors:

| count | rule |
|---|---|
| 32 | E501 line too long |
| 9 | I001 unsorted imports |
| 9 | E702 multiple statements on one line |
| 6 | W293 whitespace on blank line |
| 2 | F401 unused import |
| 2 | E402 import not at top |
| 2 | E401 multiple imports on one line |
| 1 | F841 unused local |

**I did not reformat.** Running `ruff format` would touch 42 of the 50 new files on a PR that
is already 384 files, burying the reviewable content, and it would not close a gate that
nothing enforces. Recommend a separate repo-wide formatting pass if the owner wants ruff clean.

The four genuinely-dead items are worth a look on their own terms:

- `exploration/stellarator_e2e/generated/modules/mfe_plasma_scaling/conductor_peak_field.py:39` — `pydantic.RootModel` imported, unused
- `exploration/stellarator_e2e/generated/modules/mfe_plasma_scaling/volume_averaged_beta.py:61` — same
- `tests/models/test_beta_peak_field.py:88` — local `numbers` assigned, never used
- Both `RootModel` cases are in **generated** files, so the fix belongs upstream in the codegen template, not here.

### Documentation — stale post-archival paths

`/_my_close` archived the three items but left path citations behind. I fixed the clearly-live
ones; the rest are reported, not edited.

**Fixed in the working tree (uncommitted, for the orchestrator to commit):**

- `.project/adr/009-integration-is-a-fixed-point-proof.md:18` and `:49` — repointed
  `.project/active/goal-integration-seam/design.md` → `.project/completed/20260827_goal-integration-seam/design.md`.
  ADR-009 is a live architecture record; its "where the mechanism is recorded" pointer has to
  resolve. Both targets verified present. **This is my edit.**

**Already in the working tree when I started (not mine):**

- `tests/orchestration/test_goal_contract.py:4` — docstring repointed to the archive.
- `work/orchestration/GOAL_RUNBOOK.md:74` — the 2026-08-27 amendment's citation of
  `gate-probe-record.md` repointed to the archive.

Both are correct and both targets exist. They need committing before the PR.

**Reported, not edited — stale citations in live files:**

- `work/orchestration/goals/cryo-volume-basis/trail.md:254` cites
  `.project/active/goal-cold-pickup-proof/verification_record.md` (now under
  `.project/completed/20260827_goal-cold-pickup-proof/`). This is inside a dated amendment in
  a goal trail, which the runbook treats as an append-only record. Repointing it is the same
  class of edit as the two above, but the trail is goal-layer product and the call belongs to
  the goal operator, not to this gate.
- `work/active/WI-030…`, `WI-031…`, `WI-032…` paths are cited from
  `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:31`,
  `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md:12`,
  `.project/backlog/epic_goal_strategy_task_harness.md:346`,
  `.project/backlog/epic_run_study_capability.md:181`, and several `.project/concepts/` files.
  All three now live under `work/completed/`.
- `.project/active/demo-study-parameterization-policy/policy.md` is cited from
  `modeling_project/STUDY_POLICY.md:3` and `tests/study/test_policy_path.py:15`; it was
  ratified and moved to `modeling_project/STUDY_POLICY.md` (`CURRENT_WORK.md:61`).

Forward references to `.project/active/goal-integration-study-proof/` and
`.project/active/goal-research-model-proof/` also do not resolve, but those are Items 5 and 6
directories that do not exist yet — expected, not stale.

---

## What is ready

Setting the scope question aside, the three declared items are in good shape. Tests green,
lens gates clear at item and epic level, hygiene clean, the owner decisions the brief names
(R3 at `e891b23a`, the runbook amendments at `4a8de283`) are present and committed.

## What the orchestrator needs to do

1. Take B1/B2 to the owner and get a ruling on PR scope. Nothing else can proceed past it.
2. Commit the three working-tree path fixes (two pre-existing, one mine).
3. Decide whether the stale-path sweep is part of this PR or a follow-up.

I did not push and did not open a PR, per the brief.
