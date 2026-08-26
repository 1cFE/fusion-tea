# Fixture — structurally reformatted holdout protocol

Used only to prove that a protocol whose §3 bullets no longer carry backticked
paths stops the parser instead of silently yielding a shorter barred set.
Contains no ARIES-CS design or cost data (spec R-D4).

## 3. Clean-room admissibility

### Barred (do not read in demo sessions)

The barred material is described in prose here rather than as backticked path
bullets, which is exactly the reformat the parser must refuse.

1. The sealed papers in the holdout directory.
2. The concept-09 analysis tree.

### Barred by default, documented-exception path

1. The two general costing sources.

### Admissible (the clean modeling basis)

- `models/library/**`
