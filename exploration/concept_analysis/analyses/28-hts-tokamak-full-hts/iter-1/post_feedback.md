VERDICT: FINDINGS

### F-1: Differentiators from conventional tokamak not explicitly listed with cost implications
- **Target:** Section 7 (Cross-Concept Notes) and Section 2 (Challenges)
- **Category:** analysis
- **Finding:** The analysis compares well against ST-E1 (the prior approved analysis) and briefly
  invokes CFS/SPARC as an analogue, but never states an explicit list of what distinguishes this
  concept from a conventional large-aspect-ratio tokamak (e.g., ITER-like baseline). The three
  defining differentiators — (1) full HTS coil set (TF + PF + CS) vs. TF-only HTS or LTS, (2)
  compact high-field geometry enabling higher Q at smaller machine volume, (3) AI-based plasma
  control enabling long-pulse operation — are present in the narrative but not collected into a
  single structured comparison. Without this, the TEA framing is incomplete: the cost implication
  of each differentiator is not stated in one place. The full-HTS coil scope relative to TF-only
  HTS competitors (more REBCO tape, higher CS coil cost, but potentially simpler cryogenics) is
  especially important and appears only in Section 4 prose.
- **Recommendation:** Add a brief differentiator table in Section 7 (or a dedicated paragraph at
  the end of Section 2) listing the 3 key differentiators vs. a conventional tokamak with a cost
  implication column: advantage, penalty, or neutral with one-line reasoning. At minimum, call out
  the full HTS coil scope (penalty: more tape/coil cost, novel CS duty cycle) vs. the partial HTS
  baseline as the single most TEA-relevant differentiator for this concept.
- **Priority:** important

### F-2: Section 2 does not name the 2–3 parameters with highest LCOE sensitivity
- **Target:** Section 2 (Challenges)
- **Category:** analysis
- **Finding:** Section 2 ranks challenges by LCOE impact (Critical / High / Moderate) but does not
  identify the specific parameters with the highest LCOE elasticity for this concept. The model
  output shows availability dominates at −0.94 elasticity, followed by interest rate (+0.64) and
  construction time (+0.26); major radius / elongation are third at +0.15. Section 2 Challenge 4
  correctly notes that "moving from 75% to 85% availability improves LCOE ~12%," which is good,
  but the analysis does not acknowledge that cost of capital (interest rate) is likely the primary
  financial lever for a capital-intensive concept with no commercial design anchor, nor does it flag
  that major radius (the key proxy for plant size given the opaque HH380) is a top structural
  sensitivity. Without this explicit sensitivity hierarchy, the modeling approach section lacks
  guidance on where to concentrate scenario analysis.
- **Recommendation:** Add a sentence or short list at the end of Section 2 naming the 2–3
  parameters with highest LCOE sensitivity for this concept: availability (dominated by AI control
  and full HTS CS reliability), cost of capital (dominant financial lever for capital-heavy concept),
  and major radius / plant scale (dominant structural uncertainty given the absent HH380 design
  point). These should be called out as the axes for scenario sweeps.
- **Priority:** important

### F-3: Key technical bets not framed as testable propositions with explicit failure consequences
- **Target:** Section 2 (Challenges) and model scenario structure
- **Category:** model
- **Finding:** The two critical technical bets — (1) full HTS CS coil reliability at 25 T under
  cyclic EM loading enabling ≥80% availability, and (2) AI plasma control reducing disruption
  frequency enough to sustain long-pulse commercial operation — are identified as challenges but
  not framed as testable hypotheses with explicit failure-mode consequences. The model uses a
  single availability point (80%) that partially captures the first bet but without a low-availability
  scenario (e.g., 60–70%) representing CS coil failure or disruption-limited operation. The
  sensitivity table shows availability elasticity of −0.94, meaning a drop from 80% to 65%
  availability increases LCOE by ~14%, but this failure scenario is never constructed. As a result,
  the model does not bracket the key risk.
- **Recommendation:** Add two explicit scenario branches to the model: a "CS coil reliability
  failure" scenario (availability 65%, add coil replacement cost factor) and a "AI control
  underperforms" scenario (availability 70%, increased disruption frequency penalty). Report LCOE
  under each scenario alongside the base case in the model output. This converts the qualitative
  risk narrative into quantified LCOE bounds that support the concept's TEA positioning.
- **Priority:** important
