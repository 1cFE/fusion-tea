VERDICT: FINDINGS

---

**Source assessed**: `arxiv-2501-04640.md` (Queral et al., January 2025, arXiv:2501.04640)
**Title**: "Coil geometry with large openings for a HSR3-like stellarator reactor for fast replacement of in-vessel components"
**Extraction note**: Only the arXiv abstract page was captured (trafilatura backend, 4 KB). The full paper content — engineering analysis, coil geometry specifications, quantitative results, and proposed solutions — was not extracted. Findings below are based solely on the abstract text.

---

### F-1: Missing blanket/divertor replacement interval as a capacity factor anchor
- **Target:** Section 5 (LCOE-Relevant Parameters, Capacity Factor row) and Section 6 (Data Gap Inventory, Gap #7)
- **Category:** analysis
- **Finding:** The abstract states as general stellarator reactor context that "blankets and divertor modules will have to be replaced periodically (about each 1-4 years depending on the design) due to neutron damage, and also erosion of divertor targets." The analysis uses an 85-95% capacity factor range (Sections 5 and 7) grounded in the Helios 88% design target and W7-X operational availability, but has no concrete maintenance interval anchor for the lower bound. The 1-4 year replacement interval is the physical parameter that sets the scheduled downtime floor: at a 4-week outage per replacement and a 1-year interval, availability ceiling is ~92%; at a 4-week outage per 4-year interval, ceiling is ~98%. Without this interval, the capacity factor range is not causally grounded in maintenance physics, and Gap #7 (O&M cost breakdown) cannot be informed even approximately.
- **Recommendation:** Add a row to the Section 5 Available Parameters table: "Blanket/divertor replacement interval | 1–4 years | arxiv-2501-04640.md (abstract; HSR3 context) | low | General stellarator reactor constraint; not Stellaris-specific; applicable as calibration for availability lower bound." Add a brief note in the Section 5 Capacity Factor row that the 85-95% range's lower bound is constrained by this replacement interval, and that the specific downtime per replacement event is a critical missing input for gap #7 (O&M cost). Do not change the range itself — the low-confidence analogue status of the source does not justify narrowing the range, only grounding the narrative.
- **Priority:** important

---

### F-2: Port-size disadvantage vs. tokamaks not explicit in cross-concept comparison
- **Target:** Section 7 (Cross-Concept Notes, CAS-Level Cost Delta table)
- **Category:** analysis
- **Finding:** The abstract states directly: "these requirements imply relatively small ports for in-vessel access and maintenance, i.e. in comparison with tokamaks." This is a clean, citable cross-concept comparison statement that applies to all advanced stellarators with convoluted modular coils. The analysis covers remote maintenance difficulty and constrained divertor geometry (Section 2 Challenge 5, Section 3 Island Divertor TRL, Section 6 Gap #11) but frames these as Stellaris-specific challenges. The Section 7 CAS delta table has no O&M row — O&M is listed as "truly-unknown" in Gap #7 but not discussed in the cross-concept comparison at all. The port-size structural disadvantage is a directional argument that Stellaris O&M cost is higher than an HTS compact tokamak reference, independently of island divertor physics, because access geometry for any modular stellarator coil set is tighter than for a tokamak. This belongs in Section 7 as a cross-concept O&M delta.
- **Recommendation:** Add a brief paragraph under the Section 7 CAS-Level Cost Delta table (or as a new row) noting that stellarator coil geometry structurally limits blanket and divertor module size relative to tokamaks — not because of Stellaris-specific design choices, but as a generic consequence of the convoluted modular coil architecture. State the directional implication: "+" (stellarator O&M cost higher) at unknown magnitude. Cite the abstract as basis. This completes the cross-concept O&M delta that is currently absent from the table and grounds the blanket/divertor replacement discussion in a causally clear cross-concept framing (Goal 2: Key Differentiators → Goal 3: TEA Implications).
- **Priority:** minor
