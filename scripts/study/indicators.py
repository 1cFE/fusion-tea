#!/usr/bin/env python3
"""Conservative constraint/objective reachability for declared axis groups.

Reads a generated teax package's own artifacts and reports, per author-declared
axis group, which constraints and objectives a conservative path can reach.

Two layers, and the split is what makes the exit codes honest. The lower layer is
a pedantic reader: it loads the manifest, digests the artifacts it is about to read
and checks that digest against the manifest's pin, then parses the pipeline YAML
and the model contract in a mode where every unrecognized construct raises with a
location. Every failure there is mechanical, exits non-zero, and writes nothing.
The upper layer is the trace, and every outcome there is a fact that exits 0 —
including the empty one.

The report is a document, not a stream: it is assembled in memory and written once,
after every gate has passed, so no code path can produce a partial report.

The trace is deliberately over-approximate — every module output is taken to depend
on every module input. So a negative is sound (no finer analysis can find a path
this one missed) and a positive says only that the module graph admits a route.

Usage:
    indicators.py --package DIR --manifest FILE --groups FILE [--group NAME]... [--out FILE]
    indicators.py --package DIR --print-fingerprint

Generic by construction: this module names no package, no key prefix, and no
adapter (Invariant 6).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

if __package__ in (None, ""):  # invoked as a script: put the repo root on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.study import manifest as manifest_mod  # noqa: E402

REPORT_SCHEMA_VERSION = "study-indicators/v1"
AXIS_DECLARATION_SCHEMA_VERSION = "study-axis-declaration/v1"

#: The four disclosure strings, fixed text versioned with the schema (D5). Emitted
#: verbatim at the document level and inside every group, so a group excerpted into a
#: record's per-axis framing section still carries them.
NOT_DERIVABLE = {
    "statements": [
        "monotonicity or sign of any response",
        "same-quantity identity across differing key names",
        "intra-module operand dependency (the trace is module-level)",
    ],
    "positive_reading": (
        "A reachable constraint or objective means a possible path exists in the module "
        "graph. It never means the axis responds."
    ),
}

_STR_TAG = "tag:yaml.org,2002:str"
_MAP_TAG = "tag:yaml.org,2002:map"
_NULL_TAG = "tag:yaml.org,2002:null"

_ENTRY_TYPES = ("usage_literal", "library_default", "design_attribute")


class IndicatorError(Exception):
    """Mechanical failure: an artifact, reference, or declaration we cannot interpret."""


# ------------------------------------------------------------- the strict reader


@dataclass(frozen=True)
class Port:
    """One ``<port>: <type> <ref>`` entry, with the line it was declared on."""

    type: str
    ref: str
    line: int


@dataclass(frozen=True)
class Module:
    name: str
    module_type: str
    inputs: dict[str, Port]
    outputs: dict[str, Port]
    line: int
    file: Path


def _where(path: Path, line: int, key_path: str) -> str:
    return f"{manifest_mod.repo_relative_posix(path)}:{line} (key path {key_path})"


def _fail(path: Path, node: yaml.Node, key_path: str, message: str) -> None:
    raise IndicatorError(f"{_where(path, node.start_mark.line + 1, key_path)}: {message}")


def _mapping_pairs(
    node: yaml.Node, path: Path, key_path: str, *, strict_tags: bool
) -> list[tuple[str, yaml.Node]]:
    """Ordered key/value pairs of a mapping node, with unique string keys.

    ``strict_tags`` is on inside the ``modules`` subtree, where any node tag outside
    the standard str/map tags is a mechanical failure. An empty ``inputs:`` block
    composes to a null-tagged scalar rather than an empty mapping, so that is read
    as an empty map instead of raising.
    """
    if strict_tags and node.tag == _NULL_TAG:
        return []
    if not isinstance(node, yaml.MappingNode) or node.tag != _MAP_TAG:
        _fail(path, node, key_path, f"expected a mapping, found node tag {node.tag!r}")
    pairs: list[tuple[str, yaml.Node]] = []
    seen: set[str] = set()
    for key_node, value_node in node.value:
        if not isinstance(key_node, yaml.ScalarNode) or key_node.tag != _STR_TAG:
            _fail(path, key_node, key_path, f"expected a string key, found tag {key_node.tag!r}")
        key = key_node.value
        if key in seen:
            _fail(path, key_node, key_path, f"duplicate key {key!r}")
        seen.add(key)
        pairs.append((key, value_node))
    return pairs


def _scalar_string(node: yaml.Node, path: Path, key_path: str) -> str:
    if not isinstance(node, yaml.ScalarNode) or node.tag != _STR_TAG:
        _fail(path, node, key_path, f"expected a string scalar, found node tag {node.tag!r}")
    return node.value


def _read_ports(node: yaml.Node, path: Path, key_path: str) -> dict[str, Port]:
    ports: dict[str, Port] = {}
    for name, value_node in _mapping_pairs(node, path, key_path, strict_tags=True):
        where = f"{key_path}.{name}"
        value = _scalar_string(value_node, path, where)
        parts = value.split()
        if len(parts) != 2:
            _fail(path, value_node, where, f"cannot split type/ref in {value!r}")
        ports[name] = Port(type=parts[0], ref=parts[1], line=value_node.start_mark.line + 1)
    return ports


def read_pipeline(path: Path) -> dict[str, Module]:
    """Parse one pipeline YAML with ``yaml.compose``, keeping line numbers.

    Composing parses without constructing, so no tag can execute; but tags survive
    on nodes, so the walk asserts every tag inside the ``modules`` subtree. Every
    surprise raises with file, line, and key path.
    """
    try:
        root = yaml.compose(path.read_text(encoding="utf-8"))
    except OSError as exc:
        rel = manifest_mod.repo_relative_posix(path)
        raise IndicatorError(f"cannot read {rel}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise IndicatorError(
            f"{manifest_mod.repo_relative_posix(path)} is not valid YAML: {exc}"
        ) from exc
    if root is None:
        raise IndicatorError(f"{manifest_mod.repo_relative_posix(path)} is empty")

    top = dict(_mapping_pairs(root, path, "<root>", strict_tags=False))
    if set(top) != {"metadata", "modules"}:
        raise IndicatorError(
            f"{_where(path, root.start_mark.line + 1, '<root>')}: expected exactly the keys "
            f"'metadata' and 'modules', found {sorted(top)}"
        )
    # metadata gets a shape check only; nothing reads its contents.
    _mapping_pairs(top["metadata"], path, "metadata", strict_tags=False)

    modules: dict[str, Module] = {}
    for name, body_node in _mapping_pairs(top["modules"], path, "modules", strict_tags=True):
        key_path = f"modules.{name}"
        body = dict(_mapping_pairs(body_node, path, key_path, strict_tags=True))
        unknown = sorted(set(body) - {"module_type", "inputs", "outputs"})
        if unknown:
            _fail(path, body_node, key_path, f"unknown key(s) {unknown}")
        if "module_type" not in body:
            _fail(path, body_node, key_path, "missing 'module_type'")
        modules[name] = Module(
            name=name,
            module_type=_scalar_string(body["module_type"], path, f"{key_path}.module_type"),
            inputs=(
                _read_ports(body["inputs"], path, f"{key_path}.inputs")
                if "inputs" in body
                else {}
            ),
            outputs=(
                _read_ports(body["outputs"], path, f"{key_path}.outputs")
                if "outputs" in body
                else {}
            ),
            line=body_node.start_mark.line + 1,
            file=path,
        )
    return modules


def _sole_module_of_type(
    modules: dict[str, Module], module_type: str, path: Path
) -> Module:
    found = sorted(m.name for m in modules.values() if m.module_type == module_type)
    if len(found) != 1:
        raise IndicatorError(
            f"{manifest_mod.repo_relative_posix(path)}: expected exactly one {module_type} "
            f"module, found {len(found)}: {found}"
        )
    return modules[found[0]]


# ---------------------------------------------------------------- the graph


@dataclass
class PackageGraph:
    """The package-scoped channel graph, built across every pipeline file."""

    modules: dict[str, Module] = field(default_factory=dict)
    entry_groups: set[str] = field(default_factory=set)
    input_files: list[Path] = field(default_factory=list)
    producer: dict[str, str] = field(default_factory=dict)
    deps: dict[str, dict[str, set[str]]] = field(default_factory=dict)
    input_keys: dict[str, str] = field(default_factory=dict)


def classify_ref(raw: str, entry_groups: set[str], where: str) -> tuple[str, str]:
    """Normalize one input reference into ``('bound', key)`` or ``('channel', name)``.

    R1 an entry-prefixed ``<group>.<key>`` is a bound input; R2 a bare ref is a
    produced channel; R3 a trailing ``.root`` is stripped (RootModel outputs declare a
    single field named ``root``, and 65 edges depend on the strip); R4 any other
    dotted ref is a hard failure, never guessed at and never silently dropped.
    """
    ref = raw.strip()
    head = ref.split(".", 1)[0]
    if head in entry_groups:
        rest = ref.split(".", 1)[1] if "." in ref else None
        if rest is None or "." in rest:
            raise IndicatorError(
                f"{where}: entry-prefixed reference is not '<group>.<key>': {raw!r}"
            )
        return "bound", rest
    if ref.endswith(".root"):
        return "channel", ref[: -len(".root")]
    if "." in ref:
        raise IndicatorError(f"{where}: unparseable reference {raw!r}")
    return "channel", ref


def build_graph(package_root: Path) -> PackageGraph:
    """Read every pipeline file and wire one package-scoped channel graph.

    A channel produced by more than one module — same file or across files — is a
    mechanical failure, as is a module name that appears in two files.
    """
    graph = PackageGraph()
    pipeline_paths = sorted((package_root / "pipelines").glob("*.yaml"))
    if not pipeline_paths:
        raise IndicatorError("no pipeline files at pipelines/*.yaml")

    entries: list[tuple[Module, Path]] = []
    for path in pipeline_paths:
        file_modules = read_pipeline(path)
        for name, module in file_modules.items():
            if name in graph.modules:
                raise IndicatorError(
                    f"module {name!r} is declared in two pipeline files: "
                    f"{manifest_mod.repo_relative_posix(graph.modules[name].file)} and "
                    f"{manifest_mod.repo_relative_posix(path)}"
                )
            graph.modules[name] = module
        entry = _sole_module_of_type(file_modules, "EntryPoint", path)
        _sole_module_of_type(file_modules, "ExitPoint", path)
        entries.append((entry, path))

    for entry, path in entries:
        for group, port in entry.inputs.items():
            graph.entry_groups.add(group)
            resolved = (path.parent / port.ref).resolve()
            if resolved not in graph.input_files:
                graph.input_files.append(resolved)

    for module in graph.modules.values():
        if module.module_type in ("EntryPoint", "ExitPoint"):
            continue  # R11: neither participates in the closure
        bound: set[str] = set()
        channels: set[str] = set()
        for port_name, port in module.inputs.items():
            where = _where(module.file, port.line, f"modules.{module.name}.inputs.{port_name}")
            kind, value = classify_ref(port.ref, graph.entry_groups, where)
            (bound if kind == "bound" else channels).add(value)
        graph.deps[module.name] = {"bound": bound, "channels": channels}
        for port_name, port in module.outputs.items():
            where = _where(module.file, port.line, f"modules.{module.name}.outputs.{port_name}")
            if "." in port.ref:
                raise IndicatorError(f"{where}: output channel carries a field path: {port.ref!r}")
            if port.ref in graph.producer:
                raise IndicatorError(
                    f"{where}: channel {port.ref!r} is produced by more than one module: "
                    f"{graph.producer[port.ref]!r} and {module.name!r}"
                )
            graph.producer[port.ref] = module.name

    graph.input_files.sort()
    for path in graph.input_files:
        for key in _read_input_keys(path):
            if key in graph.input_keys:
                raise IndicatorError(
                    f"input key {key!r} appears in two entry groups: "
                    f"{graph.input_keys[key]} and {manifest_mod.repo_relative_posix(path)}"
                )
            graph.input_keys[key] = manifest_mod.repo_relative_posix(path)
    return graph


def _read_input_keys(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_bytes())
    except OSError as exc:
        raise IndicatorError(
            f"cannot read input file {manifest_mod.repo_relative_posix(path)}: {exc}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise IndicatorError(
            f"input file {manifest_mod.repo_relative_posix(path)} is not valid JSON: {exc}"
        ) from exc
    if not isinstance(data, dict):
        raise IndicatorError(
            f"input file {manifest_mod.repo_relative_posix(path)}: expected an object of keys"
        )
    return list(data)


def reachable_channels(
    declared: set[str], graph: PackageGraph
) -> tuple[set[str], set[str]]:
    """Conservative forward closure (R10).

    A module fires if any declared key or any tainted channel is among its inputs,
    and firing taints all of its outputs. Iterated to fixpoint.
    """
    outputs_of: dict[str, set[str]] = {}
    for channel, module in graph.producer.items():
        outputs_of.setdefault(module, set()).add(channel)

    tainted: set[str] = set()
    fired: set[str] = set()
    changed = True
    while changed:
        changed = False
        for module, dep in graph.deps.items():
            if module in fired:
                continue
            if (dep["bound"] & declared) or (dep["channels"] & tainted):
                fired.add(module)
                tainted |= outputs_of.get(module, set())
                changed = True
    return tainted, fired


# ------------------------------------------------------------ the contract


@dataclass(frozen=True)
class ModelContract:
    semantic_fingerprint: str
    entry_types: dict[str, str]
    concrete_entries: list[dict]


def read_model_contract(package_root: Path) -> ModelContract:
    path = package_root / "contracts" / "model_contract.json"
    rel = manifest_mod.repo_relative_posix(path)
    try:
        data = json.loads(path.read_bytes())
    except OSError as exc:
        raise IndicatorError(f"cannot read {rel}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise IndicatorError(f"{rel} is not valid JSON: {exc}") from exc
    for key in ("constraint_catalog", "parameters", "outputs", "semantic_fingerprint"):
        if key not in data:
            raise IndicatorError(f"{rel}: missing {key!r}")

    entry_types: dict[str, str] = {}
    for i, param in enumerate(data["parameters"]):
        name = param.get("qualified_name")
        entry_type = param.get("entry_type")
        if not isinstance(name, str) or entry_type not in _ENTRY_TYPES:
            raise IndicatorError(
                f"{rel}: parameters[{i}] has no usable qualified_name/entry_type: {param!r}"
            )
        entry_types[name] = entry_type

    entries = data["constraint_catalog"].get("concrete_entries")
    if not isinstance(entries, list) or not entries:
        raise IndicatorError(f"{rel}: constraint_catalog.concrete_entries is empty or absent")
    for i, entry in enumerate(entries):
        for key in (
            "constraint_id",
            "definition_qualified_name",
            "source_local_identity",
            "predicate_ir",
        ):
            if key not in entry:
                raise IndicatorError(f"{rel}: concrete_entries[{i}] is missing {key!r}")
    return ModelContract(
        semantic_fingerprint=data["semantic_fingerprint"],
        entry_types=entry_types,
        concrete_entries=entries,
    )


def predicate_operands(entry: dict) -> tuple[str, list[dict]]:
    """The operator and ordered operand descriptors from ``predicate_ir`` (R7, R8).

    Literal operands exist only here — they appear in no YAML and no input file.
    Any operand kind other than ``feature_ref`` or ``literal`` raises.
    """
    cid = entry["constraint_id"]
    try:
        ir = json.loads(entry["predicate_ir"])
    except (TypeError, json.JSONDecodeError) as exc:
        raise IndicatorError(f"constraint {cid}: predicate_ir is not valid JSON: {exc}") from exc
    if ir.get("kind") != "operator":
        raise IndicatorError(f"constraint {cid}: predicate_ir root is not an operator")
    operands = []
    for operand in ir["operands"]:
        if operand["kind"] == "feature_ref":
            operands.append({"kind": "feature_ref", "name": operand["reference"]["source_name"]})
        elif operand["kind"] == "literal":
            operands.append({"kind": "literal", "value": operand["literal"]["value"]})
        else:
            raise IndicatorError(
                f"constraint {cid}: unknown predicate operand kind {operand['kind']!r}"
            )
    return ir["operator"], operands


# ------------------------------------------------------ the axis declaration


@dataclass(frozen=True)
class AxisGroup:
    axis: str
    keys: list[tuple[str, str]]  # (key, provenance)


@dataclass(frozen=True)
class AxisDeclaration:
    path: Path
    digest: str
    schema_version: str
    groups: list[AxisGroup]


def read_axis_declaration(path: Path) -> AxisDeclaration:
    """Read the per-study axis declaration. Every surprise is a mechanical failure."""
    rel = manifest_mod.repo_relative_posix(path)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise IndicatorError(f"cannot read axis declaration {rel}: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise IndicatorError(f"axis declaration {rel} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise IndicatorError(f"axis declaration {rel}: expected an object")
    unknown = sorted(set(data) - {"schema_version", "groups"})
    if unknown:
        raise IndicatorError(f"axis declaration {rel}: unknown key(s) {unknown}")
    version = data.get("schema_version")
    if version != AXIS_DECLARATION_SCHEMA_VERSION:
        raise IndicatorError(
            f"axis declaration {rel}: schema_version must be "
            f"{AXIS_DECLARATION_SCHEMA_VERSION!r}, found {version!r}"
        )
    raw_groups = data.get("groups")
    if not isinstance(raw_groups, list) or not raw_groups:
        raise IndicatorError(f"axis declaration {rel}: 'groups' must be a non-empty list")

    groups: list[AxisGroup] = []
    seen_axes: set[str] = set()
    for i, raw_group in enumerate(raw_groups):
        where = f"axis declaration {rel}: groups[{i}]"
        if not isinstance(raw_group, dict):
            raise IndicatorError(f"{where}: expected an object")
        unknown = sorted(set(raw_group) - {"axis", "keys", "note"})
        if unknown:
            raise IndicatorError(f"{where}: unknown key(s) {unknown}")
        axis = raw_group.get("axis")
        if not isinstance(axis, str) or not axis:
            raise IndicatorError(f"{where}: 'axis' must be a non-empty string")
        if axis in seen_axes:
            raise IndicatorError(f"{where}: duplicate axis name {axis!r}")
        seen_axes.add(axis)
        raw_keys = raw_group.get("keys")
        if not isinstance(raw_keys, list) or not raw_keys:
            raise IndicatorError(f"{where} ({axis}): 'keys' must be a non-empty list")
        keys: list[tuple[str, str]] = []
        seen_keys: set[str] = set()
        for j, raw_key in enumerate(raw_keys):
            key_where = f"{where} ({axis}): keys[{j}]"
            if not isinstance(raw_key, dict):
                raise IndicatorError(f"{key_where}: expected an object")
            unknown = sorted(set(raw_key) - {"key", "provenance"})
            if unknown:
                raise IndicatorError(f"{key_where}: unknown key(s) {unknown}")
            key = raw_key.get("key")
            provenance = raw_key.get("provenance")
            if not isinstance(key, str) or not key:
                raise IndicatorError(f"{key_where}: 'key' must be a non-empty string")
            if provenance not in ("fan_out", "tie"):
                raise IndicatorError(
                    f"{key_where}: 'provenance' must be 'fan_out' or 'tie', found {provenance!r}"
                )
            if key in seen_keys:
                raise IndicatorError(f"{key_where}: duplicate key {key!r} in group {axis!r}")
            seen_keys.add(key)
            keys.append((key, provenance))
        groups.append(AxisGroup(axis=axis, keys=keys))

    return AxisDeclaration(
        path=path,
        digest=hashlib.sha256(raw).hexdigest(),
        schema_version=version,
        groups=groups,
    )


# ------------------------------------------------------------ per-group work


def resolve_declared_keys(
    group: AxisGroup, graph: PackageGraph, contract: ModelContract
) -> list[dict]:
    """Resolve each declared key to its entry type, in the order that makes each failure
    say the right thing: present in inputs, else a produced channel, else absent."""
    resolved = []
    for key, provenance in group.keys:
        if key in graph.input_keys:
            entry_type = contract.entry_types.get(key)
            if entry_type is None:
                raise IndicatorError(
                    f"axis {group.axis!r}: declared key {key!r} is present in inputs/ but is not "
                    f"in contract parameters, so its entry type cannot be classified"
                )
            resolved.append({"key": key, "provenance": provenance, "entry_type": entry_type})
        elif key in graph.producer:
            raise IndicatorError(
                f"axis {group.axis!r}: declared key {key!r} names a computed quantity — it is a "
                f"channel produced by module {graph.producer[key]!r}, not a bound input. A "
                f"computed quantity is a model output, not an axis."
            )
        else:
            raise IndicatorError(
                f"axis {group.axis!r}: declared key {key!r} is absent from the package inputs"
            )
    resolved.sort(key=lambda entry: entry["key"])
    return resolved


def _constraint_entry(
    entry: dict, graph: PackageGraph, contract: ModelContract, declared: set[str], tainted: set[str]
) -> dict:
    """One constraint under one axis. The same shape serves bounds and both partitions."""
    cid = entry["constraint_id"]
    module = graph.modules.get(cid)
    if module is None:
        raise IndicatorError(f"constraint {cid!r} has no matching module in the pipeline")
    operator, operands = predicate_operands(entry)

    detail = []
    for operand in operands:
        if operand["kind"] == "literal":
            detail.append(
                {
                    "operand": "<literal>",
                    "class": "literal",
                    "reached": False,
                    "value": operand["value"],
                }
            )
            continue
        name = operand["name"]
        port = module.inputs.get(name)
        if port is None:
            raise IndicatorError(
                f"constraint {cid}: predicate operand {name!r} has no matching input port on "
                f"module {cid!r}"
            )
        where = _where(module.file, port.line, f"modules.{cid}.inputs.{name}")
        kind, value = classify_ref(port.ref, graph.entry_groups, where)
        operand_class = "bound" if kind == "bound" else "computed"
        reached = (value in declared) if kind == "bound" else (value in tainted)
        record = {"operand": name, "class": operand_class, "ref": value, "reached": reached}
        if kind == "bound":
            record["entry_type"] = contract.entry_types.get(value)
            if record["entry_type"] is None:
                raise IndicatorError(
                    f"constraint {cid}: bound operand {name!r} refers to {value!r}, which is not "
                    f"in contract parameters"
                )
        detail.append(record)

    classes = sorted({d["class"] for d in detail if d["class"] != "literal"})
    return {
        "constraint_id": cid,
        "definition_qualified_name": entry["definition_qualified_name"],
        "source_local_identity": entry["source_local_identity"],
        "operator": operator,
        "operand_classes": classes,
        "bound_vs_bound": classes == ["bound"],
        "operands": detail,
    }


def suffix_siblings(declared_keys: list[str], graph: PackageGraph) -> list[str]:
    """Advisory only (R12): keys outside the group sharing a declared key's suffix.

    Computed after the trace and never merged into the group. Suffixes are not
    identity — a tie whose suffix differs will never surface here, which is why
    membership is declared.
    """
    suffixes = {key.rsplit("__", 1)[-1] for key in declared_keys}
    declared = set(declared_keys)
    return sorted(
        key
        for key in graph.input_keys
        if key.rsplit("__", 1)[-1] in suffixes and key not in declared
    )


def tie_candidate_warnings(declared_keys: list[str], ties: list[dict]) -> list[dict]:
    """Advisory only: a tie whose partners are all in the group while its key is not."""
    declared = set(declared_keys)
    warnings = []
    for tie in ties:
        if tie["key"] in declared:
            continue
        if set(tie["rides_with"]) <= declared:
            warnings.append(
                {
                    "kind": "tie_candidate",
                    "detail": (
                        f"the manifest declares {tie['key']!r} as riding with "
                        f"{', '.join(sorted(tie['rides_with']))}, all of which are in this group. "
                        f"Membership is declared-only, so the key was not added — declare it if "
                        f"it belongs."
                    ),
                }
            )
    return warnings


def trace_group(
    group: AxisGroup,
    graph: PackageGraph,
    contract: ModelContract,
    objective_catalog: list[dict],
    ties: list[dict],
) -> dict:
    """One group object: the resolved keys, the closure, and what it reached."""
    declared_keys = resolve_declared_keys(group, graph, contract)
    declared = {entry["key"] for entry in declared_keys}
    tainted, fired = reachable_channels(declared, graph)

    bounds = sorted(
        (
            _constraint_entry(entry, graph, contract, declared, tainted)
            for entry in contract.concrete_entries
        ),
        key=lambda entry: entry["constraint_id"],
    )
    reachable = [c for c in bounds if any(o["reached"] for o in c["operands"])]
    unreachable = [c for c in bounds if not any(o["reached"] for o in c["operands"])]

    objectives_reachable = sorted(
        obj["name"] for obj in objective_catalog if obj["channel"] in tainted
    )
    objectives_unreachable = sorted(
        obj["name"] for obj in objective_catalog if obj["channel"] not in tainted
    )

    return {
        "axis": group.axis,
        "declared_keys": declared_keys,
        "group_valid": True,
        "no_constraint_response": not reachable,
        "constraints_reachable": reachable,
        "constraints_unreachable": unreachable,
        "bounds": bounds,
        "objectives_reachable": objectives_reachable,
        "objectives_unreachable": objectives_unreachable,
        "sibling_candidates": suffix_siblings(sorted(declared), graph),
        "trace_size": {"modules_fired": len(fired), "channels_tainted": len(tainted)},
        "warnings": tie_candidate_warnings(sorted(declared), ties),
        "not_derivable": NOT_DERIVABLE,
    }


# --------------------------------------------------------------- the document


def _document_warnings(
    loaded: manifest_mod.LoadedManifest, package_root: Path, groups: list[AxisGroup]
) -> list[dict]:
    """Cross-cutting facts that never gate: provenance drift and shared keys."""
    warnings = []
    recorded = loaded.data["fingerprints"]["recorded_provenance"]
    live = {
        "semantic_fingerprint": manifest_mod.read_semantic_fingerprint(package_root),
        "executable_fingerprint": manifest_mod.read_executable_fingerprint(package_root),
    }
    for name, live_value in sorted(live.items()):
        if recorded[name] != live_value:
            warnings.append(
                {
                    "kind": "provenance_drift",
                    "detail": (
                        f"manifest records {name} {recorded[name]} but the live package reports "
                        f"{live_value}. Provenance only — a record built from this run would "
                        f"state the wrong package revision."
                    ),
                }
            )

    owners: dict[str, list[str]] = {}
    for group in groups:
        for key, _ in group.keys:
            owners.setdefault(key, []).append(group.axis)
    for key, axes in sorted(owners.items()):
        if len(axes) > 1:
            warnings.append(
                {
                    "kind": "duplicate_key_across_groups",
                    "detail": f"key {key!r} is declared in more than one group: {', '.join(axes)}",
                }
            )
    return warnings


def _assert_objective_channels_exist(objective_catalog: list[dict], graph: PackageGraph) -> None:
    for objective in objective_catalog:
        if objective["channel"] not in graph.producer:
            raise IndicatorError(
                f"objective {objective['name']!r}: channel {objective['channel']!r} is produced "
                f"by no module"
            )


def build_report(
    package_root: Path,
    loaded: manifest_mod.LoadedManifest,
    declaration: AxisDeclaration,
    selected: list[str],
) -> dict:
    """Run every gate, trace the selected groups, and assemble the whole document.

    Gate order is fixed (D8): manifest schema (already done by the loader) →
    package identity → indicator-input fingerprint → pipeline parse → contract parse
    → declared-key resolution → trace. The read-set coverage check (M3) is one
    assertion after the parse; it does not disturb that order.
    """
    manifest_mod.assert_package_identity(loaded, package_root)
    fingerprint = manifest_mod.indicator_input_fingerprint(package_root)
    manifest_mod.assert_pin_matches(loaded, fingerprint)

    graph = build_graph(package_root)
    contract_path = package_root / "contracts" / "model_contract.json"
    manifest_mod.assert_read_set_covered(
        [m.file for m in graph.modules.values()] + graph.input_files + [contract_path],
        package_root,
        loaded,
    )
    contract = read_model_contract(package_root)

    objective_catalog = [
        {"name": obj["name"], "channel": obj["channel"]}
        for obj in loaded.data["objective_catalog"]
    ]
    objective_catalog.sort(key=lambda obj: obj["name"])
    _assert_objective_channels_exist(objective_catalog, graph)

    ties = loaded.data["ties"]
    declared_names = [group.axis for group in declaration.groups]
    if selected:
        unknown = sorted(set(selected) - set(declared_names))
        if unknown:
            raise IndicatorError(
                f"--group named axes that are not in the declaration: {', '.join(unknown)}"
            )
        traced = [g for g in declaration.groups if g.axis in set(selected)]
    else:
        traced = list(declaration.groups)

    groups = sorted(
        (trace_group(g, graph, contract, objective_catalog, ties) for g in traced),
        key=lambda g: g["axis"],
    )

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "tool": {
            "path": manifest_mod.repo_relative_posix(Path(__file__)),
            "source_digest": manifest_mod.tool_source_digest(),
        },
        "package": {
            "path": loaded.data["package"]["path"],
            "package_name": manifest_mod.read_package_name(package_root),
            "semantic_fingerprint": contract.semantic_fingerprint,
            "recorded_executable_fingerprint": manifest_mod.read_executable_fingerprint(
                package_root
            ),
            "indicator_input_fingerprint": fingerprint,
        },
        "manifest": {
            "path": manifest_mod.repo_relative_posix(loaded.path),
            "schema_version": loaded.data["schema_version"],
            "digest": loaded.digest,
        },
        "axis_declaration": {
            "path": manifest_mod.repo_relative_posix(declaration.path),
            "schema_version": declaration.schema_version,
            "digest": declaration.digest,
            "groups_declared": sorted(declared_names),
            "subset": bool(selected),
        },
        "objective_catalog": objective_catalog,
        "not_derivable": NOT_DERIVABLE,
        "warnings": _document_warnings(loaded, package_root, declaration.groups),
        "groups": groups,
    }


def human_summary(report: dict) -> str:
    """The per-group summary that goes to stderr, so it can never contaminate stdout."""
    lines = []
    for group in report["groups"]:
        lines.append(
            f"{group['axis']}: "
            f"no_constraint_response={str(group['no_constraint_response']).lower()} "
            f"constraints {len(group['constraints_reachable'])}/{len(group['bounds'])} "
            f"objectives {len(group['objectives_reachable'])}/"
            f"{len(group['objectives_reachable']) + len(group['objectives_unreachable'])} "
            f"modules_fired={group['trace_size']['modules_fired']}"
        )
    lines.append(NOT_DERIVABLE["positive_reading"])
    return "\n".join(lines)


def write_atomically(text: str, out_path: Path) -> None:
    """Write via a temp file in the same directory, then rename."""
    temp = out_path.with_name(out_path.name + ".tmp")
    temp.write_text(text, encoding="utf-8")
    os.replace(temp, out_path)


# ----------------------------------------------------------------------- CLI


def print_fingerprint(package_root: Path) -> str:
    """The indicator-input fingerprint plus every per-file digest, as printable text."""
    computed = manifest_mod.indicator_input_fingerprint(package_root)
    lines = [f"recipe {computed['recipe']}", f"digest {computed['digest']}", "files"]
    lines += [f"  {f['path']} {f['sha256']}" for f in computed["files"]]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="indicators.py",
        description="Conservative constraint/objective reachability for declared axis groups.",
    )
    parser.add_argument("--package", required=True, metavar="DIR", help="package root directory")
    parser.add_argument("--manifest", metavar="FILE", help="study package manifest JSON")
    parser.add_argument("--groups", metavar="FILE", help="axis declaration JSON")
    parser.add_argument(
        "--group",
        action="append",
        default=[],
        metavar="NAME",
        help="trace only this axis (repeatable); a debugging aid — forces subset: true",
    )
    parser.add_argument("--out", metavar="FILE", help="write the report here instead of stdout")
    parser.add_argument(
        "--print-fingerprint",
        action="store_true",
        help="print the indicator-input fingerprint and per-file digests, then exit",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    package_root = Path(args.package)

    if args.print_fingerprint:
        for unsupported in ("manifest", "groups", "out"):
            if getattr(args, unsupported):
                parser.error(f"--{unsupported} is not used with --print-fingerprint")
        if args.group:
            parser.error("--group is not used with --print-fingerprint")
    elif not args.manifest or not args.groups:
        parser.error("--manifest and --groups are required unless --print-fingerprint is given")

    try:
        if args.print_fingerprint:
            print(print_fingerprint(package_root))
            return 0
        loaded = manifest_mod.load(Path(args.manifest))
        declaration = read_axis_declaration(Path(args.groups))
        report = build_report(package_root, loaded, declaration, args.group)
    except (IndicatorError, manifest_mod.ManifestError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    text = json.dumps(report, indent=2) + "\n"
    print(human_summary(report), file=sys.stderr)
    if args.out:
        write_atomically(text, Path(args.out))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
