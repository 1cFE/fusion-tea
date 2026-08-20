# Audit: Quality Tools and Era Adapter Promotion (RUN-STUDY Item 4)

**Verdict:** PASS
**Audited:** 2026-08-20
**Branch:** `feat/stellarator-mbse-demo`
**Commit:** `f9ac5574`
**Auditor's own suite run:** `uv run python -m pytest tests/study -q -rs` → **273 passed, 0 skipped, 164 s, exit 0** (era worktree present, so nothing skipped even without `STUDY_REQUIRE_ERA=1`). `uv run ruff check scripts/study exploration/stellarator_e2e/studies tests/study` → clean. The 948-point slow test was not re-run, per the brief.

---

## The Point

One good study exists, and every mechanical gate that made it trustworthy is welded into one 450-line package-specific file (`exploration/stellarator_e2e/study/run_design_search.py`). The next study on this package — or the first on any other — starts from zero.

Two of those welds were not merely unshared; they were wrong. The loader accepted a package whose two glue-edited files differ from their sealed hashes and then handed teax the *sealed* fingerprint as the identity of what ran, so a glue edit changed the numbers and changed nothing about what teax thought ran. And a preflight gate asserting "manifest fingerprint matches the package" could only pass by looking away from those two files.

So this item owed the capability three things: generic gates that name no package, a package-local adapter that tells the truth about what it bypassed and states the condition under which it is deleted whole, and proof that the promoted route still produces exactly what the proof-of-life produced.

## Summary

The item delivers all three. The identity seam is real and enforced: the adapter returns a computed effective fingerprint, generic preflight recomputes it from the document's declared inputs plus the bytes on disk rather than trusting the document, and four independent lineage refusals (the glue file plus each of the three declared sources) are held by tests. The promoted route reproduces both committed CSVs byte-for-byte. The four generic modules are grep-clean against the package name, the key prefix, the oracle name, and the adapter import. All eleven design-rev-2 invariants map to enforcing code, and ten of eleven map to a named enforcing test.

The two surfaced findings are honestly recorded and correctly dispositioned, and the `annual_om` catch — the one place a wrong map would have silently shipped a 158% error — is verified here against the oracle source and the package's own generated implementation: **the shipped map is the correct one.**

Four non-blocking notes are below. None changes a number, a verdict, or a gate's behavior. The one worth acting on is a handoff, not a defect: the `p_fus` / `magnet_capital` coverage delta currently lives only in `plan.md`.

## Product Judgment

**Is this the right piece of work? Yes, and it is the work the epic asked for rather than a nearby cheaper thing.**

The load-bearing test is whether the honesty claims are earned or asserted. Three checks say earned:

- **The identity gate recomputes rather than trusts.** `scripts/study/identity.py:217-249` reads every declared file fresh from disk and derives the digest; `assert_matches` (`:288`) compares that to the document's own claim, and `assert_seal_outside_allowed_set` (`:252`) then requires every *other* sealed artifact to match. A document asserting a digest it did not earn fails, and `tests/study/test_preflight_negatives.py:58` proves it.
- **The tool refuses rather than guesses.** `verify.py` requires the package to publish `operand_bindings` and fails closed naming the constraint and the operand on anything unresolved (`scripts/study/verify.py:110-114, 140-171`). The review's L1 finding — that one operand of five constraints resolves to nothing by name at all — is answered by publication, not by a heuristic.
- **Glue honesty is output, not a comment.** `not_independently_verified` carries the g3 rung out of the identity document into the summary (`verify.py:490-494`), and the annex says the same thing in words a reader will meet (`ANNEX.md:176`).

**Product-lens ledger gate: CLEAR.** Scanning every block in `product-lens.md`: `F1` (manifest-staleness half of the fingerprint gate) FIXED and delivered as the `manifest_currency` gate; `F2` (dead-filler check homeless) FIXED and delivered as `assert_schema_fillers_are_dead` running on every load; `F3` (operand resolution) was FIX-BEFORE-PLAN, not BLOCK, and is discharged by D12 as built. No block in the ledger is unresolved. The epic's live gate is recorded CLEAR. **Limit:** I did not run a fresh product-lens pass over the implementation — see *Not checked*.

**No product-drift smell fired.** In particular the acceptance-test signature this repo has been bitten by — a suite green because each assertion is scoped to a different route while two outputs exist for one source — does not apply: promotion equivalence compares the *same* artifact bytes against the committed file (`test_promotion_equivalence.py`), and `test_verify.py:100` asserts the promoted summary against the committed summary's field set and fails if that set moves.

---

## Findings

### Brief item 1 — design-rev-2 invariants mapped to enforcing tests

| Inv | Claim | Enforced at | Test |
|---|---|---|---|
| 1 | Generic means grep-clean | — | `test_generic.py:21-40` — all four new modules in `TOOL_MODULES` (`:9-16`), needles: package name, key prefix, `era_adapter`, `mfe_stellarator`, `lcoe_calc`, `verify_stellaris`, `stellaris`, `exploration`, `stellarator` |
| 2 | The gate recomputes, never trusts | `identity.py:217,288` | `test_identity.py`; `test_preflight_negatives.py:58,118` (message names both digests) |
| 3 | Accept-set is exactly `{TAMPER on the two glue files}` | `era_adapter.py:198-205` | `test_accept_set.py:55` (**read**: mutates a *third* sealed artifact, `inputs/stellarator_plant_params.json`, asserts `SealVerificationError` and that the message names the file and says "beyond the documented glue edits"); `:66` also holds the era-version refusal |
| 4 | Declared source set covers all three files | `era_adapter.py:67-71` | `test_accept_set.py:107`; `test_lineage_refusal.py:110-148` (**read**: parametrized over four sources — the glue file plus each declared source — each asserting the fingerprint moved *and* `IncompatibleStore` on reopen) |
| 5 | Identity continuity across the run | `preflight.py:214-223`, `verify.py:269-273` | `test_verify.py:247` (the pre-capability store, carrying the sealed value, is refused); `test_preflight_negatives.py` "baseline under another identity" |
| 6 | No torn writes | `common.py:96-112` (mkstemp + `os.replace`) | `test_common.py:38`; `test_preflight_negatives.py:105` (D9: document complete, all six gates present) |
| 7 | Interpretive facts never gate | `preflight.py:196-211` (sibling scan cannot fail), `verify.py:359` | `test_verify.py:259` (no completed cases is *mechanical*, not a clean pass) |
| 8 | Adapter-owned facts checked by the adapter | `era_adapter.py:210-211` — both self-checks inside `load()` | `test_accept_set.py:78,89,101`; `test_preflight_gates.py:166` (preflight names none of `simkit`, `era_adapter`, `oracle_entry`, `StudyRunner`, `StudyQuery`) |
| 9 | Unresolved is never assumed | `verify.py:140-171` | `test_verify.py:215,226` — missing `operand_bindings` and an unresolvable key both fail closed naming constraint and operand |
| 10 | Manifest holds no era/glue/allowed-modified/operand-binding fact | manifest as edited | **No dedicated test** — see Note 2. Verified by hand this pass: the manifest contains no era pin, no glue rung, no allowed-modified declaration, and no binding data |
| 11 | Every point through `StudyRunner` | `promotion_equivalence.py:152,161` | `test_preflight_gates.py:166` holds the tools' half; the route's half is structural |

**Extended Invariant 4 (source set) reads correctly.** `DECLARED_SOURCES` is `era_adapter.py`, `oracle_entry.py`, `verify_stellaris.py` (`era_adapter.py:67-71`), which is exactly the set that can move a number fed into a run under D13. `test_lineage_refusal.py:110` proves each one moves the identity; the test redirects the digest lookup at a scratch value rather than editing repo files, which is the same input the recipe sees and is stated in the test's own docstring (`:117-121`).

**Read-set coverage of the identity gate.** `identity.assert_seal_outside_allowed_set` (`identity.py:252-285`) walks *all* of `artifact_hashes`, not a sample, and additionally refuses an allowed-modified path that is not a sealed artifact at all (`:266-271`) — so the exception cannot be widened by declaring a file the seal never covered. Item 3's read-set discipline for the indicator trace is separately held by `test_read_set_coverage.py:58`, which asserts the pinned file list equals exactly what the reader opens.

### Brief item 2 — the four deviations and two findings

All six are recorded at their phase in `plan.md` and re-stated in the whole-item Deviations summary (`plan.md:728`). None is a silent scope change; each names what changed and why.

1. `package_copy` identity convenience moved Phase 0 → Phase 3. Ordering only; the convenience exists (`conftest.py`, `edit_glue(..., reemit_identity=)` with no default, so a negative test must say which half of the gate it aims at). Honest.
2. `test_lineage_refusal.py` builds its store from the era API rather than through the promoted route. Correct and better than the plan's stencil: a test routed through `promotion_equivalence.py` would fail for either reason, and the claim under test is identity binding.
3. Four of Phase 5's five negatives mutate the *documents* preflight reads rather than the package. Correct — it keeps the committed package read-only and leaves the other five gates carrying real outcomes, which is what D9 exists to demonstrate. Three negatives beyond the plan's five were added.
4. Phase 7's manual diff was taken against a promoted-route store, not the committed proof-of-life stores. See (a).

**(a) The proof-of-life stores are refused by `verify.py` — the recorded treatment is right.** The epic's temporary-route integrity criterion (`epic_run_study_capability.md:50`) asks two things of the retained adapter: its route reproduces the committed CSVs byte-for-byte, and a glue or adapter change creates a new effective fingerprint that refuses resume of the old store. Both hold. The refusal of `study/_work/*.db` is the *second* property observed on real evidence: those stores carry `ad912041…`, the sealed value the old loader never earned, so they are a different lineage and verify says so instead of mixing them. Re-verifying them under the promoted identity would have meant either weakening Invariant 5 or re-labelling old evidence — the two things the item exists to prevent. The treatment is recorded in three durable places, not just the plan: `test_verify.py:247` holds it as an assertion, `ANNEX.md:164-168` states it in words, and the CSVs those stores produced are still reproduced byte-for-byte by the promoted route. **Correct per the criterion.**

**(b) The `p_fus` / `magnet_capital` coverage delta — correctly flagged, not absorbed.** The proof-of-life compared five hand-chosen channels; the promoted run compares six (five objective-catalog channels plus `wall_load`, which a binding resolves). `p_fus` and `magnet_capital` are in no objective catalog and no predicate binding, so a generic tool has no basis to compare them. Absorbing them would require `verify.py` to hold two package channel names — a direct Invariant 1 violation that `test_generic.py` would fail. Routing it to Item 3 as a manifest question (add objectives) is the only disposition consistent with the design. **Correctly flagged.** See Note 4 for the one gap: it is flagged only in `plan.md`.

### Brief item 3 — the `annual_om` catch: the shipped map is CORRECT

Verified independently this pass, against source rather than against the note:

- The package channel `…om_cost__annual_om` is produced by `Annual_OM_CostModule` (`generated/pipelines/mfe_stellarator.yaml:363-374`), whose generated implementation computes `om_ref * (p_net * n_mod / ref_net_power) ** alpha + om_direct` and whose docstring says **"CAS70 UNLEVELIZED annual O&M"** (`generated/handwritten/mfe_account_costs/annual_om_cost_impl.py`). The pipeline then feeds that channel into `cas71_calc`, a `Levelized_Annual_CostModule` (`mfe_stellarator.yaml:493-495`) — so the channel is unambiguously the pre-levelization value.
- In the oracle, `annual_om_unlevelized` (`verify_stellaris.py:260-261`) is that same formula term for term, and `annual_om` (`:355`) is `cas70_annual + cas80_annual`, the DCF numerator after levelization.
- `oracle_entry.py:108` maps `annual_om_unlevelized → …om_cost__annual_om`, with the reason stated at the call site (`:105-107`).

**The shipped map is the correct one.** The catch is documented in `ANNEX.md:96-100` with the right lesson attached — "the map is validated against executed evidence, not read for plausibility."

### Brief item 4 — ANNEX.md

Six `##` headings, exactly and only: `§ Declared ties`, `§ Baseline pin`, `§ Oracle`, `§ Validity masks`, `§ Loader exception and glue`, `§ Era pin`. Cross-checked against `runbook.md` as amended (15 steps): its nine annex links at `:64, 103, 117, 130, 147, 160, 173, 213` resolve into exactly those six sections and nothing else. `test_annex.py:35` holds the no-orphan-link direction and `:42` holds the no-seventh-section direction, so both halves are asserted rather than asserted once.

**Deletion condition:** stated in `ANNEX.md:178-186` under `### Deletion condition` inside `§ Loader exception and glue` — not a seventh section — and again verbatim in `era_adapter.py:3-9`. Both name the stock `ProvisionalPackageLoader` with `strict=True`, deletion whole, the swap to the sealed emitter, `promotion_equivalence.py` retiring with it, `oracle_entry.py` staying, and "no partial retirement and no dormant compatibility branch."

**Era pin:** `ANNEX.md:190-206` records the worktree and `fa0e06a`, states that the adapter asserts it on every load, and states that **current teax main's refusal of the `v1.0.0` seal is principled and "is not to be chased upstream"** — asserted by `test_annex.py:72`. `test_era_pin.py` never skips and holds the pin string in agreement across `conftest.py`, `era_adapter.py`, and `ANNEX.md`, so a drifting pin fails on a machine with no worktree at all.

### Brief item 5 — the adapter's self-checks

All three run inside `GlueAwareLoader.load()`, on every load, and every one raises rather than degrades:

- **Accept-set** — `era_adapter.py:198-205`, computed as a set difference against the two documented paths, so an *extra* diagnostic of any kind refuses. Runs before the self-checks.
- **Era pin** — `assert_era_pin` (`:131-144`), called at `:210`. It resolves the worktree from `simkit.__file__` and reads its git HEAD, so it asserts the running dependency rather than an env var; a `returncode != 0` (a directory that is not a git worktree) also refuses. Message names the expected commit, the resolved worktree, and what was found.
- **Dead-filler assertion** — `assert_schema_fillers_are_dead` (`:147-161`), called at `:211`. Deliberately broad (`"MFE_Power_Plant__p_" in text`), with the reason stated: glue feeds those keys from the oracle, so a consumer of *any* kind makes the run undisclosed both-sides circularity.

**None is asserted by a generic tool.** `test_generic.py:21` greps `era_adapter` out of all four modules, and `test_preflight_gates.py:166` additionally greps `oracle_entry`, `simkit`, `StudyRunner`, and `StudyQuery` out of `preflight.py`. The dead-filler check is the one proof-of-life gate that moved *into* the adapter, as review M6 required.

### Brief item 6 — epic Item 4 success criteria

| Criterion | Verdict | Evidence |
|---|---|---|
| Generic tools reproduce the proof-of-life gates with no package-specific code | ✅ | Six gates at `preflight.py:161-306`; four checks at `verify.py:266-340`; grep-clean by `test_generic.py:21-40` |
| Verification stratified, verdicts re-derived, summary at rel < 1e-9 | ✅ | `verify.py:231-247` (stratification a floor, proved by `test_verify.py:132`), `:174-204` (re-derivation from `predicate_ir`), `TOLERANCE = 1e-9` at `:56`; real run worst `4.81e-16` |
| If retained, the adapter route reproduces both committed CSVs byte-for-byte | ✅ | `test_promotion_equivalence.py` — 19-point sweep in the default suite (passed in my run), 948-point grid behind `-m slow` (orchestrator-verified, 130 s) |
| If retained, glue or adapter change → new identity → old store refuses resume | ✅ | `test_lineage_refusal.py:110-148`, four refusals |
| If stock loading works, the adapter is absent rather than dormant | ✅ (N/A branch, discharged) | Probe re-run at Phase 0: `artifacts=139 differing=2` (`plan.md:545`). The adapter branch is live; the criterion is discharged by the stated deletion condition, which forbids a dormant branch |
| Every point through `StudyRunner`; tools do not own execution | ✅ | `promotion_equivalence.py:152,161`; no evaluator construction in either tool |
| **Temporary-route integrity** (`epic:50`) | ✅ | Both halves above; see item 2(a) for the pre-capability-store question |

Nothing in Item 4's scope is unmet.

### Brief item 7 — the manifest edit

`git show 2487b6fd -- exploration/stellarator_e2e/studies/manifest.json`: **4 insertions, 4 deletions, all inside the `oracle` block** — `module`, `callable`, `sys_path`, `note`. `kind` stays `python_callable`. No other manifest key, and no `scripts/study/*` file, in the commit's diff. The commit is its own, as the plan required, so the data change is reviewable in isolation.

### Plan completion

All nine phases are ticked and each carries real Implementation Notes with the evidence behind the tick — including the three places the implementer caught its own bug before commit (`run_clean` hard-coding `outcome: "pass"`; `git status` collapsing an untracked directory, fixed with `--untracked-files=all`; the adapter's `link_root` defaulting inside the repo and dirtying the watched tree, fixed by making it a required positional). No TODO, FIXME, stub, or `NotImplementedError` anywhere in the eight new modules or the seventeen test files. No `except Exception` and no bare `except` in any of them.

### Spec conformance

All ten success criteria in `spec.md:30-39` are met; the mapping is the table in *Brief item 6* plus:

- SC5 (summary carries what `arms[].verification` needs) — `verify.py:447-497`, held by `test_verify.py:96,100`.
- SC7 (four negatives plus the accept-set fifth) — `test_preflight_negatives.py` (five, plus three beyond the plan) and `test_accept_set.py:55`.
- SC8 (annex at Item 2's pinned path, carrying six specified facts) — verified in *Brief item 4*.
- SC10 (no interpretive non-zero; every mechanical failure non-zero) — `preflight.py:515-518`, `verify.py:530-533`; the sibling scan structurally cannot fail (`preflight.py:196-211`).

Non-goals respected: `verify_stellaris.py` and `run_stellaris.py` are untouched, the proof-of-life directory is untouched (`git status` clean over both trees), no second execution facade exists, no Item 2 or Item 3 file was edited beyond the one pre-authorized manifest-values edit, and the `{"kind": "cli"}` amendment was declined and left unused.

### Design conformance

D1–D13 are followed as written. Two are worth naming because they were the review's changed decisions and could have been quietly softened: **D12** is implemented as publication plus fail-closed consumption, never as a name-matching fallback (`verify.py:140-171`); **D13** routes g3 through the shim (`era_adapter.py:290`) with the agreement between the two paths asserted by `test_glue_mapping_agreement.py`, so the injection and the recompute cannot drift.

**One narrow deviation from D9** — see Note 1.

### Code integrity

No god functions, no policy in utilities, no parameter sprawl, no leaky names. `common.py`'s four jobs are each one small function. `preflight.py`'s six checks are six functions with one job each; `_run_check` is the only place a refusal becomes a record. Failure honesty is strong throughout: every failure path raises a typed error with a located message, and I found no silent fallback on an invariant violation.

Two deliberate reaches are commented at the call site rather than hidden: `common.tool_source_digest` calls Item 3's private `manifest._canonical_digest` (`common.py:50-55`), with the reason — one recipe id must mean one algorithm, and two implementations of a digest disagree exactly once, silently. That trade is right.

Four non-blocking notes:

**Note 1 — `preflight.py:380-382`: an unreadable *package* file escapes the always-complete-document rule.** `package_input_keys`, `package_channels`, and `package_parameters` are called outside `_run_check`, so a malformed `inputs/*.json` or `model_contract.json` raises `ToolError` up to `main` (`:504-507`), which prints and returns 1 **without writing a results document**. D9 says the results document is always complete, and the tool's own docstring (`:29-34`) says so too; the code comment at `:505` names the exception as "a failure the checks cannot be run around at all." The narrowing is defensible and documented at the code site, but it is not recorded as a deviation and no test asserts either behavior. *What should change:* either move those three reads inside the `declared_keys`/`sibling_scan` branch so the failure is recorded as `did not run` with its condition, or state the exception in the plan's deviations.

**Note 2 — Invariant 10 has no enforcing test.** `test_generic.py:42-46` asserts the manifest holds no *executable* content, which is a different claim. I verified Invariant 10 by hand this pass: the manifest carries no era pin, no glue rung, no allowed-modified declaration, and no binding data — the oracle `note` describes the companion surface's contract in prose but holds no binding fact, and deleting the adapter requires no manifest edit. *What should change:* a one-line grep test over the manifest for the era pin, `era_adapter`, and `allowed_modified`, so the invariant survives a future manifest edit.

**Note 3 — `verify.py:459,466,481,483,491`: five summary fields are literals in the returned document.** `git_clean: true`, `matches_preflight: true`, `verdicts_rederived: true`, `verdict_mismatches: []`, and `outcome: "pass"` are each *earned* — `assert_tree_clean`, `assert_matches`, and the per-case checks all raise before the return is reached — so there is no current defect. But it is the same shape as the `run_clean` bug the implementer caught in Phase 5, where a hard-coded `outcome: "pass"` would have reported a dirty tree as clean. *What should change:* derive them from the checks that earned them, so a future early-return cannot make the document lie.

**Note 4 — the `p_fus` / `magnet_capital` delta lives only in `plan.md`.** The disposition is right (item 2(b)), but `plan.md:693` is a work-item artifact that gets archived at close. The question it raises is a live Item 3 manifest question. *What should change:* one line in a durable home — `ANNEX.md § Oracle` or an Item 3 backlog note — naming the two channels and the manifest edit that would recover them.

---

## Certification

Verified and marked this pass:

- All nine plan phases complete, with evidence in each phase's Implementation Notes cross-checked against the code.
- All ten `spec.md` success criteria met (already ticked by the implementer; each independently confirmed here against the file:line evidence in the tables above).
- All six epic Item 4 success criteria plus the temporary-route integrity criterion met.
- Ten of eleven design invariants map to a named enforcing test; Invariant 10 is verified by hand this pass and lacks one (Note 2).
- The suite re-run independently: 273 passed, 0 skipped, exit 0. Ruff clean. Working tree clean over `exploration/stellarator_e2e/pkg` and `exploration/stellarator_e2e/study`.
- The manifest edit is exactly the oracle-block values.

Checkboxes in `plan.md` and `spec.md` were already complete and are left as they stand; no deliverable was edited by this audit.

**Not checked:**

- **The 948-point slow test.** Not re-run, per the brief. I rely on the orchestrator's independent run (130 s, byte-equal) and on the 19-point sweep, which passed in my run and exercises the same route end to end.
- **A fresh product-lens pass over the implementation.** This session's standing rule forbids spawning subagents unless the user asks, and the brief did not. I read every block of the existing `product-lens.md` ledger and confirmed no unresolved BLOCK, and I re-derived the point independently above — but the ledger's last entry is against the *design* revision, not the shipped code. A lens run over the implementation is the one certification input this pass substitutes judgment for.
- **The oracle's physics.** `verify_stellaris.py` is treated as the independent reference, as the design intends. I verified that the *mapping* to package channels is right (notably `annual_om`), not that the oracle's own arithmetic is correct.
- **The era teax worktree's contents.** Read as an external pinned dependency; I confirmed the adapter asserts the pin, not that `fa0e06a` is the right commit to pin.
- **Item 2's runbook and Item 3's `manifest.py` / `indicators.py` internals.** In scope only where this item touches them (the six annex links, the oracle block, `_canonical_digest` reuse).
- **Cross-machine behavior.** Every era-dependent test ran with the worktree present. The absent-worktree path (61 loud skips, per `plan.md:700`) was not re-exercised this pass.

---

**Verdict: PASS.** Four non-blocking notes, none of which changes a number, a verdict, or a gate's behavior. Note 4 is the one worth doing before close — it is a handoff, not a fix.
