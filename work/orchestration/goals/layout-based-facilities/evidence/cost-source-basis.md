# Facility cost-source basis

Date: 2026-09-18. Researcher: delegated cost-source reader. Consumer: T-002 / REQ-LBF-01. Research type: source acquisition and accounting-boundary assessment. All recommendations below are [AGENT]; no DI entries were minted or approved.

## Result

The native result is **REGISTERED**, with three acquired sources. The source trail establishes historical methods and accounting boundaries, but does not establish a calibrated installed facility price. The original TETRA report explicitly warns that missing design detail understates quantities and recommends relative comparisons rather than absolute estimates. A material-quantity method is preferable for a layout-based estimate, but its civil reference-cost rows still need acquisition.

Run and receipts: `knowledge/research/requests/runs/REQ-LBF-01/20260919T011531965807/return.json`. Eight searches and four capture attempts consumed the declared limits. The first capture failed because sandbox DNS was unavailable; its authorized retry succeeded. The return retains that first failure in `queued[]` even though the same URL subsequently registered. It is an already-resolved access failure, not an outstanding source acquisition need. Registry verification returned zero faults and three existing legacy entries.

## Sources and checks

| Key | Registered source | Evidence used |
|---|---|---|
| S1 | `knowledge/sources/ukaea_process_cost_model_scope_and_historical_references/output.md` | Lines 414–458: 1990 method, safety factors and historical reference list; newer model citation remains an in-preparation 2015 paper |
| S2 | `knowledge/sources/ukaea_process_kovari_2014_cost_algorithm_building_and/output.md` | Lines 1568–1695 building method; 1862–1904 maintenance facilities/equipment; 2217–2287 assembly and project expenditure |
| S3 | `knowledge/sources/etr_iter_systems_code_ornl_fedc_87_7_1988/raw.pdf` | Printed pp136–142, PDF pages146–152; pp140–142 visually checked using rendered pages |
| S4, existing | `knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md` | Lines3937–4025 account21; 5126–5150 nuclear ventilation and maintenance equipment; 5267 onward indirects |
| S5, existing | `knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md` | Model-year switch, building rate defaults, ventilation and maintenance-equipment defaults |
| S6, existing | `knowledge/sources/mit_canes_capital_cost_evaluation_of_advanced_water_cooled/output.md`; original `knowledge/raw/mit194.pdf` | Printed pp31–37 method and data needs; p161–162 height dependence |

S1/S2 are official UKAEA implementation documentation. Their titles/topics were screened before capture. S3 is the original 1988 engineering report cited by PROCESS, predating the excluded concept. S6 had an existing full-text clean-screen record in SOURCE_INDEX.md. No barred source was opened. Web search/open output was used only for discovery and triage; findings here come from registered artifacts. S3's generated output.md omits most relevant prose, so the raw PDF and explicit page locators govern this report.

## Historical PROCESS: what the coefficients mean

S1 identifies a mixture of TETRA and Generomak methods, with all algorithms and costs expressed in 1990 dollars. S4 account21 says buildings scale with volume using methods developed from TFCX, TFTR and commercial plant buildings. It includes equipment, materials and installation labor, but excludes engineering and construction management. It does not give a contractor bill of quantities or shielding qualification.

The implemented form is `C_MUSD1990 = 1e-6 × u_USD1990_per_m3 × external_volume_m3 × safety_factor`, with exponent one. S5 labels several coefficients M$/m³, which conflicts with the explicit million-dollar conversion in S4. The dimensional interpretation is dollars per cubic meter. Treating these defaults as M$/m³ would overstate their contribution by one million.

| Function | Historical coefficient, USD1990/m³ | S5 identifier |
|---|---:|---|
| Reactor building | 400 | ucrb |
| Reactor maintenance building | 260 | UCMB |
| Warm shop | 460 | UCWS |
| Tritium building | 370 | UCTR |
| Electrical equipment building | 380 | UCEL |
| Administration | 180 | UCAD |
| Control | 350 | UCCO |
| General shop | 115 | UCSH |
| Cryogenic building | 460 | UCCR |

These are implementation defaults, not independently reconstructed estimates. The safety factors are 0.68, 0.84, 0.92 and 1.0; selecting a reduced factor would assert a safety credit. No such credit is established here. The maintenance-equipment account is separate: `ucme = 125000000` dollars before the first-of-kind multiplier. Nuclear ventilation is also separate, with a nonlinear volume formula in account2274. Thus the building rate cannot be described as including all installed nuclear services or all remote-maintenance hardware. General indirects and contingency sit in account9.

S3 provides the original qualification. Printed p140 says maintenance equipment estimates generally use a 1986 CIT basis. Facility costs include overhead cranes; the maintenance-equipment module excludes transfer flasks and equipment development. Printed p141 distinguishes delivered equipment and installation labor from project engineering, procurement, construction services and management. It describes defaults primarily based on September1987 TIBER II. Printed p142 explains why its less detailed systems model can understate equipment quantities and costs. Detailed cost factors are deferred to S. L. Thomson, *Systems Code Cost Accounting*, FEDC-M-88-SE-004, February19,1988. That memo was not acquired. The 1986 maintenance basis is not permission to relabel PROCESS's updated 1990 defaults.

## Kovari family: a different boundary

S5 calls the switch KOVARI_2014 and identifies 2014 dollars; S1 calls it the 2015 Kovari model. This is a cost-year versus method-label distinction. The cited primary cost paper remains identified as in preparation in S1. The 2014 PROCESS physics-paper publication date does not itself establish the building estimate.

S5 defines 1283 USD2014/m³ for the tokamak complex including building and site services, and 270 USD2014/m³ for unshielded non-active buildings. S2 uses `1,100,000 m³ × 1283 × (cryostat_volume / 18,712 m³)` for the complex excluding the hot cell. This is an ITER-reference proxy, not a calculation of the new facility's building volume. Its comments also warn against reporting individual building costs because of shared mean-rate treatment. That conflicts with interpreting the coefficients as calibrated function-specific prices.

The active maintenance facility is separately labeled **with fixed equipment**. Its reference cost is `(95 × number_of_RH_systems + 2562)` million dollars, while moveable equipment is `(139 × number_of_RH_systems + 410)` million dollars. Both scale with armour/first-wall/blanket mass against 4.35 million kg and a cost exponent. Their source comment points to an internal remote-handling location and Sam Ha. No original scope schedule was acquired. Adding these terms to a separately installed hot-cell equipment estimate would need a demonstrated exclusion ledger. Assembly and additional project expenditure are separate accounts; their scope must not be silently absorbed into a universal building-installation multiplier.

## Better alternative: MIT CANES civil quantities

S6 §2.2.3, printed p37, explicitly scales Account21 formwork, reinforcing steel and concrete by their own quantities using Eq2.2. Air/water/steam services instead use building volume. This provides a defensible conceptual method: price concrete volume, reinforcement mass, formwork area and other structural commodities separately, then account for services and equipment explicitly. It better supports layout-dependent shielding thickness and maintenance loads than a single cost per enclosed cubic meter.

The required reference prices are not supplied by the easily mistaken tables. Tables2.4/2.5, printed p35, are labor and material inflation indices from1987 to2018. Table2.6, printed p37, contains equipment and crane fits, not concrete/rebar/formwork unit rates. AppendixI TableI.1, printed p161, contains relative superstructure factors; these are not base costs. Printed pp31–33 defer the235 selected component reference rows to supplemental data. The registered report supports the method, but a numeric civil implementation still needs the original EEDB/NCET Account21 rows: reference quantity and unit, reference labor/material/factory costs, date, exponent and ME/BE treatment. S6 printed p36 also warns against treating its historical-price estimates as standalone absolute costs.

## Recommendation and remaining work

[AGENT] Prefer the S6 commodity method after acquiring its reference rows. Produce shell concrete volumes, reinforcement mass and formwork area from the layout, and preserve separate installed-services and remote-equipment scopes. Keep crane equipment out of a civil rate unless the selected row explicitly includes it. Civil shielding quantity needs an explicit geometric thickness; none of these rates proves its radiological sufficiency.

[AGENT] If a provisional comparison is needed before that acquisition, use the complete 1990 function-rate family above only as a declared historical sensitivity, with safety factor1.0 and a separate unresolved scope account. Preserve original dollar year. No numerical uncertainty interval or present-year escalation is established by this research. Do not interpret mixing the1990 and2014 families as low/high uncertainty bounds.

Outstanding source needs are the EEDB/NCET civil reference rows, the1988 Thomson memo, original ITER/Kovari building/services basis and remote-handling estimate schedule. Their absence prevents claiming a calibrated installed construction and maintenance-facility price. This does not prevent building the physical quantity ledger or disjoint accounting structure.
