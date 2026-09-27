"""Extract native whole-plant results and figures from a frozen study record.

No package, model, oracle or planning-result imports. Headline economics and
eligibility come from stored native outputs and verdicts. Cost figures divide
published PV components by published energy PV; they do not calculate LCOE.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

P = "whole_plant_conversion__plant__"
BRANCHES = ("steam", "gas")
COST_BAND_USD2025_MWH = 5.0
POWER_BAND_MW = 5.0
RANKING_ROLES = {"gas_catalog", "steam_connector_catalog",
                 "rerank_nominal_supported_catalog", "newly_admitted_scenario_offer",
                 "rerank_performance_supported_catalog", "rerank_performance_supported_catalog_at_price_bracket",
                 "rerank_performance_supported_catalog_at_reporting_band"}
GAS_OWNERS = set("cycle compressor_1 compressor_2 compressor_3 compressor_capacity compressor_equipment conversion_services electrical generator_capacity generator_equipment he_capacity he_duty_equipment he_hx heat_exchangers heat_rejection_equipment intercooler_1 intercooler_2 precooler pressure_loss recuperator_duty_capacity recuperator_hardware rejection_capacity return_control turbine_capacity turbine_equipment water_ic1 water_ic2 water_pre".split())
STEAM_OWNERS = {"bundle_sum"}
SHARED_STEAM_OWNERS = {"steam_operating", "steam_whole"}
CAVEAT = ("Conditional supplied reactor; source, nuclear-transport and global-construction "
          "qualification remain zero. Finite engineered offers and assumed prices. "
          "Failed native equipment/domain/energy checks cannot rank.")

# These are explicit names in the reviewed WI-098 assembly/configuration, not CAS tags.
PV_COMPONENTS = {
    "initial_financed_capital": "Initial financed capital",
    "annual_expense_pv": "Annual service, fuel, makeup and imports",
    "blanket_replacement_pv": "Blanket replacement",
    "magnet_replacement_pv": "Magnet replacement",
    "primary_replacement_pv": "Primary replacement",
    "overhaul_pv": "Other overhaul",
    "conversion_replacement_pv": "Conversion replacement",
    "terminal_pv": "Terminal net cost",
}
WHOLE_FIELDS = tuple(PV_COMPONENTS) + (
    "annual_source_service", "annual_service", "annual_makeup", "annual_expense",
    "source_replacement_pv", "total_cost_pv", "energy_pv", "lcoe_USD2025_MWh",
    "blanket_events", "magnet_events", "primary_events", "blanket_life_years",
    "magnet_life_years", "outage_years", "outage_margin", "economic_defined",
    "domain_supported", "cost_residual")
OPERATING_FIELDS = ("upstream_electric_MW", "net_export_MW", "standby_MW",
                    "annual_export_MWh", "annual_import_MWh", "annual_net_grid_MWh",
                    "annual_import_cost", "auxiliary_heat_MW", "auxiliary_margin_MW",
                    "primary_motor_loss_MW", "power_residual")
OVERHEAD_FIELDS = ("common_purchases", "branch_purchases", "direct_base", "contingency",
                   "indirect", "freight", "general_spares", "tax", "insurance",
                   "nonfuel_commissioning", "initial_capital", "reconciliation_residual")
FUEL_FIELDS = ("initial_T_cost", "annual_T_cost", "annual_D_cost", "annual_Li6_cost",
               "annual_fuel", "annual_T_external", "annual_D_kg", "annual_Li6_kg",
               "annual_T_bred", "annual_T_need", "annual_T_surplus", "stock_margin",
               "processing_margin", "self_sufficiency_margin")
LEDGER_FIELDS = ("gross_electric", "electrical_load", "net_electric", "total_rejected",
                 "annual_service", "annual_makeup", "capital_total", "replacement_pv",
                 *("capital_" + str(n) for n in range(1, 11)))
COMMON_ACCOUNTS = tuple("land facilities magnet heating divertor blanket shield structure vessel power_supplies remote_handling installation primary_circulators primary_pipes primary_spares primary_helium cryoplant auxiliary_rejection waste fuel_processing other_reactor reactor_controls shared_electrical miscellaneous pbl_initial owner digital_twin source_installation_allowance".split())
MAPPING = {
    "authority": "WI-098 accepted configuration: explicit native account membership; descriptive CAS tags are not used",
    "branch_capital_labels": {
        "steam": {"1": "Salt transport equipment and installation", "2": "Initial salt stock",
                  "3": "Steam generation", "4": "Steam heat rejection", "5-10": "Zero retained slots"},
        "gas": {"1-2": "Zero retained slots", "3": "Compressors", "4": "Turbine", "5": "Generator",
                "6": "Source exchanger", "7": "Interface equipment", "8": "Conversion services",
                "9": "Secondary transport including inseparable helium stock", "10": "Heat rejection"},
        "controller": "Separate local controller included once in branch capital total"},
    "prefix": P, "whole_fields": WHOLE_FIELDS, "operating_fields": OPERATING_FIELDS,
    "overhead_fields": OVERHEAD_FIELDS, "fuel_fields": FUEL_FIELDS,
    "conversion_fields": LEDGER_FIELDS, "common_accounts": COMMON_ACCOUNTS,
    "pv_components": PV_COMPONENTS,
    "branch_input_partition": {"gas_owners": sorted(GAS_OWNERS),
        "steam_owners": sorted(STEAM_OWNERS), "prefixes": {"gas_": "gas", "steam_": "steam", "salt_": "steam"},
        "shared_exceptions": sorted(SHARED_STEAM_OWNERS), "remaining_inputs": "shared"},
    "ranking_roles": sorted(RANKING_ROLES),
    "materiality": {"cost_band_USD2025_MWh": COST_BAND_USD2025_MWH, "power_band_MW": POWER_BAND_MW,
        "authority": "Whole-plant comparison contract, inherited predecessor reporting bands",
        "meaning": "Presentation choices, not physical constraints; both endpoints are included",
        "gap_direction": "gas minus steam; native headline values retained separately"},
    "gross_gas_label": "Generator electricity after compressor shaft work; do not subtract compressors again",
    "cost_plot_rule": "Published PV component divided by published energy PV only; headline is native lcoe_USD2025_MWh",
    "caveat": CAVEAT,
}


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def table(path, rows):
    columns = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, sort_keys=True) if isinstance(v, (list, dict)) else v for k, v in row.items()})


def number(row, suffix, kind="outputs"):
    value = row[kind][P + suffix]
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"nonfinite/missing numeric channel {suffix} in {row['case']}")
    return float(value)


def calc(row, owner, field):
    return number(row, owner + "__evaluate__" + field)


def input_branch(key):
    if not key.startswith(P):
        return "shared"
    owner = key.removeprefix(P).split("__")[0]
    if owner in SHARED_STEAM_OWNERS:
        return "shared"
    if owner.startswith("gas_") or owner in GAS_OWNERS:
        return "gas"
    if owner.startswith(("steam_", "salt_")) or owner in STEAM_OWNERS:
        return "steam"
    return "shared"


def common_inputs(row):
    return {k: v for k, v in row["inputs"].items() if input_branch(k) == "shared"}


def eligibility(row, branch, predicates):
    if row is None or row.get("state") != "completed":
        return False, [], "not_native_completed"
    applicable = [cid for cid, entry in predicates.items() if entry["branch"] in ("shared", branch)]
    verdicts = row["verdicts"]
    failed = [cid for cid in applicable if verdicts.get(cid) != "satisfied"]
    value = calc(row, branch + "_whole", "lcoe_USD2025_MWh")
    valid_economics = (value > 0 and calc(row, branch + "_whole", "economic_defined") == 1
                       and calc(row, branch + "_whole", "energy_pv") > 0
                       and calc(row, branch + "_operating", "net_export_MW") > 0
                       and calc(row, branch + "_operating", "annual_net_grid_MWh") > 0)
    ok = not failed and valid_economics
    return ok, failed, "shared_and_branch_pass" if ok else "native_predicate_or_energy_failure"


def metrics(row, branch):
    result = {}
    for label, owner, fields in (("whole", branch + "_whole", WHOLE_FIELDS),
                                ("power", branch + "_operating", OPERATING_FIELDS),
                                ("initial", branch + "_overheads", OVERHEAD_FIELDS),
                                ("fuel", "fuel_accounts", FUEL_FIELDS),
                                ("conversion", branch + "_ledger", LEDGER_FIELDS)):
        result.update({label + "." + field: calc(row, owner, field) for field in fields})
    for owner, field in (("source_basis", "fusion_MW"), ("source_basis", "heating_wall_MW"),
                         ("source_basis", "source_qualified"), ("source_basis", "heating_loss_MW"),
                         ("primary_loop", "p_elec"), ("primary_loop", "q_ihx"), ("primary_loop", "w_fluid"),
                         ("cryogenic_demand", "refrigeration_MW"), ("cryogenic_demand", "cold_W"),
                         ("cryogenic_demand", "intercept_W"), ("supplied_core", "coil_drive_MW"),
                         ("supplied_core", "nuclear_transport_qualified"),
                         ("supplied_core", "global_construction_qualified")):
        result[owner + "." + field] = calc(row, owner, field)
    for name in COMMON_ACCOUNTS:
        result["purchase." + name] = number(row, name + "_account__purchase__amount")
    result["purchase.tritium_initial"] = calc(row, "fuel_accounts", "initial_T_cost")
    for name in ("tf_cooling_MW", "pf_cooling_MW", "fuel_vacuum_MW", "house_MW",
                 "reactor_controls_MW", "residual_MW", "auxiliary_electric_MW"):
        result["shared_load." + name] = number(row, "steam_operating__" + name, "inputs")
    result["source_MW"] = number(row, "source_basis__q_source_MW", "inputs")
    result["deposited_heating_MW"] = number(row, "source_basis__deposited_heating_MW", "inputs")
    result["conversion.controller_capital"] = number(row, branch + "_ledger__controller_capital", "inputs")
    result["availability"] = number(row, "finance__availability", "inputs")
    return result


def comparison_labels(steam_cost, gas_cost, steam_power, gas_power, supported=True):
    """Describe differences between native outputs using the inherited reporting bands."""
    if not supported:
        return {"cost_gap_gas_minus_steam_USD2025_MWh": None, "strict_cheaper": None,
                "preference": "unsupported", "net_power_gap_gas_minus_steam_MW": None,
                "strict_higher_net_power": None, "power_comparison": "unsupported"}
    gap, power_gap = gas_cost - steam_cost, gas_power - steam_power
    strict = "steam" if gap > 0 else "gas" if gap < 0 else "equal"
    more_power = "gas" if power_gap > 0 else "steam" if power_gap < 0 else "equal"
    return {"cost_gap_gas_minus_steam_USD2025_MWh": gap, "strict_cheaper": strict,
            "preference": "indeterminate" if abs(gap) <= COST_BAND_USD2025_MWH else strict,
            "net_power_gap_gas_minus_steam_MW": power_gap, "strict_higher_net_power": more_power,
            "power_comparison": "indeterminate" if abs(power_gap) <= POWER_BAND_MW else more_power}


def extract(record):
    required = {"native": record / "results/cases.json",
                "proposals": record / "proposed-points.json",
                "membership": record / "preparation/case-membership.json",
                "predicates": record / "preparation/predicate-catalog.json"}
    docs = {name: read(path) for name, path in required.items()}
    predicates = docs["predicates"]
    if not predicates or any(x["branch"] not in ("shared", *BRANCHES) for x in predicates.values()):
        raise ValueError("invalid frozen predicate classification")
    native = {r["case"]: r for r in docs["native"]["cases"]}
    if len(native) != len(docs["native"]["cases"]):
        raise ValueError("duplicate native case label")
    proposed = {r["case"]: r for r in docs["proposals"]["cases"]}
    if set(native) - set(proposed):
        raise ValueError("native case has no frozen proposal")
    by_point = {}
    for label, row in native.items():
        point_id = digest(row["inputs"])
        if point_id != proposed[label].get("point_id", digest(proposed[label]["point"])):
            raise ValueError("native complete inputs differ from frozen proposal: " + label)
        if point_id in by_point:
            raise ValueError("duplicate native complete point")
        if row["state"] == "completed" and set(row["verdicts"]) != set(predicates):
            raise ValueError("native predicate census differs from frozen classification")
        by_point[point_id] = row
    aliases = docs["membership"]["cases"]
    if set(by_point) - {a["point_id"] for a in aliases}:
        raise ValueError("native point missing from frozen membership")
    ledger, groups = [], defaultdict(list)
    for alias in aliases:
        point_id, branch = alias["point_id"], alias["branch"]
        row = by_point.get(point_id)
        if row and number(row, "source_basis__q_source_MW", "inputs") != alias["source_MW"]:
            raise ValueError("membership source differs from native input")
        ok, failed, check = eligibility(row, branch, predicates)
        ranked = alias["role"] in RANKING_ROLES
        value = calc(row, branch + "_whole", "lcoe_USD2025_MWh") if row and row["state"] == "completed" else None
        entry = {"alias": alias["case"], "point_id": point_id, "native_case": row["case"] if row else None,
                 "candidate_id": row.get("candidate_id") if row else None,
                 "scenario": alias["scenario"], "family": alias["family"], "source_MW": alias["source_MW"],
                 "branch": branch, "role": alias["role"], "state": row["state"] if row else "not_native_executed",
                 "eligible": ok, "catalog_ranking": ranked, "native_check_status": check,
                 "failed_predicates": failed, "native_lcoe_USD2025_MWh": value}
        ledger.append(entry)
        groups[(entry["scenario"], entry["source_MW"], branch)].append(entry)
    rankings = []
    for (scenario, source, branch), entries in sorted(groups.items()):
        catalog = [e for e in entries if e["catalog_ranking"]]
        eligible = [e for e in catalog if e["eligible"]]
        unique = {e["point_id"]: e for e in eligible}
        selected = min(unique.values(), key=lambda x: (x["native_lcoe_USD2025_MWh"], x["native_case"])) if unique else None
        result = {"scenario": scenario, "source_MW": source, "branch": branch,
                  "family": entries[0]["family"], "attempted_aliases": len(entries),
                  "catalog_aliases": len(catalog), "unique_eligible_catalog_points": len(unique),
                  "status": "supported_catalog_minimum" if selected else "unsupported" if catalog else "diagnostic_only",
                  "selected": selected}
        if selected:
            row = by_point[selected["point_id"]]
            result["metrics"] = metrics(row, branch)
            result["common_input_digest"] = digest(common_inputs(row))
        rankings.append(result)
    matches = []
    for scenario, source in sorted({(r["scenario"], r["source_MW"]) for r in rankings}):
        pair = {r["branch"]: r for r in rankings if r["scenario"] == scenario and r["source_MW"] == source}
        supported = all(pair.get(b, {}).get("selected") for b in BRANCHES)
        same_common = supported and pair["steam"]["common_input_digest"] == pair["gas"]["common_input_digest"]
        if scenario == "nominal" and supported and not same_common:
            raise ValueError("nominal branch minima do not share all common inputs")
        matches.append({"scenario": scenario, "source_MW": source,
                        "matched_supported": bool(same_common),
                        "common_input_digest": pair["steam"]["common_input_digest"] if same_common else None,
                        "steam_case": pair.get("steam", {}).get("selected"),
                        "gas_case": pair.get("gas", {}).get("selected"),
                        **comparison_labels(
                            pair["steam"]["selected"]["native_lcoe_USD2025_MWh"] if same_common else None,
                            pair["gas"]["selected"]["native_lcoe_USD2025_MWh"] if same_common else None,
                            pair["steam"]["metrics"]["power.net_export_MW"] if same_common else None,
                            pair["gas"]["metrics"]["power.net_export_MW"] if same_common else None,
                            supported=bool(same_common)),
                        "cost_materiality_band_USD2025_MWh": COST_BAND_USD2025_MWH,
                        "power_materiality_band_MW": POWER_BAND_MW,
                        "interpretation": "finite catalog comparison; strict algebraic ordering is separate from reporting materiality" if same_common else "no supported matched catalog pair"})
    fingerprints = sorted({r["executable_fingerprint"] for r in native.values()})
    if len(fingerprints) != 1:
        raise ValueError("native results mix executable identities")
    used = {str(path.relative_to(record)): hashlib.sha256(path.read_bytes()).hexdigest() for path in required.values()}
    return {"kind": "stored native catalog ranking", "caveat": CAVEAT, "executable_fingerprint": fingerprints[0],
            "native_cases": len(native), "membership_aliases": len(aliases), "input_artifacts": used,
            "materiality": MAPPING["materiality"], "rankings": rankings, "matched_pairs": matches}, ledger


def figures(data, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "svg.fonttype": "none", "axes.spines.top": False,
                         "axes.spines.right": False, "savefig.dpi": 180})
    nominal = [r for r in data["rankings"] if r["scenario"] == "nominal" and r["selected"]]
    labels = [f"{r['source_MW']:g} MW · {r['branch']}" for r in nominal]
    colors = ["#146c94", "#e9a23b", "#799c4b", "#9972a5", "#cc6553", "#657786", "#a27b51", "#619d98"]

    def save(fig, name, caption):
        fig.text(.01, .015, caption, ha="left", va="bottom", fontsize=7, wrap=True)
        fig.tight_layout(rect=(0, .10, 1, .98))
        fig.savefig(out / (name + ".svg"));fig.savefig(out / (name + ".png"));plt.close(fig)

    if nominal:
        fig, ax = plt.subplots(figsize=(10, 5))
        left = [0.] * len(nominal)
        for i, (field, label) in enumerate((("power.net_export_MW", "Whole-plant export"),
                                           ("conversion.electrical_load", "Conversion electric loads"),
                                           ("power.upstream_electric_MW", "Upstream electric loads"))):
            values = [r["metrics"][field] for r in nominal]
            ax.barh(labels, values, left=left, label=label, color=colors[i])
            left = [a + b for a, b in zip(left, values)]
        gross = [r["metrics"]["conversion.gross_electric"] for r in nominal]
        ax.scatter(gross, labels, color="black", marker="|", s=130, label="Native branch gross")
        ax.set(xlabel="MW electric", title="Power budget of supported nominal offers")
        ax.legend(loc="best", fontsize=8)
        power_context = "; ".join(f"{m['source_MW']:g} MW: gas−steam net {m['net_power_gap_gas_minus_steam_MW']:+.2f} MW ({m['power_comparison']})"
                                  for m in data["matched_pairs"] if m["scenario"] == "nominal" and m["matched_supported"])
        save(fig, "power-budget", "Gas gross already includes compressor shaft work. Power reporting band: ±5 MW. " + power_context + ". Conditional source.")

        fig, ax = plt.subplots(figsize=(11, 5.5))
        left = [0.] * len(nominal)
        for color, (field, label) in zip(colors, PV_COMPONENTS.items()):
            values = [r["metrics"]["whole." + field] / r["metrics"]["whole.energy_pv"] for r in nominal]
            ax.barh(labels, values, left=left, label=label, color=color)
            left = [a + b for a, b in zip(left, values)]
        ax.scatter([r["metrics"]["whole.lcoe_USD2025_MWh"] for r in nominal], labels,
                   marker="|", s=130, color="black", label="Native headline LCOE")
        ax.set(xlabel="2025 USD/MWh", title="Published whole-plant cost contributions")
        ax.legend(loc="center left", bbox_to_anchor=(1, .5), fontsize=7)
        save(fig, "whole-cost-contributions", "Published PV components / published energy PV. Annual expense includes service, fuel, makeup and imports. Conditional prices and source.")

    # Each point uses reranked native catalog minima. Diagnostic-only cases are not plotted as optima.
    scenarios = sorted({r["scenario"] for r in data["rankings"] if r["catalog_aliases"]})
    sources = sorted({r["source_MW"] for r in data["rankings"] if r["catalog_aliases"]})
    lookup = {(r["scenario"], r["source_MW"], r["branch"]): r for r in data["rankings"]}
    fig, axes = plt.subplots(1, len(sources), figsize=(5 * len(sources), max(5, .25 * len(scenarios))), squeeze=False, sharey=True)
    for ax, source in zip(axes[0], sources):
        for index, scenario in enumerate(scenarios):
            pair = [lookup.get((scenario, source, b)) for b in BRANCHES]
            if not any(pair):continue
            if all(r and r["selected"] for r in pair) and pair[0]["common_input_digest"] == pair[1]["common_input_digest"]:
                values = [r["metrics"]["whole.lcoe_USD2025_MWh"] for r in pair]
                ax.barh(index, 2 * COST_BAND_USD2025_MWH, left=values[0] - COST_BAND_USD2025_MWH,
                        height=.6, color="#dddddd", zorder=0)
                ax.plot(values, [index, index], color="#b9b9b9", zorder=1)
                if abs(values[1] - values[0]) <= COST_BAND_USD2025_MWH:
                    ax.annotate("I", (max(values), index), xytext=(5, 0), textcoords="offset points", va="center", fontsize=7)
                ax.scatter(values[0], index, color=colors[0], marker="o", s=20)
                ax.scatter(values[1], index, color=colors[1], marker="s", s=20)
            else:
                ax.scatter(0, index, marker="x", color="#a93636", s=24)
        ax.set(title=f"{source:g} MW hot source", xlabel="Native LCOE (2025 USD/MWh)")
        ax.grid(axis="x", alpha=.2)
        ax.set_yticks(range(len(scenarios)), scenarios, fontsize=7)
    axes[0][0].invert_yaxis()
    save(fig, "preference-sensitivity", "Blue: steam. Amber: gas. Gray span: steam ±5 USD/MWh; I: indeterminate. Red ×: unsupported (not zero LCOE). Conditional finite catalog.")

    # Companion view retains the continuous gap and the reporting band's exact endpoints.
    matched = {(m["scenario"], m["source_MW"]): m for m in data["matched_pairs"]}
    fig, axes = plt.subplots(1, len(sources), figsize=(5 * len(sources), max(5, .25 * len(scenarios))), squeeze=False, sharey=True)
    for ax, source in zip(axes[0], sources):
        ax.axvspan(-COST_BAND_USD2025_MWH, COST_BAND_USD2025_MWH, color="#dddddd", zorder=0)
        ax.axvline(0, color="#999999", linewidth=.7)
        for index, scenario in enumerate(scenarios):
            entry = matched.get((scenario, source))
            if entry is None:continue
            if entry["matched_supported"]:
                color = colors[0] if entry["preference"] == "steam" else colors[1] if entry["preference"] == "gas" else "#666666"
                gap = entry["cost_gap_gas_minus_steam_USD2025_MWh"]
                ax.scatter(gap, index, color=color, s=20)
                if entry["preference"] == "indeterminate":
                    ax.annotate("I", (gap, index), xytext=(5, 0), textcoords="offset points", va="center", fontsize=7)
            else:ax.scatter(0, index, marker="x", color="#a93636", s=24)
        ax.set(title=f"{source:g} MW hot source", xlabel="Gas − steam native LCOE (2025 USD/MWh)")
        ax.set_yticks(range(len(scenarios)), scenarios, fontsize=7)
        ax.grid(axis="x", alpha=.2)
    axes[0][0].invert_yaxis()
    save(fig, "preference-gap", "Gray band: −5 through +5 USD/MWh, inclusive; I: indeterminate. Strict sign changes inside this band are not material preference reversals. Red ×: unsupported.")


def predecessor_context(record, data, out):
    folder = record / "supporting/predecessor"
    if not folder.exists():
        return
    paths = [folder / "matched-study-summary.json", folder / "selected-native-cases.json"]
    summary, saved = (read(path) for path in paths)
    old = {r["case"]: r for r in saved["cases"]}
    current = {(r["source_MW"], r["branch"]): r for r in data["rankings"] if r["scenario"] == "nominal"}
    rows = []
    prefix = "component_alternatives__plant__"
    for anchor in summary["anchors"]:
        for branch in BRANCHES:
            label = anchor["gas_case" if branch == "gas" else "selected_steam_case"]
            row = old[label]
            current_row = current.get((anchor["source_MW"], branch), {})
            rows.append({"source_MW": anchor["source_MW"], "branch": branch,
                "predecessor_case": label, "predecessor_boundary": "conversion subsystem",
                "predecessor_availability": row["inputs"][prefix + branch + "_ledger__availability"],
                "predecessor_subsystem_USD2025_MWh": row["outputs"][prefix + branch + "_ledger__evaluate__cost_per_net_MWh"],
                "predecessor_subsystem_net_MW": row["outputs"][prefix + branch + "_ledger__evaluate__net_electric"],
                "whole_case": current_row.get("selected", {}).get("native_case") if current_row.get("selected") else None,
                "whole_status": current_row.get("status", "absent"),
                "whole_availability": current_row.get("metrics", {}).get("availability"),
                "whole_USD2025_MWh": current_row.get("metrics", {}).get("whole.lcoe_USD2025_MWh"),
                "whole_net_MW": current_row.get("metrics", {}).get("power.net_export_MW")})
    table(out / "predecessor-context.csv", rows)
    write(out / "predecessor-context.json", {"interpretation": "Different boundaries, availability and independently selected offers; the difference is not a pure cost add-on.",
        "source_artifacts": {str(p.relative_to(record)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}, "rows": rows})


def render(record, out):
    record, out = record.resolve(), out.resolve()
    if out.exists():
        raise ValueError("presentation already exists; preserve it and choose another output path")
    data, ledger = extract(record)
    out.mkdir(parents=True)
    write(out / "mapping-used.json", MAPPING)
    write(out / "native-ranking.json", data)
    table(out / "native-ranking.csv", [{k: v for k, v in r.items() if k not in ("metrics", "selected")} |
        {"native_case": r["selected"]["native_case"] if r["selected"] else None,
         "native_lcoe_USD2025_MWh": r["selected"]["native_lcoe_USD2025_MWh"] if r["selected"] else None} for r in data["rankings"]])
    table(out / "attempted-case-ledger.csv", ledger)
    table(out / "matched-pairs.csv", data["matched_pairs"])
    boundary_groups = {(r["scenario"], r["source_MW"]) for r in data["rankings"]
                       if r["family"] in ("economic_boundary", "reporting_boundary")}
    write(out / "economic-boundary-context.json", {
        "interpretation": "Native finite-catalog evaluations at supplied strict-zero and reporting-band brackets. Opposite strict signs inside ±5 USD2025/MWh remain reporting-indeterminate; no boundary is solved or interpolated here.",
        "materiality": MAPPING["materiality"],
        "pairs": [m for m in data["matched_pairs"] if (m["scenario"], m["source_MW"]) in boundary_groups]})
    detailed = []
    for r in data["rankings"]:
        if r["scenario"] != "nominal":continue
        detailed.append({"scenario": r["scenario"], "source_MW": r["source_MW"], "branch": r["branch"],
                         "status": r["status"], "native_case": r["selected"]["native_case"] if r["selected"] else None,
                         "native_check_status": r["selected"]["native_check_status"] if r["selected"] else "no_supported_offer",
                         **r.get("metrics", {})})
    table(out / "matched-account-table.csv", detailed)
    write(out / "scenario-summary.json", {"caveat": CAVEAT, "materiality": MAPPING["materiality"], "scenarios": data["rankings"], "matched_pairs": data["matched_pairs"]})
    figures(data, out)
    predecessor_context(record, data, out)
    readme = ["# Native whole-plant comparison", "", CAVEAT, "",
              "Cost preference is indeterminate when the absolute gas-minus-steam gap is at most 5 USD2025/MWh, including both endpoints. Exact gaps and strict cheaper-branch labels remain in `matched-pairs.csv`; `economic-boundary-context.json` separately retains native strict-crossing and reporting-band bracket results. A strict algebraic crossing inside this band is not a material preference reversal. Net-power differences use a separate inclusive ±5 MW reporting band. Both bands are presentation choices, not physical constraints.", "",
              "All headline LCOE values and engineering checks come from stored native results. A minimum is the best admitted member of the finite catalog; held-offer and edge diagnostics remain outside catalog ranking.", "",
              "`attempted-case-ledger.csv` retains every membership alias, including failed and unexecuted points. `matched-account-table.csv` gives nominal power, initial accounts, annual fuel/service/imports, replacement and terminal values with native case IDs. `scenario-summary.json` gives all scenario selections. Blue circles in the sensitivity figure denote steam; amber squares denote gas; red crosses mean no supported matched pair.", "",
              "Gas gross electricity already includes compressor shaft work. The cost figure divides published PV components by published energy PV; its black marks are the native headline LCOE. Annual fuel, nonfuel service/makeup and import charges are separated in the table; the figure retains their published combined annual-expense PV.", "",
              "When frozen predecessor receipts are present, `predecessor-context.csv` compares their original subsystem boundary and legacy 0.85 availability with the whole-plant nominal selections at 0.80. Different boundaries, availability and reranked offers prevent interpreting the gap as a pure cost addition.", "",
              "The channel/account mapping is frozen in `mapping-used.json`. It uses reviewed account membership, not descriptive CAS labels. Input evidence digests and the executable identity are in `native-ranking.json`. Qualification flags remain visible in the detailed table. This extraction is not an independent numerical verification.", ""]
    (out / "README.md").write_text("\n".join(readme))
    write(out / "presentation-manifest.json", {"renderer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "native_input_artifacts": data["input_artifacts"], "artifacts": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir())}})
    print(json.dumps({"native_cases": data["native_cases"], "membership_aliases": data["membership_aliases"], "ranking_groups": len(data["rankings"]), "out": str(out)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    render(args.record, args.out)
