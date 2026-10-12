# Independent audit commands

Run from the repository root. No installation or synchronization was performed. The named source files and immutable upstream artifacts were read directly; no broad code search required an explorer.

## Current consumer and negative paths

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/study/test_operand_bindings.py tests/study/test_known_answers.py tests/study/test_valid_empty.py tests/study/test_indicator_operands.py tests/study/test_verify_operands.py tests/study/test_annex.py tests/study/test_verify.py tests/study/test_stock_route.py tests/study/test_numeric_evidence.py tests/study/test_output_contract.py tests/study/test_preflight_gates.py -q -rs'
```

`current-tests.log`: 164 passed, one skipped in 197.58 s. The skip is the absent optional historical proof-of-life store in `test_a_store_bound_to_another_identity_is_refused`; required current TEAx execution ran.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/study/test_study_publication_fail_closed.py -q -k "not local_export"'
```

`current-publication-tests.log`: eight passed, 121 deselected in 0.53 s. This explicitly selects current-route publication; the unchanged local exporters remain covered by the implementation's disclosed broad result and source-identity inspection, not claimed passing here.

## Fresh stored controls

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python .project/active/mfe-operating-heating-study-package/implementation/check_controls.py /tmp/mfe-operating-package-audit-controls'
```

`controls.log`: three completed cases, all 18 predicates independently rederived, worst channel relative deviation `1.3031089676201858e-16`. This reruns the inspected author's runner through native APIs; the separate fresh test checks reserve/demand procurement, signed capacity and publication. Copied the resulting controls, identity and verification summary into this directory. Store remains temporary at the recorded path. `check.py` separately confirms exact control/identity agreement with implementation evidence and reproduction of manifest baseline headline/verdicts.

## Metadata, graph and preservation

```bash
.codex-test/run python .project/active/mfe-operating-heating-study-package/audit-evidence/check.py
```

`check.log`/`checks.json`: 642 preserved hashes, 12 unchanged historical source/test identities against `6cf3649e`, seven fixed-point metadata hashes, six byte-exact fixture rederivations and three exact heating graph groups. The script computes through native fingerprint and indicator APIs without rewriting production metadata. It was extended to include fresh-control/manifest checks after the control run, then rerun successfully.

Read `git diff 6cf3649e 676c7308 --name-only -- models exploration/stellarator_e2e scripts/study work/active/WI-050_mfe-coherent-operating-heating`: exactly the four authorized current study files. `git diff --name-only 676c7308 -- exploration/stellarator_e2e models scripts/study tests/study` is empty after this audit. The fresh lens command/provenance is retained separately. Existing implementation failed logs were not edited.
