"""Validation utilities tying pipeline specs to registry metadata."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict

from ..config import schema
from ..config.pipeline_schema import (
    ChannelSource,
    PipelineChannelBinding,
    PipelineModuleSpec,
    PipelineSpecification,
)
from .pipeline_graph import PipelineDagBuilder, PipelineGraph, PipelineGraphError
from .pipeline_registry import ModuleDescriptor, PipelineModuleRegistry

if TYPE_CHECKING:
    from ..io.output_router import OutputRouter


class PipelineValidationError(Exception):
    """Raised when a pipeline specification fails validation."""

    def __init__(self, message: str, module: str | None = None, details: Dict[str, object] | None = None):
        super().__init__(message)
        self.module = module
        self.details = details or {}


@dataclass
class _ValidationContext:
    registry: PipelineModuleRegistry


class PipelineValidator:
    """Validates a pipeline specification against the module registry."""

    def __init__(
        self,
        registry: PipelineModuleRegistry,
        output_router: OutputRouter,
        schema_type_registry: dict[str, type] | None = None,
    ) -> None:
        """Initialize validator with module registry and optional schema type registry.

        Args:
            registry: Module registry for validation
            output_router: Output router for exit point validation
            schema_type_registry: Optional mapping of schema type names to type objects.
                                Used for resolving EntryPoint output types during field
                                reference validation. If None, uses built-in simkit.config.schema
                                types only.
        """
        self._registry = registry
        self._output_router = output_router
        self._schema_type_registry = schema_type_registry
        self._builder = PipelineDagBuilder()

    def validate(self, spec: PipelineSpecification) -> PipelineGraph:
        self._assert_entry_exit(spec)

        # NEW: Build channel type map for field reference validation
        channel_types = self._build_channel_type_map(spec)

        for module in spec.modules.values():
            if module.is_entry:
                continue
            if module.is_exit:
                self._validate_exit_module(module, channel_types)
                continue
            descriptor = self._resolve_descriptor(module)
            self._validate_outputs(module, descriptor)  # Make sure 1:1 mapping for output fields and types between registry and yaml
            self._validate_inputs(module, descriptor, channel_types)  # NEW: pass channel_types
        try:
            graph = self._builder.build(spec)
        except PipelineGraphError as exc:
            raise PipelineValidationError(str(exc)) from exc
        return graph

    def _assert_entry_exit(self, spec: PipelineSpecification) -> None:
        entries = [m for m in spec.modules.values() if m.is_entry]
        exits = [m for m in spec.modules.values() if m.is_exit]
        if len(entries) != 1:
            raise PipelineValidationError(
                f"Expected exactly one EntryPoint module, found {len(entries)}",
                details={"entries": [m.key for m in entries]},
            )
        if len(exits) != 1:
            raise PipelineValidationError(
                f"Expected exactly one ExitPoint module, found {len(exits)}",
                details={"exits": [m.key for m in exits]},
            )

    def _build_channel_type_map(
        self,
        spec: PipelineSpecification,
    ) -> Dict[str, type]:
        """
        Build a mapping of channel names to their type objects.

        Used for field reference validation to determine parent channel types.
        Iterates through all non-exit modules and records their output channel types.

        Args:
            spec: The pipeline specification

        Returns:
            Dict mapping channel_name -> type object
        """
        channel_types: Dict[str, type] = {}

        for module_key, module_spec in spec.modules.items():
            if module_spec.is_exit:
                continue

            if module_spec.is_entry:
                # Entry module: types come from artifact bindings (resolve from registry)
                for binding in module_spec.outputs.values():
                    if binding.type_name is not None:
                        type_obj = None

                        if self._schema_type_registry is not None:
                            # Use custom schema registry
                            type_obj = self._schema_type_registry.get(binding.type_name)
                            if type_obj is None:
                                # Not in registry - will error later if used in field reference
                                continue
                        else:
                            # Backward compatibility: fall back to built-in schema module
                            type_obj = getattr(schema, binding.type_name, None)
                            if type_obj is None:
                                # Check primitive types (lazy import avoids circular dependency)
                                from .pipeline_executor import _PRIMITIVE_TYPES
                                type_obj = _PRIMITIVE_TYPES.get(binding.type_name)
                            if type_obj is None:
                                # Type not found anywhere - skip (will error later if needed)
                                continue

                        channel_types[binding.channel_name] = type_obj
                continue

            # Regular module: get types from registry descriptor
            try:
                descriptor = self._registry.get(module_spec.module_type)
            except KeyError:
                raise PipelineValidationError(
                    f"Module type '{module_spec.module_type}' is not registered",
                    module=module_key,
                    details={"module_type": module_spec.module_type},
                )

            for field, binding in module_spec.outputs.items():
                # Get expected type from descriptor
                expected_type = descriptor.outputs.get(field)
                if expected_type is not None:
                    channel_types[binding.channel_name] = expected_type

        return channel_types

    def _unwrap_optional(self, type_annotation) -> type:
        """
        Unwrap Optional[T] to T. Returns original type if not Optional.

        Handles Python 3.10+ union syntax and typing.Optional:
        - Optional[BlanketConfig] → BlanketConfig
        - BlanketConfig | None → BlanketConfig
        - BlanketConfig → BlanketConfig (unchanged)

        Args:
            type_annotation: Type annotation to unwrap

        Returns:
            The unwrapped type (T) or original if not Optional
        """
        import typing
        import types

        # Handle both typing.Union and types.UnionType (Python 3.10+)
        is_union = False
        if hasattr(type_annotation, "__origin__") and type_annotation.__origin__ is typing.Union:
            is_union = True
        elif isinstance(type_annotation, types.UnionType):
            is_union = True

        if is_union:
            args = type_annotation.__args__
            # Remove None from union args
            non_none_args = [arg for arg in args if arg is not type(None)]
            if len(non_none_args) == 1:
                return non_none_args[0]

        return type_annotation

    def _validate_field_reference(
        self,
        binding: PipelineChannelBinding,
        parent_channel_type: type,
        expected_type: type,
        module_key: str,
        field_name: str,
    ) -> None:
        """
        Validate that a field reference binding is well-formed.

        Performs comprehensive validation:
        1. Field exists in parent type
        2. Field is not private (no leading underscore)
        3. Field is not computed (Phase 1 restriction)
        4. Field type matches expected binding type (exact match)

        Args:
            binding: The binding with field_path set
            parent_channel_type: The type object of the parent channel
            expected_type: The expected type for the field
            module_key: Module key for error messages
            field_name: Input field name for error messages

        Raises:
            PipelineValidationError: If any validation check fails
        """
        parent_type_name = parent_channel_type.__name__

        # 1. Check field is not private (before checking existence)
        if binding.field_path.startswith("_"):
            raise PipelineValidationError(
                f"Module '{module_key}' input '{field_name}': "
                f"Cannot extract private field '{binding.field_path}' from channel '{binding.channel_name}'",
                module=module_key,
            )

        # 2. Phase 1: Check if field is computed (before checking model_fields)
        if binding.field_path in parent_channel_type.model_computed_fields:
            raise PipelineValidationError(
                f"Module '{module_key}' input '{field_name}': "
                f"Cannot extract computed field '{binding.field_path}' (not supported in Phase 1)",
                module=module_key,
            )

        # 3. Check field exists in parent type
        if binding.field_path not in parent_channel_type.model_fields:
            available_fields = ", ".join(sorted(parent_channel_type.model_fields.keys()))
            raise PipelineValidationError(
                f"Module '{module_key}' input '{field_name}': "
                f"Type '{parent_type_name}' has no field '{binding.field_path}'. "
                f"Available fields: {available_fields}",
                module=module_key,
                details={
                    "channel": binding.channel_name,
                    "parent_type": parent_type_name,
                    "field_path": binding.field_path,
                    "available_fields": list(parent_channel_type.model_fields.keys()),
                },
            )

        # 4. Get actual field type
        field_info = parent_channel_type.model_fields[binding.field_path]
        actual_type_annotation = field_info.annotation

        # Unwrap Optional if present
        actual_type = self._unwrap_optional(actual_type_annotation)
        is_optional = actual_type != actual_type_annotation

        # 5. Check type compatibility (exact match in Phase 1)
        if actual_type != expected_type:
            # Get type name for error message
            actual_type_name = getattr(actual_type, "__name__", str(actual_type))
            raise PipelineValidationError(
                f"Module '{module_key}' input '{field_name}': "
                f"Type mismatch for field '{binding.channel_name}.{binding.field_path}'. "
                f"Expected type '{expected_type.__name__}', but field has type '{actual_type_name}'",
                module=module_key,
                details={
                    "expected_type": expected_type.__name__,
                    "actual_type": actual_type_name,
                    "is_optional": is_optional,
                },
            )

    def _resolve_descriptor(self, module: PipelineModuleSpec) -> ModuleDescriptor:
        module_type = module.module_type
        if not self._registry.has(module_type):
            raise PipelineValidationError(
                f"Module type '{module_type}' is not registered",
                module=module.key,
            )
        return self._registry.get(module_type)

    def _validate_exit_module(
        self,
        module: PipelineModuleSpec,
        channel_types: Dict[str, type],
    ) -> None:
        if not module.outputs:
            raise PipelineValidationError(
                "ExitPoint module must declare at least one output",
                module=module.key,
            )
        seen_filenames: set[str] = set()
        for field, binding in module.outputs.items():
            if binding.destination_filename is None:
                raise PipelineValidationError(
                    "ExitPoint output bindings must declare destination filenames",
                    module=module.key,
                    details={"output": field},
                )
            if binding.channel_name != field:
                raise PipelineValidationError(
                    "ExitPoint output channel names must match their binding keys",
                    module=module.key,
                    details={"output": field, "channel": binding.channel_name},
                )
            if binding.destination_filename in seen_filenames:
                raise PipelineValidationError(
                    "ExitPoint outputs declare duplicate destination filenames",
                    module=module.key,
                    details={"filename": binding.destination_filename},
                )
            seen_filenames.add(binding.destination_filename)
            type_name = binding.type_name
            if type_name is None:
                raise PipelineValidationError(
                    "ExitPoint outputs must declare a type",
                    module=module.key,
                    details={"output": field},
                )
            if not self._output_router.has_handler(type_name):
                raise PipelineValidationError(
                    "ExitPoint output type has no registered write handler",
                    module=module.key,
                    details={
                        "output": field,
                        "type": type_name,
                        "hint": "Register a handler with output_router.register_handler() or use create_output_router_with_json_schemas()"
                    },
                )
            # Cross-check the declared type against the producer channel's real
            # type. With scalar handlers registered a mislabeled binding would
            # otherwise write a falsely labelled manifest instead of failing.
            # Channels whose producer type is unresolvable are skipped, not
            # guessed.
            producer_type = channel_types.get(binding.channel_name)
            if producer_type is None:
                continue
            resolved_producer_type = self._unwrap_optional(producer_type)
            producer_type_name = getattr(resolved_producer_type, "__name__", None)
            if not isinstance(producer_type_name, str):
                continue
            self._validate_exit_output_type(
                module.key,
                field,
                binding,
                producer_type_name,
            )

    def _validate_exit_output_type(
        self,
        module_key: str,
        field: str,
        binding: PipelineChannelBinding,
        producer_type_name: str,
    ) -> None:
        """Reject an ExitPoint declaration that conflicts with its producer type name."""
        if binding.type_name == producer_type_name:
            return

        raise PipelineValidationError(
            "ExitPoint output type does not match producer channel type",
            module=module_key,
            details={
                "output": field,
                "declared_type": binding.type_name,
                "producer_type": producer_type_name,
                "hint": (
                    f"Declare the output as '{producer_type_name}' to match "
                    f"channel '{binding.channel_name}'"
                ),
            },
        )

    def _validate_outputs(self, module: PipelineModuleSpec, descriptor: ModuleDescriptor) -> None:
        expected = set(descriptor.outputs.keys())
        actual = set(module.outputs.keys())
        if expected != actual:
            raise PipelineValidationError(
                "Output bindings do not match registry metadata",
                module=module.key,
                details={"expected": sorted(expected), "actual": sorted(actual)},
            )
        for field, binding in module.outputs.items():
            expected_type = descriptor.outputs[field]
            self._assert_type(binding, expected_type, module.key, field, "output")

    def _validate_inputs(
        self,
        module: PipelineModuleSpec,
        descriptor: ModuleDescriptor,
        channel_types: Dict[str, type],  # NEW parameter
    ) -> None:
        """Validate module inputs against descriptor metadata."""
        expected_inputs = set(descriptor.required_inputs) | set(descriptor.optional_inputs)
        actual_inputs = set(module.inputs.keys())
        missing_required = set(descriptor.required_inputs) - actual_inputs
        if missing_required:
            raise PipelineValidationError(
                "Missing required input bindings",
                module=module.key,
                details={"missing": sorted(missing_required)},
            )
        missing_optional = set(descriptor.optional_inputs) - actual_inputs
        if missing_optional:
            raise PipelineValidationError(
                "Optional inputs must be explicitly bound or defaulted",
                module=module.key,
                details={"missing_optional": sorted(missing_optional)},
            )

        unknown_inputs = actual_inputs - expected_inputs
        if unknown_inputs:
            raise PipelineValidationError(
                "Specification declares inputs not defined by registry",
                module=module.key,
                details={"unknown": sorted(unknown_inputs)},
            )

        for field, binding in module.inputs.items():
            expected_type = (
                descriptor.required_inputs.get(field)
                or descriptor.optional_inputs.get(field)
            )
            if expected_type is None:
                continue  # already handled unknown inputs
            if binding.source is ChannelSource.DEFAULT:
                if field not in descriptor.optional_inputs:
                    raise PipelineValidationError(
                        "Default binding supplied for a required input",
                        module=module.key,
                        details={"input": field},
                    )
            else:
                # NEW: Validate field references
                if binding.is_field_reference:
                    parent_type = channel_types.get(binding.channel_name)
                    if parent_type is None:
                        raise PipelineValidationError(
                            f"Module '{module.key}' input '{field}': "
                            f"Cannot resolve type for channel '{binding.channel_name}' "
                            f"(required for field reference validation)",
                            module=module.key,
                        )
                    self._validate_field_reference(
                        binding=binding,
                        parent_channel_type=parent_type,
                        expected_type=expected_type,
                        module_key=module.key,
                        field_name=field,
                    )

                # Standard type check (existing logic - UNCHANGED)
                self._assert_type(binding, expected_type, module.key, field, "input")

    def _assert_type(
        self,
        binding: PipelineChannelBinding,
        expected_type: type[schema.StrictBaseModel],
        module_key: str,
        field: str,
        binding_kind: str,
    ) -> None:
        if binding.type_name is None:
            return
        expected_name = expected_type.__name__
        if binding.type_name != expected_name:
            raise PipelineValidationError(
                f"{binding_kind.capitalize()} '{field}' expects type {expected_name}, "
                f"but binding declares {binding.type_name}",
                module=module_key,
                details={"field": field, "expected": expected_name, "declared": binding.type_name},
            )
