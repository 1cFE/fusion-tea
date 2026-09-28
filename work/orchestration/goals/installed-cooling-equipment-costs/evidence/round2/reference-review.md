# Independent Round 2 reference-specification review

Reviewer: `equipment_review`, 2026-09-18. Non-author review of `reference_sizing.py`, `reference-sizing.json` and WI-067 candidate `design.md`. Reused original image checks from Round 1. Independently recomputed from current `entering-replay.json`, using 50-digit decimal arithmetic, rather than executing the author's script or trusting its historical intermediate quantities. No model/source edits or cost-method verdict.

## Result

**Arithmetic verified for the four retained cases; conceptual design clarification required before pricing resized exchangers.** All thirteen checked numeric fields per case agree within 2.5e-15 relative. Source OB outside area is 10310.691255 m², counterflow-terminal LMTD 26.375784 K and effective UF 984.730545 W/(m² K). Current instance bindings confirm cp=5193 J/(kg K), gamma=5/3, pressure=8 MPa and drive efficiency=1; the latter remains a lower-bound convention.

| Case | Suction density kg/m³ | Machine inlet m³/s | Machine electric MW | LMTD K | Required area per IHX m² |
|---|---:|---:|---:|---:|---:|
| selected 18 | 6.654634 | 11.764360 | 2.410455 | 29.195311 | 5824.088563 |
| matched 14 | 6.611749 | 15.223712 | 5.135574 | 26.910306 | 8277.639053 |
| r2 forward | 6.600719 | 16.001180 | 5.937183 | 26.298842 | 8930.159413 |
| r2 Table5 | 6.601319 | 15.959823 | 5.892670 | 26.332346 | 8894.261880 |

## Assumptions and limits

- Parallel topology, equal loading and ideal gas density are correctly explicit assumptions. Each machine sees half-loop mass flow, full loop pressure rise and half-loop power. Suction pressure/temperature, not discharge conditions, correctly determine volume flow. These numbers specify a conceptual duty without proving machine availability.
- Actual helium terminals produce positive terminal approaches in all four cases. Effective UF retains an unknown multipass correction; fixed UF is a conceptual transfer, not a measured off-design law. Positive end approaches alone do not verify local multipass pinch, salt hydraulics, fouling, alloy or pressure-boundary design.
- **Clarify the exchanger hydraulic coupling.** Calculated required areas are only 56.5–86.6% of source OB area. This can be a thermal-area requirement for costing research. It cannot simultaneously establish a smaller manufactured exchanger and preserve the current reference-geometry pressure-loss coefficient without an explicit assumption or reconciliation. Distinguish installed area from required area, as already done for the pipe alternatives. A retained reference module would be priced at its installed geometry; a resized exchanger needs a declared geometry/loss treatment or a clearly bounded fixed-hydraulics costing scenario.
- The fixed-case script is not a general validated calculator. It hard-codes fluid properties/pressure, assumes valid positive circuit count, suction state and duty, and does not deliberately reject nonfinite or negative inputs. It handles equal positive terminal differences and reports nonpositive approaches as invalid; near-equal differences merit stable evaluation if reused. Zero flow produces zero area but `None` for total area through truthiness, so a future production interface needs an explicit zero-duty policy. These do not invalidate the four saved cases.
- Equipment/account ownership, secondary-side architecture remaining undecided, and the explicit lifecycle scenarios are coherent candidate boundaries. They are not yet a priced design. Cost curves must use the power boundary they actually price; unity drive efficiency must not conceal motor, shaft or mechanical-loss assumptions.

## Acceptance scope

This review accepts the four-case numerical specification as a conditional research input. It does not release implementation, certify equipment performance, choose secondary architecture or assign a new R7.S score. Address the exchanger geometry/loss distinction in the design before using area to select an equipment cost method. Original price-method, installation and lifecycle review remains pending.
