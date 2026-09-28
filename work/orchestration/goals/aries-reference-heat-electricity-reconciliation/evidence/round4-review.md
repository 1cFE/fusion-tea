# Round 4 review — fresh reviewer

HEAD `21a76402`. Read the brief's files plus `raffray-p746.png` (p745 holds only Refs. 1–7). Nothing run.

**Verdict: FINDINGS** — none blocking; one owner question.

1. Owner direction — PASS. Prescribed route used (requests, runs, registry); round-4 commits touch only the goal directory, `knowledge/` and the requests. Hypothesis/inference wording holds in answer § 1, § 5, § 6, § 13, ledger rows 9/12/19, contract § 6a and L-010; exception § 12 (F1).
2. Qualifications — FINDING. No "no arrangement" remains; "arrangements checked" throughout; 891 MW carries both caveats in answer § 1, § 13, ledger rows 12/18; § 12 says "the plant makes about 891 MW net" bare (F2).
3. Citation correction — PASS. p745: Ref. 7 = Lyon, FST 54, 694; p746: Ref. 13 = Wang, Malang, Raffray, SOFE 2005; Ref. 15 = Schleicher, Raffray, Wong 2001. Applied in answer § 6, contract `[r4 correction]`, the q1 note; ledger has no stale Ref. 7.
4. Source-check application — PASS. Ref. 15 reading carries all five corrections (Ref. [4] attribution, Table III minus Tin, 737 − 30, Tout caveat, inference split), each `[sc]`; Malang § 3: "consistent with it, not supported by it, and remains an inference".
5. Bounded result — PASS. All four elements read the same in trail T-005 and result, answer § 1 and § 13, ledger row 19, contract second `[r4]`; completion "partially answered".
6. Scopes and limits — PASS. HX-01 8/8 searches, 1/3 captures, `limit_reached: max_searches`; HX-02 3/6, 1/2, none; one run each, no retries. The Malang hop goes one step past the owner's direction; recorded and bounded.
7. Learning delta — below.
8. Unsupported claims — F1, F2, F4.

## Findings

1. correct-before-use — answer § 12 treats the lumped heater as established ("which is how 708 °C appears there") and says the cited reference "is not in our files", false after round 4. Rewrite to the § 1 wording.
2. correct-before-use — answer § 12 presents 891 MW as what "the plant makes"; add the modeled-alternative and cost caveat.
3. correct-before-use, owner question — HX-01 `where_to_look` names `aries.ucsd.edu`; the registry's identity screen bars that term, so the researcher used the `qedfusion.org` mirror and Wayback snapshots of the barred site. Hold-out screen: no hit; neither paper is ARIES-CS 2008 material; the result stands. Whether the term bar is a hold-out safeguard a mirror must not bypass is the owner's call.
4. note — trail T-001 lists Ref. 15 "on p745 in the conclusions"; those markers sit in safety and radwaste sentences whose paper is Ref. 16 (Merrill); Raffray's p745 numbering is off by one, so they do not corroborate the cycle attribution.
5. note — stale or editorial: answer § 5 row 5 and L-010 say "being pursued"; § 6 omits the Malang hop; § 13 has a fragment ("comparison. whether"); ledger header still "round 3"; `SOURCE_INDEX.md` 1615 says "lumped block", the reading says boundary label.

## Learning rulings

- L-013 — accept, corrected: only Schleicher makes Tout dependent; Malang states both IHX terminals.
- L-014 — accept; add: check each marker's context (F4).
- L-015 — reject as written: a route around a screen of undetermined purpose (F3). Keep as the owner question.

## Not covered

Reading physics; p732/p735 markers; receipts beyond `return.json`; the opening commit's files; the "frozen records" claim; post-reveal authorization.

— fresh round-4 reviewer, 2026-09-25
