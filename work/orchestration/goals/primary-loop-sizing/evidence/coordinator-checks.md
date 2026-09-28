# Coordinator verification

2026-09-16. These are coordinator checks, not independent certification.

- `.codex-test/run python scripts/source_registry.py verify`: exit 0; zero faults and three pre-existing legacy entries (COST_MODELING.md loose file; eu_demo_rw_tf_coil_conductor_dematte_bruzzone and iter_cryoplant_iter_org orphan source directories). The newly registered source is coherent.
- `git diff --cached --check -- work/orchestration/goals/primary-loop-sizing knowledge/research knowledge/SOURCE_INDEX.md knowledge/MANIFEST.jsonl`: exit 0 at research checkpoint df41ea97. The raw registered extraction carries extractor-produced trailing whitespace; its captured bytes and registered digest were preserved.
- T-002 integration retains actual ten-gate results. Regeneration rewrote no package bytes, handwritten bodies remained identical, census/snapshot and baseline/oracle verification passed. Its explicit read-set-coverage omission remains unverified.
- No model implementation stage is required for the supported result: the existing loop-count input already expresses the conditional replication. New area or price laws are unsupported. The source/math and cost reviews establish why the owner's quantified-requirement/evidence-gap branch is used; this is not certification of a newly sized physical cooling plant.

- Prefreeze native record checks: `.codex-test/run python -m pytest tests/study/test_records.py -q -k 20260916-primary-loop-sizing` reports 3 passed. Initial missing backticks around § 15 finding IDs were corrected before freezing; no result or snapshot changed. All 9 answer links resolve. `commit-custody.json` verifies all 174 required study files in frozen commit `75772eba` and no model/package changes from entering `b9ddffb7`.

- After accepted discovery-log updates and the study's review addendum, `.codex-test/run python -m pytest tests/study/test_records.py -q -k '20260916-primary-loop-sizing or joined_disposition'`: 4 passed, 66 deselected. This checks the completed record and exact finding joins after bookkeeping changes.
