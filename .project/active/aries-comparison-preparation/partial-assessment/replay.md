# Reproduce the partial-assessment report

Use the licensed sealed environment described in `.project/codex-test-setup.md`. The runner verifies the retained archive and native runtime identities before work. Existing attempt names cannot be overwritten. The archive remains the original adopted model package; the diagnostic runtime is selected explicitly by the new runner.

Reporting replay does not calculate the plant again:

```bash
.codex-test/run python .project/active/aries-comparison-preparation/partial-assessment/tools/assess.py --verify
.codex-test/run python .project/active/aries-comparison-preparation/partial-assessment/tools/replay.py --attempt .project/active/aries-comparison-preparation/partial-assessment/attempts/diagnostic-1 --out /tmp/partial-report-replay.json
```

The output file must not already exist. Replay checks attempt receipt hashes, request and input identity, reconstructs the graph from the adopted archive, and recomputes all qualification paths, definedness records and 276 report rows. It compares every rebuilt document with the retained document exactly. It invokes no evaluator.

The original physical diagnostic command was:

```bash
.codex-test/run python .project/active/aries-comparison-preparation/partial-assessment/tools/assess.py --store .project/active/aries-comparison-preparation/partial-assessment/attempts --name diagnostic-1
```

That attempt already exists; the command refuses to overwrite it. A future physical diagnostic must use a new attempt name under an appropriate instruction to perform that work. `adoption.json` is an exact identity of this runner version, not a moving pointer; edits require a separately recorded version, not silent replacement of the original attempt's identity.

The additional `evidence/predicate-interpretation.json` is a reporting supplement. Its source report digest and script digest identify `evidence/interpret_predicates.py`; the script reads retained native statuses and their observed `defined_in` values. It preserves all 67 statuses and adds interpretation. It performs no model evaluation. Copy the script and source layout to a fresh location to regenerate its output without overwriting the retained supplement.
