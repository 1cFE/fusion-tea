# Narrative: pre-reveal-feasible-neighborhood

This narrative summarizes cited records. It is not evidence, state, authorization, or a decision record. If it disagrees with a cited source, the source wins.

- **Goal status:** Closed on the reviewed conditional sampled-neighborhood answer, by the owner's explicit ruling. [Closure][close]
- **Goal closed:** 2026-09-17; approximately 23:43:08 UTC, **Git commit-time proxy**, commit `482c30aa`. The owner entry supplies the date but no time. [Closure][close]
- **Narrative cutoff:** Clean cited sources at `e78099cb93ab36b57debf70045cc9c4e7bcfcdd8`; generated 2026-09-17 23:49:14 UTC. Unrelated working-tree edits are excluded; this cutoff is not provisional.
- **Review status:** Independent pre-execution, result-assurance, and final-round reviews all PASS within their stated scope. The native record predates final publication assurance; the goal review supplies that later coverage. This narrative has no independent review. [Review][review]

## At a glance

- **Starting question:** Could a wider search find nearby designs passing the current model's engineering checks before opening the sealed ARIES comparison? The owner accepted a well-explained negative answer too. [Goal][goal]
- **What changed:** Geometry and plasma operating choices were explored together under unchanged equations and limits. The passing configuration includes a separately declared 1.01 conductor-inventory multiplier: extra purchased conductor with modeled size and cost consequences. [Answer][answer]
- **Measured result:** 103 of 334 selected native cases passed all twenty implemented screens with valid power accounts. Around the chosen design, 43 of 45 tested neighbors passed. These selected samples do not establish a continuously feasible region. [Report][report]
- **Practical limit:** The smallest passing-neighbor margins were 0.0261 T for peak magnetic field and 0.0315 MW/m² for divertor heat load, the heat reaching the exhaust target. Engineering qualification, sufficient tritium production, and complete installed costs remain unresolved. [Report][report]

## Starting point and motivation

The owner asked whether a broader search could show “SOME plausible 2d region” before reveal. That was a request to investigate, not evidence that such a region must exist. The campaign required an evaluated-point map and retained failures, with a bounded negative answer permitted. [Goal][goal]

Earlier fixed-operating-assumption work had found no combined pass. The current model used the exact reference profile convention, but its frozen comparison controls still failed checks. This campaign therefore explored density and temperature alongside geometry, while keeping the physics and acceptance limits fixed. [Grounding and invariants][goal]; [strategy][trail]

## Story in one picture

| Step | Engineering consequence | What the evidence supports |
|---|---|---|
| Explore geometry, coil ampere-turns, density and temperature together | Changes magnetic field, fusion output, heating demand and exhaust loading together | Passing selected designs under the existing equations |
| Declare conductor reserve, cavity space and cooling loops | Buys current margin and provides represented fit/flow capacity | Conditional accommodation, with incomplete installed costs |
| Perturb the selected design in both directions | Smaller major radius encounters field limits; larger radius encounters exhaust heat limits | A narrow sampled neighborhood |
| Retain the frozen controls and adverse results | Keeps the new scenario separate from the prepared comparison | No retrospective repair of the comparison |

This causal table connects the changed inputs to the bounded conclusion; it does not claim new physical qualification. Sources: [matched mechanisms and margins][report], [control preservation and independent checks][review].

## Research learnings

### The positive result comes from exploring operating choices

No new source extraction or material-performance law was introduced. The accepted learning is that the current exact-profile model admits a conditional sampled neighborhood in a different declared domain from the earlier negative search. That earlier result remains valid within its own scope. [Learning L-001][learnings]; [native record][record]

### Field and exhaust heat squeeze the local band

Changing radius changes both peak magnetic field and plasma performance. Holding other inputs at the anchor, smaller radius eventually fails field; larger radius eventually fails divertor heat. Restoring density or temperature separately to their reference values also loses the divertor pass. [Answer][answer]; [matched mechanisms][report]

| One input restored to its reference value | Result with other anchor choices held |
|---|---|
| Major radius | 109.895 MW auxiliary demand; heating, divertor and wall-load failures |
| Minor radius | 108.525 MW auxiliary demand; heating failure |
| Peak density | 10.151 MW/m² divertor load; divertor failure |
| Peak ion temperature | 10.274 MW/m² divertor load; divertor and wall-load failures |

These matched interventions show why the operating choices matter. They are individual comparisons, not an optimization proof. Source: [native report, Matched mechanisms][report].

## Model changes

No physical equation, model default, acceptance limit, executable, or frozen comparison rule changed. The campaign added a study, verification records, a map, and a bounded interpretation. Source and executable continuity were independently checked. [Final round assurance][review]; [trail][trail]

The study changed explicit inputs. The conductor multiplier buys inventory rather than improving material performance. Plasma profile exponents stayed at 0.35/1.2; plasma, cooling and calendar calculations remained active. Exact multiplier-1.0 controls retained their near-zero current failures. [Answer][answer]

## Study results

### The anchor passes, but nearby margins become small

| Selected input | Anchor |
|---|---:|
| Major / minor plasma radius | 11.251748 / 1.490886 m |
| Coil ampere-turns | 12.217184 MA-turn |
| Peak electron density | 4.892468 × 10²⁰ m⁻³ |
| Peak ion temperature | 14.035596 keV |
| Radial exterior allocation / transverse clear cavity | 0.65 / 0.65 m |
| Representative helium cooling loops | 18 |
| Purchased conductor-inventory multiplier | 1.01 |

This table identifies the scenario behind the passing anchor; values are rounded for reading. Full-precision inputs and held assumptions are retained in the [native record][record] and summarized in the [answer][answer].

| Available margin | Anchor | Minimum among passing tested neighbors |
|---|---:|---:|
| Peak field below 24.9 T | 0.513786 T | 0.026062 T |
| Divertor load below 10 MW/m² | 0.291669 MW/m² | 0.031533 MW/m² |
| Installed heating headroom | 12.894671 MW | 3.358450 MW |
| Local winding-pack fit | 125.032 mm | 112.149 mm |
| Per-loop flow headroom | 68.503 kg/s | 58.343 kg/s |

This comparison shows how available headroom contracts around the anchor. The minima need not occur at the same neighbor. Source: [answer's margin table][answer]; [native report][report].

All seven continuous axes had passing tests on both sides; both adjacent integer loop counts and all sixteen combined perturbations passed. Radius changes of ±1% passed. At ±2%, the smaller-radius case failed field and the larger-radius case failed divertor heat. These are finite tests, not certification of every intermediate design. [Answer][answer]; [independent result assurance][review]

### The map shows evaluated points, not a filled feasible area

![Native evaluated-point map of major radius and coil ampere-turns](../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/feasibility-map.png)

The plot shows the field/heating tradeoff with other inputs fixed at the anchor: 44 passing, 210 failing and 2 invalid-power-account locations. The reference marker projects a different configuration onto these axes. Blank space has no feasibility claim. Sources: [native map account][report], [plot data][mapdata], [independent visual and numerical checks][review].

### Numerical verification has explicit boundaries

The search screened 835 unique coordinates in 837 calls, retaining 121 refusal calls. Generated execution covered 334 selected cases plus a separate baseline. Selection favored informative cases and passing neighborhoods; the pass count cannot estimate the feasible fraction of design space. [Report][report]; [native record][record]

Independent review checked 75,484 mapped scalar comparisons and reconstructed 6,680 native screen verdicts. Six strict-relative near-zero differences and three native/oracle current-sign disagreements persisted at multiplier 1.0. The generic strict verifier refused the known boundary; a separately labeled all-point check documented the exceptions. Sixteen scalar channels lacked independent mappings. [Review][review]

## Outcome and follow-on issues

- **Owner decision:** “ok please close the goal”. The owner closed the reviewed bounded answer; suggested additional neighborhood checks remained prospective follow-up. No further round was opened. [Closure][close]
- **Agent recommendation:** Proceed to the prepared conditional ARIES comparison when separately authorized. The frozen r2 package remains unchanged and ARIES remains sealed at this cutoff. This study supplies a separate conditional result. [Answer][answer]; [closure][close]
- **Breeding remains unresolved:** The tritium breeding ratio, tritium produced relative to consumed, is held at 1.074. It passes the authored 1.05 floor but falls below the calculated requirement of 1.190. A screen pass therefore does not establish fuel self-sufficiency. [Answer][answer]
- **Cost remains conditional:** Modeled net output is 1010.112 MW and levelized cost of electricity, lifecycle cost per unit energy, is $150.43/MWh. Complete manufacturing, larger accommodation and added cooling installation remain unpriced; mixed-year prices persist. This is neither a complete plant price nor an economic optimum. [Report][report]
- **Hardware remains unqualified:** Fixed magnetic shape/topology and transport assumptions do not establish a new equilibrium or buildable coil. The anchor's 24.386 T peak exceeds the cited conductor measurements' approximate 24 T extent. Field-angle transfer, structures, divertor deposition, cooling layout and reliability remain conditional. [Answer][answer]
- **Unsupported conclusions:** Neither a continuous feasible region, global feasibility boundary, physical qualification, nor complete economic viability follows from these samples. Software consistency and implemented screens answer narrower questions. [Native record][record]; [review][review]

## Evidence and visual index

- [Goal][goal]: owner question, adopted campaign scope, assumptions and reserved decisions.
- [Trail][trail] and [owner closure][close]: task outcomes, final review and formal close ruling.
- [Accepted learnings][learnings]: conditional neighborhood, competing limits and interpretation boundaries.
- [Answer][answer]: configuration, quantitative margins, caveats and recommendation.
- [Independent review][review]: pre-execution, result and final-publication assurance.
- [Native study record][record] and [report][report]: committed study at `1394d43d1cfd362dfa608225455c823bf977e632`; inputs, execution, results and verification scope.
- [Plot data][mapdata] and [standalone SVG][mapsvg]: fixed-configuration evaluated-point map. The inline PNG above is the retained native visual.

[goal]: ../orchestration/goals/pre-reveal-feasible-neighborhood/goal.md
[trail]: ../orchestration/goals/pre-reveal-feasible-neighborhood/trail.md
[close]: ../orchestration/goals/pre-reveal-feasible-neighborhood/trail.md#owner-closure--2026-09-17
[learnings]: ../orchestration/goals/pre-reveal-feasible-neighborhood/learnings.md
[answer]: ../orchestration/goals/pre-reveal-feasible-neighborhood/answer.md
[review]: ../orchestration/goals/pre-reveal-feasible-neighborhood/evidence/independent-review.md
[record]: ../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/record.md
[report]: ../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/report.md
[mapdata]: ../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/map-data.csv
[mapsvg]: ../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/feasibility-map.svg
