---
date: 2026-09-18
researcher: Codex coordinator with independent source and method reviewers
topic: Computed tritium breeding in the retained helium/PbLi build
tags: [tritium, neutronics, blanket, validation]
research_type: domain-and-computational
---
# Retained blanket breeding: physical basis and limits

## Question

Can a defensible physical calculation make blanket choices affect tritium production and design adequacy without changing the intended blanket technology? Owner authority is the computed-tritium-breeding goal and its scientific-judgment delegation. ARIES and barred derivatives remain sealed.

## Findings

A continuous-energy neutron-transport calculation is available for an explicitly defined conceptual helium/PbLi torus. The isolated OpenMC0.15.2 engine and processed ENDF/B-VIII.0 data run separately from the sealed plant environment. Material inventories, geometry and the neutron source are explicit. This resolves the unavailable-transfer-function problem found in Round1 without transferring an inapplicable published TBR or fitting an arbitrary scaling law.

The five directly calculated blanket-thickness nodes increase from TBR1.0914469 at0.60m to1.2524488 at1.00m. TBR is tritium atoms produced in recoverable breeder lithium per fusion neutron. At the existing0.80m thickness, TBR is1.1980739 with Monte Carlo standard error0.0009642. These are conditional torus predictions, not qualification of an actual shaped stellarator. Source numerical evidence: `work/orchestration/goals/computed-tritium-breeding/evidence/round2/transport/table-validation.json` and its named original runs.

Six withheld transport points test the proposed piecewise-linear thickness interpolation. Every declared precision and interpolation criterion passes. The largest absolute residual plus twice its combined statistical standard error is0.00932074, below the predeclared0.01 allowance. The allowance is an empirical numerical screen over these checks, not a uniform physical confidence interval. Failed initial precision cases remain and are combined with independently seeded extensions under the recorded plan.

Independent experimental information supports only a limited consistency claim. Approximate reconstructions give0.697859±0.000489 for a lithium sphere versus measured0.685±0.03836, and0.504131±0.000478 for a lead/lithium sphere versus measured0.530±0.03180. The first error is Monte Carlo; the second is experimental. Missing exact casing and penetrations prevent calling this an exact benchmark reconstruction. One predeclared low-density Pb/Li sensitivity fails the two-standard-deviation diagnostic and remains in the record. No correction is fitted. Evidence: `evidence/round2/benchmark/report.md`, `results.json` and independent `benchmark-and-interface-review.md` under the goal.

## Sources and construction assumptions

Native research requests03/04/06/07 register original IAEA evidence, a primary UKAEA material publication, PNNL material cards, an official ATSDR carbide-density compilation, and official OpenMC data/tally documentation. Their registration records preserve original bytes, checksums, extraction and acquisition failures. The migrated IAEA proceedings landing page is explicitly not quantitative evidence. The original readme was mechanically rendered to PDF for native ingestion; its missing figure was not invented.

The design uses80%PbLi,10%EUROFER and10%helium by volume in the breeder; PbLi has15.8atom%Li and70%Li-6 enrichment within lithium. Source-supported material properties are distinguished from agent-selected representative volume fractions. The first wall contains2mm tungsten armor within its total50mm thickness. Reflector/shield use90%WC/10%helium. Exact inventories and citations are in `evidence/round2/transport/material-cards.json` and `material-manifest-proposal.md`. Material/source properties remain declared scenario assumptions; no implied actual engineering inventory is claimed.

Finite toroidal shells follow the existing generic radial build. A10.8degree missing-breeder window removes breeder, reflector and hot shield, while retaining the first wall. This explicit opening is a conceptual coverage case, not actual port CAD and not a scalar3% penalty. The source is isotropic14.06MeV with correct uniform-volume torus weighting. The outer torus transmits into exterior void; changing the distant vacuum boundary reproduces the same-seed result to roundoff. Tritium tallies distinguish breeder Li-6/Li-7 from nonrecoverable structural production. Joint batch covariance determines the combined standard error. Official H3-production and installed(n,Xt) scores are checked together on the actual lithium bins in `transport/tritium-semantics-check.json`.

## Applicability and uncertainty

The proposed executable domain supports breeder thickness0.60–1.00m only, with fixedR12.7m, a1.3m, circular cross section, remaining radial layers and immutable material/source/opening scenario. Changes outside that domain are undefined, never clamped or extrapolated. Enrichment, material fraction, opening arrangement and source profile sensitivities are direct-transport research cases, not extra validated interpolation axes.

Material and source uncertainty matters more than Monte Carlo precision near the requirement. The high steel/helium scenario predicts about1.069; the low steel/helium scenario about1.254. A peaked neutron source predicts about1.209 at the baseline build versus about1.195 in the matched uniform-source pilot. The final higher-history uniform baseline is1.198. These differences are not combined into a probabilistic plant uncertainty because no justified distributions or shaped-stellarator error bound exist. Evidence: transport sensitivity results and final report. Neutron energy multiplication remains the model's held1.2 assumption; this research does not infer new plant heat from breeding tallies.

## Adequacy semantics

The existing design floor1.05 and fuel-cycle requirement1.190 answer different questions. Under burn fraction0.05 and assumed recycle recovery0.99, exhaust loss is0.19 tritium atoms per atom burned. Unity extraction and zero decay inventory/reserve growth then require1.19 gross breeder atoms per burned atom. The original cost-derived recycle factor does not establish physical isotope recovery. This remains a conditional scenario, not measured fuel self-sufficiency.

The recommended check uses the stricter of the retained policy floor and calculated fuel requirement. Production, extraction loss, exhaust-recycle loss, radioactive decay and stock growth remain separate. At0.80m the numerical lower estimate1.1980739−2×0.0009642−0.01=1.1861456 fails1.190 despite the mean being above it. Thicker supported cases can satisfy this numerical condition without claiming full plant feasibility or physically qualified self-sufficiency.

## Recommendation and open work

Integrate the reviewed narrow response with explicit applicability and separate production accounting. Verify software against an independent interpolation/conservation implementation, while retaining the experimental and transport checks as the distinct physical evidence. Execute a focused native study and obtain a fresh unchanged-rubric assessment before claiming P3. Existing knowledge insights are not silently superseded; Round1 records the conflicting old coolant wording. This report remains pending in the native research workflow and promotes no domain insight by itself.
