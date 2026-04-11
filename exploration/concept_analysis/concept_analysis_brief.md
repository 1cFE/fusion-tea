# First Pass Concept Analysis

# Goal

Perform an initial quantitative and qualitative LCOE analysis of each assigned fusion concept using publicly available information. This first pass is intentionally high-level but should include both a simple quantitative model (with code) and a qualitative write-up. The purpose is to develop a preliminary high-level understanding of each concept's cost structure, build an initial computational framework for LCOE estimation, and identify where the major uncertainties and data gaps lie.

Each team member (Tal, Mallory, Damien) will be assigned 3 concepts from the selected shortlist of 9.

# Deliverable 1: Qualitative Concept Write-Up

For each assigned concept, produce a narrative write-up (1-2 pages) covering the following:

**Availability of Data**

How much public literature exists for this concept? Are there peer-reviewed papers, published plant studies, or system code outputs? Is the company transparent about their approach, or is most information proprietary? Rate the data availability as: Rich, Moderate, Limited, or Opaque.

**Challenges in Capturing System Function**

What makes this concept hard to model from an LCOE perspective? Are there novel subsystems with no cost analogues? Are there physics uncertainties that propagate into large cost uncertainties? Are the claimed performance parameters validated or extrapolated?

**Maturity of Key Subsystems and Components**

For each major subsystem, assess the technology readiness. Are there components that exist only on paper? What has been demonstrated at laboratory or prototype scale? What materials or manufacturing processes are required that do not yet exist at the needed scale?

**Key Materials and Supply Chain Considerations**

Are there critical materials with limited supply (tritium, He-3, enriched Li-6, REBCO tape, beryllium)? Are there manufacturing bottlenecks (e.g., cryogenic target fabrication, nanostructured targets, large HTS magnets)?

# Deliverable 2: Quantitative LCOE Model (Simple)

For each assigned concept, build a simple first-pass LCOE model in code (Python, JAX, or other suitable language/framework) using publicly available information. This can be extremely high level. The model should be parameterized so that key assumptions can be varied and sensitivities explored. It should cover the following areas at whatever depth the available data supports:

**Capital Cost Drivers**

Identify the major capital cost components for the concept. What are the dominant cost items (magnets, laser systems, vacuum vessel, blanket, balance of plant, etc.)? Where do published estimates or analogues exist? Flag where no data is available. Assign rough order-of-magnitude cost estimates or ranges where possible.

**Operating Cost Drivers**

What are the expected major operating costs? Consider fuel costs, component replacement rates (first wall lifetime, target fabrication for ICF), staffing, tritium handling (if D-T), and maintenance complexity (remote vs. contact).

**Energy Conversion Pathway**

How does the concept convert fusion energy to electricity? Thermal cycle (steam, sCO2), direct energy conversion, or hybrid? What is the expected or claimed thermal/electrical efficiency? What does the balance of plant look like?

**Capacity Factor and Availability**

Is the concept continuous or pulsed? If pulsed, what rep rate is needed for baseload? What are the expected maintenance intervals and component replacement schedules? Are there inherent availability limitations?

**Scaling Assumptions**

What fusion power or gain (Q) is assumed or claimed? What is the target plant electrical output? Are there published power plant studies or system codes for this concept?

The code should output an LCOE estimate (in c/kWh) with clearly stated assumptions and the ability to run parameter sweeps on the most uncertain inputs.

**Back-Solve to $0.01/kWh**

Using the model, perform a first high-level pass on what would need to be true for this concept to achieve an LCOE of $0.01/kWh (1 c/kWh). Which parameters need to hit what values? Are those values physically plausible, or do they require breakthroughs beyond current understanding? Identify the binding constraints and the parameters with the most leverage. This does not need to be exhaustive but should give a clear picture of the gap between the concept's baseline LCOE estimate and the 1 c/kWh target, and what combination of improvements could close it. Even where data is sparse, use best-guess analogues and document the basis.
