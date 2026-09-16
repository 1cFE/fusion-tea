# Independent final assurance — primary-loop sizing

**PASS: technical answer meets the quantified-requirement/evidence-gap branch.** No equipment qualification, installed price, combined-feasibility pass or global optimum is established. Formal goal closure remains owner-held.

Reviewed 2026-09-16 by the continuing independent source/math reviewer, not the study author. Scope: frozen study `75772ebabdd9f99e2cc3cbc4b55e71aa16f81148`, source/integration checkpoint `df41ea97d6628584ee270284ef0dfcffbb65eb8b`, and the proposed answer, Round 1 result, findings and executor synthesis. Reused the prior scoped hydraulic and original-page cost reviews. No frozen artifact, model or package was changed.

## Independent checks

- Recomputed all 168 snapshot artifact hashes and compared every artifact byte against the frozen Git revision. All 174 required retained files also match that revision. Snapshot SHA256 is `ea965290dfbd83cb1962951fd5708a3e3a1765d89e3e1bdc3859ae16ab0cc23b`.
- Opened both SQLite stores read-only. Checked content-addressed evidence for the baseline and twenty study cases; joined all twenty exported inputs, outputs and predicate reports to native evidence. All five fourteen-loop entering controls preserve every numeric output and all twenty verdicts plus headline exactly.
- Fresh independent-oracle evaluation reproduced all **4520 mapped scalar comparisons and 400 exact predicate comparisons**, with the recorded 1e-9 absolute/relative tolerance for scalars. Sixteen native numeric channels remain outside this oracle map; all 242 are retained. This is numerical consistency under shared assumptions, not independent physical validation.
- Independently recomputed flow, pressure ratio/loss, compressor temperature/work, IHX energy balance, equipment counts, integer-count requirement and annual break-even burden for all twenty cases. Magnet outputs and divertor heat-account outputs remain exactly fixed within each family. Only loop-capacity verdicts change; all twenty cases fail combined feasibility.
- Confirmed no production model/package differences from entering `b9ddffb7` through the frozen study. The ten passing integration gates support the unchanged package; the disclosed read-set coverage omission remains unverified.

## Scientific and economic reading

The informative case needs sixteen averaged loops under the unchanged 225.0777778 kg/s allowance. At sixteen, total flow is 3433.821515 kg/s, pressure loss 299.290653 kPa, compressor electricity/recovered work 199.287304 MW, and required IHX duty 3765.654329 MW. Conditional counts are 32 circulators and 16 IHXs. Divertor peak remains 11.156873308 MW/m² against 10. The reference already passes the flow screen at fourteen loops.

The answer correctly distinguishes source nominal flow from hardware maximum, averaged replication from heterogeneous source circuits, required duty from installed rating, and calibration/lower-bound drive assumptions from qualification. Routing, exchanger/compressor performance and physical installation remain unresolved.

The $5.764 million coolant-account increase is not added-equipment pricing. Fresh arithmetic confirms $48.067592 million/year informative-case break-even burden using `8760 × net MW × availability`; this is an annual accounting threshold, not capex or realized savings. The missing internal cost report, large-pipe omission and installation/currency/year gaps remain explicit.

## Dispositions and reviewed documents

Accept proposed findings #1–#4 and learnings L-001–L-003 within these limits. All fourteen prior-finding mappings match the latest preceding rows in the frozen discovery log; residual scope is preserved. Their joined acceptance updates remain coordinator bookkeeping after this review, not new scientific work.

Reviewed working-tree answer SHA256: `c06fb5d2361f1a91269f78ab19f7fa7b6e1a5c191f4426a4e787c3b02eeedd17`; findings: `79642a24f209a0d17bcddeab8ccc55cb1391e84d1136c0bd50021f242d8b6776`; synthesis: `dc4cb4da13f6b758d4e25c96e62cab6097fec8ea24022578bd5289476ca18007`. Round 1 result in trail was reviewed before review-acceptance bookkeeping.
