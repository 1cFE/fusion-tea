"""The design families that share the canonical model tree, and how each is generated alone.

Since the stellarator model migration (2026-08-21) `models/` is a source collection, not
one generated plant: the IFE family (`hif_ife`, `generic_ife`) and the MFE family
(`stellarator_09`, `generic_mfe`) live side by side and share three foundation files.
Generating the whole tree as one plant is not a thing any package does, so every test that
generates must pick a family (design D6–D8):

* each family owns a set of **logical paths** — the layout the exploration twins use, i.e.
  the canonical path with the ``library/`` prefix stripped;
* the union of the owned paths must cover every canonical ``.sysml`` file;
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
        "analyses/mfe_cryo_plant.sysml",
        "analyses/mfe_lcoe_dcf.sysml",
        "analyses/mfe_magnet_cost.sysml",
        "analyses/mfe_plasma_scaling.sysml",
        "analyses/mfe_power_balance.sysml",
        "analyses/mfe_viability.sysml",
        "cost_structure/cas_hierarchy.sysml",
        "cost_structure/mfe_power_core.sysml",
        "designs/generic_mfe/mfe_plant.sysml",
        "designs/generic_mfe/mfe_subsystems.sysml",
        "designs/stellarator_09/stellarator_plant.sysml",
        "foundation/costed_component.sysml",
        "foundation/economic_parameter.sysml",
    ),
    package_name="stellarator_tea",
)

FAMILIES: dict[str, Family] = {IFE.name: IFE, MFE.name: MFE}

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
