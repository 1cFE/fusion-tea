from pydantic import Field
from simkit.config.schema import MultiOutput

class Annual_Cost_RollupOutput(MultiOutput):
    """Multi-output container for Annual_Cost_Rollup.

CAS70 = CAS71 + CAS72, and the total levelized annual cost the LCOE
numerator carries (CAS70 + CAS80). Pure addition — it introduces no new
economics, it makes the two sums producer channels the DCF core and the
1cfe-form comparison channel can read.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/model.py (pin 0254385)
*Ref**: model.py:1483-1605 (c70 = c71 + c72; lcoe numerator c90 + c70 + c80);
economics.py:88-92 (compute_lcoe)
*Basis**: 1costingFE CAS70 composition and LCOE annual-cost numerator

SysML Source: root-0/analyses/mfe_account_costs.sysml:853
    """
    cas70: float = Field(description="cas70 output")
    annual_total: float = Field(description="annual_total output")
