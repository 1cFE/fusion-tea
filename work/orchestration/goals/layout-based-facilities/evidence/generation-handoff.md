# Facilities generation and integration handoff

Date: 2026-09-18. Scope: read-only preparation against WI-067's current production procedure. No generation, repinning, model changes or production code edits were performed for this investigation. Instructions below are [AGENT] implementation guidance grounded in the referenced scripts, not authorization to execute them before the design release.

## Current producers

| Responsibility | Current path |
|---|---|
| Canonical/staged family ownership and copying | `tests/model_families.py`: MFE.owned, canonical_path, materialize_canonical_subset |
| Current reviewed generation recipe | `work/active/WI-067_installed-cooling-equipment-costs/evidence/regenerate.py` |
| Reused stock-generation function | `work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/regenerate.py`: seed_and_generate |
| Current reviewed manual-body inventory | `work/active/WI-067_installed-cooling-equipment-costs/evidence/candidate-seeds.json` |
| Baseline, manifest, census and snapshot producer | `work/active/WI-067_installed-cooling-equipment-costs/evidence/repin.py` |
| Tests' current generation pointer and explicit ABI expectations | `tests/models/current_mfe_regressions.py`: RECEIPT_EVIDENCE, current_generation, WI067_PARAMETERS |
| Canonical/staged and generation regression spine | `tests/models/test_model_family_spines.py` |
| Independent current plant equations | `exploration/stellarator_e2e/verify_stellaris.py`; cooling delegation in `oracle_cooling.py` |
| Explicit independent entry/output mappings and predicate operands | `exploration/stellarator_e2e/studies/oracle_entry.py` |
| Native route | `exploration/stellarator_e2e/studies/study_route.py` |
| Study manifest | `exploration/stellarator_e2e/studies/manifest.json` |
| Native integration | `scripts/integrate.py`; `docs/integration_seam_operator_guide.md` |
| Last WI-067 successful integration command | `work/orchestration/goals/installed-cooling-equipment-costs/evidence/round3/integration-retry1/integration_return.json`, command array |

The generated package lives at `exploration/stellarator_e2e/generated`. The public import alias `exploration/stellarator_e2e/pkg/stellarator_tea` is a symlink to `../generated`. The staged SysML tree is `exploration/stellarator_e2e/models`. The tracked structural snapshot is `exploration/stellarator_e2e/stellarator.snapshot.json`; the tracked census is `tests/models/data/mfe_census.json`.

## Smallest reproducible sequence after release

1. Add the new analysis to `tests/model_families.py` MFE.owned. Author canonical SysML and plant wiring. Synchronize staging with the existing copying helper below; this copies all owned MFE files, preserving canonical bytes.
2. Create a WI-068 generation recipe based on WI-067, preserving all31 current normative bodies and explicitly adding any new reviewed manual bodies. Obtain the new wrapper ABI from native generation before finalizing its tuple return. Record a reviewed hash inventory and exact fresh-generation evidence.
3. Extend the independent oracle, qualified input/output maps and any new predicate operand bindings. Update the test recipe pointer and explicit ABI expectations before deriving the new census. Root owns independent oracle work after the contract is stable.
4. Run the WI-068 generation and repin producers, then targeted tests. Do not invoke the old WI-067 recipes unchanged for a new family.
5. Obtain independent implementation assurance and commit the scoped producer results. Run integration against those reviewed identities. Integration verifies already-produced state; it is not the operation that repairs generation drift.

The existing staging helper can be invoked as follows after canonical changes are authorized:

```bash
.codex-test/run python - <<'PY'
from tests.model_families import MFE, materialize_canonical_subset
materialize_canonical_subset(MFE, MFE.twin)
PY
```

Current WI-067 producer entry points are exact existing commands:

```bash
.codex-test/run python work/active/WI-067_installed-cooling-equipment-costs/evidence/regenerate.py
.codex-test/run python work/active/WI-067_installed-cooling-equipment-costs/evidence/repin.py
.codex-test/run python -m pytest tests/models/test_model_family_spines.py tests/models/test_installed_cooling_equipment.py -q
```

For facilities, substitute the actual new WI-068 recipe paths and the new facilities tests. Those files are implementation deliverables; the placeholders below are not existing CLI commands:

```bash
.codex-test/run python work/active/WI-068_<actual-name>/evidence/regenerate.py
.codex-test/run python work/active/WI-068_<actual-name>/evidence/repin.py
.codex-test/run python -m pytest tests/models/test_model_family_spines.py tests/models/test_<facilities-tests>.py -q
```

The stock recipe invokes `run_codegen(GenerationConfig(output_path=..., package_name='stellarator_tea', overwrite=True, preserve_handwritten=True, smart_regen=True, models_path=...))`. It first copies only hash-checked normative seeds into a fresh destination, then generates. It repeats into a second fresh destination and requires exact byte equality. It does not accept arbitrary prepopulated output directories.

Repinning first executes the native baseline with CandidateBridge and the package route, then checks every mapped independent oracle output with the recorded tolerances. It updates manifest indicator-input fingerprints, recorded semantic/executable fingerprints, baseline headline and predicate verdicts. It derives the census through `scripts.integrate.rederived_census`, bound to the generated semantic fingerprint. Finally it calls `capture_instance_graph_snapshot` on the staged models to produce the tracked structural snapshot. Neither census nor snapshot should be hand-edited to satisfy a comparison.

## Integration invocation

This is the exact flag shape used by the successful WI-067 integration, with explicit placeholders for the new reviewed values:

```bash
.codex-test/run python scripts/integrate.py \
  --audited-work work/active/WI-068_<actual-name>@<audited-commit> \
  --models-root exploration/stellarator_e2e/models \
  --package exploration/stellarator_e2e/pkg/stellarator_tea \
  --manifest exploration/stellarator_e2e/studies/manifest.json \
  --groups tests/study/data/axes.known_answers.json \
  --census-file tests/models/data/mfe_census.json \
  --expected-semantic-fingerprint <reviewed-model-contract-fingerprint> \
  --expected-executable-fingerprint <reviewed-package-contract-fingerprint> \
  --expected-teax-revision <reviewed-teax-revision> \
  --route-sys-path exploration/stellarator_e2e/studies \
  --route-module study_route \
  --route-callable execute_baseline \
  --out-dir work/orchestration/goals/layout-based-facilities/evidence/integration
```

Read the semantic fingerprint from generated `contracts/model_contract.json` and executable fingerprint from `contracts/package_contract.json`, as recorded by the audited work. Use the reviewed teax checkout revision; do not replace a drifted expected revision with whatever is currently installed. WI-067's historical successful command used teax revision `8d877460ac4f6f264561d916e40c1708adb13397`; its historical model/package fingerprints must not be reused for the facilities package.

## Traps and constraints

- The WI-067 regeneration assertions require29 preserved bodies plus exactly2 cooling additions. A facilities addition therefore needs a new recipe and inventory, not edits to the historical recipe to make its assertions pass.
- `tests/models/current_mfe_regressions.py` RECEIPT_EVIDENCE currently points at WI-067. The family-spine tests load their generator through that pointer. Updating only MFE.owned leaves them on the old seed inventory.
- `tests/models/test_model_family_spines.py` contains an explicit expected parameter-count union. Add named facilities parameters there and in the shared regression declarations; do not use the newly generated contract itself as the sole expected ABI.
- Wrapper tuple order can differ from SysML declaration order. WI-067's `equipment-generated-abi.json` records the native order; follow the same evidence pattern for facilities.
- Map each new oracle input/output explicitly in `oracle_entry.py`. Generic verification fails closed on unmapped inputs and compares mapped outputs; an omitted output can leave a real blind spot. WI-067's first integration attempt exposed one missing calendar-output mapping.
- If a new predicate is introduced, update its explicit operand bindings and the route's expected constraint count. Preserve existing physical predicates and adverse results.
- Integration requires regeneration, snapshot capture and manifest checks to move zero bytes. Complete those producer operations and commit their results first.
- Integration gate4 uses `--census-file`, while gate5 always reads the tracked `tests/models/data/mfe_census.json`. A scratch census cannot substitute for the tracked one.
- Supply exactly one package and one manifest, exactly one sibling snapshot beside the model root, and an output directory outside the package root.
- `.codex-test/run` supplies the sealed environment described in `.project/codex-test-setup.md`. Do not substitute bare Python or ordinary syncing uv invocations. The seam adds repository/teax import paths and STUDY_REQUIRE_TEAX=1 to its child producers.
- The canonical MFE copying helper does not delete obsolete staged files. If the design retires a file, handle that deliberate removal and its ownership change explicitly; a new analysis alone needs no deletion.
- WI-067 documented six stale consumer-test failures and static validation limitations. Its targeted passes are not a whole-suite green baseline. Preserve and reassess relevant regressions rather than silently treating all entering tests as passing.
