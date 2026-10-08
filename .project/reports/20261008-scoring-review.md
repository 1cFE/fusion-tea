# Independent scoring repair review — 2026-10-08

[INHERITED: 20261008-scoring-repair.md] Review the 44-failure scoring repair against entering commit `998a67e98`. This reviewer owns only this report and authors none of the test repairs. [OWNER] The explorer API must remain unchanged. Owner-edited `CLAUDE.md` and Concept Explorer README §9, production formulas, weights, feature data, published JSON and deployment files are protected.

## Final verdict

**PASS for the owner-authorized scoring repair and retirement scope.** The final full scoring suite has 357 passes and 41 pre-existing skips, with no failures or errors. All 44 original failure identities are accounted for: 42 pass unchanged and two are owner-retired. The retired failures are not counted as passes. Current arithmetic, normalization properties and explorer compatibility remain tested. API, published data, formulas, weights and owner-authored parallel work are preserved.

## Stage calibration and independent properties

[AGENT] June 13 commit `298b7cc54` introduced corpus normalization as a separate pass after raw formula evaluation. Upper-CF formula predictions still calibrate the raw stage. The repaired conformance fixture compares those fixed predictions to raw evaluation on the same temporary inputs as the CLI output. It separately checks normalized output range, mean, variance, monotone order, equality within exact raw tiers and a real distinction from raw scores. These properties constrain the transformation independently of its implementation.

[AGENT] All normalization mean, variance and range assertions now read freshly scored temporary CSV values. The tier test evaluates raw scores from the same inputs as that fresh execution. Exact raw ties must produce equal normalized values; ordering must remain monotone; absent raw values must remain absent. All forty concept IDs must be present, and each normalized axis must actually contain a repeated tier. The unchanged framework determinism test requires repeated full scoring executions to produce identical CSV bytes. These checks constrain the current normalization behavior without comparing against stale published snapshots.

## Isolated build review

[AGENT] The builder's absolute score, feature, taxonomy and weight input paths remain the shipped paths. Tests override only its output directory and the root used to display written paths, then execute its unchanged main function. Exact field/axis checks remain. Expected IDs are the retained forty scored IDs minus the three explicitly listed UI exclusions, yielding thirty-eight included IDs. The surviving Inertia concept is required. No builder code, input data or published JSON is changed.

## Modularity and cost review

[AGENT] Seven numeric raw cases exercise current production scoring. MagLIF and NearStar compare current execution with independent two-slot arithmetic derived from declared ratings and source account amounts. MagLIF uses energy-delivery `365.7` and containment `267.3`, driver rating `4.5` and chamber rating `2.5`. NearStar uses chamber rating `4` with zero parsed energy-delivery and the `4.1` CAS27 containment amount. Its narrative subaccount lines remain unparsed by the existing extractor; this test records that existing behavior. Source account and lookup-value assertions constrain the arithmetic. No reference score is copied from current output.

[AGENT] Active lookup coverage follows the documented two-slot IFE/MIF and three-slot MFE/nonstandard dispatch, including the chamber blanket penalty. Current raw score-band, nondegenerate-distribution and unit-count bracket assertions remain. The old drift bookkeeping and fixture-coverage guards are retired under the owner's disposition.

[AGENT] The cost test independently reads the explicit source account column and pins all seven classified bucket amounts. Coils are exactly `1070.0 / 3751.7` of classified dollars. It checks every resulting bucket share with the existing strict numerical comparison and keeps the vessel/blanket ordering and stellarator checks. The former above-one-half assertion did not match this source denominator. Neither classification nor production extraction changes.

## Calibration disposition

[OWNER] Accepted clearing out old useless tests after discussing the limited value of historical calibration: “yeah I do not mind clearing out old useless tests”. Source: [coordinator disposition](20261008-scoring-repair.md#calibration-disposition). [AGENT] Later committed capex inputs made the old normalized modularity reference stale. Retire its two whole-corpus comparisons, fixture coverage, old drift bookkeeping and forty obsolete conformance parameters. Retain current independent raw arithmetic, source-account and lookup checks, normalization properties and explorer compatibility. The prior historical-replay proposal is retired.

## Independent final receipt and preservation

This reviewer independently parsed `/tmp/20261008-scoring-suite.xml`: **357 passes and 41 skips**, with no failures, errors or expected failures. The full-suite command has no selection exclusions. The log reports 332.75 seconds. Every skipped node also appears as skipped in the prior conformance receipt; no new skip is introduced. The framework's full-scoring byte-determinism node passes.

The [final attribution receipt](20261008-scoring-attribution.json) matches the official October 7 inventory exactly: **42 unchanged original-node passes and two owner-authorized retirements**. The retired originals are `test_all_concepts_within_tolerance` and `test_corpus_mean_drift_under_threshold`, and both are absent from the final collected suite. Forty obsolete modularity conformance parameters and two other bookkeeping nodes are additionally listed as retired; all are absent from the final suite. Their removal matches the documented owner disposition. No original failure is hidden behind a skip.

The conformance prediction reader and comparison assertion remain unchanged. Parameter expansion explicitly retires the forty obsolete modularity predictions; other axes retain their fixed prediction values and existing tolerances. The fixed prediction YAML is unchanged. Raw evaluation and normalized invariant checks execute fresh temporary inputs and outputs. Build tests preserve retained production input paths, exact included concept IDs, shape, axis presence and independent composite arithmetic while writing only to temporary output directories.

This reviewer independently verified all fifteen captured scoring-test source hashes against final file bytes. All eighty-four protected hashes match, including owner-edited `CLAUDE.md`, Concept Explorer README §9, published JSON, parallel backlog and API-contract-gate spec/product-lens files. The attribution receipt's XML, log and protected-hash document digests and byte counts also match. Production scoring, explorer API, deployment, model and authority-source diffs contain only the preserved owner README edit. The explorer API and served data are unchanged. No production formula, weight, feature, ranking or reference fixture is changed. No dependency synchronization or protected-data write was performed by this reviewer. Final `git diff --check` passes.

This verdict qualifies the scoring test repair and owner-directed retirement only. It claims no fresh full-repository gate, regenerated public scores or deployment. Eight recorded comparison-candidate failures and repository-wide style policy remain outside the batch.

This reviewer independently verified the prepared thirteen-file index boundary. `CLAUDE.md`, the explorer README, parallel backlog and API-contract-gate files are excluded. The owner-authored current-work prefix remains exact in the working file and is excluded from the index. Indexed current-work bytes equal the working file after removing only that prefix; the sole added section is the scoring summary and all remaining HEAD bytes are exact. Staged scoring tests match final qualified source bytes. All eighty-four protected hashes still match, and the staged whitespace check passes. Restaging this final review report is the coordinator's only remaining review-record update before commit.
