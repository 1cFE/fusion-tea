# Independent review execution record

[AGENT] Reviewed design/prototype commit `66c2b5c09abcaaad99bc9587de7b3d055f454337`. This directory contains review-only evidence; the source prototype was not edited. Numerical replays used `/tmp/wi051-review-aSYTns`; independent validation/regeneration used `/tmp/wi051-validation-review`. Temporary directories are conveniences, not required historical authority.

[AGENT] For numerical reproduction, create a fresh temporary directory and copy `prototype/generated/`, `execute.py`, `direct.py`, `standalone.py`, `cli_checks.py`, `expectations.json`, and `frozen-results.json` there from the reviewed commit. Run the following from the repository root, replacing the temporary path as needed. Each command exited 0 in this review. `direct.py entering` intentionally records the original helper's `PipelineValidationError` while the original single runner succeeds. It requires the unchanged entering production package; after implementation use the original checkout/package identity, never repaired outputs as expectations.

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python /tmp/wi051-review-aSYTns/direct.py entering'
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python /tmp/wi051-review-aSYTns/execute.py'
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python /tmp/wi051-review-aSYTns/direct.py prototype'
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python /tmp/wi051-review-aSYTns/standalone.py'
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python /tmp/wi051-review-aSYTns/cli_checks.py'
.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/review-evidence/check_evidence.py /tmp/wi051-review-aSYTns
```

[AGENT] The first five commands replay the inspected, committed probe scripts in isolation. The final command is separately authored review verification of immutable comparator hashes, complete input records/defaults, all nine edges, all scalar channels and reports, independent ratios, and source/package/manual hashes. Its results are `independent-checks.json`; the execution records copied from the isolated run retain all numerical outputs, structured reports and explicit errors. CLI child logs retain baseline success and three expected exit-1 refusals.

[AGENT] The independent validation reviewer copied the model families and preservation inputs into its own fresh directory and ran `.codex-test/run agentic-mbse validate --complete /tmp/wi051-validation-review/models` (exit 1, inherited L2/L6 failures). It replayed `prototype/preservation.py` against that isolated directory and separately generated an empty `fresh-live` destination seeded only with the four normative handwritten bodies (both successful). See `validation-review.md`, `validation/validation.log`, `validation/validation-diff.json`, `validation/preservation.log`, `validation/preservation.json`, and `validation/fresh-live-proof.json` for results and identities.

[AGENT] Four fresh delegated checks were obtained: `/root/pr_review` (requirements/source scope), `/root/ad_review` (architecture/caller), `/root/conventions_review` (SysML), and `/root/validation_review` (validation). No author was resumed. PR review found the citation-format concern; the SysML reviewer concurred after reconciling the explicit MR-4 format rule. AD supplied the empty-generation-destination suggestion. Validation supplied no additional concern. Parent dispositions remain pending.
