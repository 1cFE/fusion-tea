# Civil commodity cost basis

Date: 2026-09-18. Researcher: delegated cost-source reader. Consumer: T-004 / REQ-LBF-02 / WI-068 LF-04. Research type: primary data acquisition. Recommendations are [AGENT]; no DI entries were approved.

## Result

**The original MIT TIMCAT civil reference rows were recovered intact.** They provide installed-direct site labor and material costs for concrete, reinforcement and formwork, with original quantities. They support a conditional commodity estimate using declared transfer assumptions. They do not by themselves price all building services or remote maintenance equipment.

Native result: `knowledge/research/requests/runs/REQ-LBF-02/20260919T012251395930/return.json`, class REGISTERED. Registered source: `knowledge/sources/mit_timcat_pwr12_me_civil_reference_cost_csv_pinned_html/`. Registry verification: zero faults and three pre-existing legacy entries. Two search queries and three registration attempts were made; the raw CSV and readme attempts failed because the native extractor rejects text/plain. The supported GitHub HTML capture succeeded. The return retains both failures in its queue; the CSV content gap is resolved through the registered HTML, while no readme source was registered. Close used adequacy limit_reached after three attempts; the seam reports limit_reached null, which is retained unchanged.

## Source identity and exact recovery

Primary repository: MIT CRPG TIMCAT, commit `efd801ad7c1530d6c58b342c55765b523b67cc89`, file `PWR12_ME_inflated_reduced.csv`. Registered URL: `https://github.com/mit-crpg/TIMCAT/blob/efd801ad7c1530d6c58b342c55765b523b67cc89/PWR12_ME_inflated_reduced.csv`. Registered raw.html SHA256: `a555257877cb617788e7f9d56e763b7d9c8ada05e69f307d4b1358480a26f1db`.

The captured HTML contains an application/json script whose nested object has a `rawLines` array. Recursively locate this key, join its 862 strings with newline, and append a final newline. This reconstructs the CSV exactly: 110,944 bytes, 861 data records, SHA256 `7efdc5991e0f14972ff8822b07517b7dff2c282f947849cd96e11159aa428c9a`. An independently fetched raw file at the same pinned revision matched byte for byte. The registered HTML, rather than the temporary download or flattened output.md, is the durable source. No manual registry write or source conversion was used.

The original report, already registered at `knowledge/sources/mit_canes_capital_cost_evaluation_of_advanced_water_cooled/`, establishes EEDB PWR12 median-experience treatment and the 2018 cost basis in §2.2–2.2.3, printed pp31–37. Its preface identifies this repository. The repository readme was used for discovery/triage only; cost-year attribution here rests on the registered report and exact named reference file. The source was screened as MIT's water-reactor civil dataset before capture. No excluded concept source was opened.

## Usable reference rows

All monetary values below are USD2018. Source rows are selected by exact `Account` key in the CSV. Each listed row has factory equipment cost zero and NQA1 flag1. Labor and material columns preserve the source values; derived rates are rounded for display only. These are reference nuclear construction costs, not supplier quotes. Substructure rows contain `.13`; superstructure rows contain `.141`; reactor interior rows contain `.140`.

| Account | Commodity | Reference quantity | Site labor cost | Site material cost | Derived total per source unit |
|---|---|---:|---:|---:|---:|
| A.215.131 | Auxiliary-building substructure formwork | 3100 SF | 182434.8277 | 19191.92427 | 65.041/SF |
| A.215.132 | Auxiliary-building substructure rebar | 260 TN | 568568.0349 | 546291.652 | 4287.922/TN |
| A.215.133 | Auxiliary-building substructure concrete | 2100 CY | 358772.036 | 354136.3796 | 339.480/CY |
| A.215.1411 | Auxiliary-building superstructure formwork | 234300 SF | 14196509.53 | 1403236.116 | 66.580/SF |
| A.215.1412 | Auxiliary-building superstructure rebar | 1700 TN | 4861416.797 | 3571906.955 | 4960.779/TN |
| A.215.1413 | Auxiliary-building superstructure concrete | 11800 CY | 3527928.923 | 1989909.18 | 467.613/CY |
| A.216.131 | Waste-building substructure formwork | 9900 SF | 593213.7835 | 62961.76091 | 66.280/SF |
| A.216.132 | Waste-building substructure rebar | 305 TN | 679099.5953 | 658318.2566 | 4384.977/TN |
| A.216.133 | Waste-building substructure concrete | 6000 CY | 1043699.881 | 1039411.081 | 347.185/CY |
| A.216.1411 | Waste-building superstructure formwork | 194000 SF | 11980722 | 1193793.145 | 67.910/SF |
| A.216.1412 | Waste-building superstructure rebar | 1200 TN | 3493972.435 | 2590104.616 | 5070.064/TN |
| A.216.1413 | Waste-building superstructure concrete | 8300 CY | 2526626.061 | 1437851.996 | 477.648/CY |
| A.212.1401 | Reactor interior formwork | 100000 SF | 12747393.41 | 806176.5625 | 135.536/SF |
| A.212.1402 | Reactor interior rebar | 2100 TN | 8892432.619 | 4582893.259 | 6416.822/TN |
| A.212.1403 | Reactor interior concrete | 8000 CY | 3058256.803 | 1365355.403 | 552.952/CY |

The dimensional conversions are 1 SF = 0.09290304 m² and 1 CY = 0.764554857984 m³. Thus auxiliary-building superstructure formwork is 716.664 USD2018/m² and its concrete is 611.615 USD2018/m³. Waste-building equivalents are 730.976/m² and 624.740/m³. Reactor-interior equivalents are 1458.894/m² and 723.233/m³. Concrete price applies to solid concrete volume, not enclosed building air volume. Formwork uses contact area, not building floor area.

The data labels reinforcing-steel quantity `TN` without expanding the mass convention in this CSV. Preserve the original unit until resolved. [AGENT] A US short-ton interpretation is plausible for this US EEDB dataset, but converting to kilograms must carry that explicit assumption or obtain the original unit glossary; it is not silently established by this capture. Likewise `LT` means a lumped source row for practical use here, not a linear quantity suitable for deriving USD/kg or USD/m³.

## Formula and boundaries

For each selected row, `u = (Factory Equipment Cost + Site Labor Cost + Site Material Cost) / reference_quantity`. A conditional constant-unit-price estimate is `C = u × new_quantity`. The reference's Total Cost column is rounded, so calculate from component columns and retain their original precision. For the rows above the factory term is zero. The site labor cost is already included; adding a generic installation multiplier would duplicate that labor.

The registered report Eq2.2 permits `Cnew = Cref × (Pnew/Pref)^n`, but the CSV does not contain its exponents. Their separate source is `input_scaling_exponents.xlsx` at the pinned revision; it was not registered in this invocation. [AGENT] Choosing n=1 for a material quantity takeoff is a declared constant-unit-cost approximation, not a recovered TIMCAT exponent. It supports transparent comparisons while leaving productivity, height, congestion and safety requirements as explicit transfer uncertainties.

Only sum non-overlapping leaf costs. For example, a formwork/rebar/concrete sum does not contain embedded steel, CADWELDs, liners, joints, waterproofing, painting, structural frames, grating or doors. These have separate rows in the dataset and may matter to a complete facility. An enclosed-volume building price should not be added over the same civil scope. Crane hardware and remote maintenance systems need their own scope rows.

Building services are separate accounts. For A.215.2, the reference has factory7275625.011, labor9356760.837 and material2061848.223 dollars. For A.216.2 the corresponding amounts are1490894.581,4901770.993 and1285089.347. Each has no site reference quantity in this CSV. Their HVAC, plumbing, lighting and elevator subaccounts identify scope, but the reference building volume is not exposed here. Thus these aggregates cannot supply a defensible per-m³ service rate without joining the original building-input spreadsheet. A.212.23 identifies safety HVAC separately, reinforcing that civil concrete rates do not cover nuclear ventilation.

A small disjoint auxiliary-building services set is A.215.21 plumbing/drains (factory7810.607011, labor1525771.059, material359094.3262), A.215.22 ordinary HVAC (6063661.532,5961835.16,1190350.512), A.215.23 safety HVAC (884219.7209,385833.8304,33063.40814), A.215.24 lighting/service power (0,1326729.092,465212.2443), and A.215.25 elevator (319933.1507,156591.6954,14127.73264). All are USD2018 reference amounts; none provides a physical scaling quantity here. These are building services rather than reactor heat-transport equipment. Their specific duty, airflow and boundary with distributed plant utilities still require definition before transfer.

Site preparation offers two physical excavation rows: A.211.7112 earth excavation has120000 CY, site labor763694 and material602348 dollars; A.211.7113 rock excavation has200000 CY, labor9421369 and material3356999. Blank factory fields are consistent with no separate factory contribution to those excavation subtotals; their component sums reproduce the parent open-cut accounting with the other leaf rows. They can conditionally price explicitly calculated excavation volumes. They do not price land purchase, roads, landscaping, fencing, dewatering or fill. General yardwork and railroads are lumped with no usable physical reference quantity in this CSV. Treating these excavation rows as complete site improvements would undercount the boundary.

General indirects remain outside these direct commodity rows. The existing report separates Account9 from Account21 and treats labor/material escalation, learning and modularization independently. No general indirect multiplier, escalation to2026, stochastic confidence interval or qualification against stellarator shielding requirements was established here.

## Proposed use and remaining evidence

[AGENT] Use the auxiliary-building substructure and superstructure rows as a coherent initial civil family, with waste-building and reactor-interior rows as named transfer scenarios. The latter represent different construction functions, not statistical uncertainty bounds. Hot-cell shielding walls may require reactor-interior productivity, but no source here demonstrates that applicability. Keep quantities for basemat, shell, internal shield partitions, reinforcement and formwork separate so the functional choice remains visible.

[AGENT] This acquisition resolves the missing civil base-price evidence for a conditional estimate. It does not close the complete facility boundary. Remaining joins are the TN definition, original scaling exponents, reference volumes/input characteristics for service rows, structural-design-derived steel/formwork quantities, and any additional civil/remote-equipment items selected by the final scope. These are narrower prerequisites than the previous absence of all civil reference rows.
