# Trail: REBCO versus Nb₃Sn magnet subsystem at matched duty

What happened, and what was decided. Append-only, newest entry last, ISO dates. No entry is ever edited in place; a correction is `### Amendment YYYY-MM-DD — amends <entry heading>`. Procedure: `work/orchestration/GOAL_RUNBOOK.md`.

## Grounding — 2026-09-29

[OWNER-VERBATIM] “yes, please write the goal and we will see how it goes. write a full run-goal prompt to /tmp”. The resulting brief is preserved at [evidence/owner-brief.md](evidence/owner-brief.md) and grounds [goal.md](goal.md). Work runs on local branch `goal/magnet-material-comparison`, created from `chore/write-up-cleanup@55cc001c2` because source registration commits; the owner's uncommitted `.project/CURRENT_WORK.md` edit and untracked `.project/active/write-up/` are left untouched and are never staged by this goal.

## Round 1 — sourced-matched-duty-comparison

### Strategy revision — 2026-09-29

- **Approach:** [AGENT] Establish two facts first and in parallel: what the current model actually binds for conductor, field, fit, cryogenics and cost, and what permitted public evidence supports for each of the five evidence classes in the brief (conductor law, conductor-to-winding conversion, margins/limits, staged cryogenic demand, cost basis). If the evidence supports a useful conditional comparison, write and independently review a compact comparison contract at a supplied field-demand benchmark (ampere-turns, peak field at the conductor, conductor length and spatial allocation held common), then add genuinely different conductor definitions as isolated variants, and run one bounded native study over a common supported field range with explicit design offers for each material.
- **Assumptions:** Public primary evidence supports an Nb₃Sn field/temperature/strain scaling law with stated parameters and domain, at least one fusion-grade Nb₃Sn cable/winding construction, REBCO tape performance near 20 K over a lower-field range, and temperature-staged refrigerator efficiency. Cost evidence may support only ranges, in which case break-even analysis replaces a point ranking. A supplied duty avoids the deficient field-geometry relationship as long as no claimed result depends on geometry feeding back into field.
- **Abandonment conditions:** No permitted source supports a matched Nb₃Sn winding-pack current capability or a common field range; the model cannot host an additive conductor definition without a redesign beyond the goal's scope; or a claimed result requires field-geometry feedback that no supported evidence can repair.
- **Intended model increment:** Additive, source-cited conductor definitions (Nb₃Sn strand/cable and REBCO tape/cable) behind an explicit selection seam; temperature-staged cold-load and refrigerator demand compared with a supplied installed capacity; subsystem inventory and cost that follow the supplied winding. Existing Stellaris reference behavior unchanged.
- **Intended study question:** Across a common supported peak-field range at matched ampere-turns and conductor length, how do the two materials' supplied windings differ in current margin, conductor inventory, winding fit, cold load, refrigerator electrical demand and subsystem cost, and which of packing/cabling performance, refrigeration efficiency and conductor price reverses the preference?

**No future task list.** The next task is chosen from evidence after the previous one returns.

### T-001 scope

- **Objective:** Establish the current model's actual conductor, field, fit, cryogenic and cost equations, bindings, MR-7 roles and consumers, and the smallest additive seam for an alternative conductor definition.
- **Why now:** The strategy's first premise is that the model can host an additive conductor definition at a supplied duty; the brief requires actual bindings to be established before alternatives are designed.
- **Scope:** Read-only audit of model sources, the design instance, the generated pipeline and the write-up replay script; one evidence file. Excluded: any model, package, study or write-up change.
- **Inputs:** goal.md; evidence/briefs/t001-binding-audit.md.
- **Done when:** evidence/binding-audit.md gives file:line-cited bindings, a role table and implications, or names a precise gap.
- **Stop when:** prerequisite, strategy blocker, owner gate or declared limit.

### T-002 scope

- **Objective:** Acquire and assess permitted primary evidence for the five evidence classes (Nb₃Sn law, Nb₃Sn conductor/winding construction, REBCO law and winding construction, staged cryogenics, cost basis) and produce the evidence matrix and data-sufficiency finding.
- **Why now:** The brief makes data sufficiency the first milestone; no contract or model work is justified before it.
- **Scope:** Five research-seam requests (`knowledge/research/requests/REQ-MMC-{NB3SN-LAW,NB3SN-WP,REBCO,CRYO,COST}-01.json`), registrations through `scripts/source_registry.py`, per-class evidence notes, then a coordinator-written evidence matrix. Excluded: DI minting, model changes, purchases, source-access exceptions, quarantined content.
- **Inputs:** goal.md; evidence/briefs/t002-research-common.md and t002-research-classes.md. Clean-room screen as stated in the common brief.
- **Done when:** evidence/evidence-matrix.md classifies every required quantity as directly supported, derived, bounded assumption or unavailable, with exact locations and what each gap prevents; or a bounded negative names the missing evidence.
- **Stop when:** prerequisite, strategy blocker, owner gate or declared limit.

### T-001 start — 2026-09-29

T-001 · read-only model audit · evidence/binding-audit.md. Runs in parallel with T-002: T-001 writes only its evidence file and reads model sources; T-002 writes only request runs, registry entries and evidence/sources/. Neither result changes the other's scope. The coordinator integrates both sequentially.

### T-002 start — 2026-09-29

T-002 · research seam, five requests · run directories under knowledge/research/requests/runs/, registered sources, evidence/sources/{nb3sn-law,nb3sn-winding,rebco,cryo,cost}.md, then evidence/evidence-matrix.md. Five fresh workers, each owning one request, its run directory and its evidence note; registrations serialize through the registry lock. The coordinator owns the matrix and the trail.

### T-001 return — 2026-09-29

- **Outcome:** COMPLETE.
- **Evidence:** evidence/binding-audit.md (unpinned; no native digest until committed with this goal); brief evidence/briefs/t001-binding-audit.md. Published-design numbers are read from the untracked write-up replay (`.project/active/write-up/magnet-study-evaluation/replay/summary.json`, case s0), not rerun.
- **Reading:** The current model evaluates a supplied REBCO winding only at exactly 20 K and 20–32 T peak field; that law is hard-coded in a handwritten completion and feeds only the conductor current check, never cost. Parallel tape count is calculated from supplied pack volume and composition. Refrigeration is a two-stage Carnot × fixed-fraction chain driven by one `T_cold_cryo`; the coil thermal inventory refuses below 10 K, and the supplied cryoplant ratings equal the published demand exactly. Tape is purchased as metres at an agent-illustrative 20 $/m; winding labour follows conductor length. In the plant model, peak field and conductor length follow radial allocation and ampere-turns, so a larger Nb₃Sn pack in that geometry would change the duty. There is no Nb₃Sn law, construction, 4.5 K thermal basis, 4.5 K refrigerator rating or Nb₃Sn price basis.
- **Decision:** Plant geometry couples pack size to peak field and conductor length (audit §2–§3), and the brief allows a supplied field-demand benchmark · plan the comparison as an isolated magnet/refrigeration subsystem evaluation with duty supplied directly (ampere-turns, peak field at the conductor, conductor length, allocated space), not as a Stellaris plant variant, so the omitted winding-size field term cannot enter a claimed result · execution detail within brief § Comparison contract · coordinator · none yet; to be fixed in the comparison contract.
- **Decision:** The REBCO law refuses below 20 T while Nb₃Sn fusion conductors operate near or below about 13 T · a matched range requires REBCO evidence below 20 T at the selected temperature; the brief already directs a common lower-field range, so this is not a premise surprise · execution detail · coordinator · depends on T-002 rebco evidence.
- **MR-7:** Audit only; no roles changed. It confirms turns, turn current, pack side, composition and cryo ratings are supplied today and nothing is resized; parallel tapes are a calculated consequence of supplied pack volume and composition.

### T-003 scope

- **Objective:** Close the cheapest consequential gaps the T-002 evidence notes named: a citable Green 2015 refrigerator law (the wave-1 capture stored a bot page), magnet cold-load magnitudes near 4.5 K, a common-condition Nb₃Sn/REBCO price pair, Nb₃Sn fusion design points above 12 T, and an insulated or cable-in-conduit REBCO construction.
- **Why now:** evidence/sources/{cryo,cost,nb3sn-winding,rebco}.md each name these as the gaps limiting a matched comparison; each has a named open candidate.
- **Scope:** Four research-seam requests (`REQ-MMC-{CRYO,COST,NB3SN-WP,REBCO-WP}-02`) under evidence/briefs/t003-research-wave2.md, with downloaded-PDF registration because of the observed registry faults. Excluded: editing or removing the defective Green registration (registry is written only by its operation; the defect is reported to the owner), DI minting, paywalled or bot-walled access, model changes.
- **Inputs:** goal.md; T-002 evidence notes; the wave-2 brief.
- **Done when:** each request returns a class with per-class evidence notes, or a bounded negative.
- **Stop when:** prerequisite, strategy blocker, owner gate or declared limit.

### T-003 start — 2026-09-29

T-003 · research seam, four wave-2 requests · evidence/sources/{cryo-loads,cost-common,nb3sn-highfield,rebco-winding}.md and their run directories. Runs in parallel with the coordinator's T-002 evidence-matrix writing: workers own only their request runs, registry entries and notes; the coordinator owns the matrix and the trail and will fold wave-2 results in when they return.

### T-002 return — 2026-09-29

- **Outcome:** COMPLETE.
- **Evidence:** evidence/evidence-matrix.md (v1); evidence/sources/{nb3sn-law,nb3sn-winding,rebco,cryo,cost}.md; run directories `knowledge/research/requests/runs/REQ-MMC-{NB3SN-LAW,NB3SN-WP,REBCO,CRYO,COST}-01/`; eleven new source directories under `knowledge/sources/` plus index and manifest rows (all unpinned; no native digest until committed).
- **Reading:** A useful conditional comparison is supported over roughly 8–12 T: Nb₃Sn has a printed ITER-form law for a named ITER TF strand (Tsui & Hampshire 2012) and a complete EU DEMO strand-to-winding construction; REBCO has measured 20 K tape curves from 5 to 24 T (Molodyk) and a temperature law (Senatore), with the Stellaris Table 7 winding composition as its only insulated winding basis. Refrigeration efficiency is supported as a size-dependent fraction of Carnot common to both temperatures; conductor and refrigerator prices only as differently referenced ranges. The sourced constructions differ mostly in their non-superconducting copper and steel per kiloampere, so the construction basis is itself a consequential uncertainty.
- **Decision:** Wave-1 captures left named, reachable candidates for four gaps · run a bounded wave 2 (T-003) before the contract rather than accept them as unavailable · execution detail · coordinator · T-003.
- **Decision:** The REBCO worker parked the Molodyk-versus-Senatore curvature disagreement “for the owner” · treat it as two measured laws on different tapes and carry it as a sensitivity, because both are sourced and neither changes what the comparison asks · execution detail, not a reserved gate · coordinator · evidence-matrix.md §1.
- **Decision:** The registry recorded a bot-check page as Green 2015 (`knowledge/sources/green_2015_the_cost_of_coolers_for_cooling_superconducting/`) and fails some PDF URL captures · do not cite that entry; re-register the genuine PDF under a new entry with a superseding caveat; report the defective entry and both registry faults to the owner rather than editing registry files · execution detail; registry repair is the coding PM's · coordinator · T-003 brief.
- **MR-7:** Not applicable; research only.

### T-003 return — 2026-09-29

- **Outcome:** COMPLETE.
- **Evidence:** evidence/sources/{rebco-winding,nb3sn-highfield,cryo-loads,cost-common}.md; evidence/evidence-matrix.md § v2 additions; run directories `knowledge/research/requests/runs/REQ-MMC-{REBCO-WP,NB3SN-WP,CRYO,COST}-02/`; eight new source directories (unpinned; no native digest until committed).
- **Reading:** Wave 2 supplies a common protection-copper basis for both materials (SPC HTS 100 A/mm² versus EU DEMO 93.4 A/mm²), a REBCO cable-in-conduit capability point at 12 T and 20 K with degradation, an EU DEMO Nb₃Sn design at 13.5 T (untested at full current), a citable large 4.5 K refrigerator efficiency and capital law (Green 2015, re-registered from the publisher PDF), 4 K static-load magnitudes (EU DEMO, ITER), and a common-condition price pair with a Jc-scaled cost law. Insulated REBCO winding-pack composition beyond Stellaris, a nuclear heat-density law, a 20 K large-plant efficiency law and primary 12 T prices remain unavailable.
- **Decision:** The nb3sn-highfield worker found that the brief's “EU DEMO 83 kA / 13.7 T” label was wrong (it is JA DEMO) · use the EU DEMO 82.4 kA / 13.5 T design it found instead and record the correction · execution detail · coordinator · evidence/sources/nb3sn-highfield.md.
- **Decision:** Two workers found registry text defects they could not fix (the defective Green entry remains; an SPC “1000 m” pitch typo in its index block) · report to the owner with the registry faults; no hand edits · execution detail · coordinator · this entry.
- **MR-7:** Not applicable; research only.

### T-004 scope

- **Objective:** Obtain an independently checked source/math basis and an independently reviewed comparison contract before any model work.
- **Why now:** The brief requires consequential new source interpretations and equations to be checked against originals before dependent modeling, and a reviewed contract before implementation. evidence/comparison-contract.md (draft r1) and the coordinator screen evidence/screen/contract-screen.json are ready.
- **Scope:** Three fresh reviewers in parallel: Nb₃Sn source/math check, REBCO/cryogenics/cost source/math check, and contract design/MR-7 review; coordinator revision of the contract in response; same reviewers recheck changes. Excluded: model, package or study changes.
- **Inputs:** goal.md; evidence/comparison-contract.md r1; evidence/evidence-matrix.md; evidence/briefs/t004-*.md.
- **Done when:** both checks return PASS or their corrections are applied, and the contract review returns PASS on a released revision; or a bounded negative names what cannot be supported.
- **Stop when:** prerequisite, strategy blocker, owner gate or declared limit (checkpoint-style revision cap 2).

### T-004 start — 2026-09-29

T-004 · independent checks and contract review · evidence/check-nb3sn.md, evidence/check-rebco-cryo-cost.md, evidence/contract-review.md, then a released contract revision. Reviewers each own only their output file and are fresh sessions with self-contained briefs deposited under evidence/briefs/; the coordinator owns the contract and trail.

### T-004 return — 2026-09-29

- **Outcome:** COMPLETE.
- **Evidence:** evidence/comparison-contract.md (r3, released; r1 preserved as comparison-contract-r1.md); evidence/check-nb3sn.md (FINDINGS → Recheck r2 FINDINGS → Recheck r3 PASS); evidence/check-rebco-cryo-cost.md (FINDINGS → Recheck r2 PASS); evidence/contract-review.md (FINDINGS → Recheck r2 FINDINGS → Recheck r3 and design review FINDINGS with D1 blocking, contract released); evidence/model-design-draft.md (reviewed, D1–D7 applied, D1 diff recheck pending); coordinator screens evidence/screen/contract-screen*.json (unchecked magnitudes only). All unpinned; no native digest until committed.
- **Reading:** The checked sources support a conditional matched comparison. The reviewed contract compares supplied REBCO (20 K) and Nb₃Sn (4.5 K supply) windings at fixed coil geometry with excitation scaled to field, in a primary EU DEMO TF envelope and a secondary compact Stellaris envelope, over 8–12 T matched plus 13 T edge and a REBCO-only extension. Fit near 12 T is governed by construction conservatism rather than material, and non-superconducting protection copper and structure dominate winding area; superconductor price is expected to dominate cost, so a break-even REBCO price is the planned economic output.
- **Decision:** r1's Stellaris-only anchor made fit a construction verdict with no valid-design cost comparison above ≈9 T (B1) · move the primary matched duty to the EU DEMO TF envelope, keep Stellaris as a secondary anchor, and rank only pairs that pass every check · execution detail within the brief's delegated duty choice (reviewer: not an owner gate) · coordinator, independently reviewed · comparison-contract.md §§ 1–2.
- **Decision:** Reference strand fairness · use the ITER TF production median parameter set (Breschi Table III, WST) as the Nb₃Sn counterpart of REBCO's production-average tape, with upper/lower production sets as sensitivities · execution detail · coordinator, independently checked · comparison-contract.md § 3.
- **Decision:** Common protection copper · one density (93.4 A/mm²) for both materials so the common construction isolates material (N1) · execution detail · coordinator, independently reviewed · comparison-contract.md § 4.
- **MR-7:** Compliant at design level per the independent design review: element counts, component areas, temperatures and refrigerator ratings are supplied offers; copper/steel requirements, fit and capacity are calculated and compared; inventory and cost follow the supplied design; the offer policy is a separately declared study script. Executed behavior is unverified until the WI-099 tests run.
- **Review revision count:** three contract submissions (r1–r3), within the declared cap of two revisions.

### T-005 scope

- **Objective:** Implement the reviewed matched-duty conductor alternatives as native work item WI-099 (isolated library and design sources, handwritten bodies, generated package `magnet_materials_tea`, study route and MR-7/source tests), and an independent oracle, offer policy and declared case set.
- **Why now:** T-004 released the contract (r3) and the independent design review found the design MR-7-compliant with one small blocking precision fix (D1), now applied with a diff recheck pending.
- **Scope:** New paths only: `models/library/analyses/magnet_conductor_alternatives.sysml`, `models/designs/magnet_materials/`, `exploration/magnet_materials/`, `tests/models/test_magnet_materials.py`, `tests/models/test_magnet_oracle.py`, `work/active/WI-099_magnet-conductor-alternatives/`. Two fresh workers in parallel with disjoint ownership (implementer: model, bodies, package, route, package tests; oracle author: oracle, offer policy, case declaration, oracle tests), neither reading the other's calculation code. Excluded: any existing model, package, study or write-up change; study execution (next task); integration seam (coordinator, next task).
- **Inputs:** goal.md; evidence/comparison-contract.md r3; WI-099 design.md; evidence/briefs/t005-implementer.md and t005-oracle-policy.md.
- **Done when:** the package builds to a fixed point, its tests (MR-7 acceptance, source points, hardware isolation, unsupported ranking, preservation) pass, and the oracle and case set exist with their own tests; or a precise blocker is named.
- **Stop when:** prerequisite, strategy blocker, owner gate or declared limit.

### T-005 start — 2026-09-29

T-005 · WI-099 through the modeling PM · package `exploration/magnet_materials/magnet_materials_tea`, tests, oracle, case set. Ordering note: `agentic-mbse pm add-item` registered WI-099 in `work/BACKLOG.md` immediately before this line was written (a native side effect preceding its start line; recorded here rather than rewritten). Coordinator owns the WI spec, design copy, reference case, trail and later integration.

### T-005 return — 2026-09-29

- **Outcome:** COMPLETE.
- **Evidence:** WI-099 record work/active/WI-099_magnet-conductor-alternatives/ (spec.md, design.md with § 7 clarifications, reference-case.json, implementation-notes.md, build/ receipts); sources models/library/analyses/magnet_conductor_alternatives.sysml and models/designs/magnet_materials/magnet_subsystem.sysml; package exploration/magnet_materials/magnet_materials_tea with snapshot and census; bodies exploration/magnet_materials/bodies/; independent oracle exploration/magnet_materials/oracle.py, offer policy, declare_cases.py and oracle-notes.md; tests tests/models/test_magnet_materials.py (65 passed) and tests/models/test_magnet_oracle.py (58 passed). The declared case set exploration/magnet_materials/studies/cases.json (2832 cases, 12 MB) is left untracked and regenerable; SHA-256 f50eecd8a79e17b247194c9895ab3e2418b068cafe87ae4cd76d40d894cf82ba. All to be pinned at the next commit.
- **Reading:** The package builds to a fixed point and evaluates both supplied windings at a supplied duty with every source-point and MR-7 acceptance test passing. At the baseline (anchor D, 10 T, common-P reference offers) the independent oracle agrees with the package on all 128 non-constant channels within 2e−9 relative (absolute 1e−14 mm² on the at-allowance copper margin). Both windings pass all ten checks there; the break-even REBCO price is 11.25 USD/m (31.7 USD/kA·m at the operating point), below the 2021 market reference of 80 USD/m and the 30 USD/m target, above the 10 USD/m volume price. Full-case-set agreement and the study are the next tasks.
- **Decision:** The oracle author found the reference case double-counted the EU DEMO magnet load in the shield stage (A6) and two design ambiguities (A1 guard at T = 0; A2 unrounded construction C) · corrected reference-case.json, design.md § 7 and the contract test value (η(18 kW) = 30.13 %); the shield load is common to both materials and changes no ranking · execution detail · coordinator · files named; evidence-matrix.md correction note.
- **Decision:** Codegen cannot emit a negative design literal as an entry point (implementation-notes.md deviation 1) · leave `eps_intrinsic` unbound in the design with the value supplied by every case point and the manifest baseline, and never run the package on generated defaults · execution detail (toolchain limitation, recorded) · coordinator, from the implementer's report · study route and manifest.
- **MR-7:** Compliant in executed behavior for the tested scope: insufficient/sufficient supplied designs for acceptance, fit, copper, steel and capacity pass and fail as designed; field varied with hardware fixed leaves inventory and conductor cost unchanged; unsupported cases carry status 0, a violated acceptance and rankable 0; no supplied quantity is written by any calculation (test evidence in tests/models/test_magnet_materials.py).

### T-006 scope

- **Objective:** Prepare, integrate, execute and verify the native study `20260929-magnet-material-comparison` on the WI-099 package: one promoted pin (integration seam CANDIDATE) and one committed study over the declared 2832-case set, every case verified against the independent oracle.
- **Why now:** T-005 delivered the package, oracle and case set with baseline agreement; the contract's answer requires a sealed, verified native study.
- **Scope:** Study runbook steps 1–10, 14–15 in the new record directory, `studies/ANNEX.md` and `DISCOVERY_LOG.md`, and the integration seam out-dir under evidence/integration-r1. Excluded: any change to model, package, oracle or cases (a disagreement stops the task); the goal-level reading, report, figures and answer (next task); commits (coordinator).
- **Inputs:** goal.md; comparison-contract.md r3; WI-099 design.md § 6; evidence/briefs/t006-study-execute.md.
- **Done when:** a CANDIDATE pin, all cases executed and verified within tolerance, findings registered, snapshot resolved; or a named blocker.
- **Stop when:** BLOCKER from the seam, verification disagreement, prerequisite, owner gate or declared limit (this round's one pin and one study).

### T-006 start — 2026-09-29

T-006 · run-study execute mode and `scripts/integrate.py` · exploration/magnet_materials/studies/20260929-magnet-material-comparison/ (record, results, snapshot), studies/ANNEX.md, DISCOVERY_LOG.md, evidence/integration-r1/. One fresh executor owns those paths; the coordinator owns the trail and commits.

### T-006 return — 2026-09-29

- **Outcome:** PREREQUISITE — the integration seam refused a pin.
- **Evidence:** evidence/integration-r1/integration_return.json (BLOCKER, gate 5 `model-family-spine`, condition `repo-lineage-broken`: `analyses/magnet_conductor_alternatives.sysml` and `designs/magnet_materials/magnet_subsystem.sysml` are unregistered canonical files; gates 0–4 pass, 27 handwritten files preserved, 163 entry points re-derive); the prepared record exploration/magnet_materials/studies/20260929-magnet-material-comparison/ (record.md, axes.json, indicators.json, manifest.json, preflight results, ANNEX.md, DISCOVERY_LOG.md rows #1–#7, results/ with 2310 executed points and full oracle verification) — all unpinned; no native digest.
- **Reading:** Every package-scope gate passes and the package is at a fixed point, so the refusal is a registration gap in the repository's model-family registry (`tests/model_families.py`), not a package defect. The executor ran the study anyway under a disclosed `without_candidate` deviation; those results are useful evidence that the machinery works (all 2310 points execute; 128 channels × 2310 points agree with the oracle with zero disagreements and every verdict re-derived) but they are not this round's committed study, because the runbook requires a study to run against a promoted pin. Preflight passed all six gates; all seven axis groups are `constraints_reachable`, so no owner ruling was needed.
- **Decision:** Seam refusal names a repository-scope registration · treat as a prerequisite repair owned by WI-099 (register the `magnet_materials` source collection), re-run the seam, then re-execute and re-verify the study against the CANDIDATE pin rather than adopt the unpinned run · execution detail (seam repair is a named prerequisite, not an absorbed scope expansion) · coordinator · tests/model_families.py (T-007).
- **Decision:** Two record-local adaptations by the executor (a name-mapping `oracle_entry.py` because the stock manifest names a missing module; the contract's absolute 1e−9 tolerance clause declared in the record manifest) · accept both as disclosed glue with no physics, to be carried into the pinned re-run · execution detail · coordinator · record § 10/§ 13, finding #2.
- **MR-7:** Unchanged; the executed cases evaluate supplied offers only.

### T-007 scope

- **Objective:** Repair the prerequisite (register the `magnet_materials` model family), obtain the CANDIDATE pin, and re-execute, re-verify and seal the study `20260929-magnet-material-comparison` against it.
- **Why now:** T-006 returned PREREQUISITE with every package-scope gate passing; the fix is a two-line registry entry.
- **Scope:** `tests/model_families.py` addition (WI-099); seam re-run to evidence/integration-r2; the executor re-runs steps 5–10 and 14–15 against the pin, replacing the unpinned results; `.gitignore` entries for result files above the repository's size practice, with digests retained in the snapshot. Excluded: any model, package, oracle or case change; the reading, report and answer (next task).
- **Inputs:** goal.md; T-006 record and integration-r1; evidence/briefs/t006-study-execute.md.
- **Done when:** CANDIDATE pin recorded in the sealed record and every case verified; or a named blocker.
- **Stop when:** BLOCKER, verification disagreement, prerequisite, owner gate or declared limit.

### T-007 start — 2026-09-29

T-007 · `tests/model_families.py`, `scripts/integrate.py`, run-study steps 5–10/14–15 · evidence/integration-r2/, the sealed record and snapshot. Coordinator registers the family and commits; the T-006 executor (continuing context) re-runs the seam and the study.

### T-007 return — 2026-09-29

- **Outcome:** COMPLETE.
- **Evidence:** tests/model_families.py@c4195090a (family registration); evidence/integration-r2/integration_return.json (CANDIDATE, ten gates pass, pin `2d10694e8b9b2f4b84d53cbf4417f99d406f82d177a1181b25582eb0ee7ea6ee`, semantic `4d37dbaf…f2f6`, executable `7075e929…2e3f`, teax `8d877460…`); sealed record exploration/magnet_materials/studies/20260929-magnet-material-comparison/ (record.md, snapshot.json sha256 `9f16a48c…7596a`, results/, verification), studies/ANNEX.md and DISCOVERY_LOG.md — pinned at the sealing commit that follows this entry.
- **Reading:** The study ran against the promoted pin: 2832 declared cases, 2310 distinct executed points (522 aliases), all completed; the pinned run reproduces the earlier unpinned run exactly. Every non-constant channel of every point agrees with the independent oracle (0 disagreements, 0 verdict mismatches; the worst relative deviation is 3.3e−5 on an acceptance margin of 7.9e−7 K, absolute 2.6e−11 K). Nb₃Sn statuses: 1760 supported, 352 edge, 180 law-only, 540 unsupported; REBCO 2832 supported. 610 matched pairs are rankable (574 on anchor D, 36 on anchor S, the latter only under common-C); REBCO is dearer in 598 of them at the evaluated prices, Nb₃Sn dearer in 12 (REBCO at the 10 USD/m volume price, anchor D, 9–11 T). This is a valid study reading; the round's one pin and one study are spent.
- **Decision:** The machine-local result files (case dump, native store, artifacts, oracle scan; ≈152 MB) follow the repository's 2026-09-27 practice · keep them out of git with their digests in snapshot.json and record § 17 · execution detail · coordinator · .gitignore@c4195090a.
- **MR-7:** Compliant in executed behavior across the study: every case evaluates supplied offers; the offer policy is a separate study script; unsupported cases carry no ranking (verification re-derived every verdict).

### T-008 scope

- **Objective:** Produce the answer contract's deliverables from the sealed record: results table, SVG/PNG figures with data and renderer, `answer.md`, and the proposed narrative with its component/material-example assessment; obtain an independent final review of the reading and claims.
- **Why now:** T-007 sealed a verified study against the pin (record @7836424ca).
- **Scope:** Reporting worker owns evidence/figures/ (data, renderer, figures, results-table.md, README); coordinator writes answer.md and evidence/proposed-narrative.md; a fresh reviewer checks claims against the record and contract. Excluded: any change to the record, model, package or study; article or HTML edits.
- **Inputs:** goal.md; sealed record; comparison-contract.md r3; evidence/briefs/t008-reporting.md.
- **Done when:** figures trace to recorded cases, the answer states what differs, what is established, which assumptions matter and what remains unanswered, and the review returns PASS or its findings are resolved.
- **Stop when:** prerequisite, owner gate or declared limit.

### T-008 start — 2026-09-29

T-008 · reporting from exploration/magnet_materials/studies/20260929-magnet-material-comparison@7836424ca · evidence/figures/, answer.md, evidence/proposed-narrative.md, evidence/final-review.md.

### T-008 return — 2026-09-29

- **Outcome:** COMPLETE.
- **Evidence:** answer.md; evidence/proposed-narrative.md; evidence/figures/ (render_figures.py, data/*.csv with case ids, F1–F6 SVG+PNG, results-table.md, README.md); evidence/final-review.md (fresh reviewer: answer, narrative and figures each PASS WITH CORRECTIONS on first pass, findings 1–25; corrections applied; `## Recheck` section with the final verdicts); briefs evidence/briefs/t008-reporting.md and t008-final-review.md. All to be pinned at the commit that follows this entry.
- **Reading:** The answer states, from the sealed record alone, that at matched duty where both conductors are supported and fit (8–11 T on the EU DEMO envelope under common construction) the supplied Nb₃Sn winding is the cheaper subsystem under every checked assumption that leaves the pair rankable, except the REBCO price: 48.5 against 286.1 M USD/yr at 10 T, break-even REBCO price 11.25 USD/m (6.62–23.13 over the 592 supported-status rankable pairs), sign reversed only at the 10 USD/m volume price at 9–11 T. Refrigeration is 1.5 % of the annualized conductor cost difference. The Nb₃Sn law variants (strain, grade) and REBCO law variants (shape, T*, degradation) move rankability of fixed hardware, not the sign; the construction rule, not the conductor law, decides the 12 T fit boundary. The narrative passes the categorical, matched, designer-choice and novelty tests and fails the Part 4b combined-library test; it is a defensible material-choice example for the main post's "Material A vs B" claim or Part 2, not for Part 4b § 4.2.
- **Decision:** The reviewer's first-pass corrections (scope of the 610-pair range, anchor S common-C "hypothetical" label, steel failing both materials, strain-variant break-even over all fields, T1–T5 provenance, five missing qualifications, unmarked fit-failing points and `green_extrapolated` in F2–F4/F3) · all applied and rechecked by the same reviewer (recheck verdicts: narrative PASS, figures PASS, answer PASS WITH CORRECTIONS with one item left: the 592-pair median is 11.13 not 11.25, and only the two 14 T law-only common-C pairs exceed 23.13) · the last item is objectively verifiable, so the coordinator applied it and verified it by recomputation from results/cases.csv (592 pairs, median 11.13, max 23.13; pairs above 23.13: `D-14T-common-C-both-temperature-none-reference-reference` 24.63 and `…-generous-reference` 24.49) instead of a third review pass, together with the reviewer's finding-3 wording note · execution detail · coordinator and reporting worker · final-review.md § Recheck.
- **MR-7:** Reporting only; no model or study change. The answer and narrative present supplied offers as supplied and unranked pairs as unranked.

### Round 1 result — 2026-09-29

- **Intent:** met. The strategy's question (matched supplied windings of two genuinely different conductor definitions compared over a common supported range for current margin, inventory, fit, cold load, refrigerator demand and subsystem cost, with the assumptions that reverse the preference identified) is answered in answer.md, from one promoted pin and one sealed study.
- **Task sequence:** T-001 binding audit (COMPLETE) → T-002 evidence classes and matrix (COMPLETE) → T-003 second research wave (COMPLETE) → T-004 independent source checks and contract review (COMPLETE, contract r3 released) → T-005 WI-099 implementation with independent oracle (COMPLETE) → T-006 study preparation and execution (PREREQUISITE: seam blocker) → T-007 registration, CANDIDATE pin, re-execution and seal (COMPLETE) → T-008 reporting, answer, narrative and final review (COMPLETE).
- **Last semantic outcome:** COMPLETE (T-008), following the valid study reading of T-007.
- **Stop reason (derived):** valid study reading → the round closes (trigger 1). The round's one pin (`2d10694e…`) and one study (`20260929-magnet-material-comparison`) are spent; no limit was reached (0 retries; checkpoint not invoked, since the T-007 reading proposed no semantic follow-up task).
- **Evidence refs:** goal.md, evidence/owner-brief.md, evidence/binding-audit.md, evidence/evidence-matrix.md, evidence/sources/*.md, evidence/comparison-contract.md (r3; r1 preserved), evidence/check-nb3sn.md, evidence/check-rebco-cryo-cost.md, evidence/contract-review.md — all @6c2570290; work/active/WI-099_magnet-conductor-alternatives/, models/library/analyses/magnet_conductor_alternatives.sysml, models/designs/magnet_materials/magnet_subsystem.sysml, exploration/magnet_materials/ (package, bodies, oracle, studies), tests/models/test_magnet_materials.py, tests/models/test_magnet_oracle.py — @2869c34aa; tests/model_families.py, .gitignore — @c4195090a; exploration/magnet_materials/studies/20260929-magnet-material-comparison/ (record, snapshot sha256 `9f16a48c…7596a`, results), studies/ANNEX.md, studies/DISCOVERY_LOG.md, evidence/integration-r1/ and integration-r2/ (CANDIDATE) — @7836424ca; answer.md, evidence/proposed-narrative.md, evidence/figures/, evidence/final-review.md — the commit that follows this entry.
- **Proposed learning delta:** L-001 the preference is a conductor-price question at this duty and refrigeration is second-order; L-002 fit boundaries in a fixed envelope are construction-rule results, not conductor-law results; L-003 conductor-law uncertainty moves rankability of supplied hardware, not the sign, and MR-7 offers make that visible; L-004 (process) the integration seam needs family registration before a pin, the codegen cannot emit a negative design literal as an entry point, and the stock manifest must name a real oracle module.
- **Finding dispositions** (rows appended to exploration/magnet_materials/studies/DISCOVERY_LOG.md under the existing ids; none minted): #1 already resolved by registration (T-007). #2 → upstream filing, open: the package-level `oracle_entry` module and manifest tolerance declarations are WI-099 work for the owner's item closure; the sealed record is self-contained. #3 → declared seam, landed: reported as break-even price in answer.md with the sign-flip condition. #4 → research, queued: a sourced Nb₃Sn winding-pack construction at 12–13 T (answer.md § Unmet criteria); the answer claims no field limit. #5 → declared seam, landed: answer.md carries anchor S as rankable only under common-C, labelled hypothetical for Nb₃Sn. #6 → research, queued: a refrigerator cost law valid to 50 kW at 4.5 K; the flag is carried into F3 and the answer. #7 → declared seam, landed: aliases exported and carried into every figure data CSV.
- **Constraints carried forward:** the article and HTML remain unedited; goal and WI-099 closure are owner-held; any second round re-anchoring on a combined-library magnet needs its own pin and study.

### Round 1 review — 2026-09-29

- **Reviewer:** coordinator check plus independent coverage already obtained inside the round; no separate round-level fresh reviewer was commissioned. Reason: every triggered risk was covered by a fresh non-author during the round — source interpretation and equations (T-004 checks A and B, contract review r1→r3 with Recheck), model implementation (independent oracle by a separate author, 0 disagreements over 2310 points; design review D1–D7), the study reading and its dispositions (T-007 reading was factual and proposed no semantic follow-up; the T-008 final review checked every quoted number, the structural claims, contract discipline, answer-contract coverage, the figures and the narrative's category assessment, then rechecked the corrections). The round changed no existing package, model or study (integration-r2 gate outcomes; `git status` shows only new paths and the two registry lines), so the broad-integration trigger does not apply.
- **Checks:** every evidence ref above resolves at the cited commit; the round pursued the declared strategy (sourced matched-duty comparison) without a strategy revision; each task stayed inside its recorded scope (one recorded slip: `pm add-item` for WI-099 ran before the T-005 start line, recorded in the T-005 start entry; no content effect); no retries were taken; the discovery rows #1–#7 each carry a landed disposition or a concrete next reference; no cited native artifact moved outside its task (the record was sealed once, at 7836424ca, and the T-008 artifacts read it without change).
- **Learning delta:** L-001–L-004 accepted as proposed and appended to learnings.md.
- **Remaining uncertainty:** the 12 T fit boundary rests on the extrapolated common-P construction allowances (finding #4); the refrigerator cost law is extrapolated at 11 T and above on anchor D (finding #6); conductor manufacturing and joint/lead costs are partial accounting; common-C is hypothetical for Nb₃Sn. None changes the sign or the break-even band inside the supported range.
- **Recommendation:** recommend owner-held closure of the goal on the Round 1 answer, with the three next-evidence items in answer.md § Unmet criteria offered as an optional second round; recommend owner closure of WI-099 after the package-level `oracle_entry` module (finding #2) is either written or waived.
