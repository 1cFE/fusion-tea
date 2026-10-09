# Owner closure and archive handoff — 2026-10-06

[OWNER-VERBATIM] “ok formally close the goal and items. and commit all. then run $my-pre-pr”. [AGENT] Closure accepts the already reviewed conditional answers; it does not qualify a physical plant or launch follow-up modeling. Authority and timestamp are recorded in [the trail](../../trail.md#goal-closure--2026-10-06).

## Native archives

| Item | Current evidence home | Acceptance |
|---|---|---|
| WI-096 | [Matched conversion subsystems](../../../../../completed/20261006_WI-096_matched-conversion-subsystems/spec.md) | Repaired 498-case study and independent conditional economic/seal review. |
| WI-097 | [Exchanger thermal requirements](../../../../../completed/20261006_WI-097_exchanger-thermal-requirements/spec.md) | 1,277 exact maps, independent review and complete fresh replay. |
| WI-098 | [Whole-plant conversion comparison](../../../../../completed/20261006_WI-098_whole-plant-conversion-comparison/report.md) | 2,496-case catalog and independent final boundary/ranking review. |
| WI-099 | [Matched-duty conductor alternatives](../../../../../completed/20261006_WI-099_magnet-conductor-alternatives/spec.md) | Round 1's independent model/oracle and final interpretation checks. |
| WI-100 | [Plant material variants](../../../../../completed/20261006_WI-100_stellarator-material-variants/spec.md) | Round 2's sealed numerical evidence and independent integration/interpretation assurance. |

[AGENT] Existing independent acceptance scope is indexed in [the tracking audit](../pr-readiness/tracking-audit.md). Original stage documents and narratives may still describe owner closure as pending at their dated cutoffs. The table above and native completed statuses are current. [Archive preservation receipt](archive-preservation.json): all 38,554 previously tracked item files moved; 38,542 retain exact bytes and twelve receive only PM metadata/frontmatter changes. Ignored working stores moved locally without becoming newly tracked. The current registry is updated solely by native PM operations.

## Read and replay archived evidence

[AGENT] Historical snapshots retain their original path/commit provenance. Sealed oracles also read specific evidence through old active-item paths. Rewriting those sources would change the study's recorded oracle identity. [archived_work.py](../../../../../../scripts/archived_work.py) instead provides explicit, temporary filesystem aliases during read/test/replay commands; aliases are removed when the command exits. It refuses collisions and ambiguous archive locations and serializes simultaneous readers. There are no permanent active-item stubs. Use this adapter for readers; builders that write through those paths are outside its contract. Do not nest adapters.

With the configured runtime and the environment setup from [reproducibility.md](../pr-readiness/reproducibility.md):

```bash
uv run --no-sync python -m scripts.archived_work -- uv run --no-sync python work/orchestration/goals/magnet-material-comparison/evidence/pr-readiness/portable_smoke.py
uv run --no-sync python -m scripts.archived_work -- uv run --no-sync python work/orchestration/goals/magnet-material-comparison/evidence/pr-readiness/check_reproducibility.py
uv run --no-sync python -m scripts.archived_work -- uv run --no-sync python -m pytest
```

[AGENT] The portable smoke command still uses only its tracked fixture. The complete seal check requires original machine-local artifacts; the archive operation preserves their bytes and moves the item-owned ones. Neither command is a full fresh-study replay. Adapter unit tests cover cleanup, repeated use, collisions, actor replacement and child-exit propagation. [Independent review](../pr-readiness/independent-review.md) records the adapter's filesystem scope separately from scientific qualification.
