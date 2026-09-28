Extension of the Fusion Power Plant Costing Standard 

power for MIFE), followed by successive refinements that add learning, manufacturing breakdowns, installation and integration fidelity, and explicit lifetime/replacement logic (26). In parallel, each driver thread will tighten the boundary and interface to Account 22.1.7 (Power Supplies) so that supporting electrical plant costs are represented consistently across architectures (e.g., wall-plug power implications for IFE, charging and pulse-forming infrastructure for MIFE, and conventional electrical support for MFE) and are not obscured inside single-factor driver scalings (26). Each monthly session includes a “model clinic” to ensure the code remains accessible through the open Colab/web workflow and to accelerate incorporation of community feedback via issues and pull requests (26). 

## 10.1.1 Planned implementation of AACE estimate accuracy ranges
To improve consistency and transparency in future CATF IWG cost products, we plan to align reported cost uncertainty with the _AACE International Cost Estimate Classification System_ . In this framework, the _accuracy range_ is the interval within which there is an 80% confidence that the actual cost will fall, often described as the project “cone of uncertainty” as definition matures from early screening to detailed design. 

Practically, this will be implemented as follows. First, each CATF estimate deliverable will be assigned an AACE estimate class based on the maturity of the underlying project definition (e.g., availability of design basis, equipment lists, quantities, vendor quotes, and schedule logic). Second, reported cost results will include an uncertainty band consistent with the corresponding AACE class (Table 3). Third, contingency and risk adjustments will be reported in a manner that is traceable to (i) estimate class, (ii) key drivers of uncertainty (technical, regulatory, supply-chain, schedule), and (iii) any probabilistic analysis used to support the 80% confidence interpretation. 

Table 3: AACE International cost estimate classification and typical accuracy ranges (80% confidence). 

|**Estimate Class**|**Maturity Level**|**Typical Purpose**|**Expected Accuracy Range (Low/High)**|
|---|---|---|---|
|Class 5|0% to 2%|Screening or Feasibility|_−_30%to_−_50% / +30%to+100%_∗_|
|Class 4|1% to 15%|Concept Screening|_−_15%to_−_30% / +20%to+50%|
|Class 3|10% to 40%|Budget Authorization|_−_10%to_−_20% / +10%to+30%|
|Class 2|30% to 75%|Control or Bid|_−_5%to_−_15% / +5%to+20%|
|Class 1|65% to 100%|Check Estimate|_−_3%to_−_10% / +3%to+15%|

> _∗_ Class 5 ranges are often highly asymmetric and can be wider depending on novelty, scope ambiguity, and data limitations. 

## 10.2 Safety-informed costing as a design-coupled cost driver
A priority extension is tighter integration of fusion safety analysis into the costing workflow, informed by the ongoing CATF IWG safety thread embedded across the monthly sessions. The methodological objective is to treat safety not as a post-hoc checklist but as a _design-coupled cost driver_ : confinement strategy, hazard controls (cryogens, high voltage, laser hazards), tritium inventory limits, waste classification approach, and operational constraints each impose tangible implications for facility layout, ventilation and detritiation capacity, shielding, remote maintenance provisions, commissioning scope, and staffing. In practice, the next-year plan is to formalize a small set of _safety basis input knobs_ that (i) add or modify specific COA accounts (buildings/structures, auxiliary systems, radioactive waste treatment, instrumentation and control, and owner’s costs), and (ii) propagate into indirect accounts through QA/QC requirements, testing/acceptance, licensing scope, and commissioning complexity (26). This will enable more consistent sensitivity studies of the cost consequences of safety posture choices across MFE/IFE/MIFE. 

## 10.3 Cost-basis library, governance, and supply-chain alignment to the COA
Several of the monthly sessions explicitly target “cost bases” as a first-class community product: a curated, versioned library of cost basis entries with metadata (source type, normalization to installed cost, reference year dollars, and uncertainty tags) and clear contribution templates (26). This work is directly aligned with the broader goal of accelerating deployment through _shared standards_ . If stakeholders converge on COA-based categorization, the supply chain can be described in a way that is immediately interpretable across developers and reviewers: vendors can map products and services into cost accounts; EPCs can bid, benchmark, and de-risk projects using a common accounting structure; and funding organizations can identify capability gaps (manufacturing capacity, qualifying test infrastructure, long-lead items, workforce needs) in an apples-to-apples way across concepts. A concrete near-term example is the ongoing effort to categorize fusion supply chains according to standardized cost accounts (including work by Fusion Advisory Services), which can translate “what is missing” from qualitative narratives into account-tagged procurement and scale-up priorities that are legible to both industry and capital providers. The IWG will use the monthly forum to refine 

