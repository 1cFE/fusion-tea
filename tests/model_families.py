"""The design families that share the canonical model tree, and how each is generated alone.

Since the stellarator model migration (2026-08-21) `models/` is a source collection, not
one generated plant: the IFE family (`hif_ife`, `generic_ife`) and the MFE family
(`stellarator_09`, `generic_mfe`) live side by side and share three foundation files.
Generating the whole tree as one plant is not a thing any package does, so every test that
generates must pick a family (design D6–D8):

* each family owns a set of **logical paths** — the layout the exploration twins use, i.e.
  the canonical path with the ``library/`` prefix stripped;
* family ownership plus independently generated source collections must exactly
  cover every canonical ``.sysml`` file;
* a path owned by both families is a shared file and must be byte-identical in canonical,
  the IFE twin and the MFE twin;
* a family generates from a **materialized canonical subset**: its owned canonical files
  copied into a temporary directory in the twin layout, which must equal the twin itself.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CANONICAL = REPO / "models"
LIBRARY_PREFIX = "library/"


@dataclass(frozen=True)
class Family:
    name: str
    twin: Path
    owned: tuple[str, ...]  # logical paths
    package_name: str


IFE = Family(
    name="ife",
    twin=REPO / "exploration" / "ife_e2e" / "models",
    owned=(
        "analyses/fusion_cycle.sysml",
        "analyses/hif_economics.sysml",
        "analyses/ife_lcoe.sysml",
        "cost_structure/cas_hierarchy.sysml",
        "cost_structure/ife_cost_parameters.sysml",
        "designs/generic_ife/ife_plant.sysml",
        "designs/generic_ife/ife_subsystems.sysml",
        "designs/hif_ife/hif_driver.sysml",
        "designs/hif_ife/hif_plant.sysml",
        "foundation/costed_component.sysml",
        "foundation/economic_parameter.sysml",
    ),
    package_name="self_binding_check",
)

MFE = Family(
    name="mfe",
    twin=REPO / "exploration" / "stellarator_e2e" / "models",
    owned=(
        "analyses/mfe_account_costs.sysml",
        "analyses/mfe_facilities.sysml",
        "structure/mfe_facilities_parts.sysml",
        "analyses/mfe_cryo_plant.sysml",
        "analyses/mfe_cryo_inventory.sysml",
        "analyses/mfe_heating_chain.sysml",
        "analyses/mfe_lcoe_dcf.sysml",
        "analyses/mfe_magnet_cost.sysml",
        "analyses/mfe_winding_pack_cost.sysml",  # WI-040 explicit inventory and procurement
        "analyses/mfe_winding_pack_fit.sysml",
        "analyses/mfe_conductor_current.sysml",
        "analyses/mfe_conductor_grade.sysml",  # WI-038 relative field-envelope quantity
        "analyses/mfe_magnet_field.sysml",
        "analyses/mfe_plasma_scaling.sysml",
        "analyses/mfe_plasma_sustainment.sysml",
        "analyses/mfe_power_balance.sysml",
        "analyses/mfe_matched_steam_cycle.sysml",
        "structure/mfe_steam_cycle_components.sysml",
        "analyses/mfe_power_cycle.sysml",  # WI-045 (2026-09-08): the cycle fit, handwritten stage
        "analyses/mfe_cooling_accounts.sysml",
        "analyses/mfe_cooling_equipment.sysml",
        "analyses/mfe_primary_loop.sysml",  # WI-045 (2026-09-08): the representative helium circuit
        "analyses/mfe_lifecycle.sysml",  # WI-046 (2026-09-08): the lifecycle calendar, handwritten stage
        "analyses/mfe_fuel_cycle.sysml",  # WI-047 (2026-09-08): the tritium flows and the required breeding ratio
        "analyses/mfe_tritium_breeding.sysml",  # WI-066: computed breeding and conditional adequacy
        "analyses/mfe_divertor_heat.sysml",  # WI-047 (2026-09-08): the divertor surface-heat ledger
        "analyses/mfe_vacuum.sysml",  # WI-047 (2026-09-08): the exhaust gas load
        "analyses/mfe_viability.sysml",
        "cost_structure/cas_hierarchy.sysml",
        "cost_structure/mfe_power_core.sysml",
        "structure/mfe_interfaces.sysml",  # WI-057 commit C: item and port definitions
        "structure/mfe_plasma.sysml",  # WI-057 (2026-09-13): the plasma as a part
        "structure/mfe_magnet_parts.sysml",  # WI-057: coil, winding pack, casing
        "structure/mfe_radial_build_parts.sysml",  # WI-057: the first wall
        "structure/mfe_plant_systems.sysml",  # WI-057: heat transport, cryoplant, fuel cycle, vacuum pumping
        "designs/generic_mfe/mfe_plant.sysml",
        "designs/generic_mfe/mfe_subsystems.sysml",
        "designs/stellarator_09/stellarator_plant.sysml",
        "foundation/costed_component.sysml",
        "foundation/economic_parameter.sysml",
    ),
    package_name="stellarator_tea",
)

FAMILIES: dict[str, Family] = {IFE.name: IFE, MFE.name: MFE}

# Separate generation units, not exploration twins or a combined plant family.
# Sources: exploration/aries_transfer/<name>/{build,verify}.py staging lists.
SOURCE_COLLECTIONS: dict[str, tuple[str, ...]] = {
    "aries_integrated": (
        "analyses/integrated_lifecycle_costs.sysml",
        "analyses/mfe_lcoe_dcf.sysml",
        "analyses/integrated_heat_electricity.sysml",
        "analyses/integrated_equipment_costs.sysml",
        "structure/integrated_equipment_parts.sysml",
        "foundation/costed_component.sysml",
        "analyses/mfe_account_costs.sysml",
        "analyses/source_budget_accounting.sysml",
        "analyses/radial_density_profile.sysml",
        "analyses/supplied_profile_plasma.sysml",
        "analyses/mfe_plasma_scaling.sysml",
        "analyses/mfe_fuel_cycle.sysml",
        "analyses/mfe_viability.sysml",
        "analyses/dual_circuit_heat_accounting.sysml",
        "analyses/ideal_gas_brayton_components.sysml",
        "designs/aries_cs_transfer/plasma_integration.sysml",
        "designs/aries_cs_integrated/plant.sysml",
    ),
    "aries_density_profile": (
        "analyses/radial_density_profile.sysml",
        "designs/aries_cs_transfer/density_profile.sysml",
    ),
    "aries_fuel_reuse": (
        "analyses/mfe_fuel_cycle.sysml",
        "analyses/mfe_viability.sysml",
        "designs/aries_cs_transfer/fuel_reuse.sysml",
    ),
    "aries_plasma_integration": (
        "analyses/supplied_profile_plasma.sysml",
        "analyses/radial_density_profile.sysml",
        "analyses/mfe_plasma_scaling.sysml",
        "designs/aries_cs_transfer/plasma_integration.sysml",
    ),
    "aries_constituent_inventory": (
        "analyses/sector_constituent_inventory.sysml",
        "designs/aries_cs_transfer/constituent_inventory.sysml",
    ),
    "aries_plasma_fuel": (
        "analyses/supplied_profile_plasma.sysml",
        "analyses/radial_density_profile.sysml",
        "analyses/mfe_plasma_scaling.sysml",
        "analyses/mfe_fuel_cycle.sysml",
        "analyses/mfe_viability.sysml",
        "designs/aries_cs_transfer/plasma_integration.sysml",
        "designs/aries_cs_transfer/plasma_fuel.sysml",
    ),
    "aries_dual_blanket_heat": (
        "analyses/dual_circuit_heat_accounting.sysml",
        "analyses/mfe_viability.sysml",
        "designs/aries_cs_transfer/dual_blanket_heat.sysml",
    ),
    "aries_nominal_brayton": (
        "analyses/ideal_gas_brayton_components.sysml",
        "analyses/mfe_viability.sysml",
        "designs/aries_cs_transfer/nominal_brayton.sysml",
    ),
    "aries_source_budget": (
        "analyses/source_budget_accounting.sysml",
        "analyses/mfe_account_costs.sysml",
        "designs/aries_cs_transfer/source_budget.sysml",
    ),
    # WI-093: cross-plant assemblies from existing definitions; source: exploration/combinations/build.py staging list.
    "combinations": (
        "structure/mfe_interfaces.sysml",
        "structure/mfe_plasma.sysml",
        "analyses/mfe_plasma_sustainment.sysml",
        "analyses/mfe_plasma_scaling.sysml",
        "analyses/mfe_primary_loop.sysml",
        "analyses/mfe_power_cycle.sysml",
        "analyses/mfe_viability.sysml",
        "analyses/integrated_heat_electricity.sysml",
        "analyses/dual_circuit_heat_accounting.sysml",
        "analyses/ideal_gas_brayton_components.sysml",
        "analyses/integrated_equipment_costs.sysml",
        "structure/integrated_equipment_parts.sysml",
        "foundation/costed_component.sysml",
        "analyses/mfe_fuel_cycle.sysml",
        "designs/combinations/combinations_circulator_purchase.sysml",
        "designs/combinations/combinations_loop_brayton.sysml",
        "designs/combinations/combinations_lumped_fit.sysml",
        "designs/combinations/combinations_plasma_chain.sysml",
    ),
    # WI-094 (goal design-study-parameters): the costed loop-Brayton assembly; source: exploration/costed_loop_brayton/build.py staging list.
    "costed_loop_brayton": (
        "analyses/mfe_primary_loop.sysml",
        "analyses/mfe_viability.sysml",
        "analyses/integrated_heat_electricity.sysml",
        "analyses/ideal_gas_brayton_components.sysml",
        "analyses/integrated_equipment_costs.sysml",
        "structure/integrated_equipment_parts.sysml",
        "foundation/costed_component.sysml",
        "analyses/mfe_fuel_cycle.sysml",
        "analyses/mfe_account_costs.sysml",
        "analyses/mfe_lcoe_dcf.sysml",
        "analyses/integrated_lifecycle_costs.sysml",
        "analyses/loop_return_control.sysml",  # WI-095
        "designs/costed_loop_brayton/costed_loop_brayton.sysml",
    ),
}

SHARED_PATHS: tuple[str, ...] = tuple(sorted(set(IFE.owned) & set(MFE.owned)))


def canonical_path(logical: str) -> Path:
    """The canonical file for a logical path: ``designs/…`` stays, everything else is
    under ``library/``."""
    if logical.startswith("designs/"):
        return CANONICAL / logical
    return CANONICAL / LIBRARY_PREFIX / logical


def logical_path(canonical: Path, root: Path = CANONICAL) -> str:
    relative = canonical.relative_to(root).as_posix()
    if relative.startswith(LIBRARY_PREFIX):
        return relative[len(LIBRARY_PREFIX):]
    return relative


def canonical_files(root: Path = CANONICAL) -> dict[str, Path]:
    """Every canonical SysML file keyed by logical path; refuses a layout collision."""
    files: dict[str, Path] = {}
    for path in sorted(root.rglob("*.sysml")):
        name = logical_path(path, root)
        assert name not in files, (
            f"logical path collision {name!r}: {files[name].relative_to(root)} and "
            f"{path.relative_to(root)}"
        )
        files[name] = path
    return files


def materialize_canonical_subset(family: Family, destination: Path) -> Path:
    """Copy the family's owned canonical files into ``destination`` in the twin layout."""
    destination.mkdir(parents=True, exist_ok=True)
    for logical in family.owned:
        source = canonical_path(logical)
        assert source.is_file(), f"{family.name} owns {logical!r} but {source} is missing"
        target = destination / logical
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return destination


def assert_canonical_ownership(root: Path = CANONICAL) -> None:
    """Refuse unregistered canonical files and missing registered files alike."""
    owned = {path for family in FAMILIES.values() for path in family.owned}
    owned.update(path for paths in SOURCE_COLLECTIONS.values() for path in paths)
    actual = set(canonical_files(root))
    assert owned == actual, {
        "unregistered": sorted(actual - owned),
        "missing": sorted(owned - actual),
    }

# WI-096 additive matched-conversion generation unit; existing collections unchanged.
SOURCE_COLLECTIONS["component_alternatives"] = (
    'analyses/mfe_primary_loop.sysml',
    'analyses/mfe_viability.sysml',
    'analyses/integrated_heat_electricity.sysml',
    'analyses/ideal_gas_brayton_components.sysml',
    'analyses/integrated_equipment_costs.sysml',
    'structure/integrated_equipment_parts.sysml',
    'foundation/costed_component.sysml',
    'analyses/mfe_account_costs.sysml',
    'analyses/mfe_lcoe_dcf.sysml',
    'analyses/loop_return_control.sysml',
    'analyses/mfe_matched_steam_cycle.sysml',
    'analyses/cooling_equipment_selected_pumps.sysml',
    'analyses/component_alternatives_thermal.sysml',
    'designs/component_alternatives/plant.sysml',
)

# WI-098 isolated conditional whole-plant comparison.
SOURCE_COLLECTIONS["whole_plant_conversion"] = tuple(p for p in SOURCE_COLLECTIONS["component_alternatives"] if not p.startswith("designs/")) + ("analyses/mfe_fuel_cycle.sysml", "analyses/whole_plant_conversion_accounts.sysml", "designs/whole_plant_conversion/plant.sysml")

# WI-099 isolated matched-duty magnet conductor alternatives (goal magnet-material-comparison).
SOURCE_COLLECTIONS["magnet_materials"] = (
    'analyses/magnet_conductor_alternatives.sysml',
    'designs/magnet_materials/magnet_subsystem.sysml',
)

# WI-100 derived stellarator material packages (goal magnet-material-comparison). The build stages the MFE
# twin (equal to these canonical files) and Round 1's conductor library; the variants library and the materials
# design file live in the package's own tree (exploration/stellarator_materials/models/), outside models/.
SOURCE_COLLECTIONS["stellarator_materials"] = MFE.owned + ("analyses/magnet_conductor_alternatives.sysml",)
