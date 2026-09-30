# T-004 independent source/math check A — Nb₃Sn

You are a fresh, independent checker in `/home/reid/1cfe/fusion-tea`. You did not author any of this work. Check source interpretations against the **original pages**, not the author's summaries. Write your verdict to `work/orchestration/goals/magnet-material-comparison/evidence/check-nb3sn.md` (the only file you write; use a scratch directory outside the repository for scripts and renders). Budget about 30 tool calls; return at most 500 words. Do not load wider project context, do not read goal trails, do not delegate.

## Clean room

Do not open `knowledge/holdout/**`, `knowledge/sources/aries_cost_account_documentation/`, `knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`, `exploration/concept_analysis/analyses/09-qi-stellarator-hts/`, or anything naming ARIES-CS.

## Claims to check (from `evidence/sources/nb3sn-law.md`, `nb3sn-winding.md`, `nb3sn-highfield.md` and `evidence/comparison-contract.md` §2–§4)

Render PDF pages with `.codex-test/run python -c "import fitz; ..."` (PyMuPDF) from the stored raw PDFs in each source directory or `knowledge/raw/`, and view the PNGs.

1. **Law form and parameters.** Tsui & Hampshire 2012 (`knowledge/sources/critical_current_scaling_and_the_pivot_point_in_nb3sn/`): eq. (6)–(7) form, and Table 5(c) BEAS II parameters p 0.489, q 1.618, C 2.227e10 A T m⁻², Ca1 226.93, Ca2 203.86, ε0,a 0.187 %, εM −0.366 %, Bc2*(0,0) 30.28 T, Tc*(0) 16.02 K. Engineering Jc over the whole strand, 10 µV/m.
2. **Strain units and meaning.** In the ITER form, are strains fractions (0.00187) so that 1 − Ca1·ε0,a > 0? Does the law take intrinsic strain εI directly? Is the SULTAN/EU DEMO “effective strain” (−0.3 % in Demattè's sizing, −0.27/−0.33 % prototypes, −0.55 to −0.97 % ITER TF) the same intrinsic strain input? Is εM needed at all when intrinsic strain is supplied directly?
3. **Independent evaluation.** Implement the law yourself (do not read `evidence/screen/contract_screen.py` until you have your own numbers). Compute Ic of a 0.82 mm strand at (12 T, 4.2 K, εI = 0), and compare with the ITER TF specification (> 190 A at 12 T, 4.22 K) and with any Ic value you can read off a Tsui BEAS II figure at a stated applied strain (convert with εI = εA − εM as the paper defines, stating your convention). Then compute Ic at (12 T, 5.2 K, −0.3 %), (12 T, 6.7 K, −0.3 %), (8 T, 6.7 K, −0.3 %), (12 T, 6.7 K, −0.6 %). Finally compare with `evidence/screen/contract-screen.json` and report any discrepancy.
4. **EU DEMO construction arithmetic** (Demattè & Bruzzone, `knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/`; Table I on raw.pdf p.2, sizing text p.3–4): 104.95 kA, 12.04 T, 6.5 K, −0.3 %; 399 × 1 mm strands, Cu:non-Cu 1; 20 % void; 68 × 37.9 mm conductor; total Cu 1123.7 mm²; steel 982.7 mm²; pack 1296 × 411 mm, 142 turns. Check the contract's derived per-kA values: steel 9.36 mm²/kA; insulation/ground/filler fraction 0.237 of gross (1 − 142 × 68 × 37.9 / (1296 × 411)); protection copper 93.4 A/mm². Is scaling steel per kA linearly with B defensible as a bounded assumption, or is there a better-sourced basis?
5. **Temperature budget.** Sedlak 2020 (`knowledge/sources/advance_in_the_conceptual_design_of_the_european_demo/`): Tcs ≥ 6.7 K = 4.5 K inlet + 0.7 K nuclear + 1.5 K margin. Is it right to evaluate the conductor at 5.2 K and require Tcs ≥ 6.7 K? How does Demattè's “6.5 K for 2 K temperature margin” relate?
6. **Range.** Bruzzone CP(15)09/01 (`knowledge/sources/design_manufacture_and_test_of_a_82_ka_react_wind_tf/`): 82.4 kA at 13.50 T, 1.5 K margin, tested only to 70 kA. Tsui BEAS II measured domain (field and temperature). Is 8–12 T “matched, supported” and 13 T “edge” a fair reading? Is 8 T inside the measured BEAS II domain at the relevant temperatures?

## Return

`check-nb3sn.md` with, per numbered claim: verdict (`confirmed`, `corrected: <what>`, or `unverifiable: <missing evidence>`), the original location you inspected, and your independent numbers. Overall verdict: `PASS`, `FINDINGS` (list what must change before modeling), or `UNVERIFIABLE`.
