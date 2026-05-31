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
  uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 01 02 03 && review 01 02 03
"""

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

from lib.paths import (
    ANALYSES_DIR,
    ARCHETYPE_FIT_PATH,
    BRIEF_PATH,
    COMPARABLES_PATH,
    CONCEPT_ANALYSIS_DIR,
    COSTINGFE_DIR,
    DESIGN_POINT_PATH,
    EXTRACT_OUTPUT,
    FREEFORM_EXEMPLAR_PATH,
    FREEFORM_ROUTES_PATH,
    HANDWRITTEN_DIR,
    MEMORY_DIR,
    ONTOLOGY_PATH,
    PHASE_1A_DIR,
    REPO_ROOT,
    RESEARCH_DIR,
    SCHEMA_PATH,
    SOURCE_INDEX_PATH,
    TABLE_PATH,
    TEMPLATES_DIR,
)
from lib.frontmatter import make_frontmatter, parse_frontmatter, update_frontmatter_field
from lib.templating import fill_template
from lib.concepts import (
    get_comparison_status,
    is_costingfe_runnable,
    load_concepts,
    load_freeform_routes,
    load_legacy_table,
    resolve_concepts,
    resolve_one,
)
from lib.iteration import read_loop_state
from lib.state import clear_staleness, get_concept_state, get_extraction_state, get_iteration_summary
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
from lib.landscape import build_concept_landscape, extract_iter_count
from lib.memory import (
    find_approved,
    find_approved_syntheses,
    find_exemplars,
    format_path_list,
    load_relevant_memories,
)
from lib.claude import invoke_claude_validated, run_model
from lib.loop import build_model_vars, extract_findings, run_stage1_loop
from lib.step_runner import prepare_step, StepContext
from lib.validators import (
    REVIEW_VERDICT_RE,
    make_file_modified_validator,
    validate_feedback_verdict,
    validate_non_empty,
    validate_python_syntax,
    validate_review_verdict,
)
from lib.scoring import (
    build_verified_scores,
    has_section8,
    parse_calibrated_table,
    parse_adjustments,
    validate_calibration_output,
    validate_score_output,
    write_verified_json,
    write_verified_md,
)
from lib.heatmap import generate_heatmap_html


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
        "iterating":   None,  # dynamic: " I{N}"
        "reviewed":    "  R",
        "synthesized": "  S",
        "approved":    "  A",
    }

    extraction_symbols = {
        "not-extracted": "  ",
        "extracted":     " E",
        "stale":         "E*",
    }

    print(f"{'ID':<45} {'Concept Name':<40} {'State':<6} {'Extr':<4} {'Iterations'}")
    print("-" * 130)

    counts = {s: 0 for s in state_symbols}
    stale_count = 0
    extracted_count = 0
    extraction_stale_count = 0
    for c in targets:
        state = get_concept_state(c["_id"])
        base_state = state.rstrip("*")
        counts[base_state] = counts.get(base_state, 0) + 1
        iter_summary = get_iteration_summary(c["_id"])

        # Build state symbol — dynamic for iterating
        if base_state == "iterating":
            n = extract_iter_count(iter_summary)
            sym = f" I{n}"
        else:
            sym = state_symbols.get(base_state, "  ?")
        if state.endswith("*"):
            sym = sym + "*"
            stale_count += 1

        # Extraction status
        ext_state = get_extraction_state(c["_id"])
        ext_sym = extraction_symbols.get(ext_state, "  ")
        if ext_state == "extracted":
            extracted_count += 1
        elif ext_state == "stale":
            extracted_count += 1
            extraction_stale_count += 1

        print(f"{c['_id']:<45} {c['Concept Name']:<40} {sym:<6} {ext_sym:<4} {iter_summary or ''}")

    ext_summary = ""
    if extracted_count:
        ext_summary = f", {extracted_count} extracted"
        if extraction_stale_count:
            ext_summary += f" ({extraction_stale_count} stale)"

    print(f"\n{len(targets)} concepts: "
          f"{counts['approved']} approved, {counts['synthesized']} synthesized, "
          f"{counts['reviewed']} reviewed, {counts['iterating']} iterating, "
          f"{counts['gap-checked']} gap-checked, "
          f"{counts['not-started']} not-started"
          + (f", {stale_count} stale" if stale_count else "")
          + ext_summary)
    print("\nLegend: A=approved  S=synthesized  R=reviewed  I{N}=iterating(N iterations)  "
          "G=gap-checked  -=not-started  *=stale downstream  E=extracted  E*=extraction stale")


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
        gap_path = out_dir / "gap_report.md"

        # Prereq: must have a dossier
        dossier_path = get_dossier_path(rid)
        if not dossier_path:
            print(f"  skip {cid} (no Phase 1a dossier found)")
            continue

        sources = find_sources(rid)
        source_index_content = SOURCE_INDEX_PATH.read_text(encoding="utf-8")

        template_text = (TEMPLATES_DIR / "gap_check.md").read_text(encoding="utf-8")
        prompt_text = fill_template(template_text, {
            "concept_id": cid,
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "dossier_path": str(dossier_path),
            "source_file_list": format_source_list(sources),
            "source_index_path": str(SOURCE_INDEX_PATH),
            "source_index_content": source_index_content,
            "brief_path": str(BRIEF_PATH),
            "schema_path": str(SCHEMA_PATH),
        })

        ctx = prepare_step(
            step_label="gap-check",
            concept_id=cid,
            prompt_text=prompt_text,
            prompt_path=out_dir / "prompts" / "gap_check_prompt.md",
            out_dir=out_dir,
            skip_if_exists=gap_path,
            dry_run=args.dry_run,
            force=args.force,
        )
        if not ctx.proceed:
            continue

        # NOTE: output_path=None is DELIBERATE here. Gap-check is a stdout-mode
        # call — Claude produces the gap report in its response, not as a file.
        # Passing output_path=None routes invoke_claude_validated into the
        # stdout-validation branch and bypasses the H-01 file-existence check
        # because there is no file for Claude to write. We validate the stdout
        # text via validate_non_empty, then explicitly write it below. Do NOT
        # "fix" this to use output_path — see design.md#migration-6-cmd_gap_check.
        result = invoke_claude_validated(
            ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
            timeout=args.timeout, model=args.model,
            validator=validate_non_empty,
            output_path=None,
            step_label="gap-check",
        )
        elapsed = time.time() - ctx.start_time

        if result.invoke.returncode != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
            print(f"    stderr: {result.invoke.stderr[:500]}", file=sys.stderr)
            continue

        if not result.validation_passed:
            print(f" FAILED ({elapsed:.0f}s) — gap-check validation exhausted")
            continue

        # Explicit write — replaces the legacy stdout_to_file mode.
        gap_path.write_text(result.invoke.stdout, encoding="utf-8")
        print(f" done ({elapsed:.0f}s, {len(result.invoke.stdout)} chars)")


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

    add_passes = getattr(args, "add_passes", None)
    resume = getattr(args, "resume", False)

    # --add-passes implies --resume
    if add_passes is not None:
        resume = True

    # Validate flag constraints
    if resume and args.force:
        print("Error: --resume and --force are mutually exclusive.")
        print("  --resume continues from the last iteration")
        print("  --force restarts from scratch")
        sys.exit(1)

    feedback = getattr(args, "feedback", None)
    if feedback:
        if args.force:
            print("Error: --feedback and --force are mutually exclusive.")
            print("  --feedback edits an existing analysis.md")
            print("  --force re-creates analysis.md from scratch (cold-start)")
            sys.exit(1)
        if len(targets) > 1:
            print("Error: --feedback can only be used with a single concept")
            sys.exit(1)
        if not feedback.is_file():
            print(f"Error: feedback file not found: {feedback}")
            sys.exit(1)
        if feedback.stat().st_size == 0:
            print(f"Error: feedback file is empty: {feedback}")
            sys.exit(1)
        fb_result = validate_feedback_verdict(feedback.read_text(encoding="utf-8"))
        if not fb_result.valid:
            print(f"Error: feedback file format invalid: {feedback}")
            print(f"  {fb_result.fix_message}")
            sys.exit(1)
        # FR-6 (a): cold-start incompatibility. --feedback edits an existing
        # analysis.md; if none exists, the user wants a cold-start instead.
        target_analysis = ANALYSES_DIR / targets[0]["_id"] / "analysis.md"
        if not target_analysis.exists():
            print(f"Error: --feedback requires an existing analysis.md for "
                  f"{targets[0]['_id']}.")
            print(f"  Run a cold-start first: "
                  f"analyze {targets[0]['_id']} (no --feedback).")
            sys.exit(1)
        # --feedback is a mid-iteration tool; implies --resume so the loop
        # appends a new iter rather than cold-starting. The user's file is
        # consumed once by the external-feedback producer in run_stage1_loop.
        resume = True

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

        common_vars = _build_common_vars(c, concepts)
        if common_vars is None:
            continue  # skip message already printed

        out_dir.mkdir(parents=True, exist_ok=True)

        # Per-concept max_passes override for --add-passes
        if add_passes is not None:
            loop_state = read_loop_state(out_dir)
            current_iter = loop_state.next_iteration - 1  # completed iterations
            args.max_passes = current_iter + add_passes
            if args.max_passes < 1:
                args.max_passes = add_passes  # fresh concept: just use add_passes
            print(f"  {cid}: at iter {current_iter}, will run up to {add_passes} more (max_passes={args.max_passes})")

        # Delegate to loop runner
        run_stage1_loop(c, args, resume=resume,
                        common_vars=common_vars,
                        analysis_template=analysis_template,
                        assessment_template=assessment_template)


def _build_common_vars(concept: dict, concepts: list[dict] | None = None) -> dict | None:
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

    landscape = ""
    if concepts is not None:
        landscape = build_concept_landscape(concepts, exclude_id=cid)

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
        "concept_landscape": landscape,
    }


def cmd_model_setup(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 3: Generate model setup script (1costingfe or free-form)."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
    )
    if not targets:
        print("No concepts to model-setup.")
        return

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        model_path = out_dir / "model_setup.py"

        feedback_text = ""
        if getattr(args, "feedback", None):
            feedback_text = extract_findings(args.feedback)
            if not feedback_text:
                feedback_text = args.feedback.read_text(encoding="utf-8")
        mv = build_model_vars(c, model_path, out_dir, standalone=True,
                              model_feedback=feedback_text)
        if mv is None:
            print(f"  skip {cid} (no analysis.md — run analyze first)")
            continue
        template_name, cached_vars = mv
        path_label = "1costingfe" if "costingfe_concept" in cached_vars else "free-form"

        template_text = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
        prompt_text = fill_template(template_text, cached_vars)

        ctx = prepare_step(
            step_label=f"model-setup ({path_label})",
            concept_id=cid,
            prompt_text=prompt_text,
            prompt_path=out_dir / "prompts" / "model_setup_prompt.md",
            out_dir=out_dir,
            skip_if_exists=model_path,
            dry_run=args.dry_run,
            force=args.force,
        )
        if not ctx.proceed:
            continue

        result = invoke_claude_validated(
            ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
            timeout=args.timeout, model=args.model,
            validator=validate_python_syntax,
            output_path=model_path,
            step_label="model-setup",
        )
        elapsed = time.time() - ctx.start_time

        if result.invoke.returncode != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
            print(f"    stderr: {result.invoke.stderr[:500]}", file=sys.stderr)
            continue

        if not result.validation_passed:
            print(f" FAILED ({elapsed:.0f}s) — model_setup.py validation exhausted")
            continue

        # Producer-clears-on-write contract: a fresh model_setup.py is
        # by definition not stale relative to the current analysis.md.
        clear_staleness(cid, "model_setup.py")

        size = model_path.stat().st_size
        print(f" done ({elapsed:.0f}s, {size} bytes)")

        # Post-validation: run the model and report.
        model_output_path = out_dir / "model_output.txt"
        print(f"    running model ...", end="", flush=True)
        ok, msg = run_model(model_path, model_output_path)
        if ok:
            lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
            lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
            print(f" ok{lcoe_str}")
        else:
            print(f" FAILED: {msg}")
            print(f"    hint: fix model_setup.py and run: uv run python {model_path}")


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

        template_text = (TEMPLATES_DIR / "review.md").read_text(encoding="utf-8")
        prompt_text = fill_template(template_text, {
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "analysis_path": str(analysis_path),
            "model_setup_path": str(model_path) if model_path.exists() else "",
            "model_output_path": str(model_output_path) if model_output_path.exists() else "",
            "approved_syntheses": format_path_list(
                synth_list, "(none yet — this is among the first reviews)"),
            "source_paths": format_source_list(sources),
            "source_count": str(len(sources)),
            "output_path": str(review_path),
            "iteration": str(iteration),
            "date": date.today().isoformat(),
        })

        ctx = prepare_step(
            step_label="review",
            concept_id=cid,
            prompt_text=prompt_text,
            prompt_path=out_dir / "prompts" / "review_prompt.md",
            out_dir=out_dir,
            skip_if_exists=review_path,
            dry_run=args.dry_run,
            force=args.force,
        )
        if not ctx.proceed:
            continue

        result = invoke_claude_validated(
            ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
            timeout=args.timeout, model=args.model,
            validator=validate_review_verdict,
            output_path=review_path,
            step_label="review",
        )
        elapsed = time.time() - ctx.start_time

        if result.invoke.returncode != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
            print(f"    stderr: {result.invoke.stderr[:500]}", file=sys.stderr)
            continue

        if not result.validation_passed:
            print(f" FAILED ({elapsed:.0f}s) — review validation exhausted")
            continue

        # Producer-clears-on-write contract.
        clear_staleness(cid, "review.md")

        # Detect verdict from the validated review file (not stdout). The
        # validator already guaranteed a VERDICT line is present.
        review_text = review_path.read_text(encoding="utf-8")
        verdict_match = REVIEW_VERDICT_RE.search(review_text)
        if verdict_match and verdict_match.group(1) == "PROCEED":
            review_status = "proceed"
        elif verdict_match and verdict_match.group(1) == "REVISE":
            review_status = "revise"
        else:
            # Should be unreachable post-validation, but keep a defensive
            # fallback for legacy review-output formats.
            if re.search(r"\*\*Overall:\*\*\s*CLEAN", review_text, re.MULTILINE):
                review_status = "clean"
            else:
                review_status = "has-actions"
                print(
                    f"\n  WARNING: could not detect PROCEED/REVISE verdict in review output."
                    f"\n  Defaulting to 'has-actions'. Check review.md manually.",
                    file=sys.stderr,
                )

        text = analysis_path.read_text(encoding="utf-8")
        text = update_frontmatter_field(text, "Review-Iterations", str(iteration))
        text = update_frontmatter_field(text, "Last-Review", date.today().isoformat())
        text = update_frontmatter_field(text, "Review-Status", review_status)
        analysis_path.write_text(text, encoding="utf-8")
        print(f" done ({elapsed:.0f}s, {len(review_text)} chars) — {review_status}")


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
                  f"run analyze --resume to address review findings, "
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

        template_vars = {
            "concept_name": c["Concept Name"],
            "analysis_path": str(analysis_path),
            "model_setup_path": str(model_path) if model_path.exists() else "",
            "decisions_block": "\n".join(decisions_lines),
            "log_path": str(log_path),
            "iteration": iteration,
            "date": date.today().isoformat(),
        }

        prompt_path = out_dir / "prompts" / "address_review_prompt.md"
        template_text = (TEMPLATES_DIR / "address_review.md").read_text(encoding="utf-8")
        prompt_text = fill_template(template_text, template_vars)

        # address-review has a custom dry-run format with action count;
        # handle dry-run before constructing the file-modified validator (which
        # would otherwise snapshot the file unnecessarily).
        if args.dry_run:
            prompt_path.parent.mkdir(parents=True, exist_ok=True)
            prompt_path.write_text(prompt_text, encoding="utf-8")
            print(f"  dry-run {cid}: prompt saved to {prompt_path} "
                  f"({len(actionable)} actions)")
            continue

        ctx = prepare_step(
            step_label="address-review",
            concept_id=cid,
            prompt_text=prompt_text,
            prompt_path=prompt_path,
            out_dir=out_dir,
            dry_run=False,  # already handled above
            force=False,
        )
        if not ctx.proceed:
            continue

        # Snapshot analysis.md bytes AFTER prepare_step but BEFORE invocation,
        # so the SHA-256 reflects the state Claude is about to edit. We
        # validate ONLY analysis.md (not model_setup.py) — see
        # design.md#migration-10-cmd_address_review for the scope decision.
        file_modified = make_file_modified_validator(analysis_path)

        result = invoke_claude_validated(
            ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
            timeout=args.timeout, model=args.model,
            validator=file_modified,
            output_path=analysis_path,
            step_label="address-review",
        )
        elapsed = time.time() - ctx.start_time

        if result.invoke.returncode != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
            print(f"    stderr: {result.invoke.stderr[:500]}", file=sys.stderr)
            continue

        if not result.validation_passed:
            print(f" FAILED ({elapsed:.0f}s) — analysis.md was not modified")
            continue

        # Re-run model if it exists
        model_output_path = out_dir / "model_output.txt"
        if model_path.exists():
            print(f"    re-running model ...", end="", flush=True)
            ok, msg = run_model(model_path, model_output_path)
            if ok:
                lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
                lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
                print(f" ok{lcoe_str}")
            else:
                print(f" FAILED: {msg}")
                print(f"    warn: model may be broken after review changes")

        # Update frontmatter
        text = analysis_path.read_text(encoding="utf-8")
        text = update_frontmatter_field(text, "Review-Status", "addressed")
        analysis_path.write_text(text, encoding="utf-8")
        print(f" done ({elapsed:.0f}s, {len(actionable)} actions processed)")


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

        # Enforce ordering: must be reviewed (unless --skip-review-gate)
        skip_gate = getattr(args, "skip_review_gate", False)
        if not skip_gate:
            fm = parse_frontmatter(analysis_path)
            review_status = fm.get("Review-Status", "")
            if review_status not in ("addressed", "clean", "proceed"):
                print(f"  skip {cid} (Review-Status is '{review_status}'; "
                      f"run review and address-review first, or use --skip-review-gate)")
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
        gap_report_path = out_dir / "gap_report.md"

        template_text = (TEMPLATES_DIR / "synthesis.md").read_text(encoding="utf-8")
        prompt_text = fill_template(template_text, {
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "analysis_path": str(analysis_path),
            "gap_report_path": str(gap_report_path) if gap_report_path.exists() else "",
            "model_setup_path": str(model_setup_path) if model_setup_path.exists() else "",
            "model_output_path": str(model_output_path) if model_output_path.exists() else "",
            "approved_syntheses": approved_syntheses,
            "output_path": str(body_path),
        })

        ctx = prepare_step(
            step_label="synthesize",
            concept_id=cid,
            prompt_text=prompt_text,
            prompt_path=out_dir / "prompts" / "synthesis_prompt.md",
            out_dir=out_dir,
            dry_run=args.dry_run,
            force=False,  # we handle skip above (synthesis_path, not body_path)
        )
        if not ctx.proceed:
            continue

        # Pre-write synthesis.md with controlled frontmatter before Claude call.
        # Done after prepare_step (which handles dry-run) so dry-run does not
        # create synthesis.md.
        today = date.today().isoformat()
        synth_fm = (
            f"---\n"
            f"ID: {cid}\n"
            f"Concept: {c['Concept Name']}\n"
            f"Company: {c.get('Company', '')}\n"
            f"Type: synthesis\n"
            f"Status: draft\n"
            f"Created: {today}\n"
            f"---\n"
        )
        synthesis_path.write_text(synth_fm, encoding="utf-8")

        result = invoke_claude_validated(
            ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
            timeout=args.timeout, model=args.model,
            validator=validate_score_output,
            output_path=body_path,
            step_label="synthesize",
        )
        elapsed = time.time() - ctx.start_time

        if result.invoke.returncode != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
            print(f"    stderr: {result.invoke.stderr[:500]}", file=sys.stderr)
            synthesis_path.unlink(missing_ok=True)
            continue

        if not result.validation_passed:
            print(f" FAILED ({elapsed:.0f}s) — synthesis body validation exhausted")
            synthesis_path.unlink(missing_ok=True)
            continue

        # Assemble: frontmatter + body
        _merge_synthesis_body(synthesis_path, body_path)
        # Producer-clears-on-write contract.
        clear_staleness(cid, "synthesis.md")
        size = len(synthesis_path.read_text(encoding="utf-8"))
        print(f" done ({elapsed:.0f}s, {size} chars)")


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
# Scoring pipeline: score, extract-scores, calibrate, heatmap
# ---------------------------------------------------------------------------

SCORES_DIR = CONCEPT_ANALYSIS_DIR / "scores"


def _merge_synthesis_body(synthesis_path: Path, body_path: Path) -> None:
    """Concatenate frontmatter stub + body, write to synthesis_path, delete body.

    The synthesize stage pre-writes synthesis.md with frontmatter only, then has
    Claude write content to synthesis_body.md, then merges. If the merge step
    is interrupted (e.g. parent subprocess timeout in run_scoring_pipeline.py),
    the body file is left orphaned. This helper performs the merge idempotently.
    """
    fm_raw = synthesis_path.read_text(encoding="utf-8").rstrip("\n") + "\n"
    body = body_path.read_text(encoding="utf-8")
    # Strip any frontmatter Claude may have added to the body.
    if body.startswith("---"):
        fm_end = body.find("---", 3)
        if fm_end != -1:
            body = body[fm_end + 3:].lstrip("\n")
    synthesis_path.write_text(fm_raw + "\n" + body, encoding="utf-8")
    body_path.unlink()


def recover_orphan_synthesis_bodies(concepts: list[dict]) -> int:
    """Merge any orphaned synthesis_body.md files into their synthesis.md.

    Returns the count of recovered concepts.
    """
    recovered = 0
    for c in concepts:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        synthesis_path = out_dir / "synthesis.md"
        body_path = out_dir / "synthesis_body.md"
        if not synthesis_path.exists() or not body_path.exists():
            continue
        # Only merge if synthesis.md still looks like a frontmatter stub (i.e.
        # the merge from a prior synthesize run was interrupted).
        text = synthesis_path.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n.*?\n---\s*\n?$", text, re.DOTALL)
        if not m:
            # synthesis.md already has body content; leave both files alone.
            continue
        _merge_synthesis_body(synthesis_path, body_path)
        recovered += 1
        print(f"  recovered {cid} (merged orphan synthesis_body.md)")
    return recovered


def cmd_score(concepts: list[dict], args: argparse.Namespace) -> None:
    """Append Section 8 (LCOE Downselect Scoring) to syntheses that lack it."""
    targets = resolve_concepts(
        args.concepts, concepts,
        family=args.family,
        all_remaining=args.all_remaining,
    )
    if not targets:
        print("No concepts specified.")
        return

    # Gather approved prior syntheses for cross-concept context
    prior_syntheses = find_approved_syntheses()

    scored = 0
    skipped = 0
    failed = 0
    failures = []
    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        synthesis_path = out_dir / "synthesis.md"
        analysis_path = out_dir / "analysis.md"
        gap_report_path = out_dir / "gap_report.md"
        model_setup_path = out_dir / "model_setup.py"
        model_output_path = out_dir / "model_output.txt"

        if not synthesis_path.exists():
            print(f"  skip {cid} (no synthesis.md — run synthesize first)")
            skipped += 1
            continue

        if has_section8(synthesis_path) and not args.force:
            print(f"  skip {cid} (Section 8 exists, use --force to re-score)")
            skipped += 1
            continue

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md)")
            skipped += 1
            continue

        # Format approved prior syntheses (exclude current concept)
        synth_list = [s for s in prior_syntheses if s.parent.name != cid]
        if synth_list:
            approved_syntheses = format_path_list(synth_list)
        else:
            approved_syntheses = "(none yet — this is among the first syntheses)"

        score_body_path = out_dir / "score_body.md"

        template_text = (TEMPLATES_DIR / "score.md").read_text(encoding="utf-8")
        prompt_text = fill_template(template_text, {
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "concept_id": cid,
            "synthesis_path": str(synthesis_path),
            "analysis_path": str(analysis_path),
            "gap_report_path": str(gap_report_path) if gap_report_path.exists() else "",
            "model_setup_path": str(model_setup_path) if model_setup_path.exists() else "",
            "model_output_path": str(model_output_path) if model_output_path.exists() else "",
            "approved_syntheses": approved_syntheses,
            "output_path": str(score_body_path),
        })

        ctx = prepare_step(
            step_label="score",
            concept_id=cid,
            prompt_text=prompt_text,
            prompt_path=out_dir / "prompts" / "score_prompt.md",
            out_dir=out_dir,
            dry_run=args.dry_run,
            force=args.force,
        )
        if not ctx.proceed:
            continue

        result = invoke_claude_validated(
            ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
            timeout=args.timeout, model=args.model,
            validator=validate_score_output,
            output_path=score_body_path,
            step_label="score",
        )
        elapsed = time.time() - ctx.start_time

        if result.invoke.returncode != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
            print(f"    stderr: {result.invoke.stderr[:500]}", file=sys.stderr)
            failed += 1
            failures.append(f"{cid}: rc={result.invoke.returncode}")
            continue

        if not result.validation_passed:
            reason = ""
            if result.log_entries:
                reason = f" — {result.log_entries[-1].get('details', '')}"
            print(f" FAILED ({elapsed:.0f}s) — score validation exhausted{reason}")
            failed += 1
            failures.append(f"{cid}: validation failed{reason}")
            continue

        # Append Section 8 to synthesis.md
        existing = synthesis_path.read_text(encoding="utf-8").rstrip("\n")
        section8 = score_body_path.read_text(encoding="utf-8")
        # Strip any frontmatter Claude may have added
        if section8.startswith("---"):
            fm_end = section8.find("---", 3)
            if fm_end != -1:
                section8 = section8[fm_end + 3:].lstrip("\n")
        synthesis_path.write_text(existing + "\n\n" + section8 + "\n", encoding="utf-8")
        score_body_path.unlink()
        scored += 1
        size = len(synthesis_path.read_text(encoding="utf-8"))
        print(f" done ({elapsed:.0f}s, {size} chars)")

    print(f"\nScored: {scored}, Skipped: {skipped}, Failed: {failed}")
    if failures:
        print("Failures:")
        for f in failures:
            print(f"  - {f}")


def cmd_extract_scores(concepts: list[dict], args: argparse.Namespace) -> None:
    """Extract YAML scores from synthesis files and compute C2, C6, C7."""
    # Recover any orphaned synthesis_body.md files (interrupted synthesize runs).
    recovered = recover_orphan_synthesis_bodies(concepts)
    if recovered:
        print(f"Recovered {recovered} orphan synthesis bodies before extraction.\n")

    scores, warnings = build_verified_scores(concepts, ANALYSES_DIR)

    for w in warnings:
        print(f"  warn: {w}")

    if not scores:
        print("No concepts with extractable scores found.")
        return

    SCORES_DIR.mkdir(parents=True, exist_ok=True)
    json_path = SCORES_DIR / "verified_scores.json"
    md_path = SCORES_DIR / "verified_scores.md"

    write_verified_json(scores, json_path)
    write_verified_md(scores, md_path)

    print(f"\nExtracted scores for {len(scores)} concepts.")
    print(f"  {json_path}")
    print(f"  {md_path}")

    # Print summary table
    print(f"\n{'Concept':<45} C1   C2   C3   C4   C5   C6   C7   C8")
    print("-" * 95)
    for s in scores:
        print(
            f"{s['concept_id']:<45} "
            f"{s['C1']:.1f}  {s['C2']:.1f}  {s['C3']:.1f}  {s['C4']:.1f}  "
            f"{s['C5']:.1f}  {s['C6']:.1f}  {s['C7']:.1f}  {s['C8']:.1f}"
        )


def cmd_calibrate(concepts: list[dict], args: argparse.Namespace) -> None:
    """Cross-concept calibration of scores via Claude."""
    verified_md = SCORES_DIR / "verified_scores.md"
    if not verified_md.exists():
        print("Error: verified_scores.md not found. Run extract-scores first.")
        sys.exit(1)

    verified_table = verified_md.read_text(encoding="utf-8")

    # Build concept file paths for the calibration prompt
    concept_paths_lines = []
    for c in concepts:
        cid = c["_id"]
        synth = ANALYSES_DIR / cid / "synthesis.md"
        analysis = ANALYSES_DIR / cid / "analysis.md"
        if synth.exists():
            concept_paths_lines.append(f"- **{cid}**")
            concept_paths_lines.append(f"  - Synthesis: `{synth}`")
            if analysis.exists():
                concept_paths_lines.append(f"  - Analysis: `{analysis}`")
    concept_file_paths = "\n".join(concept_paths_lines)

    calibration_body_path = SCORES_DIR / "calibration_body.md"

    template_text = (TEMPLATES_DIR / "calibrate.md").read_text(encoding="utf-8")
    prompt_text = fill_template(template_text, {
        "verified_scores_table": verified_table,
        "concept_file_paths": concept_file_paths,
        "output_path": str(calibration_body_path),
    })

    SCORES_DIR.mkdir(parents=True, exist_ok=True)
    prompt_path = SCORES_DIR / "calibration_prompt.md"

    ctx = prepare_step(
        step_label="calibrate",
        concept_id="all",
        prompt_text=prompt_text,
        prompt_path=prompt_path,
        out_dir=SCORES_DIR,
        dry_run=args.dry_run,
        force=True,  # always re-run calibration
    )
    if not ctx.proceed:
        return

    result = invoke_claude_validated(
        ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
        validator=validate_calibration_output,
        output_path=calibration_body_path,
        step_label="calibrate",
    )
    elapsed = time.time() - ctx.start_time

    if result.invoke.returncode != 0:
        print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
        print(f"    stderr: {result.invoke.stderr[:500]}", file=sys.stderr)
        return

    if not result.validation_passed:
        print(f" FAILED ({elapsed:.0f}s) — calibration validation exhausted")
        return

    # Parse calibrated scores and adjustments
    body_text = calibration_body_path.read_text(encoding="utf-8")
    calibrated = parse_calibrated_table(body_text)
    adjustments = parse_adjustments(body_text)

    if not calibrated:
        print(f" FAILED ({elapsed:.0f}s) — could not parse calibrated score table")
        return

    # Write outputs
    cal_json_path = SCORES_DIR / "calibrated_scores.json"
    cal_json_path.write_text(
        json.dumps({"scores": calibrated, "adjustments": adjustments}, indent=2),
        encoding="utf-8",
    )

    # Write calibrated markdown (keep the raw body)
    cal_md_path = SCORES_DIR / "calibrated_scores.md"
    cal_md_path.write_text(body_text, encoding="utf-8")
    calibration_body_path.unlink()

    print(f" done ({elapsed:.0f}s, {len(calibrated)} concepts calibrated, "
          f"{len(adjustments)} adjustments)")
    print(f"  {cal_json_path}")
    print(f"  {cal_md_path}")


def cmd_heatmap(concepts: list[dict], args: argparse.Namespace) -> None:
    """Generate HTML heatmap from calibrated scores."""
    cal_json_path = SCORES_DIR / "calibrated_scores.json"
    if not cal_json_path.exists():
        print("Error: calibrated_scores.json not found. Run calibrate first.")
        sys.exit(1)

    data = json.loads(cal_json_path.read_text(encoding="utf-8"))
    calibrated = data.get("scores", [])
    adjustments = data.get("adjustments", [])

    if not calibrated:
        print("Error: no calibrated scores found in JSON.")
        sys.exit(1)

    output_path = CONCEPT_ANALYSIS_DIR / "heatmap.html"
    generate_heatmap_html(
        calibrated_scores=calibrated,
        adjustments=adjustments,
        output_path=output_path,
        analyses_dir=ANALYSES_DIR,
        concepts=concepts,
    )

    print(f"Heatmap generated: {output_path}")
    print(f"  {len(calibrated)} concepts scored")


# ---------------------------------------------------------------------------
# init-tables — coverage validation gate (read-only; does not generate)
# ---------------------------------------------------------------------------

_CONCEPT_DIR_RE = re.compile(r"^\d+[a-z]?-")


def _csv_ids(path: Path) -> set[str]:
    """Return the set of ``concept_id`` values in a table CSV (empty if absent)."""
    if not Path(path).exists():
        return set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {row["concept_id"].strip() for row in csv.DictReader(f)
                if row.get("concept_id", "").strip()}


def _disk_concept_ids(research_dir: Path) -> set[str]:
    """Concept directories under ``research_dir`` (filtered to the slug grammar)."""
    if not Path(research_dir).exists():
        return set()
    return {d.name for d in Path(research_dir).iterdir()
            if d.is_dir() and _CONCEPT_DIR_RE.match(d.name)}


def _validate_tables(
    research_dir: Path,
    ontology_path: Path,
    archetype_fit_path: Path,
    comparables_path: Path,
    design_point_path: Path,
    freeform_routes_path: Path,
) -> tuple[list[str], list[str]]:
    """Validate table coverage. Returns ``(errors, summary_lines)``.

    Strict (errors → non-zero exit):
      * all four table CSVs exist;
      * every on-disk concept dir appears in ontology.csv AND archetype_fit.csv;
      * no ontology/archetype_fit row references a concept with no dir;
      * comparables.csv / design_point.csv reference only known concepts.

    Warning-only (summary, never fails): design-point coverage — pending rows are
    expected while Item 5's batch runs.
    """
    errors: list[str] = []
    summary: list[str] = []

    missing_files = [str(p) for p in
                     (ontology_path, archetype_fit_path, comparables_path, design_point_path)
                     if not Path(p).exists()]
    if missing_files:
        return [f"missing table file: {p}" for p in missing_files], summary

    disk = _disk_concept_ids(research_dir)
    ont_ids = _csv_ids(ontology_path)
    af_ids = _csv_ids(archetype_fit_path)
    comp_ids = _csv_ids(comparables_path)
    dp_ids = _csv_ids(design_point_path)

    for cid in sorted(disk - ont_ids):
        errors.append(f"concept dir not in ontology.csv: {cid}")
    for cid in sorted(disk - af_ids):
        errors.append(f"concept dir not in archetype_fit.csv: {cid}")
    for cid in sorted(ont_ids - disk):
        errors.append(f"ontology.csv row has no concept dir: {cid}")
    for cid in sorted(af_ids - disk):
        errors.append(f"archetype_fit.csv row has no concept dir: {cid}")
    for cid in sorted(comp_ids - ont_ids):
        errors.append(f"comparables.csv references unknown concept: {cid}")
    for cid in sorted(dp_ids - ont_ids):
        errors.append(f"design_point.csv references unknown concept: {cid}")

    # Coverage summary (warning-only). Mappable = fit_grade != None.
    mappable: set[str] = set()
    if Path(archetype_fit_path).exists():
        with open(archetype_fit_path, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                cid = row.get("concept_id", "").strip()
                if cid and (row.get("fit_grade", "").strip() != "None"):
                    mappable.add(cid)
    freeform = load_freeform_routes() if Path(freeform_routes_path) == Path(FREEFORM_ROUTES_PATH) \
        else _freeform_from(freeform_routes_path)
    pending = mappable - dp_ids - freeform
    summary.append(
        f"design-point coverage: {len(dp_ids & mappable)}/{len(mappable)} mappable "
        f"concepts have a row; {len(pending)} pending; {len(freeform)} judged-freeform "
        f"(freeform-routes file {'present' if Path(freeform_routes_path).exists() else 'absent'})"
    )
    if pending:
        summary.append("  pending: " + ", ".join(sorted(pending)))
    return errors, summary


def _freeform_from(path: Path) -> set[str]:
    """Parse freeform concept_ids from an arbitrary path (test-injection helper)."""
    if not Path(path).exists():
        return set()
    text = Path(path).read_text(encoding="utf-8")
    return set(re.findall(r"\b(\d{2}[a-z]?-[a-z][a-z0-9-]+)", text))


def cmd_init_tables(_records: list[dict], _args: argparse.Namespace) -> None:
    """Validate the four tables exist and cover every concept (read-only)."""
    errors, summary = _validate_tables(
        RESEARCH_DIR, ONTOLOGY_PATH, ARCHETYPE_FIT_PATH,
        COMPARABLES_PATH, DESIGN_POINT_PATH, FREEFORM_ROUTES_PATH,
    )
    for line in summary:
        print(line)
    if errors:
        print(f"\ninit-tables FAILED — {len(errors)} coverage error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    print("init-tables OK — ontology + archetype_fit cover every concept dir.")


# ---------------------------------------------------------------------------
# regenerate-concept — delete-and-rebuild sequencer (four-state-aware guard)
# ---------------------------------------------------------------------------

# Artifacts removed before a real regeneration (relative to analyses/<id>/).
_REGEN_RM_FILES = [
    "analysis.md", "model_setup.py", "model_output.txt",
    "synthesis.md", "review.md", "address_log.md", "research_log.json",
]
_REGEN_RM_DIRS = ["prompts"]  # iter-* handled separately by glob

_REGEN_STAGES = ["analyze", "model-setup", "review", "synthesize", "score", "approve"]


def _regen_refusal_reason(record: dict) -> str | None:
    """Return a state-specific refusal reason, or None if the concept is runnable."""
    if is_costingfe_runnable(record):
        return None
    status = get_comparison_status(record)
    if status == "freeform-deferred":
        if record.get("fit_grade") == "None":
            return "fit_grade=None — freeform, out of scope to model (Item 11)"
        return ("freeform by judgment (listed in design_point_freeform_routes.md) — "
                "out of scope to model (Item 11)")
    if status == "pending-design-point":
        return ("pending-design-point — design-point row missing in Item 5's batch; "
                "populate design_point.csv first")
    return f"not costingfe-runnable (comparison-status={status})"


def _regen_namespace(cid: str) -> argparse.Namespace:
    """A Namespace that drives a single-concept stage run with re-run forced."""
    return argparse.Namespace(
        concepts=[cid], family=None, all_remaining=False,
        model="sonnet", timeout=900, dry_run=False, force=True,
        max_passes=3, add_passes=None, feedback=None, resume=False,
        research=False, max_research_searches=5, max_research_extractions=3,
        skip_review_gate=False,
    )


def cmd_regenerate_concept(records: list[dict], args: argparse.Namespace) -> None:
    """Delete prior artifacts and re-run the costingfe stage chain for one concept.

    Hard-requires an ``archetype_fit.csv`` row (the concept must resolve to a
    record) and refuses unless ``is_costingfe_runnable`` with a state-specific
    reason. ``--dry-run`` prints the stage sequence and writes a temp frontmatter
    (verifying table → record → frontmatter wiring end-to-end) without deleting
    anything or invoking an LLM — the Item 6 acceptance boundary.
    """
    matches = resolve_one(records, args.concept)
    if not matches:
        raise ValueError(
            f"No concept matching '{args.concept}' — needs an archetype_fit.csv row")
    if len(matches) > 1:
        detail = ", ".join(m["concept_id"] for m in matches)
        raise ValueError(f"Ambiguous '{args.concept}' matched: {detail}")
    record = matches[0]
    cid = record["concept_id"]

    reason = _regen_refusal_reason(record)
    if reason is not None:
        print(f"regenerate-concept refuses {cid}: {reason}", file=sys.stderr)
        sys.exit(1)

    stages = ([] if args.keep_gap_report else ["gap-check"]) + _REGEN_STAGES

    if args.dry_run:
        print(f"regenerate-concept {cid} (DRY RUN) — comparison-status="
              f"{get_comparison_status(record)}")
        print("  stage sequence:")
        for s in stages:
            print(f"    - {s}")
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as tf:
            tf.write(make_frontmatter(record))
            tmp_path = tf.name
        print(f"  wrote temp frontmatter (wiring check): {tmp_path}")
        return

    # Real run: delete prior artifacts, then sequence the stages directly.
    concept_dir = ANALYSES_DIR / cid
    rm_files = list(_REGEN_RM_FILES)
    if not args.keep_gap_report:
        rm_files.append("gap_report.md")
    for name in rm_files:
        (concept_dir / name).unlink(missing_ok=True)
    for d in _REGEN_RM_DIRS:
        shutil.rmtree(concept_dir / d, ignore_errors=True)
    for itd in concept_dir.glob("iter-*"):
        shutil.rmtree(itd, ignore_errors=True)

    ns = _regen_namespace(cid)
    if not args.keep_gap_report:
        cmd_gap_check(records, ns)
    cmd_analyze(records, ns)
    cmd_model_setup(records, ns)
    cmd_review(records, ns)
    cmd_synthesize(records, ns)
    cmd_score(records, ns)
    cmd_approve(records, ns)
    print(f"regenerate-concept {cid}: complete.")


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
    p_analyze.add_argument("--add-passes", type=int, default=None, metavar="N",
                            help="Run N additional passes from each concept's current iteration "
                                 "(implies --resume; works across concepts at different iterations)")
    p_analyze.add_argument("--feedback", type=Path, metavar="PATH",
                            help="Use file as pre_feedback.md for next iter "
                                 "(requires existing analysis.md; implies --resume; "
                                 "runs full analyze→model_setup→assess)")
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
    p_ms.add_argument("--feedback", type=Path, default=None,
                      help="Feedback file with model-targeted findings (### F-N: format)")

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
    p_syn.add_argument("--skip-review-gate", action="store_true",
                       help="Synthesize even if analysis hasn't been reviewed")

    # -- approve --
    p_approve = sub.add_parser("approve", help="Approve a reviewed analysis")
    p_approve.add_argument("concepts", nargs="+", help="Concept IDs to approve")
    p_approve.add_argument("--force", action="store_true", help="Approve even without synthesis")

    # -- add-source --
    p_add = sub.add_parser("add-source", help="Add a PDF or URL source to a concept")
    p_add.add_argument("concept", help="Concept ID (single concept)")
    p_add.add_argument("source", help="PDF path or URL to extract")
    p_add.add_argument("--name", help="Override automatic source name")
    p_add.add_argument("--force", action="store_true",
                       help="Re-extract even if source name already exists")
    p_add.add_argument("--dry-run", action="store_true", help="Show what would be created")

    # -- score --
    p_score = sub.add_parser("score", help="Add Section 8 (LCOE Downselect Scoring) to syntheses")
    p_score.add_argument("concepts", nargs="*", default=[], help="Concept IDs")
    p_score.add_argument("--all", dest="all_remaining", action="store_true", help="All concepts with syntheses")
    p_score.add_argument("--family", help="Filter by confinement family")
    p_score.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_score.add_argument("--dry-run", action="store_true", help="Generate prompts without calling Claude")
    p_score.add_argument("--timeout", type=int, default=1200, help="Per-invocation timeout in seconds (default: 1200)")
    p_score.add_argument("--force", action="store_true", help="Re-score even if Section 8 exists")

    # -- extract-scores --
    p_extract = sub.add_parser("extract-scores", help="Extract YAML scores and compute C2, C6, C7")

    # -- calibrate --
    p_calibrate = sub.add_parser("calibrate", help="Cross-concept score calibration via Claude")
    p_calibrate.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
    p_calibrate.add_argument("--dry-run", action="store_true", help="Generate prompt without calling Claude")
    p_calibrate.add_argument("--timeout", type=int, default=3600, help="Timeout in seconds (default: 3600)")

    # -- heatmap --
    p_heatmap = sub.add_parser("heatmap", help="Generate HTML heatmap from calibrated scores")

    # -- init-tables --
    sub.add_parser("init-tables",
                   help="Validate the four upstream tables exist and cover every concept")

    # -- regenerate-concept --
    p_regen = sub.add_parser(
        "regenerate-concept",
        help="Delete prior artifacts and re-run the costingfe stage chain for one concept")
    p_regen.add_argument("concept", help="Concept ID (must have an archetype_fit.csv row)")
    p_regen.add_argument("--dry-run", action="store_true",
                         help="Print the stage sequence and verify wiring; no rm, no LLM")
    p_regen.add_argument("--keep-gap-report", action="store_true",
                         help="Skip gap-check and preserve the existing gap_report.md")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

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
        "add-source": cmd_add_source,
        "score": cmd_score,
        "extract-scores": cmd_extract_scores,
        "calibrate": cmd_calibrate,
        "heatmap": cmd_heatmap,
        "init-tables": cmd_init_tables,
        "regenerate-concept": cmd_regenerate_concept,
    }

    # Loader dispatch split (design.md "CLI dispatch split"). Orchestrator
    # handlers consume the four-table ConceptRecords; scoring/heatmap handlers
    # consume legacy-only architecture columns (Fuel, MFE Topology, …) that the
    # new tables intentionally do not carry — passing records there would
    # silently zero every scoring derivation. Not a superset; do not unify.
    LEGACY_TABLE_COMMANDS = {"score", "calibrate", "extract-scores", "heatmap"}
    if args.command in LEGACY_TABLE_COMMANDS:
        data = load_legacy_table()
    else:
        data = load_concepts()

    handler = dispatch[args.command]
    try:
        handler(data, args)
    except ValueError as exc:
        # Library code (resolve_concepts, resolve_source_names) raises
        # ValueError on user-facing errors. The CLI layer owns the exit
        # contract — print a clean message and exit non-zero rather than
        # surfacing a stack trace.
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
