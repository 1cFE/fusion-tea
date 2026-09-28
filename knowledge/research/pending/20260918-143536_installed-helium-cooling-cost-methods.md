---
date: 2026-09-18
researcher: cost_research
topic: installed-cooling-equipment-costs
tags: [helium, installed-cost, IHX, circulator, piping]
research_type: source-method-applicability
---

# Installed helium cooling equipment: source methods and bounded gaps

[AGENT] No transferable installed equipment price or complete price interval was established. The search found two directly relevant NGNP original reports, but their original downloads failed. One independent INL installed-cost methodology was registered. It applies to low-temperature LWR heat delivery, so its prices and scaling coefficients cannot be transferred to the retained helium system. This is a bounded acquisition and applicability result, not a claim that helium cost evidence does not exist.

## Question and retained scope

[INHERITED: work/orchestration/goals/installed-cooling-equipment-costs/evidence/research-brief.md] Seek conceptual installed helium circulator, piping and IHX costing methods for 8 MPa helium at 300–500 C. The selected design requires eighteen representative circuits and about 3013.915 MW total IHX duty. These are sizing requirements, not hardware qualification. No model, inherited allowance, acceptance predicate, or goal state changed in this research.

## Source families and results

| Family | Evidence examined | What is supported | What remains unavailable |
|---|---|---|---|
| EU DEMO HCPB engineering | Previously registered Barucca et al. 2022, `knowledge/sources/maturation_of_critical_technologies_for_the_demo_balance_of/output.md:495` and `:497`; prior native acquisition in `work/orchestration/goals/primary-loop-sizing/evidence/cost-research.md` | Preliminary supplier budgetary offers exist; circulators and main exchangers are important cost components; largest pipes above DN 850 were omitted from that assessment. | Numerical supplier quotes, currency and price year, complete installation scope, and transfer law. Internal Bubelis deliverable remains a named source gap. |
| NGNP helium transport and independent equipment costing | General Atomics report 911105 revision 0, 6 April 2007; Dominion Engineering memorandum M-6914-00-04 revision 1, 18 March 2011. Search and web tools used only for triage. Original institutional URLs and registration failures are recorded in the native return. | Concrete original candidate identities and where to seek original helium transport/equipment costing evidence. | Native original capture, verification of numerical tables, currency year, installation inclusions, detailed transfer applicability. Cached web text is not admitted as model evidence or copied as a cost table. |
| INL installed thermal delivery methodology | Knighton et al., INL/EXT-20-58884 revision 1, June 2020, registered at `knowledge/sources/inl_markets_and_economics_for_thermal_power_extraction_from/` | Actual installed-equipment estimating workflow and stated omissions, described below. | Applicable high-pressure helium prices and engineering-specific installation estimates. This source does not supply those. |

## Registered installed-cost method

The INL source was downloaded from `https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_26712.pdf`, screened before content inspection using `scripts/holdout_guard.py` with zero term matches across 66 pages, and captured through `scripts/source_registry.py register --local-pdf`. Raw SHA256 is `fec51bddcae7f50089196c288cabda8b29aa44905b53d14c933e04a534a3044b`. The source concerns existing LWR process heat. No barred source or derivative was read.

Section 6.2 uses process mass and energy balances to establish equipment specifications, then Aspen Process Economic Analyzer to estimate installed cost. The installation boundary includes structural components, instrumentation, piping, paint, insulation, materials and labor, including ancillary connections between adjacent equipment. Section 6.2.1 uses exchanger area from Aspen Exchanger Design and Rating plus design pressure and temperature. Pipe length is specified; diameter follows fluid phase and flow. Pump estimates follow flow. Source: registered `output.md:651–667`, original printed pp 25–26.

The source defaults to carbon steel and explicitly omits expansion vessels or surge tanks and their fluid inventories. Its end-use application requires approximately 175 C or less, and its economics assume no additional operating labor, no deterioration in heat production, and a simplified finance calculation excluding taxes, depreciation and decommissioning. Source: `output.md:641–667`, original printed pp 24–26. These assumptions do not establish maintenance or replacement obligations for the retained helium circuits.

[AGENT] This is usable as a specification for an estimate, not as a helium cost correlation. It shows why thermal duty alone cannot select an installed price. The source's separate steam-boiler capacity exponent belongs to a different purchased-equipment estimate and is not a permissible IHX or circulator exponent.

## Required estimate boundary

[AGENT] A defensible conceptual estimate can be organized as the following identity, with each term independently priced and overlaps removed: installed total = circulator packages + IHX packages + process piping and valves + supports and installation labor + instrumentation/electrical connections + insulation + engineering/testing allowances supported by the chosen estimate method. This is an accounting proposal, not a source-derived set of numerical factors.

| Item | Physical specification needed | Price evidence still needed | Transfer restriction |
|---|---|---|---|
| Circulator | Helium inlet density and temperature, pressure, flow, required head, shaft/electrical power, motor/drive/bearing/seal arrangement, number and redundancy | Helium-specific procurement quote or verified correlation with price year and drive/package inclusions; installation labor and connection scope | Pumping MW alone does not establish a gas-machine purchase cost or physical availability. |
| IHX | Both fluids, both pressure and temperature profiles, duty per module, approach temperature, allowable losses, area, exchanger technology, alloy, pressure boundary and module count | Verified area/mass/design-specific equipment method or quote; fabrication and installation separated | The 8 MPa helium primary and required duty do not specify secondary pressure/fluid or heat-transfer area. PCHE, shell-and-tube and finned designs are not interchangeable price anchors. |
| Piping and valves | Routed lengths, diameters, wall thickness, alloy, fittings, insulation, supports, welds and valve schedule | Fabricated pipe, fittings/valves, installation and QA labor, currency/year | Raw alloy price alone misses fabrication/installation. DN850 omission in the DEMO source directly matters when larger pipes are needed. |
| Lifecycle | Service intervals, replaceable parts, inspection/downtime, lifetime and availability assumptions | Replacement procurement/labor and incremental O&M, with clear boundary against existing operating allowance | Neither a publication year nor an electrical energy charge supplies maintenance and replacement cost. |

[AGENT] No pressure multiplier, temperature multiplier, installation factor, water-pump price, currency conversion, inflation adjustment, or unverified scaling exponent was introduced. Publication years are bibliographic dates, not established capital price years. No all-in interval was computed by combining unrelated equipment anchors.

## Actual investigation and native record

Request: `knowledge/research/requests/REQ-COOL-INSTALL-01.json`. Initial run: `knowledge/research/requests/runs/REQ-COOL-INSTALL-01/20260918T213031349204/`. Its native return is REGISTERED with two queued sources and no bounded negative. The source registration receipt, extraction logs and request history are retained.

The first six logged entries encode eight search-engine queries because two entries paired adjacent queries. Three further entries record two targeted NGNP queries and the OSTI API query, totaling eleven query strings in nine log entries. Queries covered OSTI NGNP circulators/IHX cost; INL HTGR piping/circulator capital cost; GA 911105 helium cost; PCHE/NGNP cost correlations; exact GA and Dominion titles; exact titles excluding the broken INL host; targeted911105 PDF and OSTI title queries; and the OSTI API. OSTI's first ten results did not provide either target original. The existing DEMO source was reread rather than reacquired.

[AGENT] Procedural deviation: the request was initially opened with a six-search limit. Its file was later amended to twelve, but the open run retained its original limit snapshot. The eleven actual query strings therefore exceeded the initial bound; the return reports max_searches. This history is disclosed rather than relabeled exhausted. The coordinator authorized additional retrieval work; the explicit native continuation below preserves the corrected prospective bound and remaining queue. Three capture attempts were made: one succeeded and two failed. No failed attempt is counted as a registered helium source.

Additional retrieval checks: the GA original URL returned 404 by unsandboxed HTTPS and HTTP; a prospective migrated WordPress path also returned 404. The Dominion original returned 404. The INL WordPress search API and NGNP landing path returned 403. Internet Archive availability returned 429. Web-open triage could access cached text for GA, but both requested original PDF screenshots, pages 26–27, failed with cache-miss. Native URL registrations failed extraction. These are acquisition failures, not evidence that the underlying cost methods lack value.

## Disposition and next useful action

[AGENT] Preserve the installed subtotal as unresolved. Obtain either NGNP original from INL document services or an accessible archive, then verify its equipment tables, cost-year convention, installation exclusions and operating envelope before considering transfer. Existing high-pressure DEMO geometries could supply a more relevant physical sizing basis, but combining them with an unrelated source price requires an explicit, justified bridge. A helium-specific supplier/budget estimate based on the table above is an alternative. The absence of the internal EUROfusion report alone was not used as exhaustion.

[AGENT] No domain insight was minted or approved. The research remains pending. The registered INL source supports estimate structure only and does not justify a production-model cost replacement.

## Continuation result and conceptual release inputs

[AGENT] The authorized continuation `knowledge/research/requests/runs/REQ-COOL-INSTALL-01-CONT/20260918T213554641136/return.json` closed OPERATOR_QUEUE after nineteen distinct logged searches under a prospective twenty-search bound. Twelve were performed by the coordinator and seven by this researcher. It registered no new source and produced no bounded negative. The native close token `exhausted` describes the attempted retrieval routes in this invocation; it does not establish that a source family or all accessible literature is exhausted. The searchable queued request remains open to new evidence.

Two further original candidates were investigated: NGNP Steam Generator Alternatives Study, report 911120/0, at the INL URL recorded in the queue; and Stewart et al., *Economic solution for low carbon process heat: A horizontal, compact high temperature gas reactor*, Applied Energy 304 (2021), DOI `10.1016/j.apenergy.2021.117650`. The former returned HTTP 404. The latter returned 403 from the publisher and author-uploaded ResearchGate PDF; its publisher API supplied bibliographic metadata only, full-text view returned 401, and PDF retrieval returned 406. Thus their potentially useful installed-cost table and helium cost methodology remain retrieval gaps. Their actual formulas, installation scope and transfer validity are not certified by this research.

The accessible INL follow-up *Quantifying Capital Cost Reduction Pathways for Advanced Nuclear Reactors*, INL/RPT-24-7767, June 6, 2024, was downloaded from `https://inldigitallibrary.inl.gov/sites/STI/STI/Sort_109810.pdf`. All 80 pages passed a term pre-screen before reading. Targeted inspection found general capital-cost and construction methodology with a citation to Stewart 2021, but no helium circulator, IHX or piping-specific method. It was rejected for this request and not registered. The accessible LWR installed method has an applicability gap; the four queued originals have retrieval gaps. These are distinct limitations.

[AGENT] A conceptual estimate does not require vendor quotations as its only acceptable authority. An acquired published reference estimate can support an explicit conditional model if its scope and engineering transfer are justified. Possible routes are: a reference circulator package scaled by a documented power/flow/head law; an exchanger area or manufactured-mass method with verified material, pressure and temperature domain; or a pipe bill of quantities with published fabrication/installation labor and unit-cost bases. None of those laws or complete anchors was verified here, so none was implemented.

[AGENT] Release inputs for a future conceptual implementation are concrete: (1) readable original cost equation/table with currency and base year; (2) equipment-only versus installed inclusions and exclusions; (3) a selected reference equipment design, count and physical scaling attribute; (4) target helium conditions and equipment sizing inputs, including secondary IHX conditions and piping geometry; (5) justified transfer across scale, materials, pressure and temperature with uncertainty or stated extrapolation; (6) a currency/year normalization method compatible with the model accounting; (7) a nonoverlapping replacement/addition boundary against the inherited aggregate coolant account; and (8) explicit treatment or exclusion of replacement, maintenance and downtime. These are agent-proposed evidence requirements for an auditable estimate, not owner-originated settled requirements. Physical engineering qualification can remain separately unresolved at the conceptual costing stage.
