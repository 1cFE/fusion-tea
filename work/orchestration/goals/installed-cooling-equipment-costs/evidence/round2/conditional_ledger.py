"""Research ledger only: conditional price analogies, never a plant cost result."""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
reference = json.loads((HERE / "reference-sizing.json").read_text())
CPI = {2006: 201.6, 2017: 245.1, 2025: 321.9}
PIPE_RATE_2017_USD_KG = 310.0
FITTING_MASS_RATIO = 14440.0 / 66560.0
RHO_STEEL_KG_M3 = 8000.0  # AGENT nominal density scenario.
PIPE_WALL_M = 0.065  # AGENT uniform-wall proxy, not a pressure qualification.

rows = []
for case in reference["cases"]:
    n = case["circuits"]
    hp = case["circulator_electric_MW"] * 1e6 / 745.6998715822702
    if n <= 0 or not math.isfinite(hp) or not 200 <= hp <= 30000:
        raise ValueError("Case is outside the explicitly priced compressor power domain")
    for material, factor in (("stainless", 2.5), ("nickel-alloy", 5.0)):
        purchase_each = factor * math.exp(7.5800 + 0.80 * math.log(hp))
        for length in (20.0, 50.0, 100.0):
            # Two representative straight main legs per circuit. Source DN values
            # motivate, but DO NOT establish, these assumed outside diameters.
            volumes = [math.pi / 4 * (d*d - (d-2*PIPE_WALL_M)**2) * length
                       for d in (1.3, 1.1)]
            straight_mass = sum(volumes) * RHO_STEEL_KG_M3 * n
            fitting_mass = straight_mass * FITTING_MASS_RATIO
            fabricated = (straight_mass + fitting_mass) * PIPE_RATE_2017_USD_KG
            # NETL generic pipe labor fraction transferred to ANL delivered
            # nuclear fabrication by explicit assumption, not nuclear calibration.
            pipe_labor = 0.50 * fabricated
            circ_2006 = purchase_each * 2 * n
            rows.append({
                "case": case["case"], "circuits": n,
                "circulator_material_scenario": material,
                "circulator_power_hp_each": hp,
                "circulator_count": 2*n,
                "circulator_purchase_USD_CE500": circ_2006,
                "circulator_purchase_USD_2025_CPI_proxy": circ_2006*CPI[2025]/CPI[2006],
                "length_m_each_main_leg": length,
                "main_pipe_length_m_total": 2*n*length,
                "straight_pipe_mass_kg": straight_mass,
                "fitting_mass_kg_proxy": fitting_mass,
                "pipe_delivered_fabrication_USD_2017": fabricated,
                "pipe_field_labor_USD_2017_analogy": pipe_labor,
                "pipe_fabrication_plus_field_labor_USD_2025_CPI_proxy": (fabricated+pipe_labor)*CPI[2025]/CPI[2017],
                "IHX_installed_area_m2_each_fixed_source_module": reference["reference"]["OB_area_m2"],
                "IHX_required_area_m2_each_conditional": case["IHX_conditional_area_m2_each"],
                "IHX_price_USD": None,
                "circulator_installation_USD": None,
                "circulator_helium_auxiliaries_USD": None,
                "pipe_valves_supports_insulation_USD": None,
                "coolant_inventory_and_secondary_equipment_USD": None,
                "cooling_lifecycle_annual_USD": None,
                "complete_installed_cooling_USD": None,
                "plant_capital_change_USD": None,
                "LCOE_change_USD_per_MWh": None,
                "checks": {
                    "compressor_power_in_source_range": True,
                    "pipe_pressure_material_design_qualified": False,
                    "helium_price_transfer_calibrated": False,
                    "installed_scope_complete": False,
                    "geometry_changes_propagated_to_hydraulics": False,
                    "is_executable_plant_prediction": False,
                },
            })

result = {
    "status": "partial conditional research ledger; null means unresolved, not zero",
    "reporting_year": 2025,
    "normalization": "General purchasing-power comparison using registered annual CPI; not equipment-specific escalation or whole-plant normalization. CE500 is treated as the source's 2006 base.",
    "raw_CPI": CPI,
    "pipe_assumptions": {
        "outside_diameters_m": [1.3, 1.1],
        "wall_m": PIPE_WALL_M, "density_kg_m3": RHO_STEEL_KG_M3,
        "fittings_mass_per_straight_mass": FITTING_MASS_RATIO,
        "basis": "AGENT simple layout sensitivity; source nominal diameters are not measured OD; 65mm is source upper wall, not a general pressure design; fitting ratio is ANL reference-layout transfer",
        "omitted": "branches, valves, supports, insulation, weld schedule, in-vessel geometry, inventories, secondary circuits",
        "hydraulics": "Held historical demands for pricing sensitivity only; no prediction of changed layout or pipe resistance",
    },
    "source_example": {
        "ANL_reference_pipe_and_fitting_lb": 81000,
        "computed_USD_2017": 81000*0.45359237*PIPE_RATE_2017_USD_KG,
        "source_rounded_USD_2017": 11.4e6,
    },
    "cases": rows,
}
(HERE / "conditional-ledger.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
for row in rows:
    if row["circulator_material_scenario"] == "stainless":
        print(row["case"], row["length_m_each_main_leg"],
              "circulator raw/CPI MUSD", round(row["circulator_purchase_USD_CE500"]/1e6, 3), round(row["circulator_purchase_USD_2025_CPI_proxy"]/1e6, 3),
              "pipe tonnes", round((row["straight_pipe_mass_kg"]+row["fitting_mass_kg_proxy"])/1000, 3),
              "pipe fabrication raw MUSD", round(row["pipe_delivered_fabrication_USD_2017"]/1e6, 3),
              "pipe incl labor CPI MUSD", round(row["pipe_fabrication_plus_field_labor_USD_2025_CPI_proxy"]/1e6, 3))
