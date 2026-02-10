"""ComponentCostEvaluator TEAx Module

Wraps generate_costs.py's compute_costs() as a TEAx module.
Bridges component-level cost computation into the pipeline.

Outputs total_capex (dynamically computed) and all design parameters
(from pre-generated design_params.json) as a MultiOutput with RootModel[float]
fields. Each field becomes a separate pipeline channel.
"""

import importlib.util
import json
from pathlib import Path

from pydantic import BaseModel, Field
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v2.primitives import Float


class CostEvaluatorInput(BaseModel):
    """Input for ComponentCostEvaluator module."""

    model_path: str = Field(..., description="Path to SysML model directory")


class CostEvaluatorResult(MultiOutput):
    """Output from ComponentCostEvaluator module.

    MultiOutput container with RootModel[float] fields.
    Each field becomes a separate pipeline channel via to_channel_dict().
    Downstream modules reference channels with .root to extract float values.
    """

    total_capex: Float = Field(description="Total capital expenditure")
    p_net_mw: Float = Field(description="Net power in MW")
    n_mod: Float = Field(description="Number of modules")
    plant_availability: Float = Field(description="Plant availability factor")
    plant_lifetime: Float = Field(description="Plant lifetime in years")
    yearly_inflation: Float = Field(description="Yearly inflation rate")
    discount_rate: Float = Field(description="Discount rate")
    om_rate_per_kw_year: Float = Field(description="O&M rate per kW per year")
    fuel_unit_cost: Float = Field(description="Fuel unit cost")
    fuel_consumption: Float = Field(description="Fuel consumption")
    p_net_kw: Float = Field(description="Net power in kW")


class ComponentCostEvaluator(ModuleBase[CostEvaluatorInput, CostEvaluatorResult]):
    name: str = "ComponentCostEvaluator"
    version: str = "v0.1"

    def validate_and_fill_default(self, model_path: str) -> CostEvaluatorInput:
        return CostEvaluatorInput(model_path=model_path)

    def run(self, model_path: str) -> ModuleResult[CostEvaluatorResult]:
        validated = self.validate_and_fill_default(model_path)
        model_dir = Path(validated.model_path)

        # 1. Dynamically compute total_capex via compute_costs()
        compute_costs = self._import_compute_costs(model_dir)
        costs = compute_costs(str(model_dir))
        total_capex = costs["solar_battery_plant"]["capital_cost"]

        # 2. Read design parameters from pre-generated JSON
        design_params_path = model_dir / "design_params.json"
        with open(design_params_path) as f:
            params = json.load(f)

        # 3. Override total_capex with dynamically computed value
        params["total_capex"] = total_capex

        # 4. Wrap all values in Float (RootModel[float]) for MultiOutput channels
        return ModuleResult(
            data=CostEvaluatorResult(
                **{k: Float(v) for k, v in params.items()}
            )
        )

    @staticmethod
    def _import_compute_costs(model_dir: Path):
        """Import compute_costs from generate_costs.py using importlib."""
        import sys

        spec = importlib.util.spec_from_file_location(
            "generate_costs",
            model_dir / "generate_costs.py",
        )
        module = importlib.util.module_from_spec(spec)
        # Register in sys.modules so @dataclass can resolve string annotations
        sys.modules["generate_costs"] = module
        spec.loader.exec_module(module)
        return module.compute_costs
