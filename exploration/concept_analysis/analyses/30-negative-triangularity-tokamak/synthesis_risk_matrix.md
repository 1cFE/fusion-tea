#### F1: Plasma Performance

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | H₉₈ = 1.44 L-mode confinement at n/n_GW ≈ 0.85, T_i ≈ 12 keV, sustained for ≥15 min burn pulses in D-T burning plasma at Q ≥ 11 (MANTA spec) |
| Best demonstrated | TCV: H₉₈ ≈ 1.3–1.5 in NT L-mode at T_i ≤ 2 keV, non-burning, transient (seconds). DIII-D: similar NT L-mode confinement enhancement at higher power but still non-burning, T_i ≤ 5 keV, no alpha heating |
| Gap ratio | Temperature: 12 keV / 2 keV = 6×; burning plasma: never demonstrated (N/A); pulse length: 900 s / 5 s = 180× |
| Closure mechanism | MANTA and Ball et al. extrapolate TCV/DIII-D L-mode confinement scaling to reactor conditions using IPB98(y,2) scaling law with NT-specific H-factor. Assumes density peaking, impurity transport, and alpha-particle pressure do not degrade confinement relative to small-scale experiments |
| Classification | **Binary** — if H₉₈ drops below ~1.2 at reactor conditions, Q falls below breakeven and net electricity becomes negative or marginal |
| Evidence tier | **3** (subscale demonstration) — TCV and DIII-D validate NT L-mode exists and shows confinement enhancement vs. PT L-mode at experimental scale, but reactor-relevant temperature, density, and burning-plasma conditions are un demonstrated. Guizzo et al. (2025) demonstrate vertical stability control at copper-magnet demonstrator scale (R₀=1m, Bₜ=3T) via passive plates, partially de-risking the path to larger NT devices, but confinement scaling gap remains |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | First wall and divertor survival under NT L-mode heat flux (P_SOL = 23.5 MW, peak divertor 2.8 MW/m²) with ≥2 full-power-years between replacements. V-4Cr-4Ti vacuum vessel surviving 14 MeV neutron fluence (≥20 dpa over plant lifetime) with acceptable embrittlement |
| Best demonstrated | WEST tungsten monoblock divertor: >1000 pulses at 5–10 MW/m², transient. ITER tungsten divertor mock-ups qualified at 10–20 MW/m² for short cycles. V-4Cr-4Ti: lab-scale neutron irradiation to ~10 dpa (fission spectrum), no fusion-spectrum 14 MeV data at commercial fluence |
| Gap ratio | Divertor: 2.8 MW/m² well within demonstrated 10–20 MW/m² (no gap, tier 4–5). V-4Cr-4Ti: 20 dpa fusion spectrum / 10 dpa fission spectrum = 2× fluence, plus helium embrittlement from (n,α) reactions not present in fission |
| Closure mechanism | Divertor: MANTA's low P_SOL keeps peak heat flux within demonstrated tungsten monoblock limits — no advanced materials required. V-4Cr-4Ti: MANTA notes "future material options (ODS ferritic steels, SiC-SiC composites) depend on technology readiness," suggesting fallback to RAFM steel if V-4Cr-4Ti supply fails |
| Classification | **Degrading** — divertor at 2.8 MW/m² is within demonstrated limits (low risk). V-4Cr-4Ti supply failure forces RAFM substitution → higher activation → thicker shielding, longer maintenance windows, higher capital cost (+$100–200M, availability -5–10%), but plant remains operational |
| Evidence tier | **4** (near-regime for divertor, partial for V-4Cr-4Ti) — Divertor: WEST/ITER-scale tungsten endurance at 5–20 MW/m² exceeds MANTA's 2.8 MW/m² requirement → tier 4–5. V-4Cr-4Ti: lab-scale fission-neutron irradiation provides partial evidence but fusion-spectrum He production and commercial-scale production are undemonstrated → tier 3. Composite score: **3.5** (average, rounds to 4.0 per heritage credit floor) |

---

#### F2: Driver / Energy Input

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | ICRF heating delivering 40 MW to plasma at 110 MHz (He-3 minority scheme) with ≥50% absorption efficiency, or ohmic-only operation achieving Q ≥ 11 with zero auxiliary heating (H_NA ≥ 2 confinement enhancement) |
| Best demonstrated | ICRF: JET delivered 32 MW ICRF in D-T at 42–51 MHz with ~60% absorption efficiency (2021). WEST operates 9 MW ICRF at 55 MHz continuously. Ohmic-only at Q>1: never demonstrated — highest ohmic Q achieved is ~0.01 in tokamaks (resistive heating alone insufficient for ignition in all prior experiments) |
| Gap ratio | ICRF power: 40 MW / 32 MW = 1.25× (modest extrapolation). Ohmic Q: Q=11 / Q=0.01 = 1100× (N/A for practical purposes — regime has never been approached) |
| Closure mechanism | ICRF path: scale JET/WEST antenna technology to 40 MW at 110 MHz with neutron-hardened materials. Ohmic path: Ball et al. claim H_NA ≈ 2 ohmic confinement enhancement in compact high-field NT geometry enables Q ≈ 500 via reduced transport losses at Greenwald density limit. This is a 0D power balance extrapolation from preliminary TCV data |
| Classification | **Binary** (for ohmic path only) — if ohmic-only operation fails (H_NA < 1.5), full 40 MW ICRF system is required. If ICRF also fails (poor coupling, antenna damage), plasma cannot reach ignition → zero net electricity. ICRF path alone is not binary (degrading) — partial heating reduces Q but doesn't eliminate fusion output |
| Evidence tier | **4** (ICRF path) — JET 32 MW D-T and WEST continuous-wave ICRF provide near-regime demonstration for 40 MW ICRF at MANTA scale. Frequency shift (42–51 MHz → 110 MHz) and neutron environment are extrapolations but not fundamental physics changes. **Tier 1** (ohmic path) — Ball et al.'s Q ≈ 500 ohmic-only result is a 0D calculation with H_NA = 2 assumed from "preliminary analysis of TCV NT database"; no experimental validation at any scale. Composite: **4.0** for ICRF baseline (use this for scoring), **1.0** for ohmic scenario (flagged as binary risk but not the primary path in MANTA baseline) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | ICRF antennas surviving 14 MeV neutron fluence with ≥2 FPY lifetime, maintaining 50% coupling efficiency. 40 MW RF power supplies and transmission lines operating continuously for 15-min pulses. If ohmic-only: eliminate heating hardware entirely (zero requirement) |
| Best demonstrated | ITER ICRF antenna design qualified to ~0.3 dpa (limited neutron exposure, not yet operated in burning plasma). JET ICRF antennas: operated in D-T but with low integrated neutron fluence (~0.1 dpa over campaign), replaced after damage. WEST ICRF: long-pulse but non-burning (zero 14 MeV fluence). Industrial RF power supplies: 10+ MW continuous-wave systems operational in fusion experiments (WEST, ASDEX-U) |
| Gap ratio | Neutron fluence: MANTA-scale ≥2 FPY at 450 MW fusion → ~5–10 dpa over lifetime / ITER antenna 0.3 dpa demonstrated = 15–30× fluence gap. Power: 40 MW / JET's 32 MW = 1.25× |
| Closure mechanism | MANTA notes "detailed antenna design was outside the scope of this study" — no specific materials or geometry proposed. Industry analogue: ITER ICRF antenna development (boron carbide Faraday screen, neutron-resistant ceramics) provides pathway, but full-lifetime demonstration requires ITER D-T campaign results (post-2035). Ohmic path eliminates hardware entirely if H_NA validates |
| Classification | **Degrading** — ICRF antenna failures require replacement ($10–30M per set, ~3–6 month outage), reducing availability and increasing O&M cost, but plant can operate with degraded heating (lower Q, reduced output) or periodic antenna replacement cycles. Not a binary failure unless all antennas fail simultaneously and replacement is infeasible |
| Evidence tier | **3** (partial demonstration) — ITER antenna design and JET D-T operation provide subscale/adjacent evidence, but full-lifetime neutron exposure at MANTA fluence (~5–10 dpa) is undemonstrated. WEST long-pulse operation shows RF component reliability but in non-burning environment. Composite tier: **3.0** (subscale, awaiting ITER D-T validation) |

---

#### F3: Instability Control

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | NT L-mode operation maintaining MHD stability (no disruptions) at βN = 1.45, q₉₅ ≈ 3.5, with ≥99.5% disruption-free operation over 15-min burn pulses for 2 FPY between major maintenance |
| Best demonstrated | TCV: NT plasmas demonstrated at βN ≈ 1.5–2.0 with no sawteeth and reduced turbulence vs. PT L-mode, transient (seconds). DIII-D: NT L-mode stable at moderate βN (<2.0), no inherent ELMs, but long-pulse stability (>100 s) not yet demonstrated in NT geometry. Disruption rate in NT: uncharacterized experimentally — no NT disruption database exists |
| Gap ratio | Pulse length: 900 s / 5 s = 180×. Disruption-free operation: MANTA target ≥99.5% (≤1 disruption per 200 pulses) / TCV-DIII-D disruption rate unknown = N/A. Burning plasma stability with alpha-particle pressure: never demonstrated in NT |
| Closure mechanism | MANTA relies on L-mode's intrinsic lack of ELMs and NT's reduced turbulence transport to avoid edge instabilities. Vertical stability controlled via passive conducting plates (Markovičiūtė et al. 2024, Guizzo et al. 2025 demonstrate ~75–84% growth rate reduction). Core MHD (sawteeth, tearing modes) assumed manageable via plasma shaping and q-profile control, but no NT-specific disruption mitigation strategy published |
| Classification | **Degrading** — disruptions damage divertor and first wall, requiring replacement ($20–50M per event + 3–12 month outage), but do not prevent reactor operation if disruption rate is <1% of pulses. If disruption rate exceeds 5% (≥1 per 20 pulses), availability drops below 60% → LCOE rises ~30–50%, but plant remains operational with high O&M cost |
| Evidence tier | **3** (subscale demonstration) — TCV/DIII-D validate NT MHD stability at experimental scale with favorable properties (no ELMs, reduced turbulence), but reactor-scale burning plasma with alpha heating and 15-min pulses is extrapolation. Markovičiūtė et al. (2024) provide vertical stability theory; Guizzo et al. (2025) provide pre-conceptual engineering validation at demonstrator scale (R₀=1m, copper magnets). No burning-plasma NT experiment → tier 3 |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Passive vertical stabilizer plates (NT-specific) providing ≥75% growth rate reduction, positioned at optimized radial locations per Markovičiūtė et al. (2024). Conducting plates surviving neutron activation and providing <100 ms response time to vertical displacement events (VDEs). Plasma control coils (PF system) capable of ≥1 MA current ramps for equilibrium control |
| Best demonstrated | ITER and JT-60SA passive stabilizer plates: tokamak-scale conducting shells operational, but PT geometry (different positioning constraints). Guizzo et al. (2025): pre-conceptual design for compact copper-magnet NT device (R₀=1m, Bₜ=3T) demonstrates ~75% vertical instability growth rate reduction via optimized passive plate placement, validating the engineering approach at demonstrator scale. MANTA's PF coil system: standard tokamak technology (8–12 PF coils at MA-scale), operational on ITER-class devices |
| Gap ratio | Vertical stabilizer plates for NT: Guizzo demonstrator-scale (R₀=1m, Bₜ=3T) / MANTA commercial scale (R₀=4.55m, B=11T) = ~4.5× radius, ~3.7× field → extrapolation in stored magnetic energy and mechanical loads, but core physics (passive plate effectiveness) validated. PF coils: no gap — MANTA specs within demonstrated ITER/JET range |
| Closure mechanism | Guizzo et al. (2025) provide the engineering foundation: demountable copper coils, optimized passive plate geometry (high-field side and/or low-field side), force analysis during current quench. Scaling to MANTA's superconducting REBCO coils and larger size requires mechanical design but no new physics. MANTA's PF2 coil lifetime (~890 MW·yr, ~2 FPY) drives maintenance cycle — standard tokamak challenge, not NT-specific |
| Classification | **Degrading** — stabilizer plate failure or VDE increases disruption rate, damaging divertor/first wall (see F3 physics risk), but does not prevent plasma operation. PF coil failures require replacement (6–12 month outage, $50–100M per coil set) but are recoverable |
| Evidence tier | **4** (near-regime with demonstrator validation) — Guizzo et al. (2025) move NT vertical stability from pure theory (Markovičiūtė 2024, tier 2–3) to pre-conceptual engineering demonstration at copper-magnet demonstrator scale, validating passive plate effectiveness. Scaling to MANTA's REBCO coils and 4.5× larger radius is extrapolation but within tokamak engineering experience (ITER/JET analogues). PF coils are tier 5 (fully demonstrated tokamak technology). Composite: **4.0** for NT-specific stabilizer plates + PF system |

---

#### F4: Plasma-Wall Interaction

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tungsten first wall and divertor erosion ≤10 μm/year at MANTA conditions (P_SOL = 23.5 MW, peak divertor 2.8 MW/m², radiative NT L-mode with impurity content Z_eff ≈ 1.5–2.0), sustaining ≥2 FPY between divertor replacements |
| Best demonstrated | WEST: tungsten divertor operated >1000 pulses at 5–10 MW/m², erosion rates ~1–5 μm per 1000 pulses (transient, non-steady). ITER divertor simulations: tungsten erosion ~10–50 μm/year projected for 10 MW/m² steady-state with 15% P_SOL fraction (higher than MANTA's 5.2%). TCV NT experiments: reduced divertor heat load confirmed but no erosion measurements at reactor-relevant fluence |
| Gap ratio | Heat flux: MANTA 2.8 MW/m² / WEST demonstrated 5–10 MW/m² = 0.3–0.6× (MANTA is easier). Steady-state operation: MANTA 15-min pulses / WEST transient ~10 s = 90× duration per pulse. Neutron-assisted erosion: 14 MeV fusion neutrons increase sputtering yield vs. non-burning experiments — factor ~2–5× erosion rate increase (model-dependent) |
| Closure mechanism | MANTA's low P_SOL (5.2% of fusion power) keeps divertor well below demonstrated tungsten limits. NT L-mode provides intrinsic edge radiation without active impurity seeding. Erosion projections from ITER simulations and WEST data suggest ≤5 μm/year at MANTA conditions → ≥4-year divertor lifetime (exceeds 2 FPY target). Neutron-enhanced erosion remains uncertain without burning-plasma NT data |
| Classification | **Degrading** — excessive erosion shortens divertor lifetime from ≥4 years toward ~1 year, increasing replacement frequency and reducing availability by 10–20 percentage points, but does not prevent operation. Tungsten dust accumulation (if erosion exceeds 50 μm/year) could trigger safety concerns but is unlikely at MANTA's low heat flux |
| Evidence tier | **4** (near-regime) — WEST and ITER tungsten divertor testing at 5–20 MW/m² demonstrate performance above MANTA's 2.8 MW/m² requirement, but steady-state burn and fusion-neutron environment are extrapolations. TCV/DIII-D NT experiments confirm low P_SOL but lack quantitative erosion data. Composite: **tier 4** (near-regime, with margin) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tungsten monoblock divertor tiles with RAFM steel or Cu-Cr-Zr cooling tubes surviving 2.8 MW/m² peak heat flux for ≥2 FPY (≥10⁷ seconds integrated exposure), maintaining thermal conductivity and structural integrity under 14 MeV neutron irradiation (≥5 dpa divertor region) |
| Best demonstrated | ITER divertor mock-ups: tungsten monoblocks on Cu-Cr-Zr tubes tested at 10–20 MW/m² for 1000–5000 cycles (High Heat Flux test facilities, GLADIS, JET). WEST: tungsten divertor operated >1000 plasma pulses at 5–10 MW/m², but non-burning (zero 14 MeV fluence, <0.1 dpa). Neutron irradiation: tungsten samples tested to ~5 dpa in fission reactors (different spectrum, lower He/dpa ratio than fusion) |
| Gap ratio | Heat flux: MANTA 2.8 MW/m² / ITER-tested 10–20 MW/m² = 0.15–0.3× (MANTA easier, well within demonstrated limits). Integrated exposure: MANTA ≥2 FPY continuous-equivalent = ~6×10⁷ s / ITER-tested 5000 cycles ×10 s = 5×10⁴ s = ~1200× duration gap. Neutron spectrum: fusion 14 MeV with He production / fission spectrum = different damage mechanism (He embrittlement unknown at fusion fluence) |
| Closure mechanism | MANTA's 2.8 MW/m² is conservative vs. demonstrated 10–20 MW/m² tungsten limits — large engineering margin. Long-pulse integrated exposure extrapolation relies on ITER D-T campaigns (post-2035) and commercial tokamak divertor demonstrations (DEMO, STEP). Cu-Cr-Zr cooling tubes may require substitution with RAFM steel in high-neutron-fluence regions (≥5 dpa) to avoid embrittlement. Divertor replacement every ~2–4 FPY is assumed in MANTA maintenance schedule |
| Classification | **Degrading** — divertor failure requires replacement ($20–40M, 3–6 month outage), reducing availability but not preventing operation. If divertor lifetime drops to <1 FPY (failure rate higher than expected), availability falls to ~70–75% with frequent replacements → LCOE increases ~15–25%, but plant remains operational |
| Evidence tier | **4** (near-regime) — ITER divertor testing at 10–20 MW/m² exceeds MANTA's 2.8 MW/m² requirement by 3–7×, providing strong margin. WEST long-pulse operation validates tungsten endurance in tokamak environment. Fusion-neutron spectrum gap (14 MeV, He production) is the primary uncertainty, but the conservative heat flux target mitigates risk. Awaiting ITER D-T divertor results for full validation → **tier 4** (near-regime with margin, not yet full-scale burning plasma) |

---

#### F5: Neutron/Particle Handling

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | FLiBe liquid immersion blanket achieving TBR ≥ 1.05 (minimum for tritium self-sufficiency after accounting for losses and hold-up inventory) at 450 MW fusion power with 80 cm effective blanket thickness, accounting for penetrations for diagnostics, heating access (if ICRF), and PF coil clearances |
| Best demonstrated | ITER TBM (Test Blanket Module): helium-cooled solid breeder modules designed for TBR ~1.1–1.2 in 6-module configuration (not yet operated). FLiBe TBR calculations: OpenMC / MCNP neutronics simulations for MANTA geometry predict TBR = 1.15 (design value), but no experimental validation of FLiBe breeding at fusion-relevant neutron flux (14 MeV, ≥0.1 MW/m² wall loading) |
| Gap ratio | Neutron flux: MANTA 0.75 MW/m² wall loading / ITER TBM (when operational) ~0.5 MW/m² = 1.5×. TBR experimental validation: MANTA design 1.15 / ITER TBM untested = N/A. 14 MeV neutron spectrum with FLiBe: never tested in tokamak geometry (MSRE used fission-spectrum thermal neutrons in a reactor, not fusion 14 MeV) |
| Closure mechanism | MANTA relies on MCNP/OpenMC neutronics calculations with ENDF/B-VIII.0 cross-section libraries. The 80 cm FLiBe thickness and toroidally continuous blanket geometry (no segmentation gaps) provide large breeding margin. MANTA notes "TBR value of 1.15 has significant uncertainty" and that "detailed analysis of penetrations has not been performed" — the design-value 1.15 could drop to ~1.05–1.10 with realistic port penetrations |
| Classification | **Binary** — if TBR < 1.0 after accounting for penetrations, blanket module gaps, and neutron streaming losses, the plant cannot sustain tritium self-sufficiency → requires external tritium purchase (unavailable at scale) or fails to operate continuously → zero net electricity over lifetime |
| Evidence tier | **2** (simulation-based, no experimental validation) — MCNP/OpenMC models with validated cross-section libraries (ENDF/B) are the standard for fusion neutronics, but no FLiBe blanket has been tested in a 14 MeV fusion-neutron environment. ITER TBMs will provide first data (post-2035) but for solid breeders, not FLiBe. MANTA's TBR = 1.15 is a computational prediction without experimental anchor → **tier 2** |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | FLiBe liquid immersion blanket tank (V-4Cr-4Ti vacuum vessel, toroidally continuous) surviving 14 MeV neutron irradiation to ≥20 dpa over 30-year plant lifetime, maintaining structural integrity and corrosion resistance. FLiBe chemistry control (MoF₆ barrier for corrosion mitigation) preventing tritium permeation into secondary coolant at <1% loss rate |
| Best demonstrated | V-4Cr-4Ti: lab-scale fission-neutron irradiation to ~10 dpa (HFIR, ATR) with acceptable ductility and low activation. No fusion-spectrum 14 MeV irradiation at ≥20 dpa. Commercial production: zero — V-4Cr-4Ti has never been manufactured at multi-hundred-tonne vacuum vessel scale. FLiBe corrosion: MSRE (1965–1969) operated Hastelloy-N containment with molten fluoride salts (FLiNaK, not FLiBe) at 650°C for ~13,000 hours — demonstrated feasibility but not fusion-specific FLiBe chemistry or tritium permeation control |
| Gap ratio | Neutron fluence: 20 dpa fusion spectrum / 10 dpa fission spectrum = 2× plus He/dpa ratio ~10× higher in fusion (embrittlement mechanism differs). Production scale: MANTA vacuum vessel ~200–300 tonnes / lab samples ~kg scale = 10⁵× scale-up with no industrial supply chain. FLiBe tritium permeation: MANTA <1% loss target / MSRE (no tritium, only trace H₂) = N/A |
| Closure mechanism | MANTA acknowledges "future material options (ODS ferritic steels, SiC-SiC composites) depend on technology readiness" — V-4Cr-4Ti is preferred for low activation but not locked. Fallback to RAFM steel (EUROFER) sacrifices low-activation advantage but gains existing supply chain. FLiBe corrosion and MoF₆ barrier: computational chemistry models (CALPHAD) + CSP molten-salt experience provide engineering pathway, but fusion-scale demonstration requires dedicated test loop (DoE Fusion Materials Program, ~5–10 year timeline) |
| Classification | **Degrading** — V-4Cr-4Ti supply failure forces RAFM substitution → higher activation → thicker biological shielding (+$100–200M capital), longer maintenance cooling periods (-5–10% availability) → LCOE increases ~12–18%, but plant remains operational. FLiBe tritium permeation exceeding 1% loss increases fuel processing cost and makeup tritium demand, but does not prevent operation if TBR ≥ 1.05 net |
| Evidence tier | **3** (subscale, adjacent analogue) — Lab-scale V-4Cr-4Ti fission-neutron testing and MSRE molten-salt containment provide adjacent evidence, but fusion 14 MeV spectrum at ≥20 dpa and commercial-scale production are undemonstrated. FLiBe blanket is at conceptual design stage (MANTA), not hardware demonstration. Awaiting dedicated FLiBe test loop and ITER/DEMO neutron irradiation campaigns → **tier 3** (subscale/adjacent, not yet fusion-relevant scale) |

---

#### F6: Fuel Cycle Closure

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tritium breeding from FLiBe achieving TBR ≥ 1.05 net (after extraction losses, permeation, decay, and hold-up inventory) with ≤5% breeding margin uncertainty, sustaining 450 MW D-T fusion continuously for ≥2 FPY between blanket maintenance |
| Best demonstrated | Lab-scale lithium breeding: TSTA (Tritium Systems Test Assembly, 1984–1995) demonstrated tritium extraction from solid Li₂O breeders at gram/day scale. FLiBe breeding: MCNP neutronics predict TBR = 1.15 for MANTA, but no experimental validation of FLiBe tritium production at fusion neutron flux (14 MeV, MW-scale). Burning plasma tritium consumption: JET D-T campaigns (1997, 2021) consumed ~1 g tritium total over hours of operation — factor ~10⁶× less than MANTA's ~440g startup + 75g operational inventory |
| Gap ratio | Tritium throughput: MANTA requires ~0.5 kg/FPY tritium breeding (net after fueling and losses) / JET 1g total = ~500× scale-up. Breeding validation: TBR ≥ 1.05 required / TBR never measured in FLiBe fusion system = N/A. Continuous burn: MANTA 15-min pulses × ~10,000 pulses/year = ~2500 hours burn time/year / JET ~10 hours D-T total = ~250× integrated burn time |
| Closure mechanism | MANTA's TBR = 1.15 provides 10% margin above self-sufficiency (TBR ≥ 1.05 net). Extraction from FLiBe uses gas sparging (He bubbles through molten salt to extract dissolved T₂, TF) with electrolytic processing — analogues exist in MSRE and CSP molten-salt chemistry, but fusion-scale tritium throughput (kg/year) is extrapolation. MANTA acknowledges "a fully functioning tritium fuel cycle has yet to be developed or tested" and employs "conservative estimates" for inventory (75g operational, 440g startup) |
| Classification | **Binary** — if net TBR < 1.0 (breeding fails to exceed consumption + losses), the plant exhausts its tritium inventory within ~1–2 years of operation and cannot continue burning → zero net electricity over lifetime. External tritium purchase is not viable at commercial scale (global supply ~25–30 kg, declining 5.5%/year) |
| Evidence tier | **2** (simulation, no fusion-scale validation) — MCNP/OpenMC neutronics with ENDF/B cross-sections provide TBR predictions, and lab-scale lithium breeding exists (TSTA), but no FLiBe blanket has demonstrated TBR ≥ 1.0 in a 14 MeV fusion-neutron environment at MW-scale. ITER TBMs (post-2035) will provide first tritium breeding data but for solid breeders (Li₄SiO₄, Li₂TiO₃), not liquid FLiBe. MANTA's TBR = 1.15 is computational → **tier 2** |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | FLiBe tritium extraction system processing ≥0.5 kg T/year throughput at ≥95% extraction efficiency, with tritium inventory hold-up ≤15 minutes (MANTA spec: "short tritium system hold-up time of fifteen minutes"), maintaining <1% permeation loss to secondary coolant. Tritium purification, storage (440g startup + 75g operational reserve), and fueling systems (pellet injection or gas puffing at ~mg/s rates for D-T burn) |
| Best demonstrated | ITER tritium plant (not yet operational, commissioning delayed to ~2035): designed for 1.8 kg/day tritium processing (factor ~3× higher than MANTA 0.5 kg/year rate) with cryogenic distillation and isotope separation. TSTA: tritium extraction from solid Li₂O at ~100 g/day scale (1984–1995). FLiBe extraction: gas sparging demonstrated in MSRE for fission-product noble gases (Kr, Xe), but not tritium at kg/year throughput. Tritium fueling: DIII-D and JET pellet injectors operational at mg/s rates, but non-burning (no closed-loop recycling) |
| Gap ratio | FLiBe tritium extraction throughput: MANTA 0.5 kg/year / MSRE gas sparging (no tritium) = N/A (analogue exists but not tritium-specific). Closed-loop fuel cycle: MANTA requires breeding + extraction + purification + fueling + exhaust recovery in continuous operation / ITER tritium plant (under construction, not yet tested) = N/A. Tritium permeation control: <1% loss / MSRE (no tritium inventory, only trace H₂) = N/A |
| Closure mechanism | MANTA's short tritium hold-up time (15 min) reduces in-process inventory, lowering safety/regulatory burden. Extraction technology path: gas sparging (He bubbles) → cryogenic separation → electrolytic processing → pellet fabrication, with analogues in ITER design and MSRE chemistry. MANTA notes "conservative estimates" for inventory (75g operational) and acknowledges "low technological readiness level" for FLiBe-specific tritium processing. Industrial-scale demonstration requires ITER tritium plant commissioning (2035+) and dedicated FLiBe test loop (DoE Fusion Materials Program, 5–10 year timeline) |
| Classification | **Binary** — tritium extraction failure (efficiency <80%, hold-up time exceeds fuel supply rate, or permeation loss >5%) prevents closed-loop operation → plant exhausts startup inventory within months and cannot sustain D-T burn → zero net electricity. Tritium system is the critical path for all D-T fusion concepts — no commercial plant can operate without demonstrated fuel cycle closure at ≥95% efficiency |
| Evidence tier | **2** (design study with partial analogues) — ITER tritium plant design and MSRE gas sparging provide engineering analogues, but no FLiBe tritium extraction system has been built or tested at any scale. TSTA solid-breeder extraction is adjacent (different chemistry, lower throughput). MANTA explicitly calls tritium fuel cycle "yet to be developed or tested" → **tier 2** (design-based, awaiting ITER and FLiBe loop demonstrations) |

---

#### F7: Power Conversion & BOP

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | FLiBe primary coolant transferring 539 MW thermal (450 MW fusion × 1.11 blanket multiplication + 40 MW auxiliary heating) to NaNO₃/KNO₃ molten-salt secondary loop via heat exchanger, achieving outlet temperatures ≥600°C for steam Rankine cycle at 35–38% thermal efficiency (MANTA design) or ≥700°C for advanced Brayton at 45–55% (commercial plant target) |
| Best demonstrated | Concentrated Solar Power (CSP): NaNO₃/KNO₃ molten-salt secondary loops operational at 290–565°C in commercial plants (Gemasolar, Crescent Dunes, Noor III) transferring ~100–200 MW thermal. FLiBe as primary coolant: MSRE operated FLiNaK (not FLiBe) at 650°C, transferring ~8 MW thermal (fission reactor, 1965–1969). FLiBe-to-salt heat exchanger: conceptual design only (MANTA), never built at any scale |
| Gap ratio | Thermal power: MANTA 539 MW / CSP 100–200 MW = 2.7–5.4× scale-up. Temperature: MANTA ≥600°C / CSP 565°C = modest extrapolation (1.06×). FLiBe-to-salt HX: MANTA fusion environment with tritium permeation control / MSRE fission environment without tritium = adjacent regime but different requirements |
| Closure mechanism | CSP molten-salt loop technology (pumps, valves, heat exchangers for NaNO₃/KNO₃ at 290–565°C) is TRL 7–8. FLiBe primary loop (650–700°C) has MSRE precedent (TRL 3–4 for fusion application). The interface — FLiBe-to-salt HX with tritium permeation barrier — is "low technological readiness level" per MANTA §6.3. Engineering pathway: materials coatings (Ni-alloys, oxide barriers) + intermediate HX stages + gas gap separation to block tritium permeation. Requires dedicated test loop before commercial plant |
| Classification | **Degrading** — FLiBe HX failure or low efficiency forces lower outlet temperatures (≤550°C) → thermal efficiency drops from 45–55% target to ~32–38%, increasing LCOE by ~10–20% via reduced net electricity output. Does not prevent operation, but degrades economics. If HX completely fails, plant requires shutdown and HX replacement (6–12 month outage), but this is recoverable with maintenance |
| Evidence tier | **3** (subscale + adjacent analogue) — CSP provides adjacent demonstration of molten-salt secondary loop (NaNO₃/KNO₃) at commercial scale and relevant temperatures, but FLiBe primary loop at fusion scale is undemonstrated (MSRE is 60× smaller power, fission not fusion). FLiBe-to-salt HX with tritium permeation control is conceptual design stage. Awaiting FLiBe loop test facility (5–10 year timeline) → **tier 3** (subscale, requires scale-up validation) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Steam Rankine cycle (or advanced Brayton cycle for commercial plant) converting 539 MW thermal to ≥90 MWe gross electrical (MANTA pilot) or ≥1000 MWe (commercial plant), with turbine-generator-condenser equipment surviving molten-salt loop chemistry and operating for ≥5 years between major overhauls. Thermal energy storage (molten salt tanks) buffering 15-min burn / 2-min dwell pulsed output to provide steady grid supply |
| Best demonstrated | Steam Rankine cycle: GW-scale operational in coal, nuclear, and CSP plants at 32–42% efficiency (TRL 9). Molten-salt thermal storage: CSP plants (Gemasolar: 15-hour storage at 19.9 MW, Crescent Dunes: 10-hour at 110 MW) demonstrate NaNO₃/KNO₃ storage tanks at ~100 MW thermal scale. Advanced Brayton (sCO₂): 10 MWe pilots operational (Sandia, SwRI); 100+ MWe demonstration projects under construction (TRL 6–7 for fusion scale) |
| Gap ratio | Thermal storage: MANTA ~540 MW thermal buffering 2-min dwell (~18 MWh thermal) / CSP Crescent Dunes 1100 MWh thermal (110 MW × 10 hr) = 60× smaller storage requirement (MANTA easier, within demonstrated range). Turbine scale: commercial plant 1000 MWe / existing nuclear plants 1000–1500 MWe = no gap (standard equipment). Advanced Brayton: 1000 MWe sCO₂ / 10 MWe demonstrated = 100× scale-up |
| Closure mechanism | Steam Rankine at MANTA/commercial scale is off-the-shelf technology (TRL 9). Thermal storage sizing for pulsed fusion is straightforward engineering (CSP tank design scaled to 2-min buffering vs. 10-hour storage — much smaller tanks required). Advanced Brayton for higher efficiency (45–58%) requires sCO₂ turbine scale-up (DoE Supercritical CO₂ Power Cycle Program, 2025–2035 timeline for 100–300 MWe demonstrations) |
| Classification | **Degrading** — BOP equipment failures (turbine, condenser, thermal storage pumps) cause plant outages (3–12 months for major turbine replacement, 1–3 months for auxiliary equipment) and reduce availability by 5–15 percentage points, but are recoverable with standard power-plant maintenance. Does not prevent long-term operation |
| Evidence tier | **5** (operating-regime demonstrated at commercial scale) — Steam Rankine cycle and molten-salt thermal storage are fully operational in existing CSP and nuclear plants at MANTA scale and above. Turbine-generator sets at 100–1500 MWe are commodity equipment. Advanced Brayton (sCO₂) for higher efficiency is tier 3–4 (pilots operational, scale-up underway) but not required for baseline MANTA design (uses steam Rankine). Composite: **tier 5** for MANTA baseline BOP (steam Rankine + molten-salt storage at demonstrated scale) |

