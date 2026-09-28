# Nuclear-data and tally authority

Date: 2026-09-18. `[AGENT]` Evidence for the isolated OpenMC0.15.2 research runtime; no model or test changes. Native request `REQ-computed-tritium-breeding-07` used zero searches and two captures. Its run `knowledge/research/requests/runs/REQ-computed-tritium-breeding-07/20260918T205426929015/return.json` closed REGISTERED. The returned `max_searches` limit reflects the deliberate zero-search bound, not a capture failure.

## Processed dataset identity

The [pinned dataset repository](https://github.com/openmc-data-storage/ENDF-B-VIII.0-NNDC/tree/466ab3042f70e60b693fbbd3f6f15f30dba7cd1d) is registered at `knowledge/sources/openmc_endf_b_viii_0_nndc_processed_hdf5_dataset_pinned/`. This establishes the selected distribution and immutable commit. It is processed ENDF/B-VIII.0 NNDC neutron HDF5 data, not FENDL. Comparisons against published FENDL calculations therefore combine data-library differences with other modeling differences.

[Runtime evidence](transport-runtime.md), [individual data hashes](runtime/data-manifest.json), [selection](runtime/data-selection.json), and [processed properties](runtime/data-properties.json) preserve exact file identities, available temperatures, energy limits and MT205 presence for the initial subset. Additional material isotopes are recorded in [extra data hashes](transport/data-manifest-extra.json) and [extra selection](transport/data-selection-extra.json). No HDF5 data were downloaded again for this registration. The captured GitHub page is repository metadata; its registry hash is not the hash of the full nuclear-data library.

## Tally interpretation

The [official version0.15.2 documentation](https://docs.openmc.org/en/v0.15.2/usersguide/tallies.html), registered at `knowledge/sources/openmc_0_15_2_tally_scores_and_source_normalization/`, defines `H3-production` as total tritium production per source particle. Integer scores select ENDF MT reactions. All tallies use source-particle normalization; filters and nuclide selection determine their scope (§§8.1–8.3).

The installed API explicitly maps MT205 to `(n,Xt)` in `.codex-test/breeding-transport/env/lib/python3.12/site-packages/openmc/data/reaction.py:55`. The runtime and plant prototype currently request this MT205 score. The user-guide table does not directly document that alias or prove its equivalence to the separate `H3-production` product-yield implementation. The [paired execution check](transport/tritium-semantics-check.json) now establishes exact agreement of both means and standard errors for breeder Li6 and Li7 in10,000 histories with the installed engine and pinned data. This resolves the candidate-specific equivalence question; it does not establish equivalence for every nuclide or other library. Breeder Li6+Li7 production and whole-assembly tritium remain different tally scopes.

## Validation limits

The smoke run demonstrates data loading, transport execution and tally readback. Byte counts, Git blob hashes and SHA256 values establish reproducibility, not nuclear-data accuracy. This acquisition does not independently verify the upstream processing code/version, reconstruction and linearization tolerances, Doppler broadening, probability tables, reaction-product completeness or covariance propagation. Neither the source registration nor smoke test supplies those uncertainties or validates blanket TBR; experimental benchmark evidence is separate.

Interpolation between processed600K and900K cross sections at773.15K is independent of the material-density prescription. Published500°C liquid/gas density cards and representative constant solid densities retain the qualifications in [material basis](material-manifest-proposal.md). A statistical tally error excludes library bias, processing uncertainty and geometry/material uncertainty.
