
## Purpose
Define the contract and tooling that enables non-costingfe concept scripts to produce `CostModelData`-compatible output, including sensitivity data via finite-difference.

## Requirements
- Standalone scripts expose a `to_explorer_dict() -> dict` function that returns a dict passing `CostModelData.model_validate()`
- A `finite_difference_sensitivity(params_dataclass, cost_fn, delta=0.01) -> dict` utility computes dimensionless elasticities identical in definition to costingfe's autodiff: `(dLCOE/dp) * (p/LCOE)` via central differences
- `finite_difference_sensitivity` returns `{"engineering": {param: elasticity}, "financial": {param: elasticity}}` — same shape as `model.sensitivity()`
- The resulting `SensitivityAnalysis` carries `method="finite_difference"`
- The pipeline validation stage calls `CostModelData.model_validate(to_explorer_dict())` and errors on failure — no silent degradation

## Acceptance Criteria
- Given a standalone script implementing `to_explorer_dict()`, `CostModelData.model_validate(to_explorer_dict())` passes without error
- Given `finite_difference_sensitivity(params, cost_fn)` where `cost_fn` is a pure function of `params`, the returned elasticities match a known analytical result within 1% for a test function
- Given a standalone concept with sensitivity data, the tornado chart renders (non-empty) in the same format as a costingfe concept
- Given a script missing `to_explorer_dict()`, the pipeline stage raises `AttributeError` with a clear message naming the missing function
- `SensitivityAnalysis.method == "finite_difference"` for standalone-sourced data

## Interfaces
- **Utility file**: `exploration/concept_explorer/sensitivity_utils.py`
- **Function**: `finite_difference_sensitivity(params_dataclass, cost_fn, delta=0.01, engineering_keys=None, financial_keys=None) -> dict`
- **Contract**: standalone `model_setup.py` files must expose `to_explorer_dict() -> dict`
- **Called by**: `06-data-extraction-pipeline.md` for standalone concept extraction
- **Output shape**: same as `02-costingfe-adapter.md` output — `CostModelData` (see `01-data-models.md`)

## Constraints
- NEVER allow standalone concepts to produce an empty `sensitivities` dict — either finite-difference sensitivity is computed or the pipeline errors
- NEVER modify the standalone scripts' existing computation logic — `to_explorer_dict()` wraps the existing output
- `finite_difference_sensitivity` MUST use central differences `(f(p+δ) - f(p-δ)) / (2δ)` scaled to dimensionless elasticity
- The utility MUST handle zero-valued parameters without division-by-zero (skip or use absolute delta)

## Out of Scope
- Migrating standalone scripts to costingfe (future work)
- Slider/recomputation support for standalone concepts (costingfe-only, see `10-computation-api.md`)
- Automatic detection of which parameters are "engineering" vs "financial" for standalone scripts (caller provides the classification)

