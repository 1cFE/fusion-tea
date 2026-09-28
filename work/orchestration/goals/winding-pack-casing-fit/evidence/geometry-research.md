# Winding-pack and casing geometry evidence

Date: 2026-09-15. Researcher: delegated geometry reader. Status: evidence for independent preimplementation review; proposed screen assumptions are agent recommendations, not owner requirements or qualified device dimensions.

## Conclusion

The admissible Stellaris paper supports a nominal square winding pack whose face is tangential to the plasma. It does not establish the local casing cavity dimensions, external ground-insulation thickness, or assembly allowance needed to prove that the resized pack fits. A two-direction rectangular screen is useful only conditional on those independently supplied dimensions and on an explicit interpretation of the nominal pack envelope.

There is a source ambiguity inside that envelope: Figure 40 draws a 0.5 mm pancake insulation strip outside the vertical 20 mm cell dimension, while the prose and Table 8 use square 20 mm-pitch sizing. The screen must disclose this; the published pack size cannot be described as a verified fully insulated manufactured envelope.

## Evidence inspected

### S1: Stellaris primary paper

Registered source: `knowledge/SOURCE_INDEX.md:179`. PDF: `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, SHA256 `7fd72c1242ce3a17a9c4b9a4597fcb9ff5296b942b2d8343a0b463539d8d3865`. Lion et al., *Stellaris*, doi 10.1016/j.fusengdes.2025.114868. Original PDF pages 21–23 were rendered and visually inspected, including an enlarged Figure 40; pages 24 and 27 were read from direct PDF text. The accompanying extraction contains material errors, including altered cell dimensions, table fractions and orientation statements; it is not the numeric witness.

| Observation | Source location | Meaning for fit |
|---|---|---|
| Square winding packs; coil 0–5 side lengths 360, 360, 340, 340, 320, 300 mm. Turn counts 324, 324, 289, 289, 256, 225. | PDF p.22 prose and p.23 Table 8, image checked | Nominal section side equals 20 mm times square root of turn count. These are pack dimensions, not casing cavities. |
| Each turn is described as 20 × 20 mm, with a 6 × 6 mm tape stack and 15 mm diameter copper former. Figure 40 explicitly omits casing. | PDF p.22, Figure 40 and prose, image checked | Tape stack, composite unit cell, winding pack and casing are distinct geometry levels. |
| Figure 40 labels pancake insulation 0.5 mm. Its yellow strip lies above the vertical 20 mm arrow, whose upper endpoint is below that strip. Prose specifies insulation between pancakes and electrical contact between radial turns. | PDF p.22, Figure 40 enlarged and left-column NI paragraph | This is internal pancake insulation, not an external ground wrap. The figure does not reconcile its extra strip with the square nominal section in Table 8. |
| Pack orientation is decoupled from tape orientation. A flat pack face is tangential to the plasma; individual tapes align to local magnetic field. | PDF p.22 left column, paragraph beginning “We note…” | Define local section axes from the pack face and centerline. Do not rotate the pack automatically with the tape field-alignment angle. |
| Figure 39 labels 10350 mm tall, 6500 mm radial extent and 4820 mm toroidal extent for the first coil including casing. | PDF p.21, Figure 39, image checked | These whole-coil exterior spans do not give the local section cavity or wall thickness. |
| Table 8 explicitly defines its minimum distances with respect to the neighboring coil; casing-to-casing distances are separate from pack side lengths. | PDF p.23 Table 8 heading and rows, image checked | Inter-coil clearance cannot be used as pack-to-casing assembly clearance. |
| Local mechanical model treats plates and casing as separate contacting bodies without friction/clamping; global structural model assumes the winding pack, casing and support fully bonded. | PDF p.24 structural-integrity paragraph; p.27 Section 2.10 | These are analysis assumptions for different models, not measurements of a manufactured assembly gap. |

[AGENT inference] Table 8 current densities agree with current divided by nominal square section, e.g. 15.4 MA / (360 mm)² ≈ 118.8 A/mm², printed as 119 A/mm². Thus a side derived from the published engineering current density reproduces the nominal envelope. Adding the 0.5 mm strip repeatedly changes that interpretation and would require a justified layer-count/packing model. Adding 0.5 mm once around the outside misidentifies the source feature. Neither change is justified by this evidence.

### S2: W7-X manufacturing primary manuscript

**Title correction:** The retrieved PDF actually reads K. Riße for the W7-X team, *Experiences from Design and Production of Wendelstein 7-X Magnets*, 25th SOFT. The web search assigned this URL the title *The design of the superconducting coil system for Wendelstein 7-X*, and registration used that incorrect title before the captured PDF was inspected. Cite the actual title and hash below. The native registry has no metadata amendment command; the erroneous index heading/slug is a known metadata defect, not a different paper.

Captured extraction: `knowledge/sources/the_design_of_the_superconducting_coil_system_for/output.md`. Source URL: `https://pure.mpg.de/rest/items/item_2141097/component/file_2141096/content`. Raw/source SHA256: `a92c209b6949d9c4b4ce5e9797e07f71fa92309949f7156c74a5565d7f9522c4`. PDF pages 5 and 6 were rendered and inspected. The source contains W7-X manufacturing evidence; no barred design/cost datum was used.

- The manuscript distinguishes interturn/interlayer insulation from insulation against ground and specifies separate electrical tests. See extraction line 85, Section 3.
- Winding packs are embedded in steel casings with a sand-filled gap. The intended prestress depended on thermal expansion during assembly and operation; the production process did not achieve the intended prestress. See PDF pp.5–6, Section 2.4; extraction lines 67–71.
- The discussion reports specified 5 mm insulation reduced to 3 mm in the context of manufacturing defects and hand-applied insulation. It provides no defensible Stellaris ground-wrap default. See PDF p.5; extraction lines 49–57.

This supports separate insulation and embedding/assembly allowances, with temperature and tolerance states declared. It supplies no transferable Stellaris cavity dimensions or assembly-clearance value. Sand-filled embedding space should not be relabeled an operating air gap.

## Conditional screen recommendation

[AGENT] Retain the inherited nominal square pack side as `s`, explicitly described as the published homogenized pack-envelope basis with unresolved internal pancake-insulation reconciliation. Do not label it bare conductor. A fully manufactured fit verdict requires a dimensionally reconciled pack envelope from a drawing, CAD model, measurement or qualified packing definition.

[AGENT] Accept independent cavity interior dimensions `C_x` and `C_y` in the pack's local cross-section frame, normal to the centerline, with `x` along the plasma-tangential face and `y` normal to that face. Declare that the nominal pack and rectangular cavity share orientation and center; actual shaped/offset cavities need a more detailed check. For the square approximation, width and height are both `s`; retain two margins so an anisotropic cavity can bind in one direction.

[AGENT] Define external ground-insulation thicknesses `t_x,t_y` and nonnegative per-face assembly/tolerance allowances `g_x,g_y` outside that nominal envelope. Then `required_x = s + 2*t_x + 2*g_x`, `required_y = s + 2*t_y + 2*g_y`; signed total margins are `C_x-required_x` and `C_y-required_y`. Conditional fit requires both margins nonnegative, with zero denoting exact allowance contact. Symmetric per-face margins, if reported, equal half these total margins. State units and factor-of-two convention at the inputs.

[AGENT] Keep wall thickness separate. If a rectangular exterior diagnostic is useful, compute exterior dimensions from cavity plus two wall thicknesses; do not infer cavity from support mass, casing mass, coil bore or thermal surface allowance. Cavity dimensions held fixed while varying pack side produce a diagnostic screen; increasing the cavity along with every proposal would hide the intended fit boundary.

[AGENT] Any numerical cavity, external insulation or assembly allowance introduced now is an explicit scenario assumption. The evidence supports no nominal Stellaris value for these inputs. A screen pass establishes only local rectangular non-interference under those assumptions. It does not establish coil-to-coil clearance, insertion path, cold deformation, mechanical load transfer or a buildable magnet.

## Measurements that would resolve the gap

- A dimensioned local section of each coil type at limiting locations, including nominal/maximum manufactured pack envelope, pancake count and insulation inclusion convention.
- Minimum cavity width and height, fillets and obstructions, local orientation and offset from the pack centerline.
- External ground-wrap build, tolerance stack, embedding/filler specification and required assembly allowance.
- Temperature/load state for each dimension and expected differential contraction/deformation; assembly-path geometry if a full assembly claim is desired.

## Acquisition record and limits

Native request: `knowledge/research/requests/REQ-FIT-01.json`. Run: `knowledge/research/requests/runs/REQ-FIT-01/20260915T194514322676/`. Return class: `REGISTERED`. One query and two capture attempts were used, within the six-query/three-capture allowance. The first URL capture failed due to sandbox network access; an authorized public-PDF download followed by native local-PDF registration succeeded. `return.json` retains the failed URL attempt as queued because the seam does not reconcile it against the later local-file success; it is the same captured paper, not an unresolved access need. No new domain insight was approved or added.

The search stopped once the source distinction and missing Stellaris cavity dimensions were established for this bounded local screen. This is not a claim that no engineering drawing exists elsewhere. No model, generated package, goal state or PM state was changed by this research. Files are ready for coordinator review and commit; no commit was made by this reader.

## Coordinator alternative: inherited exterior radial allocation

[AGENT, conditional design alternative requested during review] If the existing `coil_t` radial-build input is explicitly interpreted as the available **exterior local radial allocation**, a cavity may instead be derived as `C_radial = coil_t - 2*wall_radial`. This preserves an independently held allocation while the pack grows; it is not a source-derived cavity. The reported inherited 0.30 m allocation is smaller than the source nominal 0.36 m maximum pack even before walls and external allowances, so this interpretation produces an honest reference failure and exposes a cross-model geometry inconsistency. Do not adjust the allocation merely to obtain a pass. The transverse cavity dimension still needs its own input or allocation. This alternative must be reconciled with the radial-build input's documented meaning before implementation; the research did not inspect or certify that model semantic.

The source's plasma-tangential pack face supports a local tangential/face-normal frame. Calling its normal “radial” is a declared approximation; a nonplanar coil's local plasma-facing normal is not globally the cylindrical radial direction everywhere. A conditional rectangular section can use these axes if the cavity alignment and station are explicit.

[AGENT, sensitivity only] If reviewers choose to explore omitted internal sheets, Figure 40 puts pancake sheets across the stack in the tangent direction (vertical Φ direction in its sketch); they are not a uniform exterior wrap. An assumed 18-cell stack with 17 internal sheets would add 17 × 0.5 mm = 8.5 mm in that one direction. This is not a verified correction: whether sheets are already represented in the nominal pack/current-density basis, and whether the bounding convention counts 17 or 18 sheets, remain unresolved. Adding 8.5 mm in both directions lacks support from this figure. A declared full-build allowance may express this uncertainty, but it must not turn the nominal source envelope into a confidently named bare-conductor section.
