# Spike: snapshot recapture byte-stability (GSTH Item 3, bet B2)

**Date:** 2026-08-26 · **Branch:** `feat/goal-integration-seam` · **Commit:** `029b9a29` · **Owner:** Reid W
**Serves:** `.project/active/goal-integration-seam/design.md` bet **B2** (`:71`), the risk note `:170`, and gate 4 in the gate table (`:101`)
**Status:** closed — **CONFIRMED, and stronger than the bet claimed**

## Summary of Findings

**CONFIRMED.** Recapturing the instance-graph snapshot from the same models path is **byte-identical** to the tracked `exploration/stellarator_e2e/stellarator.snapshot.json`. Not "differs only in `captured_at`" — **zero bytes differ, and zero key paths differ**, on a fully recursive key-by-key comparison of both files.

| comparison | sha256 | bytes | differing key paths |
|---|---|---|---|
| tracked (`stellarator.snapshot.json`) | `3a923b4f…f00d314` | 654,504 | — |
| recapture #1, from the real `models/` | `3a923b4f…f00d314` | identical | **0** |
| recapture #2, from the real `models/` | `3a923b4f…f00d314` | identical | **0** |
| recapture from a `/tmp` copy of `models/` | `3a923b4f…f00d314` | identical | **0** |

**The premise B2 rests on is stale, and that is the real finding.** The tracked snapshot has **no `captured_at` key at all** — the string does not appear anywhere in the file. `captured_at` belonged to the pre-v6 flat snapshot format. The WI-029 audit that B2 cites (`work/analysis/20260725-091831_audit_WI-029_handshake-lcoe-construction.md:190`, 2026-07-25) measured that older format, whose top-level keys were `aggregation_expressions`, `calc_defs`, …, `captured_at`, …. The stellarator-model-migration commit `89f78130` (2026-08-21) replaced it with the **v6 envelope**: top-level keys are exactly `authority`, `format`, `instance_graph`, `integrity`, `sources`, `version`. The v6 envelope deliberately dropped the `capture` block — including `captured_at` — because those fields could not be verified even with the sources in hand (`sysml_codegen/snapshot/envelope.py:38-44`). The envelope module states the consequence outright: *"capture is deterministic. The same model in the same environment produces byte-identical snapshot files"* (`envelope.py:46`). This spike measures that claim on the real package and finds it true.

**What this means for gate 4.** Gate 4 is not at risk, and its comparison can be **stronger** than the design wrote:

- **Recommended:** compare the recaptured snapshot to the tracked one **byte-for-byte** (a sha256 of each file). This is the strongest available form, it is what actually holds, and it needs no exclusion list.
- The design's current wording — "snapshot differs outside `captured_at`" (`design.md:101`) — should drop the `captured_at` exclusion. Excluding a key that does not exist is harmless at runtime but is dead wording that will mislead the next reader into thinking the snapshot carries a timestamp.
- The fallback the design reserved (narrow to `instance_graph.fingerprint` alone, recorded as weaker — `design.md:71`, `:170`) is **not needed** and should be struck rather than carried as a live option.
- `design.md:50`'s "Snapshot recapture is not byte-stable" is now measured false. Recapture **is** byte-stable under the v6 envelope.

**Bonus finding: the models path does not leak into the snapshot.** Capturing from `/tmp/spike-snap/.../models` produced the identical file to capturing from `/home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/models`. The v6 envelope records sources as root-relative referents (`sources.files[].referent = "root-0/analyses/mfe_account_costs.sysml"`), not absolute document paths. This kills a hazard the older format had: WI-027 recorded that a fresh capture emitted absolute `file:///…` `document_path` values where the committed file had relative `file:exploration/…` ones (`work/completed/20260720_WI-027_demo-constraint-execution/plan.md:361`). That difference class is gone in v6. Gate 4 may capture into `--out-dir` from any models root without path-normalizing anything.

**Runtime and env preconditions.**
- **Runtime: 1.65s** per capture, three times identically. Snapshot recapture is not an expensive gate.
- **`SYSIDE_LICENSE_KEY` must be exported.** Capture is the license-requiring entry point (`sysml_codegen/snapshot/capture.py:1-2`). Export via `set -a; source ~/1cfe/agentic-mbse/.env; set +a`. In R-A6 terms this is a **could not run**, not a refusal — the same class the sibling spike recorded for generate (`spike_regen_determinism.md`).
- **`STOP_PARSER_TEAX_ROOT` is not needed** for capture. teax matters at verification (gate 8), not here.
- **The pin is the installed wheel:** `sysml_codegen` 0.1.1 at `.venv/lib/python3.12/site-packages/sysml_codegen/`, matching the git rev pin in `pyproject.toml`. Migration invariant I2 (never capture through a local checkout) was observed.

**Scope of the claim.** One package (stellarator, MFE family) at one sealed state (`029b9a29`), under one codegen pin, in one environment. Byte-identity is environment-conditional by construction: the `authority` block restates `syside_version` 0.8.4, `sysml_codegen_version` 0.1.1, `agentic_mbse_version` 0.1.3 and the pinned standard-library digest, so a toolchain bump *will* move the bytes. That is a feature, not a fragility — the toolchain-pin gate (gate 1a) stands in front of it. It does mean gate 4's byte comparison is a lineage check as much as a content check, which is the right thing for it to be.

## Question / Goal

`design.md` bet **B2**: recapturing the instance-graph snapshot from the same models path differs from the tracked `stellarator.snapshot.json` **only** in the `captured_at` key.

**Confirms:** a clean recapture differs from the tracked file in nothing but `captured_at`.
**Disproves:** any other key path differs — in which case gate 4 refuses every invocation, and its comparison must narrow to `instance_graph.fingerprint` alone (recorded as weaker).

Evidence before this spike was one recorded comparison (`WI-029 audit:190`), not a measurement. The design tried to remeasure and was blocked by sandbox restrictions on the license export (`design.md:50`).

## Log

**Approach.** The real tree is read, never written. Every capture goes to `/tmp`. Gate 4's own shape reads the real `models/` root, so the probe does that too — twice, for recapture-vs-recapture stability — and adds a third capture from a `/tmp` copy of `models/` as a path-sensitivity control. Probe script: `spike/probe_snapshot_stability.sh`.

**Step 0 — structure of the tracked snapshot, before running anything.** Walking the tracked file showed six top-level keys and **no `captured_at`**:

```
authority format instance_graph integrity sources version
.instance_graph.fingerprint = '3508b4b6c410cf04473637733c72ede83b86ae8313004ade6c7d3f7f19d0f443'
.integrity.digest           = 'e991765aa1dead8f8ca590ea78c58c2c45e79af66d7bd1d9a2668db5a631af94'
.sources.fingerprint        = '25d3d52a1cb0550b55edb9501aa4b17d0f96807c40fb57c43326e29b597ce65a'
.version = 6
```

That alone put B2's premise in doubt, so the probe was written to report *every* differing key path recursively rather than to check a named exclusion.

**Step 1 — the probe.** Three captures via the entry point the design and WI-030's plan both name (`work/completed/20260822_WI-030_computed-beta-peak-field/plan.md:156`):

```python
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
capture_instance_graph_snapshot([Path(models_root)], Path(out))
```

Result — all three captures produced the same sha256 as the tracked file:

```
   real1    3a923b4faeeadfa596bbc183423f7b72b61535acbadd7137a82ac9f47f00d314   wall=1.65s
   real2    3a923b4faeeadfa596bbc183423f7b72b61535acbadd7137a82ac9f47f00d314   wall=1.65s
   scratch1 3a923b4faeeadfa596bbc183423f7b72b61535acbadd7137a82ac9f47f00d314   wall=1.65s
   tracked  3a923b4faeeadfa596bbc183423f7b72b61535acbadd7137a82ac9f47f00d314

   real1 vs tracked:    BYTE-IDENTICAL
   real2 vs tracked:    BYTE-IDENTICAL
   scratch1 vs tracked: BYTE-IDENTICAL
   real1 vs real2:      BYTE-IDENTICAL (recapture-vs-recapture stable)
   real1 vs scratch1:   BYTE-IDENTICAL (models path does not leak)
```

**Step 2 — key-by-key deep diff**, recursive through dicts and lists to every leaf, so ordering, float formatting, and nested content would all surface:

```
--- tracked vs real1:    0 differing key path(s)
--- tracked vs real2:    0 differing key path(s)
--- tracked vs scratch1: 0 differing key path(s)
--- real1 vs real2:      0 differing key path(s)

'captured_at' present anywhere in tracked : False
'captured_at' present anywhere in real1   : False
```

There is no list of differing key paths to characterize as timestamp / ordering / float-formatting / content. The set is empty.

**Step 3 — where `captured_at` went.** Walked the tracked file's git history to check whether the key ever existed:

```
ba5c9945 2026-08-21  captured_at_hits=0  v6    [authority, format, instance_graph, integrity, sources, version]
89f78130 2026-08-21  captured_at_hits=0  v6    [authority, format, instance_graph, integrity, sources, version]
f22bd288 2026-07-25  captured_at_hits=1  vNone [aggregation_expressions, calc_defs, …, captured_at, …]
ad41a1d5 2026-07-20  captured_at_hits=1  vNone [aggregation_expressions, calc_defs, …, captured_at, …]
```

`f22bd288` is the WI-029 commit the audit was written against. `89f78130` (stellarator-model-migration Phases 1-3) is the format flip. So the WI-029 observation was correct for its format and simply does not carry to v6 — an inherited premise, not a wrong measurement.

**Step 4 — mechanism, read from the envelope.** `sysml_codegen/snapshot/envelope.py:38-46` says the v6 envelope removed `capture.model_name` / `capture.captured_at` because they were unverifiable, and states that capture is therefore deterministic. `sources.files[].referent` is root-relative (`root-0/analyses/…`), which is why the path-sensitivity control came back identical.

**Step 5 — real tree untouched.** `git status --porcelain` at close shows one entry: the probe script itself (`?? .project/active/goal-integration-seam/spike/probe_snapshot_stability.sh`). The tracked snapshot's sha256 is unchanged at `3a923b4f…f00d314`. No file under `exploration/` was written.

## Reproduction

```bash
cd /home/reid/1cfe/fusion-tea
./.project/active/goal-integration-seam/spike/probe_snapshot_stability.sh
```

The script exports the licence itself (`set -a; source ~/1cfe/agentic-mbse/.env; set +a`), stages a scratch copy of `models/` under `/tmp/spike-snap/<short-sha>/`, runs three captures, and prints the byte comparison and the recursive key diff. Artifacts land in `/tmp/spike-snap/<short-sha>/out/` (`*.snapshot.json`, `cap_*.log`, `keydiff.txt`). Expected output: four identical sha256 values and `0 differing key path(s)` on every comparison. Nothing outside `/tmp` is written.

## Open Questions / Follow-ups

- **Byte-identity is environment-conditional.** The `authority` block pins `syside_version`, `sysml_codegen_version`, `agentic_mbse_version` and the standard-library digest into the file. Any of those moving will move the snapshot bytes and refuse gate 4. That is correct behavior — gate 1a is the gate that should catch a toolchain drift first — but the design should say plainly that gate 4's byte comparison also functions as a toolchain-lineage check, so a future reader does not read a refusal there as model drift.
- **One package only.** Measured on the stellarator MFE package. Whether the IFE packages recapture byte-identically is unmeasured and out of scope for B2.
- **Stale wording elsewhere.** Several older records describe the pre-v6 `captured_at` / `document_path` difference classes as standing facts (`work/completed/20260720_WI-027_demo-constraint-execution/plan.md:361`, `work/completed/20260720_WI-028_handshake-account-scope/plan.md:296`, `modeling_project/VALIDATION_MATRIX.md:61`). They were true when written. Not corrected here — this spike does not own those artifacts — but flagged so the next agent reading them does not re-inherit the premise the way B2 did.
