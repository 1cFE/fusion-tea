# Source Acquisition: Re-source first-light-fusion-technology.orig.md

You are a research agent. Below is a legacy source file — a Haiku paraphrase
compiled from multiple URLs. Your job: find the actual URLs where this data
comes from, and extract each one as a proper individual source file using
`add-source`.

The file belongs to concept **22-projectile-icf** (concept number **22**).

## The Legacy File

```
# First Light Fusion — Technology Overview

**Sources**: Multiple pages compiled from firstlightfusion.com, newatlas.com, ipgroupplc.com, neimagazine.com, nextbigfuture.com, interestingengineering.com
**Retrieved**: 2026-03-07

## Company Overview

First Light Fusion, founded in 2011 as an Oxford University spinoff, originally pursued projectile-based inertial confinement fusion. In September 2025, they pivoted to FLARE (Fusion via Low-power Assembly and Rapid Excitation), a pulsed-power-driven liner implosion approach.

## Original Projectile Approach (2011–2025)

### Electromagnetic Launcher
- Machine 3: Electromagnetic launch pulsed power machine, launches projectiles at hypervelocity
- Big Friendly Gun (BFG): Two-stage hyper-velocity gas gun (UK's biggest), used for target testing
- Projectile velocity achieved: 6.5 km/s (23,400 km/h)
- Machine 4 was planned (60 km/s projectile, 100 MJ stored energy) but cancelled in Feb 2025

### Target Design
- Cubic form, ~1 cm sides
- Multiple cavities create interacting shockwaves that amplify pressure
- Fuel accelerated to >70 km/s during implosion through proprietary "amplifier" technology
- Fuel compressed to 10 terapascals (100 million atmospheres)
- Fuel volume reduced from several millimeters to under 100 microns

### 2022 Fusion Achievement
- April 2022: First Light confirmed fusion using projectile approach
- Independently validated by UK Atomic Energy Authority (UKAEA)
- World first for projectile-driven fusion

## FLARE Approach (September 2025–present)

### Core Technology
- Uses modular low-voltage pulsed power devices
- Delivers electric currents into hollow metal cylinders (imploding liners)
- Liners implode under magnetic pressure, compressing D-T fuel
- Adapts First Light's proven "amplifier technology" to cylindrical implosions

### Key Innovation: Decoupled Compression and Ignition
- Unlike conventional IFE which compresses and heats simultaneously
- FLARE first compresses fuel in a controlled manner
- Then separately ignites the compressed fuel via "auxiliary source such as a short-pulse laser or pulsed power system"
- This is a form of fast ignition

### Performance Targets
- Gain: up to 1,000x (minimum 200x for commercial viability)
- Current world record: 4x at NIF

## Power Plant Design

### Reactor Chamber
- Liquid lithium pool reactor, dynamically structured with inert gas
- 1-meter-thick curtains of liquid lithium metal flowing within the chamber
- Lithium absorbs neutrons, breeds tritium, captures heat, and protects reactor walls
- Neutrons do not reach vessel wall → lifetime-of-plant vessel

### Tritium Breeding
- TBR of 1.8 (highest announced by any fusion concept)
- At 333 MWe design point: net tritium surplus of 25 kg annually
- Tritium self-sufficiency in as little as one week

### Energy Conversion
- Liquid lithium → heat exchanger → water/steam → turbine → electricity
- Conventional steam Rankine cycle ("150-year-old steam turbine technology")
- "After the lithium heat exchanger, the plant is identical to many other already working facilities"

### Plant Specifications (various stated targets)
- ~150 MWe pilot plant, <$1B, 2030s
- ~333 MWe design point (referenced in TBR analysis)
- ~400 MW capacity (referenced in FLARE announcement)
- ~500 MWe commercial plant, <$5B
- LCOE target: under $50/MWh

### Repetition Rate
- Original projectile concept: once every 30 seconds (0.033 Hz) for 150 MW plant
- Alternative mention: once every 10 seconds for 500 MW plant
- Another reference: once every 90 seconds
- FLARE: "lower pulse rates enabled by high gain" (specific rate not disclosed)

### Cost
- FLARE demonstrator: $100–200M (1/20th of NIF)
- FLARE driver cost per joule: $2 (vs $6–13 for alternatives)
- Energy delivery system: 1/10th cost of previous fast ignition schemes

## Strategic Pivot (February 2025)
- Cancelled Machine 4 development
- No longer plans to build own power plant
- Will partner with other IFE companies, offering amplifier technology
- New CEO: Mark Thomas (former Reaction Engines)

## Then FLARE (September 2025)
- Published FLARE white paper
- Resumed own power plant development path via FLARE approach

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
uv run python scripts/run_analysis.py add-source 22 "<url>"
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
3. Extract confirmed sources via `add-source 22 "<url>"`

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
`/tmp/resurface/22-first-light-fusion-technology.json`

Use this exact format:

```json
{
  "orig_file": "first-light-fusion-technology.orig.md",
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
