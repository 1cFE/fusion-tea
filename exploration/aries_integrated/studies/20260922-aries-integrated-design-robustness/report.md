# Robustness of conditional area and demand comparisons

[AGENT executor interpretation] All 174 declared native cases completed once. Independent all-point checking passes 364 numerical channels and 14 rederived predicates per point. The 168 design/uncertainty cases pass evaluated checks; all six inherited source controls retain heat-removal failures. Scientific qualification is absent throughout.

Reducing both purchased exchanger areas to 45,000 m² remains a small saving in every tested uncertainty setting and both fixed fuel scenarios. The near-feed-floor operating diagnostic is less stable: its apparent feed100 advantage reverses under lower neutron multiplication, lower availability and lower tritium price. These are conditional results from twenty one-at-a-time settings plus default, not joint-uncertainty robustness or a physical optimum.

## Cases, matching and quantities

Four fixed physical designs are the assumed integrated baseline (50k/50k m², density 5e20 m⁻³), area45k at the same density, near-feed-floor at 45k/45k and 4.875e20, and high-density-demand at 45k/45k and 5.25e20. Three physical descriptor groups and ten uncertainty groups give thirteen declared groups; the correlated HX price group has two explicitly tied independent keys. No automatic resizing occurs.

Every design receives the same 21 assumption settings and the same two fixed supply scenarios. No-credit supplies zero new feed and zero service. Feed100 supplies 100 kg/calendar-year and charges 30 million USD2004/year service, even when feed is curtailed. Exhaust recycling is already credited before gross new makeup. The six source controls retain inherited assumptions and are excluded from ranking.

results/all-case-accounting.csv is the compact full 174-row account: physical/uncertainty/supply labels, net MW and MWh/year, gross/feed/purchases/curtailment, annual service, all eleven native LCOE contributions and total, installed area/UA in MW/K/quantity/capital, unmet heat and qualification. results/accounting.json retains every native margin and predicate. results/matched-comparisons.json compares each candidate to the baseline at the SAME uncertainty setting and supply scenario. Generic default-baseline deltas are not used for robustness conclusions.

All 126 intended comparisons pass evaluated checks on both sides. The reporting guard would mark either-side failures unrankable while retaining their numerical differences. This evaluated status never establishes scientific feasibility.

## Matched conditional LCOE differences

Values are candidate minus matched baseline in USD2004/MWh; negative means lower conditional cost. The default row is the only comparison against original default assumptions. Each other row uses its own changed baseline. The two supply scenarios remain separate.

| Uncertainty setting | Area45k no-credit | Near-floor no-credit | High-demand no-credit | Area45k feed100 | Near-floor feed100 | High-demand feed100 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| default | -0.381913 | +175.677879 | -222.323737 | -0.381913 | -17.105317 | +27.564264 |
| he_u=500 | -0.381913 | +175.677879 | -222.323737 | -0.381913 | -17.105317 | +27.564264 |
| he_u=1500 | -0.381913 | +175.677879 | -222.323737 | -0.381913 | -17.105317 | +27.564264 |
| pbli_u=500 | -0.381913 | +175.677879 | -222.323737 | -0.381913 | -17.105317 | +27.564264 |
| pbli_u=1500 | -0.381913 | +175.677879 | -222.323737 | -0.381913 | -17.105317 | +27.564264 |
| neutron_multiplier=1 | -0.636126 | +532.796121 | -537.862295 | -0.636126 | +1.104192 | +7.762890 |
| neutron_multiplier=1.25 | -0.311819 | +115.010180 | -155.093309 | -0.311819 | -17.468453 | +28.522177 |
| helium_fraction=0.3 | -0.381913 | +175.677879 | -222.323737 | -0.381913 | -17.105317 | +27.564264 |
| helium_fraction=0.46 | -0.381913 | +175.677879 | -222.323737 | -0.381913 | -17.105317 | +27.564264 |
| exchange_fraction=0.02 | -0.381913 | +175.677879 | -222.323737 | -0.381913 | -17.105317 | +27.564264 |
| exchange_fraction=0.06 | -0.381913 | +175.677879 | -222.323737 | -0.381913 | -17.105317 | +27.564264 |
| other_load=2.5 | -0.379670 | +173.057705 | -219.627078 | -0.379670 | -17.200546 | +27.719000 |
| other_load=7.5 | -0.384183 | +178.352352 | -225.064728 | -0.384183 | -17.006103 | +27.404895 |
| hx_price_factor=0.5 | -0.190957 | +175.507459 | -221.677227 | -0.190957 | -17.275737 | +28.210774 |
| hx_price_factor=1.5 | -0.572870 | +175.848300 | -222.970247 | -0.572870 | -16.934897 | +26.917755 |
| availability=0.75 | -0.432835 | +179.085015 | -226.733902 | -0.432835 | +30.866652 | -25.331576 |
| availability=0.95 | -0.341712 | +172.987603 | -218.841482 | -0.341712 | -4.374880 | +4.742519 |
| tritium_price=10000000.0 | -0.381913 | +74.075994 | -94.243911 | -0.381913 | +11.149802 | -12.630657 |
| tritium_price=100000000.0 | -0.381913 | +531.284477 | -670.603130 | -0.381913 | -115.998234 | +168.246491 |
| discount=0.03 | -0.273272 | +170.108983 | -215.057964 | -0.273272 | -22.674213 | +34.830037 |
| discount=0.08 | -0.589481 | +186.315825 | -236.203212 | -0.589481 | -6.467371 | +13.684789 |

## Equipment savings and missing physical response

Area45k saves 0.190957–0.636126 USD2004/MWh against its matched baseline across these OAT settings. At default it saves 17.381059 million USD2004 overnight and 0.381913 USD2004/MWh. At matched assumptions, native net electricity and gross fuel makeup stay unchanged; the saving comes through selected purchased quantity, financing and capital-proportional overhaul/terminal/salvage allowances. Each reduction remains within the tested assumption window; no minimum adequate area is found.

Changing U from 1000 to 500 or 1500 W/(m² K) changes native UA, but all tested selected areas still remove the modeled heat. Thus these U endpoints do not reverse the rankings or locate the heat-removal boundary. Deposition partitions change internal heat routing without changing the modeled total conversion result in this adequate-area window. These bounded observations do not qualify geometry, pumping pressure drop, MHD, materials or neutron transport.

The HX price factors are a common uncertainty multiplier on two independently owned purchase inputs, not a physical hardware identity. Both price factor and discount have no modeled constraint response. Before execution, record §8 quoted the owner’s authorization for sensitivity-only assumptions and retained separate missing price/quality and financing/credit-response findings. Neither endpoint is promoted as an optimized choice.

## Why the operating ordering reverses

Without breeding credit, near-feed-floor is more expensive than matched baseline in all 21 settings; high-density-demand is cheaper in all 21. These are fixed-hardware imposed-demand diagnostics. Confinement and controllability are unqualified, so the lower price does not select a realizable operating point.

With feed100, near-feed-floor is cheaper at default, but becomes more expensive at neutron multiplier 1, availability 0.75, and tritium price 10 million USD2004/kg. High-density-demand becomes cheaper at availability 0.75 and tritium price 10 million; it is more expensive in the other 19 settings. The following native quantities explain the reversals.

| Setting / physical design, feed100 | Net MW | MWh/year | Gross T kg/year | Purchases kg/year | LCOE USD2004/MWh |
| --- | ---: | ---: | ---: | ---: | ---: |
| default / baseline | 423.106794 | 3150453.189 | 104.667707 | 4.667707 | 176.686569 |
| default / near-feed-floor | 349.596229 | 2603093.523 | 99.527499 | 0.000000 | 159.581252 |
| default / high-density-demand | 575.711005 | 4286744.141 | 115.338520 | 15.338520 | 204.250834 |
| neutron_multiplier=1 / baseline | 254.022006 | 1891447.853 | 104.667707 | 4.667707 | 294.294535 |
| neutron_multiplier=1 / near-feed-floor | 188.860002 | 1406251.576 | 99.527499 | 0.000000 | 295.398726 |
| neutron_multiplier=1 / high-density-demand | 389.295025 | 2898690.758 | 115.338520 | 15.338520 | 302.057425 |
| availability=0.75 / baseline | 423.106794 | 2779811.637 | 92.420003 | 0.000000 | 149.290942 |
| availability=0.75 / near-feed-floor | 349.596229 | 2296847.226 | 87.884525 | 0.000000 | 180.157594 |
| availability=0.75 / high-density-demand | 575.711005 | 3782421.301 | 101.835425 | 1.835425 | 123.959366 |
| availability=0.95 / baseline | 423.106794 | 3521094.741 | 116.915411 | 16.915411 | 262.894802 |
| availability=0.95 / near-feed-floor | 349.596229 | 2909339.820 | 111.170473 | 11.170473 | 258.519923 |
| availability=0.95 / high-density-demand | 575.711005 | 4791066.981 | 128.841614 | 28.841614 | 267.637322 |
| tritium_price=10000000.0 / baseline | 423.106794 | 3150453.189 | 104.667707 | 4.667707 | 140.506660 |
| tritium_price=10000000.0 / near-feed-floor | 349.596229 | 2603093.523 | 99.527499 | 0.000000 | 151.656462 |
| tritium_price=10000000.0 / high-density-demand | 575.711005 | 4286744.141 | 115.338520 | 15.338520 | 127.876003 |
| tritium_price=100000000.0 / baseline | 423.106794 | 3150453.189 | 104.667707 | 4.667707 | 303.316251 |
| tritium_price=100000000.0 / near-feed-floor | 349.596229 | 2603093.523 | 99.527499 | 0.000000 | 187.318018 |
| tritium_price=100000000.0 / high-density-demand | 575.711005 | 4286744.141 | 115.338520 | 15.338520 | 471.562743 |

At availability 0.75 the baseline and near-floor designs both require less than the fixed 100 kg/year supply, removing the near-floor purchase advantage; the lower electricity then makes near-floor more expensive. At 0.95 both require supplemental purchases, and near-floor remains slightly cheaper. Availability does not multiply the independently supplied feed or service charge.

Reducing neutron multiplication to 1 lowers native thermal/electrical output without changing gross makeup at the same density. The near-floor design still avoids purchases, but its reduced denominator outweighs that advantage. At the lower tritium price, purchases matter less and the high-demand design’s larger denominator becomes cheaper.

Tritium price changes initial stock purchase capital as well as annual external purchases. At 10 million USD2004/kg baseline overnight capital is 4.052208470 billion USD2004; at 100 million it is 5.393208470 billion. A fuel-price interpretation that holds initial stock capital fixed would misstate the native graph. The default remains 30 million per kg.

Other-load sensitivity changes only the 5 MW generator auxiliary allowance to 2.5 or 7.5 MW. Cryogenic and control assumptions remain held. This narrow test does not establish robustness to all parasitic loads. The nonfuel/nonsupply subtotal in the JSON is presentation arithmetic excluding tritium, deuterium and supply service; exact contribution differences remain available for every comparison.

## Source controls and unsupported checks

| Source control, both supply scenarios | Unmet heat MW | Failed qualified predicates |
| --- | ---: | --- |
| nominal-source-assumed | 158.725848 | aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07=violated |
| literal-Lyon-source-input | 398.908524 | aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07=violated |
| literal-Raffray-accounting | 502.134202 | aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535=violated; aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07=violated |

Source controls retain finite conditional LCOE and their actual failures. No published-source numerical agreement is asserted; earlier source-boundary and unmatched-comparison evidence remains applicable. Plant scientific flags for magnets, deposition, hydraulics, machine maps, breeding and materials remain unsupported. New-feed/extraction support remains unsupported; passing a numerical capacity screen is a different claim.

## Verification and replay

The 174 unique maps completed once through the stock native lifecycle, with 174 starts and 174 commits. All-point independent verification passes 63,336 scalar comparisons and 2,436 rederived predicate comparisons under reviewed relative/channel-specific absolute tolerances. No model, runtime, live manifest, prior frozen study or physical oracle was changed. All production quantities came from native generated outputs.

plots/matched-uncertainty-differences.png and .pdf show matched conditional differences; plots/default-design-accounting.* show major native contributions, electricity and fuel at the four default designs; plots/preserved-failed-controls.* visibly retain all six adverse cases and unmet heat. Every figure states the missing scientific qualification. The full CSV/JSON retain all outputs needed to inspect any other setting.

The skeleton preceded dispatch and populated framing/rulings preceded coordinator GO and native launch. Exact execution commit and commands are in results/execution-context.json and replay.md. Reused baseline identity and fresh preflight are retained in preparation/ and results/integration/. Frozen snapshot/archive/commit are coordinator-owned.

These engineered one-at-a-time scenarios have no assigned probabilities and do not cover simultaneous uncertainty, unknown machine maps, price calibration or scientific qualification. Equipment savings persist in the tested settings; the fuel-floor operating benefit does not. No global optimum or fully feasible reactor is claimed.
