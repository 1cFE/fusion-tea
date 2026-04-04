# Implementation Plan: Source Replacement Completion

**Status:** Draft
**Created:** 2026-04-03
**Last Updated:** 2026-04-03

## Source Documents
- **Spec:** `.project/active/source-replacement/spec.md`
- **Prior plan:** `.project/active/source-replacement/plan.md` — covers concepts 01-22 (complete) plus the manifest for 23-36
- **arXiv HTML fix:** `agentic-mbse` commit `1b155a0` (2026-03-29) — routes `arxiv.org/html/` URLs through Pandoc instead of trafilatura
- **arXiv image downloading:** `agentic-mbse` feature (2026-04-04) — downloads referenced images to `images/` subdir, rewrites markdown refs to local paths
- **Extraction warnings:** `agentic-mbse` feature (2026-04-04) — `ExtractionResult.warnings` list surfaces partial failures (e.g., image 404s) in CLI output and `metrics.json`. Replaces silent `log.warning()` + stack traces.

## Implementation Strategy

**No design document** — this is an operational task continuing the source replacement work. The plan IS the operational document.

**Context:**
Concepts 01-22 (124 files) are replaced. Concepts 23-36 (76 files) remain. During execution, we discovered that trafilatura destroys tables, equations, and scientific notation from arXiv HTML papers. The fix was committed to agentic-mbse *after* 9 arXiv HTML sources in concepts 01-22 had already been extracted with the broken pipeline. These need re-extraction.

Additionally, `knowledge/concept_research/SOURCE_INDEX.md` was auto-generated during migration but needs validation against the actual post-replacement disk state and enrichment with source URLs from YAML frontmatter.

**Phasing Rationale:**
Validate the fix first (Phase 1) to confirm no information loss. Then re-extract the 9 affected files (Phase 2) while quality is fresh in mind. Run one complete concept end-to-end as a dry run (Phase 3) to validate the full workflow works in the new `knowledge/concept_research/` location. Then bulk-execute remaining concepts (Phase 4). Finally, reconcile SOURCE_INDEX.md against reality (Phase 5).

**Execution Model:**
Phases 1-3 are human-validated (user reviews extraction quality). Phase 4 follows the established workflow from the prior plan. Phase 5 is scripted.

---

## Phase 1: Validate arXiv HTML Fix + Image Downloading

### Goal
Confirm the Pandoc routing fix produces materially better output for arXiv HTML papers AND that the new image downloading feature saves figures locally with rewritten markdown references. This de-risks Phase 2 (re-extracting 9 files) and Phase 4 (concept 29 has an arXiv HTML source).

### Target
**Concept 11, file:** `knowledge/concept_research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions`

This is the exact paper (`arxiv.org/html/2411.06644v1`) cited in the agentic-mbse fix commit as the verification case. Re-running after the arXiv image downloading feature (spec: `agentic-mbse/.project/active/web-extraction-quality/spec-arxiv-images.md`) to validate images are saved locally.

### Steps

- [x] **Re-extract with fixed pipeline + image downloading:**
  ```bash
  uv run agentic-mbse extract https://arxiv.org/html/2411.06644v1 \
    --save-source \
    --output knowledge/concept_research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions/
  ```
  - This overwrites `output.md` and `raw.html` in the companion dir
  - Should now also create `images/` subdirectory with downloaded PNGs

- [x] **Update top-level .md:** Copy new `output.md` over the top-level `.md`:
  ```bash
  cp knowledge/concept_research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions/output.md \
     knowledge/concept_research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions.md
  ```

- [ ] **User reviews the diff:**
  - Tables: Do columns align? Are parameter names present? Is scientific notation preserved (not `1.66 1020`)?
  - Equations: Are they rendered or garbled?
  - Overall: Line count comparison, content completeness
  - Images: Are figures available locally for agent inspection?
  - Verdict: PASS (proceed to Phase 2) or FAIL (debug before continuing)

### Validation
- [x] New extraction has YAML frontmatter with `source`, `content_hash_sha256`, `backend`
- [x] Tables render with correct columns and scientific notation
- [x] Line count is similar or better than current extraction
- [x] No content loss relative to current extraction (should only be gains)
- [x] `images/` subdirectory exists in companion dir with downloaded PNGs
- [x] Image count > 0 (paper has ~10 figures) — **21 images downloaded**
- [x] Markdown image references point to local `images/` paths (not remote arXiv URLs)

**What We Know After This Phase:**
The arXiv HTML Pandoc fix works end-to-end with image downloading in the fusion-tea extraction workflow. Safe to re-extract the other 8 affected files.

---

## Phase 2: Re-extract Affected arXiv HTML Sources

### Goal
Replace the 9 arXiv HTML extractions that used the broken trafilatura pipeline with Pandoc-routed extractions.

### Affected Files

**6 unique papers, 9 file locations** (some papers appear in multiple concepts):

| # | Concept | File | arXiv URL | Also used by |
|---|---------|------|-----------|-------------|
| 1 | 05-planar-coil-stellarator | `iter-01/sources/thea-energy-helios-arxiv-2512-08027` | `2512.08027v1` | concept 09 (#4) |
| 2 | 05-planar-coil-stellarator | `iter-02/sources/thea-energy-canis-prototype-arxiv-2503-18960` | `2503.18960v1` | — |
| 3 | 07-maglif | `iter-01/sources/arxiv-2408-15206-pulsed-magnetic-fusion` | `2408.15206v1` | — |
| 4 | 09-qi-stellarator-hts | `iter-02/sources/helios-stellarator-comparison` | `2512.08027v1` | same paper as #1 |
| 5 | 11-magnetic-mirror | `iter-01/sources/arxiv-2411-06644-confinement-predictions` | `2411.06644v1` | — (done in Phase 1) |
| 6 | 12-levitated-dipole | `iter-01/sources/arxiv-2508-17691-junior-design-results` | `2508.17691v1` | — |
| 7 | 12-levitated-dipole | `iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants` | `2602.20564v1` | concept 12 (#8), concept 19 (#9) |
| 8 | 12-levitated-dipole | `iter-02/sources/arxiv-2602-20564-plasma-state-clarification` | `2602.20564` | same paper as #7 |
| 9 | 19-orbital-levitated-dipole | `iter-02/sources/dipole-reactor-heating-energy-conversion` | `2602.20564` | same paper as #7 |

### Steps

For each file (skipping #5, done in Phase 1):

- [x] **#1** — `05/iter-01/sources/thea-energy-helios-arxiv-2512-08027`:
  - Extract: `uv run agentic-mbse extract https://arxiv.org/html/2512.08027v1 --save-source --output <companion-dir>/`
  - Copy `output.md` → top-level `.md`
  - Quick quality check: tables, equations, images present? — 12 images

- [x] **#2** — `05/iter-02/sources/thea-energy-canis-prototype-arxiv-2503-18960`:
  - Extract: `https://arxiv.org/html/2503.18960v1`
  - Copy + quality check — **0 images** (all 18 failed with 404: double-slash URL bug in agentic-mbse)

- [x] **#3** — `07/iter-01/sources/arxiv-2408-15206-pulsed-magnetic-fusion`:
  - Extract: `https://arxiv.org/html/2408.15206v1`
  - Copy + quality check — 11 images

- [x] **#4** — `09/iter-02/sources/helios-stellarator-comparison`:
  - Same paper as #1 — copy #1's extraction output (`output.md`, `raw.html`, and `images/`)
  - Verify byte counts match — 180,588 bytes, 12 images

- [x] **#6** — `12/iter-01/sources/arxiv-2508-17691-junior-design-results`:
  - Extract: `https://arxiv.org/html/2508.17691v1`
  - Copy + quality check — 7 images

- [x] **#7** — `12/iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants`:
  - Extract: `https://arxiv.org/html/2602.20564v1`
  - Copy + quality check — 23 images

- [x] **#8** — `12/iter-02/sources/arxiv-2602-20564-plasma-state-clarification`:
  - Same paper as #7 — copy #7's extraction output (including `images/`)
  - Verify byte counts match — 268,048 bytes, 23 images

- [x] **#9** — `19/iter-02/sources/dipole-reactor-heating-energy-conversion`:
  - Same paper as #7 — copy #7's extraction output (including `images/`)
  - Verify byte counts match — 268,048 bytes, 23 images

- [ ] **User spot-check:** Pick 1-2 re-extracted papers and verify table/equation/image quality matches Phase 1 expectations

### Validation
- [x] All 9 files have updated extraction timestamps in YAML frontmatter
- [x] Shared papers (#1=#4, #7=#8=#9) have identical byte counts
- [x] All companion dirs have `images/` subdirectories with downloaded figures (except #2 — see bug below)
- [x] No content regressions (line counts should be similar or better)
- [x] Commit re-extractions — `8aba464`

### Known Limitation: Paper #2 (2503.18960) images unavailable on arXiv
All 20 images for this paper return 404 from arXiv. This is NOT an agentic-mbse bug — arXiv's HTML viewer isn't serving the images for this paper (they exist in the e-print source tarball but not via HTTP). The URL construction is correct (`/html/2503.18960v1/fig_canis_render_detail.png`). The HTML source has `src=".//fig_..."` which is how LaTeXML generates paths when images are at the document root. Other papers (e.g., 2411.06644v1) work because their images are under an `extracted/` subdirectory. Text/markdown extraction is unaffected; only local image copies are missing for this one paper.

After adding the `ExtractionResult.warnings` feature, these failures are now cleanly surfaced in CLI output (`⚠ 20 warning(s)`) and captured in `metrics.json` — no more silent failures or stack traces.

**What We Know After This Phase:**
All arXiv HTML sources across concepts 01-22 now use the Pandoc pipeline. The trafilatura quality issue is fully resolved for completed work.

---

## Phase 3: End-to-End Dry Run — Concept 29

### Goal
Validate the full source replacement workflow works in the new `knowledge/concept_research/` location with the fixed pipeline. Concept 29 (negative-triangularity-tokamak) has 7 files spanning URL, SEARCH, CITE, and arXiv HTML categories — exercises all code paths.

### Files

From the original plan manifest (`.project/active/source-replacement/plan.md` lines 566-580):

| # | File | Category | URL |
|---|------|----------|-----|
| 1 | `iter-01/sources/ball-balestri-ohmic-nt-paper.md` | URL | `https://arxiv.org/html/2407.06439v2` |
| 2 | `iter-01/sources/firefly-fusion-diii-d-collaboration.md` | URL | `https://d3dfusion.org/fireflyfusion/` |
| 3 | `iter-01/sources/fusion-energy-base-profile.md` | URL | `https://www.fusionenergybase.com/organizations/firefly-fusion` |
| 4 | `iter-01/sources/greyb-firefly-interview.md` | URL | `https://greyb.com/blog/firefly-fusion-scouted-interview` |
| 5 | `iter-01/sources/venture-kick-profile.md` | URL | `https://www.venturekick.ch/firefly-fusion` |
| 6 | `iter-02/sources/firefly-website-2026.md` | URL | `https://fireflyfusion.energy/` |
| 7 | `iter-02/sources/manta-reference-design.md` | CITE | `arXiv:2405.20243` → `https://arxiv.org/abs/2405.20243` |

### Steps

For each file, follow the established workflow from the original plan (lines 98-107):

- [x] **#1** `ball-balestri-ohmic-nt-paper` — arXiv HTML URL
  - 252 lines vs 27 orig. pandoc-arxiv. 16 images. Full paper text. **YES**

- [x] **#2** `firefly-fusion-diii-d-collaboration` — regular URL
  - 28 lines vs 20 orig. trafilatura. Full page verbatim. **YES**

- [x] **#3** `fusion-energy-base-profile` — regular URL
  - 14 lines vs 16 orig. trafilatura. JS-heavy, thin extraction. **NO**

- [x] **#4** `greyb-firefly-interview` — regular URL
  - 89 lines vs 27 orig. trafilatura. Full interview with quotes. **YES**

- [x] **#5** `venture-kick-profile` — regular URL
  - Extraction FAILED (JS/cookie redirect). WebFetch also failed. Kept original. **NO**

- [x] **#6** `firefly-website-2026` — regular URL
  - 57 lines vs 36 orig. trafilatura. Team/advisors captured but lost About section (JS). **MIXED**

- [x] **#7** `manta-reference-design` — CITE (arXiv paper)
  - arXiv HTML 404 (no HTML version). Fell back to PDF pipeline.
  - 3007 lines vs 62 orig. 62 images, 162 table rows, $1.96. Full 50+ page design study. **YES**

- [x] **Write quality notes** to source replacement report for all 7 files
- [x] **User reviews** extraction quality for the concept — approved 2026-04-04

### Validation
- [x] All 7 files have YAML frontmatter (except #5 which kept original)
- [x] Companion directories exist with `raw.html` or `raw.pdf` + `metrics.json` (6 of 7 — #5 failed)
- [x] `.orig.md` files preserved for 6 of 7 (#5 restored to .md since extraction failed)
- [x] Quality notes written to report
- [x] Commit concept 29

**What We Know After This Phase:**
The full workflow works end-to-end in the migrated directory structure. Any path issues, tooling quirks, or workflow gaps are caught before bulk execution.

---

## Phase 4: Complete Remaining Concepts (23-28, 30-36)

### Goal
Replace all remaining 69 source files (76 minus 7 from Phase 3) across 13 concepts using the established workflow.

### Execution Instructions

Same workflow as Phase 3 and the original plan (lines 98-132). For each file:
1. Rename `.md` → `.orig.md`
2. Extract with `--save-source` into companion dir
3. Copy `output.md` → top-level `.md`
4. WebFetch comparison
5. Quality note to report

**Category-specific instructions** (from original plan lines 98-132):
- **SEARCH**: Read `.orig.md` for context, WebSearch to find original URL, then extract
- **CITE**: Construct URL from arXiv ID or DOI
- **403/paywall**: Ask user for local PDF copy
- **JS-heavy sites**: May produce thin output — note in report, keep original if NO verdict

### Batch Schedule

Process in batches of 3-5 concepts, committing after each batch:

**Batch A (14 files):**
- [ ] 23-laser-icf-nanostructured-target (4 files)
- [ ] 24-dense-plasma-focus (3 files)
- [ ] 25-heavy-ion-beam-icf (3 files)
- [ ] 26-laser-icf-indirect-drive — partial (4 of 7 files)
- Commit

**Batch B (14 files):**
- [ ] 26-laser-icf-indirect-drive — remaining (3 files)
- [ ] 27-polywell (4 files)
- [ ] 28-hts-tokamak-full-hts (2 files)
- [ ] 30-laser-icf-nif-commercialization (3 files)
- [ ] 31-laser-icf-oec-architecture (2 files)
- Commit

**Batch C (17 files):**
- [ ] 32-laser-icf-french-national (5 files)
- [ ] 33-state-backed-tokamak-best (3 files)
- [ ] 34-compact-spherical-tokamak-india (2 files)
- [ ] 35-polomac-magnetic-confinement (3 files)
- [ ] 36-helical-coil-stellarator (4 files)
- Commit

### Known Challenges (from original plan notes)

| Concept | File | Issue |
|---------|------|-------|
| 25 | `intensity-energy-search-results.md` | Original search found nothing — company likely doesn't exist. May not be replaceable. |
| 28 | `energy-singularity-overview.md` | Chinese company site — may extract poorly |
| 33 | `best-research-plan-v1.1-summary.md` | Large PDF — may produce very long extraction |
| 33 | `neo-fusion-company-profile.md` | Chinese company site — may be down |
| 33 | `cfetr-power-conversion-studies.md` | ScienceDirect paywalled |
| 35 | `elio-2014-fed-poloidal-confinement.md` | ScienceDirect paywalled |
| 32 | `taranis-project-details.md` | French-language CNRS page |

### Validation (per batch)
- [ ] All files have YAML frontmatter (or are documented SKIPs)
- [ ] Companion directories present where extraction succeeded
- [ ] `.orig.md` preserved for all files
- [ ] Quality notes in report
- [ ] No broken symlinks or missing files

**What We Know After This Phase:**
All 200 source files across 36 concepts have been processed. The replacement report is complete.

---

## Phase 5: SOURCE_INDEX Reconciliation

### Goal
Ensure `knowledge/concept_research/SOURCE_INDEX.md` accurately reflects the post-replacement state, including source URLs from YAML frontmatter.

### Steps

#### 5a: Assess current index accuracy
- [ ] Run `uv run python scripts/migrate_research.py --reindex` to regenerate from disk state
- [ ] Diff the regenerated index against the current index to identify discrepancies
- [ ] Catalog what's missing: the current index shows file types (`[PDF]`, `[HTML]`, `[processed .md]`) but not source URLs, quality verdicts, or replacement status

#### 5b: Enhance index generation (if warranted)
- [ ] **Decision point with user:** Is the current format (file listing + type) sufficient, or should the index include:
  - Source URLs (from YAML frontmatter of replaced `.md` files)
  - Replacement status (replaced vs original Haiku paraphrase)
  - Quality verdict from the replacement report (YES/NO/MIXED/SKIP)
- [ ] If enhancements wanted: update `generate_source_index()` in `scripts/migrate_research.py` to:
  - Read YAML frontmatter from `.md` files and extract `source` URL
  - Distinguish replaced sources (have companion dir + frontmatter) from unreplaced (no companion dir)
  - Optionally include quality verdict (would need to parse the replacement report)
- [ ] Re-run `--reindex` with enhanced logic

#### 5c: Final validation
- [ ] Spot-check 5 concepts across the spectrum (1 early, 1 mid, 1 late, 1 with SKIPs, 1 with NO verdicts):
  - Index entry matches actual disk contents
  - Source count matches actual file count
  - URLs in index (if added) match YAML frontmatter
  - Companion dirs listed match actual dirs
- [ ] Verify concepts 20a and 20b still show "Sources: none"
- [ ] Verify no `.orig.md` files appear in the index (the current script already skips these)

#### 5d: Cross-reference with replacement report
- [ ] Compare SOURCE_INDEX source count per concept against replacement report file count
- [ ] Flag any concepts where counts don't match (indicates missed files or extra files)
- [ ] Commit final SOURCE_INDEX.md

### Validation
- [ ] `--reindex` runs without errors
- [ ] All 38 concepts listed (36 numbered + 20a + 20b)
- [ ] Source counts match reality for spot-checked concepts
- [ ] No stale entries (files listed that don't exist on disk)
- [ ] No missing entries (files on disk not listed)
- [ ] Commit

**What We Know After This Phase:**
SOURCE_INDEX.md is the authoritative, accurate index of all concept research sources. It can be trusted by the analysis pipeline and future agents.

---

## Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| arXiv HTML fix doesn't improve quality | Low | High | Phase 1 validates before bulk re-extraction. If FAIL, debug agentic-mbse first. |
| Paywalled sources in 23-36 (ScienceDirect, Wiley, T&F) | High | Low | Same pattern as 01-22: ask user for local PDF copy. |
| JS-heavy company sites produce thin output | High | Low | Expected — note NO/MIXED in report, keep original. Not a blocker. |
| `--reindex` script doesn't handle new edge cases | Low | Low | Script is simple glob-based scanner — easy to fix inline. |
| Extraction costs accumulate | Low | Medium | arXiv HTML is free (no Claude call). PDF extractions ~$1-2 each. Budget ~$50-75 for remaining 69 files. |

---

## Implementation Notes

_To be filled during execution._

### Phase 1 Completion (first run — Pandoc fix only)
**Completed:** 2026-04-03
**Verdict:** PASS — Pandoc routing produces dramatically better output. Tables (0→3), equations (bare labels→full LaTeX), scientific notation preserved. 430→591 lines (+37%). No content loss.
**Issues:** None

### Phase 1 Re-run (Pandoc fix + arXiv image downloading)
**Reason:** arXiv image downloading feature added to agentic-mbse after initial run. Re-extracting to include locally saved images.
**Completed:** 2026-04-04
**Verdict:** PASS — 21 images downloaded to `images/` subdir. All markdown refs rewritten to local `images/` paths (0 remote arXiv image refs remain). Line count unchanged at 591. Tables/equations/notation all preserved from first run.
**Issues:** None

### Phase 2 Completion (first run — no images)
**Completed:** 2026-04-03
**Files re-extracted:** All 9 (6 unique papers, 3 copies for shared papers)
- #1 (05/helios 2512.08027): 660 lines, pandoc-arxiv
- #2 (05/canis 2503.18960): 456 lines, pandoc-arxiv
- #3 (07/pulsed 2408.15206): 512 lines, pandoc-arxiv
- #4 (09/helios copy): byte-identical to #1 (180,812 bytes)
- #5 (11/confinement): done in Phase 1 (591 lines)
- #6 (12/junior 2508.17691): 274 lines, pandoc-arxiv
- #7 (12/dt-dipole 2602.20564): 934 lines, pandoc-arxiv
- #8 (12/plasma-state copy): byte-identical to #7 (268,324 bytes)
- #9 (19/dipole-reactor copy): byte-identical to #7 (268,324 bytes)
**Issues:** None — but re-running with image downloading feature

### Phase 2 Re-run (with images)
**Completed:** 2026-04-04
**Files re-extracted:** All 9 (6 unique papers, 3 copies for shared papers)
- #1 (05/helios 2512.08027): 180,588 bytes, 12 images
- #2 (05/canis 2503.18960): 88,647 chars, **0 images** (double-slash URL bug)
- #3 (07/pulsed 2408.15206): 85,304 chars, 11 images
- #4 (09/helios copy): byte-identical to #1, 12 images
- #5 (11/confinement): done in Phase 1 re-run, 21 images
- #6 (12/junior 2508.17691): 55,264 chars, 7 images
- #7 (12/dt-dipole 2602.20564): 268,048 bytes, 23 images
- #8 (12/plasma-state copy): byte-identical to #7, 23 images
- #9 (19/dipole-reactor copy): byte-identical to #7, 23 images
**Issues:** Paper #2 (2503.18960) has a double-slash in image URLs causing all 18 downloads to 404. Bug in agentic-mbse `_download_arxiv_images()` URL resolution. Text/markdown extraction unaffected.

### Phase 3 Completion
**Completed:** 2026-04-04
**Quality summary for concept 29:**
- 7 files processed: 4 YES, 1 MIXED, 2 NO (1 extraction failure, 1 JS-thin)
- #1 ball-balestri: arXiv HTML via Pandoc, 252 lines, 16 images — full paper
- #2 diii-d-collaboration: 28 lines, full page verbatim text
- #3 fusion-energy-base: JS-heavy, 14 lines — thinner than orig
- #4 greyb-interview: 89 lines, full interview with CEO quotes
- #5 venture-kick: FAILED — JS/cookie redirect, both trafilatura and WebFetch fail. Kept original.
- #6 firefly-website: 57 lines, team/advisors but lost JS-rendered About section
- #7 manta-reference-design: arXiv HTML not available (404). PDF pipeline: 3007 lines, 62 images, 162 tables, $1.96
**Issues:**
- Venture Kick (venturekick.ch) uses a cookie/JS redirect that blocks all automated extraction. The original Haiku paraphrase is the only capture of this content.
- arXiv HTML not available for all papers — 2405.20243 required PDF fallback
- Fusion Energy Base and Firefly website are JS-heavy — static extraction captures less than the original Haiku paraphrases which had access to JS-rendered content via WebFetch's headless browser

### Phase 4 Completion
**Completed:**
**Batch A:** / **Batch B:** / **Batch C:**
**Issues:**

### Phase 5 Completion
**Completed:**
**Index enhancements:**
**Issues:**
