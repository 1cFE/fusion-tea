"""Auto-generated implementation for SolarBatteryDesign__solar_battery_plant__p_net_kw.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    p_net_mw * 1000.0
"""

AUTO_IMPLEMENTED = True

from solar_battery_v2.modules.solarbatterydesign.solar_battery_plant.p_net_kw import p_net_kwInput


def run_solarbatterydesign__solar_battery_plant__p_net_kw(inputs: p_net_kwInput) -> float:
    """Execute p_net_kw computed attribute.

SysML Expression: p_net_mw * 1000.0
    """
    return (inputs.p_net_mw * 1000.0)
