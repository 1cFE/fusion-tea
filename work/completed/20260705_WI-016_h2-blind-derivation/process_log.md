# WI-016 Process Log — Blind Derivation Phase

Chronological record of the research loop. Honesty over polish: includes dead ends, judgment calls, pretraining fallbacks, and firewall near-misses.

## Firewall events

1. **SOURCE_INDEX.md lists PyFECONS as a registered source at `/home/reid/PyFECONS`** (first entry under Primary Sources). This is a costing codebase closely related to the held-out answer key. I read only the index entry (which is unavoidable — the index is whitelisted) and did NOT open the codebase or use anything from the entry beyond noting its existence. Near-miss logged; no formula exposure.
2. **`knowledge/sources/tea_dt_mfe_cost_analysis/`** — before using it I verified its identity from the header: it is Araiinejad & Shirvan 2025, Applied Energy 401, an independent MIT bottom-up TEA, not the costing-code methodology paper. I used only its source-quoted unit costs and its restatement of ARC quantities. No PyFECONS/1costingfe code references were encountered in the passages I read.
3. No dossier `model_setup.py` files were opened at all; every ARC number used is source-quoted from the Sorbom 2015 extraction or its table images.

## Search/consultation record

| # | Action | What it contributed |
|---|--------|---------------------|
| 1 | `ls knowledge/concept_research/`, `ls knowledge/sources/`, head of SOURCE_INDEX.md | Corpus map; flagged PyFECONS entry (firewall event 1) |
| 2 | Listed concept 01 dossier tree | Found full ARC paper extraction under `iter-03/sources/arc-reactor-specifications/` (2219 lines + equation/table images) |
| 3 | Header check of `tea_dt_mfe_cost_analysis/output.md` | Identified paper (firewall event 2) |
| 4 | Grep ARC extraction for cost/REBCO/stored-energy terms | Located Section 6 costing (lines 1533–1642), Table 10/11, REBCO 5730 km, tape/cable/coil counts (lines 1025–1095) |
| 5 | Grep ARC extraction for physics operating-point terms | Located Section 3.1 0-D design (lines 236–422): Troyon, kink q*, Greenwald, elongation, B-on-coil closures — the entire closure set came from this one pass |
| 6 | Read ARC lines 230–430 in full | Closure equations (2)–(9), bootstrap formula (13), design-point narrative |
| 7 | Grep ARC for Brayton/efficiency/Pnet/recirculating | Power-balance anchors: ηth = 0.40/0.46/0.50 phases, Pnet = 190/233/261 MW, Qe = 3/3.5/3.8 (lines 186–226); klystron 50% (line 860); cryo 0.57 MW (line 1107) |
| 8 | Read ARC cost section (1533–1642) | Materials table, $1.06M/tonne fabricated scaling, Table 11 breakdown |
| 9 | Read ARC lines 525–575 and 1390–1410 | Final operating point (⟨T⟩ 13.9 keV, ⟨n20⟩ 1.3, βN 2.59, Ip 7.8, κ 1.84) from the machine-comparison table |
| 10 | Grep ARIES cost documentation for magnet cost algorithms | Account 22.02.01 scope and the "parametrically determined by field strength and current density" / "stored energy" statements (lines 1317–1322, 1475) — justified the scaling form |
| 11 | Grep ALPHA-revisit paper for coils | Only a CAS line item (22.1.3 Coils, 5.9/22.8 M$) for small MIF magnets — **dead end** as a tokamak-scale anchor, not used |
| 12 | Grep Helios overview for coils/costs/aux power | Stellarator stretch material: 20 T on-coil, 1.2 m standoff, 12+324 planar coils, NCSX/W7-X overrun narrative, 70 MW aux load, 25 T→7.5 T on-axis statement |
| 13 | Grep TEA paper for alpha/neutron/multiplication conventions | **Dead end** — the paper doesn't state the D-T split or blanket multiplication explicitly in extracted text |
| 14 | Read TEA paper lines 300–345, 440–514 | Confirms it re-uses ARC's 5730 km / 70 kA cable quantities; unit costs $2.5/W heating, $1.5/W power supplies, $300/kW cryo at 20 K; learning-rate treatment of magnets |
| 15 | Read ARC lines 845–899 | RF wall-plug closure: ICRF 19 MW wall-plug for 13.6 MW coupled; LH power budget table |
| 16 | Read ARC lines 180–235 | Brayton phase details; located Table 1 caption — the actual Table 1 body is MISSING from the text extraction (image not captured either) |
| 17 | Image inspection: `page_026_table_0.png` | Machine-comparison table — **caught an extraction error**: markdown line 1404 labels the 143 MW ARC row "P_fus"; the image says **P_heat** (consistent with 105 alpha + 38 RF). The markdown value would have been badly wrong as a fusion-power anchor |
| 18 | Image inspection: `page_028_table_1.png`, `page_029_table_0.png` | **Caught a second extraction error**: REBCO price is $18–36/m in the image; markdown says "$198/m ~ $36/m" (OCR of $18 → $198). Confirmed via arithmetic: 5730 km × $36/m = $206M = Table 11's high-end tape cost. Also confirmed magnet mass/cost breakdown |
| 19 | Scan of concept 01 `dossier.md` | Corroborating context only (CFS 20 T demo, ARC evolution to pulsed operation); no additional quantitative anchors used |

## Judgment calls

1. **C_prof calibration (Relation 1).** The uniform-plasma relation gives 497 MW vs. ARC's 525 MW. I introduced a profile factor and calibrated C_prof ≈ 1.05 on the single anchor point rather than integrating profiles. Defensible physically (peaking gains are damped by reactivity flattening above 15 keV), but it is a one-point calibration, declared as such.
2. **Blanket multiplication M_n (Relation 2).** Not stated anywhere in the corpus I found. Standard range 1.1–1.2 is pretraining. I selected M_n ≈ 1.2 because it closes ARC's published Pnet = 190 MW / Qe = 3 given my recirculating-power accounting (69 MW RF wall-plug + ~1 MW cryo). This is inference-by-consistency, not a sourced value; the honest uncertainty band on Pnet is ±10%.
3. **Q_e scope.** ARC's Qe = 3 only works out if house/BOP loads are excluded and only RF wall-plug + cryo count as recirculating. I adopted that scope for the worked example and flagged the definitional trap.
4. **k_st structure multiplier (Relation 3).** ARC's 4350 t structure vs. a 215 t virial minimum gives k_st ≈ 20, but the paper says the base is conservatively modeled as solid steel. I bracketed k_st as 5–10 physical / 20 upper, on judgment. Weakest constant in the whole derivation.
5. **OCR corrections.** Trusted table images over markdown text in both discrepancies found (rows 17–18 above), per the project's own image-inspection protocol.

## Pretraining fallbacks (declared)

- D-T reactivity quadratic approximation ⟨σv⟩ ≈ 1.1e-24 T² m³/s, 10–20 keV [Freidberg, *Plasma Physics and Fusion Energy*]
- E_fus = 17.6 MeV; alpha/neutron 3.52/14.06 MeV momentum split [Freidberg]
- Torus volume 2π²Ra²κ; Ampère's law N·I = 2πRB/μ0
- Virial-theorem minimum structural mass M ≥ ρE/σ [standard magnet engineering]
- M_n ≈ 1.1–1.2 blanket multiplication range [standard blanket engineering]
- f_3D ≈ 2–5 stellarator coil complexity factor — weakest pretraining claim, direction corpus-supported (Helios/NCSX narrative), magnitude not

## Corpus insufficiencies found

1. ARC Table 1 (the master parameter table) is absent from the extraction — text and image both. Worked around via the Table 7 comparison table (image-verified) and in-text statements. Cost the session ~3 extra searches.
2. No corpus source states blanket energy multiplication for any concept I checked.
3. No cross-machine magnet structure mass/cost table (ARIES systems-code outputs are described but not tabulated in the extracted cost-account document), so the structure cost constant rests on one rough ARC anchor.
4. The ALPHA-revisit coil line items are for small MIF magnets and don't transfer to tokamak-scale TF systems.
