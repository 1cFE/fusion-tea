# Consumer validation results

[AGENT] The current oracle and metadata migration implement SC-1–5 against corrected production `708dddefdbeb5f990d9ef824ce06258fa6b46345`. This is implementation evidence for the fresh auditor, not a certification verdict. Implementation commit: `cb11b3bd`; the later evidence commit also carries additional direct tests and current annex corrections.

## Arithmetic and route

- `finance-tests.xml`: 118 passed, including the first 117 direct checks and one 30-case route test. The retained route evidence is `finance-route-evidence.json`.
- `direct-finance-final.xml`: 169 passed, one route test deselected. This replaces the initial direct-test count and adds independently derived yearly energy, restart/held clipping boundaries and fractional near-equality cases. The unchanged route test already passed separately; there are 170 distinct tests in the final module.
- The route executed 30 proposals: live and held modes, each at ordinary 0.07, exact 0.02 equality with the existing fixed inflation input, 0.02 ± 1e-12, exact zero, and both signs of 1e-4, 1e-8, 1e-12, 1e-16 and 1e-18. All completed. The worst relative deviation over all seven already-mapped finance outputs was `3.2815407520306707e-15`. Tiny nonzero quantities used relative comparisons without an absolute floor; true-zero handling used 1e-9 absolute tolerance.
- Every case retained all 158 published scalars. All 145 nonfinance scalars and all eighteen authored verdicts were exactly equal to the same-mode ordinary native control. These rate tests do not establish feasibility; the baseline divertor violation remains.
- Direct references use 100-digit inverse dated unit-payment sums for CRF, dated growing payments for integer annuities, dated construction spending for integer IDC, a generalized binomial series for fractional IDC, equal-rate PV and logarithmic continuations for fractional annuities, dated replacement sums, and full-year production minus outage overlap for energy. The oracle uses independent 80-digit retained equations. Zero/equal limits, tiny signed rates, fractional operating/construction duration, one-year neighbors, zero replacement events and event-boundary semantics pass.

## Coverage and radius controls

The adapter files remain byte-identical to the corrected starting revision. Before and after counts are 246 native inputs, 99 mapped inputs and 147 refused omissions; 158 native outputs, 141 mapped outputs and seventeen omissions. `finance-route-evidence.json` records the complete maps and omission lists. Seven mapped finance outputs are reported IDC, calendar replacement PV/annual cost/energy ratio, comparison capital charge and both LCOEs. Six finance outputs remain omitted from the adapter: both public CRFs, CAS71/CAS80 levelized costs and both CAS70 aggregates. Their prior native independent financial checks remain evidence, not newly claimed adapter coverage.

`radius-controls.json` retains the two current executions and every mapped independent comparison against the immutable WI-051 controls. All thirteen finance channels differ from frozen values by ordinary roundoff at both baseline and R14. No other channel differs. The new caller checks all 145 nonfinance channels exactly, including R14, and allows only those thirteen finance channels 1e-9 relative tolerance with no absolute floor. The thirteen-channel set follows the retained native dependency/scalar ledger; its six unmapped channels are independently substantiated in WI-052 native audit evidence. No historical helper or frozen number changed.

## Metadata and preservation

Two fresh producer invocations wrote `/tmp/wi052-consumer-metadata-a` and `-b`. `metadata-reproduction.json` records their output hashes and equality checks. Manifests and every graph fixture are byte-identical; reports differ only in the path of the isolated manifest they read. All graph fixtures also match the repository, so none changed. The initial invocation lacked the sealed simkit source path and stopped before native execution; the new preparation script now adds that existing runtime path explicitly. No dependency was installed.

Only current manifest provenance and its native headline value changed. The indicator-input digest remains `609e6cca0a4f329e834b52369a425541ca167bfdfe8608879d900a27ccedf06d`; semantic fingerprint remains `15ed665c374729a984f29fa753f444677805939ffb195933419b3489debbd47e`; executable fingerprint is `1a7c216dabff8425c279f6b3c2781629115729173fc0b406600497ac348b4340`. Headline changes from 224.26923288439 to 224.26923288439002, relative `1.267e-16`. Baseline physical inputs and eighteen verdicts, declared ties and objective meanings are unchanged. The fixture preparations and disposable integration tests do not promote a production candidate or historical study pin.

`preservation.json` compares explicit protected Git paths against the frozen revision. No canonical model, family model, generated package, model snapshot, model test, native WI-052 record, WI-051 record, historical radius coding item, shared producer, input adapter or route changed. The package-contract and snapshot SHA256 values match the documentation repair. The only pre-existing tracked worktree change is setup `.gitignore`, which is excluded from this item's commits. No preservation walker or quarantine inspection was used.

## Focused existing acceptance

- `focused-tests.xml`: 203 passed across the complete current radius, known-answer, stock-route and preflight-negative files. This includes all 147 unmapped-input refusals and existing retired-radius refusals.
- `existing-calendar-tests.xml`: 15 passed against the existing live/held native calendar caller tests, with no skip.
- `affected-nodes.xml`: all 22 exact nodes passed in 517.29 seconds. `affected-differential.json` matches each original failure identity to its passing result. The command is retained in `affected-command.json`.

The native implementation's 108 known historical failures remain historical evidence. They were not rerun merely to recount them. No additional unresolved failure occurred in these focused runs.

## Commands

All commands ran from `/tmp/fusion-mfe-financial-rate-limits` using its `.codex-test/run`; integration test subprocesses inherit the sealed interpreter and runtime. The implementation directory contains JUnit and text results for these commands:

```text
.codex-test/run python .project/active/mfe-financial-study-package/implementation/refresh_metadata.py /tmp/wi052-consumer-metadata-a
.codex-test/run python .project/active/mfe-financial-study-package/implementation/refresh_metadata.py /tmp/wi052-consumer-metadata-b
.codex-test/run python -m pytest tests/study/test_financial_consumers.py -q --basetemp=/tmp/wi052-current-finance-tests --junitxml=.project/active/mfe-financial-study-package/implementation/finance-tests.xml
.codex-test/run python -m pytest tests/study/test_financial_consumers.py -q -k 'not current_rate_route' --junitxml=.project/active/mfe-financial-study-package/implementation/direct-finance-final.xml
.codex-test/run python -m pytest tests/study/test_major_radius.py tests/study/test_known_answers.py tests/study/test_stock_route.py tests/study/test_preflight_negatives.py -q --basetemp=/tmp/wi052-consumer-focused --junitxml=.project/active/mfe-financial-study-package/implementation/focused-tests.xml
.codex-test/run python -m pytest tests/models/test_lifecycle_calendar.py -q --junitxml=.project/active/mfe-financial-study-package/implementation/existing-calendar-tests.xml
```

The exact affected-node command is the argument array in `affected-command.json`, produced directly from the native `new-downstream-failures.json` node list. `git diff --check` passed.

[INHERITED] Broader model/engineering and financial-domain limitations, source authority, parked construction-duration zero, native checker limitations and oracle omissions retain their existing status. No source adoption, residual acceptance, model change, source research, historical study execution, archive, merge, push or goal close occurred. Fresh independent coding/native completion review remains required.
