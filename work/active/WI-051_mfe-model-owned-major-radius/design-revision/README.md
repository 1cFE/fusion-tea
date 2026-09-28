# WI-051 bounded design correction evidence

[INHERITED] Parent accepted R1 and R2 in [stage-provenance/design-review.md](../stage-provenance/design-review.md). Immutable alignment is `work/orchestration/mfe-model-owned-major-radius.md@b847558b`; source interpretation is inherited from T-021 at `2f8856b7`. This directory records an author correction and native parsing, not an independent review or production implementation. The original [review](../review.md) remains `concerns`.

## R1: attached source documentation

[AGENT] [proposed.patch](proposed.patch) is the exact revised delta against `prototype/entering-models/`, applicable with `-p1` from a family root. It contains the generic radius binding with attached structured documentation and the original stellarator literal removal. [from-prototype.patch](from-prototype.patch) is the exact documentation-only change against the already proven `prototype/models/`. The isolated [models](models/) copy contains the same 23-file family. Only the generic plant file differs from the original prototype; the other 22 files are byte-identical. Neither patch changes an equation.

[AGENT] The `Source` field points directly to `work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md`. `Ref` names `## Model and existing source interpretation` and `## Assessment` at `2f8856b7`. `Basis` explicitly inherits the existing model-intent interpretation of a shared plasma/axis scale and distinguishes it from real modular-coil surfaces and the separate minor-radius quantities. Preparation compared the citation file with its immutable git object and the retained frozen source-meaning copy; all match SHA256 `92110f6a826da0ed3031db2c361565209271fd43bd20c18798d5bb8a297c1c36`. No fresh physical-source assessment or source approval is claimed.

[AGENT] Native L1 validation passed: 23 files, zero errors and zero warnings. [parse.json](parse.json) additionally records zero parser/semantic errors and the documentation attached to `mfe_plant::'MFE Power Plant'::magnet::R0`, whose native type is `ReferenceUsage`. The initial probe queried `AttributeUsage` and failed its attachment assertion despite successful parsing. That probe, log and JSON are retained as `parse-attempt-1.*`; only the probe's element-kind query was corrected. The source stencil did not change after that attempt.

## Source and package identities

[AGENT] The generic plant source SHA256 changes from `73cf854e9df48aa5e93f6ca8c7e7740fdbb83fe649a100275f7b4defb78f8841` to `266c39d3f069620a22a62879b6b8d8f04527953cf3a439fef222fca89868cad7`. [source-identity.json](source-identity.json) records all original and revised source hashes and identifies the original prototype commit `66c2b5c09abcaaad99bc9587de7b3d055f454337`.

[AGENT] No package was generated from this revision. Its semantic and executable fingerprints are therefore explicitly unmeasured. Documentation can affect extraction and package metadata; the old package fingerprints and old live/snapshot equality identify only the original proven prototype. Implementation must freshly generate from these revised sources, re-derive all identities and establish live/snapshot agreement and the required numerical comparisons. Repeating the full numerical study solely for this documentation correction is unnecessary; the original numerical and independent review evidence is preserved without being relabeled.

## R2: generation and reproduction obligations

[AGENT] The design now requires a recorded destination check before either seeding or native generation, independently for source and snapshot generation. The destination must be absent or an empty real directory, counting hidden entries. Reject a populated destination, non-directory or symlink without modifying it. If absent, create it exclusively. Retain failed attempts and choose a fresh path on retry. This corrects the original scripts' unenforced freshness assumption; it does not assert stale generation in the retained prototype.

[AGENT] Seed exactly the four paths and hashes in [manual-preservation.json](../prototype/manual-preservation.json), and check the full seed file inventory against that manifest before generation. The four bodies are lifecycle calendar, DT fusion power, plasma sustainment and power-cycle efficiency. Independently repeat the precondition and seed check for snapshot generation. Retain the empty-destination observation, exact pre-generation seed inventory, unchanged manual hashes afterward, complete generated inventory and re-derived package identities. These safeguards apply to copied reproduction scripts as well as implementation; the original scripts and outputs remain untouched.

[INHERITED, REFERENT] Correct chronology for reused reproduction descriptions: the 158 numeric expectations and coverage were frozen from `2f8856b7` before original prototype generation. The additional 177-channel raw representation was captured through the unchanged original single runner after generation but before repaired execution. The raw capture adds no new numeric channels. The stale description in the original `expectations.json`/`freeze.py` is preserved with its original hash; this revision reuses no corrected expectation file and derives no expectations from repaired outputs.

## Commands and preservation

[AGENT] Commands ran from `/home/reid/1cfe/fusion-tea-codex-test`. Every Python/model invocation used `.codex-test/run`; no installation or synchronization was performed. `prepare.py` refuses to overwrite an existing revised model copy. To reproduce, place these scripts in a new sibling evidence directory alongside the original `prototype/`; retain this directory as evidence.

```bash
.codex-test/run python -B work/active/WI-051_mfe-model-owned-major-radius/design-revision/prepare.py > work/active/WI-051_mfe-model-owned-major-radius/design-revision/prepare.log 2>&1
.codex-test/run python -B work/active/WI-051_mfe-model-owned-major-radius/design-revision/parse.py > work/active/WI-051_mfe-model-owned-major-radius/design-revision/parse.log 2>&1
.codex-test/run agentic-mbse validate --level=1 work/active/WI-051_mfe-model-owned-major-radius/design-revision/models > work/active/WI-051_mfe-model-owned-major-radius/design-revision/validation-l1.log 2>&1
```

[AGENT] Preparation exited 0. The initial parse probe exited 1 for the query mistake described above; the corrected probe and native L1 CLI each exited 0. Two read-only native probes enumerated model element kinds to resolve the query mistake. Shell operations inspected files, retained the failed probe and ran whitespace/diff checks. [protected-before.json](protected-before.json) inventories 4,048 protected file contents and symlink targets, including original prototype, frozen expectations, review and review evidence, canonical/twin models, production generated package and direct callers. [preservation.json](preservation.json) records an exact match after parsing. Existing concurrent workspace changes were preserved.

[AGENT] Remaining obligations are the design's mandatory fresh generation and identity derivation, production tests/native validation and the independent production audit. Parent verifies these objective corrections before fresh plan-model. This author found no new blocker and stopped before planning or production changes.
