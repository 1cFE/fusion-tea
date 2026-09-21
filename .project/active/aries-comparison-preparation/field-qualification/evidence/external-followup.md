# Focused author-dataset follow-up

[AGENT] The follow-up acquired an isolated, pinned author script that distinguishes loaded original Stellaris coils from newly optimized alternatives. The script requires two external Stellaris input files. Neither file was acquired. This narrows the missing-data contract; it does not qualify the current model or establish universal public absence.

## Record and provenance

Request: `knowledge/research/requests/REQ-STELLARIS-FIELD-GEOMETRY-02.json`. Run and computed return: `knowledge/research/requests/runs/REQ-STELLARIS-FIELD-GEOMETRY-02/20260921T025127422759/`. This question follows a concrete newly identified author dataset, rather than repeating the completed broad search. One search and two captures were used under limits of one and three. Return: `REGISTERED`, with one queued paper rejected by the registry and no bounded negative.

The registered source is `knowledge/sources/author_stellaris_augmented_lagrangian_script_at_a79006b/raw.html`, captured from `https://github.com/PedroFranciscoGil/simsopt/blob/a79006b0bc1e6df8ab48de284e3457d39a49b995/examples/3_Advanced/auglag/auglag_stellaris.py`. Its raw SHA-256 is `1a638e56f3d7bf6a45c0c918a335bef855727c3da130e532292a245be1880fcc`; extraction SHA-256 is `b09de07ca67b04a136b07a659c928ac1ac0a76bea9e834d748c4b47ea7a30694`.

The standard `output.md` extraction retains page navigation but loses the code. The captured raw HTML contains a JSON `rawLines` array holding all 276 source lines. [author-stellaris-script.txt](author-stellaris-script.txt) is a derived, unexecuted view of that exact array, retained for readable line references. The registered raw HTML remains the authority. To reproduce, parse the HTML `script[type="application/json"]` elements as JSON, recursively locate `rawLines`, and join its strings with newlines plus a terminal newline. No code in the source was executed.

## What the isolated source establishes

| Finding | Source lines in the derived view |
|---|---|
| The script identifies the Stellaris SQUID design and says the plasma boundary is available from Jorrit Lion upon request. | 6–7 |
| It documents parameters for five-coil and six-coil alternative solutions, then selects six in its defaults. | 9–29, 57 |
| It reads `tests/test_files/input.stellaris` as a VMEC boundary, including a half-period grid and a full-torus plotting surface. This is a required input, not embedded boundary coefficients. | 71–92 |
| It loads `tests/test_files/coils.stellaris` into original coils with a Fourier order and quadrature setting, then evaluates the original field on the supplied surface. Actual currents come from that missing coil file. | 102–113 |
| It declares a square 0.32 m cross section and 256 turns for regularized force calculations. These are code settings, not a recovered six-family winding-pack definition or a conductor-peak validation dataset. | 94–102 |
| It separately initializes new coils using the boundary, a fixed summed current, and field-period/stellarator symmetry. The source comment identifies an imposed field normalization averaged over the major radius. This is an author optimization choice, not an independent pointwise field oracle. | 146–169 |
| It writes newly optimized geometry and a serialized Biot–Savart object. Output filenames in a script are not acquired output datasets. | 254–275 |

[AGENT] This source establishes an original-versus-alternative distinction at the algorithm level. It does not supply the original `input.stellaris` or `coils.stellaris`, prove any archived alternative's identity, or provide local winding-pack orientation frames, conductor positions and independent finite-pack peak-field verification.

## Concrete acquisition boundaries

The direct author-paper candidate `https://arxiv.org/html/2507.12681v3` returned `holdout_hit` from `source_registry.py`, with rule `term:aries-cs`, three matches at offsets `[63547, 64555, 155078]`. Its receipt is in this run's `receipts/`. The candidate was stopped. No cropped version was registered and no paper claims from web-tool triage are adopted as scientific evidence. This is a workflow rejection of that candidate, not evidence that its Stellaris section or the dataset lacks geometry.

The author branch file tree was inspected as filename-only triage through `https://api.github.com/repos/PedroFranciscoGil/simsopt/git/trees/auglag_coils?recursive=1`. The returned tree identified commit `a79006b0bc1e6df8ab48de284e3457d39a49b995`, reported `truncated: false`, and exposed the isolated script that was subsequently registered. Neither required basename appeared in this observed tree. The tree itself was not registered; this observation is an acquisition log, not a citable scientific absence claim. No unrelated numerical files were retrieved.

The Zenodo preview provides plain filename spans, without per-member retrieval links. Its exact Stellaris-named entries are `zenodo_repository/figures/poincare_fieldlinestellaris.png`, `zenodo_repository/figures/stellaris_coils.png`, `zenodo_repository/figures/stellaris_coils5_130.png`, `zenodo_repository/figures/stellaris_coils6_145.png`, and `zenodo_repository/figures/stellaris_coils6_engineering.png`. The preview does not establish that these images contain recoverable coil definitions. No isolated executable member was identified by those names. No archive was downloaded and no archive numerical contents were read. The registered landing page remains a real unresolved dataset lead, not a qualified geometry source.

## Supported conclusion and next dependency

[AGENT] The original Stellaris boundary and coil files are now named precisely. Field-method qualification still depends on acquiring and authenticating them, defining current/turn conventions, and supplying the finite-pack geometry and independent verification needed for conductor peaks. A usable alternative would need its own explicit configuration identity and support assessment. The captured script neither fills these gaps nor justifies replacing the existing geometry family. No model or plant calculation was run, and this post-reveal investigation makes no clean-holdout claim.

[AGENT] The reproducibility script still requires the boundary it describes as available on request and a separate original-coil file. Their absence from the inspected pinned repository tree does not establish absence from the uninspected ZIP or elsewhere. Partial field-curve data may exist there; its identity and sufficiency remain unverified. No new domain insight or fitted field normalization is adopted.
