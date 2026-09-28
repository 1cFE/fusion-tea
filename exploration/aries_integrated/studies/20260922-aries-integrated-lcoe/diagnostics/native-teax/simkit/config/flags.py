"""Feature flag registry for the async demo."""
from __future__ import annotations

from typing import Dict

DEFAULT_FLAGS: Dict[str, str] = {
    "rate_profile": "tou_synth_v1",
    "battery_sizer": "heuristic_v1",
    "telemetry_policy": "tou_shave_v1",
    "project_finance": "simple_v1",
}


def merge_flags(overrides: Dict[str, str] | None) -> Dict[str, str]:
    merged = DEFAULT_FLAGS.copy()
    if overrides:
        merged.update(overrides)
    return merged
