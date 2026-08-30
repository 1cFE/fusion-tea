---
id: 0008
title: A non-Zotero source's durable identity is the SHA-256 of its raw bytes as fetched
date: 2026-08-25
owner: Reid W
status: active
amended_by: []
superseded_by: null
provenance: "[AGENT], delegated by the owner at Align (goal-research-seam align.md:8, \"make sure you use your judgement\")"
seams: []
supersedes: null
promoted_to: null
---

## Decision

Every registered source carries `source_id` = SHA-256 of the raw source bytes **as fetched**, taken from the extraction frontmatter (`content_hash_sha256`), and a separate `raw_artifact_sha256` = digest of the raw artifact **as stored** in the repository. The two are different bytes by construction for any non-UTF-8 page (`agentic-mbse` re-encodes `raw.html`) and are never compared to each other. Dedupe order: `zotero_key` when supplied → `source_id` → `source_url` (exact, then scheme/host-lowercased and fragment-stripped, pre-fetch only). `zotero_key` remains on Zotero rows and is absent otherwise.

## Why

`MANIFEST.jsonl` was keyed on `zotero_key`, so a source that never passed through Zotero — a URL capture, a hand-supplied PDF — had no durable identity: duplicates could not be detected and provenance could not be re-verified (goal-research-seam spec R-B3). The owner deferred the mechanism to design at Align (`.project/active/goal-research-seam/align.md:8`). Decided in `.project/active/goal-research-seam/design.md` D1/D2, confirmed through design review (C1 forced the identity/integrity split below).

Identity from the producer's hash of the fetched bytes makes duplicate detection and re-fetch verification the same check, with no service call and no manual step — which is what lets the whole registration chain be proven offline (spec R-E1). The stored-artifact digest gives any later reader an integrity check recomputable from the repository alone. A single hash was the original proposal and was measured false in design review (C1: frontmatter hash ≠ `raw.html` digest on an `iso-8859-1` fixture); the split is what survives that measurement.

## Invariants established

- `knowledge/MANIFEST.jsonl` — row schema: `source_id`, `source_kind`, `source_url`/`origin_path`, `raw_sha256`, `raw_artifact_sha256`, `extract_sha256`.
- `scripts/zotero_lib.py` — loaders tolerate rows without `zotero_key`; `load_manifest_rows()`.
- `scripts/source_registry.py` — dedupe order, provenance verification, `verify`.
- `knowledge/SOURCE_INDEX.md` — extended-metadata fields `Source ID`, `Raw SHA256`, `Raw Artifact SHA256`.

Manifest readers must tolerate rows without `zotero_key` (landed with a characterization test before the first non-Zotero row). Duplicates are detected before a second entry is written. A re-fetch whose bytes changed is refused as a duplicate rather than superseded — supersession stays out of scope (upstream `pm supersede-insight` stub). The identity hash is trusted from the producer's frontmatter; the stored artifact's digest is the only hash a reader recomputes.

## Rejected alternatives

- **URL-derived key** — no identity at all for local PDFs; breaks on redirects and mirrors (the WI-031 iter.org entry already covers one source at two URLs).
- **Push every URL source through Zotero first** — adds a network and API-key step into a path required to be provable offline, and Zotero workflow redesign is an epic non-goal.
