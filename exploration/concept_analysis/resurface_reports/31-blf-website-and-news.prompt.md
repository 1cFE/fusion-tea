# Source Acquisition: Re-source blf-website-and-news.orig.md

You are a research agent. Below is a legacy source file — a Haiku paraphrase
compiled from multiple URLs. Your job: find the actual URLs where this data
comes from, and extract each one as a proper individual source file using
`add-source`.

The file belongs to concept **31-laser-icf-oec-architecture** (concept number **31**).

## The Legacy File

```
# Blue Laser Fusion - Website and News Sources

## Company Website (bluelaserfusion.com)

### Homepage
- DT-based target for high gain fusion reaction
- Dual energy conversion: steam from blanket heat + direct conversion of charged particles
- 5 MJ laser capacity, 1 GW target plant
- World record 60,000x power stacking (2024)
- Target: 1 GW pilot plant by 2032

### Technology Page
- CBC injection laser: modular, single-mode, wavelength tunable, pulse shaping
- OEC: highly reflective mirrors in vacuum, pulse stacking >100,000x
- Based on proven LIGO gravitational wave detection technology
- MJ-class output, nanosecond pulses, 1-10 Hz rep rate
- Several hundred beams

### About Page
- Founded 2022 in California
- CEO: Shuji Nakamura (2014 Nobel Laureate for blue LED)
- CTO: Hiroaki Ohta (plasma physics, Kyoto University, former McKinsey, CEO of ACSL drone company)
- General Counsel: Richard Ogawa
- Partners: UC San Diego, UC Santa Barbara, University of Rochester, Caltech, Colorado State University, Osaka University

## INFUSE Awards
- 2024 DOE INFUSE award: OEC development with Caltech (Prof. Rana Adhikari)
- 2025 DOE INFUSE award: Advanced optical interference coatings with Colorado State University (Prof. Carmen Menoni)

## JST Moonshot Program (October 2025)
- Selected for Japan's Moonshot R&D Program Goal 10
- Led by Prof. Shinsuke Fujioka (BLF/Osaka collaborative research institute)
- Multi-year initiative for laser, target ignition, and reactor design

## Partnerships
- ITOCHU Corporation: capital and business alliance (March 2024)
- RSE (Italian energy research): MoU for joint R&D (November 2024)
- Toshiba Energy Systems & Solutions
- YUKI Holdings (metal processing)
- SoftBank, JAFCO (investors)

## Funding
- $25M seed round (2023)

## Published Machine/Plant
- No published specific machine design beyond the Optics Express paper reactor concept
- Reactor parameters given as ranges (0.1-2.8 GW, 1-10 Hz)

## Lab Experiments
- 1.5 m OEC prototype: finesse 419,000, enhancement factor 59,000 (CW, 2024)
- 15 m OEC systems under construction at Goleta facility and Osaka University
- No fusion experiments performed by BLF

## Note on Advanced Fuels
- Interesting Engineering article (secondary source) mentions BLF looking at boron fuel
- However, ALL primary sources (website, Optics Express paper) specify D-T fuel
- The boron mention appears aspirational/long-term; current design is firmly D-T
- Website homepage explicitly says "DT based target"

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
uv run python scripts/run_analysis.py add-source 31 "<url>"
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
3. Extract confirmed sources via `add-source 31 "<url>"`

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
`/tmp/resurface/31-blf-website-and-news.json`

Use this exact format:

```json
{
  "orig_file": "blf-website-and-news.orig.md",
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
