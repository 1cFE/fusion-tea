"""What the website's pinned explorer frontend requests, and how it reads the responses.

The request list (design Appendix A) and its cite tables, read from the pinned frontend
at 10f7b9b; `observe`, which serves a tree and sends every request the way the pinned
JavaScript derives it; and the concept lists and features the frontend takes from the
responses. Module-level imports are standard library only: the server and FastAPI load
inside `serve`, so the gate can run before a serving venv exists.
"""

from __future__ import annotations

import math
import os
import urllib.parse
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from json_shapes import strings_at

# ---------------------------------------------------------------------------
# The request list. A template is a method and route; a suffix after ":" names one
# body shape.
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
# allowed set comes from the JavaScript, not from data: the grade palette (USAGE_SITES).
# No literal map-key read needs a required-key table at this pin (Appendix B).
_FIT_GRADES = ("High", "Med", "Low", "None")
LITERAL_READS: dict[tuple[str, str], tuple[str, ...]] = {
    (MANIFEST, ".concepts[].fit_grade"): _FIT_GRADES,
    (CONCEPT, ".fit_grade"): _FIT_GRADES,
}

# Where the pinned JavaScript uses the maps and the literal values (Appendix B). No rule
# reads these; they are cited so recording tracks these files' blob SHAs too (M5, N6).
USAGE_SITES = (
    "tornado.js:99",  # sensitivities.engineering iterated
    "tornado.js:105",  # sensitivities.financial iterated
    "tornado.js:101-108",  # parameter_metadata: guarded lookup by name
    "tornado.js:135-136",  # parameter_index.parameters: guarded lookup by name
    "view_sensitivity.js:98",  # compare page: sensitivity maps iterated
    "view_sensitivity.js:101",
    "view_sensitivity.js:194",  # compare page: parameter_metadata iterated
    "cas_breakdown.js:20-24",  # CAS22_ORDER, the fixed codes read behind an existence check
    "cas_breakdown.js:221-229",  # cas22_detail iterated
    "caveat_marker.js:53",  # fit_grade === "None"
    "ontology_palette.js:108-113",  # the Archetype Fit palette: High, Med, Low, None
    "ontology_palette.js:161",  # the matrix facet that uses it
)

WEBSITE_ORIGIN = "https://1cf.energy"
# Relative to a repo root.
EXPLORER = Path("exploration/concept_explorer")
STATIC_JS = EXPLORER / "static" / "js"  # where every cite above resolves

# ---------------------------------------------------------------------------
# Observe: serve a tree and send every request the pinned frontend makes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Response:
    instance: str | None  # concept ID or parameter name; None for a single-instance template
    sent: Mapping[str, Any] | None  # the JSON body the request carried; None for a GET or preflight
    status: int
    body: Any  # parsed JSON when the status is 2xx, else None
    allow_origin: str | None  # the access-control-allow-origin header, if any

    @property
    def ok(self) -> bool:
        return _is_success(self.status)


def _is_success(status: int) -> bool:
    return 200 <= status < 300


# Template -> its responses, in request order. A template that was sent zero times
# has an empty list.
Observation = dict[str, list[Response]]


@contextmanager
def serve(base_dir: Path) -> Iterator[Any]:
    """Run the explorer app rooted at `base_dir` in a TestClient, without the compute warm-up."""
    os.environ["EXPLORER_SKIP_WARMUP"] = "1"
    from fastapi.testclient import TestClient

    from exploration.concept_explorer.server import create_app

    with TestClient(create_app(base_dir=base_dir), raise_server_exceptions=False) as client:
        yield client


def observe(client: Any, concept_ids: Sequence[str]) -> Observation:
    """Send every request the pinned frontend makes, as the pinned JavaScript derives them.

    Concept-keyed requests go to `concept_ids` in order. Parameter names, slider bodies
    and which concepts get compute requests come from the current responses.
    """
    observation: Observation = {template: [] for template in REQUESTS}
    origin = {"Origin": WEBSITE_ORIGIN}

    def send(
        template: str, instance: str | None, sent: Mapping[str, Any] | None, call: Callable[[], Any]
    ) -> Any:
        response = call()
        body = response.json() if _is_success(response.status_code) else None
        observation[template].append(
            Response(instance, sent, response.status_code, body, _allow_origin(response))
        )
        return body

    def get(template: str, instance: str | None, url: str) -> Any:
        return send(template, instance, None, lambda: client.get(url, headers=origin))

    def post(template: str, instance: str | None, body: dict[str, Any]) -> None:
        url = route(template)
        send(template, instance, body, lambda: client.post(url, json=body, headers=origin))

    for template in (MANIFEST, REGISTRY, TREE, COST_LANDSCAPE):
        get(template, None, route(template))
    index = get(PARAMETER_INDEX, None, route(PARAMETER_INDEX))
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


# The preflights a browser sends before each of the website's JSON POSTs. Only the CORS
# rule judges them, because the pinned server had no CORS.
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
        response = client.options(route(template), headers=headers)
        observation[template] = [
            Response(None, None, response.status_code, None, _allow_origin(response))
        ]
    return observation


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


def route(template: str) -> str:
    """'POST /api/compute:slider' -> '/api/compute'."""
    return template.split(" ")[1].split(":")[0]


def _is_finite(value: Any) -> bool:
    """JavaScript's Number.isFinite: a real number, never a boolean."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _magnitude(value: Any) -> float:
    return abs(value) if _is_finite(value) else 0.0


# ---------------------------------------------------------------------------
# What the frontend takes from the responses: concept lists and features
# ---------------------------------------------------------------------------


def bodies(responses: Iterable[Response]) -> list[Any]:
    """The parsed bodies of the 2xx responses."""
    return [r.body for r in responses if r.ok]


def manifest_concept_ids(client: Any) -> list[str]:
    """The concept IDs the served manifest lists, sorted."""
    response = client.get("/api/manifest")
    response.raise_for_status()
    return sorted(strings_at([response.json()], (), _is_concept_id))


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
    return strings_at(bodies(observation.get(template, [])), (), wanted)


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
