---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-09T08:20:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea PR #41 (dd59e37, 3122aed, 249cbae) — Avalanche Orbitron switched from DT to PB11"
patch_class: "fuel_correction + spec_anchor + scale_workaround"
critical: true
---

# CRITICAL Analyst Patch: Avalanche Orbitron MUST use Fuel.PB11 (not DT)

**Why this source exists.** The Avalanche Energy Orbitron is an
**aneutronic p-B11 concept**. A prior version of `model_setup.py` had
`fuel=Fuel.DT` (a regression / wrong assumption), which silently activated
D-T cost infrastructure (tritium breeding, 14.1 MeV neutron shield, T-handling
plant, T-inventory, DT licensing premium) that an actual Orbitron at any
scale doesn't need. **The DT-forced version produced LCOE ≈ $890/MWh; the
correct PB11 version produces LCOE ≈ $92/MWh** — a 10× difference driven
entirely by removing infrastructure that doesn't apply.

This is the **most consequential patch in Phase 3**. A cold-start regen that
defaults to `Fuel.DT` would silently regress LCOE by 10× and badly mis-classify
this concept's economics.

## The directive — fuel + concept class

`model_setup.py` MUST contain:

```python
from costingfe import ConfinementConcept, CostModel, Fuel
...
model = CostModel(concept=ConfinementConcept.ORBITRON, fuel=Fuel.PB11)
```

NOT `Fuel.DT`. The library's `steady_state_orbitron.yaml` is also calibrated
for PB11 (mn=1.0 no neutron multiplier, p_trit=0 no tritium plant,
f_dec=0.90 DEC default), so the concept-class default matches the fuel
choice naturally.

## Cost impact of fuel switch (for reviewer reference)

| Account | DT cost | PB11 cost | Delta |
|---------|---------|-----------|-------|
| `decom_provision` | $127M | $53M | -$74M |
| `special_materials` (T inventory) | $15M | $0M | -$15M |
| `licensing_cost` | $5M | $0.1M | -$4.9M |
| `om_cost` (annual) | $52M/yr | $24M/yr | -$28M/yr |
| `owner_cost` | $39M | $20M | -$19M |
| `p_trit` (default tritium plant power) | 10 MW | 0 MW | -10 MW (removes one source of `rec_frac > 1`) |

## Verified spec values (transcribe verbatim)

| Parameter | Value | Source |
|-----------|-------|--------|
| `plasma_t` (plasma radius) | 0.06 m | avalanche-cwfest2023-blog.md §Fusion Rate Scaling ("six centimetre radius") |
| `B` (central field) | 0.3 T | avalanche-cwfest2023-blog.md §Magnetic Field Targets (lower bound of 0.3-0.4 T range) |
| `f_dec` (direct conv. fraction) | 0.0 | OVERRIDES library default. Avalanche's product page describes a **thermal cycle** at kW commercial scale (no DEC), even though Orbitron is architecturally DEC-capable. The library ORBITRON YAML defaults f_dec=0.90; we override to 0.0 to model the analyst's "thermal cycle per product page" interpretation. |
| `blanket_form` | `"molten_salt"` | Heat-exchange medium only (no breeding) — p-B11 is aneutronic, blanket exists purely to absorb alpha and X-ray energy. |
| `blanket_fill` | `"flibe"` | Closest available library enum value |
| `p_input` (aggregate wallplug) | 0.040 MW (= 40 kW) | At Q_sci ≈ 7 (Avalanche's longer-term target), 40 kW input × Q=7 → 280 kW fusion → with thermal cycle → 80 kW net. Verifies p_input/P_native = 40/80 = 0.50 at F9 cap. |
| `P_native` | 1.0 MWe (workaround) | Library convergence floor; actual product target is 80 kWe (5 kW–100s kW range per avalanche-orbitron-page.md). See scale-workaround section below. |
| `ConfinementConcept` | `ORBITRON` | Library has dedicated class |
| `Fuel` | `PB11` | **CRITICAL — see top of file** |

## Scale workaround: P_native = 1.0 MWe (not 0.08 MWe)

The library's inverse power balance enforces a minimum-scale floor via
`pi_eff = max(p_input, p_rad - p_ash)` and coupled constraints in
`physics.py mfe_inverse_power_balance`. Any `P_native < ~1 MWe` is rejected
with `rec_frac > 1` regardless of spec values.

**Workaround:** scale to 1 MWe (the analyst's convergence floor). At 1 GWe
NOAK projection, `n_mod = 1000 modules × per-module cost`. The per-module
cost still reflects sub-MW behavior, but the 1 GWe LCOE is usable for
cross-concept comparison.

A 1costingfe library PR is required to enable computation below 1 MWe. Until
that ships, the P_native=1.0 MWe workaround is mandatory.

## Critical do-not-set parameters

- **`fuel = DT`** — see top of file. CRITICAL regression.
- **`P_native = 0.08`** (true Avalanche target) — library rejects below ~1 MWe.
  Use workaround value 1.0 MWe.
- **`p_fus`** — library back-solves via inverse power balance (Q × p_input).
- **`eta_*` overrides** — power-conversion efficiencies are ENUM-owned.

## Model directive (machine-parseable)

```yaml
model_directives:
  spec:
    plasma_t: 0.06
    B: 0.3
    f_dec: 0.0              # override of library default 0.90 (thermal cycle per product page)
    blanket_form: "molten_salt"
    blanket_fill: "flibe"
    p_input: 0.040          # 40 kW aggregate wallplug
  P_native: 1.0             # library convergence-floor workaround; actual product is 0.08 MWe
  ConfinementConcept: ORBITRON
  Fuel: PB11                # CRITICAL — see provenance, not DT
  do_not_set:
    - fuel_DT               # regression source: would silently add T-cycle infrastructure
    - p_fus                 # library back-solves
    - eta_th                # ENUM-owned
    - eta_dec               # ENUM-owned
  rationale: "Avalanche Energy Orbitron p-B11 electrostatic fusion. PR #41 corrected fuel; library convergence floor forces P_native=1 MWe workaround."
  provenance: "direct (fuel choice from Avalanche company materials)"
  upstream_blockers:
    - "1costingfe convergence floor at ~1 MWe — currently worked around via P_native=1.0"
    - "Per-module CAS30 should be per-plant — separate library issue tracked"
```

## Sources cited (already in research corpus)

- `avalanche-cwfest2023-blog.md` §Fusion Rate Scaling, §Magnetic Field Targets — geometry
- `avalanche-orbitron-page.md` — product range, thermal cycle (no DEC at kW scale)
- Avalanche Energy public technical materials confirming p-B11 fuel choice

## Maintenance — IMPORTANT

**Never change fuel to DT** without an explicit Avalanche disclosure shift.
The CWFest 2023 reference may describe D-T physics-demonstration targets at
experimental scale (proving confinement), NOT the commercial Orbitron product.
The commercial product is p-B11; the experimental demo may use D-T for
detection convenience.

If Avalanche publishes a new commercial design at higher power, supersede the
P_native value but keep `Fuel.PB11`.
