"""Independent reviewer arithmetic; not a solved steam cycle or plant evaluation."""
import json
import math

cold = 270 - 9.80665 * 40 / (.75 * 1560)
eta445 = .1802 * math.log(445 + 273) - .7823
eta480 = .1802 * math.log(480 + 273) - .7823
print(json.dumps({
    "salt_return_C": cold,
    "pinch_fraction_lower_bound_62bar_20K": (277.733 + 20 - cold) / (465 - cold),
    "eta445": eta445,
    "eta480": eta480,
    "relative_gross_change_fixed_heat": eta445 / eta480 - 1,
    "ideal_salt_heat_exergy_fraction_at_42C_sink": 1 - 315.15 * math.log(738.15 / (cold + 273.15)) / (465 - cold),
    "qualification": "Exergy ceiling is necessary only, not an attainable Rankine efficiency; no water-property solution."
}, indent=2))
