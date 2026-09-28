# T-001 hydraulic source account

Investigation, 2026-09-16. Findings and proposals are `[AGENT]`, not independent certification. Quarantine protocol read; no barred content or external retrieval used. Original PDF page 6 visually checked against extraction.

## Source establishes design points, not hard capacities

[Moscato §§2.1–2.2](../../../../../knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md) specifies 2025.7 kg/s removing 2101.7 MW at 8 MPa and 300→500°C. Nine independent circuits comprise three inboard (IB) and six outboard (OB) loops. Each IB loop serves six sectors; each OB loop serves three. These are different hydraulic circuits, not nine identical units.

[Original PDF p.6, Tables 1–3](../../../../../knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/raw.pdf) supplies:

| Per-loop quantity | IB | OB |
|---|---:|---:|
| Compressors / IHXs | 2 / 1 | 2 / 1 |
| Hot / cold manifolds | 12 / 12 | 9 / 9 |
| Blanket pressure loss, kPa | 214 | 174 |
| External piping loss, kPa | 62 | 56.6 |
| IHX loss, kPa | 87.9 | 85.1 |
| Serial path total, kPa | 363.9 | 315.7 |
| Circulator unit power, MW | 6.8 | 7.5 |
| IHX duty, MW | 208.1 | 267.8 |
| IHX helium inlet/outlet, °C | 500 / 287.7 | 500 / 289.3 |
| Tube count per pass / bundle length, m | 5801 / 12.2 | 7426 / 11.6 |

Each loop has one hot leg, cold leg and cold header. Tube outside diameter is 19.05 mm; tube bore is absent. Table 2 prints MPa for the IHX losses; Table 3 prints kPa. Preserve this source inconsistency and use Table 3. Total IHX duty is 2231.1 MW; circulator power totals 130.8 MW. Their 129.4 MW heat increment supports fluid-work recovery but does not resolve motor efficiency.

## Existing transfer and its limits

[Plant bindings](../../../../../models/designs/stellarator_09/stellarator_plant.sysml:1140) turn 2025.7/9 = 225.0778 kg/s into a representative rating and size fourteen loops. This is a declared reference-flow screen, not a manufacturer maximum. Identical parallel replication is a model assumption. Source §3's eight homogeneous loops belong to a changed blanket/IHX architecture at approximately 520°C; they cannot justify identical replication of the old circuit without qualification.

The current 329.187 kPa resistance is weighted by IHX duty, not measured branch flow. The IHX temperature spans differ. Using current cp and those spans infers approximately 188.76/244.75 kg/s per IB/OB loop and 2034.79 kg/s total, 0.45% above the printed total. These are derived checks, not new flow ratings. Preserve representative averaging rather than claiming exact branch reconstruction.

## Supported next comparison

Retain the existing thermodynamic chain and vary its explicit integer loop count. No new hydraulic equation is needed for that conditional diagnostic. Pipe-area changes remain an evidence gap: the source's DN1300/DN1100, approximately 4 km total piping and hot walls up to 65 mm do not establish exact bores, per-loop routing, blanket-channel geometry or an IHX transfer law. Changing external pipe area alone would not remove blanket or exchanger resistance.

Sixteen representative loops are sixteen averaged modules, not replication of the source layout. Whole-layout replication adds nine loops; preserving only the IB:OB ratio allows three-loop groups. Neither establishes stellarator routing. Publish loop, compressor and IHX counts and installed reference duties. IHX feasibility needs positive terminal approaches and `UA_required=Q/LMTD`, corrected for two-pass geometry. Source area (~87300 m²) and nominal duties do not prove off-design capacity. Routing, compressor maps, drive efficiency, exchanger coefficients and equipment costs remain unresolved; enlargement remains conditional.
