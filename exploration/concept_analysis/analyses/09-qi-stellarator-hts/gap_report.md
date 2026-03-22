# Gap Assessment: QI Stellarator - HTS

**Overall Rating: Mostly Ready**

Here's the headline picture:

**Strengths** — The Stellaris plant study (FED, 2025) is unusually substantive for a company at this stage. Power balance is well-characterized: 2.7 GW fusion → ~3.1 GW thermal → ~1 GW net electric (~32% efficiency). The WCLL blanket (TBR 1.07, EUROFER97, <500°C) gives concrete engineering anchors. W7-X provides a validated physics basis, and the analogous Helios stellarator paper (arXiv 2512.08027v1) fills several inferential gaps (ECRH at 170 GHz, steam Rankine at 635°C, ~40% thermal efficiency). Operation is steady-state — no pulsed-system complexity.

**Key gaps in order of criticality:**

1. **Full Stellaris paper** — `proprietary` (paywalled, not truly proprietary). This single source would resolve Q value, heating specs, power conversion details, shielding architecture, and remote maintenance design. **Highest-priority acquisition before writing.**

2. **Capital cost breakdown** — `not-yet-sourced`. No Stellaris cost estimate exists in public sources. Build from EU DEMO WCLL cost studies (blanket), scaled REBCO tape projections (magnets), and conventional BoP. Alpha demo cost (~€2B) is a weak anchor.

3. **3D non-planar HTS coil manufacturing cost** — `not-yet-sourced`. This is the concept's most novel and risky component. SMC demo in 2027 is the de-risking milestone. PSI/BNET may have published engineering detail.

4. **First-wall replacement schedule** — `truly-unknown`. Stellarator PFC geometry is far more complex than a tokamak; no commercial-scale data exists. Drives O&M cost structure.

5. **Capacity factor** — `derivable`. Steady-state design supports high availability (~85–90%) as a baseline; remote maintenance interval (from 3D geometry) is the main sensitivity axis.

**Recommendation:** Proceed to full analysis. Prioritize acquiring the Stellaris paper and EU DEMO WCLL cost literature before finalizing LCOE numbers. The primary model sweep axes should be REBCO tape cost at scale, 3D coil manufacturing multiplier, Q value, and first-wall replacement interval.

Report written to `analyses/09-qi-stellarator-hts/gap_report.md`.
