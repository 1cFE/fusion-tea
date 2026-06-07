# Per-Account Override Walkthrough

This is the discipline for discovering override candidates. It is **not**
open-ended. You do not ask "what overrides does this concept need?" — you walk
the canonical account schema you were given, one account at a time, and for each
one ask the same question of the dossier.

## The walkthrough

For **each** account in the canonical schema (the table injected above), ask:

> Does the dossier name a **company-grounded quantity, unit cost, or published
> dollar figure** that lets me price *this account* better than the 1costingFE
> library default?

Then decide:

- **No company data for this account** → propose **no** override. The library
  default stands. This is the common case; most accounts are not overridden.
  Do not invent a value and do not re-state the default.
- **Yes, the dossier grounds this account** → write a six-field Override
  Candidate entry:
  - **Identify the account's cost class first (S / U / P)** using the
    override-semantics class table embedded above. The class is part of the yes/no
    decision: it tells you why the library's 1 GWe fleet cost is what it is and
    dictates the **authoring shape** — a per-module M$ value anchored to
    `generic.cas22_detail["C2201xx"]` for a Class-U reactor-island sub-account, or
    a whole-plant M$ value anchored to `generic.costs.<rollup>` for a top-level
    Class-S or Class-P account. Whichever class, the headline lands on `M ×` the
    library's fleet cost for that account, and the `rationale` is written against
    the modular-fleet baseline — never a "conventional 1 GWe plant."
  - `account` — the canonical code from the schema (never an invented code).
  - `value` — a plain number, a self-documenting constant expression (e.g.
    `260.0 * 1.34` for a CPI-adjusted published cost), or — for a *relative*
    override defined as a fraction of the library's own computation — an
    expression over the library's bare overrides-off cost, written as
    `0.70 * generic.costs.cas21`. (In `model_setup.py`, `generic` is the
    mandatory `generic_reference(model, spec, P_native)` line placed before the
    overrides list; the model-setup prompt has the mechanics.) A relative
    `value` MUST reference `generic`, never `native` or the 1 GWe projection.
  - `enabled` — `true` if this departure should be active in the baseline run.
  - `provenance` — `direct` (company published the exact figure, or a published
    quantity × a published unit price) or `derived` (you assembled it from a
    published quantity plus an analyst-sourced unit price). When `derived`, the
    arithmetic — including any CPI factor — MUST appear in `rationale`.
  - `source` — `filename.md §Section` pointing at the company-grounded evidence.
  - `rationale` — why the library default misrepresents this design point, and
    the derivation chain for the value.

## Why per-account, not ad-hoc

Open-ended override discovery under-proposes: it finds the one or two obvious
departures and silently skips the rest. Walking every canonical account forces a
deliberate yes/no on each, so a legitimate override is never missed and an
un-evidenced one is never invented. "I considered this account and the dossier
gives no company figure for it" is a complete, correct answer for most accounts.

## Count sanity-check

After the walkthrough, compare your count of `enabled` overrides against the
expected band for this concept's archetype-fit grade (given to you as the
override-count rubric). If your count falls outside the band, do not pad or prune
to hit it — instead add one line noting the discrepancy and why your evidence
genuinely supports the count you have. The band is a smell-check, not a quota.
