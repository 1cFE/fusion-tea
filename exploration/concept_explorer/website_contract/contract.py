"""The website contract: what the website's pinned explorer frontend gets from the API.

The public page 1cf.energy/tools/concepts/ runs a copy of the explorer frontend frozen
at one fusion-tea commit (the pin), against the live API. Record observes the pin's own
server and writes contract.txt; check observes the checkout's server with the same
requests and reports, as failure keys, every change the pinned frontend could break on.
Design: .project/active/explorer-api-contract-gate/design.md.

    contract.py check [--tree ROOT] [--contract FILE] [--waivers FILE]

Module-level imports are standard library only. The server and FastAPI load inside
`serve`, so this file can run before a serving venv exists.
"""

from __future__ import annotations

import argparse
import datetime
import math
import os
import re
import sys
import time
import tomllib
import urllib.parse
from collections import defaultdict
from collections.abc import Callable, Collection, Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# The request list (design Appendix A), read from the pinned frontend at 10f7b9b.
# A template is a method and route; a suffix after ":" names one body shape.
# ---------------------------------------------------------------------------

MANIFEST = "GET /api/manifest"
REGISTRY = "GET /api/taxonomy/registry"
TREE = "GET /api/taxonomy/tree"
COST_LANDSCAPE = "GET /api/cost-landscape"
PARAMETER_INDEX = "GET /api/parameter_index"
CONCEPT = "GET /api/concepts/{id}"
FINDINGS = "GET /api/concepts/{id}/findings"
PARAMETER = "GET /api/parameters/{name}"
STATE_CONCEPT = "POST /api/state:concept"
STATE_COMPARE = "POST /api/state:compare"
SLIDER = "POST /api/compute:slider"
SLIDER_RANGE = "POST /api/compute:slider-range"
TOGGLE = "POST /api/compute:toggle"


@dataclass(frozen=True)
class Request:
    """Where the pinned JavaScript sends a template, and where it derives instances and body."""

    fetch_sites: tuple[str, ...]
    derived_by: tuple[str, ...]


_SLIDER_RULE = (
    "concept_page.js:465-469",
    "concept_page.js:621-625",
    "tornado.js:113-115",
    "tornado.js:452-461",
)

REQUESTS: dict[str, Request] = {
    MANIFEST: Request(
        (
            "index_page.js:247",
            "matrix_page.js:423",
            "cost_landscape_page.js:573",
            "concept_page.js:387",
            "comparison.js:146",
        ),
        (),
    ),
    REGISTRY: Request(
        (
            "matrix_page.js:424",
            "cost_landscape_page.js:574",
            "comparison.js:700",
            "view_categorical.js:82",
        ),
        (),
    ),
    TREE: Request(("matrix_page.js:425", "cost_landscape_page.js:575", "comparison.js:701"), ()),
    COST_LANDSCAPE: Request(("cost_landscape_page.js:576", "comparison.js:702"), ()),
    PARAMETER_INDEX: Request(("concept_page.js:388",), ()),
    CONCEPT: Request(("concept_page.js:386", "comparison.js:153"), ()),
    FINDINGS: Request(("concept_page.js:837",), ("concept_page.js:838-862",)),
    PARAMETER: Request(("concept_page.js:684",), ("concept_page.js:685-698",)),
    STATE_CONCEPT: Request(
        ("concept_page.js:348",), ("concept_page.js:351-355", "concept_page.js:646")
    ),
    STATE_COMPARE: Request(("comparison.js:133",), ("comparison.js:136-141",)),
    SLIDER: Request(("concept_page.js:618",), _SLIDER_RULE),
    SLIDER_RANGE: Request(("concept_page.js:618",), _SLIDER_RULE),
    TOGGLE: Request(
        ("concept_page.js:720",), ("concept_page.js:723-727", "concept_page.js:763-768")
    ),
}

# Lists the pinned frontend joins to the manifest by concept ID. A pinned ID that
# leaves one silently loses its cells, band or bar.
JOINED_LISTS: dict[str, tuple[str, ...]] = {
    "manifest": ("matrix_data.js:54-62",),
    "registry": ("matrix_data.js:47-62", "view_categorical.js:86-88"),
    "tree": ("matrix_data.js:154-162",),
    "cost-landscape": ("cost_landscape_page.js:592-598",),
}

# Lists the pinned frontend builds concept-page links from (D9). An ID the website
# doesn't list becomes a dead link.
LINKED_LISTS: dict[str, tuple[str, ...]] = {
    "manifest": ("matrix_page.js:122", "index_page.js:94", "cost_landscape_page.js:460"),
    "parameters/{name}": ("parameter_card.js:258",),
}

# Plain strings the pinned JavaScript compares to literals (Appendix B, N1). The
# allowed set comes from the JavaScript, not from data: caveat_marker.js:53 tests
# fit_grade === "None", and ontology_palette.js:108-113 is the full grade palette.
# No literal map-key read needs a required-key table at this pin (Appendix B).
_FIT_GRADES = ("High", "Med", "Low", "None")
LITERAL_READS: dict[tuple[str, str], tuple[str, ...]] = {
    (MANIFEST, ".concepts[].fit_grade"): _FIT_GRADES,
    (CONCEPT, ".fit_grade"): _FIT_GRADES,
}

WEBSITE_ORIGIN = "https://1cf.energy"
EXPLORER = Path("exploration/concept_explorer")  # the explorer app, relative to a repo root

# ---------------------------------------------------------------------------
# Observe: serve a tree and send every request the pinned frontend makes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Response:
    instance: str | None  # concept ID or parameter name; None for a single-instance template
    status: int
    body: Any  # parsed JSON when the status is 2xx, else None
    seconds: float
    allow_origin: str | None  # the access-control-allow-origin header, if any

    @property
    def ok(self) -> bool:
        return _is_success(self.status)


def _is_success(status: int) -> bool:
    return 200 <= status < 300


# Template -> its responses, in request order. A template that was sent zero times
# has an empty list; a skipped template has no entry.
Observation = dict[str, list[Response]]


@contextmanager
def serve(base_dir: Path) -> Iterator[Any]:
    """Run the explorer app rooted at `base_dir` in a TestClient, without the compute warm-up."""
    os.environ["EXPLORER_SKIP_WARMUP"] = "1"
    from fastapi.testclient import TestClient

    from exploration.concept_explorer.server import create_app

    with TestClient(create_app(base_dir=base_dir), raise_server_exceptions=False) as client:
        yield client


def manifest_concept_ids(client: Any) -> list[str]:
    """The concept IDs the served manifest lists, sorted."""
    response = client.get("/api/manifest")
    response.raise_for_status()
    return sorted(_strings_at([response.json()], (), _is_concept_id))


def observe(client: Any, concept_ids: Sequence[str], skip: Collection[str] = ()) -> Observation:
    """Send every request the pinned frontend makes, as the pinned JavaScript derives them.

    Concept-keyed requests go to `concept_ids` in order. Parameter names, slider bodies
    and which concepts get compute requests come from the current responses. Templates
    in `skip` are not sent.
    """
    observation: Observation = {template: [] for template in REQUESTS if template not in skip}
    origin = {"Origin": WEBSITE_ORIGIN}

    def send(template: str, instance: str | None, call: Callable[[], Any]) -> Any:
        if template not in observation:
            return None
        response, seconds = _timed(call)
        body = response.json() if _is_success(response.status_code) else None
        observation[template].append(
            Response(instance, response.status_code, body, seconds, _allow_origin(response))
        )
        return body

    def get(template: str, instance: str | None, url: str) -> Any:
        return send(template, instance, lambda: client.get(url, headers=origin))

    def post(template: str, instance: str | None, body: dict[str, Any]) -> None:
        send(template, instance, lambda: client.post(_route(template), json=body, headers=origin))

    for template in (MANIFEST, REGISTRY, TREE, COST_LANDSCAPE):
        get(template, None, _route(template))
    index = get(PARAMETER_INDEX, None, _route(PARAMETER_INDEX))
    concepts: dict[str, dict[str, Any]] = {}
    for concept_id in concept_ids:
        body = get(CONCEPT, concept_id, f"/api/concepts/{concept_id}")
        if isinstance(body, dict):
            concepts[concept_id] = body
    for concept_id in concept_ids:
        get(FINDINGS, concept_id, f"/api/concepts/{concept_id}/findings")
    for name in _parameter_names(index):
        get(PARAMETER, name, "/api/parameters/" + urllib.parse.quote(name, safe="!'()*"))

    sliders = {cid: page_sliders(concepts.get(cid, {})) for cid in concept_ids}
    post(
        STATE_CONCEPT,
        None,
        {
            "current_concept_id": concept_ids[0],
            "slider_overrides": sliders[concept_ids[0]],
            "comparison_set": [],
        },
    )
    post(
        STATE_COMPARE,
        None,
        {
            "current_concept_id": None,
            "slider_overrides": {},
            "comparison_set": list(concept_ids[:2]),
            "timestamp": "",
        },
    )

    # Compute requests are grouped by concept so each concept module loads once.
    range_concept = next((cid for cid in concept_ids if sliders[cid]), None)
    for concept_id in concept_ids:
        concept = concepts.get(concept_id, {})
        if sliders[concept_id]:
            body = _compute_body(concept_id, sliders[concept_id], apply_overrides=True)
            post(SLIDER, concept_id, body)
        if concept_id == range_concept:
            at_high = _first_at_high(concept, sliders[concept_id])
            post(SLIDER_RANGE, None, _compute_body(concept_id, at_high, apply_overrides=True))
        if sends_toggle(concept):
            post(TOGGLE, concept_id, _compute_body(concept_id, {}, apply_overrides=False))
    return observation


def _timed(call: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[Any, float]:
    """`call(*args, **kwargs)` and the seconds it took."""
    start = time.perf_counter()
    result = call(*args, **kwargs)
    return result, time.perf_counter() - start


def _allow_origin(response: Any) -> str | None:
    return response.headers.get("access-control-allow-origin")


def page_sliders(concept: Mapping[str, Any]) -> dict[str, float]:
    """The overrides a concept page's sliders send at baseline; empty without live sliders.

    Live sliders need a costingfe concept with sensitivities (concept_page.js:465-469).
    They cover the top 15 parameters by |elasticity| whose metadata range is finite with
    high > low, each at its finite baseline or else range[0] (tornado.js:113-115,452-461).
    """
    sensitivities = (concept.get("cost_model") or {}).get("sensitivities")
    if (
        concept.get("model_type") != "costingfe"
        or not concept.get("has_sensitivities")
        or sensitivities is None
    ):
        return {}
    # Like the JavaScript's object merge: a financial entry replaces an engineering
    # entry of the same name but keeps its position.
    merged = {**(sensitivities.get("engineering") or {}), **(sensitivities.get("financial") or {})}
    # A non-number elasticity is a Shape failure; sort it last rather than stop here.
    top = sorted(merged, key=lambda name: -_magnitude((merged[name] or {}).get("elasticity")))[:15]
    metadata = concept.get("parameter_metadata") or {}
    sliders: dict[str, float] = {}
    for name in top:
        meta = metadata.get(name) or {}
        bounds = meta.get("range")
        if (
            isinstance(bounds, list)
            and len(bounds) == 2
            and all(map(_is_finite, bounds))
            and bounds[1] > bounds[0]
        ):
            sliders[name] = meta["baseline"] if _is_finite(meta.get("baseline")) else bounds[0]
    return sliders


def sends_toggle(concept: Mapping[str, Any]) -> bool:
    """Whether the concept page's analyst-override toggle is live (concept_page.js:763-768)."""
    count = concept.get("analyst_override_count")
    return concept.get("model_type") == "costingfe" and _is_finite(count) and count > 0


def _first_at_high(concept: Mapping[str, Any], sliders: Mapping[str, float]) -> dict[str, float]:
    """`sliders` with its first parameter moved to the top of its range (m8)."""
    first = next(iter(sliders))
    return {**sliders, first: concept["parameter_metadata"][first]["range"][1]}


def _compute_body(
    concept_id: str, overrides: dict[str, float], *, apply_overrides: bool
) -> dict[str, Any]:
    return {
        "concept_id": concept_id,
        "overrides": overrides,
        "apply_analyst_overrides": apply_overrides,
    }


def _parameter_names(index: Any) -> list[str]:
    parameters = index.get("parameters") if isinstance(index, dict) else None
    return list(parameters) if isinstance(parameters, dict) else []


def _route(template: str) -> str:
    """'POST /api/compute:slider' -> '/api/compute'."""
    return template.split(" ")[1].split(":")[0]


def _is_finite(value: Any) -> bool:
    """JavaScript's Number.isFinite: a real number, never a boolean."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _magnitude(value: Any) -> float:
    return abs(value) if _is_finite(value) else 0.0


# ---------------------------------------------------------------------------
# Shapes: flatten JSON bodies to "path -> set of kinds"
# ---------------------------------------------------------------------------

KINDS = ("object", "array", "string", "number", "boolean", "null", "absent", "empty")
VACANT = frozenset({"null", "absent", "empty"})  # kinds that carry no value
_PATH_BREAKERS = re.compile(r"[\s.\[\]{}]")


def flatten(bodies: Iterable[Any], map_paths: Collection[str]) -> dict[str, set[str]]:
    """Path -> the kinds seen there, unioned over `bodies`, array elements and map values.

    Objects at `map_paths` are maps: their values share one `{*}` path, and an empty map
    is `empty`. Every other object is a record, whose fields get their own paths. A field
    is `absent` where an object at its record path lacks it; a path under a parent never
    observed as an object is not observed at all.
    """
    kinds: dict[str, set[str]] = defaultdict(set)
    objects_seen: dict[str, int] = defaultdict(int)
    fields_seen: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for body in bodies:
        for path, value in _nodes(body, ".", map_paths):
            is_map = path in map_paths
            kinds[path].add(_kind(value, is_map))
            if isinstance(value, dict) and not is_map:
                objects_seen[path] += 1
                for key in value:
                    fields_seen[path][key] += 1
    for path, seen in objects_seen.items():
        for key, count in fields_seen[path].items():
            if count < seen:
                kinds[_field(path, key)].add("absent")
    return dict(kinds)


def _nodes(value: Any, path: str, map_paths: Collection[str]) -> Iterator[tuple[str, Any]]:
    """Every (path, value) in `value`, depth first, starting with `value` itself."""
    yield path, value
    if isinstance(value, dict):
        if path in map_paths:
            children = ((path + "{*}", child) for child in value.values())
        else:
            children = ((_field(path, key), child) for key, child in value.items())
    elif isinstance(value, list):
        children = ((path + "[]", child) for child in value)
    else:
        return
    for child_path, child in children:
        yield from _nodes(child, child_path, map_paths)


def _field(path: str, key: str) -> str:
    if _PATH_BREAKERS.search(key):
        raise ValueError(
            f"record key {key!r} under {path} can't be written as a path; "
            "a data-driven key like this most likely means a map was classified as a record"
        )
    return f".{key}" if path == "." else f"{path}.{key}"


def _kind(value: Any, is_map: bool) -> str:
    if isinstance(value, dict):
        return "empty" if is_map and not value else "object"
    if isinstance(value, list):
        return "array" if value else "empty"
    if isinstance(value, bool):  # before int: bool is an int subclass
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if value is None:
        return "null"
    raise TypeError(f"not a JSON value: {value!r}")


def _strings_at(
    bodies: Iterable[Any], map_paths: Collection[str], wanted: Callable[[str], bool]
) -> set[str]:
    """Every string value at a path `wanted` accepts."""
    return {
        value
        for body in bodies
        for path, value in _nodes(body, ".", map_paths)
        if isinstance(value, str) and wanted(path)
    }


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
            enums[name] = tuple(_line_value(str(value)) for value in node["enum"])
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
            walk(template, child, _field(path, key))
        for child in [node["items"]] if "items" in node else node.get("prefixItems", []):
            walk(template, child, path + "[]")

    routes = {
        _route_pattern(route): operations for route, operations in openapi.get("paths", {}).items()
    }
    for template in REQUESTS:
        method = template.split(" ")[0].lower()
        operation = routes.get(_route_pattern(_route(template)), {}).get(method)
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


def _route_pattern(route: str) -> str:
    """'/api/concepts/{concept_id}' and '/api/concepts/{id}' -> '/api/concepts/{}'."""
    return re.sub(r"\{[^}]*\}", "{}", route)


# ---------------------------------------------------------------------------
# The contract and its text form, contract.txt
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Contract:
    pin: str
    tools: tuple[str, ...]  # record-mode test tools, "dist==version"
    js: Mapping[str, str]  # cited JavaScript file -> git blob SHA at the pin
    concepts: tuple[str, ...]  # the pinned manifest's concept IDs
    lists: Mapping[str, tuple[str, ...]]  # joined list name -> pinned concept IDs
    coverage: Mapping[str, tuple[str, ...]]  # template -> concepts that qualified at the pin
    status: Mapping[str, tuple[int, ...]]  # template -> statuses seen at the pin
    enums: Mapping[str, tuple[str, ...]]  # enum name -> values
    literals: Mapping[tuple[str, str], tuple[str, ...]]  # (template, path) -> allowed values
    maps: frozenset[tuple[str, str]]  # (template, path) of every map object
    shapes: Mapping[tuple[str, str], frozenset[str]]  # (template, path) -> kinds seen at the pin


def record(
    observation: Observation, schema: Schema, pin: str, tools: Iterable[str], js: Mapping[str, str]
) -> Contract:
    """The contract an observation of the pinned server establishes."""
    maps = frozenset((template, path) for template, path in schema.maps if template in observation)
    shapes = shapes_of(observation, maps, schema.enum_paths)
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
        maps=maps,
        shapes=shapes,
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
        for path, kinds in flatten(_bodies(responses), map_paths).items():
            enum_name = enum_paths.get((template, path))
            if enum_name is not None and "string" in kinds:
                kinds = (kinds - {"string"}) | {f"enum:{enum_name}"}
            shapes[(template, path)] = frozenset(kinds)
    return shapes


def joined_lists(observation: Observation) -> dict[str, set[str]]:
    """The concept IDs in each list the pinned frontend joins to the manifest (JOINED_LISTS)."""
    return {
        "manifest": _ids(observation, MANIFEST, _is_concept_id),
        "registry": _ids(observation, REGISTRY, _is_concept_id),
        "tree": _ids(observation, TREE, lambda path: path.endswith(".concepts[]")),
        "cost-landscape": _ids(observation, COST_LANDSCAPE, _is_concept_id),
    }


def linked_lists(observation: Observation) -> dict[str, set[str]]:
    """The concept IDs in each list the pinned frontend builds concept links from (LINKED_LISTS)."""
    return {
        "manifest": _ids(observation, MANIFEST, _is_concept_id),
        "parameters/{name}": _ids(observation, PARAMETER, _is_concept_id),
    }


def _ids(observation: Observation, template: str, wanted: Callable[[str], bool]) -> set[str]:
    """String values at the paths `wanted` accepts, in the template's 2xx bodies (no maps)."""
    return _strings_at(_bodies(observation.get(template, [])), (), wanted)


def _is_concept_id(path: str) -> bool:
    return path == ".concepts[].concept_id"


def coverage_sets(observation: Observation) -> dict[str, set[str]]:
    """For each concept-keyed template, the concepts the pinned frontend gets a feature from.

    Findings: the response carries HTML the page shows (concept_page.js:844-857).
    Slider and toggle: the concept page sends that compute request.
    """
    concepts = {
        r.instance: r.body
        for r in observation.get(CONCEPT, [])
        if r.ok and isinstance(r.body, dict)
    }
    return {
        FINDINGS: {
            r.instance
            for r in observation.get(FINDINGS, [])
            if r.ok
            and isinstance(r.body, dict)
            and (r.body.get("exec_summary_html") or r.body.get("analysis_html"))
        },
        SLIDER: {concept_id for concept_id, body in concepts.items() if page_sliders(body)},
        TOGGLE: {concept_id for concept_id, body in concepts.items() if sends_toggle(body)},
    }


def _bodies(responses: Iterable[Response]) -> list[Any]:
    return [r.body for r in responses if r.ok]


def render(contract: Contract) -> str:
    """contract.txt: a fixed header order, each group sorted, then one sorted line per shape."""
    pin, concepts = contract.pin, sorted(contract.concepts)
    lines = [
        f"# Recorded from fusion-tea {pin}. Do not edit; clear false blocks in waivers.toml.",
        f"# Regenerate: exploration/concept_explorer/website_contract/gate.sh record {pin}",
        f"pin {pin}",
        " ".join(["tools", *sorted(contract.tools)]),
        *sorted(f"js {path} {sha}" for path, sha in contract.js.items()),
        " ".join(["concepts", *_concept_ids(concepts)]),
        *sorted(
            " ".join(
                ["list", name, *(["="] if sorted(ids) == concepts else _concept_ids(sorted(ids)))]
            )
            for name, ids in contract.lists.items()
        ),
        *sorted(
            " ".join(["coverage", t, *_concept_ids(sorted(ids))])
            for t, ids in contract.coverage.items()
        ),
        *sorted(
            " ".join(["status", t, *map(str, sorted(codes))])
            for t, codes in contract.status.items()
        ),
        *sorted(
            f"enum {name} {_line_value(v)}"
            for name, values in contract.enums.items()
            for v in values
        ),
        *sorted(
            f"literal {t} {p} {_line_value(v)}"
            for (t, p), values in contract.literals.items()
            for v in values
        ),
        *sorted(f"map {t} {p}" for t, p in contract.maps),
        *sorted(f"{t} {p} {_render_kinds(kinds)}" for (t, p), kinds in contract.shapes.items()),
    ]
    return "\n".join(lines) + "\n"


def parse(text: str) -> Contract:
    """Read contract.txt, failing on any line it doesn't recognize."""
    pin = None
    tools: list[str] = []
    js: dict[str, str] = {}
    concepts: list[str] = []
    lists: dict[str, list[str] | None] = {}  # None: "=", the contract concepts
    coverage: dict[str, tuple[str, ...]] = {}
    status: dict[str, tuple[int, ...]] = {}
    enums: dict[str, list[str]] = defaultdict(list)
    literals: dict[tuple[str, str], list[str]] = defaultdict(list)
    maps: set[tuple[str, str]] = set()
    shapes: dict[tuple[str, str], frozenset[str]] = {}
    for number, line in enumerate(text.splitlines(), 1):
        word, _, rest = line.partition(" ")
        try:
            if word.startswith("#"):
                continue
            if word == "pin":
                pin = rest
            elif word == "tools":
                tools = rest.split()
            elif word == "js":
                path, sha = rest.split(" ")
                js[path] = sha
            elif word == "concepts":
                concepts = rest.split()
            elif word == "list":
                name, *ids = rest.split(" ")
                lists[name] = None if ids == ["="] else ids
            elif word == "coverage":
                method, route, *ids = rest.split(" ")
                coverage[f"{method} {route}"] = tuple(ids)
            elif word == "status":
                method, route, *codes = rest.split(" ")
                status[f"{method} {route}"] = tuple(int(code) for code in codes)
            elif word == "enum":
                name, value = rest.split(" ", 1)
                enums[name].append(value)
            elif word == "literal":
                method, route, path, value = rest.split(" ", 3)
                literals[(f"{method} {route}", path)].append(value)
            elif word == "map":
                method, route, path = rest.split(" ")
                maps.add((f"{method} {route}", path))
            elif word in ("GET", "POST"):
                route, path, kinds = rest.split(" ")
                shapes[(f"{word} {route}", path)] = _parse_kinds(kinds)
            else:
                raise ValueError(f"unknown line kind {word!r}")
        except ValueError as error:
            raise ValueError(f"contract.txt line {number}: {line!r}: {error}") from error
    if pin is None:
        raise ValueError("contract.txt has no pin line")
    return Contract(
        pin=pin,
        tools=tuple(tools),
        js=js,
        concepts=tuple(concepts),
        lists={name: tuple(concepts if ids is None else ids) for name, ids in lists.items()},
        coverage=coverage,
        status=status,
        enums={name: tuple(values) for name, values in enums.items()},
        literals={key: tuple(values) for key, values in literals.items()},
        maps=frozenset(maps),
        shapes=shapes,
    )


def _concept_ids(ids: Iterable[str]) -> list[str]:
    ids = list(ids)
    for concept_id in ids:
        if not concept_id or _PATH_BREAKERS.search(concept_id):
            raise ValueError(f"concept ID {concept_id!r} can't be written as one contract token")
    return ids


def _line_value(value: str) -> str:
    """An enum or literal value, written as the rest of its line."""
    if not value or value != value.strip() or "\n" in value:
        raise ValueError(f"value {value!r} can't be written as the rest of a contract line")
    return value


def _render_kinds(kinds: Collection[str]) -> str:
    return ",".join(
        sorted(kinds, key=lambda kind: KINDS.index("string" if kind.startswith("enum:") else kind))
    )


def _parse_kinds(text: str) -> frozenset[str]:
    kinds = frozenset(text.split(","))
    unknown = {kind for kind in kinds if kind not in KINDS and not kind.startswith("enum:")}
    if unknown:
        raise ValueError(f"unknown kinds {sorted(unknown)}")
    return kinds


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
            _key("status", template, r.instance) for r in responses if r.status not in codes
        }
        if 200 in codes and not any(r.status == 200 for r in responses):
            failures.add(_key("status", template, None))
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
                failures.add(_key("unpopulated", template, path))
        elif kinds - pinned:
            failures.add(_key("shape", template, path))
    return failures


def value_failures(observation: Observation, contract: Contract) -> set[str]:
    """Enum: a value outside the pinned enum. Literal: a value outside the cited allowed set."""
    rules = [("enum", key, contract.enums[name]) for key, name in _enum_paths(contract).items()]
    rules += [("literal", key, values) for key, values in contract.literals.items()]
    failures = set()
    for rule, (template, path), allowed in rules:
        map_paths = {p for t, p in contract.maps if t == template}
        bodies = _bodies(observation.get(template, []))
        values = _strings_at(bodies, map_paths, lambda p: p == path)
        if values - set(allowed):
            failures.add(_key(rule, template, path))
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
        _key("coverage", template, concept_id)
        for template, ids in contract.coverage.items()
        for concept_id in set(ids) - now[template]
    }


def _key(rule: str, template: str, detail: str | None) -> str:
    return " ".join([rule, template] + ([detail] if detail is not None else []))


def _rule(key: str) -> str:
    """The rule a failure key reports: its first token."""
    return key.split(" ", 1)[0]


# ---------------------------------------------------------------------------
# CORS: the fixed rule (rules table). Checked on every response, never recorded,
# because the pinned server had no CORS.
# ---------------------------------------------------------------------------

PREFLIGHTS = ("OPTIONS /api/compute", "OPTIONS /api/state")


def preflight(client: Any) -> Observation:
    """Send the preflight a browser sends before each of the website's JSON POSTs."""
    headers = {
        "Origin": WEBSITE_ORIGIN,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
    }
    observation: Observation = {}
    for template in PREFLIGHTS:
        response, seconds = _timed(client.options, _route(template), headers=headers)
        observation[template] = [
            Response(None, response.status_code, None, seconds, _allow_origin(response))
        ]
    return observation


def cors_failures(observation: Observation) -> set[str]:
    """A response the website's origin may not read, or a preflight that didn't succeed."""
    return {
        _key("cors", template, None)
        for template, responses in observation.items()
        for r in responses
        if r.allow_origin != WEBSITE_ORIGIN or (template in PREFLIGHTS and r.status != 200)
    }


# ---------------------------------------------------------------------------
# Record and check a whole tree
# ---------------------------------------------------------------------------


def record_tree(tree: Path, pin: str, tools: Iterable[str], js: Mapping[str, str]) -> Contract:
    """Serve the explorer in repo root `tree` and record the contract its responses establish."""
    with serve(tree / EXPLORER) as client:
        schema = classify(client.get("/openapi.json").json())
        observation = observe(client, manifest_concept_ids(client))
    return record(observation, schema, pin, tools, js)


def check_tree(tree: Path, contract: Contract) -> list[str]:
    """Every failure key the explorer in repo root `tree` earns, CORS included, sorted."""
    with serve(tree / EXPLORER) as client:
        observation = observe(client, contract.concepts)
        preflights = preflight(client)
    return sorted(set(check(observation, contract)) | cors_failures({**observation, **preflights}))


# ---------------------------------------------------------------------------
# Waivers (D7, Appendix E): hand-written; each clears the failure keys its match names
# ---------------------------------------------------------------------------

UNWAIVABLE = frozenset({"cors"})  # rules whose keys are printed but never matched (M4)
_WAIVER_FIELDS = ("match", "reason", "evidence", "date")
# An unpopulated waiver must show the pinned JavaScript was read: a file.js:N cite of
# the JS that reads the path, or "unread:" and the search terms that found no reader
# (orchestrator, 2026-10-08, replacing N4's cite-only wording).
_JS_CITE = re.compile(r"\b[\w-]+\.js:\d+")
_UNREAD = re.compile(r"\bunread:\s*\S")
_MATCH_PARTS = re.compile(r"([ .])")  # a key's separators: tokens by spaces, paths by dots


class WaiverError(ValueError):
    """waivers.toml breaks the waiver grammar."""


@dataclass(frozen=True)
class Waiver:
    match: str
    reason: str
    evidence: str
    date: datetime.date


def load_waivers(path: Path) -> list[Waiver]:
    """Read waivers.toml, raising WaiverError on anything outside the grammar."""
    try:
        document = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise WaiverError(str(error)) from error
    entries = document.get("waiver", [])
    if set(document) - {"waiver"} or not isinstance(entries, list):
        raise WaiverError("write each waiver as a [[waiver]] table, and nothing else")
    return [_waiver(entry, f"waiver {number}") for number, entry in enumerate(entries, 1)]


def _waiver(entry: Mapping[str, Any], where: str) -> Waiver:
    if set(entry) != set(_WAIVER_FIELDS):
        raise WaiverError(
            f"{where}: needs exactly the fields {', '.join(_WAIVER_FIELDS)}, "
            f"has {', '.join(sorted(entry)) or 'none'}"
        )
    for field in ("match", "reason", "evidence"):
        if not isinstance(entry[field], str) or not entry[field].strip():
            raise WaiverError(f"{where}: {field} must be a non-empty string")
    if not isinstance(entry["date"], datetime.date):
        raise WaiverError(f"{where}: date must be a TOML date, like 2026-10-08")
    waiver = Waiver(**entry)
    _check_match(waiver.match, where)
    if waiver.match.startswith("unpopulated ") and not (
        _JS_CITE.search(waiver.evidence) or _UNREAD.search(waiver.evidence)
    ):
        raise WaiverError(
            f"{where}: an unpopulated waiver's evidence must cite the JavaScript that reads "
            "the path (file.js:N), or say 'unread:' and the search terms that found no reader"
        )
    return waiver


def _check_match(match: str, where: str) -> None:
    """A match is a failure key, with `*` standing for one whole token or path segment."""
    tokens = match.split(" ")
    if "" in tokens:
        raise WaiverError(f"{where}: match {match!r} must be tokens separated by single spaces")
    if "*" in tokens[0]:
        raise WaiverError(f"{where}: match {match!r} must name its rule; * can't stand for it")
    for part in _MATCH_PARTS.split(match):
        if "*" in part.replace("{*}", "") and part != "*":
            raise WaiverError(f"{where}: * must be a whole token or path segment, not {part!r}")


def waiver_matches(match: str, key: str) -> bool:
    """Whether a waiver's match names `key`: equal parts, each `*` standing for any one."""
    pattern = "".join(
        "[^ .]+" if part == "*" else re.escape(part) for part in _MATCH_PARTS.split(match)
    )
    return re.fullmatch(pattern, key) is not None


@dataclass(frozen=True)
class Verdict:
    failing: tuple[str, ...]  # failure keys no waiver clears
    waived: tuple[str, ...]  # failure keys a waiver clears
    stale: tuple[Waiver, ...]  # waivers that match no waivable failure


def apply_waivers(failures: Sequence[str], waivers: Sequence[Waiver]) -> Verdict:
    """Split failures into waived and failing; CORS keys are never waived."""
    waivable = [key for key in failures if _rule(key) not in UNWAIVABLE]
    waived = {key for key in waivable if any(waiver_matches(w.match, key) for w in waivers)}
    return Verdict(
        failing=tuple(key for key in failures if key not in waived),
        waived=tuple(key for key in failures if key in waived),
        stale=tuple(w for w in waivers if not any(waiver_matches(w.match, k) for k in waivable)),
    )


# ---------------------------------------------------------------------------
# Command line (gate.sh runs `contract.py check` on every push)
# ---------------------------------------------------------------------------

EXIT_FAILED = 1  # an unwaived failure
EXIT_CONFIG = 2  # waivers.toml breaks the grammar
_HERE = Path(__file__).resolve().parent

# What each rule's failure means, printed under the keys for a reader without the code.
_RULE_MEANINGS = {
    "status": "a request the website sends no longer gets the status it got at the pin",
    "shape": "a response path now carries a JSON kind the website never received there",
    "unpopulated": "a path the pin only sent empty now carries data; read the pinned JS first",
    "enum": "a value outside the enum the pinned website knows",
    "literal": "a value outside the set the pinned JavaScript compares against",
    "concept-missing": "a website concept left a list the website joins by concept ID",
    "concept-unlisted": "a concept the website doesn't list appears where it builds links",
    "coverage": "a concept no longer gets a feature (findings, sliders, toggle) it had at the pin",
    "cors": "the website's origin may not read this response; fix the allowlist, never waive",
}


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="contract.py", description=__doc__.split("\n")[0])
    commands = parser.add_subparsers(required=True)
    check_parser = commands.add_parser("check", help="check a checkout against contract.txt")
    check_parser.add_argument("--tree", type=Path, default=_HERE.parents[2], help="repo root")
    check_parser.add_argument("--contract", type=Path, default=_HERE / "contract.txt")
    check_parser.add_argument("--waivers", type=Path, default=_HERE / "waivers.toml")
    check_parser.set_defaults(command=_check_command)
    args = parser.parse_args(argv)
    return args.command(args)


def _check_command(args: argparse.Namespace) -> int:
    contract = parse(args.contract.read_text(encoding="utf-8"))
    try:
        waivers = load_waivers(args.waivers)
    except WaiverError as error:
        print(f"configuration error in {args.waivers}: {error}")
        return EXIT_CONFIG
    tree = args.tree.resolve()
    sys.path.insert(0, str(tree))  # import the server from the tree under check
    verdict = apply_waivers(check_tree(tree, contract), waivers)
    print(report(verdict, contract.pin))
    return EXIT_FAILED if verdict.failing else 0


def report(verdict: Verdict, pin: str) -> str:
    """One line per failure key, waived key and stale waiver, then what the rules mean."""
    lines = [f"FAIL {key}" for key in verdict.failing]
    lines += [f"WAIVED {key}" for key in verdict.waived]
    lines += [f"STALE {w.match}" for w in verdict.stale]
    rules = sorted({_rule(key) for key in verdict.failing})
    if rules:
        lines += ["", "Each key is the rule, the request, then a path or instance. Rules failing:"]
        lines += [f"  {rule}: {_RULE_MEANINGS[rule]}" for rule in rules]
        lines += [
            "A false block clears with a [[waiver]] in "
            "exploration/concept_explorer/website_contract/waivers.toml (RUNBOOK, Deploy gate)."
        ]
    if verdict.stale:
        lines.append("Delete each STALE waiver: it matches no failure any more.")
    lines.append(
        f"website contract (pin {pin[:9]}): {len(verdict.failing)} failing, "
        f"{len(verdict.waived)} waived, {len(verdict.stale)} stale waivers"
    )
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
