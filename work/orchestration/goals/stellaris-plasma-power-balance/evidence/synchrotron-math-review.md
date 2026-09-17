# Supplemental independent source/math review

2026-09-17. Reviewer: `/root/clean_coordinator/plasma_reviewer`, continuing fresh non-author. Judgments are [AGENT]. Scope: synchrotron-review-brief.md; same quarantine and exclusions as the initial review. No production change or new plasma evaluation was made. Read-only source inspection began under the coordinator's initial task message before the supplemental brief was deposited; the review paused on request and resumed after that brief arrived. No diagnostic execution was released in that interval.

## Verdict and exact release

**PASS for two explicit alternative radiation diagnostics. No production correction is justified by this evidence.** The initial review's normalization prerequisite is resolved for these calculations. Exact Stellaris implementation and integrated Point-A radiation remain missing.

1. Evaluate original Zohm Eq6 with the Table5-conditioned model state's geometry, B=9 T, volume-average electron temperature and volume-average electron density. Specify temperature as the unweighted volume average, `Te0/(1+alpha_T)`, under the current effective-radius measure. Map density to the model's `<ne>_V/1e20` explicitly as an application assumption; the inspected original does not independently establish that density averaging convention. Do not use peak or density-weighted temperature silently.

2. Evaluate a separately named local-profile interpretation of Stellaris A.4 with the frozen derived electron and temperature profiles, normalized density and `dV=V*2rho drho`. This is a sensitivity calculation for an unverified adaptation of a global radiation correlation. It is not a second verified source implementation. With coefficient 1.32e-7, the local expression returns MW/m³. Its zero-temperature endpoint can be evaluated through the equivalent finite expression proportional to `sqrt(ne20/a)*B^2.5*(Te^2.5+(18a/R)*Te^2)`; no arbitrary temperature floor is needed for this diagnostic.

Hold all other radiation, confinement and alpha terms fixed. For either case report `delta_aux = Psync_alternative - 14.187588254589881 MW` and `A_alternative = 44.00380775886009 MW + delta_aux`. Retain signed outputs. No thermal/electric/LCOE prediction or changed predicate follows from these held-state calculations. Review the resulting numbers before final interpretation.

## Original evidence and limits

I visually inspected original Zohm PDF pages1–3 in synchrotron-pages/. Page2 (journal p4) shows Eq6, the MW/keV/1e20 m^-3/T/m unit convention, volume-average temperature definition and wall reflectivity0.8. Algebraic substitution `A=R/a` and division by V reproduce Stellaris A.4's functional form. Consequently coefficient1.32e-7 corresponds to MW/m³; W/m³ would require coefficient0.132 with those same inputs. Stellaris's printed watts label conflicts with its cited original normalization. Changing density to SI or converting MW twice is not a remedy.

The reviewed synchrotron-source.md SHA256 is `3f8d72a0e720a227cec73ee8a63f4b840f29e5c08fd21328d4c0ccc9f488834e`; its six witness hashes and report hash match the manifest. The native REGISTERED return identifies source SHA256 `a598bc99d8324346e99dcde2085f5e7a9c2dbb82f4a2458ab1dc8a85e7d5b9bc`. This review inspected retained original-page witnesses and registration identity; it did not independently rerender the raw PDF.

The original is a tokamak scoping model, with its examined scenarios at aspect ratio3.1. Applying it at Stellaris aspect ratio9.8 remains a transfer assumption. The current Albajar implementation uses reflectivity0.6; the source expression embeds0.8. A numerical difference combines correlation, reflectivity, geometry and averaging choices. It cannot be attributed solely to a coefficient or unit error in the production model. No extra reflectivity factor is authorized.

## Completed finite diagnostics

T006 diagnostics.json SHA256 is `8f83954d5fc022898156b8f6345d714d6e5844c046f93c150de11326f11cf9d8`. I inspected diagnostics.py, independently rechecked all1130 saved scalar comparisons and100 saved predicate comparisons against the prior native cases, and recomputed the four balance combinations and both W/tau paths. All pass. This independently checks recorded comparisons, not a fresh rerun of the oracle.

The paired confinement change is +20.4379754991 MW, fusion-power change at the model alpha fraction is −18.3717192629 MW, and the approximate source alpha-fraction change is +0.513 MW. They carry the44.0038077589 MW model demand to46.5830639950 MW. The W/tau interaction is −0.4257985887 MW. The printed-fuel rescaling and conditional rounding calculations are consistent with the released scope. None supplies missing core-radiation evidence or establishes ignition.
