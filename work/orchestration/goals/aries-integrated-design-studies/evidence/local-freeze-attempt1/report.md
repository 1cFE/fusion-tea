# Local response of the assumed integrated ARIES baseline

[AGENT executor interpretation] All 24 declared native points completed and pass all-point numerical verification. Fourteen pass all 14 evaluated engineering checks; ten retain heat-removal failures. Scientific qualification remains absent at every point. This is a post-reveal conditional study of the unchanged reviewed package, not a validated reactor design.

The baseline remains **423.106794 MW assumed integrated baseline**. Reducing either purchased exchanger area from 50,000 to 45,000 m² saves 8.690529 million USD2004 overnight and 0.190957 USD2004/MWh in each fixed fuel scenario. Net power and gross fuel demand do not change. This is a native inventory/capital saving within the tested assumptions. The 5,000 m² controls show that reducing area further can leave heat unremoved and reduce electricity; they are excluded from design ranking.

## Complete paired accounting

All engineering quantities come from results/cases.json; results/accounting.json retains exact inputs, areas, UA, purchased quantities and capital, every lifecycle contribution, all constraint verdicts and support flags, native margins, and matched-scenario baseline deltas. Annual fuel is kg per calendar year. The feed100 scenario always charges 30 million USD2004/year service; no-credit charges zero. Exhaust recycling is already included before gross new makeup.

| Case | Scenario | Net MW | MWh/year | Gross T kg/year | Feed kg/year | Purchases kg/year | Curtailed kg/year | LCOE USD2004/MWh | Checks |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| baseline | no-credit | 423.106794 | 3150453.189 | 104.667707 | 0 | 104.667707 | 0.000000 | 1119.408083 | passes evaluated checks |
| baseline | feed100-service30m | 423.106794 | 3150453.189 | 104.667707 | 100 | 4.667707 | 0.000000 | 176.686569 | passes evaluated checks |
| he_area-45000.0 | no-credit | 423.106794 | 3150453.189 | 104.667707 | 0 | 104.667707 | 0.000000 | 1119.217127 | passes evaluated checks |
| he_area-45000.0 | feed100-service30m | 423.106794 | 3150453.189 | 104.667707 | 100 | 4.667707 | 0.000000 | 176.495613 | passes evaluated checks |
| he_area-55000.0 | no-credit | 423.106794 | 3150453.189 | 104.667707 | 0 | 104.667707 | 0.000000 | 1119.599040 | passes evaluated checks |
| he_area-55000.0 | feed100-service30m | 423.106794 | 3150453.189 | 104.667707 | 100 | 4.667707 | 0.000000 | 176.877526 | passes evaluated checks |
| he_area-5000.0 | no-credit | 389.195517 | 2897949.817 | 104.667707 | 0 | 104.667707 | 0.000000 | 1215.075689 | heat-removal failure |
| he_area-5000.0 | feed100-service30m | 389.195517 | 2897949.817 | 104.667707 | 100 | 4.667707 | 0.000000 | 190.213221 | heat-removal failure |
| pbli_area-45000.0 | no-credit | 423.106794 | 3150453.189 | 104.667707 | 0 | 104.667707 | 0.000000 | 1119.217127 | passes evaluated checks |
| pbli_area-45000.0 | feed100-service30m | 423.106794 | 3150453.189 | 104.667707 | 100 | 4.667707 | 0.000000 | 176.495613 | passes evaluated checks |
| pbli_area-55000.0 | no-credit | 423.106794 | 3150453.189 | 104.667707 | 0 | 104.667707 | 0.000000 | 1119.599040 | passes evaluated checks |
| pbli_area-55000.0 | feed100-service30m | 423.106794 | 3150453.189 | 104.667707 | 100 | 4.667707 | 0.000000 | 176.877526 | passes evaluated checks |
| pbli_area-5000.0 | no-credit | 399.006806 | 2971004.679 | 104.667707 | 0 | 104.667707 | 0.000000 | 1185.197854 | heat-removal failure |
| pbli_area-5000.0 | feed100-service30m | 399.006806 | 2971004.679 | 104.667707 | 100 | 4.667707 | 0.000000 | 185.536015 | heat-removal failure |
| density-4.75e+20 | no-credit | 277.946691 | 2069591.064 | 94.517422 | 0 | 94.517422 | 0.000000 | 1556.890873 | passes evaluated checks |
| density-4.75e+20 | feed100-service30m | 277.946691 | 2069591.064 | 94.517422 | 100 | 0.000000 | 5.482578 | 201.298114 | passes evaluated checks |
| density-5.25e+20 | no-credit | 575.711005 | 4286744.141 | 115.338520 | 0 | 115.338520 | 0.000000 | 897.365025 | passes evaluated checks |
| density-5.25e+20 | feed100-service30m | 575.711005 | 4286744.141 | 115.338520 | 100 | 15.338520 | 0.000000 | 204.531513 | passes evaluated checks |
| nominal-source-assumed | no-credit | 796.005288 | 5927055.374 | 138.730402 | 0 | 138.730402 | 0.000000 | 767.420931 | heat-removal failure |
| nominal-source-assumed | feed100-service30m | 796.005288 | 5927055.374 | 138.730402 | 100 | 38.730402 | 0.000000 | 266.328936 | heat-removal failure |
| literal-Lyon-source-input | no-credit | 807.016660 | 6009046.048 | 138.730402 | 0 | 138.730402 | 0.000000 | 756.949825 | heat-removal failure |
| literal-Lyon-source-input | feed100-service30m | 807.016660 | 6009046.048 | 138.730402 | 100 | 38.730402 | 0.000000 | 262.695000 | heat-removal failure |
| literal-Raffray-accounting | no-credit | 805.910865 | 6000812.303 | 134.703333 | 0 | 134.703333 | 0.000000 | 737.855370 | heat-removal failure |
| literal-Raffray-accounting | feed100-service30m | 805.910865 | 6000812.303 | 134.703333 | 100 | 34.703333 | 0.000000 | 242.922376 | heat-removal failure |

## Purchased area comparison

Only the area cases at baseline density enter this equipment comparison. Both 45,000 m² choices pass evaluated checks and have the same provisional installed unit price, so their cost changes coincide. Increasing either area to 55,000 m² increases capital by the same amount without increasing net electricity. The tested local window identifies excess area under this assumed U and thermal boundary; it does not locate a minimum acceptable area. Geometry, pressure drop, MHD and material qualification remain unsupported.

| Design | Overnight million USD2004 | He area m² / UA W/K | PbLi area m² / UA W/K | Unmet heat MW | Δ net MW | Δ no-fuel/no-supply subtotal USD2004/MWh |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| baseline | 4350.208470 | 50000 / 50 | 50000 / 50 | 0.000000 | 0.000000 | 0.000000 |
| he_area-45000.0 | 4341.517941 | 45000 / 45 | 50000 / 50 | 0.000000 | 0.000000 | -0.190957 |
| he_area-55000.0 | 4358.898999 | 55000 / 55 | 50000 / 50 | 0.000000 | 0.000000 | 0.190957 |
| he_area-5000.0 | 4271.993706 | 5000 / 5 | 50000 / 50 | 47.118607 | -33.911277 | 8.822196 |
| pbli_area-45000.0 | 4341.517941 | 50000 / 50 | 45000 / 45 | 0.000000 | 0.000000 | -0.190957 |
| pbli_area-55000.0 | 4358.898999 | 50000 / 50 | 55000 / 55 | 0.000000 | 0.000000 | 0.190957 |
| pbli_area-5000.0 | 4271.993706 | 50000 / 50 | 5000 / 5 | 33.486142 | -24.099988 | 5.588305 |

The displayed subtotal is presentation arithmetic summing native contributions except tritium, deuterium and supply service. It is not a second native LCOE output. Baseline deltas match the same fuel scenario.

## Operating diagnostic and fuel threshold

Density changes keep the entire selected hardware inventory fixed. The low-density case reduces net power to 277.946691 MW and gross makeup to 94.517422 kg/year. Feed100 then supplies all new makeup and curtails 5.482578 kg/year, yet LCOE rises to 201.298114 USD2004/MWh because reduced electricity outweighs the purchased-fuel saving. High density raises net power to 575.711005 MW and gross makeup to 115.338520 kg/year. Its no-credit LCOE falls to 897.365025, while feed100 LCOE rises to 204.531513 because purchases rise to 15.338520 kg/year. Neither result establishes confinement, controllability or a qualified operating optimum.

The fixed feed assumption changes the ordering of the three density points: high density is best without credit, while the baseline is best under feed100/service30m. The scenario difference in results/accounting.json compares identical physical inputs and retains the service charge. It cannot be attributed to improved breeding, and it must not be combined with the purchased-area ranking.

## Native contribution accounting

| Contribution USD2004/MWh | Baseline no-credit | Baseline feed100/service30m |
| --- | ---: | ---: |
| capital_lcoe | 93.155987937 | 93.155987937 |
| om_lcoe | 22.219025582 | 22.219025582 |
| tritium_lcoe | 996.691911412 | 44.447957897 |
| deuterium_lcoe | 0.022061004 | 0.022061004 |
| consumables_lcoe | 1.587073256 | 1.587073256 |
| imports_lcoe | 0.000000000 | 0.000000000 |
| supply_lcoe | 0.000000000 | 9.522439535 |
| replacement_lcoe | 3.301126391 | 3.301126391 |
| other_overhaul_lcoe | 1.516445832 | 1.516445832 |
| terminal_lcoe | 1.143064971 | 1.143064971 |
| salvage_lcoe | -0.228612994 | -0.228612994 |
| lcoe_sum | 1119.408083391 | 176.686569410 |

All 11 contributions plus total are retained for every point in results/accounting.json and displayed in plots/contributions-*.png and .pdf. Constant USD2004, the retained real discount/calendar convention, one construction financing adjustment, explicit dated replacements, separate overhaul, gross terminal cost and negative salvage all remain unchanged. The annual replacement reserve is excluded from LCOE.

## Preserved adverse controls and scientific limits

Source controls are excluded from design ranking. Their paired finite LCOEs do not erase native heat-removal failures. The source cases retain respectively 158.725848, 398.908524 and 502.134202 MW unmet heat. Numerical agreement with published source LCOE is not claimed; the predecessor source-boundary record remains the authority for unmatched financial/case scope.

| Adverse design | Unmet heat MW | Failed qualified predicate |
| --- | ---: | --- |
| he_area-5000.0 | 47.118607 | aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07=violated |
| pbli_area-5000.0 | 33.486142 | aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07=violated |
| nominal-source-assumed | 158.725848 | aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07=violated |
| literal-Lyon-source-input | 398.908524 | aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07=violated |
| literal-Raffray-accounting | 502.134202 | aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535=violated; aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07=violated |

All native whole-plant scientific flags remain zero for magnet, deposition, hydraulics, machine maps, breeding and materials; native breeder/supply qualification flags remain zero as well. Capacity-screen support is a different field and does not qualify these scientific assumptions. All exact support flags remain in the accounting artifact.

## Figures and verification

plots/axis-*.png and .pdf show the studied settings, native LCOE, electricity and external purchases, including the unchanged baseline. Crosses mark evaluated failures; open marks explicitly retain missing scientific qualification. plots/power-fuel-capital.* separates native electricity, fuel and purchased capital. Contribution figures retain every declared case and label failed controls; margin figures preserve each native output separately rather than combining different units. Full units and bounds are in axis-plan.json and native package interfaces.

All-point verification passed using the independent oracle and rederived predicates; results/verification_summary.json records channels, tolerances and limitations. The stock runner supplies all engineering values. Report generation reads stored JSON only and makes no native evaluations. Reproduction uses design_protocol.md, the committed support/executor sources and the coordinator’s retained execution context; immutable replay must target a fresh directory.
