# Independent source/math review — T-001

**Verdict: FINDINGS.** The proposed conditional loop-count diagnostic is supported by the existing reduced equations. Engineering qualification and installed cost remain unestablished. No owner intervention is needed to execute that bounded diagnostic; no source establishes a feasible or priced installation.

Fresh review, 2026-09-16. Read quarantine PROTOCOL only within the holdout; no barred content or external documentation opened. Evidence checked: Moscato `knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md` §§2–3 and original page-6 image `work/orchestration/goals/plant-closure/evidence/grounding_sources/moscato_p6_tables2_3.png`; `models/library/analyses/mfe_primary_loop.sysml`; `models/library/structure/mfe_plant_systems.sysml:11`; `models/designs/stellarator_09/stellarator_plant.sysml:1060`; `models/library/analyses/mfe_account_costs.sysml:532`; admitted external `cas22.py:675–688`.

## Independent arithmetic

The named case implies 3433.821515 kg/s and 3566.367025 MW source heat. Ceiling of total flow / 225.0777778 gives **16 loops**. Using unchanged reference pressure, loss, temperatures, efficiency and ideal-helium properties:

| Loops | Flow/loop kg/s | Loss kPa | Total compressor MW | Required IHX MW/loop | Circulators / IHXs |
|---|---:|---:|---:|---:|---:|
| 14 | 245.272965 | 390.910240 | 260.861120 | 273.373439 | 28 / 14 |
| 15 | 228.921434 | 340.526254 | 226.966340 | 252.888891 | 30 / 15 |
| 16 | 214.613845 | 299.290653 | 199.287304 | 235.353396 | 32 / 16 |
| 18 | 190.767862 | 236.476565 | 157.228848 | 206.866437 | 36 / 18 |

Compressor numbers equal fluid work and lower-bound electrical draw at drive efficiency 1. Required IHX duty includes that work. These are independent equation checks, not native study verification.

## Findings to carry forward

1. Amend hydraulic-source-account's “Concrete next model” recommendation to match the brief: resistance splitting and a flow-area lever are unnecessary for count-only comparisons. No new hydraulic equation is needed.
2. The source establishes two circulators and one IHX per loop, but distinct 3-IB/6-OB circuits. Counts above are conditional averaged-module replication. Reference flow is a screening allowance, not proven maximum capacity. Duty-weighted resistance is not exact flow weighting; retain that distinction in downstream prose.
3. IHX duties are requirements, not installed ratings. Source duty, area and equipment counts cannot prove off-design transfer, routing or compressor capability. Preserve the Table-2 MPa/Table-3 kPa inconsistency, calibration status and drive-loss gap.
4. Verified cost equations have no direct loop-count input. Their resulting account changes cannot price added equipment. External-document coverage claims in entering-cost-account were not independently checked. Supplier/equipment evidence remains missing.

Keep all twenty predicates and distinguish the loop-only screen. Missing qualification and pricing must remain explicit conclusions, never inferred passes.

## Correction recheck — 2026-09-16

**PASS for the scoped diagnostic.** Rechecked hydraulic-source-account's “Supported next comparison”: finding 1 is addressed. It now calls for the existing integer-count comparison without new hydraulic equations. The 14/15/16/18-loop diagnostic may proceed with all twenty predicates preserved. Findings 2–4 remain disclosure and evidence limits; engineering qualification and installed-equipment pricing are still unestablished. Interpret “installed reference duties” only as conditional source-derived nominal comparisons, never as demonstrated installed ratings. This releases the diagnostic, not a feasibility or priced-benefit claim.
