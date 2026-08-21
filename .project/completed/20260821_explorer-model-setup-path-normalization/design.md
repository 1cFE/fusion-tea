# Design: Normalize Concept-Directory Resolution in the Explorer (Stop Storing Paths)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-06-15
**Complexity:** MEDIUM
**Branch:** TBD (off `main`)

## Overview

Stop persisting filesystem paths in the explorer JSON. `/api/compute` derives a concept's `model_setup.py` from its `concept_id` at request time — the same way the findings endpoint already locates `analysis.md` — and gates slider-capability on the `model_type` field the data already carries. The `SourcePaths` block is deleted.

## Related Artifacts

- **Spec:** `.project/active/explorer-model-setup-path-normalization/spec.md`
- **Breaking commit:** `fd76070c` (regenerated explorer JSON on a Windows machine, baked `C:\Users\mallo\…` paths).
- **Reused mechanism:** `findings.py:83` (`_find_concept_dir`), `server.py:756` (`analyses_root` derivation).

## Research Findings

- **The capability signal already exists.** `ConceptData` carries `model_type: ModelType` (`models.py:53–55`, field at `:464`). The two extractor branches set it in lockstep with the path: costingfe → `model_type=COSTINGFE` + `model_setup=<path>` (`extract_explorer_data.py:478,489`); freeform → `model_type=STANDALONE` + `model_setup=None` (`:786,805`). So `model_setup is None` ⟺ `model_type == STANDALONE`. The server already gates other behavior on this exact field (`server.py:950`, `concept.model_type == ModelType.STANDALONE`).
- **A path-free resolver already exists and is in use.** `findings.py:83 _find_concept_dir(concept_id, analyses_root)` prefix-scans `{analyses_root}/{concept_id}-*`, correctly handling letter-suffix IDs (`17a` doesn't match under `17`). The findings endpoint resolves `analysis.md` with **no stored path**: `analyses_root = state.base_dir.parent / "concept_analysis" / "analyses"` (`server.py:756`).
- **Compute is the only path-trusting holdout.** Two references: the 422 gate (`server.py:1042`, `concept.sources.model_setup is None`) and the module load (`server.py:990,994`, `_load_model_module(Path(model_setup))`).
- **`sources.analysis` is dead.** Nothing reads it; findings derives `analysis.md` itself. Non-test readers of `.sources` are exactly `server.py:990,1042` + the field def (`models.py:492`) + the two extractor constructors.
- **All machine paths are confined to the `sources` block.** Each of the 38 files has exactly 2 `mallo` strings, both in `model_setup`/`analysis`. Removing the block satisfies FR-1 completely.
- **No flag-day.** `ConceptData` has no `extra="forbid"` — pydantic ignores leftover keys. Old JSON with a `sources` block still loads after the field is removed, so the schema change and the data migration can land in either order.
- **`_load_model_module` is `lru_cache`d on the `Path`** (`server.py:159`). The derived path is deterministic from `concept_id`, so caching behaves identically.

## Core Concept

The explorer already knows how to find a concept's files from nothing but its `concept_id` — the findings endpoint proves it. The stored `model_setup` path was always redundant with that knowledge, and "redundant data that a regeneration can silently desync" is exactly the bug. The fix is to delete the redundancy: compute resolves `model_setup.py` the same way findings resolves `analysis.md`, and reads slider-capability from `model_type`, which the data already carries. Nothing in the JSON points at a filesystem anymore, so no machine-specific string can be baked in by any contributor on any OS. This is a *removal*, not an addition — the design composes two pieces that already exist (`_find_concept_dir` + `model_type`) and throws away the third (`SourcePaths`).

## Key Bets

- **B1.** A concept's directory is fully determined by its `concept_id` via the `{concept_id}-*` prefix scan, on every host where compute runs. *If false → compute resolves the wrong directory or none, and recompute breaks again — but findings already relies on this exact assumption in production, so it is already load-bearing.*
- **B2.** `model_type == COSTINGFE` is exactly equivalent to "has a `model_setup.py` that supports slider recompute" (i.e., the old `model_setup is not None`). *If false → a concept is mis-gated: a freeform concept attempts a module load (500) or a costingfe concept is refused (422). Mitigated by the lockstep construction in both extractor branches and a parity assertion across all 38 files during implementation.*
- **B3.** The `concept_analysis/analyses/` tree is deployed alongside the explorer data on every target host. *If false → costingfe concepts 500 because their source dir is absent. This is already true for findings today; if it weren't, findings would be blank in the deploy container. Compute simply adopts the same deployment dependency.*

## Key Decisions

- **D1. Remove `SourcePaths` / the `sources` field entirely** rather than keep a slimmed or vestigial version. The path was the field's only content: location is now derived, capability lives in `model_type`, and `analysis` is dead. *Rejected: keeping an empty `SourcePaths` or a `model_backed: bool` — both leave dead schema that invites re-population (which is how this bug persisted) and add a field that duplicates `model_type`.*
- **D2. Reuse `_find_concept_dir` from `findings.py`** (promoted to a public `find_concept_dir`), and factor the `analyses_root` derivation into one helper used by both the findings endpoint and compute. *Rejected: duplicating the prefix-scan or the `base_dir.parent/concept_analysis/analyses` literal in `server.py` — FR-2 forbids re-implementing the resolution, and two copies of the root literal would drift.*
- **D3. Error semantics: 422 for non-costingfe, 500 for an unresolvable costingfe concept.** A freeform concept legitimately doesn't support sliders (client-meaningful → 422). A costingfe concept whose dir/`model_setup.py` can't be found is a deploy/data-integrity fault, not a client error (→ 500, explicit message, no fallback per FR-5). *Rejected: 422 for both — it would mask a broken deployment as an ordinary "not supported" response.*
- **D4. Migrate via a one-shot script that strips the `sources` block** from each of the 38 files, preserving all other formatting. *Rejected: full re-extraction of all 38 — it requires the 1costingfe library, reruns every model, and would churn unrelated fields, risking exactly the kind of broad regen diff that introduced the bug. Parity with fresh output (FR-6) holds structurally: the extractor now omits `sources`, the migration removes `sources`, and nothing else changes.*

## Architecture

```
ComputeRequest(concept_id, overrides, apply_analyst_overrides)
        │
   compute()                      ── 404 if concept unknown
        │                         ── 422 if model_type != COSTINGFE        (was: sources.model_setup is None)
        ▼
   _compute_cached(concept_id, …)  [lru_cache]
        │
        ├─ analyses_root  = analyses_root_for(state.base_dir)   ── shared helper (also used by findings @756)
        ├─ concept_dir    = find_concept_dir(concept_id, analyses_root)   ── reused from findings.py
        │        └─ None or missing model_setup.py  → 500 (explicit, no fallback)   [B3, D3]
        ├─ module = _load_model_module(concept_dir / "model_setup.py")   [lru_cache on Path]
        └─ … unchanged forward/override math …
```

Data flow change: the arrow from JSON `sources.model_setup` → `_load_model_module` is severed and replaced by `concept_id` → `find_concept_dir` → `model_setup.py`. The findings endpoint's data flow is unchanged; it just shares the `analyses_root` helper instead of inlining the literal.

## Required Invariants

- **INV-1.** No `data/*.json` contains a filesystem path to a source script. (Verifiable: grep for `C:\\`, `/home/`, `model_setup.py`, `analysis.md` in `data/*.json` → empty.)
- **INV-2.** For every concept, `model_type == COSTINGFE` ⟺ a resolvable `{analyses_root}/{concept_id}-*/model_setup.py` exists. (Verifiable across all 38 at implementation time; underpins B2.)
- **INV-3.** A no-op recompute for a costingfe concept reproduces its stored `result_1gw` headline (concept `01` → `lcoe_per_mwh ≈ 161.69`). Unchanged from today; the math path is untouched.
- **INV-4.** Compute resolves identically regardless of the absolute location of the repo/data on disk (host independence).

## Component Overview

- **`models.py`** — Delete `SourcePaths` (`:400`) and the `sources` field on `ConceptData` (`:492`). No replacement field; `model_type` already present.
- **`server.py`** — (a) add a small `analyses_root_for(base_dir)` helper (single home for the `base_dir.parent/concept_analysis/analyses` literal) and use it at the findings endpoint (`:756`) and in compute; (b) compute 422 gate switches to `model_type != COSTINGFE` (`:1042`); (c) the module-load path (`:990–994`) resolves `concept_dir` via `find_concept_dir` and raises an explicit 500 when unresolvable.
- **`findings.py`** — Promote `_find_concept_dir` → public `find_concept_dir` (`:83`); internal call site updated. Optionally consume `analyses_root_for` too (cosmetic).
- **`extract_explorer_data.py`** — Drop the `sources=SourcePaths(...)` argument from both `ConceptData` constructions (`:489`, `:805`). No path is emitted.
- **Migration script** — One-shot: load each `data/*.json`, remove the top-level `sources` key, write back with identical indent/encoding. Lives under `scripts/` or the work-item dir.
- **Tests** — Remove `SourcePaths` imports/usages across ~8 test files; the compute fixtures (`test_state_and_compute.py:133–173`, `test_slider_override_semantics.py`) must place the fake `model_setup.py` under a *derived* `analyses_root` mirroring the real layout and set `model_type` instead of a path.

## Non-Goals

- No change to recompute math, override application, `result_1gw`/three-forward contract, or the costingfe-vs-freeform *classification* logic.
- No frontend changes (verified: no JS/HTML reads `sources`).
- No change to `manifest.json`, `concept_registry.json`, `decision_tree.json`, `parameter_index.json` (verified clean of machine paths).
- Not introducing a config knob for `analyses_root` location — the `base_dir`-relative derivation is already correct and deterministic.

## Implementation Notes

- **Resolution root must stay consistent** between findings and compute. The single `analyses_root_for(base_dir)` helper guarantees this; don't reinline the literal.
- **Compute-test fixture restructuring is the main cost.** Today `costingfe_base_dir` writes `model_setup.py` at `tmp_path/analyses/04-fake-concept` and feeds the absolute path via `SourcePaths`. After this change the fixture must write it where `analyses_root_for(base_dir)` resolves — i.e., build `base_dir = tmp_path/exploration/concept_explorer` and place the module at `tmp_path/exploration/concept_analysis/analyses/04-fake-concept/model_setup.py` — and set `model_type=COSTINGFE` (no path). The standalone concept sets `model_type=STANDALONE`.
- **Migration ↔ code-change ordering is free** (no `extra="forbid"`). Recommend landing them in one commit anyway for a coherent diff, but either order is safe.
- **No fallbacks (FR-5):** `find_concept_dir` returning `None`, or a missing `model_setup.py`, raises with a message naming the concept_id and the resolved `analyses_root`. Do not substitute a default path or skip silently.
- Keep `find_concept_dir`'s prefix semantics exactly (trailing-hyphen anchor) — letter-suffix IDs depend on it.

## Potential Risks

- **B2 false for some concept** (model_type/path desync in current data): a costingfe concept with no resolvable dir, or vice-versa. *Mitigation:* before deleting the field, run a one-time audit asserting INV-2 across all 38 files; fix any mismatch as data, not code.
- **Deploy omits the `analyses/` tree** (B3): costingfe concepts 500. *Mitigation:* this dependency already exists for findings; document it in the hosting work-item (`explorer-web-hosting`) and surface a clear 500 message so the cause is obvious.
- **Broad test churn** introduces incidental breakage. *Mitigation:* changes are mechanical (drop import, set `model_type`); run the full explorer suite as the gate.

## Integration Strategy

Pure simplification of the existing compute path; replaces the stored-path mechanism, complements the already-path-free findings endpoint, and unblocks `explorer-web-hosting` (which needs a working compute endpoint in the `python:3.12-slim` container). No new workflow.

## Validation Approach

- **Audit (pre-change):** assert INV-2 across all 38 files.
- **Unit/integration:** `uv run python -m pytest exploration/concept_explorer/tests/ -q` after fixture updates.
- **End-to-end:** start the server, `POST /api/compute {concept_id:"01", overrides:{}}` → 200, `headline.lcoe_per_mwh ≈ 161.69` (INV-3); a freeform concept (02/03/16/27/35) → 422 (INV-2/D3).
- **Host independence (INV-4):** run compute against a data dir copied to a path matching no contributor's machine → still 200.
- **FR-1 grep:** no path strings remain in `data/*.json` (INV-1).

## Next-Stage Handoff

**Fixed:** no stored paths (delete `SourcePaths`); derive via shared `analyses_root_for` + reused `find_concept_dir`; gate on `model_type`; 422 freeform / 500 unresolvable-costingfe; strip-`sources` migration.

**Open for plan:** exact home of `analyses_root_for` (module fn in `server.py` vs `findings.py`); whether migration script lives in `scripts/` or the work-item dir; precise wording of the 500 message.

**De-risk first:** run the INV-2 audit before touching code — if any of the 38 concepts violate the `model_type`↔`model_setup.py` equivalence, that is a data fix that must precede the schema deletion.

---
Next Step: After approval → `/_my_plan` (recommended — multi-file change with a pre-change data audit) or `/_my_implement`.
