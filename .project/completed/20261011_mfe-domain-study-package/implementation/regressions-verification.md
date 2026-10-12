# T-036 current regression migration verification

Implementation verification passed; independent audit is pending. Native basis is `3d9711e2`; the T-036 scope is recorded at `42008bf8`. The separate T-035 oracle return remains `c6c04d32` and `1176eabf`.

The coherent model suite returned **566 passed, 13 skipped, zero failures/errors**. All thirteen skip identities match the entering native baseline. The recorded 79 warnings concern existing `record_property` use with JUnit's xunit2 format in financial tests; those tests were not changed. `regressions-final-attribution.json` maps all **63 new** candidate failure/error nodes and the **one inherited** stale-receipt failure to current passing identities. Five component tests were renamed to state the corrected behavior; their original names remain in the mapping. No failure was dismissed as inherited after first appearing in the candidate.

## Changes and checks

- Fresh current heating and model-family generation uses WI-053's ten checked manual seeds. Historical scenario definitions and the original eight-seed helper are preserved. Live and snapshot generation equality, exact entry censuses and mutation-consumer checks pass.
- Radius drivers are copied to pytest temporary directories. Exact-once substitutions retain historical numerical and structured expectations, six independent radius ratios, fixed anchors and the bounded WI-052 financial tolerance channel set. The valid field control remains equal to its frozen value. Original negative/equality and invalid reference geometry now require ValueError with the correct live/reference clearance message.
- Native and both direct public callers retain retired-input rejection. Coil-centre equality, R=3 and negative R now require the deliberate live-clearance diagnostic. R=4 remains the preexisting sustainment error; zero R retains its earlier upstream division error. Those unrelated domains are not claimed repaired.
- Source preservation checks compare all bytes outside the two authorized calculation definitions to entering sources and retain exact canonical/twin equality. Original source/snapshot generation receipts remain checked. The current package hash check now uses the immutable WI-053 candidate receipt, resolving the already failing WI-052-era comparison without rewriting either receipt.

## Commands and attempts

All invocations used `.codex-test/run`; no environment install or synchronization occurred. The standalone native test requires the sealed simkit source on the import path. The successful invocation prefix was `.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; exec .codex-test/run python -m pytest ...'`.

1. Affected modules: `tests/models/test_mfe_major_radius.py tests/models/test_mfe_operating_heating.py tests/models/test_model_family_spines.py -q --tb=short --junitxml=.project/active/mfe-domain-study-package/implementation/regressions-affected.xml`. Initial result: 38 passed, 47 radius setup errors and one missing-simkit invocation failure. The setup errors were one temporary driver expecting the old negative-R TypeError. They led to the specific ValueError correction. Raw results are retained.
2. Radius retry using the successful prefix: `tests/models/test_mfe_major_radius.py -q --tb=short --junitxml=.project/active/mfe-domain-study-package/implementation/regressions-radius-retry.xml`. Result: 64 passed. The inherited receipt check was also diagnosed independently with a single passing invocation; it was not the missing-simkit failure.
3. Coherent suite using the successful prefix: `tests/models -q --tb=short --junitxml=.project/active/mfe-domain-study-package/implementation/regressions-models-final.xml`. Result: 566 passed, 13 inherited skips. This includes explicit clearance-message checks on the native and direct failure paths.
4. `.codex-test/run python .project/active/mfe-domain-study-package/implementation/attribute_regressions.py` joins immutable native attribution with final JUnit identities. Result: 63 new and one inherited failure resolved; no remaining failure/error.

The matching `.txt` and `.xml` files retain each attempt. `git diff --check` passes for the owned changes. This report records implementation evidence, not independent certification, integration or pin promotion.
