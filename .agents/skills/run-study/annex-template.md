# Package annex — `<package name>`

Package fact, not rule. The run-study runbook cites a section here at each step that needs something only true of this package. Nothing in this file is an instruction, and nothing in it is inlined into the runbook.

Copy this file to `<studies-dir>/ANNEX.md`, in the package's studies directory, and replace every `<...>`. Keep the four `§` headings exactly as written: the runbook cites them by name. A section with nothing to say states its nil, in the record template's explicit-nil sense.

---

## Package-owned pieces

What this package supplies that no runbook step can. The runbook's § What a package annex supplies says what each piece must do.

| Piece | Where it is |
|---|---|
| Package | `<package root, project-relative>` |
| Manifest | `<studies-dir>/manifest.json` |
| Axis declaration | `<axis declaration, project-relative>` |
| Route | `<route module>`: `execute_baseline`, and `<the callable that runs the study's points>`. It is one of the routes the study policy's § Execution routes names. |
| Oracle | `<oracle module>.<callable>` and its `operand_bindings()`, as the manifest's `oracle` block names them |
| Snapshot | `<the one *.snapshot.json beside the models root>` |
| Census | `<the tracked entry-point census>` |

**The snapshot rule.** `sysml-codegen study integrate` recaptures the snapshot at its gate 4, so it needs exactly one `*.snapshot.json` beside the models root, in the models root's parent directory. sysml-codegen's usual snapshot name, `instance_graph_snapshot.json`, does not match that pattern: name the tracked snapshot `<name>.snapshot.json`.

---

## § Declared ties

Read at runbook step 2. A tie is declared, never derived.

`<every tie: the entry keys that are one physical quantity, the identity claimed, and who declared it on what grounds — or: no ties; every axis key fans out from one attribute>`

---

## § Baseline pin

Read at runbook steps 5 and 6. Preflight's baseline gate checks that the route reproduces this headline.

`<the baseline point, its headline channel and value, and its expected verdicts, as the manifest's baseline block carries them; where each value came from; and what the baseline does and does not establish about the design>`

---

## § Oracle

Read at runbook steps 7 and 10. The oracle is independent of the generated package: agreement between the two means something only because neither was derived from the other.

`<what the oracle computes and from what source; which channels and constraints it covers and which it does not; how operand_bindings() maps each constraint operand to an input or a channel; and any input it refuses>`

---

## § Validity masks

Read at runbook step 7. A mask is a derived bound from held-fixed inputs, never a design screen.

`<each bound applied to a candidate range, stated as its derivation from held-fixed inputs, itemized so that a moved input moves the bound — or: none>`
