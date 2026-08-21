"""Probe: does _scale_overrides preserve the design's per-module-at-native semantic?

The rework design specifies: override `value` is per-module M$ at design-point
single-module reference. When the two-knob call applies the override at
(net=1000, n_mod=1000/P_native), each module is held at native operating point
and should cost exactly `value` per module — i.e. the override should pass
through unscaled per-module, and the framework should replicate by n_mod for
the total.

The current _scale_overrides runs ref/target forwards both at the CALLER's
n_mod (= 1000/P_native). So the ref call's per-module power is P²/1000, not
P_native — meaning for accounts whose per-module value depends on per-module
power, the override gets unintentionally rescaled.

This probe quantifies the rescaling for each ARC override.
"""

from __future__ import annotations
import annotated_types
import costingfe.validation as _v
_field = _v.CostingInput.model_fields["n_mod"]
_field.annotation = float
_field.metadata = [annotated_types.Gt(0)]
_field.default = 1.0
_v.CostingInput.model_rebuild(force=True)

from costingfe import ConfinementConcept, CostModel, Fuel

P_native = 400.0
n_mod_1gw = 1000.0 / P_native
spec = dict(R0=3.3, plasma_t=1.13, elon=1.84, eta_th=0.46, p_input=38.6)
common = dict(availability=0.85, lifetime_yr=30, noak=True)
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

print(f"P_native={P_native}, n_mod_1gw={n_mod_1gw}\n")

# Library's actual reference run inside _scale_overrides (caller n_mod):
ref_current = model.forward(net_electric_mw=P_native, n_mod=n_mod_1gw, **common, **spec)
# What the design semantic wants (single-module at native):
ref_intended = model.forward(net_electric_mw=P_native, n_mod=1, **common, **spec)
# Target side of _scale_overrides (caller n_mod):
tgt = model.forward(net_electric_mw=1000.0, n_mod=n_mod_1gw, **common, **spec)

accounts = ["C220101", "C220103", "C220106"]
print(f"{'account':<10} {'ref_current':>14} {'ref_intended':>14} {'tgt':>14} "
      f"{'ratio_current':>14} {'ratio_intended':>14}")
for a in accounts:
    rc = ref_current.cas22_detail.get(a, 0.0)
    ri = ref_intended.cas22_detail.get(a, 0.0)
    tv = tgt.cas22_detail.get(a, 0.0)
    rat_c = tv / rc if rc > 0 else float('nan')
    rat_i = tv / ri if ri > 0 else float('nan')
    print(f"{a:<10} {float(rc):>14.2f} {float(ri):>14.2f} {float(tv):>14.2f} "
          f"{float(rat_c):>14.4f} {float(rat_i):>14.4f}")

# CAS27 is top-level
def attr(r, a):
    return float(getattr(r.costs, a.lower())) if hasattr(r.costs, a.lower()) else float('nan')

print()
print(f"CAS27   ref_current={attr(ref_current,'cas27'):.2f}  "
      f"ref_intended={attr(ref_intended,'cas27'):.2f}  "
      f"tgt={attr(tgt,'cas27'):.2f}")

print()
print("Interpretation:")
print(" - ratio_current = the library's _scale_overrides multiplier today.")
print(" - ratio_intended = the multiplier IF the reference call were at single-module/native.")
print(" - If ratio_intended ≈ n_mod_1gw, design semantic holds (override is per-module value, library replicates).")
print(" - If ratio_current diverges, current code rescales the user's number unintentionally.")
