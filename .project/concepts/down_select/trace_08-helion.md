# Trace #3 — 08 Helion (FRC + Direct Conversion) — targeted dossier-cell fill

**Scope:** This is a **targeted trace**, not a full `concept_part2.md` template population. Goal: defend the 4 cells marked `[thin]` in row 2 of `decision_dossier_draft_v0.md` Part B. Per entry 009 stopping rule: populate exactly what the dossier needs, surface methodology observations as side-notes, stop.

**Source:** `exploration/concept_analysis/analyses/08-frc-w-direct-conversion/synthesis.md` (entire file, single read). No additional sources consulted — synthesis self-contained for the 4 cells.

**Companion:** `trace_01-hts-compact-tokamak.md`, `trace_15-sfs-z-pinch.md`.

---

## Cell 1 — LCOE floor (point, band, basis, epistemic)

**Point:** $50/MWh (NOAK, 1 GWe scale, model output per synthesis §1 line 18).

**Band:** $50 → $500+/MWh **plus a D-T-fallback shelf at ~$150–200/MWh**.

This is the *widest* LCOE band of any shortlist concept by a factor of ~3 and is **structurally different** from ARC's and Zap's bands:

| Concept | Floor → ceiling | Basis | Band character |
|---|---|---|---|
| ARC | $200 → $300 | engineering-bounded (REBCO curve, FOAK overrun) | tight, single-axis sensitivity |
| Zap | $145–200 → $500 | far-thin physics × early-cohort engineering | wide, uncertainty-bounded |
| **Helion** | **$50 → $500+ plus fallback shelf at $150–200** | **physics-gate × manufacturing-gate × efficiency-gate (3 independent gates) + D-T-fallback floor** | **trifurcated** |

**Basis:** Joint product of three independent gates, each with its own basis type:
1. **Physics gate (binary):** D-He3 ignition at ~65 keV. Helion's current 13 keV → 5× temperature gap. *Below threshold, the gate doesn't close — the concept falls back to D-T, not to a slightly-higher-LCOE D-He3.* (Synthesis Risk 1, §3, lines 62–65.)
2. **Manufacturing gate (degrading):** Capacitor $/J. Today's $5/J → target $0.50/J. *Degrades LCOE proportionally rather than producing a binary failure.* (Synthesis line 74.) At $5/J, LCOE > $500/MWh even with all other gates closed.
3. **Conversion-efficiency gate (binary, sharp):** Direct recovery ≥90%. Per synthesis line 30: *"At the ARPA-E design point (η_coupling=0.2, Q=1.2), net electricity requires eta_recovery ≥ ~90%. A drop from 95% to 85% eliminates net output entirely — this is a go/no-go parameter, not a gradual penalty."* Cliff at 90%.

**Epistemic:** **Multi-gate-conditional with a fallback shelf.** This is a new pattern the dossier didn't anticipate. ARC's $240/MWh is *NOAK-conditional* (single gate: REBCO $10/kA-m). Helion's $50/MWh is *joint-NOAK-conditional* (three gates: physics + manufacturing + conversion). The joint probability is meaningfully smaller than any single-gate concept's NOAK probability.

**Critically:** *the fallback shelf is structural*, not just a worst-case estimate. If gate 1 (D-He3) fails, Helion does not die — it operates as a pulsed D-T machine with capacitor-bank driver, losing direct conversion's full benefit (~75%) and requiring a tritium-breeding blanket. The synthesis estimates the D-T fallback at $150–200/MWh (§5 line 144). **This makes Helion an unusual portfolio member: its downside scenario is not "kill" but "convert to a different and more expensive but still operable concept."**

**Dossier update:** Row 2 LCOE-floor cell should read: `($50/MWh point, $50–$500+ band with D-T-fallback shelf at $150–200/MWh, joint-gate-conditional on D-He3 ignition + capacitor $0.50/J + 90% direct recovery, physics×manufacturing-bounded)`.

---

## Cell 2 — Dominant failure (with qualifier)

**Tag:** `F1.binary-with-fallback × F2.d-capability-gap-degrading × F7.binary-cliff-at-90%`

This is a **compound failure across three F-codes with two qualifier types stacked** — the most complex failure structure in the shortlist.

**F1 component (Plasma Performance, binary-with-fallback):**
- Physics: 5× temperature gap from 13 keV demonstrated to ~65 keV required.
- Failure mode: D-He3 doesn't ignite at commercial Q.
- Consequence on failure: **forced fallback to D-T architecture** (synthesis line 14 explicitly), not company death. LCOE rises to $150–200/MWh.
- Qualifier: **binary-with-fallback** — distinct from Zap's binary-terminal (Q-gate fails → company dies entirely).

**F2.d component (Driver — capability-gap, degrading):**
- Supply-chain shape: pulsed-power capacitor manufacturing is the *wrong technology class at current cost* — same shape as Zap's F2.d (per `trace_15-sfs-z-pinch.md` finding 3).
- Magnitude: 10× cost gap ($5/J → $0.50/J).
- Qualifier: **degrading** — proportional, not cliff. Synthesis line 74 explicit: *"degrades LCOE proportionally rather than producing a binary failure."*
- Note: capability-gap qualifier (v1 grammar Change 2) earns its keep here. ARC's REBCO is "not-enough-of-right-class" (slack); Helion's capacitor is "wrong-class-entirely" (capability-gap). Same code, different reality.

**F7 component (Power Conversion & BOP, binary at 90% threshold):**
- Efficiency cliff at 90% direct recovery.
- Qualifier: **binary-sharp-cliff** — go/no-go at 90%, not a continuous degradation.
- Distinct from F1 binary because the fallback is not D-T; it's "no net electricity at all." If F7 fails, the architecture itself doesn't produce power.

**Dossier update:** Row 2 dominant-failure cell should read: `F1 binary-with-fallback (D-He3 gate, fallback to D-T at $150–200/MWh) × F2.d capability-gap degrading (capacitor $/J 10×) × F7 binary-sharp-cliff (90% direct recovery)`.

**Methodology observation #1:** v1 grammar's binary/degrading qualifier (Change 5) needs a *tripartite split* on the binary side: **binary-terminal** (Zap) vs **binary-with-fallback** (Helion F1) vs **binary-sharp-cliff** (Helion F7). The first kills the concept; the second converts it to another concept; the third zeros the output without converting. These three are not commensurable.

---

## Cell 3 — Dominant leverage (with qualifier)

**Tag:** `E_arch.unconditional (direct-conversion architecture proof) + F3.b.gate-conditional (Helion's modular pulsed-FRC)`

The dominant leverage **decomposes into two qualitatively different layers** — only one of which depends on Helion succeeding.

**Layer A — Unconditional (architecture-level, persists even if Helion fails):**
- *Direct-conversion proof-of-architecture* at commercial relevance. Faraday-induction recovery from expanding magnetized plasma at 1–2 Hz × 40 T at GW scale is the engineering demonstration. Once shown, the architecture is licensable / copyable / repurposable.
- *Pulsed-power-capacitor manufacturing curve* — Helion's in-house capacitor manufacturing has external market overlap with grid stabilization, pulsed industrial loads, accelerator facilities, defense. The synthesis doesn't quantify this overlap directly, but the lever pattern matches ARC's HTS-supplier-effect: the *manufacturing learning curve is not concept-specific*. Operating-regime-overlap qualifier (v1 grammar Change 3): **partial** — defense + grid + accelerator pulsed loads overlap on $/J but at different stored-energy density and rep-rate envelopes. Not as broad as ARC's HTS-into-MRI/grid/transport (high overlap), but real.
- *D-He3 fuel-cycle demonstration* — even partial D-He3 progress informs every other D-He3 concept globally.

**Layer B — Gate-conditional (concept-specific, requires Helion's gates to close):**
- F3.b modularization: 50-MWe modules ×20 = 1 GWe. *Conditional on all three Helion gates closing* (physics, manufacturing, efficiency). Per the synthesis, the modularization claim doesn't operate as leverage if the underlying gates don't close — there's nothing to modularize.
- Specific NOAK cost numbers ($1706/kW overnight, $50/MWh) — gate-conditional.

**Dossier update:** Row 2 dominant-leverage cell should read: `Layer A unconditional: direct-conversion architecture proof + pulsed-power capacitor manufacturing curve (regime-overlap=partial). Layer B gate-conditional on D-He3 + capacitor + recovery: F3.b modularization (50 MWe × 20)`.

**Methodology observation #2:** v1 grammar Change 6 (unconditional/gate-conditional qualifier) is too coarse — it forces a single tag per leverage cell. Helion has *both layers simultaneously*. The grammar needs to allow **leverage-layer decomposition** (Layer A unconditional + Layer B gate-conditional), and the dossier cell should accommodate that decomposition rather than forcing a single tag. This is a new structural pattern that 01 and 15 don't exhibit:
- ARC: leverage is mostly unconditional (HTS curve, MRI/grid markets) — single layer.
- Zap: leverage is mostly gate-conditional (modularization claim only post-Q) — single layer.
- Helion: **both** — and the unconditional layer is the methodology's actual portfolio justification for including Helion (architecture proof is portfolio-valuable independent of Helion shipping).

---

## Cell 4 — Stage-1 binary-vs-degrading on D-He3 gate

Already addressed within Cell 2's F1 analysis. Recapping the qualifier:

**Tag:** F1 = **binary-with-fallback**.

**Distinguishing features vs Zap's F1 binary:**

| Feature | Zap F1 binary | Helion F1 binary-with-fallback |
|---|---|---|
| What fails | Q-gate physics (sheared-flow stabilization at reactor scale) | D-He3 ignition (temperature gap) |
| Consequence on failure | Concept dead; company dead. | Concept converts to D-T pulsed compression; remains operable but more expensive |
| Distance to gate | "Q achieved" ~0.0001, far-thin | 13/65 keV ratio, far-thin (5× gap) |
| Failure recovery | None: nothing to fall back to | Yes: D-T fallback at $150–200/MWh (synthesis §5 line 144) |
| Asymmetry | Symmetric (binary terminal) | **Asymmetric (binary on D-He3, but D-T fallback shelf preserves operability)** |

**Methodology observation #3:** The fallback-shelf concept means Helion's dossier should carry a **fallback-LCOE field** in Part B that other concepts may not need. This is a row-specific extension, not a grammar change. Suggest adding to Part B as `Fallback-floor: [optional, if concept has architectural fallback to a different gate-state]`. For Helion: `D-T fallback at $150–200/MWh (loses direct conversion + adds breeding blanket)`. For ARC: empty (no architectural fallback — REBCO is not substitutable). For Zap: empty (Q-gate is terminal).

---

## Methodology side-notes (for eventual revision pass)

Side-notes from this trace, surfaced for later methodology revision per entry 009 stopping rule:

1. **binary qualifier needs tripartite split**: binary-terminal | binary-with-fallback | binary-sharp-cliff. (v1 grammar Change 5 was too coarse.)
2. **Leverage cells should support layer decomposition**: unconditional Layer A + gate-conditional Layer B may coexist. (v1 grammar Change 6 was too coarse.)
3. **Fallback-floor is a new optional Part-B field**: only concepts with architectural fallback to a different gate-state need it. Helion needs it; ARC and Zap do not.
4. **Joint-gate-conditional epistemic** is qualitatively distinct from single-gate-conditional. Helion has 3 independent gates with joint probability product — meaningfully smaller than any single-gate NOAK. The methodology should flag "joint-gate count" as a top-level Part-B field, not buried inside LCOE-basis.
5. **Architecture-proof-as-portfolio-justification** is the actual reason Helion is in the 5-set. The dossier Part A.4 line *"thermal-cycle-free / blanket-free cost structure"* understates this — it's not just a cost structure, it's an architecture proof whose value persists independent of Helion's commercial success. This is the methodology's strongest argument for including a single high-risk concept in a 5-set.

## What this trace did NOT do

Per entry 009 stopping rule:
- Did not populate the full `concept_part2.md` template.
- Did not consult dossier.md, iter-N files, or model outputs.
- Did not exhaustively enumerate F-codes for stages 2/3/4 (irrelevant — Helion's dominant failure is Stage 1).
- Did not re-open Part E coverage matrix (the set is locked per entry 009).

**Total scope:** 4 dossier cells filled with defensible source-anchored basis; 5 methodology side-notes for eventual revision; ~1 hour of focused source reading + writing.
