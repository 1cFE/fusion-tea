# Diff: 19-orbital-levitated-dipole

**Generated:** 2026-05-22T10:35:33-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 10 | 10 | 0 |
| important_count  | 3 | 7 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
(none)
```

## Blocking-tier lines (baseline)

```
36:- Company technical disclosure (fuel, heating, conversion) — `proprietary` — **blocking** (forces all key parameters to be inferred)
37:- No orbital fusion power plant study of any kind exists — `truly-unknown` — **blocking** (no cost methodology precedent)
59:- No applicable LCOE framework for orbital power delivery — `truly-unknown` — **blocking** (requires methodological invention before the model can be scoped)
61:- Power beaming losses and infrastructure cost — `truly-unknown` for this application — **blocking** (determines whether the concept can ever produce cheap electricity at the customer)
84:- Direct energy conversion technology at reactor scale — `truly-unknown` for orbital application — **blocking**
106:- He-3 supply path to orbital platform — `truly-unknown` — **blocking** (if the fuel can't be delivered to orbit at scale, the concept can't operate)
135:| Capital cost breakdown (magnet, launch, direct conversion, power beaming) | proprietary + truly-unknown | blocking | $30M claim likely magnet-only; launch + power beaming system dominate |
136:| Falcon 9 launch cost (rideshare) | not-yet-sourced | blocking | SpaceX pricing; $2-5k/kg to LEO is public — mass of system needed |
137:| System mass (coil + support structure + heating + power electronics) | proprietary | blocking | Determines launch cost, which may dominate |
138:| Target fusion power (MW) | proprietary | blocking | "MW-class" is all that's stated |
139:| Target Q (fusion gain) | proprietary | blocking | Required to compute recirculating power and net output |
140:| Heating power requirement | derivable (once Q and fusion power known) | blocking | ECRH at 30-40% efficiency is a major recirculating power cost |
141:| Direct conversion efficiency (orbital separatrix) | truly-unknown | blocking | Never been built; 60-80% claimed in theory |
142:| Power beaming efficiency (fusion → delivered electricity) | truly-unknown | blocking | Each step (conversion → beaming → receipt) has large loss; likely 20-40% end-to-end |
143:| Power beaming infrastructure cost (ground/orbit receiver) | truly-unknown | blocking | May dominate system LCOE |
145:| Operating cost (fuel resupply, orbital maintenance) | truly-unknown | blocking | On-orbit maintenance is either impossible or extremely expensive |
```

## Blocking-tier lines (new)

```
32:- No company technical disclosures exist — `proprietary` — **blocking**: can only make physics inferences, no engineering parameters
56:- Energy conversion pathway (direct conversion + power beaming) is completely uncharacterized — `truly-unknown` at engineering level, `not-yet-sourced` for Hasegawa-type direct conversion literature — **blocking**: determines what fraction of fusion energy becomes deliverable power
57:- Plasma-orbit stability and spacecraft integration — `truly-unknown` — **blocking**: no analog exists for an orbital fusion plasma device
79:- Direct energy conversion at separatrix: TRL 1-2 — `truly-unknown` at engineering level — **blocking**
100:- He-3 fuel quantity and cost per unit energy: No fusion-scale production or cost estimate exists — `truly-unknown` for fusion application, though CRS report provides useful supply context — **blocking** for any cost model
101:- He-3 production at fusion scale: Current global supply completely inadequate for a power plant; alternative production (tritium decay, lunar mining) is speculative — `not-yet-sourced` (lunar He-3 literature exists but is unverified for this analysis) — **blocking**
129:| Plant electrical output (MWe) | proprietary | blocking | No target specified; "megawatt-class" only |
130:| Fusion power (MWth) | proprietary | blocking | No target; coil size/field not disclosed |
131:| Q (fusion gain) | proprietary | blocking | Not disclosed; D-He3 requires Q >> D-T |
132:| Energy conversion efficiency (direct + beaming) | truly-unknown | blocking | No demonstrated direct converter for dipole; beaming efficiency at MW scale uncharacterized |
133:| Capital cost breakdown by subsystem | proprietary | blocking | No cost estimate at any level |
134:| Launch cost (mass to LEO) | derivable | blocking | Requires coil mass + full system manifest; coil mass not disclosed |
135:| Operating cost (orbital maintenance, station-keeping) | truly-unknown | blocking | No comparable orbital fusion system exists |
136:| He-3 fuel cost per MWh | derivable | blocking | Requires fusion parameters + He-3 price at scale; neither known |
137:| Capacity factor / availability | derivable | blocking | Requires operational cadence; orbital logistics completely uncharacterized |
138:| Power beaming losses | not-yet-sourced | blocking | MW-class space-to-orbit power beaming not demonstrated; solar analogs give rough bounds |
141:| He-3 production at reactor scale | truly-unknown | blocking | Current global supply inadequate by orders of magnitude; lunar/accelerator sources speculative |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/19-orbital-levitated-dipole.md	2026-05-22 09:21:13.862147386 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/gap_report.md	2026-05-22 10:35:33.193282800 -0700
@@ -1,13 +1,10 @@
-Now I have everything I need. Let me write the gap assessment.
-
----
+I now have sufficient information to write the gap assessment. Let me compose it.
 
 # Gap Assessment: Orbital Levitated Dipole (D-He3)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
-
-**Summary**: Zephyr Fusion is a pre-prototype, 2-person startup (founded 2025, YC F25) that has disclosed almost nothing beyond the existence of their concept. The academic heritage from LDX, Hasegawa 1987, and a 2026 D-T dipole reactor study (arxiv 2602.20564) provides a credible physics foundation, but Zephyr itself has not confirmed fuel type, heating method, energy conversion pathway, performance targets, or any cost-relevant engineering detail. Critically, the concept is an *orbital* power plant — a fundamentally different techno-economic system than any terrestrial fusion reactor — with no established LCOE methodology, no cost analogues, and launch cost dominating the capital structure in ways the standard fusion LCOE framework does not capture. A D1+ analysis can be written but must be heavily inference-based and clearly flagged as such.
+**Summary**: Zephyr Fusion (YC F25, founded 2025) has disclosed essentially nothing beyond a marketing launch page. The concept's fundamental novelty — orbital deployment, D-He3 fuel, direct energy conversion, power beaming — places every LCOE-relevant parameter either unknown or outside the applicable range of conventional fusion plant methodology. The one substantive technical source found during Phase 1a research (arXiv 2602.20564, OpenStar DT levitated dipole) addresses a terrestrial D-T dipole with a blanket and thermal cycle, which is architecturally distinct from Zephyr's concept in every dimension that matters for cost modeling. A D1+ analysis can be written, but it will read as a structured inventory of unknowns with physics-based bounds rather than a quantitative LCOE estimate.
 
 ---
 
@@ -17,176 +14,178 @@
 **Coverage**: Poor
 
 **Available**:
-- YC launch page (`yc-launch-page.md`): confinement principle, HTS magnet scale, Falcon 9 deployability, megawatt-class power target, $30M claimed cost for magnetized volume exceeding ITER, founder credentials
-- NASASpaceFlight forum (`nasaspaceflight-forum-discussion.md`): community skepticism inventory — identifies every undisclosed element (energy conversion, shielding, power beaming path, tritium breeding)
-- LDX/RT-1 heritage (`levitated-dipole-technical-background.md`): demonstrated physics of levitated dipole confinement, heating methods used in experiments, τₑ ~ R² scaling, high-beta properties
-- arxiv 2602.20564 (OpenStar D-T dipole reactor study, via `dipole-reactor-heating-energy-conversion.md`): the only published modern dipole reactor design — 667 MW fusion power, 208 MW net electric, ICRH baseline, sacrificial shield lifetime (~1 year)
-- Hasegawa & Chen 1987 (PPPL-2627, via `dipole-reactor-heating-energy-conversion.md`): original D-He3 dipole reactor concept with direct energy conversion at separatrix, space propulsion parameters (1 kW/kg specific power)
-- ARIES-III D-He3 tokamak study (referenced via `dipole-reactor-heating-energy-conversion.md`): 47% net efficiency hybrid rectenna + thermal conversion, synchrotron radiation recovery concept
-- Comprehensive web survey (`zephyr-fusion-web-sources-2026.md`): exhaustive confirmation that no ARPA-E/DOE funding, no patents, no conference papers, no additional technical disclosures exist as of March 2026
+- Company description at marketing level: YC launch page (`iter-01/sources/yc-launch-page.md`) — one paragraph on physics concept, no technical parameters
+- Peripheral press coverage: DCD article (`iter-02/sources/zephyr-fusion-web-sources-2026.md`) — paraphrases YC post, adds nothing
+- Community skepticism: NASASpaceFlight forum (`iter-01/sources/nasaspaceflight-forum-discussion.md`) — highlights absence of power conversion, heat removal, and blanket
+- Concept heritage: Wikipedia levitated dipole article (`iter-01/sources/levitated-dipole-technical-background.md`) — LDX, RT-1 experiments, Hasegawa 1987 proposal; no quantitative fusion parameters
+- Terrestrial dipole analog: OpenStar arXiv 2602.20564 (`iter-02/sources/dipole-reactor-heating-energy-conversion.md`) — detailed D-T dipole plant study (208 MWe), but fundamentally different fuel, location, and power delivery
+- He-3 supply context: CRS Report R41419 (`iter-02/sources/everycrsreport-reports-r41419.md`) — comprehensive analysis of He-3 shortage; global supply ~8,000 L/yr from weapons program
 
 **Missing**:
-- Any primary Zephyr technical disclosure beyond the YC launch page
-- Confirmation of fuel type, heating method, or energy conversion approach from the company
-- Any published plant study for a D-He3 *orbital* dipole
-- Performance targets (Q, ion temperature, plasma density, power output)
-- Timeline and milestones
+- Any Zephyr technical paper, patent, or conference presentation
+- Hasegawa & Chen (1987) D-He3 dipole proposal (cited but not extracted)
+- LDX and RT-1 experimental papers with plasma parameter data
+- Any prior D-He3 dipole reactor study (ARIES-III covers D-He3 in a tokamak, not dipole)
+- Direct conversion technology literature (Hasegawa-type separatrix direct converter, not extracted)
 
 **Gaps**:
-- Company technical disclosure (fuel, heating, conversion) — `proprietary` — **blocking** (forces all key parameters to be inferred)
-- No orbital fusion power plant study of any kind exists — `truly-unknown` — **blocking** (no cost methodology precedent)
-- No Zephyr patents or conference presentations — `proprietary` — **important** (no mid-level technical detail available)
+- No company technical disclosures exist — `proprietary` — **blocking**: can only make physics inferences, no engineering parameters
+- Hasegawa 1987 D-He3 dipole paper not extracted — `not-yet-sourced` — **important**: foundational document underpinning the concept
+- LDX/RT-1 experimental results not extracted — `not-yet-sourced` — **important**: only experimental data on dipole plasma performance
+- ARIES-III D-He3 study not extracted — `not-yet-sourced` — **important**: only prior cost study for D-He3 fusion (tokamak geometry, but relevant for fuel cycle and direct conversion costs)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial (physics understood; engineering and economics not)
+**Coverage**: Poor
 
 **Available**:
-- The levitated dipole confinement physics is well-documented in LDX/RT-1 experiments and the arxiv 2602.20564 reactor study. The τₑ ~ R² scaling, high-beta advantage, and disruption-free steady-state operation are all experimentally grounded.
-- The D-He3 fuel cycle rationale — aneutronic primary reaction, 85% energy in charged particles, no blanket requirement — is clearly established in Hasegawa 1987 and consistent with orbital operation.
-- Direct charged particle conversion at the separatrix is physically well-motivated and the geometry is cited as "particularly suitable" for D-He3 in the academic literature.
-- The core insight (space vacuum eliminates vacuum vessel as energy loss channel) is documented and acknowledged by the community as physically valid.
+- Physics rationale for orbital advantage: YC launch page and OpenStar paper establish that (a) dipole confinement benefits from large plasma volume, (b) space vacuum eliminates vacuum vessel as loss mechanism, (c) τ_e ~ R² scaling applies. The physics logic is documented.
+- Qualitative power conversion pathway: Dossier inference + Hasegawa 1987 heritage that D-He3 dipole at separatrix enables direct charged-particle deceleration. This is physics-consistent but unconfirmed by Zephyr.
+- Heating options: OpenStar paper (`iter-02/sources/dipole-reactor-heating-energy-conversion.md`, Section 2.2.7) systematically evaluates ECRH (30-40% efficiency), ICRH (~70% efficiency), and NBI for terrestrial dipoles; these constraints apply qualitatively to the orbital case.
+- Terrestrial D-T dipole power balance equations: OpenStar paper Table 2 provides η_th = 0.4, η_aux = 0.7, η_cryo = 0.0125, duty cycle ~90%, Q_sci = 15 targets. These are analogs for some subsystems, but inapplicable to the D-He3 direct-conversion orbital scenario.
 
 **Missing**:
-- This concept doesn't fit the standard LCOE framework at all. The "plant" is an orbiting spacecraft with no grid connection — LCOE in $/kWh is only meaningful if power beaming losses and beaming infrastructure costs are included. No methodology exists for this.
-- D-He3 requires ~60 keV ion temperatures (vs. ~20 keV for D-T), implying a challenging heating power requirement. Without target plasma parameters, heating power cannot be estimated.
-- The relationship between orbital altitude, drag makeup, plasma confinement geometry, and power output is completely uncharacterized.
-- No description of how synchrotron radiation is managed (tolerable power load? recovered? radiated?)
-- The power beaming pathway (fusion energy → direct conversion → microwave/laser → ground/customer) has multiple efficiency stages, each unspecified.
+- Power delivery mechanism: "power beaming partners" is stated in dossier but mechanism is unspecified. The arxiv 2401.15267 paper (`iter-02/sources/arxiv-2401-15267.md`) covers lightweight coherent RF arrays for space-to-ground wireless power transfer (solar power context), providing some efficiency reference (~end-to-end ~12-20% for SPS), but this is for solar, not fusion-scale MW power beaming.
+- Direct energy conversion at separatrix: No source in the collection addresses the engineering implementation of charged-particle direct conversion for a dipole. The concept is physically motivated (Hasegawa 1987) but no engineering design or efficiency estimate exists in any extracted source.
+- Station-keeping and orbital mechanics: What maintains the coil in a stable orbit while the surrounding plasma extends 10-50 m? No source addresses this.
+- Plasma-spacecraft interaction in LEO: No source addresses particle/radiation environment effects on the HTS coil or plasma boundary.
+- D-He3 physics scaling to fusion-relevant conditions: No levitated dipole has ever operated near D-He3 fusion conditions (requires ~60 keV ion temperatures; LDX operated at ~100 eV).
 
 **Gaps**:
-- No applicable LCOE framework for orbital power delivery — `truly-unknown` — **blocking** (requires methodological invention before the model can be scoped)
-- D-He3 plasma ignition/sustainment conditions not characterized for dipole geometry at orbital scale — `not-yet-sourced` (search: Hasegawa 1987 PPPL-2627 full text, arxiv dipole D-He3 reactor studies) — **important**
-- Power beaming losses and infrastructure cost — `truly-unknown` for this application — **blocking** (determines whether the concept can ever produce cheap electricity at the customer)
-- Heating power requirement and recirculating power fraction — `derivable` from D-He3 reactivity data + target plasma parameters, but no targets disclosed — **important**
+- Energy conversion pathway (direct conversion + power beaming) is completely uncharacterized — `truly-unknown` at engineering level, `not-yet-sourced` for Hasegawa-type direct conversion literature — **blocking**: determines what fraction of fusion energy becomes deliverable power
+- Plasma-orbit stability and spacecraft integration — `truly-unknown` — **blocking**: no analog exists for an orbital fusion plasma device
+- D-He3 confinement scaling from LDX to reactor-scale — `truly-unknown` — **important**: no data exists for this extrapolation, orders of magnitude in triple product separate LDX from fusion conditions
+- D-He3 vs D-T reactivity disadvantage: D-He3 requires ~10× higher triple product than D-T; LDX never approached this. The OpenStar paper (DT focus) explicitly notes that prior advanced-fuel dipole designs were infeasible due to triple-product requirements — `derivable` from literature but not yet compiled — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial (heritage physics demonstrated; most engineering subsystems at TRL 1-2)
+**Coverage**: Partial
 
 **Available**:
-- **Dipole confinement physics**: TRL 4-5. LDX (MIT/Columbia, 2004-2012) and RT-1 (U. Tokyo) demonstrated stable levitated dipole confinement with ECRH heating, density/pressure profiles consistent with theory, and high-beta operation.
-- **HTS magnet technology**: TRL 6-7 for terrestrial magnets. REBCO tape technology is commercially available; tokamak projects (SPARC, Commonwealth Fusion) have demonstrated high-field HTS magnets at meter scale. Space qualification of HTS magnets is lower (TRL 3-4).
-- **ECRH heating (ground-based)**: TRL 7-8 for terrestrial application. Demonstrated on LDX. Gyrotrons at industrial scale exist.
-- **NBI**: TRL 8-9 for terrestrial application. Mature technology.
-
-**Missing** (no data available for any of these):
-- **Orbital HTS magnet deployment**: No demonstration of superconducting magnets sustained in LEO. Passive cooling in LEO thermal environment is uncharacterized for this application.
-- **Direct energy conversion at dipole separatrix**: TRL 1-2. Described theoretically in Hasegawa 1987 and ARIES-III but never built or tested at any scale.
-- **Microwave/laser power beaming from orbit**: Contested TRL (various demos exist for small-scale terrestrial and near-orbit). MW-class continuous power beaming is undemonstrated.
-- **Heating systems in space vacuum**: ECRH/ICRH/NBI in space environment — no heritage. RF systems in vacuum would need different engineering.
-- **Plasma fueling/refueling at orbital platform**: Unaddressed.
-- **Cryogenic maintenance in LEO**: Sustained HTS magnet operation over years requires thermal management strategy not described.
+- HTS coil technology: OpenStar paper establishes REBCO-based dipole coil design, CICC architecture, 23 T peak field, structural over-band design. This is TRL 4-5 for terrestrial operation; orbital deployment would downgrade to TRL 2-3.
+- Coil levitation physics: LDX (TRL 5-6 for demonstration levitation), RT-1 (TRL 5-6 for HTS levitation). Both are terrestrial, small-scale.
+- Space launch of HTS systems: No dedicated heritage, but Falcon 9 rideshare for meter-scale payloads is TRL 9. The challenge is operating superconducting coils in LEO thermal/radiation environment.
+- Power beaming (microwave/laser): arxiv 2401.15267 and NSS SPS workshop (`iter-02/sources/nss-wp-content-uploads-2017-07-space-solar-power-workshop.md`) provide context for WPT arrays. TRL 4-6 for small-scale space demonstrations.
+
+**Missing**:
+- Compact RF heating (ECRH or ICRH) for orbital deployment: No space-compatible heating system design exists in any source
+- Direct energy converter for D-He3 charged particles at separatrix: Only theoretical proposal (Hasegawa 1987); no experimental or engineering demonstration
+- Cryogenic coil management in LEO thermal cycling (beta angle, eclipse/sunlight cycling): Not addressed in any source
+- Plasma diagnostics and control for orbital device: Not addressed
 
 **Gaps**:
-- Direct energy conversion technology at reactor scale — `truly-unknown` for orbital application — **blocking**
-- Space-qualified superconducting magnet (sustained multi-year operation) — `not-yet-sourced` (search: NASA/ESA superconducting magnet space qualification efforts, CERN for space, etc.) — **important**
-- Heating subsystem in space environment — `truly-unknown` — **important**
-- Fuel delivery / refueling logistics — `truly-unknown` — **important**
+- Direct energy conversion at separatrix: TRL 1-2 — `truly-unknown` at engineering level — **blocking**
+- Compact RF heating system for space: TRL 2-3 — `not-yet-sourced` (defense/directed-energy literature may have compact gyrotron designs) — **important**
+- Orbital HTS coil thermal management: TRL 3-4 — `not-yet-sourced` — **important**
+- No TRL documentation exists for any Zephyr-specific component — `proprietary` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial (He-3 supply well-documented elsewhere; orbital supply chain is unique)
+**Coverage**: Partial (He-3 supply well-documented; others minimal)
 
 **Available**:
-- **HTS tape (REBCO)**: Supply chain is constrained but exists. The broader fusion industry (SPARC, many startups) is building this supply chain. Meter-scale coil for a single satellite is a small quantity relative to terrestrial reactor magnets.
-- **He-3 supply**: The D-He3 fuel choice has a well-documented supply gap in the literature. Terrestrial He-3 comes primarily from tritium decay (~15 kg/year from US/Russia weapons programs). Lunar He-3 mining remains speculative. This supply constraint is a fundamental challenge for any D-He3 concept, not unique to Zephyr.
-- **D (deuterium)**: Abundant, electrochemically separable from seawater. Not a supply concern.
+- He-3 supply chain: CRS Report R41419 (`iter-02/sources/everycrsreport-reports-r41419.md`) is comprehensive. Key facts: global supply ~8,000 L/yr from tritium decay in weapons programs; historical price $40-85/L (pre-shortage), spiked significantly; shortage documented as of 2009. Production tied to nuclear weapons maintenance, not adjustable to meet fusion demand.
+- REBCO tape: OpenStar paper establishes ~4,320 km of REBCO tape required for their 208 MWe terrestrial reactor. Current REBCO supply chain (SuperOx, Faraday Factory, SuNAM) is growing but not at scale for fusion. For orbital deployment, radiation hardness of REBCO in LEO environment is unverified.
+- Deuterium: Abundant, not a supply constraint.
 
 **Missing**:
-- No estimate of He-3 consumption rate for a MW-class D-He3 dipole (requires plasma parameters)
-- No consideration of D-He3 fuel delivery logistics to orbital platform
-- Orbital logistics supply chain (launch cadence for fuel resupply) — novel problem with no precedent
-- Space-rated power electronics for direct conversion at MW scale — no supply chain exists
+- He-3 quantity required for D-He3 orbital dipole: No published estimate for the Zephyr concept or any D-He3 dipole reactor exists in the sources. The D-He3 fusion reaction consumes He-3 at a rate dependent on fusion power and fuel cycle efficiency — not calculable without plasma parameters.
+- He-3 price at scale: CRS report cites historical prices for detector-grade quantities; fusion-scale demand (orders of magnitude larger) would require new production pathways at unknown cost
+- REBCO radiation hardness in LEO: Not addressed in any source; DD neutrons from D-He3 side reactions would continuously irradiate the coil
 
 **Gaps**:
-- He-3 supply path to orbital platform — `truly-unknown` — **blocking** (if the fuel can't be delivered to orbit at scale, the concept can't operate)
-- He-3 fuel consumption rate — `derivable` from D-He3 reactivity + plasma parameters once targets are known — **important**
-- Space-rated MW-class direct conversion hardware — `truly-unknown` — **important**
-- REBCO tape quantity for meter-scale coil — `derivable` (small relative to terrestrial projects, manageable supply risk) — **nice-to-have**
+- He-3 fuel quantity and cost per unit energy: No fusion-scale production or cost estimate exists — `truly-unknown` for fusion application, though CRS report provides useful supply context — **blocking** for any cost model
+- He-3 production at fusion scale: Current global supply completely inadequate for a power plant; alternative production (tritium decay, lunar mining) is speculative — `not-yet-sourced` (lunar He-3 literature exists but is unverified for this analysis) — **blocking**
+- REBCO radiation tolerance in LEO: `not-yet-sourced` — **important**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor — almost no LCOE-relevant parameters available; standard LCOE framework may not apply
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Magnetized plasma volume | ">ITER" (>840 m³ implied) | YC launch page | medium |
-| Capital cost (magnet/coil only) | <$30M | YC launch page | low (unverified claim) |
-| Net electrical output | "MW-class" | YC launch page | low (no number given) |
-| Confinement scaling | τₑ ~ R² | LDX heritage | high (physics) |
-| Launch vehicle | Falcon 9 (rideshare) | YC launch page | medium |
-| D-He3 charged particle fraction | ~85% | Hasegawa 1987 heritage | high (physics) |
-| ARIES-III D-He3 net efficiency (tokamak analogue) | 47% | ARIES-III via `dipole-reactor-heating-energy-conversion.md` | medium (different geometry) |
-| D-T dipole reactor analogue: net electric | 208 MW from 667 MW fusion | arxiv 2602.20564 | medium (different fuel) |
-| D-T dipole analogue: sacrificial shield replacement | ~1 year cycle | arxiv 2602.20564 | medium (different fuel/geometry) |
-| Hasegawa 1987 space parameter | 1 kW/kg specific power | `levitated-dipole-technical-background.md` | low (1987 design estimate) |
+| Target power output | MW-class (orbital) | YC launch page | low |
+| Confinement concept | Dipole, τ_e ~ R² | YC + LDX Nature Physics 2010 (cited) | medium |
+| Magnet type | REBCO, meter-scale, Falcon 9-deployable | YC launch page | high |
+| Steady-state operation | Yes | Dossier inference | high |
+| Heating efficiency (ICRH analog) | ~70% wall-plug | OpenStar paper (DT terrestrial) | low (D-T analog only) |
+| Heating efficiency (ECRH analog) | 30-40% wall-plug | OpenStar paper (DT terrestrial) | low (analog) |
+| D-He3 charged particle fraction | ~85% | Physics — standard D-He3 reaction | medium |
+| DD neutron energy fraction | ~10% | Physics — standard D-He3 side reactions | medium |
+| He-3 current global supply | ~8,000 L/yr | CRS R41419 | high |
+| He-3 historical price | $40-85/L (pre-shortage) | CRS R41419 | high |
+| Power beaming end-to-end efficiency (SPS analog) | ~12-20% | arxiv 2401.15267 + NTRS SPS comparison | low (solar, not fusion) |
+| Comparable ISS solar cost | ~$1B/MW installed | YC launch page (Zephyr's own claim) | medium |
+| Zephyr claimed total cost | <$30M | YC launch page | very low (marketing) |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost breakdown (magnet, launch, direct conversion, power beaming) | proprietary + truly-unknown | blocking | $30M claim likely magnet-only; launch + power beaming system dominate |
-| Falcon 9 launch cost (rideshare) | not-yet-sourced | blocking | SpaceX pricing; $2-5k/kg to LEO is public — mass of system needed |
-| System mass (coil + support structure + heating + power electronics) | proprietary | blocking | Determines launch cost, which may dominate |
-| Target fusion power (MW) | proprietary | blocking | "MW-class" is all that's stated |
-| Target Q (fusion gain) | proprietary | blocking | Required to compute recirculating power and net output |
-| Heating power requirement | derivable (once Q and fusion power known) | blocking | ECRH at 30-40% efficiency is a major recirculating power cost |
-| Direct conversion efficiency (orbital separatrix) | truly-unknown | blocking | Never been built; 60-80% claimed in theory |
-| Power beaming efficiency (fusion → delivered electricity) | truly-unknown | blocking | Each step (conversion → beaming → receipt) has large loss; likely 20-40% end-to-end |
-| Power beaming infrastructure cost (ground/orbit receiver) | truly-unknown | blocking | May dominate system LCOE |
-| Capacity factor / on-orbit lifetime | proprietary | important | No satellite lifetime assumptions stated; degradation of HTS coil in LEO radiation environment unknown |
-| Operating cost (fuel resupply, orbital maintenance) | truly-unknown | blocking | On-orbit maintenance is either impossible or extremely expensive |
-| He-3 fuel consumption rate | derivable | important | Requires plasma parameters |
-| Replacement schedule (if any components fail) | truly-unknown | important | On-orbit replacement logistics are unique problem |
+| Plant electrical output (MWe) | proprietary | blocking | No target specified; "megawatt-class" only |
+| Fusion power (MWth) | proprietary | blocking | No target; coil size/field not disclosed |
+| Q (fusion gain) | proprietary | blocking | Not disclosed; D-He3 requires Q >> D-T |
+| Energy conversion efficiency (direct + beaming) | truly-unknown | blocking | No demonstrated direct converter for dipole; beaming efficiency at MW scale uncharacterized |
+| Capital cost breakdown by subsystem | proprietary | blocking | No cost estimate at any level |
+| Launch cost (mass to LEO) | derivable | blocking | Requires coil mass + full system manifest; coil mass not disclosed |
+| Operating cost (orbital maintenance, station-keeping) | truly-unknown | blocking | No comparable orbital fusion system exists |
+| He-3 fuel cost per MWh | derivable | blocking | Requires fusion parameters + He-3 price at scale; neither known |
+| Capacity factor / availability | derivable | blocking | Requires operational cadence; orbital logistics completely uncharacterized |
+| Power beaming losses | not-yet-sourced | blocking | MW-class space-to-orbit power beaming not demonstrated; solar analogs give rough bounds |
+| D-He3 triple product requirement | derivable | important | ~60 keV ion temperature needed; ~10× harder than D-T |
+| Cryogenic power load in orbit | derivable | important | Requires thermal environment model + coil mass |
+| He-3 production at reactor scale | truly-unknown | blocking | Current global supply inadequate by orders of magnitude; lunar/accelerator sources speculative |
 
 ---
 
 ## Source Recommendations
 
-1. **Hasegawa & Chen 1987 (PPPL-2627) full text** — cited in dossier, may contain quantitative D-He3 dipole reactor parameters (plasma density, temperature, power, direct conversion design). Priority: high. *Verify availability at INIS/IAEA: https://inis.iaea.org/records/05wfd-4pb29 — confirm before citing.*
+1. **Hasegawa & Chen (1990), "A D-3He fusion reactor based on a dipole magnetic field"** — cited in OpenStar paper as Hasegawa et al. 1990; also Hasegawa (1987) original. These are foundational for D-He3 dipole physics and direct energy conversion design. Search PPPL report PPPL-2627 and journal *Comments on Plasma Physics and Controlled Fusion* 11(3):147-151. — `unverified — confirm existence before searching`
+
+2. **LDX experimental papers** — Boxer et al. (2010), Nature Physics, "Turbulent inward pinch of plasma confined by a levitated dipole magnet" — the primary experimental validation of dipole confinement. Directly cited by Zephyr. Available on Nature Physics. — `not-yet-sourced`
 
-2. **ARIES-III D-He3 fusion reactor study** — cited in dossier (`fti.neep.wisc.edu/pdf/fdm815.pdf`). Full study likely contains capital cost breakdown, direct conversion efficiency, LCOE estimate. The most relevant analogue for D-He3 energy conversion economics, even though it's a tokamak. Priority: high. *Link appears in source documents — confirm file exists before using.*
+3. **Kesner et al. (2003), "Helium catalysed D–D fusion in a levitated dipole"** — cited in OpenStar paper; directly addresses DD → He3 → D-He3 fuel cycle in levitated dipole context. Relevant for tritium breeding and advanced fuel cycle. — `not-yet-sourced`
 
-3. **arxiv 2602.20564 (OpenStar D-T dipole reactor, 2026)** — already cited, partially extracted. Contains cost estimates for D-T terrestrial dipole. Can be used as lower bound / structural analogue for magnet and plasma-facing component costs, with heavy caveats. Priority: medium. *Exists — referenced in multiple source files.*
+4. **ARIES-III D-He3 tokamak design study** — covers direct energy conversion from charged D-He3 products in a tokamak, relevant as the only full cost study for D-He3 fusion including direct converter design. Search OSTI for "ARIES-III" and "D-He3 direct energy conversion." — `not-yet-sourced, unverified — confirm existence before searching`
 
-4. **MIT LDX program publications** — `https://www-internal.psfc.mit.edu/ldx/pubs/` cited in sources. May contain performance scaling analyses useful for extrapolating to reactor scale. Search for LDX design reports and FESAC presentations. Priority: medium. *Internal MIT URL — may not be publicly accessible; unverified — confirm existence before searching.*
+5. **Wallace et al. (2025), "Ion Cyclotron Heating in a Levitated Dipole Fusion Reactor"** — cited in OpenStar paper; directly addresses ICRH in dipole geometry. Most current heating study for this concept. — `not-yet-sourced`
 
-5. **Space-based power systems LCOE literature** — No specific paper cited. Search: "space-based solar power LCOE", "SBSP techno-economic analysis", "orbital power plant economics". These are the closest cost-methodology analogues for Zephyr's business model (orbital source + power beaming to ground). This literature provides the only credible framework for estimating launch-cost-dominated capital structure. Priority: high for methodology. *Unverified — confirm existence before searching.*
+6. **Lunar He-3 resource literature** — for supply chain assessment, search for Harrison Schmitt and/or University of Wisconsin fusion He-3 program publications (~2000-2010) to bound alternative He-3 supply scenarios. — `not-yet-sourced, unverified — confirm existence before searching`
 
-6. **Zephyr Fusion new disclosures** — Monitor for: conference papers (FPA, IAEA FEC, APS-DPP), DOE/ARPA-E grant announcements, patent filings (USPTO search: "levitated dipole" + "orbital" + "fusion"), investor updates. As of March 2026, none exist. *No specific paper to cite — ongoing monitoring recommended.*
+7. **Space nuclear power regulatory literature** — for orbital nuclear systems, search for NASA/DOE space nuclear power safety standards and prior space nuclear mission costs (e.g., RTG, Kilopower) as lower-bound cost analogs. OSTI and NASA technical reports. — `not-yet-sourced`
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with heavy caveats — but restructure the LCOE model scope first.**
+The available data is insufficient to support a standard D1+ LCOE analysis for the Orbital Levitated Dipole. All five analysis sections face blocking gaps rooted in the same fundamental problem: Zephyr Fusion has made no technical disclosures, and the orbital D-He3 concept is sufficiently novel that no published plant study exists anywhere in the literature. The most informative source in the collection (OpenStar arXiv 2602.20564) is an analog for the dipole confinement architecture but addresses D-T fuel, terrestrial deployment, and conventional thermal power conversion — three of the four defining characteristics of Zephyr's concept are opposite.
 
-The physics section (Section 2) can be written with moderate confidence, drawing on LDX/RT-1 heritage and the arxiv 2602.20564 reactor study. The maturity section (Section 3) can clearly delineate demonstrated physics (TRL 4-5) from unbuilt engineering subsystems (TRL 1-2). The materials section (Section 4) has enough to discuss He-3 supply and REBCO.
+What a D1+ analysis can do with the current data:
+- Characterize the physics basis and why the orbital approach is hypothetically attractive
+- Document what is unknown and why
+- Bound D-He3 fusion requirements (triple product, He-3 supply chain impossibility at current production rates)
+- Note the NASASpaceFlight critique as indicative of fundamental engineering gaps (power conversion, heat removal, neutron management)
+- Use OpenStar's terrestrial dipole cost methodology as a partial structural analog (HTS coil, REBCO tape, magnet engineering) with explicit caveats
 
-The LCOE model (Deliverable 2) requires a methodological decision before coding: **standard fusion LCOE ($/kWh assuming grid connection) does not apply to an orbital power plant.** The analysis must either (a) frame LCOE in terms of delivered power at the customer endpoint — including power beaming losses and ground/orbit receiver infrastructure — or (b) analyze specific power (W/kg) as the more natural figure of merit for this concept, with LCOE back-derivation for a hypothetical customer. The Hasegawa 1987 "1 kW/kg" figure is the only existing target.
+**Recommendation**: Proceed to a full analysis structured as a "concept assessment" rather than a quantitative LCOE model. Flag explicitly that no LCOE computation is possible from first principles without Zephyr disclosures, and use the $1B/MW ISS solar baseline and Zephyr's own <$30M claim as the only available cost reference points (marking both as highly uncertain). Acquiring the Hasegawa 1987/1990, LDX Boxer (2010), and ARIES-III D-He3 sources before writing would meaningfully improve coverage of the physics basis and direct energy conversion context even if the cost gap cannot be closed.
 
-The $30M claim from the YC launch page is for the confinement volume (likely the magnet alone), not a system cost. The actual capital cost is dominated by unknowns: system mass × launch cost/kg + direct conversion hardware + power beaming transmitter. Without these, the quantitative model must be explicit that it is computing a lower bound on system capital cost and parametrically sweeping the unknown fractions.
-
-**Recommend**: Acquire the ARIES-III and Hasegawa 1987 full texts before writing the analysis — both are cited in the dossier and likely contain quantitative parameters (plasma conditions, direct conversion efficiency, reactor-scale cost estimates) that would substantially improve the analysis quality. Without them, every LCOE-relevant number will be first-principles inference.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Insufficient Data"
 blocking_count: 10
-important_count: 3
-counting_method: "section_5_missing_parameters"
+important_count: 7
+counting_method: "deduplicated across all sections; counted distinct blocking gaps: (1) no company technical disclosures, (2) energy conversion pathway uncharacterized, (3) plasma-orbit stability unknown, (4) direct energy conversion TRL 1-2, (5) no plant electrical output target, (6) no capital cost estimate, (7) He-3 fuel cost at scale unknown, (8) capacity factor/availability framework inapplicable, (9) power beaming MW-scale losses unknown, (10) He-3 production at reactor scale infeasible with current supply. Important gaps: heating method unconfirmed, compact RF for orbit not sourced, orbital HTS thermal management not sourced, D-He3 triple product requirement not compiled, REBCO radiation hardness in LEO not sourced, Hasegawa 1987/1990 not extracted, LDX/RT-1 experimental papers not extracted."
 section_coverage:
   availability_of_data:       "Poor"
-  system_function:            "Partial (physics understood; engineering and economics not)"
-  subsystem_maturity:         "Partial (heritage physics demonstrated; most engineering subsystems at TRL 1-2)"
-  materials_supply_chain:     "Partial (He-3 supply well-documented elsewhere; orbital supply chain is unique)"
-  lcoe_parameter_extraction:  "Poor — almost no LCOE-relevant parameters available; standard LCOE framework may not apply"
-```
+  system_function:            "Poor"
+  subsystem_maturity:         "Partial"
+  materials_supply_chain:     "Partial"
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
