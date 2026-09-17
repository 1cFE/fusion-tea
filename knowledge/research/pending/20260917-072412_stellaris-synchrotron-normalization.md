---
date: 2026-09-17
researcher: plasma_source
topic: stellaris-synchrotron-normalization
research_type: original-source
tags: [radiation, stellarator, units]
---

# T-005 — original synchrotron normalization

Date: 2026-09-17. Status: author source reconstruction complete; independent review pending. [AGENT] Findings below resolve a unit convention, not a change to the production model. Scope follows synchrotron-brief.md and T-005 in trail.md. Previous T-001 report is preserved.

## Result

Zohm's original Eq (6) uses MW for integrated synchrotron power. Dividing it by plasma volume gives MW/m³ with the coefficient 1.32e-7 and density normalized to 1e20 m^-3. Substituting A=R/a reproduces the algebra of Stellaris Eq A.4. The latter's printed W/m^-3 label is inconsistent with that normalization. A literal watts interpretation produces a result one million times smaller than the cited formula. Changing the density to an unnormalized SI number is not the justified remedy.

The original also fixes wall reflectivity at 0.8 and uses volume-average temperature. This resolves the units prerequisite for a labeled comparison, but does not establish that integrating the expression locally over Stellaris profiles reproduces the source's calculation.

## Source and native evidence

Original: H. Zohm, “On the Use of High Magnetic Field in Reactor Grade Tokamaks,” Journal of Fusion Energy 38 (2019), 3–10, DOI 10.1007/s10894-018-0177-y. Retrieved original journal PDF from the German National Library, https://d-nb.info/1178904288/34. Publication metadata also checked against https://link.springer.com/article/10.1007/s10894-018-0177-y. These are two locations for one source, not additional citation hops.

Raw SHA256: a598bc99d8324346e99dcde2085f5e7a9c2dbb82f4a2458ab1dc8a85e7d5b9bc. Native registered extraction: knowledge/sources/on_the_use_of_high_magnetic_field_in_reactor_grade_tokamaks/. Extract SHA256: e3b8d6ebff0bf8fddc1f5fb322e340a6bd00a74c0936f3b8f36949f05ec7374a. Native request: knowledge/research/requests/REQ-STELLARIS-PLASMA-SYNC-01.json. Run and return: knowledge/research/requests/runs/REQ-STELLARIS-PLASMA-SYNC-01/20260917T142147780849/. Registration used scripts/source_registry.py and wrote the raw artifact, source extraction, manifest and index through the owning operation.

Witnesses: synchrotron-pages/zohm-p2.png is PDF page 2, journal page 4; the equation and units were inspected visually. Pages 1 and 3 provide model scope and the investigated domain. Matching text files are navigation aids. The witness manifest records hashes. One initial acquisition failed because the restricted shell could not resolve the host; its authorized network retry succeeded. Registration succeeded on its first attempt. No further references were followed. Quarantine was reread before fetching; a content-free scan found zero held-source name/host matches in the original. No holdout or excluded mixed-source note was opened.

## Equation and exact conversion

Original Eq (6), journal page 4:

```text
P_syn = 1.32e-7 (B T_ave)^2.5 sqrt(A n_e / R)
        * [1 + 18 / (A sqrt(T_ave))] V
```

The unit convention printed under Eq (1) on the same page is MW, keV, 1e20 m^-3, T, m. The surrounding radiation equations use the same power convention: Eq (3) computes bremsstrahlung with coefficient 5.35e-3 and volume V; Eq (5) gives a cooling coefficient in MW m³; the paragraph after Eq (6) sums all three contributions. The temperature T_ave is explicitly volume averaged in the paragraph introducing Eq (2). The factor 1.3 T_ave used for the fusion-reactivity approximation is not the temperature printed in Eq (6).

With A=R/a and q_syn=P_syn/V, the same expression becomes:

```text
q_syn [MW/m^3] = 1.32e-7 (B T_ave)^2.5 sqrt(n_e / a)
                * [1 + 18 a / (R sqrt(T_ave))]
```

For q_syn in W/m³ with these same normalized inputs, the coefficient is 0.132. This is a unit conversion, not a fitted coefficient. For an implementation returning total MW, use the first form or integrate a separately justified density form with consistent units; do not apply the million-fold conversion twice.

## Assumptions and transfer limits

The text immediately following Eq (6) specifies wall reflectivity 0.8. That assumption is already embodied in the stated expression; an extra reflectivity factor would need an explicitly derived change. The original does not expose a free reflectivity exponent in this equation.

The model is a 0D reactor-grade tokamak model. Its geometry uses major radius, aspect ratio and toroidal field, and the page-4 footnote assumes ITER-shaped volume scaling. The cases investigated on journal page 5 keep A=3.1. This establishes the study's tested domain, not a universal prohibition on other aspect ratios. Stellaris uses A about 9.8 and imposed radial profiles. Neither original provides validation here for local evaluation on those profiles or an exact specification of how Stellaris adapted the average-temperature formula.

The original's synchrotron relation is distinct from the alternate Albajar expression identified by the coordinator's model reader. This report does not independently inspect that implementation or infer numerical differences. A comparison must retain its own geometry, profile integration, reflectivity and unit assumptions. Source unit repair alone does not justify declaring the alternate correlation erroneous.

## Recommendation and remaining gap

[AGENT] Permit an independently reviewed, explicitly labeled source-law diagnostic using the resolved MW convention. Preserve the current correlation as a separate assumption unless later evidence justifies replacement. Report global-average application and any local-profile adaptation as different cases if both are evaluated; do not equate them silently.

The exact Stellaris implementation, profile averaging and integrated Point-A synchrotron output remain missing. Its printed unit label can be reconciled to its cited ancestor, but its intended numerical result cannot be certified from the publication alone. No model, generated package, oracle or study was changed by this task.
