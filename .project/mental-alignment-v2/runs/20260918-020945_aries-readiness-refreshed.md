---
question: |-
  Please read this handoff for context: /tmp/handoff-20260917-075503.md

  As we are getting ready for the ARIES reveal, I'm trying to get a good summary of where we are. Please build a $my-mental-model-v2 

  What were the goals for this "hold-out set" of sorts? 
  - What was the "rubric" used for readiness?

  What was the intent for use stellaris? 
  What is a quick summary of the model evolution?
  What do we make of the outcomes? 
  - In reference to the stellaris design point (e.g. level of replication)
  - And generally with the assessed feasibility space

  Please summarize where we are now:
  - Assessment against the readiness rubric
  - Stats around the model fidelity; plus LCOE and feasibility 

  And then explain the proposed plan for "revealing" and "assessing" our model with ARIES.
date: 2026-09-18 02:09 UTC
policy: discovered
shape: checkpoint
evidence:
  - .project/mental-alignment-v2/runs/20260917-153751_aries-readiness.md
  - knowledge/holdout/aries-cs/PROTOCOL.md
  - .project/active/demo-depth-rubric/rubric.md
  - work/analysis/20260912-plant-closure-consolidated-grade.md
  - work/orchestration/goals/stellaris-reference-reconciliation/answer.md
  - work/orchestration/goals/stellaris-plasma-power-balance/answer.md
  - work/orchestration/goals/pre-reveal-feasible-neighborhood/goal.md
  - work/orchestration/goals/pre-reveal-feasible-neighborhood/answer.md
  - work/orchestration/goals/pre-reveal-feasible-neighborhood/trail.md
  - work/orchestration/goals/pre-reveal-feasible-neighborhood/evidence/independent-review.md
  - exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/report.md
  - exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/record.md
  - .project/active/aries-comparison-preparation/replacement-r2/evidence/final-review.md
  - .project/active/aries-comparison-preparation/draft.md
code_inspected: "Not inspected; native study records, goal decisions, rubric, and frozen-package review examined. No execution."
limits: "No sealed papers, barred source derivatives, old synthesis reviews or shared feedback read. Historical intent carried from the previous synthesis; no new depth grading, source-page verification or model runs."
---

# TLDR

The computer model estimates a fusion plant’s performance and electricity cost from design choices such as reactor size, magnet current, plasma temperature and cooling equipment. It began with **Stellaris**, a published stellarator design. **ARIES-CS** is another published design, kept aside to test the model against information that did not guide development.

The latest study found **103 passing designs among 334 selected calculations**. Passing means satisfying all twenty modeled engineering checks and a separate check that the power calculation is valid. It does not establish that the plant could be built or supply its own fuel.

One passing design was selected as the center for tests of small design changes. The study calls it the **anchor**. **43 of 45 nearby changes pass.** Its modeled electricity cost is **$150.43/MWh**: lifetime cost per unit of electricity, called levelized cost of electricity (LCOE). Some installed costs are missing. The design was selected for room below engineering limits, not minimum cost.

[OWNER] The owner closed the study on September 17. The ARIES papers remain unopened. [AGENT] The prepared comparison is useful, provided its original predictions and limitations remain visible.

Sources: [latest answer](../../../work/orchestration/goals/pre-reveal-feasible-neighborhood/answer.md), [owner closure](../../../work/orchestration/goals/pre-reveal-feasible-neighborhood/trail.md).

## Latest study results

An earlier search found no design passing every check among 71 selected cases plus a baseline. The new search also varied peak plasma density and temperature, alongside geometry and magnet current. **Equations, material performance and acceptance limits stayed unchanged.** The passing choices therefore do not change the earlier result.

The selected design uses **18 helium cooling circuits** and buys **1% extra superconducting conductor** beyond the current-sizing calculation. The study writes that purchase factor as **1.01**. The extra conductor costs money and takes up space; it does not assume better material performance. Modeled net electricity, after the plant’s own electricity use, is **1,010.112 MW**.

The two-dimensional plot varies reactor ring radius and coil current-times-turns, an input to magnetic-field strength. Other design choices stay constant. Its **256 points contain 44 passes, 210 failures and 2 invalid power calculations**. These points are part of the wider selected study, not 256 additional designs. The cost plot colors only passing points. Untested space between points has no feasibility claim.

The nearby tests show competing limits. Making the ring radius 2% smaller raises peak magnetic field beyond its limit; making it 2% larger makes exhaust heat at the divertor exceed its limit. The **divertor** receives and removes plasma exhaust heat. Both ±1% radius changes pass. Across passing nearby designs, the smallest spare allowances below the limits—called **margins**—are **0.026 T** for field and **0.032 MW/m²** for divertor heat.

The 103/334 result is not a percentage of all possible designs that work: the cases were deliberately selected. Nor do 43 nearby passes prove that every intermediate combination passes. The plot and nearby tests overlap and must not be added together.

There are important limits even for passing designs. **Tritium breeding ratio** means tritium produced relative to tritium consumed. The model assumes **1.074**, above its pass/fail minimum of **1.05** but below its fuel-cycle calculation’s required **1.190**. Passing that check does not establish adequate fuel production. The selected design’s field also exceeds the conductor measurements’ approximate **24 T** extent. Coil qualification and some manufacturing, space and cooling-equipment costs remain missing.

Sources: [native study report](../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/report.md), [full calculation record](../../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/record.md), [independent review](../../../work/orchestration/goals/pre-reveal-feasible-neighborhood/evidence/independent-review.md). Visual cue: show evaluated passing/failing points beside estimated cost at passing points, with held settings explained.

## Comparison with Stellaris

The two original Stellaris test cases still fail some checks. The newer passing designs use different inputs; they do not make the original inputs work.

The second archived comparison package, **r2**, saves the software, test inputs, results and comparison rules. They stay unchanged before the ARIES test. One saved case calculates through the model’s approximate geometry and field relationships; project records call this **forward**. The other supplies published geometry, plasma volume and field to test the remaining calculations; records call this **Table 5-conditioned**. Supplied values are not predictions.

Both saved cases use **14 cooling circuits and no extra conductor**, unlike the selected design’s 18 circuits and 1% extra. They still fail divertor heat, conductor-pack fit and a current-related check infinitesimally beyond its limit.

| Quantity | Published Stellaris | Saved: calculated | Saved: supplied |
|---|---:|---:|---:|
| Fusion power, MW | 2,700 | 2,609.0 | 2,603.4 |
| Stored plasma energy, MJ | 504.65 | 513.325 | 513.001 |
| Energy confinement time, s | 1.46 | 1.56872 | 1.57743 |
| External heating delivered to plasma, MW | Ignition: zero | 45.1725 | 44.0038 |
| Estimated electricity cost, $/MWh | No cost benchmark supplied | 162.871 | 162.947 |

**Ignition** means fusion heating sustains the plasma without external heating. **Energy confinement time** relates stored energy to transport heat loss. Similar-sized power and energy outputs do not reproduce the publication’s ignition result: even the supplied-value case needs 44 MW of external heating. Substituting published energy/confinement and fusion-heating terms leaves **46.5831 MW** required with modeled radiation retained. Missing source details prevent independent resolution; that difference is not a measured radiation error.

The reconstruction also uses generic geometry, approximate conductor behavior and helium-primary cooling. The publication instead uses water/lead–lithium (PbLi) blanket cooling with a separate helium-cooled first wall. The model does not reproduce one complete published plant.

Sources: [source comparison](../../../work/orchestration/goals/stellaris-reference-reconciliation/answer.md), [heating balance](../../../work/orchestration/goals/stellaris-plasma-power-balance/answer.md), [saved-case quantities in previous synthesis](20260917-153751_aries-readiness.md). Dropdown candidate: the signed heating calculation and what each term represents.

## Model assessment

We have a rubric to assess how much of the plant the model calculates, how calculations respond to design changes, and how detailed its costs are. This is separate from whether one design passes its checks. A target is the level the project expects that plant area to reach; scores are the highest fully evidenced level. Physics and cost scores never average.

| Level | Physics (P) | Structure and cost (S) |
|---|---|---|
| 0 | Behavior absent | Structure or cost account absent |
| 1 | Value assumed or supplied | One aggregate estimate |
| 2 | Calculated from inputs and checked in execution | Cost follows size/performance, with sources and account rollup |
| 3 | Calculated limits and subsystem interactions affect plant behavior | Separately sized parts with appropriate installation, replacement and maintenance costs |
| 4 | Interacting physics solved across subsystem boundaries and independently checked over a justified range | Design-based estimate covering procurement through maintenance, with uncertainty/maturity and reference validation |

**September 12, 2026 assessment: 17 of 23 scored entries met target; six were below.** Three other entries were confirmed not applicable. This remains the latest consolidated grade, not a fresh assessment of every later change. Entries below are **score / target**.

| Plant area | Physics | Structure and cost |
|---|---|---|
| Plasma geometry, fusion and operating point | 3 / 3 | Not applicable |
| First wall, blanket and shield | Build/wall load: 3 / 3; material life: 3 / 3; **breeding: 1 / 3** | 3 / 3 |
| Magnets, structures, supplies and cryogenic cooling | 3 / 3 | 3 / 3 |
| Heating, current drive, fueling and control | 2 / 2 | 2 / 2 |
| Divertor and plasma-facing maintenance | 3 / 3 | 2 / 2 |
| Vacuum vessel and vacuum systems | 2 / 2 | 2 / 2 |
| Heat transport and plant power balance | 3 / 3 | **2 / 3** |
| Power conversion, electrical equipment and heat rejection | 3 / 2 | 2 / 2 |
| Buildings, site and maintenance facilities | Not applicable | **2 / 3** |
| Fuel and tritium cycle | **1 / 2** | **1 / 2** |
| Availability, replacement, maintenance and decommissioning | 3 / 3 | 2 / 2 |
| Total cost accounting, financing, LCOE and estimate quality | Not applicable | **2 / 3** |

### Remaining gaps

- **Achieved tritium production:** calculate what the blanket produces instead of assuming a breeding ratio.
- **Cooling-system costs:** price installed pumps, pipes and heat exchangers individually.
- **Buildings:** derive sizes from layout and maintenance requirements.
- **Fuel inventory:** calculate operating stock and startup requirements.
- **Fuel-processing costs:** size and price equipment from the quantity of fuel handled.
- **Estimate quality:** state maturity and quantify uncertainty.

New passing designs do not fill these missing calculations. For example, the assumed tritium ratio can pass its chosen floor while the physics score for calculating that ratio remains below target.

### Model evolution

The initial model linked physics estimates to costs. Later calculations connected design choices to equipment and electricity output: more magnet current requires conductor that costs money and may not fit; coolant flow uses pumping electricity; coolant temperature changes conversion efficiency; component life changes replacement dates and downtime. Divertor heat and cooling-circuit capacity added explicit limits. Source comparison then separated supplied values from predictions and retained the unresolved ignition difference.

Sources: [rubric and area-specific criteria](../../active/demo-depth-rubric/rubric.md), [September 12 assessment](../../../work/analysis/20260912-plant-closure-consolidated-grade.md). Visual cue: show both the level definitions and the actual area-by-area score/target table; keep gaps visible.

## Calculation checks

The archived comparison package passed independent reproduction review and **97 extracted tests**. Its **174 comparison entries** include missing model outputs rather than dropping them. These focused checks do not erase historical failures in broader validation tests.

The generated Python executable—called **native** in the records—was compared with a separate Python implementation of the same equations, called the **oracle**. **75,484 numeric comparisons** meet the retained combined absolute/relative criterion. **6,680 pass/fail decisions**, reconstructed from the executable’s own numbers, agree with its reported results. Both saved Stellaris cases reproduce all **242 numeric outputs and 20 decisions exactly**.

Six strict-relative near-zero numeric differences and three current-related pass/fail disagreements remain when no extra conductor is purchased. The generic strict tool stopped at that known boundary. A separate comparison of all cases preserves the exceptions; it is not a generic strict pass. Sixteen numeric outputs lack a counterpart in the independent implementation. Agreement supports correct execution of the shared equations, not proof of their physical assumptions.

Sources: [study review](../../../work/orchestration/goals/pre-reveal-feasible-neighborhood/evidence/independent-review.md), [archived-package review](../../active/aries-comparison-preparation/replacement-r2/evidence/final-review.md).

## ARIES comparison plan

[OWNER intent carried from previous synthesis] The original aim was “80% methodology demo”: test structured SysML v2 modeling and generated calculation software, then compare with a design kept out of development. The wider motivation was what would need to be true for 1¢/kWh electricity.

Stellaris supplied the starting design, alongside W7-X and generic magnetic-fusion sources, but no complete cost benchmark. The **1costingFE** costing library checks calculation machinery at matching inputs. **ARIES-CS** tests how well the model predicts another design’s quantities and costs. This is one held-out published design, not a statistical test set.

[OWNER] The archived r2 package and a first comparison under its helium cooling assumptions are approved. Reveal remains a separate owner decision. Unsupported matches between model and reference technologies must remain explicit.

1. **Open and record the papers after authorization.** Keep extracted values and source citations in the designated records.
2. **Replace only seven permitted inputs:** major/minor plasma radius, peak density/temperature, coil current-times-turns and two coil-space dimensions. Record units and matching definitions. Missing inputs remain assumed and block dependent claims of an exact reference-design calculation.
3. **Run the saved software without tuning.** Keep density/temperature shapes, no-extra-conductor setting, fourteen cooling circuits and other frozen assumptions. Preserve every result and failure.
4. **Compare like quantities.** Assess subsystems, surrounding-layer order and cost-account coverage. Physical model/reference ratios use **[1/3, 3]**; component costs use **[0.5, 2]**. Missing/incompatible entries cannot pass. LCOE has no formal pass range. The formal verdict permits no monetary-year adjustment. Exclude or footnote inherited ARIES information in power-supply account C220107, including its effect on totals.
5. **Preserve the first report, then investigate separately.** Later tests may supply selected reference outputs to isolate downstream calculations; supplied quantities earn no prediction credit. The special Table 5 run remains a Stellaris check. Corrections, other technologies and optimization need separately identified versions.

Sources: [procedure summary](../../active/aries-comparison-preparation/draft.md), [published-package review](../../active/aries-comparison-preparation/replacement-r2/evidence/final-review.md), [reveal protocol](../../../knowledge/holdout/aries-cs/PROTOCOL.md), [historical intent](20260917-153751_aries-readiness.md). Visual cue: first report retained, later diagnostic reports separate.

# Judgment

[AGENT] The latest study shows that changing the modeled design can produce several nearby cases that pass the current checks. That makes the ARIES comparison useful. It does not make the two original Stellaris cases pass, reproduce published ignition, supply the six missing model capabilities or qualify a plant for construction. The owner closed the study; opening ARIES remains a separate decision.

# Renders

## 2026-09-18 02:31 — 20260918-020945_aries-readiness-refreshed_resumed.html

Path: `.project/mental-alignment-v2/runs/20260918-020945_aries-readiness-refreshed_resumed.html`.

Wall clock: 5m 54s (initial dispatch 02:25:23 UTC to initial completed render observed 02:31:17 UTC; one layout revision and browser checks followed).

Tokens: not measured.

Owner quality: not asked.
