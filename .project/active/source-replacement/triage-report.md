# Phase 6 Triage Report: NO and MIXED Verdict Decisions

**Created:** 2026-04-04
**Status:** Draft — awaiting user approval before applying changes

## Overview

After completing source replacement across all 36 concepts (171 files), this report compiles all NO and MIXED verdicts and recommends a disposition for each.

**Verdict totals from replacement report:**
- YES: ~102 → action: delete `.orig.md`, keep replacement
- MIXED: 27 → triage below
- NO: 29 → triage below
- SKIP: 11 → no action (originals never renamed)

**`.orig.md` files on disk:** 143

---

## NO Verdicts: Triage (29 files)

### Summary

| Disposition | Count | Description |
|------------|-------|-------------|
| REVERT | 22 | Restore `.orig.md` → `.md`, remove companion dir |
| NO ACTION | 7 | Original was never renamed or already restored |

**Root cause pattern:** 22 of 29 NOs are JS-heavy company/startup websites where static extraction (trafilatura) captured only thin marketing text, while the original Haiku paraphrases — created via WebFetch's headless browser — preserved richer content including JS-rendered team lists, technical specs, and funding details.

### REVERT — restore original (22 files)

These files have `.orig.md` (original) + `.md` (thin replacement) + companion dir. Action: `mv .orig.md .md` (overwrites replacement), `rm -rf` companion dir.

| # | Concept | File | New vs Orig (lines) | Reason |
|---|---------|------|---------------------|--------|
| 1 | 04-laser-icf | `iter-01/sources/hb11-company-overview` | 13 vs 36 | JS-heavy; lost team, partnerships, funding |
| 2 | 04-laser-icf | `iter-01/sources/hb11-technology-page` | 15 vs 19 | JS-heavy; lost ICF + Fast Ignition specs |
| 3 | 04-laser-icf | `iter-02/sources/hb11-technology-page-2025` | 15 vs 29 | JS-heavy; same URL as #2 |
| 4 | 05-planar-coil-stellarator | `iter-01/sources/thea-energy-website-and-press` | 23 vs 57 | JS-heavy; lost Eos/Helios specs, funding, timeline |
| 5 | 07-maglif | `iter-01/sources/pacific-fusion-website-technology` | 53 vs 61 | JS-heavy; lost $900M funding, 156 modules, 60+ MA |
| 6 | 14-mtf-pneumatic | `iter-01/sources/general-fusion-technology-overview` | 17 vs 22 | JS-heavy; lost 24 prototypes, LM26 targets |
| 7 | 14-mtf-pneumatic | `iter-02/sources/general-fusion-lm26-milestones-2025` | 14 vs 30 | Video embed page; lost timeline, PI3 specs |
| 8 | 15-sfs-z-pinch | `iter-01/sources/zap-energy-website-how-it-works` | 27 vs 15 | JS-heavy; lost D-T fuel, 10 Hz, LiPb specs |
| 9 | 17-laser-icf-dd | `iter-01/sources/focused-energy-technology` | 19 vs 47 | JS-heavy; lost DPSSL specs, $40M Amplitude |
| 10 | 20-modular-hts-stellarator | `iter-01/sources/type-one-energy-infinity-two-design` | 61 vs 51 | Marketing; lost 800 MW, 350 MWe, Q>40, all params |
| 11 | 21-spherical-tokamak-hts | `iter-01/sources/tokamak-energy-overview` | 44 vs 46 | JS-heavy; lost founding, ST40, £250M+, timeline |
| 12 | 21-spherical-tokamak-hts | `iter-02/sources/tokamak-energy-roadmap` | 17 vs 40 | Paywalled (ANS); lost full ST progression roadmap |
| 13 | 22-projectile-icf | `iter-01/sources/first-light-fusion-technology` | 31 vs 93 | JS-heavy; lost projectile specs, FLARE, plant design |
| 14 | 23-laser-icf-nano | `iter-01/sources/hb11-energy-technology` | 11 vs 76 | JS-heavy; lost technical specs, team, reactor design |
| 15 | 23-laser-icf-nano | `iter-01/sources/marvel-fusion-technology` | 21 vs 68 | JS-heavy; lost nanostructured target details |
| 16 | 23-laser-icf-nano | `iter-02/sources/hb11-energy-2025-updates` | 15 vs 56 | JS-heavy; lost proton fast ignition details |
| 17 | 24-dense-plasma-focus | `iter-01/sources/lppfusion-website-technology` | 28 vs 76 | JS-heavy; lost Focus Fusion physics, device specs |
| 18 | 26-laser-icf-indirect | `iter-01/sources/xcimer-energy-website-and-science` | 14 vs 54 | JS-heavy; lost excimer specs, ArF technology |
| 19 | 27-polywell | `iter-01/sources/emc2-website-summary` | 13 vs 35 | JS-heavy; lost device specs, development history |
| 20 | 29-neg-tri-tokamak | `iter-01/sources/fusion-energy-base-profile` | 14 vs 16 | JS-heavy; lost magnet strategy quote |
| 21 | 31-laser-icf-oec | `iter-01/sources/blf-website-and-news` | 26 vs 58 | JS-heavy; lost OEC architecture, team, milestones |
| 22 | 35-polomac | `iter-01/sources/deutelio-company-profile` | 0 vs ~20 | JS-heavy; no content extracted |

**Note on reverted files:** Reverted files lose YAML frontmatter and companion dirs (provenance metadata). The original source URLs are preserved in the replacement report for future re-extraction if tooling improves (e.g., headless browser support in agentic-mbse).

### NO ACTION — already correct (7 files)

These files were never renamed (extraction was attempted but deemed NO immediately, original kept in place) or failed and were restored.

| # | Concept | File | Reason |
|---|---------|------|--------|
| 1 | 08-frc-w-direct-conversion | `iter-01/sources/contrary-research-helion` | JS SPA; extraction got 6 lines of footer/nav |
| 2 | 08-frc-w-direct-conversion | `iter-01/sources/docslib-helion-arpa-e-presentation` | JS document viewer; got sidebar only |
| 3 | 08-frc-w-direct-conversion | `iter-01/sources/helion-website-technology` | Multi-source compilation (8 URLs) far richer |
| 4 | 11-magnetic-mirror | `iter-01/sources/aps-dpp-2025-sutherland` | Garbled HTML entities in extraction |
| 5 | 29-neg-tri-tokamak | `iter-01/sources/venture-kick-profile` | Extraction failed (JS/cookie redirect) |
| 6 | 33-state-backed-tokamak | `iter-01/sources/neo-fusion-company-profile` | Site down (jbxnah.com timeout) |
| 7 | 34-compact-st-india | `iter-02/sources/iaea-fuse-pranos-profile` | SharePoint auth required |

---

## MIXED Verdicts: Triage (27 files)

### Summary

| Disposition | Count | Description |
|------------|-------|-------------|
| KEEP | 27 | Delete `.orig.md`, keep replacement |

### Rationale for KEEP-all

The MIXED pattern is consistent: the new extraction captures **verbatim text from a single authoritative source** with full provenance (YAML frontmatter, companion dir with `raw.html`/`raw.pdf`, `metrics.json`), while the original was a **lossy Haiku paraphrase synthesizing multiple sources**.

Keeping the replacement is correct because:
1. **Provenance**: YAML frontmatter + companion dir creates a traceable chain. The Haiku paraphrases have no provenance — you can't verify claims against the original text.
2. **Verbatim text**: Replacement has the author's actual words, not Haiku's interpretation. This matters for quantitative claims.
3. **Breadth is recoverable**: Multi-source coverage lost by single-source replacement can be restored later by adding more sources. Fabricated content in Haiku summaries cannot be fixed.
4. **Analysis pipeline reads sources individually**: The concept analysis agent reads each source file separately. A richer single-source file is more useful than a lossy multi-source synthesis that conflates claims from different origins.

### KEEP — delete `.orig.md` (27 files)

| # | Concept | File | New vs Orig (lines) | What was gained | What was lost |
|---|---------|------|---------------------|-----------------|---------------|
| 1 | 01-hts-compact-tokamak | `iter-04/sources/cfs-2025-2026-updates` | 52 vs 34 | Verbatim Fortune article, direct quotes | Multi-source breadth (5 sources) |
| 2 | 02-acoustic-icf | `iter-01/sources/sonofusion-energy-website` | 11 vs 21 | Actual page text | Haiku reformatting (neither has tech content) |
| 3 | 03-laser-icf-liquid-jet | `iter-01/sources/cortex-fusion-website` | 83 vs 33 | 11 patent applications, 4 publications | Tech description (isochoric heating, OAM) |
| 4 | 04-laser-icf | `iter-02/sources/hb11-recent-developments-2024-2025` | 23 vs 65 | Verbatim H2 Tech article, McKenzie quote | Multi-source breadth (6 sources) |
| 5 | 07-maglif | `iter-01/sources/fuse-energy-technology` | 47 vs 42 | Timeline milestones, TITAN specs | Wikipedia details (APEIRON-I, ICECAP) |
| 6 | 07-maglif | `iter-01/sources/z-ife-power-plant-concept` | 71 vs 36 | Verbatim OSTI abstract, chamber specs | Multi-source synthesis (3 sources) |
| 7 | 10-large-scale-stellarator | `iter-02/sources/gauss-fusion-partnerships-2025` | 22 vs 26 | Full article prose, Roveda quote | Better-structured partnership categories |
| 8 | 11-magnetic-mirror | `iter-01/sources/wham-experiment-details` | 16 vs 31 | Full page prose, ARPA-E/HTS details | Structured bullet points, WIPPL params |
| 9 | 13-electrostatic-hybrid | `iter-01/sources/talk-polywell-orbitron-paper-discussion` | 20 vs 14 | AIP paper link, forum posts | Curated analysis (Brillouin limit, 300kV) |
| 10 | 15-sfs-z-pinch | `iter-02/sources/century-and-fuze-a-updates-2025` | 52 vs 47 | Verbatim APS DPP abstract, FuZE-A intro | Multi-source breadth (FST paper, TechCrunch) |
| 11 | 17-laser-icf-dd | `iter-01/sources/xcimer-energy-approach` | 29 vs 45 | Core approach narrative, cost reduction | Specific specs (10+ MJ, 248 nm, HYLIFE III) |
| 12 | 17-laser-icf-dd | `iter-02/sources/hylife-energy-conversion-notes` | 111 vs 31 | OSTI bibliographic record, BOP definition | Analytical comparison (steam vs He Brayton) |
| 13 | 18-p-b11-frc | `iter-01/sources/tae-energy-conversion-notes` | 1618 vs 30 | **Complete ICC patent** (US7459654B2) | Multi-source analytical comparison |
| 14 | 18-p-b11-frc | `iter-02/sources/tae-djt-merger-davinci-specs` | 23 vs 25 | ANS journalism, governance scrutiny | Da Vinci timeline milestones |
| 15 | 19-orbital-lev-dipole | `iter-01/sources/levitated-dipole-technical-background` | 59 vs 49 | Full Wikipedia article, LDX/CTX history | Multi-source breadth (arXiv, MIT LDX) |
| 16 | 19-orbital-lev-dipole | `iter-02/sources/zephyr-fusion-web-sources-2026` | 30 vs 41 | DCD journalism, direct Burke/Hinson quotes | Multi-source breadth (8 sources) |
| 17 | 20-modular-hts-stellarator | `iter-01/sources/renaissance-fusion-technology` | 66 vs 48 | Full tech page narrative, HTS paradigm | Quantitative specs from journal papers |
| 18 | 21-spherical-tokamak-hts | `iter-02/sources/tokamak-energy-st-e1-design-evolution` | 21 vs 41 | WNN article, DPP 2024 specs | Design evolution tracking (DPP 2024→2025 param changes) |
| 19 | 21-spherical-tokamak-hts | `iter-03/sources/tokamak-energy-ec-heating-pilot-plant` | 29 vs 31 | EPJ abstract page | Additional extracted parameters |
| 20 | 22-projectile-icf | `iter-02/sources/first-light-flare-pivot-update` | 27 vs 51 | Verbatim WNN journalism | Multi-source compilation (projectile vs FLARE table) |
| 21 | 26-laser-icf-indirect | `iter-01/sources/inertia-enterprises-website-and-faq` | 45 vs 41 | Landing page content | FAQ content from multi-source |
| 22 | 26-laser-icf-indirect | `iter-02/sources/inertia-enterprises-2026-update` | 40 vs 55 | GlobeNewsWire article | Multi-source breadth (5 sources) |
| 23 | 28-hts-tokamak-full | `iter-02/sources/energy-singularity-technical-summary` | 23 vs 62 | Xinhua article, HH70 world record | Multi-source breadth (9 sources) |
| 24 | 29-neg-tri-tokamak | `iter-02/sources/firefly-website-2026` | 57 vs 36 | Team bios, advisor details | "About" section, tech description (JS) |
| 25 | 30-laser-icf-nif | `iter-01/sources/inertia-website-technical` | 45 vs 55 | Landing page content | Multi-source compilation with FAQ |
| 26 | 32-laser-icf-french | `iter-01/sources/taranis-project-details` | 43 vs 49 | Verbatim CNRS French text | English summary from multiple sources |
| 27 | 35-polomac | `iter-01/sources/jtsp-2024-polomac-technical-report` | 20 vs 18 | Journal abstract page | Similar content |

---

## Execution Plan

After user approval:

### Step 1: REVERT 22 NO files
```bash
# For each: mv .orig.md → .md (overwrites replacement), rm -rf companion dir
```

### Step 2: DELETE .orig.md for all KEEP files (YES + MIXED)
```bash
# For all 143 .orig.md files minus the 22 reverted ones = 121 deletions
find knowledge/concept_research/ -name "*.orig.md" -type f -delete
```

### Step 3: Verify
- No `.orig.md` files remain
- All REVERT files are originals (no YAML frontmatter)
- Source count matches expectations
- `find_sources()` glob no longer picks up `.orig.md` files

### Step 4: Update replacement report
- Add triage decisions to report summary
- Update verdict counts
- Mark Phase 6 complete in plan

---

## Report Summary Correction

The replacement report summary table shows `Total source files: 166` but the actual subtotals sum to 171 (102+28+30+11). The original spec counted 166 files; additional files were discovered during execution. The summary should be updated to `Total: 171` in Phase 6d.
