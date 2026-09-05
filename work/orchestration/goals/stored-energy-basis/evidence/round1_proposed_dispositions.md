# Round 1 — proposed dispositions on the discovery rows the grounding evidence touched

Goal `stored-energy-basis`, round 1 (`write-up-from-grounding`). Written 2026-09-05 by the round agent for the pre-execution disposition checkpoint (`GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint). The reading under review is `w_counterfactual/NOTES.md` §§ 3–8 (grounding evidence, oracle-side, at `3687d2f6`); the rows are the five `20260904-wall-and-heating` findings that reading touches. Nothing is landed until the checkpoint passes. No id is minted; every row joins an id the record's § 15 already carries.

**What the reading is, in one paragraph.** Every executed point of `20260904-wall-and-heating` (6,311; record dir at `a5b0b96a`, rows at `8906d4e7`) was re-evaluated through the oracle with the model's stored thermal energy scaled by one constant (0.9151) to the paper's printed 504.65 MJ, the closure left live, and every verdict compared with the record's column by case id. The scale is multiplicative and geometry-independent: the sign of each move is robust, the location of any boundary is not a claim (§ 6). Nothing under `models/`, the generated package, or the study store was written; the pin `c1b0f0d1…` stands. Sixty committed points re-evaluated unmodified reproduce the record exactly. And the target itself is in question: no reading of the paper's plotted profiles with its printed peaks reaches 504.65 MJ (527–575 across readings; the printed β implies 567 at the axis field), so the counterfactual is a sensitivity, not a correction (§ 7). REQ-W-01 (the paper's own definitions) is the open research act on the target; its return is recorded in the trail § T-001 return.

**Row conventions.** Kind `model`. Disposition class from the ADR-0004 set (`model fix | research | declared seam | upstream filing`), status, responsible actor, and the concrete next reference. A row that changes nothing says so.

## `20260904-wall-and-heating#1` — the (b)(ii) answer, a conditional positive

Current state (newest row, `8906d4e7`): `model fix` — the (b)(ii) answer carried to the round-2 result for the owner's close ruling, conditional on `#2`, `#3`, `#4` and the WI-041 constancy assumption; the round-2 fresh review (2026-09-05, `wall-and-heating/evidence/round2_review.md`, untracked) reads the four conditions as disclosed facts the contract accepts and recommends close.

Proposed row:

> `declared seam` — **a fifth disclosed condition, W-sensitivity**, added beside the four: with the model's stored energy scaled to the printed 504.65 MJ (a 9 % change), the design geometry opens at 100 MW — six feasible driven points at R 12.7, a 1.3 (cheapest `c0625` 315.09; the pinned baseline `c2973` itself 332.585 at 37.5 MW required) where the record has none — while the cheapest driven point barely moves and is a different point (212.460 at `c1721` → 212.314 at `c1676`) and 347 of the record's 657 driven points stop being driven (305 ignite, 40 fail `recirc_ok`, 2 fail `sustainment_ok`). The region's existence at the printed level is robust to W; "never at the design's minor radius" is not. The condition is a seam, not a fix: the stored-energy basis the model carries is the owner's ruling (`stored-energy-basis/goal.md` § Answered when (c)), W is never tuned, and the printed value is not shown to be the right target (§ 7). Responsible: the owner, at the `wall-and-heating` close (the (b) ruling) and at this goal's (c) ruling; the `wall-and-heating` round agent when L-009 lands (its Scope line). | `stored-energy-basis/evidence/w_counterfactual/NOTES.md` §§ 5, 8 at `3687d2f6`; `stored-energy-basis/trail.md` § Round 1 result

## `20260904-wall-and-heating#2` — the ash knife-edge

Current state: `research` — open; the aspect-ratio scaling of τ*/τ_E, helium suppression and the ISS04 iota is the sourced input any `a`-claim needs; responsible: the owner at the round-2 close (mint or carry).

Proposed row:

> `research` — open, unchanged in class and routing; **the knife-edge's location is W-sensitive**: on the design column τ*/τ_E = 6 goes from driven at +44.4 MW required (wall 4.54, violated) to ignited at −12.2 MW (wall 4.33, still violated); at 12, 158.4 → 109.0 MW; nothing on the transect is feasible in either state, so the shape stands and the flip points move with W. Any research return on the transport facts is read at a stated W basis. Responsible: unchanged (the owner at the `wall-and-heating` close; the next strategy author executing). | unchanged, plus `NOTES.md` § 5 at `3687d2f6`

## `20260904-wall-and-heating#4` — the one-sided sustainment fence

Current state: `model fix` — open; a second inequality `p_aux_required ≥ 0` or a burn-control lever, not minted; every feasibility claim in the record is on `feasible_driven`; responsible: the owner at the round-2 close.

Proposed row:

> `model fix` — open, unchanged in class and routing; **the ignited set is the most W-sensitive set in the study**: 787 → 1,282 ignited per level under the forced W, and 305 of the record's driven points cross into ignition, so the one-sided fence's pass-through grows with any W decrease and the `feasible_driven` reading on which every record claim rests is the reading W moves most. A second inequality, if minted, is evaluated at a stated W basis and its verdict counts reported beside the sustainment counts. Responsible: unchanged. | unchanged, plus `NOTES.md` § 5 at `3687d2f6`

## `20260904-wall-and-heating#6` — round 1's 220 MW result re-executed

Current state: `model fix` — discharged by WI-041 (the sighting row carries the routing; the round-2 review's F4 asks for a joined row from that goal's agent).

Proposed row:

> `model fix` — **discharged, unchanged**; re-sighted under the forced W: the re-read arm goes 24 → 58 driven (all at the design geometry), cheapest 371.70 against the record's 378.556, and 25 of its 152 flipped wall verdicts flip back through `p_fus`. The discharge stands (the fence's form and WI-041's arithmetic are untouched; the peak moves through fusion power, not through the fence); the survivor count is W-conditional. Responsible: none owed beyond this row. | unchanged, plus `NOTES.md` § 5 at `3687d2f6`

## `20260904-wall-and-heating#7` — `R`'s effect on wall load

Current state: `model fix — none owed`, discharged as a measurement, to L-010.

Proposed row:

> `model fix — none owed` — **unchanged**: the field chain does not read W, and the wall peak still rises with `R` under the forced W; the exponent was not re-measured and is not claimed here. Row written so the touched set is complete. | unchanged

## Rows not touched

`#3` (`a` unbounded and unpriced), `#5` (the lifetime chain's price), `#8` (the closure's validity edge): the reading reaches `#8`'s edge — 61 points fail it under the forced W, none feasible in the record — but the edge is the record's own declared seam and this reading adds no disposition to it; noted in the trail, no row.
