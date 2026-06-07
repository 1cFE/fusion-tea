# Design: Concept Explorer Omit List

**Status:** Complete (implemented & audited)
**Owner:** Reid W
**Created:** 2026-06-05 13:10
**Branch:** main

---

## Overview

A single declarative YAML file names concepts to exclude from the explorer; a shared loader in `models.py` reads it, and two independent consumers — the extractor and the server — each enforce it on their own.

## Related Artifacts

- **Spec:** `.project/active/concept-explorer-omit-list/spec.md`
- **Code touched:** `exploration/concept_explorer/models.py`, `extract_explorer_data.py`, `server.py`
- **Convention reference:** `exploration/concept_explorer/data/parameter_display_registry.yaml`

---

## Research Findings

**Extraction path** (`extract_explorer_data.py`):
- `discover_concepts()` (`:836`) iterates `analyses/`, parses the ID via `parse_concept_id()` (`:69`, regex `^(\d+[a-z]?)` → string like `"26"`, `"17a"`), and returns dirs to extract. It already takes a `concept_filter` and already has an explicit per-concept skip downstream (`pending-design-point`, `:902`) with a `skipped` report (`:971`). This is the natural insertion point — same shape as work already there.
- `yaml.safe_load` is already imported and used (`:26`, `:682`).

**Server path** (`server.py`):
- `_load_data()` (`:200`) globs `data/*.json` minus `_NON_CONCEPT_FILES` (`:219`), validates each into `ConceptData`, then builds the manifest and parameter index **in-memory from the loaded list** (`:242`–`243`). So filtering the concept set at load covers profiles, comparison, manifest, and parameter index in one place.
- `_load_taxonomy()` (`:248`) loads `ConceptRegistry` and the decision-tree dict, then computes `similarity_reports`, `compute_similarity_matrix`, and `compute_constellation` **from `registry.concepts`** (`:272`–`282`). Filtering the registry once, before these computations, covers similarity + constellation. The decision tree is a separate dict and must be pruned independently.

**Decision-tree shape** (`data/decision_tree.json`): `{version, root}`; nodes are `{field, label, children}`; leaves carry `{value, label, concepts: ["12","19","35"]}`. IDs appear only inside `concepts` lists.

**Registry shape**: `ConceptRegistry` pydantic model, `.concepts: list[...]`, each with `.concept_id` (string).

**`models.py`**: currently pure data models + `build_manifest`/`build_parameter_index` — no file I/O, no yaml import. Both the extractor and server import from it, so it is the correct shared home for the loader; this design adds one yaml import + one filesystem read to it.

---

## Core Concept

One YAML file (`omit_list.yaml`, ID → reason) is the single source of truth. A pure-ish loader `load_omit_list() -> set[str]` in `models.py` reads it once and returns the omitted IDs. Two consumers depend on the loader but **not on each other**: the extractor calls it inside `discover_concepts()` to drop omitted dirs before writing any `data/{id}.json`; the server calls it inside `_load_data()` (drop concept files) and `_load_taxonomy()` (drop registry entries + prune the tree). Because the manifest, parameter index, similarity, and constellation are all derived *from already-filtered collections*, each enforcement site is a single `if id in omitted: skip` — the derivations inherit the exclusion for free. The list is data, so changing the omitted set is a one-line YAML edit with no code change.

The insight: there are exactly two *load boundaries* in the system (extraction-write and server-read), and every downstream artifact is computed from what passes those boundaries. Filter at the two boundaries and everything downstream follows — no per-view filtering needed.

---

## Key Bets & Decisions

- **Bet: filter at load boundaries, not per-view.** Manifest/parameter-index (server) and similarity/constellation (taxonomy) are all built from collections that pass through one filterable point. We filter those collections; we do **not** add filters to each API endpoint. Invariant to preserve: those builders keep deriving from the filtered collection, never re-reading raw files.
- **Bet: `set[str]` is the whole interface.** The reasons in the YAML are documentation for humans; code only ever needs membership. The loader discards reasons and returns `set[str]`. Keeps every call site a one-liner.
- **Decision: omit file lives at `exploration/concept_explorer/omit_list.yaml`** (package dir, next to `models.py`), not in `data/`. Rationale: `data/` is extraction *output* (and is regenerated/synced); the omit list is hand-authored *config* that controls extraction, so it belongs with the code, loaded via `Path(__file__).parent`. (`parameter_display_registry.yaml` lives in `data/` for historical reasons; we are not following that placement, only its YAML style.) Alternative considered — `data/omit_list.yaml` — rejected because it mixes durable config into the regenerable output dir and would need adding to `_NON_CONCEPT_FILES` (though the `*.json` glob already wouldn't catch a `.yaml`).
- **Decision: decision-tree pruning drops emptied branches.** After removing omitted IDs from every `concepts` leaf, recursively drop any node whose subtree contains zero concepts, so the tree shows no dead-end branches. Alternative — leave empty leaves in place — rejected as a visible artifact of omission ("omit from EVERYTHING").
- **Decision: loader tolerance.** Missing file, empty file, and unknown IDs are all valid no-ops (FR-8). The loader never raises on content; a malformed YAML is the one case that may surface as an error (authoring bug, worth failing loud).

---

## Architecture

```
omit_list.yaml ──read──> load_omit_list() -> set[str]   [models.py]
                              │
                 ┌────────────┴─────────────┐   (independent consumers)
                 ▼                            ▼
   discover_concepts()            server: _load_data()  +  _load_taxonomy()
   [extract_explorer_data.py]     [server.py]
   skip omitted dirs;             drop omitted concept files;
   never write data/{id}.json;    filter registry (-> similarity, constellation);
   add to `skipped` report        prune decision tree (drop emptied branches)
```

Data flows one way: YAML → set → two enforcement points. No state is shared between the extractor and server beyond the file on disk; either works correctly if the other never ran (FR-6).

## Required Invariants

- **I-1:** `load_omit_list()` returns `set[str]` of canonical IDs matching `parse_concept_id` output (string, e.g. `"26"`, `"17a"`). YAML keys must be read as strings even when numeric-looking.
- **I-2:** No omitted concept's `data/{id}.json` is written or refreshed by extraction.
- **I-3:** No omitted concept appears in: concept profiles, comparison, manifest, parameter index, registry-derived similarity reports, constellation, or the decision tree.
- **I-4:** Manifest and parameter index continue to be built from the already-filtered concept list (not re-read from disk) — so they need no separate filter.
- **I-5:** Similarity and constellation continue to be computed from the already-filtered registry — so they need no separate filter.
- **I-6:** No file under `analyses/` or any existing file under `data/` is deleted or modified.

## Component Overview

- **`omit_list.yaml`** (new, `exploration/concept_explorer/`): flat map `"<id>": "<reason>"`. Hand-authored. Initial entries: 26, 27, 34, 38.
- **`load_omit_list()`** (new, `models.py`): reads the YAML next to the module, returns `set[str]` of keys; missing/empty file → empty set. The single shared reader.
- **`discover_concepts()`** (edit, `extract_explorer_data.py:836`): after computing `concept_id`, skip if in the omit set; collect for the existing `skipped` report.
- **`_load_data()`** (edit, `server.py:200`): exclude omitted IDs from the globbed concept set before validation. Manifest/parameter-index follow.
- **`_load_taxonomy()`** (edit, `server.py:248`): filter `registry.concepts` before similarity/constellation; prune omitted IDs from the decision-tree dict.
- **`prune_decision_tree(tree, omitted)`** (new helper, location TBD in plan — likely `server.py` or `taxonomy_models.py`): recursive removal of omitted IDs from `concepts` lists + drop of emptied branches.

## Non-Goals

- No per-view or partial omission; omission is all-or-nothing per concept.
- No deletion/modification of `analyses/` or existing `data/` files.
- No change to the upstream pipeline that generates `concept_registry.json` / `decision_tree.json` — the server filters them at load.
- No UI/runtime toggle; the list is applied at extraction time and server startup.

## Implementation Notes

- **String-key gotcha (I-1):** `yaml.safe_load` will parse a bare `26:` key as the **int** `26`. Author keys quoted (`"26":`) and/or coerce `str(k)` in the loader. This is the single most likely correctness bug; the plan should add a test that an unquoted numeric key still matches.
- **Loader path:** `Path(__file__).parent / "omit_list.yaml"` so it resolves regardless of CWD (extraction runs from repo root; server sets its own `base_dir`).
- **Decision-tree prune sketch** (concept only, not final code):

  ```
  def prune(node, omitted):
      if "concepts" in node:
          node["concepts"] = [c for c in node["concepts"] if c not in omitted]
      node["children"] = [prune(c, omitted) for c in node.get("children", [])]
      node["children"] = [c for c in node["children"] if subtree_has_concepts(c)]
      return node
  ```
  Apply to `root`; if `root` empties entirely, the tree endpoint returns an empty-but-valid tree.
- **Don't double-filter:** resist adding `id in omitted` checks to API endpoints — that would violate I-4/I-5's "derive from filtered collection" and create two places to keep in sync.
- **Reporting:** reuse the existing `skipped` list/print block (`extract_explorer_data.py:971`); add omitted concepts with reason `"omit_list"`.

## Potential Risks

- **Int-vs-string key mismatch** (see Implementation Notes) — mitigated by string coercion + a regression test.
- **Decision-tree structure drift:** prune assumes `children` + `concepts` keys. If the upstream tree schema changes, prune must change. Mitigated by `subtree_has_concepts` being tolerant of missing keys and by a test fixture mirroring the real shape.
- **Constellation/similarity assuming full registry:** if any of those functions index concepts by position or expect a fixed count, filtering could shift results. Low risk (they take the registry list as input), but the plan should spot-check `compute_similarity_matrix`/`compute_constellation` for positional assumptions.

## Integration Strategy

Purely additive at the two existing load boundaries; no new endpoints, no schema changes, no data migration. Existing extraction and server runs behave identically when the omit file is empty/absent. Complements the existing `pending-design-point` skip (per-concept, frontmatter-driven) with a project-level, frontmatter-independent exclusion.

## Validation Approach

- **Unit:** `load_omit_list()` — missing file → `set()`; empty file → `set()`; unquoted numeric key `26` → `{"26"}`; reasons ignored.
- **Unit:** `prune_decision_tree` — omitted IDs removed from leaves; fully-emptied branch dropped; unrelated branches intact.
- **Integration (extraction):** with 26/27/34/38 omitted, `run_extraction` does not write those `data/*.json` and lists them as skipped; a non-omitted concept still writes.
- **Integration (server):** with the same omit file, none of 26/27/34/38 appear in `/api/manifest`, parameter index, registry/similarity, constellation, or decision-tree responses; pre-existing `data/26.json` etc. remain on disk unmodified.
- **Independence (FR-6):** server filtering hides 26/27/34 (which have stale on-disk JSON) without any extraction run; extraction skipping works without the server.
- **Regression:** existing explorer test suite passes (`exploration/concept_explorer/tests/`).

## Next-Stage Handoff

**Fixed for the plan:**
- One YAML file at the package dir; loader in `models.py` returning `set[str]`; two independent enforcement points; emptied decision-tree branches dropped; existing files untouched; initial set 26/27/34/38.

**Open for the plan:**
- Exact home for `prune_decision_tree` (`server.py` vs `taxonomy_models.py`).
- Whether to coerce keys in the loader, require quoted keys, or both (recommend both + test).

**De-risk first:**
- The int-vs-string key match and the decision-tree prune — write those two tests before wiring the call sites.

---

**Next Step:** After approval → `/_my_plan`
