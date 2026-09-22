"""Registry providing metadata about available pipeline modules."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Mapping, MutableMapping

from pydantic import BaseModel

from .base import ModuleBase


ModuleFactory = Callable[[], ModuleBase]


@dataclass(frozen=True)
class ModuleDescriptor:
    """Metadata describing inputs/outputs for a pipeline module.

    Accepts any Pydantic BaseModel subclass for inputs/outputs, not just
    simkit.config.schema.StrictBaseModel. This allows external users to
    define custom schemas without depending on TEAx internal schema classes.
    """

    module_type: str
    factory: ModuleFactory
    required_inputs: Mapping[str, type[BaseModel]]
    optional_inputs: Mapping[str, type[BaseModel]]
    outputs: Mapping[str, type[BaseModel]]
    version: str


class PipelineModuleRegistry:
    """Holds descriptors for known pipeline modules.

    Use create_registry() from registry_builder to create a registry
    from module classes. Domain-specific packages (e.g., battery_tea)
    should provide their own registry factory function.
    """

    def __init__(self, modules: MutableMapping[str, ModuleDescriptor] | None = None) -> None:
        self._modules: Dict[str, ModuleDescriptor] = dict(modules or {})

    def register(self, module_type: str, descriptor: ModuleDescriptor) -> None:
        if module_type in self._modules:
            raise ValueError(f"Module type {module_type!r} already registered")
        self._modules[module_type] = descriptor

    def has(self, module_type: str) -> bool:
        return module_type in self._modules

    def get(self, module_type: str) -> ModuleDescriptor:
        if module_type not in self._modules:
            raise KeyError(module_type)
        return self._modules[module_type]

    def items(self):
        return self._modules.items()

    def copy(self) -> "PipelineModuleRegistry":
        return PipelineModuleRegistry(self._modules)
