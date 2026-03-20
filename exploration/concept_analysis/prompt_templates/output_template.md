# D1+ Analysis Output Template

This template defines the required section structure for automated concept analyses. Every analysis must include all sections below. Sections may be brief for thin-data concepts, but must not be omitted.

---

## Required YAML Frontmatter

```yaml
---
ID: {concept-id}
Concept: {concept-name}
Company: {company}
Status: draft
Created: {date}
Approved-Date:
Reuses:
  - {list of concept IDs referenced from approved prior analyses, if any}
---
```

---

## Required Sections

### Section 1: Availability of Data

**Rating: [Rich / Moderate / Limited / Opaque]**

Assess the breadth and depth of publicly available information for this concept. Cover:
- Peer-reviewed publications, plant studies, system code outputs
- Company transparency (published designs, whitepapers, technical blogs)
- Independent analyses or third-party assessments
- Completeness of Phase 1a dossier coverage

Cite specific sources for each claim. End with a summary of key data gaps that limit the analysis.

### Section 2: Challenges in Capturing System Function

Identify and rank the major challenges for LCOE modeling of this concept. For each challenge:
- Explain what makes it difficult to model
- Quantify the uncertainty range where possible
- Note whether the challenge is shared with other concepts or unique

Typical challenge categories (include those that apply, skip those that don't):
- Dominant LCOE cost drivers and their uncertainty
- Novel subsystems with no cost analogues
- Physics uncertainties that propagate into cost uncertainty
- Scaling extrapolations from current experiments to plant scale
- Regulatory or licensing unknowns

### Section 3: Maturity of Key Subsystems and Components

For each major subsystem, provide a TRL assessment in **ascending order of maturity** (least mature first). For each subsystem:

**{Subsystem Name} — TRL {N}[-{M}]**
- **Demonstrated**: What has been built, tested, or operated at what scale
- **On paper only**: What exists only in design studies or simulations
- **Missing at scale**: What must be developed for a commercial plant

Cover at minimum: the core confinement/driver system, plasma-facing components, breeding blanket, tritium fuel cycle, energy conversion / balance of plant, and any concept-specific subsystems (e.g., target fabrication for IFE, pulsed power driver for MIF).

### Section 4: Key Materials and Supply Chain Considerations

For each critical material or supply chain constraint:
- Current production capacity vs. plant-scale demand
- Cost trajectory and scaling potential
- Sole-source or limited-supplier risks
- Shared supply chains with other fusion concepts or industries

Common materials to assess (include those relevant): tritium, HTS tape (REBCO), FLiBe/blanket materials, lithium-6 enrichment, beryllium, tungsten, specialized alloys, laser components, capacitors/switches, target materials.

### Section 5: LCOE-Relevant Parameters

Extract all quantitative parameters relevant to LCOE modeling. Present as a structured table:

**Available Parameters:**
| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output | ... | ... | high/medium/low | ... |
| Fusion power / gain | ... | ... | ... | ... |
| Thermal efficiency | ... | ... | ... | ... |
| Recirculating power | ... | ... | ... | ... |
| Capacity factor | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

Include parameters across these categories where data exists:
- **Performance**: Q, fusion power, net electric, thermal efficiency
- **Capital cost**: Total plant cost, major subsystem costs, $/kWe
- **Operating cost**: Fuel, consumables, maintenance, replacement schedules
- **Availability**: Capacity factor, maintenance intervals, component lifetimes
- **Scaling basis**: Plant studies, system code outputs, design point references

Every value MUST cite a specific source. Values without a source must be flagged:
- `[inferred]` — derived from available data with stated reasoning
- `[analogue]` — borrowed from a similar concept with stated basis
- `[estimated]` — rough order of magnitude with stated assumptions

**Missing Parameters:**
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| ... | truly-unknown / proprietary / not-yet-sourced / derivable | blocking / important / nice-to-have | ... |

### Section 6: Data Gap Inventory

Consolidate all gaps identified across Sections 1-5 into a single structured inventory:

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | ... | S1/S2/S3/S4/S5 | truly-unknown / proprietary / not-yet-sourced / derivable | blocking / important / nice-to-have | ... |

Gap types:
- `truly-unknown` — no one has published this data
- `proprietary` — company likely has this but hasn't published
- `not-yet-sourced` — published data likely exists but wasn't captured
- `derivable` — can be estimated from available data with stated assumptions

### Section 7: Cross-Concept Notes

If approved prior analyses were available:
- What assumptions, models, or data were reused from which prior concept
- What diverges from prior analyses and why
- Shared subsystems, materials, or cost structures across concept families

If no approved priors were available, state: "No approved prior analyses available for cross-referencing."

### Section 8: Sources

List all sources cited in the analysis, in order of importance. For each:
- Full citation (author, title, year, publication)
- What it contributes to the analysis
- Where it was found (Phase 1a source path, URL, or database)
