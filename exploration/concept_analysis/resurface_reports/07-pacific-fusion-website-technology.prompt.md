# Source Acquisition: Re-source pacific-fusion-website-technology.orig.md

You are a research agent. Below is a legacy source file — a Haiku paraphrase
compiled from multiple URLs. Your job: find the actual URLs where this data
comes from, and extract each one as a proper individual source file using
`add-source`.

The file belongs to concept **07-maglif** (concept number **07**).

## The Legacy File

```
# Pacific Fusion - Website and Press Releases (compiled)

**Source URLs**:
- https://www.pacificfusion.com/
- https://www.pacificfusion.com/updates/founders-letter
- https://www.pacificfusion.com/updates/crada-sandia-national-laboratories
- https://www.pacificfusion.com/updates/experimental-breakthrough-by-pacific-fusion-clears-major-obstacle-to-affordable-commercial-fusion
- https://lowercarbon.com/company/pacific-fusion/

**Accessed**: 2026-03-07

## Company Overview

- Founded summer 2023 by Eric Lander, Will Regan, Keith LeChien, Carrie von Muench, and Leland Ellison
- Based in Fremont, California
- $900 million in committed funding
- Team includes people directly involved in NIF ignition experiments and Sandia Z Machine work
- CTO Dr. Keith LeChien invented the impedance-matched Marx generator (IMG)

## Technology: Pulsed Magnetic Inertial Fusion

- "Fast-rising, high-current pulses to magnetically squeeze and heat small containers of deuterium-tritium fuel"
- Fuel container rapidly squeezed by powerful magnetic field created by driving large, fast-rising electrical current across it
- Process repeated "over and over, like in a piston engine"
- Described as "a pulsed magnetic path to inertial fusion"

## Driver Technology: Impedance-Matched Marx Generators (IMGs)

- Massive battery-like capacitors dump huge amounts of electric current in 100-nanosecond bursts
- IMGs first demonstrated by LLNL in 2022
- Small modular units called "bricks" (two capacitors and a switch) assembled into shipping-container-sized modules
- Three modular components: fast electric pulser, small fusion chamber (meter-scale), tiny fuel containers (centimeter-scale)

## Self-Magnetizing Targets (Feb 2026 Breakthrough)

- Partnership with Sandia National Laboratories
- Self-magnetizing targets made of plastic and aluminum
- Targets create their own internal magnetic field to premagnetize fusion fuel
- Eliminates need for external copper coils (destroyed each shot in traditional MagLIF)
- Two versions tested: aluminum thicknesses of 50 and 200 microns
- "Small metal cylinders, about the size of a pencil eraser"
- 22 million amps of electric current through a target in just 120 nanoseconds
- Goal: also eliminate need for laser pre-heating

## CRADA with Sandia

- Focus on developing cutting-edge pulser architectures
- Advancing capabilities for high-yield fusion (100+ MJ)
- Addressing challenges of operating in high fusion yield environment

## Targets and Timeline

- Net facility gain demonstration by 2030
- First commercial fusion system in US by mid-2030s
- Electricity at 2 cents per kilowatt-hour by 2040
- Building Albuquerque Research and Manufacturing Campus

## Fuel

- **Confirmed D-T**: "deuterium-tritium fuel" explicitly stated in founders' letter

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
uv run python scripts/run_analysis.py add-source 07 "<url>"
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
3. Extract confirmed sources via `add-source 07 "<url>"`

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
`/tmp/resurface/07-pacific-fusion-website-technology.json`

Use this exact format:

```json
{
  "orig_file": "pacific-fusion-website-technology.orig.md",
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
