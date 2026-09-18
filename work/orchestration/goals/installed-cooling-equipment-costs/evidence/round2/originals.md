# T-003 alternate original retrieval

[AGENT] Twenty individually prelogged searches reached the prospective search cap. Two alternate original reports were acquired and passed full-document term screening before inspection. They establish cost-method and lifecycle boundaries, but neither supplies a calibrated helium circulator price or fabricated 316L pipe unit rate. The exact GA911105/911120, Dominion M-6914-00-04 and Stewart2021 originals remain unacquired. No model changes or domain insights were made.

## Native evidence and acquisition

Request: `knowledge/research/requests/REQ-COOL-R2-ORIGINALS.json`. Run: `knowledge/research/requests/runs/REQ-COOL-R2-ORIGINALS/20260918T215650907336/`. Limits were declared before searching:20 searches,6 captures,35 tool calls. Coordinator subsequently authorized8 completion/lifecycle calls and then administrative completion without another call gate; searches and capture caps remained unchanged. Queries are individually recorded in the native run. Exact-title/report-number alternatives searched author/institution repositories, open supporting-code leads and public archive indexes. No broken Round1 download URL was retried. No author was contacted. Public-archive searching did not retrieve an archive snapshot; no snapshot was acquired.

| Original | Retrieval and identity | Registration |
|---|---|---|
| MIT-ANP-TR194, Capital Cost Evaluation of Advanced Water-Cooled Reactor Designs with Consideration of Uncertainty and Risk,2022 | Public mirror `https://47278698.fs1.hubspotusercontent-na2.net/hubfs/47278698/194-ANP-TR%20MIT%20CANES.pdf`;167pages; SHA256 `59f2305b0322a6969a2108335ee178459cbc729d46b6784b5323c0e7027c3c6b` | `knowledge/sources/mit_canes_capital_cost_evaluation_of_advanced_water_cooled/` |
| INL/EXT-07-12967 Rev1, NGNP Pre-Conceptual Design Report, November2007 | Institutional original `https://inldigitallibrary.inl.gov/sites/sti/sti/3867694.pdf`;637pages; SHA256 `6745eb812feaca31c967cf0047bce964135fdac2cc712a01a77a81ecbd9d7734` | `knowledge/sources/inl_ngnp_pre_conceptual_design_report_revision1_2007/`. Contains original GA PC-000544/0 executive report and INL heat-transport whitepaper. |

An ORNL original, `https://info.ornl.gov/sites/publications/files/Pub12288.pdf`, ORNL/TM-2008/129,111pages, also passed full-document term screening. Targeted reading showed a materials-development plan rather than useful equipment prices; rejected without registration. The MIT author page failed both web-open and direct retrieval. Search-result snippets were triage only. All substantive claims below come from retrieved original PDF bytes. Screens used case-insensitive ARIES-CS spelling variants, barred host and sealed paper stems; this is term screening with source-context judgment, not a guarantee against unnamed derivative content. The reports concern fission reactor designs and no barred design data were encountered.

## Usable cost method and applicability

[INHERITED: MIT-ANP-TR194, printed36–37, PDF37–38, equations2.1–2.2 and Table2.6; both pages image-checked] The report gives `C=A*(B+D*P^n)` and `C=C_EEDB*(P_new/P_EEDB)^n`. In the first expression A is fitted against the EEDB water-reactor reference. The report explicitly says it mixes nuclear quality-assurance effects with extrapolation error. Its primary coolant pump is especially far outside the handbook domain. This is a concrete conceptual estimating method, but the water-reactor coefficient is not a helium installation factor.

| Component | B | D | n | Parameter P | Handbook range | EEDB reference | A |
|---|---:|---:|---:|---|---|---:|---:|
| Primary coolant pump |9054|247|0.92|Table literally labels it “power (liters/s)”|0.2–126|5968|39.7|
| Steam generator |316888|61|1.2|surface area,m²|10–1000|5126|17|

[INHERITED: same source] Values are inflated to2018 cost basis from the2010 handbook basis. The pump label is dimensionally inconsistent in the original; liters/s is flow, not power. The table is transcribed without silently correcting it. The report cautions that its estimates are best compared relatively across its reactor architectures. These factors do not establish pressure, temperature, helium, materials, installed piping or equipment replacement applicability for the retained circuit. Applying the steam-generator formula to a helium IHX would additionally require an appropriate exchanger design/area and a justified manufacturing/material conversion. Applying the pump formula to the helium circulator would change equipment class and fluid and is unsupported.

[INHERITED: INL/EXT-07-12967, GA PC-000544 printed113, PDF591, Table5-1 image-checked] NGNP costs distinguish capitalized direct costs, field indirect costs, field management, owner costs, supplementary spares/equipment, contingency and financing. The table reports2007 dollars in thousands. It is a whole-project cost table; no isolated helium circulator or pipe procurement/installation unit price appears in it. Thus its ratios cannot supply an equipment installation multiplier. Its accompanying operating-cost section, PDF592, treats O&M, fuel and decommissioning separately.

[AGENT] Full-document text searches and targeted appendix inspection found no316L occurrence or transferable fabricated high-pressure pipe unit rate. This is a bounded inspection result, not proof that the engineering market lacks such a rate. The acquired source does not remove the separately priced piping gap.

## Lifecycle and engineering scope

[INHERITED: NGNP PDF544, GA printed66, original page image-checked] The IHX vessel has a60-year design target; internals may need replacement. The original sentence ends incompletely after “replaced in” and supplies no interval. The page describes a6MPa primary/secondary helium PCHE concept with primary950°C inlet and590°C outlet, secondary565–925°C, internally insulated piping and unresolved fabrication, inspection and maintenance issues. A60-year vessel target is not a60-year whole-exchanger life certification and does not establish the retained8MPa300–500°C equipment lifetime.

[INHERITED: NGNP PDF549, GA printed71] The primary helium circulator includes motor, axial impeller/diffuser, loop shutoff valve, motor controls/power, magnetic-bearing controls/power, labyrinth seal, internal cooler and barrier/sleeve. The design is part of the primary pressure boundary. PDF551 says the secondary circulator is similar but lacks the primary loop shutoff valve. These are concrete equipment-scope items that a generic compressor cost may omit. No motor/bearing replacement interval or maintenance price was found.

[INHERITED: NGNP PDF609, GA printed131] The planned post-test maintenance demonstration includes replacement of the turbine-machine rotor, IHX heat-transfer element and other equipment not designed for plant life. This supports keeping replaceable internals separate from long-lived vessels. It supplies neither a periodic replacement schedule nor a priced service contract.

[AGENT] An explicit scenario may distinguish vessel life, replaceable exchanger internals and circulator motor/bearing service. Any selected service interval or cost fraction would remain an agent assumption until separately supported; this source does not justify an annual percentage. Design life and qualified achieved life must remain distinct.

## Consequence for the retained circuit

[INHERITED: T-003 brief] Target:8MPa helium300–500°C;18circuits;167.440MW IHX duty per circuit;156.575kg/s and159.303kPa per loop. Two circulators per circuit is an assumed topology.

[AGENT] No source here turns those inputs into a justified installed helium equipment total. The useful additions are an original, inspectable conceptual cost formulation with an explicit nontransferability warning; project-versus-equipment cost separation; and component-level lifecycle boundaries. Generic gas-equipment methods investigated separately may support conditional pricing without recovery of every queued original. These originals do not supply the missing fabricated piping price or priced replacement schedule.

[AGENT] A final component-price check inspected every text page containing circulator together with cost, price, dollar or million terms. GA printed13/PDF491 gives only an approximate$16million difference between complete helium and molten-salt heat-transport systems, attributed mainly to the circulator. This is not an isolated purchased or installed circulator price and cannot serve as a package anchor.

## Closed result

Native return is `REGISTERED`, with two completed full-PDF source registrations, one queued MIT author-page access failure, no bounded negative, and `limit_reached=max_searches`. Exactly20 query strings and2 capture attempts were recorded. The original Round1 source queue remains unchanged. The native extracted files contain the checked method and scope passages; MIT extraction line475 and NGNP extraction lines9210/9819 are useful entry points. Retained inspection images are in `evidence/round2/originals-images/`: `mit194-37.png`, `mit194-38.png`, `ngnp-591.png`, `ngnp-544.png`. The two raw hashes above match the native registration identities. No raw source was replaced by a hand-made extraction or excerpt.
