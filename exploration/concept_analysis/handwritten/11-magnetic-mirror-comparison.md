# Comparison Report: Handwritten vs. Automated Concept Analysis — Magnetic Mirror (D-T)

**Date:** 2026-03-22
**Subject:** Concept 11 — Magnetic Mirror (D-T), Realta Fusion
**Handwritten files:** `handwritten/11-magnetic-mirror.md`, `handwritten/11-magnetic-mirror.py`
**Automated files:** `analyses/11-magnetic-mirror/` (analysis.md, model_setup.py, review.md, synthesis.md, gap_report.md, model_output.txt)

---

## 1. Executive Summary

The handwritten analysis reads like a domain expert's notebook — insightful, opinionated, and grounded in physics intuition. The automated pipeline produces a structured due-diligence document — systematic, citation-traced, and conservative. Both have real strengths. Both have real problems.

The **qualitative** outputs diverge primarily in depth, structure, and source rigor. The handwritten analysis offers unique expert judgment (e.g., dismissal of Venetian blind DEC, personal PhD context on ponderomotive plugging) but lacks structured TRL assessments, data gap inventories, and traceable citations. The automated analysis is thorough on all of these but occasionally verbose and mechanically conservative.

The **quantitative** outputs diverge significantly in LCOE: **80.2 vs. 135.2 $/MWh** (handwritten vs. automated). This is a 69% difference driven by compounding parameter disagreements. The automated model is better documented and more defensible. The handwritten model contains an internal contradiction between its qualitative dismissal of DEC and its quantitative reliance on aggressive DEC parameters.

**Bottom line:** The automated pipeline produces a more reliable, auditable analysis. The handwritten analysis contains expert insights the pipeline cannot replicate. Neither is sufficient alone — the ideal output would combine the handwritten expert judgment with the automated pipeline's rigor and traceability.

---

## 2. Qualitative Analysis Comparison

### 2.1 Scope and Coverage

| Topic | Handwritten | Automated | Winner |
|-------|:-----------:|:---------:|:------:|
| Device description / concept overview | Yes (detailed) | Yes (detailed) | Tie |
| Physics of confinement | Yes (expert-level) | Yes (thorough) | Handwritten |
| End-plug approaches (tandem, centrifugal, ponderomotive, non-axisymmetric) | Yes (4 approaches) | Tandem only | Handwritten |
| Data availability assessment | Brief | Detailed with rating | Automated |
| Challenges in capturing system function | Brief (4 physics + 5 DT items) | 5 ranked challenges with impact ratings | Automated |
| Subsystem TRL assessments | Informal mentions only | 7 subsystems with TRL ranges + demonstrated/paper/missing structure | Automated |
| Materials and supply chain | One sentence | Detailed (REBCO, tritium, Li-6, NBI, gyrotrons) with cost proxies | Automated |
| Data gap inventory | None | 12 gaps with type/criticality/source recommendations | Automated |
| Cross-concept comparison | None | 4 prior analyses referenced, structural advantages/disadvantages tabulated | Automated |
| LCOE parameter table (available + missing) | None | Comprehensive table with 13 available + 12 missing parameters | Automated |
| Source recommendations | None | 6 prioritized source recommendations | Automated |
| Historical context (MARS, MINIMARS) | Mentioned with cost result (7 ¢/kWh, 1983$) | Extensively used as analogue | Automated |
| References | 7 listed | 8 with full citations + source verification | Automated |

**Assessment:** The automated pipeline covers substantially more ground. The handwritten analysis is narrower in scope but deeper on topics it does cover (especially physics and end-plug variations). The automated analysis's gap inventory and cross-concept comparison sections have no handwritten equivalent.

### 2.2 Source Rigor and Citation Quality

**Handwritten:** Lists 7 references at the end. No inline citations link specific claims to specific sources. When the MARS/MINIMARS LCOE result is quoted ("7 cent/kWh in 1983 dollars"), no specific page or section is cited. When TRL claims are made ("TRL 5" for Venetian blinds), no source is given. The reader must trust the author's expertise.

**Automated:** Every factual claim carries an inline citation with source file path and section anchor (e.g., `arxiv-2411-06644-confinement-predictions.md §Key Technical Details`). The review stage (review.md) independently verified 15 citations against the actual source documents — 14 exact matches, 1 partial match. The pipeline caught its own errors: the review identified a "500 MW" unit ambiguity (source says "500 MW" without specifying thermal/electric) and flagged it. The address log shows all 4 proposed actions were accepted and applied.

**Assessment:** The automated pipeline is decisively stronger. Traceable citations are not optional in techno-economic analysis — they are what separates analysis from opinion. The handwritten analysis relies entirely on the reader trusting the author. The automated analysis is independently auditable.

**Critical note on the automated citations:** The review stage (review.md) found that some citations are chain-inferred rather than directly traceable. CV-14 (gyrotron wall-plug efficiency "~45–55%") traces to analysis.md rather than to a primary source document. CV-15 (REBCO operating temperature "20 K") is not stated in the cited source. These are minor issues — the values are physically correct — but they show the pipeline sometimes launders self-generated content as sourced content.

### 2.3 Depth of Technical Analysis

**Handwritten strengths:**
- The physics section demonstrates genuine understanding of loss-cone dynamics, magnetic moment conservation, and the origin of the mirror name
- End-plug taxonomy (tandem, centrifugal, ponderomotive, non-axisymmetric) is broader than the automated analysis, which focuses only on tandem mirrors because Realta pursues that approach
- Personal context on ponderomotive plugging ("This is my PhD thesis topic") signals deep domain expertise
- The statement that LCOE "saturates around 600 MWe" (from MARS/MINIMARS) is a valuable economic insight not captured in the automated analysis
- The observation that mirrors "require working in a hot (radioactive) cell surrounding entire machine" for module replacement shows practical engineering awareness

**Automated strengths:**
- Challenge ranking by economic impact (Critical/High/Moderate) with specific LCOE consequences
- TRL ladder for every subsystem with clear evidence citations
- Explicit distinction between "demonstrated," "on paper only," and "missing at scale" for each subsystem
- Materials section quantifies supply chain concerns with actual numbers ($50M REBCO, $35,000/g tritium, 25-30 kg global inventory)
- The synthesis document identifies the single most important risk (end-plug confinement) and the single most important advantage (linear scaling) with correct prioritization

**Assessment:** The handwritten analysis is deeper on physics and broader on concept variants. The automated analysis is deeper on economics, subsystem maturity, and data gaps. For a techno-economic analysis, the automated approach is more useful. For a physics review, the handwritten is more valuable.

### 2.4 Domain Expertise and Calibration

**Handwritten:** The author clearly understands magnetic mirror physics at a professional level. The discussion of loss cones, magnetic moment, end-plug approaches, and NBI injection angles is accurate and specific. The mention of contemporary companies (Realta, Terra Fusion, Gridfire, TAE) is current. The statement that Venetian blinds have "~50-65% efficiency, which is not *that* high compared to turbines" shows practical engineering judgment (though the comparison is somewhat misleading — DEC applies to a different energy stream than the thermal cycle).

**Automated:** The pipeline demonstrates systematic knowledge application rather than expert intuition. It correctly identifies the key physics uncertainties (DCLC, end-plug confinement) but doesn't explain *why* they matter at the mechanistic level. It accurately quantifies TRL levels but the assessments read like they were produced by carefully reading source documents rather than by someone who has worked in the field. The synthesis document's "What Would Change My Mind" section shows good analytical calibration — it identifies the three most impactful future developments and quantifies their potential LCOE impact.

**Assessment:** The handwritten analysis is written by an expert. The automated analysis is written for experts. The calibration of the automated analysis is arguably better — it is more careful about distinguishing what is known from what is assumed, and its uncertainty ranges are more conservative. But the handwritten analysis's physics intuition catches things the pipeline misses (e.g., the LCOE saturation at 600 MWe, the breadth of end-plug approaches, the practical challenge of hot-cell operations on a linear machine).

### 2.5 Critical Thinking and Risk Assessment

**Handwritten:** Identifies four open physics questions and five generic D-T challenges. The risk assessment is flat — no ranking by importance or economic impact. The Venetian blind dismissal ("I think this is not worth considering") is a strong opinion backed by reasoning (low efficiency relative to thermal cycle, electrode survivability concerns) — this is valuable expert judgment that the automated pipeline cannot produce. However, this dismissal is not reflected in the quantitative model, which uses DEC aggressively (see Section 3).

**Automated:** Ranks five challenges by economic impact with specific LCOE consequences. The synthesis provides explicit "Risk Verdicts" with calibrated language ("Genuinely uncertain — concept-gating" vs. "Likely resolvable — timeline-extending"). The distinction between risks that could reduce Q by 2x (DCLC) and risks that might delay licensing by a few years (regulatory) is useful. The synthesis explicitly states "This concept's structural claim rests entirely on the center-cell linear scaling thesis, which has not been costed at any level of detail" — this is a sharp and correct observation.

**Assessment:** The automated analysis does a better job of prioritizing risks and quantifying their potential impact. The handwritten analysis contains sharper individual judgments (e.g., the Venetian blind dismissal) but doesn't integrate them into a coherent risk picture. The automated synthesis's statement about the linear scaling thesis being the key claim is arguably the single most important sentence in either analysis — and it appears only in the automated output.

### 2.6 Key Content Differences

**Handwritten claims not in automated:**
1. "LCOE saturates around 600 MWe" (from MARS/MINIMARS) — valuable economic insight
2. Module replacement and hot-cell operations as a practical concern
3. End-plug taxonomy beyond tandem mirrors (centrifugal, ponderomotive, non-axisymmetric)
4. Alpha channeling for ash removal through loss cone
5. "Current developments allow to use simpler magnet geometry and better HTS" (vs. MARS yin-yang coils)
6. Explicit dismissal of DEC as not worth considering for commercial viability

**Automated claims not in handwritten:**
1. $50M REBCO tape cost for WHAM++ as a cost proxy
2. $9.5M SVB facility funding context
3. First plasma date (July 2024) for WHAM
4. End-plug physics is "comparable to claiming Q=10 before achieving burning plasma"
5. DEC contribution is modest for D-T (~11% of fusion power recovered)
6. Overnight capital estimate of $9,620/kW with confidence rating
7. Comprehensive cross-concept positioning against tokamak and FRC analyses

---

## 3. Quantitative (LCOE) Model Comparison

### 3.1 Summary of Results

| Metric | Handwritten | Automated | Difference |
|--------|------------|-----------|------------|
| **LCOE** | **80.2 $/MWh** | **135.2 $/MWh** | **+69%** |
| Overnight cost | 5,862 $/kW | 9,620 $/kW | +64% |
| Fusion power | 1,137 MW | 1,683 MW | +48% |
| Net electric | 500 MW | 500 MW | — |
| Q_eng | 4.6 | 2.8 | -39% |
| Recirculating fraction | 22.0% | 35.8% | +63% |
| Total capital | ~$2,931M (est.) | $4,810M | +64% |

The automated model produces a substantially more expensive and less efficient plant. The differences compound: higher recirculating fraction requires more fusion power, which requires a larger reactor, which costs more, which raises LCOE.

### 3.2 Parameter-by-Parameter Comparison

#### Parameters that drive the LCOE divergence (ordered by impact):

| Parameter | Handwritten | Automated | Impact on LCOE | Assessment |
|-----------|------------|-----------|----------------|------------|
| **chamber_length** | 20.0 m | 70.0 m | High — drives building cost | **Automated is more defensible.** The arxiv paper targets 50m for Q>5 at Hammir pilot. MARS was ~100m. A 20m commercial mirror appears in no design study. The handwritten value produces unrealistic implied Q (see 3.3). |
| **CAS21 override** | $250M | None ($592M from framework) | High — $342M difference | **Automated is more defensible.** The override is unjustified in the handwritten model — no source is given for $250M. Even with a 20m chamber, $250M for a D-T fusion building is aggressive. |
| **eta_th** | 0.50 | 0.40 | Medium — affects power balance | **Automated is more defensible.** MARS achieved ~36%. Even with optimistic sCO2, 45% is aggressive. 50% thermal efficiency for a D-T plant with blanket heat extraction has no precedent. |
| **p_input** | 40 MW | 100 MW | Medium — affects recirculating power | **Both are uncertain.** Neither has a source. The automated model acknowledges this explicitly as "UNCERTAIN: proprietary for Hammir." The handwritten model provides no justification. |
| **f_dec** | 0.30 | 0.20 | Medium — affects DEC contribution | **Automated is more physically grounded.** D-T physics: 80% of fusion energy is in neutrons (blanket), 20% in alphas. The handwritten value of 0.30 may attempt to account for unburned fuel ions also escaping through the loss cone, but this is not stated. Without explanation, 0.30 overstates the DEC energy stream. |
| **eta_de** | 0.60 | 0.54 | Low — but compounds with f_dec | **Both are defensible.** Venetian blinds in the 1970s showed 50-65% range. The automated model conservatively uses the MARS historical value. |
| **p_coils** | 5.0 MW | 10.0 MW | Low | **Automated is better justified** (acknowledges uncertainty, explains elevation from default). |
| **p_cool** | 20.0 MW | 25.0 MW | Low | Minor difference. |
| **p_trit** | 10.0 MW | 12.0 MW | Low | Minor difference. |
| **p_cryo** | 1.0 MW | 2.0 MW | Negligible | Automated justifies elevation for larger magnet set. |

#### Combined effect of efficiency assumptions:

The handwritten model's optimistic trio — eta_th=0.50, f_dec=0.30, eta_de=0.60 — produces a fundamentally different power balance:
- Less fusion power needed for 500 MWe net (1,137 MW vs 1,683 MW)
- Lower recirculating fraction (22% vs 36%)
- Higher Q_eng (4.6 vs 2.8)

Each parameter individually might be defensible with argument. Taken together, they represent a systematically optimistic power balance with no stated uncertainty range. The automated model uses more conservative values and explicitly labels each as UNCERTAIN with confidence levels.

### 3.3 Internal Consistency Assessment

**Critical inconsistency in the handwritten model:**

The handwritten qualitative analysis states:
> "Venetian blinds... have a ~50-65% efficiency, which is not *that* high compared to turbines. This technology has a TRL 5... the added efficiency over and above a thermal cycle is small. The survivability of thin uncooled electrodes downstream of a fusion reactor is low. **I think this is not worth considering.**"

Yet the handwritten quantitative model uses:
- `f_dec = 0.30` (30% of transport power to DEC — more than the 20% alpha fraction)
- `eta_de = 0.60` (60% DEC efficiency — near the top of the claimed range)

**This is a direct contradiction.** The qualitative analysis dismisses DEC as not worth considering, but the LCOE model uses DEC aggressively — with parameters more optimistic than even the automated pipeline. The DEC contribution in the handwritten model reduces LCOE by capturing 30% × 60% = 18% of transport power as electricity. Removing DEC (f_dec=0, eta_de=0) from the handwritten model would significantly increase LCOE, narrowing the gap with the automated result.

**Implied Q_plasma inconsistency in the handwritten model:**

With chamber_length=20m and the ~7 MWt/m scaling from Realta, the center cell should produce ~140 MWt of fusion power. But the model outputs P_fus = 1,137 MW. This means the costingfe framework back-solves from net electric power to fusion power, and chamber_length only affects capital costs, not the physics power balance. The implied Q_plasma = P_fus / p_input = 1,137 / 40 = 28.4. No mirror concept has ever been projected at Q = 28. The WHAM paper targets Q > 5. This Q value is physically unrealistic and suggests the model parameters are not self-consistent with mirror physics.

In contrast, the automated model shows P_fus = 1,683 MW with p_input = 100 MW, giving Q_plasma ≈ 16.8. This is still high but more consistent with the "Q > 10 possible with longer cell" projection at commercial scale.

**Neither model achieves full internal consistency** between physics parameters and LCOE model inputs. The costingfe framework appears to treat chamber geometry and power balance as independent — the user must ensure they are self-consistent, and neither the handwritten nor automated models fully do so. The automated model is closer to self-consistency (70m × 7 MWt/m ≈ 490 MWt is in the same order of magnitude as a 500 MWe plant at ~40% efficiency, though the actual P_fus=1683 MW reflects the recirculating power requirement).

**Automated model internal inconsistency (caught by review):**

The review stage found that the original model_setup.py comment claimed "Q~10, 1000 MWt" for the 70m chamber, but the geometry implies Q~5 at ~490 MWt. This was caught in review iteration 1 (PA-2) and corrected in the address log. The corrected comment now correctly states Q~5 consistency. This demonstrates the value of the review stage.

### 3.4 Documentation and Traceability

**Handwritten model (11-magnetic-mirror.py):**
- 104 lines, no comments explaining parameter choices
- No source citations for any parameter value
- No uncertainty flags
- No sensitivity analysis methodology explanation (uses `model.sensitivity()` but doesn't interpret results)
- Brief output formatting, minimal context

**Automated model (model_setup.py):**
- 277 lines including extensive docstring
- Every parameter has inline comments with:
  - Source citation (file + section)
  - UNCERTAIN/DEFAULT flag
  - Physical reasoning for the chosen value
  - Reference to alternatives considered
- 47-line "Data Quality Warning" documenting what the model cannot capture
- Key assumptions printed in output for reader reference
- The review stage independently audited 10 model parameters (MSA-1 through MSA-10) with traceability judgments

**Assessment:** The automated model is an order of magnitude better documented. A reader of the handwritten model must reverse-engineer why each parameter was chosen. A reader of the automated model can trace every choice to its justification and source. For a techno-economic analysis intended to inform investment or policy decisions, the automated model's documentation standard is the minimum acceptable level.

### 3.5 Sensitivity Analysis

Both models run `model.sensitivity()` and print elasticity tables.

**Handwritten:** Prints raw elasticity values in two categories (engineering, financial) with no interpretation.

**Automated model_output.txt:** Same raw elasticity output. However, the synthesis.md interprets the sensitivity results in Section 2, ranking the top 5 levers by elasticity magnitude, providing the assumed value, the sensitivity range (e.g., "Dropping from 85% to 60% availability raises LCOE by ~21%"), and a "What flips the economics" narrative for each lever. This interpretation transforms raw numbers into actionable insight.

The handwritten analysis includes a valuable "Back-Solve to $0.01/kWh" section that the automated pipeline does not produce. This section concludes that "DT mirror can't reach 1 ¢/kWh, even with extreme assumptions. The best case... gets to 2.70 ¢/kWh." This is a useful analytical exercise that stress-tests the concept's economic ceiling. However, the back-solve uses the handwritten model's optimistic baseline — if the automated model's parameters were used, the floor would be even higher.

### 3.6 CAS Cost Structure Comparison

The handwritten model does not include full CAS breakdown in its output as shown in the markdown file, but the script prints it. The automated model shows:

| Account | Automated (M$) | Notes |
|---------|:---------:|-------|
| CAS21 (Buildings) | 592.1 | Handwritten overrides to 250.0 |
| CAS22 (Reactor Plant Equipment) | 2,454.4 | Likely similar framework calculation |
| CAS30 (Indirect Costs) | 557.5 | Scales with direct costs |
| CAS60 (IDC) | 627.9 | Sensitive to total capital and construction time |
| CAS70 (O&M annualized) | 115.1 | Based on plant size |

The CAS21 override in the handwritten model ($250M vs $592M) is the single largest identifiable cost difference. This alone accounts for ~$342M in direct costs, plus indirect cost and IDC ripple effects. With no justification provided, this override is the weakest element of the handwritten LCOE calculation.

---

## 4. Strengths and Weaknesses

### 4.1 Handwritten Analysis

**Strengths:**
- Expert physics intuition throughout
- Broader end-plug taxonomy (4 approaches vs. 1)
- Unique insights (LCOE saturation at 600 MWe, hot-cell practical challenges)
- Concise and readable — the qualitative section is ~120 lines vs. ~330 lines for the automated analysis
- Opinionated where appropriate (DEC dismissal, "this is my PhD thesis topic")
- Back-solve analysis tests the concept's economic ceiling
- References section includes foundational papers (Post 1987, Ryutov 1988)

**Weaknesses:**
- No inline citations — claims are unverifiable without trusting the author
- No structured TRL assessments
- No data gap inventory
- No cross-concept comparison
- Quantitative model uses parameters that contradict the qualitative analysis (DEC)
- chamber_length=20m has no basis in any design study
- CAS21 override ($250M) is unjustified
- eta_th=0.50 is unrealistically optimistic for a D-T plant
- Implied Q_plasma ≈ 28 is physically unrealistic
- No uncertainty flags or confidence levels on any parameter
- Sensitivity results printed but not interpreted

### 4.2 Automated Pipeline

**Strengths:**
- Comprehensive coverage with structured sections
- Every claim traced to a specific source with section anchors
- Self-auditing review stage caught 4 issues and corrected them
- Conservative parameter choices with explicit UNCERTAIN/DEFAULT flags
- Data gap inventory with criticality ratings and source recommendations
- Cross-concept comparison provides context
- Synthesis document integrates risks and sensitivities into a coherent economic narrative
- "What Would Change My Mind" section is calibrated and actionable
- Model documentation is independently auditable

**Weaknesses:**
- Verbose — the full analysis set (analysis.md + gap_report.md + review.md + synthesis.md) is ~1,000+ lines across 4 documents. Some information is repeated across documents.
- Cannot replicate expert judgment or insider knowledge (e.g., the handwritten author's ponderomotive plugging expertise, the LCOE saturation insight)
- Regulatory risk section (§S2 Challenge 5) is speculative and adds limited value
- Some citations are chain-inferred rather than primary (CV-14, CV-15)
- The review stage's "calculations checked: 3" is a small sample given the number of derived quantities
- Does not include a back-solve or floor analysis
- Narrower on physics (only covers Realta's tandem approach, not the broader mirror concept space)
- The pipeline focuses on Realta Fusion specifically rather than the magnetic mirror concept generically — this is a design choice but limits the analysis's generality

---

## 5. Verdict

### 5.1 Which is more reliable?

**The automated analysis is more reliable.** Its LCOE of 135.2 $/MWh is better supported, more conservatively parameterized, and more thoroughly documented than the handwritten 80.2 $/MWh. The handwritten model's lower LCOE stems from a combination of optimistic efficiency assumptions, an unjustified building cost override, and an unrealistic chamber length — all undocumented. The internal contradiction between dismissing DEC qualitatively and relying on it quantitatively undermines the handwritten model's credibility.

### 5.2 Which is more useful?

**Depends on the audience.** For a domain expert who can independently evaluate parameter choices, the handwritten analysis is a quick, opinionated assessment that identifies the right issues. For anyone else — including future versions of the same expert who may not remember the reasoning — the automated analysis is more useful because every choice is documented and auditable.

### 5.3 What would the ideal analysis look like?

The ideal analysis would:
1. Use the automated pipeline's structure, citation standards, and parameter documentation
2. Incorporate the handwritten analysis's broader end-plug taxonomy and physics depth
3. Resolve the DEC question explicitly: either dismiss DEC (f_dec=0) with stated reasoning, or use it with a physics-derived f_dec value and a stated uncertainty range — not both
4. Use a chamber_length derived from a self-consistent physics model (50-70m for Q > 5-10, not 20m)
5. Include the back-solve analysis from the handwritten work, run on the more conservative automated baseline
6. Add the "LCOE saturates at 600 MWe" insight from MARS/MINIMARS as a cross-check
7. Flag where expert judgment overrides the available data, with explicit reasoning

### 5.4 Scoring

| Dimension | Handwritten | Automated | Notes |
|-----------|:-----------:|:---------:|-------|
| Physics depth | 8/10 | 6/10 | Handwritten shows genuine understanding |
| Source rigor | 3/10 | 9/10 | Automated traces every claim |
| TRL assessment | 2/10 | 8/10 | Handwritten has no structured TRL |
| Risk prioritization | 4/10 | 8/10 | Automated ranks and quantifies |
| LCOE model defensibility | 3/10 | 7/10 | Automated parameters are conservative and documented |
| Internal consistency | 3/10 | 7/10 | Handwritten contradicts itself on DEC |
| Documentation quality | 2/10 | 9/10 | Automated is independently auditable |
| Insight density (per line) | 9/10 | 5/10 | Handwritten is concise and opinionated |
| Cross-concept context | 1/10 | 8/10 | Automated draws on 4 prior analyses |
| Completeness | 4/10 | 8/10 | Automated covers more dimensions |
| **Overall** | **3.9/10** | **7.5/10** | |

The overall scores are weighted toward reliability and defensibility — the qualities that matter most for a techno-economic analysis that will inform downstream modeling decisions. On pure physics insight, the handwritten analysis scores higher.

---

## Appendix A: Parameter Comparison Table

| Parameter | Handwritten | Automated | Framework Default | Notes |
|-----------|:-----------:|:---------:|:-----------------:|-------|
| net_electric_mw | 500 | 500 | — | Same |
| availability | 0.85 | 0.85 | 0.85 | Same (DEFAULT) |
| lifetime_yr | 30 | 30 | 30 | Same (DEFAULT) |
| construction_time_yr | 5.0 | 5.0 | 5.0 | Same (DEFAULT) |
| interest_rate | 0.07 | 0.07 | 0.07 | Same (DEFAULT) |
| inflation_rate | 0.02 | 0.02 | 0.02 | Same (DEFAULT) |
| noak | True | True | — | Same |
| R0 / axis_t | 0.0 | 0.0 | — | Same (cylindrical geometry) |
| plasma_t | 1.5 | 1.5 | 1.5 | Same (DEFAULT) |
| **chamber_length** | **20.0** | **70.0** | **?** | **Major divergence — see 3.2** |
| blanket_t | 0.60 | 0.60 | 0.60 | Same |
| ht_shield_t | 0.20 | 0.20 | 0.20 | Same |
| structure_t | 0.15 | 0.15 | 0.15 | Same |
| vessel_t | 0.10 | 0.10 | 0.10 | Same |
| **p_input** | **40.0** | **100.0** | **?** | **Major divergence** |
| mn | 1.1 | 1.1 | 1.1 | Same |
| **eta_th** | **0.50** | **0.40** | **0.40** | **Handwritten is optimistic** |
| eta_p | 0.50 | 0.50 | 0.50 | Same |
| eta_pin | 0.50 | 0.50 | 0.50 | Same |
| **eta_de** | **0.60** | **0.54** | **?** | **Both in plausible range** |
| f_sub | 0.03 | 0.03 | 0.03 | Same |
| **f_dec** | **0.30** | **0.20** | **?** | **Handwritten overstates — see 3.3** |
| **p_coils** | **5.0** | **10.0** | **5.0** | Automated elevated with rationale |
| **p_cool** | **20.0** | **25.0** | **20.0** | Automated elevated for 70m cooling |
| p_pump | 1.5 | 2.0 | — | Minor difference |
| **p_trit** | **10.0** | **12.0** | **10.0** | Automated elevated for exhaust mgmt |
| p_house | 4.0 | 5.0 | — | Minor difference |
| **p_cryo** | **1.0** | **2.0** | **1.0** | Automated elevated for larger magnets |
| **CAS21 override** | **$250M** | **None** | **$592M** | **Handwritten unjustified** |

## Appendix B: Qualitative Content Unique to Each Analysis

### Unique to Handwritten
- Centrifugal end plugging: concentric electrodes (TAE, Realta), central electrode (Terra Fusion)
- Ponderomotive end plugging: off-resonance RF wave repulsion, rotation + static perturbation
- Non-axisymmetric devices: yin-yang coils, baseball coils, Ioffe bars
- Alpha channeling as ash removal mechanism
- LCOE saturation at ~600 MWe (from MARS/MINIMARS)
- Hot-cell operations as a practical mirror challenge
- NBI aiming angle importance for confinement
- ECRH causing faster electron depletion risk
- Back-solve analysis showing DT mirror floor at ~2.70 ¢/kWh

### Unique to Automated
- WHAM first plasma date (July 2024) and magnet records (17 T in-bore, >20 T on-conductor)
- $50M REBCO tape cost for WHAM++ as cost proxy
- $9.5M SVB facility funding (February 2026)
- Anvil device purpose and status
- DCLC stability as a ranked economic risk with Q degradation estimate
- Tritium supply chain quantification ($35,000/g, 25-30 kg global inventory)
- Li-6 enrichment geographic concentration (Russia, China)
- Cross-concept comparison with tokamak, FRC, and MagLIF analyses
- "What Would Change My Mind" section with 3 specific developments
- 12-item data gap inventory with criticality ratings
- Confidence rating (Low) with explicit uncertainty ranges per parameter
