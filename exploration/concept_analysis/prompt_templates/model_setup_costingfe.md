# 1costingfe Model Setup: {{concept_name}}

You are generating a runnable 1costingfe model setup script for **{{concept_name}}**
({{company}}). The script must run via `uv run python model_setup.py` and emit an
LCOE estimate.

## The contract in one sentence

The design point is already chosen, the 1costingFE library already carries the
default cost story, and your job is to transcribe the fixed design point into the
**three-forward helper form** and add only the **evidence-backed overrides** the
analysis already discovered — nothing else.

## Step 0: Read the Design Point block from the analysis (primary source)

**Start here.** Open `{{analysis_path}}` and read its `## Design Point` block and
`## Section 5b: Override Candidates` block. These are your primary inputs:
- `P_native` — the design point's native net-electric power (MWe). You do **not**
  choose this; copy it.
- The Section 5 "Design Point Parameters" table — the geometry / physics / power
  inputs for the `spec` dict.
- The Section 5b Override Candidates YAML — the six-field override registry,
  transcribed verbatim into the `overrides` list.

The dossier is a *fallback* only for spec inputs the analysis did not extract — not
the primary source. The rendered Design Point and account schema for this concept,
for reference:

{{design_point_block}}

### Canonical account schema (override codes must come from here)

{{canonical_accounts}}

## Required Reading (supporting)

- **Closest example (pattern to imitate):** `{{example_path}}`
- **1costingfe README:** `{{readme_path}}`
- **Costing constants:** `{{costing_constants_path}}`

## Concept Mapping
- **ConfinementConcept:** `{{costingfe_concept}}`
- **Fuel:** `{{costingfe_fuel}}`

{{#if model_feedback}}
## Assessment Feedback

The following findings were raised by the most recent assessment. Address findings
tagged `Category: model` (they affect what the model computes, sweeps, or
parameterizes). Findings tagged `Category: analysis` may still have model
implications (e.g. a new Section 5 parameter that should also appear in `spec`).

{{model_feedback}}
{{/if}}

## The Three-Forward Structure (emit literally, in this order)

Your script body, after the imports, is exactly these steps: `spec`, `model`,
the mandatory `generic` forward, the `overrides` registry, then one helper call
that returns `native` and `result_1gw`. Do **not** hand-roll the two-knob
`forward()` — the helper owns the overrides-on forwards and is the only accepted
shape. The three forwards are: **`generic`** (overrides off, design scale),
**`native`** (overrides on, design scale), **`result_1gw`** (overrides on, 1 GWe).
Each adjacent pair moves exactly one dimension.

```python
"""1costingfe model: {{concept_name}} ({{company}}).

Usage:
    uv run python model_setup.py              # print results
    uv run python model_setup.py | tee model_output.txt
"""
import sys
from pathlib import Path

# Make the shared three-forward helper importable regardless of where this file
# lives (concept dir or iter-N/ dir): walk up to the scripts/ root.
_SCRIPTS = next(
    p / "scripts"
    for p in Path(__file__).resolve().parents
    if (p / "scripts" / "lib" / "model_setup_helpers.py").exists()
)
sys.path.insert(0, str(_SCRIPTS))

from costingfe import ConfinementConcept, CostModel, Fuel
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
)

# 1. Specification — design-point inputs only, at native scale.
#    Geometry / physics / power. NO library-default re-passing.
spec = dict(
    R0=...,        # arc-reactor-specifications.md §Geometry
    plasma_t=...,
    elon=...,
    B0=...,
    p_input=...,
    # ... only parameters the design point actually specifies
)
P_native = ...     # MWe — copied from the analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.{{costingfe_concept}}, fuel=Fuel.{{costingfe_fuel}})

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6",
     "rationale": "156 t HTS x $44k/kg (2024 CPI) = $6,901M; library default misses HTS unit cost."},
    # Relative example (references the mandatory `generic` line above):
    #   {"account": "C220101", "value": 0.70 * generic.costs.cas21, "enabled": True,
    #    "provenance": "derived", "source": "...", "rationale": "30% structure
    #    cost reduction from modular fab vs library default; 0.70 x library CAS21."},
    # ... one dict per Override Candidate; use overrides = [] if there are none.
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
```

## Hard Rules

1. **`model`, `generic`, `native`, `result_1gw` are module-level** (not inside a
   function or `if`-block). These are the three-forward contract: `generic`
   (forward 1, overrides off), `native` (forward 2, overrides on at design scale),
   `result_1gw` (forward 3, overrides on at 1 GWe). `result_1gw` is the
   standardized cross-concept number.
2. **Step 4 is the helper call**, exactly `native, result_1gw = run_native_and_1gw(
   model, spec=spec, overrides=overrides, p_native=P_native)`, and **`generic` is
   the mandatory standalone line** `generic = generic_reference(model, spec,
   P_native)` (Step 2b). An inline two-knob `forward(net_electric_mw=1000, ...)` is
   rejected by the contract validator. `noak=True` is the helper default — do
   **not** re-pass it.
3. **`spec` carries only design-point inputs.** Do NOT put the uniform
   financial / operating-economics parameters in `spec`: `availability`,
   `lifetime_yr`, `interest_rate`, `inflation_rate` are library-owned and MUST
   NOT appear. The helper sources `availability` / `lifetime_yr` from the library.
4. **No `# DEFAULT: ...` comments.** An account you don't override is already
   handled by the library — do not re-pass or annotate defaults. Cite the source
   for the values you *do* set with a normal inline comment.
5. **Overrides are six-field dicts** (`account`, `value`, `enabled`, `provenance`,
   `source`, `rationale`), `account` from the canonical schema above, `provenance`
   ∈ `{direct, derived}`, no two entries sharing an `account`. `value` may be a
   number, a constant expression (e.g. `260.0 * 1.34`), or a **relative** override
   expressed as a fraction of the library's own cost: reference the mandatory
   `generic` line, e.g. `0.70 * generic.costs.cas21`. `generic` is the library's
   bare overrides-off answer at the design point — do NOT reference `native` or
   `result_1gw` (overrides-on; wrong reference frame) or `result` (the removed
   two-forward name); the validator rejects all three.
6. **Physics-characteristic params** (`eta_th`, `eta_de`) go in `spec` only when
   the design point has a *legitimately different* value backed by archetype-
   specific physics (e.g. Helion direct conversion → non-thermal cycle). A
   company-published "optimistic" number is NOT a reason to override the library
   default. Test: "does the library's archetype default fail to represent this
   concept's physics?" — if no, leave it to the library.
7. **Sweeps / sensitivity `print()` output is allowed** below the steps; only
   `generic`, `native`, and `result_1gw` are the standardized forwards. Do not add
   `scaled_headline` and do not compute sensitivities for `result_1gw`.

## Output
Write the script to: `{{output_path}}`
