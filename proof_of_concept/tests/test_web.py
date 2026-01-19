"""Tests for web server API endpoints."""

import pytest
from fastapi.testclient import TestClient

from proof_of_concept.web.server import app

client = TestClient(app)


def test_get_model_valid_path():
    """API returns Cytoscape elements for valid model."""
    response = client.get("/api/model/models/tests/coffee_maker")
    assert response.status_code == 200
    data = response.json()
    assert "elements" in data
    assert len(data["elements"]) == 10  # Matches golden reference


def test_get_model_invalid_path():
    """API returns 404 for nonexistent path."""
    response = client.get("/api/model/nonexistent/path")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_index_served():
    """GET / returns HTML page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
