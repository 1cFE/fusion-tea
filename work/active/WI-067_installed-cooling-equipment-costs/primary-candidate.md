# Primary equipment candidate for independent review

[AGENT] This is a conceptual construction and price scenario, not an equipment selection. It carries the acquired methods into quantities that can be reviewed before production implementation. The current primary helium conditions and hydraulic equations remain unchanged. Secondary-loop technology is an owner-held choice now requested separately; no HITEC plant architecture has been adopted through this document.

## Construction and thermal requirement

Use two active, equally loaded parallel circulators and one reference-capacity exchanger per circuit. Keep source OB tube outside diameter19.05mm,7426tubes per pass, two passes and11.6m active length. Its installed outside area is10310.691m². Report the separately calculated required area and its ratio to installed area; do not reduce installed steel when demand falls. Fixed source geometry therefore adds equipment in modules as circuit count changes. Current pumping demand continues to respond to heat load and count.

The source does not give the pressure-boundary manufacturing drawings. The following explicitly assumed construction supplies a reproducible mass scenario. It cannot establish mechanical-code compliance. Retain that limitation in every result, alongside existing flow, thermal and full-plant checks.

| Quantity | Candidate assumption | Sensitivity or evidence limit |
|---|---:|---|
| Exchanger material | Stainless steel, nominal8000kg/m³ | ANL304-to-target-stainless finished-fabrication analogy; exact alloy/service suitability unqualified |
| Tube wall |1.5mm|1.0/1.5/2.0mm cost sensitivity; no pressure-rating certification |
| Shell inside diameter |3.2m|Triangular tube pitch1.25OD requires about3.05m bundle bore for14852tube sections; clearance is assumed |
| Shell cylindrical length |13.0m|11.6m active length plus assumed end space |
| Shell wall |0.20m|0.10/0.20/0.30m cost sensitivity; shell operating pressure undecided, not silently equal to tube pressure |
| Heads |Two hemispheres at shell radii|Simple costing geometry, not the source NFN manufacturing drawing |
| Tubesheets |Two3.2m discs,0.60m thick|Gross unperforated mass is a conservative quantity convention; mechanical adequacy remains unassessed |
| Nozzles, baffles and internal supports |10tonnes per unit|Explicit unresolved-detail mass allowance;5/10/20tonnes sensitivity, not sourced layout |
| Primary main-pipe outside diameters |1.3m hot and1.1m cold|Approximations motivated by source DN labels; DN is not established OD |
| Main-pipe wall |65mm both legs|Source reports up to65mm hot leg; use on both legs is an assumption |
| Main-leg lengths |50m hot and50m cold per circuit|20/50/100m each; layout cost sensitivity only |
| Main-pipe fittings |14440/66560 times straight mass|ANL reference-layout transfer; does not price branch networks or valves |

Tube metal is `rho*pi/4*(Do²-(Do-2t)²)*(2*Npass*L)`. Shell metal uses the same cylindrical difference over shell length. Two hemispherical heads together have metal volume `4*pi/3*((ri+t)³-ri³)`. Gross tubesheet mass is `2*rho*pi/4*Di²*t_sheet`. These quantities are independent of a price allowance. Report tubes, shell, heads, sheets and the explicit accessory allowance separately so its contribution cannot be concealed.

This construction is intentionally only a mass scenario. A pressure calculation may report ideal cylindrical hoop stress, but must not label that a pressure qualification: allowable stress at temperature, weld factors, creep, tubesheet support, fatigue, corrosion and code class are not established. No new claimed safe operating limit is created.

The main-pipe estimate remains visibly incomplete pending a branch/manifold/valve/support schedule. This candidate does not conceal those items in its fitting ratio. Changing an assumed pipe length here is a price sensitivity at retained hydraulic requirements; it is not a prediction of a redesigned layout's pumping power.

## Purchased, fabricated and installed scope

Circulator sizing consumes mass flow, inlet volume, pressure rise, suction conditions and electrical/fluid power. Preserve two alternative price methods during review: Seider's motor-inclusive stainless centrifugal purchase analogue at CE500, and BNL's December1978 helium machine/motor reference with its pressure/material-half formula. The BNL formula acts on550000USD and nominal50hp pumping duty; it does not use the140hp motor nameplate as that duty denominator. Treat target extrapolation as uncalibrated, not a confidence interval or lower bound.

[AGENT] For an explicitly illustrative complete BNL electrical package, hold the source power-supply/machine ratio110000/550000 across size. The source does not provide that scaling law. Preserve the power-supply line separately and test it; do not call it source-derived scaling. Charge source130000USD first-design engineering once per identical machine design, with no repeated-unit production discount. Existing plant engineering remains project-level work, not this manufacturer's detailed machine design.

[AGENT] ORNL provides a possible package-installation analogy:0.27 times hardware, where its hardware is vendor procurement plus15.5% procurement services. Preserve both the denominator and service scope. Assign this component allowance to circulator setting/local connections only if independent review accepts that imposed boundary. It does not price the separately estimated main pipes, exchanger installation or buildings. Generic project engineering and contingency remain in existing CAS30/CAS29; do not add ORNL's separate35%engineering and27.5%contingency again. Procurement services need an explicit owner before integration rather than being silently dropped.

For the stainless exchanger use ANL `factory_delivered = 310 USD2017/kg * total_dry_mass`; this includes fabrication. Separately show site labor0.024 and site material0.002 times factory cost using ANL's actual IHX installation method. Do not add the alternative fixed PWR installation allowance or NETL exchanger setting again. The transfer from sodium/steam service to the declared helium exchanger remains a conceptual construction analogy, with material and pressure differences carried by the bill and its limitations.

For main pipes and fittings use ANL's delivered310USD2017/kg. NETL labor0.50 times piping material cost is a possible explicitly transferred field-labor scenario; applying it to ANL finished nuclear fabrication is uncalibrated. Do not simultaneously add NETL's0.40equipment-based pipe material or0.20pipe labor allowances. Pipe supports, insulation, valves and branches remain separate missing quantities in this candidate.

Use the registered annual CPI only to compare source amounts in completed2025 purchasing-power equivalents; preserve source-year amounts. This general index is not nuclear-equipment price escalation and does not normalize the inherited whole plant. Source CE500 is treated as its stated2006 basis; the BNL December1978 quote uses an explicitly chosen1978 annual-index convention. Retain an un-escalated source-price report.

## Lifecycle and account decisions still needed

Initial spares should be counted as physical equipment rather than an unexplained percentage. A candidate is one complete uninstalled spare circulator package per plant, with no duplicate first-design fee; source evidence does not establish that redundancy policy. Whole-circulator replacement at10/20/30calendar-year intervals is an explicit lifecycle sensitivity, not sourced reliability. Tube-bundle replacement should price actual replaceable metal; whole-vessel60-year design targets must not be used to claim60-year internals. Replacement removal/handling and consumable maintenance still need an explicit estimate or an unpriced flag. No extra pumping-electricity cost is added outside the energy balance.

Do not switch the plant's cost selector yet. Replacing C220201 requires a complete enough primary bill and disjoint package/service ownership. C220202's inherited aggregate does not establish how much exchanger or secondary scope it includes. Its remaining value cannot be relabeled as a proven disjoint allowance. Resolve the intermediate technology and scope before either retaining or replacing it alongside the new exchanger cost. The owner question is recorded in the goal trail.

Native interfaces are already traced: keep one `heat_transport.coolant_cost` consumer in CAS22; introduce a cooling replacement producer and route its sum with calendar replacements into CAS70; exclude delivered-equipment scope from CAS50 shipping exactly once. Generic designs retain disabled defaults. The native implementation plan follows a reviewed full ledger, not this conditional partial candidate.
