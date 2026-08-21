---
date: 2026-08-20T22:18:35-07:00
researcher: Claude
topic: "Reconciling the stellarator-mbse-demo worktree with main: what diverged, how to merge, what the models need after the recent PRs, and how to prove the study work before and after"
tags: [research, stellarator-demo, run-study, sysml-codegen, teax, merge-plan, d5-migration]
status: complete
last_updated: 2026-08-21
---

# Research: Stellarator demo worktree → main reconciliation plan

**Date**: 2026-08-20 22:18 PDT
**Researcher**: Claude
**Research Type**: Codebase / Integration

## Research Question

The demo worktree (`~/1cfe/fusion-tea-stellarator-mbse-demo`, branch `feat/stellarator-mbse-demo`, epic `.project/backlog/epic_run_study_capability.md`) has been building study capability and demo material while `main` shipped the stop-parser pins and the D-5 model migration. Four questions:

1. What was developed on the demo branch since the common fork, and what did `main` do meanwhile?
2. How do we merge cleanly: demo → main, or bring the demo branch up to date and PR it?
3. The demo's SysML v2 models are likely affected by the recent PRs. What model updates are needed, what workaround glue can go, and what's actually blocking?
4. How do we demonstrate the codegen + study work before and after the migration, so nothing regresses silently?

## Summary

- **The fork is clean and the textual merge is nearly trivial.** Common ancestor is `91d03a7f` (PR #101, 2026-07-12). Demo: 138 commits, 846 files. Main: 42 commits, 71 files. A dry merge (`git merge-tree`) produces exactly three conflicts: `.project/CURRENT_WORK.md`, `.project/backlog/BACKLOG.md`, `uv.lock`. `pyproject.toml` auto-merges. No model file is touched on both sides.
- **But there is one structural collision.** Main's D-5 spine test (`tests/models/test_self_binding_replacement.py:101-103`) copies the *whole* `models/` tree and generates it. The demo added 11 MFE model files to `models/` carrying 94 self-named bindings (`in R = R`), which the exact route refuses. Merging as-is turns that licensed, fail-not-skip test red. Recommendation: land the demo work with the MFE models staying only in the self-contained staged twin (`exploration/stellarator_e2e/models/`), and promote them into `models/` in the migration PR once they generate clean.
- **The glue can all go — after regeneration.** A live probe on the pinned codegen (`8a758e92`) + teax main (`744745f`) generated, sealed, loaded, and executed a model carrying all five glue shapes (BOP alias repoint, schema fillers, CAS28 constant, `n_mod` default, cross-part CAS27). Every rung is unnecessary on the exact route, and the g1 hand-edits are now structurally refused (post-seal edits to `pipelines/**` or `inputs/**` fail the manifest). The adapter's own deletion condition ("stock loader accepts with `strict=True`") becomes satisfiable.
- **The stellarator model does not regenerate today, even after the D-5 rename.** The rename is mechanized and the tool's four preconditions pass on this tree (probe). Behind it sit three new refusal classes: six scalar function calls (`sqrt`/`max`/`min`/`floor`) the exact route doesn't admit (owner-filed P2 upstream, no fix in the pin); unit-comment collisions from scraped `//` comments on formals; and four calc usages whose positional parameter redefinition skips a leading defaulted formal. Past those, unknown. Plus: an owner hold on editing the stellarator model still stands in codegen's BACKLOG.
- **Recommended shape: three PRs in sequence.** (1) Merge `main` into the demo branch, land everything non-model on `main` now (no model risk). (2) A model-migration item: D-5 + the three blockers, iterated against `sysml-codegen generate` until it seals at 2.0.0. (3) Regenerate, delete the adapter and glue, re-pin the manifest, run the study on the stock route with before/after evidence. RUN-STUDY Item 6 then runs on the stock route instead of the era adapter.

## Detailed Findings

### 1. What diverged since the fork

**Fork point**: `91d03a7f` (merge of PR #101, 2026-07-12). Demo tip `6689400d` (2026-08-20). Main tip `ebe4d376` (2026-08-20). `git rev-list --left-right --count main...feat/stellarator-mbse-demo` → 42 / 138.

**Demo side (846 files, +108,979 / −115 lines)**, grouped by what it is:

| Group | What | Where | Notes |
|---|---|---|---|
| MFE / stellarator models | 11 new `.sysml` files (7 analyses, 1 cost_structure, 3 designs) + one additive enum member `mfe_divergent` in `economic_parameter.sysml` | `models/library/analyses/mfe_*.sysml`, `models/library/cost_structure/mfe_power_core.sysml`, `models/designs/generic_mfe/`, `models/designs/stellarator_09/` | 94 self-named bindings: 89 in `mfe_plant.sysml`, 5 in `stellarator_plant.sysml` |
| Staged model twin | Self-contained copy used for generation (own `foundation/`, `cost_structure/`, `analyses/` — no IFE files) | `exploration/stellarator_e2e/models/` (14 files) | Byte-identical to `models/` except two "Item 10" comment blocks in `mfe_plant.sysml` (staged lines 402-406, 564) |
| Generated, sealed package | 140 files; `pkg/stellarator_tea` is a symlink to `generated/` | `exploration/stellarator_e2e/generated/` | codegen `06d95f8`, teax `07eb0ac`, 2026-07-25 (WI-029 plan.md:475-480, 513); `runtime_contract_version 1.0.0`, `generator_version 0.1.0` |
| Handshake + oracle | Pure-Python whole-plant recompute and the 1costingFE handshake | `exploration/stellarator_e2e/verify_stellaris.py`, `run_stellaris*.py`, `HANDSHAKE_REPORT.md` | Headline: total $16,129,706,216.04 / LCOE 275.264220 (`run_stellaris_single.py:77`), 5/5 verdicts satisfied |
| Proof-of-life study | 948-point (R, a) grid + 19-point availability sweep, report | `exploration/stellarator_e2e/study/` (CSVs, `verification_summary.json`, `report.html`, `synthesis.md`) | Stores under `study/_work/` are gitignored |
| Run-study capability (Items 1–5) | Skill + runbook + record template; generic tools; package manifest; era adapter; 273 tests | `.claude/skills/run-study/`, `scripts/study/{indicators,manifest,identity,common,preflight,verify}.py` + schemas, `exploration/stellarator_e2e/studies/{manifest.json,era_adapter.py,oracle_entry.py,promotion_equivalence.py,ANNEX.md}`, `tests/study/` (26 files) | Item 6 (A/B consumer + policy cutover) not started; waits on owner Align |
| PM records | 9 `.project/active/` items, 2 epics, 5 research docs, 1 report, 13 `work/completed/` WIs, 6 audits, 6 orchestration trails, `work/BACKLOG.md`, `work/backlog/epic-mfe-cost-modeling.md` | `.project/`, `work/` | Two PM systems both touched; no overlap with main's edits |
| Hold-out | ARIES-CS quarantine (4 sealed PDFs + protocol) | `knowledge/holdout/` (7 files) | |
| Test rewrites | WI-026 re-recorded stale model tests | `tests/models/test_foundation.py`, `test_power_balance.py` | 30 passed / 13 skipped |
| Config | `jsonschema>=4.26.0` dep; `slow` pytest marker; `.gitignore` negation for the skill + `exploration/*/outputs/` | `pyproject.toml`, `.gitignore` | |
| Noise | 126 tracked files of `.orchestrate-logs/`; 2 IFE osiris run-output dirs (16 files) | `.orchestrate-logs/`, `exploration/ife_e2e/outputs/osiris/ife-tea-results-{5f077ef7,b8433ea7}/` | Candidates to drop in the merge |

**Main side (71 files)**:

- Stop-parser shipment (PR #102): `pyproject.toml` switched from editable path sources to git-SHA pins (`agentic-mbse==0.1.3`, `1costingfe==0.1.0`, `sysml-codegen==0.1.1`); `tests/test_dependency_provenance.py` asserts exactly those sources and SHAs (`:54-76`); `tests/test_codegen_teax_acceptance.py` and `tests/test_occurrence_mutation_teax.py` drive real teax from `STOP_PARSER_TEAX_ROOT` (`:109`, `:170`).
- D-5 self-binding migration (`9e1ff87b`): 15 `in x = x` bindings renamed to `in x_in = x` in the IFE models, in both `models/` and `exploration/ife_e2e/models/`; plus `tests/models/test_self_binding_replacement.py`, which copies the whole model set (`:101-103`), generates it (`:106-114`), and pins a 23-entry-point / 18-design-attribute census. Licensed; fails, never skips (`:12`).
- IFE regeneration and the CONSTRAINT-EXEC fusion items (Items 8, 9, 14 Appendix C), all under `exploration/ife_e2e/`.
- Docs: CURRENT_WORK, BACKLOG, two reports, two research files, `docs/concept-pipeline/dependency-graph.html`.

The demo's canonical `models/` still carries the pre-D-5 IFE files (the 15 sites), because the demo never touched them. Merging main brings the rename in without conflict.

### 2. Merge mechanics

**Dry merge** (`git merge-tree --write-tree --name-only main feat/stellarator-mbse-demo`):

```
CONFLICT (content): .project/CURRENT_WORK.md
CONFLICT (content): .project/backlog/BACKLOG.md
CONFLICT (content): uv.lock
Auto-merging pyproject.toml   (clean)
```

Resolution is mechanical:
- `CURRENT_WORK.md`: take main's rewritten version (2026-08-20) and add one section for the stellarator/run-study state.
- `BACKLOG.md`: union. Main added one row (run_analysis CLI spec) and a date; the demo added two In-Progress rows (Stellarator MBSE Full Demo, Run-Study Capability) and one epic section.
- `uv.lock`: do not hand-merge. Regenerate from the merged `pyproject.toml` (`uv lock`). The merged file is main's git pins plus the demo's `jsonschema` line; `test_dependency_provenance.py` only inspects the three pinned packages, so the extra dependency is fine.

**Direction.** Bring the demo branch up to date (merge `main` into `feat/stellarator-mbse-demo` in the demo worktree), then PR it into `main` with a merge commit. Reasons:
- 138 commits with their own PM trail; a rebase would rewrite history the `work/completed/` records cite by SHA (e.g. `a92251a7`, `d9ced308`, `316fc3a0`, `f22bd288`).
- The demo worktree already has the era teax worktree and the exec venv wired in by absolute path; running its suite after the merge proves the combined tree in the environment it was built for.
- Branch protection requires an owner admin merge anyway (`! gh pr merge <n> --repo 1cFE/fusion-tea --merge --admin`).

**The one structural collision.** Main's `tests/models/test_self_binding_replacement.py` generates the whole `models/` tree. With the demo's MFE files present, the run hits `SI_SELF_BINDING` on 94 sites and, even after a rename, the generated package's entry-point census changes (the test pins 23/18 for IFE). Three ways out:

| Option | What | Cost |
|---|---|---|
| A (recommended) | In the merge PR, keep the MFE models only in the staged twin `exploration/stellarator_e2e/models/` (`git rm` the 11 files from `models/` in the merge commit; keep the additive `economic_parameter.sysml` enum member). Promote them back into `models/` in the migration PR, alongside a test change that scopes each model set to a design family. | Temporarily contradicts MR-3's "library definitions live in `models/library/`" for MFE. The package was never generated from `models/` anyway (WI-029 plan.md:274, 513), so nothing executable changes. |
| B | Keep MFE in `models/`; change the spine test to copy an IFE-only subset. | Edits main's spine proof in a PR whose subject is the demo; the subset list is a new maintenance surface. |
| C | Do the D-5 rename + fix the three blockers before merging. | Couples a ~109k-line docs/tooling landing to an open-ended model-migration effort; main stays without the study tooling for weeks. |

Also check in the merge: the `economic_parameter.sysml` enum addition is shared with IFE (`models/designs/generic_ife/ife_subsystems.sysml` imports it). Run the spine test after the merge to confirm the IFE census and byte-identity still hold.

**Small things to settle in the merge PR:**
- `.gitignore`: the demo's `exploration/*/outputs/` rule would hide future IFE fixture outputs (main tracks `exploration/ife_e2e/outputs/**` as fixtures). Narrow it to `exploration/stellarator_e2e/outputs/`.
- Drop `.orchestrate-logs/` (126 tracked files of agent run logs) and the two IFE osiris result dirs the demo branch picked up.
- `tests/study/conftest.py:267-269` hardcodes `/home/reid/1cfe/teax-v1-era`; tests skip cleanly without it (or fail under `STUDY_REQUIRE_ERA=1`). Acceptable on main until Phase 3 deletes the era dependency.

### 3. What the models need after the recent PRs

Source for this section: a live probe run by the upstream-status agent against codegen `8a758e92` (fusion-tea's pin; the 75 commits after it on codegen `main` touch no `src/` or `scripts/` file) and teax `744745f`, in the scratchpad only. Four probes: the D-5 tool on the demo tree; the exact route on the renamed tree; a 25-line model isolating a new refusal; a 50-line model carrying all five glue shapes, generated → sealed → loaded by teax's `ProvisionalPackageLoader` → executed by `execute_pipeline`.

**3a. Required: the D-5 rename (mechanized).**
- The exact route refuses `in R = R` as `SI_SELF_BINDING` (`sysml-codegen src/.../elaboration/elaborate.py:2199-2202`).
- Tool: `sysml-codegen/scripts/make_d5_variant.py --root <models> --scratch <dir> --formals <names>`; customer mode refuses on four preconditions before writing (`:437-509`). Probe on the demo tree: *114 binding sites, 112 declaration blocks across 75 formals — preconditions clear — strip check: 0 problems* (the 114 = 94 MFE + 15 pre-D-5 IFE + 5). Note the tool only builds into scratch; replacing the originals is a separate step, and both the canonical and staged trees need it.
- Already filed upstream as `[STELLARATOR-D5-MIGRATION]` P2 with "needs an owner before any edit" (codegen `BACKLOG.md:403-412`). That hold must be released.

**3b. Blockers behind the rename (found in order; each stops the run).**

1. **Scalar function calls — `SI_EXPRESSION_SOURCE_UNSUPPORTED`.** Only `NumericalFunctions::sum` is admitted (`agentic-mbse src/agentic_mbse/sysml/reference_use.py:395-428`). Six sites: `RealFunctions::sqrt` at `models/library/analyses/mfe_plasma_scaling.sysml:194`; `max`/`min`/`floor` at `mfe_account_costs.sysml:816, 820, 830-832`. Upstream: `[SCALAR-FUNCTION-VOCABULARY]` P2, `[OWNER 2026-08-18]`, annotated "no existing fixture or Fusion model needs them" (codegen `BACKLOG.md:36-41`) — the stellarator does. Codegen's `docs/architecture/modeling-assumptions.md:241-243` says functions need a calc def. Decision needed: wait for upstream, or rewrite the six sites model-side.
2. **Unit-comment collisions — `SI_RENDERING_COLLISION` "conflicting projected metadata"** (`project.py:497-504`). Unit text is scraped from trailing `//` comments on formals (`extraction/feature_metadata.py:81-110`); consumers of one entry point disagree (e.g. `availability` reads `'Capacity'` from `mfe_lcoe_dcf.sysml:31` `// Capacity factor [0..1]`, `'i'` elsewhere, `None` elsewhere). Stripping the 808 comment lines in the scratch copy cleared the class. Fix: harmonize or remove trailing comments on formals.
3. **Positional parameter redefinition — `SI_RENDERING_COLLISION` "distinct inputs render to one parameter name"** (`project.py:674-685`). A calc usage that skips a *leading* defaulted formal lands each binding one slot early. Four usages: `mfe_plant.sysml:116` (`geom`) and `:141` (`rb`) skip `pi` (`mfe_plasma_scaling.sysml:30/71`); `mfe_plant.sysml:530` (`supplementary`) skips four rate formals (`mfe_account_costs.sysml:559-590`); `stellarator_plant.sysml:855` (`wall_load_calc`) skips `ash_frac` (`mfe_plasma_scaling.sysml:231`). Fix: declare defaulted formals last, or bind all. **Not filed in codegen.** This is also a premise-grade finding: the legacy route matched by name so the old package was numerically right; on the exact route these four would be mis-wired if the collision check did not stop them. It should be filed upstream whichever way the model is fixed.
4. Beyond #3: unknown. The probe stopped there. Scale: 28 library calc defs carry defaulted formals; 42 calc usages across the two design files.

**3c. Contract versions.** Current codegen seals `runtime_contract_version 2.0.0` (`contracts/versions.py:11`); teax main accepts exactly `{"2.0.0"}` (`teax packages/teax-simkit/simkit/evaluation/package_load.py:33`, enforced `:133-139`, "replaced, not extended" `:39-42`). Catalog schema 3.0.0 and verifier hash match on both sides. So the old 1.0.0 package is refused by design (ANNEX.md § Era pin says the same: "not to be chased upstream") and regeneration is what resolves it.

### 4. Workaround glue: what it is, and why it can go

The demo's own ledger (`exploration/stellarator_e2e/studies/ANNEX.md` § Loader exception and glue; `era_adapter.py:1-40`; `study/run_design_search.py:29-45`):

| Rung | What the harness supplies | Root cause (old route) | On the pinned route (probe 4) |
|---|---|---|---|
| g1 | 6 `power:` lines in `pipelines/mfe_stellarator.yaml` repointed from `mfe_plant_params.mfe_plant__MFE_Power_Plant__p_{the,et,th}` to `stellarator_09__stellaris__pb__p_*` (on-disk lines 93, 103, 113, 123, 134, 146); 3 keys added to `inputs/system_design.json` (lines 2-4). Applied by `run_stellaris.py:127-155` on every execute. Reversing the 6 substitutions reproduces the sealed sha256 `68dd6cc2…`. | Alias `attribute p_th : Real = pb.p_th;` (`mfe_plant.sysml:244-246`) only wired when the consumer formal had the same name (`CODEGEN_FINDINGS.md:7-13`). | Aliases are `AttrNode(is_alias=True)` resolved regardless of consumer name (`elaborate.py:985-1016, 2511-2576`). Probe: `power: float mini3_pkg__mini__pb__p_the`. And post-seal edits under `pipelines/**`/`inputs/**` are now refused (`contracts/manifest.py:18, 56-103`; teax hash-verifies at `package_load.py:141-150`). **Unnecessary and impossible.** |
| g2a | `cas23_to_28_capital__cas28_capital`, `cas2x_pre_contingency__cas28_capital` = 5.0e6 | `:>> cas28_capital = 5000000.0` on the part usage (`stellarator_plant.sysml:727`) dropped; the attribute consumed by two aggregations surfaced as two per-module entry points (WI-028 plan.md:370). | `ValueSite.OCCURRENCE_OVERRIDE` literal (`elaborate.py:1121-1127`), same shape as the Slice-3D `:>> gain = 80.0` proof. **Unnecessary.** |
| g2b | `replacement_cost_per_event__n_mod` = 1.0 | `attribute n_mod : Real default 1.0` (`mfe_plant.sysml:328`) inside an aggregation resolved to NULL (WI-029 plan.md Finding 1). | Computed attribute → `CalcNode`; defaults via `extraction/modeled_defaults.py:66-75`. **Unnecessary.** |
| g2c | 3 dead `mfe_plant__MFE_Power_Plant__p_*` fillers | Same alias defect as g1, surfaced as unminted required schema fields. | Exact route wires the edge or refuses (`SI_EDGE_DANGLING`, `project.py:713-717`); no placeholders. **Unnecessary.** |
| g3 | `special_materials_capital` (2 keys) recomputed per point = `blanket_vol × 0.50 × 9400 × 5.0` — **not independently verified** | `:>> special_materials_capital = rb.blanket_vol * …` (`stellarator_plant.sysml:658`): cross-part read the legacy builder could not carry. | `COMPUTED_ATTRIBUTE` fed by a typed cross-part edge (`project.py:436-470`). Probe: `blanket_vol: float mini3_pkg__mini__rb__vol__blanket_vol.root`, executed 23.5e6. **Unnecessary** — and it closes the one verification hole the proof-of-life disclosed. |

**What gets deleted when the deletion condition fires** (ANNEX.md § Deletion condition; `era_adapter.py:3-9`): `studies/era_adapter.py` and `studies/promotion_equivalence.py` whole; `GlueAwareLoader` + glue constants in `study/run_design_search.py:155-…`; `patch_bop_wiring()` and `GLUE_CONSTANTS` in `run_stellaris.py`; the era fixtures in `tests/study/conftest.py:255-300`; the seven era-bound test files (`test_accept_set`, `test_glue_mapping_agreement`, `test_lineage_refusal`, `test_promotion_equivalence`, `test_annex`, `test_committed_store`, parts of `test_verify`/`test_preflight_gates`); ANNEX § Loader exception and glue, § Era pin. `oracle_entry.py` stays (verification seam, not glue) but its `ENTRY_KEY_TO_ORACLE_INPUT` map updates if entry keys move. `verify_stellaris.py` (the oracle) is untouched by design.

**What gets re-pinned**: `studies/manifest.json` — `fingerprints.indicator_inputs.digest` (:10), `recorded_provenance.{executable,semantic}_fingerprint` (:20-21), `baseline.point` keys (:63-71), `baseline.headline.value` (:75), `baseline.verdicts` (:77-83), `ties` keys (:53-56), `objective_catalog` channels (:25-49). Preflight's `manifest_currency` gate (`scripts/study/preflight.py:233-259`) fails by design until this is done. Test literals: `tests/study/test_known_answers.py:21` (`EXPECTED_SEMANTIC_FINGERPRINT`), the six `tests/study/data/*.expected.json:2`, `test_operand_bindings.py:28-35` (baseline point + `PINNED_LCOE`), `conftest.py:267-269`, `test_era_pin.py:18-23`.

Expect entry-key names to move: the D-5 IFE migration renamed 11 supplier keys. So the proof-of-life CSV headers will not be byte-equal after migration; compare by value, not bytes.

### 5. Before / after evidence

**"Before" — reproducible today, on the era worktree only** (`/home/reid/1cfe/teax-v1-era` @ `fa0e06a`):

| Evidence | Command / location | Pass bar |
|---|---|---|
| 273 study tests incl. the 948-point grid | `STUDY_REQUIRE_ERA=1 uv run python -m pytest tests/study -q -m slow` from the demo worktree (~140 s) | green; `promotion_equivalence` byte-equal to `study/design_search_R_a.csv` (948 rows, sha in `study/synthesis.md:8`) and `study/availability_sweep.csv` (19 rows) |
| Baseline headline + verdicts | `run_stellaris_single.py:77, 100-116` (WI-029 teax pin `07eb0ac` + exec venv in the main checkout) | LCOE 275.264220042, total 16,129,706,216.04, 5/5 satisfied |
| Oracle parity | `study/verification_summary.json` | worst rel 5.67e-16, `package_git_clean: true`, `glue_note` lists g3 as not independently verified |
| Model tests | `uv run python -m pytest tests/models` | 30 passed / 13 skipped |
| Package identity | `generated/contracts/package_contract.json` `executable_fingerprint ad912041…`; `model_contract.json` `semantic_fingerprint c9bc1640…` | recorded |

Capture all of this into a committed "before" record (hashes, counts, env SHAs) before touching a model. Nothing that loads the package runs on teax main today.

**"After" — on the stock route** (codegen `8a758e92` via the pin, teax `744745f`):

1. Regenerate from the migrated staged twin: `uv run sysml-codegen generate --models <staged> --output <generated> --package-name stellarator_tea [--overwrite]` (`cli/__init__.py:1086-1119`; generates and seals in one step), with `SYSIDE_LICENSE_KEY` from `~/1cfe/agentic-mbse/.env`. Two handwritten impls survive by signature match (WI-029 plan.md:539): `dt_fusion_power_impl.py`, `levelized_replacement_cost_impl.py` — verify they re-attach.
2. Deletion condition: `ProvisionalPackageLoader(package_dir, package_name, link_root, strict=True).load()` accepts. Seal reads `runtime_contract_version 2.0.0`, zero `TAMPER` diagnostics, 0 hand edits.
3. Baseline point through `execute_pipeline`: headline within rel 1e-9 of 275.2642200420774 and the same five verdicts (`source_local_identity` match). Any drift is a finding, not a tolerance — g3's CAS27 is now computed in-package, so this is the first time that ingredient is checked against the oracle.
4. Re-run the 948-point grid and the 19-point sweep through the promoted tools (`preflight.py` → `StudyRunner` → `verify.py`): per-point LCOE and verdict equal to the before-CSVs by value (rel < 1e-9), keyed by (R, a) not by column name.
5. Oracle parity: `verify.py` stratified sample at rel < 1e-9, `verification_summary.json` with an empty `not_independently_verified` list.
6. Mutation proof, mirroring the D-5 spine test pattern (`tests/models/test_self_binding_replacement.py`): move one input (e.g. `cas28_capital`), confirm exactly the expected modules move.
7. Model tests + the spine test: the IFE census (23/18) and IFE byte-identity unchanged; the MFE set generates with zero readiness diagnostics.

Items 3–5 are the regression gate. Items 2 and 6 are the "glue really is gone" gate.

## Code References

- `tests/models/test_self_binding_replacement.py:12, 30, 101-114` — licensed whole-tree generation of `models/`; the structural collision.
- `tests/test_dependency_provenance.py:54-76, 82-98` — pin contract the merged `pyproject.toml` must keep.
- `~/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/studies/ANNEX.md` — glue ledger, deletion condition, era pin.
- `…/studies/era_adapter.py:1-40, 61-94, 131-161` — adapter contract, accept-set, era assertion, dead-filler check.
- `…/study/run_design_search.py:29-45, 155-…` — glue ledger g1–g3, `GlueAwareLoader`.
- `…/run_stellaris.py:127-155` — `patch_bop_wiring()` (the g1 edits, applied per execute).
- `…/exploration/stellarator_e2e/CODEGEN_FINDINGS.md:7-13` — Finding 8, the alias defect behind g1/g2c.
- `…/work/completed/20260802_WI-029_handshake-lcoe-construction/plan.md:274, 475-480, 513-516, 539` — generation provenance.
- `…/scripts/study/preflight.py:76-83, 214-306` — identity / currency / baseline / clean gates.
- `…/tests/study/conftest.py:255-300` — era dependency, `STUDY_REQUIRE_ERA`.
- `~/1cfe/sysml-codegen/scripts/make_d5_variant.py:437-509, 583-604` — D-5 preconditions and `--root` flags.
- `~/1cfe/sysml-codegen/.project/backlog/BACKLOG.md:36-41, 403-412` — `[SCALAR-FUNCTION-VOCABULARY]`, `[STELLARATOR-D5-MIGRATION]` hold.
- `~/1cfe/sysml-codegen/src/sysml_codegen/contracts/versions.py:11` and `~/1cfe/teax/packages/teax-simkit/simkit/evaluation/package_load.py:33, 133-150` — 2.0.0 contract both sides.
- `~/1cfe/sysml-codegen/.project/completed/20260814_cutover-recovery/plan.md` "Slice 3D Completion" — the IFE whole-plant route to mirror.

## Architecture Insights

- The demo kept two copies of the MFE models on purpose: `models/` as the canonical home (MR-3) and a self-contained staged twin that was actually generated. That split is what makes Option A cheap: nothing executable reads `models/` for MFE.
- Every workaround was scoped and self-asserting (accept-set of exactly two files, dead-filler check on every load, effective fingerprint over declared sources). That discipline is why retirement is a clean delete rather than an archaeology job.
- Main's stop-parser pins mean the fusion-tea venv no longer tracks local editable checkouts. The migration should run against the pinned codegen SHA, not `~/1cfe/sysml-codegen` HEAD — they agree today (no `src/` change in 75 commits), but that is a fact to re-check, not assume.

## Feasibility Assessment

- **Merge (Phase 1)**: low risk, one session. Three mechanical conflicts; one deliberate structural choice (Option A); verification is running main's suites plus `tests/study`.
- **Model migration (Phase 2)**: medium-to-high, open-ended. The rename is a tool run. Blocker 1 depends on an owner call (wait upstream vs rewrite six sites). Blockers 2–3 are model edits with clear shapes. Blocker 4 is unknown until 1–3 clear. Budget for at least one more refusal class.
- **Regeneration + glue retirement (Phase 3)**: low risk once Phase 2 seals. The deletion list and re-pin list are fully enumerated above; the bars are numeric.
- **Prerequisites**: owner release of the stellarator edit hold; the syside license (`~/1cfe/agentic-mbse/.env`); teax main on the path for the after-route (main's tests use `STOP_PARSER_TEAX_ROOT`, whose pinned commit is not documented in fusion-tea — confirm it is `744745f` or record what it is).

## Recommendations

1. **PR 1 — land the demo work (no model changes).** In the demo worktree: merge `main` into `feat/stellarator-mbse-demo`; resolve CURRENT_WORK/BACKLOG by hand, regenerate `uv.lock`; apply Option A (MFE models stay in the staged twin); narrow the `.gitignore` rule; drop `.orchestrate-logs/` and the two osiris dirs. Verify: `tests/test_dependency_provenance.py`, licensed `tests/models` incl. the spine test, `tests/study` (era skips allowed on main, `STUDY_REQUIRE_ERA=1` in the worktree). Owner admin-merges with a merge commit.
2. **Before-record.** Commit the "before" evidence table (Section 5) as a record beside the study, captured on the era route, before any model edit.
3. **PR 2 — model migration item** (`/_my_spec` → design → plan). Scope: release the hold; D-5 via the tool on both trees; fix blockers 1–3 (owner decides blocker 1's route); iterate `sysml-codegen generate` until it seals at 2.0.0; file the positional-redefinition finding upstream regardless; promote MFE into `models/` with the spine test scoped per design family.
4. **PR 3 — regenerate and retire the glue.** Delete the adapter and glue per Section 4, re-pin the manifest and test literals, and run the Section 5 "after" gates on the stock route with teax main.
5. **Then RUN-STUDY Item 6** on the stock route. Running the first A/B consumer without the era adapter is a stronger first proof and retires the `[AGENT]` "Temporary-route integrity" criterion for good.

Alternative considered: run Item 6 first on the era route, migrate later. It works, but it produces a capability-compliant record under an identity that retires on migration, and Item 6's A/B arms would each need re-running. Not recommended unless the migration stalls on blocker 1.

## Decisions (owner, 2026-08-21)

Walked through with the owner after the research; the questions below are kept as the record of what was open.

- **Q1 → A.** `[OWNER]` MFE models stay only in the staged twin for PR 1; promoted into `models/` in the migration PR. The spine test is reshaped there, not before — tracked as the "Test cleanup" row at the top of `BACKLOG.md`.
- **Q2 → after migration.** `[OWNER]` RUN-STUDY Item 6 runs on the stock route once the package is regenerated. Revisit only if the migration stalls.
- **Q3 → Both.** `[OWNER]` Rewrite the six `sqrt`/`max`/`min`/`floor` sites model-side now (check whether `**` is admitted before choosing the `sqrt` form); file the six sites upstream as the motivating case for `[SCALAR-FUNCTION-VOCABULARY]`; revert the rewrites when the pin catches up — the revert is a `BACKLOG.md` row, not a memory. Choosing this route releases the stellarator edit hold (codegen `BACKLOG.md:403-412`).
- **Q5 resolved by lookup.** fusion-tea pins no teax commit. Main's two teax acceptance tests read `STOP_PARSER_TEAX_ROOT`, which the sealed runner (`sysml-codegen verification/run_independent_green.py:1121`) supplies from the `/tmp` shipment tree; they are environment-contract tests, not something an ordinary checkout runs. For the "after" route use teax main `744745f`, the only teax that accepts `runtime_contract_version 2.0.0`.
- **Q6 picked by default.** Narrow the ignore rule to `exploration/stellarator_e2e/outputs/`; drop `.orchestrate-logs/` from tracking in PR 1.
- **Q7 unchanged.** Stays with the Item 6 Align.

## Open Questions (as raised; see Decisions above)

1. **MFE models in `models/` during the merge** — Option A (staged-only until they generate clean) vs B (scope the spine test now). Owner call; A recommended.
2. **Blocker 1 route** — wait for `[SCALAR-FUNCTION-VOCABULARY]` upstream (P2, no owner, no fix in the pin) or rewrite the six `sqrt`/`max`/`min`/`floor` sites as calc defs model-side?
3. **Release the stellarator edit hold** (codegen `BACKLOG.md:403-412`).
4. **Item 6 before or after migration** — after recommended.
5. **`STOP_PARSER_TEAX_ROOT`** — which teax commit main's acceptance tests expect; not recorded in fusion-tea.
6. **`.gitignore` scope** for `outputs/` and whether `.orchestrate-logs/` should ever be tracked.
7. Whether the verification-vs-oracle step is mandatory in the general study contract (carried from Item 5 to the Item 6 Align) — unchanged by this research, but the migration removes the only disclosed verification hole (g3), which may inform the answer.
