package toy_library {
    private import ScalarValues::*;

    calc def 'Panel Area' {
        doc /*
        Toy geometry calc: rectangular panel area = length * width.
        First stage of a two-calc chain used to validate usage-level
        calc chaining for the WI-010 plant idiom.

        **Source**: work/backlog/epic-pipeline-derisk-demo.md (Item 2)
        **Ref**: WI-009 design.md "Structure ↔ behavior binding"
        **Basis**: Synthetic validation fixture — no domain content
        */

        in attribute length : Real;
        in attribute width : Real;

        // NOTE (live validation 2026-07-05): was `return area : Real = ...`.
        // syside parses and evaluates both forms, but sysml-codegen only
        // recognizes `out attribute` parameters as module outputs — with
        // `return`, the generated module has zero outputs and template
        // rendering crashes ("list object has no element 0").
        out attribute area : Real = length * width;
    }

    calc def 'Panel Cost' {
        doc /*
        Toy cost calc: cost = area * unit_cost. Second stage of the
        chain — its `area` input is bound to `'Panel Area'.area` at
        the usage level inside the part def.

        **Source**: work/backlog/epic-pipeline-derisk-demo.md (Item 2)
        **Ref**: WI-009 design.md "Structure ↔ behavior binding"
        **Basis**: Synthetic validation fixture — no domain content
        */

        in attribute area : Real;
        in attribute unit_cost : Real;

        out attribute cost : Real = area * unit_cost;
    }

    constraint def 'Cost Within Budget' {
        doc /*
        Toy viability constraint: total cost must not exceed budget.
        Validates part-level `assert constraint` whose inputs are
        calc outputs (mirrors 'Net Power Positive' in the WI-009
        plant sketch).

        **Source**: work/backlog/epic-pipeline-derisk-demo.md (Item 2)
        **Ref**: WI-009 design.md "Structure ↔ behavior binding"
        **Basis**: Synthetic validation fixture — no domain content
        */

        in attribute cost : Real;
        in attribute budget : Real;

        cost <= budget
    }
}
