---
date: 2026-05-15T14:34:25-04:00
researcher: Claude
topic: "Triple-product based technology-risk framework for cross-concept fusion comparison"
tags: [research, scoring-framework-v2, technology-risk, lawson-criterion, triple-product, c7]
status: complete
last_updated: 2026-05-15
---

# Research: Triple-Product Technology-Risk Framework

**Date**: 2026-05-15
**Researcher**: Claude
**Research Type**: Methodology / Domain
**Reads with:** `.project/concepts/scoring-framework-v2.md`, `exploration/concept_analysis/prompt_templates/config/scoring_framework.md` (C7), `.project/concepts/down_select/concept_part2.md` (Stage 1 timeline note)

---

## Research Question

How do we build a **technology-risk** assessment that:

1. Leverages the **triple product** ($n T \tau_E$ / Lawson criterion) framing,
2. For any concept (fuel + confinement-type pair) measures *how far we are* on the individual physics metrics required for net energy,
3. Works **uniformly across all 38 concepts** (tokamaks, stellarators, mirrors, FRCs, MIF, laser/heavy-ion ICF, muon-catalyzed, acoustic, electrostatic, levitated dipole, …),
4. Is **transparent and objective** enough to defend publicly and localize disagreements?

---

## Summary

- **The triple product is a starting point, not the whole framework.** $n T \tau_E$ is the canonical Lawson scalar for MCF in thermal equilibrium. It does not naively transfer to ICF (where hot-spot $\rho R$ and isobaric gain $G$ are the natural metrics), to pulsed MIF (compression-time-limited burn fraction), or to non-Maxwellian/non-thermal concepts (muon catalysis, beam-driven, acoustic, electrostatic). A uniform framework must (a) keep the *meaning* of "gap to ignition" while (b) substituting the physics-regime-appropriate scalar.
- **The Wurzel & Hsu 2022 "generalized Lawson parameter" is the strongest existing precedent** and should anchor the framework. It normalizes MCF, MIF, and ICF onto a single $n T \tau^*$-style axis using a regime-appropriate $\tau$, plotting "scientific gain" $Q_{\text{sci}}$ vs. Lawson parameter on a log-log chart that has slots for every fusion experiment in history. It directly solves the cross-concept comparability problem and is peer-reviewed.
- **Recommend a three-quantity decomposition per concept**, not a single scalar: (1) design-target Lawson parameter, (2) best demonstration in the concept's lineage, (3) best demonstration globally. The three gaps that fall out — *design-to-ignition*, *demo-to-ignition*, *demo-to-design* (the proponent's extrapolation burden) — are individually disputable and individually citable.
- **For concepts outside the Lawson framework** (muon, acoustic, exotic hybrids), the framework should not force a fit. Instead, it assigns those concepts to an *off-chart* tier and substitutes a regime-specific surrogate (muons: $N_{\text{fus}}/\text{muon}$ vs. $E_\mu$; acoustic: any positive gain demonstration). These concepts inherit a uniform "no Lawson analogue → maximum physics extrapolation" penalty, which is both honest and uniform.
- **This drops cleanly into the V2 architecture.** The triple-product framework is a *bundle of embeddings* (Layer 2) over a small set of plasma-physics features (Layer 1) and a shared evidence corpus of demonstrated experimental records (Wurzel-Hsu table + Lindl ICF gain curves). It naturally subsumes the current C7-F1 evidence-tier judgement and replaces the hand-set heritage-credit floors with values *derived* from lineage best-demonstrated parameters.
- **The current codebase has the risk-grading scaffolding but is missing the physics-baseline data layer.** `table.csv` has zero physics-performance columns. C7-F1 cells today record plant-requirement vs. best-demonstrated in prose, with citation, but inconsistently and per-concept. A *shared* evidence corpus turns those scattered citations into a single normalized chart everyone references.

---

## Detailed Findings

### 1. What the codebase has today

**C7 Technical Risk Evidence** (`scoring_framework.md`):

- 7 functions × 2 subcategories (physics/hardware) = 14-cell matrix.
- Each cell requires: plant requirement, best demonstrated, gap ratio, classification (binary/degrading), evidence tier 1–5.
- Heritage credit floor on F1–F7 by lineage (Tokamak/Stellarator 4.0, Laser IFE 3.5, Mirror/FRC 2.5, Spherical Tokamak 3.0, …). **D-T fuel only.**
- Evidence tiers anchored to operating regime: Tier 5 (commercial-scale operating demonstration in same fuel/T/p/flux/duty) down to Tier 1 (asserted/absent).

What this gives us: a *qualitative* gap framework, with citation requirements at tier ≥3. What it lacks:

- A normalized cross-concept axis. Gap ratios are per-cell and per-concept; there is no single number that lets a reviewer say "concept A is 3× further from ignition than concept B."
- Determinism. The mapping from "JET 1997 D-T at 11 MW for 4 s" to "tier 4 for steady-state D-T tokamak" is judgement embedded in each LLM scoring pass, not a rule.
- Uniform treatment across concept families. Heritage floors are hand-set integers per family, not derived from the best demonstrated parameter in each lineage.

**Stage 1 timeline note** (`concept_part2.md`): descriptive, not evaluative. Records "current Q achieved, distance to Stage-2-ready commercial regime, paradigm co-development depth." Deliberately *does not score*. The triple-product framework would slot in here as a quantitative companion to the timeline note — not changing the methodology's stance that Stage 1 does not gate, but giving the descriptive note a defensible numerical anchor.

**Per-concept synthesis files** carry the data points unevenly:

- `01-hts-compact-tokamak`: rich (peak field, normalized power, H factor, bootstrap fraction).
- `06-magnetic-mirror`: thin (DEC efficiency assumed, no measured $n T \tau$).
- `16-muon-catalyzed-fusion`: explicit but inside a cost model, not a physics benchmark.
- `12-levitated-dipole`: cites OpenStar's $Q_{\text{sci}}=15$ target and an arXiv triple-product scaling argument.

No file consistently records the three quantities the framework needs: design target, lineage best demo, global best demo.

### 2. The triple product, generalized: what "Lawson parameter" means across regimes

The textbook Lawson criterion for D-T ignition (50:50, alpha self-heating) is:

$$
n_e T_i \tau_E \gtrsim 3 \times 10^{21} \;\; \text{keV} \cdot \text{s} / \text{m}^3 \quad (\text{minimum near } T_i \approx 14 \text{ keV})
$$

The threshold *function* $n T \tau_{\text{ign}}(T_i, \text{fuel})$ shifts strongly by fuel:

| Fuel | Approx. min $n T \tau$ for ignition | Optimum $T_i$ | Source |
|---|---|---|---|
| D-T | $\sim 3 \times 10^{21}$ | $\sim 14$ keV | Wesson, Lawson 1957 |
| D-D | $\sim 5 \times 10^{22}$ | $\sim 50$ keV | Atzeni & Meyer-ter-Vehn |
| D-He3 | $\sim 1.5 \times 10^{22}$ | $\sim 60$ keV | Atzeni & Meyer-ter-Vehn |
| p-B11 | $\sim 3 \times 10^{23}$ (with $T_e \ll T_i$ caveat) | $\sim 150–300$ keV | Nevins 1998; Putvinski 2019 |

These threshold curves are *the* reference surface against which every concept should be measured.

For ICF, hot-spot ignition replaces $\tau_E$ with the *inertial confinement time* $\tau_{\text{ICF}} \sim R / c_s$ (sound-speed transit), and the operative form is $\rho R \cdot T$ (areal density × temperature). Lindl 1995/2004 gives ignition contours of $(\rho R, T_{\text{hot-spot}})$ for D-T at hot-spot ignition. The NIF Aug-2022 and Dec-2022 shots ($Q_{\text{sci}} = 0.72$ and $1.54$) sit on a known point of this chart.

**Wurzel & Hsu 2022** ("Progress toward fusion energy breakeven and gain as measured against the Lawson criterion," *Physics of Plasmas* 29, 062103) builds the unifying chart: a log-log plot of $Q_{\text{sci}}$ vs. *generalized Lawson parameter* (or $n T \tau$ proxy), populated with ~50 experiments across MCF, MIF, ICF. Every fusion experiment has a known $(Q_{\text{sci}}, n T \tau)$ pair on this chart. It is the natural reference frame for "how far away are we."

### 3. Proposed framework: three options ranked

#### **Option A (recommended): Wurzel–Hsu normalized chart, with per-fuel ignition thresholds**

**Per-concept inputs** (Layer 1 features, fixed schema):

```yaml
plasma_physics:
  fuel: D-T | D-D | D-He3 | p-B11 | muon-catalyzed | other
  confinement_regime: thermal-MCF | thermal-ICF | non-thermal | hybrid
  design_target:
    T_i_keV: <number>            # design ion temperature
    n_m3:   <number>             # design density (peak for ICF, volume-avg for MCF)
    tau_s:  <number>             # energy confinement time (MCF) OR inertial time (ICF)
    Q_sci_design: <number>       # scientific gain at design
    rhoR_kg_m2: <number, ICF only>
  best_demo_lineage:             # best demonstration in this confinement family + fuel
    experiment_id: <evidence-corpus-ref>
    T_i_keV: ...
    n_m3: ...
    tau_s: ...
    Q_sci_demo: ...
  best_demo_global: <evidence-corpus-ref>   # best demonstration anywhere on this physics regime
```

Every numeric field is provenance-tagged (proponent-claimed / physics-derived / analyst-estimate), per the V2 contract.

**Shared evidence corpus** (one artifact, referenced by ID):

- The Wurzel–Hsu chart points: ~50 experiments with $(T_i, n, \tau, Q_{\text{sci}}, \text{fuel})$ each.
- Ignition-threshold functions per fuel: $n T \tau_{\text{ign}}(T_i, \text{fuel})$ from Lawson/Wesson/Atzeni references.
- ICF gain curves: $(\rho R, T_{\text{hot-spot}}) \to G$ from Lindl 2004 / NIF post-shot analyses.

This corpus is *cited once* and referenced by ID from every concept's features. Drift is impossible by construction.

**Embeddings** (Layer 2, deterministic):

| Embedding | Definition | Units |
|---|---|---|
| `lawson_design` | $\log_{10}(n T \tau)_{\text{design}}$ | unitless log |
| `lawson_demo_lineage` | $\log_{10}(n T \tau)_{\text{lineage best demo}}$ | unitless log |
| `lawson_ignition` | $\log_{10} n T \tau_{\text{ign}}(T_i^{\text{design}}, \text{fuel})$ | unitless log |
| `gap_design_to_ignition` | `lawson_ignition − lawson_design` | log-decades |
| `gap_demo_to_ignition` | `lawson_ignition − lawson_demo_lineage` | log-decades |
| `extrapolation_burden` | `lawson_design − lawson_demo_lineage` | log-decades |
| `Q_sci_demo_lineage` | scalar from corpus | unitless |
| `Q_sci_design` | from feature | unitless |
| `regime_match_flag` | does the demo's regime match the design's (steady vs. pulsed, fuel, magnetization)? | bool |
| `tech_risk_F1_tier` | piecewise mapping of (`gap_demo_to_ignition`, `extrapolation_burden`, `regime_match_flag`) to a 1–5 tier | int |

The piecewise map is the only place judgement lives, and it lives in **one rule for all concepts**, not 38 separate LLM passes. Example breakpoints (for spec discussion, not pinned here):

- gap ≤ 0.3 dec **and** regime match → tier 5 (operating-regime demonstrated)
- 0.3 < gap ≤ 1.0 dec **and** regime match → tier 4 (near-regime)
- 1.0 < gap ≤ 2.0 dec **or** adjacent regime → tier 3 (subscale/partial)
- gap > 2.0 dec → tier 2 (design/extrapolation only)
- no demo of *any* concept-relevant point → tier 1

This makes today's qualitative tier scale into a deterministic function.

**Score layer** (Layer 3): `tech_risk` is a weight matrix over (gap_design_to_ignition, gap_demo_to_ignition, extrapolation_burden, Q_sci_design), trivially recomputable. A scenario like `bet:HTS_extrapolation_underwritten` could downweight `extrapolation_burden` for HTS-tokamak concepts; `bet:p-B11_kinetic_effects_recovered` could downweight `gap_demo_to_ignition` for p-B11.

**Heritage credit replacement.** The current hand-set floor (Tokamak = 4.0, Mirror = 2.5, …) becomes a *derived* quantity: it is exactly $f(\text{lawson_demo_lineage} \text{ vs. } \text{lawson_ignition})$. Tokamaks score high because JET-DT and ITER baseline give them small `gap_demo_to_ignition`; mirrors score low because TMX/MFTF demonstrated a much smaller Lawson product. The asymmetry the current heritage table encodes survives, but it is now defensible from data, not stipulated.

**Why this is the strongest option:** every contested value resolves to a specific number in either (a) the concept's design target (proponent-cited), (b) the evidence corpus (peer-reviewed citation), or (c) the ignition-threshold formula (textbook). Disputes localize to one of three places, and each place has an external citation chain.

#### **Option B: per-metric vector ($n$, $T$, $\tau$ separately)**

Each plant requirement is decomposed into separate features and gaps:

- `gap_T` = log10(T_design / T_demo_lineage)
- `gap_n` = log10(n_design / n_demo_lineage)
- `gap_tau` = log10(τ_design / τ_demo_lineage)

**Strength:** More information; the framework reveals *which* parameter is the bottleneck. A reviewer can say "the temperature extrapolation is fine, but the confinement time gap is two decades."

**Weakness:** The three gaps trade off in non-additive ways. The Lawson criterion is the *product* — you can win by raising any factor — so separating them and adding them in a weight matrix loses physics. Also, ICF and MCF don't share the same $n, T, \tau$ axes (ICF density is ~$10^{31}$/m³ for ~$10^{-10}$ s; MCF is $10^{20}$ for seconds; the product is comparable but the factors aren't). This forces ICF concepts onto inappropriate per-factor scales.

**Verdict:** Use this *inside* Option A as a diagnostic readout (which factor is driving the gap), not as the primary score axis.

#### **Option C: physics-regime-appropriate scalar per concept**

Each concept picks its own metric:

- MCF: $n T \tau_E$
- ICF: $\rho R \cdot T$ + $Q_{\text{sci}}$
- Muon-catalyzed: $N_{\text{fus}}(\mu) \cdot Q_\mu / E_\mu$
- Acoustic / electrostatic / exotic: any breakeven demonstration; "no Lawson analogue" tag

**Strength:** Honest about the diversity of physics. Each concept is judged on its own native metric.

**Weakness:** Loses comparability — the whole point of the user's request. A reviewer can't see whether muon-catalyzed at $E_\mu = 1.5$ GeV is "closer" to viability than a $\rho R = 0.5$ g/cm² ICF target.

**Verdict:** Adopt as the *fallback* for concepts that don't fit Option A. Concepts that fit go on the Wurzel–Hsu chart; concepts that don't get a regime-specific scalar and a uniform "off-chart" penalty.

#### Recommendation

Adopt **Option A with Option B as diagnostic readout and Option C as fallback for non-Lawson concepts.** That is:

1. Default: place every concept on the generalized Lawson chart using the Wurzel–Hsu construction.
2. For each MCF/ICF/MIF concept, additionally report the three per-factor gaps (Option B) as a transparency artifact — they don't enter the score but they sit next to it.
3. For concepts without a Lawson analogue (muons, acoustic, electrostatic confinement, certain hybrids), use a per-concept fallback metric (Option C) and pin them at the "off-chart / maximum physics extrapolation" floor. This is *uniform* across the off-chart set: they all carry the same baseline penalty, with the regime-specific metric used only for tie-breaking.

### 4. Mapping each concept family to the framework

| Family | Concepts | Primary metric | Demonstrated benchmark to cite |
|---|---|---|---|
| Conventional/Compact Tokamak (D-T) | 01, 21, 28, 29, 33, 34 | $n T \tau_E$ | JET 1997 D-T peak; JT-60U equiv-DT; ITER projected baseline |
| Stellarator (D-T) | 05, 09, 10, 20a, 20b, 36 | $n T \tau_E$ | W7-X long-pulse + LHD high-density |
| Spherical Tokamak | (subset of 01-family) | $n T \tau_E$ | MAST-U, NSTX-U; STEP projected |
| Magnetic Mirror | 06, 11 | $n T \tau_E$ | TMX, GAMMA-10, MFTF-B; very large gap |
| FRC / Compact Pulsed MFE | 08, 15, 18 | $n T \tau_E$ (transient) + sustainment evidence | TAE C-2W, FRX-L; LSX confinement |
| Levitated Dipole | 12, 19 | $n T \tau_E$ | LDX (high-β, modest $\tau$); RT-1 |
| Laser IFE (D-T) | 17a, 17b, others | $\rho R T$, $Q_{\text{sci}}$ | NIF 2022 (Q=1.54); LMJ; SG-III |
| Laser IFE (alt-fuel) | 03 (D-D), 04 (p-B11) | $\rho R T$, hot-spot T | NIF for D-T baseline; HB11 lab claims for p-B11 |
| MIF / MagLIF / MTF | 07, 14, 22 | hybrid $n T \tau$ + $\rho R$ | Z-machine MagLIF (~10¹⁸ neutrons); General Fusion stated $n T \tau > 10^{21}$ target |
| Sheared-Flow Z-pinch | 15 | $n T \tau$ during pinch | FuZE pinch + sustainment data |
| Muon-catalyzed | 16 | $N_{\text{fus}}(\mu) \cdot Q_\alpha / E_\mu$ | TRIUMF/RIKEN $N_{\text{fus}} \sim 100$; $E_\mu \sim 4-6$ GeV best |
| Acoustic / Electrostatic / Exotic | 02, 13, 24, 25, 27, 35 | "off-chart" | no published peer-reviewed positive net-energy demonstration |

This mapping is itself a deliverable — it sits in the framework spec, not in each concept dossier.

### 5. Transparency & objectivity controls

The framework is publicly defensible to the extent that each numeric output traces to a citable input. Concretely:

1. **Every demonstrated benchmark is a corpus entry**, not prose. Two concepts citing JET 1997 cite *the same* corpus row.
2. **The ignition threshold is a function call, not a value.** $n T \tau_{\text{ign}}(T_i, \text{fuel})$ comes from a peer-reviewed reference; updating the threshold is updating the function in one place.
3. **Per-concept claims are proponent-tagged.** Design targets cited from the proponent are flagged; physics-derived (e.g., recomputed from claimed plant power and volume) are flagged separately.
4. **Three contestable axes per concept**: design target value, demo benchmark value, threshold value. A reviewer can dispute exactly one and the others stay.
5. **No LLM in the scoring loop.** The Lawson embedding is closed-form arithmetic over the three inputs. (LLM use is permitted *only* in feature extraction from synthesis prose into the structured schema, under the V2 reproducibility contract.)
6. **Heritage credit is derived, not stipulated.** The current floor table becomes a *consequence* of where each lineage's best demo sits on the Wurzel–Hsu chart, removing one of the most-contested judgement calls in the current framework.

### 6. Open questions and risks

1. **Non-thermal regimes inside the Lawson framework.** p-B11 with $T_i \gg T_e$, FRCs with field-reversed equilibria, and beam-driven concepts all "live on" the chart but with caveats. The framework should record a `regime_caveats` flag per concept, and the piecewise tier map should treat unflagged → flagged as one tier of penalty by default.
2. **ICF–MCF unit reconciliation.** Wurzel–Hsu uses a generalized $\tau^*$ to make both fit one axis; the spec must pin the exact formula and reference. Different formulations (Wurzel–Hsu vs. Betti et al.) give slightly different placements.
3. **What "best demo lineage" means** when a concept's lineage is contested (e.g., is HB11's p-B11 lineage the LULI lab shots or every p-B11 calculation back to Nevins?). The corpus needs a `lineage_tag` field to make this explicit.
4. **Heritage floor as derived value: edge cases.** Polywell, dipole, muon-catalyzed all have lineages with extremely poor best-demos — the derived floor will be very low. That is *honest* but may produce score collapse for whole concept families. The Stage 1 timeline-note framing (no gating) is the right counterweight; the framework should preserve the V2 stance that score-collapse on physics risk doesn't auto-kill a concept.
5. **Interaction with the Stage 2/3/4 stage-gate methodology.** The triple-product framework lives at Stage 1 in `concept_part2.md` terms — it's a physics-maturity readout. It does not feed Stage 2/3/4 failure modes (FOAK affordability, chasm-crossing, learning-curve descent). The doc that ships should be explicit that triple-product gap is *one input* to the timeline note, not a replacement for any Stage 2+ analysis.
6. **What to do for the explicitly "magic" concepts** (acoustic, certain electrostatic). They are uniformly assigned the off-chart floor. This is a feature, not a bug — but the methodology needs a short defense paragraph for why "off-chart" is a single category and not, e.g., five sub-tiers of speculation.
7. **Living vs. snapshot corpus.** Wurzel–Hsu 2022 is current as of writing; NIF, SPARC, JT-60SA continue to produce new chart points. The corpus needs a `last_synced` field and a refresh cadence.

### 7. Where this slots into V2

Mapping directly to `scoring-framework-v2.md`:

- **Feature schema additions:** the `plasma_physics` block above. Becomes one of the first concrete sections of the V2 feature spec.
- **Evidence corpus seed:** Wurzel–Hsu 2022 chart points + Lawson/Lindl threshold functions. This is likely the right first artifact to build — it's bounded (~50–100 entries), peer-reviewed, and immediately useful for every MCF/ICF concept.
- **Embedding rulebook additions:** the 10 embeddings in the table above. All deterministic, all closed-form (the tier piecewise map is the only judgement, and it's the same rule for every concept).
- **Weight matrix:** a starter `tech_risk` dimension with a few candidate scenarios (`bet:HTS_path_underwritten`, `bet:p-B11_kinetic_effects_recovered`, `bet:icf_polar_drive_succeeds`).
- **Carry-forward from V1:** current C7-F1 cells (plant requirement, best demonstrated, gap ratio, evidence tier) become the *output* of the embedding pass — produced deterministically rather than authored by Claude per concept.

This is naturally **(b) evidence-corpus seeding** plus **(c) embedding-rulebook porting** in the V2 decomposition guidance, and it covers the most-contested judgement call (C7-F1) in V1.

---

## Code & Document References

- `.project/concepts/scoring-framework-v2.md:76-145` — V2 three-layer architecture; the proposed triple-product framework is a concrete instantiation of Layers 1–2.
- `exploration/concept_analysis/prompt_templates/config/scoring_framework.md` (C7 section) — current evidence-tier methodology to be replaced/grounded.
- `.project/concepts/down_select/concept_part2.md` — Stage 1 timeline note; this framework supplies the quantitative readout the timeline note currently lacks.
- `.project/concepts/down_select/research_q4_q5.md` — CATF/Woodruff probabilistic costing methodology; analogous "data-sparsity → wider uncertainty band, same point estimate" pattern that the triple-product framework should mirror at the physics layer.
- `exploration/concept_analysis/table.csv` — taxonomy columns (fuel, confinement family, topology, operation mode) sufficient to seed `confinement_regime`; missing all physics-performance columns.
- `exploration/concept_analysis/analyses/*/synthesis.md` — current source for design-target values; the V2 extraction pass will normalize these into the `plasma_physics` block.

## External References (for spec)

- Wurzel, S.E. & Hsu, S.C. (2022). "Progress toward fusion energy breakeven and gain as measured against the Lawson criterion." *Physics of Plasmas* 29, 062103. **The canonical reference for the unified chart.**
- Lawson, J.D. (1957). "Some criteria for a power producing thermonuclear reactor." *Proc. Phys. Soc. B* 70, 6.
- Lindl, J. et al. (2004). "The physics basis for ignition using indirect-drive targets on the National Ignition Facility." *Phys. Plasmas* 11, 339.
- Atzeni, S. & Meyer-ter-Vehn, J. (2004). *The Physics of Inertial Fusion.* Oxford. (ignition thresholds for D-T, D-D, D-He3.)
- Nevins, W.M. (1998). "A review of confinement requirements for advanced fuels." *J. Fusion Energy* 17, 25. (p-B11 thresholds.)
- Putvinski, S. et al. (2019). "Fusion reactivity of the pB11 plasma revisited." *Nucl. Fusion* 59, 076018.
- Wesson, J. *Tokamaks* (4th ed.). (Lawson criterion derivations and threshold curves.)
- Betti, R. et al. — alternative ICF generalized-Lawson formulation, for comparison with Wurzel–Hsu.

## Recommendations

1. **Adopt Option A (Wurzel–Hsu-anchored normalized Lawson chart) as the spec basis** for the technology-risk embedding bundle in V2. Use Option B's per-factor gaps as a diagnostic readout next to the score. Use Option C only for the off-chart concepts.
2. **Spec the `plasma_physics` feature block first** (section 7 above) — it's the smallest unit that unblocks both the evidence corpus and the embedding rulebook.
3. **Seed the evidence corpus from Wurzel–Hsu 2022**, then add Lindl 2004 ICF gain curves and Atzeni/Nevins per-fuel ignition thresholds. ~50–100 corpus entries gets full coverage of MCF + ICF + MIF.
4. **Replace the hand-set heritage-floor table with a derived computation** from each lineage's best-demo Lawson parameter. Validate against the current table — large divergences are signals worth investigating.
5. **Keep the Stage 1 / Stage 2-3-4 boundary intact.** The triple-product framework feeds Stage 1's timeline note. It does not gate, score-collapse, or supersede the Stage 2/3/4 stage-gate trace in `concept_part2.md`.
6. **Pre-commit to an off-chart penalty for non-Lawson concepts** with a one-paragraph defense, so the framework's stance on muon/acoustic/exotic is established before per-concept scoring begins.

## Next Steps

1. Author a spec (`/_my_spec`) for the `plasma_physics` feature block + Wurzel–Hsu evidence corpus, scoped to "produce a single chart placing all 38 concepts with citations."
2. In parallel, draft the embedding rulebook entries (10 embeddings listed above) — these are independent of the corpus content.
3. Pick 3 test concepts spanning the regimes (e.g., 01 HTS-tokamak, 04 laser p-B11 ICF, 16 muon-catalyzed) and walk them through the framework manually. Goal: confirm the three-quantity decomposition produces a defensible numeric output for each, and that the off-chart fallback is acceptable for the exotic case.
4. Decide the disposition of the current C7-F1 cells: deprecate, auto-generate from embeddings, or keep as a separate qualitative companion.
