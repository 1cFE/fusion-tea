# Research Agent: Autonomous Source Acquisition for Laser ICF - French National Direct Drive (D-T)

You are a research agent acquiring source documents to fill data gaps in a
fusion concept analysis. Your job is to search the web, triage candidates for
relevance and accessibility, and extract promising sources using the project's
`add-source` command. You do NOT analyze source content — a separate
source-integration step handles that.

## Files to Read

Read the analysis file, specifically **Section 6 (Data Gap Inventory)**:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/analysis.md`

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

### G-2: Total plant capital cost ($/kWe) — no plant study exists for GenF/TARANIS concept [FAILED]
- Iteration 2: searched "LLNL GEM laser IFE capital cost model inertial fusion energy plant $/kWe"

### G-10: Specific laser-to-target coupling efficiency for shock ignition at 3 MJ — direct drive claims 4–5× advantage; SI-specific percentage not quantified [CLOSED]
- Iteration 2: searched "shock ignition direct drive laser coupling efficiency OMEGA experiments site:osti.gov OR site:arxiv.org"
  - Extracted: osti-servlets-purl-1833260 (https://www.osti.gov/servlets/purl/1833260)

### G-12: Thermodynamic cycle specification and integration design — 'traditional power plant methods' only; steam Rankine assumed [SKIPPED]
- Iteration 2: searched (no queries)

### G-13: Li-6 enrichment supply chain capacity and cost — ORNL Li-6 production history; global enrichment constraints [PARTIAL]
- Iteration 2: searched "lithium-6 enrichment supply chain capacity cost fusion tritium breeding ORNL"
  - Extracted: neimagazine-analysis-enriched-lithium-and-advanced-nuclear (https://www.neimagazine.com/analysis/enriched-lithium-and-advanced-nuclear/)

### G-15: DPSSL diode cost trajectory ($/W) and manufacturing scale — Thales DPSSL roadmap; TRUMPF/LLNL diode cost study [CLOSED]
- Iteration 2: searched "DPSSL diode laser cost per watt trajectory fusion IFE $0.007/W target roadmap"
  - Extracted: arpa-e-sites-default-files-migrated-a05-zuegel (https://arpa-e.energy.gov/sites/default/files/migrated/A05-Zuegel-FusionWorkshop_03-07-23.pdf)



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
uv run python scripts/run_analysis.py add-source 32 "<url>"
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
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/iter-3/research_output.json`

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
