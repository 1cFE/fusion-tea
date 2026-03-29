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
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from exploration.concept_explorer.models import (
    ConceptData,
    ConceptManifest,
    ParameterIndex,
    ParameterIndexEntry,
)

BASE_DIR = Path(__file__).parent


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
