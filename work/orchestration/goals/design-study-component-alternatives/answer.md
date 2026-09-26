# Matched conversion alternatives: partial result, implementation stopped

**The steam-versus-Brayton economic question remains unanswered.** The audits and native controls establish a plausible common source boundary and identify the required component additions. They do not establish a preferred technology. No new comparison assembly, integrated package or main study has run.

The final design review found that the proposed source-heat and Brayton pressure-ratio searches would solve physical closure outside the model. That conflicts with `modeling_project/STUDY_POLICY.md` §§3 and 5.3. The final permitted design submission therefore returned findings. The runbook's revision cap stops dependent implementation; formal goal and WI-096 closure remain with the owner. See the [independent review](evidence/design-review.md) and [trail](trail.md).

## What the comparison would hold equal

The starting source is the existing Stellaris helium primary-loop model: 14 primary paths, 8 MPa nominal pressure, helium heated from 573.15 to 773.15 K, and the inherited circulation-loss law. At its original design point, 3125.932 MW of source heat plus 175.281 MW of fluid work delivers 3301.213 MW to the conversion equipment. These are model outputs, not reference net-electricity substitutions. The retained C-1 Brayton assembly and Stellaris steam assembly use different downstream auxiliaries and costs, so their whole-plant outputs cannot directly answer this component question.

The proposed comparison includes the connecting heat exchangers, salt equipment where required, conversion machinery, water circulation and heat rejection. It excludes reactor, fuel and primary circulation equally. Its economic metric would be **conversion-subsystem cost per net MWh**, with equal finance and source conditions within every pair. The [boundary diagram](evidence/comparison-boundary.svg) shows the proposed assemblies; it is not an implemented-system result.

## What was established

### Three thermally consistent source candidates

An unchanged primary-loop calculation and independently checked counterflow exchanger calculation agree at the following diagnostic points. IHX circuit count is an independently chosen hardware offer; the matching heat input was located in a scalar diagnostic. This is not an approved study execution route.

| Diagnostic identity | IHX circuits | Source heat, MW | Delivered heat, MW | Required return, K | Primary flow margin per path, kg/s |
|---|---:|---:|---:|---:|---:|
| `source-coupling-probe#n10` | 10 | 2706.009 | 2819.514 | 564.761 | 38.975 |
| `source-coupling-probe#n11` | 11 | 2886.207 | 3024.031 | 563.599 | 26.582 |
| `source-coupling-probe#n12` | 12 | 3051.706 | 3214.740 | 562.465 | 15.200 |

The reviewer reproduced every retained loop channel. The independent effectiveness-NTU check of exchanger duty and return had residuals below 1e-10 MW and 7e-12 K. Full values and fixed inputs are in [source-coupling-probe.json](evidence/source-coupling-probe.json). No complete steam/Brayton branch was evaluated at these points. The original pressure-loss law includes the original IHX losses; applying it after changing exchanger layout imposes a total-resistance assumption. These matches do not qualify the substituted hydraulics or actual reactor turndown.

### Existing controls expose real interface limits

The [native readiness screen](evidence/readiness-screen.md) retained nine cases and their complete outputs or refusals. Three Brayton controls reproduced all 822 stored output values exactly. The original C-1 point needs about 31% modeled bypass; the retained near-matched point has a bypass near 1e-6. A neighboring point fails heat removal and return checks despite producing electricity.

On the steam side, reducing the named salt temperature alone breaks the heat join. Supplying 456 °C helium produces a nonpositive IHX terminal approach. Changing steam temperatures to 416 °C executes but fails the unchanged offered-condition checks. These results explain why a comparison cannot be made by swapping a heat number or applying a different efficiency to the existing plants.

### Equipment and cost gaps are explicit

- The steam salt circuit needs an offered pump arrangement that passes both flow and horsepower screens. Four pumps per circuit with a separately selected 250 kg/s design point are the proposed offer. The 225 kg/s offer fails flow at the first two source candidates; two/three-pump adverse offers remain in the acceptance scope.
- Brayton needs finite heat-transfer and water-pumping checks for its coolers, plus a recuperator whose effectiveness follows independently installed conductance. These are proposed additions, not demonstrated unchanged reuse.
- The steam aggregate already includes represented steam-generator and reheater children under WI-079's accounting assumption. Separate purchases would duplicate that scope. Matching source coefficients are labeled USD2025; the ARIES USD2004 prices have an explicit CPI purchasing-power conversion, with equipment-price uncertainty retained.
- Brayton service budgets, installed scope and recurring costs remain hypothetical. The design includes disjoint assumed accounts and a break-even cost-correction frontier. Even successful execution would not by itself support an unconditional economic recommendation.
- The inherited steam offer supports fewer operating choices than the Brayton model. The current scope could compare the supplied steam offer with tested Brayton offers; it could not claim equally optimized technologies.

Details: [comparison contract](comparison-contract.md), [candidate ledger](candidate-ledger.md), [cost audit](evidence/cost-audit.md), [monetary basis](evidence/monetary-basis.md), and [currency conversion](evidence/currency-conversion.md).

## Exact dependency and recommended continuation

The current [WI-096 design](../../../active/WI-096_matched-conversion-subsystems/design.md) keeps source heat and stage pressure ratio public, then proposes external root searches to enforce their physical equalities. Independent review finds that replaying the selected inputs preserves chosen hardware but does not satisfy the project's requirement to internalize coupled physical solves. Earlier agent-reviewed practice is not an owner waiver of that rule.

**Recommendation, agent judgment:** allow one additional design revision to put these closures into model-owned calculations, with solved quantities and independently selected hardware explicitly distinguished. Before implementation, the reviewer must also check the study policy's limit on additional handwritten solves and whether the revised scope remains modest. This recommendation is not an approved revision or a finding that a major new physical model is necessary.

If that continuation is authorized, the remaining work is native implementation and behavior validation, independent integration review, a sealed matched study, uncertainty checks, and the requested performance/cost figures. The retained specification, design, audits and probes supply the starting evidence. No new round has been opened to bypass the cap.

## Completion assessment

| Requested outcome | State |
|---|---|
| Named starting configuration, common boundary and candidate ledger | Recorded; conditional source candidates independently checked |
| Interface/cost audits and independent design review | Complete; final review has unresolved findings |
| Matched native branch implementation and integration | Not started |
| Verified performance and economic comparison | Unmet |
| Price/efficiency sensitivity and causal cost decomposition | Designed; not executed |
| Sealed main-study evidence | Absent; diagnostic receipts are not a substitute |
| Assembly SVG/PNG and reproducible script | Supplied, labeled proposed |
| Matched net/cost/delta plots | Absent because no matched results exist |
| Replay and proposed passage | Supplied for the partial result |

The result is useful source/interface readiness evidence, with a specific workflow dependency. It is not evidence that steam or Brayton wins, and it is not a completed economic comparison. [Replay instructions](evidence/replay.md) distinguish native controls, scalar diagnostics and figures. The [proposed passage](proposed-passage.md) states only what this record supports.
