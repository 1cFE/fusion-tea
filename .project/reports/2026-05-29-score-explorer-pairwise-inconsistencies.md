# Score Explorer — Pairwise Inconsistency Audit

**Date:** 2026-05-29
**Scope:** `tools/score_explorer/data/concepts.json` (39 concepts), scored by `exploration/scoring_v2/score.py` against `exploration/scoring_v2/weights/default.yaml` and the embeddings in `exploration/scoring_v2/embeddings/rulebook.py`.
**Method:** Every finding is a *pairwise* ordering inconsistency between two named concepts on one named axis, traced to the exact lookup key / trigger / feature value that produced it, with a concrete, named-file fix and a before/after prediction for both concepts.

**Framework design accepted as given** (not critiqued): the 7-axis equal-weighted composite, the axis choices, the weight *values*, the rubric philosophy, aneutronic concepts ranking high, TF=1.0 floors, and the absence of a TRL/programmatic axis. Findings target *mechanical* inconsistencies — dead keys, key collisions, key splits, trigger gating, and feature-derivation errors — that make two concepts rank inconsistently **by the framework's own rules**.

---

## 1. Ranked findings (executive summary)

1. **D-T│TBD blanket key is dead — undeclared blankets out-score declared ones.** `33-state-backed-tokamak-best` (Neo, blanket=TBD) gets `blanket_modularity_rating=5.0` while `20a-type-one-stellarator` (declared Solid breeder) gets `4.0`, even though the lookup sets `D-T|TBD: 4` = `D-T|Solid breeder: 4`. Cause: `_blanket_modularity_rating()` rewrites `TBD → "Liquid metal"` *before* the lookup, so the `D-T|TBD: 4` entry is never hit. Fix: delete the TBD→Liquid-metal rewrite in `rulebook.py` so TBD hits its own `=4` key (drives BEST from 2.00 → 1.92, matching its v5 target of 1.91).

2. **upper_cf rewards an undeclared blanket over a declared one.** `28-hts-tokamak-full-hts` (Energy Singularity, blanket=TBD) scores `upper_cf=4.0`; the architecturally-identical `01-hts-compact-tokamak` (CFS, declared Molten salt) scores `3.5`. Cause: TBD silently defaults to Liquid metal (renewable, not in `_STATIC_BLANKET_VALUES`), so `non_renewable_blanket` never fires for ES; CFS's declared Molten salt fires it. Fix: default TBD to a non-renewable blanket (Solid breeder) inside `_compute_triggered_cf_penalties`, so disclosure is never penalized relative to non-disclosure.

3. **A levitated single-ring HTS coil scores as a mass-manufacturable wound coil.** `12-levitated-dipole` (OpenStar) gets `magnet_driver_modularity_rating=5.0` via key `MFE|HTS (wound)|*`, while `09-qi-stellarator-hts` (Proxima, 3D HTS coils) gets `3.0` via `MFE|HTS (continuous helical)|*`. A single suspended cryogenic ring is at least as bespoke as a 3D stellarator coil. Cause: magnet_type `"HTS (levitated dipole)"` has no keyword match in `_magnet_driver_key`, so it falls through to the generic `if "HTS" in mt → MFE|HTS (wound)|*` (=5.0) branch. Fix: add a `"levitated"`/`"dipole"` pattern routing to `MFE|HTS (continuous helical)|*` (=3.0).

4. **A target-factory penalty is escaped by leaving rep rate "Unknown".** `37-magnetized-target-inertial-fusion-mtif` (NearStar, rep=Unknown) fires *no* target-factory penalty; `14-magnetized-target-fusion-pneumatic-compression` (General Fusion, rep=~1 Hz) fires `target_factory_high` (2.0). Both are `mif_method=Magnetized target` (target-using). Cause: `"Unknown"` matches neither `_HIGH_REP_RATES` nor `_LOW_REP_RATES`. Fix: route Unknown rep for a confirmed target-using concept to `target_factory_low`.

5. **MagLIF's dedicated vessel key is dead; it's misrouted to the pneumatic bucket.** `07-maglif` (Pacific) gets `vessel_modularity_rating=4.0` via `MIF|Pneumatic compression|D-T`, even though the lookup has a `MIF|MagLIF|*: 5` entry written for it. Cause: `_vessel_key` matches the *taxonomy* `mif_method` substring `"MagLIF"`, but MagLIF concepts carry `mif_method="Magnetized target"` (MagLIF lives only in the derived `confinement_concept`). Fix: identify MagLIF in `_vessel_key` via `primary_heating=="Pulsed power implosion"` (the same test `_mvs_key` already uses), lifting MagLIF vessel 4.0 → 5.0.

6. **A p-B11 spherical tokamak inherits the D-T tokamak achievement record.** `39-spherical-tokamak-cs-free-p-b11` (ENN) scores `technical_feasibility=2.0`; `18-p-b11-frc` (TAE) scores `1.0`. Both are pre-demonstration p-B11 MFE devices. Cause: `achieved_triple_product` is keyed `family|concept` and is *fuel-blind* — ENN's p-B11 device collides with the D-T-projected `MFE|Spherical tokamak: 1.5e21`, while TAE's `MFE|FRC` is `1e19`. Fix: add fuel-qualified achieved keys (`MFE|Spherical tokamak (p-B11)`, no data → floor), giving ENN TF=1.0 = TAE.

7. **`pulsed_power_thermal` is gated on confinement family, not on the actual driver.** `22-projectile-icf` (First Light, electromagnetic gun → thermal steam) does *not* fire `pulsed_power_thermal`; `37-magnetized-target-inertial-fusion-mtif` (NearStar, plasma-armature railgun → thermal) *does*. Both are electromagnetic-launcher concepts with a thermal cycle. Cause: `is_pulsed_power_arch = (cfam=="MIF" or "Z-pinch" in cconcept or "Dense plasma focus" in cconcept)` — IFE is excluded by family regardless of an EM launcher. Fix: also fire when `driver_technology`/`primary_heating` contains an EM/pulsed-power marker (railgun, electromagnetic gun, pulsed power).

8. **Two FRCs get a 2-point magnet/driver split purely from MFE-vs-MIF classification.** `18-p-b11-frc` (TAE, MFE, magnet=Resistive) gets `magnet_driver=3.0` (`MFE|Resistive|*`); `08-frc-w-direct-conversion` (Helion, MIF, capacitor compression) gets `5.0` (`MIF|*|Capacitor compression`). Helion's pulsed capacitor-compression coil set is no more "modular" than TAE's DC resistive coils, yet scores higher. Cause: the MIF `magnet_driver_lookup` blanket-assigns 5.0 to *every* MIF driver (Pulsed power / Pneumatic / Capacitor / Railgun / fallback). Fix: split `MIF|*|Capacitor compression` down to 3–4, or route MFE compact-toroid resistive coils to a dedicated key, so equivalent pulsed-coil hardware scores equally across families.

9. **The TBD→Liquid-metal default also lets an undeclared blanket beat a declared one on supply chain.** Same pair as Finding 2: `28-hts-tokamak-full-hts` (TBD) `supply_chain=2.0`; `01-hts-compact-tokamak` (declared Molten salt) `1.5`. ES's TBD→Liquid-metal avoids the `beryllium`+`flibe` (1.5) that CFS's Molten salt incurs, paying only `vanadium` (1.0). Cause: same TBD rewrite in `_compute_triggered_bottlenecks`. Fix: as Finding 2 — default TBD to a conservative blanket so non-disclosure is not rewarded. (Corollary of Finding 2; same root line, different axis/triggers.)

10. **A mechanically-supported dipole inherits the free-levitation penalty.** `35-polomac-magnetic-confinement` (Deutelio, "internal dipole coil with magnetic tunnel supports") fires `levitation_stabilization`, exactly like the free-floating `12-levitated-dipole` (OpenStar). Cause: `derived.py` collapses every non-orbital `Dipole` to `confinement_concept="Levitated dipole"`, and the trigger fires on that label. Fix: add a supported-dipole branch in `_confinement_concept` (or gate the trigger on a levitation feature) so a supported coil does not pay the active-levitation-control penalty.

11. **A non-power neutron source is scored as if it had a steam cycle.** `38-particle-accelerator-driven-fusion` (SHINE, `energy_capture=N/A`, a non-power neutron source) gets `thermal_rejection_score=2`, identical to `01-hts-compact-tokamak` (real steam plant). SHINE has no thermal-rejection footprint at all. Cause: `_classify_thermal_rejection("N/A")` falls through the `else` to `"thermal"`. Fix: add an explicit `N/A`/non-power mapping in `_classify_thermal_rejection`.

---

## 2. Detailed findings

### Finding 1 — D-T│TBD blanket key is dead (modularity / blanket sub-rating)

**Step 1 — Pairwise inconsistency.** `33-state-backed-tokamak-best` scoring `blanket_modularity_rating = 5.0` is suspect given that `20a-type-one-stellarator` scores `4.0` on the same sub-rating. By the framework's own logic these should be **equal**: BEST's `blanket_config=TBD` and Type One's `blanket_config=Solid breeder` both map to `4` in `blanket_lookup` (`D-T|TBD: 4` and `D-T|Solid breeder: 4`). Instead BEST's *undeclared* blanket out-scores Type One's *declared* solid breeder.

**Step 2 — Mechanical cause.** `_blanket_modularity_rating()` (rulebook.py) short-circuits TBD before the lookup:

```python
effective_blanket = "Liquid metal" if blanket_config == "TBD" else blanket_config
key = f"{fuel}|{effective_blanket}"     # "D-T|Liquid metal" for BEST → 5.0
```

Confirmed in diagnostics: every D-T TBD concept (`07`, `13`, `16`, `28`, `29`, `33`) shows `blanket_lookup_key = "D-T|Liquid metal"` with `blanket_modularity_rating = 5.0`. The explicit `"D-T|TBD": 4` entry in `weights/default.yaml` is **never reached**. The YAML comment for that key even states the v5 BEST calibration target wins ("BEST bl=4 in v5 matrix; the calibration target wins") — the code does the opposite. Corroboration: BEST's `v5_calibration_target = 1.91`, its current `modularity = 2.00`; with blanket=4 it computes to **1.92** — a near-exact match to the calibrated target, confirming `=4` was the intent.

**Step 3 — Fix.** In `rulebook.py::_blanket_modularity_rating`, delete the TBD→"Liquid metal" rewrite and let TBD flow into the lookup key `D-T|TBD` (=4.0), which already exists. Predicted before/after:

| Concept | blanket key now → fix | brate now → fix | modularity now → fix |
|---|---|---|---|
| 33-BEST | `D-T│Liquid metal` → `D-T│TBD` | 5.0 → 4.0 | 2.000 → **1.917** (v5 tgt 1.91) |
| 20a-Type One | `D-T│Solid breeder` (unchanged) | 4.0 → 4.0 | 3.023 → 3.023 |

Result: BEST blanket 4.0 = Type One blanket 4.0 — the intended equality, and BEST's composite moves toward its calibration target. Also corrects `29-negative-triangularity-tokamak` (5.0→4.0; its v5 target 3.71 vs current mod 3.50 moves the right direction). **Foreseen side effect:** this is intentional — every D-T│TBD concept (`13`, `16`, `28`, `29`, `33`) drops its blanket sub-rating 5→4; all of those are concepts that declared no blanket, so the demotion is correct by the lookup's own design. Does not touch any concept with a declared blanket.

---

### Finding 2 — upper_cf rewards undeclared blankets (upper_cf / non_renewable_blanket)

**Step 1 — Pairwise inconsistency.** `28-hts-tokamak-full-hts` scoring `upper_cf = 4.0` is suspect given that `01-hts-compact-tokamak` scores `3.5` on the same axis. The two are the same architecture (D-T, HTS-wound REBCO compact tokamak, quasi-steady/steady). By the framework's own logic a concept that *disclosed* a static blanket should not rank **below** one that disclosed nothing.

**Step 2 — Mechanical cause.** In `_compute_triggered_cf_penalties()`:

```python
blanket = "Liquid metal" if raw_blanket == "TBD" else raw_blanket
...
if blanket in _STATIC_BLANKET_VALUES:   # {Solid breeder, Molten salt, Other/hybrid}
    triggered["non_renewable_blanket"] = weights["non_renewable_blanket"]   # 0.5
```

ES's `blanket_config=TBD` → "Liquid metal", which is **not** in `_STATIC_BLANKET_VALUES`, so `non_renewable_blanket` does not fire → penalties = `{neutronic_fuel: 1.0}` → CF = 4.0. CFS's declared `Molten salt` *is* static → penalties = `{neutronic_fuel: 1.0, non_renewable_blanket: 0.5}` → CF = 3.5.

**Step 3 — Fix.** Default TBD to a conservative *non-renewable* blanket (Solid breeder) for the penalty stacks rather than the most-favorable Liquid metal — e.g. change the rewrite in `_compute_triggered_cf_penalties` to `blanket = "Solid breeder" if raw_blanket == "TBD" else raw_blanket`. Predicted before/after:

| Concept | blanket used | non_renewable fires? | upper_cf now → fix |
|---|---|---|---|
| 28-ES | TBD → Solid breeder | no → **yes** | 4.0 → **3.5** |
| 01-CFS | Molten salt | yes | 3.5 → 3.5 |

Result: ES 3.5 = CFS 3.5 — tie restored. **Foreseen side effect:** the same change applied to `_compute_triggered_cf_penalties` also lowers other D-T TBD concepts (`13`, `16`, `29`, `33`) from CF 4.0 → 3.5; that is the intended correction (undeclared blankets should not earn the renewable-blanket benefit). Keep this change *scoped to upper_cf* unless Finding 9 is adopted jointly — see the cross-cutting note after Finding 9.

---

### Finding 3 — Levitated single-ring HTS coil scored as wound coil (modularity / magnet_driver)

**Step 1 — Pairwise inconsistency.** `12-levitated-dipole` scoring `magnet_driver_modularity_rating = 5.0` is suspect given that `09-qi-stellarator-hts` scores `3.0` on the same sub-rating. By the framework's own logic — `MFE|HTS (wound)|* = 5` ("mass-manufacturable wound REBCO pancakes") vs `MFE|HTS (continuous helical)|* = 3` ("bespoke 3D winding") — a single large cryogenic ring that must be magnetically suspended and inductively charged is *at least* as bespoke as a 3D stellarator coil, so 12 should be **lower than or equal to** 09, not two points higher.

**Step 2 — Mechanical cause.** In `_magnet_driver_key`, magnet_type strings are matched by keyword. `"HTS (3D stellarator)"` (Proxima) contains `"3d"` → `MFE|HTS (continuous helical)|*` (=3.0). `"HTS (levitated dipole)"` (OpenStar, Zephyr) contains `"HTS"` but none of `wound/integrated/planar/segment/helical/3d` → falls through to the catch-all `if "HTS" in mt: return "MFE|HTS (wound)|*"` (=5.0). Confirmed: both `12` and `19` show `magnet_driver_lookup_key = "MFE|HTS (wound)|*"`, rate 5.0.

**Step 3 — Fix.** Add a levitated-dipole branch in `_magnet_driver_key` *before* the generic HTS fallback:

```python
if "HTS" in mt and ("levitated" in mt_lower or "dipole" in mt_lower):
    return "MFE|HTS (continuous helical)|*"   # 3.0 — single bespoke ring, not modular pancakes
```

Predicted before/after (both `12` and `19` use equal-weight percent_mod, so `pmod = mean(vessel, magdrv, blanket)`):

| Concept | magdrv now → fix | percent_mod now → fix | modularity now → fix |
|---|---|---|---|
| 12-OpenStar | 5.0 → 3.0 | 4.000 → 3.333 | 2.750 → **2.583** |
| 19-Zephyr | 5.0 → 3.0 | 4.333 → 3.667 | 2.833 → **2.667** |
| 09-Proxima | 3.0 (unchanged) | 3.628 | 3.157 |

Result: OpenStar magdrv 3.0 = Proxima 3.0, and OpenStar's modularity now sits below Proxima's (2.58 < 3.16), consistent with the dipole's single-ring construction. **Foreseen side effect:** `35-polomac` is unaffected (magnet=Resistive → `MFE|Resistive|*`). No tokamak/stellarator with a `wound`/`3d` keyword is touched.

---

### Finding 4 — target-factory penalty escaped via "Unknown" rep rate (plant_complexity)

**Step 1 — Pairwise inconsistency.** `37-magnetized-target-inertial-fusion-mtif` scoring `plant_complexity = 2.5` is suspect given that `14-magnetized-target-fusion-pneumatic-compression` scores `1.0` (floored) on the same axis with `target_factory_high` (2.0) included. Both carry `mif_method=Magnetized target`, which the framework classifies as target-using (`_TARGET_USING_MIF_METHODS`). By the framework's own logic, NearStar — which genuinely railgun-launches a manufactured magnetized target every shot — should incur a target-factory penalty too.

**Step 2 — Mechanical cause.** `_compute_triggered_pc_subsystems`:

```python
if uses_targets:
    if rep_rate in _HIGH_REP_RATES:      # {~1 Hz, ~10 Hz, High (>10 Hz), kHz}
        triggered["target_factory_high"] = ...
    elif rep_rate in _LOW_REP_RATES:     # {Sub-Hz}
        triggered["target_factory_low"] = ...
```

NearStar's `repetition_rate = "Unknown"` is in neither set, so neither branch fires. Confirmed: `37` PC triggers = `{liquid_metal_handling, pulsed_power_thermal, remote_maintenance}` (no target factory); `14` triggers = `{..., target_factory_high: 2.0, ...}`. `07-maglif` (Sub-Hz) correctly fires `target_factory_low`.

**Step 3 — Fix.** In `_compute_triggered_pc_subsystems`, route an Unknown/unspecified rep rate for a confirmed target-using concept to the conservative low tier:

```python
elif rep_rate in _LOW_REP_RATES or rep_rate in ("", "Unknown", "TBD"):
    triggered["target_factory_low"] = weights["target_factory_low"]   # 0.5
```

Predicted before/after:

| Concept | rep rate | target factory now → fix | PC weight now → fix | PC now → fix |
|---|---|---|---|---|
| 37-NearStar | Unknown | none → `target_factory_low` (0.5) | 2.5 → 3.0 | 2.5 → **2.0** |
| 14-GF | ~1 Hz | `target_factory_high` (2.0) | 5.5 | 1.0 (floored, unchanged) |

Result: NearStar now carries a target-factory cost like every other manufactured-target MIF concept. It does not reach parity with GF (GF's ~1 Hz high-rep factory is genuinely costlier), but the *direction* is corrected — NearStar no longer scores better than GF by virtue of a missing data field. **Foreseen side effect:** only affects target-using concepts with Unknown rep; in the current corpus that is uniquely NearStar.

---

### Finding 5 — MagLIF's dedicated vessel key is dead (modularity / vessel)

**Step 1 — Pairwise inconsistency.** `07-maglif` scoring `vessel_modularity_rating = 4.0` is suspect given that `37-magnetized-target-inertial-fusion-mtif` scores `5.0` on the same sub-rating, and given that the lookup contains a `MIF|MagLIF|*: 5` entry written specifically for MagLIF. By the framework's own table, MagLIF's vessel should be 5.0 (a simple replaceable liner cylinder), equal to the other compression-MIF vessels — instead it is the one concept that never reaches its own key.

**Step 2 — Mechanical cause.** `_vessel_key` (MIF branch) identifies MagLIF by the *taxonomy* `mif_method` string:

```python
if "MagLIF" in (mif_method or ""):
    return "MIF|MagLIF|*"          # never matches — see below
...
return f"MIF|Pneumatic compression|{fuel}"
```

But MagLIF concepts carry `mif_method = "Magnetized target"` (MagLIF appears only in the *derived* `confinement_concept`, via `concept_id`). So `"MagLIF" in mif_method` is always False, and `07` falls to `MIF|Pneumatic compression|D-T` (=4.0). The `MIF|MagLIF|*: 5` vessel entry is dead. Note the framework already identifies MagLIF correctly elsewhere — `_mvs_key` uses `primary_heating=="Pulsed power implosion"` → `mvs=5.0` (`MIF|MagLIF`). The two sub-lookups disagree on how MagLIF is recognized.

**Step 3 — Fix.** In `_vessel_key`, identify MagLIF by the same test `_mvs_key` uses, before the pneumatic fallback:

```python
if primary_heating == "Pulsed power implosion" or "MagLIF" in (mif_method or ""):
    return "MIF|MagLIF|*"
```

(requires passing `primary_heating` into `_vessel_key`/`_vessel_modularity_rating`, as `_mvs_key` already receives it). Predicted before/after:

| Concept | vessel key now → fix | vessel rate now → fix | percent_mod now → fix | modularity now → fix |
|---|---|---|---|---|
| 07-MagLIF | `MIF│Pneumatic…│D-T` → `MIF│MagLIF│*` | 4.0 → 5.0 | 4.667 → 5.000 | 4.917 → **5.000** |
| 37-NearStar | `MIF│Pneumatic…│D-D` (unchanged) | 5.0 | 5.000 | 5.000 |

Result: MagLIF vessel 5.0 reaches parity with the other compression-MIF vessels, as the lookup intends. **Foreseen side effect:** General Fusion (`14`, true pneumatic, `primary_heating="Mechanical compression"`) is unaffected and remains on the pneumatic-D-T key (4.0) — exactly the distinction the dead key was meant to draw between a Z-machine liner and a pneumatic liquid-metal liner.

---

### Finding 6 — TF achieved-product key is fuel-blind (technical_feasibility)

**Step 1 — Pairwise inconsistency.** `39-spherical-tokamak-cs-free-p-b11` scoring `technical_feasibility = 2.0` is suspect given that `18-p-b11-frc` scores `1.0` on the same axis. Both are pre-demonstration p-B11 MFE devices that have never produced a p-B11 triple product. By the framework's own logic (gap = required/achieved, log-bucketed), ENN's advantage comes entirely from being credited with a **D-T** tokamak achievement.

**Step 2 — Mechanical cause.** `_triple_product_gap` builds the achieved key as `f"{confinement_family}|{confinement_concept}"` with **no fuel term**:

- `39-ENN`: key `MFE|Spherical tokamak` → `achieved = 1.5e21` (the table comments this as the "JT-60U/JET D-T projected equivalent"); `required` (p-B11, MFE) = `5e24`; gap = 3333 → log 3.52 → bucket 2.0.
- `18-TAE`: key `MFE|FRC` → `achieved = 1e19`; required 5e24; gap = 5e5 → log 5.7 → floor 1.0.

So ENN's p-B11 spherical tokamak collides on the achieved side with the D-T spherical tokamak `21-spherical-tokamak-hts` (both key `MFE|Spherical tokamak`, both `achieved=1.5e21`), even though p-B11 burn has never been demonstrated in that device and is ~10³× harder.

**Step 3 — Fix.** Add fuel-qualified achieved keys for advanced-fuel devices in `weights/default.yaml::technical_feasibility.achieved_triple_product`, and have `_triple_product_gap` try the fuel-qualified key first:

```yaml
# no measured p-B11 burn in a tokamak/FRC → omit (no-data floor)
# "MFE|Spherical tokamak (p-B11)": <omitted>
```
```python
key = f"{cf}|{cconcept} ({fuel})"
a = achieved.get(key, achieved.get(f"{cf}|{cconcept}")) if fuel in ("p-B11","D-He3") else achieved.get(f"{cf}|{cconcept}")
```

With the p-B11 spherical-tokamak key omitted, ENN takes the no-data floor. Predicted before/after:

| Concept | fuel | achieved now → fix | gap | TF now → fix |
|---|---|---|---|---|
| 39-ENN | p-B11 | 1.5e21 → no data | — → ∞ | 2.0 → **1.0** |
| 18-TAE | p-B11 | 1e19 (unchanged) | 5e5 | 1.0 → 1.0 |
| 21-Tokamak Energy | D-T | 1.5e21 (unchanged) | 2.0 | 4.0 → 4.0 |

Result: ENN 1.0 = TAE 1.0, both reflecting "no demonstrated p-B11 burn," while the D-T spherical tokamak keeps its legitimate 1.5e21. **Foreseen side effect:** this is purely additive (new keys + a guarded lookup); it touches only advanced-fuel concepts whose achieved value was an inherited D-T number. It does **not** alter the design intent that aneutronic concepts rank high overall — that ranking is carried by customization/supply-chain/upper-cf, not by a borrowed D-T physics record.

---

### Finding 7 — `pulsed_power_thermal` gated on family, not on the driver (plant_complexity)

**Step 1 — Pairwise inconsistency.** `22-projectile-icf` scoring `plant_complexity = 2.0` (no `pulsed_power_thermal`) is suspect given that `37-magnetized-target-inertial-fusion-mtif` scores `2.5` *with* `pulsed_power_thermal` (1.0) included. First Light drives a target with an **electromagnetic gun** into a thermal steam cycle; NearStar drives one with a **plasma-armature railgun** into a thermal cycle. By the trigger's own rationale (a pulsed/electromagnetic energy source coupled to a thermal cycle), First Light should fire it too.

**Step 2 — Mechanical cause.** `_compute_triggered_pc_subsystems`:

```python
is_pulsed_power_arch = (cfam == "MIF" or "Z-pinch" in cconcept or "Dense plasma focus" in cconcept)
has_thermal = energy.startswith("Thermal") or energy == "Hybrid (thermal + direct)"
if is_pulsed_power_arch and has_thermal:
    triggered["pulsed_power_thermal"] = ...
```

The gate is `confinement_family`/concept, not the driver. NearStar (`cfam=MIF`) qualifies; First Light (`cfam=IFE`, `confinement_concept=Projectile ICF`) is excluded — even though its `driver_technology="Electromagnetic gun"` is the more literally "pulsed-power/EM" of the two. Confirmed: `37` fires `pulsed_power_thermal`; `22` does not.

**Step 3 — Fix.** Add a driver-based OR-clause so the trigger keys on the actual hardware:

```python
drv = (driver_technology or "").lower()
is_pulsed_power_arch = (
    cfam == "MIF" or "Z-pinch" in cconcept or "Dense plasma focus" in cconcept
    or any(k in drv for k in ("railgun", "electromagnetic gun", "pulsed power", "coaxial electrode"))
)
```
(requires threading `driver_technology` into the function — it is already available on the feature doc). Predicted before/after:

| Concept | driver | pulsed_power_thermal now → fix | PC weight now → fix | PC now → fix |
|---|---|---|---|---|
| 22-First Light | Electromagnetic gun | no → **yes** (1.0) | 3.0 → 4.0 | 2.0 → **1.0** |
| 37-NearStar | Plasma-armature railgun | yes (1.0) | 2.5 → 2.5 (+0.5 from F4 → 3.0) | 2.5 → 2.5/2.0 |

Result: First Light now pays the same pulsed-EM-to-thermal coupling cost as NearStar, removing the IFE-family escape. **Foreseen side effect:** General Fusion (`14`, pneumatic pistons — *mechanical*, not electrical) keeps `pulsed_power_thermal` only via the `cfam==MIF` clause; if the analyst intends the penalty to be strictly *electrical* pulsed power, the MIF clause should additionally require a non-pneumatic driver — flagged for analyst decision, since it would *remove* the penalty from GF (currently floored, so no score change either way).

---

### Finding 8 — FRC magnet/driver split from MFE-vs-MIF classification (modularity / magnet_driver)

**Step 1 — Pairwise inconsistency.** `08-frc-w-direct-conversion` scoring `magnet_driver_modularity_rating = 5.0` is suspect given that `18-p-b11-frc` scores `3.0` on the same sub-rating. Both are field-reversed-configuration devices. Helion's pulsed capacitor-driven *compression* coil set is, if anything, higher-energy and more bespoke than TAE's DC resistive equilibrium coils, yet it scores two points higher.

**Step 2 — Mechanical cause.** The two FRCs route through different family branches of `magnet_driver_lookup`:

- `18-TAE`: `confinement_family=MFE`, `mfe_topology=Compact Toroid`, `magnet_type=Resistive` → `MFE|Resistive|*` = **3.0**.
- `08-Helion`: `confinement_family=MIF`, `mif_method=FRC compression` → `MIF|*|Capacitor compression` = **5.0**.

Every MIF driver key in the lookup is 5.0 (`Pulsed power`, `Pneumatic`, `Capacitor compression`, `Railgun`, and the `MIF|*|*` fallback), so any FRC classified as MIF inherits 5.0, while a structurally similar copper-coil FRC classified as MFE gets 3.0.

**Step 3 — Fix.** Differentiate the MIF compression drivers in `weights/default.yaml::modularity.magnet_driver_lookup` so high-energy pulsed compression is not auto-5.0:

```yaml
"MIF|*|Capacitor compression":   3      # high-energy pulsed compression coils, not modular
"MIF|*|Pulsed power":            4
```

Predicted before/after (Helion uses equal-weight percent_mod: `mean(vessel 5, magdrv, blanket 5)`):

| Concept | magdrv key | magdrv now → fix | percent_mod now → fix | modularity now → fix |
|---|---|---|---|---|
| 08-Helion | `MIF│*│Capacitor compression` | 5.0 → 3.0 | 5.000 → 4.333 | 5.000 → **4.667** |
| 18-TAE | `MFE│Resistive│*` | 3.0 (unchanged) | 3.667 | 3.667 |

Result: the two FRC coil sets are scored within one point instead of two, and the higher score still belongs to Helion's compression FRC only to the extent its vessel/mvs justify it. **Caveat / foreseen side effect:** this is the weakest of the structural findings because the MIF=5.0 assignment may be a deliberate "pneumatic-class modular by default" design choice; lowering `Capacitor compression` to 3.0 also lowers it for any future capacitor-compression MIF concept. If the analyst wants to preserve the pneumatic-class default, an alternative is to *raise* the MFE compact-toroid resistive case (add `MFE|Compact Toroid resistive` → 4) rather than lower the MIF case. Either resolves the pairwise; the choice is a calibration call.

---

### Finding 9 — TBD→Liquid-metal default also rewards non-disclosure on supply chain (supply_chain)

**Step 1 — Pairwise inconsistency.** `28-hts-tokamak-full-hts` scoring `supply_chain = 2.0` is suspect given that `01-hts-compact-tokamak` scores `1.5` on the same axis. Same architecture; the only difference is that ES left `blanket_config=TBD` while CFS declared `Molten salt`. By the framework's own logic a concept disclosing a (bottleneck-heavy) blanket should not rank below one disclosing nothing.

**Step 2 — Mechanical cause.** `_compute_triggered_bottlenecks`:

```python
blanket = "Liquid metal" if raw_blanket == "TBD" else raw_blanket
```

ES → Liquid metal → `{tritium, lithium6, vanadium}` = 3.0 → SC = 2.0. CFS → Molten salt → `{tritium, lithium6, beryllium, flibe}` = 3.5 → SC = 1.5. The TBD default lands on the *single lowest-bottleneck* D-T blanket; declaring Molten salt instead adds `beryllium` (1.0) + `flibe` (0.5) and replaces `vanadium`.

**Step 3 — Fix.** Same one-line change as Finding 2, applied here: default TBD to `Solid breeder` in `_compute_triggered_bottlenecks` (Solid breeder → `{tritium, lithium6, beryllium}` = 3.0, SC = 2.0). Predicted before/after:

| Concept | blanket used | bottlenecks | SC now → fix |
|---|---|---|---|
| 28-ES | TBD → Solid breeder | `{t, li6, be}` = 3.0 | 2.0 → 2.0 |
| 01-CFS | Molten salt | `{t, li6, be, flibe}` = 3.5 | 1.5 → 1.5 |

**Honest assessment of resolution:** on *this* axis the fix does **not** fully close the ES↔CFS gap (ES stays 2.0, CFS stays 1.5) — because Molten salt genuinely carries the extra `flibe` (0.5) that Solid breeder does not. So the residual 0.5 gap is a *real* material-bottleneck difference, not a TBD artifact, and is correct to leave in place. What the fix *does* remove is the TBD-vs-declared reward relative to **solid-breeder** declarers: today `12-OpenStar` (Solid breeder, SC 2.0) and `28-ES` (TBD, SC 2.0) tie only by coincidence (LM vanadium 1.0 == solid-breeder beryllium 1.0); under the fix ES is explicitly placed on the same conservative blanket it failed to disclose. **Cross-cutting note (Findings 2 + 9):** both trace to the identical `TBD → "Liquid metal"` rewrite, which appears separately in `_compute_triggered_cf_penalties` and `_compute_triggered_bottlenecks` (and `_compute_triggered_pc_subsystems`). Changing all three together is consistent; changing only one creates a blanket-assumption that differs across axes for the same concept. Recommend a single shared helper `_effective_blanket(raw)` so the TBD policy is defined once.

---

### Finding 10 — Supported dipole inherits the levitation penalty (plant_complexity)

**Step 1 — Pairwise inconsistency.** `35-polomac-magnetic-confinement` firing `levitation_stabilization` (and thus carrying that 0.5 cost in its PC stack) is suspect given that `12-levitated-dipole` fires the identical trigger — the two are treated as the same architecture for this penalty, but Polomac's coil is described as held by "magnetic tunnel supports" (a supported/constrained internal ring), whereas OpenStar's is a free-floating levitated coil. By the trigger's own rationale (active feedback control of a *freely levitated* magnet), a supported coil should not pay it.

**Step 2 — Mechanical cause.** `levitation_stabilization` fires when `confinement_concept in LEVITATED_DIPOLE_CONCEPTS = {"Levitated dipole", "Levitated dipole (orbital)"}`. `derived.py::_confinement_concept` maps **every** non-orbital `mfe_topology=Dipole` concept to `"Levitated dipole"`:

```python
if mfe_top == "Dipole":
    if "orbital" in concept_id.lower():
        return "Levitated dipole (orbital)"
    return "Levitated dipole"
```

There is no "supported dipole" category, so Polomac (`35`) and OpenStar (`12`) collide on `confinement_concept`, and the trigger cannot tell them apart.

**Step 3 — Fix.** Add a supported-dipole branch in `_confinement_concept` keyed on a marker in the driver/structure description (e.g. `"support" in driver_technology.lower()`), returning a distinct label (`"Supported dipole"`) that is **not** in `LEVITATED_DIPOLE_CONCEPTS`. Predicted before/after:

| Concept | confinement_concept | levitation fires? | PC weight now → fix | PC now → fix |
|---|---|---|---|---|
| 35-Polomac | `Levitated dipole` → `Supported dipole` | yes → **no** | 1.5 → 1.0 | 3.5 → **4.0** |
| 12-OpenStar | `Levitated dipole` | yes | 3.5 (floored) | 1.5 |

Result: Polomac no longer pays an active-levitation-control cost it does not incur. **Caveat:** the engineering reading of "magnetic tunnel supports" is uncertain — it may denote a magnetically-supported (still actively-controlled) coil rather than a mechanically-fixed one, in which case the current behavior is defensible. The *mechanical* cause (the deriver collapse erasing the supported/levitated distinction) is certain; the fix should be gated on confirming Polomac's support scheme with the source dossier before implementation. Ranked low for that reason. **Foreseen side effect:** none for `12`/`19` (genuinely levitated) as long as the marker is specific to supported designs.

---

### Finding 11 — Non-power neutron source scored as a steam plant (customization)

**Step 1 — Pairwise inconsistency.** `38-particle-accelerator-driven-fusion` scoring `thermal_rejection_score = 2` (the "thermal/steam" tier) is suspect given that `01-hts-compact-tokamak` scores the same `2` — they are scored *identically* on thermal-rejection footprint, yet SHINE is a non-power neutron source (`energy_capture=N/A`, `blanket=N/A (non-power)`) with no steam cycle and no waste-heat rejection at all, while CFS is a full thermal plant. By the axis's own logic (lower thermal-rejection footprint → higher score; direct conversion = 4), a plant with *no* thermal cycle should not be lumped with steam plants — they should differ, and they do not.

**Step 2 — Mechanical cause.** `_classify_thermal_rejection`:

```python
energy = energy_capture or ""
if energy.startswith("Direct"): return "direct_conversion"
if energy == "Hybrid (thermal + direct)": return "hybrid"
return "thermal"          # everything else, incl. "N/A", falls here → score 2
```

SHINE's `energy_capture="N/A"` hits the final `return "thermal"`, scoring 2 — identical to any steam concept. Confirmed in diagnostics: `sub_factor_a = {classification: thermal, value: ... , score: 2}` is what produces CUST 1.67 for SHINE.

**Step 3 — Fix.** Add an explicit non-power mapping in `_classify_thermal_rejection` and a corresponding entry in `weights/default.yaml::customization.thermal_rejection_scores`:

```python
if energy in ("N/A", "N/A (non-power)") or not energy:
    return "non_power"     # no thermal rejection footprint
```
```yaml
thermal_rejection_scores:
  direct_conversion: 4
  non_power:         4     # no power cycle → no thermal-rejection burden
  hybrid:            3
  thermal:           2
```

Predicted before/after:

| Concept | energy_capture | thermal class now → fix | sub_factor_a now → fix | customization now → fix |
|---|---|---|---|---|
| 38-SHINE | N/A | thermal → non_power | 2 → 4 | 1.67 → **3.00** |
| 01-CFS | Thermal (steam) | thermal | 2 | 1.67 |

Result: SHINE (no thermal cycle) now differs from a steam plant on the thermal-rejection sub-factor, as the axis logic requires. **Caveat / foreseen side effect:** SHINE is a non-power isotope/neutron source whose presence in an *electricity*-cost framework is itself debatable; if the analyst prefers to keep non-power sources comparable to thermal plants (conservative), leave as-is. The only concept with `energy_capture=N/A` is SHINE, so the change is isolated. This is an "equal where it should differ" finding (the weakest pairwise form) and is ranked last for that reason.

---

## 3. Per-concept walk-through (39 concepts)

- **01-hts-compact-tokamak (CFS, D-T compact tokamak).** Findings 2 & 9 (the *declarer* side): its disclosed Molten salt blanket makes it score upper_cf 3.5 and supply_chain 1.5, below the architecturally-identical Energy Singularity (`28`) which left blanket TBD. No inconsistency *internal* to CFS; it is the reference victim of the TBD-default asymmetry.
- **02-acoustic-icf-sonofusion (D-D acoustic).** No ranked finding. Minor: at kHz pulsed operation it carries no target-factory cost (acoustic cavitation is in-bulk, correctly excluded from `_TARGET_USING_IFE_DRIVERS`), so PC=4.0 vs `03`'s 2.0; this is by design. Composite evidence is `low` (no capex, no triple product) — interpret its 4.67 modularity cautiously.
- **03-laser-icf-liquid-jet-target (Cortex, D-D laser).** No inconsistency found; serves as the PC peer that *does* fire `target_factory_high` (contrast with `02`). Its mvs uses the `IFE|Laser (liquid jet)`=4 key correctly via `laser_approach=Liquid jet`.
- **04-laser-icf (hb11, p-B11 laser fast ignition).** Clean. TF floors at 1.0 (p-B11 IFE gap ~1.4e5) by design; customization 3.67 from p-B11 fuel safety. No pairwise issue.
- **05-planar-coil-stellarator (Thea, D-T).** No ranked finding. Its magnet_driver=5.0 (`MFE|HTS (planar)|*`) vs other stellarators' 3.0 (`continuous helical`) is a *defensible* split — Thea's flat planar coil array is the genuine modularity claim. Noted, not flagged.
- **06-magnetic-mirror (Pale Blue, p-B11).** Clean. Top customization (5.0) and supply chain (5.0) from aneutronic direct-conversion, by design; TF floors at 1.0.
- **07-maglif (Pacific, D-T MIF).** **Finding 5** (dead `MIF|MagLIF|*` vessel key → vessel 4.0 instead of 5.0). Also illustrates the MagLIF recognition mismatch: `mvs` recognizes it (5.0) but `vessel` does not.
- **08-frc-w-direct-conversion (Helion, D-He3 MIF).** **Finding 8** (MIF capacitor-compression magnet_driver auto-5.0 vs TAE's 3.0). Otherwise consistent; helium3 bottleneck (3.0) correctly drives SC to 2.0.
- **09-qi-stellarator-hts (Proxima, D-T).** **Finding 3** peer (3D HTS coil → continuous helical 3.0, the correct comparison against OpenStar's wrongly-5.0 dipole coil).
- **10-large-scale-stellarator (Gauss, D-T).** No score-affecting inconsistency. Minor: `confinement_concept` derives to "QI stellarator" (from `stellarator_type=QI`) though Gauss builds HELIAS-class classical stellarators; harmless because all stellarator achieved values are 1e20. LTS+HTS magnet → cryoplant_lts (1.0) and magnet_driver 2.0, correctly.
- **11-magnetic-mirror (Realta, D-T).** Clean. HTS wound mirror magnet → magnet_driver 5.0 (legitimate wound coil). Hybrid energy capture fires `hybrid_energy` (0.5) correctly.
- **12-levitated-dipole (OpenStar, D-T).** **Finding 3** (HTS levitated-ring coil mis-scored as wound 5.0). Also Finding 1 peer on the declared/undeclared blanket axis (its Solid breeder = 4.0 is the correct comparator to BEST's TBD=5.0).
- **13-electrostatic-hybrid (Avalanche, D-T Non-Standard).** Findings 1/2/9 family member (blanket=TBD → Liquid-metal default on modularity, upper_cf, supply_chain). mvs `Non-Standard|Electrostatic`=5.0 is correct.
- **14-magnetized-target-fusion-pneumatic-compression (General Fusion, D-T MIF).** **Finding 4** (fires `target_factory_high` at ~1 Hz, the contrast against NearStar's Unknown-rep escape). Floored at PC=1.0. Pneumatic (mechanical) driver also raises the Finding 7 question (does `pulsed_power_thermal` belong on a non-electrical driver?).
- **15-sheared-flow-stabilized-z-pinch (Zap, D-T).** No ranked finding. Minor dead key: the `MFE|Z-pinch|*: 3` vessel entry is never used — `_vessel_key` returns `MFE|Mirror|*` for all Open/Linear (both score 3, so no divergence). `disruption_mitigation` fires (Z-pinch ∈ DISRUPTION_PRONE), by design.
- **16-muon-catalyzed-fusion (Acceleron, D-T Non-Standard).** Findings 1/2/9 family (blanket TBD). Minor: mvs routes to `Non-Standard|Particle accelerator`=3.0 (driver_tech contains "accelerator") rather than the `Non-Standard|Muon-catalyzed`=3.0 key — both 3.0, no divergence.
- **17a-laser-icf-hybrid-drive (Xcimer, D-T KrF).** No ranked finding. Worst supply chain in the corpus (SC=1.0) from Molten salt + laser KdP (be+flibe+kdp+li6+t = 4.0); all triggers legitimate. Xcimer-class mvs key (3.0) correctly applied via `excimer` in driver_tech.
- **17b-laser-icf-fast-ignition (Focused, D-T DPSSL).** No ranked finding. Observation (not flagged, see §4): equal-weight percent_mod (4.33) vs the capex-weighted laser peers (`26`=4.76) despite identical 3/5/5 sub-ratings — an artifact of cost-model availability.
- **18-p-b11-frc (TAE, p-B11 MFE).** **Findings 6 & 8** (p-B11 FRC floored at TF 1.0 while the p-B11 spherical tokamak ENN gets 2.0; resistive magnet_driver 3.0 while Helion's MIF FRC gets 5.0).
- **19-orbital-levitated-dipole (Zephyr, D-He3).** **Finding 3** (HTS levitated coil → wound 5.0). D-He3 → helium3 SC bottleneck (3.0). Collides with `12` and `35` on mvs (`MFE|Levitated dipole`=3.0) by design.
- **20a-type-one-stellarator (Type One, D-T).** **Finding 1** peer (declared Solid breeder → blanket 4.0, the correct comparator to BEST's TBD-inflated 5.0). v5 target 3.03 vs score 3.02 — well-calibrated.
- **20b-renaissance-stellarator (Renaissance, D-T).** Clean. Other/hybrid blanket → blanket 4.0 (correct). NBI → high_power_aux (1.0) vs `20a`'s RF → rf_aux (0.5); the 0.5 PC difference between the two modular-stellarator twins is the legitimate NBI-vs-RF distinction.
- **21-spherical-tokamak-hts (Tokamak Energy, D-T).** Finding 6 context: legitimately holds `MFE|Spherical tokamak`=1.5e21 (D-T) → TF 4.0; the fix preserves this and only removes ENN's p-B11 inheritance of the same number.
- **22-projectile-icf (First Light, D-T).** **Finding 7** (EM-gun driver escapes `pulsed_power_thermal` because IFE is family-excluded). Otherwise consistent.
- **23-laser-icf-nanostructured-target (Marvel, p-B11).** Clean. Hybrid energy + p-B11 → customization 4.33; TF floors 1.0 (ultrashort-pulse p-B11). No pairwise issue.
- **24-dense-plasma-focus (LPPFusion, p-B11).** Clean. Top customization (5.0, direct + p-B11) and supply chain (5.0); TF floors 1.0. `energy_capture=Direct (charged particle)` → no `pulsed_power_thermal` despite DPF arch (no thermal cycle), correctly.
- **25-heavy-ion-beam-icf (Intensity, D-T).** No ranked finding. Observation (§4): `unit_count_estimate=1` → unit_multiplicity 1.0, vs the other large-driver IFE laser plants at 200–1000 (umult 5.0); a manual feature with no architectural basis stated for the 1-vs-1000 spread. TF floors at 1.0 (achieved 1e15, a weight). Fires `target_factory_high` (heavy-ion beam ∈ target-using).
- **26-laser-icf-indirect-drive (Inertia, D-T).** No ranked finding. Highest IFE TF (5.0, indirect-drive achieved 5e21, gap 0.6); the +0.0 indirect modifier vs −0.25 direct (`31`/`32`) is a documented design weight, not flagged. Observation (§4): capex-weighted percent_mod 4.76 vs equal-weight laser peers.
- **27-polywell (EMC2, D-T Non-Standard).** Findings 1/2/9 family (blanket TBD). mvs `Non-Standard|Electrostatic`=5.0; resistive magnet → no cryoplant, correctly.
- **28-hts-tokamak-full-hts (Energy Singularity, D-T compact tokamak).** **Findings 1/2/9** (the *non-discloser* side): blanket=TBD inflates its blanket sub-rating to 5.0 and lets it beat CFS on upper_cf (4.0 vs 3.5) and supply_chain (2.0 vs 1.5). v5 target 3.50 vs modularity 3.72 — over by 0.22, consistent with the TBD blanket inflation.
- **29-negative-triangularity-tokamak (Firefly, D-T).** **Finding 1** (blanket=TBD → 5.0; v5 target 3.71 vs score 3.50). Correctly routed to `MFE|Tokamak (negative-T)` mvs (3.0) and `MFE|Tokamak|non-compact` vessel (2.0).
- **31-laser-icf-oec-architecture (Blue Laser, D-T).** No ranked finding. TF 4.75 (direct drive 5e21, −0.25 modifier). The direct-vs-indirect −0.25 modifier (vs `26`) is a design weight, not flagged.
- **32-laser-icf-french-national (GenF, D-T).** No ranked finding. Same direct-drive profile as `31` (TF 4.75); capex-weighted percent_mod 4.58. Clean.
- **33-state-backed-tokamak-best (Neo, D-T standard tokamak).** **Finding 1** (headline): blanket=TBD → 5.0 instead of the v5-intended 4.0; with the fix modularity moves 2.00 → 1.92, matching its v5 target 1.91. LTS-override correctly routes it to non-compact mvs/vessel (2.0).
- **35-polomac-magnetic-confinement (Deutelio, D-D dipole).** **Finding 10** (supported dipole inherits `levitation_stabilization` via the Dipole→"Levitated dipole" deriver collapse). D-D → SC 5.0 (no bottlenecks), correctly.
- **36-helical-coil-stellarator (Helical Fusion, D-T).** No ranked finding. Observation (§4): `unit_count_estimate=1` → unit_multiplicity 1.0 drives modularity to 2.02, vs Proxima (`09`, units=50, umult 5.0) at 3.16 — the two QI/helical HTS stellarators (magnet_driver both 3.0) diverge almost entirely on a manual unit-count estimate. Continuous-helical magnet_driver (3.0) correctly applied via `stellarator_type=Helical coil`.
- **37-magnetized-target-inertial-fusion-mtif (NearStar, D-D MIF).** **Findings 4 & 7** (escapes `target_factory` via rep=Unknown; fires `pulsed_power_thermal` as the railgun comparator to First Light). Finding 5 peer (D-D pneumatic vessel 5.0, the value MagLIF should also reach).
- **38-particle-accelerator-driven-fusion (SHINE, D-T Non-Standard).** **Finding 11** (N/A energy → thermal misclassification). Minor: `_vessel_key` routes it to `Non-Standard|Electrostatic|*` (nsm=Electrostatic) while mvs/magnet_driver route it to `Particle accelerator` — all 3.0, no divergence. Tritium fires but no breeding bottlenecks (blanket non-power), giving SC 4.0.
- **39-spherical-tokamak-cs-free-p-b11 (ENN, p-B11 spherical tokamak).** **Finding 6** (headline): inherits the D-T `MFE|Spherical tokamak`=1.5e21 achieved record → TF 2.0, above the p-B11 FRC (TAE, 1.0), purely from a fuel-blind achieved key. Top customization/upper_cf (5.0) and SC (5.0) from aneutronic fuel are by design.

---

## 4. Methodology observations (not ranked findings — no clean pairwise fix)

These are real mechanical effects but either lack a clean pairwise ordering violation, or the natural "fix" conflicts with an accepted design choice (e.g. the project's no-fallbacks stance). Recorded for completeness:

- **percent_mod equal-weight fallback vs capex-weighting.** Concepts with a `model_output.txt` (capex shares ≥ 0.30 of plant cost) get a *cost-weighted* percent_mod that pulls toward their dominant subsystem (usually the high-rated coil set); concepts without one fall back to equal 1/3 weighting. Identical sub-ratings therefore yield different percent_mod (e.g. `26`-Inertia 4.76 capex-weighted vs `17b`-Focused 4.33 equal-weight, both 3/5/5). This is the designed sparse-capex backstop; the honest "fix" (a family-default capex profile) is a fabricated fallback the project explicitly avoids, so it is left as-is. Mitigation already present: such concepts carry `low`/`medium` modularity evidence.
- **Manual `unit_count_estimate` spread.** unit_multiplicity (0.25 of modularity) swings on an analyst-entered integer with no architectural derivation. Single-unit estimates (`25`-heavy-ion, `36`-helical, `33`-BEST, `12`/`19` dipoles = umult 1.0) sit beside 200–1000-unit estimates (`26`-indirect = umult 5.0) for comparably-sized single-driver/single-device plants. Not a lookup/trigger inconsistency — the cause is a feature *value* — so the fix is data re-estimation per concept, outside the scoring mechanism. Flagged for a feature-file review pass rather than a code change.
- **Dead lookup keys with no score impact (traceability hygiene).** Several keys can never be reached and should be removed or rewired to avoid implying coverage that does not exist: `MFE|Z-pinch|*` (vessel; `_vessel_key` returns `MFE|Mirror|*` for all Open/Linear), `MFE|Other` (mvs; no concept derives to it), and the `Non-Standard|Muon-catalyzed`/`Particle accelerator` mvs keys that are shadowed by the `driver_technology`-contains-"accelerator" override. All happen to share the score of the key that wins, so no current ranking is affected — but they are latent collision risks if any value is recalibrated.
