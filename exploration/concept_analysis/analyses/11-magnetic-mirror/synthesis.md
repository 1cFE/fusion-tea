---
ID: 11-magnetic-mirror
Concept: Magnetic Mirror (D-T)
Company: Realta Fusion
Type: synthesis
Status: draft
Created: 2026-03-29
---

# Synthesis: Magnetic Mirror (D-T) — Realta Fusion

---

## 1. Executive Summary

- **Most important risk**: End-plug confinement physics has never been demonstrated at commercial conditions. Realta's entire economic thesis — Q scaling linearly with center-cell length at constant heating cost — collapses if DCLC instability or trapped-particle modes require more end-plug heating than modeled. The Anvil demonstrator (~2028) is the first real test of this physics, and no equivalent device has operated since MFTF-B was mothballed in 1986 without ever demonstrating sustained confinement. If end-plug Q degrades by a factor of 2 from the modeled value, the concept likely cannot achieve net electricity at commercially relevant scale.

- **Most important advantage**: Linear geometry and the claimed cost-invariant Q scaling. A tokamak must grow in all three dimensions to achieve higher Q, driving capital cost up roughly as volume. A magnetic mirror, if the physics holds, grows only in one dimension at roughly constant per-MWe cost for the expensive end-plug hardware. This is structurally different from any toroidal concept — it implies that a 70 m Hammir is not just a scaled-up WHAM but a qualitatively different cost regime. Whether this advantage is real depends entirely on the uncosted center-cell cost-per-meter, but the physics claim is coherent and consistent with the arXiv paper.

- **LCOE ballpark**: **118.6 $/MWh (11.9 ¢/kWh)** from the 1costingfe model at NOAK, 500 MWe, 85% availability, 70 MW input power (conservative). Overnight capital: **8,601 $/kW**. This is a parametric placeholder, not a plant estimate — every major parameter is sourced from 1983 MARS analogues or framework defaults. The arXiv-anchored optimistic case (p_input ~35 MW, consistent with Table 3 of arXiv:2411.06644) would reduce the recirculating power fraction from 30.3% and likely cut LCOE to the 85–100 $/MWh range. The $118.6/MWh central estimate should be treated as an order-of-magnitude upper bound under conservative assumptions; the range is plausibly 80–180 $/MWh given the input uncertainty spread.

- **Confidence verdict: Low.** No plant-level cost data exists for any modern HTS magnetic mirror. Every CAS account is a framework default or MARS analogue. The dominant model uncertainties (input heating power, commercial plant length, blanket type) are all marked "blocking" in the analysis and span 2.5× ranges. This is the least data-anchored model in the analysis pipeline to date.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity elasticity from the model, with qualitative context for parameters the sensitivity sweep cannot capture.

### 1. Availability — elasticity: −0.91

**Assumed value**: 85% (framework default; no Realta target published).
**Sensitivity**: Moving from 85% to 65% availability raises LCOE ~29%, from $119 to ~$154/MWh. At 50% availability (realistic for an early pulsed or novel continuous-plasma system with unresolved DEC electrode survivability), LCOE approaches $200/MWh.
**What flips the economics**: Availability below ~55% pushes the concept above advanced-fission LCOE and makes it economically uninteresting. The DEC electrode survivability problem — thin uncooled electrodes operating continuously in a D-T fusion exhaust stream, with no published lifetime data — is the most likely mechanism for availability degradation that the model cannot capture. A 30% unplanned downtime factor from DEC maintenance alone would eliminate the concept's commercial case.

### 2. Interest Rate — elasticity: +0.64

**Assumed value**: 7% real discount rate.
**Sensitivity**: At 10% (realistic for pre-commercial fusion technology under project finance), LCOE rises ~19% to ~$141/MWh. At 12% (high-risk first-of-a-kind financing), ~$155/MWh.
**What flips the economics**: Project finance rates above ~15% push LCOE above $170/MWh regardless of engineering assumptions. This is a structural feature of the $8,601/kW overnight cost — a high-capital plant is disproportionately sensitive to financing cost. The mirror concept does not have a capital cost advantage over tokamaks (overnight cost is similar or higher), so it does not benefit from reduced interest sensitivity.

### 3. Construction Time — elasticity: +0.26

**Assumed value**: 5 years (framework default; modular linear geometry supports this).
**Sensitivity**: Each additional year adds ~5% to IDC ($561M at baseline). At 8 years, LCOE increases ~$15/MWh.
**What flips the economics**: Not a primary risk vector. The linear geometry is a genuine manufacturing advantage (modular center-cell assembly vs. complex 3D tokamak structure), and 5 years is defensible. This is the one engineering parameter where the model's assumption is on solid footing.

### 4. Center Cell Length — elasticity: +0.22

**Assumed value**: 70 m (extrapolated from arXiv 50 m pilot scaling; commercial length not published).
**Sensitivity**: Elasticity +0.22 means a 50% increase in length raises LCOE ~11%. But this elasticity does not capture the full picture: longer length also adds fusion power at ~7 MW/m, improving Q and potentially reducing the recirculating fraction. The net LCOE impact of length changes depends on whether heating power stays constant (as Realta claims) or grows with length.
**What flips the economics**: If the cost-invariant Q scaling breaks down — if the center cell at 70 m costs significantly more per meter than at 50 m due to building length, solenoid coil count, or blanket complexity — the economic thesis fails without the LCOE numbers obviously signaling it. This is a gap that only the uncosted center-cell cost structure can resolve.

### 5. Thermal Efficiency — elasticity: −0.15

**Assumed value**: η_th = 0.38 (MARS 1983 steam Rankine achieved ~36%; 0.38 reflects modest improvement).
**Sensitivity**: Moving to sCO₂ at 42% would reduce LCOE by ~6%, ~$7/MWh. MARS baseline at 36% would raise it by ~3%.
**What flips the economics**: Not a concept-altering parameter on its own. But combined with input power uncertainty and DEC uncertainty, it can shift the concept from marginally viable to clearly uncompetitive. At 36% thermal efficiency, 70 MW input power, and 85% availability, LCOE is approximately $125/MWh — already above most fusion and advanced-fission targets. This is why blanket/thermal-cycle selection matters despite its modest individual elasticity.

---

## 3. Risk Verdicts

### Challenge 1: End-Plug Confinement Physics (electrostatic plugging at commercial Q)

**Verdict: Genuinely uncertain — but the timeline is slow.**
**Rationale**: The DCLC instability that destroyed earlier tandem mirror programs (TMX, MFTF-B) was managed in 1980s experiments only through complex plasma shaping that degraded mirror ratio. Realta's HTS axisymmetric approach at mirror ratio 10+ is a genuinely new configuration, and the arXiv paper demonstrates that ML-optimized designs can achieve Q = 5.8 at 50 m in simulation. But simulation is not demonstration. The WHAM experiment (operational July 2024) validates the magnet geometry and basic plasma operation — it does not demonstrate stable end-plug confinement at commercial Q. Anvil, the end-plug demonstrator, has not been built and is planned for ~2028.
**What would retire this risk**: Anvil demonstrating stable end-plug confinement at the density and temperature required for Q > 3 in a main cell with D-T-relevant particle sources. This is a binary outcome — either the physics holds and the concept becomes credible, or it doesn't and the concept joins TMX in history. Expected data: 2029–2031.

### Challenge 2: Commercial Plant Scale and Input Power Unknown

**Verdict: Likely resolvable with the 2026 design paper — but currently blocking.**
**Rationale**: The two prior models produced LCOE estimates of 80.2 and 135.2 $/MWh using 40 MW and 100 MW input power respectively — a 69% spread from a single unknown parameter. This is not a physics uncertainty; it is a proprietary disclosure problem. Realta is expected to publish a Hammir pre-conceptual design paper in 2026 that should specify commercial plant parameters.
**What would retire this risk**: The Hammir pre-conceptual design paper, if it discloses input heating power, commercial plant length, and net electric output target. This is the single near-term disclosure that would reduce LCOE uncertainty by ~50%.

### Challenge 3: Recirculating Power Fraction Couples to End-Plug Risk

**Verdict: Genuinely uncertain — cannot be de-risked without Anvil data.**
**Rationale**: At the modeled 70 MW input, the recirculating fraction is 30.3% and Q_eng = 3.3, which is physically coherent. But if DCLC management requires 150 MW input instead of 70 MW, the recirculating fraction rises to ~50%, Q_eng drops below 2, and net electricity at commercial scale becomes marginal. The arXiv-anchored estimate of ~30–40 MW input for the 50 m pilot (derived from Table 3, P_fusion = 175 MW, Q = 5.8) is actually more optimistic than the model's 70 MW — which would put the LCOE below $100/MWh if valid.
**What would retire this risk**: A published power balance for the Hammir pilot that specifies NBI + ECH input power and projected Qe. This is the parameter with the highest leverage on LCOE uncertainty.

### Challenge 4: DEC Contribution Real but Modest for D-T Fuel

**Verdict: Likely resolvable in principle — but electrode survivability is a real risk.**
**Rationale**: The thermodynamic contribution of DEC in D-T is inherently limited. Physics caps the capturable charged-particle fraction at 20% (alpha particles); at η_de = 0.54, DEC contributes at most ~11% of total plant electrical output. Excluding DEC entirely raises LCOE by ~10–15%. That is real but not concept-defining. The harder question is whether venetian blind electrodes survive 30 years of continuous operation in a fusion exhaust stream. No fusion-condition DEC survivability data exists.
**What would retire this risk**: Any fusion-condition DEC lifetime test — even a short-duration experiment demonstrating electrode survival under D-T plasma bombardment. This could be done on WHAM or a dedicated DEC test stand before Hammir.

### Challenge 5: Tritium Breeding Blanket Type Undisclosed

**Verdict: Likely resolvable — but choice materially affects thermal efficiency.**
**Rationale**: Realta confirms a lithium blanket but has not disclosed the type. FLiBe (outlet temp ~700°C, TBR potentially >1.1 with sCO₂ cycle) vs. LiPb (outlet temp ~350°C, MARS historical baseline) drives thermal efficiency from 36% to potentially 45% — a $15–$20/MWh LCOE difference. The cylindrical center-cell geometry is well-suited to modular blanket segments; no fundamental physics barrier exists for any of the candidate blanket types.
**What would retire this risk**: Blanket type disclosure in the 2026 design paper. Until then, the MARS LiPb analogue at η_th = 0.36–0.38 is the conservative assumption.

---

## 4. Structural Advantages and Disadvantages

Compared against the conventional D-T tokamak baseline (CFS ARC-class, 01-hts-compact-tokamak).

### Advantages Over D-T Tokamak

| Item | Estimated Value | Confidence |
|---|---|---|
| No disruption risk (no plasma current) | Vacuum vessel design simplified; no disruption loads on structure; smaller safety margins | Medium — not quantified in any available source |
| Linear geometry modularity | Center-cell assembly in factory segments; 5-year construction plausible vs. 7+ for tokamak | Medium — consistent with linear machine manufacturing |
| Steady-state operation (no pulsing) | No fatigue cycling in structural components; simpler thermal management than pulsed systems | High — inherent to open-ended geometry |
| Lower magnet complexity | Axisymmetric solenoids vs. shaped D-coils or saddle coils; simpler winding, lower fabrication cost per unit tape length | High — solenoid geometry well-understood |
| Small end-plug hardware at commercial Q (if scaling holds) | End-plug hardware cost does not scale with center-cell length — Q growth is "free" | Low — uncosted and undemonstrated at commercial scale |
| DEC hybrid energy capture | Recovers ~11% of fusion energy electrically that would otherwise be waste heat in a pure thermal plant | Medium — MARS demonstrated DEC physics, not Realta venetian-blind design |

### Disadvantages vs. D-T Tokamak

| Item | Estimated Cost Premium | Confidence |
|---|---|---|
| Large building footprint ($545M CAS21) | 70 m linear machine requires ~30–40% more building volume per MWe than compact tokamak | Medium — building scales with length; magnitude uncertain |
| Higher overnight capital ($8,601/kW) | CFS ARC-class targets ~$3,000–5,000/kW; mirror model is $8,601/kW — approximately 2× penalty | Low — both estimates are parametric; comparison directionally valid |
| DEC electrode replacement cost | No data; thin uncooled electrodes in continuous fusion flux require periodic replacement with hot-cell access at machine ends | Low — purely speculative without lifetime data |
| End-plug heating system (continuous ECH/NBI) | Continuous 70 MW input at ~$1M/MW gyrotron cost = ~$70–100M in heating hardware alone; tokamak pulsed heating is cheaper per kW-installed | Medium — gyrotron costs are documented |
| Remote handling complexity for linear machine | Hot-cell operations along 70 m length with no crane geometry advantage; MARS noted this as a significant maintenance challenge | Medium — qualitative only |

### Net Capital Assessment

The model's $8,601/kW overnight cost is substantially worse than the ARC-class tokamak target and Helion's $1,773/kW. The mirror concept offers structural operational advantages (no disruptions, steady-state, modularity) but does not translate these into capital cost savings under current assumptions. The key unresolved question is whether the center cell's linear scaling thesis, once costed, reveals a cost-per-MWe that drops below the tokamak at large fleet scale — the MARS finding that LCOE saturates around 600 MWe suggests this could be true, but MARS used 1983 technology and the HTS-equivalent cost structure is unknown.

---

## 5. Cross-Concept Positioning

The magnetic mirror occupies a distinct but currently unproven niche: **the only steady-state linear D-T concept with a plausible path to modular scaling**. Its physics is simpler than a tokamak in some respects (no plasma current, no disruptions) and more complex in others (end-plug confinement, open-ended boundary physics). Its current LCOE model is worse than all three concepts previously analyzed in this pipeline.

**Closest economic analog: 01-HTS Compact Tokamak (CFS ARC-class)**
Both concepts are D-T with REBCO HTS magnets and thermal energy conversion. Both depend on the same REBCO supply chain and face the same tritium breeding and Li-6 enrichment constraints. The tokamak has a substantially lower modeled overnight capital and a much more developed physics basis (ARC-class machines have credible peer-reviewed system studies; Hammir does not). The mirror's only defensible structural advantage over the tokamak is the claimed Q-vs-length scaling — if costed, this could favor the mirror at large plant size. At current data availability, the tokamak wins on every metric where data exists.

**Conceptual contrast: 08-FRC w/ Direct Conversion (Helion)**
Both concepts use DEC, but to completely different economic effect. Helion's D-He3 fuel routes ~40% of fusion energy through DEC, enabling a thermal-cycle-free plant at $1,773/kW. Realta's D-T fuel routes only 20% through DEC, contributing ~11% of plant output. The Realta concept is fundamentally a thermal plant that uses DEC as a bonus — Helion is a DEC plant that uses a thermal backup. The mirror's linear geometry is similar to Helion's but the operating physics (steady-state vs. pulsed, open-ended vs. closed compression) and economic structure (high capital vs. low capital) are completely different.

**What makes the magnetic mirror fundamentally different from everything else in this analysis:** It is the only concept with an explicit physics argument that capital cost per MWe decreases as the plant gets larger and achieves higher Q — without increasing the size or cost of the most expensive subsystems. This is the linear Q scaling thesis. It is either the most underappreciated advantage in fusion economics or an uncosted claim that will fall apart when the center-cell cost-per-meter is actually quantified. The Hammir design paper, expected 2026, will be the first real test of this claim.

---

## 6. Modeling Confidence

**Rating: Low.**

| Parameter | Data-Anchored? | Uncertainty |
|---|---|---|
| Input heating power (p_input = 70 MW) | Partially — arXiv Table 3 suggests ~30 MW for 50 m pilot | Factor of ~2.5 range (40–100 MW from prior runs) |
| Commercial plant length (70 m) | No — extrapolated from 50 m pilot | ±30 m plausible; LCOE elasticity +0.22 |
| Thermal efficiency (η_th = 0.38) | Partially — MARS 1983 baseline ~36% | Range 36–45%; LCOE elasticity −0.15 |
| DEC efficiency (η_de = 0.54) | Partially — MARS gridless analogue | Venetian blind ≠ gridless; factor of ~1.5 uncertainty |
| Buildings ($545M CAS21) | No — framework default for linear geometry | Could be 2× if 70 m building is undercosted |
| CAS22 Reactor Plant Equipment ($2,158M) | No — framework defaults throughout | All subsystem costs are placeholders |
| Availability (85%) | No — no Realta target published | 65–85% plausible; elasticity −0.91 |

**Dominant source of LCOE uncertainty**: Input heating power (p_input), because it directly controls Q_plasma, recirculating fraction, and whether the concept produces net electricity at all. The difference between p_input = 35 MW (arXiv-anchored optimistic) and p_input = 100 MW (automated pipeline conservative) is the difference between an LCOE near $85/MWh and one near $160/MWh. No other parameter has this range.

**Secondary source**: Buildings. The 70 m linear machine requires a building roughly 2× the footprint of a compact tokamak. CAS21 at $545M is 13% of total capital — larger than the turbine plant — and is entirely a framework default. If the actual building for a 70 m device at this power level costs $800–$1,000M (plausible for nuclear-licensed facilities), overnight capital rises to $9,000–$10,000/kW.

**The model is best interpreted as a rough upper bound on LCOE, with the range 80–180 $/MWh spanning the defensible input parameter space. Nothing in the model can be called data-anchored. The LCOE output should not be quoted to better than ±50%.**

---

## 7. What Would Change My Mind

**1. Hammir pre-conceptual design paper (expected 2026) disclosing input power and commercial parameters.**
This is the highest-leverage near-term disclosure. If Realta publishes a design paper specifying NBI + ECH input power (~35 MW consistent with arXiv, vs. ~70 MW conservative), commercial plant length, and blanket type, the LCOE uncertainty range collapses from ±50% to ±20–25%. If the arXiv-implied Q of ~7 at 70 m is confirmed with ~35 MW input, the recirculating fraction drops to ~20% and LCOE falls to approximately 85–95 $/MWh — still above competitive targets but within the range where cost reductions from NOAK learning, REBCO price declines, and thermal cycle optimization could plausibly reach 70–80 $/MWh. That would put the concept in the same ballpark as the more optimistic D-T tokamak projections, making the modular scaling advantage potentially decisive.

**2. Anvil end-plug demonstrator results showing stable confinement at Q > 3.**
If Anvil (planned ~2028, results ~2029–2031) demonstrates stable end-plug confinement at commercial Q conditions — specifically, electrostatic potential barriers sustained against DCLC perturbation at the densities and temperatures required for Q > 3 — the concept's physics gating condition is resolved. This would be the most consequential single result in Realta's development timeline. If Anvil fails to achieve stable plugging, the commercial case is over regardless of what the LCOE model says. I would immediately revise the risk verdict on Challenge 1 from "Genuinely uncertain" to "Likely resolved" and the confidence verdict from Low to Medium.

**3. Any peer-reviewed cost or system study for a modern HTS magnetic mirror.**
The current model uses 1983 MARS technology as its cost analogue. If an independent TEA of a modern axisymmetric HTS mirror were published — even a single-author academic study — it would either confirm or refute the framework's cost scaling for this geometry. The absence of any such study is the single biggest gap in the entire analysis. If such a study showed overnight costs below $5,000/kW by virtue of modular linear assembly, linear Q scaling, and HTS coil simplicity, I would revise the concept's LCOE estimate downward by 30–40% and its cross-concept positioning substantially upward. Conversely, if the study showed costs exceeding $10,000/kW due to building footprint, heating system scale, and center-cell complexity, the concept would be economically non-competitive at any Q.
