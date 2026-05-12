# Trace: 15-sheared-flow-stabilized-z-pinch (Zap Energy)

**Purpose:** Second calibration pass. Trace #1 (`trace_01-hts-compact-tokamak.md`) populated the template for a cohort-rich, supply-chain-fragile concept. This trace targets the **structurally opposite** case: physics-gated, low-data, no meaningful cohort. Inputs: `exploration/concept_analysis/analyses/15-sheared-flow-stabilized-z-pinch/synthesis.md` (FST 2023 reactor design + downselect scoring) and `knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/dossier.md`. Methodology findings inline with **[METHOD]**, consolidated at the bottom.

---

## Stage 1 — Physics path (time-and-cost-to-Stage-2 discount)

- **Current TRL / Q achieved:** Q never measured at any scale. FuZE-3 (Nov 2025) achieved 1.6 GPa total pressure at ~40 µs pinch lifetime — thermonuclear neutrons but Q << 1. FuZE-Q targets Q ≥ 1. Commercial requires Q ≥ 10 at 200 µs pinch, 1.2–1.5 MA — a 5× lifetime, 30× density, and ≥100× Q extrapolation from current state.
- **Estimated capital and time to Stage-2 entry:** Zap has raised ~$330M; Century engineering platform operating but at 0.2 Hz with non-fusing gas. Path to a Stage-2-eligible plant requires (a) FuZE-Q or successor demonstrating Q ≥ 1 with validated scaling, (b) Century scaling to 1+ Hz with LiPb (not Bi), (c) integrated D-T reactor design beyond the FST 2023 paper. Realistic Stage-2 entry: 10–15 years from now, conditional on multiple binary physics gates closing.
- **Discount-calibration inputs:**
  - *Paradigm co-development:* **Weak.** ZETA (1950s) showed Z-pinch instability the hard way. Sheared-flow stabilization (Shumlak, UW, 2010s+) is essentially a single-group lineage. No other private or public program is pursuing SFS Z-pinch at reactor scale.
  - *Open scientific heritage:* Moderate. Thompson et al. FST 2023 reactor paper is published and peer-reviewed; FuZE diagnostics (Te, Ti, density) are independently measured. But the Q > 10 projection is a calculated extrapolation, not validated.
  - *Workforce depth:* **Thin.** Pulsed power workforce exists in defense (Sandia Z-machine, NNSA labs) but at wrong rep rate (single-shot MV vs. 10 Hz at 50–200 kV). Sheared-flow Z-pinch expertise is concentrated at UW + Zap (low hundreds of people globally).
- **Discount applied:** **Heavy.** Among the 38 concepts, this discount is in the top quartile of severity — the physics gate is real, binary, and singly-developed.

**[METHOD] Finding 1 (carries from trace #1):** Even with the proposed *minimal / low / moderate / heavy* four-bucket gradation, "heavy" still under-resolves the structural distinction *why* the discount is heavy. ARC's residual risk is *engineering*; Zap's residual risk is *physics existence proof*. Suggest splitting the discount into **two orthogonal sub-discounts**: (i) physics-gate-distance and (ii) lineage-thinness. ARC ranks "near + thick"; Zap ranks "far + thin". Single-axis "heavy" loses this.

**[METHOD] Finding 2:** Stage 1 currently has NO named F-factors — just a "discount." But for Zap, the dominant failure mode (Q < 7 → net-electric-negative) lives at Stage 1. The trace template can't tag a dominant failure at Stage 1 because there's no F-vocabulary there. Either (a) elevate the Stage-1 discount calibration into proper F-factors (e.g., `F1.a — physics gate distance`, `F1.b — paradigm co-development depth`, `F1.c — workforce depth`), or (b) explicitly accept that Stage-1-gated concepts have their dominant failure recorded in a different slot than Stage-2/3/4-gated concepts.

---

## Stage 2 — FOAK affordability

### Intrinsic F-factors
- **F2.a — Minimum-viable-plant capital cost:** FST 2023 reactor: 458 MWe (10 modules × 45.8 MWe net). Total overnight capital ~$5B (back-of-envelope from synthesis tables; $750M driver + $495M blanket + $507M buildings + $1B turbine/electric/BOP + balance). Right at the $5B sovereign-only threshold. But this estimate is *conditional* on Q = 10 holding and on driver cost coming in at $75M/module — both unconstrained. Plausible FOAK range: $4B–$15B depending on driver cost realization. **Pole: failure-leaning at upper tail; borderline at central estimate.**
- **F2.b — Build-time risk:** Assuming Stage-1 physics gates close by ~2035, FOAK build adds 6–8 years → first electricity ~2041–2043. Within Eash-Gates ratcheting zone. NRC Part 30 helps (same as ARC). **Pole: moderate failure-leaning.**

### Ecosystem-relational F-factors
- **F2.c — Regulatory framework state:** Same as ARC — Part 30 leverage for D-T fusion. **Pole: leverage** (inherited from the broader D-T cohort, not concept-specific).
- **F2.d — Critical component supply maturity:**
  - *Pole:* **Failure.** No commercial pulsed-power system exists at the required spec (50–200 kV at 100–200 kA, 10⁸–10⁹ shot lifetime). Current industrial capacitors: 10⁴–10⁵ shots. Switch capability gap is a **technology-class** gap, not a scaling gap — SiC tops at 6.5–15 kV. OSTI 2025: 10–20 year roadmap to required component class.
  - *Slack/bottleneck:* **Bottleneck at FOAK volumes** if commercial-grade components are needed; **slack** if FOAK can tolerate early-generation components at reduced lifetime (with much higher consumable cost). Effectively a *capability* gap rather than a *quantity* gap.
- **[METHOD] Finding 3:** F2.d's slack/bottleneck axis is the **wrong dimension** for this concept. The Zap problem is "the component class doesn't exist at the right operating point" — neither slack nor bottleneck applies because there's no supply curve at all. Suggest adding a third state to the F2.d/F3.a/F4.c qualifier: `{slack | bottleneck | capability-gap}`, where capability-gap means the technology class is wrong, not the quantity.

### Distinct E-factors
- **E2.a — Crossover platform attracts non-fusion investment:** **Weak.** Pulsed power has a defense customer (NNSA, DoD directed energy, Sandia Z-machine campaigns) and an industrial niche (mining, materials processing), but the **operating regime is wrong**: defense systems are MV-class single-shot or low-rep; industrial systems are low-voltage continuous. Neither funds the 10⁸-shot, 100-kA, 50–200 kV component class Zap needs. The crossover-platform vocabulary holds, but the *operating-point overlap* is small enough that the effective leverage is near zero. Contrast with REBCO: MRI/grid/transport all operate in the same temperature/current regime ARC needs.
- **[METHOD] Finding 4:** Crossover-platform leverage needs an **operating-point-overlap qualifier**. ARC's REBCO crossover is "100% operating-regime overlap with MRI/grid/transport." Zap's pulsed-power crossover is "<10% operating-regime overlap with defense/industrial." Same `E2.a` tag with the same pole (`leverage exists`) hides a 10× quantitative difference. Suggest annotating E2.a with `{regime-overlap: high | partial | nominal}`.
- **E2.b — Intra-fusion early-mover effect:** **Net negative for Zap; cohort is thin.** No other concept in the 38-candidate set uses SFS Z-pinch architecture. Adjacencies: MagLIF/Z-machine (pulsed power, but MV single-shot — wrong regime); MIF concepts (also pulsed power, mostly low rep rate). The 4 concepts that "need pulsed-power capacitors at scale" per the dossier section don't share Zap's specific 50–200 kV / 10 Hz operating point. **First-mover-and-isolated**, in the role taxonomy implied by Finding 6 of trace #1.

### Plausible FOAK buyer
DOE/NNSA pulsed-power infrastructure investment (national security framing) + private equity. **No hyperscaler PPA story credible** at this stage — the physics risk is too high for a clean-firm-power off-take contract. Buyer pool: research-flagged government anchor + venture capital tolerant of binary risk.

### Dominant failure factor at this stage
**F2.d (failure pole, capability-gap-tagged)**, but largely a downstream consequence of the Stage-1 physics gate. Even if FOAK is financeable, building it requires component technology that doesn't exist. The interesting structural feature is that Stage-2 fragility is *materially separable* from Stage-1 fragility — fixing one doesn't fix the other.

### Dominant leverage factor at this stage
**F2.c (regulatory framework) — inherited from D-T cohort.** Genuinely no concept-distinctive Stage-2 leverage exists. This is the trace's most uncomfortable finding for Zap: it has no positive Stage-2 wedge of its own.

---

## Stage 3 — Chasm crossing

### Intrinsic F-factors
- **F3.b — Site-specialization fraction:** Strong leverage. Modular architecture (10 × 46 MWe units). Driver (37% of capital) is factory-manufactured. Electrodes (10%) are factory-built consumables. Blanket assembly is site work but uses repeated sub-assemblies. C1 score 4.1 from synthesis. **Pole: leverage-leaning.**
- **F3.c — Replication unit size:** Per-module $500M, per-plant ~$5B at 458 MWe → ~$11/We FOAK, ~$4–6/We NOAK if driver cost-down works. Multi-module architecture lets hyperscalers commit to fractional plants (4–6 modules ≈ $2–3B). **Pole: leverage-leaning at NOAK; failure-leaning at FOAK.**

### Ecosystem-relational F-factors
- **F3.a — Supply-chain maturity at chasm scale:**
  - *Pole:* **Failure, capability-gap-tagged.** At fleet scale (~10 plants × 10,000–216,000 capacitors per plant — synthesis cites OSTI 2025), required capacitor count is 100,000s to millions of units at a lifetime spec that doesn't exist. Western pulsed-power manufacturing has 4–6 year lead times for current spec; building 10 plants would take 50+ years at current capacity per OSTI.
  - *Slack/bottleneck/capability:* **Capability-gap** (per Finding 3) — different from ARC's REBCO case which is a quantity bottleneck against a known unit cost trajectory.
- **F3.d — Regulatory amortization path:** Standard D-T cohort amortization applies. **Pole: leverage**, but it's a shared leverage with all D-T concepts.

### Distinct E-factors
- **E3.a — Intra-fusion fleet co-development:** **Weak.** The "pulsed-power-dependent" cohort (~4 concepts per dossier) doesn't share Zap's specific operating point. Each pulsed-power concept (MagLIF, MIF, IFE drivers, Z-pinch) needs different voltage/rep-rate/lifetime combinations. Co-development on shared sub-problems (dielectric materials, switch device classes) is real but partial.
- **E3.b — Shared sub-problem solutions:** **Moderate.** LiPb blanket chemistry shared with ARC variants + select MFE liquid-wall concepts. D-T tritium breeding shared across all D-T cohort. Pulsed-power dielectric research shared with NNSA programs (but operating-regime mismatch limits transfer).

### Most plausible chasm-crossing path
Pre-Stage-3 prerequisite: Q ≥ 7 demonstrated AND pulsed-power capability class developed (10⁷+ shot capacitors at 50+ kV, 100+ kA switches). If both close by ~2040, first 3–5 plants on government infrastructure anchor + early hyperscaler interest. Fleet build constrained by capacitor manufacturing capacity (OSTI's 50+ year buildout) absent a major industrial program. **The chasm is structurally narrower than ARC's** (no $642/MWh-vs-$80/MWh wholesale gap if Q hits — synthesis shows $145–200/MWh achievable) — but **the chasm sits behind two binary gates** that have to close first.

### Dominant failure factor at this stage
**F3.a (failure pole, capability-gap-tagged): pulsed-power component manufacturing scale-up.** Compound with Stage-1 binary physics gate — failure here matters only if Stage-1 closes.

### Dominant leverage factor at this stage
**F3.b (site-specialization, leverage pole): modular factory-manufactured architecture.** Zap's most distinctive structural advantage. Module count (10× per plant) supports faster learning curves than single-unit tokamaks.

---

## Stage 4 — Learning-curve descent

### Intrinsic F-factors
- **F4.b — Volume vs. R&D learning mechanism:** **Mixed.** Driver cost (37%) is volume-driven IF the capability class develops (Wright's Law on capacitor manufacturing). LiPb chemistry, electrode lifetime, plant integration are R&D-driven. Recirculating-fraction reduction is R&D-driven (driver efficiency from 70% → 80% requires component innovation, not volume).
- **F4.d — Modularization-vs-scale crossover:** Strong modular case (10 × 46 MWe). Crossover N where learning offsets scale penalty is probably ~5–10 plants — earlier than ARC's because (a) per-module cost is lower and (b) module count per plant is higher (factory-line economics within a single plant). **Pole: leverage-leaning.**

### Ecosystem-relational F-factors
- **F4.a — Cost-reduction knobs and non-fusion ride-along:**
  - *Knob count:* 4–5 (driver capacitor $/J, electrode lifetime, LiPb chemistry, driver efficiency, capacity factor via electrode-swap tempo). Comparable to ARC's count.
  - *Non-fusion ride-along:* **Thin.** Capacitor knob has partial defense-industrial ride-along but at wrong regime. Other knobs are fusion-specific.
  - *Pole:* **Mixed-failure-leaning.** Fewer knobs with strong external pull than ARC.
- **F4.c — Specialty-input external-market position:**
  - *Pole:* **Failure, capability-gap-tagged.** Pulsed-power components have an external market (defense, industrial) but operating-regime mismatch means Wright's Law doesn't run from combined volume. LiPb/Li-6/Be: same as ARC, no external market.
  - *Slack/bottleneck/capability:* All inputs are **capability-gap or bottleneck** at maturity.

### Distinct E-factors
- **E4.a — Crossover platform revenue funds continued R&D:** **Weak** (same root cause as E2.a — operating-regime mismatch). Defense pulsed-power R&D may incidentally help, but Zap can't count on it as a financing wedge.
- **E4.b — Talent inflow from adjacent industries:** **Moderate.** High-voltage engineering, capacitor manufacturing, arc-furnace electrode engineering all have adjacent industries. LiPb chemistry workforce is narrow.

### Plausible learning-curve mechanism
**R&D-dominated.** Volume learning is constrained by the small cohort. Cost floor at maturity (per synthesis): **$130–500/MWh band, central ~$145–200/MWh at 1 GWe scale.** Central estimate is **lower than ARC's $200–300/MWh floor** — Zap is structurally cheaper *if it works* because the magnet system is eliminated. But the **uncertainty band is 4× wider** than ARC's because Q and driver-cost have no anchor.

### Dominant failure factor at this stage
**F4.c (failure pole, capability-gap) for pulsed-power components.** Plus the cohort-thinness multiplier — fewer concepts sharing the ride means slower Wright's Law descent even if the components exist.

### Dominant leverage factor at this stage
**F4.d (modularization-vs-scale crossover, leverage pole).** Per-module size matched to factory production; crossover N is reachable at modest deployment volumes if the cohort builds at all.

---

## Cross-stage carriers

### F-carriers
- **Pulsed-power component lifetime & capability:** Bites at all three (Stage 2 / 3 / 4). Fundamental concept-defining carrier. Distinct from ARC's REBCO carrier in that it's a *capability-class* gap, not a *quantity* gap.
- **Tritium / Li-6 / Be supply:** Same as ARC (shared D-T cohort carrier). Bites hardest at Stage 4.
- **Electrode erosion lifetime:** Bites at Stage 3 and Stage 4 (capacity factor + consumable cost). Concept-specific.

### E-carriers
- **D-T fuel-ecosystem R&D position:** Shared with the D-T cohort, same as ARC.
- **Pulsed-power adjacent-industry workforce:** Moderate, but operating-regime overlap is small.

---

## LCOE lower bound (promoted to first-class output, per trace #1 Finding 4)

**Central estimate:** ~$145–200/MWh at 1 GWe scale, Q = 10, $75M/module driver.

**Uncertainty band:** $130/MWh (optimistic Q + driver cost) to >$500/MWh (Q = 5 or driver > $200M/module). This is **four times wider** than ARC's $200–300/MWh floor band. The point estimate is favorable, but the epistemic confidence is **structurally lower** because two dominant uncertainties (Q value, driver cost) have no experimental or market anchor.

**[METHOD] Finding 5:** LCOE-lower-bound as a first-class output should be reported as **(point, band)**, not point alone. ARC's floor is "tight band around the central estimate"; Zap's is "wide band around a lower central estimate." Down-select decisions that ignore the band width will systematically over-rate Zap-class concepts and under-rate ARC-class concepts (or vice versa, depending on risk preference). The band width itself is a feature — it expresses how much the LCOE estimate is doing real work vs. summarizing ignorance.

---

## Concept's dominant failure mode (single biggest gate across all stages)

**Stage 1 / physics-gate (Q ≥ 7 never demonstrated).** Binary failure mode: if SFS Z-pinch can't reach Q ≥ 7 at commercial current and pinch lifetime, the concept produces no net electricity at any cost, in any timeline. Every Stage-2/3/4 risk is conditional on this gate closing.

**Compound secondary: Stage 3 / F3.a (pulsed-power capability-class gap).** Even if Stage 1 closes, the supply chain for required pulsed-power components doesn't exist and has a 10–20 year development roadmap. Both gates are binary in the sense that failing either kills the concept.

**[METHOD] Finding 6:** The trace template's `(stage, F-code)` failure tag doesn't have a place for **Stage-1 physics-gate failures**. ARC's failure was Stage-3 supply-chain; Zap's is Stage-1 physics. For Stage-1 concepts, the failure is recorded in the "discount" section, not in the dominant-failure section, which creates **asymmetric reporting**. Either (a) add proper Stage-1 F-factors per Finding 2, or (b) explicitly allow the dominant-failure tag to point at the Stage-1 discount, not just F-factor codes.

**[METHOD] Finding 7:** Binary-vs-degrading classification (present in synthesis C7 risk matrix) is missing from the trace's failure-mode taxonomy. ARC's REBCO bottleneck is *degrading* (worse economics, not zero output); Zap's Q-gate is *binary* (zero output if it fails). These are fundamentally different gate types and should be tagged distinctly. Suggest adding a `{binary | degrading}` qualifier to every failure-mode entry.

---

## Concept's dominant leverage (single biggest tailwind across all stages)

**Stage 3 / F3.b (site-specialization, leverage pole) + Stage 4 / F4.d (modularization-vs-scale crossover).** Modular factory-manufactured architecture eliminates the largest tokamak cost driver (magnets, ~30–40% of capital) and replaces it with components that *could* ride a factory learning curve — if the capability class develops. The leverage is **conditional on the failure modes resolving**.

**[METHOD] Finding 8:** Zap's leverage is *conditional* in a way ARC's isn't. ARC's REBCO + cohort leverage operates **regardless of whether ARC ships** (REBCO descends because of MRI/grid/transport demand). Zap's modularization leverage only matters **if the binary gates close first**. Suggest tagging leverage entries with `{unconditional | gate-conditional}` — unconditional leverage is much more decision-relevant in a down-select context because it doesn't compound the concept's own gate risk.

---

## Concept-cohort position (per trace #1 Finding 6)

**First-mover, isolated.** Zap is the only commercial SFS Z-pinch program. No fast-follower exists. The pulsed-power adjacency (MagLIF, MIF) is too operating-regime-distant to count as a cohort.

Contrast with ARC's "first-mover, cohort-rich" position. This is the single most decision-relevant structural feature distinguishing the two concepts — it makes Zap's failure modes uninsurable in a way ARC's are not (ARC's REBCO bet is mutualized across 8 concepts; Zap's Q bet is borne entirely by Zap).

---

## Methodology findings consolidated

1. **Stage-1 discount needs two orthogonal axes** (physics-gate distance × lineage thinness), not a single bucket. ARC and Zap both "heavy" in trace #1's coarse vocabulary but for structurally different reasons.
2. **Stage 1 needs proper F-factors** so dominant-failure tags can land there. Currently Stage-1-gated concepts can't have their primary failure recorded in the same slot as Stage-2/3/4-gated concepts.
3. **F2.d / F3.a / F4.c slack/bottleneck axis needs a third state: `capability-gap`** for cases where the required technology class doesn't exist (Zap's pulsed-power vs. ARC's REBCO-quantity-shortage).
4. **E2.a crossover-platform needs an operating-regime-overlap qualifier** `{high | partial | nominal}`. ARC's REBCO crossover has high regime overlap; Zap's pulsed-power crossover is nominal. Same pole, different reality.
5. **LCOE lower bound should be reported as (point, band)**, not point. Band width is itself a structural feature distinguishing engineering-bounded estimates (ARC) from uncertainty-bounded estimates (Zap).
6. **Dominant-failure tag needs a `{binary | degrading}` qualifier.** ARC's REBCO bottleneck is degrading; Zap's Q gate is binary. These are not commensurable risks under a single tag.
7. **Leverage entries need a `{unconditional | gate-conditional}` qualifier.** ARC's REBCO crossover delivers leverage even if ARC fails to ship; Zap's modularization leverage requires Zap's gates to close first.
8. **Cohort-position role confirmed as a structural feature** (trace #1 Finding 6). Zap = "first-mover, isolated"; ARC = "first-mover, cohort-rich." This axis predicts mutualization of failure modes and should be a top-level trace field.

---

## What two traces teach the broader methodology

Trace #1 found the vocabulary needs *widening* (new F-factor codes, compound failures, stage-dependent qualifiers). Trace #2 finds the vocabulary needs *new dimensions*:

- **Capability-gap vs. quantity-bottleneck** is a separate axis from slack/bottleneck.
- **Binary vs. degrading** is a separate axis from intrinsic/ecosystem.
- **Unconditional vs. gate-conditional leverage** is a separate axis from F/E.
- **(Point, band) LCOE** is a different reporting object than (point) LCOE.
- **Stage-1 gate position** needs first-class F-vocabulary, not just a discount.

These are not additional codes inside the existing framework — they are **orthogonal qualifiers** that apply to existing codes. The methodology revision after two traces should propose:

1. Promote Stage-1 discount inputs to `F1.a/b/c` F-factors so failure-mode tagging is symmetric across stages.
2. Add three orthogonal qualifiers to every F-factor entry: `{slack | bottleneck | capability-gap}`, `{binary | degrading}`, and (for E-factors and leverage) `{unconditional | gate-conditional}`.
3. Report LCOE lower bound as (point, band) with band width as a first-class field.
4. Add `cohort-role` as a top-level concept field with values `{first-mover-cohort-rich | first-mover-isolated | fast-follower | adjacent}`.

The trace structure itself held up across two structurally opposite concepts — the gaps are in the **annotation grammar**, not the template skeleton. Recommend locking the skeleton and proposing the qualifier-grammar revision as a single follow-up artifact.
