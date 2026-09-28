# Stellaris conductor reference reconciliation

Date: 2026-09-16 America/Los_Angeles (2026-09-17 UTC). Author: delegated clean source reader. Consumer: T-001. All recommendations and calculations below are [AGENT]; published evidence is attributed to its source rather than treated as an owner decision. This report changes no production model, acceptance limit or freeze.

## Finding

The entering absolute-current rejection is a conditional perpendicular-field reconstruction, not a reproduction of Stellaris's locally aligned cable calculation. The paper's maximum ungraded operating fraction is 60.5% for coil 0; the entering model gives 168.653%. Correcting the representative turn partition or choosing one of the paper's nearby peak-field values cannot close that difference. A quantitative decomposition into specimen performance, angle, local field and construction is not possible from the published coefficients and geometry available here. No fitted orientation multiplier is warranted.

The 112.709 reference-effective tapes are **not a published maximum-field conductor inventory**. The source has a 6 × 6 mm stack per 20 × 20 mm cell, 324 coil-0 turns and 47.6 kA turn current. Transferring the model's assumed 56 μm composite thickness to that stack gives 107.143 effective tapes. Even that number is an inferred continuous count, not a documented integer bill of materials. The model instead repartitions coil 0 into 308 turns at 50 kA, keeping pack area and tape volume. Both partitions give essentially the same current per tape.

## Original witnesses

The admitted Stellaris authority is `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, registered in `knowledge/SOURCE_INDEX.md:179`. Printed pp. 22–24 were extracted with the pdf-analysis skill. Pages 22 and 23 were visually inspected; durable renders and extracted text are in [conductor-pages](conductor-pages/). The page-23 original verifies Table 8 and Figs. 41–43. The page-22 original verifies Fig. 40 and Table 7. The page-24 text verifies the grading prescription.

The current normalization was independently checked against registered Molodyk et al., *Scientific Reports* 11:2084 (2021), `knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf`: original p. 3 Figs. 1–2 and p. 4 Fig. 4 were visually inspected; original pp. 7–8 were extracted. This confirms the prior performance report's main normalization and construction caveats.

A new bounded request investigated the source Stellaris actually fitted: Wimbush, Strickland and Pantoja, [SuperOx YBCO dataset v1](https://doi.org/10.6084/m9.figshare.13708690.v1), Stellaris reference [297]. The primary description and 20 K workbook were fetched through this investigation, screened before reading for the quarantine's barred terms and examined for unrelated design material. They concern only a short tape specimen. Their original bytes and API metadata are preserved under `conductor-pages/wimbush-*`. The downloads' MD5 values match the publisher API's `computed_md5` values. Registration failed twice at extraction; these are preserved research witnesses awaiting successful native registration, not registered model authority. See the acquisition disposition below.

## Source-to-model account

| Quantity or definition | Original evidence | Entering reconstruction | Classification and consequence |
|---|---|---|---|
| Unit cell and stack | Stellaris p. 22: 20 × 20 mm cell; 6 × 6 mm soldered stack in a 15 mm diameter copper former | Fixed 9% stack volume treated as complete composite tape volume | Physical interpretation/transfer. Table 7 says tape stack, not a counted tape bill. Inter-tape construction and exact tape thickness are not established. |
| Six unique coils | Table 8: turns 324/324/289/289/256/225; current 47.6/44.9/47.8/44.7/48.9/49.8 kA | Common maximum 50 kA and continuous turns from ampere-turns | Deliberate effective partition, documented in `stellarator_plant.sysml:192`. Source maximum is a lead-design bound, not every coil's operating current. |
| Coil 0 ampere-turns and pack | Table 8: 15.4 MA-turns, 360 mm square, printed 119 A/mm² | 15.4 MA-turns, 360 mm square, 118.8271605 A/mm² | Calibrated from rounded source pair. It reproduces geometry; it is not an independent prediction. |
| Full tape construction | Stellaris p. 24 identifies 6 mm tape width; thickness not specified in inspected conductor section | 6 mm × 56 μm; 56 μm transferred from Molodyk 4 mm thin-substrate product | Explicit material/construction scenario, not a transcription error. Source-specific exact count remains unknown. |
| Model reference and set counts | No corresponding Table 8 count | 112.708720 reference; 113.739339 set-effective | Distinct aggregate normalizations from shared inventory. Neither proves worst local conductor capacity. |
| Ungraded tape lengths | Table 8: 807/847/721/717/636/567 km per unique coil | 36.578571 million m whole set from 136.56 m³ pack, 9% tape and 56 μm thickness | Table 8 totals 34.360 million m over eight copies of each coil. Model is 6.457% higher. The common 25 m path and transferred thickness prevent unique attribution; do not change thickness merely to match total metres. |
| Graded tape lengths | Table 8: 167/161/146/134/131/118 km per coil; total 6.856 million m | Ungraded homogeneous fraction | Separate source case. Perfect grading locally replaces tape with stabilizer at fixed target operating fraction; its total length cannot be uniformly substituted into the ungraded current check. |
| Temperature | Stellaris p. 22: uniform 20 K analysis; 10–15 K suggested as possible future margin | 20 K fixed | Compatible temperature scenario. Cooling to a lower temperature is not a justified correction to this source case. |
| Current law | Stellaris p. 23: Zhang magneto-angular functional form [296], fitted to Wimbush dataset [297]; local tape alignment and Biot–Savart field calculation | Molodyk lot-average statistical normalization at perpendicular global peak field; orientation factor 1 | Unsupported transfer if interpreted as Stellaris local margin. Legitimate separately labeled scalar scenario. |
| Operating fraction | Table 8 ungraded maxima: 60.5/46.5/50.2/54.1/56.3/55.8%; graded 80% each | Reference scalar 168.653%; allowed 80% | Same numerical ceiling, different performance/spatial premises. Failure does not refute the published aligned calculation. |
| Current criterion | Wimbush description: 0.5 μV over 5 mm; fitted voltage curve | Molodyk absolute scenario lacks one verified common high-field criterion across all contributing labs | Wimbush criterion is 1 μV/cm. This closes the source-fit specimen criterion gap only; it cannot silently certify every Molodyk measurement. |

The Table 8 ampere-turns, turn currents and densities are rounded independently. For example, 15.4 MA-turns / 324 = 47.530864 kA, not exactly the printed 47.6 kA. Do not demand exact closure among rounded rows or silently choose whichever row produces a favorable result.

## Inventory, turns and quantitative attribution

The entering equations are in `models/library/analyses/mfe_conductor_current.sysml:4`; construction and density bindings are in `models/designs/stellarator_09/stellarator_plant.sysml:350` and `:452`. The initial current model landed at `09178a90`; current-driven sizing followed at `a8589d6b`. This report addresses the legacy reference and keeps the current-sized branch separate.

With tape area 0.336 mm² and tape fraction 0.09, the reference count is `N_ref = I_turn × 0.09 / (j_pack × 0.336)`. The set count is `L_tape/L_conductor`; conversion back to the reference multiplies by `f_set/f_wp_vol`. The inherited factors are 0.8701298701 and 0.8780864198. Series turns therefore cancel in the current loading; they must not be multiplied into parallel capacity.

At the entering 50 kA and 308-turn partition, `N_ref = 112.708720` and operation per tape is 443.621399 A. At the geometrical 324-turn partition, taking 15.4 MA-turns as anchor, current is 47.530864 kA and the cell holds 107.142857 effective 56 μm tapes. Operation per tape remains 443.621399 A. Using the independently rounded 47.6 kA source row instead changes that by only about 0.15%. Relabeling the effective partition is supported; increasing physical parallel capacity without additional volume is not.

| Attribution case | Per-tape critical current, A | Effective cable critical current, kA | Operating fraction | Allowed-current margin at 80%, kA |
|---|---:|---:|---:|---:|
| Entering 24.9 T, 50 kA effective partition | 263.038697 | 29.646755 | 1.686525 | −26.282596 |
| Change only peak to Fig. 41 coil-0 label 24.70 T | 264.314556 | 29.790555 | 1.678384 | −26.167556 |
| Change only peak to Table 8 coil-0 24.6 T | 264.958702 | 29.863156 | 1.674304 | −26.109475 |
| Change only peak to p. 23 prose 24.59 T | 265.023347 | 29.870442 | 1.673896 | −26.103646 |

At 24.6 T with the 6 × 6 mm/56 μm construction and printed 47.6 kA current, the scalar fraction is 1.676739. It still fails. The nearby field choices change the entering fraction by less than 0.8%, not the factor needed to approach 0.605.

For comparison only, the published 47.6 kA/0.605 implies a minimum local cable critical current of 78.677686 kA if the reported maximum ratio is taken literally for an ungraded coil of constant current. Its printed stack density 1323 A/mm² divided by 0.605 implies 2186.776860 A/mm² at the location of that maximum ratio. These are reverse calculations of published predictions, not independent measurements. The ratio 1.686525/0.605 = 2.787645 combines all changed premises. It is **not** an inferred orientation gain and must never be installed as one. The maximum-field location need not be the minimum-capacity location.

The complete reproducible arithmetic is [derive.py](conductor-pages/derive.py), with results in [arithmetic.json](conductor-pages/arithmetic.json). It imports no production model and makes no numerical fit.

## Source cases and internal peak-field differences

The page-23 Table 8 peak fields are 24.6/23.1/22.0/21.0/21.4/19.5 T. Fig. 41 labels are 24.70/23.33/22.02/20.90/21.37/20.19 T. The adjacent text gives 24.59 T maximum inside the pack. These are actual original-page discrepancies; the differences in coils 1 and 5 exceed simple rounding of the printed table. The caption calls Fig. 41 a surface-field plot from a magnetostatic FE calculation. The current-ratio calculation uses a separately described finite-section Biot–Savart calculation. The paper does not provide enough provenance to establish whether revisions, locations or calculation methods explain every discrepancy.

Keep Table 2's entering 24.9 T engineering envelope, Table 8's per-coil design table, Fig. 41's FE image and the prose 24.59 T as named witnesses. Do not mix their favorable numbers into an invented exact source case. The present report does not establish one corrected global field default.

## What the absolute normalization and new dataset establish

Molodyk p. 7 gives a lot-average 175 A per 4 mm at 77 K self-field. Page 4 Fig. 4 gives fitted lift 1.13 at 20 K, 20 T, with direct high-field and 12 T-extrapolated points mixed. Their product is 197.75 A/4 mm, rounded to the entering 200 A/4 mm, or 300 A/6 mm. The figure's 56 μm engineering-density axis is a construction conversion, not proof all underlying points share that construction. The transfer remains an inferred production scenario. The 20 K open-symbol data on p. 3 Fig. 1 extend to approximately 24 T; the approximately 31 T points are 4.2 K. The angular plot confirms a large, narrow parallel-field enhancement, but supplies no whole-coil angle map.

The original Wimbush v1 description identifies specimen SOX021, manufacturer sample #477-R (420-763), collected 20–28 January 2021: 2.5 cm long, 4 mm wide, laser-patterned to a 1 mm × 5 mm bridge. `Ic/w` is normalized to one centimetre width; `Ic` is the bridge's actual current. The fit is `V = V0 + V1 I + Vc (I/Ic)^n`, with `Vc = 0.5 μV` over 5 mm. Angle is from the sample normal; zero is perpendicular and 90° parallel. The description recommends the `Field` value and the measured `Hall angle` rather than assuming the commanded angle is exact. No composite thickness is stated.

The retrieved 20 K angular workbook contains 20 field sheets from 0 to **8 T**. At 8 T, its angular minimum is 985.71 A/cm at Hall angle 24.91°, and maximum 4865.33 A/cm at 86.56°, a ratio 4.935863. At 5 T, the ratio is 3.890823. These are actual measurements over this specimen's angular sweep, not a 24.9 T design multiplier. Linear transfer to 6 mm would multiply A/cm by 0.6; it would still carry width/bridge/product assumptions. The measured range confirms that using this dataset for the published approximately 25 T coil analysis involves extrapolating the fitted law beyond this workbook's 8 T endpoint. The publication's Fig. 42a vertical axis is **critical current [A/cm]**, although its caption calls the surface current density; reproducing a stack density therefore also requires an explicit tape-count/thickness conversion.

Stellaris does not print the fitted coefficients in the inspected magnet section, a full local field-and-angle dataset, tape stack count, or a traceable conversion from the fitted specimen to a manufactured cable. A new fit chosen merely to recover 60.5% would add unsupported assumptions. Source reproduction can carry the reported operating fractions as source-conditioned outputs, but must give them no independent prediction credit.

## Supported dispositions

1. Retain the existing scalar current calculation and its failed raw result as a clearly identified perpendicular-field, global-peak, assumed-construction scenario. It is conservative with respect to removing alignment benefit for a fixed matching specimen; it is not a certified universal lower bound covering construction, defects and manufacturing uncertainty.
2. Add or report the Table 8 coil-0 partition separately: 324 turns, 47.6 kA as rounded published current, 6 × 6 mm stack. Label any 107.143 count as derived using transferred 56 μm thickness. Do not describe 112.709 as the actual maximum-field cable inventory.
3. Keep ungraded and perfectly graded cases separate. Their source-predicted maxima are 60.5% and 80%; their total tape lengths are 34.360 and 6.856 million m. Neither is a measured installed procurement total. Grading leaves copper/stabilizer replacement and difficult local alignment manufacturing to be designed and priced.
4. Treat the global-current rejection as inapplicable to judging reproduction of Stellaris's local aligned-margin prediction unless the missing local calculation is implemented. Preserve the raw failure and an explicit unknown/not-reproduced status; do not convert unknown to pass.
5. Preserve peak-field source disagreement explicitly. Its tiny current-law effect is quantified above. It cannot justify a pass recovery or removal of the selected-envelope criterion.
6. Successful native registration of the new specimen dataset and independent source review precede any dependent model update. Remaining requirements are exact product thickness/count, local vector field and tape orientation along every relevant turn, fitted law and fit range, grading map, and quantified assembly sharing/degradation. Existing strain and field predicates do not supply these dependencies.

## Native acquisition disposition and integrity

Request: `knowledge/research/requests/REQ-STELLARIS-IC-01.json`. Run: `knowledge/research/requests/runs/REQ-STELLARIS-IC-01/20260917T045436514613/`. One direct-source search and two captures were recorded. Both captures failed with `extract exited 1`; native `return.json` is `OPERATOR_QUEUE`, zero registered sources, two named candidates. The two-capture budget was used, though the return's computed `limit_reached` field is null. Raw official attachments were obtained successfully; the unresolved issue is supported native extraction/registration, not source accessibility. No registration success or bounded negative is claimed. Registry records remain unchanged; acquisition receipts and raw evidence remain reviewable.

The official description has SHA-256 `93a2af6aa950a4fb292072832998186f61fa0978206597fd87afbe71ac01eeee` and publisher-matching MD5 `35d49333fee613b9a1f291d351e059e0`. The workbook has SHA-256 `8ae063a870223d5955ec08723577ef745eaf8f37fbd0da54f2d6479c14eed256` and publisher-matching MD5 `716ed7296d6794b5cb556b821fc7cb64`. Metadata endpoint: `https://api.figshare.com/v2/articles/13708690/versions/1`; original downloads: files 26344210 and 26340625 at `https://ndownloader.figshare.com/files/`. Description bytes are cp1252, not UTF-8; the original bytes are retained.

No sealed or barred artifact was read by this delegated reader. No production/freeze edits, temperature reduction, acceptance change or fitted performance multiplier was made.
