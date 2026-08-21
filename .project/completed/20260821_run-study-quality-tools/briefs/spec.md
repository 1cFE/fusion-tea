# Brief: spec for "Quality Tools and Era Adapter Promotion" (RUN-STUDY Item 4)

Work item home: `.project/active/run-study-quality-tools/` — write `spec.md` there.

## Objective

Extract the proof-of-life's reusable mechanical gates into generic `scripts/study/preflight.py`
and `scripts/study/verify.py`, and isolate any still-required package workaround in a
package-local, self-checking `era_adapter.py` under a truthful effective executable fingerprint.

## Governing sources (read in this order)

1. `.project/backlog/epic_run_study_capability.md` — Item 4 section is your scope contract.
2. `.project/concepts/run-study-skill-design.md` — ACCEPTED design: Tools, "The package
   manifest ... and the temporary adapter", Architectural Bets (manifest+adapter), Required
   Invariants (Tools, Adapter → lineage), Validation Strategy, Edge Cases. Settled.
3. `.project/concepts/run-study-skill-design-review.md` — C4, C5, M6, m3.
4. `exploration/stellarator_e2e/study/run_design_search.py` — the 450-line proof-of-life
   script whose generic checks you promote (GlueAwareLoader, baseline gate, git-clean gate,
   stratified verification, dead-filler assertion, glue rungs g1-g3).
5. `exploration/stellarator_e2e/study/verification_summary.json` — the verification output shape
   that worked.
6. `.project/active/run-study-indicators/design.md` — Item 3's ACCEPTED design. Your tools
   consume its seams: `scripts/study/manifest.py` (manifest schema
   `study-package-manifest/v1`, fingerprint recipes, typed oracle object), JSON Schemas under
   `scripts/study/schemas/`. Item 3 is being implemented in parallel — cite its design, do
   not re-derive or fork its schemas.
7. `.project/active/run-study-contract/design.md` — Item 2's ACCEPTED design. The record
   snapshots an arm-scoped `verification` block (command, tool revision, sampling scheme,
   tolerance, digest of verification_summary.json); verify.py must produce what that snapshot
   needs. Preflight results are mandatory record content (pass/fail per gate).

## Forwarded findings you MUST address (verified by orchestrator 2026-08-19)

- **The preflight "manifest-fingerprint match" gate cannot be a sealed-hash match while the
  adapter exists.** The two glue-edited files (`pipelines/mfe_stellarator.yaml`,
  `inputs/system_design.json`) differ on disk from their sealed `artifact_hashes`; the
  `semantic_fingerprint` covers neither. Item 3's manifest pins an indicator-input fingerprint
  over the artifacts ITS trace reads. Your preflight needs its own honest gate design (the
  effective-fingerprint machinery is the design's frame: sealed fingerprint + allowed-modified
  file digests + adapter source).
- **The oracle has no parameterizable CLI.** `verify_stellaris.py` is module + `compute()` +
  module-global `IN` dict; `__main__` prints the fixed baseline only. The manifest records it
  as `{"kind": "python_callable", ...}`. Your verify.py consumes the typed oracle object
  through manifest.py; if you need a command form, add a package-owned CLI to the package-side
  script and amend the manifest field ADDITIVELY (coordinate: the manifest is Item 3's file;
  the amendment is data, your spec states it).
- **You author the package annex** `exploration/stellarator_e2e/studies/ANNEX.md` (path pinned
  by Item 2's design D9): era pin, oracle parameterization, glue rungs, loader exception,
  package-specific validity masks. Orchestrator ruling 2026-08-19.

## Scope (epic-fixed)

1. Generic `preflight.py`: declared-key validation (advisory sibling scan), manifest/package
   fingerprint gate (your honest answer above), baseline headline gate (pinned headline at
   rel < 1e-9), package git-clean checks.
2. Generic `verify.py`: stratified-by-verdict-combination sampling, package-owned oracle from
   the manifest, rel < 1e-9 channel comparison, verdict re-derivation,
   `verification_summary.json`.
3. AT ITEM START: probe whether the stock teax loader accepts the current package. If YES:
   delete the adapter path from the capability (no dormant compatibility code). If NO: extract
   package-local self-checking `era_adapter.py` + annex with its exact deletion condition.
4. If the adapter exists: bind teax to the effective executable fingerprint (sealed fingerprint
   + actual allowed-file digests + adapter source); glue and dead-filler assertions live inside
   the adapter.
5. Prove promotion equivalence: the promoted route reproduces both committed proof-of-life CSVs
   byte-for-byte; run missing-key, dirty-package, wrong-fingerprint, and modified-glue
   resume-refusal cases.

## Settled constraints

- [OWNER] Interpretive conditions never gate; mechanical failures exit non-zero.
- [AGENT ratified] Generic tools: no package-specific name, never import the adapter;
  adapter-owned checks run in the adapter. Every point executes through stock teax
  (`StudyRunner`); tools never own execution. No second execution facade, no hand-rolled sweep.
- [AGENT ratified] Era teax worktree pin: `/home/reid/1cfe/teax-v1-era` @ `fa0e06a` (see
  proof-of-life plan Phase 0 result). Current teax main refuses the package's v1.0.0 seal —
  that refusal is principled, not a bug; do NOT chase upstream changes (non-goal).
- The GlueAwareLoader accepts ONLY the exact diagnostic set {TAMPER on the two documented
  glue-edited files}; anything else still refuses.

## Out of scope (epic-fixed)

- Second execution facade or hand-rolled sweep loop; package knowledge inside generic tools;
  upstream teax or sysml-codegen changes; interpretive gating on indicators or outcomes.

## Success criteria (from the epic)

- Generic tools reproduce the proof-of-life mechanical gates with no package-specific code.
- Verification stays stratified, re-derives verdicts, emits the summary at rel < 1e-9.
- If retained, adapter route reproduces both committed CSVs byte-for-byte; changing an allowed
  glue file or adapter source changes effective identity and the old store refuses resume.
- If stock loading works, the adapter is absent, not dormant.
- Every point still executes through StudyRunner; tools do not own execution.

## Conventions

- `uv run python ...` always; working voice; provenance grades in the spec.
