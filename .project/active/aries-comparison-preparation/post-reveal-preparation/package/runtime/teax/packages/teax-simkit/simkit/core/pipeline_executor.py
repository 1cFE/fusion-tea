"""Serial pipeline executor leveraging the channel-based specification."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Mapping

from pydantic import BaseModel

from ..config import schema
from ..config.schema import MultiOutput
from ..config.environment import loadenv, resolve_input_dir
from ..config.pipeline_schema import (
    ChannelSource,
    PipelineChannelBinding,
    PipelineModuleSpec,
    PipelineSpecification,
)
from ..io import readers
from ..io.output_router import OutputRouter, OutputRouterError, create_default_router
from .pipeline_graph import PipelineGraph
from .pipeline_registry import PipelineModuleRegistry
from .pipeline_validator import PipelineValidationError, PipelineValidator


class PipelineExecutionError(Exception):
    """Raised when pipeline execution fails at runtime."""
    pass


class PipelineExecutionContext:
    """Execution state for a pipeline run."""

    def __init__(
        self,
        registry: PipelineModuleRegistry,
    ) -> None:
        self.registry = registry
        self.channels: Dict[str, Any] = {}
        self.module_versions: Dict[str, str] = {}
        self.entry_artifacts: Dict[str, Path] = {}
        self.failed_module_key: str | None = None
        #: Positive write-phase signal (evaluator OUTPUT_WRITE, design C1). True
        #: only while genuinely inside the output-write phase, so a write failure
        #: is stamped honestly and entry/module failures never over-claim it.
        self.in_output_write: bool = False

    def set_channel(self, name: str, value: Any) -> None:
        self.channels[name] = value

    def get_channel(self, name: str) -> Any:
        if name not in self.channels:
            raise KeyError(f"Channel '{name}' not produced during execution")
        return self.channels[name]

    def record_entry_artifact(self, name: str, path: Path) -> None:
        self.entry_artifacts[name] = path


@dataclass(frozen=True)
class RunResult:
    """Container for pipeline execution results."""

    outputs: Mapping[str, Any]
    manifest: schema.RunManifest | None
    module_versions: Mapping[str, str]
    pipeline_metadata: schema.PipelineRunMetadata | None = None
    provenance: schema.Provenance | None = None


class SerialPipelineExecutor:
    """Executes modules in topological order using registry metadata."""

    def __init__(
        self,
        registry: PipelineModuleRegistry | None = None,
        *,
        output_router: OutputRouter | None = None,
        schema_type_registry: dict[str, type] | None = None,
        entry_loaders: dict[type, Callable] | None = None,
    ) -> None:
        """Initialize pipeline executor with optional custom registries.

        Args:
            registry: Module registry containing module descriptors. If None, creates
                     an empty registry (callers must provide registry via execute_pipeline
                     or register modules manually). Domain packages like battery_tea
                     provide registry factory functions (e.g., create_battery_registry()).
            output_router: Optional custom output router. If None, uses default router.
            schema_type_registry: Optional schema type name-to-type mapping for custom
                                 schemas. If None, only built-in TEAx schemas are available
                                 for EntryPoint loading and field reference validation.
            entry_loaders: Optional type-to-loader mapping for entry artifact loading.
                          If None, uses built-in loaders only. Custom types will need
                          loaders registered to be loadable.
        """
        self._registry = registry or PipelineModuleRegistry()
        self._output_router = output_router or create_default_router()
        self._schema_type_registry = schema_type_registry
        self._entry_loaders = entry_loaders or dict(_BUILTIN_ENTRY_LOADERS)
        self._validator = PipelineValidator(
            self._registry,
            self._output_router,
            schema_type_registry=schema_type_registry,
        )

    def build_graph(self, spec: PipelineSpecification) -> PipelineGraph:
        return self._validator.validate(spec)

    def run(
        self,
        graph: PipelineGraph,
        context: PipelineExecutionContext,
        *,
        base_output_dir: Path | None = None,
        run_name: str | None = None,
        pipeline_metadata: object | None = None,
        persist_outputs: bool = True,
    ) -> RunResult:
        context.failed_module_key = None
        spec = graph.spec
        exit_spec = next((m for m in spec.modules.values() if m.is_exit), None)
        if exit_spec is None:  # pragma: no cover - validator guarantees an exit module
            raise PipelineValidationError("Pipeline is missing an ExitPoint module")

        if persist_outputs:
            self._ensure_exit_handlers(exit_spec)

        exit_outputs: Dict[str, Any] | None = None
        for module_key in graph.topological_order:
            module_spec = spec.modules[module_key]
            if module_spec.is_entry:
                self._execute_entry(module_spec, spec, context)
                continue
            if module_spec.is_exit:
                exit_outputs = {}
                for field, binding in module_spec.outputs.items():
                    try:
                        exit_outputs[field] = context.get_channel(binding.channel_name)
                    except KeyError:
                        # Optional exit outputs may not be produced; skip here, router will record absence.
                        continue
                break
            try:
                self._execute_module(module_key, module_spec, context)
            except Exception:
                context.failed_module_key = module_key
                raise
        else:  # pragma: no cover - spec validator guarantees an exit node
            raise RuntimeError("Pipeline specification is missing an exit module")

        if exit_outputs is None:  # pragma: no cover - defensive guard
            raise RuntimeError("Pipeline execution did not encounter ExitPoint outputs")

        router_manifest: schema.RunManifest | None = None
        if persist_outputs:
            # Positive write-phase signal (design C1): set True *before* the write
            # and clear it only on success, so a failure raised here propagates
            # with the flag still True — the evaluator stamps OUTPUT_WRITE off this
            # flag, never off exception type or a null module key. (A `finally`
            # would clear it before the exception reached the evaluator.)
            context.in_output_write = True
            router_result = self._output_router.write_outputs(
                exit_spec.outputs,
                context.channels,
                base_output_dir=base_output_dir,
                run_name=run_name,
                pipeline_metadata=pipeline_metadata,
            )
            context.in_output_write = False
            router_manifest = router_result.manifest

        return RunResult(
            outputs=exit_outputs,
            manifest=router_manifest,
            module_versions=dict(context.module_versions),
        )

    # ------------------------------------------------------------------
    # Execution helpers

    def _execute_entry(
        self, module_spec: PipelineModuleSpec, spec: PipelineSpecification, context: PipelineExecutionContext
    ) -> None:
        loadenv()

        if spec.source_path is not None:
            base_dir = spec.source_path.parent
        else:
            base_dir = Path.cwd()
        for binding in module_spec.outputs.values():
            value, resolved_path = self._load_entry_binding(module_spec.key, binding, base_dir)
            context.set_channel(binding.channel_name, value)
            context.record_entry_artifact(binding.channel_name, resolved_path)

    def _execute_module(
        self,
        module_key: str,
        module_spec: PipelineModuleSpec,
        context: PipelineExecutionContext,
    ) -> None:
        descriptor = self._registry.get(module_spec.module_type)
        module = descriptor.factory()

        # Gather inputs
        kwargs: Dict[str, Any] = {}
        for field, binding in module_spec.inputs.items():
            kwargs[field] = _resolve_input(binding, context)

        outputs = module_spec.outputs
        result = module.run(**kwargs)
        data = result.data

        # Check if module returned MultiOutput container (new pattern)
        if isinstance(data, MultiOutput):
            # Multi-output mode - extract fields from MultiOutput container
            channel_dict = data.to_channel_dict()
            for field, binding in outputs.items():
                if field not in channel_dict:
                    raise RuntimeError(
                        f"Module '{module_key}' MultiOutput missing field '{field}' "
                        f"declared in YAML. Available fields: {list(channel_dict.keys())}"
                    )
                context.set_channel(binding.channel_name, channel_dict[field])
            context.module_versions[module_key] = descriptor.version
            return

        # Legacy multi-output mode - dict pattern (backward compatibility)
        if len(outputs) > 1 and isinstance(data, Mapping):
            for field, binding in outputs.items():
                context.set_channel(binding.channel_name, data[field])
            context.module_versions[module_key] = descriptor.version
            return

        # Single-output mode - assign entire data to one channel
        if len(outputs) == 1:
            binding = next(iter(outputs.values()))
            context.set_channel(binding.channel_name, data)
        else:
            # Error: multiple outputs declared but data is neither MultiOutput nor dict
            raise RuntimeError(
                f"Module '{module_key}' declared {len(outputs)} outputs in YAML "
                f"but returned {type(data).__name__} instead of MultiOutput or dict"
            )

        context.module_versions[module_key] = descriptor.version

    # ------------------------------------------------------------------
    # Utility helpers

    def _ensure_exit_handlers(self, module_spec: PipelineModuleSpec) -> None:
        for binding in module_spec.outputs.values():
            type_name = binding.type_name
            if type_name is None:
                raise OutputRouterError(
                    f"ExitPoint binding '{binding.channel_name}' is missing a type declaration"
                )
            if not self._output_router.has_handler(type_name):
                raise OutputRouterError(
                    f"No writer registered for ExitPoint output type '{type_name}'"
                )

    def _load_entry_binding(
        self,
        module_key: str,
        binding: PipelineChannelBinding,
        base_dir: Path,
    ) -> tuple[Any, Path]:
        """
        Resolve the artifact path for an entry binding. 
        
        Will first try to resolve paths relative to "base_dir", but will fall back to:
        - Resolving relative to `PYRONDO_INPUT_DIR` environment variable if it is set.
        - Resolving relative to `run_data/inputs` in the project root if `PYRONDO_INPUT_DIR` is not set.
        - Raising a `PipelineValidationError` if the artifact path cannot be resolved.

        Args:
            module_key: The key of the module that is binding the artifact.
            binding: The binding of the artifact.
            base_dir: The base directory to resolve the artifact path relative to. Should come from either the pipeline spec or the current working directory.

        Returns:
            A tuple of the artifact value and the resolved path.
        """
        if binding.artifact_path is None:
            raise ValueError(f"Entry binding '{binding.channel_name}' is missing an artifact path")
        literal = binding.artifact_path
        if not literal.is_absolute():
            literal = (base_dir / literal).resolve()
        attempted_paths = [literal]
        if literal.exists():
            resolved_path = literal
        else:
            fallback_root = resolve_input_dir()
            fallback = (fallback_root / binding.artifact_path).resolve()
            if fallback not in attempted_paths:
                attempted_paths.append(fallback)
            if fallback.exists():
                resolved_path = fallback
            else:
                attempted = ", ".join(str(path) for path in attempted_paths)
                raise PipelineValidationError(
                    (
                        f"Entry binding '{binding.channel_name}' could not locate artifact. "
                        f"Attempted paths: {attempted}"
                    ),
                    module=module_key,
                    details={
                        "channel": binding.channel_name,
                        "attempted_paths": [str(path) for path in attempted_paths],
                    },
                )

        # Use instance registry for type resolution
        type_cls = _resolve_schema_type(binding.type_name, self._schema_type_registry)

        # Use instance loaders
        loader = self._entry_loaders.get(type_cls)
        if loader is None:
            raise ValueError(
                f"No loader registered for entry binding type '{binding.type_name}'. "
                f"Built-in types should have loaders automatically. For custom types, "
                f"ensure the type is included in custom_schema_types parameter."
            )
        return loader(resolved_path), resolved_path


# ----------------------------------------------------------------------
# Helper functions

# Single source of truth for primitive type mapping lives in config.schema
# (shared with the output router). Aliased privately here so the existing
# references in _build_schema_type_registry() and _resolve_schema_type()
# continue to read _PRIMITIVE_TYPES unchanged.
_PRIMITIVE_TYPES: dict[str, type] = schema.PRIMITIVE_TYPES


def _resolve_schema_type(
    type_name: str | None,
    type_registry: dict[str, type] | None = None,
) -> type:
    """Resolve type name string to type object using registry.

    Args:
        type_name: String name of schema type (e.g., "FinancialParams", "CustomParams")
        type_registry: Optional mapping of type names to type objects. If None,
                      falls back to built-in schema module for backward compatibility.

    Returns:
        Resolved type class object

    Raises:
        ValueError: If type_name is None or not found in registry/schema module
    """
    if type_name is None:
        raise ValueError("Channel binding is missing a type name")

    if type_registry is not None:
        # Use custom schema registry
        type_obj = type_registry.get(type_name)
        if type_obj is None:
            raise ValueError(
                f"Unknown schema type '{type_name}'. "
                f"If this is a custom type, ensure it's included in the "
                f"custom_schema_types parameter of execute_pipeline()."
            )
        return type_obj
    else:
        # Fall back to built-in schema module only
        type_obj = getattr(schema, type_name, None)
        if type_obj is not None:
            return type_obj
        # Check primitive types (uses same _PRIMITIVE_TYPES constant as registry builder)
        primitive = _PRIMITIVE_TYPES.get(type_name)
        if primitive is not None:
            return primitive
        raise ValueError(f"Unknown schema type '{type_name}'")


def _resolve_input(binding: PipelineChannelBinding, context: PipelineExecutionContext) -> Any:
    """
    Resolve an input binding to its actual value.

    Handles three binding types:
    1. Default bindings (return None for module to fill)
    2. Standard channel bindings (return full channel value)
    3. Field reference bindings (extract field from channel value)

    Args:
        binding: The channel binding to resolve
        context: Execution context with channel storage

    Returns:
        The resolved value (channel value, extracted field, or None)

    Raises:
        PipelineExecutionError: If field extraction fails at runtime
        KeyError: If channel doesn't exist (shouldn't happen with proper validation)
    """
    if binding.source is ChannelSource.DEFAULT:
        return None

    # Fetch channel value
    value = context.get_channel(binding.channel_name)

    # Extract field if this is a field reference
    if binding.field_path:
        try:
            extracted = getattr(value, binding.field_path)
        except AttributeError:
            # Defensive check (should be caught by validator)
            raise PipelineExecutionError(
                f"Channel '{binding.channel_name}' has no field '{binding.field_path}' "
                f"(type: {type(value).__name__})"
            )

        # Check for None on Optional fields
        if extracted is None:
            raise PipelineExecutionError(
                f"Field '{binding.field_path}' on channel '{binding.channel_name}' is None "
                f"(expected {binding.type_name}). Optional fields must have non-None values at runtime."
            )

        return extracted

    return value


def _build_schema_type_registry(
    custom_types: list[type] | None = None
) -> dict[str, type]:
    """Build unified schema type lookup from built-ins and custom types.

    MAINTAINER NOTE: This function manually enumerates all user-facing built-in
    schemas. When adding a new schema to simkit/config/schema.py that should be
    usable in EntryPoint/ExitPoint or field references:

    1. Add the schema to the registry dict below
    2. Update test_all_user_facing_schemas_registered() to expect the new schema
    3. Consider if schema needs custom entry loader in _BUILTIN_ENTRY_LOADERS
    4. Consider if schema needs write handler in create_default_router()

    See comment block at top of simkit/config/schema.py for full guidance.

    Creates a dictionary mapping schema type name strings to type class objects.
    Used by PipelineValidator for field reference validation and by executor
    for entry artifact loading.

    Args:
        custom_types: Optional list of custom Pydantic schema type classes.
                     Each type must be a BaseModel subclass.

    Returns:
        Dict mapping type name strings (e.g., "FinancialParams") to type objects
        (e.g., simkit.config.schema.FinancialParams class).

    Raises:
        TypeError: If any custom type is not a BaseModel subclass
        ValueError: If duplicate type names detected (custom conflicts with
                   built-in or with another custom type)

    Example:
        >>> from pydantic import BaseModel
        >>> class CustomParams(BaseModel):
        ...     value: float
        >>>
        >>> registry = _build_schema_type_registry([CustomParams])
        >>> registry["CustomParams"]
        <class 'CustomParams'>
        >>> registry["FinancialParams"]  # Built-in
        <class 'simkit.config.schema.FinancialParams'>
    """

    # Build registry starting with built-in generic schemas
    registry: dict[str, type] = {
        schema.FinancialParams.__name__: schema.FinancialParams,
        schema.FinancialResults.__name__: schema.FinancialResults,
        schema.SyncTimeGrid.__name__: schema.SyncTimeGrid,
        schema.PriceTrajectory.__name__: schema.PriceTrajectory,
        schema.MockForecastConfig.__name__: schema.MockForecastConfig,
        schema.DynamicSimConfig.__name__: schema.DynamicSimConfig,
        schema.MockForecastSeries.__name__: schema.MockForecastSeries,
        schema.SyncGuidanceSeries.__name__: schema.SyncGuidanceSeries,
        **_PRIMITIVE_TYPES,
    }

    # Track seen names (includes built-ins)
    seen_names = set(registry.keys())

    if custom_types is None:
        return registry

    # Process custom types
    for schema_type in custom_types:
        # Validate it's a proper type class
        if not (isinstance(schema_type, type) and issubclass(schema_type, BaseModel)):
            raise TypeError(
                f"Custom schema type must be a Pydantic BaseModel subclass. "
                f"Got: {schema_type} (type: {type(schema_type).__name__})"
            )

        # Extract type name
        type_name = schema_type.__name__

        # Check for duplicates
        if type_name in seen_names:
            # Determine if collision is with built-in or custom
            if type_name in registry and registry[type_name] is not schema_type:
                conflicting_type = registry[type_name]
                conflict_module = getattr(conflicting_type, "__module__", "unknown")
                raise ValueError(
                    f"Duplicate schema type name '{type_name}' detected. "
                    f"Custom type {schema_type.__module__}.{type_name} conflicts with "
                    f"existing type {conflict_module}.{type_name}. "
                    f"Rename your custom schema or use a different type."
                )
            else:
                raise ValueError(
                    f"Duplicate schema type name '{type_name}' in custom_types list. "
                    f"Each type name must be unique."
                )

        seen_names.add(type_name)
        registry[type_name] = schema_type

    return registry


def _build_entry_loaders(
    custom_types: list[type] | None = None
) -> dict[type, Any]:
    """Build entry loader registry from built-ins and custom types.

    Creates a dictionary mapping schema type classes to loader functions.
    All custom types are auto-registered with the generic JSON loader
    (readers.read_json_model) which handles standard Pydantic model
    deserialization.

    For schemas requiring special loaders (e.g., Parquet files, custom JSON
    parsing), users will need to provide custom_entry_loaders in a future
    enhancement. Current implementation covers 90% use case (JSON schemas).

    Args:
        custom_types: Optional list of custom Pydantic schema type classes.
                     Each will be registered with read_json_model() loader.

    Returns:
        Dict mapping type objects to loader functions.
        Signature of loaders: Callable[[Path], BaseModel]

    Example:
        >>> from pydantic import BaseModel
        >>> class CustomParams(BaseModel):
        ...     value: float
        >>>
        >>> loaders = _build_entry_loaders([CustomParams])
        >>> loader_fn = loaders[CustomParams]
        >>> obj = loader_fn(Path("data.json"))
        >>> isinstance(obj, CustomParams)
        True
    """
    # Start with copy of built-in loaders
    loaders = dict(_BUILTIN_ENTRY_LOADERS)

    if custom_types is None:
        return loaders

    # Auto-register custom types with generic JSON loader
    for type_cls in custom_types:
        # Use default argument closure to capture type_cls correctly in loop
        # Pattern: lambda path, cls=type_cls ensures cls binds at definition time
        loaders[type_cls] = lambda path, cls=type_cls: readers.read_json_model(path, cls)

    return loaders


def _load_financial_params(path: Path) -> schema.FinancialParams:
    return readers.read_json_model(path, schema.FinancialParams)


# Built-in entry loaders for TEAx schema types.
#
# Maps Pydantic schema type classes to loader functions that deserialize
# artifacts from disk. All loaders follow signature: Callable[[Path], BaseModel].
#
# For custom schema types, use _build_entry_loaders() instead of modifying this dict.
# Domain-specific packages (e.g., battery_tea) should register their own loaders
# via custom_schema_types parameter in execute_pipeline().
_BUILTIN_ENTRY_LOADERS: Dict[type, Any] = {
    schema.FinancialParams: _load_financial_params,
    schema.SyncTimeGrid: lambda path: readers.read_json_model(path, schema.SyncTimeGrid),
    schema.MockForecastConfig: lambda path: readers.read_json_model(path, schema.MockForecastConfig),
    schema.DynamicSimConfig: lambda path: readers.read_json_model(path, schema.DynamicSimConfig),
}


def _load_price_trajectory(path: Path) -> schema.PriceTrajectory:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "series" in payload:
        series = payload["series"]
        timestamps = [
            datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
            if isinstance(item["timestamp"], str)
            else item["timestamp"]
            for item in series
        ]
        timestamps = [
            ts if ts.tzinfo is not None else ts.replace(tzinfo=timezone.utc)
            for ts in timestamps
        ]
        values = [float(item["value"]) for item in series]
        return schema.PriceTrajectory(
            time_index=timestamps,
            values=values,
            currency=payload["currency"],
            unit=payload["unit"],
            source=payload.get("source"),
        )
    return readers.read_json_model(path, schema.PriceTrajectory)


# PriceTrajectory is a generic type
_BUILTIN_ENTRY_LOADERS[schema.PriceTrajectory] = _load_price_trajectory


def _load_json_primitive(path: Path, expected_type: type) -> float | int | str | bool:
    """Load a bare primitive from a JSON file with type checking."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not expected_type:
        raise TypeError(
            f"Expected {expected_type.__name__} from '{path}', "
            f"got {type(value).__name__}: {value!r}"
        )
    return value


# Entry loaders for the JSON-native scalars, derived from the single source of
# truth so the loadable set can never diverge from the writable/resolvable set.
# (_t default-binds the loop variable so each lambda captures its own type.)
for _primitive_type in _PRIMITIVE_TYPES.values():
    _BUILTIN_ENTRY_LOADERS[_primitive_type] = (
        lambda path, _t=_primitive_type: _load_json_primitive(path, _t)
    )
