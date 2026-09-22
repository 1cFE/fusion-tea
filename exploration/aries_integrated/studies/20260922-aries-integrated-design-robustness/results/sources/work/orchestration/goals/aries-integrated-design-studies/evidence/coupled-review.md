# Independent coupled execution and robustness review

[AGENT independent continuing reviewer, 2026-09-22] **PASS for the executed coupled evidence, proposed interpretation and exact 174-case robustness allocation below.** Final report, plots, record and freeze checks remain coordinator-owned. The report was not yet present at this review. This is not certification of unexecuted robustness outcomes or whole-plant qualification.

## Executed evidence

[Probe](coupled-review-probe.py) and [receipt](coupled-review-probe.json) check all 68 proposed maps against the immutable SQLite store, original evidence digests, full exported outputs and native responses. Store transitions show 68 starts and 68 commits, all attempt 1. Every pair differs in exactly the two fixed supply entries. Original package and store remain unchanged. The unchanged executable and semantic identities are recorded in the receipt and match prior reviews.

Eight independent isolated native replays cover baseline and 45,000/45,000 m² at densities 5e20, 4.875e20 and 5.25e20, each in both supply scenarios. Every replay exactly matches all 546 outputs, 14 constraint responses and headline. Invocation uses the local-review command with `coupled-review-probe.py`. All-case checks independently verify purchase/UA equations, gross makeup, fixed feed/service, purchases/curtailment, annual energy, unsupported flags and eleven-term contribution closure. The producer's all-point verification reports PASS. Prior reviewed mathematics is reused; this review does not independently rederive the thermal root solver.

## Interpretation and MR-7

**MR-7 passes for this tested scope.** Additional all-grid checks in [robustness review evidence](coupled-review-robustness.json) confirm purchased outputs are invariant to density at matched area, while net power and gross makeup are invariant to area at matched density. Both reduced areas save 17.381059 million USD2004 overnight capital and 0.381913 USD2004/MWh at baseline density, with unchanged power/fuel. This is a provisional inventory saving; no minimum adequate area is located.

The reduced-area 4.875e20 case produces 349.596229 MW and requires 99.527499 kg/year gross makeup. Feed100 purchases become zero, with LCOE 159.581252 USD2004/MWh; no-credit LCOE worsens to 1295.085963. Accept the supply-threshold interpretation, not a physical-efficiency or breeding improvement. At 5.25e20, reduced-area results are 575.711005 MW and 897.084346/204.250834 USD2004/MWh for no-credit/feed100. Density remains an unqualified fixed-hardware operating diagnostic.

All ten adverse cases survive: six paired source controls and four undersized-area controls. The latter retain extrapolation flags and are excluded from ranking. Scientific flags remain unsupported. The earlier local report now labels UA as MW/K and accounting uses `ua_mw_k`; this confirms the presentation correction without changing native quantities.

## Accepted robustness allocation

The linked JSON is the exact key/default/fanout/level register for the worker. Use four fixed designs: baseline, reduced areas at baseline density, reduced areas at 4.875e20, and reduced areas at 5.25e20. Pair both fixed supply scenarios for every setting. Ten OAT groups, each with two levels plus one shared baseline, give `21 × 4 × 2 + 6 = 174` native cases.

Accepted sensitivity levels: separate He/PbLi U 500/1500; neutron multiplier 1/1.25; helium deposition fraction .30/.46; exchange .02/.06; other electrical load 2.5/7.5 MW; correlated He/PbLi HX price factors .5/1.5; availability .75/.95; tritium price 10/100 million USD2004/kg; real discount .03/.08. Existing keys/defaults and consumers were checked. The other-load group changes only `generator_auxiliaries.other_electric`, whose default is 5 MW. Tritium price affects initial stock capital as well as annual purchases. Correlated HX prices are an explicit cost scenario, not an identity between physical inputs.

Before indicators/preflight, declare the record-local correlated uncertainty tie containing exactly `aries_integrated_plant__he_hx__price_factor` and `aries_integrated_plant__pbli_hx__price_factor`. Both values are .5 in the low-price scenario and 1.5 in the high-price scenario. This explicit study tie joins independently owned inputs; it neither changes the package nor declares physical hardware identity. Execution acceptance depends on that declaration matching the proposed maps.

These settings match the reviewed WI-090 assumption/thermal register and WI-091 finance register. They can expose conditional ranking reversals; they provide no probability, joint-uncertainty coverage or qualification. Held cryogenic/control loads, machine maps, geometry/hydraulics, confinement and material limits remain missing-response findings. Preserve every refusal and adverse outcome.

Accept the process finding that skeleton deposition followed native launch. Pre-existing framing/maps/gates do not establish an earlier record timestamp. Deposit future skeletons before dispatch; this timing deviation establishes neither numerical invalidity nor retrospective authorization.
