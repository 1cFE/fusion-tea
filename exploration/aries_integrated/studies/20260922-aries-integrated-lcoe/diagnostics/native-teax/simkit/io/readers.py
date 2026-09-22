"""Input adapters for loading fixtures and configs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, Type, TypeVar

import yaml
from pydantic import BaseModel

from ..config.pipeline_schema import PipelineSpecLoader, PipelineSpecification

ModelT = TypeVar("ModelT", bound=BaseModel)


def _load_raw(path: str | Path, loader: Callable[[Path], Any]) -> Any:
    resolved = Path(path)
    if not resolved.exists():
        raise FileNotFoundError(f"File not found: {resolved}")
    return loader(resolved)


def read_json_model(path: str | Path, model_cls: Type[ModelT]) -> ModelT:
    """Read a JSON file and parse it into a Pydantic model.

    Args:
        path: Path to the JSON file
        model_cls: Pydantic model class to parse the JSON into

    Returns:
        Parsed Pydantic model instance
    """
    def loader(resolved: Path) -> Dict[str, Any]:
        with resolved.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    payload = _load_raw(path, loader)
    return model_cls(**payload)


def read_yaml_config(path: str | Path) -> Dict[str, Any]:
    """Read a YAML file and return its contents as a dictionary.

    Args:
        path: Path to the YAML file

    Returns:
        Dictionary containing the YAML contents
    """
    def loader(resolved: Path) -> Dict[str, Any]:
        with resolved.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)

    return _load_raw(path, loader)


def read_pipeline_spec(path: str | Path) -> PipelineSpecification:
    """Load and validate a pipeline specification from YAML, including metadata."""

    loader = PipelineSpecLoader()
    return loader.load(path)
