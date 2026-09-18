# Transport runtime probe — 2026-09-18

[AGENT] Read-only probe through `.codex-test/run python` found numpy, scipy, pymupdf and syside importable. The openmc Python module is absent. `openmc` and `mcnp` executables are absent from PATH. `OPENMC_CROSS_SECTIONS` is unset. Docker is present at `/usr/bin/docker`; no daemon, transport image, Serpent installation or nuclear-data inventory was established. This is a narrow environment finding, not proof that transport cannot be provisioned.

Initial source-registry URL capture failed with `extract exited 1`. A direct sandbox curl probe could not resolve the publisher hostname. An approved network download to `/tmp` succeeded; native local-PDF registration succeeded for Lyytinen2024 and Shimwell2019. No seam code or runtime installation was changed.
