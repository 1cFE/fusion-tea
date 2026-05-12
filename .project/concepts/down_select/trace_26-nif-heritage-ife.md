# Trace #5 — 26 NIF-heritage Laser ICF Indirect Drive — targeted dossier-cell fill

**Scope:** Targeted trace per entry 011 stopping rule. Goal: defend the cells flagged `[thin]` in row 4 of `decision_dossier_draft_v0.md` Part B. Single-source read of `26-laser-icf-indirect-drive/synthesis.md` §1, §3, §5.

**Companion traces:** `trace_01-hts-compact-tokamak.md`, `trace_15-sfs-z-pinch.md`, `trace_08-helion.md`, `trace_14-general-fusion.md`.

---

## Cell 1 — LCOE floor (point, band, basis, epistemic)

**Point:** $98/MWh at 1.5 GWe baseline (synthesis §1).

**Band:** $80 → $160/MWh — a **2× band**, comparable to GF's but **dominated by a different parameter**: availability (elasticity −0.97), not driver capital.

**Basis: joint-multi-gate-conditional, with a different gate-composition than Helion.** The basis-type taxonomy now has a *sub-flavor* split within joint-multi-gate:

| Concept | Joint-gate composition | Dominant uncertainty within joint |
|---|---|---|
| Helion (08) | physics × manufacturing-cost × conversion-efficiency | capacitor $/J 10× gap |
| **26 NIF-heritage** | **physics × manufacturing-cost × operational-availability** | **availability (elasticity −0.97)** |

Both are joint-multi-gate; the difference is *which gate dominates the uncertainty*. The methodology should track this — same basis-type can have different dominant-uncertainty profiles.

**Gate decomposition for 26:**
1. **Physics gate (binary):** Target gain G > 100 required; NIF demonstrated 4.13. Gap ratio = 25-50× (synthesis §1 line 12). The synthesis is unusually direct: §5 line 163 — *"if gain saturates below G ~10, the concept is economically nonviable."*
2. **Manufacturing-cost gate (degrading):** Laser diodes at $0.007/W (3× below current floor of $0.02/W). Elasticity +0.35.
3. **Operational-availability gate (degrading, but elasticity −0.97 makes it dominant):** 75% baseline has *no published basis*; OSIRIS/SOMBRERO (1992) modeled 68-69%; Inertia's 3-5 yr chamber replacement implies 55-60%; Xcimer's liquid-wall "no structural replacement" claim is unvalidated and would enable >85% if it holds.

**Epistemic:** Joint-multi-gate-conditional. **Critically: the gain gate is binary-terminal-economically; the other two are degrading.** This is a *mixed-qualifier joint product* — different from Helion (where 2 gates are binary and 1 is degrading) and different from any other shortlist concept.

**Dossier update:** Row 4 LCOE-floor cell should read: `($98/MWh baseline, band $80-$160; joint-multi-gate-conditional on gain G>100 (binary) × laser $/J ≤ $300/J (degrading) × availability ≥ 75% (degrading-dominant via elasticity −0.97); availability is dominant uncertainty.`

---

## Cell 2 — Dominant failure (with qualifier)

**Tag:** `F1 binary-terminal-economically, gate-type=physics (G > 100 gain scaling) × F2.d capability-gap-degrading, gate-type=manufacturing-cost (DPSSL $/J 3× short) × F_operational capability-gap-degrading, gate-type=engineering-operational (75% availability unvalidated)`

**Primary component (binary-terminal-economically, physics-gated):**
- Per synthesis §5 line 163 direct quote: *"if gain saturates below G ~10, the concept is economically nonviable and development effort should shift to alternate confinement approaches."*
- This is a **new qualifier sub-flavor**: `binary-terminal-economically`. Distinct from:
  - Zap's `binary-terminal` (concept dies completely; physics is wrong),
  - GF's `binary-terminal` (concept dies completely; engineering can't be built),
  - Helion F1's `binary-with-fallback` (concept converts to D-T at higher LCOE),
  - Helion F7's `binary-sharp-cliff` (output goes to zero).
- 26's binary-terminal-economically means: the physics *as a science demonstration* continues (NIF keeps operating for NNSA), but the *commercial concept* is dead. The architecture persists in another role.

**Methodology observation #1:** The binary-qualifier taxonomy now has **five entries**:
1. `binary-terminal` (concept dies completely — Zap, GF)
2. `binary-terminal-economically` (commercial concept dies, science role persists — 26)
3. `binary-with-fallback` (concept converts to another concept — Helion F1)
4. `binary-sharp-cliff` (output goes to zero, architecture continues — Helion F7)
5. (placeholder for trace #6, possibly `binary-with-state-backed-rescue` if 28 has it)

These five differ on two orthogonal questions: (a) does the architecture persist? (b) does it persist in a *commercial* role or a *science/defense* role?

**Secondary components:**
- **F2.d manufacturing-cost capability-gap (degrading):** Laser cost $0.02/W → $0.007/W. Same shape as Helion's capacitor capability-gap (information also-partially-disclosed; cost reduction trajectory unproven). Sub-flavor: *manufacturing-curve dependency*.
- **F_operational capability-gap (degrading, dominant):** Availability has no validated model. **This is a new gate-type** that GF (engineering-built) did not exhibit. GF's failure was "does this system exist?" 26's secondary failure is "does this system run at sufficient duty?" — **engineering-operational** as a gate-type.

**Methodology observation #2:** The gate-type axis (introduced in trace #4) extends to a **5-entry taxonomy**:
1. `physics` (Zap, Helion F1, **26 primary**)
2. `engineering-built` (GF — does this exist?)
3. `engineering-operational` (**26 secondary** — does this run at duty?)
4. `manufacturing-cost` (Helion F2.d, **26 tertiary** — does the cost curve close?)
5. `supply-chain` (ARC REBCO singleton — does the supply curve mature?)

Each gate-type has characteristic resolution paths: physics needs experimental closure (NIF EYC, Polaris); engineering-built needs prototype; engineering-operational needs sustained operation data; manufacturing-cost needs learning-curve evidence; supply-chain needs industry maturation. **The methodology should record gate-type for every failure tag — it's the strongest predictor of "what evidence would retire this risk."**

**Dossier update:** Row 4 dominant-failure cell should read: `F1 binary-terminal-economically, gate-type=physics (G > 100, synthesis §5 line 163: "economically nonviable") × F2.d capability-gap degrading, gate-type=manufacturing-cost (laser diodes $0.02/W → $0.007/W) × F_operational capability-gap degrading, gate-type=engineering-operational (availability dominant uncertainty, elasticity −0.97; 1992 SOMBRERO baseline 68-69%; no validated model)`.

---

## Cell 3 — Dominant leverage (with qualifier)

**Tag:** `Layer A unconditional (HIGH): NNSA-funded NIF ignition demonstrations + DPSSL industrial-supply-chain overlap + HYLIFE-III liquid-wall heritage. Layer B gate-conditional: target factory <$1/target + 10 Hz cycle.`

**Layer A is the strongest of any trace so far** — it has *three distinct unconditional leverage threads*:

**Thread 1 — Public-sector physics demonstration (architecture-proof, government-funded):**
- NIF's 10 ignition shots (Dec 2022 - Oct 2025) are funded by NNSA stockpile stewardship, **not by commercial fusion economics**. The physics demonstrations happen whether or not Inertia/Xcimer succeed (synthesis §5 lines 153-154).
- This is *qualitatively different* from Helion's architecture-proof (which requires Helion to operate Polaris/Orion). NIF is already operating; the proof is *underway, government-funded, independent of company-level commercial outcomes.*
- **New sub-flavor of Layer A unconditional leverage: government-funded-independent-architecture-proof.**

**Thread 2 — DPSSL industrial supply-chain overlap (high regime-overlap):**
- Per synthesis §1 line 14: laser driver uses *"industrial supply chains (semiconductor diodes, optical components) rather than fusion-specific REBCO or Nb₃Sn superconductors."*
- DPSSL diodes have overlap with: defense (laser weapons), LIDAR (automotive, mapping), industrial materials processing, semiconductor lithography. **Regime-overlap = high**, comparable to ARC's HTS-into-MRI/grid/transport.

**Thread 3 — HYLIFE-III liquid-wall heritage (design lineage durable):**
- The 1992 SOMBRERO/OSIRIS conceptual studies established the IFE plant architecture and tritium-breeding pathways (synthesis §5 lines 155-156). FLiBe TBR > 1.2 is from peer-reviewed published analysis.
- This is *durable design infrastructure* — engineering optionality that survives any single company.

**Layer B gate-conditional:**
- Target factory at <$1/target (Goodin 2007 baseline $0.17/target at NOAK).
- 10 Hz cycle (Inertia) or sub-1 Hz (Xcimer) at commercial yield.
- Specific NOAK numbers ($98/MWh, $300/J).

**Methodology observation #3:** Layer A is not monolithic — it decomposes into **sub-threads** with different durabilities and different mechanism types:
- *Architecture-proof* (Helion's direct conversion; 26's NIF ignition) — knowledge/method asset
- *Industrial supply-chain overlap* (ARC's HTS; 26's DPSSL) — manufacturing learning curve asset
- *Design-lineage heritage* (26's HYLIFE-III; not present in other traces) — engineering infrastructure asset

The strongest Layer A profiles (26, ARC) have multiple sub-threads; weaker profiles (Helion partial, Zap nominal) have one or zero. **GF's Layer-A-empty is the limit case of zero sub-threads.**

**Methodology observation #4:** Layer A strength correlates with cohort structure. Cohort-rich concepts (ARC private cohort, 26 NIF-cohort + IFE-family) have multiple Layer A threads because Layer A is *largely a cohort/ecosystem property, not a company property*. Cohort-isolated concepts (Helion isolated, Zap isolated, GF isolated) have weaker Layer A by construction. **This is a deeper structural finding than the dossier's current cohort-role tag** — the cohort/Layer-A relationship is mechanistic, not coincidental.

**Dossier update:** Row 4 dominant-leverage cell should read: `Layer A unconditional (HIGH, 3 sub-threads): (i) NNSA-funded NIF ignition demonstrations (government-funded-independent-architecture-proof); (ii) DPSSL industrial supply-chain overlap with defense/LIDAR/industrial-laser markets (regime-overlap=high); (iii) HYLIFE-III liquid-wall heritage from 1992 SOMBRERO/OSIRIS (durable design-lineage). Layer B gate-conditional: target factory <$1/target, 10 Hz cycle (Inertia) or sub-1 Hz (Xcimer), specific NOAK $98/MWh numbers.`

---

## Cell 4 — Fallback-floor

**Tag: EMPTY for 26-specifically; but in-family pivot paths exist.**

**Evidence:** The synthesis does *not* contain a "if X fails, fall back to Y" structural assertion analogous to Helion's §5 line 144 or GF's §5 line 166. However, §5 discusses several in-family pivot paths:
- Xcimer is already pivoting from direct drive to **Hybrid Direct Drive (HDD)** (§5 line 136) — higher coupling efficiency, potentially higher gain.
- **Fast Ignition** (concept 17b, Focused Energy) decouples driver/ignition (§5 line 138) — could reduce driver cost if timing/alignment solved.
- **Heavy Ion Beam ICF** (concept 25) replaces lasers with particle accelerators (§5 line 140) — different driver cost structure.

These are *pivots to adjacent IFE concepts*, not fallbacks within concept 26. If 26's gain gate fails, the methodology cannot collapse 26 to an adjacent concept the way Helion can collapse to D-T pulsed-FRC.

**Methodology observation #5:** This surfaces a **new field beyond fallback-floor**: **in-family-pivot-paths**. Helion has internal fallback (D-T within its own architecture). 26 has external pivots (to HDD, fast-ignition, HIB — all within IFE family but architecturally distinct). GF has neither. ARC has neither (its REBCO sensitivity is parametric, not pivot-based).

The methodology should distinguish:
- **Fallback-floor** (internal-to-concept): only Helion has this.
- **In-family-pivot-paths** (cohort-mutualized escape routes): 26 has multiple; ARC has stellarator/ST cohort but those aren't "pivots from ARC," they're parallel concepts.

**Recommendation:** Add `in-family-pivot-paths` as an optional inline note in Layer A leverage (since pivots are cohort-mutualization, which is Layer A territory). For 26: `Cohort mutualization via HDD (Xcimer), Fast Ignition (Focused Energy), HIB-ICF — laser/target/optics knowledge transfers across IFE family.`

**Dossier update:** Row 4 — no fallback-floor cell, but Layer A leverage note adds cohort-mutualization via in-family pivot paths.

---

## Cumulative methodology side-notes (after 5 traces)

Side-notes accumulated from traces #1-#5; **not yet promoted to grammar revision**. Will revise after trace #6.

1. **Binary qualifier taxonomy (5 entries):** terminal | terminal-economically | with-fallback | sharp-cliff | (one more from trace #6?).
2. **Gate-type axis (5 entries):** physics | engineering-built | engineering-operational | manufacturing-cost | supply-chain. Each carries characteristic "what evidence retires this risk" implications.
3. **Layer A sub-threads (3 types so far):** architecture-proof | industrial-supply-overlap | design-lineage-heritage. Stronger Layer A profiles have multiple sub-threads.
4. **Layer A ↔ cohort correlation:** Layer A strength is largely a cohort property, not a company property. Cohort-rich → multiple Layer A threads. Cohort-isolated → weak Layer A. GF Layer-A-empty is the limit case.
5. **Basis-type sub-flavors within joint-multi-gate:** same basis-type can have different dominant uncertainties (Helion: capacitor $/J; 26: availability). The dominant uncertainty within the joint product is decision-relevant.
6. **Fallback-floor vs in-family-pivot-paths:** distinct mechanisms. Internal-to-concept fallback (Helion D-T) vs cohort-mutualized pivots (26 → HDD/FI/HIB).
7. **Synthesis-quote-anchoring pattern (now 3 instances):** GF §5 line 166 "no fallback"; Helion §5 line 144 "D-T fallback"; **26 §5 line 163 "economically nonviable" if G<10**. When syntheses carry direct structural assertions, dossier should quote-anchor. *This is now the trace-#3/4/5 methodology default.*
8. **Capability-gap sub-flavors (3):** not-enough-of-right-class (ARC); wrong-technology-class (Helion); information-absent (GF q_eng); **manufacturing-curve-dependency** (26 laser $/J — partial-disclosure-with-trajectory-unproven, distinct from GF's information-absent).

---

## What this trace did NOT do

Per stopping rule: did not consult dossier.md or iter-N; did not exhaustively enumerate F-codes; did not re-open Parts A/D/E; did not write methodology revision (deferring until after trace #6). ~1h, single-source.
