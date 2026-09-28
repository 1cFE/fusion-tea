# Independent preliminary sizing-source review

Reviewer: fresh non-author agent `equipment_review`, 2026-09-18. Scope: Moscato 2018 source applicability to `models/library/analyses/mfe_primary_loop.sysml`. This is a preliminary source review, not approval of an equipment-cost implementation. Quarantine protocol followed; no barred source read. Findings and recommendations below are reviewer judgments, not owner requirements.

## Verdict

**Conditional conceptual transfer only; equipment sizing is incomplete.** The paper supports an exchanger area anchor, nominal operating conditions, and selected pipe dimensions. It does not establish complete circulator specifications, exchanger pressure-boundary construction, or a stellarator piping bill. No combined preimplementation pass is issued.

## Evidence examined

- `knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md`, sections 2.1.1–2.2.3.
- Original PDF page 6, retained at `work/orchestration/goals/primary-loop-sizing/evidence/source-pages/moscato-p6.png`: Tables 1–3, exchanger pass arrangement, temperature terminals and total area, hot-leg wall limit.
- Original PDF page 5, rendered independently to `/tmp/equipment-review-moscato-p5.png`: layout, nominal pressure/temperatures, pipe material and nominal diameters, total piping length.
- Original Figure 1 image `knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/images/tmpz3x8nelu.pdf-0004-07.png`: system schematic; insufficient machine-level topology.
- Independent arithmetic executed with `.codex-test/run python`; no model or source edits.

## Findings

### Circulators: count is established; topology is not

Image-checked Table 1 specifies two compressors per loop. Table 3 reports 6.8 MW (IB) and 7.5 MW (OB); surrounding prose discusses power per compressor. Two active machines per loop give 130.8 MW across three IB and six OB loops, close to the 129.4 MW difference between total exchanger duty and blanket heat. This supports two operating machines but cannot distinguish series from parallel. Neither inspected figure resolves the machine arrangement. A parallel assumption gives half-loop flow and full loop head per machine; series gives full-loop flow and divided compression across stages. Equal power split alone does not resolve topology. A costing design must cite another source or label its topology as an engineering assumption and assess the resulting applicability of its compressor cost method.

### Exchanger area: a defensible geometric anchor

Table 2 gives tubes **per pass**, with two tube passes and two shell passes. Using outside surface area `A = 2*pi*Dext*L*N_per_pass`, the image-checked inputs produce:

| Quantity | IB | OB |
|---|---:|---:|
| Duty, MW | 208.1 | 267.8 |
| Bundle length, m | 12.2 | 11.6 |
| Tubes per pass | 5801 | 7426 |
| Tube outside diameter, mm | 19.05 | 19.05 |
| Derived outside area, m² | 8471.06 | 10310.69 |
| Area/duty, m²/MW | 40.7067 | 38.5015 |

Three IB plus six OB units give 87277.32 m², matching the paper's approximately 87300 m². Omitting the second pass halves the area incorrectly.

Helium terminals are 500/287.7 °C (IB), 500/289.3 °C (OB); HITEC terminals are 270/465 °C. Counterflow terminal LMTD is 25.3746/26.3758 K. Consequently `Q/(A*LMTD)` is 968.13/984.73 W/(m² K). This is an **effective UF**, absorbing the unknown multipass correction factor; it is not an independently established film-based U. A fixed effective UF is a permissible stated conceptual assumption near these conditions and with equivalent exchanger configuration. Fixed area/duty is a weaker assumption because it also freezes temperature driving force. Neither proves performance across changed helium flow, salt temperatures, or geometry.

The existing model solves compressor inlet temperature but does not prove an exchanger can attain it. Use that solved temperature as the helium cold terminal; require positive terminal approaches to the adopted secondary temperatures. Do not silently reuse reference LMTD when compressor work changes. No salt-flow, fouling, multipass correction, tube-wall, or material design is supplied here.

### Pressure boundary and layout: partial evidence

Page 5 confirms 8 MPa nominal helium operation, AISI 316L(N) ex-vessel pipework, nominal hot/cold legs DN1300/DN1100 and approximately 4 km total piping. Page 6 gives hot-leg thickness **up to** 65 mm. These are not pipe inner diameters, universal wall thicknesses, design-pressure ratings, or exchanger shell/tube material specifications. The full 4 km includes a branched distribution network; multiplying it by a main-leg section cannot be represented as a source-derived steel mass.

The source layout serves a segmented tokamak with upper-port routing. Its counts and total length do not establish stellarator layout. A transferred layout must remain an explicit representative assumption with uncertainty. Resizing pipe diameter or length changes hydraulic resistance; it conflicts with retaining the present model's fixed-reference pressure-loss law unless that inconsistency is addressed.

Finally, the original Table 2 itself prints exchanger pressure drop units as MPa. Table 3 repeats the same numbers as kPa, consistent with the 8 MPa circuit. Use 87.9/85.1 kPa and record this source inconsistency; it is not merely an extraction error.

## Combined-review conditions

Review the actual costing design for: explicit operating topology and per-machine flow/head; geometry-derived exchanger area and thermal feasibility; pressure/material/correlation limits; an honest pipe scope; installation and price-year boundaries; and prevention of duplicate costs. Missing specifications or unsupported cost correlation domains remain review blockers, even if equipment counts and area arithmetic pass.

### Clarification: conceptual pricing versus physical qualification

An explicit `[AGENT]` assumption of two equally loaded parallel circulators is acceptable as the definition of a conceptual costing case while the hydraulic law remains per loop. For pricing, the design must propagate half-loop mass flow, full loop pressure rise, the corresponding inlet volumetric flow/density, and half-loop power to each machine; establish that the selected cost source covers comparable helium pressure, temperature, power and construction; and state whether motors, drives and installation are included. Topology uncertainty must remain visible because a series alternative changes flow and head even at similar power. A power-only cost method may suppress that effect mathematically without demonstrating its insignificance.

Physical qualification would additionally need a supported machine selection or performance map, operating margin, control/load-sharing scheme, piping/valve arrangement and a mechanical pressure/temperature design basis. Those are not prerequisites to an honestly bounded conceptual estimate, but their absence prevents calling the equipment qualified or the arrangement source-proven. A pricing method that itself requires these specifications cannot replace them with equipment count.
