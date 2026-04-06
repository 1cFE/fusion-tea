# Source Acquisition: Re-source type-one-energy-infinity-two-design.orig.md

You are a research agent. Below is a legacy source file — a Haiku paraphrase
compiled from multiple URLs. Your job: find the actual URLs where this data
comes from, and extract each one as a proper individual source file using
`add-source`.

The file belongs to concept **20-modular-hts-stellarator** (concept number **20**).

## The Legacy File

```
# Type One Energy — Infinity Two Design Basis

## Source
- Company website: https://typeoneenergy.com/our-technology/
- Design announcement: https://typeoneenergy.com/type-one-energy-issues-first-realistic-unified-fusion-power-plant-design-basis/
- ANS Nuclear Newswire: https://www.ans.org/news/2025-04-01/article-6903/
- Modern Sciences summary: https://modernsciences.org/type-one-energy-fusion-pilot-plant-design-april-2025/
- Journal of Plasma Physics special issue: https://www.cambridge.org/core/journals/journal-of-plasma-physics/collections/physics-basis-of-the-infinity-two-fusion-power-plant

## Key Specifications — Infinity Two Fusion Pilot Plant

- **Configuration**: 4-field-period, quasi-isodynamic (QI) stellarator, maximum-J approach
- **Aspect ratio**: A = 10
- **Volume-averaged magnetic field**: <B> = 9 T
- **Fusion power**: 800 MW
- **Net electric power**: ~350 MWe
- **Fusion gain**: Q = 40
- **Fuel**: Deuterium-Tritium (D-T)
- **Plasma state**: Burning plasma
- **Plasma density**: n_e ≈ 2×10²⁰ m⁻³
- **Heating**: ECRH (electron cyclotron resonance heating) + pellet injection for fueling
  - "The only envisioned external sources required for Infinity Two operation are pellet injection and electron cyclotron resonance heating (ECRH)"
- **Blanket**: Helium Cooled Pebble Bed (HCPB) — gas-cooled solid breeder
  - TBR = 1.30 (sufficient margin at low engineering fidelity)
  - Tritium inventory: ~675 grams operational
  - Required TBR for self-sufficiency: < 1.05
  - FLiBe considered as alternative where "shielding efficiency is a primary consideration"
- **Energy conversion**: Rankine cycle with reheat (steam)
  - Thermal efficiency > 30%
- **Divertor**: Island divertors for helium ash exhaust
- **Magnets**: Modular HTS (REBCO) — "over 200x current carrying capacity of copper"
- **Operation**: Steady-state, continuous
  - 2-year operating cycle, 30-day planned maintenance outages

## Infinity One (Prototype)
- Located at TVA's Bull Run site near Oak Ridge, Tennessee
- Target completion: early 2029
- Goals: demonstrate HTS magnet system, metallic first wall plasma performance, reduced turbulence, exhaust efficiency

## Development Heritage
- Built on HSX (U. Wisconsin-Madison) and W7-X (IPP Greifswald) experience
- Co-founders involved in both machines
- Used DOE Frontier exascale computer for optimization (70,000+ simulations)

## Published Physics Basis
Six peer-reviewed papers in Journal of Plasma Physics (2025), including:
- Comprehensive unified baseline physics design (Hegna et al.)
- Baseline plasma physics design
- Core plasma performance predictions
- Breeder blanket and tritium fuel cycle feasibility

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
uv run python scripts/run_analysis.py add-source 20 "<url>"
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
3. Extract confirmed sources via `add-source 20 "<url>"`

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
`/tmp/resurface/20-type-one-energy-infinity-two-design.json`

Use this exact format:

```json
{
  "orig_file": "type-one-energy-infinity-two-design.orig.md",
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
