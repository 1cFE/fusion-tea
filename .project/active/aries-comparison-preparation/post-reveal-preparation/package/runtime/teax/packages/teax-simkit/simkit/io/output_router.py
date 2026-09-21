"""Output routing infrastructure for ExitPoint artifacts."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, MutableMapping

from ..config import environment, schema
from ..config.pipeline_schema import PipelineChannelBinding
from . import writers


class OutputRouterError(Exception):
    """Raised when output routing fails due to configuration or IO issues."""


@dataclass(frozen=True)
class WriteHandler:
    fn: Callable[[Any, Path], Path]
    extension: str


@dataclass(frozen=True)
class OutputRouterResult:
    run_dir: Path
    manifest: schema.RunManifest
    manifest_path: Path


class OutputRouter:
    """Routes ExitPoint outputs to filesystem artifacts and records manifests."""

    def __init__(
        self,
        type_handlers: Mapping[str, WriteHandler],
        *,
        manifest_writer: Callable[[Any, Path], Path] | None = None,
        in_memory: bool = False,
    ) -> None:
        """Create OutputRouter for persisting pipeline outputs.

        Args:
            type_handlers: Mapping of schema type names to write handlers
            manifest_writer: Optional custom manifest writer function
            in_memory: If True, validate outputs but don't write files.
                      Useful for testing and programmatic pipeline execution.
                      Default: False (write files normally).
        """
        self._type_handlers: Dict[str, WriteHandler] = dict(type_handlers)
        self._manifest_writer = manifest_writer or writers.write_json_payload
        self._in_memory = in_memory

    def register_handler(self, type_name: str, handler: WriteHandler) -> None:
        self._type_handlers[type_name] = handler

    def has_handler(self, type_name: str) -> bool:
        return type_name in self._type_handlers

    def write_outputs(
        self,
        exit_bindings: Mapping[str, PipelineChannelBinding],
        channel_values: Mapping[str, Any],
        *,
        base_output_dir: Path | None = None,
        run_name: str | None = None,
        pipeline_metadata: object | None = None,
    ) -> OutputRouterResult:
        # In-memory mode: validate and collect without writing
        if self._in_memory:
            return self._collect_outputs_in_memory(
                exit_bindings,
                channel_values,
                run_name=run_name,
                pipeline_metadata=pipeline_metadata,
            )

        # Normal mode: validate and write to disk
        resolution = environment.resolve_output_dir(preferred=base_output_dir, run_name=run_name)
        run_dir, short_id = self._prepare_run_directory(resolution.base_dir, resolution.run_name)

        artifacts: list[schema.RunArtifactRecord] = []
        used_filenames: set[str] = set()

        for alias, binding in exit_bindings.items():
            destination = binding.destination_filename
            if not destination:
                raise OutputRouterError(f"ExitPoint binding '{alias}' is missing a destination filename")
            if destination in used_filenames:
                raise OutputRouterError(f"Destination filename '{destination}' declared more than once")
            used_filenames.add(destination)

            type_name = binding.type_name
            if type_name is None:
                raise OutputRouterError(f"ExitPoint binding '{alias}' is missing a type declaration")

            handler = self._type_handlers.get(type_name)
            if handler is None:
                raise OutputRouterError(f"No writer registered for type '{type_name}'")
            if handler.extension and not destination.endswith(handler.extension):
                raise OutputRouterError(
                    f"Destination filename '{destination}' does not match expected extension '{handler.extension}'"
                )

            channel_name = binding.channel_name
            payload = channel_values.get(channel_name)
            if payload is None:
                artifacts.append(
                    schema.RunArtifactRecord(
                        channel=channel_name,
                        type_name=type_name,
                        relative_path=None,
                        produced=False,
                    )
                )
                continue

            target_path = run_dir / destination
            handler.fn(payload, target_path)

            artifacts.append(
                schema.RunArtifactRecord(
                    channel=channel_name,
                    type_name=type_name,
                    relative_path=destination,
                    produced=True,
                )
            )

        metadata_payload = None
        if pipeline_metadata is not None:
            if hasattr(pipeline_metadata, "model_dump"):
                metadata_payload = pipeline_metadata.model_dump()
            elif isinstance(pipeline_metadata, Mapping):
                metadata_payload = dict(pipeline_metadata)
            else:
                raise OutputRouterError(
                    "pipeline_metadata must be a mapping or provide a model_dump() method"
                )

        manifest = schema.RunManifest(
            run_name=resolution.run_name,
            run_directory=run_dir.name,
            base_output_dir=str(resolution.base_dir),
            short_id=short_id,
            metadata=metadata_payload,
            artifacts=artifacts,
        )
        manifest_path = run_dir / "manifest.json"
        self._manifest_writer(manifest, manifest_path)

        return OutputRouterResult(run_dir=run_dir, manifest=manifest, manifest_path=manifest_path)

    def _collect_outputs_in_memory(
        self,
        exit_bindings: Mapping[str, PipelineChannelBinding],
        channel_values: Mapping[str, Any],
        *,
        run_name: str | None = None,
        pipeline_metadata: object | None = None,
    ) -> OutputRouterResult:
        """Validate outputs without writing to disk (in-memory mode).

        Performs all validation checks but skips file I/O. Returns an OutputRouterResult
        with synthetic paths for compatibility with pipeline executor.
        """
        artifacts: list[schema.RunArtifactRecord] = []
        used_filenames: set[str] = set()

        # Validate all bindings (same validation as normal mode)
        for alias, binding in exit_bindings.items():
            destination = binding.destination_filename
            if not destination:
                raise OutputRouterError(f"ExitPoint binding '{alias}' is missing a destination filename")
            if destination in used_filenames:
                raise OutputRouterError(f"Destination filename '{destination}' declared more than once")
            used_filenames.add(destination)

            type_name = binding.type_name
            if type_name is None:
                raise OutputRouterError(f"ExitPoint binding '{alias}' is missing a type declaration")

            handler = self._type_handlers.get(type_name)
            if handler is None:
                raise OutputRouterError(f"No writer registered for type '{type_name}'")
            if handler.extension and not destination.endswith(handler.extension):
                raise OutputRouterError(
                    f"Destination filename '{destination}' does not match expected extension '{handler.extension}'"
                )

            channel_name = binding.channel_name
            payload = channel_values.get(channel_name)

            # Record artifact without writing
            artifacts.append(
                schema.RunArtifactRecord(
                    channel=channel_name,
                    type_name=type_name,
                    relative_path=destination if payload is not None else None,
                    produced=payload is not None,
                )
            )

        # Create metadata payload (same as normal mode)
        metadata_payload = None
        if pipeline_metadata is not None:
            if hasattr(pipeline_metadata, "model_dump"):
                metadata_payload = pipeline_metadata.model_dump()
            elif isinstance(pipeline_metadata, Mapping):
                metadata_payload = dict(pipeline_metadata)
            else:
                raise OutputRouterError(
                    "pipeline_metadata must be a mapping or provide a model_dump() method"
                )

        # Create manifest with synthetic paths (since we didn't create directories)
        final_run_name = run_name or "in_memory_run"
        short_id = "mem"

        manifest = schema.RunManifest(
            run_name=final_run_name,
            run_directory=f"{final_run_name}-{short_id}",
            base_output_dir="<in-memory>",
            short_id=short_id,
            metadata=metadata_payload,
            artifacts=artifacts,
        )

        # Return result with synthetic paths
        synthetic_run_dir = Path("<in-memory>") / f"{final_run_name}-{short_id}"
        synthetic_manifest_path = synthetic_run_dir / "manifest.json"

        return OutputRouterResult(
            run_dir=synthetic_run_dir,
            manifest=manifest,
            manifest_path=synthetic_manifest_path,
        )

    def _prepare_run_directory(self, base_dir: Path, run_name: str) -> tuple[Path, str]:
        base_dir.mkdir(parents=True, exist_ok=True)
        short_id = uuid.uuid4().hex[:8]
        run_dir = base_dir / f"{run_name}-{short_id}"
        while run_dir.exists():  # Extremely unlikely, but rotate if collision occurs
            short_id = uuid.uuid4().hex[:8]
            run_dir = base_dir / f"{run_name}-{short_id}"
        run_dir.mkdir(parents=False, exist_ok=False)
        return run_dir, short_id


def create_default_router(*, in_memory: bool = False) -> OutputRouter:
    """Create an OutputRouter populated with default generic schema type handlers.

    Args:
        in_memory: If True, router validates but doesn't write files.
                  Default: False.

    Note:
        Domain-specific packages (e.g., battery_tea) should register their own
        type handlers via create_output_router_with_json_schemas() or by creating
        a custom OutputRouter instance.
    """
    handlers: MutableMapping[str, WriteHandler] = {
        schema.FinancialResults.__name__: WriteHandler(fn=writers.write_json_model, extension=".json"),
        schema.MockForecastSeries.__name__: WriteHandler(
            fn=writers.write_mock_forecast_series,
            extension=".json",
        ),
        schema.SyncGuidanceSeries.__name__: WriteHandler(
            fn=writers.write_sync_guidance_series,
            extension=".json",
        ),
    }
    # JSON-native scalars, both channel shapes, keyed off the shared constant so
    # the exit contract cannot drift from the entry loaders. Bare values arrive
    # from multi-output decomposition (write_json_primitive); RootModel wrappers
    # arrive from single-output modules (write_json_model). The two produce
    # byte-identical JSON for the same scalar, so on-disk output is shape-blind.
    for type_name in schema.PRIMITIVE_TYPES:
        handlers[type_name] = WriteHandler(
            fn=writers.write_json_primitive, extension=".json"
        )
        handlers[f"RootModel[{type_name}]"] = WriteHandler(
            fn=writers.write_json_model, extension=".json"
        )
    return OutputRouter(type_handlers=handlers, in_memory=in_memory)


def create_output_router_with_json_schemas(
    custom_schema_types: list[str],
    *,
    include_builtins: bool = True,
    in_memory: bool = False,
) -> OutputRouter:
    """Create OutputRouter with custom JSON-serializable schema types.

    This is a convenience function for external packages that want to register
    custom Pydantic schema types for ExitPoint persistence. All custom types
    will use the standard JSON writer. When built-ins are included, an existing
    default handler wins over a custom name collision (so a custom type named
    "float" cannot silently replace the primitive writer); use
    register_handler() for a deliberate override.

    Args:
        custom_schema_types: List of schema type names to register with JSON handlers.
                            Type names should match what appears in pipeline YAML
                            (e.g., "FusionParams", "AlphaNeutronSplitOutput").
        include_builtins: If True, includes all built-in TEAx schema handlers.
                         If False, creates router with only custom schemas.
                         Default: True (recommended for most use cases).
        in_memory: If True, router validates but doesn't write files.
                  Default: False.

    Returns:
        OutputRouter configured with requested handlers

    Raises:
        ValueError: If custom_schema_types contains duplicates

    Example:
        >>> # Register fusion schemas with built-in TEAx schemas
        >>> router = create_output_router_with_json_schemas([
        ...     "FusionParams",
        ...     "AlphaNeutronSplitOutput",
        ... ])
        >>>
        >>> # Use in pipeline
        >>> from simkit.core.pipeline import execute_pipeline
        >>> result = execute_pipeline(
        ...     "fusion_pipeline.yaml",
        ...     "outputs/",
        ...     output_router=router,
        ... )

        >>> # Custom-only (no built-ins)
        >>> router = create_output_router_with_json_schemas(
        ...     ["MySchema"],
        ...     include_builtins=False,
        ... )
    """
    # Check for duplicates
    if len(custom_schema_types) != len(set(custom_schema_types)):
        duplicates = [t for t in custom_schema_types if custom_schema_types.count(t) > 1]
        raise ValueError(
            f"Duplicate schema types in custom_schema_types: {set(duplicates)}"
        )

    # Start with builtins or empty
    if include_builtins:
        router = create_default_router(in_memory=in_memory)
    else:
        router = OutputRouter(type_handlers={}, in_memory=in_memory)

    # Register custom types with JSON handler. Defaults win: never replace a
    # handler the default router already supplied (register_handler() remains
    # the deliberate override).
    json_handler = WriteHandler(fn=writers.write_json_model, extension=".json")
    for type_name in custom_schema_types:
        if not router.has_handler(type_name):
            router.register_handler(type_name, json_handler)

    return router
