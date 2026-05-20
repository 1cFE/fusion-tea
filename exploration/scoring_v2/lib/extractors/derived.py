"""Derived extractor.

Computes feature values from other features already on disk (which were
populated by upstream extractors — typically `taxonomy`).

Currently implements one derived feature:

* `confinement_concept` — a single canonical concept label (e.g. "Compact
  tokamak", "Laser ICF (indirect drive)", "Levitated dipole") that collapses
  the v3 taxonomy columns (Confinement Family, MFE Topology, IFE Driver,
  MIF Method, Non-Standard Mechanism, Tokamak Shape, Stellarator Type,
  Laser Approach) into a single string used by Technical Feasibility (triple
  product lookup), Plant Complexity (subsystem trigger sets like
  TOKAMAK_CONCEPTS / DISRUPTION_PRONE_CONCEPTS), and reporting.

Disambiguation rules implement the Technical Feasibility implementation
spec's mapping table; the controlled vocabulary the downstream specs use:

  Tokamaks (4):  "Tokamak", "Compact tokamak", "Spherical tokamak",
                 "Negative triangularity tokamak"
  Stellarators (4): "Stellarator", "QI stellarator", "Modular stellarator",
                    "Helical coil stellarator", "Planar coil stellarator"
  Open/Linear:   "Mirror", "Z-pinch (sheared-flow)"
  Dipoles:       "Levitated dipole", "Levitated dipole (orbital)"
  Compact toroid: "FRC"
  IFE laser:     "Laser ICF ({approach})"
  IFE non-laser: "Heavy ion ICF", "Projectile ICF", "Acoustic ICF (sonofusion)"
  MIF:           "MagLIF", "Magnetized target fusion", "FRC compression (MIF)"
  Non-standard:  "Polywell", "Electrostatic hybrid", "Beam-target fusion",
                 "Muon-catalyzed fusion", "Dense plasma focus"

Caller is responsible for ordering: the derived extractor reads from
features/{cid}.yaml, so taxonomy extraction must run first. See
`extract.py --bulk-derived`.
"""
from __future__ import annotations

from typing import Any

from .. import feature_io


def _v(doc: dict, name: str) -> str:
    block = doc.get(name)
    if isinstance(block, dict):
        return str(block.get("value") or "")
    return ""


def _confinement_concept(concept_id: str, doc: dict) -> str:
    cfam = _v(doc, "confinement_family")
    mfe_top = _v(doc, "mfe_topology")
    ife_drv = _v(doc, "ife_driver")
    mif_meth = _v(doc, "mif_method")
    non_std = _v(doc, "non_standard_mechanism")
    tok_shape = _v(doc, "tokamak_shape")
    stel_type = _v(doc, "stellarator_type")
    laser_app = _v(doc, "laser_approach")

    if cfam == "MFE":
        if mfe_top == "Tokamak":
            return {
                "Compact":                "Compact tokamak",
                "Spherical":              "Spherical tokamak",
                "Negative triangularity": "Negative triangularity tokamak",
                "Standard":               "Tokamak",
            }.get(tok_shape, "Tokamak")
        if mfe_top == "Stellarator":
            return {
                "QI":           "QI stellarator",
                "Modular":      "Modular stellarator",
                "Helical coil": "Helical coil stellarator",
                "Planar coil":  "Planar coil stellarator",
            }.get(stel_type, "Stellarator")
        if mfe_top == "Open/Linear":
            # Pinches identify themselves in the concept_id; everything else
            # in this branch is a mirror variant.
            if "z-pinch" in concept_id.lower() or "pinch" in concept_id.lower():
                return "Z-pinch (sheared-flow)"
            return "Mirror"
        if mfe_top == "Dipole":
            if "orbital" in concept_id.lower():
                return "Levitated dipole (orbital)"
            return "Levitated dipole"
        if mfe_top == "Compact Toroid":
            # Steady-state FRC (MFE) — distinct from MIF FRC compression.
            return "FRC"
        return "Unknown"

    if cfam == "IFE":
        if ife_drv == "Laser":
            label = {
                "Direct drive":     "direct drive",
                "Indirect drive":   "indirect drive",
                "Fast ignition":    "fast ignition",
                "Ultrashort pulse": "ultrashort pulse",
                "Hybrid drive":     "hybrid drive",
                "Liquid jet":       "liquid jet",
            }.get(laser_app)
            return f"Laser ICF ({label})" if label else "Laser ICF"
        if ife_drv == "Heavy ion beam":
            return "Heavy ion ICF"
        if ife_drv == "Projectile":
            return "Projectile ICF"
        if ife_drv == "Acoustic":
            return "Acoustic ICF (sonofusion)"
        return "Unknown"

    if cfam == "MIF":
        if mif_meth == "Magnetized target":
            # MagLIF is a distinct architecture (z-pinch-driven liner). All
            # current MagLIF concepts carry "maglif" in their ID; other
            # magnetized-target concepts (pneumatic, MTIF) collapse to the
            # generic MIF label.
            if "maglif" in concept_id.lower():
                return "MagLIF"
            return "Magnetized target fusion"
        if mif_meth == "FRC compression":
            return "FRC compression (MIF)"
        return "Unknown"

    if cfam == "Non-Standard":
        if non_std == "Electrostatic":
            cid = concept_id.lower()
            if "polywell" in cid:
                return "Polywell"
            if "accelerator" in cid or "particle-accelerator" in cid:
                return "Beam-target fusion"
            return "Electrostatic hybrid"
        if non_std == "Muon-catalyzed":
            return "Muon-catalyzed fusion"
        if non_std == "Plasma focus":
            return "Dense plasma focus"
        return "Unknown"

    return "Unknown"


_DERIVERS = {
    "confinement_concept": _confinement_concept,
}


def extract(
    concept_id: str, feature_name: str, schema_entry: dict[str, Any]
) -> tuple[Any, str, str]:
    deriver = _DERIVERS.get(feature_name)
    if deriver is None:
        raise ValueError(
            f"derived extractor has no rule for feature {feature_name!r}; "
            f"add one to lib/extractors/derived.py"
        )
    doc = feature_io.read_features(concept_id)
    value = deriver(concept_id, doc)
    return value, "derived", "high"
