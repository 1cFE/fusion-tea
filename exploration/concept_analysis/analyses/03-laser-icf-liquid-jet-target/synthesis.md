---
ID: 03-laser-icf-liquid-jet-target
Concept: Laser ICF - Liquid Jet Target (D-D)
Company: Cortex Fusion Systems
Type: synthesis
Status: draft
Created: 2026-03-22
---

# Synthesis: Laser ICF — Liquid Jet Target (D-D) (Cortex Fusion Systems)

---

## 1. Executive Summary

- **Most important risk**: The physics has never been demonstrated in any laboratory, by anyone, at any scale — and the primary source document contains a calculation that is almost certainly wrong by three orders of magnitude (3,333 MeV per D-D event vs. the standard ~3.65 MeV). If the 3,333 MeV figure is a calculation error, the Q~100 claim is built on a broken foundation. If it is a real physics claim, it is extraordinary and unverified. Either way, no LCOE estimate for this concept is trustworthy until the anomaly is explained and fusion from nanoshells is experimentally demonstrated by any group.

- **Most important advantage**: D-D fuel with no tritium, no superconducting magnets, and no cryogenic systems eliminates three of the most expensive and supply-chain-constrained cost categories in conventional fusion. If the physics ever works, the capital structure would be qualitatively lighter than any D-T concept: ~$300–600M in avoided tritium blanket, ~$50–100M in avoided cryogenics, and a laser driver that — if the Q~100 claim holds — would consume only ~40 MW of aggregate laser output power at 1 GWe scale.

- **LCOE ballpark**: **122.4 $/MWh** from the 1costingfe model (overnight capital: $4,557/kW, availability: 40%). This number is not a projection. It is the answer to the question "what would LCOE be if the undemonstrated physics worked exactly as claimed and all framework defaults are correct?" The real LCOE is either infinity (concept fails at physics), or somewhere above $122/MWh after availability, energy capture, and gold recycling assumptions are anchored to real data. Do not treat $122/MWh as a forecast.

- **Confidence verdict: Very Low.** Every LCOE-relevant parameter is either a framework default (no concept-specific data), a speculative extrapolation (Q~100 from a theoretical preprint with an anomalous energy figure), or a structural unknown (energy capture architecture, capacity factor, capital cost). The model's primary value is taxonomic — it shows what eliminated cost categories look like in the CAS structure — not predictive.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity elasticity from the 1costingfe model. The rank order is standard IFE pulsed architecture. The real rank order — if the physics eventually materializes — would be led by a parameter not in the model: whether plasmonic D-D fusion produces net energy at all.

### 1. Availability — elasticity: –0.99

**Assumed value**: 40% (pessimistic proxy for TRL 1 physics; no operational data exists).
**Sensitivity**: The strongest lever in the model by a factor of ~4 over the next-largest. Raising availability from 40% to 85% (mature IFE projection) would reduce LCOE from $122/MWh to approximately $57/MWh — putting this concept in competitive territory. Dropping further to 20% pushes LCOE above $240/MWh.
**What flips the economics**: This parameter is entirely unconstrained. There is no maintenance model, no component lifetime estimate, no MHz-rate continuous operation demonstration of any subsystem. Availability is a proxy for everything Cortex has not built: a nanoshell delivery system that runs at 10¹² events per second, optics that survive repeated plasma debris exposure, and liquid jet nozzles that operate reliably for years. Until these are demonstrated, 40% is not a defensible choice — it is an arbitrary placeholder. The availability assumption dominates LCOE but anchors nothing.

### 2. Interest Rate — elasticity: +0.70

**Assumed value**: 7% nominal (framework convention).
**Sensitivity**: At 10% interest, LCOE increases ~21% to ~$148/MWh; at 5%, decreases ~14% to ~$105/MWh.
**What flips the economics**: At $4,557/kW overnight, IDC ($595M) is the third-largest cost category. A project finance rate above 10% — realistic for a concept with zero experimental results — would add $15–25/MWh to LCOE from interest alone. This is a standard high-capital-cost vulnerability, not a concept-specific one.

### 3. Construction Time — elasticity: +0.28

**Assumed value**: 5 years (IFE framework default; no Cortex-specific basis).
**Sensitivity**: Each additional year of construction adds ~5.5% to IDC. At 7 years, LCOE increases by ~$14/MWh. At 8 years, ~$22/MWh.
**What flips the economics**: Not a primary concern at this stage of development. Construction time becomes relevant when there is a plant to build.

### 4. Laser Wall-Plug Efficiency (eta_pin1) — elasticity: –0.15

**Assumed value**: 10% (Ti:sapphire upper bound; Yb-fiber could reach 30%).
**Sensitivity**: A 3× improvement in laser efficiency (from 10% to 30%, achievable with Yb-fiber architecture) would reduce LCOE by ~15 × 0.15 ≈ 2.25% — modest, about $2.75/MWh. The impact is larger in the power balance: at 30% efficiency, laser wall-plug consumption at 1 GWe drops from 400 MW to ~133 MW, reducing the recirculating fraction from 31% to ~13%.
**What flips the economics**: If the driver requires Ti:sapphire at 5% efficiency (lower bound), the recirculating fraction grows and net output shrinks, requiring more fusion power per GWe of net electricity. At plant scale, laser driver architecture is a real economic choice — but it is secondary to whether the physics works at all.

### 5. Chamber Radius (plasma_t) — elasticity: +0.145

**Assumed value**: 4.0 m (IFE framework default; no Cortex chamber design disclosed).
**Sensitivity**: A 50% larger chamber (6 m) would increase LCOE by ~7%, primarily through CAS22 volume-based accounts. A smaller chamber (2 m) would reduce LCOE by ~7%.
**What flips the economics**: Chamber geometry is entirely unspecified by Cortex. This elasticity reflects a framework default, not a concept-driven design choice. The real issue is that chamber design depends on the energy capture architecture, which does not exist.

---

## 3. Risk Verdicts

**Challenge 1: No Energy Capture Architecture.**
**Verdict: Unlikely resolvable in the near term.**
**Rationale**: This is not a measurement gap — the energy conversion method does not exist even as a design concept in any Cortex source. A concept with no energy conversion architecture cannot be analyzed for LCOE; eta_th = 0.35 in the model is pure fiction.
**What would retire this risk**: A credible design (even pre-conceptual) describing how D-D charged particles and neutrons are captured, thermalized or directly converted, and used to produce electricity — including an efficiency estimate and the resulting BOP architecture.

**Challenge 2: Extraordinary Physics Claims, Anomalous Energy Figure.**
**Verdict: Unlikely resolvable without peer review and independent replication.**
**Rationale**: The Q~100 projection rests entirely on a theoretical preprint that also reports 3,333 MeV per D-D event — approximately 900× the standard value. Standard D-D produces 3.27 MeV (He-3 + n branch) or 4.03 MeV (T + p branch); secondary reactions at most bring total yield to ~20–30 MeV per initial D-D. The paper does not explain the 3,333 MeV figure. Until this is resolved, the Q claim has no credible basis.
**What would retire this risk**: Peer-reviewed publication of arXiv:2503.15531 with the 3,333 MeV figure resolved, followed by independent experimental demonstration of D-D fusion from nanoshells by any group.

**Challenge 3: Nanoshell Delivery at MHz Rates — Gold Recovery.**
**Verdict: Genuinely uncertain — but this is the least severe of the blocking risks.**
**Rationale**: The Cambridge group demonstrated stable kHz D2O liquid jet targets in 2024, providing partial proof of concept for the delivery mechanism. The novel element — gold nanoshell suspension at MHz rates with near-complete recovery — is an engineering challenge, not a physics impossibility. At ~60 mg/s gold consumption (estimated), unrecovered loss costs ~$18,000/hr at current gold prices ($85k/kg). Near-complete recycling is economically essential.
**What would retire this risk**: A laboratory demonstration of nanoshell delivery at ≥10 kHz with >95% gold recovery measured over sustained operation.

**Challenge 4: D-D Neutron Management at 10¹⁹ n/s.**
**Verdict: Genuinely uncertain — but technically tractable once flux and geometry are defined.**
**Rationale**: D-D produces 2.45 MeV neutrons (lower per-neutron damage than D-T 14 MeV), and shielding physics is well-understood. The challenge is scale: 10¹⁹ n/s exceeds all existing D-D sources by 14 orders of magnitude, and no shielding design exists for this concept. However, this is a solvable engineering problem once the chamber architecture is defined — it does not require new physics.
**What would retire this risk**: A neutronics pre-conceptual design study specifying shielding thickness, structural material selection, and activation inventory management for the projected flux — which requires first resolving the energy capture architecture.

**Challenge 5: 14-Order-of-Magnitude Scaling Gap.**
**Verdict: Unlikely resolvable in any near-term timeframe — this is the scale of the NIF challenge, applied to an unvalidated mechanism.**
**Rationale**: The closest independent experimental result (Cambridge 2024) achieved ~10⁵ n/s from a kHz liquid target. Cortex projects 10¹⁹ n/s. NIF required decades of development to achieve ignition, starting from a physics basis that was validated by nuclear weapons data. Cortex is starting from a theoretical preprint. The 14-order-of-magnitude gap is not a reason to dismiss the concept — it is a statement about the length of the development roadmap.
**What would retire this risk**: Nothing short of a multi-decade development program validated at each stage. The first milestone is any measurable D-D fusion signal from nanoshells; subsequent milestones are kHz, MHz, and eventually GW-scale operation.

**Challenge 6: Capital Cost Without Any Analogues.**
**Verdict: Genuinely uncertain — but unimportant until the physics works.**
**Rationale**: Femtosecond laser costs at plant-scale average power, nanoshell target factory costs, and the BOP have no precedents. This is a real economic uncertainty — but it is downstream of the physics question. Modeling capital cost before the concept produces any fusion is premature.
**What would retire this risk**: A plant design study, even at conceptual level, with cost estimates for the laser driver and target factory.

---

## 4. Structural Advantages and Disadvantages

**Compared against a conventional 1 GWe D-T tokamak baseline (e.g., CFS ARC-class concept).**

### Eliminated Cost Categories

| Item Eliminated | Approximate Saving | Confidence |
|---|---|---|
| Tritium breeding blanket (Li, FLiBe, Be) | ~$300–600M/GWe | High — D-D requires no lithium blanket or tritium supply |
| Isotope separation plant (C220112 = $0) | ~$50–100M/GWe | High — no Li-6 enrichment required |
| Superconducting coils (C220103 = $0) | ~$200–800M/GWe | High — no magnets of any kind |
| Cryogenic systems (p_cryo = 0 MW) | ~$50–100M/GWe | High — no superconductors |
| 14 MeV neutron damage management | Structural reduction in first-wall costs | Medium — D-D neutrons at 2.45 MeV are less damaging |
| Divertor (C220108 = $0) | ~$50–150M/GWe | High — IFE has no plasma exhaust channel |

At 1 GWe scale, these eliminations potentially remove **$650M–$1,750M** from the tokamak capital bill. This is the structural argument for the concept: if the physics works, the cost composition is genuinely lighter.

### Added or Amplified Cost Categories

| Item Added | Approximate Cost | Confidence |
|---|---|---|
| Gold nanoshell target factory (CAS22) | Unknown — model uses $2M/yr power assumption only | Very Low — cost of MHz nanoshell production entirely uncharacterized |
| Gold operating cost (if not recycled) | ~$158M/yr at 60 mg/s unrecovered | Medium — recoverable from geometry; recycling critical |
| Femtosecond laser driver at plant scale | Unknown — no cost analogue | Very Low — no fs laser at MW-class average power has been priced |
| Neutron shielding at 10¹⁹ n/s D-D | Unknown — no design exists | Very Low |
| Energy capture system | Unknown — concept not designed | Zero — does not exist |

### Net Assessment

The model produces $4,557/kW overnight (vs. ~$5,000–9,000/kW for D-T tokamaks) — but this comparison is misleading. The model uses IFE framework defaults for the large CAS categories (CAS22: $1,475M, CAS21: $816M) that have no relation to an actual Cortex plant. The eliminated cost items (magnets, blanket, cryogenics) are real and genuine; the remaining cost structure is entirely fabricated from framework analogues. The true overnight cost for a working Cortex plant could be $2,000/kW or $10,000/kW. The model cannot distinguish between these outcomes.

---

## 5. Cross-Concept Positioning

Cortex occupies a position unlike any other concept in this analysis: **zero experimental results, the lowest TRL, and an unresolved physics anomaly — combined with the most compelling theoretical cost structure if the physics works.**

**Where it sits in the landscape**: This is not in the same class as Helion (TRL 5–6, demonstrated fusion yields, known rep rate challenge) or Realta (TRL 3–4, WHAM validated, Q is the open question). Cortex is at TRL 1: basic principles of plasmonic field enhancement are real in nanophotonics, but their application to nuclear fusion has not been demonstrated by anyone. The concept is closer in maturity to a research proposal than to an engineering program.

**Closest economic analogues:**
- *07-MagLIF*: Both are pulsed, both rely on a pulsed driver, both need MHz rep rates for commercial operation. MagLIF has demonstrated single-shot fusion yields and is scaling up; Cortex has not demonstrated any yield. MagLIF also carries per-shot consumable costs; Cortex's nanoshell recycling, if achieved, would avoid this.
- *26-Laser ICF indirect drive (NIF-class)*: Both are laser IFE. Cortex's claimed advantage is radical driver simplification — eliminating the multi-billion-dollar DPSSL or KrF system in favor of a ~40 MW femtosecond laser at plant scale. This would be transformative if true. NIF spent $3.5B on the laser alone. Cortex is claiming the laser cost problem is essentially solved if the plasmonic enhancement works.

**What makes this concept fundamentally different:**
1. **It is the only concept in this analysis where the primary physics mechanism has no experimental support of any kind.** Every other concept — even early ones — has laboratory fusion yield data.
2. **If the plasmonic enhancement works as described, it solves the laser cost problem that has blocked laser IFE commercialization for 40 years.** This is not incremental improvement — it is a different physical mechanism for achieving ignition-equivalent conditions.
3. **The 3,333 MeV anomaly is a concept-specific flag with no analogue in any other analysis.** If this figure reflects a calculation error in the primary source, the foundational Q claim requires independent recalculation before any economic analysis is meaningful.

**Bottom line on positioning**: Cortex should be tracked as a speculative long-shot with a genuinely novel physical mechanism, not as a near-term competitor. The development timeline, if successful, is measured in decades — not years. The economic upside is real if the physics is validated; the probability of near-term validation is low.

---

## 6. Modeling Confidence

**Rating: Very Low** (below the "Low" applied to Helion and Realta in prior syntheses).

| Parameter | Data Source | Uncertainty |
|---|---|---|
| Availability (40%) | Analyst judgment; no operational data | Factor of 2+ plausible; 0% (concept fails) is nonzero |
| eta_th (35%) | Rankine placeholder; no energy architecture exists | Completely unconstrained — architecture doesn't exist |
| Q_sci (~100) | Theoretical preprint with 3,333 MeV anomaly | May be fundamentally wrong |
| p_implosion (40 MW) | Scaled from 3 kW @ 1 MW fusion; very rough | Factor of 3–5 plausible range |
| eta_pin1 (10%) | Ti:sapphire upper bound; Yb-fiber could reach 30% | Factor of 3 range |
| Gold recycling (100%) | Assumed; not demonstrated | 0–100% — fully unconstrained |
| CAS22 ($1,475M) | IFE framework default | Not derived from any Cortex data |
| CAS21 ($816M) | IFE framework default | Not derived from any Cortex data |
| Chamber geometry | IFE YAML defaults | No Cortex chamber design exists |

**Dominant source of LCOE uncertainty**: The physics basis. If the plasmonic enhancement mechanism does not produce D-D fusion at the claimed rates — which is the most likely near-term outcome given zero experimental evidence — the LCOE is undefined and the concept does not proceed. This is not a "the LCOE might be higher" situation. It is a "the concept might not work" situation, and it is the dominant uncertainty.

**Secondary source**: Energy capture architecture. eta_th = 0.35 is entirely fabricated. The true value depends on an architecture that does not exist. A direct-conversion scheme (if the charged-particle branch is exploited) could achieve 60–80% efficiency, dramatically improving LCOE. A thermalized neutron scheme with a Rankine cycle would achieve 30–40%. Without the architecture, eta_th has a factor of ~2 uncertainty that directly multiplies into LCOE.

**The $122/MWh model output should be read as a structural lower bound for a working Cortex plant at NOAK scale with optimistic framework defaults — not as a central estimate.** The upper bound is infinite if the physics does not work, and poorly characterized even if it does.

---

## 7. What Would Change My Mind

**1. Peer-reviewed publication of arXiv:2503.15531 with the 3,333 MeV anomaly resolved.**
This is the highest-priority near-term disclosure. If the 3,333 MeV figure is corrected in peer review (most likely outcome), the Q~100 claim requires recalculation and may not survive. If it is explained and defended (extraordinary claim), it would represent a physics breakthrough that would fundamentally alter every downstream estimate. Either outcome — the error or the explanation — changes the LCOE analysis: downward if Q is reduced, and would raise confidence from Very Low to Low if explained consistently. This is achievable in 6–12 months through normal peer-review timelines.

**2. Any published measurement of D-D fusion yield from nanoshells — by any group.**
Even 10² neutrons per second at laboratory scale would confirm the physical mechanism. This development would not move the LCOE estimate significantly — the 14-order-of-magnitude gap to commercial scale would remain — but it would transition Cortex from "theoretical proposal" to "demonstrated physical effect" and justify moving from a TRL 1 to TRL 2–3 treatment. At that point, more detailed LCOE modeling becomes meaningful: the model structure is correct, only the parameters are unconstrained. Impact: would shift modeling confidence from Very Low to Low and give the $122/MWh lower-bound estimate a defensible physical interpretation.

**3. Disclosure of an energy capture architecture with any efficiency estimate.**
The single blocking gap that makes commercial LCOE completely unmodelable. Even a preprint or patent application describing how D-D fusion energy is converted to electricity — whether direct conversion of charged particles, thermal neutron capture in a blanket, or some hybrid — would allow eta_th to be estimated from first principles rather than fabricated. If Cortex discloses a direct-conversion architecture with plausible 60–70% efficiency, LCOE under the "physics works" scenario drops to approximately $80–90/MWh — competitive with new fission. If the architecture is thermal Rankine, LCOE stays near $120/MWh. This disclosure is zero-cost for Cortex and would substantially reduce the dominant non-physics uncertainty in the model.
