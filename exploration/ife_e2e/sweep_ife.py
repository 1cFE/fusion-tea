"""WI-015 viability sweep: grid over (eta, G, f) using the GENERATED modules.

Calls the codegen-generated implementation functions directly
(ife_tea.handwritten.*) — the same code the teax executor ran for the anchor
checks — in-process, so a ~10k-point grid takes seconds instead of hours.

Classification per point (harness-side, per WI-014: constraints do not
survive codegen extraction — Phase 6 gap):
  - viable:      eta * G > 10      (DI-001, fusion_cycle.sysml
                                    'Viability Threshold')
  - power_positive: P_net > 0      (Hawker Eq. 2.12: eta_th*M*G*eta > 2)
  - attractive:  viable AND lcoe <= $100/MWh (LCOE-threshold overlay)

Non-swept parameters are held at the realistic-HIF baseline (anchor B),
so the f=5 Hz, eta=0.25, G=100 grid point reproduces the $68.69 anchor.

Run:  ../pipeline_spike/.venv-exec/bin/python sweep_ife.py
Output: data/ife_sweep/sweep_results.csv
"""

import csv
import sys
import time
from pathlib import Path

E2E = Path(__file__).parent
REPO = E2E.parent.parent
OUT = REPO / "data/ife_sweep"

pkg_dir = E2E / "pkg"
sys.path.insert(0, str(pkg_dir))

from ife_tea.handwritten.fusion_cycle.recirculating_power_fraction_impl import (  # noqa: E402
    run_recirculating_power_fraction,
)
from ife_tea.handwritten.ife_lcoe.ife_lcoe_impl import run_ife_lcoe  # noqa: E402
from ife_tea.modules.fusion_cycle.recirculating_power_fraction import (  # noqa: E402
    Recirculating_Power_FractionInput,
)
from ife_tea.modules.ife_lcoe.ife_lcoe import IFE_LCOEInput  # noqa: E402

# Realistic-HIF baseline (anchor B) for non-swept parameters
BASE = dict(
    availability=0.85, blanket_energy_multiple=1.2, discount_rate=0.05,
    driver_cost_constant=5.0, driver_energy=5.0e6, driver_lifetime_shots=1.0e9,
    om_cost_constant=30.0, plant_cost_constant=3000.0,
    target_cost_constant=0.50, thermal_efficiency=0.40,
    yield_cost_constant=5.0e6, construction_years=5.0, operational_years=40.0,
)

ETA_GRID = [0.02 + 0.01 * i for i in range(39)]          # 0.02 .. 0.40
G_GRID = [10.0 + 5.0 * i for i in range(59)]             # 10 .. 300
F_GRID = [1.0, 2.0, 5.0, 10.0, 20.0]                     # Hz

LCOE_THRESHOLD = 100.0  # $/MWh overlay
ETA_G_MIN = 10.0        # DI-001


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    rows = []
    for f in F_GRID:
        for eta in ETA_GRID:
            for g in G_GRID:
                inp = IFE_LCOEInput(
                    driver_efficiency=eta, gain=g, frequency=f, **BASE
                )
                lcoe = run_ife_lcoe(inp)
                f_recirc = run_recirculating_power_fraction(
                    Recirculating_Power_FractionInput(
                        eta=eta, gain=g,
                        blanket_multiplier=BASE["blanket_energy_multiple"],
                        thermal_efficiency=BASE["thermal_efficiency"],
                    )
                )
                # P_net > 0 iff eta_th * M * G * eta > 2 (Hawker Eq. 2.12)
                p_net_w = (BASE["driver_energy"] * f *
                           (BASE["thermal_efficiency"] * BASE["blanket_energy_multiple"]
                            * g * eta - 2.0))
                eta_g = eta * g
                viable = eta_g > ETA_G_MIN
                power_positive = p_net_w > 0.0
                attractive = viable and power_positive and lcoe <= LCOE_THRESHOLD
                rows.append(dict(
                    frequency_hz=f, eta=round(eta, 4), gain=g,
                    eta_g=round(eta_g, 4),
                    lcoe_per_mwh=lcoe if power_positive else float("nan"),
                    f_recirc=f_recirc, p_net_mw=p_net_w / 1e6,
                    power_positive=power_positive, viable=viable,
                    attractive=attractive,
                ))

    path = OUT / "sweep_results.csv"
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    nv = sum(r["viable"] for r in rows)
    na = sum(r["attractive"] for r in rows)
    npp = sum(r["power_positive"] for r in rows)
    print(f"{n} grid points in {time.time()-t0:.1f}s -> {path}")
    print(f"power-positive: {npp} ({100*npp/n:.1f}%)")
    print(f"viable (eta*G>10): {nv} ({100*nv/n:.1f}%)")
    print(f"attractive (viable & LCOE<=${LCOE_THRESHOLD:.0f}): {na} ({100*na/n:.1f}%)")

    # sanity: anchor B point must be on the grid and reproduce $68.69
    hit = [r for r in rows if r["frequency_hz"] == 5.0 and r["eta"] == 0.25
           and r["gain"] == 100.0]
    assert hit, "anchor B point missing from grid"
    lc = hit[0]["lcoe_per_mwh"]
    assert abs(lc - 68.6902) < 0.001, f"anchor B on-grid check failed: {lc}"
    print(f"on-grid anchor B check: LCOE={lc:.4f} OK")


if __name__ == "__main__":
    main()
