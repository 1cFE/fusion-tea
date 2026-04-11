# Research Agent: Autonomous Source Acquisition for MagLIF (D-T)

You are a research agent acquiring source documents to fill data gaps in a
fusion concept analysis. Your job is to search the web, triage candidates for
relevance and accessibility, and extract promising sources using the project's
`add-source` command. You do NOT analyze source content — a separate
source-integration step handles that.

## Files to Read

Read the analysis file, specifically **Section 6 (Data Gap Inventory)**:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/analysis.md`

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

### G-1: No plant study for IMG architecture: all TEA data from Z-IFE LTD-era (2006) [PARTIAL]
- Iteration 5: searched "Pacific Fusion IMG magnetized liner inertial fusion self-magnetizing target gain 60 MA preprint 2024 2025", "ARPA-E MagLIF magnetized liner fusion IMG inertial gun driver capital cost award 2023 2024"
  - Extracted: arxiv-2504-10680 (https://arxiv.org/abs/2504.10680)
- Iteration 6: searched "Pacific Fusion IMG pulsed power plant TEA cost model techno-economic analysis 2025 2026 preprint"
  - Extracted: ans-news-2025-04-24-article-6980-pacific-fusion-fusing (https://www.ans.org/news/2025-04-24/article-6980/pacific-fusion-fusing-pulser-innovation-with-general-atomics-expertise/)
- Iteration 7: searched (no queries)
- Iteration 8: searched "Pacific Fusion IMG pulsed power plant cost model pilot plant economics arxiv 2025 2026"
  - Extracted: arxiv-2602-19389 (https://arxiv.org/abs/2602.19389)

### G-6: IMG driver capital cost at 60+ MA plant scale [FAILED]
- Iteration 5: searched "ARPA-E MagLIF magnetized liner fusion IMG inertial gun driver capital cost award 2023 2024"

### G-10: Thermal cycle above 900 K: high-temperature materials availability for He Brayton or combined cycle [SKIPPED]
- Iteration 5: searched "ODS ferritic steel SiC composite fusion reactor blanket 900K thermal efficiency He Brayton cycle material availability"
  - Extracted: frontiersin-journals-nuclear-engineering-articles-10-3389 (https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2025.1683702/full)
- Iteration 7: searched "SiC composite ODS ferritic steel fusion blanket He Brayton cycle 900K thermal efficiency materials availability 2024 2025"
- Iteration 8: searched (no queries)

### G-11: Pacific Fusion self-magnetizing target gain at 60+ MA (eliminates coils and laser) [FAILED]
- Iteration 5: searched "Pacific Fusion IMG magnetized liner inertial fusion self-magnetizing target gain 60 MA preprint 2024 2025"
  - Extracted: arxiv-2504-10680 (https://arxiv.org/abs/2504.10680)
- Iteration 6: searched "Pacific Fusion IMG pulsed power plant TEA cost model techno-economic analysis 2025 2026 preprint", "MagLIF laser preheat elimination laserless magnetized liner inertial fusion feasibility Pacific Fusion 2024 2025"
- Iteration 7: searched "Pacific Fusion self-magnetizing target MagLIF arxiv preprint 2025 2026 laserless preheat-free gain", ""self-magnetizing" OR "self magnetizing" MagLIF liner fusion target Z machine 2025 2026 site:arxiv.org"
  - Extracted: ans-news-2026-02-06-article-7739-fusion-simplification (https://www.ans.org/news/2026-02-06/article-7739/fusion-simplification-demonstrated-by-pacific-fusion-and-sandia/)
  - Failed: https://pubs.aip.org/aip/pop/article/32/4/042707/3344537/Simulated-thermonuclear-performance-of-auto — AIP Publishing paywall — extraction rc=1, no stderr. No open-access preprint found for this specific paper.
- Iteration 8: searched "arxiv "auto-magnetizing" OR "self-magnetizing" MagLIF liner thermonuclear preheat-free 2025 2026", "arxiv "dynamic screw pinch" OR "DSP-driven MagLIF" self-magnetizing fusion 2025", "site:osti.gov "self-magnetizing" OR "dynamic screw pinch" MagLIF 2025"
  - Failed: https://pubs.aip.org/aip/pop/article/32/5/052708/3347081/Integrated-simulations-of-premagnetized-and-self — AIP paywall. OSTI purl 404. ResearchGate 403. No open-access version found.

### G-12: Apeiron I hybrid fusion-fission: independent review of 150x fission amplification claim [CLOSED]
- Iteration 5: searched "Apeiron fusion fission hybrid z-pinch amplification Sandia 2007 neutron multiplication subcritical blanket", "Sandia 'In-Zinerator' Z-pinch fusion fission hybrid subcritical 2007 OSTI report Meier"
  - Extracted: osti-biblio-895981 (https://www.osti.gov/biblio/895981)

### G-13: Laser preheat elimination: feasibility at commercially relevant yields [FAILED]
- Iteration 5: searched (no queries)
- Iteration 6: searched "MagLIF laser preheat elimination laserless magnetized liner inertial fusion feasibility Pacific Fusion 2024 2025", "MagLIF 'without laser' OR 'no laser' OR 'laser-free' OR 'preheat-free' target self-heating self-magnetizing 2024 2025 2026"
  - Extracted: globenewswire-news-release-2025-04-24-3067836-0-en-pacific (https://www.globenewswire.com/news-release/2025/04/24/3067836/0/en/Pacific-Fusion-and-General-Atomics-Team-Up-to-Deliver-Breakthroughs-in-Inertial-Fusion-Energy.html)
- Iteration 7: searched (no queries)
- Iteration 8: searched "arxiv "auto-magnetizing" OR "self-magnetizing" MagLIF liner thermonuclear preheat-free 2025 2026"

### G-3: Rep-rated yield demonstration: gain not validated above chi ≈ 0.1 [FAILED]
- Iteration 6: searched "MagLIF repetitive operation rep rate pulsed magnetic fusion experimental yield demonstration 2024 2025 2026", "arxiv 'pulsed magnetic fusion' 'repetitive' OR 'rep rate' site:arxiv.org 2025"
  - Failed: https://pubs.aip.org/aip/pop/article/32/2/022507/3336518/Progress-and-issues-with-pulsed-magnetic-fusion — 403 Forbidden — AIP paywall. No open-access preprint found.



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
uv run python scripts/run_analysis.py add-source 07 "<url>"
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
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/iter-9/research_output.json`

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
