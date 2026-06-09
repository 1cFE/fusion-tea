---
ID: 05-planar-coil-stellarator
Concept: Planar-Coil Stellarator (Thea Energy)
Company: Thea Energy
Type: synthesis
Status: draft
Created: 2026-06-08
---

# Editorial Synthesis: Planar-Coil Stellarator (Thea Energy)

## 1. Executive Summary

- **Most important risk**: Zero published cost data — the Helios paper is a 200-page engineering masterwork with DOE certification, but it contains no capital cost breakdown, no LCOE projection, and no subsystem dollar figures. All costing relies entirely on library defaults.
- **Most important advantage**: Planar coil manufacturing simplicity is a genuine stellarator breakthrough — 324 identical shaping coils wound flat in tension, plus software-corrected field errors, eliminates the NCSX/W7-X nightmare of precision-fabricated 3D coil geometries. If the cost claim is real, this retires stellarators' historic Achilles' heel.
- **LCOE ballpark**: 241 $/MWh at 1 GWe NOAK (model output) — roughly 5× conventional fission and ~50% higher than the HTS compact tokamak (162 $/MWh). This is library-only costing with zero overrides; the true figure is unknowable without Thea publishing cost data.
- **Confidence verdict**: Low — physics and engineering documentation is exceptional (DOE-certified, gyrokinetic-verified, experimental prototype validated), but economic viability is unmeasurable. The concept could be 30% cheaper than modeled (if planar coils are as cheap as claimed) or 50% more expensive (if V-4Cr-4Ti and Li-6 supply chains collapse).

## 2. What Matters Most for LCOE

Ranked by LCOE impact potential from the model and gap analysis:

### 2.1 Magnet Cost (C220103: $3,098M library default, dominates capital)
- **Assumed value**: $3,098M for 336 HTS planar coils (12 encircling at up to 50 kA + 324 shaping at 150 A nominal), all REBCO at 20 T peak field, computed from library defaults using R₀ = 8 m and B = 6 T
- **Source**: None — Helios paper provides no REBCO tape quantity, no coil mass, no dollar cost. Library back-solves from geometry.
- **Sensitivity**: C220103 is 23% of 1 GWe overnight capital (3,098 $/kW vs. 13,307 $/kW total CAS22). A ±40% swing ($1,860M – $4,340M) moves LCOE by ±20 $/MWh.
- **What would flip the conclusion**: If Thea's manufacturing claim is validated — all 324 shaping coils are the same double-pancake geometry, wound in tension with COTS current supplies at 150 A, takt time 1 coil/day demonstrated in Canis — and total magnet cost comes in at <$2B NOAK, LCOE drops to ~200 $/MWh and stellarators become cost-competitive with tokamaks. Conversely, if 20 T field-on-conductor at reactor scale requires custom SMI architecture that doesn't mass-produce, and the true magnet account is $5–6B (comparable to ARC's $4.6B structural-steel cage), LCOE exceeds 280 $/MWh and the concept is dead on capital cost.

### 2.2 First Wall Material Maturity (V-4Cr-4Ti: 15-year lifetime vs. EUROFER: 7-year)
- **Assumed value**: V-4Cr-4Ti first wall with 15 full-power-year neutron damage tolerance, enabling a 2-year (84-day biennial) maintenance cycle and 88% capacity factor
- **Source**: thea-energy-helios-arxiv-2512-08027.md §4.2 — explicitly acknowledges "immature supply chain" and "high affinity for hydrogenic species" as risks
- **Sensitivity**: If V-4Cr-4Ti proves unqualifiable at multi-hundred-tonne scale (no industrial supplier exists), Helios falls back to EUROFER97 with ~7 FPY lifetime. This halves the replacement interval from 15 years → 7 years, increases outage frequency, and drops capacity factor from 88% → ~75%. At 75% CF, LCOE rises from 241 → ~285 $/MWh.
- **What would flip the conclusion**: A qualified V-4Cr-4Ti industrial supplier demonstrating multi-tonne production at <$50/kg with validated 15-year irradiation performance would confirm the 88% CF target and lock in the 241 $/MWh baseline. Alternatively, if advanced tungsten-alloy first walls (refractory alloys with 20+ FPY lifetime) emerge from the materials-science pipeline and can replace V-4Cr-4Ti, capacity factor could rise to 92% and LCOE drop to ~220 $/MWh. Failure to qualify V-4Cr-4Ti *and* inability to retrofit EUROFER97 (due to blanket integration constraints) would retire the design.

### 2.3 Confinement Validation (H_ISS04 = 1.4 vs. 1.2)
- **Assumed value**: ISS04 confinement enhancement factor H_ISS04 = 1.4, claimed as "achieved in W7-X"; gyrokinetic verification yields 1.33
- **Source**: thea-energy-helios-arxiv-2512-08027.md §2 Table 1 and §3.5
- **Sensitivity**: Helios operates ignited (958 MW fusion with 1 MW ECRH steady-state). If H_ISS04 falls to 1.2 (a 15% confinement degradation), auxiliary heating must increase to ~15–20 MW to sustain ignition, raising recirculating power from ~48 MW to ~70 MW. Net output drops from 390 MWe → ~350 MWe at fixed fusion power, increasing $/kWe by 11% and LCOE from 241 → ~270 $/MWh.
- **What would flip the conclusion**: Eos first plasma (~2030) achieving H_ISS04 ≥ 1.4 in a QA stellarator at intermediate scale (R ~ 4 m) would retire the confinement extrapolation risk and confirm the Helios ignition assumption. Conversely, if no QA stellarator achieves H_ISS04 > 1.3 at any scale, Helios would need to redesign for higher auxiliary power (larger gyrotron array, higher recirculating load) — not a concept-killer but a ~10% LCOE penalty.

### 2.4 Li-6 Enrichment and Pb-17Li Inventory (CAS27: $18.9M library default)
- **Assumed value**: Library default CAS27 ($18.9M at 1 GWe, negligible) — but Helios uses 65% Li-6 enrichment in a uniform 50 cm Pb-17Li blanket, implying hundreds of tonnes of enriched lithium at an industrial scale that doesn't currently exist
- **Source**: thea-energy-helios-arxiv-2512-08027.md §4.3 (TBR = 1.3 with 65% Li-6) — no mass or cost published
- **Sensitivity**: Global Li-6 enrichment is supply-constrained (Russia/China mercury processes, Western alternatives nascent). If enriched Li-6 at 65% costs $500/g (vs. natural lithium ~$10/kg), and Helios needs 50–100 tonnes for initial fill, CAS27 balloons to $25–50M per unit. At 1 GWe NOAK (n_mod ~ 2.6), this adds ~$130M to overnight capital — a 6 $/kW penalty and +2 $/MWh to LCOE. Not decisive, but non-negligible.
- **What would flip the conclusion**: Development of a Western industrial Li-6 enrichment supply chain (e.g., via laser isotope separation or plasma separation) at <$100/g cost and >10 t/yr capacity would retire this risk entirely. Conversely, if geopolitical access to Russian/Chinese enrichment is cut off and no alternative scales, Li-6 becomes a bottleneck that gates Helios deployment regardless of LCOE — same supply-chain stranglehold as the ARC FLiBe/beryllium problem.

### 2.5 Capacity Factor (88% assumed vs. 75–80% tokamak baseline)
- **Assumed value**: 88% (library default for stellarators), derived from one 84-day planned outage every two years
- **Source**: thea-energy-helios-arxiv-2512-08027.md §4.5 — sector-based maintenance with 15-year first-wall lifetime enables biennial schedule
- **Sensitivity**: Capacity factor is always a first-order LCOE lever. A 10-point drop (88% → 78%) increases LCOE by ~13% (241 → ~272 $/MWh). The 88% claim depends on both the 15-year V-4Cr-4Ti lifetime (see 2.2) *and* the sector-based remote handling working as designed (undemonstrated in any stellarator).
- **What would flip the conclusion**: If the sector removal scheme proves faster than tokamak blanket segment extraction (Helios claims overhead crane lift vs. ITER's serial port-based handling), and the 15-year first-wall lifetime is validated, 88% CF is achievable and the LCOE baseline holds. If sector handling encounters unanticipated integration issues (shaping coil removal, cooling disconnects, blanket sealing) and outages stretch from 84 days → 120 days, capacity factor drops to ~82% and LCOE rises to ~260 $/MWh.

## 3. Risk Verdicts

### 3.1 Planar Coil Manufacturing Cost (Impact: Critical)
- **Verdict**: Genuinely uncertain
- **Rationale**: The manufacturing claim — 324 identical shaping coils wound flat in tension, relaxed tolerances via software field correction, takt time 1 double-pancake/day demonstrated in Canis — is qualitatively compelling and addresses stellarators' historic cost disease (NCSX canceled mid-manufacturing, W7-X coils took decades). But Canis operated at ~3 T field-on-conductor, not 20 T; the SMI partially-insulated architecture is Thea-specific and unproven at production volume; and zero cost data is published.
- **What would retire this risk**: Completion of the Eos magnet system (12 encircling + ~80 shaping coils at intermediate scale) on-budget and on-schedule, with published cost per coil and validated field accuracy. If Eos coils come in at <$5M/coil average (vs. tens-of-millions for W7-X modular coils), the cost revolution is real. If Eos coils overshoot $15M/coil, the planar advantage evaporates.

### 3.2 V-4Cr-4Ti First Wall Supply Chain (Impact: High)
- **Verdict**: Unlikely resolvable in first generation
- **Rationale**: Nuclear-grade V-4Cr-4Ti has never been produced at the multi-hundred-tonne scale needed for a single reactor. The alloy requires controlled impurities (O, N, C, Si <500 wppm) to maintain post-irradiation ductility, and global vanadium production (~100k t/yr) is concentrated in China/Russia/South Africa with no fusion-qualified supply chain. Helios explicitly acknowledges this as a risk and names EUROFER97 as the fallback.
- **What would retire this risk**: A qualified Western industrial V-4Cr-4Ti supplier emerging in the 2025–2035 timeframe with demonstrated >10 t/yr capacity and validated irradiation testing to 150 dpa. This is a 10–15 year materials-development program, not a near-term unlock. More plausibly, Helios Gen-1 uses EUROFER97 (7-year lifetime, 75% CF, +18% LCOE penalty), and V-4Cr-4Ti is reserved for Gen-2+ once the supply chain matures.

### 3.3 QA Stellarator Physics Validation at Reactor Scale (Impact: Moderate)
- **Verdict**: Likely resolvable
- **Rationale**: Quasi-axisymmetric stellarator physics is validated at small scale (HSX) and extensively simulated with state-of-the-art codes (DESC for equilibrium, TERPSICHORE/M3D-C1 for MHD, STELLOPT/BEAMS3D for fast ions, GX gyrokinetic for transport). Helios's gyrokinetic verification yielding H_ISS04 = 1.33 (vs. assumed 1.4) is close enough to claim the confinement target is credible. The 2.7% volume-averaged beta is conservative relative to ARIES-CS (~5%).
- **What would retire this risk**: Eos first plasma achieving H_ISS04 ≥ 1.3 and demonstrating QA transport and MHD stability at intermediate scale. This is a 2030-era milestone. If Eos hits its targets, the physics extrapolation to Helios is low-risk. If Eos fails to reach Q > 0.1 or exhibits unexpected transport degradation, the Helios physics basis is suspect.

### 3.4 Tokamak-Like X-Point Divertor in a Stellarator (Impact: Moderate)
- **Verdict**: Genuinely uncertain
- **Rationale**: No experimental stellarator has ever implemented a tokamak-like continuous X-point divertor. The Helios design claims 10× better gas compression than island divertors and leverages decades of tokamak divertor R&D, but this is entirely on paper. Heat flux management to 10 MW/m² requires "some combination of radiative impurity seeding, detachment, enhanced core radiation, or finely contoured targets" — i.e., the same divertor-physics challenges tokamaks face, now imported into stellarator geometry.
- **What would retire this risk**: Successful X-point divertor operation in Eos with demonstrated 10 MW/m² steady-state heat flux and <10% core power radiated. If the X-point divertor works as simulated, Helios inherits a mature solution. If it fails (excessive impurity contamination, inability to achieve detachment in QA geometry), Helios must fall back to island divertors (lower pumping efficiency, likely higher tritium inventory, possible vacuum system cost penalty).

### 3.5 Sector-Based Remote Maintenance in a Stellarator (Impact: Moderate-High)
- **Verdict**: Likely resolvable
- **Rationale**: Tokamak-inspired sector removal is conceptually simpler than ARIES-CS's port-based extraction of hundreds of components, and the design avoids W7-X's close-fitted modular coils by maintaining 1.2 m plasma-coil distance. The overhead crane lift scheme is plausible. However, no stellarator has performed sector-based maintenance, and the integration challenge — shaping coil removal, helium cooling disconnects, Pb-17Li drain, sector re-alignment to <1 mm after reinsertion — is non-trivial.
- **What would retire this risk**: A full-scale mockup of the sector removal sequence (or successful sector swap in Eos) demonstrating <84-day turnaround with <$20M labor cost. If the sector scheme works, 88% CF is credible. If sector removal proves slower than blanket segment extraction in tokamaks, the stellarator maintenance advantage evaporates.

### 3.6 Tritium Breeding with 65% Li-6 Enrichment (Impact: Moderate)
- **Verdict**: Likely resolvable
- **Rationale**: TBR = 1.3 (idealized) with TMAP8 fuel-cycle modeling showing TBR > 1.15 sufficient for self-sustaining operation is a comfortable margin. The uniform 50 cm blanket geometry is the simplest breeding configuration in the stellarator corpus (vs. ARIES-CS's non-uniform blanket with ports and penetrations). The DCLL Pb-17Li blanket is EU-DEMO heritage, not exotic.
- **What would retire this risk**: Validation of the homogenized TBR = 1.3 figure with a heterogeneous neutronics model including all penetrations, diagnostics ports, and maintenance access cutouts. If realistic TBR remains >1.2, self-sufficiency is assured. The bigger risk is Li-6 enrichment supply (see 2.4), not breeding physics.

## 4. Structural Advantages and Disadvantages

### Advantages (relative to conventional D-T tokamak baseline)

1. **Eliminates ~20–30% of stellarator magnet fabrication cost** (vs. 3D modular coils) by using planar coils with relaxed mechanical tolerances and software-corrected field errors. W7-X non-planar coils required sub-mm precision over 3.5 m span and took 10+ years to manufacture; Helios shaping coils are all identical pancakes wound in tension at 1 coil/day takt. This is a genuine stellarator manufacturing breakthrough if validated at scale.

2. **Uniform radial build** (1.2 m minimum plasma-coil distance, enabled by planar coil flexibility) allows a symmetric 50 cm blanket with no port-driven non-uniformity. This avoids the ARIES-CS blanket complexity (non-uniform thickness, tortuous Pb-17Li flow paths) and simplifies neutronics, thermal-hydraulics, and tritium extraction. Cost direction: moderate advantage in blanket fabrication and reduced engineering hours.

3. **Steady-state operation** (essentially ignited: 958 MW fusion with 1 MW ECRH) eliminates pulsed-operation thermal storage and cyclic stress on first wall/divertor. Compared to ARC's pulse/dwell cycle requiring molten-salt ESS buffer, Helios avoids a $50–100M BOP capital item. The 2.5 MW auxiliary heating budget is trivially small (vs. 38.6 MW for ARC, 73 MW for SPARC).

4. **No disruptions** (stellarators are intrinsically disruption-free) eliminates the ITER/tokamak disruption-mitigation R&D burden and allows thinner first-wall design without disruption-induced thermal-shock margin. This is a reliability and uptime advantage but does not materially reduce capital cost (first-wall cost is dominated by neutron shielding, not disruption tolerance).

### Disadvantages (cost additions vs. baseline)

1. **336 coils with individual power supplies and control systems** (12 encircling + 324 shaping) add electrical complexity and control-software overhead that a tokamak's ~18 TF + 6 PF coils avoids. The shaping coil supplies use "inexpensive COTS relays" due to 150 A nominal current, but the *integration* cost — 324 independent current channels, real-time feedback control to 0.5% RMS field error, cryogenic feedthroughs for each coil — is plausibly $50–100M (C220107 library default is $40.9M at 1 GWe, likely underestimated).

2. **V-4Cr-4Ti supply-chain risk** exposes Helios to a material that doesn't exist at industrial scale and may never mature. If the fallback to EUROFER97 is forced, capacity factor drops 13 points (88% → 75%) and LCOE rises 18% (241 → 285 $/MWh). This is a stellarator-specific penalty (tokamaks can use EUROFER or tungsten with established suppliers).

3. **Li-6 enrichment at 65%** (vs. natural lithium 7.5% Li-6 or modest 20–30% enrichment in some tokamak designs) creates a geopolitical supply dependency and adds $50–100M to initial inventory cost (see 2.4). The 65% target is driven by the 50 cm blanket thickness constraint; a thicker blanket could relax enrichment but would require moving coils outward (larger machine, higher magnet cost).

4. **Unproven X-point divertor in stellarator geometry** carries tokamak-level divertor-physics risk (detachment, impurity seeding, heat flux asymmetries) without the benefit of 40 years of tokamak divertor experimental data. If the X-point concept fails, Helios must retrofit island divertors — a major redesign that could add 1–2 years to schedule and $100–200M to capital cost.

5. **No published cost data** means all economic analysis is library-only. This is the largest disadvantage in *modeling confidence*, not in actual system cost. Thea may possess internal cost estimates that are 30% lower than the model (if planar coils are as cheap as claimed); alternatively, the true cost may be 50% higher (if REBCO tape quantity is enormous and V-4Cr-4Ti doesn't scale). We have no way to know.

## 5. Cross-Concept Positioning

### Within the stellarator family

Helios sits at the **planar-coil, quasi-axisymmetric, HTS, sector-maintenance** corner of the stellarator landscape. Its nearest neighbors are:

**09-qi-stellarator-hts (Proxima Fusion / Stellaris)**: QI vs. QA is the fundamental physics fork. QI (W7-X heritage) has stronger experimental validation but requires 3D non-planar coils with close plasma-coil spacing. QA (HSX heritage, tokamak-like transport) enables planar coils and tokamak-like divertors but is unvalidated at reactor scale. The cost trade: Helios's planar coil manufacturing simplicity vs. Proxima's proven QI confinement physics. Direction: *divergent risk profiles*, not a clear winner — Helios bets on manufacturing, Proxima bets on physics maturity.

**10-large-scale-stellarator (Gauss Fusion)**: If Gauss pursues W7-X-class 3D modular coils (likely LTS or LTS+HTS), the dominant delta is **C220103 magnet manufacturing** — Helios's planar mass-production vs. Gauss's precision-3D heritage. Helios wins on manufacturing (plausibly $2–3B magnet account vs. $4–5B for 3D coils), but Gauss wins on physics validation (W7-X lineage vs. untested QA). LCOE direction: Helios potentially 15–25% cheaper if planar coil cost claim is validated.

**20b-renaissance-fusion (laser-patterned HTS film)**: Both claim stellarator coil manufacturing disruption via radically different methods. Renaissance eliminates tape winding entirely (laser-deposits film on cylindrical substrates); Helios simplifies winding to planar geometry. Incomparable cost structures — Renaissance's method is TRL 2–3 lab-only, Helios's is TRL 4–5 with Canis prototype. Helios is closer to commercial readiness but with unknown cost; Renaissance is further from deployment but potentially cheaper per ampere-meter if the deposition process scales.

**36-helical-coil-stellarator (Helical Fusion / HESTIA)**: Helical coils (LHD heritage) are topologically simpler than QA/QI modular coils — one continuous helical winding path instead of N discrete coils — but suffer higher energetic particle losses historically. Cost delta is concentrated in **coil count and control complexity**: Helios's 336 coils with real-time feedback vs. HESTIA's 2–4 continuous helical windings with simpler power supplies. Helios carries higher control-software cost; HESTIA carries higher structural support cost (helical coils need complex 3D bucking). Physics direction: Helios's QA optimization claims better alpha confinement (smaller plasma volume for same net power, magnet advantage).

### The stellarator manufacturing paradox

Stellarators promise **inherent steady-state operation** and **no disruptions** — advantages tokamaks cannot match without auxiliary current drive or active disruption mitigation. But stellarators have historically been strangled by **3D coil manufacturing cost**. Helios's planar coil architecture directly attacks this cost disease. If the attack succeeds (Eos delivers magnet system <$500M for ~200 MWe-scale), stellarators become cost-competitive with tokamaks on capital $/kWe. If it fails (planar coils at 20 T prove as expensive as 3D coils), stellarators remain a niche research path.

The modeled 1 GWe NOAK LCOE of 241 $/MWh is **library-only costing** with zero Thea-specific overrides. This is 49% higher than the HTS compact tokamak (162 $/MWh) but uses identical stellarator cost defaults as ARIES-CS, W7-X, etc. — i.e., it prices Helios as if planar coils are no cheaper than 3D modular coils. If Thea's cost claim is real, the true LCOE is plausibly 180–200 $/MWh (stellarator-tokamak parity). If the claim is illusory, the true LCOE is 250–300 $/MWh (stellarators remain uncompetitive).

## 6. Modeling Confidence

**Rating**: Low

### Data-anchored parameters (11 / 15 major inputs)
- Plasma geometry (R₀ = 8 m, a = 1.8 m, A = 4.5, V = 500 m³): high confidence, DOE-certified design point
- Magnetic field (B₀ = 6 T, B_peak = 20 T): high confidence, REBCO specification
- Fusion power (958 MW): high confidence, back-solved from net electric 390 MWe + thermal efficiency 40.2%
- Thermal efficiency (40.2% Rankine at 635°C): high confidence, published power flow Sankey
- Confinement (H_ISS04 = 1.4 target, 1.33 gyrokinetic): medium-high confidence, conservative vs. ARIES-CS but unvalidated at QA reactor scale
- Auxiliary heating (2.5 MW wallplug): high confidence, essentially ignited operation
- TBR (1.3 idealized, >1.15 required): medium-high confidence, MCNP-derived but homogenized
- Beta (2.7% volume-averaged): high confidence, conservative relative to equilibrium limits
- Capacity factor (88%): medium confidence, depends on undemonstrated sector maintenance and V-4Cr-4Ti lifetime
- Coil count (336 total): high confidence, design specification
- First wall material (V-4Cr-4Ti, 15 FPY): low-medium confidence, acknowledged immature supply chain

### Speculative / default parameters (4 / 15 major inputs)
- Magnet cost ($3,098M library default): **low confidence** — zero published REBCO tape quantity, zero dollar figures; plausible range $1.5–6B depending on whether planar coil claim is real
- Divertor cost ($58.8M library default): **low confidence** — X-point divertor in stellarator is paper-only; plausible 2× upside if tokamak divertor experience doesn't transfer
- Li-6 enrichment inventory (CAS27 library default $18.9M): **low-medium confidence** — no published Pb-17Li mass; 65% enrichment at scale is supply-constrained
- O&M cost (library default): **medium confidence** — no Helios-specific staffing or scheduled replacement cost published

### Dominant source of LCOE uncertainty

**Magnet cost**, driven by unpublished REBCO tape quantity and unvalidated planar coil manufacturing cost. The C220103 account is $3.1B (23% of 1 GWe overnight capital) in the model, but the true cost is bounded only by physical plausibility: lower bound ~$1.5B (if all 324 shaping coils cost <$5M each and encircling coils are $50M each, optimistic learning), upper bound ~$6B (if 20 T SMI architecture doesn't scale and Helios magnets cost as much as W7-X per ampere-meter). A $3B swing in C220103 moves LCOE from 180 → 300 $/MWh.

The second-largest uncertainty is **V-4Cr-4Ti first wall maturity**, which gates capacity factor (88% vs. 75%, a 44 $/MWh LCOE swing). But this is a known risk with a known fallback (EUROFER97); the magnet cost is an unknown risk with no published fallback.

## 7. What Would Change My Mind

### Evidence that would materially lower LCOE estimate (to ~180 $/MWh or below)

1. **Eos magnet system delivered at <$500M total** (implying <$5M average per coil at intermediate scale), *and* Eos achieves H_ISS04 ≥ 1.3 with demonstrated X-point divertor heat flux management to 10 MW/m², *and* a qualified V-4Cr-4Ti supplier emerges with >10 t/yr capacity. This triple validation — manufacturing cost, physics, and materials — would confirm the planar coil revolution is real, retire the confinement and divertor risks, and lock in 88% capacity factor. LCOE would drop from 241 → ~180 $/MWh, making stellarators cost-competitive with HTS tokamaks.

2. **Thea publishes a bottoms-up cost estimate** showing total Helios overnight capital <$6B for 390 MWe (< $15,400/kW), with documented REBCO tape quantity, per-coil fabrication cost, and magnet system integration budget. If the estimate is credible (third-party reviewed, anchored to supplier quotes), and shows C220103 < $2B, the library-only model is too pessimistic by 30–40%.

### Evidence that would materially raise LCOE estimate (to >300 $/MWh, rendering concept uncompetitive)

1. **Eos magnet system overshoots $1.2B for ~200 MWe scale** (implying >$15M average per coil), proving that planar coils at 20 T field-on-conductor are no cheaper to build than W7-X-class 3D modular coils. If Eos coil cost scales linearly to Helios (670 coils at $15M each = $10B magnet account), LCOE exceeds 400 $/MWh and the planar stellarator bet is dead.

2. **V-4Cr-4Ti supply chain fails to materialize by 2035**, forcing Helios to use EUROFER97 (7-year first-wall lifetime, 75% CF), *and* the X-point divertor proves unworkable in QA geometry (excessive impurity contamination, inability to detach), forcing a retrofit to island divertors with 2-year schedule slip and $200M cost adder. Combined penalty: capacity factor 75%, divertor cost +$140M, LCOE from 241 → 320 $/MWh.

3. **Eos fails to achieve Q > 0.1 or H_ISS04 < 1.2**, indicating that QA stellarator confinement does not scale to reactor-relevant parameters. This would not immediately retire Helios (the gyrokinetic analysis could still be correct) but would force a major auxiliary heating redesign (1 MW → 50+ MW ECRH, recirculating power from 48 MW → 150+ MW, net output from 390 MWe → 280 MWe). At 280 MWe native with fixed capital cost, LCOE rises from 241 → ~335 $/MWh, and the concept loses commercial viability.
