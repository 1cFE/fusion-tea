# Magnet design-point transfer

## Judgment

[AGENT] The model supports a conditional transfer of magnet sizing and component-cost estimates over the tested points. It does not yet support an engineering-qualified magnet design transfer. The implemented responses are numerically consistent; configuration-specific geometry, absolute conductor margin, pack/casing fit and complete manufacturing costs remain unverified. This is the coordinator's judgment for fresh review, not owner acceptance of those residual assumptions.

WI-040 was implemented and independently audited first, followed by WI-038. Native integration passed all ten gates. The [study record](../../../../exploration/stellarator_e2e/studies/20260913-magnet-design-transfer/record.md), frozen at `fa195fa4`, carries the actual package identity, execution, source assumptions and verification; its independent post-execution review passes. The [fresh administrator synthesis](../../../../exploration/stellarator_e2e/studies/20260913-magnet-design-transfer/synthesis.md) independently supports this conditional reading and finds no material record-contract defect. The [source assessment](evidence/transfer-evidence-assessment.md) distinguishes established facts from missing engineering evidence. The final goal-review verdict is recorded separately in the [goal trail](trail.md).

## Range and meaning

The study evaluates 108 combinations: major radius 11.43, 12.7 and 13.97 m; minor radius 1.17, 1.3 and 1.43 m; coil current 14, 15.4 and 17 MA; selected conductor envelope 20, 24.9, 27.5 and 30 T. These are engineered exploration points, not source-qualified bounds or a continuous validity interval.

The conductor interpretation is one REBCO construction at 20 K, holding reference pack current density, material fractions, coil-set factors and unit economics fixed. The envelope values are scenarios, not qualified manufacturer grades. The source supplies a relative tape field/current trend, not an absolute operating margin. Its visible 20 K measurements extend to approximately 24 T; even the inherited 24.9 T normalization is beyond that extent. A satisfied field verdict compares demand with the selected envelope; it does not qualify that envelope.

## What the execution establishes

- Every proposed case completed; none was excluded. All 17,388 mapped numeric comparisons and 1,944 constraint-verdict comparisons agree with the independent calculation. The maximum reported relative numeric difference is about 3.1e-13 against a declared 1e-9 tolerance. Sixteen native outputs remain outside the independent oracle map. See study `results/exhaustive-oracle.json`.
- The declared joint sizing, inventory, stress, energy and additive-cost identities pass. At fixed geometry and current, raising the selected envelope from 20 to 30 T increases pack volume by 27.54%, pack side by 12.93% and the selected pack cost by 13.48%; modeled stress falls by 11.45%. Actual peak field and the length-based winding-operation charge remain unchanged. These are matched-point responses, not continuous monotonicity or manufacturing-validation claims. See study `results/identity-checks.json` and `results/summary.json`.
- Five points satisfy all eighteen modeled limits; 103 violate at least one. All five use selected envelopes of 27.5 or 30 T, beyond the inspected measurement extent. Peak-field demand exceeds the selected envelope at 48 points and winding stress exceeds its limit at 16. Other violations involve divertor heat, sustainment, primary-loop capacity, neutron wall load, burn hold and recirculating power. The baseline retains its divertor violation. None of the five passing points is certified buildable. See study `results/summary.json`, with every qualified identity and violating case.

The current reference estimate remains 142.507 $/MWh after WI-038. WI-040 changed the old economic baseline by replacing an unsplit estimate with explicitly selected procurement and winding-operation terms. That change is not demonstrated cost savings. At the same reference geometry/current, increasing the envelope from 24.9 to 30 T changes pack volume from 136.56 to 152.71 m³ and selected pack cost from $1.5704 billion to $1.6674 billion; the plant still violates the divertor limit. See study cases `c0053` and `c0055` in `results/cases.json`.

Minor-radius changes alone increase field demand and casing cost in this window, but leave winding inventory and its selected cost unchanged at fixed current, major radius and envelope. This is consistent with sizing to purchased capacity. It is not automatic conductor resizing to actual demand, nor evidence that arbitrary coil-bore changes require no additional manufacturing effort. The field verdict can reject a geometry that exceeds the selected envelope.

## Where transfer stops

The explicit material account separates composite tape from external jacket, solder, steel and coolant. It does not constitute a complete factory estimate: insulation, fixed cable additions and cross-section-dependent winding effort are unquantified; the inherited steel price has an ambiguous fabrication basis; the tape price is a target assumption, not a qualified high-field quote. Whole-plant price years are not normalized.

Independent reference-density changes are outside the priced same-technology claim. They can change modeled tape volume without a matching tape-price change; the WI-038 audit demonstrates why that reference must stay fixed. Geometry extrapolation also retains the anchored coil shapes and unprinted configuration factors. A numerical clearance check cannot replace configuration-specific coil spacing or structural fit.

[AGENT] Use this package to compare conditional responses at stated assumptions and to expose constraint violations. Do not use this evidence alone to select a qualified coil design, claim a manufactured-magnet price, or establish a geometry/conductor operating range. Stronger claims need the specific evidence listed in the source assessment, not a denser sweep of the same equations.
