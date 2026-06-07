---
date: 2026-06-05T14:54:24-07:00
researcher: Claude
topic: "Relative `cost_overrides` against `generic.costs.casXX` — double-discount hypothesis"
tags: [research, costingfe, concept-analysis, cost-overrides, scaling]
status: complete
last_updated: 2026-06-05
---

# Research: Does `value = X * generic.costs.casYY` double-discount small-scale concepts?

**Date**: 2026-06-05
**Researcher**: Claude
**Research Type**: Codebase / Library semantics

## Research Question

The user observed that `exploration/concept_analysis/analyses/24-dense-plasma-focus/model_setup.py`
writes cost overrides as multiples of `generic.costs.cas21` (etc.) for a 5 MWe device
("0.05 × generic.costs.cas21 because the device is small"). They hypothesized that
because `generic = generic_reference(model, spec, P_native)` already runs the
library at `P_native = 5 MWe`, the small-size effect is *already in*
`generic.costs.cas21`, and multiplying by 0.05 double-discounts.

Tasked: (1) trace the scaling of each CAS account inside 1costingfe; (2) trace
the override mechanism (`cost_overrides` + `override_reference_mw`) used by
`run_native_and_1gw`; (3) confirm/refute; (4) find other concepts with the
same pattern.

## Summary

- **Native LCOE column: hypothesis CONFIRMED.** At the native forward,
  `override_reference_mw == net_electric_mw == p_native`, so `_scale_overrides`
  multiplies by ratio = 1.0 — the user's literal value passes through. With
  `value = 0.05 * generic.costs.cas21`, the native CAS21 equals 5% of the
  *already-small-device* CAS21. The author's stated intent ("~100× reduction
  vs. a conventional fusion plant") collapses to "100× × ~20× ≈ 2000× reduction."
- **1 GWe projection LCOE (the headline number): hypothesis REFUTED.**
  `_scale_overrides` runs an internal reference forward at
  `(p_native, n_mod=1)` and a target forward at `(1000 MWe, n_mod=N)`, both
  override-free, and replaces the user's value with
  `value · (target_cas / ref_cas)`. The ref and the author's anchor are the
  same quantity (`generic.costs.cas21`), so the ratio cancels:
  final override = `0.05 · ref_cas21 · (tgt_cas21 / ref_cas21) = 0.05 · tgt_cas21`.
  The 1 GWe column correctly expresses "5% of the library's natural 1 GWe-scale
  CAS21 for this concept with N modules."
- **Net effect**: the native LCOE is artifactually low for small-`P_native`
  concepts that use the `X * generic.costs.casYY` (or `... * generic.cas22_detail[..]`)
  pattern, while the 1 GWe headline LCOE that `run_model` greps is correct
  *for the author's stated intent* ("fraction of a conventional plant"). The
  `generic → native` column in `print_cas_breakdown` therefore tells a
  misleading story for these concepts: it shows the override at face value,
  which under-represents what the framework will eventually inflate it to
  at 1 GWe.
- **17 concepts** use the relative-override pattern at `P_native < 1000 MWe`.
  The severity grows as `P_native / 1000` shrinks; concept 24 (5 MWe), 08 (50),
  18 (50), 37 (50), 29 (90), 23 (100) are the most exposed.

## Detailed Findings

### 1. How each CAS account scales inside 1costingfe

Reference points are 1 GWe-class (`P_ET_REF=1150`, `P_TH_REF=2500`, `P_FUS_REF=2300`).
All powers (`p_net`, `p_et`, `p_th`, `p_fus`) derive from `net_electric_mw`
via the layer-2 power balance (`physics.py:285`).

| Account | Scaling | n_mod | Source |
|---|---|---|---|
| CAS10 (land) | land ∝ `p_net · √n_mod`; rest fixed | √n_mod (land only) | `costs.py:54-69` |
| CAS21 (buildings) | per-building **linear**: `base[fuel] · (p_X / P_X_REF)` summed; some buildings "fixed" (ratio=1) | none | `costs.py:72-113` |
| C220101 (blanket) | `vol · (p_th/2500)^0.6` | ×n_mod | `cas22.py:220` |
| C220105 (structure) | `vol · (p_et/1150)^0.5` | ×n_mod | `cas22.py:406` |
| C220110 (remote handling) | `(p_et/1000)^0.5` | ×n_mod | `cas22.py:531` |
| C220111 (labor) | frac × reactor subtotal | `1 + (n−1)·multi_unit_labor_factor` | `cas22.py:550` |
| C220200 (cooling) | linear `p_net_total` + `(p_th_total/3500)^0.55` | uses `n_mod·p_*` | `cas22.py:567-572` |
| C220500 (fuel handling) | `(p_net_total/1000)^0.7` | uses `n_mod·p_net` | `cas22.py:604` |
| C220600 (radwaste) | `(p_net_total/1000)^0.8` | uses `n_mod·p_net` | `cas22.py:610` |
| CAS23 / 24 / 25 / 26 | linear in `p_the` / `p_et` / `p_th` | linear ×n_mod | `costs.py:116-148` |
| CAS27 (special mats) | linear `p_net/1000` | none | `costs.py:170` |
| CAS28 (digital) | fixed | none | `costs.py:179` |
| CAS40 (capitalized indirect) | `(p_net/1000)^0.5` | none | `costs.py:223` |
| CAS70 (O&M) | `(p_net/1000)^0.5` | none directly | `costs.py:281-324` |
| CAS80 (fuel) | `p_fus`, availability | ×n_mod | `costs.py:409+` |

**Key:** CAS21 has *no* 0.6 power-law — it is a weighted linear blend with
fixed pieces. So `generic.costs.cas21` at P_native = 5 MWe is dominated by the
"fixed" buildings, not 5/1150 of the 1 GWe value.

### 2. The override / re-scaling mechanism

`forward()` does two things with `cost_overrides`:

1. **Re-scale step** (`model.py:470-483, 991-1043`): if `override_reference_mw`
   is given and differs from `net_electric_mw`, `_scale_overrides()` runs two
   internal, override-free forwards (one at `(reference_mw, n_mod=1)`, one at
   `(target_mw, caller_n_mod)`) and replaces each user value with
   `value · (target_account / reference_account)`. For CAS22 sub-accounts it
   uses `cas22_detail`; for top-level rollups it uses `costs.casXX`.
2. **Inject step** (`model.py:631-846`): the rescaled dict `co` is consulted
   as `co.get("CASxx", default_formula(...))` — pure replacement, no extra
   multiplier.

Helper-call mapping for `run_native_and_1gw`
(`exploration/concept_analysis/scripts/lib/model_setup_helpers.py:147-176`):

- **Native** (`net_electric_mw = override_reference_mw = p_native`, `n_mod=1`):
  the two internal forwards inside `_scale_overrides` are *identical*, so the
  ratio is exactly 1.0 for every account. **The user's override value passes
  through verbatim.**
- **1 GWe projection** (`net_electric_mw = 1000`, `override_reference_mw = p_native`,
  `n_mod = round(1000/p_native)`): the ratio is the library's *own*
  account-by-account scale-up from `(p_native, 1)` to `(1000, N)`. The
  override gets re-anchored to 1 GWe scale.

### 3. Resolution of the hypothesis

Substituting `value = 0.05 · generic.costs.cas21` (where `generic` was the
no-override forward at `p_native`, identical to what `_scale_overrides` uses
as its reference):

- **Native CAS21** = `0.05 · generic.costs.cas21` ← already-small × 0.05.
  *Double-discount confirmed for this column.*
- **1 GWe CAS21** = `0.05 · generic.costs.cas21 · (cas21_at_1GWe_N / cas21_at_p_native_1)`
  = `0.05 · cas21_at_1GWe_N`. *No double-discount — exactly "5% of the
  library's natural 1 GWe answer with N modules."*

This works for *any* account whose override anchor is `generic.costs.<attr>`
or `generic.cas22_detail[<key>]` from the *same* `generic_reference` call —
the reference value the author used *is* the same value `_scale_overrides`
divides by. The ratio cancels.

**The "bug" surfaces only in the native LCOE / native CAS column** of the
generic/native/1 GWe table emitted by `print_cas_breakdown` — and that column
exists specifically to show the override effect at design-point scale, where
it now reports a value that has been (small-scale × author-fraction)-discounted
without any re-anchoring back to the author's stated reference baseline
("vs. a conventional fusion plant"). The headline LCOE that downstream
tooling consumes is the 1 GWe projection and is fine.

### 4. Two interpretations of "X * generic.costs.casYY"

The pattern is ambiguous and the framework resolves it differently per column:

- **Interpretation A** ("fraction of a conventional 1 GWe plant"):
  the rationale in concept 24 says "~100× reduction in building volume vs. a
  conventional fusion plant" and "the ~200× power reduction." The 1 GWe
  column matches this intent; the native column does not.
- **Interpretation B** ("fraction of the library's answer for *this* sized
  device"): would make the native column correct and the 1 GWe column over-
  shoot. Concept 12 (`1.34 * generic.cas22_detail["C220103"]`) and concept
  17a (`1.25 * generic.costs.cas21`) — both inflations rather than
  reductions — only make sense under interpretation B (the library default
  already includes scale, the author is correcting upward for archetype-fit
  reasons). Under interpretation A those would mean "1.34× of a 1 GWe
  reference at small native scale" which is nonsensical.

The codebase mixes interpretations. The framework picks A by construction
(re-anchor at projection), but the native-column reader sees B.

## Affected concepts (relative override against `generic.costs.casXX` or `generic.cas22_detail[..]`, `P_native < 1000`)

Searched with `grep -rEn '(generic\.costs\.cas|generic\.cas22_detail\[)'` over
all `analyses/*/model_setup.py` (including `iter-N/` snapshots) and joined
against the file's declared `P_native`.

| Concept | P_native (MWe) | Pattern | Severity (rough) |
|---|---:|---|---|
| 24-dense-plasma-focus | 5 | CAS21, 24, 26, 27, 70; C220105, C220110 | **highest** — 200× ratio |
| 08-frc-w-direct-conversion | 50 | C220103, C220109 (as fraction of `generic.costs.cas22`) | high |
| 18-p-b11-frc | 50 | C220101, C220102 | high |
| 37-magnetized-target-inertial-fusion-mtif | 50 | CAS21 (note: declared as `lambda: 0.70 * generic.costs.cas21` — see "Open Questions") | high |
| 29-negative-triangularity-tokamak | 90 | CAS70 only | moderate |
| 23-laser-icf-nanostructured-target | 100 | C220101/02/06, CAS21, CAS70 | moderate-high |
| 06-magnetic-mirror | 150 | C220102 only (1% scaler) | low (small fraction × small override) |
| 14-MTF-pneumatic-compression | 150 | C220101/04/07 | moderate |
| 22-projectile-icf | 150 | C220102, C220110 (sub-account preamble too) | moderate |
| 12-levitated-dipole | 208 | C220103 (1.34× — inflate), CAS70 (0.05× of C220103) | mixed — CAS70 anchor is *also* relative to C220103, double indirection |
| 17a-laser-icf-hybrid-drive | 400 | C220101/02/08, CAS21 (1.25×), CAS70 | moderate |
| 04-laser-icf | 500 | C220101/02, C220110, CAS21, CAS70 | low-moderate |
| 10-large-scale-stellarator | 1000 | CAS21, CAS70 — both `enabled: False` | **none** (overrides disabled; also at projection scale) |

Counts: **12 active concepts at sub-1 GWe** use the relative-anchor pattern
with at least one enabled override. Iteration snapshots (`iter-1/2/3/`) under
the same concepts inherit the pattern.

## Code References

- `exploration/concept_analysis/analyses/24-dense-plasma-focus/model_setup.py:62`
  — `P_native = 5.0`
- `exploration/concept_analysis/analyses/24-dense-plasma-focus/model_setup.py:114,146,161,178,202`
  — the five CAS-rollup relative overrides
- `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:85-112`
  — `generic_reference`: plain forward at `(p_native, n_mod=1)`, no overrides
- `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:147-176`
  — `run_native_and_1gw`: both forwards pass `override_reference_mw=p_native`
- `/home/reid/1cfe/1costingfe/src/costingfe/model.py:991-1043`
  — `_scale_overrides`: the rescale ratio mechanism
- `/home/reid/1cfe/1costingfe/src/costingfe/model.py:470-483`
  — where `_scale_overrides` is invoked from `forward`
- `/home/reid/1cfe/1costingfe/src/costingfe/model.py:631-846`
  — the `co.get("CASxx", default)` injection points
- `/home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py:72-113`
  — CAS21 buildings: linear blend with fixed pieces, refs at 1 GWe class
- `/home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py:220,406,531,604,610`
  — CAS22 power-law scaling exponents (0.6, 0.5, 0.5, 0.7, 0.8)

## Architecture Insights

- `_scale_overrides` is **deliberately designed** so that the analyst writes
  the override in the design-point frame (`(p_native, n_mod=1)`) and the
  framework re-anchors automatically when projecting. The shared helper
  `run_native_and_1gw` matches that contract (both forwards pass
  `override_reference_mw=p_native`). The 1 GWe projection thus does *not*
  double-discount.
- The `generic / native / 1 GWe` print block is reading the override at three
  different conceptual frames: `generic` = library default, no override;
  `native` = override at literal face value (rescale ratio = 1); `1 GWe` =
  override re-anchored to 1 GWe. The `generic → native` "isolates override
  effect at fixed scale" framing in the helper docstring (`model_setup_helpers.py:16`)
  is mathematically true but **interpretively misleading** when the author's
  override was authored against a 1 GWe-conventional baseline — the column
  is reporting the override applied at p_native scale only.
- The `_scale_overrides` mechanism imposes a hidden constraint on how
  relative overrides *should* be authored: the multiplier must be the
  fraction-vs-1GWe-baseline interpretation (A), not the fraction-vs-this-device
  interpretation (B). Concept 12 and 17a appear to use B (multipliers >1.0
  authored against a same-scale baseline), which produces a 1 GWe projection
  that *over*-applies the inflation by the library's own scale ratio.

## Feasibility Assessment

Two questions for the user:

1. **Is the user's hypothesis the bug, or is the `_scale_overrides` mechanism
   the bug?** The 1 GWe headline LCOE — the number `run_model` greps and
   reports as the cross-concept comparable — actually behaves correctly under
   interpretation A. The native LCOE column is the affected one.
2. **Are concepts 12 and 17a (multipliers > 1.0) authored under interpretation
   B?** If so, their 1 GWe projection LCOEs are inflated by an additional
   library-scale factor on those accounts.

## Recommendations

Possible follow-up directions, depending on the user's intent:

- **If the native LCOE is the artifact of concern**: document the column's
  semantics in `print_cas_breakdown`'s docstring; the existing "isolates
  override effect at fixed scale" framing is incomplete. No code change
  needed if the headline 1 GWe number is the comparison axis.
- **If the user wants the native column to reflect "5% of a conventional plant"
  baseline at native scale**: the override anchor must be a `generic_reference`
  computed at 1 GWe, not at `p_native` — and `override_reference_mw` must be
  set to 1000.0 for both forwards. Concept files would change to:
  `generic_at_1GWe = generic_reference(model, spec, 1000.0)`
  `value = 0.05 * generic_at_1GWe.costs.cas21`
  …and the helper would need a different `override_reference_mw`.
- **If concepts 12 and 17a were authored under interpretation B**: their
  multipliers need to be reinterpreted (and likely adjusted) so the 1 GWe
  projection is what the analyst intends. Worth flagging to the analyst who
  authored each before any framework-level decision.
- **Independent of the above**: the `relative override against
  generic.costs.X` pattern is fragile under interpretation drift. A typed
  helper (`relative_override("CAS21", 0.05, baseline=generic, intent="vs_1GWe")`)
  could make the author's intent explicit and pick the right anchor.

## Open Questions

- Concept 37 declares `"value": lambda: 0.70 * generic.costs.cas21` — a
  *lambda*, not a number. The Override TypedDict declares `value: float`.
  Is this a typo, or is there a code path that resolves lambdas? Worth
  checking before relying on the 37 row.
- Concept 12 uses CAS70 anchored to **C220103** (`0.05 * generic.cas22_detail["C220103"]`).
  CAS70 is a top-level rollup; the library's CAS70 scaling (`(p_net/1000)^0.5`)
  is unrelated to C220103 ((p_th/2500)^0.6 or similar). The `_scale_overrides`
  ratio for CAS70 will be the *CAS70* ratio, not the C220103 ratio — so the
  author's "anchor to C220103" choice survives only at native; the 1 GWe
  rescale will use the CAS70-by-CAS70 ratio. Worth verifying with the
  concept-12 author.
- The two interpretations (A vs. B) appear inconsistently across the corpus.
  Is there an authoritative spec that should pick one? Search of
  `.project/active/` for `concept-rework-three-forward-contract` design notes
  might already address this — recommended next step before any change.

## Addendum (2026-06-05): Where the misunderstanding enters the pipeline

Follow-up investigation into the prompt templates that drive `analyze` and
`model_setup` to identify where the relative-override semantics fail to reach
the authoring agent.

### Origin in the design doc

`.project/concepts/concept-analysis-rework-design.md:178` is the canonical
phrasing the prompts inherit:

> `0.70 * generic.costs.cas21`, "70% of the library's computed value because
> the company states a 30% prefab reduction"

The author was thinking **interpretation A** (the framework re-anchors via
`_scale_overrides`, so the multiplier means "fraction of the library's
*projected* answer"). But the phrase "the library's computed value" is silent
about which scale baseline, and the surrounding context (`generic` = "bare
answer for a reactor this size") nudges the reader toward interpretation B.
Line 198 ("Every cost override is interpreted at the design-point reference …
The library scales each to the call's `(net_electric_mw, n_mod)` per the
account's own scaling law") states the *mechanism* but not the *semantic*
implication for how to author the multiplier.

### Where it shows up in the runtime prompts

1. **`prompt_templates/model_setup_costingfe.md:133-137`** — the gloss on the
   `generic` line ("the library's bare answer for a reactor this size, and
   the reference a relative override is written against") frames `generic` as
   the small-device answer, full stop. No mention of `_scale_overrides`
   re-anchoring at projection time.

2. **`prompt_templates/model_setup_costingfe.md:141-147`** — the inline
   example anchors `C220101` (a sub-account) to `generic.costs.cas21` (a
   top-level rollup), contradicting Rule 5's storage-shape rule a few lines
   below. The rationale ("30% structure cost reduction from modular fab vs
   library default; 0.70 x library CAS21") is exactly the A/B ambiguity at
   issue — prose anchored on "library default" without specifying scale.

3. **`prompt_templates/model_setup_costingfe.md:269-289`** (Rule 5 relative-
   override section) — explains the *syntactic* choice between
   `generic.costs.<rollup>` and `generic.cas22_detail["..."]` but is silent on:
   - That `_scale_overrides` divides by the unmodified `generic` value at
     projection time, so the ratio cancels and the headline equals
     `multiplier × library_at_1GWe_with_N_modules`.
   - That the multiplier therefore expresses "fraction of the library's
     natural projection answer," not "fraction of the small-device answer."
   - That the native LCOE column displays the multiplier at face value
     (ratio=1) and is *not* calibrated against the analyst's stated baseline.

4. **`prompt_templates/output_template.md:137-151`** (Section 5b YAML schema,
   where `analysis.md` first proposes overrides):

   > "Relative `value` expressions reference the library's bare overrides-off
   > cost (`generic.costs.cas21`), never `native` or `result_1gw`."

   Tells the analysis agent *what variable to multiply by*, but not what the
   multiplier means semantically. The analysis agent then writes a rationale
   anchored to "conventional fusion plant" (interpretation A) while writing a
   value anchored to the small-device library default (interpretation B);
   both pass their respective validators because they're never cross-checked.

5. **`exploration/concept_analysis/scripts/lib/model_setup_helpers.py:16-17`**
   (helper docstring, leaks into agent mental models via example output):

   > "`generic → native` isolates the override effect at fixed scale"

   True mechanically, but the column shows the override at face value
   (rescale ratio = 1.0) regardless of which baseline the analyst was
   reasoning against. For sub-1 GWe concepts using A-style multipliers, the
   native column reports a number with no calibration to the rationale's
   stated frame — yet it's printed as a peer of the headline LCOE in the
   breakdown.

### What to add

The single highest-leverage edit is one paragraph in `model_setup_costingfe.md`
Rule 5 and a mirror in `output_template.md` Section 5b:

> **What the multiplier means.** When you write `value: M * generic.costs.cas21`
> (or `M * generic.cas22_detail["..."]`), the library at projection time
> replaces the computed account with `M × library_at_1GWe_with_N_modules` —
> the ratio against `generic` at `P_native` cancels. The multiplier therefore
> expresses **"fraction of the library's natural answer for this concept at
> the projection scale"** (the 1 GWe headline frame), not "fraction of the
> small-device library default." Author both the multiplier and the rationale
> against the 1 GWe-projected baseline (e.g. "vs. a conventional 1 GWe fusion
> plant"). The native LCOE column shows `M × generic.costs.cas21` at face
> value (no rescale at native, since `override_reference_mw == P_native`); for
> sub-1 GWe concepts this is *not* calibrated to the rationale's baseline and
> is for override-mechanism inspection only — not for comparison to the
> headline.

Plus a mechanism aside on the `generic` line gloss (`model_setup_costingfe.md:133-137`):

> `generic` is the library's no-override answer at `P_native`, used both as
> the writing frame for relative overrides *and* as the reference the
> framework divides against when projecting them to 1 GWe (`_scale_overrides`
> in `1costingfe/src/costingfe/model.py:991`). The same `generic` value
> appears on both sides of that ratio, so the multiplier you write survives
> unchanged at projection; what scales is the library's own per-account
> answer.

And fix the inconsistent inline example: switch the demonstrated account from
`C220101` to a top-level rollup (e.g. `CAS21`) so it actually models the
top-level pattern correctly per Rule 5.
