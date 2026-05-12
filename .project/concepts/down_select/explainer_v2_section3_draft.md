# Explainer — Method and Worked Examples

The explainer has four sections. Sections 1 and 2 already exist in `explainer_outline.md` (Journey + what history teaches at each stage) and stand. This draft covers Section 3 (The Method) and Section 4 (Worked Examples). There is no separate "what this isn't" section.

---

## Section 3 — The Method

The method has three steps: trace, tag, map.

### Trace

For each candidate, walk through Stages 2, 3, and 4. At each stage, assess how the concept sits on the three factor types Section 2 introduced.

The intrinsic features: capital cost of the minimum viable plant, build time, site-specialization fraction, replication unit size, learning mechanism.

The ecosystem-relational features: regulatory framework, critical-component supply, specialty inputs. Each spans a failure pole (no ecosystem support; must internalize the gap) and a leverage pole (strong ecosystem support; rides existing industrial currents). Where supply dynamics matter, tag the assessment slack or bottleneck.

The ecosystem-distinct leverage: crossover platforms that bring non-fusion investment to the concept's components, intra-fusion cohorts whose combined demand scales shared supply chains, shared sub-problem R&D that amortizes across concepts.

Stage 1 enters only when it's the binding question. We don't adjudicate physics claims. But for concepts whose physics gate is genuinely open — a Z-pinch that has not reached Q ≥ 7, a D-He3 machine five times below ignition temperature — we record that the concept's binding uncertainty lives at Stage 1.

### Tag

From the trace, identify two factors and one structural feature.

The **primary failure factor** is the one whose closure is most uncertain at time of analysis. The deep-dive's value lives where the answer isn't yet known: study what's open, not what's already obvious. When two or three factors are genuinely co-uncertain (gain, laser-diode cost, and plant availability all open at once for laser-driven indirect-drive IFE), record them jointly.

The **primary leverage** is the strongest tailwind. Mark it *unconditional* when it operates whether the concept ships or not — an HTS gigafactory underwritten by MRI and grid demand keeps running regardless of fusion's outcomes. Mark it *gate-conditional* when it only pays off if the concept's binding factor resolves first — a factory-modular architecture only delivers a learning curve if the underlying physics closes.

Record the concept's **cohort position**: first-mover in a rich cohort, first-mover isolated, fast-follower, or adjacent to a non-fusion cohort. One tag per concept.

### Map

Plot the traced concepts on a 2D space. Primary failure factor on one axis. Primary leverage on the other. The axes are categorical lists, not continuous scores — entries like "Stage 3 supply chain bottlenecked at fleet scale" or "crossover platform from MRI / grid / transport, unconditional."

Concepts cluster into cells. Some cells are crowded; many are empty. The populated cells reveal the structure of the fusion landscape: which bets are crowded, which are unique, which aren't being made at all.

---

## Section 4 — Worked Examples

Two concepts traced end to end. The pair is chosen to contrast: one engineering-gated with strong ecosystem leverage and a rich cohort; one physics-gated, ecosystem-thin, isolated. The method should produce visibly different outputs for them. If it does, the method discriminates.

### Example A — 01 ARC (compact HTS tokamak, CFS)

**Stage 1 entry.** Compact-tokamak physics draws on ITER, JET, JT-60, and multiple private programs. SPARC is expected to demonstrate Q > 1 in 2027–28. Stage 1 is not a binding factor; the discount on downstream value is small.

**Stage 2.** Minimum viable plant cost is ~$12.6B for FOAK ARC — above the ~$5B threshold where the buyer pool shrinks to sovereigns and hyperscaler consortia. Build time is 7–10 years post-SPARC, within the regulatory-ratcheting risk zone. The NRC's Part 30 framework (finalized February 2026) is a Stage-2 leverage — fit-for-purpose regulatory pathway, lower burden than Part 50/52. Critical-component supply sits at the failure pole on REBCO (CFS is vertically integrating its tape manufacturing — singleton internalization) and on FLiBe / Be / tritium (no industrial base). The HTS crossover platform — MRI, grid interconnects, transport — is the dominant ecosystem-distinct leverage: it underwrites the REBCO gigafactory CFS must build, and the gigafactory has a non-fusion revenue floor even if ARC stalls.

**Stage 3.** Site-specialization is modest (modular components, demountable joints, ship-and-install architecture). Replication unit size is ~400 MWe — a hyperscaler can plausibly anchor a small fleet. Supply-chain maturity at chasm scale is the central failure mode: at fleet scale, ARC plus seven other fusion concepts plus growing non-fusion HTS demand all compete for REBCO production capacity. Whether external markets keep the supply slack or combined demand pushes it into bottleneck is genuinely open. Regulatory amortization is favorable: standardized design plus SPARC precedent should let the second plant inherit the licensing template. The intra-fusion REBCO cohort — eight concepts — is the strongest ecosystem-distinct leverage at this stage.

**Stage 4.** Cost-reduction mechanism is mixed — REBCO descends a volume-driven learning curve from external pull; plant integration descends an R&D-driven curve from CFS-fleet learning. The concept has four to five independent cost-reduction knobs; the REBCO knob has strong non-fusion ride-along, the rest are fusion-funded. At fleet scale, non-fusion REBCO demand from MRI + grid + transport probably co-dominates fusion demand, which means the REBCO cost floor is not bounded by fusion deployment volume alone. FLiBe and lithium-6 have no external market; their cost floor is fusion-determined.

**Tag.** Primary failure factor: REBCO supply trajectory at fleet scale, bottleneck-tagged. Most uncertain at time of analysis — the supply curve could descend cleanly to $10/kA-m or stall at $50, and combined-cohort demand could push it either way. Primary leverage: the HTS crossover platform — MRI / grid / transport — unconditional. Cohort position: first-mover, cohort-rich.

**Map cell.** Stage-3 supply-chain bottleneck × crossover-platform unconditional. Other compact-HTS tokamaks would land in the same cell or adjacent; state-backed full-HTS tokamaks (different supply-chain economics) land in a neighboring cell.

### Example B — 15 Zap (sheared-flow-stabilized Z-pinch)

**Stage 1 entry.** Sheared-flow stabilization is a recent paradigm with one organized program (Zap Energy, ~$200M raised). Q achieved to date is below 1. The Stage-1 gate is open and binding: if SFS Z-pinch cannot reach Q ≥ 7 at commercial current and pinch lifetime, the concept produces no net electricity at any cost, on any timeline. Stage 2–4 risks exist but are conditional on this gate closing.

**Stage 2.** Minimum viable plant cost is unspecified in the public record — no FOAK design beyond a 50 MWe modular unit concept. Build time is unestimated. Regulatory: D-T fusion, Part 30 framework applies (shared leverage with the entire D-T cohort). Critical-component supply is the structurally interesting feature: pulsed-power capacitors and switches at the required ratings and shot-counts are a *capability-class gap* — the supply class itself doesn't exist at the scale and lifetime Z-pinch fleet would need, distinct from a quantity gap where supply exists but volume must scale. Crossover platforms are limited: pulsed-power has defense applications, but the overlap with Z-pinch's specific requirements is partial.

**Stage 3.** Site-specialization is favorable: modular factory-built 50 MWe units, ship-and-install. Replication unit size is small — twelve units is feasible for a hyperscaler anchor. Supply-chain maturity at chasm scale is again capability-class-gap on pulsed-power components; whether the supply class develops by chasm-era volumes is uncertain and depends on whether the broader pulsed-power-MIF cohort (Z-pinch, MagLIF, others) scales together. Regulatory amortization rides the D-T cohort. Intra-fusion cohort leverage on pulsed-power is thin — three or four concepts, not eight.

**Stage 4.** Cost-reduction mechanism is volume-driven if the cohort builds at all — many small units, factory-manufacturable, in principle on a solar-like trajectory. Modularization is structurally favorable (small unit, factory-built). But the cost-reduction knobs at Stage 4 depend on pulsed-power components, which have no dominant non-fusion market. Cost floor is fusion-bounded.

**Tag.** Primary failure factor: Q ≥ 7 physics gate at Stage 1. Binary, terminal — the most uncertain factor in the trace, the question whose answer would determine whether anything downstream is real. Primary leverage: factory-modular architecture (Stage 3 + Stage 4). Gate-conditional — its value materializes only if the Q-gate closes. Cohort position: first-mover, isolated.

**Map cell.** Stage-1 physics gate × factory-modular leverage gate-conditional. No other shortlist concept occupies this exact cell. The closest neighbor is Helion (Stage-1 physics gate × architecture-proof leverage *unconditional*) — same failure-axis row, opposite leverage-axis column.

### What the two examples show

ARC's binding uncertainty lives at Stage 3 supply scale; Zap's lives at Stage 1 physics. ARC's leverage operates regardless of whether ARC ships; Zap's only operates if Zap's physics gate closes. ARC sits in a cohort of eight; Zap is alone. The method places them in cells separated on both axes of the map, with different conditionality on the leverage axis and different cohort positions on the structural tag. The two deep-dives would resolve completely different questions and produce non-overlapping outputs — which is what a methodology meant to discriminate among candidate deep-dives is supposed to do.
