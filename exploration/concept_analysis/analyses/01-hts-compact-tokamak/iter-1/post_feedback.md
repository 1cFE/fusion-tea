VERDICT: FINDINGS

### F-1: No explicit differentiator list vs. conventional tokamak
- **Target:** Section 7 (Cross-Concept Notes) and overall framing (Goals 1–2)
- **Finding:** The analysis compares ARC against three approved concepts (ST-HTS, FRC, MagLIF) but never explicitly lists the key differentiators from the reference case — a conventional large-bore LTS tokamak (ITER/ARIES-RS class). The differentiators (HTS enabling compact high-field geometry, demountable coils, FLiBe liquid blanket vs. solid ceramic breeder, I-mode physics basis, high bootstrap fraction enabling non-inductive drive) are scattered through the narrative but not structured as a comparison list. A reader cannot quickly identify what is novel vs. borrowed from conventional tokamak practice.
- **Recommendation:** Add a brief structured comparison against a conventional tokamak (ITER or ARIES-RS class) — 4–6 bullet differentiators, each labeled as novel or borrowed, with a single-sentence cost implication. This can be a paragraph in Section 7 or a short table at the top of the analysis. The differentiators are already in the text; they just need to be surfaced as an explicit list.
- **Priority:** important

### F-2: Modeling approach recommendation absent
- **Target:** Section 5 or equivalent (Goal 4)
- **Finding:** The analysis nowhere addresses how ARC should be modeled: whether a structured costing framework (e.g., pyFECONS / 1costingfe) or free-form cost estimation is appropriate, or what the primary modeling strategy should be given the incomplete BOP cost data. This is a required output of the analysis per Goal 4 ("what is the right way to model those differences?"). The parameter table in Section 5 is comprehensive, but it stops at listing parameters without recommending a modeling architecture.
- **Recommendation:** Add a modeling approach subsection (within Section 5 or as a standalone section) that states: (a) whether structured costing or free-form is appropriate for this concept and why — e.g., ARC's $5.56B covers only VV + blanket + magnets, so BOP and indirect costs must be estimated by analogy, which suggests free-form with analogue scaling rather than a framework requiring a complete CAS breakdown; (b) what the primary scaling axes are (REBCO tape cost per kA-m, capacity factor, regulatory cost multiplier); and (c) what the model should not attempt to compute from first principles given data gaps.
- **Priority:** blocking

### F-3: Key hypotheses not stated as testable propositions
- **Target:** Section 2 and Section 5 (Goal 4)
- **Finding:** Section 2 ranks challenges by LCOE impact well, but presents them as concerns rather than testable hypotheses. The TEA model should be organized around a small set of explicit propositions — e.g., "ARC achieves sub-$100/MWh LCOE if and only if REBCO tape cost falls to ~$10/kA-m AND capacity factor exceeds 75%." Without these, the model risks being an accounting exercise rather than a test of the concept's viability claims. Goal 4 explicitly requires hypotheses stated as testable propositions, not open questions.
- **Recommendation:** Add 2–3 testable hypotheses, each framed as a conditional claim: "Hypothesis: [outcome] holds if [parameter] is in [range]." Candidates from the existing analysis: (1) REBCO cost trajectory hypothesis (tape price determines whether magnet cost is competitive); (2) capacity factor hypothesis (ARC is CAPEX-heavy, so a 2× CF swing dominates LCOE more than any other variable); (3) I-mode extrapolation hypothesis (if I-mode is inaccessible at ARC parameters, recirculating power fraction increases enough to push Qe below economic threshold). These are already implied in Section 2 — they just need to be made explicit.
- **Priority:** important
