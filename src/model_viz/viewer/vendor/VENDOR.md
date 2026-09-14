# Vendored libraries

The viewer loads these files from this directory and makes no network request. Each was downloaded with `curl -fsSL` from unpkg on 2026-09-13 at the exact version the layout spike used. Licences were read from each package's `package.json` on unpkg.

| File | Package | Version | Source URL | Licence | SHA-256 |
|---|---|---|---|---|---|
| `cytoscape-3.28.1.min.js` | cytoscape | 3.28.1 | https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js | MIT | `92d752b48ea949720675865197fd2a0001c95bc5888545e990af60321712d4c6` |
| `dagre-0.8.5.min.js` | dagre | 0.8.5 | https://unpkg.com/dagre@0.8.5/dist/dagre.min.js | MIT | `62eb9787ccfdbdf4148d4d99d31dbf9ee4770eafee81e637d759b52aac22cd51` |
| `cytoscape-dagre-2.5.0.js` | cytoscape-dagre | 2.5.0 | https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js | MIT | `bf70fe402991dcbff33e05a7e4a5271c78020bb75e85d1c80ab7538e4157112e` |

`cytoscape-expand-collapse` is deliberately not vendored: the viewer computes the visible elements for each collapse state itself and rebuilds the graph (design D1, `.project/active/model-viz/design.md`).

Check the files with `sha256sum src/model_viz/viewer/vendor/*.js`.
