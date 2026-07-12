# WI-015 Demonstration Report: SysML Model → Executable Pipeline → Viability Map

**Date**: 2026-07-05 · **Epic**: Pipeline De-Risk & Demonstration, Item 3

## What this demonstrates

For the first time, a fusion cost model authored as a formal SysML v2 system model was mechanically turned into executable Python, run through the teax pipeline executor, checked against verified answers, and swept across its parameter space to map where inertial fusion energy is economically viable. No step required a human to re-derive or re-type a formula.

The subject is the IFE/HIF model set: Hawker's 14-parameter LCOE model (`models/library/analyses/ife_lcoe.sysml`), the fusion-cycle viability relation (`fusion_cycle.sysml`, DI-001), Meier's HIF driver/plant cost chain (`hif_economics.sysml`), and the Osiris heavy-ion plant that binds them (`models/designs/generic_ife/`, `models/designs/hif_ife/`).

## The chain that ran

1. **Live extraction + generation** — `sysml-codegen generate` over the 11-file model set (first live syside parse since the license lapse; first ever of these models). Output: a 6-module computation graph, Pydantic schemas, teax module wrappers, pipeline YAML, and — because live extraction carries compiled expression ASTs — **all six calculation bodies auto-implemented**. The AI implementation pass, which WI-013 needed for 15 stencils, had zero translation work here; every body was reviewed against the SysML and is faithful.
2. **Name sanitization** — one deterministic post-processing step (`exploration/ife_e2e/sanitize_names.py`) because quoted SysML names ('IFE LCOE') leak into Python identifiers, which is a filed codegen gap, not a modeling issue.
3. **Execution** — teax `execute_pipeline()` over the generated YAML + registry, three times (one per anchor point). 8 output channels per run, written as per-channel JSON under `exploration/ife_e2e/outputs/`.
4. **Anchor check** — executed LCOE vs `scripts/verify_ife_lcoe.py` (the verified oracle that mirrors the SysML line-for-line).
5. **Viability sweep** — 11,505 grid points over driver efficiency η (0.02–0.40), target gain G (10–300), rep rate f (1–20 Hz), classified harness-side by the model's viability constraint (ηG > 10) plus a $100/MWh overlay. 0.1 s total, calling the generated module implementations in-process.

## Anchor table (the correctness oracle)

| Anchor | Point | Expected | Executed | Tolerance | Result |
|---|---|---|---|---|---|
| A | Hawker 14-parameter defaults | $252.30/MWh | $252.2999631/MWh | rel 1e-6 | **exact (rel dev 0.0)** |
| B | Realistic HIF: f=5 Hz, η=0.25, E_d=5 MJ, G=100, d=0.05, δ=$0.50 | $68.69/MWh | $68.6902017/MWh | rel 1e-6 | **exact** |
| C | Osiris hif_plant point, γ from Meier Eq. 5 (SV-013 ~$270) | $270.12/MWh | $270.1211779/MWh | rel 1e-6 | **exact** |

Also checked per run: recirculating power fraction; Meier driver cost $0.975B and γ = $68.247/J; Meier COE 4.74 c/kWh at Osiris — Meier 1986 published ~5 c/kWh, so the independent 1988-dollar cross-model output lands inside SV-014's ±15% too. Registered as **SV-023, passing**.

Agreement is bit-exact because the whole model is flat floating-point arithmetic and the generated bodies came from the compiled expression ASTs — the pipeline reproduced the oracle's float operations exactly. The 1e-6 tolerance existed to catch a wrong term or constant; nothing needed it.

One honest asterisk: the model's internal wiring `driver.cost_per_joule = meier_cost.gamma` does not survive codegen (cross-part references become unresolved entry points — filed gap). The harness closes that loop explicitly: run A produces γ from the generated Meier module, run C feeds it back as the LCOE input. The numbers flow through generated code end to end; one edge of the plumbing is harness glue and is labeled as such in `findings.md`.

## What the viability map shows (data/ife_sweep/)

**`ife_viability_eta_gain.png`** — the η–G plane at f = 5 Hz:

- **The knee is real and sharp.** Two boundaries stack in the lower-left: the dashed P_net = 0 line (η_th·M·G·η = 2 — below it the plant consumes more than it makes) and, above it, the solid ηG = 10 line (DI-001). Between them LCOE explodes through $250 → $1000/MWh within a few grid cells: the plant is net-positive but recirculates so much power to its own driver that the economics collapse. That cliff is exactly the "fusion cycle gain" knee the sources describe, now emerging from generated code rather than a textbook figure.
- **Past the knee, the map goes flat.** Once ηG ≳ 25–30, LCOE settles into a broad $50–80/MWh basin and further gain buys little — capital and O&M dominate, not recirculation. Physically: get efficiently past breakeven, then economics is about plant cost, not plasma performance.
- **Driver type sets the required gain.** Read the knee at fixed η: a heavy-ion driver (η ≈ 0.25–0.35) needs G ≳ 40; a laser driver at η ≈ 0.07 needs G ≳ 143. This is DI-001's per-driver gain requirement, visible as one curve.
- The white star is anchor B ($68.69/MWh), sitting in the basin — a sanity pin connecting the map to the checked point.

**`ife_viability_by_freq.png`** — the same plane at f = 1, 2, 5, 10, 20 Hz. The knee position barely moves (it is set by the power balance, not shot rate), but rep rate scales plant power (P_net ∝ f), so higher f pushes the same physics point to bigger, cheaper-per-MWh plants: the attractive share edges up from 63% (1 Hz, at this grid's baseline economics) to 65% and the $100/MWh contour hugs the knee more tightly. At the Hawker-defaults point (f = 0.2 Hz) the same effect explains anchor A's $252/MWh: a 44 MW plant is simply too small for its capital assumptions.

Grid totals: 90.7% of points power-positive, 75.8% viable (ηG > 10), 64.5% attractive (viable and ≤$100/MWh). Non-swept parameters held at the anchor-B baseline; LCOE is reported NaN where P_net ≤ 0.

## Everything that broke, and how it was handled

Full detail with file:line pointers in `findings.md`. Summary:

| # | Break | Handling |
|---|---|---|
| 1 | `return`-style calc outputs invisible to extraction → generation crash | Model fix (6× `return` → `out attribute`); codegen gap filed. Independently confirmed by WI-014 live checks |
| 2 | Redefinition-typed part usage (`part :>> driver : 'HIF Driver'`) not counted as instantiation → Meier driver calc dropped | Model fix (concrete `hif_driver_instance`, the WI-014 rider); codegen gap filed |
| 3 | Quoted SysML names → invalid Python in generated package | Deterministic sanitizer (`sanitize_names.py`); codegen gap filed |
| 4 | Cross-part references unresolved → no gamma→LCOE wiring, empty input pre-fill | Harness feeds run-A outputs into run C; codegen gap filed |
| 5 | Docstring expressions lose literals and parentheses (doc-only; bodies correct) | Noted; codegen gap filed |
| 6 | Constraints not emitted (Phase 6, known) | Viability evaluated harness-side, per plan |
| 7 | teax primitive-channel gaps (known from WI-013) | WI-013 workaround reused |

Three model fixes total (all Level-1 verified, all listed prominently in findings): the `return` → `out attribute` conversions, the `cost_billions` output promotion, and the `hif_driver_instance` usage.

## What this means for the epic

- **H4 (executable exploration) now has its first real evidence on models that matter**: formal model → generated code → verified numbers → a physics-meaningful feasible-region map, with the correctness oracle passing exactly.
- **WI-012 lands on proven ground**: every failure mode it would have hit on MFE models is now characterized with a file:line pointer and either a fix idiom or a filed gap. The modeling idiom for codegen-bound work is now concrete: `out attribute` for outputs, concrete part usages for every def carrying calcs, unquoted-name-safe generation pending the codegen fix.
- **The wiring gap (finding 4) is the one to watch**: until codegen resolves cross-part bindings into channels, plant-idiom models generate modules but not the connections between them.

## Artifact index

- `exploration/ife_e2e/models/` — staged model snapshot (post-fix, as extracted)
- `exploration/ife_e2e/generated/` — the generated package (post-sanitizer)
- `exploration/ife_e2e/{sanitize_names,run_anchors,sweep_ife,plot_sweep}.py` — the harnesses
- `exploration/ife_e2e/outputs/{hawker_defaults,realistic_hif,osiris}/` — executor runs
- `data/ife_sweep/` — `sweep_results.csv` + the two figures
- `work/active/WI-015_ife-end-to-end-demo/{spec,findings}.md` — spec (anchors + tolerance) and findings
- SV-023 in `modeling_project/VALIDATION_MATRIX.md` — passing
