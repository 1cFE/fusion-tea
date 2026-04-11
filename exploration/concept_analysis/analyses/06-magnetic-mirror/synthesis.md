---
ID: 06-magnetic-mirror
Concept: Magnetic Mirror (p-B11)
Company: Pale Blue Fusion
Type: synthesis
Status: draft
Created: 2026-03-22
---

# Synthesis: Magnetic Mirror (p-B11) — Pale Blue Fusion (CHARM)

---

## 1. Executive Summary

- **Most important risk**: p-B11 nonthermal plasma has never been demonstrated in any experiment at any scale. This is not a component-level or integration risk — it is a physics viability gate. If bremsstrahlung losses exceed fusion gain at the nonthermal proton conditions required for CHARM (because alpha channeling efficiency is insufficient, or because the proton distribution thermalizes), the concept cannot produce net energy. There is no hardware demonstration anywhere in the literature that de-risks this constraint. The concept could be physically impossible at acceptable recirculating power fractions.

- **Most important advantage**: The p-B11 fuel cycle structurally eliminates the three most expensive and supply-chain-constrained elements of D-T fusion: tritium breeding blanket (~$516M in CAS22 at D-T mirror scale), lithium enrichment, and 14 MeV neutron shielding. It also eliminates the operating cost burden of tritium handling and remote maintenance of activated components. Combined with a DEC-primary power conversion architecture that bypasses most of the thermal cycle, the cost structure of a working CHARM plant would be fundamentally lighter than any D-T thermal concept — if the physics works.

- **LCOE ballpark**: **63.7 $/MWh (6.37 ¢/kWh)** from the 1costingfe model at NOAK, 500 MWe, 80% availability. Overnight capital: **$4,963/kW**, total capital $2,482M. This number should not be cited as an estimate — every plasma parameter in the model is a placeholder with no experimental anchor. The model's value is structural: it shows that a working CHARM plant could plausibly achieve competitive LCOE (~$60–80/MWh) through its cost structure alone, without requiring unusual financial assumptions. But the physics preconditions for achieving that cost structure are unmet at every level.

- **Confidence verdict: Very Low** (below the "Low" floor applied to other concepts in this analysis). Unlike Realta or Helion, where the LCOE uncertainty is wide but bounded by proxy data and simulation, CHARM's uncertainty is open-ended because the fundamental plasma physics has no experimental anchor. The model is a structural sketch, not a cost estimate. The true LCOE range runs from non-igniting (concept fails) to competitive ($60–80/MWh), and there is currently no basis for choosing a point in that range.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity elasticity from the 1costingfe model, with qualitative adjustment for physics risks the model cannot capture.

### 1. Availability — elasticity: –1.00

**Assumed value**: 80% (slightly below D-T mirror default of 85%; no Pale Blue target published).
**Sensitivity**: The strongest single lever in the model — essentially unit elasticity. Dropping from 80% to 60% availability raises LCOE by ~25%, from $63.7 to ~$80/MWh. A drop to 40% would push LCOE to ~$127/MWh, eliminating the concept's economic advantage.
**What flips the economics**: The open-ended linear geometry may enable simpler maintenance than toroids (direct access to plasma chamber from ends). But this advantage is speculative — no maintenance study, first-wall replacement schedule, or component lifetime estimate exists for CHARM. The relevant failure mode is not first-wall replacement (no neutron damage) but electrode erosion, cryogenic magnet reliability, and DEC collector degradation — none characterized. Steady-state operation is a genuine availability advantage over pulsed concepts, but only if the plasma can sustain continuously, which has never been demonstrated for p-B11 conditions.

### 2. Construction Time — elasticity: +0.29

**Assumed value**: 5 years (DEFAULT for mirror geometry; no Pale Blue estimate).
**Sensitivity**: Each additional year of construction adds ~$65M in IDC (IDC = $324M at baseline). At 7 years, LCOE increases by ~6% (~$4/MWh).
**What flips the economics**: Not a primary lever, but at $4,963/kW overnight, construction time compounds material interest during construction. A 5-year schedule is plausible for the simpler linear geometry versus a tokamak. However, a pre-commercialization concept with no design point and no experimental device has no basis for any construction timeline estimate.

### 3. DEC Fraction (f_dec) — elasticity: –0.08

**Assumed value**: f_dec = 0.85 (fraction of transport power routed to DEC; speculative based on near-aneutronic power balance).
**Sensitivity**: A 10% decrease in f_dec (0.85 → 0.76) raises LCOE by ~0.8%. The elasticity appears modest, but this understates the true structural importance: f_dec governs how much fusion energy bypasses the thermal cycle, which is the mechanism by which CHARM achieves its low cost structure. If the thermal/direct conversion split is unfavorable — e.g., f_dec = 0.50 because synchrotron and bremsstrahlung losses dominate — LCOE would rise significantly and the cost advantage over D-T concepts would erode.
**What flips the economics**: f_dec below ~0.50 would require a substantially larger thermal plant (CAS23 is only $128.7M now because only ~15% of energy goes thermal). A conventional thermal fraction would add $200–$300M to capital and push LCOE toward $80–90/MWh.

### 4. Heating System Efficiency (eta_pin) — elasticity: –0.05; Auxiliary Power (p_input) — elasticity: +0.05

**Assumed value**: eta_pin = 0.60, p_input = 60 MW (RF for alpha channeling ~20 MW + rotation sustainment ~30 MW + misc ~10 MW).
**Sensitivity**: Symmetric at ±0.05 — a 10% change in either raises or lowers LCOE by ~0.5%. Individually modest.
**What flips the economics**: The 60 MW auxiliary power assumption is the model's most consequential unknown. Rotation sustainment power depends on plasma resistivity and rotation energy confinement time — neither is characterized for CHARM. If rotation requires 150–200 MW of auxiliary power (a range consistent with the complete absence of published numbers), the recirculating fraction climbs from 23.2% toward 40–50%, Q_eng falls from 4.3 toward 2, and LCOE rises 15–30%. The sensitivity elasticity formula underestimates this risk because it assumes a small perturbation around a central estimate that itself has no empirical basis.

### 5. DEC Efficiency (eta_de) — elasticity: –0.013

**Assumed value**: eta_de = 0.70 (speculative; above the 54% empirical MARS result; within PRX Energy 2025 physics limits).
**Sensitivity**: Elasticity is low — a 10% decrease in eta_de raises LCOE by only ~0.13%. DEC efficiency is not an LCOE-dominant lever for this concept.
**Why it matters anyway**: DEC efficiency matters most for the power balance closure, not the LCOE sensitivity formula. If eta_de is 0.40 rather than 0.70, the plant cannot close its power balance at the assumed fusion power and p_input — meaning the entire model is internally inconsistent. The right frame for eta_de is binary feasibility (does the power balance close?) rather than continuous sensitivity (how much does LCOE change?).

---

## 3. Risk Verdicts

**Challenge 1: p-B11 Reactivity Deficit and Nonthermal Operation.**
**Verdict: Genuinely uncertain — and concept-gating.**
**Rationale**: Bremsstrahlung losses exceed fusion gain in a thermal p-B11 plasma at any achievable temperature. CHARM's solution (nonthermal proton population maintained by alpha channeling) is analytically motivated but experimentally undemonstrated. The existence of the concept depends on this working. It might — the physics is not obviously wrong — but there is no experimental data to distinguish "plausible but undemonstrated" from "physically achievable."
**What would retire this risk**: A laboratory plasma experiment (not necessarily CHARM-architecture) demonstrating a sustained nonthermal proton energy distribution in a mirror-confined plasma with measureable p-B11 fusion yield above the bremsstrahlung floor. This experiment does not currently exist. CMFX could potentially serve this role if upgraded for higher temperature and p-B11 fueling, but that would require a substantial new experimental program.

**Challenge 2: Alpha Channeling Efficiency.**
**Verdict: Genuinely uncertain — the master lever for concept viability.**
**Rationale**: Alpha channeling efficiency η_α determines whether CHARM achieves net gain. The 6.9× reduction in required confinement time (from the hybrid fast-thermal scheme) is the difference between p-B11 being plausibly achievable and clearly infeasible. This factor is derived from analytical models and has never been measured experimentally — not in CHARM, not in CMFX, and not in any fusion experiment. A 2× reduction in η_α from model estimates could move the concept from net-gain to non-igniting.
**What would retire this risk**: Experimental measurement of alpha channeling efficiency in a rotating plasma with relevant wave parameters. This requires an experiment specifically instrumented for alpha particle trajectory measurement in the presence of ICRF waves — not a trivial upgrade to existing devices. A measured η_α within a factor of 2 of the analytical prediction would substantially anchor the commercial model.

**Challenge 3: Helium Ash Management and Multi-Chamber Architecture.**
**Verdict: Genuinely uncertain — sequentially compounding risk.**
**Rationale**: Five distinct physics mechanisms must function simultaneously for the multi-chamber architecture to work: centrifugal species separation (p vs. B11 mass ratio), ponderomotive barriers as ion traffic controllers, helium migration to the heat exchange chamber, wave-induced ash removal, and continuous stable plasma rotation. Each is individually at TRL 1–2 for CHARM-specific conditions. The compounded probability of all five working without one failure mode dominating is low — not impossibly low, but not predictable from current data.
**What would retire this risk**: A two-chamber experiment (fusion chamber + heat exchange chamber) demonstrating centrifugal species separation and helium migration with a plasma analogous to CHARM conditions (high mass ratio species pair, E×B rotation, relevant temperatures). This is a multi-year experimental program, not an incremental upgrade.

**Challenge 4: Rotation Sustainment Power and Recirculating Fraction.**
**Verdict: Genuinely uncertain — dominates LCOE uncertainty more than the model shows.**
**Rationale**: The model assumes 60 MW of auxiliary power (rotation + RF), giving a 23.2% recirculating fraction. This number is fabricated from reasonable analogies — there is no published power balance for CHARM, no CMFX data on rotation sustainment power at reactor-relevant plasma conditions, and no first-principles estimate that has been independently checked. If sustained rotation requires 150 MW (plausible given the large voltage drops and cross-field transport in a reactor-scale plasma), the recirculating fraction rises to ~40% and Q_eng falls below 2.5, which would push LCOE well above $80/MWh.
**What would retire this risk**: CMFX publishing rotation sustainment power measurements as a function of plasma parameters (density, temperature, rotation velocity). Even at low-temperature D-D conditions, the scaling of electrode power with plasma size and field would provide a first anchor for reactor-scale projections.

**Challenge 5: Direct Energy Conversion Efficiency and Capital Cost.**
**Verdict: Genuinely uncertain — but not concept-gating if power balance closes.**
**Rationale**: Unlike Realta's DEC (where it is economically secondary at D-T), CHARM's DEC is structurally primary — it recovers ~85% of the fusion energy. If DEC efficiency is 40% rather than 70%, the LCOE impact is direct and substantial. However, the physics limits established by Rax, Kolmes, Fisch (PRX Energy 2025) support the 0.70 estimate at the adiabatic limit; the risk is more engineering than physics. Capital cost of the DEC hardware is the more pressing unknown — the model assigns near-zero cost to DEC infrastructure because no published design exists.
**What would retire this risk**: A small-scale prototype of Pale Blue's rotation energy recovery DEC approach demonstrating measured efficiency and capital cost at laboratory scale. The SWDEC patent (US20230298771) provides a starting architecture — the hardware needs to be built and tested.

---

## 4. Structural Advantages and Disadvantages

Compared against the conventional D-T HTS tokamak ($5,000–$9,000/kW overnight) and the D-T mirror (11-magnetic-mirror, $9,620/kW overnight).

### Quantified Advantages vs. D-T Mirror

| Eliminated Item | Cost Impact | Confidence |
|---|---|---|
| Tritium processing (p_trit = 0 MW, no tritium plant) | ~$50M capital + $5–10M/yr O&M | High — fuel cycle is aneutronic by design |
| Breeding blanket (X-ray capture wall only, blanket_unit_cost_pb11 vs. DT blanket) | ~$300–$400M in CAS22 RPE at D-T mirror scale | High — well-characterized in framework |
| 14 MeV neutron shielding (ht_shield_t = 0.10 vs. full D-T shielding) | ~$50M in structure/shielding | High — no neutron flux |
| Remote handling and hot cells (remote_handling_pb11_base = $20M vs. D-T base) | ~$80–$150M reduction | High — no activated components |
| Buildings: no tritium building, no hot cell, no remote handling facility | ~$400M reduction vs. D-T mirror ($200M vs. $592M) | Medium — framework default, no design study |
| Thermal cycle downsizing (DEC primary, CAS23 = $128.7M vs. full steam plant) | ~$100–$200M vs. full D-T thermal plant | Medium — speculative power balance |
| O&M (om_cost_pb11 = $24M/yr vs. D-T active maintenance regime) | $10–$20M/yr operating cost reduction | High — structural consequence of aneutronic fuel |
| Fuel cost (CAS80 = $0.1M/yr; boron is cheap and abundant) | Near-zero vs. $35M+ tritium startup inventory | High — boron is not radioactively controlled |

**Net capital estimate**: $2,482M total capital at 500 MWe vs. $4,810M for D-T mirror at 500 MWe — a ~49% capital cost reduction, driving LCOE from $135 to $63.7/MWh. This is not a marginal optimization; it is a structural cost category elimination.

### Structural Disadvantages vs. D-T Tokamak

| Added Item | Cost Premium | Confidence |
|---|---|---|
| DEC hardware capital (rotation energy recovery — TRL 2–3) | Unknown; modeled at near-zero (no design exists) | Very Low |
| Central electrode system (100 kV, reactor-scale; erosion, contamination) | Modest ($10–30M est.) | Low |
| Alpha channeling RF system (novel geometry, no prototype) | $20–50M est. (generic ICRF antenna cost) | Low |
| Magnet system for multi-chamber architecture (inner + outer coil sets, unspecified conductor) | Comparable to D-T mirror if HTS adopted | Medium |
| Higher bremsstrahlung wall loading on first wall (X-ray flux management) | Minor capital premium | Low |
| p-B11 nonthermal plasma control complexity | Unknown operational cost premium | Very Low |

### Net Assessment

The cost structure of a working CHARM plant is substantially cheaper than any D-T concept in this analysis — not because of engineering refinement but because of fuel cycle physics. The p-B11 aneutronic cycle eliminates ~$600–800M in D-T-specific capital items and ~$50M+/year in operating costs. This is a real structural advantage that cannot be replicated by optimizing a D-T design. However, this advantage is contingent on the physics working — a precondition that is currently unmet at every experimental level. The fuel cycle advantage is large enough that if a 10% probability of success is assigned, the expected LCOE (probability-weighted across success and failure) may still compare favorably to D-T concepts with higher confidence but higher cost structures.

---

## 5. Cross-Concept Positioning

CHARM occupies the most extreme position in the fusion landscape: the **highest-upside, lowest-confidence concept** in this analysis. It is physically distinct from every other MFE or IFE concept analyzed, and its cost structure — if achievable — is competitive with advanced fission and natural gas.

**Closest economic analog: Helion FRC (08-frc-w-direct-conversion)**
Both target aneutronic fuels, both use DEC as the primary energy conversion pathway, and both eliminate the D-T thermal plant cost structure. Helion modeled at $50.3/MWh vs. CHARM at $63.7/MWh — in the same competitive range. The fundamental difference is experimental maturity: Helion has 7 prototype generations and an operating experiment (Polaris); Pale Blue has a research group, 29 papers, and no hardware. The CHARM physics is also harder — p-B11 requires ~9× higher temperatures than D-T vs. D-He3 requiring ~3–4×. If CHARM achieves its physics, it has a slight cost advantage over Helion (boron is cheaper than He3, and the aneutronic suppression is more complete). But CHARM is at least 15–20 years behind Helion experimentally.

**Structural contrast with D-T mirror (11-magnetic-mirror, Realta)**
Realta and Pale Blue share the mirror confinement geometry and (probably) HTS magnet infrastructure. But the D-T mirror retains every expensive D-T element that CHARM eliminates — tritium breeding, neutron shielding, full thermal plant — and its LCOE comes in at $135.2/MWh vs. CHARM's $63.7/MWh. From a pure cost structure perspective, CHARM dominates the D-T mirror if the physics is achievable. The irony: the D-T mirror has a plausible experimental path to validation (WHAM → Anvil → Hammir), while the p-B11 mirror requires an experimental leap that has not yet been attempted.

**Fundamental distinction from all D-T MFE concepts**
CHARM is the only concept in this analysis that eliminates the thermal cycle as a structural matter rather than as an optimization target. Every D-T tokamak, mirror, and stellarator retains a Rankine or sCO₂ cycle as the primary energy extraction mechanism. CHARM treats direct energy conversion as the primary channel and the thermal cycle (bremsstrahlung/synchrotron capture) as the residual. This is qualitatively the same approach as Helion's inductive recovery, but in a steady-state rather than pulsed configuration. The steady-state operation is a genuine availability advantage over Helion's 1 Hz rep-rate requirement.

**Where CHARM sits in the broader landscape**
- Most scientifically ambitious concept analyzed: the highest fuel cycle barrier (p-B11), the most novel confinement architecture (CHARM multi-chamber), the most experimental gaps
- Lowest TRL of any concept analyzed: every distinguishing technical element is at TRL 1–3
- Highest upside if successful: ~$60/MWh LCOE with near-zero fuel cost, no tritium supply chain, and no neutron management infrastructure
- Investment profile: maximum optionality value relative to current investment ($1.5M ARPA-E, no private funding) — if CMFX-scale experiments provide supporting evidence, private funding rounds would be justified; if early experiments show fundamental barriers, capital exposure is minimal

---

## 6. Modeling Confidence

**Rating: Very Low** — the lowest in this analysis series.

| Parameter | Data Source | Uncertainty Range |
|---|---|---|
| Net electric output (500 MWe) | Framework reference scale; no design point | Factor of 2–5 plausible |
| Chamber length (30 m) | Conservative upscale from CMFX (6.7 m); no published reactor point | Factor of 2–3 plausible |
| p_input (60 MW) | Estimated from CMFX electrode power + generic RF; no published power balance | Factor of 3–5 plausible |
| f_dec (0.85) | Theoretical estimate based on near-aneutronic fuel cycle | 0.50–0.90 plausible range |
| eta_de (0.70) | PRX Energy 2025 physics limit; no engineering efficiency data | 0.40–0.75 plausible |
| eta_th (0.20) | Speculative; fraction of power going through thermal cycle | 0.10–0.40 plausible |
| Q_eng (4.3) | Model output from speculative power balance parameters | 1.5–8 plausible (or below 1 if physics fails) |
| Availability (80%) | DEFAULT; no maintenance study | 50–90% plausible |
| Buildings (200 M$) | Manual override; no plant design | ±50% plausible |
| DEC capital | Framework: near-zero (no design) | True cost: $50–300M unknown |
| Magnet system | Generic HTS solenoid; conductor not specified | Factor of 2–3 on C220104 ($353M) |

**Dominant source of LCOE uncertainty**: The physics basis for net gain. If the nonthermal p-B11 plasma cannot be sustained with positive net energy (the bremsstrahlung-to-fusion power ratio remains >1 at achievable plasma conditions), the concept does not produce electricity at any cost. This is not a quantifiable uncertainty — it is a binary outcome that cannot be resolved without a dedicated experimental program. The model's $63.7/MWh estimate is conditioned on the physics working as theorized, which is itself an unvalidated assumption.

**Secondary source**: Rotation sustainment power. The assumed 60 MW of auxiliary power has a plausible range of 20–200 MW with no experimental anchor. At 200 MW, Q_eng falls to ~1.5 and LCOE rises to ~$90–100/MWh. At 200 MW with eta_de = 0.50 (below the PRX Energy physics limit rather than at it), the power balance may not close. The model cannot bracket this uncertainty without published data from Pale Blue or CMFX.

**The model is best interpreted as**: a demonstration that CHARM's cost structure is theoretically competitive if the physics works, not as an LCOE estimate. The number $63.7/MWh is a conditional forecast — it tells you what LCOE to expect if every physics bet resolves favorably, using framework defaults for unspecified engineering parameters. The unconditional LCOE, probability-weighted across the outcome space (including concept failure), is not modelable.

---

## 7. What Would Change My Mind

**1. CMFX (or a successor experiment) publishing rotation sustainment power data as a function of plasma parameters.**
The single most actionable near-term risk retirement is characterizing how much power it costs to sustain plasma rotation in a centrifugal mirror at conditions approaching CHARM's design space. CMFX already has a 100 kV, 100 kW electrode system — measuring the sustained electrode power as a function of plasma density, temperature, and field parameters would provide the first empirical anchor for the recirculating fraction. If CMFX data shows rotation sustainment at 5% of fusion power (consistent with the 60 MW model assumption at 984 MW fusion power), the model's central estimate becomes defensible. If it shows 20–30%, the entire concept's economic case collapses. This measurement is achievable within the next 2–3 years without a new device. LCOE impact of favorable data: would compress the uncertainty range and shift confidence from Very Low to Low, allowing meaningful LCOE bounds.

**2. Any demonstration of a sustained nonthermal plasma with positive fusion gain exceeding bremsstrahlung losses.**
This is the concept's physics existence proof. It does not require CHARM architecture — any experiment (laser, mirror, FRC) that sustains a nonthermal proton distribution at p-B11-relevant temperatures with measured fusion yield exceeding bremsstrahlung loss would establish that the nonthermal approach is physically viable. No such experiment currently exists. A positive result would transform CHARM from a speculative physics bet into an experimentally grounded concept, which would justify substantially larger private investment and a more aggressive device roadmap. LCOE impact: would shift the probability of concept viability from ~10–30% to ~50–70% in my judgment, materially changing the expected-value LCOE calculation.

**3. Pale Blue Fusion publishing a power balance code output, even at the 0D level, with their central design parameters.**
The Fisch group has a working 0D power balance code, (PB)², shown at the ARPA-E meeting. If they publish even a summary of what this code produces — fusion power, recirculating fraction, Q_eng — for a specific design point, it would replace the model's five most uncertain parameters with company-internal estimates. Those estimates would still be theoretical (no experimental validation), but they would provide a more defensible central case than the current framework defaults. LCOE impact: could shift the overnight capital estimate by ±30% and LCOE by ±$15–20/MWh, and would allow the confidence rating to rise from Very Low to Low.
