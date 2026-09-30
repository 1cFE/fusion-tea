from pydantic import Field
from simkit.config.schema import MultiOutput

class Blanket_Tritium_BreedingOutput(MultiOutput):
    """Multi-output container for Blanket_Tritium_Breeding.

Continuous-energy-transport response interpolation for an explicitly fixed material/source scenario. The supported lever is breeder thickness [m]; all other geometry inputs [m, except dimensionless kappa] are applicability guards. Fixed enrichment and material/source metadata belong to the immutable response-data manifest, not free public inputs. The typed manual implementation checks finite inputs, the released table domain and every fixed geometry coordinate; no extrapolation or clamping. Table release and independent withheld validation are prerequisites for implementation completion.
Outputs are Li6/Li7 production and total tritium atoms per emitted fusion neutron, total Monte Carlo standard error, interpolation allowance, numerical lower estimate and defined_flag (exactly 0 or 1). The statistical multiplier and allowance are declared in the released manifest. The lower estimate is not a physical confidence bound. Unsupported inputs return zero numerical carriers and defined_flag=0; those carriers are undefined, not physical zero breeding or proof of deficit. Shaped-stellarator bias and physical scenario uncertainties remain separate.
*Source**: work/active/WI-066_computed-tritium-breeding/spec.md
*Reference**: work/active/WI-066_computed-tritium-breeding/design.md; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
*Last Updated**: 2026-09-18

SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:4
    """
    interpolation_allowance: float = Field(description="interpolation_allowance output")
    tbr_lower: float = Field(description="tbr_lower output")
    defined_flag: float = Field(description="defined_flag output")
    tbr_li6: float = Field(description="tbr_li6 output")
    tbr_std_error: float = Field(description="tbr_std_error output")
    tbr_li7: float = Field(description="tbr_li7 output")
    tbr_mean: float = Field(description="tbr_mean output")
