---
date: 2026-06-07T10:00:00-07:00
researcher: Claude
topic: "Which concepts may be suffering from inconsistent 1 GWe override semantics, and how to fix them"
tags: [research, costingfe, cost-overrides, 1gw-policy, concept-corpus, edit-pass]
status: complete
last_updated: 2026-06-07
related:
  - .project/research/20260606-093951_override-scaling-semantics-by-account-class.md
  - .project/reports/2026-06-06-1gw-estimate-policy.md
  - .project/active/prompt-updates-for-1gw-estimate-policy/spec.md
---

# Research: Concepts affected by the 1 GWe override-semantics policy, and how to rerun them

**Date**: 2026-06-07 · **Type**: Codebase audit + remediation feasibility

## Research Question

The override-semantics investigation (2026-06-06 policy doc) found that relative
overrides written as `M * generic.costs.X` can silently mean very different
things at the 1 GWe headline depending on the cost class of `X`:

| class | accounts | rescale ratio at STEP 3a | effect of a relative override at headline |
|---|---|---|---|
| **S** Shared / charged once | CAS10, CAS21, CAS40, CAS70 | **1.0** | `M ×` one small module → biased low (or high) vs analyst's mental "fraction of a 1 GWe plant" |
| **U** Per-unit (×n_mod) | C2201xx sub-accounts, CAS80 | **n_mod** | `M ×` the full fleet → matches "fraction of a conventional plant" |
| **P** Power-proportional | CAS23/24/25/26, plant-wide CAS22 sub-accounts | (size-invariant per MWh) | scales with output |
| **C** Blend | CAS22 rollup, CAS30/50/60 | between 1 and n_mod | partway between |

Concept 24 (Dense Plasma Focus) was reauthored under the new policy.
This research:

1. enumerates **which other concepts in the corpus carry relative overrides on
   Class-S or Class-C accounts**, or have an anchor/account class mismatch, so
   they're candidates for the same silent inconsistency, and
2. assesses **whether a targeted feedback/edit-pass rerun is feasible** as
   opposed to a full from-scratch re-extraction.

## Summary

- **13 concepts use relative overrides**: 04, 06, 08, 10, 12, 14, 17a, 18, 22,
  23, 24 (already fixed), 29, 37. Of these:
- **4 high-priority** for rerun (relative override on Class-S CAS21 or CAS70
  *and* enabled, sub-1 GWe scale, or visibly inconsistent rationale frame):
  - **04-laser-icf** (P=500, `0.50 * generic.costs.cas21` enabled) —
    rationale carries an internally-wrong NOTE claiming CAS21 is per-module and
    "total plant CAS21 = 139.9 × 2", which is the exact misconception the
    policy fixes (CAS21 is Class S, charged once).
  - **17a-laser-icf-hybrid-drive** (P=400, `1.25 * generic.costs.cas21`,
    `0.75 * generic.costs.cas70`, both enabled) — no scale-frame on the
    rationale; reads as "vs library default" with no modular-fleet anchor.
  - **29-negative-triangularity-tokamak** (P=90, `0.70 * generic.costs.cas70`
    enabled) — sub-1 GWe so the Class-S ×1.0 rescale bites; rationale says
    "Relative override: 70% of library CAS70" without naming the modular-fleet
    frame.
  - **37-magnetized-target-inertial-fusion-mtif** (P=50, `0.70 *
    generic.costs.cas21` — *disabled, blocked by 1cFE/fusion-tea#2*) — would
    be the worst case if enabled, because P_native = 50 MWe means n_mod = 20
    and the rescale gap is largest. Worth re-authoring now so the file is
    correct the day the block lifts.
- **1 medium-priority** for rerun (anchor/account class mismatch):
  - **08-frc-w-direct-conversion** (P=50) — two enabled sub-account overrides
    (`C220103` and `C220109`) carry the value `M * generic.costs.cas22`. The
    sub-account is Class U; the anchor is the Class-C CAS22 rollup. Per FR-2 of
    the prompt-update spec, an override's anchor must match its account's class
    (a sub-account uses `generic.cas22_detail["..."]`, not `generic.costs.cas22`).
- **Disabled-but-mismatched** (low priority — file hygiene, no behavioral
  impact): 10-large-scale-stellarator (disabled C220103 anchored to cas21;
  disabled CAS70), 12-levitated-dipole (enabled-but-token CAS70 anchored to a
  C220103 detail).
- **Not at risk**: 06-magnetic-mirror, 14-mtf-pneumatic, 18-pb11-frc, 22-projectile-icf,
  23-laser-icf-nanostructured (uses absolute values for all overrides; no
  surviving `* generic.costs` patterns). Their relative overrides — where they
  exist — are all Class-U sub-accounts (`generic.cas22_detail["C2201xx"]`)
  anchored to themselves, which the policy says is fine.
- **Feedback / edit-pass rerun is feasible and the right tool** for this
  fix. The pipeline already has `--feedback` on both `analyze` and `model-setup`
  subcommands of `run_analysis.py`; recent commits (`70b6fbe1`, `eb3d721f`) just
  unbroke the edit-pass model-setup convergence path. The right shape is a
  per-concept `pre_feedback.md` naming the specific Class-S or anchor-mismatch
  override(s) and quoting the policy invariant, then `run_analysis model-setup
  --concept N --feedback path/to/feedback.md`. This avoids cold-start
  re-extraction and re-research, keeping the dossier and analysis stable while
  just re-authoring the override registry rationale and (where needed) the
  account anchor.

## Detailed Findings

### Enumeration of every relative override in the corpus

Search performed: `grep -E '\* *generic\.costs|\* *generic\.cas22_detail'
**/model_setup.py` over `exploration/concept_analysis/analyses/`. Iter
artifacts elided; the canonical surface is each concept's top-level
`model_setup.py`.

| concept | P_native | account | value expression | enabled | account class | anchor class | risk |
|---|---:|---|---|:---:|:---:|:---:|---|
| 04-laser-icf | 500 | C220101 | `0.05 * generic.cas22_detail["C220101"]` | ✓ | U | U | none |
| 04-laser-icf | 500 | C220102 | `0.05 * generic.cas22_detail["C220102"]` | ✓ | U | U | none |
| 04-laser-icf | 500 | C220110 | `0.15 * generic.cas22_detail["C220110"]` | ✓ | U | U | none |
| **04-laser-icf** | 500 | **CAS21** | `0.50 * generic.costs.cas21` | ✓ | **S** | S | **HIGH — wrong note in rationale** |
| 04-laser-icf | 500 | CAS70 | `0.50 * generic.costs.cas70` | ✗ (disabled) | S | S | low (disabled) |
| 06-magnetic-mirror | 150 | C220102 | `0.01 * generic.cas22_detail["C220102"]` | ✓ | U | U | none |
| **08-frc-w-direct-conversion** | 50 | **C220103** | `0.04 * generic.costs.cas22` | ✓ | U | **C** (rollup) | **MED — anchor mismatch** |
| **08-frc-w-direct-conversion** | 50 | **C220109** | `0.08 * generic.costs.cas22` | ✓ | U | **C** (rollup) | **MED — anchor mismatch** |
| 10-large-scale-stellarator | 1000 | C220103 | `0.60 * generic.costs.cas21` | ✗ | U | S | low (disabled, also at-scale) |
| 10-large-scale-stellarator | 1000 | CAS70 | `1.15 * generic.costs.cas70` | ✗ | S | S | low (disabled, also at-scale) |
| 12-levitated-dipole | 208 | C220103 | `1.34 * generic.cas22_detail["C220103"]` | ✓ | U | U | none (self-anchored) |
| 12-levitated-dipole | 208 | CAS70 | `0.05 * generic.cas22_detail["C220103"]` | ✓ | S | U | low — strange anchor, but CAS70 not overridable today (1cFE/1costingfe#106) |
| 14-mtf-pneumatic | 150 | C220101/4/7 | `M * generic.cas22_detail["C2201xx"]` | ✓ | U | U | none |
| **17a-laser-icf-hybrid-drive** | 400 | **CAS21** | `1.25 * generic.costs.cas21` | ✓ | **S** | S | **HIGH — no scale-frame in rationale** |
| **17a-laser-icf-hybrid-drive** | 400 | **CAS70** | `0.75 * generic.costs.cas70` | ✓ | **S** | S | **HIGH — no scale-frame in rationale** |
| 17a-laser-icf-hybrid-drive | 400 | C220101/2/8 | `M * generic.cas22_detail["C2201xx"]` | ✓ | U | U | none |
| 18-p-b11-frc | 50 | C220101/2 | `M * generic.cas22_detail["C2201xx"]` | ✓ | U | U | none |
| **29-negative-triangularity-tokamak** | 90 | **CAS70** | `0.70 * generic.costs.cas70` | ✓ | **S** | S | **HIGH — sub-1GWe Class-S, no modular-fleet frame in rationale** |
| **37-mtif** | 50 | **CAS21** | `0.70 * generic.costs.cas21` (lambda) | ✗ (blocked by `1cFE/fusion-tea#2`) | **S** | S | HIGH if/when enabled |

### Why each high-priority concept is on the list

**04-laser-icf** — Class-S CAS21 with internally-wrong rationale.
Lines 168–190 of `exploration/concept_analysis/analyses/04-laser-icf/model_setup.py`
carry this CAS21 override with a NOTE that states:

> *"NOTE: CAS21 is a per-module account. At 1 GWe (n_mod=2) the output shows
> the same per-module value (139.9 M$) as native; total plant CAS21 is 139.9 * 2
> = ~279.8 M$, handled by n_mod aggregation downstream. The apparent lack of
> scaling is correct per-module behavior, not a bug."*

That NOTE is the exact misconception the policy doc fixes. CAS21 is Class S,
charged **once** at the fleet level — *not* multiplied by `n_mod=2`. The
analyst's mental model assumed the framework would multiply by `n_mod`; it
doesn't. The 0.50 multiplier intended "50% of a full-plant building scope" but
the framework delivers "50% of one 500 MWe-module's building scope" = 50% of
≈$139.9M ≈ $70M, *not* 50% of the conventional-1-GWe baseline. (For P=500 the
ratio bug is smaller than for sub-100 MWe concepts, but the *interpretation*
is still wrong and the NOTE has to be retracted.)

**17a-laser-icf-hybrid-drive** — Class-S CAS21 (1.25×) and CAS70 (0.75×) with
no scale frame named in the rationale. The CAS21 rationale says "1.25x
multiplier is an analyst estimate reflecting the larger footprint" — the
multiplier is ambiguous between "1.25× of one 400 MWe-module's building scope"
(what the framework will do) and "1.25× of a conventional 1 GWe plant's
building scope" (what the words imply). Under the new policy this must read
"1.25× of the library's default for a fleet of this device at 1 GWe."

**29-negative-triangularity-tokamak** — Class-S CAS70 (0.70×), and P_native=90
so the rescale gap is real. Rationale: "MANTA assumes ~1 person/MWe staffing
at $150k/employee-year = ~$15M/yr for 90 MWe plant. This is ~30% lower than
library default staffing assumptions for tokamaks. Relative override: 70% of
library CAS70." This reads as the value-frame-mismatch the policy warns about:
the bottom-up justification ("$15M/yr for 90 MWe") computes a *native-scale*
absolute number, then writes it as a fraction of the library's per-module
CAS70 default — and the headline run carries that per-module value, charged
once, into a 1 GWe fleet whose realistic O&M staff would be more than 1 person
× 1000 (because shared facilities don't scale linearly with module count).
Rationale should be rewritten in the modular-fleet frame and the value
reconsidered (it may convert to an absolute value once the frame is named).

**37-mtif** — Currently disabled (`blocked_by: 1cFE/fusion-tea#2`), but
P=50 MWe means n_mod=20 at the headline, which makes the Class-S CAS21 bug
maximal. Even though it doesn't affect today's outputs, this file is a
landmine: the day the block lifts and someone flips `enabled: True`, the
silent inconsistency activates. Fixing now is cheap (it's a lambda value with
a comment block; just retire the lambda, rewrite the value with the
modular-fleet rationale, and update the comment).

**08-frc-w-direct-conversion** — different defect: the anchor is the CAS22
*rollup* (Class C blend), but the account being overridden is a sub-account
(Class U). The rationale arithmetic shows what happened — the analyst computed
"override multiplier = $7.5M / $188M ≈ 0.04", deriving the multiplier from the
native-scale rollup magnitude so the at-native dollar number lands at $7.5M.
That math is internally self-consistent at *native*, but at the headline the
rescale ratio of `generic.costs.cas22` (CAS22 rollup, Class C — blend) is
different from the rescale ratio of `cas22_detail["C220103"]` (sub-account,
Class U — ×n_mod), so the override no longer means "$7.5M at native" at
1 GWe. Per the prompt-update spec FR-2, the anchor must be
`generic.cas22_detail["C220103"]` so the value moves coherently with the
account being overridden.

### What the disabled/no-effect entries tell us

Several mismatched anchors are disabled (10-stellarator, 04 CAS70, 37 CAS21) or
attached to accounts that the costingfe library doesn't currently honor as
overridable (CAS70 — 1cFE/1costingfe#106 — applies to 12-dipole's CAS70 and
some others). These don't move the headline today, but each is a future trap:
when the block lifts or the analyst flips `enabled: True`, the silent
inconsistency activates. The cheapest moment to fix is when we're already in
the file rewriting the high-priority overrides.

### Existing tooling — feedback/edit-pass is already built

`exploration/concept_analysis/scripts/run_analysis.py` already implements
`--feedback PATH` for both `analyze` (line 1392) and `model-setup` (line 1415).
Mechanics, from reading the code:

- `--feedback` writes the file as `iter-N/pre_feedback.md` for the next
  iteration (line 354: "feedback is a mid-iteration tool; implies --resume").
- The prompt template incorporates `pre_feedback.md` content into the
  model-setup or analysis prompt (line 463–469: `feedback_text` →
  `extract_findings()` → injected as `model_feedback`).
- This drives an **edit pass**: the agent reads the existing `analysis.md`
  and/or `model_setup.py` and rewrites *only what the feedback asks for*,
  rather than starting from the dossier.
- Recent fix `70b6fbe1` ("edit-pass model-setup no longer discards valid
  work") + `eb3d721f` ("apply Defect A fix to all four remaining runners")
  unbroke this pathway on 2026-06-06; concept 24's iter-1 → iter-2
  convergence was the proof.

So the rerun mode is: not a cold-start re-extraction (which would re-do
dossier ingest, source synthesis, analysis writing, and override authoring
from scratch — ~30+ min/concept and re-introduces randomness in the parts
we don't want to change), but a targeted **model-setup edit-pass** driven by
a small `pre_feedback.md` per concept that points at the specific overrides
to re-author and quotes the policy invariant.

## Code References

- `exploration/concept_analysis/analyses/04-laser-icf/model_setup.py:168-190` —
  CAS21 0.50× with internally-wrong "per-module aggregation" NOTE.
- `exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/model_setup.py:168-180` —
  CAS21 1.25× without a scale frame.
- `exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/model_setup.py:202-216` —
  CAS70 0.75× without a scale frame.
- `exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/model_setup.py:82-89` —
  CAS70 0.70× with native-frame bottom-up.
- `exploration/concept_analysis/analyses/37-magnetized-target-inertial-fusion-mtif/model_setup.py:105-122` —
  CAS21 0.70× lambda; disabled but worth re-authoring.
- `exploration/concept_analysis/analyses/08-frc-w-direct-conversion/model_setup.py:62-85` —
  C220103 and C220109 anchored to `generic.costs.cas22` (rollup) instead of
  `generic.cas22_detail["..."]`.
- `exploration/concept_analysis/scripts/run_analysis.py:324-358, 463-469,
  1252, 1392-1395, 1415` — feedback pathway, validation, and CLI surface.
- `exploration/concept_analysis/scripts/lib/loop.py` (touched by 70b6fbe1) —
  the validators-before-returncode fix that made edit-pass actually converge.

## Feasibility Assessment

**Targeted edit-pass rerun is the right tool for this fix.**

Why edit-pass beats cold-start re-extraction here:

1. The dossier, source synthesis, and analysis.md are already correct — none
   of the policy violations are in the *narrative* or the *quantitative
   findings*, they're in the **override-registry authoring** (rationale frame +
   anchor choice) at the very end of the pipeline.
2. The edit-pass model-setup mode reads the existing `model_setup.py` and the
   `pre_feedback.md`, and rewrites only the specified overrides. This preserves
   the analyst's earlier judgments (Class-U sub-account overrides that are
   fine, absolute values that are fine) while fixing exactly the cells the
   policy flags.
3. The convergence loop is intact (post-`70b6fbe1`/`eb3d721f`): validators →
   verdict → optional next iter. Concept 24 already converged in 2 iters under
   this mode.
4. Cold-start would re-roll dossier-level decisions that aren't broken; it
   would also re-author the *good* Class-U sub-account overrides, introducing
   noise where none is wanted.

Caveats / risks:

- **Edit-pass model-setup is 4–7× slower** than cold-start per `70b6fbe1`'s
  commit message — it cold-boots `uv run python model_setup.py` repeatedly to
  self-verify. Budget ~15–30 min/concept; the timeout floor was raised by the
  same fix so timeouts shouldn't recur.
- **The `pre_feedback.md` has to be specific.** A vague "fix the override
  semantics" will not converge cleanly. The right shape is per-override:
  *"`CAS21 = 0.50 * generic.costs.cas21` — your rationale frames this as a
  per-module account that gets multiplied by `n_mod` downstream. Per
  `.project/reports/2026-06-06-1gw-estimate-policy.md`, CAS21 is Class S —
  charged once at fleet level, not multiplied. The headline value will be
  0.50 × the library's per-module floor (≈$139.9M × 0.50 ≈ $70M), not 0.50 ×
  a conventional 1 GWe building scope. Rewrite either (a) the rationale to
  state the modular-fleet frame explicitly and accept that headline value,
  or (b) the value as an absolute $M that you'd defend as the fleet's once-
  charged building cost."*
- **08's anchor mismatch is mechanically different** — that fix is also a
  *value-derivation* rewrite, not just a rationale rewrite, because the
  multiplier was computed against the rollup magnitude. The feedback for
  08 should ask the agent to recompute the multiplier against
  `generic.cas22_detail["C220103"]` and `generic.cas22_detail["C220109"]`
  and update both anchor and value.

## Recommendations

**Suggested approach — feedback-driven edit-pass, in priority order:**

1. **Author a per-concept `pre_feedback.md`** for the 5 priority concepts
   (04, 08, 17a, 29, 37), each naming the specific override(s) and quoting
   the policy invariant. Templates:
   - For Class-S rationale-frame violations (04 CAS21, 17a CAS21, 17a CAS70,
     29 CAS70, 37 CAS21): "the value is being interpreted as 'M × one
     module's <account>', not 'M × the fleet's <account>'. Rewrite rationale
     in the modular-fleet frame per
     `.project/reports/2026-06-06-1gw-estimate-policy.md`; consider whether
     the value should remain a relative `M × generic.costs.<X>` or convert to
     an absolute $M now that the frame is named."
   - For 04 specifically: include "retract the NOTE about per-module
     aggregation; CAS21 is Class S, charged once."
   - For 08: "C220103 and C220109 are Class U sub-accounts; their relative
     anchor must be `generic.cas22_detail["C2201xx"]`, not
     `generic.costs.cas22` (which is the Class-C rollup). Recompute the
     multiplier against the per-sub-account anchor so the value remains
     coherent under rescaling."
2. **Run each through `model-setup --feedback`** with `--max-passes 3` and
   verify convergence (verdict.json: `pass=True`).
3. **Spot-check headline LCOE** before and after for each — for the Class-S
   CAS21 cases the headline will *not* change much (buildings are a small
   slice; see the original research doc's STEP 3a discussion), but the
   *value* will move (e.g. concept 04 will go from biased-low to its
   intended fraction). The headline LCOE for 29 may move more visibly
   because CAS70 is a larger slice of LCOE.
4. **Open one cleanup PR** that bundles all five edits + their iter-N
   artifacts; one commit per concept for review clarity.

**Out-of-band cleanup** (not needed to ship, but worth doing in the same
sweep since the files are open):

- Re-anchor 10-stellarator's disabled C220103 to `generic.cas22_detail` and
  rewrite the disabled CAS70 rationale in modular-fleet frame (file hygiene).
- Update 12-levitated-dipole's CAS70 anchor (currently
  `0.05 * generic.cas22_detail["C220103"]` — anchor doesn't match account
  class) — file hygiene; behavioral fix waits on 1cFE/1costingfe#106.

**Concepts to leave alone** (verified no relative overrides at risk):
06, 14, 18 (all Class-U sub-account, self-anchored, fine).
22, 23 use only absolute values for their overrides — no policy violation
possible.

## Architecture Insights

- The policy and the corpus diverge mostly in **one place** (the override
  registry rationale + anchor), which is exactly the surface `--feedback`
  was built for. The prompt-update spec
  (`.project/active/prompt-updates-for-1gw-estimate-policy/spec.md`) already
  shipped the prompt changes that teach the *new* model-setup agent the
  invariant — but those prompts only help future cold-starts; the corpus
  fix needs the feedback pathway.
- The edit-pass mode being newly-fixed (June 6) makes this a good time to
  exercise it on the policy-violation cohort: it's a sharp, small, easily
  verifiable rewrite of a single account's rationale (and occasionally its
  anchor), and the feedback signal is unambiguous (policy doc).
- The Class-C "blend" accounts (CAS22 rollup, CAS30/50/60) deserve special
  attention in any future audit — 08's defect is exactly the kind of mistake
  the prompt language has to actively prevent (per the spec's FR-2 "anchor
  matches account class" requirement). Worth confirming the prompt edits on
  branch `feat/1gw-override-semantics-prompts` include language that names
  the rollup-vs-detail distinction explicitly.

## Open Questions

1. **Headline-LCOE sensitivity per concept.** Worth running the spike script
   (`exploration/concept_analysis/scripts/spike_override_semantics.py`) on
   each priority concept *before* the rerun to quantify how much each
   override moves the headline — that tells us whether 29's CAS70 (probably
   the most LCOE-leveraged of the cohort) deserves an *absolute*-value
   rewrite rather than a relative one with corrected framing.
2. **Should 08's value change as well as its anchor?** Re-anchoring without
   rewriting the multiplier means the *native* dollar number will move,
   because the multiplier was derived against the rollup. Depending on how
   the agent re-derives, the headline could move noticeably. This is the
   *correct* behavior, but it's worth being explicit in the feedback that
   the headline is allowed to change.
3. **CAS40 today.** No concept in the corpus currently overrides CAS40, so
   it's not a remediation item — but the policy applies symmetrically when
   it becomes overridable (also blocked by 1cFE/1costingfe#106). Worth
   noting in the prompt-update follow-up so the day-1 surface is correct.
4. **Should the cohort rerun produce a regression artifact** (LCOE before
   vs after by concept) for the project-level report? Useful for the
   broader "what did the policy correction change in the corpus"
   question — separate from the per-concept fix.
