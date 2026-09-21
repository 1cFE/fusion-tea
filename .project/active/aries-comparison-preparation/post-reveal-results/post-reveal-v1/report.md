# Post-reveal ARIES comparison: conductor-domain refusal

The repaired model did not complete the authorized comparison. Its conductor-current calculation received a peak field of **56.61785714285713 T at 20 K**, outside the selected conductor approximation's **20–32 T** domain. The retained native state is `execution_failed`, and the adapter exited 1. **LCOE is unavailable.** No completed power, component-cost or engineering-predicate results were returned. This establishes an evaluation limit for this supplied design and request; it does not establish that a physical plant is impossible.

## Design and request

The single [committed request](request.json) supplies nominal major radius 7.75 m, minor radius 1.70 m and peak ion temperature 11.83 keV. The other 701 public inputs remain the adopted repaired design, including density/profile assumptions, 308 installed reference-coil turns, 50000 A per turn, coil geometry, conductor product, equipment capacities, inventory, prices and finance. The full [held-input inventory](input-evidence/held-input-inventory.json), [input decisions](input-evidence/decisions.md) and [independent input review](review/input-review.md) identify their evidence and consequences.

The three source scalars do not transfer ARIES plasma shape, volume, profiles, coil families, cooling cycle or installed equipment. Aggregate ampere-turns did not choose turns or per-turn current; average density did not substitute for peak density; winding dimensions did not substitute for coil exterior or clear cavity dimensions. Source revisions, the 18-versus-24-coil conflict and unresolved equipment correspondence remain recorded. This is a post-reveal evaluation of the held supplied design under selected reference inputs, not a reconstruction of the reference plant or the original experiment.

## Retained execution and engineering evidence

[This post-reveal attempt](attempts/first-forward/result.json) identifies `stellarator_09__stellaris__magnet__conductor_current` as the failing module. Its recorded cause is `ValueError: REBCO Conductor Current: B_peak outside 20..32 T; actual=56.61785714285713 T at 20.0 K`. The adopted implementation is `exploration/stellarator_e2e/generated/handwritten/mfe_conductor_current/rebco_conductor_current_impl.py:32` inside the archive. The reported field is a diagnostic from that exception, not a published complete model output.

The native result contains zero outputs, zero verdicts and no retained partial artifacts. All 67 expected engineering predicates are **unevaluated**. No engineering-predicate violation was established by this attempt. The six violations observed in the separate synthetic restoration baseline do not belong to this reference request. No downstream values were reconstructed from partial calculations, defaults or that baseline.

The [first-attempt pointer](attempts/first-attempt.json), [raw request](attempts/first-forward/request.raw.json), [effective selection](attempts/first-forward/selection.json), [native record](attempts/first-forward/native-case.json), native database, [export](attempts/first-forward/model-export.json) and [receipt](attempts/first-forward/receipt.json) retain the attempt. The preparation, reviewed request and execution were committed separately before reporting. There was one reference invocation and no changed-input retry.

## Source comparison

All 276 historical rows are retained in [observations](observations.json). All model values remain unavailable and all model-validity flags are false. The worksheet contains 52 contextual source numbers with page/table/definition evidence; other numerical reference fields remain unavailable. [Source decisions](source-decisions.md) and the [source evidence index](source-evidence/index.json) preserve source bytes, hashes, uncertainty gaps, technology differences and scope conflicts. A populated reference field is not proof of a matched quantity.

No model/reference ratio, numerical agreement, disagreement, supported whole-plant prediction or overall comparison pass can be established. Broad structural counterparts provide qualitative context; exact radial architecture and account correspondence remain unresolved. Supplied values, held aliases, capacities and purchase prices earn no independent prediction credit.

The unchanged inclusive bands remain [1/3, 3] for derived quantities and [0.5, 2] for component costs; LCOE has no formal band. Disjoint account aggregation, C220107 disclosures and exclusions, actual source account labels, raw money years and permitted unit/accounting conversions remain in the report. Missing cost scope is never zero. There is no manufactured common currency year. The published reference LCOE is context only; there is no model LCOE to compare.

The [machine report](reports/first-forward/report.json) completed with all 276 comparison rows blocked, all ratios unavailable and no independent prediction credit. Every account reconciliation is blocked, and the constraint inventory is incomplete because the attempt returned no verdicts. The [independent source/observation review](review/observation-review.md) accepts this interpretation. The [independent replay review](review/replay-review.md) reproduced the export byte for byte and matched the entire scientific report, with only the separate report-attempt name and pointer digest differing. All 14 account checks remain blocked. See the [replay receipt](review/replay-receipt.json).

## Scientific limits and unresolved questions

The refusal leaves the following adopted limits unresolved: fixed breeding-geometry support; the selected conductor product's 20 K and field applicability; equipment point ratings without qualified off-design maps; coupled steam-cycle and heat-exchanger endpoints; incomplete joint plasma and cost-correlation support; hypothetical equipment offers; mixed-year costs; and structural qualification. Completed arithmetic, if achieved by some future authorized evaluation, would not by itself resolve them. Conditional LCOE would not demonstrate a feasible plant price or a complete uncertainty estimate.

Identity verification establishes the archived bytes within its indexed scope. The documented file-read checks do not certify native C/SQLite reads, direct syscalls, environment/network access, pre-opened handles, all installed dependencies or unexecuted branches. Software restoration passed nine focused checks and a separate synthetic baseline; that evidence does not expand a scientific domain.

No alternate input point, resized equipment, revised conductor model or extended domain was evaluated. **Any further physical execution requires a separate owner decision.** Reporting and export replay may use this retained attempt without another physical evaluation. No unrelated goal is closed, and nothing was pushed, merged or published externally.

## Identities and replay

The adopted archive SHA256 is `d65d6ea44517dba3d9012d06706e74fe3006247e2809f6b4bdd64edd85ab5a7a`; executable fingerprint `83ea3b6cf99f5fda6045e7e03b5d430ede91abbe8aa41262c2f9f5aba8663d23`; request SHA256 `d5cdb3751ceb00ed52851ce5f232ada5f0f2dbf1b97adf9157d5dfb530a05560`. [Runtime identities](receipts/external-runtime.json), native runtime hashes, [checkpoint index](checkpoints.md), [journal](journal.md) and [replay instructions](replay.md) identify the retained evidence and prerequisites.

The original failed r3 experiment remains at commit `829539f5eb7fde217d18318d1646a5e47103812c` on `evidence/aries-r3-comparison-20260920`. This result register is `/home/reid/1cfe/fusion-tea/.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1`.
