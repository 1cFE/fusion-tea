# Stellaris reference reconciliation study

Eight native cases completed; 0 pass all twenty raw predicates. These are conditional reconstructions and local sensitivity checks. Published-reference qualification remains unresolved.

| Case | LCOE $/MWh | Total capital $ | Raw failures |
|---|---|---|---|
| legacy-control | 144.747431 | 8905077000.15 | divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok |
| selected-reserve-control | 163.194229 | 10298783892.97 | divertor_heat_ok, wp_fit_ok |
| exact-profiles-legacy | 144.616024 | 8836818928.94 | divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok |
| exact-profiles-selected-reserve | 163.218513 | 10230525653.83 | divertor_heat_ok, wp_fit_ok |
| table5-conditioned-legacy | 144.656523 | 8843672993.22 | divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok |
| table5-conditioned-selected-reserve | 163.295231 | 10240131189.97 | divertor_heat_ok, wp_fit_ok |
| offref-R-plus2pct | 145.927487 | 9028705854.66 | divertor_heat_ok, reference_conductor_current_ok, sustainment_ok, wp_fit_ok |
| offref-a-plus2pct | 141.940118 | 8959507124.38 | divertor_heat_ok, peak_field_ok, reference_conductor_current_ok, wp_fit_ok |

| Case | Fusion MW | Required auxiliary MW | On-axis T | Minimum fit margin m | Pump MW |
|---|---|---|---|---|---|
| legacy-control | 2652.563263 | 49.079601 | 9.000000 | -0.120000 | 175.280934 |
| selected-reserve-control | 2652.563263 | 49.079601 | 9.000000 | -0.285309 | 175.280934 |
| exact-profiles-legacy | 2608.999914 | 45.172538 | 9.000000 | -0.120000 | 166.241132 |
| exact-profiles-selected-reserve | 2608.999914 | 45.172538 | 9.000000 | -0.285309 | 166.241132 |
| table5-conditioned-legacy | 2603.403337 | 44.003808 | 9.000000 | -0.120566 | 164.994756 |
| table5-conditioned-selected-reserve | 2603.403337 | 44.003808 | 9.000000 | -0.285972 | 164.994756 |
| offref-R-plus2pct | 2706.509296 | 55.663445 | 8.823529 | -0.120000 | 187.233589 |
| offref-a-plus2pct | 2653.463537 | 34.270313 | 9.000000 | -0.120000 | 172.964783 |

All costs use the retained model basis. Water cooling hardware and local cavity/conductor qualification remain unpriced; tape procurement price is assumed and account price years differ. `results/case-summary.csv` retains magnet procurement, heating, pumping/cycle and capital responses alongside every scalar.

| Contrast | LCOE change $/MWh | Raw predicate changes |
|---|---|---|
| legacy-control → selected-reserve-control | 18.446798 | reference_conductor_current_ok: violated → satisfied |
| legacy-control → exact-profiles-legacy | -0.131407 | none |
| selected-reserve-control → exact-profiles-selected-reserve | 0.024284 | none |
| exact-profiles-legacy → table5-conditioned-legacy | 0.040499 | none |
| exact-profiles-selected-reserve → table5-conditioned-selected-reserve | 0.076718 | none |
| exact-profiles-legacy → offref-R-plus2pct | 1.311463 | sustainment_ok: satisfied → violated |
| exact-profiles-legacy → offref-a-plus2pct | -2.675906 | peak_field_ok: satisfied → violated |

`results/contrasts.json` defines the allowable attribution for each contrast. The selected cases enable current-driven inventory sizing plus 1% inventory reserve. The legacy-to-selected cost change belongs to that joint intervention, not to the reserve alone. Reference-effective tapes rise from 112.708720 to 239.983701 and tape procurement cost rises from $731,571,428.57 to $1,557,689,763.85 at the control. These are not the exact historical selected-mode control at multiplier 1. Source radius, volume shape and current conditioning change together and cannot identify a radius-only effect. The two off-reference checks change one geometric attribute each.

All 1808 mapped scalar comparisons and 160 exact predicate comparisons pass. Sixteen native scalars remain outside the oracle map. Results verify implementation, not engineering qualification. Complete source applicability is in `results/case-predicate-applicability.json`; no filtered feasibility pass is calculated.

| Supplied source case | Deposited MW | Uncaptured MW | Peak-equivalent area m² |
|---|---|---|---|
| high-temperature | 49.500000 | 0.500000 | 5.210526 |
| low-temperature | 48.500000 | 1.500000 | 9.700000 |

Both paired source cases supply 500 MW input and 90% radiation. Their capture/peak pairs are 0.99/9.5 MW/m² and 0.97/5 MW/m². Supplied peaks earn accounting consistency only; the derived area is not measured wetted geometry. `results/source-conditioned-divertor.json` preserves temperature and diffusion pairings.

The exact historical selected-entry diagnostic is retained separately in preparation. Its current-boundary sign discrepancy is not corrected by tolerance or relabeled a pass. It is reused history, not a ninth native study case.
