# Raw Learnings

Append-only log of modeling discoveries captured via `/record-learning`.

## How This Works

- **User-triggered**: Run `/record-learning` anytime to reflect on session and capture insights
- **Agent-initiated**: Agents may record learnings when they discover something noteworthy

## Review Process

Periodically review entries:
1. Verify correctness (run `syside check` on code examples)
2. Cross-reference with SysML v2 spec if applicable
3. Formalize valuable learnings into `docs/patterns/` documentation
4. Update MODELING_GUIDE.md Pattern Documentation Index

---

## 2026-07-04 — WI-014: The WI-010 plant wiring idiom (calc chaining + assert constraint)

**Context**: WI-014 validated the two constructs the WI-010 plant idiom depends on: usage-level calc chaining (`in x = someCalc.result`) inside a part def, and part-level `assert constraint` fed by calc outputs. Live syside runs were blocked (license expired 2026-05-25, vendor renewal required), so evidence comes from the existing corpus and sysml-codegen's committed fixtures/baselines/snapshots. Full detail: `work/active/WI-014_sysml-wiring-construct-validation/findings.md`.

**The copy-paste idiom for WI-010** (toy at `exploration/construct_validation/`):

```sysml
part def 'Toy Plant' {
    attribute length : Real = 4.0;
    attribute unit_cost : Real = 250.0;
    attribute budget : Real = 5000.0;

    calc area_calc : 'Panel Area' { in length = length; in width = width; }
    calc cost_calc : 'Panel Cost' {
        in area = area_calc.area;      // <- chain: sibling calc's result
        in unit_cost = unit_cost;
    }
    attribute total_cost : Real = cost_calc.cost;   // derived attr from calc result
    assert constraint affordable : 'Cost Within Budget' {
        in cost = cost_calc.cost;      // <- constraint fed by calc output
        in budget = budget;
    }
}
part demo_plant : 'Toy Plant';   // REQUIRED for codegen — see below
```

**What's proven**:
- Calc chaining survives codegen extraction end to end: chain_spike fixture + committed baseline (`sysml-codegen/tests/fixtures/baseline_outputs/chain_spike/computation_graph.json`) wires the upstream calc's output channel into the downstream input; regression-tested.
- Calc usages declared inside a `part def` are projected onto each part **usage** at extraction (`sysml-codegen/tests/fixtures/unresolvable_attr_probe/extraction_snapshot.json`: `my_calc` in the def becomes `...__design_derived_instance__my_calc`). **Gotcha**: a plant part def with no part usage generates nothing — WI-010's plant def needs a concrete design instance.
- Derived attributes reading calc results (`= calc.result`) extract as computed attributes (probe pattern D3; catf_mfe `volume = volume_calc.volume` baseline).

**The gap**: `assert constraint` does NOT survive codegen extraction. `sysml-codegen/src/sysml_codegen/extraction/extractor.py:106-107` stubs constraints to `[]`; the existing `constraint_extractor.py` has zero callers, and it wouldn't resolve constraint-usage `in` bindings anyway (reads the usage's own expression, regexes variable names). So constraints are model-documentation until codegen's Phase 6 lands — viability classification in sweeps (WI-010/012) must be applied in analysis code, not expected from generated code.

**Corpus note**: the epic's "exercised nowhere" was stale — `hif_plant.sysml:199` already chains calcs (in a part usage) and `ife_plant.sysml:155` already has a part-def `assert constraint` (fed by attributes). The genuinely new combination is chaining in a part def + constraint fed by calc outputs; both are in the toy, pending a live `syside check` + Compiler evaluation once the license is renewed.

**Addendum (2026-07-05, license restored — live-run syntax deltas)**: All three deferred checks ran; the constructs stand (parse pass, `total_cost` = 3000.0, chain survives extraction, constraint silently dropped as predicted). The toy needed two syntax fixes to pass live, and both are traps the WI-010 plant model must avoid — note the idiom sketch above contains trap 1 as written:

1. **Never self-name calc bindings.** `in length = length;` (calc parameter shadowing a same-named part attribute) parses and passes `syside check`, but at evaluation syside resolves the right-hand side to the calc's *own* parameter → infinite recursion ("Evaluating expression took too long"; raising `max_steps` doesn't help). Fix: name part attributes distinctly (`plant_length`) so bindings read `in length = plant_length;`. sysml-codegen's chain_spike fixture self-names and extracts fine, so the trap is invisible until something evaluates.
2. **Use `out attribute x : Real = expr;`, not `return x : Real = expr;`, for calc outputs.** Both parse and evaluate in syside, but sysml-codegen only treats `out attribute` as a module output — with `return` the module has zero outputs and generation crashes (`teax_module.py.jinja2:118`, "list object has no element 0").

Two smaller live findings: an `assert constraint` doesn't evaluate to a boolean directly — evaluate the constraint *def*'s predicate `OperatorExpression` with `scope=` the assert usage (two-step); and the derived attribute `total_cost = cost_calc.cost` evaluates but is dropped at extraction (`EXPOSE_PURE ... could not identify instance/output` warning) — the value survives only as the raw channel `cost_calc__cost`. Full detail: findings.md "Live checks — license restored".
