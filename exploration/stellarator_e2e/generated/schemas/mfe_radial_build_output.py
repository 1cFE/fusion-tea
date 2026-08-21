from pydantic import Field
from simkit.config.schema import MultiOutput

class MFE_Radial_BuildOutput(MultiOutput):
    """Multi-output container for MFE_Radial_Build.

Forward radial build [m, m^2, m^3] for an MFE torus: cumulative layer
radii from the plasma minor radius outward, then torus-shell volumes and
the first-wall surface area.

  or_i      = or_{i-1} + t_i                              (cumulative radii)
  layer_vol = kappa * 2*pi^2 * R * (or_out^2 - or_in^2)   (torus shell)
  wall_area = kappa * 4*pi^2 * R * vacuum_or              (first-wall SA)

Aggregates match 1costingFE's CAS22 grouping (model.py:1205-1208):
blanket = firstwall+blanket+reflector; shield = ht+lt; structure; vessel.
Concept-agnostic: R major radius, a minor radius (= plasma_t), kappa
elongation, per-layer thicknesses. Pure torus shells, no shape factor
(owner Option 1, WI-021) -- engineered annuli are sized by the radial
build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
admissible per PROTOCOL.md section 3.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
*Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
(cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
(CAS22 aggregation)
*Basis**: forward radial build; torus branch; MFE-generic

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:44
    """
    wall_area: float = Field(description="wall_area output")
    shield_vol: float = Field(description="shield_vol output")
    structure_vol: float = Field(description="structure_vol output")
    r_coil: float = Field(description="r_coil output")
    blanket_vol: float = Field(description="blanket_vol output")
    vessel_vol: float = Field(description="vessel_vol output")
