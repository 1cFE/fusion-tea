# Round 1 source-image check

Checked 2026-09-10 by the parent round agent. This is supporting evidence for T-001, not a new source registration or independent item audit. Citation guidance: `source-traceability`; project MR-4 governs the path-based citation format.

## Source

`knowledge/sources/energy_from_inertial_fusion/output.md@a9ec0b76e2a3c6bb05bc27667f22c47c78c93909`, operating-parameters table, Osiris column; accompanying image `knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png` (local ignored image; unpinned, no native digest for this image). The image was visually inspected in the primary checkout; the worktree also has the local image available for stage/audit verification.

## Printed values

| Quantity | Osiris column |
|---|---:|
| Driver energy | 5.0 MJ |
| Gain | 87 |
| Yield | 432 MJ |
| Pulse rate | 4.6 Hz |
| Driver efficiency | 28% |
| Fusion power | 1987 MW |
| Thermal power | 2504 MW |
| Thermal efficiency | 45% |
| Gross electric power | 1127 MW |
| Driver power | 82 MW |
| Auxiliary power | 45 MW |
| Net electric power | 1000 MW |
| Cost of electricity | 5.6 (1992 cents/kWh) |

## Interpretation for the item

[AGENT] The printed table supports F01. Source facts must retain their printed values. Gain 87 and yield 432 MJ are rounded reported quantities: 432 / 5 = 86.4. An executable chain must state which input governs its computed yield rather than calling both exact.

[AGENT] The historical power columns are internally consistent to their printed precision: 432 × 4.6 = 1987.2 MW fusion; 2504 × 0.45 = 1126.8 MW gross; 5 / 0.28 × 4.6 = 82.142857 MW driver draw; 1127 − 82 − 45 = 1000 MW net. These are arithmetic checks, not an independent reconstruction of the source's plant model.

[AGENT] The current Hawker chain uses blanket multiplication 1.15 and cooling consumption equal to driver consumption. Those are not the same as this historical table's thermal and auxiliary assumptions. Correcting the input transcription therefore does not warrant forcing the Hawker result to 1000 MW. The design must give historical reference facts and the computed operating case explicit identities.
