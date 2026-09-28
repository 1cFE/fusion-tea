# Source-check review — contract, Q1 and materiality budget

Verdict: **FINDINGS** (none blocking; three correct-before-use).

All eight images viewed. Every `[SOURCE]`/`[SOURCE-FIG]` value in contract sections 2–4 reads as stated: Lyon Table IV, p703 text, Fig. 18, p717, Raffray Tables II/III/V, Fig. 12 topology, Fig. 13. Qualifications follow.

## Findings

1. Lyon p708 items 170 + 27 + 55 sum to 252; the text prints "Part (253 MW)". Contract and brief write "= 253". The contract's `[DERIVED]` 1000.9 uses 0.43 × 2916, not the printed 1253 − 253 = 1000. Note. Record 253 as printed, 252 as itemised.
2. Two citations fall outside the evidence set: 1.16 to Lyon Fig. 5 (p708 text prints it; cite that) and P_input = 0 to Lyon p707 (unverified; missing evidence, not a contradiction). Note.
3. Lyon p717's "50 MW ... balance of plant ... 5 MW for cryogenic cooling" sits in the LiPb/SiC alternative-blanket paragraph. Applying it to the reference 55 MW is an inference; the total matches. Note; grade `[DERIVED]`.
4. Raffray "2365 MW" is the Fig. 14 plot inset; the caption prints "2.36 GW". Note.
5. Raffray Table V items (23.6 + 23.6 + 48 + 24 = 119.2 MW) do not sum to the printed 186 MW; ≈ 67 MW is unlabelled, presumably neutron heating. Correct-before-use for any divertor-branch comparison; list as a bounded item.
6. Q1's C = 2916/352 blends Lyon thermal power with Raffray's span (Raffray's own: 8.0 MW/K), and "≈ 820 MW" assumes ε ≈ 0.98; Table III's printed 30 °C approach gives ≈ 590 MW. Note; conclusion unchanged.
7. Budget, turbine inlet ±5 K: rationale inverted. If Fig. 12 disagrees with Table II by up to 13 K, ±5 K over-reads the figure. Anchor to printed values: 738 °C (Table II) − 30 °C (Table III) = 708 °C; then ±5 K is defensible. Correct-before-use.
8. Budget, per-circuit ±10 MW: asserted, not derived. Scaling ×1.030 moves He by ≈ 36 MW, and the 141 MW friction term does not scale linearly; the choice of rule for it alone moves He by ≈ 10 MW. State the rule and derive the budget. Correct-before-use.
9. Budget, net/gross ±15 MW: Table IV pins 1253 and 1000 to the MW and 0.43 × 2916 reproduces 1253 within 1 MW, so the source supports ≈ ±2 MW. ±15 MW is a purpose-driven attribution resolution; say so. Note.

## Q1

The claim follows from the pages, more strongly than the contract states. Table II fixes blanket He at 386 → 456 °C carrying 1192 MW (42% of Raffray's 2822 MW); Fig. 12 draws the whole cycle flow through that exchanger first, entering at 355 °C; Table III fixes a 30 °C approach. In one series stream, heat fractions must match temperature-span fractions: the blanket stage can span at most 426 − 355 = 71 K of the 352 K rise (20%), so no cycle flow rate works (blanket stage needs ≥ 16.8 MW/K, the rest ≤ 5.8 MW/K). Temperatures, duties and arrangement cannot all hold, independent of the 8.3 MW/K estimate. The 90% and 43% are correctly characterised: Lyon p703 and Fig. 18 state them as fixed percentages and no viewed page contains an exchanger calculation; Raffray's 0.43 is a cycle-optimisation output (p737 text, Table III) where exchangers appear only as a 30 °C approach parameter.

## Budget

Net, gross, thermal and unmet-heat budgets are acceptable lines for explaining a 204 MW gap, and the thermal-composition ambiguity is rightly a bounded item, not tolerance. Turbine inlet (finding 7) and per-circuit heat (finding 8) are not yet justified by what the pages print, and the divertor ambiguity (finding 5) is missing from the bounded list. With those corrected, a tired engineer would accept the table.

— fresh source-check reviewer, 2026-09-25

## Recheck r2 — 2026-09-25

Verdict: **FINDINGS** (one correct-before-use; rest notes). Page images from r1 reused, not re-read.

**Corrective diff.** All r1 findings 1–9 are addressed by `[r1]` edits. Finding 2 stays partly open by disclosure: P_input = 0 still rests on a text extraction (p707, `page-13.md`), not a viewed image.

1. Contract § 8, blanket shortfall: the inherited 385.4 MW includes 20 MW deposited auxiliary heat that the corrected setting removes, so the blanket circuits receive ≈ 198 MW too little (2580.7 − 2382.4), not ≈ 218; 218 is the divertor excess only. Correct-before-use.
2. § 8 reading is otherwise fair and confirmed: Table IV 462/365/97.0/98.1; Fig. 18 89%/11%; Table V 186 − 119.2 = 66.8 → 68.8 MW; f_rad = 1 − 167/487.2 = 0.657; 111/2365 = 0.0469; carried approximation stated. Cross-check worth recording: Raffray's plasma-side divertor items 23.6 + 23.6 + 48 = 95.2 MW × 1.030 = 98.1 MW, matching Lyon exactly, so 98.1 includes alpha loss. Note.
3. § 8 cites "P_div ≈ 0.1 P_α" to Fig. 18; it is p704 text. Note.
4. Budget per-circuit derivation: the He-circuit items listed (1 + 1 + 3.3 + 4.2) sum to ≈ 9.5 MW, not ≈ 5; the ±10 MW line holds with little margin. Note.
5. Study input 1600 kg/s: arithmetic right (2916e6/(352 × 5193) = 1595). The 352 K span is a `[SOURCE-FIG]` Raffray value used in a Lyon case, so under the contract's § 1 rule the grade should carry the figure inheritance and cross-source mark. The 1500–2000 bracket makes this harmless to the study. Note.
6. Study input 283 kg/s: correctly `[SOURCE]` (Table V). It is a 2365 MW value held fixed at 2436 MW; mark that convention where used. Note.

— fresh source-check reviewer, 2026-09-25

## Recheck r3 — 2026-09-25

Verdict: **PASS**.

All r2 items are addressed by `[r2]` edits:

1. P_input = 0: `lyon-p707.png` viewed once; the page prints "an ignited plasma (P_input = 0), P_electric = 1 GW" (§ VII opening). `[SOURCE]` now image-verified. Closed.
2. Cycle flow: § 5 grades 1595/1600 kg/s `[DERIVED, cross-source]` over the `[SOURCE-FIG]` 352 K span, bracketed 1500–2000. Closed.
3. Divertor flow: § 4 states 283 kg/s is a 2365 MW value held fixed at 2436 MW. Closed.
4. § 8: divertor excess ≈ 218 MW, blanket shortfall ≈ 198 MW (2580.7 − 2382.4), difference explained as the 20 MW auxiliary-heat item. Closed.
5. § 8: P_div ≈ 0.1 P_α cited to p704 text; 95.2 × 1.030 = 98.1 cross-check recorded `[DERIVED, r2]`. Closed.
6. Budget: helium items ≈ 9.5 MW, PbLi ≈ 5.3 MW, with the ±10 MW line stated as purpose-driven. Closed.

No new findings.

— fresh source-check reviewer, 2026-09-25
