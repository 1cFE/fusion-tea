I have all the source data I need. Now I'll compose the new-format analysis.

### 1. Design Point Block

```
Design name:       ARC pilot power plant (Sorbom et al. 2015 conceptual design)
Company:           Commonwealth Fusion Systems (MIT PSFC spinout)
Maturity tier:     paper-concept
P_native (MWe):    233
Primary sources:
  - arc-reactor-specifications.md (Sorbom et al. 2015 — reactor dimensions, magnets, blanket, cost, R&D gaps)
  - arc-power-conversion-studies.md (Colliva et al. 2024 — three-cycle PCS comparison, Rankine preferred at 46% net)
  - sparc-icrf-heating-paper.md (Lin & Wright et al. 2020 — ICRF system, SPARC machine parameters)
  - cfs-2025-2026-updates.md (CFS Jan 2026 — first TF coil installed, SPARC timeline, 400 MWe commercial target)
  - dossier.md (Phase 1a synthesis — per-column confidence ratings, key sources)
Selection rationale: CFS has two candidate devices: SPARC (burning plasma experiment, under
construction, no net electrical output) and ARC (conceptual power plant, detailed design published
in peer-reviewed literature with geometry, physics, blanket engineering, and component-level cost
analysis). SPARC produces no net electricity and routes out per the design-point selection rule. ARC
is therefore the only viable design point. The 2015 Sorbom paper represents the fully-analyzed
published baseline; the 2025 CFS target of 400 MWe has no published updated physics or geometry
and cannot be used as a design point. P_native of 233 MWe corresponds to the conservative Pilot
phase from the 2015 paper (1100 K FLiBe, ~46% Brayton efficiency, Qe = 3.5), which is the
lower-risk commercial demonstration scenario within the stated 200–250 MWe range.
```

### 2. LCOE-relevant Parameters (ARC 2015 Design Point, 233 MWe)

| Parameter | Value | Source | Confidence | Note |
|---|---|---|---|---|
| R0 (major radius) | 3.3 m | arc-reactor-specifications.md §2, Table 7 | high | Final design after iteration from 3.2 m 0-D estimate |
| a (minor_radius / plasma_t) | 1.13 m | arc-reactor-specifications.md §2, Table 7 | high | Aspect ratio = R0/a = 2.92 ≈ 3 |
| elongation (κ) | 1.84 | arc-reactor-specifications.md Table 7 | high | Below elongation limit κ ≤ 5.4ε for vertical stability |
| B0_on_axis | 9.2 T | arc-reactor-specifications.md §2, §4.2 | high | Fixed in final design; enables compact high-power-density |
| B_peak_on_coil | ~23 T | arc-reactor-specifications.md §4.1, Table 3 (Layer #1) | high | Peak at inboard midplane; REBCO operates at 50% of critical current margin |
| fusion_power_MW | 525 MW | arc-reactor-specifications.md §3.4 (ACCOME result) | high | Converged from initial 500 MW 0-D target; Pfus/Sp ≈ 2.5 MW/m² |
| net_electric_MWe | 233 MWe | arc-reactor-specifications.md §2 (conservative Pilot) | medium | 1100 K FLiBe outlet, ~46% Brayton efficiency; FNSF baseline is 190 MWe (900 K). 2025 CFS target is 400 MWe (no published updated parameters) |
| Qp (plasma gain) | 13.6 | arc-reactor-specifications.md abstract | high | Fully non-inductive design point |
| Qe (electricity gain) | 3.5 | arc-reactor-specifications.md §2 | high | Conservative Pilot phase; ~3.0 at FNSF, ~3.8 at aggressive Pilot |
| eta_th (thermal efficiency) | ~46% | arc-reactor-specifications.md §2; arc-power-conversion-studies.md Table 15 | high | ARC paper uses Brayton at 1100 K; Colliva 2024 Rankine at similar input gives 46% net. Brayton and Rankine both converge to ~46% net at ~1100 K conditions |
| p_input_MW (auxiliary heating, coupled) | 38.6 MW | arc-reactor-specifications.md §2, §3.4 (ACCOME) | high | 25 MW LHCD (8 GHz) + 13.6 MW ICRF (50 MHz); wall-plug: 69.6 MW LHCD + ~19 MW ICRF |
| Ip (plasma current) | 7.75 MA | arc-reactor-specifications.md §3.4 | high | ACCOME equilibrium; 1.77 MA LHCD-driven + 1.1 MA ICRF-driven + ~4.9 MA bootstrap |
| bootstrap_fraction | 63% | arc-reactor-specifications.md §3.4 | high | Modest by AT standards — gives more external current profile control |
| q95 (safety factor) | ~7.2 | arc-reactor-specifications.md §3.4 | high | Well above kink limit; reduces disruption risk |
| beta_N | 2.59 | arc-reactor-specifications.md §3.2 | high | Below Troyon limit (3) and 4*li limit (2.68); margin to pressure-driven instabilities |
| confinement factor (H98) | 2.8 | arc-reactor-specifications.md §3.5 | medium | Consistent with AT weak-shear scenarios on DIII-D; I-mode basis unvalidated at ARC parameters |
| TBR (FLiBe blanket) | ≥ 1.1 (opt ~1.22) | arc-reactor-specifications.md §5.3 | high | 90% ⁶Li enrichment; double-walled VV with W first wall and Be neutron multiplier |
| FLiBe bulk blanket outlet temperature | 900 K (FNSF) / 1100 K (cons. Pilot) | arc-reactor-specifications.md §5.4.2 | high | Inlet at 800 K; flow velocity ≤ 0.2 m/s; sets thermal cycle efficiency |
| TF coil operating temperature | 20 K | arc-reactor-specifications.md §4.2 | high | Subcooled REBCO; cooled by liquid hydrogen (5–10 bar) |
| TF coil fluence lifetime | 9 FPY | arc-reactor-specifications.md §5.2 | high | Lower bound from 3×10¹⁸ n/cm² fluence limit; could extend with larger radius |
| REBCO tape (TF coil system) | ~5,730 km total | arc-reactor-specifications.md §4.1 | medium | 12 mm width; 18 TF coils × 2 legs × 120 CIC cables; cable length per leg ~6.7–7 m |
| REBCO tape materials cost | $103–206M (2014 USD) | arc-reactor-specifications.md §6 | medium | At $36–198/m (2014 price range); does not include fabrication labor or tooling |
| VV + internal structure material | Inconel 718 | arc-reactor-specifications.md §2, §5.1 | high | "First-round material" — corrosion resistant but prone to nuclear activation |
| W first wall thickness | 1 cm | arc-reactor-specifications.md §5.3 | high | Tungsten chosen to increase TBR (neutron multiplication cross section) |
| TiH₂ neutron shield mass | ~380 t | arc-reactor-specifications.md §6 | high | At ~$26.4/kg ≈ $10M materials cost |
| FLiBe blanket tank inventory | ~950 t | arc-reactor-specifications.md §5.4 | medium | Includes blanket tank + cooling channels + HX inventory; at $154/kg NOAK → ~$146M |
| Magnet+structure fabricated cost | $5.15B (2014 USD) | arc-reactor-specifications.md §6 | medium | Mass-proportional at $1.06M/tonne; ~92% of total fabricated component cost; NOAK assumed |
| Blanket fabricated cost | $260M (2014 USD) | arc-reactor-specifications.md §6 | medium | $160M materials + ~$100M fabrication; FLiBe + Inconel VV + tritium extraction hardware |
| VV fabricated cost | $92M (2014 USD) | arc-reactor-specifications.md §6 | medium | $5.5M materials |
| Total fabricated component cost | $5.56B (2014 USD) | arc-reactor-specifications.md §6 | medium | VV + blanket + magnets only; explicitly excludes BoP, land, indirects, financing |
| Capacity factor | not published | proprietary | — | No CFS/ARC publication states a target; model uses framework default 0.85 |
| Annual O&M cost | not published | not-yet-sourced | — | FECONS anchor: $60/kWe-yr → ~$14M/yr at 233 MWe; not ARC-specific |

### 3. Override Candidates

```yaml
overrides:
  - account: CAS22.1.3
    value: 6900
    enabled: true
    provenance: derived
    source: "arc-reactor-specifications.md §6 (Sorbom et al. 2015)"
    rationale: >
      Sorbom §6 reports total fabricated magnet + structure cost as $5.15B (2014 USD) using
      mass-proportional scaling at $1.06M/tonne benchmarked against four prior conceptual designs
      (FIRE, BPX, PCASTS, ARIES-RS). Inflated to 2024 USD: $5.15B × CPI 1.34 = $6.9B. This
      account covers all 18 REBCO TF coils (demountable, with comb-style joints), PF coils,
      CS, and supporting structure. The ~92% share of total fabricated cost is driven by REBCO
      tape unit cost ($36–198/m in 2014, ~$20/m in 2025), fabrication tooling for demountable
      joints, and steel structure. Library default for a conventional LTS tokamak at this scale
      would not capture the HTS tape cost premium or the joint fabrication overhead. The 2025
      REBCO market price (~$20/m ≈ $100/kA-m) is well below the 2014 range but ~10× above the
      commercial viability target (~$10/kA-m), so this value should be treated as a mid-point
      scenario; model tape cost as a sensitivity spanning at least 5× (from $10 to $50/kA-m).
      The $1.06M/tonne basis embeds implicit NOAK manufacturing learning — first-of-kind premium
      not captured here.

  - account: CAS22.1.1
    value: 348
    enabled: true
    provenance: derived
    source: "arc-reactor-specifications.md §6 (Sorbom et al. 2015)"
    rationale: >
      Sorbom §6 reports fabricated blanket cost as $260M (2014 USD), comprising $160M materials
      (FLiBe + Inconel + heat exchangers) and ~$100M fabrication. Inflated to 2024 USD:
      $260M × CPI 1.34 = $348M. This account covers the FLiBe liquid immersion blanket tank,
      double-walled Inconel-718 vacuum vessel with FLiBe cooling channels, tritium extraction
      hardware, and Be neutron multiplier. The library default for solid ceramic breeder modules
      would not capture the FLiBe chemical processing plant, the molten-salt-compatible HX
      materials, or the tritium extraction system — all ARC-specific additions. The ARPA-E
      ALPHA re-costing study (osti-servlets-purl-1820946.md) benchmarks Fuel Processing
      (CAS22.5 in that taxonomy) at $92–176M for structurally analogous concepts, consistent
      with this value as an order-of-magnitude floor. FLiBe-specific additions (MHD flow
      conditioning, redox control, Li-6 enrichment recycle) may push actual NOAK cost above $348M.
```

### 4. Family-Delta Notes

**vs. conventional large-bore LTS tokamak (ITER/ARIES-RS archetype):**

The two structural bets that distinguish ARC from the archetype are HTS compactness and the liquid immersion blanket. On the magnet side, ARC achieves 9.2 T on-axis by running REBCO at 23 T peak-on-coil at 20 K — roughly double the on-coil field of Nb₃Sn designs. This enables a tokamak roughly one-third the linear size of ARIES-RS at one-quarter the electrical output, with the cost claim that smaller size dominates over REBCO tape premium. Both overrides above are meant to capture this: CAS22.1.3 at $6.9B reflects the tape-dominated magnet cost, which is higher per unit volume than a Nb₃Sn design at the same field but achieves that field in half the device radius. The demountable TF joint design is novel and adds fabrication overhead not in the library; it enables modular vacuum vessel replacement (the entire VV lifts out as one piece), which is the maintenance approach that justifies the capacity factor assumption — without demonstrating this at power-plant speed, the 0.85 default is optimistic.

On the blanket side, the FLiBe liquid immersion is architecturally different from solid ceramic breeders. The FLiBe simultaneously breeds tritium, shields magnets, and removes heat — eliminating separate shield modules and remote blanket handling hardware at the cost of a molten-salt chemistry plant with no commercial analogue. This structural difference is captured in the CAS22.1.1 override. No override is proposed for the power conversion system (CAS23) because the supercritical Rankine BoP is standard commercial hardware; the library default should apply.

The I-mode operating regime is a real departure: ARC avoids ELMs entirely, reducing divertor erosion rates and potentially extending component life. However, no company cost figure exists for this confinement-mode effect, so it has no corresponding override. It should be treated as a qualitative reliability benefit.

**vs. spherical tokamak HTS (21 — Tokamak Energy ST-E1):**

Both share REBCO CICC technology and FLiBe-to-Rankine BOP. The key divergence is aspect ratio and field strategy: ARC's A=3, B=9.2 T, R=3.3 m achieves high fusion power density via field; ST-E1's A=2.3, B=5.25 T, R=5.0 m compensates with volume. ARC's CAS22.1.3 override at $6.9B reflects the field-dominance strategy — more tape per unit volume at higher unit cost. Concept 21 (ST-E1) has no published cost data and uses ARC as an analogue; their REBCO supply chain constraint is shared and should be modeled identically.

**vs. HTS tokamak full-HTS (28) and state-backed tokamak (33):**

Concept 28 likely represents a larger-scale full-HTS tokamak design that would share the REBCO tape cost structure and demountable-joint trade-offs but at different B/R operating points. Without concept 28's analysis, no specific delta can be stated. Concept 33 (state-backed tokamak) is likely ITER-class scale with state subsidies, LTS magnets, and full NRC regulatory pathway — the $6.9B ARC magnet cost cannot be compared directly because the field and tape type differ fundamentally.

**vs. negative triangularity tokamak (29):**

NT shaping achieves ELM-free operation through plasma cross-section geometry rather than I-mode regime. Both approaches target ELM elimination, but the underlying engineering drivers diverge: NT primarily affects plasma cross-section shaping and the divertor geometry, not the magnet or blanket cost structure. No magnet or blanket delta exists between ARC and an NT design; the distinction is in confinement physics, not cost accounts.

### 5. Open Data Gaps (affecting cost projection to 1 GWe NOAK)

- **Full plant capital cost excluding nuclear island**: No ARC-specific BoP, indirects, owner's costs, or construction financing exist. The $5.56B covers fabricated components only. FECONS framework bounds the indirect multiplier (~1.41× direct costs), but the BoP direct cost structure is absent.
- **Capacity factor**: No CFS publication states an annual availability target for ARC. This is the primary LCOE lever for a CAPEX-heavy plant. The 2× swing from 50% to 90% availability is near-2× LCOE at current magnet cost estimates.
- **ARC 400 MWe commercial design parameters**: CFS's 2025 commercial target (400 MWe, early 2030s, Virginia site) has no published updated geometry, B₀, or Pfus. The 2015 design point at 233 MWe should not be scaled to 400 MWe without an explicit assumption flag; the cost does not scale linearly with output.
- **FLiBe chemistry and tritium extraction plant cost**: Explicitly excluded from the $5.56B fabricated cost. No published ARC-specific estimate exists. ARPA-E ALPHA analogue floor is $100–200M but FLiBe-specific scope likely pushes this higher.
- **REBCO tape NOAK price trajectory**: The commercial viability target (~$10/kA-m) is ~10× below 2025 market price (~$100/kA-m). NOAK projection to 1 GWe scale requires this reduction; no published learning-rate curve specific to REBCO exists. This gap makes CAS22.1.3 the widest-uncertainty cost account.
- **Blanket/VV replacement schedule and remote handling cost**: FLiBe blanket does not face a hard fluence limit, but VV Inconel service life under combined radiation + FLiBe corrosion is uncharacterized. TF coil replacement at 9 FPY is stated but the replacement cost at NOAK is not modeled in any available source.

---

That completes the new-shape analysis. A few notes on the output:

**Design point decision**: SPARC routes out (no net electrical output); ARC 2025 (400 MWe) routes out (no published parameters). The 2015 ARC paper is the only viable design point. P_native = 233 MWe is the conservative Pilot phase — the lowest-risk commercial demonstration scenario within the paper's stated 200–250 MWe range.

**Override count (2 of 0–4)**: Both are derived, not direct — the Sorbom 2015 costs use mass-proportional scaling at $1.06M/tonne, not procurement quotes. No additional overrides are justified because the library's standard tokamak accounts (CAS23 Rankine BOP, CAS21 structures, CAS24 electrical) should apply cleanly to ARC's conventional subsystems.

**What the existing analysis.md preserved vs. dropped**: The new format drops the multi-section narrative (data availability, challenges, subsystem maturity, materials/supply chain, cross-concept notes) in favor of the compact block-table-YAML structure. That narrative content is useful context but lives in the existing file; the new format is the machine-readable basis for `model_setup.py`.
