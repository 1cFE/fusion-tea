# T-001 — Composite tape procurement basis

## Recommendation

[AGENT] Convert the model's existing composite `tape_volume` to purchased tape metres with `L_tape = tape_volume / (tape_width * tape_thickness)`. Use 6 mm width and 56 μm total composite thickness. Width is Stellaris-specific; applying Molodyk's measured 4 mm product construction at 6 mm width is an explicit transfer assumption. The thickness includes substrate, buffers, REBCO, silver and copper stabilizer. Charge the resulting length once for the complete purchased tape; retain the existing separately inventoried external copper jacket, solder, steel and helium.

[AGENT] Use an explicit assumed price per metre of this 6 mm composite product. A convenient transparent starting scenario is $30/m of 6 mm tape (equivalent to $20/m at 4 mm width under proportional-width pricing). This is an illustrative engineering price assumption, not a sourced market price or a supplier quote. No price was fitted to the entering magnet cost. Absolute price choice is independent of the geometric conversion and should remain a visible sensitivity input.

## Evidence inspected

| Claim | Primary evidence and verification | Force and limitation |
|---|---|---|
| Winding pack contains 9% tape stack, 35% copper jacket, 12% solder, 36% steel and 8% helium | Original Table 7 image: `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png`; visually inspected | Source fact. Fractions total 100%. The extraction's text table is wrong. |
| Unit cell contains a 6 × 6 mm tape stack and has a 20 × 20 mm cross section | Original Fig. 40 images: same directory, `stellaris-high-field-quasi-isodynamic-stellarator.pdf-21-1.png` and `stellaris-high-field-quasi-isodynamic-stellarator.pdf-21-2.png`; visually inspected | Source fact. 36/400 = 9%, consistent with Table 7. The extraction's 35 × 20 mm cell is wrong. |
| Actual tape width is 6 mm; coil 0 uses 807 km without grading, 167 km with perfect grading at 80% operating/critical current | Original Stellaris PDF `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, printed page 24 left column; rendered and visually inspected. Original Table 8 image: iter-01 `images/page_022_table_0.png`, visually inspected | Source fact. Perfect grading locally replaces superconducting tape with copper tape or compatible stabilizer. Published reduced lengths are not a scalar correction to fixed material fractions. |
| Total composite thickness is 56 μm for the 40 μm substrate product, with 5 μm copper per side | Molodyk et al., Scientific Reports 11:2084 (2021), `knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf`, printed page 4, Fig. 4 caption; rendered and visually inspected | Source fact for that 4 mm product. Applying the same thickness to Stellaris 6 mm product is an agent assumption. |
| Tape is a composite, including substrate and copper | Same source, printed page 7 Fig. 6; original extracted image `images/tmpcqui2wme.pdf-0007-01.png`, visually inspected | Hastelloy C276 substrate; oxide buffers; REBCO; silver; copper. Figure offers 40, 60 or 100 μm substrates. The chosen 56 μm construction is one product, not all REBCO tape. |
| Current density in this source is based on the full wire cross section | Same source, `output.md:17,51,77` and original p. 4 Fig. 4 | Distinguish composite engineering current density from superconducting-layer current density. |

No barred source was read. The quarantine protocol was read before source investigation. No external acquisition was needed. Original page renders used for visual checks are scratch in `/tmp`; the durable witnesses are the existing original PDFs and repository images cited above.

## Numeric conversion and price units

[AGENT DERIVATION] With `w = 0.006 m`, `t = 0.000056 m`, the tape cross section is `A_tape = 3.36e-7 m² = 0.336 mm²`.

- `L_tape [m] = 2,976,190.476190476 × V_tape [m³]`.
- At the held 9% tape fraction, `L_tape [m] = 267,857.142857143 × V_pack [m³]`.
- Example: 1 m³ of pack contains 0.09 m³ of composite tape and 267.857143 km of 6 mm tape. At the illustrative $30/m assumption, that is $8.035714 million of tape procurement.
- The 36 mm² tape stack contains an effective `36 / 0.336 = 107.142857` tapes at this construction. This is a continuous inventory approximation; a manufactured stack requires integer counts and tolerances.

[AGENT DERIVATION] A price stated in dollars per metre must name tape width and construction. For price `p_ref` per metre at width `w_ref`, proportional-width transfer gives `p_w = p_ref * w / w_ref`. That proportional transfer is a price assumption. Physical tape metres and reference-width-equivalent metres are different outputs: `L_ref = L_actual * w / w_ref`. Dollars per square metre of tape area convert as `p_m = p_area * w`.

[AGENT DERIVATION] A price `q` in dollars/(kA·m) converts to dollars/m only after declaring the critical-current rating and its conditions: `p_m = q * Ic_quote[A] / 1000`. The quote must state temperature, field magnitude, field angle, width, construction and criterion. Operating pack ampere-metres do not supply that rating. If `Iop/Ic_quote = u`, the same purchased inventory costs `q * operating_kAm / u`, not `q * operating_kAm`. This is dimensional bookkeeping, not a claim that operating conditions equal the quote conditions.

[AGENT] Procurement loss, spare lengths, minimum lot lengths and manufacturing yield are omitted (effective procurement multiplier 1). Add them only as named assumptions if required. Tape inside its complete purchased product already includes the substrate and stabilizing copper; adding those masses again would double count them.

## Meaning of changing reference pack current density

[AGENT DERIVATION] At fixed required ampere-turns and mean coil length, pack cross section and pack volume vary as `1/j_pack`. At fixed material fractions and tape construction, purchased tape length therefore also varies as `1/j_pack`. Higher reference pack density buys less tape. With a 9% tape fraction, composite tape operating current density is `j_tape,op = j_pack / 0.09`; individual tape current is `j_pack * 0.336 / 0.09` amperes when `j_pack` is in A/mm². For example, 120 A/mm² in the pack gives 1333.333 A/mm² in the composite and 448 A per tape. This is arithmetic, not a qualification of 448 A at the limiting field/angle.

[AGENT] That increase in tape current needs a physical interpretation. The alternatives are:

1. Consume operating margin on unchanged tape. At unchanged field, angle, temperature, strain and tape critical current, raising pack density raises `Iop/Ic` in direct proportion. A fixed field ceiling alone does not protect this margin. This arm needs a margin calculation or an explicitly conditional interpretation.
2. Improve tape critical-current performance at the same width and thickness. Better pinning/material quality can support greater current in the same cross section. At a held operating fraction and field envelope, required critical-current improvement equals the pack-density ratio. This is a technology scenario; a price premium or price change must be declared independently.
3. Improve local field alignment or reduce conductor temperature. Either may raise critical current without changing the tape's cross section. These are changes in orientation or thermal state and need corresponding engineering/thermal evidence; the current density alone does not represent them.
4. Change tape construction, fill fractions, packing, or grading. Thinner substrate, thicker REBCO, different copper, or replacement by stabilizer changes the inventory or its performance relation. These mechanisms are outside a sweep that holds construction and fractions fixed and cannot silently justify that sweep.

[AGENT RECOMMENDATION] For a bounded density sweep with fixed field envelope, construction, fractions and temperature, interpret the density multiplier as an assumed proportional improvement of tape critical-current capability at held operating margin. Label it an unqualified technology scenario. Retain independent procurement price scenarios; do not claim those density cases are feasible using only the existing field-envelope predicate. An unchanged-tape margin-consumption study is a distinct interpretation and needs an explicit current-margin bound.

## Native research return

Request: `knowledge/research/requests/REQ-TAPE-001.json`. Run: `knowledge/research/requests/runs/REQ-TAPE-001/20260915T160422939553/`. Native class: `REGISTERED`, with `pre_existing: true`; no queued candidates. One internal source search was logged; no external search or new source capture occurred. One existing-source registration attempt returned `duplicate`.

The native duplicate receipt and return leave `slug` and `path` null, although the registry command's actual response correctly identified `existing_slug = development_and_large_volume_production_of_extremely_high` and `existing_path = knowledge/sources/development_and_large_volume_production_of_extremely_high/`. The durable join is its source ID `2925a09fba687fbcf37d86bada14da7a0925e63a207b932650311de475f97f9b`, also present in `knowledge/SOURCE_INDEX.md`. The native record is preserved as produced; no research-seam tooling was changed. This report supplies the missing path explicitly.

No domain insight was minted or approved. The engineering recommendations above remain agent-originated assumptions for the consuming modeling work item.
