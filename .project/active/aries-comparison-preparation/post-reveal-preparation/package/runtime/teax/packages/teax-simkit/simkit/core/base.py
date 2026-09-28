"""Common utilities for core modules."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel

InputModel = TypeVar("InputModel", bound=BaseModel)
OutputModel = TypeVar("OutputModel", bound=BaseModel)


@dataclass
class ModuleResult(Generic[OutputModel]):
    data: OutputModel
    notes: str | None = None


class ModuleBase(Generic[InputModel, OutputModel]):
    """Canonical interface for demo modules."""

    name: str = "module"
    version: str = "v0.1"

    def validate_and_fill_default(self, *args, **kwargs) -> InputModel:  # pragma: no cover - abstract
        raise NotImplementedError

    def run(self, *args, **kwargs) -> ModuleResult[OutputModel]:  # pragma: no cover - abstract
        raise NotImplementedError
