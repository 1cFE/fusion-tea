# Q1 thermal-cycle review — fresh reviewer

Reviewed at repository HEAD `812b79bf`. No model or study was run.

**Verdict: SURVIVES.** Deciding check: (e), which shows the contradiction is independent of exchanger arrangement; (a) and (b) close the diagram-reading and definition escape routes.

Premise note: the brief's Raffray images hold Fig. 15, Table V and Fig. 20, not Tables II–III or Figs. 12–14. Those are on `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p734/p736/p737.png` (Table II; Figs. 12–13; Table III), named by contract § 1, so I read them.

## (a) Diagrams

Fig. 12 (p736): one cycle stream `He T_HX,in` passes the blanket-He exchanger (counterflow), then splits between the LiPb and divertor-He exchangers, which rejoin at `He T_HX,out` → Brayton cycle. No bypass, no split before the He exchanger, no He–PbLi exchanger (the 111 MW is conduction inside the blanket), no reheat; Fig. 13: whole-flow recuperator, one expansion. The inset draws Cycle He 355 → 707 °C over the whole z-range, Blkt He 385 → 460 °C over the lower part and LiPb 464 → 737 °C plus Div He 571 → 700 °C over the upper part, end to end as one hot leg. So 355/707 °C are the train's cycle-side inlet and outlet; the figure shows series-then-parallel.

## (b) Definitions

Table II (p734): He inlet/first-wall outlet/module outlet 386/430/456 °C; PbLi 451/738 °C; He duty 1192 MW "including 141 MW of friction power + 111 MW of conducted power from Pb-17Li"; PbLi 1444 MW net of the 111 MW. Table V (p741): divertor 573/700 °C, 186 MW. Each loop runs blanket → exchanger → blanket, so 456 °C is the He hot inlet. Table III (p737): "HX temperature difference between hot and cold legs 30 °C" is an exchanger terminal difference (inset: 385/355, 737/707); recuperator effectiveness 0.95 is a separate row. Duties are heat carried to each exchanger, and p737 says friction "was added to the fusion thermal power", so all 2822 MW enters the cycle. No reading lets 1192 MW enter above 456 °C.

## (c) Cross-paper mapping

Raffray 2822 × 2436/2365 = 2907 MW against Lyon 2916 (Table IV, p708): 9 MW apart, both including returned pump heat (Fig. 18, p704). Capacity rate over 352 K: 8.02 MW/K (Raffray) or 8.28 (Lyon, 1595 kg/s). Lyon has no exchanger model; Fig. 18 applies 43% to all of P_thermal. The mapping moves cycle flow 3% and cannot supply the ≥ 11.8 MW/K the He stage needs. The contradiction is internal to Raffray.

## (d) Our representation

Fig. 13 and our chain (`plant.sysml` 142–390; `network_heat_driven_closure_impl.py`) agree: compressor discharge 371.1 K → whole-flow recuperator `R = Tc + ε(kTt − Tc)` → train → one expander (k 0.6439). Executed inputs: ε_rec 0.95, primary flows 3261/26 860/283 kg/s, UA 50 MW/K per stage. At 1700 kg/s (C 8.83 MW/K) nothing binds: `unmet_heat` 0, `he_hot` 716 K, and `turbine_temperature` 901.4 K (628 °C) equals the closed form `Tt = (Q/C + 0.05·Tc)/(1 − 0.95k)`; heater inlet 297 °C. At 1600 kg/s (C 8.31) the He bound binds (`he_hot` 729.15 K, `he_hot_terminal_difference` 3.6 K, `he_unmet` 53.5 MW) and the PbLi cold end pinches (`pbli_cold_terminal_difference` 5.5 K, `pbli_unmet` 56.4 MW); turbine inlet 647 °C against 681 °C with all heat accepted. Reaching 707 °C needs C ≈ 8.08 MW/K with R = 345 °C, where the He stage accepts only ≈ 875 MW of 1249. The driver is the recuperated energy balance at high flow and the He hot bound at low flow; conductances, split and arrangement are not limiting. The published 355 °C inlet would limit the He stage far more: C × (426 − 355) = 569 MW (590 at 8.31) against 1192 at the 30 °C approach, 810 at zero. Our model is generous to the source.

## (e) Reconstruction

C = 2822/352 = 8.02 MW/K. The He stage must put 1192 MW into fluid entering at ≥ 355 °C and leaving ≤ 456 − Δ: it needs ≥ 11.8 MW/K (Δ 0) or 16.8 (Δ 30), more than the whole flow. He-first series: He outlet 504 °C > 456. All parallel, or He parallel with the rest: minimum He fraction 1.47 (Δ 0) / 2.09 (Δ 30). He last: outlet 707 > 456. No arrangement is consistent; Fig. 12 supports only the first. The series train closes only with train inlet ≤ 272 °C (Δ 0; C 6.5, ε_rec ≤ 0.67) or ≤ 221 °C (Δ 30; C 5.8, ε_rec ≤ 0.47), contradicting 0.95 and 355 °C. The inset explains the source: one lumped hot leg 385 → 737 °C with 30 K at both ends gives 707 °C only if heat fractions equal span fractions, but He carries 42% of the heat over 21% of the span.

## Implied change

An interpretation, not a model element: Raffray's 707 °C / 0.43 is the output of a lumped hot-leg treatment, not a per-branch operating point. Reproducing it needs a lumped heater (one hot stream 385 → 737 °C, 30 K terminal difference): turbine inlet +60–80 K, efficiency +0.03–0.04, physical He limit discarded. Lowering the recuperator (ε ≤ 0.67) reaches 707 °C but drops gross efficiency to ≈ 0.36. Keep per-branch exchangers; carry Q1 as a source-internal inconsistency in attribution.

## Undetermined

How Raffray's cycle code treated the exchangers, and whether Lyon's 2916 MW includes BOP heat (≈ 50 MW). The cycle/HX calculation behind p737's Ref. 7 would settle the first.

## Findings

1. Correct-before-use — Q1 wording: no exchanger arrangement, not only the implemented network, can reach 707 °C; cite the inset's lumped hot leg as the mechanism.
2. Correct-before-use — Scaling duties × 1.030 with primary flows held at Raffray's values pinches the PbLi cold end (return must be 447 °C, against 455 at 2365 MW); part of the 56 MW PbLi unmet at 1600 kg/s is this artefact.
3. Correct-before-use — The brief mislabels p738/p742 (premise note) and gives 301 °C for the 1600 kg/s heater inlet; `cases.json` says 308.6 °C.
4. Note — Model approaches (3.6–4.8 K He, 4–5 K PbLi) are far tighter than the source's 30 °C; imposing 30 K enlarges the shortfall.

## Not covered

ε-NTU numerics beyond spot checks; Lyon's thermal-power composition; cost channels; other study cases.

— fresh thermal-cycle reviewer, 2026-09-25
