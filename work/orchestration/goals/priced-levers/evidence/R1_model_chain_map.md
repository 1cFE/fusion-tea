# Round 1 evidence — the two levers as the model actually wires them

**Author:** the round agent, 2026-09-02, from a read-only survey of `models/` (subagent-assisted; every reference re-stated here was checked against the file). No native side effect.

Input to the WI-036 / WI-038 specs. The point of this file is that both levers are *more* disconnected than the goal's grounding assumed, and the two of them price through **different** channels — which decides how the increment is shaped.

## Lever 1 — `wp_side` reaches exactly one thing

`wp_side = 0.36` (`models/designs/stellarator_09/stellarator_plant.sysml:195`) has **one** consumer in the entire model:

- `models/library/analyses/mfe_magnet_field.sysml:81` — `out attribute sigma_wp : Real = k_sigma * I_coil * B_peak_in / wp_side;`
- asserted by `wp_stress_ok` (`models/library/analyses/mfe_viability.sysml:124`; wired `models/designs/generic_mfe/mfe_plant.sysml:936-939`).

Everything else it ought to touch, it does not:

| channel | state | reference |
|---|---|---|
| winding-pack volume → `vol_cold_cryo` | **broken.** `vol_cold_cryo = 136.56` is a held literal; the "(COMPUTED)" in its comment is a provenance claim about arithmetic done **by hand in the doc comment**, not a model computation | `stellarator_plant.sysml:686-704` |
| winding-pack cost | **cross-section blind.** `kAm_wind = n_coils * I_coil * f_set * c_coil / 1000`, `cost = kAm_wind * cost_per_kAm * f_wp_fab` — no area term | `models/library/analyses/mfe_magnet_cost.sysml:98,100` |
| magnet structure cost | **inert.** `cost = n_coils * m_casing * steel_price * f_steel_fab`, with `m_casing = 63000.0` held | `mfe_magnet_cost.sysml:135`; `stellarator_plant.sysml:219` |
| radial build | **absent, and inconsistent.** The build's coil layer is a *separate* held thickness `coil_t = 0.30`, cited to 1costingFE's geometry default — not to the Stellaris 0.36 m winding pack. Two independent statements of coil radial extent, from different sources, with no relation between them | `stellarator_plant.sysml:456` vs `:195` |

So today, widening the winding pack relieves stress and costs **exactly zero dollars, zero cold mass, and zero radial build**.

**The one live cost consequence already waiting for an input** is the cryo route: `vol_cold_cryo` → `mfe_cryo_plant.sysml:47` (`p_cold = (q_nuc * vol_cold * 1e-6 + p_fixed) * f_uplift`) → power-balance `p_cryo` (`mfe_plant.sysml:365`) **and** → `mfe_account_costs.sysml:588` (`cryo_cost = cryo_base * (p_cryo / p_cryo_ref) ** alpha`) → `cryoplant_capital` (`mfe_plant.sysml:955`). Connect `wp_side` to winding-pack volume and the cost consequence lands without inventing an account.

## Lever 2 — `B_max` reaches exactly one thing, and it is an inequality

`B_max = 24.9` (`stellarator_plant.sysml:164`, declared `models/library/cost_structure/mfe_power_core.sysml:96`) is consumed **only** by `peak_field_ok` (`mfe_viability.sysml:120`, `B_peak <= B_max_in`; wired `mfe_plant.sysml:929-933`). It enters no calc, no cost, no other constraint. Exhaustive grep over `models/` confirms it. Raising it is free in every channel.

The field chain it gates: `I_coil, n_coils, k_link, R0 → B_axis` (`mfe_magnet_field.sysml:45`) `→ × peak_ratio → B_peak` (`mfe_plasma_scaling.sysml:355`), and `B_peak` feeds both `peak_field_ok` and the stress operand above.

## The consequence: the two levers price through different channels

This is the finding that shapes the increment, and it corrects a loose assumption in the strategy revision ("raising the ceiling costs conductor"):

- **A wider pack at constant current does not buy more superconductor.** Ampere-metres are set by current and winding length; widening the cross-section adds structure, stabilizer and cold mass. So the existing ampere-metre-proportional conductor cost is *right* to be cross-section-blind, and `wp_side` must price through **cold mass (cryo), structure, and radial build** — not through the tape term.
- **A higher required field does buy more superconductor per ampere-metre**, because engineering current density falls with field, so more tape is needed to carry the same current. That lands on the **existing** `cost_per_kAm` term — `conductor_cost_rebco = 50.0 $/kA·m` in the pinned 1costingFE (`data/defaults/costing_constants.yaml:56`), on the `cost = total_kAm × $/kA·m × markup` path (`layers/cas22.py:427,442`). So the conductor-grade lever needs **`cost_per_kAm` to become a function of the required peak field**, not a new account.

That is the open research question `REQ-038-02`, and it is the one input the pinned source cannot supply on its own: 1costingFE prices REBCO at a single $/kA·m with no field argument, and its `MAGNET_TABLE` ceiling (`defaults.py:609-617`, `rebco_hts b_max = 23.0`) sits below the model's own 24.9 T.

## Standing rulings this touches

1. **`vol_cold_cryo` stays settable** — `[OWNER 2026-08-27]`, WI-032 R3, restated by the owner in this goal's grounding instruction. Reading taken: the ruling bars *retiring* it as a settable entry point; it does not bar giving it a computed default with the setter preserved. That is the same shape the owner drew for `p_pump` in the same instruction ("stays a held settable input — the ruling bars only the fixed-fraction form, not loop modelling"). Recorded here, and carried into the WI-036 spec as an explicit requirement rather than assumed.
2. **`k_sigma = 0.6102331403536223` was back-solved at `wp_side = 0.36`** (`stellarator_plant.sysml:198,203`). The constant and the proposed variable share an anchor point. Defensible — it is a stress *concentration* factor, not a size factor — but the spec must say so in words rather than let a reader assume the relation was independently sourced.
3. **`c_coil = 25.0` is the printed "typical" circumference** (`stellarator_plant.sysml:191`) and is the sole length term in magnet cost. Per the WI-036 mint record (`work/orchestration/goals/magnet-closure/trail.md:417-418`), geometry-derived winding length is the item's other half, and the expectation recorded there is "one held constant traded for a smaller one."
