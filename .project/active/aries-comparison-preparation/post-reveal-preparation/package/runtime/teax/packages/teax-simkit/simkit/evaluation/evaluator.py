"""Evaluator: prepare once, evaluate per case (touches the generated package — D2)."""
from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Any, Mapping, NoReturn, Protocol

from pydantic import BaseModel

from ..core.pipeline import (
    _build_entry_loaders,
    _build_schema_type_registry,
    entry_point_validate,
)
from ..core.pipeline_executor import PipelineExecutionContext, SerialPipelineExecutor
from ..io.output_router import create_output_router_with_json_schemas

from .entry_source import MappingEntrySource
from .evidence import EvidenceProvenance, ModelEvidence
from .failure import EvaluationFailed, EvaluationFailure, EvaluationPhase
from .package_load import PackageLoader
from .projection import REPORT_CHANNEL, project


class Evaluator(Protocol):
    def evaluate(self, typed_inputs: Mapping[str, BaseModel]) -> ModelEvidence: ...


def _json_safe(value: Any) -> Any:
    """Non-finite floats -> a stable tag; everything else passes through.

    Digest-input only (design.md#implementation-notes) — never the on-disk
    evidence encoding.
    """
    if isinstance(value, float) and not math.isfinite(value):
        tag = "nan" if math.isnan(value) else ("inf" if value > 0 else "-inf")
        return {"__nonfinite__": tag}
    if isinstance(value, dict):
        return {key: _json_safe(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_json_safe(val) for val in value]
    return value


def _input_digest(typed_inputs: Mapping[str, BaseModel]) -> str:
    payload = {channel: _json_safe(model.model_dump(mode="json")) for channel, model in typed_inputs.items()}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _normalize_run_failure(
    error: Exception, context: PipelineExecutionContext
) -> NoReturn:
    """Raise the evaluator's fixed run-failure record from the original error.

    The phase is read from a **positive** write-phase signal set at the executor
    seam (``context.in_output_write``, C1) — never inferred from the exception
    type or a null module key. An entry-load or module failure keeps
    ``MODULE_EXECUTION``; only a failure raised while genuinely inside output
    write is stamped ``OUTPUT_WRITE``.
    """
    phase = (
        EvaluationPhase.OUTPUT_WRITE
        if getattr(context, "in_output_write", False)
        else EvaluationPhase.MODULE_EXECUTION
    )
    raise EvaluationFailed(
        EvaluationFailure(
            phase=phase,
            module_or_channel=context.failed_module_key,
            cause=f"{type(error).__name__}: {error}",
        )
    ) from error


def _entry_artifact_path(spec: Any, spec_path: Path, work_dir: Path) -> Path:
    """The on-disk entry-artifact path the file-backed route writes the candidate
    to, derived from the spec's single entry binding (relative to the spec) — not
    a hardcoded fixture filename. Falls back to the legacy path when the spec has
    no single entry binding (e.g. multi-group), which was the prior behavior."""
    entry_spec = next((m for m in spec.modules.values() if m.is_entry), None)
    bindings = list(entry_spec.outputs.values()) if entry_spec is not None else []
    if len(bindings) == 1 and bindings[0].artifact_path is not None:
        return (spec_path.parent / bindings[0].artifact_path).resolve()
    return work_dir / "inputs" / "toy_plant_params.json"


class _MappingContext(PipelineExecutionContext):
    def __init__(self, registry, entry_values: Mapping[str, BaseModel]) -> None:
        super().__init__(registry)
        self.entry_values = entry_values


class _MappingExecutor(SerialPipelineExecutor):
    """Real executor with only file-backed EntryPoint loading replaced (B4)."""

    def _execute_entry(self, module_spec, spec, context) -> None:
        for binding in module_spec.outputs.values():
            context.set_channel(binding.channel_name, context.entry_values[binding.channel_name])


class PreparedEvaluator:
    """In-memory evaluator: prepare once (topology + write-handler validation,
    INV3), evaluate per case with a fresh context (no channel bleed)."""

    EVIDENCE_SCHEMA_VERSION = "v3"
    """The shape and numeric publication contract of this evaluator's evidence.

    `v2` -> `v3`: publish bare real ExitPoint values alongside numeric root wrappers,
    including Python bool as 0.0/1.0. Bind the expanded membership to a new study
    lineage even when package fingerprints remain unchanged. Historical stores remain readable.

    `v1` -> `v2` at CONSTRAINT-SEMANTICS Item 3: the report tree inside `ModelEvidence.report`
    gained a required `coverage` block, renamed `assessed_count` to `assessed_entry_count`,
    and replaced its headline vocabulary. This is a **bound** `Compatibility` field, so it is
    the carrier that makes reopening a pre-Item-3 store raise `IncompatibleStore` — the
    archive-and-begin route, already mechanized. `model_contract_fingerprint` cannot carry it:
    the item adds no catalog field and keeps `CATALOG_SCHEMA_VERSION` at 3.0.0, so for an
    already-constraint-bearing package whose channel set does not move, that fingerprint is
    byte-identical across the item.
    """
    EVALUATOR_VERSION = "v1"

    def __init__(
        self,
        loader: PackageLoader,
        spec_path: Path,
        *,
        expects_constraint_report: bool,
    ) -> None:
        self.package, self.fingerprint = loader.load()
        custom_types = list(self.package.CUSTOM_SCHEMA_TYPES)
        schema_types = _build_schema_type_registry(custom_types)
        entry_loaders = _build_entry_loaders(custom_types)
        registry_factory = getattr(self.package, f"create_{self.package.__name__}_registry")
        self._registry = registry_factory()
        spec = entry_point_validate(spec_path)
        self._expects_report = expects_constraint_report

        router = create_output_router_with_json_schemas(
            [t.__name__ for t in custom_types], include_builtins=True, in_memory=True
        )
        self._executor = _MappingExecutor(
            self._registry,
            output_router=router,
            schema_type_registry=dict(schema_types),
            entry_loaders=dict(entry_loaders),
        )
        try:
            self._graph = self._executor.build_graph(spec)
        except Exception as error:
            raise EvaluationFailed(
                EvaluationFailure(
                    phase=EvaluationPhase.PREPARATION,
                    cause=f"{type(error).__name__}: {error}",
                )
            ) from error
        self._source = MappingEntrySource.from_spec(spec, schema_types)

    @property
    def entry_models(self) -> Mapping[str, type[BaseModel]]:
        """Entry channel name -> typed model class, derived from the pipeline
        spec at prepare time — never a hardcoded generated class name (CE-F3)."""
        return self._source.expected_types

    def evaluate(self, typed_inputs: Mapping[str, BaseModel]) -> ModelEvidence:
        validated = self._source.validate(typed_inputs)
        context = _MappingContext(self._registry, validated)
        try:
            result = self._executor.run(self._graph, context, persist_outputs=False)
        except Exception as error:
            _normalize_run_failure(error, context)
        provenance = EvidenceProvenance(
            executable_fingerprint=self.fingerprint,
            evidence_schema_version=self.EVIDENCE_SCHEMA_VERSION,
            evaluator_version=self.EVALUATOR_VERSION,
            input_digest=_input_digest(typed_inputs),
        )
        return project(result, provenance=provenance, expects_report=self._expects_report)


class FileBackedEvaluator:
    """Audit backend: file entry, real (persisting) router, `persist_outputs=True`.

    Shares the same `project(...)` as `PreparedEvaluator` — this is what the
    parity test (INV4) admits the fast in-memory path on. The spec/entry
    artifacts live under a scratch `work_dir` this evaluator owns (a copy of
    the fixture package's `pipelines/pipeline.yaml`); it never writes into
    the sealed, seal-checked fixture tree itself.
    """

    EVIDENCE_SCHEMA_VERSION = PreparedEvaluator.EVIDENCE_SCHEMA_VERSION
    EVALUATOR_VERSION = PreparedEvaluator.EVALUATOR_VERSION

    def __init__(
        self,
        loader: PackageLoader,
        package_dir: Path,
        work_dir: Path,
        output_dir: Path,
        *,
        expects_constraint_report: bool,
    ) -> None:
        self.package, self.fingerprint = loader.load()
        custom_types = list(self.package.CUSTOM_SCHEMA_TYPES)
        schema_types = _build_schema_type_registry(custom_types)
        entry_loaders = _build_entry_loaders(custom_types)
        registry_factory = getattr(self.package, f"create_{self.package.__name__}_registry")
        registry = registry_factory()

        router = create_output_router_with_json_schemas(
            [t.__name__ for t in custom_types], include_builtins=True, in_memory=False
        )
        self._executor = SerialPipelineExecutor(
            registry,
            output_router=router,
            schema_type_registry=dict(schema_types),
            entry_loaders=dict(entry_loaders),
        )

        pipelines_dir = work_dir / "pipelines"
        pipelines_dir.mkdir(parents=True, exist_ok=True)
        spec_path = pipelines_dir / "pipeline.yaml"
        shutil.copy(package_dir / "pipelines" / "pipeline.yaml", spec_path)
        (work_dir / "inputs").mkdir(parents=True, exist_ok=True)

        spec = entry_point_validate(spec_path)
        try:
            self._graph = self._executor.build_graph(spec)
        except Exception as error:
            raise EvaluationFailed(
                EvaluationFailure(
                    phase=EvaluationPhase.PREPARATION,
                    cause=f"{type(error).__name__}: {error}",
                )
            ) from error
        self._registry = registry
        self._expects_report = expects_constraint_report
        # Write the candidate to the entry artifact path the spec actually
        # declares, derived from the single entry binding — not a hardcoded
        # fixture filename — so any generated single-group package loads.
        self._entry_path = _entry_artifact_path(spec, spec_path, work_dir)
        self._output_dir = output_dir

    def evaluate(self, entry_json_path: Path) -> ModelEvidence:
        entry_bytes = entry_json_path.read_bytes()
        self._entry_path.write_bytes(entry_bytes)
        context = PipelineExecutionContext(self._registry)
        try:
            result = self._executor.run(
                self._graph, context, base_output_dir=self._output_dir, persist_outputs=True
            )
        except Exception as error:
            _normalize_run_failure(error, context)
        provenance = EvidenceProvenance(
            executable_fingerprint=self.fingerprint,
            evidence_schema_version=self.EVIDENCE_SCHEMA_VERSION,
            evaluator_version=self.EVALUATOR_VERSION,
            input_digest=hashlib.sha256(entry_bytes).hexdigest(),
        )
        return project(result, provenance=provenance, expects_report=self._expects_report)
