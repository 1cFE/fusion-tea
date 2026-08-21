# Phase 3 diff: 19-orbital-levitated-dipole

**Generated:** 2026-05-22T14:46:25-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 10 | 7 | -3 |
| important_count  | 7 | 8 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
Now I have enough information to write the full assessment. I've read all concept-scoped sources and the applicable fleet-wide sources.
```

## Blocking-tier lines (new)

```
31:- No company technical disclosures — proprietary — **blocking**
32:- No D-He3 orbital dipole design study — truly-unknown — **blocking**
53:- Energy conversion pathway (fusion → beamable power) — proprietary/truly-unknown — **blocking**
54:- D-He3 burning conditions in dipole geometry not modeled or published — not-yet-sourced — **blocking**
79:- Space-hardened HTS cryogenic system: core engineering bet with no existing design — not-yet-sourced — **blocking**
105:- He-3 supply at fusion scale: no viable production pathway exists — truly-unknown — **blocking**. Global production (~15,000 liters/year) is estimated to be orders of magnitude below what a MW-class D-He3 device would consume.
131:| Fusion gain Q | proprietary | blocking | No target disclosed; D-He3 requires far higher confinement than D-T; Q<1 likely initially |
132:| Net power output | proprietary | blocking | MW-class claimed but no specific target; required for all normalization |
133:| Capital cost by subsystem (CAS) | truly-unknown | blocking | No plant study; orbital concept lacks standard CAS structure (no blanket, no steam cycle, no power block) |
134:| Energy conversion efficiency | truly-unknown | blocking | Fusion → direct conversion → RF beam → rectenna chain undefined; end-to-end efficiency unknown |
135:| Capacity factor / availability | truly-unknown | blocking | No plant design basis; orbital ops subject to debris avoidance, orbit decay, docking cycles |
136:| O&M cost model | truly-unknown | blocking | On-orbit maintenance has no cost analog; resupply logistics undefined |
137:| He-3 fuel cycle cost | truly-unknown | blocking | No fusion-scale He-3 supply exists; cost would be indeterminate |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/19-orbital-levitated-dipole.md	2026-05-22 12:59:21.074580760 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/gap_report.md	2026-05-22 14:46:25.127753401 -0700
@@ -1,12 +1,10 @@
-I now have sufficient information to write the gap assessment. Let me compose it.
+Now I have enough information to write the full assessment. I've read all concept-scoped sources and the applicable fleet-wide sources.
 
 # Gap Assessment: Orbital Levitated Dipole (D-He3)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
-**Summary**: Zephyr Fusion (YC F25, founded 2025) has disclosed essentially nothing beyond a marketing launch page. The concept's fundamental novelty — orbital deployment, D-He3 fuel, direct energy conversion, power beaming — places every LCOE-relevant parameter either unknown or outside the applicable range of conventional fusion plant methodology. The one substantive technical source found during Phase 1a research (arXiv 2602.20564, OpenStar DT levitated dipole) addresses a terrestrial D-T dipole with a blanket and thermal cycle, which is architecturally distinct from Zephyr's concept in every dimension that matters for cost modeling. A D1+ analysis can be written, but it will read as a structured inventory of unknowns with physics-based bounds rather than a quantitative LCOE estimate.
-
----
+**Summary**: Zephyr Fusion (YC F25, founded 2025, 2 employees, pre-prototype) has disclosed no plasma performance targets, no energy conversion mechanism, and no reactor design in any public source. The concept's most fundamental parameters — Q value, net power output, heating method, and the fusion-to-beamable-power conversion chain — remain either proprietary or technically undefined. Additionally, the D-He3 fuel cycle requires He-3 at scales orders of magnitude beyond current global production, and no credible supply pathway exists at fusion scale. A qualitative narrative can be structured around dipole physics heritage and the orbital architecture concept; a quantitative LCOE model cannot be responsibly constructed.
 
 ## Section Coverage
 
@@ -14,25 +12,25 @@
 **Coverage**: Poor
 
 **Available**:
-- Company description at marketing level: YC launch page (`iter-01/sources/yc-launch-page.md`) — one paragraph on physics concept, no technical parameters
-- Peripheral press coverage: DCD article (`iter-02/sources/zephyr-fusion-web-sources-2026.md`) — paraphrases YC post, adds nothing
-- Community skepticism: NASASpaceFlight forum (`iter-01/sources/nasaspaceflight-forum-discussion.md`) — highlights absence of power conversion, heat removal, and blanket
-- Concept heritage: Wikipedia levitated dipole article (`iter-01/sources/levitated-dipole-technical-background.md`) — LDX, RT-1 experiments, Hasegawa 1987 proposal; no quantitative fusion parameters
-- Terrestrial dipole analog: OpenStar arXiv 2602.20564 (`iter-02/sources/dipole-reactor-heating-energy-conversion.md`) — detailed D-T dipole plant study (208 MWe), but fundamentally different fuel, location, and power delivery
-- He-3 supply context: CRS Report R41419 (`iter-02/sources/everycrsreport-reports-r41419.md`) — comprehensive analysis of He-3 shortage; global supply ~8,000 L/yr from weapons program
+- YC launch page (`iter-01/sources/yc-launch-page.md`): physics basis (τₑ ~ R² scaling, dipole magnetosphere analogy), market positioning (orbital industrial power), hardware approach (meter-scale REBCO coil, Falcon 9 deployable), founder credentials (ORNL, LLNL, W7-X, DIII-D), claimed cost comparisons (ISS solar at ~$1B/MW, ITER at ~$650M/MW)
+- Community technical critique (`iter-01/sources/nasaspaceflight-forum-discussion.md`): identifies key gaps — no blanket, no heat output, no power conversion, no tritium breeding
+- Levitated dipole heritage (`iter-01/sources/levitated-dipole-technical-background.md`): LDX (MIT, Nature Physics 2010), RT-1 (U. Tokyo), OpenStar 2024 helium ionization demonstration, terrestrial dipole landscape
+- OpenStar D-T dipole reactor paper (`iter-02/sources/dipole-reactor-heating-energy-conversion.md`, arxiv 2602.20564): detailed D-T terrestrial levitated dipole engineering study — REBCO coil design, heating options with efficiency figures (ECRH 30-40%, ICRH 70%, NBI), neutron shielding, plant power balance equations, assumed thermal efficiency 40%, cryogenic efficiency 1.25%; D-T reactor designs at 667 MW fusion / 208 MW net electric
+- He-3 supply chain (`iter-02/sources/everycrsreport-reports-r41419.md`): CRS congressional report on He-3 shortage — historical prices ($40-85/liter from DOE auctions), production sources (primarily weapons tritium decay at ~15,000 liters/year peak), alternative sources (CANDU byproduct, particle accelerators, atmospheric extraction), quantified shortage context at neutron-detection scale
+- Power beaming context (`iter-02/sources/arxiv-2401-15267.md`): Caltech/MAPLE WPT experiment demonstrating flexible coherent WPT array in LEO for 8 months; RF pointing to ground confirmed (`iter-02/sources/nss-wp-content-uploads-2017-07-space-solar-power-workshop.md`): WPT microwave theory and SPS transmission efficiency framework
+- Web survey (`iter-02/sources/zephyr-fusion-web-sources-2026.md`): confirms no additional technical content beyond YC page across FusionXInvest, Fondo, DCD, LinkedIn sources
 
 **Missing**:
-- Any Zephyr technical paper, patent, or conference presentation
-- Hasegawa & Chen (1987) D-He3 dipole proposal (cited but not extracted)
-- LDX and RT-1 experimental papers with plasma parameter data
-- Any prior D-He3 dipole reactor study (ARIES-III covers D-He3 in a tokamak, not dipole)
-- Direct conversion technology literature (Hasegawa-type separatrix direct converter, not extracted)
+- Any Zephyr-authored technical document (paper, patent, conference presentation)
+- D-He3 orbital dipole design study — no peer-reviewed reactor study for this specific configuration exists
+- Teller et al. 1992 "Space Propulsion by Fusion in a Magnetic Dipole" — original orbital dipole proposal (referenced in YC page but not extracted)
+- Hasegawa & Chen 1987 PPPL-2627 — original D-He3 dipole proposal (referenced throughout but not extracted)
+- ARIES-III study — D-He3 advanced fuel tokamak with direct energy conversion analysis
 
 **Gaps**:
-- No company technical disclosures exist — `proprietary` — **blocking**: can only make physics inferences, no engineering parameters
-- Hasegawa 1987 D-He3 dipole paper not extracted — `not-yet-sourced` — **important**: foundational document underpinning the concept
-- LDX/RT-1 experimental results not extracted — `not-yet-sourced` — **important**: only experimental data on dipole plasma performance
-- ARIES-III D-He3 study not extracted — `not-yet-sourced` — **important**: only prior cost study for D-He3 fusion (tokamak geometry, but relevant for fuel cycle and direct conversion costs)
+- No company technical disclosures — proprietary — **blocking**
+- No D-He3 orbital dipole design study — truly-unknown — **blocking**
+- Teller 1992 and Hasegawa 1987 original papers not extracted — not-yet-sourced — important
 
 ---
 
@@ -40,23 +38,22 @@
 **Coverage**: Poor
 
 **Available**:
-- Physics rationale for orbital advantage: YC launch page and OpenStar paper establish that (a) dipole confinement benefits from large plasma volume, (b) space vacuum eliminates vacuum vessel as loss mechanism, (c) τ_e ~ R² scaling applies. The physics logic is documented.
-- Qualitative power conversion pathway: Dossier inference + Hasegawa 1987 heritage that D-He3 dipole at separatrix enables direct charged-particle deceleration. This is physics-consistent but unconfirmed by Zephyr.
-- Heating options: OpenStar paper (`iter-02/sources/dipole-reactor-heating-energy-conversion.md`, Section 2.2.7) systematically evaluates ECRH (30-40% efficiency), ICRH (~70% efficiency), and NBI for terrestrial dipoles; these constraints apply qualitatively to the orbital case.
-- Terrestrial D-T dipole power balance equations: OpenStar paper Table 2 provides η_th = 0.4, η_aux = 0.7, η_cryo = 0.0125, duty cycle ~90%, Q_sci = 15 targets. These are analogs for some subsystems, but inapplicable to the D-He3 direct-conversion orbital scenario.
+- Dipole confinement physics (LDX/RT-1 heritage): turbulent inward pinch confirmed, peaked pressure profiles, natural stability to interchange modes; τₑ ~ R² scaling motivates large plasma volumes
+- D-T dipole engineering analysis (`dipole-reactor-heating-energy-conversion.md`): equilibrium physics (Grad-Shafranov, Eq. 1-6), β limits, plasma edge conditions, energy confinement time framework, power balance model (Equations 9-20 in OpenStar paper); identifies that transport in the "good curvature" region approaching inner first closed flux surface is a key open physics question
+- Heating options with efficiency data: ECRH (30-40% wall-plug, high cutoff density, high-field-side launch), ICRH (70% efficiency, complex antenna geometry, ongoing investigation), NBI (mature, geometrically compatible with dipoles)
+- Power beaming infrastructure: microwave WPT demonstrated in LEO at small scale; transmission efficiency theory well-developed for SPS concepts
 
 **Missing**:
-- Power delivery mechanism: "power beaming partners" is stated in dossier but mechanism is unspecified. The arxiv 2401.15267 paper (`iter-02/sources/arxiv-2401-15267.md`) covers lightweight coherent RF arrays for space-to-ground wireless power transfer (solar power context), providing some efficiency reference (~end-to-end ~12-20% for SPS), but this is for solar, not fusion-scale MW power beaming.
-- Direct energy conversion at separatrix: No source in the collection addresses the engineering implementation of charged-particle direct conversion for a dipole. The concept is physically motivated (Hasegawa 1987) but no engineering design or efficiency estimate exists in any extracted source.
-- Station-keeping and orbital mechanics: What maintains the coil in a stable orbit while the surrounding plasma extends 10-50 m? No source addresses this.
-- Plasma-spacecraft interaction in LEO: No source addresses particle/radiation environment effects on the HTS coil or plasma boundary.
-- D-He3 physics scaling to fusion-relevant conditions: No levitated dipole has ever operated near D-He3 fusion conditions (requires ~60 keV ion temperatures; LDX operated at ~100 eV).
+- D-He3 fusion performance in dipole geometry: D-He3 requires ~60 keV ion temperature vs. ~15 keV for D-T; triple product requirement is ~100× harder; no published analysis asks whether an orbital dipole can reach D-He3 burning conditions
+- Energy conversion chain: the full pathway from fusion-product charged particles (85% of D-He3 energy) through direct conversion at the separatrix, to DC power, to RF beam — undesigned and unanalyzed
+- Orbital plasma environment effects: LEO atomic oxygen erosion, charged particle belt radiation effects on plasma, microgravity effects on plasma fueling and particle injection
+- Fueling system design: D and He-3 injection on orbital platform not addressed
 
 **Gaps**:
-- Energy conversion pathway (direct conversion + power beaming) is completely uncharacterized — `truly-unknown` at engineering level, `not-yet-sourced` for Hasegawa-type direct conversion literature — **blocking**: determines what fraction of fusion energy becomes deliverable power
-- Plasma-orbit stability and spacecraft integration — `truly-unknown` — **blocking**: no analog exists for an orbital fusion plasma device
-- D-He3 confinement scaling from LDX to reactor-scale — `truly-unknown` — **important**: no data exists for this extrapolation, orders of magnitude in triple product separate LDX from fusion conditions
-- D-He3 vs D-T reactivity disadvantage: D-He3 requires ~10× higher triple product than D-T; LDX never approached this. The OpenStar paper (DT focus) explicitly notes that prior advanced-fuel dipole designs were infeasible due to triple-product requirements — `derivable` from literature but not yet compiled — **important**
+- Energy conversion pathway (fusion → beamable power) — proprietary/truly-unknown — **blocking**
+- D-He3 burning conditions in dipole geometry not modeled or published — not-yet-sourced — **blocking**
+- Orbital plasma environment effects on confinement — truly-unknown — important
+- On-orbit fueling system design — proprietary/not-yet-sourced — important
 
 ---
 
@@ -64,124 +61,130 @@
 **Coverage**: Partial
 
 **Available**:
-- HTS coil technology: OpenStar paper establishes REBCO-based dipole coil design, CICC architecture, 23 T peak field, structural over-band design. This is TRL 4-5 for terrestrial operation; orbital deployment would downgrade to TRL 2-3.
-- Coil levitation physics: LDX (TRL 5-6 for demonstration levitation), RT-1 (TRL 5-6 for HTS levitation). Both are terrestrial, small-scale.
-- Space launch of HTS systems: No dedicated heritage, but Falcon 9 rideshare for meter-scale payloads is TRL 9. The challenge is operating superconducting coils in LEO thermal/radiation environment.
-- Power beaming (microwave/laser): arxiv 2401.15267 and NSS SPS workshop (`iter-02/sources/nss-wp-content-uploads-2017-07-space-solar-power-workshop.md`) provide context for WPT arrays. TRL 4-6 for small-scale space demonstrations.
+- **REBCO HTS coil (terrestrial)**: TRL 6-7. OpenStar Junior device validated 14-coil REBCO assembly with levitation and internal low-field shielding region (`dipole-reactor-heating-energy-conversion.md`). Commercial tape available from multiple vendors. Faraday Factory "Mirai" tape at >1000 A/mm² engineering current density.
+- **Orbital HTS deployment**: TRL 2-3. No superconducting magnet system has operated in LEO. The OpenStar paper's cryogenic slush strategy (neon slush, 5-minute docking intervals) is designed for terrestrial operation; an orbital equivalent is undesigned.
+- **ECRH heating (terrestrial)**: TRL 6-7. Demonstrated on LDX, RT-1, and W7-X. Orbital adaptation TRL 2-3 (no space plasma heating system built).
+- **ICRH (terrestrial)**: TRL 4-5 for dipole geometry (demonstrated on RT-1 with "mixed results" per OpenStar paper). Ongoing at OpenStar. Orbital adaptation TRL 2.
+- **Power beaming (microwave WPT)**: TRL 4-5. Caltech/MAPLE LEO WPT experiment demonstrated 8-month operation of flexible coherent arrays, RF beam pointing confirmed to ground stations (`arxiv-2401-15267.md`). Efficiency at SPS scale (>85% rectenna) is theoretical.
+- **Direct energy conversion**: TRL 2-3. Concept studied for D-He3 tokamak in ARIES-III (not extracted), no experimental demonstration.
+- **SpaceX Falcon 9 launch**: TRL 9. Rideshare economics available.
 
 **Missing**:
-- Compact RF heating (ECRH or ICRH) for orbital deployment: No space-compatible heating system design exists in any source
-- Direct energy converter for D-He3 charged particles at separatrix: Only theoretical proposal (Hasegawa 1987); no experimental or engineering demonstration
-- Cryogenic coil management in LEO thermal cycling (beta angle, eclipse/sunlight cycling): Not addressed in any source
-- Plasma diagnostics and control for orbital device: Not addressed
+- TRL for space-rated HTS cryogenic system (the orbital equivalent of neon slush docking strategy)
+- TRL for D-He3 direct conversion at dipole separatrix
+- TRL for He-3 fuel handling in orbit (pressurized gas management, radiation shielding of inventory)
+- System-level TRL integration for the complete orbital fusion platform
 
 **Gaps**:
-- Direct energy conversion at separatrix: TRL 1-2 — `truly-unknown` at engineering level — **blocking**
-- Compact RF heating system for space: TRL 2-3 — `not-yet-sourced` (defense/directed-energy literature may have compact gyrotron designs) — **important**
-- Orbital HTS coil thermal management: TRL 3-4 — `not-yet-sourced` — **important**
-- No TRL documentation exists for any Zephyr-specific component — `proprietary` — **important**
+- Space-hardened HTS cryogenic system: core engineering bet with no existing design — not-yet-sourced — **blocking**
+- Direct energy conversion TRL and engineering maturity — not-yet-sourced (ARIES-III not extracted) — important
+- He-3 on-orbit fuel handling: no published design — truly-unknown — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial (He-3 supply well-documented; others minimal)
+**Coverage**: Partial (He-3 supply well-covered by CRS report; system-level supply chain poor)
 
 **Available**:
-- He-3 supply chain: CRS Report R41419 (`iter-02/sources/everycrsreport-reports-r41419.md`) is comprehensive. Key facts: global supply ~8,000 L/yr from tritium decay in weapons programs; historical price $40-85/L (pre-shortage), spiked significantly; shortage documented as of 2009. Production tied to nuclear weapons maintenance, not adjustable to meet fusion demand.
-- REBCO tape: OpenStar paper establishes ~4,320 km of REBCO tape required for their 208 MWe terrestrial reactor. Current REBCO supply chain (SuperOx, Faraday Factory, SuNAM) is growing but not at scale for fusion. For orbital deployment, radiation hardness of REBCO in LEO environment is unverified.
-- Deuterium: Abundant, not a supply constraint.
+- **REBCO HTS tape**: Mature commercial supply chain (SuperOx, Fujikura, AMSC, Faraday Factory). Cost declining with demand growth from MRI and fusion programs. No supply chain bottleneck identified for this concept.
+- **He-3 fuel supply** (`everycrsreport-reports-r41419.md`): comprehensive CRS data —
+  - Historical auction price: $40-85/liter (U.S. DOE; pre-shortage)
+  - Primary production: tritium decay from nuclear weapons stockpile (~15,000 liters/year at peak U.S. production)
+  - By 2009, neutron-detection demand (thousands of liters/year) alone exceeded supply; federal rationing implemented
+  - Alternative sources: CANDU heavy-water reactor byproduct (small quantities), particle accelerator production (expensive), natural gas/atmosphere extraction (trace only), lunar regolith (long-term, speculative)
+  - No fusion-scale He-3 demand has ever been analyzed or planned for in any source reviewed
+- **Launch vehicle**: SpaceX Falcon 9 rideshare economics available; Falcon 9 fairing constrains coil geometry (YC launch page)
 
 **Missing**:
-- He-3 quantity required for D-He3 orbital dipole: No published estimate for the Zephyr concept or any D-He3 dipole reactor exists in the sources. The D-He3 fusion reaction consumes He-3 at a rate dependent on fusion power and fuel cycle efficiency — not calculable without plasma parameters.
-- He-3 price at scale: CRS report cites historical prices for detector-grade quantities; fusion-scale demand (orders of magnitude larger) would require new production pathways at unknown cost
-- REBCO radiation hardness in LEO: Not addressed in any source; DD neutrons from D-He3 side reactions would continuously irradiate the coil
+- He-3 demand estimate for a MW-scale D-He3 fusion device: no calculation in any source; first-principles estimate suggests MW-class D-He3 fusion would consume more He-3 annually than the entire current global He-3 production
+- Current He-3 market pricing (post-2010): the CRS report is from 2010; prices rose dramatically after the shortage and current market is opaque
+- Radiation-hardened electronics supply chain for orbital plasma systems
+- Space-rated cryogenic system supply chain
 
 **Gaps**:
-- He-3 fuel quantity and cost per unit energy: No fusion-scale production or cost estimate exists — `truly-unknown` for fusion application, though CRS report provides useful supply context — **blocking** for any cost model
-- He-3 production at fusion scale: Current global supply completely inadequate for a power plant; alternative production (tritium decay, lunar mining) is speculative — `not-yet-sourced` (lunar He-3 literature exists but is unverified for this analysis) — **blocking**
-- REBCO radiation tolerance in LEO: `not-yet-sourced` — **important**
+- He-3 supply at fusion scale: no viable production pathway exists — truly-unknown — **blocking**. Global production (~15,000 liters/year) is estimated to be orders of magnitude below what a MW-class D-He3 device would consume.
+- He-3 post-2010 market pricing: not captured — not-yet-sourced — important
+- Radiation-hardened cryogenic and plasma-system electronics: supply chain unassessed — not-yet-sourced — important
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Available Parameters**:
+**Coverage**: Poor
 
+**Note on metric applicability**: The orbital concept does not target terrestrial $/MWh LCOE. The value proposition is orbital power at $/kW to space customers. Standard CAS-based LCOE methodology partially applies (capital cost, O&M, utilization/capacity factor) but the power market is fundamentally different from grid electricity.
+
+**Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Target power output | MW-class (orbital) | YC launch page | low |
-| Confinement concept | Dipole, τ_e ~ R² | YC + LDX Nature Physics 2010 (cited) | medium |
-| Magnet type | REBCO, meter-scale, Falcon 9-deployable | YC launch page | high |
-| Steady-state operation | Yes | Dossier inference | high |
-| Heating efficiency (ICRH analog) | ~70% wall-plug | OpenStar paper (DT terrestrial) | low (D-T analog only) |
-| Heating efficiency (ECRH analog) | 30-40% wall-plug | OpenStar paper (DT terrestrial) | low (analog) |
-| D-He3 charged particle fraction | ~85% | Physics — standard D-He3 reaction | medium |
-| DD neutron energy fraction | ~10% | Physics — standard D-He3 side reactions | medium |
-| He-3 current global supply | ~8,000 L/yr | CRS R41419 | high |
-| He-3 historical price | $40-85/L (pre-shortage) | CRS R41419 | high |
-| Power beaming end-to-end efficiency (SPS analog) | ~12-20% | arxiv 2401.15267 + NTRS SPS comparison | low (solar, not fusion) |
-| Comparable ISS solar cost | ~$1B/MW installed | YC launch page (Zephyr's own claim) | medium |
-| Zephyr claimed total cost | <$30M | YC launch page | very low (marketing) |
+| Target power class | MW-scale (unspecified) | YC launch page | l |
+| HTS coil technology | REBCO, up to 23 T peak (D-T analog) | OpenStar D-T dipole paper, §2.2.1 | l (analog) |
+| Thermal efficiency (D-T analog) | 40% | OpenStar D-T dipole, Table 2 | l (analog) |
+| ICRH auxiliary heating efficiency | 70% | OpenStar D-T dipole, Table 2 | l (analog) |
+| Cryogenic system efficiency | 1.25% | OpenStar D-T dipole, Table 2 | l (analog only) |
+| He-3 historical fuel price | $40–85/liter | CRS He-3 report, p.2 | l (outdated, pre-shortage) |
+| Terrestrial modular fusion LCOE analog | $34–54/MWh (~$43/MWh average) | ARPA-E ALPHA revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) | l (analog only) |
+| ISS solar power cost reference | ~$1B/MW | YC launch page | m |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Plant electrical output (MWe) | proprietary | blocking | No target specified; "megawatt-class" only |
-| Fusion power (MWth) | proprietary | blocking | No target; coil size/field not disclosed |
-| Q (fusion gain) | proprietary | blocking | Not disclosed; D-He3 requires Q >> D-T |
-| Energy conversion efficiency (direct + beaming) | truly-unknown | blocking | No demonstrated direct converter for dipole; beaming efficiency at MW scale uncharacterized |
-| Capital cost breakdown by subsystem | proprietary | blocking | No cost estimate at any level |
-| Launch cost (mass to LEO) | derivable | blocking | Requires coil mass + full system manifest; coil mass not disclosed |
-| Operating cost (orbital maintenance, station-keeping) | truly-unknown | blocking | No comparable orbital fusion system exists |
-| He-3 fuel cost per MWh | derivable | blocking | Requires fusion parameters + He-3 price at scale; neither known |
-| Capacity factor / availability | derivable | blocking | Requires operational cadence; orbital logistics completely uncharacterized |
-| Power beaming losses | not-yet-sourced | blocking | MW-class space-to-orbit power beaming not demonstrated; solar analogs give rough bounds |
-| D-He3 triple product requirement | derivable | important | ~60 keV ion temperature needed; ~10× harder than D-T |
-| Cryogenic power load in orbit | derivable | important | Requires thermal environment model + coil mass |
-| He-3 production at reactor scale | truly-unknown | blocking | Current global supply inadequate by orders of magnitude; lunar/accelerator sources speculative |
+| Fusion gain Q | proprietary | blocking | No target disclosed; D-He3 requires far higher confinement than D-T; Q<1 likely initially |
+| Net power output | proprietary | blocking | MW-class claimed but no specific target; required for all normalization |
+| Capital cost by subsystem (CAS) | truly-unknown | blocking | No plant study; orbital concept lacks standard CAS structure (no blanket, no steam cycle, no power block) |
+| Energy conversion efficiency | truly-unknown | blocking | Fusion → direct conversion → RF beam → rectenna chain undefined; end-to-end efficiency unknown |
+| Capacity factor / availability | truly-unknown | blocking | No plant design basis; orbital ops subject to debris avoidance, orbit decay, docking cycles |
+| O&M cost model | truly-unknown | blocking | On-orbit maintenance has no cost analog; resupply logistics undefined |
+| He-3 fuel cycle cost | truly-unknown | blocking | No fusion-scale He-3 supply exists; cost would be indeterminate |
+| Launch cost contribution | not-yet-sourced | important | Falcon 9 rideshare pricing exists but coil mass unspecified; not integrated |
+| Power beaming infrastructure cost | not-yet-sourced | important | Rectenna ground infrastructure, orbital relay costs not addressed |
+| Plant lifetime in LEO | truly-unknown | important | REBCO lifetime under LEO radiation environment uncharacterized |
 
 ---
 
 ## Source Recommendations
 
-1. **Hasegawa & Chen (1990), "A D-3He fusion reactor based on a dipole magnetic field"** — cited in OpenStar paper as Hasegawa et al. 1990; also Hasegawa (1987) original. These are foundational for D-He3 dipole physics and direct energy conversion design. Search PPPL report PPPL-2627 and journal *Comments on Plasma Physics and Controlled Fusion* 11(3):147-151. — `unverified — confirm existence before searching`
+**Sources to acquire for qualitative analysis improvement**:
+- **Teller et al. 1992** "Space Propulsion by Fusion in a Magnetic Dipole," Fusion Technology: original orbital dipole proposal, physics case for D-He3 burning at large magnetospheric scale. Search OSTI/Fusion Technology journal archives. `not-yet-sourced`
+- **Hasegawa & Chen 1987** PPPL-2627: original D-He3 dipole design with direct conversion. Available via INIS or PPPL technical reports. `not-yet-sourced`
+- **ARIES-III study** (Najmabadi et al.): D-He3 advanced fuel tokamak with direct conversion of charged particles and synchrotron radiation rectennas — closest analog for energy conversion efficiency data. Search ARIES project publications via OSTI. `not-yet-sourced`
+- **Kesner et al. 2003** "Helium catalysed D-D fusion in a levitated dipole": D-D/He-3 fuel cycle analysis for dipole geometry (cited in OpenStar D-T paper). Journal of Plasma Physics. `not-yet-sourced`
+- **LDX experimental papers** (Boxer et al. 2010, Nature Physics; Garnier et al. 2006): quantitative achieved plasma parameters (n, T, β, τₑ) from the only levitated dipole demonstrating turbulent inward pinch. `not-yet-sourced`
+- **He-3 current pricing**: DOE Office of Isotope R&D and Production annual reports (post-2010). Current price is likely substantially higher than the $40-85/liter in the CRS report. `not-yet-sourced` — confirm existence before searching
+- **Wurzel & Hsu 2021** (meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/): Contains levitated dipole LDX data point in their cross-concept physics progress compilation. Already in repo — recommend reading for TRL physics baseline.
 
-2. **LDX experimental papers** — Boxer et al. (2010), Nature Physics, "Turbulent inward pinch of plasma confined by a levitated dipole magnet" — the primary experimental validation of dipole confinement. Directly cited by Zephyr. Available on Nature Physics. — `not-yet-sourced`
+**Fleet-wide source disqualifications** (sources read or assessed; not applicable to this concept):
 
-3. **Kesner et al. (2003), "Helium catalysed D–D fusion in a levitated dipole"** — cited in OpenStar paper; directly addresses DD → He3 → D-He3 fuel cycle in levitated dipole context. Relevant for tritium breeding and advanced fuel cycle. — `not-yet-sourced`
+- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Read. Provides terrestrial modular fusion LCOE analog ($34-54/MWh for ~500 MWe). Integrated as order-of-magnitude cost reference in §5. Does not downgrade any blocking gap: the orbital concept's economics differ fundamentally (no grid delivery, no conventional CAS structure, no terrestrial BOP), and the ALPHA concepts were D-T MIF concepts with standard power blocks.
 
-4. **ARIES-III D-He3 tokamak design study** — covers direct energy conversion from charged D-He3 products in a tokamak, relevant as the only full cost study for D-He3 fusion including direct converter design. Search OSTI for "ARIES-III" and "D-He3 direct energy conversion." — `not-yet-sourced, unverified — confirm existence before searching`
+- **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Applicable to D-T MFE with blanket, steam cycle, and tritium breeding. The orbital concept has none of these subsystems. The CAS structure provides vocabulary but no transferable cost data. Disqualified for quantitative use.
 
-5. **Wallace et al. (2025), "Ion Cyclotron Heating in a Levitated Dipole Fusion Reactor"** — cited in OpenStar paper; directly addresses ICRH in dipole geometry. Most current heating study for this concept. — `not-yet-sourced`
+- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Standard CAS framework (accounts 20-27 direct, 90-98 indirect). Inapplicable: no CAS 23 (vacuum vessel/blanket), no CAS 24 (power turbine plant), no CAS 26 (heat rejection), no conventional BOP. An orbital concept requires a space-system cost framework, not CAS. Disqualified for quantitative use.
 
-6. **Lunar He-3 resource literature** — for supply chain assessment, search for Harrison Schmitt and/or University of Wisconsin fusion He-3 program publications (~2000-2010) to bound alternative He-3 supply scenarios. — `not-yet-sourced, unverified — confirm existence before searching`
+- **A simplified economic model for inertial fusion** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): IFE-specific Monte Carlo LCOE model for pulsed driver-target concepts. Different confinement family, different physics regime, different cost structure. Disqualified.
 
-7. **Space nuclear power regulatory literature** — for orbital nuclear systems, search for NASA/DOE space nuclear power safety standards and prior space nuclear mission costs (e.g., RTG, Kilopower) as lower-bound cost analogs. OSTI and NASA technical reports. — `not-yet-sourced`
+- **Overview of the Helios Design** (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`): Planar-coil stellarator, D-T, terrestrial. Different confinement, different fuel, no orbital infrastructure. Disqualified.
 
----
-
-## Summary
+- **Economic studies for heavy-ion-fusion**, **Energy from Inertial Fusion**, **Accelerators for IFE**, **AMPS high-yield IFE**, **Commercialization of laser fusion energy**: All IFE-specific, terrestrial, pulsed driver technologies. Disqualified.
 
-The available data is insufficient to support a standard D1+ LCOE analysis for the Orbital Levitated Dipole. All five analysis sections face blocking gaps rooted in the same fundamental problem: Zephyr Fusion has made no technical disclosures, and the orbital D-He3 concept is sufficiently novel that no published plant study exists anywhere in the literature. The most informative source in the collection (OpenStar arXiv 2602.20564) is an analog for the dipole confinement architecture but addresses D-T fuel, terrestrial deployment, and conventional thermal power conversion — three of the four defining characteristics of Zephyr's concept are opposite.
+- **An Assessment of the Economics of Future Electric Power Generation Options** (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): Historical terrestrial LCOE benchmarking against coal, nuclear, renewables. The orbital concept targets space power markets, not terrestrial grid competition. Benchmarking framework inapplicable. Disqualified.
 
-What a D1+ analysis can do with the current data:
-- Characterize the physics basis and why the orbital approach is hypothetically attractive
-- Document what is unknown and why
-- Bound D-He3 fusion requirements (triple product, He-3 supply chain impossibility at current production rates)
-- Note the NASASpaceFlight critique as indicative of fundamental engineering gaps (power conversion, heat removal, neutron management)
-- Use OpenStar's terrestrial dipole cost methodology as a partial structural analog (HTS coil, REBCO tape, magnet engineering) with explicit caveats
+- **NSS WPT workshop** (`iter-02/sources/nss-wp-content-uploads-2017-07-space-solar-power-workshop.md`) and **arxiv 2401.15267** (`iter-02/sources/arxiv-2401-15267.md`): Read. These cover WPT transmission from orbit (not fusion-to-electricity conversion). The arxiv paper demonstrates LEO WPT array functionality but does not address the upstream conversion of fusion products to RF power. They confirm WPT infrastructure feasibility but do not resolve the energy conversion gap. Integrated as WPT context; do not downgrade any blocking gap.
 
-**Recommendation**: Proceed to a full analysis structured as a "concept assessment" rather than a quantitative LCOE model. Flag explicitly that no LCOE computation is possible from first principles without Zephyr disclosures, and use the $1B/MW ISS solar baseline and Zephyr's own <$30M claim as the only available cost reference points (marking both as highly uncertain). Acquiring the Hasegawa 1987/1990, LDX Boxer (2010), and ARIES-III D-He3 sources before writing would meaningfully improve coverage of the physics basis and direct energy conversion context even if the cost gap cannot be closed.
+- **NTRS NASA comparison SPS vs. CSP** (`iter-02/sources/ntrs-api-citations-20140003205-downloads-20140003205.md`): Read. SPS-to-CSP efficiency comparison for 1 GW systems. Context on space power economics but no fusion content. Provides the observation that SPS total infrastructure area remains large regardless of solar cell efficiency — useful framing for orbital power limits but no applicability to fusion LCOE. Disqualified for quantitative use.
 
 ---
 
+## Summary
+
+Proceed to qualitative narrative analysis only. The concept can be described in terms of (1) the physics motivation for orbital dipole confinement advantage over terrestrial alternatives, (2) engineering challenges unique to space deployment — HTS cryogenics in LEO, direct conversion, power beaming chain, (3) He-3 supply as a potentially civilization-scale constraint with no current solution, and (4) positioning relative to terrestrial levitated dipole competitors (OpenStar, Deutelio) and other orbital power concepts (space solar). Do not attempt quantitative LCOE modeling without Zephyr or peer-reviewed disclosure of: plasma performance targets, energy conversion mechanism, and an architecture-level plant design. Sourcing Teller 1992, Hasegawa 1987 PPPL-2627, ARIES-III, LDX experimental papers, and Kesner 2003 would substantially enrich the qualitative analysis but would not unlock a quantitative LCOE unless a reactor design study also becomes available.
+
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Insufficient Data"
-blocking_count: 10
-important_count: 7
-counting_method: "deduplicated across all sections; counted distinct blocking gaps: (1) no company technical disclosures, (2) energy conversion pathway uncharacterized, (3) plasma-orbit stability unknown, (4) direct energy conversion TRL 1-2, (5) no plant electrical output target, (6) no capital cost estimate, (7) He-3 fuel cost at scale unknown, (8) capacity factor/availability framework inapplicable, (9) power beaming MW-scale losses unknown, (10) He-3 production at reactor scale infeasible with current supply. Important gaps: heating method unconfirmed, compact RF for orbit not sourced, orbital HTS thermal management not sourced, D-He3 triple product requirement not compiled, REBCO radiation hardness in LEO not sourced, Hasegawa 1987/1990 not extracted, LDX/RT-1 experimental papers not extracted."
+blocking_count: 7
+important_count: 8
+counting_method: "all_sections_deduplicated — blocking: (1) no plasma performance targets/Q, (2) energy conversion mechanism undefined, (3) no plant-level design/capital cost, (4) He-3 supply at fusion scale nonexistent, (5) capacity factor absent, (6) O&M cost model absent, (7) space-hardened HTS cryogenic system undesigned. Important: heating method undisclosed, D-He3 orbital plasma physics, He-3 post-2010 pricing, direct conversion TRL, launch cost not integrated, power beaming infrastructure cost, plant lifetime in LEO, He-3 on-orbit fuel handling."
 section_coverage:
   availability_of_data:       "Poor"
   system_function:            "Poor"
```
