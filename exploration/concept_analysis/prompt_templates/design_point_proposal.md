# Design-Point Proposal Prompt

You propose **one design-point row for one fusion concept**, and write the **reasoning trace** that shows how you got there. Your job is selection only: pick the one named plant that will be the cost-projection target for this concept, fix its `P_native`, cite the primary sources, and document the alternatives you rejected so downstream sensitivity analysis can find them later. You do **not** extract geometry, physics, performance values, or override candidates — those happen downstream in `analyze` against the plant you've fixed here.

Your output is **one markdown document** that both (a) walks the human verifier through your reasoning and (b) embeds the structured YAML row a script will parse into the project's design-point table.

## Inputs

- `concept_id`: {concept_id}
- `concept_name`: {concept_name}
- `confinement_subfamily`: {confinement_subfamily}
- `fuel`: {fuel}
- `archetype_fit_grade`: {fit_grade}

**Research directory** for this concept: `knowledge/concept_research/{concept_id}/`

Structure to use:

```
knowledge/concept_research/{concept_id}/
├── dossier.md                          # Synthesized summary — read this first for orientation
├── iter-NN/                            # Most-recent iteration (highest NN); older iters are superseded
│   ├── sources/
│   │   ├── <source-name>.md            # Extracted source text — THE AUTHORITY for quantitative claims
│   │   └── <source-name>/
│   │       ├── output.md               # Same content, raw extraction
│   │       ├── metrics.json            # Extraction metadata
│   │       └── images/                 # Figures — inspect when a number must be cross-checked visually
```

**Source authority hierarchy** (use in this order when grounding `p_native_mwe` or naming primary sources):

1. The original-document extractions in `iter-NN/sources/<source>.md` are the authority. Cite these as `primary_sources`.
2. `dossier.md` is a synthesized summary. Use it to orient and find which sources are relevant. Do **not** cite the dossier as a primary source if the underlying source file exists — cite the source.
3. Images in `iter-NN/sources/<source>/images/` are necessary when the number you need lives in a table, plot, or equation that text extraction degraded. PDF equations exist as images only.

**Existing `analysis.md`**: `exploration/concept_analysis/analyses/{concept_id}/analysis.md` (if present). Use only as a reference for what sources exist; **do not** preserve its plant-mixing, override claims, or design-point choice. The whole point of this proposal is to make that choice fresh against the source authority.

## Selection rule

> **Pick the most-mature design with the best published quantitative data.** Whitepaper-only long-term targets qualify if they have published geometry, power, and fuel for one named unit. A demo with no electrical output by design (no `P_native`) does not qualify.

Where the company has multiple plausible candidates (a near-term demo + a longer-term commercial design + an aspirational target), the rule chooses **one** — and the rationale must explicitly name the alternatives you rejected and why.

The selection is load-bearing: `P_native` drives `n_mod = 1000/P_native` and dominates the comparison number. A 233 MWe pick produces a materially different 1 GWe LCOE than a 400 MWe pick of the same concept. Do not split the difference; pick one and defend it.

## Grounding confidence

Not all design points are equally well-grounded. Mark each selection with one of three values that reflect **how well the chosen design point traces to published engineering data**:

- **`high`** — design point with reasonable published data. The named plant has documented geometry + power + fuel + at least some engineering parameters (e.g. ARC 2015 Conservative Pilot: 233 MWe net, R0=3.3m, B0=9.2T, FLiBe blanket, full thermal cycle). The cost projection has solid ground under it.
- **`medium`** — design point exists but with minimal data. The named plant has a stated power and fuel, perhaps geometry at a high level, but most engineering parameters are missing or proprietary (e.g. Helion Orion: 50 MWe committed + ARPA-E architectural sketch, but no public reactor specs). The cost projection is grounded but the downstream `analyze` step will have to fill many specification gaps from the dossier or related ENUM defaults.
- **`low`** — no explicit engineered design point; the chosen `p_native_mwe` traces to a back-of-envelope projection, an informal "if we built this it would be ~X MWe" estimate, or a scenario calculation in a physics paper using placeholder efficiencies. The plant has no committed geometry or engineering architecture. The cost projection will be **asterisked** in the comparison view; the row exists to keep the concept in the comparison, with the user warned the number is poorly grounded.

The grade is about **the chosen design point's data quality**, not about the concept's overall maturity, the company's prospects, or the architecture's mappability. A High-fit-grade concept can have `low` grounding (small company with mappable architecture but no published commercial plant); a Low-fit-grade concept can have `high` grounding (Helion Orion — strained PULSED_FRC fit, but the Orion target itself is well-documented within Helion's portfolio of public communications).

### When to route to freeform instead

Route to freeform only when there is **literally no published `P_native` of any kind** for any design in the concept's portfolio — not a back-of-envelope number, not a scenario projection, not an aspirational target. If the sources name *any* electrical output figure traceable to a company source or company-cited paper, pick it as the design point with `grounding_confidence: low` and an honest rationale; do not route to freeform.

A concept whose only published designs are physics demonstrators with no electrical output by design (SPARC, Polaris, LM26) still routes to freeform if there is no commercial design with a stated `P_native` anywhere in the dossier. The test is "any number anywhere," not "any number with engineering parameters."

## Naming the case precisely (multi-phase designs)

Many fusion designs publish **multiple operating phases of the same machine** (e.g. ARC 2015: FNSF phase 190 MWe / Conservative Pilot 233 MWe / Aggressive Pilot 261 MWe — three phases, one geometry, different blanket temperatures). When you pick from such a design:

- **Name the specific phase or case**, not a rounded headline or abstract-level range. `design_name` should be `"ARC 2015 Conservative Pilot phase (Sorbom et al.)"`, not `"ARC 200 MWe reactor"`.
- **`p_native_mwe` is the computed value for that phase**, not the rounded marketing label. If the phase computes 233 MWe and the headline rounds to 200, use 233.
- **Each non-chosen phase is itself a rejected candidate** and must appear in `alternatives_considered` with a directional sensitivity note (see below). A different phase of the same machine is exactly the kind of "what if we picked differently" surface downstream sensitivity analysis cares about.

## Plant-stitching is forbidden

If the company publishes geometry for Design A (e.g. an early 2015 pilot) and a power target for Design B (e.g. a 2025 aspirational target), you may not adopt B's power with A's geometry. Either:

- **Pick A** (geometry + its native power, even if smaller), and call out the power target as a forward-looking aspiration that is **not** the design point.
- **Pick B** (if B has its own published geometry + power), and treat A as a precursor that is **not** the design point.

If neither A nor B is internally complete, pick the most-complete and flag the gaps in the rationale. Do not invent or transfer values across designs.

## Multi-module commercial designs — `P_native` is the module, not the plant

If the design's natural architecture is multiple modules in tandem (e.g. General Fusion's commercial plant is two 150 MWe modules totaling 300 MWe; some MTF/IFE concepts assume per-shot replication at the chamber level), `p_native_mwe` is the **per-module** electric power, not the plant total. The two-knob 1 GWe projection scales the reactor island linearly by `n_mod = 1000 / p_native_mwe`, so picking the natural module size keeps each module at its validated operating point. Picking the plant total would imply scaling the architecture's module up to 300 MWe, which the design doesn't describe.

Mention the architecture in `selection_rationale` (e.g. "150 MWe per module, two-module commercial plant; P_native is the module size to preserve the architecture's natural replication unit").

## Maturity tier vocabulary (pick exactly one)

- `paper-concept` — design exists as published whitepaper / journal article; no hardware built at scale. Includes long-term commercial targets that are well-specified but not yet engineered.
- `pilot-demonstrator` — design is the company's near-term first-of-kind production unit (often sub-commercial scale); has published engineering parameters at hardware-design level.
- `proposed-commercial` — design is a published commercial-scale plant with documented engineering parameters.

If a concept's most-mature design is a sub-scale physics demonstrator (no net electricity by design, e.g. SPARC), that design does **not** qualify as the design point — route to freeform.

## Output format

Output **one markdown document** following the exact structure below. No preamble before the `#` heading, no postscript after the final section. The document must begin with the literal first line `# Design Point Reasoning Trace — {concept_id}`.

The document carries two readers:
- A **human verifier** reading the prose sections to evaluate whether your selection is principled.
- A **CSV-ingestion script** parsing the YAML block inside section 3 into one row of `design_point.csv`. The script will fail loudly if the YAML is missing or malformed.

### Required structure

````markdown
# Design Point Reasoning Trace — {concept_id}

## 1. Sources walked

A bulleted list of every source file you opened (not just cited). One line per source, repo-root-relative path, with a short note on what it provided. Example:

- `knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md` — Sorbom et al. 2015 ARC paper; defines three operating phases with per-phase Pnet
- `knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/cfs-2025-2026-updates.md` — CFS public communications on the 400 MWe Virginia commercial target

## 2. Candidates surfaced

Enumerate every named design candidate you found in the sources, including different operating phases of the same machine. For each, state: what `P_native` it implies (or "no electrical output"), what its maturity status is, and what's published for it. This is the inventory the selection draws from. Do **not** filter here — list everything you considered, including ones you will reject in section 3.

## 3. Selection

State which candidate you picked and the rule application, then emit the structured YAML row. The prose is what the human verifier reads; the YAML is what the script parses.

Use this YAML schema exactly:

```yaml
proposal:
  concept_id: <copy from input>
  design_name: <specific named design + phase/case if applicable, e.g. "ARC 2015 Conservative Pilot phase (Sorbom et al.)">
  maturity_tier: paper-concept | pilot-demonstrator | proposed-commercial
  grounding_confidence: high | medium | low   # see "Grounding confidence" section above
  p_native_mwe: <single number — the computed value for this phase, not a rounded headline>
  primary_sources:
    - <repo-root-relative path>
    - <at least 2 entries; each must be a source that grounds geometry, power, OR fuel for THIS plant>
  selection_rationale: |
    <2-4 sentences: which candidate, why it beat the alternatives by the selection rule.
    Name the specific phase/case if multi-phase. If the architecture is multi-module,
    say P_native is the per-module value.>
  alternatives_considered:
    - design: <name + phase/case of rejected candidate>
      reason_rejected: <one phrase>
      sensitivity_implication: <one sentence, DIRECTIONAL only: "if picked instead,
        P_native would be higher/lower → fewer/more modules at 1 GWe → 1 GWe LCOE
        would shift down/up. Worth probing later if X." Do NOT compute numbers.>
    - <one entry per rejected candidate. Different phases of the same machine each
      get their own entry. If there were genuinely no other candidates, write one
      entry with design "(no other candidates)", reason "single-design company",
      sensitivity_implication "n/a".>
```

## 4. Open questions

A short bulleted list — gaps in the dossier that affect this selection. What would change the call if it were resolved (e.g. "if CFS publishes engineering parameters for the 400 MWe Virginia design, revisit P_native"). These are explicit watch-items, distinct from the rejected-candidate sensitivities: those are "could probe later"; these are "would force a re-selection."
````

### Sensitivity implications — directional only

The `sensitivity_implication` field for each rejected candidate captures **direction and reason to revisit**, not arithmetic. Examples:

- Good: `"if picked instead, P_native rises substantially → fewer modules at 1 GWe → 1 GWe LCOE shifts down. Worth probing if higher-temp blanket materials mature."`
- Good: `"P_native rises substantially (400 vs 233 MWe) → fewer modules → 1 GWe LCOE shifts down. Eligible for design-point revisit if CFS publishes engineering parameters."`
- Bad (numeric): `"n_mod_1gw drops from 4.29 to 3.83; per-module fixed costs spread over fewer modules → LCOE drops 8%."`
- Bad (skipping it): `"n/a"` unless truly n/a (e.g. SPARC with no electrical output)

The downstream sensitivity-analysis step will do the arithmetic. Your job is to flag which branches are worth the arithmetic.

### Special case — route to freeform

If after reading the dossier you conclude that no design in this concept's portfolio has a `P_native` (the leading designs are physics demonstrators with no electrical-output design point), the YAML in section 3 takes this alternate shape instead:

```yaml
proposal:
  concept_id: <copy from input>
  route_to_freeform: true
  reason: <2-3 sentences explaining which designs you considered and why each lacks an electrical design point>
  designs_considered:
    - design: <name>
      reason_no_p_native: <one phrase>
```

Sections 1, 2, and 4 still apply; only section 3's YAML schema changes.

## Discipline reminders

1. **Output begins with `# Design Point Reasoning Trace — `** and no other text comes before it. No "I have all the data needed..." preamble.
2. **The YAML block in section 3 is parsed mechanically.** It must be a valid YAML document inside a triple-backtick `yaml`-fenced block. The script will fail loudly if the YAML is malformed or missing.
3. **`primary_sources` requires at least 2 entries.** If you can only find one, you have not walked the source tree carefully enough — go back to section 1 and look harder. Companion sources for cross-checking geometry, power, or fuel always exist for High-fit concepts.
4. **`p_native_mwe` is a single number.** Not a range. Not "200-400". If the published value is a range or the design has multiple phases, pick the specific phase and use its computed value (see "Naming the case precisely" above).
5. **Citations are repo-root-relative paths**, not URLs or dossier section names. Format: `knowledge/concept_research/{concept_id}/iter-NN/sources/<source>.md`. If you cannot point a citation at a specific source file, you are likely citing the dossier summary — drill down to the source.
6. **`alternatives_considered` must list every candidate you surfaced in section 2** that you did not pick — including different phases of the same machine. Each gets a directional `sensitivity_implication`. If you list a candidate in section 2 but not here, the verifier will flag the omission.
7. **Do not propose geometry, physics, performance, override candidates, or LCOE-relevant parameters.** Those are out of scope. The trace covers selection only.
8. **Do not invent `P_native`.** If the source doesn't state a net electric power for the design you've chosen, either pick a different design that does, or route to freeform. The value must trace to a primary source citation in `primary_sources`.
9. **`grounding_confidence` is honest about the chosen design point's data quality.** If the only number you could find is informal, use `low` and say so — don't dress up a back-of-envelope projection as if it were an engineering whitepaper. The asterisk in the comparison view exists precisely so this honesty is preserved.
