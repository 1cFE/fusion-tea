# Synthetic comparison preparation v1

[AGENT] This preparation adapter evaluates the current supplied design through the native route. It loads no reference observations and cannot authorize a reference comparison or publication. The eight proposed controls are defined in `mapping.json`; reference-coil ampere-turns alone are refused. Unspecified controls remain visibly held at the pinned model defaults. The historical seven-input intent requires a separate mapping decision before any reference use.

Run from the repository with its documented sealed environment:

```bash
.codex-test/run python .project/active/model-evaluation-comparison-adapter/v1/adapter.py --request synthetic.json --store /tmp/preparation-store --attempt example
```

The request has exactly `schema_version: "adapter-request/v1"`, `purpose: "synthetic_preparation"` and a `values` object. An empty object evaluates held defaults. Each supplied key requires `value`, `unit`, `definition`, `resolution: "matched"`, and a nonempty synthetic `source` label. Match units/definition identifiers in `mapping.json` exactly. Fixture provenance is not proof of scientific correspondence.

The immutable identity ledger pins source, generated package, native route, adapter, mapping and historical criteria/accounting bytes. Initial development capture uses `--pin` after review; it refuses an existing pin. Identity drift refuses execution. The current package loader independently enforces its sealed runtime contract.

Each attempt exclusively retains its raw request, selection, native case/database, terminal result, model export and hash receipt. `first-attempt.json` atomically reserves the first attempt before decoding. A refused or interrupted first attempt remains first; a later successful result is a later attempt. Duplicate names refuse without touching the first result. A malformed first pointer blocks further custody rather than resetting it. Interrupted attempts lack a terminal `result.json` and remain visibly incomplete. Receipts are tamper-evident hashes, not write-protection against external filesystem edits.

Historical criteria and accounting are byte copies. Current roles/applicability are a separate export overlay: direct controls are supplied/held, computed responses (including ampere-turns and field) remain calculated, and partial runs produce no available predictions. Raw partial native evidence remains separate. No row earns independent comparison credit. Completion means output/verdict inventory is complete; failed physical checks and empirical limits remain distinct. The full current predicate inventory is retained separately from the historical manifest.

Account scope, mixed-year money, C220107 lineage, unresolved installed scope and the distinction between calculated primary pumping and total pumping remain inherited limitations. Supplied prices represent selected offers. Holdings are not qualification, and this adapter never restores automatic sizing or changes equipment purchase choices from demand.
