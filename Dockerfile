# Slim serving image for the concept-explorer web deployment.
#
# Installs ONLY requirements-serve.txt (the pinned serving set — no torch,
# docling, agentic-mbse, sysml-codegen) and runs the existing app unchanged
# from the copied repo tree. This is the single artifact every candidate
# platform (Railway primary; Render/HF fallback) consumes; it deliberately
# bypasses pyproject.toml / uv.lock / [tool.uv.sources] so the offline pipeline
# install stays untouched (FR-3). See .project/completed/20260821_explorer-web-hosting/.
FROM python:3.12-slim

# Unbuffered stdout/stderr so logs stream to the platform; no .pyc litter.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dependency layer first so it caches independently of app-source changes.
COPY requirements-serve.txt .
RUN pip install --no-cache-dir -r requirements-serve.txt

# Runtime tree: app + the analyses/archive files compute & findings read.
# .dockerignore trims the ~7 GB of dev/research bulk from this context.
# WORKDIR=/app becomes the repo root at runtime (invariant: CWD=repo root).
COPY . .

# Shell form so ${PORT} expands at runtime (exec form would not). Single
# worker (no --workers) — app.state / LRU cache / in-memory state assume one
# process. ${PORT:-8421} keeps `docker run` usable locally without -e PORT.
CMD ["sh", "-c", "uvicorn exploration.concept_explorer.server:app --host 0.0.0.0 --port ${PORT:-8421}"]
