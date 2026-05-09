---
date: 2026-05-01T18:00:00-04:00
researcher: Claude
topic: "Down-selection methodology: data-availability thresholds and learning-rate predictors"
tags: [research, down-selection, data-availability, learning-rates, TEA-methodology]
status: complete
last_updated: 2026-05-01
---

# Research: Down-Selection Methodology (Q4--Q5)

**Date**: 2026-05-01
**Researcher**: Claude (3 parallel agents: local knowledge scan + 2 web research)
**Research Type**: Domain / Literature Review
**Scope**: Questions 4--5 from `concept.md`; builds on Q1--Q3 in `research_q1_q3.md`

---

## Research Questions Addressed

4. **Data-availability thresholds.** How have prior comparative TEA studies (fusion, advanced fission, broader energy) handled the "concept is too thinly documented to model" problem? Strict thresholds, sliding penalties, or assessed in combination with technical merit?

5. **Learning-rate predictors.** Which concept-level features (modularization, factory-buildability, supply-chain depth, commodity-vs-specialty materials, plant footprint, regulatory class, unit replication path) have measurable historical association with realized learning rates in capital-intensive generation?

---

## Q4: Data-Availability Thresholds in Comparative TEA Studies

### Summary

No study found uses a hard binary threshold ("exclude if data below X"). The field employs a spectrum of three paradigms, evolving from exclusion toward continuous uncertainty widening:

1. **Hard exclusion** -- binary include/exclude based on data availability (Lazard, IRENA implicitly, OECD/NEA "sufficient data")
2. **Tiered comparison** -- group by maturity class, compare within tiers, label cross-tier comparisons (PPCS, IEA ETP, AACE, ARIES)
3. **Continuous uncertainty widening** -- data sparsity maps to wider probability distributions via TRL/maturity factors (CATF/Woodruff probabilistic costing, NASA TRL cost growth models, fuzzy MCDA)

The most methodologically sophisticated fusion-specific approach is the CATF/Woodruff probabilistic costing framework, which compounds TRL-based uncertainty as a multiplicative log-normal factor -- a sliding penalty that widens confidence bands without excluding concepts.

### Fusion TEA Studies

#### ARIES Program (1990s--2010s)

The ARIES program avoided cross-concept comparison entirely. Each study (ARIES-I, -II, -IV, -RS, -ST, -AT, -CS, -ACT) modeled a single tokamak or stellarator variant in depth. Cost-scaling relations from fission experience (Generomak/Sheffield models) were applied uniformly. When subsystem data was missing, analogy to fission or industrial experience was used, documented but not penalized quantitatively. All estimates were effectively AACE Class 5 (0--2% project definition, -50% to +100% accuracy range) though this classification was not stated explicitly.

- Najmabadi, F. et al. (2006). "The ARIES-AT advanced tokamak." *Fusion Engineering and Design* 80:3--23. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0920379605007210)

#### European PPCS (2001--2005)

The Power Plant Conceptual Study used **explicit maturity tiering**. Five models (A, B, AB, C, D) were arranged on a maturity spectrum: Models A--B used near-term ITER-extrapolated technology; Models C--D required significant breakthroughs (SiC/SiC blankets, He-cooled divertors). The PROCESS systems code used the same methodology across all models, but advanced models required more assumed parameters. This was handled through narrative qualification rather than quantitative penalty -- no formal data-quality gates, no probabilistic uncertainty bands.

- Maisonnier, D. et al. (2005). "The European power plant conceptual study." *Fusion Engineering and Design* 75--79:1173--1179. [PPPL PDF (full text)](https://fire.pppl.gov/eu_ppcs_full_2005.pdf)

#### Woodruff Scientific / ARPA-E Costing Framework (2017--2024)

The most directly relevant example for our down-selection. The 2017 study applied a single costing framework to four radically different ARPA-E ALPHA concepts (Stabilized Liner Compressor, Plasma Jet MIF, Staged Z-Pinch, Flow-Stabilized Z-Pinch) -- concepts with very limited data. Three key methodological choices:

1. **Common plant architecture**: Force all concepts into a standardized ~150 MWe layout with common balance-of-plant; vary only the fusion power core.
2. **Cost-scaling from analogy**: Apply ARIES-style cost-scaling relations uniformly, calibrated via a Bechtel/Decysive Systems benchmarking study.
3. **Metric-specific threshold**: The team *deliberately refused* to compute LCOE because "the juxtaposition of the conceptual nature of the fusion core designs versus the level of granular knowledge commonly used as input for calculating an LCOE" made it inappropriate. Output was restricted to overnight capital cost comparisons -- an implicit data-quality gate that limits the *metric* rather than excluding concepts.

By 2023--2024, the framework evolved to include bottom-up subsystem models replacing legacy ARIES scalings for novel architectures.

- Woodruff, S. et al. (2026). "A costing framework for fusion power plants." arXiv:2601.21724. [arXiv](https://arxiv.org/html/2601.21724)
- Woodruff Scientific (2021). "Revisit of the 2017 Costing for Four ARPA-E ALPHA Fusion Concepts." OSTI 1820946. [OSTI](https://www.osti.gov/servlets/purl/1820946)

#### CATF/IWG Probabilistic Costing Extension (2024--2025)

The **state-of-the-art** approach. The CATF International Working Group developed a probabilistic costing layer that explicitly handles maturity differences through three compounding multiplicative uncertainty factors:

**C = C₀ × U_mat × U_TRL × U_LR**

Where:
- **C₀** = baseline deterministic cost element from standardized accounts
- **U_mat** = materials price/specification uncertainty (log-normal, from historical price series or expert-specified)
- **U_TRL** = technology maturity dispersion: U_TRL ~ LogNormal(μ(TRL), σ(TRL)), where σ decreases monotonically from low to high TRL
- **U_LR** = learning-rate uncertainty from bootstrapped regression

**Key design principle**: "TRL controls uncertainty bounds but does not alter the deterministic central estimate used for like-for-like reporting." Data-sparse concepts get the *same* point estimate but *wider* confidence bands. Monte Carlo sampling across all three factors produces empirical cost distributions. P10/P50/P90 percentile reporting communicates confidence.

No binary exclusion gates. The implicit threshold is whether a subsystem cost basis can be stated at all ($/kg, $/J, $/W) -- if it can, it enters the model with appropriate uncertainty.

- Woodruff, S. et al. (2026). "Extension of the fusion power plant costing standard." arXiv:2602.19389. [arXiv](https://arxiv.org/html/2602.19389)

#### Bustreo et al. -- FRESCO Monte Carlo (2015)

Applied Monte Carlo simulation with wide parameter distributions to a DEMO-class tokamak. Found the COE can range from ~0.67× to ~4× the deterministic estimate when uncertainties are properly propagated -- demonstrating that deterministic point comparisons across concepts at different maturities are misleading.

- Bustreo, C. et al. (2015). "The Monte Carlo approach to the economics of a DEMO-like power plant." *Fusion Engineering and Design* 98--99:2108. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0920379615000976)

#### Foster et al. -- Cost Extrapolation (2024)

Explicitly acknowledged: "estimating the costs of prototype or demonstration fusion power plants is difficult due to the often still preliminary designs. This difficulty is compounded by nonexisting supply chains for many bespoke technologies or materials." Their prescription: "these cost models are more relevant for differential cost assessments than absolute cost assessments" -- use for relative ranking, not absolute LCOE claims.

- Foster, J. et al. (2024). "Extrapolating Costs to Commercial Fusion Power Plants." *IEEE Transactions on Plasma Science*. Local: `knowledge/meta_analysis/Extrapolating_Costs_to_Commercial_Fusion_Power_Plants__1_/output.md`

### Advanced Fission TEA Comparisons

#### GEN IV EMWG Cost Estimating Guidelines

The canonical nuclear approach. All GEN IV concepts (SFR, GFR, LFR, MSR, VHTR, SCWR) use the same Uniform Code of Accounts. For immature concepts, cost-scaling equations substitute for bottom-up estimation. No exclusion threshold -- estimate what you can, document the basis, let users assess credibility.

- GIF/EMWG/2007/004 (2007). "Cost Estimating Guidelines for Generation IV Nuclear Energy Systems." Rev. 4.2. [GIF PDF](https://www.gen-4.org/gif/upload/docs/application/pdf/2013-09/emwg_guidelines.pdf)

#### INL Meta-Analysis of Advanced Reactor Cost Estimations (2024)

Introduced the concept of **"BOAK" (Between-A-First-and-Nth-Of-A-Kind)** to handle the fact that most advanced reactor data is neither purely FOAK nor NOAK. Uses **range reporting** rather than point estimates -- wider ranges for less mature concepts. BOAK ranges "assumed applicable from 2030 onward" -- a temporal threshold for when estimates become meaningful.

- INL/RPT-24-77048 (2024). "Meta-Analysis of Advanced Nuclear Reactor Cost Estimations." Rev. 2. [INL PDF](https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_107010.pdf) | [GAIN PDF](https://gain.inl.gov/content/uploads/4/2024/11/INL-RPT-24-77048-Meta-Analysis-of-Adv-Nuclear-Reactor-Cost-Estimations.pdf)

### Broader Energy Comparison Methodologies

#### AACE 18R-97 Cost Estimate Classification

The de facto standard for communicating estimate quality across industries. Maps project definition level to accuracy range:

| Class | Project Definition | Accuracy Range | End Use |
|---|---|---|---|
| 5 | 0--2% | -50% to +100% | Concept screening |
| 4 | 1--15% | -30% to +50% | Feasibility |
| 3 | 10--40% | -20% to +30% | Budget authorization |
| 2 | 30--75% | -15% to +20% | Contractor bid |
| 1 | 65--100% | -10% to +15% | Check estimates |

Key principle: "The maturity level of definition is the sole determining characteristic of class." The AACE framework does not say "don't estimate at Class 5" -- it says Class 5 estimates have -50% to +100% accuracy and should only be used for concept screening, not budget decisions. This is a continuous classification with labeled uncertainty bands, not a binary gate. Nearly all fusion cost estimates are Class 5.

- AACE International (2020). "18R-97: Cost Estimate Classification System." [Summary](https://epcland.com/cost-estimate-classification-system-for-process-industries/)

#### Lazard LCOE Analysis -- Hard Exclusion

The closest to a hard binary threshold. Lazard's annual LCOE+ report excludes technologies without "sufficient observable market data" -- advanced nuclear, CCS, and long-duration storage are either excluded or frozen at prior estimates. Lazard itself has warned its LCOE tool "has been widely misused to compare apples and oranges" across maturity levels.

- Lazard (2024). "Levelized Cost of Energy+ (LCOE+)." Version 17.0. [Lazard PDF](https://www.lazard.com/media/xemfey0k/lazards-lcoeplus-june-2024-_vf.pdf)

#### IEA ETP -- Tiered by TRL

Uses an extended TRL 1--11 scale grouped into four readiness categories (Mature / Early adoption / Demonstration / Large prototype). Does not exclude lower-TRL technologies but reports them in separate maturity categories with wider cost bands and qualitative caveats. Tracks ~600 technology designs.

- IEA. "ETP Clean Energy Technology Guide." [IEA](https://www.iea.org/data-and-statistics/data-tools/etp-clean-energy-technology-guide)

#### IRENA -- Data-Driven Exclusion

Database of ~20,000 utility-scale projects and ~13,000 PPA/auction results. Methodology relies on observed market data -- if no projects exist, no costs are reported. Learning rates from literature are substituted for technologies with limited market history, with the substitution noted.

- IRENA (2025). "Renewable Power Generation Costs in 2024." [IRENA](https://www.irena.org/Energy-Transition/Technology/Power-generation-costs)

### TRL-Cost Interaction Frameworks

#### NASA/DoD TRL-Based Cost Growth Models

The strongest empirical calibration of how TRL maps to cost uncertainty (though calibrated on aerospace, not energy). Key findings from 68 NASA programs:

- Average total cost growth: **46%** over baseline estimates at Milestone B
- Programs at **TRL 6 and TRL 8** showed highest relative cost growth (the "valley of death" transition)
- Probability distributions calibrated per TRL level using Johnson's four-parameter family

These provide a quantitative, continuous penalty function mapping TRL to expected cost growth.

- Hicks, B. et al. (2009). "Cost Growth Models for NASA's Programs." AIAA. [ResearchGate](https://www.researchgate.net/publication/255573429_Cost_Growth_Models_for_NASA'S_Programs_A_Summary)
- Dubos, G. & Saleh, J. (2012). "An Analysis of TRL-Based Cost and Schedule Models." [ResearchGate](https://www.researchgate.net/publication/255908640_An_Analysis_of_TRL-Based_Cost_and_Schedule_Models)

#### RAND Cost Estimation for New Technologies (1981)

Early foundational work showing degree of system definition and level of technological innovation are the dominant drivers of cost growth in pioneer energy plants. Novel technology plants systematically underestimate costs.

- Merrow, E.W. et al. (1981). "A Review of Cost Estimation in New Technologies." RAND R-2481-DOE. [RAND](https://www.rand.org/pubs/reports/R2481.html)

#### Reference Class Forecasting

Addresses "too thinly documented to model" by substituting the "inside view" (bottom-up estimation) with an "outside view" (statistical distribution from comparable past projects). For UK infrastructure, RCF reduced average cost overruns from 38% to 5%. For fusion/novel energy, the challenge is that no adequate reference class exists; recent work proposes clustering-based approaches using unsupervised ML to construct reference classes from risk factor similarity.

- Flyvbjerg, B. (2025). "Reference class forecasting: promises, problems, and a research agenda." *Production Planning & Control*. [Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/09537287.2025.2578708)
- "An approach to support reference class forecasting when adequate project data are unavailable." *Results in Engineering* (2024). [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2590123024005887)

### MCDA and Data Gaps

The dominant approach in energy multi-criteria decision analysis is **not** to exclude data-sparse options but to widen uncertainty on their scores and use stochastic dominance or outranking methods robust to imprecision. Bayesian networks can infer missing evaluations from causal relationships between criteria. Modified ELECTRE III and SMAA-PROMETHEE handle imprecise weights and non-deterministic performance scores.

- Wang, S.-H. et al. (2025). "A multi-criterion decision making method for renewable energy storage technology selection with incomplete evaluation information." *TFSC*. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0040162525001477)
- DOE/Linkov (2016). "MCDA to PandRA." [DOE webinar PDF](https://www.energy.gov/sites/prod/files/2016/03/f30/2016.02.23%20-%20Linkov%20and%20Bates%20webinar%20to%20MCDA%20to%20PandRA%20CoP.pdf)

### Synthesis: Three Paradigms

| Paradigm | Mechanism | Who Uses It | Limitation |
|---|---|---|---|
| **Hard exclusion** | Binary include/exclude | Lazard, IRENA (implicitly), OECD/NEA | Eliminates potentially interesting options; threshold is subjective |
| **Tiered comparison** | Group by maturity; compare within tiers | PPCS, IEA ETP, AACE classes, ARIES | Tier boundaries are subjective; cross-tier comparisons remain qualitative |
| **Continuous uncertainty widening** | Data sparsity → wider distributions | CATF/Woodruff, FRESCO, NASA TRL models, fuzzy MCDA | Requires functional form choice; no calibration exists for fusion specifically |

**The field is evolving from Paradigm 1 toward Paradigm 3.** The CATF/Woodruff C = C₀ × U_mat × U_TRL × U_LR framework is the most complete fusion implementation. The NASA cost growth models provide the strongest empirical calibration of TRL-to-uncertainty mapping (though calibrated on aerospace).

### Implications for Our Down-Selection

The literature strongly supports a **combined assessment** (data availability evaluated alongside technical merit) rather than a strict exclusion threshold:

1. **Use concept data-availability ratings as a continuous score**, not a gate. Our §1 data-availability ratings and §6 data-gap inventories map naturally to a CATF-style uncertainty-widening approach.
2. **Metric-specific thresholds** are more defensible than concept-exclusion thresholds. Following Woodruff 2017: we can compare capital cost structures across all concepts, but restrict LCOE claims to concepts with sufficient parameter confidence.
3. **AACE Class 5 framing**: All our estimates are concept-screening level. Cross-concept comparison is the appropriate use of Class 5 estimates -- budget authorization or cost-competitiveness claims are not.
4. **Data availability feeds into Phase 2(c) learning-curve plausibility**, not as an independent gate: a concept with thin data but plausible learning-curve features may be *more* worth diving into (to resolve uncertainty) than a well-documented concept with limited upside.

---

## Q5: Learning-Rate Predictors

### Summary

Six bodies of work provide quantitative evidence on what predicts learning rates. The strongest single predictor is **unit size/granularity** (R² ≈ 0.33), but the **two-dimensional typology** of design complexity × need for customization (Malhotra & Schmidt 2020, applied to fusion by Tang & Schmidt 2025) provides the most actionable framework. Key finding: fusion power plants are firmly "Type 3" (complex, customized), predicting ~5% experience rates -- far below the 8--20% assumed in most fusion TEA literature.

No study runs a full multivariate regression with granularity, complexity, customization, regulatory class, and supply chain depth as simultaneous predictors. This is the key gap in the literature.

### Feature-by-Feature Evidence

#### 1. Unit Size / Granularity

**Evidence strength: Strong (R² = 0.33, p < 0.001)**

Wilson et al. (2020) measured granularity as unit cost or unit size (MW/unit) and correlated it against learning rates across energy technologies:

| Relationship | R² | Significance |
|---|---|---|
| Conventional learning rate vs. unit cost | 0.33 | p < 0.001 |
| De-scaled "true" learning rate vs. unit cost | 0.33 | p < 0.05 |
| Component count (complexity) vs. unit cost | 0.77 | p < 0.001 |

The "de-scaled" learning rate strips out unit scale economies (building bigger) and measures pure experience effects (building more units). The correlation persists -- smaller units genuinely learn faster from replication, not just from scale.

**Mechanism**: "More-granular technologies offer more opportunities for repetitive, replicative experience to drive faster improvement." Manufacturing plant scale-up (order-of-magnitude increases in production output per facility) explained >1/3 of solar PV cost reductions 2001--2012 (Kavlak et al. 2018). Conversely, up-scaling of plant sizes explained ~3/4 of US coal power cost reductions 1908--1970.

**Fusion discrimination**: MFE minimum capacity ~530 MW, LFE ~230 MW (Tang & Schmidt expert estimates). Both sit at the extreme "lumpy" end of Wilson et al.'s continuum. However, R² of 0.33 means two-thirds of variance is NOT explained by unit size alone.

- Wilson, C. et al. (2020). "Granular technologies to accelerate decarbonization." *Science* 368(6486): 36--39. [DOI](https://doi.org/10.1126/science.aaz8060). Local: `knowledge/meta_analysis/Granularity_Manuscript_preprint/output.md`

#### 2. Design Complexity

**Evidence strength: Strong (theoretical + empirical typology validation)**

Malhotra & Schmidt (2020) develop a typology with design complexity as one of two dimensions. Five approaches exist to quantify it: Design Structure Matrices, N/K models on patent data, economic complexity indices, network analysis of patent topologies, and expert elicitation.

**Quantitative association with learning rates (from Figure 2, global experience rates by type):**

| Type | Complexity | Examples | Median Global ER |
|---|---|---|---|
| Type 1 (simple, standardized) | Low | Solar PV, LEDs | ~20--23% |
| Type 2 (intermediate) | Medium | Wind, EVs, rooftop PV | ~10--15% |
| Type 3 (complex, customized) | High | Nuclear, CCS, biomass | ~0--5% |

Theoretical basis: McNerney et al. (2011) and Fink & Reeves showed mathematically that "the more complex the design, the slower the rate of improvement."

**Fusion-specific**: Tang & Schmidt (2025) rated MFE design complexity at 6.8/7 and LFE at 6.4/7 via expert elicitation -- both exceeding nuclear fission (benchmarked at 6/7). PV panels rated ~2/7.

- Malhotra, A. & Schmidt, T.S. (2020). "Accelerating Low-Carbon Innovation." *Joule* 4: 2259--2267. [DOI](https://doi.org/10.1016/j.joule.2020.09.004). Local: `knowledge/meta_analysis/accelerating_low_carbon_innovation/output.md`

#### 3. Need for Customization

**Evidence strength: Moderate (typology-based, not independently regressed)**

The second dimension of the Malhotra & Schmidt typology: "the extent to which a technology must be adapted to its use environment" (physical, regulatory, user-specific). Technologies needing local adaptation have lower *global* learning rates because knowledge spillovers become context-specific.

**Fusion-specific**: Tang & Schmidt rated MFE customization at 5.0/7, LFE at 4.3/7 -- slightly below nuclear fission, attributed to fusion's inherent safety advantages reducing regulatory customization. This is the one dimension where fusion may slightly outperform fission.

**Key insight**: Customization is independent of complexity. A technology can be large but standardized (e.g., CCGT: moderate learning) or small but customized (e.g., building retrofits: low learning).

#### 4. Factory-Buildability / Modular Manufacturing

**Evidence strength: Moderate (SMR projections + historical analogues)**

**Quantitative evidence from the OECD-NEA (2020) report**:
- 60--80% factory fabrication levels are achievable for designs below 300 MWe (Lloyd 2019)
- Industries with serial manufacturing (shipbuilding, aircraft): 10--20% learning rates (NNL 2014)
- Nuclear pair construction: ~15% cost reduction on the second unit (NEA 2000)
- Barakah (UAE) 4-unit project: costs fell >50% from first to fourth unit (Gogan 2019)

**SMR-specific projections** (Mignacca & Locatelli 2019):
- Expected learning rate: 5--10% with 45--60% factory fabrication proportion
- 10% cost reduction per doubling of volume with 30% factory fabrication
- Learning curve flattens after 5--7 units
- Co-siting economies: 15--20% capital cost savings from shared infrastructure
- Economy of scale penalty: SMR OCC is 70% greater by size alone; after multiples (14%), learning (8%), schedule (6%), design (17%), only 5% higher

**Kavlak et al. (2018)** decomposition: Manufacturing plant scale-up explained >1/3 of solar PV cost reductions 2001--2012. This mechanism is unavailable for site-assembled technologies.

- OECD NEA (2020). *Unlocking Reductions in the Construction Costs of Nuclear.* NEA No. 7530. [NEA PDF](https://www.oecd-nea.org/upload/docs/application/pdf/2020-07/7530-reducing-cost-nuclear-construction.pdf)
- Mignacca, B. & Locatelli, G. (2020). "Economics and finance of Small Modular Reactors." *RSER* 118: 109519. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1364032119307270). Local: `knowledge/meta_analysis/economics_and_finance_of_smr/output.md`

#### 5. Series Construction / Unit Replication Path

**Evidence strength: Moderate-Strong (nuclear fleet data)**

**Quantitative nuclear fleet evidence (OECD-NEA 2020)**:

| Programme | Observed Cost Reduction | Mechanism |
|---|---|---|
| Pair construction (generic) | ~15% on second unit | Shared infrastructure, workforce retention |
| Second pair vs. first pair | Additional ~5% | Series standardization |
| Barakah (UAE) 4 units | >50% first-to-fourth | Continuous construction, Korean design standardization |
| Korean programme | 75 → 53 months (first twin to second pair) | Lead time compression |
| French CP1-CP2 series | ~23% reduction within series | Fleet standardization |
| French P4-P4' series | ~19% reduction within series | Fleet standardization |
| French N4 series | ~6% reduction within series | Diminishing returns, design changes |
| Sizewell B → Sizewell C | 37% OCC reduction (up to 55% with non-recurrent indirects) | FOAK-to-NOAK, same design |

**Critical threshold**: Need **>6 units** to "take full advantage of a standardised series effect" (OECD-NEA). The 25--40% combined savings (OCC + IDC) from series construction represents one of the strongest quantified learning effects in capital-intensive generation.

**Korean success vs. US failure**: Korea built 54 units in 15 years (up to 8 commissioned in one year) with continuous supply chains. Countries with construction hiatuses lost capabilities and saw costs rise. Programme continuity is as important as technology design.

- Lovering, J.R. et al. (2016). "Historical construction costs of global nuclear power reactors." *Energy Policy* 91: 371--382. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0301421516300106). Local: `knowledge/meta_analysis/historial_construction_costs_of_global_nuclear_power_reactors/output.md`

#### 6. Regulatory Classification and Stability

**Evidence strength: Moderate (case-study-based, strong causal logic)**

The key finding is that regulatory *instability* (not burden per se) destroys learning:

- **Davis-Besse (US)**: Cost escalated from $136M to $650M. **$398M (61% of final cost) attributed to NRC modifications and their chain effects** (Basset 1978, cited in OECD-NEA 2020)
- **US nuclear fleet**: Steel requirements +41%, concrete +27%, piping +50%, cable +36% between early and late 1970s -- quadrupled costs (Cohen, U. Pittsburgh)
- **Lack of international regulatory harmonization**: Adds ~30% to EPC costs (OECD-NEA 2020, Box 14)
- **Nuclear-grade vs. industrial-grade components**: Cost gap roughly 2× for equivalent valves (OECD-NEA Figure 28), driven by quality management qualification, not materials
- **NRC proposed fusion framework (Feb 2026)**: Classifying fusion under 10 CFR Part 30 (byproduct material) rather than Part 50/52 (power reactors) -- significantly lighter than fission. Aneutronic concepts could face even lighter requirements.

**France vs. US**: France (stable regulatory regime, standardized fleet) achieved substantially lower costs than the US (mid-build regulatory changes, bespoke designs). But even France showed real-term cost escalation over its full programme (Grubler 2010) -- regulatory stability is necessary but not sufficient.

#### 7. Supply-Chain Commodity vs. Specialty Materials

**Evidence strength: Suggestive (case studies, no regression)**

No study directly regresses "supply chain depth" as a numerical variable against learning rates. The evidence is qualitative but compelling:

- **Nuclear-grade qualification** almost doubles component costs (OECD-NEA Figure 28)
- **REBCO HTS tape**: Currently ~$100/kA-m; projected to drop to <$10/kA-m with volume (approaching Nb-Ti commodity pricing). Raw material cost is low -- the premium is immature manufacturing, not scarcity (Wang et al. 2022). But: "We have barely enough conductors to make one magnet every several years."
- **Tritium/Li-6**: World tritium inventory ~50 kg, production ~2 kg/yr. Enriched Li-6 "supply is practically zero." "Most resource supply chains are not yet ready for even pilot plant scale" (Pearson 2022).
- **Solar PV analogy**: Silicon (commodity, deep supply chain) was one of three dominant cost-reduction drivers (Nemet 2006). Chinese manufacturing competition in a commodity material supply chain was a critical enabler of the post-2008 price crash.

**Supply chain immaturity directly limits learning-rate potential**: you cannot learn-by-doing without a supply chain to do with.

- Wang et al. (2022). "REBCO: silver bullet for high-field magnets." arXiv:2203.08736. [arXiv](https://arxiv.org/pdf/2203.08736). Local: `knowledge/meta_analysis/rebco_silver_bullet_for_high_field_magnet_collider_budget/output.md`
- Pearson/Kyoto Fusioneering (2022). "Resource Availability and Supply." DOE FES Workshop. [DOE PDF](https://science.osti.gov/-/media/fes/pdf/fes-presentations/2022/Pearson_resource-availability-and-supply_presentation.pdf). Local: `knowledge/meta_analysis/Pearson_resource_availability_and_supply_presentation/output.md`

#### 8. Plant Footprint

**Evidence strength: Weak (no direct studies)**

No studies found that directly correlate physical footprint with learning rates. Plant footprint correlates with unit size and is not an independent predictor. Not recommended as a standalone scoring dimension.

### The Tang & Schmidt Fusion-Specific Prediction

Tang & Schmidt (2025, *Nature Energy*) is the single most directly relevant paper for our down-selection. They applied the Malhotra & Schmidt typology specifically to fusion power plants via structured expert elicitation:

| Feature | MFE Rating | LFE Rating | Fission Benchmark |
|---|---|---|---|
| Design complexity | 6.8/7 | 6.4/7 | 6/7 |
| Need for customization | 5.0/7 | 4.3/7 | ~5.5/7 |
| Minimum unit size | ~530 MW | ~230 MW | Variable |

**Predicted experience rate for fusion**: ~5% (median of 2--8% range for Type 3 technologies). This is dramatically lower than the 8--20% assumed in prior fusion TEA literature. The paper documents that existing assumptions range from "none" (no rationale given) to "upper value of ER for coal and natural gas" -- most are essentially ungrounded.

**FOAK cost anchoring**: Private sector experts averaged $7,000/kW vs. public sector experts at $26,000/kW, attributed to "optimism bias in firms." The IQR of compiled estimates was used to filter anomalous highs/lows.

- Tang, L. & Schmidt, T.S. (2025). "Fusion power experience rates are overestimated." *Nature Energy*. Local: `knowledge/meta_analysis/fusion_power_experience_rates_are_overestimated/output.md`

### Correlation Structure and Composite Predictors

The features above are partially correlated:

- **Unit size, complexity, and component count**: R² = 0.77 (Wilson et al.) -- larger technologies tend to be more complex
- **Unit size and factory-buildability**: Inversely correlated -- larger units are harder to factory-fabricate
- **Standardization and replication path**: Correlated -- standardized designs enable higher replication counts
- **Regulatory class and customization need**: Correlated -- heavier regulation forces more site-specific adaptation

The literature suggests two relatively independent composite dimensions:

1. **Manufacturing paradigm** (combines unit size + factory-buildability + replication path + supply chain): Captures how the technology gets built and how many get built. The solar/battery end vs. the nuclear/CCS end.
2. **Design-environment interface** (combines complexity + customization + regulatory class): Captures how much the technology must adapt to its deployment context. The standardized-commodity end vs. the bespoke-regulated end.

These two composite dimensions are partially but not fully correlated -- a technology can be factory-built but regulatory-heavy (SMR thesis), or site-built but standardized (CCGT).

### Quantitative Summary Table

| Predictor Feature | Direction | Quantitative Strength | Source Quality | Fusion Discrimination |
|---|---|---|---|---|
| Unit size (MW/unit) | Smaller → faster LR | R² = 0.33 (cross-tech) | Strong | High (200--1000+ MW range) |
| Design complexity | Simpler → faster LR | Type 1 ~22% vs. Type 3 ~5% ER | Strong (typology validated) | Moderate (all fusion is complex, but degrees vary) |
| Need for customization | More standardizable → faster LR | Type 3 ~5% vs. Type 1 ~22% ER | Moderate (typology-based) | Moderate (aneutronic vs. D-T, siting flexibility) |
| Factory fabrication % | Higher → faster LR | 60--80% enables 10--20% LR analogues | Moderate (SMR projection) | High (compact vs. ITER-scale) |
| Series replication (>6 units) | More → faster LR | 15--50% reduction over series | Strong (nuclear fleet data) | High (modular vs. economy-of-scale) |
| Regulatory stability | More stable → faster LR | 30--61% cost from regulatory changes | Moderate (case studies) | Moderate (Part 30 vs. Part 50/52) |
| Supply chain commodity fraction | Higher → faster LR | ~2× cost penalty for nuclear-grade | Suggestive (case studies) | High (copper/steel vs. REBCO/tritium) |
| Plant footprint | Smaller → faster LR | No direct evidence | Weak | Low (correlated with unit size) |

### Methodological Caveat

All cross-technology studies use bivariate or at best two-dimensional correlations across 10--30 technologies. R² values are moderate (0.33 for the strongest predictor). These are associations, not controlled experiments. Within-technology evidence (nuclear fleet studies) provides stronger causal evidence but is limited to case studies. **No study runs a full multivariate regression with all predictors simultaneously.** This is the key gap.

### Implications for Our Down-Selection

For Phase 2(c) (learning-curve plausibility), the literature supports scoring fusion concepts on six features with defensible evidence:

1. **Unit size** (smaller is better; below 300 MWe enables 60--80% factory fabrication)
2. **Design complexity** (fewer interacting novel subsystems is better)
3. **Standardizability** (less site-specific adaptation is better)
4. **Factory fabrication fraction** (higher is better; 60--80% is the SMR threshold)
5. **Regulatory class** (lower nuclear-grade component fraction is better)
6. **Programme replication feasibility** (need >6 units for full series effect; smaller/cheaper units have shorter paths to >6)

The base-rate prediction for any fusion concept is ~5% ER (Tang & Schmidt). Concepts that excel on the features above may achieve somewhat higher rates; concepts that cluster at the ITER-scale extreme may achieve lower. But the evidence strongly suggests no fusion concept is likely to reach Type 1 learning rates (>20%) -- the inherent complexity of fusion power systems places a ceiling.

---

## Cross-Reference: Local Meta-Analysis Sources Used

All 17 directories under `knowledge/meta_analysis/` were read. The following were directly relevant:

| Source Directory | Relevance |
|---|---|
| `fusion_power_experience_rates_are_overestimated` | **Primary** for Q5 -- Tang & Schmidt fusion ER prediction |
| `accelerating_low_carbon_innovation` | **Primary** for Q5 -- Malhotra & Schmidt typology |
| `Granularity_Manuscript_preprint` + `science_aaz8060...` | **Primary** for Q5 -- Wilson et al. granularity correlations |
| `review_of_learning_rates_for_electricity_supply_technologies` | **Primary** for Q4+Q5 -- Rubin et al. meta-review, component-based learning for data-sparse tech |
| `how_predictable_is_technological_progress` | Supporting for Q5 -- Farmer & Lafond predictability of cost trends |
| `empirically_grounded_technology_forecasts_and_the_energy_transition` | Supporting for Q5 -- Way et al. Wright's law forecasting |
| `historial_construction_costs_of_global_nuclear_power_reactors` | **Primary** for Q5 -- Lovering et al. nuclear fleet learning |
| `economics_and_finance_of_smr` | **Primary** for Q5 -- Mignacca & Locatelli SMR learning projections |
| `Extrapolating_Costs_to_Commercial_Fusion_Power_Plants__1_` | Supporting for Q4 -- Foster et al. on cost model limitations |
| `what_you_should_know_about_megaprojects_and_why` | Supporting for Q5 -- Flyvbjerg megaproject dynamics |
| `learning_from_case_studies_financing_and_development_foak` | Supporting for Q4 -- DOE OCED Adoption Readiness Levels |
| `what_is_foak` | Supporting for Q4 -- practitioner perspective on FOAK uncertainty |
| `bringing_fusion_energy_to_the_grid` | Supporting context |
| `proposed_rules_fusion_regulatory` | Supporting for Q5 -- NRC fusion regulatory framework |
| `Pearson_resource_availability_and_supply_presentation` | Supporting for Q5 -- supply chain constraints |
| `rebco_silver_bullet_for_high_field_magnet_collider_budget` | Supporting for Q5 -- HTS cost trajectory |

---

## Open Questions / Gaps

1. **No multivariate regression exists** combining all predictor features simultaneously. The cross-technology R² values (0.33 at best) leave substantial unexplained variance. We will need to exercise judgment about feature weighting rather than relying on a single empirical formula.

2. **Fusion-specific calibration is absent.** The CATF/Woodruff U_TRL factor needs empirical calibration against fusion-relevant data (the NASA models are calibrated on aerospace). Until fusion plants are built, the uncertainty widening factors are themselves uncertain.

3. **Programme characteristics vs. technology characteristics**: The nuclear fleet data (Korea vs. US, France vs. UK) suggests that programme execution (build continuity, regulatory stability, workforce retention) may matter as much as technology design. Our down-selection scores technology characteristics, but a concept's learning-curve plausibility also depends on the *programme* that would build it -- which we cannot score from concept-level data alone.

4. **Non-monotonic effects**: The OECD-NEA data shows learning flattens after 5--7 units and regulatory changes can reverse it entirely. Learning curves are not guaranteed monotone; scoring must account for the fragility of projected learning, not just its slope.
