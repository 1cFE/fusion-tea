I have enough context. Writing the review now.

---

# Critic Review — 01-hts-compact-tokamak

## Headline issues

1. **analysis.md and model_setup.py use different design points** — analysis.md pins P_native = 233 MWe (ARC 2015 conservative Pilot, explicitly selected as the only viable design point after routing out SPARC and the 2025 400 MWe target) while model_setup.py declares `P_native = 400.0` with the comment "We take CFS at its word on the commercial design while inheriting the published 2015 geometry/physics." The analysis itself wrote the disqualification: "The 2025 CFS target of 400 MWe has no published updated physics or geometry and cannot be used as a design point." The model does exactly that. The consequence is visible in the native forward output: `p_fus = 1019 MW` versus Sorbom 2015's converged result of 525 MW at the same R = 3.3 m geometry. The library is computing "what fusion power must this machine produce to yield 400 MWe net" — a question the 2015 design never answered. All three Sorbom cost overrides were calibrated for the 233 MWe machine; applying them at P_native = 400 makes the per-module cost basis inconsistent with the stated power level. Fix: set `P_native = 233.0` in model_setup.py, consistent with analysis.md.

2. **C220103 is the entire LCOE story; its 5–10× sensitivity range is not modeled anywhere** — The toggle probe shows C220103 alone responsible for Δ = −256 $/MWh when disabled, representing 86% of the 297 $/MWh library premium. The analysis correctly notes REBCO tape spans commercial target ($10/kA-m) to 2025 market ($100/kA-m) — roughly 10×. Held all else equal, the magnet cost scales proportionally: the headline 402.6 $/MWh sits somewhere in a range that likely spans 150–750 $/MWh. That range is not stated, not plotted, and not a named sensitivity in the result. A reviewer reading the output would see one number without knowing it is the midpoint of a decade-wide distribution. Fix: add a REBCO unit-price sensitivity table (e.g., at $10, $20, $50, $100/kA-m corresponding to ~$690M, $1.38B, $3.45B, $6.9B for C220103) reporting the resulting 1GWe LCOE at each step.

3. **Override provenance mislabeled: "direct" in model_setup.py, "derived" in analysis.md** — C220103, C220101, and C220106 are labeled `provenance: "direct"` in model_setup.py but `provenance: derived` in analysis.md. The Sorbom §6 cost methodology is explicit: "mass-proportional scaling at $1.06M/tonne benchmarked against four prior conceptual designs (FIRE, BPX, PCASTS, ARIES-RS)." That is derived arithmetic, not a procurement quote. `direct` provenance means the company published this exact dollar figure. Mislabeling inflates apparent evidential weight and obscures that the $6.9B figure embeds both the NOAK manufacturing assumption and the benchmarking uncertainty from four legacy designs. Fix: change all three to `provenance: "derived"` in model_setup.py.

4. **Two overrides appear in model_setup.py with no corresponding entry in analysis.md's Override Candidates section** — C220106 (Inconel VV, $123M) and CAS27 (FLiBe inventory, $146M) are in the model registry but absent from analysis.md. The pipeline contract requires override entries to flow from the analysis; entries that appear only in model_setup.py have no analyst-written rationale, source traceability, or reviewability in the canonical artifact. Their toggle deltas are small (−4.7 and −5.9 $/MWh), so the LCOE impact is not the concern — the traceability gap is. Fix: add both to analysis.md's Override Candidates section with the same six-field structure used for C220103 and C220101, or explicitly document why they were promoted directly to the model.

---

## Detailed reasoning

### Spec coherence

analysis.md describes exactly one named plant throughout: ARC (Sorbom et al. 2015), P_native = 233 MWe. The Design Point block is internally coherent — every parameter in the LCOE table (p_fus = 525 MW, net = 233 MWe, η_th ≈ 46%, p_input = 38.6 MW) traces to the same Sorbom 2015 calculation. The selection rationale correctly routes SPARC out (no net electrical output) and the 2025 400 MWe target out (no published updated geometry or physics). P_native = 233 MWe is the lower bound of the Sorbom "conservative Pilot" range, a defensible conservative choice. No stitching occurs within analysis.md.

model_setup.py breaks spec coherence at `P_native = 400.0`. The spec dict inherits R0 = 3.3 m, p_input = 38.6 MW, and η_th = 0.46 verbatim from the 2015 paper, but then declares the net output as 400 MWe. The library's native forward yields p_fus = 1019 MW — the physics it infers to produce 400 MWe net at the 2015 geometry — which is ~2× Sorbom's converged value of 525 MW. No validation of the plasma at 1019 MW in this geometry exists anywhere in the literature. The design principle states explicitly: "we take the company at its word on whatever named design we adopt." The 2015 design says 233 MWe. The 2025 commercial target of 400 MWe has no design we can adopt.

### Override discipline

**C220103 ($6,901M, labeled "direct")**: Arithmetic checks: $5.15B × 1.34 = $6,901M. ✓ But this is the fabricated cost for the 233 MWe machine; applying it at P_native = 400 without rescaling implies the same magnet mass serves 400 MWe — not independently supported. Disabling C220103 yields library default for CAS22.1.3 at native scale = 516.1 M$, which is a meaningful ARIES-calibrated reference and should be used as a lower bound comparator. Provenance should be `derived`.

**C220101 ($348M, labeled "direct")**: Arithmetic: $260M × 1.34 = $348M. ✓ Same Sorbom §6 origin, same 233 MWe machine, same provenance issue. probe_override_scaling.txt flags `ratio_current = 1.4671` vs `ratio_intended = 1.0000` — the library is applying an unintended ×1.47 rescaling to this override. The 1GWe C220101 value of 510.5 is therefore unreliable (it would be 348 × 2.5 = 870 if per-module, or 348 × 1.0 = 348 if fixed). Toggle delta is −30.3 $/MWh — not dominant, but not ignorable.

**C220106 ($123M, labeled "direct")**: Arithmetic: $92M × 1.34 = $123.3M ≈ $123M. ✓ Not in analysis.md. Same ratio_current = 1.4671 scaling bug. Toggle delta = −4.7 $/MWh — effectively noise at 1GWe scale. Excluding this override and relying on the library default would not materially change the result.

**CAS27 ($146M, "derived")**: Arithmetic: 950 t × $154/kg = $146.3M ≈ $146M. ✓ Not in analysis.md. The probe shows `ref_current = 2.40` vs `ref_intended = 6.00` — a distinct scaling bug from the C220101/C220106 pattern. The 1GWe CAS27 = 365.0 = 146 × 2.5, which looks correct, but the probe's reference mismatch suggests the internal calculation path is wrong. The 950 t FLiBe quantity is from the 233 MWe design; for a 400 MWe plant the inventory would scale up, but no published figure exists. Toggle delta = −5.9 $/MWh.

Could a reviewer flip any of these to `enabled: False` and get a meaningful library answer? Yes for C220103 (516.1 M$ native, ARIES-calibrated). For C220101, the library default for a solid-ceramic breeder blanket would be the comparison, which is architecturally distinct but still informative as a floor. For C220106 and CAS27, the library defaults are meaningful lower bounds. The override discipline criterion is met for C220103 and C220101; C220106 and CAS27 are marginal.

### Fit-grade vs. override count

High fit with 4 enabled overrides is right at the threshold (>4 is the suspicion zone). The High fit is reasonably earned: ARC shares the conventional tokamak cost structure for BoP (CAS23), structures (CAS21), and electrical systems (CAS24). The 4 overrides are concentrated in the nuclear island (CAS22 sub-accounts) and blanket inventory (CAS27) — exactly where REBCO and FLiBe diverge architecturally from the LTS archetype. The distribution makes structural sense for a High-fit concept.

However, C220106 (VV, −4.7 $/MWh) and CAS27 (−5.9 $/MWh) together contribute less than 3% of the headline LCOE. They are not doing real work. C220103 carries 86% of the override LCOE delta and C220101 carries another 7%. The two extra overrides are adding analytical noise and scaling bugs without corresponding analytical backing in analysis.md — they should be explicitly defended or removed.

### Two-knob projection

The call implements the standardized shape: `forward(net=1000, n_mod=2.5, availability=0.85, lifetime_yr=30, noak=True, override_reference_mw=400, **spec)`. The structure is correct.

probe_override_scaling.txt reveals that C220103 applies cleanly (ratio_current = ratio_intended = 1.0000) while C220101 and C220106 each have ratio_current = 1.4671 ≠ ratio_intended = 1.0000, and CAS27 has a separate reference mismatch. These are library bugs, not analyst errors, but they mean the 1GWe per-account values for C220101, C220106, and CAS27 are not the values the analyst intended. The headline LCOE of 402.6 $/MWh is mostly defensible because C220103 (the dominant account) is clean — but individual CAS22 sub-account values for C220101 and C220106 should not be cited until the library is patched.

The library-bare 1GWe LCOE of 105.7 $/MWh is a useful cross-concept lower bound — it represents a conventional LTS tokamak at 1 GWe at this geometry and availability assumption.

### Family delta vs comparables

The analysis correctly identifies the two structural bets that distinguish ARC: REBCO compactness and FLiBe liquid-immersion blanket. These are attributed to architecture, not presentation. The comparison with ST-E1 (21) correctly notes the shared REBCO supply chain risk without overstating cost comparability. The NT tokamak (29) comparison is correctly scoped to confinement physics, identifying that no magnet or blanket cost delta exists between the two approaches — the distinction is plasma operating regime, not cost structure. The state-backed tokamak (33) comparison correctly flags the LTS/HTS and scale incompatibility that prevents direct cost comparison.

One gap: the I-mode operating regime is cited as a qualitative reliability benefit (ELM elimination, reduced divertor erosion) but its capacity-factor impact is not quantified. If ARC's I-mode operation genuinely achieves higher availability than a conventional ELMing tokamak, this is a real architectural cost advantage that reduces LCOE relative to the 0.85 default. The design principle says "take the company at its word" — but CFS has not published an availability claim, so the correct treatment is to flag this as an upside uncertainty, not to model it.

### Gaps and load-bearing assumptions

The analysis correctly identifies the major gaps. The two most load-bearing assumptions, in order of LCOE impact:

1. **REBCO tape price at NOAK** — The Δ from C220103 alone spans the difference between 146.6 and 402.6 $/MWh. The commercial viability target of $10/kA-m is 10× below 2025 market; whether this is reached by 1GWe NOAK deployment is the central cost question for HTS tokamaks and currently has no published learning curve. This gap is correctly identified but should appear as a quantified sensitivity in the result, not only in the rationale text.

2. **Capacity factor** — The analysis correctly flags this as "the primary LCOE lever for a CAPEX-heavy plant" with a stated 2× LCOE swing between 50% and 90% availability. The 0.85 default is optimistic for an undemonstrated demountable-joint maintenance scheme. Bounding this gap with at least a two-point sensitivity (0.60, 0.85) would be more honest than a single default.

The FLiBe chemistry/tritium plant and blanket/VV replacement schedule gaps are real and correctly flagged. The BoP gap is acknowledged with a FECONS bound. The ARC 400 MWe geometry gap is correctly identified in analysis.md — though model_setup.py ignores the analysis's own conclusion here.

---

## What I deliberately did not say

- I did not independently verify the BLS CPI-U factor ×1.34. All three Sorbom-derived overrides move proportionally if this is wrong.
- I did not assess whether the Araiinejad & Shirvan (2025) $154/kg FLiBe NOAK price captures ⁶Li enrichment at 90% purity and 950 t quantity. ⁶Li enrichment is specialty chemistry and could dominate the FLiBe line item at that enrichment fraction.
- The H98 = 2.8 confinement factor at ARC parameters was not spot-checked against the DIII-D weak-shear basis cited in the analysis. If the I-mode H98 is materially lower, p_fus and Qe drop and the 233 MWe design point may not close.
- The probe_override_scaling.txt ratio semantics for C220103 (`ratio_current = ratio_intended = 1.0` with `ref_current = ref_intended = 516.10`) could reflect correct behavior — the override overrides the account at face value regardless of n_mod, with the library handling n_mod replication elsewhere. I cannot verify this without the library source.
- I did not evaluate whether the VV ($92M) or TiH₂ shield ($10M materials) cost figures from Sorbom 2015 are complete given that demountable joints require additional sealing and alignment hardware not present in a conventional welded VV.
