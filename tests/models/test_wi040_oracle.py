"""Independent WI-040 accounting identities and public oracle mappings."""

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e/studies"))
import oracle_entry as oracle  # noqa: E402


def test_inventory_mass_cost_and_residual():
    p = dict(oracle.vs.IN)
    result = oracle.vs._winding_material_inventory(p, 10.0)
    assert result["mass_copper"] == pytest.approx(31290.0)
    assert result["mass_solder"] == pytest.approx(10068.0)
    assert result["mass_steel"] == pytest.approx(28800.0)
    assert result["helium_density"] == pytest.approx(1.5e6 / (2077.2644 * 20.0))
    assert result["tape_volume"] == pytest.approx(0.9)
    assert result["material_cost"] == pytest.approx(sum(result["cost_" + m] for m in ("copper", "solder", "steel", "helium")))
    doubled = oracle.vs._winding_material_inventory(p, 20.0)
    for name in result:
        assert doubled[name] == pytest.approx(result[name] * (1 if name == "helium_density" else 2))


def test_procurement_no_material_tape_or_fabrication_overlap():
    p = dict(oracle.vs.IN)
    base = oracle.vs._winding_procurement(p, 25.0, 123.0, 12.2904)
    assert base["conductor_length"] == pytest.approx(321600.0)
    assert base["tape_cost"] == pytest.approx(12.2904 / (.006 * .000056) * 20)
    assert base["cost"] == pytest.approx(base["tape_cost"] + 123.0 + base["winding_fabrication_cost"])
    tape = oracle.vs._winding_procurement(p | {"magnet_tape_price_per_m": 40.0}, 25.0, 123.0, 12.2904)
    assert tape["tape_cost"] == 2 * base["tape_cost"]
    assert tape["winding_fabrication_cost"] == base["winding_fabrication_cost"]
    turn = oracle.vs._winding_procurement(p | {"magnet_turn_current": 25000.0}, 25.0, 123.0, 12.2904)
    assert turn["conductor_length"] == 2 * base["conductor_length"]
    assert turn["winding_fabrication_cost"] == 2 * base["winding_fabrication_cost"]
    assert turn["tape_cost"] == base["tape_cost"]


@pytest.mark.parametrize("name,value", [("magnet_f_copper", 1.0), ("magnet_rho_steel", 0.0), ("magnet_price_solder", -1.0), ("magnet_helium_pressure", float("nan")), ("T_cold_cryo", 0.0)])
def test_inventory_invalid_facts(name, value):
    with pytest.raises(ValueError, match="Winding Pack Material Inventory"):
        oracle.vs._winding_material_inventory(oracle.vs.IN | {name: value}, 10.0)


@pytest.mark.parametrize("name,value", [("magnet_turn_current", 0.0), ("magnet_f_set", 1.1), ("magnet_winding_rate_1990", -1.0), ("magnet_nonplanar_factor", float("inf"))])
def test_procurement_invalid_facts(name, value):
    with pytest.raises(ValueError, match="Winding Pack Procurement Cost"):
        oracle.vs._winding_procurement(oracle.vs.IN | {name: value}, 25.0, 100.0, 12.2904)


def test_public_mapping_retains_legacy_and_maps_selected_account():
    mapping = oracle.ORACLE_OUTPUT_TO_CHANNEL
    assert mapping["winding_pack"].endswith("__winding_procurement__cost")
    assert mapping["winding_pack_legacy"].endswith("__winding_pack_cost__cost")
    assert len(set(mapping.values())) == len(mapping)
    assert set(oracle.ENTRY_KEY_TO_ORACLE_INPUT.values()) <= set(oracle.vs.IN)
