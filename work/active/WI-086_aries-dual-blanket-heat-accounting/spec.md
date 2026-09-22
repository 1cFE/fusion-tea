---
Status: active
Scale: standard
Epic: ARIES model transfer experiment
Owner: reid
Created: 2026-09-21
Updated: 2026-09-21
---

# Dual blanket heat accounting

[INHERITED: coordinator assignment, 2026-09-21] Implement the missing two-blanket-branch energy-accounting architecture as a separately conditioned source case, preserving independently supplied exchanger capacities. [AGENT] The case reconstructs source heat boundaries; it does not predict nuclear deposition, flow, pressure drop, heat transfer or qualified equipment. It remains separate from WI-083 and the Lyon 2436 MW systems point.

## Source and boundary contract

[AGENT] Raffray p734 Table II, p736 Fig12/13 and p737 discussion are retained in `evidence/raffray-p734.png`, `raffray-p736.png` and `raffray-p737.png`. The source figures show separate blanket PbLi, blanket He and divertor He heat exchangers. This model covers only the two blanket branches; its total is not all heat delivered to the power cycle. The engineering study labels fusion power 2365 MW in Fig14. No whole-plant source identity is inferred from its similarity to the later systems study.

| Quantity | MW | Role and authority |
|---|---:|---|
| He deposited heat before exchange/friction | 940 | Supplied source-derived boundary: 1192 - 141 - 111 |
| PbLi deposited heat before exchange | 1555 | Supplied source-derived boundary: 1444 + 111 |
| PbLi-to-He transfer | 111 | Supplied approximate source value; single owner consumed with opposite signs |
| Recovered He friction heat | 141 | Supplied source value, included once in He branch duty |
| Recovered PbLi friction heat | 0 | AGENT source-balance approximation, neglecting the listed 1–10 kW pump term; not a physical zero-pumping claim |
| Printed blanket fusion thermal power | 2496 | Independent report/test comparison value; not an input to the physical ledger |
| He/PbLi offered exchanger ratings | 1250 / 1500 | AGENT hypothetical supplied scalar capacities under assumed supported conditions |
| He/PbLi delivered heat | Calculated | Branch energy balances; source reconstruction should give 1192 / 1444 |
| Combined deposited heat and source residual | Calculated | 2495 MW and -1 MW; retain source mismatch |

[AGENT] Reproducing branch duties from source-derived boundary inputs is accounting consistency, not independent validation of their physical prediction. The integer/approximate source data leave a -1 MW residual against the independent printed blanket total. This may reflect rounding but is neither erased nor declared a proven rounding error. Printed He pumping power 156 MW is distinct from 141 MW recovered friction; no electrical loss model is derived from their difference. Table III compressor efficiency 0.89 describes cycle compressors, not blanket circulators.

## MR-7 and model design

[AGENT] Branch deposition, exchange and friction heat remain supplied inputs in MW. Each branch owns its supplied offered exchanger-duty rating and capability-support flag. Calculated duty is compared with that rating; no calculation changes the selected rating. These are necessary scalar duty screens under explicit assumptions, not UA/pinch/material/pressure qualification. No flow, cp, pressure loss, efficiency, inventory or cost is inferred.

[AGENT] Add two generic calculations in `dual_circuit_heat_accounting.sysml`: `Coolant Branch Heat`, implementing `delivered = deposited + received - exported + recovered_friction`, and `Dual Circuit Heat Ledger`, consuming both calculated branch duties plus their supplied depositions/friction. Ledger outputs are combined delivered heat, combined deposition, combined recovered friction and `energy_residual = delivered_total - deposited_total - friction_total`. The report/test separately computes `source_residual = deposited_total - 2496` from the native deposition output; the published comparison total is not a physical ledger input. Both residuals are signed MW, not capacity constraints.

[AGENT] The new design owns a single inter-coolant exchange occurrence, one helium occurrence, one PbLi occurrence and an assembly ledger. The sole exchange attribute feeds PbLi exported heat and He received heat. Each branch exposes its computed duty to the ledger and to its own occurrence of unchanged `Offered Capacity Screen`; each asserts unchanged `Offered Equipment Capacity`. Cross-component consumers bind public exposed outputs, not internal calculations.

[AGENT] New arithmetic is guarded through typed native completions: all supplied heat inputs and branch duties must be finite nonnegative; reject negative net branch heat rather than clamping; totals and residuals must be finite. Zero input heat is allowed. Signed residuals remain visible. The unchanged offered-capacity implementation enforces its documented nonnegative/finite and support rules. No current DEMO primary-loop, salt transport or Rankine model is reused with new physical labels.

## Native acceptance

- [ ] Independent source/design review accepts the bounded accounting contract before model implementation.
- [ ] Implement two generic definitions, one four-owner assembly and two unchanged capacity-screen/constraint occurrences; generate and seal an isolated native package.
- [ ] Execute baseline and independently smaller He/PbLi ratings. Verify duties and source residual, meaningful capacity changes and unchanged supplied equipment.
- [ ] Execute 10% higher supplied depositions with original capacities held, changed exchange with total heat unchanged, and zero He friction with thermal duty reduced exactly once.
- [ ] Execute an unsupported He capability condition and ensure undefinedness prevents capacity credit; do not mislabel it physical shortage.
- [ ] Refuse negative/nonfinite heat inputs, negative net branch heat and invalid capacities through native execution; retain meaningful attempts.
- [ ] Compare native branch/ledger outputs with independent dimensional energy arithmetic and reused capacity behavior; run scoped validation and obtain completion review.

[AGENT] A successful result establishes two modeled heat branches and preserved capacity choices. It does not close hydraulic/equipment qualification, the omitted divertor circuit, conversion efficiency, electrical recirculation, costs or LCOE. T09 power conversion requires a separate supported contract after this item.
