# Source-check review — reading of Raffray's Ref. 15

Reviewed at HEAD `6b40a8d3`. Read: the brief, `ref15-reading.md`, `output.md`, `raw.pdf` (5 pp.), the three named page images, Raffray p736/p737, `owner-supplement-r4.md`. Nothing run.

**Verdict: FINDINGS.** The core answer is right: the source's only heat-source representation is the Fig. 1 boundary label, Tin is an input, Tout is dependent, and no per-branch exchanger, duty, temperature or terminal difference appears in the five pages. Five items need correction before use.

- Check 1 (quotes): faithful except one misquote (F1) and one gloss that adds meaning (F4). The parameter-list "quote" is condensed, drops the η symbols, and spans pp. 1–2, not p. 2.
- Check 2 (absence): holds. "exchanger" ×6 (fossil primary HX p1; Fig. 1 label p2; IHX p2; recuperator materials p4; porous-media recuperator p5; IHX in conclusion p5); "blanket" ×1 (Ref. [4] title only); "duty" ×2 (recuperator, p4); "divertor", "approach", "pinch", "ΔT" ×0 (only ΔP). Eq. (2), p2, has no heat-source term. Nothing contradicts.
- Check 3 (mapping): "exactly" is wrong and 738 should be 737 (F2, F3). The inference is tagged `[DERIVED]` correctly but the prose states it as a conclusion.
- Check 4 (§ 3): "supported at the methodology level" holds for the method only; attaching it to the Fig. 12 inset overreaches (F5). "Does not resolve" is the right bounded result and uses the owner's wording.

## Findings

1. correct-before-use — "four expressions derived for the cycle shown in Fig. 1" is an extraction artifact. Page 2 has two equations, (1)–(2); the "4" is the superscript citation to Ref. [4], Malang, Schnauder, Tillack, Fusion Eng. Des. 39–40 (1998) 561, a liquid-metal-blanket plus gas-turbine coupling paper. Fix the quote; record Ref. [4] as the expressions' origin and a lead on the goal's actual question.
2. correct-before-use — Table 1 (p2) lists Tin, ε_rec, Pout, η_T,ad, η_C,ad, ΔP/Pout. Table III omits Tin and adds "HX temperature difference 30 °C" and stage counts. That row is a terminal-difference specification the cited method lacks. Say "all of Table 1 except Tin, which Table III replaces by an HX ΔT".
3. correct-before-use — the inset reads 737 °C, and the same sentence says 737; 737 − 30 = 707 exactly. Fix 738 or cite its origin.
4. correct-before-use — the gloss "not a constraint from the heat source side" drops the source's next sentence: "in practical systems, Tout can be constrained by material considerations" (p2). Amend.
5. correct-before-use — the source never mentions ARIES-CS or Fig. 12. Established: the cited method is lumped with Tin as input. That Raffray applied it so is inference; Raffray p737 says the blanket thermal-hydraulic parameters were optimized together with the cycle. Split the sentence; drop "now supported".
6. note — "850→1200 has the major effect" is the Fig. 3 discussion (p3), not Fig. 2. The source carries two captions labelled "Fig. 2" (T-S p2; efficiency p3); cite by image file.
7. note — Fig. 1 draws no block; the heat source is a boundary label with Tout leaving and Tin entering. Saying so strengthens the claim.
8. note — Raffray's Π_C 3.5 lies outside the source's plotted 1–3 range (optimum ≈ 2.4). Worth a line where § 2 relies on reproducing 0.43.

Not covered: Raffray p735 citation context, Table II, contract §§ 5–6a, Ref. 13, the registration summary.

— fresh source-check reviewer (Ref. 15), 2026-09-25
