# Spike: regeneration determinism in place (GSTH Item 3, R-D4)

**Date:** 2026-08-26 · **Branch:** `feat/goal-integration-seam` · **Commit:** `beb994aa` · **Owner:** Reid W
**Serves:** `.project/active/goal-integration-seam/spec.md` R-D4 (and the Open Questions bullet at `:153`)
**Status:** closed — **CONFIRMED**

## Summary of Findings

**CONFIRMED.** The pinned `sysml-codegen generate --smart-regen --preserve-handwritten`, run in place on the already-sealed stellarator package, is byte-stable. The first in-place regeneration changed **zero bytes** — `git status --porcelain` returned empty and a full-tree sha256 manifest was identical to the sealed baseline. A second in-place run was identical again. Both fingerprints held at their WI-030 values across all three states:

| state | `git status --porcelain` | semantic fingerprint | executable fingerprint |
|---|---|---|---|
| sealed (baseline) | 0 entries | `1ca93d0c…1ab860` | `7447efea…2d9a97` |
| after in-place generate #1 | **0 entries** | `1ca93d0c…1ab860` | `7447efea…2d9a97` |
| after in-place generate #2 | **0 entries** | `1ca93d0c…1ab860` | `7447efea…2d9a97` |

**What this means for the spec.** R-D4's assumption holds, so **R-B4 needs no exemption for regeneration**. The seam can re-run the full gate sequence, regeneration included, and R-D1's "same identity" `CANDIDATE` path is the one that fires on unchanged inputs — not the fail-closed `BLOCKER` fallback R-D4 wrote as insurance. R-C1 (non-git-clean tree is a `BLOCKER`) stays as written and simply does not trip on a re-run. Design is unblocked and may treat idempotent re-invocation as the normal case rather than a hazard.

**Why it is stable — the mechanism, which is worth knowing.** `--preserve-handwritten` does not merely restore the handwritten files, it never opens them for write. All 58 files under `generated/handwritten/` — including both `AUTO_IMPLEMENTED = False` normative impls — kept their original mtimes across both runs. The other 95 files (modules, schemas, contracts, inputs, pipelines, tests) were rewritten every run, with byte-identical content each time. Content is stable; only mtimes move.

This also explains why in-place is *more* stable than the scratch-target comparison WI-030 ran. WI-030's two residual differences (`package_contract.json` sha entries for preserved impls vs. fresh stubs, and stale `SysML Source:` line refs inside preserved stubs — `WI-030 plan:291`) are artifacts of a scratch target generating *fresh* stubs where the real tree has *preserved* ones. In place, there are no fresh stubs to differ from. The in-place case is the easier one, and it is clean.

**Operational notes a design should carry.**
- **Runtime is negligible.** 1.80s and 1.81s wall for the two generates. Regeneration is not the expensive gate in the sequence; re-running it on every invocation costs nothing worth designing around.
- **Env precondition.** `SYSIDE_LICENSE_KEY` must be exported (`set -a; source ~/1cfe/agentic-mbse/.env; set +a`). This is a "could not run" condition in R-A6 terms, not a refusal — the same class as the `tests/models` license failure the spec already cites.
- **`STOP_PARSER_TEAX_ROOT` is not needed for generate.** It was exported during the probe but generation does not read it. teax matters downstream (verify/execution), not at the regeneration gate.
- **mtimes move on 95 of 153 files, harmlessly.** Nothing under `scripts/study/` or `tests/models/` reads `st_mtime`/`getmtime` (grep returned empty), and both git and the fingerprints are content-addressed. Recorded so a future design does not build an mtime-based change detector on top of this and get a false positive on every re-run.
- **The pin is the installed wheel.** `sysml_codegen` resolved to `.venv/lib/python3.12/site-packages/sysml_codegen/__init__.py`, version `0.1.1`, matching `pyproject.toml:10` and the git rev pin `8a758e9240707b58fe32a509c3b509941ca4fa01` (`pyproject.toml:37`). Migration invariant I2 (never generate through the local checkout) was observed.

**Scope of the claim.** This is one package (stellarator, MFE family) at one sealed state, under one codegen pin. It confirms the assumption R-D4 actually made and no more. It does not establish that regeneration is stable across a codegen version bump — that is a different question, and one the toolchain pin gate (R-B1.1a) is what stands in front of.

## Question / Goal

`spec.md` R-D4 assumes the pinned generate, run a second time in place on an already-sealed package, leaves the tree git-clean and both fingerprints unmoved. WI-030 checked the nearest thing — generate twice against a *scratch* target and `diff -r` (`work/completed/20260822_WI-030_computed-beta-peak-field/plan.md:158`, result `:291`) — but never a re-run in place onto its own output.

**Confirms:** first and second in-place regeneration both leave `git status --porcelain` empty and both fingerprints at their sealed values.
**Disproves:** any file content moves, or either fingerprint changes, at either run.

Why it matters: if stable, the seam re-runs the whole gate sequence idempotently (R-B4, no gate skipped). If not, R-B4 needs a stated exemption for regeneration and the design changes shape.

## Log

**Approach.** Never generate against the real repo tree. Copy the sealed package into a scratch directory, make that directory its own git repo so `git status` is meaningful, and run the pinned codegen from the real repo's venv with absolute `--models`/`--output` paths pointing into the scratch. The real repo is read from, never written to.

**Step 0 — baseline check.** The repo tree at `beb994aa` already carries WI-030's recorded fingerprints, so it is genuinely in the sealed state:

```
generated/contracts/model_contract.json   semantic_fingerprint   = 1ca93d0c988c2828bb1ce3fef18be85be86947a296a33b236d77daeb0f1ab860
generated/contracts/package_contract.json executable_fingerprint = 7447efea9f205dc64543a976e6a3c21a9fd468726f2de78aaf8d845e6f2d9a97
```

Both match `WI-030 plan:291` exactly.

**Step 1 — first probe run.** Wrote `spike/probe_regen_inplace.sh`, staged `models/`, `generated/`, `pkg/`, `stellarator.snapshot.json` into `/tmp/spike-regen/<sha>/`, committed as `sealed`, ran generate twice. Result was already clean, but the probe wrote its own logs into the scratch **git root**, so `git status --porcelain` showed 2 then 5 untracked entries — all of them the probe's own files, no `M` entries anywhere. Correct answer, muddy evidence.

**Step 2 — tightened probe.** Split the scratch into `tree/` (the git root, package only) and `out/` (probe artifacts, outside git). Added a sealed-baseline sha manifest so the *first* in-place regeneration is compared byte-for-byte, not just checked for git-cleanliness, and added mtime capture to separate "rewritten identically" from "not touched". Re-ran:

```
-- clean at start: [0 entries]
-- git status --porcelain after sealed: 0 entries
[sealed] semantic   = 1ca93d0c…1ab860
[sealed] executable = 7447efea…2d9a97
== generate (1)   exit=0   wall=1.80s
-- git status --porcelain after 1: 0 entries
[1] semantic   = 1ca93d0c…1ab860
[1] executable = 7447efea…2d9a97
== compare sealed vs run1 (first in-place regeneration)
   IDENTICAL tree (sealed == run1) — first in-place regen changed no bytes
-- files whose mtime moved in run1: 95 of 153
== generate (2)   exit=0   wall=1.81s
-- git status --porcelain after 2: 0 entries
[2] semantic   = 1ca93d0c…1ab860
[2] executable = 7447efea…2d9a97
== compare run1 vs run2
   IDENTICAL tree (run1 == run2)
```

**Step 3 — stencil accounting.** Both generate logs report the same line, and it is the handwritten-preservation gate (R-B1.3) passing on a re-run:

```
INFO: Stencils - New: 0, Preserved: 55, Regenerated: 0
```

`New: 0` (versus WI-030's `New: 2`) is the expected difference: WI-030 was adding two calcs, this run adds nothing.

**Step 4 — what actually got rewritten.** Grouping the 95 moved-mtime files and the 58 untouched ones by top-level directory:

| rewritten (identical content) | untouched (never opened) |
|---|---|
| `modules/` 67, `schemas/` 11, `inputs/` 6, `contracts/` 4, `tests/` 2, `pipelines/` 2, `primitives.py`, `__init__.py`, `IMPLEMENTATION_BACKLOG.md` | `handwritten/` — all 58 |

Both normative impls (`volume_averaged_beta_impl.py`, `conductor_peak_field_impl.py`) are in the untouched set.

**Step 5 — mtime safety and pin identity.** `grep -rn "st_mtime\|getmtime" scripts/study/ tests/models/` → empty. `sysml_codegen.__file__` → the installed wheel, `__version__` `0.1.1`, matching the `pyproject.toml` pin.

**Real repo left untouched.** The only paths written under the repo are this findings doc, the probe script under `spike/`, and the spec back-reference. `exploration/stellarator_e2e/` was read only.

## Reproduction

```bash
cd /home/reid/1cfe/fusion-tea
set -a; source ~/1cfe/agentic-mbse/.env; set +a      # SYSIDE_LICENSE_KEY
bash .project/active/goal-integration-seam/spike/probe_regen_inplace.sh
```

Runs in about 15 seconds. Expected output is the Step 2 block above: `0 entries` at every snapshot, `IDENTICAL tree` twice, both fingerprints unchanged. Artifacts (per-run logs, porcelain snapshots, sha manifests, mtime lists, diffs) land in `/tmp/spike-regen/<commit-sha>/out/`; the scratch package git repo is `/tmp/spike-regen/<commit-sha>/tree/`. Both are disposable and rebuilt from scratch on each run. The script is throwaway probe code — it is not a kept test.

## Open Questions / Follow-ups

- **Stability across a codegen version bump is untested and out of scope here.** R-B1.1a (the pinned-toolchain gate) is what stands in front of that question; this spike assumes the pin holds.
- **Other packages are untested.** Only the stellarator/MFE package was probed. The mechanism (preserve-handwritten never writes the handwritten subtree) is package-agnostic and should generalize, but that is reasoning, not evidence.
- **Whether the seam should regenerate at all on a re-run is still design's call.** This spike removes the *correctness* objection to always regenerating; at 1.8s there is no cost objection either. Whether design still wants to skip it for another reason is open, and R-B4 currently says do not.
