# ARIES density-profile subsystem experiment

Run from the repository root:

```bash
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/density_profile/verify.py
```

The script stages the two new SysML files, parses them, generates an isolated package, installs the typed mathematical-domain guard completion, regenerates its seal and executes native TEAx checks. Generated files and runtime stores are ignored locally. Durable evidence lives in `work/active/WI-081_aries-hollow-finite-edge-density-profile/evidence/`.

This evaluates local density under explicit supplied parameters. The case uses source shape values and a disclosed arbitrary amplitude; it is not a reference plasma power prediction. See the work item's spec, design and implementation record for the source ambiguity and claim boundary.
