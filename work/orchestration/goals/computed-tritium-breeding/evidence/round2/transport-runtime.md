# Isolated OpenMC transport runtime

Provisioned 2026-09-18 under the runtime brief. OpenMC 0.15.2 and a selected ENDF/B-VIII.0 neutron library are runnable. A fixed-source smoke test passes. This is tooling evidence, not scientific validation or a calibrated breeding result. No sealed environment, production model, project dependency, registry, or goal state was edited.

## Runtime identity

- [AGENT] Used the conda-forge binary route documented in the [official OpenMC installation guide](https://docs.openmc.org/en/stable/usersguide/install.html). All installed files are below ignored `.codex-test/breeding-transport/`.
- Engine and Python API: OpenMC **0.15.2**, engine commit **e23760b0264c66fb7bb373aa0596801e5209d920**. Release build, GNU 14.3.0, MPI disabled, DAGMC enabled. Parallel execution here uses two OpenMP threads.
- Bootstrap: micromamba **2.9.0**, downloaded from `https://micro.mamba.pm/api/micromamba/linux-64/latest`; archive SHA256 **8761c382127e6363bd9e0a2451aa3ef90d071a79133f736e2f759a3bf13040dd**. The mutable bootstrap URL must be checked against this digest when reproducing this installation; an updated archive is a new runtime identity.
- The initial solve requested `openmc=0.15.2 python=3.12` from conda-forge. It installed 128 packages with approximately 188 MB downloaded. [Explicit package lock](runtime/conda-explicit.txt) preserves every package URL and MD5; [package manifest](runtime/package-manifest.json) additionally preserves all 128 SHA256 hashes and build identities.

## Nuclear data

[AGENT] Selected 40 individual neutron HDF5 files from the [OpenMC data-storage ENDF/B-VIII.0 NNDC repository](https://github.com/openmc-data-storage/ENDF-B-VIII.0-NNDC), commit **466ab3042f70e60b693fbbd3f6f15f30dba7cd1d**. The upstream downloader's own mapping identifies this repository as the ENDFB-8.0-NNDC HDF5 source. This is processed ENDF/B-VIII.0 data, not a FENDL library. Scientific work must carry that distinction when comparing a published FENDL calculation.

The subset contains H1/H2, He4, Li6/Li7, B10/B11, C12/C13, O16/O17/O18, Si28/29/30, V50/51, Cr50/52/53/54, Mn55, Fe54/56/57/58, Ni58/60/61/62/64, W180/182/183/184/186 and Pb204/206/207/208. Its exact size is **556,698,704 bytes**. This covers the requested initial species and common steel constituents; it does not assert completeness for a yet-unspecified steel recipe.

[Selection](runtime/data-selection.json) preserves upstream paths, byte counts and Git blob hashes. [Data manifest](runtime/data-manifest.json) preserves every immutable download URL and SHA256. The acquisition script verifies byte counts and Git blob hashes before producing the manifest. [Data properties](runtime/data-properties.json) records each isotope's processed temperatures, maximum energies and presence of the MT205 total tritium-production reaction. `cross_sections.xml` is generated from this subset only. No full multi-GB library was fetched.

## Reproduce and use

Run from repository root. Downloads need network access. The environment itself and raw data are intentionally ignored; tracked scripts and manifests reproduce them.

```bash
mkdir -p .codex-test/breeding-transport/downloads
curl -fL https://micro.mamba.pm/api/micromamba/linux-64/latest -o .codex-test/breeding-transport/downloads/micromamba.tar.bz2
sha256sum .codex-test/breeding-transport/downloads/micromamba.tar.bz2
# Require the bootstrap digest recorded above before extracting.
tar -xjf .codex-test/breeding-transport/downloads/micromamba.tar.bz2 -C .codex-test/breeding-transport bin/micromamba
.codex-test/breeding-transport/bin/micromamba create --no-rc -r "$PWD/.codex-test/breeding-transport/mamba" -p "$PWD/.codex-test/breeding-transport/env" --file work/orchestration/goals/computed-tritium-breeding/evidence/round2/runtime/conda-explicit.txt -y
.codex-test/run python work/orchestration/goals/computed-tritium-breeding/evidence/round2/runtime/fetch_data.py
work/orchestration/goals/computed-tritium-breeding/evidence/round2/runtime/run work/orchestration/goals/computed-tritium-breeding/evidence/round2/runtime/smoke.py
```

[Launcher](runtime/run) accepts ordinary Python arguments, including a script path or `-c`. It invokes the isolated interpreter through `.codex-test/run`, sets the isolated OpenMC executable on `PATH`, sets `OPENMC_CROSS_SECTIONS`, and defaults `OMP_NUM_THREADS` to 2. It does not activate or mutate the sealed environment. Scripts can use `openmc.Model.run()` directly. To run an existing XML model, invoke `.codex-test/breeding-transport/env/bin/openmc` in its directory with `OPENMC_CROSS_SECTIONS` pointing at the runtime data index.

## Check performed and limits

[Smoke script](runtime/smoke.py) builds a deliberately arbitrary 30 cm lithium sphere, launches 10 batches of 1,000 isotropic 14.1 MeV source neutrons with seed 1739, scores `(n,Xt)`, and reads the statepoint. It completed without engine errors. The score was **0.32904922245860607 ± 0.0029366263602033224** per source neutron (reported one standard deviation). The leakage fraction was 0.91450 ± 0.00318. [Machine-readable result](runtime/smoke-result.json) includes the generated model XML SHA256. Raw XML, statepoint and logs are under `.codex-test/breeding-transport/smoke/` and the runtime root.

This checks interpreter/API/engine compatibility, data loading, transport execution and tally/statepoint readback. It does not validate a blanket, an independent benchmark, thermal scattering, material compositions, scientific temperature choices, variance convergence, or a physical tritium-breeding prediction. No S(α,β) thermal-scattering kernels, photon data or depletion chains were acquired. Additional constituents or kernels must be added explicitly if a later material definition needs them.
