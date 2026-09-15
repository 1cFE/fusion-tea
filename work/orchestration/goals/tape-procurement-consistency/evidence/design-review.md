---
Verdict: pass
Created: 2026-09-15
Related Artifacts:
  Design: ../../../../active/WI-060_tape-procurement-quantity-basis/design.md
  Spec: ../../../../active/WI-060_tape-procurement-quantity-basis/spec.md
---
# Independent source/math/interface review

**PASS for design readiness.** No blocking source, arithmetic or interface defect found. Implementation and study evidence remain to be reviewed.

## Original evidence

Read the quarantine protocol before source inspection; no barred source opened. Visually inspected the three Table 7/Fig. 40 images named in [the brief](design-review-brief.md), Table 8 (`page_022_table_0.png`), Stellaris original PDF printed p. 24, and Molodyk original PDF printed pp. 4 and 7. PDF figures were rendered locally and inspected, following the pdf-analysis image workflow. Source paths are recorded in [the research report](tape-basis-research.md).

- Table 7 gives tape/copper/solder/steel/helium fractions 9/35/12/36/8%. Fig. 40 shows a 6 × 6 mm stack in a 20 × 20 mm cell: 36/400 = 9%.
- Molodyk Fig. 4 explicitly gives 56 μm total thickness, including a 40 μm substrate and 5 μm copper per side. Fig. 6 confirms the composite layers. Applying this construction to Stellaris's 6 mm width is correctly identified as an assumption.
- Stellaris p. 24 distinguishes 807 km ungraded from 167 km perfectly graded tape for coil 0. Grading replaces tape locally with stabilizer. Those lengths cannot calibrate a reduction while retaining the proposed constant 9% purchased-tape fraction. The design makes no such reduction.

## Math and accounting

The section is 3.36e-7 m². At 136.56 m³ pack volume, the proposed inventory is 36,578,571.43 tape metres and $731,571,428.57 at the assumed $20/m. This is an independent geometric result, not a supplier quote or a reproduction of published graded lengths.

Envelope factor Q enters pack volume once. Direct dollars/metre pricing adds no second Q. Density scaling inversely changes tape and other pack materials. The unchanged-tape interpretation honestly leaves absolute current margin unknown; existing feasibility predicates cannot qualify it.

Composite substrate/stabilizer stay inside the tape purchase. External copper, solder, steel and helium remain separate. Existing material bindings consume winding-pack volume, excluding extra cryogenic volume. Winding work retains conductor metres.

## Interfaces, oracle and applicability

The proposed binding and migration inventory covers the current grade-price path and its consumers. The independent expanded oracle can catch drift from native intermediate volumes. Planned combined density/envelope cases, dimensional sensitivities, invalid-domain tests and fresh generation are adequate for readiness.

Keep the two set factors distinct: `f_wp_vol` represents summed pack cross-sections; `f_set` represents summed coil currents. Their reference ratio is 1.00914409. Thus set-effective tape loading also depends on `f_set/f_wp_vol`; `j_pack × tape_area/f_tape` describes the reference coil, not an exact set-average current. Count/circumference changes scale both inventories; independent factor changes alter their ratio. Fixed factors are acceptable transfer approximations. Include separate factor perturbations in implementation checks and retain this limit in study interpretation.
