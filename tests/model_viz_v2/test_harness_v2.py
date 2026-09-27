"""The v2 test folder collects beside v1's: namespace imports of v1 helpers and one fixture pin."""

from viewer2_harness import FIXTURE, FIXTURE_SHA256

from tests.model_viz import panel_dom, part_panel_dom, structure_oracle
from tests.model_viz import viewer_harness as v1_harness


def test_v1_helpers_import_as_namespace_modules():
    assert callable(panel_dom.panel_dump) and callable(part_panel_dom.part_panel_dump)
    assert callable(structure_oracle.ancestors)


def test_fixture_pin_matches_v1():
    assert FIXTURE_SHA256 == v1_harness.FIXTURE_SHA256 and FIXTURE == v1_harness.FIXTURE


def test_fixture_on_pin(fixture_path):
    assert fixture_path == FIXTURE
