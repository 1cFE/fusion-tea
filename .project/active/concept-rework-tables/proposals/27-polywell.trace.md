# Design Point Reasoning Trace — 27-polywell

## 1. Sources walked

- `knowledge/concept_research/27-polywell/dossier.md` — synthesized concept summary; confirmed D-T as the current EMC2 design fuel per Park 2025; noted that p-B11 R&D is officially suspended; oriented the candidate search
- `knowledge/concept_research/27-polywell/iter-02/sources/polywell-revisited-2025-park.md` — full text of Park et al. (2025), "Polywell Revisited," arXiv:2508.06761; the only reactor-scale design study; Section 4 provides specific design parameters (1.6 m cube, 4.5 T boundary field, 20 keV, D-T 50:50, ~980 MW fusion power, 78 MW e-beam input, Q=10.5 at γ=0.1); no power conversion system, thermal cycle, or net electrical output stated anywhere in the paper
- `knowledge/concept_research/27-polywell/iter-02/sources/emc2-fpns-talk-polywell-2023.md` — forum post reproducing the DOE/FPA 2023 FPNS program proposal; gives FPNS device parameters (350 kW steady-state fusion, 5–6 MW ion beam, 2–3 T boundary field, 500 eV plasma, 8.5–10 cm plasma radius); $20M / 24 months R&D budget; confirms FPNS is a neutron-production facility for materials testing, not a power plant
- `knowledge/concept_research/27-polywell/iter-03/sources/thefusionreport-p-interview-with-emc2-fusion-a-different/output.md` — TheFusionReport 2025 interview with EMC2 (Dave Mansfield); mentions "a system with coils roughly 2 meters in diameter should theoretically be able to generate 100 megawatts (100 MW) of fusion energy"; informal remark, no engineering basis, and "fusion energy" denotes thermal/fusion power not net electrical output
- `knowledge/concept_research/27-polywell/iter-03/sources/arxiv-2508-06761/output.md` — arXiv landing page for Park 2025 (abstract only); confirmed submission date August 2025; no additional quantitative data beyond the abstract
- `knowledge/concept_research/27-polywell/iter-01/sources/polywell-technical-details/output.md` — Wikipedia article (older extraction); provides experimental history WB-1 through WB-X, operating principle, critics (Rider, Nevins), University of Sydney 2019 negative results; no electrical design point for any machine
- `knowledge/concept_research/27-polywell/iter-01/sources/emc2-website-summary/output.md` — EMC2 corporate website summary; minimal content; no technical specifications or electrical output figures
- `exploration/concept_analysis/analyses/27-polywell/analysis.md` — existing D1+ analysis (used for orientation and cross-checking candidate inventory only); noted that the ~300 MWe net electric figure appearing in Section 5 is analyst-derived inference (980 MW × assumed 40% thermal efficiency − assumed recirculating power losses), not a number stated in any source document

## 2. Candidates surfaced

**Candidate A — Park et al. (2025) D-T reactor design (arXiv:2508.06761, Section 4)**

The only reactor-scale design document in the Polywell portfolio. Park et al. present a physics-scaling study for a compact Q>10 D-T Polywell device:

- Geometry: 1.6 m cube side length; plasma volume ~4.1 m³
- Fuel: D-T (50:50 mixture)
- Boundary magnetic field: 4.5 T at coil surface
- Ion temperature: 20 keV
- Electron beam input: 60 keV, 1.3 kA, steady-state; total input power 78 MW (at γ=0.1)
- Fusion power: ~980 MW (computed from D-T reactivity at 20 keV and stated density/volume)
- Q = 10.5 (at γ=0.1 loss reduction factor)
- Maturity: physics-scaling paper; no engineering design, no blanket specified, no power conversion cycle, no thermal efficiency stated

**P_native (net electrical output): Not stated.** The paper gives fusion power (980 MW) and input power (78 MW) but does not include a power conversion system, thermal cycle, or electrical output calculation. Deriving P_native requires adding thermal efficiency (wholly absent — no blanket type, coolant, or thermodynamic cycle is specified) and beam supply efficiency (also absent). Both parameters must be borrowed entirely from MFE analogues not present in any Polywell source. The ~300 MWe figure in the existing analysis.md is an analyst calculation using assumed 40% thermal efficiency and 80% beam supply efficiency; it traces to no company source or company-cited paper.

Additionally, the γ = 0.1 assumption underlying the 980 MW fusion power is an explicitly acknowledged free parameter: "currently, we lack a quantitative model for the reduction in the loss rate." This means the fusion power itself is a scenario projection with an unvalidated input — compounding the derivation gap for any electrical output estimate.

**Candidate B — EMC2 FPNS (Fusion Prototypic Neutron Source), SHINE Technologies partnership (2023 DOE proposal)**

- Plasma radius: 8.5–10 cm; fuel: D-T; fusion power: 350 kW steady-state; ion beam: 5–6 MW at 150–200 keV; boundary field: 2–3 T; R&D cost: $20M / 24 months
- Purpose: produce 10 dpa/cy neutron flux for fusion materials testing

**P_native: None.** The FPNS is a neutron-production device by explicit design; no electrical generation is intended or described. Disqualifies as a design point under the selection rule.

**Candidate C — Informal ~100 MW fusion energy estimate (TheFusionReport 2025, Dave Mansfield / EMC2)**

From the interview paraphrase: "a system with coils roughly 2 meters in diameter should theoretically be able to generate 100 megawatts (100 MW) of fusion energy."

**P_native: None.** The 100 MW figure refers to fusion (thermal) power, not net electrical output. The remark is a journalist paraphrase of an informal EMC2 statement, specifies only coil diameter with no density, field strength, or fuel, and carries no engineering architecture. It does not constitute a design point under any confidence tier.

**Note on fuel discrepancy:** The input specifies `fuel: PB11`, but all current EMC2 reactor-scale documents use D-T. Park et al. (2025) explicitly states that p-B11 R&D (mechanisms M4–M6, including non-thermal plasma operation) has been suspended. The FPNS uses D-T neutrons. No p-B11 Polywell reactor design with a stated P_native exists in the saved source corpus. The Rogers (2018) paper (J. Fusion Energy 37, 1–17), which reportedly describes a p-B11 Polywell reactor, is referenced in the dossier's key sources list but is not saved as an extracted source and could not be evaluated for a P_native figure.

## 3. Selection

All three candidates lack a P_native traceable to any source. Candidate A (Park 2025) is the most sophisticated document in the portfolio and the only one at reactor scale, but it is a physics scaling study that computes fusion power and Q without specifying a power conversion pathway or electrical output. Reaching a net electrical output number requires two unspecified parameters (thermal efficiency, beam supply efficiency) that must be imported wholesale from MFE analogues — this goes beyond back-of-envelope projection into pure analyst construction with no anchor in a company source. Candidate B (FPNS) is a neutron source with no electrical output by design. Candidate C (100 MW informal) refers to fusion power, not electrical output, and has no engineering architecture behind it.

```yaml
proposal:
  concept_id: 27-polywell
  route_to_freeform: true
  reason: |
    The Park et al. (2025) reactor design (arXiv:2508.06761) is the only reactor-scale Polywell
    document and gives fusion power (~980 MW at γ=0.1) and plasma gain Q=10.5, but does not
    state a net electrical output anywhere in the paper. Reaching a P_native requires adding
    thermal efficiency (no blanket, coolant, or thermodynamic cycle is specified in the paper)
    and beam supply efficiency (also absent) — both are MFE-analogue assumptions not traceable
    to any company source or company-cited paper. The FPNS device (350 kW fusion, 5–6 MW ion
    beam input) is a neutron-production facility with no electrical output by design. The
    informal "~100 MW of fusion energy" remark in the TheFusionReport 2025 interview refers to
    fusion thermal power for a notional ~2 m coil system, not electrical output, and carries no
    engineering architecture. No Polywell design in the source portfolio states a P_native.
  designs_considered:
    - design: "Park et al. (2025) 1.6 m Polywell Q=10 D-T reactor (arXiv:2508.06761, Section 4)"
      reason_no_p_native: "Physics scaling study; states fusion power (980 MW, γ=0.1 free parameter) and input power (78 MW) but specifies no power conversion system, thermal cycle, blanket type, or net electrical output — deriving P_native requires adding two unspecified parameters (thermal efficiency, beam supply efficiency) with no anchor in any source"
    - design: "EMC2 FPNS — Fusion Prototypic Neutron Source (2023 DOE program proposal, SHINE Technologies partnership)"
      reason_no_p_native: "Neutron-source device by design; 350 kW fusion power; no electrical generation intended or described"
    - design: "Informal ~100 MW fusion estimate (TheFusionReport 2025 interview, Dave Mansfield / EMC2)"
      reason_no_p_native: "Refers to fusion (thermal) power for a notional ~2 m coil system; journalist paraphrase with no engineering architecture; does not constitute an electrical design point"
```

## 4. Open questions

- **Fuel discrepancy:** The input row specifies `fuel: PB11`, but all available reactor-scale EMC2 sources commit to D-T (Park 2025 explicitly suspends p-B11 R&D). If concept row 27-polywell is intended to represent a p-B11 Polywell variant, the Rogers (2018) paper (J. Fusion Energy 37, 1–17; not in the saved source corpus) should be retrieved and evaluated — it reportedly describes a p-B11 reactor. Even so, p-B11 represents a formally abandoned EMC2 direction, and neither a D-T nor a p-B11 Polywell currently has a P_native in any saved source.

- **What would unblock a design-point pick:** An EMC2 engineering document that specifies (a) a power conversion cycle type and its efficiency for the Park 2025 reactor geometry, and (b) the resulting net electrical output, would immediately enable a `grounding_confidence: low` selection at approximately 250–350 MWe (the plausible range from standard MFE thermal efficiency assumptions). The physics parameters in Park 2025 are sufficient; only the thermal-conversion step is missing from any source. The FPNS program's go/no-go decision (Task 5 of the 2023 proposal) would also constrain γ experimentally — a validated γ would sharpen the fusion power projection from which P_native could eventually be derived.

- **Rogers (2018) p-B11 design:** If the Rogers 2018 paper (not in the source corpus) states a net electrical output for a p-B11 Polywell reactor, it could change the answer for a p-B11 concept row — but given EMC2's formal suspension of p-B11 work, any design point from that paper represents a path the company has abandoned. Worth retrieving if the concept row is explicitly scoped to p-B11.

- **Scalability of the Park 2025 result:** The paper notes "a reduction in confinement time of up to a factor of 10 can be compensated by increasing the reactor size and/or magnetic field strength," implying design-point variations at larger geometries are on the table. If a future EMC2 document specifies a revised geometry with a stated electrical output, the Park 2025 design (1.6 m cube) should be treated as a baseline candidate among alternatives rather than as the sole reference.

---

**Routing decision:** `route_to_freeform: true`. The blocking gap is not physics data — it is the absence of a power conversion specification from any source. Park 2025 provides fusion power, input power, and geometry, but the step from fusion power to net electrical output requires thermal efficiency and beam supply efficiency assumptions that are wholly absent from the Polywell source corpus. That two-step inference is not "a back-of-envelope number" from the source; it is the analyst supplying two free parameters with no grounding. The row exists in the comparison framework but will carry an explicit freeform flag until an EMC2 engineering document specifies how the thermal power becomes electricity.