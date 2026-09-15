# T-005 — source-backed cryogenic engineering scenario

**2026-09-15 · [AGENT] technical proposal under the owner's delegated judgment.** Proceed with a conventional-metal, conduction-cooled current-lead scenario, a 77 K shield/intercept, and explicit steel thermal bridges. This is an executable engineering estimate, not a qualified Stellaris cryostat design. The nominal scenario deliberately exceeds ideal lead heat and the NASA warm-insulation benchmark; low/high cases expose the principal choices. All scenario values below are agent choices unless identified as sourced or inherited.

## Admitted primary evidence

Native request `knowledge/research/requests/REQ-MCR-LEADS-02.json`; return `knowledge/research/requests/runs/REQ-MCR-LEADS-02/20260915T135952089105/return.json`: `REGISTERED`, three successful captures, two searches, no queue. Source registration and Git staging were coordinated with the root agent.

- **Lead physics:** `knowledge/sources/current_leads_links_and_buses_ballarino/`, A. Ballarino, *Current Leads, Links and Buses*, author copy https://arxiv.org/pdf/1501.07166. Original p1 verifies Wiedemann–Franz–Lorenz law `kρ=L0 T` and `L0=2.45e-8 W Ω K⁻²`. Original p3 has actual typographical inconsistencies: equations 5/6 divide the left side by current while retaining current inside the square root; equation 3 prints a temperature derivative where spatial differentiation is needed. These are not extraction errors and must not be copied into the model. Pages 2–4 establish vacuum conduction cooling, intermediate heat sinks, nominal-current optimization, and the need for measured material properties to realize geometry. The paper discusses practical low-current applications; this source does not qualify a manufactured 50 kA lead.
- **Correct formula witness:** `knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/`, same author's CERN lecture, original slide 14. It prints the spatial heat balance and `Qc,min=|I|sqrt[L0(Th²−Tc²)]`, with zero warm-end conductive flux. The printed room-temperature/liquid-helium example of approximately 47 W/kA agrees dimensionally and numerically. Use this verified slide as the equation authority.
- **Steel conductivity:** `knowledge/sources/nist_316_stainless_cryogenic_material_properties/`, original NIST table rendered from registered `raw.html`. Conductivity uses `k(T)=10^(Σa_i(log10 T)^i)` in W/(m·K), coefficients `[-1.4087,1.3982,0.2543,-0.6260,0.2334,0.4256,-0.4658,0.1650,-0.0199]`. Printed data range 4–300 K, equation range 1–300 K, 2% fit error relative to data. Using 316 conductivity for a conceptual 316LN support is an explicit material proxy, not demonstrated equivalence.
- **Radiation and insulation:** existing `knowledge/sources/layered_thermal_insulation_systems_for_cryogenic/`, NASA original slide 21, prints the two-surface radiation term `σ(Th⁴−Tc⁴)/(1/εh+1/εc−1)` alongside gas and solid-conduction terms. Slide 20's high-vacuum MLI benchmark is below 1 W/m² at 300/77 K. This supports the form and a warm-boundary reference; it supplies neither the selected emittance nor a 77/20 K measured flux.

Original page images and NIST browser sidecar are retained in the native run's `inspection/`. NIST static table is complete and legible; missing navigation/plot resources and file-origin CORS errors are recorded in its sidecar. No missing plot was used. `scenario.py` and `scenario.json` retain the numerical calculation. Sources are admitted by native capture, not by web-search snippets.

## Equations and accounting

Let `I` be the winding **turn current in A**, currently 50,000 A, not coil ampere-turns. Let `N=12` leads: two terminals for each of the six source-verified series groups. Six groups are sourced in Stellaris original p25; two terminals per group is the stated engineering topology assumption. The current model varies turn count at fixed turn current, so varying coil ampere-turns does not change these lead loads.

For two separately optimized resistive segments, choose `Tc=20 K`, `Ts=77 K`, `Ta=300 K`:

- `QL,c = fL N |I| sqrt[L0(Ts²−Tc²)]` W to the cold stage.
- `QL,s = fL N |I| sqrt[L0(Ta²−Ts²)]` W to the warm intercept.
- `Plead,direct = QL,c + QL,s` W of supplied resistive electricity for this scenario. At the ideal optimum each segment has zero heat entering its warm end, so no lower-segment conductive term is subtracted at the intercept. `fL>1` is a lumped excess-dissipation allowance, not an asserted solution for an as-built off-optimum lead. Do not infer resistance or manufactured dimensions from that allowance.

At fixed hardware, the paper says standby/off-nominal current behavior depends on material properties. These equations describe a lead sized at each candidate design current; they are not a time-history model of installed hardware. Conventional leads carry higher cryogenic losses than a suitable HTS design, but no universal HTS improvement factor is assumed.

Choose a high-vacuum cold gap with no interlayer spacers; radiation is `QR,c=A_c εeff σ(Ts⁴−Tc⁴)`, with `εeff=(1/εh+1/εc−1)⁻¹` and `σ=5.670374419e-8 W m⁻² K⁻⁴`. Explicit thermal bridges are modeled separately. For the warm jacket, `Qin,s=A_s qMLI`; its **net** refrigeration contribution is `QR,s=Qin,s−QR,c`. This subtraction conserves energy: heat radiated onward to the coil is not also removed by the shield refrigerator. Require nonnegative net stage heat in the scoped scenario; a negative value indicates that the assumed shield requires heating or a different thermal model. Warm MLI heat flux includes its insulation's radiation/gas/spacer contributions; do not add them again.

For each support segment, Fourier conduction gives `QC,support=Gc∫Tc^Ts k(T)dT` and `Qin,support=Gs∫Ts^Ta k(T)dT`, with `G=ΣA_support/L_support` in metres. The warm stage removes `QS,support=Qin,support−QC,support`. Nominal exact integrals are 307.436740008 W/m at 20–77 K and 2704.713065690 W/m at 77–300 K. A simple implementation may bind mean conductivities **5.39362701769** and **12.12875814211 W/(m·K)** and multiply by segment ΔT. Holding the cold mean while varying Tc over 10/20/30 K gives +11.99%/0/−9.21% error in the support heat compared with reintegration; this is a disclosed approximation on the support contribution, not a whole-plant error. Do not extrapolate these means to a moving intercept without a new source integration.

Finally, with cold and warm thermal powers in W, `Pe,added = Qc(Ta−Tc)/(ηc Tc) + Qs(Ta−Ts)/(ηs Ts) + Plead,direct`. Convert to MW once at the output. The existing nuclear/joint cold heat remains separately accounted. Existing `p_tf=0` explicitly leaves lead and joint direct electricity uncounted (`models/designs/stellarator_09/stellarator_plant.sysml:650`). Recommend including both lead direct power and existing 7.5 kW joint direct power once in the inventory's electrical term; refrigeration of those same watts is a different consumption. Do not also add them to `p_tf`. Conversion loss of the electrical supply remains outside this unity-efficiency direct-load estimate.

## Concrete parameter choices

All values in this table are **[AGENT] engineering assumptions**, except the existing temperatures/current where noted. The bounds are sensitivity cases, not confidence limits or safety bounds.

| Parameter | Low | Nominal | High | Meaning |
|---|---:|---:|---:|---|
| Leads N | 12 | 12 | 12 | Six sourced groups × assumed terminal pair; no 96-lead interpretation. |
| Coil/intercept/ambient K | 20/77/300 | 20/77/300 | 20/77/300 | 20/300 inherited; 77 chosen to match insulation witness and fixed segment means. |
| Lead excess factor fL | 1.0 | 1.25 | 1.5 | Ideal to extra dissipative load; not HTS qualification. |
| Effective cold-gap emittance | 0.02 | 0.05 | 0.10 | Clean low-emittance surfaces through degraded finish; assumed, unqualified. |
| Warm MLI qMLI W/m² | 0.5 | 1.0 | 2.0 | NASA benchmark context; nominal at its stated upper benchmark, high installation degradation. |
| Gc and Gs per coil, m | 0.01 | 0.04 | 0.16 | Four gravity-support thermal paths per coil, each 1 m per segment, nominal area 0.01 m² per path; low/high alter area by ×0.25/×4. |
| ηc and ηs, fraction Carnot | 0.30 | 0.20 | 0.15 | Nominal retains current model choice; range tests plant performance, not guaranteed efficiencies. |

**Geometry [AGENT]:** use existing per-coil winding length `c_coil`; set `A_c=n_coils c_coil 4(b_wp+2t_case)` with conceptual casing allowance `t_case=0.10 m`. Set warm-shield area `A_s=1.2 A_c`. These expose actual area and do not equate winding-pack volume to cold surface. Hold nominal support topology and per-path area/length while changing plasma size; this is an anchored thermal bridge, not a structural sizing law. Revise it if the structure model supplies an actual ground-support geometry. The scenario covers warm-to-cold gravity supports; inter-coil structures entirely at 20 K create no warm-to-cold bridge by themselves. Penetrations/vacuum quality beyond the explicitly chosen surface scenario and nuclear heating of cases/supports remain residuals; this scenario is not a comprehensive cryostat design.

## Numerical witness

Illustrative geometry: 48 coils, 25 m per coil, `b_wp=0.50 m`, casing allowance 0.10 m; therefore `A_c=3360 m²`, `A_s=4032 m²`, turn current 50 kA. This is a transparent calculation point, not a claim to reproduce the current generated model's exact pack dimension.

| Added term | Low | Nominal | High |
|---|---:|---:|---:|
| Lead cold heat kW | 6.983 | 8.729 | 10.475 |
| Radiation cold heat kW | 0.133 | 0.333 | 0.667 |
| Support cold heat kW | 0.148 | 0.590 | 2.361 |
| Total additional 20 K heat kW | 7.264 | 9.653 | 13.503 |
| Net additional 77 K heat kW | 30.264 | 42.340 | 66.654 |
| Lead direct electricity kW | 34.214 | 42.767 | 51.321 |
| Additional wall power MW | 0.665 | 1.332 | 2.598 |

Wall-power row includes both refrigeration stages and lead direct electricity. It excludes the existing nuclear/joint refrigeration and the recommended additional 0.0075 MW joint direct supply. Nominal result is principally lead cooling; changing support mean conductivity within the quantified 10–30 K approximation error is secondary. No value was fitted toward an external cryoplant total or toward feasibility.

**Implementation recommendation [AGENT]:** use this nominal scenario and expose low/high parameters. Replace the old unnamed non-nuclear uplift with these explicit terms; label any retained residual separately rather than multiplying newly counted loads again. The known case/support nuclear-heating gap cannot be numerically bounded by these sources and must remain disclosed, or receive a separately justified volume/heating scenario. Acceptance is of this declared engineering estimate, not of a complete source-anchored Stellaris cryogenic design.
