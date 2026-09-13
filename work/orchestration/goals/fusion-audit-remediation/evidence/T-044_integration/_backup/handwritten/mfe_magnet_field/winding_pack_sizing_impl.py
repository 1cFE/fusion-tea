"""WI-055 typed completion of the canonical finite winding-magnitude contract."""
import math
from stellarator_tea.modules.mfe_magnet_field.winding_pack_sizing import Winding_Pack_SizingInput

AUTO_IMPLEMENTED = False


def run_winding_pack_sizing(inputs: Winding_Pack_SizingInput) -> float:
    """Size finite nonnegative amp-turn magnitude at finite positive A/mm²."""
    if not math.isfinite(inputs.I_coil) or inputs.I_coil < 0:
        raise ValueError("Winding Pack Sizing: I_coil must be finite and nonnegative")
    if not math.isfinite(inputs.j_wp) or inputs.j_wp <= 0:
        raise ValueError("Winding Pack Sizing: j_wp must be finite and positive")
    return (((inputs.I_coil / inputs.j_wp) ** 0.5) / 1000.0)
