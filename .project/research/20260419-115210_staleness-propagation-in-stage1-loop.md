---
date: 2026-04-19T11:52:10-07:00
researcher: Claude
topic: "Staleness propagation inside the stage1 analysis loop — is concept 07 correctly marked stale?"
tags: [research, concept-analysis, pipeline, staleness, bug-investigation]
status: complete
last_updated: 2026-04-19
---

# Research: Staleness Propagation in the Stage1 Analysis Loop

**Date**: 2026-04-19T11:52:10-07:00
**Researcher**: Claude
**Research Type**: Codebase / Pipeline behavior

## Research Question

Concept 07 (MagLIF) is marked `stale` in `exploration/concept_analysis/concept_status.md`. The user believed the model was just updated in the last commit and suspected `manage-concept`'s state method. Another agent claimed the staleness is a structural bug in the loop: `propagate_staleness()` runs at the end of every iteration, clobbering the just-promoted canonical `model_setup.py`.

**Objective:** Establish with 100% confidence whether (a) concept 07 is correctly or incorrectly marked stale, and (b) whether the staleness mechanism has a structural bug.

## Summary

1. **The concept_status.md marking for 07 is factually correct.** Concept 07's `model_setup.py` begins with `# STALE: analysis-updated-iter-9` on disk. That header is the authoritative signal the status generator reads.
2. **The user's premise is wrong.** The last commit (`88b9c6b`) did NOT update 07's `model_setup.py`. Git history shows 07's `model_setup.py` has not been touched since `e5a2cb2` (the pipeline integration commit). The 8 concepts refreshed in `88b9c6b` were 01, 05, 06, 11, 14, 17a, 21, 28 — not 07.
3. **The other agent's structural-bug diagnosis is substantially correct — and slightly worse than stated.** `propagate_staleness()` runs at `loop.py:238` unconditionally on every loop iteration, *after* `_update_canonical_files` has already promoted a clean `iter-N/model_setup.py` to the canonical location. It re-stamps that clean file with `# STALE:` on every iteration, **including the PASS iteration** that exits the loop.
4. **Consequence:** A concept that finished the loop (PASS or FAIL) always ends up with a stale canonical `model_setup.py`, unless the file is overwritten later (e.g., by a manual post-hoc edit or by re-running standalone model-setup with `--force` / after deletion). This is exactly the state 07, 09, 10 are in.
5. **The state-detection method (`get_concept_state`) is correct** — it faithfully reads what's on disk. The *source of the stale marker* is the in-loop staleness propagator, not a false positive in status detection.

## Detailed Findings

### 1. Ground truth for concept 07

The canonical file is stale:

```
exploration/concept_analysis/analyses/07-maglif/model_setup.py:1
    # STALE: analysis-updated-iter-9
```

The iter-N copies are **clean** (no `# STALE:` header):

```
.../07-maglif/iter-9/model_setup.py:1-3
    """MagLIF (D-T) — 1costingfe cost model setup (iter-9)."""
.../07-maglif/iter-8/model_setup.py:1-3
    """MagLIF (D-T) — 1costingfe cost model setup."""
```

Iter-9's `verdict.json` shows `verdict: "FAIL"`, `model_ran: true`, `model_ok: true`. So model-setup produced a clean, valid script in iter-9; the canonical promotion happened; then `propagate_staleness` stamped it.

### 2. User's "we just updated the model in our last commit" claim is incorrect

```bash
git log --all --follow --oneline -- exploration/concept_analysis/analyses/07-maglif/model_setup.py
```
returns only `e5a2cb2`, `46afb62`, `d8cb8ce` — all from before the current branch.

`git show --stat 88b9c6b | grep 07-maglif` — no matches. The commit touched `01, 05, 06, 11, 14, 17a, 21, 28` only. The cross-check with the live files confirms: 01/05 have clean headers (no STALE); 09/10 still carry STALE headers. The concept_status.md table is consistent with this.

### 3. The in-loop sequence (loop.py:107–248)

For each iteration in `run_stage1_loop`, in order:

| Step | Code | Effect |
|------|------|--------|
| Feedback producer | `loop.py:115–178` | Selects cold-start / review / source-integration / research / assess |
| Analyze | `loop.py:181–198` → `_run_cold_start` / `_run_feedback_pass` | Writes `concept_dir/analysis.md` |
| Capture | `loop.py:201` → `_capture_analysis_output` | Writes `iter-N/analysis_output.md` |
| Model-setup | `loop.py:204–207` → `_run_model_in_iteration` | Writes `iter-N/model_setup.py` |
| **Canonical promotion** | `loop.py:210` → `_update_canonical_files` | Copies `iter-N/model_setup.py` → `concept_dir/model_setup.py` **if `model_ok=True`** |
| Assess | `loop.py:222` → `_run_assess` | Writes `iter-N/feedback.md` + verdict |
| Verdict | `loop.py:227–232` → `write_verdict` | Writes `iter-N/verdict.json` |
| Reload | `loop.py:235` | Refreshes loop_state |
| **Staleness** | `loop.py:238` → `propagate_staleness` | Prepends `# STALE: analysis-updated-iter-N` to `concept_dir/model_setup.py` |
| PASS exit | `loop.py:240–241` | `return "PASS"` — but staleness has already run |

### 4. `propagate_staleness` — unconditional stamping

`lib/state.py:59–103`:

```python
def propagate_staleness(concept_id: str, reason: str, analyses_dir=ANALYSES_DIR):
    ...
    for path in downstream:  # model_setup.py, review.md, synthesis.md
        if not path.exists():
            continue
        if path.suffix == ".py":
            text = path.read_text(encoding="utf-8")
            if "# STALE:" not in text:
                text = f"# STALE: {reason}\n" + text
                path.write_text(text, encoding="utf-8")
```

No guard against "model was just promoted this iteration". No short-circuit on `model_ok`. No check whether analysis.md was actually modified during this iteration. If the file exists and is not already stale, it gets stamped.

### 5. The PASS-exit clarification

The other agent wrote: *"The stale marker only clears when a concept exits the loop with PASS and `_update_canonical_files` copies the clean version."* This is **incorrect** about the clearing condition. Reading `loop.py:237–241`:

```python
# --- Propagate staleness ---
propagate_staleness(cid, f"analysis-updated-iter-{iter_num}")

if verdict == "PASS":
    return "PASS"
```

Staleness is stamped **before** the PASS return. So the canonical `model_setup.py` is marked stale even on the final PASS iteration. In practice the stale marker clears only via external overwrites — e.g., the per-account 1GW refresh in commit `88b9c6b` rewrote the file wholesale for 8 concepts, which is why they now show `yes` in the status table.

### 6. Standalone paths

- `cmd_analyze --feedback` (run_analysis.py:456): calls `propagate_staleness("feedback-applied-from-change-requests")` after manually applied changes. **Legitimate** — the analysis was mutated without regenerating downstream artifacts, so marking them stale is correct.
- `cmd_model_setup` (run_analysis.py:467–544): writes directly to canonical `out_dir/"model_setup.py"` via `invoke_claude_validated`. Note: it uses `skip_if_exists=model_path` (line 505), so if the file exists it *skips* — it does not rewrite a stale file. Thus running `analyze model-setup` alone does NOT clear an existing STALE marker unless `--force` is passed (or the file is deleted first).

### 7. Why the "other agent" diagnosis is right in substance

Their structural claim — *"propagate_staleness inside the loop is clobbering work that just happened"* — matches the code exactly:
- iter-N/model_setup.py is generated from the just-updated analysis.md ✓ (`_run_model_in_iteration`)
- The canonical copy is the clean, just-generated version ✓ (`_update_canonical_files` with `model_ok=True`)
- `propagate_staleness` then unconditionally stamps that same canonical file ✓ (`loop.py:238`)

The one correction is that the stale marker **is not cleared even on PASS** — the bug is slightly worse than they described.

## Code References

- `exploration/concept_analysis/scripts/lib/loop.py:55-248` — `run_stage1_loop` main loop
- `exploration/concept_analysis/scripts/lib/loop.py:210` — `_update_canonical_files` call site (clean promotion)
- `exploration/concept_analysis/scripts/lib/loop.py:238` — `propagate_staleness` call site (bug site)
- `exploration/concept_analysis/scripts/lib/loop.py:882-901` — `_update_canonical_files` body
- `exploration/concept_analysis/scripts/lib/state.py:59-103` — `propagate_staleness` body (unconditional stamp)
- `exploration/concept_analysis/scripts/lib/state.py:11-56` — `get_concept_state` (status reader — correct)
- `exploration/concept_analysis/scripts/run_analysis.py:456` — standalone `analyze --feedback` staleness call (legitimate)
- `exploration/concept_analysis/scripts/run_analysis.py:467-544` — `cmd_model_setup` (standalone, uses `skip_if_exists`)

## Architecture Insights

- **Design intent.** `propagate_staleness` was built for the standalone `analyze --feedback` path, where analysis.md is mutated but `model_setup.py` / `review.md` / `synthesis.md` are *not* regenerated. In that flow, stamping downstream as stale is correct.
- **Integration mismatch.** When model-setup was pulled *inside* the loop (FR-6 in the loop.py docstring), the staleness call was apparently ported alongside the analyze step without reconsidering that the in-loop flow already regenerates model_setup.py and promotes it fresh.
- **The model_ok guard** on `_update_canonical_files` was designed to preserve last-known-good state when the model failed mid-loop — but staleness propagation ignores that distinction and stamps regardless.

## Feasibility Assessment

The bug is real, narrowly scoped, and fixable. Options:

1. **Move `propagate_staleness` out of the per-iteration loop.** It serves no purpose inside the loop because `_update_canonical_files` already reflects the current analysis. Run it only from the standalone `--feedback` path.
2. **Skip `model_setup.py` in the in-loop staleness call.** Pass an excludes list so only `review.md` / `synthesis.md` / explorer JSON get stamped (those are NOT regenerated in the loop and legitimately become stale).
3. **Condition on `model_ok`.** If `model_ok=True`, the canonical is fresh — don't stamp it. This is the minimum-surface-area fix.

Option 2 is the cleanest — it preserves the original intent (mark downstream artifacts stale when analysis changes) while recognizing that `model_setup.py` is NOT downstream *within* the loop.

### What this does NOT explain

The `R*` / `S*` markings in concept_status.md also consider `review.md` / `synthesis.md` Stale frontmatter. In-loop staleness propagation affects those too. Stellarator 09 (R*, 9 iters) and MagLIF 07 (R*, 9 iters) likely have STALE on both `model_setup.py` and `review.md`. Any fix should reconsider review/synthesis alongside, since those artifacts really ARE not regenerated in the analyze loop.

## Recommendations

1. **Trust the status table.** It reports ground truth — the file-on-disk state is in fact stale.
2. **Fix the loop bug.** Option 2 above is the surgical fix: when `propagate_staleness` is called from `loop.py:238`, exclude `model_setup.py` (that artifact was just regenerated and promoted).
3. **Before shipping a fix, add a regression test** in `scripts/test_failure_chains.py` asserting that after a PASS iteration in `run_stage1_loop`, `concept_dir / "model_setup.py"` does **not** start with `# STALE:`. The test should run the loop end-to-end with `_fake_claude.py` as a stand-in for Claude.
4. **Clean up existing stale markers** once the bug is fixed: a one-liner for each affected concept, e.g., `sed -i '1{/^# STALE:/d}' exploration/concept_analysis/analyses/07-maglif/model_setup.py` — but only after verifying the current canonical file matches the last iter-N clean copy.
5. **Do not assume the other agent is always wrong.** On this one, their structural diagnosis is accurate; their only error was overstating the clearing case.

## Open Questions

- Should `review.md` / `synthesis.md` be included in the in-loop staleness propagation? They are not regenerated by the loop. If an older `review.md` exists from a prior cycle and the analyze loop runs again, marking them stale is correct. So option 2 (exclude only `model_setup.py`) is right, not option 1 (skip all in-loop staleness).
- `concept 09` also shows `R*` with iter-9. Is its canonical `# STALE: analysis-updated-iter-9` — consistent with the same bug pattern? (Yes — spot-checked: `analyses/09-qi-stellarator-hts/model_setup.py:1 → "# STALE: analysis-updated-iter-9"`.)
- Should the analysis-status doc itself be reworded to make this explicit — e.g., note that "stale" on canonical `model_setup.py` often reflects this known loop-propagation artifact rather than true drift from analysis?
