"""Output persistence helpers for simulation pipelines."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel

from ..config import schema


def write_json_model(model: BaseModel, path: str | Path) -> Path:
    """Write a Pydantic model to a JSON file.

    Args:
        model: Pydantic model instance to serialize
        path: Path to write the JSON file

    Returns:
        Path to the written file
    """
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    payload = model.model_dump(mode="json")
    with resolved.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    return resolved


def write_json_payload(payload: Dict[str, Any] | BaseModel | Any, path: str | Path) -> Path:
    """Write a dictionary or Pydantic model to a JSON file.

    Args:
        payload: Dictionary or Pydantic model to serialize
        path: Path to write the JSON file

    Returns:
        Path to the written file
    """
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, BaseModel):
        data = payload.model_dump(mode="json")
    else:
        data = payload
    with resolved.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
    return resolved


def write_json_primitive(value: float | int | str | bool, path: str | Path) -> Path:
    """Write a bare Python primitive to a JSON file.

    Produces raw JSON (e.g., ``42.0``, ``"hello"``, ``true``) consistent with
    ``RootModel[T].model_dump(mode="json")`` output for the same value.

    Args:
        value: Primitive value to serialize
        path: Path to write the JSON file

    Returns:
        Path to the written file
    """
    if not isinstance(value, tuple(schema.PRIMITIVE_TYPES.values())):
        expected = "|".join(schema.PRIMITIVE_TYPES)
        raise TypeError(
            f"write_json_primitive expects {expected}, got {type(value).__name__}"
        )
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with resolved.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
    return resolved


def write_provenance(metadata: Dict[str, Any], path: str | Path) -> Path:
    """Write provenance metadata to a JSON file.

    Args:
        metadata: Dictionary of provenance metadata
        path: Path to write the JSON file

    Returns:
        Path to the written file
    """
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with resolved.open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
    return resolved


def write_mock_forecast_series(
    series: schema.MockForecastSeries, path: str | Path
) -> Path:
    """Write a MockForecastSeries to a JSON file.

    Args:
        series: MockForecastSeries schema object
        path: Path to write the JSON file

    Returns:
        Path to the written file
    """
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    payload = series.model_dump(mode="json")
    with resolved.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    return resolved


def write_sync_guidance_series(
    series: schema.SyncGuidanceSeries, path: str | Path
) -> Path:
    """Write a SyncGuidanceSeries to a JSON file.

    Args:
        series: SyncGuidanceSeries schema object
        path: Path to write the JSON file

    Returns:
        Path to the written file
    """
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    payload = series.model_dump(mode="json")
    with resolved.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    return resolved
