# Audit: Indicator Tool and Package Manifest (RUN-STUDY Item 3)

**Verdict:** PASS (Certify)
**Audited:** 2026-08-20
**Branch:** `feat/stellarator-mbse-demo`
**Commit:** `14745681` (deliverables last touched at `620c752d`, coordination fixes)
**Auditor scope:** the delivered state including the orchestrator's three Item 4 coordination fixes

---

## The Point

Before any study point runs, the agent needs deterministic, package-derived facts about what in the model can push back on each proposed axis. The proof-of-life availability sweep ran to completion, came out entirely feasible with a monotone cost response, and only afterwards was it clear that no constraint in the model responds to availability at all — a sensitivity analysis published as a design search. The facts were always in the generated package: it records its own dataflow, its constraint operands, and which operands are bound inputs versus computed values. No step asked for it.

This item builds the durable pair that asks: a generic tool (`scripts/study/indicators.py` + `scripts/study/manifest.py`) any teax package can use, and a data-only catalog (`exploration/stellarator_e2e/studies/manifest.json`) of the stable facts the stellarator package supplies to it.

Two owner-grade constraints govern it. Interpretive facts never gate a study; mechanical failures fail closed — a broken analysis and an empty one must never share an exit code. And generic and package-specific never share a file: the tool names no package, the manifest holds no logic.

## Summary

The implementation delivers what the spec and design asked for. The suite is green (134 passed, ~12s), ruff is clean, all twelve design invariants have tests that assert what they claim, the six known-answer expectations reproduce the Item 1 spike's output field-for-field and were never patched after they were written, the manifest is data-only with a pin that matches the live package, and the three mechanical failure paths I ran by hand each exit non-zero with a message that locates the fault and write zero bytes.

Nothing rose to a should-fix. Three recorded deviations from the design (package-relative pin paths, the oracle's `sys_path` field, the nine-key baseline point) are each sound and each written down in `plan.md`. Two small observations are listed under Code integrity as notes, not defects.

## Product Judgment

**Is this the right piece of work? Yes.**

The product-lens ledger at `.project/active/run-study-indicators/product-lens.md` records two runs. The first raised `F1` (per-key `fan_out | tie` provenance dropped) and `F2` (a computed-quantity key reported as an absent key) and gated BLOCKED. The second resolves both by citation against the spec text, and the gate is CLEAR. I scanned every block, not just the latest: no earlier block is left unresolved. The epic's live Product-Lens gate (`.project/backlog/epic_run_study_capability.md`, Product-Lens section) is CLEAR — `epic-F1` and `epic-F2` are FIXED on owner authority.

Both lens findings are not merely marked fixed but visibly delivered in code and asserted by tests:
- `F1` — provenance survives declaration → output per key (`scripts/study/indicators.py:585`), asserted by `tests/study/test_provenance.py:23`.
- `F2` — a declared key naming a produced channel is its own mechanical outcome with its own wording (`scripts/study/indicators.py:586-591`), asserted distinct from the absent-key message by `tests/study/test_mechanical_failures.py:111`.

No product-drift smell fired. Specifically, the acceptance-test signature this repo has been bitten by — a suite green because each assertion selects a different route while two outputs exist for one source — does not apply: `bounds` is the single authoritative list and both partitions are asserted to be exactly `bounds` filtered on "any operand reached" (`tests/study/test_output_contract.py:256`), so there is one representation, not two kept in sync.

## Findings

### Plan completion

All seven phases are committed and their checkboxes are genuine. Commit trail, oldest first: `6e7f164f` (Phases 1–3 substance and known answers), `dc285ab5` (Phase 4 synthetic package + `package_copy`), `ccc913f0` (Phase 5), `b927dca2` (Phase 6), `e4cf9cd1` (Phase 7), `e805142b` (spec criteria ticked), `620c752d` (orchestrator coordination fixes).

**On the timeout.** The brief warned the final phase's notes might be thin because the implement session's wall clock expired after its last commit. They are not. `plan.md` Phase 7 Completion carries actual changes, issues, deviations, the twelve-invariant sweep table naming the asserting test for each, manual verification, and a final state line. I did not need to reconstruct anything from commits; the only thing the timeout cost was the wrap-up message, and `620c752d`'s commit body says so.

Every phase's deviations are recorded, none silent. The four recorded deviations across all phases:
- Phase 1: pinned fingerprint paths are package-relative, not repo-relative, resolved in favour of the design's own schema example over its recipe prose.
- Phase 1: the `tool-source-digest/v1` recomputation test moved to Phase 2, because the recipe's file list includes schema files Phase 2 authors.
- Phase 2: the oracle object carries a required `sys_path` field beyond the design's rendered shape.
- Phase 2: `baseline.point` records nine qualified keys rather than three axis names.
- Phase 3: the `axis_declaration` block and both advisory scans shipped early (the report cannot validate against its own schema without them); their tests still landed in Phase 6 as planned.
- Phase 4: the synthetic package root sits at `data/synthetic_pkg/pkg/` with its manifest and axes as siblings.
- Phase 7: `.project/CURRENT_WORK.md` deliberately untouched — it carried an uncommitted modification from Item 2's parallel work.

Each is sound and each is stated with its reason. I checked the two that could change downstream behavior. The package-relative pin is what Invariant 10 compares resolved reads against (`scripts/study/manifest.py:493`), so it is the internally consistent choice; but see the note in Code integrity. The `sys_path` field is additive within D6's typed object and is validated as required (`scripts/study/manifest.py:359`), so Item 4's `verify.py` cannot silently skip it.

No TODO, FIXME, stub, or placeholder code exists in `scripts/study/` or `tests/study/`. The one grep hit is the word "placeholder" in a docstring describing the minimal-manifest fixture.

### Spec conformance

Eleven success criteria; all eleven verified. They were already ticked at `e805142b`; I re-verified each rather than trusting the tick.

1. **Known-answer tests for six cases matching the Item 1 fixture contract field for field** — verified independently, see *Known answers* below. `tests/study/test_known_answers.py`.
2. **Valid empty exits 0; five named mechanical failures exit non-zero with no partial output** — `tests/study/test_valid_empty.py:18`, `tests/study/test_mechanical_failures.py:98` (nine parameterized cases, each asserting non-zero exit *and* empty stdout *and* no output file).
3. **A declared key naming a produced channel exits non-zero with a distinct message** — `scripts/study/indicators.py:586`; asserted distinct at `tests/study/test_mechanical_failures.py:111` and confirmed by hand (below).
4. **Per-key `fan_out | tie` provenance survives input to output** — `tests/study/test_provenance.py:23`.
5. **Every mechanical failure message locates the fault** — spot-checked by running three paths; see *Error messages* below.
6. **Suffix siblings and tie candidates appear in the output and never change what is traced** — `sibling_candidates` is its own named field (`scripts/study/indicators.py:732`), tie candidates go to group `warnings` (`:734`); `tests/study/test_warnings.py:39` asserts nine trace fields are identical with and without the manifest tie. The spec's parenthetical records that this landed per M2 rather than the spec's original wording; the delivered split matches the accepted design.
7. **`indicators.py` names no package, key prefix, or adapter** — `tests/study/test_generic.py:14` plus three stronger greps (`:21`, `:29`) that also refuse `mfe_stellarator`, `lcoe_calc`, `verify_stellaris`, `stellaris`, `exploration`, `stellarator`.
8. **The manifest parses as data, holds no executable content, and carries no per-study choices** — verified directly, see *The manifest* below.
9. **Every report states the three not-derivable facts and the positive reading, in its own output** — `scripts/study/indicators.py:53-63`, emitted at document and group level, byte-equal (`tests/study/test_output_contract.py:231`). I read the block: three statements plus `positive_reading` ("a possible path exists in the module graph. It never means the axis responds").
10. **The output schema is documented and versioned** — `scripts/study/schemas/indicators.v1.schema.json`, `schema_version: "study-indicators/v1"` carried inside the output; real output validated against it at `tests/study/test_output_contract.py:222`.
11. **Tests run under `uv run python -m pytest`** — `uv run python -m pytest tests/study -q` → **134 passed in 11.78s**, run by me.

**Known requirements.** The `[HARD]` indicator-input fingerprint is implemented over exactly the three legs the trace reads (`scripts/study/manifest.py:97`); the `[HARD]` data-only manifest holds and the `[HARD]` assert-before-mutating rule is carried by the `package_copy` factory (`tests/study/conftest.py:151`, raising if the target substring is absent). The `[NEED][OWNER]` mechanical/interpretive exit-code split holds end to end. The `[NEED][OWNER]` manifest content boundary is asserted mechanically (`tests/study/test_output_contract.py:131` pins the top-level key set). R1–R12 are implemented and, for R3 in particular, the Phase 5 defect fix (strip `.root`, then still apply the R4 dotted-ref check) is real in the code at `scripts/study/indicators.py:251-255`.

**Non-goals respected.** Nothing infers membership from suffixes; the tool emits no "responds" or "unresisted" string; no preflight, oracle, or execution code was built; no second package manifest exists; `indicators.py` never reads the baseline or the oracle (confirmed by grep — neither `baseline` nor `oracle` appears in it).

**Known answers — checked independently, not patched.** I wrote my own comparator (`.orchestrate-logs/audit_diff.py`) against `.project/active/run-study-reachability-spike/indicators.json` rather than trusting the suite. For all six cases — `availability`, `interest_rate`, `R`, `R+tie`, `a`, `beta` — every field both artifacts carry matches: declared key set, `entry_type` per key, `group_valid`, `no_constraint_response`, `sibling_candidates`, both objective lists, `modules_fired`/`channels_tainted`, the reachable-constraint set by `source_local_identity`, and per constraint the operator, `bound_vs_bound`, `operand_classes`, `constraint_id`, and each operand's name, class, ref, reached flag, entry type, and literal value. **Zero mismatches.** I also cross-read the fixture contract in `findings.md` (§Fixture contract for Item 3, cases 1–5 plus 3b and the mechanical-outcome table) — the counts (6/8, 8/11, 54/67, 2/2), the objective splits, and the valid-empty expectation (`land_cost` → `lcoe`, `lcoe_1cfe`, `total_capital`, asserted verbatim at `tests/study/test_valid_empty.py:29`) all agree.

**Not patched, on the record.** `git log -- tests/study/data/` shows three commits. The six `*.expected.json` files were created in `6e7f164f` and never touched again; `dc285ab5` added only the synthetic package, `b927dca2` added only `axes.extras.json`. The fixture-binding assert (`tests/study/test_known_answers.py`) plus the `derived_against_semantic_fingerprint` field in each expectation file are the forward guard.

**The manifest.** `exploration/stellarator_e2e/studies/manifest.json` is a JSON object with exactly the seven schema blocks and no others. No axes, no windows, no selected objectives. `tests/study/test_generic.py:35` greps it for `import `, `lambda`, `eval(`, `exec(`, `$ref`, `!!` — none present, which I confirmed by reading the file. Its pinned digest `612edfc9…bbb9` equals the live `--print-fingerprint` output over the five artifacts (I ran the tool; digest and all five per-file sha256s match the pinned list). `package.name` `stellarator_tea` matches the live package contract. Recorded provenance carries the sealed `executable_fingerprint` `ad912041…fa2d` and the contract `semantic_fingerprint` `c9bc1640…c261`, the fingerprint Item 1's evidence is bound to.

**Error messages — three failure paths run by hand** (`.orchestrate-logs/audit_failpaths.py`). Each exited 1, wrote 0 bytes to stdout, and created no output file:
- Absent key → `axis 'probe': declared key 'stellarator_09__stellaris__geom__NOPE' is absent from the package inputs` — names the key.
- Computed quantity → `… names a computed quantity — it is a channel produced by module 'stellarator_09__stellaris__pb', not a bound input. A computed quantity is a model output, not an axis.` — names the key, says what it is, names the producing module, and is visibly not the absent-key wording.
- Corrupt pipeline line (on a re-pinned copy) → `…/mfe_stellarator.yaml:24 (key path modules.stellarator_09__stellaris__geom.inputs.R): cannot split type/ref in 'floatonly_one_token'` — file, line, and key path, which is stronger than the spec's accepted fallback.

One aside worth recording, because it is the exact hazard Item 1's log entry 7 named: my first attempt at the corrupt-line probe used a wrong target substring and would have "passed" against an uncorrupted file. My script asserted the target first and refused. The repo's own `package_copy.edit` carries the same guard (`tests/study/conftest.py:155`), so the suite cannot make that mistake either.

### Design conformance

**All twelve invariants have an enforcing test, and each test asserts what the invariant says.** I resolved every test named in `plan.md`'s sweep table against the collected suite — all fifteen names exist — and read the bodies rather than trusting the names.

| # | Invariant | Enforcing test | Verified |
|---|---|---|---|
| 1 | No partial output | `test_mechanical_failures.py::test_fails_closed` (9 cases), `test_multipipeline.py::test_mechanical_failure`, `test_read_set_coverage.py` (2 failure cases) | Yes — each asserts rc≠0 **and** `out == ""` **and** the out-path does not exist; runs are subprocesses, so a partial write would show |
| 2 | Determinism incl. across working directories | `test_output_contract.py::test_byte_determinism_across_working_directories`, `::test_two_runs_from_the_same_directory_are_byte_identical` | Yes — also asserts no absolute path anywhere in the document |
| 3 | Declared-only membership | `test_warnings.py::test_advisory_never_changes_the_trace`, `::test_suffix_siblings_never_join_the_traced_set` | Yes — nine trace fields compared with and without the manifest tie |
| 4 | `no_constraint_response == (constraints_reachable == [])`, always emitted | `test_valid_empty.py::test_no_constraint_response_is_emitted_even_when_false` | Yes — asserts the equality for every group, plus a `False` case |
| 5 | Constraint completeness, both halves | `test_output_contract.py::test_constraint_completeness` | Yes — catalog ids read live from the contract, compared to `bounds` and to the partition |
| 6 | Grep-clean | `test_generic.py::test_tool_modules_are_generic` (6 cases) | Yes, plus three stricter greps |
| 7 | Disclosure parity | `test_output_contract.py::test_not_derivable_is_byte_equal` | Yes — `json.dumps(sort_keys=True)` compared document vs every group |
| 8 | Provenance round-trip | `test_provenance.py::test_provenance_round_trips_from_the_declaration` | Yes — declaration file re-read and compared per key |
| 9 | Interpretive facts never gate | `test_valid_empty.py::test_a_group_with_no_constraint_reach_exits_zero`, `test_warnings.py::test_provenance_drift_warns_on_both_recorded_fingerprints` | Yes — drift on both recorded fingerprints exits 0 |
| 10 | Read-set coverage | `test_read_set_coverage.py` (all six) | Yes — outside-the-pin, outside-the-root, refused-by-path-before-open, the positive statement, M1, and a followed rename |
| 11 | Record-feeding run is a full-document run | `test_subset_flag.py::test_a_full_run_covers_the_whole_declaration`, `::test_a_group_run_is_visibly_narrower` | Yes — `groups_declared` stays whole under `--group` |
| 12 | `sibling_candidates` is a named group field | `test_warnings.py::test_suffix_siblings_land_in_their_own_named_field` | Yes — 17 candidates against 1 declared key, and `"sibling"` absent from `warnings` |

**None unenforced.**

The architecture matches the design: the two-module split (D3), the gate order (D8, `scripts/study/indicators.py:802-812`, with the M3 coverage check placed between `read_pipelines` and `build_graph` so inputs files are checked by path before any is opened), `yaml.compose` with the accept-set scoped to the `modules` subtree and null-tagged empty sections tolerated (D2/S6, `:116` and `:180`), assemble-then-write with atomic `--out` (`:888`), the three constraint identities (D10, `:644-652`), the not-derivable constant emitted at both levels (D5), and `--group` forcing `subset: true` (D11, `:863`).

**Coordination fixes (`620c752d`) checked as delivered state.** `tool_source_digest()` now returns `{recipe, digest, files}` with per-file digests (`scripts/study/manifest.py:157`); the schema's digest definition gained `files` as an optional additive property; `test_generic.py` changed its directory listings from exact-match to subset assertions (`:48`, `:56`) with a docstring naming why — Item 4's `preflight.py`/`verify.py`/`identity.py`/`common.py` and its schema files share the directory. The subset change is the right call: pinning a shared directory's exact contents is a test asserting something the item does not own. `test_output_contract.py:288` was updated in the same commit and still asserts recipe id, recomputation, and now the shape of the `files` entries.

### Code integrity

No god functions, no policy in utilities, no silent fallbacks, no broad `except Exception`, no back-compat shims, no optional parameters papering over missing data. Every `except` clause names its exception type and re-raises as a located `IndicatorError`/`ManifestError`. Failure honesty is the whole design of the module and it holds in the code.

Two notes, neither a defect and neither blocking:

- **`scripts/study/manifest.py:162` prose vs. behavior on pin path scope.** The recipe uses package-relative paths; `design.md:162` still says "sorted by repo-relative POSIX path". `plan.md` Phase 1 records the deviation and the reason, and the code is internally consistent (Invariant 10 compares against the same package-relative form). But Item 4 reads `manifest.py` for the same recipe and may read the design prose alongside it. If the design gets another revision, that one clause should be corrected to match; nothing in this item needs to change.
- **`tests/study/test_output_contract.py:176` (`test_schemas_are_closed`) is weaker than it reads.** The walk only inspects nodes carrying `"type": "object"`, so a property-bearing subschema that omits `type` would pass unexamined. I ran an independent check across all three schema files for any node with `properties` and no `additionalProperties`: **none**. So the claim is currently true; the test just does not fully guarantee it stays true.

For completeness on failure honesty: an unexpected shape in `contracts/model_contract.json` — for instance `parameters` arriving as a mapping rather than a list (`scripts/study/indicators.py:422`) — would surface as a traceback rather than a located message. It still exits non-zero and still writes nothing, so no invariant breaks and the owner's rule holds; the cost is only message quality on a path the strict reader was not asked to cover.

---

## Certification

**Certify.** The product-lens ledger gate is CLEAR with no unresolved block in any run, and the epic's gate is CLEAR. All eleven spec success criteria are verified and stay ticked. All seven plan phases are verified complete and stay ticked. All five of the epic's Item 3 success criteria are met, and I have marked them and appended ✅ to the item heading. `CURRENT_WORK.md` is updated to certified.

What I checked, concretely: ran the suite myself (134 passed); ran ruff (clean); ran the tool end-to-end on the real package; ran three mechanical failure paths by hand and read their messages; recomputed the live fingerprint and compared it to the manifest pin file-for-file; wrote an independent comparator diffing all six known-answer expectations against the Item 1 spike output; checked `git log` on the expectation files for post-hoc patching; read both tool modules in full; read all ten test files; independently verified the schema-closure claim; read every product-lens block.

**Not checked:**
- The synthetic two-pipeline fixture's own correctness. I read `test_multipipeline.py`'s assertions and the plan's manual-verification note, but I did not independently re-derive that the fixture's cross-file channel edge is real rather than an artifact of how it was authored. The design named this the one behavior with no real package data behind it; the implement session's manual read-through is the only evidence, and I am relying on it.
- The three JSON Schema files line by line. I verified closure mechanically, verified both load-bearing `description` lines are present, and verified real output and the real manifest validate — but I did not audit every field definition against the design's rendered shapes.
- The `study_package_manifest.v1` and `axis_declaration.v1` schemas against Items 2 and 4's actual consumption. Whether the seam is *sufficient* for them is their audits' question, not this one's.
- Performance, and behavior on any package other than the stellarator and the synthetic fixture.
- Whether the manifest's recorded baseline point and headline LCOE are numerically correct against the model. I verified the manifest holds them as data and that `indicators.py` never reads them; validating the values is Item 4's baseline gate.
- The `.orchestrate-logs/` scratch scripts I wrote for this audit are working artifacts, not deliverables, and are not part of the certified state.
