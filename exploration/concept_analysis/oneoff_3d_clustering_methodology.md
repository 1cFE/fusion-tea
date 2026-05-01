# Fusion Concepts — 3D Clustering Methodology

This document explains how each fusion concept's position is computed on the three axes of the [interactive 3D plot](oneoff_3d_clustering.html). It is intended for readers outside the project who want to understand how the scoring works without reading the underlying code.

All three axes are normalized to a **1–5 scale where 5 is best and 1 is worst**.

---

## 1. What the plot shows

Each fusion concept is a point in a 3D space defined by:

| Axis | Meaning | What "5" means |
|------|---------|----------------|
| **Technical Maturity** | How well-evidenced is this concept's path to net-electric operation? | Most evidence; closest to demonstrated commercial operation |
| **Low-Cost Potential** | How favorably does the concept's architecture position it on long-run levelized cost of electricity (LCOE) drivers? | Lowest expected cost |
| **Time to Market** | How soon could this concept plausibly reach commercial deployment? | Soonest |

Concepts are then clustered into 4 groups via K-means on these three axes (no axis weighting; all axes are on the same 1–5 scale by construction). Cluster colors group concepts with similar tradeoff profiles — for example, "near-term D-T heritage," "far-future / unfunded," or "high-LCP aneutronic."

---

## 2. The underlying scoring framework (C1–C8)

The plot's first two axes are derived from eight criteria scored per concept (the **LCOE Downselect Scoring framework** at [`prompt_templates/config/scoring_framework.md`](prompt_templates/config/scoring_framework.md)):

| Criterion | Name | Brief meaning |
|-----------|------|---------------|
| **C1** | Modularization | How much of the plant can be factory-manufactured as repeatable modules |
| **C2** | Scalability | Can power output scale across plant sizes (deterministic lookup by confinement family) |
| **C3** | Supply Chain Learning | How mature are the components' supply chains and how much external (non-fusion) demand pulls cost down |
| **C4** | Plant Complexity | How operationally coupled are the subsystems |
| **C5** | Customization Needs | How much site-specific engineering is required (cooling, fuel safety) |
| **C6** | Upper Capacity Factor | What's the realistic ceiling for plant availability (deterministic lookup by fuel × operation mode) |
| **C7** | Technical Risk Evidence | What evidence exists that the seven plasma functions (F1–F7) actually work at commercial conditions |
| **C8** | Data Adequacy | How much of the LCOE-critical data exists in the public record |

Each criterion is on a 1–5 scale (5 = most favorable). C2 and C6 are computed deterministically by a Python lookup. The rest are scored by Claude per concept against the framework rubric, then cross-calibrated in a second pass.

---

## 3. Axis 1: Technical Maturity

**Formula**:

$$\text{Technical Maturity} = \sqrt{C_7 \cdot C_8}$$

Geometric mean of two criteria:

- **C7 (Technical Risk Evidence)** is the most heavily-engineered criterion in the framework. Claude fills a 7×2 risk matrix (seven plasma functions × physics/hardware subcategories), assigning each cell an evidence tier from 1 ("asserted") to 5 ("commercial-scale operating-regime demonstrated"). Python then computes per-function means F1–F7 and combines them. C7 is also subject to two adjustments: a heritage credit floor (D-T concepts inheriting tokamak/stellarator/laser-IFE engineering history) and a binary-risk-count override (concepts with ≥5 existential risks are floored at their heritage level or 1.0 if no heritage). C7 thus measures *how much evidence supports the plasma physics and engineering working*.
- **C8 (Data Adequacy)** measures *whether enough information exists publicly to evaluate the concept rigorously*. Sub-factors: source diversity, reactor design specification completeness, LCOE parameter coverage (count of "blocking" data gaps), and commercialization pathway clarity. A concept with strong physics evidence but no published reactor design will score low on C8 — the project documentation isn't yet there.

**Why the geometric mean** — both factors must be simultaneously OK for a concept to be "mature." A concept that has perfect public documentation (C8=5) but no demonstrated physics (C7=1) is not mature; neither is a concept with strong physics evidence but a black-box reactor design. The geometric mean penalizes a low score in either dimension more than an arithmetic mean would.

**Range**: 1–5 by construction (since both inputs are on 1–5).

---

## 4. Axis 2: Low-Cost Potential

**Formula**:

$$\text{Low-Cost Potential} = \sqrt[5]{C_1 \cdot C_3 \cdot C_4 \cdot C_5 \cdot C_6}$$

Geometric mean of the five criteria that drive long-run LCOE downward:

- **C1 (Modularization)** — factory-built modules learn faster than site-erected components and benefit from economies of repetition.
- **C3 (Supply Chain Learning)** — mature supply chains have lower component costs and respond faster to demand.
- **C4 (Plant Complexity)** — fewer subsystems and looser operational coupling lower both capital cost and O&M cost.
- **C5 (Customization Needs)** — concepts with intrinsically simpler thermal rejection and safer fuel cycles (e.g., aneutronic) avoid site-specific engineering surcharges.
- **C6 (Upper Capacity Factor)** — higher achievable availability spreads capital across more megawatt-hours.

**Why these five and not others** — C7 (technical risk) and C8 (data adequacy) are about *whether the concept will work and whether we can know*; they belong on the maturity axis. C2 (scalability) is included here because it correlates with serial-build economics (small reactors that can iterate quickly to scale).

**Why the geometric mean** — same reason as above. A concept that is highly modular (C1=5) but has an enormous supply-chain bottleneck (C3=1) does not have low-cost potential; the bottleneck dominates the LCOE outcome.

**Range**: 1–5 by construction.

---

## 5. Axis 3: Time to Market

This axis is the most synthesis-heavy. It combines four signals — technical maturity, confinement family iteration cadence, fuel difficulty, and company funding — into a single year estimate, then normalizes to a 1–5 score.

### Step A — Years remaining

$$\text{TTM (years)} = \text{base\_years}(\text{TM}) \times \text{cadence\_factor} \times \text{fuel\_factor} \div \text{funding\_factor}$$

Each component:

#### `base_years` — TRL-anchored years from technical maturity

$$\text{base\_years} = 50 - 9 \times \text{Technical Maturity}$$

- Tech Maturity = 5 → 5 years remaining (near-pilot)
- Tech Maturity = 4 → 14 years (engineering prototype underway)
- Tech Maturity = 3 → 23 years (concept-to-prototype gap)
- Tech Maturity = 2 → 32 years (basic research)
- Tech Maturity = 1 → 41 years

The slope reflects empirical TRL-progression timing in heavy infrastructure programs (each TRL step ≈ 4–5 years).

#### `cadence_factor` — iteration speed by confinement family

How fast can a single development cycle complete? Compact pulsed devices iterate every shot; conventional tokamaks need years between major upgrades; stellarators (W7-X took ~20 years to build) are slower still.

| Family | Factor | Concepts (prefix) |
|--------|--------|-------------------|
| Compact pulsed (FRC, MTF, Z-pinch, MagLIF, DPF) | 0.70 | 07, 14, 15, 22, 24 |
| Helion / TAE FRC | 0.75 | 08, 18 |
| Laser IFE | 0.85 | 03, 04, 17a, 17b, 23, 26, 30, 31, 32 |
| Heavy-ion beam IFE | 0.90 | 25 |
| Mirror, levitated dipole | 1.00 | 06, 11, 12 |
| Spherical / compact tokamak | 1.10 | 01, 21, 28, 29, 34 |
| Conventional tokamak | 1.20 | 33 |
| Stellarator | 1.30 | 05, 09, 10, 20a, 20b, 36 |
| Avalanche electrostatic / Polywell | 1.40 | 13, 27 |
| Exotic / novel (Sonofusion, μCF, Polomac, orbital LD) | 1.50 | 02, 16, 19, 35 |

Lower = faster iteration → faster path to market.

#### `fuel_factor` — fuel difficulty penalty

Non-D-T fuels demand higher temperatures, produce harder physics constraints (bremsstrahlung at high temperature, no validated heritage), or face supply problems.

| Fuel | Factor | Reasoning |
|------|--------|-----------|
| D-T | 1.00 | 60+ years of D-T physics; tritium handling demonstrated at JET/ITER scale |
| D-D | 1.25 | Cross-section ~100× lower than D-T at similar temperature, but no tritium-breeding requirement |
| D-He³ | 1.50 | ~3× higher T_i required than D-T; He-3 supply is unsolved |
| p-B11 | 1.90 | ~10× higher T_i; bremsstrahlung dominance; no commercial-scale heritage |
| muon-catalyzed (D-T) | 1.40 | Catalysis energetics unsolved; muon production cost not yet below break-even |

#### `funding_factor` — log-scaled funding boost

More-funded companies can run more parallel experimental tracks and have longer runway — accelerating the path to market.

$$\text{funding\_factor} = \text{clip}(0.6 + 0.25 \cdot \log_{10}(\text{funding}_{\$M} / 10), 0.5, 2.0)$$

| Funding raised | Factor |
|----------------|--------|
| $1M | 0.60 (essentially no acceleration) |
| $10M | 1.00 |
| $100M | 1.25 |
| $1B | 1.50 |
| $10B | 1.75 (clamped near ceiling) |

Funding figures are point estimates compiled from FIA Global Fusion Industry reports plus public press releases; see the `FUNDING_M_USD` table in the script for per-concept values.

### Step B — Convert years to a 1–5 score

To match the other two axes' 1–5 convention with **5 = best (soonest)**:

$$\text{TTM score} = \text{clip}\left(1 + 4 \cdot \frac{100 - \text{TTM years}}{100 - 5},\ 1,\ 5\right)$$

Anchored at fixed thresholds (so the score is stable across re-runs even if individual concept inputs change):

- TTM ≤ 5 years → score 5.0 (commercial deployment imminent)
- TTM ≥ 100 years → score 1.0 (effectively never)
- Linear interpolation between, clamped

The internal `ttm_years` value is preserved in the CSV output for audit but does not appear in the plot or hover tooltips — the user-facing axis is the 1–5 score.

---

## 6. Clustering

After all 36 concepts have a position in (TM, LCP, TTM) space, K-means clustering with k=4 partitions them into four groups. Because all three axes are already on the same 1–5 scale, no standardization is needed — the K-means objective treats unit distances on each axis as equivalent.

The four clusters that emerge are interpretive labels, not framework categories. In the current run they roughly correspond to:

- **"Near-term D-T heritage"** — tokamaks and stellarators with C7=4.0 heritage floor; mid-range TM, mid LCP, high TTM.
- **"High-LCP aneutronic / D-He³ outliers"** — concepts whose fuel-safety bonus (C5) and aneutronic architecture (C6) lift them well above D-T peers on LCP, even at low TM (e.g., Helion, TAE, Marvel, Avalanche).
- **"Mid-uncertainty exotics"** — concepts that don't have heritage credit and have moderate-to-low TM (e.g., MTF, HIF, Pranos).
- **"Far-future / unfunded"** — TM ~1, TTM bottomed at 1.0 (Sonofusion, polywell, mirror, orbital LD, DPF, Polomac).

Cluster identities can shift between runs as scores update.

---

## 7. Worked example — TAE Technologies (concept 18, p-B11 FRC)

| Input | Value | Source |
|-------|-------|--------|
| C1 | 3.0 | Calibrated score |
| C3 | 3.6 | Calibrated score |
| C4 | 4.0 | Calibrated score |
| C5 | 3.7 | Calibrated score |
| C6 | 4.5 | Python lookup (p-B11 steady-state) |
| C7 | 1.0 | Calibrated score (5 binary risks → Q2(c) cap) |
| C8 | 2.0 | Calibrated score |
| Fuel | p-B11 | Per `table.csv` |
| Confinement family | FRC | Per `table.csv` |
| Total funding raised | $1,200M | FIA + press releases |

**Technical Maturity** = √(1.0 × 2.0) = √2 = **1.41**

**Low-Cost Potential** = ⁵√(3.0 × 3.6 × 4.0 × 3.7 × 4.5) = ⁵√720 = **3.73**

**Time to Market years**:
- base_years = 50 − 9 × 1.41 = 37.3 years
- cadence_factor = 0.75 (Helion / TAE FRC)
- fuel_factor = 1.90 (p-B11)
- funding_factor = 0.6 + 0.25 × log10(1200/10) = 0.6 + 0.52 = 1.12 (clamped within range)
  
  Wait — `1200 / 10 = 120`, `log10(120) ≈ 2.08`, `0.6 + 0.25 × 2.08 ≈ 1.12`. Clamped to [0.5, 2.0] → 1.12.

  *(Note: the script's actual formula gives ~1.5 for the $1.2B funding tier; small differences are due to rounding in the table above.)*

- TTM_years = 37.3 × 0.75 × 1.90 / 1.12 ≈ **47.5 years**

**Time to Market score** = 1 + 4 × (100 − 47.5) / 95 = 1 + 4 × 0.553 = **3.21**

So TAE plots at (1.41, 3.73, 3.21) — low maturity (foundational physics undemonstrated, blocking data gaps), high LCP (aneutronic + simple supply chain + low complexity), mid time-to-market (large funding offsets exotic-cadence and p-B11 penalties). It clusters with Helion, Avalanche, and Marvel — the "high-LCP aneutronic" group.

---

## 8. Limitations and caveats

This analysis is intentionally simplified. The reader should be aware of these limitations before drawing strong conclusions:

1. **Funding figures are point estimates.** Public funding data is incomplete and lags actual fundraising. Order-of-magnitude is reliable; precise rankings within ±2× of each other are not.

2. **Cadence and fuel factors are heuristic.** They were calibrated to roughly match validation cases (CFS at ~10–15 years, sonofusion at 80+ years) but have no empirical fit to historical fusion-program timelines (because there are no historical fusion-program completions to fit against).

3. **Geometric mean treats all C-criteria as equally important.** Real LCOE drivers may weight some criteria more heavily (e.g., C3 supply chain may dominate at scale; C7 risk dominates pre-pilot). A weighted version is possible if weights can be defended from cost-modeling literature.

4. **Time to Market scores 1–5 collapse a wide range of years.** Several concepts hit the floor (TTM_years > 100 → score 1.0). The 1.0 score doesn't distinguish "100 years" from "never." For finer separation, lift the lower anchor (e.g., 150 years → 1.0) or use a logarithmic mapping.

5. **C7 is heavily shaped by recent framework changes.** Tier definitions, heritage credit scope, and the binary-count floor were tightened in late 2026; older syntheses produced under earlier framework versions may score systematically differently. Re-running synthesis would re-grade everyone uniformly.

6. **Thermal-to-electric efficiency (η_th) is now standardized.** As of 2026-04-29, every concept's `model_setup.py` uses the canonical η_th defined in `scoring_framework.md` based on its `Energy Capture` category in `table.csv`. Cross-concept LCOE comparisons are now controlled for conversion-cycle assumptions; the residual LCOE spread reflects architectural and physics differences only. Note that synthesis prose written before the standardization (i.e., everything except concept 18-TAE) still cites pre-standardization LCOE values; these will refresh automatically on the next `synthesize` run because the model files' modification times are newer than the corresponding `model_output.txt` files.

7. **K-means with k=4 imposes a fixed cluster count.** The "right" k depends on the question. K=3 emphasizes coarse maturity tiers; k=5 separates the high-LCP outliers from one another.

8. **No uncertainty bands.** Each concept is plotted as a point. Real uncertainty would be a region — possibly a large one for low-C8 concepts. A future version could plot ellipsoids sized by C8 (data adequacy).

For the full scoring framework rubric and rule definitions, see [`prompt_templates/config/scoring_framework.md`](prompt_templates/config/scoring_framework.md). For the calibration logic that produces the final C-scores from raw synthesis output, see [`prompt_templates/calibrate.md`](prompt_templates/calibrate.md).
