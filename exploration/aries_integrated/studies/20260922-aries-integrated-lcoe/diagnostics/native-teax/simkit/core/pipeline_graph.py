"""Graph utilities for channel-driven pipelines."""
from __future__ import annotations

from dataclasses import dataclass
from graphlib import CycleError, TopologicalSorter
from typing import Dict, Iterable, Mapping, Set

from ..config.pipeline_schema import ChannelSource, PipelineSpecification


@dataclass(frozen=True)
class PipelineGraph:
    """In-memory representation of a validated pipeline DAG."""

    spec: PipelineSpecification
    dependencies: Mapping[str, Set[str]]
    adjacency: Mapping[str, Set[str]]
    channel_providers: Mapping[str, str]
    topological_order: Iterable[str]


class PipelineGraphError(Exception):
    """Raised when a pipeline graph cannot be constructed."""


class PipelineDagBuilder:
    """Constructs a DAG from a pipeline specification."""

    def build(self, spec: PipelineSpecification) -> PipelineGraph:
        modules = spec.modules
        dependencies: Dict[str, Set[str]] = {key: set() for key in modules}
        adjacency: Dict[str, Set[str]] = {key: set() for key in modules}
        channel_providers: Dict[str, str] = {}  # Channel name -> module providing
        missing_channels: list[tuple[str, str]] = []

        for module in modules.values():
            if module.is_exit:
                continue
            for binding in module.outputs.values():
                channel_providers[binding.channel_name] = module.key

        exit_modules = [module for module in modules.values() if module.is_exit]

        for module in modules.values():
            for binding in module.inputs.values():
                if binding.source is ChannelSource.DEFAULT:
                    continue  # Explicit use default (i.e. input None)
                provider = channel_providers.get(binding.channel_name)
                if provider is None:
                    missing_channels.append((module.key, binding.channel_name))
                    continue
                if provider == module.key:
                    if module.is_entry:
                        continue
                    raise PipelineGraphError(
                        f"Module {module.key!r} cannot consume its own channel '{binding.channel_name}'"
                    )
                dependencies[module.key].add(provider)
                adjacency[provider].add(module.key)

        for module in exit_modules:
            for binding in module.outputs.values():
                provider = channel_providers.get(binding.channel_name)
                if provider is None:
                    missing_channels.append((module.key, binding.channel_name))
                    continue
                dependencies[module.key].add(provider)
                adjacency[provider].add(module.key)

        if missing_channels:
            formatted = ", ".join(
                f"{module}:{channel}" for module, channel in missing_channels
            )
            raise PipelineGraphError(f"Unresolved channels detected: {formatted}")

        topo_input = {node: dependencies[node] for node in modules}
        sorter = TopologicalSorter(topo_input)
        try:
            order = tuple(sorter.static_order())
        except CycleError as exc:  # pragma: no cover - exercised via validator tests
            raise PipelineGraphError(f"Pipeline contains a cycle: {exc}") from exc

        return PipelineGraph(
            spec=spec,
            dependencies=dependencies,
            adjacency=adjacency,
            channel_providers=channel_providers,
            topological_order=order,
        )
