---
Verdict: concerns
Created: 2026-07-20
Reviewer: skeptical independent (fresh session)
Related Artifacts:
  Design: ./design.md
  Spec: ./spec.md
  Brief: ../../orchestration/handshake-lcoe-construction.md
  Anchor: ../../../.project/active/demo-anchor-acceptance-spec/spec.md
  Upstream: ../../completed/20260720_WI-028_handshake-account-scope/design.md
---

# WI-029 Design Review — Handshake LCOE construction (CAS70/80 + IDC)

## Verdict: **REVISE** — two genuine must-fixes, both cheap and localized

The design is strong and its analysis holds up under independent verification. Every headline number was re-checked against 1cfe source at pin `0254385` by importing and calling the actual functions (not trusting the design's table), and **all of them reproduce**. The codegen-envelope ruling was re-checked against the `06d95f8` pin *object* (all worktrees drifted, as the design warns), and the allow-list, the byte-identical-lowering claim, and `preserve_handwritten` all confirm. The CAS10 single-error/zero-residual ruling is arithmetically forced and confirmed. The 1.5043→1.439 refutation is correct. The MR-WI029-9 `total_capital` finding is correct and properly surfaced.

Two defects survive verification. Neither invalidates the approach; both are fixable with a small design touch-up before `/plan-model`. Both live on the CAS72 handwritten rung and its trap table — the one part of the design that is a hand-written Python impl rather than codegen, and therefore the part with no automatic envelope to catch a mistake.

---

## What I verified (and it held)

**Re-derivation (pin `0254385`, by direct function call + oracle `onecfe_point.json`):** every value CONFIRMED.

| Claim | Design | Verified | Verdict |
|---|---|---|---|
| CAS71 | 79.004 | 79.00362 | ✓ |
| Levelization factor | 1.439 (1.5043 REFUTED) | 1.439046, constant in `annual_om` | ✓ — spec's 1.5043 is refuted correctly |
| annual_om split | 54.900 handshake / 52.517 design | 54.900 (p_net 1000) / 52.517 (p_net 915.08) | ✓ — oracle field `annual_om_unlevelized_musd` = 54.900 |
| Tc | 8 (NOAK), 10 (FOAK) | `_total_project_time` returns 8.0 / 10.0 | ✓ |
| CAS72 chain | 82.230, n_rep=4, full chain | q_n 3.12851, FPY 5.75354, cal 6.39282, event 671.160, s 0.64887, n_rep 4, pv 1020.396, cas72 82.230 | ✓ every intermediate |
| replaceable set | (C220101, C220108) | `defaults.py:299` exact | ✓ |
| CAS80 | 0.769, ×1.19 burn | 0.76907, (0.95/0.05)×0.01=0.19 | ✓ |
| CAS90 / LCOE | 813.587 / 123.743 | 813.587 / 123.743 | ✓ |
| CAS10 reconstruction | 32→16 gives 18.5, residual 0, no 2nd error | land 2.5 common; studies Δ = 20−4 = 16.0 exactly; contingency 0 both sides | ✓ single error forced |

**Codegen envelope (pin `06d95f8` object):** allow-list is exactly `{+ − * / ** ^}` at `calc_compat_renderer.py:39-46`; `**` takes arbitrary operands; every `InvocationNode` hard-fails at `:76` and routes to `MANUAL_REQUIRED`; no conditional/comparison node exists in the IR. The `extraction/` directory diffs to **nothing** pin→HEAD (lowering behavior unchanged, as claimed). `preserve_handwritten` is at `cli/__init__.py:91,478` at the pin. All CONFIRMED.

**IDC-independence (design point 4):** CONFIRMED sound. CAS71/72/80 levelization depends only on `i, g, n, Tc`. Neither IDC option touches those — Option (i) changes `total_capital` and the CAS90 multiplier; Option (ii) adds a separate 1cfe-form CAS90 channel. `Tc = construction_time = 8` is shared by both the levelization and both IDC forms and is unchanged either way. CAS10 is likewise IDC-independent. No hidden coupling.

**A-4 completeness under each open IDC option (design point 8):** CONFIRMED. Under Option (ii), at the handshake point the 1cfe-form CAS90 channel = `CRF·(overnight+CAS60)` matches 1cfe under A-2 (overnight matches 1cfe once CAS10 is fixed at the point), cas70/cas80 match, so the 1cfe-form LCOE reconciles with only the C220106_pump ($0.721M) itemized remainder. Under Option (i) the convention line *closes* and only the pump remains. The D6 verdict artifact carries the convention line "per gate," so it is structurally correct under both. The A-4 dual condition is satisfiable regardless of the gate outcome — the gate picks *which* channel is the headline, not *whether* A-4 can be written. Design's claim holds.

**MR-WI029-9 finding (design point 5):** CONFIRMED and correctly surfaced. `precon_fixed_base` is power-independent and flows into `overnight = total_capital`, so the CAS10 fix lowers the design-point total by exactly $16M to ≈$16,129.7M ($16,145.7M − $16M). The spec's "total_capital unchanged" is genuinely wrong; the design refutes it loudly per capture-fidelity §4 rather than asserting-unchanged. This is a design strength, not a defect.

**D2b / MR-3 / MR-4:** the checklist lands every `.sysml` edit region-identical in both trees, recaptures the snapshot from the staged tree, and runs the mirroring diff gate — inherited correctly from WI-028. The two flat-Real library defs in `prototype/wi029_lcoe_construction.sysml` parse clean, use only `+ − * / **`, carry fuel constants as instance inputs, and hold no Stellaris literal. MR-3/MR-4 compliant. (`'DT Fuel Cost'` naming follows the WI-022 `'DT Fusion Power'` precedent — fuel-typed, not concept-specific.)

---

## Must-fix

### MF-1 — The handwritten CAS72 impl (and its oracle mirror) must carry `clip` and both `max` guards verbatim, not drop them as "documented no-ops"

**Where:** design.md §CAS72 codegen-envelope ruling (lines 83, 89, 97, 101) and §Proposed design D1 (line 166); the "Clip caveat" para.

**What's wrong.** The design's codegen-envelope analysis is correct — for *codegen*, `ceil`, `clip`, and both `max` calls are all `InvocationNode`s that break the arithmetic-only envelope, and at the pinned point only `ceil` is numerically *live* (clip and the maxes are inert). That analysis is fine and should stay. The defect is that the design lets that "only ceil is live" reasoning drive the **handwritten** implementation: it describes the impl as computing "FPY with the inert clip documented" and "n_rep via ceil," and the Clip-caveat paragraph frames dropping `clip` as a "documented no-op tied to this operating point."

The handwritten `_impl.py` is plain Python. **It has no envelope constraint at all** — the arithmetic-only limit applies only at the SysML→codegen boundary. So there is *zero cost* to reproducing 1cfe's `_core_lifetime_fpy` (`jnp.clip(fluence/jnp.maximum(q_n,1e-6), 0.5, lifetime·avail)`, `model.py:102-111`) and `levelized_replacement_cost` (`n_rep = jnp.maximum(0.0, jnp.ceil(n/t)−1.0)`, `economics.py:53-75`) **bit-for-bit, guards included.** Dropping them buys nothing and adds risk:

1. **Silent, discontinuous wrong result at study-sweep extremes.** If wall loading drops far enough, FPY hits the cap `n·avail` and `clip` goes live; if it rises far enough, FPY hits the 0.5 floor; a long replacement interval relative to plant life makes `ceil(n/t)−1 ≤ 0` and the outer `max(0,·)` goes live. An impl that dropped these returns a wrong CAS72 with no error — exactly the failure mode the design itself argues against three paragraphs earlier ("Do NOT freeze `n_rep` … it would fail *silently and discontinuously* … the worst failure mode," line 97). That argument applies with identical force to dropping `clip` and `max`; the design applies it to `n_rep` but not to the guards.
2. **No caveat for `max` at all.** The design surfaces the `clip` inertness caveat (good), but there is no equivalent for either `max`. `max(0, ceil(n/t)−1)` can go live the same way.
3. **The oracle mirror is only a check if it carries the guards too.** The mirror keeps the rung honest by recomputing CAS72 "a second way." If both the impl and the mirror drop `clip`/`max`, the mirror is blind to precisely the divergence it exists to catch. The design must state that the mirror reproduces the full guarded chain.

**Fix.** State plainly that the handwritten `_impl.py` and the oracle mirror both reproduce 1cfe's `_core_lifetime_fpy` and `levelized_replacement_cost` verbatim — `clip(·, 0.5, n·avail)`, inner `max(q_n, 1e-6)`, and outer `max(0, ceil(n/t)−1)` all carried in code, not as point-inert no-ops. This makes sweep-extreme correctness structural and retires the "re-verify inertness if inputs move" obligation entirely. Keep the codegen-envelope analysis ("only `ceil` is live") as the justification for *why the account is on the manual rung* — it is correct and belongs there; it just must not shape the impl toward dropping guards.

### MF-2 — The planned levelization trap cannot catch a wrong `annual_om` base; it validates only `i/g/n/Tc`

**Where:** design.md §D4 Trap assertions, item 1: "Assert the 1.439 factor materializes (cas71/annual_om at the handshake point)."

**What's wrong.** The design's own D1-a proves the levelization factor is **mathematically constant in `annual_om`** (the levelization is linear in the base, so `cas71/annual_om` depends only on `i, g, n, Tc`). Verified: the factor is 1.439046 regardless of base. That means the planned trap — asserting `cas71/annual_om ≈ 1.439` — will read 1.439 **whether `annual_om` is the correct handshake-point 54.900 or the wrong design-point 52.517.** It validates the levelization inputs but is blind to the exact duty-7 error it is meant to guard — the one the design itself names "the duty-7 trap in miniature" (D1-b).

A-5 is [HARD]: every mapping asserted, never left to "the default handles it." The `annual_om` base injection (p_net=1000 → 54.900, over the design-point 52.517) is a mapping this item newly relies on, and the trap that names it does not test it.

**Fix.** Add an explicit trap asserting the handshake-point `annual_om` base = **54.900** (i.e. p_net=1000 injected, not the design-point 52.517), independent of the factor check. Note: the end-to-end A-2 `cas71 = 79.004` comparison row *does* catch a wrong base (52.517 would give cas71 = 75.57, failing A-2), so this is not an uncaught-correctness hole — it is a trap-discipline completeness gap under A-5, which requires the localized assertion so a failure points at the base rather than surfacing only as a downstream A-2 miss.

---

## Should-fix

- **SF-1 — "four lowering files byte-identical" is under-specified, and one file it leans on did drift.** The design says "these four lowering files are byte-identical `06d95f8`↔HEAD" but names only two (`calc_compat_renderer.py`, `expression_compiler.py`). The substantive claim holds — the whole `extraction/` directory diffs to nothing pin→HEAD. But `cli/__init__.py` (relied on for `preserve_handwritten` at `:91,478`) **is not** byte-identical pin→HEAD (an Item-12 guard was added elsewhere in the file; lines 91/478 are untouched). Either name the four files or drop the count, and state explicitly that `cli/__init__.py` drifted but the `preserve_handwritten` lines are unaffected — and that the plan checks out the pin worktree regardless, so it runs against the pin object either way. This tightens the pin-safety story rather than leaving a loose "four."

- **SF-2 — citation precision, `expression_compiler.py:108`.** Line 108 is inside the compilability aggregator, not the `CompilationError`-catch/`MANUAL_REQUIRED` site (that is ~305-313, with the circular-dependency `MANUAL_REQUIRED` path at 255-265). "Accurate in spirit," but the catch site is the load-bearing line — cite 255-311 for the routing and drop 108 or label it as the aggregator.

- **SF-3 — design-point re-baseline should name its IDC option.** Validation Plan step 5 records "the new Stellaris headline," but under Option (i) the model's headline LCOE convention changes (drops `idc_factor`) while under Option (ii) it does not, so the recorded design-point LCOE differs by option. State which option the recorded re-baseline is taken under (or record both), so the headline is not ambiguous once the gate is ruled.

---

## On the reserved IDC gate (not reviewing the option choice)

Per the brief (ruling 3, OPEN with options), I did not review the option *choice*. I did check the two things asked: the analysis is **sound** — the multipliers (model 1.310796 even-spend-midpoint vs 1cfe 1.282476 uniform-spend closed form) genuinely differ, the +2.208% capital-charge gap is real, and adopting 1cfe's form would change the model's own headline, so "genuine convention choice, not mechanical fall-out" is the correct call and mirrors WI-028's D4. And the non-dependent design **is** truly IDC-independent: CAS71/72/80/CAS10 verified above to not move under either option; only the CAS90/LCOE tail wiring is gated. Parking it for owner with options is the right disposition.

## On the CAS10 stop condition (ruling 4)

The stop condition does **not** fire, and the design is right to say so. The divergence is arithmetically forced to a single error: land (2.5) is common to both sides, so the entire +$16.0M is the studies term (foak 20 − noak 4 = 16.0 exactly), and contingency is 0 on both sides at NOAK. The `precon_fixed_base` 32→16 reconstruction gives 18.5 with zero residual, and no second candidate cause carries nonzero contribution. The WI-025 "×1.10 exactly" doc note is a stale FOAK tail contributing zero — correctly diagnosed as documentation hygiene, not an independent error. Clean single error; closure is warranted.

---

## Summary

Approach approved; numbers verified end-to-end; two localized must-fixes on the handwritten CAS72 rung and its trap before `/plan-model`. MF-1 (carry `clip`/`max` verbatim in the impl and mirror) removes a latent silent-wrong-result at sweep extremes at zero cost. MF-2 (explicit `annual_om = 54.900` trap) closes an A-5 gap the factor-trap cannot cover. Fold both into a short `/design-model` touch-up, then plan.

ARTIFACT: work/active/WI-029_handshake-lcoe-construction/design-review.md
