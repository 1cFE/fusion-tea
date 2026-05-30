---
date: 2026-05-30T07:28:32-07:00
researcher: Claude
topic: "1costingfe library + current concept_analysis pipeline — context for redesign of analysis.md and model_setup.py"
tags: [research, costingfe, pipeline, concept-analysis, redesign, archetypes, overrides]
status: complete
last_updated: 2026-05-30
---

# Research: 1costingfe + Current Concept-Analysis Pipeline (for Redesign)

**Date**: 2026-05-30
**Researcher**: Claude
**Research Type**: Library reference + pipeline territory map

## Research Question

The user is about to redesign the `analysis.md` and `model_setup.py` stages of
`exploration/concept_analysis/`. Two issues drive the redesign:

1. **Inconsistent target** — sometimes FOAK data is fed into 1costingfe when the goal
   is a NOAK estimate.
2. **Stomping 1costingfe** — model_setup.py files override values that the library
   would compute fine on its own, defeating cross-concept consistency.

To support the redesign, the user wants:

- A precise reference for `1costingfe`: every enum/archetype, the required/expected
  inputs, the calculated defaults, the `cost_overrides` semantics, the
  `override_reference_mw` scaling mechanism, the `n_mod` feature, NOAK/FOAK behavior.
- A scoped map of the current pipeline (analyze + model_setup, plus surrounding
  loop, validators, review, extractor coupling) — to know what changes vs. what
  stays vs. what brittle joints to fix by design.

## Summary

- **1costingfe is sturdier than current pipeline treats it as.** Two construction
  enums (`ConfinementConcept`, `Fuel`) + a few config enums drive a YAML-defaults
  contract that is **already concept-aware**. The library has good per-concept
  defaults for geometry, BOP, finance, and most plant-wide CAS22 sub-accounts. The
  weak points where overrides really earn their place are concentrated in a small,
  named set of accounts (coils C220103, pulsed driver C220104, pulsed power
  supplies C220107, DEC C220109) and a handful of efficiency knobs.
- **NOAK vs FOAK is a binary `noak: bool`** at `model.forward()`, with discrete
  changes (contingency 10%→0%, $20M→$4M plant studies, FOAK-only licensing time
  addition, $10000→$75/kg PB11). There is **no learning curve / progress-ratio**
  modeling in the library; the multi-module labor factor (0.92) is the only
  fleet-effect. This makes the FOAK/NOAK lever simple but coarse.
- **Scaling via `override_reference_mw`** runs the model twice without overrides
  (at ref MW and target MW), takes per-account ratios, and rescales each user
  override before the final forward(). It is **per-account scaling**, not a single
  exponent — so it already handles the "BOP scales linearly but blanket scales
  ~0.6" reality correctly.
- **`n_mod`** is per-module physics + plant-aggregated BOP, with a single labor
  learning factor (0.92 for module 2+). It is NOT a fleet learning curve.
- **Current pipeline analysis.md template has no explicit FOAK/NOAK rule, no
  target-unit selection methodology, and no archetype-first framing.** The 8
  required output sections are data-availability-centric, not first-principles
  identity-centric. There is no upfront, deterministic mapping from concept to
  costingfe archetype — that mapping is implicit in `concepts.py:COSTINGFE_MAPPING`
  (a static dict) and otherwise reconstructed each iteration by Claude.
- **The biggest brittle joint in the loop is the F-N/VERDICT markdown contract**
  enforced by 3 separate regex validators + a SHA-hash "did Claude actually Edit"
  check. A structured-output contract collapses all of them.
- **The extractor does NOT regex-parse `analysis.md` body** (only frontmatter +
  one prose line `**Confinement Family**: ...`). The body is consumed by
  `extract_narrative` via `claude -p` — LLM-mediated. So the `analysis.md` schema
  can be redesigned freely from the extractor's standpoint.
- **`model_setup.py` contract is just three module-level names** (`model`,
  `result`, optionally `result_1gw` for non-1GW concepts) for costingfe, plus
  `params` + `results` for freeform. Everything else inside the script is
  redesign-free.
- **"Delete and regenerate one concept" is already safe**: knowledge data lives in
  `knowledge/concept_research/{id}/`, fully separate from
  `exploration/concept_analysis/analyses/{id}/`. The only hand-edited content
  inside `analyses/` is the user-filled `Decision:` / `User Notes:` fields in
  `review.md` PA-N blocks (Minor Fixes).

---

## Part A — 1costingfe Library Reference

Library root: `/home/reid/1cfe/1costingfe/`. Installed editable as `costingfe`.

### A.1 Package Layout

```
src/costingfe/
├── model.py             # CostModel — entry point (1141 LOC)
├── types.py             # ALL enums + dataclasses (ForwardResult etc) (296 LOC)
├── defaults.py          # CostingConstants + YAML loaders (436 LOC)
├── validation.py        # Pydantic CostingInput + physics checks (446 LOC)
├── adapter.py           # FusionTeaInput / run_costing wrapper (172 LOC)
├── layers/
│   ├── physics.py       # MFE & pulsed power-balance forward/inverse (994 LOC)
│   ├── tokamak.py       # 0D tokamak physics + disruption (684 LOC)
│   ├── radiation.py     # Brems/synch/line (293 LOC)
│   ├── geometry.py      # RadialBuild → component volumes (161 LOC)
│   ├── cas22.py         # Reactor plant sub-accounts (CORE costing) (475 LOC)
│   ├── costs.py         # CAS10/21/23-90 functions (482 LOC)
│   └── economics.py     # CRF, levelization, LCOE (67 LOC)
└── data/defaults/       # 16 per-concept YAMLs + costing_constants.yaml
```

`CostModel` constructor (`model.py:70-89`):

```python
CostModel(concept: ConfinementConcept, fuel: Fuel,
          costing_constants: CostingConstants = None,
          power_cycle: PowerCycle = PowerCycle.RANKINE,
          pulsed_conversion: PulsedConversion = None)
```

Derives `family` from `CONCEPT_TO_FAMILY`, defaults `pulsed_conversion` from
`CONCEPT_DEFAULT_CONVERSION`, loads engineering defaults from
`data/defaults/{family}_{concept}.yaml`.

Key public methods:

- `forward(net_electric_mw, availability, lifetime_yr, n_mod=1,
  construction_time_yr=6.0, interest_rate=0.07, inflation_rate=0.02,
  noak=True, cost_overrides=None, override_reference_mw=None, **overrides)
  -> ForwardResult` (`model.py:394`)
- `sensitivity(params, cost_overrides=None) -> dict` (`model.py:1064`) —
  JAX autodiff elasticities, partitioned into `{"engineering": ...,
  "financial": ..., "costing": ...}`
- `batch_lcoe(param_sets, params, cost_overrides=None) -> list[float]`
  (`model.py:1107`) — `jax.vmap` sweep.

Returned dataclasses (all in `types.py`):

- `ForwardResult` (`types.py:287`) — `power_table`, `costs`, `params`,
  `overridden` (list of overridden keys), `cas22_detail` (dict
  `C220101..C220700` + `C220000`), `plasma_state` (when 0D active).
- `CostResult` (`types.py:220`) — 21 fields `cas10..cas90`, plus
  `total_capital`, `lcoe` ($/MWh), `overnight_cost` ($/kW).
- `PowerTable` (`types.py:185`) — 23 power values + `e_driver_mj`,
  `e_stored_mj`, `f_rep`, `f_ch`.

### A.2 Enums / Archetypes — every value

**Required at construction**: `concept`, `fuel`. Everything else has defaults.

| Enum | Values | Source | Effect |
|---|---|---|---|
| `ConfinementFamily` | `STEADY_STATE`, `PULSED` | `types.py:5` | Dispatches power balance (`model.py:103-279`): SS uses MFE balance + radiation; pulsed uses driver/rep-rate. |
| `ConfinementConcept` | TOKAMAK, STELLARATOR, MIRROR, DIPOLE, LASER_IFE, ZPINCH, HEAVY_ION, MAG_TARGET, PLASMA_JET, PULSED_FRC, MAGLIF, THETA_PINCH, DENSE_PLASMA_FOCUS, STAGED_ZPINCH, ORBITRON, POLYWELL | `types.py:10` | Selects YAML defaults (`defaults.py:411`); coil geometry factor (`cas22.py:36-92`); driver model (`cas22.py:236-254`); volume formula (`geometry.py:94-145`); remote-handling scale (`cas22.py:338`); O&M scale (`costs.py:291`). |
| `PulsedConversion` | `THERMAL`, `INDUCTIVE_DEC` | `types.py:29` | Per-concept default `CONCEPT_DEFAULT_CONVERSION` (`types.py:53`). Selects pulsed branch (`model.py:241-274`) and C220109 formula (`cas22.py:306-322`). DEC bypasses thermal cycle (`eta_th=0`). |
| `Fuel` | DT, DD, DHE3, PB11 | `types.py:178` | Pervasive: blanket cost, shield scale, CAS21 buildings, CAS27 special materials, CAS40 owner, CAS50, CAS70 O&M, CAS80 fuel cost, core lifetime, licensing time. |
| `PowerCycle` | RANKINE (η=0.40), BRAYTON_SCO2 (0.47), COMBINED (0.53) | `types.py:172`, `defaults.py:420` | Sets `eta_th`, `turbine_per_mw`, `heat_rej_per_mw` (`model.py:443-454`). DEC concepts force `eta_th=0`. |
| `CoilMaterial` | REBCO_HTS ($50/kAm), NB3SN ($7), NBTI ($7), COPPER ($1) | `types.py:84-101` | `default_cost_per_kAm` feeds C220103 conductor (`cas22.py:202`). |
| `BlanketForm` | LIQUID_METAL (sf=1.0), MOLTEN_SALT (1.3), SOLID_BREEDER (1.2), NONE (0.0) | `types.py:104-131` | `structure_factor` multiplies C220101 (`cas22.py:160-165`). Constrains valid fills (`types.py:157`). |
| `BlanketFill` | PBLI (ff=1.0), LI (2.0), FLIBE (5.0), BE_CERAMIC (13.0), CERAMIC_ONLY (3.0), NONE (0.0) | `types.py:134-155` | `fill_factor` multiplies CAS27 (`costs.py:163`). |
| `WallMaterial` | TUNGSTEN, CARBON, BERYLLIUM, MOLYBDENUM, SIC, LITHIUM | `types.py:67` | Used only in impurity radiation model. **No direct cost impact** (TODO at `cas22.py:157`). |

**`CONCEPT_TO_FAMILY`** (`types.py:34`): TOKAMAK/STELLARATOR/MIRROR/DIPOLE/ORBITRON/POLYWELL → STEADY_STATE; others → PULSED.

**`CONCEPT_DEFAULT_CONVERSION`** (`types.py:53`): PULSED_FRC and THETA_PINCH default to INDUCTIVE_DEC; others to THERMAL.

**Concept "subtypes" inside cost code (not enums):**

- `_COIL_DEFAULTS` (`cas22.py:36-66`) — IFE/zpinch/heavy_ion/DPF/staged_zpinch get `None` → **C220103 = 0**.
- Coil geometry factor G (`cas22.py:71-92`): MIRROR/DIPOLE = `n_coils · 4π`; STELLARATOR = `4π² · path_factor`; default (tokamak) = `4π²`.
- Driver dispatch (`cas22.py:236-254`): LASER_IFE/HEAVY_ION/PLASMA_JET/STAGED_ZPINCH cost on `$/MJ` (e_driver_mj); MAG_TARGET costs on `$/MW` (p_driver); MAGLIF gets only laser preheat (driver electrical, in C220107); PULSED_FRC/THETA_PINCH/DPF/STAGED_ZPINCH → no target factory in C220108 (`cas22.py:290-296`).
- C220108 dropped from `replaceable_accounts` for non-steady-state (target factory is capex, not consumable; `model.py:751-752`).
- Electrode replacement (CAS72): STAGED_ZPINCH and PLASMA_JET only (`costs.py:361-376`).

### A.3 Input Contract

**Required at construction** — `concept`, `fuel`. No defaults.

**Required at `forward()`** — no working defaults:
- `net_electric_mw` (MW, `Field(gt=0)` `validation.py:80`)
- `availability` (per-concept default 0.85, mirror 0.87 via `default_availability` `validation.py:25`)
- `lifetime_yr` (validation default 40, forward has none — caller must pass)

**Customer parameters with sensible defaults** (passed to `forward()`):

| Param | Default | Source | Notes |
|---|---|---|---|
| `n_mod` | 1 | `model.py:399` | int ≥ 1. See A.5. |
| `construction_time_yr` | 6.0 | `model.py:400` | drives CAS60 IDC, CAS30 indirect. |
| `interest_rate` | 0.07 | `model.py:401` | CAS60, CAS90 CRF. |
| `inflation_rate` | 0.02 | `model.py:402` | levelizes O&M, fuel. |
| `noak` | True | `model.py:403` | FOAK adds licensing time, 10% contingency, 5× plant studies, B11 FOAK price. |

**Engineering parameters** filled from per-concept YAML via `load_engineering_defaults` (`defaults.py:411`). Tokamak YAML (representative) buckets:

**Geometric / physics** (m, T, m⁻³, keV):
- `R0`, `plasma_t`, `elon`, `chamber_length` (mirror), `blanket_t`,
  `ht_shield_t`, `structure_t`, `vessel_t`, `B`, `b_max`, `r_coil`,
  `n_e`, `T_e`, `Z_eff`, `plasma_volume`, `R_w`, `T_edge`, `tau_ratio`,
  `wall_material`.
- 0D-only: `q95`, `f_GW`, `M_ion`, `lambda_q`, `use_0d_model`.

**Engineering** (efficiencies, powers, MW):
- `p_input` (heating power), `p_nbi`/`p_ecrh`/`p_icrf`/`p_lhcd` (must sum
  to p_input if any provided; auto-nbi-fill is skipped).
- `mn` (neutron multiplier), `eta_p`/`eta_pin`/`eta_de`, `f_sub`,
  `f_dec`, `p_coils`/`p_cool`/`p_pump`/`p_trit`/`p_house`/`p_cryo`.
- `burn_fraction`, `fuel_recovery`, branching ratios
  (`dd_f_T`, `dd_f_He3`, `dhe3_dd_frac`, `dhe3_f_T`, `pb11_f_alpha_n`,
  `pb11_f_p_n`).
- Pulsed: `q_eng` (default 5.0 baked in `model.py:247,262`), `f_rep`,
  `p_target`, `f_rad`, `eta_dec`, `f_pdv`.
- Disruption (0D tokamak): `disruption_rate_base/_steepness/_damage/_downtime`.

**Configuration**: `blanket_form`, `blanket_fill`, `coil_material`
(default `"rebco_hts"` at `model.py:576`), `n_coils`, `pulsed_conversion`,
`power_cycle`.

**Validation tiers** (`validation.py`):
- T1 — pydantic `Field` constraints.
- T2 (`:198`) — if ANY engineering param set, ALL family-required must be
  set (`_COMMON_REQUIRED` + `_MFE_REQUIRED` or `_PULSED_REQUIRED`).
- T3 (`:236,277`) — runs power balance; errors on `rec_frac > 0.95`; warns
  on `Q_sci < 2`, `rec_frac > 0.5`; weird η warn; blanket form/fill
  compatibility; errors on DT with `blanket_form=NONE`; warns on aneutronic
  + breeding blanket.

### A.4 Calculated Defaults — Trust Tiers (the key insight)

**This is the section that drives the override policy.**

**From geometry → volumes** (`geometry.py:94-161`): given `R0`,
`plasma_t`, `elon`, `chamber_length` + radial-build thicknesses + concept,
the library computes 9 component volumes and firstwall area. Three formulas
dispatch by concept (torus shell for tokamak family; cylindrical ring for
mirror; spherical shell for pulsed/IFE/MIF). **Closed-form math — sturdy.**

**From power balance → all powers** (`_power_balance`, `model.py:103`):
inverts target `p_net` to find `p_fus`, `p_th`, `p_et`, `q_eng`, etc.
- MFE: `mfe_inverse_power_balance` (physics.py).
- Pulsed thermal: `pulsed_thermal_inverse`.
- Pulsed inductive DEC: `pulsed_dec_inverse` (η_th=0).
- 0D tokamak (`use_0d_model=True`): `tokamak_0d_inverse` derives p_fus
  from plasma physics given R0/a/κ/B/q95/f_GW (`model.py:281-392`).

Defaults for efficiencies (Rankine 0.40, eta_pin MFE 0.5, eta_pin laser
IFE 0.10, eta_de 0.85) are concept-specific and reasonable. **Override only
when concept publishes a measured value.**

**Per-account formulas (CAS22)** — full per-account drivers and trust tier:

| Account | Driver / Formula | Reference | Trust |
|---|---|---|---|
| C220101 Blanket+FW | `unit($/fuel) × form.sf × blanket_vol × (p_th/2500)^0.6` | `cas22.py:160` | **High** for DT (calibrated to pyFECONs); reasonable non-DT |
| C220102 Shield | `0.74 × shield_vol × shield_scale(fuel) × (p_th/2500)^0.6` | `cas22.py:178` | **High** DT, estimated non-DT |
| C220103 Coils | `total_kAm × $/kAm × markup`; `total_kAm = G·b_max·r_coil²/(μ₀·1000)`, concept-specific G | `cas22.py:189-215` | **LOW — override-heavy.** All depends on `(b_max, r_coil, n_coils, coil_material, markup)`. Dipole adds levitated coil term needing extras. |
| C220104 Heating/Driver | MFE: `nbi·p_nbi + icrf·p_icrf + ecrh·p_ecrh + lhcd·p_lhcd`. Pulsed: `$/MJ × e_driver_mj` (laser/heavy_ion/plasma_jet/staged_zpinch); `$/MW × p_driver` (mag_target); + laser preheat. | `cas22.py:224-254` | **High** ITER-class MFE (calibrated); **LOW** pulsed (NOAK-target estimates with high uncertainty) |
| C220105 Structure | `0.15 × structure_vol × (p_et/1100)^0.5` | `cas22.py:261` | High |
| C220106 Vacuum | `0.72 × vessel_vol × (p_et/1100)^0.6` | `cas22.py:268` | High |
| C220107 Power supplies | MFE: `80 × (p_et/1000)^0.7`. Pulsed: `c_cap_allin_per_joule × e_stored_mj`. | `cas22.py:276-280` | **LOW pulsed** (0.5 $/J NOAK, 0.5×–4× uncertainty per `defaults.py:106`) |
| C220108 Divertor/Target | MFE: `60 × (p_th/1000)^0.5`. IFE/MIF: `244 × (p_et/1000)^0.7`. Magnetized-only pulsed: 0. | `cas22.py:288-298` | Moderate; target factory estimates for IFE/MIF |
| C220109 DEC | INDUCTIVE_DEC: circuit markups on C220107 + grid-tie inverter. Electrostatic: `125 × (p_dee/400)^0.7`. | `cas22.py:306-322` | **LOW — HIGH UNCERTAINTY admitted in `defaults.py:92`** |
| C220110 Remote handling | `rh_base(fuel) × concept_scale × (p_et/1000)^0.5`; scale 1.0 (tokamak/stellarator), 0.55 mirror, 0.5 other | `cas22.py:331-344` | Moderate |
| C220111 Installation | `0.14 × reactor_subtotal` | `cas22.py:363` | High (industry-norm) |
| C220112 Isotope sep | 0 (embedded in CAS80 fuel price) | `cas22.py:372` | Intentional |
| C220200 Coolant | `166·(p_net_total/1000) + 40.6·(p_th_total/3500)^0.55` | `cas22.py:383` | High |
| C220300 Aux cooling+cryo | `1.10e-3 · p_th_total + 200 · (p_cryo/30)^0.7` | `cas22.py:392` | High (ITER cryoplant) |
| C220400 Rad waste | `1.96 · (p_th_total/1000)` | `cas22.py:401` | High |
| C220500 Fuel handling | `fh_base(fuel) · (p_net_total/1000)^0.7` | `cas22.py:417` | High |
| C220600 Other | `11.5 · (p_net_total/1000)^0.8` | `cas22.py:423` | High |
| C220700 I&C | `85 · (p_th_total/3500)^0.65` | `cas22.py:430` | High |

**Other accounts (`costs.py`):**
- CAS10: land (∝√n_mod) + permits + licensing-by-fuel + plant studies (FOAK $20M / NOAK $4M) + contingency (`costs.py:47`).
- CAS21: per-building YAML table × fuel-specific cost × scaling basis at 1 GWe ref (`costs.py:65`, YAML in `data/defaults/costing_constants.yaml`).
- CAS23: `n_mod × p_the × turbine_per_mw` (cycle-dependent, zero when DEC).
- CAS24/25/26: linear in p_et or p_th × per-MW coefficient.
- CAS27: `special_materials_fuel × fill_factor × (p_net/1000)`.
- CAS28: fixed $5M.
- CAS40: `owner_cost(fuel) × (p_net/1000)^0.5`.
- CAS50: spares + startup fuel + decom + shipping + tax + insurance.
- CAS60: closed-form IDC on interest+construction.
- CAS70 = CAS71 (O&M, fuel × concept_scale × √p_net) + CAS72 (PV-discounted scheduled replacement of `replaceable_accounts` + DEC grid + cap bank + electrodes).
- CAS80: cost-per-reaction × annual reactions × burn-fraction loss correction.
- CAS90: `CRF(i, lifetime) × total_capital`.

#### A.4.1 Trust ranking (override policy implications)

**High trust — LEAVE DEFAULTED:**
- Geometry volumes (closed-form math).
- BOP coefficients CAS23-26 (ARIES/NETL-calibrated, `defaults.py:200-203`).
- CAS28 (fixed $5M).
- CAS60 (closed-form finance).
- CAS90 (closed-form finance).
- Plant-wide CAS22 sub-accounts (C220200-C220700) — well-calibrated power-law fits.
- Multi-unit labor factor (fission-derived 0.92).

**Medium trust — override if concept-specific data available:**
- C220101/102/105/106 volume-based (calibrated to DT tokamak; non-DT scales are estimates).
- C220108 divertor (calibrated for MFE; estimated for IFE/MIF target factory).
- CAS21 buildings (1 GWe reference; scaling reasonable but plant-architecture-specific).
- CAS40/50/70 staffing-based (fuel-specific but plant-class-specific).

**Low trust — OVERRIDE-ESSENTIAL when concept differs from YAML defaults:**
- C220103 coils (b_max, r_coil, n_coils, coil_material, markup — concept-design-specific).
- C220104 pulsed drivers ($/MJ NOAK targets, high uncertainty — `defaults.py:60-70`).
- C220107 pulsed power supplies (`c_cap_allin_per_joule` 0.5–4.0 range).
- C220109 DEC (HIGH UNCERTAINTY admitted).
- DEC grid lifetimes (factor-3 uncertainty, `defaults.py:96`).
- Cap shot lifetime, electrode shot lifetime (1e7–1e9 range).
- `coil_markup`, `n_coils` for non-standard concepts.

### A.5 Cost Overrides

`cost_overrides` dict to `forward()` (`model.py:404`):

| Key | Unit | Effect |
|---|---|---|
| `CAS10` | M$ | Replaces computed value (`model.py:557`) |
| `CAS21` | M$ | Replaces (`:563`) |
| `CAS22` | M$ | Replaces total; **also rescales all C2201xx/C2202xx sub-accounts proportionally** so CAS72 replacement reflects it (`:678-688`) |
| `CAS23` | M$ | (`:690`) |
| `CAS24/25/26/27/28` | M$ | (`:694-713`) |
| `C220101..C220112`, `C220200..C220700` (NOT `C220000`) | M$ | Replace sub-account; CAS22 total then recomputed from patched detail with n_mod multiplication and labor discount (`:642-676`) |

**Only top-level CAS10-28 and CAS22 sub-accounts are overridable.** CAS29,
CAS30, CAS40, CAS50, CAS60, CAS70/71/72, CAS80, CAS90 are computed and
cannot be overridden (comment at `model.py:829-836`).

**Semantics**: pure replacement of the computed M$ value. No additive mode.
For CAS22 the override rescales the detail dict, which preserves the
replaceable-accounts CAS72 chain.

**Unit forms**: overrides are always in M$. Per-unit forms ($/kAm, $/J)
are exposed only via `costing_overrides` on `CostingConstants`
(`adapter.py` / `FusionTeaInput`), which mutates underlying constants via
`cc.replace(**costing_overrides)`. Per-sub-account dollar overrides
bypass formulas entirely.

### A.6 Scaling: `override_reference_mw`

Method: `_scale_overrides` at `model.py:849-896`.

**Mechanism (step-by-step):**

1. User passes `cost_overrides` valid at `override_reference_mw` (e.g. a 400 MWe study) and a `net_electric_mw` target (e.g. 1000 MWe).
2. `forward()` intercepts before merging params and calls `_scale_overrides`.
3. `_scale_overrides` runs `self.forward(net_electric_mw=reference_mw, cost_overrides=None, ...)` and `self.forward(net_electric_mw=target_mw, cost_overrides=None, ...)` — two full computations (recursive, but no infinite loop because overrides=None).
4. For each override key, looks up the computed value at ref and target via `cas22_detail[key]` or `_OVERRIDE_TO_ATTR` for top-level CAS.
5. Scaled value = `user_value × (target_computed / reference_computed)`.
6. If `ref_computed == 0` (account absent for the concept, e.g. CAS28 fixed): passes through unscaled.
7. Returns scaled dict; proceeds to normal `forward()` flow.

**Effective per-account scaling exponents** (derived from formulas — the actual exponents the scaler applies):

| Account | Driver | Exponent |
|---|---|---|
| CAS10 | √n_mod·p_net land + fixed | ~linear in p_net (small) |
| CAS21 | mixed (fixed + p_et/p_fus/p_th/p_the) | linear |
| CAS22 | composite | ~0.5–0.8 |
| CAS23 | p_the | linear |
| CAS24/25 | p_et | linear |
| CAS26 | p_th | linear |
| CAS27 | p_net | linear |
| CAS28 | fixed | 0 |
| C220101/102 | volume × (p_th)^0.6 | ~0.6 + vol |
| C220103 | b_max, r_coil — **invariant under p_net** unless geometry overridden | ~0 |
| C220104 | p_input (MFE) or e_driver (pulsed) | linear |
| C220105 | (p_et)^0.5 + vol | ~0.5 |
| C220106 | (p_et)^0.6 + vol | ~0.6 |
| C220107 | (p_et)^0.7 (MFE) / e_stored (pulsed) | 0.7 |
| C220108 | (p_th)^0.5 or (p_et)^0.7 | 0.5–0.7 |
| C220110 | (p_et)^0.5 | 0.5 |
| C220500 | (p_net)^0.7 | 0.7 |
| C220600 | (p_net)^0.8 | 0.8 |
| C220700 | (p_th)^0.65 | 0.65 |
| BOP CAS23-26 | linear in p_th/p_et | 1.0 |

Plant-aggregate scaling lands in 0.6–0.8 (chemical-engineering norm).
Consistent with `examples/scaled_overrides.py`.

**Pitfalls:**
- Scaler runs the model twice without overrides (`model.py:865-870`). If
  the base model fails (validation, power balance) at either ref or
  target, scaling fails.
- If `ref_computed = 0`, scaler silently passes the override unscaled
  (`:892-894`).
- If `ref_mw` is far below thermal-balance breakeven, inverse power
  balance can produce nonsensical p_fus (rec_frac > 0.95 raises).
- **Geometry is held constant across ref→target** — the radial build
  doesn't grow with power. The scaler assumes you keep the same machine
  geometry and only stretch BOP. For a different machine you must rebuild.
- Override keys not in `_OVERRIDE_TO_ATTR` and not in `cas22_detail`
  silently pass unscaled.

### A.7 N_MOD (Multi-Module Plants)

`n_mod: int` (default 1). Encodes a single plant site with N identical reactor modules totaling `net_electric_mw`.

**Per-module vs plant-wide accounting:**

- Power balance per-module: `p_net_per_mod = net_electric_mw / n_mod` (`model.py:105`). Physics, geometry, and per-module CAS22 sub-accounts at per-module size.
- Per-module equipment keys (`model.py:642-655`): C220101..C220112; each × n_mod for total.
- Plant-wide keys (`:656-663`): C220200..C220700, use totals `n_mod * p_th`, `n_mod * p_net`.
- Labor C220111: `c220111 × (1 + (n_mod−1) × multi_unit_labor_factor)`, default 0.92 → second module is 92% of first (`cas22.py:451`, `defaults.py:155-164`). **This is the only learning curve in the library** — explicitly NOT Wright's Law.
- CAS10 land: `land_intensity × p_net × √n_mod × land_cost` (`costs.py:49`), sub-linear in n_mod.
- CAS23-26: `n_mod × per-MW × power` (linear in n_mod).
- CAS40, CAS50, CAS70, CAS80: scale with total p_net.
- CAS72 scheduled replacement: cost-per-event × n_mod.

Common N: examples use {1, 2, 4} (`examples/multi_module.py`). No upper limit.

### A.8 NOAK vs FOAK

`noak: bool` (default True). Discrete toggle, no learning curve:

- Contingency: FOAK 10%, NOAK 0% (`defaults.py:209-211`). Affects CAS10, CAS21, CAS29, CAS50.
- Plant studies (CAS10): FOAK $20M, NOAK $4M (`defaults.py:18-19`).
- Licensing time (FOAK only, fuel-dependent): adds to project time for levelization basis (`costs.py:36-39`).
- B-11 price (CAS80, PB11 only): FOAK $10000/kg, NOAK $75/kg (`defaults.py:259-262`).

No general progress ratio. Just binary.

### A.9 Other Notable Features

**Sensitivity** (`model.sensitivity`, `model.py:1064`): returns `{"engineering", "financial", "costing"}` elasticities (dLCOE/LCOE × p/dp). Implemented via `jax.grad` autodiff (`:1084`). Closed-over `cost_overrides` get zero gradient.

**Power Table** (`PowerTable`, `types.py:185`): 23 power values (MW) + pulsed energies. Use to verify physics convergence before trusting LCOE.

**Adapter / `FusionTeaInput`** (`adapter.py`): string-typed wrapper for pipeline integration. Accepts `cost_overrides` (M$) AND `costing_overrides` (modifies `CostingConstants`). Returns flat dicts. **Use this when integrating with fusion-tea** if you want per-unit-cost overrides.

#### Footguns

- `compare_all` (`__init__.py:48`) catches all exceptions silently — non-viable combinations vanish.
- JAX-traced floats: `forward()` skips pydantic validation when any param is a `jax.Tracer` (`model.py:479-512`).
- `q_eng` defaults to 5.0 in pulsed branch (`model.py:247,262`) if not in YAML — silent.
- `eta_th=0` is forced for INDUCTIVE_DEC unless explicitly overridden (`model.py:445-447`), zeroing CAS23 and the thermal cycle entirely.
- `p_trit=0` auto-applied for non-DT fuels (`model.py:471-472`).
- `r_coil` is **not** the radial-build vessel radius — it's an independent calibration parameter (default 1.85 m, `model.py:574`).
- DT + `blanket_form=NONE` raises ValueError (`validation.py:297-305`).
- 0D model is tokamak-only (`validation.py:224`).
- `override_reference_mw` runs forward() twice without overrides — silent perf hit + failure surface if bare model can't converge at either scale.
- `CAS22` override rescales the entire `cas22_detail` proportionally — overriding `CAS22` does NOT preserve individual sub-account distribution; it scales every sub-account by the same factor (`model.py:683-688`).

### A.10 Recommended Classification Inputs (for upstream archetype mapping)

For the deterministic up-front concept→1costingfe table the user wants to build, the **minimum sufficient classification** is:

1. `concept` (ConfinementConcept) — drives family, coil geometry, driver dispatch, volume formula. **Required**.
2. `fuel` (Fuel) — drives blanket cost, shield, materials, licensing, O&M, lifetime. **Required**.
3. `pulsed_conversion` — only for PULSED concepts; usually defaultable.
4. `power_cycle` — Rankine default; override to BRAYTON_SCO2 only if concept publishes Brayton design.
5. `blanket_form` + `blanket_fill` — constrained by Fuel (DT must have non-NONE; aneutronic should be NONE).
6. `coil_material` — only for coil-bearing concepts.
7. Geometric inputs (R0, plasma_t, elon, chamber_length, blanket_t, b_max, r_coil, n_coils) — override only when concept publishes specific values that differ from YAML defaults.
8. Pulsed concepts: q_eng, f_rep, c_cap_allin_per_joule.

**Override-essential cells** (when concept differs from YAML defaults): C220103 coils, C220104 pulsed driver, C220107 pulsed power supplies, C220109 DEC, efficiencies with concept-specific data.

**Leave defaulted (sturdy):** BOP CAS23-26, CAS28, CAS60, CAS90, plant-wide CAS22 sub-accounts, geometry math, FOAK/NOAK discrete flags.

---

## Part B — Current Pipeline Territory

Pipeline root: `exploration/concept_analysis/`. Concepts in `analyses/{id}-{slug}/`. Templates in `prompt_templates/`. Drivers in `scripts/`.

### B.1 Stage Inventory

CLI subcommands in `scripts/run_analysis.py:1388-1520`:

| # | Stage | Subcommand | Handler |
|---|---|---|---|
| 0 | list/status | `list`, `status` | `:100,114` |
| 1 | Gap-check | `gap-check` | `:196` |
| 2 | Analyze (iterative loop) | `analyze` | `:279` → `lib/loop.py:55` |
| 3 | Model-setup (standalone) | `model-setup` | `:418`; loop runs it in-band at `loop.py:575` |
| 4 | Review | `review` | `:501` |
| 5 | Address-review | `address-review` | `:616` |
| 6 | Synthesize | `synthesize` | `:753` |
| 7 | Approve | `approve` | `:894` |
| 8 | Add-source | `add-source` | `:951` |
| 9 | Score (§8 append) | `score` | `:1103` |
| 10 | Extract-scores | `extract-scores` | `:1226` |
| 11 | Calibrate | `calibrate` | `:1264` |
| 12 | Heatmap | `heatmap` | `:1355` |

Plus feedback-producer `source_integration` (`loop.py:822`) and `research` (`lib/research.py`, opt-in `--research`).

### B.2 Stage → input → output → template → validator

| Stage | Inputs | Output | Template | Validator |
|---|---|---|---|---|
| gap-check | dossier, sources, SOURCE_INDEX | `gap_report.md` | `gap_check.md` | `validate_non_empty` |
| analyze cold-start | dossier, sources, exemplars, approved, template, memory, landscape | `analysis.md` + `iter-N/*` | `analysis_v2.md` (cold_start) | `validate_non_empty` |
| analyze feedback-pass | existing `analysis.md`, `iter-N/pre_feedback.md`, sources | rewritten `analysis.md` | `analysis_v2.md` (feedback_pass) | `make_file_modified_validator` (sha256) |
| model-setup standalone | `analysis.md`, costingfe example/defaults/readme | `model_setup.py` + `model_output.txt` | `model_setup_costingfe.md` or `_freeform.md` | `validate_python_syntax` |
| model-setup in-loop | + prior iter's model + `pre_feedback.md` | `iter-N/model_setup.py` + `model_output.txt`; copied to root on `model_ok` | `*_edit.md` if prior exists | tiered: syntax only OR chain(file_modified, syntax) when `has_model_category_findings` |
| assess (in loop) | `analysis.md`, `model_output.txt`, landscape | `iter-N/post_feedback.md` | `assessment.md` + `config/*` | `validate_feedback_verdict` |
| source-integration | new sources detected, `analysis.md` | `iter-N/source_integration_output.md` | `source_integration.md` | `validate_feedback_verdict` |
| research | gap report, web | `research_output.json` + extracted sources | `research.md` | TODO |
| review | `analysis.md`, `model_setup.py`, `model_output.txt`, sources, approved syntheses | `review.md` (sets `Review-Status` frontmatter) | `review.md` | `validate_review_verdict` |
| address-review | `review.md` (user-filled Decisions), `analysis.md` | edited `analysis.md` + `address_log.md` | `address_review.md` | `make_file_modified_validator` |
| synthesize | `analysis.md`, `gap_report.md`, model artifacts, prior syntheses | `synthesis.md` | `synthesis.md` | `validate_score_output` |
| approve | `analysis.md`, `synthesis.md` | mutates frontmatter `Status=approved` | — | — |
| score | `synthesis.md`, `analysis.md`, `gap_report.md`, model artifacts | appends §8 LCOE-downselect to `synthesis.md` | `score.md` + `config/scoring_framework.md` | `validate_score_output` |
| extract-scores | all `synthesis.md` §8 | `scores/verified_scores.{json,md}` | — | YAML parse |
| calibrate | `verified_scores.md` | `scores/calibrated_scores.{json,md}` | `calibrate.md` | `validate_calibration_output` |
| heatmap | calibrated scores | `heatmap.html` | — | — |

### B.3 The `analysis.md` stage (close read)

Template: `prompt_templates/analysis_v2.md`. Three modes (cold_start / feedback_pass / self_advance) via Mustache booleans (`:51,123,172`). The loop only sets cold_start (iter 1) or feedback_pass (iter ≥ 2).

**Template sections (prompt structure):**
1. Analysis Goals (transcluded `config/analysis_goals.md:1-25`) — 5 goals: Concept Positioning, Key Differentiators, TEA Implications, Modeling Approach, Risks/Assumptions.
2. Quality Standards (`config/quality_standards.md`).
3. Per-Source Reading Pattern — mandates subagent per source (`:14-27`).
4. Optional Cross-Concept Memory (`:29-38`).
5. Optional Concept Landscape (`:40-49`).
6. Mode-specific Required Reading list.
7. Cross-Concept Reuse block listing `approved_analyses` paths (`:200-209`).

**Output structure** (`prompt_templates/output_template.md`): 8 required sections:
1. Availability of Data
2. Challenges in Capturing System Function
3. Maturity of Key Subsystems and Components
4. Key Materials and Supply Chain
5. **LCOE-Relevant Parameters** (table + Missing sub-table)
6. Data Gap Inventory
7. Cross-Concept Notes
8. Sources

**What the template DOES NOT say (gaps the redesign should fill):**
- **FOAK vs NOAK** — not in `analysis_v2.md` or `output_template.md`. Lives in `model_setup_costingfe.md` examples only.
- **Target unit selection** — not in analysis template. Lives in `model_setup_costingfe.md:47-89`.
- **Source priorities (company vs reference)** — not articulated; emerges only from Required Reading ordering.
- **`Reuses:` frontmatter** — Claude is told to edit frontmatter and replace `Reuses: []` with concept IDs (`analysis_v2.md:112-120`). Pre-seeded by `lib/frontmatter.py:make_frontmatter`. Not validated.
- **Scaling** — not in analysis template.
- **"Essence" / first-principles identity** — no explicit framing. Section 1 of output is data-availability, not identity. Sections 3-4 cover distinctiveness data-centrically.

**In-the-wild samples:** `01.../analysis.md`, `04.../analysis.md` (HB11), `12.../analysis.md` confirm the 8-section structure even for freeform concepts.

### B.4 The `model_setup.py` stage (close read)

Templates routed by `lib/concepts.py:get_model_path` (static `COSTINGFE_MAPPING`; freeform = anything not mapped):

| Path | Template |
|---|---|
| costingfe, cold start | `model_setup_costingfe.md` |
| costingfe, prior exists | `model_setup_costingfe_edit.md` |
| freeform, cold start | `model_setup_freeform.md` |
| freeform, prior exists | `model_setup_freeform_edit.md` |

**`model_setup_costingfe.md:91-123`:**
- Structure: docstring → imports → constants → `model.forward(...)` → results print → assumptions → sensitivity.
- Output interface (`:102-111`): module-level `model` and `result` are CRITICAL; extractor imports and `getattr`s these.
- Traceability (`:112-118`): every parameter and override must carry inline citation.
- Anti-hallucination (`:120-123`): overrides MUST be justified from analysis; unknown costs use framework defaults with `# DEFAULT:` comment.

**Threshold for "override or not"**: **not articulated.** No explicit rule like "override only if concept-specific value differs from default by >X%." Decision is per-parameter, defended by inline comment.

**`_NOAK_OVERRIDES` pattern**: **convention, not enforced.** Plain literal dict (e.g. concept 01:
```python
_NOAK_OVERRIDES = {
    "C220103": round(C220103_OVERRIDE, 1),   # Magnets+structure
    "C220101": round(C220101_OVERRIDE, 1),   # FLiBe blanket
    "C220106": round(C220106_OVERRIDE, 1),   # Vacuum vessel
    "CAS27":   CAS27_OVERRIDE,               # FLiBe inventory
}
```
Used in `forward(cost_overrides=_NOAK_OVERRIDES)` and `sensitivity(... cost_overrides=_NOAK_OVERRIDES)`. FOAK scenario re-declares `_FOAK_OVERRIDES` separately + parallel `result_foak = model.forward(..., noak=False)`. **Not toggleable.** Multi-scenario = multiple dicts + multiple forward() calls.

**Override volume in the wild**: concept 01 (440 lines) has 4 cost overrides + NOAK + FOAK scenarios + sensitivity. Concept 12 freeform (1142 lines) carries reasoning via dataclass docstrings. Concept 04 costingfe (338 lines) carries it in docstring header.

**"What-if" / sweeps**: just parallel `forward()` calls — `result` is baseline; `result_foak`, etc. are scenarios. **Extractor only consumes `result` (plus `result_1gw`)** — other scenario names are print-only.

### B.5 Consistency Checks / Validators

`scripts/lib/validators.py`. Harness: `lib/claude.py:invoke_claude_validated` (retry-on-fail with `fix_message` re-prompt).

| Validator | Where | Method | Catches | Brittleness |
|---|---|---|---|---|
| `validate_non_empty` (`:187`) | gap-check, analyze cold | strip non-empty | empty output | Low |
| `validate_python_syntax` (`:208`) | model-setup | `compile()` | broken Python | Low — **does NOT check for `result`/`model`/`result_1gw`** |
| `make_file_modified_validator` (`:230`) | feedback analyze, address-review, model-setup edit | sha256 snapshot | Claude returned without Edit | Robust |
| `validate_feedback_verdict` (`:61`) | assess, source-integration | regex `^VERDICT: (PASS|FINDINGS)$`, `^### F-\d+:`, `^- \*\*Category:?\*\*:?\s*(analysis|model)` | missing verdict/finding/category | **MED-HIGH** — 3 separate format invariants on free-form markdown |
| `validate_review_verdict` (`:125`) | review | regex `^VERDICT: (PROCEED|REVISE)$`, `## Corrective Actions`, F-N blocks | missing verdict / actions | Same class |
| `validate_calibration_output` | calibrate | parses markdown score table | unparseable | High — LLM table parse |
| `validate_score_output` | synthesize, score, calibrate | YAML-in-markdown parse | invalid YAML / missing fields | High |
| `has_model_category_findings` (`:297`) | gating in loop | regex `FINDING_CATEGORY_RE` | which validator tier to use | Conservative on missing |
| `parse_proposed_actions` | address-review | regex on `## Minor Fixes` PA-N | malformed PA-N | Medium |

#### B.5.1 Brittle joints worth fixing by design

1. **Regex-enforced verdict + finding format** (`validators.py:22-38`) used 3× → **replace with structured output** (JSON `{verdict, findings: [{category, ...}]}`).
2. **`make_file_modified_validator`** compensates for the Edit-tool prose contract. Drop the contract → drop the validator.
3. **`validate_score_output`/`validate_calibration_output`** — YAML-in-markdown → structured output.
4. **`parse_proposed_actions`** — PA-N markdown with hand-filled Decision/User Notes → CLI prompt or HTML form.
5. **`output_template.md` 8-section presence** — not enforced. Template scaffolding (prewritten skeleton headers) makes absence impossible.
6. **`Reuses:` populated by Claude via Edit tool** (`analysis_v2.md:112-120`) — not validated. Move to explicit structured output.
7. **Module-level `result`/`result_1gw` discipline** — template prose only; Python syntax check doesn't see it. AST check or explicit interface module.
8. **`**Confinement Family**: ...` prose-line regex** (`extract_explorer_data.py:89-91`) — single point of failure. Move to frontmatter.

### B.6 Loop / Feedback Machinery

Entry: `lib/loop.py:run_stage1_loop` (`:55`) from `cmd_analyze`.

**Per-iteration body** (`:108-286`):
1. Refresh sources (`:113`).
2. Feedback-producer dispatch in priority order (`:117-206`): external `--feedback` → cold-start → review kick-back (frontmatter `Review-Status=revise`) → source-integration → research → default (prior iter's `post_feedback.md`).
3. Analyze (cold or feedback) (`:208-226`).
4. Capture `iter-N/analysis_output.md` (`:229`).
5. Model-setup in-iter (`:232`) with `_find_best_prior_model` (`:546-572`) selecting prior model_ok=True iter.
6. Promote `iter-N/{model_setup.py,model_output.txt}` to canonical iff `model_ok` (`:945-970`).
7. Assess (`:747-819`) → immutable `post_feedback.md`.
8. Write `verdict.json` (`:255-260`).
9. `propagate_staleness` (`:273`).
10. Terminate on PASS or `iter_num >= max_passes`.

**State between iterations**: iter-N/ dirs, `LoopState` (`lib/iteration.py:33-55`), canonical files at concept root, frontmatter (Review-*).
**Between concepts**: none — except read-only cross-concept context (`find_approved`, `find_approved_syntheses`, memory, `build_concept_landscape`).

**Kill switches**: `--force` (nukes iter-*/ via `clear_iterations`); `--resume`; `--add-passes N`; `--feedback PATH`; `--max-passes 1` (short-circuits assess to `SINGLE_PASS`).

### B.7 Review Process

Two reviewers + human:

**A. In-loop `assess`** (every iteration) — `assessment.md` + transclusions. Scope is "shape of concept" (positioning, differentiators, TEA, modeling, risks) plus numerical plausibility if `model_output.txt` exists. Output `iter-N/post_feedback.md` with VERDICT and up to 3 findings each tagged `Category: analysis|model`. Feeds next iteration.

**B. Standalone `review`** (post-loop) — `prompt_templates/review.md`. 5 dimensions: Modeling Approach, Strategic Positioning, Risk Framing, Data Sufficiency, Cross-Concept Consistency. Output `review.md`:
- VERDICT: PROCEED → `## Minor Fixes` PA-N blocks (user fills Decision/User Notes).
- VERDICT: REVISE → `## Corrective Actions` F-N blocks; user runs `analyze --resume` and the loop reads `review.md` corrective actions via `_get_review_feedback`.

**C. Human review** — manually edits PA-N Decisions in `review.md`. `cmd_address_review` refuses without at least one Decision set.

**Gating**: `cmd_synthesize` needs `Review-Status in (addressed, clean, proceed)`. `cmd_approve` needs same + synthesis.md exists.

### B.8 Starting-Fresh Mechanics

`analyses/{id}/` contents — all derivable except user-filled review Decisions:

| Artifact | Derivable? | Owner |
|---|---|---|
| `analysis.md` | Yes (analyze) | pipeline |
| `gap_report.md` | Yes (gap-check) | pipeline |
| `model_setup.py` | Yes (model-setup) | pipeline |
| `model_output.txt` | Yes | pipeline |
| `review.md` | Yes; user-filled Decisions if PROCEED+Minor Fixes | pipeline + user |
| `address_log.md` | Yes | pipeline |
| `synthesis.md` | Yes (synthesize + score) | pipeline |
| `iter-*/` | Yes | pipeline |

**Research data is OUTSIDE** `analyses/`: `knowledge/concept_research/{id}/`. Dossier via `lib/sources.py:get_dossier_path(rid)`; sources via `find_sources(rid)`. **Safe to delete `analyses/{id}/` without touching knowledge.**

**Cross-concept dependencies at generation time:**
- `Reuses:` frontmatter is a documented-and-cite link, not an import. Deleting 17a does not break 17b's analysis content.
- `approved_syntheses` cross-context read by review, synthesize, score, calibrate — read-only.
- Concept landscape (`build_concept_landscape`) reads all concepts' state — shifts what Claude sees but doesn't break.
- **No concept reads another concept's `model_setup.py` or `model_output.txt`** at generation time.

**Smallest safe regenerate sequence:**
```bash
rm -rf exploration/concept_analysis/analyses/{ID}/
uv run python exploration/concept_analysis/scripts/run_analysis.py gap-check {ID}
uv run python exploration/concept_analysis/scripts/run_analysis.py analyze {ID}
uv run python exploration/concept_analysis/scripts/run_analysis.py review {ID}
# user edits review.md if PROCEED+Minor Fixes
uv run python exploration/concept_analysis/scripts/run_analysis.py address-review {ID}
uv run python exploration/concept_analysis/scripts/run_analysis.py synthesize {ID}
uv run python exploration/concept_analysis/scripts/run_analysis.py score {ID}
uv run python exploration/concept_analysis/scripts/run_analysis.py approve {ID}
```

Lighter form: keep `gap_report.md` (one-shot, expensive, doesn't iterate); delete the rest and re-run from `analyze`.

`--force` on `analyze` calls `clear_iterations` (`loop.py:83`); does NOT delete `analysis.md` first — cold-start overwrites.

### B.9 Extractor coupling (what schema-changes break)

The extractor consumes `analysis.md` in **two ways**:

1. **Regex on body**: ONE line — `**Confinement Family**: ...` (`extract_explorer_data.py:89-91`). Plus frontmatter (`parse_frontmatter` at `:822`).
2. **LLM-mediated `extract_narrative`** (`:723-741`): runs `claude -p` with full `analysis.md` text in a JSON-extraction prompt to produce `NarrativeData(key_bets, eliminated_costs, novel_costs, risks)`. **Robust to any markdown restructure** — consumer extracts meaning.

So `analysis.md` body schema can change freely **except**:
- YAML frontmatter must stay (and its key fields: Status, Approved-Date, Reuses, Review-Status, Review-Iterations, Last-Review).
- The `**Confinement Family**: ...` prose line must stay — **OR be moved into frontmatter and the regex updated** (recommended; that's a brittle joint).

The extractor parses `model_setup.py` via **module-level attribute access only** — `model`, `result`, optional `result_1gw`, optional `scaled_headline` for costingfe; `params` + `results` for freeform. No AST. So `model_setup.py` body is redesign-free as long as those names remain.

---

## Architecture Insights

### Where the library already does the right thing

- **Per-account scaling exponents are correct.** `override_reference_mw` uses the model's own ratios — no need for a single-α post-hoc factor. (Prior migration `.project/research/20260419-costingfe-scaled-overrides-integration.md` already wired this in.)
- **Concept-aware defaults via YAML** (`data/defaults/{family}_{concept}.yaml`) — the library shifts defaults by concept. Existing per-concept YAMLs cover 16 concepts.
- **NOAK/FOAK is a single boolean** with discrete sensible jumps. The redesign's "always target NOAK" rule maps to `noak=True` everywhere.
- **Scaling to 1 GW**: pass `net_electric_mw=1000` and `override_reference_mw=<native>` to the second `forward()`. The dual-result pattern is already in production for 8 concepts (concept 01 et al).

### Where the pipeline fights the library

- **Overrides in current `model_setup.py` files cover high-trust accounts.** Looking at concept 01: 4 overrides in `_NOAK_OVERRIDES`. Some (C220103 coils, CAS27 FLiBe) are correctly in the override-essential bucket; others (C220101 blanket, C220106 vacuum) are MEDIUM-trust accounts where the library would compute a defensible value from geometry. The override "stomping" the user worries about is real and concentrated in MEDIUM-trust accounts that get overridden without strong concept-specific justification.
- **Override choices are not toggleable.** A single dict; flipping baseline ↔ scenario requires editing the dict or duplicating the forward() call. The user's proposed `[(category, ON/OFF)]` format would fix this with minimal disruption.
- **FOAK/NOAK consistency is not enforced.** Some concepts compute overrides on FOAK data (whatever the company released) and feed them to a model run with `noak=True`. There is no template rule, no validator, no review-time check.

### Brittle markdown contracts dominate validator complexity

Of 9 active validators, 5 are LLM-markdown-parsing regex (verdict, findings, score YAML, calibration YAML, PA-N). A single structured-output contract (Claude returns JSON for assess/review/score/calibrate) collapses all of them and eliminates the SHA-hash file-modified validator. **The redesign's "remove fragile regex" goal is achievable with one well-placed change.**

### The `analysis.md` template is data-discovery shaped, not analysis-design shaped

The 8 output sections are organized around "what data exists / where the gaps are." That's right for the gap-check stage but wrong for the redesign's "essence first, then target unit, then LCOE parameters driven by 1costingfe expectations" methodology. The redesign should consider whether the analysis template's output structure should be **restructured around the workflow steps** rather than the data-availability lens — for example, sections for: (1) Identity / family delta, (2) Reference design selection, (3) Geometry/physics inputs (driven by 1costingfe schema), (4) Override candidate list with justification, (5) Open gaps.

The current template is also missing **explicit instruction to consult the ontology / 1costingfe enum mapping**. The mapping lives in `concepts.py:COSTINGFE_MAPPING` (Python dict, invisible to Claude). The redesign's "deterministic up-front ontology table + 1costingfe archetype + fit assessment" structure should make this visible to Claude *before* analysis starts.

## Feasibility Assessment

**Can the redesign be implemented?** Yes. The blast radius is large but the joints are clean:

- **`analyses/{id}/` is fully regenerable** (knowledge stays put). Safe to delete-and-rebuild per concept.
- **Extractor decoupling is mostly already there** — body is LLM-mediated. One regex (Confinement Family) needs migration to frontmatter.
- **1costingfe `forward()` interface is stable** — `result` / `result_1gw` contract continues to work.
- **Loop machinery is sound** — only the **format of feedback payload** is brittle. Restructuring `analysis.md` does not require changes to `loop.py` core.

**Risks:**

- **The new ontology + 1costingfe-fit table is upstream work** that affects every concept. If the table is built per concept, the cost is ~30 concepts × ~30 minutes of curation = 1 person-week. If built per-family, ~10 families × 1 hour = 1.5 days but loses some fidelity.
- **Override-toggle representation** (`[(category, ON/OFF)]`) requires changes to extractor compute path (`_forward_with_overrides`) and explorer UI (sliders). Not in `model_setup.py` template only — server.py + concept_page.js touch.
- **Devil's-advocate review agent** is a new review stage; it bolts onto the existing review machinery cleanly (same template/validator pattern) but adds latency and cost.
- **Cross-concept "comparables" populated up-front** instead of at runtime is a clean win, but requires the upfront table to exist before analyses can run. Sequencing matters.

## Recommendations

1. **Migrate the `**Confinement Family**: ...` regex to YAML frontmatter** before any other body restructure. This removes a single point of failure in the extractor and makes any future body redesign safe.
2. **Build the deterministic up-front tables FIRST**:
   - Ontology (confinement family, fuel, taxonomy axes).
   - 1costingfe archetype mapping + fit assessment (High/Med/Low) per concept.
   - Comparables (replaces runtime `Reuses:` discovery).
   These are small Python/YAML data structures. They become inputs to both `analysis.md` and `model_setup.py` templates.
3. **Tie the override policy to the fit assessment**:
   - High fit → zero or one override.
   - Med fit → 2-4 overrides, each in MEDIUM/LOW trust accounts only.
   - Low fit → broad override permission OR switch to freeform.
   Make this rule explicit in the model_setup template AND a validator.
4. **Replace the F-N/VERDICT/Category markdown contract with structured JSON** at the same time. This is the single highest-leverage validator simplification.
5. **Always target NOAK**:
   - Template: `noak=True` only, always.
   - When concept publishes FOAK-only data: explicit transform step in analysis.md ("FOAK→NOAK adjustment" with rationale).
   - Validator: refuse model_setup.py that sets `noak=False` in the baseline `result`.
6. **Toggleable overrides**: represent as `[("C220103", "ON", value, rationale_ref), ...]`. Build a small helper module in `costingfe_helpers/` so `model_setup.py` files share boilerplate. Extractor compute path and explorer UI plug into the toggle list.
7. **Add the devil's-advocate reviewer as a third reviewer stage** (after assess + review). Output: high-level summary, no F-N findings. Template: `devils_advocate.md`. Validator: structured JSON output (one paragraph + 3-5 concrete concerns). Human-only consumer.
8. **Sanity-check stage** (cost categories vs. comparables): can be a deterministic Python script, NOT an LLM call. Inputs: this concept's CAS breakdown + comparables' CAS breakdowns from the explorer's data. Output: flagged outliers per CAS. Pipe into review.
9. **Delete-and-regenerate workflow**: add a `regenerate-concept` subcommand that wraps the existing safe sequence (rm + gap-check + analyze + review + synthesize + score + approve), with a `--keep-gap-report` flag for the lighter form.

## Open Questions

1. **Should the deterministic ontology + 1costingfe-fit table be in `knowledge/` (alongside concept research) or in a new top-level location?** Argues for `knowledge/concept_ontology.yaml` (single canonical source).
2. **Should freeform concepts eventually get a 1costingfe archetype mapping too?** Even a "weak fit" mapping would let the redesign apply the same scaling and structure to them. Out of scope for redesign v1; worth flagging.
3. **How is the comparables list maintained as new concepts are added?** Manual update vs auto-derived from ontology (same family + fuel + a similarity score). Recommend auto-derived with human override.
4. **Override-toggle format**: tuple `(category, ON/OFF, value)` or richer `(category, ON/OFF, value, justification_ref, source_doc)`? Richer is better for auditability but more work to author.
5. **Where does the per-concept "fit assessment" come from initially**? A one-time LLM pass that reads each concept's analysis.md and YAML defaults and proposes the fit + key override candidates? Or a manual curation pass driven by the user with Claude assistance?

## Code References

### 1costingfe library
- `src/costingfe/types.py:5,10,29,53,67,84,104,134,172,178,287` — all enums + ForwardResult
- `src/costingfe/types.py:34` — `CONCEPT_TO_FAMILY`
- `src/costingfe/types.py:53` — `CONCEPT_DEFAULT_CONVERSION`
- `src/costingfe/model.py:70-89` — `CostModel.__init__`
- `src/costingfe/model.py:103-279` — `_power_balance` family dispatch
- `src/costingfe/model.py:281-392` — 0D tokamak path
- `src/costingfe/model.py:394-731` — `forward()` (full body)
- `src/costingfe/model.py:642-688` — n_mod multiplication + CAS22 override rescale
- `src/costingfe/model.py:751-752` — non-steady-state drops C220108 from replaceables
- `src/costingfe/model.py:829-836` — list of overridable accounts
- `src/costingfe/model.py:837-847` — `_OVERRIDE_TO_ATTR`
- `src/costingfe/model.py:849-896` — `_scale_overrides` (the scaling mechanism)
- `src/costingfe/model.py:901-988` — sensitivity key partitioning
- `src/costingfe/model.py:1064-1107` — `sensitivity()` + `batch_lcoe()`
- `src/costingfe/layers/geometry.py:94-161` — volume formulas (per concept)
- `src/costingfe/layers/cas22.py:36-92` — coil defaults + geometry G
- `src/costingfe/layers/cas22.py:151-475` — every CAS22 sub-account formula
- `src/costingfe/layers/costs.py:36-473` — CAS10/21/23-90 formulas
- `src/costingfe/validation.py:25,80,89,198,224,236,277,297-305` — pydantic + physics validation
- `src/costingfe/defaults.py:18-19,60-70,92,96,106,155-164,200-211,259-262,411,420` — calibration constants + per-concept loader
- `src/costingfe/adapter.py:*` — `FusionTeaInput`, `run_costing`
- `examples/scaled_overrides.py` — full `override_reference_mw` walkthrough
- `examples/multi_module.py` — n_mod usage
- `examples/foak_vs_noak.py` — FOAK/NOAK toggle
- `examples/cost_overrides.py`, `examples/dt_tokamak.py` — override patterns

### fusion-tea pipeline
- `exploration/concept_analysis/scripts/run_analysis.py:100,114,196,279,418,501,616,753,894,951,1103,1226,1264,1355,1388-1544` — CLI dispatch
- `exploration/concept_analysis/scripts/lib/loop.py:55,83,108-286,117-206,322,388,419,475-482,498,546-572,575,633-644,715,733,786,808,822,945-970` — loop body, feedback dispatch, model_setup tier
- `exploration/concept_analysis/scripts/lib/validators.py:22-38,61,125,187,208,230,283,297` — all validators
- `exploration/concept_analysis/scripts/lib/concepts.py:10-101` — `COSTINGFE_MAPPING` + routing
- `exploration/concept_analysis/scripts/lib/iteration.py:33-55` — LoopState
- `exploration/concept_analysis/scripts/lib/frontmatter.py:*` — `make_frontmatter`, `parse_frontmatter`
- `exploration/concept_analysis/scripts/lib/sources.py:*` — dossier + sources lookup
- `exploration/concept_analysis/scripts/lib/scoring.py:*` — `validate_score_output`, `validate_calibration_output`, `build_verified_scores`
- `exploration/concept_analysis/prompt_templates/analysis_v2.md:14-27,29-38,40-49,51,56-90,112-120,123,172,200-209` — template structure
- `exploration/concept_analysis/prompt_templates/output_template.md:11-50,54-163` — 8-section output
- `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md:15,47-89,91-123,102-111,112-118,120-123` — costingfe template
- `exploration/concept_analysis/prompt_templates/model_setup_freeform.md:101-146` — freeform template
- `exploration/concept_analysis/prompt_templates/assessment.md:32-79` — in-loop assessor
- `exploration/concept_analysis/prompt_templates/review.md:33-124` — standalone review
- `exploration/concept_analysis/prompt_templates/synthesis.md`, `score.md`, `calibrate.md` — late-stage templates
- `exploration/concept_analysis/prompt_templates/config/analysis_goals.md:1-25` — 5 goals
- `exploration/concept_analysis/prompt_templates/config/feedback_format.md`, `assessment_checklist.md`, `quality_standards.md`, `scoring_framework.md` — transcluded configs
- `exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_setup.py:118-124,206,285-339,343-422,428` — `_NOAK_OVERRIDES`, FOAK scenario
- `exploration/concept_explorer/extract_explorer_data.py:89-91,132-153,183-252,288,389-540,701-741,822` — frontmatter parse, narrative LLM, costingfe + freeform extraction
- `exploration/concept_explorer/models.py:~345` — `ConceptData` (target of `cost_model_1gw` field)
- `.project/research/20260419-costingfe-scaled-overrides-integration.md` — prior research on `override_reference_mw` integration (read in full for the scaling story)
- `.project/research/20260517-081444_model-setup-inconsistencies.md` — prior research on model_setup inconsistencies (read by reference)
- `.project/research/20260408-pipeline-holes-comprehensive-audit.md` — related audit
- `.project/research/20260406-concept-analysis-fragile-control-flow.md` — related fragility study
