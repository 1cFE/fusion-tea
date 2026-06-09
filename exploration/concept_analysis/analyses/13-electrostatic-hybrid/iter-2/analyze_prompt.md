# D1+ Concept Analysis: Electrostatic Hybrid (Orbitron)

You are producing a D1+ analysis for the fusion concept **Electrostatic Hybrid (Orbitron)** (Avalanche Energy).

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

**The headline is the replicated 1 GWe fleet.** Every concept's comparable number
is LCOE for a 1 GWe NOAK plant, reached by *replicating* the real `P_native`
design point into a fleet of identical modules — never a monolithic 1000 MWe
machine. Override values and rationales share that frame: a relative override
means "`M` of the library's 1 GWe *fleet* cost for that account," and its
rationale is anchored to the library's modular-fleet default, not a "conventional
1 GWe plant." (The full semantics — the S/U/P cost classes and the single
invariant — are in the override-semantics policy embedded in the override-
discovery section of your prompt.)

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

## The Headline Is the Replicated 1 GWe Fleet
Every concept's comparable number is LCOE for a 1 GWe NOAK plant, reached by
*replicating* the real `P_native` design point into a fleet of identical modules
(`run_native_and_1gw`, `noak=True`) — never a monolithic 1000 MWe machine.
Override values and their rationales share that frame: a relative override means
"`M` of the library's 1 GWe *fleet* cost for that account," and its rationale is
anchored to the library's modular-fleet default, **not** a "conventional 1 GWe
plant." (The full semantics — the S/U/P cost classes and the single invariant —
are in the override-semantics policy embedded in the override-discovery section
of your prompt.)

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

- Name: Orbitron commercial module — lower bound (Avalanche Energy product page / CWFest 2023)
- Maturity: paper-concept
- P_native: 0.005 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-orbitron-page.md
  - knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-cwfest2023-blog.md

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
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | primary pulsed driver (laser/accelerator/gun) on $/J of driver energy; electrical-drive concepts cost it in C220107 |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | pulsed-power capacitor bank on $/J stored — usually the dominant driver cost for electrically-driven pulsed schemes |
| `C220108` | Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing) | high-rep-rate target manufacturing factory (IFE/MIF) |
| `C220109` | Direct energy converter (electrostatic for mirror/FRC exhaust, or inductive DEC on a pulsed driver) | only if the design point uses direct energy conversion (directed axial exhaust or an inductive DEC stage) |
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

(No comparable concept in the corpus for this design point.)

### Override-Count Rubric (from Archetype-Fit grade)

Archetype-Fit is Med → expect 3–8 enabled overrides. Flag in your output if your count falls outside this band.

## Override Candidate Discovery

Before proposing any relative override, read the override-semantics policy below.
It carries the single headline invariant (`account = M × the library's 1 GWe
fleet cost for that account`), the S/U/P cost classes, and the modular-fleet
rationale baseline. The model-setup agent that transcribes your Section 5b reads
the same policy, so your override values and rationales must already be in this
frame.

# Override semantics and the 1 GWe headline

## The invariant (this is the whole rule)

Every concept's headline is one number: LCOE for a **1 GWe NOAK plant**, reached
by **replicating** the real `P_native` design point into a fleet of `n_mod`
identical modules (`run_native_and_1gw(...)`, `noak=True`). There is no monolithic
1 GWe machine — we never extrapolate the physics model to a single 1000 MWe
reactor we have no design basis for.

At that headline, for **every account in every class**:

    account = M × (the library's 1 GWe fleet cost for that account)

`M` is the fraction of the library's fleet answer you believe this concept should
pay. `M = 1.0` means "trust the library default"; you only write an override when
evidence says this concept departs from it. That is the entire authoring rule.

The framework guarantees this invariant regardless of *which* `generic` value you
anchor to: `_scale_overrides` (in `1costingfe/src/costingfe/model.py`) rescales
your override from the native frame to the fleet frame by the per-account ratio
`fleet_cost / native_cost`, so the headline always lands on `M × fleet_cost`. You
do **not** compute that ratio yourself — you pick the right `generic` anchor for
the account's storage shape (below) and the framework does the rest.

## The cost classes — comprehension, not three rules

The classes below explain **why** the fleet cost is what it is (so you can sanity-
check `M`) and dictate the **authoring shape** — which `generic` value you anchor
to. They do **not** introduce per-class multipliers. If you delete the table, the
invariant above still tells you what an override means; the table only tells you
*where to anchor it* and *why the fleet cost looks the way it does*.

| Class | Why the fleet cost is what it is | Authoring shape (what to anchor to) | Accounts |
|---|---|---|---|
| **S — Shared / fixed** | A site needs these **once**, however many modules it runs — the library charges them once across the fleet. That single charge *is* the amortization that gives a small machine a fair shot. | whole-plant M$ → `M * generic.costs.<rollup>` | CAS10, CAS21, CAS28, CAS40, CAS70 |
| **U — Per-unit** | One per module: `N` modules → `N` cores. The library multiplies by `n_mod`; `noak=True` credits mass-production learning as the offset for losing single-core economy of scale. | per-module M$ → `M * generic.cas22_detail["C2201xx"]` | CAS22 reactor-island sub-accounts `C2201xx`; CAS80 fuel (taught, but not overridable today — see note) |
| **P — Power-proportional** | Scales with the **total** plant power, so the value is the same whether you replicate or not. | whole-plant M$ → `M * generic.costs.<rollup>` | CAS23, CAS24, CAS25, CAS26, CAS27; plant-wide CAS22 sub-accounts `C2202xx`–`C2207xx` |

**Storage-shape footnotes (which `generic` attribute exists):**
- Only the CAS22 reactor-island sub-accounts (`C2201xx`) live under
  `generic.cas22_detail["C220xxx"]`. Everything else — CAS21, CAS23–27, CAS70,
  CAS80, and the CAS22 rollup — is a top-level attribute on `generic.costs`.
- **Taught but NOT overridable today: CAS40 (owner's costs), CAS70 (O&M), and
  CAS80 (fuel).** Overrides on these are silently dropped — e.g. a CAS80 override,
  whether absolute (`0.050`) or relative (`M * generic.costs.cas80`), leaves the
  fleet value at the library default and does **not** move the headline
  (`1cFE/1costingfe#106`; the CAS70 / CAS80 no-op is pinned by
  `1costingfe/tests/test_override_scaling_semantics.py`). They are in the class
  table so you know *why* the library prices them as it does (and so a future
  override surface lands on prepared ground) — but do **not** author an override
  against them expecting an effect. Use only codes from the canonical account
  schema you are given.

**Reading the output — how to verify a Class-U override actually scaled:**
The `print_cas_breakdown` **CAS22 sub-account detail table shows per-module M$ at
every scale** — its `native` (n_mod=1) and `1 GWe` (n_mod=200) columns are
*supposed to be identical* for a `C2201xx` row, because the per-module cost does not
change; the ×`n_mod` fleet multiplication shows up in the **`C220000` / `CAS22`
rollup**, not in the detail row. So a Class-U detail row that reads the same at
native and 1 GWe is **expected, not a scaling failure.** To confirm a Class-U
override reached the fleet, check that the **`CAS22` (or `C220000`) rollup** moved
by roughly `Δ(per-module value) × n_mod` — never infer "it didn't scale" from the
detail row alone.

## The rationale baseline (one named frame, always)

Every relative override's `rationale` answers "why is `M` what it is?" against
**one** named baseline:

> **the library's default for a fleet of this device at 1 GWe.**

Never against "a conventional 1 GWe plant" / a monolithic 1000 MWe machine — under
the always-replicate decision that baseline does not exist. Anchor the rationale
to the same frame as the value. (Citing a monolithic plant from the literature as
a *comparable* — ARC, STEP — is fine; using one as the override's *anchor
baseline* is the inconsistency this policy removes.)

A multiplier above 1.0 is legitimate: it means "this concept's account costs more
than the library's modular-fleet default" (e.g. a harder-to-build module), still
in the fleet frame — not "more than a conventional plant."

## What wrong looks like

- **Value/rationale frame mismatch.** Value reads `0.70 * generic.cas22_detail["C220101"]`
  (70% of one module's blanket) while the rationale says "70% of a conventional
  1 GWe plant's blanket." The value is per-module fleet-frame; the rationale is
  monolithic. Rewrite the rationale in the modular-fleet frame.
- **Monolithic baseline in rationale.** Any "vs a conventional / standard 1 GWe
  plant," "vs a monolithic reactor," or bare "vs library default" with no fleet
  frame. Replace with "vs the library's 1 GWe modular-fleet default."
- **Class/anchor mismatch.** Overriding a CAS22 sub-account (Class U) but anchoring
  to a top-level rollup (e.g. `C220101` valued against `generic.costs.cas21`).
  Anchor each account to its own storage location: `C2201xx` →
  `generic.cas22_detail["C2201xx"]`; top-level rollups → `generic.costs.<rollup>`.


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
  - **Identify the account's cost class first (S / U / P)** using the
    override-semantics class table embedded above. The class is part of the yes/no
    decision: it tells you why the library's 1 GWe fleet cost is what it is and
    dictates the **authoring shape** — a per-module M$ value anchored to
    `generic.cas22_detail["C2201xx"]` for a Class-U reactor-island sub-account, or
    a whole-plant M$ value anchored to `generic.costs.<rollup>` for a top-level
    Class-S or Class-P account. Whichever class, the headline lands on `M ×` the
    library's fleet cost for that account, and the `rationale` is written against
    the modular-fleet baseline — never a "conventional 1 GWe plant."
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
| Acoustic ICF (Sonofusion) | Sonofusion Energy | IFE | iter-6/FAIL (3 findings) | E |
| Laser ICF Hybrid Drive (Xcimer Energy) | Xcimer Energy | IFE | iter-5/FAIL (3 findings) | E |
| Orbital Levitated Dipole (Zephyr Energy) | Zephyr Fusion | MFE | iter-5/FAIL (3 findings) | E |
| Laser ICF (HB11 Energy) | hb11 | IFE | iter-4/FAIL (3 findings) | E |
| Negative-Triangularity Tokamak | Firefly Fusion | MFE | iter-4/FAIL (1 findings) | E |
| Muon-Catalyzed Fusion (Acceleron Fusion) | Acceleron Fusion | OTHER | iter-3/FAIL (3 findings) | E |
| Projectile ICF (First Light Fusion) | First Light Fusion | IFE | iter-3/FAIL (2 findings) | E |
| Laser ICF Nanostructured Target (Marvel Fusion) | Marvel Fusion | IFE | iter-3/FAIL (3 findings) | E |
| Polywell (EMC2) | EMC2 | MFE | iter-3/FAIL (3 findings) | E* |
| HTS Tokamak Full HTS | Energy Singularity | MFE | iter-3/PASS | E |
| Helical-Coil Stellarator (HESTIA) | Helical Fusion | MFE | iter-3/PASS | E |
| MTIF (Magneto-Inertial Fusion Technologies) | NearStar Fusion | MIF | iter-3/FAIL (3 findings) | E |
| HTS Compact Tokamak (Commonwealth Fusion / ARC) | Commonwealth Fusion Systems | MFE | iter-2/FAIL (1 findings) | E |
| Laser ICF Liquid-Jet Target (Cortex Fusion Systems) | Cortex Fusion | IFE | iter-2/PASS | E |
| MagLIF (Pacific Fusion) | Pacific Fusion | MIF | iter-2/PASS | E |
| Renaissance Stellarator (Renaissance Fusion) | Renaissance Fusion | MFE | iter-2/PASS | E |
| Spherical Tokamak HTS (Tokamak Energy) | Tokamak Energy | MFE | iter-2/PASS | E |
| Dense Plasma Focus (LPP Fusion) | LPPFusion | MFE | iter-2/PASS | E |
| Laser ICF OEC Architecture (BLF) | Blue Laser Fusion | IFE | iter-2/PASS | E |
| Spherical Tokamak CS-Free PB11 (ENN) | ENN Energy | MFE | iter-2/PASS | E |
| Planar-Coil Stellarator (Thea Energy) | Thea Energy | MFE | iter-1/PASS | E |
| Magnetic Mirror (Pale Blue) | Pale Blue | MFE | iter-1/INCOMPLETE | E |
| FRC w/ Direct Conversion (Helion Energy) | Helion Energy | MFE | iter-1/INCOMPLETE | E |
| QI Stellarator HTS (Proxima Fusion / Stellaris) | Proxima Fusion | MFE | iter-1/INCOMPLETE | E |
| Large-Scale Stellarator | Gauss Fusion | MFE | iter-1/INCOMPLETE | E |
| Magnetic Mirror (Realta Fusion / CoSMo) | Realta Fusion | MFE | iter-1/INCOMPLETE | E |
| Levitated Dipole (OpenStar Technologies) | OpenStar Technologies | MFE | iter-1/INCOMPLETE | E |
| MTF Pneumatic Compression (General Fusion) | General Fusion | MIF | iter-1/PASS | E |
| Sheared-Flow Z-Pinch (Zap Energy) | Zap Energy | MFE | iter-1/PASS | E |
| Laser ICF Fast Ignition (Focused Energy) | Focused Energy | IFE | iter-1/INCOMPLETE | E |
| PB11 FRC (TAE Technologies) | TAE Technologies | MFE | iter-1/INCOMPLETE | E |
| Type One Stellarator (Type One Energy) | Type One Energy | MFE | iter-1/INCOMPLETE | E |
| Heavy-Ion Beam ICF | Intensity Energy | IFE | iter-1/PASS | E |
| Laser ICF Indirect Drive (Inertia Thunderwall) | Inertia Enterprises | IFE | iter-1/PASS | E |
| Laser ICF NIF Commercialization (Focused Energy LIFE-class) | Inertia Enterprises | IFE | iter-1/PASS | E |
| Laser ICF French National (GenF) | GenF Systems | IFE | iter-1/PASS | E |
| State-Backed Tokamak (Neo / ASIPP-class) | Neo Fusion | MFE | iter-1/PASS | E |
| Polomac Magnetic Confinement (Deutelio) | Deutelio | MFE | iter-1/PASS | E |
| Particle Accelerator-Driven Fusion (SHINE-style) | SHINE Technologies | OTHER | iter-1/PASS |  |





## Mode: Feedback Pass

You are improving an existing analysis based on specific feedback from the
assessment agent.

### Existing Analysis
Read this file completely first: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\13-electrostatic-hybrid\analysis.md`

### Feedback to Address
Then read the feedback: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\13-electrostatic-hybrid\iter-2\pre_feedback.md`

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

Sources available: - `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\avalanche-29m-raise-2026.md` (6 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\avalanche-300kv-press-release.md` (6 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\avalanche-cwfest2023-blog.md` (28 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\avalanche-fusionwerx-grant.md` (6 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\avalanche-orbitron-page.md` (3 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\meetings-meeting-dpp24-session-np12-69.md` (0 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\neimagazine-news-avalanche-energy-launches-fusionwerx.md` (0 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\osti-pages-servlets-purl-2582151.md` (0 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\prnewswire-news-releases-avalanche-energy-announces-new.md` (0 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\talk-polywell-orbitron-paper-discussion.md` (2 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\ui-2023aps-dpptp1006m-abstract.md` (0 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-01\sources\ui-2023aps-dppyo8010l-abstract.md` (0 KB)
- `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\iter-03\sources\analyst-patch-pb11-fuel-critical.md` (6 KB)
Dossier (read directly — short and structured): `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\knowledge\concept_research\13-electrostatic-hybrid\dossier.md`

### Instructions
1. Read the existing analysis completely
2. Read the feedback findings
3. For each finding, gather targeted evidence via the per-source subagent pattern
4. Use the Edit tool to make targeted improvements to `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\13-electrostatic-hybrid\analysis.md`
5. Do NOT rewrite sections the feedback doesn't address; maintain existing citations
6. If a finding asks for parameter rows, add them in the correct table position
   with Source and Confidence columns
7. After editing, re-read the modified sections to verify coherence




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
