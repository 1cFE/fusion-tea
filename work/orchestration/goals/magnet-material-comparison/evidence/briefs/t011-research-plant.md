# T-011 research briefs — plant-chain evidence (three requests, one worker each)

Common part: follow `evidence/briefs/t002-research-common.md` §§ Protocol, Write, Do not, Return exactly (same seam commands, same clean-room screen, same evidence-note shape). The context differs: Round 2 asks whether REBCO's higher-field or smaller-winding capability improves a whole stellarator plant enough, in LCOE, to offset its dearer magnet. The plant model (`exploration/stellarator_e2e`, Stellaris configuration) computes peak field as `B_axis × peak_ratio × bore factor` with the winding-pack term of Lion 2021 eq. 39 omitted because its coefficient is unprinted, and its plasma scaling (ISS04 with a renormalization factor) declares no validity band away from the Stellaris point (9.0 T on axis, 24.9 T peak). Nb₃Sn supports at most about 12 T peak, which on this coil set means 4.3–4.7 T on axis. Read `evidence/plant-chain-audit.md` § 3 rows D1, D3, D8 and § 8 items 1 and 3 before searching. Registered sources you must check first: `knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/`, `knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/`, the Stellaris design paper (grep `SOURCE_INDEX.md` for "Stellaris Design Paper"), `the_helias_reactor_beidler_et_al_iaea_cn_77_ftp1_16/`. Inspect page images for every equation and table you rely on; `output.md` renders equations as image links.

## Worker A — `REQ-MMC-FIELD-01` → `evidence/sources/field-term.md`

Question in the request file. What the note must settle:

1. The exact printed form of Lion 2021 eq. 39 (render the page image; `output.md:448-455` shows only image links) with every symbol defined, and whether a0, a1 are printed anywhere for any coil set (Table 1 of the DEMO benchmark, the 2023 thesis, the Stellaris paper). If Table 1 prints winding-pack dimensions and B_max for the DEMO benchmark alongside the tokamak-PROCESS values, record every number: it may be a second anchor.
2. The explicit cuboid-beam field formula of appendix A: transcribe it fully with its geometry conventions, so a later task can judge whether computing a1 for a registered coil geometry (Proxima simplified CAD, `knowledge/sources/proxima_fusion_public_simplified_stellarator_cad_models/`) is a bounded calculation or a new solver.
3. Any sourced self-field or pack-size dependence of the peak field for a rectangular winding pack: tokamak PROCESS's TF peak-field treatment (Kovari 2014 or the PROCESS documentation; open access), HELIAS 5-B magnet paper (Schauer 2013) if it prints B_max against winding-pack dimensions, or a textbook straight-conductor self-field bound. State the form, its assumptions and its domain.
4. What the Stellaris paper itself prints about winding-pack dimensions, coil current, B_max and B_axis (a single anchor is already in the model; note any second design variant or scan in that paper).

Classify each finding as the common brief requires. The gap statement must say plainly whether the pack term can be fixed from evidence, computed from registered geometry, bounded, or is unavailable.

## Worker B — `REQ-MMC-PLASMA-01` → `evidence/sources/plasma-validity.md`

Question in the request file. What the note must settle:

1. ISS04's fitted database ranges (field, density, size, beta, iota, heating) from Yamada 2005 or Dinklage 2007: the numbers, with page/table.
2. What the renormalization factor `f_ren` (the model holds it at the Stellaris value) is defined as and how the Stellaris paper and Lion 2021/2023 justify its reactor value; whether any source states a validity band for extrapolation in field.
3. What beta limit the Stellaris paper and the PROCESS stellarator papers use and whether it is field-dependent; whether any source discusses a lower-field (4–6 T) HELIAS-class operating point and its confinement/beta assumptions (Warmer 2016 HELIAS 5-B at 5.9 T is a likely case).
4. State plainly: on the evidence, is a 4.3–4.7 T on-axis operating point of this configuration a supported extrapolation of ISS04 with the same `f_ren`, an unsupported one, or undeclared; and what would make it supported.

## Worker C — `REQ-MMC-NB3SN-PLANT-01` → `evidence/sources/nb3sn-stellarator.md`

Question in the request file. What the note must settle:

1. For each Nb₃Sn/NbTi stellarator reactor design found (HELIAS 5-B is the primary target; HELIAS 4/5, HSR5/22, HSR4/18 secondary): axis field, maximum field on the coil (and thus the peak/axis ratio), coil count, R, a, winding-pack dimensions and cross-section, coil current or ampere-turns, conductor type and operating temperature, fusion power, net electric power, with page/table/figure for each. Compare with the Stellaris anchor (48 coils, R 12.7 m, 9.0 T axis, 24.9 T peak, ratio 2.7667).
2. Whether any of these sources prints the peak field's dependence on winding-pack size or current density for its coil set.
3. What each source says limited the field (conductor, stress, or configuration) and whether the design point was self-consistent (plasma, confinement, beta) at that field.
4. State plainly whether a sourced Nb₃Sn stellarator design point exists that could serve as a second coil-set anchor for a peak/axis ratio, and what facts the plant model would have to re-anchor to use it (list them against `evidence/plant-chain-audit.md` § 2 held constants).

Budget per worker: about 50 tool calls. Return at most 400 words as the common brief says.
