# Source Acquisition: Re-source tokamak-energy-roadmap.orig.md

You are a research agent. Below is a legacy source file — a Haiku paraphrase
compiled from multiple URLs. Your job: find the actual URLs where this data
comes from, and extract each one as a proper individual source file using
`add-source`.

The file belongs to concept **21-spherical-tokamak-hts** (concept number **21**).

## The Legacy File

```
# Tokamak Energy Development Roadmap

## Device Progression

### ST40 (Operational)
- Compact spherical tokamak with copper magnets
- R0 ≈ 0.4 m, R/a ≈ 1.8
- Target: Ip = 2 MA, Bt0 = 3 T
- Achievement: 100 million °C plasma (2022) — highest in private spherical tokamak
- Heating: NBI + 1 MW ECRH gyrotron (from Kyoto Fusioneering, 2025)
- <1 cubic meter plasma volume — "15× less volume than any other tokamak achieving same threshold"

### ST80-HTS (Under Construction)
- World's first high-field spherical tokamak with HTS magnets at scale
- Completion: 2026
- Pulse length target: up to 15 minutes
- Purpose: demonstrate ST operations, inform ST-E1 design
- Target: higher triple product than any previous fusion device

### ST-E1 (Pilot Plant)
- Fusion pilot plant — demonstrate grid electricity delivery
- Timeline: early 2030s
- Design evolution: see st-e1-design-evolution.md
- Rev D (Nov 2025): 5.0 m major radius, A=2.3, 5.25 T, 450-750 MW net
- Part of US DOE Milestone-Based Fusion Development Program

### Commercial Plants
- Target: 500 MW commercial fusion plants in mid-2030s (per ANS article)

## Lab Experiments (Spherical Tokamak Physics)
- **START** (Culham, UK): First spherical tokamak, 1991. Demonstrated beta up to 12%.
- **MAST-U** (Culham/UKAEA): Mega Amp Spherical Tokamak Upgrade. First campaign 2021.
- **NSTX-U** (PPPL, US): National Spherical Torus Experiment Upgrade.
- **Globus-M2** (Ioffe Institute, Russia): Spherical tokamak experiment.

## Sources
- https://www.ans.org/news/article-4447/tokamak-energy-bets-its-spherical-design-will-deliver-fusion-energy-in-the-early-2030s/
- https://www.theengineer.co.uk/content/news/tokamak-energy-st80-hts-hailed-as-next-step-to-grid-fusion
- https://www.prnewswire.com/news-releases/tokamak-energy-announces-st80-hts-advanced-prototype-on-path-to-demonstrate-grid-ready-fusion-power-in-the-early-2030s-301659095.html
- https://royalsocietypublishing.org/doi/10.1098/rsta.2017.0438

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
uv run python scripts/run_analysis.py add-source 21 "<url>"
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
3. Extract confirmed sources via `add-source 21 "<url>"`

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
`/tmp/resurface/21-tokamak-energy-roadmap.json`

Use this exact format:

```json
{
  "orig_file": "tokamak-energy-roadmap.orig.md",
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
