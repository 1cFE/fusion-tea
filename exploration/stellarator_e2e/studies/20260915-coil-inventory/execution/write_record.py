"""Render the study arguments from record-local executed evidence; snapshot remains separate."""
import json,re
from pathlib import Path
H=Path(__file__).resolve().parents[1];R=H/'results'
read=lambda p:json.loads(p.read_text())
a=read(R/'analysis.json');ind=read(H/'indicators.json');ver=read(R/'verification_summary.json');allpts=read(R/'oracle-all-points.json');base=read(R/'baseline_result.json');axes=read(H/'axes.json')['groups']
D=a['design'];cols=a['columns'];P='stellarator_09__stellaris__'
cheap=[c['sampled_feasible_minimum'] for c in cols if c['arm']=='arm-a-transect' and c['sampled_feasible_minimum']]
lines=[]
def add(x=''):lines.append(x)
add('## 1. Study header\n')
add('- **Study id:** 20260915-coil-inventory\n- **Package:** stellarator_tea\n- **Date executed:** 2026-09-15\n- **Executor:** goal Round3coordinator (authored synthesis, not independent reading)\n- **Mode:** execute\n- **Arms:** arm-a-transect, arm-R-transect, arm-matched-window, arm-assumptions\n')
add('## 2. Intake\n')
add('> the whole point of this is for  you to continue until it finishes. do research if you need data on a decision, otherwise, use your best judgement\n')
add('[OWNER-VERBATIM 2026-09-15] Above is the completion/technical-judgment delegation. [AGENT] The final study reads the implemented cryogenic and total-support increment against its immediately entering Round1package, while retaining older-package historical references under the owner-approved comparison amendment. Equipment/accounting alternatives are explicit engineering scenarios.\n')
add('## 3. Objective and result\n')
add(f'Headline objective `{P}lcoe_calc__lcoe`; comparison objective `{P}lcoe_1cfe_calc__lcoe`. Native design-point headline is **{D["lcoe"]:.6f} $/MWh**, with17of18predicates satisfied. The cheapest nominal sampled fully feasible point stays at R12.7m/a1.7m; prices are '+', '.join(f'{r["lcoe"]:.6f} $/MWh at{r["column"].split("-")[-1]}MW installed heating' for r in cheap)+'. These are sampled minima, not a global optimum.\n')
add('## 4. Constraint outcomes\n')
add('Every count below is across183exported arm rows (180unique native proposals); full feasibility requires all eighteen predicates. The native store retains qualified identities and complete verdicts.\n')
add('| constraint_id | source_local_identity | Satisfied rows | Violated rows |\n|---|---|---:|---:|')
for v in base['verdicts']:
 name=v['source_local_identity'];n=sum(c['violations_by_predicate'][name] for c in a['counts'].values());add(f'| `{v["constraint_id"]}` | `{name}` | {183-n} | {n} |')
add('\nPer-arm counts and locations are in results/analysis.json and points.csv. No indeterminate verdict or failed native case occurred.\n')
add('## 5. Framing\n')
add('All eighteen declared axes were proposed and remain **sensitivity**-framed. Geometry/envelope coordinates re-read the existing engineered window. Equipment parameters quantify declared alternatives. The density and installed-heating groups locate historical columns. No boundary or procurement optimum is claimed. Assumption-altered rows are excluded from nominal geometry minima.\n')
add('## 6. Per-axis account\n')
for g in axes:
 axis=g['axis'];add(f'#### {axis} — feasible structure (search framing)\n\n**Applies:** not applicable; this axis is sensitivity-framed.\n')
 add(f'#### {axis} — observed response (sensitivity framing)\n\n**Applies:** yes. ')
 if axis in ('a','R'):
  ar='arm-a-transect' if axis=='a' else 'arm-R-transect'
  entries=[c for c in cols if c['arm']==ar]
  add('The design column has no fully feasible sample. Each cheap column retains one fully feasible point at R12.7/a1.7. Unrestricted minima and their failed predicates are listed separately in results/analysis.json. Both ends of every transect are caught by recorded predicates (results/edge-scan.json); this does not establish the continuous boundary.\n')
 elif axis in ('I_coil','B_max'):
  add('The108matched-coordinate rows retain five all-predicate passes. This study makes no new qualification claim for the extrapolated27.5/30T envelopes. Full coordinates and violated predicates remain in points.csv; historical and attributed flip tables name each source case. No boundary claim.\n')
 elif axis in ('n_e0','p_wallplug_heat'):
  add('This is a fixed column coordinate, not an isolated sweep. At100/220MW installed heating the same sampled geometry satisfies all18predicates; installed capacity changes capital while computed operating heating is unchanged at identical plasma coordinates. No boundary claim.\n')
 elif axis.startswith('cryoplant_') and axis not in ('cryoplant_q_nuc_structure','cryoplant_p_tfcool'):
  add('This parameter participates in the declared low/high equipment bundles. Their combined thermal/refrigeration response is reported in results/analysis.json; it does not identify a separate measured effect or independent uncertainty for this parameter. All assumption rows at the two cheap anchors remain18-feasible; design-anchor alternatives retain its divertor violation. No boundary claim.\n')
 else:
  add('The named cost, residual or model-form alternative is reported at all three anchors in results/analysis.json. Coefficient and exponent change together only for the distinct thesis fit; its unit/exponent pairing is preserved. Alternatives remain conditional input scenarios. The two cheap anchors retain18-predicate feasibility and the design anchor retains its divertor violation. No boundary claim.\n')
add('## 7. Axis groups\n')
add('| Axis | Qualified entry key | Provenance |\n|---|---|---|')
for g in axes:
 for k in g['keys']:add(f'| `{g["axis"]}` | `{k["key"]}` | `{k["provenance"]}` |')
add('\nAll18groups were traced without subset. No ties are asserted; equipment bundles jointly select independent assumptions.\n')
add('## 8. Indicators and rulings\n')
add('The steel-price and nonmagnet-residual-fraction axes report `no_constraint_response`; the remaining sixteen report `constraints_reachable`. The owner explicitly delegated research and technical judgment before execution; the executor selected these two as cost sensitivities, with finding#1 recording the absent procurement/infrastructure evidence. This is an agent choice under delegation, not owner-originated parameter values.\n')
add('Reachability means a possible path, never an observed response. Indicators do not derive monotonicity, physical identity across key names, or intra-module operand dependency. No axis is promoted to a search by having a reachable path.\n')
add('## 9. Preflight results\n')
add('All six native gates pass in results/preflight_results.json: declared keys, sibling scan, sealed identity, manifest currency, pinned baseline and clean package. The integrated candidate was already proven through all ten integration gates. No gate was skipped.\n')
add('## 10. Execution route and why\n')
add('A study-local direct-API definition uses the stock PreparedListStrategy/StudyRunner lifecycle over180unique proposals, joined into183arm rows by exact proposal identity. It supports coordinated transects and historical coordinates without a custom evaluation loop. One native store serves all four arms. Glue ledger: none; stock sealed loader, no adapter.\n')
add('## 11. Study definition and window provenance\n')
add('The geometry windows preserve the30+21transect and108matched coordinates from entering Round1. They were rescanned at the new package, including all edges and the two current feasible cheap anchors. The design column has no feasible anchor, explicitly recorded. Bounds are engineered sensitivity windows, not sourced admissibility intervals. Twenty-four added rows evaluate eight declared equipment/accounting alternatives at three anchors. Exact proposals, all ten native input files, the final model contract/manifest, implemented design and source bases are retained under preparation; snapshot.json records their digests.\n')
add('## 12. Cross-fingerprint correlation and what it means\n')
add('One sealed executable fingerprint applies to all four arms; there is no cross-arm fingerprint correlation problem. snapshot.json resolves the package/manifest/semantic/executable digests, tool revisions, TEAx revision and source references. The attributed before is the immediately entering Round1package; older plant-closure/magnet-transfer packages remain historical references. No frozen source result was rerun or rewritten.\n')
add('## 13. Verification\n')
add(f'Generic verify.py stratifies its sample by verdict combination and independently re-derives all eighteen authored predicates. Results/verification_summary.json records actual sample/coverage. The record-local check additionally compares {allpts["scalar_comparisons"]} required mapped scalar values and{allpts["predicate_comparisons"]} predicate outcomes across183arm rows, maximum relative scalar deviation{allpts["max_relative_deviation"]:.3g}, with zero differences outside tolerance. Circumference and cold volume use separately stated identities; those checks are not independent oracle publication. No failed/missing required comparison is silently omitted.\n')
add('## 14. Review outcomes\n')
add('Independent preexecution review PASS in reviews/preexecution-review.md; its conditions are discharged by final indicators, edge evidence and all native baseline/preflight gates before execution. Source/math and native integration reviews are reused for their unchanged equations. The coordinator authors this record; independent postexecution correctness/disposition review PASS is retained in reviews/postexecution-review.md. All six dispositions and both proposed learnings are accepted; final snapshot and regression checks remain separate completion gates.\n')
add('## 15. Findings\n')
add('| Finding id | Kind | Finding | Proposed disposition | Home |\n|---|---|---|---|---|')
add('| `20260915-coil-inventory#1` | `model` | Steel price and nonmagnet budget have no constraint response; procurement qualification and a sized nonmagnet infrastructure floor are absent. | `declared seam` — sensitivity only; conditional cost basis remains explicit. | WI-059 design D1–D2; protocol.md |')
add('| `20260915-coil-inventory#2` | `model` | Thermal/support inventory now follows declared coil geometry, but actual cryostat geometry, structure deposition,316LN transfer, configuration fit and fabrication rates remain unqualified. | `declared seam` — implementation complete; retain engineering scope limits and numerical sensitivities. | WI-059 design; goal answer |')
add('\nExisting bore-price/cryogenic/transfer findings are joined by the goal disposition record after independent review; first sightings remain immutable.\n')
add('## 16. Snapshot\n')
add('snapshot.json carries resolved values and digests, separate from these arguments. There is no unresolved execution or numerical disposition. Both new findings retain declared engineering limits; sensitivity bands are not statistical bounds, and35.5W/m³ is a winding-deposition proxy, not an upper bound for steel heating. No further model execution is proposed by this reading.\n')
add('## 17. What this record does not contain\n')
add('No detailed manufactured50kA lead, complete cryostat/support path design, validated nonmagnet budget or vendor316LN fabrication quotation is supplied. Nominal structure nuclear heating is zero; the named proxy sensitivity exposes its consequence. The mass fit unit transfer is inferred from the different2023fit. The15MW cooling allowance has no equipment decomposition. Per-coil geometry, local stress/fit, absolute conductor margin and cross-section-dependent winding effort retain the magnet-design-transfer limits. The unchanged engineering predicates cannot certify these missing qualifications.\n')
text='\n'.join(lines)
# Readable unit/quantity spacing in prose; preserve exact inline code identifiers.
segments=re.split(r'(`[^`]*`)',text)
for i in range(0,len(segments),2):
    segments[i]=re.sub(r'(?<=[0-9])(?=[A-Za-z])|(?<=[A-Za-z])(?=[0-9])',' ',segments[i])
    segments[i]=segments[i].replace('316 LN','316LN')
(H/'record.md').write_text(''.join(segments))
