---
ID: 05-planar-coil-stellarator
Concept: Planar Coil Stellarator
Company: Thea Energy
Type: synthesis
Status: draft
Created: 2026-03-22
---

# Synthesis: Planar Coil Stellarator (Thea Energy — Helios)

---

## 1. Executive Summary

- **Most important risk**: ISS04 H = 1.4 confinement enhancement has never been demonstrated in a quasi-axisymmetric (QA) configuration. The entire Helios design point — 958 MW fusion power, 390 MWe net, 88% availability — rests on this single unvalidated physics assumption. If Eos (2030) measures H_ISS04 = 1.2 rather than 1.4, fusion power drops by 30–50% and the machine must either grow or deliver significantly less electricity. No other concept in this analysis puts as much economic weight on a single number that has never been measured in the relevant geometry.

- **Most important advantage**: Helios is effectively ignited — 1 MW operational ECRH against 958 MW fusion power means zero current-drive recirculating power penalty. This is structurally distinct from every tokamak analyzed here. The model confirms it: Q_eng = 7.7, the highest of any D-T thermal concept analyzed. Current-drive-dependent tokamaks (ARC-class, ST-E1) pay 20–100 MWe in recirculating power even at design-point physics; Helios pays less than 1 MWe for plasma control. Combined with steady-state operation (no disruptions, no pulsed energy storage), this produces a BOP that is simpler and a capacity factor assumption that is structurally more defensible than for pulsed systems.

- **LCOE ballpark**: **155.5 $/MWh** (FOAK, 390 MWe net, 88% availability, $12,695/kW overnight) from the costingfe parametric model. This is within 4% of Thea's own $150/MWh FOAK target — but the proximity is partly coincidental. The model uses ARIES-CS stellarator cost defaults throughout; Thea's 336-coil REBCO magnet system is the largest single capital item and is entirely unmodeled (no published cost account exists). The true FOAK LCOE could be $130–$200/MWh depending on whether the planar coil manufacturing advantage more than offsets the higher coil count and control infrastructure premium vs. conventional stellarators.

- **Confidence verdict: Medium.** Thea Energy has published more engineering detail than any other private stellarator company, and the Helios physics parameters are well-anchored to a real design. But the capital cost structure — particularly the magnet system — is completely uncharacterized in public sources. Medium (not Low) because the physics is data-rich; not High because the cost model is built on defaults.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity elasticity from the costingfe model. All elasticities are %LCOE / %parameter.

### 1. Plant Availability — elasticity: –0.91

**Assumed value**: 88% (stated in arXiv:2512.08027 §Operations; 84-day biennial maintenance cycle).
**Sensitivity**: Dropping from 88% to 75% availability raises LCOE by approximately 15% — from $155.5 to ~$179/MWh. A drop to 65% pushes LCOE above $200/MWh. Moving the other direction: if the sector-maintenance concept works and availability reaches 92%, LCOE drops to ~$148/MWh — within Thea's target.
**What flips the economics**: The 324-coil shaping array introduces novel failure modes that don't exist in conventional stellarators. If the mean time between failures (MTBF) for individually addressed power supply circuits is shorter than the control system can compensate, unplanned plasma terminations will erode the 88% assumption. The divertor is the second concern: a novel QA X-point divertor with no experimental hardware precedent could underperform on impurity compression, requiring additional plasma interruptions. The 88% figure is stated without a published availability model — this is the single number most likely to be wrong, and it has the largest LCOE elasticity.

### 2. Interest Rate — elasticity: +0.81

**Assumed value**: 7% nominal (standard LCOE financial assumption; no Thea-specific financing disclosed).
**Sensitivity**: At 10% interest (realistic for FOAK first-of-kind technology without commercial precedent), LCOE increases by approximately 24% — from $155.5 to ~$193/MWh. At 5% (achievable with government-backed financing), LCOE drops to ~$131/MWh.
**What flips the economics**: IDC (interest during construction) is already $1,090M at 7% — 22% of total capital. At 8-year FOAK construction and 10% interest, IDC alone exceeds $1,400M and overnight cost scales accordingly. This is Helios's structural vulnerability: $12,695/kW overnight is high, and every percentage point of financing cost matters. A public utility or government co-investment structure (reducing effective interest rate to 5–6%) could bring LCOE below $140/MWh without touching any technical parameter.

### 3. Construction Time — elasticity: +0.42

**Assumed value**: 8 years (framework default; no Thea-published construction timeline).
**Sensitivity**: Each additional year of construction adds ~5% to LCOE through compounding IDC. At 10 years (credible for a FOAK stellarator with novel subsystems), LCOE rises to ~$168/MWh. At 12 years (pessimistic but not implausible), LCOE reaches ~$181/MWh.
**What flips the economics**: ITER's construction time has run roughly 2× its original schedule. Helios has more novel subsystems than ITER (QA X-point divertor, 324-coil control infrastructure, sector-based maintenance) and less experimental precedent. An 8-year assumption for a first-of-kind stellarator is optimistic. If construction runs 12 years, construction time and interest rate together add approximately $40/MWh above baseline — and the LCOE target of $150/MWh becomes unreachable without significant financing support.

### 4. Machine Scale / Major Radius — elasticity: +0.20 (correlated with plasma_t, elon)

**Assumed value**: R0 = 8.0 m (directly from Helios preconceptual design; highly confident).
**Sensitivity**: A 10% increase in R0 raises LCOE by approximately 2% (~$3/MWh) through increased reactor plant equipment and building costs. This understates the true sensitivity because R0 is a design-point choice driven by ISS04 scaling: if H_ISS04 comes in at 1.2, Thea would need to grow the machine to approximately R0 = 9–10 m to maintain the same fusion power. At R0 = 10m, direct capital scales roughly as R^2.5 in volumetric estimates — a 30–45% increase in magnet and blanket cost, adding $20–40/MWh to LCOE.
**What flips the economics**: The H_ISS04 risk (Section 3, Challenge 1) and the machine scale risk are coupled. If the physics validation forces a larger machine, the entire capital structure grows nonlinearly. The 8m design point is where Helios's economics look defensible; at 10m, it starts to look like DEMO.

### 5. Thermal Efficiency — elasticity: –0.15

**Assumed value**: η_th = 0.40 (40.2% gross; from three-stage steam Rankine at 635°C, directly from Helios arXiv:2512.08027 §Energy Conversion). Already below the framework default of 0.46.
**Sensitivity**: A 2 percentage-point improvement in thermal efficiency (η_th = 0.42 — achievable with sCO₂ at the same temperature) would reduce LCOE by ~$4/MWh. The current value is conservative and anchored to the helium-cooled primary loop, which introduces heat exchange losses that a water-cooled primary would avoid.
**What flips the economics**: Thermal efficiency is not a first-order driver for Helios — the machine is ignited, so reducing recirculating power from ECRH has near-zero marginal value. The thermal cycle governs gross-to-net conversion on the power plant side. It matters, but it is not in the same league as availability or financing.

---

## 3. Risk Verdicts

**Challenge 1: ISS04 H = 1.4 Confinement Enhancement in QA Geometry**
**Verdict: Genuinely uncertain — and concept-gating.**
**Rationale**: W7-X has achieved H_ISS04 ≈ 1.3–1.4 in the quasi-isodynamic (QI) configuration. QA stellarators are predicted by neoclassical theory to have superior transport (more tokamak-like), which is favorable — but no QA stellarator of any significant size has ever been operated. The claim that QA transport is better than QI is theoretical. The Helios design requires H_ISS04 = 1.4 *sustained*, not peak, in a configuration geometry that has zero experimental basis.
**What would retire this risk**: Eos achieving H_ISS04 ≥ 1.3 in sustained D-D operation (2030+). A measurement within 10% of the Helios design value would confirm the physics pathway; a measurement of 1.2 or below would require either machine redesign or a revised commercial target.

**Challenge 2: Novel QA X-Point Divertor — TRL 1–2**
**Verdict: Unlikely to be resolved before Eos operates.**
**Rationale**: This is the largest hardware gap in the Helios design with no experimental validation path before 2030. The claimed 10× neutral compression advantage over island divertors is simulation-only. Helium impingement jet cooling of 51,000 tungsten tiles at 10 MW/m² in a QA magnetic geometry has no test data from any device. The combination of novel divertor physics + novel cooling architecture + novel scrape-off layer conditions means the design uncertainty is compounded.
**What would retire this risk**: Any hardware demonstration of a QA stellarator divertor — even a partial, reduced-scale test of the helium impingement cooling system at representative heat flux and magnetic field. An Eos device that includes the X-point divertor geometry (not just a simple island divertor fallback) would be the critical milestone.

**Challenge 3: 6.6% Alpha Particle Loss**
**Verdict: Likely resolvable — a managed design constraint, not a showstopper.**
**Rationale**: At 958 MW fusion power, 6.6% alpha loss deposits ~12.7 MW on first-wall and divertor surfaces beyond the design thermal load. This is higher than tokamak values (2–4%) but is incorporated into the Helios first-wall material (V-4Cr-4Ti) specification and the 15-year replacement schedule. The ASCOT5 simulations that produced this number are the same codes used to characterize tokamak fast-ion losses, giving reasonable confidence in the methodology. This is a nuisance cost, not a concept-threatening issue.
**What would retire this risk**: Eos fast-ion loss measurements showing the ASCOT5 prediction is accurate to within ±30%. If actual alpha loss is 3–4% rather than 6.6%, first-wall lifetime could extend significantly beyond 15 years, improving O&M economics.

**Challenge 4: 324-Coil Software-Controlled Array at Plant Scale**
**Verdict: Genuinely uncertain — novel failure mode, no plant-scale reliability analysis.**
**Rationale**: Canis validated 9-coil field control to <1% error. Scaling to 324 coils with 450+ independent control variables in a burning plasma is not a validated extrapolation — it is a qualitatively different engineering regime. There is no published MTBF analysis for the power supply electronics serving each shaping coil. If even a small fraction of circuits fail simultaneously or unexpectedly, field error could trigger plasma termination. The Canis result is genuinely promising, but 9 → 324 is not an incremental demonstration.
**What would retire this risk**: Eos field control data from the full coil complement (Eos will have its own shaping array), demonstrating sustained plasma operation without field-error-induced terminations over hundreds of operational hours. An MTBF model for Helios coil circuits derived from commercial HTS power electronics reliability data.

**Challenge 5: Capital Cost Structure — No Bottom-Up Cost Account Published**
**Verdict: Unlikely to fully resolve before Helios CDR, which is a decade away.**
**Rationale**: Thea's $150/MWh FOAK target is asserted without a supporting cost model. The costingfe model produces $155.5/MWh using ARIES-CS defaults — but those defaults were calibrated to conventional 3D stellarator coils, not a 336-coil REBCO planar array. The net cost impact of planar manufacturing (simpler per coil, but ×13 more coils than a large tokamak) is genuinely unknown. The model could be underestimating capital cost by 20–40% if the magnet system costs significantly above the parametric default — or overestimating it if planar manufacturing yields real economies that ARIES-CS doesn't capture.
**What would retire this risk**: A Thea Energy capital cost account at the CAS level (even a rough order-of-magnitude estimate) with a line item for the magnet system. Any disclosure — investor presentation, DOE report, peer-reviewed cost study — would materially improve model confidence.

**Challenge 6: V-4Cr-4Ti First Wall at Scale**
**Verdict: Genuinely uncertain, but not concept-blocking before 2040.**
**Rationale**: V-4Cr-4Ti is the most supply-chain-limited material in the Helios design, with no production history at multi-hundred-tonne plant scale. However, this constraint doesn't bite until Helios actually needs to procure material — probably late 2030s at earliest. Nuclear-grade vanadium alloy pricing and production scale are unknowns, but the global vanadium industry is large enough that nuclear-grade production could be ramped with sufficient lead time and capital investment.
**What would retire this risk**: A DOE or EU fusion materials program procurement study for V-4Cr-4Ti at power plant quantities, including a price-quantity curve.

---

## 4. Structural Advantages and Disadvantages

Compared against a conventional D-T HTS compact tokamak (CFS ARC-class; 01-hts-compact-tokamak baseline at ~$3,000–$6,000/kW overnight, current-drive dependent).

### Eliminated or Reduced Cost Categories

| Item | Magnitude | Confidence |
|---|---|---|
| Current-drive recirculating power (20–100 MWe in tokamaks → 1 MWe in Helios) | Saves ~20–100 MWe of ECRH/LHCD auxiliary load; at η_pin = 0.5 wall-plug efficiency, saves ~40–200 MWe equivalent in power supply infrastructure | High |
| Disruption-mitigation systems (MGI, halo current limiters, RE suppression) | Minor capital saving (~$20–50M); eliminates disruption-induced first-wall replacement premium | High |
| Pulsed energy storage / flywheel (required for pulsed tokamak variants) | Not applicable to Helios (steady-state); eliminates ~$30–80M BOP item | High |
| Complex current-profile control actuators (lower hybrid, NBCD, ECCD systems beyond startup) | Startup ECRH system only (10 MW); operational system is 1 MW; saves $50–$100M in CD hardware vs. pulsed tokamak | Medium |

### Added or Amplified Cost Categories

| Item | Magnitude | Confidence |
|---|---|---|
| Larger machine footprint (R=8m vs. ARC R=3.3m) → larger buildings, more structural material | CAS21 Buildings = $374.8M; expected ~$150–$200M more than an equivalent-power ARC-class tokamak of same net output | Medium |
| Higher coil count HTS magnet system (336 coils vs. ~25 for large tokamak) → more cryo infrastructure and power electronics | p_cryo = 15 MW (336 REBCO coils at 20K); adds ~$30–50M cryo system premium over fewer-coil design | Medium |
| Novel control infrastructure for 450+ independent coil channels | Unquantified; likely $20–60M in software/control hardware beyond conventional stellarator scope | Low |
| QA X-point divertor (TRL 1–2; no hardware analogue) | Unquantified R&D premium at Eos; cost uses framework default for Helios but TRL gap introduces validation risk that conventional tokamak divertors do not have | Low |
| V-4Cr-4Ti first wall (specialty material, limited supply) | Unknown premium over EUROFER97 or tungsten alternatives; potentially $50–150M above baseline | Low |

### Net Assessment

Helios's structural advantages are real and concentrated in the power balance: Q_eng = 7.7 is genuinely superior to current-drive-dependent tokamaks at comparable power scales (typically Q_eng = 3–6). This translates directly to lower recirculating fraction (11% vs. 20–30% for driven tokamaks) and higher net electricity per unit of fusion power. However, these advantages do not overcome the larger machine size. At $12,695/kW overnight, Helios is currently above the $3,000–$6,000/kW range targeted by HTS compact tokamaks — though those targets are themselves speculative for FOAK plants. The competitive advantage Helios claims over tokamaks is real in physics; it has not yet been demonstrated in capital cost structure.

The most precise comparison: a stellarator that is truly ignited and steady-state eliminates approximately **$100–$200/kW** in current-drive hardware and recirculating power infrastructure vs. an equivalent pulsed D-T tokamak. Against the total overnight cost of ~$12,700/kW, this is a 1–2% capital advantage — real, but not game-changing. The economic story for Helios is primarily about steady-state operation and availability, not about capital cost reduction relative to tokamaks.

---

## 5. Cross-Concept Positioning

Helios occupies a distinctive position in the MFE landscape: **the most credibly documented private-sector stellarator concept, with the best combination of physics data quality and steady-state operational advantages — but with the largest unmodeled capital cost item of any concept in this analysis.**

**Where it sits in the LCOE landscape:**
- *Magnetic mirror (11, Realta Fusion)*: $135/MWh model, but ~80% of inputs are defaults or speculation. A lower number built on much weaker data. The mirror has a linear scaling thesis that could be transformative; Helios has better-characterized near-term physics but a larger machine. Both have Low-to-Medium modeling confidence.
- *FRC w/ Direct Conversion (08, Helion)*: $50/MWh model (NOAK), but requires direct energy conversion and He3 fuel — fundamentally different cost structure. Not a meaningful comparison for D-T thermal economics.
- *HTS Compact Tokamak (01, CFS ARC)*: $3,000–$6,000/kW overnight targets (NOAK), smaller machine, better-characterized physics in the relevant scaling regime. The tokamak has disruption risk and current-drive cost; Helios eliminates both at the cost of a larger machine and unvalidated QA confinement. The tokamak currently has the better capital cost story; Helios has the better steady-state physics story.

**What makes Helios structurally unique among D-T thermal concepts:**
1. **The only QA stellarator concept with published engineering parameters**. Every other stellarator power plant study (ARIES-CS, HELIAS, etc.) uses conventional 3D-coil geometry. Helios's planar coil approach has no direct predecessor, making the cost comparison inherently uncertain — but also meaning the cost structure is not constrained by 3D coil manufacturing economics.
2. **Highest Q_eng of any D-T thermal concept analyzed** (Q_eng = 7.7 at FOAK, from the model). This is a direct consequence of ignited operation. If this is achievable at commercial scale, Helios delivers more net electricity per unit of invested capital than any current-drive-dependent tokamak at the same fusion power.
3. **DOE-certified preconceptual design**. As the first Milestone-Based program awardee to receive design certification (January 13, 2026), Helios has undergone independent engineering review at a level that no other private stellarator concept has. This is a meaningful quality signal, even if it doesn't validate the physics uncertainties.

**Concepts sharing similar economics:**
EU-DEMO stellarator (HELIAS 5-B class, ~7.75m major radius, 3D helical coils). Helios is approximately the same scale as the HELIAS design but with a fundamentally different coil geometry. The ARIES-CS cost structure analogy is imperfect but reasonable as a structural framework. The key unknown is whether Thea's planar approach genuinely shifts cost from the magnet system to the control software — and whether that trade-off is economic at commercial scale.

---

## 6. Modeling Confidence

**Rating: Medium.**

| Parameter | Data Source | Status | Uncertainty |
|---|---|---|---|
| Geometry (R0=8m, a=1.8m, β=2.7%) | arXiv:2512.08027 directly | Anchored | Low |
| Power balance (1,094 MW thermal, 390 MWe net) | arXiv:2512.08027 directly | Anchored | Low |
| Availability (88%) | arXiv:2512.08027 stated; no supporting model | Stated, unvalidated | Medium |
| Thermal efficiency (η_th = 0.40) | arXiv:2512.08027 (40.2% gross) | Anchored | Low |
| Operational heating (p_input = 1 MW) | arXiv:2512.08027 (Q~958) | Anchored | Low |
| Cryogenic load (p_cryo = 15 MW) | Derived, upper-bound estimate | UNCERTAIN | High |
| Magnet system capital cost | No Thea data; ARIES-CS default | Framework default | Very High |
| Buildings and reactor plant equipment | No Thea data; parametric default | Framework default | High |
| Construction time (8 years) | Framework default; no Thea disclosure | Framework default | High |
| Capital cost breakdown (CAS-level) | No Thea data | Entirely unanchored | Very High |

**How many parameters are data-anchored vs. speculative:**
Physics parameters: ~85% anchored to Helios arXiv. Cost parameters: ~10% anchored (availability and thermal efficiency feed into revenue/power; everything else is a default). The split is unusual — Helios is the most physics-data-rich concept in this batch, but one of the most cost-data-poor.

**Dominant source of LCOE uncertainty**: The magnet system cost. The 336-coil REBCO array at 20T is the largest single capital item for any stellarator, and Thea has published no bottom-up estimate. If the true magnet system cost is 40% above the ARIES-CS parametric default (plausible given higher coil count and HTS premium), LCOE rises to approximately $175–$185/MWh FOAK — materially above Thea's $150/MWh target. If planar manufacturing is genuinely cheaper per coil and the higher count doesn't fully offset this, the model's $155.5/MWh could be conservative.

**The model is best interpreted as a physics-credible LCOE estimate with a placeholder cost structure.** It is more reliable than the magnetic mirror or FRC analyses (better physics anchoring) but less reliable than a concept with a published cost account (which none of them have). Treat the $155.5/MWh as the median of a $120–$220/MWh FOAK range, with the upper end driven by magnet cost uncertainty and the lower end by planar manufacturing optimism.

---

## 7. What Would Change My Mind

**1. Eos confinement results — H_ISS04 measurement in QA configuration (2030+).**
This is the single most important near-term development. If Eos achieves H_ISS04 ≥ 1.3 in sustained plasma operation, the central physics bet is validated: the Helios FOAK LCOE range compresses to approximately $140–$180/MWh and confidence upgrades from Medium to Medium-High. If Eos measures H_ISS04 ≤ 1.1, the Helios design point is broken — either the machine grows (LCOE jumps 25–40%) or fusion power falls below the commercial threshold for 390 MWe net. This single number, measured in a 2030 experiment, will determine whether Helios is a credible commercial concept or a redesign candidate.
*LCOE impact: favorable result narrows range; unfavorable result shifts center estimate up by $30–$60/MWh.*

**2. Thea Energy capital cost disclosure — any CAS-level breakdown of the magnet system.**
An investor presentation, DOE program report, or peer-reviewed cost study that provides even order-of-magnitude estimates for the 336-coil REBCO array would replace the largest uncertainty in the model. If the magnet system is confirmed at less than 25% of overnight capital ($3,175/kW or below), Helios's $150/MWh FOAK target is credible. If it comes in at 40%+ of overnight capital (plausible for an HTS-intensive design at 20T), LCOE could reach $200/MWh FOAK or above. This disclosure matters more than any single physics result for the accuracy of the cost model.
*LCOE impact: could revise the central estimate by ±$30/MWh in either direction.*

**3. First REBCO tape price below $10/kA-m at commercial production volumes.**
REBCO tape is the shared critical material for all HTS-magnet fusion concepts. If commercial HTS production reaches $10/kA-m (from current $30–100/kA-m), the magnet system capital for a 336-coil REBCO array drops by 3–10× — potentially removing $500–1,500/kW from overnight cost and $8–24/MWh from LCOE. This development (shared with all HTS tokamak concepts) would shift the competitive positioning of Helios meaningfully: at $10/kA-m, higher coil count becomes less of a capital penalty, and the steady-state + ignited physics advantages start to dominate the economic comparison. This is the most plausible single external development that could move the LCOE to $120/MWh FOAK range.
*LCOE impact: if achieved before Helios CDR, potentially $8–24/MWh reduction from baseline.*
