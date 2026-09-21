# Geometry acquisition findings

This continues [F015–F018](../field-qualification/findings.md). These are post-reveal acquisition findings, not new physical results.

## F019 — The complete archive directory omits both named inputs

[AGENT] All 677 directory entries in the author archive were parsed and independently cross-checked with Python's ZIP reader. Neither `input.stellaris` nor `coils.stellaris` appears as an exact basename, ignoring case. The five Stellaris-labeled entries are images. The archive index was previously unresolved; its named-file membership is now checked. Differently named or embedded data remain possible because member payloads were not inspected. [Evidence](evidence/archive-inventory.json).

## F020 — Exact-path repository history did not recover the files

[AGENT] The author branch resolves to the previously pinned commit. GitHub's commits API returned empty arrays for both exact paths with no pagination links. This is evidence about those paths and that history, not every branch or renamed file. [Evidence](evidence/history-result.md).

## F021 — The field repair still needs configuration data

[INHERITED: ../field-qualification/capability-contract.md] The required field calculation needs coil geometry, current conventions and winding-pack information tied to the published configuration. [AGENT] Neither follow-up supplied these inputs. Model qualification remains open; a narrower conductor diagnostic or more detailed archive inventory cannot supply the missing physical geometry. The [unsent request](../field-qualification/data-request-draft.md) specifies the data dependency.
