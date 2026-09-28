"""Helper utilities for synchronous simulation time management."""
from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Literal

import pandas as pd
from pandas.tseries.frequencies import to_offset

if TYPE_CHECKING:  # pragma: no cover - imported only for type checking
    from .schema import InnerLoopConfig, SyncOuterStep


def normalize_timespan(
    raw: str | int | float | timedelta,
    unit: Literal["seconds", "minutes", "hours", "days"] | None = None,
) -> pd.Timedelta:
    """Coerce diverse time span inputs into a pandas Timedelta."""

    if isinstance(raw, pd.Timedelta):
        return raw
    if isinstance(raw, timedelta):
        return pd.Timedelta(raw)
    if isinstance(raw, (int, float)):
        if unit is None:
            raise ValueError("Numeric TimeSpan inputs require an explicit unit")
        return pd.to_timedelta(raw, unit=unit)
    if isinstance(raw, str):
        value = raw.strip()
        if not value:
            raise ValueError("TimeSpan string inputs must be non-empty")
        normalized = (
            value.replace("H", "h")
            .replace("T", "min")
            .replace("S", "s")
        )
        return pd.to_timedelta(normalized)
    raise TypeError(f"Unsupported TimeSpan input type: {type(raw)!r}")


def to_pandas_freq(delta: pd.Timedelta) -> str:
    """Return the canonical pandas frequency string for a timedelta."""

    offset = to_offset(delta)
    return offset.freqstr


def build_inner_index(outer_step: "SyncOuterStep", config: "InnerLoopConfig") -> pd.DatetimeIndex:
    """Construct the inner-loop datetime index for a given outer step."""

    freq = config.step.to_pandas_freq()
    return pd.date_range(
        start=outer_step.start,
        periods=config.samples_per_outer,
        freq=freq,
        tz=outer_step.start.tzinfo,
    )
