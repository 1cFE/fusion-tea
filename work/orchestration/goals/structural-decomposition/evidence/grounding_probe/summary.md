# Grounding probe — do the structural constructs parse and generate?

Run 2026-09-13 by the grounding session, in the scratchpad, against the installed toolchain (syside via `agentic_mbse.sysml.syside_adapter`, `sysml-codegen generate`, both from the fusion-tea venv). Question: the research report's open question 1 — does the pipeline accept `port def`, conjugated ports, `connect`, `flow of`, nested part usages, and a calc reading a nested attribute through a multi-segment chain?

## What was run

- `structural_probe.sysml` — a `Plant` with `magnet` (holding `coil` and `casing`), `blanket` (a `ThermalPort`), `primary_loop` (the conjugate `~ThermalPort`), a `connect` between them, a `flow of Coolant` through the port items, and a calc whose formals read `magnet.casing.m_casing_ref` and `magnet.n_coils`; a concrete `probe : Plant` binding values through nested `:>>` redefinitions two levels down.
- Parse: `get_syside().try_load_model([file])` — 0 errors, 0 warnings.
- Generate: `uv run sysml-codegen generate --models <dir> --output <dir> --package-name probe_pkg --overwrite` — exit 0, package sealed (`codegen.log`).
- Snapshot: `uv run sysml-codegen snapshot --models <dir>` — six occurrences, `coil` and `casing` nested under `magnet` (`contract_parameters.txt`).

## What it establishes

1. syside parses every construct the report's steps 1–3 need. Two authoring rules surfaced on the way and are worth carrying: `loop` is a reserved word (the plant-closure round already renamed the usage `primary_loop`); on a conjugated port the item directions flip, so a flow into `~ThermalPort` targets its `heat_out` item, and a def-level `attribute x : Real = 50.0` is a binding that a nested `:>>` cannot override — declare without a value (or `default`) and bind in the instance.
2. codegen accepts ports, connections and flows and ignores them: no diagnostic, no parameter, no channel. They are declarative in this pipeline.
3. Nested part usages become nested occurrences, and a nested attribute's qualified name carries the path: `StructuralProbe__probe__magnet__casing__m_casing_ref`. Moving an attribute under a sub-part renames its study key.
4. A calc formal bound through a three-segment chain resolves and the output channel is emitted (`StructuralProbe__probe__casing_total__m_total`).

## What it does not establish

- Behaviour on the real 292-attribute, 76-calc model (readiness diagnostics, the handwritten stages, the twins) — that is the item's own validation.
- Whether the attribute `I_coil`, read only by a plant attribute and not by a calc, is meant to appear as a parameter; it did not. The item's rename ledger will show which moved attributes are parameters.
