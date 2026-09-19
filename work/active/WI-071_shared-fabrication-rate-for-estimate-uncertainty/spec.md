---
Status: active
Scale: standard
Epic: standalone
Owner: agent
Created: 2026-09-19
Updated: 2026-09-19
---
# WI-071: Shared fabrication rate for estimate uncertainty

## Purpose and authority

[NEED] Quantify uncertainty supported by available evidence while preserving shared drivers, raw monetary bases, disjoint accounts and physical failures. Source: `work/orchestration/goals/cost-estimate-maturity-and-uncertainty/evidence/owner-prompt.md`, required results4–8.

[INFERRED] One shared raw fabricated-stainless price input makes the existing ANL cost analogy inspectable and variable without applying the general cooling multiplier to unrelated equipment. The source-family scenarios are conditional on the adopted construction analogy; target-equipment transfer, design errors and missing scope remain outside the numerical range. This is an analysis interface, not a revised baseline price or new procurement claim.

[INHERITED] Required reading: `knowledge/holdout/aries-cs/PROTOCOL.md`, `.agentic-mbse/codex.md`, `.project/codex-test-setup.md`, `modeling_project/MODELING_PROCESS.md`, `modeling_project/REQUIREMENTS.md`, applicable calculation-binding guidance in `MODELING_GUIDE.md` and `.agentic-mbse/patterns/plant-idiom.md`. Preserve sealed ARIES, excluded derivatives, frozen r2 and unrelated edits. No merge or push.

## Acceptance conditions

| ID | Provenance | Observable result |
|---|---|---|
| MR-071-01 | [INFERRED], source/method proposal | A public raw stainless fabrication rate, expressed in USD2017/kg, reaches the four existing bills: exchanger, primary pipe, secondary pipe and future exchanger-bundle replacement. Default310 reproduces the current estimate. |
| MR-071-02 | [NEED], owner result5 | One shared driver propagates together through initial purchase, existing installation/removal fractions, delivered-cost exclusions, scheduled replacement and electricity cost. Pumps, coolant inventories, spare machines and unrelated accounts do not acquire that driver. |
| MR-071-03 | [INFERRED] implementation of [NEED], owner results1,6 | Preserve the raw January2017 source basis and disclose the inherited annual-CPI2017-to-2025 purchasing-power approximation. No whole-plant price normalization or financial-policy change. |
| MR-071-04 | [INFERRED] implementation of [NEED], owner results5,7 | Quantities, all physical outputs, denominator and predicate verdicts remain unchanged for price-only cases. Disabled behavior is finite; active nonfinite or nonpositive prices are rejected explicitly. |
| MR-071-05 | [INFERRED] implementation of [NEED], owner result8 | Source240/360 values independently reproduce fixed120USD2017/kg carbon base times2/3. Test nominal equivalence, four-bill response, account sums, replacement contribution, unaffected outputs and boundary rejection. Synchronize canonical/twin/generated/oracle interfaces and verify affected consumers. |

## Source and design

[INHERITED] ANL2018 `knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md`, sections3.6.2–3.6.3, original printed26–27. Original images and research interpretation are in the goal's `evidence/method-source-images/` and `evidence/method-research.md`. NAF's2–3 ratio is reported expert communication, not observed quote dispersion. The source's310000USD/t recommendation and two historical point reconstructions are retained. The proposed240–360 bracket fixes the uncertain carbon reference itself; it does not bound modern target cost.

[AGENT] Proposed owner input `heat_transport.equipment_stainless_fabrication_usd2017_per_kg`; calc formal `stainless_fabrication_usd2017_per_kg_in`. Bind with distinct names using the existing Primary Heat Transport pattern. Preserve the existing310 default in both reusable compatibility path and concrete design. Add the value to the generated manual implementation's existing input dictionary and positive-domain checks. Replace only four310 multipliers. The independent oracle gets an independently named parameter and the adapter publishes the exact qualified entry. Retain historical model/executable files unchanged in frozen records.

[AGENT] Affected paths: canonical `mfe_cooling_equipment.sysml`, `mfe_plant_systems.sysml`, stellarator design and their model-family twins; generated cooling manual body and regenerated package/contracts; independent `oracle_cooling.py`, `verify_stellaris.py`, study `oracle_entry.py`; targeted cooling tests, model-family census, snapshot and manifest. Enumerate actual consumers before editing. One worker owns all scientific implementation and generation. Coordinator owns commits, integration and goal trail.

## Execution checklist

- [x] Native registration and bounded specification.
- [x] Full independent method/source/interface release, including maturity framework and contingency policy, before substantial implementation.
- [x] Confirm consumers; implement canonical/twin/manual/oracle input and source citations.
- [x] Regenerate and synchronize package, baseline manifest, census and snapshot using the pinned runtime.
- [x] Run targeted source, four-bill, preservation, domain and affected model-family checks; report static diagnostics honestly.
- [x] Obtain focused independent implementation assessment and resolve material findings; see `audit.md`.
- [x] Commit audited candidate at `fe720553`; native integration returned CANDIDATE with all ten gates passing. See goal `evidence/integration/integration_return.json`; omitted read-set coverage remains disclosed.

No separate design or plan document is needed for this single shared-input change. This specification carries the contract, interface and persistent checklist. The goal's focused native study owns combined uncertainty cases and final interpretation.

## Implementation scope and consumers

[AGENT] Confirmed 2026-09-19: the cooling calculator and heat-transport owner belong only to the MFE family, with one stellarator instance and a generic disabled compatibility path. Canonical changes synchronize to `exploration/stellarator_e2e/models`; IFE has no affected owned file. Native regeneration derives the module/schema/input/pipeline/contracts/manifest and census/snapshot. Thirty-five unrelated manual seeds must remain byte-identical; only the cooling seed changes. Independent consumers are `oracle_cooling.py`, `verify_stellaris.py`, `studies/oracle_entry.py`, installed-cooling tests and `current_mfe_regressions.py` generation/ABI adapters.

[INFERRED] Study verification prerequisite: expose the existing `contingency_rate` public key in the oracle adapter. The plant and independent oracle already contain its equation and 0.10 default. Verify both 0 and 0.10 through the native pipeline; do not change financial policy or formulas.

## Implementation evidence

[AGENT] Candidate implementation and checks are recorded in `implementation.md`. Two fresh generations match; the nominal result preserves all956 outputs and25 authored predicates. Targeted batches pass43 and89 tests; the six implementation cases pass5604 mapped scalar/Boolean comparisons and150 predicate comparisons. L2/L6 retain exactly their entering diagnostic identities. SV-119/SV-120 are registered and passing. Independent implementation assessment passed in `audit.md`; candidate `fe720553` passed all ten native integration gates. The study and final R12.S grade remain owned by the goal.
