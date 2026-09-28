# Preparation and execution gates

[AGENT] This single study asks how thermal assumptions and explicit purchased choices change the integrated plant's operating demands, adequacy and costs while preserving independently selected inventory. Thermal, demand and selected-equipment point families answer that same dependency question. Price uncertainty belongs to a later round.

The commands below are proposed replay instructions, not a record that they ran. Use the repository's `.codex-test/run` launcher. Commands that construct the native evaluator also require the TEAx path documented in `../ANNEX.md`. The model author owns package generation/sealing and canonical receipts; the coordinator owns candidate promotion and execution release.

After a stable, committed package and four author baselines exist:

```bash
.codex-test/run python -m exploration.aries_integrated.studies.prepare_equipment_study metadata --author-receipt work/active/WI-090_aries-integrated-equipment-and-costs/evidence/baseline-execution.json
.codex-test/run python -m exploration.aries_integrated.studies.prepare_equipment_study check-canonical
.codex-test/run python -m exploration.aries_integrated.studies.prepare_equipment_study oracle-scan
.codex-test/run python -m scripts.study.indicators --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/manifest.json --groups exploration/aries_integrated/studies/axes.json --out exploration/aries_integrated/studies/20260922-aries-integrated-equipment-costs/indicators.json
```

Review retained canonical verification, oracle scan/domain refusals, indicators and exact new bindings. Finalize the windows and record every missing-response finding before execution. Metadata preparation computes no plant result; canonical checking and oracle scanning execute only independent development arithmetic. Native integration owns the baseline/preflight execution needed to produce a candidate. Do not run the study executor before the coordinator releases the matching native CANDIDATE.

The existing executor accepts the record path and actual integration-return path. It refuses a mismatched executable/semantic/indicator identity, dirty package or pre-existing results. After execution, run native numerical verification with the actual result store and identity document; choose all64 points if practical so all thermal/purchase families and verdict combinations are covered. No guessed store path or identity is supplied here.

Keep actual verification commands, package/source digests, copied source files and result identities in the final immutable snapshot. The checker imports `equipment_bindings.py` and `equipment_oracle.py`; both are part of its required source identity, alongside `oracle_entry.py` and route/interface dependencies. A digest of the entry file alone is insufficient.
