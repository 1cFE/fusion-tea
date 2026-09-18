"""Concrete primary-only research candidate; unresolved scope prevents a plant total."""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
reference = json.loads((HERE / "reference-sizing.json").read_text())
pipe_rows = json.loads((HERE / "conditional-ledger.json").read_text())["cases"]
CPI = {1978: 65.2, 2006: 201.6, 2017: 245.1, 2025: 321.9}
HP_W = 745.6998715822702
PSI_PA = 6894.757293168


def exchanger_mass(tube_wall=0.0015, shell_wall=0.20, accessory_kg=10000.0):
    rho, tube_od, shell_id = 8000.0, 0.01905, 3.2
    if not 0 < tube_wall < tube_od/2 or shell_wall <= 0 or accessory_kg < 0:
        raise ValueError("Invalid conceptual geometry")
    ri, ro = shell_id/2, shell_id/2+shell_wall
    masses = {
        "tubes_kg": rho*reference["reference"]["OB_area_m2"]*tube_wall*(1-tube_wall/tube_od),
        "shell_kg": rho*math.pi*(ro**2-ri**2)*13.0,
        "heads_kg": rho*4*math.pi/3*(ro**3-ri**3),
        "gross_unperforated_tubesheets_kg": 2*rho*math.pi*ri**2*0.60,
        "assumed_nozzles_baffles_supports_kg": accessory_kg,
    }
    masses["total_kg"] = sum(masses.values())
    # Triangular pitch footprint checks geometric packing only.
    required_footprint = 14852*math.sqrt(3)/2*(1.25*tube_od)**2
    return {"mass": masses, "bundle_footprint_m2": required_footprint,
            "shell_bore_area_m2": math.pi*ri**2,
            "packing_fits": required_footprint <= math.pi*ri**2,
            "pressure_qualification": "not established"}


variants = {"nominal": (0.0015, 0.20, 10000.0),
            "tube_wall_1mm": (0.001, 0.20, 10000.0),
            "tube_wall_2mm": (0.002, 0.20, 10000.0),
            "shell_wall_100mm": (0.0015, 0.10, 10000.0),
            "shell_wall_300mm": (0.0015, 0.30, 10000.0),
            "accessories_5t": (0.0015, 0.20, 5000.0),
            "accessories_20t": (0.0015, 0.20, 20000.0)}
hx_variants = {}
for label, geometry in variants.items():
    value = exchanger_mass(*geometry)
    factory = value["mass"]["total_kg"]*310.0
    value.update({"factory_delivered_USD_2017_each": factory,
                  "site_labor_USD_2017_each": 0.024*factory,
                  "site_material_USD_2017_each": 0.002*factory,
                  "component_installed_USD_2025_CPI_proxy_each": 1.026*factory*CPI[2025]/CPI[2017]})
    hx_variants[label] = value

rows = []
for case in reference["cases"]:
    n = case["circulator_count"] if "circulator_count" in case else case["circulators"]
    # Current eta_drive=1.0 makes electrical and fluid powers numerically equal.
    # BNL denominator is nominal loop pumping50hp, NOT rated motor140hp.
    duty_hp = case["circulator_electric_MW"]*1e6/HP_W
    machine = 550000*(0.5+0.5*(case["circulator_suction_pressure_Pa"]/(735*PSI_PA))*(duty_hp/50)**0.28)
    supply = machine*110000/550000  # AGENT fixed package proportion, not source scaling law.
    vendor = (machine+supply)*n
    procurement_driver = 0.155*vendor
    installation = 0.27*(vendor+procurement_driver)
    pipe = next(r for r in pipe_rows if r["case"] == case["case"] and r["length_m_each_main_leg"] == 50 and r["circulator_material_scenario"] == "stainless")
    hx = hx_variants["nominal"]
    rows.append({
        "case": case["case"], "circuits": case["circuits"],
        "active_circulators": n, "assumed_uninstalled_spares": 1,
        "BNL_machine_motor_USD_late1978_each": machine,
        "BNL_supply_USD_late1978_each_assumed_ratio": supply,
        "active_vendor_hardware_USD_late1978": vendor,
        "source_analogy_procurement_driver_USD_late1978_unassigned": procurement_driver,
        "assembly_USD_late1978_analogy": installation,
        "one_design_engineering_USD_late1978": 130000,
        "one_uninstalled_spare_USD_late1978": machine+supply,
        "active_hardware_assembly_one_design_one_spare_USD_2025_proxy_excluding_procurement": (vendor+installation+130000+machine+supply)*CPI[2025]/CPI[1978],
        "HX_factory_USD_2017": hx["factory_delivered_USD_2017_each"]*case["circuits"],
        "HX_component_installed_USD_2025_proxy": hx["component_installed_USD_2025_CPI_proxy_each"]*case["circuits"],
        "main_pipe_fittings_field_labor_USD_2025_proxy": pipe["pipe_fabrication_plus_field_labor_USD_2025_CPI_proxy"],
        "complete_primary_USD": None,
        "complete_intermediate_USD": None,
        "plant_total_USD": None,
        "LCOE_USD_per_MWh": None,
        "unresolved": ["procurement ownership versus CAS30", "target-specific circulator seals, isolation valves, bearing/control accessories beyond source package", "primary branches, valves, supports, insulation", "replacement removal and maintenance scope", "secondary architecture and accounting", "mechanical design and source-transfer uncertainty"],
    })

result = {"status": "conditional primary candidate, not integrated or a complete installed estimate",
          "source_years": "BNL December1978 quote; ORNL installation factor1987; ANL fabrication2017",
          "normalization": {"annual_CPI": CPI, "meaning": "general purchasing-power comparison only"},
          "HX_variants": hx_variants, "cases": rows}
(HERE / "primary-hardware-estimate.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
for row in rows:
    print(row["case"], "circulator candidate MUSD2025", round(row["active_hardware_assembly_one_design_one_spare_USD_2025_proxy_excluding_procurement"]/1e6, 3),
          "HX component MUSD2025", round(row["HX_component_installed_USD_2025_proxy"]/1e6, 3),
          "main pipe MUSD2025", round(row["main_pipe_fittings_field_labor_USD_2025_proxy"]/1e6, 3))
print("HX nominal tonnes", hx_variants["nominal"]["mass"]["total_kg"]/1000)
