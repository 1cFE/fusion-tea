"""WI-063 conditional sheet procurement and unpriced ground-envelope inventory.

Normative contract: models/library/analyses/mfe_winding_pack_cost.sysml.
"""
import math
from stellarator_materials_rebco_tea.modules.mfe_winding_pack_cost.winding_pack_insulation_inventory import Winding_Pack_Insulation_InventoryInput
from stellarator_materials_rebco_tea.schemas.winding_pack_insulation_inventory_output import Winding_Pack_Insulation_InventoryOutput

AUTO_IMPLEMENTED = False


def run_winding_pack_insulation_inventory(inputs: Winding_Pack_Insulation_InventoryInput) -> tuple[float, float, float, float]:
    name = "Winding Pack Insulation Inventory"
    nonnegative = ("volume_in", "internal_fraction_x", "internal_fraction_y", "ground_thickness", "sheet_price")
    positive = ("wp_side", "aspect_ratio", "n_coils", "c_coil", "sheet_thickness", "f_perimeter")
    for key in nonnegative + positive:
        value = getattr(inputs, key)
        if not math.isfinite(value) or value < 0 or (key in positive and value == 0):
            raise ValueError(f"{name}: {key} must be finite and {'positive' if key in positive else 'nonnegative'}")
    if inputs.f_perimeter > 1:
        raise ValueError(f"{name}: f_perimeter must be in (0, 1]")

    def checked(key, value, positive=False):
        if not math.isfinite(value) or value < 0 or (positive and value == 0):
            raise ValueError(f"{name}: {key} arithmetic overflow/underflow")
        return value

    def product(key, *values):
        value = 1.0
        for factor in values:
            expected_positive = value > 0 and factor > 0
            value = checked(key, value * factor, expected_positive)
        return value

    fx, fy = inputs.internal_fraction_x, inputs.internal_fraction_y
    fraction = checked("internal_fraction", fx + fy + product("fraction_cross_term", fx, fy))
    internal_volume = product("internal_volume", inputs.volume_in, fraction)
    root = math.sqrt(inputs.aspect_ratio)
    x = product("section_x_factor", root, checked("internal_x_factor", 1 + fx))
    y = checked("section_y_factor", checked("internal_y_factor", 1 + fy) / root, True)
    shape = checked("section_factor", x + y, True)
    path = product("coil_path", inputs.n_coils, inputs.c_coil)
    perimeter = product("integrated_perimeter", 2.0, path, inputs.wp_side, inputs.f_perimeter, shape)
    shell = product("ground_shell", inputs.ground_thickness, perimeter)
    corners = product("ground_corners", 4.0, inputs.ground_thickness, inputs.ground_thickness, path)
    ground_volume = checked("ground_volume", shell + corners)
    sheet_area = checked("sheet_area", internal_volume / inputs.sheet_thickness, internal_volume > 0)
    stock_cost = product("stock_cost", sheet_area, inputs.sheet_price)
    values = dict(internal_volume=internal_volume, ground_volume=ground_volume, sheet_area=sheet_area, stock_cost=stock_cost)
    return tuple(values[key] for key in Winding_Pack_Insulation_InventoryOutput.model_fields)
