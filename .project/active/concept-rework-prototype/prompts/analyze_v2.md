# Analyze (rework v2) — prototype prompt

You are analyzing one fusion concept to produce a new-shape `analysis.md`. The analysis pipeline has been reworked: every concept must specify exactly **one named plant** (the Design Point), and every LCOE-relevant parameter on the page must describe that one plant. Cost projection to 1 GWe NOAK happens later in `model_setup.py`; you do not touch that here.

## Inputs you are given

**Pre-computed upstream facts (deterministic — do not invent or override):**

- `concept_id`: {concept_id}
- `confinement_family`: {confinement_family}
- `fuel`: {fuel}
- `ConfinementConcept enum`: {enum}
- `archetype_fit_grade`: {fit_grade}    (High = library should fit cleanly; Low = many overrides expected; None = freeform branch, not your concern here)
- `comparables`: {comparables}            (nearest-neighbor concepts pre-computed; you do not edit this)

**Source material:**

- The concept dossier (one named file): {dossier_path}
- The existing `analysis.md` for this concept (use only as a reference for what sources exist; **do not** preserve its plant-mixing or its `# DEFAULT` re-passing): {existing_analysis_path}
- Companion source files cited in the dossier.

## What to produce

Output **exactly** the following markdown sections, in order. Do not add other sections.

### 1. Design Point Block

Exactly one named plant. Pick using this rule:

> The most-mature design with the best published quantitative data. Whitepaper-only long-term targets qualify if they have published geometry + power + fuel. A demo with no electrical output routes to freeform — not your concern here, the orchestrator filters before you run.

If the company has multiple plausible candidates (a near-term demo + a longer-term commercial design), **state both, then pick one and justify**. Do not stitch.

Required fields:

```
Design name:       <e.g. "ARC commercial pilot (2025 CFS public target)">
Company:           <>
Maturity tier:     paper-concept | pilot-demonstrator | proposed-commercial
P_native (MWe):    <net electric power, single named plant, single value — not a range>
Primary sources:   <bullet list of 2–5 source files cited for the values below>
Selection rationale: <2–4 sentences — why this design point and not the other candidates>
```

### 2. LCOE-relevant Parameters (describe the Design Point, 1:1)

A table. Every row must describe the named plant above at its native scale. Do **not** mix in values from a different sized design. If a value is only available for a different design, either (a) note it as "no value for the design point — gap" or (b) state explicitly that you are inheriting it as a stated company target.

| Parameter | Value | Source | Confidence | Note |
|---|---|---|---|---|

Include at minimum: `R0`, `a` (plasma_t), `elongation`, `B0_on_axis`, `B_peak_on_coil`, `fusion_power_MW`, `net_electric_MWe`, `eta_th`, `p_input_MW` (auxiliary heating), and any geometry/physics knob that distinguishes this concept from the archetype baseline.

### 3. Override Candidates

A list of cost-account departures from the 1costingFE library default that this concept's company-published data justifies. **Strict discipline:**

- One entry per account. Account must be a real 1costingFE account (CAS21, CAS22, C220101, ..., CAS27, etc.).
- `value` is the per-module M$ at the Design Point's native scale.
- `provenance ∈ {direct, derived}`:
  - **`direct`** = the company has published this exact $ figure (or a quantity × unit price both directly stated).
  - **`derived`** = you assembled the number from a published quantity and a price the analyst sources elsewhere; *show the arithmetic in the rationale*.
- Do **not** propose an override that is "library default looks low to me." If you cannot cite specific company data, omit the entry.
- If a company-published $ figure is dated, **show the inflation factor explicitly in the rationale** (e.g. "$260M 2014 USD × CPI 1.34 = $348M 2024 USD").
- Expected count for this concept's fit grade — **{fit_grade}**:
  - `High` → typically 0–4 overrides; many overrides are suspicious.
  - `Med` → typically 3–8.
  - `Low` → typically 6–12.

Output as a YAML list inside a fenced block so it can be machine-validated:

```yaml
overrides:
  - account: <CAS code>
    value: <M$ at design-point per-module>
    enabled: true
    provenance: direct | derived
    source: <citation, e.g. "arc-reactor-specifications.md §6">
    rationale: <one short paragraph — show arithmetic if derived>
```

### 4. Family-Delta Notes

A short prose section: what is *different* about this concept versus its archetype family and its comparables (from the upstream `comparables` table above). Only list real architectural differences, not generic "this is a tokamak" prose. These differences are what the override candidates above are meant to capture; if a delta has no corresponding override, say so and explain why (e.g. structural difference is qualitative, no company $ figure available).

### 5. Open Data Gaps (only those affecting cost projection)

A short bulleted list. Do not duplicate the full analysis.md gap inventory — only gaps that *affect the cost projection* of the Design Point at 1 GWe NOAK.

## Anti-patterns (do not do these)

1. **Do not** stitch a near-term demo's geometry to a longer-term commercial target's power. Pick one plant.
2. **Do not** propose overrides that just re-state the library default in different words.
3. **Do not** invent `provenance: direct` for a number you derived; if you did arithmetic, it is `derived`.
4. **Do not** populate or edit the `comparables` field — it is upstream-deterministic.
5. **Do not** include sensitivity sweeps, FOAK scenario branches, or modeling code — those are model_setup.py territory.

## Output format

Output the markdown body only. No frontmatter. No preamble. Begin with `### 1. Design Point Block`.
