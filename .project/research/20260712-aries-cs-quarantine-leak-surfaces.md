# Research: Source-discovery leak surfaces for a quarantined ingestion

**Date:** 2026-07-12
**Context:** ARIES-CS hold-out ingestion (`.project/active/aries-cs-holdout/`), stellarator MBSE demo concept (`.project/concepts/stellarator-mbse-demo.md`)
**Method:** Read-only survey of the main checkout: source-discovery code paths, ingestion machinery, sync scope, skills, and prompt templates.

## Question

If ARIES-CS papers are ingested into the repo but must stay out of all model-development and research agent context until a deliberate reveal, through which surfaces could they leak, and what placement avoids them?

## Findings

### 1. Scripted discovery (concept-analysis pipeline)

- `find_sources()` (`exploration/concept_analysis/scripts/lib/sources.py:9`) globs `knowledge/concept_research/{concept-id}/iter-*/sources/*.md` and injects the path list into the gap-check, analysis, review, and synthesis prompts.
- **Auto-integration**: `detect_new_sources()` (`scripts/lib/iteration.py:160`) diffs current sources against the prior `verdict.json`; the resume loop (`scripts/lib/loop.py:108,154`) spawns one integration subagent per new source. Dropping a file into any `iter-*/sources/` doesn't just expose it — it actively pulls it into the analysis on the next run.
- **Whole-index injection**: `run_analysis.py:240` injects the *entire* `knowledge/SOURCE_INDEX.md` into every concept's gap-check prompt (`prompt_templates/gap_check.md:48`). A mere registry entry leaks repo-wide, no file read needed. This is the widest single surface.
- `resurface_orig.py:172` globs `knowledge/concept_research/**/iter-*/sources/*.orig.md` across all concepts.

### 2. Index-keyed discovery (agentic-mbse commands)

`/research`, `/spec-model`, `/design-model`, `/plan-model`, `/audit-models`, `/backlog`, `/onboard`, `/manage-sources` all discover sources via `knowledge/SOURCE_INDEX.md` entries (e.g. research.md:50-51: read "local materials in `knowledge/sources/` and paths listed in SOURCE_INDEX.md"). Unregistered directory → invisible; registered → exposed to all of them.

### 3. Skill-driven discovery

- `concept-research-navigation` skill (triggers on "check sources", "dossier", …): protocol is check `knowledge/concept_research/SOURCE_INDEX.md` **or glob `knowledge/concept_research/*/dossier.md`**, then read ALL `iter-NN/sources/*.md`. Anything shaped like a concept dir under `concept_research/` gets enumerated; a dir outside `concept_research/` does not.
- `project-structure` and `source-traceability` skills point sessions at `knowledge/SOURCE_INDEX.md` and describe the `knowledge/` layout — an unexplained new directory there invites ad-hoc exploration even with no glob hitting it.

### 4. Index regeneration

`scripts/migrate_research.py` `generate_source_index()` (lines 65-133) scans **every subdirectory** of `knowledge/concept_research/` (no filter) on `--reindex` and writes each into `concept_research/SOURCE_INDEX.md` — even a non-`iter-*` dir gets an entry (revealing its name).

### 5. Ingestion machinery — both standard paths auto-register

- `scripts/zotero_ingest.py`: extracts into `knowledge/sources/{slug}/output.md`, then unconditionally appends to `knowledge/SOURCE_INDEX.md` (`append_source_index_entry()`, line 210) and `knowledge/MANIFEST.jsonl` (`scripts/zotero_lib.py:20-21`).
- `run_analysis.py add-source` (`cmd_add_source`, line 981): extracts into `{concept}/iter-NN/sources/` — immediately visible to `find_sources()` and auto-integrated (finding 1).
- Consequence: a quarantined ingestion cannot use either path; it needs a bespoke landing zone with deliberate non-registration.

### 6. R2 sync scope and the mirror hazard

`scripts/sync_research.sh:28-29` hardcodes `knowledge/concept_research` ↔ `r2:1cfe-research/concept_research`, binaries only, **mirror semantics** (`rclone sync`): a `pull` deletes local binaries not on R2; a `push` from a machine lacking a dir purges it from R2. A quarantine dir *inside* `concept_research/` risks having its binaries deleted by any pull before first push. A dir *outside* is never synced — but then nothing backs it up, and the binary gitignore lives at `knowledge/concept_research/.gitignore` (not repo root), so out-of-tree PDFs are **git-tracked by default** unless a local `.gitignore` is added.

### 7. No existing quarantine precedent

Greps for quarantine/holdout/do-not-read as a source mechanism: none. The "blocklist" hits are the spec-key blocklist (parameter-level workarounds in `prompt_templates/model_setup_costingfe.md:213`, `scripts/lib/canonical_spec_keys.py`). Closest precedent for negative instructions is the analyst-patch pattern (e.g. `09-qi-stellarator-hts/iter-03/sources/analyst-patch-spec-anchors.md`, `do_not_set:` directives) — but it *delivers* rules by being an injected source file, i.e. via the positive channel. There is no precedent for "files agents must not discover."

### 8. Second-order leakage

Once any agent session has seen quarantined content, it can escape via derived artifacts: memory files (`exploration/concept_analysis/memory/*.md` are injected into later analyses), dossiers, `knowledge/KNOWLEDGE.md` DI-entries, comparables (`derive_comparables.py`), and the auto-memory. A quarantine protocol must govern derived artifacts, not just source files. (Mitigated for this work item by the raw-PDFs-only decision: no agent reads the content at ingestion time.)

## Verdict

An out-of-tree directory (e.g. `knowledge/holdout/` — exact name/path is a design choice) is invisible by default to every scripted and index-keyed surface, provided it is: never registered in either SOURCE_INDEX or MANIFEST.jsonl, never placed under `knowledge/concept_research/`, and never routed through `zotero_ingest.py` or `add-source`. Residual risks: git-tracks binaries unless locally gitignored (and then nothing backs them up); advisory-only protection against free exploration (a README stating the quarantine is the only soft control); second-order leakage once content is ever read.

## Paper availability (verified 2026-07-12)

All four core ARIES-CS papers (FS&T Vol 54 No 3, 2008 special issue) are free PDFs on the ARIES program site, pattern `http://aries.ucsd.edu/LIB/REPORT/JOURNAL/FST/08-FST-{Najmabadi,Ku,Lyon,Raffray}.pdf` (mirrors: qedfusion.org, aries.pppl.gov — both serve the same `/DOCS/ARIES-CS/bib.shtml`). OSTI landing pages (1014258 = Lyon 2008; 20849901 = Najmabadi 2005 initial-results, FS&T 47) carry no direct full text.
