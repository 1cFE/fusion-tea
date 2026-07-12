"""WI-013 AI implementation pass.

Fills the 15 generated implementation stencils in
generated/handwritten/solarbatterylibrary/ with mechanical translations of the
SysML calc def expressions in
~/1cfe/sysml-codegen/tests/fixtures/solar_battery_model/library.sysml.

Every body is a line-for-line translation of the calc def's `out attribute`
expressions; line numbers cite library.sysml. No expression required anything
beyond arithmetic and `**` — nothing was outside the mechanical envelope.

Run:  uv run python fill_impls.py   (any venv; stdlib only)
"""

import re
from pathlib import Path

IMPL_DIR = Path(__file__).parent / "generated/handwritten/solarbatterylibrary"

# Bodies keyed by impl filename. Comments cite the SysML source line for each
# output expression. Return order matches the stencil's documented tuple order.
BODIES = {
    "pvmodulecostcalc_impl.py": """\
    # library.sysml:43-47
    material_cost = inputs.wattage * inputs.cost_per_watt
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
""",
    "invertercostcalc_impl.py": """\
    # library.sysml:65-69
    material_cost = inputs.power_rating * inputs.cost_per_watt
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
""",
    "arrayboscostcalc_impl.py": """\
    # library.sysml:89-93
    material_cost = (
        inputs.string_count * inputs.cost_per_string
        + inputs.panel_count * inputs.cost_per_panel_bos
    )
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
""",
    "batterypackcostcalc_impl.py": """\
    # library.sysml:112-116
    material_cost = inputs.capacity_kwh * inputs.cost_per_kwh * inputs.chemistry_factor
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
""",
    "hybridinvertercostcalc_impl.py": """\
    # library.sysml:134-138
    material_cost = inputs.power_rating * inputs.cost_per_watt
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
""",
    "batteryboscostcalc_impl.py": """\
    # library.sysml:156-160
    material_cost = inputs.pack_count * inputs.cost_per_pack_bos
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
""",
    "rackingcostcalc_impl.py": """\
    # library.sysml:180-184 (tilt_angle is a design parameter with no cost effect)
    material_cost = inputs.panel_count * inputs.cost_per_panel_rack
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
""",
    "electricalpanelcostcalc_impl.py": """\
    # library.sysml:203-207
    material_cost = inputs.base_cost + inputs.circuit_count * inputs.cost_per_circuit
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
""",
    "permittingcostcalc_impl.py": """\
    # library.sysml:224-228 (soft cost: no material/fab/install split)
    material_cost = 0.0
    fab_cost = 0.0
    install_cost = 0.0
    total_cost = inputs.system_capacity_kw * inputs.cost_per_kw
    idiot_index = 0.0
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
""",
    "allocationcostcalc_impl.py": """\
    # library.sysml:255-260
    fastener_cost = inputs.child_count * inputs.fastener_cost_per_child
    seal_cost = inputs.child_count * inputs.seal_cost_per_child
    wiring_cost = inputs.total_child_mass * inputs.wiring_cost_per_kg
    total_allocation = fastener_cost + seal_cost + wiring_cost
    material_portion = total_allocation * 0.8
    return (fastener_cost, seal_cost, wiring_cost, total_allocation, material_portion)
""",
    "energyproductioncalc_impl.py": """\
    # library.sysml:280
    return 8760.0 * inputs.p_net_mw * inputs.n_mod * inputs.plant_availability
""",
    "annualizedomcalc_impl.py": """\
    # library.sysml:295
    return inputs.om_rate_per_kw_year * inputs.p_net_kw
""",
    "annualizedfuelcalc_impl.py": """\
    # library.sysml:311
    return inputs.fuel_unit_cost * inputs.fuel_consumption
""",
    "annualizedfinancialcalc_impl.py": """\
    # library.sysml:329-332
    capital_recovery_factor = (
        inputs.discount_rate * (1.0 + inputs.discount_rate) ** inputs.plant_lifetime
        / ((1.0 + inputs.discount_rate) ** inputs.plant_lifetime - 1.0)
    )
    annualized_capital_cost = capital_recovery_factor * inputs.total_capex
    return (capital_recovery_factor, annualized_capital_cost)
""",
    "lcoecalc_impl.py": """\
    # library.sysml:352-355
    return (
        inputs.annualized_capital_cost
        + (inputs.annual_om_cost + inputs.annual_fuel_cost)
        * (1.0 + inputs.yearly_inflation) ** inputs.plant_lifetime
    ) / inputs.annual_energy_mwh
""",
}

RAISE_RE = re.compile(
    r"    raise NotImplementedError\(\n(?:.*\n)*?    \)\n?", re.MULTILINE
)


def main() -> None:
    for fname, body in BODIES.items():
        path = IMPL_DIR / fname
        text = path.read_text()
        new_text, n = RAISE_RE.subn(body, text)
        if n != 1:
            raise SystemExit(f"{fname}: expected 1 NotImplementedError block, found {n}")
        path.write_text(new_text)
        print(f"filled {fname}")
    print(f"AI pass complete: {len(BODIES)} implementations")


if __name__ == "__main__":
    main()
