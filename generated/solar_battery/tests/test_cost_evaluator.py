"""Tests for ComponentCostEvaluator module in isolation (no pipeline)."""

import pytest
from pathlib import Path

from solar_battery.modules.component_cost_evaluator import (
    ComponentCostEvaluator,
    CostEvaluatorResult,
    CostEvaluatorInput,
)


class TestComponentCostEvaluator:
    """Test cost evaluator module in isolation (no pipeline)."""

    MODEL_PATH = str(
        Path(__file__).resolve().parents[3] / "models" / "tests" / "solar_battery"
    )

    def test_run_produces_result(self):
        module = ComponentCostEvaluator()
        result = module.run(model_path=self.MODEL_PATH)
        assert isinstance(result.data, CostEvaluatorResult)

    def test_total_capex_matches_expected(self):
        module = ComponentCostEvaluator()
        result = module.run(model_path=self.MODEL_PATH)
        assert result.data.total_capex.root == pytest.approx(41205.0, abs=0.01)

    def test_design_params_present(self):
        module = ComponentCostEvaluator()
        result = module.run(model_path=self.MODEL_PATH)
        assert result.data.p_net_mw.root == pytest.approx(0.008)
        assert result.data.plant_lifetime.root == pytest.approx(25.0)
        assert result.data.discount_rate.root == pytest.approx(0.05)

    def test_validate_and_fill_default(self):
        module = ComponentCostEvaluator()
        validated = module.validate_and_fill_default(model_path="/some/path")
        assert isinstance(validated, CostEvaluatorInput)
        assert validated.model_path == "/some/path"
