# Exact-path author repository history check

[AGENT] Neither named input was recovered. On 2026-09-21 UTC, the public GitHub commits API returned HTTP 200 and an empty JSON array for each of `tests/test_files/input.stellaris` and `tests/test_files/coils.stellaris`, starting at commit `a79006b0bc1e6df8ab48de284e3457d39a49b995` in `PedroFranciscoGil/simsopt`. The branch metadata independently resolved `auglag_coils` to that SHA. Neither commit response included a pagination link.

The exact API URLs, original response bodies, original HTTP headers, byte counts and SHA-256 digests are retained in [history-manifest.json](history-manifest.json) and its linked response files. Both empty-array bodies are five bytes with SHA-256 `2ba33ca0557f1bb5b7ba88d67f9d0093c7185a36ec51fe2b7bd9372d3e001d6d`. These are acquisition records, not registered scientific sources.

[AGENT] This result covers only the two exact paths in the history exposed by the commits API from the pinned branch SHA. It does not establish absence under renamed paths, on other refs, in unreachable commits, in other repositories, or in the separate archive. No numerical source contents, other configuration datasets, or model calculations were accessed. No additional web searches were needed, and no author was contacted.

The initial sandboxed HTTP request failed DNS resolution; the authorized network escalation succeeded. The checks were read-only.
