---
ID: 08-frc-w-direct-conversion
Concept: FRC w/ Direct Conversion
Company: Helion Energy
Type: synthesis
Status: approved
Created: 2026-03-22
Approved-Date: 2026-03-22
---

# Synthesis: FRC w/ Direct Conversion (Helion Energy)

---

## 1. Executive Summary

- **Most important risk**: The repetition rate gap. Trenta demonstrated ~0.002 Hz; the commercial target is 1–2 Hz — a 500–1,000× increase in pulse frequency with no public milestone on Polaris. Availability drives LCOE with elasticity –0.91, but that's not the real danger. The danger is that achieving and sustaining 1 Hz for 30 years (≈10⁹ shots) is a qualitatively different engineering regime from anything Helion has demonstrated, and the entire capital structure of a $1,773/kW plant produces no revenue at 0.002 Hz.

- **Most important advantage**: No thermal conversion cycle. Eliminating the steam turbine, heat exchangers, and associated balance-of-plant saves an estimated ~$127M per 50 MWe module (handwritten analyst, §Quantitative LCOE Model). At fleet scale, this is approximately $100–$150/kW of capital that Helion simply doesn't need to build or maintain. Combined with no HTS supply chain, no breeding blanket, and near-zero fuel cost (deuterium from water), the cost structure of a working Helion plant is fundamentally lighter than any D-T thermal concept.

- **LCOE ballpark**: **50.3 $/MWh (5.0 ¢/kWh)** from the 1costingfe model at NOAK, 1 GWe fleet scale (20 × 50 MWe modules), 85% availability. Overnight capital: $1,773/kW. This is best-case: it assumes NOAK capacitor banks at $0.50/J (10× cheaper than current commercial), He3 fuel at the optimistic self-bred cost ($2M/kg vs. $16,000–$120,000/g spot), and energy recovery efficiency of 90%. Under a stress scenario — current cap bank pricing ($5/J) — capital roughly doubles and LCOE reaches approximately **$100/MWh**. The true range is $50–$100/MWh under explicitly modeled assumptions; it is unbounded if He3 startup inventory is large.

- **Confidence verdict: Low.** No independent TEA exists for Helion. The three most influential parameters (availability, energy recovery efficiency, capacitor bank cost) each span a 2–10× range from available public data, with no direct plant-scale measurement anchoring any of them. The model is structurally sound but parametrically speculative.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity elasticity from the 1costingfe model, supplemented with qualitative judgment for parameters the model cannot capture.

### 1. Availability — elasticity: –0.91

**Assumed value**: 85% (standard fusion plant assumption; no published Helion target).
**Sensitivity**: A drop from 85% to 50% availability raises LCOE by roughly 37%, from $50 to ~$69/MWh. A drop to 30% (credible for a first-of-kind pulsed system) would push LCOE to ~$100/MWh.
**What flips the economics**: Availability below ~40% would push LCOE above competitive natural-gas power and undermine the concept's value proposition. The driver is not just downtime — it is the interplay between rep rate reliability, coil cooling cycles, bank maintenance, and plasma exhaust management, none of which have been validated at sustained 1 Hz operation.

### 2. Interest Rate — elasticity: +0.73

**Assumed value**: 7% nominal.
**Sensitivity**: At 10% interest, LCOE increases by ~22%; at 5%, decreases by ~15%.
**What flips the economics**: This concept's capital cost ($1,773/kW overnight) is moderate by fusion standards — lower than D-T tokamaks — so interest rate sensitivity is real but not dominant. A project finance rate above 12% (realistic for a pre-commercial technology) would push LCOE toward $80–$90/MWh from the model baseline alone.

### 3. Fuel Recovery — elasticity: –0.52

**Assumed value**: 95% He3 recovery from exhaust.
**Sensitivity**: This elasticity is surprisingly large — larger than energy recovery efficiency — because He3 fuel cost is the single largest annualized cost in the model ($223.7M/year at NOAK self-bred $2M/kg). At 95% recovery, fuel cost is bounded. At 80% recovery, fuel cost grows by a factor of ~5 (every cycle loses more expensive He3), which would push annualized fuel cost to ~$1B/year and make LCOE noncompetitive.
**What flips the economics**: Fuel recovery below ~85% would make He3 fuel cost dominant. This highlights a structural fragility: even the "cheap" self-bred He3 cost assumption ($2M/kg) is large enough to dominate LCOE if exhaust recycling is inefficient. This parameter is unvalidated in any public Helion source.

### 4. Construction Time — elasticity: +0.24

**Assumed value**: 4 years (factory-built modular).
**Sensitivity**: Each additional year of construction adds ~24% to interest during construction (IDC = $175.7M at baseline). At 6 years, LCOE increases by ~10%.
**What flips the economics**: Not a primary concern for modular deployment. The factory-built, compact linear geometry is a genuine advantage that reasonably supports the 4-year assumption. This is the one parameter where the model's optimistic estimate is defensible without qualification.

### 5. Energy Recovery Efficiency (eta_th) — elasticity: –0.11

**Assumed value**: 90% (central estimate from three conflicting public data points: >95% subscale, 85–95% Contrary Research range, 70% ARPA-E design point).
**Sensitivity**: The elasticity is modest — 10% reduction in eta_th raises LCOE by ~1%. But this misrepresents the true risk: if the ARPA-E figure of 70% is the correct plant-scale value (not the subscale demo), the recirculating fraction increases substantially and the net electric output per module shrinks. At eta_th = 0.70, the model would need to be re-run with different power balance — the elasticity formula is not a reliable extrapolation that far from the central point.
**What flips the economics**: If plant-scale efficiency is 70% (ARPA-E design point), not 90%, the concept still works but with a significantly higher recirculating fraction. The 90% assumption deserves scrutiny as the highest-leverage physics question still unresolved.

---

## 3. Risk Verdicts

**Challenge 1: Energy balance underclosed — gain and recirculating power unknown.**
**Verdict: Genuinely uncertain.**
**Rationale**: The ARPA-E η×Gain = 0.2×1.2 at η=0.70 is internally consistent, but Helion's website claims >95% recovery — irreconcilable without knowing what "recovery" each source is measuring. Commercial Q is not disclosed.
**What would retire this risk**: A published power balance table — even an order-of-magnitude Q estimate — for Polaris operation, or a peer-reviewed system study from Helion.

**Challenge 2: Rep rate — 500–1,000× demonstration gap.**
**Verdict: Unlikely resolvable without major milestones in the next 2–3 years.**
**Rationale**: The jump from 0.002 Hz (Trenta) to 1–2 Hz is not a linear scaling problem. It requires solving coil cooling, bank recharge, FRC formation reliability, and plasma exhaust clearing simultaneously at 10⁹-shot lifetimes. The timeline pressure is real: Orion is under construction for a 2028 target, but no public rep-rate data has been released for Polaris despite it being the critical demonstration device.
**What would retire this risk**: A publicly disclosed rep rate ≥0.5 Hz demonstrated on Polaris for sustained operation (hundreds of consistent shots).

**Challenge 3: D-He3 physics — temperature gap and undemonstrated fuel cycle.**
**Verdict: Genuinely uncertain — but the gap is smaller than it looks.**
**Rationale**: Polaris reached 13 keV (D-T) in January 2026. D-He3 threshold is ~17 keV per Helion. That is a 33% increase — not a factor of 20 — even though the D-He3 cross-section peak (300–500 keV) is far above operating temperature. Helion's strategy operates at the low-energy tail of the D-He3 cross section where temperatures are achievable, not at the peak. The physics is harder than D-T but probably achievable with continued prototype development.
**What would retire this risk**: D-He3 fusion yield demonstrated on Polaris or the next prototype generation. Even a small yield measurement would confirm the physics pathway.

**Challenge 4: He3 breeding bootstrap — startup inventory unknown.**
**Verdict: Genuinely uncertain — and potentially blocking for fleet deployment.**
**Rationale**: This is the concept's hidden systemic risk. If each plant requires ~10 kg of He3 at startup (a plausible but unpublished estimate), and global production is ~8 kg/year, fleet deployment beyond the first few plants is rate-limited by He3 supply. The 12.3-year tritium decay path means even a plant running DD operation for 5 years has produced only a fraction of its own He3 inventory. At market spot prices ($16,000–$120,000/g), a 10 kg startup inventory is $160M–$1.2B per plant.
**What would retire this risk**: Public disclosure of the He3 startup inventory requirement per plant and a fleet deployment model showing how DD breeding fills the gap.

**Challenge 5: Capacitor bank cost — requires 10× cost reduction from current prices.**
**Verdict: Likely resolvable — but carries execution risk.**
**Rationale**: Helion's in-house manufacturing strategy directly targets this. The analogy to photovoltaic and battery manufacturing learning curves is reasonable: purpose-built volume manufacturing regularly achieves 5–10× cost reductions over 10–15 years. The IGBT switching hardware is commercially available and has a mature cost reduction trajectory. The specific lifetime requirement (10⁹ shots) is the harder challenge, but pulsed-power literature suggests this is addressable with modern components.
**What would retire this risk**: A published Helion manufacturing cost curve for capacitors, or a demonstrated NOAK prototype achieving $1/J or below.

**Challenge 6: Direct conversion unvalidated at plant scale.**
**Verdict: Likely resolvable.**
**Rationale**: The physics (expanding magnetized plasma inducing current in surrounding coils) is sound and well-understood. The subscale >95% demonstration (>1M pulses with IGBTs) is the best TRL evidence for any subsystem in this concept. Scaling to 50 MW/module at 1–2 Hz is an engineering challenge, not a physics puzzle.
**What would retire this risk**: A system-level demonstration at Polaris-scale power and rep rate with measured round-trip efficiency.

---

## 4. Structural Advantages and Disadvantages

**Compared against a conventional 1 GWe D-T tokamak baseline (e.g., CFS ARC-class concept analyzed in 01-hts-compact-tokamak).**

### Eliminated Cost Categories

| Item Eliminated | Approximate Saving | Confidence |
|---|---|---|
| Steam turbine plant (CAS23 = $0) | ~$200–$400M/GWe | Medium — handwritten estimates $127M/50 MWe |
| HTS superconducting coils | ~$500–$1,000M/GWe | High — aluminum at commodity pricing vs. REBCO |
| Cryogenic systems (p_cryo = 0) | ~$50–$100M/GWe | High — no superconductors means no cryo |
| Tritium breeding blanket | ~$300–$600M/GWe | High — D-He3 eliminates FLiBe, Li, Be blanket |
| 14 MeV neutron shielding | Structurally reduced | High — DD neutrons at 2.45 MeV, not 14.1 MeV |
| Per-shot consumables | ~$0.70–$1/shot → $0 | High — coils not destroyed (unlike MagLIF) |

At fleet scale, these eliminations collectively amount to roughly **$1,000–$2,000/kW in avoided capital** relative to D-T thermal designs — which explains why the model's $1,773/kW overnight cost is competitive despite the technology's early stage.

### Added or Amplified Cost Categories

| Item Added | Approximate Cost | Confidence |
|---|---|---|
| Capacitor bank + IGBT (CAS22 C220104) | $200M for 20 modules (at NOAK $0.50/J) | Low — requires 10× cost reduction |
| He3 fuel handling system (C220500) | $40M plant-wide | Medium |
| He3 fuel cost (annualized, CAS80) | $223.7M/year at $2M/kg self-bred | Low — spot price would be >$500M/year |
| Remote handling (C220110) | $156.7M (dominant CAS22 line item) | Medium |

**The capacitor bank and He3 fuel are the two added cost burdens that have no equivalent in D-T thermal designs.** Of these, He3 fuel cost (annualized) actually exceeds the cap bank total at NOAK — which is non-obvious and important.

### Net Assessment

The capital structure favors Helion over thermal tokamaks: $1,773/kW vs. ~$3,000–$5,000/kW for D-T concepts with HTS magnets and thermal cycles. But this advantage evaporates quickly if cap banks remain at current pricing ($5/J → capital doubles to ~$3,500/kW), or if He3 startup inventory adds $100M–$1B of pre-operation cost per plant.

---

## 5. Cross-Concept Positioning

Helion occupies a structurally unique position in the fusion landscape: **highest potential upside on cost structure, combined with least data-anchored physics.** No other concept has simultaneously eliminated the thermal cycle, the HTS supply chain, the tritium blanket, and per-shot consumables. These are four of the five most expensive components of conventional D-T fusion. But no other concept with a serious commercial timeline has as large a gap between its leading prototype performance and its commercial requirements.

**Closest economic analogs:**
- *07-MagLIF*: Shares pulsed operation framework and capacitor bank cost challenge. Diverges sharply in that MagLIF must pay ~$0.70–$1/shot in consumable targets and has no direct energy recovery pathway. Helion's cost structure is better in the long run if rep rate is achieved.
- *General Atomics FRC / Norman (TAE)*: Similar device architecture (FRC), different fuel strategy (p-B11 for TAE; D-He3 for Helion). TAE's p-B11 requires even higher temperatures than D-He3, making physics risk higher still.

**What makes Helion fundamentally different** from all tokamak concepts (01-hts-compact-tokamak, 21-spherical-tokamak-hts): the elimination of the thermal cycle is not an incremental improvement — it is a different economic category. Thermal efficiency constraints (η ≈ 35–42% for Rankine) force tokamak designs to produce 3× the fusion power they sell as electricity. Helion at η = 90% produces ~1.1× the fusion power they sell as electricity. This is why a Helion concept with Q_eng = 3.8 is competitive with a tokamak requiring Q_eng > 10.

**What makes Helion the highest-risk bet**: Every other concept in this analysis (tokamaks, MagLIF) has at least one independent peer-reviewed TEA anchoring cost estimates. Helion has none. The absence of a published techno-economic analysis means the model here is built from fragment data: an ARPA-E slide, a CEO quote about aluminum magnets, and a capacitor bank from an investor research report. The uncertainty envelope is proportionally wider.

---

## 6. Modeling Confidence

**Rating: Low.**

| Parameter | Data-Anchored? | Primary Uncertainty |
|---|---|---|
| Energy recovery efficiency (eta_th = 90%) | No — 3 conflicting sources (70%, 85–95%, >95%) | Factor of ~1.4 range |
| Availability (85%) | No — no published Helion target | Factor of ~2 plausible range |
| Capacitor bank cost ($0.50/J NOAK) | No — current commercial is $5/J | Factor of ~10 range |
| He3 fuel cost ($2M/kg self-bred) | Partially — spot price 8–60× higher | Factor of 8–60 on fuel line |
| Buildings ($400M) | No — analogue from dhe3_pulsed_frc.py | Order-of-magnitude placeholder |
| Coil cost ($5M/mod) | Partially — commodity Al pricing | Factor of ~2–3 plausible |
| Construction time (4 yr) | Partially — modular geometry supports this | Low uncertainty |

**Dominant source of LCOE uncertainty**: Availability. Not because we have a good reason to believe 85%, but because availability is a proxy for everything Helion hasn't demonstrated: rep rate reliability, coil fatigue life, bank lifetime, and FRC formation consistency. The model assumes the concept works as designed. If the rep rate demonstration gap (1,000×) is not closed, the availability assumption fails catastrophically.

**Secondary source**: He3 startup inventory cost. This is entirely unmodeled. If each plant requires even 5 kg of He3 at startup ($80M–$600M at spot), it adds $8–$60/MWh to LCOE for a single-module Orion plant — potentially dominating capital cost. At fleet scale with self-bred inventory, this cost eventually disappears. But the first-plant economics could look nothing like the NOAK model.

**The model is best interpreted as a lower-bound LCOE floor assuming Helion's engineering bets all succeed at NOAK scale.** The upper bound is not well-characterized.

---

## 7. What Would Change My Mind

**1. Published rep rate for Polaris ≥ 0.5 Hz with sustained operation data.**
This is the single most important near-term disclosure. If Polaris is achieving even 0.1 Hz reliably, the 1,000× gap becomes a 10–20× gap — still large, but plausibly bridgeable in a commercial development program. A confirmed rep rate would also allow a real availability estimate for the first time, replacing the model's most uncertain input with a data-anchored value. LCOE impact: if demonstrated availability of 70%+ is shown, confidence in the $50–$70/MWh range improves substantially.

**2. He3 startup inventory disclosure or Orion commissioning data.**
If Orion comes online in 2028 and Helion discloses the He3 inventory required, fleet economics become calculable for the first time. If the startup inventory is small (<$5M worth of He3), the economic model is essentially validated. If it's large (>$100M), LCOE for early plants is substantially higher than this model shows — and the fleet deployment timeline is constrained by global He3 supply. This disclosure alone would either confirm or undermine the $50/MWh narrative.

**3. Capacitor bank NOAK cost target published or demonstrated below $1/J.**
If Helion discloses a manufacturing cost roadmap showing a credible path to $0.50–$1.00/J through in-house production at volume, the cap bank assumption in this model transitions from speculative to defensible. If instead an independent plant design study shows that commercial-scale banks at 40 T require $3–$5/J for the foreseeable future, LCOE doubles and the concept's competitive position relative to advanced fission (AP1000 at ~$1,500–$2,500/kW) weakens materially.
