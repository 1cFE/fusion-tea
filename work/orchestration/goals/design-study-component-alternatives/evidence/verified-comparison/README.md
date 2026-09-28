# Verified comparison renderer

[AGENT] Completed reporting for the verified `20260926-design-study-component-alternatives-b` record. Stock verification passes all 498 cases; the original anchors remain exact catalog minima. The script reads retained cases, accounting outputs, metadata and verification receipts. It imports no model or oracle and executes no study.

Run `.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/verified-comparison/analyze-verified.py` after the coordinator deposits the completed record. Optional `--record PATH` and `--out-dir PATH` select the input record and report destination.

Generation requires the stock `results/verification_summary.json` to pass, cover all 498 exact case IDs, and match the fingerprint of every stored case. A missing receipt was tested: the script exits 1 before writing result data or figures. Original and new complete input maps must match exactly. The original selected anchors must remain minima in their finite passing catalogs; an assertion failure requires investigation before reporting.

Outputs are `report.md`, `matched-study-summary.json`, `plot-data.json`, `plot-data.csv`, and output/cost/sensitivity figures in SVG and PNG. The summary separates scalar numerical changes from predicate changes against the preserved old record. Per-case data retains native identities, actual verdicts, cooler failure codes, bracket UA values, and capacity margins. The old blocked figures and data remain unchanged.

The generated report passed its verification gate, input-map equality checks, exact catalog-minimum assertions and accounting checks. All three PNG figures were visually inspected; the sensitivity figure was expanded to show both opposed quote scenarios and inspected again. The coordinator's independent reviewer assesses the arithmetic and conclusions.
