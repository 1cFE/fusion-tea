VERDICT: FINDINGS

---

**Source assessment note**: Both new source files (`aries-cs-compact-stellarator-study.md` and
`aries-cs-systems-optimization.md`) are OSTI metadata extracts — abstract and bibliographic
information only, no full article content. Numerical data is absent. The findings below are
based on claims in the abstracts that are not addressed in the existing analysis.

---

### F-1: Alpha particle confinement not addressed — a key QI differentiator is missing

- **Target:** Section 2 (Challenges) and Section 7 (Cross-Concept Notes)
- **Finding:** The ARIES-CS Phase 1 study (compact-stellarator-study source) explicitly identifies
  "high alpha particle loss" as a critical issue for compact stellarator configurations. The
  existing analysis does not address alpha particle confinement anywhere — not as a challenge,
  not as a resolved risk, and not as a differentiator. This is a material gap in Goal 2 (Key
  Differentiators) and Goal 5 (Risks and Assumptions). The QI optimization strategy is
  specifically designed to improve fast-particle (alpha) confinement by minimizing trapped-particle
  radial drifts — this is arguably the defining physics advantage of the QI approach over other
  stellarator symmetries (QA, QH) and a key differentiator from compact tokamaks where alpha
  confinement is a known challenge at low aspect ratio. Whether the ARIES-CS finding applies to
  Stellaris (QI) or only to the QA configurations ARIES-CS actually studied is exactly the
  distinction the analysis should draw. If QI optimization resolves this problem, it strengthens
  the burning plasma assumption (H4). If residual alpha losses persist at Stellaris scale, it
  undermines H4 and affects the energy balance calculation.
- **Recommendation:** Add a subsection in Section 2 or a note in the "Recommended Modeling
  Approach" addressing alpha particle confinement: (1) state that ARIES-CS compact stellarators
  identified high alpha particle loss as a critical issue, (2) explain that QI optimization
  specifically targets this problem through control of the second adiabatic invariant J∥, making
  W7-X the experimental proof of concept, (3) assess residual risk for Stellaris — is the QI
  confinement quality at Stellaris scale (larger device, stronger field) sufficient to ensure
  alpha self-heating drives ignition, or does the compact geometry re-introduce alpha loss
  pathways? This connects directly to H4 and should be flagged as a physics assumption the SMC
  demo cannot validate (requires burning plasma conditions).
- **Priority:** important

---

### F-2: ARIES-CS is QA, not QI — the analogue distinction needs to be stated

- **Target:** Section 1 (Availability of Data) and Section 6 (Data Gap Inventory)
- **Finding:** The systems-optimization source abstract explicitly refers to "issues for the
  development of compact quasi-axisymmetric (QA) stellarators" — confirming that ARIES-CS
  studied QA configurations, not QI. The existing analysis cites ARIES-CS as a cost floor
  analogue for Stellaris (a QI device) without noting this distinction. QA and QI optimize
  different quantities (quasi-axisymmetry vs. quasi-isodynamicity), have different coil topology
  implications, and different alpha particle confinement properties. Using ARIES-CS as a cost
  floor is reasonable, but the analysis should acknowledge that the analogue gap is larger than
  just LTS vs. HTS — it also spans different symmetry classes with different physics and
  potentially different cost structures (especially in the coil account, where QA coils may
  differ from QI coils in geometric complexity). This affects how confidently the ARIES-CS
  floor should be relied upon in Section 5 and Section 6.
- **Recommendation:** In Section 1 where ARIES-CS is introduced as a reference, add a sentence
  noting that ARIES-CS studied QA (quasi-axisymmetric) configurations, not QI, and that the
  cost floor inference carries an additional structural assumption: that QA and QI stellarators
  of similar size and field have comparable cost structures. In Section 6, Gap #1 (capital cost),
  update the source recommendation to note the QA/QI distinction as a caveat on the ARIES-CS
  analogue.
- **Priority:** minor
