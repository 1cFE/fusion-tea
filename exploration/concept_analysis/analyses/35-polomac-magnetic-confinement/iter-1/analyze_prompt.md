# D1+ Concept Analysis: Polomac Magnetic Confinement (Deutelio)

You are producing a D1+ analysis for the fusion concept **Polomac Magnetic Confinement (Deutelio)** (Deutelio).

## Analysis Goals

# Analysis Goals

These are the objectives the analysis agent works toward. Every section of the
analysis should contribute to answering these questions.

**What is already fixed upstream (do NOT re-decide):** the concept's confinement
family, its 1costingFE archetype, the fixed list of comparable concepts, and the
named design point (plant name, maturity, native net-electric power `P_native`,
and grounding confidence) are all determined by the upstream tables and arrive
through the analysis frontmatter. They are inputs, not outputs. Your job is not
to choose a family, a nearest neighbour, or a plant — it is to *articulate the
delta* against the fixed comparables and to *extract and account for* the design
point you are given.

1. **Family-Delta Articulation**: Given the fixed comparables, what does this
   design point do differently, and how does that difference move cost? Name the
   specific subsystem, the direction of the cost effect (advantage / penalty /
   neutral), and the magnitude where the data supports it. "It is a tokamak" is
   not a delta; "its all-REBCO TF coils replace the LTS magnets the comparable
   prices at $X/kg" is.

2. **Design-Point Parameter Extraction**: Extract the complete quantitative
   description (geometry, physics, performance) of the *named* design point at
   its *native* scale. Every LCOE-relevant parameter you record must describe
   that one plant — not a different machine, not a different power level, not a
   roadmap aspiration.

3. **TEA Implications**: For each family-delta, state the techno-economic
   consequence. Which differences create cost advantages, which create cost
   penalties, which are cost-neutral, and which are simply unknown for lack of
   data?

4. **Override-Candidate Discovery**: For each canonical 1costingFE account the
   archetype touches, decide whether the dossier names a company-grounded
   quantity, unit cost, or published dollar figure that justifies departing from
   the library default. The library carries the default story; an override is an
   *accountable, evidence-backed* departure from it — not a guess and not an
   optimism adjustment.

5. **Risks and Assumptions**: Are the key risks and assumptions called out, and
   is the analysis honest about what it does not know? How should each be carried
   into the TEA — as a sensitivity parameter, a scenario branch, or an explicit
   data gap?


## Quality Standards

# Quality Standards

## The Library Is the Default Story
The 1costingFE library already prices every account for this archetype from its
built-in per-archetype defaults. You do **not** restate, re-pass, or "confirm"
those defaults. The analysis's job is to describe the design point and to flag
the *specific* accounts where company data justifies departing from the library
— nothing else is an override.

- Do **not** emit `# DEFAULT: ...` re-passes of library values. An account you
  do not override is *already* handled by the library; saying so adds noise and
  invites accidental drift.
- Do **not** put uniform financial / operating-economics parameters
  (`availability`, `lifetime_yr`, `interest_rate`, `inflation_rate`) into the
  design point or the override registry. These are library-owned and identical
  across concepts by construction.

## Override Accountability (six fields, honest provenance)
Every override candidate is a six-field registry entry: `account`, `value`,
`enabled`, `provenance`, `source`, `rationale`.

- `account` MUST be a canonical 1costingFE code from the schema you are given
  (e.g. `C220103`, `CAS27`) — never an invented `CAS22.1.3`-style code.
- `provenance` is `direct` only when the company published the exact dollar
  figure (or a quantity × a stated unit price, both directly published).
  Anything you assemble from a published quantity plus an analyst-sourced unit
  price is `derived`, and the arithmetic — including any CPI inflation factor —
  MUST be shown in `rationale`.
- An override is justified by *evidence*, not by optimism. "We think we can do
  better than the default" is not an override; "the company published 156 t of
  HTS at $44k/kg" is.

## Citation Standards
Follow the Citation Format section in the output template exactly. Key rules:
- Parameter table Source column: `filename.md §Section Heading` (not bare filenames)
- 3–5 direct block quotes per section for critical claims
- Derivation chains for all `[inferred]` values
- Footnote-style references in prose with source path and section

## Anti-Hallucination Rules
- If data does not exist in the provided sources, say "No data found in
  available sources" — do not invent plausible-sounding facts, cost figures, or
  performance numbers.
- Do NOT cite papers or sources not in the provided materials unless they are
  well-known landmark publications you are certain exist.
- When a section has thin data, write a shorter section that honestly states
  what is and isn't known. Prefer "unknown" over "likely" when evidence is absent.

## Depth Expectations
- Match the analytical depth of the handwritten exemplars.
- TRL assessments: Demonstrated / On paper only / Missing at scale.
- LCOE challenges ranked by impact, not listed randomly.
- Materials / supply chain: quantify demand vs. supply where possible.
- The analysis should be useful to an engineer building an LCOE model — and to
  the model-setup agent that reads your Design Point block and Override
  Candidates registry directly.


---

## Fixed Contract Inputs (orchestrator-supplied — do NOT re-decide)

The upstream tables have already fixed this concept's design point, archetype, and
comparables. They reach you below as rendered blocks. Treat every one as a **read-
only input**: copy it where instructed, extract against it, and build on it — but
never re-choose, re-derive, or edit it.

### Design Point (selection — copy verbatim to the top of the analysis body)

## Design Point

(No design-point row for this concept yet — selection is upstream-pending. Do not invent one.)

### Canonical 1costingFE Account Schema (this archetype)

These are the **only** account codes you may use in Override Candidates. Do not
invent codes (no `CAS22.1.3`-style strings). Each row says, in one line, what the
account costs — enough to judge whether the dossier justifies an override.

(No 1costingFE archetype mapping for this concept — the canonical account schema does not apply. Do not propose account-coded overrides.)

### Comparables (fixed — for the Section 7 family-delta)

(No comparable concept in the corpus for this design point.)

### Override-Count Rubric (from Archetype-Fit grade)

(No archetype-fit grade for this concept — the override-count band does not apply.)

## Override Candidate Discovery

# Per-Account Override Walkthrough

This is the discipline for discovering override candidates. It is **not**
open-ended. You do not ask "what overrides does this concept need?" — you walk
the canonical account schema you were given, one account at a time, and for each
one ask the same question of the dossier.

## The walkthrough

For **each** account in the canonical schema (the table injected above), ask:

> Does the dossier name a **company-grounded quantity, unit cost, or published
> dollar figure** that lets me price *this account* better than the 1costingFE
> library default?

Then decide:

- **No company data for this account** → propose **no** override. The library
  default stands. This is the common case; most accounts are not overridden.
  Do not invent a value and do not re-state the default.
- **Yes, the dossier grounds this account** → write a six-field Override
  Candidate entry:
  - `account` — the canonical code from the schema (never an invented code).
  - `value` — a plain number, a self-documenting constant expression (e.g.
    `260.0 * 1.34` for a CPI-adjusted published cost), or — for a *relative*
    override defined as a fraction of the library's own computation — an
    expression over the library's bare overrides-off cost, written as
    `0.70 * generic.costs.cas21`. (In `model_setup.py`, `generic` is the
    mandatory `generic_reference(model, spec, P_native)` line placed before the
    overrides list; the model-setup prompt has the mechanics.) A relative
    `value` MUST reference `generic`, never `native` or the 1 GWe projection.
  - `enabled` — `true` if this departure should be active in the baseline run.
  - `provenance` — `direct` (company published the exact figure, or a published
    quantity × a published unit price) or `derived` (you assembled it from a
    published quantity plus an analyst-sourced unit price). When `derived`, the
    arithmetic — including any CPI factor — MUST appear in `rationale`.
  - `source` — `filename.md §Section` pointing at the company-grounded evidence.
  - `rationale` — why the library default misrepresents this design point, and
    the derivation chain for the value.

## Why per-account, not ad-hoc

Open-ended override discovery under-proposes: it finds the one or two obvious
departures and silently skips the rest. Walking every canonical account forces a
deliberate yes/no on each, so a legitimate override is never missed and an
un-evidenced one is never invented. "I considered this account and the dossier
gives no company figure for it" is a complete, correct answer for most accounts.

## Count sanity-check

After the walkthrough, compare your count of `enabled` overrides against the
expected band for this concept's archetype-fit grade (given to you as the
override-count rubric). If your count falls outside the band, do not pad or prune
to hit it — instead add one line noting the discrepancy and why your evidence
genuinely supports the count you have. The band is a smell-check, not a quota.


---

## Per-Source Reading Pattern

For each source document you need to read, spawn a **separate subagent** using the
Agent tool. Do NOT read all sources in your main thread — delegate each source to a
subagent for context efficiency.

**Subagent prompt template:**
# Source Reader

Read the source document and answer the provided questions.

## Instructions
1. Read the entire source document
2. For each question, provide a focused answer with:
   - The relevant information from the source
   - The section heading or location where you found it (e.g., §Results, §Table 3)
   - Direct quotes for the most important claims
3. If the source does not contain information relevant to a question,
   say "Not addressed in this source"
4. Keep answers concise — focus on facts and data, not interpretation


Construct each subagent call as follows:
- Give the subagent the path to ONE source document
- Provide 3–5 specific questions (see your mode instructions below for what to ask)
- The subagent reads the source and returns answers with section references

After receiving subagent responses, **read the cited sections yourself** to confirm
the subagent's characterization before incorporating claims. Do not blindly trust
subagent summaries for critical claims.


## Cross-Concept Memory

The following insights were captured from prior concept analyses. Use them to avoid
known pitfalls and apply established patterns. Do not cite these memories as
sources — they are guidance, not evidence. Verify any specific claims against the
actual source documents.

## ARIES Studies Are Best Parameter Source for MFE Concepts
Date: 2026-03-29 | Concepts: MFE

ARIES-AT and ARIES-CS studies provide the most complete parameter sets
for magnetic confinement cost modeling — plant-level CAS breakdowns,
thermal efficiency targets, and magnet cost estimates. Prefer these over
individual paper estimates when available. Cross-check against PROCESS
code outputs where overlap exists.

## Assessment Repeatedly Flags Missing O&M Breakdown
Date: 2026-03-29 | Concepts: all

The assessment agent flags missing O&M cost breakdown (fixed vs variable,
scheduled maintenance, unplanned outage costs) in >80% of first-pass
analyses. Cold-start analyses should include a placeholder O&M subsection
in Section 3 even when source data is sparse, to avoid a guaranteed
feedback finding.



## Concept Landscape

The taxonomy of all fusion concepts under investigation, grouped by pipeline
maturity. The comparables for *this* concept are already fixed (above) — use the
landscape only for context, not to re-select neighbours.

## Concept Landscape (39 concepts)

Use this catalog for nearest-neighbor identification and cross-concept positioning.
Approved concepts have full analyses available; I{N} indicates N completed iterations.


### In Progress (by maturity)

| Concept Name | Company | Confinement Family | Iterations | Extracted |
|---|---|---|---|---|
| Acoustic ICF (Sonofusion) | Sonofusion Energy | IFE | iter-6/FAIL (3 findings) | E* |
| Orbital Levitated Dipole (Zephyr Energy) | Zephyr Fusion | MFE | iter-5/FAIL (3 findings) | E* |
| Muon-Catalyzed Fusion (Acceleron Fusion) | Acceleron Fusion | OTHER | iter-3/FAIL (3 findings) | E* |
| Laser ICF Fast Ignition (Focused Energy) | Focused Energy | IFE | iter-3/FAIL (3 findings) | E* |
| Polywell (EMC2) | EMC2 | MFE | iter-3/FAIL (3 findings) | E* |
| HTS Tokamak Full HTS | Energy Singularity | MFE | iter-3/FAIL (3 findings) | E* |
| Laser ICF NIF Commercialization (Focused Energy LIFE-class) | Inertia Enterprises | IFE | iter-3/FAIL (3 findings) | E* |
| Spherical Tokamak CS-Free PB11 (ENN) | ENN Energy | MFE | iter-3/FAIL (2 findings) |  |
| HTS Compact Tokamak (Commonwealth Fusion / ARC) | Commonwealth Fusion Systems | MFE | iter-2/FAIL (1 findings) | E* |
| Negative-Triangularity Tokamak | Firefly Fusion | MFE | iter-2/PASS | E* |
| Laser ICF OEC Architecture (BLF) | Blue Laser Fusion | IFE | iter-2/FAIL (3 findings) | E* |
| Particle Accelerator-Driven Fusion (SHINE-style) | SHINE Technologies | OTHER | iter-2/FAIL (3 findings) |  |
| Heavy-Ion Beam ICF | Intensity Energy | IFE | iter-1/PASS | E* |
| Laser ICF Indirect Drive (Inertia Thunderwall) | Inertia Enterprises | IFE | iter-1/PASS | E* |
| Laser ICF French National (GenF) | GenF Systems | IFE | iter-1/PASS | E* |
| State-Backed Tokamak (Neo / ASIPP-class) | Neo Fusion | MFE | iter-1/INCOMPLETE | E |

### Not Started

| Concept Name | Company | Confinement Family | Extracted |
|---|---|---|---|
| Laser ICF Liquid-Jet Target (Cortex Fusion Systems) | Cortex Fusion | IFE | E* |
| Laser ICF (HB11 Energy) | hb11 | IFE | E* |
| Planar-Coil Stellarator (Thea Energy) | Thea Energy | MFE | E* |
| Magnetic Mirror (Pale Blue) | Pale Blue | MFE | E* |
| MagLIF (Pacific Fusion) | Pacific Fusion | MIF | E* |
| FRC w/ Direct Conversion (Helion Energy) | Helion Energy | MFE | E* |
| QI Stellarator HTS (Proxima Fusion / Stellaris) | Proxima Fusion | MFE | E* |
| Large-Scale Stellarator | Gauss Fusion | MFE | E* |
| Magnetic Mirror (Realta Fusion / CoSMo) | Realta Fusion | MFE | E* |
| Levitated Dipole (OpenStar Technologies) | OpenStar Technologies | MFE | E* |
| Electrostatic Hybrid (Orbitron) | Avalanche Energy | MFE | E* |
| MTF Pneumatic Compression (General Fusion) | General Fusion | MIF | E* |
| Sheared-Flow Z-Pinch (Zap Energy) | Zap Energy | MFE | E* |
| Laser ICF Hybrid Drive (Xcimer Energy) | Xcimer Energy | IFE | E* |
| PB11 FRC (TAE Technologies) | TAE Technologies | MFE | E* |
| Type One Stellarator (Type One Energy) | Type One Energy | MFE | E* |
| Renaissance Stellarator (Renaissance Fusion) | Renaissance Fusion | MFE | E* |
| Spherical Tokamak HTS (Tokamak Energy) | Tokamak Energy | MFE | E* |
| Projectile ICF (First Light Fusion) | First Light Fusion | IFE | E* |
| Laser ICF Nanostructured Target (Marvel Fusion) | Marvel Fusion | IFE | E* |
| Dense Plasma Focus (LPP Fusion) | LPPFusion | MFE | E* |
| Helical-Coil Stellarator (HESTIA) | Helical Fusion | MFE | E |
| MTIF (Magneto-Inertial Fusion Technologies) | NearStar Fusion | MIF |  |



## Mode: Cold Start

You are producing a D1+ analysis from scratch. No prior analysis exists for this
concept.

### Required Reading

Read these files in this order before writing:

1. **Output Template** (canonical section structure you must follow): `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\prompt_templates\output_template.md`
2. **Analysis Brief** (purpose and quality expectations): `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\concept_analysis_brief.md`
3. **Handwritten Exemplars** (calibrate depth and style): - `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\handwritten\01-hts-compact-tokamak.md`
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\handwritten\07-maglif.md`
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\handwritten\08-frc-w-direct-conversion.md`
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\handwritten\11-magnetic-mirror-comparison.md`
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\handwritten\11-magnetic-mirror.md`
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\handwritten\26-laser-icf-indirect-drive.md`
4. **Dossier** (structured research summary — your factual foundation): `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\35-polomac-magnetic-confinement\dossier.md`
5. **Extracted Source Documents** (use subagents — see Per-Source Reading Pattern).
   For cold start, ask each subagent:
   - What does this source say about the concept's cost structure and unique subsystems?
   - What LCOE-relevant parameters or performance targets for the **named design point** are stated?
   - What cost advantages or penalties relative to the comparables are discussed?
   - What technical risks, assumptions, or data gaps are mentioned?
   - What materials, supply-chain, or manufacturing considerations are relevant?

   Sources to read via subagents:
   - `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\35-polomac-magnetic-confinement\iter-01\sources\deutelio-company-profile.md` (2 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\35-polomac-magnetic-confinement\iter-01\sources\elio-2014-fed-poloidal-confinement.md` (9 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\35-polomac-magnetic-confinement\iter-01\sources\jtsp-2024-polomac-technical-report.md` (2 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\35-polomac-magnetic-confinement\iter-01\sources\jtsp-jtsp-article-download-32-28.md` (0 KB)
6. **Schema** (controlled vocabulary and column definitions): `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\phase_1a\schema.md`

### Content Requirements
- Follow the canonical section structure from the output template exactly:
  the `## Design Point` block at the top, then Sections 1–8 (including Section 5
  "Design Point Parameters" and Section 5b "Override Candidates").
- **Copy the rendered Design Point block verbatim** to the top of the body. Do not
  edit its selection fields.
- Every quantitative value in Section 5 must describe the **named design point at
  native scale** and carry a Source and Confidence entry.
- Section 5b Override Candidates must come from the per-account walkthrough above —
  six-field entries, canonical account codes only.
- Section 7 articulates the family-delta against the fixed Comparables list.
- Values without sources must be flagged `[inferred]`, `[analogue]`, or
  `[estimated]` with reasoning.

### Output

Write the complete analysis **body** to this file using the Write tool:
`C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\35-polomac-magnetic-confinement\iter-1\analysis_body.md`

Write ONLY the analysis content (the `## Design Point` block followed by Sections
1–8). Do NOT include:
- YAML frontmatter (the pipeline adds it automatically)
- Preamble, commentary, or code fences wrapping the document

Start the file with the `## Design Point` block (copied verbatim) and end after
Section 8.

### Frontmatter is orchestrator-owned — do not edit it

The pipeline pre-populates the analysis frontmatter from the signed-off upstream
tables. The fields `Comparables`, `Confinement-Family`, `Archetype`,
`Archetype-Fit`, `Comparison-Status`, and the four `Design-Point-*` fields are
determined upstream and are **not** analyzer-editable. Do not add, edit, or remove
frontmatter fields — write only the analysis body.






## Output Template Structure

`C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\prompt_templates\output_template.md` defines the canonical sections. The analysis must follow
this structure regardless of mode.

## Comparables and Cross-Concept Context

No approved prior analyses available.

If approved prior analyses are available:
- Read them to keep shared-subsystem assumptions and cost structures consistent —
  cite the source concept when you reuse an assumption.
- Articulate divergences in Section 7 (Family-Delta vs Comparables), measured
  against the fixed Comparables list — not an arbitrary neighbour.
- Do NOT copy text verbatim — synthesize and adapt to this concept's specifics.
