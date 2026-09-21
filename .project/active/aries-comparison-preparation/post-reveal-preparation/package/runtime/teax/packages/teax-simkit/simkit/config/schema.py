"""Pydantic data models for the TEAx simulation framework.

This module contains generic framework types. Domain-specific types
(e.g., battery schemas) should be defined in separate packages.

IMPORTANT FOR MAINTAINERS:

When adding a new user-facing schema to this file (i.e., a schema that will be
used in EntryPoint artifact loading, module I/O, or ExitPoint writing), you MUST
also register it in the following locations:

1. simkit/core/pipeline_executor.py:_build_schema_type_registry()
   - Add schema to the manual enumeration dict
   - Update tests to expect the new schema

2. simkit/io/output_router.py:create_default_router()
   - Add schema to the manual enumeration for JSON write handlers
   - Only if schema should be writable at ExitPoint

3. simkit/core/pipeline_executor.py:_BUILTIN_ENTRY_LOADERS
   - Add entry loader function if schema requires special loading
   - Most schemas use default JSON loader (no action needed)

Schemas that do NOT need registration:
- Abstract base classes (e.g., MultiOutput)
- Pipeline metadata types (e.g., Provenance, RunManifest)
- Nested field types not used as standalone artifacts
- Internal implementation types (e.g., TimeSpan, SyncOuterStep)
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Any, Dict, List, Literal, Optional, Tuple

import pandas as pd
from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
    model_validator,
)

from . import time_utils


# Single source of truth for the JSON-native scalar types the framework
# persists and loads by default. Consumed by the output router (exit handler
# names, bare and RootModel-wrapped) and the pipeline executor (entry loaders,
# schema-type registry, type resolution). Lives here in config so both the io
# and core layers can import it without an io->core dependency cycle.
PRIMITIVE_TYPES: Dict[str, type] = {
    "float": float,
    "int": int,
    "str": str,
    "bool": bool,
}


class StrictBaseModel(BaseModel):
    """Base model enforcing immutable, validated data."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class MultiOutput(StrictBaseModel):
    """Container base class for modules that produce multiple typed outputs.

    Use this as the OutputModel for modules that need to route different
    data types to different downstream modules. Each field in the subclass
    becomes a separate channel in the pipeline.

    Example:
        >>> class AlphaNeutronSplitOutput(MultiOutput):
        ...     p_alpha: PowerValue
        ...     p_neutron: PowerValue
        ...
        >>> class AlphaNeutronSplitModule(
        ...     ModuleBase[FusionInput, AlphaNeutronSplitOutput]
        ... ):
        ...     def run(self, ...) -> ModuleResult[AlphaNeutronSplitOutput]:
        ...         return ModuleResult(
        ...             data=AlphaNeutronSplitOutput(
        ...                 p_alpha=PowerValue(value=520.5),
        ...                 p_neutron=PowerValue(value=2079.4),
        ...             )
        ...         )

    The pipeline executor will automatically extract each field and route it
    to the appropriate channel based on the YAML output declarations.

    See Also:
        - thoughts/designs/generalized_teax_type_system_design.md (Component 2)
        - thoughts/research/input_output_asymmetry_analysis.md
    """

    def to_channel_dict(self) -> Dict[str, Any]:
        """Convert multi-output fields to channel routing dict.

        Returns:
            Dictionary with field names as keys and field values as values.
            Used by executor to route outputs to separate channels.

        Example:
            >>> output = AlphaNeutronSplitOutput(p_alpha=..., p_neutron=...)
            >>> channels = output.to_channel_dict()
            >>> # {"p_alpha": PowerValue(...), "p_neutron": PowerValue(...)}
        """
        return {
            field_name: getattr(self, field_name)
            for field_name in self.__class__.model_fields.keys()
        }


# ---------------------------------------------------------------------------
# Financial analysis types (generic, not battery-specific)


class FinancialParams(StrictBaseModel):
    discount_rate: float
    analysis_years: int
    depreciation_method: Optional[str]
    tax_rate: Optional[float]
    escalation_energy: Optional[float]
    escalation_om: Optional[float]
    upfront_capex_usd: Optional[float]
    annual_om_usd: Optional[float]


class CashflowEntry(StrictBaseModel):
    year: int
    net_cashflow: float
    cumulative_cashflow: float


class LedgerEntry(StrictBaseModel):
    name: str
    amount: float
    currency: str
    category: str


class FinancialResults(StrictBaseModel):
    annual_savings: float
    cashflow: List[CashflowEntry]
    npv: float
    irr: Optional[float]
    payback_years: Optional[float]
    lcoe: Optional[float]
    lcob: Optional[float]
    ledger: List[LedgerEntry]
    currency: str
    price_year: int
    schema_version: str = "v0.1"


# ---------------------------------------------------------------------------
# Pipeline metadata types


class Provenance(StrictBaseModel):
    config_hash: str
    module_versions: Dict[str, str]
    notes: Optional[str]
    output_folder: Optional[str] = None


class PipelineRunMetadata(StrictBaseModel):
    spec_path: str
    run_description: Optional[str] = None
    output_folder: Optional[str] = None


class RunArtifactRecord(StrictBaseModel):
    channel: str
    type_name: str
    relative_path: str | None = None
    produced: bool = True


class RunManifest(StrictBaseModel):
    run_name: str
    run_directory: str
    base_output_dir: str
    short_id: str
    metadata: Dict[str, Any] | None = None
    artifacts: List[RunArtifactRecord]


# ---------------------------------------------------------------------------
# Synchronous simulation schema (Phase 1 foundations)


class TimeSpan(StrictBaseModel):
    """Flexible duration representation convertible to pandas offsets."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    raw: str | int | float | timedelta
    unit: Literal["seconds", "minutes", "hours", "days"] | None = None

    @computed_field(return_type=pd.Timedelta)
    def delta(self) -> pd.Timedelta:
        return time_utils.normalize_timespan(self.raw, self.unit)

    def to_pandas_freq(self) -> str:
        return time_utils.to_pandas_freq(self.delta)

    def total_seconds(self) -> float:
        return float(self.delta.total_seconds())


class SyncOuterStep(StrictBaseModel):
    """Outer supervisory loop step definition."""

    index: int
    start: datetime
    duration: TimeSpan

    @computed_field(return_type=datetime)
    def end(self) -> datetime:
        return self.start + self.duration.delta.to_pytimedelta()

    @model_validator(mode="after")
    def _validate_step(self) -> "SyncOuterStep":
        if self.index < 0:
            raise ValueError("SyncOuterStep index must be non-negative")
        if self.start.tzinfo is None:
            raise ValueError("SyncOuterStep.start must be timezone-aware")
        return self

    def to_timespan(self) -> TimeSpan:
        return self.duration


class InnerLoopConfig(StrictBaseModel):
    """Inner-loop configuration executed within each outer step."""

    component: str
    step: TimeSpan
    samples_per_outer: int

    @model_validator(mode="after")
    def _validate_inner(self) -> "InnerLoopConfig":
        if not self.component:
            raise ValueError("InnerLoopConfig.component must be non-empty")
        if self.samples_per_outer <= 0:
            raise ValueError("InnerLoopConfig.samples_per_outer must be positive")
        return self


class SyncTimeGrid(StrictBaseModel):
    """Composite time grid describing outer steps and nested inner loops."""

    timezone: str | None = None
    outer_steps: List[SyncOuterStep]
    inner_loops: List[InnerLoopConfig]

    @model_validator(mode="after")
    def _validate_grid(self) -> "SyncTimeGrid":
        if not self.outer_steps:
            raise ValueError("SyncTimeGrid requires at least one outer step")

        indices = [step.index for step in self.outer_steps]
        if indices != list(range(len(self.outer_steps))):
            raise ValueError("SyncTimeGrid outer step indices must be contiguous starting at 0")

        reference_duration = self.outer_steps[0].duration.delta
        for step in self.outer_steps:
            if step.start.tzinfo is None:
                raise ValueError("SyncTimeGrid outer steps require timezone-aware timestamps")
            if self.timezone is not None and str(step.start.tzinfo) != self.timezone:
                raise ValueError("SyncTimeGrid timezone mismatch between grid and outer steps")
            if step.duration.delta != reference_duration:
                raise ValueError("All SyncTimeGrid outer steps must share the same duration")

        for previous, current in zip(self.outer_steps, self.outer_steps[1:]):
            if current.start != previous.end:
                raise ValueError("SyncTimeGrid outer steps must be contiguous without gaps")

        for config in self.inner_loops:
            ratio = reference_duration / config.step.delta
            if not math.isclose(ratio, round(ratio), rel_tol=0, abs_tol=1e-9):
                raise ValueError(
                    "InnerLoopConfig.step must divide the outer step duration without remainder"
                )
            expected_samples = int(round(ratio))
            if config.samples_per_outer != expected_samples:
                raise ValueError(
                    "InnerLoopConfig.samples_per_outer must equal outer_duration / step duration"
                )
        return self

    @property
    def outer_duration(self) -> pd.Timedelta:
        return self.outer_steps[0].duration.delta


class PriceTrajectory(StrictBaseModel):
    """Time-aligned price series used for forecasting and guidance."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    time_index: List[datetime]
    values: List[float]
    currency: str
    unit: str
    source: str | None = None

    @model_validator(mode="after")
    def _validate_series(self) -> "PriceTrajectory":
        if len(self.time_index) != len(self.values):
            raise ValueError("PriceTrajectory time_index and values must be the same length")
        if len(self.time_index) == 0:
            raise ValueError("PriceTrajectory requires at least one sample")
        for ts in self.time_index:
            if ts.tzinfo is None:
                raise ValueError("PriceTrajectory timestamps must be timezone-aware")
        if len(self.time_index) > 1:
            deltas = [later - earlier for earlier, later in zip(self.time_index, self.time_index[1:])]
            first_delta = deltas[0]
            for delta in deltas[1:]:
                if delta != first_delta:
                    raise ValueError("PriceTrajectory requires uniform spacing between samples")
        return self

    def to_pandas(self) -> pd.Series:
        return pd.Series(self.values, index=pd.DatetimeIndex(self.time_index))

    @property
    def frequency(self) -> pd.Timedelta:
        if len(self.time_index) == 1:
            return pd.Timedelta(0)
        return pd.Timedelta(self.time_index[1] - self.time_index[0])

    @computed_field(return_type=datetime)
    def start(self) -> datetime:
        return self.time_index[0]

    @computed_field(return_type=datetime)
    def end(self) -> datetime:
        step = self.frequency
        if step == pd.Timedelta(0):
            return self.time_index[-1]
        return self.time_index[-1] + step.to_pytimedelta()

    @computed_field(return_type=pd.Timedelta)
    def span(self) -> pd.Timedelta:
        step = self.frequency
        if step == pd.Timedelta(0):
            return pd.Timedelta(0)
        return step * len(self.time_index)

    def slice(self, count: int) -> "PriceTrajectory":
        if count <= 0:
            raise ValueError("slice count must be positive")
        if count > len(self.time_index):
            raise ValueError("slice count exceeds available trajectory samples")
        return type(self)(
            time_index=list(self.time_index[:count]),
            values=list(self.values[:count]),
            currency=self.currency,
            unit=self.unit,
            source=self.source,
        )

    def window(self, span: str | TimeSpan) -> "PriceTrajectoryWindow":
        return PriceTrajectoryWindow.from_trajectory(self, span)


class PriceTrajectoryWindow(PriceTrajectory):
    """Price trajectory slice representing the look-ahead window for a step."""

    @model_validator(mode="after")
    def _validate_window(self) -> "PriceTrajectoryWindow":
        if self.span <= pd.Timedelta(0):
            raise ValueError("PriceTrajectoryWindow span must be positive")
        return self

    @classmethod
    def from_trajectory(
        cls,
        trajectory: "PriceTrajectory",
        span: str | TimeSpan,
    ) -> "PriceTrajectoryWindow":
        window_span = (
            span.delta
            if isinstance(span, TimeSpan)
            else time_utils.normalize_timespan(span, None)
        )
        if window_span <= pd.Timedelta(0):
            raise ValueError("PriceTrajectoryWindow span must be positive")
        if trajectory.frequency == pd.Timedelta(0):
            count = 1
        else:
            ratio = window_span / trajectory.frequency
            count = int(math.ceil(float(ratio)))
        payload = trajectory.slice(count).model_dump(exclude={"start", "end", "span"})
        return cls(**payload)

    @classmethod
    def from_series(
        cls,
        trajectory: "PriceTrajectory",
        span: str | TimeSpan,
    ) -> "PriceTrajectoryWindow":
        return cls.from_trajectory(trajectory, span)


# ---------------------------------------------------------------------------
# Forecast component types


class MockForecastMetadata(StrictBaseModel):
    currency: str
    unit: str
    component: str = "forecast"


class MockForecastConfig(StrictBaseModel):
    name: str
    seed: int | None = None
    noise_std_dev: float = 0.0
    lookahead: TimeSpan
    window_span: TimeSpan

    @model_validator(mode="after")
    def _validate_config(self) -> "MockForecastConfig":
        if self.noise_std_dev < 0:
            raise ValueError("MockForecastConfig.noise_std_dev must be non-negative")
        if self.lookahead.delta <= pd.Timedelta(0):
            raise ValueError("MockForecastConfig.lookahead must be positive")
        if self.window_span.delta <= pd.Timedelta(0):
            raise ValueError("MockForecastConfig.window_span must be positive")
        return self


class MockForecastPoint(StrictBaseModel):
    outer_index: int
    issued_at: datetime
    timestamps: Tuple[datetime, ...]
    values: Tuple[float, ...]
    metadata: MockForecastMetadata

    @model_validator(mode="after")
    def _validate_point(self) -> "MockForecastPoint":
        if self.issued_at.tzinfo is None:
            raise ValueError("MockForecastPoint.issued_at must be timezone-aware")
        if len(self.timestamps) != len(self.values):
            raise ValueError("MockForecastPoint timestamps and values must be the same length")
        for ts in self.timestamps:
            if ts.tzinfo is None:
                raise ValueError("MockForecastPoint timestamps must be timezone-aware")
        return self


class MockForecastSeries(StrictBaseModel):
    series: Tuple[MockForecastPoint, ...]

    @computed_field(return_type=Tuple[int, ...])
    def outer_indices(self) -> Tuple[int, ...]:
        return tuple(point.outer_index for point in self.series)


# ---------------------------------------------------------------------------
# Guidance component types


class GuidanceMetadata(StrictBaseModel):
    component: str = "guidance"


class SyncGuidance(StrictBaseModel):
    outer_index: int
    timestamp: datetime
    setpoint_kw: float
    metadata: GuidanceMetadata = GuidanceMetadata()

    @model_validator(mode="after")
    def _validate_guidance(self) -> "SyncGuidance":
        if self.timestamp.tzinfo is None:
            raise ValueError("SyncGuidance.timestamp must be timezone-aware")
        return self


class SyncGuidanceSeries(StrictBaseModel):
    series: Tuple[SyncGuidance, ...]

    @computed_field(return_type=Tuple[int, ...])
    def outer_indices(self) -> Tuple[int, ...]:
        return tuple(item.outer_index for item in self.series)


# ---------------------------------------------------------------------------
# Dynamics component types


class DynamicSimConfig(StrictBaseModel):
    bridge: Literal["stub", "matlab"]
    fail_at_outer_step: int | None = None
    integration_step: TimeSpan
    telemetry_fields: Tuple[str, ...]

    @model_validator(mode="after")
    def _validate_config(self) -> "DynamicSimConfig":
        if self.integration_step.delta <= pd.Timedelta(0):
            raise ValueError("DynamicSimConfig.integration_step must be positive")
        if not self.telemetry_fields:
            raise ValueError("DynamicSimConfig.telemetry_fields must not be empty")
        return self


class DynamicsStepInput(StrictBaseModel):
    outer_step: SyncOuterStep
    guidance: SyncGuidance
    inner_index: Tuple[datetime, ...]


