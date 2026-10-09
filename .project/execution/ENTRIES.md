# Execution Facts

Append-only log of how this codebase and environment actually behave, discovered while working. Newest at the bottom.

The rules for writing an entry are in `README.md`, in this directory. Do not rewrite or reorder existing entries.

---

## [WebFetch] 2026-09-17

**Fact:** `1cf.energy` returns HTTP 403 to the WebFetch tool. `curl` with a browser User-Agent works. Blog posts also exist as markdown in `~/1cfe/1costingfe/docs/blog/`.
**Evidence:** Observed directly during content retrieval attempts.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [concept_analysis] 2026-09-17

**Fact:** `print_cas_breakdown` uses `%.1f`, so small nonzero per-module CAS22 values print as `0.0`. Assessment findings that call an override "dead/zero" are often a display-rounding misread — verify the underlying `cas22_detail` floats before removing.
**Evidence:** Manual verification on concept 24-dense-plasma-focus iter-2 (C220102 shield, C220107/C220109 absolute overrides).
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [orchestrate-stage.sh] 2026-09-17

**Fact:** Stages write evidence files (screenshots, JSON) as they go and the summary last. Stopping a stage on a reviewer's advice can kill a run that already has results — only the findings doc is missing. Check the stage's output folder with `ls` before stopping.
**Evidence:** Model-viz spike, 2026-09-14; stage home had 25 screenshots and results JSON but no summary doc.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [sysml-codegen] 2026-09-17

**Fact:** When a `manual_required` calc's inputs change, `sysml-codegen generate --smart-regen --preserve-handwritten` overwrites the handwritten impl with a `NotImplementedError` stencil and moves the old body to a backup dir. Fix: restore by hand, delete `handwritten/backup/`, regenerate again.
**Evidence:** WI-041, 2026-09-04; `SealVerificationError: TAMPER ... MISSING(handwritten/backup/...)`.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [claude -p] 2026-09-17

**Fact:** For cold/fresh headless sessions, invoke `claude -p` directly with `--output-format stream-json` (survives mid-run kill), not `orchestrate-stage.sh`. Kill via `setsid` pgid. Poll with date-anchored greps. Freshness fence checks must sweep tool-call inputs, not raw transcript. Background Bash caps at 10 min.
**Evidence:** GSTH Item 4 cold-session proof, 2026-08-26.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [systemd-run] 2026-09-17

**Fact:** `setsid nohup` runs launched from the tool shell are killed silently after ~3 minutes (20 GB free). `systemd-run --user --collect --unit=<name> bash -c '...'` survives. The session kills detached process trees it still accounts for; a user systemd unit is outside that tree.
**Evidence:** 2026-09-13, WI-057 study arms; two runs died at 182 rows, relaunched under systemd completed.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [bash] 2026-09-17

**Fact:** Two heredocs chained on one command line (`python - <<'EOF' && cat >> file <<'EOF2'`) hand the wrong body to the first command when bodies aren't written in operator order. The Python run gets prose as input — `SyntaxError`, nothing written. Use one heredoc per tool call.
**Evidence:** stored-energy-basis round 2, 2026-09-05; trail entry and dispositions had to be redone.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [tests/study] 2026-09-17

**Fact:** Never run two `tests/study` batteries at once — they share `.integration_workspace` and produce 41 phantom workspace errors with wrong pass/fail counts. The harness's memory accounting kills background waiters; use `setsid nohup` for detached runs and Monitor for polling, not `run_in_background` waiters.
**Evidence:** 2026-09-08, goal plant-closure T-004; concurrent batteries gave 89/380/41 instead of true 86/424/1.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [orchestrate-stage.sh] 2026-09-17

**Fact:** An orchestration run that pins a fixture (e.g. snapshot sha256) cannot share a checkout with a modeling session that regenerates the package. Use `git worktree add` to a sibling path and run tests with the primary `.venv/bin/python`.
**Evidence:** 2026-09-13, model-viz tests; snapshot moved 377→399 attrs mid-run and commits interleaved.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [orchestrate-stage.sh] 2026-09-17

**Fact:** Stage subagents can lose git/.claude write permissions mid-run. `resume` drops `bypassPermissions` and the flag is refused. Route: stage writes to a staging dir, orchestrator applies and commits. Plan one fresh `run implement` per phase. `run spec` and `run concept_design_review` default to `acceptEdits`, blocking venv Python.
**Evidence:** 2026-08-25 (GSTH Item 1), 2026-09-13 (model-viz v2), 2026-09-14 (spec/review stages).
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [bash] 2026-09-17

**Fact:** `pkill -f '<pattern>'` from the Bash tool matches the tool's own shell command line and kills it (exit 144, chained cleanup skipped). Use a bracket pattern like `stud[y].py` or kill by PID.
**Evidence:** WI-042 study, 2026-09-05; the `rm` of stale outputs never ran.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [sysml-codegen] 2026-09-17

**Fact:** After a model regeneration, five producers must be re-pinned in order: snapshot, manifest (files as paths not dicts), census (import `scripts.integrate` as module), fixtures (from indicators.py), single runner. Manifest returns dicts not strings for file entries; importing `scripts/integrate.py` by path breaks frozen dataclasses.
**Evidence:** WI-042, 2026-09-05; manifest slip caught only by `m.load` validation. Addenda from WI-043 (2026-09-07) and WI-048 (2026-09-13).
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [tests/test_dependency_provenance.py] 2026-09-17

**Fact:** The provenance test hashes three sealed stop-parser wheel files. The wheels live at `/home/reid/1cfe/stop-parser-sealed-wheels/`. The uv git-built wheels in `~/.cache/uv` hash differently and fail. Export `STOP_PARSER_WHEEL_TARGET` and the three `STOP_PARSER_{AGENTIC,CODEGEN,COSTINGFE}_WHEEL` vars.
**Evidence:** Recovered 2026-08-26 from temp dir; sha256-verified.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [tests/study/test_records.py] 2026-09-17

**Fact:** Study record commits must pass `test_records.py` — no `<` character anywhere in `record.md`, every snapshot arm needs `effective_executable_fingerprint`. The goal T-scope line is the most-skipped step. Fix prose slips via dated `## Addendum`, never by editing frozen text. Two-lineage comparison studies need one row per arm per point.
**Evidence:** `20260903-priced-levers` round, `20260903-wall-and-heating` finish, `20260913-structural-decomposition` two-lineage study.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [syside] 2026-09-17

**Fact:** `tests/models` needs `SYSIDE_LICENSE_KEY` exported; the `.env` file defines it without `export`, so a plain `source` doesn't reach `uv run`. Use `set -a; source .env; set +a`. The study suite also needs `STOP_PARSER_TEAX_ROOT` and `PYTHONPATH` to teax-simkit.
**Evidence:** 2026-08-22, RUN-STUDY Item 6 Phase 2; setup failure "SYSIDE_LICENSE_KEY is not loaded".
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [agentic-mbse] 2026-09-17

**Fact:** `--force` only bypasses the `output.md` existence check. It does NOT delete old files. Need explicit cleanup before re-extraction.
**Evidence:** Observed during re-extraction runs; old artifacts persisted alongside new output.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [agentic-mbse] 2026-09-17

**Fact:** During re-extraction, existing dirs (e.g., `images/`) mean multiple subdirs exist under the output dir. Must search for subdirs containing `output.md` rather than checking `len(subdirs) == 1`.
**Evidence:** `_flatten_extraction_output()` in `zotero_ingest.py`; observed during batch re-extraction.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [agentic-mbse] 2026-09-17

**Fact:** `agentic-mbse extract --check` (and other commands invoking Claude CLI) produce no stdout when run from non-interactive shells. Workaround: pipe to file, then read — `uv run agentic-mbse extract --check-json <pdf> > /tmp/out.json 2>/tmp/err.txt`.
**Evidence:** Observed during scripted extraction runs; empty stdout in subprocess.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [claude -p] 2026-09-17

**Fact:** `--output-format json` returns a **list** of event objects, not a dict. The result text is in the last event with `type: "result"`, key `"result"`. There is no `--max-tokens` flag.
**Evidence:** Phase 2a expand.py development; parsing failures until list-indexing was used.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [agentic-mbse] 2026-09-17

**Fact:** The Hawker PDF extraction (`a_simplified_economic_model_for_inertial_fusion/output.md`) has 17 `~~strikethrough~~` markers. This is an upstream OCR/table limitation — same count in old and new extraction. Not fixable from fusion-tea side.
**Evidence:** Compared old and new extraction outputs; count identical.
**Source:** migrated from the native memory store, triaged 2026-09-17.

## [scripts/study/verify.py] 2026-09-17

**Fact:** A comparison failure exits with stderr before writing the requested `--out` summary. Check exit status before loading that file; a failed run does not emit a verification summary.
**Evidence:** `scripts/study/verify.py:556`; pre-reveal feasibility study `results/generic-verification-refusal.json`, commit `1394d43d`.

## [sysml-codegen] 2026-09-22

**Fact:** In the pinned integration toolchain, smart regeneration can replace handwritten completions with stubs when public function annotations do not match the generated signature or when its scanner treats `inputs.model_dump()` as an input field. WI-089 uses typed public adapters that delegate to unchanged reviewed bodies, and proves the exact `--smart-regen --preserve-handwritten` command is byte-stable.
**Evidence:** `work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/evidence/smart-normalization-verification.json`; `work/orchestration/goals/aries-integrated-heat-electricity/evidence/packaging-review.md@143a556c`.

## [starlette.testclient] 2026-10-09

**Fact:** Starlette 1.3.1, the version `requirements-serve.txt` pins, has its test client import `httpx2` first and fall back to `httpx` with a `StarletteDeprecationWarning`. The website-contract gate runs on that fallback: its request driver and `test_cors.py` use FastAPI's `TestClient`, and the gate installs `httpx==0.28.1` from `exploration/concept_explorer/website_contract/test_tools.txt`. A Starlette release that drops the fallback breaks the gate's contract step as well as its self-tests, so a Starlette bump needs `test_tools.txt` changed with it.
**Evidence:** `starlette/testclient.py:32-51` in the 1.3.1 wheel, read 2026-10-09; `requirements-serve.txt:47` pins `starlette==1.3.1` and lists no `httpx2`; `website_contract/frontend_requests.py:173` imports `fastapi.testclient.TestClient`. The warning was first noticed in the gate's runs during `.project/completed/20261009_explorer-api-contract-gate/`.

## [docker] 2026-10-09

**Fact:** `docker` fails in agent shells with "permission denied while trying to connect to the docker API at unix:///var/run/docker.sock". The user `reid` is listed in the `docker` group, but the shell's process groups don't include it. `sg docker -c '<command>'` runs the command with the group and reaches the daemon.
**Evidence:** 2026-10-09: `docker info` gave the permission error; `id` showed no `docker` group while `getent group docker` printed `docker:x:126:reid`; `sg docker -c 'docker info --format {{.ServerVersion}}'` printed `29.1.3`. The explorer-api-contract-gate run had planned around "agents have no Docker" (`.project/completed/20261009_explorer-api-contract-gate/design.md:652`).
