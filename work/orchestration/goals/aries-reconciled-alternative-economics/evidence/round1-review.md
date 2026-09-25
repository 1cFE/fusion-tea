# Round 1 review — `aries-reconciled-alternative-economics` (fresh non-author reviewer, 2026-09-25)

**Verdict: `FINDINGS`** — one correct-before-use, six notes, no owner gate. The round did what it declared, the numbers in `answer.md` are the sealed study's, nothing was tuned toward 77.6, and the answer is honest about what it could not price. The corrections are wording and labelling; no re-execution and no round 2 are needed.

## 1. Native evidence by citation (checked)

Confirmed against `results/cases.json` raw channels (prefix `aries_integrated_plant__`) for `alt-canonical-*`: `cost_ledger__evaluate__overnight` 4,359,271,605.16; `lifecycle_accounts__evaluate__financed_capital` 5,046,401,791.92; `generator_auxiliaries__evaluate__net_electric` 891.0017; `lifecycle_accounts__evaluate__capital_lcoe` 44.329. Confirmed against `results/attribution.json` (script-generated from that file): LCOE 685.695 and 238.028; tritium contribution 627.323 (91.5 %); baseline deltas −433.713 and +61.342; ladder combined 59.313 (branch 53.058); L7 at 8 % 84.687; capital-scope effect +0.267 (`branch_reads`); denominator effect −6.491 = 59.549 − 53.058; sensitivities `sens-tritium-price-1e+08-no-credit` +1474.637, `sens-cycle-side-2.0` +9.332 (overnight +894.4 MUSD in raw), `sens-pbli-pump-30MW-feed100` +8.291 (raw net 861.013), `sens-availability-0.75-feed100` −51.843. Hand arithmetic holds: direct 2,619.603 + 300 + 6.083 = 2,925.686; × 1.49 = 4,359.27; IDC 1.05³ − 1 = 0.1576; 891.0017 × 8760 × 0.85 = 6,634,398 MWh.

`verification_summary.json`: outcome `pass`, `sampled_rows` 64, 364 channels, 14 verdicts re-derived, identity `f739dbce…` matches preflight; the reported worst relative deviation 8.29e+03 is `residual_magnitude` at 7.5e-9 MW, inside its reviewed 1e-7 MW absolute allowance (record § 13 names it). `attempt-comparison.json` `identical: true` (35,264 channels, 0 differing). `replay-alternative.json` `passed: true`.

## 2–3. Strategy fidelity and task scopes

The round ran the declared sequence (replay, fresh audit, interim checks, one committed study with a fresh pre-execution review r1 FINDINGS → r2 PASS, answer with delivery checks). The 64 case names are `alt-`, `baseline-`, `original-`, `adverse-`, `sens-`, `diag-` only; every published substitution is a `diag-*` case or the separately labelled branch column; the only 77.6-derived input (L3 O&M) is labelled target-derived on every rung inheriting it. Task returns stay inside their scopes; the one deviation (live manifest amended) is recorded in the T-004 return and in `answer.md` § 13. `findings-log.md` and `answer-draft.md` sit outside any task scope but the owner brief asks for the log; trivial.

## 4. Retry classification (note)

Task, inputs and meaning were identical (`input_maps_differing: 0`; outputs bit-identical). Scope was not: the retry amended the live manifest, which the T-004 scope excluded. The attempt-1 entry says "scope identical" and in the same sentence records the deviation; amend the trail wording. The fix is mechanical: the fresh review confirmed the float64-versus-Decimal mechanism by reading the code, the allowance (1e-9 kg/year) is five orders above the class bound and no verdict reads the channels. One caution: `goal.md` § Reserved gates lists declared numerical tolerances as `[OWNER]`. This was a new allowance for a channel class the relative rule cannot pass, not a relaxation to accept an economic result, and § 13 surfaces it; the owner should ratify it explicitly at closure.

## 5–6. Discovery rows and liveness (pass)

`DISCOVERY_LOG.md` lines 326–336 carry `…economics#1`–`#11`; record § 15 gives each a disposition and a home; none `unrouted`. `git log 352ecee4..HEAD -- exploration/aries_integrated/aries_integrated models` is empty; the last package commit `49668453` is an ancestor of `352ecee4`. Live manifest fingerprints (`f739dbce…`, `78dd23bf…`, indicator digest `06e0627c…`) equal the snapshot's and `manifest_used.json`.

## 7. MR-7 — compliant for this round's scope (one note)

`configuration-record.md` § 3–4 and record § 4: every rating is a supplied input, the 14 checks read calculated demand, and the two adverse controls remain `violated` (−67.033 MW; −98 kg/s) with no resize. Note: the T-002 decision says the demand-matched pump capacities are "disclosed in `configuration-record.md` § 3 and the study record", but § 3 only tabulates 3359/27,666 with ratios and § 4 shows margin 0.000 without saying why; record.md line 84 says "declared mapping value". The explicit "supplied choice equal to the operating flow" sentence exists only in `answer.md` § 2/§ 8 and the trail. Disclosure is made; the citation is wrong. Add one sentence to the configuration record or amend the trail.

## 8. Learning delta

- L-001 accept. L-004 accept. L-005 accept.
- L-002 correct: add "with the three bounded costs excluded from the aligned case" — their upper values would lift the "ours" band by up to ≈ +16 USD/MWh.
- L-003 correct (see the finding below): the cycle-side allowances do have a purchase (fixed), only no response, rating or screen; and the PbLi figure +8.3 is on the feed100 base.
- L-006 correct: +0.7 and +1.5 are two applicability points, not a bound; the E8 low end (2 FPY) gives +2.817.

## 9. Completion honesty (note)

"Met as a conditional assessment" is honest in substance but is a fourth state; the brief allows met, partially answered or unmet. The three bounded costs do not prevent a useful comparison: the aligned residual is already a rate band 73 USD/MWh wide, and the bounds (+4.9, +9.3 capital; ≈ +2.1 denominator on the aligned base) sit inside it without moving the conclusion that the gap is fuel treatment plus an unprinted rate. State "met" and list the four conditions.

## Finding — correct before use

**PbLi pumping bound overstated for the aligned comparison.** `sens-pbli-pump-30MW-feed100` adds no overnight; its +8.291 is exactly the denominator ratio on the feed100 base (246.319 / 238.028 = 891.0017 / 861.0126). On the aligned 59.313 base the same −29.989 MW is ≈ +2.07, and on the branch (supplied 1000 MW denominator) ≈ 0. `answer.md` § 1, § 5, § 6, § 7 and the trail present +8.291 as the bound "material against 77.6". Still material (≥ 1.0) but four times smaller. Restate the figure by base in § 5–7 and in L-003.

## 10. Constraints and round 2

Carry forward as listed in the round result. No round 2 is needed: the corrections are edits to `answer.md`, `learnings.md` and a trail amendment.

## Not checked; remaining uncertainty

Did not execute the package, oracle or verifier; did not view the Lyon page images (relied on the pre-execution review); did not re-derive the branch's +0.267 capital-scope arithmetic; did not read the prior goal beyond cited paths. Not verified: the 8.29e+03 worst deviation is the only absolute-tolerance channel above the relative rule (the summary reports one `worst_at`).

fresh round reviewer, 2026-09-25, 15 tool calls
