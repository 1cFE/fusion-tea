# Source Replacement Report — Phase 1a

**Created:** 2026-03-28
**Status:** In Progress

## Summary

| Metric | Count |
|--------|-------|
| Total source files | 166 |
| Replaced (YES) | 4 |
| Replaced (MIXED) | 1 |
| Not improved (NO) | 0 |
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

<!-- Entries added concept-by-concept during Phase 2 -->

