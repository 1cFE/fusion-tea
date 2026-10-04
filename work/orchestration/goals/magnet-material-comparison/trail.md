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

## Round 2 — plant-consequence-lcoe-comparison

### Strategy revision — 2026-09-30

Opened on the owner's Round 2 brief ([evidence/owner-brief-round2.md](evidence/owner-brief-round2.md); goal.md Amendment 1). Question: “Can REBCO’s additional field or winding-space capability improve the plant enough to offset its higher magnet cost, measured in LCOE?”

- **Approach:** [AGENT] Work the chain conductor choice → field and winding geometry → plant performance and equipment → LCOE inside one coherent plant model, and let each material carry its own supplied plant design. First establish, from the model and its prior studies, what the plant already computes along that chain, where its field/geometry relationship is known to be deficient, and how its LCOE accounts overlap Round 1's subsystem accounts. Then reconcile the accounting boundary, repair the field/geometry relationship with sourced evidence where the answer depends on it, bring the two conductor definitions and temperature-staged refrigeration into the plant package behind an explicit selection seam, and write a plant comparison contract that names the per-material design choices, the bounded search ranges and the interaction cases (field × pack allocation × REBCO price × construction rule). Then one native study of a few verified design points per material with an LCOE decomposition, a matched-duty connection to Round 1, and the whole-plant break-even REBCO price where a supported crossing exists. Cleanup the owner named (package `oracle_entry`, retirement of the bot-page source entry) runs alongside as bounded native work.
- **Assumptions:** The Stellaris plant package (`exploration/stellarator_e2e`, 199 calculations, native LCOE) is the coherent plant model: its axis field follows from coil count, ampere-turns and major radius, its plasma performance and sustainment depend on that field, and its LCOE carries magnet capital, cryo electricity and net electricity (Round 1 binding audit §§ 2, 5). The plant's field–geometry deficiencies are the omitted winding-pack term in peak field and the transverse-casing response, both recorded in prior goals and in the owner's evaluation; sourced relations exist to repair or bound them. Round 1's conductor definitions transfer into the plant package as additive definitions. A lower-field design point is inside the plasma scaling's supported domain, so that field consequences are computed, not inferred from a conductor limit.
- **Abandonment conditions:** No sourced relation ties winding-pack size or allocation to peak field and coil geometry, so REBCO's “winding-space capability” cannot reach the plant; the plant package cannot host a 4.5 K conductor and staged refrigeration without a redesign beyond the goal's scope; the plasma scaling or the plant's cost accounts have no supported domain at the field a Nb₃Sn design requires, so a credible LCOE for the Nb₃Sn plant cannot be established (then partial completion, naming the missing relationship, per the brief).
- **Intended model increment:** In the plant package: a conductor selection seam carrying both Round 1 definitions at their own temperatures; a peak-field relation that responds to winding-pack size and radial allocation with sourced coefficients; temperature-staged cold loads and refrigeration at 4.5 K and 20 K with supplied ratings; conductor price bases per material; every supplied design choice (turns, turn current, pack side, allocation, casing, ratings, field target) kept supplied, requirements calculated. Existing Stellaris reference behavior preserved under the reference selection.
- **Intended study question:** For a small set of supplied plant design points per material inside justified ranges of peak field, major radius and winding allocation, how does whole-plant LCOE decompose between magnet purchases, structure, refrigeration and electrical consumption, affected plant equipment and net electricity, which design points pass every check, and at what REBCO price does the whole-plant preference change; and does higher field or smaller size change the value of a lower REBCO price, or do construction limits and other plant costs erase it?

**No future task list.** The next task is chosen from evidence after the previous one returns.

### T-009 scope

- **Objective:** Read-only audit of the plant chain and the accounting boundary: what `exploration/stellarator_e2e` computes from conductor choice through field, geometry, plasma performance, equipment and LCOE; the exact form and evidence status of the known field/geometry deficiencies; which LCOE accounts already carry magnet purchases, structure, refrigeration, electricity, replacements and net electricity, and how they map onto Round 1's subsystem accounts; what prior studies (magnet-technology A/B, joint sizing, feasible neighborhood, magnet design transfer, coil realism) already established and what they left open; and the smallest additive seam for two conductor definitions and 4.5 K staging in the plant package. Also state why this package, and not the ARIES-integrated or whole-plant-conversion packages, supports the comparison, or say if it does not.
- **Why now:** The brief requires one coherent plant model chosen with reasons, the accounting boundary reconciled before any LCOE is quoted, and field/geometry limitations resolved where the result depends on them; none of that can be scoped without this audit.
- **Scope:** Model sources, generated pipeline, prior study records and goal answers, the Round 1 binding audit; one evidence file. Excluded: any model, package, study or write-up change; research acquisition.
- **Inputs:** goal.md with Amendment 1; evidence/owner-brief-round2.md; evidence/binding-audit.md; evidence/briefs/t009-plant-chain-audit.md.
- **Done when:** evidence/plant-chain-audit.md gives file:line-cited bindings for the chain, a deficiency table with what each deficiency would change in this comparison, an account-boundary map (plant account ↔ Round 1 account ↔ gap), a prior-evidence table, a seam proposal, and the package recommendation; or names a precise gap.
- **Stop when:** prerequisite, strategy blocker, owner gate or declared limit.

### T-010 scope

- **Objective:** The cleanup the brief names: (a) write the package-level `exploration.magnet_materials.studies.oracle_entry` module and the stock manifest's tolerance declarations so the stock verifier runs from `exploration/magnet_materials/studies/manifest.json` (finding `20260929-magnet-material-comparison#2`); (b) add a `retire` operation to the source registry (the only write door into `knowledge/`), with tests, and retire the bot-page entry `green_2015_the_cost_of_coolers_for_cooling_superconducting` under it, leaving a durable retirement record and the genuine `green_2015_cost_of_coolers_at_4_2_20_40_and_77_k_publisher` entry untouched.
- **Why now:** Owner-authorized in the Round 2 brief; independent of T-009; both are prerequisites for a clean second pin and a clean citation base.
- **Scope:** New module and manifest edit under `exploration/magnet_materials/studies/`; `scripts/source_registry.py` (+ `zotero_lib` if needed) and `tests/research/`; the registry operation applied once. Excluded: any change to the sealed record, the Round 1 package bodies or models, or any other source entry.
- **Inputs:** evidence/briefs/t010-cleanup.md; `.project/completed/20260827_goal-research-seam/` design; record `20260929-magnet-material-comparison` § 15 finding #2 and its `oracle_entry.py`.
- **Done when:** the stock verifier runs from the package manifest against the sealed record's results with 0 disagreements; `scripts/source_registry.py verify` reports no drift after the retirement; registry tests pass; the retired slug no longer appears in SOURCE_INDEX.md.
- **Stop when:** prerequisite, owner gate or declared limit.

### T-009 start — 2026-09-30

T-009 · read-only plant-chain and accounting audit of `exploration/stellarator_e2e` · evidence/plant-chain-audit.md. Runs in parallel with T-010: T-009 writes only its evidence file; T-010 writes only under `exploration/magnet_materials/studies/` (new module, manifest), `scripts/`, `tests/research/`, `tests/models/` and the registry's own files. Neither result changes the other's scope.

### T-010 start — 2026-09-30

T-010 · package `oracle_entry` and manifest tolerances; registry `retire` operation with tests, applied once to the bot-page entry · files as scoped; brief evidence/briefs/t010-cleanup.md.

### T-009 return — 2026-09-30

- **Outcome:** COMPLETE, with premise conflicts surfaced (OWNER_GATE on the Nb₃Sn plant basis; see the Decision lines).
- **Evidence:** evidence/plant-chain-audit.md (§ 2 chain with file:line bindings; § 3 deficiency table D1–D8; § 4 account-boundary map; § 5 prior-evidence table; § 6 seam proposal; § 7 package recommendation; § 8 premise conflicts). Pinned at the commit that follows this entry.
- **Reading:** `exploration/stellarator_e2e` is the one package that computes the chain the brief names (axis field from ampere-turns and geometry; peak field from the bore; a supplied winding with fit, stress and strain; ISS04 sustainment and beta reading the field; staged cryo; native LCOE); `aries_integrated` supplies its field and has no magnet model, `whole_plant_conversion` freezes one 48 kA capture. Field reaches the plasma only through the ISS04 confinement time (heating demand, ash) and beta; fusion power does not read field; equipment accounts are field-blind supplied prices (D7). The peak field omits Lion 2021 eq. 39's winding-pack term (D1, `a1(C)` unprinted anywhere in the corpus) and its peak ratio 2.7667 is anchored to the Stellaris coil set (D3); the tape count is implied by the 9 % composition rather than supplied (D4); the conductor law, thermal inventory and cryo screens refuse or mis-rate anything but 20 K (D5, D6); the plasma scaling declares no validity band away from the Stellaris point (D8). No passing plant exists at the Stellaris reference on the current model (six failures, four non-magnet); every prior all-pass point predates the supplied-winding model. The plant already carries every Round 1 account in another form (tape metres from pack volume at 20 $/m of 6 mm tape, year unstated; winding operations ≈ 2,333 $/conductor-m always on; supplied cryo price 31.48 M$; 0.20 Carnot; DCF ≈ 0.16/yr; electricity valued at the plant LCOE), so nothing annualized from Round 1 may be added and one conductor-quantity, tape-width, price and money-year basis must be fixed first.
- **Decision:** With the Stellaris peak ratio held, Nb₃Sn's supported field (≤ 12 T peak) puts the axis field at 4.34–4.70 T, where beta (≈ 11 % vs the 5 % limit), heating (≈ 4.8×) or size (R ≈ 34 m) leave every anchored fact's neighbourhood and the plasma scaling declares no domain (audit § 8.1; the 2026-08-23 A/B found 0 of 4,144 feasible Nb₃Sn points). Choosing the Nb₃Sn plant basis changes the comparison's meaning · returned to the owner with options and a recommendation (this session's report) · reserved gate (unresolved scientific choice) · owner · dependent work (plant contract, seam implementation, study) parked; independent work (D1/D8 research, cleanup) continues.
- **Decision:** REBCO's own levers are blind or barred today (D1 pack term absent; `B_max` 24.9 T owner-ruled zero-margin ceiling; D4 count implied), so REBCO's "winding-space capability" has no field consequence until D1 and D4 are repaired · research D1 first; port the supplied count (D4) with the seam · execution detail under the brief's “resolve the known field/geometry limitations” · coordinator · audit § 3, § 6.
- **MR-7:** Read-only; the audit's role classification (§ 2) and seam proposal keep turns, current, pack side, allocation, counts, ratings and prices supplied.

### T-010 return — 2026-09-30

- **Outcome:** COMPLETE.
- **Evidence:** exploration/magnet_materials/studies/oracle_entry.py (new; delegates to oracle.py), exploration/magnet_materials/studies/manifest.json (oracle note and `absolute_tolerances` copied from the record's manifest; fingerprints byte-identical), tests/study/test_magnet_materials_oracle_entry.py (5 passed); scripts/source_registry.py `retire` and scripts/zotero_lib.py (`RETIRED_PATH`), tests/research/test_retire.py (17) with conftest and hermetic-path updates (tests/research 167 passed; 172 with the oracle-entry test); knowledge/RETIRED.jsonl (one line: slug, `retired_at` 2026-09-30T03:13:32Z, reason, index-block sha256 `5ddfdf60…`, the removed manifest row verbatim); knowledge/MANIFEST.jsonl −1 row, knowledge/SOURCE_INDEX.md −16 lines, `knowledge/sources/green_2015_the_cost_of_coolers_for_cooling_superconducting/` removed; docs/research_seam_operator_guide.md `retire` section. Pinned at the commit that follows this entry.
- **Reading:** The stock verifier now runs from the package manifest against the sealed record's stores: 2,311 rows, 16 objective/binding channels, 0 disagreements, 0 verdict mismatches, bindings digest and worst deviation identical to the record's (the stores are machine-local, so a fresh clone cannot rerun this; the package adapter also matched the record adapter on all 128 channels over 300 sampled points). `verify` reports 0 faults and the 3 pre-existing legacy entries after the retirement. Finding `20260929-magnet-material-comparison#2` is resolved (disposition row appended below at the round result).
- **Decision:** The genuine Green entry's caveat says it "supersedes" the retired slug, which the brief's literal R3 would have refused · a carve-out lets a reference that *supersedes* the retiree stand while any other reference blocks; tested · execution detail (the requirement was the coordinator's ad hoc rule) · coordinator, ratifying the worker's choice; reported to the owner · tests/research/test_retire.py.
- **Note:** `tests/study/test_known_answers.py` (stellarator pin) fails before and after this task; unrelated to it, reported to the owner. Historical references to the retired slug remain in Round 1 evidence notes and request runs (listed in the worker's return); left as history.

### T-011 scope

- **Objective:** Acquire and assess the evidence every Nb₃Sn-plant option needs and REBCO's own levers need: (A) the winding-pack term of the peak-field relation (Lion 2021 eq. 39: printed coefficients, a second anchor, the appendix A cuboid formula, or a sourced self-field form); (B) the ISS04 scaling's fitted ranges, the renormalization factor's meaning, and what the sources state about a 4–5 T on-axis operating point; (C) sourced Nb₃Sn/NbTi stellarator reactor design points (HELIAS 5-B and kin) as a second coil-set anchor and existence proof.
- **Why now:** T-009 surfaced that D1 (pack term) blocks REBCO's winding-space lever under every option and that D8/D3 decide whether an Nb₃Sn plant is a design point on this plant at all; the owner's choice among the Nb₃Sn-plant bases is better made on this evidence, and the research is independent of that choice.
- **Scope:** Three research-seam requests (`REQ-MMC-FIELD-01`, `REQ-MMC-PLASMA-01`, `REQ-MMC-NB3SN-PLANT-01`), registrations, three evidence notes under evidence/sources/. Excluded: model changes, DI minting, purchases, source-access exceptions, quarantined content.
- **Inputs:** evidence/briefs/t011-research-plant.md (+ t002-research-common.md); evidence/plant-chain-audit.md § 3, § 8.
- **Done when:** each note classifies its quantities and states plainly whether the pack term can be fixed, whether a 4.3–4.7 T point is a supported extrapolation, and whether a sourced Nb₃Sn stellarator anchor exists; or names the missing evidence.
- **Stop when:** prerequisite, strategy blocker, owner gate or declared limit.

### T-011 start — 2026-09-30

T-011 · three fresh research workers in parallel, one request each · evidence/sources/field-term.md, plasma-validity.md, nb3sn-stellarator.md; request runs under knowledge/research/requests/runs/. Runs alongside the owner gate raised at the T-009 return; no dependent work starts until the owner rules.

### T-011 return — 2026-09-30

- **Outcome:** COMPLETE (all three requests REGISTERED); the evidence sharpens the owner gate raised at T-009 rather than resolving it.
- **Evidence:** evidence/sources/field-term.md, plasma-validity.md, nb3sn-stellarator.md; runs knowledge/research/requests/runs/REQ-MMC-{FIELD-01,PLASMA-01,NB3SN-PLANT-01}/; five new registrations: `ukaea_process_superconducting_tf_coil_model_documentation/`, `confinement_study_of_net_current_free_toroidal_plasmas/` (Yamada 2004, ISS04 precursor), `from_w7_x_to_a_helias_fusion_power_plant_motivation_and/` (Warmer 2016), `helias_5_b_magnet_system_structure_and_maintenance_concept/` (Schauer 2013, author manuscript, image-only), `coil_winding_pack_fe_analysis_for_a_helias_reactor_schauer/` (Schauer 2011). Pinned at the commit that follows this entry.
- **Reading (D1, pack term):** Lion 2021 eq. 39 as printed is `B_max = μ0 I N/(R − a_coil) · [a0(C) + R a1(C)/√A_wp]`; a0, a1 are printed nowhere for any coil set. No second same-coil-set (B_max, A_wp) pair exists; Stellaris Table 8's six coils (I 15.4→11.2 MA, pack side 360→300 mm, peak 24.6→19.5 T, all at j_WP 112–124 A/mm²) are six coil shapes, so they validate a computation but do not separate a0 from a1. Appendix A's cuboid-beam formula is transcribed (with printed typos noted); computing a1 is a bounded closed-form sum once coil filaments exist, and no registered source holds Stellaris filaments (the Proxima CAD is a scaled W7-X, uncaptured). A three-point Helias-5 fit (ratio ≈ 0.15 + 0.064·R/√A_wp) is poorly conditioned and may mix coil sets: sensitivity-arm material only. Exact Ampère floor `B_max ≥ μ0 I/(4√A_wp)` (13.4 T of 24.6 T at coil 0). Tokamak PROCESS's pack-size peaking fit is for 16–20 planar coils with coefficients in code. Queued: Schauer 2013 publisher version; MPG PuRe item (403).
- **Reading (D8, plasma validity):** Stellaris uses f_ren = 1.0 at ⟨β⟩ 3 % with no numerical beta limit and no validity band printed (the model's 5 % is a PROCESS input). Every sourced HELIAS-class Nb₃Sn/NbTi point at 4.75–5.9 T closes only with confinement enhancement f_ren 1.33–1.8 at the 4.2–5 % beta limit (Lion 2023 Table 4.3: 5.81 T, f_ren 1.38, β 5 %, R 17.1 m; Beidler HSR5/22 4.75 T, τE ratio 1.69; Warmer 2016 windows cap f_ren ≤ 1.5 for Nb₃Sn). A 4.3–4.7 T point with f_ren = 1.0 is undeclared by every source and unsupported by every sourced analogue. Discrepancy found: ISS04 density exponent 0.52 (Lion 2021 eq. 9, thesis eq. 1.26) vs 0.54 (Stellaris eq. A.7 and the model), ≈ 7 % in τE; the journal ISS04 paper (Yamada 2005) is queued (bot-check/embargo). Registry `--use-for` for Yamada 2004 states per-device f_ren "about 0.4–1.2" where Fig. 3 reads 0.25–1.0 (tool-written prose; the note carries the correct values).
- **Reading (Nb₃Sn anchors):** HELIAS 5-B (Schauer 2013 Table 1): 50 coils, R 22 m, a 1.8 m, 5.9 T axis, 12.5 T on coils (ratio 2.12), 86 kA Nb₃Sn/Nb₃Al cable, pack 0.75 × 0.71 m (0.53 m², 4.1× Stellaris), 3000 MW "estimated for a plasma axis field of 5 T" (not self-consistent at 5.9 T). HSR50a (2011): 5.6/12.3 T, 13.4 MA per coil, 4.7 K, field "limited mainly by structural integrity". Every HELIAS-line and ITER design sits at peak/axis 2.0–2.2 against Stellaris 2.77; k_link 0.92–0.97 vs 0.773. Self-consistent Nb₃Sn points are PROCESS outputs at 5.5–7.1 T; none at 4.3–4.7 T. Using HELIAS 5-B as the Nb₃Sn anchor re-anchors ≈ 25 held constants (listed in the note). Queued: Schauer 2009/2010 "Extrapolation of the W7-X magnet system to reactor size"; Muldrew 2021 HELIAS 5-B PROCESS point (not captured, limit).
- **Decision:** Option (a) of the T-009 gate (same coil set at ≤ 4.7 T axis) can only be run under a supplied confinement enhancement the sources give for other configurations (1.33–1.8), so the two materials would be compared under different confinement assumptions; option (b) is a sourced but different configuration; option (c) remains fully supported · restated to the owner with a revised recommendation (this session's report) · reserved gate · owner · dependent work stays parked.
- **MR-7:** Research only; no model change.

### Owner ruling on the T-009 gate — 2026-09-30

[OWNER-VERBATIM] “we need to focus on getting some insight. Across explicit assumptions about confinement and coil geometry, when does each material give lower LCOE—and are those conditions supported by evidence?”

[AGENT] Reading of the ruling, applied from here: the Nb₃Sn plant basis is not chosen among (a)/(b)/(c); instead confinement (the renormalization factor and beta limit) and coil geometry (the peak/axis field ratio and the pack-size term) become explicit, declared assumption axes. For each assumption cell the round finds the best supported plant design per material inside a bounded search, compares LCOE, and labels the cell with the evidence support of its assumptions (directly supported at Stellaris; sourced analogue from another configuration; derived; assumption). The deliverable is that map with its evidence labels, the LCOE decomposition behind it, and the REBCO price at which the preference changes per cell. Recorded as goal.md Amendment 2. Dependent work resumes.

### T-012 scope

- **Objective:** Write the plant comparison contract (r1) that makes the owner's refined question executable on the Stellaris plant: assumption axes with evidence labels, materials in the plant, supplied-design policy and bounded grid, single accounting basis, statuses, reporting, package and verification plan; obtain a fresh review and release r2.
- **Why now:** The owner's ruling resolved the T-009 gate; the T-011 evidence fixes what each assumption value can be labelled; no design or implementation may start before the contract is reviewed (brief: "focused independent review of … comparison assumptions").
- **Scope:** evidence/plant-contract.md (coordinator), evidence/plant-contract-review.md (fresh reviewer), one revision round. Excluded: model, package or study changes.
- **Inputs:** owner-brief-round2.md, goal.md Amendments 1–2, plant-chain-audit.md, sources/{field-term,plasma-validity,nb3sn-stellarator}.md, Round 1 comparison-contract.md r3, briefs/t012-plant-contract-review.md.
- **Done when:** the review returns RELEASE, or its blocking and must-fix findings are applied and rechecked.
- **Stop when:** BLOCK on a premise the owner must rule on, or declared limit.

### T-012 start — 2026-09-30

T-012 · plant-contract.md r1 written by the coordinator · fresh reviewer dispatched on briefs/t012-plant-contract-review.md. Design drafting (next task) waits for the review's blocking findings.

### T-013 scope

- **Objective:** Open WI-100 (plant-level conductor material variants on the Stellaris plant) through the modeling PM and produce its reviewed design: the isolated derived package `exploration/stellarator_materials/` per the audit's seam proposal and the plant contract § 9, with the material variants, staged cryoplant, supplied element count and `pack_area_ok`, the pack-arm slot, the three-instance design file, the reference bit-for-bit regression, and the study interface (entry keys for every contract § 5 supplied quantity, including the package ratings, purchase costs and power classes).
- **Why now:** The plant contract r2 fixes the physics and accounting; the seam mechanics (WI-057 retype, WI-096 isolation, WI-080 enabled/evaluation_defined pattern) do not depend on the recheck's remaining details; the design and the contract recheck can be reviewed together.
- **Scope:** `work/active/WI-100_*/spec.md` and `design.md` (coordinator spec; fresh modeler design); a fresh design review. Excluded: implementation, bodies, package build, studies.
- **Inputs:** plant-contract.md r2; plant-chain-audit.md § 2, § 6; WI-099 design and library; WI-057, WI-096, WI-080 designs; briefs/t013-design.md.
- **Done when:** the design names every file, definition, binding, entry key and test, with MR-7 roles, and the review returns PASS or its findings are applied.
- **Stop when:** a seam step proves infeasible in the toolchain (report), owner gate, or declared limit.

### T-013 start — 2026-09-30

T-013 · WI-100 registered through `agentic-mbse pm add-item` immediately after this line · spec.md by the coordinator · design.md by a fresh modeler on briefs/t013-design.md · fresh design review after the contract recheck lands.

### T-012 return — 2026-09-30

- **Outcome:** COMPLETE; plant contract r3 released.
- **Evidence:** evidence/plant-contract.md (r3), evidence/plant-contract-r1.md (preserved), evidence/plant-contract-review.md (r1 review REVISE: 3 blocking, 13 must-fix, 8 notes; `## Recheck r2` RELEASE with five one-sentence corrections). Pinned at the commit that follows this entry.
- **Reading:** The r1 draft would have decided the map for reasons that are not the question: the held plasma temperature made enhanced-confinement and high-field REBCO designs burn-hold failures; the plant's ~35 captured equipment ratings were held while thermal power moved; and the "matched-duty connection" compared the materials at different fields. r2 adds an operating-point ladder with matched fusion power and an `ignited` status with a driven companion design, re-supplies every screened package rating and the power classes per design with a declared [U] purchase scaling and a `free_capacity` flag, adds equal-duty REBCO points and smaller plants to the grid, makes evidence labels per design with the cell label the weaker of the two plus a policy-assumption column, labels the HELIAS-class geometry [U] with a `k_link` variant, gives the pack arm a domain flag, treats `B_max` as a supplied envelope flag, adds the basis bridge and the money-year bias, measures the break-even from two evaluated prices, and adds figures, replay, narrative and the focused checks. The recheck confirmed by scaling on the recorded reference that the ladder makes 18 T REBCO designs driven under enhanced confinement while 24.9 T stays ignited everywhere, so `ignited` will be a common labelled status at the top of the field grid.
- **Decision:** The five r2 corrections (money-year direction depends on the sign of the non-conductor difference; `peak_field_ok` carried as `envelope_flag`, not `failed`; "selected building and parcel dimensions"; order-10⁴ policy evaluations; purchase-exponent variants 0.5/1.0) and the garbled companion phrase · applied as r3 by the coordinator without a further reviewer pass, as the recheck itself ruled them objectively verifiable · execution detail · coordinator · plant-contract.md r3 header.
- **MR-7:** The contract keeps every policy-proposed quantity supplied and checked; the model resizes nothing; the conductor status alone decides `unsupported`; `B_max` is an envelope flag.

### T-014 scope

- **Objective:** Focused independent check (STUDY_POLICY § 11; contract § 9) of the two derived field relations the contract uses: the Ampère floor on the peak field and the pack-size arm's three-point fit and re-anchoring.
- **Why now:** Both are single-author derivations that the study will evaluate on every case; the check must land before the study and is independent of the design.
- **Scope:** one evidence note by a fresh checker; corrections to the contract text if required. Excluded: any new derivation, model change or research capture.
- **Inputs:** briefs/t014-check-field-relations.md; sources/field-term.md; the registered Lion 2021, Lion 2023 and Stellaris PDFs.
- **Done when:** each relation has a verdict with reproduced numbers; corrections applied to the contract or the relation withdrawn.
- **Stop when:** a relation fails and the contract needs a replacement (report), or declared limit.

### T-014 start — 2026-09-30

T-014 · fresh checker on briefs/t014-check-field-relations.md · evidence/check-field-relations.md. Runs in parallel with the T-013 design draft.

### Owner instruction — 2026-09-30 — subagent model

[OWNER-VERBATIM] “continue, but use opus 5.5 for all subagent work”. The owner stopped the running T-013 design draft and T-014 check before either wrote a file. Both restart on Opus 5.5 (`model: opus`) with identical briefs, inputs, scope and meaning; every later worker, oracle author, executor and reviewer of this goal runs on Opus 5.5. Until this entry, subagents inherited the session model (Fable 5.1). Not a retry: neither stopped task produced an outcome.

### T-014 return — 2026-09-30

- **Outcome:** COMPLETE; both relations PASS WITH CORRECTIONS; contract r4 released with the corrections applied.
- **Evidence:** evidence/check-field-relations.md; evidence/plant-contract.md (r4, § 3.2 and § 7 marked `(C)`). Pinned at the commit that follows this entry.
- **Reading:** The Ampère floor is exact for any coil shape (the other coils cannot lower the mean tangential field around the pack), applies to the surface and interior peak alike, and reproduces on all six Stellaris Table 8 coils (13.44 T against 24.6 T at coil 0; 11.73 against 19.5 T at coil 5); it binds on the anchored and HELIAS-class cells at large R and small pack, never under the arm. The pack-arm fit reproduces (slope 0.0641, intercept 0.143, residuals ≤ 0.004; slope range 0.058–0.071 from table rounding, 0.034–0.095 formal); the three points are consistent with one Helias 5 coil set; the sign comes from the fitted slope, not the printed equation; the anchor is 35.278; the 25–40 flag band is an agent-chosen tolerance, not a fitted domain; the slope is [D] on Helias 5 and its transfer to Stellaris [U].
- **Decision:** A design whose modeled peak field lies below the floor has an impossible field that would favour small REBCO packs · new check `ampere_floor_ok`, filed `failed` (checker's recommendation) · execution detail · coordinator · contract r4 § 3.2, § 7.
- **MR-7:** No supplied quantity changes; the floor is a check on a calculated field.

### T-013 design draft — 2026-09-30 (interim)

- **Evidence:** work/active/WI-100_stellarator-material-variants/design.md (fresh modeler, Opus 5.5; to contract r4). Pinned at the commit that follows this entry.
- **Decision (placement):** The design's § 1.1 premise conflict: spec R5 (reference package byte-identical) and the audit/contract placement of the seam edits in the canonical library cannot both hold, because the twin rule (`tests/models/test_model_family_spines.py:291-304`) forces a regeneration of `stellarator_e2e`, which would change every sealed study's executable fingerprint · keep every seam edit inside the derived package's staged source copies as a recorded hunk set (15 hunks in 5 files plus 2 body copies, each value-neutral at the reference), canonical, twin and Stellaris design file untouched; port to canonical at the reference's next regeneration as a later work item · execution detail (isolation over canonical placement; the goal invariant asks for preserved behavior and additive isolated variants) · coordinator · spec R3/R5 amended; contract § 6 r4a note (CPI variant also covers the Green refrigerator capital).
- **Next:** fresh design review on briefs/t013-design-review.md, including the design's probe P1 (rebound cryoplant seams resolved by codegen when the consumer is in the plant definition) and the three-instance wording deviation (the reference is the staged Stellaris file itself).

### T-013 return — 2026-09-30

- **Outcome:** COMPLETE; WI-100 design reviewed and released for implementation.
- **Evidence:** work/active/WI-100_stellarator-material-variants/spec.md (R3/R5 amended), design.md (fresh modeler, Opus 5.5; corrections D1–D18 applied in place with a § 8 change list), evidence/design-review-wi100.md (fresh reviewer, Opus 5.5: PASS WITH CORRECTIONS, 9 corrections, 10 notes; `## Recheck` PASS WITH CORRECTIONS with R1–R2 on the probe-P1 fallbacks and notes R3–R6, all carried into the implementation and oracle briefs as binding amendments). Pinned at the commit that follows this entry.
- **Reading:** The design realizes the audit's seam inside the derived package's staged copies (15 value-neutral hunks in 5 files plus 2 body copies, plus the contingent H6 `winding_account` seam), with the reference instance being the staged unchanged Stellaris file and two material instances in a derived design file; five toolchain probes (P1 cross-part seam consumers, P2 double retype, P3 def-level literals as keys, P4 auto-implemented conditional calc, P5 per-case cost of three instances) run on scratch copies before implementation; the reviewer confirmed every plant binding, MR-7 compliance (no cycle, no output bound back, no demand-sizing) and a working precedent for retyping a sub-part in the pinned instance (`stellarator_plant.sysml:560`).
- **Decision:** The recheck's two fallback corrections and four notes apply only if probe P1 fails and to naming; they are carried as binding amendments in briefs/t015-implementer.md and t015-glue-oracle.md rather than a third design pass · execution detail · coordinator · the review's § Recheck.
- **Process note:** the design author made one scripted text edit with bare `python3` (nothing executed); recorded as reported.
- **MR-7:** Design § 4 role table reviewed: every policy-proposed quantity supplied and checked; `B_max` an envelope flag; the conductor status alone decides `unsupported`.

### T-015 scope

- **Objective:** Implement WI-100 (probes, package build, regression, route, tests, family registration) and, independently and in parallel, the glue oracle with its channel-ownership map and pure-oracle tests.
- **Why now:** The design is released; the two tracks are independent by construction (the oracle author reads design and contract only).
- **Scope:** implementer owns `exploration/stellarator_materials/` (except the oracle files), `tests/models/test_stellarator_materials.py`, `tests/model_families.py` (one addition), WI-100 `implementation-notes.md`, `build/`, `prototype/`; oracle author owns `exploration/stellarator_materials/oracle_glue.py`, `oracle-reuse.json`, `oracle-notes.md`, `tests/models/test_stellarator_materials_oracle.py`. Excluded: the offer policy and case declaration (next task, after the oracle), the seam run, the study.
- **Inputs:** design.md + review § Recheck; contract r4; briefs t015-implementer.md, t015-glue-oracle.md.
- **Done when:** probes deposited, package built with the reference bit-for-bit, tests pass, family registered; oracle written with tests passing and the ownership map complete; or a probe refusal the fallbacks cannot absorb is reported.
- **Stop when:** prerequisite, strategy blocker (a seam step infeasible), owner gate or declared limit.

### T-015 start — 2026-09-30

T-015 · implementer (Opus 5.5) on briefs/t015-implementer.md · glue-oracle author (Opus 5.5) on briefs/t015-glue-oracle.md · parallel; neither reads the other's files.

### T-015 interim — glue oracle returned — 2026-09-30

- **Evidence:** exploration/stellarator_materials/oracle_glue.py, oracle-reuse.json (generated map: per material ≈ 1,423 channels — plant 1,288, Round 1 57, glue 45, composed 33; 73 verdicts), oracle-notes.md (G1–G12), tests/models/test_stellarator_materials_oracle.py (23 passed). Pinned at the commit that follows this entry.
- **Reading:** The plant's `verify_stellaris.compute()` refuses every material instance (it always runs the plant REBCO law), so the oracle composes the plant chain from function-level pieces and re-derived equations; with the reference legs it matches `compute()` on all 1,362 outputs bit for bit, and at the REBCO bridge point all 1,288 plant-owned channels match. The D2 breakdown closes to 1.6e−16; the arm at slope 0 is identity; the Ampère floor at coil 0 is 13.44 T.
- **Decision:** G1 is a design defect (NIST `k_c` clashes with the inherited `Cryoplant::k_c`, giving 27.83 W instead of 590.28 W of conduction) · design § 9 amendments A1–A8 appended by the coordinator and relayed to the implementer · execution detail · coordinator · design.md § 9.

### T-016 scope

- **Objective:** The study's declared offer policy (contract § 5) and the case declaration, using the composite oracle as the evaluator; policy acceptance tests.
- **Why now:** The oracle exists; the policy is independent of the package build and takes the longest wall-clock of the remaining steps (order 10⁴ evaluations).
- **Scope:** `exploration/stellarator_materials/studies/{offer_policy.py, declare_cases.py, cases.json, policy-notes.md}`, `tests/study/test_stellarator_materials_policy.py`. Excluded: package files, seam, execution.
- **Inputs:** contract r4 §§ 3–8; design § 5, § 9; oracle_glue.py; briefs/t016-policy-cases.md.
- **Done when:** the case set covers the contract grid with counts by label near the estimate, the acceptance tests pass, and the notes list every ambiguity.
- **Stop when:** the oracle cannot evaluate a required region (report), owner gate or declared limit.

### T-016 start — 2026-09-30

T-016 · fresh policy author (Opus 5.5) on briefs/t016-policy-cases.md · runs in parallel with the T-015 implementer; reads only the oracle files and, when present, `studies/interface_data.py`.

### T-015 return — 2026-09-30

- **Outcome:** COMPLETE (implementer and oracle author both returned); one structural deviation recorded below.
- **Evidence:** `exploration/stellarator_materials/` (seams/seam_hunks.json with 15 hunks; models/ with the variants library and two material design files; bodies B1, B2 and the shape-branch fallback; build.py; regression.py; units/{reference,rebco,nb3sn}/ each with staged input_models, generated package, snapshot and census; studies/{study_route.py, prepare_interface.py, interface_data.py, reference|rebco/manifest.json, baselines}); tests/models/test_stellarator_materials.py (29 passed, 287 s); tests/model_families.py (one additive entry; spine 15 passed); WI-100 implementation-notes.md, prototype/ (P1–P5), build/ receipts (force-added, `_work/` excluded); the oracle files of the interim entry. Pinned at the commit that follows this entry.
- **Reading:** Probes: P1 passed on all five cross-part reads (H6 not applied); P2: the retypes work but codegen refuses a package holding two `'MFE Power Plant'` instances (`REGISTRY_CLASS_NAME_COLLISION`), so the K21 fallback applies: three units (reference, rebco, nb3sn) generated from one staged source set; P3: def-level literals are emitted as entry keys (the route refuses the two material ones); P4: the `if` form is refused, so the shape branch has a handwritten body; P5: ≈ 1.5 s per plant evaluation. Regression: the reference unit reproduces the pin bit for bit (1,352 outputs, 67 verdicts, identical ids) with the declared delta only (`evaluation_defined = 1.0`; keys `arm_slope` 0, `arm_x_ref` 0, `rebco_law_enabled` 1); 76,581 protected files unchanged; `git diff --stat` on the protected trees empty. Baseline LCOE at the manifest point: reference 318.7377 $/MWh (the pin); REBCO bridge 412.4334 $/MWh (Green cryo chain and the supplied count at 80 USD2021/m of 4 mm tape replacing the plant's composition-implied 6 mm tape at 20 $/m; the basis bridge by account is the study's first report); Nb₃Sn at the Stellaris plasma refuses (`nonpositive IHX terminal approach`, design K22), so no Nb₃Sn manifest baseline exists until the policy records an evaluable design. Test 4(d) bridge parity: 1,266 channels bit for bit. A1 confirmed (staged conduction 590.28 W). At the REBCO bridge, `pack_area_ok` fails by 0.35 mm² per turn: the 0.991 `f_set/f_wp_vol` factor, reported not absorbed (A6).
- **Decision:** Three executable units from one staged source tree instead of one package · accepted as the design's reviewed K21 fallback; for the round's "one promoted pin" bound the pin is the staged source set with its three unit fingerprints, all issued by one seam run and recorded together in the study manifest and record § 11/§ 16 · execution detail (toolchain limit) · coordinator · implementation-notes.md deviation 1; the seam task that follows.
- **Decision:** `tests/model_families.py` registers only canonical paths (the two new SysML files live outside `models/` by the placement ruling and would fail gate 5 if registered) · accepted; if the seam's gate 5 refuses the package-local sources, that is the next task's finding · execution detail · coordinator · implementation-notes.md deviation 9.
- **MR-7:** Test evidence: insufficient/sufficient supplied designs for acceptance, pack area, fit, capacity and floor pass and fail as designed; unsupported cases carry status only; no supplied quantity is written by any calculation; the arm at slope 0 is identity.

### T-016 interim — policy returned with premise conflicts — 2026-09-30

- **Evidence:** exploration/stellarator_materials/studies/{offer_policy.py, declare_cases.py, policy-notes.md (Q1–Q30)}, tests/study/test_stellarator_materials_policy.py (11 passed; a 27-case sample re-evaluated without the policy reproduces recorded values to 1e−9; matched power within 2e−4; all 210 equal-duty pairs share ampere-turns exactly); `cases.json` (2,909 cases: 885 recorded designs = 693 grid + 43 companions + 149 variants; 43,350 oracle evaluations, 26,788 plasma solves). First-pass statuses under r4: 190 supported, 626 failed, 52 ignited, 13 capacity-limited, 4 unsupported; **at f_ren 1.0 no design was supported in any geometry, the reference cell included.**
- **Reading:** That result followed from two contract defects and one model fact, not from the materials: (Q1) the r4 ladder wording "lowest temperature meeting the bounds" selected the highest-heating operating point because installed heating is re-supplied above the requirement (229 MW at 11 keV against 52.7 MW at 14.63 keV at the reference design); (Q5) the asserted `divertor_heat_ok` reads the source-anchored unscaled `q_target_peak` (the R-scaled channel is an unasserted shadow, no source supports the scaling, `stellarator_plant.sysml:1143-1144`), so at matched fusion power it passes only when `p_aux_required` ≤ 21.8 MW at every size and the published reference (49 MW) fails it; (Q13/Q14) the maintenance-schedule resources and the IHX exchanger count are screened but were not on the re-supply list.
- **Decision:** contract r5 (P): the ladder rule selects the least-required-heating ladder value meeting the bounds; `divertor_heat_ok` is carried like `tbr_ok` (open plant gap, margin reported, `divertor_pass` column and the divertor-passing subset reported per cell); the IHX count and the schedule resources join the re-supplied set with stated rules · the policy re-runs only its selection and re-supply pass from the recorded traces; the r1 reviewer rechecks r5 in parallel · execution detail with a status-rule change disclosed for recheck · coordinator · plant-contract.md r5; policy-notes.md Q1, Q5, Q13, Q14.
- **Model finding to register at the study:** the divertor screen cannot respond to plant size by the model's own statement (unasserted R-scaled shadow); a sourced divertor-geometry relation is a model repair candidate.

### T-016 return — 2026-09-30

- **Outcome:** COMPLETE (re-run under contract r5).
- **Evidence:** exploration/stellarator_materials/studies/{offer_policy.py, declare_cases.py, policy-notes.md (Q1–Q30 and "Re-run under r5")}, tests/study/test_stellarator_materials_policy.py (13 passed); `cases.json` (2,921 cases from 889 recorded designs: 736 first-pass and 153 variants; gitignored at `.gitignore:104`; sha256 `f07133acdd561610287ff9dea01f641bf48b1562ec417254c85484ea8645e583`, 63 MB; regenerates from declare_cases.py); 51,413 oracle evaluations spent in all. Pinned at the commit that follows this entry.
- **Reading:** Under r5, 194 of the 229 matched first-pass designs moved to 13–18 keV and none stays at 11 keV; the IHX count runs 1–16 with 69 designs needing 15 or 16, and the cooling hall, spare positions and annex depths follow it, so no design fails the IHX or facility checks. Statuses over all recorded designs: 348 supported, 472 failed, 56 ignited, 9 capacity-limited, 4 unsupported (r4: 190/626); 555 designs pass the divertor screen and 233 are both supported and divertor-passing. At f_ren 1.0, 53 first-pass designs are supported (8 divertor-passing) and **every Nb₃Sn design in the reference cell fails `recirc_ok` (28 of 28) and most also `net_positive` (23)**: at 4.3–4.7 T on axis with the Stellaris confinement the heating draw exceeds the plant's recirculation limit. Failed-check tallies: `recirc_ok` 359, `net_positive` 215, `ampere_floor_ok` 83, `wall_load_ok` 74, `wp_stress_ok` 17. Data-driven placements: structure-mass variants on helias × 1.0 and × 1.8; common-P on arm × 1.4 at 12 T; `k_link` and 86 kA on helias × 1.4 at 18 T.
- **Decision:** The annex re-supply splits the facility's published required width into north and south depths by copying three lines of the facility oracle's arithmetic, checked against the oracle's published sum on every pass · accepted as policy glue, disclosed for the executor's verification (the recorded designs are re-evaluated without the policy) · execution detail · coordinator · policy-notes.md "Re-run under r5".
- **MR-7:** Every policy-proposed quantity is a supplied input in `cases.json`; the acceptance tests re-evaluate recorded designs without the policy (matched power within 2e−4; peak field within −0.044/+0.098 T); every insufficient offer fails and every generous offer passes.

### T-017 scope

- **Objective:** Prepare, integrate (three unit pins from one staged source set), execute and verify the Round 2 native study `20260930-magnet-material-plant-map` over the declared case set; register findings; seal.
- **Why now:** Package, oracle, policy and contract r5 are all in place.
- **Scope:** the record directory, `studies/ANNEX.md`, `studies/DISCOVERY_LOG.md`, `evidence/integration-r3-{reference,rebco,nb3sn}/`. Excluded: any change to units, oracle, policy, cases or models; the reading and report (next task).
- **Inputs:** briefs/t017-study-execute.md; contract r5; design § 5, § 9; implementation-notes.md; policy-notes.md.
- **Done when:** three CANDIDATE pins recorded, every case executed and verified against the oracle with policy acceptance on recorded designs, findings registered, snapshot resolved; or a named blocker.
- **Stop when:** BLOCKER, verification disagreement, prerequisite, owner gate or declared limit.

### T-017 start — 2026-09-30

T-017 · fresh study executor (Opus 5.5) on briefs/t017-study-execute.md · record `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/`.

### T-017 interim — Nb₃Sn seam BLOCKER at gate 8 — 2026-09-30

- **Evidence:** record `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/` (record.md §§ 1–2, 7–11, 14–15 drafted; `results/tolerance_diagnostic.json`, `results/oracle_scan_summary.json`; per-unit manifests, axes and indicator reports); `evidence/integration-r3-reference/` CANDIDATE (10/10 gates, pin `4229205b…59fc`), `integration-r3-rebco/` CANDIDATE (10/10, pin `f3884b47…6e75`), `integration-r3-nb3sn/` BLOCKER at gate 8 `verification-refused` (gates 1a–7 pass). Pinned at the commit that follows this entry.
- **Reading:** The Nb₃Sn package and the oracle disagree on one channel pair (`acceptance_margin` and its alias `temp_rule_margin`) by relative 5.56e−9 against the 1e−9 relative clause, absolute 1.28e−11 K (worst 4.24e−11 K on a 33-case sample); `T_cs` agrees to 6.3e−12 K, every verdict matches, all REBCO channels agree. Cause: the policy sizes the margin at allowance (≈ 1e−3 K), so the package's 1e−10 K Tcs bisection tolerance shows as ≈ 1e−8 relative. Round 1's contract carried the absolute clause for this case; r5 § 9 omitted it. The oracle scan of all 2,921 cases before execution: failed 1,638, supported 1,081, ignited 175, capacity-limited 23, unsupported 4; Nb₃Sn 806 (289 supported), REBCO 2,115 (792 supported); anchored × 1.0 has no supported Nb₃Sn design (0 of 135); the 736 first-pass designs reproduce the policy's counts.
- **Decision:** Restore Round 1's tolerance clause (relative 1e−9 or absolute 1e−9 per unit, whichever is looser) in contract § 9 as r5a and in the record manifests; re-run the Nb₃Sn seam; then execute · a verification-clause omission, not a model or oracle defect (the package's own stated bisection tolerance bounds the deviation ten times below the clause) · execution detail · coordinator · plant-contract.md r5a; the executor's re-run.
- **Executor deviations accepted:** indicators run through a record-local alias shim (codegen lower-cases two UA capacity-check module names; the shim cannot change the trace); per-unit axes files (preflight validates against one package); an added `conductor-assumptions` group for the Nb₃Sn strain; per-unit oracle modules imported by dotted name; Nb₃Sn cases' `magnet__eps_min` (a package constant the route refuses) dropped after an equality check; the executor's contract § 7 status derivation supersedes the policy's `failed` label on 133 re-evaluations of ignited or capacity-limited designs. Six process findings registered (#1–#6).

### Resume — 2026-10-04

[OWNER] Requested `$run-goal` to continue this work and instructed: “Make sure you only use uv run --no-sync”. This runtime instruction supersedes the prior launcher wording for this continuation. Runtime inspection with `uv run --no-sync` resolves the existing `.venv` interpreter and the editable `/home/reid/1cfe/agentic-mbse/src/agentic_mbse/__init__.py`; the existing integration environment and TEAx import path are retained without synchronization.

[AGENT] Round 2 remains open; T-017 is the only started task with no return. No matching study worker is running. Native evidence in the untracked study record and integration receipts shows execution, full numerical verification, policy acceptance and all three CANDIDATE returns completed after r5a; `snapshot.json` is absent and record § 16 retains its placeholder. Resume T-017 at snapshot resolution and evidence validation, preserving completed execution artifacts. The original goal invariants, contract r5a, case-set identity, reviewed source/model basis, no-push/no-merge boundary and owner-held formal closure remain applicable. The 2026-09-30 instruction assigning all subagent work to Opus 5.5 remains in force.

### T-017 return — 2026-10-04

- **Outcome:** COMPLETE for execution, numerical verification and snapshot resolution; substantive independent integration/interpretation review remains the next task's required coverage.
- **Evidence:** `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/record.md` §§ 3–4, 11, 13, 15–17; `snapshot.json` at `d494d0e92768ff6ed2498c32f9d24fc1cee9e8562cf863e269f92a01eed46de7`; all three `evidence/integration-r3-*/integration_return.json`; `evidence/resume-validation.json` (coordinator hash, pin, case-count and finding-join checks). Sealed by the coordinator at the commit following this entry.
- **Reading:** The native deposit resolves the initial numerical refusal without changing models, cases or the oracle. Independent comparison excludes constants and the two static-load channels without oracle legs; the record's opening and verification paragraph now say that explicitly. The study's conditional ranking is available for interpretation, but its evidence-labelled map, interactions, figures and final assurance remain absent. No physical plant qualification follows from numerical agreement.
- **MR-7:** Existing declared offers remain supplied inputs; completed policy acceptance and preservation evidence is reused within its original scope. No design or calculation ownership changed during this resume.

### Review availability — 2026-10-04

[AGENT] A fresh read-only Opus review was attempted with `evidence/briefs/t017-resume-audit.md`, preserving the earlier owner model instruction. The sandboxed CLI produced no outcome and was interrupted; an escalation to permit the external review was rejected by automatic approval review because it could export repository contents to an unapproved destination. No reviewer verdict exists. The owner has been asked to permit a fresh Codex reviewer, explicitly approve the external review, or retain an Opus review handoff. Independent local reporting may proceed; dependent scientific follow-up and final round assurance remain parked pending required review.
