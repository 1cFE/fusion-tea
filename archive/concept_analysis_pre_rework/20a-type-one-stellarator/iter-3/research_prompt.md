# Research Agent: Autonomous Source Acquisition for QI Modular HTS Stellarator - Infinity Two

You are a research agent acquiring source documents to fill data gaps in a
fusion concept analysis. Your job is to search the web, triage candidates for
relevance and accessibility, and extract promising sources using the project's
`add-source` command. You do NOT analyze source content — a separate
source-integration step handles that.

## Files to Read

Read the analysis file, specifically **Section 6 (Data Gap Inventory)**:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/analysis.md`

Section 6 contains a table of data gaps. Each row has:
- Gap number
- Description of what data is missing
- Which analysis section(s) need it
- Gap type: `not-yet-sourced`, `proprietary`, `truly-unknown`, or `derivable`
- Priority: `blocking`, `important`, or `nice-to-have`
- Source recommendations (where to look)

**You are only targeting `not-yet-sourced` gaps.** Skip all other gap types.


## Prior Research Attempts

The following gaps have been attempted in previous iterations. Do NOT
re-attempt gaps marked CLOSED or FAILED. Gaps marked PARTIAL may be
re-attempted with different search queries.

## Prior Research Attempts (do not re-attempt these)

### G-3: Thermal efficiency (confirmed) — implied ~38–42% from power balance but 'Rankine with reheat > 30%' is the only published bound [PARTIAL]
- Iteration 2: searched "Type One Energy Infinity Two stellarator thermal efficiency power balance 2025"
  - Extracted: cambridge-core-journals-journal-of-plasma-physics-article (https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/comprehensive-unified-baseline-physics-design-for-the-type-one-energy-stellarator-fusion-pilot-power-plant-infinity-two/CB8A21D770BFA375A9865A28EFBE800B)

### G-6: ECRH auxiliary power confirmed value — upper bound derivable from Q>40; actual Q value not published so actual ECRH power unknown [PARTIAL]
- Iteration 2: searched "Type One Energy Infinity Two ECRH heating power MW Journal Plasma Physics 2025"

### G-9: HCPB blanket module replacement interval and cost for stellarator geometry — EU-DEMO studies suggest ~5 dpa limit for Li4SiO4 [FAILED]
- Iteration 2: searched "HCPB blanket Li4SiO4 pebble neutron irradiation damage replacement interval EU-DEMO dpa"
  - Failed: https://www.mdpi.com/2673-4362/4/3/37 — Extraction failed (rc=1, no stderr) — likely JavaScript-rendered MDPI page incompatible with extraction backend

### G-10: Beryllium pebble supply chain and cost at fusion plant scale — Materion Corp and Heraeus produce Be pebbles for EU-DEMO TBM [CLOSED]
- Iteration 2: searched "beryllium pebbles neutron multiplier HCPB blanket supply cost fusion EU-DEMO Materion"
  - Extracted: science-media-fes-pdf-fes-presentations-2022-pearson (https://science.osti.gov/-/media/fes/pdf/fes-presentations/2022/Pearson_resource-availability-and-supply_presentation.pdf)

### G-12: Remote maintenance system for non-axisymmetric stellarator geometry — W7-X remote handling provides partial basis [FAILED]
- Iteration 2: searched "W7-X remote maintenance stellarator non-axisymmetric blanket handling robot 2024 2025"



## Instructions

For each `not-yet-sourced` gap (prioritize `blocking` > `important` > `nice-to-have`):

### Step 1: Search (up to 5 WebSearch calls total)

Construct search queries from the gap's description and source recommendations.
Try multiple query strategies:
- Direct technical terms from the gap description
- Site-scoped queries for known databases: `site:arxiv.org`, `site:osti.gov`,
  `site:scholar.google.com`, `site:iaea.org`
- Author names or report numbers if mentioned in source recommendations
- Company name + technical parameter (e.g., "CFS ARC capital cost")

### Step 2: Triage (WebFetch for relevance checks)

For each promising search result, use WebFetch to check:
- Is the content actually accessible (not paywalled, not 403/404)?
- Is it relevant to the specific data gap?
- Is it a full document (not a landing page, abstract-only page, or JS-empty shell)?
- Does it contain quantitative data, cost estimates, or technical parameters?

**IMPORTANT:** WebFetch passes content through a summarizer. Use it ONLY for
relevance and accessibility checks. NEVER use WebFetch output as source
content — it is lossy and unsuitable for citation.

### Step 3: Extract (up to 3 extractions total)

For URLs that pass triage, extract them using this Bash command:

```
uv run python scripts/run_analysis.py add-source 20a "<url>"
```

Run this command from the working directory (it will be set correctly).

- One URL per `add-source` call. Never combine multiple URLs.
- If extraction fails (timeout, paywall, empty content), log the failure and
  continue to the next candidate.
- Before extracting, verify the URL is not already present in the concept's
  existing sources (check filenames in the analysis or prior research log).

## Source Quality Hierarchy

Prioritize sources in this order:
1. **Peer-reviewed papers** (journals, conference proceedings)
2. **Government reports** (OSTI, DOE, IAEA, national lab publications)
3. **Institutional pages** (university research groups, national lab project pages)
4. **Press releases** (company announcements with technical detail)
5. **News articles with direct quotes** (The Engineer, NEI Magazine, WNN)
6. **News summaries** (trade press without primary data)

Blog posts and forums are NOT acceptable as sole sources for quantitative claims.

## News-Site Heuristic

When company websites return nothing useful (JS-heavy, login-required, empty
content), search for news coverage of the company's announcements on standard
HTML sites that are reliably extractable:
- The Engineer (theengineer.co.uk)
- NEI Magazine (neimagazine.com)
- World Nuclear News (world-nuclear-news.org)
- GlobeNewsWire (globenewswire.com)
- ANS Nuclear Newswire (ans.org/news)
- Fusion Industry Association press releases

## Rules

1. **NEVER** use WebFetch output as source content. WebFetch is for triage only.
2. **NEVER** write source files manually. Every source MUST come from `add-source`.
3. **One URL per `add-source` call.** No multi-source compilations.
4. **Check for duplicates** before extracting — if a URL's domain and title
   match an existing source, skip it.
5. **Respect budget limits:** At most 5 WebSearch calls and
   3 source extractions per invocation.
6. **Log everything:** Record all searches, triage decisions, and outcomes in
   the output file (see Output section below).

## Output

After completing your search-triage-extract work, write a JSON results file
using the Write tool to:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/iter-3/research_output.json`

Use this exact format:

```json
{
  "gaps_attempted": [
    {
      "gap_id": "G-1",
      "gap_description": "Description from Section 6 table",
      "queries": ["search query 1", "search query 2"],
      "candidates": [
        {
          "url": "https://example.com/paper",
          "title": "Paper Title",
          "triage": "relevant",
          "notes": "Contains cost data for subsystem X"
        },
        {
          "url": "https://paywalled.com/paper",
          "title": "Paywalled Paper",
          "triage": "paywall",
          "notes": "IEEE access required"
        }
      ],
      "extracted": [
        {
          "url": "https://example.com/paper",
          "source_name": "example-paper-title"
        }
      ],
      "failed": [
        {
          "url": "https://broken.com/page",
          "reason": "403 Forbidden — institutional access required"
        }
      ],
      "status": "closed"
    }
  ],
  "summary": {
    "gaps_attempted": 2,
    "sources_extracted": 1,
    "sources_failed": 1,
    "searches_used": 3,
    "extractions_used": 1
  }
}
```

**Gap status values:**
- `closed` — gap addressed (source extracted that covers it)
- `partial` — some relevant sources found but gap not fully addressed
- `failed` — searched but nothing accessible/relevant found
- `skipped` — gap deprioritized due to budget limits

**Gap ID format:** Use "G-N" where N is the gap number from the Section 6 table.

Write this file even if no sources were extracted — the log of what was
searched and why candidates were rejected is valuable for future iterations.
