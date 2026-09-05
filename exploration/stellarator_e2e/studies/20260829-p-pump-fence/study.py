"""Study definition for `20260829-p-pump-fence` (GSTH Item 6, goal `p-pump-fence` round 1).

One arm and two swept axes. The arm is the package's own configuration -- nothing is
held to a study-chosen block -- so this study asks what the re-based `p_pump` did to the
(R, a) design space and nothing else. Route mechanics come from the package-owned route
`studies/study_route.py`; nothing here touches the package or any tool under
`scripts/study/`.

**Why the window is the comparand's, exactly.** The question is where the `recirc_ok`
fence *moved*, and a fence position is only subtractable against another fence position
measured on the same grid. `20260821-power-cycle-ab` swept R 4.0-20.0 at 0.5 and
a 0.80-2.20 at 0.05 under the ANNEX validity mask, and this study reuses `study_route`'s
own `R_VALUES`, `A_VALUES` and `BUILD_STACK_M` rather than restating them, so the two
grids are the same object and not merely the same numbers. Adopted by owner ruling
2026-08-29 in place of the runbook's step-7 window scan (record.md section 11).

**The comparand arm.** `20260821-power-cycle-ab` ran four arms; this study runs one,
which is the package's own held configuration. That configuration *is* that study's
`arm-rankine-paper`: its baseline-geometry LCOE, 275.264, is bit-for-bit the package's
pre-WI-033 pinned headline. So the arm-to-arm comparison is exact, not approximate.

Lessons from the two prior studies applied here: the store lives beside the record
directory (`20260821-power-cycle-ab#11`); the two power-balance operands the store does
not record (`pb__p_net`, `pb__rec_frac`) are emitted from the oracle as a separate,
labelled artifact before verification (`#10`); and `points.csv` carries `case_id`
(`20260823-magnet-technology-ab#6`).

A proposal carries every axis key explicitly, at its baseline value when not swept, plus
the declared tie -- so a case is attributable from its own inputs alone.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIES = HERE.parent
if str(STUDIES) not in sys.path:
    sys.path.insert(0, str(STUDIES))

import study_route as route  # noqa: E402

STUDY_ID = "20260829-p-pump-fence"
ARM_ID = "arm-package-default"
P = route.P

# --- Held values -------------------------------------------------------------------
# `availability` and `discount_rate` were declared, traced `no_constraint_response`, and
# declined by the owner (2026-08-29, "decline those"); they are held at the comparand's
# values in every proposal and never swept. `p_pump` is not here because it is not a
# study input at all: it is the package's own held value, 195.0 MW, landed by WI-033.
# The goal's held-equal invariant is what makes the fence positions subtractable, so
# every one of these matches `20260821-power-cycle-ab`'s.
HELD = {"availability": 0.85, "discount_rate": 0.07}

# The comparand's window and mask, taken from the route rather than restated.
R_VALUES = route.R_VALUES                       # 4.0 .. 20.0 step 0.5  (33 values)
A_VALUES = route.A_VALUES                       # 0.80 .. 2.20 step 0.05 (29 values)
BUILD_STACK_M = route.BUILD_STACK_M             # validity mask R > a + 2.25 (ANNEX)
BASELINE = {"R": 12.7, "a": 1.3}                # the manifest's pinned baseline geometry

RECIRC_THRESHOLD = 0.5                          # recirc_ok bound; ANNEX section Oracle


def point(R: float, a: float) -> dict[str, float]:
    """One complete proposal: both swept axes, the declared tie, the held economics."""
    return {
        f"{P}R": R,
        f"{P}magnet__R0": R,                    # declared tie rides with R
        f"{P}a": a,
        f"{P}availability": HELD["availability"],
        f"{P}discount_rate": HELD["discount_rate"],
    }


def proposals() -> list[dict[str, float]]:
    """Row-major over (R, a) under the validity mask, then the baseline geometry.

    The baseline point is off-grid (R 12.7, a 1.3 fall between nodes) and is appended
    for the same reason the comparand appended it: the LCOE half of the goal's question
    is asked at that exact point, against that exact point's published comparand value.
    """
    grid = [point(R, a) for R in R_VALUES for a in A_VALUES if R > a + BUILD_STACK_M]
    grid.append(point(BASELINE["R"], BASELINE["a"]))
    return grid


def masked_nodes() -> list[tuple[float, float]]:
    """The (R, a) nodes the validity mask excluded, so the count is auditable."""
    return [(R, a) for R in R_VALUES for a in A_VALUES if not R > a + BUILD_STACK_M]


# --- The evaluability pre-screen ----------------------------------------------------
# At `p_pump` = 195 MW a region of the comparand's own window has net electric power
# below zero, and there the CAS10 land term takes the square root of a negative: the
# package returns `execution_failed` and the oracle returns a complex number. Those
# points are not worse designs and they are not infeasible designs -- the model cannot
# be evaluated there at all. They are pre-screened out and disclosed, never silently
# dropped, and the boundary is itself a reported result (record.md section 11).
#
# This is the pattern `20260823-magnet-technology-ab/record.md:224-226` established for
# that study's density floor -- an evaluability limit derived from the oracle, disclosed
# as a bound and not a design screen -- applied here to a two-dimensional staircase
# instead of a one-dimensional floor.


def oracle_p_net(point: dict[str, float]) -> float:
    """Net electric power [MW] from the package-owned oracle at one point.

    Reaches past `oracle_entry.evaluate` deliberately. That published surface casts every
    channel to float, so at a net-negative point it raises on the complex land term
    rather than reporting the `p_net` that explains why -- and `p_net` is exactly what the
    screen needs. Nothing here modifies the oracle; it is read, as the seam reads it.
    """
    import oracle_entry as oe

    return oe._compute(oe._oracle_overrides(point))["p_net"]


def screen(candidates: list[dict[str, float]]) -> tuple[list[dict], list[dict]]:
    """Split proposals into (evaluable, unevaluable) on the oracle's `p_net > 0`.

    Mechanism only: it reports the split and decides nothing about what to do with it.
    """
    evaluable: list[dict[str, float]] = []
    unevaluable: list[dict[str, float]] = []
    for candidate in candidates:
        p_net = oracle_p_net(candidate)
        (evaluable if isinstance(p_net, float) and p_net > 0.0 else unevaluable).append(candidate)
    return evaluable, unevaluable


def export_excluded(unevaluable: list[dict[str, float]], path: Path) -> Path:
    """The disclosed evaluability exclusions, with the `p_net` that put each one there."""
    rows = []
    for candidate in unevaluable:
        p_net = oracle_p_net(candidate)
        rows.append({
            "R": candidate[f"{P}R"],
            "a": candidate[f"{P}a"],
            "reason": "oracle p_net <= 0; the CAS10 land term takes sqrt(p_net), so the "
                      "package returns execution_failed and the oracle returns complex",
            "source": "oracle (verify_stellaris via oracle_entry), pre-screen before execution",
            "p_net_MW": p_net.real if isinstance(p_net, complex) else p_net,
            "p_net_is_complex": isinstance(p_net, complex),
        })
    rows.sort(key=lambda r: (r["R"], r["a"]))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def exclusion_boundary(unevaluable: list[dict[str, float]]) -> dict[float, float]:
    """Largest excluded `a` at each excluded `R` — the staircase, for the record."""
    boundary: dict[float, float] = {}
    for candidate in unevaluable:
        R, a = candidate[f"{P}R"], candidate[f"{P}a"]
        boundary[R] = max(boundary.get(R, a), a)
    return dict(sorted(boundary.items()))


CHANNELS = {
    "lcoe": f"{P}lcoe_calc__lcoe",
    "lcoe_1cfe": f"{P}lcoe_1cfe_calc__lcoe",
    "wall_load": f"{P}wall_load_calc__wall_load",
    "p_fus": f"{P}fusion__p_fus",
    "plasma_volume": f"{P}geom__V",
    "beta": f"{P}beta_calc__beta",
    "total_capital": f"{P}total_capital__total_capital",
    "magnet_capital": f"{P}magnet_cost__capital_cost",
    "overnight_capital": f"{P}overnight_capital__overnight_capital",
    "cas72": f"{P}cas72_calc__cost",
    "fuel": f"{P}fuel_calc__annual_fuel",
}


def _is_baseline(inp: dict) -> bool:
    return (abs(float(inp[f"{P}R"]) - BASELINE["R"]) < 1e-12
            and abs(float(inp[f"{P}a"]) - BASELINE["a"]) < 1e-12)


def export(cases, path: Path) -> Path:
    """`points.csv`, carrying `case_id` (finding `20260823-magnet-technology-ab#6`)."""
    rows = []
    for case in cases:
        inp = case.inputs
        for axis in ("availability", "discount_rate"):
            if abs(float(inp[f"{P}{axis}"]) - HELD[axis]) > 1e-12:
                raise route.RouteError(f"case moved a declined axis ({axis}): {inp}")
        row = {
            "case_id": case.candidate_id,
            "arm_id": ARM_ID,
            "R": float(inp[f"{P}R"]),
            "a": float(inp[f"{P}a"]),
            "is_baseline_point": _is_baseline(inp),
            "availability": float(inp[f"{P}availability"]),
            "discount_rate": float(inp[f"{P}discount_rate"]),
        }
        row.update(route.required_outputs(case, CHANNELS))
        verdicts = route.short_verdicts(case)
        row.update(verdicts)
        row["feasible"] = all(status == "satisfied" for status in verdicts.values())
        rows.append(row)
    rows.sort(key=lambda r: (r["is_baseline_point"], r["R"], r["a"]))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def export_oracle_operands(cases, path: Path) -> Path:
    """Recompute the power-balance operands independently for each case.

    Finding `20260821-power-cycle-ab#10`: historical v2 evidence omitted these
    fields, so this study used oracle-derived `pb__rec_frac` to read its fence.
    V3 publishes the fields; this export retains its independent oracle provenance.
    """
    import oracle_entry as oe  # the seam, beside the route

    plant = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    bounds = {
        "recirc_threshold": RECIRC_THRESHOLD,
        "wall_load_limit": plant[f"{P}wall_load_limit"],
        "p_pump_MW": plant[f"{P}p_pump"],
    }
    rows = []
    for case in cases:
        ch = oe.evaluate(dict(case.inputs))
        rows.append({
            "case_id": case.candidate_id,
            "arm_id": ARM_ID,
            "R": float(case.inputs[f"{P}R"]),
            "a": float(case.inputs[f"{P}a"]),
            "is_baseline_point": _is_baseline(case.inputs),
            "source": "oracle (verify_stellaris via oracle_entry); bounds from generated/inputs",
            "p_net_MW": ch[f"{P}pb__p_net"],
            "rec_frac": ch[f"{P}pb__rec_frac"],
            "q_eng": ch[f"{P}pb__q_eng"],
            "p_et_MW": ch[f"{P}pb__p_et"],
            "p_th_MW": ch[f"{P}pb__p_th"],
            **bounds,
        })
    rows.sort(key=lambda r: (r["is_baseline_point"], r["R"], r["a"]))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def run(record_dir: Path = HERE) -> dict[str, object]:
    """Screen for evaluability, disclose the exclusions, then run the rest.

    The policy is here and not in `screen`: unevaluable points are excluded from the
    proposal list and written to `results/excluded_points.csv`. Nothing is dropped
    quietly — the count, the boundary and the reason all reach the record.
    """
    record_dir = Path(record_dir)
    work_dir = record_dir.parent / "_work" / STUDY_ID           # beside the record (#11)

    evaluable, unevaluable = screen(proposals())
    excluded_path = export_excluded(unevaluable, record_dir / "results" / "excluded_points.csv")

    cases, db = route.run_points(STUDY_ID, evaluable, work_dir, required_channels=CHANNELS)
    completed = route._completed(cases, STUDY_ID)
    return {
        "points": export(completed, record_dir / "results" / "points.csv"),
        "oracle_operands": export_oracle_operands(
            completed, record_dir / "results" / "oracle_operands.csv"
        ),
        "excluded": excluded_path,
        "store": db,
        "counts": {"proposed": len(evaluable) + len(unevaluable),
                   "evaluated": len(completed), "excluded": len(unevaluable)},
        "boundary": exclusion_boundary(unevaluable),
    }


if __name__ == "__main__":
    print(run())
