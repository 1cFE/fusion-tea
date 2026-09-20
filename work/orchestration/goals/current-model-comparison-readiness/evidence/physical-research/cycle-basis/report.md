---
date: 2026-09-19
researcher: Codex physical-interface agent
topic: Kovari helium Rankine cycle basis
tags: [physical-interface, source-applicability, Rankine]
research_type: bounded-primary-source-check
---

# Cycle-basis source check

The 62 bar/171°C feedwater/42°C sink screening case is **not established as a match to the cycle behind the Kovari efficiency fit**. The newly captured Dostal report illustrates a materially different steam cycle. Transplanting that illustrated cycle unchanged into the current salt span produces a negative cold-end temperature gap. This is source-applicability evidence, not a revised plant design.

## Question and authority

[INHERITED: parent T-003 research instruction] Determine whether Dostal MIT-ANP-TR-100 (2004) and Porton EFDA 2M4XFP (2012) establish pressure, feedwater, regeneration, sink and heat-grade assumptions behind Kovari's helium-primary Rankine fit. The bounded task permits four targeted searches and two primary captures, with no model changes or new physical assumptions. The request is `knowledge/research/requests/REQ-COMPARISON-KOVARI-CYCLE-BASIS.json`; its completed run is `knowledge/research/requests/runs/REQ-COMPARISON-KOVARI-CYCLE-BASIS/20260920T004633797736/`.

## What the primary sources establish

Kovari explicitly attributes the helium-primary superheated Rankine modeling to Dostal et al. [10], with a 0.0179 efficiency penalty to agree at one point with benchmark [6], Porton et al. These are distinct roles. This attribution is visible in the retained original `work/orchestration/goals/plant-closure/evidence/grounding_sources/kovari2016_p9_table4.png` (PDF page 9, journal page 17), and the registered extraction `knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md:329`. The temperature fit, its 384–642°C stated range, and its 20 K helium-to-steam difference do not themselves supply a matched steam-generator state set or a part-load map.

The [original MIT report](https://web.mit.edu/22.33/www/dostal.pdf) was retrieved, screened and registered as `knowledge/sources/dostal_driscoll_hejzlar2004_mit_anp_tr100_cycle_report/`. Its raw SHA-256 is `80401528cc9af65f0f3b873b9f31c50d65710f12ecb0bd3c586f9cee87e16d7c`. The source has 326 PDF pages. The relevant section is **Chapter 12, §12.2**, not Chapter 6 as mistakenly anticipated in the capture metadata. The original page images and `original-page-locators.json` beside this report provide the checked locators.

| Original source location | Checked observation | Applicability limit |
|---|---|---|
| PDF 282 / printed 263, `dostal-p282.png` | §12.2 distinguishes the superheated steam cycle from the supercritical steam cycle and attributes the former to earlier Dostal work. | Parameters of the separately described supercritical cycle cannot be transferred to the helium Rankine fit. |
| PDF 284 / printed 265, Figure 12.8, `dostal-p284.png` | The illustrated superheated Rankine cycle labels main steam at 15 MPa and feedwater entering the steam generator at 280°C. It includes turbine stages, a reheat arrangement and regenerative feedwater heating. Other visible heating labels are 80, 130, 180 and 230°C. | This is a representative cycle diagram. The exact regression dataset and the state assumptions at every Kovari fit point have not been reproduced. |
| Same figure | A 30°C label appears on the condenser side; intermediate pressure labels include 3 MPa and 1 MPa, and the feed-pump discharge is labeled 16 MPa. | The 30°C label alone is insufficient to reconstruct cooling-water approaches, condenser pressure and all rejected-heat accounting. It is not the screening case's demonstrated 42°C sink. |
| PDF 283 / printed 264 and PDF 285 / printed 266, `dostal-p283.png` and `dostal-p285.png` | The comparison uses cycle efficiency because the needed net-efficiency data were unavailable. The text warns that steam cycles need additional supporting equipment and station loads. Figure 12.10 compares cycle efficiency against turbine inlet temperature. | Do not treat the source curve as a complete plant net-efficiency map or assume exact agreement with a separately solved simple Rankine cycle. No curve digitization or refitting was performed. |
| PDF 319 / printed 300, `dostal-p319.png` | The bibliography lists earlier Dostal cycle studies. | Earlier-reference year labels are inconsistent with the report's front catalog; tracing another report was outside this bounded capture. |

## Quantified incompatibility with unchanged transplantation

The current fourteen-circuit admission screen fixes salt leaving the steam generator at 269.664729914530°C, before the salt pump raises it to 270°C. See `../screening/results.json`, `../screening/README.md` and the entering baseline cited there. Pairing that cold end with Figure 12.8's illustrated 280°C feedwater gives:

`ΔT_cold = 269.664729914530 − 280 = −10.335270085470 K`.

[AGENT inference] The current countercurrent steam generator cannot admit this illustrated feedwater state over the unchanged salt span: its cold end would require heat to move from colder salt into hotter feedwater. This failure precedes any proposed positive minimum-approach criterion. It is a conditional transplantation check, not proof that every state underlying the Kovari fit has this same failure.

The v2 62 bar/171°C screen remains internally calculable, with a 20 K minimum gap and required UA of 47.786926 MW/K at 445°C steam. Its conditional fit electricity demands 93.9244% of the admitted water-exergy increase. Neither that necessary exergy test nor the positive heat-admission result validates the fit for this different cycle. The new source evidence strengthens the reason to retain that distinction.

## Retrieval result and boundary

Four targeted searches and one primary capture were used. The admissible MIT PDF passed the content-free quarantine screen recorded in `dostal-screen.json`. The cited original Porton identifier endpoint, `https://user.efda.org/?uid=2M4XFP`, was actually attempted with a 30-second retrieval limit. It returned no body and failed with curl status 28 / HTTP 000. The bounded searches found bibliographic references but no captured primary Porton report. This is a failed retrieval in this run, not evidence that the report is universally inaccessible. The native run closes as REGISTERED with the Dostal source and a queued Porton retrieval failure; the four-search limit was reached.

## Decision supported by this evidence

1. **Retain a restricted conditional package.** [AGENT option] Keep the independently checked heat-admission screen and expose the Kovari-derived electricity/LCOE only as conditional calculations for an unmatched cycle. This is useful for tracing model arithmetic and identifying sensitivity. It cannot support a claim that the current integrated plant has demonstrated cycle performance, and it requires explicit acceptance of that limitation before canonical adoption.
2. **Establish and solve a coherent matched cycle.** [AGENT option] Resolve a steam-cycle state set, regeneration/reheat, sink and internal-work convention that can receive the current salt heat; then calculate its efficiency or acquire evidence that validates a surrogate for that state set. The illustrated Dostal cycle cannot simply be substituted unchanged. This is additional scientific scope beyond the current fit and bounded admission screen. It must preserve the current salt span unless separately authorized.

[AGENT recommendation] Preserve the conditional package for review, and leave demonstrated electricity/LCOE readiness unresolved. Do not convert the 62 bar screen into a matched-cycle claim. The choice between accepting restricted conditional results and commissioning a coherent cycle solution is material because it changes what the comparison is allowed to conclude. This report adopts neither option and changes no canonical assumptions.

The focused active-knowledge check found no existing insight claiming these exact fit states. A proposed future insight is: “A heat-admission calculation validates the exchanger state path; transfer of a cycle-efficiency fit additionally requires cycle-state and work-boundary applicability.” Its model implication is separate admission and efficiency-applicability status; its analysis implication is that a positive pinch and exergy ceiling are necessary but insufficient evidence for gross electrical performance. No knowledge insight has been approved or superseded.
