---
ID: 11-magnetic-mirror
Concept: Magnetic Mirror (D-T)
Company: Realta Fusion
Type: synthesis
Status: approved
Created: 2026-03-22
Approved-Date: 2026-03-22
Stale: true
Stale-Reason: analysis-rewritten-by-force
---

# Synthesis: Magnetic Mirror (D-T) — Realta Fusion

---

## 1. Executive Summary

- **Most important risk**: End-plug confinement is experimentally undemonstrated. WHAM proved simple mirror operation with HTS magnets; Anvil (the device to demonstrate tandem end-plug sustainment) has not been built. The Q > 5 thesis is simulation-only. This is not a refinement risk — it is a concept-validity gate. If end-plug confinement at HTS-enabled mirror ratios of 10+ does not perform as modeled, the commercial premise collapses entirely.

- **Most important advantage**: Linear center-cell scaling decouples commercial fusion power from end-plug hardware cost. At ~7 MWt/m, lengthening the center cell from 50m (Q > 5) toward 70m (Q ~ 8–10) adds power without additional end-plug R&D. If the physics works, the primary capital marginal is weak solenoid coils and building volume — not precision high-field magnets. This is a structurally different scaling thesis from every tokamak concept in this analysis.

- **LCOE ballpark**: **135.2 $/MWh (13.52 ¢/kWh)** from the 1costingfe model at NOAK, 500 MWe, 85% availability. Overnight capital: **$9,620/kW**, total capital $4.81B. This is not a competitive commercial LCOE. New nuclear (AP1000) runs $80–120/MWh at favorable financing; natural gas combined cycle is $40–70/MWh. To reach $80/MWh, the model would need roughly a 40% capital cost reduction from the baseline — which is not achievable through sensitivity levers alone given the dominant building and reactor plant equipment costs. The LCOE is best interpreted as an order-of-magnitude anchor for a concept this early.

- **Confidence verdict: Low.** Almost every parameter is either DEFAULT (no concept-specific data) or UNCERTAIN (inference from historical proxy). The physics basis is simulation-only. No independent TEA exists. The model's primary value is structural — it shows what drives cost and what levers matter — not as a precise LCOE estimate.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity elasticity from the 1costingfe model, supplemented with qualitative judgment for risks the model cannot capture.

### 1. Availability — elasticity: –0.88

**Assumed value**: 85% (DEFAULT; no Realta target published).
**Sensitivity**: The strongest single lever in the model. Dropping from 85% to 60% availability raises LCOE by ~21% (to ~$163/MWh). A drop to 50% pushes LCOE above $175/MWh.
**What flips the economics**: Unlike pulsed concepts where availability maps to rep rate, a mirror's availability is governed by maintenance access and component lifetimes. The open-ended linear geometry is a genuine maintenance advantage — technicians can access the center cell directly from the ends rather than through complex remote handling. But no maintenance schedule, first-wall replacement cycle, or blanket module lifetime estimate exists for Hammir. If the venetian-blind DEC collectors degrade under ion bombardment (no lifetime data exists), unplanned downtime could be a dominant failure mode. The assumption that a first-of-kind 70m device can achieve 85% availability is optimistic without a credible maintenance plan.

### 2. Interest Rate — elasticity: +0.62

**Assumed value**: 7% real.
**Sensitivity**: At 10% interest, LCOE increases ~18% to ~$159/MWh. At 5%, decreases ~12% to ~$119/MWh.
**What flips the economics**: At $9,620/kW overnight, interest during construction ($628M at baseline) is a large absolute cost. A project finance rate above 10% — realistic for a first-of-kind concept without an operating precedent — pushes LCOE further from commercial viability. The 5-year construction time assumption (DEFAULT) is relatively favorable; any slip to 7+ years would compound this.

### 3. Chamber Length — elasticity: +0.30

**Assumed value**: 70m (UNCERTAIN; extrapolated from 50m Q > 5 simulation result).
**Sensitivity**: A 10% reduction in chamber length (to 63m) reduces LCOE by ~3% — modest. A 10% increase (to 77m) raises LCOE by ~3%. The sensitivity here captures building and structure scaling costs but misses the physics interaction: shorter chamber means lower Q means higher recirculating power fraction means worse economics. The true sensitivity of LCOE to chamber length includes both the direct capital cost term (modeled) and the physics performance term (not independently modeled).
**What flips the economics**: If the commercial Q target requires more than 90–100m of center cell (e.g., if DCLC-driven transport is worse than modeled), the building cost becomes dominant — CAS21 is already $592M at 70m. The "input power stays constant as cell lengthens" thesis is the key assumption; if end-plug power requirements scale with center-cell length, the favorable scaling breaks down.

### 4. Construction Time — elasticity: +0.25

**Assumed value**: 5 years (DEFAULT for mirror geometry; reflects simpler linear assembly vs. toroidal).
**Sensitivity**: Each additional year of construction adds ~10% to IDC (IDC = $628M at baseline). At 7 years, LCOE increases by ~5% (~$7/MWh).
**What flips the economics**: The linear geometry plausibly supports shorter construction than a tokamak. However, a 70m linear reactor is a novel first-of-kind civil structure. No mirror device larger than MFTF-B (historically canceled before operation) has been completed. Regulatory uncertainty for open linear geometry (see Section 3) could add years to licensing. This lever matters but is not primary.

### 5. Thermal Efficiency — elasticity: –0.19

**Assumed value**: η_th = 0.40 (UNCERTAIN; MARS 1983 baseline was ~36%; modern steam or sCO₂ could reach 40–45%).
**Sensitivity**: A drop from 0.40 to 0.35 raises LCOE by ~2.4% to ~$138/MWh. An improvement to 0.45 (optimistic sCO₂) reduces LCOE by ~2.4%.
**What flips the economics**: Thermal efficiency is not a concept-differentiating lever here — this is a D-T thermal plant, and efficiency is governed by heat source temperature and cycle choice. The DEC system (η_de = 0.54) applies only to the ~20% of fusion power in escaping alphas, providing a modest Q boost (Q_eng = 2.8 vs. ~2.5 without DEC). DEC does not change the economic character of the concept the way it does for aneutronic fuels — it is an incremental benefit, not a structural one.

---

## 3. Risk Verdicts

**Challenge 1: End-Plug Tandem Mirror Confinement Is Undemonstrated.**
**Verdict: Genuinely uncertain — and concept-gating.**
**Rationale**: WHAM validated simple mirror confinement with HTS; Anvil will test tandem end-plug sustainment; Hammir requires the full tandem configuration to produce gain. Each step is a distinct physics experiment. The Q > 5 simulation is sound in methodology (POPCON with ML optimization), but unvalidated confinement assumptions at HTS mirror ratios of 10+ could easily result in Q = 1–3 rather than Q > 5. This is not a component integration risk — it is the primary physics risk.
**What would retire this risk**: Anvil operating and demonstrating stable end-plug sustainment with measured electrostatic potential sufficient to suppress loss-cone losses at mirror ratio 10+. A measured confinement time within 2× of POPCON predictions would be sufficient to anchor commercial Q projections.

**Challenge 2: Direct Energy Conversion Efficiency and Capital Cost Are Undefined.**
**Verdict: Genuinely uncertain — but economically secondary for D-T.**
**Rationale**: The DEC contribution to Qe is modest: 54% efficiency on 20% of fusion energy recovers ~11% of fusion power from DEC. This is real but not structural. The venetian-blind design is TRL 2–3 with no prototype — both efficiency and capital cost are genuinely unknown. However, even if DEC underperforms significantly (say, 30% efficiency instead of 54%), the LCOE impact is modest (~1.2% per 10% change in η_de, elasticity = –0.012). DEC matters more for achieving Qe > 1 at the Hammir pilot scale than for commercial LCOE.
**What would retire this risk**: A small-scale prototype of the venetian-blind collector demonstrating measured efficiency and ion bombardment lifetime. Even a 1–10 kW laboratory demonstration would anchor the efficiency assumption.

**Challenge 3: Linear Center-Cell Scaling Cost Is Uncharacterized.**
**Verdict: Genuinely uncertain — the most under-analyzed economic risk.**
**Rationale**: Realta's economic thesis depends on the marginal cost per meter of center cell being dominated by cheap solenoid magnets — not on the total footprint cost. The model shows CAS21 (Buildings) at $592M for a 70m plant. This is not the solenoid cost; it is the building, shielding, vacuum vessel, and structure cost — all of which scale roughly linearly with length. The "constant input power" claim holds for heating; it does not hold for capital. The cost-per-meter breakdown between magnets, structure, blanket, shielding, and vacuum vessel is unknown.
**What would retire this risk**: A pre-conceptual design study (the Hammir paper, expected 2026) with cost-per-meter breakdown of the center cell and a sensitivity study on commercial chamber length.

**Challenge 4: DCLC and MHD Instability at Full Scale.**
**Verdict: Genuinely uncertain — historically fatal, now theoretically managed.**
**Rationale**: DCLC was the dominant failure mode of 1980s mirror machines. Realta's solution (ML-optimized sloshing ions + vortex flow stabilization) is theoretically sound but undemonstrated at HTS mirror ratios. If DCLC suppression works as modeled, this risk retires entirely. If it doesn't, the effective Q is reduced by some factor — potentially 2× or more — which would manifest as either a longer required chamber or higher p_input, both of which raise LCOE substantially.
**What would retire this risk**: Anvil data showing anomalous transport is within a factor of 2 of classical predictions under tandem mirror conditions.

**Challenge 5: Regulatory Pathway for Linear Open Geometry.**
**Verdict: Likely resolvable — but timeline-extending.**
**Rationale**: The NRC's 2023 10 CFR Part 30 framework is favorable in principle. The specific questions (open plasma exhaust, tritium in expander region, end-plug discharge management) are novel but addressable through the existing hazard analysis framework. Unlike the physics risks, this is an institutional process, not a fundamental barrier.
**What would retire this risk**: DOE or NRC pre-application engagement with Realta, or NRC issuing conceptual design criteria for open-geometry magnetic confinement systems.

---

## 4. Structural Advantages and Disadvantages

**Compared against a conventional D-T HTS tokamak (01-hts-compact-tokamak) baseline at ~$5,000–$9,000/kW overnight.**

### Claimed Advantages

| Item | Assessment | Magnitude | Confidence |
|---|---|---|---|
| Simpler magnet geometry (axisymmetric solenoids vs. 3D TF coils) | Real advantage in winding complexity and coil stress analysis | ~5–15% reduction in magnet cost | Medium |
| Steady-state operation (no disruption risk) | Real advantage — no emergency shutdown systems for sudden termination of plasma current | Minor (disruptions are manageable, not capital-dominant) | High |
| Linear center-cell scaling for power increase | Real advantage IF cost-per-meter is truly dominated by cheap solenoids | Unknown magnitude | Low |
| Direct maintenance access to center cell | Real advantage over toroidal geometry for first-wall/blanket replacement | Unknown magnitude — no remote-handling tooling designed | Low |
| DEC reduces Q threshold for net electricity | Real but modest for D-T (20% of fusion energy capturable) | ~5–10% improvement in effective Q_eng | Medium |

### Structural Disadvantages vs. D-T Tokamak

| Item | Cost Premium | Confidence |
|---|---|---|
| Large buildings for 70m linear device (CAS21 = $592M) | +$200–$400M vs. equivalent-power tokamak building | Medium |
| NBI+ECH for end-plug sustainment adds recirculating load (~36% circ. fraction) | Contributes to high overnight cost | Medium |
| DEC capital cost uncharacterized (venetian-blind TRL 2–3) | Unknown positive or negative | Low |
| Tritium breeding blanket retained in full (Li unspecified) | Same as D-T tokamak — not eliminated | Cost-equivalent |
| 14 MeV neutron shielding retained in full | Same as D-T tokamak — not eliminated | Cost-equivalent |
| No thermal cycle elimination (η_th = 0.40, Rankine/sCO₂) | Same as D-T tokamak — full steam plant retained | Cost-equivalent |

### Net Assessment

The magnetic mirror does not eliminate the expensive elements of a D-T thermal power plant — it retains the full thermal cycle, tritium breeding blanket, 14 MeV neutron shielding, and REBCO supply chain challenge. At $9,620/kW overnight vs. a competitive D-T HTS tokamak target of $4,000–$6,000/kW, the mirror is not currently cheaper on a per-kW basis. The primary potential advantage — linear scaling at ~$X/m for cheap center-cell extension — remains unquantified and may not be large enough to compensate for the large building and reactor plant equipment costs. **This concept's structural claim rests entirely on the center-cell linear scaling thesis, which has not been costed at any level of detail.**

---

## 5. Cross-Concept Positioning

The magnetic mirror occupies a structurally distinct but economically challenged position in the fusion landscape: **the only MFE concept with a credible linear scaling thesis**, combined with physics that is two device generations from commercial validation.

**Where it sits**: This is a thermal D-T concept with a novel confinement geometry. Its cost structure is closer to the D-T tokamak cluster (01-hts-compact-tokamak, 21-spherical-tokamak-hts) than to concepts that eliminate the thermal cycle (08-frc-w-direct-conversion). The $9,620/kW overnight is above the range of HTS compact tokamak targets ($3,000–$6,000/kW), not below it. This is largely because the linear geometry drives large building costs and the recirculating fraction (36%) is high.

**Closest economic analogs**:
- *01-HTS Compact Tokamak (CFS ARC)*: Similar REBCO supply chain challenge, similar D-T blanket requirements, similar thermal cycle. The tokamak has better-characterized physics (Q = 10 target is closer to demonstrated than mirror Q > 5), but the mirror's axisymmetric geometry genuinely simplifies magnet winding. The mirror's building costs and recirculating fraction are currently worse.
- *Historical MARS Study (1983)*: The most direct precedent. MARS estimated a copper-magnet tandem mirror at ~$3,000–$5,000/kW (1983 dollars, escalated significantly). Realta's HTS end-plug design aims to improve on this by enabling higher mirror ratios and potentially smaller end-plug hardware. The model here ($9,620/kW) is worse than MARS on a capital basis — suggesting that the HTS advantage has not yet materialized in the cost structure at the assumptions available.

**What makes the mirror fundamentally different**:
1. **The only linear-geometry MFE concept** — all tokamaks, stellarators, and FRCs are toroidal or compact; the mirror's 70m footprint is unique and creates both maintenance access advantages and building cost burdens.
2. **The only concept where fusion power scales by adding cheap material (center-cell length)** rather than by improving confinement physics parameters. This is a manufacturing problem, not a physics problem — which is a fundamentally better place to be if the physics works.
3. **The only D-T MFE concept still early enough that the commercial plant design is almost entirely unconstrained** — for better (any design choice is still available) and worse (no design choice has been validated or costed).

---

## 6. Modeling Confidence

**Rating: Low.**

| Parameter | Data Source | Uncertainty Range |
|---|---|---|
| Commercial plant scale (500 MWe) | Analyst assumption; Hammir pilot is only >50 MWe | Factor of ~2 plausible |
| Chamber length (70m) | Extrapolation from 50m Q > 5 simulation | ±30% plausible range |
| Q_plasma (~8–10 at 70m) | Simulation-only, no experimental anchor | Factor of 2–3 uncertainty |
| p_input (100 MW NBI+ECH) | Proprietary; estimated for Q~5 at 70m | Factor of 2 plausible |
| η_th (0.40) | MARS 1983 historical + modern inference | ±10 percentage points |
| η_de (0.54) | MARS 1983 historical proxy; Realta design uncharacterized | Factor of 1.5–2 uncertainty |
| DEC capital cost | No data; framework default used | Completely unconstrained |
| REBCO magnet cost | Only $50M proxy for WHAM++ (pre-commercial device) | Factor of 3–5 for Hammir |
| Availability (85%) | DEFAULT; no Hammir precedent | Factor of ~2 plausible |
| Buildings ($592M) | Framework default for 70m linear geometry | ±40% plausible |

**Dominant source of LCOE uncertainty**: The physics basis. If end-plug confinement achieves Q ~ 3 rather than Q ~ 8, the model would require either a longer chamber (~120m), higher p_input (~300 MW), or both — and LCOE would jump to $200–$250/MWh or higher. None of this can be bounded until Anvil data exists.

**Secondary source**: Capital cost structure. The model uses framework defaults for DEC, REBCO magnets, and center-cell costs. The actual Hammir capital structure could be 30–50% different from these defaults in either direction. The REBCO cost alone (only $50M proxy for WHAM++) could be $300–$600M for Hammir, which would add $600–$1,200/kW to overnight cost if modeled explicitly — a 6–12% LCOE premium.

**The model is best interpreted as a structural lower bound assuming the physics performs as simulated and all framework defaults are roughly correct.** The upper bound is not well-characterized, but $200+ $/MWh is plausible if end-plug physics underperforms or capital costs come in above framework defaults.

---

## 7. What Would Change My Mind

**1. Anvil operating with measured end-plug confinement data.**
This is the single most important near-term development. A measured Q_plasma in the Anvil tandem configuration — even if lower than Hammir projections — would provide the first experimental anchor for the commercial LCOE model. If Anvil achieves classical confinement at mirror ratio 10+, Q > 5 in Hammir becomes defensible. If confinement is anomalous (e.g., 3× above classical rates), the Hammir design requires substantially longer cells or higher input power, raising LCOE by 20–50%. LCOE impact of favorable Anvil data: could compress the LCOE range from $135–$250/MWh to $120–$160/MWh and shift confidence from Low to Medium.

**2. The Hammir pre-conceptual design paper (expected 2026) including cost-per-meter breakdown.**
Realta has publicly committed to publishing the Hammir design paper. If it includes even rough capital cost estimates, CAS-level breakdowns, or blanket type selection, it would replace the model's framework defaults with concept-specific anchors for the three largest cost categories (CAS22 RPE, CAS21 Buildings, REBCO magnet cost). A design paper showing center-cell cost of $5–10M/m (vs. the framework default) would either confirm or undermine the "cheap scaling" thesis. This single publication would do more to constrain the LCOE than any other near-term disclosure.

**3. REBCO tape price declining below $10/m with improved production yields from announced factory expansions.**
Realta's REBCO cost is currently the most opaque major cost item. WHAM++ alone requires $50M in tape. If REBCO commodity pricing drops to $10/m (from current ~$50–100/m) as production scales, the Hammir magnet bill drops by a factor of 5–10 — potentially reducing overnight capital by $500–$1,500/kW and LCOE by $10–$20/MWh. This development (shared across all HTS concepts) would also improve the relative position of the mirror vs. tokamak on capital cost, since the mirror's simpler winding geometry would benefit proportionally more from commodity tape pricing.
