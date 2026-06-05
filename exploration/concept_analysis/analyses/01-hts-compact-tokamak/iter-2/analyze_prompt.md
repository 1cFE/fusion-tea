# D1+ Concept Analysis: HTS Compact Tokamak (Commonwealth Fusion / ARC)

You are producing a D1+ analysis for the fusion concept **HTS Compact Tokamak (Commonwealth Fusion / ARC)** (Commonwealth Fusion Systems).

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

- Name: ARC 2015 Conservative Pilot phase (Sorbom et al.)
- Maturity: paper-concept
- P_native: 233 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md
  - knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arc-power-conversion-studies.md

(Selection fields are orchestrator-fixed from the design-point table. Copy them verbatim; you are forbidden to edit them. The quantitative description of this plant belongs in Section 5.)

### Canonical 1costingFE Account Schema (this archetype)

These are the **only** account codes you may use in Override Candidates. Do not
invent codes (no `CAS22.1.3`-style strings). Each row says, in one line, what the
account costs — enough to judge whether the dossier justifies an override.

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220103` | Confinement magnets / coils (HTS-REBCO conductor + winding + cryostat) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | supplementary heating (NBI/ICRF/ECRH/LHCD) per installed MW |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | DC magnet power supplies and switchgear |
| `C220108` | Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing) | divertor (W monoblock cassettes on CuCrZr heat sinks) |
| `C220110` | Remote handling & maintenance equipment (rad-hardening tier x vessel geometry) | always (for this archetype) |
| `C220111` | Reactor-equipment installation & assembly (fraction of the CAS22 subtotal) | always (for this archetype) |
| `CAS21` | Buildings & site structures (reactor, turbine, hot cell, balance-of-plant) | always (for this archetype) |
| `CAS23` | Turbine plant equipment (thermal cycle; zero for direct-conversion / eta_th=0 plants) | zero if the design point is direct-conversion (no thermal cycle) |
| `CAS24` | Electric plant equipment (switchyard, transformers, plant distribution) | always (for this archetype) |
| `CAS26` | Heat rejection system (cooling towers, circulating water) | always (for this archetype) |
| `CAS27` | Special materials — initial reactor material inventory / blanket fill (distinct from C220101 structure) | always (for this archetype) |
| `CAS70` | Annualized O&M + scheduled component replacement (staffing-based) | always (for this archetype) |
| `CAS80` | Annualized fuel cost — consumables and enriched-isotope procurement | always (for this archetype) |

### Comparables (fixed — for the Section 7 family-delta)

- 21-spherical-tokamak-hts
- 28-hts-tokamak-full-hts
- 29-negative-triangularity-tokamak
- 33-state-backed-tokamak-best

### Override-Count Rubric (from Archetype-Fit grade)

Archetype-Fit is High → expect 0–4 enabled overrides. Flag in your output if your count falls outside this band.

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
    expression over the **native** `result` (e.g. `0.70 * result.costs.cas21`).
    Relative overrides MUST reference the native `result`, never `result_1gw`.
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

### Approved (primary cross-reference pool)

| Concept Name | Company | Confinement Family | Iterations | Extracted |
|---|---|---|---|---|
| Spherical Tokamak HTS (Tokamak Energy) | Tokamak Energy | MFE | iter-2/FAIL (3 findings) | E* |

### In Progress (by maturity)

| Concept Name | Company | Confinement Family | Iterations | Extracted |
|---|---|---|---|---|
| MagLIF (Pacific Fusion) | Pacific Fusion | MIF | iter-11/FAIL (3 findings) | E* |
| QI Stellarator HTS (Proxima Fusion / Stellaris) | Proxima Fusion | MFE | iter-9/FAIL (3 findings) | E |
| Laser ICF Hybrid Drive (Xcimer Energy) | Xcimer Energy | IFE | iter-7/FAIL (3 findings) | E* |
| Acoustic ICF (Sonofusion) | Sonofusion Energy | IFE | iter-6/FAIL (3 findings) | E |
| Electrostatic Hybrid (Orbitron) | Avalanche Energy | MFE | iter-5/FAIL (3 findings) | E |
| Orbital Levitated Dipole (Zephyr Energy) | Zephyr Fusion | MFE | iter-5/FAIL (3 findings) | E |
| Type One Stellarator (Type One Energy) | Type One Energy | MFE | iter-5/FAIL (3 findings) | E* |
| Projectile ICF (First Light Fusion) | First Light Fusion | IFE | iter-5/PASS | E |
| HTS Tokamak Full HTS | Energy Singularity | MFE | iter-5/FAIL (3 findings) | E* |
| FRC w/ Direct Conversion (Helion Energy) | Helion Energy | MFE | iter-4/FAIL (3 findings) | E |
| Levitated Dipole (OpenStar Technologies) | OpenStar Technologies | MFE | iter-4/FAIL (3 findings) | E |
| MTF Pneumatic Compression (General Fusion) | General Fusion | MIF | iter-4/FAIL (3 findings) | E* |
| Heavy-Ion Beam ICF | Intensity Energy | IFE | iter-4/FAIL (3 findings) | E* |
| Negative-Triangularity Tokamak | Firefly Fusion | MFE | iter-4/FAIL (3 findings) | E* |
| Laser ICF NIF Commercialization (Focused Energy LIFE-class) | Inertia Enterprises | IFE | iter-4/FAIL (3 findings) | E* |
| State-Backed Tokamak (Neo / ASIPP-class) | Neo Fusion | MFE | iter-4/FAIL (3 findings) | E* |
| Polomac Magnetic Confinement (Deutelio) | Deutelio | MFE | iter-4/FAIL (3 findings) | E |
| Helical-Coil Stellarator (HESTIA) | Helical Fusion | MFE | iter-4/FAIL (3 findings) | E* |
| Large-Scale Stellarator | Gauss Fusion | MFE | iter-3/FAIL (3 findings) | E |
| Sheared-Flow Z-Pinch (Zap Energy) | Zap Energy | MFE | iter-3/FAIL (3 findings) | E |
| Muon-Catalyzed Fusion (Acceleron Fusion) | Acceleron Fusion | OTHER | iter-3/FAIL (3 findings) | E |
| Laser ICF Fast Ignition (Focused Energy) | Focused Energy | IFE | iter-3/FAIL (3 findings) | E |
| PB11 FRC (TAE Technologies) | TAE Technologies | MFE | iter-3/FAIL (3 findings) | E |
| Renaissance Stellarator (Renaissance Fusion) | Renaissance Fusion | MFE | iter-3/FAIL (3 findings) | E |
| Laser ICF Nanostructured Target (Marvel Fusion) | Marvel Fusion | IFE | iter-3/FAIL (9 findings) | E |
| Dense Plasma Focus (LPP Fusion) | LPPFusion | MFE | iter-3/FAIL (3 findings) | E |
| Laser ICF Indirect Drive (Inertia Thunderwall) | Inertia Enterprises | IFE | iter-3/FAIL (3 findings) | E |
| Polywell (EMC2) | EMC2 | MFE | iter-3/FAIL (3 findings) | E |
| Laser ICF OEC Architecture (BLF) | Blue Laser Fusion | IFE | iter-3/FAIL (3 findings) | E |
| Laser ICF French National (GenF) | GenF Systems | IFE | iter-3/FAIL (3 findings) | E |
| Spherical Tokamak CS-Free PB11 (ENN) | ENN Energy | MFE | iter-3/FAIL (2 findings) |  |
| Laser ICF Liquid-Jet Target (Cortex Fusion Systems) | Cortex Fusion | IFE | iter-2/FAIL (3 findings) | E* |
| Magnetic Mirror (Pale Blue) | Pale Blue | MFE | iter-2/FAIL (3 findings) | E* |
| MTIF (Magneto-Inertial Fusion Technologies) | NearStar Fusion | MIF | iter-2/FAIL (3 findings) |  |
| Particle Accelerator-Driven Fusion (SHINE-style) | SHINE Technologies | OTHER | iter-2/FAIL (3 findings) |  |
| Laser ICF (HB11 Energy) | hb11 | IFE | iter-1/INTERRUPTED | E* |
| Planar-Coil Stellarator (Thea Energy) | Thea Energy | MFE | iter-1/INTERRUPTED | E* |
| Magnetic Mirror (Realta Fusion / CoSMo) | Realta Fusion | MFE | iter-1/INTERRUPTED | E* |





## Mode: Feedback Pass

You are improving an existing analysis based on specific feedback from the
assessment agent.

### Existing Analysis
Read this file completely first: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md`

### Feedback to Address
Then read the feedback: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/iter-2/pre_feedback.md`

The feedback contains `### F-N:` findings with a Target, Category, Finding,
Recommendation, and Priority. Address each finding.

Findings marked `Category: model` primarily target the model code
(`model_setup.py` — the `overrides` list, `spec` dict, sweeps). You should still
update analysis prose where it supports the model change (e.g. a Section 5b
override entry or a Section 5 parameter row), but do NOT try to resolve model
findings by narrative rewording alone — the model-setup agent receives them too.

If the feedback contains a "Carried-Forward Assessment Findings" section, treat
those unresolved findings with the same priority as regular findings.

### Preserve the fixed contract
- Do **not** edit the `## Design Point` selection block — its fields are
  orchestrator-fixed. Targeted edits only; do not re-write conforming sections.
- Any Override Candidate you add or change uses a **canonical** account code from
  the schema above and the six-field shape.

### Source Documents (use subagents for targeted evidence)
For each finding, spawn subagents with questions specific to that finding.

Sources available: - `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md` (172 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/sparc-icrf-heating-paper.md` (65 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arc-power-conversion-studies.md` (35 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2405-01514.md` (61 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2503-23048.md` (59 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2601-21724.md` (165 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2602-19389.md` (249 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/cfs-2025-2026-updates.md` (6 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-etdeweb-servlets-purl-10149275.md` (164 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-etdeweb-servlets-purl-20261446.md` (11 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-servlets-purl-1305833.md` (48 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-servlets-purl-1820946.md` (14 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/sciencedirect-science-article-pii-s092037961930835x.md` (2 KB)
- `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/sciencedirect-science-article-pii-s2772830725000390.md` (2 KB)
Dossier (read directly — short and structured): `/home/reid/1cfe/fusion-tea/knowledge/concept_research/01-hts-compact-tokamak/dossier.md`

### Instructions
1. Read the existing analysis completely
2. Read the feedback findings
3. For each finding, gather targeted evidence via the per-source subagent pattern
4. Use the Edit tool to make targeted improvements to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md`
5. Do NOT rewrite sections the feedback doesn't address; maintain existing citations
6. If a finding asks for parameter rows, add them in the correct table position
   with Source and Confidence columns
7. After editing, re-read the modified sections to verify coherence




## Output Template Structure

`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/prompt_templates/output_template.md` defines the canonical sections. The analysis must follow
this structure regardless of mode.

## Comparables and Cross-Concept Context

- `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`

If approved prior analyses are available:
- Read them to keep shared-subsystem assumptions and cost structures consistent —
  cite the source concept when you reuse an assumption.
- Articulate divergences in Section 7 (Family-Delta vs Comparables), measured
  against the fixed Comparables list — not an arbitrary neighbour.
- Do NOT copy text verbatim — synthesize and adapt to this concept's specifics.
