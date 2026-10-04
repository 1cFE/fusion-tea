"""Render retained Round 2 evidence; never evaluate or change a plant model."""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
RECORD = ROOT / "exploration/stellarator_materials/studies/20260930-magnet-material-plant-map"
EXPECTED_SNAPSHOT = "d494d0e92768ff6ed2498c32f9d24fc1cee9e8562cf863e269f92a01eed46de7"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name, rows):
    with (HERE / name).open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def save(fig, name):
    fig.savefig(HERE / f"{name}.svg", bbox_inches="tight")
    fig.savefig(HERE / f"{name}.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    assert digest(RECORD / "snapshot.json") == EXPECTED_SNAPSHOT
    summary = json.loads((RECORD / "results/summary.json").read_text())
    cases = {r["case_id"]: r for r in csv.DictReader((RECORD / "results/cases.csv").open())}
    assert len(cases) == 2921
    maps, interactions, terms = [], [], []
    for key, cell in summary["cells"].items():
        geometry, confinement = key.split("|")
        be = cell["breakeven"]
        designs = [cell[m]["best_supported"] for m in ("rebco", "nb3sn")]
        row = {"cell": key, "geometry": geometry, "f_ren": float(confinement),
               "rebco_case": designs[0]["case_id"] if designs[0] else "",
               "nb3sn_case": designs[1]["case_id"] if designs[1] else "",
               "rebco_lcoe": designs[0]["lcoe"] if designs[0] else "",
               "nb3sn_lcoe": designs[1]["lcoe"] if designs[1] else "",
               "gap": cell["comparison"].get("lcoe_difference", ""),
               "break_even_USD2021_m": be["breakeven_USD_m"] if be else "",
               "comparison_evidence": "U", "policy_evidence": "U",
               "rebco_confinement_evidence": "U", "nb3sn_confinement_evidence": "U",
               "rebco_geometry_evidence": "U", "nb3sn_geometry_evidence": "U",
               "beta_limit_evidence": "A"}
        for price in (80, 30, 10):
            row[f"winner_at_{price}"] = be["reselection"][str(price)]["winner"] if be else "no comparison"
        for material, design in zip(("rebco", "nb3sn"), designs):
            if design:
                assert design["case_id"] in cases
                assert abs(float(cases[design["case_id"]]["lcoe"]) - design["lcoe"]) < 1e-9
                row[f"{material}_peak_field_T"] = design["B_peak"]
                row[f"{material}_R_m"] = design["inputs"]["plasma__R"]
                row[f"{material}_power_short"] = bool(design["flags"]["power_short"])
                row[f"{material}_divertor_pass"] = design["flags"]["divertor_pass"]
            else:
                for name in ("peak_field_T", "R_m", "power_short", "divertor_pass"):
                    row[f"{material}_{name}"] = ""
        maps.append(row)
        if be:
            for d in be["designs"]:
                case = cases[d["case_id"]]
                interactions.append({"cell": key, "geometry": geometry, "f_ren": float(confinement),
                                     "case_id": d["case_id"], "nb3sn_comparator": be["best_nb3sn"],
                                     "R_m": float(case["R"]), "a_m": float(case["a"]),
                                     "target_peak_T": float(case["B_peak_target"]),
                                     "actual_rebco_peak_T": float(case["B_peak"]),
                                     "equal_duty": case["equal_duty"] == "True",
                                     "crossing_USD2021_m": d["crossing_USD_m"],
                                     "slope_per_USD_m": d["slope_per_USD_m"]})
            comp = cell["comparison"]
            assert abs(sum(comp["terms"].values()) - comp["lcoe_difference"]) < 1e-9
            for group, value in comp["terms"].items():
                terms.append({"cell": key, "rebco_case": row["rebco_case"], "nb3sn_case": row["nb3sn_case"],
                              "account_group": group, "difference_USD_MWh": value})
    write_csv("map.csv", maps)
    write_csv("interactions.csv", interactions)
    write_csv("decomposition.csv", terms)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(10, 6))
    values = np.full((3, 3), np.nan)
    for row in maps:
        y = ["anchored", "helias", "arm"].index(row["geometry"])
        x = [1., 1.4, 1.8].index(row["f_ren"])
        if row["break_even_USD2021_m"] != "": values[y, x] = row["break_even_USD2021_m"]
        label = (f"Break-even ${values[y,x]:.1f}/m\n" + "/".join(row[f"winner_at_{p}"] for p in (80, 30, 10))
                 if np.isfinite(values[y,x]) else "No Nb₃Sn design passes\nthe ranking checks")
        ax.text(x, y, label + "\nEvidence: U", ha="center", va="center", fontsize=9)
    im = ax.imshow(values, cmap="YlGnBu", vmin=0, vmax=40, alpha=.45)
    fig.colorbar(im, ax=ax, label="REBCO break-even tape price (USD2021/m)")
    ax.set_xticks(range(3), ["1.0", "1.4", "1.8"])
    ax.set_yticks(range(3), ["Stellaris ratio", "HELIAS ratio hybrid", "Transferred pack-size arm"])
    ax.set_xlabel("Supplied confinement multiplier f_ren")
    ax.set_title("Conditional material preference at tape prices 80 / 30 / 10 USD2021/m")
    fig.text(.1, -.02, "U = unsupported transfer assumption. Rankings exclude breeding and divertor gaps; no plant qualification.", fontsize=9)
    save(fig, "assumption-map")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharey=True)
    for i, geometry in enumerate(("anchored", "arm")):
        for j, variable in enumerate(("target_peak_T", "R_m")):
            ax = axes[i, j]
            for f, color in zip((1., 1.4, 1.8), ("#64748b", "#007f86", "#b65a2a")):
                selected = [r for r in interactions if r["geometry"] == geometry and r["f_ren"] == f
                            and (variable != "target_peak_T" or not r["equal_duty"])]
                grouped = {}
                for r in selected: grouped.setdefault(r[variable], []).append(r["crossing_USD2021_m"])
                xs = sorted(grouped)
                if xs: ax.plot(xs, [max(grouped[x]) for x in xs], "o-", label=f"f_ren {f:g}", color=color)
            ax.axhline(10, color="grey", lw=.7, ls=":")
            ax.axhline(30, color="grey", lw=.7, ls=":")
            ax.set_title(f"{geometry}: best crossing at each tested {'field' if j == 0 else 'size'}")
            ax.set_xlabel("Target peak field (T)" if j == 0 else "Supplied major radius R (m)")
            ax.set_ylabel("REBCO break-even price (USD2021/m)")
            ax.legend(fontsize=8)
    fig.suptitle("Field and size change the price needed to beat each cell's best Nb₃Sn design")
    fig.tight_layout()
    fig.text(.08, -.025, "Field: own-sized designs only. Size: all offers, differing minor radii. Discrete points; lines guide the eye. Evidence: U.", fontsize=9)
    save(fig, "field-size-interactions")
    fig, ax = plt.subplots(figsize=(11, 6))
    keys = [r["cell"] for r in maps if r["gap"] != ""]
    groups = {"Conductor": ["conductor_purchase"], "Other capital/annual": [t["account_group"] for t in terms[:15]
              if t["account_group"] not in ("conductor_purchase", "net_electricity_denominator")],
              "Net electricity": ["net_electricity_denominator"]}
    groups["Other capital/annual"] = sorted(set(groups["Other capital/annual"]))
    xs = np.arange(len(keys))
    for idx, (label, account_groups) in enumerate(groups.items()):
        ys = [sum(t["difference_USD_MWh"] for t in terms if t["cell"] == key and t["account_group"] in account_groups) for key in keys]
        ax.bar(xs + (idx - 1) * .23, ys, width=.23, label=label)
    ax.axhline(0, color="grey", lw=.8)
    ax.set_xticks(xs, keys, rotation=30, ha="right")
    ax.set_ylabel("LCOE difference: REBCO − Nb₃Sn (USD/MWh, mixed-year basis)")
    ax.set_title("Why the best tested designs differ at the reference tape price")
    ax.legend()
    fig.tight_layout()
    fig.text(.08, -.025, "Conditional accounting at the reference prices. Unsupported transfers (U); breeding and divertor gaps excluded from ranking.", fontsize=9)
    save(fig, "lcoe-decomposition")
    receipt = {"snapshot_sha256": EXPECTED_SNAPSHOT, "sources": {name: digest(RECORD / name)
               for name in ("results/summary.json", "results/cases.csv")},
               "outputs": {p.name: digest(p) for p in HERE.iterdir() if p.suffix in (".csv", ".svg", ".png")},
               "assertions": "2921 unique retained cases; selected case/LCOE parity; decomposition closure <1e-9"}
    (HERE / "provenance.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
