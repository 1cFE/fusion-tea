---
ID: 21-renaissance-stellarator
Concept: Renaissance Stellarator (D-T)
Company: Renaissance Fusion
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Editorial Synthesis: Renaissance Stellarator (D-T)

## 1. Executive Summary

- **Biggest Risk**: Laser-patterned HTS film manufacturing has no cost analogue at any scale. A 10× cost premium vs. tape-winding would drive LCOE to >500 $/MWh; this single account dominates all other uncertainties.
- **Biggest Advantage**: Integrated liquid metal wall consolidates first wall, blanket, coolant, and breeder into a single flowing circuit, potentially eliminating the discrete module replacement cycle that drives availability losses in solid-blanket concepts. The sCO₂ combined cycle delivers 48% thermal efficiency — a 13-point premium over steam Rankine.
- **LCOE Ballpark**: 130–520 $/MWh at the published 1 GWe design point, spanning the laser-patterning cost uncertainty (0.3–10× tape-winding baseline). The nominal case (129 $/MWh, assuming tape-winding cost applies) is a placeholder — it does not reflect the manufacturing risk.
- **Confidence Verdict**: Low. The concept architecture is bold and well-integrated, but two critical cost accounts (magnet system, liquid metal wall) have no data anchors, and the Q=∞ plasma target sits ~11× below the ISS04-extrapolated Lawson threshold at the published T=10 keV design point.

---

## 2. What Matters Most for LCOE

### 1. Laser-Patterned HTS Coil Cost (r_coil and C220103 multiplier)
- **Assumed value**: Tape-winding cost model yields C220103 = $2.26B (placeholder). No published manufacturing cost data exists.
- **Sensitivity**: Elasticity +0.76 on r_coil. A 10× cost multiplier (first-of-kind film deposition premium) produces LCOE = 517 $/MWh — a 418 $/MWh swing from the optimistic 0.3× scenario (99 $/MWh).
- **What would flip the conclusion**: If laser-patterned film deposition achieves <$50/m² at production scale (vs. $100–300/kA-m for wound tape), the magnet cost advantage could be real. If deposition costs exceed $200/m², the concept becomes uncompetitive. The MT29 Helmholtz demo (6 T at 1.2 m diameter) validates physics but provides zero cost insight.

### 2. Plant Availability
- **Assumed value**: 92% (estimated from "near-100% duty cycle" claim; maintenance intervals uncharacterized).
- **Sensitivity**: Elasticity −0.94. A 10-point drop (92% → 82%) increases LCOE by ~9.4%.
- **What would flip the conclusion**: If the liquid metal wall eliminates solid-blanket replacement downtime and achieves >95% availability (comparable to gas turbines), LCOE drops ~4%. If pump/exchanger failures drive availability below 85%, LCOE rises into non-competitive territory regardless of capital cost.

### 3. Construction Time
- **Assumed value**: 10 years (first-of-kind liquid metal wall integration and laser-patterned magnet manufacturing add schedule risk).
- **Sensitivity**: Elasticity +0.54. Reducing to 7 years (NOAK with established magnet supply chain) cuts LCOE by ~16%; extending to 13 years (manufacturing delays) raises LCOE by ~16%.
- **What would flip the conclusion**: If the laser-patterning process scales faster than wound-tape production lines (fewer manual steps), construction time could beat conventional HTS stellarators by 1–2 years. If film deposition quality control requires extensive rework, add 2–3 years to schedule.

### 4. Peak Coil Field (b_max)
- **Assumed value**: 15 T (baseline design target). Published envelope: 15–40 T.
- **Sensitivity**: Elasticity +0.38. The 15 T → 40 T swing produces an 82 $/MWh LCOE increase (129 → 211 $/MWh) independent of the r_coil manufacturing cost uncertainty. At b_max = 40 T, REBCO Jc degrades sharply at 20 K, requiring larger coil cross-section or lower operating temperature — both drive cost.
- **What would flip the conclusion**: Achieving the compact A=4 QI geometry at b_max ≤ 18 T would significantly reduce coil material demand. If the design requires b_max > 30 T to close confinement, the magnet cost doubles and LCOE exceeds 200 $/MWh even in the optimistic film-cost scenario.

### 5. Thermal Efficiency (eta_th)
- **Assumed value**: 48% (sCO₂ Brayton-Rankine; canonical for this category per scoring framework; ECM 2023 reports 49–51%).
- **Sensitivity**: Elasticity −0.12. A 5-point drop (48% → 43%) increases LCOE by only ~1.3%. Not a dominant lever.
- **What would flip the conclusion**: Nothing. The 13-point efficiency premium over steam Rankine (48% vs. 35%) is favorable but secondary to coil cost and availability. If the sCO₂ cycle fails to demonstrate at GW scale and the plant falls back to steam Rankine, LCOE rises ~7% — painful but not fatal.

---

## 3. Risk Verdicts

### Laser-patterned HTS film manufacturing at stellarator scale
- **Verdict**: Genuinely uncertain
- **Rationale**: The 6 T Helmholtz demo validates the physics; scaling to 10–15 T across a full toroidal array with nuclear-grade uniformity is an engineering challenge without precedent.
- **What would retire this risk**: A full-scale modular coil segment (2–3 m diameter, 15 T peak field, QI-optimized current path) operated for >1000 hours at 20 K, with published manufacturing throughput and yield data. Until then, use 3–10× cost uncertainty bounds.

### Ignited plasma (Q=∞) in compact QI stellarator
- **Verdict**: Unlikely resolvable without intermediate steps
- **Rationale**: ISS04 scaling extrapolated to R₀=4 m, a=1 m, B=10 T at T=10 keV predicts n·τ_E ~11× below the Lawson ignition threshold. The design likely targets T=20–30 keV (where <σv>/T² peaks for D-T) or relies on confinement improvement beyond ISS04, neither of which is experimentally validated in a compact stellarator.
- **What would retire this risk**: A burning-plasma stellarator experiment (Q ≥ 5) at any aspect ratio, or a validated physics model showing compact QI confinement improvement factors >3× vs. ISS04. Without this, the Q=∞ claim is speculative and should be modeled as Q=5–10 with continuous heating.

### Liquid Li-LiH wall at 25 MW/m² and 10 T
- **Verdict**: Likely resolvable (but not yet resolved)
- **Rationale**: The physics of liquid metal MHD in high-field environments is well-understood from sodium fast reactors and fusion blanket R&D. The Li-LiH mixture at fusion-relevant wall loading is undemonstrated but not fundamentally blocked.
- **What would retire this risk**: A prototypical flowing Li-LiH test section operated at ≥10 MW/m² and ≥5 T for >100 hours with measured MHD pressure drop, tritium extraction rate, and heat transfer performance. This is a tractable near-term experiment.

### sCO₂ combined cycle at 48% efficiency and GW scale
- **Verdict**: Likely resolvable
- **Rationale**: sCO₂ Brayton cycles have been demonstrated at 10 MWe scale. The combined Brayton-Rankine architecture is established in gas turbine plants. The fusion-specific challenge is integrating with a liquid metal heat source at the required temperature; this is an engineering problem, not a physics barrier.
- **What would retire this risk**: A 100+ MWe sCO₂ Brayton-Rankine demonstration plant (not necessarily fusion-coupled) achieving >45% efficiency for >1000 hours. This is on industry roadmaps for 2025–2030.

### TBR = 1.60 in liquid Li-LiH blanket
- **Verdict**: Likely resolvable
- **Rationale**: JNM 599 reports TBR = 1.60 analytically (10 cm Pb + 22 cm Li-LiH), well above the 1.15 design requirement. The 39% margin is intended to cover port losses in the 3D stellarator geometry. This is conservative and credible.
- **What would retire this risk**: Experimental validation of TBR > 1.3 in a prototypical liquid Li-LiH blanket mockup under fusion-relevant neutron flux. The analytical result is trustworthy for scoping but should be validated at subscale.

### No divertor design published
- **Verdict**: Genuinely uncertain
- **Rationale**: Not a single published source addresses plasma exhaust or divertor architecture. This is a critical omission for any D-T stellarator. The liquid metal wall may tolerate higher heat fluxes than solid PFCs, but a magnetic divertor or island divertor is still required for impurity control.
- **What would retire this risk**: Publication of a divertor concept integrated with the compact QI geometry and liquid metal wall. Until then, assume a W7-X-style island divertor adapted to A=4, adding uncertainty to first-wall/exhaust capital cost.

---

## 4. Structural Advantages and Disadvantages

### Advantages vs. D-T Tokamak Baseline

1. **No central solenoid (CS)** — stellarator inherent. Eliminates C220104 (CS magnet capital cost, ~$50–100M) and removes CS fatigue as an availability constraint.

2. **No disruptions** — stellarator inherent. Eliminates disruption mitigation hardware (C220109, ~$20–50M) and enables the >90% availability assumption. Tokamaks budget 5–10% availability loss to disruption recovery; stellarators avoid this.

3. **Integrated liquid metal wall** — novel. Consolidates C220101 (first wall, ~$300–500M in solid-blanket designs), C220102 (blanket modules, ~$400–600M), and portions of C220106 (coolant systems) into a single $400M (±50%) flowing circuit. The uncertainty is large, but if the integration works, this is a 30–40% reduction in CAS22 accounts vs. discrete module replacement.

4. **Ignited plasma (if achieved)** — novel. Eliminates C220109 (ECRH gyrotrons, ~$100–200M for continuous heating) and reduces recirculating power fraction from ~15% (ECRH-heated stellarator) to ~8% (cryogenics + pumps only). At 1 GWe net, this saves ~100 MW of parasitic load, worth ~5 $/MWh LCOE.

5. **sCO₂ combined cycle at 48%** — novel. Reduces required thermal power by ~25% vs. steam Rankine (35%) for the same 1 GWe output. This scales down blanket/BOP capital cost by ~15–20% (not 1:1 because many BOP accounts are fixed). Worth ~10–15 $/MWh LCOE reduction.

### Disadvantages vs. D-T Tokamak Baseline

1. **Laser-patterned HTS film (factor 3–10× cost uncertainty)** — novel. If film deposition costs exceed tape-winding by >3×, the magnet cost penalty wipes out all other architectural savings. C220103 becomes the dominant LCOE driver, potentially adding +200–400 $/MWh.

2. **3D non-planar stellarator field geometry** — stellarator inherent. Even with laser patterning, the complex current paths required for QI optimization add manufacturing difficulty vs. axisymmetric tokamak coils. This is already reflected in the high b_max sensitivity (elasticity +0.38).

3. **Liquid metal circulation pumps (p_pump = 380 MW, ±50%)** — novel. At 25 MW/m² wall loading, the liquid metal system consumes ~26% of gross electric output just for pumping. By comparison, solid-blanket stellarators budget ~200 MW for all coolant pumps at much lower wall loading. If p_pump rises to 500 MW (the +50% uncertainty case), net efficiency drops to 30%, and LCOE increases by ~13%.

4. **Unanchored economics** — novel. Unlike CFS (Sorbom et al. 2015), ARIES-CS, or any other stellarator with a published cost model, Renaissance Fusion has released zero economic data. Every CAS account is built from first principles or analogies. This introduces systemic modeling uncertainty of ±30–50% on total capital cost, independent of the specific technology risks.

---

## 5. Cross-Concept Positioning

Renaissance Fusion occupies a unique position: it is the **only stellarator in the survey with integrated liquid metal walls** and the **only HTS-magnet concept using laser-patterned film instead of wound tape**. The architectural choices are internally consistent — the liquid metal wall tolerates high heat flux and enables compact geometry; the compact geometry (A=4) requires high field (10 T) to maintain confinement; high field demands HTS; and laser-patterned film eliminates the 3D coil winding complexity that would otherwise dominate manufacturing cost.

**Similar economics (if laser-patterning cost is favorable)**:
- **Proxima Fusion (09)** and **Type One Energy (20a)**: QI stellarators with HTS magnets, but wound REBCO tape and solid blankets. If Renaissance's film deposition achieves <1× tape-winding cost, it undercuts Proxima/Type One by ~20–30% on C220103 and gains another ~10–15% from the integrated wall. Combined advantage: ~30–40 $/MWh LCOE reduction.
- **ARC-class compact tokamaks (01)**: Similar high-field HTS + liquid metal blanket architecture, but tokamak disruption risk and CS fatigue limit availability. Renaissance's stellarator physics offers +5–10 percentage points availability advantage, worth ~15–25 $/MWh.

**Similar economics (if laser-patterning cost is unfavorable)**:
- **Gauss Fusion large-scale stellarator (10)**: Large A~10 stellarator with conventional magnets. If Renaissance's film deposition costs 5–10× tape-winding, the magnet penalty (+200–300 $/MWh) overwhelms all compact-geometry savings, and Gauss's lower-field LTS approach becomes cheaper despite lower power density.

**Fundamentally different**:
- **Laser IFE (NIF-commercialization, 30)**: Pulsed target-based fusion with no continuous plasma or magnets. Renaissance's steady-state operation and magnet-driven cost structure have no overlap.
- **Levitated dipole (12, 19)**: Zero external coils (plasma confined by internal levitated magnet). Renaissance depends entirely on external HTS coils — opposite ends of the stellarator design space.

The concept's economic fate hinges on **two binary technology bets**: (1) Can laser-patterned film deposition scale to <2× tape-winding cost? (2) Can a compact A=4 QI stellarator achieve Q ≥ 5 with published confinement scalings? If both succeed, Renaissance is competitive at 100–150 $/MWh. If either fails, LCOE exceeds 300 $/MWh.

---

## 6. Modeling Confidence

**Rating: Low**

### Data-anchored parameters (40% of LCOE impact):
- Thermal efficiency (48%, ECM 2023)
- Net efficiency (34%, ECM 2023)
- Machine geometry (R=4 m, A=4, B=10 T, NF 2024)
- Blanket TBR and energy multiplication (JNM 2024)
- Availability (92%, inferred from steady-state + liquid wall)

### Speculative parameters (60% of LCOE impact):
- **Magnet system cost (C220103 = $2.26B ± factor 5)**: Dominant. The tape-winding model is inapplicable; the placeholder value has no manufacturing basis. LCOE sensitivity to this account alone is ±300 $/MWh.
- **Liquid metal wall system cost (C220101 = $400M ± 50%)**: Na-cooled fast reactor analogy is rough. The Li-LiH mixture at 25 MW/m² and 10 T has no cost precedent.
- **Plasma confinement quality (Q=∞ target)**: ISS04 extrapolation predicts ~11× shortfall at T=10 keV. The design must rely on higher temperature (20–30 keV) or confinement improvement beyond ISS04 — neither is validated.
- **Recirculating power fraction (p_pump = 380 MW ± 50%)**: Inferred from published net efficiency gap, but no breakdown of parasitic loads is published. Liquid metal pumping at 25 MW/m² could range 300–500 MW; this propagates ±5 $/MWh LCOE uncertainty.

### Dominant source of LCOE uncertainty:
The **laser-patterned HTS film manufacturing cost**. Until production throughput and yield data are published, the magnet cost is unknowable within a factor of 3–10. This single account (C220103) represents ~21% of overnight capital in the nominal model and drives the 99–517 $/MWh LCOE range. No amount of diligence on other parameters will retire this uncertainty — only Renaissance Fusion can publish the data or build the manufacturing line.

Secondary uncertainty is **plasma ignition feasibility**. The Q=∞ claim reduces recirculating power by ~7% vs. Q=5, worth ~15 $/MWh LCOE. But if ignition fails and the plant requires continuous ECRH heating, add $100–200M to C220109 and restore the 15% recirculating fraction, raising LCOE by ~20 $/MWh.

---

## 7. What Would Change My Mind

### Toward more favorable LCOE (upside scenario):

1. **Publication of magnet manufacturing cost data showing film deposition <$100/m² at >1 m²/day throughput** — If Renaissance demonstrates this in a peer-reviewed source or industrial partnership announcement, the magnet cost drops to the 0.3–0.5× tape-winding range, and LCOE falls below 100 $/MWh. This is the single highest-impact disclosure.

2. **Experimental validation of Q ≥ 5 in any compact stellarator (A ≤ 6) at B ≥ 5 T** — If Proxima Fusion, Type One Energy, or an academic group demonstrates burning plasma in a compact QI geometry, Renaissance's Q=∞ claim becomes credible. LCOE impact is modest (~15 $/MWh) but removes the largest physics risk from the concept.

3. **sCO₂ Brayton-Rankine demo plant achieving 46–50% efficiency at 100+ MWe for >1000 hours** — This is on industry roadmaps for 2026–2030. Success would validate the 48% efficiency assumption and retire BOP technology risk, confirming the ~15 $/MWh thermal efficiency advantage.

### Toward less favorable LCOE (downside scenario):

1. **Any peer-reviewed analysis concluding laser-patterned film deposition costs >5× wound tape at production scale** — If REBCO film deposition equipment has intrinsically lower throughput or higher capital cost than tape production lines (due to vacuum chamber size, substrate handling, or yield issues), the magnet cost penalty drives LCOE above 300 $/MWh and the concept becomes uncompetitive.

2. **Experimental data showing liquid Li-LiH MHD pressure drop at 10 T requires >600 MW pumping for 25 MW/m² wall loading** — If the MHD resistance is worse than the current 380 MW estimate (already high), net efficiency drops below 30%, and LCOE rises above 180 $/MWh even in the optimistic magnet-cost scenario.

3. **Failure of any large-scale HTS magnet program to demonstrate >10 T steady-state field for >1 year** — If REBCO degradation, quench risk, or AC loss issues emerge in long-duration operation (a shared risk with CFS, Tokamak Energy, and all HTS concepts), the 20 K operating temperature advantage evaporates, and the concept falls back to 4 K LTS with higher cryogenic parasitic load. Worth ~10–15 $/MWh LCOE penalty.

---

## 8. LCOE Downselect Scoring

### C1: Modularization

**Sub-factor 1: Construction mode classification per CAS account**

| CAS Account | Construction Mode | Score | Justification |
|-------------|------------------|-------|---------------|
| CAS21 (Buildings) | Site-assembled from factory sub-assemblies | 3 | Stellarator reactor hall and bioshield are site-erected from prefab steel/concrete modules. Standard nuclear construction. |
| CAS220101 (First Wall / Liquid Metal Wall) | Factory-manufactured module | 5 | Liquid metal circuit components (pumps, heat exchangers, piping, Pb pebble beds) are factory-assembled packages. The wall itself is a flowing fluid, not a field-erected structure. |
| CAS220102 (Blanket / Shield) | Factory-manufactured module | 5 | Integrated with C220101 as a single liquid metal circuit. VH₂ shield segments are factory-fabricated and bolted in place. |
| CAS220103 (Magnets) | Site-assembled from factory sub-assemblies | 3 | Laser-patterned HTS cylinders are factory-produced, but final 3D stellarator field assembly requires on-site alignment, interconnection, and cryogenic integration. Not fully modular. |
| CAS220105 (Vessel) | Site-assembled from factory sub-assemblies | 3 | Vacuum vessel segments welded on-site. Standard tokamak/stellarator practice. |
| CAS220106 (Primary Heat Transport) | Factory-manufactured module | 5 | Liquid metal pumps, Li-LiH circulation loops, and heat exchangers are skid-mounted factory packages. |
| CAS220107 (Auxiliary Cooling) | Factory-manufactured module | 5 | sCO₂ Brayton-Rankine turbomachinery and heat rejection systems are factory-built modules (industrial sCO₂ standard practice). |
| CAS22 (other) | Site-assembled from factory sub-assemblies | 3 | Diagnostics, power supplies, cryogenics, control systems: mix of factory modules and site integration. |
| CAS23 (Turbine Plant) | Factory-manufactured module | 5 | sCO₂ turbine, generator, and Rankine bottoming cycle are factory-assembled and delivered as integrated power block. |
| CAS24 (Electrical Plant) | Factory-manufactured module | 5 | Switchgear, transformers, and grid connection are standard industrial components. |
| CAS26 (Heat Rejection) | Factory-manufactured module | 5 | Cooling towers or air-cooled condensers are prefabricated and trucked to site. |

Cost-weighted average (using model output CAS22 detail):
- C220101 ($400M) × 5 = 2000
- C220102 ($189M) × 5 = 945
- C220103 ($2262M) × 3 = 6786
- C220105 ($9.3M) × 3 = 28
- C220106 ($34M) × 5 = 170
- C220107 ($106M) × 5 = 530
- CAS22 other ($1353M) × 3 = 4059
- CAS23 ($232M) × 5 = 1160
- CAS24 ($126M) × 5 = 630
- CAS26 ($69M) × 5 = 345

Total = 16653 / 4780M = 3.48

**Sub-factor 2: Module repetition boost**

The liquid metal circulation system uses multiple identical pump/heat exchanger modules (estimated 10–20 units for a 1 GWe plant, though not specified in sources). The sCO₂ power conversion also benefits from multiple turbine stages. However, the magnet system (the largest cost account) is a bespoke 3D array with minimal unit repetition.

Module repetition boost: +0.5 (moderate; liquid metal and BOP modules repeat, but magnet dominates capital cost and is not repetitive).

**C1 score: 3.48 + 0.5 = 3.98, clamped to [1, 5] → 4.0**

**Justification**: The liquid metal wall, blanket, heat transport, and sCO₂ BOP are highly modular (factory-built, bolt-together). This is a genuine architectural advantage over solid-blanket designs with field-erected modules. However, the magnet system (C220103, 21% of capital) requires on-site 3D assembly and integration, pulling the weighted average down to ~3.5. The repetition boost reflects the liquid metal circuit's use of 10+ identical pump/exchanger modules.

---

### C3: Supply Chain Learning

**Sub-factor A: Component learning rates (1-5, cost-weighted)**

| CAS Account | Cost (M$) | Learning Category | Score | Justification |
|-------------|-----------|-------------------|-------|---------------|
| C220101 (Liquid Metal Wall) | 400 | Fusion-specific (no current market) | 2 | Li-LiH flowing walls at 25 MW/m² have no commercial analogue. Learning from Na fast reactors applies but extrapolation is large. |
| C220102 (Blanket/Shield) | 189 | Specialty component (limited supply chain) | 3 | VH₂ outer shield and Pb pebbles are producible, but Li-LiH blanket mixture is fusion-specific. |
| C220103 (Magnets) | 2262 | Fusion-specific (no current market) | 2 | Laser-patterned REBCO film at 1 m diameter has no existing supply chain. REBCO tape market exists but is not directly applicable. |
| C220106 (Heat Transport) | 34 | Industrial component (growing production) | 4 | Liquid metal pumps and heat exchangers exist for Na fast reactors and chemical processing. Fusion-specific tritium barriers add cost but analogue is strong. |
| C220107 (Auxiliary Cooling) | 106 | Industrial component (growing production) | 4 | sCO₂ Brayton turbomachinery is scaling to GW class (Echogen, NET Power, Sandia). Production base is growing. |
| CAS23 (Turbine Plant) | 232 | Industrial component (growing production) | 4 | Same as C220107; sCO₂ combined cycle is on industrial roadmap. |
| CAS21 (Buildings) | 675 | Commodity (established manufacturing) | 5 | Concrete, steel, rebar are global commodities. |
| CAS24 (Electrical) | 126 | Commodity (established manufacturing) | 5 | Switchgear and transformers are mature industrial products. |
| CAS26 (Heat Rejection) | 69 | Commodity (established manufacturing) | 5 | Cooling towers are standard industrial equipment. |
| CAS22 other | 1353 | Mix (specialty + industrial) | 3 | Diagnostics, cryogenics, power supplies: mix of fusion-specific and industrial. |

Cost-weighted average:
(400×2 + 189×3 + 2262×2 + 34×4 + 106×4 + 232×4 + 675×5 + 126×5 + 69×5 + 1353×3) / 5446M = 2.73

**Sub-factor B: Supply chain bottleneck count (1-5)**

Start at 5.0 and subtract penalties:

- **Hard constraint: REBCO film deposition capacity at 1+ m diameter** — No existing production line. This is a greenfield manufacturing challenge. Penalty: −1.0
- **Scaling constraint: Li-6 enrichment for fleet deployment** — Global capacity is ~10 kg/yr (Russia, China, limited Western alternatives). A single 1 GWe plant with 0.33 m Li-LiH blanket requires ~2–5 tonnes Li (mostly Li-7 if non-enriched baseline is used). Fleet scaling requires 10–100× enrichment capacity growth. Penalty: −0.5
- **Scaling constraint: sCO₂ turbomachinery at GW scale** — Current demonstrations are 10 MWe; scaling to 1.5 GWe is underway but not yet achieved. Penalty: −0.5
- **Sole-source dependency: Laser patterning equipment** — Only a handful of vendors (if any) produce the required large-area REBCO deposition and laser ablation tools. Penalty: −0.25

Subtotal: 5.0 − 1.0 − 0.5 − 0.5 − 0.25 = 2.75

**Sub-factor C: External demand pull (1-5)**

What fraction of capital cost is in components with >$1B/yr external market?

- CAS21 (Buildings, $675M): Concrete, steel — global markets >$1T/yr. Counts.
- CAS23 (Turbine Plant, $232M): sCO₂ turbines — external market is emerging (~$500M/yr currently, projected >$5B/yr by 2030 for power + industrial). Counts.
- CAS24 (Electrical, $126M): Switchgear, transformers — global market >$100B/yr. Counts.
- CAS26 (Heat Rejection, $69M): Cooling towers — global market ~$5B/yr. Counts.
- C220106 (Heat Transport, $34M): Liquid metal pumps — niche but >$1B/yr for chemical/nuclear applications. Counts.
- C220107 (Auxiliary Cooling, $106M): Same as CAS23. Counts.

Total external-demand capital: 675 + 232 + 126 + 69 + 34 + 106 = 1242M of 5446M total = 23%

Score: 3 (20–40% range)

**C3 = (2.73 + 2.75 + 3.0) / 3 = 2.83 → 2.8**

**Justification**: The magnet system (largest cost account) has fusion-specific learning (score 2) and a hard manufacturing bottleneck (no film deposition at scale). The liquid metal wall and sCO₂ BOP have industrial analogues (scores 3–4) but are still scaling-constrained. External demand pull is modest (23%) because the two dominant accounts (C220103 magnets, C220101 liquid wall) are fusion-specific. Supply chain maturity is weak.

---

### C4: Plant Complexity

**Sub-factor A: Operational coupling density (1-5)**

- **Liquid metal circulation** — If a primary pump fails, wall heat removal stops, and plasma must be shut down within ~10 seconds to avoid overheating. This is a single-point failure cascade. However, the liquid metal circuit can be designed with N+1 pump redundancy (5–10 pumps in parallel, each handling ~50–100 MW of heat). Partial pump failure degrades power output but does not force immediate shutdown.
- **Plasma-wall MHD coupling** — If the liquid metal flow rate drops, MHD pressure gradients change, potentially affecting plasma edge conditions. This is a modest operational coupling (not catastrophic, but requires active control).
- **sCO₂ Brayton-Rankine balance of plant** — The sCO₂ turbine, heat exchangers, and Rankine bottoming cycle are tightly coupled: sCO₂ loop failure stops power conversion, but does not directly affect plasma. The heat rejection side (liquid metal to sCO₂) can tolerate brief sCO₂ interruptions by dumping heat to auxiliary cooling.
- **HTS magnet cryogenics** — If cryogenic refrigeration fails, magnet temperature rises, Jc degrades, and field weakens over ~hours (not seconds). The stellarator can tolerate slow field ramp-down without disruption (unlike a tokamak). This is low coupling.
- **Tritium processing** — Failure of tritium extraction from the Li-LiH circuit increases in-circuit tritium inventory but does not stop plasma operation on ~day timescales. Moderate coupling.

Overall: The liquid metal circulation is the tightest operational coupling (pump failure → rapid shutdown). However, pump redundancy is straightforward to implement. The stellarator's lack of disruptions and slow thermal time constants provide decoupling buffers. Other subsystems (BOP, cryogenics, tritium) can fail without immediate plasma shutdown.

**Score: 3.5** (Moderate coupling; liquid metal circulation is the dominant cascade path, but N+1 pump redundancy and slow thermal response reduce severity vs. tokamak single-point failures like CS coil or ECRH interruption).

**Sub-factor B: Subsystem count (1-5)**

Count CAS22 sub-accounts >1% of total capital ($109M threshold):

From model output CAS22 detail:
- C220101 (Liquid Wall): $400M (3.7%) ✓
- C220102 (Blanket/Shield): $189M (1.7%) ✓
- C220103 (Magnets): $2262M (20.7%) ✓
- C220106 (Heat Transport): $34M (<1%) —
- C220107 (Auxiliary Cooling): $106M (1.0%) — (borderline; exclude)
- C220108 (Power Supplies): $106M (1.0%) — (borderline; exclude)
- C220110 (Cryogenics): $184M (1.7%) ✓
- C220111 (Diagnostics): $417M (3.8%) ✓
- C220200 (Fuel Handling): $204M (1.9%) ✓
- C220300 (Remote Handling): $226M (2.1%) ✓
- C220700 (Instrumentation): $79M (<1%) —

Count: 7 significant subsystems (C220101, C220102, C220103, C220110, C220111, C220200, C220300)

**Score: 4** (5–7 significant subsystems per framework)

**C4 = (3.5 + 4.0) / 2 = 3.75 → 3.8**

**Justification**: The integrated liquid metal wall reduces subsystem count vs. solid-blanket stellarators (which separate first wall, blanket, coolant into 3–4 distinct systems). The ignited plasma eliminates the heating/current-drive subsystem. However, the liquid metal circulation introduces a tight operational coupling (pump failure → rapid shutdown), partially offset by pump redundancy. The stellarator's intrinsic lack of disruptions and slow thermal time constants provide operational buffers. Complexity is moderate, not low.

---

### C5: Customization Needs

**Sub-factor A: Thermal rejection (1-4)**

The plant uses a large sCO₂ Brayton-Rankine combined cycle at ~1.5 GWe gross thermal input. The Rankine bottoming cycle rejects waste heat via standard cooling towers or air-cooled condensers (same as any thermal power plant). The sCO₂ primary loop is closed-cycle and does not require external cooling beyond the Rankine condenser.

At ~52% total thermal rejection (48% cycle efficiency), the plant rejects ~1.5 GWth to the environment. This is comparable to a 1.5 GWe CCGT plant and requires large cooling towers. Site selection is constrained by cooling water availability or dry-cooling capability.

**Score: 2** (Large cooling towers required; standard thermal cycle)

**Sub-factor B: Fuel safety profile (1-4)**

D-T fuel with full tritium breeding and handling infrastructure.

**Score: 1** (D-T: full tritium handling and breeding infrastructure)

**C5 raw = (2 + 1) / 2 = 1.5**

**C5 scaled = 1 + (1.5 − 1) × (4/3) = 1 + 0.667 = 1.67 → 1.7**

**Justification**: The sCO₂ combined cycle is thermodynamically efficient but still rejects ~52% of fusion power as waste heat, requiring large cooling infrastructure. D-T fuel adds tritium breeding, extraction from Li-LiH, and permeation barriers in heat exchangers. Customization needs are high.

---

### C8: Data Adequacy

**Sub-factor A: Source diversity & independence (1-5)**

- **Independent public-domain sources**: Three peer-reviewed papers in high-quality journals (Nuclear Fusion, J. Nuclear Materials, Energy Conversion and Management). This is unusually strong for a private fusion startup.
- **Company sources with public peer review**: All three primary sources are peer-reviewed external publications, not white papers or preprints.
- **Company publications**: Company website and MT29 abstract provide hardware validation (6 T Helmholtz demo).

**Score: 4** (Mix of independent and company sources with public peer review. Not score 5 because no independent third-party LCOE study or techno-economic analysis exists.)

**Sub-factor B: Reactor design specification (1-5)**

- Machine geometry (R, A, B) and plasma design point (T, Q) are published (NF 2024).
- Blanket radial build, TBR, and neutron energy multiplication are published (JNM 2024).
- Power conversion cycle architecture and efficiency are published (ECM 2023).
- **Gaps**: No divertor design, no plasma confinement time or density, no magnet coil count or dimensions, no full plant layout, no O&M plan, no remote handling scheme.

**Score: 3** (Partial design with key subsystems defined but gaps in integration. The published papers cover physics design point and major subsystems, but not full plant integration or component-level specs.)

**Sub-factor C: LCOE parameter coverage (1-5)**

From gap_report.md:
- Blocking gaps: Capital cost (C220103, C220101, total plant), liquid metal pump power, divertor design, plasma confinement parameters, O&M cost (total: 7 blocking gaps)
- Important gaps: Peak Li-LiH temperature, HTS cylinder count, cryogenic power, component replacement schedule, sCO₂ turbomachinery cost (total: 5+ important gaps)

Blocking gap count: 7

**Score: 2** (5–7 blocking gaps per framework)

**Sub-factor D: Commercialization pathway clarity (1-5)**

- Renaissance Fusion is pre-pilot plant. No published commercialization timeline, funding milestones, or demonstration plant design exists in public sources.
- The company has raised funding (not disclosed in available sources) and is building hardware (MT29 demo), but no public roadmap connects the 6 T Helmholtz demo to a pilot plant or commercial deployment timeline.
- The "economically optimized design point" framing in NF 2024 suggests commercial intent, but no pathway is articulated.

**Score: 2** (Vague or aspirational commercialization narrative. Hardware demonstration exists but no public timeline or milestones.)

**C8 = (4 + 3 + 2 + 2) / 4 = 2.75 → 2.8**

**Justification**: Strong peer-reviewed publication record (unusual for a startup) provides credible physics and subsystem performance data. However, LCOE-critical parameters (magnet cost, pump power, O&M) are absent, and no commercialization pathway is public. Data adequacy is moderate for physics assessment, poor for economic modeling.

---

### C7: Technical Risk Evidence (Risk Matrix)

#### Function 1: Plasma Performance

| Field | Physics Risk | Hardware Risk |
|-------|--------------|---------------|
| **Plant requirement** | n·τ_E ≥ 3.1×10²⁰ m⁻³·s (Lawson ignition criterion at T=10 keV); alternatively achieve Q ≥ 5 at lower confinement if T=20–30 keV | Vacuum vessel, cryostat, and plasma-facing components must survive ≥30 years at 25 MW/m² neutron wall loading and 10 T toroidal field |
| **Best demonstrated** | W7-X: n·τ_E ~ 1–2×10¹⁹ m⁻³·s at T ~ 3 keV, A=10, B=3 T (2018–2023 campaigns). No stellarator has approached burning plasma. | ITER vacuum vessel and cryostat designed for 500 MW fusion power, 5.3 T field; not yet operated. W7-X cryostat operates at 3 T for ~100 plasma pulses per campaign at low neutron flux. |
| **Gap ratio** | ~15× gap in n·τ_E (W7-X at 2×10¹⁹ vs. requirement 3×10²⁰). ISS04 scaling extrapolated to Renaissance geometry predicts ~11× shortfall at T=10 keV. | ~5× wall loading gap (5 MW/m² typical solid-blanket stellarator vs. 25 MW/m²); ~3× field gap (3 T W7-X vs. 10 T); no stellarator vessel has operated with >1 MW/m² neutron flux. |
| **Closure mechanism** | (a) Operate at T=20–30 keV where <σv>/T² is 2–3× higher, reducing n·τ_E requirement; (b) achieve confinement improvement >ISS04 via high-field QI optimization; (c) larger plasma volume (>200 m³) than estimated. | Liquid metal wall is claimed to self-renew and tolerate high heat flux without erosion. RAFM steel vessel and VH₂ shield tolerate 14 MeV neutron damage at fusion-relevant fluence (analogy to ITER/DEMO vessel designs). |
| **Classification** | Binary (if confinement shortfall is severe, Q << 1 and net electricity is impossible without massive external heating) | Degrading (vessel/cryostat damage shortens lifetime or requires early replacement; does not prevent net electricity) |
| **Evidence tier** | **Tier 2** (ISS04 scaling law is empirically validated but extrapolates far beyond W7-X regime; no burning-plasma stellarator exists to validate high-field compact QI confinement). | **Tier 3** (RAFM steel under 14 MeV neutrons tested at FFTF, HFIR to ~10–20 dpa; ITER vessel design qualified for 500 MW fusion via analysis; liquid metal wall operates at 5 MW/m² in NSTX-LiMIT experiments but not 25 MW/m² or steady-state). |

#### Function 2: Driver / Energy Input

| Field | Physics Risk | Hardware Risk |
|-------|--------------|---------------|
| **Plant requirement** | NNBI must deliver sufficient power (estimated 50–100 MW) to heat plasma from startup to ignition threshold (~5 keV → 10+ keV) with ≥60% neutralization efficiency | NNBI beamline, ion source, and power supplies must operate for ~100–500 startup cycles over 30-year plant lifetime; tolerate stellarator port geometry constraints |
| **Best demonstrated** | ITER NNBI design: 1 MeV, 40 A, 60% neutralization efficiency demonstrated in ELISE test facility at ~MW scale (2016–2023). Positive NBI at 500 keV used on JT-60U, LHD. | ITER NNBI ion source and beamline hardware under construction; not yet operated at full ITER spec (1 MeV, 16.5 MW per beamline). |
| **Gap ratio** | ~1× (neutralization efficiency and energy match; power scale is lower for Renaissance startup-only application) | ~10× duty cycle gap (ITER NNBI designed for ~3600 s continuous pulses; Renaissance needs <100 s startup pulses but over 500 cycles). Reliability regime is different. |
| **Closure mechanism** | Scale ITER NNBI technology to lower power (startup only, not continuous operation) and adapt beamline geometry to compact stellarator port access. | Startup-only duty cycle reduces total beam-on time vs. ITER, potentially improving ion source lifetime. |
| **Classification** | Degrading (if NNBI neutralization efficiency is lower, more recirculating power required during startup; does not prevent steady-state operation) | Degrading (beamline component failures extend startup time or reduce availability; does not prevent net electricity once ignited) |
| **Evidence tier** | **Tier 4** (ITER NNBI at 60% neutralization efficiency demonstrated in ELISE at near-regime; extrapolation to startup-only application is straightforward). | **Tier 3** (ITER NNBI hardware in late construction; subscale demonstration at 1 MeV but not full ITER beamline power or pulse length). |

#### Function 3: Instability Control

| Field | Physics Risk | Hardware Risk |
|-------|--------------|---------------|
| **Plant requirement** | Stellarator QI optimization must suppress neoclassical transport and avoid low-order rational surfaces that drive MHD instabilities; maintain β ≤ 5% (3-D MHD limit) | Magnetic diagnostics, plasma control coils (if used), and real-time equilibrium reconstruction must operate at 10 T field environment |
| **Best demonstrated** | W7-X: QI optimization validated, achieved quasi-isodynamic field at β ~ 1–2%, no major MHD events. LHD: operated at β ~ 4% (near 5% limit). | W7-X magnetic diagnostics and control systems operate at 3 T for 30-minute pulses. No stellarator diagnostics have operated in a 10 T neutron environment. |
| **Gap ratio** | ~2.5× field gap (3 T W7-X vs. 10 T Renaissance); ~2× β gap (W7-X at 2% vs. potential operation near 5% limit). Compact A=4 QI has less shape freedom than W7-X A=10. | ~3× field gap for diagnostics (3 T vs. 10 T); diagnostic components must tolerate 14 MeV neutron damage (no stellarator diagnostics have operated in high neutron flux). |
| **Closure mechanism** | High-field QI optimization codes (not published by Renaissance) predict stable operation at β ~ 2–4%; margin below 5% limit. Compact geometry accepted as constraint. | ITER-class radiation-hard diagnostics adapted to stellarator geometry; liquid metal wall may reduce line-of-sight access complexity vs. solid PFCs. |
| **Classification** | Degrading (MHD instabilities or excessive transport degrade confinement → higher heating requirement or lower Q; does not necessarily prevent net electricity) | Degrading (diagnostic failures reduce plasma control quality; increase risk of off-normal operation; do not prevent steady-state at reduced performance) |
| **Evidence tier** | **Tier 4** (W7-X QI validation at 3 T is near-regime for 10 T stellarator; LHD β~4% demonstrates proximity to 5% limit is achievable). | **Tier 3** (ITER diagnostics designed for 5.3 T, high neutron flux but not yet operated; stellarator adaptation is analogue but not demonstrated). |

#### Function 4: Plasma-Wall Interaction

| Field | Physics Risk | Hardware Risk |
|-------|--------------|---------------|
| **Plant requirement** | Plasma edge must tolerate direct contact with flowing Li-LiH surface without confinement degradation; impurity influx (Li, H) must remain <1% of electron density to avoid radiative collapse | Liquid metal wall must flow stably at 25 MW/m² heat flux without boiling, MHD instabilities, or excessive sputtering; liquid metal pumps and containment must survive ≥30 years |
| **Best demonstrated** | NSTX: LiMIT liquid lithium limiter tolerated ~1–5 MW/m² heat flux; reduced edge recycling and improved confinement. TJ-II: liquid lithium experiments showed reduced ELMs. | NSTX-LiMIT: flowing liquid lithium at ~1–5 MW/m² for <10 s pulses. No long-pulse or steady-state liquid metal wall at >10 MW/m². |
| **Gap ratio** | ~5–25× heat flux gap (NSTX at 1–5 MW/m² vs. 25 MW/m² requirement). Li-LiH mixture (solid LiH at room temp, melts at 680°C) is not the same as pure Li used in NSTX. | ~5× heat flux gap; ~1000× pulse length gap (NSTX <10 s vs. steady-state). Liquid metal MHD at 10 T field (Renaissance) vs. <1 T (NSTX) is undemonstrated. |
| **Closure mechanism** | Li-LiH mixture operates at high temperature (>680°C) where LiH is molten; JNM 2024 neutronics analysis validates heat removal and breeding. Plasma edge modeling (unpublished) predicts acceptable impurity influx. | Liquid metal pumps designed for high MHD pressure drop (pressure drop scales with B²·v·L); Pb pebble bed provides neutron multiplication and slows neutron spectrum to reduce Li-6 burnup. |
| **Classification** | Degrading (excessive impurity influx or edge radiation reduces core performance; may require higher heating or lower wall loading; does not necessarily prevent net electricity) | Degrading (pump or flow failures reduce wall loading capability → derate power output; early replacement increases O&M cost) |
| **Evidence tier** | **Tier 2** (NSTX-LiMIT is a subscale analogue at 5× lower heat flux and different field regime; Li-LiH mixture and high-field MHD are undemonstrated experimentally). | **Tier 2** (Na-cooled fast reactor liquid metal pumps operate at similar temperatures but ~1000× lower magnetic field; fusion-relevant MHD flow at 10 T is purely analytical). |

#### Function 5: Neutron/Particle Handling

| Field | Physics Risk | Hardware Risk |
|-------|--------------|---------------|
| **Plant requirement** | 14 MeV D-T neutrons must deposit 99.99% of energy in blanket/shield; activation of RAFM structure must decay to hands-on maintenance levels <100 years; He production in steel must not cause embrittlement before 30-year lifetime | RAFM steel vessel and shield structure must tolerate ~20–30 dpa (displacement per atom) over 30 years at 25 MW/m² neutron wall loading; VH₂ outer shield must reduce dose to magnets to <10⁻⁴ dpa/yr |
| **Best demonstrated** | MCNP neutronics for D-T stellarators calculated in ARIES-CS (similar geometry): TBR ~ 1.1–1.2, 99%+ neutron absorption validated. He production in RAFM steel measured in FFTF, HFIR fission reactors. | RAFM steel (EUROFER, F82H) irradiated to 10–20 dpa in HFIR, FFTF fission test reactors; 14 MeV neutron data from RTNS-II, FNS (Japan) at lower fluence. ITER vessel designed for ~3 dpa over 20 years. |
| **Gap ratio** | ~1.5× TBR gap (ARIES-CS analytical TBR ~ 1.1 vs. Renaissance JNM 2024 claim of 1.60). Neutron energy multiplication (fm=1.07 per JNM 2024) is within ARIES-CS range. | ~2–3× dpa gap (RAFM tested to 10–20 dpa in fission reactors; Renaissance requires 20–30 dpa in 14 MeV spectrum). 14 MeV He production rate is ~10× higher than fission spectrum (gas bubble embrittlement risk). |
| **Closure mechanism** | JNM 2024 neutronics analysis with MCNP validates TBR=1.60, 99.99% absorption, and radial build. Pb pebble layer provides neutron multiplication. | RAFM steel qualified to 20 dpa in DEMO studies; extrapolate to 30 dpa at Renaissance wall loading via scaling laws. VH₂ shield thickness (50 cm) designed to attenuate fast neutrons to <10⁻⁴ dpa/yr at magnets (MCNP). |
| **Classification** | Binary (TBR < 1.0 prevents tritium self-sufficiency → concept cannot scale to fleet without external T supply) | Degrading (early vessel failure or excessive activation shortens lifetime or increases replacement cost; does not prevent initial operation) |
| **Evidence tier** | **Tier 2** (JNM 2024 TBR=1.60 is MCNP calculation, not experimental validation; ARIES-CS provides analogue but not at identical geometry or wall loading). | **Tier 3** (RAFM steel tested to ~10–20 dpa in fission reactors; ITER vessel design extends to ~3 dpa via analysis; Renaissance 20–30 dpa is subscale extrapolation). |

#### Function 6: Fuel Cycle Closure

| Field | Physics Risk | Hardware Risk |
|-------|--------------|---------------|
| **Plant requirement** | TBR ≥ 1.05 (net breeding after losses); tritium extraction from liquid Li-LiH must achieve ≥95% recovery efficiency; tritium permeation through sCO₂ heat exchangers must be <0.1% of inventory per day | Tritium extraction plant must process ~1–2 kg/day tritium from flowing Li-LiH circuit; permeation barriers in Li-LiH-to-sCO₂ heat exchangers must limit T loss to <1 Ci/day; tritium inventory in Li circuit must remain <10 kg for safety |
| **Best demonstrated** | ITER tritium plant design: TBR ~ 1.0 (with breeding blanket); tritium extraction from Pb-17Li in EU WCLL mockups at lab scale (~g/day). | EU WCLL blanket: tritium extraction from Pb-17Li demonstrated in TRIEX-II, LIFUS-6 loops at ~100 g/day scale. Permeation barriers (aluminized steel, Al₂O₃ coatings) tested in lab at <650°C. |
| **Gap ratio** | ~10–100× extraction rate gap (WCLL lab demonstrations at 100 g/day vs. 1–2 kg/day for 1 GWe plant). Li-LiH extraction chemistry is different from Pb-17Li. | ~10–100× extraction scale gap; permeation barrier effectiveness at Li-LiH temperatures (>680°C) is undemonstrated (EU tests are for Pb-17Li at <650°C). |
| **Closure mechanism** | Li-6 enrichment (optional) increases TBR margin; baseline non-enriched Li-LiH achieves TBR=1.60 per JNM 2024, providing ~55% margin above requirement. Tritium extraction via molten salt extraction or getter beds (unpublished design). | Scale EU WCLL tritium extraction technology to Li-LiH chemistry and higher throughput; permeation barriers on heat exchanger tubes (technology exists but not demonstrated at required temperature and scale). |
| **Classification** | Binary (tritium extraction failure or TBR < 1.0 prevents fuel cycle closure → external T purchase required, limiting fleet scale to global T inventory / startup requirements) | Binary (inability to limit tritium permeation to sCO₂ side creates environmental release and regulatory failure) |
| **Evidence tier** | **Tier 2** (TBR=1.60 is MCNP analytical result; tritium extraction from liquid Li at kg/day scale is undemonstrated experimentally, though lab-scale Pb-17Li extraction exists). | **Tier 2** (EU WCLL tritium extraction is subscale analogue; permeation barriers tested in lab but not at Li-LiH fusion-plant conditions). |

#### Function 7: Power Conversion & BOP

| Field | Physics Risk | Hardware Risk |
|-------|--------------|---------------|
| **Plant requirement** | N/A (power conversion is purely engineering; no plasma physics coupling) | sCO₂ Brayton-Rankine combined cycle must achieve 48% thermal efficiency at ~1.5 GWth input; Li-LiH-to-sCO₂ heat exchangers must transfer heat at >600°C without tritium permeation or fouling; sCO₂ turbomachinery must operate for ≥30 years with availability >95% |
| **Best demonstrated** | N/A | sCO₂ Brayton cycle demonstrated at 10 MWe scale (Sandia, Echogen, SwRI) at 45–47% efficiency for ~1000 hours. Combined Brayton-Rankine is conceptual; Rankine bottoming cycle is mature. Li-to-sCO₂ heat exchangers: not demonstrated (Na-to-steam HX in EBR-II, Phenix is closest analogue). |
| **Gap ratio** | N/A | ~150× power scale gap (10 MWe demo vs. 1500 MWe gross); ~10× duration gap (1000 hours demo vs. 30-year lifetime); heat exchanger tritium permeation barriers undemonstrated at Li-LiH chemistry and temperature. |
| **Closure mechanism** | N/A | Scale sCO₂ turbomachinery to GW class using industrial gas turbine design principles; combined Brayton-Rankine optimized via genetic algorithm (ECM 2023). Heat exchanger tritium barriers from EU WCLL/HCLL programs adapted to sCO₂ working fluid. |
| **Classification** | N/A | Degrading (sCO₂ turbine failure or efficiency shortfall reduces net output or increases O&M cost; does not prevent net electricity at reduced efficiency if fallback to steam Rankine is possible) |
| **Evidence tier** | N/A | **Tier 3** (sCO₂ Brayton demonstrated at 10 MWe, ~45% efficiency; subscale but in the correct efficiency regime. Combined Brayton-Rankine is design study. Li-LiH-to-sCO₂ HX is analogue to Na-to-steam in fast reactors but different chemistry). |

---

### Function-level means (F1–F7)

| Function | Physics Tier | Hardware Tier | Mean (before heritage) | Heritage Floor (D-T stellarator) | Final F_n |
|----------|--------------|---------------|------------------------|----------------------------------|-----------|
| F1 (Plasma Performance) | 2 | 3 | 2.5 | 4.0 | **4.0** |
| F2 (Driver / Energy Input) | 4 | 3 | 3.5 | 4.0 | **4.0** |
| F3 (Instability Control) | 4 | 3 | 3.5 | 4.0 | **4.0** |
| F4 (Plasma-Wall Interaction) | 2 | 2 | 2.0 | 4.0 | **4.0** |
| F5 (Neutron/Particle Handling) | 2 | 3 | 2.5 | 4.0 | **4.0** |
| F6 (Fuel Cycle Closure) | 2 | 2 | 2.0 | 4.0 | **4.0** |
| F7 (Power Conversion & BOP) | N/A | 3 | 3.0 | 4.0 | **4.0** |

**Binary risks** (all functions):
- TBR < 1.0 (F5 physics; mandatory binary per framework)
- Tritium extraction failure from Li-LiH circuit (F6 physics; mandatory binary per framework)
- Tritium permeation through sCO₂ heat exchangers exceeds regulatory limits (F6 hardware; mandatory binary per framework)
- Plasma confinement shortfall prevents ignition and external heating cost exceeds economic viability (F1 physics; binary classification due to Q=∞ target — if n·τ_E is ~11× below Lawson threshold and cannot be closed via T increase or confinement improvement, concept fails to achieve net electricity at competitive cost)

**Heritage credit applied**: All F1–F7 scores are floored at 4.0 per stellarator-lineage D-T heritage (W7-X, LHD, TJ-II). Renaissance Fusion's design inherits decades of stellarator QI optimization, D-T tokamak neutronics (ITER vessel, blanket), and thermal-cycle BOP integration. The undemonstrated elements (laser-patterned HTS, liquid metal wall at 25 MW/m², Q=∞ compact QI plasma) are architectural innovations on top of this heritage base, not greenfield development.

---

### YAML Scores Block

```yaml
---
scores:
  C1: 4.0
  C3: 2.8
  C4: 3.8
  C5: 1.7
  C8: 2.8
  F1: 4.0
  F2: 4.0
  F3: 4.0
  F4: 4.0
  F5: 4.0
  F6: 4.0
  F7: 4.0
  binary_risks:
    - "TBR < 1.0 (F5 physics; mandatory binary per framework)"
    - "Tritium extraction failure from Li-LiH circuit (F6 physics; mandatory binary per framework)"
    - "Tritium permeation through sCO2 heat exchangers exceeds regulatory limits (F6 hardware; mandatory binary per framework)"
    - "Plasma confinement shortfall prevents ignition (Q=∞ target); if n·τ_E ~11× below Lawson threshold cannot be closed via higher T or confinement improvement, concept fails to achieve net electricity at competitive cost (F1 physics; binary due to ignition dependency)"
---
```
