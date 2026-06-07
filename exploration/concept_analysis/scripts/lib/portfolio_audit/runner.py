"""Portfolio-audit runner — cheap deterministic prep, then the lead Opus agent.

The runner does *only* the work the lead shouldn't waste context on, and gets out
of the way:

1. Resolve the run folder (timestamped, collision-safe).
2. Build `manifest.json` (audited state) and `cohort_digest.json` (lead payload).
3. Render the lead prompt and write it to `prompts/lead_prompt.md`.
4. **All three forensic files are on disk before the lead is invoked** — a crash
   mid-lead leaves a complete state record (design Invariant: forensics first).
5. Invoke the single lead agent. Everything after that — investigators, writers,
   report.md, findings.jsonl — is the lead's own work via the Task tool. The
   runner does not parse the lead's output or coordinate any fan-out (Bet 1).
6. Verify the expected outputs exist and write `run.log`.

The runner makes exactly one Claude call (the lead). It never writes `report.md`
(Invariant 3) — it only checks one exists at exit.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

from lib.claude import invoke_claude
from lib.iteration import read_loop_state
from lib.paths import ANALYSES_DIR, CONCEPT_ANALYSIS_DIR, TEMPLATES_DIR
from lib.portfolio_audit.digest import build_digest
from lib.portfolio_audit.manifest import (
    build_manifest,
    last_complete_iteration,
    sha256_of,
)
from lib.templating import fill_template

REVIEWS_DIR = CONCEPT_ANALYSIS_DIR / "reviews"
LEAD_TEMPLATE = TEMPLATES_DIR / "portfolio_audit" / "lead.md"
CRITERIA_PATH = TEMPLATES_DIR / "config" / "portfolio_audit_criteria.md"

# Lead orchestration is long-running (it fans out investigators + writers).
DEFAULT_TIMEOUT_S = 7200

# Prepended to the lead prompt when resuming an unchanged cohort (--inherit-from).
RECOVERY_PREAMBLE = (
    "**Recovery:** You started this audit in a prior run and did not finish. The "
    "cohort and all concept artifacts are unchanged. The `report.md` and "
    "`concepts/*.md` files in this run folder contain your work so far. Read them. "
    "Pick up where you left off — continue investigating concepts you hadn't "
    "reached, refine findings if new context warrants, and update `report.md` "
    "(which you should continue to edit continuously per the durability rule). Do "
    "not re-investigate concepts that already have a satisfactory "
    "`concepts/<id>.md` unless new cross-cohort reasoning gives you a reason."
)


# ---------------------------------------------------------------------------
# Cohort resolution
# ---------------------------------------------------------------------------


def latest_verdict(concept_id: str) -> str | None:
    """Verdict of the concept's highest completed iteration, or None if none yet."""
    last = last_complete_iteration(read_loop_state(ANALYSES_DIR / concept_id))
    return last.verdict if last else None


def resolve_audit_cohort(records: list[dict], *, passed_only: bool = False) -> list[dict]:
    """The audit cohort: ``records`` as given, or only PASS-verdict ones (FR-3).

    Concept *selection* (numeric/full-id/name/--all/--family) is the caller's job
    via ``resolve_concepts``; this applies only the ``--passed-only`` filter.
    """
    if not passed_only:
        return list(records)
    return [r for r in records if latest_verdict(r["concept_id"]) == "PASS"]


# ---------------------------------------------------------------------------
# Run folder
# ---------------------------------------------------------------------------


def make_run_dir(now: datetime | None = None) -> Path:
    """Create and return a sortable timestamped run folder under ``reviews/``.

    Folder name is ``YYYYMMDD-HHMMSS`` (local). On collision, append ``-2``,
    ``-3``, … so two runs in the same second never clobber each other.
    """
    stamp = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
    candidate = REVIEWS_DIR / stamp
    suffix = 2
    while candidate.exists():
        candidate = REVIEWS_DIR / f"{stamp}-{suffix}"
        suffix += 1
    candidate.mkdir(parents=True)
    return candidate


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------


def run(
    records: list[dict],
    *,
    run_dir: Path,
    model: str = "opus",
    cli: str = "",
    timeout: int = DEFAULT_TIMEOUT_S,
    dry_run: bool = False,
    inherit_from: Path | None = None,
) -> Path:
    """Build forensics, then invoke the lead. Returns the run folder.

    Writes ``manifest.json``, ``cohort_digest.json``, and
    ``prompts/lead_prompt.md`` *before* any lead call. With ``dry_run`` the lead
    is not invoked (the forensic artifacts are still produced). Otherwise the lead
    runs to completion and the runner verifies its outputs and writes ``run.log``.

    ``inherit_from`` resumes a prior run *all-or-nothing*: the new cohort must be
    byte-identical to the prior (same concepts, same artifact SHAs, same staleness)
    or the run aborts naming what changed. On an exact match it copies the prior
    ``report.md`` / ``concepts/*.md`` / ``findings.jsonl`` forward and tells the
    lead to pick up where it left off.
    """
    concept_ids = [r["concept_id"] for r in records]
    (run_dir / "prompts").mkdir(parents=True, exist_ok=True)
    (run_dir / "concepts").mkdir(parents=True, exist_ok=True)

    run_meta = {
        "timestamp": run_dir.name,
        "cli": cli,
        "model": model,
        "criteria_sha": sha256_of(CRITERIA_PATH),
        "cohort": concept_ids,
    }
    manifest = build_manifest(concept_ids, run_meta)
    digest = build_digest(records, manifest)

    recovery_preamble = ""
    if inherit_from is not None:
        recovery_preamble = _apply_inheritance(manifest, inherit_from, run_dir)

    prompt = _render_lead_prompt(digest, run_dir, recovery_preamble=recovery_preamble)

    # --- forensics on disk BEFORE the lead call (crash leaves a full record) ---
    _write_json(run_dir / "manifest.json", manifest)
    _write_json(run_dir / "cohort_digest.json", digest)
    (run_dir / "prompts" / "lead_prompt.md").write_text(prompt, encoding="utf-8")

    if dry_run:
        print(f"  dry-run: forensics written to {run_dir}; lead not invoked")
        return run_dir

    start = time.time()
    result = invoke_claude(prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=timeout, model=model)
    elapsed = time.time() - start

    _verify_outputs(run_dir)
    _write_run_log(run_dir, result, elapsed=elapsed, model=model, concept_ids=concept_ids)
    return run_dir


def _render_lead_prompt(
    digest: dict, run_dir: Path, *, recovery_preamble: str = ""
) -> str:
    template = LEAD_TEMPLATE.read_text(encoding="utf-8")
    body = fill_template(
        template,
        {
            "cohort_digest": json.dumps(digest, indent=2, default=str),
            "run_dir": str(run_dir.resolve()),
            "concept_count": str(len(digest["concepts"])),
        },
    )
    if recovery_preamble:
        return f"{recovery_preamble}\n\n---\n\n{body}"
    return body


# ---------------------------------------------------------------------------
# All-or-nothing resume (--inherit-from)
# ---------------------------------------------------------------------------


def diff_manifests(new: dict, prior: dict) -> list[str]:
    """Reasons the new cohort state differs from the prior run (empty = identical).

    Identity = the audited *content*: the cohort set, plus each concept's three
    artifact SHAs and its ``model_stale`` flag. Run metadata, iteration counts,
    timestamps, and import_status are deliberately excluded — they don't change
    what was reviewed. One human-readable reason per mismatch.
    """
    new_c = new.get("concepts", {})
    prior_c = prior.get("concepts", {})
    new_ids, prior_ids = set(new_c), set(prior_c)

    reasons: list[str] = []
    for cid in sorted(new_ids - prior_ids):
        reasons.append(f"{cid}: in the new cohort but not the prior run")
    for cid in sorted(prior_ids - new_ids):
        reasons.append(f"{cid}: in the prior run but not the new cohort")
    for cid in sorted(new_ids & prior_ids):
        n, p = new_c[cid], prior_c[cid]
        if n.get("sha256") != p.get("sha256"):
            reasons.append(f"{cid}: artifact SHAs changed since the prior run")
        if n.get("model_stale") != p.get("model_stale"):
            reasons.append(
                f"{cid}: model_stale changed "
                f"({p.get('model_stale')} -> {n.get('model_stale')})"
            )
    return reasons


def _apply_inheritance(new_manifest: dict, prior_run_dir: Path, run_dir: Path) -> str:
    """Gate + copy-forward for --inherit-from. Returns the recovery preamble.

    Exits (non-zero) if the prior run has no manifest or the cohort changed at
    all — partial inheritance is impossible by design (Invariant 9). On an exact
    match, copies the prior report / per-concept docs / findings into ``run_dir``.
    """
    prior_manifest_path = prior_run_dir / "manifest.json"
    if not prior_manifest_path.exists():
        print(
            f"Error: --inherit-from {prior_run_dir} has no manifest.json — "
            f"not a portfolio-audit run folder.",
            file=sys.stderr,
        )
        sys.exit(1)

    prior_manifest = json.loads(prior_manifest_path.read_text(encoding="utf-8"))
    reasons = diff_manifests(new_manifest, prior_manifest)
    if reasons:
        print(
            "Error: cannot inherit — the cohort changed since the prior run:",
            file=sys.stderr,
        )
        for reason in reasons:
            print(f"  - {reason}", file=sys.stderr)
        print(
            "Inheritance is all-or-nothing; start a fresh run (omit --inherit-from).",
            file=sys.stderr,
        )
        sys.exit(1)

    _copy_forward(prior_run_dir, run_dir)
    return RECOVERY_PREAMBLE


def _copy_forward(prior_run_dir: Path, run_dir: Path) -> None:
    """Copy the prior run's durable work (report, per-concept docs, findings)."""
    for name in ("report.md", "findings.jsonl"):
        src = prior_run_dir / name
        if src.exists():
            shutil.copy2(src, run_dir / name)
    prior_concepts = prior_run_dir / "concepts"
    if prior_concepts.is_dir():
        for doc in prior_concepts.glob("*.md"):
            shutil.copy2(doc, run_dir / "concepts" / doc.name)


def _verify_outputs(run_dir: Path) -> None:
    """Check the lead produced a report. Warn (don't raise) if it didn't.

    The runner never writes report.md (Invariant 3); the lead's continuous
    writeback is the durability mechanism. A missing report means the lead failed
    very early — worth a loud warning, but the forensics are still on disk.
    """
    if not (run_dir / "report.md").exists():
        print(
            f"  WARNING: lead produced no report.md in {run_dir} — "
            f"it may have failed before writing one. Forensics are on disk.",
        )


def _write_run_log(
    run_dir: Path, result, *, elapsed: float, model: str, concept_ids: list[str]
) -> None:
    """Write run.log: lead returncode, wall time, and cost/usage when available.

    Cost/usage come from the lead result event (``InvokeResult.cost_usd`` etc.).
    They're lead-level totals — the event stream doesn't break cost out
    per-subagent, so we report what's reliably present rather than fabricate
    per-subagent rows. When the stream carried no cost, say so plainly.
    """
    cost = getattr(result, "cost_usd", None)
    usage = getattr(result, "usage", None)
    turns = getattr(result, "num_turns", None)

    lines = [
        f"portfolio-audit run {run_dir.name}",
        f"model: {model}",
        f"concepts ({len(concept_ids)}): {', '.join(concept_ids)}",
        f"lead returncode: {result.returncode}",
        f"lead wall time: {elapsed:.0f}s",
        f"lead cost: ${cost:.2f}" if cost is not None
        else "lead cost: unavailable (no total_cost_usd in event stream)",
    ]
    if usage:
        lines.append(f"lead usage: {json.dumps(usage, default=str)}")
    if turns is not None:
        lines.append(f"lead turns: {turns}")
    if result.returncode != 0:
        lines.append(f"lead stderr: {result.stderr[:500]}")
    (run_dir / "run.log").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
