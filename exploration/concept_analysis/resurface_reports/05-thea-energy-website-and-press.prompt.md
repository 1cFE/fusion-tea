# Source Acquisition: Re-source thea-energy-website-and-press.orig.md

You are a research agent. Below is a legacy source file — a Haiku paraphrase
compiled from multiple URLs. Your job: find the actual URLs where this data
comes from, and extract each one as a proper individual source file using
`add-source`.

The file belongs to concept **05-planar-coil-stellarator** (concept number **05**).

## The Legacy File

```
# Thea Energy — Website & Press Sources

## Company Overview
- **Founded**: 2022, spin-out from Princeton Plasma Physics Laboratory (PPPL) and Princeton University
- **Former name**: Princeton Stellarators, Inc.
- **HQ**: New Jersey
- **CEO**: Brian Berzin
- **URL**: https://thea.energy/

## Funding
- DOE ARPA-E: $3M grant (2020, for permanent magnet stellarator research at PPPL)
- DOE INFUSE awards: 2 in 2022, 1 in 2023
- DOE Milestone-Based Fusion Development Program: Selected May 2023 (1 of 8 companies)
- Series A: $20M (September 2024) — Prelude Ventures lead

## Key Machines
- **Eos**: Demonstration stellarator / neutron source
  - Triple product target: 10^21 keV·s/m^3
  - Coil field: ~16 T at coil
  - <40 MW electric power consumption
  - Tritium production: ~0.2 g/day (70 g/year) via D-D
  - D-D fusion operations
  - First plasma target: 2030
  - HTS planar coils, only 1 size shaping coil
  - 30+ year magnet lifetime
  - 450+ independent control variables

- **Helios**: Commercial fusion pilot plant
  - 1.1 GW thermal, 390 MWe net electric
  - First plasma target: mid-2030s
  - DOE preconceptual design certified
  - LCOE target: $150/MWh initially → $60/MWh at scale

## Published Machines/Plants
- Helios preconceptual design (200-page report, arXiv:2512.08027)
- Eos design (Nuclear Fusion paper, Jan 2025)
- Both are published designs, though neither is built yet

## Lab Experiments (Heritage)
- Wendelstein 7-X (IPP Greifswald) — world's largest stellarator
- CNT (Columbia Non-neutral Torus, Columbia University) — stellarator experiment
- 3x3 superconducting planar coil array — Thea Energy's own prototype (2025)

## Nuclear Fusion Papers (Jan 2025)
1. "Stellarator fusion systems enabled by arrays of planar coils"
2. "Coil optimization methods for a planar coil stellarator"
3. "The scoping, design, and plasma physics optimization of the Eos neutron source stellarator"
4. "Fast ion confinement in quasi-axisymmetric stellarator equilibria"

Sources:
- https://thea.energy/fusion-technology/
- https://thea.energy/eos/
- https://thea.energy/press-release/thea-energy-announces-peer-reviewed-publications-outlining-the-planar-coil-stellarator-approach-for-commercial-fusion-energy/
- https://thea.energy/press-release/u-s-department-of-energy-certifies-thea-energys-fusion-pilot-plant-preconceptual-design/
- https://www.ans.org/news/2025-12-18/article-7628/
- https://interestingengineering.com/energy/thea-energy-unveils-helios-realistic-fusion-power-plant

```

## Instructions

### Phase 1: Extract URLs from the file

Scan the file above for URLs. They appear in headers using various formats:
- `**Sources**: url1, url2, ...` or `**Source**: url1, url2`
- `Source: url (description)` (no bold)
- Bullet lists under `## Source` or `## Sources` headings
- Inline URLs anywhere in the text body
- Domain names without `https://` prefix (e.g., "firstlightfusion.com")

List every URL you find. If no URLs are present, proceed directly to Phase 3.

### Phase 2: Try header URLs first

For each URL found in Phase 1, attempt extraction using this exact command:

```
uv run python scripts/run_analysis.py add-source 05 "<url>"
```

Run from the working directory (it will be set correctly).

Log the outcome for each URL:
- **Success**: source extracted — note the source filename created
- **Fail (JS/empty)**: URL returned thin or no content (JS-heavy company site) — note this, search for news coverage in Phase 3
- **Fail (404/timeout)**: URL is dead — note this
- **Fail (paywall/403)**: URL requires access — log for human action
- **Duplicate**: source name already exists in this concept — skip

If a URL is just a domain name (e.g., "firstlightfusion.com"), skip it — company
homepages are almost always JS-heavy. Search for news coverage in Phase 3 instead.

Stop after 3 successful extractions. If you hit the cap, proceed
directly to Phase 4.

### Phase 3: Search for uncovered claims

After Phase 2, review the original file content. Are there significant claims,
technical parameters, funding amounts, or data points NOT covered by any
successfully-extracted source?

For each uncovered claim cluster:
1. Use WebSearch to find alternative URLs (news articles, press releases,
   institutional pages) that contain the same data
2. Use WebFetch to triage candidates — check accessibility and relevance
3. Extract confirmed sources via `add-source 05 "<url>"`

**Source Quality Hierarchy** — prioritize sources in this order:
1. **Peer-reviewed papers** (journals, conference proceedings)
2. **Government reports** (OSTI, DOE, IAEA, national lab publications)
3. **Institutional pages** (university research groups, national lab project pages)
4. **Press releases** (company announcements with technical detail)
5. **News articles with direct quotes** (The Engineer, NEI Magazine, WNN)
6. **News summaries** (trade press without primary data)

Blog posts and forums are NOT acceptable as sole sources for quantitative claims.

**News-Site Heuristic** — when company websites return nothing useful (JS-heavy,
login-required, empty content), search for news coverage of the company's
announcements on standard HTML sites that are reliably extractable:
- The Engineer (theengineer.co.uk)
- NEI Magazine (neimagazine.com)
- World Nuclear News (world-nuclear-news.org)
- GlobeNewsWire (globenewswire.com)
- ANS Nuclear Newswire (ans.org/news)
- Fusion Industry Association press releases

### Phase 4: Coverage Assessment

After all extraction attempts, assess coverage:
- Which claims from the original file are now backed by at least one extracted source?
- Which claims remain uncovered?
- Recommendation:
  - `delete` — >80% of claims are covered by extracted sources. The `.orig.md` can be removed.
  - `partial` — 50-80% covered. Flag uncovered claims for human review.
  - `keep` — <50% covered. The `.orig.md` still holds unique data.

Also check: does a thin replacement `.md` file exist at the same path without
`.orig` (e.g., `foo.md` alongside `foo.orig.md`)? If so, note whether its content
is a subset of what the newly-extracted individual sources cover. If yes, it can
also be deleted.

## Rules

1. **NEVER** use WebFetch output as source content. WebFetch is for triage only.
2. **NEVER** write source files manually. Every source MUST come from `add-source`.
3. **One URL per `add-source` call.** No multi-source compilations.
4. **Check for duplicates** before extracting — if a URL's domain and title
   match an existing source file in this concept, skip it.
5. **At most 3 source extractions** per invocation.
6. **Log everything** in the output file (see Output section below).

## Output

After completing your work, write a JSON results file using the Write tool to:
`/tmp/resurface/05-thea-energy-website-and-press.json`

Use this exact format:

```json
{
  "orig_file": "thea-energy-website-and-press.orig.md",
  "urls_found": ["https://example.com/page1", "https://example.com/page2"],
  "extractions": [
    {
      "url": "https://example.com/page1",
      "source_name": "example-page-title",
      "outcome": "success",
      "covers": ["claim A", "claim B"]
    },
    {
      "url": "https://companysite.com/",
      "outcome": "fail_js",
      "notes": "JS-heavy, only navigation text extracted"
    }
  ],
  "uncovered_claims": [
    "Specific claim X — no accessible source found"
  ],
  "recommendation": "delete",
  "replacement_md_note": "Thin replacement (31 lines) is a subset of extracted sources"
}
```

**Outcome values:** `success`, `fail_js`, `fail_404`, `fail_paywall`, `fail_timeout`, `duplicate`, `skipped`

Write this file even if no sources were extracted — the log of what was
attempted and why it failed is valuable.
