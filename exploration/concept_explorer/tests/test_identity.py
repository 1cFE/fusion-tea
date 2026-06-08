"""Tests for canonical identity resolution (Theme A / A1).

Coverage:
- De-risk audit: every served (non-omitted) concept resolves to a clean
  ``Name (Fuel)`` — the gate Option B's correctness rests on.
- ``resolve_identity``: normal, suffix-variant (17a), not-in-registry (honest
  degradation), and the one documented composed-suffix exception (concept 35).
- ``_compose_name``: idempotence, and the fuel-missing path never yields
  ``(None)`` (FR-A1.5).
- End-to-end stamping: ``/api/concepts/{id}`` and ``/api/taxonomy/concepts/{id}``
  return the same canonical name + code.
"""

from __future__ import annotations

import json
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from exploration.concept_explorer.models import (
    FUEL_DISPLAY,
    FuelType,
    load_omit_list,
)
from exploration.concept_explorer.server import (
    BASE_DIR,
    _compose_name,
    create_app,
    resolve_identity,
)
from exploration.concept_explorer.taxonomy_models import ConceptRegistry

_DATA_DIR = BASE_DIR / "data"


# ---------------------------------------------------------------------------
# Fixtures — the real, on-disk CSV-backed registry (identity source of truth)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def registry() -> ConceptRegistry:
    """The real registry as seeded from table.csv (unstamped, as on disk)."""
    return ConceptRegistry.model_validate_json(
        (_DATA_DIR / "concept_registry.json").read_text()
    )


def _served_ids() -> list[str]:
    """Served concept IDs (data/NN.json stems) minus the shipped omit list."""
    omit = load_omit_list()
    non_concept = {
        "manifest.json", "parameter_index.json",
        "concept_registry.json", "decision_tree.json",
    }
    return sorted(
        p.stem
        for p in _DATA_DIR.glob("*.json")
        if p.name not in non_concept and p.stem not in omit
    )


# ---------------------------------------------------------------------------
# De-risk audit gate — FR-A1.1 holds for every served concept
# ---------------------------------------------------------------------------


def test_audit_every_served_concept_resolves_to_name_fuel(registry: ConceptRegistry):
    """Every served concept resolves to a name ending in its structured fuel's
    display suffix.

    This is the Phase-1 gate: it proves Option 1 achieves FR-A1.1 universally,
    including concept 35 (whose authored CSV name omits the suffix despite a
    known D-D fuel — composed back in by `resolve_identity`).
    """
    offenders: list[str] = []
    for cid in _served_ids():
        tax = registry.by_id(cid)
        assert tax is not None, f"served concept {cid} missing from registry"
        ident = resolve_identity(cid, registry)
        disp = FUEL_DISPLAY.get(tax.fuel, "")
        # Every served concept has a real (display-able) fuel, so the suffix
        # must be present after resolution.
        assert disp, f"served concept {cid} has no display fuel ({tax.fuel})"
        if not ident.name.endswith(f"({disp})"):
            offenders.append(f"{cid}: {ident.name!r} (fuel {disp})")
    assert not offenders, "served concepts without a (Fuel) suffix: " + "; ".join(offenders)


# ---------------------------------------------------------------------------
# resolve_identity — the stencil
# ---------------------------------------------------------------------------


def test_resolve_identity_normal(registry: ConceptRegistry):
    ident = resolve_identity("01", registry)
    assert ident.code == "01"
    assert ident.name == "HTS Compact Tokamak (D-T)"  # Name (Fuel), not the company form
    assert ident.fuel == FuelType.DT


def test_resolve_identity_suffix_variant(registry: ConceptRegistry):
    ident = resolve_identity("17a", registry)
    assert ident.code == "17a"
    assert ident.name.endswith(")")  # fuel suffix present


def test_resolve_identity_composed_suffix_exception(registry: ConceptRegistry):
    """Concept 35: authored CSV name lacks the suffix; fuel D-D is known, so it
    is composed (Option 1). Documents the one non-clean registry row."""
    assert registry.by_id("35").name == "PoloMac Magnetic Confinement"  # raw, no suffix
    ident = resolve_identity("35", registry)
    assert ident.code == "35"
    assert ident.fuel == FuelType.DD
    assert ident.name == "PoloMac Magnetic Confinement (D-D)"


def test_resolve_identity_not_in_registry(registry: ConceptRegistry):
    """A served-but-unregistered concept degrades to its stored name + code —
    never throws, never blank."""
    ident = resolve_identity("zz-unregistered", registry, served_name="Mystery Reactor")
    assert ident.code == "zz-unregistered"
    assert ident.name == "Mystery Reactor"
    assert ident.fuel is None

    # No served_name either: degrade to the bare code, still non-blank.
    bare = resolve_identity("zz-unregistered", registry)
    assert bare.name == "zz-unregistered"


def test_resolve_identity_none_registry():
    """No registry at all (taxonomy not loaded) still degrades honestly."""
    ident = resolve_identity("01", None, served_name="Stored Name")
    assert ident.code == "01"
    assert ident.name == "Stored Name"
    assert ident.fuel is None


# ---------------------------------------------------------------------------
# _compose_name — idempotence and honest fuel-missing
# ---------------------------------------------------------------------------


def test_compose_name_idempotent():
    assert _compose_name("HTS Compact Tokamak (D-T)", FuelType.DT) == "HTS Compact Tokamak (D-T)"


def test_compose_name_appends_when_absent():
    assert _compose_name("PoloMac Magnetic Confinement", FuelType.DD) == (
        "PoloMac Magnetic Confinement (D-D)"
    )


def test_compose_name_fuel_missing_no_none_suffix():
    """Fuel-missing path renders the base name — never '(None)' or '(OTHER)'."""
    assert _compose_name("Freeform Concept", None) == "Freeform Concept"
    assert _compose_name("Freeform Concept", FuelType.OTHER) == "Freeform Concept"
    assert "(None)" not in _compose_name("Freeform Concept", None)
    assert "(None)" not in _compose_name("Freeform Concept", FuelType.OTHER)


# ---------------------------------------------------------------------------
# End-to-end stamping — both layers serve one canonical identity
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def real_client() -> Generator[TestClient, None, None]:
    """Client backed by the real data/ tree (full registry + concept payloads)."""
    app = create_app(base_dir=BASE_DIR)
    with TestClient(app) as c:
        yield c


@pytest.mark.parametrize(
    ("cid", "expected_name"),
    [
        ("01", "HTS Compact Tokamak (D-T)"),
        ("24", "Dense Plasma Focus (p-B11)"),
        ("35", "PoloMac Magnetic Confinement (D-D)"),  # composed-suffix exception
    ],
)
def test_both_layers_serve_canonical_identity(
    real_client: TestClient, cid: str, expected_name: str
):
    """The explorer layer and the taxonomy layer return the same canonical name
    and the same code for a given concept."""
    explorer = real_client.get(f"/api/concepts/{cid}")
    taxonomy = real_client.get(f"/api/taxonomy/concepts/{cid}")
    assert explorer.status_code == 200, explorer.text
    assert taxonomy.status_code == 200, taxonomy.text
    ex, tx = explorer.json(), taxonomy.json()
    assert ex["name"] == expected_name
    assert tx["name"] == expected_name
    assert ex["concept_id"] == cid
    assert tx["concept_id"] == cid


def test_explorer_payload_retains_analyst_name(real_client: TestClient):
    """The overlay overwrites `name` with the canonical form but preserves the
    raw frontmatter phrasing on `analyst_name` (and stamps the structured fuel)."""
    payload = real_client.get("/api/concepts/35").json()
    assert payload["name"] == "PoloMac Magnetic Confinement (D-D)"
    assert payload["fuel"] == FuelType.DD.value
    # The raw frontmatter phrasing (company form) is retained, not discarded.
    assert payload["analyst_name"] and payload["analyst_name"] != payload["name"]


def test_manifest_carries_canonical_name(real_client: TestClient):
    """Landing-card data (the manifest) is rebuilt from stamped concepts, so it
    carries the canonical name too."""
    manifest = real_client.get("/api/manifest").json()
    by_id = {e["concept_id"]: e for e in manifest["concepts"]}
    assert by_id["01"]["name"] == "HTS Compact Tokamak (D-T)"
    assert by_id["35"]["name"] == "PoloMac Magnetic Confinement (D-D)"
