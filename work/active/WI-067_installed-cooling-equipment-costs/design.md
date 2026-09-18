---
Status: draft
Created: 2026-09-18
Updated: 2026-09-18
Related Artifacts: spec.md; ../../orchestration/goals/installed-cooling-equipment-costs/evidence/round2/reference-sizing.json
---

# Conceptual cooling equipment estimate

[AGENT] Candidate design, not implementation release. Sources and quantitative price methods remain under investigation in goal Round 2. This document supplies explicit target specifications against which those methods can be evaluated. It does not require equipment qualification or a complete plant layout to support a conceptual estimate.

## Equipment boundary and ownership

The current primary heat-transport calculation remains the owner of total/per-circuit helium flow, pressure rise, compressor inlet temperature, fluid work, electric demand and exchanger duty. Equipment accounts consume those results. One plant-facing coolant total replaces supported overlapping C220200 scope; no priced equipment is added to the same unchanged allowance. Dedicated primary circulators, ex-vessel primary piping and the primary-to-secondary exchanger have distinct accounts. Secondary circulation, piping and transfer to the conversion system need an explicit boundary before replacing the intermediate allowance. The current source-HITEC exchanger is an analytical reference, not an owner-selected intermediate architecture.

The existing blanket owns in-vessel cooling structures. Avoid buying their steel again as ex-vessel piping. Buildings, magnet cryogenics, turbine and ultimate heat rejection retain their distinct CAS homes. Equipment connection labor and dedicated controls/drive scope must be normalized against existing plant-wide indirects and service allowances. See the reviewed `account-boundary-map.md` and `accounting-preimplementation-review.md` under the goal for actual equations.

## Concrete target cases

`evidence/round2/reference_sizing.py` under the goal derives the machine and exchanger specifications from retained executed demands. `reference-sizing.json` retains full precision, assumptions and all four cases. Its only physical transfer beyond the current model uses the independently image-checked source exchanger geometry/temperatures in Round 1's sizing review.

| Specification | Selected eighteen circuits | Same selected design, fourteen circuits | Saved r2 forward |
|---|---:|---:|---:|
| Assumed equally loaded parallel circulators | 36 | 28 | 28 |
| Mass flow per circulator, kg/s | 78.288 | 100.655 | 105.619 |
| Inlet volumetric flow per circulator, m³/s | 11.764 | 15.224 | 16.001 |
| Pressure rise per circulator, kPa | 159.303 | 263.337 | 289.951 |
| Suction pressure, MPa | 7.841 | 7.737 | 7.710 |
| Suction temperature, K | 567.221 | 563.325 | 562.325 |
| Electric power per circulator, MW | 2.410 | 5.136 | 5.937 |
| Required exchanger duty per circuit, MW | 167.440 | 219.352 | 231.267 |
| Conditional exchanger area per circuit, m² | 5,824 | 8,278 | 8,930 |

### Circulators

[AGENT] Two equally loaded parallel machines per circuit are a candidate conceptual arrangement, not a source-established topology. Each sees half the loop flow and full loop pressure rise. Inlet density is calculated at `p_suction = p_loop - dp_loop` and the solved compressor-inlet temperature, using the current ideal-helium properties. `R_specific = cp*(gamma-1)/gamma`; volumetric flow is mass flow divided by density. The current drive efficiency of unity makes electric and shaft/fluid powers coincide; a source cost curve requiring shaft power must consume the correct quantity and keep motor/drive scope separate. Zero-flow dormant operation and unavailable machine sizes need explicit domain handling.

A power-only cost method must be checked against flow, pressure rise, casing pressure, temperature, speed and construction. Mathematical membership in a horsepower range does not establish a high-pressure helium machine price. A series arrangement changes per-machine flow and pressure ratio, so it is a separate design sensitivity if source applicability supports both arrangements.

### Heat exchangers

[AGENT] Candidate thermal reference uses the source OB two-pass shell/tube configuration, HITEC temperatures270/465°C, and an effective `UF = Q_ref/(A_ref*LMTD_ref)`. The geometry-derived area is `2*pi*19.05mm*11.6m*7426 = 10310.69m²`; both passes are counted. The resulting effective UF is about984.73W/(m²K), including the unknown multipass correction rather than asserting an independently measured U. Actual target helium terminals are500°C and the current solved compressor-inlet temperature. Positive terminal differences determine the logarithmic mean temperature difference (LMTD), then `A = Q/(UF*LMTD)`.

All four reference cases have positive terminal approaches. This establishes conditional required area, not manufactured geometry or source-qualified off-design performance. Secondary pressure, exchanger alloy/tube wall, shell arrangement, fouling and salt flow remain missing. If the cost method requires several smaller shells, their count, area, pressure loss, connections and installation must be accounted for; dividing a large area by an arbitrary number to evade a cost-domain limit is unacceptable.

[AGENT] Independent review (`evidence/round2/reference-review.md`) confirms the arithmetic but requires separate required and installed areas. The conditional required area is only56.5–86.6% of the source OB module. A fixed-geometry case must price the installed10310.69m² module per circuit, retaining the reference hydraulic interpretation and reporting unused thermal area. A resized or modular exchanger case must establish its own flow passages and pressure losses before its smaller installed area changes the plant estimate. Required area alone is not a purchase quantity. The fixed-case diagnostic is not production code and needs explicit invalid/zero-input handling before reuse.

### Piping

[AGENT] Retain an explicit circuit piping schedule with separate hot leg, cold leg, branches/manifolds, valves, fittings, supports and insulation. Each line needs inside/outside diameter, wall or pressure class, material and a stated length basis. Nominal DN1300/DN1100 and “up to65mm” from the source are not enough to infer a full steel mass. Distinguish source dimensions, derived dimensions and assumed layout lengths in the exported quantities.

Two candidate approaches remain open: retain reference-capacity module geometry and charge per circuit, or derive pipe sizes from flow and a justified velocity/pressure-loss basis. The former retains the current hydraulic-law meaning but needs a source-backed module bill; the latter must reconcile changed resistance with the current hydraulic path rather than alter cost geometry alone. Layout sensitivity must propagate hydraulic consequences or clearly state the limited fixed-hydraulics accounting question. No complete stellarator layout is required.

## Price and lifecycle method acceptance

Each candidate method must supply source equipment type and construction, independent sizing driver, raw price/currency/year, supported range and correction terms, fabrication/procurement inclusions, installed scope and excluded services. Report engineering applicability separately from arithmetic/correlation evaluation. Use published justified installation labor or representative installed unit costs where available. Do not invent factors to force a total.

[AGENT] Life-cycle design will separate initial spares from replaceable subassemblies, scheduled replacements and routine maintenance. A justified lifetime beyond plant operation can give zero scheduled whole-equipment replacements without claiming zero maintenance. Explicitly assumed service-life scenarios are admissible if their physical rationale and cost consequences are shown; they are not sourced reliability predictions. Routine work must be reconciled with existing staffing O&M. Pump electricity is already a generation penalty and must not be charged twice. Coincident maintenance may use existing outages only as an explicit scenario with throughput plausibility; additional outage is a separate consequence.

## Verification and focused study contract

1. Recompute all four reference specifications independently, including inlet density, machine splitting and actual thermal approaches. Verify topology and UF are labeled assumptions. Exercise invalid approaches, negative/zero inputs and source cost range edges.
2. Verify exact replacement arithmetic at unchanged inputs: equipment direct total minus removed allowance; propagate the delta through CAS22, contingency, indirects, supplementary charges, construction financing and annual cash flows. Account for every retained intermediate/service term explicitly.
3. Check source numerical examples using the actual original equations/tables, then independently compare target applicability and scale. Numerical agreement alone cannot release physical transfer.
4. Run current baseline, saved r2 forward/Table5 overrides, selected18 and selected14. Keep all current breeding/current/divertor/fit failures. First compare old/new accounting on identical inputs; only then vary circuit count or thermal demand.
5. Choose a small declared grid covering14/18 circuits plus a neighboring count, a supported demand perturbation, and important pipe-length, exchanger thermal-transfer and price/lifecycle assumptions. No optimum or continuous feasible-region claim. Exact cases and ranges await source-domain review, not an arbitrary broad sweep.
6. Update and test affected producer/consumer contracts against the regenerated package. The prior consumer failures stop before some numerical checks; restore meaningful current coverage rather than dropping assertions. Preserve frozen records and report remaining unrelated failures separately.

## Release status

Source methods and installed/lifecycle boundaries are not yet accepted. The independent reviewer must assess a concrete complete or explicitly partial estimate before substantial implementation. Any partial estimate must identify unpriced scope and cannot by itself claim the entire goal's S3 outcome.
