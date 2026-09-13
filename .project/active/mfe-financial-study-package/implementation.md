# Current financial consumer implementation

[AGENT] Implementation starts from corrected production HEAD `708dddefdbeb5f990d9ef824ce06258fa6b46345`. The frozen package has semantic fingerprint `15ed665c374729a984f29fa753f444677805939ffb195933419b3489debbd47e` and executable fingerprint `1a7c216dabff8425c279f6b3c2781629115729173fc0b406600497ac348b4340`. This implements the inferred SC-1–5 contract in `spec.md@dbaea1ad`; certification belongs to a fresh auditor.

## Implementation choices

[AGENT] The independent oracle evaluates retained finance with 80-digit stdlib Decimal arithmetic, converting the actual represented binary64 operands exactly. Power evaluation and cancellation use high precision rather than the production helper's binary64 numerical branches. Exact-zero CRF and IDC and equal-rate annuity use their analytic limits. The worst tested IDC cancellation loses roughly 52 digits at a 1e-18 rate and a binary64 neighbor of one year. Eighty-digit arithmetic leaves over 25 significant digits before conversion back to binary64. The tests independently evaluate CRF as inverse dated unit payments, integer annuities and construction finance as dated sums, and fractional IDC through a generalized binomial series. Fractional annuity equality is tested against its PV identity. No production financial code is imported by the oracle.

[AGENT] Held replacement uses its existing clipped lifetime and ceil-derived event count, followed by high-precision dated sums. Live replacement uses its existing independently derived dates. Live energy retains the same year-bin geometry and computes discount factors at high precision. All physical statements in the oracle remain unchanged.

[AGENT] The current input/output adapter remains unchanged: 99 mapped inputs of 246, with 147 explicit omissions; 141 mapped outputs of 158. Seven of the thirteen finance-dependent native channels are already mapped. The input adapter exposes discount rate, with inflation fixed at its existing 0.02 default. Current-route tests exercise exact equality there, zero, signed rates through 1e-18, and nearby distinct rates. Direct oracle tests cover other escalation and Real-duration cases. This migration adds no adapter mappings or output coverage.

[AGENT] The current radius caller now uses `tests/study/financial_radius_controls.py`. It retains the frozen controls and applies exact equality to all 145 nonfinance native channels at both baseline and R14. Only the exhaustive thirteen rate-dependent channels may use 1e-9 relative tolerance, with zero absolute tolerance against the frozen ordinary values. Independent finance checks justify that tolerance. The historical helper and its evidence remain unchanged.

## Metadata preparation

[AGENT] `implementation/refresh_metadata.py` writes only to a fresh caller-selected directory. It calls the current native fingerprint producer, baseline route and indicator producer. The inspected older radius refresh script writes the repository manifest, graph fixtures and a test file despite accepting a workdir, so it was read as precedent and never executed. The new script explicitly passes its isolated manifest to baseline execution and does not import the old script. Producers read current package inputs, pipelines and contracts; baseline stores and identity reports go under the fresh output directory.

[AGENT] Two isolated preparations produced byte-identical manifests and graph fixtures. Indicator reports differ only in the recorded destination manifest path. All graph fixtures already match their committed versions, so no fixture update is needed. The current manifest retains ties, axes, objective meanings, baseline physical inputs and all eighteen verdicts. Its executable identity changes to the corrected package. Native baseline headline changes by one ulp, from 224.26923288439 to 224.26923288439002, matching the already-attributed native finance roundoff. No integration candidate or historical study pin is promoted.

## Validation record

Final focused results and the exact 22-node passing differential are recorded in `implementation/results.md`. Integration acceptance tests run only against disposable fixture copies. Existing historical failure evidence is retained without a broad rerun.

## Remaining limits

[INHERITED] The broader model, engineering feasibility, finance-domain and coverage limitations remain. The ordinary divertor violation remains. Construction-duration zero is parked; extreme rates, underflow/overflow and arbitrary untested durations receive no new acceptance credit. Native/model/generated artifacts, native WI-052 records, older coding evidence and frozen study records are immutable for this stage. A fresh independent audit must assess these changes and the native completion prerequisites.
