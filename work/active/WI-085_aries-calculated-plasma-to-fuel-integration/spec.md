---
Status: active
Scale: standard
Epic: ARIES model transfer experiment
Owner: transfer_physics_inventory
Created: 2026-09-21
Updated: 2026-09-21
---

# WI-085: Calculated plasma power drives fuel demand

[INHERITED: owner continuation through coordinator, 2026-09-21] Connect the accepted WI-083 calculated fusion-power producer to the unchanged WI-082 fuel balances and offered-capacity check. No new physical definitions or equations are required. Preserve all original cases, library definitions and typed completions. Scope is a conditioned plasma-to-tritium-demand evaluation; actual ARIES equipment, breeding, inventory and cost remain unqualified.

## Contract and roles

- **R1 [INHERITED]:** A new `models/designs/aries_cs_transfer/plasma_fuel.sysml` imports the existing WI-083 case and binds its exposed `plasma.fusion_power_MW` directly to the unchanged `Fuel Cycle Flows.p_fus_in`. The generated fuel consumer must read an upstream module output. No supplied fusion-load parameter may remain in this integrated fuel case.
- **R2 [INHERITED]:** Keep the existing plasma case's supplied profiles/temperature/species/measure/field/volume and WI-082 burn fraction 0.05, recovery 0.99 and independently selected tritium-processing rating 2e22 atoms/s. Constants and dormant breeding placeholders retain WI-082 meanings; no breeding result is accepted.
- **R3 [INHERITED]:** Increasing only supplied density amplitude from 5e20 to 7.5e20 m^-3 should increase calculated fusion power and downstream demand by 2.25 under fixed other choices. The original selected 2e22-atoms/s capacity remains unchanged, and its adequacy check must switch from satisfied to violated. A second supplied lower/higher rating at fixed plasma must change only capacity results, not demand.
- **R4 [INHERITED]:** Preserve unsupported states. Invalid plasma temperature refuses native evaluation rather than yielding a passing downstream check; unsupported offered-capacity conditions retain definedness=0 and cannot pass adequacy.
- **R5 [INFERRED]:** Execute actual generated TEAx; independently verify burn rate from calculated fusion power and the retained reaction energy, fuel conservation, expected scaling and unchanged capacity. Check exact baseline fuel-function equivalence at the newly calculated loads. Assess all scoped validation levels and obtain independent review of the new producer/consumer binding and observed behavior.

## Design and MR-7

[AGENT] The integrated model stages the unchanged WI-083 case and its three library files, the unchanged fuel/viability library files, and one new design assembly. It does not stage the old WI-082 case, which still has a supplied source-load input. The new fuel-system occurrence binds the actual imported plasma occurrence's exposed calculated power. Its exhaust EXPOSE feeds a processing occurrence's unchanged `Offered Capacity Screen`; the unchanged `Offered Equipment Capacity` asserted constraint evaluates definedness and margin. No wrapper or physical relationship is added to select hardware or calculate a replacement load.

| Quantity | Role and owner |
|---|---|
| Profile amplitude and other WI-083 inputs | Supplied choices owned by the imported plasma occurrence, unchanged from WI-083 |
| Fusion power MW | Calculated by the existing plasma integration; exposed producer attribute; consumed by fuel balance |
| Burn/recovery/extraction and dormant inventory/TBR choices | Supplied scenario choices owned by the new fuel occurrence, copied with the explicit WI-082 provenance |
| Tritium burn/injection/exhaust/loss atoms/s | Calculated by unchanged fuel balance |
| Processing rating atoms/s | Independently supplied new processing occurrence choice; fixed during demand perturbation |
| Capacity margin, definedness and adequacy | Calculated/evaluated by unchanged capacity screen and asserted constraint |

[AGENT] The four-view path is the explicit requirement for calculated-load propagation → plasma reaction and fuel-processing-demand behavior → imported plasma, fuel-system and processing occurrences → native producer binding, fuel conservation, capacity screen and executable predicate. Ports or an additional behavior solver are not needed for this scalar steady-state exchange. The assembly's documentation records the exchange and component responsibilities. Inventory/cost responses are not tested because none are represented in this scoped assembly.

## Execution and verification

[AGENT] Reuse the isolated native route. Generate a new package; reuse WI-083 integration and WI-081 density completions with package-prefix changes only; reuse the exact extracted reaction kernel; reuse the existing capacity completion with package-prefix change only. The standard generator implements fuel balances and beta automatically. Verify source/staging hashes and typed completion identity, regenerate the package seal and assert the generated graph's fusion-load input is the integration output channel rather than an entry input.

[AGENT] Native cases: nominal plasma/capacity; amplitude times 1.5 with fixed capacity; nominal plasma with insufficient 1e22 rating; nominal plasma with higher 3e22 rating; unsupported capacity conditions; plasma edge temperature 0.023 keV (expected domain refusal). Compare all seven fuel outputs to the existing baseline function at each computed load, excluding dormant breeding quantities from physical conclusions. Use independently computed energy/conservation identities. Record the selected hardware before/after, actual constraint report, and unchanged load under capacity perturbation. Numerical/scientific limits inherited from WI-083 remain unchanged.

## Checklist

- [x] Record inherited source/physics scope, actual new binding, roles and verification.
- [x] Independent source/design acceptance of the new cross-component binding.
- [x] Implement new assembly and isolated package with unchanged calculations/completions.
- [x] Execute native conservation, scaling, hardware-preservation and unsupported-state cases; scoped complete validation.
- [x] Record evidence and final independent review; hand off native tracking to coordinator.

[AGENT] Independent design accepted in `work/orchestration/aries-transfer-experiment/evidence/plasma-fuel-review.md`. Native first attempt passes all six intended cases and 35 exact fuel-output comparisons. Full scoped validation exits 1: levels 1–5 pass, including one admitted executable constraint; level 6 reports 12 EXPOSE diagnostics on outputs/consumers exercised by the actual native graph. Final review pending; see `implementation.md`.
