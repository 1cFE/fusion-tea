# Viewer regression fixture

`stellarator.snapshot.json` is copied byte for byte from `82ae3958:exploration/stellarator_e2e/stellarator.snapshot.json`, the WI-057 snapshot used by the structural/v2 viewer branches. SHA-256: `8e79aa4e489e7bcf1be8e24796a77a6df3acbbf8b327b3eb6b961e96b55bf9ae`.

The tests retain their original counts and assertions against this fixture. The live model has evolved since those branches; keeping the fixture here lets the viewer regressions run without replacing or freezing the live model.
