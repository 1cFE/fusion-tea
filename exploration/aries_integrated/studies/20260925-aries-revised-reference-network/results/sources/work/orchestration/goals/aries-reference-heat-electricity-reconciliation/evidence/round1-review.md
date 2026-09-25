# Round 1 review — fresh reviewer

**Verdict: FINDINGS** (none blocking).

1. **Native evidence — PASS.** `cases.json`: `nominal-source-assumed` net 796.005, pbli_unmet 158.726, he/divertor 0; `oat-cycle-flow-1600` unmet 0, net 773.518; `combined-c3-partition` net 842.732, unmet 151.002; `c3-minus-recuperator` net 759.886, unmet 0; `c3-cycle-flow-1800` net 803.563, unmet 0; largest gross 1128.379. `attribution.md`: the five C3-path forward deltas (+11.011, −22.487, −1.605, −18.334, −13.650) sum to −45.065 against combined +46.727. `sha256sum snapshot.json` = `dae3a465…dba78`, matching record § 16. `verification_summary.json`: `verdict_mismatches: []`.
2. **Goal and strategy fidelity — PASS.** No model or package change (snapshot `git_clean: true` at `52e01b48`); one study, no promotion; original case stored verbatim with the frozen numbers; nothing tuned toward 1000 MW.
3. **Task scopes — FINDING (minor drift).** T-001 to T-003 in scope. T-004's scope declared 21 points; 27 ran after the source check added the partition axes, and no dated trail amendment records the point-count change. The native baseline point ran at T-004 start, before the T-003 review returned; T-003's "no study execution before the review" holds for the 27 declared points only.
4. **Retries — PASS.** None. The contract and budget went r1 to r3 (two revisions) under T-002/T-003's own done-when; if the owner counts reviewer-driven revisions as checkpoint revisions, the cap of 2 was reached, not "untouched".
5. **Discovery rows — PASS.** Rows #1–#10 at `DISCOVERY_LOG.md:280–289`; dispositions identical to record § 15; none unrouted.
6. **Reading and dispositions — PASS.** "All unremoved heat is in the PbLi stage" is true for the original (he 0, divertor 0, pbli 158.726) and for C3 (he 0, divertor 0, pbli 151.002); not for C2 (divertor_unmet 12.747). Routing #7 to a topology increment is justified: no source-supported input set removes the heat with every check satisfied. It is not the only remedy on this package: 0.8 recuperation at 1600 kg/s, or 0.95 at 1800 kg/s (A6 rating exceeded; A6 is an assumption, not a source value), both reach unmet 0. Finding #7's "after every input-level correction" should read "after every source-supported correction at the 1600 kg/s convention".
7. **Learning delta.** L-001 accept. L-002 accept (1700 kg/s leaves 16.3 MW, 1800 removes all; 0.8/1600 efficiency 0.345–0.346). L-003 accept as a source-reading claim conditioned on the owner's Q1 gate; scientific truth not assessed here. L-004 accept with a note: the 218/198 MW deposition figures trace to the contract, not this study, which confirms only the partition's effect (Δnet −13.650, PbLi unmet 177.693).
8. **Budget discipline — PASS.** Declared and reviewed before execution; residuals outside it (net −157, He +25) are carried as unresolved or bounded, not absorbed.
9. **Overstated claims.** (a) Ledger net "842.727" is a transcription slip; cases give 842.732. (b) Ledger "removable only at 0.8 recuperation with 1600 kg/s" overstates: removable with all checks satisfied only there. (c) PbLi floor quoted as ≈ 499 °C (T-001) and ≈ 475 °C (finding #7); temperature channels not verified.

**Remaining uncertainty.** Temperature channels not read; Q1's source truth outside this brief.

**Recommendation.** Do not close; open round 2 on the parallel PbLi/divertor topology increment after MR-7 design review, correcting the ledger items above first.

— fresh round-1 reviewer, 2026-09-25
