# Source Replacement Report — Phase 1a

**Created:** 2026-03-28
**Status:** In Progress

## Summary

| Metric | Count |
|--------|-------|
| Total source files | 166 |
| Replaced (YES) | 12 |
| Replaced (MIXED) | 4 |
| Not improved (NO) | 3 |
| Skipped (SKIP) | 0 |
| Failed | 0 |

## Quality Verdicts

- **YES** — New extraction is substantively richer than original
- **NO** — New extraction is not better (paywall, JS-only, thin content)
- **MIXED** — New extraction has some gains but also some losses
- **SKIP** — Original URL could not be found or recovered

## Replacement Log

### 11-magnetic-mirror (Phase 1 test)

| File | Category | URL | Verdict | Notes |
|------|----------|-----|---------|-------|
| `iter-01/sources/realta-fusion-hub-spotlight.md` | URL | https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion | **YES** | 259 lines vs 37 orig. Full article with direct quotes, mirror ratio physics, HTS magnets, device timeline (WHAM/WHAM++/HAMMIR), industrial heat strategy. WebFetch returned ~25-line bullet summary. Companion dir: `raw.html` (392KB), `metrics.json`. Frontmatter: `source`, `content_hash_sha256`, `backend: trafilatura`. |

### 01-hts-compact-tokamak

| File | Category | URL | Verdict | Notes |
|------|----------|-----|---------|-------|
| `iter-03/sources/arc-reactor-specifications.md` | URL | https://arxiv.org/pdf/1409.3540 | **YES** | 2219 lines vs 60 orig. Full 35-page Sorbom et al. paper via PDF pipeline. 94 extracted images (equations, figures, tables). Companion: `raw.pdf`, `images/`, `metrics.json`, `decisions.json`. WebFetch returned ~20-line abstract summary. Massive quality improvement — complete paper with all parameters, design details, and blanket analysis. |
| `iter-03/sources/sparc-icrf-heating-paper.md` | URL | Cambridge Core (SPARC ICRF) | **YES** | 428 lines vs 18 orig. Full open-access paper by Lin, Wright, Wukitch. Complete ICRF system description: antenna design, heating scenarios, power coupling analysis. WebFetch returned only tracking code / JS metadata (no article content). Companion: `raw.html`, `metrics.json`. |
| `iter-04/sources/arc-power-conversion-studies.md` | URL | Local PDF (SSRN-4482183) | **YES** | 579 lines vs 29 orig. Full Colliva et al. paper from local PDF. 20 extracted images (tables, equations, figures). Detailed comparison of Rankine, sCO2 Brayton, and He Brayton cycles with GateCycle modeling results. Original MDPI URL returned 403; used SSRN preprint PDF provided by user. Companion: `images/`, `metrics.json`, `decisions.json`. `source_type: local_file`. |
| `iter-04/sources/cfs-2025-2026-updates.md` | SEARCH | https://fortune.com/2026/01/07/fusion-power-commonwealth-sparc-nuclear-fusion-pilot-ai-siemens-nvidia/ | **MIXED** | 52 lines vs 34 orig. Fortune CES 2026 article: magnet installation, ARC Virginia 400 MWe, Nvidia/Siemens digital twin. Richer prose but covers only one source; orig compiled 5+ sources (Google/Eni PPAs, operation mode details, funding amounts). WebFetch returned similar bullet summary. Extraction is a better single-source capture but loses the multi-source synthesis. |

### 02-acoustic-icf-sonofusion

| File | Category | URL | Verdict | Notes |
|------|----------|-----|---------|-------|
| `iter-01/sources/bubble-fusion-scientific-history.md` | SEARCH | https://en.wikipedia.org/wiki/Bubble_fusion | **YES** | 177 lines vs 42 orig. Full Wikipedia article: Taleyarkhan 2002 experiments, Oak Ridge failed replication, subsequent replication attempts, Purdue misconduct investigation, ONR debarment, DARPA report, Impulse Devices. Orig was a multi-source synthesis; Wikipedia covers the same ground more thoroughly with citations. WebFetch returned 403 (Wikipedia blocks it). Companion: `raw.html` (211KB), `metrics.json`. |
| `iter-01/sources/sonofusion-energy-website.md` | URL | https://www.sonofusion.energy/ | **MIXED** | 11 lines vs 21 orig. Page is genuinely thin (698 chars of actual content — two marketing paragraphs). New extraction captures actual text faithfully. Orig Haiku paraphrase was longer because it reformatted the same facts into bullet lists and added an editorial "Technical Details Absent" section. WebFetch returned more content (climate stats: "10-15 years", "60% by 2050", "$23T wealth reduction"; scalability claims: "table-top" to "utility-scale") that trafilatura missed — likely JS-rendered sections. Neither version has substantive technical content because the source page doesn't. |
| `iter-01/sources/ucla-putterman-group-sonoluminescence.md` | URL | http://acoustics-research.physics.ucla.edu/sonoluminescence/ | **YES** | 70 lines vs 29 orig. Full page content: detailed experiment descriptions (drop tower, shake tube, sulfuric acid, water SL, multi-bubble), dense microplasma section (charge density >10²¹/cm³), acoustic neutron detector specs (20% efficiency, ns timing), fusion discussion (Taleyarkhan non-replication), publication links (Nature 1991, Physics Today 2012). WebFetch returned comparable structured summary. Companion: `raw.html` (55KB), `metrics.json`. |

### 03-laser-icf-liquid-jet-target

| File | Category | URL | Verdict | Notes |
|------|----------|-----|---------|-------|
| `iter-01/sources/arxiv-2308-levitt-quantum-control.md` | URL | https://arxiv.org/pdf/2308.07417 | **YES** | 478 lines vs 18 orig. Full Levitt paper via PDF pipeline. Complete quantum control framework, ultrafast laser architectures, Schrödinger equation solutions, net power conditions. 7 extracted images (equations, figures). WebFetch returned abstract only. Companion: `raw.pdf`, `images/`, `metrics.json`, `decisions.json`, `cost.json`. |
| `iter-01/sources/arxiv-2503-nanoshell-paper.md` | URL | https://arxiv.org/pdf/2503.15531 | **YES** | 220 lines vs 54 orig. Full Kharzeev/Levitt/Trallero-Herrero nanoshell paper via PDF pipeline. Complete derivation: plasmonic field enhancement, deuteron kinematics, fusion rate calculations, reactor parameter estimates (Q~100, 1 MW). Orig had excellent structured summary but was paraphrased; new has verbatim paper text. Companion: `raw.pdf`, `raw.html`, `metrics.json`, `decisions.json`. |
| `iter-01/sources/cortex-fusion-website.md` | URL | https://www.cortexfusion.systems/ | **MIXED** | 83 lines vs 33 orig. Extraction landed on Patents/Publications section: 11 specific patent applications (US numbers) and 4 publications. Lost technology description (isochoric heating, orbital angular momentum, >1000 Tesla, nanophotonic targets) present in orig. WebFetch captured the tech description. JS-heavy single-page app — different sections resolve to same URL. Companion: `raw.html`, `metrics.json`. |
| `iter-01/sources/kHz-liquid-sheet-fusion-paper.md` | URL | Cambridge Core (HPLSE) | **YES** | 562 lines vs 21 orig. Full Knight et al. paper: kHz-rate D-D fusion on thin D2O liquid sheet, three-detector neutron suite (EJ-309, ³He, bubble detectors), TOF analysis confirming 2.45 MeV neutrons. Original short URL returned 404; full slug URL worked. WebFetch returned 404. Companion: `raw.html`, `metrics.json`. |

### 04-laser-icf

| File | Category | URL | Verdict | Notes |
|------|----------|-----|---------|-------|
| `iter-01/sources/hb11-company-overview.md` | URL | https://hb11.energy/our-story/ | **NO** | 13 lines vs 36 orig. Very thin marketing text (3 paragraphs). Orig had detailed team (8 key people), partnerships (TINEX, INFUSE, Osaka), commercial model, funding ($23M), technical evolution. Page is heavily JS-rendered — team bios, partnerships loaded dynamically. WebFetch also got limited content. Trafilatura missed all structured content. |
| `iter-01/sources/hb11-osaka-experiment-2022.md` | URL | Local PDF (applsci-12-01444-v2.pdf) | **YES** | 320 lines vs 24 orig. Full Margarone/Batani et al. paper. Complete experimental setup (LFEX PW laser, ~3×10²⁰ W/cm², BN target), alpha particle measurements (~10¹⁰/sr), in-target vs pitcher-catcher geometry comparison. MDPI URL returned 403; used local PDF. Companion: `images/` (5 figures), `metrics.json`, `decisions.json`, `cost.json`. `source_type: local_file`. |
| `iter-01/sources/hb11-patent-reactor-design.md` | URL | https://patents.google.com/patent/US20170125129A1/en | **YES** | 671 lines vs 42 orig. Full patent text: claims, definitions, embodiments, all technical specifications (≥1 kT field, -1.4 MV bias, 714 A discharge, 1 GJ/reaction, cylindrical fuel 1cm×0.2mm). ~200 lines of Google Patents metadata (chemical compounds, classifications) followed by complete patent description. WebFetch returned excellent structured summary. Companion: `raw.html`, `metrics.json`. |
| `iter-01/sources/hb11-technology-page.md` | URL | https://hb11.energy/our-technology/ | **NO** | 15 lines vs 19 orig. Very thin — 4 paragraphs of high-level energy transition messaging. Orig had specific technical details: ICF + Fast Ignition, 8.7 MeV, thousands of commercial lasers, pellet injection ~1/s, conventional steam cycle generator. WebFetch captured those technical details. Page is JS-rendered — technical content not in static HTML. |
| `iter-02/sources/hb11-newatlas-article.md` | URL | https://newatlas.com/energy/hb11-hydrogen-boron-fusion-clean-energy/ | **YES** | 38 lines vs 27 orig. Full article text: direct quotes from McKenzie and Hora, reactor sphere design, two-laser system, direct electrostatic conversion claim, CPA laser mention, billion-times-better claim. Required sanitizer bugfix in agentic-mbse (`html_sanitize.py:69` tag.attrs None guard). WebFetch returned comparable structured summary. Companion: `raw.html`, `metrics.json`. |
| `iter-02/sources/hb11-recent-developments-2024-2025.md` | URL | https://h2-tech.com/news/2023/08-2023/hb11-energy-receives-grant-from-u-s-department-of-energy/ | **MIXED** | 23 lines vs 65 orig. Full H2 Tech DOE INFUSE article with McKenzie quote and LLE partnership details. But orig was multi-source compilation covering 6+ sources (INFUSE, TINEX $180M, Adelaide $8.2M, Optica OPN, 12 experiments, FusionXInvest funding). Single-source extraction loses breadth. |
| `iter-02/sources/hb11-technology-page-2025.md` | URL | https://hb11.energy/our-technology/ (same as iter-01) | **NO** | 15 lines vs 29 orig. Same extraction as `hb11-technology-page` (identical URL). Same JS-rendering issue — tech specs not in static HTML. Orig had similar content plus annotations about steam cycle vs direct conversion design evolution. Copied from iter-01 extraction. |

<!-- Entries added concept-by-concept during Phase 2 -->

