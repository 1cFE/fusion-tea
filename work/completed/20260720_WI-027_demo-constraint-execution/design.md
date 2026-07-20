---
Status: complete
Created: 2026-07-19
Updated: '2026-07-20'
Related Artifacts:
  Spec: ./spec.md
  Orchestration: ../../orchestration/demo-constraint-execution.md
  Protocol: ../../../knowledge/holdout/aries-cs/PROTOCOL.md
---

# WI-027 Design — Demo Constraint Execution (STELLARATOR-DEMO Item 2)

## ⚠ AMENDMENT / SUPERSESSION (2026-07-20, constraint-lifecycle Item 10)

**Two of this design's load-bearing decisions are superseded by the ratified lifecycle contract
and Item 10. Do not build on D7 or the Gate-B options below.**

- **D7 (passthrough calcs for constraint actuals) is SUPERSEDED by owner decision D-2**
  (`~/1cfe/sysml-codegen/.project/concepts/constraint-execution-authoritative-lifecycle-contract.md`,
  D-2): a direct literal-valued design attribute is a valid actual; no passthrough calc is required.
  D7 was designed but never landed; the staged asserts read design attributes directly. Nothing to remove.
- **Gate A / Gate B are resolved upstream** — Gate A by lifecycle Item 2 (shared resolver), Gate B by
  Item 3 (extension-time V11 check proven vacuous and deleted). The three Gate-B options here are moot.
- **The cross-part capital rollup is now compiled by codegen** (Item 10, WI-015 finding #4 root closure):
  `direct_capital`/`total_capital` are real instance-scoped aggregation producers. The staged twins now
  carry the canonical formulas (the DEMO-NOTE plain-input conversions are removed), the snapshot is
  recaptured (v5, 5 constraint facts), and public generation emits with **zero V11 offenders and zero
  producer-completeness violations — no private bridge, no placeholder, no D7 passthrough.**
- **Retired:** `bridge_v11_generate.py`, `run_stellaris.py` glue-2 rollup arithmetic, and
  `handshake_1costingfe.py`'s rollup glue (its 1costingFE comparison role stays). The runner cuts over to
  bridge-free execution; the six ordinary anchors stay bit-exact (anchor movement is a STOP) and the five
  verdicts remain all-satisfied.

Evidence: `~/1cfe/sysml-codegen/.project/active/constraint-lifecycle-producer-completeness/evidence.md`.
The rest of this document is retained as the historical record of the pre-Item-10 blocked state.

---


**Required reading honored.** PROTOCOL §3 barred paths were not read, cited, or opened during this design. Admissible sources only: the staged demo package under `exploration/stellarator_e2e/`, the canonical `models/`, the sysml-codegen editable dep (`~/1cfe/sysml-codegen`), and the in-repo IFE constraint-exec acceptance in the primary checkout (`~/1cfe/fusion-tea/exploration/ife_e2e/`).

## Overview

The demo criterion (concept criterion 2) wants the five already-modeled viability asserts to **execute through the generated pipeline** and land their verdicts (`satisfied | violated | indeterminate`) as data in the run report — with no hand-coded viability rule anywhere. The model carries the asserts; the staged demo package strips them before codegen, so they never run.

The whole job in one sentence: **un-strip the five asserts in the staged twins, recapture the snapshot so it carries the constraint facts, and regenerate through the existing bridge — the constraint modules then emit and execute for free, because the constraint-emission machinery already lives inside the exact generation functions the bridge calls.** Every numeric channel stays bit-exact; five verdicts appear alongside them.

This design settles the six mechanism questions the brief handed off, records the defect-register check (all five forms NOT-HIT), and pins the toolchain commit.

---

## ⚠ SURFACED PREMISE FLAG (2026-07-19) — Gate B blocks emission; dependent conclusions parked

**This item cannot reach "constraints emit and execute" without an owner decision. The rewiring the owner already ruled on (below, D7) is proven necessary and works — but a *second, independent* architectural gate, unknown when the ruling was made, blocks the generate-and-emit path. Every resolution is out of this item's authorized surfaces. I am surfacing, not designing around it (capture-fidelity §4).**

Two gates stand between the un-stripped asserts and executed verdicts. Both were proven by capture probes at `512786c` (evidence in `.orchestrate-logs/wi027_probe/` and the CODEGEN_FINDINGS #9 addendum):

- **Gate A — INV-2 refuses literal-valued design-attribute actuals** (the original implement bounce). **RESOLVED** by the owner-ruled rewiring (D7): route each literal-valued limit/value through a passthrough calc so the actual is a calc output. Proven — a capture then carries all five facts, correctly rewired.

- **Gate B — constraint lowering is architecturally incompatible with the demo's V11 capital-rollup bridge. NOT RESOLVED; needs an owner decision.** `extend_graph_with_constraints` runs a whole-graph V11 coverage check that hard-fails on the 3 capital-rollup keys (`contingency__direct_subtotal`, `indirect__direct_cost`, `lcoe_calc__total_capital`) — the exact keys `bridge_v11_generate.py` fills at *generation*, not capture. Filling them clears coverage (proven: `uncovered AFTER placeholder fill: []`), but there is no capture-time bridge hook, and the from-snapshot lowering runs *before* the bridge fills placeholders. A lowering-OFF capture carries the facts but records no occurrence table, so a later force-lower dies `FrozenOccurrenceIndexCorruptionError`. The occurrence table and V11 coverage are produced together only during a *fully-covered, lowering-ON* capture — which the bridge pattern structurally prevents. The IFE acceptance never hit this: it has no cross-part capital-rollup bridge (its graph is fully covered at capture). **The design's original premise — "constraints emit for free through the existing bridge" — is false for a bridged whole-plant package.**

**Resolution options for Gate B (each exceeds this item's current scope — owner picks one):**

1. **Upstream sysml-codegen fix (recommended).** Scope the constraint-lowering V11 check to the constraint-added inputs only (beta/tbr/wall_load — all covered), not a re-check of pre-existing unrelated offenders the harness bridges; or run the check after entry-point bridging. Clean and correct, but sysml-codegen is read/checkout-only for this item — needs the remediation epic to take it (filed to CODEGEN_FINDINGS #9 addendum, "file upstream").
2. **Cover the capital-rollup keys in the model at capture** — give `direct_capital`/`total_capital` placeholder defaults in the staged twin so the graph is V11-covered at capture (harness still overwrites at execution → zero numeric movement). Touches the finding-4 capital-rollup region, which is **spec Out-of-Scope** and named "left as-is"; also needs the bridge's offender-count assert changed (3 → 0). Requires the owner to widen scope.
3. **Re-scope / defer WI-027** until the upstream fix lands (option 1), sequencing it behind the constraint-PR-wave remediation.

**Parked pending the decision:** D1's generation recipe (emission step), D6's numeric-neutrality run, SV-033's executed record, and all downstream phases. D7 (the rewiring) stands regardless — it is the proven Gate-A fix and a prerequisite for every option. Do not proceed to `/implement-model` on the emission path until Gate B is decided.

---

## Key research findings (mechanism facts this design rests on)

Four facts, each verified this session, carry the whole design:

1. **The snapshot is codegen's input, not the `.sysml` files.** `bridge_v11_generate.py:73` builds its graph from `stellarator.snapshot.json`. The current snapshot has `constraint_lowering_mode: "applied"` but **zero constraint facts** (grep: 0 `assert`, 0 `beta_ok`/`net_positive`/…) — it was captured from the *stripped* staged copies. So restoring the asserts in the `.sysml` does nothing until the snapshot is **recaptured**. This is the crux the strip-site line numbers alone hide.

2. **Constraint emission is embedded in the private `_generate_*` functions the bridge already calls.** In `~/1cfe/sysml-codegen/src/sysml_codegen/cli/__init__.py`: `_generate_schemas` emits `constraint_types.py` gated on `ctx.computation_graph.constraint_catalog` (:338-345); `_generate_modules` emits `constraints/predicates.py` and every `ModuleKind.CONSTRAINT` / `ModuleKind.REPORT_AGGREGATOR` module (:363-392); `_generate_pipeline` wires them via `generate_pipeline_yaml(graph=…)` (:522-527). The bridge (`bridge_v11_generate.py:110-124`) calls all three. **So the bridge path emits the predicate module, the per-constraint modules, and the `ConstraintReportAggregatorModule`, wired into the pipeline as exit points — automatically, once the graph carries a constraint catalog.** No IFE-path adoption, no new codegen call.

3. **The IFE acceptance is the working proof of this exact machinery.** `~/1cfe/fusion-tea/exploration/ife_e2e/study/` (2294/2301, 2026-07-13) regenerated the IFE package on `constraint-exec-epic`, emitted 8 modules (was 6) including a viability-constraint module and `ConstraintReportAggregatorModule`, and re-verified anchors byte-exact — "regeneration changed nothing about the plant's numerics, only added the now-executing constraint." The verdict record shapes, the aggregator structure, and the two `run_anchors.py`-side exit-path adapters are all lifted directly from there (see §Verdict surface).

4. **`6db3212` (WI-025 pin) and `512786c` (current HEAD, IFE lineage) both emit constraints.** The five-seam emission and profile-v3 admission landed *below* `6db3212`; emission defaults on (`lower_constraints_enabled=True`) and is gated on non-empty `constraint_facts.usages`. So WI-025 emitted no constraints only because its snapshot was stripped — not because `6db3212` couldn't. `512786c` = `6db3212` + GAP-CLOSE F-series hardening (constraint/path/symlink/warning); none of it touches numeric templates or our five forms (§Pin).

## Mechanism decision 1 — Generation path

**Decision: keep today's chain unchanged — recapture the snapshot from the *un-stripped* staged tree, then run `bridge_v11_generate.py` with `preserve_handwritten=True`.** The only new thing versus WI-025 is that the staged twins carry the five asserts when the snapshot is captured.

The recipe (from the WI-025 record and `CODEGEN_FINDINGS.md:29`), one added precondition in bold:

```
source ~/1cfe/fusion-tea/.env                       # SYSIDE_LICENSE_KEY
# **precondition 1: five asserts un-commented in both staged twins (MR-3)**
# **precondition 2: D7 constraint-actual rewiring applied to canonical + staged twins**
sysml-codegen snapshot -m exploration/stellarator_e2e/models \
    -o exploration/stellarator_e2e/stellarator.snapshot.json     # NO --design-path-filter
cd ~/1cfe/sysml-codegen && uv run python <e2e>/bridge_v11_generate.py   # preserve_handwritten=True
# execute via exploration/pipeline_spike/.venv-exec/bin/python run_stellaris.py
```

**⚠ This recipe does NOT yet complete — Gate B (premise flag above) aborts the snapshot step under lowering-ON, which the emission path requires.** With D7 applied, the capture resolves all actuals (Gate A cleared) but `extend_graph_with_constraints` then hard-fails on the 3 capital-rollup keys the bridge fills only at generation. The recipe is correct in shape; the final emission step is **parked** pending the Gate-B decision. The `preserve_handwritten=True`, no-`--design-path-filter`, and exactly-3-bridged-offenders invariants are unchanged and still apply.

- **`preserve_handwritten=True` is untouched** (`bridge_v11_generate.py:108`), so the WI-022 `dt_fusion_power_impl.py` sha256 (`8d2357…794a9f`) survives regen (MR-5.5). The Bosch-Hale hand impl is orthogonal to constraint emission.
- **No `--design-path-filter`** (the WI-024 gotcha: the filter bakes 8 spurious V11 offenders into the snapshot). Control: the bridge must still report **exactly 3** bridged offenders (the capital-rollup keys) — `bridge_v11_generate.py:91-92` aborts otherwise. Constraints add only *covered* operands, so they introduce no new V11 offender.
- **The V11 bridge and the constraints are independent seams.** The bridge exists for the cross-part capital-rollup feature-chain sum (`direct/total_capital`), which codegen can't wire. The five constraints touch none of those keys. The bridge's `entry_point_groups` manipulation and the constraint emission do not interact.

**Rejected alternative: adopt the IFE acceptance's bridged-generation path** (`generated_bridged`/`pkg_bridged`). Rejected because our V11 bridge exists for a *different* reason than IFE's (IFE has no cross-part capital-rollup problem), it is already proven for the stellarator package (WI-022→025), and swapping it would drop the capital-rollup fix and risk the bit-exactness bar. The IFE path is the *evidence* that the underlying machinery works, not a path to copy. Minimum-delta wins: one precondition (un-strip) added to a proven chain.

## Mechanism decision 2 — Verdict surface and report shape

**Where verdicts come from (all generated, all data):** `_generate_modules` emits, per assert, a compiled predicate function in `generated/modules/constraints/predicates.py` and a constraint module that wraps it and emits one `ConstraintEvaluation`; and one `ConstraintReportAggregatorModule` that collects all five into a `ConstraintReport`. `_generate_pipeline` declares the `ConstraintReport` and the five `ConstraintEvaluation`s as pipeline **exit-point outputs**, written as JSON next to the numeric channel files. A `violated` verdict is a data value in that report, never an exception (INV-3, proven at three layers in the IFE package).

**Verdict record shape (lifted from the IFE package — `generated/schemas/constraint_types.py`):**

```
ConstraintEvaluation:
  constraint_id : str                    # e.g. stellarator_09__stellaris__beta_ok__<hash>
  actual_value  : Optional[bool]         # predicate truth; None ⇒ indeterminate
  status        : "satisfied"|"violated"|"indeterminate"
  margin        : Optional[float]        # signed distance to bound, e.g. beta_limit − beta
  observed      : dict[str,float]        # operands explaining the verdict, e.g. {beta, beta_limit}

ConstraintReport:
  catalog_fingerprint : str
  assessed_count      : int              # = 5 for this item
  headline            : "violation"|"indeterminate"|"all_satisfied"|"not_assessed"
  results             : list[ConstraintEvaluation]   # one per assert
```

The aggregator is generic over N constraints (IFE ran one; we run five): its `EXPECTED_IDS` tuple and `ConstraintReportAggregatorInput` fields are generated from the catalog, `extra="forbid"` so a missing or unexpected verdict is a schema error, not a silent gap. Headline precedence: `violation > indeterminate > all_satisfied > not_assessed`. At our design point the report is `headline="all_satisfied"`, `assessed_count=5`, five `status="satisfied"` rows.

**How `run_stellaris.py` captures it into the run report.** `run_stellaris.py` already runs the pipeline through teax's `execute_pipeline(..., output_router=…, custom_schema_types=CUSTOM_SCHEMA_TYPES)` in two passes (Pass A physics+accounts, glue-2 capital rollup in Python, Pass B final). Three additive harness edits, all mirroring the IFE `run_anchors.py` fixes, all confined to `exploration/stellarator_e2e/`, all marked `# CONSTRAINT-EXEC` adapters:

1. **Register write handlers for the new exit-point types.** Add `ConstraintEvaluation` and `ConstraintReport` to `CUSTOM_SCHEMA_TYPES` / the output router (IFE `run_anchors.py:122-131`). Without this the `PipelineValidator` rejects the run — one write handler is required per exit-point type.
2. **Skip non-numeric exit outputs in the oracle-comparison dict.** The `check()`/oracle loop coerces every channel with `float()`; the two verdict-evidence channels aren't scalars. Filter to `hasattr(val,"root") or isinstance(val,(int,float))` (IFE `run_anchors.py:139-146`). This keeps MR-5.1 bit-exactness on numeric channels exactly as it was — the verdict channels are simply not in the numeric set.
3. **Harvest the `ConstraintReport` from Pass B and print the verdict table.** Read `constraint_report.json` from the Pass B exit outputs, print a five-row `constraint | actual | bound | verdict` table into the existing run report next to the CAS breakdown, and assert parity (§Decision 3). Pass B is the canonical final run at the design point; verdicts are pass-invariant (their operands — `p_net`, `rec_frac`, `wall_load`, static `beta`/`tbr`/limits — are identical in both passes; only the capital rollup differs between passes).

**SV-033 records** the Pass-B `ConstraintReport` verbatim: `headline`, `assessed_count=5`, and the five `{constraint_id, status, actual_value, margin, observed}` rows (expected all satisfied, table below), plus the catalog fingerprint.

**One implement-time check on the pipeline rewrite:** `patch_bop_wiring()` (`run_stellaris.py` glue-1) rewrites the pipeline YAML to repoint four BOP power inputs. It edits named BOP nodes only and must **not** drop the new constraint/aggregator nodes or their exit-point declarations. Verify the rewritten YAML still contains the five constraint modules, the aggregator, and their exit points.

## Mechanism decision 3 — Oracle treatment and verdict parity

**Decision: the oracle stays a pure numeric mirror; verdict parity is a dedicated runner assertion against the static expected-verdict list — the oracle does NOT recompute the comparisons.**

This is the runner-assertion option the brief offered, chosen over "oracle asserts verdicts" because **MR-WI027-2 explicitly puts the oracle inside the no-viability-comparison grep scope** ("grep-provable across the staged demo package and its harness (oracle, runner, handshake, glue)"). Writing `beta <= beta_limit` into `verify_stellaris.py` to recompute a verdict would be a viability comparison in the oracle — exactly what MR-2 forbids by name. So:

- `verify_stellaris.py` is unchanged in kind — it mirrors the numeric channels (`p_net`, `rec_frac`, `wall_load`, …) at rel 1e-9 and asserts nothing about limits. MR-5.1 bit-exactness is untouched.
- The runner asserts each generated `report.results[i].status == "satisfied"` and `report.headline == "all_satisfied"`, comparing the **model's own reported verdict** against the **static expected constants** from the design-point actuals table (MR-4). This is a verdict *regression* check — a string equality against `"satisfied"` — not a physics comparison. It introduces no `X <= limit` anywhere.

Why this is honest verification and not a weakening: the five verdicts are trivially derivable from channels the oracle *already* proves bit-exact (`p_net>0`, `rec_frac≤0.5`, `wall_load≤4.05`) plus the published static limits (`beta≤0.05`, `tbr≥1.05`). An independent reader confirms the verdicts from the bit-exact numerics and the model's limit attributes; the parity assertion catches any regression against the known-expected set. The **source of the reported verdict is the generated `ConstraintReport`**, which is the demo's whole claim.

**Rejected alternative: oracle recomputes the five comparisons for parity** (the brief's "recommended if cheap"). Rejected because MR-2's grep scope names the oracle; a recomputed `beta <= beta_limit` there would trip the very check that proves criterion 2's second half. The independence it would buy is already provided by the bit-exact numeric mirror plus static limits.

**MR-WI027-2 grep terms (named here, per its validation clause).** Absence is proven by:

```
grep -rnE '(p_net|net_electric|rec_frac|beta|wall_load|tbr)\s*[<>]=?[^=]' exploration/stellarator_e2e/ --include=*.py
grep -rnE '\b(viable|is_viable|passes_viability)\b'                       exploration/stellarator_e2e/ --include=*.py
```

Expected result: **zero viability comparisons** (verified zero on the current tree; the change adds only `status == "satisfied"` string equality, which these patterns do not match). The report field that carries verdicts instead is `ConstraintReport.results[].status`. Physics channel arithmetic (`rec_frac = 1.0/q_eng`), dict-key channel names, and numeric band checks (`abs(val-target)<=tol`) are not viability rules and are not matched by the operand-vs-bound pattern above.

## Mechanism decision 4 — Pin and defect-register check (MR-6/MR-7)

### Pin

**Generate at sysml-codegen `constraint-exec-epic` @ `512786c` (current HEAD) — the IFE-acceptance lineage.**

Reconciliation, recorded per MR-6:

| State | Emits constraints? | Relation |
|---|---|---|
| WI-025 stellarator regen | `6db3212` | yes (five-seam + profile-v3 landed below it) | numeric baseline |
| IFE acceptance | `constraint-exec-epic` tip, "W1 landed" | yes (proven, 8 modules) | = current HEAD `512786c` |
| **This item** | **`512786c`** | **yes** | `= 6db3212 + GAP-CLOSE F-series` |

`512786c` is a descendant of `6db3212`; the delta is GAP-CLOSE F-series hardening (F5 nullable-QN identity, F9 symlink coverage, boundary guards, warning parity) plus uncommitted certified R-series fixes in the working tree (20 modified files). None of it touches numeric templates or any of our five forms (§defect table). Generating at HEAD (a) matches the state that *proved* constraint emission end-to-end, per the brief's "reuse the IFE evidence"; (b) is the checked-out commit, so no ancestor checkout in a dirty tree. **Implement records the exact `512786c` and the sysml-codegen `git status` at generation time into SV-033**; the working-tree fixes are NOT-HIT for our forms, so committed-`512786c` and `512786c`+worktree emit identical constraint output for us. For a fully deterministic pin the team may stash the worktree and generate from clean `512786c` (identical result for our five, since the worktree fixes are NOT-HIT).

**Residual risk, gated:** the `6db3212 → 512786c` delta is asserted to leave numerics bit-exact (F-series is constraint/path/symlink/warning, not numeric templates), but this is *checked, not assumed* — MR-5.1 (oracle bit-exact) and MR-5.4 (offender list = 6 pre-existing) are the gate. A numeric shift is a surface-to-orchestrator event, not a silent re-baseline.

**Rejected alternative: generate at `6db3212`** to match the WI-025 numeric-baseline codegen exactly. Rejected because it would emit constraint modules that are *not* the proven-identical IFE ones (F-series may have hardened the constraint/aggregator templates below HEAD), sacrificing the strongest evidence we have; it needs an ancestor checkout in sysml-codegen's dirty tree; and F-series does not touch numeric templates, so `512786c` should be bit-exact anyway — with the bar to catch it if not.

### Defect-register check (MR-WI027-7) — all five forms NOT-HIT, no premise flag

Register walked: `~/1cfe/sysml-codegen/.project/backlog/epic_constraint_pr_wave_remediation.md` and its code-review research (`R-1…R-12`). Our five forms are **plain relational comparisons of numeric operands, no negation**, and each assert is **co-located in the same `.sysml` file as the calc-usage its operand reads** (verified: `pb` at `mfe_plant.sysml:223`, its asserts at `:464-465`; `wall_load_calc` at `stellarator_plant.sysml:728`, its assert at `:745`). All five constraints are **named** and all **ADMIT** (numeric). Against that profile:

| Defect | Sev / status | Touches our path? | Verdict |
|---|---|---|---|
| R-1 ordering admits non-numeric operands | High / open | all five operands are Real | **NOT-HIT** — non-numeric-operand hole; ours are numeric, admit correctly |
| **R-2 negated asserts execute inverted** | High / open | only `assert not constraint` | **NOT-HIT** — none of the five is negated; the inverted-verdict branch is never reached (the specific defect the brief flagged) |
| R-3 reserved-name shadowing (`value/status/verdict/self`) | High / certified (worktree) | predicate compiler + aggregator | **NOT-HIT** — no operand named value/status/verdict/self (ours: beta, beta_limit, wall_load, tbr, net_electric, rec_frac, threshold, …) |
| R-4 nullable-QN filter crashes from-snapshot rebuild | High / open | snapshot replay | **NOT-HIT** — needs an anonymous *excluded* usage alongside an anonymous ADMIT; all five are named and ADMIT, no excluded usage exists |
| R-5 recursive part containment truncates occurrence set | Med / open | occurrence expansion | **NOT-HIT** — no self-recursive `part def`; the stellarator part tree is not self-referential |
| R-6 excluded locations leak abs paths into fingerprints | Med / certified (worktree) | path portability + aggregator | **NOT-HIT** — leak is via named *excluded* (non-numerical) usages; ours all ADMIT, so `excluded_records` is empty |
| R-7 constraint demand overwrites calc-usage grouping | Med / open | assert lowering + demand | **NOT-HIT** — fires when the assert sits in a *different file* from the calc-usage; ours are co-located (verified above) |
| R-8 warning pre-pass masks BLOCK diagnostic | Med / open | non-numerical warning path | **NOT-HIT** — fires on NON_NUMERICAL statements; all five are numeric, ADMIT |
| R-9 `_literal_float` drops unit/signed modeled defaults | Med / open | default resolution for our limits | **NOT-HIT** — every limit is a bare unsigned `Real` literal (`beta_limit=0.05`, `wall_load_limit=4.05`, `tbr_floor=1.05`, `threshold=0.5`); units are in comments only, no `[unit]` annotation, no sign |
| R-10 seal/verify symlink gaps | Med / certified (worktree) | package integrity | **NOT-HIT** — symlink-tree defect, constraint-content-independent |
| R-11 v3 loader raw errors on malformed sections | Med / certified (worktree) | snapshot replay diagnostics | **NOT-HIT** — fires only on a malformed/hand-edited snapshot; valid replay unaffected |
| R-12 invalid `TEAX_SIMKIT_PATH` falls through | Med / open | test-harness discovery | **NOT-HIT** — test infra, not emission |

Boundary hazard (the IFE 7-row `>` vs `>=` class): our design-point actuals sit off **every** bound (below), so no verdict rides a boundary. **No defect touches a construct we use. No premise flag; design proceeds.**

## Mechanism decision 5 — Staged-twin diff-bar

The staged twins already carry the five asserts in commented-out DEMO NOTE blocks (staged `mfe_plant.sysml:459-465`, staged `stellarator_plant.sysml:741-746`). Un-stripping means: **delete the DEMO NOTE strip comments and un-comment the five asserts, so the staged viability-constraint regions become byte-identical to canonical `models/`.**

**Amendment (D7):** canonical is now also edited — the constraint-actual rewiring (D7) lands in canonical `models/` first (owner-ruled), and the staged twins mirror it. Canonical remains the source of truth; the twins stay byte-identical to it in the viability region. The `mfe_viability.sysml` library gains the `'Scalar Value'` passthrough def in both the canonical library and its staged copy (`models/analyses/mfe_viability.sysml`), byte-identical.

**Twin diff-bar for this item (what may differ after the edit):**

- The five assert blocks **plus the D7 passthrough calcs** in both staged twins: **byte-identical to canonical** after un-strip + rewiring. `git diff` of the viability-constraint regions between staged and canonical is **empty**. (The rewiring is applied to canonical, then mirrored — so byte-identity holds by construction.)
- The two **unrelated** capital-rollup DEMO NOTEs stay exactly as they are: staged `mfe_plant.sysml:400-409` (`direct_capital` → plain input) and `:430-434` (`total_capital` → plain input). WI-015 findings 4/8, out of scope (spec Out of Scope). These remain the *only* intentional staged↔canonical divergences.
- **Nothing else may differ.** No other staged region changes. Any additional staged↔canonical delta introduced by this item is a defect.

Twin identity holds per-edit-region, as it has since WI-015: after this item, the staged twins differ from canonical only in the two documented capital-rollup conversions.

## Mechanism decision 6 — Validation design

**SV-033 executed-record shape** (filled at implement, `modeling_project/VALIDATION_MATRIX.md`):

- The Pass-B `ConstraintReport`: `headline`, `assessed_count=5`, catalog fingerprint, and five rows. Expected:

| constraint_id (suffix) | actual | bound | status | margin (≈) |
|---|---|---|---|---|
| `net_positive`  | net_electric 915.081088 MW | `> 0`    | satisfied | +915.08 |
| `recirc_ok`     | rec_frac 0.151362          | `≤ 0.5`  | satisfied | +0.3486 |
| `beta_ok`       | beta 0.0276                | `≤ 0.05` | satisfied | +0.0224 |
| `wall_load_ok`  | wall_load 3.13 MW/m²       | `≤ 4.05` | satisfied | +0.92 |
| `tbr_ok`        | tbr 1.074                  | `≥ 1.05` | satisfied | +0.024 |

All satisfied, none on a boundary. If any comes back `violated`/`indeterminate`, MR-4 governs: record and surface as a demo finding, do not tune away (and cross-check the machinery via the MR-7 result — a non-satisfied verdict at a design point the oracle proves passing would indict the predicate/codegen, not the model).

**Standing bars re-verified (MR-5), each recorded in SV-033:**

1. **Oracle bit-exact** — every numeric channel vs `verify_stellaris.py` at rel < 1e-9 (unchanged).
2. **Handshake untouched, original bar** — `handshake_1costingfe.py` edited only within `set_1cfe_inputs`'s injection map, and **`git diff exploration/stellarator_e2e/handshake_comparison.json` empty** after the run. Expectation: **no handshake edit is needed at all** — constraints don't touch cost injection.
3. **IFE anchors** — `run_anchors.py` reproduces 252.29996307 / 68.69020165 / 270.12117794, Meier 4.735, byte-exact (SV-023). Untouched: this item regenerates only the stellarator package.
4. **L1 offender list = the 6 pre-existing** — `mfe_plant.sysml` (3, line-shifted per WI-025), `ife_plant.sysml:33/41`, `hif_plant.sysml:205`; compare the offender *list*, not level flags. **Zero new offenders.** The un-commented asserts parse (they parse in canonical, which is L1-clean) and reference resolving operands, so they add no L1 offender; the ~3 known contingency/indirect/lcoe rollup keys are the WI-025 baseline set, unchanged. The five generated constraint modules are generated code (proven-clean templates), not `models/` L1 scope.
5. **WI-022 handwritten-impl hash** — `dt_fusion_power_impl.py` sha256 `8d2357…794a9f` content-identical through `preserve_handwritten=True`.
6. **pytest tally 11 failed / 18 passed / 14 skipped / 0 errors** — unchanged (WI-026 owns any re-record; out of scope).

**Which SVs re-verify:** SV-025/026 (handshake byte-identity, original bar — sub-bar 2), SV-023 (IFE anchors — sub-bar 3). **L1–L6 expectation:** offender list exactly the 6 pre-existing, zero new; level-summary flags may shift with the added modules, so compare the *list*.

**D7 rewiring numeric-neutrality (MR-8 amended — canonical now edited, but only representation).** The passthrough calcs carry constants that were already in the model; they are constraint-operand plumbing, not in the cost/physics dataflow, so no executed numeric channel moves. This must be *proven*, not assumed, once Gate B is resolved and the package emits — name the checks (all parked with Gate B):
- **Oracle bit-exact** — every executed numeric channel matches `verify_stellaris.py` at rel < 1e-9, unchanged from WI-025 (the passthrough calcs add channels but touch none of the numeric spine).
- **Headline to the cent** — total $12,638,857,665.74, LCOE $203.647152/MWh, p_net 915.081088 MW, magnet 50.03% — identical.
- **Handshake** — `git diff exploration/stellarator_e2e/handshake_comparison.json` empty; injection map untouched.
- **L1–L6 offender list = the 6 pre-existing** — the five new passthrough calc modules must add **zero** new offenders (compare the list, not level flags).
- **WI-022 hash** — `dt_fusion_power_impl.py` sha256 `8d2357…794a9f` intact.

**MR-8 status:** canonical `models/` is now edited by this item — but only the owner-ruled *representation-only* rewiring (D7), never viability semantics or values. Gate B (above) is the surfaced blocking canonical↔codegen incompatibility; it is surfaced, not silently fixed. The earlier claim that "codegen at `512786c` lowers exactly these forms per the IFE proof" was **wrong** (see Prototype-status correction).

## Mechanism decision 7 — Constraint-actual rewiring (Gate A fix, owner-ruled 2026-07-19)

**Decision: route each literal-valued design-attribute constraint actual through a passthrough calc so the actual resolves to a calc output. Keep the design attributes as the single documented value source (their MR-4 citations stay put); add one passthrough calc per literal actual and retarget the assert.** This is the WI-021 pattern (route a value through a calc so it forward-computes through codegen) and is representation-only, value-preserving, zero numeric movement, no viability-semantics change — within the owner's amended MR-WI027-8.

**Exactly what changes (canonical `models/`, mirrored to the staged twins — D5).** Only the three asserts binding literal design attributes need it; `net_positive`/`recirc_ok` (read `pb.p_net`/`pb.rec_frac`) and `wall_load_ok`'s achieved `wall_load` (reads `wall_load_calc.wall_load`) already resolve.

- **Library `models/library/analyses/mfe_viability.sysml`** — add one concept-agnostic passthrough calc def:
  ```
  calc def 'Scalar Value' {
      in attribute v : Real;
      out attribute value : Real = v;
  }
  ```
- **Instance `models/designs/stellarator_09/stellarator_plant.sysml`** — keep `beta`/`beta_limit`/`wall_load_limit`/`tbr`/`tbr_floor` attributes as-is (unchanged values + docs); add five calc usages reading them, and retarget the three asserts:
  ```
  calc beta_val           : 'Scalar Value' { in v = beta; }
  calc beta_limit_val     : 'Scalar Value' { in v = beta_limit; }
  calc wall_load_limit_val: 'Scalar Value' { in v = wall_load_limit; }
  calc tbr_val            : 'Scalar Value' { in v = tbr; }
  calc tbr_floor_val      : 'Scalar Value' { in v = tbr_floor; }

  assert constraint beta_ok : 'Beta Limit' {
      in beta = beta_val.value;  in beta_limit = beta_limit_val.value; }
  assert constraint wall_load_ok : 'Neutron Wall Load Limit' {
      in wall_load = wall_load_calc.wall_load;  in wall_load_limit = wall_load_limit_val.value; }
  assert constraint tbr_ok : 'TBR Floor' {
      in tbr = tbr_val.value;  in tbr_floor = tbr_floor_val.value; }
  ```

**Capture-probe evidence (owner-mandated; run at `512786c`).** Applied the above to a scratch copy of the staged models tree and ran the D1 capture:

- **Gate A cleared.** The INV-2 abort (`beta_ok.beta: unresolved actual 'beta'`) is gone. A capture with lowering deferred (`lower_constraints_enabled=False`) **succeeds and carries all five constraint facts**, with the rewired actuals captured exactly: `beta = beta_val.value`, `beta_limit = beta_limit_val.value`, `wall_load_limit = wall_load_limit_val.value`, `tbr = tbr_val.value`, `tbr_floor = tbr_floor_val.value`; `net_positive`/`recirc_ok` unchanged (`pb.p_net`/`pb.rec_frac`). Evidence: `.orchestrate-logs/wi027_probe/probeA_deferred.snapshot.json` (5 usages), `.../probe_deferred.py`.
- **Gate B then surfaced** (see the premise flag above): a *lowering-ON* capture, which the emission path needs, aborts on the whole-graph V11 check over the 3 capital-rollup keys before writing a snapshot. `.../probeA.log`, `.../probe_forcelower.py`.

So D7 is **proven to fix Gate A and to produce correct constraint facts**; it does not, by itself, make constraints emit — that is gated by Gate B, parked above. D7 is a prerequisite for every Gate-B resolution option, so it is recorded as settled.

**Rejected alternative — fold the value inline** (`calc beta_val : 'Scalar Value' { in v = 0.0276; }`, drop the standalone attribute). Also resolves Gate A, but moves the value + MR-4 citation off the named design attribute onto a calc input binding, weakening traceability and duplicating nothing gained. The design-attribute-as-source form (chosen) keeps the documented value where it has always lived.

## Prototype status

**CORRECTION (2026-07-19):** the original assessment below was **wrong**. It claimed no syside spike was needed because the IFE acceptance proved the machinery for our forms. It does not: the IFE constraint operands are calc outputs / free no-default inputs, so IFE exercised neither Gate A (literal-valued design-attribute actuals) nor Gate B (V11-bridge coexistence). The capture probes this amendment ran are the missing spike; they found both gates. The paragraph below is retained struck-through-in-spirit as the record of the error.

~~**No syside spike run — justified by proven precedent plus a static check, per the brief's "reuse the IFE evidence rather than re-spike."**~~ The constraint-exec constructs (predicate compilation, per-constraint modules, aggregator, exit-point wiring, three-valued verdicts, violated-never-raises) are proven by the IFE acceptance (2294/2301). The one new-to-stellarator seam — *does our V11 bridge path emit constraints, or does the CLI do it in a step the bridge omits?* — is resolved by static inspection: constraint emission lives inside `_generate_schemas` / `_generate_modules` / `_generate_pipeline` (`cli/__init__.py:338,363,522`), all of which `bridge_v11_generate.py:112-121` calls, gated only on the snapshot's constraint catalog. The second seam — handwritten-impl coexistence — is orthogonal (`preserve_handwritten` restores one hand impl file; constraint modules are separate generated files). **The remaining uncertainty is entirely covered by the MR-5 bars at implement** (bit-exact, offender list, WI-022 hash, handshake diff), which are the true acceptance gate. Running syside here would reproduce, at a license cost, what the IFE acceptance already established and what the bars will confirm on the real regen.

## Implementation checklist (phased)

1. **Un-strip (MR-3, Decision 5).** In both staged twins, delete the DEMO NOTE strip comments and un-comment the five asserts. Verify the viability regions are byte-identical to canonical; the two capital-rollup DEMO NOTEs remain the only staged divergences.
2. **Recapture snapshot (Decision 1).** `sysml-codegen snapshot -m exploration/stellarator_e2e/models -o …/stellarator.snapshot.json`, **no `--design-path-filter`**. Confirm the new snapshot carries five constraint facts (`beta_ok`/`net_positive`/… present; `constraint_lowering_mode: applied`).
3. **Regenerate (Decision 1, Pin).** Pin sysml-codegen at `512786c`; record commit + `git status`. Run `bridge_v11_generate.py`; confirm **exactly 3** bridged offenders and that `generated/modules/constraints/` + a `ConstraintReportAggregatorModule` now exist and the pipeline YAML declares five `ConstraintEvaluation` + one `ConstraintReport` exit points.
4. **Harness adapters (Decision 2/3).** Add the two IFE-mirror exit-path fixes and the verdict-harvest + parity assertion to `run_stellaris.py`, marked `# CONSTRAINT-EXEC`. Verify `patch_bop_wiring()` preserves the constraint/aggregator nodes.
5. **Execute + verify (Decision 6).** Run via `exploration/pipeline_spike/.venv-exec/bin/python`. Check: five verdicts all `satisfied`, `headline=all_satisfied`; oracle bit-exact; handshake diff empty; IFE anchors; offender list = 6; WI-022 hash; MR-2 grep clean. Fill SV-033.
6. **Records.** Commit pin + defect-register outcome in the item record and SV-033; `/plan-model` decides MR-2's PR-XXX promotion.

## Risks

1. **Numeric shift from `6db3212 → 512786c`** (low/high). F-series is asserted non-numeric; gate = MR-5.1 + MR-5.4. Shift ⇒ surface to orchestrator, not re-baseline.
2. **`patch_bop_wiring` drops constraint nodes** (low/medium). The YAML rewrite could omit the new nodes. Mitigation: checklist step 4 verifies the rewritten YAML retains all five constraint modules, the aggregator, and their exit points.
3. **Exit-path adapter creep** (low/low). The two `run_stellaris.py` fixes must read generated verdicts only — never compute a viability comparison (MR-2) and never touch the injection map (MR-5.2). Mitigation: adapters marked, grep sweep in step 5.
4. **A non-satisfied verdict** (low/informational). MR-4 governs: record and surface; the design-point actuals sit off every bound, so `indeterminate` would point at a missing operand (codegen), `violated` at the model — both are findings to keep.

## Traceability

- Governing: `.project/concepts/stellarator-mbse-demo.md` criterion 2; spec `work/active/WI-027_demo-constraint-execution/spec.md`; orchestration `work/orchestration/demo-constraint-execution.md`.
- Precedent (evidence, not path-to-copy): `~/1cfe/fusion-tea/exploration/ife_e2e/study/findings.md`, `generated/schemas/constraint_types.py`, `generated/modules/constraints/`.
- Toolchain: sysml-codegen `constraint-exec-epic` @ `512786c`; emission sites `cli/__init__.py:338/363/522`; bridge `exploration/stellarator_e2e/bridge_v11_generate.py:110-124`.
- Defect register: `~/1cfe/sysml-codegen/.project/backlog/epic_constraint_pr_wave_remediation.md` (R-1…R-12) — all NOT-HIT (§Decision 4).
- Standing bars: `work/orchestration/stale-basis-recompute.md §inherited`; WI-025 record `work/completed/20260718_WI-025_stale-basis-pass-through-recompute/`.
- Protocol: `knowledge/holdout/aries-cs/PROTOCOL.md` §3 (barred, honored).

## Validation Report

- **Prototype status:** the capture probes (this amendment) are the spike. Gate A **PASS** (D7 rewiring resolves the actuals; five facts captured correctly). Gate B **FAIL/BLOCKED** — lowering-ON capture aborts on the V11-bridge incompatibility; emission is not reachable in-scope. The original "PASS by proven-precedent" claim was wrong (§Prototype status correction).
- **Defect-register check:** the twelve *registered* R-series defects are NOT-HIT against the five forms (§Decision 4 table). **But the probes found a NEW, unregistered defect — Gate B** (V11-bridge/occurrence-table incompatibility), filed to CODEGEN_FINDINGS #9 addendum. This IS a premise flag (top of doc).
- **Files this design implicates (implement):** un-strip — staged `mfe_plant.sysml`, staged `stellarator_plant.sysml`; recapture — `stellarator.snapshot.json`; regenerate — `generated/**` (additive: constraint modules, aggregator, evidence schemas, pipeline exit points); harness — `run_stellaris.py` (three marked adapters). Untouched: canonical `models/`, `verify_stellaris.py` (kind), `handshake_1costingfe.py` (expected), `handshake_comparison.json` (must stay byte-identical).
- **Bars deferred to implement (the real gate):** oracle bit-exact, offender list = 6, WI-022 hash, handshake empty diff, IFE anchors, pytest tally, MR-2 grep — recorded in SV-033.

**NOT ready for `/plan-model` on the emission path.** D7 (Gate-A fix) is settled and proven; the emission mechanism (D1) and validation (D6) are **parked** pending the owner's Gate-B decision (premise flag, top). Once Gate B is resolved, the parked conclusions and the existing plan's Phases 2–5 resume from D7. `/review-model` available for independent review of D7 and the Gate-B surfacing.
