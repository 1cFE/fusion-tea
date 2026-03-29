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
import types
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager, redirect_stdout
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import lru_cache
from io import StringIO
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from exploration.concept_explorer.models import (
    ComputeRequest,
    ConceptData,
    ConceptManifest,
    CostModelData,
    ExplorerState,
    ParameterIndex,
    ParameterIndexEntry,
)

BASE_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# Parameter sets for model.forward() re-invocation (compute endpoint)
# ---------------------------------------------------------------------------

# Named args that forward() takes explicitly (not via **overrides)
_FORWARD_NAMED = frozenset(
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
# Keys present in result.params that are model properties — never re-pass to forward()
_FORWARD_SKIP = frozenset({"fuel", "concept"})


def _load_model_module(path: Path, module_name: str = "_concept_module") -> types.ModuleType:
    """Import a model_setup.py file, suppressing stdout from module-level prints.

    Module-level print() calls in model_setup.py are suppressed so they don't
    pollute server logs during live recompute requests.
    """
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
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
        n_mod=int(float(params.get("n_mod", 1))),
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
    # lru_cache-wrapped concept lookup; keyed on concept_id string
    get_concept: Callable[[str], ConceptData | None]
    # Explorer session state (in-memory only; resets on server restart)
    explorer_state: ExplorerState = field(default_factory=ExplorerState)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def _load_data(
    data_dir: Path,
) -> tuple[dict[str, ConceptData], ConceptManifest, ParameterIndex]:
    """Load all data files from *data_dir*.

    Raises RuntimeError with a clear message when data/ is absent or empty.
    Called once during server startup — errors here abort the process.
    """
    if not data_dir.is_dir():
        raise RuntimeError(
            f"data/ directory not found at {data_dir}. "
            "Run extract_explorer_data.py to populate it before starting the server."
        )

    manifest_path = data_dir / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError(
            f"manifest.json not found in {data_dir}. "
            "Re-run extract_explorer_data.py to regenerate it."
        )

    index_path = data_dir / "parameter_index.json"
    if not index_path.exists():
        raise RuntimeError(
            f"parameter_index.json not found in {data_dir}. "
            "Re-run extract_explorer_data.py to regenerate it."
        )

    concept_files = [
        f
        for f in data_dir.glob("*.json")
        if f.name not in ("manifest.json", "parameter_index.json")
    ]
    if not concept_files:
        raise RuntimeError(
            f"No concept data files found in {data_dir}. "
            "Re-run extract_explorer_data.py to populate it."
        )

    manifest = ConceptManifest.model_validate_json(manifest_path.read_text())
    parameter_index = ParameterIndex.model_validate_json(index_path.read_text())

    concepts: dict[str, ConceptData] = {}
    for path in concept_files:
        concept = ConceptData.model_validate_json(path.read_text())
        concepts[concept.concept_id] = concept

    return concepts, manifest, parameter_index


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
    written in Tasks 10–12 and server startup must not fail before them.
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

    for concept_id in concepts:
        _try_render(
            "concept.html.j2",
            dist_dir / "concept" / f"{concept_id}.html",
            concept_id=concept_id,
            active_nav="concepts",
        )


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

    # Single-element list: mutable container for nonlocal assignment in the lifespan.
    _state: list[_State | None] = [None]

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: ARG001
        concepts, manifest, parameter_index = _load_data(data_dir)
        _render_templates(templates_dir, dist_dir, concepts)

        # Build a per-app LRU cache so repeated /api/concepts calls skip the dict
        # lookup after the first hit.  Defined here so it closes over `concepts`.
        @lru_cache(maxsize=256)
        def _get_concept_cached(concept_id: str) -> ConceptData | None:
            return concepts.get(concept_id)

        _state[0] = _State(
            concepts=concepts,
            manifest=manifest,
            parameter_index=parameter_index,
            get_concept=_get_concept_cached,
        )
        yield
        _state[0] = None

    def _s() -> _State:
        """Return the loaded state; asserts the lifespan has run."""
        s = _state[0]
        assert s is not None, "App state not initialised — lifespan must run first"
        return s

    app = FastAPI(title="Fusion TEA Concept Explorer", lifespan=lifespan)

    # Static assets (CSS, JS, vendor libs, images)
    if static_dir.is_dir():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # ------------------------------------------------------------------
    # Data API
    # ------------------------------------------------------------------

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/manifest", response_model=ConceptManifest)
    def get_manifest() -> ConceptManifest:
        return _s().manifest

    @app.get("/api/concepts/{concept_id}", response_model=ConceptData)
    def get_concept(concept_id: str) -> ConceptData:
        concept = _s().get_concept(concept_id)
        if concept is None:
            raise HTTPException(status_code=404, detail=f"Concept {concept_id} not found")
        return concept

    @app.get("/api/parameters/{param_name}", response_model=ParameterIndexEntry)
    def get_parameter(param_name: str) -> ParameterIndexEntry:
        entry = _s().parameter_index.parameters.get(param_name)
        if entry is None:
            raise HTTPException(status_code=404, detail=f"Parameter {param_name} not found")
        return entry

    # ------------------------------------------------------------------
    # Explorer state API — in-memory session context for the /manage-concept agent
    # ------------------------------------------------------------------

    @app.get("/api/state", response_model=ExplorerState)
    def get_state() -> ExplorerState:
        return _s().explorer_state

    @app.post("/api/state")
    def post_state(body: ExplorerState) -> dict[str, str]:
        """Store explorer state; timestamp is set server-side (client value ignored)."""
        ts = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        _s().explorer_state = body.model_copy(update={"timestamp": ts})
        return {"status": "ok"}

    # ------------------------------------------------------------------
    # Computation API — slider-driven model recompute (costingfe concepts only)
    # ------------------------------------------------------------------

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
        concept = _s().get_concept(concept_id)
        assert concept is not None, f"Concept {concept_id!r} not found in loaded data"
        model_setup = concept.sources.model_setup
        assert model_setup is not None, "compute called for a concept with no model_setup"

        module = _load_model_module(Path(model_setup))
        model = getattr(module, "model")
        result = getattr(module, "result")

        new_result = _forward_with_overrides(model, result.params, dict(overrides_frozen))

        raw: dict[str, Any] = dataclasses.asdict(new_result)
        params_dict: dict[str, Any] = raw.get("params", {})
        # Inject availability into power_table for capacity_factor fallback (same
        # fix as extract_explorer_data.py — availability lives in params, not power_table)
        if "availability" in params_dict:
            raw.setdefault("power_table", {})["availability"] = params_dict["availability"]

        baseline_sensitivities = concept.cost_model.sensitivities if concept.cost_model else None
        return CostModelData.from_forward_result(raw, baseline_sensitivities)

    @app.post("/api/compute", response_model=CostModelData)
    def compute(body: ComputeRequest) -> CostModelData:
        concept = _s().get_concept(body.concept_id)
        if concept is None:
            raise HTTPException(status_code=404, detail=f"Concept {body.concept_id} not found")
        if concept.sources.model_setup is None:
            raise HTTPException(
                status_code=422,
                detail="Slider computation only available for costingfe-backed concepts",
            )
        return _compute_cached(body.concept_id, frozenset(body.overrides.items()))

    # ------------------------------------------------------------------
    # Page routes — serve pre-rendered HTML from dist/
    # NEVER embed concept data here; pages are shells, data fetched by JS.
    # ------------------------------------------------------------------

    def _serve(path: Path) -> FileResponse:
        """Return FileResponse if *path* exists; 404 otherwise."""
        if not path.is_file():
            raise HTTPException(status_code=404, detail=f"{path.name} not found")
        return FileResponse(str(path))

    @app.get("/")
    def index_page() -> FileResponse:
        return _serve(dist_dir / "index.html")

    @app.get("/compare")
    def compare_page() -> FileResponse:
        return _serve(dist_dir / "compare.html")

    @app.get("/concept/{concept_id}")
    def concept_page(concept_id: str) -> FileResponse:
        return _serve(dist_dir / "concept" / f"{concept_id}.html")

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
    uvicorn.run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
