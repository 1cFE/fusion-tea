# Round 3 review: goal `design-study-parameters` (fresh, bounded)

Fresh reviewer, no prior context; only the brief's entry files read; nothing run. 2026-09-26.

**Verdict: FINDINGS** (one `correct-before-close`, the rest `note`). The direction is applied in substance, the numbers match the sealed record, the seal is sound, the scopes held. One figure in the answer is not supported by the stored channels.

## Q1 Direction applied: yes

(1) Answer § 5 states the arrangement: an explicit bypass control (B) modeled, consistent settings (A) executed as its zero-bypass family. The owner said "choose"; the round evaluated both and shows the same best point under either. Applied in substance; the acceptable bypass fraction (check vacuous at 1.0) is correctly the owner's and does not block the answer.

(2) Enforced: the check holds at the root-solve closure, 1e-6 K, against residuals of order 1e-11 K; infeasible cases carry the physical deficit (+0.33 to +2.08 K) and fail. That tolerance would not admit round 2's 0.70 K or 49 K.

(3) The start, five round-1 leading points, S6, the I-A start, ladders at 2,500 and 2,250 kg/s, and the matched point at seven flows were executed and verified.

(4) The comparison is on 11-of-11 cases, against the start (B, 31 % bypass) and against the matched 2,500 point.

"Exactly consistent" now rests on seven executed, verified boundary points. "Without reordering" is gone; the ranking changed (round 1's band superseded).

## Q2 Numbers: match

About forty values in § 2 and § 6 checked against readout § 1–2 (all eleven rows' net, deltas, unmet, bypass, nonfuel, Δnonfuel, tritium, total; the seven boundary ratios and nets; the 85.6 MW span; the 0.0023 ratio gap; nonfuel = total − tritium − 0.02..0.03 consistently). All match at the stated rounding, except:

- `correct-before-close` "Round 1's best band ... 20–23 MW below the matched point" (answer § 2, L-012, trail T-011 return, record #2). The stored deltas against the design-flow matched point are −23.3 and −26.3, as the answer's own table shows. Write 23–26 MW (or 2.7 and 23.4 MW against each flow's own matched point). Correct the answer and L-012; carry it in the joined disposition for #2 rather than editing the seal.
- `note` +46 % (answer § 2) versus +45 % (passage, trail, record #2): it is 45.5 %. Use one form.
- `note` "3.18 → 4.62 TWh" implies a capacity factor (0.85) the answer does not state and the readout does not carry.

## Q3 Bypass fractions and residuals: match

0.3112, 0.1296, 0.0194, 0.0388; feasible residuals −6.2e-11..+5.2e-11 K. The supersession of 18.8 % and 6.0 % is stated with the records' reason (the mixing estimate assumed the outlet unchanged), matching record #4.

## Q4 Seal and identity: sound

§ 13: pass on all 22 cases, 255 channels, the manifest's twelve classes, eleven verdicts re-derived. § 16: sha256 `f0f72112…`, matching answer § 8. `snapshot.json` exists, `study_id` correct. § 12 licenses round-1 cycle values by the bit-identical replay of the eight WI-094 receipts; the re-executed round-1 points in readout § 1 match the ledger's round-1 values to three decimals.

- `note` "declared before execution" is shown by the trail (T-010 before T-011), not by § 13's text.

## Q5 Scope and learnings

Scopes held: one new library file, no shared library file edited, receipts and round-1 record stated untouched, no package or model change in T-011/T-012. L-011, L-012 (after the fix), L-013, L-015 follow from the records.

- `note` T-010's decision cites `studies/prepare_interface.py`, absent from its scope; T-011/T-012 added `fill-record-b.py`, `fill-answer-r3.py` under `evidence/` unnamed in scope. Harmless; list them. T-012 lacks a return block.
- `note` L-014 is graded [OWNER] but generalizes an instance-specific direction into a rule; the generalization is agent-authored. Grade it [AGENT] from the [OWNER] direction, or keep the owner's words.
- `note` L-011 cites `readout.md` for 3,836.5 / 3,301.2 MW; those live in `results/readout.json` and the record.
- `note` Ledger row `ia-f2500-r1.5183` prints "capacity_ok violated" three times; name the three ratings.

## Missing evidence / uncertainty

- 472 K / 423 K heater inlets (answer § 3) and the capacity factor are not in readout § 1–2; unverified.
- The 3,836.5 / 3,301.2 pair was located by filename, not read.
- "Untouched" receipts and record, and `prepare_interface.py`'s edit status, are the trail's assertions; no git check run.
- Physics beyond the records' statements not evaluated, per the brief.
