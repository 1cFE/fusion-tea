# Brief: spec for "Indicator Tool and Package Manifest" (RUN-STUDY Item 3)

Work item home: `.project/active/run-study-indicators/` — write `spec.md` there.

## Objective

Turn the Item 1 spike's proven trace into a package-agnostic indicator tool
(`scripts/study/indicators.py`) backed by a data-only catalog of stable package facts
(`exploration/stellarator_e2e/studies/manifest.json`).

## Governing sources (read in this order)

1. `.project/backlog/epic_run_study_capability.md` — Item 3 section is your scope contract.
2. `.project/active/run-study-reachability-spike/findings.md` — Item 1 spike findings, CONFIRMED
   2026-08-19. Contains: 12 proven parsing/normalization rules (R1–R12), the exact per-axis
   fixture contract (declared groups + expected outputs for availability, interest_rate, R,
   R+tie, a, beta), mechanical-outcome fixtures, and open questions addressed to you.
   The spike scripts (`trace.py`, `cases.py` in the same folder) are throwaway reference code —
   learn from them, do not import them.
3. `.project/concepts/run-study-skill-design.md` — ACCEPTED design: "The indicator builder",
   "The package manifest", Design Principles 1–2 and 4, Appendix A (field vocabulary — use
   exactly), Required Invariants (Tools).
4. `.project/concepts/run-study-skill-design-review.md` — C1 (declared groups, suffix advisory),
   M8 (reachable ≠ responds), m3.

## Scope (epic-fixed)

1. Define the `manifest.json` schema; populate the stellarator package catalog: declared ties
   (`magnet__R0` with `R`), objective-channel catalog, pinned baseline point + headline
   (LCOE 275.2642200420774, all 5 verdicts satisfied), package-owned oracle command, package
   fingerprint. Package catalog ONLY — no per-study choices, no executable behavior.
2. Implement `scripts/study/indicators.py` over author-declared qualified entry-key groups with
   per-key `fan_out | tie` provenance.
3. Emit: group validity, entry types, suffix-sibling warnings, conservative constraint/objective
   reachability, bound facts (from predicate_ir), `no_constraint_response` — Appendix A
   vocabulary exactly.
4. Tests: known-answer (all fixture-contract cases), missing-key, malformed-pipeline,
   valid-empty, suffix-warning.
5. Document the output schema (JSON) as the seam consumed by the runbook and record (Item 2).

## Settled semantics (do not relitigate; provenance as marked)

- [AGENT ratified 2026-08-19] Axis membership comes ONLY from the declared group; suffix scan is
  advisory warnings, never membership. `no_constraint_response` is a sound negative;
  `constraints_reachable` = conservative possible path, NEVER "responds". Monotonicity, cross-name
  same-quantity identity, and intra-module dependency are not derivable — every report states so.
- [OWNER] Interpretive facts never gate (exit 0); mechanical failures (missing key, fingerprint
  mismatch, unparseable artifact, ghost objective channel) exit non-zero. Valid empty result
  exits 0. A broken analysis must never look like an empty one.
- [AGENT ratified] The generic tool reads the manifest, contains no package-specific name, never
  imports any adapter. Package facts live only in manifest data.

## Spike open questions assigned to your spec (decide and record)

- Hand parser vs `yaml.safe_load` + strict schema validation: the property that must survive is
  "every unexpected construct raises" (spike probe 4 lesson: a negative test that corrupts
  nothing looks like a pass — keep its fix: assert the mutation target exists).
- Objective catalog: owned by the manifest (this item), not hard-coded. The spike's five channels
  (lcoe, lcoe_1cfe, cas72, fuel, total_capital) are the starting catalog.
- Multi-pipeline packages: only `mfe_stellarator.yaml` exists; design says `pipelines/*.yaml`.
  Decide the tool's stance (e.g., trace all files, fail on cross-file channel collision) and
  record it — do not silently assume single-pipeline.
- `lcoe_calc__discount_rate` vs `interest_rate` group: a MODELING question, out of your scope —
  the tool must not decide same-quantity identity. Exclude; note it.

## Out of scope (epic-fixed)

- Inferring group membership from suffixes; claiming positive response; deriving monotonicity.
- Preflight baseline/git gates, oracle sampling, adapter behavior, point execution (Item 4).
- Package-specific names or imports in the generic tool.

## Success criteria (from the epic)

- Known-answer tests pass for R, a, availability, interest rate, beta (per fixture contract).
- Valid empty exits 0; missing keys, fingerprint mismatch, unparseable artifacts exit non-zero.
- Suffix matches are warnings only, never alter declared membership.
- Generic tool contains no stellarator-specific name and never imports an adapter.
- Manifest is data-only, separating stable package catalog facts from study choices.

## Project conventions

- `uv run python ...` always; tests runnable via `uv run python -m pytest`.
- Working voice per `~/agentic-project-init/claude-pack/rules/working-voice.md`; provenance
  grades in the spec.
