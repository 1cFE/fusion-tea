# WI-033 Verification Record — 2026-08-28

Branch `feat/wi033-p-pump-rebase` off `main` (0a3815d4). Commit chain (each verified `git merge-base --is-ancestor` over its predecessor by construction of the linear branch):

| Commit | SHA | Content |
|---|---|---|
| C-OPEN | 65780622 | spec/design/plan + SV-037 pending |
| C-FIX | 5f97a761 | registry raw.pdf fix + PDF-URL regression test |
| C-REG-CIS | 39bd3b41 | Cismondi registered |
| C-REG-MOS | 891b95bc | Moscato registered |
| C-MODEL | ffb22724 | p_pump 195.0 in both twins |
| C-TESTS | 18a5ce86 | MFE census fixture re-derived |
| C-FLIP | 9f0019e8 | runbook flip + goal.md amendment |

## Spec success criteria

1. **p_pump = 195.0 with the MR-WI033-2 doc comment, twins byte-identical, syntax clean.** ✔ `cmp` clean at C-MODEL; `agentic-mbse validate models/`: L1 0 errors / 0 warnings (22 files); L2 = the 12 pre-existing placeholder-binding WARNs in `generic_mfe/mfe_plant.sysml`, count and locations unchanged from the pre-edit baseline captured this session.
2. **Both sources registered, outcome `registered`, zero hand edits.** ✔ Receipts: `registry-cismondi.json` (slug `progress_in_eu_breeding_blanket_design_and_integration`, raw = source_id = `dd240e3c…`, byte-identical to the 2026-04 concept-research extraction of the same URL) and `registry-moscato.json` (slug `progress_in_the_design_development_of_eu_demo_helium_cooled`, raw = `75f2417a…`, byte-identical to the design-phase probe of both URL variants). `SOURCE_INDEX.md`/`MANIFEST.jsonl` edits are registry-authored within C-REG-* only.
3. **First-order re-derivation.** ✔ Cismondi registered `output.md:174`: "In case of helium the pumping power is ~150MW, one order of magnitude higher than in case of water (~15MW)", plus the 9 km → ~3 km lever in the same passage; `:172` HCPB-representative-for-HCLL. Moscato registered `output.md:81` (2101.7 MW, 2025.7 kg/s), `:89–:91` (9 loops: 3 IB + 6 OB), `:145`/`:154` (Table 3: 6.8 IB / 7.5 OB MW; 2 compressors per loop per Table 1) → 3×2×6.8 + 6×2×7.5 = **130.8 MW ≈ 131 MW (6.2 %)**. Near-term Table 4 body is absent from the text extract; re-derived from the registered `raw.pdf` p.7: **5.9 (STHE) / 5.2 (CWHE) MW** → 16 × 5.9 / 5.2 = **94.4 / 83.2 MW = the 83–94 MW (~4 %) band**. **DI-008 disposition: figures CONFIRM the recorded basis — no amendment** (confirmation is not an amendment; correction-over-accretion).
4. **Runbook flip per archived recipe; ancestry; integrate untouched; goal amendment.** ✔ Four edits only (`git show 9f0019e8`: GOAL_RUNBOOK.md 4+/4−); patch script asserted the `integrate` row and bullet byte-untouched (R-G1); `git merge-base --is-ancestor 891b95bc 9f0019e8` → true. `goal.md` § Amendments dated entry, operator's pen. Honest limit, recorded in the flip commit: the flip rests on the write door (`source_registry.py`) running live; `research_seam.py`'s request/return path has not run end-to-end — owed to a future real round, and to GSTH Item 6's epic evidence.
5. **tests/models green; no regen.** ✔ 48 passed / 13 skipped (SysIDE live generation included). Census fingerprint moved `1ca93d0c…` → `f08daa7b…`; fixture re-derived from a fresh canonical-subset generation with the D7 guard (by_entry_type name-identical: 173 = 45/10/118). Regen fence: `git diff main` shows zero lines under committed study/package dirs; every changed file is in the declared scope list. `tests/research` 150 passed (includes the new PDF-URL regression test).
6. **SV-037 passing.** ✔ `pm update-validation SV-037 --status passing` (this commit).

## Deviation (owner-ruled in-session)

- **C-FIX** (spec § Scope Amendment `[OWNER 2026-08-28]` "fix it"): `source_registry.py:485` hardcoded `raw.html` for URL captures; the extractor stores PDF URLs as `raw.pdf` (`agentic-mbse extract_cli.py:282`). First Cismondi attempt returned `capture_failed` (receipt `registry-cismondi-attempt1-capture_failed.json`); rollback held (registry files untouched, `verify` 0 faults, 3 pre-existing legacy). Fixed + loopback PDF-URL regression test; Item 2's URL-chain tests had fixtured HTML only.
- **Registry commit semantics** (design D2 corrected): the registry's "commits four things or none" is the filesystem transaction; git commits are the operator's.

## Owner-sequenced next steps (not this item's)

Push + PR (owner's call; `/_my_pre_pr` if this ships alone), `/audit-models`, then `pm close-item WI-033`. Package regeneration waits on the `integrate` seam (GSTH Item 6); until then the model (195.0) intentionally diverges from every committed package (1.0) and `scripts/integrate.py` refusing a stale package is the designed detection.
