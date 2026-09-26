# Design review: WI-094 costed loop-Brayton assembly

Reviewer: fresh non-author reviewer. Date: 2026-09-26. Brief: `design-review-brief.md`. Reviewed `work/active/WI-094_costed-loop-brayton/design.md` (§ 1–7, § 10), `spec.md` (R1–R6) and `evidence/draft-costed_loop_brayton.sysml` against the entry files the brief names. Nothing was run.

## Verdict: PASS

No `correct-before-implementation` finding. Five notes.

## Q1. Formals and units

Read: every `in` of every cost calc (draft lines 464–966) against the `in attribute` lists of the five analysis files; 'Selected Equipment' and 'Costed Component'; the cited ARIES ranges; the four bodies.

Compared: all 18 definitions are fully bound with existing formals (Equipment Cost Ledger 19/19, Lifecycle Cashflow Accounts 27/27, Annual Selected Fuel 11/11, Fuel Cycle Flows 12/12, the rest likewise). Units line up: MW into `p_fus_in`, `net_power_in`, `net_electric_mw`; atoms/s × kg/atom × s → kg in Annual Selected Fuel (body lines 10–14); kg stock against kg `required_stock`; USD and years elsewhere. Bindings equal ARIES except the disclosed substitutions. The one real shadow, formal `direct_cost` against sibling part `direct_cost`, is qualified (line 747) as ARIES does. 'Selected Equipment' adds only `capital_cost` and `cas_code`, so `he_hx`'s `selected_area`, `ua`, `area` are safe.

Finding: none. `note`: cross-part references are unqualified (`cost_accounts.estimate_mode`, `compressor_capacity.selected_rating`) where ARIES qualifies every one; § 1a's generation test is the only evidence this resolves.

## Q2. MR-7

Read: the six purchase leaves, `fuel_inventory`, `replacement_scope`, `annual_om`; MR-7.

Compared: each `quantity_in` reads a screen's `selected_rating` (literals 1600/3500/1800/2500/1500) or `selected_area` (50,000); none reads a demand. Stock capital is `selected_tritium_kg` × price; `required_stock` is calculated and screened, never bound. O&M is flat (`om_ref` 0, `p_net` literal 1000). Loop flow direction is C-1's.

Finding: compliant; no sizing rule. `note`: § 9 says the manifest's verdicts are "the eight checks"; § 1a counts nine (the stock screen). It is constant across the sweep (≈ 0.09 kg required against 10 kg), but the manifest should say nine or state why the ninth is omitted.

## Q3. Single counting

Read: `priced_equipment`, `direct_cost`, `cost_ledger`, `lifecycle_accounts`; the ledger and lifecycle bodies; contract § 5, § 6.

Compared: priced = the seven § 5 items (reference sum 461,372,866.67, arithmetic checked); rest = 2,619,603,000 − 461,372,866.67 = 2,158,230,133.33; direct = rest + priced + stock, the ARIES shape (`plant.sysml:1951–1964`). Overnight = direct(1 + 0.2 + 0.24 + 0.05) (ledger line 11) = contract § 6. Replacement enters once via `pv_replacement`; the ledger does not add the reserve to `annual_operating`. Stock is capital, makeup is operating, and the lifecycle reconciles both (lines 19–20, 37–39). `q_ihx` feeds only the closure and `p_elec` only the balance; no cost part reads either.

Finding: single-counted. `note`: that the ARIES source scope holds the seven items at exactly their reference values is taken from contract § 6; `direct_source_scope` lies outside the brief's ranges.

## Q4. Control claim

Read: a mechanical diff of draft lines 26–463 against original lines 20–441, names normalised.

Compared: differences are doc text, the `he_hx` specialisation, and `fuel_exhaust` moved from before `control` to after `other_electric` (value 0.0). No C-1 part references a cost part; `fuel_exhaust` stays a literal, not `fuel.exhaust_rate`; the conductance bindings are byte-identical and the purchase calc only reads `selected_area`.

Answer: No. The cost parts are downstream only, the fuel term is a literal zero, and the conductance path is unchanged. `note`: § 1's "unchanged WI-093 text" is not literal (the reorder); say "unchanged bindings and values" or restore the order. `note`: channel keys change with the root rename, so § 7 needs a key map; and the lifecycle body refuses at net ≤ 0 (line 15), so § 6/§ 7 should state that a downstream refusal still stores that case's C-1 channels, or confirm all five controls have net > 0.

## Missing evidence / uncertainty

- Resolution of the unqualified references (Q1 note): reported in § 1a, not runnable here.
- `direct_source_scope` composition (Q3 note).
- The 'Selected Inventory Purchase' (mode 0) and 'LCOE DCF' bodies were not in the brief's list; taken as ARIES-reviewed.
