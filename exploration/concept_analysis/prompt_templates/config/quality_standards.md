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
