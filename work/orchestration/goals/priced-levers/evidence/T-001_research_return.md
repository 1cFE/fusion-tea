# T-001 evidence — what admissible sources establish about the two field fences

**Author:** the round agent, 2026-09-02. Clean room honored: `PROTOCOL.md` §1–3 read first; no sealed or barred artifact opened; the one screened candidate (pyFECONs costing framework) was **not** registered and is recorded in the run log with its reason.

Three research-seam runs, all returning `REGISTERED` (`knowledge/research/requests/runs/`). Three sources registered. The largest single finding, though, came from a source the repository already had.

## 1. The Stellaris Table 8 text extraction is garbled; the image is clean

The model's own primary source carries the conductor design in Table 8. The markdown extraction of that table is **wrong in most rows** — it misaligns columns, drops rows, and carries `[?]` markers. The extracted table **image** (`knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_022_table_0.png`) is clean and was read directly, and cross-checked against the raw PDF page (iter-02 `raw.pdf`, page index 22). This repeats the round-1 finding of the predecessor goal that the iter-02 extraction is unreliable and the raw PDF governs.

Image-verified Table 8, coils 0–5:

| row | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| I (total Amp-turns) [MA] | 15.4 | 14.6 | 13.8 | 12.9 | 12.5 | 11.2 |
| Number of turns | 324 | 324 | 289 | 289 | 256 | 225 |
| j_WP [A/mm²] | 119 | 112 | 120 | 112 | 122 | 124 |
| j_tape-stack [A/mm²] | 1323 | 1249 | 1330 | 1243 | 1360 | 1384 |
| Cross section side length [mm] | 360 | 360 | 340 | 340 | 320 | 300 |
| Coil mass, no casing [ton] | 24.2 | 25.4 | 21.6 | 21.5 | 19.0 | 17.0 |
| Peak field [T] | 24.6 | 23.1 | 22.0 | 21.0 | 21.4 | 19.5 |
| Max j_op/j_crit **no grading** [%] | 60.5 | 46.5 | 50.2 | 54.1 | 56.3 | 55.8 |
| Max j_op/j_crit **with grading** [%] | 80 | 80 | 80 | 80 | 80 | 80 |
| **Tape length no grading [km]** | 807 | 847 | 721 | 717 | 636 | 567 |
| **Tape length with grading [km]** | 167 | 161 | 146 | 134 | 131 | 118 |
| Max WP linear force [MN/m] | 174 | 131 | 115 | 115 | 115 | 85 |
| Peak stress on WP [MPa] | <650 (all coils) | | | | | |

Every Table-8-derived value the model already holds is **confirmed correct** by this read: `wp_side = 0.36` (coil 0, 360 mm), the six side lengths behind `vol_cold_cryo`, `I_coil = 15.4` MA, the per-coil ampere-turns behind `f_set` (including the two the model's doc comment already flags as text-extraction misprints — image gives 14.6 and 12.5, and the model uses those), and the "<650 MPa" behind `k_sigma`. Prior image verification held.

## 2. The sizing relation the model does not have

The table closes exactly, across all six coils, under **I_coil = j_WP · wp_side²**:

| coil | I from the table [MA] | j_WP · side² [MA] | error |
|---|---|---|---|
| 0 | 15.40 | 15.422 | +0.15% |
| 1 | 14.60 | 14.515 | −0.58% |
| 2 | 13.80 | 13.872 | +0.52% |
| 3 | 12.90 | 12.947 | +0.37% |
| 4 | 12.50 | 12.493 | −0.06% |
| 5 | 11.20 | 11.160 | −0.36% |

Two consequences.

**(a) The winding pack is sized by current, and the model does not know it.** `wp_side` is held at 0.36 m while the committed study swept `I_coil` from 8 to 24 MA. At a fixed 0.36 m the implied winding-pack current density runs 119 A/mm² at the design point, **139 at 18 MA, 147 at 19, 154 at 20** — against a design range of 112–124 across Stellaris' own coil set. The committed sweep silently raised the winding-pack current density by up to 30% without adding conductor. This is a disclosure about the committed study, not a defect in it: `wp_side` was never a swept axis and the record does not claim otherwise.

**(b) `j_WP` is the design lever, and it does not exist in the model at all.** Making `wp_side` computed from `I_coil` and `j_WP` is what turns a held number into a design variable — and `j_WP` is precisely the quantity Stellaris varies across its own coil set.

**Volume closes too.** Σ(side²)·25 m·8 occurrences = **136.560 m³**, reproducing the model's held `vol_cold_cryo = 136.56` exactly. The implied winding-pack density is 7419–7840 kg/m³ across the six coils (total 1029.6 t). Noted as an internal tension worth stating rather than resolving: that density is steel-like, while Table 7's material fractions (conductor 15%, Cu jacket 10%, insulation 45%, steel 26%, He 4%) read lighter — most likely the 316LN radial plates are counted inside "insulation". Do not silently reconcile the two tables.

## 3. Tape quantity is the conductor currency, and grading is the knob

From the same source, page 24 text (raw PDF, verified): coil 0 "without grading, would require 807 km of 6 mm tape, but with perfect grading (assuming j_op/j_crit = 80% everywhere), this requirement decreases to 167 km." Across the six coils the grading factor is **4.8×–5.4×**. The design criterion is j_op/j_crit ≤ 80%, and the un-graded design sits at 46.5–60.5%.

So the conductor lever's real currency is **tape length**, not a grade name from a table.

## 4. Field capability is not the binding constraint — REGISTERED

`knowledge/sources/development_and_large_volume_production_of_extremely_high/` — Molodyk et al. 2021, *Sci. Rep.* 11:2084, open access.

- J_E > 1000 A/mm² at 20 K and 20 T, field perpendicular to the tape (the worst orientation); the SPARC design target was 700 A/mm² at the same point and production tape beat it.
- **Jc ∝ B^(−0.6) at 20 K**, with the pinning force saturating near 15 T — a slow power law above it, not a cliff.

Applying that exponent (this arithmetic is the round agent's, not the paper's): going from the model's 24.9 T ceiling to the 29.1 T the deadlock needs costs **≈ 11% in engineering current density**, hence ≈ 11% more tape for the same current. The Stellaris source independently states the record HTS magnet at 20 K reaches ~45.5 T peak field on the HTS.

**Reading: ~29 T on the winding at 20 K is not conductor-limited.** Two caveats carried, not buried: no open source demonstrates a *winding pack* at 29–31 T at 20 K (the highest fusion-relevant demonstrated point is SPARC's TFMC at 20.1 T / 20 K), so anything above that is extrapolation and must be labelled as such; and Zhai, Otto & Zarnstorff (PPPL, 2024) argue REBCO winding-pack current density at 20 K "may drop to about 50 A/mm²", far below what the tape data implies. That disagreement is surfaced, not resolved — and note Stellaris' own coil set runs at 112–124 A/mm².

## 5. Premise conflict — the 800 MPa allowable is already the optimistic end — REGISTERED

`knowledge/sources/in_plane_and_out_of_plane_tf_coil_support_for_the_us_fnsf/` — Titus & Kessel, PPPL-5297 (2016), open DOE report. Verified verbatim in the registered extraction (`output.md:95-99,137`), not taken on a subagent's word:

> Static Primary Stress Allowable based on ITER: 2/3 * 1000 MPa Yield = 666 MPa
> Optimistic Primary Stress Allowable based on Improved 316 metallurgy: 800 MPa

and, at `:137`:

> 666 MPa is the usual allowable for ITER grade 316 stainless steel. Some modest reallocation of metal cross sections may still be needed. Improved yield stainless steels are an option. Limit analysis has been used to qualify this level of stress by showing a factor of safety of 2.0 against burst over the design loads.

**This works against the goal's assumption that the structural fence has room above it.** The model's `sigma_allow = 800e6` is inherited from Stellaris' own design limit for cryogenic 316LN, and it is *not* wrong — but the wider literature calls that number the optimistic case and names 666 MPa as usual practice. There is no comfortable headroom above 800.

Material substitution does not rescue it: JJ1, the steel ITER actually uses in high-stress TF case regions, yields 1126 MPa at 4 K against 316LN plate's 1066 — about 5% on a two-thirds rule. High-nitrogen 316LN forgings could support 760–865 MPa, i.e. roughly where the model already sits.

**The routes PPPL-5297 itself names are geometry and design rule, not material** — "reallocation of metal cross sections" first. That is the same lever § 2 identifies, arrived at independently. The report also notes, directly on point for a REBCO machine: *"More steel with less space for conductor may be possible with high temperature superconductors (HTS). REBCO HTS are thin layers of HTS coated HASTELLOY tapes in which the steel tapes make up most of the cross section."*

Surfaced to the owner in session per capture-fidelity law 4; not resolved silently in either direction.

## 6. Bounded negative — no $/kA·m-versus-field curve exists — with the composition route

`knowledge/sources/hts_potential_and_needs_for_future_accelerator_magnets/` — Bottura & Bordini 2025 (CERN), arXiv:2503.23048, open access. It carries the present REBCO price band, **150–200 USD/kA·m**, and states the mechanism explicitly: more superconductor is needed at higher field both because critical current density falls with field and because mechanical and protection limits force lower current density.

**But no open source gives $/kA·m as a function of operating field for a fusion magnet.** The unit itself hides the problem — it is quoted at a reference condition (77 K self-field, or 4.2 K / 20 T, or unstated) and the sources do not agree on which. The honest route is a **composition, not a citation**: conductor quantity = (coil geometry and current) ÷ J_E(B, 20 K) with J_E(B) from the Molodyk exponent, priced at a per-kA·m rate. Each leg has a source; the composed chain does not, and must be labelled a constructed relation carrying its citations.

For calibration against what the model already holds: the pinned 1costingFE prices REBCO at **50 $/kA·m** (`costing_constants.yaml:56`), its own comment calling it an "aggressive NOAK target". Bottura's present-day band is 150–200; Zhai et al. name 10 $/kA·m as the price needed for LTS parity and note price may halve per 10× procurement volume. So the model's 50 sits between an aggressive target and today's market, which is a disclosure the cost chain should carry rather than a number to change in this round.

## 7. The synthesis: the deadlock has an evidenced escape, and it is geometric

Combining § 2 and § 5 with the committed study's own numbers, at the cheapest sustainment-satisfying point (I_coil 18 MA, B_peak 29.10 T), sizing the winding pack consistently with Stellaris' own design current density:

| j_WP | `wp_side` = √(I/j_WP) | σ = k_sigma·I·B_peak/wp_side | vs 800 MPa |
|---|---|---|---|
| 112 A/mm² (coils 1, 3) | 0.4009 m | **797.3 MPa** | **feasible** |
| 119 A/mm² (coil 0) | 0.3889 m | 821.9 MPa | 2.7% over |
| 124 A/mm² (coil 5) | 0.3810 m | 838.9 MPa | 4.9% over |

**At the low end of Stellaris' own winding-pack current-density range, an 18 MA coil is stress-legal.** It is a knife-edge — the whole design range spans feasible to 5% over — which is exactly why `j_WP` has to become a swept design lever rather than a number someone picks.

The other half of the unlock, B_max ≥ 29.1 T, costs ≈ 11% more tape by § 4.

**One conservatism, disclosed:** the model holds `peak_ratio = 2.7667` fixed, so `B_peak` scales with current alone. The Stellaris source states that "the peak field is also heavily dependent on the size of the winding pack" — a larger pack lowers the peak field, which would relieve *both* fences at once. The model cannot represent that (no admissible relation for peak ratio versus pack size), so the numbers above are conservative in the helpful direction. Disclosed, not modelled, and not defaulted.

## 8. The extrapolation, bracketed — and a limit in the source's own model

A second research pass sharpened § 4 and found the honest boundary of every available basis. **Registered:** `knowledge/sources/general_approach_for_the_determination_of_the_magneto/` — Zhang et al., *Supercond. Sci. Technol.* 30 (2017) 025010, open access via CORE. This is the parameterization Stellaris fitted:

> I_c(B, θ) = I_c0 · [1 + (B/B₀)^α]^(−β) · ε_θ,  ε_θ = (cos²θ + γ⁻² sin²θ)^(1/2)

**Its published fits are at 77 K and fields up to 400 mT only.** Nothing at 20 K, nothing above 0.4 T. Above the fitted range the form degenerates to a pure power law, I_c ∝ B^(−αβ), and **αβ is not universal**: across the five commercial tapes fitted at 77 K it spans 0.58 to 1.50, a 2.6× spread.

**The measurement dataset behind Stellaris' own fit stops at 8 T.** Wimbush, Strickland & Pantoja, *Critical current characterisation of SuperOx YBCO 2G HTS superconducting wire*, figshare doi 10.6084/m9.figshare.13708690.v1, CC BY 4.0 and openly downloadable — 15–85 K, 90 angles, **0 to 8.0 T, hard stop**. **Not registered:** the artifacts are `.xlsx` workbooks, which the source registry cannot extract; recorded here so the gap is durable rather than forgotten, with the direct file URLs in the run log. Its load-bearing use below is a single number.

**So Stellaris' own j_crit at 24.6 T is itself an extrapolation**, roughly 3× beyond its fitting data. That is a finding about the source's model, not a gap in this search, and it belongs in the model's disclosure rather than in a correction.

**The 8 → 20 T gap is bracketed empirically**, because the figshare dataset and the registered Molodyk paper measured **the same SuperOx wire** (the dataset's own description says so):

| point | conditions | I_c/w |
|---|---|---|
| Robinson (figshare) | 20 K, 8 T, 0° (B⊥, worst) | 1023 A/cm |
| Molodyk (registered) | 20 K, 20 T, B//c (same worst orientation) | 550–675 A/cm |

The implied exponent between two measured points is **αβ = 0.46–0.68, centred ≈ 0.56** — sitting on Molodyk's independently stated α ≈ 0.6, and at the shallow end of Zhang's 77 K range. The tape's high-field decay is mild.

**Tape-quantity multiplier for the step the deadlock needs (24.9 → 30 T)**, at fixed j_op/j_crit margin, where quantity scales as 1/J_E:

| assumed αβ | J_E ratio | tape multiplier |
|---|---|---|
| 0.6 — Molodyk's measured exponent, and the 8↔20 T bracket | 0.894 | **×1.12** |
| 1.0 | 0.830 | ×1.20 |
| 1.5 — Zhang's steepest tape at 77 K | 0.756 | ×1.32 |

**Reading: the field increase is not paid for in conductor.** Even on the steepest exponent it costs about a third more tape, against a grading lever worth 4.8× (§ 3). It is paid for in *structure* — Lorentz load scales as B², so 24.9 → 30 T is ×1.45 on a stress allowable that § 5 shows has no headroom. That asymmetry is the round's central physical finding.

**Two caveats to carry into the model, not to bury:** 30 T is 1.5× beyond the highest *measured* 20 K point in the open literature (20 T), so the model's ceiling relation is an extrapolation and must be labelled one; and the exponent is wire-specific — Senatore et al. (2024) show a 4× vendor spread in J_c at 20 K/19 T — so this bracket is licensed for the SuperOx wire family Stellaris actually specifies, and transfers to no other vendor without refitting.

**One further design constraint found, filed not actioned:** thermomagnetic flux jumps appear in thick REBCO layers (≥3.5 µm at 4.2 K, 5 µm even above 20 K) at high field — a real limit on buying capability by thickening the superconducting layer (Jaroszynski et al., NHMFL, arXiv:2502.02706, open; measures I_c to 45 T but at 4.2 K, so it is not a 20 K basis).
