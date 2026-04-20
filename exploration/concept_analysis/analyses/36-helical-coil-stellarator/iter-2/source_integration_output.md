VERDICT: FINDINGS

---

**Source assessed:** Kovari, M., Harrington, C., Jenkins, I., and Kiely, C. (2014) "Converting energy from fusion into useful forms," *Proceedings of the Institution of Mechanical Engineers, Part A: Journal of Power and Energy*. doi:10.1177/0957650913514230. (arxiv-1401-4232.md)

**Scope of source:** Comprehensive review of energy conversion systems for fusion power plants — coolants (water, helium, lithium-lead, FLiBe), thermodynamic cycles (Rankine, Brayton, combined), and the constraints imposed by material operating windows and parasitic internal power demands. Covers stellarators, tokamaks, and inertial confinement.

---

### F-1: Stellarator current-drive advantage not distinguished from heating recirculation in cross-concept comparison

- **Target:** Section 7 (Cross-Concept Notes) — Key divergences from the ST-E1 and broader tokamak family
- **Category:** analysis
- **Finding:** The Kovari source explicitly states that stellarators have zero internal power demand for current drive — "A stellarator does not have this issue" — in contrast to tokamaks, which carry both current-drive recirculating power and heating recirculating power. The analysis identifies HESTIA's recirculating power as approximately 50% of gross output (Q_eng = 2.0), and notes ECRH wall-plug (~40 MW) as a dominant component. However, Section 7 does not distinguish that HESTIA's entire recirculating power load is attributable to heating, cryogenics, and BOP — with zero current-drive component. For tokamaks, current drive can consume an additional 10–30% of gross output on top of heating. This is a structural differentiator relevant to Goals 2 and 3: it means HESTIA's Q_eng figure is not directly comparable to tokamak Q_eng figures that must also absorb current-drive losses, and that the recirculating power margin is structured differently even when the headline Q_eng numbers appear similar.
- **Recommendation:** Add a paragraph to Section 7 under the key divergences block noting that stellarators carry zero current-drive recirculating power (confirming the Kovari review). Clarify that HESTIA's Q_eng = 2.0 figure includes ECRH heating (~40 MW wall-plug) and cryogenic/BOP loads but no current-drive term — and that this is why steady-state operation does not carry the same recirculating power structure as current-driven tokamaks. This is relevant when comparing HESTIA's Q_eng to published tokamak Q_eng values; a tokamak at Q_eng = 2.0 pays an additional current-drive cost that HESTIA does not.
- **Priority:** important

---

### F-2: sCO₂ efficiency ceiling anchored to CSP literature rather than fusion-specific review; Kovari "no consistent solution" finding not incorporated

- **Target:** Section 2, Challenge 4 (Novel power conversion — sCO₂ at >50% efficiency — undemonstrated at scale) and Section 3 (sCO₂ Brayton Power Conversion — TRL 3–4)
- **Category:** analysis
- **Finding:** The analysis cites "~40–47% in CSP applications" as the state-of-the-art reference for sCO₂ Brayton efficiency. The Kovari source is a fusion-specific review that independently establishes **47% gross efficiency** for a CO₂ recompression Brayton cycle combined with a Rankine bottoming cycle in a fusion plant design study — confirming the upper bound but in the fusion engineering context rather than CSP. More importantly, the Kovari review concludes that "no fully consistent solution for engineering design, coolant and working cycle" has been found for fusion energy conversion. This is a substantive finding that goes beyond "the specific HESTIA target is undemonstrated" — it characterizes the field-wide state as unresolved. The analysis frames the sCO₂ risk as HESTIA-specific (the concept has set an aggressive target), but the Kovari review indicates the underlying challenge is endemic to fusion energy conversion more broadly. This distinction matters for how the risk is framed in TEA terms (Goal 5): is this a HESTIA-specific execution risk, or a cross-concept design uncertainty that affects all fusion concepts?
- **Recommendation:** In Section 2 Challenge 4, update the efficiency reference to cite the Kovari fusion-specific review (47% for CO₂ recompression + Rankine bottoming in fusion design study) alongside the CSP figures, and note this as the authoritative upper bound from a fusion engineering context. Add one sentence noting that the Kovari review characterizes fusion energy conversion as an unsolved design problem field-wide — framing HESTIA's sCO₂ target as an instance of a cross-concept challenge, not merely a company-specific execution gap. In Section 3, add the Kovari citation to the sCO₂ TRL section's "Demonstrated" block as the reference source for the 47% efficiency ceiling.
- **Priority:** important
