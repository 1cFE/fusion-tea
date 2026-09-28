# T-001 — original Point-A power-balance reconstruction

Status: author research complete; recommendations require independent review. Date: 2026-09-17. Scope: original Stellaris plus two registered reference hops (Lion 2021 and Lion 2023). No model changes, studies, tuning, holdout material or excluded mixed-source note were used. [OWNER] Scope and constraints are inherited from adjacent source-brief.md, goal.md and owner-request.md. All deductions and recommendations below are [AGENT], not settled owner decisions.

## Finding

Stellaris explicitly defines radiation and confinement as separate loss terms. Its Appendix A substitutes W/tau_E into ISS04 while retaining radiation in the balance. Thus removing radiation merely because confinement uses W/tau_E would contradict its stated model. However, Table 5 does not supply an unambiguous, numerically closing same-boundary ledger. Its total energy, confinement time, LCFS heat-flux ratio and photon wall load cannot all be identified with a single balance without additional assumptions. Ignition is a reported source outcome, not independently reproduced by those rows.

## Original witnesses and identity

All page numbers below are one-based PDF pages. Stellaris printed and PDF numbering coincide. Images and text are saved under source-pages/ adjacent to this report; manifest.json contains source hashes and witness hashes. Text is a navigation aid; equation and table claims were checked visually on images.

| Source | Original file | SHA256 | Inspected material |
|---|---|---|---|
| Stellaris | knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf | 7fd72c1242ce3a17a9c4b9a4597fcb9ff5296b942b2d8343a0b463539d8d3865 | pp8–10,15–16,19,32; Table 4/5, Fig 15/16, Eq 2/3 and A.1–A.8 |
| Lion2021, Nucl Fusion61 126021 | Registered Origin Path in knowledge/SOURCE_INDEX.md:454 | db74f1c6d04aa505a763c9aa8a168f39324ef345aa3fe454d89bea2eabb18793 | PDF 4–5 (printed3–4), Eq 7–13 |
| Lion2023, thesis | Registered Origin Path in knowledge/SOURCE_INDEX.md:470 | 4eafe5a7c38b39c0d73307541b370e9adf3288cee2ac0ec059acf6c557de3bf0 | PDF 39–40 (printed31–32), Eq 2.6–2.13; PDF 151–152 (printed143–144), AppA |

The two ancestor originals remain at the exact /tmp Origin Paths recorded in SOURCE_INDEX; witness images/text and their hashes are durable in this goal. Both originals were hash-checked against the register. No third reference was followed. No relevant plasma-energy DI was found in the inspected knowledge register; this report does not promote or supersede an insight.

## Equations and their boundaries

Stellaris p32 Eq A.2 states p_rad+p_conf=f_alpha p_alpha+p_aux. Eq A.3 replaces p_conf with w/tau_E and p_alpha with E_alpha n_D n_T <sigma v>_T. E_alpha is explicitly 3.5 MeV; f_alpha is the fraction of total alpha power absorbed in the plasma. Table 4 p9 assumes f_alpha=0.95, distinct from the alpha fraction of total fusion energy. Eq A.5/A.6 prescribe helium generation, residence time tau_alpha*=8 tau_E and density suppression 0.5. Suppression changes ash density; it is not another 50% loss of alpha heating.

The source calls p both integrated and volume-averaged, printing <p>_V=integral_V p dV without a normalization factor. This is a notation inconsistency, not permission to mix MW and MW/m³. An unambiguous integrated reconstruction would use P_rad+W/tau_E=f_alpha P_alpha+P_aux throughout one common volume, with powers in MW, W in MJ and tau in seconds. The source does not provide a complete executable specification of that volume and the W used for Table 5.

Eq A.7 prints tau_E=0.134 f_ren a^2.28 B^0.84 iota_(2/3)^0.41 n_19^0.54 R^0.64 P^-0.61. The paragraph explicitly rewrites P=W/tau_E to obtain Eq A.8: tau_E=0.152 f_ren^2.56 a^2.72 B^2.15 iota_(2/3)^1.05 n_19^-0.18 R^0.08 T_keV^-1.56. The source does not state whether Table 5 was calculated with the rounded explicit A.8 coefficients or an exact implicit A.7 implementation, nor exactly how its temperature/density averages and species energy enter the conversion. Treat the two numerical implementations as distinct until established, not algebraically identical to printed precision.

Lion2021 PDF 5 Eq 7/8 independently shows P_conf+P_Br+P_line+P_sync=f_alpha P_alpha+f_nonalpha P_nonalpha+P_aux and P_conf≈P_scaling=W/tau_E. Eq 10 obtains W from V(3/2)integral_0^1 sqrt(g)n(rho)T(rho)drho, with species-averaged density and temperature; Eq 11 says sqrt(g)~rho. Lion2023 PDF 40 Eq 2.9–2.12 gives the analogous energy-density expression. These formulas support a thermal species-profile energy with no explicit fast-alpha term. They do not prove that Stellaris Table 5's total plasma energy excludes fast alphas. Stellaris p9 explicitly includes a fast-particle pressure model; p32 only calls W stored plasma energy. Its thermal/fast-alpha split remains missing.

Lion2021 Eq 9 and Lion2023 Eq 2.13 identify density as line-averaged electron density and B_t as toroidal field. Both print density exponent0.52; Stellaris A.7 and thesis AppendixA print0.54. This literal ancestor difference is recorded, not silently corrected or used to replace Stellaris. Lion2021 PDF 4 calls its macroscopic field parameter total magnetic field strength on axis. Stellaris Table 5 explicitly labels B0=9.0 T axis averaged. Its A.7 merely says variables have their usual meanings; no explicit mapping to a volume-averaged field or a different numerical field was found. Axis9 T is the stated anchor; an alternative averaging convention would be an agent assumption.

Thesis AppendixA PDF 151 says its volume is usually the confined volume up to a core radius. Stellaris AppendixA omits that clause and only says plasma volume. It is not valid to import the ancestor core cutoff into Table 5 as a confirmed fact. The ancestor supports the definition lineage, not hidden Table 5 implementation details.

## Point-A inputs and reported outputs

| Quantity | Original witness | Status for reconstruction |
|---|---|---|
| a1.3 m, R12.74 m, axis-average B9 T, V425 m³, plasma surface327 m² | Table 5 p10 | Supplied geometry/field; substituting these is source conditioning |
| Profile exponents alpha_T1.2, alpha_n0.35; Ti/Te0.95 | pp8–9 Eq 2/3 and text | Fixed assumptions; fuel-ion profile differs from ancestor electron-profile assumption |
| f_ren1.0, f_alpha0.95, residence ratio8, suppression 0.5 | Table 4 p9 | Explicit assumptions |
| Te0=15.40 keV, Ti0=14.63 keV, D0=T0=1.96e20/m³ | Table 5 p10 | Selected Point-A profile anchors |
| ne0=5.06e20/m³, volume-average ne3.17e20/m³, He0=0.56e20/m³ | Table 5 p10 | Reported composition outputs; holding them bypasses composition prediction |
| P_fus2700 MW, operating P_aux0 MW, Q infinity | Table 5 p10 | Reported source outcome; ignition claim |
| W504.65 MJ, tau_E1.46 s | Table 5 p10 | Reported outputs; thermal/fast split and exact averaging unspecified |
| P/S_LCFS(no edge radiation)=1.18 MW/m² | Table 5 p10 | Reported heat-flux ratio; P is not explicitly linked to W/tau in this row |
| Average photon wall power0.70 MW/m² | Table 5 p10 | Wall load, not labeled an integrated core radiation term; averaging area unspecified |
| Average neutron wall power2.87 MW/m² | Table 5 p10 | Another wall-load row; plasma area cannot be presumed wall area |
| Approximately 50 MW installed auxiliary to reach A | p9 Fig 15/text | Startup path requirement, distinct from zero steady operating power |

Table 5's caption says subsequent studies use Point A unless stated otherwise. This is same-design-point support, but does not erase different control volumes and conservative engineering scenarios. The p10 GENE/TANGO comparison fixes its fusion heating source and neglects radiation losses; it is explicitly not a fully integrated consistent temperature-profile prediction. It cannot independently close the 0.5D balance.

## Radiation and alpha conventions

Stellaris AppendixA and p9 use Aurora/ADAS line and continuum cooling plus the synchrotron model A.4. A.4 uses B in T, Te in keV, ne in1e20/m³, and a,R in m; its literal unit label W/m^-3 is typographically awkward, while the described quantity is a power density. The model evaluates profile-dependent radiation. No standalone integrated Point-A core-radiation value is printed in the inspected material.

Sections 2.6/2.7 use separate exhaust assumptions. Page15 assumes 90% of net core heating radiates before the divertor and illustrates 500 MW heating with 50 MW divertor demand. That500 MW is a rounded engineering illustration, not a replacement for Table 5 alpha arithmetic. The first-wall analysis instead assumes 100% of heating radiates to bound wall loading. Page16 separates computed profile-based core radiation (bremsstrahlung, tungsten, synchrotron) from a prescribed edge Gaussian near rho 1, truncated above 1. Geometry-integrated wall loads use Eq 7 and a different wall surface. These downstream scenarios must not be added to core losses a second time.

For total fusion-to-alpha power, thesis AppendixA PDF 151 explicitly states one fifth in good approximation. Stellaris p19 uses 2160 MW neutron power at 2700 MW fusion, consistent with an80/20 bookkeeping split. These support 0.2 as an approximate source convention; they do not establish an exact reaction-energy denominator for E_alpha=3.5 MeV. No source-supported exact replacement of the model's0.2002 follows from those facts alone.

## Arithmetic checks, explicitly conditional

The following are algebraic consistency diagnostics, not reproduced source calculations or proposed calibration. Assume for illustration alpha fraction0.2, f_alpha0.95, and all selected rows refer to the same integrated balance. Then P_alpha=540 MW and retained alpha=513 MW. W/tau=345.650685 MW. Zero auxiliary would REQUIRE core radiation167.349315 MW. That last number is inferred from the desired equality; it is not an independently supplied source radiation prediction and cannot earn prediction credit.

Multiplying the LCFS ratio by the listed plasma surface gives1.18×327=385.86 MW,40.209315 MW above W/tau. Multiplying the photon wall-load row by that same plasma surface gives0.70×327=228.9 MW. Forcing the latter into P_rad gives W/tau+228.9−513=+61.550685 MW, not ignition. Adding both flux-derived powers gives614.76 MW,101.76 MW above retained alpha. These inconsistencies disqualify the naive identification, not the source ignition claim itself.

As an independent warning against the area identification,2160/2.87 implies approximately 752.61 m² if the average neutron wall-load row were a total-power/area ratio, whereas the plasma surface is 327 m². This is a conditional implied area, not a measured wall area. The source does not give enough definitions to establish the area or averaging weighting of the photon row.

The paper provides no uncertainty bounds or explicit rounding rule for these rows. Under an EXTRA assumption of nearest rounding to the last displayed digit, keeping fixed geometry assumptions and0.2×0.95 retention, W/tau lies in[344.467577,346.841924]MW;1.18×327 in[383.6375,388.0875]MW;0.70×327 in[226.9175,230.8875]MW. These conditional intervals do not overlap the confinement-flux identification and cannot eliminate the tens-of-MW forced-balance mismatch. They are precision checks, not physical uncertainty bounds or justified acceptance tolerances. In particular2700 MW has no unambiguous significant-figure rounding interval. Do not infer±50 MW merely because its trailing digits are zero.

## Signed heating, limits and recommendation

[AGENT] Rearranging the stated balance defines signed P_aux_required=P_rad+W/tau−f_alpha P_alpha. Positive means additional plasma heating is needed; zero is the marginal self-sustaining condition; negative means excess retained heating at the prescribed point. Fig 15 labels an ignited high-temperature/high-density region, and p10 discusses burn control by fuel change or deliberate confinement degradation. This supports preserving the negative diagnostic and considering control requirements; it does not authorize clamping the balance residual to claim equilibrium, or establish a dynamically stable operating point whenever the residual is negative.

[AGENT] Recommend keeping radiation separate, retaining signed balance diagnostics, and diagnosing Table 5-conditioned W/tau independently from forward thermal W and confinement calculations. Do not install the inferred167.35 MW radiation or alter alpha retention to reproduce zero. Independent review should first decide which conditionally compatible substitutions are informative and explicitly approve any changed predicate semantics.

Missing evidence after the two-hop bound: exact Table 5 implementation and unrounded input/output vector; energy split and integration volume; whether A.8 or implicit A.7 produced tau; profile averages and field used in that computation; independently integrated core-radiation components and their impurity atomic-data settings; alpha/fusion reaction-energy normalization; definitions and averaging surfaces for both wall-power and LCFS rows; the source's signed-versus-clamped auxiliary reporting rule. These prevent a verified full source-conditioned ignition reconstruction from the printed table alone. Further arbitrary coefficients would be tuning, not evidence.

## Synchrotron expression requiring a source check before substitution

The p32 image literally prints A.4 as p_sync = 1.32e-7 (B Te)^2.5 sqrt(ne/a) [1 + 18 a/(R sqrt(Te))], followed by units a,R in m, Te in keV, B in T and ne in 1e20/m³. The square root covers ne/a; sqrt(Te) is in the denominator of the final correction. The power-density unit label is literally W/m^-3. These printed units and normalization need verification against cited ref [140] before installing or numerically attributing this formula: changing the density normalization under a square root changes the result by orders of magnitude. The coordinator reports the current model uses a different Albajar radiation expression; that implementation was outside this reader’s code ownership. Treat the difference as a candidate alternative assumption and an unresolved source prerequisite, not a justified numerical correction. The two-reference-hop allowance is exhausted, so ref [140] has not been fetched or inspected.
