---
Status: implemented-candidate
Created: 2026-09-19
Updated: 2026-09-19
Related Artifacts: spec.md, evidence/proposed-abi.md, evidence/account-reconciliation.md
---
# WI-070 design: conditional exhaust-processing capital

## Decision and model ownership

[AGENT] Add one guarded library calculation for the four-row processing aggregate, owned by the existing Fuel Cycle. Its inputs are the upstream operating isotope flow, configuration/source values and the existing legacy price. Its selected output replaces the existing `fuel_handling_cost` producer. Keep the old `fuel_handling` power-law calculation as an explicitly labeled legacy comparison and dormant generic route. No residual old allowance enters the active rollup.

The existing `exhaust_processor` stock occurrence already represents cleanup/separation and the single outlet recovery loss. Specialize its type to a `Fuel Processing Stock` that inherits `Fuel Stock` and the standard `Costed Component`, adds equipment/direct-installation breakdown attributes and owns CAS220500. Bind its `capital_cost` to the sibling `processing_cost.cost`, including legacy mode. Stock remains per module while attached cost/breakdowns represent the whole plant. This grounds the price in the existing functional occurrence without duplicating the stock, creating another mass balance, or pretending four cost rows are four independently designed equipment trains. Transfer and limited containment are local support within this account's explicit boundary.

Reusable calculation/part definitions live in the library; raw prices, source CPI values and active scenario bindings live in `stellarator_09`. Dormant placeholders and neutral switches are documented generic configuration defaults. Canonical and exploration twin files remain byte-identical. Existing patterns for pure EXPOSE, owner-qualified component bindings and strict handwritten execution are reused; no new language mechanism needs a prototype before this review.

## Producer and applicability semantics

The existing `Fuel Cycle.inventory.dt_processor_kg_s` is per-module operating exhaust inlet. Add a public Fuel Cycle EXPOSE `dt_processing_flow` of that exact output; do not change its arithmetic. The cost calculation binds the public alias in the same owner. It also reads existing `inventory_enabled`; it must not infer validity from zero flow. Cross-owner consumers read named producer interfaces, not deep calculation internals.

[AGENT] An active processing estimate requires active inventory. Active processing with disabled inventory raises a domain error, rather than pricing a dormant zero carrier. Undefined breeding is different: WI-069 still computes physical plasma-exhaust flow when `breeding_defined=0`. Therefore breeding applicability does not suppress the processing price or its defined flag. Failed breeding cases remain in the plant response and studies.

`processing_source_conditions` means that the user is invoking the declared conventional/feed-conditioned scenario; it is not a measurement. When active and this declaration is false, retain numerical diagnostic costs but emit `defined_flag=0` through the plant-facing named interface `fuel_cycle.fuel_processing_defined`; consumers and study interpretation cannot call those physical prices. When active and declared true, `defined_flag=1` means a conditional estimate is defined, not that purity/recovery or full plant feasibility is verified. No new engineering qualification constraint is invented. Dormant generic legacy output has `defined_flag=0` for the new method while preserving legacy price behavior.

Source conditions remain in component/calculation documentation: near-equimolar primary D/T, reference-like minor impurities, cleanup to below 1 ppm noncondensibles, approximately atmospheric cryogenic separation and 20 K class refrigeration, full source separation service, conditional 99% functional recovery. A Boolean declaration does not test them. No code threshold falsely turns the ITER comparison into a certified upper capacity.

## Four-row calculation

Let `F` be actual kg D+T/s per module, `m` capacity margin, `n` module count, `p` source-price multiplier, `F0=2.08e-5 kg/s`, `a=0.3`, `It` target CPI and `Ij` row source CPI. Define `Fd=m*F`, `r=Fd/F0`, `s=r^a`. For row j with raw capital `Kj` and installation `Lj`, source-capacity converted values are `K0j=Kj*It/Ij` and `L0j=Lj*It/Ij`. Actual plant totals are `Kplant,j=n*p*s*K0j` and `Lplant,j=n*p*s*L0j`. Sum the rows separately, then `new_account=equipment_total+installation_total`. Source-capacity converted values exclude margin, module count and price multiplier so reference reproduction is unambiguous.

| Row | Raw capital USD | Raw installation USD | Source CPI | Monetary-year interpretation |
|---|---:|---:|---:|---|
| Transfer pumps |111000|112000|60.6|1977 |
| Cleanup |1000000|70000|82.4|1980 |
| Cryogenic distiller |1237000|63000|65.2|1978 |
| Limited secondary containment |182000|30000|82.4|1980 central assumption within 1978–1982 |

`It=321.9` expresses 2025 CPI purchasing power. Raw installation uses the corresponding capital year as an explicit proxy. The public `processing_containment_cpi` parameter supports documented endpoint scenarios 65.2 (1978), 82.4 (1980), 96.5 (1982); its domain is positive CPI, not a fabricated date interpolation. Study scenarios must name the actual source year rather than treating CPI values as year numbers. The remaining source constants stay inspectable public configuration; mandatory coverage checks all generated keys, including any constructor defaults that surface.

At source flow, one module, margin 1 and price 1, each row reproduces the reviewed raw/CPI conversion. At current F and defaults, equipment=$20,443,419.583268173, installation=$2,342,809.8205252266, total=$22,786,229.4037934 before generic charges. The reviewed endpoint totals are $23,180,989.577015813 and $22,567,582.023116916. These are regression anchors, not a complete uncertainty band.

## Domain and operating modes

- Disabled processing returns the legacy account exactly and zero new-method breakdown/shipping exclusion/defined flag. Dormant zero source placeholders are never divided or exponentiated. Finite input checking remains strict; active-only positivity checks do not invalidate existing dormant generic values.
- Active mode requires finite F≥0, active inventory, integer n≥1, finite margin≥1, price multiplier>0, F0>0, exponent>0, target/source CPI>0 and nonnegative raw row amounts. Declared flags must be exact Booleans. Intermediate and final outputs must remain finite; overflow is a ValueError, not a plausible cost.
- F=0 yields exact zero active row/account costs through the source power-law limit. It is an extrapolative no-exhaust diagnostic, not a statement that all real plant safety equipment disappears. A zero margin or zero price is rejected. Source-capacity converted row outputs remain nonzero at F=0 for inspection.
- Module basis is independent identical per-module processing scope: each module has flow F and cost at F, then costs multiply by n. No shared economy of scale, spare train or multi-unit discount is assumed. The current plant has n=1; unit/isolated calculator tests verify n=2, while native whole-plant n>1 may remain refused by other established subsystem domains.
- Availability is absent from the cost interface. Recovery is not a cost input: it affects only the established physical producer where applicable. Burn fraction/fusion power changes reach F through WI-069. Capacity margin and price uncertainty remain distinct inputs.

## Accounting

Use `evidence/account-reconciliation.md` as the account contract. The full selected output enters the existing Fuel Cycle EXPOSE and CAS22 summand once. Source installation is excluded from generic freight after applying the same CAS29 contingency that entered CAS20. Purchased/fabricated capital remains in the inherited shipping proxy because freight inclusion in historical package prices is not established; no delivered-price claim is made.

Extend existing `Facility Shipping Scope` with default-zero `fuel_installation_in` and `contingency_in` formals and a new output `fuel_installation_exclusion`. It computes `(1+contingency)*fuel_installation`, rejects combined exclusions exceeding CAS20, and exposes the remaining base. Extend `Supplementary Cost` with the default-zero exclusion and subtract it only in shipping. Existing cooling/facility outputs and arithmetic stay unchanged. Generic disabled processing gives exact zero exclusion and preserves old results. These are project-charge scope corrections, not new equipment prices.

[AGENT] Assign the controls included in the four source packages exclusively to C220500. C220700 covers distinct plasma diagnostics, central supervision, plant computer/data acquisition and plant-level safety coordination, excluding those package-local instruments/controllers. Keep its inherited coefficient unchanged as an uncalibrated residual allowance; the source does not establish that the historical coefficient excluded local controls. Add this exact scope and limitation to the existing I&C calculation and owning plant documentation. Additional specialized fuel instruments outside the four packages have no separate estimate. This explicit modeled allocation follows goal `evidence/controls-review.md`; it is not a historical price decomposition.

## Affected files and execution route

| Surface | Intended responsibility |
|---|---|
| `models/library/analyses/mfe_fuel_cycle.sysml` | Guarded `Fuel Processing Cost` definition with explicit output-only typed manual completion and source equations/docs |
| `models/library/structure/mfe_plant_systems.sysml` | Costed processor type, source/configuration inputs, public flow EXPOSE, calculation ownership and selected fuel-cost outputs |
| `models/designs/stellarator_09/stellarator_plant.sysml` | Active owner-ratified conventional scenario, source rows/CPI and separate study controls |
| `models/library/analyses/mfe_facilities.sysml` | Existing shipping-scope guard extended for process installation |
| `models/library/analyses/mfe_account_costs.sysml` and `models/designs/generic_mfe/mfe_plant.sysml` | Supplementary shipping subtraction, named producer bindings and explicit C220700 supervisory-controls allocation documentation |
| Corresponding `exploration/stellarator_e2e/models/` paths | Identical canonical twins |
| Generated `handwritten/mfe_fuel_cycle/fuel_processing_cost_impl.py` | New normative guarded cost implementation |
| Generated `handwritten/mfe_facilities/facility_shipping_scope_impl.py` | Only existing normative body expected to change; retains prior default behavior |
| `exploration/stellarator_e2e/oracle_fuel_processing.py`, `verify_stellaris.py`, `studies/oracle_entry.py` | Independent row arithmetic, full account response and explicit maps; old legacy output remains mapped distinctly from selected price |
| `tests/models/test_fuel_processing_costs.py`, `test_fuel_processing_oracle.py`, `current_mfe_regressions.py` | Source/limits/accounting/native behavior and current generation-receipt/ABI expectations |
| Generated contracts/schema/pipeline, model snapshot, census and package manifest fingerprints | Derived metadata refreshed through retained WI-069 procedure after implementation; no new study runs by author |

Reuse WI-069 `evidence/regenerate.py` and the underlying WI-040 strict fresh-generator recipe. Start from its 35 normative seeds; register the new cost body and changed shipping guard explicitly, rejecting unrelated changes or obsolete paths. Preserve byte-exact fresh-generation comparisons twice and emitted output-schema order. Do not edit autogenerated code to compensate for a model binding error.

Adapt WI-069 `repin.py` to the full new oracle mapping and exact package; refresh existing package manifest fingerprints/baseline, snapshot and census only as required producer metadata, not study case records. Coordinator performs native integration after reviewed changes are committed. The coordinator explicitly authorized author updates to the existing package manifest as producer metadata. Historical study records remain outside author ownership.

## Verification and review gates

Use the acceptance table in spec.md. Source/price arithmetic and engineering transfer reviews already passed; reuse them at their original scope. Preimplementation independent review must check source-to-flow binding, generic compatibility, undefined-breeding behavior, module basis, I&C disposition and all charge equations. No whole-plant feasibility assertion follows from a lower account price.

After release, verify source rows with independent Decimal calculations and raw-year conversion, exact zero limit and invalid domains, scalar-source multiplier identities, module linearity and capacity exponent ratios. Test price/date/margin-only changes against all upstream physical outputs, not only a chosen headline. Test public native burn-fraction and operating-power changes against the independent flow and accounting chain. Test dormant legacy parity and breeding-undefined cases. Test positive contingency to catch shipping labor charged through CAS29; test combined exclusions so no negative freight base can be silently clamped.

Run relevant fuel inventory, processing, facility-account/shipping, model-family generation and affected current-regression checks; compare validator diagnostic identities before/after. Record pre-existing failures/skips honestly. All new outputs need explicit oracle mapping and numerical comparison, including definition flags and row breakdowns. Native study and final R10.S grading remain coordinator-owned downstream obligations.
