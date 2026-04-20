# Design: Staleness Propagation Fix

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-19 12:07 PDT
**Branch:** fix/stale-tracker
**Commit (at design):** 8c3580c

---

## Overview

Reshape `propagate_staleness` to take an explicit regeneration-set argument, add a single `clear_staleness` helper that every producer calls on successful write, and rewire the two existing call sites. The in-loop bug becomes a special case of the new contract.

---

## Related Artifacts

- **Spec:** `.project/active/staleness-propagation-fix/spec.md`
- **Concept:** `.project/concepts/staleness-propagation.md`
- **Research:** `.project/research/20260419-115210_staleness-propagation-in-stage1-loop.md`

---

## Research Findings

### Current call sites and producers

| Location | Role | Current behavior |
|---|---|---|
| `scripts/lib/state.py:59-103` | `propagate_staleness` body | Stamps fixed downstream list — no regeneration-set concept |
| `scripts/lib/state.py:11-56` | `get_concept_state` reader | Reads markers correctly; no changes needed |
| `scripts/lib/loop.py:238` | In-loop call | Unconditional stamp after `_update_canonical_files` — the bug |
| `scripts/lib/loop.py:882-902` | `_update_canonical_files` | Uses `shutil.copy2` — a full overwrite, so copying a clean iter-N naturally clears the marker, but the subsequent propagate call re-stamps |
| `scripts/run_analysis.py:456` | `cmd_analyze --feedback` | Correct semantics — propagates with all downstream stamped |
| `scripts/run_analysis.py:512-531` | `cmd_model_setup` write path | `invoke_claude_validated` overwrites file on success; no explicit clearing step |
| `scripts/run_analysis.py:611-631` | `cmd_review` write path | Same — Claude writes fresh frontmatter |
| `scripts/run_analysis.py` | `cmd_synthesize` write path | Same pattern |
| `exploration/concept_explorer/extract_explorer_data.py:812-816` | Explorer extractor | **Already clears its own `.stale` sidecar inline** via `stale_marker.unlink()` after successful write. No import from `concept_analysis/scripts/lib/`. |

### Reusable utilities

- `scripts/lib/frontmatter.py:56` — `update_frontmatter_field` sets a field but has no "remove-field" counterpart. Design adds one.
- `scripts/lib/frontmatter.py:8` — `parse_frontmatter` already recognizes `Stale`.
- `scripts/_fake_claude.py` — existing subprocess fake used by pytest tests.
- `scripts/test_failure_chains.py` — existing pattern: pytest classes (`TestH01_...`), mocks only at `lib.claude.subprocess.run`, lets internal code run for real.

### Marker formats on disk

- `.py`: `# STALE: {reason}` as first line (single line, newline-terminated).
- `.md`: YAML frontmatter fields `Stale: true` and `Stale-Reason: {reason}`.
- Explorer JSON: `{num}.json.stale` sidecar file alongside `{num}.json`; body of sidecar is the reason string.

---

## Core Concept

Every tracked artifact has one code path that writes it (its producer) and one that invalidates it (the propagator). The current system lets the propagator run as if no producer ever fires, so freshly written artifacts get stamped over. The fix is symmetric: the propagator accepts a set of "what the caller just wrote" and exempts those paths; every producer makes a single `clear_staleness` call on its own artifact after a successful write.

The key insight is that `clear_staleness` and `propagate_staleness(..., regenerated=…)` are two halves of the same contract. Together they guarantee that after any step in the pipeline, the on-disk markers exactly describe which artifacts are out of date relative to the root analysis. Neither half works alone.

---

## Key Bets & Decisions

- **Regeneration set is passed as a set of bare filenames** (e.g. `{"analysis.md", "model_setup.py"}`), not `Path` objects. The propagator already iterates by filename; strings keep call sites terse and stringly-matched to the keys it already uses. Alternative considered: `set[Path]`. Rejected — forces every call site to import `Path` and stringify for comparison.
- **Marker helpers live in `lib/state.py`**, not a new module. `state.py` already owns marker-on-artifact semantics; adding strip helpers keeps all marker logic in one file. Alternative: new `lib/markers.py`. Rejected — splits related logic for no readability benefit at this scale.
- **`clear_staleness` in concept_analysis scopes to `.py` and `.md` artifacts only.** The explorer extractor already clears its own `.stale` sidecar inline and has no dependency on `lib/state.py`; the existing asymmetry (concept_analysis reads from and writes sidecars into the explorer directory, but explorer imports nothing from concept_analysis) is preserved. No cross-directory import is introduced by this work item. Alternative considered: have explorer import and call `clear_staleness`. Rejected — creates a new upward dependency for a one-line operation the extractor already performs correctly.
- **`clear_staleness` is called explicitly by every concept_analysis producer, even when the write would implicitly clear the marker via overwrite** (Claude's rewriting of .py/.md files). Explicit calls make the contract audit-able at each call site. Cost: one extra line per producer. Benefit: a future producer that doesn't overwrite the whole file still satisfies the contract.
- **`--force` semantics are unchanged.** `--force` continues to mean "bypass the exists-check." Clearing falls out of the producer rule naturally — no separate flag behavior.
- **Regression tests live in a new file `scripts/test_staleness.py`**, not in `test_failure_chains.py`. `test_failure_chains.py` tracks a numbered audit (H-01..H-21); adding an unrelated test class would dilute that. Alternative: extend `test_failure_chains.py`. Rejected for clarity.
- **Data cleanup for concepts 07, 09, 10 is a separate final commit**, performed after code + tests land and a sanity run of the loop on a test concept shows no re-stamping. Keeps the fix commit and the cleanup commit independently revertable.

---

## Architecture

```
                     analysis.md (root)
                          │
                          │ writes
                          ▼
                ┌─────────────────────┐
                │  Analyze producer   │
                │  (cold-start /      │
                │   feedback pass)    │
                └──────────┬──────────┘
                           │
                           ▼
          clear_staleness(analysis.md) ← [FR-4]
                           │
                           ▼
        ┌─────────────────────────────────────┐
        │  Model-setup producer (in-loop)     │
        │  writes iter-N/model_setup.py       │
        │  → _update_canonical_files promotes │
        │    iff model_ok=True                │
        └──────────┬──────────────────────────┘
                   │
                   ▼
    clear_staleness(model_setup.py) iff model_ok
                   │
                   ▼
   propagate_staleness(reason, regenerated={...})
                   │
                   │ iterates downstream: model_setup, review, synthesis, explorer
                   │ stamps each that is NOT in regenerated
                   ▼
           stale markers on disk
                   │
                   ▼
   get_concept_state reads markers → status table
```

**Data flow on in-loop PASS:**
1. Analyze writes `analysis.md` → `clear_staleness("analysis.md")` (idempotent no-op; root doesn't carry markers).
2. Model-setup writes `iter-N/model_setup.py` (clean).
3. `_update_canonical_files(model_ok=True)` copies to canonical → `clear_staleness("model_setup.py")` as belt-and-suspenders.
4. Assess, verdict written.
5. `propagate_staleness(reason, regenerated={"analysis.md", "model_setup.py"})` → stamps only `review.md`, `synthesis.md`, explorer JSON.
6. PASS exits with canonical `model_setup.py` fresh.

**Data flow on `model_ok=False`:**
1-2 same.
3. `_update_canonical_files` short-circuits; canonical is not overwritten. No `clear_staleness` for `model_setup.py`.
4-5 as above, but `regenerated = {"analysis.md"}` — `model_setup.py` is correctly stamped stale (no longer reflects the new analysis).

**Data flow on standalone `analyze --feedback`:**
1. User feedback applied to `analysis.md`.
2. `clear_staleness("analysis.md")` (no-op).
3. `propagate_staleness(reason, regenerated={"analysis.md"})` → all four downstream stamped.

---

## Required Invariants

1. `propagate_staleness` MUST accept an explicit `regenerated` argument. A member of `regenerated` MUST NOT be stamped in that call.
2. The in-loop call at `loop.py:238` MUST include `"analysis.md"` in `regenerated` and MUST include `"model_setup.py"` iff the iteration's `model_ok` is `True`.
3. Every concept_analysis producer listed in the Component Overview MUST call `clear_staleness(concept_id, artifact_name)` after a successful write and before returning. The explorer extractor satisfies this obligation by its existing inline sidecar `unlink()`.
4. `clear_staleness` MUST be idempotent — calling it on an artifact with no marker is a safe no-op.
5. `clear_staleness` MUST NOT modify bytes beyond the marker. For `.py`, only the first line (if it starts with `# STALE:`) is removed. For `.md`, only the `Stale` / `Stale-Reason` frontmatter fields are removed.
6. `propagate_staleness` MUST remain idempotent (same input → same on-disk result on repeat calls).
7. No marker clearing path MUST ever touch an iter-N/ file. Only canonical-directory artifacts are in scope for both set and clear.
8. No new import from `concept_explorer` into `concept_analysis/scripts/lib/` is introduced. Dependency direction remains one-way (concept_analysis → concept_explorer for reads and sidecar writes).

---

## Component Overview

### `scripts/lib/state.py` (modified)

Owns all marker-on-artifact operations on the concept_analysis side. After this change:
- `propagate_staleness(concept_id, reason, regenerated: Iterable[str], analyses_dir=ANALYSES_DIR)` — new required parameter; skips any downstream whose filename is in `regenerated`. Still writes the explorer-JSON `.stale` sidecar as today (that part is the invalidator side, which lives in concept_analysis).
- `clear_staleness(concept_id, artifact: str, analyses_dir=ANALYSES_DIR)` — new function; dispatches to the format-specific strip helper based on artifact name. Scope: `.py` and `.md` artifacts only. Explorer JSON is not handled here because its producer lives outside concept_analysis and already clears its sidecar inline.
- `_strip_py_stale_marker(path)` — new helper; removes `# STALE:` first line iff present.
- `_strip_md_stale_marker(path)` — new helper; removes `Stale` and `Stale-Reason` frontmatter fields iff present.
- `get_concept_state`, `get_extraction_state` — unchanged.

### `scripts/lib/frontmatter.py` (modified)

- `remove_frontmatter_field(text, key) -> str` — new companion to `update_frontmatter_field`; removes a field if present, returns unchanged text otherwise. Called by `_strip_md_stale_marker`.

### `scripts/lib/loop.py` (modified)

- `_update_canonical_files` — after the `copy2` to canonical `model_setup.py`, calls `clear_staleness(concept_id, "model_setup.py")` when `model_ok=True`.
- Line 238 call site — now passes `regenerated={"analysis.md", "model_setup.py"} if model_ok else {"analysis.md"}`.
- `_run_cold_start` / `_run_feedback_pass` — each calls `clear_staleness(concept_id, "analysis.md")` after a successful analyze write.

### `scripts/run_analysis.py` (modified)

- `cmd_analyze --feedback` (line 456 region) — pass `regenerated={"analysis.md"}` to `propagate_staleness`.
- `cmd_model_setup` — after a successful validated write (post line 531), call `clear_staleness(cid, "model_setup.py")`.
- `cmd_review` — after successful validated write, call `clear_staleness(cid, "review.md")`.
- `cmd_synthesize` — after successful validated write, call `clear_staleness(cid, "synthesis.md")`.

### Explorer extractor (`exploration/concept_explorer/extract_explorer_data.py`)

**No change required.** The extractor at line 812-816 already deletes its `.stale` sidecar inline after a successful write (`stale_marker.unlink()`). This satisfies the producer-clears-on-write contract for the explorer JSON. The plan phase should include a read-only verification of these lines — no edit.

### `scripts/test_staleness.py` (new)

Pytest file covering:
- Unit tests for the three strip helpers (six+ cases each: present/absent/idempotent/content-preservation).
- Unit tests for `propagate_staleness` regeneration-set exemption.
- Unit tests for `clear_staleness` dispatch by artifact kind.
- Integration/regression: PASS iteration leaves canonical fresh; `model_ok=False` iteration leaves canonical stamped.

### Data cleanup (one-off, final commit)

A short shell/script invocation strips `# STALE:` from `model_setup.py` for concepts 07, 09, 10, after verifying the canonical content matches the last clean iter-N copy. Not a permanent script — executed once, then discarded.

---

## Non-Goals

- No change to marker formats on disk.
- No change to `get_concept_state` or the status-table generator.
- No review→synthesis transitive edge.
- No detection of out-of-band hand-edits to `analysis.md`.
- No new `--force-clear` or similar flag — clearing is not user-facing.
- No refactor of `prepare_step` / `skip_if_exists` machinery.

---

## Implementation Notes

**Function signatures (illustrative, not final):**

```python
def propagate_staleness(
    concept_id: str,
    reason: str,
    regenerated: Iterable[str],
    analyses_dir: Path = ANALYSES_DIR,
) -> list[str]: ...

def clear_staleness(
    concept_id: str,
    artifact: str,           # "analysis.md" | "model_setup.py" | "review.md" | ...
    analyses_dir: Path = ANALYSES_DIR,
) -> bool: ...               # True if a marker was removed
```

**Strip-helper edge cases to handle:**
- `.py` first-line marker followed by a blank line vs directly followed by the module docstring — preserve whatever comes after line 1.
- `.py` file with no newline at EOF — preserve trailing-newline status of body.
- `.md` with `Stale: true` but no `Stale-Reason` — remove the one present field.
- `.md` with fields in arbitrary order — preserve order of remaining fields.
- Explorer JSON sidecar missing — delete is a no-op.

**Ordering rule in `_update_canonical_files`:**
Copy first, then clear. If a crash happens between, the canonical file is clean content with a leftover marker — next run's clear call cleans it up. The inverse order could leave a stamped file if the copy fails.

**Test strategy for the in-loop regression:**
Reuse the existing `_fake_claude.py` subprocess fake. Drive `run_stage1_loop` end-to-end with scripted Claude responses for analyze / model / assess. Assert on canonical file contents after loop exit. The existing `test_failure_chains.py` TestH01 pattern is the template.

**Build order (de-risk first):**
1. Add `remove_frontmatter_field` + test it in isolation.
2. Add three strip helpers + test them in isolation. **This is the first risk to de-risk.**
3. Add `clear_staleness` dispatcher + test.
4. Change `propagate_staleness` signature; update the two call sites; exemption test.
5. Wire `clear_staleness` into every producer.
6. Add the PASS / `model_ok=False` regression tests.
7. Run the full loop on a test concept; verify canonical is clean.
8. Data cleanup commit for 07, 09, 10.

---

## Potential Risks

- **Silent breakage of the status reader.** `get_concept_state` reads marker presence. If a strip helper leaves a half-removed marker (e.g., stray blank line or orphaned `Stale-Reason` field), the reader's detection could flip. Mitigation: unit tests for strip helpers assert exact byte output on fixture inputs.
- **Explorer extractor assumption could drift.** Today the extractor clears its sidecar on successful write (`extract_explorer_data.py:812-816`). A future refactor could drop that block, silently re-introducing the original pattern on the explorer side. Mitigation: the plan phase explicitly verifies those lines still exist; validation adds a smoke check that running the extractor on a concept with a seeded `.stale` sidecar leaves no sidecar afterward.
- **Signature change is breaking.** Any out-of-tree caller of `propagate_staleness` breaks. Mitigation: the repo-wide grep in the spec's acceptance criteria — two call sites exist, both in-repo.
- **Cleanup commit re-stamps itself.** If cleanup runs before the code fix is merged (or if the fix regresses), the markers return on the next loop iteration. Mitigation: cleanup is sequenced after the fix is verified on a test concept.
- **Crash-between-copy-and-clear.** `_update_canonical_files` writes then clears; a crash between leaves a clean file with a stale marker. Mitigation: idempotent clear on next loop entry; documented in invariants.

---

## Integration Strategy

- Lands on `fix/stale-tracker`, already created off `scaling_1gw`.
- No schema or interface changes visible to the explorer UI or to `concept_status.md` readers — markers on disk keep the same format.
- No coordination with other branches required; the fix is surgical.
- After merge, a single loop run on any test concept confirms no false markers. No data migration.

---

## Validation Approach

**Unit (pytest, `scripts/test_staleness.py`):**
- Each strip helper: present-marker → removed; absent-marker → unchanged; malformed-input → unchanged; multiple calls → idempotent; body content preserved.
- `clear_staleness` dispatches correctly by artifact name; returns `True` when it removed something, `False` when it didn't.
- `propagate_staleness` with `regenerated={"model_setup.py"}` does not stamp `model_setup.py`; does stamp `review.md`.

**Regression (pytest, in-loop):**
- Seed a temp concept with analysis.md; drive `run_stage1_loop` with scripted Claude returning PASS; assert canonical `model_setup.py` does not start with `# STALE:`.
- Drive loop with scripted `model_ok=False`; assert canonical `model_setup.py` does start with `# STALE:`.
- Pre-seed review.md / synthesis.md; PASS run; assert both carry `Stale: true`.

**Manual smoke:**
- Run loop on a test concept (e.g., a spare concept or a throwaway copy). `grep -c '^# STALE:' analyses/*/model_setup.py` → 0 for fresh passes.
- Seed a `.stale` sidecar next to an explorer JSON; run the extractor on that concept; assert the sidecar is gone afterward. Verifies the existing inline clear at `extract_explorer_data.py:812-816` still works.
- After cleanup commit: same grep on 07, 09, 10 → 0.

**Acceptance tie-in:**
Each spec acceptance criterion maps to at least one test case above.

---

## Next-Stage Handoff

**Fixed (plan should treat as settled):**
- Propagator signature (`regenerated` as `Iterable[str]` of bare filenames).
- Helper location in `lib/state.py`, scoped to `.py` and `.md` artifacts.
- Explicit `clear_staleness` call in every concept_analysis producer, not reliance on overwrite alone.
- Explorer extractor needs no code change — it already clears its sidecar at `extract_explorer_data.py:812-816`. The plan only verifies this.
- No cross-directory import from `concept_explorer` to `concept_analysis/scripts/lib/`.
- New test file `scripts/test_staleness.py`.
- Build order: strip helpers first, then dispatcher, then call-site rewiring.

**Open (plan to pin down):**
- Whether `clear_staleness` should log its removals at INFO (useful for audit) or stay silent.
- Whether the data-cleanup step for concepts 07/09/10 is a standalone Python script in `scripts/` or an inline shell snippet in the plan's final phase.

**First risk to de-risk:**
- Strip-helper correctness. Write the three strip helpers and their unit tests before anything else. Every subsequent change depends on them behaving exactly right.

---

## Next Steps

After approval → `/_my_plan` to produce the phased plan.
