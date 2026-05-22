"""Layer 2 of the eta_th-double-count fix: LLM-driven semantic audit.

Reads each concept's `model_setup.py` and asks Claude (Sonnet by default) to
report what it found — values, surrounding narrative, DEVIATION annotations,
scenario-sweep blocks — as structured JSON. Then compares each report against
`lib.canonical_params._CANONICAL_EFFICIENCIES` deterministically and emits a
drift report.

Catches what the regex layer (`standardize_eta_th.py`) cannot:
  * Value-vs-narrative contradictions ('eta_th=0.55' next to a
    "MARS Rankine ~36%" sourcing block).
  * Missing kwargs implied by Energy Capture (Hybrid without eta_de).
  * DEVIATIONs that lack a source citation.
  * Scenario-sweep flattening — an "Optimistic" scenario whose
    eta_th now equals the "Conservative" scenario, likely because the
    standardizer ate it.

Read-only by design. Outputs:
    verify_output/drift_report.json   # machine-readable, schema-conformant
    verify_output/summary.md          # human-readable, severity-grouped

Usage:
    uv run python exploration/concept_analysis/scripts/verify_canonical_params.py
    uv run python exploration/concept_analysis/scripts/verify_canonical_params.py --only 11 23 39
    uv run python exploration/concept_analysis/scripts/verify_canonical_params.py --model haiku --cost-cap 2.0
    uv run python exploration/concept_analysis/scripts/verify_canonical_params.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.canonical_params import canonical_eta_de, canonical_eta_th  # noqa: E402
from lib.claude import invoke_claude  # noqa: E402

ROOT = SCRIPT_DIR.parent
TABLE_PATH = ROOT / "table.csv"
ANALYSES_DIR = ROOT / "analyses"
OUT_DIR = SCRIPT_DIR / "verify_output"
SCHEMA_PATH = OUT_DIR / "schema.json"

PROMPT_VERSION = "1.0.0"

# Default invoke_fn is the real Claude CLI; tests pass a mock.
_DEFAULT_TIMEOUT_SEC = 600


# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

_PROMPT_TEMPLATE = """\
You are auditing a fusion concept's `model_setup.py` file for consistency with
the project's canonical (eta_th, eta_de) policy. costingfe's physics layer
distinguishes two efficiency channels and adds them:

    p_the = eta_th * p_th                    # thermal-cycle heat load
    p_dee = f_dec * eta_de * p_transport     # DEC end-loss channel
    p_et  = p_the + p_dee                    # total useful electric power

The canonical per Energy Capture category is therefore a (eta_th, eta_de) pair,
not a single overall-plant efficiency. Conflating them (the pre-2026-05 bug)
double-counts the DEC contribution.

CONCEPT
  concept_id:        {concept_id}
  energy_capture:    {energy_capture}
  canonical_eta_th:  {canonical_eta_th}     # thermal-cycle only
  canonical_eta_de:  {canonical_eta_de}     # DEC channel only

YOUR TASK
Read the model_setup.py file below and emit a JSON object conforming to the
schema fields described next. Return JSON only — no prose, no markdown
fences, no preamble. Pure JSON in your reply.

DISTINGUISH CANONICAL KWARGS FROM SCENARIO SWEEPS
- A CANONICAL kwarg is the eta_th / eta_de value passed to the file's primary
  `model.forward(...)` call (or its module-level constant `ETA_TH = ...` /
  `eta_th: float = ...` if that constant feeds the canonical call). These
  are the values the cost engine actually uses; they SHOULD match canonical
  unless a `# DEVIATION:` annotation is present.
- A SCENARIO SWEEP value is an eta_th / eta_de sitting inside a dict literal,
  list, or loop whose surrounding context names it as "Conservative",
  "Optimistic", "Pessimistic", "Baseline", a sensitivity sweep, or similar.
  Sweep values are EXPECTED to differ from canonical. Do NOT report them in
  `observed_eta_th` / `observed_eta_de` and do NOT count them as drift.
  Report them only in `scenario_sweep_findings`, and only when something looks
  off — e.g., an "Optimistic" value equal to the "Conservative" value
  (likely the standardizer flattened the sweep), or a `# standardized from
  <X>` annotation inside a sweep block (the standardizer should not have
  touched that line).

SCHEMA FIELDS (all required)
  concept_id:                "{concept_id}"
  energy_capture:            "{energy_capture}"
  canonical_eta_th:          {canonical_eta_th}
  canonical_eta_de:          {canonical_eta_de}
  observed_eta_th:           array (or null if no canonical eta_th line exists).
                             Each item: {{line:int, value:float,
                             context:"thermal-cycle"|"overall-plant"|"DEC"
                                     |"blended"|"other"|"unclear"}}
                             where context is what the surrounding comments
                             describe the value as.
  observed_eta_de:           array (or null). Each item: {{line:int,
                             value:float, context:"DEC"|"EM-recovery"
                                     |"alpha-channeling"|"other"|"unclear"}}
  deviations:                array of `# DEVIATION:` annotations Claude
                             found on eta_th / eta_de lines. Each:
                             {{axis:"eta_th"|"eta_de", line:int,
                             value:float, has_source_citation:bool,
                             rationale_summary:string (optional)}}.
                             has_source_citation = true iff the DEVIATION
                             comment carries a Source: or §reference pointer.
  narrative_contradictions:  cases where a kwarg VALUE contradicts its OWN
                             surrounding sourcing/narrative — not vs canonical.
                             Example: eta_th=0.55 next to a "MARS 1983 steam
                             Rankine ~36%" comment block. Each:
                             {{axis, line, observed_value, narrative_value_or_description,
                             severity:"high"|"medium"|"low"}}.
  missing_kwargs:            kwargs implied by Energy Capture but absent.
                             Each: {{axis:"eta_th"|"eta_de", reasoning:string}}.
                             For Direct (charged particle): eta_de MUST be
                             present, eta_th absent is fine if costingfe's
                             pulsed_conversion=INDUCTIVE_DEC auto-zero applies.
                             For Direct (inductive): same logic.
                             For Hybrid: BOTH should be present.
                             For Thermal: eta_th must be present, eta_de may
                             be absent (DEC channel inert when f_dec=0).
  scenario_sweep_findings:   per the rule above — sweep-block irregularities.
                             Each: {{axis, line, value, scenario_label,
                             concern:string}}.
  confidence_notes:          array of free-text strings — anything unusual
                             you noticed, ambiguous Energy Capture mappings,
                             custom physics implementations that don't use
                             costingfe.forward(), etc.
  prompt_version:            "{prompt_version}"

FILE CONTENTS BELOW (concept {concept_id}, {n_lines} lines):

```python
{file_text}
```

Return JSON only.
"""


# ---------------------------------------------------------------------------
# Library helpers
# ---------------------------------------------------------------------------


def load_concept_energy_capture() -> dict[str, str]:
    out: dict[str, str] = {}
    with open(TABLE_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid = row["ID"].strip()
            ec = row.get("Energy Capture", "").strip()
            if cid and ec:
                out[cid] = ec
    return out


def build_prompt(
    *,
    file_text: str,
    energy_capture: str,
    canonical_eta_th: float | None,
    canonical_eta_de: float | None,
    concept_id: str,
) -> str:
    return _PROMPT_TEMPLATE.format(
        concept_id=concept_id,
        energy_capture=energy_capture,
        canonical_eta_th=("null" if canonical_eta_th is None else canonical_eta_th),
        canonical_eta_de=("null" if canonical_eta_de is None else canonical_eta_de),
        prompt_version=PROMPT_VERSION,
        n_lines=file_text.count("\n") + 1,
        file_text=file_text,
    )


def _extract_json_from_llm_text(text: str) -> dict[str, Any]:
    """Pull the JSON object out of Claude's reply.

    Claude returns the result field as a string. That string SHOULD be pure
    JSON per the prompt, but defensively strip code fences and find the first
    balanced object.
    """
    s = text.strip()
    # Strip ```json fences if present.
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*", "", s)
        s = re.sub(r"\s*```\s*$", "", s)
    # Find the first { and last } and try that span.
    first = s.find("{")
    last = s.rfind("}")
    if first == -1 or last == -1 or last <= first:
        raise ValueError("no JSON object found in LLM reply")
    return json.loads(s[first:last + 1])


def _parse_claude_payload(stdout: str) -> str:
    """Extract the LLM reply text from invoke_claude's result.

    `lib.claude.invoke_claude` already runs `_parse_json_events()` and stores
    the parsed result string in `InvokeResult.stdout`, so this function is
    normally a no-op. We keep it as a hook for tests that pass a raw JSON
    event stream (matching the fake-LLM shape used in test fixtures).
    """
    s = (stdout or "").strip()
    # If stdout looks like a list of events (test mocks construct this shape),
    # pull the result field. Otherwise treat it as the already-extracted text.
    if s.startswith("["):
        events = json.loads(s)
        for ev in events:
            if isinstance(ev, dict) and ev.get("type") == "result":
                r = ev.get("result")
                if isinstance(r, str):
                    return r
        raise ValueError("no type=result event in stdout list")
    return s


def _make_null_canonical_report(
    *, concept_id: str, energy_capture: str, reason: str,
) -> dict[str, Any]:
    """Emit a schema-conformant report when canonical lookup is impossible."""
    return {
        "concept_id": concept_id,
        "energy_capture": energy_capture,
        "canonical_eta_th": None,
        "canonical_eta_de": None,
        "observed_eta_th": None,
        "observed_eta_de": None,
        "deviations": [],
        "narrative_contradictions": [],
        "missing_kwargs": [],
        "scenario_sweep_findings": [],
        "confidence_notes": [reason],
        "prompt_version": PROMPT_VERSION,
    }


def verify_file(
    model_path: Path,
    *,
    energy_capture: str,
    concept_id: str,
    invoke_fn: Callable[..., Any] = invoke_claude,
    model: str | None = "sonnet",
    timeout: int = _DEFAULT_TIMEOUT_SEC,
) -> dict[str, Any]:
    """Run the verifier on one model_setup.py and return a parsed report."""
    # Canonical lookup; on failure, emit a null-canonical report and skip the LLM.
    try:
        eth_can: float | None = canonical_eta_th(energy_capture)
        ede_can: float | None = canonical_eta_de(energy_capture)
    except ValueError as e:
        return _make_null_canonical_report(
            concept_id=concept_id,
            energy_capture=energy_capture,
            reason=f"Unrecognized Energy Capture key for canonical lookup ({e}); "
                   f"skipped LLM call to save cost.",
        )

    file_text = model_path.read_text(encoding="utf-8")
    prompt = build_prompt(
        file_text=file_text,
        energy_capture=energy_capture,
        canonical_eta_th=eth_can,
        canonical_eta_de=ede_can,
        concept_id=concept_id,
    )

    res = invoke_fn(prompt, model_path.parent, timeout=timeout, model=model)
    if getattr(res, "returncode", 0) != 0:
        return _make_null_canonical_report(
            concept_id=concept_id,
            energy_capture=energy_capture,
            reason=f"Claude CLI failed (rc={res.returncode}); "
                   f"{(res.stderr or '')[:200]}",
        )

    payload = _parse_claude_payload(res.stdout)
    report = _extract_json_from_llm_text(payload)

    # Make sure required identity fields match what we expected, in case the
    # LLM hallucinated. Override unconditionally; trust the script's
    # bookkeeping over the LLM's.
    report["concept_id"] = concept_id
    report["energy_capture"] = energy_capture
    report["canonical_eta_th"] = eth_can
    report["canonical_eta_de"] = ede_can
    report["prompt_version"] = PROMPT_VERSION

    # Defensive: ensure all required arrays exist (LLM sometimes omits empty ones).
    for k in ("deviations", "narrative_contradictions", "missing_kwargs",
              "scenario_sweep_findings", "confidence_notes"):
        report.setdefault(k, [])
    for k in ("observed_eta_th", "observed_eta_de"):
        report.setdefault(k, None)

    return report


# ---------------------------------------------------------------------------
# Comparator — derives drift/clean from a parsed report
# ---------------------------------------------------------------------------


def compare_to_canonical(report: dict[str, Any]) -> dict[str, Any]:
    """Compare an LLM report against canonical_params and emit a verdict.

    Status taxonomy:
      - "clean":               no concerns
      - "drift":               at least one canonical-vs-observed concern
      - "scenario_sweep_concern":  no canonical drift, but sweep flagged
      - "unknown_canonical":   energy_capture not in canonical map
    """
    flags: list[str] = []

    if report.get("canonical_eta_th") is None or report.get("canonical_eta_de") is None:
        return {"status": "unknown_canonical", "flags": list(report.get("confidence_notes", []))}

    eth_can = report["canonical_eta_th"]
    ede_can = report["canonical_eta_de"]
    deviating_lines = {
        ("eta_th", d["line"]) for d in report.get("deviations", []) if d.get("axis") == "eta_th"
    } | {
        ("eta_de", d["line"]) for d in report.get("deviations", []) if d.get("axis") == "eta_de"
    }

    # Canonical-vs-observed comparison — skip lines marked DEVIATION.
    for entry in report.get("observed_eta_th") or []:
        if ("eta_th", entry["line"]) in deviating_lines:
            continue
        if abs(entry["value"] - eth_can) > 1e-6:
            flags.append(
                f"eta_th drift L{entry['line']}: {entry['value']} vs canonical {eth_can}"
            )
    for entry in report.get("observed_eta_de") or []:
        if ("eta_de", entry["line"]) in deviating_lines:
            continue
        if abs(entry["value"] - ede_can) > 1e-6:
            flags.append(
                f"eta_de drift L{entry['line']}: {entry['value']} vs canonical {ede_can}"
            )

    # Narrative contradictions are drift regardless of DEVIATION protection —
    # they signal that the sourcing block disagrees with the value, which is
    # a documentation bug even if the value itself is policy-justified.
    for nc in report.get("narrative_contradictions", []):
        flags.append(
            f"narrative contradiction L{nc['line']} ({nc['axis']}, {nc.get('severity', '?')}): "
            f"{nc['observed_value']} vs '{nc['narrative_value_or_description']}'"
        )

    # Unsourced DEVIATIONs are drift.
    for d in report.get("deviations", []):
        if not d.get("has_source_citation", False):
            flags.append(
                f"unsourced DEVIATION L{d['line']} ({d['axis']}): "
                f"value {d['value']} lacks Source/§ citation"
            )

    # Missing kwargs implied by Energy Capture.
    for mk in report.get("missing_kwargs", []):
        flags.append(f"missing {mk['axis']} kwarg: {mk['reasoning']}")

    if flags:
        return {"status": "drift", "flags": flags}

    sweep_flags: list[str] = []
    for ssf in report.get("scenario_sweep_findings", []):
        sweep_flags.append(
            f"sweep concern L{ssf['line']} ({ssf['axis']}, "
            f"scenario={ssf['scenario_label']}): {ssf['concern']}"
        )
    if sweep_flags:
        return {"status": "scenario_sweep_concern", "flags": sweep_flags}

    return {"status": "clean", "flags": []}


def summarize_drift(reports: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate verdicts into a printable summary."""
    counts = {"clean": 0, "drift": 0, "scenario_sweep_concern": 0, "unknown_canonical": 0}
    per_concept: list[dict[str, Any]] = []
    for r in reports:
        v = compare_to_canonical(r)
        counts[v["status"]] += 1
        per_concept.append({
            "concept_id": r.get("concept_id", "?"),
            "energy_capture": r.get("energy_capture", "?"),
            "status": v["status"],
            "flags": v["flags"],
        })
    return {"counts": counts, "per_concept": per_concept}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _matches_only(cid: str, only: list[str]) -> bool:
    return any(cid.startswith(f"{x}-") or cid.startswith(f"0{x}-") for x in only)


def _render_summary_md(summary: dict[str, Any], elapsed: float) -> str:
    lines = ["# Canonical efficiency drift report", ""]
    c = summary["counts"]
    lines.append(f"- **clean**: {c['clean']}")
    lines.append(f"- **drift**: {c['drift']}")
    lines.append(f"- **scenario_sweep_concern**: {c['scenario_sweep_concern']}")
    lines.append(f"- **unknown_canonical**: {c['unknown_canonical']}")
    lines.append(f"- elapsed: {elapsed:.1f}s")
    lines.append("")
    for status in ("drift", "scenario_sweep_concern", "unknown_canonical", "clean"):
        rows = [pc for pc in summary["per_concept"] if pc["status"] == status]
        if not rows:
            continue
        lines.append(f"## {status}")
        for r in rows:
            lines.append(f"- **{r['concept_id']}** ({r['energy_capture']})")
            for f in r["flags"]:
                lines.append(f"  - {f}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--only", nargs="*", default=None,
                   help="Restrict to concept ID prefixes (e.g. 11 23 39).")
    p.add_argument("--model", default="sonnet", choices=("sonnet", "haiku", "opus"),
                   help="Claude model (default: sonnet).")
    p.add_argument("--dry-run", action="store_true",
                   help="Build prompts and exit; do not call the LLM.")
    p.add_argument("--cost-cap", type=float, default=None,
                   help="Abort if estimated cost exceeds this (USD; sonnet pricing).")
    p.add_argument("--timeout", type=int, default=_DEFAULT_TIMEOUT_SEC,
                   help="Per-file LLM timeout (seconds).")
    p.add_argument("--parallel", type=int, default=4,
                   help="Number of concurrent LLM calls (default: 4). Each "
                        "concept is one subprocess; the bottleneck is the "
                        "remote Sonnet call, not local CPU.")
    args = p.parse_args()

    energy_captures = load_concept_energy_capture()
    cids = sorted(energy_captures)
    if args.only:
        cids = [c for c in cids if _matches_only(c, args.only)]

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Cost estimate (rough; assumes ~6k input + ~1k output per call on Sonnet).
    sonnet_in, sonnet_out = 3.0 / 1_000_000, 15.0 / 1_000_000  # USD per token
    est_per_call = 6_000 * sonnet_in + 1_000 * sonnet_out
    est_total = est_per_call * len(cids)
    print(f"Verifying {len(cids)} concept(s). Estimated cost: ${est_total:.2f} "
          f"(model={args.model}; ~$0.02/call).")
    if args.cost_cap is not None and est_total > args.cost_cap:
        print(f"Estimated cost ${est_total:.2f} exceeds --cost-cap ${args.cost_cap:.2f}. Aborting.")
        sys.exit(2)

    if args.dry_run:
        print("--dry-run: building prompts only, no LLM calls.")
        for cid in cids:
            ec = energy_captures[cid]
            mp = ANALYSES_DIR / cid / "model_setup.py"
            if not mp.exists():
                print(f"  {cid}: no model_setup.py")
                continue
            try:
                eth_can: float | None = canonical_eta_th(ec)
                ede_can: float | None = canonical_eta_de(ec)
            except ValueError:
                eth_can = ede_can = None
            prompt = build_prompt(
                file_text=mp.read_text(encoding="utf-8"),
                energy_capture=ec,
                canonical_eta_th=eth_can,
                canonical_eta_de=ede_can,
                concept_id=cid,
            )
            print(f"  {cid}: prompt {len(prompt)} chars, canonical=({eth_can}, {ede_can})")
        return

    # Each verify_file call is dominated by a remote LLM round-trip, so we
    # parallelize via threads. The cost is the same; the wall-clock divides
    # by `--parallel`.
    targets: list[tuple[str, str, Path]] = []
    for cid in cids:
        ec = energy_captures[cid]
        mp = ANALYSES_DIR / cid / "model_setup.py"
        if not mp.exists():
            print(f"  skip {cid}: no model_setup.py")
            continue
        targets.append((cid, ec, mp))

    reports: list[dict[str, Any]] = []
    t0 = time.time()
    completed = 0

    def _run_one(cid: str, ec: str, mp: Path) -> dict[str, Any]:
        try:
            return verify_file(mp, energy_capture=ec, concept_id=cid,
                               model=args.model, timeout=args.timeout)
        except Exception as e:
            return _make_null_canonical_report(
                concept_id=cid, energy_capture=ec,
                reason=f"verifier exception: {type(e).__name__}: {e}",
            )

    with ThreadPoolExecutor(max_workers=max(1, args.parallel)) as ex:
        future_to_cid = {ex.submit(_run_one, c, e, m): c for c, e, m in targets}
        for fut in as_completed(future_to_cid):
            r = fut.result()
            reports.append(r)
            completed += 1
            v = compare_to_canonical(r)
            print(f"  [{completed}/{len(targets)}] {r['concept_id']} "
                  f"({r['energy_capture']}) ... {v['status']}",
                  flush=True)

    elapsed = time.time() - t0
    summary = summarize_drift(reports)

    (OUT_DIR / "drift_report.json").write_text(
        json.dumps({"summary": summary, "reports": reports}, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "summary.md").write_text(
        _render_summary_md(summary, elapsed),
        encoding="utf-8",
    )

    c = summary["counts"]
    print(f"\nSummary: {c['clean']} clean, {c['drift']} drift, "
          f"{c['scenario_sweep_concern']} sweep, {c['unknown_canonical']} unknown. "
          f"Elapsed {elapsed:.1f}s.")
    print(f"Reports written to {OUT_DIR}/drift_report.json and {OUT_DIR}/summary.md")


if __name__ == "__main__":
    main()
