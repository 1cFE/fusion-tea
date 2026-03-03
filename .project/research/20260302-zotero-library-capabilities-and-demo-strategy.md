---
date: 2026-03-02T14:00:00-05:00
researcher: Claude
topic: "Zotero library inspection capabilities and demo ingestion strategy"
tags: [research, zotero, demo, ingestion, strategy]
status: complete
last_updated: 2026-03-02
---

# Research: Zotero Library Inspection Capabilities & Demo Ingestion Strategy

**Date**: 2026-03-02
**Researcher**: Claude
**Research Type**: Integration / Strategy

## Research Questions

1. What data is visible about PDFs in Zotero before downloading and ingesting?
2. Can Claude find PDFs about a specific fusion concept from the library?
3. What's the strategy for the next demo work items (source ingestion)?

## Summary

- **166 top-level items** in the Zotero group library, **130 have PDFs**, **6 already extracted**
- **Rich metadata is available before download**: title, abstract, authors, date, tags, item type, DOI — all via API without touching PDFs
- **No collections** are used — items are organized only by tags (100+ unique tags)
- **pyzotero supports keyword search** (`q=` parameter), tag filtering (AND/OR/NOT), and item type filtering — all combinable
- **Several fusion concepts have multi-paper clusters** suitable for a focused demo ingestion

## Detailed Findings

### What's Visible Without Downloading

The pyzotero API returns full bibliographic metadata for every item without downloading any files:

| Field | Coverage | Notes |
|-------|----------|-------|
| `title` | ~98% (163/166) | 3 items have empty titles |
| `abstractNote` | ~70% (116/166) | Reports/webpages less likely to have abstracts |
| `creators` | ~90% | Author lists with first/last names |
| `date` | ~85% | Various formats (ISO, month/year, text) |
| `tags` | ~45% (75/166) | User-assigned and auto-imported |
| `itemType` | 100% | journalArticle, report, preprint, thesis, etc. |
| `DOI` | varies | Present for published articles |
| `collections` | 0% | **No collections are configured** in this library |

### Search and Filtering Capabilities

pyzotero supports:
- **Title/keyword search**: `zot.top(q="tokamak cost")` — substring match on title, creator, year
- **Full-text search**: `zot.top(q="LCOE", qmode="everything")` — searches PDF content (if indexed by Zotero)
- **Tag filtering**: `zot.top(tag="fusion")`, `zot.top(tag="fusion || economics")` (OR), `zot.top(tag="-extracted")` (NOT)
- **Item type filtering**: `zot.items(itemType="report")`, `zot.items(itemType="-attachment")` (exclude)
- **Combined**: All filters can be combined in a single call

### Current Library Composition

**By item type** (166 items):
- journalArticle: ~90
- report: ~20
- preprint: ~20
- thesis: 3
- webpage: ~10
- attachment (standalone): ~10
- conferencePaper: 4
- other (patent, blogPost, document, presentation, bookSection): ~9

**By tag clusters** (rough topic grouping from the 100+ tags):

| Topic Cluster | Relevant Tags | Approx Items |
|---------------|---------------|--------------|
| Fusion Economics/Costs | LCOE, fusion economics, Costs, Commercialization, Technoeconomics, NPV, Cost estimating | ~25 |
| Tokamak | Tokamak power plant, spherical tokamak, ARIES-RS, compact fusion reactor | ~15 |
| Stellarator | Stellarator | ~5 |
| Inertial Fusion | HeavyIonFusion, inertial fusion, Pacific Fusion, VASTAR Fusion | ~8 |
| Proton-Boron (p-B11) | HB11, Hydrogen boron fusion, Proton fusion, Aneutronic fusion | ~8 |
| Alternative/Exotic | Z-pinch, Magnetically confined plasmas | ~5 |
| AI/ML for Fusion | machine learning, Computer Science - AI, Digital twin | ~10 |
| Policy/Market | deployment, fusion investments, Energy markets, funding | ~10 |

### Concept Clusters with Multiple Papers

These are the concepts with enough papers to tell a coherent story for the demo:

#### 1. **Proton-Boron (p-B11) / Aneutronic Fusion** — ~8 papers
Strong cluster with papers spanning physics, feasibility, and economics:
- `8UST5IMD` — HB11—Understanding Hydrogen-Boron Fusion as a New Clean Energy Source (2023)
- `SGIQMK5B` — Preventing ash from poisoning proton–boron 11 fusion plasmas (2025)
- `86VXIL2R` — Preventing ash from poisoning proton-boron 11 (preprint, 2025)
- `BJWP66UK` — Wave-supported hybrid fast-thermal p-11B fusion (2022)
- `EMDGGJXK` — A New Evaluation of the 11B(p,α)αα Reaction Rates (2016)
- `UF6YY6EN` — Improving feasibility of economical proton-boron-11 fusion (2022)
- `EWW24Q7H` — Elimination of Secondary Neutrons from Laser Proton-Boron Fusion (2021)
- `NVZMF5HC` — Focus Fusion: Overview of Progress Towards p-B11 with Dense Plasma Focus (2023)
- Also related: `EWQDN2SG` — Colliding Beam Fusion Reactor (1997), `2JELYA48` — Aneutronic power symposium (1989)

**Strength**: Coherent concept with physics + economics + feasibility papers. Exotic enough to be interesting. Clear contrast with D-T fusion economics.

#### 2. **Tokamak Economics** — ~15 papers
The largest cluster, spanning ARIES studies through modern commercial designs:
- `PMXLGPKG` — TEA D-T MFE Cost Analysis (2025) ✅ already extracted
- `IH9ZSRF8` — TEA of D-T MFE (thesis, 2024)
- `FJBCCYBR` — Overview of the SPARC tokamak (2020)
- `KLP5A8SE` — ARIES-RS reversed-shear tokamak power plant study (1997)
- `9MU8HUC6` — The ARIES tokamak reactor study (1989)
- `6GRAXEA4` — The ARIES tokamak fusion reactor study (1989)
- `FKQXYYKL` — Potential minimum cost of electricity of superconducting magnet tokamak reactors (1990)
- `8VYHSXCP` — Study of design parameters for minimizing cost of tokamak fusion (1998)
- `JQLE89UL` — Impact of Disruptions on Economics of a Tokamak Power Plant (2024)
- `H7SKIKNK` — Lessons Learned from TAIES (1994)

**Strength**: Deepest literature, most mature costing. But already partially covered by existing extractions.

#### 3. **Inertial Fusion (IFE)** — ~6 papers
- `LCZMWLYM` — Simplified economic model for inertial fusion (2020) ✅ already extracted
- `GI92TAS2` — Economic studies for heavy-ion-fusion electric power plants (1986)
- `5JQ3TV49` — Development of indirect-drive approach to ICF (1995)
- `BQWVRWCF` — Energy from Inertial Fusion (1992)
- `VKWLFRFK` — Accelerators for Inertial Fusion Energy Production (2013)
- `WQVP4WBW` — Affordable, manageable, practical high-yield/high-gain (Pacific Fusion, 2025)
- `LMZ7HXR5` — VASTAR Approach to Inertial Fusion Energy (standalone PDF)

**Strength**: Good historical depth. Contrasts well with MFE economics.

#### 4. **Stellarator** — ~5 papers
- `7E42ICWG` — Helios Design (stellarator, 2026) ✅ already extracted
- `DT8ZFH9D` — Helios Design (duplicate preprint, 2025)
- `SLFP8J5B` — Helical Fusion Power Plant Economics Studies (2005)
- `NW7CX8PJ` — Stellarator fusion systems enabled by arrays of planar coils (2025)
- `JEQHIH9U` — Thermodynamic/economic analyses of retrofit... stellarator (2024)

**Strength**: Good contrast with tokamaks (same MFE category, very different engineering).

#### 5. **Cross-Concept Economics** — ~10 papers
Papers comparing economics across concepts:
- `6I8Z5PBZ` — Revisit of 2017 Costing for Four ARPA-E ALPHA Concepts ✅ already extracted
- `XH2I672M` — Assessment of Economics of Future Electric Power ✅ already extracted
- `HJMWLC47` — ARIES Cost Account Documentation ✅ already extracted
- `XB9IFQZ8` — A costing framework for fusion power plants (2026)
- `BHWW45IS` — Can fusion energy be cost-competitive? (2023)
- `5KMJ3G3W` — Fusion Power Plant Cost Modeling Uncertainties (2024)
- `8U5V4FUZ` — Reference Class Forecasting for Fusion Power Plant Cost (2024)
- `U87YVD3A` — Extrapolating Costs to Commercial Fusion Power Plants (2024)
- `EF8SNZQD` — Updated Comparison of Economics of Fusion Reactors With Advanced Fission (1991)

**Strength**: Directly serves the investigation's cross-concept comparison goal.

### What Claude Can Do With This Data

**Yes, I can find concept-specific papers.** Given the metadata above, I can:

1. **Search by keyword**: `zot.top(q="stellarator")` finds stellarator papers
2. **Filter by tag**: `zot.top(tag="HB11 || Aneutronic fusion")` finds p-B11 papers
3. **Identify clusters**: Group papers by concept from title/abstract analysis
4. **Check what's already extracted**: Cross-reference against MANIFEST.jsonl
5. **Recommend ingestion batches**: Pick concept-coherent sets for demo purposes

**Limitation**: ~30% of items lack abstracts, so concept identification for those relies on title alone. Tags are inconsistent (user-assigned, no controlled vocabulary).

### Ingestion Constraint

From MEMORY.md: extraction must run from a terminal, not from within Claude Code (the `claude` CLI refuses to run inside another Claude Code session). So **I can identify and queue items, but you'll need to run the actual extraction command.**

## Strategy Recommendations for Next Work Items

### For the Demo: Pick One Concept Cluster + Cross-Concept Economics

The demo needs to show the full arc: ingestion → research → taxonomy → modeling. That works best with:

1. **A focused concept cluster** (3-5 papers about one approach) — shows depth
2. **Cross-concept comparison papers** (2-3 papers) — shows breadth and connects to the investigation scope

**Recommended concept for demo: Inertial Fusion (IFE)**

Rationale:
- Already have 1 extracted paper (Hawker 2020 — simplified IFE economics)
- 5-6 more papers available covering heavy-ion, laser, indirect-drive, and Pacific Fusion
- Clear contrast with MFE (the other extracted papers) — different physics, different cost structure
- Serves the investigation goal: "economics across fundamentally different approaches"
- The Hsu et al. ARPA-E paper (already extracted) covers 4 concepts including some IFE-adjacent ones

Alternative: **p-B11 / Aneutronic** would be more exotic and attention-grabbing for a demo, with ~8 papers. But the economics literature is thinner (most papers are physics-focused).

### Proposed Next Epic Items

**Item 3: Targeted Source Ingestion** [1 day]
- Select ~8-10 papers from the Zotero library (IFE cluster + cross-concept economics)
- Write a small script or use `--tag` workflow to batch-ingest the selected set
- Run extraction from terminal (not Claude Code)
- Update SOURCE_INDEX.md with "Use for" annotations
- Verify extraction quality on cost data tables

**Item 4: Domain Research — Cost Structure Comparison** [1 day]
- Use `/research` against the newly ingested + existing sources
- Extract DI-XXX insights: What cost categories exist? How do IFE and MFE differ?
- Feed findings into taxonomy development (R2)

**Item 5: Taxonomy Framework — Fusion Concept Classification** [1 day]
- Using research findings, build the concept taxonomy
- Confinement types → subtypes → specific approaches
- Identify shared vs. divergent cost structure elements
- This becomes the first real modeling artifact

## Code References

- `scripts/zotero_ingest.py` — batch ingestion pipeline
- `scripts/zotero_lib.py:74-76` — `connect()` creates pyzotero client
- `scripts/zotero_lib.py:135-168` — `resolve_pdf_info()` resolves download metadata
- `scripts/zotero_lib.py:79-88` — `find_pdf_attachment()` finds child PDFs
- `scripts/zotero_ingest.py:247-273` — `fetch_all_processable_items()` gets full library

## Open Questions

1. **Tag-based workflow vs. key list**: Should we tag selected items in Zotero (e.g., "demo-batch") and use `--tag demo-batch`, or pass a list of keys? Tag-based is cleaner for reproducibility.
2. **Budget for demo ingestion**: $50/paper × 10 papers = $500. Acceptable? Could use `--budget 0` for papers where we only need text (no table enhancement).
3. **Which concept cluster for the demo?** IFE (recommended), p-B11 (exotic), or tokamak economics (deepest literature)?
