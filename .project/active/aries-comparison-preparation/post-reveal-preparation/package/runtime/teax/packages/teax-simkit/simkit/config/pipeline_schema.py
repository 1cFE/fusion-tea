"""Schema definitions for channel-based pipeline specifications."""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Set

import yaml
from pydantic import Field, field_validator, model_validator

from .schema import StrictBaseModel


class ChannelSource(str, Enum):
    """Origin of a channel binding."""

    ENTRY = "entry"
    MODULE = "module"
    DEFAULT = "default"


class PipelineChannelBinding(StrictBaseModel):
    """Represents either a provided channel or a dependency on one."""

    type_name: str | None
    channel_name: str
    field_path: str | None = None  # e.g., "blanket_config" for single-level extraction
    source: ChannelSource
    artifact_path: Path | None = None  # Note: reserved for EntryPoint module only
    destination_filename: str | None = None  # Note: reserved for ExitPoint module only

    @property
    def is_default(self) -> bool:
        return self.source is ChannelSource.DEFAULT

    @property
    def is_field_reference(self) -> bool:
        """True if this binding extracts a field from a channel."""
        return self.field_path is not None


class PipelineModuleSpec(StrictBaseModel):
    """Module declaration within a pipeline specification."""

    key: str
    module_type: str
    inputs: Dict[str, PipelineChannelBinding] = Field(default_factory=dict)
    outputs: Dict[str, PipelineChannelBinding] = Field(default_factory=dict)

    @property
    def is_entry(self) -> bool:
        return self.module_type == "EntryPoint"

    @property
    def is_exit(self) -> bool:
        return self.module_type == "ExitPoint"


class PipelineMetadata(StrictBaseModel):
    """Optional metadata about the pipeline configuration."""

    run_description: str | None = None
    output_folder: str | None = None

    @field_validator("output_folder")
    @classmethod
    def _validate_output_folder(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("output_folder must be non-empty when provided")
        return value


class PipelineSpecification(StrictBaseModel):
    """Fully parsed pipeline specification."""

    modules: Dict[str, PipelineModuleSpec]
    metadata: PipelineMetadata | None = None
    source_path: Path | None = None

    @model_validator(mode="after")
    def _validate_graph(self) -> "PipelineSpecification":
        entries = [m for m in self.modules.values() if m.is_entry]
        exits = [m for m in self.modules.values() if m.is_exit]
        if len(entries) != 1:
            raise ValueError("Pipeline must declare exactly one EntryPoint module")
        if len(exits) != 1:
            raise ValueError("Pipeline must declare exactly one ExitPoint module")

        provided_channels: Dict[str, str] = {}
        for module in self.modules.values():
            if module.is_exit:
                continue
            for binding in module.outputs.values():
                owner = provided_channels.get(binding.channel_name)
                if owner is None:
                    provided_channels[binding.channel_name] = module.key
                elif owner == module.key:
                    raise ValueError(
                        f"Module {module.key!r} declares channel '{binding.channel_name}' more than once"
                    )
                else:
                    raise ValueError(
                        f"Channel '{binding.channel_name}' is provided by multiple modules: "
                        f"{owner!r} and {module.key!r}"
                    )

        exit_module = exits[0]
        for field, binding in exit_module.outputs.items():
            if binding.channel_name not in provided_channels:
                raise ValueError(
                    f"ExitPoint module '{exit_module.key}' references unknown channel '{binding.channel_name}'"
                )

        allowed_defaults = _collect_entry_defaults(entries[0])
        for module in self.modules.values():
            if module.is_entry:
                continue
            for binding in module.inputs.values():
                if binding.is_default:
                    continue
                if binding.artifact_path is not None:
                    # Only the entry module may reference filesystem artifacts.
                    raise ValueError(
                        f"Module {module.key!r} input '{binding.channel_name}' unexpectedly references a file"
                    )
                if binding.channel_name in allowed_defaults:
                    continue
                if binding.channel_name not in provided_channels:
                    raise ValueError(
                        f"Module {module.key!r} requires unknown channel '{binding.channel_name}'"
                    )
        return self


def _collect_entry_defaults(entry: PipelineModuleSpec) -> Iterable[str]:
    return [name for name, binding in entry.outputs.items() if binding.source is ChannelSource.ENTRY]


class PipelineSpecLoader:
    """Parses YAML pipeline specifications into structured models."""

    def load(self, config_path: str | Path) -> PipelineSpecification:
        path = Path(config_path)
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("Pipeline specification must be a mapping")
        return build_pipeline_spec(raw, source_path=path)


def build_pipeline_spec(raw: Dict[str, Any], *, source_path: Path | None = None) -> PipelineSpecification:
    modules_section = raw.get("modules")
    if not isinstance(modules_section, dict):
        raise ValueError("Pipeline specification must include a 'modules' mapping")

    modules: Dict[str, PipelineModuleSpec] = {}
    for module_key, module_data in modules_section.items():
        modules[module_key] = _parse_module(module_key, module_data)

    metadata_obj: PipelineMetadata | None = None
    metadata_section = raw.get("metadata")
    if isinstance(metadata_section, dict):
        metadata_obj = PipelineMetadata(**metadata_section)

    return PipelineSpecification(modules=modules, metadata=metadata_obj, source_path=source_path)


def _parse_module(module_key: str, module_data: Any) -> PipelineModuleSpec:
    if not isinstance(module_data, dict):
        raise ValueError(f"Module '{module_key}' must be defined as a mapping")

    module_type = module_data.get("module_type")
    if not isinstance(module_type, str) or not module_type:
        raise ValueError(f"Module '{module_key}' must declare a non-empty module_type")

    raw_inputs = module_data.get("inputs") or {}
    raw_outputs = module_data.get("outputs") or {}
    if not isinstance(raw_inputs, dict):
        raise ValueError(f"Module '{module_key}' inputs must be a mapping")
    if not isinstance(raw_outputs, dict):
        raise ValueError(f"Module '{module_key}' outputs must be a mapping if provided")

    if module_type == "EntryPoint":
        inputs, outputs = _parse_entry_module(module_key, raw_inputs, raw_outputs)
    elif module_type == "ExitPoint":
        inputs = _parse_inputs(raw_inputs)  # NOTE: has no effect, should be empty
        outputs = _parse_exit_outputs(module_key, raw_outputs)
    else:
        inputs = _parse_inputs(raw_inputs)
        outputs = _parse_outputs(module_key, raw_outputs)

    return PipelineModuleSpec(
        key=module_key,
        module_type=module_type,
        inputs=inputs,
        outputs=outputs,
    )


def _parse_entry_module(
    module_key: str,
    raw_inputs: Dict[str, Any],
    raw_outputs: Dict[str, Any],
) -> tuple[Dict[str, PipelineChannelBinding], Dict[str, PipelineChannelBinding]]:
    inputs: Dict[str, PipelineChannelBinding] = {}
    outputs: Dict[str, PipelineChannelBinding] = {}

    for field, raw_value in raw_inputs.items():
        if not isinstance(raw_value, str):
            raise ValueError(
                f"EntryPoint input '{field}' must be specified as '<Type> <path>'"
            )
        parts = raw_value.strip().split(" ", 1)
        if len(parts) != 2:
            raise ValueError(
                f"EntryPoint input '{field}' must be formatted as '<Type> <path>'"
            )
        type_name, artifact = parts
        artifact_path = Path(artifact.strip())
        binding = PipelineChannelBinding(
            type_name=type_name.strip(),
            channel_name=field,
            source=ChannelSource.ENTRY,
            artifact_path=artifact_path,
        )
        inputs[field] = binding
        outputs[field] = PipelineChannelBinding(
            type_name=type_name.strip(),
            channel_name=field,
            source=ChannelSource.ENTRY,
            artifact_path=artifact_path,
        )

    if raw_outputs:
        explicit_outputs = _parse_outputs(module_key, raw_outputs)
        outputs.update(explicit_outputs)

    return inputs, outputs


def _parse_inputs(raw_inputs: Dict[str, Any]) -> Dict[str, PipelineChannelBinding]:
    """Parse input bindings from YAML, supporting field references like 'Type channel.field'."""
    bindings: Dict[str, PipelineChannelBinding] = {}
    for field, raw_value in raw_inputs.items():
        if not isinstance(raw_value, str):
            raise ValueError(
                f"Input '{field}' must be a string formatted as '<Type> <channel>' or 'None -> <channel>'"
            )
        value = raw_value.strip()

        # Handle default bindings (UNCHANGED)
        if value.lower().startswith("none"):
            channel_name = _parse_default_channel(value, field)
            binding = PipelineChannelBinding(
                type_name=None,
                channel_name=channel_name,
                source=ChannelSource.DEFAULT,
            )
        else:
            # Split on whitespace: "<Type> <channel_ref>"
            parts = value.split(None, 1)
            if len(parts) != 2:
                raise ValueError(
                    f"Input '{field}' must be formatted as '<Type> <channel>' or '<Type> <channel.field>'"
                )

            type_name, channel_ref = parts

            # NEW: Check for field reference (contains dot)
            if "." in channel_ref:
                # Split on first dot only
                dot_index = channel_ref.index(".")
                channel_name = channel_ref[:dot_index].strip()
                field_path = channel_ref[dot_index + 1:].strip()

                # Phase 1: Reject nested field paths
                if "." in field_path:
                    raise ValueError(
                        f"Input '{field}': Nested field paths not supported in Phase 1 "
                        f"(got '{channel_ref}'). Use single-level fields only (e.g., 'channel.field')."
                    )

                # Validate field_path is not empty
                if not field_path:
                    raise ValueError(
                        f"Input '{field}': Field path cannot be empty (got '{channel_ref}')"
                    )

                binding = PipelineChannelBinding(
                    type_name=type_name.strip(),
                    channel_name=channel_name,
                    field_path=field_path,
                    source=ChannelSource.MODULE,
                )
            else:
                # Standard channel binding (no field reference) - UNCHANGED
                binding = PipelineChannelBinding(
                    type_name=type_name.strip(),
                    channel_name=channel_ref.strip(),
                    source=ChannelSource.MODULE,
                )

        bindings[field] = binding
    return bindings


def _parse_outputs(module_key: str, raw_outputs: Dict[str, Any]) -> Dict[str, PipelineChannelBinding]:
    bindings: Dict[str, PipelineChannelBinding] = {}
    for field, raw_value in raw_outputs.items():
        if not isinstance(raw_value, str):
            raise ValueError(
                f"Output '{field}' in module '{module_key}' must be a string formatted as '<Type> <channel>'"
            )
        value = raw_value.strip()
        if value.lower().startswith("none"):
            raise ValueError(
                f"Output '{field}' in module '{module_key}' cannot be a default sentinel"
            )
        parts = value.split(None, 1)
        if len(parts) != 2:
            raise ValueError(
                f"Output '{field}' in module '{module_key}' must be formatted as '<Type> <channel>'"
            )
        type_name, channel_name = parts
        bindings[field] = PipelineChannelBinding(
            type_name=type_name.strip(),
            channel_name=channel_name.strip(),
            source=ChannelSource.MODULE,
        )
    return bindings


def _parse_exit_outputs(
    module_key: str,
    raw_outputs: Dict[str, Any],
) -> Dict[str, PipelineChannelBinding]:
    bindings: Dict[str, PipelineChannelBinding] = {}
    filenames: Set[str] = set()
    for field, raw_value in raw_outputs.items():
        if not isinstance(raw_value, str):
            raise ValueError(
                f"Output '{field}' in module '{module_key}' must be formatted as '<Type> <filename>'"
            )
        value = raw_value.strip()
        if value.lower().startswith("none"):
            raise ValueError(
                f"Output '{field}' in module '{module_key}' cannot be a default sentinel"
            )
        parts = value.split(None, 1)
        if len(parts) != 2:
            raise ValueError(
                f"Output '{field}' in module '{module_key}' must be formatted as '<Type> <filename>'"
            )
        type_name, filename = parts
        filename = filename.strip()
        if not filename:
            raise ValueError(
                f"Output '{field}' in module '{module_key}' must be formatted as '<Type> <filename>'"
            )
        if "/" in filename or "\\" in filename:
            raise ValueError(
                f"Output '{field}' in module '{module_key}' must use a filename without directories"
            )
        if filename in filenames:
            raise ValueError(
                f"ExitPoint module '{module_key}' declares duplicate destination filename '{filename}'"
            )
        filenames.add(filename)
        bindings[field] = PipelineChannelBinding(
            type_name=type_name.strip(),
            channel_name=field,
            source=ChannelSource.MODULE,
            destination_filename=filename,
        )
    return bindings


def _parse_default_channel(value: str, field: str) -> str:
    marker = "->"
    if marker not in value:
        raise ValueError(
            f"Default binding for input '{field}' must follow 'None -> <channel>'"
        )
    _, channel = value.split(marker, 1)
    channel_name = channel.strip()
    if not channel_name:
        raise ValueError(
            f"Default binding for input '{field}' must specify a channel name after '->'"
        )
    return channel_name
