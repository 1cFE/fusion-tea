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

### T-001 return — revised r2, 2026-08-28

Revision 1 of 2, submitted as C-001.r2. This entry replaces nothing: `### T-001 return — 2026-08-28` stands as written and the disagreement is the record.

**What this revision changes.** All three required changes of `### Checkpoint C-001.r1` are applied. Both non-required observations are taken. One statement inside the checkpoint's own confirmations is disputed, with the evidence, below. The outcome is unchanged at `COMPLETE`, and the central conclusion is unchanged and now rests on more evidence, not less.

**Additional evidence read for this revision.**

- `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md@ffa5c54c:43` — the Moscato row of the three-figure table, with its inputs.
- `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/scipub-wp-content-uploads-eurofusion-wppmicpr17-17709.md@0bf791d1:176` — re-read for two sentences the first return passed over: the HCPB-to-HCLL representativeness statement, and the statement that the pumping figure is expected to fall.
- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/output.md@e5a2cb23:1349` and `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:490` — Stellaris's blanket is HCLL, in the source and in the model's own citation.
- `models/library/analyses/mfe_cryo_plant.sysml@8f3b510c:47-52` with the bound inputs at `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:567-600`, and `:508,530,626,629` — for the constancy check the `#5` disposition now rests on.
- `.project/adr/004-finding-disposition.md@007d9488`.

**Required change 1 — accepted. `#5` gets a proposed disposition row.**

The checkpoint is right and my reasoning was wrong. ADR-004's bar on a self-discovered finding becoming a log row is a bar on **minting an id**; `#5` already exists, its subject is exactly the gap this task's reconstruction ran over, and its Home column reads `unrouted`. What I read as "already disposed" is the executor's account of how the study *handled* the gap, which is not a routing. "No touched row returns as `unrouted`" is unconditional. The proposed row is in the revised dispositions entry below.

I checked the constancy claim the row's next reference depends on, rather than taking it from the checkpoint. Every other term of the recirculating sum is a bound constant at every grid point: `p_tf` 0 and `p_pf` 0 (`stellarator_plant.sysml@ba5c9945:508,626`), `p_tfcool` 15.0 and `p_pfcool` 0 (`:530,629`), `p_trit` 10.0 and `p_house` 4.0, `p_input`/`eta_pin` = 100. `p_cryo` is computed but from bound inputs only — `q_nuc` 35.5, `vol_cold` 136.56, `p_fixed` 0.0075, `f_uplift` 1.0, `T_cold` 20, `T_amb` 300, `f_carnot` 0.20 — so `mfe_cryo_plant.sysml@8f3b510c` returns 0.864352 MW at every point, matching the baseline channel exactly and moving with neither R nor a. `p_sub` is `f_sub`·`eta_th`·`p_th`, and `points.csv` carries `eta_th` as a column. So `rec_frac` and `p_net` are recoverable at all 3,792 rows from the committed record alone.

**Required change 2 — accepted, with the grade stated.**

"Moscato 2018 is not in the repository" was too flat, and it carried the claim that mattered. The *figures* are in the repository, in the approved research artifact this return already cites: 2101.7 MWth, nine loops of two compressors, ≈131 MW total, and a near-term eight-loop design at 83–94 MW (`…wi031-item6-second-arm-values.md@ffa5c54c:43`). What is absent is the source PDF.

**I admit them, at second-order grade, and say what the grade means.** They are a prior session's transcription from a web-fetched PDF that was never ingested, so unlike Cismondi and ARIES-ACT they cannot be re-derived at a line in a source — the standard this task applied to the other two. They are not thereby worthless: the artifact is approved, it is in the repository's own research pipeline, and DI-008 was minted partly from it. Admitting them at that grade and saying so is more honest than excluding them silently, and it is what the owner needs in order to weigh the answer.

The consequence is that the answer is a range, not a point:

| source | grade | fraction of thermal power |
|---|---|---|
| Cismondi 2017, HCPB, ~150 MW / 2389 MW | ingested extraction, read at the line | ~6 % |
| Moscato 2018, HCPB, ≈131 MW / 2101.7 MWth | second-order, via the approved research artifact | ~6 % |
| Moscato 2018, near-term 8-loop, 83–94 MW | second-order, same | ~4 % |

**And D-2's claim is restated to what the evidence carries: the low end of DI-008's 60–190 MW band does not apply.** DI-008 built that band as 2–6 % of ~3150 MWth. The 2 % leg is ARIES-ACT, a machine with no helium-primary blanket, so the ~60 MW floor has no helium-primary evidence behind it. The helium-primary evidence supports **~4–6 %**, which at the model's computed thermal power is **~130–195 MW** — inside DI-008's band, in its upper half. The first return's "a single point, one source, above the band" was a stronger and shakier claim riding on the sound one, and it is withdrawn.

**Required change 3 — accepted. The value is carried at ~6 %, not 6.279 %.**

The source says "~150MW". Four significant figures do not come out of one approximate one, and the sharpest comparative claim in the first return — "at or just above the top of the band" — was an artifact of that false precision. At the source's own precision the value is **~195 MW held, ~200 MW computed**, which is *at* the top of DI-008's band, not above it.

The same paragraph also qualifies the figure, and the first return reported this only as an aside about the source's kind: "Accurate design studies are on-going to reduce the pressure drop in the helium loops and consequently the requested pumping power", with the specific lever named — larger pipes would cut the loop from ~9 km to ~3 km. So ~150 MW is a preliminary figure for one unoptimized layout that its own authors expect to fall. That is consistent with Moscato's near-term eight-loop design at ~4 %, and it means **the low end of the ~4–6 % range is the direction of travel, not an outlier**. The value is proposed with that qualification attached, not with it in a footnote.

**None of this touches the answer to the first half of `goal.md` § Question.** 1.0 MW is ~0.03 % of thermal power against a sourced 4–6 %. That holds at any precision, at either end of the range, and with or without the Moscato leg. Stated plainly: the conclusion does not rest on a sharp number and never needed one.

**Observation 1 — taken, as a reported sensitivity rather than a change of basis.**

Both readings of the like-for-like check are reported: including the 50 MW of plasma heating, the model's thermal power is 1.178 × `p_fus`; excluding it, 1.160 × `p_fus`; DEMO's blanket deposition is 1.173 × its fusion power. Both are within 1.2 % of DEMO. The value moves 1.6 % between them, which is inside the source's own precision and invisible at ~6 %. I do not switch the basis, because `p_input` is heating power that does reach the wall and DEMO's own 2389 MW cannot be shown from the paragraph to exclude the equivalent term. Reporting both is what the evidence supports; picking one would assert a resolution the source does not give. D-1 stands, and is now stated with its sensitivity.

**Observation 2 — taken.**

The stated warrant for transporting an HCPB ratio to Stellaris is replaced. Pressure match alone was thin. The source carries the warrant directly: "the HCPB PHTS can be also be considered representative for the HCLL concept", and Stellaris's blanket is HCLL — in the extraction (`…output.md@e5a2cb23:1349`) and in the model's own citation for `mn` (`stellarator_plant.sysml@ba5c9945:490`). Both native helium-primary data points are HCPB, and the source itself licenses the transport. The 80 bar / 8 MPa match is now corroboration, not the argument.

**One statement in the checkpoint disputed: the ACT1/ACT2 blanket assignment is inverted, and my own phrasing was wrong too.**

The checkpoint corrects "self-cooled LiPb (DCLL)" with "ACT1 is DCLL, ACT2 is SCLL". Read at `…purl-1178069.md@aff7a2f9:290`, it is the other way round. The paragraph pairs each characterization with its configuration: "The **advanced** characterization of high βN (5.75), high H98 (1.65), and SiC composite structure **SCLL** blanket concept … results in a 6.25-m plasma", and "The **conservative** characterization of low βN, low H98, and RAFM steel structure **DCLL** blanket concept … results in a 9.75-m plasma"; the same page identifies "ACT2 (conservative physics/conservative technology)". Conservative is ACT2, so **ACT1 is SCLL and ACT2 is DCLL**.

My own phrasing was separately wrong: "self-cooled LiPb (DCLL)" conflated the two concepts. DCLL is dual-coolant — helium *and* LiPb — and SCLL is the self-cooled one. The correct statement: both configurations use Li₁₅.₇Pb₈₄.₃ as liquid-metal breeder/coolant (`:290`); ACT1's blanket is SCLL, ACT2's is DCLL; in both, helium is the divertor coolant (`:175`, 10 MW for ACT1 and 12 MW for ACT2).

**Neither error changes anything.** Neither configuration has a helium-primary blanket, which is the whole of the reason ARIES-ACT does not answer this goal's question. Recorded because the checkpoint's correction would otherwise enter the record as fact. One further detail while at the line: `:175` reports ≈2 % for *both* ACT1 and ACT2 in the divertor section, while `:290` reports ~1 % of total thermal power in the conclusions. DI-008 already reads the pair that way ("~1 %, 2 % for helium in the divertor"); no correction is proposed, and neither figure is a helium-primary-blanket figure.

**The revised reading, in full.**

The repository holds two helium-primary HCPB circulator data points at different grades, and one figure from a machine that has no helium-primary blanket. Read together, the two that apply support a primary-circulator power of **~4–6 % of thermal power** for a helium loop at 80 bar, transported to Stellaris on the source's own HCPB-representative-for-HCLL statement. At the model's computed thermal power that is **~130–195 MW** as a held scalar, or **~130–200 MW** as a computed fraction, at the baseline point on the comparison pin. The upper end is a preliminary figure its authors expect to fall; the lower end is the near-term optimized design.

Against that, `p_pump` = 1.0 MW is ~0.03 % of thermal power. **1.0 MW is not defensible for a helium-primary loop at this plant scale**, and the finding does not depend on which end of the range or which precision is taken.

Against DI-008 as written: the 60–190 MW band's **upper** half is what the helium-primary evidence supports, and its **lower** end is not supported at all, because the 2 % leg it was built from is not a helium-primary machine.

Effect at the baseline point, from the reconstruction the checkpoint independently confirmed: `rec_frac` 0.1514 → 0.266 (4 %) or 0.322 (6 %) in the η 0.333 arm, and 0.116 → 0.197 or 0.237 in the η 0.47 arms; `p_net` falls 11.8–17.7 % and 7.4–11.1 %. **No verdict flips at the baseline point** against the 0.5 threshold. Where the `recirc_ok` fence moves, and what LCOE does, still need a package run — `p_th` reaches nine cost accounts directly, so LCOE is not hand-derivable, and locating the fence is the round's study question, not this task's result.

**Decision D-1 — revised. The denominator, with its sensitivity.**
- *Trigger:* DI-008 names "blanket thermal power" as the basis; the model has no blanket-only channel; and the like-for-like check can be drawn with or without the plasma-heating term.
- *Decision and reason:* apply the fraction to the model's computed `p_th`, and report both forms of the check — 1.178 × `p_fus` including `p_input`, 1.160 excluding, against DEMO's 1.173. Both are within 1.2 %; the value moves 1.6 % between them, inside the source's own precision. Neither is asserted over the other, because the source paragraph does not say whether its 2389 MW excludes the equivalent term.
- *Tier:* execution detail.
- *Decided by:* round agent.
- *What changed:* none. Trail only.

**Decision D-2 — revised. What the evidence says about DI-008's band.**
- *Trigger:* reading the three figures at their available grades. ARIES-ACT has no helium-primary blanket. Moscato's figures are in the repository in an approved research artifact, though its source PDF is not.
- *Decision and reason:* admit Moscato at second-order grade with the grade stated, and conclude that the helium-primary evidence supports ~4–6 % (~130–195 MW), so **the low end of DI-008's 60–190 MW band does not apply** while its upper half does. Reason: the goal's question names a helium-primary loop, and the 2 % leg the ~60 MW floor was built from comes from a machine without one. The first return's stronger claim — one point, one source, above the band — is withdrawn as overstated.
- *Tier:* premise surprise. It still cuts against DI-008 as written, and it still bears on the 60–190 vs 30–190 discrepancy `goal.md` § Grounding evidence logged for the owner — the 30 MW end is the same ARIES-ACT leg. What changed is the direction: the band's floor is unsupported, not its ceiling exceeded.
- *Decided by:* round agent; surfaced to the owner, not resolved. Amending or re-sourcing DI-008 is reserved gate 4.
- *What changed:* none. Trail only.

**Decisions D-3 and D-4 carry unchanged.** The answer's shape stays referred under reserved gate 2 — now as a range, ~130–195 MW held against ~130–200 MW computed. Nothing is landed, no source is registered, no work item is minted, under gates 3 and 4 and the general gate. Neither decision is re-argued here; the originals stand as written.

**Two items flagged for the round review, not resolved here.**

- The LCOE channel. `goal.md` § Invariants routes LCOE through `p_net`; `p_th` also reaches nine cost accounts directly. The checkpoint confirmed the count and left where this lands to the round review. Unchanged from the first return.
- `goal.md` § Grounding evidence says of Moscato "it is the one not in the repository". That is imprecise in exactly the way required change 2 corrected in my return: the source is absent, the figures are present in the artifact `goal.md` cites in the same bullet. Surfaced rather than resolved — `goal.md` is amended by the operator, in its own § Amendments, and a round does not edit it.

### T-001 dispositions — proposed, revised r2, 2026-08-28

Supersedes the proposals in `### T-001 dispositions — proposed, 2026-08-28`; that entry stands as written. Still nothing is written to `DISCOVERY_LOG.md` — the append happens after a passing checkpoint.

**`20260821-power-cycle-ab#3` — the goal's consumer. Proposed disposition: `model fix`, routed, not yet answered.** Unchanged in kind; the finding it carries is revised. The row's own wording says `p_pump` is "roughly 100×" below helium-primary figures; read against the helium-primary evidence at its available grades it is **~130–195×**, i.e. the row understates its own case, and the sourced range sits in the upper half of DI-008's band rather than at a single point above it. Routed to goal `p-pump-basis`, round 1, task T-001. No work item is minted — that is a `work/` write under the general reserved gate, and the value change is gate 3. Home: the WI-031 R4 follow-up the row already names, plus `work/orchestration/goals/p-pump-basis/trail.md`.

**`20260821-power-cycle-ab#5` — new proposal, replacing the first return's "touched, already disposed". Proposed disposition: `declared seam`.**

- *Kind:* `declared seam`.
- *Status:* the gap stands; its practical cost for this package is removed.
- *Responsible:* not this goal. The underlying fix is an evidence-layer change in sysml-codegen / teax, outside this repository, exactly as the sighting row's Home says.
- *Concrete next reference:* `rec_frac` and `p_net` are recoverable at all 3,792 rows of `results/points.csv@0d176a8c` from the committed record alone, with no oracle and no re-run — every other term of the recirculating sum is a bound constant at every grid point (`p_tf` 0, `p_pf` 0, `p_tfcool` 15.0, `p_pfcool` 0, `p_trit` 10.0, `p_house` 4.0, `p_input`/`eta_pin` 100, and `p_cryo` = 0.864352 from bound cryo inputs only), `p_sub` follows from the `eta_th` column the CSV carries, and `p_th` follows from the `p_fus` column. The recipe was checked against the study's own reported baseline values in both arms and reproduces them exactly.
- *Why `declared seam` and not `upstream filing`:* filing anything with sysml-codegen or teax is an action outside this goal directory and outside every gate this round holds. What this round can honestly record is that the seam is declared and no longer blocks a reader of this package. If the checkpoint reads the obligation as requiring `upstream filing`, that is a defensible alternative and the row can be rewritten to it; the difference is which word names a fix this round cannot perform.

**`20260821-power-cycle-ab#10` — no new row, unchanged from the first return.** Its Home is "runbook step 9; applied as executor practice in study 1", which is a real routing, not `unrouted`. The checkpoint concurred.

**Nothing else was touched.** No other row in `DISCOVERY_LOG.md@e891b23a` bears on this task's evidence.

### Stop — 2026-08-28

Second stop of this date; it follows the revised return and dispositions above.

- **Kind:** `handoff`.
- **What is true on disk:** unchanged from the first handoff except this file. Nothing outside `work/orchestration/goals/p-pump-basis/trail.md` has been written. `models/`, `knowledge/`, `work/` and `exploration/` are untouched; no source is registered, no DI is amended, no work item is minted, `p_pump` is still 1.0 MW at `stellarator_plant.sysml@ba5c9945:502` in both homes of the twin, and `DISCOVERY_LOG.md` is unchanged at `e891b23a`. T-001 remains returned `COMPLETE`. The round is open: strategy revision present, no round result.
- **What the owner must see:** a fresh session is needed for checkpoint resubmission **C-001.r2** — submission 2 of 3, revision 1 of 2 (`goal.md` § Limits). This session authored the revision and may not review it. Three things also point at the owner and are not this round's to settle: **D-2**, that the low end of DI-008's 60–190 MW band has no helium-primary evidence behind it, which bears on the 60–190 vs 30–190 discrepancy `goal.md` already logged; **D-3/D-4**, the reserved gates the answer runs into (the scalar-vs-computed shape, the value change in the twin, registering Cismondi and the grade at which Moscato's figures are admitted); and the two items flagged above for the round review.
- **The material to review:** `work/orchestration/goals/p-pump-basis/trail.md` — `### T-001 return — revised r2` and `### T-001 dispositions — proposed, revised r2`, read against `### Checkpoint C-001.r1`, `goal.md`, and the evidence refs both returns cite. Resume at `GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint.

### Checkpoint C-001.r2 — 2026-08-28

**Reviewer.** A fresh session, opened by the operator for this gate. It authored no part of round 1 and no part of the r2 revision, and it did not write `### Checkpoint C-001.r1` either — it carries neither the round agent's reasoning nor the first checkpoint's (`GOAL_RUNBOOK.md` § What "fresh" means). It read `goal.md`, `GOAL_RUNBOOK.md`, `.project/adr/004-finding-disposition.md@007d9488`, the whole trail, and every evidence ref both returns cite, at the cited lines. Arithmetic was re-derived from the committed channels rather than checked against the return's working.

**The reading reviewed.** `### T-001 return — revised r2, 2026-08-28`, outcome `COMPLETE`: two helium-primary HCPB data points at different grades supporting ~4–6 % of thermal power, ~130–195 MW held or ~130–200 MW computed at the baseline point; 1.0 MW not defensible; the low end of DI-008's 60–190 MW band unsupported and its upper half supported; the baseline power-balance effect with no verdict flip. Decisions D-1 and D-2 as revised, D-3 and D-4 carried.

**The dispositions reviewed.** `### T-001 dispositions — proposed, revised r2, 2026-08-28`: `#3` as `model fix`; `#5` as a new `declared seam` row with a concrete next reference; `#10` unchanged with no new row; nothing else touched.

**Verdict: passes. No required changes.** Submission 2 of 3; one revision remains unused (`goal.md` § Limits). Semantic follow-up work under this reading may execute, behind the reserved gates it names. Three carry-forwards for the round result are listed at the end; none of them blocks the follow-up task.

**The three required changes of C-001.r1 are applied, and each is right on re-derivation.**

- **RC1 — `#5`.** The sighting at `DISCOVERY_LOG.md@e891b23a:11` is the newest row under the id and its Home reads `unrouted`; the r1 reading of ADR-004 is correct and the revision accepts it on the right ground (an existing id, appended under, is not a minted id). I checked the constancy claim the row's next reference rests on rather than taking it from either entry. `p_tf` 0, `p_pf` 0 (`stellarator_plant.sysml@ba5c9945:508,626`), `p_tfcool` 15.0, `p_pfcool` 0 (`:530,629`), `p_trit` 10.0, `p_house` 4.0 (`:548,551`), `p_input`/`eta_pin` = 100 (`:486,500`). `mfe_cryo_plant.sysml@8f3b510c:47-52` on the bound cryo inputs returns `p_elec` = 0.8643516 MW, which is the value in `baseline_result.json@ffa5c54c` to every digit and moves with neither R nor a. I then ran the recipe end to end: it reproduces the oracle's `rec_frac` and `p_net` not only at the baseline (0.1514 / 915.08 paper, 0.1160 / 1345.40 at η 0.47) but at two off-baseline grid corners — R=4, a=0.8 gives 0.9424 / 8.3 and R=20, a=2.2 gives 0.0572 / 4529.2, against `oracle_scan.json@ffa5c54c` exactly. The next reference is stronger than the row claims: it is checked at the corners, not only at the design point.
- **RC2 — Moscato.** The figures are in `…wi031-item6-second-arm-values.md@ffa5c54c:43` as the revision states — 2101.7 MWth, 9 loops × 2 compressors, ≈131 MW (6.2 %), near-term 8-loop 83–94 MW (~4 %). Admitting them at a stated second-order grade, with the reason they cannot be re-derived at a source line, is the honest handling: the owner sees the rule and the exception to it, and the answer becomes a range. D-2 restated to "the low end of the band does not apply" is the claim the evidence carries.
- **RC3 — precision.** Carrying ~6 % rather than 6.279 % is right, and it changes the headline: ~195 MW held sits at the top of DI-008's band, not above it. The source's own qualification is now reported where the value is proposed — "Accurate design studies are on-going to reduce the pressure drop in the helium loops," with the 9 km → 3 km pipe lever, read at `…wppmicpr17-17709.md@0bf791d1:176`. Both observations are also taken: the denominator check is reported both ways rather than switched, and the transport warrant is now the source's own "the HCPB PHTS can be also be considered representative for the HCLL concept" at the same line, against Stellaris's HCLL blanket at `…output.md@e5a2cb23:1349` and in the model's own citation for `mn` at `stellarator_plant.sysml@ba5c9945:490`.

**The disputed statement: the revision is right and C-001.r1 was wrong. ACT1 is SCLL, ACT2 is DCLL.**

Adjudicated at the lines, and one line neither entry cited settles it outright. `…purl-1178069.md@aff7a2f9:157`: "ACT1 uses the self-cooled PbLi concept with SiC composite structures, whereas ACT2 uses a dual-cooled blanket with about half of the heat removed by He in RAFM steel structures. Notably, ACT2 is the first integrated power plant study by the ARIES Team using the DCLL blanket." The conclusions paragraph at `:290` agrees once the characterizations are matched to their configurations — advanced → SCLL, conservative → DCLL — and `:100` names ACT1 as advanced/advanced and ACT2 as conservative/conservative. So C-001.r1's parenthetical correction was inverted, and this entry records that so the inversion does not stand as fact in the trail. The revision's correction of its own first phrasing is also right: "self-cooled LiPb (DCLL)" conflated two concepts; DCLL is dual-coolant and SCLL is the self-cooled one.

Neither error touches any conclusion. Neither configuration has a helium-primary blanket, which is the whole of why ARIES-ACT does not answer this goal's question.

**Re-derivation, so the author does not repeat it and a later reader can see what the verdict rests on.**

- Cismondi at `…@0bf791d1:176`: fusion power 2037 MW, "the power deposited in the HCPB and WCLL of 2389 MW and 2045 MW respectively", "In case of helium the pumping power is ~150MW", helium at 80 bar. 150/2389 = 6.279 %, and 2389/2037 = 1.173.
- Moscato at `…@ffa5c54c:43`: 131/2101.7 = 6.23 %, and 83–94/2101.7 = 3.95–4.47 %. The revision's "~6 %" and "~4 %" are the honest renderings.
- The denominator. `p_alpha` = (3.52/17.58)·`p_fus` (`mfe_power_balance.sysml@8f3b510c:97`), so `p_th` − `eta_p·p_pump` = 1.17815 × `p_fus` and (`mn·p_neutron` + `p_alpha`) = 1.15999 × `p_fus`, against DEMO's 1.17280. Within 0.5 % and 1.1 %. Reporting both rather than picking one is the right call: the source paragraph does not say whether its 2389 MW includes an equivalent of the 50 MW heating term.
- The value. `p_fus` = 2748.0569 MW at baseline (`baseline_result.json@ffa5c54c`), `p_th` = 3238.12 MW. 4 % → 129.5 MW, 6 % → 194.3 MW. Solving the self-referential form gives 132.1 MW and 200.3 MW. The revision's ~130–195 held and ~130–200 computed are exact.
- The effect. Reconstructing the balance reproduces the study's own baseline in both arms exactly, so the reconstruction is checked. At 4 % and 6 % held: `rec_frac` 0.1514 → 0.2659 and 0.3219 in the η 0.333 arm, 0.1160 → 0.1971 and 0.2368 at η 0.47; `p_net` −11.8 % to −17.7 % and −7.4 % to −11.1 %. No verdict flips against the 0.5 threshold at baseline. All as stated.
- `points.csv@0d176a8c`: 3,792 rows; `p_fus` and `eta_th` non-empty at all of them; `p_net`, `rec_frac`, `q_eng`, `p_th`, `p_et` empty at all of them.
- Nine cost accounts take `p_th` directly in `mfe_plant.sysml@ba5c9945` (330, 338, 366, 405, 431, 505, 515, 526, 544). Exactly nine, as C-001.r1 also found.
- Citation liveness. Every path either return cites is at the sha it is cited at, checked with `git log -1` at this session's HEAD: `DISCOVERY_LOG.md` `e891b23a`, `KNOWLEDGE.md` and the research artifact `ffa5c54c`, the two design/model homes `ba5c9945` and `8f3b510c`, the three sources `0bf791d1` / `aff7a2f9` / `e5a2cb23`, `points.csv` `0d176a8c`, ADR-004 `007d9488`. None has moved.
- Scope and gates. The working tree carries no change under `models/`, `knowledge/`, `work/` or `exploration/`. `p_pump` is still 1.0 at `stellarator_plant.sysml@ba5c9945:502`, `DISCOVERY_LOG.md` is unchanged, no source is registered, no DI is amended, no work item is minted. The revision stayed inside the T-001 scope and behind every reserved gate, and it referred the shape question rather than choosing it.

**The dispositions.** `#3` as `model fix` is right and its revised finding — ~130–195× rather than the row's own "~100×" — is what the evidence now carries. `#5` as `declared seam` is the right kind: `upstream filing` would name an action outside this repository that this round cannot perform and did not perform, and ADR-004 asks for a kind plus "what changed or the concrete next reference", which the row supplies and which I verified above. `#10`'s Home is a real routing, so no row is owed. I checked the remaining `unrouted` rows: `#1` and `#2` are the availability and discount-rate findings, and although `oracle_scan.json` carries those scan points, this task reasoned only from the baseline row and its evidence does not bear on either. "Nothing else was touched" holds.

**Two observations, not required changes.**

- **ACT2's helium is not divertor-only, and the round should say so where it dismisses the band's floor.** The revision notes that DCLL is dual-coolant, but does not quantify it: `:157` says about half of ACT2's blanket heat is removed by helium, and `:197` gives He:LiPb thermal power ratios of 27:73 for ACT1 and 49:51 for ACT2. So the machine behind DI-008's low leg cools roughly half its blanket with helium and still reports total pumping around 1 % of thermal power. That is the strongest available counter to D-2, and it points the same way the round argues rather than against it — including ACT2 as partial evidence would pull the floor *down*, not up. D-2's conclusion stands; its stated ground is thinner than the evidence allows, and the owner ruling on DI-008 should see this fact beside it.
- **The 1 % versus 2 % tension the revision flagged is resolved at a line neither entry cited.** `:100`: "a total pumping power for He and LiPb of *1% of the total thermal power (*2% to 3% of thermal power in the He-cooled divertor)". So ~1 % is the whole-plant He+LiPb figure and the 2–3 % is the divertor loop against divertor thermal power. No correction is needed anywhere; the pair is consistent and the revision was right to propose none.

**Three carry-forwards for the round result and the fresh review, not for this gate.**

- The LCOE channel. `goal.md` § Invariants routes LCOE through `p_net`; `p_th` also reaches nine cost accounts directly. The round traced this rather than widening the channel, and I confirmed the count. Where a correction to a goal-level statement lands is the round review's call.
- `goal.md` § Grounding evidence says of Moscato "it is the one not in the repository". The revision is right that this is imprecise in the way RC2 corrected: the PDF is absent, the figures are present in the artifact cited in the same bullet. `goal.md` is amended by the operator in its own § Amendments; a round does not edit it, and this checkpoint does not either.
- The C-001.r1 inversion above. It is corrected here and nowhere else, because no entry is edited in place.

**What this gate does not decide.** Whether the value lands, in what shape, and at what grade Moscato's figures are admitted are reserved gates 2, 3 and 4, referred to the owner by D-3 and D-4 and untouched by this verdict. The central conclusion — 1.0 MW is not defensible for a helium-primary loop at this plant scale — is confirmed, and it survives at any precision, at either end of the range, with or without the Moscato leg, and even against ARIES-ACT's ~1 %.

### Round 1 result — 2026-08-28

**Intent: met.** The strategy declared it would ask the repository first, derive a value on a stated basis, and land nothing, on the ground that `goal.md` § Answered when calls a trail-only answer complete. That is what happened, and the answer it produced is written and sourced in both directions the contract allows: **1.0 MW is not defensible for a helium-primary loop at this plant scale, and the repository supports ~4–6 % of thermal power — ~130–195 MW held, ~130–200 MW computed — at the baseline point.**

Two of the strategy's declared fields were not reached, and the reading "intent unmet" is available to the fresh review on them. The **model increment did not land** — nothing under `models/`, `knowledge/` or `work/` moved this round — though the strategy said in advance that this round proposes it and does not land it (reserved gate 3). The **intended study question was not asked**: no study ran, no pin was promoted. Neither is needed for § Answered when, which asks for a written sourced answer, not for a measured consequence. The counter-reading is recorded so the review can take it rather than have to find it.

**Task sequence.** One task, no retries, two checkpoint submissions.

1. `T-001` — what value, if any, do repository-native sources support for `stellarator_09`'s primary-coolant pumping power, and on what basis? Returned `COMPLETE` 2026-08-28.
2. `C-001.r1` — verdict `REVISE`: three required changes and two observations.
3. `T-001 return — revised r2` — all three required changes applied, both observations taken, one of the checkpoint's own passing statements disputed with the evidence.
4. `C-001.r2` — verdict `PASS`, no required changes, one revision of two left unused. It adjudicated the dispute in the revision's favour: ACT1 is SCLL, ACT2 is DCLL, and `C-001.r1`'s parenthetical correction was inverted. Recorded there and nowhere else, because no entry is edited in place.

No pin was promoted and no study was committed, so the round stayed well inside its bound (`GOAL_RUNBOOK.md` § Opening and closing a round). No retry was taken, so the retry cap was never engaged.

**Last semantic outcome.** `T-001` → `COMPLETE`, with its reading and dispositions passed at `C-001.r2`.

**Stop reason, derived.** Read off the last semantic outcome plus `goal.md` § Limits, not maintained as a second status.

- Limits: retry cap 2 — zero retries taken, not approached. Checkpoint revision cap 2 — one revision used, cap not hit. Round limit 6 — this is round 1. Tasks per round — none declared. **No declared limit fired**, so trigger 5 is not the reason.
- The last semantic outcome is `COMPLETE`, not a blocker: trigger 2 does not apply. The channel was traced, not widened — `p_pump` still reaches the verdicts through the same two power-balance terms — so trigger 3 does not apply.
- **Trigger 4 was tested and does not apply.** The round met three reserved gates (2, 3, 4) and referred all three. None of them *stopped* the round: `T-001`'s scope excluded every gated action before the work began, so the task reached its objective and returned `COMPLETE` rather than `OWNER_GATE`. An unresolved gate that the round is waiting on is what trigger 4 names, and this round is not waiting on one — the answer is complete without them, because § Answered when says a trail-only answer is complete and puts any model change behind the owner's gate by design.
- `goal.md` § Answered when asks for "a written, sourced answer either way — a better number, or 'keep 1.0 MW, here's why'". A better number is on the record, written, sourced, with the admissibility of each source stated and the weaker one graded. The contract explicitly does not fix the answer's shape, and it explicitly does not require a model change.
- Derived stop reason: **close trigger 6 — the goal answered.**

**This closes the round, not the goal.** `goal.md` § Close rule is owner-held: the fresh review hands the owner a recommendation once § Answered when is met, and the owner's ruling closes the goal. This result carries the recommendation; it does not close anything.

**Evidence refs.**

- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` — two joined rows appended 2026-08-28, under `20260821-power-cycle-ab#3` and `#5`. `uv run python -m pytest tests/study/test_records.py` — 7 passed after the append, so the multi-row join under one id holds.
- `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/scipub-wp-content-uploads-eurofusion-wppmicpr17-17709.md@0bf791d1:176` — Cismondi 2017: 2037 MW fusion, 2389 MW deposited in the HCPB, "~150MW" helium pumping, helium at 80 bar, the HCPB-representative-for-HCLL statement, and the statement that the figure is expected to fall.
- `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md@ffa5c54c:43` — Moscato 2018's figures, at second-order grade: the source PDF is not ingested.
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1178069.md@aff7a2f9:100,157,175,197,290` — ARIES-ACT. Read at all five lines this round, three of them for the first time at round close (see the DI-008 note below).
- `knowledge/KNOWLEDGE.md@ffa5c54c` DI-007, DI-008.
- `models/library/analyses/mfe_power_balance.sysml@8f3b510c:119,135`; `models/library/analyses/mfe_cryo_plant.sysml@8f3b510c:47-52`; `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:490,502,508,530,548,551,567-600,626,629`; `models/designs/generic_mfe/mfe_plant.sysml@ba5c9945:305,330,338,366,405,431,505,515,526,544`.
- `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/results/baseline_result.json@ffa5c54c`, `oracle_scan.json@ffa5c54c`, `points.csv@0d176a8c`; `record.md@881d4448` § 4, § 13, § 15, § 17.
- `.project/adr/004-finding-disposition.md@007d9488`.
- **Cited-ref walk at round close.** Every ref above stands at the digest it is cited at, checked with `git log -1` at this session's HEAD. The one path that moved this round — `DISCOVERY_LOG.md` — moved by this round's own ADR-004 duty, after the checkpoint passed. No external mutation; no task is voided.

**One thing found at round close that was not in the passed reading.** `C-001.r2` observed that ARIES-ACT's plant-level pumping fraction sits at a line neither prior entry had cited. I read it rather than inherit it: `…purl-1178069.md@aff7a2f9:100` says "a total pumping power for He and LiPb of ~1% of the total thermal power (~2% to 3% of thermal power **in the He-cooled divertor**)". So the ~2–3 % is measured against *divertor* thermal power, not plant thermal power, and the plant-level ARIES-ACT figure is ~1 %. **DI-008's stated 2 % floor is a divertor-relative figure read as a plant-relative one.** That also settles the 60–190 vs 30–190 discrepancy `goal.md` § Grounding evidence logged and left open: the research file's 30 MW end is the correctly-read plant-level figure and DI-008's 60 MW end is not. It strengthens D-2 rather than changing it, and it is new since the checkpoint passed, so the fresh review should weigh it as unreviewed. Amending DI-008 is reserved gate 4 and this round does not.

I also read `:157` and `:197`, which the checkpoint cited: ACT1 is self-cooled PbLi with SiC, ACT2 is dual-cooled with "about half of the heat removed by He", at He:LiPb thermal power ratios of 27:73 and 49:51. So ARIES-ACT is not irrelevant to a helium question — it is a *partially* helium-cooled machine reporting ~1 % at plant level, and that is the strongest thing standing against the ~4–6 % this round derived. It is stated here beside the conclusion rather than left out of it.

**Proposed learning delta.** Three claims, for the fresh review to accept, correct, or reject. Not appended to `learnings.md` by this session — that write belongs to the review (`GOAL_RUNBOOK.md` § The five surfaces).

- **Proposed L-001 — the repository's helium-cooling evidence spans ~1–6 % of thermal power, and the spread is design optimization, not measurement uncertainty; the helium-*primary-blanket* subset is ~4–6 %.** *Evidence:* Cismondi ~150 MW / 2389 MW HCPB at 80 bar (`…@0bf791d1:176`); Moscato ≈131 MW / 2101.7 MWth and a near-term 8-loop design at 83–94 MW, at second-order grade (`…@ffa5c54c:43`); ARIES-ACT ~1 % plant-level for a 49:51 He:LiPb blanket (`…@aff7a2f9:100,197`). The EU DEMO figures are a preliminary unoptimized layout whose own authors expect them to fall (9 km of pipe → ~3 km with larger diameters); ARIES-ACT is an optimized advanced study with a high-temperature Brayton cycle. *Scope:* helium-cooled blankets at DEMO/Stellaris scale; the ~4–6 % subset holds for HCPB and, on the source's own representativeness statement, HCLL. Not established for any other coolant or for a machine whose helium share is small. *Implication:* a re-based value carries a factor-of-two range that no further reading of these three sources will close; closing it needs a loop design, which is reserved gate 5 and a different goal. A number quoted to better than one significant figure from this evidence is false precision — a lesson this round had to be told twice before it took.
- **Proposed L-002 — a missing power-balance operand column is recoverable post hoc when the record commits the driving channel and every other term of the sum is bound.** *Evidence:* the reconstruction from `points.csv@0d176a8c`'s `p_fus` and `eta_th` columns plus the design's bound inputs reproduces `oracle_scan.json@ffa5c54c` exactly at the baseline (0.1514 / 915.1) and at both grid corners (0.9424 / 8.3 and 0.0572 / 4529.2). *Scope:* this package as configured. It fails the moment any recirculating term becomes geometry-dependent — `p_cryo` is recoverable only because every cryo input is bound (`mfe_cryo_plant.sysml@8f3b510c:47-52`). *Implication:* finding `#5` is a cost, not a wall, for this package: a later round can locate a `rec_frac` fence from committed evidence without a pin. It cannot locate an LCOE fence that way, which is L-003.
- **Proposed L-003 — `p_th` is a cost driver as well as a power-balance quantity, so a power-balance input reaches LCOE by two paths, not one.** *Evidence:* nine cost accounts take `p_th` directly in `mfe_plant.sysml@ba5c9945` (lines 330, 338, 366, 405, 431, 505, 515, 526, 544) — blanket, shield, divertor, heat rejection, buildings, coolant, aux cooling, waste, and I&C. `p_pump` enters `p_th` through `eta_p·p_pump` (`mfe_power_balance.sysml@8f3b510c:119`). *Scope:* the MFE plant spine as built. *Implication:* `goal.md` § Invariants routes LCOE through `p_net`, which is the larger path but not the only one, so an LCOE effect cannot be estimated from `p_net` alone and needs a package run. Any future goal-level channel statement about a power-balance input must name both paths.

**Finding dispositions.** Two rows touched and dispositioned, both appended 2026-08-28 under their existing ids. Neither returns as `unrouted` (ADR-004).

- `20260821-power-cycle-ab#3` — `model fix`, routed to goal `p-pump-basis` round 1 task T-001, status "routed, not yet answered". The finding is confirmed and sharpened: the row's own "~100×" understates it; the factor is ~130–195×. Nothing landed, no work item minted — reserved gates 2, 3 and 4.
- `20260821-power-cycle-ab#5` — `declared seam`. The evidence-layer gap stays with sysml-codegen / teax outside this repository; the concrete next reference is the reconstruction recipe, verified at the baseline and both grid corners. `upstream filing` was considered and rejected: it would name an action outside this repository that this round cannot perform and did not.

Rows read but not touched, with the reasoning recorded so the review can disagree:

- `20260821-power-cycle-ab#10` — its Home is "runbook step 9; applied as executor practice in study 1", a real routing, not `unrouted`. Both checkpoints concurred. No row owed.
- `20260821-power-cycle-ab#1` and `#2` — still `unrouted`. This task reasoned only from the baseline row of the oracle scan; its evidence bears on neither the availability nor the discount-rate finding. `C-001.r2` checked this independently and agreed.

**Recommendation to the owner.** `goal.md` § Close rule: the fresh review hands this to the owner, and the owner's ruling closes the goal. Three rulings are asked for, in the order they depend on each other.

**Ruling 1 — DI-008 (reserved gate 4). Recommended: correct its floor and its Stellaris band; do not narrow its 2–6 % basis.**

- Its **2 % floor is a misread**: `…@aff7a2f9:100` measures ~2–3 % against divertor thermal power, and the plant-level figure in the same sentence is ~1 %. Recommend the DI say so, which also settles the 60–190 vs 30–190 discrepancy `goal.md` logged, in the research file's favour.
- Its **60–190 MW Stellaris band** was computed against the paper's printed ~3150 MWth. Against the model's computed `p_th` at the baseline geometry the same fractions give ~65–195 MW, and the helium-primary-blanket subset alone gives ~130–195 MW.
- Do **not** narrow the basis to 4–6 %. ARIES-ACT's ~1 % is a real plant-level figure for a machine that removes about half its blanket heat with helium. It is not a helium-primary-blanket figure, but it is not nothing, and a basis that excluded it would hide the strongest evidence against this round's own number.

**Ruling 2 — the answer's shape (reserved gate 2). Recommended: `p_pump` stays a held, settable input, re-based.**

Three reasons, and one that cuts the other way, stated.

- The two forms differ by ~3 % at the design point (129.5 vs 132.1 MW at 4 %; 194.3 vs 200.3 MW at 6 %) — far inside the ~one-significant-figure precision the sources carry. Internalizing buys no accuracy.
- It costs a lever. Retiring `p_pump` as a settable input under `STUDY_POLICY.md@ad2fb4ea` § 2 rule 3 removes an axis from two committed studies and changes what is comparable across rounds.
- The fraction form asserts that pumping power scales linearly with thermal power across a swept (R, a) window. No source in the repository establishes that; Cismondi and Moscato each give one plant at one design point. DI-007's standing instruction is exactly this — a dependency the upstream model does not have must be declared, not assumed.
- **Against:** DI-008's basis *is* a fraction, and a held scalar is only right at the geometry it was derived at. A study that sweeps R and a with a held scalar is carrying a value that is wrong away from the baseline in a known direction. This is the real argument for internalizing and the owner should weigh it; the recommendation stands because the linearity it needs is unsourced, not because the objection is weak. Precedent runs the same way — `cryo-volume-basis` closed on the owner ruling the analogous value stays held, with a reversal condition.

**Ruling 3 — the value and the sources (reserved gates 3 and 4). Recommended: land ~195 MW, register Cismondi, ingest Moscato.**

- **Land 6 % of `p_th` at the baseline geometry, ≈195 MW**, in both homes of the twin, through a work item minted under the MFE Cost Modeling epic. Reason: it is the only figure re-derivable at a line in an ingested source, and it errs in the direction the current model is optimistic. Record the ~130 MW near-term figure as a documented lower bound rather than averaging to a number no source states — the pattern `f_uplift_cryo` already uses in this design (`stellarator_plant.sysml@ba5c9945`, WI-024 D6).
- **Register Cismondi in `SOURCE_INDEX.md`** through the WI-031 hand pattern. The answer's authority now rests on it and it is unregistered.
- **Ingest the Moscato PDF.** It is the only helium-primary pumping-system *design* in the set and the only source that would convert the range's lower half from second-order to first-order grade.
- **A "keep 1.0 MW" ruling is not available on this evidence.** `goal.md` § Answered when makes a reasoned "keep it" a first-class outcome, and this round tested it: 1.0 MW is ~0.03 % of thermal power against a sourced ~1–6 %, and it fails at every end of the range including ARIES-ACT's. The honest "keep it held" ruling here is Ruling 2 — keep the *form*, change the number.

**What round 2 would face, if the owner opens the gates.** Stated as a constraint, not as a plan. Landing the value makes the committed package stale, and a study measuring where the `recirc_ok` fence moves needs a regenerated, verified, pinned package. The `integrate` seam is unrepaired and has no documented hand pattern anywhere in the repository, so that is a `PREREQUISITE` return to the operator, per `goal.md` § Grounding evidence and `GOAL_RUNBOOK.md` § The native seams. The `rec_frac` half of the question could be answered without a pin by L-002's recipe; the LCOE half could not, by L-003.

**Two items for the fresh review, carried forward from `C-001.r2` and not resolved here.**

- **The LCOE channel.** `goal.md` § Invariants routes LCOE through `p_net`; `p_th` also reaches nine cost accounts directly. The round traced this rather than widening the channel, and both checkpoints confirmed the count. Its substance is proposed L-003; whether `goal.md` § Invariants also needs an operator amendment is the review's call, not this round's — a round does not edit `goal.md`.
- **`goal.md` § Grounding evidence on Moscato.** It says "it is the one not in the repository". The source PDF is absent; the figures are present in the artifact cited in the same bullet. An operator amendment in `goal.md` § Amendments, if the review agrees.

**Round 1 is closed. It is unreviewed.** The round agent's last act is the round result, and this session wrote the task, both returns, and this result, so it cannot review the round (`GOAL_RUNBOOK.md` § What "fresh" means).

### Stop — 2026-08-28

Third stop of this date; it follows the round 1 result above.

- **Kind:** `handoff`.
- **What is true on disk:** round 1 is closed — strategy revision, `T-001` (scope, start, return), `C-001.r1`, the r2 revision and its dispositions, `C-001.r2`, and the result above. Two joined disposition rows are appended to `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` under `20260821-power-cycle-ab#3` and `#5`; `tests/study/test_records.py` passes 7. That append is the round's only write outside this goal directory. `models/`, `knowledge/` and `work/` are unchanged: `p_pump` is still 1.0 MW at `stellarator_plant.sysml@ba5c9945:502` in both homes of the twin, no source is registered, no DI is amended, no work item is minted. `learnings.md` is still the unfilled template — the result proposes three claims and does not append them. Nothing is committed; the operator owns commits.
- **What the owner must see:** a fresh session is needed to review round 1. Separately, the goal is answered on `goal.md` § Answered when's terms and its close is owner-held — the result carries three recommended rulings (DI-008's floor and band; the answer's shape; the value and the two sources), each with the argument against it stated. One item in the result is newer than the passing checkpoint and is unreviewed: the ARIES-ACT plant-level reading at `…purl-1178069.md@aff7a2f9:100` that makes DI-008's 2 % floor a divertor-relative figure.
- **The material to review:** this goal directory; the two newest rows of `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`; the evidence refs listed in the result. Resume at `GOAL_RUNBOOK.md` § The fresh review.

### Round 1 review — 2026-08-28

**Reviewer.** A fresh session, opened by the operator after the round-close handoff. It authored no part of round 1 — not the strategy revision, not `T-001`'s scope, start, return or revision, not either checkpoint, not the result — and carries none of those sessions' reasoning (`GOAL_RUNBOOK.md` § What "fresh" means). It read `goal.md`, `GOAL_RUNBOOK.md`, the whole trail, `.project/adr/004-finding-disposition.md@007d9488`, the discovery log, and every evidence ref the round cites, at the cited lines. All arithmetic below was recomputed from the committed channels and the model's own bound inputs, not checked against the trail's working.

**Verdict: `FINDINGS`.** Two findings, both stated below. **Neither reopens the round and neither touches its conclusion.** The round's central answer — 1.0 MW is not defensible for a helium-primary loop at this plant scale, and the repository supports ~4–6 % of thermal power, ~130–195 MW held at the baseline point — is confirmed at every step I could recompute, and `goal.md` § Answered when is met. The findings are a citation that does not resolve at the line it names, and a recommendation to the owner whose reasoning runs against a conclusion the same round drew. The close recommendation follows this entry, because `goal.md` § Close rule triggers on § Answered when being met, not on the review's verdict; `GOAL_RUNBOOK.md` § The fresh review covers only the `PASS` case, and I read its silence as silence rather than as a bar.

**Native evidence, by citation.** Every ref the round cites resolves at the digest it is cited at, checked with `git log -1` at this session's HEAD: `DISCOVERY_LOG.md` `e891b23a` before the round's own append, `KNOWLEDGE.md` and the research artifact `ffa5c54c`, `stellarator_plant.sysml` and `mfe_plant.sysml` `ba5c9945`, `mfe_power_balance.sysml` and `mfe_cryo_plant.sysml` `8f3b510c`, the three sources `0bf791d1` / `aff7a2f9` / `e5a2cb23`, `points.csv` `0d176a8c`, ADR-004 `007d9488`. One line reference inside a live file is wrong; that is Finding 1.

What I recomputed, independently:

- **The baseline balance.** From `p_fus` = 2748.0569 (`baseline_result.json@ffa5c54c`) and the design's bound inputs, `p_th` = 3238.12 MW, and the balance returns `rec_frac` 0.15139 / `p_net` 915.1 at η 0.333 and 0.11596 / 1345.4 at η 0.47 — the study's own reported values (`oracle_scan.json@ffa5c54c`). The reconstruction is checked, not asserted.
- **The value.** 4 % → 129.5 MW held, 132.1 computed; 6 % → 194.3 held, 200.3 computed. The round's "~130–195 held, ~130–200 computed" is exact. Cismondi's 150/2389 = 6.279 %, and carrying it at ~6 % rather than four figures is right.
- **The effect.** `rec_frac` 0.1514 → 0.2659 (4 %) and 0.3219 (6 %) at η 0.333; 0.1160 → 0.1971 and 0.2368 at η 0.47. `p_net` −11.8 % / −17.7 % and −7.4 % / −11.1 %. No verdict flips at baseline against the 0.5 threshold. All as stated.
- **The denominator.** (`p_th` − `eta_p·p_pump`)/`p_fus` = 1.17815 including the 50 MW heating term, 1.15995 excluding it, against DEMO's 2389/2037 = 1.17280. Both within 1.2 %. Reporting both rather than switching is the right call and D-1 stands on either.
- **The `#5` recipe, at the corners.** I ran it from `points.csv@0d176a8c` alone: R=4/a=0.8 paper arm returns `rec_frac` 0.9424 / `p_net` 8.3, and R=20/a=2.2 returns 0.0572 / 4529.2, against `oracle_scan.json` exactly. `p_fus` and `eta_th` are non-empty at all 3,792 rows; `p_net`, `rec_frac`, `q_eng`, `p_th`, `p_et` are empty at all of them. The disposition row's next reference is real and I confirmed it end to end.
- **Nine cost accounts** take `p_th` directly in `mfe_plant.sysml@ba5c9945` — 330, 338, 366, 405, 431, 505, 515, 526, 544. Exactly nine; line 430 takes `p_the` and is correctly not counted.
- **Scope and gates on disk.** The working tree carries no change under `models/`, `knowledge/`, `work/` or `exploration/`. `p_pump` is still 1.0 MW at `stellarator_plant.sysml:502` and the exploration twin is byte-identical to the canonical home. Cismondi and Moscato are still absent from `SOURCE_INDEX.md`; no DI is amended; no work item is minted. `tests/study/test_records.py` passes 7 after the round's append.

**Goal and strategy fidelity: pass.** The strategy declared it would ask the repository first, read each figure at its line, derive a value on a stated basis, and land nothing. That is what happened. Its three abandonment conditions were tested honestly: an admissible helium-primary datum did survive reading; the shape question was referred rather than chosen, which is what the second condition asks for; and the shift proved large, not grid-resolution-small, so the third did not fire. The channel was traced, not widened — `p_pump` still reaches the verdicts through the same two power-balance terms, and the nine-account path the round found is a property of `p_th` that already existed, not a new coupling the round introduced.

**Task scope: pass.** `T-001`'s scope excluded every gated action before the work started, and none was performed. The one write outside the goal directory is the two disposition rows in `DISCOVERY_LOG.md`, which `GOAL_RUNBOOK.md` § The discovery log names as the goal layer's own pen's write and ADR-004 makes mandatory. I checked it against `goal.md` § Reserved gates: the general gate covers model and knowledge mutations landing in `work/`, `models/` or `knowledge/`, and a disposition row under `exploration/` is neither. It is authorized.

**Retry classification: pass, vacuously.** No retry was taken and no `MECHANICAL_FAILURE` was claimed. The checkpoint sequence is `r1` fail → `r2` pass, one revision of two used, each submission a new `rK` entry with nothing amended in place. The r2 entry disputing one of r1's own passing statements, and r2 adjudicating that dispute against r1 at a line neither had cited, is the checkpoint loop working as designed.

**Every touched discovery row: accounted for.** Two appended, two read-but-untouched with reasoning, one concurred — and I checked the rest myself rather than take "nothing else was touched" on trust.

- `#3` — `model fix`, appended. Right kind. Its revised finding, ~130–195× rather than the sighting row's "~100×", is what the arithmetic carries.
- `#5` — `declared seam`, appended. Its Home was literally `unrouted`, so ADR-004's obligation fired and the round's first reading (touched-but-already-disposed) was wrong; the r2 acceptance is on the right ground, since appending under an existing id is not minting one (ADR-004 line 20, line 46). `declared seam` over `upstream filing` is defensible: the fix is outside this repository and the round neither could nor did file it. **Carry forward:** the upstream fix itself is still unfiled, and `declared seam` records that honestly rather than resolving it.
- `#10` — concurred, no row owed. Its Home is "runbook step 9 (executor practice in study 1)", a real routing. Correct.
- `#1` and `#2` — read, untouched, reasoning recorded. Confirmed: availability and discount rate reach LCOE, not the power balance, and nothing in this task's evidence bears on either.
- `#4`, `#6`, `#7`, `#8`, `#9`, `#11`, and the unrouted rows of `20260823-magnet-technology-ab` (`#3`, `#4`) — I checked each against the round's evidence. None is touched. One note: `#7` ("the record carries verdicts but not, as data, the bound values they were judged against") sits close to what this round's reconstruction actually did. It carries a real Home, so no obligation fires either way, but "no other row bears on this task's evidence" is drawn slightly wider than I would draw it.

**The round-close finding, weighed at the lines.** `C-001.r2` passed before this one existed, so nothing has reviewed it. I read `…purl-1178069.md@aff7a2f9:100` myself: "a total pumping power for He and LiPb of ~1% of the total thermal power (~2% to 3% of thermal power in the He-cooled divertor)". **The round's reading is correct and I confirm it.** Two independent grounds:

- *Internal consistency.* The divertor helium loop is a subset of the He+LiPb total. A subset cannot be 2–3 % of plant thermal power while the whole is ~1 % of it. The parenthetical only parses if its denominator is divertor thermal power.
- *Arithmetic.* `:175` gives 12 MW of divertor helium for ACT2 at `Ppump/Pthermal` ≈ 2 %. ACT2 makes 1000 MWe net at η_th 0.45, so its thermal power is of order 2500 MWth and 12 MW is ~0.5 % of it, not 2 %. Against a divertor thermal power of ~600 MW, 2 % lands exactly.

So DI-008's stated 2 % floor is a divertor-relative figure read as a plant-relative one, and the 60 MW end of its Stellaris band inherits that error. This also settles the 60–190 vs 30–190 discrepancy `goal.md` § Grounding evidence logged and left open, in the research file's favour: 1 % of the paper's ~3150 MWth is ~31 MW. Amending DI-008 is reserved gate 4 and the round correctly did not.

**The result's own counter-reading: rejected, with one point of it kept.** The result offers "intent unmet" on two unreached strategy fields.

- *The model increment.* Reject. The strategy said in advance that this round proposes the increment and does not land it, because reserved gate 3 holds it. Not landing it is fidelity to the declared strategy, not a shortfall against it.
- *The study question.* Reject as an intent verdict, but the observation underneath it is real. No study ran and no pin was promoted, and that field genuinely went unreached. But it was unreachable inside this round by the goal's own construction: measuring where the `recirc_ok` fence moves needs the re-based value in the package, which needs gate 3 (owner-held) and then the `integrate` seam, which is unrepaired and which `GOAL_RUNBOOK.md` § The native seams makes a `PREREQUISITE` return by definition. A round is not unmet for declining to do what its goal forbids it. The runbook is explicit that a round may close with neither a pin nor a study.
- *What I keep from it.* The strategy should not have declared an intended study question it already knew it could not reach under gates that were written down before the round opened. That is a strategy-writing note for round 2, not an intent verdict, and it is in the constraints below.

**Intent: met**, as the result claims.

**The derived stop reason: trigger 6 stands.** I tested it against all six and against `goal.md` § Limits.

- Triggers 1 and 2 do not apply: no study reading exists, and the last semantic outcome is `COMPLETE`, not a blocker. The strategy's premise held.
- Trigger 3 does not apply: the channel was traced, not widened, and I confirmed `p_pump` still reaches the verdicts through the same two terms.
- Trigger 5 does not apply: zero retries against a cap of 2, one checkpoint revision against a cap of 2, round 1 of 6. No limit fired.
- **Trigger 4 is the close call, and the round's reasoning survives it.** Three reserved gates were met and all three were referred. But trigger 4 names a gate the round is *waiting on*, and this round is not waiting: `goal.md` § Answered when says in the owner's own sentence that a written sourced answer is the answer and that any model change comes back to the owner first. The gates are the contract working, not the round stalling. Had the round needed a gate opened to produce its answer, this would be trigger 4; it did not.
- **Trigger 6 — the goal answered.** § Answered when asks for a written, sourced answer either way. A better number is on the record, sourced, with each source's admissibility stated and the weaker one graded second-order. The round also tested the other direction and found it unavailable on the evidence, which is the honest form of that check. Correctly derived.

**Finding 1 — a load-bearing citation does not resolve at the line it names.** The r2 return and the result both cite `…wppmicpr17-17709.md@0bf791d1:176` for the source's HCPB-representative-for-HCLL statement and for the 80 bar helium pressure. Both are at **`:174`**, not `:176`. Line 176 carries the pumping figure, the "accurate design studies are on-going" qualification and the 9 km → 3 km pipe lever, all correctly attributed. This matters more than a typo because the representativeness statement is the *warrant* for transporting an HCPB ratio to Stellaris's HCLL blanket — it replaced the pressure match as the argument, on `C-001.r1`'s second observation, and it is the load-bearing sentence for the whole transport. Both checkpoints repeated the `:176` attribution without checking it. The statement is real, I read it, and the conclusion is unaffected; the citation should read `:174,176`. Correction only — no rework.

**Finding 2 — Ruling 3 lands the top of the range while the round's own reading says that figure is expected to fall, and does not say which principle governs.** The r2 return concluded that Cismondi's ~150 MW is "a preliminary figure for one unoptimized layout that its own authors expect to fall", consistent with Moscato's near-term ~4 %, and stated plainly that "the low end of the ~4–6 % range is the direction of travel, not an outlier". Ruling 3 then recommends landing ~195 MW — the 6 % end — with ~130 MW recorded as a documented lower bound. Its two reasons are real: Cismondi is the only figure re-derivable at a line in an ingested source, and it errs against the model's current optimism. But the round never engages its own contrary conclusion, and the precedent it cites points the other way: `f_uplift_cryo` (`stellarator_plant.sysml@ba5c9945:590`) lands the bound its evidence can defend and *parameterizes* the unquantified remainder so the owner can raise it — it does not pick an end of a range and footnote the other. The owner is being handed a number without being told whether traceability-first or currency-first governs the choice. **The recommendation is not withdrawn** — it is defensible — but the owner should see the tension stated, and it is stated in the recommendation below.

**The learning delta: all three accepted, one corrected.** Appended to `learnings.md` by this review and nowhere else.

- **L-001 — accepted with correction.** The proposed claim attributed the whole ~1–6 % spread to "design optimization, not measurement uncertainty". That is right for the 4 % versus 6 % gap, which is two layouts of the same EU DEMO HCPB loop. It is wrong for the 1 % leg: ARIES-ACT differs from EU DEMO in blanket architecture — dual-cooled PbLi with roughly half the blanket heat carried by helium (`…@aff7a2f9:157,197`) — not in how well the same loop was optimized. Rewritten to separate the two axes, and the divertor-relative reading of DI-008's floor folded into it as the fact the run now knows. I also dropped the proposed entry's closing aside about the round having to be told twice; the template asks for one claim, and self-assessment is not one.
- **L-002 — accepted as proposed.** I reproduced it independently at the baseline and at both grid corners from `points.csv` alone. Its scope caveat is the right one and is load-bearing: the recipe holds only because every other recirculating term is bound.
- **L-003 — accepted, tightened.** Nine accounts confirmed exactly. Stated as the claim rather than as a note about `goal.md`.

**Constraints carried into round 2, if the owner opens it.** Stated as constraints, not as a plan; the review never resumes the closed round.

- Landing a value makes the committed package stale. A study measuring the fence needs a regenerated, verified, pinned package, and the `integrate` seam is unrepaired with no documented hand pattern. That is a `PREREQUISITE` return to the operator, not a task to improvise.
- A strategy that declares an intended study question must first check that its own goal's gates leave it reachable inside one round. This one did not, which is the honest core of the result's counter-reading.
- The `rec_frac` half of any fence question is answerable without a pin, by L-002's recipe. The LCOE half is not, by L-003.
- The upstream evidence-layer fix behind `#5` remains unfiled. `declared seam` records that; it does not discharge it.

**Two operator amendments to `goal.md`, recommended.** A round does not edit `goal.md` and neither does this review; both go in its own § Amendments.

- § Invariants routes LCOE through `p_net`. It should name the second path: `p_th` reaches nine cost accounts directly, so a power-balance input moves capital as well as net power. This is L-003, and it is a correction to a goal-level statement rather than a widening of the channel.
- § Grounding evidence says of Moscato "it is the one not in the repository". The source PDF is absent; its figures are present in the approved research artifact cited in the same bullet. The bullet already says "Open PDF, not ingested" two lines up, so this is imprecision rather than error, but it is the imprecision that produced the round's first overstated claim.

**Recommendation to the owner.** `goal.md` § Close rule: this review recommends, the owner's ruling closes. § Answered when is met in the owner's own terms — a written, sourced answer, with the model change held behind the owner's gate. **I recommend closing goal `p-pump-basis` as answered**, on the three rulings the result asks for, which I endorse with one amendment.

- **Ruling 1 — DI-008 (gate 4). Endorsed as written.** Correct the 2 % floor: it is a divertor-relative figure, confirmed above at `:100` and `:175` on two independent grounds, and correcting it settles the 60–190 vs 30–190 discrepancy in the research file's favour. Restate the Stellaris band against the model's computed `p_th`. Do not narrow the basis to 4–6 % — ARIES-ACT's ~1 % is a real plant-level figure for a machine that removes about half its blanket heat with helium, and it is the strongest evidence standing against this round's own number.
- **Ruling 2 — the answer's shape (gate 2). Endorsed.** `p_pump` stays a held, settable input, re-based. The two forms differ by ~3 % at the design point, far inside one significant figure; internalizing costs a lever in two committed studies; and the fraction form asserts a linearity across swept (R, a) that no source in the repository establishes, which is exactly what DI-007's standing instruction bars. The counter-argument the round states against itself — a held scalar is only right at the geometry it was derived at — is real and the owner should weigh it, but it argues for re-deriving the scalar when the design point moves, not for asserting an unsourced scaling law.
- **Ruling 3 — the value and the sources (gates 3 and 4). Endorsed with the choice put back to the owner.** Register Cismondi and ingest Moscato through the WI-031 hand pattern: the answer's authority rests on an unregistered source, and Moscato is the only helium-primary pumping-system *design* in the set and the only thing that would lift the range's lower half to first-order grade. On the number itself, the owner is choosing between two defensible values, and Finding 2 is that the round did not say so. **~195 MW** is the figure re-derivable at a line in an ingested source and errs against the model's known optimism. **~130 MW** is the near-term optimized design and the direction the round's own evidence says the field is travelling. My recommendation is to land ~195 MW and record ~130 MW as the documented lower bound, as the result proposes — the higher value is the one whose provenance survives at the standard this goal applied to everything else, and the model's error today is optimism — but the owner should make that call knowingly rather than inherit it, and re-visit it when Moscato is ingested at first-order grade.
- **"Keep 1.0 MW" is not available.** The round tested it, as § Answered when requires. 1.0 MW is ~0.03 % of thermal power against a sourced 1–6 %, and it fails at every end of the range including ARIES-ACT's plant-level ~1 %. That is a `BOUNDED_NEGATIVE` on the first half of § Question, and it is what makes the second half live.

**Round 1 is reviewed. The goal is not closed** — that is the owner's ruling, and nothing here closes it.

### Amendment 2026-08-28 — amends `### Round 1 review — 2026-08-28`

The review entry names one correction made to proposed L-001 on accept (the attribution of the ~1–6 % spread to optimization). A second, smaller one was made and not named, so it is recorded here rather than left as an unexplained difference between the proposed delta and the appended one.

Proposed L-001's implication read "a re-based value carries a **factor-of-two** range". The range it refers to is ~130–195 MW, which is a factor of 1.5. The appended L-001 says factor-of-1.5. Arithmetic only; the claim's substance is unchanged.

## Goal close — 2026-08-28

### Owner ruling — 2026-08-28

All three rulings the round 1 result asked for are ruled, on the review's recommendation. `[OWNER 2026-08-28]`

- **Ruling 1 — DI-008 (gate 4): corrected.** The 2 % floor is a divertor-relative figure read as plant-relative; the Stellaris band restated against the model's computed `p_th` (~130–195 MW for the helium-primary subset); the 2–6 % basis not narrowed (ARIES-ACT's ~1 % plant-level figure stays in evidence). Amendment applied at `knowledge/KNOWLEDGE.md` DI-008, dated, citing this trail.
- **Ruling 2 — the answer's shape (gate 2): `p_pump` stays a held, settable input, re-based.** The fraction form would assert a linearity across swept (R, a) that no source establishes, and would retire a study lever in two committed studies. Re-derive the scalar when the design point moves.
- **Ruling 3 — the value and the sources (gates 3 and 4): land ~195 MW; register Cismondi; ingest Moscato.** Granted as a mandate to WI-033 ("P_pump re-base: helium-primary circulator basis", MFE Cost Modeling epic, minted 2026-08-28): land 6 % of `p_th` at the baseline geometry (≈195 MW) in both homes of the twin with ~130 MW recorded as the documented lower bound (the `f_uplift_cryo` pattern); register Cismondi; ingest the Moscato PDF and revisit the value at first-order grade. The choice of the traceability-first end (~195 MW) over the direction-of-travel end (~130 MW) is made knowingly, per review Finding 2. Package regeneration is explicitly out of the WI's first scope — it waits on the `integrate` seam (GSTH Item 6), and the committed studies stay reproducible at their pins.
- **"Keep 1.0 MW" was tested and is unavailable** on the evidence; recorded as the `BOUNDED_NEGATIVE` on the first half of § Question.

**Effect:** `goal.md` § Answered when is met; the goal is **closed by the owner** per § Close rule. Discovery row `20260821-power-cycle-ab#3` receives its final joined row for this goal, routed to WI-033. The two `goal.md` amendments the review recommended are applied in § Amendments, operator's pen.
