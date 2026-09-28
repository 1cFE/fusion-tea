"""WI-015 viability sweep: grid over (eta, G, f) using the GENERATED modules.

Calls the codegen-generated implementation functions directly
(ife_tea.handwritten.*) — the same code the teax executor ran for the anchor
checks — in-process, so a ~10k-point grid takes seconds instead of hours.

Classification per point:
  - viable: the GENERATED 'Viability Threshold' predicate (eta * gain >= threshold,
    threshold default 10.0; fusion_cycle.sysml, DI-001), called directly —
    CONSTRAINT-EXEC Item 14 (W1) landed the fix that lets this constraint lower and
    execute; W4 retired the harness's hand-duplicated `eta * G > 10` rule (formerly
    here) in favor of the model's own assertion. See
    `study/run_viability_study.py` for the full acceptance replay (old hand rule vs
    this predicate, over the same grid) that authorized the retirement — 100%
    agreement except grid points exactly ON the threshold, where the hand rule's
    strict `>` and the model's `>=` genuinely diverge (7 such points; flagged, not
    reconciled away, in `study/acceptance_table.csv`).
  - power_positive: guarded generating=1 AND named net_positive satisfied;
    zero prices are invalid sentinels, exported as NaN.
  - attractive:  viable AND power_positive AND lcoe <= $100/MWh (LCOE-threshold overlay; policy,
    stays hand-coded — not a modeled constraint)

Non-swept parameters use the historical realistic-HIF module scenario (anchor B),
not the repaired computed Osiris plant,
so the f=5 Hz, eta=0.25, G=100 grid point reproduces the $68.69 anchor.

Run from the repository root:
  .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/ife_e2e/sweep_ife.py --output-dir /tmp/ife-sweep'
The launcher supplies STOP_PARSER_TEAX_ROOT from the configured integration environment.
Output: temporary directory, or --output-dir PATH. Historical CSVs are retained.
"""

import argparse
import csv
import tempfile
import sys
import time
from pathlib import Path

from eligibility import module_balance, module_price, price_eligible

E2E = Path(__file__).parent
REPO = E2E.parent.parent

# Reuse the anchor bootstrap so standalone sweeps work in a fresh checkout.
pkg_dir = E2E / "pkg"
pkg_dir.mkdir(exist_ok=True)
link = pkg_dir / "ife_tea"
if not link.exists():
    link.symlink_to(E2E / "generated")
sys.path.insert(0, str(pkg_dir))

from ife_tea.handwritten.fusion_cycle.recirculating_power_fraction_impl import (  # noqa: E402
    run_recirculating_power_fraction,
)
from ife_tea.modules.constraints.predicates import (  # noqa: E402
    _finalize_assertion,
    constraint_pred_definition_fusion_cycle__viability_threshold,
)
from ife_tea.modules.fusion_cycle.recirculating_power_fraction import (  # noqa: E402
    Recirculating_Power_FractionInput,
)

# Historical realistic-HIF module scenario (anchor B), distinct from the repaired plant
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

LCOE_THRESHOLD = 100.0    # $/MWh overlay (policy, hand-coded — see module docstring)
VIABILITY_THRESHOLD = 10.0  # 'Viability Threshold' constraint default (fusion_cycle.sysml)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output = args.output_dir or Path(tempfile.mkdtemp(prefix="ife-sweep-"))
    output.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    rows = []
    for f in F_GRID:
        for eta in ETA_GRID:
            for g in G_GRID:
                balance = module_balance(dict(BASE, driver_efficiency=eta, gain=g, frequency=f))
                price, net_positive = module_price(balance)
                lcoe = price.price
                f_recirc = run_recirculating_power_fraction(
                    Recirculating_Power_FractionInput(
                        eta=eta, gain_in=g,
                        blanket_multiplier=BASE["blanket_energy_multiple"],
                        thermal_efficiency_in=BASE["thermal_efficiency"],
                    )
                )
                p_net_w = balance.net_electric_power
                eta_g = eta * g
                # Per-definition predicate body + stock finalize (positive assertion:
                # not negated, expected True). Migrated from the pre-epic per-usage
                # predicate `constraint_pred_ife_plant__ife_power_plant__viability` to the
                # per-definition API the pinned codegen emits (Item 13 compose migration).
                _body = constraint_pred_definition_fusion_cycle__viability_threshold(
                    eta=eta, gain_in=g, threshold=VIABILITY_THRESHOLD
                )
                verdict = _finalize_assertion(_body, is_negated=False, expected_value=True)
                viable = verdict.status == "satisfied"
                power_positive = price_eligible(lcoe, price.generating, net_positive)
                attractive = viable and power_positive and lcoe <= LCOE_THRESHOLD
                rows.append(dict(
                    frequency_hz=f, eta=round(eta, 4), gain=g,
                    eta_g=round(eta_g, 4),
                    lcoe_per_mwh=lcoe if power_positive else float("nan"),
                    f_recirc=f_recirc, p_net_mw=p_net_w / 1e6,
                    generating=price.generating, net_positive=net_positive,
                    power_positive=power_positive, viable=viable,
                    attractive=attractive,
                ))

    path = output / "sweep_results.csv"
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
    print(f"viable ('Viability Threshold' satisfied): {nv} ({100*nv/n:.1f}%)")
    print(f"attractive (viable & LCOE<=${LCOE_THRESHOLD:.0f}): {na} ({100*na/n:.1f}%)")

    # sanity: anchor B point must be on the grid and reproduce $68.69
    hit = [r for r in rows if r["frequency_hz"] == 5.0 and r["eta"] == 0.25
           and r["gain"] == 100.0]
    assert hit, "anchor B point missing from grid"
    assert hit[0]["power_positive"], "historical anchor B is ineligible"
    lc = hit[0]["lcoe_per_mwh"]
    assert abs(lc - 68.6902) < 0.001, f"anchor B on-grid check failed: {lc}"
    print(f"on-grid anchor B check: LCOE={lc:.4f} OK")


if __name__ == "__main__":
    main()
