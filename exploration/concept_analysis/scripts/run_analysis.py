#!/usr/bin/env python3
"""
Automated concept analysis pipeline for Fusion TEA.

Produces D1+ concept analyses for fusion concepts using Phase 1a dossiers
and extracted sources as input. Orchestrates headless Claude calls with
template-driven prompts and an approval-based reuse pool.

Usage:
  uv run python exploration/concept_analysis/scripts/run_analysis.py list
  uv run python exploration/concept_analysis/scripts/run_analysis.py status
  uv run python exploration/concept_analysis/scripts/run_analysis.py gap-check 01 --dry-run
  uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 01
  uv run python exploration/concept_analysis/scripts/run_analysis.py approve 01
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all 01 02 03
"""

import argparse
import csv
import re
import shutil
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

from lib.paths import (
    ANALYSES_DIR,
    BRIEF_PATH,
    CONCEPT_ANALYSIS_DIR,
    COSTINGFE_DIR,
    EXTRACT_OUTPUT,
    FREEFORM_EXEMPLAR_PATH,
    HANDWRITTEN_DIR,
    MEMORY_DIR,
    PHASE_1A_DIR,
    REPO_ROOT,
    RESEARCH_DIR,
    SCHEMA_PATH,
    TABLE_PATH,
    TEMPLATES_DIR,
)
from lib.frontmatter import make_frontmatter, parse_frontmatter, update_frontmatter_field
from lib.templating import fill_template
from lib.concepts import (
    COSTINGFE_MAPPING,
    FAMILY_KEY_MAP,
    FREEFORM_CONCEPTS,
    load_table,
    resolve_concepts,
    resolve_one,
)
from lib.state import get_concept_state, get_iteration_summary, propagate_staleness, _has_downstream_artifacts
from lib.sources import (
    check_duplicate_source,
    find_latest_sources_dir,
    find_sources,
    flatten_companion_dir,
    format_source_list,
    get_dossier_path,
    parse_proposed_actions,
    resolve_source_names,
    slugify_source,
)
from lib.memory import (
    find_approved,
    find_approved_syntheses,
    find_exemplars,
    format_path_list,
    load_relevant_memories,
)
from lib.claude import invoke_claude, run_model
from lib.loop import build_model_vars, run_stage1_loop
from lib.step_runner import run_claude_step, StepResult


def cmd_list(concepts: list[dict], _args: argparse.Namespace) -> None:
    """Print all concepts with IDs."""
    print(f"{'ID':<45} {'Concept Name':<40} {'Company':<30} {'Family'}")
    print("-" * 145)
    for c in concepts:
        print(f"{c['_id']:<45} {c['Concept Name']:<40} {c.get('Company', ''):<30} {c.get('Confinement Family', '')}")
    print(f"\n{len(concepts)} concepts total")


# ---------------------------------------------------------------------------
# Subcommand: status
# ---------------------------------------------------------------------------


def cmd_status(concepts: list[dict], args: argparse.Namespace) -> None:
    """Print per-concept status table."""
    # Resolve which concepts to show (default: all)
    if args.concepts or args.family:
        targets = resolve_concepts(
            args.concepts, concepts, family=args.family,
        )
    else:
        targets = concepts

    # State symbols for compact display
    state_symbols = {
        "not-started": "  -",
        "gap-checked": "  G",
        "drafted":     "  D",
        "model-setup": "  M",
        "reviewed":    "  R",
        "synthesized": "  S",
        "approved":    "  A",
    }

    print(f"{'ID':<45} {'Concept Name':<40} {'State':<6} {'Iterations'}")
    print("-" * 120)

    counts = {s: 0 for s in state_symbols}
    stale_count = 0
    for c in targets:
        state = get_concept_state(c["_id"])
        base_state = state.rstrip("*")
        counts[base_state] = counts.get(base_state, 0) + 1
        sym = state_symbols.get(base_state, "  ?")
        if state.endswith("*"):
            sym = sym + "*"
            stale_count += 1
        iter_summary = get_iteration_summary(c["_id"]) or ""
        print(f"{c['_id']:<45} {c['Concept Name']:<40} {sym:<6} {iter_summary}")

    print(f"\n{len(targets)} concepts: "
          f"{counts['approved']} approved, {counts['synthesized']} synthesized, "
          f"{counts['reviewed']} reviewed, {counts['model-setup']} model-setup, "
          f"{counts['drafted']} drafted, {counts['gap-checked']} gap-checked, "
          f"{counts['not-started']} not-started"
          + (f", {stale_count} stale" if stale_count else ""))
    print("\nLegend: A=approved  S=synthesized  R=reviewed  M=model-setup  "
          "D=drafted  G=gap-checked  -=not-started  *=stale downstream")


# ---------------------------------------------------------------------------
# Stub subcommands (implemented in later phases)
# ---------------------------------------------------------------------------


def cmd_gap_check(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 1: Gap assessment."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="gap-checked",
    )
    if not targets:
        print("No concepts to gap-check.")
        return

    for c in targets:
        cid = c["_id"]
        rid = c["_research_id"]
        out_dir = ANALYSES_DIR / cid

        # Prereq: must have a dossier
        dossier_path = get_dossier_path(rid)
        if not dossier_path:
            print(f"  skip {cid} (no Phase 1a dossier found)")
            continue

        sources = find_sources(rid)

        def _build_vars(c, _dossier=dossier_path, _sources=sources):
            return {
                "concept_id": c["_id"],
                "concept_name": c["Concept Name"],
                "company": c.get("Company", ""),
                "dossier_path": str(_dossier),
                "source_file_list": format_source_list(_sources),
                "brief_path": str(BRIEF_PATH),
                "schema_path": str(SCHEMA_PATH),
            }

        def _post(c, r):
            print(f" done ({r.elapsed:.0f}s, {len(r.output_text)} chars)")

        run_claude_step(
            c,
            template_name="gap_check.md",
            build_vars=_build_vars,
            prompt_path=out_dir / "prompts" / "gap_check_prompt.md",
            output_path=out_dir / "gap_report.md",
            label="gap-check",
            args=args,
            output_mode="stdout_to_file",
            skip_message="(gap_report.md exists, use --force to re-run)",
            post_hook=_post,
        )


def cmd_analyze(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 2: D1+ analysis with iterative assessment loop."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="approved",
    )
    if not targets:
        print("No concepts to analyze.")
        return

    resume = getattr(args, "resume", False)

    # Validate flag constraints
    if resume and args.force:
        print("Error: --resume and --force are mutually exclusive.")
        print("  --resume continues from the last iteration")
        print("  --force restarts from scratch")
        sys.exit(1)

    feedback = getattr(args, "feedback", None)
    if feedback:
        if resume:
            print("Error: --feedback and --resume are mutually exclusive.")
            sys.exit(1)
        if args.force:
            print("Error: --feedback and --force are mutually exclusive.")
            print("  --feedback applies changes to existing analysis.md")
            print("  --force re-creates analysis.md from scratch")
            sys.exit(1)
        if not feedback.is_file():
            print(f"Error: feedback file not found: {feedback}")
            sys.exit(1)
        if len(targets) > 1:
            print("Error: --feedback can only be used with a single concept")
            sys.exit(1)

    # Feedback-apply mode: separate path (not part of the loop)
    if feedback:
        _apply_external_feedback(targets, args, feedback)
        return

    # Load templates once
    analysis_template = (TEMPLATES_DIR / "analysis_v2.md").read_text(encoding="utf-8")
    assessment_template = (TEMPLATES_DIR / "assessment.md").read_text(encoding="utf-8")

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"

        # Skip logic (unchanged behavior without --resume)
        if not resume and not args.force and analysis_path.exists():
            print(f"  skip {cid} (analysis.md exists, use --force or --resume)")
            continue

        common_vars = _build_common_vars(c)
        if common_vars is None:
            continue  # skip message already printed

        out_dir.mkdir(parents=True, exist_ok=True)

        # Delegate to loop runner
        run_stage1_loop(c, args, resume=resume,
                        common_vars=common_vars,
                        analysis_template=analysis_template,
                        assessment_template=assessment_template)


def _build_common_vars(concept: dict) -> dict | None:
    """Build common template variables for a concept. Returns None if dossier missing."""
    cid = concept["_id"]
    rid = concept["_research_id"]
    analysis_path = ANALYSES_DIR / cid / "analysis.md"

    dossier_path = get_dossier_path(rid)
    if not dossier_path:
        print(f"  skip {cid} (no Phase 1a dossier found)")
        return None

    sources = find_sources(rid)
    approved = find_approved()
    exemplars = find_exemplars()
    output_template_path = TEMPLATES_DIR / "output_template.md"

    memory_context = load_relevant_memories(
        cid, MEMORY_DIR, family=concept.get("Confinement Family", ""),
    )

    return {
        "concept_id": cid,
        "concept_name": concept["Concept Name"],
        "company": concept.get("Company", ""),
        "dossier_path": str(dossier_path),
        "source_paths": format_source_list(sources),
        "brief_path": str(BRIEF_PATH),
        "schema_path": str(SCHEMA_PATH),
        "exemplar_paths": format_path_list(exemplars, "(no exemplars found)"),
        "approved_analyses": format_path_list(
            approved, "No approved prior analyses available."),
        "output_template_path": str(output_template_path),
        "analysis_path": str(analysis_path),
        "memory_context": memory_context,
    }


def _apply_external_feedback(
    targets: list[dict], args: argparse.Namespace, feedback: Path,
) -> None:
    """Apply an external feedback file to existing analysis. Preserves old behavior."""
    analysis_template = (TEMPLATES_DIR / "analysis_v2.md").read_text(encoding="utf-8")

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md — --feedback requires existing analysis)")
            continue

        common_vars = _build_common_vars(c)
        if common_vars is None:
            continue

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt = fill_template(analysis_template, {
            **common_vars,
            "output_path": "",
            "cold_start": "",
            "feedback_pass": "true",
            "feedback_path": str(feedback),
            "self_advance": "",
        })

        prompt_path = out_dir / f"feedback_apply_prompt_{ts}.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid}: feedback prompt saved to {prompt_path}")
            continue

        print(f"  apply feedback {cid} ...", end="", flush=True)
        t0 = time.time()
        _stdout, stderr, rc = invoke_claude(
            prompt, cwd=CONCEPT_ANALYSIS_DIR,
            timeout=args.timeout, model=args.model,
        )
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={rc})")
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)
            continue

        print(f" done ({elapsed:.0f}s)")

        stale = propagate_staleness(cid, "feedback-applied-from-change-requests")
        if stale:
            print(f"    stale: {', '.join(stale)}")

        archive_name = f"change_requests_{ts}.md"
        archived = feedback.parent / archive_name
        feedback.rename(archived)
        print(f"    archived: {feedback.name} → {archive_name}")


def cmd_model_setup(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 3: Generate model setup script (1costingfe or free-form)."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="model-setup",
    )
    if not targets:
        print("No concepts to model-setup.")
        return

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        model_path = out_dir / "model_setup.py"

        result = build_model_vars(c, model_path, out_dir, standalone=True)
        if result is None:
            print(f"  skip {cid} (no analysis.md — run analyze first)")
            continue
        template_name, cached_vars = result
        path_label = "1costingfe" if "costingfe_concept" in cached_vars else "free-form"

        def _build_vars(c, _vars=cached_vars):
            return _vars

        def _post(c, r, _model_path=model_path, _out_dir=out_dir):
            size = _model_path.stat().st_size
            print(f" done ({r.elapsed:.0f}s, {size} bytes)")
            model_output_path = _out_dir / "model_output.txt"
            print(f"    running model ...", end="", flush=True)
            ok, msg = run_model(_model_path, model_output_path)
            if ok:
                lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
                lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
                print(f" ok{lcoe_str}")
            else:
                print(f" FAILED: {msg}")
                print(f"    hint: fix model_setup.py and run: uv run python {_model_path}")

        run_claude_step(
            c,
            template_name=template_name,
            build_vars=_build_vars,
            prompt_path=out_dir / "prompts" / "model_setup_prompt.md",
            output_path=model_path,
            label="model-setup",
            label_suffix=f" ({path_label})",
            args=args,
            output_mode="file_exists",
            skip_message="(model_setup.py exists, use --force)",
            missing_output_message=f"Claude did not write {model_path}",
            post_hook=_post,
        )


def cmd_review(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 4: Structured review with proposed actions."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="reviewed",
    )
    if not targets:
        print("No concepts to review.")
        return

    for c in targets:
        cid = c["_id"]
        rid = c["_research_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"
        model_path = out_dir / "model_setup.py"
        review_path = out_dir / "review.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md — run analyze first)")
            continue

        if not model_path.exists():
            print(f"  warn {cid}: no model_setup.py — reviewing analysis only")

        # Determine iteration number (always increment, even with --force)
        fm = parse_frontmatter(analysis_path)
        prev_iterations = fm.get("Review-Iterations", "0")
        iteration = int(prev_iterations) + 1

        sources = find_sources(rid)
        model_output_path = out_dir / "model_output.txt"
        synth_list = [s for s in find_approved_syntheses() if s.parent.name != cid]

        def _build_vars(c, _ap=analysis_path, _mp=model_path, _rp=review_path,
                        _sources=sources, _iteration=iteration,
                        _mop=model_output_path, _synths=synth_list):
            return {
                "concept_name": c["Concept Name"],
                "company": c.get("Company", ""),
                "analysis_path": str(_ap),
                "model_setup_path": str(_mp) if _mp.exists() else "",
                "model_output_path": str(_mop) if _mop.exists() else "",
                "approved_syntheses": format_path_list(
                    _synths, "(none yet — this is among the first reviews)"),
                "source_paths": format_source_list(_sources),
                "source_count": str(len(_sources)),
                "output_path": str(_rp),
                "iteration": str(_iteration),
                "date": date.today().isoformat(),
            }

        def _post(c, r, _ap=analysis_path, _iteration=iteration):
            # Detect verdict from new strategic review format
            if re.search(r"^VERDICT:\s*PROCEED", r.output_text, re.MULTILINE):
                review_status = "proceed"
            elif re.search(r"^VERDICT:\s*REVISE", r.output_text, re.MULTILINE):
                review_status = "revise"
            else:
                # Legacy fallback for old-format review output
                if re.search(r"\*\*Overall:\*\*\s*CLEAN", r.output_text, re.MULTILINE):
                    review_status = "clean"
                else:
                    review_status = "has-actions"
            text = _ap.read_text(encoding="utf-8")
            text = update_frontmatter_field(text, "Review-Iterations", str(_iteration))
            text = update_frontmatter_field(text, "Last-Review", date.today().isoformat())
            text = update_frontmatter_field(text, "Review-Status", review_status)
            _ap.write_text(text, encoding="utf-8")
            print(f" done ({r.elapsed:.0f}s, {len(r.output_text)} chars) — {review_status}")

        run_claude_step(
            c,
            template_name="review.md",
            build_vars=_build_vars,
            prompt_path=out_dir / "prompts" / "review_prompt.md",
            output_path=review_path,
            label=f"review",
            args=args,
            output_mode="file_with_fallback",
            skip_message="(review.md exists, use --force to re-run)",
            missing_output_message="no review output",
            post_hook=_post,
        )


def cmd_address_review(concepts: list[dict], args: argparse.Namespace) -> None:
    """Apply user decisions from review report."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
    )
    if not targets:
        print("No concepts to address-review.")
        return

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        review_path = out_dir / "review.md"
        analysis_path = out_dir / "analysis.md"
        model_path = out_dir / "model_setup.py"
        log_path = out_dir / "address_log.md"

        if not review_path.exists():
            print(f"  skip {cid} (no review.md — run review first)")
            continue

        # Guard: address-review only valid for PROCEED verdict
        fm = parse_frontmatter(analysis_path)
        review_status = fm.get("Review-Status", "")
        if review_status == "revise":
            print(f"  skip {cid} (Review-Status is 'revise' — "
                  f"run stage1-all --resume to address review findings, "
                  f"not address-review)")
            continue

        # Parse proposed actions
        actions = parse_proposed_actions(review_path)
        actionable = [
            a for a in actions
            if a.get("decision") and a["decision"] not in ("", "_")
        ]

        if not actionable:
            print(f"  skip {cid} (no decisions filled in review.md — "
                  f"edit review.md and fill in Decision fields)")
            continue

        # Build decisions block for prompt
        decisions_lines = []
        for a in actionable:
            decisions_lines.append(f"### {a['id']}: {a['description']}")
            decisions_lines.append(f"- **Decision:** {a['decision']}")
            decisions_lines.append(f"- **User Notes:** {a.get('user_notes', '')}")
            decisions_lines.append(f"- **Location:** {a['location']}")
            decisions_lines.append(f"- **Proposed Fix:** {a['proposed_fix']}")
            decisions_lines.append("")

        fm = parse_frontmatter(analysis_path)
        iteration = fm.get("Review-Iterations", "1")

        def _build_vars(c, _ap=analysis_path, _mp=model_path, _lp=log_path,
                        _decisions=decisions_lines, _iteration=iteration):
            return {
                "concept_name": c["Concept Name"],
                "analysis_path": str(_ap),
                "model_setup_path": str(_mp) if _mp.exists() else "",
                "decisions_block": "\n".join(_decisions),
                "log_path": str(_lp),
                "iteration": _iteration,
                "date": date.today().isoformat(),
            }

        def _post(c, r, _ap=analysis_path, _mp=model_path, _out_dir=out_dir,
                  _actionable=actionable):
            # Re-run model if it exists
            model_output_path = _out_dir / "model_output.txt"
            if _mp.exists():
                print(f"    re-running model ...", end="", flush=True)
                ok, msg = run_model(_mp, model_output_path)
                if ok:
                    lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
                    lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
                    print(f" ok{lcoe_str}")
                else:
                    print(f" FAILED: {msg}")
                    print(f"    warn: model may be broken after review changes")
            # Update frontmatter
            text = _ap.read_text(encoding="utf-8")
            text = update_frontmatter_field(text, "Review-Status", "addressed")
            _ap.write_text(text, encoding="utf-8")
            print(f" done ({r.elapsed:.0f}s, {len(_actionable)} actions processed)")

        prompt_path = out_dir / "prompts" / "address_review_prompt.md"

        # address-review has a custom dry-run format with action count;
        # handle dry-run in caller before reaching the helper
        if args.dry_run:
            template_text = (TEMPLATES_DIR / "address_review.md").read_text(encoding="utf-8")
            prompt = fill_template(template_text, _build_vars(c))
            prompt_path.write_text(prompt, encoding="utf-8")
            print(f"  dry-run {cid}: prompt saved to {prompt_path} "
                  f"({len(actionable)} actions)")
            continue

        run_claude_step(
            c,
            template_name="address_review.md",
            build_vars=_build_vars,
            prompt_path=prompt_path,
            output_path=None,
            label="address-review",
            args=args,
            output_mode="no_output",
            skip_if_exists=False,
            post_hook=_post,
        )


def cmd_synthesize(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 5: Generate editorial synthesis."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
        target_state="synthesized",
    )
    if not targets:
        print("No concepts to synthesize.")
        return

    # Gather approved prior syntheses for cross-concept context
    prior_syntheses = find_approved_syntheses()

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"
        model_setup_path = out_dir / "model_setup.py"
        model_output_path = out_dir / "model_output.txt"
        synthesis_path = out_dir / "synthesis.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md — run analyze first)")
            continue

        # Enforce ordering: must be reviewed
        fm = parse_frontmatter(analysis_path)
        review_status = fm.get("Review-Status", "")
        if review_status not in ("addressed", "clean", "proceed"):
            print(f"  skip {cid} (Review-Status is '{review_status}'; "
                  f"run review and address-review first)")
            continue

        if synthesis_path.exists() and not args.force:
            print(f"  skip {cid} (synthesis.md exists, use --force to re-run)")
            continue

        # Ensure model output is fresh before synthesizing
        if model_setup_path.exists():
            need_run = False
            reason = ""
            if not model_output_path.exists():
                need_run = True
                reason = "model_output.txt missing"
            elif model_setup_path.stat().st_mtime > model_output_path.stat().st_mtime:
                need_run = True
                reason = "model_setup.py newer than model_output.txt"

            if need_run:
                print(f"    running model ({reason}) ...", end="", flush=True)
                ok, msg = run_model(model_setup_path, model_output_path)
                if ok:
                    lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
                    lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
                    print(f" ok{lcoe_str}")
                else:
                    print(f" FAILED: {msg}")
                    print(f"    warn: synthesizing without model output")

        # Format approved prior syntheses (exclude current concept)
        synth_list = [s for s in prior_syntheses if s.parent.name != cid]
        if synth_list:
            approved_syntheses = format_path_list(synth_list)
        else:
            approved_syntheses = "(none yet — this is among the first syntheses)"

        body_path = out_dir / "synthesis_body.md"

        def _build_vars(c, _ap=analysis_path, _msp=model_setup_path,
                        _mop=model_output_path, _bp=body_path,
                        _approved=approved_syntheses):
            return {
                "concept_name": c["Concept Name"],
                "company": c.get("Company", ""),
                "analysis_path": str(_ap),
                "model_setup_path": str(_msp) if _msp.exists() else "",
                "model_output_path": str(_mop) if _mop.exists() else "",
                "approved_syntheses": _approved,
                "output_path": str(_bp),
            }

        # Pre-write synthesis.md with controlled frontmatter before Claude call
        # (but only for live runs — dry-run should not create synthesis.md)
        def _pre_write_fm(_cid=cid, _c=c, _sp=synthesis_path):
            today = date.today().isoformat()
            synth_fm = (
                f"---\n"
                f"ID: {_cid}\n"
                f"Concept: {_c['Concept Name']}\n"
                f"Company: {_c.get('Company', '')}\n"
                f"Type: synthesis\n"
                f"Status: draft\n"
                f"Created: {today}\n"
                f"---\n"
            )
            _sp.write_text(synth_fm, encoding="utf-8")

        def _post(c, r, _sp=synthesis_path, _bp=body_path):
            # Assemble: frontmatter + body
            fm_raw = _sp.read_text(encoding="utf-8").rstrip("\n") + "\n"
            body = _bp.read_text(encoding="utf-8")
            # Strip any frontmatter Claude may have added to the body
            if body.startswith("---"):
                fm_end = body.find("---", 3)
                if fm_end != -1:
                    body = body[fm_end + 3:].lstrip("\n")
            _sp.write_text(fm_raw + "\n" + body, encoding="utf-8")
            _bp.unlink()
            size = len(_sp.read_text(encoding="utf-8"))
            print(f" done ({r.elapsed:.0f}s, {size} chars)")

        # For live runs, pre-write frontmatter before the Claude call
        if not args.dry_run:
            _pre_write_fm()

        run_claude_step(
            c,
            template_name="synthesis.md",
            build_vars=_build_vars,
            prompt_path=out_dir / "prompts" / "synthesis_prompt.md",
            output_path=body_path,
            label="synthesize",
            args=args,
            output_mode="file_with_fallback",
            skip_message="(synthesis.md exists, use --force to re-run)",
            skip_if_exists=False,  # we handle skip above (synthesis_path, not body_path)
            missing_output_message=f"Claude did not write {body_path}",
            on_failure_cleanup=lambda _sp=synthesis_path: _sp.unlink(missing_ok=True),
            post_hook=_post,
        )


def cmd_approve(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 6: Approve a reviewed analysis."""
    targets = resolve_concepts(args.concepts, concepts)
    if not targets:
        print("No concepts to approve.")
        return

    today = date.today().isoformat()

    for c in targets:
        cid = c["_id"]
        analysis_path = ANALYSES_DIR / cid / "analysis.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md found — run analyze first)")
            continue

        fm = parse_frontmatter(analysis_path)
        if fm.get("Status") == "approved":
            print(f"  skip {cid} (already approved on {fm.get('Approved-Date', '?')})")
            continue

        # Review gate: must have a PROCEED review (unless --force)
        review_status = fm.get("Review-Status", "")
        if review_status not in ("proceed", "addressed", "clean") and not args.force:
            print(f"  skip {cid} (Review-Status is '{review_status}' — "
                  f"run review first, or use --force)")
            continue

        # Synthesis gate: warn and skip if no synthesis.md (unless --force)
        synthesis_path = ANALYSES_DIR / cid / "synthesis.md"
        if not synthesis_path.exists() and not args.force:
            print(f"  skip {cid} (no synthesis.md — run synthesize first, or use --force)")
            continue

        # Update frontmatter: Status → approved, set Approved-Date
        text = analysis_path.read_text(encoding="utf-8")
        text = update_frontmatter_field(text, "Status", "approved")
        text = update_frontmatter_field(text, "Approved-Date", today)
        analysis_path.write_text(text, encoding="utf-8")

        # Also update synthesis.md frontmatter if it exists
        if synthesis_path.exists():
            synth_text = synthesis_path.read_text(encoding="utf-8")
            synth_text = update_frontmatter_field(synth_text, "Status", "approved")
            synth_text = update_frontmatter_field(synth_text, "Approved-Date", today)
            synthesis_path.write_text(synth_text, encoding="utf-8")

        print(f"  approved {cid}")


# ---------------------------------------------------------------------------
# Composite: stage1-all (gap-check → analyze → model-setup → review)
# ---------------------------------------------------------------------------


def cmd_stage1_all(concepts: list[dict], args: argparse.Namespace) -> None:
    """Run analyze → model-setup → review for specified concepts.

    Gap-check is skipped by default; pass --include-gap-analysis to include it.
    Each stage's own skip logic handles prerequisites and existing outputs,
    so re-running is safe (picks up where it left off).
    """
    # Resolve once for summary display
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
    )
    if not targets:
        print("No concepts to process.")
        return

    names = ", ".join(c["_num"] for c in targets)
    print(f"=== stage1-all: {len(targets)} concepts ({names}) ===")
    if getattr(args, "include_gap_analysis", False):
        print("    Pipeline: gap-check → analyze → model-setup → review")
    else:
        print("    Pipeline: analyze → model-setup → review")

    stages = []
    if getattr(args, "include_gap_analysis", False):
        stages.append(("Gap Check", cmd_gap_check))
    stages.extend([
        ("Analyze", cmd_analyze),
        ("Model Setup", cmd_model_setup),
        ("Review", cmd_review),
    ])

    for stage_name, handler in stages:
        print(f"\n--- {stage_name} ---")
        handler(concepts, args)

    # Final status summary
    print(f"\n=== stage1-all complete ===")
    for c in targets:
        state = get_concept_state(c["_id"])
        print(f"  {c['_num']} ({c['Concept Name']}): {state}")


# ---------------------------------------------------------------------------
# cmd_add_source — add a PDF or URL source to a concept
# ---------------------------------------------------------------------------


def cmd_add_source(concepts: list[dict], args: argparse.Namespace) -> None:
    """Add a PDF or URL source to a concept's sources directory."""
    # Resolve single concept
    matches = resolve_one(concepts, args.concept)
    if len(matches) == 0:
        print(f"  error: no concept matching '{args.concept}'")
        sys.exit(1)
    if len(matches) > 1:
        print(f"  error: '{args.concept}' matches multiple concepts:")
        for c in matches:
            print(f"    {c['_num']} {c['Concept Name']}")
        sys.exit(1)
    concept = matches[0]
    research_id = concept["_research_id"]

    # Determine source name
    name = args.name if args.name else slugify_source(args.source)
    if not name:
        print("  error: could not derive source name — use --name to specify")
        sys.exit(1)

    print(f"  concept: {concept['_num']} ({concept['Concept Name']})")
    print(f"  source:  {args.source}")
    print(f"  name:    {name}")

    # Duplicate check
    existing = check_duplicate_source(research_id, name)
    if existing:
        if args.force:
            # NOTE: existing source may be in an older iter-NN; the new
            # extraction will land in the latest iter (find_latest_sources_dir).
            # This effectively moves the source forward, which is intentional.
            print(f"  force: removing existing source '{name}' at {existing.parent}")
            existing.unlink(missing_ok=True)
            companion = existing.parent / name
            if companion.is_dir():
                shutil.rmtree(companion)
        else:
            print(f"  error: source '{name}' already exists: {existing}")
            print("  use --force to re-extract")
            sys.exit(1)

    # Find placement
    sources_dir = find_latest_sources_dir(research_id)
    companion_dir = sources_dir / name
    symlink_path = sources_dir / f"{name}.md"

    print(f"  target:  {symlink_path}")

    if args.dry_run:
        print(f"\n  [dry-run] would create:")
        print(f"    companion dir: {companion_dir}/")
        print(f"    symlink:       {symlink_path} → {name}/{EXTRACT_OUTPUT}")
        print(f"    extraction:    uv run agentic-mbse extract {args.source} --save-source --output {companion_dir}/")
        return

    # Create companion dir
    companion_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Run extraction
        print(f"\n  extracting source...")
        cmd = [
            "uv", "run", "agentic-mbse", "extract", args.source,
            "--save-source", "--output", str(companion_dir),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode != 0:
            stderr_snippet = result.stderr.strip()[:500] if result.stderr else "(no stderr)"
            print(f"  error: extraction failed (rc={result.returncode})")
            print(f"  stderr: {stderr_snippet}")
            raise RuntimeError("extraction failed")

        # Flatten nested PDF subdirectory if present
        flatten_companion_dir(companion_dir)

        # Verify output.md exists
        output_path = companion_dir / EXTRACT_OUTPUT
        if not output_path.exists():
            print(f"  error: extraction completed but {EXTRACT_OUTPUT} not found in {companion_dir}")
            raise RuntimeError("output.md missing")

        # Create symlink (relative path)
        symlink_path.symlink_to(f"{name}/{EXTRACT_OUTPUT}")
        print(f"  created: {symlink_path}")
        print(f"  done — source '{name}' added successfully")

    except Exception as exc:
        # Clean up partial artifacts
        if companion_dir.exists():
            shutil.rmtree(companion_dir)
        if symlink_path.is_symlink():
            symlink_path.unlink()
        # RuntimeError messages already printed above; print others
        if not isinstance(exc, RuntimeError):
            print(f"  error: {exc}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_analysis.py",
        description="Automated concept analysis pipeline for Fusion TEA",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- list --
    sub.add_parser("list", help="List all concepts with IDs")

    # -- status --
    p_status = sub.add_parser("status", help="Show per-concept state table")
    p_status.add_argument("concepts", nargs="*", default=[], help="Concept IDs to show (default: all)")
    p_status.add_argument("--family", help="Filter by confinement family (MFE, IFE, MIF, Non-Standard)")

    # -- gap-check --
    p_gap = sub.add_parser("gap-check", help="Run Stage 1 gap assessment")
    p_gap.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_gap.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_gap.add_argument("--family", help="Filter by confinement family")
    p_gap.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_gap.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_gap.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_gap.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # -- analyze --
    p_analyze = sub.add_parser("analyze", help="Run Stage 2 D1+ analysis")
    p_analyze.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_analyze.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_analyze.add_argument("--family", help="Filter by confinement family")
    p_analyze.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_analyze.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_analyze.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_analyze.add_argument("--force", action="store_true", help="Re-run even if output exists")
    p_analyze.add_argument("--max-passes", type=int, default=3,
                            help="Max analyze→assess iterations (default: 3; 1=no assessment)")
    p_analyze.add_argument("--feedback", type=Path, metavar="PATH",
                            help="Apply feedback file to existing analysis (skips cold-start)")
    p_analyze.add_argument("--resume", action="store_true",
                            help="Continue from last iteration (add more passes)")
    p_analyze.add_argument("--research", action="store_true",
                            help="Enable autonomous research step between iterations "
                                 "(searches web for data gaps, extracts via add-source)")
    p_analyze.add_argument("--max-research-searches", type=int, default=5,
                            help="Max WebSearch calls per research step (default: 5)")
    p_analyze.add_argument("--max-research-extractions", type=int, default=3,
                            help="Max source extractions per research step (default: 3)")

    # -- model-setup --
    p_ms = sub.add_parser("model-setup", help="Generate 1costingfe model setup script")
    p_ms.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_ms.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_ms.add_argument("--family", help="Filter by confinement family")
    p_ms.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_ms.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_ms.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_ms.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # -- review --
    p_rev = sub.add_parser("review", help="Structured review with proposed actions")
    p_rev.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_rev.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_rev.add_argument("--family", help="Filter by confinement family")
    p_rev.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_rev.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_rev.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_rev.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # -- address-review --
    p_addr = sub.add_parser("address-review", help="Apply user decisions from review")
    p_addr.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_addr.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_addr.add_argument("--family", help="Filter by confinement family")
    p_addr.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_addr.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_addr.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")

    # -- synthesize --
    p_syn = sub.add_parser("synthesize", help="Generate editorial synthesis")
    p_syn.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_syn.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_syn.add_argument("--family", help="Filter by confinement family")
    p_syn.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_syn.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_syn.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_syn.add_argument("--force", action="store_true", help="Re-run even if output exists")

    # -- approve --
    p_approve = sub.add_parser("approve", help="Approve a reviewed analysis")
    p_approve.add_argument("concepts", nargs="+", help="Concept IDs to approve")
    p_approve.add_argument("--force", action="store_true", help="Approve even without synthesis")

    # -- stage1-all --
    p_s1 = sub.add_parser(
        "stage1-all",
        help="Run full pipeline through review: gap-check → analyze → model-setup → review",
    )
    p_s1.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_s1.add_argument("--all", dest="all_remaining", action="store_true", help="All remaining concepts")
    p_s1.add_argument("--family", help="Filter by confinement family")
    p_s1.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_s1.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_s1.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout in seconds")
    p_s1.add_argument("--force", action="store_true", help="Re-run even if output exists")
    p_s1.add_argument("--max-passes", type=int, default=3,
                       help="Max analyze→assess iterations (default: 3; 1=no assessment)")
    p_s1.add_argument("--include-gap-analysis", action="store_true",
                       help="Include gap-check stage (skipped by default)")
    p_s1.add_argument("--resume", action="store_true",
                       help="Resume analysis from last iteration")
    p_s1.add_argument("--research", action="store_true",
                       help="Enable autonomous research step between iterations "
                            "(searches web for data gaps, extracts via add-source)")
    p_s1.add_argument("--max-research-searches", type=int, default=5,
                       help="Max WebSearch calls per research step (default: 5)")
    p_s1.add_argument("--max-research-extractions", type=int, default=3,
                       help="Max source extractions per research step (default: 3)")

    # -- add-source --
    p_add = sub.add_parser("add-source", help="Add a PDF or URL source to a concept")
    p_add.add_argument("concept", help="Concept ID (single concept)")
    p_add.add_argument("source", help="PDF path or URL to extract")
    p_add.add_argument("--name", help="Override automatic source name")
    p_add.add_argument("--force", action="store_true",
                       help="Re-extract even if source name already exists")
    p_add.add_argument("--dry-run", action="store_true", help="Show what would be created")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    table = load_table()

    dispatch = {
        "list": cmd_list,
        "status": cmd_status,
        "gap-check": cmd_gap_check,
        "analyze": cmd_analyze,
        "model-setup": cmd_model_setup,
        "review": cmd_review,
        "address-review": cmd_address_review,
        "synthesize": cmd_synthesize,
        "approve": cmd_approve,
        "stage1-all": cmd_stage1_all,
        "add-source": cmd_add_source,
    }

    handler = dispatch[args.command]
    handler(table, args)


if __name__ == "__main__":
    main()
