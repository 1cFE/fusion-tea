# Design Point Reasoning Trace — 20b-renaissance-stellarator

## 1. Sources walked

- `knowledge/concept_research/20b-renaissance-stellarator/dossier.md` — synthesized concept summary; confirms 1 GWe target, R ≤ 4 m, A ≈ 4, B = 10 T nominal, D-T fuel, Q = ∞, 34% net plant efficiency; cites the three peer-reviewed papers as key sources
- `knowledge/concept_research/20b-renaissance-stellarator/iter-01/sources/infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md` — J. Nuclear Materials 599 (2024) 155239 (Prost et al.); blanket/neutron management paper; Table 1 caption explicitly states "a cost-effective high-field compact fusion power plant delivering 1 GWe" with R = 3.8 m, A = 4.1, B = 10.2 T; provides independent confirmation of all key geometry and power parameters
- `knowledge/concept_research/20b-renaissance-stellarator/iter-01/sources/infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/images/tmpaupvkstl.pdf-0002-02.png` — schematic figure from JNM blanket paper; shows single compact stellarator device with 4-field-period cylindrical HTS magnet architecture; confirms single machine, not multi-module
- `knowledge/concept_research/20b-renaissance-stellarator/iter-01/sources/ukaea-process-fusion-devices-stellarator/output.md` — UKAEA PROCESS stellarator documentation; no independent systems-code study of this concept exists within it
- `knowledge/concept_research/20b-renaissance-stellarator/iter-01/sources/arxiv-1512-01930/output.md` — Senatore et al. 2015 REBCO conductor characterization; irrelevant to design-point selection
- `exploration/concept_analysis/analyses/20b-renaissance-stellarator/analysis.md` — existing D1+ analysis; used as reference for source inventory and parameter cross-check only

## 2. Candidates surfaced

**Candidate A — 1 GWe economically optimized compact liquid-wall HTS stellarator (Nuclear Fusion 64 (2024) 026007)**

Published parameters across three peer-reviewed papers:
- Net electrical output: 1 GWe (stated in NF design paper; confirmed in JNM blanket paper and ECM power conversion paper)
- R = 3.8 m, A = 4.1, B = 10.2 T (confirmed in JNM blanket paper Table 1)
- Fuel: D-T
- Net plant efficiency: 34% (ECM paper); sCO₂ cycle efficiency 49–51%
- Blanket: integrated flowing liquid Li-LiH (10 cm Pb + 22 cm Li-LiH)
- Q target: ∞
- Architecture: single machine with 4-field-period segments — these are toroidal field-period segments of one machine, not independent generating modules

P_native: 1000 MWe (the whole machine). Maturity: paper-concept.

**Candidate B — 6 T Helmholtz magnet demonstrator (MT29 Abstract, 2024)**

Physics demonstrator: 6 T Helmholtz, 1.2 m diameter, 20 K. No electrical output by design. Not a design candidate.

## 3. Selection

Candidate A is the only viable design point. Renaissance Fusion is a single-concept company; no pilot, near-term intermediate machine, or named alternative commercial plant appears in any source.

The 4-cylinder architecture note: the JNM paper models "one cylinder to account for the 4-field period symmetry" — these are 4 toroidal segments of a single machine, not 4 independent generating modules. P_native is the whole-machine net output.

```yaml
proposal:
  concept_id: 20b-renaissance-stellarator
  design_name: "1 GWe economically optimized compact liquid-wall HTS stellarator (Samulski et al., Nuclear Fusion 64 (2024) 026007)"
  maturity_tier: paper-concept
  grounding_confidence: high
  p_native_mwe: 1000
  primary_sources:
    - knowledge/concept_research/20b-renaissance-stellarator/iter-01/sources/infoscience-bitstreams-7d2d7b2f-6f75-4ac2-93cb-6eef8a65df82/output.md
    - knowledge/concept_research/20b-renaissance-stellarator/dossier.md
  selection_rationale: |
    The only design in Renaissance Fusion's published portfolio with a stated net
    electrical output is the 1 GWe economically optimized machine from Nuclear Fusion
    64 (2024) 026007. Its key parameters (R = 3.8 m, A = 4.1, B = 10.2 T, D-T fuel,
    1 GWe net) are independently confirmed in the extracted JNM blanket paper (Table 1)
    and the ECM power conversion paper (34% net efficiency). The 4-cylinder architecture
    refers to 4 field-period segments of a single toroidal machine, not 4 independent
    generating modules; P_native is therefore the whole-machine net output of 1000 MWe,
    giving n_mod = 1 at the 1 GWe comparison point.
  alternatives_considered:
    - design: "6 T Helmholtz magnet demonstrator (MT29 Abstract, 2024)"
      reason_rejected: physics demonstrator with no electrical output by design; a magnet validation milestone, not a reactor design candidate
      sensitivity_implication: "n/a — this candidate has no P_native and cannot define a competing design-point branch"
    - design: "(no other commercial or pilot design candidates)"
      reason_rejected: single-design company; no near-term pilot, intermediate machine, or named alternative commercial plant exists in the published record
      sensitivity_implication: "n/a — no alternative P_native exists to probe. If the company publishes a sub-commercial pilot design with a stated net output, that would become an alternative candidate worth comparing against the 1 GWe target."
```

## 4. Open questions

- **NF 2024 paper not extracted as a source file**: The primary design paper (Nuclear Fusion 64 (2024) 026007) is not in `iter-01/sources/` as an extracted file. Its parameters are confirmed via the JNM blanket paper (extracted) and the dossier, but direct extraction would allow firm source-file citations.
- **ECM power conversion paper not extracted**: Energy Conversion and Management 276 (2023) 116572 (Fama et al.) — source for the 34% net efficiency figure — is also not extracted. This figure drives the implied ~2.94 GWth thermal requirement and flows into blanket and BOP sizing.
- **No pilot or near-term machine published**: If Renaissance Fusion publishes a sub-commercial pilot with a stated net electrical output, revisit this selection. A pilot would become a competing candidate and the choice between it and the 1 GWe commercial target would affect the comparison.
- **4-cylinder cost granularity**: If future publications assign per-segment costs or electrical contribution to the 4 field-period segments, that architecture may prove relevant to cost modeling even though it does not change P_native from the plant level.

---

**Key judgments**:
- **`grounding_confidence: high`** — the 1 GWe figure and geometry (R, A, B, fuel) appear across three peer-reviewed papers; the blanket paper (extracted) independently confirms all key parameters in its Table 1. This clears the bar of "documented geometry + power + fuel + at least some engineering parameters." The primary design paper isn't in the source tree as an extracted file, which would normally push toward `medium`, but the blanket paper's independent confirmation of every key parameter from that paper makes `high` defensible here.
- **`p_native_mwe: 1000`** — the machine IS the 1 GWe plant; n_mod = 1. No multi-module ambiguity.
- **`dossier.md` as second primary source** — the NF 2024 design paper is not extracted in `iter-01/sources/`; the dossier is the best available in-tree pointer to it. This is noted as an open question.