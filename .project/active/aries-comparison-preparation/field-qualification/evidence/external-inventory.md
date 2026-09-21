# External geometry search

[AGENT] This bounded search did not acquire an executable, identity-matched Stellaris magnetic-field input set. It registered two landing pages and retained an unresolved author dataset lead. This is not evidence that public Stellaris geometry does not exist.

## Search contract and outcome

Request: `knowledge/research/requests/REQ-STELLARIS-FIELD-GEOMETRY-01.json`. Consumer: `field-qualification/spec.md`. Run: `knowledge/research/requests/runs/REQ-STELLARIS-FIELD-GEOMETRY-01/20260921T024556981681/`. Six search queries and three capture attempts were used. The computed return is `REGISTERED`; no bounded-negative file was produced. The run ended at its declared limits. Existing primary-paper data availability is handled by the local inventory; no duplicate paper extraction was attempted.

Search domains covered the named paper and supplementary-data terms, official Proxima repositories, Zenodo, and Stellaris/SQuID coil-data terms. Two overly broad Stellaris queries returned substantial unrelated material. Search and web-open output served only as triage. Claims below about registered sources come from their retained captures. No authors were contacted, plant calculations run, or model equations edited.

## Registered sources

| Source | Captured evidence and usefulness | Limitation |
|---|---|---|
| `knowledge/sources/proxima_fusion_public_simplified_stellarator_cad_models/output.md` | Official repository README states that its provided CAD model uses a scaled W7-X plasma and simplified geometry for simulation benchmarks. This establishes that this advertised model is not the named Stellaris baseline. | Only the landing page was captured. CAD payload was not downloaded or field-qualified. |
| `knowledge/sources/coilsets_and_scripts_from_augmented_lagrangian_methods_for/output.md` | Author Zenodo record, DOI `10.5281/zenodo.18497939`, identifies an archive associated with *Efficient Computation of Stellarator Coils with an Augmented Lagrangian Optimization Method*, arXiv `2507.12681`, and an author SIMSOPT branch. It is a concrete coil-data acquisition lead. | The capture is the landing page, not archive contents. It establishes neither original Stellaris baseline identity nor finite winding-pack data sufficiency. |

Raw/extraction SHA-256 respectively:

- Public CAD README: `fbe19b2ab852fb7910324aaf51a4e2edbd62377220805bb67573d2e04a7d5a39` / `1af5e6d19a1e2912c029c6904f2f12290b544bc3ca6f7a5ff58f0743a14861f1`.
- Author dataset landing page: `4af47472e14c982c34b16c1fd4a836154dd40e8ca417b129f987fdb89942e42e` / `37b1d6edf2f1e1b1ae087066eb57e5d95ac805667a63dcf9aa84fb8fc2617183`.

Each registered directory contains `raw.html`, `output.md` and `metrics.json`; registry receipts contain the identities. The registry alone wrote the source directories, manifest and index.

## Acquisition limits and unresolved lead

The first official-CAD registration returned `capture_failed`, reason `extract exited 1`. A diagnostic invocation of the same extractor reported `Temporary failure in name resolution`. A network-enabled retry succeeded through the registry. The computed return still queues the original failed attempt; this is a retained historical receipt, not a remaining inability to reach that README.

The Zenodo archive-preview URL is `https://zenodo.org/records/18497939/preview/zenodo_repository_auglag.zip?include_deleted=0`. The web tool could not open it. A network-enabled direct retrieval reached the filename preview. Filename-only triage indicated Stellaris-named figures and coil JSON files, but did not establish their relationship to the published baseline. The broad preview also exposed unrelated comparison filenames with quarantine-related names. Content exploration stopped at that signal. No archive was downloaded, no numerical member contents were read, and the preview was not registered or adopted as scientific evidence. The archived dataset remains queued for narrowly scoped, screened acquisition. The registry interface documents URL/web/PDF capture, not a verified ZIP-member ingestion route.

ConStellaration was considered as a search lead and rejected at triage as an unestablished match for the required coil/current/pack input set. It was not registered, so no substantive dataset claims are adopted here. A direct official product-page open also failed in the web tool; that failure does not establish absence of data. The six-query limit was already reached before the suggested pre-sPROCESS follow-up; no claim about its Stellaris-specific inputs is made.

Exact filename-only follow-up leads from the unregistered preview are `zenodo_repository/figures/poincare_fieldlinestellaris.png`, `zenodo_repository/figures/stellaris_coils.png`, `zenodo_repository/figures/stellaris_coils5_130.png`, `zenodo_repository/figures/stellaris_coils6_145.png`, and `zenodo_repository/figures/stellaris_coils6_engineering.png`. No executable member identified itself by Stellaris or SQuID in the filename search. Filenames do not establish image contents, baseline identity, or absence of appropriately named data elsewhere. The registered landing page advertises the study archive but makes no original-versus-alternative Stellaris claim. The filename quarantine signal is not a registry `holdout_hit` and does not establish that an isolated Stellaris member is barred; no such rejection occurred in this run.

## What is still needed

[AGENT] No newly acquired payload identifies all six independent coil paths, their complete symmetry/coordinate conventions, signed current and turn normalization, a matching axis/equilibrium and field statistic, local winding-pack frames and cross sections, and independent pointwise or conductor-peak verification data for the same named configuration. Aggregate coil count, bounds, or a coil optimization archive title cannot determine these quantities. Neither registered source supplies a qualified pack-size dependence or supports a transfer to changed coil shape/count/current distribution.

[AGENT] A follow-up can investigate the retained author dataset through a narrowly scoped acquisition request. It must first resolve quarantine screening and original-versus-alternative coil identity. An alternative coilset would define a different explicitly selected geometry, not validate the existing Stellaris baseline by substitution. Until those checks succeed, conclusions about numerical field qualification remain parked.
