# Native readiness screen

[AGENT] Executed 2026-09-26 after the fresh feasibility review released these diagnostics. Script: `readiness-screen.py`; complete outputs, exceptions and constraint identities: `readiness-screen.json`. Each package was copied into `/tmp/component-readiness-r1` and evaluated through its own strict stock route. The original packages were not modified. These cases test interfaces and inherited claims; they are not matched technology alternatives and establish no economic ranking.

| Case | Input change or retained case | Native outcome | Reading |
|---|---|---|---|
| S0-default | Unchanged Stellaris defaults | Executed; 7 whole-plant check failures | Steam gross 1219.998 MW, exchanger duty 3301.213 MW and 20 K main minimum gap; unrelated plant failures remain in receipt |
| S1-salt436 | Salt hot 436 °C only | Refused | Salt input heat join residual 490.950 MW; changing a named temperature alone does not change the supplying salt-loop physics |
| S2-steam416 | Main and reheat steam 416 °C on unchanged equipment | Executed; 22 failures | Steam gross 1198.749 MW; 15 additional failed checks against S0's 7, including offered-condition dependencies; no supported equipment improvement |
| S3-source456 | Primary temperature rise 156 K, source hot 456 °C | Refused | Nonpositive IHX terminal approach; the existing salt window cannot accept this boundary |
| S4-source480 | Primary temperature rise 180 K | Executed; 31 failures | Heat duty changes to 3366.775 MW and offered/capacity checks change; it is not a constant-duty temperature comparison |
| S5-source520 | Primary temperature rise 220 K | Executed; 10 failures | Heat duty changes to 3257.462 MW; same qualification |
| B0-original | Prior `ir-f2500-r1.5183` | Executed; no implemented check failures | Reproduces 426.579 MW whole-assembly net and 0.311222 bypass; not downstream subsystem net |
| B1-matched | Prior `ir-boundary-f2500` | Executed; no implemented check failures | Reproduces 620.819 MW whole-assembly net; retained solver point has bypass 1.00008e-6, near zero rather than mathematically zero |
| B2-unremoved | Prior `ir-f2500-r1.4250` | Executed; 3 failures | Reproduces 620.008 MW but return residual 0.497477 K; remains inadmissible |

All 274 stored output channels of each Brayton control replayed exactly: 822 comparisons, zero mismatches. This is replay against retained native evidence, not an independent physical oracle. The model's missing cooler/recuperator hardware checks remain missing even where its existing predicates all pass.

The stock steam route emitted inherited Pydantic warnings about floating Boolean defaults. It executed and retained the Boolean verdicts; no warning was suppressed or input silently repaired. Two refusal messages were recorded as expected engineering-interface failures, not mechanical retries. No main-study store, pin or seal is claimed for this diagnostic screen.

## Replay

Use a fresh work directory; the script refuses to reuse one.

```bash
.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/readiness-screen.py --work /tmp/component-readiness-replay --out /tmp/component-readiness-replay.json
```

The script imports the retained native route and uses the launcher's sealed runtime. The three Brayton input maps come from the sealed `20260926-design-study-parameters-b/results/cases.json`; output matches are checked against that record. Steam defaults are those of the executable fingerprint recorded in the receipt.
