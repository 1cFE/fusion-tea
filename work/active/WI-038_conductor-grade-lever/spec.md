---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-13
Updated: 2026-09-13
---

# WI-038 — Priced conductor field envelope

## Need and intended use

[NEED] The owner requests a defensible magnet design-point transfer, with “WI-040 first, then WI-038”. Scope and delegated technical judgment are recorded in `work/orchestration/goals/magnet-design-transfer/goal.md` and trail T-004. WI-040's independent audit passes at `6f705b4f`; its material accounting is the entering basis.

[INHERITED] Changing the conductor field ceiling currently changes its acceptance threshold without changing tape procurement, winding-pack sizing or stress. The registered WI-038 item calls for a cost/stress consequence chain. [INFERRED] The intended use is a relative, fixed-temperature REBCO design-envelope comparison, not selection of a certified vendor grade.

## Requirements

| ID | Required outcome | Authority | Verification |
|---|---|---|---|
| MR-WI038-1 | The model SHALL give the selected conductor field envelope explicit, source-bounded tape-quantity and effective winding-pack-current-density consequences. | [NEED] conductor-grade consequence objective; [INFERRED] relative implementation | Source check and independently calculated envelope perturbations. |
| MR-WI038-2 | At fixed current, coil geometry, composition and turn current, increasing the selected envelope SHALL increase tape procurement, winding volume and non-tape procurement consistently, while existing sizing determines the stress and cryogenic consequences. | [INFERRED] consistency needed by the goal | Public route tests of quantity, cost, volume, stress, strain and cryogenic responses. |
| MR-WI038-3 | The model SHALL retain the distinction between actual peak field and purchased design envelope, including the existing peak-field verdict and explicit limits on what its satisfaction establishes. | [INHERITED] WI-030 operating check; [INFERRED] interpretation | Crossed actual-field/envelope cases; no certified critical-field claim. |
| MR-WI038-4 | At the reference envelope, all 174 entering output channels and all 18 verdicts SHALL retain their values; existing legacy winding and 1costingFE comparison accounts SHALL remain ungraded. | [INFERRED] baseline and comparison preservation | Exact keyed before/after baseline comparison; off-reference legacy checks. |
| MR-WI038-5 | Current-density and price reference conditions, field exponent, composition assumptions and extrapolation SHALL be explicit. No absolute operating margin, temperature surface, angular surface or vendor premium SHALL be inferred from the relative relation. | [INHERITED] project MR-4; [INFERRED] source applicability | Source-image and parameter-basis review. |
| MR-WI038-6 | Reusable analysis SHALL remain in the library with identifiable physical owners, explicit bindings and coherent canonical, generated, oracle and public-consumer interfaces. | [INHERITED] MR-3, AD-007/008 | Structure inspection, exact twins, fresh generation, current oracle parity and consumers. |
| MR-WI038-7 | Invalid fields, exponent, reference density or price and non-finite computed results SHALL raise deliberate named diagnostics. | [INFERRED] valid numerical comparison | Typed component and public wrapper domain cases, including overflow. |

## Supported use and boundaries

[AGENT] This item adopts a relative quantity multiplier from an approximate REBCO field exponent reported at 20 K, anchored to the existing 24.9 T design envelope. Fig. 1a shows 20 K tape measurements extending to approximately 24 T; the reference anchor remains beyond the observed range. The source's exponent paragraph does not identify its fit interval. Use 20–30 T only as an agent-selected extrapolative design-sensitivity window; the exponent does not establish validity over that window. The goal study must separate numerical consistency from engineering qualification.

[AGENT] Hold reference `j_wp = 118.8271604938272 A/mm²`, economic reference field, conductor family, temperature, angular assumption, composition and source coil-shape/distribution factors fixed throughout supported priced transfer. The existing density input remains a calibration/arithmetic interface; independent changes require a separately justified reference price/inventory basis and are not a priced same-technology lever. Increasing all constituent volumes together approximates a uniformly enlarged composite winding pack. Winding operations remain based on composite-conductor length; their dependence on conductor cross-section is unpriced. Casing fit, quench protection, altered winding topology, absolute critical-current margin and conductor-manufacturer qualification are outside this item.

## State and references

Design review passes after the fixed-density scope and exponent-interval corrections. Implementation and generated package are committed at `0e3bf944`. Component/public checks pass 41, final model tests pass 889 with thirteen inherited skips, and baseline reconciliation preserves every entering channel/verdict exactly. Broader study-consumer verification and independent implementation audit are in progress; see `implementation.md` and `plan.md`. Existing WI-038 registration is reused. Positive independent native audit is required before completion; close/archive remains owner-held.

Read `basis.md`, `design.md`, `plan.md`, audited WI-040 and project MR-1–4/AD-007–008. Global verification registration and goal state remain coordinator-owned.
