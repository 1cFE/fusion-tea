---
date: 2026-03-28T10:05:00-07:00
researcher: Claude
topic: "Source capture pipeline feasibility — agentic-mbse extraction, Claude web-fetch capabilities, safety risks"
tags: [research, pipeline, concept-analysis, extraction, web-fetch, safety]
status: complete
last_updated: 2026-03-28
---

# Research: Source Capture Pipeline Feasibility

**Date**: 2026-03-28
**Researcher**: Claude
**Research Type**: Architecture / Feasibility / Security

## Research Questions

1. Does agentic-mbse have a mechanism to directly save and extract a source (HTML or PDF)?
2. Can a Claude agent (headless `claude -p`) use WebFetch to actually save web content?
3. What are the safety risks of saving web pages directly, and how should they be sanitized?

## Motivation

The concept analysis pipeline has a **lossy handoff** between Phase 1a research and concept analysis. Phase 1a research agents fetch web content and save 20-40 line summaries optimized for *taxonomy column filling*. The concept analysis stage then reads these summaries for a fundamentally different purpose — *techno-economic analysis* — and misses detailed cost data, engineering parameters, and quantitative tables that were in the original sources but never captured.

The question is: can we close this gap by having the pipeline capture richer source material?

---

## Summary

- **agentic-mbse**: Handles PDF and DOCX extraction excellently (8-step quality-gated pipeline), with an arXiv HTML shortcut. **No general HTML/URL extraction capability.** Cannot fetch arbitrary web pages.
- **Claude Code's WebFetch**: Returns **Haiku's paraphrase**, not actual page content. Quotes capped at 125 chars. PDFs fail (binary). **Fundamentally unsuitable for saving citable source material.**
- **Best approach**: `curl` → local file → extraction pipeline. For HTML: `curl` + `trafilatura` (or pandoc). For PDF: `curl` + `agentic-mbse extract`. This produces actual source content.
- **Safety**: Prompt injection via saved web content is a real (OWASP #1 for LLMs) but manageable risk. A BeautifulSoup pre-pass stripping hidden elements + trafilatura article extraction + saving as markdown gives strong sanitization. The pipeline's existing human review gates are the strongest defense.

---

## Detailed Findings

### Q1: agentic-mbse Extraction Capabilities

**Source code**: `~/1cfe/agentic-mbse/src/agentic_mbse/extraction/`

#### What It Can Extract

| Input | Supported | Pipeline |
|-------|-----------|----------|
| Local PDF | Yes | 8-step quality-gated (PyMuPDF4LLM → ensemble table detection → Claude enhancement) |
| Local DOCX | Yes | Docling or Pandoc backend |
| arXiv PDF | Yes (auto-detect) | If arXiv ID found on page 1, fetches HTML from `arxiv.org/html/{id}`, converts via Pandoc |
| Arbitrary URL | **No** | No URL fetching capability |
| Local HTML | **No** | No HTML extraction path |
| Web page | **No** | Not designed for web scraping |

#### arXiv Shortcut Detail

The one URL-aware path (`pandoc_convert.py`):
- Regex detects `arXiv:\d{4}\.\d{4,5}(v\d+)?` on PDF page 1
- Checks if `https://arxiv.org/html/{arxiv_id}` exists (many arXiv papers now have HTML)
- If available: downloads HTML, strips `<figure>` tags, converts via Pandoc
- Override available: `--html-path <url_or_path>` forces a specific HTML source

#### What It Can't Do

- No general URL fetching
- No HTML content extraction
- No batch URL processing
- No source registry or manifest management (SOURCE_INDEX.md is a separate MBSE concern)

#### Key CLI Flags (PDF)

```bash
uv run agentic-mbse extract <pdf> [--budget USD] [--model {opus,sonnet,haiku}]
    [--output DIR] [--force] [--index] [--summarize] [--no-tables] [--docling]
```

Default: $2 Claude budget, sonnet model. Set `--budget 0` for Claude-free extraction.

---

### Q2: Claude Agent Web Capabilities

#### WebFetch — The Critical Misunderstanding

**What most people assume**: WebFetch downloads a web page and returns its content to the agent.

**What actually happens in Claude Code** (`claude -p`):

```
Agent calls WebFetch(url, prompt)
  → Claude Code fetches the URL
  → Converts HTML to markdown (Turndown library)
  → Truncates to ~100KB
  → Passes to Haiku 3.5 with the prompt
  → Returns ONLY Haiku's summary/answer (not the page content)
```

**Implications for source capture:**
- The agent never sees the actual page content
- Verbatim quotes are capped at **125 characters**
- Numerical tables, parameter lists, and structured data are **lossy**
- The agent cannot save the original content because it never receives it
- Saving WebFetch output produces a secondary source (Haiku's interpretation), not a primary source

**PDF handling**: Binary PDFs fail completely. WebFetch only processes HTML.

**ArXiv**: Abstract pages (HTML) work. PDF links fail. Content is still Haiku-summarized.

#### WebSearch — Even More Limited

Returns **only URLs and titles** from search results. No snippets, no content. Must be combined with WebFetch (which then returns Haiku summaries).

#### The API's Web Fetch Server Tool (Different!)

The Claude API (not Claude Code) has a `web_fetch_20260209` server-side tool that returns **full content** including PDF support. This is NOT the same tool available in `claude -p`. Not relevant to our pipeline.

#### What the Phase 1a Research Agent Actually Did

The Phase 1a `run_concept.py` invokes `claude -p --dangerously-skip-permissions`. The research prompt says "Search the web" and "Save important sources." In practice:

1. Agent uses WebSearch → gets URLs
2. Agent uses WebFetch(url, "Extract all technical content...") → gets Haiku summary
3. Agent uses Write tool → saves the Haiku summary as `sources/filename.md`

**This is why the source files are 20-40 line summaries — they are Haiku's paraphrases, not the original content.** The agent literally cannot get the original content through WebFetch.

---

### Q3: Alternative Approaches That Actually Work

#### Option A: curl/wget + pandoc (HTML pages)

```bash
# Fetch and convert in one step
curl -sL 'https://example.com/paper.html' | pandoc -f html -t markdown -o output.md
```

Available on this system: `curl 8.5.0`, `wget`, `pandoc 3.1.3`.

**Pros**: Gets actual content, preserves tables, no quote limits.
**Cons**: No JS rendering, no boilerplate removal, raw HTML artifacts may remain.

#### Option B: curl + trafilatura (HTML pages, better quality)

```bash
uv add trafilatura  # One-time setup
curl -sL 'https://example.com/paper.html' | uv run python -c "
import sys; import trafilatura
print(trafilatura.extract(sys.stdin.read(), output_format='markdown', include_tables=True))
"
```

**Pros**: Article extraction (removes nav, ads, boilerplate), metadata extraction, best benchmarked F1 (0.883).
**Cons**: Requires `uv add trafilatura`.

#### Option C: curl + agentic-mbse extract (PDFs)

```bash
curl -sL 'https://arxiv.org/pdf/2411.06644' -o /tmp/paper.pdf
uv run agentic-mbse extract /tmp/paper.pdf --output /path/to/sources/
```

**Pros**: Full 8-step extraction pipeline, excellent table detection, proven in this project.
**Cons**: Two-step process (download then extract), PDF only.

#### Option D: Docling MCP Server (available in this session)

The Docling MCP accepts URLs directly:
```
mcp__docling__convert_document_into_docling_document(source="https://example.com/paper.pdf")
→ document_key
mcp__docling__export_docling_document_to_markdown(document_key=key)
→ markdown content
```

**Pros**: Direct URL support, excellent PDF/table handling.
**Cons**: MCP server must be running, designed for document conversion not web scraping.

#### Recommended Pipeline for Automated Source Capture

```
For HTML (web pages, company sites, Wikipedia):
  curl -sL <url> → BeautifulSoup sanitizer → trafilatura → save as .md

For PDF (papers, technical reports):
  curl -sL <url> -o /tmp/paper.pdf → uv run agentic-mbse extract → save .md

For arXiv specifically:
  uv run agentic-mbse extract <pdf> (auto-detects arXiv, fetches HTML if available)
```

---

### Q4: Safety Risks and Sanitization

Full analysis in `.project/research/20260328-web-content-sanitization-for-llm-pipelines.md`.

#### Risk Assessment

| Source Type | Prompt Injection Risk | Relevance to This Project |
|-------------|----------------------|---------------------------|
| Journal articles / preprints | Very low | Primary source type |
| arXiv papers | Very low | Frequent source |
| Company websites | Low-medium | Common for fusion startups |
| Wikipedia | Low-medium | Used for background |
| News articles | Low-medium | Occasionally used |
| Forums / comments | Medium-high | Not typically used |
| Arbitrary search results | Medium-high | Phase 1a searches broadly |

#### The Real Threat: CSS-Hidden Prompt Injection

Palo Alto Unit 42 documented **22 concealment techniques** for embedding hidden LLM instructions in web pages. The most relevant:

- `display: none` / `visibility: hidden` — CSS-suppressed text
- `font-size: 0px` — invisible text
- `opacity: 0` — transparent text
- Off-screen positioning (`left: -9999px`)
- Zero-width Unicode characters

**Key finding**: No standard Python content extraction tool strips CSS-hidden text. Not trafilatura, not readability, not html2text. They all extract text content regardless of CSS visibility.

#### Recommended Three-Layer Sanitization

```python
# Layer 1: BeautifulSoup pre-pass (strips hidden elements)
def sanitize_html(html: str) -> str:
    """Strip CSS-hidden elements, scripts, zero-width chars."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove script, style, noscript, iframe
    for tag in soup(["script", "style", "noscript", "iframe"]):
        tag.decompose()

    # Remove elements with hiding CSS
    HIDDEN_PATTERNS = [
        {"style": re.compile(r"display\s*:\s*none", re.I)},
        {"style": re.compile(r"visibility\s*:\s*hidden", re.I)},
        {"style": re.compile(r"opacity\s*:\s*0[^.]", re.I)},
        {"style": re.compile(r"font-size\s*:\s*0", re.I)},
        {"style": re.compile(r"position\s*:\s*absolute.*left\s*:\s*-\d{4,}", re.I)},
        {"aria-hidden": "true"},
    ]
    for pattern in HIDDEN_PATTERNS:
        for el in soup.find_all(attrs=pattern):
            el.decompose()

    # Strip zero-width Unicode characters
    text = str(soup)
    text = re.sub(r"[\u200b\u200c\u200d\u2060\ufeff]", "", text)
    return text

# Layer 2: trafilatura article extraction
content = trafilatura.extract(sanitized_html, output_format="markdown",
                               include_tables=True)

# Layer 3: Save as markdown with metadata frontmatter
```

#### Why This Is Sufficient

1. **Source type filtering**: Our pipeline fetches academic papers, company pages, and Wikipedia — not arbitrary user-generated content
2. **Sanitization removes the primary attack vectors**: CSS-hidden text, scripts, zero-width chars
3. **Markdown conversion strips remaining HTML**: No JS execution, no iframes, no tracking
4. **Human review gates**: The pipeline's review stage (Stage 4) catches anything anomalous
5. **Anti-hallucination rules**: The analysis prompt already tells the agent to only cite provided sources

---

## Architecture Insights

### The Fundamental Problem

The Phase 1a → concept analysis handoff is lossy because **WebFetch's Haiku intermediary discards the actual content**. The Phase 1a agent *thought* it was saving source material, but it was actually saving Haiku's paraphrases. This is an architectural limitation of Claude Code's WebFetch, not a bug in our pipeline.

### Two Ways to Fix It

**Option 1: Enrich sources at capture time (Phase 1a redesign)**

Modify the Phase 1a research agent to use `curl` + extraction pipeline instead of WebFetch. The agent would:
1. `WebSearch` to find URLs (still useful for discovery)
2. `Bash(curl ...)` to download the actual content
3. Sanitize + extract → save full markdown
4. Read the saved markdown for synthesis

This produces richer source files (~100-500 lines of actual content vs. 20-40 lines of Haiku summary).

**Tradeoff**: More complex agent prompt, larger source files consume more context, but the analysis stage gets dramatically better inputs.

**Option 2: Enrich sources at analysis time (on-demand fetch)**

Add a pre-analysis stage that:
1. Reads existing source files
2. Extracts original URLs from source headers (`**Source**: https://...`)
3. Re-fetches and extracts full content
4. Replaces or supplements the summary with actual content

This could be the `add-source` command from the pipeline upgrades research, automated to re-fetch all existing sources.

**Tradeoff**: Duplicates work, URLs may be stale, but doesn't require Phase 1a redesign.

### Recommended Approach

**Option 1 is better for new concepts, Option 2 is better for already-researched concepts.**

For the ~30 concepts not yet analyzed: modify the Phase 1a research prompt to use curl-based capture.

For the ~6-8 concepts already analyzed: use an `enrich-sources` command that re-fetches from recorded URLs.

---

## Feasibility Assessment

| Capability | Current State | Feasibility to Add | Dependencies |
|-----------|--------------|-------------------|-------------|
| HTML → markdown extraction | Not available | Easy — `uv add trafilatura` or use pandoc | `trafilatura` or system `pandoc` |
| PDF → markdown extraction | Available via agentic-mbse | Already works | None |
| URL fetch in headless agent | Only via Haiku summary (WebFetch) | Easy — use `curl` via Bash tool | `--dangerously-skip-permissions` already set |
| Sanitization pre-pass | Not implemented | Easy — ~30 lines of BeautifulSoup | `beautifulsoup4` (likely already installed) |
| Automated source enrichment | Not implemented | Medium — new pipeline stage | Integration with Phase 1a source paths |

**Bottom line**: The tools exist. The gap is that the pipeline uses WebFetch (lossy) instead of curl (lossless). Switching is straightforward — the hard part is deciding where in the pipeline to do it and designing the prompt changes.

---

## Recommendations

1. **Add `trafilatura` to the project**: `uv add trafilatura beautifulsoup4` — these are the two dependencies needed for safe HTML extraction.

2. **Build a `capture-source` utility function** that encapsulates: `curl` → sanitize → extract → save with metadata frontmatter (URL, access date, SHA-256 hash). This is reusable by both Phase 1a agents and the concept analysis pipeline's `add-source` command.

3. **For immediate impact on in-progress analyses**: Build an `enrich-sources` command that reads existing source files, extracts URLs from headers, re-fetches, and produces enriched versions. Run this before analyzing concepts with thin sources.

4. **For new Phase 1a research**: Update the research prompt to instruct the agent to use `curl` via Bash instead of WebFetch for substantive sources. Keep WebFetch for quick checks where a summary is sufficient.

5. **Don't over-engineer sanitization**: The three-layer approach (BeautifulSoup + trafilatura + markdown) is sufficient for academic/research content. Skip building a general-purpose web scraping framework.

---

## Open Questions

1. **Context budget**: Full source extractions will be much larger (100-500 lines vs. 20-40). Does the analysis agent's context window have room? The analysis prompt already loads dossier + all sources + exemplars + approved pool. Need to measure.

2. **Trafilatura vs. pandoc**: For our source types (mostly academic/technical), which produces better markdown? Should test with 3-5 representative pages.

3. **Source format migration**: Should enriched sources replace the originals (same filename) or be stored alongside (e.g., `source.md` + `source.full.md`)? Replacing is cleaner but loses the provenance of what the original agent saw.

4. **Rate limiting and politeness**: If we automate re-fetching of ~100+ URLs, should we add delays to avoid triggering rate limits? Most sources are academic (arXiv, university pages) which are generally permissive.

---

## Code References

- `exploration/concept_analysis/scripts/run_analysis.py:469-497` — `invoke_claude()` (headless call, uses `--dangerously-skip-permissions`)
- `exploration/concept_analysis/scripts/run_analysis.py:543-558` — `find_sources()` (discovers `iter-*/sources/*.md`)
- `exploration/phase_1a/prompt_templates/research.md:20-26` — Phase 1a research strategy (instructs WebSearch + save)
- `~/1cfe/agentic-mbse/src/agentic_mbse/extraction/pipeline.py` — 8-step PDF extraction pipeline
- `~/1cfe/agentic-mbse/src/agentic_mbse/extraction/pandoc_convert.py` — arXiv HTML detection + Pandoc conversion
- `.project/research/20260328-web-content-sanitization-for-llm-pipelines.md` — detailed safety analysis (companion document)
- `.project/research/20260328-pipeline-upgrade-feasibility.md` — prior research on pipeline upgrades (Q5 covers manual source addition)
