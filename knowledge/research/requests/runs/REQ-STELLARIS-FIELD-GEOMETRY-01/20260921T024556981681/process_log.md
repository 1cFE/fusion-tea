# Research run REQ-STELLARIS-FIELD-GEOMETRY-01

**Question:** Are machine-readable coil curves, current-family normalization, winding-pack frames and dimensions, and a matching axis or equilibrium publicly available for the named Stellaris baseline, sufficient for independent pointwise magnetic-field and conductor-peak qualification?

**Consumer:** .project/active/aries-comparison-preparation/field-qualification/spec.md  ·  **Request key:** `35880dfc9ef4a3ae261681953d86a8e063b1d38a50fce77b1074bedfc18e6acd`

- searched: `Stellaris Proxima Fusion coil geometry dataset github zenodo`
- searched: `"Stellaris" "114868" supplementary data coils`
- searched: `site:zenodo.org Stellaris coils SQuID`
- searched: `site:github.com Stellaris coils Proxima SQuID`
- candidate https://github.com/proximafusion/open_stellarator_models — **keeper** Official public CAD repository; capture README to establish device identity and geometry scope before any use.
- searched: `"Stellaris" "coil" "data" "Proxima" -site:sciencedirect.com -site:doi.org`
- searched: `"SQuID" "stellarator" "data availability"`
- candidate https://zenodo.org/records/18497939 — **keeper** Author dataset discovered through direct citation in final-query result; contains study coil archive, baseline identity and finite-pack sufficiency still unverified.
- candidate https://github.com/proximafusion/constellaration — **rejected** Triage identifies plasma-boundary/equilibrium optimization dataset; no named Stellaris coil-current-pack release established.
- candidate https://github.com/proximafusion/open_stellarator_models — **rejected** Captured README identifies simplified scaled W7-X CAD, not the named Stellaris baseline; first DNS failure was resolved by successful network retry.
- failed https://zenodo.org/records/18497939/preview/zenodo_repository_auglag.zip?include_deleted=0 — Landing page registered, archive unregistered and uninspected beyond filename triage. Mixed archive preview includes quarantine-related filenames. Requires narrowly scoped screened acquisition and confirmed Stellaris baseline identity before data use; no archive downloaded. (queued)
