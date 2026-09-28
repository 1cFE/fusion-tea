# WI-049 implementation validation

[AGENT] Production implementation is delivered for fresh independent audit. All required IFE acceptance checks pass. This report records implementation evidence; it does not certify the work item or accept inherited residuals.

## Executed environment and identity

Every Python and model command ran through `.codex-test/run`, using the existing sealed runtime and license configuration described in `.project/codex-test-setup.md`. Execution tests used `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/models/ tests/test_ife_consumer_eligibility.py -v'`. No required IFE test can silently skip missing TEAx in this environment.

The native package is `exploration/ife_e2e/generated`, package name `ife_tea`. Its semantic fingerprint is `8596c899df17f763bbce6eb50a18c1b5bca83080c40233e40bc01a7bb1aa1888`; executable fingerprint is `2810897c4ef9db8cb646aec5616884de42963c41e3b92ac20c2947450ffcbfd7`. Native generation uses the installed `GenerationConfig` and `run_codegen`. `native-regeneration.json` records all 55 file digests, both typed signatures and actual loader/evaluation results after preservation and preservation-plus-smart regeneration. All file bytes match under both routes, excluding runtime caches. The separate factor completion returns operation then construction. Its two named outputs bind to required core inputs; the existing price completion remains typed and unchanged.

## Acceptance results

`final-tests.txt`: **376 passed, 13 skipped, zero failures**. The skips are inherited: one example test explicitly awaiting customization and twelve foundation tests targeting absent `models/library/foundation` files. Every WI-049 test executed. The new file contributes 280 tests; its sealed execution retains all 264 design cases, four positive neighbors, six signed-zero duration cases, two individual duration mutations, baseline preservation and both regeneration routes. The WI-048 regressions and current supported consumers pass.

`channel-results.json` independently measures the 268 numerical acceptance cases against 80-digit Decimal annual quantities. Integer durations use explicit dated payment sums; fractional durations use separately labeled difference-of-powers algebra. Every nonzero cost, energy, factor and eligible Hawker price passes relative error at most 1e-9; absolute tolerance is used only for true-zero reference channels. Maximum measured strict residual is **5.995204332975845e-15**. `measure_channels.py` reproduces this evidence against the shipped public evaluator without regenerating or running a study.

Every case asserts the exact named net-generation verdict and inherited viability verdict, both generating flags and both supported consumer paths (`price_eligible` and `require_price`). Non-generators return exact invalid zero prices while retaining finite cost and signed or zero energy. The four positive neighbors retain 2.5 W net power, satisfied net verdict, generating=1 and positive eligible prices. This catches price suppression as well as the original zero exception and separate-channel cancellation.

The ordinary 8% test compares all 30 inherited numerical names to immutable `entry-baseline/baseline_result.json`, asserts the two exact named verdicts and exactly two added factor outputs, and independently checks the existing full annual/physical oracle. Meier arithmetic, dollar bases, replacement charges, power balance, 31557600-second shot years and 8760-hour energy years remain unchanged. Native regeneration also refreshes generated documentation already corrected in WI-048 sources; those comment changes do not alter the inherited equations.

`integer-crosscheck.txt` records successful `.codex-test/run python scripts/verify_ife_lcoe.py`. Its historical module scenarios are explicitly labeled as separate from the computed Osiris point. Direct generated module callers now evaluate the native factors first; the consumer regression tests cover zero, ±1e-12 and 8%.

## Native model validation and attribution

`phase1-l1.txt` through `phase1-l3.txt` and the corresponding Phase 2 files all pass. Final `validation-after.txt` reports IFE Levels 1–5 passing: zero parser errors/warnings, zero structural issues, zero cycles, two admitted numerical constraints with 100% executable share and 30/30 documented elements. Canonical/twin equality passes through the family spine; the new definition stays in library analyses and the generic plant contains only Real values and usages.

IFE Level 6 remains FAIL with **50 issues**. The verbose CLI truncates detailed display after five issues even with `--verbose`, so the native `validate_architecture` structured results were retained separately before any production edit in `l6-before.json`, and after implementation in `l6-after.json`. `l6-attribution.json` gives all 50 numbered comparisons, each with rule, element, exact message and before/after file locations. Matching uses a multiset of `(file, element, rule, message)`, ignoring line-number movement only. Result: **50 retained, zero resolved, zero introduced**. `check_native.py` reproduces the comparison.

The retained categories are two dynamic design-expression references, fifteen unsupported-dot EXPOSE expressions, eighteen abstract design-attribute completeness findings and fifteen static extraction findings. The new factor definition and duration bindings introduce no L6 diagnostic. This retains the existing failed quality level; executable seals and passing numerical checks do not relabel it as a static validation pass. WI-048 `implementation-evidence.md` and its final issue inventory corroborate this inherited class and count.

`validation-wider.txt` reports whole-tree Levels 1, 3, 4 and 5 passing, Level 2 failing for **10 MFE placeholder bindings**, and Level 6 failing with **277 issues**. These match the inherited WI-048 final whole-tree findings. The MFE sources are untouched and the individually matched IFE issues account for the affected slice. No blanket whole-tree pass or unrelated MFE repair is claimed.

## Traceability and scoped disposition

The factor comment documents rate/duration units, dated integer streams, fractional algebra, stable evaluation and exact-zero limits. Source, Reference, Ref, Basis and Last Updated fields resolve to registered Hawker `output.md:141-148` and the accepted design derivation. Both duration defaults now carry source and unit comments. Three native trace operations add the factor and duration rows; the affected LCOE row was refined in the existing CSV schema. The native MR/duplicate limitations and exact caller migration are recorded in `migration.md`. Source interpretation is unchanged.

SV-076, SV-077 and SV-078 were changed to passing through native `pm update-validation` after the retained tests passed, and their Test cells point to the retained tests and this report. Historical certifications were preserved. `deferred-study-tests.txt` records **10 failed, 7 passed** in the separately scoped stale study route. Its channel metadata, old package pin, old duration-validation suffixes and immutable context snapshots remain for the following package task as detailed in `migration.md`.

## Requirement handoff

| Requirement | Evidence for fresh audit |
|---|---|
| MR-WI049-1 | Decimal dated integer streams and exact-zero finite limits in SV-076; separate cost/energy assertions. |
| MR-WI049-2 | All 268 shipped cases with strict independent channel tolerances; retained residuals and rejection test for cancellation/absolute-floor masking. |
| MR-WI049-3 | Real source/input contracts, fractional algebra across six duration pairs, signed zero and individual duration mutations; no production input bounds added. |
| MR-WI049-4 | Exact net verdicts, flags, sentinels and both supported eligibility consumers at all required cases, including four positive neighbors. |
| MR-WI049-5 | All thirty inherited baseline outputs and both verdicts; independent full source oracle; unchanged Meier/physical/annual expressions. |
| MR-WI049-6 | Native/temporary sealed execution and both byte-stable preservation routes; 376 passing regressions; IFE L1–3 passing and individual L6 attribution. Positive fresh audit remains pending with the parent. |
| MR-WI049-7 | Completed model citations and direct trace rows; no source reinterpretation. |

[AGENT] No semantic or shared-tool prerequisite blocked this implementation. Representability at extreme IEEE inputs remains the design's documented limitation, not a new supported-domain policy. The next action is the parent's fresh independent audit into `audit.md`. Close/archive, study refresh or execution, financial normalization, source rulings, MFE changes and package pin promotion were not performed.
