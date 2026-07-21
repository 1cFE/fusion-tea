"""Auto-generated implementation for MFE_Radial_Build.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:41

SysML Expressions:
    pi = 3.14159265358979
    vacuum_or = a + vacuum_t
    firstwall_or = vacuum_or + firstwall_t
    blanket_or = firstwall_or + blanket_t
    reflector_or = blanket_or + reflector_t
    ht_shield_or = reflector_or + ht_shield_t
    structure_or = ht_shield_or + structure_t
    gap1_or = structure_or + gap1_t
    vessel_or = gap1_or + vessel_t
    coil_or = vessel_or + coil_t
    gap2_or = coil_or + gap2_t
    lt_shield_or = gap2_or + lt_shield_t
    C = kappa * 2.0 * pi ** 2 * R
    firstwall_vol = C * (firstwall_or ** 2 - vacuum_or ** 2)
    blanket_layer_vol = C * (blanket_or ** 2 - firstwall_or ** 2)
    reflector_vol = C * (reflector_or ** 2 - blanket_or ** 2)
    ht_shield_vol = C * (ht_shield_or ** 2 - reflector_or ** 2)
    lt_shield_vol = C * (lt_shield_or ** 2 - gap2_or ** 2)
    blanket_vol = firstwall_vol + blanket_layer_vol + reflector_vol
    shield_vol = ht_shield_vol + lt_shield_vol
    structure_vol = C * (structure_or ** 2 - ht_shield_or ** 2)
    vessel_vol = C * (vessel_or ** 2 - gap1_or ** 2)
    wall_area = kappa * 4.0 * pi ** 2 * R * vacuum_or
    r_coil = vessel_or
    
Documentation:
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
(owner Option 1, WI-021) — engineered annuli are sized by the radial
build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
admissible per PROTOCOL.md section 3.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
*Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
(cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
(CAS22 aggregation)
*Basis**: forward radial build; torus branch; MFE-generic
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plasma_scaling.mfe_radial_build import MFE_Radial_BuildInput


def run_mfe_radial_build(inputs: MFE_Radial_BuildInput) -> tuple[float, float, float, float, float, float]:
    """Execute MFE_Radial_Build calculation.

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
(owner Option 1, WI-021) — engineered annuli are sized by the radial
build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
admissible per PROTOCOL.md section 3.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
*Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
(cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
(CAS22 aggregation)
*Basis**: forward radial build; torus branch; MFE-generic

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:41

SysML Expressions:
    pi = 3.14159265358979
    vacuum_or = a + vacuum_t
    firstwall_or = vacuum_or + firstwall_t
    blanket_or = firstwall_or + blanket_t
    reflector_or = blanket_or + reflector_t
    ht_shield_or = reflector_or + ht_shield_t
    structure_or = ht_shield_or + structure_t
    gap1_or = structure_or + gap1_t
    vessel_or = gap1_or + vessel_t
    coil_or = vessel_or + coil_t
    gap2_or = coil_or + gap2_t
    lt_shield_or = gap2_or + lt_shield_t
    C = kappa * 2.0 * pi ** 2 * R
    firstwall_vol = C * (firstwall_or ** 2 - vacuum_or ** 2)
    blanket_layer_vol = C * (blanket_or ** 2 - firstwall_or ** 2)
    reflector_vol = C * (reflector_or ** 2 - blanket_or ** 2)
    ht_shield_vol = C * (ht_shield_or ** 2 - reflector_or ** 2)
    lt_shield_vol = C * (lt_shield_or ** 2 - gap2_or ** 2)
    blanket_vol = firstwall_vol + blanket_layer_vol + reflector_vol
    shield_vol = ht_shield_vol + lt_shield_vol
    structure_vol = C * (structure_or ** 2 - ht_shield_or ** 2)
    vessel_vol = C * (vessel_or ** 2 - gap1_or ** 2)
    wall_area = kappa * 4.0 * pi ** 2 * R * vacuum_or
    r_coil = vessel_or
    
Documentation:
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
(owner Option 1, WI-021) — engineered annuli are sized by the radial
build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
admissible per PROTOCOL.md section 3.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
*Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
(cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
(CAS22 aggregation)
*Basis**: forward radial build; torus branch; MFE-generic

Args:
    inputs: Input parameters validated against MFE_Radial_BuildInput schema

Returns:
    tuple[float, ...]: (blanket_vol, shield_vol, structure_vol, vessel_vol, wall_area, r_coil)

Example:
    >>> inputs = MFE_Radial_BuildInput(...)
    >>> blanket_vol, shield_vol, structure_vol, vessel_vol, wall_area, r_coil = run_mfe_radial_build(inputs)
    """
    C = (((inputs.kappa * 2.0) * (inputs.pi ** 2)) * inputs.R)
    vacuum_or = (inputs.a + inputs.vacuum_t)
    firstwall_or = (vacuum_or + inputs.firstwall_t)
    blanket_or = (firstwall_or + inputs.blanket_t)
    blanket_layer_vol = (C * ((blanket_or ** 2) - (firstwall_or ** 2)))
    firstwall_vol = (C * ((firstwall_or ** 2) - (vacuum_or ** 2)))
    reflector_or = (blanket_or + inputs.reflector_t)
    ht_shield_or = (reflector_or + inputs.ht_shield_t)
    ht_shield_vol = (C * ((ht_shield_or ** 2) - (reflector_or ** 2)))
    reflector_vol = (C * ((reflector_or ** 2) - (blanket_or ** 2)))
    structure_or = (ht_shield_or + inputs.structure_t)
    gap1_or = (structure_or + inputs.gap1_t)
    vessel_or = (gap1_or + inputs.vessel_t)
    coil_or = (vessel_or + inputs.coil_t)
    gap2_or = (coil_or + inputs.gap2_t)
    lt_shield_or = (gap2_or + inputs.lt_shield_t)
    lt_shield_vol = (C * ((lt_shield_or ** 2) - (gap2_or ** 2)))
    return (
        ((firstwall_vol + blanket_layer_vol) + reflector_vol),  # blanket_vol
        (ht_shield_vol + lt_shield_vol),  # shield_vol
        (C * ((structure_or ** 2) - (ht_shield_or ** 2))),  # structure_vol
        (C * ((vessel_or ** 2) - (gap1_or ** 2))),  # vessel_vol
        ((((inputs.kappa * 4.0) * (inputs.pi ** 2)) * inputs.R) * vacuum_or),  # wall_area
        vessel_or,  # r_coil
    )
