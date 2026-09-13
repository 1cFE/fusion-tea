# WI-051 independent architecture review

Reviewed the committed design/prototype against `work/orchestration/mfe-model-owned-major-radius.md@b847558b`, `spec.md@99aee8cd`, current AD-001–007, the Codex adapter and setup, and the actual proposed source/caller patches. This is the architecture portion of the native review. Dispositions below are recommendations for the parent, not owner decisions.

## Verdict

Pass for architecture, with one optional implementation suggestion. No critical finding or concern requiring design revision was identified. This does not certify production implementation, full regression, source approval, or the excluded study migration.

## Finding

- **AD-R1 — suggestion; proposed disposition: accept into implementation mechanics.** Assert that each native generation destination is absent or empty before seeding the four manual bodies. `prototype/build.py:25–29` and `prototype/preservation.py:19–22` use `preserve_handwritten=True` without enforcing freshness themselves. The documented fresh-directory workflow is adequate for the retained prototype, but accidental reuse would preserve all existing generated bodies and still print the freshness claim. This is a reproducibility improvement, not evidence that the retained generation was stale. Keep the recorded evidence immutable; apply the guard to the later production-generation procedure or fresh reproduction copy.

## Checks and evidence

- The producer binding belongs on the generic plant's magnet usage. The reusable library formal remains intact, consistent with AD-006/007. The exact source patch changes two logical design files; the design explicitly requires canonical/twin application and leaves the other 21 family files unchanged (`design.md:22–44`, `prototype/proposed.patch`). No library equation, finance convention, or supported concept is added.
- The direct-caller patch matches the real API. It adds keyword-only pipeline/output paths to functions that previously had no parameter override API. It passes the pipeline to stock execution with generated custom schemas. The generated plant schema uses `extra='forbid'` and contains plant R but no magnet R0 (`prototype/generated/schemas/stellarator_plant_params.py:192`). The design explicitly limits compatibility to the unchanged generated graph with modified JSON; it does not claim that the package seal validates arbitrary external YAML (`design.md:84–88`).
- The original helper actually fails with `PipelineValidationError`, whereas the original single runner supplies the complete raw baseline/tied controls. The bounded router registration/scalar-output fix is visible in `prototype/caller-proposed.patch` and independently distinguished from the binding change in `design.md:90`. The retired-alone/equal/conflicting/zero proposals all retain the exact obsolete key in both callers' validation failures (`prototype/direct-entering.json`, `prototype/direct-prototype.json`). No JSON key filtering is present in the patch.
- Independently recomputed SHA256 inventories match `prototype/generated-hashes.json`; the generated and snapshot-generated packages match byte for byte. All four manual-body hashes match both the prototype and current production files. This checks the retained package and preservation claim without rerunning or rewriting the author's evidence. The design correctly leaves production census/snapshot updates and complete family regression to implementation (`design.md:142–154`, `:172–178`).
- Independently compared all raw baseline outputs against the entering single-runner record: exact equality. Also checked the original helper failure and every recorded retired-key refusal in both direct paths. These checks used `.codex-test/run` with the prescribed TEAx environment, exit 0. No model execution or regeneration was repeated by this reviewer.
- The later coding handoff names the oracle's incorrect sustainment operand, adapter key rejection, mapping/census, manifest/route tie retirement, annex, fixtures, generic tie tests, and historical pins. It identifies exact contract/edge/control/hash artifacts and says current-study compatibility remains incomplete (`design.md:159–170`). No completion credit for those excluded surfaces is taken.

## Limits

The direct execution results are retained prototype evidence; this reviewer inspected their checks and independently verified selected serialized results and hashes, rather than repeating every runtime case. Source meaning remains inherited from T-021. L2/L6 failures, the open F07 component defect, and production regression obligations retain the design's stated limits.
