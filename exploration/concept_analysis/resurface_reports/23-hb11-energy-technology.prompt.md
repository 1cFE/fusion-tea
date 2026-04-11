# Source Acquisition: Re-source hb11-energy-technology.orig.md

You are a research agent. Below is a legacy source file — a Haiku paraphrase
compiled from multiple URLs. Your job: find the actual URLs where this data
comes from, and extract each one as a proper individual source file using
`add-source`.

The file belongs to concept **23-laser-icf-nanostructured-target** (concept number **23**).

## The Legacy File

```
# HB11 Energy - Technology Overview

**Sources**:
- https://hb11.energy/ (company website)
- https://hb11.energy/our-technology/ (technology page)
- https://newatlas.com/energy/hb11-hydrogen-boron-fusion-clean-energy/ (New Atlas, 2020)
- https://newatlas.com/energy/hb11-laser-fusion-demonstration/ (experimental results)
- https://link.springer.com/article/10.1007/s10894-023-00349-9 (Journal of Fusion Energy, 2023)
- https://arxiv.org/abs/1603.02579 (Hora et al., avalanche boron fusion)

**Retrieved**: 2026-03-07

## Core Approach

HB11 Energy uses a two-laser system for laser-driven proton-boron (p-B11) fusion via "Proton Fast Ignition." Founded by Prof. Heinrich Hora's theoretical work on non-thermal block ignition and avalanche fusion reactions.

## Two-Laser System

1. **Laser 1 (nanosecond)**: Creates a sub-kilotesla to kilotesla magnetic field inside a coil-like structure, lasting several nanoseconds. This magnetically confines the plasma and alpha particles.
2. **Laser 2 (picosecond)**: ~10 PW, ~1 ps pulse. Creates conditions for ultrahigh acceleration of plasma blocks required for non-thermal ignition. Triggers the "avalanche" fusion chain reaction via proton fast ignition.

## Avalanche Reaction Mechanism

Alpha particles from initial p-B11 reactions collide with protons, which then collide with more B11, generating secondary fusion reactions. This multiplication of reactions is the "avalanche" process, claimed to produce energy gains nine orders of magnitude above classical values.

## Target/Fuel Design

- **Fuel**: Solid hydrogen-boron cylinder
- **Dimensions**: 1 cm length, 1 mm radius
- **Pellet size**: Described as "the size of a pea" (for fuel pellet form)
- **Coaxially located** within magnetic field coils

## Magnetic Field

- **Strength**: ~10 kilotesla (laser-generated, not external magnets)
- **Purpose**: Confine plasma and alpha particles during reaction
- **Alpha gyroradius**: ~43 µm in 10 kT field (small compared to 1 mm cylinder radius)
- **Duration**: ~nanoseconds

## Energy Conversion — CONFLICTING INFORMATION

**Company website** (current): "conventional steam cycle" for electricity generation, targeting "1 GW baseload power"

**Scientific literature and earlier descriptions**: Direct conversion of alpha particle charge. "Naked helium atoms...positively charged. We just have to collect that charge." Direct conversion efficiency ~80%. Alternatively, combined MHD + Rankine could achieve ~64%.

**2023 J. Fusion Energy paper**: Discusses both options — direct electrodynamic conversion (~50%) and thermal cycle (~35-40%). Also mentions initial conversion of ion energy to photon energy at ~45% efficiency.

**Assessment**: The company appears to have pivoted or be presenting multiple options. Original Hora concept emphasized direct conversion; recent website emphasizes steam cycle.

## Repetition Rate

- **Target**: 1 Hz (pulsed once per second)

## Energy Per Shot

- **Estimated**: ~300 kWh per shot from 15 mg HB11 fuel (2.9 MeV per alpha particle, 3 alphas per reaction)

## Reactor Geometry

- **Spherical reactor**: At least 1 m radius sphere to capture alpha particle energy
- **Fuel positioned** in cylindrical axis of magnetic coil

## Experimental Results

- "World-first 'material' number of fusion reactions by a private company"
- 10x more fusion reactions than expected from earlier experiments
- Currently four orders of magnitude from net energy gain
- Initial experiments showed reaction rates "a billion times higher than anticipated"

## Funding

~$22M total raised (significantly less than Marvel Fusion)

## Location

Australia-based

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
`/tmp/resurface/23-hb11-energy-technology.json`

Use this exact format:

```json
{
  "orig_file": "hb11-energy-technology.orig.md",
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
