"""Async demo pipeline orchestrating module execution."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Mapping

from dataclasses import replace

from ..config import schema
from ..config.pipeline_schema import PipelineSpecification
from ..io import readers
from ..io.output_router import create_default_router, create_output_router_with_json_schemas
from .pipeline_executor import (
    PipelineExecutionContext,
    RunResult,
    SerialPipelineExecutor,
    _build_schema_type_registry,
    _build_entry_loaders,
)
from .pipeline_registry import PipelineModuleRegistry
from .pipeline_validator import PipelineValidationError

if TYPE_CHECKING:
    from ..io.output_router import OutputRouter

def _config_hash(payload: Dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def entry_point_validate(spec_path: str | Path) -> PipelineSpecification:
    """Normalize and load the pipeline specification."""

    resolved = Path(spec_path).expanduser()
    if resolved.is_dir():
        raise ValueError("Pipeline specification path must point to a file")
    if not resolved.exists():
        raise FileNotFoundError(f"Pipeline specification missing: {resolved}")
    specification = readers.read_pipeline_spec(resolved)
    if specification.source_path is None:
        specification = specification.model_copy(update={"source_path": resolved})
    return specification


def _build_pipeline_metadata(specification: PipelineSpecification) -> schema.PipelineRunMetadata:
    spec_metadata = specification.metadata
    spec_path_str = str(specification.source_path) if specification.source_path else ""
    return schema.PipelineRunMetadata(
        spec_path=spec_path_str,
        run_description=spec_metadata.run_description if spec_metadata else None,
        output_folder=spec_metadata.output_folder if spec_metadata else None,
    )


def _build_provenance(
    specification: PipelineSpecification,
    module_versions: Mapping[str, str],
    run_metadata: schema.PipelineRunMetadata,
) -> schema.Provenance:
    config_payload = specification.model_dump(mode="json")
    return schema.Provenance(
        config_hash=_config_hash(config_payload),
        module_versions=dict(module_versions),
        notes=run_metadata.run_description or "Async demo pipeline v0.1",
        output_folder=run_metadata.output_folder,
    )


def execute_pipeline(
    spec_path: str | Path,
    output_dir: str | Path | None = None,
    registry: PipelineModuleRegistry | None = None,
    output_router: OutputRouter | None = None,
    custom_schema_types: list[type] | None = None,
) -> RunResult:
    """Execute pipeline with optional custom module registry and schema types.

    Args:
        spec_path: Path to pipeline YAML specification
        output_dir: Optional output directory (defaults to temp dir)
        registry: Module registry for pipeline execution. Required for most pipelines.
                 Domain packages provide registry factory functions (e.g., battery_tea.create_battery_registry()).
        output_router: Optional custom output router. If None and custom_schema_types
                      provided, auto-creates router with custom types registered for
                      JSON serialization. If both None, uses default router with
                      built-in schemas only. If output_router provided explicitly,
                      custom_schema_types only affects EntryPoint loading and
                      validation (not ExitPoint writing).
        custom_schema_types: Optional list of custom Pydantic schema type classes.
                           Enables three features for custom schemas:
                           1. EntryPoint artifact loading (auto-registers JSON loaders)
                           2. Field reference validation (resolves types in validator)
                           3. ExitPoint output writing (auto-creates OutputRouter unless
                              explicit router provided)

                           All custom types default to JSON serialization. For schemas
                           requiring special loaders (Parquet, custom parsing), future
                           enhancement will add custom_entry_loaders parameter.

                           Example:
                               from custom_pkg.schemas import FusionParams, PlasmaParams

                               result = execute_pipeline(
                                   "pipeline.yaml",
                                   "outputs/",
                                   custom_schema_types=[FusionParams, PlasmaParams],
                               )

    Returns:
        RunResult with execution outputs, metadata, and provenance

    Raises:
        TypeError: If custom_schema_types contains non-BaseModel types
        ValueError: If duplicate type names in custom_schema_types
        PipelineValidationError: If pipeline spec invalid
        RuntimeError: If execution fails

    Example:
        >>> # Execute with built-in modules and schemas (backward compatible)
        >>> result = execute_pipeline("demo_pipeline.yaml", "outputs/")

        >>> # Execute with custom modules and schemas
        >>> from simkit.core.registry_builder import create_registry
        >>> from custom_pkg import CustomModule
        >>> from custom_pkg.schemas import CustomSchema
        >>>
        >>> registry = create_registry([CustomModule])
        >>> result = execute_pipeline(
        ...     "custom_pipeline.yaml",
        ...     "outputs/",
        ...     registry=registry,
        ...     custom_schema_types=[CustomSchema],
        ... )
    """
    specification = entry_point_validate(spec_path)

    # Build schema registries from custom types (if provided)
    schema_type_registry = None
    entry_loaders = None

    if custom_schema_types is not None:
        # Validate and build registries
        # Note: _build_schema_type_registry performs type validation,
        # so this will raise TypeError early if invalid types provided
        schema_type_registry = _build_schema_type_registry(custom_schema_types)
        entry_loaders = _build_entry_loaders(custom_schema_types)

    # Use custom registry if provided, otherwise create empty registry
    # (most pipelines require a registry - domain packages provide these)
    if registry is None:
        registry = PipelineModuleRegistry()

    # Use custom router if provided, otherwise auto-create from custom_schema_types
    if output_router is None:
        if custom_schema_types is not None:
            # Auto-create router with custom types + built-ins
            type_name_strings = [t.__name__ for t in custom_schema_types]
            router = create_output_router_with_json_schemas(
                type_name_strings,
                include_builtins=True,
            )
        else:
            # No custom types, use default built-in router
            router = create_default_router()
    else:
        # User provided explicit router, use as-is
        # Note: custom_schema_types will still affect EntryPoint/validation
        router = output_router

    executor = SerialPipelineExecutor(
        registry,
        output_router=router,
        schema_type_registry=schema_type_registry,
        entry_loaders=entry_loaders,
    )
    context = PipelineExecutionContext(registry)

    graph = executor.build_graph(specification)
    try:
        metadata = specification.metadata
        run_name_hint = None
        if metadata and metadata.output_folder:
            run_name_hint = metadata.output_folder
        elif metadata and metadata.run_description:
            run_name_hint = metadata.run_description
        elif specification.source_path is not None:
            run_name_hint = specification.source_path.stem

        base_output_dir = Path(output_dir) if output_dir is not None else None

        run_result = executor.run(
            graph,
            context,
            base_output_dir=base_output_dir,
            run_name=run_name_hint,
            pipeline_metadata=metadata,
        )
        produced_outputs = run_result.outputs
    except PipelineValidationError as exc:  # pragma: no cover
        raise RuntimeError(f"Pipeline execution failed: {exc}") from exc

    # TODO: I think we may want to just have the entire spec somewhere here
    pipeline_metadata = _build_pipeline_metadata(specification)
    provenance = _build_provenance(specification, run_result.module_versions, pipeline_metadata)
    # Also may want to dump these json files to the output directory as well
    return replace(
        run_result,
        pipeline_metadata=pipeline_metadata,
        provenance=provenance,
    )
