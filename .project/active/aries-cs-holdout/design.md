# Design: ARIES-CS Hold-Out Ingestion and Quarantine Protocol

**Status:** Implemented (2026-07-12; see Implementation Completion below)
**Owner:** Reid W
**Created:** 2026-07-12
**Branch:** feat/stellarator-mbse-demo

## Overview

Put four ARIES-CS PDFs in a directory nothing scans, record their checksums, and write one protocol file that carries the rules (blocked contexts, barred/admissible lists, reveal procedure, contamination inventory). Deliberately boring.

## Related Artifacts

- Spec: `.project/active/aries-cs-holdout/spec.md` (+ `spec-review.md`, L1-1 resolved clean-room)
- Research: `.project/research/20260712-aries-cs-quarantine-leak-surfaces.md` — the full leak-surface map; not restated here

## Research Findings

All in the research doc. The three facts the design rests on: (1) every scripted discovery surface selects sources by `concept_research/` globs or SOURCE_INDEX entries, so an unregistered directory elsewhere is invisible; (2) both standard ingestion paths auto-register, so ingestion here is `curl` + checksums, nothing more; (3) out-of-tree binaries are git-tracked by default and untouched by R2 sync.

## Core Concept

A single new directory, `knowledge/holdout/aries-cs/`, holds the four PDFs (git-tracked), a content-free `manifest.json`, a `README.md` that says "quarantined — do not read," and a `PROTOCOL.md` that is the one home for all the rules. One line in `CLAUDE.md` points at it so every session learns the directory exists and is off-limits. Enforcement is advisory (accepted in the spec); the protocol makes violations *detectable* by being explicit about what was sealed and when. There is no script, no hook, no new sync — four files and a rule sheet.

## Key Bets

- **B1.** Advisory controls (README + PROTOCOL + CLAUDE.md line) are enough to keep agent sessions out of one clearly-marked directory. *If false → the blind is voided by an accidental read; remedy is escalation to a deny-read hook, not more documents.* (Spec accepts this residual risk explicitly.)
- **B2.** The leak-surface survey is complete — no scanner beyond those mapped enumerates `knowledge/holdout/`. *If false → the PDFs leak into a prompt without any rule being broken.* Mitigated by the post-ingest verification checklist.

## Key Decisions

- **D1. Location: `knowledge/holdout/aries-cs/`.** Outside `concept_research/` (reindex, navigation skill, R2 mirror all scan there), unregistered in any index. *Rejected: outside `knowledge/` entirely — no leak-surface advantage, and `knowledge/` is where a future reader will look for source material.*
- **D2. Storage: git-track the four PDFs.** ~10–15 MB once, durable, survives clones, zero new machinery. *Rejected: gitignore + R2 backup — builds sync/backup machinery for four files and reintroduces mirror-deletion hazards.*
- **D3. Blocklist delivery: `PROTOCOL.md` as the single rule home**, referenced three ways: the in-dir `README.md` (for stumblers), one `CLAUDE.md` line (reaches every session), and a Required Reading entry in each demo work item (reaches demo sessions specifically). *Rejected: PreToolUse deny-read hook — more machinery than the risk warrants today; named in PROTOCOL as the escalation if the blind is ever violated.*
- **D4. Manifest: one-time generation, committed `manifest.json`** (per file: filename, source URL, SHA256, bytes, page count). Page count via pypdf metadata read — no text extraction. *Rejected: a kept ingestion script — this runs once; the exact commands live in the plan and are recorded in PROTOCOL for provenance.*
- **D5. Reveal: edit PROTOCOL.md.** Its frontmatter carries `status: sealed`; reveal = owner flips it to `revealed` with date and a dated log entry. Post-reveal extraction lands inside `knowledge/holdout/aries-cs/extracted/` and gets registered (or not) as a deliberate later-stage decision. *Rejected: separate reveal artifact — one more file for no gain.*

## Architecture

```
knowledge/holdout/aries-cs/
├── README.md          # "Quarantined. Do not read the PDFs. Rules: PROTOCOL.md"
├── PROTOCOL.md        # status, rules, barred/admissible lists, inventory, reveal log
├── manifest.json      # sha256 / bytes / pages / source URL per PDF
└── *.pdf              # 08-FST-{Najmabadi,Ku,Lyon,Raffray}.pdf, git-tracked
```

`PROTOCOL.md` contents (the only file with substance):
1. **Status**: `sealed` | `revealed`, with dates.
2. **Blocked contexts**: all demo model-development and research sessions until the hold-out comparison stage.
3. **Clean-room lists**: barred and admissible paths, copied from the spec's clean-room `[NEED]` as concrete globs (barred: this directory's PDFs, `exploration/concept_analysis/analyses/09-qi-stellarator-hts/**`, the two abstract stubs, the Helios comparison extraction; barred-by-default with documented-exception: Waganer doc, Araiinejad/Shirvan doc. Admissible: the clean 09 source extractions, 1costingFE, WI-009 library, PyFECONS).
4. **Derived-artifact rule**: no memories, dossiers, `KNOWLEDGE.md` insights, or comparables may reference sealed/barred content; binds reveal-stage sessions too.
5. **Contamination inventory**: the spec's list, verbatim.
6. **Reveal procedure + log**: owner-triggered; flip status, log date and file list.
7. **Provenance**: download commands, date, mirror URLs.

Touched outside the new directory: one `CLAUDE.md` line ("`knowledge/holdout/` is quarantined hold-out material — never read, cite, or register its contents; see `knowledge/holdout/aries-cs/PROTOCOL.md`").

## Required Invariants

- No entry for `knowledge/holdout/` ever appears in `knowledge/SOURCE_INDEX.md`, `knowledge/concept_research/SOURCE_INDEX.md`, or `knowledge/MANIFEST.jsonl` while sealed.
- Manifest SHA256s match the committed PDFs (checkable any time without reading content).
- `PROTOCOL.md` status is `sealed` until the owner flips it; every demo work item created while sealed lists PROTOCOL.md as Required Reading.

## Component Overview

Covered by Architecture — four static files plus one CLAUDE.md line. No code components.

## Non-Goals

Spec's list applies unchanged: no extraction, no reveal execution, no deletion of existing contaminated artifacts, no concept-analysis pipeline changes, no generalized quarantine facility, no enforcement hooks (escalation path only).

## Implementation Notes

- Download from `https://qedfusion.org/LIB/REPORT/JOURNAL/FST/08-FST-{Najmabadi,Ku,Lyon,Raffray}.pdf` (aries.ucsd.edu / aries.pppl.gov as mirror fallbacks); record which mirror served each file.
- Page count: `pypdf.PdfReader(f).get_num_pages()` — metadata only; do not render or extract text. pypdf availability: `uv run python -c "import pypdf"`; `uv add pypdf` if missing.
- The ingesting session must not open the PDFs' content; checksum and page count only. Ingestion is not model development, and PROTOCOL says so.
- Verification after ingest (the spec's criterion 3): grep both SOURCE_INDEX files and MANIFEST.jsonl for `holdout|aries-cs` (only pre-existing 09 abstract entries may match); confirm `find_sources('09-qi-stellarator-hts')` output is unchanged; confirm `migrate_research.py --reindex` dry-run output is unchanged (holdout is outside its scan root).

## Potential Risks

- **Accidental read by a curious agent** (B1): advisory-only; mitigation is the three-point delivery (D3) + escalation path named in PROTOCOL.
- **Unmapped scanner** (B2): mitigation is the verification checklist; residual risk accepted.
- **Mirror rot**: three mirrors known; PDFs are committed, so this risk exists only until first commit.

## Integration Strategy

Nothing existing changes behavior. The directory is inert until reveal; demo work items reference PROTOCOL.md in Required Reading as they are created.

## Validation Approach

The spec's six success criteria are the checklist; each maps directly to a file or verification step above. No tests to write — the "test" is the post-ingest verification commands, whose output gets pasted into the close-out report.

## Next-Stage Handoff

- **Fixed**: location, git-tracking, PROTOCOL.md as single rule home, manifest fields, the three-point blocklist delivery.
- **Open**: none that block implementation; exact README/PROTOCOL wording is the implementer's.
- **Risk to check first**: download the four PDFs and checksum them before writing any documentation — if a mirror serves HTML-instead-of-PDF, that's the only real-world unknown here.

---
Next Step: After approval → `/_my_implement` (a plan file would be ceremony for this; the design's checklist is the plan).

## Implementation Completion

**Completed:** 2026-07-12 (single phase — the design's checklist)

**Changes made:**
- Created `knowledge/holdout/aries-cs/` with the four PDFs (5.9 MB total, git-tracked), `manifest.json`, `README.md`, `PROTOCOL.md`
- Added the quarantine line to `CLAUDE.md` (Domain Sources section)

**Deviations from plan:**
1. **All three live mirrors are dead** (qedfusion.org now WordPress, 404 on `/LIB/**`; aries.ucsd.edu unreachable; aries.pppl.gov 401). PDFs retrieved from Internet Archive snapshots of the canonical aries.ucsd.edu URLs using the Wayback `id_` modifier (raw original bytes). Snapshot URLs recorded per file in the manifest and PROTOCOL §7. This is the design's named "mirror rot" risk, hit at ingestion time; the archive copy of the exact spec-verified URL is the closest faithful substitute.
2. **pypdf run ephemerally** (`uv run --with pypdf`) instead of `uv add pypdf` — no permanent dependency for a one-time metadata read.
3. **Two barred-list additions beyond the spec's lists**, both under the spec's own principle ("any artifact carrying ARIES-CS-specific design or cost data is inadmissible"), both flagged for owner review:
   - `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/**` — the Helios design-paper extraction carries substantive ARIES-CS design facts (17 mentions: coil mass, port/maintenance scheme, comparisons), same class as the barred iter-02 Helios comparison.
   - `knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/academia-144327326-the-aries-cs-compact-stellarator-fusion*` — a ~6 KB academia.edu landing-page extraction of the ARIES-CS overview paper in concept 36's sources; surfaced by the post-ingest index grep; also added to the contamination inventory.

**Verification (spec criterion 3 + design checklist) — all pass:**
1. Index greps for `holdout|aries-cs`: zero `holdout` matches in `knowledge/SOURCE_INDEX.md`, `knowledge/concept_research/SOURCE_INDEX.md`, `knowledge/MANIFEST.jsonl`; only pre-existing 09/36 aries-cs source entries match.
2. `find_sources('09-qi-stellarator-hts')`: 16 paths, all pre-existing, no holdout.
3. Reindex: `migrate_research.py` has no `--reindex --dry-run` combination (`--dry-run` short-circuits to the migration report), so the check was run as a real `--reindex` + git diff: regenerated index contains zero `holdout` mentions (the large diff is pre-existing `[PDF]`→`[extraction]` label drift); file restored to committed state afterward.
4. In-place SHA256 + byte sizes match `manifest.json` for all four PDFs; pypdf page counts (18/21/31/22) match the FS&T Vol 54 No 3 TOC exactly.
5. R2 sync scope: `sync_research.sh` hardcodes `LOCAL_DIR=knowledge/concept_research` — `knowledge/holdout/` is untouchable by `pull`. PDFs confirmed not gitignored (`git check-ignore` negative), so git-tracking is the durability mechanism (D2); durable once committed.

**Open for owner:**
- Ratify the two barred-list additions (deviation 3).
- The concept-36 ARIES-CS stub is a contamination-inventory addition the spec didn't know about — noted in PROTOCOL §5.
- Changes are uncommitted; the PDFs' durability (D2) starts at first commit.
