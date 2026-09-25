# Round 3 review — fresh reviewer

Reviewed at repository HEAD `77098a41`; nothing run; 15 tool calls.

**Verdict: FINDINGS.** No blocking item; four correct-before-use items (wording and bookkeeping). No stored result or stated modeling intent changes; no owner gate beyond the Q1 research decision § 13 names.

## Checks

1. **Owner framing — FINDING (F1, F4).** Statements in `answer.md` § 1, § 5, § 6, the ledger and contract § 6a stay inside the review's three limits. One § 12 sentence leans across: "the published 43% efficiency needs turbine inlet gas at 708 °C, and the published heat sources cannot deliver it, however the exchangers are arranged". The review's subject is the printed per-branch description, not the sources; § 12's last sentence retracts it. All restatements say "Fig. 13's inset"; the review § (a) puts the inset in Fig. 12 (p736).
2. **Reporting details — PASS.** The split (53.514 / 56.362) accompanies the 110 MW figure in § 1, § 3 and the ledger table; 891.003 is "best tested steady case, not an upper bound" in § 1, § 5 and the ledger. Note: § 5 row 1, the ledger status bullet and § 12 name mechanism 2 as the helium-stage bound alone.
3. **Native evidence — PASS.** `cases.json`: scaledflows unmet 95.681 (he 73.604, pbli 22.077), net 892.449; pbli-only 95.940; 1650 unmet 42.715, `heat_removal_ok` violated; both 1700 cases 14/14 satisfied, net 891.003 / 891.002. `verification_summary.json`: outcome `pass`, 12/12 cases, `sampled_rows` 12, 364 channels, 14 constraints, 0 mismatches.
4. **Study fidelity / MR-7 — PASS.** `config.json` designs 4–11 declare 3359 / 27,666 / 291.5 kg/s and capacities 3359 / 27,666, bases "scaled by 1.030 with the duty … never derived from demand"; 1650/1700 flows and ratings declared. No 1000 in `config.json` (`reference_net = 1000` is an inherited input in every case). Identity matches preflight, `git_clean` true; one study.
5. **Scope and count — FINDING (F3).** T-001 in scope (contract § 6a addendum unlisted, small). T-002: the scope names nine cases and says eleven; the amendment reaches twelve by adding C1 and C2, which makes thirteen; `network-c3-scaledflows-0.90` is named nowhere.
6. **Migration — PASS.** Stored channels: `he_unmet` 53.514 → 73.604 (+20.091), `pbli_unmet` 56.362 → 22.077 (−34.285), total −14.195; pbli-only +21.423 / −35.360.
7. **Learning delta** — rulings below.
8. **Discovery rows — PASS.** `DISCOVERY_LOG.md` lines 318–321; dispositions match record § 15; each routed.
9. **Unsupported claims — FINDING (F2, F5).**

## Findings

- **F1 (correct-before-use):** inset attributed to Fig. 13 in the trail T-001 return, contract § 6a, ledger, answer § 1 and L-010; the review says Fig. 12. Verify on `raffray-p736.png`.
- **F2 (correct-before-use):** stale `answer.md` text: § 5 row 1 "the threshold between them was not bracketed" contradicts § 3 and the ledger (1650–1700); § 5 row 5 "under investigation in round 3" and § 13 "stay open until the Q1 investigation returns" predate the return.
- **F3 (correct-before-use):** T-002 point-count amendment does not reconcile (check 5).
- **F4 (correct-before-use):** the § 12 sentence in check 1; say "the heat sources as printed".
- **F5 (note):** trail T-001 return says "three notes"; the review has one. Contract § 6a cites "reviewer note 5", which does not exist. Ledger row 2 "Which of the two the ARIES design used" is ambiguous.

## Learning rulings

- **L-010: accept**, with F1 applied and "≥ 11.8 MW/K at zero approach (16.8 at 30 °C)".
- **L-011: accept**; qualify "no steady result changes" as "unchanged to 1e-3 MW".
- **L-012: accept**; evidenced by check 6.

## Not covered

Page images; the review's physics; `learnings.md`; package diff; logs; cost channels.

— fresh round-3 reviewer, 2026-09-25
