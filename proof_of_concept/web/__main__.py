"""Entry point for running the web server.

Usage:
    uv run python -m proof_of_concept.web
"""

import uvicorn

from .server import app


def main():
    """Run the web server."""
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
