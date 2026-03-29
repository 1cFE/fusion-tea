# Implementation Plan: Phase 1a Source Replacement

**Status:** Draft
**Created:** 2026-03-28
**Last Updated:** 2026-03-29

## Source Documents
- **Spec:** `.project/active/source-replacement/spec.md`
- **Tooling (web capture):** `~/1cfe/agentic-mbse/.project/active/web-source-capture/spec.md`
- **Tooling (provenance):** `~/1cfe/agentic-mbse/.project/active/extraction-provenance/spec.md`

## Implementation Strategy

**No design document** — this is an operational task (run extractions, review output), not a code change. The plan IS the operational document.

**Phasing Rationale:**
Setup first to verify tooling works. Then process all 166 files concept-by-concept. Each file gets: rename → extract with provenance → WebFetch comparison → quality note. Report is built incrementally as each concept completes.

**Execution Model:**
The executing agent processes one concept at a time. For each file:
1. Rename `source.md` → `source.orig.md`
2. Run `uv run agentic-mbse extract <url> --save-source --output <sources-dir>/<source-name>/`
3. Copy extraction `output.md` → `<source-name>.md` (top-level, for `find_sources()`)
4. Remove `output.md` from the companion dir (it's a duplicate of the top-level `.md`)
5. Call WebFetch on the same URL for comparison
6. Read both files, write quality comment to report
7. If extraction fails, restore from `.orig.md` and remove the companion dir

**Output Directory Layout:**
Each replaced source gets a top-level `.md` file (pipeline-compatible) plus a companion directory holding the raw source and extraction artifacts:
```
iter-01/sources/
  realta-fusion-hub-spotlight.md              ← extracted markdown (with YAML frontmatter)
  realta-fusion-hub-spotlight.orig.md         ← preserved original Haiku paraphrase
  realta-fusion-hub-spotlight/                ← companion extraction dir
    raw.html (or raw.pdf)                     ← original fetched content
    metrics.json                              ← extraction metrics
    decisions.json                            ← pipeline decisions (PDF only)
    images/                                   ← extracted figures (PDF only, if any)
```

`find_sources()` globs `sources/*.md` which matches **files** only, not directories. The companion directory is invisible to the pipeline. The `.orig.md` files DO match the glob but will be cleaned up later (per spec FR-12).

**Tooling Prerequisites (resolved 2026-03-29):**
- `agentic-mbse[web]` provides HTML extraction via trafilatura with sanitization
- Extraction provenance feature provides:
  - Universal YAML frontmatter on ALL outputs (HTML, PDF, DOCX) with `source`, `source_type`, `extracted_at`, `content_hash_sha256`, `backend`
  - `--save-source` flag to preserve raw fetched content (`raw.html` or `raw.pdf`)
  - `--no-frontmatter` opt-out (not needed here)
  - Content hash of **original source bytes** (not extracted markdown) for change detection

**Category Key:**
- `URL` — URL in file header, extract directly
- `BODY` — URL in file body (not header), extract directly
- `CITE` — Paper citation, construct URL first (arXiv/DOI)
- `SEARCH` — No URL anywhere, must web-search to find original source

---

## Phase 1: Setup & Tooling Verification

### Goal
Verify `agentic-mbse extract --save-source` works on URLs (HTML and PDF), produces universal frontmatter and preserves raw sources, create the report file, and establish the companion-directory workflow.

### Steps

- [x] Verify `agentic-mbse[web]` is installed and HTML extraction works
- [x] Verify PDF extraction works
- [x] Verify universal YAML frontmatter: HTML and PDF both produce `source`, `source_type`, `extracted_at`, `content_hash_sha256`, `backend`
- [x] Verify `--save-source` saves `raw.html` (HTML) and `raw.pdf` + `raw.html` (PDF via arXiv shortcut) in output dir
- [x] Create report file: `exploration/phase_1a/research/source_replacement_report.md` with header template
- [x] Test the full companion-directory workflow on ONE file (`11-magnetic-mirror/iter-01/sources/realta-fusion-hub-spotlight.md`):
  - Rename to `.orig.md` (already done from prior test — verify state)
  - Extract with `--save-source` into companion dir
  - Copy `output.md` to top-level `.md`, remove `output.md` from companion dir
  - WebFetch the same URL
  - Write quality comment
  - Verify `find_sources()` glob finds the `.md` file but not the companion directory
  - Verify companion dir contains `raw.html` and `metrics.json`

### Validation
- [x] Extraction produces markdown with universal frontmatter (`source`, `source_type`, `extracted_at`, `content_hash_sha256`, `backend`)
- [x] Companion directory exists with `raw.html` (or `raw.pdf`) and `metrics.json`
- [x] `find_sources()` equivalent glob (`sources/*.md`) returns the `.md` file, not the directory
- [x] Report file exists with template

---

## Phase 2: Source Replacement — Full Manifest

### Execution Instructions for Implementing Agent

**Variables used below:**
- `SOURCES_DIR` = `exploration/phase_1a/research/<concept>/iter-NN/sources`
- `NAME` = source filename without `.md` extension (e.g., `realta-fusion-hub-spotlight`)

For each file below:
1. **If category is SEARCH**: Use WebSearch to find the original URL from the file title and content. Read the `.orig.md` first for context. If URL found, proceed with extraction. If not found after reasonable search, mark as SKIP in notes.
2. **If category is CITE**: Construct the URL (arXiv ID → `https://arxiv.org/abs/{id}`, DOI → `https://doi.org/{doi}`).
3. **Rename**: `mv $SOURCES_DIR/$NAME.md $SOURCES_DIR/$NAME.orig.md`
4. **Extract**: `uv run agentic-mbse extract <url> --save-source --output $SOURCES_DIR/$NAME/`
5. **Flatten** (PDF only): If extraction created a nested subdirectory inside the companion dir, move its contents up one level and remove the empty subdir.
6. **Promote**: `cp $SOURCES_DIR/$NAME/output.md $SOURCES_DIR/$NAME.md`
7. **Deduplicate**: `rm $SOURCES_DIR/$NAME/output.md` (the top-level `.md` is the canonical copy)
8. **WebFetch**: Call WebFetch on the same URL with prompt "Extract all technical and quantitative content from this page"
9. **Compare**: Read new extraction, `.orig.md`, and WebFetch result. Write quality comment.
10. **On failure**: Restore `mv $SOURCES_DIR/$NAME.orig.md $SOURCES_DIR/$NAME.md`, remove companion dir `rm -rf $SOURCES_DIR/$NAME/`, log failure reason.

### Lessons & Instructions for Future Agents

**arXiv URLs — always use `/pdf/` or `/html/`, never `/abs/`:**
The `/abs/` page returns only the abstract (~4K chars, ~20 lines). Use `/pdf/` for full paper content via the PDF pipeline, or `/html/` if the paper has an HTML version (most post-2020 papers do). The PDF pipeline produces richer output (images, tables) but takes longer (2-12 minutes per paper). The `/html/` path is faster but produces no images.

**PDF pipeline creates nested subdirectories:**
When extracting a PDF URL, the output lands inside a nested subdirectory (named after the temp file). You MUST flatten this: `mv $NAME/tmp*/* $NAME/ && rmdir $NAME/tmp*/`. Forgetting this step breaks the companion dir layout.

**403 / paywall / access errors — ask the user:**
If extraction fails with HTTP 403, paywall, or similar access errors, DO NOT skip the file. Instead:
1. Tell the user which URL failed and why
2. Ask if they can provide a local copy of the PDF/document
3. If they provide one, extract from the local path: `uv run agentic-mbse extract /path/to/local.pdf --save-source --output $SOURCES_DIR/$NAME/`
4. Note in the report that the original URL was inaccessible and a local copy was used. The `source_type` in frontmatter will be `local_file` — this is expected.

**SEARCH files — aim for the original source, not a replacement summary:**
Many SEARCH files are multi-source compilations (the Phase 1a agent synthesized content from 3-5 URLs into one file). When replacing these:
1. Read the `.orig.md` carefully — note all distinct sources mentioned
2. Try to find the single most comprehensive original source rather than picking an arbitrary one
3. If the original was a genuine multi-source synthesis, the replacement will likely be MIXED (richer per-source content but narrower scope). Flag this in the report so the user can decide whether to add supplementary sources later via `add-source`.
4. Do NOT try to re-create the multi-source synthesis — that's the analysis pipeline's job, not ours.

**WebFetch comparison is informational, not blocking:**
WebFetch sometimes returns garbage (JS tracking code, cookie banners, empty content) instead of page content. This is expected — it uses Haiku 3.5 as intermediary. When WebFetch returns unusable output, note "WebFetch: no usable content" in the report and base your quality verdict on the `.orig.md` vs new extraction comparison only.

**Result per file:**
```
$SOURCES_DIR/
  $NAME.md              ← extracted markdown with YAML frontmatter (pipeline reads this)
  $NAME.orig.md         ← preserved original Haiku paraphrase
  $NAME/                ← companion extraction dir
    raw.html or raw.pdf ← original fetched source (traceability anchor)
    metrics.json        ← extraction quality metrics
    decisions.json      ← pipeline decisions (PDF only)
    images/             ← extracted figures (PDF only, if any)
```

---

### 01-hts-compact-tokamak (4 files)

- [x] `iter-03/sources/arc-reactor-specifications.md` → `URL` https://arxiv.org/pdf/1409.3540
  - Notes: Used /pdf/ URL (not /abs/) to get full paper. PDF pipeline, 2219 lines, 94 images. YES.
- [x] `iter-03/sources/sparc-icrf-heating-paper.md` → `URL` https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/physics-basis-for-the-icrf-system-of-the-sparc-tokamak/22016DD64F3C5CAD47563A1E4AE59934
  - Notes: Open-access paper, full content via trafilatura. 428 lines. YES.
- [x] `iter-04/sources/arc-power-conversion-studies.md` → `URL` https://www.mdpi.com/2071-1050/16/17/7480
  - Notes: MDPI returned 403. Used local PDF (~/1cfe/ssrn-4482183.pdf) of SSRN preprint. 579 lines, 20 images. YES.
- [x] `iter-04/sources/cfs-2025-2026-updates.md` → `SEARCH` CFS/SPARC 2025-2026 milestones, CES 2026 magnet announcement
  - Notes: Found Fortune CES 2026 article. 52 lines vs 34 orig. Single-source vs multi-source synthesis. MIXED.

---

### 02-acoustic-icf-sonofusion (3 files)

- [x] `iter-01/sources/bubble-fusion-scientific-history.md` → `SEARCH` Bubble fusion / sonofusion scientific history, Taleyarkhan 2002
  - Notes: Source cited "Wikipedia (Bubble fusion)" → https://en.wikipedia.org/wiki/Bubble_fusion. 177 lines vs 42 orig. Full article with citations. YES.
- [x] `iter-01/sources/sonofusion-energy-website.md` → `URL` https://www.sonofusion.energy/
  - Notes: Page is genuinely thin (698 chars, 2 marketing paragraphs). 11 lines vs 21 orig. WebFetch got additional JS-rendered content (climate stats, scalability claims). MIXED.
- [x] `iter-01/sources/ucla-putterman-group-sonoluminescence.md` → `URL` http://acoustics-research.physics.ucla.edu/sonoluminescence/
  - Notes: Full page with experiment descriptions, dense microplasma physics, publication links. 70 lines vs 29 orig. YES.

---

### 03-laser-icf-liquid-jet-target (4 files)

- [x] `iter-01/sources/arxiv-2308-levitt-quantum-control.md` → `URL` https://arxiv.org/pdf/2308.07417
  - Notes: Used /pdf/ URL. 478 lines vs 18 orig. Full paper via PDF pipeline, 7 images. YES.
- [x] `iter-01/sources/arxiv-2503-nanoshell-paper.md` → `URL` https://arxiv.org/pdf/2503.15531
  - Notes: Used /pdf/ URL. 220 lines vs 54 orig. Full nanoshell paper. YES.
- [x] `iter-01/sources/cortex-fusion-website.md` → `URL` https://www.cortexfusion.systems/
  - Notes: JS-heavy SPA. Extraction got Patents/Publications (11 US patent numbers), missed tech description (isochoric heating, >1000T). 83 vs 33. MIXED.
- [x] `iter-01/sources/kHz-liquid-sheet-fusion-paper.md` → `URL` Cambridge Core (full slug URL needed)
  - Notes: Short URL 404'd; full slug URL worked. 562 vs 21. Full Knight et al. paper. YES.

---

### 04-laser-icf (7 files)

- [x] `iter-01/sources/hb11-company-overview.md` → `URL` https://hb11.energy/our-story/
  - Notes: JS-rendered page. 13 vs 36. Thin marketing text; orig had team, partnerships, funding. NO.
- [x] `iter-01/sources/hb11-osaka-experiment-2022.md` → `URL` https://www.mdpi.com/2076-3417/12/3/1444
  - Notes: MDPI 403. Used local PDF (~/1cfe/applsci-12-01444-v2.pdf). 320 vs 24. Full Margarone/Batani paper. YES.
- [x] `iter-01/sources/hb11-patent-reactor-design.md` → `URL` https://patents.google.com/patent/US20170125129A1/en
  - Notes: Full patent text + Google Patents metadata. 671 vs 42. YES.
- [x] `iter-01/sources/hb11-technology-page.md` → `URL` https://hb11.energy/our-technology/
  - Notes: JS-rendered page. 15 vs 19. Thin; missed ICF specs, 8.7 MeV, steam cycle details. NO.
- [x] `iter-02/sources/hb11-newatlas-article.md` → `URL` https://newatlas.com/energy/hb11-hydrogen-boron-fusion-clean-energy/
  - Notes: Required sanitizer bugfix (html_sanitize.py:69). 38 vs 27. Full article with direct quotes. YES.
- [x] `iter-02/sources/hb11-recent-developments-2024-2025.md` → `URL` https://h2-tech.com/news/2023/08-2023/hb11-energy-receives-grant-from-u-s-department-of-energy/
  - Notes: Single DOE INFUSE article; orig compiled 6+ sources. 23 vs 65. MIXED.
- [x] `iter-02/sources/hb11-technology-page-2025.md` → `URL` https://hb11.energy/our-technology/
  - Notes: Same URL as hb11-technology-page. Copied extraction. 15 vs 29. NO.

---

### 05-planar-coil-stellarator (4 files)

- [ ] `iter-01/sources/thea-energy-helios-arxiv-2512-08027.md` → `URL` https://arxiv.org/html/2512.08027v1
  - Notes:
- [ ] `iter-01/sources/thea-energy-website-and-press.md` → `URL` https://thea.energy/
  - Notes:
- [ ] `iter-02/sources/thea-energy-canis-prototype-arxiv-2503-18960.md` → `URL` https://arxiv.org/html/2503.18960v1
  - Notes:
- [ ] `iter-02/sources/thea-energy-doe-certification-jan2026.md` → `URL` https://thea.energy/press-release/u-s-department-of-energy-certifies-thea-energys-fusion-pilot-plant-preconceptual-design/
  - Notes:

---

### 06-magnetic-mirror (4 files)

- [ ] `iter-01/sources/arpa-e-fisch-2025-presentation.md` → `URL` https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_08_Fisch.pdf
  - Notes: PDF — routes through PDF pipeline
- [ ] `iter-01/sources/princeton-arpa-e-funding-2022.md` → `URL` https://www.princeton.edu/news/2022/03/10/fisch-receives-funding-unlikely-fantastic-clean-energy-technology
  - Notes:
- [ ] `iter-01/sources/technical-papers-summary.md` → `SEARCH` Fisch group papers: alpha channeling mirrors PRL 2006, wave-supported hybrid pB11 PoP 2022
  - Notes:
- [ ] `iter-02/sources/arpa-e-2025-fisch-presentation-notes.md` → `URL` https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_08_Fisch.pdf
  - Notes: Same PDF as 06-01 above — may produce identical extraction

---

### 07-maglif (7 files)

- [ ] `iter-01/sources/arxiv-2408-15206-pulsed-magnetic-fusion.md` → `URL` https://arxiv.org/html/2408.15206v1
  - Notes:
- [ ] `iter-01/sources/fuse-energy-technology.md` → `URL` https://www.f.energy/
  - Notes:
- [ ] `iter-01/sources/pacific-fusion-website-technology.md` → `URL` https://www.pacificfusion.com/
  - Notes:
- [ ] `iter-01/sources/z-ife-power-plant-concept.md` → `URL` https://www.osti.gov/biblio/771517
  - Notes:
- [ ] `iter-02/sources/fuse-energy-not-boring-details.md` → `URL` https://www.notboring.co/p/fuse-energy
  - Notes:
- [ ] `iter-02/sources/pacific-fusion-interview-fusion-report.md` → `URL` https://thefusionreport.substack.com/p/interview-with-pacific-fusion-on
  - Notes:
- [ ] `iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md` → `URL` https://www.osti.gov/servlets/purl/901970/
  - Notes: PDF — routes through PDF pipeline

---

### 08-frc-w-direct-conversion (5 files)

- [ ] `iter-01/sources/contrary-research-helion.md` → `URL` https://research.contrary.com/company/helion
  - Notes:
- [ ] `iter-01/sources/docslib-helion-arpa-e-presentation.md` → `URL` https://docslib.org/doc/9103852/helion-energy-david-kirtley-ceo-project-lead-20-tesla-arpa-e-experiment-40-tesla-reactor
  - Notes:
- [ ] `iter-01/sources/helion-website-technology.md` → `URL` https://www.helionenergy.com/technology/
  - Notes: JS-heavy site — may get thin extraction
- [ ] `iter-02/sources/helion-milestones-feb2026.md` → `URL` https://www.helionenergy.com/articles/helion-achieves-new-fusion-energy-milestones/
  - Notes:
- [ ] `iter-02/sources/helion-prototype-generations.md` → `SEARCH` Helion Energy prototype generations timeline (Grande, Venti, Trenta, Polaris, Orion)
  - Notes:

---

### 09-qi-stellarator-hts (5 files)

- [ ] `iter-01/sources/proxima-fusion-technology-page.md` → `URL` https://www.proximafusion.com/technology
  - Notes:
- [ ] `iter-01/sources/stellaris-design-details.md` → `URL` https://www.sciencedirect.com/science/article/pii/S0920379625300705
  - Notes: May be paywalled — extraction may be abstract-only
- [ ] `iter-02/sources/helios-stellarator-comparison.md` → `URL` https://arxiv.org/html/2512.08027v1
  - Notes:
- [ ] `iter-02/sources/proxima-fusion-2026-updates.md` → `BODY` https://www.proximafusion.com/press-news/ (URL in body text)
  - Notes:
- [ ] `iter-02/sources/stellaris-paper-details.md` → `CITE` DOI: 10.1016/j.fusengdes.2025.114868 → https://doi.org/10.1016/j.fusengdes.2025.114868
  - Notes: May be paywalled

---

### 10-large-scale-stellarator (5 files)

- [ ] `iter-01/sources/gauss-fusion-technical-summary.md` → `SEARCH` Gauss Fusion GIGA stellarator power plant, MT29 CERN abstract, FusionXInvest profile
  - Notes:
- [ ] `iter-01/sources/helias-reactor-context.md` → `SEARCH` HELIAS reactor HSR4/18 stellarator design studies
  - Notes:
- [ ] `iter-02/sources/gauss-fusion-cdr-review-2026.md` → `URL` https://www.startbase.com/news/expertengremium-bestaetigt-designkonzept-fuer-fusionskraftwerk-von-gauss-fusion/
  - Notes: German-language page
- [ ] `iter-02/sources/gauss-fusion-partnerships-2025.md` → `URL` https://www.modernpowersystems.com/news/gauss-fusion-broadens-european-partnerships/
  - Notes:
- [ ] `iter-02/sources/helias-blanket-studies.md` → `URL` https://onlinelibrary.wiley.com/doi/full/10.1002/er.7343
  - Notes:

---

### 11-magnetic-mirror (6 files)

- [ ] `iter-01/sources/aps-dpp-2025-sutherland.md` → `URL` https://meetings-archive.aps.org/dpp/2025/gm12/2/
  - Notes:
- [ ] `iter-01/sources/arxiv-2411-06644-confinement-predictions.md` → `URL` https://arxiv.org/abs/2411.06644
  - Notes:
- [ ] `iter-01/sources/realta-fusion-hub-spotlight.md` → `URL` https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion
  - Notes:
- [ ] `iter-01/sources/wham-experiment-details.md` → `URL` https://wham.physics.wisc.edu/
  - Notes:
- [ ] `iter-02/sources/fusion-report-interview-realta.md` → `URL` https://thefusionreport.substack.com/p/interview-with-realta-fusion
  - Notes:
- [ ] `iter-02/sources/realta-svb-funding-feb2026.md` → `URL` https://www.prnewswire.com/news-releases/realta-fusion-secures-9-5-million-growth-capital-facility-from-silicon-valley-bank-a-division-of-first-citizens-bank-302689285.html
  - Notes:

---

### 12-levitated-dipole (5 files)

- [ ] `iter-01/sources/arxiv-2508-17691-junior-design-results.md` → `URL` https://arxiv.org/html/2508.17691v1
  - Notes:
- [ ] `iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants.md` → `URL` https://arxiv.org/html/2602.20564v1
  - Notes:
- [ ] `iter-01/sources/openstar-prototype-roadmap.md` → `SEARCH` OpenStar Technologies prototype roadmap (Junior, Tahi, Maui, Tama Nui)
  - Notes:
- [ ] `iter-02/sources/arxiv-2602-20564-plasma-state-clarification.md` → `URL` https://arxiv.org/html/2602.20564
  - Notes: Same paper as 12-02 — may produce identical extraction
- [ ] `iter-02/sources/openstar-2026-funding-tahi-timeline.md` → `BODY` https://www.bloomberg.com/news/articles/2026-02-17/ (URL in body)
  - Notes: Bloomberg may be paywalled

---

### 13-electrostatic-hybrid (6 files)

- [ ] `iter-01/sources/avalanche-29m-raise-2026.md` → `URL` https://www.avalanchefusion.com/news-release/avalanche-energy-raises-29-million-following-plasma-physics-breakthroughs
  - Notes:
- [ ] `iter-01/sources/avalanche-300kv-press-release.md` → `URL` https://www.avalanchefusion.com/news-release/avalanche-energy-completes-final-series-a-voltage-milestone-300-000-volts-in-compact-high-efficiency-prototype-fusion-machine
  - Notes:
- [ ] `iter-01/sources/avalanche-cwfest2023-blog.md` → `URL` https://www.avalanchefusion.com/blog/cwfest2023
  - Notes:
- [ ] `iter-01/sources/avalanche-fusionwerx-grant.md` → `URL` https://www.avalanchefusion.com/news-release/avalanche-energy-awarded-10-million-grant-from-washington-state-to-develop-fusionwerx-neutron-factory
  - Notes:
- [ ] `iter-01/sources/avalanche-orbitron-page.md` → `URL` https://www.avalanchefusion.com/orbitron
  - Notes:
- [ ] `iter-01/sources/talk-polywell-orbitron-paper-discussion.md` → `URL` https://talk-polywell.org/bb/viewtopic.php?t=6587
  - Notes: Forum page — may extract poorly

---

### 14-magnetized-target-fusion-pneumatic-compression (5 files)

- [ ] `iter-01/sources/general-fusion-technical-details.md` → `SEARCH` General Fusion technical details, COMSOL story, compression system specs
  - Notes:
- [ ] `iter-01/sources/general-fusion-technology-overview.md` → `URL` https://generalfusion.com/fusion-technology/
  - Notes:
- [ ] `iter-02/sources/general-fusion-fst-2025-fuel-cycles.md` → `URL` https://www.tandfonline.com/doi/full/10.1080/15361055.2025.2526266
  - Notes: May be paywalled
- [ ] `iter-02/sources/general-fusion-iaea-fec-2025-abstract.md` → `URL` https://conferences.iaea.org/event/392/contributions/35891/attachments/19864/33918/IAEA%20FEC%202025%20LM26%20Abstract%20-%20Hildebrand.pdf
  - Notes: PDF
- [ ] `iter-02/sources/general-fusion-lm26-milestones-2025.md` → `BODY` https://generalfusion.com/post/watch-general-fusions-lm26-... (URL in body)
  - Notes:

---

### 15-sheared-flow-stabilized-z-pinch (6 files)

- [ ] `iter-01/sources/century-demo-system.md` → `URL` https://www.zapenergy.com/news/zap-attracts-130m-as-demo-system-begins-operations
  - Notes:
- [ ] `iter-01/sources/engineering-paradigms-paper-summary.md` → `URL` https://www.tandfonline.com/doi/full/10.1080/15361055.2023.2209131
  - Notes:
- [ ] `iter-01/sources/fuze-q-and-fuze-3.md` → `URL` https://www.zapenergy.com/news/zap-energy-exceeds-gigapascal-fusion-plasma-pressures-on-new-fusion-device-fuze-3
  - Notes:
- [ ] `iter-01/sources/zap-energy-website-how-it-works.md` → `URL` https://www.zapenergy.com/how-it-works
  - Notes:
- [ ] `iter-02/sources/century-and-fuze-a-updates-2025.md` → `URL` https://meetings-archive.aps.org/dpp/2025/jm12/6/
  - Notes:
- [ ] `iter-02/sources/fuze-3-gigapascal-results-2025.md` → `URL` https://www.sciencedaily.com/releases/2025/11/251120002836.htm
  - Notes:

---

### 16-muon-catalyzed-fusion (3 files)

- [ ] `iter-01/sources/acceleron-arpa-e-presentation-2025.md` → `URL` https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_09_Newburg.pdf
  - Notes: PDF
- [ ] `iter-01/sources/acceleron-company-overview.md` → `URL` https://www.acceleron.energy/
  - Notes:
- [ ] `iter-01/sources/muon-catalyzed-fusion-physics.md` → `URL` https://en.wikipedia.org/wiki/Muon-catalyzed_fusion
  - Notes:

---

### 17-laser-icf-direct-drive (5 files)

- [ ] `iter-01/sources/focused-energy-technology.md` → `BODY` https://focused-energy.co/technology (URL in sources line)
  - Notes:
- [ ] `iter-01/sources/xcimer-energy-approach.md` → `BODY` https://xcimer.energy/approach/ (URL in title)
  - Notes:
- [ ] `iter-02/sources/focused-energy-callahan-interview.md` → `URL` https://physicsworld.com/a/focusing-on-fusion-debbie-callahan-talks-commercial-laser-fusion/
  - Notes:
- [ ] `iter-02/sources/hylife-energy-conversion-notes.md` → `SEARCH` HYLIFE-II IFE energy conversion, helium Brayton cycle for laser fusion
  - Notes: Research notes — may not have a single original URL
- [ ] `iter-02/sources/xcimer-science-page.md` → `URL` https://xcimer.energy/science/
  - Notes:

---

### 18-p-b11-frc (6 files)

- [ ] `iter-01/sources/grokipedia-tae-technologies.md` → `URL` https://grokipedia.com/page/TAE_Technologies
  - Notes:
- [ ] `iter-01/sources/tae-energy-conversion-notes.md` → `SEARCH` TAE Technologies energy conversion: FAQ page, ICC patent US7459654
  - Notes: Compiled from 3 sources with conflicting info
- [ ] `iter-01/sources/tae-nbi-breakthrough-2025.md` → `URL` https://tae.com/tae-technologies-delivers-fusion-breakthrough-that-dramatically-reduces-cost-of-a-future-power-plant/
  - Notes:
- [ ] `iter-02/sources/tae-c2w-machine-details.md` → `SEARCH` TAE Technologies C-2W Norman machine dimensions and specifications
  - Notes:
- [ ] `iter-02/sources/tae-djt-merger-davinci-specs.md` → `SEARCH` TAE Technologies DJT/Trump Media merger, Da Vinci power plant specs
  - Notes:
- [ ] `iter-02/sources/tae-energy-conversion-clarification.md` → `SEARCH` TAE Technologies FAQ fusion energy conversion (tae.com/faq-fusion/)
  - Notes: Resolves 3-narrative tension; try tae.com/faq-fusion/ directly

---

### 19-orbital-levitated-dipole (5 files)

- [ ] `iter-01/sources/levitated-dipole-technical-background.md` → `URL` https://en.wikipedia.org/wiki/Levitated_dipole
  - Notes:
- [ ] `iter-01/sources/nasaspaceflight-forum-discussion.md` → `URL` https://forum.nasaspaceflight.com/index.php?topic=63860.0
  - Notes: Forum page
- [ ] `iter-01/sources/yc-launch-page.md` → `URL` https://www.ycombinator.com/launches/Oox-zephyr-fusion-in-orbit-fusion-power
  - Notes:
- [ ] `iter-02/sources/dipole-reactor-heating-energy-conversion.md` → `URL` https://arxiv.org/html/2602.20564
  - Notes:
- [ ] `iter-02/sources/zephyr-fusion-web-sources-2026.md` → `SEARCH` Zephyr Fusion company updates 2026, DCD news, Fondo blog, LinkedIn
  - Notes: Compiled from many sources — pick primary

---

### 20-modular-hts-stellarator (4 files)

- [ ] `iter-01/sources/renaissance-fusion-technology.md` → `URL` https://renfusion.eu/technology
  - Notes:
- [ ] `iter-01/sources/type-one-energy-infinity-two-design.md` → `URL` https://typeoneenergy.com/our-technology/
  - Notes:
- [ ] `iter-02/sources/renaissance-fusion-specs.md` → `CITE` Nuclear Fusion 64 (2024) 026007 → https://doi.org/10.1088/1741-4326/ad0dde
  - Notes: May be paywalled
- [ ] `iter-02/sources/type-one-infinity-two-specs.md` → `CITE` Journal of Plasma Physics (2025) → https://www.cambridge.org/core/journals/journal-of-plasma-physics/collections/physics-basis-of-the-infinity-two-fusion-power-plant
  - Notes: Collection page with multiple papers

---

### 21-spherical-tokamak-hts (11 files)

- [ ] `iter-01/sources/pulsed-spherical-tokamak-paper.md` → `URL` https://www.mdpi.com/2571-6182/5/2/19
  - Notes:
- [ ] `iter-01/sources/st40-heating-systems.md` → `URL` https://tokamakenergy.com/2025/01/21/high-power-gyrotron-heating-to-boost-performance-on-road-to-clean-and-limitless-fusion-energy/
  - Notes:
- [ ] `iter-01/sources/ste1-pilot-plant-specs.md` → `URL` https://archive.aps.org/dpp/2025/gm12/8/
  - Notes:
- [ ] `iter-01/sources/tokamak-energy-overview.md` → `URL` https://tokamakenergy.com/
  - Notes:
- [ ] `iter-02/sources/spherical-tokamak-center-stack-shielding.md` → `URL` https://pmc.ncbi.nlm.nih.gov/articles/PMC6365859/
  - Notes:
- [ ] `iter-02/sources/tokamak-energy-heating-systems.md` → `BODY` https://interestingengineering.com/energy/tokamak-energy-gets-1mw-gyrotron (URL in body)
  - Notes:
- [ ] `iter-02/sources/tokamak-energy-roadmap.md` → `BODY` https://www.ans.org/news/article-4447/tokamak-energy-bets-its-spherical-design-will-deliver-fusion-energy-in-the-early-2030s/ (URL in body)
  - Notes:
- [ ] `iter-02/sources/tokamak-energy-st-e1-design-evolution.md` → `SEARCH` Tokamak Energy ST-E1 design evolution DPP 2024/2025, World Nuclear News, NEI Magazine
  - Notes:
- [ ] `iter-03/sources/tokamak-energy-demo4-magnets.md` → `URL` https://tokamakenergy.com/2025/11/19/tokamak-energy-announces-fusion-power-plant-magnet-technology-breakthrough/
  - Notes:
- [ ] `iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md` → `URL` https://epjwoc.epj.org/articles/epjconf/abs/2026/02/epjconf_rfppc2026_02014/epjconf_rfppc2026_02014.html
  - Notes:
- [ ] `iter-03/sources/tokamak-energy-st-e1-dpp2025-abstract.md` → `URL` https://meetings-archive.aps.org/dpp/2025/gm12/8/
  - Notes:

---

### 22-projectile-icf (4 files)

- [ ] `iter-01/sources/first-light-fusion-technology.md` → `SEARCH` First Light Fusion technology overview, FLARE pivot, firstlightfusion.com
  - Notes:
- [ ] `iter-01/sources/nearstar-fusion-technology.md` → `SEARCH` NearStar Fusion MTIF technology, nearstarfusion.com/learn-more
  - Notes:
- [ ] `iter-02/sources/first-light-flare-pivot-update.md` → `SEARCH` First Light Fusion FLARE white paper September 2025
  - Notes:
- [ ] `iter-02/sources/nearstar-fusion-2025-update.md` → `SEARCH` NearStar Fusion 2025 updates, Virginia Venture Partners investment
  - Notes:

---

### 23-laser-icf-nanostructured-target (4 files)

- [ ] `iter-01/sources/hb11-energy-technology.md` → `URL` https://hb11.energy/
  - Notes:
- [ ] `iter-01/sources/marvel-fusion-technology.md` → `URL` https://www.marvelfusion.com/
  - Notes:
- [ ] `iter-02/sources/hb11-energy-2025-updates.md` → `URL` https://hb11.energy/our-technology/
  - Notes:
- [ ] `iter-02/sources/marvel-fusion-2025-updates.md` → `URL` https://cordis.europa.eu/project/id/101189082
  - Notes:

---

### 24-dense-plasma-focus (3 files)

- [ ] `iter-01/sources/lerner-2023-jfe-paper.md` → `URL` https://link.springer.com/article/10.1007/s10894-023-00345-z
  - Notes:
- [ ] `iter-01/sources/lerner-2024-frontiers-pB11-prep.md` → `URL` https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2024.1438880/full
  - Notes:
- [ ] `iter-01/sources/lppfusion-website-technology.md` → `URL` https://www.lppfusion.com/technology/focus-fusion-energy/
  - Notes:

---

### 25-heavy-ion-beam-icf (3 files)

- [ ] `iter-01/sources/hif-technology-overview.md` → `CITE` arXiv:2005.07520 → https://arxiv.org/abs/2005.07520
  - Notes: Also references HIBALL study KfK-3202 and LBNL HIF tutorial
- [ ] `iter-01/sources/intensity-energy-search-results.md` → `SEARCH` "Intensity Energy" fusion company (NOTE: original search found nothing — company likely doesn't exist)
  - Notes: This file documents a failed search. May not be replaceable.
- [ ] `iter-02/sources/hif-recent-research-compilation.md` → `SEARCH` Heavy ion beam fusion recent research 2020s, LBNL, GSI
  - Notes: Compiled from multiple sources

---

### 26-laser-icf-indirect-drive (7 files)

- [ ] `iter-01/sources/inertia-enterprises-website-and-faq.md` → `URL` https://inertia.com/
  - Notes:
- [ ] `iter-01/sources/nif-ignition-achievements.md` → `SEARCH` NIF ignition achievements 2022-2024, LLNL fusion milestones
  - Notes:
- [ ] `iter-01/sources/xcimer-energy-website-and-science.md` → `URL` https://xcimer.energy/
  - Notes:
- [ ] `iter-02/sources/inertia-enterprises-2026-update.md` → `URL` https://www.globenewswire.com/news-release/2026/02/11/3236274/0/en/
  - Notes:
- [ ] `iter-02/sources/nif-ignition-updates-2025.md` → `URL` https://lasers.llnl.gov/science/achieving-fusion-ignition
  - Notes:
- [ ] `iter-02/sources/xcimer-hybrid-direct-drive-evolution.md` → `URL` https://pubs.aip.org/aip/pop/article/31/11/112708/3322685/Hybrid-direct-drive-with-a-two-sided-ultraviolet
  - Notes:
- [ ] `iter-02/sources/xcimer-laser-milestones-2025.md` → `URL` https://xcimer.energy/xcimer-energy-completes-first-private-sector-electron-beam-excimer-laser/
  - Notes:

---

### 27-polywell (4 files)

- [ ] `iter-01/sources/emc2-website-summary.md` → `URL` https://www.emc2fusion.com/
  - Notes: Original fetch returned 403 — may still be blocked
- [ ] `iter-01/sources/polywell-technical-details.md` → `SEARCH` Polywell fusion technical details, Bussard polyhedral cusp, WB-6/WB-7/WB-8 experiments
  - Notes:
- [ ] `iter-02/sources/emc2-fpns-talk-polywell-2023.md` → `URL` https://talk-polywell.org/bb/viewtopic.php?t=6553
  - Notes: Forum page
- [ ] `iter-02/sources/polywell-revisited-2025-park.md` → `CITE` arXiv:2508.06761 → https://arxiv.org/abs/2508.06761
  - Notes:

---

### 28-hts-tokamak-full-hts (2 files)

- [ ] `iter-01/sources/energy-singularity-overview.md` → `BODY` https://www.energysingularity.cn/en/ (URL in body)
  - Notes: Chinese company site — may have limited English extraction
- [ ] `iter-02/sources/energy-singularity-technical-summary.md` → `URL` https://english.news.cn/20260206/31e447b7e3504b0d802ef705556f66ef/c.html
  - Notes:

---

### 29-negative-triangularity-tokamak (7 files)

- [ ] `iter-01/sources/ball-balestri-ohmic-nt-paper.md` → `URL` https://arxiv.org/html/2407.06439v2
  - Notes:
- [ ] `iter-01/sources/firefly-fusion-diii-d-collaboration.md` → `URL` https://d3dfusion.org/fireflyfusion/
  - Notes:
- [ ] `iter-01/sources/fusion-energy-base-profile.md` → `URL` https://www.fusionenergybase.com/organizations/firefly-fusion
  - Notes:
- [ ] `iter-01/sources/greyb-firefly-interview.md` → `URL` https://greyb.com/blog/firefly-fusion-scouted-interview
  - Notes:
- [ ] `iter-01/sources/venture-kick-profile.md` → `URL` https://www.venturekick.ch/firefly-fusion
  - Notes:
- [ ] `iter-02/sources/firefly-website-2026.md` → `URL` https://fireflyfusion.energy/
  - Notes:
- [ ] `iter-02/sources/manta-reference-design.md` → `CITE` arXiv:2405.20243 → https://arxiv.org/abs/2405.20243
  - Notes:

---

### 30-laser-icf-nif-commercialization (3 files)

- [ ] `iter-01/sources/enr-mike-dunne-interview.md` → `URL` https://www.enr.com/articles/62560-ten-minutes-with-mike-dunne-co-founder-and-cto-of-fusion-power-startup-inertia-enterprises
  - Notes:
- [ ] `iter-01/sources/globenewswire-series-a-press-release.md` → `URL` https://www.globenewswire.com/news-release/2026/02/11/3236274/0/en/Inertia-raises-450-million-to-commercialize-the-only-proven-fusion-science.html
  - Notes:
- [ ] `iter-01/sources/inertia-website-technical.md` → `URL` https://inertia.com/
  - Notes:

---

### 31-laser-icf-oec-architecture (2 files)

- [ ] `iter-01/sources/blf-website-and-news.md` → `SEARCH` Blue Laser Fusion website bluelaserfusion.com, OEC technology, pulse stacking
  - Notes:
- [ ] `iter-01/sources/optics-express-2025-paper.md` → `URL` https://bluelaserfusion.com/wp-content/uploads/2025/10/Laser-based-inertial-fusion-energy-system-enabled-by-optical-enhancement-cavities-and-a-direct-drive-configuration-reactor.pdf
  - Notes: PDF

---

### 32-laser-icf-french-national (5 files)

- [ ] `iter-01/sources/aip-advances-ribeyre-2025.md` → `URL` https://pubs.aip.org/aip/adv/article/15/9/095013/3361996/Perspectives-in-laser-driven-inertial-fusion
  - Notes:
- [ ] `iter-01/sources/genf-icf-article.md` → `URL` https://genf-systems.com/inertial-confinement-fusion/
  - Notes:
- [ ] `iter-01/sources/genf-news-timeline.md` → `URL` https://genf-systems.com/our-news/
  - Notes:
- [ ] `iter-01/sources/genf-website-technology.md` → `URL` https://genf-systems.com/technology/
  - Notes:
- [ ] `iter-01/sources/taranis-project-details.md` → `URL` https://www.cnrs.fr/fr/actualite/projet-taranis-vers-une-production-denergie-grace-la-fusion-nucleaire
  - Notes: French-language page

---

### 33-state-backed-tokamak-best (3 files)

- [ ] `iter-01/sources/best-research-plan-v1.1-summary.md` → `URL` https://euro-fusion.org/wp-content/uploads/2025/11/BEST-Research-Plan-v1.1.pdf
  - Notes: PDF — large document, may produce very long extraction
- [ ] `iter-01/sources/neo-fusion-company-profile.md` → `URL` http://jbxnah.com
  - Notes: Chinese company site — may extract poorly or be down
- [ ] `iter-02/sources/cfetr-power-conversion-studies.md` → `URL` https://www.sciencedirect.com/science/article/abs/pii/S0360544220326025
  - Notes: Paywalled — abstract only likely

---

### 34-compact-spherical-tokamak-india (2 files)

- [ ] `iter-01/sources/pranos-fusion-overview.md` → `BODY` https://theprint.in/ground-reports/... (URL in body)
  - Notes:
- [ ] `iter-02/sources/iaea-fuse-pranos-profile.md` → `URL` https://nucleus.iaea.org/sites/connect/FUSEpublic/SitePages/PRANOS.aspx
  - Notes:

---

### 35-polomac-magnetic-confinement (3 files)

- [ ] `iter-01/sources/deutelio-company-profile.md` → `URL` https://www.deutelio.com/
  - Notes:
- [ ] `iter-01/sources/elio-2014-fed-poloidal-confinement.md` → `URL` https://www.sciencedirect.com/science/article/pii/S0920379614003834
  - Notes: Paywalled
- [ ] `iter-01/sources/jtsp-2024-polomac-technical-report.md` → `URL` https://www.jtsp.eu/jtsp/article/view/32
  - Notes:

---

### 36-helical-coil-stellarator (4 files)

- [ ] `iter-01/sources/aip-2023-paper-abstract.md` → `URL` https://pubs.aip.org/aip/pop/article/30/5/050601/2891604/Development-of-steady-state-fusion-reactor-by
  - Notes:
- [ ] `iter-01/sources/helical-fusion-technology-overview.md` → `SEARCH` Helical Fusion company technology, HESTIA reactor, NIFS LHD heritage
  - Notes:
- [ ] `iter-02/sources/helical-fusion-2025-2026-updates.md` → `SEARCH` Helical Fusion HTS coil milestone Oct 2025, ANS Nuclear Newswire
  - Notes:
- [ ] `iter-02/sources/nifs-ffhr-blanket-heritage.md` → `SEARCH` NIFS FFHR blanket studies, Sagara FLiBe molten salt, LiPb twin-loop Oroshhi-2
  - Notes:

---

## Phase 2 Summary Statistics

| Category | Count | Description |
|----------|-------|-------------|
| `URL` | 110 | Direct URL in header — extract immediately |
| `BODY` | 10 | URL in body text — extract after locating URL |
| `CITE` | 8 | Paper citation — construct URL, then extract |
| `SEARCH` | 38 | No URL — web search needed first |
| **Total** | **166** | |

---

## Phase 3: Report Finalization

### Goal
Review the completed report, generate summary statistics, verify the companion directory structure, and flag any concepts that need follow-up.

### Steps

- [ ] Count replacements by outcome: successful / partial (paywall) / failed (dead URL) / skipped (no URL found)
- [ ] Identify concepts where >50% of sources got MIXED or NO quality verdicts — these may need new sources entirely
- [ ] Write summary section at top of report with aggregate stats
- [ ] Verify all `.orig.md` files are still intact
- [ ] Spot-check 5 random concepts:
  - Run `find_sources()` equivalent glob to confirm new `.md` files are discoverable
  - Verify companion directories exist with `raw.html`/`raw.pdf` and `metrics.json`
  - Verify top-level `.md` files have YAML frontmatter with `source`, `content_hash_sha256`, `backend`
  - Verify companion dirs do NOT contain `output.md` (it should only exist at top level)

### Validation

- [ ] Report has an entry for every one of the 166 files
- [ ] Every entry has a quality verdict (YES/NO/MIXED/SKIP)
- [ ] No `.md` source files were lost (count of `.md` files ≥ count of `.orig.md` files)
- [ ] Each successfully replaced file has a companion directory with raw source
- [ ] YAML frontmatter `content_hash_sha256` hashes original source bytes (not extracted markdown)
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` runs without errors

---

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-03-28 (initial), 2026-03-29 (revised with provenance features)
**Actual Changes:**
- Installed `agentic-mbse[web]` extra (trafilatura + deps)
- Verified HTML extraction: universal frontmatter (`source`, `source_type`, `extracted_at`, `content_hash_sha256`, `backend`)
- Verified PDF extraction: universal frontmatter now present (provenance feature shipped 2026-03-28)
- Verified `--save-source`: produces `raw.html` and/or `raw.pdf` in output dir
- Created report file: `exploration/phase_1a/research/source_replacement_report.md`
- Initial test file done with old workflow (no companion dir) — needs redo with revised workflow
**Issues resolved by agentic-mbse provenance feature:**
- PDF frontmatter gap: FIXED — all outputs now have universal YAML frontmatter
- Raw source preservation: FIXED — `--save-source` saves original HTML/PDF bytes
- Content hash semantics: FIXED — hashes original source bytes for change detection
**Phase 1 test (companion-dir workflow) completed 2026-03-29:**
- Extracted `realta-fusion-hub-spotlight.md` with `--save-source` into companion dir
- Top-level `.md`: 259 lines, universal frontmatter (`source`, `source_type: url`, `extracted_at`, `content_hash_sha256`, `backend: trafilatura`, `title`, `author`)
- Companion dir: `raw.html` (392KB original page), `metrics.json`
- `find_sources()` glob returns 5 files (4 original + 1 .orig.md), 0 directories — companion dir invisible
- WebFetch comparison: ~25-line bullet summary vs 259-line full article — verdict YES
- All Phase 1 validation items pass

### Phase 2 Progress
**Started:**
**Concepts Completed:** 1/36
**Files Replaced:** 4/166
**Last Concept:**
**Issues:**

### Phase 3 Completion
**Completed:**
**Final Stats:**
**Issues:**

---

**Status**: Draft → In Progress → Complete
