"""Integration test: full pipeline execution."""

import pytest
from pathlib import Path

from simkit.core.pipeline import execute_pipeline
from solar_battery import create_solar_battery_registry, CUSTOM_SCHEMA_TYPES


class TestPipelineIntegration:
    """Integration test: full pipeline execution."""

    PIPELINE_DIR = Path(__file__).resolve().parents[1]

    def _run_pipeline(self):
        return execute_pipeline(
            spec_path=str(self.PIPELINE_DIR / "pipelines" / "pipeline.yaml"),
            output_dir=str(self.PIPELINE_DIR / "outputs"),
            registry=create_solar_battery_registry(),
            custom_schema_types=CUSTOM_SCHEMA_TYPES,
        )

    def test_pipeline_executes_without_error(self):
        result = self._run_pipeline()
        assert result is not None
        assert "lcoe_per_mwh" in result.outputs

    def test_lcoe_within_tolerance(self):
        result = self._run_pipeline()
        lcoe = getattr(result.outputs["lcoe_per_mwh"], "root", result.outputs["lcoe_per_mwh"])
        assert lcoe == pytest.approx(288.68, rel=0.01)

    def test_total_capex_correct(self):
        result = self._run_pipeline()
        total_capex = result.outputs["component_costs__total_capex"]
        assert total_capex.root == pytest.approx(41205.0, abs=0.01)

    def test_all_seven_metrics(self):
        result = self._run_pipeline()
        outputs = result.outputs

        # All exit outputs are RootModel[float] — extract via .root
        assert outputs["component_costs__total_capex"].root == pytest.approx(41205.0, abs=0.01)
        assert outputs["annual_energy_mwh"].root == pytest.approx(11.14272, rel=0.01)
        assert outputs["annual_om_cost"].root == pytest.approx(160.0, rel=0.01)
        assert outputs["annual_fuel_cost"].root == pytest.approx(0.0, abs=0.01)
        assert outputs["capital_recovery_factor"].root == pytest.approx(0.070952, rel=0.01)
        assert outputs["annualized_capital_cost"].root == pytest.approx(2923.60, rel=0.01)
        assert outputs["lcoe_per_mwh"].root == pytest.approx(288.68, rel=0.01)
