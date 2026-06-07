"""FastAPI server for the Fusion TEA Concept Explorer.

Start with:
    uv run python exploration/concept_explorer/server.py [--port PORT]

The server:
- Loads all data/*.json into memory on startup (fails loudly if data/ is absent).
- Renders Jinja2 page templates to dist/ on startup (skips templates not yet written).
- Serves static/ at /static and pre-rendered dist/ at page routes.
- Exposes typed data API endpoints backed by the in-memory loaded models.
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import inspect
import json
import sys
import threading
import types
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, redirect_stdout
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import lru_cache
from io import StringIO
from pathlib import Path
from typing import Any

# Ensure project root is on sys.path so fully-qualified package imports work
# when the script is run directly (uv run python exploration/.../server.py)
_PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import uvicorn  # noqa: E402
from fastapi import Depends, FastAPI, HTTPException, Request  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from jinja2 import Environment, FileSystemLoader, TemplateNotFound  # noqa: E402

from exploration.concept_explorer.models import (  # noqa: E402
    ComputeRequest,
    ConceptData,
    ConceptManifest,
    CostModelData,
    ExplorerState,
    ParameterIndex,
    ParameterIndexEntry,
    build_manifest,
    build_parameter_index,
    load_omit_list,
)
from exploration.concept_explorer.similarity import (  # noqa: E402
    ConceptSimilarityReport,
    ConstellationData,
    SimilarityResult,
    compare_pair,
    compute_constellation,
    compute_similarity_matrix,
    explain_difference,
    find_nearest,
)
from exploration.concept_explorer.taxonomy_models import (  # noqa: E402
    ConceptRegistry,
    ConceptTaxonomy,
    prune_decision_tree,
)

BASE_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# Parameter sets for model.forward() re-invocation (compute endpoint)
# ---------------------------------------------------------------------------


def _derive_forward_named() -> frozenset[str]:
    """Extract named parameters from CostModel.forward() via introspection.

    Falls back to a hardcoded set if costingfe is not installed (e.g. in test
    environments that don't depend on it).
    """
    try:
        from costingfe.model import CostModel

        sig = inspect.signature(CostModel.forward)
        skip = {"self", "cost_overrides"}
        return frozenset(
            name
            for name, param in sig.parameters.items()
            if name not in skip
            and param.kind
            not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
        )
    except ImportError:
        return frozenset(
            {
                "net_electric_mw",
                "availability",
                "lifetime_yr",
                "n_mod",
                "construction_time_yr",
                "interest_rate",
                "inflation_rate",
                "noak",
            }
        )


# Named args that forward() takes explicitly (not via **overrides)
_FORWARD_NAMED = _derive_forward_named()
# Keys present in result.params that are model properties — never re-pass to forward()
_FORWARD_SKIP = frozenset({"fuel", "concept"})

# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------

_MODULE_LOAD_LOCK = threading.Lock()


@lru_cache(maxsize=32)
def _load_model_module(path: Path, module_name: str = "_concept_module") -> types.ModuleType:
    """Import a model_setup.py file, suppressing stdout from module-level prints.

    Module-level print() calls in model_setup.py are suppressed so they don't
    pollute server logs during live recompute requests.  The lock ensures
    redirect_stdout (which modifies sys.stdout globally) is thread-safe.
    """
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    with _MODULE_LOAD_LOCK:
        buf = StringIO()
        with redirect_stdout(buf):
            spec.loader.exec_module(module)
    return module


def _forward_with_overrides(
    model: Any, base_params: dict[str, Any], overrides: dict[str, Any]
) -> Any:
    """Re-run model.forward() with base_params updated by overrides.

    Follows costingfe's _build_lcoe_fn param-extraction pattern: the named args
    required by forward() are extracted explicitly; remaining physics/plant params
    pass as **kwargs. `fuel` and `concept` are skipped — they are model instance
    properties inferred from self, not caller-supplied kwargs.
    cost_overrides are not re-applied; this is consistent with how
    model.sensitivity() works (it also omits cost_overrides).
    """
    params = {**base_params, **overrides}
    extra = {k: v for k, v in params.items() if k not in _FORWARD_NAMED and k not in _FORWARD_SKIP}
    return model.forward(
        net_electric_mw=float(params["net_electric_mw"]),
        availability=float(params["availability"]),
        lifetime_yr=float(params["lifetime_yr"]),
        n_mod=float(params.get("n_mod", 1)),
        construction_time_yr=float(params.get("construction_time_yr", 6.0)),
        interest_rate=float(params.get("interest_rate", 0.07)),
        inflation_rate=float(params.get("inflation_rate", 0.02)),
        noak=bool(params.get("noak", True)),
        **extra,
    )


# ---------------------------------------------------------------------------
# Per-app state (populated by lifespan, held for the server's lifetime)
# ---------------------------------------------------------------------------


@dataclass
class _State:
    concepts: dict[str, ConceptData]
    manifest: ConceptManifest
    parameter_index: ParameterIndex
    dist_dir: Path
    explorer_state: ExplorerState = field(default_factory=ExplorerState)
    registry: ConceptRegistry | None = None
    decision_tree: dict | None = None
    similarity_reports: dict[str, ConceptSimilarityReport] = field(default_factory=dict)
    constellation: ConstellationData | None = None
    _state_lock: threading.Lock = field(default_factory=threading.Lock)


def get_state(request: Request) -> _State:
    """FastAPI dependency: extract _State from app.state."""
    state: _State | None = getattr(request.app.state, "data", None)
    if state is None:
        raise RuntimeError("App state not initialised — lifespan must run first")
    return state


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def _load_data(
    data_dir: Path,
    omitted: set[str] | None = None,
) -> tuple[dict[str, ConceptData], ConceptManifest, ParameterIndex]:
    """Load all data files from *data_dir*.

    Raises RuntimeError with a clear message when data/ is absent or empty.
    Called once during server startup — errors here abort the process.

    The manifest and parameter index are computed in-memory from the loaded
    per-concept JSONs. The names ``manifest.json`` / ``parameter_index.json``
    remain in ``_NON_CONCEPT_FILES`` so any stale files left on disk from
    earlier extractions don't get globbed as concept data.

    *omitted* is the omit-list set (FR-4); concept files whose stem (the concept
    ID, by the ``data/{id}.json`` convention) is in it are dropped before
    validation, so omitted concepts never enter the loaded set — and therefore
    never reach the manifest or parameter index, which are derived from it (I-4).
    The on-disk files are read-filtered only, never modified (I-6). ``None``
    defaults to the shipped omit list so the server enforces it independently of
    the extractor (FR-6); tests pass an explicit set for isolation.
    """
    if not data_dir.is_dir():
        raise RuntimeError(
            f"data/ directory not found at {data_dir}. "
            "Run extract_explorer_data.py to populate it before starting the server."
        )

    omit_set = load_omit_list() if omitted is None else omitted

    _NON_CONCEPT_FILES = {
        "manifest.json", "parameter_index.json",
        "concept_registry.json", "decision_tree.json",
    }
    concept_files = [
        f
        for f in data_dir.glob("*.json")
        if f.name not in _NON_CONCEPT_FILES and f.stem not in omit_set
    ]
    if not concept_files:
        raise RuntimeError(
            f"No concept data files found in {data_dir}. "
            "Re-run extract_explorer_data.py to populate it."
        )

    concepts: dict[str, ConceptData] = {}
    for path in concept_files:
        concept = ConceptData.model_validate_json(path.read_text())
        concepts[concept.concept_id] = concept

    # generated_at on the returned manifest now records server start time,
    # not extraction time. Functionally equivalent (used as a frontend cache key).
    concept_list = list(concepts.values())
    manifest = build_manifest(concept_list)
    parameter_index = build_parameter_index(concept_list)

    return concepts, manifest, parameter_index


def _load_taxonomy(
    data_dir: Path,
    omitted: set[str] | None = None,
) -> tuple[
    ConceptRegistry | None,
    dict | None,
    dict[str, ConceptSimilarityReport],
    ConstellationData | None,
]:
    """Load taxonomy data if available. Returns (registry, tree, reports, constellation).

    Non-fatal: if taxonomy files don't exist, returns all None/empty.
    Taxonomy is an additive feature — the server works without it.

    *omitted* is the omit-list set (FR-5). Filtering ``registry.concepts`` once,
    before similarity/constellation are computed from it, removes omitted concepts
    from the registry, similarity reports, and constellation in a single place
    (I-5); the decision tree is a separate dict, pruned independently. ``None``
    defaults to the shipped omit list so the server enforces it independently of
    the extractor (FR-6); tests pass an explicit set for isolation. The on-disk
    taxonomy JSON is read-filtered only, never modified (I-6).
    """
    registry_path = data_dir / "concept_registry.json"
    tree_path = data_dir / "decision_tree.json"

    if not registry_path.exists() or not tree_path.exists():
        return None, None, {}, None

    omit_set = load_omit_list() if omitted is None else omitted

    registry = ConceptRegistry.model_validate_json(registry_path.read_text())
    if omit_set:
        kept = [c for c in registry.concepts if c.concept_id not in omit_set]
        registry = registry.model_copy(update={"concepts": kept})

    decision_tree = json.loads(tree_path.read_text())
    if omit_set and "root" in decision_tree:
        pruned_root = prune_decision_tree(decision_tree["root"], omit_set)
        decision_tree = {**decision_tree, "root": pruned_root}

    # Precompute similarity reports for all concepts
    similarity_reports: dict[str, ConceptSimilarityReport] = {}
    for concept in registry.concepts:
        nearest = find_nearest(concept, registry, top_n=15)
        similarity_reports[concept.concept_id] = ConceptSimilarityReport(
            query_concept_id=concept.concept_id,
            query_concept_name=concept.name,
            nearest=nearest,
        )

    # Compute constellation
    matrix = compute_similarity_matrix(registry)
    constellation = compute_constellation(matrix, registry)

    return registry, decision_tree, similarity_reports, constellation


# ---------------------------------------------------------------------------
# Template rendering
# ---------------------------------------------------------------------------


def _render_templates(
    templates_dir: Path,
    dist_dir: Path,
    concepts: dict[str, ConceptData],
) -> None:
    """Render Jinja2 page templates to *dist_dir*.

    Silently skips templates that do not yet exist — page templates are
    written in Tasks 10-12 and server startup must not fail before them.
    The corresponding page routes return 404 until those tasks complete.
    """
    if not templates_dir.is_dir():
        return

    dist_dir.mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(templates_dir)), autoescape=True)

    def _try_render(template_name: str, dest: Path, **ctx: object) -> None:
        try:
            tmpl = env.get_template(template_name)
        except TemplateNotFound:
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(tmpl.render(**ctx))

    _try_render("index.html.j2", dist_dir / "index.html", active_nav="concepts")
    _try_render("compare.html.j2", dist_dir / "compare.html", active_nav="compare")
    _try_render("taxonomy.html.j2", dist_dir / "taxonomy.html", active_nav="taxonomy")

    for concept_id in concepts:
        _try_render(
            "concept.html.j2",
            dist_dir / "concept" / f"{concept_id}.html",
            concept_id=concept_id,
            active_nav="concepts",
        )


# ---------------------------------------------------------------------------
# Route handlers — module-level functions, state injected via Depends()
# ---------------------------------------------------------------------------


def _serve(path: Path) -> FileResponse:
    """Return FileResponse if *path* exists; 404 otherwise."""
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"{path.name} not found")
    return FileResponse(
        str(path),
        headers={"Cache-Control": "no-cache"},
    )


# -- Data API --

def health() -> dict[str, str]:
    return {"status": "ok"}


def api_get_manifest(state: _State = Depends(get_state)) -> ConceptManifest:
    return state.manifest


def api_get_concept(concept_id: str, state: _State = Depends(get_state)) -> ConceptData:
    concept = state.concepts.get(concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail=f"Concept {concept_id} not found")
    return concept


def api_get_parameter_index(state: _State = Depends(get_state)) -> ParameterIndex:
    return state.parameter_index


def api_get_parameter(param_name: str, state: _State = Depends(get_state)) -> ParameterIndexEntry:
    entry = state.parameter_index.parameters.get(param_name)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Parameter {param_name} not found")
    return entry


# -- Explorer state API --

def api_get_state(state: _State = Depends(get_state)) -> ExplorerState:
    return state.explorer_state


def api_post_state(body: ExplorerState, state: _State = Depends(get_state)) -> dict[str, str]:
    """Store explorer state; timestamp is set server-side (client value ignored)."""
    ts = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    with state._state_lock:
        state.explorer_state = body.model_copy(update={"timestamp": ts})
    return {"status": "ok"}


# -- Taxonomy API --

def api_taxonomy_tree(state: _State = Depends(get_state)) -> dict:
    """Return the full decision tree structure."""
    tree = state.decision_tree
    if tree is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    return tree


def api_taxonomy_registry(state: _State = Depends(get_state)) -> ConceptRegistry:
    """Return the full concept registry."""
    reg = state.registry
    if reg is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    return reg


def api_taxonomy_concept(concept_id: str, state: _State = Depends(get_state)) -> ConceptTaxonomy:
    """Return a single concept's taxonomy record."""
    reg = state.registry
    if reg is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    concept = reg.by_id(concept_id)
    if concept is None:
        raise HTTPException(
            status_code=404, detail=f"Concept '{concept_id}' not found in registry"
        )
    return concept


def api_taxonomy_similarity(
    concept_id: str, top_n: int = 5, state: _State = Depends(get_state)
) -> ConceptSimilarityReport:
    """Return precomputed similarity report (nearest neighbors + bridges).

    The ``top_n`` query parameter controls how many neighbors are returned
    (default 5, clamped to 1–15).
    """
    report = state.similarity_reports.get(concept_id)
    if report is None:
        raise HTTPException(
            status_code=404, detail=f"No similarity report for '{concept_id}'"
        )
    top_n = max(1, min(top_n, 15))
    return ConceptSimilarityReport(
        query_concept_id=report.query_concept_id,
        query_concept_name=report.query_concept_name,
        nearest=report.nearest[:top_n],
    )


def api_taxonomy_compare(
    concept_a: str, concept_b: str, state: _State = Depends(get_state)
) -> SimilarityResult:
    """Compare any two concepts on demand."""
    reg = state.registry
    if reg is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    a = reg.by_id(concept_a)
    b = reg.by_id(concept_b)
    if a is None or b is None:
        raise HTTPException(
            status_code=404, detail="One or both concept IDs not found"
        )
    comparison = compare_pair(a, b)
    bridges = explain_difference(a, b, reg)
    return SimilarityResult(
        concept_id=b.concept_id,
        concept_name=b.name,
        confinement_family=b.confinement_family,
        comparison=comparison,
        bridges=bridges,
    )


def api_taxonomy_constellation(state: _State = Depends(get_state)) -> ConstellationData:
    """Return 2D constellation coordinates for all concepts."""
    const = state.constellation
    if const is None:
        raise HTTPException(status_code=404, detail="Taxonomy data not loaded")
    return const


# -- Page routes --

def index_page(state: _State = Depends(get_state)) -> FileResponse:
    return _serve(state.dist_dir / "index.html")


def compare_page(state: _State = Depends(get_state)) -> FileResponse:
    return _serve(state.dist_dir / "compare.html")


def taxonomy_page(state: _State = Depends(get_state)) -> FileResponse:
    return _serve(state.dist_dir / "taxonomy.html")


def concept_page(concept_id: str, state: _State = Depends(get_state)) -> FileResponse:
    return _serve(state.dist_dir / "concept" / f"{concept_id}.html")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------


def create_app(base_dir: Path = BASE_DIR) -> FastAPI:
    """Return a configured FastAPI application rooted at *base_dir*.

    Using a factory (rather than a module-level singleton) lets tests inject
    a temporary directory without touching the real data/ tree.
    """
    data_dir = base_dir / "data"
    dist_dir = base_dir / "dist"
    templates_dir = base_dir / "templates"
    static_dir = base_dir / "static"

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        concepts, manifest, parameter_index = _load_data(data_dir)
        registry, decision_tree, similarity_reports, constellation = _load_taxonomy(
            data_dir
        )
        _render_templates(templates_dir, dist_dir, concepts)

        app.state.data = _State(
            concepts=concepts,
            manifest=manifest,
            parameter_index=parameter_index,
            dist_dir=dist_dir,
            registry=registry,
            decision_tree=decision_tree,
            similarity_reports=similarity_reports,
            constellation=constellation,
        )
        yield
        _compute_cached.cache_clear()
        _load_model_module.cache_clear()
        app.state.data = None

    # -- Computation closure (per-app-instance cache for test isolation) --

    @lru_cache(maxsize=128)
    def _compute_cached(
        concept_id: str, overrides_frozen: frozenset[tuple[str, float]]
    ) -> CostModelData:
        """Compute CostModelData with overridden params; result is LRU-cached.

        Cache key is (concept_id, frozenset(overrides.items())).  Identical
        param combos return the cached result without reloading the module.
        Baseline sensitivities come from the stored concept data — they are
        never recomputed on slider change (per spec 12).
        """
        state: _State = app.state.data
        concept = state.concepts.get(concept_id)
        if concept is None:
            raise ValueError(f"Concept {concept_id!r} not found in loaded data")
        model_setup = concept.sources.model_setup
        if model_setup is None:
            raise ValueError("compute called for a concept with no model_setup")

        module = _load_model_module(Path(model_setup))
        model = getattr(module, "model", None)
        if model is None:
            raise ImportError(f"Module {model_setup} does not define 'model'")
        result_1gw = getattr(module, "result_1gw", None)
        if result_1gw is None:
            raise ImportError(
                f"Module {model_setup} does not define 'result_1gw' at module level. "
                "See rework epic Items 10/11."
            )

        new_result = _forward_with_overrides(model, result_1gw.params, dict(overrides_frozen))

        raw: dict[str, Any] = dataclasses.asdict(new_result)
        params_dict: dict[str, Any] = raw.get("params", {})
        # Inject availability into power_table for capacity_factor fallback (same
        # fix as extract_explorer_data.py — availability lives in params, not power_table)
        if "availability" in params_dict:
            raw.setdefault("power_table", {})["availability"] = params_dict["availability"]

        baseline_sensitivities = concept.cost_model.sensitivities if concept.cost_model else None
        return CostModelData.from_forward_result(raw, baseline_sensitivities)

    def compute(body: ComputeRequest, state: _State = Depends(get_state)) -> CostModelData:
        concept = state.concepts.get(body.concept_id)
        if concept is None:
            raise HTTPException(status_code=404, detail=f"Concept {body.concept_id} not found")
        if concept.sources.model_setup is None:
            raise HTTPException(
                status_code=422,
                detail="Slider computation only available for costingfe-backed concepts",
            )
        return _compute_cached(body.concept_id, frozenset(body.overrides.items()))

    app = FastAPI(title="Fusion TEA Concept Explorer", lifespan=lifespan)

    # Static assets (CSS, JS, vendor libs, images)
    if static_dir.is_dir():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # -- Register routes --
    app.get("/api/health")(health)
    app.get("/api/manifest", response_model=ConceptManifest)(api_get_manifest)
    app.get("/api/concepts/{concept_id}", response_model=ConceptData)(api_get_concept)
    app.get("/api/parameter_index", response_model=ParameterIndex)(api_get_parameter_index)
    app.get("/api/parameters/{param_name}", response_model=ParameterIndexEntry)(api_get_parameter)
    app.get("/api/state", response_model=ExplorerState)(api_get_state)
    app.post("/api/state")(api_post_state)
    app.post("/api/compute", response_model=CostModelData)(compute)
    app.get("/api/taxonomy/tree")(api_taxonomy_tree)
    app.get("/api/taxonomy/registry", response_model=ConceptRegistry)(api_taxonomy_registry)
    app.get("/api/taxonomy/concepts/{concept_id}", response_model=ConceptTaxonomy)(api_taxonomy_concept)
    app.get("/api/taxonomy/similarity/{concept_id}", response_model=ConceptSimilarityReport)(api_taxonomy_similarity)
    app.get("/api/taxonomy/compare/{concept_a}/{concept_b}", response_model=SimilarityResult)(api_taxonomy_compare)
    app.get("/api/taxonomy/constellation", response_model=ConstellationData)(api_taxonomy_constellation)
    app.get("/")(index_page)
    app.get("/compare")(compare_page)
    app.get("/taxonomy")(taxonomy_page)
    app.get("/concept/{concept_id}")(concept_page)

    return app


# ---------------------------------------------------------------------------
# Module-level app instance (used when running directly or via uvicorn string ref)
# ---------------------------------------------------------------------------

# The lifespan runs only when uvicorn starts — not at import time.
app = create_app()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Fusion TEA Concept Explorer server")
    parser.add_argument(
        "--port",
        type=int,
        default=8421,
        help="TCP port to listen on (default: 8421)",
    )
    args = parser.parse_args()
    uvicorn.run(app, host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
