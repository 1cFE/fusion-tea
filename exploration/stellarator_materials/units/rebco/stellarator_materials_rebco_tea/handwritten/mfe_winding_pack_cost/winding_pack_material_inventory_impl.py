"""WI-040 typed completion of the canonical material-inventory contract."""

import math

from stellarator_materials_rebco_tea.modules.mfe_winding_pack_cost.winding_pack_material_inventory import (
    Winding_Pack_Material_InventoryInput,
)
from stellarator_materials_rebco_tea.schemas.winding_pack_material_inventory_output import (
    Winding_Pack_Material_InventoryOutput,
)

AUTO_IMPLEMENTED = False


def run_winding_pack_material_inventory(
    inputs: Winding_Pack_Material_InventoryInput,
) -> tuple[float, float, float, float, float, float, float, float, float, float, float]:
    """Price four non-tape material inventories at their declared physical state."""
    name = "Winding Pack Material Inventory"
    nonnegative = (
        "volume_in", "price_copper", "price_solder", "price_steel", "price_helium",
    )
    positive = (
        "rho_copper", "rho_solder", "rho_steel", "helium_pressure",
        "temperature", "helium_gas_constant",
    )
    fractions = ("f_copper", "f_solder", "f_steel", "f_helium")
    for key in nonnegative:
        value = getattr(inputs, key)
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name}: {key} must be finite and nonnegative")
    for key in positive:
        value = getattr(inputs, key)
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name}: {key} must be finite and positive")
    for key in fractions:
        value = getattr(inputs, key)
        if not math.isfinite(value) or not 0 <= value < 1:
            raise ValueError(f"{name}: {key} must be finite and in [0, 1)")
    fraction_sum = sum(getattr(inputs, key) for key in fractions)
    if fraction_sum >= 1:
        raise ValueError(f"{name}: fraction_sum must be less than 1")

    # Division in stages avoids overflow/underflow in the denominator product.
    helium_density = inputs.helium_pressure / inputs.helium_gas_constant / inputs.temperature
    if not math.isfinite(helium_density):
        raise ValueError(f"{name}: helium_density must be finite")
    mass_copper = inputs.volume_in * inputs.f_copper * inputs.rho_copper
    mass_solder = inputs.volume_in * inputs.f_solder * inputs.rho_solder
    mass_steel = inputs.volume_in * inputs.f_steel * inputs.rho_steel
    mass_helium = inputs.volume_in * inputs.f_helium * helium_density
    cost_copper = mass_copper * inputs.price_copper
    cost_solder = mass_solder * inputs.price_solder
    cost_steel = mass_steel * inputs.price_steel
    cost_helium = mass_helium * inputs.price_helium
    material_cost = cost_copper + cost_solder + cost_steel + cost_helium
    tape_volume = inputs.volume_in * (
        1 - inputs.f_copper - inputs.f_solder - inputs.f_steel - inputs.f_helium
    )
    output = (
        mass_copper, mass_solder, mass_steel, mass_helium,
        cost_copper, cost_solder, cost_steel, cost_helium,
        material_cost, helium_density, tape_volume,
    )
    keys = (
        "mass_copper", "mass_solder", "mass_steel", "mass_helium",
        "cost_copper", "cost_solder", "cost_steel", "cost_helium",
        "material_cost", "helium_density", "tape_volume",
    )
    for key, value in zip(keys, output, strict=True):
        if not math.isfinite(value):
            raise ValueError(f"{name}: {key} must be finite")
    # The generated schema and wrapper share their output order; SysML declaration
    # order is not the generated positional ABI. Preserve meaning by field name.
    by_name = dict(zip(keys, output, strict=True))
    return tuple(by_name[key] for key in Winding_Pack_Material_InventoryOutput.model_fields)
