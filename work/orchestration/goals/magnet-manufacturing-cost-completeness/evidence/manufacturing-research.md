# T-002 manufacturing evidence and bounded recommendation

2026-09-15 local / 2026-09-16 UTC. Consumer: REQ-MFG-01. [AGENT] Recommend a separately visible inter-pancake sheet-stock purchasing scenario. Retain the historical winding-rate estimate with explicit transfer uncertainty. Ground wrapping, resin/process costs and fixed cabling remain unpriced scope. This is a useful partial estimate, not factory completeness or qualified insulation construction.

## Native return and scope

Native class **REGISTERED**: `knowledge/research/requests/runs/REQ-MFG-01/20260916T020828587277/return.json`. Eight searches, three capture attempts, two registered sources. The run closed with `adequacy=exhausted` after examining the targeted supplier/process routes; this is a bounded investigation, not an exhaustive literature claim. No native bounded-negative file exists because sources registered. The winding-law and fixed-cable conclusions below are scoped evidence negatives within this report.

- Registered supplier: `knowledge/sources/k_mac_g10_fr4_glass_reinforced_sheet_catalog/`, including `raw.html` and `output.md`.
- Registered process source: `knowledge/sources/iter_a_to_z_on_assembling_its_largest_components/`, including `raw.html` and `output.md`.
- Queued: `https://www.cryogenicg10.com/sheets.htm`, native capture failed with `UnicodeDecodeError` for a non-UTF-8 copyright character. No extracted contents or price from that candidate are adopted. A successful future capture and qualification review could improve the material scenario; it does not block the explicitly ordinary-grade scenario.

Only source_registry wrote source directories/index/manifest. No model, test, PM, goal trail or insight registry changed. No sealed paper, barred source or external account-justification document was opened. Supplier catalogs and the ITER production article were screened as construction-only candidates before native capture; registry hold-out screening accepted both adopted sources. Web results were used for triage only. The final raw-HTML/PDF checks and native close/report exceeded the initial 35-tool-operation working target to resolve source fidelity and finish bookkeeping; no search or capture limit was extended.

## Source facts checked against originals

| Evidence | Verified fact | Authority and applicability |
|---|---|---|
| Registered Stellaris PDF `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, p.22, Figure40 and §2.9 | Figure40 labels 0.5mm insulation above a 20mm unit cell. The text places insulation between pancakes and electrical contact between radial turns. The conductor is a presoldered stack in copper, placed in nonplanar SS316 radial plates. | Original p.22 image inspected during this task. No radial turn insulation is indicated. Material identity of the yellow sheet is unspecified. |
| Same PDF, p.22 Table7 | Tape/copper/solder/steel/helium fractions 9/35/12/36/8 percent sum to100. | Original image checked. An additional sheet scenario must be outside this existing material volume; simply adding another fraction inside it double-counts occupancy. |
| Same PDF, p.23 Table8 | Six square pack sides:360,360,340,340,320,300mm. | Original p.23 image checked. Reuse as normalized set-shape distribution only; do not freeze original turns or sizes while the current model changes current/density/field scaling. |
| K-Mac `raw.html`, catalog row KS-6383; `output.md:48` | Ordinary G10/FR4 sheet,0.020in thick,12in by12in,listed$5.73. | Original HTML table row parsed and compared to extraction. Catalog is a supplier price for sheet stock; no cryogenic/radiation magnet qualification, labor, freight, tax or manufacturing yield supplied. |
| ITER `output.md`, PhaseOne through PhaseThree, and matching `raw.html` | Winding and insulation wrapping require synchronized speed and tension control; conductor terminations are shaped after winding; pancakes undergo impregnation, stacking/joining and further assembly. Size, handling and dimensional tolerances complicate production. | Primary project article dated3February2012. Raw HTML checked for the relevant passages. Describes insulated NbTi PF coils; its process is not the NI REBCO construction. |
| Existing `knowledge/sources/the_design_of_the_superconducting_coil_system_for/output.md`, §§2.2,2.5,3–4 | Actual title is *Experiences from Design and Production of Wendelstein7-X Magnets*. Curved joints made hand insulation difficult; geometric tolerances, inspection, repair and worker qualification affected production. | Existing registered primary production report. Qualitative process evidence used here; no W7-X thickness, labor rate or cost transferred. |

The Stellaris image itself leaves the published square envelope versus added sheet pitch ambiguous. WI061 already represents an excluded-sheet interpretation with transverse build fraction0.025. That choice remains an assumption. This research does not resolve it into a source-established manufactured envelope.

## Recommended sheet quantity and price

[AGENT] A clearly labeled material-cost scenario is supportable. It is not a qualified procurement forecast. Use current geometric pack volume `V`, before additional sheets, with the existing set-distribution and selected-envelope scaling applied exactly once. For uniform fractional extra build `fx,fy` occupied entirely by sheet material:

```text
V_sheet = V * ((1+fx)*(1+fy)-1)
A_sheet = V_sheet / t_sheet
C_sheet_stock = A_sheet * price_sheet_per_area
```

[AGENT] For the NI construction use `fx=0`, `fy=0.025`, and `t_sheet=0.0005m`. This is one0.5mm sheet per20mm transverse cell in the continuous approximation. It includes an end-sheet convention and is not an integer pancake bill of materials. With `fx=0`, the identity is also `A_sheet=V/0.020m`; it follows from the chosen sheet pitch, not original published turn counts. If the sheets are interpreted as already included, set the additional build to zero and record that this incremental inventory is zero. Do not silently change tape/metal fractions to make room for both interpretations.

[DERIVED] The quoted sheet area is `(12*0.0254)^2=0.09290304m²`; quoted thickness is`0.020*0.0254=0.000508m`. Thus the catalog area rate is`5.73/0.09290304=61.67720668774671USD/m²`. No density assumption is needed. The0.508mm product is a near-size purchasing proxy for the0.500mm geometric sheet scenario. That1.6% thickness difference is disclosed; using it as the actual installed product requires updating thickness/pitch and checking fit together, rather than claiming the existing fit represents that SKU.

[AGENT] Price convention: **catalog observed2026-09-16 UTC, used as a nominal2026 purchasing scenario**. The page has no verified publication/quotation year. No CPI escalation is warranted from an unknown origin date. It is not a confirmed current bulk offer. Waste/cutting/seams, cryogenic-grade substitution, irradiation qualification, delivery and installation remain unresolved. A price multiplier is an analyst scenario, not a supplier confidence interval. Keep price sensitivity separate from sheet pitch, thickness, occupancy and current geometric volume sensitivity.

[AGENT] Sheet stock already contains its cured laminate resin. Do not add a second epoxy-material charge for that laminate. Free resin/adhesive/impregnation elsewhere is different material/process scope and has no adopted quantity or price here. The2mm assembly gap is free clearance, not purchased resin or insulation.

## Ground-shell geometry, deliberately unpriced

[DERIVED] The source side distribution gives mean side divided by maximum side `f_perimeter=(.36+.36+.34+.34+.32+.30)/(6*.36)=0.9351851851851851`. Its area counterpart is`0.8780864197530865`; a perimeter factor is not the existing area factor or current factor.

[AGENT] If a future quantity output is useful, let current nominal maximum dimensions be`x=s*sqrt(r)`, `y=s/sqrt(r)`, common ground thickness`t`, equal modeled circumference`c`, and coil count`n`. Assume the six relative side ratios persist uniformly, with the same aspect ratio and internal fractional build for every coil. Then:

```text
V_ground = n*c*(2*t*f_perimeter*(x*(1+fx)+y*(1+fy)) + 4*t*t)
```

This integrates the rectangular shell around each scaled pack section in the simplified equal-length set. The corner term uses all coil lengths and is not multiplied by the perimeter factor. Use the current `s`, aspect ratio, count and circumference; any selected-envelope area scaling must enter `s` consistently once. If current `V` cannot be reconciled with `n*c*s²*area_factor`, expose that inconsistency before treating this as a coherent inventory. Actual varying circumference/shape requires a coil-by-coil sum. Ground geometry alone does not identify sheet versus glass wrap/resin construction. **No ground price is recommended**, and the internal-sheet stock rate must not automatically price this shell or its installation. The3mm thickness is the inherited geometry scenario, not newly qualified ground insulation.

## Winding effort and fixed cable: bounded evidence result

[INHERITED] PROCESS source paths are `knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307` and `knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724`. Prior original-source checks and scope are preserved in `work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/accounting-research.md`. It supports conductor-length accounting and the historical480USD1990/conductor-m coefficient, with separate conductor and casing terms. The current CPI ratio and1.9 nonplanar transfer factor remain inherited assumptions.

[AGENT] Retain `L=n*I*f_set*c/I_turn` and `C_wind=L*rate_1990*escalation*transfer`. Current, turn count and circumference affect conductor length through this identity. The primary process evidence supports additional possible drivers: terminations/joints, number of pancakes, bend/handling geometry, tolerances, insulation method and inspection/rework. It supplies no calibrated relation that converts conductor section, turn count beyond length, joints or nonplanarity into labor hours or money for this construction. No cross-section multiplier is justified. A lower machine feed speed or a project calendar duration alone would not establish paid effort, staffing or factory cost.

[AGENT] Keep winding-rate/transfer sensitivity explicit. Do not call the PROCESS coefficient a labor-only rate, or claim it covers every listed process. Material-stock addition has a known purchasing boundary, but historical winding-rate coverage is not detailed enough to prove zero overlap with all insulation material/installation; disclose that residual instead of subtracting an invented allowance.

[AGENT] Do not adopt PROCESS fixed-cable80USD/m. The current presoldered field-aligned stack, copper former and radial-plate construction needs a fabrication sequence/rate beyond purchased tape and separately priced material. Neither Stellaris nor the captured process sources establish80USD/m as that remainder. The75USD/m sheath term overlaps the explicit steel material scope. Both exclusions leave a named unpriced manufacturing remainder rather than establish zero cost.

[AGENT] The independent account map owns the steel review: `evidence/account-map.md`. Its6USD/kg fabricated-steel wording and separate factor3 do not supply an operation inventory, so this research neither certifies a duplicate nor removes a term. The nonmagnet structure budget remains an explicit allowance. No overall manufacturing-completeness claim follows from the sheet addition.

## Acceptance boundary for implementation

[AGENT] Implementing the internal-sheet stock scenario is scientifically honest if the UI/report names it as unqualified ordinary G10/FR4 stock proxy, exposes its incremental volume/area and price separately, preserves existing material/tape quantities, and carries the ground/cable/process exclusions. Verify sheet-price changes only the sheet charge; changes in current-sized volume change sheet quantity; zero additional build removes only incremental sheets; winding-rate changes remain independent. Ground geometry may be reported without a price. A later qualified supplier quote and manufacturing route would replace these assumptions rather than retroactively certify them.
