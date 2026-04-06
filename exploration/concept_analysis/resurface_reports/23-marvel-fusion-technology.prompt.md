# Source Acquisition: Re-source marvel-fusion-technology.orig.md

You are a research agent. Below is a legacy source file — a Haiku paraphrase
compiled from multiple URLs. Your job: find the actual URLs where this data
comes from, and extract each one as a proper individual source file using
`add-source`.

The file belongs to concept **23-laser-icf-nanostructured-target** (concept number **23**).

## The Legacy File

```
# Marvel Fusion - Technology Overview

**Sources**:
- https://www.marvelfusion.com/ (company website)
- https://binding.energy/ultrashort-pulse-laser-fusion/ (technical overview)
- https://optics.org/news/15/10/4 (Series B funding, Oct 2024)
- https://optics.org/news/16/4/4 (€50M extension, Apr 2025)
- https://patents.google.com/patent/US20230073280A1/en (nanostructured target patent)

**Retrieved**: 2026-03-07

## Core Approach

Marvel Fusion pursues non-thermal laser-driven fusion using ultrashort-pulse (femtosecond) lasers on nanostructured solid targets containing p-B11 fuel. The approach differs from classical ICF (NIF-style compression) by using direct-drive ignition in solid-state fuel, avoiding energy losses from compression.

## Laser Technology

- **Type**: Diode-pumped solid-state laser (DPSSL)
- **Pulse duration**: Sub-100 femtoseconds (fs)
- **Power class**: Petawatt-class (ALEPH laser at CSU to be upgraded to 2 PW)
- **Repetition rate**: 10 Hz
- **ATLAS Facility** (CSU Fort Collins): At least 3 laser systems, combined ~7 PW peak power, 10 Hz, focal spot ~100 µm. Coming online mid-2026.
- **Initial demo**: Two 100 J lasers; future scaling to kilojoule-class sources at 10 Hz after end of decade
- **Commercial plant**: Expected to need ~500 laser systems; demo plant 10-100 systems

## Target Design

- **Material**: Silicon nanostructures (nanorods/nanowire arrays)
- **Feature size**: 50-80 nm per feature
- **Manufacturing**: Standard semiconductor lithography (can use equipment up to a decade old)
- **Production**: ~5,000 targets per standard 300 mm wafer
- **Patent (US20230073280A1)**: Target comprises aligned nano-rods of first fuel material with interspaces filled with second material. Non-frozen (room temperature). Non-thermal triggering of fusion reactions.

## Fuel

- **Primary**: p-B11 (proton-boron-11)
- **Advantage**: Aneutronic — produces alpha particles (charged He nuclei), no problematic radioactivity
- **No cryogenics required** — room temperature target handling

## Energy Conversion

- **Approach**: Hybrid — combining magnetic, electrostatic, and steam power generation
- **Target efficiency**: Up to 70%
- **Mechanism**: Alpha particle kinetic energy captured via induction in magnetic and electrostatic fields (like a dynamo), with steam cycle for residual thermal energy
- **Advantage over Carnot**: Significantly lower losses than classical Carnot cycle

## Key Partners

Trumpf, Thales, Siemens, Fraunhofer, CEA

## Timeline

- Prototype facility: ~2032
- Commercial fusion power plant: ~2036

## Funding

- Series B: €113M total (including €50M extension in 2025)
- Total raised: ~€165M+
- ATLAS Facility: $150M public-private partnership with DOE/CSU

## Team

80+ physicists and engineers

## Secondary Applications

Medical isotope production, neutron imaging, high-energy physics research — potential early market pathways.

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
uv run python scripts/run_analysis.py add-source 23 "<url>"
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
3. Extract confirmed sources via `add-source 23 "<url>"`

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
`/tmp/resurface/23-marvel-fusion-technology.json`

Use this exact format:

```json
{
  "orig_file": "marvel-fusion-technology.orig.md",
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
