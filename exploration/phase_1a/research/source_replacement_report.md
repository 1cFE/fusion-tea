# Source Replacement Report — Phase 1a

**Created:** 2026-03-28
**Status:** In Progress

## Summary

| Metric | Count |
|--------|-------|
| Total source files | 166 |
| Replaced (YES) | 22 |
| Replaced (MIXED) | 6 |
| Not improved (NO) | 5 |
| Skipped (SKIP) | 1 |
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

### 05-planar-coil-stellarator

| File | Category | URL | Verdict | Notes |
|------|----------|-----|---------|-------|
| `iter-01/sources/thea-energy-helios-arxiv-2512-08027.md` | URL | https://arxiv.org/html/2512.08027v1 | **YES** | 1067 lines vs 104 orig. Full Swanson et al. paper via arXiv HTML: complete plasma parameters, power balance, magnet system (12 encircling + 324 shaping coils), blanket design (Pb-17Li, EUROFER97), multi-layer shielding, novel X-point divertor (51K hexagonal W tiles), steam Rankine cycle, sector-based maintenance, energetic particle confinement (ASCOT5), MHD stability (TERPSICHORE, M3D-C1). Orig was a well-curated parameter list but lacked context, methodology, and design rationale. WebFetch returned comprehensive structured summary. Companion: `raw.html` (269KB), `metrics.json`. |
| `iter-01/sources/thea-energy-website-and-press.md` | URL | https://thea.energy/ | **NO** | 23 lines (with frontmatter) vs 57 orig. Landing page is marketing copy — no quantitative specs, no machine parameters, no timeline dates. Orig was a multi-source compilation from 6+ subpages (thea.energy/fusion-technology/, /eos/, press releases, ANS article) with detailed funding ($3M ARPA-E, $20M Series A), machine specs (Eos: 16T coil field, <40 MWe, 0.2 g/day tritium; Helios: 1.1 GW, 390 MWe, $150→$60/MWh LCOE), and timeline. WebFetch got same thin marketing text. |
| `iter-02/sources/thea-energy-canis-prototype-arxiv-2503-18960.md` | URL | https://arxiv.org/html/2503.18960v1 | **YES** | 427 lines vs 42 orig. Full Nash et al. paper via arXiv HTML: complete 3×3 HTS coil array design, REBCO conductor specs (4mm tape, SMI architecture, multi-supplier), cryogenic system (LN₂ first stage, 20K/20bar He second stage, 325W cooling capacity), field shaping results (EOS1: 0.56% RMS, EOS2: 0.60% RMS), Monte Carlo uncertainty analysis (7578 runs), power supply specs, current lead design. Orig had only key parameters. WebFetch returned excellent structured summary. Companion: `raw.html` (136KB), `metrics.json`. |
| `iter-02/sources/thea-energy-doe-certification-jan2026.md` | URL | https://thea.energy/press-release/...doe-certifies.../ | **YES** | 31 lines vs 30 orig. Similar length but substantively different: new extraction has full verbatim press release text with direct quotes from CEO Berzin, DOE's Allain, PPPL's Parra-Diaz. Includes $46M program funding, NASA COTS comparison, Eos 2030 timeline, 5-state site selection, 200-page report detail. Orig was a curated summary that captured facts but lost all direct quotes and program context. WebFetch returned comparable structured summary. Companion: `raw.html`, `metrics.json`. |

### 06-magnetic-mirror

| File | Category | URL | Verdict | Notes |
|------|----------|-----|---------|-------|
| `iter-01/sources/arpa-e-fisch-2025-presentation.md` | URL | https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_08_Fisch.pdf | **YES** | 450 lines vs 70 orig. Full 20-slide presentation via PDF pipeline. 39 extracted images (diagrams, simulation plots, power balance). All CHARM architecture details, device components (mirror coils, biased electrode, RF walls, ponderomotive barriers), S5 PIC code results, (PB)² power balance code, company status (Pale Blue Fusion pivot), 4 patent applications, 29 publications listed, derisked questions summary. Orig was well-curated but missed slide-specific content, simulation visuals. WebFetch: cannot process PDFs. Companion: `raw.pdf`, `images/`, `metrics.json`, `decisions.json`, `cost.json`. |
| `iter-01/sources/princeton-arpa-e-funding-2022.md` | URL | https://www.princeton.edu/news/2022/03/10/fisch-receives-funding-unlikely-fantastic-clean-energy-technology | **YES** | 48 lines vs 22 orig. Full article by Liz Fuller-Wright with extensive direct quotes from Fisch ("holy grail of really clean, really abundant fusion energy"), Kolmes, Ochs (Jacobus Fellow). Includes Emily Carter comments, ARPA-E OPEN 2021 context, Secretary Granholm quote, team composition (2 postdocs + 2 grad students). Orig captured key facts but missed all quotes and narrative. WebFetch returned comparable structured summary. Companion: `raw.html`, `metrics.json`. |
| `iter-01/sources/technical-papers-summary.md` | SEARCH | (multi-source compilation) | **SKIP** | Genuine multi-source synthesis covering 7 Fisch group papers (PRL 2006, PoP 2022/2023/2024/2025, arXiv 2025) plus SWDEC patent and CMFX experiment. No single URL replaces this breadth. ARPA-E project page (arpa-e.energy.gov) is JS-rendered — both trafilatura and WebFetch returned empty content. Individual papers each cover only one aspect. The ARPA-E presentation PDF (file 1) covers the full program but is already a separate source. Kept original as-is. |
| `iter-02/sources/arpa-e-2025-fisch-presentation-notes.md` | URL | https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_08_Fisch.pdf | **YES** | 450 lines vs 99 orig. Same PDF as iter-01 file 1 — identical extraction. Orig was a more detailed slide-by-slide annotation (99 lines) vs the iter-01 orig (70 lines), but the new extraction supersedes both with full slide content plus 39 images. Companion: `raw.pdf`, `images/`, `metrics.json`, `decisions.json`, `cost.json`. |

### 07-maglif

| File | Category | URL | Verdict | Notes |
|------|----------|-----|---------|-------|
| `iter-01/sources/arxiv-2408-15206-pulsed-magnetic-fusion.md` | URL | https://arxiv.org/html/2408.15206v1 | **YES** | 462 lines vs 38 orig. Full paper via arXiv HTML: IMG pulser specs (90% efficiency, 200 kV, 100 ns), MagLIF scaling (χ ∝ I³max, 60 MJ at 60 MA), FLASH/CHICAGO codes, chamber engineering, target fabrication, rep-rate requirements. Orig captured key facts but missed detailed code descriptions, fabrication specs, and historical context. WebFetch returned excellent structured summary. Companion: `raw.html`, `metrics.json`. |
| `iter-01/sources/fuse-energy-technology.md` | URL | https://www.f.energy/ | **MIXED** | 47 lines vs 42 orig. Extraction captured timeline milestones and TITAN specs but missed details from Wikipedia source in orig (APEIRON-I hybrid fusion-fission blanket, ICECAP facility, patent count). Orig compiled from f.energy + Wikipedia. WebFetch returned richer content (LANL CRADA, $200M+ valuation, team credentials, Air Force SBIR). Single-source extraction loses multi-source breadth. |
| `iter-01/sources/pacific-fusion-website-technology.md` | URL | https://www.pacificfusion.com/ | **NO** | 53 lines vs 61 orig. Landing page is marketing copy — no quantitative specs (no $900M funding, no 156 modules, no 60+ MA current, no self-mag targets). Orig compiled from 5 subpages (founders letter, CRADA, breakthrough announcement, LowerCarbon). WebFetch also got only marketing text. |
| `iter-01/sources/z-ife-power-plant-concept.md` | URL | https://www.osti.gov/biblio/771517 | **MIXED** | 71 lines vs 36 orig. OSTI bibliographic record with full verbatim abstract (chamber specs: 4m radius, 8m tall, 80cm FLiBe blanket, 20cm Al wall, 100-year radioactivity decay). Orig compiled from 3 sources (OSTI + T&F + ResearchGate) with extracted power conversion cycle details and RTL material options not in the abstract. New has verbatim text; orig had broader synthesis. |
| `iter-02/sources/fuse-energy-not-boring-details.md` | URL | https://www.notboring.co/p/fuse-energy | **YES** | 846 lines vs 40 orig. Full Packy McCormick deep dive: complete TITAN specs (238 bricks, 0.8 MA, 1.6 MV, 1 TW), Z STAR (16 TITANs, 15 TW, 12.8 MA), APEIRON-I hybrid fusion-fission (90 TITANs, 50-70 MA, 20 MW fusion → 3 GW thermal), FAETON revenue model, defense market analysis ($2.5B radiation testing, $150B defense electronics), company history. WebFetch returned excellent structured summary. Companion: `raw.html`, `metrics.json`. |
| `iter-02/sources/pacific-fusion-interview-fusion-report.md` | URL | https://thefusionreport.substack.com/p/interview-with-pacific-fusion-on | **YES** | 47 lines vs 37 orig. Full interview article: DS architecture (156 IMG modules, 73×80m, 320 bricks/module, ±100kV, 160nF, 80 MJ stored, 10% to target), water tank chamber (6m insulator stack), 1000× NIF price-performance target, 100× facility gain, target cassette maintenance concept. Orig captured key specs but new has full article prose with NIF comparison and ICF tutorial context. WebFetch returned comparable structured summary. Companion: `raw.html`, `metrics.json`. |
| `iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md` | URL | https://www.osti.gov/servlets/purl/901970/ | **YES** | 4618 lines vs 43 orig. Full 147-page SAND2006-7148 report via PDF pipeline. 225 extracted images, 206 table rows, $2.01 extraction cost. Complete Z-IFE power plant study: all 4 thermal cycles evaluated (sCO2 Brayton, Rankine, gas Brayton, combined Brayton-Rankine), RTL design, FLiBe blanket, chamber dynamics, tritium breeding, target manufacturing, pulsed power architecture. Orig was a curated summary of key findings. WebFetch: cannot process PDFs. Companion: `raw.pdf`, `images/`, `metrics.json`, `decisions.json`, `cost.json`. |

<!-- Entries added concept-by-concept during Phase 2 -->

