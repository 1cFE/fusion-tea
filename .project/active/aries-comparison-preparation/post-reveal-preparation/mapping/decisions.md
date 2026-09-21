# Reference-input decision

[AGENT] Prepare a partially reference-specified point with three supplied scalars: major radius 7.75 m, minor radius 1.70 m and peak ion temperature 11.83 keV. Keep the other five allowed controls and all other package inputs at their pinned values. This is the selected request for the next separately authorized comparison, not a request to execute now. No unresolved owner decision is needed to prepare this bounded case.

[OWNER] The owner delegated completion of mapping and replacement-package preparation on 2026-09-20. The physical interpretation and conservative choices below are agent decisions under that delegation, not owner-originated scientific claims. They remain challengeable against their evidence.

## Eight controls and their physical meanings

[AGENT] The new runner accepts eight controls. The original experiment accepted seven, including one aggregate ampere-turn control. Its contract and first failed attempt remain at commit `829539f5eb7fde217d18318d1646a5e47103812c`. The repaired model separates supplied installed reference-coil turns and per-turn operating current. Their product and magnetic field are calculated. Aggregate current alone cannot identify both controls; it is refused rather than decomposed.

| Control | Selection | Evidence and consequence |
|---|---|---|
| Major radius, m | Supply 7.75 | Lyon p708 Table IV, corroborated by Najmabadi p657 Table I. Nominal average radius is admitted as the model scalar. Nonaxisymmetric shape is not transferred. |
| Minor radius, m | Supply 1.70 | Najmabadi p657 Table I directly states averaged minor radius. Do not divide rounded aspect ratio into major radius. Nominal scalar correspondence does not establish equal volume or shape. |
| Peak electron density, m^-3 | Hold 5.06e20 | Lyon p708 gives central and volume-average densities; p702 Figure 12 peaks off-axis. Neither tabulated quantity is the permitted peak. This preparation does not reconstruct or qualify a peak from p701 Equation 3. No inferred peak or substituted profile. |
| Peak ion temperature, keV | Supply 11.83 | Lyon p708 Table IV gives central temperature; p701 assumes equal ion/electron temperatures; p702 Figure 12 has central temperature maximum. The magnitude matches; the source temperature profile is not substituted. |
| Radial coil exterior allocation, m | Hold 0.3 | Raffray p744 Figure 23 gives average winding and integrated support dimensions, not an exact single-coil exterior envelope. Original independent review supports holding. |
| Full transverse clear cavity, m | Hold 0.4 | Winding-pack width in Raffray p744 Figure 23 does not establish casing clear cavity including clearance. |
| Installed reference-coil turns, continuous | Hold 308 | Ku p677 describes three families of aggregate winding currents. No reference-coil identity and separate turns match is established. |
| Per-turn operating current, A | Hold 50000 | The aggregate family currents do not establish per-turn current. Do not solve either current control from reference field, performance limits, or a chosen output. |

[AGENT] The exact executable request is [proposed-reference-request.json](proposed-reference-request.json). The definitions, evidence requirements, missing/incompatible policies and claim effects are recorded for every control in [contract.json](contract.json). A `matched` record means the supplied scalar's quantity is matched within the interpretation above. It does not certify reference-equivalent geometry, profiles or whole-plant design. Incompatible scalar definitions remain refused by the runner.

## Held design and offer assumptions

[AGENT] [held-input-inventory.json](held-input-inventory.json) identifies all 701 held package inputs and the SHA256 of each generated input file. These are the repaired package's existing assumptions, not imported ARIES data. The five held comparison controls are included. The future run must use these exact input files and disclose its complete effective-input record. Missing source information never triggers sizing, fitting, optimization or repricing.

[AGENT] Held assumptions include conductor product and operating temperature; winding inventory and coil-family geometry; casing/support quantities; density/temperature profiles and plasma composition; blanket geometry and material choices; installed coolant, compressor, heat-exchanger, turbine, vacuum, cryogenic and fuel-processing equipment; facility allocation; availability/calendar choices; and supplied prices and financial inputs. Existing declared domains and engineering checks remain active. Source equipment capacity, Nb3Sn construction or Brayton-cycle details cannot silently replace the repaired model's supplied equipment.

[AGENT] Consequently this request tests the repaired model at three reference scalars with its held design. It cannot establish reproduction of the complete ARIES design, reference design feasibility, or an independently predicted reference cost. Any completed dependent result remains conditional. Supplied/held aliases earn no prediction credit. Unsupported domain results and undefined carriers remain unavailable according to the current overlay. No broadened support or new agreement criterion is introduced.

## Evidence and unresolved correspondence

[INHERITED: original independent review] Original author findings and independent review are copied verbatim in [evidence](evidence/index.json), with full commit paths and byte identities. They identify the differing coil families, average supporting-tube dimensions, source revision mismatches and 18-versus-24-coil inconsistency. These do not establish a single matched coil design. The source review is evidence for holding uncertain inputs, not proof that no additional published design data could ever exist.

[AGENT] I directly reinspected the committed images of Lyon pp701, 702 and 708 and Najmabadi p657. They support the three selected values and the density/profile distinction. The coil correspondence decisions rely on the retained independent review and its original source/image records. No new coil dimension or current was transcribed or inferred. [evidence/index.json](evidence/index.json) distinguishes the exact reviewed image bytes and their original locations under `knowledge/holdout/aries-cs/extracted/20260920-r3/` at the original evidence commit.

[AGENT] The source selection is final for this prepared request: prefer directly stated quantities with matching definitions and design revision; use the subsystem systems table for radius/temperature and the overview's directly tabulated minor radius. Retain published precision and report absent statistical uncertainty. Do not synthesize a new design by mixing subsystem revisions. Neither reference outputs nor desired agreement informed the held equipment, source values or model equations.

[AGENT] Genuine unresolved scientific correspondence remains: nonaxisymmetric geometry, hollow density/temperature profiles, coil-family identity, clear casing dimensions, conductor technology, component scope and thermodynamic equipment. The chosen disposition is to carry those as explicit limitations. Resolving them would require additional evidence or a separate modeling task; it is unnecessary for preparing this conditional request. Reference execution remains separately unauthorized.
