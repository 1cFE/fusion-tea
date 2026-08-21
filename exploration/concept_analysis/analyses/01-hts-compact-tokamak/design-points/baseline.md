# Design Point Reasoning Trace — 01-hts-compact-tokamak

## 1. Sources walked

- `knowledge/concept_research/01-hts-compact-tokamak/dossier.md` — synthesized concept summary; confirmed two published machines (SPARC, ARC), three ARC operating phases, and that the 400 MWe Virginia target has no published engineering parameters
- `knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md` — Sorbom et al. 2015 ARC paper (arXiv 1409.3540 / Fusion Engineering and Design 100); defines all three operating phases with per-phase Pnet (190, 233, 261 MW), geometry (R0=3.3m, a=1.1m, B0=9.2T, Pf=525MW), fuel (D-T), and blanket design
- `knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/sparc-icrf-heating-paper.md` — Lin & Wright et al. 2020, J. Plasma Physics; covers SPARC physics basis; confirmed SPARC has no electrical output design point
- `knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/cfs-2025-2026-updates.md` — Fortune.com / CFS public communications, January 2026; describes ARC as a "400-megawatt plant" in Chesterfield, Virginia; confirmed this figure appears only in press coverage with no published engineering parameters
- `knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arc-power-conversion-studies.md` — Colliva et al. 2024 (Sapienza University / Eni); independently analyzes three power conversion cycle options for ARC using the Sorbom 2015 design basis; confirms 645 MWth thermal output to the PCS in the FNSF phase and corroborates the geometry and thermal power from the 2015 paper

## 2. Candidates surfaced

**SPARC (CFS, under construction)**
Under construction outside Boston; first plasma targeted 2027. Burning plasma experiment designed for Q ~ 11. No electrical output by design — SPARC is a physics demonstrator, not a power plant. P_native: none. Disqualifies as design point per the selection rule.

**ARC 2015 FNSF phase (Sorbom et al.)**
One of three operating phases of the same ARC geometry (R0=3.3m, a=1.1m, B0=9.2T, Pf=525MW, D-T). Blanket outlet temperature 900 K; helium Brayton cycle efficiency ~40%. Pnet = 190 MW, Qe = 3. The paper's analytically primary phase — all neutronics, materials, and detailed engineering analysis performed at these conditions. Framed as an FNSF experimental facility / power plant demonstration at conservative material limits. Maturity tier: paper-concept.

**ARC 2015 Conservative Pilot phase (Sorbom et al.)**
Same geometry as FNSF phase. Blanket outlet temperature 1100 K (requires "evolution to higher temperature materials informed by the FNSF stage"); Brayton cycle efficiency ~46%. Pnet = 233 MW, Qe = 3.5. The paper's abstract headlines the reactor as "~200–250 MWe," which brackets this phase. Described as "more speculative" than the FNSF phase but representing the pilot plant operating intent. Maturity tier: paper-concept.

**ARC 2015 Aggressive Pilot phase (Sorbom et al.)**
Same geometry. Blanket outlet temperature 1200 K; Brayton cycle efficiency ~50%. Pnet = 261 MW, Qe = 3.8. Explicitly the most speculative phase, requiring 1200 K materials not yet demonstrated. Maturity tier: paper-concept.

**ARC 400 MWe (CFS 2025–2026 Virginia commercial target)**
Mentioned in CFS public communications (Fortune.com, January 2026) as the output of the first commercial ARC plant in Chesterfield, Virginia, with Google and Eni PPAs fully subscribing the capacity. No published engineering parameters — geometry, magnet design, blanket configuration, and thermal cycle for this design are undocumented in any accessible source. P_native: unknown (press figure only). Plant-stitching with the 2015 geometry is forbidden per the selection rule; this candidate does not qualify.

## 3. Selection

The ARC 2015 Conservative Pilot phase is selected. SPARC is excluded (no electrical output); the 400 MWe Virginia target is excluded (no published engineering parameters). The three remaining candidates are three operating phases of the same 2015 ARC geometry. The FNSF phase (190 MWe) is the paper's analytically primary phase but is framed as an FNSF experimental facility at conservative material limits — not the pilot plant design point. The Aggressive Pilot (261 MWe) requires 1200 K blanket materials the paper explicitly flags as speculative and undemonstrated. The Conservative Pilot phase (233 MWe) is the design's natural pilot plant operating point: it is the intermediate case, the paper's headline range ("~200–250 MWe") brackets it, and its 1100 K blanket temperature is described as the first post-FNSF evolution step rather than an outlier extrapolation.

```yaml
proposal:
  concept_id: 01-hts-compact-tokamak
  design_name: "ARC 2015 Conservative Pilot phase (Sorbom et al.)"
  maturity_tier: paper-concept
  p_native_mwe: 233
  primary_sources:
    - knowledge/concept_research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md
    - knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arc-power-conversion-studies.md
  selection_rationale: |
    The ARC 2015 Conservative Pilot phase (Sorbom et al.) is the pilot plant design point for
    the CFS HTS compact tokamak concept. SPARC has no electrical output by design and is
    excluded. The 400 MWe Virginia target (CFS 2025–2026 communications) has no published
    engineering parameters and cannot be adopted as a design point. Among the three 2015 ARC
    phases sharing the same geometry (R0=3.3m, a=1.1m, B0=9.2T, Pf=525MW, D-T fuel), the
    Conservative Pilot phase (blanket outlet 1100 K, Brayton ~46%, Pnet=233 MW, Qe=3.5) is
    chosen over the FNSF phase (190 MWe) because the latter is framed as an FNSF experimental
    facility at conservative material limits rather than the pilot plant design point, and over
    the Aggressive Pilot (261 MWe) because that phase requires 1200 K blanket materials the
    paper explicitly flags as speculative and undemonstrated. The Conservative Pilot is the
    paper's headlined design range (~200–250 MWe) and the standard reference in the literature
    for ARC's pilot plant capability.
  alternatives_considered:
    - design: "ARC 2015 FNSF phase (Sorbom et al.)"
      reason_rejected: primarily an FNSF experimental phase at conservative material limits, not the pilot plant design point
      sensitivity_implication: >
        If picked instead, P_native would be lower (190 vs 233 MWe) → more modules at 1 GWe
        → 1 GWe LCOE shifts up. Worth probing if the cost analysis is specifically scoped to
        the FNSF duty cycle rather than the commercial pilot plant mission.
    - design: "ARC 2015 Aggressive Pilot phase (Sorbom et al.)"
      reason_rejected: requires 1200 K blanket materials explicitly flagged as speculative in the 2015 paper
      sensitivity_implication: >
        If picked instead, P_native would be higher (261 vs 233 MWe) → fewer modules at 1 GWe
        → 1 GWe LCOE shifts down. Worth probing if high-temperature blanket materials (>1100 K
        in FLiBe-compatible alloys) are demonstrated at scale.
    - design: "SPARC (CFS, under construction)"
      reason_rejected: no electrical output by design; burning plasma demonstrator only
      sensitivity_implication: "n/a — SPARC has no P_native and cannot be used as a design point."
    - design: "ARC 400 MWe (CFS 2025–2026 Virginia commercial target)"
      reason_rejected: no published engineering parameters; power figure from press coverage only
      sensitivity_implication: >
        If CFS publishes engineering parameters for the 400 MWe Virginia design, P_native would
        be substantially higher (400 vs 233 MWe) → fewer modules at 1 GWe → 1 GWe LCOE shifts
        down significantly. This is the most consequential sensitivity in the candidate set and
        the primary watch item for design-point revision.
```

## 4. Open questions

- **400 MWe Virginia engineering basis**: CFS has publicly stated a 400 MWe commercial target with PPAs from Google and Eni, but no engineering parameters (geometry, magnet design, thermal cycle) are published. If a design basis document is released, the design point should be revisited; P_native would rise substantially and LCOE would shift down.
- **ARC geometry evolution**: The 2015 paper was a conceptual study at MIT PSFC before CFS existed as a company. CFS has been operating for 8+ years since and the internal ARC design almost certainly differs from the 2015 publication. If CFS releases an updated ARC design document, the 2015 geometry-based Conservative Pilot may no longer be representative — even if P_native is retained near 233 MWe.
- **Power conversion cycle**: The 2015 paper uses a helium Brayton cycle at the Conservative Pilot operating point; Colliva et al. 2024 and independent analyses favor supercritical steam Rankine and find different efficiencies. If CFS commits publicly to a cycle with a documented efficiency, the published Pnet of 233 MW could shift — potentially changing which phase best represents the commercial design point.

---

The proposal selects **ARC 2015 Conservative Pilot phase** at **P_native = 233 MWe**. The key call is preferring the Conservative Pilot over the FNSF phase (190 MWe): the FNSF phase is the paper's analytically primary case but is explicitly positioned as an experimental facility first, pilot plant second. The most significant open question is the 400 MWe Virginia target — if CFS publishes engineering parameters, that would force a re-selection.

If you'd like me to write this to `.project/completed/20260821_concept-rework-tables/proposals/01-hts-compact-tokamak.proposal.md`, I can do so once you approve the write permission.