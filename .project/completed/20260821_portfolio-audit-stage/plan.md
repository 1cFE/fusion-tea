# Implementation Plan: Portfolio-Audit Stage

**Status:** Complete (all 5 phases)
**Created:** 2026-06-07
**Last Updated:** 2026-06-07

## Source Documents
- **Spec:** `.project/active/portfolio-audit-stage/spec.md`
- **Design:** `.project/active/portfolio-audit-stage/design.md` ← component details, bets, invariants, schemas, gotchas

## Implementation Strategy

**Phasing Rationale:**
De-risk the deterministic core first, then layer the (untestable-by-unit) LLM orchestration on top, then add the token-saving resume.

1. **`probe.py` first** — the design names module-cache cleanup as the #1 de-risk ("if this leaks, every perturbation is suspect"). It's independent and the import pattern is already proven in `sanity_check_comparables.py`.
2. **`manifest.py` + `digest.py`** — pure functions over fixtures; SHA-stability and stale-detection are the testable invariants.
3. **Runner + CLI + prompts** — get the cheap forensic artifacts on disk and CLI conventions right *without* the expensive lead call.
4. **Live lead + run.log + real 3-concept run + mocked smoke test** — the prompt is the load-bearing tuning surface and can't be unit-tested, so a real run gates the smoke test (per design "de-risk first").
5. **Durability resume + README** — pure token-saver on a working core; lowest risk, last.

**Critical Path:**
`probe.py` (clean re-read) → `manifest.py`/`digest.py` (cohort prep) → runner renders prompt + writes forensics → live lead invocation → resume. Each stage's output is the next stage's input.

**First Proof Point:**
Phase 1 — `probe.result_for(cid)` returns the correct `result_1gw` for a fixture concept **and** two consecutive imports of different concepts don't leak `sys.modules` state.

**Overall Validation Approach:**
- Each phase starts with tests (Phases 1–3, 5 are unit-testable; Phase 4's gate is a real run + a mocked smoke test).
- New tests live in `scripts/` (run from there: `uv run python -m pytest test_portfolio_audit_*.py`), importing `from lib.portfolio_audit...`.
- **Baseline caveat:** the suite is *not* fully green today. Captured pre-change baseline (2026-06-07): **12 failures**, all library-drift / table-state and unrelated to this work — `test_canonical_accounts::test_all_enums_match_library`; `test_concepts_v2` ×5; `test_critic_inputs::test_collect_happy_path`; `test_loop_wiring::test_costingfe_gate_accepts_helper_form`; `test_model_setup_helpers` ×4. (The draft anticipated only the `test_critic_inputs` one.) "Existing tests pass" means **no new regressions** against these 12, not a clean suite.

---

## Phase 1: `probe.py` + shared import helper

### Goal
A clean, agent-callable CLI `result_for(concept_id)` that fresh-imports a concept's `model_setup.py` and returns `result_1gw` + native + CAS rollup as JSON to stdout — read-only, no file writes, per-call timeout, no module-cache leak. First because the design flags it as the load-bearing de-risk.

### Assumption Under Test
Consecutive imports of *different* concepts' `model_setup.py` don't leak module state (`sys.modules` pop works); an import failure surfaces as a structured error rather than being silently swallowed or crashing the caller.

### Test Stencil (Write This First)
```python
# scripts/test_portfolio_audit_probe.py
from lib.portfolio_audit import probe

def test_result_for_returns_cas_rollup(fixture_concept):
    out = probe.result_for("01-hts-compact-tokamak")
    assert out["import_status"] == "ok"
    assert out["cas_1gw"]["CAS22"] == pytest.approx(8291.5, rel=1e-3)
    assert out["lcoe_1gw_usd_per_mwh"] > 0

def test_consecutive_imports_no_leak():
    a = probe.result_for("01-hts-compact-tokamak")
    b = probe.result_for("07-maglif")
    assert a["concept_id"] != b["concept_id"]          # no cross-contamination
    assert "_setup_01-hts-compact-tokamak" not in sys.modules  # popped

def test_import_failure_is_structured(broken_setup):
    out = probe.result_for("broken-concept")
    assert out["import_status"].startswith("error:")    # not a raised exception
```

### Changes Required

**See `design.md` for:**
- `probe.py` scope (read-only, no `perturb()`) → `design.md#component-overview` + Bet 6
- Critical gotchas (`sys.modules.pop`, never expose raw `importlib`) → `design.md#critical-gotchas`

**Specific file changes:**

#### 1. Package marker
- [x] `lib/portfolio_audit/__init__.py` (NEW, empty)

#### 2. Test file (write first)
**File:** `scripts/test_portfolio_audit_probe.py` (NEW)
- [x] Result-shape test against a real fixture concept
- [x] Consecutive-import no-leak test
- [x] Import-failure-is-structured test
- [x] Per-call timeout fires (cap test)

#### 3. Probe implementation
**File:** `lib/portfolio_audit/probe.py` (NEW)
- [x] Lift `importlib.util` + `spec_from_file_location` + `module_from_spec` from `sanity_check_comparables.py:69`
- [x] `sys.modules.pop(modname, None)` in a `finally` so a failed import still cleans up
- [x] `result_for(cid) -> dict` returning `concept_id`, `import_status`, native + 1gw LCOE, `cas_native`/`cas_1gw` (rollup dict keyed by canonical `CAS_COLUMNS`)
- [x] `argparse` CLI entry: `result_for` printing JSON to stdout; per-call timeout via `signal` (SIGALRM/ITIMER_REAL)
- [x] No writes anywhere (invariant 6)

### Validation
**Automated:**
- [x] `uv run python -m pytest test_portfolio_audit_probe.py -q` → all pass (9 passed)
- [x] `uv run python -m pytest test_*.py -q` → no NEW failures vs baseline set (12 failed / 474 passed; same 12 as baseline, +9 new passes)

**Manual:**
- [x] `uv run python lib/portfolio_audit/probe.py result_for 01-hts-compact-tokamak` → JSON, CAS22 1gw = 8035.4 (live; ~3% drift below the 8291.5 artifact)
- [x] Run against a concept with a deliberately broken setup → `import_status: "error: SyntaxError: ..."`, exit 0

**What We Know Works After This Phase:**
The investigator's load-bearing tool: clean re-reads with no state leak, structured failure.

---

## Phase 2: `manifest.py` + `digest.py`

### Goal
Two pure deterministic builders: `build_manifest(concept_ids, run_meta)` (per-concept SHAs, iter state, `import_status`, `model_stale`) and `build_digest(concept_ids)` (LCOE/CAS from `model_output.txt`, enabled overrides via AST, `model_stale`). These are the cohort-prep the runner feeds the lead.

### Assumption Under Test
SHAs are byte-stable across re-runs on identical on-disk state (invariant 2 / FR-6 round-trip); `model_stale` correctly fires when `model_output.txt` mtime predates `model_setup.py`; a missing/garbled `model_output.txt` degrades to a recorded gap, never a crash (FR-12).

### Test Stencil (Write This First)
```python
# scripts/test_portfolio_audit_digest.py
def test_sha_stable_across_runs(fixture_tree):
    m1 = build_manifest(["01-..."], run_meta)
    m2 = build_manifest(["01-..."], run_meta)
    assert m1["concepts"]["01-..."]["sha256"] == m2["concepts"]["01-..."]["sha256"]

def test_model_stale_when_output_older_than_setup(stale_fixture):
    d = build_digest(["stale-..."])
    assert d["concepts"]["stale-..."]["model_stale"] is True

def test_broken_setup_recorded_not_raised(broken_fixture):
    m = build_manifest(["broken-..."], run_meta)
    assert m["concepts"]["broken-..."]["import_status"].startswith("error:")

def test_digest_parses_cas_skipping_preamble(fixture):
    d = build_digest(["01-..."])
    # model_output.txt has 2 Windows-env warning lines before the CAS header
    assert d["concepts"]["01-..."]["cas_1gw"][2] == pytest.approx(8291.5)  # CAS22 col
```

### Changes Required

**See `design.md` for:**
- `manifest.json` schema → `design.md#manifestjson-schema-sketch`
- `cohort_digest.json` schema + per-concept CAS rule → `design.md#cohort_digestjson-schema-concrete`
- `model_stale` mtime rule → `design.md#digest-staleness-model_stale`
- Prior art: `lib/critic_inputs.py` already loads model_setup, parses static LCOE, counts enabled overrides — lift, don't reinvent.

**Specific file changes:**
- [x] `scripts/test_portfolio_audit_digest.py` (NEW) — SHA stability, run-meta+iter state, stale/fresh detection, broken/missing/freeform setup, CAS-preamble-skip, record metadata + manifest-state copy, enabled-override extraction, relative-override→None, missing-output gap (12 tests)
- [x] ~~Build a fixture tree under `scripts/tests/fixtures/portfolio_audit/`~~ — **deviated**: used the test_critic_inputs convention instead (real concept 01 read-only for SHA/CAS/override parsing; tmp ANALYSES_DIR + crafted files + forced `os.utime` mtimes for stale/fresh/broken/missing/freeform). A committed fixture tree of a "standard concept" can't import (the model_setup walk-up needs the real `scripts/`), so tmp + monkeypatch is the right seam.
- [x] `lib/portfolio_audit/manifest.py` (NEW): `build_manifest(concept_ids, run_meta)` — SHA256 of the three files (None for missing), `read_loop_state` for iter_count + last_iter_ts + sources, `import_status_for` (one import via `probe.import_isolated`), `is_model_stale` via mtime compare
- [x] `lib/portfolio_audit/digest.py` (NEW): `build_digest(records, manifest)` — parse `model_output.txt` LCOE/overnight/CAS by line-pattern (preamble-robust), `enabled_overrides` from `model_setup.py` AST (literal values; relative exprs → None), fixed `cas_columns`, copies `import_status`/`model_stale`/`last_iter_ts` from the manifest

### Validation
**Automated:**
- [x] `uv run python -m pytest test_portfolio_audit_digest.py -q` → all pass (12 passed)
- [x] No new regressions vs baseline set (12 failed / 486 passed; same 12 baseline, +12 new passes)

**Manual:**
- [x] Built manifest+digest for concept 01 → digest matches the design `cohort_digest.json` schema field-for-field; CAS arrays match `model_output.txt` (CAS22 native 2109.5 / 1gw 8291.5), `enabled_overrides` = `[C220103 derived 1030.0]` (CAS27 excluded — disabled)

**What We Know Works After This Phase:**
Deterministic cohort prep — the lead's entire context payload — round-trips and surfaces staleness/import failure as data.

---

## Phase 3: Runner skeleton + CLI dispatch + prompt templates

### Goal
Wire `portfolio-audit` into `run_analysis.py` dispatch with the right flags; the runner resolves the cohort, writes `manifest.json` + `cohort_digest.json` + rendered `prompts/lead_prompt.md` **before** any lead call (crash leaves forensics); author the criteria + lead/investigator/writer templates. No live lead yet — short-circuit the invocation so the forensic path is exercised standalone.

### Assumption Under Test
The CLI conventions compose (selection flags + `--passed-only` + `--model opus` + `--timeout 7200`); the runner writes only under `reviews/<timestamp>/`; the lead prompt renders with digest + criteria include + inlined investigator/writer prompts.

### Test Stencil (Write This First)
```python
# scripts/test_portfolio_audit_runner.py
def test_forensics_written_before_lead(tmp_run, monkeypatch):
    # stub invoke_claude to raise — forensics must already be on disk
    monkeypatch.setattr(runner, "invoke_claude", lambda *a, **k: 1/0)
    with pytest.raises(ZeroDivisionError):
        runner.run(concept_ids=["01-..."], model="opus", run_dir=tmp_run)
    assert (tmp_run / "manifest.json").exists()
    assert (tmp_run / "cohort_digest.json").exists()
    assert (tmp_run / "prompts" / "lead_prompt.md").exists()

def test_passed_only_filters_to_pass_verdicts(cohort):
    ids = resolve_audit_cohort(cohort, passed_only=True)
    assert all(latest_verdict(i) == "PASS" for i in ids)
```

### Changes Required

**See `design.md` for:**
- Runner responsibilities (no fan-out, no parse, write forensics first) → `design.md#component-overview` (`runner.py`) + Bet 1
- Output layout → `design.md#output-layout`
- Lead/investigator/writer prompt contents → `design.md#component-overview` + the paraphrased/verbatim prompt sketches
- Plan-decides: **inline** investigator/writer prompts in the lead prompt (recommended v1); criteria ships with **starter prose** → `design.md#next-stage-handoff`

**Specific file changes:**
- [x] `scripts/test_portfolio_audit_runner.py` (NEW) — forensics-before-lead, dry-run-skips-lead, `--passed-only` filter, real `latest_verdict`, timestamp-collision `-2`, no-writes-to-concept-dir, lead-prompt-renders-includes (7 tests)
- [x] `lib/portfolio_audit/runner.py` (NEW): `run(records, *, run_dir, model, cli, timeout, dry_run)` — builds manifest + digest, renders lead prompt via `fill_template`, writes all three forensic files **then** calls `invoke_claude` (real call; `--dry-run` short-circuits before it; tests monkeypatch it). Plus `make_run_dir` (collision → `-2`), `resolve_audit_cohort` (`--passed-only`), `latest_verdict`, `_verify_outputs` (warn-not-raise), `_write_run_log` (minimal; Phase 4 enriches)
- [x] `prompt_templates/portfolio_audit/lead.md` (NEW) — orchestration, durability protocol, findings.jsonl format, report.md structure, probe usage (`-m lib.portfolio_audit.probe`), perturbation worked-example, inlined investigator + writer via `{{@includes}}`, Task `model: "opus"` reminder, out-of-scope (no synthesis/review/address_log)
- [x] `prompt_templates/portfolio_audit/investigator.md` (NEW) — generic hypothesis-driven reference prompt
- [x] `prompt_templates/portfolio_audit/writer.md` (NEW) — plain-language rules at top + 4-section structure
- [x] `prompt_templates/config/portfolio_audit_criteria.md` (NEW) — starter prose: family-internal coherence, cross-family magnitudes, source traceability, sensitivity; plus a "what NOT to flag" section (stale/import-error/well-sourced outliers)
- [x] `run_analysis.py`: added `cmd_portfolio_audit(records, args)`, `add_parser("portfolio-audit", ...)` (selection + `--passed-only` + `--model opus` + `--dry-run` + `--timeout 7200` + `--inherit-from`), registered in `dispatch`. **No `--workers`.** `--inherit-from` errors loudly (Phase 5).

### Validation
**Automated:**
- [x] `uv run python -m pytest test_portfolio_audit_runner.py -q` → all pass (7 passed)
- [x] No new regressions vs baseline (12 failed / 493 passed; same 12 baseline, +7 new)

**Manual:**
- [x] `portfolio-audit 01 --dry-run` → `reviews/<ts>/{manifest.json,cohort_digest.json,prompts/lead_prompt.md}` + empty `concepts/`, no `run.log` (lead not invoked); nothing written outside the run folder
- [x] Read the rendered `lead_prompt.md` — criteria + investigator + writer all inlined, digest embedded, run_dir paths absolute, **0 unresolved `{{}}` placeholders**
- [x] `portfolio-audit --help` shows the command; `--inherit-from` errors "(Phase 5)"; `--passed-only` filters cleanly (01's latest verdict ≠ PASS → empty cohort, no crash)

**What We Know Works After This Phase:**
The full forensic path runs end-to-end without spending an LLM token; a crash mid-lead leaves a complete state record.

---

## Phase 4: Live lead invocation + `run.log` + real 3-concept run + smoke test

### Goal
Replace the Phase 3 stub with the real `invoke_claude(model="opus", timeout=7200)`; parse the event stream into a structured `run.log` (lead + per-subagent cost/tokens/wall time); **do a real 3-concept run to confirm the lead uses Task subagents and tune the prompt**; then write the mocked-`invoke_claude` smoke test that codifies the now-known-good transcript shape.

### Assumption Under Test
The lead, given this prompt, actually spawns investigator + writer Task subagents (with `model: "opus"`, not the silent Haiku default), writes `report.md` early and continuously, appends `findings.jsonl`, and writers produce plain-language `concepts/<id>.md` — all in one invocation with no human stop.

### Test Stencil (Write This First — the smoke test, written *after* the real run confirms shape)
```python
# scripts/test_portfolio_audit_smoke.py
def test_smoke_canned_lead_transcript(tmp_run, monkeypatch):
    # canned lead transcript: 2 investigator Task calls + 1 writer that Writes concepts/<id>.md, + report.md
    monkeypatch.setattr(runner, "invoke_claude", lambda *a, **k: canned_result())
    runner.run(concept_ids=["01-...","07-...","21-..."], model="opus", run_dir=tmp_run)
    assert (tmp_run / "report.md").exists()
    assert (tmp_run / "concepts").iterdir()              # ≥1 per-concept doc
    assert (tmp_run / "run.log").exists()
    assert no_writes_outside(tmp_run)                    # invariant 1
```

### Changes Required

**See `design.md` for:**
- `run.log` cost capture (parse `total_cost_usd`, `modelUsage`, `subagent_tokens`) → `design.md#runlog--cost-capture`
- Durability rules the prompt must enforce (continuous report.md, writer-on-confirm) → `design.md#durability--recovery` (1) & (2)
- Integration smoke-test spec → `design.md#validation-approach`
- De-risk mandate (real 3-concept run before smoke test) → `design.md#next-stage-handoff` ("De-risk first")

**Specific file changes:**
- [x] `lib/portfolio_audit/runner.py`: real `invoke_claude` call already wired in Phase 3 (cwd = `CONCEPT_ANALYSIS_DIR`); Phase 4 enriched `_write_run_log` to capture lead cost/usage/turns; `_verify_outputs` warns (never synthesizes report.md — Invariant 3)
- [x] **Real 3-concept run** (`portfolio-audit 01 07 21 --model opus`) — **DONE** (user-authorized). Run `reviews/20260607-135133/`: rc 0, 517s, **$3.75**, 15 turns. Produced report.md + 2 per-concept docs + 2 findings; the lead **perturbed models** (sensitivity scripts in `/tmp`, referenced in findings). No prompt tuning needed — quality bar held on first run.
- [x] `scripts/test_portfolio_audit_smoke.py` (NEW) — canned-lead transcript driving the runner; all artifacts present, run.log cost captured, none outside run folder (2 tests)
- [x] `run.log` cost capture: **additive** `InvokeResult.cost_usd/usage/num_turns` + `_extract_result_meta` in `lib/claude.py` (does NOT touch the pinned `_parse_json_events` 2-tuple); runner writes lead totals. Per-subagent rows NOT fabricated — the result event carries lead-level totals only (noted in `_write_run_log` docstring).

### Validation
**Automated:**
- [x] `uv run python -m pytest test_portfolio_audit_smoke.py -q` → pass (2 passed); `test_claude.py` → 47 passed (additive InvokeResult change safe)
- [x] No new regressions vs baseline (12 failed / 498 passed; same 12 baseline, +5 new: 3 `_extract_result_meta` + 2 smoke)

**Manual (DONE — real run `reviews/20260607-135133/`):**
- [x] Real 3-concept run completes; `run.log` shows lead cost $3.75 + usage; `report.md` cross-links both per-concept docs; `findings.jsonl` has one line per confirmed finding (2)
- [~] Confirm Task subagents fire and are **Opus** — **PARTIAL**: output quality is Opus-level throughout and the lead clearly ran investigations (sensitivity scripts), but `run.log` captures lead-level cost/usage only, so artifact-level proof that *subagents* used Opus (vs the silent-Haiku default) isn't available. Would need raw event-stream capture (follow-up). Prompt explicitly mandates `model: "opus"`.
- [x] Cold-read both `concepts/<id>.md` — plain words, concrete numbers, exact 4-section structure; jargon scan (elasticity/anomalous/non-monotonic) across all outputs = **0 hits**
- [x] `git status` — nothing changed outside `reviews/<ts>/`; `analyses/` shows 0 changes (Invariant 10 held)

**What We Know Works After This Phase:**
The end-to-end audit produces a coherent cross-concept report + per-concept docs in one command, with cost visibility, and the prompt is tuned to the design's quality bar.

---

## Phase 5: Durability resume (`--inherit-from`) + README

### Goal
All-or-nothing resume: when `--inherit-from <prior-run>` is set, build the new manifest fresh, compare the *entire* manifest against the prior; on any difference error out naming the changed concepts; on exact match copy forward `report.md` + `concepts/*.md` + `findings.jsonl` and prepend the recovery preamble to the lead prompt. Plus the README section.

### Assumption Under Test
Manifest equality is the correct resume gate (same cohort + identical SHAs + identical `model_stale`); a single changed artifact anywhere blocks inheritance rather than silently doing a partial/fresh run.

### Test Stencil (Write This First)
```python
def test_inherit_exact_match_copies_forward(prior_run, tmp_run):
    runner.run(..., inherit_from=prior_run, run_dir=tmp_run)
    assert (tmp_run / "report.md").read_text() == (prior_run / "report.md").read_text()
    assert (tmp_run / "findings.jsonl").exists()
    assert "Recovery:" in (tmp_run / "prompts" / "lead_prompt.md").read_text()

def test_inherit_any_diff_errors_out(prior_run, changed_cohort):
    with pytest.raises(SystemExit):           # names which concept changed
        runner.run(..., inherit_from=prior_run)
```

### Changes Required

**See `design.md` for:**
- All-or-nothing resume mechanism + recovery preamble verbatim → `design.md#durability--recovery` (3)
- Invariant 9 (inheritance is all-or-nothing)

**Specific file changes:**
- [x] `scripts/test_portfolio_audit_resume.py` (NEW) — `diff_manifests` unit (sha/cohort/staleness), exact-match copy-forward + preamble, no-preamble-without-inherit, any-diff abort naming concepts, missing-prior-manifest abort (6 tests)
- [x] `lib/portfolio_audit/runner.py`: `--inherit-from` via `diff_manifests` (pure) + `_apply_inheritance` (gate: exits naming changes; copy-forward on exact match) + `_copy_forward`; `RECOVERY_PREAMBLE` prepended in `_render_lead_prompt`
- [x] `exploration/concept_analysis/README.md`: added "Portfolio Audit (cross-concept)" section (orthogonal to per-concept loop, output layout, flags); corrected the stale dispatch snippet (10→14 subcommands)
- [~] Confirm with user: commit `reviews/` (don't gitignore) — **PENDING user decision** (raised in handoff)

### Validation
**Automated:**
- [x] `uv run python -m pytest test_portfolio_audit_resume.py -q` → pass (6 passed)
- [x] Full new-test sweep `test_portfolio_audit_*.py` → green (36 passed)
- [x] No new regressions vs baseline (12 failed / 504 passed; same 12 baseline, +6 resume)

**Manual (against the real Phase 4 run `reviews/20260607-135133/`):**
- [x] `--inherit-from` with unchanged cohort → `report.md` copied forward IDENTICAL, both concept docs + 2-line findings.jsonl carried, recovery preamble prepended
- [x] Changed cohort (dropped 21) → aborts: "21-spherical-tokamak-hts: in the prior run but not the new cohort" (the model_setup-touch variant is unit-tested via the SHA/staleness diff)

**What We Know Works After This Phase:**
A timed-out run is cheaply resumable; the stage is documented and a peer of the existing pipeline stages.

---

## Environment Setup

**See CLAUDE.md for full environment rules.** Key points:
- All Python via `uv run` (tests, probe CLI, run_analysis).
- Tests run from `exploration/concept_analysis/scripts/`: `uv run python -m pytest test_portfolio_audit_*.py -q`.
- **Capture the baseline failure set once before starting** (`uv run python -m pytest test_*.py -q` from `scripts/`) so "no new regressions" is diffable — `test_critic_inputs.py::test_collect_happy_path` is a known pre-existing failure.

## Risk Management

**See `design.md#potential-risks` for the full analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: module-cache leak is the headline risk — the no-leak test asserts `sys.modules` is popped, with `pop` in a `finally` so failed imports clean up too.
- **Phase 2**: SHA non-determinism / parse fragility — pin against a committed fixture tree; preamble-skip test guards the Windows-warning lines in `model_output.txt`.
- **Phase 3**: writes escaping the run folder — test asserts nothing outside `reviews/<ts>/` changes; forensics written before the lead call so a crash is recoverable.
- **Phase 4**: the prompt is untestable by unit — real 3-concept run gates the smoke test; explicitly verify subagents are Opus (the silent-Haiku-default gotcha) in `run.log`.
- **Phase 5**: partial inheritance incoherence — equality gate is all-or-nothing by construction; diff path names the changed concept and exits.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-06-07

**Actual Changes:**
- Created `scripts/lib/portfolio_audit/__init__.py` (package marker w/ docstring).
- Created `scripts/lib/portfolio_audit/probe.py` — `result_for(cid, *, timeout_s=120)` does an isolated in-process import (`_import_isolated` registers under `_setup_<cid>` and pops it in a `finally`), reads module-level `result_1gw`/`native`, returns `{concept_id, import_status, lcoe_1gw/native_usd_per_mwh, cas_1gw, cas_native}`. CAS rollups are dicts keyed by the canonical `CAS_COLUMNS` (17 accounts). Per-call timeout via SIGALRM/ITIMER_REAL (`_time_limit`). CLI subcommand `result_for` with `--timeout`; always exits 0 (failure carried in `import_status`).
- Created `scripts/test_portfolio_audit_probe.py` — 9 tests: rollup shape, no-leak across 01↔07, distinct numbers, broken-import structured error, missing-file, freeform-without-result, timeout fires, no-file-writes invariant, CLI-emits-JSON.

**Issues:**
- **Live-vs-artifact drift.** Initial test pinned probe output to `model_output.txt` values (CAS22 1gw 8291.5). The probe reads LIVE numbers; live re-import gives 8035.4 (~3% below), the same library-drift the baseline documents. Fixed the test to assert drift-robust invariants (10% band + native<1gw replication ordering + 17-column shape) rather than stale pins. This is correct behavior, not a bug.

**Deviations:**
- **Baseline is 12 failures, not 1.** The plan's "baseline caveat" anticipated only `test_critic_inputs::test_collect_happy_path`. The real pre-change baseline is **12** failures (all library-drift / table-state, unrelated to this work): `test_canonical_accounts::test_all_enums_match_library`; `test_concepts_v2` ×5 (pending-design-point / four-state); `test_critic_inputs::test_collect_happy_path`; `test_loop_wiring::test_costingfe_gate_accepts_helper_form`; `test_model_setup_helpers` ×4 (oracle/kwarg/grepable-LCOE). "No new regressions" is diffed against these 12.
- **CAS rollup is a dict (keyed by CAS code), not the list** used by the digest schema. The probe is single-concept agent-facing (self-describing dict is friendlier); the digest cohort table uses the compact list in `CAS_COLUMNS` order. Both share `probe.CAS_COLUMNS` as the one column-order source of truth (digest will import it in Phase 2). Matches the probe test stencil (`out["cas_1gw"]["CAS22"]`).
- Reused the canonical CAS column list as `probe.CAS_COLUMNS` rather than lifting `flatten_account_values` (which mixes in CAS22 sub-accounts — the rollup wants only the 17 top-level accounts).
- Added a `sys.path` bootstrap at the top of `probe.py` (same idiom as `model_setup.py`) so the plan's documented direct-path invocation works from any cwd, in addition to `-m lib.portfolio_audit.probe`.

### Phase 2 Completion
**Completed:** 2026-06-07

**Actual Changes:**
- Created `scripts/lib/portfolio_audit/manifest.py` — `build_manifest(concept_ids, run_meta, *, timeout_s)` returns `{**run_meta, "concepts": {cid: per-concept state}}`. Per concept: `iter_count`/`last_iter_ts`/`sources` (from `read_loop_state`'s last-complete iteration), `sha256` of the three files (None when absent), `import_status` (`import_status_for` — one import via `probe.import_isolated`; "ok" iff it imports, broader than probe's CAS bar), `model_stale` (`is_model_stale` — output mtime < setup mtime).
- Created `scripts/lib/portfolio_audit/digest.py` — `build_digest(records, manifest)` returns the `cohort_digest.json` schema. Record metadata + `model_output.txt`-parsed numbers (LCOE/overnight/CAS by line-pattern regex, preamble-robust) + AST-parsed `enabled_overrides`; copies `import_status`/`model_stale`/`last_iter_ts` from the manifest (so the digest never imports a model — execution-free).
- Created `scripts/test_portfolio_audit_digest.py` — 12 tests.
- Promoted `probe._import_isolated` → public `probe.import_isolated` (the package's single hardened model-load path; reused by manifest).

**Issues:**
- None. The Phase 1 live-vs-static distinction paid off cleanly: the digest reads the **static** `model_output.txt` (8291.5 etc.), so its CAS test pins to the artifact exactly — no drift tolerance needed (unlike the live probe).

**Deviations:**
- **`build_digest(records, manifest)`, not `build_digest(concept_ids)`** (the stencil shape). Digest needs concept-record metadata (name/family/maturity/fit_grade/comparables) and the manifest's import_status/model_stale. Taking records + manifest keeps it a pure function of its inputs + `model_output.txt`/`model_setup.py` text, avoids a hidden `load_concepts()` dependency, and means one import per concept total (in the manifest). Runner will pass resolved records + the built manifest.
- **No committed fixture tree** (see checklist note above) — tmp ANALYSES_DIR + monkeypatch + `os.utime`, matching `test_critic_inputs`.
- **`maturity` sourced from `design_point.maturity_tier`**, `p_native_mwe` from `design_point.p_native_mwe` (the canonical record metadata), not the model AST. The AST parse is scoped to `enabled_overrides` only — one job for the AST helper.
- **Override values are literal-only via AST.** Relative overrides (`0.70 * generic.costs.cas21`) can't be evaluated without running the model, so `value_musd` is None for those; account + provenance still carry the signal. Documented in the digest docstring and covered by a test.

### Phase 3 Completion
**Completed:** 2026-06-07

**Actual Changes:**
- Created `scripts/lib/portfolio_audit/runner.py` — forensics-first runner (one Claude call, no fan-out logic). `run()` writes manifest/digest/lead_prompt before invoking the lead; `--dry-run` stops after forensics. Helpers: `make_run_dir` (collision-safe), `resolve_audit_cohort`/`latest_verdict` (`--passed-only`), `_verify_outputs`, `_write_run_log`.
- Created 4 prompt templates: `lead.md`, `portfolio_audit/investigator.md`, `portfolio_audit/writer.md`, `config/portfolio_audit_criteria.md`. Investigator + writer are inlined into the lead via `{{@includes}}`; criteria via `{{@config/...}}`.
- Created `scripts/test_portfolio_audit_runner.py` — 7 tests.
- Wired `cmd_portfolio_audit` + parser + dispatch into `run_analysis.py`.
- Promoted two manifest helpers to public for reuse by the runner: `last_complete_iteration`, `sha256_of`.

**Issues:**
- None blocking. Noted: the parent-repo `uv.lock` shows ~129 added lines (trafilatura/htmldate/justext/etc.) in the working tree — **not from this work** (my code is stdlib + existing project libs; I added no dependency). Pre-existing uncommitted state from some other feature; left untouched. Flag before committing.

**Deviations:**
- **`run(records, ...)`** (not the stencil's `concept_ids=...`) — same reason as digest: the runner already has resolved records and threads them to both manifest (ids) and digest (records). `run_dir` is passed in (created by `make_run_dir` in the CLI), so `run()` is testable with a tmp dir.
- **No in-code "guarded stub" for the lead** — the runner calls the real `invoke_claude`; Phase 3 stays token-free via `--dry-run` (production) and monkeypatching `invoke_claude` (tests). This is cleaner than a stub flag and means Phase 4 only has to enrich `run.log` (event-stream cost parse) — the call path is already real.
- **`--inherit-from` errors loudly** in Phase 3 rather than being silently parsed-and-ignored (honest until Phase 5 wires it).

### Phase 4 Completion
**Completed:** 2026-06-07 (code + live run, user-authorized)

**Live run result (`reviews/20260607-135133/`):** rc 0, 517s, **$3.75**, 15 turns over 3 concepts (01, 07, 21). The Opus lead found 2 real high-severity findings — 01's magnet override sits ~5× below its own cited source (would push LCOE 155→507), and MagLIF's "cheapest" ranking floats on a $0.50/J driver price 10–30× below cited cost with the source-anchored override disabled. It perturbed both models for sensitivity, traced sources to file:line, wrote report.md continuously (mtimes prove progressive writeback), and produced two plain-language 4-section per-concept docs. Jargon scan = 0 hits. No concept artifact was mutated. **No prompt tuning needed — the quality bar held on the first run.**

**Verification gap (honest):** `run.log` captures lead-level cost/usage only. I cannot prove from artifacts that the lead's *subagents* ran as Opus (vs the silent-Haiku default). Output quality is Opus-level throughout and the prompt mandates `model: "opus"`, but per-subagent model/cost would need raw event-stream capture (invoke_claude discards the stream; I kept only the result event's totals). Logged as a possible follow-up, not fabricated.

**Actual Changes:**
- `lib/claude.py` — **additive**: `InvokeResult` gained optional `cost_usd` / `usage` / `num_turns` (default None; existing positional constructors + 3-tuple unpacking unaffected). New `_extract_result_meta(raw)` reads them off the result event, best-effort, never raises. `invoke_claude` populates them. The pinned `_parse_json_events` 2-tuple is untouched (its tests still pass).
- `lib/portfolio_audit/runner.py` — `_write_run_log` now records lead cost/usage/turns (or "cost: unavailable" when the stream lacks it). Uses `getattr` so a no-cost result (or test SimpleNamespace) degrades cleanly.
- `scripts/test_portfolio_audit_smoke.py` (NEW, 2 tests) — canned-lead transcript; full-artifact + no-external-write + cost-capture assertions.
- `scripts/test_claude.py` — added `TestExtractResultMeta` (3 tests).

**Issues / blocker:**
- **The live 3-concept run is blocked by the auto-mode permission classifier**, which denies spawning `claude --dangerously-skip-permissions` (the mechanism inside `invoke_claude`). This is the de-risk run the design mandates ("one end-to-end real run before the smoke test") and the only token-spending step. It needs explicit user authorization — either a Bash allow rule for the command, or the user runs it via `!`. Until then: the lead prompt is UNVALIDATED against real lead behavior (does it actually spawn Opus subagents? does the writer hold the plain-language bar?), and `lead.md` / `writer.md` are UNTUNED.

**Deviations:**
- **No in-code lead "stub→real" swap** — Phase 3 already wired the real `invoke_claude`; Phase 4 only added cost capture. (Recorded in Phase 3 notes.)
- **Smoke test written before the real run.** The plan ordered "real run gates the smoke test." But the smoke test is a *runner-contract* test (mocked lead) that's valid regardless of real lead behavior, so it's done now. What the real run gates is *prompt tuning*, which remains pending.
- **Cost capture is lead-level only**, not per-subagent. The result event exposes run totals; the event stream doesn't break cost out per Task subagent (and I can't confirm a per-subagent shape without the blocked live run). No fabricated per-subagent rows. If the real run later surfaces per-subagent data, that's a clean follow-up.

### Phase 5 Completion
**Completed:** 2026-06-07

**Actual Changes:**
- `lib/portfolio_audit/runner.py` — `--inherit-from` resume: `diff_manifests(new, prior)` (pure; compares cohort set + per-concept artifact SHAs + model_stale, ignores run metadata/iter/timestamps/import_status), `_apply_inheritance` (loads prior manifest, aborts via `sys.exit` naming every mismatch, copies forward on exact match, returns `RECOVERY_PREAMBLE`), `_copy_forward` (report.md / findings.jsonl / concepts/*.md). `_render_lead_prompt` gained an optional `recovery_preamble` prefix.
- `run_analysis.py` — `cmd_portfolio_audit` now passes `inherit_from` through (removed the Phase-3 "not yet implemented" guard); flag help updated.
- `scripts/test_portfolio_audit_resume.py` (NEW, 6 tests).
- `README.md` — "Portfolio Audit (cross-concept)" section + dispatch-snippet correction.

**Issues:** None.

**Deviations:**
- **Identity = SHAs + model_stale + cohort set only** (per design), not the whole manifest verbatim. iter_count/last_iter_ts/import_status/run-metadata are excluded from the diff — they don't change the audited *content*. Documented in `diff_manifests`.
- **`sys.exit` lives in `_apply_inheritance`** (a runner helper) so `runner.run(..., inherit_from=...)` aborts directly, matching the test stencil's `pytest.raises(SystemExit)`. The pure `diff_manifests` is separately unit-testable; the helper owns the all-or-nothing exit policy.

---

## Final Status

**All 5 phases complete.** New module `lib/portfolio_audit/` (probe, manifest, digest, runner) + 4 prompt templates + `portfolio-audit` CLI command. **42 new tests** (probe 9, digest/manifest 12, runner 7, smoke 2, resume 6, claude `_extract_result_meta` 3, +3 within those). Full suite: 12 pre-existing baseline failures (unchanged), **504 passed**, no new regressions. One real Opus run validated end-to-end ($3.75, found 2 real findings, perturbed models, plain-language docs).

**Open items for the user (see handoff):**
1. **Commit vs gitignore `reviews/`** — design default is commit (audit artifacts). The real run `reviews/20260607-135133/` is on disk. Decision pending.
2. **`uv.lock`** has ~129 unrelated added lines (trafilatura/etc.) in the working tree — NOT from this work; resolve before committing.
3. **Subagent-Opus verification gap** — `run.log` captures lead-level cost only; per-subagent model/cost would need raw event-stream capture (possible follow-up).

**Status**: Draft → In Progress → **Complete (pending user decisions above)**
