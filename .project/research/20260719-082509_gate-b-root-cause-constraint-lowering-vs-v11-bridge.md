---
date: 2026-07-19 08:25 PDT
researcher: Claude
topic: "Gate B root cause — constraint lowering vs the V11 generation-time bridge (WI-027)"
tags: [research, wi-027, sysml-codegen, constraint-execution, v11, root-cause]
status: complete
last_updated: 2026-07-19
---

# Research: Gate B root cause — constraint lowering vs the V11 generation-time bridge

**Date**: 2026-07-19 08:25 PDT
**Researcher**: Claude
**Research type**: Integration / toolchain root-cause
**Decides nothing.** This informs the owner's option 1 / 2 / 3 ruling on the WI-027 Gate-B blocker. Section 5 is my `[AGENT]` recommendation, clearly marked.

**Evidence discipline.** Every claim carries a `file:line` or a commit hash. `VERIFIED` = I ran it or read it this session. `INFERRED` = reasoned from verified facts, marked as such. `sysml-codegen` was read-only throughout — nothing mutated, no checkout moved HEAD. Git CLI was blocked by the sandbox for me and for both sub-agents, so commit provenance (Section 2) is reconstructed from the item's own audit record and the `.git/logs/HEAD` reflog read as a file, not from `git show` diffs — this is flagged where it matters.

---

## Research question

Fully root-cause the WI-027 Gate-B blocker: (1) plain-English mechanics with runnable examples; (2) is this a codegen flaw, and how did it slip through sysml-codegen's heavy test/review process; (3) the model-side workaround; (4) a complete option-1 design handoff for sysml-codegen; (5) a recommendation.

## Summary

- **What breaks, in one sentence:** the moment the five viability asserts are live, snapshot *capture* runs a whole-graph coverage check that trips on three unrelated capital-rollup keys the demo's bridge is designed to fill later, at *generation* — so capture aborts before it can write a snapshot that carries the constraints.
- **The collision is a timing mismatch on one function.** `collect_uncovered_params` is the check. It runs at two moments: at **generation** (`cli/__init__.py:277`), where the bridge is allowed to satisfy it by filling placeholders; and — only when constraints are present — at **capture**, inside `extend_graph_with_constraints` (`constraint_lowering.py:1348`), where no bridge seam exists. Same function, wrong time.
- **Verdict: a codegen scope gap, on top of a codegen limitation — not a model defect.** The whole-graph reach of the capture-time check was never a considered decision. It was inherited verbatim from a spike prototype, its design justified it only for the *newly-minted* constraint inputs, and no fixture in the corpus could ever exercise the over-broad reach. The demo's bridge is a reasonable workaround to a *separate* codegen limitation (cross-part rollup can't be wired — WI-015 finding #4), and that bridge pattern was never filed upstream, so codegen never designed for it.
- **The workaround (option 2) is numerically safe and reversible.** Give the two rollup attributes placeholder defaults in the staged twin. The harness already overwrites those values in the final pass, so every executed number is bit-identical. The cost is a model wart in an out-of-scope region and a codegen-appeasing-edit precedent.
- **The upstream fix (option 1) is small and correct.** Scope the capture-time check to the inputs the constraints actually add, and leave pre-existing coverage to the generation gate that already owns it — which is exactly what the check's own stated intent (INV-6) describes.

---

## 1. Plain-English mechanics — what doesn't work, and why

### The mental model: capture, then generation, are two separate moments

Codegen runs in two phases, at two different times, on the same model:

1. **Capture** (`sysml-codegen snapshot`) reads the `.sysml` files, resolves everything it can, and writes `stellarator.snapshot.json`. The snapshot — not the `.sysml` — is codegen's real input from here on (`bridge_v11_generate.py:73` builds its graph from the snapshot).
2. **Generation** (`bridge_v11_generate.py`) reads that snapshot and writes the executable Python package.

The demo's whole-plant package has one thing codegen cannot do on its own: the **cross-part capital rollup** (WI-015 finding #4). Three inputs — `contingency__direct_subtotal`, `indirect__direct_cost`, `lcoe_calc__total_capital` — are sums that reach across parts, which codegen can't compile into a wired channel. So in the staged model those attributes are plain inputs with no value (`mfe_plant.sysml:409` `attribute direct_capital : Real;`, `:434` `attribute total_capital : Real;`). They are deliberately left empty at capture and **filled at generation** by the bridge, which drops in a placeholder the harness later overwrites with the real sum. This is the sanctioned "V11 bridge" pattern.

### What the coverage check demands, and when

The check is one function: `collect_uncovered_params(graph)` (`graph_builder.py:800-845`, VERIFIED). It walks every module input and flags any input that is all three of:

- wired to an entry-point key that "fell through" resolution (`qn in graph.fallback_entry_points`),
- whose entry point carries **no value** (`default_value is None` — "valueless"),
- and is actually referenced by a surviving module.

In plain terms: *"this module reads a key that nobody will put in the JSON, so the pipeline will `KeyError` at load."* The three capital-rollup keys are exactly this shape at capture time — valueless, wired, fell-through — because the bridge hasn't run yet.

The function itself raises nothing (it is pure; `graph_builder.py:803-804`). Two callers turn its result into a hard error:

- **Generation gate** — `_reconcile_params_coverage` (`cli/__init__.py:243`, raise at `:277-289`, VERIFIED). This is the *right* place: the bridge fills the three placeholders (`bridge_v11_generate.py:81-97`) and then calls this exact function (`:111` `_reconcile_params_coverage(graph)  # must pass now`). By the time the gate runs, the keys are covered. This has always worked.
- **Capture-time check** — the last three lines of `extend_graph_with_constraints` (`constraint_lowering.py:1348-1350`, VERIFIED):
  ```python
  uncovered = collect_uncovered_params(extended)
  if uncovered:
      raise _generation_error(f"V11 coverage violations in extended graph: {uncovered}")
  ```
  This runs on the **whole** extended graph — every pre-existing module plus the new constraint nodes (`extended` is built from a deep copy of all `graph.modules` at `:1207` plus the appended constraint/aggregator nodes, with `fallback_entry_points` carried over verbatim at `:1344`). So it flags the three pre-existing rollup keys, which have nothing to do with the constraints.

### Why the two collide — the guard is the whole story

`extend_graph_with_constraints` is called **only when constraints exist** (`pipeline_builder.py:1001` `if concrete_constraints:`, VERIFIED). That single guard explains everything:

- **Asserts stripped (WI-025, and every prior stage):** no constraints → `extend_graph_with_constraints` never runs at capture → the capture-time coverage check never runs → the three rollup keys ride through capture untouched → the bridge fills them at generation → the generation gate passes. **Works.**
- **Asserts live (WI-027):** constraints present → `extend_graph_with_constraints` runs at capture → its tail-end whole-graph check trips on the same three pre-existing rollup keys → **capture aborts before writing the snapshot.** The constraints themselves are fully covered; they are not the problem. Turning the asserts on is simply what *switches the capture-time check on*, and that check re-litigates coverage the generation gate already owns.

Direct evidence, the D7-rewired lowering-ON capture aborting at exactly this line (`.orchestrate-logs/wi027_probe/probeA.log:74-76`, VERIFIED):
```
File ".../analysis/constraint_lowering.py", line 1350, in extend_graph_with_constraints
    raise _generation_error(f"V11 coverage violations in extended graph: {uncovered}")
CodeGenerationError: V11 coverage violations in extended graph: [
  UncoveredInput(module='...__contingency', input='direct_subtotal', ...),
  UncoveredInput(module='...__indirect',    input='direct_cost',     ...),
  UncoveredInput(module='...__lcoe_calc',   input='total_capital',   ...)]
```

### Why "defer lowering, then bridge, then force-lower" does not rescue it

The obvious escape — capture with lowering off (so the check is skipped), let the bridge fill the placeholders, then lower — is a dead end. Proven end-to-end (`.orchestrate-logs/wi027_probe/probe_forcelower.py`, re-run this session, VERIFIED):
```
mode in snapshot: grandfathered_off
facts usages: 5
uncovered BEFORE placeholder fill: ['...contingency__direct_subtotal', '...indirect__direct_cost', '...lcoe_calc__total_capital']
bridged placeholders: 3
uncovered AFTER placeholder fill: []          <- filling DOES clear coverage
FORCE-LOWER FAILED: FrozenOccurrenceIndexCorruptionError
  owner 'mfe_plant__MFE_Power_Plant' was queried but is absent from the frozen occurrence table
```

Two facts here:

- Filling the placeholders **does** clear the coverage check (`uncovered AFTER placeholder fill: []`). So the check is genuinely satisfiable — just not at capture.
- But a deferred (lowering-off) capture records **no occurrence table**. The occurrence table is built only inside the lowering call (`pipeline_builder.py:888-898` wraps the live index in a `RecordingOccurrenceIndex` and captures `part_occurrences = recorder.recorded`, VERIFIED). With lowering off, that never runs, so `part_occurrences` stays `{}`. A later force-lower reads occurrences through a `FrozenOccurrenceIndex(snap["part_occurrences"])` (`graph_rebuild.py:214`), and `FrozenOccurrenceIndex.occurrences_of` **raises** for any owner missing from the table rather than returning empty (`part_instance_index.py:415-421`, VERIFIED) — a deliberate corruption guard. So the moment force-lowering queries any owner, the empty table raises. The occurrence table and V11 coverage are produced together only during a fully-covered, lowering-ON capture — which the bridge pattern structurally prevents.

This is why every in-scope path is blocked, and why the item surfaced rather than designed around it.

### Minimal runnable example

Two pieces of runnable evidence, both license-free and in scratch dirs (`.orchestrate-logs/wi027_probe/`):

**(a) The mechanism, isolated to one function** — `minimal_coverage_collision.py` (VERIFIED, runs clean). It builds the smallest graph carrying the demo's shape: one pre-existing cost-rollup module reading `total_capital` from a valueless fell-through entry point (the generation-time-bridged key), no constraints needed to show the trap:
```
(A) capture time  -- placeholder NOT filled (what extend_graph_with_constraints sees):
    uncovered = ['plant_params.plant__lcoe_calc__total_capital']
    -> extend_graph_with_constraints would RAISE (1 offender)
(B) generation time -- bridge filled the placeholder (what the V11 gate sees):
    uncovered = []
    -> generation-time V11 gate PASSES (0 offenders)
```
Same key, same graph, two moments. (A) is the state the capture-time check sees when constraints are present; (B) is the state the generation gate sees after the bridge runs. The failure is entirely "the check runs at moment (A) instead of (B)."

**(b) The full collision on the real package** — `probeA.log` (D7-rewired, lowering-ON capture aborting at `constraint_lowering.py:1350`) and `probe_forcelower.py` (the deferred-then-force-lower dead-end above). These are the "with the bridge" failure and the "the fill does work, just too late" proof, on the actual stellarator snapshot.

The "same example without the bridge, showing success" is the WI-025 baseline itself: with the asserts stripped, the identical package captures and generates cleanly through this exact chain — because the capture-time check never runs (the guard above).

### Gate A, for contrast (one paragraph)

Gate A is a *different*, already-resolved blocker, worth stating so the two are not confused. INV-2 is codegen's strict-resolution rule: a constraint's input value must resolve to something the model actually carries (a channel, a design attribute, or a modeled literal default) — codegen must **never** invent a placeholder entry point for it (`dependency_backtracker.py:56-65`; concept doc quote at `.project/concepts/constraint-execution-and-design-space-studies-claude.md:76` — *"Strict resolution for assertion inputs: fail, never synthesize"*). The stellarator's `beta_ok`/`tbr_ok`/`wall_load_ok` read design attributes that carry literal defaults (`beta = 0.0276`, etc.) directly as constraint actuals, which the strict resolver refuses → capture aborts with `unresolved actual 'beta'` (`dependency_backtracker.py:62`). The owner ruled a representation-only fix (D7): route each literal through a passthrough calc (`calc def 'Scalar Value'`) so the actual becomes a calc output. Proven to work — a D7-rewired capture carries all five facts correctly (`probeA_deferred.snapshot.json`, 5 usages). Gate A is resolved. **Gate B is what remains, and it is downstream of Gate A** — you only reach the coverage check after the actuals resolve.

---

## 2. Is this a codegen flaw, and how did it slip through?

### Where the flaw lives

`constraint_lowering.py:1348-1350`, inside `extend_graph_with_constraints` (defined `:1177`), calling `collect_uncovered_params` (`graph_builder.py:800-845`) on the whole extended graph. VERIFIED at HEAD `512786c`.

### The origin: an unexamined default, copied verbatim

This whole-graph reach was **never a considered scoping decision.** The trail (all VERIFIED by file read; commit hashes from the reflog file, not `git show`):

- **The check was born in an earlier epic, for a different job.** `collect_uncovered_params` came from the UPSTREAM-FINDINGS epic's warning-reconciliation item as a whole-graph "params-coverage hard check" to catch a specific dangling *calc* input (`epic_upstream_findings.md:280` — *"any module input referencing `*_params.X` with no matching key … is an error … must catch the committed catf_mfe dangling `magnet_volume` input"*). Its founding premise: **a valueless-wired input is a guaranteed runtime `KeyError`, always a bug to catch loudly.**
- **The constraint path copied it verbatim from a spike.** `extend_graph_with_constraints` was created by Item 5 ("constraint-lowering") of the CONSTRAINT-EXEC epic on 2026-07-13 (commits `ab69fea6` → `0d6eba1` → `dd181ae`, per `.git/logs/HEAD` and the item audit `audit.md:6`). It is a byte-for-byte copy of the S4 spike prototype's construct (`spike-vertical-slice-constraint-execution/s4_lib.py:603-605`, identical but for the exception type), and the design *mandated* the copy — `design.md:332` *"P3 minting mirrors S4 exactly."*
- **The design justified the check only for the constraint-added inputs.** The sole recorded rationale is INV-6 (`design.md:294-295`, VERIFIED): *"The extended graph … has zero V11 uncovered params. Constraint consumers must be present to cover the minted EPs."* The intent is about the **newly minted** constraint entry points. Whole-graph re-application onto pre-existing inputs is never discussed, weighed, or ruled on. **The code's scope is wider than its stated intent.**
- **The spike could never have caught it.** The S4 vertical slice ran the WI-014 toy, whose base graph is fully covered — so the whole-graph reach onto a pre-existing uncovered input simply never occurred (`spike-vertical-slice-constraint-execution/findings.md:36-37` reports only *"V11 coverage … pass on the extended graph"*).
- **No spike examined the scope.** Across S1–S6 in the concept design, coverage is discussed only as the *eligibility* profile check (a different check; concept doc `:90`) and at the invariant level (`:395` *"V11 … pass on the extended graph"*). Whole-graph-vs-subset is never raised.

### How the review and test process missed it

This is the part worth being precise about, because the repo does have heavy testing and review. It slipped through for one structural reason: **no fixture anywhere pairs a pre-existing, generation-time-bridged (valueless-deferred) input with constraints.** The entire corpus encodes the "valueless-wired = guaranteed bug" premise, so the one shape that distinguishes a real bug from a legitimate deferral does not exist to be tested. Per test (VERIFIED by sub-agent, file:line):

- `tests/unit/test_constraint_graph_extension.py` — the direct tests for `extend_graph_with_constraints`. Every fixture is `_empty_graph()` or `_graph_with_producer()`, neither of which sets `fallback_entry_points`. The one "V11 violation" test (`:239-254`) actually exercises `_validate_channel_references` (a dangling module-output channel), **not** `collect_uncovered_params` on a pre-existing uncovered EP. The whole-graph reach is never exercised here.
- `tests/conformance/test_constraint_pipeline_threading.py:54-69` — asserts the constraint fixture's `fallback_entry_points == set()`. A fully-covered base graph by construction; no deferred input.
- `tests/conformance/test_fusion_tea_snapshot.py:18-20` — asserts the committed fusion-tea fixture resolves to *"TRUE ZERO V11 offenders."* The committed acceptance fixture has no capital-rollup deferred inputs. (The three rollup keys appear in **zero** `.py`/`.md` files in the whole codegen repo.)
- `tests/unit/test_uncovered_params.py` — this *does* run the collector against real snapshots with fell-through EPs, and its framing is the smoking gun: fell-through-but-**valued** EPs are not violations; fell-through-**valueless**-wired EPs are treated as *"the intended safety property"* to fire on (`:119-130`, `chain_override_probe`). There is no fixture for "valueless-wired but legitimately filled downstream." The corpus encodes the premise; it cannot test the exception to it.

The acceptance model (IFE) is **structurally incapable** of triggering this. The current IFE acceptance harness generates *"whole-plant with zero V11 offenders"* and feeds *"the GENERATED inputs/*.json exactly as emitted"* with *"NO hand-written input JSONs"* (`~/1cfe/fusion-tea/exploration/ife_e2e/run_anchors.py:7-14`, VERIFIED). IFE's LCOE chain is wired by generated wiring (the Meier chain is closed) — it has no cross-part capital rollup, so no bridge, so no deferred key. Its 2294/2301 pass proves the constraint machinery emits and executes; it proves nothing about the capture-time coverage collision, which its graph shape cannot reach. The design's "the IFE acceptance proves this works" premise was true for emission and false for capture.

### Was fusion-tea's finding #8 ("file upstream") ever actually filed upstream? — No.

VERIFIED absent: the three capital-rollup keys, and every phrasing of the pattern ("file upstream", "finding 8", "capital rollup", "EXPOSE-alias blind", "generation-time bridge"), appear **nowhere** in the sysml-codegen `.project/` or code. The integration gaps that *were* filed and audited (CE-F1/F2/F3 — catalog JSON shape, multi-channel bridging, a hardcoded fixture class name) are unrelated. So the process gap is not just "no fixture" — it is that **the one counterexample to codegen's core premise was discovered downstream, marked "file upstream," and never filed.** That non-filing is itself part of the answer, and it belongs on the record.

### Verdict `[AGENT]`: a codegen scope gap on top of a codegen limitation — not a model defect

Stated plainly, weighing the evidence rather than presuming the framing:

- **It is a codegen flaw**, in the specific sense that the capture-time whole-graph check does more than its own design says it should. Its stated job (INV-6) is to prove the constraints didn't introduce uncovered inputs. Its actual behavior re-audits the entire pre-existing graph's coverage — a job the generation gate (`_reconcile_params_coverage`, the *same* function at `cli/__init__.py:277`) already owns and performs at the moment the bridge is sanctioned to act. Running that audit early, gated only on constraint presence, at a point with no bridge seam, is the defect.
- **It also rests on a second codegen limitation.** The bridge exists only because codegen cannot wire the cross-part capital rollup (WI-015 finding #4, still open). The demo's bridge is a reasonable, sanctioned-at-generation workaround to that limitation — not an anomaly. Calling the bridge "the anomaly" would be backwards: the generation gate explicitly supports it.
- **The model is not at fault.** The five asserts are plain numeric relational comparisons, correctly authored; the rollup attributes are shaped exactly as finding #4 requires. Nothing in the model is wrong.

So: **both a scope gap and a limitation, rooted in codegen.** The consumer pattern is legitimate; codegen simply never designed the capture-time check to coexist with it, and never had a fixture that would have forced the question.

---

## 3. The model-side workaround (option 2), explained

**The change:** give the two rollup attributes placeholder defaults in the **staged twin only**, so the graph is V11-covered at capture:
```
attribute direct_capital : Real = 1.0;   // staged twin, mfe_plant.sysml:409
attribute total_capital  : Real = 1.0;   // staged twin, mfe_plant.sysml:434
```
`direct_capital` feeds two of the three uncovered keys (`contingency__direct_subtotal`, `indirect__direct_cost`); `total_capital` feeds the third (`lcoe_calc__total_capital`). With both carrying a default, `collect_uncovered_params` returns empty at capture, `extend_graph_with_constraints` passes, and the lowering-ON capture succeeds — carrying both the five constraint facts and the occurrence table. From there the existing chain generates and executes.

**Why zero numeric movement — the value path, traced (VERIFIED in `run_stellaris.py`):** the placeholder is only ever seen by the throwaway first pass. The runner is two-pass:
- **Pass A** (`run_stellaris.py:178-180`) runs with placeholder rollup values and harvests the per-account costs.
- **Glue-2** (`:187-210`) computes the real `direct`, `contingency`, `indirect`, `total` from the generated module outputs and **overwrites** the three keys in the input JSON:
  ```
  {P}contingency__direct_subtotal : direct
  {P}indirect__direct_cost        : direct
  {P}lcoe_calc__total_capital     : total
  ```
- **Pass B** (`:213-215`) — the canonical final run — reads those overwritten real values.

The placeholder (whether the bridge fills it at generation, as today, or the model carries it as a default, under option 2) lands only in Pass A's inputs. Pass B — every headline number, every oracle-checked channel — uses the harness-computed real rollup. The two sources of the placeholder are indistinguishable to Pass B. So the executed numerics are bit-identical; the oracle bit-exactness bar (MR-5.1) holds unchanged.

**What else changes:** the bridge currently asserts it bridges *exactly 3* offenders (`bridge_v11_generate.py:91-92`). Under option 2 the model covers those keys, so the bridge finds **0** to fill — its offender-count expectation must change 3 → 0 (or the fill step is removed). This is a harness edit, in `exploration/stellarator_e2e/`, in scope for the demo package.

**Revert path once option 1 lands:** delete the two `= 1.0` defaults (restore the plain-input form), restore the bridge's 3-offender expectation. Clean and local — two model lines and one harness assertion.

**Honest costs:**
- **Model wart.** A rollup sum attribute reading `= 1.0` is misleading to a human who doesn't know the harness overwrites it. It sits in the staged twin, not canonical, so canonical stays clean — but the twin is what a reader of the demo package sees.
- **Out-of-scope-region touch.** This edits the capital-rollup region (WI-015 finding #4), which WI-027's spec names Out-of-Scope and "left as-is." Mitigating: `direct_capital`/`total_capital` are *already* a sanctioned staged↔canonical divergence (converted from formula to plain input); option 2 deepens an existing documented divergence rather than creating a new one. It still requires the owner to widen WI-027's scope.
- **Precedent risk.** "Add a placeholder to appease codegen" is a pattern that, repeated, accretes model warts that track codegen limitations rather than the domain. Worth naming so it is a conscious, recorded choice, not a silent habit.

---

## 4. Option-1 design package — complete handoff for sysml-codegen

Everything a sysml-codegen design stage needs to fix this at the source, so they start from facts.

### 4.1 The problem, restated for their repo

`extend_graph_with_constraints` (`constraint_lowering.py:1177`) re-runs the whole-graph `collect_uncovered_params` at its tail (`:1348-1350`). When constraints are present, this runs at **capture** and rejects pre-existing valueless-fell-through inputs that a downstream consumer legitimately fills after capture (at generation, through the `_reconcile_params_coverage` gate the consumer already satisfies). The check's scope exceeds its stated intent (INV-6 covers the *minted* constraint EPs), and it duplicates a gate that already runs at the correct moment.

### 4.2 The invariant landscape (what any fix must not break)

- **INV-2 — no fallback synthesis for a constraint actual.** Concept doc `:76`, `:148` (*"Constraint actual resolution has no textual fallback and no entry-point synthesis; unresolved means generation error"*); enforced `dependency_backtracker.py:56-65`, `constraint_lowering.py:288-296`. A fix must **not** open any path where an unresolved constraint actual gets a synthesized default. The three rollup keys are filled by the model/bridge — not by relaxing strict resolution. This is the bright line: scoping the *coverage* check is fine; softening *actual resolution* is not.
- **INV-6 — the extended graph is channel-ref-valid and V11-clean for the constraints it adds.** `design.md:294-295`. This is the intent the fix should preserve exactly — the check should still catch a constraint that mints its own uncovered EP.
- **S1–S6 carry-forwards that constrain a fix** (concept doc, VERIFIED):
  - **S2 (`:279`):** the predicate compiler is *not* a unit safety net — the eligibility/profile gate must run strictly before compilation. Independent of coverage scope, but do not fold coverage and eligibility into one pass.
  - **S3 (`:289`):** occurrence identity must key by owning definition + feature, and live/snapshot catalog ordering must be byte-identical. A coverage-scope change must not perturb occurrence identity or ordering.
  - **S4 (`:297`, `:299`):** live and from-snapshot packages must stay byte-identical (24/24 artifacts, same fingerprint); strict resolution needed no fallback anywhere. The fix must hold this parity.
- **Byte-identity / determinism gates.** Live vs from-snapshot regeneration must be byte-identical — asserted `graph_rebuild.py:226-229`, `pipeline_builder.py:874-876`; enforced by `test_snapshot_constraint_parity.py`, `test_constraint_snapshot_identity.py`. Serializer determinism: `part_occurrences` emitted sorted (`serializer.py:114-119`), sets → sorted lists (`:185-187`).
- **Snapshot version / mode gates.** `SNAPSHOT_FORMAT_VERSION = 3` with a hard reject on mismatch *before* any field deserialization (`snapshot/__init__.py:19`, `loader.py:718-732`) — there is no v2/v3 coexistence, so any change to a required v3 section shape forces recapture of every committed fixture snapshot in the same change. The lowering-mode enum is **closed**: `{"applied", "grandfathered_off"}` (`snapshot/__init__.py:28-30`); a third mode would touch the loader gate and this enum. **Implication: prefer a fix that needs no snapshot schema change.**

### 4.3 Candidate fix shapes, with trade-offs

Ordered by my `[AGENT]` preference. All four are viable; (a) is the cleanest match to the check's own intent.

**(a) Scope the constraint-path check to constraint-added inputs only. `[AGENT]` recommended.**
- *What:* in `extend_graph_with_constraints`, replace the whole-graph `collect_uncovered_params(extended)` with a check restricted to the inputs the constraints introduced — the inputs of the appended CONSTRAINT / REPORT_AGGREGATOR modules, plus any pre-existing input newly wired as a constraint operand. Leave pre-existing unrelated uncovered keys to the generation gate (`_reconcile_params_coverage`), which the bridge satisfies.
- *Why it's right:* this makes the check do exactly what INV-6 says (prove the constraints didn't add an uncovered input) and nothing more. With constraints, capture then treats pre-existing keys the same way it already does *without* constraints — consistent behavior across the guard at `pipeline_builder.py:1001`.
- *Invariants touched:* INV-6 preserved (still catches constraint-minted uncovered EPs). INV-2 untouched. Byte-identity: unaffected — the emitted graph is identical; only the accept/reject decision at capture changes for pre-existing keys. No snapshot schema change.
- *Blast radius:* one function's tail. Needs a scoped variant of `collect_uncovered_params` (filter by a module-name set, or by the minted-EP QN set) — a few lines in `graph_builder.py` + the call site.
- *Test surface:* two new fixtures (Section 4.5).

**(b) Remove the capture-time re-run; rely on the generation gate.**
- *What:* delete `:1348-1350` entirely; let `_reconcile_params_coverage` at generation be the sole V11 enforcement (as it already is for the no-constraint path).
- *Trade-off:* simplest diff, but drops INV-6's capture-time self-check for constraint-minted EPs — a constraint that mints its own uncovered EP would now be caught only at generation, not at capture. Slightly later failure, arguably acceptable since generation still catches it, but it weakens a stated invariant. Prefer (a) unless the team decides INV-6-at-capture isn't worth keeping.

**(c) A declared "deferred-input" annotation.**
- *What:* let a consumer mark specific keys as "filled at generation"; the coverage check skips annotated keys at capture.
- *Trade-off:* most explicit and self-documenting, but heaviest: the annotation must live in the snapshot (v3 schema change → recapture every fixture, per 4.2), a new field to serialize deterministically, and a new closed vocabulary. Only worth it if "deferred inputs" become a first-class, multi-consumer concept. Overkill for one bridge.

**(d) A capture-time bridge hook.**
- *What:* a seam that lets a consumer inject placeholder defaults before the capture-time check.
- *Trade-off:* biggest new surface (a plugin point inside `build_pipeline_context`), and it moves consumer-specific logic into capture. It also does not remove the from-snapshot re-check (Section 4.4). Least attractive.

### 4.4 Affected code sites (VERIFIED at `512786c`) — note there are **two** call sites

A fix to (a) or (b) must address **both** places `extend_graph_with_constraints` runs, or the from-snapshot path will still trip:

- **Capture path:** `pipeline_builder.py:1001-1004` → `extend_graph_with_constraints` → check at `constraint_lowering.py:1348-1350`.
- **From-snapshot path:** `graph_rebuild.py:225` calls the same `extend_graph_with_constraints` (when the snapshot's mode is `applied`), so it runs the same check at `:1348` — **before** the bridge's placeholder fill in `bridge_v11_generate.py`. A fix that only touches the capture path leaves the bridge's own `build_pipeline_context_from_snapshot` (`bridge_v11_generate.py:73`) still aborting. Fixing the function body (option a/b) covers both call sites at once, which is another reason to prefer changing the function over guarding a call site.
- **The correct, unchanged gate:** `_reconcile_params_coverage` (`cli/__init__.py:243`, raise `:277-289`) — leave this exactly as is. It is where coverage *should* be enforced, and where the bridge satisfies it.
- **The collector:** `collect_uncovered_params` (`graph_builder.py:800-845`) — the scoped variant for option (a) lives here.

### 4.5 The fixture-corpus gap and the regression tests a fix must add

**The gap, named precisely:** no fixture pairs a pre-existing valueless-fell-through (generation-time-bridged) input with constraints. Every constraint fixture starts fully covered; every whole-graph V11 fixture treats a valueless-wired input as an intended bug. The distinguishing shape does not exist in the corpus.

**The fixture that would have caught this** (and the regression a fix must add): a synthetic `ComputationGraph` that has all three of — (1) a QN in `fallback_entry_points`, (2) an `EntryPoint` with `default_value=None` in a group, (3) a surviving pre-existing `ModuleInput` wired to it — **plus** a constraint. Assert that `extend_graph_with_constraints` **succeeds** (the pre-existing key is left for the generation gate). Add the companion negative: a constraint that mints *its own* uncovered EP → assert `extend_graph_with_constraints` still **raises** (INV-6 preserved).

**Where these go (VERIFIED idiom):**
- Home for the `extend` call: `tests/unit/test_constraint_graph_extension.py` (smallest existing example at `:81`, `test_module_output_input_wires_producer_channel_no_mint`, `extend` call at `:94`; helpers `_empty_graph()` `:27`, `_graph_with_producer()` `:31`, `_cc()` `:49`).
- Idiom for seeding the uncovered-key shape: `tests/unit/test_uncovered_params.py` (imports `EntryPoint`, `InputSource`, `ModuleInput`, `ParameterGroup` at `:42-51` and hand-builds the fell-through/valueless/wired shape). Combine the two: build the uncovered shape from `test_uncovered_params.py`, feed it through the `extend` call from `test_constraint_graph_extension.py`.
- Conformance parity: a real-snapshot fixture with a deferred rollup key + constraints, run on both the live and from-snapshot paths, to hold the S4 byte-identity gate.

### 4.6 Where this slots against the in-flight remediation wave

`.project/backlog/epic_constraint_pr_wave_remediation.md` (Status: Draft, P0; eight items, R-1…R-12). This blocker is **not** in that epic's declared scope — the epic never mentions the whole-graph coverage scope, the three rollup keys, or the fusion-tea bridge. Slotting (VERIFIED item text):
- **Item 3 (R-4/R-5/R-7) is the primary seam overlap.** It rewrites occurrence-stable identity, the `FrozenOccurrenceIndex` corruption path, snapshot replay, and demand dedup — the exact files a coverage-scope fix lives near (`constraint_lowering.py`, `graph_rebuild.py`, `part_instance_index.py`). Its own note: *"Item 3 lands before Item 5 because both edit lowering and demand-related surfaces"* (`:507`). A coverage-scope fix should **coordinate with Item 3**, ideally landing just after it to avoid churning the same lowering surface twice.
- **Item 5 (R-8/R-9)** shares the lowering surface and modeled-default entry points (R-9 makes modeled defaults reach generated inputs — the same `default_value` field the coverage check keys on).
- **Item 8** is the cross-repo compatibility / live-snapshot byte-parity gate — the fix must pass it.
- **Recommendation:** add a new item to this epic ("scope the constraint-path V11 coverage check to constraint-added inputs"), sequenced immediately after Item 3, gated by Item 8's parity check. Standalone is possible but wasteful — Item 3 touches the same code.

### 4.7 Reproduction, packaged for their repo

- The isolated mechanism as a unit test: port `minimal_coverage_collision.py` into `tests/unit/` using the object-construction idiom above — it needs only `sysml_codegen.resolution` models and `collect_uncovered_params`, no license, no syside.
- The full-package repro is a fusion-tea artifact (`probeA.log`, `probe_forcelower.py`); the unit-level fixture is what belongs in their suite.

---

## 5. Recommendation `[AGENT]` — researcher's view, not a ruling

The owner decides. My read of the evidence:

**The root cause is upstream, and the clean fix is option 1 (specifically shape 4.3(a)).** The check does more than its own design says, it duplicates a gate that already runs at the right moment, and the fix is small, invariant-safe, needs no snapshot schema change, and benefits every future whole-plant consumer — not just this demo. This is the fix that makes the codebase correct rather than the one that makes this one demo pass.

**But option 1 is out of WI-027's scope and lands on sysml-codegen's clock.** It wants a new item in the P0 remediation epic, sequenced after Item 3. If the stellarator demo's Success Criterion 2 must land before that item can, option 1 alone means deferring WI-027 (option 3).

**So my recommendation is a sequence, not a single pick:**

1. **File finding #8/Gate B upstream now, as a new remediation-epic item** (this research is the design package). This is the thing that should have happened when finding #8 was written and didn't. Do it regardless of which demo path is chosen — the non-filing is the real process gap.

   > **DONE, and resolved upstream (2026-07-19).** Filed and fixed in sysml-codegen as lifecycle
   > Item 3. Response: `20260719-222000_gate-b-upstream-filing-response-from-sysml-codegen.md`.
   > **Outcome differs from this report's recommended repair.** A spike proved extension *cannot*
   > introduce a new V11 violation, so the extension-time check was **deleted** rather than scoped
   > to a differential — a differential would have been dead code. Consequences for this report:
   > option 1 shape 4.3(a) is superseded by deletion; the Section 4.5 "required negative
   > regression" (pre-existing unwired key newly consumed by a constraint) has no model that
   > produces it and was not written; the generation gate is unchanged and still strict, so the
   > bridge's fill is still required. Option 2's placeholder defaults are no longer needed.
   > The bridge remains stale against the current API and the cross-part rollup (WI-015 finding #4)
   > is still open — neither is fixed by this.
2. **Choose the demo's near-term path by timeline:**
   - If the demo can wait for the upstream item: **option 3** (defer WI-027 behind the fix), then finish WI-027 through the clean path. Best final state, no model wart.
   - If the demo can't wait: **option 2 as an explicitly interim, reversible bridge** — with the two placeholder defaults recorded as "pending upstream Gate-B fix," the revert path (Section 3) written into the item, and the numeric-neutrality proven by the oracle bar. It is numerically safe today and costs two model lines you delete later.

I would **not** recommend option 2 as a *permanent* resolution — it leaves a codegen-appeasing wart in an out-of-scope region and, repeated, is exactly the precedent to avoid. As a marked, temporary bridge to the upstream fix, it is defensible. The one thing I'd avoid is treating option 2 as "done" and letting the upstream item lapse — that is how finding #8 became invisible the first time.

---

## Code references

**The collision (VERIFIED at `512786c`):**
- `~/1cfe/sysml-codegen/src/sysml_codegen/analysis/constraint_lowering.py:1348-1350` — the capture-time whole-graph V11 check (the flaw).
- `~/1cfe/sysml-codegen/src/sysml_codegen/analysis/constraint_lowering.py:1177,1207,1344` — `extend_graph_with_constraints`; `extended` is the whole graph + constraint nodes.
- `~/1cfe/sysml-codegen/src/sysml_codegen/resolution/graph_builder.py:800-845` — `collect_uncovered_params` (whole-graph iteration; the three violation conditions).
- `~/1cfe/sysml-codegen/src/sysml_codegen/orchestration/pipeline_builder.py:1001-1004` — the `if concrete_constraints:` guard (capture-time call site).
- `~/1cfe/sysml-codegen/src/sysml_codegen/snapshot/graph_rebuild.py:225` — the from-snapshot call site (runs the same check before the bridge).
- `~/1cfe/sysml-codegen/src/sysml_codegen/cli/__init__.py:243,277-289` — `_reconcile_params_coverage`, the correct generation-time gate the bridge satisfies.
- `~/1cfe/sysml-codegen/src/sysml_codegen/orchestration/pipeline_builder.py:888-898` — occurrence table built only inside lowering.
- `~/1cfe/sysml-codegen/src/sysml_codegen/analysis/part_instance_index.py:415-421` — `FrozenOccurrenceIndexCorruptionError` on a missing owner.

**Gate A / INV-2 (contrast, VERIFIED):**
- `~/1cfe/sysml-codegen/src/sysml_codegen/analysis/dependency_backtracker.py:56-65` — strict terminal disposition (the Gate-A abort).
- `~/1cfe/sysml-codegen/src/sysml_codegen/analysis/constraint_lowering.py:288-296` — `resolve_actual` strict ladder terminus.

**Consumer side (VERIFIED):**
- `exploration/stellarator_e2e/bridge_v11_generate.py:73,81-97,111` — the V11 bridge (fills 3 keys, asserts exactly-3, satisfies the generation gate).
- `exploration/stellarator_e2e/run_stellaris.py:178-215` — two-pass runner; glue-2 overwrites the 3 keys in Pass B (the zero-numeric-movement proof).
- `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml:409,434` — the two plain-input rollup attributes (option-2 edit site).
- `~/1cfe/fusion-tea/exploration/ife_e2e/run_anchors.py:7-14` — IFE generates zero V11 offenders, no bridge (why the acceptance couldn't trigger this).

**Process trail (VERIFIED by file read):**
- `~/1cfe/sysml-codegen/.project/concepts/constraint-execution-and-design-space-studies-claude.md:76,90,148,395` and S1–S6 carry-forwards `:242-243,279,289,297-299`.
- `~/1cfe/sysml-codegen/.project/completed/20260713_constraint-lowering/design.md:294-295,332` (INV-6; "mirrors S4 exactly").
- `~/1cfe/sysml-codegen/.project/active/spike-vertical-slice-constraint-execution/s4_lib.py:603-605` (the verbatim-copied prototype).
- `~/1cfe/sysml-codegen/.project/backlog/epic_upstream_findings.md:280` (the check's calc-pipeline origin).
- `~/1cfe/sysml-codegen/.project/backlog/epic_constraint_pr_wave_remediation.md` (Items 3, 5, 8 — slotting).
- Tests: `tests/unit/test_constraint_graph_extension.py:81,94`, `tests/unit/test_uncovered_params.py:42-51,119-130`, `tests/conformance/test_fusion_tea_snapshot.py:18-20`, `tests/conformance/test_constraint_pipeline_threading.py:54-69`.

**Runnable evidence (this session, scratch — `.orchestrate-logs/wi027_probe/`):**
- `minimal_coverage_collision.py` — isolated mechanism, license-free (VERIFIED runs).
- `probeA.log:74-76` — real-package lowering-ON capture aborting at `constraint_lowering.py:1350`.
- `probe_forcelower.py` — the deferred-then-force-lower dead-end (`FrozenOccurrenceIndexCorruptionError`), re-run VERIFIED.

## Open questions / limits of this research

- **Commit provenance is reflog-level, not diff-level.** Git CLI was sandbox-blocked. The Item-5 origin and the `ab69fea6`→`0d6eba1`→`dd181ae` chain come from `.git/logs/HEAD` (read as a file) and the item's own `audit.md:6`, not from `git show`. The code facts are all VERIFIED by direct read at the working tree, which is stated to be `512786c`; the hash itself I could not reconfirm via git.
- **Option-1 fix shapes are analyzed, not prototyped.** Section 4.3 gives shapes, invariants touched, and blast radius; a sysml-codegen design stage should still prototype 4.3(a)'s scoped collector against the two new fixtures before committing.
- **The scoped-collector filter set** (which pre-existing inputs count as "constraint-added" when a constraint reuses an existing channel) is the one detail their design must pin precisely — it is the difference between (a) and (b).

---

ARTIFACT: .project/research/20260719-082509_gate-b-root-cause-constraint-lowering-vs-v11-bridge.md
