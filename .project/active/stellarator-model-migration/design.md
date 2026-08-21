# Design: Stellarator Model Migration

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-21 08:37 PDT
**Updated:** 2026-08-21 09:01 PDT
**Branch:** `feat/stellarator-model-migration`
**Base:** `main` at `7ee0c22a`
**Design revision:** `d04ed5bb`

## Overview

Regenerate the stellarator package on the pinned codegen and stock teax route, record one-time numerical equivalence for the migration, then retire the era adapter whole and return the MFE models to the canonical model tree.

## Related Artifacts

- [Spec](spec.md)
- [Product-lens ledger](product-lens.md)
- [Reconciliation research](../../research/20260820-221835_stellarator-demo-reconciliation-plan.md)
- [Before-migration acceptance record](../../../exploration/stellarator_e2e/studies/BEFORE_MIGRATION_RECORD.md)
- [Run-Study capability epic](../../backlog/epic_run_study_capability.md)
- [Stellarator MBSE Demo epic](../../backlog/epic_stellarator_mbse_demo.md)
- [Predecessor landing plan](../stellarator-demo-landing/plan.md)

## The Point

**[OWNER 2026-08-21]** The first A/B consumer must run on the stock teax route, not under an identity that this migration retires. This item therefore has to regenerate and seal the stellarator package on the pinned codegen, delete the era adapter whole, close the CAS27 verification hole, and return the MFE models to the canonical `models/` tree without weakening the IFE regression proof.

**[OWNER-VERBATIM 2026-08-21]** “The spec should just require tracking them, classifying the change, and providing rationale of the decision. but I don't want to let this slow us down.” The migration ledger is therefore the audit surface for model edits, not a review gate in front of already-classified Class A and Class B repairs. Only a Class C finding stops the cutover.

## Research Findings

- The migration branch deliberately contains the MFE source only in the staged tree. The canonical tree still contains the IFE family, and the existing spine test treats all of `models/` as one generated plant (`tests/models/test_self_binding_replacement.py:27-30,101-115`). Promotion changes that assumption; it cannot merely add files.
- The D-5 utility is a guarded source transformer, not a generator. Its four text-level preconditions refuse before writing (`/home/reid/1cfe/sysml-codegen/scripts/make_d5_variant.py:437-509`). Those preconditions pass on the self-contained MFE tree. They do not describe the mixed canonical tree after IFE has already migrated, so the staged tree is the only sound D-5 input.
- The spec's 94-site MFE count is stale. The staged tree contains 99 stellarator-owned self-bindings: 94 in `mfe_plant.sysml` and five in `stellarator_plant.sysml` (`exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml:870-879`); the upstream migration record independently gives the same split (`/home/reid/1cfe/sysml-codegen/.project/backlog/BACKLOG.md:488-497`). The transformer census, ledger, and MFE spine must use 99.
- Exact-route expression evidence visits every expression-bearing feature before graph construction (`/home/reid/1cfe/sysml-codegen/src/sysml_codegen/elaboration/expression_evidence.py:280-307`). The pinned semantic extractor admits ordinary arithmetic and exact `NumericalFunctions::sum`, but refuses the six `sqrt`/`max`/`min`/`floor` invocations before the handwritten compiler rung can absorb them (`/home/reid/1cfe/agentic-mbse/src/agentic_mbse/sysml/reference_use.py:395-428`). Adding helper calc definitions would not change that.
- The existing handwritten rung already carries the correct executable semantics. `DT Fusion Power` computes the full profile integral (`exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py:66-71`); `Levelized Replacement Cost` carries the inner maximum, clip, ceiling, and outer maximum (`exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py:58-107`). An expressionless calc output is an established `MANUAL_REQUIRED` interface on the exact route (`/home/reid/1cfe/sysml-codegen/tests/integration/test_expression_compilation_exact_route.py:46-56,130-136`).
- The pinned generator seals runtime contract `2.0.0` (`/home/reid/1cfe/sysml-codegen/src/sysml_codegen/contracts/versions.py:11-30`). Teax `744745f` accepts exactly that version and rejects the retired version before import (`/home/reid/1cfe/teax/packages/teax-simkit/simkit/evaluation/package_load.py:33-42,123-154`).
- The five adapter-supplied shapes now have native producer paths. The earlier probe found occurrence overrides, modeled defaults, aliases, and cross-part edges all survive the pinned route; the evidence and original model sites are enumerated in the reconciliation research (`.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md:118-130`). If one is absent after regeneration, re-injecting it would hide a toolchain failure and keep the CAS27 hole open.
- The generic identity mechanism already represents a clean sealed route. `build_sealed()` emits the package fingerprint with no modified-file or adapter-source set (`scripts/study/identity.py:135-159`), and preflight recomputes that identity before checking manifest currency, the baseline, and package cleanliness (`scripts/study/preflight.py:214-259,262-306`). No replacement adapter is needed.
- The before-record is a value oracle rather than a byte oracle. It fixes the baseline, five source-local verdict identities, 948 design-search points, 19 availability points, and the rel `1e-9` bar while allowing entry-key names to move (`exploration/stellarator_e2e/studies/BEFORE_MIGRATION_RECORD.md:30-39,55-81,99-107`).
- Promotion has one shared-file conflict to resolve, not eleven simple additions. The MFE twin adds `mfe_divergent` to the shared CAS-scope enum (`exploration/stellarator_e2e/models/foundation/economic_parameter.sysml:21-40`), while canonical and the IFE twin still carry two members (`models/library/foundation/economic_parameter.sysml:21-34`). The landing attempt already proved that synchronizing only canonical breaks the IFE byte gate (`.project/active/stellarator-demo-landing/plan.md:294-301`).
- Two stop-parser acceptance tests also assume canonical `models/` is one HIF plant. They map the whole canonical tree to the IFE twin and pin HIF-only channels or mutations (`tests/test_codegen_teax_acceptance.py:16-32,130-142`; `tests/test_occurrence_mutation_teax.py:18-28,64-103`). They need an IFE canonical subset, not a broadened two-plant expectation.
- Stock teax's evaluator interface needs `expects_constraint_report`, derived from the embedded model contract, and study-store compatibility uses the contract's published semantic fingerprint (`/home/reid/1cfe/teax/packages/teax-simkit/simkit/evaluation/evaluator.py:123-151`; `/home/reid/1cfe/teax/packages/teax-simkit/simkit/study/config.py:90-106`). The package-local stock route must adapt both, not only swap loaders.
- The package alias is a tracked absolute symlink into the predecessor worktree (`tests/study/conftest.py:19-24`). Keeping that target would make a nominal stock route depend on the old worktree even after the adapter is gone.
- Bare `uv run agentic-mbse validate models/` runs the complete six-level stack, which is already red at Levels 2 and 6. The current passing project bar is Level 1. This design therefore makes Level 1 the acceptance gate and treats the complete run as an offender-delta report, matching the spec's instruction to record the level rather than asserting a false clean baseline.

## Core Concept

This system is a controlled compiler-compatibility cutover around one semantic source: the MFE SysML model. The self-contained staged MFE tree is the migration workbench. Every source edit is classified and ledgered there, then the pinned codegen regenerates the package from scratch while preserving only the two signature-matched handwritten implementations. A clean `2.0.0` seal is the boundary: after stock teax accepts it and value-based evidence matches the before-record, the same MFE source files are promoted byte-for-byte into the canonical model tree, package-owned manifests and tests are re-pinned, and the era adapter is deleted whole. Existing codegen, stock loader, study tools, oracle, and identity gates keep their current responsibilities; the design adds no compatibility layer to replace the one being removed.

## Key Bets

- **B1.** The known Class A and Class B edits are semantically inert at every accepted study point, not only at the baseline. *If false → the value comparison fails or, worse, the package appears migrated while a study result changed for an unexplained reason.*
- **B2.** The pinned generator carries all five formerly injected shapes from authored model source into the sealed package. *If false → the stock route cannot replace the adapter honestly, and the finding is Class C.*
- **B3.** The staged MFE tree is self-contained and its final files can be promoted into the canonical tree without relying on hidden IFE definitions. *If false → family-scoped generation and canonical/twin equality cannot both pass.*
- **B4.** Teax `744745f` is the stock runtime for this cutover and remains compatible with the generated `2.0.0` contract. *If false → the package can seal but the after route cannot execute; the design would need an owner decision on a runtime pin or a different tested commit.*
- **B5.** Numerical comparison by physical point and `source_local_identity` survives D-5 key movement. *If false → the before-record cannot distinguish harmless naming changes from actual numerical drift.*

## Key Decisions

- **D1. Migrate in the staged tree, then promote once.** Run the D-5 transformer and all refusal-driven edits against `exploration/stellarator_e2e/models/`. After clean generation and evidence, copy the final MFE files into `models/` and prove byte identity. *Rejected: promote first and run D-5 over the mixed canonical tree (the IFE family already contains `_in` names that invalidate the transformer's tree-wide preconditions).*
- **D2. Represent both function-bearing calculations as honest manual interfaces.** Keep their formulas, sources, guards, and numerical contract in each calc doc; retain all input formals; reduce the executable body to an opaque output so every unsupported invocation disappears from source evidence; preserve the existing handwritten implementations and oracle mirrors. *Rejected: helper calc definitions (the exact route still visits and refuses their invocations) and `sqrt(x) → x ** 0.5` alone (it would not clear CAS72 and could make the peak-only DT statement look like the normative executable behavior).*
- **D3. Reuse the sealed identity path.** The stock study-local route emits `identity.build_sealed(...)`; generic identity, manifest, preflight, and verification code remain unchanged. *Rejected: a replacement compatibility adapter or a package-specific branch in `scripts/study/` (both would preserve the architecture this item exists to retire).*
- **D4. Use the existing runtime-root contract without adding a fusion-tea teax pin.** Study integration tests consume teax through `STOP_PARSER_TEAX_ROOT`, assert that the loaded `simkit` is under that root, and record the tested commit (`744745f`) in the after evidence. *Rejected: a hard-coded `/home/reid/...` path (not portable) and adding teax as a new dependency or pin (expands this item into a shipment and conflicts with the fixed-toolchain non-goal).*
- **D5. Keep one migration PR with internal gates.** Model repair, regeneration, source promotion, runtime cutover, and adapter deletion land together on `feat/stellarator-model-migration`, but each gate produces reviewable evidence before the next boundary. *Rejected: separate model and retirement PRs (would leave an intentionally transitional route on `main` and contradict the branch contract recorded in the spec).*
- **D6. Replace the migration-era spine with one family registry and named mutations.** A successor `tests/models/test_model_family_spines.py` holds small IFE and MFE family specifications. Generation, live/snapshot equality, census, canonical/twin equality, and canonical-path coverage are parametrized; family-specific mutation proofs stay as named tests in the same module. *Rejected: two modules (duplicates subtle source/consumer and logical-path machinery) and one opaque data table for all mutations (hides family meaning).*
- **D7. Drop the one-time D-5 partition while preserving its census.** Merge the eleven renamed and seven unrenamed IFE identities into one exact neutral IFE design-attribute census; keep source uniqueness, the 23/18 classification, and both every-and-only mutations. *Rejected: keeping “renamed” assertions forever (pins a completed migration event) and deleting the identity sets (weakens the regression proof).*
- **D8. Materialize family subsets for generation.** The family registry builds temporary canonical subsets and compares each to its self-contained exploration twin. The union of owned paths must cover every canonical SysML file; shared paths belong to both families and must be byte-identical in canonical, IFE twin, and MFE twin. *Rejected: generating the 22-file canonical union as one plant or allowing shared twins to diverge.*
- **D9. Promote the shared CAS-scope enum to all three homes.** The three-member `economic_parameter.sysml` becomes canonical and is synchronized into the IFE twin as well as the MFE twin, then the unchanged IFE census proves the new enum member is inert for IFE. *Rejected: MFE-only divergence (breaks twin honesty) or omitting `mfe_divergent` from canonical (leaves the promoted MFE design incomplete).*
- **D10. Keep the package alias, but make it relative.** Repoint `exploration/stellarator_e2e/pkg/stellarator_tea` to `../generated` so the manifest and test path remain stable without depending on another worktree. *Rejected: retaining the absolute symlink (hidden era dependency) and removing the alias in the same migration (unnecessary churn across package paths and recorded manifests).*
- **D11. Make obsolete annex sections optional in the generic runbook.** Remove the package's loader/glue and era-pin sections as the spec requires, and change the two runbook references to conditional reads when those sections exist. *Rejected: empty compatibility sections (dormant architecture) and broken unconditional links.*
- **D12. Use the full grid as one-time migration equivalence, not a live-model regression.** Run the 948-point grid and 19-point sweep against the before-record during acceptance and commit the result. Do not keep a historical numerical expectation attached to the evolving `models/` tree. If this model is later valuable as a toolchain regression, freeze both its source and expected outputs under `tests/fixtures/` and run only against that immutable copy. *Rejected: a permanent before-versus-live-model test (confuses intentional model improvement with toolchain regression) and dropping the migration comparison before semantic equivalence is proved.* **[OWNER 2026-08-21]**
- **D13. Put explicitly bound formals before skipped defaults.** Reorder the four affected calc interfaces so required and explicitly bound formals form the prefix and skipped defaulted formals come last. This repairs the declaration invariant without repeating `pi`, rates, or other literals at every use. *Rejected: bind every formal at the four usages (duplicates library values in designs, creates MR-4 citation work, and leaves the unsafe interface order available to the next usage).*
- **D14. Remove trailing-comment metadata from all MFE input formals.** Move the existing prose immediately above each of the 101 affected `in attribute` declarations. This preserves documentation while deterministically removing the metadata source that codegen interprets as a unit. *Rejected: harmonizing arbitrary prose into one projected unit (keeps an accidental channel alive), deleting the documentation, and introducing typed units during a compatibility migration.*
  *Implementation finding (2026-08-21, plan Phase 1):* the collision source is codegen's unit scraper, not the formals' comments alone — it seeks a byte offset while walking the file by character count, so multi-byte characters shift the scanned line, and it projects the first word after `//` on any declaration line as a unit. The move was applied to all 174 declaration lines (formals and attributes) and comment/doc text was ASCII-normalized in the 8 files with `//` comments (ledger F3, Class B, filed upstream). D14's rejection of typed units and of deleting the documentation stands.
- **D15. Commit the migration verdict, not a second live oracle.** Add `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md` with tool revisions, commands, artifact hashes, baseline values, grid and sweep verdicts, mutation results, and any explained deviations. Temporary comparison outputs may be discarded after their hashes and verdicts are recorded. *Rejected: retaining a runnable old-versus-current comparison path after acceptance (it would preserve the retired runtime and bind future model changes to historical numbers).*

## Architecture

The cutover has one forward path:

```text
staged MFE SysML
  → classified source repairs + migration ledger
  → pinned codegen generation and 2.0.0 seal
  → stock teax strict load + sealed identity
  → one-time before/after value evidence
  → byte-identical promotion + family and mutation proofs
  → era adapter and glue deletion
```

### 1. Source-repair boundary

The D-5 transformer produces a scratch result from the staged MFE tree. The implementation reviews its 99 changed binding sites plus the matching formal declarations, replaces the staged source with the transformed result, and records every changed site. Subsequent generation diagnostics drive only the three spec classes: Class A fixes a bad authored pattern, Class B moves unsupported executable syntax behind an honest manual interface, and Class C parks dependent work for the owner.

The model ledger is updated in the same change as each source edit. It records final canonical file and line, diagnostic or rule, class, replaced form, rationale, revert marker, and `Source`/`Ref`/`Basis` when a value is introduced or relocated. The D-5 site inventory seeds the many mechanical rows; the ledger is generated and reviewed as evidence, not hand-maintained from memory.

### 2. Generation and seal boundary

Generation runs from the repaired staged tree through the installed pinned codegen, never through a local checkout at `HEAD`. The output is the existing `exploration/stellarator_e2e/generated/` package root. `--smart-regen --preserve-handwritten` preserves only valid signature-matched human implementations; generated auto-implementations are rebuilt. The resulting seal must report zero readiness diagnostics, runtime contract `2.0.0`, and zero hash differences before any runtime or study evidence is accepted.

### 3. Stock runtime boundary

The package-local execution path constructs teax's stock `ProvisionalPackageLoader` with `strict=True`. A successful load returns the sealed executable fingerprint. The study route writes the existing sealed identity document, so preflight, store lineage, and verification all operate on the identity the package actually earned.

The route also loads the embedded model contract, derives `expects_constraint_report` from its catalog, and passes the contract's `semantic_fingerprint` into study configuration. These are teax `2.0.0` integration requirements, not new fusion-tea abstractions.

No runtime code supplies CAS28, `n_mod`, dead fillers, BOP repoints, or CAS27. Their appearance in package inputs and producer edges is checked from sealed artifacts. Their values are then exercised at baseline and mutation points.

### 4. Evidence boundary

Manifest re-pinning is a declaration step after the new package exists: update both fingerprints, qualified baseline/tie keys, headline channel, verdict identities, and objective catalog from the sealed artifacts. Execute the baseline before preflight, then require `manifest_currency`, `identity`, `baseline_headline`, and `package_clean` to pass.

The one-time migration comparison joins old and new results on physical coordinates: `(R, a)` for the grid and `availability` for the sweep. LCOE uses relative deviation below `1e-9`; verdicts join on `source_local_identity`. Its output is committed acceptance evidence, not a test oracle for future live-model revisions. Generic oracle verification samples the new stores and must emit an empty `not_independently_verified` list because the regenerated package now computes CAS27. The package-owned oracle seam drops its glue sentinels, `GLUE_VALUE_KEYS`, and `glue_values()` surface. The objective catalog explicitly compares downstream `total_capital` and LCOE so an unrelated compared channel cannot mask missing CAS27 coverage.

### 5. Canonical promotion and family proofs

After the staged tree seals, its final MFE files become the canonical copies under `models/library/` and `models/designs/`. The shared `economic_parameter.sysml` is also copied to the IFE twin. Tests compare each canonical logical path to its family twin and generate the IFE and MFE families independently. The two root-level HIF acceptance tests materialize the same IFE-only canonical subset before exercising their existing contract. No test may generate the union of two plant families and call the result one package.

### 6. Retirement boundary

Only after the stock loader, values, oracle, family tests, and mutation proofs pass does the implementation delete `era_adapter.py`, `promotion_equivalence.py`, their fixtures and tests, and the glue branches in `run_design_search.py`, `run_stellaris.py`, and `run_stellaris_single.py`. `oracle_entry.py`, `verify_stellaris.py`, and all generic study tools stay. The annex loses only its loader/glue and era-pin sections; the runbook treats those package-specific sections as optional; the historical before-record keeps the retired identifiers as evidence.

## Required Invariants

- **I1 — Source authority.** Model source and the two declared handwritten implementations are the only human-authored executable semantics. No generated file outside `handwritten/**` is edited after generation.
- **I2 — Exact toolchain.** Generation imports sysml-codegen at `8a758e92`; runtime tests import teax from the declared `STOP_PARSER_TEAX_ROOT` and record `744745f` for acceptance.
- **I3 — Classified edits.** Every changed model site has exactly one ledger row and one R5 class. A Class C row cannot be followed by dependent implementation work without owner direction.
- **I4 — Manual honesty.** The two opaque calc interfaces keep the same input/output contract, complete formula documentation, normative handwritten behavior, and independent oracle mirror.
- **I5 — Seal integrity.** The stock strict loader accepts with no exception set; all artifacts match the seal; the study identity digest equals the sealed executable fingerprint.
- **I6 — No injected glue.** No execution path mutates package inputs or pipelines or supplies any g1/g2/g3 value outside the package's declared entry inputs.
- **I7 — Migration continuity.** For this cutover, baseline, grid, and sweep meet the before-record by value at rel below `1e-9`; all five verdicts match by source-local identity. The historical values do not constrain later changes to the living model.
- **I8 — Independent CAS27.** Verification receives CAS27 from the package on one side and the oracle recompute on the other, and emits no disclosure exception.
- **I9 — Twin equality.** Every promoted MFE SysML file is byte-identical between its canonical and staged logical paths; the equivalent IFE invariant remains intact.
- **I10 — Family isolation.** IFE and MFE generation, census, and mutation assertions each use their own family tree and expected outputs; the union of their owned paths covers canonical `models/`.
- **I11 — Package-agnostic tools.** No stellarator key, path, adapter, or fallback enters `scripts/study/`.
- **I12 — Historical containment.** Retired era identifiers remain only in the before-record and historical project records, never on an executable, test, or runbook path.

## Component Overview

- **Staged MFE model tree** — `exploration/stellarator_e2e/models/`. Owns migration work and remains the self-contained generation input.
- **Canonical model tree** — `models/`. Owns the approved IFE and MFE library/design sources after promotion; it is a source collection, not a single generated plant.
- **Migration ledger** — `models/stellarator_migration_ledger.md`. Owns the site-level audit trail and revert markers for toolchain-shaped edits.
- **Generated package** — `exploration/stellarator_e2e/generated/` and its `pkg/stellarator_tea` link. Owns sealed `2.0.0` runtime artifacts and the two human implementation files under `handwritten/**`.
- **Package-owned study surface** — `exploration/stellarator_e2e/studies/`, `study/run_design_search.py`, and `run_stellaris.py`. Owns manifest facts, entry-key/oracle mapping, study definitions, and stock loader construction.
- **Generic study tools** — `scripts/study/`. Continue to own manifest parsing, identity, preflight, and verification without migration-specific changes.
- **Model regression surface** — `tests/models/` plus the sealed-runner model tests in `tests/`. Owns family census, live/snapshot equality, twin equality, mutation reachability, and teax execution.
- **Study regression surface** — `tests/study/`. Owns the stock route, manifest gates, oracle parity, and retained package-specific evidence checks after era-only tests are removed.

## Non-Goals

- Run-Study Item 6, a new design study, visualization, or any on-hold Stellarator Demo item.
- Changes to sysml-codegen, teax, agentic-mbse, 1costingFE, or fusion-tea's dependency pins.
- New model physics, changed cost constants, or use of the quarantined hold-out.
- A general generated-artifact tracking policy or repair of `uv.lock` regenerability.
- Creating a permanent stellarator toolchain fixture. Acceptance may recommend one, but any such fixture is frozen under `tests/fixtures/` and scoped separately from the living model.
- Deleting the era teax worktree or rewriting historical records that correctly name it.

## Implementation Notes

- Do not run the D-5 utility against the mixed canonical tree. Its tree-wide `_in` collision check is correct for an unmigrated customer tree and will encounter the already-migrated IFE family.
- D-5 changes the two handwritten input interfaces. Update the implementation field accesses to the regenerated `_in` names, then prove signature preservation. Use smart regeneration together with handwritten preservation; preservation alone blindly skips stale files.
- The DT implementation moves eight input fields to `_in` while `V` stays unchanged; CAS72 moves `ash_frac`, `fluence_limit`, `availability`, and `operational_years` to `_in`. Update those accesses before smart regeneration so the preservation check retains the normative files instead of backing them up and stubbing them.
- Delete generated `AUTO_IMPLEMENTED = True` implementations before regeneration so they cannot be mistaken for human-owned files. The two normative implementations are the only preservation candidates.
- Keep function formulas in the SysML calc docs when making outputs opaque. Removing unsupported executable expressions must not remove the model's semantic explanation or MR-4 references.
- Resolve all generated key changes from the new contracts. Do not bulk-replace strings in manifests, CSV comparisons, or oracle maps by suffix.
- Finalize ledger line references after source repair stabilizes. Canonical paths are authoritative; twin equality covers the staged duplicates.
- Treat any numerical drift as a finding. Do not widen tolerances or normalize away a changed verdict.
- After the one-time grid passes, remove its live-model comparison harness with the other migration-only equivalence code. Keep the committed before/after result as evidence.
- Do not turn the accepted after values into permanent expectations for canonical `models/`. A future slow toolchain regression must copy both model source and expected outputs into a static fixture first.
- Repoint the tracked package symlink relatively before testing cleanliness; otherwise Git checks resolve into the predecessor worktree.
- Re-derive all known-answer fixtures from the regenerated contract. Do not copy MFE census numbers from the `1.0.0` contract, whose duplicated CAS27/CAS28 entries are part of the retired glue shape.

## Potential Risks

- **A new refusal appears after the known repairs.** Stop at that diagnostic, add a Class C ledger row, file the upstream limitation, and park generation, promotion, and retirement until the owner chooses a route. Do not generalize from the existing Class B decisions.
- **A renamed formal invalidates a handwritten implementation.** Change the two implementation accessors before smart regeneration, inspect the preservation decision, and compare the preserved file hashes. A generated stub is a failed gate even if the package seals.
- **The shared enum changes the IFE extraction surface.** Synchronize all three copies, then rerun the exact IFE 23/18 census and both mutations. Any new IFE input or changed consumer set blocks promotion.
- **Contract keys move in a way suffix matching cannot disambiguate.** Resolve keys through the emitted model contract and record their qualified identities in the manifest and after-record. Never pick the first suffix match.
- **The external teax root is not the tested revision.** Assert the imported module path, record `git rev-parse HEAD`, and stop if it is not `744745f`. This item has no authority to choose a new runtime revision.
- **The absolute package link masks old generated files.** Convert it before stock-route checks and assert the resolved path is inside this worktree.
- **A historical model value escapes into a permanent test.** The acceptance review checks that the before CSVs and after record are documentary evidence only. No test may load them as the expected output of the canonical live model.

## Integration Strategy

1. **Repair the staged source.** Run D-5 into scratch, review the 99 binding changes and matching declarations, apply the four formal-order fixes, normalize the 101 comment sites, make the two calculation interfaces manual, update handwritten accessors, and complete the ledger. Exit when all known edits are classified and no Class C row exists.
2. **Regenerate and seal.** Remove only auto-generated implementations, run the pinned generator with smart handwritten preservation, inspect the two preservation decisions, verify zero diagnostics and hashes, and strict-load the `2.0.0` package through stock teax. Exit when the package earns a sealed identity without injected values.
3. **Prove migration equivalence once.** Re-pin package-owned manifests from the emitted contract, execute the baseline, 948-point grid, 19-point sweep, CAS27 oracle comparison, and direct package mutation probes. Compare against the existing before artifacts by physical coordinate and source-local verdict identity. Commit `AFTER_MIGRATION_RECORD.md`; do not retain a live comparison harness.
4. **Promote and reshape model tests.** Copy the final MFE source into canonical paths, synchronize the shared enum to the IFE twin, restore the canonical power-balance path, and replace the migration spine with family-scoped generation and mutations. Exit when both twins are honest, each family generates alone, and owned paths cover all canonical SysML files.
5. **Retire the old route.** Delete the adapter, promotion-equivalence helper, era fixtures, and all package-owned glue. Convert the package link, switch the study entry points to the strict stock loader, remove the obsolete annex sections, and keep generic tools untouched. Exit when executable and test-path searches find no retired identifier.
6. **Close the branch gates.** Run licensed model and study suites, dependency provenance, lock validation, Level 1 model validation, the complete validation characterization, MR-4 review, and upstream backlog checks. Record commands, revisions, counts, and results in the plan and after-record.

This is one branch and one merge. Each numbered boundary is a checkpoint in the implementation plan, not a separately shippable compatibility state.

## Validation Approach

| Criterion | Required proof |
|---|---|
| SC1 | `uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten`; zero readiness diagnostics; runtime contract `2.0.0`; strict stock load; seal/hash check; recorded codegen and teax revisions. |
| SC2 | New baseline equals `275.2642200420774` at rel below `1e-9`; all five verdicts match by `source_local_identity`; all 948 grid and 19 sweep points match the before CSVs by physical coordinate and value. The committed proof is `AFTER_MIGRATION_RECORD.md`, not a permanent test against live models. |
| SC3 | Deletion inventory covers both adapter modules, `run_design_search.py`, `run_stellaris.py`, `run_stellaris_single.py`, era fixtures/tests, glue oracle surfaces, and the two annex sections. Repository search leaves retired identifiers only in the before-record and historical project records. |
| SC4 | Stratified verification at rel below `1e-9` produces an empty `not_independently_verified`; its compared channels include package-derived CAS27, oracle-derived CAS27, downstream `total_capital`, and LCOE. |
| SC5 | Manifest fingerprints, qualified keys, ties, baseline, verdict identities, headline channel, and objectives are derived from the sealed contract. All four preflight gates pass, and `git diff -- scripts/study/` is empty. |
| SC6 | Canonical contains 22 SysML files: 11 IFE plus 14 MFE minus three shared files. Every family path is byte-identical to its twin; the power-balance test uses `models/library/`; staging and model READMEs describe a twin rather than a quarantine. |
| SC7 | Licensed `tests/models/test_model_family_spines.py` proves per-family generation, live/snapshot equality, exact census, twin equality, and canonical coverage. IFE remains exactly 23 entry points and 18 design attributes with both existing mutation proofs. MFE expectations are captured from its first clean `2.0.0` package. |
| SC8 | `models/stellarator_migration_ledger.md` has one row per edited site with final canonical location, trigger, R5 class, replaced form, rationale, revert marker, and MR-4 fields where applicable. The upstream revert backlog row points to it. |
| SC9 | The sysml-codegen backlog records the four positional sites and attaches all six scalar-function sites to `[SCALAR-FUNCTION-VOCABULARY]`; every later toolchain limitation has a matching filing. |
| SC10 | A CAS28-capital mutation changes exactly its direct consumers. A nested blanket-thickness mutation changes exactly its direct consumers. Both run through the regenerated stock package and assert non-consumers remain unchanged. |
| SC11 | Licensed `tests/models`, `tests/study`, and the two root acceptance surfaces pass with family-scoped inputs; dependency-provenance tests and `uv lock --check` pass; `uv run agentic-mbse validate models --level 1` is green. `--complete` is recorded as an existing-offender delta, not misreported as the passing gate. Review confirms MR-4 citations. |

## Next-Stage Handoff

The implementation plan must preserve these fixed decisions: staged-tree-first migration; 99 binding sites; manual DT and CAS72 interfaces backed by the two existing handwritten implementations; smart regeneration; stock strict loading and sealed identity; one-time numerical equivalence; family-scoped promotion tests; full adapter deletion; and Level 1 as the current model-validation gate.

Plan the riskiest checkpoint first: apply the known source repairs and attempt a clean pinned generation before spending effort on promotion, manifest churn, or adapter deletion. An unknown refusal is the only anticipated owner stop. The exact MFE census and qualified contract keys are implementation outputs, but their derivation method is fixed: read them from the first clean sealed package and record them rather than guessing from the retired contract.

After design approval, run `$my-design-review` for an independent pressure test, then `$my-plan` to turn the six integration boundaries into persistent checked phases. Do not begin implementation from this draft.
