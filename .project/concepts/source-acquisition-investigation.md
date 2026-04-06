# Source Acquisition Investigation: How Phase 1a Research Agents Created Source Files

**Date:** 2026-04-04
**Context:** During Phase 6 triage of source replacement NO verdicts, we investigated how the original `.orig.md` files were created, whether their data is real, and what tools were involved. This document captures everything learned, to inform the design of the autonomous source acquisition module.

---

## The Original Research Pipeline (Phase 1a)

### Prompt

The research agent prompt is at `exploration/phase_1a/prompt_templates/research.md`. The critical instruction is line 26:

> **Save important sources**: When you find a page with substantial technical detail, save it to `./sources/` with a descriptive filename (e.g., `company-website-technology.md`, `arxiv-2025-paper-summary.md`). Use the Write tool. **Save the key technical content, not the entire page.**

This tells the agent to write its own synthesis — not the actual page text, not exact quotes, not a per-fact URL mapping. The result is that every saved source file is the agent's interpretation of what it read, not the source material itself.

### Tools Available

The research agent had access to:

- **WebSearch** — searches the web, returns result snippets and URLs. This is a real search tool. The agent sees result titles, URLs, and short excerpts. Good for discovering which pages exist.
- **WebFetch(url, prompt)** — fetches a URL, converts HTML to markdown, then passes the markdown through a **small, fast model (Haiku 3.5)** with the given prompt. Returns Haiku's response. **The agent never sees the raw page content.** It sees Haiku's summary/extraction of the page.
- **Write tool** — writes files to disk. The agent uses this to save source files.

### What WebFetch Actually Does

This is the most important thing to understand. WebFetch is described in its tool spec as:

> "Fetches content from a specified URL and processes it using an AI model. Takes a URL and a prompt as input. Fetches the URL content, converts HTML to markdown. Processes the content with the prompt using a small, fast model. Returns the model's response about the content."

So the data flow is:

```
URL → HTTP GET → raw HTML → HTML-to-markdown conversion → Haiku 3.5 (with prompt) → summary text
```

The research agent sees ONLY the final output — Haiku's summary. It does NOT see:
- The raw HTML
- The converted markdown (pre-Haiku)
- The actual text on the page

This means:
- "Exact quotes" from WebFetch are Haiku's version of quotes, not verbatim page text
- Numbers and specs pass through Haiku's interpretation before the agent sees them
- If Haiku drops, paraphrases, or hallucinates a detail, the research agent has no way to detect it

### What WebFetch Does NOT Do

- It does **NOT** use a headless browser. It's a simple HTTP GET. If a page requires JavaScript to render content (SPA, dynamic loading), WebFetch gets the empty HTML shell.
- It does **NOT** render JavaScript. The "HTML to markdown" step works on the raw HTTP response.
- It does **NOT** execute cookies, handle redirects requiring JS, or interact with auth flows.

We originally blamed "JS-heavy sites" for the NO verdicts. This was partially correct (the primary company URLs are often JS-rendered), but misleading — the actual data in the `.orig.md` files came from external news sites that are standard HTML. More on this below.

### How the Agent Created Multi-Source Compilations

The research agent didn't just WebFetch one URL per source file. The typical flow was:

1. Agent receives research task for a concept (e.g., "First Light Fusion")
2. Agent calls WebSearch for "First Light Fusion fusion technology" → gets 10+ URLs
3. Agent calls WebFetch on several promising URLs:
   - firstlightfusion.com (company site — often JS-heavy, returns thin content)
   - newatlas.com article about First Light (standard HTML — returns full article summary)
   - neimagazine.com article (standard HTML — returns full article summary)
   - ipgroupplc.com press release (standard HTML — returns full content)
   - etc.
4. Agent compiles findings from ALL WebFetch calls into a single `.md` file
5. Agent writes the file with a header listing source domains

The result: a multi-source compilation where each fact could have come from any of 3-8 different pages, with no per-fact attribution.

### Header Quality Varies Wildly

The source file headers range from usable to garbage:

| File | Header | Quality |
|------|--------|---------|
| pacific-fusion-website-technology.orig.md | Lists 5 specific URLs (pacificfusion.com/updates/founders-letter, etc.) | Usable |
| hb11-company-overview.orig.md | "Sources: hb11.energy/our-story/, hb11.energy/, various news articles" | Mixed |
| first-light-fusion-technology.orig.md | "Sources: Multiple pages compiled from firstlightfusion.com, newatlas.com, ipgroupplc.com, neimagazine.com, nextbigfuture.com, interestingengineering.com" | Domain names only — no URLs |
| zap-energy-website-how-it-works.orig.md | "Source: https://www.zapenergy.com/how-it-works" | Single URL — good |

---

## Verification: Is the Data Real?

We spot-checked 3 concepts (10 quantitative claims) against independent sources.

### Test 1: HB11 Energy (concept 04)

`.orig.md` claims: "$23M funding (PitchBook)", 8 team members by name, "TINEX $180M"

- **WebFetch on hb11.energy/our-story/** returned full team bios matching all 8 names in the `.orig.md`. The team data IS in the server-rendered HTML — trafilatura's readability heuristics excluded it (it's in a team grid section, not article body), but WebFetch's simpler HTML-to-markdown captured it.
- **"$23M funding"** — NOT on hb11.energy. The `.orig.md` attributes it to "(PitchBook)". WebSearch confirmed PitchBook reports $23.3M.
- **"TINEX $180M"** — NOT on hb11.energy. WebSearch found HB11's own press release confirming this.
- **WebFetch on pacificfusion.com** returned the same thin marketing text as trafilatura. WebFetch explicitly noted: "No funding amounts, team member names, or specific technical specifications are provided in this page content."

### Test 2: Pacific Fusion (concept 07)

`.orig.md` claims: "$900M funding", 5 founders by name, 156 modules, 22M amps

- **WebFetch on pacificfusion.com/updates/founders-letter** returned: "More than $900 million in our Series A" with all 5 founder names. This is a standard HTML page that our extraction pipeline would handle fine.
- **156 modules** confirmed in the YES-verdict Fusion Report interview (already extracted as a replacement source).
- The `.orig.md` listed 5 specific subpage URLs — the best provenance of any NO file.

### Test 3: First Light Fusion (concept 22)

`.orig.md` claims: TBR 1.8, 333 MWe, LCOE <$50/MWh, 6.5 km/s projectile

- **WebFetch on firstlightfusion.com** returned nothing useful — pure JS SPA.
- **WebFetch on firstlightfusion.com/flare/** (white paper page) — also nothing, JS-rendered.
- **WebSearch for "First Light Fusion TBR 1.8"** found multiple independent news sources: The Engineer, NEI Magazine, IP Group, Eureka Magazine. All confirm TBR 1.8, 333 MWe, 25 kg/year tritium surplus, validated by TÜV SÜD UK.
- **WebFetch on theengineer.co.uk article** returned the full article text with all specs. Standard HTML, zero JS issues. Our `agentic-mbse extract` would capture this perfectly.
- **WebFetch on neimagazine.com article** — same, full text returned.

### Conclusion

**The data is real.** 10/10 claims verified. Haiku did not fabricate numbers.

**The data lives on standard HTML news sites** — not the JS-heavy company sites we blamed. The Engineer, NEI Magazine, GlobeNewsWire, PR Newswire, Interesting Engineering, World Nuclear News — all standard server-rendered HTML that both WebFetch and `agentic-mbse extract` handle without issues.

**The "JS problem" framing was wrong.** The primary company URLs (hb11.energy, firstlightfusion.com, etc.) ARE JS-heavy, and our trafilatura-based extraction captures little from them. But the original research agents got their data from external news sites covering those companies, not from the company sites themselves. Our source replacement extracted only the primary URL and called the result "NO — JS issue" when the real issue was single-source vs multi-source.

---

## What the Replacement Pipeline Did Differently

The source replacement project (`agentic-mbse extract <url>`) does something fundamentally different from the original research agents:

| | Original research agent | Source replacement |
|---|---|---|
| **URLs per file** | 3-8 (multi-source compilation) | 1 (single URL extraction) |
| **Content capture** | Haiku summary of each page | Verbatim text via trafilatura/Pandoc |
| **Provenance** | Domain names or vague attribution | YAML frontmatter with exact URL, timestamp, content hash |
| **Raw source preserved** | No | Yes (companion dir: raw.html/raw.pdf, metrics.json) |
| **Verifiable quotes** | No (Haiku paraphrase) | Yes (verbatim extraction) |

The replacement is better on every dimension EXCEPT breadth — it only visits one URL. The original visited many URLs but captured them through a lossy, unverifiable pipeline.

---

## Design Implications for the Autonomous Research Module

### The core principle

**Research (finding URLs) and capture (extracting content) must be separate operations using different tools.**

- **WebSearch** → find candidate URLs. Good for discovery.
- **WebFetch** → evaluate candidates ("is this page relevant to the gap?"). Good for triage. NOT for capture.
- **`agentic-mbse extract` (via `add-source`)** → capture content from confirmed-relevant URLs. Produces verbatim text with YAML frontmatter, companion dir, raw source. This is the ONLY acceptable way to create source files.

If the research agent uses WebFetch to write source file content, you get the same broken pipeline that produced the `.orig.md` files.

### What the research agent prompt must enforce

1. **Never use WebFetch output as source file content.** WebFetch is for deciding whether to extract, not for extracting.
2. **Every source file must be created by `add-source` / `agentic-mbse extract`.** This ensures YAML frontmatter, companion dir, and verbatim text.
3. **One URL per source file.** No multi-source compilations. The analysis agent synthesizes across sources at read time.
4. **Log the search → evaluate → extract chain.** For each source acquired: what query found it, what WebFetch preview showed, why it was deemed relevant to which gap.

### What WebFetch IS useful for

- **Quick relevance check:** "Does this page contain data about REBCO conductor costs?" → WebFetch can answer this in 2 seconds without a full extraction.
- **Triage before expensive extraction:** PDF extractions cost $2-50. Use WebFetch to check if a URL is worth extracting before committing.
- **Identifying the right URL:** A WebSearch result might point to a journal's landing page. WebFetch can check whether the full paper is accessible or paywalled.

### Test cases: the 21 NO `.orig.md` files

These are ideal for validating the module:
- Verified-real data (10/10 spot-check)
- Domain hints in headers (even if not exact URLs)
- The actual source URLs are on standard HTML sites our extraction handles
- 21 varied cases across startup profiles, news articles, press releases, conference pages
- Measurable success: do the extracted sources cover the claims in the `.orig.md`?

### Source quality hierarchy

The research agent needs guidance on what to prioritize:
1. Peer-reviewed papers (arXiv, journal articles) — most authoritative for physics/engineering claims
2. Government reports (OSTI, DOE, IAEA) — authoritative for program data
3. Institutional pages (university, national lab) — authoritative for facility specs
4. Press releases (company's own) — authoritative for company announcements, funding, milestones
5. News articles with direct quotes (The Engineer, WNN, ANS) — good for sourcing company claims with attribution
6. News summaries without quotes — weakest acceptable source
7. Blog posts, forums — not acceptable as sole source for quantitative claims

---

## Files Referenced

- Research prompt: `exploration/phase_1a/prompt_templates/research.md`
- Triage report: `.project/active/source-replacement/triage-report.md`
- Concept doc: `.project/concepts/autonomous-source-acquisition.md`
- Replacement report: `knowledge/concept_research/source_replacement_report.md`
- Updated plan: `.project/active/source-replacement/plan-completion.md` (Phase 6, Steps 1-3)
