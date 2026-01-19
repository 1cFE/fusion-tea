"""FastAPI server for SysML structural view visualization."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from proof_of_concept.extraction import extract_structural_view, load_model, to_cytoscape

app = FastAPI(title="SysML Structural View")

# Static files directory (relative to this file)
STATIC_DIR = Path(__file__).parent / "static"


@app.get("/api/model/{path:path}")
def get_model_view(path: str) -> dict:
    """Return Cytoscape.js elements for model at path.

    Args:
        path: Path to model directory or .sysml file

    Returns:
        Dict with "elements" key containing Cytoscape.js node data

    Raises:
        HTTPException: 404 if path not found, 422 if extraction fails
    """
    try:
        model = load_model(path)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    view_result = extract_structural_view(model)

    # Check for extraction errors in metadata
    if view_result.get("metadata", {}).get("error"):
        raise HTTPException(
            status_code=422, detail=view_result["metadata"]["error"]
        )

    return to_cytoscape(view_result)


@app.get("/")
def index():
    """Serve the main HTML page."""
    return FileResponse(STATIC_DIR / "index.html")


# Mount static files for other assets (JS, CSS, etc.)
# Note: This must come after explicit routes to avoid conflicts
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
