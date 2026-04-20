VERDICT: FINDINGS

---

**Source assessment summary:**
- `arxiv-2401-15267`: Only the abstract was extracted (Trafilatura backend, 4 KB). The paper is about flexible WPT arrays for space-to-ground power transfer from a LEO demonstration — Space Solar Power infrastructure, not fusion. No quantitative data is accessible. The analysis already covers SPS-heritage power beaming at TRL 2–3 and ~40–60% efficiency; this source adds no material content beyond confirming small-scale LEO WPT demonstrations continue.
- `everycrsreport-reports-r41419`: CRS Report R41419 (2011), "The Helium-3 Shortage: Supply, Demand, and Options for Congress." This is a substantive 89 KB policy and supply-chain report. It provides He3 production volumes, cost data, regulatory context, and supply risk assessment not fully reflected in the current analysis.

---

### F-1: He3 export controls and dual-use regulatory barriers absent from challenge and risk coverage

- **Target:** Section 2 (He3 supply challenge) and Section 6 (Gap 14)
- **Category:** analysis
- **Finding:** The analysis thoroughly covers He3 as an economic and market-availability problem but treats the supply constraint as purely a physical scarcity issue. CRS R41419 establishes that He3 and tritium are export-controlled dual-use materials subject to inter-agency oversight (DOE, DHS, DOD, NSC) and nonproliferation scrutiny. Procurement for a commercial program requires government-to-company supply agreements subject to political and policy constraints — including rationing decisions by the Interagency Policy Committee (which in 2009–2011 actively cut allocations to science programs to prioritize security uses). This is a distinct risk dimension from the physical scarcity already described. The current Section 6 Gap 14 covers only nuclear operations in LEO (IAEA/COPUOS); He3/tritium procurement controls are a separate regulatory track not mentioned anywhere in the analysis.
- **Recommendation:** Add a sentence to the Section 2 He3 supply discussion noting that commercial He3 procurement also faces export control regulatory complexity: He3 and tritium are dual-use controlled materials; U.S. government allocation has historically been rationed and prioritized for security over science; international procurement faces analogous restrictions. Update Gap 14 in Section 6 to distinguish two regulatory tracks — (1) nuclear safety in LEO (already covered) and (2) He3/tritium export controls and dual-use procurement regulations (add CRS R41419 as the source reference). This adds a policy-risk dimension to the already-blocking He3 supply challenge.
- **Priority:** important

---

### F-2: He3 fuel cost scenario range is too narrow — production cost alternatives are absent from the parameter table

- **Target:** Section 5 (LCOE-Relevant Parameters) and Section 2 (He3 supply challenge)
- **Category:** model
- **Finding:** The analysis parametrizes He3 cost at a single market price point (~$5,000–6,000/std L) without a scenario range. CRS R41419 provides a production cost range from alternative supply pathways: ~$300/liter incremental extraction from existing natural gas processing infrastructure (lowest credible long-run supply cost if scaled), to ~$12,000/liter full-cost natural gas extraction, to $11,000–18,000/liter for unsubsidized new tritium production. The lower bound ($300/liter) differs from the current market price by roughly 15–20×. For LCOE scenario modeling — even as a sensitivity parameter — this range matters: if long-run commercial He3 production infrastructure were established, it would substantially change the D-He3 fuel cost outlook relative to current market price. The current Section 5 table presents only one number and does not acknowledge that production cost and market allocation price are different quantities. Note: CRS data is from 2011 and current costs will differ; the order-of-magnitude spread remains relevant for scenario bounding.
- **Recommendation:** Add a second He3 cost row in Section 5 distinguishing market price (current, ~$5,000–6,000/std L) from estimated long-run production cost range ($300–18,000/liter from CRS R41419, 2011 basis). Add a note in Section 2 that the fuel cost sensitivity depends on whether commercial He3 production infrastructure is ever developed: the $300/liter lower bound (incremental natural gas extraction) versus $5,000+ market allocation price defines a scenario branch in the LCOE model, not just a single uncertain parameter. This gives the model a defensible range for He3 fuel cost scenarios rather than a single point.
- **Priority:** important
