# Brief: implement "Indicator Tool and Package Manifest" (RUN-STUDY Item 3)

Execute `.project/active/run-study-indicators/plan.md` phase by phase. Spec, design, and plan
are ACCEPTED. Tick checkboxes as you complete phases; add per-phase completion notes; run
`uv run python -m pytest tests/study` green before ticking any phase.

Hard rules from the accepted design (violations are defects, not choices):
- The committed package under `exploration/stellarator_e2e/pkg/` is READ-ONLY. All mutation
  tests run on `package_copy` temp copies.
- No partial output on failure; interpretive facts exit 0; mechanical failures exit non-zero.
- Grep-clean: no package name, no key prefix, no adapter import in scripts/study/*.py.
- Known-answer expectations come from the Item 1 fixture contract
  (.project/active/run-study-reachability-spike/findings.md) — never patched to pass.

Item 2's implementation runs in parallel with yours — you share no files with it. Do not edit
anything outside: `scripts/study/`, `tests/`, `exploration/stellarator_e2e/studies/`
(new directory for manifest.json), `pyproject.toml`+`uv.lock` (the jsonschema dependency),
`.project/active/run-study-indicators/`.

NOTE on uv.lock: it currently carries a pre-existing uncommitted modification (syside pin).
When you commit the jsonschema dependency change, commit ONLY the hunks your `uv add`
introduces if separable; if uv rewrites the lock wholesale, commit it and say so in the
commit message.

Commit at each phase boundary with a message leading with what the phase delivered.
End with ARTIFACT: <plan path> and a one-paragraph summary of deviations if any.
