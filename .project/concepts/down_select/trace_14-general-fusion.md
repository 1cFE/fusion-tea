# Trace #4 — 14 General Fusion (MTF Pneumatic Compression) — targeted dossier-cell fill

**Scope:** Targeted trace per entry 010 stopping rule. Goal: defend the cells flagged `[thin]` in row 3 of `decision_dossier_draft_v0.md` Part B. Single-source read of `14-magnetized-target-fusion-pneumatic-compression/synthesis.md` (§1-7).

**Companion traces:** `trace_01-hts-compact-tokamak.md`, `trace_15-sfs-z-pinch.md`, `trace_08-helion.md`.

---

## Cell 1 — LCOE floor (point, band, basis, epistemic)

**Point:** $104/MWh at 300 MWe FOAK; $78/MWh at 1000 MWe (synthesis §1 line 16).

**Band:** $70 → $150/MWh — a **factor-of-~2 band**, narrower than Helion's trifurcated $50-$500+ but wider than ARC's $200-$300.

**Basis:** **Engineering-bounded with a binary-engineering gate.** This is a *new fourth basis-type* the methodology hasn't named yet. Comparison across traces:

| Concept | Basis-type |
|---|---|
| ARC | Post-FOAK engineering (REBCO supply curve sensitivity) — band tightens as supply matures |
| Zap | Physics-gated (Q-gate distance) — band undefined until physics closes |
| Helion | **Physics × manufacturing × conversion** (3 independent gates, joint product) |
| **GF** | **Engineering-gated** (pneumatic compression never built at commercial scale) — band is bounded conditional on the engineering gate closing |

GF's failure mode is *not* physics (LM26 will likely demonstrate Lawson criterion in 2026 per synthesis §7) — it's *the commercial pneumatic compression system has never been built*. Per synthesis §1 line 12: *"a binary viability gate, not a parametric uncertainty."*

**Epistemic:** Single-gate-conditional on commercial pneumatic compression feasibility (the engineering gate). Within that condition, three co-dominant LCOE uncertainties:
- Compression driver capital: $50M-$500M (±$200M around $180M), elasticity +0.16 — *but the range is 10×, dwarfing the elasticity coefficient*.
- Recirculating power fraction (q_eng): 2.0-4.0 against assumed 3.0, elasticity -0.50.
- Capacity factor: 50-90% against assumed 80%, elasticity -0.98 (near-unity, the strongest LCOE multiplier).

Joint propagation per §6 line 189: "factor of ~2× uncertainty band: 70-150 $/MWh."

**Dossier update:** Row 3 LCOE-floor cell should read: `($104/MWh at 300 MWe FOAK, $78 at 1 GWe; band $70-$150; engineering-gated on commercial pneumatic compression feasibility; within-gate uncertainty co-dominant on driver capital × q_eng × availability)`.

---

## Cell 2 — Dominant failure (with qualifier)

**Tag:** `F_engineering binary-terminal (commercial pneumatic compression never built) × F2.d capability-gap (recirculating power fraction undisclosed)`

**Primary component (binary-terminal):**
- The commercial pneumatic compression system at 1 Hz / 4 m cavity / synchronized piston array has never been tested at any scale. LM26 uses an electromagnetic theta-pinch surrogate compressing a solid lithium liner — a *fundamentally different mechanism* from the commercial concept.
- The synthesis is unusually direct about the failure mode: §5 line 166 — *"If unsuccessful, there is no fallback — the concept's viability is binary on pneumatic compression feasibility."*
- Qualifier: **binary-terminal**. Same qualifier as Zap's F1 binary, but the *gate type is different*: Zap's is Stage-1 physics; GF's is Stage-1 engineering.

**Methodology observation #1:** The v1 binary/degrading qualifier and the trace-#3 tripartite split (terminal | with-fallback | sharp-cliff) need a **second orthogonal axis: gate-type** = `physics | engineering | manufacturing-cost | supply-chain`. Same qualifier (binary-terminal) can apply to qualitatively different gates:

| Concept | Binary-terminal? | Gate type |
|---|---|---|
| Zap | Yes | Physics (Q-gate, sheared-flow stabilization at reactor scale) |
| **GF** | **Yes** | **Engineering (pneumatic compression never built)** |
| Helion F1 | No (binary-with-fallback) | Physics (D-He3 ignition) |
| Helion F7 | No (binary-sharp-cliff) | Engineering (90% direct recovery) |

This is a 2D grammar: qualifier × gate-type. Trace #3 surfaced the qualifier axis; trace #4 surfaces the gate-type axis.

**Secondary component (F2.d capability-gap, but with a special character):**
- Recirculating power fraction (q_eng) is *entirely undisclosed* by General Fusion. Steam-driven piston recharge energy per pulse is the dominant unknown.
- This is not "wrong technology class" (Helion's capacitor) or "not enough of right class" (ARC's REBCO). It's **information-absent capability-gap**: the technology exists but the *parameter value* is undisclosed.
- Qualifier: capability-gap + information-absent (a sub-flavor of capability-gap, not a new qualifier — but worth noting).

**Dossier update:** Row 3 dominant-failure cell should read: `F_engineering binary-terminal, gate-type=engineering (commercial pneumatic compression never built; no fallback per synthesis §5) × F2.d capability-gap, information-absent (q_eng undisclosed)`.

---

## Cell 3 — Dominant leverage (with qualifier)

**Tag:** `Layer A: empty (no unconditional layer) | Layer B gate-conditional: liquid-metal-wall architecture (4π breeding + self-renewing PFC + zero consumables)`

**Critical structural finding:** **GF has no unconditional leverage layer.** This is the first trace where the Layer-A/Layer-B decomposition from trace #3 *collapses to a single layer.*

Comparison across traces:

| Concept | Layer A (unconditional) | Layer B (gate-conditional) |
|---|---|---|
| ARC | HTS curve, MRI/grid/transport overlap (regime-overlap=high) | F2.a $12.6B FOAK |
| Zap | Modularization-claim → external markets thin (regime-overlap=nominal) | Q-gate physics |
| Helion | **Direct-conversion architecture proof + pulsed-power capacitor curve** | F3.b modularization × NOAK cost numbers |
| **GF** | **EMPTY** | Liquid-metal-wall architecture + zero-consumables + 4π breeding + HTS-elimination |

**Why empty:** The synthesis is explicit — §5 line 166: *"If unsuccessful, there is no fallback."* The pneumatic compression architecture has **no external-market overlap** (synthesis §3 Risk 1: piston synchronization at <1% timing in an activated, liquid-metal environment has "no industrial analogues"). Industrial reciprocating compressors exist, but the GF-specific configuration is sui generis — regime-overlap=nominal-to-none, which is below the threshold for portfolio-valuable unconditional leverage.

The liquid-metal-wall innovation (4π breeding, self-renewing, no PFC replacement, no consumables) is *architecturally valuable*, but it is **gate-conditional on the compression system working** — nobody else's machine can use a liquid-metal wall the way GF's does. Other MIF concepts (MagLIF, Pacific Fusion) use electromagnetic liner compression with solid wall, not flowing liquid metal vortex.

**Dossier update:** Row 3 dominant-leverage cell should read: `Layer A: empty (no unconditional leverage; no external-market overlap; "no fallback" per synthesis §5). Layer B gate-conditional: liquid-metal-wall architecture (4π breeding + self-renewing PFC + zero per-shot consumables + HTS-elimination); contingent on pneumatic compression viability.`

**Methodology observation #2:** "Layer A empty" is a structural finding for the dossier. It is the **strongest signal that a concept is portfolio-fragile** — if Layer B fails, nothing remains. This is qualitatively different from Helion (Layer A persists if Helion fails) and ARC (Layer A *is* the main leverage). The dossier should flag Layer-A-empty concepts as carrying disproportionate portfolio risk — they're "all eggs in the gate" picks.

**Methodology observation #3:** The corollary is that **Layer-A-emptiness is decision-relevant for the 5-set composition.** If GF stays in the set, the dossier should acknowledge it is in *despite* having no unconditional leverage layer — included only because MTF + liquid-metal-wall + mechanical compression *would be* unique architectural information *if the gate closes*. This shifts the portfolio rationale from "leverage-driven" to "axis-coverage-driven" for this specific pick. The set's slot 3 is a pure axis-coverage slot, not a leverage slot.

---

## Cell 4 — Fallback-floor (new optional field introduced in trace #3)

**Tag:** **EMPTY / N/A.**

**Evidence:** Synthesis §5 line 166 explicitly: *"If unsuccessful, there is no fallback."*

This is the second confirmation across traces #3 and #4 that **fallback-floor is Helion-specific**:
- ARC: empty (REBCO is not architecturally substitutable; if HTS doesn't reach $10/kA-m, ARC operates at higher LCOE but doesn't convert).
- Zap: empty (Q-gate terminal; no fallback).
- **Helion: D-T fallback at $150-200/MWh.** *(Sole instance.)*
- **GF: empty** (explicit no-fallback in synthesis).

**Dossier update:** Row 3 — no fallback-floor field needed. Across the 4 traces, fallback-floor is a single-row field (only row 2). Confirms entry 010's hypothesis that this is an optional row-specific field, not a universal column. Recommend keeping it as an optional inline note in the LCOE-floor cell rather than promoting to a separate column.

---

## Methodology side-notes (for eventual revision pass)

Cumulative side-notes from traces #3 + #4:

1. **Binary qualifier tripartite (from trace #3): terminal | with-fallback | sharp-cliff.** Confirmed by trace #4 — GF reuses binary-terminal (same as Zap).
2. **Gate-type axis (new from trace #4):** `physics | engineering | manufacturing-cost | supply-chain`. Orthogonal to the binary/degrading axis. Two concepts can share a qualifier but differ in gate-type — Zap (binary-terminal × physics) vs GF (binary-terminal × engineering) — and these are different decision objects.
3. **Layer-A-empty pattern (new from trace #4):** When leverage decomposition collapses to a single (gate-conditional) layer, the concept is portfolio-fragile. The dossier's risk-if-dropped column should distinguish Layer-A-empty concepts because their *included rationale* is axis-coverage, not leverage.
4. **Basis-type taxonomy now has 4 entries** (one per trace): post-FOAK-engineering (ARC), physics-gated (Zap), joint-multi-gate (Helion), engineering-gated (GF). Worth promoting to a Part-B field if a 5th basis-type emerges from traces #5 (26 NIF-heritage) or #6 (28 China HH380).
5. **Capability-gap sub-flavors:** Helion = "wrong technology class" (capacitor $/J 10× short). GF = "information-absent" (q_eng undisclosed). ARC = "not enough of right class" (REBCO supply curve). Three sub-flavors of v1 grammar Change 2. The grammar needs to support distinguishing them.
6. **Synthesis-quote-anchoring for "no fallback" assertions:** The GF synthesis was unusually direct — *"If unsuccessful, there is no fallback"* (§5 line 166). When a synthesis explicitly asserts no-fallback, the dossier can quote it directly. Helion's synthesis was similarly direct about D-T fallback (§5 line 144). **Recommendation:** when filling fallback-floor cells, look for direct synthesis assertions first; only infer from CAS structure if no direct quote exists.

---

## What this trace did NOT do

Per stopping rule:
- Did not consult dossier.md, iter-N files, or model outputs.
- Did not exhaustively enumerate F-codes for stages 2/3/4.
- Did not re-open Parts A/D/E or the 5-set selection.
- Did not write up the methodology revision (collect through trace #6, then revise).

**Total scope:** 4 dossier cells filled (3 substantive + 1 confirmed empty); 6 cumulative methodology side-notes (2 new from this trace, 4 confirmed/extended from trace #3); ~1 hour.
