# Lifecycle study scenario plan

[AGENT] Preparation only, 2026-09-22. Authority: WI-091 design accepted at `b4ed8ecb`; T-004 preparation brief. No package or oracle points have run. Exact maps, generated-key expansion, indicators and gates await a stable committed package and coordinator release.

## One question

How do explicitly selected finance and net-new-tritium assumptions change complete conditional lifecycle cost per net MWh of the same integrated ARIES plant, and does native electricity/cost propagation preserve that accounting under fixed-hardware demand changes?

[OWNER-VERBATIM] “Report LCOE separately for the no-breeding-credit case and explicitly defined tritium-supply scenarios. Clarify the supplied recovery boundary and prevent double-counting exhaust recycling. Do not present increased recovery as free equipment improvement or optimize it without a supporting model. Complete the terminal-cost boundary, apply financing once, and use either replacement cashflows or the reserve—not both.” Source: retained owner supplement.

[OWNER-VERBATIM] “For this prompt, I authorize explicitly labeled diagnostic/sensitivity-only sweeps of declared assumptions even when no modeled constraint resists them. Record the missing constraint response and development finding before execution.” Source: retained owner brief, Studies, logging and delivery.

## Cases and scope

[AGENT] Target approximately 64 unique complete maps. Every point starts from an author canonical map; normalization to numeric floats preserves exact numeric values. Final count is established by full-map deduplication with all scenario aliases retained before execution. No Cartesian sweep or optimum is proposed. All financial windows are engineered assumption ranges from design F1–F8, not distributions.

| Block | Proposed coverage | Expected new maps |
| --- | --- | --- |
| Canonical | All four predecessor physical/source cases with current finance; baseline no-credit plus assumed net extracted breeder feed of 100 kg/calendar year charged 30 million USD2004/year | 5 |
| Discount | r=0, 1e-12, .03, .08, .10 for both no-credit and named-feed baselines; nominal .05 already present | 10 |
| Construction | T=0,4,10 years for both supply scenarios; nominal6 already present | 6 |
| Calendar life | N=20,30,60 years for both supply scenarios; nominal40 already present | 6 |
| Availability | A=.60,.75,.95 for both supply scenarios; R and supply-service charge held fixed within each scenario | 6 |
| Major cost assumptions | Selected nuclear-island price, unallocated source-scope price, tritium price, routine O&M, consumables: two endpoints each on no-credit baseline | 10 |
| Terminal/overhaul | Gross terminal fraction .05,.20; salvage0,.05; overhaul fraction0,.10; overhaul year15,30 | 8 |
| Blanket replacement | Lifetime2,8 FPY and event factor .5,2; reserve remains excluded | 4 |
| New feed and service | R=50,110 kg/y at fixed30m service; service10m,100m at fixed100kg/y | 4 |
| Fixed-hardware propagation | Density amplitude4.5e20,5.5e20 on named-feed case, holding R100 and service30m fixed | 2 |
| Purchased equipment | Helium exchanger selected area5000,75000 m2 on no-credit case; demand unchanged; retain engineering violations and actual purchase-cost response | 2 |
| Joint analytic limit | r=0 and T=0 on no-credit baseline | 1 |

[AGENT] Provisional total is64 before exact canonical deduplication. Exact nuclear-island price owner and all key names will be checked against the actual generated interface; an absent planned owner must be resolved explicitly before preparation. Existing predecessor endpoints for T price are10m/100m USD2004/kg, routine O&M35m/140m USD2004/year, consumables1m/15m USD2004/year, ordinary purchase factors.5/1.5 and unallocated source scope.5/2. The existing published input `fuel_inventory.annual_recovery_kg` now means net NEW extracted supply outside the internal exhaust recycling loop; inherited99% internal exhaust recovery stays fixed. Missing production capability and service-price response are recorded as development gaps, not inferred improvements.

[AGENT] Source-conditioned finance is calculated by the separately named native branch at every supported point. It substitutes already-financed inclusive capital, supplied1000MW and T=0; recurring expenses and blanket events are held relative to that point, while terminal/salvage/overhaul fractions scale the substituted capital. Its price is a scope comparison, not a source reconstruction. The original terminal figure in USD1992 remains unmatched.

## Predeclared negative controls

[INHERITED: accepted design] Nonpositive calculated net power, negative real discount, noninteger/nonpositive operating life and unsupported schedule/date controls are genuine refused native attempts outside the finite-LCOE sensitivity set. Request the author's canonical negative-control receipts first. Reuse only exact final-package identities and full input maps, preserving actual failure status, reason and available upstream diagnostic outputs; otherwise declare fresh control proposals before separate released execution. Undefined LCOE stays absent. These controls do not count toward all-point finite numerical coverage and cannot make a failed sensitivity point disappear.

## Verification and export

[AGENT] `lifecycle_oracle.py` independently enumerates end-year operating/energy payments and replacement events with60-digit Decimal discount factors. It does not import production finance code, CRF helpers or native outputs. It checks contribution sums, energy agreement and schedule counts, then provides integrated and source-conditioned accounting comparisons through bindings to be added after ABI delivery. The physical/equipment oracle remains reused unchanged except for the explicit finance extension at its integration boundary. All compact-study points will be checked, with exact predicate derivation. Existing declared residual tolerance remains scoped; any additional absolute tolerance requires quantified numerical evidence before use.

[AGENT] A record-local executor will retain stock StudyRunner and PreparedListStrategy and match exported rows by complete numeric dictionary equality. It will reject duplicate normalized maps and ambiguous/missing matches before writing reports. This avoids the known integer/float JSON spelling failure. No evaluator rerun or shared verifier/gate change is planned. Native database/evidence files and full input/output/verdict maps remain retained; any recovery queries an immutable read-only or disposable copy, with persistent hashes checked.

[AGENT] Before execution, the formal record will contain all17 native headings, intake, complete axes with generated-key provenance, all indicators, owner rulings, missing-response findings and preflight results. Freeze/integration/commits remain coordinator-owned. This first preparation artifact does not claim readiness of the unbuilt interface or native gate results.
