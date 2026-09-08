# Checkpoint C-001.r2 — goal `minor-radius`, round 1 (same fresh reviewer, 2026-09-08)

**Reviewer:** the C-001.r1 session, resumed with the r2 resubmission. Primary checkout at `3f30c418` (the commit carrying the r2 file, the record's second Addendum, the recount script's docstring fix, the r1 checkpoint deposit and the trail's § Checkpoint C-001.r1 entry). Nothing under `knowledge/holdout/` opened. No file edited; no state-changing git; read-only recounts only (`uv run python`). Scratch files under `checkpoint_minor_radius/` only (this file added).

**What I checked:** `evidence/T-003_proposed_dispositions.md` r2 in full; `git diff 851d2738 3f30c418` (five files: the dispositions file 25 lines changed, 13 `[r2]` markers plus the `[r2 — rewritten …]` marker on (c) = 14; the record's Addendum 14 appended, `results/`, `snapshot.json`, `indicators.json` untouched; the recount script's docstring; the trail's r1 entry, which is faithful to my r1 text; the r1 checkpoint deposited verbatim); every number r2 introduces, recounted from `results/points.csv`: `c2821` **255.903** at 100 MW (R 15.7, a 2.2, 13 MA, 13 keV, n 0.8×; A 7.14; wall peak 2.79); `c7779` **244.327** at 220 MW (R 14.2, a 2.9); the R ≥ 14.2 feasible peak-field range **15.27–24.34 T**; `c3711` **24.936 T** here and **24.865 T** under the alternative bore (`a + 1.70`, normalised at 3.00), `wp_stress_ok` satisfied, so kept; the two cheapest machines 7.67 and 6.90 T under the ceiling ("7 T"); the 220 MW cheapest column 214.286 at 2.7 against 218.921 at the edge, feasible through 3.2, refused at 3.3; the 63 t floor is the printed floor of Stellaris § 2.10's 63–200 t cast-part range (WI-035 design D5), so "a printed lower bound" is right; 13 MA on R 12.7 satisfies `peak_field_ok` at every `a` in the window (49 / 50 / 50 / 50 / 50 / 50 per level); the 24 lost points at R 12.7 are **18 at 15 MA and 6 at 14 MA** (the `a` 2.2 cell).

## Verdict: `PASS`

The reading is right and the dispositions now follow from it. The rows may be appended to `DISCOVERY_LOG.md` (the `[r2]` markers stripped on landing, the precedent), and the round result and the fresh review may cite them. Two slips r2 introduced are recorded below as corrections to apply on landing; each is a single phrase, verifiable against the recount, touches no disposition row and no headline number, and does not need an r3 (the pipeline's rule for minor, objectively verifiable fixes: record the verification and continue).

## Per-change confirmation (my r1's required changes 1–9)

1. **Applied.** § 1 item 1: "27 on the R 11.2 row (every committed-feasible point there) and 24 at R 12.7 at `a` ≥ 1.7"; the 30 / 21 gone.
2. **Applied.** § 1 item 4: "50 of the 51 lost feasible points stand under either bore and one — `c3711` (R 11.2, a 1.3, 13 MA, 220 MW; 24.936 T here, 24.865 T under the alternative) — does not", citing Addendum item 14; the record carries item 14 in a second Addendum, evidence untouched. One slip inside item 14 — see correction B.
3. **Applied.** (c) gives both levels: 202 at 100 MW; at 220 MW "the same column's cheapest point is also at 2.7 m, 214 $/MWh, against 219 at the window's edge — by nothing in the model before the sustainment closure stops answering at 3.3 m"; the one-sentence summary states the level and the seam at 220 MW.
4. **Applied.** (c) carries the four held values (τ*/τ_E 8, helium suppression 0.5, ι 0.92; calibration 1.316441), the 1.83× band, "neither headline machine survives", and the cheapest survivors 256 (R 15.7, a 2.2, A 7.1) and 244 (R 14.2, a 2.9) — both recounted.
5. **Applied.** "at its design current every fatter plasma, the coil bore rebuilt outward from it as this model does, exceeds that ceiling"; "the model does not carry the paper's coil set as a fixed object"; "at lower currents (13 MA) the same column clears the ceiling at every minor radius in the window" — recounted true.
6. **Applied.** "its price moved by three hundredths … its computed casing mass, 61 t, sits under the 63 t the old model held — the model's casing anchor is a printed lower bound, so a lighter casing is the anchor's seam scaling below its floor, not a saving". "Printed" verified against WI-035 D5.
7. **Applied.** `20260904-wall-and-heating#3`, `20260905-stored-energy-basis#2`: "discharged in part … the *price* half is landed"; what stands named with homes — the sourced bound (`f_geo`) at `goal.md` § Limits (1), the re-anchoring rule at § Limits (2) and the epic's § Item WI-044 note; the `closed [OWNER]` row to carry both by reference. `20260907-burn-control#3`: "discharged in part, scoped … the sourced bound (`f_geo`) stands unbuilt". Right.
8. **Applied.** A `#8` row: `declared seam — standing, newly witnessed on a second column`, the four transect exclusions and the edges' error rows cited, the 220 MW `a`-edge resting on it; the pair out of "not touched".
9. **Applied.** `#2` / `stored-energy-basis#8`: "a bounded negative, the close owner-held", the owner's carry `[OWNER 2026-09-06]` named in the sighting column, the reading marked `[AGENT]` (ratified with option 2), the reopening condition stated. Responsible "the owner (close or carry)". Right.

Optional F10 (the 15.3–24.3 T range; "7 T under" attributed to the two cheapest machines) and F12 (the Addendum commits cited in § 4; the docstring now "69 new points") applied. F11: (iv) applied as "at 15 MA and above" — see correction A; (i), (ii), (iii) not applied — they were not conditions and are not now (the (c) is owner-held proposed text; the owner reads it at the round boundary).

## Corrections to apply on landing (verifiable; not an r3)

**A. (c), the current descriptor.** "the fat R 12.7 m plasmas at 15 MA and above — 51 points": the 24 lost points at R 12.7 are 18 at 15 MA and 6 at 14 MA (the `a` 2.2 cell); none at 16 or 18 MA (already violated committed). Write "at 14 and 15 MA". The 51 is right.

**B. The record's Addendum item 14, `c3711`'s coordinates.** It says "(R 11.2, a 1.3, 13 MA, **13 keV, n 0.6×**, 220 MW)"; the row reads **17 keV, n 0.8×** (4.048e20 / 5.06e20). R, a, I, the level and both fields are right, and the dispositions file's item 4 does not state T or n, so nothing in the rows or the reading is wrong; the record's Addendum is, and Addenda are not edited — one further Addendum line (item 15) records it. The reviewer's r1 text also named only R, a, I and the level.

Not a correction: the (c)'s "the conductor ceiling and the stress check … (…) — 51 points" still reads as if the stress check took some of the 51 (all 51 are through the ceiling; the 369 stress flips land on points already infeasible), and "keeps getting cheaper to a minor radius of 2.7 m" is not monotone (200.07 / 200.26 / 198.94 at 2.5 / 2.6 / 2.7). Both were optional in r1 and stay so; noted for the owner's reading of (c).

## Per-row rulings

- `20260904-wall-and-heating#3`, `20260905-stored-energy-basis#2` — `PASS` (discharged in part at the pin, the price; the bound and the re-anchoring standing at named homes; close owner-held).
- `20260907-burn-control#3` — `PASS` (discharged in part, scoped; the bound standing).
- `20260904-wall-and-heating#2`, `20260905-stored-energy-basis#8` — `PASS` (bounded negative on the admissible corpus, `[AGENT]`; close owner-held).
- `20260904-wall-and-heating#8` — `PASS` (seam standing, newly witnessed; the 220 MW edge on it).
- Not touched, sound: `20260904-wall-and-heating#4`, `20260905-stored-energy-basis#1`, `#3`, `20260907-burn-control#1`, `#2`, `#4`, `#5`.
- This record's `#1`–`#6`: no correction row owed (no sighting row repeats an Addendum item, 14 included).

ADR-0004 checklist: every row names a class from the set, a status, a responsible party and a concrete next reference; no touched row is `unrouted`; rows that change nothing say so; no sighting row is edited; no id is minted. Reserved gates: nothing tuned, nothing minted, one pin, no bound on `a` claimed, no rubric re-grade; the (c) restatement is proposed text for the owner, now carrying the casing seam as a seam.

**Revision spent:** 1 of 2 (r1 → r2); the cap was not reached.

**Confidence:** high on every recount (each new number derived independently and matched); high on the nine confirmations and on corrections A and B (both read directly off `results/points.csv`).
