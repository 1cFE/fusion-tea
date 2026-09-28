---
Status: active
Scale: standard
Owner: reid
Created: 2026-09-21
Updated: 2026-09-21
---

# Conditioned fuel-flow reuse proof

[INHERITED: coordinator assignment, 2026-09-21] Execute an isolated native SysML/codegen/TEAx fuel-flow and supplied-capacity demonstration. Shared definitions and baseline packages remain unchanged. [AGENT] The scope is tritium exhaust in atoms/s, with a synthetic offered tritium-processing rating in the same units; it does not establish total D+T equipment capacity, ARIES installed hardware, breeding or independent fusion power.

## Analysis contract and MR-7

| Quantity | Units | Role and authority |
|---|---|---|
| Fusion load | MW | Supplied 2436, visually checked Lyon Table VII p716 reference column, retained image `.project/active/aries-comparison-preparation/alternative-point-screen/evidence/source-Lyon-page-23.png`; doubled/halved loads are AGENT perturbations. |
| Reaction energy, conversion, atomic mass | MeV, J/MeV, kg/atom | Inherited existing stellarator constants 17.58, 1.6021766339999998e-13, 5.008267663228036e-27, respectively; no new physical calibration. |
| Burn fraction and recovery | 1 | AGENT scenario assumptions 0.05 and 0.99; not sourced ARIES performance. |
| Extraction, inventory, growth, TBR placeholder | 1, atoms, atoms/s, 1 | AGENT dormant assumptions 1, 0, 0, 0. TBR placeholder is not achieved or predicted breeding; breeding outputs are outside the accepted result. |
| Offered tritium-processing rating | atoms/s | AGENT independently supplied 2e22, with 1e22 inadequate variant; not inferred or resized from demand. |
| Burn, injection, exhaust and loss | atoms/s | Calculated by unchanged Fuel Cycle Flows. |
| Capacity margin and adequacy | atoms/s, Boolean | Calculated by unchanged Offered Capacity Screen and asserted Offered Equipment Capacity; applicability and support are explicit conditional scenario flags, not vendor qualification. |

[AGENT] Required path: supplied power → fuel-system occurrence → existing reaction/burn/exhaust balance → exposed exhaust → processing occurrence's existing offered-capacity screen → executable adequacy constraint. No inventory or cost calculation is represented, so acceptance verifies selected capacity preservation rather than asserting an unmodeled cost response.

## Acceptance

- [INHERITED] Reuse the existing two calculation definitions and capacity constraint unchanged, with hashes retained.
- [INHERITED] Generate an isolated package and run actual TEAx pipelines, retaining evidence and generated contracts.
- [AGENT] Reference-load case passes at 2e22 atoms/s and fails at 1e22; doubled demand fails with the original 2e22 selected rating unchanged; halved demand passes. Unsupported conditions do not return an adequate result.
- [AGENT] Compare all flow outputs exactly to the existing native implementation; independently check energy-to-reaction conversion and injection = burn + exhaust, loss = unrecovered exhaust. Test linear demand response at fixed hardware.
- [AGENT] Record source fidelity, translation, arithmetic and conditional adequacy separately. Publish no actual ARIES fuel capability or whole-plant prediction.
