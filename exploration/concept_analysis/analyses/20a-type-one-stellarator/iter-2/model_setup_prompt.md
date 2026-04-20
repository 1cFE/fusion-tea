# 1costingfe Model Update: QI Modular HTS Stellarator - Infinity Two

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Staged development program (Infinity One, 2029) absent from TRL assessment

- **Target:** Section 3 (3D HTS Modular Stellarator Coils — TRL 2–3) and Section 1 (Availability of Data)
- **Category:** analysis
- **Finding:** The Cambridge Core JPP article reveals that Type One Energy has a concrete subscale demonstration program — "Infinity One" — planned for 2029, with a TVA Cooperative Agreement signed January 20, 2025, and a deployment site at the retired Bull Run fossil plant in Tennessee. Infinity Two full deployment targets mid-2030s. The analysis rates 3D HTS coil winding at TRL 2–3 and identifies it as the top risk, which is correct, but presents no resolution path. In reality, Type One has a staged validation strategy: Infinity One is explicitly intended to resolve the computational modeling uncertainties the company acknowledges (including island divertor/core plasma confinement compatibility), and would provide the first demonstration of the HTS cable technology in stellarator geometry before committing to Infinity Two scale. The current analysis reads as if the TRL 2–3 risk has no planned mitigation, which misrepresents the company's roadmap.
- **Recommendation:** Add a paragraph at the end of Section 3's 3D HTS coils subsection describing the Infinity One subscale demonstration program: signed TVA agreement (January 2025), 2029 target, Bull Run site, and the company's stated intent that Infinity One resolves design margins and HTS-in-stellarator uncertainties before Infinity Two commitment. Cross-reference to Section 1 by noting that the JPP physics basis papers and TVA agreement together constitute a more advanced commercialization posture than most private fusion developers at equivalent TRL. Flag the Infinity One–to–Infinity Two timeline gap as a schedule risk parameter (2029 verification + construction time implies mid-2030s at earliest).
- **Priority:** important

---

### F-2: Li-6 enrichment risk framed as concentration issue; should be framed as near-zero Western supply

- **Target:** Section 4 (Lithium Orthosilicate / Metatitanate Pebbles — Li-6 enrichment paragraph)
- **Category:** analysis
- **Finding:** The analysis states Li-6 enrichment capacity "remains concentrated in Russia and China (legacy mercury amalgam processes; no Western industrial-scale alternative is yet operational)." The Pearson (2022) FES presentation specifies that COLEX — the mercury amalgam enrichment process used historically — is now banned under the Minamata Convention, eliminating the historical Western enrichment route entirely. Current Western commercial Li-6 supply is effectively zero. The primary alternative technology (ICOMAX) is at TRL 3–4 and Pearson characterizes it as potentially taking "decades to fully establish and scale." The analysis's framing ("concentrated in adversary nations") implies supply exists but is geopolitically exposed. The Pearson framing is more severe: there is no viable Western commercial Li-6 supply pathway on the timescale relevant to Infinity Two's HCPB blanket. This is a qualitative difference, not just a quantitative one — it affects the severity of the supply chain risk rating for the solid breeder pebbles. Pearson also identifies natural lithium blankets (no enrichment required) as a technically challenging but conceptually viable alternative design path, which the analysis does not mention.
- **Recommendation:** Update Section 4's Li-6 enrichment paragraph to: (a) specify that COLEX is banned under the Minamata Convention, not merely deprecated; (b) characterize ICOMAX as TRL 3–4 with a multi-decade scale-up horizon; (c) note that Western commercial Li-6 supply is currently near-zero, making this a supply creation problem rather than a diversification problem; (d) add one sentence noting natural lithium blankets as a design alternative that avoids enrichment entirely, with the tradeoff of requiring higher TBR margins. Upgrade the risk severity in the data gap inventory (Section 6, item 13) from "nice-to-have" to "important" to reflect that Li-6 enrichment availability is path-critical for HCPB deployment, not merely an efficiency parameter.
- **Priority:** important

---

### F-3: Tritium startup window risk not connected to Infinity Two deployment timeline

- **Target:** Section 4 (Tritium paragraph) and Section 6 (data gap inventory)
- **Category:** analysis
- **Finding:** Pearson (2022) establishes that global fusion tritium demand is expected to begin depleting the available stockpile from approximately 2035 onwards, with supply becoming "highly uncertain" beyond 2050 as the CANDU fleet reaches end of life. The Cambridge Core article establishes that Infinity Two targets mid-2030s deployment. These two facts together create a material timeline intersection: Infinity Two's first plasma and startup tritium procurement would coincide with the period when the global tritium stockpile first comes under sustained fusion demand pressure from multiple concurrent projects. The analysis covers tritium constraints (Section 4) and the startup inventory cost (~1 kg at >$35,000/g), but presents them as a fixed cost item, not a supply-timing risk. The analysis does not flag that the mid-2030s deployment target is precisely the window when tritium availability transitions from abundant to constrained.
- **Recommendation:** Add a sentence to Section 4's tritium paragraph noting the deployment timeline intersection: if Infinity Two achieves first plasma mid-2030s as planned, it would need to secure startup tritium inventory during the period when Pearson (2022) projects fusion demand pressure on the global stockpile to begin. Update Section 6's tritium gap (implicitly covered under Section 4 discussion) to add a specific note that the ~1 kg startup inventory cost estimate assumes current tritium pricing and availability — both of which may increase substantially if the mid-2030s stockpile drawdown scenario is realized. This converts the tritium startup item from a fixed parameter to a scenario-dependent risk that should be modeled as a range in Section 5.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Island divertor cost implication direction not stated
- **Target:** Section 2 (challenge #4) and Section 7 (differentiator list, item 4)
- **Category:** analysis
- **Finding:** The island divertor is correctly identified as a key differentiator from tokamak heat exhaust, but Section 7 states only "different cost structure from tokamak divertor" without naming the direction. The TEA checklist requires each differentiator to have a stated cost implication (advantage, penalty, or neutral with reasoning). No cost direction is given for island divertors anywhere in the analysis — the analysis notes there is no published cost estimate but stops there. This leaves the cost impact of a major plasma-facing subsystem uncharacterized for the model.
- **Recommendation:** Add a sentence in Section 2 (challenge #4) and Section 7 (item 4) stating the expected cost direction: island divertors likely represent a cost penalty relative to tokamak divertors for capital (complex 3D target geometry, no published unit cost, W7-X-scale manufacturing only reference) and for O&M (high steady-state heat flux on targets, 2-year continuous exposure before replacement access). Frame this explicitly as an upward pressure on CAS22 (divertor capital) and CAS70 (O&M), even though the magnitude is unknown. "Different cost structure" is not a TEA implication — a directional claim with reasoning is required.
- **Priority:** blocking

### F-2: Model LCOE presented without lower-bound caveat despite acknowledged coil cost underestimation
- **Target:** Model output and model_setup.py
- **Category:** model
- **Finding:** The model output acknowledges that C220103 (3D HTS coils, elasticity = 0.99) "likely underestimates significantly" relative to the W7-X LTS coil benchmark (€1B for magnets alone), yet presents a single LCOE figure (311 $/MWh, or 154 $/MWh at 1 GW scale) without framing it as a lower bound. The coil cost parameter has the highest LCOE elasticity in the entire sweep (+0.99), meaning a 2× error in coil cost produces nearly a 2× error in LCOE. Presenting a central-estimate LCOE when the highest-sensitivity input is acknowledged as likely underestimated is a misleading output framing.
- **Recommendation:** Add a coil cost scenario sweep to model_setup.py: run LCOE at 1× (framework default), 3×, and 5× the baseline coil cost, and output the resulting LCOE range alongside the base case. Present the model result as a range (e.g., "311–900 $/MWh depending on 3D HTS coil cost realization") rather than a single number. Alternatively, add an explicit note in the model output header stating: "LCOE IS A LOWER BOUND — coil cost (elasticity +0.99) uses a framework default acknowledged as likely too low." Either approach is acceptable; the current presentation of a single LCOE number without this qualification is not.
- **Priority:** blocking

### F-3: Top LCOE sensitivity parameters not named in Section 2
- **Target:** Section 2
- **Category:** analysis
- **Finding:** The analysis checklist requires Section 2 to identify the 2-3 parameters with highest LCOE sensitivity for this specific concept. Section 2 ranks challenges qualitatively (Critical / High / Moderate) by LCOE impact, which is good framing, but does not identify the specific model parameters with the highest leverage. The model sensitivity output shows the top three are coil cost proxy (r_coil, elasticity +0.99), availability (elasticity −0.93), and construction time (elasticity +0.55) — but this is only visible in the model output, not distilled into the analysis narrative. A reader of the analysis alone cannot determine which parameters to prioritize for sensitivity sweeps.
- **Recommendation:** Add a short paragraph at the end of Section 2 naming these three parameters and explaining the mechanism for each: (1) coil cost — the highest-leverage unknown, proxied by coil radius but representing the 3D HTS manufacturing cost premium; (2) availability — the 2-year cycle supports a ~96% theoretical maximum but actual unplanned outage exposure is unknown; (3) construction time — 3D HTS coil manufacturing complexity makes schedule risk the dominant financial cost driver. This bridges the qualitative challenge framing and the model's quantitative structure.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_stellarator.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20a-type-one-stellarator/iter-2/model_setup.py`
