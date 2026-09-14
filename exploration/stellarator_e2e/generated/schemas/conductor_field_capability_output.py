from pydantic import Field
from simkit.config.schema import MultiOutput

class Conductor_Field_CapabilityOutput(MultiOutput):
    """Multi-output container for Conductor_Field_Capability.

Relative conductor quantity for a purchased design field envelope, distinct from actual peak-field demand. Normative manual equations: quantity_factor = (B_design / B_reference)^field_exponent; j_wp_effective = j_reference / quantity_factor; cost_per_kAm_effective = price_reference * quantity_factor.
Inputs: B_design and B_reference [T], field_exponent [1], j_reference [A/mm^2], price_reference [dollars/(kA m)] at the reference envelope. Outputs: quantity_factor [1], j_wp_effective [A/mm^2], cost_per_kAm_effective [dollars/(kA m)]. Effective price represents increased tape quantity, not a vendor grade premium. Fixed composition makes all pack material volumes follow the enlarged pack; do not multiply material procurement by quantity_factor again.
Supported priced transfer holds reference density, economic reference field, tape family, temperature, angular assumption, composition and coil-set shape/distribution factors fixed. Independent reference-density changes remain calibration/arithmetic and require a separately justified price/inventory basis. This is a relative engineering estimate, not an absolute critical-current margin, temperature/angle surface, vendor qualification or casing-fit check. The source's approximate 20 K exponent has no stated fit interval in the inspected paragraph; Fig. 1a's open black squares extend the 20 K measurements to approximately 24 T, below the 24.9 T reference. Pinning-force saturation does not establish a validity boundary.
Numerical domain: finite positive B_design, B_reference, field_exponent and j_reference; finite nonnegative price_reference. Intermediate field ratio and quantity_factor and output j_wp_effective must be finite and positive; effective price finite and nonnegative. Typed manual completion raises ValueError naming the calculation and quantity for invalid inputs, overflow and zero-underflow outputs. At equal fields quantity_factor is exactly one and reference density/price are preserved.
*Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf
*Reference**: Molodyk et al. (2021), printed p. 5 (approximate critical-current field exponent 0.6 at 20 K); Fig. 1 (tape-level field measurements). Inverse relative-current-density law at fixed operating fraction; uniform fixed-composition pack enlargement and unchanged reference unit-tape economics are agent assumptions.
*Last Updated**: 2026-09-13

SysML Source: root-0/analyses/mfe_conductor_grade.sysml:4
    """
    quantity_factor: float = Field(description="quantity_factor output")
    j_wp_effective: float = Field(description="j_wp_effective output")
    cost_per_kAm_effective: float = Field(description="cost_per_kAm_effective output")
