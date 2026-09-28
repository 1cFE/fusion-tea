# T-002 — current model accounting

[AGENT] Inspection complete, 2026-09-17. This record describes implemented equations and existing numerical evidence. It makes no new source-definition ruling and authorizes no correction. No production file changed and no model evaluation or study ran. The holdout protocol and mixed-source exclusion were applied; the excluded note was not read or recovered.

## Result

The Table 5-conditioned case requires **44.00380775886009 MW** of plasma-coupled operating auxiliary heating. Its exact accounting is **213.9323790635418 MW radiation + 325.2127094323997 MW confinement loss − 495.14128073708144 MW retained alpha heating**. The source fusion, W and tau numbers are comparison values, not inputs to these three computed terms.

The complete eight-case inventory, including downstream outputs and predicate verdicts, is [inventory.json](model-accounting/inventory.json). The nine-decimal table is [controls.md](model-accounting/controls.md). [inventory.py](model-accounting/inventory.py) only reads the prior native record and performs arithmetic; rerun with `.codex-test/run python work/orchestration/goals/stellaris-plasma-power-balance/evidence/model-accounting/inventory.py`.

## Exact producers and boundaries

Paths below are repository-relative. `oracle` means `exploration/stellarator_e2e/verify_stellaris.py`; `manual` means `exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py`. `sustainment` means `models/library/analyses/mfe_plasma_sustainment.sysml`.

| Term | Implemented meaning and producer | Classification and open distinction |
|---|---|---|
| Fusion power, MW | `P_fus = n_D0 n_T0 V E_fus integral(u^(2 alpha_n) sigv(T_i0 u^alpha_T) 2 rho d rho) / 1e6`; Bosch–Hale reactivity, oracle:81,97,1066; manual:228; E_fus=2.817e-12 J bound at `models/designs/stellarator_09/stellarator_plant.sysml:864`. | Predicted from supplied peaks, profile and geometry; no held 2700 MW. The retained manual calculation and public fusion calculation use the same contract. Legacy sigma_v>0 bypass exists at oracle:1067 but is inactive for these controls. |
| Fuel, helium and electrons, m^-3 | `n_D0=n_T0=(n_e0−2n_He0)/2`; ash shape `S=u^(2 alpha_n) sigv(T_i)/sigv(T_i0)`; electrons `2n_D0 u^alpha_n +2n_He0 S`; oracle:181,194,229; manual:174,188,231. | Peak electrons supplied; fuel/ash predicted. Pointwise quasineutrality neglects trace tungsten charge. Supplied Z_eff is not derived consistently from every species. |
| Ash amount | Damped fixed point `n_He0=f_suppr tau_ratio tau_E n_D0 n_T0 sigv(T_i0)`; oracle:213; manual:207. | f_suppr=0.5 and tau_ratio=8 are held source facts. Uniform particle/energy confinement ratio in radius is the implemented reading; ash follows fusion births, not a fitted ash exponent. |
| Stored thermal energy, MJ | `W=1.5 V <p>_V /1e6`; pressure contains electrons plus D, T and thermal He, with Te=Ti/0.95 and effective-radius `dV/V=2rho d rho`; oracle:203; manual:199; sustainment:48. | Predicted thermal species sum. Fast-alpha energy and trace impurity pressure excluded. Effective-radius volume measure and thermal-only convention come from admitted sister-code ancestry; they are not independently established as Stellaris's full implementation. |
| Confinement time, s | `C=0.134 f_ren a^2.28 B^0.84 iota^0.41 R^0.64 n_bar19^0.54`; `tau=(C W^-0.61)^(1/0.39)`; line average of derived electrons; oracle:189–209; manual:184–204. | Predicted; a,R in m, B in T, n_bar19 in 10^19 m^-3, power in MW, W in MJ. f_ren=1.0. W/tau is the explicit confinement term in the implemented balance; the source reader must confirm that control volume before source substitutions. |
| Retained alpha heat, MW | `0.95 * 0.2002 * P_fus`; oracle:261; sustainment:91,205. | Alpha retention is separate from helium suppression. Lost fast-alpha energy is excluded from core heating. Plant thermal alpha uses the slightly different exact ratio 3.52/17.58, oracle:1073. |
| Bremsstrahlung, MW | `1e-6 V 5.35e-37 Z_eff integral(n_e^2 sqrt(Te) dV/V)`; oracle:250; manual:253. | Z_eff=1.20 is supplied. Uses Te in keV; coefficient unit W m^3 keV^-1/2. |
| Tungsten radiation, MW | `1e-6 V f_W integral(n_e^2 Lz(Te) dV/V)`; oracle:126,254; manual:257. | f_W=7.76e-6 supplied. Piecewise coronal cooling fit inherited from admitted library ancestry, called “line” in the model. Original-source agreement and continuum overlap are not established by code inspection. This is 110.2179 MW of the Table 5 core radiation. |
| Synchrotron, MW | Albajar formula with effective electron exponent `n_e0/<n_e>−1`; oracle:137,258; manual:261. | Wall reflectivity 0.6, elongation 1.0 and tokamak-fit application are held assumptions, not Stellaris fitted data. Uses n_e0/1e20. |
| Signed auxiliary, MW | `p_rad + W/tau − p_alpha_heat`; oracle:262; manual:267; sustainment:95. | Computed signed core heating demand; no floor or clamp. |
| Installed and operating heating | Installed: wallplug × source efficiency × coupling plus direct coupled input; operating: signed demand divided by coupling, then source efficiency; `models/library/analyses/mfe_heating_chain.sysml:65,88`; oracle:1085–1096. | 100 MW installed electrical ×0.5×1.0 =50 MW installed coupled. Table 5 operating demand is 44.0038 coupled /88.0076 electrical MW. Installed capacity does not enter the core balance. |

Numerical contract: trapezoidal integration over 200,000 radial intervals, double precision, Bosch–Hale temperature floor 1e-6 keV, ash absolute tolerance 1e12 m^-3, 200-iteration cap and half-step damping (`sustainment:115`). The W cooling curve has its own 0.01 keV floor and explicit piece boundaries at 0.1, 1 and 10 keV (`oracle:126`). Their source accuracy is distinct from quadrature precision.

## Existing controlled attribution

The entering control uses alpha_n=0.33, alpha_T=1.19, R=12.7 m and V=425.0000143721807 m³. Exact profiles use 0.35 and 1.2. The Table 5-conditioned group also supplies R=12.74 m, holds a=1.3 m, sets the shape factor to recover V=425 m³ and adjusts current to retain B=9 T. These are grouped source conditions, not independently predicted geometry. Case definitions are `exploration/stellarator_e2e/studies/20260916-stellaris-reference-reconciliation/execution/prepare.py:20`.

| Ordered change | Delta radiation MW | Delta W/tau MW | Delta minus-alpha MW | Delta auxiliary MW |
|---|---:|---:|---:|---:|
| Entering → exact profiles | −5.569599883 | −6.622776177 | +8.285313293 | −3.907062768 |
| Exact profiles → Table 5 conditioning | −0.219666277 | −2.013476852 | +1.064412868 | −1.168730261 |

These differences telescope exactly along the tested path: 49.079600788 →45.172538020 →44.003807759 MW. They include each group's live ash/confinement interactions. They do not establish order-independent contributions of individual profile exponents or geometric inputs. The selected-reserve magnet variants have identical plasma terms; their economics differ. The two existing off-reference controls give 55.663445303 MW at R+2% and 34.270313421 MW at a+2%, both starting from exact profiles and retaining their declared other inputs.

## Downstream accounting

The divertor ledger receives retained alpha plus signed operating auxiliary, subtracts core radiation to form separatrix transport, and distributes a supplied 90% total radiated fraction into core and edge destinations. Radiation is not added as generation. The fixed-geometry peak is the supplied 9.5 MW/m² case scaled by nonradiated incoming power/50 MW; 99% capture sets deposition and equivalent area together. Exact producers: `models/library/analyses/mfe_divertor_heat.sysml:9,43`, oracle:23. At the Table 5 legacy case: absorbed heat 539.145088496 MW, separatrix 325.212709432 MW, target incoming 53.914508850 MW, deposited 53.375363761 MW, peak 10.243756681 MW/m². The peak screen fails. It is not total target-load qualification; radiation deposition remains omitted.

The plant thermal boundary recovers total alpha energy, multiplied neutron energy and operating auxiliary, plus primary pump heat (`models/library/analyses/mfe_power_balance.sysml:118,138,190`; oracle:1108,1142). It differs deliberately from retained alpha at the core boundary. Table 5 reactor source heat is 3063.833207983 MW; recovered pump heat 164.994755971 MW gives thermal power 3228.827963954 MW. The electric cycle gives 1328.199544871 MW gross, 1004.162026549 MW net; recirculating loads include operating electrical heating (`oracle:1158`). Legacy LCOE is 144.656523419 $/MWh; its exact financial numerator and energy denominator are at oracle:1359–1367. These are model outputs with retained engineering qualifications, not validated source economics.

The upper sustainment predicate checks demand≤installed coupled heating (`models/library/analyses/mfe_viability.sysml:276`). Burn Hold checks demand≥0 (`:343`). At exact zero both pass. A negative demand is an unsupported hold point with surplus heating, not a claim that ignition is impossible. Table 5 legacy violates divertor peak, reference conductor current and winding-pack fit; the other recorded predicates pass. Every variant's full verdicts are preserved in the inventory. Existing magnet/casing, conductor, cooling applicability and divertor omissions are not repaired by plasma reconciliation.

## Earlier answers retained

[INHERITED: `work/orchestration/goals/stored-energy-basis/{goal,trail,learnings}.md`] WI-042 already replaced the former flat ash profile with the source-rule profile and derived electrons by quasineutrality. Its historical 90.6→49.1 MW change must not be offered again as a new correction. The earlier 518.3 MJ reconstruction used printed peaks, whereas the current 513.0 MJ Table 5 case closes its ash amount; those numbers describe different conditioning. The earlier source-rules calculation could not reproduce printed W=504.65 MJ. Its possible volume-measure/core-radius/fast-alpha distinctions remained unresolved, and the printed beta/W comparison did not establish a tunable correction.

[INHERITED: `work/orchestration/goals/operating-point-closure/learnings.md`, L-001/L-002; WI-042 design] ISS04 uses line-average electrons. Replacing that with volume average previously missed tau by about −23%. Forward sustainment was chosen after solving temperature proved unsuitable at that model state. A constant W multiplier cannot predict new closure locations or even all off-reference signs; stored-energy L-006 records explicit counterexamples.

[INHERITED: `work/completed/20260907_WI-043_two-sided-sustainment-condition/design.md`; current Burn Hold producer] The lower bound is an operating-point hold condition. It already admits exact ignition and preserves signed over-heating diagnostics. No present evidence supports deleting it to reproduce ignition.

## Recommended discriminating diagnostics, not authorized execution

[AGENT] After source-reader compatibility checks, evaluate frozen-state source-term substitutions algebraically: total fusion/retained alpha, W, tau, and a jointly compatible W/tau pair. Holding all else fixed, more fusion lowers demand; lower W lowers it; lower tau raises it. The printed tau=1.46 s is lower than 1.5774 s, so substituting it alone increases demand. A fully source-conditioned residual needs compatible radiation and alpha conventions; model radiation must remain labeled model-supplied if used.

[AGENT] Separate frozen-state arithmetic from closure-live diagnostics. In the latter, W changes tau and ash, and ash changes fuel dilution, radiation and fusion. Report the difference as interaction; do not add isolated changes without checking the combination. An initial finite arithmetic matrix can include singles, compatible pairs and their grouped total without creating new model entry points.

[AGENT] Source evidence for tungsten cooling and its separation from bremsstrahlung is a useful discriminator because the modeled W channel is large and the fit is piecewise. Comparing original radiation coefficients/definitions is preferable to sweeping f_W or reflectivity. The 0.2002 versus 3.52/17.58 alpha ratio discrepancy is small by inspection; quantify separately if source convention warrants, never use it as a fit lever. No supported rounding interval was established by this task.

## Evidence identity and reuse

Current canonical and staged sustainment hashes match. Current oracle bytes match the prior study's captured oracle. Exact SHA256 values are in inventory.json. The prior native study records pin `6e427038e8515501e9c42c39823f85e3b0bcbd9f54f830b2779a792851f02551`, semantic fingerprint `8ea7a4c353455698deaa1026d3d3d547d572e08c6ceb58c2bb9cfea26c0120e0` and executable fingerprint `f52729e684f513d1b210c75f523340085786440fa2828490309b96493755fd14` in preparation/integration-return.json. Its results/oracle-all-points.json records eight cases, 1808 scalar and 160 exact predicate comparisons, maximum relative difference 4.3655745685100556e-14, no failures. This inspection does not freshly certify the entire generated package identity.

[AGENT] If the coordinator verifies that full identity is unchanged, the existing native results are sufficient control evidence; fresh oracle checks are optional confirmation. Repeating identical native controls supplies no additional attribution. Changed semantics, changed package identity or downstream effects of an actual correction require new native/generated/oracle checks and finite off-reference controls. The present inventory is not a new study and grants no prediction credit to supplied source values.

### Printed-fuel arithmetic diagnostic

[AGENT] At the coordinator's requested printed D/T density 1.96e20 m^-3 (source authority remains T-001), the Table 5 model's computed D=T=1.920874169510505e20 m^-3 explains the direction of much of the fusion deficit. Holding the existing temperature profile, geometry and reactivity integral fixed, quadratic rescaling gives `2603.4033373840975*(1.96e20/1.920874169510505e20)^2 = 2710.539664829757 MW`. This is 10.5397 MW above the printed 2700 MW. Thus the same reactivity/profile integral nearly reproduces the printed fusion power when supplied the printed fuel peaks. It is a useful discriminator for ash dilution, not proof of correct reactivity.

Changing only the fusion contribution in the frozen balance adds 20.376258116889957 MW retained alpha heating and leaves 23.627549641970134 MW demand. This calculation does not reclose quasineutrality, stored energy, radiation or ash. It is a partial source-conditioned arithmetic diagnostic, not a realizable native operating point or an independent forward prediction. The model's helium peak is 6.091258304894951e19 m^-3, so the fuel difference is coupled to its ash closure. The full model electron volume average is 3.1201534250473076e20 m^-3 and its line average 3.741613961070496e20 m^-3; these are distinct conventions.

The coordinator separately reports the current sealed identity, 179 captured snapshot artifacts, 12 indicator files and all production scopes matching the prior study in `evidence/reuse-check.json`. That check supplies the full-identity prerequisite above; it was not rerun by this task.
