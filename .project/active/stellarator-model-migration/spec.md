# Spec: Stellarator Model Migration

**Status:** Implementation Complete 2026-08-21 (audit pending)
**Owner:** Reid W
**Created:** 2026-08-21 08:23
**Complexity:** HIGH
**Branch:** `feat/stellarator-model-migration` (off `main` `7ee0c22a`); spec, design, plan, and implementation for this item all live here, one PR at the end

---

## Problem

The stellarator package (`exploration/stellarator_e2e/generated/`) was generated on 2026-07-25 with an older sysml-codegen and sealed at runtime contract 1.0.0. Today it runs only on a frozen teax worktree (`/home/reid/1cfe/teax-v1-era` @ `fa0e06a`) through `studies/era_adapter.py`, which supplies five things that codegen could not at the time: a hand-edit to two sealed files, a CAS28 constant, an `n_mod` default, three dead schema fillers, and a per-point CAS27 value the package could not compute across parts. That last one is fed identically to the package and to the oracle, so the proof-of-life's verification has one disclosed hole.

The pinned toolchain (`sysml-codegen` `8a758e92` via fusion-tea's pins; teax main `744745f`) no longer needs any of the five — a live probe generated, sealed, loaded, and executed all five shapes (`.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` § 3–4). But it refuses the **model**: 94 self-named `in x = x` bindings (`SI_SELF_BINDING`), six scalar function calls (`sqrt`/`max`/`min`/`floor`), unit text scraped from trailing `//` comments that collides across consumers, and four calc usages whose positional parameter redefinition skips a leading defaulted formal. Past those four classes, unknown.

Until the model generates clean at 2.0.0:
- the adapter and its glue cannot be deleted, so every study runs on a route we intend to remove;
- RUN-STUDY Item 6 (the first A/B consumer) would write its record under an identity that retires on migration — `[OWNER 2026-08-21]` ruled Item 6 waits for this;
- the MFE models cannot live in `models/` (`[OWNER 2026-08-21]` Q1 → A: staged-twin only until they generate), which bends MR-3 and keeps `tests/models/test_power_balance.py` pointed at the twin;
- the CAS27 verification hole stays open.

The owner hold on editing the stellarator model (sysml-codegen `BACKLOG.md:403-412`) is released by the Q3 decision (`[OWNER 2026-08-21]`).

## Success Criteria

- [ ] **SC1 — Generates clean on the pinned toolchain.** `sysml-codegen generate` over the MFE model tree completes with zero readiness diagnostics and seals at `runtime_contract_version 2.0.0`; stock `ProvisionalPackageLoader(..., strict=True)` on teax main accepts it; zero sealed artifacts differ from their hashes. (Today: 1.0.0, refused, 2 of 139 differ.)
- [ ] **SC2 — Same numbers.** On the regenerated package, the baseline point (`R = 12.7`, `a = 1.3`, `availability = 0.85`) gives LCOE within rel 1e-9 of `275.2642200420774` and the same five verdicts `satisfied`, matched by `source_local_identity`; the 948-point grid and 19-point sweep match `exploration/stellarator_e2e/studies/BEFORE_MIGRATION_RECORD.md` § 2's CSVs **by value** (rel < 1e-9 on LCOE and identical verdicts per point, keyed by (R, a) / availability — not by column name or bytes, since entry keys move with the rename). Any drift is a finding to explain, not a tolerance to widen.
- [ ] **SC3 — Adapter gone, not dormant.** `studies/era_adapter.py` and `studies/promotion_equivalence.py` deleted; the glue loader and constants in `study/run_design_search.py` and `run_stellaris.py` deleted; the era fixtures in `tests/study/conftest.py` and the seven era-bound test files deleted or rewritten against the stock route; `ANNEX.md` § Loader exception and glue and § Era pin removed; no reference to `fa0e06a` or `teax-v1-era` remains outside `BEFORE_MIGRATION_RECORD.md` and historical records. `oracle_entry.py` and `verify_stellaris.py` stay.
- [ ] **SC4 — Verification closes the hole.** `scripts/study/verify.py` stratified oracle parity at rel < 1e-9 on the regenerated package with an **empty** `not_independently_verified` list — CAS27 is now computed in-package and checked against the oracle for the first time.
- [ ] **SC5 — Manifest re-pinned, tools unchanged.** `studies/manifest.json` fingerprints, baseline, ties, and objective catalog re-declared against the new package; `preflight.py`'s `manifest_currency`, `identity`, `baseline_headline`, and `package_clean` gates pass on the stock route; no package-specific code enters `scripts/study/`.
- [ ] **SC6 — MFE models promoted.** The MFE/stellarator model files live in `models/library/` and `models/designs/` again, with `exploration/stellarator_e2e/models/` as a byte-identical twin (the IFE precedent), and `tests/models/test_power_balance.py` reads `models/library/` again with its TEMPORARY note removed. `exploration/stellarator_e2e/STAGED_MODELS.md` is deleted or rewritten as the twin's note.
- [ ] **SC7 — Spine test reshaped, not weakened.** `tests/models/test_self_binding_replacement.py` (or its successor) generates each design family from its own tree and asserts that family's census; the IFE assertions (23 entry points / 18 design attributes, live == snapshot, both mutation proofs) still pass unchanged; an MFE census of the same kind is added; the one-time D-5 rename asserts are either kept under the IFE entry or dropped, by a recorded choice. This discharges the "Test cleanup" row at the top of `BACKLOG.md`.
- [ ] **SC8 — Every model edit is ledgered.** One table, committed beside the models, with a row per change: file:line, the refusal or rule it answers, its class (see R5), what it replaced, the rationale, and — for any value a change introduces or relocates — its `Source`/`Ref`/`Basis` citation per MR-4 (`modeling_project/REQUIREMENTS.md`). Rewrites that exist only because the toolchain lacks a feature are marked for revert and the `BACKLOG.md` revert row updated to point at the ledger.
- [ ] **SC9 — Upstream filings made.** The positional-redefinition finding is filed in sysml-codegen's backlog with the four sites; the six scalar-function sites are attached to `[SCALAR-FUNCTION-VOCABULARY]` as the motivating case; any further toolchain-limitation class found during the work is filed the same way.
- [ ] **SC10 — Mutation proof on the new package.** Move one input (e.g. `cas28_capital`) and exactly the expected consuming modules react; move a second, nested one (e.g. a radial-build thickness) and only its consumers react — the spine-test pattern, on the stellarator.
- [ ] **SC11 — Suites and model validation green.** Licensed `tests/models` (incl. the reshaped spine test) and `tests/study` pass on the stock route with no era dependency; `tests/test_dependency_provenance.py` pin tests pass; `uv lock --check` passes; `uv run agentic-mbse validate models/` passes at the level the project runs today (record the level), and every new or moved quantitative value carries an MR-4 citation (checked by review — no audit script exists yet; `traceability-system` is paused).

## Known Requirements

- **[HARD]** sysml-codegen is fixed at fusion-tea's pinned SHA `8a758e92` (`pyproject.toml`, enforced by `tests/test_dependency_provenance.py`). No upstream change is a dependency of this item (a re-pin is a shipment-sized event; see the `uv.lock` P1 row). Upstream fixes are *filed*, not waited for.
- **[INFERRED]** teax main `744745f` is the "after" runtime: fusion-tea pins no teax commit, and `744745f` is the only teax that accepts `runtime_contract_version 2.0.0` (research Decisions Q5, an agent lookup). Design records which teax the after-route tests load and how (see Open Questions); if a teax pin is wanted, that is an owner decision.
- **[HARD]** The seal is final after generation: post-seal edits under `pipelines/**` or `inputs/**` are refused by codegen's manifest and hash-verified by teax before import. No hand-edits to generated artifacts, ever.
- **[HARD]** Only `handwritten/**` may carry human code in the package. The two existing handwritten impls (`dt_fusion_power_impl.py`, `levelized_replacement_cost_impl.py`) re-attach by signature match on regeneration; if a signature moves, the impl is updated in `handwritten/`, not patched elsewhere.
- **[HARD]** `SI_SELF_BINDING` is refused by the exact route; the ratified migration is the D-5 rename (`in x_in = x`), applied with sysml-codegen's `scripts/make_d5_variant.py --root`, whose four preconditions pass on this tree (probe, 2026-08-20).
- **[NEED]** `[OWNER-VERBATIM 2026-08-21]` "Yeah I like threshold. we already know some: BAD patterns that should be fixed as per new rules (like self-assignment); KNOWN and similar patterns for expressions unsupported → calc defs. The spec should just require tracking them, classifying the change, and providing rationale of the decision. but I don't want to let this slow us down." → R5 below.
- **[NEED]** `[OWNER 2026-08-21]` (Q3) The six scalar-function sites are rewritten now, filed upstream as the motivating case, and reverted when the pin catches up; the revert is a `BACKLOG.md` row, not a memory.
- **[NEED]** `[OWNER 2026-08-21]` (Q1 → A) The MFE models return to `models/` in this item, with the spine test reshaped here, not before.
- **[NEED]** `[OWNER 2026-08-21]` (Q2) RUN-STUDY Item 6 runs after this item, on the stock route; this item does not run studies beyond what SC2/SC4/SC10 need.
- **R5 — the change policy [NEED, from the verbatim above]:**
  - **Class A — bad pattern, fixed as a rule.** The model was wrong or inert by current modeling rules (self-named bindings; positional usages that skip a leading defaulted formal; metadata that collides). Fix in place; ledger it; no revert, no owner stop.
  - **Class B — known unsupported expression shape → calc def.** A construct the exact route does not admit (scalar function calls, and shapes of the same kind found later). Rewrite to the documented form (codegen `docs/architecture/modeling-assumptions.md:241-243`: functions live in a calc def, or a numerically identical expression); ledger it; mark for revert; file upstream. No owner stop.
  - **Class C — no equivalent form exists.** Stop, surface, park the dependent work. This is the only stop condition.
  - **Glue absorption is not a model edit.** The five values the adapter supplies are already in the model — `:>> cas28_capital = 5000000.0` (`stellarator_plant.sysml:727`), `attribute n_mod : Real default 1.0` (`mfe_plant.sysml:328`), `:>> special_materials_capital = rb.blanket_vol * …` (`:658`), the `p_*` aliases (`mfe_plant.sysml:244-246`) — and the pinned codegen resolves each of them (research § 4, probe 4). Regeneration picks them up; the glue simply has nothing left to supply. If a regenerated package lacks any of them, that is a toolchain finding to surface (Class C), never a reason to re-add glue or to re-enter a constant by hand. The cost-constant Non-Goal is about changing values, not about the model carrying the ones it already has.
  - Every change, whatever its class, gets a ledger row (SC8). The ledger is the audit surface; nothing is rewritten silently.
- **[INFERRED]** Numerical identity to the old package is the bar (SC2) because every known fix is meaning-preserving: the rename is inert, the old route matched positional bindings by name so the old numbers were already right, comment edits move no number, and `sqrt`/`max`/`min`/`floor` have exact expression or calc-def forms. A change that cannot preserve the number is Class C until the owner says otherwise.
- **[INFERRED]** The MFE twin keeps the IFE precedent: canonical `models/` plus a byte-identical `exploration/stellarator_e2e/models/` twin enforced by test, rather than deleting the twin.
- **[INFERRED]** Unit metadata on formals is harmonized or removed so one entry point projects one unit; a typed-units form is a design choice, not required here.
- **[INHERITED]** The before-record's seven "after" bars (`BEFORE_MIGRATION_RECORD.md` § 7) are the acceptance oracle for SC1–SC4 and SC10. Source: that file, captured 2026-08-21 from the era route.
- **[INHERITED]** The adapter's own deletion condition — "stock loader accepts with `strict=True` → delete whole, no partial retirement, no dormant branch" (`studies/era_adapter.py:3-9`, `ANNEX.md` § Deletion condition) — is SC3's definition of done. Source: RUN-STUDY Item 4 design, ratified by owner 2026-08-19.
- **[INHERITED]** Generic study tools stay package-agnostic (no stellarator names, no adapter import). Source: RUN-STUDY Items 3–4 success criteria.

## Non-Goals

- Running RUN-STUDY Item 6 or any new design study (beyond SC2's reproduction runs and SC10's mutation probes).
- Changing sysml-codegen, teax, or agentic-mbse, or moving fusion-tea's pins. Findings are filed upstream; nothing waits on them.
- Fixing the `uv.lock` regenerability defect (its own P1 row). If this item needs a new dependency, the hand-add-then-`uv lock --check` route from the landing plan applies and is recorded.
- Deciding what generated artifacts belong in git (its own P1 row). This item regenerates the package in place; the tracked/ignored policy is applied afterwards. Coordinate so the two don't fight over the same files.
- Changing model physics, cost constants, or the ARIES-CS hold-out (`knowledge/holdout/` stays quarantined).
- Visualization, the Stellarator Demo epic's on-hold items, or deleting the era teax worktree (tidy pass).

## Open Questions / Deferred to design

- How each Class B site is rewritten: `sqrt(x)` as `x ** 0.5` if the power operator is admitted (a `/_my_spike` answers this in minutes) or as a calc def; `max`/`min`/`floor` as calc defs or bounded-by-construction expressions.
- Positional-binding fix form: reorder defaulted formals last in the library defs (touches every usage of those defs) vs bind every formal at the four usages. Either is Class A.
- Unit-comment fix form: strip trailing `//` unit comments on formals, harmonize the text, or move to a typed form. The research probe cleared the class by stripping; design picks.
- Spine-test shape: one parametrized test over `{IFE, MFE}` with per-family expected censuses, or two test modules; where the one-time D-5 rename asserts go.
- Ledger home and format (a markdown table beside `models/`, or a section in `STAGED_MODELS.md`'s successor).
- Order of work: land the model fixes + regeneration as one PR and the adapter retirement + promotion as a second (the research's PR 2 / PR 3), or one PR. Plan decides by risk; the spec requires both halves.
- Which teax the "after" route uses in tests on `main`: the stock route via `STOP_PARSER_TEAX_ROOT` (the sealed-runner contract) or a plain `sys.path` to teax main. Design, with the `tests/study` conftest as the integration point.
- Whether the 948-grid re-run is a kept test (`-m slow`, like today's promotion equivalence) or a one-time acceptance run recorded in the ledger.

---

## Related Artifacts

- **Epic:** none — this item is the bridge between RUN-STUDY (`.project/backlog/epic_run_study_capability.md`, Item 6 depends on it) and the on-hold Stellarator MBSE Demo epic (`epic_stellarator_mbse_demo.md`).
- **Research:** `.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` (§ 3 model blockers, § 4 glue retirement, § 5 before/after bars, Decisions Q1–Q3)
- **Before-record (acceptance oracle):** `exploration/stellarator_e2e/studies/BEFORE_MIGRATION_RECORD.md`
- **Adapter contract:** `exploration/stellarator_e2e/studies/era_adapter.py:1-40`, `exploration/stellarator_e2e/studies/ANNEX.md`
- **Predecessor:** `.project/active/stellarator-demo-landing/plan.md` (PR #104; Option A; the retargeted `test_power_balance.py`)
- **Backlog rows discharged or touched:** "Test cleanup" (P1), "Revert the six scalar-function rewrites" (P2, updated to point at the ledger); coordinated with "Review codegen-generated artifacts" (P1).
- **Upstream references:** sysml-codegen `BACKLOG.md:36-41` (`[SCALAR-FUNCTION-VOCABULARY]`), `:403-412` (`[STELLARATOR-D5-MIGRATION]` hold, released), `scripts/make_d5_variant.py`, `.project/completed/20260814_cutover-recovery/plan.md` "Slice 3D" (the IFE route to mirror)
- **Product-lens:** `.project/active/stellarator-model-migration/product-lens.md`
- **Design:** `.project/active/stellarator-model-migration/design.md` (to be created)

---

**Next Steps:** After approval, `/_my_spec_review` in a fresh session (HIGH complexity), then `/_my_design`.
