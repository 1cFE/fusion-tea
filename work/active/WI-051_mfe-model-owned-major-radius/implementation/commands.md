# WI-051 executed commands and retained attempts

[AGENT] Commands ran from the test worktree. Every Python/model/PM execution used `.codex-test/run`; TEAx runs use the launcher-contained environment shown below. Read-only shell inspection used git/cat/rg/sed/tail/wc. Original evidence scripts were read and adapted, never executed into original write paths.

- `phase1-L1`: `.codex-test/run agentic-mbse validate /home/reid/1cfe/fusion-tea-codex-test/work/active/WI-051_mfe-model-owned-major-radius/implementation/models --level=1`; exit 0; [phase1-L1.log](phase1-L1.log).

- `phase1-L2`: `.codex-test/run agentic-mbse validate /home/reid/1cfe/fusion-tea-codex-test/work/active/WI-051_mfe-model-owned-major-radius/implementation/models --level=2`; exit 1; [phase1-L2.log](phase1-L2.log).

- `phase1-L3`: `.codex-test/run agentic-mbse validate /home/reid/1cfe/fusion-tea-codex-test/work/active/WI-051_mfe-model-owned-major-radius/implementation/models --level=3`; exit 0; [phase1-L3.log](phase1-L3.log).

- Entering capture: `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/prepare.py capture`; exit 0.
- Entering regression: `.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python -m pytest tests/models/ -v -ra --junitxml=work/active/WI-051_mfe-model-owned-major-radius/implementation/entering-tests.xml'`; exit 0; `entering-tests.log`.
- Apply: `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/prepare.py`; exit 0; `prepare.log`.
- Phase 1 focused tests: `.codex-test/run python -m pytest tests/models/test_mfe_major_radius.py -v -ra --junitxml=work/active/WI-051_mfe-model-owned-major-radius/implementation/phase1-tests.xml`; exit 0; `phase1-tests.log`.

- `phase2-L1`: `.codex-test/run agentic-mbse validate /home/reid/1cfe/fusion-tea-codex-test/work/active/WI-051_mfe-model-owned-major-radius/implementation/models --level=1`; exit 0; [phase2-L1.log](phase2-L1.log).

- `phase2-L2`: `.codex-test/run agentic-mbse validate /home/reid/1cfe/fusion-tea-codex-test/work/active/WI-051_mfe-model-owned-major-radius/implementation/models --level=2`; exit 1; [phase2-L2.log](phase2-L2.log).

- `phase2-L3`: `.codex-test/run agentic-mbse validate /home/reid/1cfe/fusion-tea-codex-test/work/active/WI-051_mfe-model-owned-major-radius/implementation/models --level=3`; exit 0; [phase2-L3.log](phase2-L3.log).

- `generate-attempt-1`: `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/regenerate.py`; exit 0; `generate-attempt-1.log`.

- `contract-checks`: `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/contract_checks.py`; exit 0; `contract-checks.log`.

- `promote`: `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/regenerate.py promote`; exit 0; `promote.log`.

- Phase 2 tests: launcher-contained TEAx environment; `python -m pytest tests/models/test_model_family_spines.py tests/models/test_mfe_major_radius.py -v -ra --junitxml=work/active/WI-051_mfe-model-owned-major-radius/implementation/phase2-tests.xml`; exit 0; `phase2-tests.log`.

- `phase3-L1`: `.codex-test/run agentic-mbse validate /home/reid/1cfe/fusion-tea-codex-test/work/active/WI-051_mfe-model-owned-major-radius/implementation/models --level=1`; exit 0; [phase3-L1.log](phase3-L1.log).

- `phase3-L2`: `.codex-test/run agentic-mbse validate /home/reid/1cfe/fusion-tea-codex-test/work/active/WI-051_mfe-model-owned-major-radius/implementation/models --level=2`; exit 1; [phase3-L2.log](phase3-L2.log).

- `phase3-L3`: `.codex-test/run agentic-mbse validate /home/reid/1cfe/fusion-tea-codex-test/work/active/WI-051_mfe-model-owned-major-radius/implementation/models --level=3`; exit 0; [phase3-L3.log](phase3-L3.log).

- `SV-083`: `.codex-test/run agentic-mbse pm update-validation SV-083 --status passing`; exit 0; [SV-083.log](SV-083.log).

- `SV-084`: `.codex-test/run agentic-mbse pm update-validation SV-084 --status passing`; exit 0; [SV-084.log](SV-084.log).

- `SV-085`: `.codex-test/run agentic-mbse pm update-validation SV-085 --status passing`; exit 0; [SV-085.log](SV-085.log).

- `SV-086`: `.codex-test/run agentic-mbse pm update-validation SV-086 --status passing`; exit 0; [SV-086.log](SV-086.log).

- `SV-087`: `.codex-test/run agentic-mbse pm update-validation SV-087 --status passing`; exit 0; [SV-087.log](SV-087.log).

- `SV-088`: `.codex-test/run agentic-mbse pm update-validation SV-088 --status passing`; exit 0; [SV-088.log](SV-088.log).

## Production execution and final checks

- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/run_acceptance.py` → exit 0; [acceptance-attempt-1.log](acceptance-attempt-1.log). Attempt-specific source copies and explanations are in validation.md.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/run_acceptance.py work/active/WI-051_mfe-model-owned-major-radius/implementation/acceptance-attempt-2` → exit 0; [acceptance-attempt-2.log](acceptance-attempt-2.log). Attempt-specific source copies and explanations are in validation.md.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/record_native.py` → exit 0; [record-native-attempt-1.log](record-native-attempt-1.log). Attempt-specific source copies and explanations are in validation.md.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/final_evidence.py` → exit 1; [final-evidence-attempt-1.log](final-evidence-attempt-1.log). Attempt-specific source copies and explanations are in validation.md.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/final_evidence.py` → exit 1; [final-evidence-attempt-2.log](final-evidence-attempt-2.log). Attempt-specific source copies and explanations are in validation.md.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/final_evidence.py` → exit 1; [final-evidence-attempt-3.log](final-evidence-attempt-3.log). Attempt-specific source copies and explanations are in validation.md.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/final_evidence.py` → exit 1; [final-evidence-attempt-4.log](final-evidence-attempt-4.log). Attempt-specific source copies and explanations are in validation.md.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/final_evidence.py` → exit 0; [final-evidence-attempt-5.log](final-evidence-attempt-5.log). Attempt-specific source copies and explanations are in validation.md.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/generated_body_delta.py` → exit 0; [generated-body-delta.log](generated-body-delta.log). Attempt-specific source copies and explanations are in validation.md.

- `.codex-test/run agentic-mbse validate work/active/WI-051_mfe-model-owned-major-radius/implementation/models --complete` → exit 1; [final-validation.log](final-validation.log), four passing levels and inherited L2/L6 failures.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/checkpoint.py phase1` → exit 0; `phase1-differential.log`. Individual L1/L2/L3 commands and exits appear above.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/checkpoint.py phase2` → exit 0; `phase2-differential.log`. Individual L1/L2/L3 commands and exits appear above.
- `.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/checkpoint.py phase3` → exit 0; `phase3-differential.log`. Individual L1/L2/L3 commands and exits appear above.
- `.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python -m pytest tests/models/test_mfe_major_radius.py -v -ra --junitxml=work/active/WI-051_mfe-model-owned-major-radius/implementation/phase3-tests-attempt-1.xml'` → exit 1; [phase3-tests-attempt-1.log](phase3-tests-attempt-1.log).
- `.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python -m pytest tests/models/test_mfe_major_radius.py -v -ra --junitxml=work/active/WI-051_mfe-model-owned-major-radius/implementation/phase3-tests-attempt-2.xml'` → exit 0; [phase3-tests-attempt-2.log](phase3-tests-attempt-2.log).
- `.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python -m pytest tests/models/ -v -ra --junitxml=work/active/WI-051_mfe-model-owned-major-radius/implementation/final-tests-attempt-1.xml'` → exit 1; [final-tests-attempt-1.log](final-tests-attempt-1.log).
- `.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python -m pytest tests/models/ -v -ra --junitxml=work/active/WI-051_mfe-model-owned-major-radius/implementation/final-tests-attempt-2.xml'` → exit 0; [final-tests-attempt-2.log](final-tests-attempt-2.log).

## Native PM provenance

- `.codex-test/run agentic-mbse pm trace-element --help` → exit 0; [trace-help.log](trace-help.log).
- `.codex-test/run agentic-mbse pm update-validation --help` → exit 0; [sv-help.log](sv-help.log).
- `.codex-test/run agentic-mbse pm trace-element --element 'mfe_plant::'"'"'MFE Power Plant'"'"'::magnet::R0' --file models/designs/generic_mfe/mfe_plant.sysml --type reference_usage --requirement MR-051-01 --requirement MR-051-03 --requirement MR-051-08 --source-type documentation --source-doc 'T-021 radius ownership assessment' --source-location 'work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md@2f8856b7; ## Model and existing source interpretation; ## Assessment' --confidence medium --assumptions 'Inherited model-intent interpretation: shared plasma/axis scale; standalone R0 and fixed reference anchors preserved. No general domain certification.'` → exit 1; [trace-generic-attempt-1.log](trace-generic-attempt-1.log).
- `.codex-test/run agentic-mbse pm trace-element --element 'mfe_plant::'"'"'MFE Power Plant'"'"'::magnet::R0' --file models/designs/generic_mfe/mfe_plant.sysml --type reference_usage --source-type documentation --source-doc 'T-021 radius ownership assessment' --source-location 'work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md@2f8856b7; ## Model and existing source interpretation; ## Assessment; MR-051-01/03/08' --confidence Medium --assumptions 'Inherited model-intent interpretation: shared plasma/axis scale; standalone R0 and fixed reference anchors preserved. No general domain certification.'` → exit 0; [trace-generic-attempt-2.log](trace-generic-attempt-2.log).
- `.codex-test/run agentic-mbse pm trace-element --element stellarator_09::stellaris::R --file models/designs/stellarator_09/stellarator_plant.sysml --type reference_usage --source-type documentation --source-doc 'Stellaris Design Paper, Table 2; inherited T-021 assessment' --source-location 'work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md@2f8856b7; ## Source observations; ## Assessment; MR-051-01/03/08' --confidence Medium --assumptions 'Existing sourced 12.7 m plasma major radius; now sole public operational radius. No new source approval or engineering envelope.'` → exit 0; [trace-stellarator.log](trace-stellarator.log).

[AGENT] Native SV child commands and exits are recorded above. No PM close/archive operation ran. Accepted native trace output has CRLF, retained because native operations own these rows. `git diff --check` reports those two line endings; it is not claimed passing.
