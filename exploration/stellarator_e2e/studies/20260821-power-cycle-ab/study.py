"""Study definition for `20260821-power-cycle-ab` (RUN-STUDY Item 6, study 2).

Everything this study decides lives here: the three arms as fixed value blocks, the
four swept axes and their windows, the proposal list (arms x windows, one store), and
the export. Route mechanics (loader, definition, runner, baseline) are imported from
the package-owned route, `studies/study_route.py`; nothing here touches the package or
any tool under `scripts/study/`.

A proposal carries every key explicitly -- the swept axes at their baseline values when
not swept, the declared tie, and the arm's block -- so a case in the store is attributable
to its arm from its own inputs alone. The export's `arm_id` column is a convenience.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIES = HERE.parent
if str(STUDIES) not in sys.path:
    sys.path.insert(0, str(STUDIES))

import study_route as route  # noqa: E402

STUDY_ID = "20260821-power-cycle-ab"
P = route.P

# --- Arms: the power-conversion block, one fixed triple per arm ------------------
# Sources: Stellaris raw.pdf p. 3 (eta 1/3, the model as built); 1costingFE
# defaults.py:578-593 (Rankine 0.40 / 0.20284 / 0.03506; sCO2 0.47 / 0.15908 /
# 0.02258, M$/MW -> $/MW). See record.md section 2 for why there are three arms.
BLOCK_KEYS = (f"{P}eta_th", f"{P}turbine__cost_per_mw", f"{P}heat_rejection__cost_per_mw")
ARMS: dict[str, dict[str, float]] = {
    "arm-rankine-paper": {BLOCK_KEYS[0]: 0.333, BLOCK_KEYS[1]: 202840.0, BLOCK_KEYS[2]: 35060.0},
    "arm-rankine-upstream": {BLOCK_KEYS[0]: 0.40, BLOCK_KEYS[1]: 202840.0, BLOCK_KEYS[2]: 35060.0},
    "arm-sco2": {BLOCK_KEYS[0]: 0.47, BLOCK_KEYS[1]: 159080.0, BLOCK_KEYS[2]: 22580.0},
    # Decomposition arm (owner, 2026-08-22, on the pre-execution critique): sCO2
    # efficiency with the Rankine cost rates, so an sCO2 difference can be split
    # between "higher eta" and "cheaper turbine / heat rejection".
    "arm-sco2-eta-only": {BLOCK_KEYS[0]: 0.47, BLOCK_KEYS[1]: 202840.0, BLOCK_KEYS[2]: 35060.0},
}

# --- Axes and windows --------------------------------------------------------------
BASELINE = {"R": 12.7, "a": 1.3, "availability": 0.85, "discount_rate": 0.07}
R_VALUES = route.R_VALUES                      # 4.0 .. 20.0 step 0.5 (proof-of-life)
A_VALUES = route.A_VALUES                      # 0.80 .. 2.20 step 0.05 (proof-of-life)
BUILD_STACK_M = route.BUILD_STACK_M            # validity mask R > a + 2.25 (ANNEX)

# availability and discount_rate were proposed, came back `no_constraint_response`,
# and were declined by the owner (record.md section 8, 2026-08-22). They are held at
# their baseline values in every proposal and never swept. The A/B runs across the
# whole (R, a) window in every arm -- that is the "different geometries" the owner asked
# for, not an economic sweep repeated at a few points.
SWEEPS = ("grid",)


def point(arm: str, sweep: str, *, R=None, a=None, availability=None, discount_rate=None):
    """One complete proposal: all four axes, the tie, and the arm's block."""
    R = BASELINE["R"] if R is None else R
    a = BASELINE["a"] if a is None else a
    availability = BASELINE["availability"] if availability is None else availability
    discount_rate = BASELINE["discount_rate"] if discount_rate is None else discount_rate
    return {
        f"{P}R": R, f"{P}magnet__R0": R,          # declared tie rides with R
        f"{P}a": a,
        f"{P}availability": availability,
        f"{P}discount_rate": discount_rate,
        **ARMS[arm],
    }


def proposals() -> list[tuple[str, str, dict[str, float]]]:
    """(arm_id, sweep, proposal) in a fixed order: arm-major, row-major over (R, a)."""
    out = []
    for arm in ARMS:
        for R in R_VALUES:
            for a in A_VALUES:
                if R > a + BUILD_STACK_M:
                    out.append((arm, "grid", point(arm, "grid", R=R, a=a)))
        out.append((arm, "grid", point(arm, "grid")))               # the baseline geometry
    return out


def arm_of(inputs: dict) -> str:
    """Attribute a case to its arm from its own inputs (the block values)."""
    for arm, block in ARMS.items():
        if all(abs(float(inputs[k]) - v) < 1e-12 for k, v in block.items()):
            return arm
    raise route.RouteError(f"case inputs match no arm block: {inputs}")


def sweep_of(inputs: dict) -> str:
    """Every case is a grid case; a moved economic axis means a foreign store."""
    for ax in ("availability", "discount_rate"):
        if abs(float(inputs[f"{P}{ax}"]) - BASELINE[ax]) > 1e-12:
            raise route.RouteError(f"case moved a declined axis ({ax}): {inputs}")
    return "grid"


CHANNELS = dict(route.CHANNELS, p_net=f"{P}pb__p_net", rec_frac=f"{P}pb__rec_frac",
                q_eng=f"{P}pb__q_eng", p_th=f"{P}pb__p_th", p_et=f"{P}pb__p_et",
                cas72=f"{P}cas72_calc__cost", turbine_cost=f"{P}turbine_cost__cost",
                heat_rejection_cost=f"{P}heat_rejection_cost__cost",
                bop_capital=f"{P}bop_capital__bop_capital", beta=f"{P}beta_calc__beta")


def export(cases, path: Path) -> Path:
    rows = []
    for case in cases:
        inp = case.inputs
        row = {"arm_id": arm_of(inp), "sweep": sweep_of(inp),
               "R": inp[f"{P}R"], "a": inp[f"{P}a"],
               "availability": inp[f"{P}availability"], "discount_rate": inp[f"{P}discount_rate"],
               "eta_th": inp[BLOCK_KEYS[0]]}
        for name, channel in CHANNELS.items():
            row[name] = case.outputs.get(channel)
        verdicts = route.short_verdicts(case)
        row.update(verdicts)
        row["feasible"] = all(s == "satisfied" for s in verdicts.values())
        rows.append(row)
    rows.sort(key=lambda r: (r["arm_id"], r["sweep"], r["R"], r["a"], r["availability"], r["discount_rate"]))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return path


def run(out_dir: Path = HERE) -> Path:
    """Every proposal through the stock lifecycle, one store, then the export."""
    out_dir = Path(out_dir)
    props = [p for _, _, p in proposals()]
    cases, db = route.run_points(STUDY_ID, props, out_dir / "_work")
    completed = route._completed(cases, STUDY_ID)
    return export(completed, out_dir / "results" / "points.csv")


if __name__ == "__main__":
    print(run())
