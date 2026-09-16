---
date: 2026-09-16
researcher: Codex goal coordinator
topic: primary-loop-sizing
tags: [helium, cooling, capacity, cost]
research_type: source-and-model-trace
---

# Explicit primary-loop sizing: evidence and supported use

## Research question

[OWNER] Make primary-loop capacity follow an explicitly sized cooling system, with consistent heat removal, flow, pressure drop, pumping power and cost. Preserve the existing coolant, divertor limit and magnet constraints; a quantified capacity requirement and explicit evidence gap are valid results where sizing is unsupported.

## Findings

- [INHERITED: current model] `models/library/analyses/mfe_primary_loop.sysml` already computes flow from source heat divided by coolant heat capacity and temperature rise, then per-loop flow from explicit loop count. Pressure loss follows squared relative flow; compressor work enters both recirculating electricity and recovered IHX heat. `models/designs/stellarator_09/stellarator_plant.sysml:1148` holds fourteen loops.
- [SOURCE] `knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md` §§2.1–2.2, Tables 1–3 supplies a nominal 2025.7 kg/s design with three inboard and six outboard loops, two circulators and one IHX per loop. It does not establish 225.0778 kg/s as a manufacturer maximum. The existing model's average-module transfer and flow screen are assumptions; branch topology and losses differ.
- [AGENT] Existing integer-count input can quantify a conditional accommodation without altering the flow allowance. It does not establish routing, compressor-map margin, exchanger off-design capacity or a pipe-area law. Full source trace and original-table review are in `work/orchestration/goals/primary-loop-sizing/evidence/hydraulic-source-account.md` and `source-review.md`.
- [INHERITED: current model] `models/library/analyses/mfe_account_costs.sysml:532` prices coolant with net/thermal-power correlations. Added-loop hardware does not enter that cost equation. Its indirect response cannot establish the installed price of an added loop; see goal `evidence/entering-cost-account.md`.
- [SOURCE] `knowledge/sources/maturation_of_critical_technologies_for_the_demo_balance_of/output.md:495` reports preliminary cost assessment, expensive helium circulators/main exchangers and omitted piping above DN 850. Line 497 reports supplier budgetary offers. Reference 37 at line682 names the unacquired internal report BOP-3.1-T012-D001, EFDA_D_2NSZ4M. No installed unit price, currency or cost basis year is established here. Native acquisition and provenance: goal `evidence/cost-research.md` and requests REQ-LOOP-COST-01/REQ-LOOP-COST-01-CONT.

## Supported use and gaps

[AGENT] A bounded native loop-count diagnostic can report required flow, pressure loss, pumping, recovered heat, required IHX duty, conditional equipment counts and separate predicates. Its price result is an explicit evidence gap, with numerical aggregate-cost responses labelled as inherited accounting. Area enlargement and qualified hardware replication need geometry and equipment evidence. No new source-based price or hydraulic law is supported by this investigation.

[AGENT] No new DI entry or approval is requested as a prerequisite to the already reviewed conditional diagnostic. This report remains pending research curation. The goal owns its final interpretation and review.
