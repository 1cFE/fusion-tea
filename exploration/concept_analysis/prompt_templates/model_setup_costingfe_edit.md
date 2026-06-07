# 1costingfe Model Update: {{concept_name}}

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `{{output_path}}`.

**Your task**: Read the existing model at `{{prior_model_path}}` and apply
**targeted edits** based on the assessment findings below. Use the Edit tool — do
NOT rewrite the file from scratch, and do NOT restructure conforming code.

## Validator Contract (read this; do NOT go read the validator source)

Your output is judged by four validators run against the bytes on disk. Every
requirement they enforce is stated **here** — exhaustively. **Do not Read or
grep `scripts/lib/validators.py`, `scripts/lib/canonical_accounts.py`, the
costingfe source, or the orchestrator code to "check what's required" — the
contract is below. Reading those files is the single biggest time sink in
this step and is forbidden unless an assessment finding *explicitly* points
at one of them.**

1. **Python syntax** — file must `ast.parse()` clean.
2. **File modified** — the file's SHA-256 must change from the prior model.
   Editing in place satisfies this; copying the file unchanged does not.
3. **Three-forward contract** — module-level bindings, in this order:
   `spec`, `P_native`, `model = CostModel(...)`, `generic = generic_reference(model, spec, P_native)`,
   `overrides = [ ... ]`, `native, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`,
   then `print_cas_breakdown(generic, native, result_1gw, overrides)`. Do
   not inline a two-knob `forward()`. Do not drop `generic`.
4. **Override registry** (the validator that previously sent agents on
   archaeology expeditions — full contract here):
   - `overrides` must be a module-level **list literal of dict literals**
     (`overrides = []` is fine if there are none).
   - Each entry has **all six** fields: `account`, `value`, `enabled`,
     `provenance`, `source`, `rationale`. `provenance ∈ {"direct", "derived"}`.
   - `account` must be one of the concept's canonical accounts (already
     listed in the "Canonical account schema" section below — do not look it
     up elsewhere).
   - **Forbidden rollup accounts** (rejected outright): `C220111`, `C220000`,
     `C220100`, `C220200`, `C220300`, `C220400`, `C220500`, `C220600`,
     `C220700`. To express "this concept assembles more simply," override
     `installation_frac` via `costing_overrides`, not the C220111 dollar
     amount.
   - `value` may be a **number**, a **constant numeric expression** (e.g.
     `260.0 * 1.34`), or an **expression over `generic`** (e.g.
     `0.70 * generic.costs.cas21`). It **MUST NOT** reference `native`,
     `result_1gw`, or `result` (wrong reference frame).
   - Literal `value` must satisfy `|value| <= 5e4` (M$, never raw $).
   - **Disabled** entries (`enabled: False`) must carry a 7th field
     `blocked_by: "<org>/<repo>#NN"` (e.g. `"1cFE/1costingfe#42"`).
   - Every entry must declare `cost_basis: "noak"`. The framework runs
     `noak=True`; `foak`, `conceptual_design`, `vendor_target`, and
     `unspecified` are rejected. Non-NOAK published values: either disable
     with `blocked_by`, or apply a documented learning-curve adjustment in
     `rationale` and declare `cost_basis: "noak"`.
   - No two entries may share an `account`.

## Self-verification budget

You may run the edited model at most **twice** as a self-check:

- Once after your edits to confirm it executes and prints a CAS breakdown.
- (Optionally) once more if a *specific finding* requires you to numerically
  verify a value you changed.

Each `uv run python` cold-boot costs ~30s. Do not write ad-hoc test scripts
under `/tmp/` to probe library internals — if the model runs and the
override registry above is satisfied, you are done.

## Operational constraints

- This is an orchestrated pipeline run. **Do not write to your auto-memory**
  (`~/.claude/projects/.../memory/`) and do not take open-ended exploratory
  actions outside the scope of the findings below.
- If you discover a library bug while editing, **do not** investigate or
  fix it — record it as a `blocked_by: <org>/<repo>#NN` on the affected
  override (file the tracker issue out of band).

## Preserve the three-forward contract

The file already follows the canonical shape; keep it:
1. `spec` dict (design-point inputs only) + `P_native`
2. `model = CostModel(...)`
3. `generic = generic_reference(model, spec, P_native)` — the mandatory
   overrides-off forward (forward 1), the reference a relative override is written against
4. `overrides = [ ... ]` — six-field registry entries
5. `native, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`

with `model`, `generic`, `native`, `result_1gw` at module level and the
`print_cas_breakdown(generic, native, result_1gw, overrides)` call retained. Do
not convert the helper call into an inline two-knob `forward()` (the contract
validator rejects it), do not drop the mandatory `generic` line, and do not
re-introduce `# DEFAULT:` comments or the uniform financial parameters
(`availability`, `lifetime_yr`, `interest_rate`, `inflation_rate`) into `spec`.
**Do not re-introduce power-conversion efficiencies (`eta_th`, `eta_de`,
`eta_dec`) into `spec`** — these are ENUM-driven; the way to express a
different value is to add an upstream ENUM member in costingfe, not a per-
concept override. `f_dec` (DEC fraction) MAY appear in `spec` with provenance —
it's a physics+architecture property, not a hardware-efficiency claim.
A relative override references `generic` (never `native` or `result_1gw`).

**Low archetype-fit concepts: do not empty `spec`.** When the frontmatter
declares `Archetype-Fit: Low`, the prior model may still have a populated `spec`
expressing the concept's actual geometry / physics using canonical kwargs (even
where the archetype isn't a perfect cost match). **Preserve those entries** and
only edit specific fields if a finding calls for it. Replacing a populated
low-fit `spec` with `spec = dict()` is a regression — the library would fall
back to pure archetype YAML defaults that carry zero signal for this concept's
actual machine. Cost-side overrides (the registry below) are where the "Low
fit" caveat properly lives.

**Archetype-specific spec key blocklist (library-bug workarounds).** Until library issues are
fixed, some spec keys must not be passed for specific archetypes — even when the published design
point has a value for them. If the prior model contains any of these keys in `spec`, **remove
them** as part of this edit:
- **DIPOLE**: remove `plasma_volume` if present. The MFE radiation calc treats `plasma_volume`
  as a uniform integrator and over-counts radiation for dipole-peaked profiles. Library issue:
  **1cFE/1costingfe#24**. Document the removal with a brief comment citing the issue.

**Override values are M$, never raw dollars** (validator rejects `|value| > 5e4`).
**Derived rollup accounts cannot be overridden**: C220111, C220000, C220100,
C220200, C220300, C220400, C220500, C220600, C220700. To express "this concept
assembles more simply," override `installation_frac` via `costing_overrides`,
not the C220111 dollar amount.
**Disabled overrides must carry a `blocked_by` field** matching `<org>/<repo>#<NN>`
(e.g. `"1cFE/1costingfe#42"`) so library-side findings route to a tracker
instead of dying in the rationale text.
**Every override must declare `cost_basis: "noak"` (strict).** The framework runs
`noak=True`; any other vintage (`foak`, `conceptual_design`, `vendor_target`,
`unspecified`) is rejected. If your source publishes a non-NOAK value, either
(a) disable + `blocked_by`, (b) apply a documented learning-curve adjustment in
`rationale` and declare `cost_basis: "noak"`, or (c) file a tracker issue.

## Override semantics and the 1 GWe headline (read before editing any override)

This is the same policy the analysis agent authored Section 5b against — the single
headline invariant, the S/U/P cost classes, and the modular-fleet rationale
baseline. Any override you add or change must match it: the value anchored to the
account's own storage shape, and the rationale in the modular-fleet frame (never a
"conventional 1 GWe plant").

{{@config/override_semantics.md}}

**Rules**:
- Preserve all existing sweeps, scenarios, and sensitivity analyses unless a
  finding specifically says to change them.
- Add content incrementally; every change must be traceable to a specific finding
  or a direct consequence of one.
- Any override you add or change uses a **canonical** account code (schema below)
  and the six-field shape; keep `provenance` honest and show derivation arithmetic
  in `rationale`.

{{#if model_feedback}}
## Assessment Findings

Focus on findings tagged `Category: model`. Findings tagged `Category: analysis`
are informational (the analysis agent handles prose), but you may adjust model
parameters if an analysis finding implies the model's assumptions are wrong.

{{model_feedback}}
{{/if}}

## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `{{analysis_path}}`
- **Example (pattern):** `{{example_path}}`
- **README:** `{{readme_path}}`
- **Costing Constants:** `{{costing_constants_path}}`
- **Concept mapping:** `ConfinementConcept.{{costingfe_concept}}`, `Fuel.{{costingfe_fuel}}`

### Canonical account schema (for any new/changed override)

{{canonical_accounts}}

### Canonical `spec` field glossary (for any new/changed spec key)

If your edit touches the `spec` dict (adding/renaming/replacing a field),
the new key MUST come from the glossary below. Read the "Common confusions"
block before editing — most prior errors (concept 05/09 fusion-vs-heating
mix-up, dipole `plasma_volume` regression, kJ-vs-MJ driver-energy mistakes)
trace back to ignoring these warnings.

{{canonical_spec_keys}}

## Output
Write changes to: `{{output_path}}`
