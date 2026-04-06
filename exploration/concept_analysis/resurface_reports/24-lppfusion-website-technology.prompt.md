# Source Acquisition: Re-source lppfusion-website-technology.orig.md

You are a research agent. Below is a legacy source file — a Haiku paraphrase
compiled from multiple URLs. Your job: find the actual URLs where this data
comes from, and extract each one as a proper individual source file using
`add-source`.

The file belongs to concept **24-dense-plasma-focus** (concept number **24**).

## The Legacy File

```
# LPPFusion Website — Technology Pages (Retrieved 2026-03-08)

## Sources
- https://www.lppfusion.com/technology/focus-fusion-energy/
- https://www.lppfusion.com/technology/focus-fusion-energy/dpf-device/
- https://www.lppfusion.com/investing-in-lppfusion/executive-summary/
- https://www.lppfusion.com/investing-in-lppfusion/our-plan-to-net-energy/
- https://www.lppfusion.com/investing-in-lppfusion/our-business-development-plan/focus-fusion-timelines-and-milestones/

## Device: Dense Plasma Focus (DPF)

- Two concentric cylindrical metal electrodes
- Outer electrode: ~6-7 inches diameter, ~1 foot long
- Inner electrode (anode): 2.8 cm radius (FF-2B)
- Maximum current: 2.7 MA (FF-2B)
- Pulse of electricity from capacitor bank discharged across electrodes
- Gas ionized → current sheath forms → runs down electrodes → filaments pinch at end of inner electrode → forms plasmoid

## Plasmoid Properties

- Duration: ~10 ns (billionths of a second)
- Size: "a few thousandths of an inch across"
- Temperature: billions of degrees C (ion energies >100 keV, record >200 keV)
- Density: "close to solid density" — up to 10²¹ cm⁻³ demonstrated in DPF devices
- Self-organized current filaments form the pinch

## Fuel

- Primary: p-B11 (hydrogen-boron)
- Experimental fuel for pB11 tests: isotopically pure decaborane (B¹⁰H₁₄)
- Currently experimenting with deuterium (for development)
- pB11 reaction produces only charged particles (3 alpha particles), no neutrons

## Energy Conversion (Two Channels)

1. **Ion beam** (~2/3 of plasmoid energy): Directed into a decelerator — "particle accelerator in reverse" — decelerates charged particles to generate electricity directly
2. **X-rays** (remainder of energy): Converted to electricity via photoelectric effect (like solar panels). LPPFusion has patented x-ray conversion technology.

Called "high-tech step-down transformer" in executive summary.

## Power Plant Targets

- 5 MW net electric per generator
- ~25 kJ net energy per pulse
- Repetition rate: up to ~200 Hz ("a few hundred times a second")
- Mass: ~3 tons
- Volume: ~30 m³ (garage-sized, ~20 m² footprint)
- Construction cost: <$1 million per unit
- LCOE claim: <0.2 cents/kWh

## Development Phases

### Phase 1 (Current — FF-2B, laboratory)
- Demonstrate net energy with pB11 fuel
- Current yield: ~0.26 J per shot (record, June 2024)
- Target: 30,000 J (30 kJ) per shot
- Key milestones: low impurity → 10 J yield → 100× density increase → pB11 fuel → net energy

### Phase 2 (Future — ~$100M, 3-4 years)
- Develop repetitively pulsed generator
- Develop energy conversion devices (ion beam + x-ray)
- Perfect cooling and electrical control
- Target: 5 MW net electricity

## Key Achievements (as of 2024-2025)
- Record confined ion energy: >200 keV (2016, ten-shot mean 125 keV)
- Record plasma purity: <0.2% impurities entering pinch (with Be electrodes)
- Beryllium electrodes replacing tungsten to reduce impurities (Be z=4 vs W z=74)
- Record nτT product: 3.4 × 10²⁰ keV·s/m³

## Quantum Magnetic Field Effect (QMFE)
- Lerner's theoretical contribution (2003)
- In strong magnetic fields, electron orbits are quantized → reduces ion-electron energy transfer
- Makes ions much hotter than electrons → enhances fusion power relative to bremsstrahlung
- Simulations show fusion power can exceed bremsstrahlung by factor of ~2
- Critical for p-B11 viability (bremsstrahlung is the main energy loss channel for p-B11)

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
uv run python scripts/run_analysis.py add-source 24 "<url>"
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
3. Extract confirmed sources via `add-source 24 "<url>"`

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
`/tmp/resurface/24-lppfusion-website-technology.json`

Use this exact format:

```json
{
  "orig_file": "lppfusion-website-technology.orig.md",
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
