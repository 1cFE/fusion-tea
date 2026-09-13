# Current consumer and harness handoff

The two public calculation interfaces, 246 native inputs, 158 scalar outputs, pipeline bindings and authored engineering assertions are unchanged. Internal intermediate attributes became implementation locals; public model-contract and pipeline bytes are identical. Native valid results and reports are exact against fresh baseline.

Direct calculation ValueError messages identify live clearance, reference clearance, or `require 0 < T_cold < T_amb`. PreparedEvaluator returns EvaluationFailed carrying that message; these invalid cases do not produce an engineering result. T-035 current oracle must reject the same domains. Unsupported oracle parameters remain unsupported.

T-036 current tests need ten-seed regeneration via `evidence/regenerate.py::seed_and_generate`, two-file scoped source-preservation allowances and updated temporary radius-driver invalid-case expectations. Historical WI-050/051/052 outputs and helpers remain historical evidence. The exact 63 new failing/error nodes and one inherited stale hash node are in `evidence/regression-attribution.json`.

Current metadata is prepared for subsequent sequential integration. No integration or study was run here. Await fresh independent audit after current consumer/harness prerequisites complete.
