# Integrated ARIES heat and electricity

The positive integration goal is met under the documented assumptions. Native integration and the committed fourteen-point study pass their declared verification. The [independent final review](evidence/round-review.md) accepts the result and finding dispositions. The owner closed the goal and WI-089 on 2026-09-22.

## What runs

One native assembly at `models/designs/aries_cs_integrated/plant.sysml` connects an explicit plasma/source selector to fuel demand, neutron/charged heat deposition, helium/PbLi/divertor circuits, fixed-capability heat exchangers, a recuperated Brayton cycle, generator/auxiliaries and net electricity. Every reported physical output comes from the generated graph. The reusable additions are in `models/library/analyses/integrated_heat_electricity.sysml`; the package is `exploration/aries_integrated/aries_integrated`.

The calculated-plasma nominal scenario is a conditional engineering approximation. It is not a verified reconstruction of the published ARIES plant. Its assumptions were chosen before native execution; no input was fitted to source electrical output. `run.py` names the canonical scenarios, and the study’s full point maps identify every supplied input.

## Native nominal and comparison results

| Scenario | Fusion MW | Heat accepted MW | Unmet removal MW | Gross electricity MW | Net electricity MW | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Calculated-plasma nominal | 1835.451283 | 2240.389047 | 0 | 655.354927 | 423.106794 | Connected assumed scenario; all ten scoped checks satisfied |
| Lyon source-conditioned, assumed equipment | 2436 | 2759.082152 | 158.725848 | 1028.658530 | 796.005288 | Thermally inadequate; electricity describes removable-heat subset |
| Literal Lyon source-input variant | 2436 | 2518.899476 | 398.908524 | 1039.669902 | 807.016660 | Source recuperator setting retained; heat-removal failure retained |
| Literal Raffray accounting variant | 2365 | 2517.615798 | 502.134202 | 1038.516213 | 805.910865 | Heat-removal failure and 182.03 MW source-energy mismatch retained |

The literal variants preserve available source inputs while retaining named assumptions for missing inputs. They are not complete published-plant reconstructions. Lyon reports 2436 MW fusion, 1253 MW gross electricity and a 1000 MW electric plant basis. Those are comparisons, not targets fitted by this model. Source-mode fusion is conditioned on a supplied source value; calculated-mode fusion comes from the unchanged WI-083 plasma calculation. Raffray’s 1192 MW He and 1444 MW PbLi duties are reproduced source accounting, with the original -1 MW blanket-deposition discrepancy. Electrical outputs are calculated under the stated approximations; none establishes independent source agreement.

The nominal heat paths deliver 896.545166 MW from blanket helium, 1039.526189 MW from PbLi and 304.317692 MW from divertor helium. The cycle rejects 1571.659530 MW and produces 668.729517 MW net shaft work after 1372.850948 MW compressor demand. Generator losses are 13.374590 MW. Plant auxiliary electricity is 232.248133 MW: primary pumps 166.01, heating 40, cryogenics 10, fuel processing 6.238133, control 5 and other loads 5 MW. Pumping work recovered as heat enters once; full pump electricity is debited once. Cycle compression is debited before generation, not again as a plant auxiliary.

The nominal whole-plant residual is approximately -7.54e-9 MW against a 2.24e-6 MW modeled tolerance. Unmet heat is an explicit operating inadequacy, not an invented rejection path. A small arithmetic residual cannot turn the source variants into steady operating plants.

## Assumptions and supported use

The sole detailed assumption/source register and interface contract remain in [WI-089 design](../../../completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md). Important boundaries are constant fluid properties, nominal compressor/turbine efficiencies, a sequential three-exchanger approximation to the published network, assumed deposition partition and neutron multiplication, supplied primary flows/UA/hot-temperature limits, and named auxiliary-load assumptions. The recuperator/exchanger feedback is solved inside a typed native calculation. Flow, conductance, compressor ratios and offered ratings remain independent supplied choices.

Deposition transport, hydraulic performance, material limits, machine maps, magnets and breeding remain scientifically unqualified. Native outputs carry conditional-result and unsupported-science flags. Scalar capacity satisfaction is narrower than equipment qualification. A supplied reference value does not turn an unavailable magnetic or breeding calculation into a pass.

## Verification and preservation

The native development evidence contains 40 cases: 30 evaluated cases and ten expected domain refusals. Every one of the eight represented equipment ratings has a low/high test at fixed demand. A fresh reviewer independently traced density amplitude 5e20 → 5.15e20 through fusion power 1835.451 → 1947.230 MW and net electricity 423.107 → 513.776 MW with every other entry unchanged. Independent counterflow temperature/heat checks and a closed-form thermal check agree. See [implementation review](evidence/implementation-review.md).

Validation levels 1–5 pass. Level 6 retains 182 documented unsupported static EXPOSE forwards; actual generated execution resolves them. This is a scoped reviewed tool limitation, not a complete-validator pass. The original Stellaris replay reproduces all 1,352 numeric outputs and 68 responses exactly; all 8,657 protected entry files remain unchanged. Digest preservation and behavioral replay are separate evidence.

Two bounded tooling prerequisites are recorded separately: explicit ownership of independently generated ARIES source sets, and optional declared absolute accuracy for near-zero numerical residual verification. The latter keeps ordinary relative comparisons and exact independently re-derived verdict agreement. Additional old verifier regressions retain two stale entering Stellaris expectations (73 passed, one skipped, two failed), demonstrated against entry Git evidence; no original model or frozen result was altered to satisfy them.

## Study and exact package identity

The current native package is `aries_integrated`, executable `cebe17fd3ca0dae4c5102365b384cc40635406b3c470c29dd7f55c086b9657bd`, semantic fingerprint `35c6023027b2a842b3a681ae44bb782485394c60a5dd18dde382bc3b3f269c97`, under TEAx revision `8d877460ac4f6f264561d916e40c1708adb13397`. It is checkpointed at `687a57ad`. The original physical verification used executable `469191fd32c624ccf70e0b4ebc1065b34920df8174c37a09e8f45ecfb241a7d7`; thirteen typed completion adapters preserve the original module AST and all four canonical input/output sets exactly. See [corrective packaging review](evidence/packaging-review.md).

The sole native candidate passes every integration gate at `a8912fa4`. Its indicator-input pin is `55d5e43ae88b6bd5cf720ce7a8a41422d67d100a18e14b6367775860d0caacfb`. See [native gate return](evidence/integration-attempt3/integration_return.json).

All fourteen declared native study points completed. Independent checking covers all fourteen points across five verdict combinations: 420 scalar comparisons on thirty named channels and 140 exact predicate-verdict comparisons. The checker uses independent numerical integration/root methods but shares stated reaction-law authority; it does not independently validate every one of the 211 stored numeric channels (187 are declared CSV columns) or unsupported scientific models. A reviewed 1e-7 MW absolute comparison allowance applies only to the near-zero ledger residual, below the model's minimum engineering tolerance; ordinary comparisons retain relative 1e-9 and all verdicts require exact agreement.

| Change from calculated nominal | Net MW | Unmet heat MW | Observed response |
|---|---:|---:|---|
| Density amplitude 4.5e20 m^-3 | 140.230696 | 0 | Fusion falls to 1486.715539 MW; every hardware input held fixed |
| Density amplitude 5.5e20 m^-3 | 735.759323 | 0 | Fusion rises to 2220.896052 MW; every hardware input held fixed |
| Fuel processing rating 1e22 / 2e22 particles/s | 423.106794 / 423.106794 | 0 / 0 | Low rating fails, high rating passes; demand unchanged |
| Helium rating 500 / 1800 MW | 423.106794 / 423.106794 | 0 / 0 | Low rating fails, high rating passes; heat demand unchanged |
| First compressor ratio 1.4 / 1.65 | 470.897994 / 366.692730 | 0 / 0 | Cycle response changes at fixed other selections |
| Helium exchanger UA 5 / 75 MW/K | 389.195517 / 423.106794 | 47.118607 / 0 | Low conductance fails heat removal; extra conductance gives no gain once the supplied heat is accepted |

The four baseline/source scenarios above are included in the same study and preserve their failures. These points demonstrate sensitivity and insufficient/sufficient supplied equipment; they do not locate a feasible-region boundary or engineering optimum. The [frozen native study](../../../../exploration/aries_integrated/studies/20260922-integrated-heat-electricity/record.md) is committed at `8e6fb2f2`, snapshot SHA-256 `e888d008f2e740129bdbb39f359a619df53a2d9d6fd789a1df40a982a2bbc4ca`. Its [executor synthesis](../../../../exploration/aries_integrated/studies/20260922-integrated-heat-electricity/synthesis.md) states the reading and its limits. Eight finding IDs retain concrete dispositions in the study discovery log.

## Successor handoff

Prompt 02 should continue from this single assembly and its explicit interfaces. Its independent equipment choices provide a starting point for inventory and cost ownership, but actual exchanger geometry/materials, purchased machine ratings/maps, pump/hydraulic data, installation quantities and applicable prices remain missing. Fuel inventory, cryogenic configuration, magnetic hardware qualification and breeding response remain separate work. Price supplied equipment; do not silently convert required duty into installed purchases. Preserve the literal failures and the conditional status of the nominal result. Before making stronger published-plant claims, separately reconcile each source configuration’s deposition/auxiliary energy basis, thermal topology, temperature limits and exchanger performance; the present record establishes those discrepancies, not their physical resolution.

## Replay without replacing accepted evidence

From the recorded repository checkout, use the pinned `.codex-test` environment. The sealed package archive is not a standalone execution environment; seven native-tool schemas resolve through that recorded checkout. This runs the same fourteen full point maps, including the calculated nominal, into a fresh temporary record and store:

```bash
study_replay_dir=$(mktemp -d /tmp/aries-integrated-replay.XXXXXX)
cp exploration/aries_integrated/studies/20260922-integrated-heat-electricity/proposed-points.json "$study_replay_dir/proposed-points.json"
.codex-test/run bash -c '
  export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"
  export STUDY_REQUIRE_TEAX=1
  python -m exploration.aries_integrated.studies.execute_study --record "$1" --integration-return "$2"
' _ "$study_replay_dir" work/orchestration/goals/aries-integrated-heat-electricity/evidence/integration-attempt3/integration_return.json
```

Inspect `results/cases.json` and `results/cases.csv` under that fresh directory. `nominal-calculated` identifies the accepted nominal. Recheck the complete native integration gate separately with `.codex-test/run python work/orchestration/goals/aries-integrated-heat-electricity/evidence/integrate.py --out-dir /tmp/aries-integration-replay`, choosing a fresh output directory for each replay. Check protected originals with `.codex-test/run python work/orchestration/goals/aries-integrated-heat-electricity/evidence/check-preservation.py --output /tmp/aries-preservation-replay.json`.
