# Assessment: Particle Accelerator-Driven Fusion (SHINE-style)

You are evaluating a D1+ concept analysis (and its model setup, if present) for
design-point coherence, override discipline, family-delta concreteness, and
numerical plausibility — against the new pipeline contract.

## Files to Read

### Analysis
Read this file completely: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\38-particle-accelerator-driven-fusion\analysis.md`

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



## Model Output

The concept has a quantitative LCOE model. Its output is at: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\38-particle-accelerator-driven-fusion\iter-1\model_output.txt`

Evaluate whether:
1. The model's assumptions and parameter values are consistent with the analysis.
2. The 1 GWe projection LCOE (`result_1gw`) is plausible (order of magnitude) for
   this concept type, and the native LCOE is coherent with it.
3. Key cost drivers in the model match the analysis narrative's emphasis.


## Coherence Flags (computed — interpret, do not just echo)

The pipeline ran cross-artifact coherence checks against this iteration's
artifacts. Read them and factor them into your findings. A `FLAG:` line is a
real discrepancy to investigate; a clean line confirms a check passed.



## Override-Count Rubric

(No archetype-fit grade for this concept — the override-count band does not apply.)

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
| Acoustic ICF (Sonofusion) | Sonofusion Energy | IFE | iter-6/FAIL (3 findings) | E* |
| Orbital Levitated Dipole (Zephyr Energy) | Zephyr Fusion | MFE | iter-5/FAIL (3 findings) | E* |
| Muon-Catalyzed Fusion (Acceleron Fusion) | Acceleron Fusion | OTHER | iter-3/FAIL (3 findings) | E* |
| Laser ICF Fast Ignition (Focused Energy) | Focused Energy | IFE | iter-3/FAIL (3 findings) | E* |
| Polywell (EMC2) | EMC2 | MFE | iter-3/FAIL (3 findings) | E* |
| HTS Tokamak Full HTS | Energy Singularity | MFE | iter-3/FAIL (3 findings) | E* |
| Laser ICF NIF Commercialization (Focused Energy LIFE-class) | Inertia Enterprises | IFE | iter-3/FAIL (3 findings) | E* |
| Laser ICF OEC Architecture (BLF) | Blue Laser Fusion | IFE | iter-3/FAIL (3 findings) | E* |
| Spherical Tokamak CS-Free PB11 (ENN) | ENN Energy | MFE | iter-3/FAIL (2 findings) |  |
| HTS Compact Tokamak (Commonwealth Fusion / ARC) | Commonwealth Fusion Systems | MFE | iter-2/FAIL (1 findings) | E* |
| Negative-Triangularity Tokamak | Firefly Fusion | MFE | iter-2/PASS | E* |
| Heavy-Ion Beam ICF | Intensity Energy | IFE | iter-1/PASS | E* |
| Laser ICF Indirect Drive (Inertia Thunderwall) | Inertia Enterprises | IFE | iter-1/PASS | E* |
| Laser ICF French National (GenF) | GenF Systems | IFE | iter-1/PASS | E* |
| State-Backed Tokamak (Neo / ASIPP-class) | Neo Fusion | MFE | iter-1/PASS | E* |
| Polomac Magnetic Confinement (Deutelio) | Deutelio | MFE | iter-1/PASS | E* |
| Helical-Coil Stellarator (HESTIA) | Helical Fusion | MFE | iter-1/INCOMPLETE | E |
| MTIF (Magneto-Inertial Fusion Technologies) | NearStar Fusion | MIF | iter-1/INCOMPLETE |  |

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

Write the assessment to this file using the Write tool: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\38-particle-accelerator-driven-fusion\iter-1\post_feedback.md`

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

