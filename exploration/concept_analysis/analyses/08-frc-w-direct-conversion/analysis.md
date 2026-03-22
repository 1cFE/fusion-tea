---
ID: 08-frc-w-direct-conversion
Concept: FRC w/ Direct Conversion
Company: Helion Energy
Status: draft
Created: 2026-03-22
Approved-Date:
Reuses: [07-maglif]
---

# D1+ Analysis: FRC w/ Direct Conversion (Helion Energy)

**Concept**: FRC w/ Direct Conversion — D-He3 fuel
**Company**: Helion Energy (Everett, WA)
**Confinement Family**: MIF (Magneto-Inertial Fusion)
**Operation Mode**: Pulsed (~ms plasma lifetime, target commercial rate 1–2 Hz)

---

## Section 1: Availability of Data

**Rating: Limited**

Helion Energy publishes milestone announcements and conceptual explainers at far higher frequency than most private fusion companies, yet the available material systematically stops short of engineering-grade data. No plant study equivalent to ARIES (tokamaks) or LIFE (laser ICF) exists for the Helion concept. No independent techno-economic analysis has been published. The richest single engineering parameter source — an ARPA-E presentation by CEO David Kirtley — is undated but likely 2019–2021 vintage based on prototype context, predating Polaris by years. Operational performance from Polaris, the current seventh-generation prototype, has been reported only at the milestone level (temperature, fuel milestone) without accompanying engineering parameters.

**Peer-reviewed literature:**
Helion's founding team has published a thin but foundational academic record. Slough, Votroubek, and Pihl (2011, *Nuclear Fusion* 51(5)) established the physics of FRC merging-and-compression to high temperatures, the core approach that all seven prototypes implement. Votroubek and Slough et al. (2008, *J. Fusion Energy*) documented stable FRC formation through merging. Kirtley & Milroy (2023, *J. Fusion Energy*) published scaling analysis for adiabatic FRC compression to thermonuclear conditions, which received a peer commentary response in 2026 raising questions about the scaling assumptions [dossier.md]. Beyond these, academic publications on the Helion concept are sparse; the lab heritage (FRX-L at LANL, FRCHX at LANL/AFRL, IPA at MSNW/University of Washington) is documented in older literature that predates Helion's commercial machine design [helion-prototype-generations.md].

**Government and third-party technical data:**
The ARPA-E Kirtley presentation (DocsLib) is the most detailed public engineering document: it discloses plasma density targets (1×10²¹ m⁻³ formation, 1×10²³ m⁻³ compressed), compression field targets (20 T experiment, 40 T reactor), a Fusion Engine design point (50 MW at 2 Hz), and parametric energy balance values (delivery efficiency ~20%, magnetic recovery η = 0.7) [docslib-helion-arpa-e-presentation.md]. The Contrary Research analyst report (undated, likely 2022–2023) independently confirms several key parameters including the aluminum magnet choice, the 85–95% direct energy recovery claim, and the Microsoft PPA terms [contrary-research-helion.md]. Thunder Said Energy (2022) provided a third-party estimate of 1–6 cents/kWh and 50–200 MWe modular plant scale, with methodology not fully disclosed [dossier.md].

**Company disclosures:**
Helion publishes twelve-plus technical articles covering the FRC concept, the RLC circuit energy analogy, the D-He3 fuel choice, the self-breeding fuel cycle, the pulsed approach philosophy, and individual prototype milestones. The February 2026 milestone announcement confirms Polaris achieved 150M°C (13 keV) and demonstrated D-T fusion in January 2026 — the first privately-funded machine to do so [helion-milestones-feb2026.md]. Orion, the eighth-generation commercial plant, began construction in Malaga (Chelan County), Washington in July 2025 with a 2028 delivery target under a Microsoft PPA [helion-milestones-feb2026.md]. Orion's engineering specifications — output, capital cost, compression field, rep rate, efficiency — are entirely proprietary.

**Phase 1a dossier coverage:**
All twelve differentiation columns were filled at high confidence [dossier.md]. The two residual honest gaps are: (1) the achieved rep rate on Polaris (target is ~1 Hz; not reported in the February 2026 milestone announcement), and (2) the precise neutron energy fraction at D-He3 commercial conditions (Helion claims ~5% vs. the schema default of ~10% for D-He3, which is resolvable by D-He3/D-D reaction fraction physics at ~200M°C).

**Key data gaps limiting this analysis:**
1. No independent TEA or LCOE model for the Helion concept exists in the public literature
2. Orion engineering specifications are entirely proprietary — no cost, Q, efficiency, or rep rate targets published
3. D-He3 plasma conditions (200M°C commercial target) not yet demonstrated on any Helion machine
4. No disclosed Q value or recirculating power fraction for commercial design point
5. Energy recovery efficiency not characterized at commercial field strength (40 T target) or bank size

---

## Section 2: Challenges in Capturing System Function

Challenges are ranked in descending order of LCOE impact.

### 1. Q_engineering Definition Is Non-Standard and Entirely Undisclosed (Impact: Critical)

Helion explicitly does not aim for plasma ignition (Q_plasma >> 1 in the conventional sense) and avoids the Q framing in public communications. Net electricity is produced when inductively recovered fusion energy exceeds the net electrical draw per pulse cycle. The breakeven condition is approximately: η_recovery × Q_plasma × η_delivery > 1, where η_delivery is the fraction of stored capacitor energy that reaches the plasma and η_recovery is the fraction of fusion plus residual magnetic energy that is inductively recovered. With η_delivery ≈ 20% (ARPA-E presentation) and η_recovery ≈ 95% (Helion claim), the minimum Q_plasma for net positive electricity is roughly Q > 0.26 — far below ignition. However, useful net electricity at commercial scale requires substantially higher gain: at 50 MJ stored energy, 1 Hz rep rate, and 50 MWe net output target, the per-pulse net energy must be ~50 MJ, implying (0.95 × Q × 0.2 − 1) × 50 MJ = 50 MJ → Q_plasma ≈ 6 [inferred, from stated parameters and Orion output target]. Helion has not published a target Q value for Orion, the ARPA-E design point gain of 1.2 is a historical experimental snapshot, and no independent analysis has validated the commercial energy balance. This makes LCOE modeling dependent on an assumed energy balance that cannot be anchored to public data.

The sensitivity of net electricity to small parameter changes is severe at low gain values. A 2% reduction in recovery efficiency (from 95% to 93%) approximately halves net electricity per pulse at Q ≈ 2. This non-linearity means the LCOE is highly sensitive to the precise efficiency of direct conversion — a parameter that varies with compression field strength, plasma energy, and IGBT switching losses, none of which have been characterized at commercial-scale conditions.

### 2. D-He3 Plasma Conditions Are Not Yet Demonstrated (Impact: Critical)

Commercial D-He3 operation requires ~200M°C (~17 keV) [helion-website-technology.md]. The demonstrated record on Polaris is 150M°C (13 keV) for D-T fusion in January 2026 [helion-milestones-feb2026.md] — approximately 33% below the D-He3 commercial target. The gap matters for two reasons: (a) additional magnetic compression energy or plasma energy is required to reach 200M°C, which scales the capacitor bank size and magnetic field requirement; (b) the D-He3 reaction cross-section peaks at higher temperatures than D-T and has a narrower resonance, making temperature control more critical and gain more sensitive to precise plasma conditions. The progression Helion has publicly described (D-D → D-T → D-He3) has completed only through the D-T milestone. No D-He3 fusion event has been reported in any Helion prototype. The temperature gap from the demonstrated 150M°C to the 200M°C commercial target is not trivially bridged by a scaling argument — it requires Polaris or Orion to demonstrate the capability.

### 3. Rep Rate Scaling Is the Dominant Power Output Lever (Impact: Critical)

Annual energy output = (net energy per pulse) × rep_rate × availability × operating hours. Trenta operated at ~1 pulse per 10 minutes (0.0017 Hz) for 16 months [helion-website-technology.md]. Polaris targets ~1 Hz but has not publicly reported achieving this. The ARPA-E Fusion Engine design point is 2 Hz. The commercial rep rate gap from Trenta's historical operation to the ARPA-E design point is a factor of ~1,200. While Helion's architecture — where coils and the plasma vessel are not consumed per shot, unlike liner-based MIF concepts — is fundamentally better suited to high rep rate than MagLIF, the practical requirements of continuous multi-Hz operation are non-trivial: gas injection and FRC formation must be reliable and repeatable; the 50+ MJ capacitor bank must fully recharge within <1 second at 1 Hz (requiring sustained ~50 MW of charging power); high-voltage IGBT switches must operate at 1–2 Hz cycling for years without degradation. None of these have been demonstrated at the required scale. Each doubling of rep rate from the current prototype performance directly doubles net power output from the same capital, making this the highest-leverage undemonstrated parameter.

### 4. Direct Energy Conversion Efficiency at Commercial Scale (Impact: High)

The >95% round-trip energy recovery claim (demonstrated for >1 million pulses on a 2015-vintage subscale system) is the economic lynchpin of the Helion concept [helion-website-technology.md]. This figure must hold at commercial conditions — higher compression fields (40 T vs. Polaris's 15 T+), larger plasma energies, and faster cycling — for the LCOE projections to be meaningful. Parasitic losses (resistive dissipation in longer cable runs, IGBT switching losses per cycle at higher frequency, skin effect in aluminum coils at commercial scale) that are negligible in a prototype could compound at plant scale. The ARPA-E presentation discloses a magnetic energy recovery efficiency of η = 0.7, which is distinct from the 95% "round-trip" claim and suggests additional losses in the magnetic coupling stage [docslib-helion-arpa-e-presentation.md]. The reconciliation of these efficiency figures at commercial conditions is not publicly documented.

### 5. Capacitor Bank Capital Cost Scaling (Impact: High)

The pulsed power system — capacitor banks (>50 MJ), high-voltage IGBTs, aluminum electromagnetic coils, and power electronics — is the dominant capital cost item. Commercial pulsed power capacitors cost approximately $5/J (inferred from pulsed power industry; see MagLIF analysis, 07-maglif). At this price, a 50 MJ commercial bank implies ~$250M for capacitors alone — clearly incompatible with a 50 MWe power plant economics. Helion manufactures some high-voltage capacitors in-house [contrary-research-helion.md], indicating management awareness of this supply chain risk, but no cost reduction roadmap or cost targets have been publicly disclosed. Significant manufacturing learning-curve reductions (analogous to what the SfA white paper identified for MagLIF: $5/J → <$0.50/J) are required. For Helion, the challenge is compounded by the higher rep rate target (1–2 Hz vs. MagLIF's 0.1 Hz baseline), which multiplies the number of switching cycles per year and the associated component wear rates.

### 6. He3 Fuel Inventory and Self-Breeding Dynamics (Impact: Moderate)

Helion's D-He3 self-breeding cycle depends on DD side reactions: 50% produce He3 directly, 50% produce tritium which decays to He3 with a 12.3-year half-life [helion-website-technology.md]. The long half-life means a significant fraction of potential He3 inventory is locked in decaying tritium at any given time. During the startup campaign — before a sufficient He3 inventory exists for commercial D-He3 operation — the plant must operate on D-D or D-T, accumulating He3 over years. The startup inventory timeline, the required He3 mass to initiate D-He3 commercial operation, and the transition schedule are not publicly documented. The economics of the startup period (lower performance, lower output, operating cost without full revenue) are uncharacterized and could affect project IRR significantly.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least to most mature.

---

**D-He3 Fusion — TRL 1–2**
- **Demonstrated**: D-T fusion at 150M°C (13 keV) on Polaris, January 2026 — first D-T fusion by a privately-funded machine [helion-milestones-feb2026.md]. D-D fusion at lower temperatures in earlier Trenta and Polaris campaigns. D-He3 requires ~200M°C (~17 keV).
- **On paper only**: D-He3 fusion at commercial temperatures on any Helion prototype. Scaling from the demonstrated 150M°C to the 200M°C commercial target.
- **Missing at scale**: Any D-He3 fusion event in a Helion device. Characterization of D-He3 yield as a function of plasma parameters. Validation of the ~5% neutron fraction claim at commercial plasma conditions (depends on D-He3/D-D reaction ratio at ~200M°C, which has not been experimentally measured in the Helion system).

---

**Net Electricity Demonstration — TRL 2**
- **Demonstrated**: >95% round-trip magnetic energy recovery for >1M pulses on a subscale system (2015 press release) [helion-website-technology.md]. The 2021 press release described "first direct magnetic energy recovery from a subscale pulsed magnetic system." Polaris is equipped with 3,800 diagnostics and is explicitly designed to demonstrate net electricity [helion-website-technology.md].
- **On paper only**: Net positive electricity from fusion in any Helion machine. This remains Polaris's stated primary objective as of the February 2026 milestone announcement.
- **Missing at scale**: Net electricity production with D-He3 fusion (still one technology step beyond current D-T demonstration). Efficiency of inductive recovery under full electromagnetic loading of a commercial device (40 T, commercial bank scale). Power electronics behavior at 1–2 Hz sustained operation.

---

**Commercial Rep Rate Operation — TRL 2**
- **Demonstrated**: Trenta operated continuously for 16 months with >10,000 pulses at ~1 pulse per 10 minutes (~0.0017 Hz) [helion-website-technology.md]. Polaris target is ~1 Hz; no public confirmation of achieved rate.
- **On paper only**: All multi-Hz integrated shot cycle operation: gas injection, FRC formation, acceleration, collision, compression, fusion, expansion, energy recovery, recharge, repeat — at 1–2 Hz for years.
- **Missing at scale**: Capacitor recharge within <1 second (requiring ~50 MW sustained charging power for a 50 MJ bank at 1 Hz). Gas injection and FRC formation repeatability at Hz-class rates. IGBT and power electronics reliability under sustained high-frequency, high-voltage operation. Integrated shot cycle at any rate above Trenta's achieved ~0.0017 Hz.

---

**He3 Self-Breeding System — TRL 2–3**
- **Demonstrated**: The underlying DD side-reaction physics producing He3 and tritium is established nuclear physics. Helion received regulatory tritium approval in 2025 [helion-milestones-feb2026.md], demonstrating isotope handling capability. Tritium decay physics (12.3-year half-life producing He3) is well understood.
- **On paper only**: Operational He3 accumulation system — collection of He3 from DD reaction products, tritium storage during He3 decay cycle, He3 separation from fuel exhaust, and reinjection into plasma stream as inventory grows.
- **Missing at scale**: Commercial-throughput He3 breeding and accumulation system. He3/D2 separation at plant scale. Startup inventory plan and transition schedule from D-D/D-T testing to D-He3 commercial operation. Tritium decay management for the multi-decade accumulation period.

---

**FRC Formation, Acceleration, and Compression — TRL 4–5**
- **Demonstrated**: Seven prototype generations spanning 2013–present. Trenta (6th gen): 100M°C (8 keV ion temperature), >8 T compression, >10,000 pulses over 16 months of continuous operation [helion-website-technology.md]. Polaris (7th gen): 150M°C (13 keV), 15 T+ compression field, D-T fusion. FRC velocities >300 km/s demonstrated. Formation plasma density at 1×10²¹ m⁻³, compressed density target 1×10²³ m⁻³ [docslib-helion-arpa-e-presentation.md]. Heritage from MSNW/UW IPA experiments (2005–2012) and national lab programs (FRX-L at LANL, FRCHX at LANL/AFRL) [helion-prototype-generations.md].
- **On paper only**: Commercial compression conditions — 40 T field, ~200M°C plasma temperature [docslib-helion-arpa-e-presentation.md]. Full D-He3 fusion burn cycle with stable plasma through expansion and energy recovery at commercial parameters.
- **Missing at scale**: Demonstration of 40 T compression capability (2.7× above Polaris's 15 T target). D-He3 plasma stability at 200M°C through the full compression-fusion-expansion cycle. Reproducible shot performance at commercial parameters and rep rates. Scaling validation of Kirtley & Milroy (2023) FRC compression scaling relations under peer scrutiny [dossier.md].

---

**Direct Inductive Energy Recovery — TRL 4–5**
- **Demonstrated**: >95% round-trip energy recovery for >1M pulses on a subscale system (2015) [helion-website-technology.md]. The physical mechanism — expanding magnetized plasma inducing current in surrounding coils via Faraday's law — is established electromagnetics. Modern high-voltage IGBTs demonstrated as enabling technology.
- **On paper only**: Direct energy recovery at commercial fusion power levels (50+ MWe), at 40 T compression fields, and at 1–2 Hz cycling. Full energy conversion chain from D-He3 charged particle energy (3.6 MeV alpha + 14.7 MeV proton) through inductive recovery to grid-compatible AC output.
- **Missing at scale**: Performance characterization at 40 T (vs. Polaris 15 T+ and Trenta 8 T+ demonstrated fields). IGBT performance and lifetime under 1–2 Hz, high-voltage sustained operation over years. Recovery efficiency from D-He3 fusion products specifically (alpha and proton have different magnetic rigidities than D-T products). Reconciliation of the "η = 0.7 magnetic recovery efficiency" from ARPA-E data with the ">95% round-trip" claim from press materials.

---

**Pulsed EM Coils and Power Electronics — TRL 5–7**
- **Demonstrated**: Aluminum electromagnetic coils successfully operated through seven prototype generations, from Grande (4 T, 2014) through Polaris (15 T+, 2024–present) [helion-prototype-generations.md]. Capacitor bank >50 MJ at tens of kV built and operational on Polaris [helion-website-technology.md]. ~720 miles of coaxial cable (copper, aluminum, custom alloys) engineered on Polaris.
- **On paper only**: Scale-up to 40 T commercial compression field. Long-term (multi-year) reliability at 1–2 Hz cycling and commercial voltage levels. Cost reduction from current pricing to commercially viable levels.
- **Missing at scale**: Commercial-scale capacitor bank lifecycle cost and replacement schedule. Aluminum coil performance at 40 T (significantly above demonstrated 15 T+ on Polaris). IGBT long-term reliability under continuous multi-Hz, high-voltage load for 30-year plant lifetime.

---

**No Tritium Breeding Blanket Required (D-He3 Commercial Operation) — Structural Advantage**

One of the most significant economic differentiators of the Helion concept is the complete absence of a tritium breeding blanket in commercial D-He3 operation. The ~5% neutron energy fraction from D-He3 reactions and DD side reactions does not require breeding to sustain the fuel cycle; tritium produced by DD reactions accumulates and decays to He3 internally. This eliminates:
- Blanket capital cost (typically 15–25% of direct capital in D-T reactor cost studies)
- Li-6 enrichment supply chain and procurement cost
- FLiBe or solid breeder inventory, processing, and supply chain
- Tritium extraction and processing infrastructure at kg/day throughput
- Remote handling systems for activated blanket replacement
- High-neutron-fluence structural material qualification (no first wall operating under 14.1 MeV bombardment commercially)

During current D-T testing on Polaris, tritium handling is required and has been licensed [helion-milestones-feb2026.md], but this is an explicitly temporary testing configuration. The commercial D-He3 plant design carries none of these cost items.

---

**No Primary Steam Cycle Required — Structural Advantage (BoP)**

Direct inductive energy recovery eliminates the steam turbine, condenser, heat exchangers, and feedwater system that account for ~15–20% of direct capital in conventional fusion power plants. The ~5% neutron energy fraction would require a small secondary thermal circuit, but this is a modest capital item. Grid interconnection, power conditioning electronics, and auxiliary systems are conventional. The main novel BoP challenge is interface electronics between the pulsed direct-current output of the inductive recovery system and grid-frequency AC — a power electronics design challenge with industrial precedents (pulsed power, energy storage) but not yet demonstrated at fusion power plant scale.

---

## Section 4: Key Materials and Supply Chain Considerations

**No Superconducting Magnets — Structural Supply Chain Advantage**
Helion's aluminum pulsed electromagnetic coils require no REBCO tape, no Nb₃Sn, and no cryogenic infrastructure. This eliminates the single largest supply chain bottleneck constraining compact tokamak timelines: global REBCO production capacity of ~thousands km/year vs. >5,000 km required per reactor at companies like CFS [inferred from 01-hts-compact-tokamak analysis]. Aluminum is globally abundant (~$2/kg), and precision coil fabrication at the required tolerances is within established industrial capability. The absence of superconductors also eliminates cryoplant capital, cryogenic maintenance cost, and quench protection system complexity.

**High-Voltage Capacitors — Primary Capital Cost Challenge**
Capacitor banks are the dominant capital cost item in the pulsed power system. Current commercial pulsed power capacitor pricing is approximately $5/J, implying ~$250M for a 50 MJ commercial bank at current commodity pricing — unacceptable for a 50 MWe plant whose entire capital budget must be competitive with utility-scale power. Helion manufactures some high-voltage capacitors in-house [contrary-research-helion.md], suggesting intentional supply chain control, but no cost data or cost reduction trajectory has been published. By analogy with the pulsed magnetic fusion concept family [07-maglif analysis], a roughly 10× cost reduction (from ~$5/J to <$0.50/J) is needed for commercial viability, achievable only through high-volume manufacturing learning curves. Helion's potential advantage over MagLIF here is higher rep rate (1–2 Hz target vs. MagLIF's 0.1 Hz), which increases annual energy throughput per dollar of capital — but it also increases annual cycle count by 10×, compounding IGBT and switch wear.

**Deuterium — Abundant and Cost-Negligible**
Deuterium is the sole external commercial fuel input (He3 is self-bred). Deuterium is produced by electrolysis of heavy water or by isotopic distillation, available commercially at $600–2,000/kg, and in global supply adequate for any plausible fusion fleet. A 50 MWe plant operating at 1 Hz with full D-He3 combustion would consume grams of deuterium per day. Fuel cost contribution to LCOE is negligible.

**He3 — No External Supply Required (Long-Term)**
Natural He3 is extraordinarily scarce — global production of ~15,000 liters/year as a byproduct of tritium decay in nuclear weapons programs, priced at ~$10,000–$15,000/liter in the current market. Relying on external He3 would be commercially prohibitive at any plausible plant scale. Helion's self-breeding approach avoids this entirely. However, during the startup accumulation period before a sufficient He3 inventory exists, the plant may require some initial He3 — the quantity, cost, and timeline of this startup period are undisclosed and depend on the DD reaction rate during early campaigns.

**No Tritium for Commercial Operation — Major Simplification**
Commercial D-He3 operation requires no external tritium. This eliminates:
- Startup tritium inventory (~$30,000/g, 1–5 kg required for D-T concepts)
- Tritium processing, confinement, and extraction infrastructure
- Li-6 supply chain for breeding
- Regulatory compliance burden of high-inventory tritium handling

The D-T testing phase on Polaris required and obtained regulatory tritium approval (2025) [helion-milestones-feb2026.md], indicating regulatory familiarity, but this infrastructure is not part of the commercial plant design.

**Neutron Management Materials — Far Below D-T Standards**
With only ~5% neutron energy fraction (Helion claim; vs. ~80% for D-T), and 2.45 MeV DD neutrons (vs. 14.1 MeV D-T neutrons), the neutron fluence on structural components is roughly 50× lower in energy density than a D-T concept at equivalent fusion power. Shielding is borated polyethylene and borated concrete (~1 m total) — equivalent to hospital particle accelerator shielding [helion-website-technology.md]. Structural materials do not require qualification against 14.1 MeV neutron embrittlement, eliminating the need for ODS steels, tungsten composites, or SiC-SiC that constrain D-T plant design. First wall activation is negligible for commercial purposes, enabling personnel access and simplified maintenance.

**Power Electronics (IGBTs) — Component Lifetime Risk**
High-voltage IGBTs enabling >95% energy recovery per cycle are commercially available and have been demonstrated in prototype service. At 1–2 Hz commercial operation, an IGBT switching 10⁸ times per year faces far higher accumulated cycle count than any current industrial application. The commercial IGBT lifetime data — typically specified at much lower switching frequencies or in different load profiles — does not directly translate to Helion operating conditions. Component failure rates and replacement costs at commercial cycling are uncharacterized. This is a discrete OPEX risk that could drive maintenance costs if replacement intervals are short.

**Quartz Tubes and In-House Manufacturing**
Helion manufactures quartz plasma formation tubes in-house [contrary-research-helion.md]. Quartz (fused silica) is abundant and commercially available; precision tube fabrication is mature industrial practice. The in-house manufacturing strategy reflects control of a supply chain item identified by management as critical, not fundamental scarcity.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output (Orion) | 50 MWe+ | Helion milestones Feb 2026 [helion-milestones-feb2026.md] | high | Target after 1-year ramp-up; Microsoft PPA; engineering specs proprietary |
| Net electrical output (Nucor partnership) | 500 MWe | Contrary Research [contrary-research-helion.md] | medium | Long-term; no construction timeline |
| ARPA-E design point output | 50 MW at 2 Hz | ARPA-E presentation [docslib-helion-arpa-e-presentation.md] | medium | Vintage 2019–2021; design has evolved |
| Plasma temperature achieved (Polaris, D-T) | 150M°C (13 keV) | Helion milestones Feb 2026 [helion-milestones-feb2026.md] | high | January 2026; D-T milestone |
| Plasma temperature target (D-He3 commercial) | ~200M°C (~17 keV) | Helion website [helion-website-technology.md] | high | Not yet demonstrated; ~33% above current D-T record |
| Capacitor bank stored energy (Polaris) | >50 MJ | Helion website [helion-website-technology.md] | high | Polaris-specific; commercial size undisclosed |
| Compression field (Polaris target) | 15 T+ | Helion website [helion-website-technology.md] | high | Polaris target; Trenta achieved >8 T |
| Compression field (reactor target) | 40 T | ARPA-E presentation [docslib-helion-arpa-e-presentation.md] | medium | ARPA-E design point; may have evolved |
| Direct energy recovery efficiency (claimed) | 85–95% | Contrary Research [contrary-research-helion.md]; Helion website | medium | Company claim; >95% round-trip demonstrated (2015, subscale, 1M+ pulses) |
| Magnetic energy recovery efficiency (ARPA-E) | η = 0.7 | ARPA-E presentation [docslib-helion-arpa-e-presentation.md] | low | Vintage design point; reconciliation with ">95% round-trip" not documented |
| Energy delivery efficiency (ARPA-E) | ~20% (η × Gain = 0.2 × 1.2) | ARPA-E presentation [docslib-helion-arpa-e-presentation.md] | low | Historical snapshot, gain 1.2 is far below commercial target |
| Rep rate — Trenta operational | ~1 pulse / 10 min (0.0017 Hz) | Helion website [helion-website-technology.md] | high | Demonstrated over 16-month campaign |
| Rep rate — Polaris target | ~1 Hz | Helion website; dossier [dossier.md] | medium | Target, not confirmed as achieved publicly |
| Rep rate — ARPA-E Fusion Engine design point | 2 Hz | ARPA-E presentation [docslib-helion-arpa-e-presentation.md] | medium | Commercial Fusion Engine design point |
| Rep rate — long-term speculative | 10–60 Hz | Helion website [helion-website-technology.md] | low | Long-term speculative; no technical basis disclosed |
| FRC velocity | >300 km/s | ARPA-E presentation [docslib-helion-arpa-e-presentation.md]; Helion website | high | Both plasmoids accelerated to this velocity |
| Plasma density (formation) | 1×10²¹ m⁻³ | ARPA-E presentation [docslib-helion-arpa-e-presentation.md] | medium | Pre-compression density |
| Plasma density (compressed target) | 1×10²³ m⁻³ | ARPA-E presentation [docslib-helion-arpa-e-presentation.md] | medium | Target; achievement at commercial scale unconfirmed |
| D-He3 reaction energy | 18.3 MeV (3.6 MeV α + 14.7 MeV p) | Helion website [helion-website-technology.md] | high | Nuclear physics; 95% charged particles |
| D-He3 neutron energy fraction | ~5% | Helion FAQ [helion-website-technology.md] | medium | Company claim; schema default ~10%; depends on D-D side reaction rate at ~200M°C |
| DD side reaction → He3 yield | 50% direct He3, 50% tritium (→ He3, t½ 12.3 yr) | Helion website [helion-website-technology.md] | high | Nuclear physics |
| Plasma lifetime per pulse | >1 ms | Helion FAQ [helion-website-technology.md] | high | FRC lifetime through full compression-expansion cycle |
| FRC plasma beta | ~100% | Contrary Research [contrary-research-helion.md] | medium | High-beta FRC; vs. ~10% for tokamaks |
| Shielding approach | Borated polyethylene + borated concrete, ~1 m | Helion FAQ [helion-website-technology.md] | high | Analogous to hospital particle beam shielding |
| Coil/magnet material | Aluminum pulsed EM; no superconductors | Contrary Research [contrary-research-helion.md]; Helion website | high | CEO confirmed "regular aluminum magnets" |
| No tritium breeding blanket (commercial) | N/A — D-He3, no Li blanket needed | Helion website [helion-website-technology.md] | high | External fuel is D2 only commercially |
| Target operating temperature for He3 | 750M Kelvin | Contrary Research [contrary-research-helion.md] | medium | Alternative figure cited alongside 200M°C; possible discrepancy in units or context |
| LCOE target (third-party analyst) | 1–6 ¢/kWh | Thunder Said Energy, 2022 [dossier.md] | low | Third-party estimate; methodology not disclosed |
| Input energy cost target | <$0.03/MJ | ARPA-E presentation [docslib-helion-arpa-e-presentation.md] | medium | Constrains recirculating power cost; implies grid electricity price assumption |
| Prototype generations | 7 (Grande 2014 → Polaris 2024) | Helion prototype generations [helion-prototype-generations.md] | high | 16-month Trenta continuous operation; Polaris operational since end 2024 |
| Orion location and status | Chelan County, WA; construction began July 2025 | Helion milestones Feb 2026 [helion-milestones-feb2026.md] | high | Land leased from Chelan County PUD; targeting 2028 |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q_fusion (plasma gain at commercial conditions) | proprietary | blocking | Helion avoids Q framing; energy balance at Orion conditions entirely undisclosed |
| Orion capital cost | proprietary | blocking | No published estimate; no applicable analogue in existing fusion literature |
| Specific capital cost ($/kWe) | not-yet-sourced | blocking | No plant study; direct-conversion pulsed fusion has no published cost model |
| D-He3 plasma conditions achieved or demonstrated | truly-unknown | blocking | Not yet achieved; next Polaris milestone |
| Rep rate achieved on Polaris | proprietary | blocking | Milestone announcement disclosed temperature but not rep rate |
| Energy recovery efficiency at commercial field (40 T) | proprietary | blocking | Demonstrated at prototype scale; not characterized at commercial parameters |
| Net electricity per pulse (Polaris) | proprietary | blocking | Primary Polaris objective; not yet reported |
| Orion engineering specs (output, field, rep rate, efficiency) | proprietary | blocking | No public disclosure |
| He3 startup inventory and accumulation timeline | truly-unknown | important | Depends on DD reaction rate in startup campaigns; no published analysis |
| Capacitor bank capital cost at commercial scale | proprietary | important | In-house manufacturing cited; no cost data |
| IGBT / power electronics lifetime under 1–2 Hz sustained operation | truly-unknown | important | No published reliability data for this operating profile |
| Capacity factor / planned availability | proprietary/TBD | important | Trenta 16-month baseline; commercial target not stated |
| Commercial fuel cycle He3 throughput and inventory | proprietary | important | Key for fuel cost and supply chain sizing |
| Secondary thermal BOP cost for ~5% neutron fraction | not-yet-sourced | nice-to-have | Small circuit; analogues from other concepts; not Helion-specific published |
| Neutron energy fraction at D-He3 commercial conditions (5% vs. 10%) | not-yet-sourced | nice-to-have | Resolvable by D-He3/D-D cross-section ratio at ~200M°C |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Q_fusion and energy balance at commercial Orion conditions entirely undisclosed | S1, S2, S5 | proprietary | blocking | Polaris net electricity results when announced; Orion pre-operational disclosure |
| 2 | D-He3 plasma conditions (200M°C) not yet demonstrated; 33% above current record | S1, S2, S3, S5 | truly-unknown | blocking | Next Polaris campaign milestone; company announcement |
| 3 | Rep rate achieved on Polaris not reported; commercial 1–2 Hz undemonstrated | S1, S2, S3, S5 | proprietary | blocking | Future Helion milestone; GeekWire/press coverage; NRC licensing documentation |
| 4 | Orion capital cost and specific capital ($/kWe) not published; no plant study | S1, S5 | proprietary | blocking | NRC license filing; DOE milestone program disclosure; future investor communications |
| 5 | Direct energy recovery efficiency at 40 T / commercial bank scale not characterized | S2, S3, S5 | proprietary | blocking | Polaris and Orion test results; future Helion peer-reviewed publications |
| 6 | Net electricity demonstration from any Helion prototype not yet reported | S1, S2, S3 | truly-unknown | blocking | Imminent Polaris result; Helion milestone announcement |
| 7 | Capacitor bank capital cost at commercial 50+ MJ / 1–2 Hz scale undisclosed | S2, S4, S5 | proprietary | important | In-house manufacturing means cost is internally known; no public path to disclosure |
| 8 | He3 startup inventory, accumulation timeline, and transition cost | S2, S4, S5 | truly-unknown | important | No published analysis; requires DD reaction rate characterization in startup campaigns |
| 9 | IGBT / power electronics lifetime under sustained commercial cycling (1–2 Hz, >10⁷ cycles/year) | S3, S4, S5 | truly-unknown | important | Industrial pulsed power lifetime data provides lower bound; Helion-specific testing needed |
| 10 | Capacity factor and planned maintenance schedule for commercial plant | S5 | proprietary/TBD | important | Trenta 16-month baseline is only public data point; commercial targets not stated |
| 11 | He3/D2 separation technology and throughput at commercial scale | S3, S4 | truly-unknown | important | No published fuel cycle engineering for D-He3 at commercial throughput |
| 12 | Neutron energy fraction at D-He3 commercial conditions (5% vs. schema default 10%) | S5 | not-yet-sourced | nice-to-have | D-He3/D-D cross-section ratio at ~200M°C; nuclear data tables; not Helion-specific |
| 13 | Secondary thermal BOP design and cost for 5% neutron energy fraction | S3, S5 | not-yet-sourced | nice-to-have | Analogues from other low-neutron concepts; straightforward once neutron fraction confirmed |

---

## Section 7: Cross-Concept Notes

The approved MagLIF (D-T) analysis [07-maglif] is the most structurally relevant prior analysis, as both concepts are pulsed MIF approaches using pulsed electromagnetic energy storage. Cross-referencing this analysis reveals both shared challenges and fundamental structural divergences.

**Shared analytical framework — pulsed architecture LCOE structure:**
The MagLIF analysis established that for pulsed fusion concepts, "effective capacity factor has two components — plant uptime (maintenance-driven) and achieved rep rate as a fraction of design rep rate (engineering-driven)," and that "small changes in rep rate produce non-linear effects on specific capital cost." This framing applies identically to Helion. Standard LCOE formulations that treat capacity factor as maintenance-only systematically misrepresent pulsed fusion economics. For Helion, a 10× increase in rep rate (from Trenta's operational 0.0017 Hz to Polaris's target 1 Hz) represents a ~600× increase in annual energy output from the same machine — making rep rate the single highest-leverage parameter in the model, as it is for MagLIF.

**Shared supply chain challenge — capacitor cost reduction:**
Both concepts depend on pulsed power systems whose commercial economics require roughly 10× reductions in capacitor cost (from ~$5/J to <$0.50/J), though neither has published a detailed cost reduction roadmap. For Helion, the challenge is somewhat more acute on a per-MWh basis because higher rep rates (1–2 Hz vs. MagLIF's 0.1 Hz baseline) increase annual switch cycle count proportionally, compounding IGBT wear.

**Divergences from MagLIF — fundamental structural differences:**

*1. No per-shot consumables (major Helion advantage):*
MagLIF destroys the target liner, recyclable transmission line, and potentially magnetization coils each shot — creating a cost floor estimated at ~$28M/year at $1/shot × 28M shots/year at 1 Hz. Helion's coils and plasma vessel are not consumed per shot; the sole consumable is fuel gas (deuterium + He3), which is cost-negligible. This structural difference removes one of the most challenging economic constraints in pulsed fusion and is why Helion can target higher rep rates without compounding per-shot hardware cost.

*2. D-He3 vs. D-T fuel (fundamentally different cost structure):*
MagLIF uses D-T fuel, requiring: a tritium breeding blanket (FLiBe, Li-6 enrichment, TBR > 1 design), startup tritium inventory at ~$30,000–$150,000/g, tritium processing at industrial throughput, and structural material qualification under 14.1 MeV neutron bombardment. Helion's D-He3 commercial cycle eliminates all of these. The neutron energy fraction contrast is stark: ~80% for D-T vs. ~5% for D-He3 — a factor of 16 reduction in neutron loading that cascades through blanket, shielding, activation, remote handling, and structural material costs. The absence of a tritium breeding blanket alone likely removes 15–25% of direct capital from the cost structure compared to D-T concepts.

*3. Direct energy conversion vs. thermal cycle:*
MagLIF uses conventional thermal cycles (Rankine or Brayton, ~40% efficiency). Helion's direct inductive recovery — if achieved at the claimed 85–95% efficiency — eliminates the steam turbine, condenser, and heat exchanger from the primary energy path. At equivalent gross fusion power, Helion's net electrical output fraction could be roughly 2× higher than MagLIF's, dramatically reducing the required fusion power for a given net electrical output. The tradeoff is that Helion's energy recovery efficiency at commercial scale is an undisclosed, undemonstrated parameter that carries enormous LCOE uncertainty.

*4. No FLiBe supply chain:*
MagLIF's planned blanket/coolant (FLiBe, Li₂BeF₄) involves beryllium supply constraints, Li-6 enrichment requirements, and a production scale-up challenge (shared with laser ICF concepts). Helion has no FLiBe requirement for commercial operation, eliminating this supply chain risk entirely.

*5. Physics demonstration maturity:*
MagLIF has a stronger independent academic literature base — 70+ integrated experiments on the Z machine with peer-reviewed scaling relations validated by Sandia, LLNL, LANL, and university groups. Helion's experimental validation comes primarily from the company's own seven-prototype program; independent peer review of the scaling claims (Kirtley & Milroy 2023 commentary, 2026) has raised methodological questions. Both concepts have fundamental validation gaps at commercial scale, but MagLIF's experimental basis is more publicly verifiable.

---

## Section 8: Sources

1. **Helion Energy Website (multiple technical articles)** — Primary source for all operational parameters, fuel cycle description, energy capture mechanism, magnet design, and prototype milestones. Articles: technology/, faq/, polaris/, how-to-make-fusion-electricity-without-ignition, explaining-helions-fusion-fuel-choice-d-he-3, how-to-engineer-a-renewable-deuterium-helium-3-fusion-fuel-cycle, helions-fusion-system-is-basically-an-rlc-circuit, more-on-helions-pulsed-approach-to-fusion.
   - Found: Phase 1a sources [helion-website-technology.md]
   - Covers: Sections 1, 2, 3, 4, 5, 6

2. **Helion Energy Milestones Announcement (February 2026)** — Most current milestone report: 150M°C (13 keV) D-T fusion on Polaris; first privately-funded D-T fusion; Orion construction timeline; Microsoft PPA.
   - Source: https://www.helionenergy.com/articles/helion-achieves-new-fusion-energy-milestones/
   - Found: Phase 1a sources [helion-milestones-feb2026.md]
   - Covers: Sections 1, 3, 5

3. **DocsLib: Helion ARPA-E Presentation (Kirtley, CEO)** — Richest publicly available engineering parameter document: 20 T experiment / 40 T reactor fields, 50 MW @ 2 Hz design point, plasma density targets, energy balance parameters (η × Gain = 0.2 × 1.2, magnetic recovery η = 0.7), input cost target (<$0.03/MJ).
   - Source: https://docslib.org/doc/9103852/helion-energy-david-kirtley-ceo-project-lead-20-tesla-arpa-e-experiment-40-tesla-reactor
   - Found: Phase 1a sources [docslib-helion-arpa-e-presentation.md]
   - Covers: Sections 2, 5

4. **Contrary Research: Helion Energy** — Third-party analyst report: confirms aluminum magnets, 85–95% energy recovery efficiency, 750M K He3 operating temperature, Microsoft PPA terms, in-house capacitor manufacturing, supply chain risk.
   - Source: https://research.contrary.com/company/helion
   - Found: Phase 1a sources [contrary-research-helion.md]
   - Covers: Sections 1, 3, 4, 5

5. **Helion Energy Prototype Generations** — Prototype timeline (Grande through Polaris), FRC velocities, key achievements per generation, published research citations, national lab heritage (FRX-L, FRCHX, IPA).
   - Found: Phase 1a sources [helion-prototype-generations.md]
   - Covers: Sections 1, 3

6. **Slough, Votroubek, Pihl (2011)** — "Creation of a high-temperature plasma through merging and compression of supersonic field reversed configuration plasmoids." *Nuclear Fusion* 51(5). DOI: 10.1088/0029-5515/51/5/053008. Foundational peer-reviewed paper establishing the collision-and-compress physics approach that all Helion prototypes implement.
   - Covers: Sections 1, 3

7. **Kirtley & Milroy (2023)** — "Fundamental Scaling of Adiabatic Compression of FRC Thermonuclear Fusion Plasmas." *Journal of Fusion Energy*. DOI: 10.1007/s10894-023-00367-7. Scaling analysis supporting the Helion commercial design approach; subject to peer commentary (2026, DOI: 10.1007/s10894-026-00554-2).
   - Covers: Sections 1, 2

8. **Thunder Said Energy: Helion (2022)** — Third-party analyst assessment providing the only independent LCOE range estimate in available sources: 50–200 MWe modular, 1–6 cents/kWh target. Methodology not fully disclosed.
   - Source: https://thundersaidenergy.com/2022/03/28/helion-linear-fusion-breakthrough/
   - Found: dossier.md citation [dossier.md]
   - Covers: Section 5

9. **Phase 1a Dossier: FRC w/ Direct Conversion** — Aggregated research summary with all 12 differentiation table columns at high confidence, source citations, and iterative confidence tracking.
   - Found: Phase 1a [dossier.md]
   - Covers: All sections
