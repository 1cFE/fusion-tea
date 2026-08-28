# Trail: p-pump-basis

What happened, and what was decided. Append-only, newest entry last, ISO dates. **No entry is ever edited in place.** A correction is `### Amendment YYYY-MM-DD — amends <entry heading>`, stating what changed and why.

This file logs judgment, not routine stage motion. Native workflows keep their own stage records; entries here cite them by path or native id and never restate their content. Procedure is in `work/orchestration/GOAL_RUNBOOK.md`.

## Round 1 — rebase-from-native-sources

### Strategy revision — 2026-08-28

- **Approach:** ask the repository first. Take the sourced circulator figures the goal already has in hand (`goal.md` § Grounding evidence), read each one at its cited line, decide which of them actually answers a *helium-primary loop* question, and derive from those a `p_pump` for `stellarator_09` on a stated basis. Land nothing; the value and its basis are trail-level output, which `goal.md` § Answered when says is a complete answer.
- **Assumptions:**
  - DI-008 as written is what this goal works against — the 2–6 % basis and the 60–190 MW band (`goal.md` § Grounding evidence, the recorded open item; `knowledge/KNOWLEDGE.md@ffa5c54c` DI-008).
  - The comparison baseline is the pin study `20260821-power-cycle-ab` ran against (`goal.md` § Invariants, Package).
  - `p_pump` reaches the verdicts through the two power-balance terms and nothing else (`goal.md` § Invariants, the channel).
- **Abandonment conditions:**
  - No admissible **helium-primary** datum survives reading at its cited line. The strategy would then be a research strategy, not a re-basing one, and the `research` seam is unrepaired.
  - The evidence turns out to fix the answer's *shape* (scalar vs computed) rather than leave it open — that is reserved gate 2 and the strategy stops rather than choosing.
  - The derived shift proves small enough to sit inside the study's grid resolution, which would make "keep 1.0 MW" the answer without any measurement.
- **Intended model increment:** `p_pump` in `models/designs/stellarator_09/stellarator_plant.sysml`, in both homes of the twin, re-based off the 1costingFE default onto a helium-circulator basis with a citation that resolves. Owner-gated (`goal.md` § Reserved gates 3); this round proposes it, it does not land it.
- **Intended study question:** at the re-based value, where does the `recirc_ok` fence sit across the (R, a) window study `20260821-power-cycle-ab` covered, and what does LCOE do there?

**No future task list.** The next task is chosen from evidence after this one returns.

### T-001 scope

- **Objective:** what value, if any, do repository-native sources support for `stellarator_09`'s primary-coolant pumping power, and on what basis?
- **Why now:** it is the first thing the strategy rests on, and `goal.md` § Question makes the second half of the question conditional on the first. Triggering evidence: discovery row `20260821-power-cycle-ab#3` and DI-008's model implication.
- **Scope:** authorized — read the three circulator figures at their cited lines, judge each against a helium-primary loop, derive a value and state its basis and its admissibility, and derive what it does to the plant power balance at the baseline point. Excluded — changing `p_pump` in either home of the twin (reserved gate 3); making it computed (gate 2); registering a source or touching a DI (gate 4); minting a work item or any other write under `work/`, `models/`, `knowledge/` (the general gate); any pressure-drop or coolant-loop modeling (gate 5).
- **Inputs:** `goal.md` in full. No narrower constraint than it states.
- **Done when:** either a value with a stated basis and a citation that resolves, or a bounded negative saying what the repository is missing and why the gap is not closable from inside this task.
- **Stop when:** an owner gate is reached that the objective cannot be met around, or the evidence contradicts a premise the strategy rests on.

### T-001 start — 2026-08-28

Re-base `p_pump` from native sources · native target: read-only over `knowledge/` sources, `knowledge/KNOWLEDGE.md`, the committed record `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/`, and `models/` · expected artifact: this trail's `### T-001 return`. No native write is expected; every write this task could make is behind a reserved gate.

### T-001 return — 2026-08-28

**Outcome:** `COMPLETE`.

**Evidence.**

- `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/scipub-wp-content-uploads-eurofusion-wppmicpr17-17709.md@0bf791d1:176` — Cismondi et al. 2017. Read at the line. It gives helium pumping power and, in the same paragraph, the blanket power it belongs to. Ingested, unregistered in `knowledge/SOURCE_INDEX.md@ffa5c54c` (grep for the author, the report id and the OSTI id returns nothing).
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1178069.md@aff7a2f9:175,290` — Kessel et al., ARIES-ACT overview. Read at both lines. Ingested, unregistered.
- `knowledge/KNOWLEDGE.md@ffa5c54c` DI-007, DI-008.
- `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md@ffa5c54c` § 1 — the three-figure table and its admissibility column.
- `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/results/baseline_result.json@ffa5c54c` — the baseline point's `fusion__p_fus` and `cryo_elec__p_elec` channels.
- `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/results/oracle_scan.json@ffa5c54c` — the baseline `rec_frac` and `p_net` per arm, used only as the target of a reconstruction check.
- `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/results/points.csv@0d176a8c` — the `p_fus` column, present at every row; the five power-balance columns, empty at every row.
- `models/library/analyses/mfe_power_balance.sysml@8f3b510c:119,135`; `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:490-560`; `models/designs/generic_mfe/mfe_plant.sysml@ba5c9945:305,330-544`.

Cited-ref liveness: every path `goal.md` cites was checked with `git log -1` at this session's HEAD and none has moved since the sha it is cited at. `snapshot.json` and `points.csv` last moved at `0d176a8c`, which is an ancestor of `881d4448`, so the record-directory citation still pins them.

**Reading.**

*What the sources say when read at the line, and which of them answers this question.*

Only one of the three figures is a helium-primary blanket circulator datum that is in the repository.

- **Cismondi 2017 is that one.** The same paragraph carries both halves of the ratio: the power deposited in the HCPB blanket and the helium pumping power for its loops. That gives **6.279 %** of blanket-deposited thermal power, for a helium loop at 80 bar. Stellaris's primary loop is helium at 8 MPa — the same pressure (`knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md@ffa5c54c` § 1, quoting the Stellaris extraction). This is a single reported figure, not a pumping-system design.
- **ARIES-ACT does not answer it.** Read at both lines, its blanket is self-cooled LiPb (DCLL); the 12 MW of helium is *divertor* coolant, and the "≈ 1 % of the total thermal power" in its conclusions is a whole-plant pumping figure for a machine with no helium-primary blanket. It is an admissible citation for what it says. It is not evidence about a helium primary loop, which is what `goal.md` § Question asks about.
- **Moscato 2018 is not in the repository.** It is the only helium-primary *pumping-system design* in the set and the only source that would give a band rather than a point. Bringing it in is the `research` seam, which is unrepaired, and registering it is reserved gate 4.

*The denominator, and why it lands on `p_th`.* DI-008 states the basis as a fraction of **blanket** thermal power, and the model has no blanket-only thermal channel — `mn·p_neutron` alone is 0.960 × `p_fus`, while DEMO's blanket-deposited power is 1.173 × its fusion power, so the two are not the same quantity. The model's `p_th` less the recovered pumping heat is 1.178 × `p_fus`, which matches DEMO's ratio to within 0.5 %. So the model quantity that is like-for-like with the source's denominator is `p_th`, not `mn·p_neutron`. Applying the fraction to `p_th` needs no split the model does not carry.

*The value.* At the baseline point (R 12.7 m, a 1.3 m), on the pin the comparison baseline names:

- as a **held scalar**, `p_pump` = 6.279 % × `p_th` ≈ **203 MW**;
- as a **computed fraction** of `p_th`, self-consistently (because `p_th` contains `eta_p·p_pump`, the equality closes in one step): **210 MW**.

The two differ by 3.2 %. Both are ~200 × the held 1.0 MW. Both sit at or just above the top of DI-008's stated 60–190 MW band, because DI-008 rounded 6.279 % down to 6 % and applied it to the paper's printed ~3150 MWth rather than to the model's computed thermal power.

*So the first half of `goal.md` § Question has an answer.* 1.0 MW is not defensible for a helium-primary loop at this plant scale. It is 0.03 % of thermal power against a sourced 6.3 %, and the one source in the repository that speaks to the case says so directly.

*What the repository does not support.* It does not support DI-008's **2–6 % band**. The band's low end comes from a machine with no helium-primary blanket, and its other helium-primary leg is not in the repository. What the repository supports today is a **single point**, from a single unregistered source. That is a narrower claim than DI-008 makes, and it is the reason the second half of `goal.md` § Question is answerable as a number but not yet as a range.

*What the re-based value does at the baseline point, and what it does not tell us.* Reconstructing the plant power balance by hand from the committed `p_fus` channel and the design's bound inputs reproduces the study's own reported baseline `rec_frac` (0.1514) and `p_net` (915.1 MW) exactly, so the reconstruction is checked, not assumed. At 203 MW: `rec_frac` goes 0.151 → 0.330 in the η 0.333 arm and 0.116 → 0.242 in the η 0.47 arms; `p_net` falls 18.5 % and 11.6 %. **No verdict flips at the baseline point** — the `recirc_ok` threshold is 0.5 and both stay under it. Two things this does *not* establish, and must not be read as establishing:

- **Where the fence moves.** `recirc_ok` is already violated at small R (record § 4), and a recirculating sum that roughly doubles moves that boundary outward. Locating it is the round's study question, not this task's result.
- **What LCOE does.** `p_th` feeds nine cost accounts directly through `mfe_plant.sysml@ba5c9945` (buildings, aux cooling, heat rejection, waste, incremental, and others), so a re-based `p_pump` moves capital as well as net power. `goal.md` § Invariants routes LCOE through `p_net`; that is the larger of the two paths but not the only one. LCOE is not hand-derivable here and needs a package run.

*One bounded observation about the evidence layer.* The reconstruction above worked because `points.csv` carries `p_fus` at every row while the five power-balance columns are empty. So the operand `rec_frac` — the governing quantity of finding `#10` — is recoverable post hoc from the committed record alone, without the oracle. That does not make a hand reconstruction a package result: the invariants read results as LCOE plus the five verdicts, and LCOE does not come out of this arithmetic. `goal.md`'s statement that measuring the fence needs a package run therefore stands. This observation is a finding this round made itself, so it is not a discovery-log row; its home is the round's proposed learning delta at close.

**Decision D-1 — the denominator.**
- *Trigger:* DI-008 names "blanket thermal power" as the basis, but computed its own Stellaris numbers against total thermal power, and the model carries no blanket-only channel.
- *Decision and reason:* apply the fraction to the model's computed `p_th`. The like-for-like check holds — the model's `p_th` less recovered pumping heat is 1.178 × `p_fus` against DEMO's blanket deposition at 1.173 × `p_fus` — so `p_th` matches the source's denominator to within 0.5 % and no split the model does not carry has to be invented.
- *Tier:* execution detail.
- *Decided by:* round agent.
- *What changed:* none. Trail only.

**Decision D-2 — the band is not natively supported.**
- *Trigger:* reading the three figures at their cited lines. ARIES-ACT's 1–2 % is a LiPb-cooled blanket with helium only in the divertor; Moscato is not in the repository. Only Cismondi speaks to a helium primary loop.
- *Decision and reason:* derive the value from Cismondi alone, and report DI-008's 2–6 % band as **not supported by what the repository holds** — one point, one source, unregistered. Reason: `goal.md` § Question asks about a helium-primary loop, and a figure from a machine without one is not evidence about it. Recording this narrowing is required rather than resolving it silently.
- *Tier:* premise surprise. It cuts against DI-008 as written, which is the premise the strategy declared it works against, and it bears directly on the 60–190 vs 30–190 band discrepancy `goal.md` § Grounding evidence logged as an owner item — the 30 MW end is the ARIES-ACT leg, and this reading says that leg does not apply.
- *Decided by:* round agent; surfaced to the owner, not resolved. Amending or re-sourcing DI-008 is reserved gate 4.
- *What changed:* none. Trail only.

**Decision D-3 — the answer's shape is referred, not chosen.**
- *Trigger:* the derivation produces two admissible forms — a held scalar at 203 MW and a computed fraction of `p_th` at 210 MW — and `goal.md` § Answered when leaves the shape open as the goal's own work.
- *Decision and reason:* report both with their arithmetic and refer the choice. Making `p_pump` computed retires it as a settable input under `STUDY_POLICY.md@ad2fb4ea` § 2 rule 3, which is reserved gate 2 and a comparison-meaning change the operator sees before a round acts on it, not after.
- *Tier:* reserved gate.
- *Decided by:* referred to the owner.
- *What changed:* none.

**Decision D-4 — nothing is landed and no source is registered.**
- *Trigger:* the derived value exists and the natural next moves are to bind it in `stellarator_plant.sysml`, to register Cismondi in `SOURCE_INDEX.md`, and to mint the modeling item DI-008 asks for.
- *Decision and reason:* none of the three is done. Gate 3 holds the value change, gate 4 holds the source and the DI, and the general gate holds any write under `work/`, `models/` or `knowledge/`. `goal.md` § Answered when says a trail-only answer is complete, so the objective did not need any of them.
- *Tier:* reserved gate.
- *Decided by:* referred to the owner.
- *What changed:* none.

### T-001 dispositions — proposed, 2026-08-28

Not a contract entry kind. It exists because `GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint reviews a reading **and its proposed dispositions** before any semantic follow-up executes, so the dispositions have to be a reviewable object before the checkpoint sits. Nothing here is written to `DISCOVERY_LOG.md`; the append happens after the checkpoint passes.

**`20260821-power-cycle-ab#3` — the goal's consumer. Proposed disposition: `model fix`, routed, not yet answered.**

The row's premise is confirmed and made sharper. Its own wording says `p_pump` is "roughly 100×" below helium-primary figures; read against the one native helium-primary source it is ~200× below, and the sourced value sits at or above the top of the band DI-008 states. Routed to goal `p-pump-basis`, round 1, task T-001. **No work item is minted** — minting one is a `work/` write under the general reserved gate, and the value change itself is gate 3. Home: the existing WI-031 R4 follow-up the row already names, plus `work/orchestration/goals/p-pump-basis/trail.md`.

**`20260821-power-cycle-ab#5` and `#10` — touched, already disposed, no new row proposed.**

This task's reconstruction ran over exactly the gap these two rows describe, so the evidence touches them. Both already carry a disposition and both are routed outside this goal (`#5` to the evidence layer, `#10` to study-runbook step 9, already applied as executor practice). The runbook's obligation is that every **open** row the evidence touched gets a disposition; neither is open. The one fact this task adds — that the missing operand is reconstructible from the committed `p_fus` column plus the design's bound inputs, without the oracle — is a finding this round made itself, so it belongs in the round's learning delta, not in a log row. Stated here so the checkpoint reviewer can disagree with the judgment rather than have to notice it.

**Nothing else was touched.** No other row in `DISCOVERY_LOG.md@e891b23a` bears on this task's evidence.

### Stop — 2026-08-28

- **Kind:** `handoff`.
- **What is true on disk:** nothing outside this file has been written. `models/`, `knowledge/`, `work/` and `exploration/` are unchanged; no source is registered, no DI is amended, no work item is minted, `p_pump` is still 1.0 MW in both homes of the twin, and `DISCOVERY_LOG.md` is unchanged at `e891b23a`. T-001 is returned `COMPLETE`. The round is open: it has a strategy revision and no round result.
- **What the owner must see:** a fresh session is needed to review the T-001 reading and its proposed dispositions before any follow-up task executes. This session authored them and may not review them (`GOAL_RUNBOOK.md` § What "fresh" means). Two items also point at the owner directly and are not this round's to settle: **D-2**, the premise surprise that DI-008's 2–6 % band is not supported by what the repository holds and that its low end comes from a machine with no helium-primary blanket — which bears on the 60–190 vs 30–190 discrepancy `goal.md` already logged; and **D-3/D-4**, the three reserved gates the answer now runs into (the scalar-vs-computed shape, the value change in the twin, and registering Cismondi).
- **The material to review:** `work/orchestration/goals/p-pump-basis/trail.md` (`### T-001 return` and `### T-001 dispositions`), against `work/orchestration/goals/p-pump-basis/goal.md` and the evidence refs listed in the return. Resume at `GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint.

### Checkpoint C-001.r1 — 2026-08-28

**Reviewer.** A fresh session, opened by the operator for this gate. It authored no part of round 1 — not the strategy revision, not the T-001 scope, start, return, or proposed dispositions — and carried none of that session's reasoning into this one (`GOAL_RUNBOOK.md` § What "fresh" means). It read `goal.md`, `GOAL_RUNBOOK.md`, `.project/adr/004-finding-disposition.md`, and every evidence ref the return cites, at the cited lines, and re-derived the arithmetic independently rather than checking the return's own working.

**The reading reviewed.** `### T-001 return — 2026-08-28`, outcome `COMPLETE`: that only Cismondi 2017 is a native helium-primary datum, that the fraction lands on the model's computed `p_th`, that the value is ~203 MW held or ~210 MW computed, that 1.0 MW is not defensible, that DI-008's 2–6 % band is not natively supported, and the baseline power-balance effect. Decisions D-1 through D-4.

**The dispositions reviewed.** `### T-001 dispositions — proposed, 2026-08-28`: `#3` as `model fix`, routed, not yet answered; `#5` and `#10` as touched but already disposed with no new row; nothing else touched.

**Verdict: does not pass. Revise and resubmit as C-001.r2.** Two of the three required changes bear on claims the round is handing to the owner, and one is a disposition the runbook does not permit as written. No semantic follow-up task may execute against this reading until a passing checkpoint entry exists (`GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint). This is submission 1 of 3; the cap is 2 revisions (`goal.md` § Limits).

**What re-derivation confirmed.** Stated so the author does not re-do it and so a later reader can see what the verdict rests on.

- Cismondi at `…wppmicpr17-17709.md@0bf791d1:176`. The paragraph carries both halves: fusion power 2037 MW, "the power deposited in the HCPB and WCLL of 2389 MW and 2045 MW respectively", and "In case of helium the pumping power is ~150MW". 150 / 2389 = 6.2788 %. Helium at 80 bar, confirmed in the same paragraph. Its blanket-to-fusion ratio is 2389 / 2037 = 1.173.
- ARIES-ACT at `…purl-1178069.md@aff7a2f9:175,290`. The reading is right and the reason is right. Line 290: "Both configurations utilize Li15.7Pb84.3 as liquid-metal breeder/coolant"; line 175 puts the 12 MW of helium in the divertor. There is no helium-primary blanket in either configuration, so its 1–2 % is not evidence about one. (One detail to correct in passing: the return calls the blanket "self-cooled LiPb (DCLL)". ACT1 is DCLL, ACT2 is SCLL. It does not change the conclusion.)
- The denominator. `p_alpha` = (3.52/17.58)·`p_fus`, so `mn·p_neutron` = 1.2 × 0.79977 = 0.95973 × `p_fus`, and `p_th` − `eta_p·p_pump` = 1.17815 × `p_fus` against DEMO's 1.17280 — within 0.46 %.
- The value. At the baseline `p_fus` = 2748.057 MW (`baseline_result.json@ffa5c54c`), `p_th` = 3238.1 MW and 6.279 % of it is 203.3 MW. Solving the self-referential form (`p_th` contains `eta_p·p_pump`) gives 209.9 MW. The 3.2 % gap between them is as stated.
- The baseline effect. Reconstructing the balance from `p_fus` plus the design's bound inputs reproduces the study's own `rec_frac` 0.1514 and `p_net` 915.1 in the paper arm and 0.116 / 1345.4 in the sCO2 arm (`oracle_scan.json@ffa5c54c`) — exactly, so the reconstruction is checked. At 203 MW: `rec_frac` 0.1514 → 0.3294 and 0.116 → 0.2421; `p_net` −18.5 % and −11.6 %. No verdict flips at baseline against the 0.5 threshold. All as stated.
- `points.csv@0d176a8c`: `p_fus` non-empty at all 3,792 rows; `p_net`, `rec_frac`, `q_eng`, `p_th`, `p_et` empty at all 3,792. As stated.
- Nine cost accounts take `p_th` directly in `mfe_plant.sysml@ba5c9945` (lines 330, 338, 366, 405, 431, 505, 515, 526, 544). Exactly nine.
- Citation liveness. Every path the return cites is at the sha it is cited at, checked at this session's HEAD. `0d176a8c` and `ffa5c54c` are both ancestors of `881d4448`, so the record-directory citation still pins them.
- Scope and gates. Nothing was written outside the goal directory. `models/`, `knowledge/`, `work/` and `exploration/` are unchanged, `p_pump` is still 1.0 at `stellarator_plant.sysml@ba5c9945:502`, and `DISCOVERY_LOG.md` is unchanged at `e891b23a`. The round stayed inside the T-001 scope and behind every reserved gate, and the strategy's abandonment conditions were honoured — the shape question was referred, not chosen.

**Required change 1 — `#5` may not return as touched-and-already-disposed. It is `unrouted`.**

The newest row under `20260821-power-cycle-ab#5` is its sighting, at `DISCOVERY_LOG.md@e891b23a:11`, and its Home column reads `unrouted` — an evidence-layer question for sysml-codegen / teax. The proposed dispositions say `#5` "already carries a disposition and is routed outside this goal". What it carries is the study executor's account of how the study handled the gap ("empty export columns kept and disclosed"); its routing is the word `unrouted`. ADR-004 is unconditional on this point: "Every open discovery row a round's evidence touches receives a disposition… **No touched row returns as `unrouted`.**" The round agrees its evidence touched the row — its own words are that the reconstruction "ran over exactly the gap these two rows describe".

The reasoning that sends the new fact to the learning delta instead conflates two rules. ADR-004's "a finding the round discovers itself is not a discovery-log row" bars **minting an id**. Here the id already exists, its subject is exactly this gap, and it is open. Appending under `#5` is not minting; it is the obligation. And the round is holding precisely what the row has been missing: a concrete next reference — the operand is recoverable post hoc from the committed `p_fus` column plus the design's bound inputs, with no oracle, because every other term in the recirculating sum is a bound constant at every grid point (`p_coils` 0, `p_aux` 14, `p_cool` 15, `p_cryo` 0.8644 from geometry-independent inputs, `p_input/eta_pin` 100) and `p_sub` follows from `eta_th`, which `points.csv` carries as a swept column. I checked that: `p_cryo` derives from `q_nuc_cryo` 35.5 × `vol_cold_cryo` 136.56 plus `p_fixed_cryo`, all bound, so it does not move with (R, a).

Propose a disposition row for `#5` under its own id, in the ADR-004 fields, with that as the next reference. The generalizable claim can still go to the learning delta; the two homes are not exclusive. `#10` needs nothing — its Home is "runbook step 9; applied as executor practice in study 1", which is a real routing, and the round's read of it is correct. `#3` is fine as proposed.

**Required change 2 — "a single point, one source" overstates the poverty of the evidence, and it is the claim going to the owner.**

D-2 concludes that the repository supports one point from one source and that DI-008's 2–6 % band is "not supported by what the repository holds". The first half is not right as written. Moscato's helium-primary HCPB figures are in the repository — quoted, with their inputs, in `…wi031-item6-second-arm-values.md@ffa5c54c:47`, the approved research artifact the return itself cites two items earlier: 2101.7 MWth, nine loops of two compressors, ≈131 MW total (6.2 %), and a near-term eight-loop design at 83–94 MW (~4 %). That is a second helium-primary HCPB data point at the same quality DI-008 was minted from. What is absent is the *source PDF*, not the figures.

This is not a quibble, because it moves the answer. Admit the near-term Moscato leg and the helium-primary evidence supports roughly 4–6.3 %, i.e. ~130–205 MW at the model's `p_th` — a range, sitting **inside** DI-008's 60–190 MW band at its lower end rather than above it. Exclude it and you get the return's single point above the band. The owner is being asked to act on the difference.

There is a defensible reason to exclude it: a figure quoted in an approved research file cannot be re-derived at a cited line in the source, which is the standard this task applied to Cismondi and ARIES-ACT. If that is the reason, say it as the reason, in the return, and let the owner see the rule being applied. What the entry may not do is assert "Moscato 2018 is not in the repository" without qualification while citing the artifact that holds its numbers.

Either way, restate D-2 to the claim the evidence actually carries: **the low end of DI-008's band does not apply**, because its 1–2 % leg comes from a machine with no helium-primary blanket. That is the finding, it is sound, and it is what bears on the 60–190 vs 30–190 discrepancy `goal.md` logged. "Only one point exists" is a stronger and shakier claim riding on top of it.

**Required change 3 — carry the value at the precision and with the qualification its source gives it.**

The source says "~150MW". The return turns that into 6.279 %, 203 MW and 210 MW, a 3.2 % gap between the two forms, and "at or just above the top of DI-008's stated 60–190 MW band". Four significant figures out of one approximate one. At the source's own precision — ~6 % — the value is ~194 MW, which sits **at** the top of DI-008's band, not above it. The sharpest comparative claim in the reading is an artifact of precision the source does not carry.

The same paragraph also qualifies the figure in a way the reading does not report: "Accurate design studies are on-going to reduce the pressure drop in the helium loops and consequently the requested pumping power," followed by the specific lever — larger pipes would cut the loop from ~9 km to ~3 km. So 150 MW is a preliminary figure for one unoptimized layout that its own authors expect to fall, which is consistent with Moscato's near-term ~4 %. Report the value as approximately 200 MW, or ~6 % of `p_th`, with that qualification stated where the value is proposed and not only in the "single reported figure" aside. The conclusion that 1.0 MW is indefensible is robust to all of this — it survives at any precision and either end of the range — and the entry should say so plainly rather than resting on a sharp number.

**Two observations, not required changes.**

- The like-for-like denominator check includes `p_input` (50 MW of plasma heating) in the quantity compared against DEMO's blanket deposition, which is not blanket-deposited power. The cleaner comparison, (`mn·p_neutron` + `p_alpha`) / `p_fus` = 1.160 against DEMO's 1.173, is within 1.1 % and reaches the same place; the value moves by about 1.5 %. D-1 stands on either version. Worth tightening if the return is being revised anyway.
- The reading's stated warrant for transporting Cismondi's ratio to Stellaris is the pressure match (80 bar against 8 MPa). Matching pressure alone is thin — the fraction also depends on mass flow, blanket ΔT and loop pressure drop. The source carries a stronger warrant that the reading passes over: "the HCPB PHTS can be also be considered representative for the HCLL concept", and Stellaris's blanket is HCLL (`…wi031-item6-second-arm-values.md@ffa5c54c` § 1, quoting `output.md:1349`). Use it. The conclusion is better supported than its stated grounds.

**One thing for the round review, flagged and left there.** `goal.md` § Invariants routes LCOE through `p_net`. The return found that `p_th` also reaches nine cost accounts directly, which I confirmed exactly. The round handled this honestly in prose and did not widen the channel — it traced it. But it is a correction to a goal-level statement of what the channel does, and where that lands is the round result's and the fresh review's call, not this checkpoint's.

**What passes.** The arithmetic, the source readings, the citation liveness, the scope discipline, the gate discipline, and the refusal to choose the answer's shape. The reading's central conclusion — 1.0 MW is not defensible for a helium-primary loop at this plant scale — is confirmed and is not in question. The three required changes are about how narrowly the supporting claim is drawn, how precisely the number is carried, and one disposition the runbook does not allow.
