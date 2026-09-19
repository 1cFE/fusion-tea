# WI-071 implementation candidate

[AGENT] Author implementation and verification, 2026-09-19. The fresh method/source/interface review in `work/orchestration/goals/cost-estimate-maturity-and-uncertainty/evidence/method-review.md` released this bounded change. Independent implementation assessment and native integration are pending. No study, git staging or commit was performed by this worker.

## Behavior and scope

One public heat-transport input, `stellarator_09__stellaris__heat_transport__equipment_stainless_fabrication_usd2017_per_kg`, defaults to 310 USD2017/kg and supplies exactly four pre-existing finished-fabrication bills: initial exchanger, primary piping, secondary piping and future exchanger bundle. Existing installation/removal fractions follow their original bases. Initial delivered-cost exclusions follow changed initial purchases; future replacement is absent from the initial exclusion. No new equipment producer was added.

The nominal native result reproduces all 956 frozen WI-070 output channels exactly and all 25 authored predicate statuses exactly. The headline aggregate response is also still violated. Overnight capital stays $17,918,171,013.726093; headline LCOE stays $271.5843199172948/MWh; comparison-form LCOE stays $266.4589305666054/MWh. Evidence: [nominal preservation](evidence/nominal-preservation.json), [baseline](evidence/baseline.json), [unchanged entering baseline](evidence/entering-baseline.json).

The new rate is checked for positive, finite values on the active equipment path. The disabled calculation returns its original finite zero outputs before active guards. The existing overall equipment-price multiplier remains distinct and continues to affect machines and inventories as before. The new source-rate input does not price those items.

The oracle adapter also exposes the existing native `stellarator_09__stellaris__contingency_rate` key. The independent equation/default already existed. This mapping is the verification prerequisite for separately labeled zero-contingency diagnostics, and changes no model formula or baseline policy.

## Source meaning

ANL printed26–27 supports a fixed carbon reference of 120000 USD2017/metric tonne and a stainless/carbon factor of 2–3, with its recommended stainless amount 310000 USD/tonne. Dividing by 1000 kg/tonne gives the retained 310 and the conditional 240/360 USD2017/kg cases. The source's January2017 basis continues to use the inherited annual CPI2017=245.1 to annual CPI2025=321.9 purchasing-power approximation. It is not an equipment escalation index or a whole-plant price normalization.

The endpoints represent a conditional source-family construction analogy. They do not bound the carbon base, modern fabrication quotes, target helium/salt applicability, equipment geometry, missing equipment, delivery schedule or plant accuracy. These limits are in the source-facing model comments and the method review; no new confidence claim accompanies the exposed parameter.

## Changed implementation and consumers

The authoritative model changes are `models/library/analyses/mfe_cooling_equipment.sysml`, `models/library/structure/mfe_plant_systems.sysml` and `models/designs/stellarator_09/stellarator_plant.sysml`. Their MFE twins are byte-identical. The owner and formal have distinct names; the existing pattern binds the owner input into the calculation. The MFE family has one active stellarator occurrence and a generic disabled compatibility path. No affected definition belongs to the IFE family.

The only changed normative manual seed is [cooling_equipment_impl.py](seeds/cooling_equipment_impl.py). Its generated copy receives the new typed input, rejects invalid active rates through the existing guards, and replaces exactly four hardcoded multipliers. All 35 unrelated manual seeds remain byte-identical to WI-070. The independently written `exploration/stellarator_e2e/oracle_cooling.py` uses `fabrication_rate_2017`; `verify_stellaris.py` passes `cooling_fabrication_rate_2017`, and `studies/oracle_entry.py` maps the exact native key.

Stock regeneration changes the cooling wrapper/schema, public input schema/JSON, pipeline, contracts and fingerprints. Three other automatic calculation wrappers/bodies have source-line-number metadata changes only: cooling initial handoff, initial sector start, and special-material capital. Their equations are unchanged. [Generation changes](evidence/generation-changes.json) and [changed manual seed](evidence/changed-seeds.json) separate those effects. Model-family census, manifest and structural snapshot are regenerated. The current regression helper points to this item's seed protocol and names the one additional entry explicitly.

The complete tracked change list is [changed-paths.json](evidence/changed-paths.json); this item directory itself additionally owns the seed, scripts, specification and evidence. The new test file is `tests/models/test_shared_cooling_fabrication_rate.py`. The installed cooling tests supply the new compatibility input and encode retained legacy Boolean proposals using the existing accepted numeric representation. No shared runner, input-admission policy or toolchain implementation changed.

## Generated identity

| Identity | Value |
|---|---|
| Native entry points | 490, one more than WI-070 |
| Semantic fingerprint | `ea1555ea133db8ed7ba1c638b29ddf540ba99d811bfcf7d9ef9454b626d3a28a` |
| Executable fingerprint | `b032da4a3971979792bc024bf9cd1a41a2d83d340bad5b59ef3e1a9aeaa77236` |
| Indicator/candidate pin | `e48d5218b6e3be2775a94269a461dccd259fccc5fc41fed7c135dc1336bfe284` |
| Manual completion inventory | 36 bodies; 35 unchanged, one revised |

Two separate fresh stock generations match the complete retained package inventory exactly. The canonical and twin family sources agree. The scripts use the already-established WI-070 procedure and the WI-040 hash-checked stock generator, with a new WI-071 seed inventory. No historical generation record was modified. [Generation log](evidence/generation.log), [model hashes](evidence/model-hashes.json), [package hashes](evidence/package-hashes.json), [repin log](evidence/repin.log).

## Validation results

All commands run from repository root through `.codex-test/run`. The verification scopes below overlap; their counts are not summed as independent evidence.

| Command after launcher | Result | Evidence |
|---|---|---|
| `python work/active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/regenerate.py` | Two fresh packages exactly equal; unrelated seeds unchanged | `evidence/generation.log` |
| `python work/active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/repin.py` | Native nominal baseline agrees with 934 mapped oracle channels; manifest/census/snapshot derived | `evidence/repin.log`, `baseline.json` |
| `python -m pytest tests/models/test_shared_cooling_fabrication_rate.py tests/models/test_installed_cooling_equipment.py -q` | **43 passed**, 16 inherited Boolean serializer warnings | `evidence/cooling-tests-repaired.log` |
| `python -m pytest tests/models/test_model_family_spines.py tests/models/test_fuel_processing_oracle.py tests/models/test_facility_account_consumers.py tests/models/test_facilities_oracle.py -q` | **89 passed**, 25 Boolean serializer warnings | `evidence/affected-tests.log` |
| `python work/active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/verify_candidate.py` | **Six native cases; 5604 mapped comparisons and 150 authored-predicate comparisons pass; zero calculation failures** | `evidence/native-candidate-cases.json` and `.log` |
| `agentic-mbse validate --complete exploration/stellarator_e2e/models` | L1/L3/L4/L5 pass; L2/L6 fail, exit 1 | `evidence/static.log` |
| `python work/active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/static_check.py` | L2 exactly10 issues and L6 exactly1082; no added or removed issue identities against WI-070 | `evidence/static-delta.json` and `.log` |

The tests independently derive source metric-ton conversion, exactly-once CPI application, all four fabrication bills, dependent installation/removal, the single bundle replacement's discounted annual contribution, direct/delivered/overnight account deltas and headline LCOE deltas. They assert invariant nonfabrication equipment, every output outside the declared monetary fan-out, physical predicates, net electricity and availability. They also test zero/negative/infinite/NaN active prices and dormant finite behavior through the typed public module, and check both zero and 10% contingency through the whole native pipeline and independent oracle.

The bounded native receipt exists for implementation review, not as the goal's uncertainty study. Its six rows reproduce these results:

| Raw rate USD2017/kg | Direct contingency | Cooling installed USD million | Cooling replacement USD million/year | Overnight USD million | Headline USD/MWh |
|---:|---:|---:|---:|---:|---:|
| 240 | 0.10 | 5114.294826 | 50.779434 | 15978.171726 | 245.286727 |
| 310 | 0.10 | 6471.347146 | 55.673508 | 17918.171014 | 271.584320 |
| 360 | 0.10 | 7440.670231 | 59.169275 | 19303.884790 | 290.368315 |
| 240 | 0 | 5114.294826 | 50.779434 | 14555.567435 | 226.452466 |
| 310 | 0 | 6471.347146 | 55.673508 | 16317.702399 | 250.395262 |
| 360 | 0 | 7440.670231 | 59.169275 | 17576.370230 | 267.497260 |

Every row retains the reference's four violated physical predicates; no row is presented as feasible. The annual-energy denominator remains 7,978,704.890195747 MWh/year. Full precision outputs and verdicts are in the native receipt.

The initial test log is retained as `evidence/cooling-tests.log`: 38 passed, five failed. One new assertion incorrectly compared the whole response map, including its aggregate headline field, with the frozen list of 25 authored predicates. The repaired assertion checks those exact25 and separately requires the violated headline. Four retained legacy controls were refused before execution because stock proposal admission rejects their Boolean encoding. The already-documented numeric0/1 encoding repairs only the caller representation; the original control values, plant equations, shared route and expected results remain unchanged. The corrected command's full result is retained separately. No failing physical point was removed or expectation relaxed.

Native PM operations registered **SV-119** and **SV-120**, then marked both passing on the above tests. The registration receipt retains the pre-existing malformed-type warnings in the validation matrix. No existing criterion was changed. The current full static diagnostics and twenty-two inherited numeric channels outside the oracle map remain limitations. Integration, including its read-set coverage behavior, is a coordinator-owned next step and is not certified here.

## Acceptance and handoff

MR-071-01 through MR-071-05 have author evidence in the nominal receipt, source/bill tests, canonical comments, native cases and regeneration/consumer checks above. Independent implementation assessment remains unchecked in the specification. The coordinator can audit this coherent candidate, commit approved scientific files, run native integration and then release the combined conditional uncertainty study. No additional engineering accuracy, source-scope completeness, price-year reconciliation or S3 grade follows solely from these implementation checks.
