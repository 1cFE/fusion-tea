# D1+ Analysis: Negative Triangularity Tokamak (Firefly Fusion)

**Concept**: Negative Triangularity (NT) HTS Tokamak — D-T fuel
**Company**: Firefly Fusion (Lausanne/Cadarache; founded 2024)
**Prototype**: LUCIOLE (copper magnets, pre-commercial)
**Confinement Family**: MFE — Tokamak (Negative Triangularity)

---

## Section 1: Availability of Data

**Rating: Limited**

The NT tokamak concept sits in an unusual position: the underlying plasma physics is moderately well-documented through independent academic work, but Firefly Fusion itself — the only private company developing this approach — is effectively opaque. The "Limited" rating reflects that a published reference design (MANTA) exists and provides real engineering anchors, but Firefly has disclosed almost no proprietary parameters and the concept remains less experimentally validated than conventional positive-triangularity tokamaks.

**Published reference design:**
The MANTA study (Rutherford et al. 2024, MIT/community authors) is the single most important data source for this analysis. MANTA is a community-authored conceptual design for an NT ARC-class pilot plant producing 450 MW fusion power at Q=11.5 with a net electrical output of 90 MWe. It provides a complete plant parameter set, systems-level cost breakdown (overnight cost $3.4B), and LCOE projections. The MANTA team explicitly positions NT as enabling a "simpler, conventional divertor" compared to positive-triangularity devices [manta-reference-design.md §Abstract]. MANTA is the primary engineering foundation for this analysis.

> "Systems-level economic analysis estimates an overnight cost of US$3.4 billion, meeting the NASEM FPP requirement that this first-of-a-kind be less than US$5 billion."
> — manta-reference-design.md, §Abstract

**Physics basis — ohmic NT feasibility:**
Balestri, Ball, and Coda (2024) — co-authored by Firefly co-founder Justin Ball — provides the physics basis for the most radical NT economic argument: that a compact, high-field NT tokamak could operate with ohmic heating alone, eliminating auxiliary heating systems entirely. The paper demonstrates analytically and numerically that for a MANTA-class device at the Greenwald density limit, ohmic heating alone could achieve Q ≈ 500, compared to Q ≈ 30 with 40 MW external heating [ball-balestri-ohmic-nt-paper.md §Numerical results]. For a SPARC-class device, ohmic NT achieves Q = 80 vs. Q ≈ 12 for heated positive-triangularity H-mode. These results are from a zero-dimensional power balance model — not validated in a burning plasma — but they represent the most quantitatively specific claim available for Firefly's underlying hypothesis.

**Experimental validation of NT physics:**
NT plasma behavior has been studied on DIII-D (General Atomics) and TCV (EPFL/SPC). Firefly's collaboration with DIII-D is documented, focused on "diagnostics, edge physics, and control strategies" for NT plasmas [firefly-fusion-diii-d-collaboration.md]. These experiments validate the core NT claim — that L-mode confinement in NT is enhanced relative to conventional L-mode — but do not reach burning-plasma or reactor-relevant parameters.

**Firefly Fusion transparency:**
Firefly has disclosed: CEO background (Rustem Ospanov, CERN/Fermilab experimental physics); device target parameters (R=2–2.5 m, B=10–12 T HTS, Q>5, P_fusion=50–100 MW); prototype name (LUCIOLE); approach (copper magnets for LUCIOLE, HTS for commercial); and key advisors (Kikuchi — NT plasma expert; Bucalossi — WEST director; Huguet — former ITER/JET director) [greyb-firefly-interview.md, firefly-fusion-diii-d-collaboration.md]. The March 2026 company website discloses no technical parameters beyond general mission statements [firefly-website-2026.md].

> "Firefly's mission is to rapidly demonstrate burning plasmas by building an affordable, actively-cooled copper-magnet tokamak as a first step toward commercial fusion deployment"
> — firefly-fusion-diii-d-collaboration.md

**Independent analyses:**
No independent TEA exists specifically for NT tokamaks. The MANTA study is the closest. Standard MFE tokamak TEA tools (PROCESS/UKAEA, Araiinejad & Shirvan 2025, ARIES studies) apply to the underlying tokamak architecture but do not incorporate NT-specific modifications to divertor cost structure or heating system reduction.

**Key data gaps limiting this analysis:**
1. Firefly has no published plasma parameter set — all Firefly-specific parameters are aspirational statements from press materials
2. No commercial-scale NT tokamak plant study exists — MANTA targets 90 MWe net, far below commercial viability
3. NT confinement at burning-plasma conditions is unvalidated — all experimental data is from non-burning L-mode plasmas
4. Firefly's blanket design, tritium breeding approach, and power conversion cycle are entirely undisclosed

---

## Section 2: Challenges in Capturing System Function

The NT tokamak shares the standard D-T tokamak LCOE modeling challenges (magnet cost uncertainty, capacity factor, blanket and tritium cycle maturity) but adds several NT-specific uncertainties. The NT geometry also introduces a potential economic *advantage* — if divertor simplification and heating elimination are validated — that is equally hard to quantify. Challenges are ranked by impact on LCOE uncertainty.

**1. NT confinement scaling to burning-plasma conditions — the physics anchor is unvalidated (Impact: Critical)**

The entire NT economic case rests on the claim that NT L-mode confinement, as observed on TCV and DIII-D, scales favorably to reactor conditions. The MANTA study explicitly acknowledges this: "Compared to positive triangularity, negative triangularity is far less understood... Further experimental data, especially with regards to radiative ELM-free plasmas, is required to provide greater confidence that NT can scale to a reactor-class tokamak" [manta-reference-design.md §8]. The confinement factors H_NA (ohmic enhancement for NT), H_98 (H-mode-equivalent scaling), and H_89 used in Ball et al. "represent the biggest uncertainty in predicting how a NT plasma will behave" [ball-balestri-ohmic-nt-paper.md §Appendix B]. If NT confinement does not maintain its advantage at high plasma pressure and high-Z impurity concentrations, the key cost-reduction claims collapse. There is no analogue for this uncertainty in conventional tokamak analysis — ITER, SPARC, and ARC all extrapolate from a much richer H-mode database.

**2. Net electric output is very low — commercial scaling path unknown (Impact: Critical)**

MANTA, the primary reference design, produces only 90 MWe net from 450 MW fusion power. The Q_e (electrical gain) of 2.4 is better than break-even but far from commercial viability. MANTA's own LCOE projection for a scaled 550 MW device over 30 years is US$396/MWh — roughly 3× offshore wind costs. The MANTA authors identify the path to viability as requiring: extended magnet lifetimes (56% LCOE reduction), higher thermal efficiency via elevated operating temperatures, and fusion power approaching 1 GW [manta-reference-design.md §7.2]. None of these parameters are characterized for Firefly's smaller 50–100 MW fusion power target, which would produce even less net electricity at similar recirculating power fractions. There is currently no credible path from Firefly's stated design point to commercial LCOE targets without major upscaling and technology improvements.

**3. Ohmic-only hypothesis: compelling but unvalidated (Impact: High)**

Ball et al.'s central result — that NT L-mode at high density can achieve Q ≈ 500 with zero auxiliary heating — depends on the ohmic confinement enhancement factor H_NA = 2 being sustained in a reactor-scale plasma. The paper notes this is based on "a preliminary analysis of the TCV NT database" [ball-balestri-ohmic-nt-paper.md §Appendix B]. If H_NA ≈ 1 (no enhancement relative to standard ohmic scaling), ohmic heating at compact device sizes may be insufficient to reach burning-plasma conditions, and a full auxiliary heating system (40–100 MW, ~$100–500M capital) would be required. The difference between Q ≈ 500 (ohmic) and Q ≈ 12 (full heating) has enormous implications for recirculating power fraction and operating cost. This uncertainty cannot currently be resolved without experiments on larger NT devices.

**4. Dominant cost driver unchanged — TF coils are ~44% of plant cost (Impact: High)**

MANTA shows that the toroidal field coil cost ($1.5B of $3.4B total) is the single largest cost driver, completely independent of the NT geometry choice [manta-reference-design.md §7.1]. NT's economic benefits — divertor simplification, heating elimination — address secondary cost categories, not the dominant driver. Any NT cost model must first anchor the magnet cost correctly (which depends on REBCO tape pricing, coil geometry, and field strength) before NT-specific savings become meaningful. The NT-vs.-PT cost differential may be 10–30% of total plant cost if divertor and heating advantages materialize, but the magnet cost floor creates a hard lower bound that NT cannot overcome.

> "The toroidal field coil cost and replacement time are the most critical upfront and lifetime cost drivers, respectively."
> — manta-reference-design.md, §Abstract

**5. Divertor simplification — real but unquantified (Impact: Moderate)**

The most concrete NT economic advantage is the simpler divertor. NT geometry moves the X-points to larger major radius, increasing divertor target area by ~50% and enabling radiative exhaust at very low scrape-off-layer power. MANTA achieves P_SOL = 23.5 MW for 450 MW fusion power — an exhaust fraction of only 5.2%, compared to 15–25% for a typical positive-triangularity design [manta-reference-design.md §3]. This eliminates the need for exotic liquid-metal or "snowflake" divertor concepts and allows a conventional tungsten monoblock design. The capital and maintenance cost savings are not directly quantified in MANTA, but a simpler divertor implies higher availability (less divertor replacement downtime) and lower engineering risk.

> "MANTA's radiative and NT operation permits a much simpler, conventional divertor to meet the reactor power exhaust challenge"
> — manta-reference-design.md, §3

**6. Quasi-steady pulsed operation — thermal buffering cost (Impact: Moderate)**

Like ARC-class conventional tokamaks, MANTA operates with ~15-minute inductive pulses and 2-minute inter-pulse dwell periods. The pulsed thermal output requires molten-salt thermal energy storage to produce a steady grid output. This thermal buffer system is a capital cost item absent from steady-state designs; its sizing and cost for the specific NT design point have not been published separately from MANTA's overall plant cost. The 15-min pulse / 2-min dwell cycle yields ~88% duty cycle thermally, but the ~37% capacity factor in MANTA reflects additional planned maintenance downtime.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature.

---

**NT Confinement at Reactor Scale — TRL 2–3**

- **Demonstrated**: NT L-mode plasmas on TCV (EPFL/SPC) and DIII-D (General Atomics) confirming enhanced L-mode confinement vs. positive triangularity, absence of ELMs in NT geometry, and improved heat exhaust. Firefly collaboration with DIII-D focuses on "diagnostics, edge physics, and control strategies" [firefly-fusion-diii-d-collaboration.md]. MANTA uses H_98 = 1.44 as the design confinement factor, supported by TCV/DIII-D data.
- **On paper only**: NT confinement at high fusion power densities (α-particle heating regime). Radiative ELM-free operation with high impurity seeding at reactor-relevant density and temperature. Ohmic NT operation with H_NA ≥ 2 confinement enhancement at compact high-field conditions [ball-balestri-ohmic-nt-paper.md §Appendix B].
- **Missing at scale**: Burning-plasma NT experiment at reactor-relevant Q. Demonstration that NT confinement advantage persists with high alpha-particle pressure. Validation of density peaking predictions (MANTA's TGLF model "has shown significant variability" [manta-reference-design.md §2.2.2]). NT disruption characterization at high plasma current and energy.

---

**FLiBe Liquid Immersion Blanket — TRL 2–3**

- **Demonstrated**: Small-scale FLiBe chemistry experiments. ITER Test Blanket Module program includes helium-cooled and liquid-metal breeder concepts. Lab-scale tritium breeding from lithium.
- **On paper only**: Full-scale FLiBe liquid immersion blanket as implemented in MANTA — toroidally continuous tank serving as breeder, coolant, and shield simultaneously with TBR = 1.15 [manta-reference-design.md §5.1]. Self-healing molybdenum barrier via MoF₆ in FLiBe. FLiBe-compatible vacuum vessel V-4Cr-4Ti corrosion and compatibility at operating temperature.
- **Missing at scale**: Continuous tritium extraction from FLiBe at kg/day throughput. FLiBe-to-molten-salt heat exchanger at commercial scale ("low technological readiness level" explicitly noted in MANTA [manta-reference-design.md §6.3]). 14 MeV neutron irradiation database for V-4Cr-4Ti vacuum vessel at fusion-relevant fluence.

---

**Tritium Fuel Cycle — TRL 3–4**

- **Demonstrated**: Lab-scale tritium handling. MANTA designs around 75g reserve inventory and 440g startup inventory [manta-reference-design.md §5.4]. JET and TFTR operated gram-level tritium inventories.
- **On paper only**: Closed-loop kg/day-scale tritium breeding and extraction from FLiBe. MANTA acknowledges "a fully functioning tritium fuel cycle has yet to be developed or tested, so the following model employs conservative estimates" [manta-reference-design.md §5.4].
- **Missing at scale**: Industrial tritium processing for FLiBe-cooled NT tokamak. Demonstrated TBR > 1.0 under realistic conditions with blanket penetrations for diagnostics and heating access.

---

**Heating and Current Drive — TRL 3–5 (if ohmic-only); TRL 5–7 (if ICRF required)**

- **Demonstrated**: MANTA uses 40 MW ICRF (He-3 minority at 110 MHz) for auxiliary heating — mature technology at 40 MW scale on JET, WEST, and other tokamaks. Ohmic heating is the oldest plasma heating method and universally demonstrated. Firefly's "microwaves" claim [venture-kick-profile.md] may indicate ECRH, though MANTA uses ICRF.
- **On paper only**: Ohmic-only burning-plasma NT operation — the Ball et al. scenario [ball-balestri-ohmic-nt-paper.md §Numerical results] has never been attempted at any scale. Q = 500 from ohmic heating is a theoretical extrapolation from 0D power balance.
- **Missing at scale**: Validated ohmic ignition (or near-ignition) at compact high-field NT conditions. If ICRF is required: continuous-wave ICRF antenna design surviving the fusion neutron environment with multi-year lifetime. MANTA notes detailed antenna design was "outside the scope of this study" [manta-reference-design.md §2.1].

---

**Remote Maintenance System — TRL 4–6**

- **Demonstrated**: ITER remote handling prototypes at full scale. MANTA's design explicitly incorporates demountable TF coils to enable rapid component replacement; PF2 coil requires replacement approximately every 2 full-power-years [manta-reference-design.md §5.2, Table 7].
- **On paper only**: Complete remote maintenance cycle for MANTA or Firefly design — blanket module extraction, PF coil replacement, vacuum vessel exchange at the ~2-year cycle time driven by PF2 lifetime limits.
- **Missing at scale**: Radiation-hardened robotics for NT tokamak geometry with demountable TF coil architecture. Remote maintenance cycle time validation against availability targets.

---

**HTS Magnets (REBCO) — TRL 6–7**

- **Demonstrated**: MANTA's REBCO-based design targets 11 T at 47.2 kA with 40% margin to critical current, 20 K liquid hydrogen cooling, non-insulated TF coils [manta-reference-design.md §4]. CFS demonstrated a 20 T REBCO single coil (2021). Tokamak Energy Demo4 achieved 11.8 T in a complete 14 TF + 2 PF coil set (2025). Firefly targets 10–12 T HTS for commercial plants [greyb-firefly-interview.md].
- **On paper only**: NT-specific TF coil geometry — MANTA uses 18 TF coils with demountable joints; the connection between demountability and NT plasma shape imposes specific coil geometry constraints not faced by conventional tokamaks.
- **Missing at scale**: REBCO tape performance under cumulative 14 MeV neutron + gamma irradiation at commercial plant fluence. MANTA estimates REBCO tolerance to 3×10²² n/m² but notes this is extrapolated [manta-reference-design.md §4]. Full-plant REBCO tape volume at 11 T not published for MANTA.

---

**Divertor — TRL 5–7 (with NT advantage)**

- **Demonstrated**: Tungsten monoblock divertors tested at >10–20 MW/m² in WEST, GLADIS, DTT. NT's low P_SOL (23.5 MW for 450 MW fusion) creates a substantially more benign divertor environment than comparable positive-triangularity designs. DIII-D experiments confirm NT reduces divertor heat flux significantly.
- **On paper only**: Conventional tungsten divertor at MANTA conditions — the design simply requires what tokamak programs have nearly demonstrated, because NT's low P_SOL keeps peak heat flux below established limits.
- **Missing at scale**: Long-term divertor lifetime under NT operating conditions at burning plasma. Remote replacement mechanism in MANTA/Firefly geometry.

---

**Balance of Plant — TRL 7–8 (BOP) / TRL 3–4 (FLiBe–molten-salt interface)**

- **Demonstrated**: Steam Rankine cycle at GW scale. Molten-salt secondary loops in concentrated solar (NaNO₃/KNO₃ binary salt is the CSP standard, the same as MANTA's secondary loop [manta-reference-design.md §6.3]).
- **On paper only**: Integration of FLiBe primary loop with NaNO₃/KNO₃ secondary via molten-salt heat exchanger at fusion-plant scale. Thermal energy storage buffer sized for MANTA's 15-min/2-min pulse cycle.
- **Missing at scale**: Molten-salt heat exchanger technology for FLiBe-to-secondary coupling — MANTA explicitly notes "low technological readiness level" [manta-reference-design.md §6.3]. Tritium permeation through heat exchanger surfaces.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape — Critical Bottleneck (shared with HTS tokamak family)**

MANTA's TF coils require REBCO tape at 11 T, 47.2 kA, with 40% margin to critical current. Total tape demand for a full MANTA-scale plant has not been published but is on the order of thousands of km, comparable to ARC-class designs. REBCO production is ramping but remains at thousands km/year globally vs. 5,000+ km needed per plant [01-hts-compact-tokamak analysis, Section 4]. The MANTA cost sensitivity study showed ±50% variation in REBCO tape cost produces bounded overall plant cost uncertainty (within the $5B NASEM cap) [manta-reference-design.md §7.1, Fig. 25]. This relative insensitivity occurs because TF coil cost is dominated by quantity of tape, not unit price at the margin; however, it does not eliminate the supply-chain volume constraint.

**FLiBe (2LiF·BeF₂) — Supply Chain Constrained by Beryllium**

MANTA uses FLiBe as the liquid immersion blanket material (blanket coolant, tritium breeder, and shield) with a TBR of 1.15. FLiBe requires beryllium, which is produced globally at ~300 tonnes/year, dominated by Materion Corp. (US). A single MANTA-scale reactor requires substantial FLiBe inventory; fleet-scale deployment would compete with other beryllium uses. Li-6 enrichment (standard lithium is 7.5% Li-6) is also required for adequate breeding; enrichment capacity is controlled by Russia and China using legacy mercury amalgam processes with limited Western alternatives. Araiinejad & Shirvan (2025) estimate NOAK FLiBe cost at ~$154/kg assuming a 20% learning rate. This is the same supply chain constraint as the CFS ARC design; NT geometry does not change this requirement.

**V-4Cr-4Ti Vacuum Vessel — Advanced Alloy with No Commercial Production**

MANTA specifies a V-4Cr-4Ti vacuum vessel (~1 cm thick) for its 3-orders-of-magnitude lower activation relative to stainless steel [manta-reference-design.md §5.3]. V-4Cr-4Ti has never been produced at the multi-hundred-tonne scale required for a full vacuum vessel. Commodity vanadium is available (~100,000 t/year), but nuclear-grade V-4Cr-4Ti with controlled impurities has no industrial supply chain. The MANTA team notes that future material options (ODS ferritic steels, SiC-SiC composites) depend on technology readiness [manta-reference-design.md §5.1], suggesting the vacuum vessel material choice is not yet locked.

**Tritium — Declining Supply (Standard D-T Constraint)**

Global tritium inventory ~25–30 kg, decaying at 5.5%/year from CANDU reactor byproduction. Startup requirement ~440g (MANTA's conservative estimate [manta-reference-design.md §5.4]), growing toward ~1 kg as fuel cycle systems mature. MANTA's design includes a 75g operational reserve with a 15-minute tritium system hold-up inventory. NT geometry does not change this fundamental constraint — the same CANDU-supply sequencing issue applies as for all D-T concepts. The TBR = 1.15 design target provides adequate breeding margin once the fuel cycle is operational.

**Tungsten (First Wall and Divertor) — Supply Adequate, NT Demand Significantly Reduced**

NT's low P_SOL substantially reduces tungsten divertor component replacement rates relative to a positive-triangularity device at the same fusion power. MANTA's conventional tungsten monoblock design at 2.8 MW/m² peak heat flux [manta-reference-design.md §Table 1] is below the demonstrated endurance limit of modern tungsten tiles, potentially enabling longer divertor lifetime. This is a meaningful NT supply chain advantage: lower divertor erosion rates may extend replacement intervals from ~5 years (typical high-heat-flux PT assumption) toward ~10 years, reducing tungsten consumption and maintenance costs. Quantitative estimates require detailed modeling not yet performed.

**Molten-Salt Heat Exchanger Components — Novel, Low-TRL Supply Chain**

MANTA's secondary thermal loop uses NaNO₃/KNO₃ binary salt with a two-stage heat exchanger design. FLiBe-to-salt heat exchangers are not commercially available and represent a nascent supply chain. The concentrated solar power industry provides some manufacturing base for molten-salt components, but the temperature range, corrosion environment, and tritium-permeation requirements for fusion are distinct. MANTA explicitly calls this out as a component with "low technological readiness level" [manta-reference-design.md §6.3].

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| **MANTA Reference Design Parameters** | | | | |
| Major radius (R₀) | 4.55 m | manta-reference-design.md §Table 1 | high | Community reference design; not Firefly's target |
| Minor radius (a) | 1.2 m | manta-reference-design.md §Table 1 | high | Aspect ratio 3.79 |
| Toroidal field (B₀) | 11 T | manta-reference-design.md §Table 1 | high | REBCO HTS; 20 K, liquid H₂ cooling |
| Plasma current (Iₚ) | 10 MA | manta-reference-design.md §Table 1 | high | |
| Plasma gain (Q) | 11.5 | manta-reference-design.md §Table 1 | high | |
| Fusion power (P_fus) | 450 MW | manta-reference-design.md §Table 1 | high | |
| Net electrical output | 90 MWe | manta-reference-design.md §Table 1 | high | Pilot plant; far below commercial scale |
| Electrical gain (Q_e) | 2.4 | manta-reference-design.md §Table 1 | high | Net electric / auxiliary heating power |
| Scrape-off layer power (P_SOL) | 23.5 MW | manta-reference-design.md §Table 1 | high | 5.2% of fusion power — very low vs. PT designs |
| Peak divertor heat flux | 2.8 MW/m² | manta-reference-design.md §Table 1 | high | Well within tungsten monoblock demonstrated limits |
| Normalized beta (βN) | 1.45 | manta-reference-design.md §Table 1 | high | Conservative; NT does not require high beta |
| Confinement factor (H₉₈) | 1.44 | manta-reference-design.md §Table 1 | high | Achieved in L-mode — key NT advantage claim |
| Triangularity (δ) | -0.5 | manta-reference-design.md §Table 1 | high | Strongly negative; defines NT operating regime |
| Auxiliary heating power | 40 MW ICRF | manta-reference-design.md §2.1 | high | He-3 minority heating at 110 MHz |
| Pulse length | 15 min | manta-reference-design.md §Operation | high | Inductive burn; CS re-magnetization during inter-pulse |
| Inter-pulse dwell | 2 min | manta-reference-design.md §Operation | high | Thermal duty cycle ~88% |
| Capacity factor (pilot) | ~37% | manta-reference-design.md §7.2 | medium | Pilot plant estimate incl. planned maintenance downtime |
| Blanket type | FLiBe liquid immersion | manta-reference-design.md §5.1 | high | Toroidally continuous; dual breeder/coolant/shield |
| Tritium breeding ratio (TBR) | 1.15 | manta-reference-design.md §5.1 | high | Adequate margin for self-sufficiency |
| Blanket power multiplication | 1.11 | manta-reference-design.md §5.1 | high | |
| Vacuum vessel material | V-4Cr-4Ti | manta-reference-design.md §5.3 | high | ~3 orders lower activation than SS316LN |
| TF coil lifetime | 3,100 ± 400 MW·yr (minimum) | manta-reference-design.md §5.2 | medium | Far exceeds 1,000 MW·yr target |
| PF2 coil lifetime (limiting) | ~890 MW·yr minimum | manta-reference-design.md §5.2, Table 7 | medium | ~2 full-power-years; sets maintenance cycle |
| **MANTA Cost Parameters** | | | | |
| Overnight capital cost | $3.4B | manta-reference-design.md §7.1 | high | Pilot plant; community design |
| TF coil cost | $1.5B | manta-reference-design.md §7.1 | high | ~44% of total plant cost; dominant cost driver |
| Tokamak system cost | $3.1B | manta-reference-design.md §7.1 | high | ~89% of total; balance is BOP |
| Unit capital cost | ~$38M/MWe | manta-reference-design.md §7.1 | medium | Derived: $3.4B / 90 MWe; far above commercial targets |
| LCOE (scaled 550 MW device) | $396/MWh | manta-reference-design.md §7.2 | medium | 30-year study; ~3× offshore wind; requires significant improvements |
| **Firefly Fusion Target Parameters** | | | | |
| Major radius (Firefly target) | 2–2.5 m | greyb-firefly-interview.md | medium | Aspirational; no design study published |
| Toroidal field (Firefly target) | 10–12 T | greyb-firefly-interview.md | medium | HTS commercial; copper for LUCIOLE |
| Plasma gain (Firefly target) | Q > 5 | greyb-firefly-interview.md | medium | "> 100 MW fusion from 20–30 MW heating" |
| Fusion power (Firefly target) | 50–100 MW | greyb-firefly-interview.md | medium | Aspirational; approximately 5× smaller than MANTA |
| **Ball et al. Ohmic NT Parameters** | | | | |
| Theoretical Q (ohmic MANTA-class) | ~500 | ball-balestri-ohmic-nt-paper.md §Numerical results | low | 0D power balance; H_NA=2 assumed; unvalidated |
| Theoretical Q (ohmic SPARC-class) | ~80 | ball-balestri-ohmic-nt-paper.md §Numerical results | low | Same model; much higher than PT H-mode Q=12 |
| Ohmic heating power (eliminated) | 0 MW (vs. 40 MW ICRF) | ball-balestri-ohmic-nt-paper.md §Conclusions | low | Represents entire auxiliary heating capital saving |
| **Analogue Parameters from HTS Tokamak Family** | | | | |
| REBCO tape cost (current) | $30–100/kA-m | 01-hts-compact-tokamak analysis §4 | medium | Commercial viability target ~$10/kA-m |
| Tritium inventory (global) | ~25–30 kg | 01-hts-compact-tokamak analysis §4 | high | Shared constraint for all D-T concepts |
| Tritium market price | >$35,000/g | 01-hts-compact-tokamak analysis §4 | medium | |
| FLiBe NOAK cost | ~$154/kg | Araiinejad & Shirvan 2025 [01-hts-compact-tokamak analysis] | medium | Assumes 20% learning rate |
| Regulatory cost multiplier (fission-style) | 2.2× building cost | Stewart & Shirvan 2022 [01-hts-compact-tokamak analysis] | medium | Upper-bound scenario for all D-T concepts |
| Capacity factor (D-T MCF range) | 75–90% | Araiinejad & Shirvan 2025 [01-hts-compact-tokamak analysis] | medium | Commercial plant target; MANTA's 37% is pilot-plant specific |

---

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Firefly plasma parameter set (complete) | proprietary | blocking | No Q, I_p, β, confinement factor, or auxiliary heating target published for Firefly's specific design |
| Net electrical output for Firefly design | proprietary | blocking | Firefly targets 50–100 MW fusion power; net electric derivation requires efficiency and recirculating power assumptions not yet disclosed |
| Commercial-scale NT plant cost estimate | truly-unknown | blocking | MANTA is a pilot plant ($3.4B, 90 MWe); no study for a 1 GW+ commercial NT tokamak exists |
| Thermal efficiency for NT tokamak commercial plant | not-yet-sourced | blocking | MANTA uses steam Rankine at low efficiency; commercial plant targets higher temperatures and cycles not specified |
| NT confinement validation at Q > 1 | truly-unknown | blocking | No burning NT plasma data exists anywhere; all physics extrapolated from L-mode non-burning experiments |
| Firefly blanket and tritium system design | proprietary | blocking | No disclosure from Firefly; MANTA FLiBe is a proxy but Firefly's design may differ |
| LUCIOLE prototype parameters | proprietary | important | Copper magnets, NT design; no published parameter set |
| Ohmic NT confinement enhancement (H_NA) validation | truly-unknown | important | Ball et al. use H_NA = 2 from preliminary TCV data; not validated beyond 0D estimate |
| Auxiliary heating capital cost (NT reduction vs. PT) | derivable | important | Savings = cost of 40 MW ICRF system (~$100–300M) if ohmic-only works; depends on validation |
| Divertor cost differential (NT vs. PT) | not-yet-sourced | important | NT simpler divertor quantified in MANTA design philosophy but not separately cost-estimated |
| Capacity factor for Firefly commercial plant | proprietary / not-yet-sourced | important | MANTA 37% is pilot-specific; commercial NT tokamak availability target unknown |
| V-4Cr-4Ti vacuum vessel industrial supply | truly-unknown | nice-to-have | No commercial production of nuclear-grade V-4Cr-4Ti; cost unknown |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | NT confinement scaling to burning plasma — H_NA, H₉₈ at reactor conditions unvalidated | S1, S2, S3 | truly-unknown | blocking | DIII-D/TCV NT database; future burning NT experiment (none planned); Ball et al. TCV analysis as intermediate step |
| 2 | Firefly complete plasma parameter set (Q, Ip, beta, heating power, plant size) not published | S1, S5 | proprietary | blocking | Watch for Firefly technical publications or conference presentations; company is pre-publication stage |
| 3 | Commercial-scale NT plant cost study does not exist — MANTA is a sub-commercial pilot | S1, S2, S5 | truly-unknown | blocking | Extend MANTA cost model to 1 GW+ fusion power; apply PROCESS/ARIES frameworks to NT geometry |
| 4 | Net electric output derivable only with efficiency and recirculating power assumptions | S2, S5 | derivable | blocking | For MANTA proxy: known (90 MWe); for Firefly: use 50–100 MW fusion × analogued efficiency chain |
| 5 | Ohmic-only NT feasibility — H_NA = 2 is preliminary and model-dependent | S2, S3, S5 | truly-unknown | blocking | Requires larger NT device experiments; TCV upgrade or DIII-D dedicated NT campaign |
| 6 | Thermal efficiency for commercial NT plant undisclosed | S2, S5 | not-yet-sourced | blocking | Apply STEP/ARIES steam Rankine and sCO₂ Brayton studies to NT plant parameters as analogues |
| 7 | Firefly blanket design, TBR target, and tritium system not disclosed | S1, S4, S5 | proprietary | blocking | MANTA FLiBe design is the best available proxy; Firefly's ARC-class heritage makes FLiBe likely |
| 8 | Divertor cost differential NT vs. PT not separately quantified in MANTA study | S2, S5 | not-yet-sourced | important | Requires detailed divertor design cost study; use tokamak divertor cost analogue from ARIES studies |
| 9 | Auxiliary heating capital cost saving (if ohmic-only validated) not estimated | S2, S5 | derivable | important | Estimate: ICRF system cost ~$100–300M for 40 MW; represents ~3–9% of total plant cost |
| 10 | Capacity factor for a commercial NT plant — MANTA 37% is pilot-plant-specific | S2, S5 | not-yet-sourced | important | Apply D-T MCF range (75–90% per Araiinejad & Shirvan) with NT-specific upside from simpler divertor |
| 11 | FLiBe–molten-salt heat exchanger design and cost at MANTA/commercial scale | S3, S4, S5 | truly-unknown | important | Low-TRL acknowledged in MANTA; CSP industry salt HX as cost analogue only |
| 12 | V-4Cr-4Ti vacuum vessel industrial supply chain and cost | S4, S5 | truly-unknown | nice-to-have | Review fission breeder literature; consult EUROFER/vanadium alloy programs |
| 13 | REBCO tape total demand for MANTA-scale TF coil set | S4, S5 | not-yet-sourced | nice-to-have | Derivable from MANTA TF coil geometry if dimensions published; Tokamak Energy Demo4 scaling as analogue |
| 14 | NT disruption characteristics and wall impact at high plasma current | S3 | not-yet-sourced | nice-to-have | DIII-D NT disruption experiments; review TCV data |

---

## Section 7: Cross-Concept Notes

The approved analysis for the Spherical Tokamak - HTS (`21-spherical-tokamak-hts`, Tokamak Energy) is the only approved prior analysis available. While the concept family (D-T HTS tokamak) is shared, the NT and spherical tokamak diverge substantially in geometry, operating regime, and key challenges. Cross-referencing is productive for shared supply chain constraints, but the TEA implications are distinct.

**Reused assumptions from 21-spherical-tokamak-hts:**

- **REBCO tape supply chain**: Global production bottleneck (~thousands km/year capacity), current pricing ($30–100/kA-m), commercial viability target (~$10/kA-m). These figures apply equally to NT tokamak REBCO requirements [21-spherical-tokamak-hts analysis §4]. Both MANTA and Tokamak Energy's ST-E1 use REBCO at similar field strengths (~11 T).
- **D-T tritium fuel cycle constraints**: Global inventory (~25–30 kg), startup inventory (~440–1,000g), CANDU-decline sequencing, self-sufficiency requirement (TBR > 1.0). Identical constraint for all D-T concepts.
- **Regulatory cost scenario**: Stewart & Shirvan 2.2× building cost factor applies to NT tokamak as a D-T fusion device, exactly as for ST-E1.
- **Capacity factor sensitivity**: Araiinejad & Shirvan (2025) 75–90% range applies as a commercial plant target. NT's simpler divertor may provide upside to this range, but this is not yet quantified.
- **FLiBe supply chain**: Both MANTA (NT tokamak) and CFS ARC (conventional tokamak) use FLiBe blankets. The beryllium and Li-6 supply constraints are shared; Araiinejad & Shirvan's $154/kg NOAK FLiBe estimate applies equally.

**Key divergences from 21-spherical-tokamak-hts:**

- **Divertor challenge**: Tokamak Energy's ST-E1 shares the conventional positive-triangularity divertor challenge — managing high P_SOL per unit divertor area with MAST-U Super-X geometry. NT tokamak's P_SOL = 23.5 MW for 450 MW fusion is dramatically lower than any comparable PT design, fundamentally changing the divertor engineering problem. NT eliminates the need for advanced divertor concepts (Super-X, snowflake, liquid metal) — a meaningful capital and risk reduction not present in the ST-E1 analysis.
- **Heating system**: ST-E1 uses ECRH exclusively at flat-top (~50–55% wall-plug efficiency), creating a significant recirculating power fraction. NT tokamak may use ICRF at lower power (MANTA: 40 MW) or potentially ohmic-only (Ball et al.). If ohmic-only is validated, the NT concept eliminates the entire auxiliary heating capital cost — a divergence not present in any other approved tokamak analysis.
- **Physics maturity**: ST-E1 extrapolates from a rich H-mode database with ITER, JET, and SPARC as near-neighbors. NT tokamak extrapolates from a much thinner L-mode database with no burning-plasma NT experiments. The physics uncertainty is higher for NT despite sharing the same confinement family.
- **Aspect ratio**: MANTA operates at A = 3.79 (conventional tokamak), vs. ST-E1 at A = 2.3 (spherical tokamak). The different geometry eliminates the ST center-stack shielding challenge (Section 3 of ST-E1 analysis) but introduces NT-specific plasma shaping requirements.
- **Magnet and geometry cost structure**: ST-E1's dominant cost challenge is the compact center stack with WC cermet shielding and outboard-only blanket. NT tokamak at MANTA geometry has a more conventional aspect ratio and standard inboard/outboard coverage. The NT cost challenge is the TF coil cost dominance ($1.5B of $3.4B) — same structural driver as ST-E1 but without the ST-specific geometry complications.
- **Data availability**: ST-E1 has published machine parameters (R=5.0 m, A=2.3, B=5.25 T, 450–750 MWe net, TBR=1.2) from DPP 2025. MANTA has a more complete published parameter set. Firefly has less than ST-E1. For direct Firefly modeling, MANTA is the only available anchor.

**NT tokamak-specific TEA features not in other approved analyses:**

1. **Ohmic-only scenario branch**: No other approved concept eliminates auxiliary heating as a scenario. A two-branch TEA model (with/without heating system) should capture the Q ≈ 30 (with ICRF) vs. Q ≈ 500 (ohmic) divergence and its cost implications.
2. **Divertor cost and availability premium**: NT's simpler divertor and lower P_SOL should be represented as a cost line item reduction and a capacity factor uplift relative to conventional PT tokamaks. Quantification requires divertor-specific cost modeling.
3. **Physics validation risk as scenario parameter**: Unlike other MFE concepts where confinement scaling is better established, the NT confinement factor uncertainty (H_NA = 1.0 vs. 2.0) should be treated as a scenario branch rather than a sensitivity parameter.

---

## Section 8: Sources

**1. Rutherford, G. et al. (2024) — MANTA NT Tokamak Reference Design**
- Full citation: Rutherford, G., Bhatt, N., Calvo-Carrera, M., Chandra, R., Cler, D., DePaolo, K., Dunn, K., Golfinopoulos, T., Hartwig, Z., Maris, A., Qian, L., Rhodes, R., Rodriguez Fernandez, P., Sing Chaudhari, C., Wai, J., White, A., Witkowski, P., Wigram, M., Zweben, S., Whyte, D. (2024). "MANTA: A Negative-Triangularity Tokamak Pilot Plant Concept." arXiv:2405.20243.
- Contribution: Complete NT tokamak pilot plant parameter set (R=4.55 m, B=11 T, Q=11.5, P_fus=450 MW, P_net=90 MWe), systems-level cost breakdown ($3.4B overnight, $1.5B TF coils), LCOE projections ($396/MWh for scaled device), materials choices (FLiBe blanket, V-4Cr-4Ti VV, REBCO HTS), operational parameters (15 min pulses, TBR=1.15), and explicit discussion of NT advantages and data gaps. Primary engineering foundation for this analysis.
- Location: `iter-02/sources/manta-reference-design.md`

**2. Balestri, A., Ball, J., and Coda, S. (2024) — Ohmic NT Tokamak Feasibility**
- Full citation: Balestri, A., Ball, J., and Coda, S. (2024). "Ohmic tokamaks with negative triangularity: a path to net energy." arXiv:2407.06439v2.
- Contribution: Physics basis for ohmic-only operation in NT tokamaks. Demonstrates theoretically that MANTA-class NT device could achieve Q ≈ 500 with ohmic heating only (vs. Q ≈ 30 with 40 MW ICRF). Identifies H_NA confinement enhancement as critical uncertain parameter. Co-authored by Firefly co-founder Justin Ball.
- Location: `iter-01/sources/ball-balestri-ohmic-nt-paper.md`

**3. GreyB / Scouted Interview with CEO Rustem Ospanov (2024)**
- Contribution: Primary Firefly technical parameter disclosure: R = 2–2.5 m, B = 10–12 T HTS, Q > 5, P_fusion = 50–100 MW with 20–30 MW heating. Economic framing ("capital costs comparable to modern power plants"). NT physics motivation (heat management at compact scale). Founder background (CERN/Fermilab).
- Location: `iter-01/sources/greyb-firefly-interview.md`

**4. DIII-D National Fusion Facility — Firefly Collaboration Page**
- Contribution: Confirms DIII-D experimental collaboration for NT physics validation. LUCIOLE prototype identified. Copper magnet strategy for prototype stage. "Diagnostics, edge physics, and control strategies" focus for NT experiments. Confirms NT as scientifically active research area, not purely theoretical.
- Location: `iter-01/sources/firefly-fusion-diii-d-collaboration.md`

**5. Venture Kick (2024) — Firefly Fusion Profile**
- Contribution: "Utilizing microwaves to create and control hot plasma" — primary basis for ECRH heating hypothesis. CHF 50,000 seed funding confirmation. Stage of development (computational analysis).
- Location: `iter-01/sources/venture-kick-profile.md`

**6. Firefly Fusion Website (March 2026)**
- Contribution: Team and advisor bios (Ospanov, Gibson; advisors Kikuchi, Bucalossi, Huguet, Peters). Company framing ("existing technologies... accelerated schedule at the lowest possible cost"). Confirms no technical parameters disclosed as of March 2026.
- Location: `iter-02/sources/firefly-website-2026.md`

**7. Araiinejad, L.S. and Shirvan, K. (2025) — D-T MCF TEA**
- Full citation: Araiinejad, L.S. and Shirvan, K. (2025) "Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants," *Applied Energy*, 401(Part B), 126567. doi:10.1016/j.apenergy.2025.126567.
- Contribution: D-T MCF LCOE sensitivity framework (capacity factor 75–90%, regulatory scenarios, FLiBe NOAK cost $154/kg). Applied as analogue for commercial-scale parameters not available in MANTA or Firefly disclosures.
- Location: Referenced via approved analysis `01-hts-compact-tokamak`

**8. Stewart, W.R. and Shirvan, K. (2022) — Fusion Regulatory Cost Scenario**
- Contribution: 2.2× building cost factor for fission-style nuclear regulation. Applicable to all D-T fusion concepts including NT tokamak.
- Location: Referenced via approved analyses `01-hts-compact-tokamak`, `21-spherical-tokamak-hts`

**9. Approved D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-concept reference for shared HTS magnet supply chain (REBCO tape costs, production capacity), D-T tritium fuel cycle constraints, FLiBe supply chain characterization, regulatory cost scenarios, and capacity factor benchmarks. Also provides contrast for NT-specific divertor simplification and ohmic heating advantages.
- Location: `analyses/21-spherical-tokamak-hts/analysis.md`
