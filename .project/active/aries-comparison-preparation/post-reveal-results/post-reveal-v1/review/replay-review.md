# Independent retained-evidence and replay review

[AGENT] **PASS for retained execution custody and reporting replay.** I did not author the execution, source worksheet or comparison report. I restored the adopted archive into a new directory, verified its identity, reproduced the export and replayed the archived reporter against the original attempt. No physical evaluation was performed by this review. This verdict establishes replayability of the retained failed result, not scientific feasibility or numerical agreement.

## Verified custody

The archive SHA256 is `d65d6ea44517dba3d9012d06706e74fe3006247e2809f6b4bdd64edd85ab5a7a`. All 588 archive members and 587 pinned files match the adoption. The retained identity SHA256 is `a63cf7ae1d497f0f74375ebcbf693f26d8cd1a9cc8c2c3c7d9407f64f8765dff`. Every original attempt receipt entry matches its retained bytes, including the database and SQLite sidecars. The first-attempt pointer matches the terminal record and receipt. The adopted request digest matches both the committed request and retained raw request.

Recomputing selection from the archived defaults and request reproduces all 704 effective inputs and their roles: three supplied and 701 held. Only `first-forward` exists in the operating attempt store. Inspection of an immutable database copy finds one proposal, one native case, and one attempt with transitions `started` then `execution_failed`. Its recorded failure is the conductor-current domain exception at 56.61785714285713 T and 20 K. No retained outputs, verdicts or partial artifacts exist. The required predicate inventory has 67 entries; none has a returned verdict. Original database and sidecar hashes remain unchanged after inspection and reporting.

## Reproduction and report review

The archived pure export reproduces the original export byte for byte. All 276 rows have `execution_not_completed`, and no model value is available. The archived reporter accepts the independently reviewed observation bytes, whose SHA256 is `e4305c2dafef62f5e0d0151dd11eb3c82b3d530ba50fe108632b5c9fd30a958e`. The original report receipt was verified before replay. Replay is retained in [the separate verification store](../replay-verification/reports/independent-replay/report.json).

The entire numerical-comparison object matches exactly, including all 276 rows, ratios, statuses, accounting, constraints, roles, raw observations, source notes and scientific qualification. All 276 rows are blocked; every ratio is null and every independent prediction credit is false. All 14 account checks are blocked. Current predicates are empty and incomplete. Input/attempt evidence identities, selection qualifications, original result digest and observation digest match exactly. LCOE has no available model prediction. These facts support the failure interpretation and claim boundaries in [the narrative report](../report.md).

The reports are not globally byte-identical. The sole differing field is `first_report_attempt`: the original reserves `first-forward`, while this separate verification store reserves `independent-replay`, with a different pointer digest. The original attempt path is unchanged because both reports read the same retained attempt. The temporary restored-root path differs from the executor's restore path but does not enter scientific report content. Exact differences and original/replay digests are recorded in [the receipt](replay-receipt.json).

## Durable replay evidence and prerequisites

[Archive/export verification](replay-tools/verify.py) and [report replay](replay-tools/report_replay.py) record the exact operations. They use `/home/reid/1cfe/fusion-tea/.venv/bin/python`, the documented sealed-interpreter exception. Invoke the verification script first, then the reporting script. The reporting script reserves an exclusive verification attempt; on a later replay, choose a new verification store/name instead of deleting this review's retained pointer or report. The scripts never call the numerical execution route. The archive and original retained attempt are sufficient inputs to their computation; the reproduction receipt retains the restored location used in this review.

Pure export/report replay here uses the Python standard library and does not invoke licensed model tooling. A new physical run would additionally need the external Python 3.12 environment, installed sealed dependencies and SysIDE/license access described by the archived reproduction instructions and [external runtime identities](../receipts/external-runtime.json). The archive bundles model/runtime source and sealed wheels, not the full installed environment or credentials. It is not a portable environment installer. No secrets are copied into review evidence.

[The reproduced export](../replay-verification/model-export.json), [database inspection](../replay-verification/database-inspection.json), database copy, replayed report/receipt, [verification receipt](replay-receipt.json) and these scripts are retained inside the sole operating register. Temporary extraction is replaceable from the hashed archive; it is not the only retained evidence. Hash verification provides scoped local tamper evidence, not filesystem immutability or universal file-read assurance.

## Disposition

No blocking custody or replay findings remain. The narrative correctly separates the conductor-domain failure from an engineering-predicate violation, preserves the post-reveal designation and original experiment, and withholds LCOE and overall feasibility. Independent source interpretation is covered by the separate observation review; this review verifies its exact binding and reproducibility. Any further physical evaluation requires a separate owner decision.

## Exact review commands

These commands were run from `/home/reid/1cfe/fusion-tea`. The first verification invocation exposed a reviewer-script assertion that omitted the retained `requested_overrides` selection field; the script was corrected to compare `selection | {'requested_overrides': point}` and then passed. This was a review-script correction, not a change to the adopted package, request, attempt or report.

```bash
/home/reid/1cfe/fusion-tea/.venv/bin/python .project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1/review/replay-tools/verify.py
/home/reid/1cfe/fusion-tea/.venv/bin/python .project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1/review/replay-tools/report_replay.py
```

These are exact local command receipts. The scripts hardcode this checkout/register and the reserved replay name, so they are not portable launchers. On another checkout, adjust root/register paths and reserve a new replay store/name; use the generic archived CLI instructions in [replay.md](../replay.md). Do not overwrite this completed verification record when repeating verification.
