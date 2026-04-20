# D1+ Analysis: p-B11 FRC (TAE Technologies)

**Concept**: Field-Reversed Configuration driven by Neutral Beam Injection — p-B11 aneutronic fuel  
**Company**: TAE Technologies (Mission Viejo, CA)  
**Commercial Design**: Da Vinci (50 MWe initial; 350–500 MWe at scale)  
**Confinement Family**: MFE — FRC (beam-driven)

---

## Section 1: Availability of Data

**Rating: Moderate**

TAE Technologies occupies an unusual position in the transparency spectrum: it is one of the most publicly active private fusion companies by press release and investor communication volume, but its technical disclosures stop well short of what is needed to anchor a closed LCOE model. The company has operated a continuous series of experimental machines (C-2, C-2U, C-2W/Norman, and now Norm) and published physics results in peer-reviewed journals, including a 2025 Nature Communications paper on NBI-only FRC formation. However, the Da Vinci commercial design parameters are almost entirely unpublished beyond a single power output figure (50 MWe) and a rough timeline. The "Moderate" rating reflects real experimental data for the FRC confinement platform, alongside near-total opacity on the commercial plant engineering.

**Experimental physics publications:**  
The C-2W/Norman campaign produced the most detailed published FRC physics dataset for TAE's beam-driven approach. Key parameters are in the public record: ion temperatures up to ~3 keV (total plasma temperature Ttot up to ~3 keV), averaged electron density ~1–3 × 10¹⁹ m⁻³, trapped magnetic flux ~5–10 mWb in standard operation (up to ~16 mWb in records), and external axial magnetic field ~1 kG [tae-c2w-machine-details.md §Key Features and Plasma Parameters]. More recent C-2W campaigns have pushed electron temperature to ~1 keV peak (>0.75 keV averaged inside separatrix) — the first time the 1 keV threshold was reached — and total plasma energy to ~13 kJ [osti-pages-servlets-purl-2441289.md §Abstract; §3.1 Enhanced performance]. The 2025 NBI-only formation paper (Nature Communications, s41467-025-58849-5) is the highest-profile peer-reviewed disclosure in several years, demonstrating plasma formation without traditional plasma guns or formation sections [tae-nbi-breakthrough-2025.md §The 'Norm' Breakthrough]. TAE demonstrated first p-B11 fusion in a magnetically confined plasma in 2023 (with NIFS Japan) — a milestone confirmed in the dossier but the primary paper is not in the current source set [dossier.md §Fuel].

**Company communications:**  
TAE's FAQ and press materials explain the concept physics and strategic positioning clearly, including the thermal/steam conversion approach for Da Vinci, the long-term ICC vision, and the p-B11 fuel rationale [tae-energy-conversion-clarification.md §How do you produce electricity from fusion?]. The December 2025 Trump Media/DJT merger announcement provides the only published commercial spec (50 MWe, construction start 2026, first plasma 2029) [tae-djt-merger-davinci-specs.md §Deal details]. TAE holds 2,500+ patents globally including the foundational Inverse Cyclotron Converter patents (US7459654, US6628740, US6888907); the original ICC patent provides detailed operational parameters for the direct conversion system that TAE envisions as the long-term energy capture technology [tae-energy-conversion-notes.md §Description].

**Independent analyses:**  
No independent techno-economic analysis of the TAE p-B11 FRC concept is in the current source set. The Grokipedia entry provides a comprehensive third-party narrative synthesis of TAE's published milestones and claimed advantages, but it is not peer-reviewed and draws on TAE's own press materials [grokipedia-tae-technologies.md]. The Helion FRC handwritten exemplar [08-frc-w-direct-conversion.md] provides the closest independent LCOE modeling precedent in this analysis pipeline, though for a different fuel cycle (D-He3) and different confinement approach (pulsed compression).

**Phase 1a dossier completeness:**  
The dossier achieved high confidence on all primary taxonomy columns: confinement family, fuel, heating method, energy capture (thermal/steam for Da Vinci baseline confirmed), plasma state, tritium breeding (N/A), neutron management (minimal/aneutronic), and operation mode. One medium-confidence item remains: Da Vinci's magnet type (resistive copper inferred from low beta requirements and TAE's "simple geometry magnets" positioning, but not explicitly disclosed for the commercial plant) [dossier.md §Magnet Type].

**Key data gaps limiting this analysis:**

1. No published plasma parameters for the Norm machine or Copernicus design targets (temperature, density, confinement time needed for net gain with p-B11)
2. Da Vinci fusion power, Q value, and recirculating power fraction entirely unpublished
3. NBI system specifications for Da Vinci (beam energy, total power, wall-plug efficiency) not disclosed
4. No cost estimates or capital cost decomposition for any TAE commercial design
5. ICC technology is patent-stage only — no experimental demonstration of conversion efficiency at reactor-relevant parameters

---

## Section 2: Challenges in Capturing System Function

TAE's p-B11 FRC concept poses the most severe LCOE modeling challenges of any concept in this pipeline. The challenges are not primarily engineering unknowns (as with many D-T concepts where the physics is validated) but *physics unknowns* that fundamentally determine whether the concept can reach any positive energy balance at all. The following are ranked by LCOE impact.

**1. Bremsstrahlung power balance for p-B11 — the binding physics constraint (Impact: Critical)**

The p-B11 reaction requires plasma ion temperatures in the range of 150–300 keV [grokipedia-tae-technologies.md §Aneutronic Fusion via p-B11 Reaction; dossier.md §Fuel]. At these temperatures, bremsstrahlung X-ray radiation from electron-ion interactions scales approximately as P_brem ∝ n² T_e^0.5 Z_eff², and can rival or exceed the fusion alpha power output. For a fully thermalized Maxwellian p-B11 plasma, achieving net energy gain (Q_plasma > 1) requires satisfying a Lawson-type criterion that is estimated to be roughly 100× more demanding than D-T at its optimal temperature [inferred from physics literature; no source in available materials provides this exact factor for TAE's specific plasma regime]. TAE's approach to this problem is to maintain a non-equilibrium, beam-driven plasma where ion temperature substantially exceeds electron temperature (T_i >> T_e), with the high-energy neutral beams continuously replenishing the non-Maxwellian ion energy distribution before it thermalizes. This strategy is physically motivated but unvalidated at the temperatures required:

> "The reaction faces significant technical hurdles: its cross-section peaks at higher energies (around 600 keV) compared to D-T (100 keV), necessitating plasma temperatures of 100-200 keV for meaningful reactivity. Bremsstrahlung radiation losses dominate at these conditions, complicating ignition and confinement."  
> — grokipedia-tae-technologies.md, §Aneutronic Fusion via p-B11 Reaction

Partial experimental validation of the non-equilibrium strategy has emerged: equilibrium reconstruction from recent C-2W high-performance shots via the SEQUOIIA code shows fast-ion pressure exceeding bulk thermal plasma pressure by ~1.5× in the core region [osti-pages-servlets-purl-2441289.md §3.1 Enhanced performance in advanced beam-driven FRCs]. This confirms that NBI does produce a meaningfully fast-ion-dominated plasma distinct from a Maxwellian at current operating conditions (~1 keV total temperature). However, the critical qualification is that this validation holds at ~1 keV — electron-ion equilibration timescales and bremsstrahlung loss rates are categorically different at the 150+ keV ion temperatures required for Da Vinci. Whether the T_i >> T_e regime persists at commercial conditions remains the open and defining gap.

The fundamental LCOE uncertainty created by this challenge is unbounded: if the power balance cannot close at any achievable plasma parameter, there is no LCOE — the concept does not produce net energy. This is qualitatively different from engineering uncertainties in D-T concepts where the physics is validated. There is no equivalent challenge in any D-T concept in this pipeline.

**2. Temperature extrapolation from current experiments to commercial conditions (Impact: Critical)**

The C-2W/Norman device achieved ion temperatures up to ~3 keV total (T_tot = T_e + T_i) [tae-c2w-machine-details.md §Plasma Performance Records]. Da Vinci targets ~250 keV ion temperatures [dossier.md §Fuel]. This represents roughly an 80–100× extrapolation in ion temperature from the most advanced TAE experimental machine to the commercial design point. No plasma physics confinement scaling law has been validated over this range for any confinement concept, let alone for beam-driven FRCs. TAE has described Copernicus as the machine intended to "demonstrate the viability of net energy generation" before the end of the decade [tae-nbi-breakthrough-2025.md §Norm breakthrough context], but Copernicus parameters have not been published and the machine had not yet been built as of the December 2025 merger announcement. This extrapolation is the single largest unresolvable uncertainty in the LCOE model:

> "Achieving net energy gain (Q > 1) remains undemonstrated for p-B11, with current experiments yielding fusion products but far below breakeven."  
> — grokipedia-tae-technologies.md, §Aneutronic Fusion via p-B11 Reaction

**3. NBI recirculating power fraction at commercial scale (Impact: High)**

NBI serves four functions in TAE's system: plasma formation, heating, current drive, and MHD stabilization [dossier.md §Primary Heating]. At reactor scale, the NBI system must maintain ion temperatures of ~250 keV against bremsstrahlung, charge-exchange, and transport losses. The recirculating power fraction is:

> Q_eng = P_net / (P_gross – P_NBI,wall-plug)

C-2W measurements from the 2024 *Nuclear Fusion* paper provide the most direct available efficiency data. The attenuated NBI power reaching the plasma is less than 50% of the electrical input — the losses encompass neutralization efficiency, duct geometry, impact ionization, and charge-exchange effects:

> "Generally, attenuated power is estimated to be less than half of the electrical power due to a menagerie of neutralization efficiency, duct geometry, impact ionization and charge-exchange effects."  
> — osti-pages-servlets-purl-2441289.md, §2 C-2W experimental apparatus

Additionally, beam shine-through (beam ions exiting the far side of the plasma unabsorbed) is measured at 15 ± 5% independent of injected beam current [osti-pages-servlets-purl-2441289.md §3.3 Optimizations of neutral beam systems]. The combined wall-plug-to-absorbed-heating efficiency is therefore:

η_NBI ≈ (wall-plug → beam: ~0.55–0.65) × (beam → plasma, accounting for duct+neutralization+ionization: <0.50) × (1 – 0.15 shine-through) ≈ **0.20–0.35**

This is substantially more pessimistic than the 50–60% assumption used in early analysis. At η_NBI = 0.26 (central estimate) and η_th = 0.30, the Q_eng breakeven condition:

> Q_plasma_breakeven = 1 / (η_th × η_NBI) = 1 / (0.30 × 0.26) ≈ **12.8**

Commercial operation requires comfortable margin, so the practical requirement is Q_plasma ≥ 25–35. At the optimistic bound (η_NBI = 0.35), breakeven is ~9.5 and the commercial target is Q_plasma ≥ 20. At the pessimistic bound (η_NBI = 0.20), breakeven is ~16.7 and the commercial target is Q_plasma ≥ 35. The sensitivity model should sweep: Q_plasma from 5 to 50, η_NBI_total from 0.20 to 0.45, decomposed into source efficiency (η_NBI_source ≈ 0.55–0.65) and plasma coupling efficiency (η_NBI_couple ≈ 0.35–0.50).

[inferred: NBI efficiency chain from C-2W attenuation data; wall-plug-to-absorbed estimate from three-stage decomposition; breakeven condition from Q_eng = 0 at rated power]

Furthermore, the Q_plasma floor derived above assumes rated-power operation — it is a best-case figure. Fusion plant economics research identifies a compounding effect: recirculating power in a fusion reactor (here, NBI) does not scale down proportionally when the plant operates below rated output, because the NBI must remain active at near-full power to maintain plasma stability [arxiv-2103-12451.md §Abstract: "the recirculated power remains high if it runs at reduced output power"]. For a first-generation Da Vinci plant with undemonstrated CW FRC operation (current pulse record ~40 ms), early capacity factors well below 90% are plausible. At, say, 60% capacity factor, the effective recirculating power fraction relative to average output rises substantially above the rated-power calculation, tightening the Q_plasma requirement further. The two gaps — Q_plasma floor and capacity factor — interact multiplicatively, not independently.

**4. FRC stability at reactor scale (Impact: High)**

FRC confinement relies on anomalous suppression of the tilt and rotational instability modes by the tangential NBI [grokipedia-tae-technologies.md §Inherent Limitations of FRC Approach]. In C-2W/Norman, this stabilization was demonstrated at separatrix radii of ~0.4 m and plasma currents of 300–350 kA [dossier.md §Confinement Concept]. Da Vinci requires "major radii of approximately 1–2 meters" [grokipedia-tae-technologies.md §FRC Stability at Scale], a factor of 2.5–5× scale-up:

> "Reactor-relevant FRCs, necessitating major radii of approximately 1–2 meters and total plasma currents of several megaamperes, face amplified risks of [tilt and kink] modes, demanding active control measures like beam injection or magnetic shaping that are not intrinsic to the configuration itself."  
> — grokipedia-tae-technologies.md, §Inherent Limitations of FRC Approach

Stability scaling at reactor size is a physics unknown that directly determines whether the FRC can operate at all at commercial conditions. From an LCOE perspective, the required NBI power for stability (as distinct from heating) introduces an additional recirculating power floor that cannot be estimated without reactor-scale experiments.

**5. Energy conversion: thermal baseline vs. ICC potential (Impact: High)**

Da Vinci's baseline energy conversion is thermal/steam at approximately 30–35% efficiency [tae-energy-conversion-clarification.md §How do you produce electricity from fusion?]. Yet p-B11's aneutronic fusion products (three alpha particles, essentially all in charged particles) were specifically chosen to enable direct energy conversion at >90% efficiency via the ICC [tae-energy-conversion-notes.md §Direct Energy Conversion]. Using thermal conversion on a fuel chosen for direct conversion represents a structural LCOE penalty: the 60-percentage-point efficiency gap between the ICC vision and the Da Vinci baseline means the near-term plant cannot realize the key economic benefit of the aneutronic fuel choice. This is not a temporary limitation — until ICC is commercially demonstrated, the LCOE for Da Vinci will be substantially worse than TAE's long-term vision implies.

**6. O&M cost structure — placeholder (Impact: Moderate)**

No O&M cost breakdown is available in the source materials. The aneutronic nature of the concept provides structural advantages: no tritium handling, minimal neutron activation, and hands-on maintenance capability [dossier.md §Neutron Management]. These eliminate several major O&M cost categories present in D-T concepts. The dominant O&M driver for p-B11 FRC will likely be NBI system maintenance (beam sources, gas cells, neutralizers, power supplies), which are analogous to large NBI systems in tokamak facilities (JET, JT-60U, ITER). No published data on Da Vinci NBI O&M costs exists.

### Modeling Approach

Given six blocking data gaps — including the foundational question of whether p-B11 can achieve Q_plasma > 1 in any confinement device — the standard 1costingfe cost template (which presupposes validated fusion physics and fills parameter tables from experimental data) is inappropriate here. The correct approach is free-form scenario modeling with three explicit branches:

**Branch A — Physics fails (no viable LCOE):** Q_plasma cannot be sustained above the bremsstrahlung breakeven threshold at any achievable beam-driven FRC plasma condition. This branch has no LCOE output and must be flagged explicitly as a non-viable outcome. The model should report the Q_plasma threshold below which this branch is selected.

**Branch B — Physics succeeds, Da Vinci baseline (thermal steam conversion):** Q_plasma meets or exceeds the viability threshold derived in Challenge 3 (≥10–15 with η_NBI ≥ 0.55), and Da Vinci operates on its confirmed steam Rankine cycle at ~30–35% thermal efficiency. This is the near-term commercial case. LCOE is dominated by NBI capital cost, recirculating power fraction, and capacity factor. The Q_plasma × η_NBI parameter space around the viability boundary is the primary sensitivity axis.

**Branch C — Physics succeeds, ICC upgrade:** As Branch B, but the Inverse Cyclotron Converter (patent-stage >90% efficiency) is demonstrated and deployed. The ~60-point efficiency gain over steam conversion is the central value proposition of the aneutronic fuel choice. This branch represents the LCOE floor that the concept is ultimately targeting; it shows the economic case for p-B11 *if* both the physics and the ICC technology succeed.

The model's primary analytical function is to map the Q_plasma × η_NBI parameter space and identify the viability boundary — not to estimate a single central-case LCOE. This positions the analysis as a physics-viability and scenario tool rather than a cost-estimation exercise.

A critical missing dimension in early model iterations was the bremsstrahlung radiation loss fraction (f_rad). Because bremsstrahlung suppression via the T_i >> T_e non-equilibrium regime is TAE's central physical bet, f_rad is not a fixed engineering parameter — it is the primary unknown the concept is trying to solve. At fully thermalized Maxwellian p-B11 conditions, f_rad could exceed 0.80–1.0, forcing Branch A regardless of Q_plasma. The model should sweep f_rad from 0.05 (optimistic non-Maxwellian suppression) to 0.90 (near-Maxwellian), identifying the f_rad threshold at the baseline Q_plasma below which P_net ≤ 0. A Q_plasma × f_rad viability grid should be generated alongside the Q_plasma × η_NBI grid, converting the qualitative bremsstrahlung discussion in Challenge 1 into a quantitative viability boundary.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least to most mature.

---

**p-B11 High-Q Plasma Operation — TRL 1–2**

- **Demonstrated**: First p-B11 fusion in a magnetically confined plasma (TAE + NIFS Japan, 2023) — fusion products observed but at conditions far below breakeven [dossier.md §Fuel]. C-2W/Norman demonstrates beam-driven FRC operation at 3 keV total temperature [tae-c2w-machine-details.md §Plasma Performance Records]. p-B11 fusion physics well-characterized in accelerator experiments at the required cross-section peak energies.
- **Demonstrated at low temperature**: Non-Maxwellian fast-ion-dominated plasma at C-2W conditions. Equilibrium reconstruction (SEQUOIIA code) confirms fast-ion pressure exceeds bulk thermal plasma pressure by ~1.5× in the core of recent high-performing C-2W shots [osti-pages-servlets-purl-2441289.md §3.1 Enhanced performance in advanced beam-driven FRCs]. This validates the beam-driven non-equilibrium strategy at ~1 keV total temperature but does not extrapolate to commercial conditions.
- **On paper only**: Net energy gain (Q_plasma > 1) for p-B11 in any confinement device. Non-Maxwellian beam-driven plasma at T_i ~150 keV with sustained T_i >> T_e at reactor-relevant temperatures (required for bremsstrahlung suppression at commercial conditions). Confinement scaling from ~1–3 keV to 250 keV in beam-driven FRC. Fusion power levels above milliwatts in magnetically confined p-B11 plasma.
- **Missing at scale**: Demonstration that beam-driven FRC can sustain T_i >> T_e at reactor-relevant densities and temperatures without equilibration erasing the temperature advantage. At 150+ keV, electron-ion equilibration timescales and bremsstrahlung loss rates are categorically different from the 1 keV regime where fast-ion dominance is now validated. Measurement of energy confinement time τ_E at 150+ keV conditions. Copernicus intermediate-step validation data (not yet available as of 2026). Any published Lawson parameter (nτT) for a p-B11 FRC plasma approaching reactor relevance.

---

**Inverse Cyclotron Converter (ICC) Direct Energy Conversion — TRL 2–3**

- **Demonstrated**: The ICC concept is described at length in foundational patents (US7459654, US6628740, US6888907), with a detailed physical design for decelerating annular beams of fusion products in a tapered magnetic field [tae-energy-conversion-notes.md §Description]. Ion rotation frequencies of 1–10 MHz (preferably 5–10 MHz) and coherent beam energies of 100 keV to 3.3 MeV are specified in the patent. TAE claims the ICC is under active development, consistent with the 2,500+ patent portfolio.
- **On paper only**: Demonstrated ICC conversion of MeV-range alpha particles from actual fusion reactions. System-level demonstration of ICC connected to a fusion plasma source. Grid-compatible power conditioning for the ~5 MHz ICC output [tae-energy-conversion-notes.md §Direct Energy Conversion System]. Integration of ICC with FRC geometry.
- **Missing at scale**: Any published experimental result demonstrating ICC conversion efficiency above laboratory proof-of-concept scales. The patent notes that "various factors, such as perpendicular rotational energy of the annular beam before it enters the converter, may reduce this efficiency by about 5%" — practical efficiency at reactor scale is entirely undemonstrated [tae-energy-conversion-notes.md §ICC Efficiency]. Da Vinci baseline bypasses ICC entirely, confirming the technology is not ready for near-term commercial deployment.

---

**NBI System at 250+ keV Beam Energy — TRL 4–5**

- **Demonstrated**: C-2W operates eight injectors (four fixed 15 keV, four tunable 15–40 keV) at up to 21 MW total injected power [tae-c2w-machine-details.md §NBI System]. The 2025 NBI-only formation breakthrough demonstrates formation, heating, and stabilization by NBI alone [tae-nbi-breakthrough-2025.md §The 'Norm' Breakthrough]. High-energy NBI systems at up to ~120 keV exist in fusion research (JT-60U, ITER NNBI at 1 MeV range, but for D beams).

> "TAE's new machine uses only neutral beam injection (NBI) to produce a hot, stable FRC plasma — reducing the machine's size, complexity and cost by up to 50% and optimizing for economic competitiveness and commercial viability."  
> — tae-nbi-breakthrough-2025.md, §The 'Norm' Breakthrough

- **On paper only**: NBI systems delivering sufficient power density to heat and sustain a Da Vinci-scale FRC at ~250 keV. Proton beam neutralization at the required energies (high-energy proton NBI is less mature than deuterium NBI). Power supply systems for multi-tens-of-MW NBI at reactor scale. NBI beam geometry optimized for both 250 keV FRC heating and MHD stabilization simultaneously.
- **Missing at scale**: Wall-plug efficiency characterization for high-energy NBI systems at Da Vinci parameters. NBI system lifetime and replacement schedule in a radiation environment. Recirculating power budget for NBI at commercial fusion conditions. Demonstrated beam coupling efficiency to FRC plasma at >10 keV ion temperatures.

---

**FRC Plasma Formation and Sustainment — TRL 5–6**

- **Demonstrated**: C-2W/Norman routinely operates beam-driven FRCs for up to ~30–40 ms (NBI pulse duration limited), with plasma current 300–350 kA, separatrix radius 0.4 m [dossier.md §Confinement Concept]. NBI-only formation breakthrough eliminates auxiliary plasma gun hardware [tae-nbi-breakthrough-2025.md]. Machine learning optimization (Google collaboration) has identified new high-performance operational regimes [tae-c2w-machine-details.md §ML-Driven Optimization]. First p-B11 fusion products observed in FRC confinement in 2023. Recent C-2W campaigns have achieved electron temperature of ~1 keV peak (>0.75 keV averaged inside separatrix) for the first time, and total plasma energy of ~13 kJ [osti-pages-servlets-purl-2441289.md §Abstract; §3.1]. These represent the current experimental high-water marks; the extrapolation gap from 1 keV (Te) to the ~150 keV (Ti) Da Vinci requirement is approximately **150×** in ion temperature.

> "Norm, routinely achieves TAE's highest steady-state plasma performance"  
> — tae-nbi-breakthrough-2025.md, §The 'Norm' Breakthrough

- **On paper only**: FRC sustainment for seconds-to-continuous timescales (current record ~40 ms). Steady-state FRC operation with continuous NBI fueling and exhaust. Validated confinement scaling from C-2W to Da Vinci scale (factor of 2.5–5× in major radius).
- **Missing at scale**: Seconds-scale or CW FRC operation at reactor-relevant temperatures. Particle exhaust and density control in a sustained FRC. Demonstrated plasma current stability at multi-megaampere levels. Confinement scaling validation across the density and temperature range required for Da Vinci.

---

**Copper Resistive Magnets (Equilibrium + Mirror Fields) — TRL 7–8**

- **Demonstrated**: C-2W/Norman uses copper coils for equilibrium, mirror, saddle/trim, and previously formation functions [grokipedia-tae-technologies.md §Machine Design; dossier.md §Magnet Type]. Copper resistive magnet technology is fully mature for the ~1 kG external axial field levels used in FRC operation [tae-c2w-machine-details.md §Magnet System]. Near-unity FRC beta (~90–100%) means external magnetic field requirements are minimal — the plasma's own poloidal currents provide most of the confinement.
- **On paper only**: Da Vinci magnet geometry and coil design (not publicly disclosed). Power consumption of resistive coils at commercial plasma scale. Cooling system design for continuous high-current operation.
- **Missing at scale**: Da Vinci-specific coil set confirmation (HTS vs. copper for the commercial plant has not been officially stated; resistive is inferred from TAE's "simple geometry magnets" positioning). Long-term coil lifetime in modest radiation environment from secondary neutrons.

---

**Balance of Plant (Thermal Steam Conversion) — TRL 7–9**

- **Demonstrated**: Conventional steam Rankine cycles are commercially mature at GW scale. The Da Vinci FAQ explicitly confirms thermal/steam conversion: "a network of pipes will transport that heat via working fluid to a steam generator. The steam spins a turbine which drives an electric generator, similar to what happens in operating power plants today" [tae-energy-conversion-clarification.md §How do you produce electricity from fusion?].
- **On paper only**: Integration of thermal steam cycle with a p-B11 FRC heat source. Heat exchanger design for alpha particle energy deposition in the plasma-facing components of an FRC (geometry differs substantially from tokamak with blanket). Sizing of thermal balance of plant for Da Vinci 50 MWe scale.
- **Missing at scale**: Confirmation of the thermodynamic cycle operating temperature range (sets achievable efficiency). Heat exchanger materials compatibility with FRC plasma-facing components. First wall heat flux management (alpha particle energy deposition geometry in a linear FRC differs from a toroidal blanket).

---

## Section 4: Key Materials and Supply Chain Considerations

TAE's p-B11 FRC concept has a radically simpler materials and supply chain footprint than any D-T tokamak or stellarator in this pipeline. The elimination of tritium breeding and heavy neutron shielding removes several of the most constrained supply chain elements. The dominant supply chain risks are instead associated with the NBI system and, to a lesser extent, the p-B11 fuel itself.

**Boron-11 Fuel — Abundant, Minimal Processing Required**

The p-B11 reaction consumes protons (hydrogen) and boron-11. Boron-11 constitutes approximately 80% of natural boron [grokipedia-tae-technologies.md §Aneutronic Fusion via p-B11 Reaction], and boron is extracted from borax minerals (primarily from Turkey and the United States) with global production of approximately 6–8 million tonnes per year. Unlike tritium (requiring active breeding) or He-3 (vanishingly rare on Earth), B-11 fuel supply is not a bottleneck. For a 50 MWe plant consuming ~1 gram of p-B11 per day [estimated — based on 8.7 MeV per reaction, ~10²⁴ reactions/day at 50 MWe with 90% ICC efficiency, or ~1–2 kg/day at 30% thermal efficiency; [inferred: fuel consumption rate from reaction energy × plant output × efficiency; no source states this directly]], the annual demand is on the order of kilograms to tonnes of isotopically standard boron. Some isotopic enrichment to increase B-11 fraction from 80% to higher purity may be desirable for reaction rate optimization, but this is not a critical constraint given the natural abundance. Boron-11 enrichment is not a specialized nuclear supply chain item — it does not require the security-sensitive infrastructure of Li-6 enrichment or the declining availability of tritium.

**No REBCO Tape, No FLiBe, No Li-6 Enrichment Required**

Unlike every HTS tokamak, stellarator, and mirror concept in this pipeline, TAE's FRC does not require superconducting tape at commercial scale (near-unity FRC beta means resistive copper magnets suffice at very low external field). This removes the global REBCO production bottleneck (currently a few thousand km/year capacity for a fleet requirement of tens of thousands of km per plant). No FLiBe breeding blanket means no beryllium supply constraint (global production ~300 tonnes/year, Materion-dominated [referenced in 01-hts-compact-tokamak.md analysis]). No tritium breeding means no Li-6 enrichment supply chain. These are genuine structural advantages over the D-T MFE field.

**NBI System Components — Specialized, Scale-Up Uncharacterized**

The NBI system is the dominant engineered subsystem. C-2W uses eight injectors at up to 21 MW total; Da Vinci will require a larger NBI system (exact specs not disclosed). Key supply chain elements:
- **Ion sources**: High-current positive-ion or negative-ion sources for proton or deuterium beams at 40–250+ keV. Negative-ion sources at high energy are more complex (ITER NBI uses 1 MeV negative D beams). No commercial supply chain exists for reactor-scale high-energy NBI systems.
- **Neutralization cells**: Gas or photodetachment neutralizers for beam formation. Gas cell efficiency at high beam energies falls for positive ions (limiting H+ NBI to <~120 keV for efficient neutralization); negative-ion approaches are more efficient at higher energies but more complex.
- **Power supplies**: Large pulsed or DC power supplies for multi-MW NBI. These exist in the fusion research community but at commercial quantities would require industrial-scale manufacturing scale-up.
- **Beam dump components**: Unreacted beam fractions must be absorbed; at reactor scale, beam dump thermal loading is a significant engineering item.

No published supply chain analysis exists for TAE Da Vinci NBI system components. The NBI technology at C-2W scale is not commercially unusual, but the scale-up to commercial fusion conditions is entirely uncharacterized.

**Copper Magnets — No Supply Chain Risk**

Commercial-grade copper is globally abundant. Resistive coils for the FRC equilibrium and mirror fields (at ~1 kG levels) present no supply chain constraint. Electrical power for resistive coil operation is a continuous operating cost, unlike superconducting magnets (which have cryogenic operating costs instead). The power consumption of the copper coil system at Da Vinci scale is not published.

**No Tritium Infrastructure — Major Structural Simplification**

The absence of tritium breeding, handling, and accounting systems eliminates a specialized industrial requirement present in all D-T concepts. No remote handling robots, no tritium-compatible valves and pipes, no radiological containment for the primary circuit. This simplifies plant licensing, reduces O&M complexity, and enables hands-on maintenance. The economic value of this simplification is substantial but unquantified in the available sources.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output (Da Vinci initial) | 50 MWe | tae-djt-merger-davinci-specs.md §Deal details | high | Published in merger announcement; 350–500 MWe stated as scale target |
| Net electrical output (Da Vinci scaled) | 350–500 MWe | dossier.md §Driver Technology | high | Per DJT merger announcement |
| Fuel cycle | p + ¹¹B → 3α + 8.7 MeV | dossier.md §Fuel | high | All energy in charged alpha particles; <1% neutron fraction |
| p-B11 cross-section peak energy | ~600 keV (c.m.) | grokipedia-tae-technologies.md §Aneutronic Fusion | high | Sets minimum required ion temperature |
| Required ion temperature for Da Vinci | ~150–300 keV | dossier.md §Fuel; grokipedia-tae-technologies.md §Aneutronic Fusion | high | TAE targets ~250 keV; cross-section peak requires >100 keV |
| C-2W total plasma temperature (record) | ~3 keV (Ttot) | tae-c2w-machine-details.md §Plasma Parameters | high | Ti substantially higher than Te; experimental record |
| C-2W electron temperature (recent campaigns) | ~1 keV peak; >0.75 keV averaged inside separatrix | osti-pages-servlets-purl-2441289.md §Abstract; §3.1 | high | "First time achieving 1 keV in C-2W"; 3× improvement over prior ~300 eV baseline |
| C-2W total plasma energy (recent record) | ~13 kJ | osti-pages-servlets-purl-2441289.md §Abstract; §3.1 | high | Achieved with optimized NBI, magnetic field, and edge-biasing |
| C-2W fast-ion / thermal pressure ratio | ~1.5× (fast-ion exceeds thermal) | osti-pages-servlets-purl-2441289.md §3.1 | high | SEQUOIIA equilibrium reconstruction; validates fast-ion dominated regime at 1 keV |
| C-2W electron density | 1–3 × 10¹⁹ m⁻³ (average) | tae-c2w-machine-details.md §Plasma Parameters | high | Fusion-relevant scale requires higher density × confinement time |
| C-2W trapped flux (typical) | 5–10 mWb | tae-c2w-machine-details.md §Plasma Parameters | high | Record 16 mWb |
| C-2W external axial field | ~1 kG (0.1 T) | tae-c2w-machine-details.md §Plasma Parameters | high | Very low field; FRC near-unity beta provides self-confinement |
| C-2W separatrix radius / axial length | 0.4 m / 2 m | dossier.md §Confinement Concept | high | C-2W/Norman geometry; Da Vinci will be larger (1–2 m major radius) |
| C-2W plasma current | 300–350 kA | dossier.md §Confinement Concept | high | Da Vinci will require multi-megaampere plasma currents |
| C-2W NBI total power | up to 21 MW | tae-c2w-machine-details.md §NBI System | high | 4 fixed 15 keV + 4 tunable 15–40 keV injectors |
| C-2W plasma lifetime | ~30–40 ms | dossier.md §Plasma State | high | NBI pulse-duration limited; CW operation not yet demonstrated |
| FRC plasma beta | ~90–100% | grokipedia-tae-technologies.md §FRC Fundamentals | high | Near-unity beta; self-confinement by plasma currents |
| Da Vinci energy conversion | Thermal (steam) | tae-energy-conversion-clarification.md §How do you produce electricity | high | Official FAQ confirms steam turbine; ICC is future upgrade only |
| Long-term ICC target efficiency | >90% | tae-energy-conversion-notes.md §ICC Description | medium | Patent-stage claim; not demonstrated; not Da Vinci baseline |
| ICC patent ion rotation frequency | 1–10 MHz (5–10 MHz preferred) | tae-energy-conversion-notes.md §Fusion Parameters | medium | Patent specification; experimental validation not published |
| Plasma-electric power generation scale (patent) | 50–450 kW/cm (length) | tae-energy-conversion-notes.md §Fusion Parameters | low | Original 2001-era patent spec; may not reflect current Da Vinci design |
| Ion temperature in patent spec | 30–230 keV (80–230 keV preferred) | tae-energy-conversion-notes.md §Fusion Parameters | low | Patent design point; consistent with p-B11 requirements |
| External applied field in patent spec | 2.5–15 kG (5–15 kG preferred) | tae-energy-conversion-notes.md §Fusion Parameters | low | Somewhat higher than C-2W; more detailed reactor design assumption |
| NBI complexity reduction from Norm breakthrough | ~50% cost reduction vs. prior design | tae-nbi-breakthrough-2025.md §The 'Norm' Breakthrough | medium | TAE's stated figure; basis not independently verified |
| Total private funding raised | >$1.2–1.3B | dossier.md §Driver Technology; tae-djt-merger-davinci-specs.md | high | Per merger documents |
| Da Vinci construction start target | 2026 | tae-djt-merger-davinci-specs.md | high | Subject to regulatory approval; per DJT merger announcement |
| Da Vinci first plasma target | 2029 | dossier.md §Driver Technology | high | Per DJT merger announcement |
| Thermal efficiency (Da Vinci baseline) | [inferred] ~30–35% | [inferred: steam Rankine cycle is baseline per FAQ; standard steam Rankine efficiency range; no Da Vinci-specific thermal efficiency published] | low | Same efficiency as D-T concepts using steam cycle |
| Fusion power required for 50 MWe (steam) | [estimated] ~170–200 MWth | [estimated: P_net = 50 MWe; η_th = 0.30; P_gross ≈ P_net / (η_th × (1 – f_recirc)); f_recirc unknown; lower bound assumes f_recirc → 0] | low | Must close Q_plasma >> 1 AND cover NBI recirculating power |
| C-2W NBI wall-plug-to-plasma absorbed efficiency | <50% (wall-plug→plasma, excl. shine-through) × (1 – 0.15 shine-through) ≈ 0.20–0.35 total | osti-pages-servlets-purl-2441289.md §2 C-2W apparatus; §3.3 NBI optimizations | high | Source: "attenuated power estimated to be less than half of the electrical power"; shine-through 15±5%; combined η_NBI ≈ 0.20–0.35 |
| Q_plasma required for net electricity (NBI+steam) | [estimated] ≥ 25–35 (central); ≥ 20 (optimistic) | [estimated: derivation in Section 2; η_NBI ≈ 0.20–0.35 from C-2W attenuation data; η_th = 0.30; breakeven Q = 1/(η_th × η_NBI) ≈ 10–17; commercial margin requires 2× breakeven] | low | Revised upward from earlier ~10–15 estimate; see Section 2 Challenge 3 for full derivation |
| Boron-11 fuel cost | [estimated] negligible (<$1/MWh) | [estimated: natural boron ~$2–5/kg; B-11 is 80% of natural; 1 kg/day fuel for GW-scale plant is ~$2000/year fuel cost; negligible vs. capital-dominated LCOE] | low | B-11 fuel cost is not a meaningful LCOE driver |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q_plasma for p-B11 in any confinement device | truly-unknown | blocking | Never demonstrated at Q > 1; Copernicus (unpublished) is intended to address this; LCOE model is physically undefined without this |
| Da Vinci fusion power and Q value | proprietary / truly-unknown | blocking | No published plant physics design; not derivable without knowing confinement quality at reactor conditions |
| NBI system specs for Da Vinci (beam energy, total power) | proprietary | blocking | Required to calculate NBI recirculating power fraction; missing from all public sources |
| NBI wall-plug-to-plasma efficiency at Da Vinci beam energies | not-yet-sourced | blocking | C-2W data shows total η_NBI ≈ 0.20–0.35 (see Section 5 and Section 2 Challenge 3); Da Vinci beam energy may differ; negative-ion NBI at >120 keV is uncertain; coupling efficiency vs. C-2W may change |
| Da Vinci overnight capital cost | proprietary | blocking | No published estimate; no analogous plant study |
| FRC confinement scaling to reactor conditions | truly-unknown | blocking | 80× temperature extrapolation from C-2W to Da Vinci; no validated scaling law |
| Bremsstrahlung loss fraction at Da Vinci conditions | truly-unknown | blocking | Depends on T_e/T_i ratio and confinement at 150–250 keV; experimentally unvalidated |
| Da Vinci plasma geometry (major radius, length) | proprietary | important | Required for confinement volume, NBI geometry, and heat flux calculations |
| Plant capacity factor | proprietary / not-yet-sourced | important | Steady-state concept; no disruptions or CS re-magnetization penalties, but FRC CW operation undemonstrated. Interacts multiplicatively with NBI recirculating power fraction (see Section 2, Challenge 3): sub-unity capacity factor raises the effective recirculating power fraction because NBI power remains near-constant at reduced output [arxiv-2103-12451.md §Abstract], tightening the Q_plasma floor beyond the rated-power estimate |
| O&M cost breakdown | truly-unknown | important | NBI maintenance is expected dominant driver; no published data for fusion-scale NBI O&M |
| First wall heat flux and material | proprietary | important | Alpha particle energy deposition in FRC linear geometry; material not disclosed |
| ICC experimental validation data | truly-unknown | important | Patent claims >90% efficiency; no experimental paper exists in public domain |
| Cost of NBI system components at Da Vinci scale | truly-unknown | important | No analogous commercial NBI system exists at this scale |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Q_plasma > 1 never demonstrated for p-B11 in any confinement device — the concept has no validated physics basis for net energy gain | S1, S2, S3 | truly-unknown | blocking | Watch for Copernicus experimental results; review theoretical Lawson analysis for non-Maxwellian p-B11 FRC (Nevins & Swain 2000 or equivalent — not in source set) |
| 2 | Bremsstrahlung power balance at Da Vinci conditions unknown — the T_i >> T_e non-equilibrium regime has not been sustained at >10 keV ion temperatures | S2, S3, S5 | truly-unknown | blocking | Requires Copernicus or equivalent experiment; no shortcut from current sources |
| 3 | Temperature extrapolation from 3 keV (C-2W) to 250 keV (Da Vinci) — ~80× gap with no validated confinement scaling | S2, S3, S5 | truly-unknown | blocking | Copernicus experimental results; FRC transport scaling literature |
| 4 | NBI system specs for Da Vinci (beam energy, total power, wall-plug efficiency) — recirculating power fraction incalculable | S2, S3, S5 | proprietary | blocking | TAE investor disclosures; Da Vinci engineering announcement |
| 5 | Da Vinci fusion power and Q value entirely unpublished | S1, S5 | proprietary | blocking | Watch for ARPA-E or DOE Milestone progress reports |
| 6 | Da Vinci capital cost and LCOE estimate absent — no plant study or independent TEA | S1, S5 | proprietary | blocking | Post-merger engineering announcements; ARPA-E program disclosures |
| 7 | FRC stability at reactor scale (1–2 m major radius, multi-MA plasma current) unvalidated | S2, S3, S5 | truly-unknown | blocking | Copernicus / Da Vinci experimental results only |
| 8 | ICC direct conversion: zero experimental demonstration at MeV-range fusion product energies | S2, S3, S5 | truly-unknown | important | TAE internal R&D; watch for research publications on ICC prototyping |
| 9 | Plasma-facing component design and first wall heat flux management for FRC linear geometry | S3, S5 | proprietary | important | TAE technical publications or Da Vinci design announcements |
| 10 | Da Vinci plasma geometry (major radius, length) — required for confinement volume and NBI geometry estimation | S5 | proprietary | important | DJT merger follow-on technical disclosures |
| 11 | O&M cost structure — NBI maintenance, component replacement schedule, availability estimate | S2, S5 | truly-unknown | important | NBI maintenance analogy from tokamak research facilities (ITER, JET); no fusion-scale commercial NBI O&M data |
| 12 | NBI supply chain scale-up: no commercial manufacturing pathway for reactor-scale high-energy NBI systems | S4 | truly-unknown | important | Review ITER NBI industrial procurement; identify commercial NBI manufacturers |
| 13 | Plant capacity factor target — steady-state concept avoids pulsed penalties but FRC CW operation undemonstrated | S5 | not-yet-sourced | important | Look for TAE operational availability claims or analogue from beam-driven MFE concepts |
| 14 | Copper coil electrical power consumption at Da Vinci scale — continuous operating cost for resistive magnets | S4, S5 | derivable | nice-to-have | Estimable once Da Vinci coil geometry and external field requirements are disclosed |
| 15 | B-11 isotopic enrichment cost if higher purity required than natural abundance | S4 | not-yet-sourced | nice-to-have | B-11 enrichment is commercially available; cost negligible at fuel volumes |

---

## Section 7: Cross-Concept Notes

The only approved prior analysis available is the Spherical Tokamak - HTS (Tokamak Energy, `21-spherical-tokamak-hts`). This concept shares essentially no subsystems, cost structures, or physics regime with the p-B11 FRC. It is included here for completeness of cross-reference.

**From `21-spherical-tokamak-hts`:**  
No material assumptions or cost structures are reused from the ST-HTS analysis. That concept uses REBCO HTS magnets, FLiBe/liquid Li blanket, D-T fuel, 14 MeV neutron management, and quasi-steady pulsed operation — all categorically absent from p-B11 FRC. The REBCO supply chain, tritium infrastructure, and regulatory cost multiplier analyses from that concept are deliberately inapplicable here. Shared observations from all D-T analyses (capacity factor sensitivity, O&M cost gap) are noted but do not directly transfer to a concept that eliminates the dominant D-T engineering challenges.

**Most relevant cross-concept comparisons (not yet approved):**

The Helion FRC (`08-frc-w-direct-conversion`) is the closest near-neighbor on the *confinement topology* dimension — both use FRC geometry with direct energy conversion aspirations and non-tritium fuel. The Helion handwritten exemplar notes that a D-He3 pulsed FRC can achieve ~4 c/kWh with copper coils and no tritium infrastructure, but that capital costs "skyrocket" if HTS is substituted [08-frc-w-direct-conversion.md §Quantitative LCOE]. This analogy is partially relevant: TAE's p-B11 FRC also uses copper resistive magnets and has no tritium or breeding blanket costs. However, Helion's pulsed compression approach differs fundamentally from TAE's steady-state beam-driven approach, and D-He3 is a far more favorable fusion regime than p-B11 (lower temperature requirements, better Lawson criterion, validated 100 million °C performance). The Helion analogy suggests a favorable BOP and magnet cost structure for a p-B11 FRC *if* the physics can be made to work, but it does not address the p-B11 physics feasibility question.

**p-B11 Aneutronic Concept Peers (fuel-dimension neighbors):**

Four other concepts in this pipeline share the p-B11 aneutronic fuel: `06-magnetic-mirror` (Pale Blue Fusion), `04-laser-icf` (HB11 Energy), `23-laser-icf-nanostructured-target` (Marvel Fusion), and `24-dense-plasma-focus` (LPPFusion). All four share the same structural TEA relief from the aneutronic fuel choice: no tritium breeding, minimal neutron shielding, hands-on maintenance, no REBCO or FLiBe supply chain. What distinguishes the FRC NBI-driven approach from these peers is primarily their strategy for escaping the bremsstrahlung power balance problem — the central physics challenge all p-B11 concepts share.

*Dense Plasma Focus — p-B11 (LPPFusion, 24-dense-plasma-focus)*: The DPF takes a pulsed, electromagnetically compressed approach — plasma is heated impulsively to the ~600 keV p-B11 cross-section peak in microsecond pulses via coaxial electrodes (2.7 MA capacitor bank). The short pulse sidesteps the sustained T_i >> T_e requirement entirely: electron equilibration time exceeds the pulse duration, so bremsstrahlung losses during the active phase are suppressed by construction. The tradeoff is high repetition rate (>10 Hz) for commercial power density, electrode erosion, and achieving the required compression ratio at reactor scale. The capital cost structure is radically simpler than TAE's approach — no NBI, no external magnets — but the electrode lifetime and capacitor bank costs at commercial scale are the analogous engineering unknowns. DPF's energy capture is also direct (charged particles), making it structurally similar to TAE's ICC vision but at a lower TRL. In TEA terms: DPF bets on achieving the required ion conditions transiently; TAE bets on sustaining them continuously.

*Magnetic Mirror — p-B11 (Pale Blue Fusion, 06-magnetic-mirror)*: This concept shares the MFE steady-state paradigm with TAE's FRC and similarly proposes direct energy conversion of charged fusion products. The mirror topology differs in having open field lines (end-loss problem) which the FRC avoids by its closed topology. Pale Blue adds alpha channeling (RF waves, E×B rotation, ponderomotive barriers) to suppress end losses and enable direct conversion. Like TAE, this concept faces a sustained non-Maxwellian plasma challenge and a recirculating power burden for continuous RF and NBI heating. The mirror's magnetic field geometry is simpler than the FRC's internal plasma currents, but confinement quality (τ_E) tends to be lower than an FRC at equivalent parameters. Analysis still in progress (iter-1/INTERRUPTED); no direct TEA comparison is available in this pipeline.

*Laser ICF — p-B11 approaches (HB11 Energy, Marvel Fusion; concepts 04 and 23)*: Both IFE approaches use high-intensity pulsed laser drivers to reach p-B11 ignition conditions. Like DPF, the pulsed approach avoids the sustained temperature maintenance problem — bremsstrahlung losses during the implosion are brief enough to be manageable. The penalty is that laser driver efficiency (~10–20% for DPSSL) creates a recirculating power problem structurally analogous to TAE's NBI efficiency challenge. HB11 uses a petawatt ps CPA laser with a laser-driven kT magnetic field to enhance fusion yield; Marvel Fusion uses nanostructured silicon targets (nanowire arrays from semiconductor lithography) to increase reaction cross-section at achievable intensities. In TEA terms, the laser IFE concepts have broadly similar LCOE drivers to TAE (driver wall-plug efficiency, repetition-rate capital for laser systems vs. steady-state NBI) but introduce target fabrication and chamber clearing as additional cost centers absent from the FRC approach.

The FRC NBI-driven approach's distinctive bet in the p-B11 concept family is steady-state, beam-driven non-Maxwellian confinement: if the T_i >> T_e regime can be sustained at commercial scale with high enough Q_plasma, the FRC produces continuous power with no rep-rate or pellet engineering. The downside is that the NBI recirculating power burden is continuous — it cannot be amortized over short pulses the way DPF or laser IFE do.

**Structural TEA differences from all D-T concepts:**

The p-B11 FRC is categorically different from every D-T concept in the pipeline in ways that directly affect the TEA model structure:

1. **No breeding blanket cost account**: Eliminates CAS accounts for blanket manufacturing, Li enrichment, tritium extraction, and blanket coolant. This is a large capital and O&M cost category removed entirely.
2. **No neutron shielding to commercial grade**: Minimal secondary neutron shielding (thin water/boron shield) vs. multi-meter composite shields in D-T. Reduces building volume, structural steel, and remote handling costs.
3. **Hands-on maintenance possible**: Eliminates remote handling robotics capital cost. A major driver of D-T facility O&M costs (ITER remote maintenance systems cost >$500M) is absent.
4. **NBI as dominant cost driver**: The NBI system replaces magnets + blanket as the dominant capital cost item. This is structurally different from any other concept in the pipeline.
5. **Da Vinci thermal conversion is a temporary sub-optimal state**: Unlike D-T concepts where thermal conversion is the optimal long-term choice, Da Vinci's steam cycle is explicitly a stepping stone. The ICC upgrade changes the economic picture substantially (from ~30% to potentially >90% efficiency), meaning Da Vinci LCOE is not representative of the concept's ultimate potential.

**Rough LCOE anchoring against D-T FRC reference:**

The model's Branch B scenario (steam Rankine, Q_plasma = 15) produces LCOE in the range of ~$250–270/MWh — roughly the expected result when aneutronic structural savings (no blanket, no shielding, no tritium) are offset by (a) the NBI recirculating power burden at the realistic η_NBI ≈ 0.20–0.35, and (b) Q_plasma remaining far below the value needed for favorable economics. For comparison, the Helion D-He3 FRC exemplar estimates ~4 ¢/kWh (~$40/MWh) for a D-He3 pulsed FRC with copper coils, no tritium, and an optimistic direct conversion pathway [08-frc-w-direct-conversion.md §Quantitative LCOE]. This reference is not directly comparable — it uses a pulsed compression approach, D-He3 fuel (far more favorable physics), and assumes direct conversion rather than steam — but it illustrates that the ~$250/MWh Branch B result is 6× worse than the best analogous D-T-free FRC estimate, confirming that steam-mode p-B11 FRC is not economically competitive even against its nearest neighbor.

The Branch C scenario (ICC direct conversion, η_conv ~90%) drops LCOE to ~$75–80/MWh — closer to the D-T compact tokamak range, and competitive if the NBI Q_plasma requirements can be met. This confirms the economic logic of the aneutronic fuel choice: the concept's value proposition depends entirely on ICC demonstration, not on the steam-cycle Da Vinci design.

*Note: Branch B and Branch C LCOE figures are model outputs (model_setup.py) subject to revision as the fuel cost error (CF-F-1) and bremsstrahlung sweep (CF-F-2) are corrected. The Helion reference is from a handwritten exemplar, not a validated LCOE model.*

---

## Section 8: Sources

**1. Grokipedia — TAE Technologies (comprehensive concept summary)**
- Contribution: Third-party narrative synthesis of TAE's machine history, performance milestones, technical approach, FRC physics, cost claims, and technical risk assessment for p-B11 FRC. Primary narrative source for concept positioning, plasma physics challenges, and stability risks.
- Location: Phase 1a source [iter-01/sources/grokipedia-tae-technologies.md]

**2. TAE Energy Conversion Notes (foundational ICC/FRC patent, ~2001–2002)**
- Full citation: Rostoker, N. et al., US patents US7459654, US6628740, US6888907 (Tri Alpha Energy / UC / UF). Detailed ICC converter design and FRC fusion plasma parameters for p-B11.
- Contribution: Technical design parameters for the ICC direct conversion system (>90% efficiency claim, ion rotation frequency 1–10 MHz, coherent beam parameters). Plasma parameter design point (ion temp 30–230 keV, external field 2.5–15 kG). Confirms theoretical basis for direct conversion efficiency.
- Location: Phase 1a source [iter-01/sources/tae-energy-conversion-notes.md]

**3. TAE NBI Breakthrough Press Release (2025)**
- Full citation: TAE Technologies press release, April 2025. "NBI-Only FRC Formation." Reports on "Norm" device achieving NBI-only plasma formation.
- Contribution: Confirms 50% cost reduction claim from NBI-only formation approach. Establishes Norm as highest-performance TAE machine. Confirms path to Copernicus.
- Location: Phase 1a source [iter-01/sources/tae-nbi-breakthrough-2025.md]

**4. TAE C-2W Machine Details (IAEA FEC 2020 paper)**
- Contribution: Authoritative C-2W/Norman plasma parameters: Ttot ~3 keV, Te ~300 eV, ne 1–3 × 10¹⁹ m⁻³, flux ~5–10 mWb, external field ~1 kG, NBI up to 21 MW. Confinement time up to 30 ms. Primary quantitative source for current experimental performance.
- Location: Phase 1a source [iter-02/sources/tae-c2w-machine-details.md]

**5. TAE DJT Merger / Da Vinci Specs (December 2025)**
- Full citation: TAE Technologies / Trump Media and Technology Group merger announcement, December 2025.
- Contribution: Authoritative source for Da Vinci 50 MWe specification and commercial timeline (construction 2026, first plasma 2029, net energy 2030, power operations 2031). Total funding: >$1.3B.
- Location: Phase 1a source [iter-02/sources/tae-djt-merger-davinci-specs.md]

**6. TAE Energy Conversion Clarification (FAQ)**
- Contribution: Official TAE FAQ confirming Da Vinci baseline as thermal/steam conversion (not ICC). Confirms p-B11 aneutronic fuel strategy. Establishes that ICC is a future upgrade, not Da Vinci baseline. Primary source for energy capture classification.
- Location: Phase 1a source [iter-02/sources/tae-energy-conversion-clarification.md]

**7. Phase 1a Dossier — p-B11 FRC (18-p-b11-frc)**
- Contribution: Consolidated taxonomy values with confidence ratings and citations for all differentiation columns. Key sources: NBI quadruple duty, Da Vinci specs, FRC near-unity beta, aneutronic fuel classification, resistive magnet inference.
- Location: [knowledge/concept_research/18-p-b11-frc/dossier.md]

**8. Handwritten exemplar — FRC with Direct Conversion (Helion, 08-frc-w-direct-conversion)**
- Contribution: Nearest-neighbor FRC LCOE estimate (~4 c/kWh for D-He3 pulsed FRC with copper coils, no tritium). Qualitative parallel for BOP cost structure and magnet cost advantage. Notes He-3 fuel cost as dominant driver — analogously, p-B11 NBI cost may be the analogous dominant driver.
- Location: [exploration/concept_analysis/handwritten/08-frc-w-direct-conversion.md]

**9. Nature Communications 2025 — NBI-Only FRC Formation**
- Full citation: TAE Technologies / collaborators (2025). "NBI-Only FRC Formation." *Nature Communications*, s41467-025-58849-5.
- Contribution: Peer-reviewed confirmation of NBI-only FRC formation breakthrough. Establishes elimination of plasma gun hardware and 50% complexity reduction claim.
- Location: External publication; cited in dossier.md [knowledge/concept_research/18-p-b11-frc/dossier.md §Primary Heating]

**10. Mulder et al. (2021) — Fusion Plant Efficiency: Capacity Factor and Recirculated Power**
- Full citation: Mulder et al. (2021). arXiv:2103.12451. Plant efficiency of a nuclear fusion power plant accounting for capacity factor and recirculated power fraction.
- Contribution: Establishes the compounding relationship between capacity factor and recirculating power fraction for fusion plants. Key finding: recirculated power remains high at reduced output, so sub-unity capacity factor raises the effective recirculating power fraction. Informs the Section 2 Challenge 3 discussion of Q_plasma floor sensitivity and the Section 5 Gap #13 cross-reference.
- Location: Phase 1b source [iter-02/sources/arxiv-2103-12451.md] — abstract only; full paper at arXiv:2103.12451

**11. TAE Technologies / OSTI 2441289 — C-2W Performance Report (*Nuclear Fusion* 2024)**
- Full citation: TAE Technologies team (2024). Advanced performance in C-2W field-reversed configuration plasmas. *Nuclear Fusion*. OSTI:2441289.
- Contribution: Primary quantitative source for three key iter-3 updates: (a) Te milestone of ~1 keV peak (>0.75 keV averaged) — first time achieving 1 keV in C-2W; (b) total plasma energy record of ~13 kJ; (c) NBI efficiency data — attenuated power is "less than half of the electrical power" from duct geometry, neutralization, and charge-exchange effects, with 15±5% additional beam shine-through; (d) SEQUOIIA equilibrium reconstruction confirming fast-ion pressure exceeds thermal plasma pressure by ~1.5× in the core of high-performing shots. Critical for revising the Q_plasma viability threshold in Section 2 Challenge 3 and the fast-ion TRL assessment in Sections 2 and 3.
- Location: Phase 1b source [iter-02/sources/osti-pages-servlets-purl-2441289.md]
