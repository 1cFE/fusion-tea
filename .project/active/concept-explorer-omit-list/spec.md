# Spec: Concept Explorer Omit List

**Status:** Complete (implemented & audited)
**Owner:** Reid W
**Created:** 2026-06-05 13:01
**Complexity:** LOW
**Branch:** main

---

## Work Item Summary

Add a single, declarative "omit list" that excludes chosen fusion concepts from the concept explorer. One data file names the omitted concept IDs; two independent consumers honor it — the extractor skips writing the concept's `data/{id}.json`, and the server skips loading/rendering the concept everywhere it would otherwise surface (concept profiles, comparison, manifest, parameter index, constellation map, decision tree). "Done" means a concept ID listed in the omit file disappears from the explorer end to end, with no manual file deletion required and no edits scattered across the codebase.

## Why This Matters Now

Some analyzed concepts are not ones we want shown in the explorer (incomplete, low-quality, duplicative, or otherwise not meant for comparison), but today there is no clean way to exclude them. The only levers are deleting on-disk data files (which the extractor will silently recreate, and which does nothing for taxonomy artifacts that still reference the concept) or hand-editing skip logic in multiple places. We want one obvious place to say "leave these out" that the whole system respects. The immediate trigger is excluding concepts 26, 27, 34, and 38.

## Key Bets / Constraints

- **Bet:** A flat declarative list of concept IDs (with a per-entry reason for documentation) is sufficient — exclusion is all-or-nothing per concept; we do not need per-stage or per-view granularity.
- **Constraint:** The two enforcement points (extraction, server rendering) MUST be independent — each reads the omit list directly and enforces it on its own, with no ordering or runtime dependency between them. Skipping extraction does not rely on the server, and skipping rendering does not rely on extraction having skipped.
- **Constraint:** Existing on-disk `data/{id}.json` files for omitted concepts are left untouched; the server filter is what hides any that already exist.
- **Constraint:** The omit list is the single source of truth — adding/removing a concept is a one-line edit to one file, with no code change required.
- **Non-goal:** This does not delete, archive, or modify any concept's analysis artifacts under `analyses/`, nor any existing files under `data/`.
- **Non-goal:** This does not change how non-omitted concepts are extracted or rendered.

---

## Business Goals

### Why This Matters

The explorer is the primary surface for cross-concept comparison. Concepts that are not ready or not wanted for that comparison currently leak into every view because inclusion is implicit ("whatever is on disk / in the taxonomy"). Making exclusion explicit and declarative keeps the explorer's concept set curated and trustworthy without destructive file operations.

### Success Criteria

- [x] A concept ID added to the omit file is absent from every explorer surface after re-extraction and server restart, with no other edits.
- [x] A concept ID removed from the omit file returns to the explorer (subject to normal extraction) with no other edits.
- [x] Concepts 26, 27, 34, and 38 are omitted as the initial set.
- [x] Reviewers can see, in one file, exactly which concepts are excluded and why.

### Priority

P2 — quality-of-curation improvement, not blocking other pipeline work. No dependencies on active work items.

---

## Problem Statement

### Current State

- **Extraction** (`extract_explorer_data.py`): `discover_concepts()` walks `analyses/` and writes `data/{id}.json` for every concept that has `model_setup.py` or `analysis.md`. The only existing skip is the per-concept `Comparison-Status: pending-design-point` frontmatter check — there is no project-level way to exclude a concept regardless of its frontmatter.
- **Visualization** (`server.py`): `_load_data()` globs `data/*.json` (minus four known non-concept filenames) and renders whatever is present; `_load_taxonomy()` loads `concept_registry.json` + `decision_tree.json` and builds the constellation and decision tree from them. A concept is shown if its files exist, with no exclusion hook.
- The four target concepts are in inconsistent states, which is exactly why piecemeal deletion fails: 26 and 27 have data files and appear in the taxonomy; 34 has a data file but is not in the taxonomy; 38 has no data file but is still in the taxonomy. No single existing action hides all four everywhere.

### Desired Outcome

One declarative omit file, read independently by the extractor and the server, that removes a listed concept from extraction output and from every rendered surface — profiles, comparison, manifest, parameter index, constellation map, and decision tree.

---

## Scope

### In Scope

- A new declarative omit-list data file (e.g. `omit_list.yaml`) under `exploration/concept_explorer/`, mapping concept ID → reason, matching the existing `parameter_display_registry.yaml` convention.
- A shared loader for the omit list in `models.py` (the module both the extractor and the server already import), returning the set of omitted IDs.
- **Extraction enforcement:** the extractor skips omitted concepts so it does not write (or refresh) their `data/{id}.json`, and reports what was omitted (consistent with the existing skipped-concepts report).
- **Server enforcement (everywhere):** omitted IDs are excluded from the loaded concept set (profiles, comparison), and therefore from the in-memory manifest and parameter index built from it; and excluded from the taxonomy — filtered out of the registry before similarity/constellation computation, and pruned from the decision tree — so they do not appear in the constellation map or decision tree.
- Initial omit set populated with 26, 27, 34, 38.

### Out of Scope

- Deleting or modifying any files under `analyses/` or any existing files under `data/` (omitted concepts' stale data files are left as-is).
- Per-view or partial omission (e.g. "hide from comparison but keep in the map"). Omission is all-or-nothing per concept.
- A UI control or runtime toggle for editing the omit list; it is an at-rest config file, applied at extraction time and at server startup.
- Changing the upstream pipeline that generates `concept_registry.json` / `decision_tree.json`; the server filters them at load time rather than regenerating them.

### Edge Cases & Considerations

- **Empty or missing omit file:** treated as "omit nothing" — the explorer behaves exactly as today.
- **Omit ID with no matching concept anywhere:** harmless no-op; should not error (allows pre-listing an ID before its analysis exists, or keeping an ID after its artifacts are gone).
- **Suffixed IDs** (e.g. `17a`, `20b`): the omit list matches on the same canonical concept ID string the rest of the system uses (`parse_concept_id`), so suffixed IDs are supported.
- **ID typing:** numeric-looking IDs like `26` must match consistently whether parsed from filenames or read from YAML (avoid int-vs-string mismatch).
- **Decision-tree pruning:** the tree is a nested structure keyed/leafed by concept IDs; pruning must remove omitted concepts without corrupting the tree for the remaining concepts.

---

## Requirement Selection Notes

The normative requirements below fix the two things the user was explicit about — a single source of truth, and two independent enforcement points covering *everything* — plus the non-destructive constraint on existing files. The mechanics of *how* the loader is shared, how the decision tree is pruned, and the exact file/format details are intentionally left to design.

---

## Requirements

### Functional Requirements

1. **FR-1:** The set of omitted concepts MUST be defined in a single declarative data file under `exploration/concept_explorer/`, where each entry is a concept ID with an associated human-readable reason.
2. **FR-2:** Adding or removing a concept from the explorer's exclusion MUST require editing only that one file — no code changes.
3. **FR-3:** The extractor MUST NOT write or refresh `data/{id}.json` for any omitted concept, and MUST report which concepts were omitted.
4. **FR-4:** The server MUST exclude omitted concepts from the loaded per-concept data, and therefore from concept profiles, comparison, the manifest, and the parameter index.
5. **FR-5:** The server MUST exclude omitted concepts from the taxonomy — they MUST NOT appear in the constellation map or the decision tree, and MUST NOT participate in similarity/constellation computation.
6. **FR-6:** The two enforcement points (extraction per FR-3, server rendering per FR-4/FR-5) MUST each read the omit list and enforce it independently, with no runtime or ordering dependency between them.
7. **FR-7:** Omitting a concept MUST NOT delete or modify any file under `analyses/`, nor any existing file under `data/`.
8. **FR-8:** An empty/absent omit file MUST behave as "omit nothing," and an omit ID matching no concept MUST be a no-op rather than an error.
9. **FR-9:** The initial omit set MUST contain concept IDs 26, 27, 34, and 38.

### Non-Functional Requirements

- The omit-list loader SHOULD live in `models.py` so the extractor and the server share one implementation rather than duplicating parse logic.
- The omit file format SHOULD follow the existing `parameter_display_registry.yaml` convention for consistency.

---

## Acceptance Criteria

### Core Functionality

- [x] With 26, 27, 34, 38 in the omit file: re-running extraction does not (re)write `data/26.json`, `27.json`, `34.json`, `38.json`, and prints that they were omitted.
- [x] With the same omit file and the server started: none of 26, 27, 34, 38 appear in any concept profile, the comparison view, the manifest, the parameter index, the constellation map, or the decision tree.
- [x] Pre-existing `data/26.json`, `data/27.json`, `data/34.json` remain on disk, unmodified, after extraction and server startup.
- [x] Removing a concept from the omit file (and re-extracting / restarting) makes it reappear in the explorer.
- [x] An empty omit file (or none) yields explorer behavior identical to today.
- [x] An omit entry for a non-existent concept ID does not raise an error.

### Quality & Integration

- [x] Existing tests continue to pass.
- [x] Extraction and server enforcement each work when exercised in isolation (independence per FR-6).

---

## Next-Stage Handoff

**Settled in this spec:**

- One declarative omit file is the single source of truth; ID → reason shape.
- Two independent enforcement points; both honor the list; omission is total (extraction + all server surfaces including taxonomy).
- Existing on-disk files are never touched by this feature.
- Initial set is 26, 27, 34, 38.

**Design must figure out:**

- The exact file name/schema and the shared loader's signature/location in `models.py`.
- Where in `discover_concepts()` the extraction skip sits relative to the existing `pending-design-point` skip, and how it reports omissions.
- The concrete filter points in `_load_data()` and `_load_taxonomy()`, and the decision-tree pruning algorithm that removes omitted IDs without corrupting the remaining tree.
- ID normalization so YAML-sourced IDs match `parse_concept_id` output (string vs int).

**Watch-outs for design:**

- Decision-tree pruning is the only non-trivial transform — get its shape from the actual `decision_tree.json` structure before designing.
- Manifest and parameter index are built in-memory from the loaded concepts, so filtering at the concept-load step should cover them automatically — verify rather than filtering them a second time.
- Keep the loader tolerant: missing file, empty file, and unknown IDs are all valid no-ops, not errors.

---

## Related Artifacts

- **Design:** `.project/active/concept-explorer-omit-list/design.md` (to be created)
- **Code:** `exploration/concept_explorer/extract_explorer_data.py`, `server.py`, `models.py`
- **Convention reference:** `exploration/concept_explorer/data/parameter_display_registry.yaml`

---

**Next Steps:** After approval, proceed to `/_my_design`
