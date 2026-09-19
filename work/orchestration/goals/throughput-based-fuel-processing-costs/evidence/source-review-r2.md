# Corrective source-transfer review

**Verdict: OWNER_GATE for adoption; conditional technical PASS for the proposed costing scenario.** [AGENT] The new primary engineering evidence resolves the first review's central scale-transfer concern. The joined evidence supports using ORNL's historical throughput law for a declared conventional plasma-exhaust cleanup and cryogenic isotope-separation estimate at the current demand. It does not establish that the present stellarator has the assumed feed or selected technology. Adopting that premise as its processing-cost basis is the remaining material scientific decision.

Reviewed 2026-09-19 against `knowledge/research/pending/20260919-092112_conventional-reactor-fuel-processing-transfer.md`. The first review remains in `source-review.md`. No model was changed, no price/accounting design was accepted, and no R10.S grade was assigned. All conclusions below are [AGENT] judgments unless identified as source observations.

## Original-source checks

| Primary evidence inspected | Finding |
|---|---|
| `knowledge/sources/ladd_et_al_iter_fuel_cycle_conventional_long_pulse/`; original `/tmp/fuel-iter-cycle.pdf`, pages 1, 3 and 4; page 3 also rendered and inspected visually | Nominal fueling is 50/50 D/T. The long-pulse processing requirement is 317 mol/hour for pulses up to 3000 s. The early roughly 100 mol/hour case is time-averaged and is not the applicable running-capacity comparator. The source describes front-end Pd/Ag permeators and impurity detritiation before isotope separation, and steady processing during long pulses. |
| `knowledge/sources/iwai_yamanishi_nishi_jaeri_tech_2000_002_iter_cryogenic/`; original images at PDF indices 3, 10 and 25 | The English abstract specifies a four-column cascade for 10000 s ITER operation. Section 3.1 specifies 320 mol/hour plasma exhaust, 5% H and D/T from 50:50 to 75:25 after noncondensible impurity removal. Table 1 explicitly identifies molecular species H2, HD, HT, D2, DT and T2. Its equal-D/T case gives atomic H/D/T fractions 5/47.5/47.5%. Water and neutral-beam feeds are separate 20 and 40 mol/hour streams. |

The Japanese design-conditions page and its table agree with the research report's numerical transcription. The English abstract independently establishes the operating duty and technology. Neither source is a commercial operating demonstration or a cost-law validation; those are not prerequisites for a conceptual S2 estimate.

## Why the engineering transfer now works conditionally

The current 12.911794045 kg D+T/day demand is approximately 107.6 molecular mol/hour using the source comparison convention of 5 g/mol. The JAERI equal-D/T plasma stream contains approximately 36.48 kg D+T/day, about 2.825 times the current isotope demand. These comparisons concern instantaneous processing duty. They neither assume annual availability reduces installed capacity nor claim that finite-pulse operation establishes year-round reliability.

The joined argument is now sufficient at conceptual-estimate depth: ORNL supplies an explicit reactor-oriented economic scaling method; TSTA supplies its historical equipment and expenditure basis; later reactor designs show that the same class of cleanup and cryogenic separation can be designed above the target molecular throughput. That is a reasoned engineering transfer beyond the small reference facility. It resolves the lack of process-scale evidence without treating Bartlit's local cost guidance as a hard maximum or inventing parallel trains.

Keep ORNL's 1.79712 kg D+T/day reference and its row-specific 0.3 exponent. The later sources do not provide a new exponent, a validated economic uncertainty interval, a certified upper limit or modern equipment prices. Extrapolation of the historical cost relationship remains a disclosed estimation assumption. That residual uncertainty is acceptable for the proposed conditional S2 scenario; it is not independently a blocker.

## The owner decision

The concrete choice is whether to adopt a conventional cleanup-plus-cryogenic-separation cost scenario for the represented plasma-exhaust function, conditional on source-like impurity burden, near-equimolar primary isotope feed, and conditioning to the TSTA separation reference. The current model verifies isotope flow, not those feed conditions. This choice makes a previously unspecified technology and an unverified feed premise control the processing-capital estimate. Given the owner's explicit reservation of major process-technology decisions, I classify adoption as material and owner-held.

This is narrower than committing a detailed plant design. The proposed scenario preserves existing loss/recovery assumptions, stock residence times and throughput; it adds no direct-recycle bypass or invented redundant train. Preparing its price conversion, account coverage and reviewable numerical example is within the authorized work. Scientific implementation as the plant's selected cost basis should follow the owner's acceptance of the premise. An owner acceptance would authorize the conditional scenario, not certify actual feed purity, recovery or commercial service.

Recommended owner-facing choice: accept this conventional, source-conditioned exhaust-processing estimate, with blanket extraction and other omitted functions clearly unpriced, or require a different process/feed basis before replacing the existing account. I recommend accepting the conditional scenario because its functions match the represented cleanup/separation role and the primary designs now support its scale. Retain its conditions explicitly in the model and reported results.

## Conditions for the next stage

- Price only the represented plasma-exhaust cleanup/separation boundary under this transfer. Blanket extraction, fueler rejects and additional recovered-isotope feeds are not silently included. If blanket T later joins the priced process, establish its conditioning and actual isotope-flow interface first. No fictitious D companion is warranted.
- State the source-like raw impurity burden and cleaned-feed requirement as external applicability conditions. Unknown impurity mass is not zero. Existing 99% functional recovery remains an assumption rather than a guarantee supplied by these sources.
- Preserve the source separation service and reference pressure/refrigeration class. Do not discount columns, products or cleanup duties merely because the functional model does not expose them.
- Complete dated price conversion and account coverage before a production estimate. General CPI escalation may be labeled a purchasing-power proxy; it does not establish modern equipment price. This review has not checked the proposed index or implementation.
- Explicitly identify what replacing the broad processing-plus-containment allowance removes. S2 can disclose unpriced containment, storage, transfer equipment, blanket extraction and other functions; it need not become S3 equipment decomposition. It cannot describe the two process rows as a complete fuel plant or imply omitted safety coverage remains costed.
- Verify the actual throughput-to-cost-to-plant-total chain and study response before seeking a fresh R10.S grade. Source acceptance alone earns no grade.
