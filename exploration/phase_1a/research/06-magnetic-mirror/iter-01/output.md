Now let me compile the full dossier.

---

## Research Findings: Magnetic Mirror (p-B11) — Pale Blue Fusion

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: ARPA-E presentation (Day2_08_Fisch.pdf, July 2025) — centrifugal magnetic mirror confinement
- **Notes**: The CHARM concept uses magnetic mirror fields enhanced by plasma rotation (centrifugal confinement). This is magnetic confinement — the plasma is confined by external magnetic fields in a mirror geometry, with rotation providing additional stabilization and differential species confinement.

### Confinement Concept
- **Value**: `Magnetic mirror`
- **Confidence**: high
- **Citation**: ARPA-E presentation — "CHARM: CHambered Aneutronic Rotating Mirror"
- **Notes**: Specifically a **centrifugal magnetic mirror** — a rotating mirror where E×B rotation provides centrifugal enhancement of confinement. The multi-chamber architecture (fusion chamber + heat exchange chamber + plug) is a key distinguishing feature. The proprietary name is "CHARM" (CHambered Aneutronic Rotating Mirror). Related physics validated on CMFX at University of Maryland (separate group).

### Fuel
- **Value**: `p-B11`
- **Confidence**: high
- **Citation**: ARPA-E project title "Economical Proton-Boron11 Fusion"; Princeton press release (2022); all publications
- **Notes**: The entire concept is designed around p-B11's unique properties — mass disparity between protons (1 amu) and boron-11 (11 amu) enables centrifugal species separation. Fisch calls p-B11 "the holy grail of really clean, really abundant fusion energy."

### Primary Heating
- **Value**: `RF + NBI`
- **Confidence**: low
- **Citation**: Inferred from described alpha channeling mechanism and published physics
- **Notes**: The primary energy input mechanism is **RF waves** (alpha channeling) — waves extract energy from fusion-born alpha particles and channel it into protons, maintaining the nonthermal distribution. The "hybrid fast and thermal proton scheme" (Kolmes et al. 2022) relies on wave-particle interactions to sustain energetic protons. The specific RF scheme is not publicly specified. The concept may not use NBI at all — the "RF + NBI" vocabulary is the closest match, but pure RF with alpha channeling is more accurate. The heating is fundamentally wave-driven. **Best fit might be `RF (ECRH)` or `RF (ICRH)` but neither is confirmed** — the waves used for alpha channeling could be ion cyclotron waves, lower hybrid waves, or other modes. Recommending schema note: "RF (alpha channeling)" would be more accurate for this concept.

### Energy Capture
- **Value**: `Direct (charged particle)`
- **Confidence**: medium
- **Citation**: Patent US20230298771 "Direct Energy Converter for Axisymmetric Mirror Fusion Reactor" (2023); search results describing Standing Wave Direct Energy Converter (SWDEC); ARPA-E presentation question #9 "Can rotation energy be recovered efficiently?"
- **Notes**: p-B11 fusion produces only charged particles (3 alpha particles per reaction, no neutrons). The group has patented a Standing Wave Direct Energy Converter (SWDEC) that converts alpha particle kinetic energy directly to electricity via an RF device. Power from SWDEC is recirculated to maintain the radial electric field driving plasma rotation. The presentation also mentions capturing helium energy as a key requirement. Since ~99% of fusion energy is in charged particles, direct conversion is the natural and only viable path.

### Plasma State
- **Value**: `Confined`
- **Confidence**: medium
- **Citation**: ARPA-E presentation; Princeton press release describing theoretical/early-stage research
- **Notes**: The concept targets a **sustained, nonthermal** plasma state — not a burning plasma in the traditional sense. The "highly nonthermal approach" with energetic protons and colder electrons/boron means this is neither a conventional burning plasma nor a simple confined plasma. The protons are maintained at fusion-relevant energies by alpha channeling, while electrons and boron are kept cooler to minimize bremsstrahlung. `Sustained` could also fit if the concept achieves net energy gain, but given the early theoretical stage and Q~1 target range suggested by the breakeven analysis, `Confined` is more appropriate. The concept is still working toward demonstrating Q > 0.

### Magnet Type
- **Value**: `HTS (wound)`
- **Confidence**: low
- **Citation**: Inferred from mirror geometry and current fusion magnet trends; CMFX uses LTS but is a university experiment
- **Notes**: The Pale Blue/CHARM concept has not publicly specified its magnet technology. Mirror machines use solenoidal (axisymmetric) coils — simple wound coils, not complex 3D geometries. The related CMFX experiment at UMD uses **LTS superconducting magnets** (3 T throat, 0.3 T midplane). For a reactor-scale device, HTS would be the likely choice given current industry trends, but this is speculative. Could equally be `LTS` or even `Resistive` for early experiments. **TBD** would be more honest — I'm recording `HTS (wound)` as a likely reactor choice with low confidence.

### Tritium Breeding
- **Value**: `N/A (aneutronic)`
- **Confidence**: high
- **Citation**: ARPA-E presentation: "No tritium breeding and containment" listed as key p-B11 advantage
- **Notes**: p-B11 fuel cycle produces no tritium. No breeding blanket needed.

### Neutron Management
- **Value**: `Minimal (aneutronic)`
- **Confidence**: high
- **Citation**: ARPA-E presentation: "No neutron damage and induced radioactivity"; p-B11 reaction physics
- **Notes**: p-B11 is truly aneutronic (<1% neutron energy from side reactions). The presentation explicitly lists "no neutron damage and induced radioactivity" and "easier regulatory environment" as advantages. Minimal shielding required.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: Initial concept CSV lists "Continuous"; centrifugal mirror physics is inherently steady-state; ARPA-E presentation shows continuous plasma flow between chambers
- **Notes**: The CHARM concept is a steady-state device — plasma continuously rotates in the mirror, boron is centrifugally trapped, and helium ash is continuously extracted via alpha channeling. There is no pulsed compression or discrete burn events.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state concept
- **Notes**: N/A — continuous operation, no repetition rate applicable.

### Driver Technology
- **Value**: `Centrifugal mirror with alpha channeling (RF waves, E×B rotation)`
- **Confidence**: high
- **Citation**: ARPA-E presentation (CHARM concept); published papers on alpha channeling, centrifugal confinement, ponderomotive barriers
- **Notes**: The distinguishing technology bet is the combination of: (1) **centrifugal confinement** via E×B plasma rotation providing species-selective confinement exploiting mass disparity, (2) **alpha channeling** using RF waves to extract energy from fusion-born helium and channel it into fuel protons, (3) **ponderomotive barriers** using static field perturbations for species-selective ion traffic control between chambers, and (4) **multi-chamber architecture** (fusion + heat exchange + plug) enabling spatial separation of reactants and products. Patents filed March 2025.

---

## Metadata Columns

### Concept Name
- **Value**: Magnetic Mirror (p-B11) — CHARM (CHambered Aneutronic Rotating Mirror)
- **Notes**: "CHARM" is the proprietary concept name from the ARPA-E presentation.

### Companies
- **Value**: Pale Blue Fusion (incorporating, Princeton University spinoff)
- **Confidence**: high
- **Citation**: ARPA-E 2025 presentation mentions "approvals and support from Princeton University in place" with plan to incorporate as Pale Blue Fusion
- **Notes**: As of July 2025, not yet formally incorporated. Founded by/associated with Nat Fisch, Ian Ochs, Elijah Kolmes (all Princeton). No public website found. Not yet listed in FIA membership or Wikipedia's list of fusion companies.

### Description
- **Value**: Multi-chamber centrifugal magnetic mirror using plasma rotation to centrifugally separate lighter protons from heavier boron-11 ions, enabling a nonthermal p-B11 fusion approach. Alpha channeling extracts helium ash energy via RF waves and recycles it into fuel protons, addressing the critical bremsstrahlung and helium poisoning challenges of p-B11 fusion.
- **Confidence**: high

### Published Machine/Plant?
- **Value**: No
- **Confidence**: high
- **Citation**: Princeton press release (2022) describes "purely theoretical research with no experiments yet"; ARPA-E presentation shows reactor concept (CHARM) but no built hardware
- **Notes**: CHARM is a reactor concept shown in ARPA-E presentations with CAD-like renderings, but no physical machine has been built by this group. The related CMFX experiment at UMD validates centrifugal mirror physics but is a separate effort.

### Lab Experiments
- **Value**: CMFX (Centrifugal Mirror Fusion Experiment, University of Maryland) — validates centrifugal mirror confinement physics. First plasma 2022, fusion yield measurements 2025.
- **Confidence**: medium
- **Citation**: arXiv:2505.23047; ARPA-E BETHE program funding for CMFX
- **Notes**: CMFX is a separate group (UMD, not Princeton/Pale Blue) but demonstrates the underlying centrifugal mirror physics. The Fisch group's work is theoretical — published papers on alpha channeling, breakeven requirements, ash removal, and ponderomotive barriers, but no dedicated experimental facility.

---

## Remaining Gaps

1. **Primary Heating** (low confidence): The specific RF wave type/frequency for alpha channeling is not publicly specified. The schema's controlled vocabulary doesn't have a clean match for "RF (alpha channeling)." Could be ICRH-range, lower hybrid, or other modes. A detailed technical paper specifying the wave scheme would resolve this. **Recommend recording as `RF (ICRH)` with a note**, since alpha channeling in mirrors historically uses ion cyclotron range waves, but this is inferred from general physics.

2. **Magnet Type** (low confidence): No public specification from Pale Blue/Fisch group. The CMFX experiment uses LTS, but a reactor would likely use HTS. The group's publications focus on plasma physics, not engineering subsystems. **Recommend recording as `TBD`** until the company discloses.

3. **Plasma State** (medium confidence): The nonthermal, wave-sustained plasma doesn't map cleanly to the schema vocabulary. It's not "Burning" (alpha heating doesn't dominate in the traditional sense — alphas are removed, their energy channeled into protons via waves). It's not simply "Confined" either — it's actively sustained by wave-particle interactions. `Sustained` might be the better fit.

4. **Energy Capture** (medium confidence): Direct charged particle conversion via SWDEC is described in a related patent and search results, but not explicitly confirmed as Pale Blue's baseline. The patent (US20230298771) is from a different inventor group — need to verify if Pale Blue adopts this approach or develops their own DEC technology. The physics strongly favors direct conversion for p-B11.

5. **Company status**: Pale Blue Fusion appears to be pre-incorporation as of the July 2025 ARPA-E presentation. No website, no FIA listing, no Crunchbase profile found. The company may have incorporated since then (current date: March 2026) but no public evidence found.

## Sources Consulted

- ARPA-E presentation: https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_08_Fisch.pdf (PDF, image-based — read via user-provided screenshots)
- ARPA-E project page: https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/economical-proton-boron11-fusion
- Princeton press release: https://www.princeton.edu/news/2022/03/10/fisch-receives-funding-unlikely-fantastic-clean-energy-technology
- Princeton breakthrough article: https://www.princeton.edu/news/2025/12/17/search-next-big-breakthrough-princeton
- Princeton Technology Licensing page: https://patents.princeton.edu/news/fisch-receives-funding-unlikely-fantastic-clean-energy-technology
- arXiv:2302.12346 — Ochs, Munirov, Fisch, "Confinement time and ambipolar potential in a relativistic mirror-confined plasma"
- arXiv:2504.18634 — Kolmes, Ochs, Fisch, "Ion Mix Can Invert Centrifugal Confinement"
- arXiv:2502.02008 — "Ponderomotive barriers in rotating mirror devices using static fields"
- arXiv:2502.13300 — Ochs, Kolmes, Fisch, "Preventing ash from poisoning proton-boron 11 fusion plasmas"
- IEEE Spectrum: https://spectrum.ieee.org/aneutronic-fusion (did not mention Pale Blue)
- NextBigFuture: https://www.nextbigfuture.com/2023/10/five-aneutronic-fusion-companies.html (did not mention Pale Blue)
- Centauri Dreams: https://www.centauri-dreams.org/2023/09/20/a-fusion-drive-using-centrifugal-mirror-technologies/ (centrifugal mirror context)
- Patent US20230298771: "Direct Energy Converter for Axisymmetric Mirror Fusion Reactor" (SWDEC concept)
- CMFX at UMD: https://ireap.umd.edu/research/centrifugal-mirror-fusion-experiment
- Fusion Industry Association members: https://www.fusionindustryassociation.org/about/members/ (Pale Blue not found)
- Wikipedia list of nuclear fusion companies (Pale Blue not listed)
- Crunchbase/Tracxn: Found "Pale Blue" (aerospace propulsion company, unrelated) but no "Pale Blue Fusion"
