# Source check — reading of Malang, Schnauder and Tillack 1998

HEAD `3e945e0a`. Read: the brief, `malang98-reading.md`, `raw.pdf` pp. 561–567, the three page renders, `ref15-reading.md` § 1–2, `owner-supplement-r4.md`.

**Verdict: FINDINGS** — one correct-before-use, five notes. The reading states what the source says, with correct page, figure and table citations.

## Checks

1. Figure labels — PASS. The To/Ts plot (ΣΔp/p 5%, 8%) sits under "Fig. 1. Combination of self-cooled blanket…" (p. 562); the schematic with T–s inset sits under "Fig. 3. Influence of maximum/minimum helium temperature…" (p. 565); Fig. 2 (p. 564) is captioned correctly; the text refers to figures by content. The swap description is right.
2. `[SOURCE]`/`[SOURCE-FIG]` — PASS. Every quotation matches the PDF at its cited page. Table 1's nine values, the p. 565 46%/44% and 650/35 vs 630/28 °C statements, and every Section 4 number (helium 18 MPa, 0.4 MPa, 436/650 °C; lithium 670/470 °C; 3 × 900 MW; 8175 m², 3.6 m, 9.0 m, 0.020/0.024 m; 0.04 MPa) agree. Schematic states 1–10 read correctly.
3. Absence claim — PASS. "divertor", "parallel", "series": none. "First Wall (FW)": once (p. 563). "loop": about ten, all the lithium loop, the helium loop, or the Rankine alternative's secondary loop (pp. 561, 562, 566; conclusion (d)). "exchanger": about seventeen, all the IHX, cycle exchangers generally, or Rankine-plant comparisons (liquid metal/water p. 562; Li/Na IHX p. 566). Nearest to a branch structure: "three units with a thermal power of 900 MW each" (p. 566).
4. § 2–3 — FINDINGS. Lineage supported by `ref15-reading.md` § 1 (expressions attributed to Ref. [4]). "Does not address it" is the right bounded result: one loop, 1998, no mention of ARIES-CS. "Natural inheritance" overreaches (finding 1).

## Findings

1. Correct-before-use — § 3 "the natural inheritance of the method" presents an agent plausibility judgement as something the source "adds". The source is silent on combining loops; silence is not support. Reword: the source applies the method to one hot stream and says nothing about several; the Fig. 12 inset reading is consistent with it, not supported by it, and remains an inference.
2. Note — § 1 b1 and § 3 say "one intermediate heat exchanger"; the paper sizes it as three identical 900 MW units (p. 566, recorded in b5). Say "one IHX duty, three identical units on the same terminals". "The only exchangers are…" holds for the described system only.
3. Note — "origin": Malang attributes the parameterisation to Rust 1979 [8] (p. 563; p. 567) and prints the three-stage form. Say "origin within the ARIES lineage".
4. Note — § 1 b3 drops β's exponent (γ−1)/γ; "the heat source enters only through To and the IHX's share of β" is a reading of the equation, so grade it `[DERIVED]`.
5. Note — § 2 b2 gives PbLi outlet 738 °C; `ref15-reading.md` § 2 gives 737 °C. Not from this source; reconcile.
6. Note — `ref15-reading.md` § 1 records Schleicher's Ref. [4] as vol. 39–40; the PDF is vol. 41 (1998) 561–567. Identification holds; record the discrepancy once.

## Not covered

`output.md`, the ARIES-CS numbers in § 2 b2, Raffray 2008 Table III, Ref. 13, Lyon's 2916 MW.

— fresh source-check reviewer (Malang 1998), 2026-09-25
