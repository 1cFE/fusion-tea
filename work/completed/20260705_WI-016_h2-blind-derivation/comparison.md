# WI-016 H2 Probe — Comparison: blind-derived relations vs 1costingfe

The derivation phase produced three relations blind from the research corpus (`derivation.md`, frozen). This document compares them against 1costingfe (the held-out answer key) at the concept 01 (ARC-class tokamak) and 20a (Infinity Two stellarator) design points, adjudicates every divergence, and gives the H2 verdict.

**How this was evaluated.** `comparison/compare.py` implements the derived relations verbatim and calls 1costingfe directly (same editable install the concept analyses use, at `~/1cfe/1costingfe`). Outputs: `comparison/results.json` (point values), `comparison/grid.csv` (R × B0 sweep). Answer-key formulas were also reproduced closed-form and checked against the live model to the last digit (coil formula check matches `C220103` exactly).

One version note up front: the recorded concept-01 output (`model_output.txt`) shows computed C220103 = $567M; the current library gives $508.4M. Same formula — the coil-bore radius convention moved from 3.85 m (vessel_or + coil_t + gap2) to 3.45 m (vessel_or). I report both; no adjudication changes.

---

## 1. Point-value comparison

### Concept 01 — ARC-class tokamak (R=3.3, a=1.13, κ=1.84, B0=9.2, Ip=7.8, ⟨n⟩=1.3e20, ⟨T⟩=13.9 keV)

**Fusion power** (forward, at the paper's volume-averaged plasma state, V = 153 m³):

| Source | P_fus [MW] | Basis |
|---|---|---|
| Published (Sorbom 2015) | 525 | full profile calculation |
| Derived, state form (C_prof=1.05) | 407 | quadratic ⟨σv⟩ = 1.1e-24·T² |
| Derived, β form (C_prof=1.05, β_N=2.59) | 522 | 1.20·β_T²·B0⁴·V |
| Answer key `compute_fusion_power` | 432 | Bosch-Hale, flat profile (tokamak.py:102-114) |

The two flat-profile 0D forms (derived state form, answer key) agree with each other to 6% and both undershoot the paper ~20%, because neither carries profile peaking. The derived β form hits the published value because ARC's β_N is pressure-based and already contains the peaking (⟨p⟩ ≈ 1.13 × 2⟨n⟩⟨T⟩ at ARC's profiles); the C_prof = 1.05 calibration was fitted through that channel. So: derived and answer key have the **same flat-0D core**; the derived model additionally has a channel (β form + C_prof) that reproduces the published number, but the calibration constant is channel-specific, not universal.

**Power balance** (forward, P_fus = 525 MW, P_aux,coupled = 38.6 MW, η_th = 0.40, η_wp = 38.6/69):

| Quantity | Published | Derived (M_n=1.2) | Key, mn=1.2, ARC-matched loads | Key, library defaults (mn=1.1, full loads) |
|---|---|---|---|---|
| P_th [MW] | — | 647.6 | 647.6 | 606.1 |
| P_gross [MW] | ~250 class | 259.0 | 259.0 | 242.4 |
| P_net [MW] | 190 | 189.0 | 189.0 | 135.0 |
| Q_p / q_sci | 13.6 | 13.6 | 13.6 | 13.6 |
| Q_e (= q_eng − 1) | 3 | 2.7 | 2.7 (q_eng 3.7) | 1.26 (q_eng 2.26) |
| f_recirc / rec_frac | — | 0.27 | 0.27 | 0.44 |

With the same M_n and the same load scope, derived and answer key agree to **0.01 MW** — the accounting structures are the same equation. All of the apparent disagreement is (a) mn 1.1 vs 1.2 and (b) load scope (key defaults add p_cool 13.7 + p_trit 10 + p_house 4 + p_coils 2 + p_cryo 0.5 + p_pump 1 + 3% subsystem, physics.py:294-328; steady_state_tokamak.yaml:23-28).

**Magnet cost:**

| Source | Value | Basis |
|---|---|---|
| ARC paper FOAK fabricated | $5.1–5.2B (2014$) | Table 11: 5730 km REBCO + 4350 t structure at $1.06M/t |
| Derived, ARC-anchored (k_st=20) | conductor $104–207M + structure $4.57B = **$4.67–4.77B** | virial term, E=18 GJ, σ=660 MPa |
| Derived, k_st=7 (physically-loaded bracket) | $1.70–1.81B | same, lower structure multiplier |
| Answer key computed C220103 | **$508M** current / $567M recorded | kAm × $50/kAm × 3.09 markup, conductor-only (cas22.py:427,441-444; costing_constants.yaml:56,73-75) |
| Analyst override (in the concept model) | **$1030M NOAK** | Sorbom $5.15B FOAK × 1.26 CPI × 0.18 learning (model_setup.py:56-100) |
| Derived FOAK total × the override's own NOAK chain | 4.72B × 1.26 × 0.18 ≈ **$1.07B** | independent reconvergence on the override |

The known candidate for category (iv) is confirmed and is the headline result: the derived model's virial structure term reproduces the ARC paper's structure-dominated total to −8%, and pushing it through the same FOAK→NOAK adjustment the analyst used lands within 4% of the $1030M override — the number the answer key could only reach by manual intervention.

**Concept-01 native inverse run** (the answer key's own mode, target 233 MWe): the key back-solves P_fus = 782 MW, T_e = 13.0 keV, n = 1.94e20 (f_GW 0.85), Ip = 8.67 MA (q95 3.5), q_eng 2.94. The derived relations have no inverse mode; run forward at P_fus = 782 they give P_net ≈ 283 MW (fusion-core loads) vs the key's 233 (whole-plant loads) — same mn/load deltas as above, no new physics disagreement.

### Concept 20a — Infinity Two stellarator (R0=12.5, a=1.25, B=9, P_fus,pub=800, P_net,pub=350)

| Quantity | Published | Derived | Answer key (native run, 350 MWe target) |
|---|---|---|---|
| P_fus [MW] | 800 | (no stellarator P_fus relation derived — tokamak closures don't apply) | 992 required |
| P_net at P_fus=800, η_th=0.33 | 350 | 263 (small house loads) / 198 (70 MW house) | — (key needs 992 MW fusion at η_th=0.40 to make 350) |
| Q_p | 40 | 40 | q_sci 40.3 |
| Magnet cost | — | conductor $284–569M + structure $17.6B (k_st=20) | C220103 = $4080M |

Two things worth stating plainly:

1. **Both models say the vendor's 800 MW_fus → 350 MW_e doesn't close** at Rankine-class efficiency with any realistic recirculation. Derived: 800 MW at η_th=0.33 gives at most 313 MW gross. The key demands 992 MW fusion for 350 net. Derived and key agree with each other against the published point — exactly what a cross-check should do.
2. **The key's 20a coil price is internally wrong** (finding, see D13): the stellarator branch prices coils at the YAML calibration field `b_center = 6.0 T` (steady_state_stellarator.yaml:29), not the spec's B = 9 T, because only the tokamak branch derives b_center from B (model.py:1272-1275). At its own intended field the formula gives $6120M, not $4080M — a silent 33% undercount whenever a stellarator design point's B differs from 6 T.

---

## 2. Grid scaling comparison (R ∈ {2.5, 3.3, 4.5, 6} × B0 ∈ {5, 7, 9, 12}, other params fixed at ARC)

Full table: `comparison/grid.csv`. Common closure (Ip from q95=4.20, n = 0.669·n_GW, T = 13.9 keV) so the functional forms are isolated:

- **P_fus ratio derived/key = 0.942 at every one of the 16 grid points.** With T held fixed, quadratic and Bosch-Hale reactivity differ only by a T-dependent constant; the (n, B, R) scaling is *identical* (both ∝ n²V with the same current/density closures available to both).
- **The T dependence is the entire functional difference.** Quadratic/Bosch-Hale ratio: 2.01 at 5 keV, 1.13 at 8, 0.97 at 10, 0.90 at 13.9, 1.02 at 20, 1.48 at 30 keV. This matches the derived relation's own declared validity window (10–20 keV, ~10%) exactly.
- Note on the grid's `beta_N` column: it is key-computed, i.e. **half** the conventional value (see D15). Conventional βN across the grid is 1.76–4.22, so the low-B corner is actually beyond the Troyon limit the key believes it is checking.
- **Closure choice dominates off-design:** the derived model's native Troyon-pinned form (β_N = 2.59 fixed) ranges from 0.36× to 2.05× the specified-density value across the grid, tracking (β_N,actual/2.59)². Not an error — it answers "what would a machine designed at the beta limit do," while the key answers "what does this specified density/temperature do." Different questions, both defensible.
- **Conductor ampere-meters are bit-identical** between derived and key at every grid point when given the same bore (kAm columns equal): the derived N·I·ℓ with ℓ = 2πr_coil *is* the key's G·B·R0·r_coil/μ0 with G = 4π².
- **Structure changes the B scaling:** derived total magnet grows superlinearly in B (structure ∝ B²R) while key C220103 is linear in B (∝ B·R). At R=3.3, derived-structure/key-C220103 goes from 6.1× (5 T) to 14.7× (12 T). The key's own comment concedes the omission: peak-field derating and a B²-structure term are "neither of which is modeled here" (cas22.py:287-289).

---

## 3. Adjudication of divergences

Categories: (i) equivalent within tolerance · (ii) different-but-both-defensible · (iii) one side wrong · (iv) one side captures something the other lacks.

| # | Quantity | Verdict | Adjudication |
|---|---|---|---|
| D1 | Reactivity functional form (quadratic T² vs Bosch-Hale) | **i** | Within 10% on 10–20 keV, exactly as the derivation's validity section claims; derived model self-declared the window and the fallback ("outside it use the full Bosch-Hale form"). Key: layers/reactivity.py; derived: derivation.md step 2. |
| D2 | Profile factor | **iv (derived)** — with a caveat | The key has no profile treatment; at ARC's volume-averaged inputs it underpredicts the published 525 MW by 18%. The derived C_prof + β-form channel recovers it. Caveat: C_prof=1.05 only works through the β channel (ARC's β_N carries the peaking); as a universal constant it is single-point calibrated. |
| D3 | Operating-point closure (Troyon-pinned vs specified n, T) | **ii** | Design-limit closure vs point-evaluation closure. The key's 0D inverse mode additionally back-solves T from a net-power target (tokamak.py:415-639) — a capability the derived relations lack entirely. |
| D4 | Plasma current relation | **i/ii** | Derived q* = 5a²B(1+κ²)/(2RIp) (ARC Eq. 3) vs key Ip = 2πa²κB/(μ0Rq95) (tokamak.py:86-91). Same Ip ∝ a²B/(Rq) skeleton, different shaping convention ((1+κ²)/2 vs κ) and different q definition (q* vs q95). At ARC both reproduce Ip = 7.8 MA with their respective q values (5.0, 4.2). |
| D5 | Power-balance structure | **i** | Mapped term-for-term: with equal M_n and load scope, P_th agrees to 0.02 MW and P_net to 0.01 MW (647.58/647.6, 189.03/189.04). Key: physics.py:288-328; derived: Relation 2. Q_e vs q_eng is definitional (Q_e = q_eng − 1). |
| D6 | Blanket multiplication M_n | **ii** | Key default 1.1 (steady_state_tokamak.yaml:14, from pyFECONs); derived inferred 1.2 by closing ARC's published numbers. For ARC specifically, 1.2 is what closes; as a fleet default 1.1 is defensible. ±7% on P_net. The derivation flagged this as inferred-by-consistency, honestly. |
| D7 | Recirculating-load scope | **ii** | Derived uses ARC's fusion-power-core accounting (aux wall-plug + cryo, ~70 MW); key itemizes whole-plant loads (+31 MW fixed + 3% of gross; yaml:23-28). Derived explicitly warned Q_e "definitions vary by scope" and cited the ~70 MW house load of a large plant. Key q_eng 2.26 vs derived 3.7 at the same physics point is entirely this. |
| D8 | Radiation channel | **iv (key)** | Key computes bremsstrahlung + synchrotron + impurity radiation (p_rad = 23 MW at the ARC point) and routes it through the thermal stream (physics.py:269-303); derived omits radiation. For DT net power the effect is ~nil (radiation lands in the same thermal pool), but the key can split first-wall vs divertor loads and model radiation-dominated fuels; the derived relation cannot. |
| D9 | Conductor cost functional form | **i** | Identical bilinear ampere-meter law. Derived N·I·ℓ_coil/I_tape (validated against ARC's tape inventory to 1%); key G·B·R0·r_coil/μ0 with G=4π² (cas22.py:115-140, 427). kAm identical at all 16 grid points given the same bore. |
| D10 | Conductor cost constants | **ii** | Derived: $27–55/kAm materials, 2014 FOAK, at 23 T/20 K (ARC Table 10). Key: $50/kAm NOAK tape × 3.09 installed markup = $154.5/kAm installed (costing_constants.yaml:56,73-75, SPARC-calibrated). Different cost basis (materials vs installed system), both traceable; not directly contradictory. |
| D11 | Magnet structure term | **iv (derived) — the big one** | Derived carries virial structure (k_st·ρE/σ × $1.06M/t): ARC-anchored $4.57B structure vs paper $5.1–5.2B (−8%). Key is conductor-only ($508M computed) and needed a $1030M analyst override; the derived FOAK total × the override's own NOAK chain = $1.07B, within 4% of the override. The derived model independently produces what the key required manual analyst work for. Counter-caveat: k_st = 20 is calibrated on one machine whose mass basis is conservative (reactor base as solid steel, flagged in the derivation), and extrapolating it to 20a gives $17.6B structure — almost certainly a large overestimate. The *term* is right; the *multiplier* is one-point-calibrated and would need cross-machine calibration before use. |
| D12 | Stellarator penalty | **ii** | Derived: f_3D ≈ 2–5, direction-only, declared "a real insufficiency." Key: path_factor 2 × markup ratio 5.87/3.09 → 3.8× a tokamak per B·R·r (cas22.py:137-138; yaml:73-75, NCSX-overrun-calibrated). The key's number sits inside the derived bracket. |
| D13 | 20a coil field basis | **iii (key wrong)** | The stellarator branch prices coils at YAML `b_center = 6 T`, ignoring the design point's B = 9 T (model.py:1272-1275); concept 20a's C220103 is $4080M but $6120M at its own field. A tokamak spec would not have this trap (b_center := B). Found only because the derived model uses the actual axis field. |
| D14 | Field-dependence of conductor | **iv (derived)** | Derived notes I_tape derates with peak field and B_pk = B0/(1−ε−Δb/R), making cost superlinear in B0; key is linear in B by construction and its own comment concedes the omission (cas22.py:285-289). Matters exactly in the high-field-compact regime the ARC/CFS strategy occupies. |
| D15 | Beta definition | **iii (key wrong)** | Key's `compute_beta_N` computes β_t = μ0·n(T_e+T_i)/B² (tokamak.py:117-126) — exactly **half** the standard β = 2μ0·p/B² that Troyon's βN limit is defined against (ARC Eq. 2; derived Relation 1 closure 1). Verified factor = 2.000 numerically: at the ARC point the key reports βN = 1.15 where the flat-profile conventional value is 2.29 (paper: 2.59). βN does not feed P_fus or cost in the key, but the Troyon gate (βN ≤ 3.5, tokamak.py:649) and the disruption-rate margins are therefore ~2× permissive. Found because the derived model carried the corpus definition. |

**Count: (i) 4 · (ii) 6 · (iii) 2 (both answer key) · (iv) 3 derived-over-key, 1 key-over-derived.**

Not scored above but real: the answer key covers four fuels, eight-plus confinement topologies, inverse and sizing modes, radiation/impurity physics, disruption penalties, and a full CAS stack. The derived relations are three DT-tokamak formulas with a stellarator note. The comparison is per-relation, not per-model.

---

## 4. H2 verdict

**The hypothesis "agents can derive good physics/cost models from a research corpus" comes out well on functional forms, mixed on constants, and the comparison shows exactly where each would fail silently.**

Where the blind derivation did well:

- Every functional form matched or exceeded the answer key: the reactivity skeleton, the complete power-balance accounting (agreement to 0.01 MW once constants are aligned), and the ampere-meter conductor law (bit-identical scaling, independently validated against ARC's tape inventory to 1%).
- The virial structure term is a genuine capture the answer key lacks: it reproduces ARC's structure-dominated magnet cost to −8% FOAK and reconverges on the $1030M analyst override to 4% when pushed through the same NOAK adjustment.
- The comparison exposed two real answer-key defects that only surfaced by holding a corpus-derived model against the code: the 6 T/9 T stellarator coil-field decoupling (D13, 33% undercount at 20a) and the factor-2-low beta_N convention that makes the Troyon and disruption gates ~2× permissive (D15).
- The derivation's self-declared uncertainty was well calibrated: everything it flagged as weak (M_n inferred, k_st upper bracket, f_3D unquantified) is exactly where the divergences are; everything it declared solid held up.

Where it got lucky:

- **M_n = 1.2** was inferred by closing ARC's published numbers, not sourced. It happens to be right for ARC and defensible generally, but a paper with an arithmetic inconsistency would have poisoned the constant unnoticed — consistency-closure has no error signal.
- **C_prof = 1.05** works only through the β-form channel, where ARC's pressure-based β_N already carries the profile peaking. Applied to the state form it would still underpredict by ~20%; the calibration point and the validation point are the same machine.

Where it would have misled without the answer key to check against:

- **k_st = 20 does not travel.** One-machine calibration on a conservatively-stated mass gives $17.6B of structure at the 20a point — the term is right, the multiplier needs the cross-machine ARIES-class mass/cost tables the corpus didn't contain (the derivation said as much, but nothing in the derived artifact would stop a downstream user from using 20 anyway).
- **No inverse/sizing capability and no radiation channel** means the derived relations answer "what does this machine do" but not "what machine do I need" — the mode the whole costing pipeline actually runs in — and cannot handle radiation-dominated regimes at all.
- Single-anchor constants generally (tape price at one field/temperature point, 2014 dollars) would drift silently as designs move off-ARC.

Net: for the three relations attempted, the blind derivation is at answer-key quality on structure, better than the key on magnet-cost physics, and weaker on breadth, constants provenance, and off-anchor robustness. The strongest argument for the H2 workflow is that the *disagreements* were informative in both directions — two answer-key bugs (D13, D15) and one answer-key structural gap (D11) were found only by holding the two models against each other.

---

## Files

- `comparison/compare.py` — evaluation script (derived relations verbatim + live 1costingfe calls)
- `comparison/results.json` — all point-value comparisons
- `comparison/grid.csv` — 16-point R × B0 sweep, both models
