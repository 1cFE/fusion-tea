# No screened ARIES alternative supports a whole-plant LCOE in the current model

**None of the 17 screened table entries can produce a supported whole-plant prediction with the unchanged model.** The decisive limit is breeding geometry, independently of the magnet problem. This is a limit of our model, not a finding that the ARIES designs are physically infeasible.

The screen covers Lyon Tables VII, IX and X, with Table VIII's component recipe and surrounding definitions. Repeated reference cases remain separate table entries; this is not a claim of 17 unique designs or an exhaustive search of all ARIES literature. [Source inventory and images](source-screen.md).

## Results by published family

| Published cases | Entries | Major radius | Current-model result |
|---|---:|---:|---|
| Reference plus full/tapered FS/He and SiC blanket alternatives, Table VII | 4 | 7.75–10.13 m | All outside breeding geometry support |
| ARE, SNS and MHH2 configurations, Table IX | 3 | 7.75–9.25 m | All outside breeding geometry support |
| FS/He power cases, 1–2 GW net, Table X | 5 | 7.75–10.90 m | All outside breeding geometry support |
| SiC power cases, 1–2 GW net, Table X | 5 | 7.75–9.42 m | All outside breeding geometry support |

The frozen breeding function accepts **exactly R = 12.7 m and a = 1.3 m**, together with eight fixed shape/layer coordinates. Within that geometry it interpolates blanket thickness between 0.60 and 1.00 m. None of the screened major radii equals 12.7 m. The implementation returns an undefined flag outside this domain; it does not calculate breeding at the new radius. Dependent fuel calculations therefore cannot establish a supported full-plant result. [Frozen rules and exact checks](domain-screen.md).

This also explains why broad depth targets were insufficient to establish applicability: the model has a computed, coupled breeding calculation, but its supporting response table covers one fixed geometry. More tabulated operating points do not extend that coverage.

## Three different questions

| Question | Answer |
|---|---|
| Do the sources provide a complete input specification? | No complete matched coil/current/equipment specification was established for an alternative. Partial nominal SiC pack-depth/case dimensions exist, but not a complete independent winding specification. |
| Can the numerical program run at one of these points? | **Not tested in this screen.** Static comparisons do not establish execution success or failure of every module. Some modules can return numbers while breeding is undefined. |
| Can the current model support a whole-plant comparison? | **No for every screened entry.** Each fails the necessary breeding-radius condition. Other scientific and correspondence limits remain. |
| Does the selected equipment pass engineering checks? | **Not evaluated for these alternative rows.** No additional plant run was performed. |

Holding missing inputs at model defaults would define another transferred scenario, not reconstruct a published alternative. No input was fitted or inferred from the desired output, and no scientific range was expanded.

## The magnet limitation also remains

The seven Table VII/IX peak-field entries are 11.4–16 T, below the selected REBCO approximation's 20–32 T interval. That comparison concerns the published fields and our selected product's interval; it is not a prediction of what our field calculation would output at those geometries. The published magnets use different technology. Table X reports axis field only, so its 10 T values cannot be used as conductor peak fields.

The source tables lack a complete independent specification of currents, turns and pack geometry. Scalar-radius proximity does not qualify the existing field approximation for another coil family. See [source sufficiency](source-screen.md) and [other domain limits](domain-screen.md).

## What is still possible without new coil data

A financial-accounting test could supply published capital costs, annual expenses and electricity and compare the resulting electricity-cost calculation. It would test economic conventions under supplied inputs, not independently predict ARIES hardware or plant performance.

That test requires a mapping first. ARIES's published capital includes construction financing in its total/direct multiplier; the model DCF expects overnight capital and adds construction interest separately. Direct substitution would mix those bases. Lifetime, availability and annual-versus-lifetime cost conventions also need reconciliation. [Economic screen](economics-screen.md).

The source's material recipes and structural drawings can support narrower subsystem checks when input meanings match. They do not by themselves supply the missing complete input deck. The completed assessment already uses architecture, dimensions and component-cost scope comparisons.

**Recommendation:** do not spend the remaining assessment time running another full-plant ARIES point. The static domain check already establishes why it cannot give a supported LCOE. Include this explicit coverage finding in the write-up. Treat any later financial-only reconciliation as a separate accounting task, with no independent plant-prediction credit.

## Evidence, review and replay

[Every screened entry](evidence/screen.csv) has a separate record for source completeness, new numerical execution, scientific applicability and engineering status. [Full JSON](evidence/screen.json) retains the source data and exact rule identities. [Independent review](evidence/review.md) checks this bounded conclusion. [Preservation receipt](evidence/preservation-after.json) verifies that all 1,350 protected files are unchanged. No model or previous result changed; no new plant run, push or merge occurred.

Reporting-only replay, from the repository root:

```bash
.codex-test/run python .project/active/aries-comparison-preparation/alternative-point-screen/evidence/domain-screen.py
.codex-test/run python .project/active/aries-comparison-preparation/alternative-point-screen/evidence/screen.py
```

The first script reads frozen source and performs scalar guard comparisons; it does not execute model functions. The second joins those rules to the visually checked source inventory. Source transcriptions and interpretations remain review obligations beyond arithmetic replay. [Findings log F028–F030](findings.md).
