"""Record a contract from an observation of the pin, and check an observation against it.

Recording classifies map and enum paths from the pinned server's /openapi.json. Check
reads no response schema, only what contract.txt stores; the Request fields rule reads the
current server's request schemas (design Architecture). The rules and their failure keys
follow the design's rules table and Appendix E.
"""

from __future__ import annotations

import re
from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from contract_text import Contract, line_value
from frontend_requests import (
    EXPLORER,
    LITERAL_READS,
    PREFLIGHTS,
    REQUESTS,
    WEBSITE_ORIGIN,
    Observation,
    bodies,
    coverage_sets,
    joined_lists,
    linked_lists,
    manifest_concept_ids,
    observe,
    preflight,
    route,
    serve,
)
from json_shapes import VACANT, field_path, flatten, strings_at, unwritable_keys

# ---------------------------------------------------------------------------
# Classify: map paths and enum paths from the pinned server's /openapi.json
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Schema:
    maps: frozenset[tuple[str, str]]  # (template, path) of every map object
    enum_paths: Mapping[tuple[str, str], str]  # (template, path) -> enum name
    enums: Mapping[str, tuple[str, ...]]  # enum name -> its values


def classify(openapi: Mapping[str, Any]) -> Schema:
    """Find the map and enum paths in each template's 200 response schema.

    A map is an object whose `additionalProperties` is a schema; `true` stays a record.
    A route the server doesn't have contributes nothing: its requests 404, and record
    writes that status.
    """
    components = openapi.get("components", {}).get("schemas", {})
    maps: set[tuple[str, str]] = set()
    enum_paths: dict[tuple[str, str], str] = {}
    enums: dict[str, tuple[str, ...]] = {}

    def walk(template: str, node: Mapping[str, Any], path: str) -> None:
        name = None
        if "$ref" in node:
            name = node["$ref"].rsplit("/", 1)[1]
            node = components[name]
        if "enum" in node:
            if name is None:
                raise ValueError(f"inline enum at {template} {path} has no component name")
            enum_paths[(template, path)] = name
            enums[name] = tuple(line_value(str(value)) for value in node["enum"])
            return
        for alternative in node.get("anyOf", []) + node.get("allOf", []):
            walk(template, alternative, path)
        extra = node.get("additionalProperties")
        if isinstance(extra, dict):
            if node.get("properties"):
                raise ValueError(
                    f"{template} {path}: an object with both properties and a map schema"
                )
            maps.add((template, path))
            walk(template, extra, path + "{*}")
        for key, child in node.get("properties", {}).items():
            walk(template, child, field_path(path, key))
        for child in [node["items"]] if "items" in node else node.get("prefixItems", []):
            walk(template, child, path + "[]")

    for template in REQUESTS:
        operation = _operation(openapi, template)
        if operation is None:
            continue
        schema = (
            operation["responses"]["200"]
            .get("content", {})
            .get("application/json", {})
            .get("schema")
        )
        if schema is not None:
            walk(template, schema, ".")
    return Schema(frozenset(maps), enum_paths, enums)


def request_fields(openapi: Mapping[str, Any]) -> dict[str, frozenset[str]]:
    """For each template, the top-level fields its route's JSON request body declares.

    A route that takes no JSON body, or isn't there, declares none.
    """
    components = openapi.get("components", {}).get("schemas", {})
    declared = {}
    for template in REQUESTS:
        operation = _operation(openapi, template) or {}
        content = operation.get("requestBody", {}).get("content", {})
        schema = content.get("application/json", {}).get("schema")
        declared[template] = frozenset() if schema is None else _properties(schema, components)
    return declared


def _properties(node: Mapping[str, Any], components: Mapping[str, Any]) -> frozenset[str]:
    """The property names an object schema declares, through `$ref`, `anyOf` and `allOf`."""
    if "$ref" in node:
        node = components[node["$ref"].rsplit("/", 1)[1]]
    names = frozenset(node.get("properties", {}))
    for alternative in node.get("anyOf", []) + node.get("allOf", []):
        names |= _properties(alternative, components)
    return names


def _operation(openapi: Mapping[str, Any], template: str) -> Mapping[str, Any] | None:
    """The OpenAPI operation serving `template`; None if the server has no such route."""
    method = template.split(" ")[0].lower()
    for path, operations in openapi.get("paths", {}).items():
        if _route_pattern(path) == _route_pattern(route(template)):
            return operations.get(method)
    return None


def _route_pattern(path: str) -> str:
    """'/api/concepts/{concept_id}' and '/api/concepts/{id}' -> '/api/concepts/{}'."""
    return re.sub(r"\{[^}]*\}", "{}", path)


# ---------------------------------------------------------------------------
# Record
# ---------------------------------------------------------------------------


def record(
    observation: Observation, schema: Schema, pin: str, tools: Iterable[str], js: Mapping[str, str]
) -> Contract:
    """The contract an observation of the pinned server establishes."""
    _refuse_unwritable_keys(observation, schema.maps)
    shapes = shapes_of(observation, schema.maps, schema.enum_paths)
    used_enums = {
        kind.removeprefix("enum:")
        for kinds in shapes.values()
        for kind in kinds
        if kind.startswith("enum:")
    }
    lists = joined_lists(observation)
    return Contract(
        pin=pin,
        tools=tuple(sorted(tools)),
        js=dict(js),
        concepts=tuple(sorted(lists["manifest"])),
        lists={name: tuple(sorted(ids)) for name, ids in lists.items()},
        coverage={
            template: tuple(sorted(ids)) for template, ids in coverage_sets(observation).items()
        },
        status={
            template: tuple(sorted({r.status for r in responses}))
            for template, responses in observation.items()
        },
        enums={name: schema.enums[name] for name in used_enums},
        literals=dict(LITERAL_READS),
        maps=schema.maps,
        shapes=shapes,
    )


def _refuse_unwritable_keys(observation: Observation, maps: Collection[tuple[str, str]]) -> None:
    """Raise if a record key can't be written as a path: the contract couldn't hold it.

    Check skips such a key as new; a recording mustn't silently leave it out.
    """
    for template, responses in observation.items():
        map_paths = {path for t, path in maps if t == template}
        unwritable = unwritable_keys(bodies(responses), map_paths)
        if unwritable:
            where = ", ".join(f"{key!r} under {path}" for path, key in unwritable)
            raise ValueError(
                f"{template}: record keys can't be written as paths: {where}. A data-driven "
                "key like this most likely means a map was classified as a record"
            )


def shapes_of(
    observation: Observation,
    maps: Collection[tuple[str, str]],
    enum_paths: Mapping[tuple[str, str], str],
) -> dict[tuple[str, str], frozenset[str]]:
    """(template, path) -> kinds across the 2xx bodies; enum-path strings become `enum:<Name>`."""
    shapes: dict[tuple[str, str], frozenset[str]] = {}
    for template, responses in observation.items():
        map_paths = {path for t, path in maps if t == template}
        for path, kinds in flatten(bodies(responses), map_paths).items():
            enum_name = enum_paths.get((template, path))
            if enum_name is not None and "string" in kinds:
                kinds = (kinds - {"string"}) | {f"enum:{enum_name}"}
            shapes[(template, path)] = frozenset(kinds)
    return shapes


# ---------------------------------------------------------------------------
# Check: the rules (design Architecture, rules table; Appendix E key grammar)
# ---------------------------------------------------------------------------


def check(observation: Observation, contract: Contract) -> list[str]:
    """Every failure key the observation earns against the contract, sorted."""
    return sorted(
        status_failures(observation, contract)
        | shape_failures(observed_shapes(observation, contract), contract)
        | value_failures(observation, contract)
        | concept_failures(observation, contract)
        | coverage_failures(observation, contract)
    )


def observed_shapes(
    observation: Observation, contract: Contract
) -> dict[tuple[str, str], frozenset[str]]:
    """The observation's shapes, flattened with the contract's map and enum paths.

    A pinned record field that no object at its parent path carries any more is
    `absent`. Flattening alone can't say so, because it never saw the key.
    """
    shapes = shapes_of(observation, contract.maps, _enum_paths(contract))
    for template, path in contract.shapes.keys() - shapes.keys():
        parent = _record_parent(path)
        if parent is not None and "object" in shapes.get((template, parent), ()):
            shapes[(template, path)] = frozenset({"absent"})
    return shapes


def _record_parent(path: str) -> str | None:
    """'.a.b' -> '.a' and '.b' -> '.'; None for an array or map element path."""
    if path == "." or path.endswith(("[]", "{*}")):
        return None
    return path.rsplit(".", 1)[0] or "."


def _enum_paths(contract: Contract) -> dict[tuple[str, str], str]:
    return {
        key: kind.removeprefix("enum:")
        for key, kinds in contract.shapes.items()
        for kind in kinds
        if kind.startswith("enum:")
    }


def status_failures(observation: Observation, contract: Contract) -> set[str]:
    """A status outside the pinned set; or no 200 at all where the pin had one (decision 8)."""
    failures = set()
    for template, codes in contract.status.items():
        responses = observation.get(template, [])
        failures |= {
            failure_key("status", template, r.instance) for r in responses if r.status not in codes
        }
        if 200 in codes and not any(r.status == 200 for r in responses):
            failures.add(failure_key("status", template, None))
    return failures


def shape_failures(
    shapes: Mapping[tuple[str, str], frozenset[str]], contract: Contract
) -> set[str]:
    """Shape: a recorded path has a new kind. Unpopulated: a vacant pinned path carries a value."""
    failures = set()
    for (template, path), kinds in shapes.items():
        pinned = contract.shapes.get((template, path))
        if pinned is None:
            continue  # a new path
        if pinned <= VACANT:
            if kinds - VACANT:
                failures.add(failure_key("unpopulated", template, path))
        elif kinds - pinned:
            failures.add(failure_key("shape", template, path))
    return failures


def value_failures(observation: Observation, contract: Contract) -> set[str]:
    """Enum: a value outside the pinned enum. Literal: a value outside the cited allowed set."""
    rules = [("enum", key, contract.enums[name]) for key, name in _enum_paths(contract).items()]
    rules += [("literal", key, values) for key, values in contract.literals.items()]
    failures = set()
    for rule, (template, path), allowed in rules:
        map_paths = {p for t, p in contract.maps if t == template}
        template_bodies = bodies(observation.get(template, []))
        values = strings_at(template_bodies, map_paths, lambda p: p == path)
        if values - set(allowed):
            failures.add(failure_key(rule, template, path))
    return failures


def concept_failures(observation: Observation, contract: Contract) -> set[str]:
    """A pinned ID left a joined list; or an unlisted ID appears where links are built (D9)."""
    failures = set()
    joined = joined_lists(observation)
    for name, ids in contract.lists.items():
        failures |= {f"concept-missing {name} {cid}" for cid in set(ids) - joined[name]}
    for name, ids in linked_lists(observation).items():
        failures |= {f"concept-unlisted {name} {cid}" for cid in ids - set(contract.concepts)}
    return failures


def coverage_failures(observation: Observation, contract: Contract) -> set[str]:
    """A concept that qualified for a feature at the pin no longer does (M2)."""
    now = coverage_sets(observation)
    return {
        failure_key("coverage", template, concept_id)
        for template, ids in contract.coverage.items()
        for concept_id in set(ids) - now[template]
    }


def request_field_failures(
    observation: Observation, declared: Mapping[str, frozenset[str]]
) -> set[str]:
    """Request fields: a top-level field the pinned frontend sends that the current server's
    request schema doesn't declare, so the server ignores it (audit B1). Keys inside a sent
    map, such as `overrides`, are data and aren't checked."""
    return {
        failure_key("request-field", template, field)
        for template, responses in observation.items()
        for r in responses
        if r.sent is not None
        for field in r.sent.keys() - declared[template]
    }


def cors_failures(observation: Observation) -> set[str]:
    """CORS, the fixed rule: a response the website's origin may not read, or a preflight
    that didn't succeed. Never recorded, because the pinned server had no CORS."""
    return {
        failure_key("cors", template, None)
        for template, responses in observation.items()
        for r in responses
        if r.allow_origin != WEBSITE_ORIGIN or (template in PREFLIGHTS and r.status != 200)
    }


def failure_key(rule: str, template: str, detail: str | None) -> str:
    """'<rule> <template> [<path or instance>]', as check prints it and a waiver matches it."""
    return " ".join([rule, template] + ([detail] if detail is not None else []))


def rule_of(key: str) -> str:
    """The rule a failure key reports: its first token."""
    return key.split(" ", 1)[0]


# ---------------------------------------------------------------------------
# Record and check a whole tree
# ---------------------------------------------------------------------------


def record_tree(tree: Path, pin: str, tools: Iterable[str], js: Mapping[str, str]) -> Contract:
    """Serve the explorer in repo root `tree` and record the contract its responses establish."""
    with serve(tree / EXPLORER) as client:
        schema = classify(_openapi(client))
        observation = observe(client, manifest_concept_ids(client))
    return record(observation, schema, pin, tools, js)


def check_tree(tree: Path, contract: Contract) -> list[str]:
    """Every failure key the explorer in repo root `tree` earns, sorted: the recorded rules,
    plus the fixed Request fields and CORS rules."""
    with serve(tree / EXPLORER) as client:
        declared = request_fields(_openapi(client))
        observation = observe(client, contract.concepts)
        preflights = preflight(client)
    return sorted(
        set(check(observation, contract))
        | request_field_failures(observation, declared)
        | cors_failures({**observation, **preflights})
    )


def _openapi(client: Any) -> dict[str, Any]:
    """The served app's own /openapi.json."""
    response = client.get("/openapi.json")
    response.raise_for_status()
    return response.json()
