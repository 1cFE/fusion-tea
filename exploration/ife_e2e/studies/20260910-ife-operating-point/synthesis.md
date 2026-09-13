# IFE operating-point study synthesis

**Administrator:** fresh Codex agent `/root/ife_study_admin`. **Date:** 2026-09-10. **Mode:** ADMINISTER, bounded record-only reading. **Snapshot SHA256:** `3edebbe53943050eba7de55102f8773e21b09db8cf3b2c2b5dd92c5e2103179e`, recomputed from [snapshot.json](snapshot.json). This synthesis separates recorded facts from administrator interpretations; it does not rerun or amend the study.

## What the study set out to do

**Recorded:** Test how beam energy and repetition rate affect the corrected IFE net-power and price calculations, then check that fixed negative/zero-generation cases are ineligible for price comparison. The executor chose five unique one-factor points and two coordinated diagnostics in one arm. The framing is agent-originated and recorded as owner-ratified. The ordinary window is engineered: beam 4/5/6 MJ at 4.6 Hz, and rate 3.6/4.6/5.6 Hz at 5 MJ, with gain and other assumptions held. [protocol.md](protocol.md), [results/window.json](results/window.json), [results/proposals.json](results/proposals.json).

## What it found

**Recorded results:** Each ordinary increase raises net generation and lowers each separately denominated price across its three sampled points. All five ordinary points are model-feasible and price-eligible. Both diagnostics fail eligibility; their stored zero prices are invalid sentinels. Values below are rounded from [results/points.csv](results/points.csv); qualified channels, generating flags and inputs are retained in [results/cases.json](results/cases.json).

| Case | Net electric MW | Hawker mixed-basis $/MWh | Meier 1988 cents/kWh |
|---|---:|---:|---:|
| Baseline: 5 MJ, 4.6 Hz | 871.231786 | 240.666461 | 5.589992 |
| Beam 4 MJ | 696.985429 | 290.031012 | 6.257484 |
| Beam 6 MJ | 1045.478143 | 207.756760 | 5.125380 |
| Rate 3.6 Hz | 681.833571 | 244.405964 | 6.773097 |
| Rate 5.6 Hz | 1060.630000 | 238.272338 | 4.806524 |
| Counterexample | -46.000000 | Invalid sentinel | Invalid sentinel |
| Exact zero | 0.000000 | Invalid sentinel | Invalid sentinel |

**Recorded verification:** All seven cases completed and were checked across thirty numerical channels and both re-derived predicates. No verdict mismatches occurred; worst relative deviation was approximately `1.025e-15`, below `1e-9` tolerance. The independent reference comparison covers bank energy and driver electrical draw for all seven cases; it does not compare whole-plant net power or LCOE on a common basis. [results/verification_summary.json](results/verification_summary.json), [results/1costingfe-driver-identities.json](results/1costingfe-driver-identities.json), [results/reference-applicability.md](results/reference-applicability.md).

## Framing verdict per axis

| Axis | Recorded proposed → judged framing | Administrator reading |
|---|---|---|
| `beam_energy_mj` | Sensitivity → sensitivity; unchanged | Supported. Net power and both prices respond at 4/5/6 MJ while both verdicts remain satisfied. These points reveal response under held assumptions, without locating a boundary. |
| `frequency` | Sensitivity → sensitivity; unchanged | Supported. Net power and both prices respond at 3.6/4.6/5.6 Hz while both verdicts remain satisfied. No repetition-rate ceiling is identified. |

Evidence: [record.md](record.md), sections 5–6; [results/points.csv](results/points.csv). The wider oracle scan also retains positive net power throughout its sampled beam/rate values. The diagnostics change several inputs together and sit outside the ordinary window; they cannot turn either axis into a searched feasibility boundary. [results/oracle-scan.json](results/oracle-scan.json), [results/proposals.json](results/proposals.json).

## Constraint structure

| Named constraint and complete identity | Recorded structure | Every case outcome |
|---|---|---|
| `net_positive`: `hif_plant_pkg__hif_plant__net_positive__1d299cceab19c61c` | Computed net electric power strictly greater than zero; reachable from each axis | Satisfied: baseline, beam-4.0, beam-6.0, rate-3.6, rate-5.6. Violated: counterexample, zero. |
| `viability`: `hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b` | Efficiency-times-gain heuristic at or above its threshold; bound operands unreachable from either axis | Satisfied on all seven cases, including counterexample and zero. |

Evidence: [indicators.json](indicators.json), [results/points.csv](results/points.csv), [results/context/ANNEX.md](results/context/ANNEX.md), “Validity masks.” No indeterminate outcome occurred. Both axes have `no_constraint_response: false`; graph reachability alone establishes neither response sign nor a verdict change. Eligibility additionally requires a generating flag of one and a finite positive price. **Administrator interpretation:** the retained counterexamples directly demonstrate why the heuristic cannot substitute for the strict net gate. They do not establish completeness of the two-check constraint set.

## Findings carried forward

These are the executor's three findings and recorded dispositions, preserved from [record.md](record.md), section 15.

- **`20260910-ife-operating-point#1` — model fix:** The corrected chain responds coherently and rejects non-generation despite the satisfied heuristic. Recorded disposition: WI-048 independently audited; this study verifies the retained repair at named points. Evidence: [results/context/WI048-audit.md](results/context/WI048-audit.md), [results/cases.json](results/cases.json).
- **`20260910-ife-operating-point#2` — declared seam:** Held gain and absent sourced beam/rate capacity checks prevent engineering-boundary claims. Recorded disposition: unresolved engineering coverage, with source/engineering work and owner disposition still required; no residual acceptance. Evidence: [results/context/ANNEX.md](results/context/ANNEX.md), [record.md](record.md), sections 6 and 15.
- **`20260910-ife-operating-point#3` — declared seam:** The prices retain incompatible historical bases. Recorded disposition: separate labels enforced; normalized comparison and residual acceptance remain owner-held. Evidence: [results/context/ANNEX.md](results/context/ANNEX.md), “Baseline pin”; [results/reference-applicability.md](results/reference-applicability.md).

## What the record does not support

- **Missing engineering evidence:** No measured hardware performance, gain-versus-beam relation, validated capacity envelope, optimum, or source-backed feasibility boundary is supplied. Arithmetic agreement cannot fill these gaps. [record.md](record.md), sections 13 and 17.
- **Missing common financial basis:** Neither cross-price ranking nor agreement with the historical Osiris price is established. The copied audit distinguishes the printed 1992 price from the computed Meier 1988 interpretation. [results/context/WI048-audit.md](results/context/WI048-audit.md), “Acceptance and completion gates.”
- **Limits of independent verification:** The oracle shares selected source facts and held assumptions with the model and supports positive integral construction/operation years. A full source-image re-audit is absent; the copied audit cites supporting material that is not all copied here. These are evidence limits, not newly verified source authority. [record.md](record.md), sections 13 and 17; [results/context/ANNEX.md](results/context/ANNEX.md), “Oracle”; [results/context/WI048-audit.md](results/context/WI048-audit.md).
- **Process provenance limit:** The verification summary's TEAx revision is `unrecorded`; the snapshot separately records revision `8d877460ac4f6f264561d916e40c1708adb13397`. The revision is therefore available as snapshot provenance, but this reading cannot independently recover the verifier's runtime identity from its summary. The complete generated package and external reference checkout are also revision/fingerprint-identified rather than copied in full. [results/verification_summary.json](results/verification_summary.json), [snapshot.json](snapshot.json), [record.md](record.md), section 17.
- **No broader acceptance:** The recorded PASS reviews cover their stated scopes. They do not accept findings #2/#3 or certify whole-project readiness; the copied WI-048 audit still reports Level 6 failure. [post-execution-review.md](post-execution-review.md), [results/context/WI048-audit.md](results/context/WI048-audit.md).
