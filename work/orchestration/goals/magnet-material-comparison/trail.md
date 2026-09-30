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
