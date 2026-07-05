# 1costingfe bug report — two defects found by WI-016 differential comparison

**Date**: 2026-07-05
**Found by**: WI-016 (H2 blind-derivation probe) — a physics/cost model derived blind from the research corpus was held against 1costingfe as the answer key; these two defects surfaced as adjudicated divergences D13 and D15 in `work/completed/20260705_WI-016_h2-blind-derivation/comparison.md`.
**Status**: Report only. No changes have been made to 1costingfe. Both bugs were re-reproduced live against the installed code (`~/1cfe/1costingfe`, editable install used by the concept analyses) on 2026-07-05 before writing this up.

---

## Bug 1: Stellarator coil cost priced at YAML `b_center=6 T`, decoupled from the concept's design field

### Summary

The stellarator branch of the coil cost (C220103) reads the field from the YAML default `b_center = 6.0 T` instead of the design point's on-axis field `B`. Only the tokamak branch derives `b_center` from `B`. Any stellarator concept whose spec field differs from 6 T gets a silently wrong coil cost — at concept 20a (B = 9 T) the served C220103 is a 33% undercount, and changing `B` in the spec does not move the coil cost at all.

### Affected code

- `src/costingfe/model.py:1271-1274` — `b_center = params["B"]` only when `self.concept == ConfinementConcept.TOKAMAK`; every other concept falls to `params.get("b_center", 0.0)`
- `src/costingfe/data/defaults/steady_state_stellarator.yaml:28` — `b_center: 6.0` (the value every stellarator run silently inherits)
- `src/costingfe/layers/cas22.py:427` — `total_kAm = G * b_center * R0 * r_coil / (_MU0 * 1000)` (the toroidal coil-cost term, linear in `b_center`)
- `src/costingfe/layers/cas22.py:441-444` — conductor cost × `coil_markup` (5.87 for stellarator, `costing_constants.yaml:73-75`)

### Impact

The fusion-tea concept explorer serves six stellarator analyses through this branch. None of them set `b_center`; all are priced at 6 T regardless of their design field. Coil cost is linear in the field, so the error factor is `6/B`:

| Concept | Spec B [T] | Coil-cost error |
|---|---|---|
| 20a type-one stellarator (Infinity Two) | 9.0 | −33.3% (served $4080M, correct $6120M) |
| 36 helical-coil stellarator | 9.0 | −33.3% |
| 20b renaissance stellarator | 10.2 | −41.2% |
| 09 QI stellarator HTS | 5.86 | +2.4% |
| 05 planar-coil stellarator | 6.0 | none (coincidence) |
| 10 large-scale stellarator | 6.0 | none (coincidence) |

Direction: high-field stellarators look systematically cheaper than the model intends. C220103 is a large CAS22 line, so this flows into total capital cost and LCOE for the affected concepts. The error is silent — the run succeeds and nothing warns that the costed field differs from the spec field.

### Minimal repro

From the 1costingfe repo root:

```python
# repro_bug1.py — concept 20a design point (R0=12.5, a=1.25, B=9 T, 350 MWe)
from costingfe import ConfinementConcept, CostModel, Fuel
from costingfe.validation import CostingInput, default_availability

SPEC = dict(R0=12.5, plasma_t=1.25, B=9.0, p_input=20.0, elon=1.0)
COMMON = dict(
    net_electric_mw=350.0,
    availability=default_availability(ConfinementConcept.STELLARATOR),
    lifetime_yr=CostingInput.model_fields["lifetime_yr"].default,
)
m = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)
c_served = m.forward(**COMMON, **SPEC).cas22_detail["C220103"]
c_b6 = m.forward(**COMMON, **{**SPEC, "B": 6.0}).cas22_detail["C220103"]
c_fixed = m.forward(**COMMON, b_center=9.0, **SPEC).cas22_detail["C220103"]

print(f"C220103, spec B=9.0 T (as served):        {c_served:8.1f} M$")
print(f"C220103, spec B=6.0 T (field changed):    {c_b6:8.1f} M$")
print(f"C220103, explicit b_center=9.0 T:         {c_fixed:8.1f} M$")
print(f"served/fixed = {c_served / c_fixed:.4f}  "
      f"(undercount {100 * (1 - c_served / c_fixed):.1f}%)")
print(f"coil cost moved when B changed 9->6 T: {abs(c_served - c_b6) > 0.05}")
```

```
uv run python repro_bug1.py
```

Observed (2026-07-05):

```
C220103, spec B=9.0 T (as served):          4080.1 M$
C220103, spec B=6.0 T (field changed):      4080.1 M$
C220103, explicit b_center=9.0 T:           6120.2 M$
served/fixed = 0.6667  (undercount 33.3%)
coil cost moved when B changed 9->6 T: False
```

Expected: the first number should equal the third ($6120M) — a toroidal device's coil-cost center field is its on-axis field. The middle line shows the decoupling directly: changing the design field by 3 T moves the coil cost by exactly nothing.

### Root cause

`model.py:1265-1270` explains the design intent for tokamaks: derive `b_center` from `B` at the point of consumption "rather than storing a second b_center: that keeps it from drifting from B." The stellarator was left out of that derivation (`model.py:1271-1274` tests `== ConfinementConcept.TOKAMAK` only), so it falls through to the loop-device path meant for mirrors, where central and plug fields genuinely differ. A stellarator is toroidal — its coil-cost field is the on-axis field, same as a tokamak — so it has exactly the drift the comment warns about, fed by the YAML calibration value 6.0.

### Suggested fix

Extend the `b_center := params["B"]` derivation at `model.py:1271-1274` to STELLARATOR (i.e., to all toroidal concepts), and drop or deprecate `b_center` from `steady_state_stellarator.yaml` so it can't silently shadow the design field. Recost the six served stellarator concepts afterward.

### How it was found

Corpus-derived magnet-cost relation (which prices at the actual axis field) held against the code at the concept 20a point — WI-016, adjudication D13.

---

## Bug 2: `compute_beta_N` returns exactly half the standard beta_N convention; Troyon and disruption gates are ~2× permissive

### Summary

`compute_beta_N` computes toroidal beta as `mu0 * p / B^2` where the standard definition is `2 * mu0 * p / B^2` (pressure over magnetic pressure `B^2/2mu0`). The returned beta_N is therefore exactly half the conventional value that the Troyon limit is defined against. The thresholds it is compared to (3.5) are standard-convention literature numbers, so the stability gates effectively sit at conventional beta_N = 7 — roughly twice as permissive as intended.

### Affected code

- `src/costingfe/layers/tokamak.py:117-126` — `compute_beta_N`: `beta_t = MU_0 * n_e * p_J / B**2` (missing the factor 2 from `B^2/(2*mu0)`)
- `src/costingfe/layers/tokamak.py:649` — `PlasmaLimits.beta_N_max = 3.5  # Troyon limit` (hard gate; `check_plasma_limits` raises `OperatingPointInfeasible` via tokamak.py:586-596)
- `src/costingfe/layers/tokamak.py:727,744` — `DisruptionModel.beta_N_max = 3.5`; `margin_beta = 1 - beta_N / beta_N_max` feeds the disruption rate, which penalizes availability and component lifetime
- `src/costingfe/layers/tokamak.py:986,992` — power-to-geometry sizing caps its temperature search at `beta_N <= beta_N_max`
- `src/costingfe/data/defaults/steady_state_tokamak.yaml:105` — `beta_N_max: 3.5  # Troyon normalized-beta limit (binding constraint)`

### Impact

Every concept run through the tokamak 0D path (`use_0d_model=True`, and the sizing mode) — the tokamak-family concepts the explorer serves. Three consequences, all in the optimistic direction:

- The infeasibility gate (beta_N ≤ 3.5) actually permits conventional beta_N up to 7 — it never fires for any realistic design point, so physically beta-limited claims are costed without complaint. The WI-016 grid sweep found low-B corners beyond the true Troyon limit that pass the gate (comparison.md §2).
- The disruption-rate margin is computed from the halved value, so disruption penalties on availability and component lifetime are understated near the real limit.
- The sizing solver can pin operating points at up to twice the conventional Troyon limit.

beta_N does not feed fusion power or any cost account directly, so point costs at gate-passing designs are unchanged; the error is in what gets gated, penalized, and sized.

### Minimal repro

From the 1costingfe repo root:

```python
# repro_bug2.py — concept 01 parameters (ARC-class, Sorbom 2015):
# n_e=1.3e20 m^-3, T_e=T_i=13.9 keV, B0=9.2 T, I_p=7.8 MA, a=1.13 m
from costingfe.layers.tokamak import MU_0, compute_beta_N

n_e, T, B, I_p, a = 1.3e20, 13.9, 9.2, 7.8, 1.13
KEV_TO_J = 1.602176634e-16

key = float(compute_beta_N(n_e, T, T, 1.0, B, I_p, a))
# Standard definition: beta_T = 2*mu0*p/B^2 with p = n_e*T_e + n_i*T_i,
# then beta_N = beta_T[%] * a * B0 / I_p  [%.m.T/MA]
p_total = n_e * (T + T) * KEV_TO_J            # n_i = n_e for DT
std = (2.0 * MU_0 * p_total / B**2) * 100.0 * a * B / I_p

print(f"compute_beta_N (answer key):   {key:.4f}")
print(f"standard convention:           {std:.4f}")
print(f"published (ARC, Sorbom 2015):  2.59 (profile-peaked)")
print(f"ratio std/key = {std / key:.4f}")
```

```
uv run python repro_bug2.py
```

Observed (2026-07-05):

```
compute_beta_N (answer key):   1.1458
standard convention:           2.2916
published (ARC, Sorbom 2015):  2.59 (profile-peaked)
ratio std/key = 2.0000
```

Expected: 2.29 at this flat-profile point (the ARC paper reports 2.59 with profile peaking). The ratio is exactly 2.0000 — a pure convention factor, not a numerical drift.

### Root cause

The standard beta is pressure over magnetic pressure: `beta = p / (B^2/2mu0) = 2*mu0*p/B^2` with total pressure `p = n_e*T_e + n_i*T_i`. The code computes `mu0*p/B^2`. The docstring (tokamak.py:118-122) says the formula "reduces to the historical 2*mu_0*n_e*T/B^2 convention exactly" — which the code does produce, but `2*mu0*n_e*T/B^2` is the beta of a single species' pressure `nT`; for the two-species total pressure `2nT` the standard value is twice that. The author conflated single-species and total pressure, losing a factor 2 while intending the standard convention.

### Nuance check: wrong number, or deliberate internal convention with matched gates?

Checked whether the gates were calibrated to the halved value (which would make this "misleading convention + consistent gates" rather than an error). They were not — this is a genuine convention error against thresholds imported from the standard-convention literature:

- All three thresholds are 3.5 and all are explicitly labeled as the Troyon limit in standard units: `PlasmaLimits.beta_N_max = 3.5  # Troyon limit [%·m·T/MA]` (tokamak.py:649), `DisruptionModel.beta_N_max = 3.5  # Troyon limit` (tokamak.py:727), and `beta_N_max: 3.5  # Troyon normalized-beta limit (binding constraint)` (steady_state_tokamak.yaml:105). 3.5 is the standard-convention no-wall value; a gate calibrated to the halved units would be ~1.75.
- The docstring itself claims equivalence to the "historical" (i.e., external, standard) convention — the intent to match the standard definition is stated in the code.
- Empirically, published machines read implausibly low in the key's units: ARC (published beta_N 2.59, an aggressive but sub-Troyon design) reports 1.15, with believed headroom to the gate of 2.35 where the real headroom is 1.21. Under a deliberately halved convention with matched gates, ARC would sit near the cap, not at a third of it.
- `validation.py` (the pydantic input-validation tier) contains no beta usage at all; every beta threshold lives in tokamak.py and the tokamak YAML, and all inherit the standard-convention number.

Verdict: the computed quantity is wrong by exactly 2 and the gates are correct standard-convention values applied to it — gates ~2× permissive, as stated.

### Suggested fix

Add the missing factor 2 in `compute_beta_N` (tokamak.py:125): `beta_t = 2.0 * MU_0 * n_e * p_J / B**2`. Leave the 3.5 thresholds alone — they are already in the right convention. Then re-run the served tokamak concepts: some design points that previously passed the gate may now correctly fail or pick up larger disruption penalties, and the sizing mode may choose different operating points.

### How it was found

Corpus-derived relation carried the standard beta definition (ARC Eq. 2); holding it against the code exposed the exact factor 2 — WI-016, adjudication D15.
