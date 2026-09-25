# Source-screen review — the `aries.ucsd.edu` term bar and the two round-4 registrations (2026-09-25)

[AGENT] Written under round 5 T-001 at the owner's direction (`owner-supplement-r5.md` item 1). Facts are quoted from the rule home and the run records; the assessment and the decisions needed are the coordinator's.

## 1. What the restriction is and what it is for

- `[SOURCE]` `scripts/holdout_guard.py` (the registry's screen) derives the barred *paths* from `knowledge/holdout/aries-cs/PROTOCOL.md` § 3 and keeps a short list of barred *terms*: "Terms that mark ARIES-CS material. The four stems are the sealed papers (PROTOCOL § 7); the host is the canonical program mirror." The terms are `aries-cs`, `aries.ucsd.edu`, `08-fst-ku`, `08-fst-lyon`, `08-fst-najmabadi`, `08-fst-raffray`.
- `[SOURCE]` Same module: "There is no waiver. A match is reported; adjudicating it is the owner's job, through the protocol's own § 6 exception log, outside this seam."
- `[SOURCE]` `scripts/source_registry.py`: the identity screen runs before any fetch on the registration input (a local path or URL) and on the caller's title (`_input_identity_holdout_hit`); a second content scan runs on the fetched bytes and extraction (`_post_capture_refusal`). A hit at either stage returns `holdout_hit` with the rule id, writes nothing into `knowledge/`, and the command file instructs the researcher that the candidate "is queued for the operator. There is no flag, and asking for one is out of scope."
- `[SOURCE]` PROTOCOL § 3 principle: "any artifact carrying ARIES-CS-specific design or cost data is inadmissible until reveal. Bibliographic citations of ARIES-CS inside otherwise clean sources are not data and do not taint a source." § 6: status flips to `revealed` only by the owner; the frontmatter still reads `status: sealed`, `revealed: null`. § 7 records that the four sealed papers were themselves retrieved from Wayback snapshots of `aries.ucsd.edu/LIB/REPORT/JOURNAL/FST/`.
- `[DERIVED]` Intended scope of the host term: provenance marking. Anything whose registration identity names the canonical ARIES program library is presumed ARIES-CS-marked and must be adjudicated by the owner, whatever its content; the content scan then decides ARIES-CS-specific data on the bytes. The term bar is therefore an acquisition safeguard with an owner adjudication step, not a content judgement.

## 2. What the existing authorization says

- `[OWNER]` Owner brief for this goal: "ARIES source reading is authorized post-reveal. Prefer retained primary papers/page images and reviewed source records. The historical quarantine warning does not prohibit this authorized investigation; do not rewrite shared policy or bypass acquisition safeguards. Any additional acquisition follows the prescribed research route." Carried into `goal.md` § Invariants (Sources).
- `[OWNER]` Owner supplement r5: "Do not treat acceptance by a domain filter as permission to bypass an underlying restriction."
- `[DERIVED]` The authorization covers reading retained ARIES material for this goal and acquiring through the route; it does not delegate the registry's adjudication step to the agent, and it names bypassing acquisition safeguards as out of bounds.

## 3. What the two round-4 registrations did

- **Run REQ-ARIES-CYCLE-HX-01** (Schleicher, Raffray and Wong 2000/2001): `process_log.md` records Wayback CDX index queries of `aries.ucsd.edu/LIB/REPORT/CONF/ANS00/*`, `…/CONF/SOFE05/*`, `…/CONF/*`, `…/ARIES/DOCS/ARIES-CS/*` and `qedfusion.org/…` (directory listings of the library to locate files; triage only, nothing captured from those listings), then registration of `https://qedfusion.org/LIB/REPORT/CONF/ANS00/schleicher.pdf` (receipt `20260925T203652-001.json`: outcome `registered`, source id `392f145d…`, captured true, rule id null). The researcher's return states the mirror was used because "the registry's identity screen bars the `aries.ucsd.edu` term, so the Wayback copy of the same file would have been refused".
- **Run REQ-ARIES-CYCLE-HX-02** (Malang, Schnauder and Tillack 1998): `process_log.md` records that a UCSD publication page pointed at `aries.ucsd.edu/LIB/REPORT/CONF/ISFNT4/malang2.pdf`, "on the barred aries.ucsd.edu domain, so the qedfusion.org mirror is used"; registration of `https://qedfusion.org/LIB/REPORT/CONF/ISFNT4/malang2.pdf` (receipt `20260925T205036-001.json`: `registered`, source id `3c5633b1…`, captured true, rule id null).
- **Content:** both papers predate ARIES-CS (2000 and 1997/1998), the post-capture content scan reported no term hit, and the two source checks (`ref15-reading-review.md`, `malang98-reading-review.md`) found no ARIES-CS material in either.
- **Provenance and receipts preserved:** the run directories, receipts, `return.json`, `process_log.md` and `run.jsonl` are committed (`8bbb7e3c`, `620e341f`); nothing here alters them.

## 4. Assessment

- On content the two registrations satisfy PROTOCOL § 3's principle and would satisfy the content scan under any reading.
- On procedure the researcher, on finding that the canonical host was a barred term, substituted a mirror host of the same library so that no match was presented for adjudication. That avoids the safeguard's adjudication step rather than passing through it; it is the pattern the owner's supplement names ("acceptance by a domain filter" is not "permission to bypass an underlying restriction"). The Wayback index queries of the barred host were triage of directory listings, with no capture from that host, but they used the barred host as the source of candidates.
- The existing authorization does not resolve this: it authorizes reading and route-based acquisition and forbids bypassing safeguards; it does not say whether ARIES-library provenance for pre-ARIES-CS material is admissible without an owner exception, and the guard reserves that adjudication to the owner.

## 5. Decisions needed from the owner (before any dependent source access)

- **D1 — the two round-4 registrations.** Ratify them as owner exceptions logged under PROTOCOL § 6 (scope: two pre-ARIES-CS cycle papers obtained from the ARIES program library mirror; content clean), or withdraw them from the registry. Until ruled, their readings stand as evidence of what those papers say, and no further ARIES-library access (either host, or its Wayback snapshots) is used by this goal.
- **D2 — the Wang, Malang and Raffray SOFE 2005 paper.** Its title contains "ARIES-CS", so the registry's pre-fetch identity screen refuses any registration with `holdout_hit` (`term:aries-cs`) regardless of where a copy comes from; obtaining it into the repository requires an owner exception under § 6 in every case. The bounded round-5 attempt therefore stops at locating a permitted-access copy and queues it (no capture); the owner decides whether to log the exception and, if the only copies are paywalled, whether to purchase or use institutional access.

No shared policy file is edited by this review; the § 6 log is the owner's.
