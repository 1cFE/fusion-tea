# Research Agent: Autonomous Source Acquisition for State-Backed Tokamak - BEST

You are a research agent acquiring source documents to fill data gaps in a
fusion concept analysis. Your job is to search the web, triage candidates for
relevance and accessibility, and extract promising sources using the project's
`add-source` command. You do NOT analyze source content — a separate
source-integration step handles that.

## Files to Read

Read the analysis file, specifically **Section 6 (Data Gap Inventory)**:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/analysis.md`

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

### G-2: Capital cost for BEST or any Chinese commercial fusion device not published [PARTIAL]
- Iteration 2: searched "Chen 2015 "preliminary cost assessment" CFETR "Journal of Fusion Energy" China fusion engineering test reactor", ""integrated cost models" fusion power plants 2025 tokamak LCOE capital cost"
  - Extracted: scientific-publications-wp-content-uploads-extrapolating (https://scientific-publications.ukaea.uk/wp-content/uploads/Extrapolating_Costs_to_Commercial_Fusion_Power_Plants.pdf)
  - Failed: https://www.researchgate.net/publication/395795447_Developing_Integrated_Cost_Models_for_Fusion_Power_Plants — extraction failed (rc=1) — ResearchGate login required for full PDF download

### G-4: Formal power conversion cycle commitment for PFPP not made (sCO2 preferred but not committed) [FAILED]
- Iteration 2: searched "CFETR sCO2 supercritical CO2 Brayton cycle power conversion fusion plant China 2024 2025"

### G-11: H&CD portfolio selection and recirculating power for commercial PFPP [CLOSED]
- Iteration 2: searched "CFETR heating current drive NBI ECRH LHCD commercial fusion recirculating power efficiency"
  - Extracted: osti-pages-servlets-purl-1465662 (https://www.osti.gov/pages/servlets/purl/1465662)

### G-14: Tritium permeation through CO2-facing heat exchangers in COOL TBM / sCO2 circuit [SKIPPED]
- Iteration 2: searched "tritium permeation supercritical CO2 sCO2 fusion blanket heat exchanger LiPb"



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
uv run python scripts/run_analysis.py add-source 33 "<url>"
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
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/iter-3/research_output.json`

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
