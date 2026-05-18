"""Phase 4 (ontology-v3 item 4): verify Heating Type / Driver Type wiring."""

from exploration.phase_2a.column_map import (
    DESIGN_COLUMNS,
    KEY_TO_COLUMN,
    VALUE_ALIASES,
    VOCABULARY,
    lookup_term,
)


def test_typed_columns_in_design_columns():
    assert "Heating Type" in DESIGN_COLUMNS
    assert "Driver Type" in DESIGN_COLUMNS


def test_key_to_column_routes_typed_aliases():
    assert KEY_TO_COLUMN["heating_type"] == "Heating Type"
    assert KEY_TO_COLUMN["driver_type"] == "Driver Type"


def test_value_aliases_present_for_typed_columns():
    assert VALUE_ALIASES["Driver Type"]["magnetic"] == "Magnetic"
    assert VALUE_ALIASES["Heating Type"]["icrh"] == "ICRH"


def test_vocabulary_lookup_for_typed_terms():
    icrh = lookup_term("ICRH")
    assert icrh is not None and icrh.column == "Heating Type"
    dpssl = lookup_term("DPSSL Laser")
    assert dpssl is not None and dpssl.column == "Driver Type"
