# Proposed goal-level dispositions — round 1, after the `20260903-wall-and-heating` reading

Author: the resuming round-1 session of goal `wall-and-heating`, 2026-09-04 (the session that executed the 639 points wrote the study definition and the first results; this session completed runbook steps 5, 6 and 10–15, committed the record at `2d11ca1b`, and proposes these). Status: **PROPOSED** — nothing below executes until a fresh checkpoint reviewer passes it (`GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint). What the checkpoint gates: the disposition rows these proposals become, the T-004 return and the round-1 result that cite them, and — downstream — the evidence base the fresh round reviewer will write round 2's strategy on. One task remains inside round 1 after this checkpoint, the fresh Row-4 re-grade (T-005); it grades the model increment and does not rest on this reading.

The reading of record is the fresh administrator's `exploration/stellarator_e2e/studies/20260903-wall-and-heating/synthesis.md` (spawn prompt `evidence/T-004_administrator_prompt.md`) together with the committed record's § 15 (`record.md@2d11ca1b`). The administrator's independent recount (`synthesis.md` § 3) agrees with every § 3 headline, every § 4 count, every § 15 finding, the baseline row, both transects, the optimum and the shadow survivors; it found five prose slips in § 4/§ 6/§ 11 (a 14.75 MA LCOE value, a wall-blocked column count, the scan's `wp_stress` count, and two labels), each re-derived by the executor and corrected in the record's Addendum of 2026-09-04 — no finding, count or disposition below rests on any of them. The administrator's reading of the study question is `synthesis.md` § 7, its constraint structure § 5, its per-axis framing verdicts § 4, and its list of what the record does not carry § 8 (the pre-change oracle run behind the "not new" claim, the 36-point predecessor identity, the shadow bounds' provenance, and the critique's probe numbers are all outside the record directory by the administer contract; each is cited here from its own home). This document does not restate either; it cites.

## Rows the round's evidence touched

Fourteen rows: the seven this study sighted, and seven predecessor rows the round's evidence bears on — three named in `goal.md` § Consumer as owed a disposition by any round whose evidence touches them (`20260903-priced-levers#1`, `#5`, `20260901-sustainment-fence#4`), and four the study's own results re-sighted (`20260903-priced-levers#3`, `#4`, `20260901-sustainment-fence#1`, `#3`).

### 1. `20260903-wall-and-heating#1` — at the printed heating level nothing is feasible, and the negative is absolute in source efficiency

- **Reading relied on:** record § 4 (`arm-fence-p100`: 0 of 240; sustainment alone 36, wall alone 10, ceiling alone 9), § 6 `eta_source_heat` (the 36 sustainment-alone points need at least 87.061 MW coupled — `c0036`, I 15.4 MA, T 17 keV, n 0.9× — so 100 MW wall-plug opens only at `eta_source_heat` ≥ 0.871 at `eta_couple` 1.00; crossings 0.871–1.629 across the 36; the scan's 0.92 was its coarser grid), § 15 #1, § 17 (no buildability claim; no geometry claim).
- **What "absolute" means, stated so the reviewer can rule on it:** a claim about the executed (I, T, n) window — I 14–17 MA, T 14.63–22 keV, n 0.9–1.2× — and, at coarser resolution, about the scan's 3080 candidates at 100 MW (0 feasible over efficiencies 0.40–0.60). Not a claim about the machine outside those windows, and not a claim about any geometry other than R 12.7 m, a 1.3 m. Within the windows it is absolute in efficiency because efficiency reaches no fence but sustainment (§ 8): the 204 points blocked by the wall or the ceiling cannot be opened by any source.
- **Class:** `model fix`.
- **Status:** **routed → round 2 of this goal, not minted.** The heating half of this finding is answered — heating-source efficiency is not the escape at the printed level, at any efficiency, in this window. The wall half is not: 174 of the 240 points fail a wall fence that compares a flat-wall average to a printed peak limit (§ 4), and whether they are really blocked is exactly what the honest fence decides. The owner has settled round 2's subject as the wall-load fence `[OWNER 2026-09-04, verbatim in trail § Round 1 result]`; its shape is the fresh reviewer's to write. Minting is that strategy's act (one-pin/one-study bound).
- **Responsible:** the fresh round-1 reviewer (round 2's strategy revision), then round 2's agent.
- **Concrete next reference:** `evidence/T-001_research_return.md` § 5 (the three-part decision: the fence's form, its area basis, the 0.10 m standoff transfer); record § 15 #3 and the shadow columns; `goal.md` § Answered when (b).
- **What changed by this disposition:** the heating escape at the printed level is closed by measurement in this window; the wall escape is carried to round 2 with its correction bounds as data.

### 2. `20260903-wall-and-heating#2` — whether source efficiency pays depends entirely on which quantity is held

- **Reading relied on:** record § 3, § 6 `eta_source_heat` (fixed 220 MW wall-plug: LCOE 269.823 → 273.675 over 0.35 → 0.65, heating capital 406.8 → 755.5 M$, wall-plug draw constant, crossing at 0.5238; fixed 132 MW coupled: 317.234 → 255.970 over 0.35 → 0.75, heating capital constant at 697.3 M$, `rec_frac` 0.4499 → 0.3096; `p_fus`, wall load, beta, `p_aux_required` bit-identical across efficiency in all 96 cells), § 8 (the one new reach: efficiency → `sustainment_ok`), § 12, § 14 Honesty (the three cut-back claims), § 15 #2, § 17 (no matched pre-change comparison).
- **Class:** `model fix` — the nearest of the four ADR-0004 classes for a finding that is an *answer* rather than a defect, on the `priced-levers` C-001.r1 precedent for information-only findings; **the reviewer may re-class it.**
- **Status:** **answered at the model level by WI-039; no model change routed; carried.** Two homes: the Row-4 re-grade evidence map (`.project/active/demo-depth-rubric/evidence-map-r4-regrade.md` § Load-bearing study evidence — the chain re-deriving at scale is study evidence for the P2 anchor's "verified"), and the round-1 result. The one open model gap the finding names — `eta_couple_heat` held at the optimistic 1.00 with no admissible source for a coupling loss — stays where WI-039 put it, as a stated assumption in the model text (`stellarator_plant.sysml:670-698`); a sourced coupling figure would be a research-seam question, and this round opens no request for it.
- **Responsible:** the T-005 grader (the anchor's "verified" is theirs to judge); the round-1 result (the goal-level reading).
- **Concrete next reference:** record § 6 `eta_source_heat`; `results/points.csv` arms `arm-transect-eta` and `arm-couple-132`; `evidence-map-r4-regrade.md`.
- **What changed:** the heating half's measured answer exists and its newness claim is the cut-back one (the fixed-wall-plug experiment is new; the constant-coupled sign is not).

### 3. `20260903-wall-and-heating#3` — every economic result at 220 MW is set by the wall fence as bound

- **Reading relied on:** record § 3, § 4 (`wall_load_ok` 144 of 384 at 220 MW; alone 77), § 6 `I_coil`, `T_i0`, `n_e0` (LCOE falls with density and temperature until the wall stops it), § 15 #3 (the optimum at 98.9% of the limit; 4.604 under the low bound; 51 of 91 survive the low bound, 0 the high; cheapest survivor 326.201), § 17 (no claim about the honest fence); `evidence/T-001_research_return.md` §§ 3–5 (the bounds' derivation: peaking 1.5–2.1 over a shaped-wall average, shape factor 1.146–1.303 on the wall-side radius, so the net multiplier on a circular-torus average is peaking ÷ shape, 1.15 at the low end and 1.83 at the high; the standoff gap 0.10 m vs 0.30 m).
- **Class:** `model fix`.
- **Status:** **routed → round 2 of this goal, not minted** — the same route as row 1, and the reason the two halves of this goal are one goal. The shadow columns are data, not a decision: they say what round 1's result becomes under each end of the sourced correction, so that round 2's fence change cannot invalidate round 1's reading unnoticed.
- **Responsible:** the fresh round-1 reviewer (strategy), round 2's agent (the fence's form, area basis and standoff transfer, with any baseline verdict change disclosed and never tuned away — `goal.md` § Invariants).
- **Concrete next reference:** `results/points.csv` columns `wall_load_shadow_lo/hi`, `wall_load_ok_shadow_lo/hi`, `feasible_shadow_lo`; T-001 § 4 (the wall-side-radius convention the correction must use) and § 5; `goal.md` § Answered when (b)(i).
- **What changed:** round 2's impact on round 1's result is pre-registered as data: under the low bound the round-1 optimum moves from 267.159 to 326.201 and from (I 14.25, T 16, n 1.0) to (I 14.25, T 14.63, n 1.0); under the high bound nothing at 220 MW survives.

### 4. `20260903-wall-and-heating#4` — the four `heat__*` chain channels came back blank (process)

- **Reading relied on:** record § 13, § 15 #4; the class already declared at `ANNEX.md` § Oracle and in `20260821-power-cycle-ab#5`, `20260901-sustainment-fence#3`, `20260903-priced-levers#4`.
- **Class:** `declared seam`.
- **Status:** **closed for this goal.** The four channels were removed from the store declaration, exported oracle-side in `results/oracle_operands.csv`, and the study re-executed; `ANNEX.md` § Oracle now names `heat__*` (committed with the record at `2d11ca1b`). What this sighting adds: the silent-blank-column failure mode has now recurred three times (`20260901-sustainment-fence#3`, `20260903-priced-levers#4`, this) after the ANNEX prose documented it — the recorded repeats ADR-0003 asks for before a mechanism is promoted. The hardening candidate proposed at `20260903-priced-levers#4` (a declaration-time guard in `scripts/study/` refusing a declared store channel that does not resolve to a single-field float) now has three recorded repeats behind it; **recommended for minting owner-present as a coding-PM item under the run-study epic; not minted by this round.**
- **Responsible:** the run-study tooling owner; the owner at the next selection act.
- **Concrete next reference:** `ANNEX.md` § Oracle; the `20260903-priced-levers#4` disposition row.
- **What changed:** the ANNEX names the module; the hardening candidate's evidence grew from two repeats to three.

### 5. `20260903-wall-and-heating#5` — two arms silently shared a point (process)

- **Reading relied on:** record § 11, § 15 #5; `study.py` `proposals()` (raises on a shared point).
- **Class:** `declared seam`.
- **Status:** **closed in this study; practice recorded.** The definition now fails loudly; the couple arm cites `c0550` for its 0.60 point. The transferable practice — a study definition asserts no two arms share a point, and arm membership is checked by counting rows per arm after execution — is a study-definition convention, on the `20260823-magnet-technology-ab#6` precedent (home: the study definition file beside each record).
- **Responsible:** the next study's executor; the `run-study` skill's maintainer if the runbook's step 9 is to carry the assertion (not edited by this round).
- **Concrete next reference:** `study.py` `proposals()`; runbook step 9.
- **What changed:** one lost case recovered by re-execution; a loud failure where a silent one was.

### 6. `20260903-wall-and-heating#6` — the constant-coupled arm's first anchor sat below its own fence (process)

- **Reading relied on:** record § 11, § 15 #6; `study.py` (the `COUPLE_TARGET` note).
- **Class:** `declared seam`.
- **Status:** **closed in this study; practice recorded** — a transect's held level is read off its anchor's own operands (`results/oracle_operands.csv` `p_coupled_installed_MW`), never assumed from the arm's name. Home: runbook step 7 as executor practice, on the `20260829-p-pump-fence#2` precedent.
- **Responsible:** the next study's executor; the `run-study` skill's maintainer.
- **Concrete next reference:** `study.py` § the `COUPLE_TARGET` comment; runbook step 7.
- **What changed:** the arm measured economics instead of re-measuring the fence.

### 7. `20260903-wall-and-heating#7` — `j_wp` is inert in this window (re-sighting of `20260903-priced-levers#2`)

- **Reading relied on:** record § 8 (the critique's probe: 95–145 A/mm², LCOE 0.08 $/MWh, B_peak / `p_aux_required` / wall load unmoved), § 15 #7; `evidence/T-004_precritique.md` F7.
- **Class:** `model fix`.
- **Status:** **standing at WI-040** (minted 2026-09-03 `[OWNER]`, `work/BACKLOG.md`, sequenced before WI-038); no new work routed. The reviewer may rule that this should have been folded into `20260903-priced-levers#2` rather than minted as its own id; it was minted because the study's § 15 registers every finding its reviews produced (runbook step 14) and this one was produced by the critique on this pin.
- **Responsible:** WI-040's owner at its own start.
- **Concrete next reference:** `work/backlog/epic-mfe-cost-modeling.md` § Item WI-040; `20260903-priced-levers#2`'s mint row.
- **What changed:** nothing; the row is accounted for.

### 8. `20260903-priced-levers#1` — the deadlock at the printed power is sustainment against neutron wall load (sighting; routed → this goal at grounding)

- **Reading relied on:** `evidence/T-001_research_return.md` §§ 3–5 and § 8 (the finding that outranks both candidate forms: every published average is over a shaped 3D wall; the model's circular-torus area is 15–30% too small on the same wall-side radius; the honest fence probably tightens); record § 4 and § 12 (at the WI-039 pin and this study's own 100 MW grid: sustainment alone 36, wall alone 10, ceiling alone 9 of 240 — a different grid from the predecessor's, so not comparable as counts; the 36 shared points identical to every digit); record § 15 #1, #3.
- **Class:** `model fix`.
- **Status:** **routed → round 2 of this goal, not minted; the defect is now sharper than the row's sighting states.** The sighting named an average-vs-peak mismatch; T-001 found the area basis underneath it, and the study pre-registered the correction's effect on the current optimum as data. Round 2 decides the fence's form, its area basis and the standoff transfer, on T-001's three registered sources.
- **Responsible:** the fresh round-1 reviewer (strategy), round 2's agent.
- **Concrete next reference:** `evidence/T-001_research_return.md` § 5 and § 8; record § 15 #3; `goal.md` § Answered when (b).
- **What changed:** the model's flat-wall area is identified as the thing that has to be corrected for either honest form; the likely direction (tightening) and its size (net 1.15–1.83× on the operand) are recorded as data, never tuned away.

### 9. `20260903-priced-levers#4` — a declared store channel came back empty (process; disposed `declared seam` with a hardening candidate)

- **Reading relied on:** as row 4.
- **Class:** `declared seam`.
- **Status:** **unchanged in class; the hardening candidate gains its third recorded repeat.** Nothing this round does changes the row's disposition; it is dispositioned because the study's evidence touched it. The recommendation to mint the declaration-time guard owner-present is restated in row 4, not here.
- **Responsible:** the run-study tooling owner; the owner at selection.
- **Concrete next reference:** `20260903-wall-and-heating#4`.
- **What changed:** nothing in the row's own state; one more sighting joins it.

### 10. `20260903-priced-levers#5` — the temperature axis is worth 16.645 $/MWh and the predecessor's optimum sat on its window edge (disposed `declared seam`; a standing study-design constraint)

- **Reading relied on:** record § 5, § 6 `T_i0` (T swept to 22 keV at 100 MW and 18 keV at 220, the scan to 24 keV; the 220 MW optimum at 16 keV, interior; nothing feasible above 18 keV at either level), § 11.
- **Class:** `declared seam` (as its last row).
- **Status:** **applied, and the failure did not recur; no change to the row.** The constraint the row routed into `goal.md` § Invariants (T is a search axis with a window wide enough that the optimum is interior or a fence catches it) governed this study's windows, and the executed optimum is interior in T. Dispositioned because the study's evidence touched the row; it moves nothing.
- **Responsible:** the next fence study's executor (unchanged).
- **Concrete next reference:** record § 6 `T_i0`.
- **What changed:** nothing; one confirming application.

### 11. `20260901-sustainment-fence#4` — installed heating is pure cost once sustainment is met; a heating-system model would change the trade (sighting; minted → WI-039; the heating half of this goal)

- **Reading relied on:** trail § T-002 return (WI-039 landed: the chain as seven named quantities, the baseline unchanged in every number, the perturbation test, SV-048/049 passing); trail § T-003 return (pin `2649e0ea…`, `CANDIDATE`); record § 6 `eta_source_heat`, § 8, § 15 #2.
- **Class:** `model fix`.
- **Status:** **discharged at the model level by WI-039 at pin `2649e0ea…`; the grade is pending (T-005) and the work-item close is owner-held.** The sighting's premise — "a heating-system model would change the trade" — is now measured rather than expected: it changes the trade in the parameterization that holds coupled power (efficiency is worth 61.264 $/MWh over 0.35–0.75 at fixed 132 MW coupled) and not at fixed installed hardware (LCOE rises with efficiency at fixed 220 MW wall-plug), and at the printed level it changes nothing (0 of 240 at any efficiency). Heating is still "pure cost" in the row's sense at fixed wall-plug; what WI-039 added is the second parameterization and the efficiency's reach to the sustainment fence.
- **Responsible:** the T-005 grader (§ Answered when (a)); the owner (WI-039 close).
- **Concrete next reference:** `evidence-map-r4-regrade.md`; record § 15 #2; `work/active/WI-039_heating-system-structure/plan.md` § Phase 4.
- **What changed:** the model object the row asked for exists and executes; its measured consequence is row 2.

### 12. `20260901-sustainment-fence#3` — multi-field-module channels do not reach the evidence store (process; `declared seam`)

- **Reading relied on:** as row 4.
- **Class:** `declared seam`.
- **Status:** **unchanged; the class gains a fourth member and the ANNEX sentence now names it** (`heat__*` beside `pb__*` and `sustain__*`).
- **Responsible:** unchanged (the evidence layer in sysml-codegen / teax, outside this repository).
- **Concrete next reference:** `ANNEX.md` § Oracle.
- **What changed:** the ANNEX sentence.

### 13. `20260903-priced-levers#3` — `cond_strain_ok` is inert at the 0.4% limit (disposed `research`; Pierro 2019 queued)

- **Reading relied on:** record § 4 (violated 0 of 639; max strain 0.251% at this study's windows).
- **Class:** `research` (as its last row).
- **Status:** **unchanged; re-confirmed at the WI-039 pin.** The Pierro et al. 2019 operator fetch remains queued and owner-held (REQ-036-03 `queued[]`); no `eps_cond_allow` arm was run here (the study is heating-shaped and declined every magnet-fact axis). Dispositioned because the evidence touched the row; it moves nothing.
- **Responsible:** the operator (the fetch); the next fence study's executor.
- **Concrete next reference:** unchanged.
- **What changed:** nothing.

### 14. `20260901-sustainment-fence#1` — the 50 MW deadlock (sighting; WI-038 minted; the 262 conductor candidate; sequenced after the wall half and WI-040)

- **Reading relied on:** record § 4 (at 100 MW: ceiling alone 9, wall alone 10, sustainment alone 36 of 240; `peak_field_ok` violated 96 of 240 at I ≥ 16 MA), `results/points.csv` (`c0149`: eta 0.50, I 17 MA, T 17 keV, n 1.0×, `j_wp` 118.827 — ceiling-alone at **262.10 $/MWh**, B_peak 27.487 T against 24.9, wall load 3.886, required heating 22.44 MW against 50 coupled: the `priced-levers` review's F1 candidate re-appears at this pin to the cent; and under T-001's low correction bound its wall load reads 4.469 against 4.05 — **violated**), record § 12 (the 36 shared points identical).
- **Class:** `model fix`.
- **Status:** **unchanged — WI-038 stays minted, unstarted, sequenced after this goal's wall half and after WI-040 `[OWNER 2026-09-03]`; the owner's sequencing is now supported by measurement.** The conductor candidate is still there and still cheap at the fence as bound, and it fails the wall under even the mildest sourced correction. Whether the conductor escape survives an honest wall fence is decided by round 2, which is why WI-038 waits. Dispositioned because the study's evidence touched the row; the row's own state does not change.
- **Responsible:** the owner (sequencing, unchanged); round 2's agent (the honest fence decides whether the candidate survives).
- **Concrete next reference:** `c0149` in `results/points.csv` with its `wall_load_shadow_lo`; `work/backlog/epic-mfe-cost-modeling.md` § Item WI-038.
- **What changed:** nothing in the row's state; the candidate is re-measured at the new pin with its wall-correction exposure stated.

## What no row does

No row edits a first-sighting row. No row mints a work item — the round is at its one-pin/one-study bound and minting is the next strategy's selection act, or the owner's. No row changes anything under `models/`. No touched row returns as `unrouted` — every row above carries a class, a status, a responsible actor and a concrete next reference, which is the ADR-0004 test (`priced-levers` C-001.r1 ruling on (c)).

## Revision r2 — 2026-09-04, after checkpoint C-001.r1 (`REVISE`)

The r1 text above stands as submitted; this section supersedes the named passages. The reviewer's recounts agreed with every number (trail § Checkpoint C-001.r1); the seven changes are wording, citation, and disclosure. No class, count, responsible actor or next reference changes. Rows 4, 5, 6, 7, 9, 10, 12, 13 passed as written and are unchanged.

**Row 1 (`20260903-wall-and-heating#1`) — the "at any efficiency" phrase is withdrawn.** The Status paragraph's sentence "heating-source efficiency is not the escape at the printed level, at any efficiency, in this window" is replaced by: *heating-source efficiency is not the escape at the printed level at any swept efficiency (0.40–0.60), and not below 0.871 at `eta_couple` 1.00; the 12 (I, T, n) cells behind the 36 sustainment-alone points open in the model at or above 0.871, and no source in the repository bounds whether such a source exists (record § 17). The other 204 blocked points fail the wall or the ceiling, which no efficiency reaches.* The `study.py` phrasing "not window-limited" and "factor of 1.5" is not imported into any row.

**Row 2 (`20260903-wall-and-heating#2`) — the "not new" claim is grounded on committed text.** The sentence "the falling constant-coupled curve is not (the pre-change model produced the same sign)" is carried on this basis: at the pre-WI-039 tree `860ce7d1`, `models/library/analyses/mfe_power_balance.sysml:134-136` computes `recirculating = … + p_input_in / eta_pin_in` and `:119` adds `p_input_in` to the thermal sum directly; `models/designs/generic_mfe/mfe_plant.sysml:399,403,526` bind `p_input`, `eta_pin` and `p_ecrh`; and `models/designs/stellarator_09/stellarator_plant.sysml:842-845` prices heating as `heating_ecrh_per_mw` × `p_ecrh`, with `p_ecrh` tied to `p_input` (`manifest.json` tie, since removed). A sweep of `eta_pin` at held `p_input`/`p_ecrh` therefore holds coupled power and heating capital and moves only the recirculating term — structurally the constant-coupled arm at `eta_couple` 1.00 — and record § 12's 36-point identity shows the rest of the model unchanged across the boundary. The scratch-worktree run of the pre-change oracle is corroboration only and carries nothing on its own; record § 17's "no matched pre-change comparison" stays true.

**Rows 3 and 8 (`20260903-wall-and-heating#3`, `20260903-priced-levers#1`) — the bounds carry their condition.** Wherever the r1 text calls 1.15–1.83× "the sourced bounds" or "T-001's correction bounds", read: *the sourced range for an **unoptimised equidistant wall at a 0.30 m standoff** — the only configuration the three registered sources measure (T-001 § 3: peaking 1.5–2.1 for unoptimised walls; § 4: shape factor 1.146–1.303 on the wall-side radius, from Lion alone). Lion's optimised walls on the same plasma give peaking 1.12–1.23 and so a net of 0.86–1.07, below the range; the model's 0.10 m standoff gains less area and peaks harder than Lion's 0.30 m wall (T-001 § 4), pushing above it.* Row 3's "so that round 2's fence change cannot invalidate round 1's reading unnoticed" is replaced by: *the shadow columns pre-register round 1's result over that range; a round-2 fence outside it, in either direction, is not pre-registered and round 2 must restate round 1's result against whatever form it chooses.* Row 8's "the likely direction (tightening)" is conditioned the same way T-001 § 5 conditions it: *tightening under an unoptimised wall at the source's standoff; recorded for scale, not as a prediction.*

**Row 11 (`20260901-sustainment-fence#4`).** "at the printed level it changes nothing (0 of 240 at any efficiency)" → *at the printed level it changes nothing (0 of 240 at any swept efficiency, 0.40–0.60).*

**Row 14 (`20260901-sustainment-fence#1`).** "it fails the wall under even the mildest sourced correction" → *under the low end of the unoptimised-wall range it fails the wall (3.886 × 1.15 = 4.469 against 4.05); under an optimised wall (net 0.86–1.07) it clears at the lower end and fails at the upper (4.041 at 1.04, 4.170 at 1.073). Whether the candidate survives is decided by the fence round 2 chooses, which is why WI-038 waits.* The r1 sentence "the owner's sequencing is now supported by measurement" is softened to *consistent with measurement over the unoptimised range*.

**Owed at the T-004 return (reviewer items 6 and 7), not disposition text:** (6) the trail's T-004 return carries the scope extension explicitly — arm `arm-couple-132`, wall-plug = 132/eta over eta 0.35–0.75, F1's reason — so record § 2's "recorded in `study.py` and in the trail" becomes true; (7) the stale note in the digested `axes.json` (`arm-couple-110`, `110/eta_source` — the first design's arm name and level) is disclosed as stale prose in a second record Addendum, written now, on the `20260821-power-cycle-ab#9` precedent; the artifact is not edited.
