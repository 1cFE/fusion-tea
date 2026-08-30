# PROTOCOL Amendment Draft — clean-room split (APPLIED — kept as the approval record)

**Status 2026-08-30:** owner-approved, applied to `knowledge/holdout/aries-cs/PROTOCOL.md` (§8, §6-logged), guard + holdout tests verified. This file is the approval record; the canonical text is the PROTOCOL itself.

**Drafted:** 2026-08-30, per `.project/active/demo-depth-rubric/spec.md` success criterion 1.
**Applies to:** `knowledge/holdout/aries-cs/PROTOCOL.md`. Frontmatter untouched — status stays `sealed`.
**Parser safety:** the two `### Barred` headings and their path bullets in §3 are not modified; `scripts/holdout_guard.py` parses only those. Verified against `_section_after` / `_backticked_paths`.

Once approved, the three edits below are applied verbatim and the §6 log entry is added.

---

## Edit 1 — §2, append after the "Not blocked:" paragraph

> Also not blocked: yardstick sessions, per §8.

## Edit 2 — §3, append to the intro paragraph of "Barred by default, documented-exception path"

> Yardstick sessions are exempt from this default (§8); the exception path continues to govern model-facing sessions.

## Edit 3 — new section §8, appended after §7

> ## 8. Clean-room split (owner ruling, 2026-08-30)
>
> The clean room exists so the model is never built from ARIES-CS data. It binds the sessions that build the model, not the ones that build the yardstick.
>
> - **Yardstick sessions** — sessions producing the depth rubric, gradings against it, or the maturation phase's gap reports, and touching no model file — are exempt from §2 blocking and §3 admissibility, including the two barred-by-default costing sources (the Waganer ARIES cost-account doc explicitly). The four sealed PDFs in this directory are **not** covered by the exemption: they stay unread until the §6 reveal.
> - **Model-facing sessions** — anything building, refining, researching for, or reviewing the model — keep the full clean room exactly as §2/§3 state it.
> - **The firewall between the two is the yardstick's output:** rubrics and gradings carry depth prescriptions only — what to model and how deeply — never ARIES-CS-specific values or design facts. §4 binds every session as always.
> - **Source register:** any source ingested for yardstick work is barred for model-facing sessions until screened clean; screening verdicts are recorded as rows below this line. (None yet — no yardstick ingestion planned.)

## §6 log entry

> - 2026-08-30 — owner-approved amendment (clean-room split, §8): yardstick sessions exempted from §2/§3, sealed PDFs excluded, Waganer readable in yardstick sessions; model-facing sessions unchanged. Status remains `sealed`; no reveal. Ruling captured in `.project/concepts/stellarator-demo-maturation.md`.
