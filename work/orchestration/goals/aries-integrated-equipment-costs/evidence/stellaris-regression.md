# Isolated Stellaris regression

[AGENT] A fresh isolated replay on 2026-09-22 reproduces all 1,352 original numeric outputs and 68 responses exactly, including inherited failed engineering predicates. This establishes unchanged baseline behavior, not scientific adequacy.

The script copies the original generated package into a new temporary directory, prepares it through the stock route and evaluates the empty proposal using the original fixed inputs. The original package and all 8,752 protected files remain byte-identical before and after. `stellaris-regression-receipt.json` records the baseline digest, temporary copy, exact comparison and preservation checks; `stellaris-regression-actual.json` retains all channels; `stellaris-regression.log` retains runtime output. Existing float-as-Boolean serializer warnings are preserved.

The replay script reuses the predecessor's reviewed procedure, changing only the evidence directory and preservation-manifest filename. Run from the repository root with `.codex-test/run python work/orchestration/goals/aries-integrated-equipment-costs/evidence/stellaris-regression.py`; choose a fresh evidence destination for any later replay to preserve these receipts.
