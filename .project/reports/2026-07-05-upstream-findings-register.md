# Upstream Findings Register — Pipeline De-Risk & Demonstration Epic

**Date**: 2026-07-05
**Status**: Register only — filing is on hold pending user approval. Each entry is written so it can be pasted into a GitHub issue as-is.
**Scope**: every gap, bug, and finding the epic (WI-013 → WI-016) surfaced in the three upstream codebases (`~/1cfe/sysml-codegen`, `~/1cfe/teax`, `~/1cfe/1costingfe`) plus the agentic-mbse validation stack. Sources: the WI-013/014/015 findings docs, the WI-016 comparison, the hypothesis dossier's findings table, the validation-stack gap audit, and `work/learnings/RAW_LEARNINGS.md`.

**Severity key**:

- **blocks-pipeline** — stops or silently breaks the SysML → codegen → teax execution path
- **wrong-numbers** — produces incorrect quantitative output in a tool that serves numbers today
- **friction** — costs time or misleads, but has a route around
- **enhancement** — missing capability, nothing broken

## Summary

| Repo | blocks-pipeline | wrong-numbers | friction | enhancement | Total |
|---|---|---|---|---|---|
| sysml-codegen | 5 | 0 | 3 | 3 | 11 |
| teax | 2 | 0 | 1 | 0 | 3 |
| 1costingfe | 0 | 2 | 0 | 1 | 3 |
| agentic-mbse | 0 | 0 | 2 | 1 | 3 |
| **Total** | **7** | **2** | **6** | **5** | **20** |

One positive finding balances the register and is worth stating in any filing conversation: with live extraction, codegen auto-implemented all six IFE calc bodies correctly from compiled expression ASTs — the AI implementation pass had zero work to do, and the anchors came out bit-exact (WI-015 finding 6).

---

## sysml-codegen

### SC-1 — Constraint predicates are silently dropped from generated pipelines (Phase 6 stub)

- **Severity**: blocks-pipeline (blocks the constraint-checking capability; the drop is silent — no error, no warning)
- **Evidence**: `src/sysml_codegen/extraction/extractor.py:106-107` stubs `constraints = []` with a `# stub for now` comment; `CalculationDefinitionData` has no constraints field (`extraction/data_models.py:96-126`). A standalone extractor exists with zero callers (`extraction/constraint_extractor.py:39`), a constraint→Pydantic translator exists with zero callers (`extraction/constraints.py:41,107`), and its output template body is `# TODO: Implement constraint validation` then `return self` (`templates/constraint_validator.py.jinja2:9-17`). Even if wired in, the extractor reads the expression off the constraint *usage* (`_extract_constraint_expression`, line 96) and regexes variable names (line 120) — for a usage typed by a constraint def, the predicate lives in the def and the usage holds only `in` bindings.
- **How it manifested**: confirmed three ways. WI-013: code reading of the three disconnected pieces. WI-014 live run: `sysml-codegen generate` over a toy with `assert constraint affordable` completed with no error or warning, and `affordable` and its `budget` input appear in no generated artifact. WI-015: the real `assert constraint viability` in `ife_plant.sysml:155` vanishes from the generated package the same way.
- **Workaround**: viability is re-implemented harness-side — the WI-015 sweep applies ηG > 10 in the sweep script, not in generated code.
- **Fix**: wire `extract_all_constraints` into `SysMLDataExtractor` (extractor.py:106) and resolve constraint-usage `in` bindings the same way calc-usage bindings are resolved (`usage_extractor.py:369ff`). Interim minimum: emit a warning when a constraint is encountered and dropped, so the silence stops.

### SC-2 — `return`-style calc outputs are invisible to extraction; generation crashes on legal SysML

- **Severity**: blocks-pipeline
- **Evidence**: `return x : Real = expr` parses in syside as a ReferenceUsage with direction Out, but `extraction/extractor.py:152-153` only inspects AttributeUsage members, so the calc def extracts with `output_attributes = []` and module generation dies at `templates/teax_module.py.jinja2:118` (`output_attributes[0]` on an empty list; jinja2 `UndefinedError: list object has no element 0`). Both forms parse and evaluate in syside; every proven fixture happens to use `out attribute`, so this had never been hit.
- **How it manifested**: WI-014 live check 3 hit it on the toy model; WI-015 hit it six times across the canonical IFE models (`ife_lcoe.sysml:122`, `fusion_cycle.sysml:26`, `hif_economics.sysml:40,60,80,103`) before conversion.
- **Workaround**: convert `return x : Real = expr;` to `out attribute x : Real = expr;` in the models (done for the IFE set; recorded as trap 2 in `work/learnings/RAW_LEARNINGS.md`).
- **Fix**: handle ReferenceUsage/Return members in extraction, or reject `return` with a clear diagnostic instead of crashing in a template.

### SC-3 — Part-usage index keys each usage under its first type, so redefinition subtypes look uninstantiated and their calcs are silently dropped

- **Severity**: blocks-pipeline (silent module loss)
- **Evidence**: `_build_part_usage_index` (`extraction/usage_extractor.py:160-167`) indexes each PartUsage under `next(iter(usage.types))` only. For `part :>> driver : 'HIF Driver'` (`models/designs/hif_ife/hif_plant.sysml:28`), syside returns `types = ['IFE Driver', ..., 'HIF Driver']` — supertype first — so the usage is indexed under 'IFE Driver' and 'HIF Driver' appears uninstantiated.
- **How it manifested**: WI-015 — the `meier_cost` template calc was dropped with "no PartUsage instantiations" until a standalone instance was added.
- **Workaround**: `part hif_driver_instance : 'HIF Driver'` added at `hif_driver.sysml:100`.
- **Fix**: index every type of the usage (or the most-specific declared type), not the first.

### SC-4 — Quoted SysML names leak raw into Python identifiers; generated package is not valid Python

- **Severity**: blocks-pipeline
- **Evidence**: calc defs named with quotes ('IFE LCOE') produce file names (`'ife lcoe'.py`), import paths (`from ife_tea.modules.ife_lcoe.'ife lcoe' import ...`), and class names (`class 'IFE LCOE'Input`) containing quotes and spaces. The registry's import lines *do* sanitize class names (`IFE_LCOEModule`), so the package is also internally inconsistent.
- **How it manifested**: WI-015 finding 3 — the generated IFE package could not import as emitted.
- **Workaround**: `exploration/ife_e2e/sanitize_names.py`, a deterministic post-processor (global textual replace + file renames + py_compile check), run as step 2 of the WI-015 repro.
- **Fix**: apply `sanitize_name` uniformly in module/stencil/schema template contexts, matching what the registry template already does.

### SC-5 — Cross-part references drop to unresolved entry points: no channel wiring between parts, no literal pre-fill

- **Severity**: blocks-pipeline (the biggest functional gap for plant-idiom models)
- **Evidence**: WI-015 finding 4 — all lcoe_calc inputs bound to subsystem attributes (`driver.efficiency`, `chamber.blanket_energy_multiple`, `target_factory.cost_per_target`) and the calc-chain bindings (`driver.cost_per_joule = meier_cost.gamma`) come out "Registry unresolved" and become bare entry points. Generated input JSONs are mostly empty — even literals like `availability = 0.90` don't pre-fill — and the gamma → lcoe.driver_cost_constant edge is absent from the pipeline YAML.
- **How it manifested**: WI-015 — numbers flow through generated code end to end, but one edge of the plumbing is hand-built.
- **Workaround**: the harness closes the loop by feeding run-A outputs (gamma, cost_billions) into run C's inputs (`exploration/ife_e2e/run_anchors.py`).
- **Fix**: resolve cross-part attribute references and calc-output bindings into channel wiring (or pre-filled literals) at extraction. Gates the MFE epic (WI-010/WI-012), where essentially all wiring crosses part boundaries.

### SC-6 — Stencil/docstring expression reconstruction corrupts literals and loses parenthesization — docstrings show wrong math next to correct bodies

- **Severity**: friction (doc-only; executable bodies are generated from compiled ASTs and are correct)
- **Evidence**: SysIDE literal nodes carry a `.function.name`, so they hit the invocation branch of `reconstruct_expression` (`src/sysml_codegen/extraction/expression_utils.py:57-62`) before the literal branch (`:64-66`, which matches node type names SysIDE doesn't use) — literals render as `LiteralRationalEvaluation()` (39 occurrences in the solar_battery snapshot alone). WI-015 added: parenthesization is also lost (`lcoe = a * b + c * d / e * f`).
- **How it manifested**: WI-013 finding 2 (the AI implementation pass had to open the `.sysml` source for every literal); WI-015 finding 5 (a docstring showing *wrong math* next to a correct body is worse than showing nothing).
- **Workaround**: implementers read the SysML source directly.
- **Fix**: correct the branch ordering / node-type matching in `reconstruct_expression` and preserve parentheses, or stop emitting reconstructed expressions in docstrings until they are faithful.

### SC-7 — Derived attributes reading a calc result lose their name at extraction (EXPOSE_PURE drop)

- **Severity**: friction (value survives as the raw channel; only the alias is lost)
- **Evidence**: `attribute total_cost : Real = cost_calc.cost` triggers `WARNING: EXPOSE_PURE total_cost: could not identify instance/output from refs ['cost', 'cost_calc']` and `total_cost` appears nowhere in the generated output; the underlying channel `cost_calc__cost` is still a graph output.
- **How it manifested**: WI-014 live check 3 on the toy (`exploration/construct_validation/toy_plant.sysml`); recorded in the WI-014 findings, construct (a). The def+usage toy shape fails; catf_mfe's baseline sits in a different scoping shape.
- **Workaround**: consume the raw channel name; don't rely on the derived-attribute name appearing in generated code.
- **Fix**: preserve the alias in extraction (or upgrade the warning to say plainly that the name is being dropped and where the value went).

### SC-8 — Warning noise that looks like failure but isn't

- **Severity**: friction
- **Evidence**: (a) "Registry unresolved" lines for design-attribute-bound params (e.g. `...energy_production|p_net_mw`) that resolve correctly as `design_params` entry points — 10 in the WI-013 run, 3 more (benign) in the WI-014 toy run; (b) "EXPOSE_PURE misc_hardware_cost: could not identify instance/output" while the YAML wires `allocation_model__total_allocation` into the rollup correctly (`pipelines/solar_battery.yaml:319`).
- **How it manifested**: WI-013 finding 3 — triage time on every run distinguishing real failures (SC-5, SC-7 emit similar text) from noise.
- **Workaround**: none; read the generated artifacts to check each warning.
- **Fix**: triage — either silence the warnings that describe correct outcomes or confirm they mask a real edge case elsewhere.

### SC-9 — No snapshot-input path in the CLI

- **Severity**: enhancement
- **Evidence**: `sysml-codegen generate` Step 1 is live parsing (`extraction/extractor.py:57` → agentic-mbse `syside_adapter.py:44`); the context build is parse-only (`src/sysml_codegen/cli/__init__.py:622`). A snapshot loader exists but is test-tree only (`tests/helpers/snapshot_loader.py`).
- **How it manifested**: WI-013 — with the syside license expired, generation from the fixture's `extraction_snapshot.json` required a custom harness (`exploration/pipeline_spike/generate_from_snapshot.py`) replicating `run_codegen()` internals plus test-only helpers. The generated registry was byte-identical to the committed baseline, so the path is sound.
- **Workaround**: the WI-013 harness.
- **Fix**: a `--from-snapshot` CLI mode, decoupling generation debugging from the syside license. See SC-10 for a known limit.

### SC-10 — `compilation_results` cannot be rebuilt from a snapshot

- **Severity**: enhancement (rider on SC-9)
- **Evidence**: expression ASTs aren't serialized; the loader documents this at `tests/helpers/snapshot_loader.py:6`.
- **How it manifested**: WI-013 — passing `compilation_results=None`/`{}` still produced a correct package for solar_battery, but any model relying on compiled-expression auto-implementation (which is what made WI-015's bodies zero-work) would lose it in a snapshot-driven run.
- **Workaround / Fix**: serialize expression ASTs into the snapshot if SC-9 is implemented, or document the limitation in the `--from-snapshot` help.

### SC-11 — Module class-name collisions handled via aliasing — confirm intended

- **Severity**: enhancement (informational)
- **Evidence**: 20 aggregation modules in the solar_battery run share class names (`capital_costModule` × 4 scopes, etc.); the generator emits aliased imports + `module_type_override` and it works.
- **How it manifested**: WI-013 finding 4. No failure observed.
- **Fix**: confirm the aliasing scheme is intended behavior and covered by a test, so it doesn't regress silently.

---

## teax

The two blocking entries are one contract gap with codegen seen at two layers: codegen emits primitive-typed exit channels, and teax rejects primitives at both validation and write time. They should be filed together (or as one issue) because one side of the contract must move: teax registers primitive handlers by default, or codegen emits/registers them in the generated package.

### T-1 — ExitPoint cannot write primitive-typed channels; pipeline validation hard-fails

- **Severity**: blocks-pipeline
- **Evidence**: generated YAML declares exit outputs as `RootModel[float]` and `float`, but the default router has no handlers for those names, so validation hard-fails (`packages/teax-simkit/simkit/core/pipeline_validator.py:320`). `execute_pipeline`'s `custom_schema_types` can't express them — it registers class-named Pydantic types only (`simkit/core/pipeline.py:76-100`).
- **How it manifested**: WI-013 — first-ever execution of a codegen-generated pipeline could not pass validation out of the box; WI-015 hit the same wall on the IFE package.
- **Workaround**: harness-built router via `create_output_router_with_json_schemas(["RootModel[float]", ...])` (`simkit/io/output_router.py:276`), reused verbatim in `exploration/ife_e2e/run_anchors.py`.
- **Fix**: register primitive-type handlers in the default router (or settle the contract on the codegen side).

### T-2 — `write_json_model` assumes a Pydantic model; plain-float channels crash at write time

- **Severity**: blocks-pipeline (second layer of the T-1 contract gap)
- **Evidence**: `'float' object has no attribute 'model_dump'` at `simkit/io/writers.py:25`. Codegen emits many plain-float channels.
- **How it manifested**: WI-013 — even after routing around T-1, per-channel JSON writing crashed on scalars.
- **Workaround**: custom scalar `WriteHandler` in the harness (same file as the T-1 workaround).
- **Fix**: handle non-Pydantic values in the writer (or, again, settle the contract on the codegen side).

### T-3 — Workspace packaging is broken for `uv run`; the repo root is not installable

- **Severity**: friction
- **Evidence**: `uv run --project ~/1cfe/teax` fails to build the root — setuptools flat-layout discovery finds `['thoughts', 'packages']` as top-level packages and aborts. The repo's `.venv` is empty (nothing installed).
- **How it manifested**: WI-013 — could not use the repo as a uv project; had to build a side venv.
- **Workaround**: install `packages/teax-simkit` editable into a fresh venv (`exploration/pipeline_spike/.venv-exec/`), which works fine.
- **Fix**: make the root `pyproject.toml` a functioning workspace root (uv workspace members or explicit package discovery config).

---

## 1costingfe

These are the production-number findings. The explorer serves these numbers today. Numeric evidence and repro live in the WI-016 comparison (`work/completed/20260705_WI-016_h2-blind-derivation/comparison.md`); the evaluation script calls the live library at `~/1cfe/1costingfe` (same editable install the concept analyses use).

### C-1 — Stellarator coil cost is priced at the YAML calibration field, ignoring the design point's field (silent ~33% undercount at concept 20a)

- **Severity**: wrong-numbers
- **Evidence**: only the tokamak branch derives `b_center` from the design B (`model.py:1272-1275`); the stellarator branch prices coils at the YAML calibration value `b_center = 6.0 T` (`steady_state_stellarator.yaml:29`) regardless of the spec's field. Numeric: concept 20a (Infinity Two, B = 9 T) gets C220103 = **$4080M**; at its own intended field the same formula gives **$6120M** — a silent 33% undercount whenever a stellarator design point's B differs from 6 T. A tokamak spec would not hit this trap.
- **How it manifested**: WI-016 comparison, adjudication D13 — found only because the blind-derived model uses the actual axis field. Repro: `work/completed/20260705_WI-016_h2-blind-derivation/comparison/compare.py` (live 1costingfe calls), point values in `comparison/results.json`.
- **Workaround**: none in place — concept 20a's served numbers carry the undercount.
- **Fix**: derive `b_center` from the design point's B in the stellarator branch, as the tokamak branch already does.

### C-2 — `compute_beta_N` is exactly half the standard beta convention; Troyon and disruption gates are ~2× permissive

- **Severity**: wrong-numbers (gate/margin outputs, not cost — βN does not feed P_fus or cost)
- **Evidence**: `compute_beta_N` computes β_t = μ0·n(T_e+T_i)/B² (`tokamak.py:117-126`) — exactly half the standard β = 2μ0·p/B² that Troyon's βN limit is defined against (ARC Eq. 2). Factor verified 2.000 numerically: at the ARC design point the key reports βN = 1.15 where the flat-profile conventional value is 2.29 (paper: 2.59). The Troyon gate (βN ≤ 3.5, `tokamak.py:649`) and the disruption-rate margins are therefore ~2× permissive; across the WI-016 grid, conventional βN runs 1.76–4.22, so the low-B corner is beyond the Troyon limit the model believes it is checking.
- **How it manifested**: WI-016 comparison, adjudication D15 — found because the derived model carried the corpus definition. Repro: `comparison/compare.py`; the `beta_N` column in `comparison/grid.csv` is key-computed (i.e., half-convention).
- **Workaround**: none in place.
- **Fix**: add the factor of 2 (use total pressure) in `compute_beta_N`, and re-check any design points that passed the gate marginally.

### C-3 — Magnet cost model is conductor-only: no structure term, no peak-field derating (concedes its own omission)

- **Severity**: enhancement (a modeling gap the code itself acknowledges, not a bug)
- **Evidence**: C220103 is kAm × $/kAm × markup, linear in B (`cas22.py:115-140, 427, 441-444`; `costing_constants.yaml:56,73-75`); the code's own comment concedes peak-field derating and a B²-structure term are "neither of which is modeled here" (`cas22.py:287-289`). Consequence at the ARC point: computed C220103 is $508M where the structure-dominated published total is $5.1–5.2B FOAK, requiring a $1030M NOAK analyst override (`model_setup.py:56-100`). The WI-016 derived virial structure term reproduces the ARC total to −8% and reconverges on the override to 4% (comparison D11/D14) — i.e., the missing term is capturable.
- **How it manifested**: WI-016 comparison D11/D14; also the reason derived-vs-key magnet totals diverge 6–15× across the B grid.
- **Workaround**: per-concept analyst overrides (as concept 01 already does).
- **Fix (suggested)**: add a virial-theorem structure-mass term and peak-field conductor derating; calibration needs cross-machine mass/cost tables (the one-point k_st = 20 does not travel — see comparison D11 caveat).

---

## agentic-mbse (validation stack)

Source: `.project/research/20260705-120000_validation-stack-gap-audit.md`. The context: the epic surfaced SysML patterns that parse cleanly but break evaluation or codegen, and none of them is caught by the 6-level validation stack today. The rules exist only as prose in `work/learnings/RAW_LEARNINGS.md`. The audit's recommendation is one backlog item covering the checks plus negative fixtures.

### A-1 — The 6-level validation stack catches none of the unworkable-SysML traps the epic surfaced

- **Severity**: friction (the gap itself doesn't block, but it leaves blocks-pipeline authoring traps undetected until execution)
- **Evidence** — the audit's gap matrix, with the recommended home for each check:

| Trap | Caught today? | Where the check should live | Check severity |
|---|---|---|---|
| Self-named binding (`in x = x;`) → infinite recursion at syside evaluation | NO | Level 2 (`level2_structure.py`, extend `check_unbound_inputs`): flag bindings whose RHS resolves to the parameter being bound | FAIL |
| Calc `return` style → zero codegen outputs, template crash (SC-2) | PARTIAL — `level6_architecture.py:279-281` checks an output *exists*, not its style | Level 6 (refine `check_calc_def_structure`): distinguish ReturnParameterUsage from out AttributeUsage | FAIL |
| `assert constraint` silently dropped by codegen (SC-1) | NO — Level 4 only counts constraints (`level4_constraints.py:113-114`) | Level 6 (new check): inventory ConstraintUsages, WARN "not executable downstream — apply in harness" | WARN |
| Part def with calcs but no concrete part usage → codegen emits nothing (SC-3 adjacent) | NO | Level 6 (new check): every calc-containing part def in designs/ needs ≥1 PartUsage typed by it | FAIL |
| Derived attr `x = calc.result` dropped at extraction (SC-7) | NO | Primary fix is codegen-side; secondary Level 6 INFO in `check_design_attr_completeness` | INFO/WARN |
| Arithmetic envelope (`exp()`, conditionals need manual impls) | PARTIAL — `adr002.py:25-26` has `SUPPORTED_OPERATORS` but the set is inconsistent (`**` excluded despite being in-envelope; no function-call detection) | Level 6 ADR-002: fix the operator set; detect FunctionInvocation → WARN | WARN |

- **Why the suite passes anyway**: the negative-fixture suite (`tests/fixtures/l6_negative/`) covers missing outputs, not output *style*, and the regression baselines are built from `sample_models/` which contain none of these traps — so the suite passes whether or not the checks exist.
- **How it manifested**: every trap above surfaced only because WI-013/014/015 *executed* the pipeline for the first time; the WI-014 toy needed two syntax fixes to pass live checks that all six validation levels had waved through.
- **Workaround**: the rules live as prose in `work/learnings/RAW_LEARNINGS.md`; authoring correctness currently depends on agents having read that file.
- **Fix**: file one agentic-mbse backlog item ("validation: unworkable-SysML trap checks") implementing the six checks plus a negative fixture for each.
- **Vendor note**: the self-named-binding infinite recursion is arguably syside behavior worth reporting to Sensmetry separately — it parses, passes `syside check`, and only fails at evaluation with an unhelpful "expression took too long" (raising `Compiler.max_steps` does not help; it is genuine recursion). The agentic-mbse Level 2 check is the local defense either way.

### A-2 — The sysml-conventions skill stencil actively teaches the broken `return` pattern

- **Severity**: friction (actively wrong guidance — every model authored from the stencil walks into SC-2)
- **Evidence**: the skill's calc-def stencil shows `return` — the exact style that crashes codegen (gap audit, "Short answer"; SC-2 for the crash mechanics).
- **How it manifested**: the canonical IFE models used `return` in six places (WI-015 model fix 1), consistent with agents following the taught pattern.
- **Workaround**: RAW_LEARNINGS trap 2 documents the rule, for agents that read it.
- **Fix**: change the stencil to `out attribute x : Real = expr;` immediately — this is a one-line doc fix and the audit flags it as the do-now item, independent of the A-1 backlog item.

### A-3 — The no-loops modeling rule is undocumented

- **Severity**: enhancement (documentation)
- **Evidence**: SysML calc defs can't express iteration, so iterative formulas must be pre-solved to closed form — the Hawker DCF became a geometric series (WI-006 DD-3). Nothing in MODELING_GUIDE.md or ADR-002 says so (gap matrix item 7). There is nothing for a validator to detect — the language can't express the broken form — so this is a modeling-guide rule, not a check.
- **Fix**: add the rule to MODELING_GUIDE.md / ADR-002 prose.

---

## Infrastructure note — syside licensing (not a bug)

The syside license is an operational constraint on the whole pipeline, recorded here so filing conversations account for it:

- The previous key expired 2026-05-25 (cached machine file 2026-06-01) and blocked `syside check`, the evaluation API, and all sysml-codegen extraction for the first day of the epic — WI-013 ran from a committed extraction snapshot, and WI-014's live checks and all of WI-015 were license-gated until renewal on 2026-07-05.
- The renewed license is a **single seat, machine-fingerprinted** to this machine, with a **weekly heartbeat** to the vendor server — offline or multi-machine work will hit it.
- The current license record **expires 2026-08-06**. Plan the renewal ahead of the MFE epic's codegen work; the failure mode is a hard import error with no grace period, and there is no local action that renews it (vendor: Sensmetry, syside.support@sensmetry.com).
- Mitigation that would reduce exposure: SC-9 (`--from-snapshot` codegen path) decouples generation debugging from the license entirely.

---

## Reconciliation against the hypothesis dossier register

The dossier's 12-row "Findings filed upstream" table (`modeling_project/HYPOTHESIS_DOSSIER.md`) reconciles cleanly against the findings docs — every row traces to a source finding, and nothing in it lacks evidence. Mapping: dossier rows 1–2 = T-1/T-2; row 3 = SC-1; rows 4–5 = C-1/C-2; row 6 = SC-2; row 7 = SC-3; row 8 = SC-4; row 9 = SC-5; row 10 = SC-6; row 11 = A-1's self-named-binding check (owner split syside/agentic-mbse, handled in A-1's vendor note); row 12 = A-1.

This register carries eight entries the dossier table does not:

- **T-3** (teax workspace packaging) — in WI-013's findings, absent from the dossier table entirely; the only substantive omission.
- SC-7 (derived-attribute alias drop) — in the dossier's H3 riders prose, not its table.
- SC-8/SC-9/SC-10/SC-11 — the dossier acknowledges these in a prose footnote ("WI-013 additionally filed five smaller codegen findings") without table rows; the fifth of those five, literal rendering, is folded into SC-6 here as the dossier's own row 10 extension does.
- C-3 (magnet structure omission) — discussed at length in the dossier's H2 section (D11) but never registered as a filable finding.
- A-2 (skill stencil) and A-3 (no-loops doc) — the stencil is named in the dossier's H1/H3 limits prose; neither has a table row.

Nothing in the findings docs contradicts the dossier, and no dossier row is missing from this register.

---

## Recommended filing order

1. **C-1 and C-2 (1costingfe) first.** These are the only wrong-numbers findings, and 1costingfe serves production numbers today — concept 20a's coil cost is undercounted 33% in output people read, and the Troyon/disruption gates are 2× permissive on every tokamak run. Both have closed-form numeric evidence and a live repro script. File together; they came from the same comparison and the maintainer will want `compare.py`.
2. **A-2 (skill stencil `return` fix)** — not really a filing, a one-line doc change in agentic-mbse; do it immediately, because until it lands the tooling actively teaches the SC-2 crash pattern to every authoring agent.
3. **SC-2 (`return`-style crash)** — legal SysML that kills generation with an opaque template error; cheap fix (or a cheap diagnostic), bit two work items independently, and pairs naturally with item 2.
4. **SC-3 (part-usage type index)** — silently drops modules on any model using redefinition typing, which is exactly the MFE reuse idiom (tokamak/stellarator specializing shared defs). Silent wrongness beats loud crashes in filing priority.
5. **SC-5 (cross-part wiring)** — the biggest functional gap for plant-idiom models and an explicit gate on WI-010/WI-012; file early so the maintainer can weigh in before the MFE epic commits to a harness idiom.
6. **SC-1 (constraint drop)** — the full Phase 6 fix is large, but the interim ask (warn instead of silently dropping) is small and removes the worst property, the silence. Frame the issue that way.
7. **T-1 + T-2 (teax primitive contract, one issue)** — needed by every codegen-generated pipeline; the workaround is stable, so it can follow the silent-failure items, but it should reference the codegen side so the contract decision lands in one place.
8. **SC-4 (quoted names)** — loud failure with a deterministic workaround in hand; include `sanitize_names.py` as the reference implementation.
9. **A-1 (validation trap checks)** — agentic-mbse backlog item with the gap-matrix table as the issue body.
10. **The rest batched**: SC-6/SC-7/SC-8 as friction issues, SC-9/SC-10/SC-11, C-3, A-3 as enhancements — file when the blocking and wrong-numbers queue is clear.

The order's logic: numbers being served wrong beat everything; then stop teaching the broken pattern; then silent failures before loud ones; then contract decisions that gate the next epic; enhancements last.

---

## Addendum (2026-07-05, exp() mini-spike)

Two further sysml-codegen findings from the out-of-envelope spike (`exploration/exp_spike/findings.md`):

| # | Title | Severity | Evidence |
|---|-------|----------|----------|
| C-12 | manual_required stencil renders literals as `LiteralRationalEvaluation()` — values lost | friction (misleads the AI pass) | `expression_utils.py:64` keys on wrong class names, falls to `str()` fallback at `:79` |
| C-13 | Stencil renders binary ops without parentheses — `** (1.0/3.0)` reads as `(** 1.0) / 3.0` | friction (misleads the AI pass) | `expression_utils.py:96` |

Both make the rendered expression in the stencil lossy; faithful AI-pass implementation currently relies on the file:line pointer back to the `.sysml` source (which the stencil does provide). Fix before pointing the AI pass at larger models.
