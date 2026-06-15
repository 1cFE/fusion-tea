# Spec: Normalize Concept-Directory Resolution in the Explorer (Stop Storing Paths)

**Status:** Implementation Complete
**Owner:** Reid W
**Created:** 2026-06-15
**Complexity:** MEDIUM
**Branch:** TBD (off `main`)

---

## Work Item Summary

The concept explorer stores a filesystem path to each concept's `model_setup.py` inside its committed JSON data, and the `/api/compute` endpoint imports that path verbatim to run slider recomputes. The path is machine-specific, so recompute only works on the machine that last regenerated the data. This work item removes the stored path entirely: the server already knows how to find a concept's directory from its `concept_id` (the findings endpoint does exactly this), so compute should derive the `model_setup.py` location the same way instead of trusting baked data. When done, slider recompute works on every host — dev box, deploy container, and after a regeneration from any machine — with no path strings in the data.

## Why This Matters Now

`/api/compute` currently returns HTTP 500 on `main` for every cost-model concept on any host that isn't the Windows machine that last regenerated the JSON. The stored value on HEAD is `C:\Users\mallo\...\model_setup.py`, which doesn't exist on the Linux dev box or the `python:3.12-slim` deploy container, so `_load_model_module` raises `FileNotFoundError`. Slider recompute — a core explorer feature — is broken everywhere it actually runs, and the web-hosting work (`explorer-web-hosting`) cannot ship a working compute endpoint until this is fixed.

## Key Bets / Constraints

- **Bet:** The concept directory is fully derivable from `concept_id` at request time. The codebase already proves this: `findings.py:83 _find_concept_dir(concept_id, analyses_root)` resolves a concept's directory by prefix-scanning `{analyses_root}/{concept_id}-*`, and the findings endpoint uses it with **no stored path**. Compute is the only endpoint still trusting a baked path.
- **Bet:** Removing the path is strictly better than fixing it (e.g. to a repo-relative path). Any stored path duplicates information the server can derive and re-introduces a machine-coupling failure mode on the next regeneration. The `SourcePaths` docstring already *claims* paths are "repo-relative" (`models.py:401`); the last regen silently violated that contract. Data that can't drift is better than data we hope stays correct.
- **Constraint:** The "is this concept costingfe-backed / slider-capable" signal must be preserved. Today that signal is overloaded onto the path field (`model_setup is None` ⇒ freeform ⇒ compute returns 422). It must survive the change as an explicit signal, not as a side effect of a path being present.
- **Constraint:** uv-only repo (`uv run python ...`). No fallback / silent-default behavior — if a concept claims to be model-backed but its directory or `model_setup.py` can't be resolved, that is an error, not a degraded-mode pass.
- **Non-goal:** No change to recompute math, override semantics, the freeform-vs-costingfe extraction logic itself, or any frontend code. This is a data-normalization and resolution-path fix only.

---

## Business Goals

### Why This Matters

The explorer's value is interactive cost exploration — moving a slider and seeing LCOE update. That path is dead on every deployment target right now. Beyond the immediate outage, the data carries machine-specific absolute paths into version control, which is a recurring footgun: every regeneration re-bakes whoever's local path, and "works on my machine" silently ships. Normalizing the resolution removes the bug and the class of bug.

### Success Criteria

- [ ] Slider recompute works on the dev box, in the deploy container, and after a regeneration performed on any machine (Windows or Linux), with no per-host configuration.
- [ ] No filesystem path strings remain in the committed explorer JSON.
- [ ] A future regeneration cannot re-introduce a machine-specific path, because the extractor no longer writes one.

### Priority

P0 for the explorer-hosting track — compute is currently broken on every target host. Standalone fix; does not depend on other in-flight work and unblocks `explorer-web-hosting`.

---

## Problem Statement

### Current State

- All 38 cost-model concept JSON files under `exploration/concept_explorer/data/*.json` store `sources.model_setup` (and `sources.analysis`) as a machine-absolute path. On HEAD these are Windows paths: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\...\model_setup.py`.
- `server.py:994` runs `_load_model_module(Path(model_setup))` on that string. On any non-`mallo` host this raises `FileNotFoundError`, so `/api/compute` returns HTTP 500 for every cost-model concept.
- **Git history (the user's hunch, confirmed):** the path was *always* machine-absolute. Before commit `fd76070c` it was `/home/reid/1cfe/fusion-tea/...` — which resolved on Reid's dev box but never in the deploy container. Commit `fd76070c` ("chore(models): regenerate ... explorer JSON", Mallory Snowden, 2026-06-08) regenerated the JSON on a Windows machine and baked in `C:\Users\mallo\...`, which broke it on the dev box too. So compute was *never* portable; the regen just moved which single machine it happened to work on.
- `sources.analysis` carries the same machine-absolute path but is **never read by the server** — the findings endpoint derives `analysis.md` itself via `analyses_root` + `_find_concept_dir`. It is dead data.

### Desired Outcome

The explorer JSON stores no filesystem path. `/api/compute` resolves a concept's `model_setup.py` at request time from `concept_id`, reusing the same `analyses_root` + `_find_concept_dir` mechanism the findings endpoint already uses. The costingfe-vs-freeform distinction is carried as an explicit capability signal so freeform concepts still return 422. The fix is host-independent and regeneration-proof.

---

## Scope

### In Scope

- The explorer data schema (`models.py` `SourcePaths`): remove the stored `model_setup` path and the dead `analysis` field; carry the slider-capable signal as an explicit boolean.
- The `/api/compute` resolution path (`server.py`): derive `model_setup.py` from `concept_id` instead of reading a stored path; preserve the 422 for non-model-backed concepts.
- The extractor (`extract_explorer_data.py`): stop writing filesystem paths; emit the capability signal.
- Migration of the 38 committed `data/*.json` files to the new schema.
- Updating the tests that construct/assert `SourcePaths` (`test_models.py`, `test_extract_adapter.py`, `test_taxonomy_server.py`).

### Out of Scope

- Recompute math, override application, and the `result_1gw` / three-forward contract — unchanged.
- The freeform-vs-costingfe *classification* logic in the extractor (which extraction branch a concept takes) — unchanged; only what each branch writes for the source signal changes.
- Any frontend (JS/HTML/templates) — verified that nothing client-side reads `sources.model_setup` or `sources.analysis`.
- The non-concept data files (`manifest.json`, `concept_registry.json`, `decision_tree.json`, `parameter_index.json`) — verified clean of machine paths.

### Edge Cases & Considerations

- **Freeform concepts** (currently `model_setup: null` — concepts 02, 03, 16, 27, 35): must still report "not slider-capable" and produce a 422 from compute, not a 500 or a silent success.
- **Sub-lettered concept IDs** (e.g. `17a`, `17b`): resolution must stay unambiguous. `_find_concept_dir` matches the prefix `{concept_id}-`, and compute is always called with the full ID (`17a`), so `17a-` matches only that directory — but this should be confirmed in design/test.
- **A concept marked model-backed whose directory or `model_setup.py` can't be resolved** at request time: must surface as an explicit error (no fallback). Decide in design whether this is a 422 or a 500 and what the message says.
- **`_load_model_module` is `lru_cache`d** (`server.py:160`, with `.cache_clear()` at `:955`): the derived value must be a stable `Path` so caching keys behave the same as today.
- **Migration parity:** regenerating the JSON from the extractor should produce the new schema; the migration of the existing 38 files should match what a fresh extraction would now emit (no drift between hand-migrated and regenerated data).

---

## Requirement Selection Notes

The normative requirements below fix the *outcome* — no stored paths, derived resolution, preserved capability signal, host independence — and deliberately leave the *mechanism* to design. Specifically, the exact name and placement of the capability signal (e.g. a `model_backed: bool` on `SourcePaths`, a different field, or a slimmer schema), and the precise error type for an unresolvable model-backed concept, are design decisions, not spec decisions, and are handed off below.

---

## Requirements

### Functional Requirements

> All requirements are from the user's request and the confirmed investigation unless marked otherwise.

1. **FR-1**: The committed explorer JSON MUST NOT contain any filesystem path to `model_setup.py`, `analysis.md`, or other source scripts. After this work, `exploration/concept_explorer/data/*.json` MUST contain no machine-specific path strings.
2. **FR-2**: `/api/compute` MUST resolve a concept's `model_setup.py` location at request time from the `concept_id`, reusing the existing directory-resolution mechanism (`analyses_root` derived from `base_dir`, plus `_find_concept_dir`'s `{concept_id}-*` prefix scan) rather than reading a stored path. It MUST NOT duplicate that resolution logic — the shared resolver SHOULD be reused (refactored to a common location if needed).
3. **FR-3**: The schema MUST carry an explicit signal for whether a concept is costingfe-backed / slider-capable. Compute MUST return HTTP 422 for non-model-backed (freeform) concepts and MUST NOT attempt to load a module for them. The dead `sources.analysis` field MUST be removed.
4. **FR-4**: The extractor (`extract_explorer_data.py`) MUST stop writing filesystem paths into the JSON and MUST instead emit the capability signal from FR-3. Re-running the extractor for any concept MUST produce JSON with no path strings.
5. **FR-5**: A concept that reports itself model-backed but whose directory or `model_setup.py` cannot be resolved at request time MUST surface as an explicit error. There MUST be no fallback, default path, or silent degraded-mode pass. (Exact error type/message: design.)
6. **FR-6**: The 38 existing committed `data/*.json` files MUST be migrated to the new schema, and the migrated data MUST match what a fresh extractor run now emits (no hand-migration drift).

### Non-Functional Requirements

- Host independence: identical compute behavior on the dev box, the `python:3.12-slim` deploy container, and after a regeneration from any contributor's machine. No per-host configuration.
- uv-only: all commands run via `uv run python ...`.

---

## Acceptance Criteria

### Core Functionality

- [ ] `POST /api/compute` for concept `01` with empty overrides returns HTTP 200 with `headline.lcoe_per_mwh ≈ 161.69` (the parity-verified value).
- [ ] `POST /api/compute` for a freeform concept (02, 03, 16, 27, or 35) returns HTTP 422 (slider compute not available), not 500.
- [ ] `grep -rl 'C:\\Users\\mallo' exploration/concept_explorer/data/*.json` returns nothing; no absolute path (Windows or POSIX) to a source script remains in any `data/*.json`.
- [ ] Re-running the extractor for one concept emits JSON with the capability signal and no filesystem path.
- [ ] Compute works against a data directory copied to a path that matches no contributor's machine (proves host independence).

### Quality & Integration

- [ ] Existing explorer tests pass: `uv run python -m pytest exploration/concept_explorer/tests/ -q`.
- [ ] Tests constructing/asserting `SourcePaths` (`test_models.py:116,378`, `test_extract_adapter.py`, `test_taxonomy_server.py`) are updated to the new schema and pass.
- [ ] The findings endpoint (which already derives its paths) is unaffected.

---

## Next-Stage Handoff

**Settled in this spec:**
- No filesystem paths in the committed JSON (FR-1).
- Compute derives the directory from `concept_id` and reuses the existing resolver, not a stored path (FR-2).
- An explicit capability signal replaces the overloaded path-presence test; `sources.analysis` is removed (FR-3).
- No fallbacks; unresolvable model-backed concepts are an explicit error (FR-5).
- The 38 data files are migrated to match fresh extractor output (FR-6).

**Design must figure out:**
- The exact schema shape for the capability signal — `model_backed: bool` on `SourcePaths`, a relocated field, or a slimmed/removed `SourcePaths` — and how `models.py`, the extractor, and the 38 files line up on it.
- Where the shared resolver lives. `_find_concept_dir` is currently in `findings.py`; decide whether compute imports it from there or it moves to a shared module both endpoints use.
- The precise error type and message for an unresolvable model-backed concept (422 vs 500).
- The migration mechanism: a one-shot script vs. a full extractor re-run for all 38, and how parity with fresh output is verified.

**Watch-outs for design:**
- `_load_model_module` is `lru_cache`d — keep the resolved value a stable `Path` so cache keys don't change behavior.
- Sub-lettered IDs (`17a`/`17b`) and prefix-match ambiguity in `_find_concept_dir`.
- Keep the costingfe-vs-freeform *classification* untouched; only change what the branches emit for the source signal.
- The migrated data must equal fresh extractor output — guard against the hand-migration and the extractor diverging.

---

## Related Artifacts

- **Breaking commit:** `fd76070c` — "chore(models): regenerate model_output.txt and explorer JSON against latest 1costingFE" (2026-06-08).
- **Reused mechanism:** `exploration/concept_explorer/findings.py:83` (`_find_concept_dir`), `server.py:756` (`analyses_root` derivation).
- **Related work:** `.project/active/explorer-web-hosting/` (depends on a working compute endpoint), `.project/active/explorer-identity-spine/` (concept-identity resolution).
- **Design:** `.project/active/explorer-model-setup-path-normalization/design.md` (to be created).

---

**Next Steps:** After approval, proceed to `/_my_design`.
