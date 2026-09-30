"""WI-061 conditional aligned local rectangular fit, with deliberate domains."""
import math
from stellarator_materials_reference_tea.modules.mfe_winding_pack_fit.winding_pack_casing_fit import Winding_Pack_Casing_FitInput
from stellarator_materials_reference_tea.schemas.winding_pack_casing_fit_output import Winding_Pack_Casing_FitOutput

AUTO_IMPLEMENTED = False


def run_winding_pack_casing_fit(inputs: Winding_Pack_Casing_FitInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    name = 'Winding Pack Casing Fit'

    def checked(key, value, positive=False):
        if not math.isfinite(value) or (value <= 0 if positive else value < 0):
            raise ValueError(f'{name}: {key} must be finite and {"positive" if positive else "nonnegative"}')
        return value

    positive = ('wp_side', 'aspect_ratio', 'radial_allocation', 'interior_y', 'wall_thickness')
    for key in positive:
        checked(key, getattr(inputs, key), True)
    for key in ('internal_fraction_x', 'internal_fraction_y', 'ground_insulation', 'assembly_clearance'):
        checked(key, getattr(inputs, key))
    root = math.sqrt(inputs.aspect_ratio)
    out = {}
    wall = checked('two_walls', 2.0 * inputs.wall_thickness, True)
    ground = checked('two_ground_faces', 2.0 * inputs.ground_insulation, inputs.ground_insulation > 0)
    clearance = checked('two_clearance_faces', 2.0 * inputs.assembly_clearance, inputs.assembly_clearance > 0)
    out['cavity_x'] = checked('cavity_x', inputs.radial_allocation - wall, True)
    out['cavity_y'] = inputs.interior_y
    out['exterior_x'] = inputs.radial_allocation
    out['exterior_y'] = checked('exterior_y', inputs.interior_y + wall, True)
    for axis, nominal, fraction in (
        ('x', inputs.wp_side * root, inputs.internal_fraction_x),
        ('y', inputs.wp_side / root, inputs.internal_fraction_y),
    ):
        out['nominal_' + axis] = checked('nominal_' + axis, nominal, True)
        internal = checked('internal_' + axis, nominal * fraction, fraction > 0)
        out['internal_' + axis] = internal
        pack = checked('pack_' + axis, nominal + internal, True)
        out['pack_' + axis] = pack
        insulated = checked('insulated_' + axis, pack + ground, True)
        out['insulated_' + axis] = insulated
        required = checked('required_' + axis, insulated + clearance, True)
        out['required_' + axis] = required
        margin = out['cavity_' + axis] - required
        if not math.isfinite(margin):
            raise ValueError(f'{name}: margin_{axis} must be finite')
        out['margin_' + axis] = margin
    out["minimum_margin"] = min(out["margin_x"], out["margin_y"])
    return tuple(out[key] for key in Winding_Pack_Casing_FitOutput.model_fields)
