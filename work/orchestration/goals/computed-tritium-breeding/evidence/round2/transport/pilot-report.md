# Toroidal transport prototype and pilot evidence

2026-09-18. This report records numerical execution and direct physical scenarios. It does not itself certify the independent benchmark, shaped-stellarator applicability, or adequacy. The fresh method precheck authorized the prototype; `table-freeze.md` fixes the smaller proposed production response domain.

## What executes

`plant_transport.py` constructs the current circular-average radial build as finite OpenMC ZTorus shells in centimetres. It retains the 2 mm armor within the 50 mm first-wall envelope, explicit source void, all material layers, surrounding void, and a convex vacuum boundary. `material-cards.json` freezes the registered constituent cards and chosen volume fractions. Natural elements expand explicitly using OpenMC 0.15.2 abundances before checking cross-section coverage; missing nuclides never silently renormalize the composition. Fourteen supplementary Ta/P/S/Mo isotope files, 94,773,584 bytes, are pinned and hashed in `data-selection-extra.json` and `data-manifest-extra.json`; the combined runtime now indexes 54 isotope files. Full composition/density/temperature and number-density expansions are recorded in each case manifest.

The uniform source uses native cylindrical radial density proportional to radius and rejection into the plasma torus. `source-verification.json` records one million candidate samples: acceptance 0.785577 against π/4, analytical moments within 0.77 standard errors, and direct ZTorus membership checks. `geometry-verification.json` records two million random-volume samples, layer-volume comparisons within five standard errors, actual CSG point ownership, and retained central-hole void. `opening-verification.json` verifies 8,000 point assignments for each opening layout, unchanged first-wall material, and exact removed breeder volume 22.261090118745063 m³ at the baseline.

Useful production is Li-6 plus Li-7 `(n,Xt)` in the breeder only. A separate paired 10,000-history check (`tritium-semantics-check.json`, model and full engine log alongside) scores documented `H3-production` in those same isotope/filter bins. Both isotope means and reported standard errors agree exactly with `(n,Xt)` on the installed 0.15.2 engine and selected data. This establishes the aliases for this execution, not a claim about arbitrary processed libraries. Separate all-material and all-breeder production tallies retain excluded tritium. Per-batch isotope tallies are retained and the combined mean/standard error is computed with their covariance, not by adding independent component variances. `verify_tallies.py` independently checks isotope means and errors against OpenMC, the combined covariance, absence of lost-particle warnings, and the neutron balance `1 + nu-scatter - scatter - absorption - leakage`. The completed cases checked so far close that balance below 5e-13 per source neutron. Raw statepoints remain under ignored `.codex-test/breeding-transport/plant/`; compact batch realizations, model XML, material manifests, logs and resource use are captured under the evidence results directories.

## Diagnostics

All table entries below are TBR mean ± one Monte Carlo standard error, each from 100,000 histories in 50 batches. The geometry/material/source scenario is a declared conceptual assembly. All nuclear data are the pinned processed ENDF/B-VIII.0 NNDC data, not a FENDL calculation.

| Case | Recoverable TBR | Meaning |
|---|---:|---|
| Full coverage | 1.24677 ± 0.00380 | Diagnostic upper-coverage assembly |
| Independent full-coverage seed | 1.25383 ± 0.00437 | Difference consistent with sampled uncertainty |
| Enclosing sphere 30 m instead of 20 m | 1.24677 ± 0.00380 | Same-seed mean differs by about 1.2e-15 |
| One 10.8° toroidal opening | 1.19529 ± 0.00306 | Breeder/reflector/HT-shield replaced by void, first wall retained |
| Two opposite 5.4° openings | 1.19455 ± 0.00325 | Equal removed volume; layout difference unresolved at this precision |

A multiplicative 0.97 applied to the full-coverage result would give approximately 1.20937, around 0.014 above the explicit single-window result. That multiplier is not used. The single opening is the fixed table scenario because it is the simplest explicit contiguous opening representation; it is not a claim about actual ports. At baseline the transport scenario removes 3% of breeder and reflector inventory, while an unchanged full-shell cost calculation would still charge it. The production integration must identify that conservative cost convention or align the inventory.

## Direct physical sensitivities

All cases here use the single opening and otherwise retain the reference inputs. Each is a new independent 100,000-history run. Small differences are unresolved when they are comparable with their combined Monte Carlo errors; this table is not a fitted uncertainty distribution.

| Case | Recoverable TBR | Changed assumption |
|---|---:|---|
| Breeder 90% PbLi / 5% EUROFER / 5% He | 1.25366 ± 0.00339 | Both nonbreeder fractions at their low scenario endpoint |
| Breeder 60% PbLi / 20% EUROFER / 20% He | 1.06911 ± 0.00385 | Both nonbreeder fractions at their high scenario endpoint |
| WC density −5% | 1.19432 ± 0.00400 | Representative solid-density sensitivity |
| WC density +5% | 1.20078 ± 0.00395 | Representative solid-density sensitivity |
| Ideal-gas He at 8 MPa / 773.15 K | 1.19791 ± 0.00345 | Replaces source-card helium density only |
| Exterior 0.2 m SS316 after 0.1 m gap | 1.20191 ± 0.00316 | Hypothetical additional backscatter; not a reconstruction of outer components |
| Li-6 atom fraction 0.60 | 1.17022 ± 0.00353 | Direct enrichment response, outside the final table's fixed enrichment |
| Li-6 atom fraction 0.90 | 1.23717 ± 0.00406 | Direct enrichment response, outside the final table's fixed enrichment |

The material-volume fractions and enrichment visibly affect breeding. The WC, helium-density and exterior-steel differences require more histories if their signs or magnitudes are decision-critical. These comparisons do not bound an arbitrary stellarator shape change. The centrally peaked source gives **1.20907 ± 0.00317**, compared with the uniform-source single-window pilot **1.19529 ± 0.00306**. It samples the existing plant fusion emissivity using alpha_n 0.33, alpha_T 1.19 and peak ion temperature 14.63 keV. The 500,000-particle bank has the exact toroidal Jacobian; its normalized minor-radius-squared moment differs from independent quadrature by 1.20 standard errors. A finite source bank adds a separate sampling term that this one pilot does not independently bound. The roughly 0.014 TBR shift reinforces the conditional source claim. Provenance and bank digest are in `peaked-source-provenance.json`.

## Runtime and repairs

The first full-coverage torus pilot took 34.144 seconds in the engine: 4.8615 seconds for initialization and 29.235 seconds for active histories, approximately 3,421 histories/second. It used a provisional WC card at 15.6 g/cm³ while source acquisition finished. The subsequently registered authority gives that same number; subsequent cases use the frozen sourced card. The provisional result is retained as a throughput check, not substituted for a final table node.

Four parallel two-thread diagnostics each took about 57–61 seconds, with baseline maximum resident memory 766,424 KiB. The last split-window run took 38.6 seconds as contention reduced. Actual timings, rather than the much faster two-isotope sphere smoke, govern the table budget.

Two setup defects were repaired and their failed artifacts retained: OpenMC pads intermediate statepoint batch numbers (`statepoint.01.h5`), so the first successful pilot's reader required a filename fix; and OpenMC's source-file writer checks sequence length, so the first peaked-source generation required a list instead of a generator. Neither repair changed a material card or transport result to improve agreement. The source retry has a distinct case name. Failed attempts remain in ignored runtime logs.

The frozen table uses five thickness nodes and six independent withheld points. The initial numerical precision target is 0.002 absolute TBR standard error, tightened to 0.001 within 0.02 of the reference conditional requirement 1.190. The baseline's margin is small, and the table's numerical allowance may leave it unresolved. Physical scenario spread remains separate and can change an adequacy conclusion even when numerical interpolation passes.
