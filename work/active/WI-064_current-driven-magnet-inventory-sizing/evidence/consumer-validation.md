# WI-064 current-generation consumer validation

[AGENT] The consumer adapter now selects the WI-064 reviewed seed/receipt recipe. Explicit ABI expectations add the two sizing inputs and six sizing outputs. Frozen historical artifacts and original numerical baselines are unchanged; temporary translated replays include independently computed new diagnostic outputs. No new predicates were introduced.

## Initial failure and repair

Command: `.codex-test/run python -m pytest tests/models/test_structure_translation.py -q`.

Result before repair: 1 failed, 6 passed in 2.18 s. The live-contract bijection assertion omitted exactly `magnet__winding_pack__sizing_mode` and `magnet__winding_pack__inventory_multiplier`. Inspection found the corresponding stale unions in the major-radius, operating-heating and model-family consumers. Their explicitly enumerated input/output unions were updated with WI-064 additions. The receipt path in `tests/models/current_mfe_regressions.py` now points to this item's `regenerate.py`, preserving the prior reviewed manual bodies plus the one added sizing calculation.

## Affected checks

Command: `.codex-test/run python -m pytest tests/models/test_structure_translation.py tests/models/test_mfe_major_radius.py tests/models/test_mfe_operating_heating.py tests/models/test_model_family_spines.py tests/models/test_mfe_financial_rate_limits.py -q`.

Result after repair: **166 passed, zero failed/skipped, in 90.30 s**. Temporary command output: `/tmp/wi064-consumers.log`. `git diff --check` passed for all five edited consumer files. No broader suite was run by this reader.

Coverage includes explicit current ABI/translation boundaries, fresh generation and seed refusal, major-radius native/direct/CLI regression replay, operating heat and financial attribution/parity, canonical/twin model-family equality and dependency-mutation checks, and financial finite-rate regressions. This is affected-consumer verification, not an independent item audit or the full model suite. Coordinator-owned oracle, census, manifest, snapshot and integration changes are consumed by these checks but were not edited here.
