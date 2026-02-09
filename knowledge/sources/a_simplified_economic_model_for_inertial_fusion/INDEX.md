---
document: Hawker___2020___A_simplified_economic_model_for_inertial_fusion
generated: 2026-02-09T19:18:48Z
source_checksum: sha256:fabac3cfe8b198b9c9f228ecff46f87f770fe84aaf80823966af7ea8bfda1c7a
total_lines: 918
depth: 3
section_count: 11
---

# Hawker___2020___A_simplified_economic_model_for_inertial_fusion Index

## 1 Abstract
**Lines:** 55-118

A 14-parameter, technology-agnostic LCOE model for inertial fusion power plants, explored via Monte Carlo sampling, finding that high target gain (>500) combined with high fusion energy yield per shot (>5 GJ) enables designs with LCOE as low as $25/MWh. The introduction contextualizes fusion cost competitiveness against other generation technologies (solar, wind, coal, gas, nuclear) and argues that gain requirements must be evaluated economically, not just physically.

## 2 The cost of electricity
**Lines:** 119-166

LCOE definition and competitive price targets for fusion energy, based on projected costs of generation technologies in the 2030s. Argues fusion must reach ~$100/MWh initially (competing with nuclear) with a pathway to $60/MWh (displacing gas), accounting for the "clean power gap" that renewables alone cannot fill in net-zero scenarios.

## 3 Previous studies
**Lines:** 167-184

Previous conceptual design studies of inertial fusion power plants examined singular design points across three driver types (lasers, heavy ion beams, pulsed power), with laser studies trending toward lower energy/higher frequency drivers and pulsed power studies constrained to lower frequencies. The present work aims to complement these by providing a tool that clarifies the cost impact of design choices like operating frequency.

## 4 Model
**Lines:** 185-492

LCOE (Levelized Cost of Electricity) is defined as the ratio of discounted lifetime costs to discounted lifetime energy, representing the break-even electricity price. The model decomposes costs into plant capital cost (scaled by $/kWe), yield cost (reaction vessel, scaled by fusion energy per shot), driver cost (with lifetime/replacement), target cost (per-shot consumables), and O&M — governed by 14 independent parameters including availability, gain, driver energy/efficiency/lifetime, thermal efficiency, blanket energy multiple, and shot frequency. Electrical power is derived from thermal power (fusion power × blanket multiple × thermal efficiency) minus recirculating power, with fusion power set by target gain × driver efficiency × driver energy × frequency. Two gain curve models are included: the isobaric hot-spot limiting gain curve and a hydrodynamic-equivalence-based scaling with burn fraction.

## 5 Results and discussion
**Lines:** 493-501 | **Subsections:** 5.1, 5.2, 5.3, 5.4

Monte Carlo sampling (10M samples) over 14 parameters identifies discount rate, plant cost, and target cost as the strongest LCOE correlators via Pearson analysis, while detailed parameter sweeps reveal nonlinear thresholds (target cost <$10/target, gain >~400) and a complex frequency-yield interaction where higher fusion energy per shot lowers both optimal frequency and LCOE, potentially enabling cost-competitive designs as small as ~150 MWe.

### 5.1 Correlation analysis
**Lines:** 502-606

Pearson correlation analysis ranks input parameters by their influence on inertial fusion LCOE: discount rate (+0.247), plant cost (+0.210), and target cost (+0.186) are the strongest drivers, while gain, driver lifetime, and availability form a middle tier; driver cost, efficiency, O&M, yield cost, and target energy have weak correlations. An economy-of-scale effect is also observed, with larger plant electrical power correlating with lower LCOE (−0.233), partly explained by recirculating power fraction.

### 5.2 Dependence on individual parameters
**Lines:** 607-688

Explores how LCOE depends on individual parameters (target cost, yield cost, driver lifetime, gain, frequency, plant size) in an inertial fusion economic model, identifying nonlinear thresholds (e.g., ~$10/target, gain >400, driver lifetime ~5 years) beyond which further improvement yields diminishing returns, and showing that higher fusion yield per shot enables lower optimal frequencies and smaller viable plant sizes.

### 5.3 Addition of gain curves
**Lines:** 689-736

Covers the addition of two gain curves to the economic model: (1) a limiting gain curve for spherical isobaric hot-spot fuel (parameterized by coupling efficiency μc and isentrope parameter A), and (2) a more restrictive gain curve (max ~250 gain) parameterized by fuel mass density ρ, internal energy e, implosion velocity V, and coupling efficiency μc — with Monte Carlo sampling showing the second curve removes the lowest-cost designs requiring gains above ~400.

### 5.4 Minimum cost design point
**Lines:** 737-809

Explores minimum-cost IFE design points via parameter scanning, identifying configurations with LCOE as low as $24.6/MWh and detailing the specific parameters (availability, driver lifetime, thermal efficiency, target energy, gain of 1000, etc.) that produce them, while cautioning that such optimistic results require much more detailed validation—particularly around achievable gain, driver costs at low energy/high efficiency, and plant cost scaling for smaller electrical output.

## 6 Conclusion
**Lines:** 810-857

Summarizes key findings of the simplified IFE LCOE model: no single parameter dominates cost (discount rate, plant cost, and target cost matter most); a gain threshold around 400 yields diminishing returns; higher energy-per-shot with lower repetition rate unlocks fundamentally lower LCOE and reduces engineering challenges, with a competitive ~150 MWe design point identified. Notes the model is extensible and supports cross-approach comparison.

## 7 Acknowledgements and References
**Lines:** 858-918

Acknowledgements (reviewers, competing interests, funding statement) and a bibliography of 19 references covering inertial fusion physics, LCOE and renewable energy cost analyses, IFE power plant designs (HYLIFE, OSIRIS/SOMBRERO, Z-IFE, LIFE, HiPER), and capital cost/discount rate methodologies.
