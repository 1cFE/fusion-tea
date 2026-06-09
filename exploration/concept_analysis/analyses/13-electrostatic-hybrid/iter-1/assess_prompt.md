# Assessment: Electrostatic Hybrid (Orbitron)

You are evaluating a D1+ concept analysis (and its model setup, if present) for
design-point coherence, override discipline, family-delta concreteness, and
numerical plausibility — against the new pipeline contract.

## Files to Read

### Analysis
Read this file completely: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\13-electrostatic-hybrid\analysis.md`

### Analysis Goals

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


### Override Semantics (the policy the overrides must satisfy)

The overrides you are assessing are authored against this policy — the same one the
analysis and model-setup agents read. Use its vocabulary (the single invariant, the
S/U/P cost classes, the modular-fleet rationale baseline) when judging override
discipline below.

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


### Assessment Checklist

# Assessment Checklist

Evaluate the analysis (and `model_setup.py`, when present) against each criterion
below. A finding means the artifact does not adequately satisfy the criterion.
Group your judgment under the five areas; emit at most 3 findings total, on the
most impactful gaps.

## 1. Design-Point Coherence
- [ ] The top-of-body Design Point block copies the selection fields verbatim
      from frontmatter — name, maturity, `P_native`, grounding — and the analysis
      has **not** silently substituted a different plant or power level.
- [ ] Every quantitative parameter in Section 5 describes that one named plant at
      its native scale. No roadmap aspiration, no different machine, no 1 GWe
      figure smuggled into the native parameter table.
- [ ] `P_native` is identical across the Design Point block, Section 5, and (if
      present) the `model_setup.py` `P_native` constant. The coherence flags
      provided to you report cross-artifact drift — read them.

## 2. Override Discipline
- [ ] Every Override Candidate is a six-field entry with a **canonical** account
      code (no invented `CAS22.1.3`-style codes).
- [ ] Each `enabled` override is evidence-backed: `provenance` honestly reflects
      whether the dollar figure was company-published (`direct`) or analyst-
      assembled (`derived`), and `derived` entries show their arithmetic
      (including any CPI factor) in `rationale`.
- [ ] No override merely re-states a library default, and no uniform financial /
      operating parameter (`availability`, `lifetime_yr`, `interest_rate`,
      `inflation_rate`) appears in `spec` or the registry.
- [ ] The same override `account` appears in the analysis Section 5b YAML and the
      `model_setup.py` `overrides` list with the **same** `provenance` label.
- [ ] Every enabled relative override is in the **modular-fleet frame**: its
      `rationale` anchors to "the library's default for a 1 GWe fleet of this
      device," not a "conventional / monolithic 1 GWe plant," and its value anchor
      matches the account's cost class (Class-U CAS22 sub-account →
      `generic.cas22_detail["C2201xx"]`; top-level Class-S/P →
      `generic.costs.<rollup>`). Citing a monolithic plant as a literature
      *comparable* is fine; using one as the override's *anchor baseline* is a
      finding. **Do not read a scaling failure off the CAS22 sub-account detail
      table** — it shows per-module M$ at every scale, so a `C2201xx` row identical
      at native and 1 GWe is expected; Class-U fleet scaling appears in the
      `C220000` / `CAS22` rollup, not the detail row.

## 3. Override Count vs. Archetype-Fit Grade
- [ ] The count of `enabled` overrides is consistent with the concept's
      archetype-fit grade band (the override-count rubric is given to you):
      `High → 0–4`, `Med → 3–8`, `Low → 6–12`. A High-fit concept with many
      enabled overrides, or a Low-fit concept with zero, is a flag. The count-vs-
      grade check in the coherence flags reports this — corroborate it against
      what you read.

## 4. Family-Delta Concreteness
- [ ] The family-delta prose (Section 7) compares the design point against the
      **fixed** comparables list, not an arbitrary neighbour, and names specific
      subsystems with a cost direction — not generic "this is novel" framing.
- [ ] Each claimed differentiator carries a stated TEA consequence (advantage,
      penalty, neutral, or honestly "unknown").

## 5. Two-Knob Projection & Model Integrity
- [ ] If `model_setup.py` exists: it uses the three-forward helper form — a
      mandatory `generic = generic_reference(...)` line plus
      `native, result_1gw = run_native_and_1gw(...)`, with `model`, `generic`,
      `native`, `result_1gw` at module level — not an inline two-knob `forward()`.
- [ ] `native` / `result_1gw` reflect real parameter-driven computation (CAS
      values are not hardcoded constants or all-zero placeholders); sensitivity
      results, if present, show non-trivial variation.
- [ ] The model's LCOE is plausible (right order of magnitude) for this concept
      type, and its dominant cost drivers match the analysis narrative's emphasis.

You are NOT checking formatting, style consistency, or template-structure
compliance. Focus on coherence, accountability, and numerical plausibility.




## Coherence Flags (computed — interpret, do not just echo)

The pipeline ran cross-artifact coherence checks against this iteration's
artifacts. Read them and factor them into your findings. A `FLAG:` line is a
real discrepancy to investigate; a clean line confirms a check passed.

- FLAG: 13-electrostatic-hybrid: P_native mismatch model_setup=1 vs design_point=0.005
- FLAG: Med archetype fit with 0 enabled overrides (expected 3–8) — a poorer-fit concept with this few corrections suggests the library default is being trusted where the archetype says it shouldn't be.

## Override-Count Rubric

Archetype-Fit is Med → expect 3–8 enabled overrides. Flag in your output if your count falls outside this band.

Check the count of `enabled` overrides (in `analysis.md` Section 5b, and in
`model_setup.py` if present) against this band. A High-fit concept with many
enabled overrides, or a Low-fit concept with none, is a finding unless the
evidence clearly justifies it.


## Concept Landscape

The comparables for this concept are fixed upstream. Use the landscape only to
sanity-check that the family-delta prose engages the *fixed* comparables, not an
arbitrary neighbour.

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


## Instructions

1. Read the analysis completely (and the model output, if present).
2. Evaluate against each checklist area, the coherence flags, and the override
   rubric.
3. Identify the most significant gaps — **at most 3 findings**.
4. For each finding, explain what is insufficient and what should change, and tag
   its `Category` (`analysis` or `model`) by where the fix lands.
5. If the analysis and model adequately satisfy the contract, return `VERDICT: PASS`.

You are NOT checking formatting, style consistency, or template-structure
compliance. Focus on coherence, accountability, and numerical plausibility.

## Output

Write the assessment to this file using the Write tool: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\13-electrostatic-hybrid\iter-1\post_feedback.md`

Use the exact format below.

# Feedback Format

Both the assessment agent and the interactive manage-concept agent produce
feedback in this format. The analysis agent (and, for model-category findings,
the model-setup agent) consume it in feedback-pass mode.

This format is machine-parsed by simple line-anchored scanning. Emit it exactly
as specified — the verdict line and the finding headers are read literally.

## Structure

Each feedback file contains, in order:
1. A **verdict line** — a line reading exactly `VERDICT: PASS` or
   `VERDICT: FINDINGS`, on its own line, with nothing after the token.
   (`VERDICT: PASS — all good` is NOT accepted; put any commentary on a
   separate line.)
2. Zero or more findings (maximum 3 per pass).

## Finding Format

Each finding is a block that begins with a `### F-N:` header (N is an integer:
`### F-1:`, `### F-2:`, …) followed by bold-key bullet lines:

```
### F-N: [Short title]
- **Target:** [Section or artifact the fix lands in — e.g. "Section 5b (Override
  Candidates)" or "model_setup.py overrides list"]
- **Category:** analysis | model
- **Finding:** [What is insufficient, missing, or incorrectly framed]
- **Recommendation:** [What the agent should do differently — specific enough to
  act on without seeing your reasoning]
- **Priority:** blocking | important | minor
```

## Category — exactly two values

Each finding MUST carry a `Category` field whose value is `analysis` or `model`:
- **`analysis`** — the fix lands in `analysis.md` (Design Point block, Section 5
  parameters, Section 5b Override Candidates, family-delta prose, framing).
- **`model`** — the fix lands in `model_setup.py` (the `overrides` list, the
  `spec` dict, sweeps/scenarios, or the two-knob helper call).

There is **no third category.** The new contract's cross-artifact failure modes
route by where the fix lives:
- `P_native` mismatch between the Design Point block and `model_setup.py` →
  `analysis` if the analysis text is wrong, `model` if the model constant is wrong.
- Override `provenance` drift (analysis YAML says `direct`, model says `derived`,
  or vice-versa) → the artifact carrying the wrong label.
- Account-namespace miss (an invented or wrong canonical code) → wherever the bad
  code appears.

## Rules
- Maximum 3 findings per pass — focus on the most impactful issues.
- Findings about numbers focus on *plausibility* (order of magnitude, physical
  reasonableness, design-point coherence), not on re-deriving calculations.
- Each finding must be specific enough to act on without access to your reasoning.
- If the analysis adequately addresses all goals: `VERDICT: PASS` with no findings.

## Example

VERDICT: FINDINGS

### F-1: Override count exceeds the High-fit band without justification
- **Target:** Section 5b (Override Candidates)
- **Category:** analysis
- **Finding:** The concept is graded High archetype-fit (expected 0–4 enabled
  overrides) but the registry enables 7, and three of them re-state the library
  default with no company-published quantity or unit cost in `rationale`.
- **Recommendation:** Disable or remove the three un-evidenced overrides
  (C220105, C220110, CAS24) so the library default stands, leaving only the
  company-grounded departures.
- **Priority:** important

