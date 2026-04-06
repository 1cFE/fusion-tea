"""Stage 1 loop runner: assess↔analyze with in-loop model-setup.

Extracts the iteration loop from cmd_analyze into a dedicated module with:
- Per-iteration directories (iter-N/)
- Structured verdicts (verdict.json)
- Substitutable feedback-producers (assess, source-integration, research)
- In-loop model-setup (FR-6)
- Resume semantics (FR-9)
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import time
from pathlib import Path

from lib.claude import invoke_claude, invoke_claude_validated, run_model
from lib.concepts import get_costingfe_mapping, get_model_path, FUEL_MAPPING
from lib.frontmatter import make_frontmatter, parse_frontmatter
from lib.iteration import (
    clear_iterations,
    detect_new_sources,
    parse_verdict_from_feedback,
    read_loop_state,
    write_verdict,
)
from lib.paths import (
    ANALYSES_DIR,
    CONCEPT_ANALYSIS_DIR,
    COSTINGFE_CONSTANTS_PATH,
    COSTINGFE_DEFAULTS_DIR,
    COSTINGFE_EXAMPLES_DIR,
    COSTINGFE_README_PATH,
    FREEFORM_EXEMPLAR_PATH,
    TEMPLATES_DIR,
)
from lib.sources import find_sources, format_source_list
from lib.state import propagate_staleness
from lib.templating import fill_template


def run_stage1_loop(
    concept: dict,
    args: argparse.Namespace,
    *,
    resume: bool = False,
    common_vars: dict,
    analysis_template: str,
    assessment_template: str,
) -> str:
    """Run the stage1 loop for one concept. Returns final verdict string.

    The loop body per iteration is:
      [feedback-producer] → analyze(cold_start or feedback_pass) → model-setup → assess

    Feedback-producers are substitutable: assess output (normal), source-integration
    (after add-source), or research (future, FR-A3).
    """
    cid = concept["_id"]
    rid = concept["_research_id"]
    concept_dir = ANALYSES_DIR / cid
    analysis_path = concept_dir / "analysis.md"
    max_passes = args.max_passes

    # Defensive copy — loop mutates source_paths each iteration (FR-12)
    common_vars = dict(common_vars)

    # 1. Handle --force: clean slate
    if args.force:
        deleted = clear_iterations(concept_dir)
        if deleted:
            print(f"  {cid}: cleared {deleted} prior iteration(s)")

    # 2. Read existing iteration state
    loop_state = read_loop_state(concept_dir)

    # 3. Determine start iteration
    if resume:
        start_iter = loop_state.next_iteration
        if start_iter > max_passes:
            print(f"  {cid}: max passes reached ({max_passes})")
            return loop_state.iterations[-1].verdict if loop_state.iterations else "NONE"
    else:
        start_iter = 1

    # 4. Detect new sources (for feedback-producer selection on resume)
    current_sources = find_sources(rid)
    new_sources = detect_new_sources(loop_state, current_sources) if resume else []
    used_source_integration = False
    used_review_feedback = False

    verdict = "NONE"

    for iter_num in range(start_iter, max_passes + 1):
        iter_dir = concept_dir / f"iter-{iter_num}"
        iter_dir.mkdir(parents=True, exist_ok=True)

        # --- Refresh sources each iteration (FR-12) ---
        current_sources = find_sources(rid)
        common_vars["source_paths"] = format_source_list(current_sources)

        # --- Select and run feedback-producer (FR-16) ---
        feedback_source = "cold_start"
        feedback_path = None
        merged_assess = False

        if iter_num == 1 and not resume:
            # Cold start — no feedback producer
            feedback_source = "cold_start"
        elif not used_review_feedback and _has_revise_status(analysis_path):
            # Review kick-back (FR-6): one-shot, fires once then falls through
            used_review_feedback = True
            feedback_text = _get_review_feedback(concept_dir)
            if feedback_text is not None:
                feedback_source = "review"
                feedback_path = iter_dir / "feedback.md"
                feedback_path.write_text(feedback_text, encoding="utf-8")
                print(f"  {cid} iter {iter_num}: using review corrective actions as feedback")
            else:
                # review.md exists but no extractable F-N findings — fall through
                feedback_source = "assess"
                feedback_path = _get_prior_feedback(concept_dir, iter_num)
        elif new_sources and not used_source_integration:
            # Source-integration producer (FR-17)
            feedback_source = "source_integration"
            feedback_path = _run_source_integration(
                concept, iter_dir, new_sources, analysis_path, args)
            if feedback_path is None:
                # Source integration found PASS (no material additions)
                # Fall through to normal assess feedback
                feedback_source = "assess"
                feedback_path = _get_prior_feedback(concept_dir, iter_num)
            used_source_integration = True
        elif getattr(args, "research", False) and iter_num > 1:
            feedback_source = "research"
            from lib.research import run_research_step
            acquired = run_research_step(concept, iter_dir, args)

            # Refresh sources after research (FR-15) — must happen before
            # source-integration so it can see the new files
            current_sources = find_sources(rid)
            common_vars["source_paths"] = format_source_list(current_sources)

            if acquired:
                # Chain to source-integration for rich feedback (FR-10)
                si_path = _run_source_integration(
                    concept, iter_dir, acquired, analysis_path, args)
                if si_path is not None:
                    # Merge with prior assess findings so they aren't dropped (FR-8)
                    assess_fb = _get_prior_feedback(concept_dir, iter_num)
                    merged_assess = assess_fb is not None and assess_fb.exists()
                    feedback_path = _merge_feedback(
                        assess_fb, si_path, iter_dir / "feedback.md")
                else:
                    # Source integration found PASS — use assess feedback as-is
                    feedback_source = "assess"
                    feedback_path = _get_prior_feedback(concept_dir, iter_num)
            else:
                # Nothing acquired — fall through to assess
                feedback_source = "assess"
                feedback_path = _get_prior_feedback(concept_dir, iter_num)
        else:
            # Normal: prior iteration's assess output
            feedback_source = "assess" if iter_num > 1 else "cold_start"
            feedback_path = _get_prior_feedback(concept_dir, iter_num) if iter_num > 1 else None

        # --- Analyze step ---
        if feedback_source == "cold_start":
            ok = _run_cold_start(concept, iter_dir, common_vars,
                                 analysis_template, analysis_path, args)
            if not ok:
                write_verdict(iter_dir, iteration=iter_num, verdict="ERROR",
                              finding_count=0, feedback_source=feedback_source,
                              model_ran=False, model_ok=False, research_ran=False,
                              sources=[str(p) for p in current_sources])
                return "ERROR"
        else:
            ok = _run_feedback_pass(concept, iter_dir, feedback_path, common_vars,
                                    analysis_template, args)
            if not ok:
                write_verdict(iter_dir, iteration=iter_num, verdict="ERROR",
                              finding_count=0, feedback_source=feedback_source,
                              model_ran=False, model_ok=False, research_ran=False,
                              sources=[str(p) for p in current_sources])
                return "ERROR"

        # --- Capture iteration output (FR-4) ---
        _capture_analysis_output(analysis_path, iter_dir)

        # --- Model-setup inside loop (FR-6) ---
        model_ran, model_ok = _run_model_in_iteration(concept, iter_dir, args, feedback_path)

        # --- Update canonical model files (FR-5) ---
        _update_canonical_files(concept_dir, iter_dir)

        # --- Skip assess if max_passes is 1 (current behavior) ---
        if max_passes <= 1:
            write_verdict(iter_dir, iteration=iter_num, verdict="SINGLE_PASS",
                          finding_count=0, feedback_source=feedback_source,
                          model_ran=model_ran, model_ok=model_ok,
                          research_ran=(feedback_source == "research"),
                          sources=[str(p) for p in current_sources])
            return "SINGLE_PASS"

        # --- Assess step ---
        verdict, finding_count = _run_assess(
            concept, iter_dir, analysis_path, assessment_template, args)

        # --- Write verdict.json (FR-3, FR-19) ---
        write_verdict(iter_dir, iteration=iter_num, verdict=verdict,
                      finding_count=finding_count, feedback_source=feedback_source,
                      model_ran=model_ran, model_ok=model_ok,
                      research_ran=(feedback_source == "research"),
                      sources=[str(p) for p in current_sources],
                      merged_assess=merged_assess)

        # --- Propagate staleness ---
        propagate_staleness(cid, f"analysis-updated-iter-{iter_num}")

        if verdict == "PASS":
            return "PASS"

        # Last allowed pass?
        if iter_num >= max_passes:
            print(f"  warn: {cid} did not converge in {max_passes} passes")
            return verdict

    return verdict


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _split_findings(text: str) -> list[str]:
    """Split feedback text into individual F-N finding blocks.

    Returns a list of stripped finding blocks (each starting with '### F-N:').
    Non-finding preamble (VERDICT line, etc.) is excluded.
    """
    from lib.validators import FINDING_HEADER_RE

    parts = re.split(r"(?=^### F-\d+:)", text, flags=re.MULTILINE)
    return [p.strip() for p in parts if FINDING_HEADER_RE.match(p)]


def _extract_model_findings(feedback_path: Path | None) -> str:
    """Extract model-targeted findings from a feedback file.

    Returns formatted text of model-targeted findings, or empty string
    if none exist. Findings without a Category field default to 'analysis'
    (backward compatibility).
    """
    from lib.validators import FINDING_CATEGORY_RE

    if feedback_path is None or not feedback_path.exists():
        return ""

    text = feedback_path.read_text(encoding="utf-8")
    finding_blocks = _split_findings(text)

    model_findings = []
    for block in finding_blocks:
        cat_match = FINDING_CATEGORY_RE.search(block)
        if cat_match and cat_match.group(1) == "model":
            model_findings.append(block.strip())

    return "\n\n".join(model_findings)


def _merge_feedback(
    assess_feedback_path: Path | None,
    source_integration_path: Path,
    output_path: Path,
) -> Path:
    """Merge carried-forward assess findings with source-integration output.

    Writes a combined feedback file to output_path. The source-integration
    output is the primary content; assess findings are carried forward
    under a separate header so the analysis agent can distinguish them.

    Returns output_path (always — even if no assess findings to carry).
    """
    si_text = source_integration_path.read_text(encoding="utf-8")

    if assess_feedback_path is None or not assess_feedback_path.exists():
        output_path.write_text(si_text, encoding="utf-8")
        return output_path

    assess_text = assess_feedback_path.read_text(encoding="utf-8")
    assess_verdict, assess_count = parse_verdict_from_feedback(assess_text)

    if assess_verdict == "PASS" or assess_count == 0:
        output_path.write_text(si_text, encoding="utf-8")
        return output_path

    assess_findings = _split_findings(assess_text)

    merged = si_text.rstrip() + "\n\n"
    merged += "---\n\n"
    merged += "## Carried-Forward Assessment Findings\n\n"
    merged += (
        "The following findings were flagged by the prior assessment but have not "
        "yet been addressed (they were carried forward across a source-integration "
        "pass). Address these alongside the source-integration findings above.\n\n"
    )
    merged += "\n\n".join(assess_findings)
    merged += "\n"

    output_path.write_text(merged, encoding="utf-8")
    return output_path


def _run_cold_start(
    concept: dict,
    iter_dir: Path,
    common_vars: dict,
    template: str,
    analysis_path: Path,
    args: argparse.Namespace,
) -> bool:
    """Run cold-start analysis (iteration 1). Returns True on success.

    Extracted from run_analysis.py:334-386.
    """
    cid = concept["_id"]
    body_path = iter_dir / "analysis_body.md"

    prompt = fill_template(template, {
        **common_vars,
        "output_path": str(body_path),
        "cold_start": "true",
        "feedback_pass": "",
        "feedback_path": "",
        "self_advance": "",
    })

    prompt_path = iter_dir / "analyze_prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    if args.dry_run:
        print(f"  dry-run {cid}: cold-start prompt saved to {prompt_path}")
        return True

    # Pre-write analysis.md with frontmatter
    analysis_path.write_text(make_frontmatter(concept), encoding="utf-8")

    print(f"  analyze {cid} iter 1 (cold start) ...", end="", flush=True)
    t0 = time.time()
    _stdout, stderr, rc = invoke_claude(
        prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
    )
    elapsed = time.time() - t0

    if rc != 0:
        print(f" FAILED ({elapsed:.0f}s, rc={rc})")
        print(f"    stderr: {stderr[:500]}", file=sys.stderr)
        analysis_path.unlink(missing_ok=True)
        return False

    if not body_path.exists():
        print(f" FAILED ({elapsed:.0f}s) — Claude did not write {body_path}")
        analysis_path.unlink(missing_ok=True)
        return False

    # Assemble: read back frontmatter (Claude may have updated Reuses) + body
    fm_raw = analysis_path.read_text(encoding="utf-8").rstrip("\n") + "\n"
    body = body_path.read_text(encoding="utf-8")
    analysis_path.write_text(fm_raw + "\n" + body, encoding="utf-8")
    body_path.unlink()
    print(f" done ({elapsed:.0f}s, {len(body)} chars)")
    return True


def _run_feedback_pass(
    concept: dict,
    iter_dir: Path,
    feedback_path: Path,
    common_vars: dict,
    template: str,
    args: argparse.Namespace,
) -> bool:
    """Run feedback-pass analysis (iteration N>1). Returns True on success.

    Extracted from run_analysis.py:440-472.
    feedback_path must be a valid path — callers are responsible for ensuring
    the prior iteration's feedback.md exists before invoking feedback-pass.
    """
    cid = concept["_id"]
    iter_num = int(iter_dir.name.split("-")[1])

    prompt = fill_template(template, {
        **common_vars,
        "output_path": "",  # not used in feedback mode
        "cold_start": "",
        "feedback_pass": "true",
        "feedback_path": str(feedback_path),
        "self_advance": "",
    })

    prompt_path = iter_dir / "analyze_prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    if args.dry_run:
        print(f"  dry-run {cid}: feedback-pass prompt saved to {prompt_path}")
        return True

    max_passes = args.max_passes
    print(f"  analyze {cid} iter {iter_num}/{max_passes} (feedback pass) ...",
          end="", flush=True)
    t0 = time.time()
    _stdout, stderr, rc = invoke_claude(
        prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
    )
    elapsed = time.time() - t0

    if rc != 0:
        print(f" FAILED ({elapsed:.0f}s, rc={rc})")
        print(f"    stderr: {stderr[:500]}", file=sys.stderr)
        return False

    print(f" done ({elapsed:.0f}s)")
    return True


def _capture_analysis_output(analysis_path: Path, iter_dir: Path) -> None:
    """Save the body of analysis.md (sans frontmatter) to iter-N/analysis_output.md.

    Creates the per-iteration audit trail without changing how Claude writes.
    """
    if not analysis_path.exists():
        return
    text = analysis_path.read_text(encoding="utf-8")
    # Strip frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            body = text[end + 3:].lstrip("\n")
        else:
            body = text
    else:
        body = text
    (iter_dir / "analysis_output.md").write_text(body, encoding="utf-8")


def _run_model_in_iteration(
    concept: dict,
    iter_dir: Path,
    args: argparse.Namespace,
    feedback_path: Path | None = None,
) -> tuple[bool, bool]:
    """Run model-setup inside the loop. Returns (model_ran, model_ok).

    Adapted from cmd_model_setup. Uses invoke_claude directly (not run_claude_step)
    because skip-if-exists logic doesn't apply inside the loop.
    Non-fatal on failure (FR-7).
    """
    cid = concept["_id"]
    model_script = iter_dir / "model_setup.py"
    model_output = iter_dir / "model_output.txt"

    if args.dry_run:
        print(f"  dry-run {cid}: model-setup would run in {iter_dir}")
        return False, False

    # Build model vars using shared helper
    model_feedback = _extract_model_findings(feedback_path)
    model_vars = build_model_vars(concept, model_script, iter_dir,
                                  model_feedback=model_feedback)
    if model_vars is None:
        return False, False

    template_name, vars_dict = model_vars
    template = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    prompt = fill_template(template, vars_dict)

    # Save prompt for audit trail
    (iter_dir / "model_setup_prompt.md").write_text(prompt, encoding="utf-8")

    print(f"    model-setup {cid} ...", end="", flush=True)
    t0 = time.time()
    _stdout, stderr, rc = invoke_claude(
        prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
    )
    elapsed = time.time() - t0

    if rc != 0:
        print(f" FAILED ({elapsed:.0f}s, rc={rc})")
        return False, False

    if not model_script.exists():
        print(f" FAILED ({elapsed:.0f}s) — no model_setup.py")
        return True, False

    print(f" done ({elapsed:.0f}s)", end="")

    # Run the model
    print(f" → running model ...", end="", flush=True)
    ok, msg = run_model(model_script, model_output)
    if ok:
        lcoe_match = re.search(r"LCOE:\s*([\d.]+)\s*\$/MWh", msg)
        lcoe_str = f" (LCOE={lcoe_match.group(1)} $/MWh)" if lcoe_match else ""
        print(f" ok{lcoe_str}")
        return True, True
    else:
        print(f" model FAILED: {msg}")
        return True, False


def build_model_vars(
    concept: dict,
    model_path: Path,
    iter_dir_or_out_dir: Path,
    *,
    standalone: bool = False,
    model_feedback: str = "",
) -> tuple[str, dict] | None:
    """Build template name and variables for model-setup.

    Shared by _run_model_in_iteration (in-loop) and cmd_model_setup (standalone).
    Returns (template_name, vars_dict) or None if analysis.md is missing.

    When standalone=True, iter_dir_or_out_dir is the concept dir itself and
    analysis.md is looked up directly within it. Otherwise it's an iter-N/ dir
    and analysis.md is in the parent.
    """
    if standalone:
        analysis_path = iter_dir_or_out_dir / "analysis.md"
    else:
        analysis_path = iter_dir_or_out_dir.parent / "analysis.md"

    if not analysis_path.exists():
        return None

    model_path_type = get_model_path(concept)
    if model_path_type == "costingfe":
        template_name = "model_setup_costingfe.md"
        mapping = get_costingfe_mapping(concept)
        vars_dict = {
            "concept_name": concept["Concept Name"],
            "company": concept.get("Company", ""),
            "analysis_path": str(analysis_path),
            "example_path": str(COSTINGFE_EXAMPLES_DIR / mapping["example"]),
            "defaults_path": str(COSTINGFE_DEFAULTS_DIR / mapping["defaults"]),
            "readme_path": str(COSTINGFE_README_PATH),
            "costing_constants_path": str(COSTINGFE_CONSTANTS_PATH),
            "costingfe_concept": mapping["concept"],
            "costingfe_fuel": FUEL_MAPPING.get(concept.get("Fuel", "D-T"), "DT"),
            "mapping_notes": mapping.get("notes", ""),
            "output_path": str(model_path),
            "model_feedback": model_feedback,
        }
    else:
        template_name = "model_setup_freeform.md"
        vars_dict = {
            "concept_name": concept["Concept Name"],
            "company": concept.get("Company", ""),
            "analysis_path": str(analysis_path),
            "costing_constants_path": str(COSTINGFE_CONSTANTS_PATH),
            "output_path": str(model_path),
            "model_feedback": model_feedback,
        }

    return template_name, vars_dict


def _run_assess(
    concept: dict,
    iter_dir: Path,
    analysis_path: Path,
    template: str,
    args: argparse.Namespace,
) -> tuple[str, int]:
    """Run the assessment step. Returns (verdict, finding_count).

    Extracted from run_analysis.py:394-432.
    """
    cid = concept["_id"]
    iter_num = int(iter_dir.name.split("-")[1])
    feedback_path = iter_dir / "feedback.md"

    model_output = iter_dir / "model_output.txt"
    assess_prompt = fill_template(template, {
        "concept_name": concept["Concept Name"],
        "analysis_path": str(analysis_path),
        "feedback_path": str(feedback_path),
        "model_output_path": str(model_output) if model_output.exists() else "",
    })

    (iter_dir / "assess_prompt.md").write_text(assess_prompt, encoding="utf-8")

    if args.dry_run:
        print(f"  dry-run {cid}: assess prompt saved to {iter_dir / 'assess_prompt.md'}")
        return "DRY_RUN", 0

    from lib.validators import validate_feedback_verdict

    print(f"  assess {cid} iter {iter_num} ...", end="", flush=True)
    t0 = time.time()
    result = invoke_claude_validated(
        assess_prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
        validator=validate_feedback_verdict,
        output_path=feedback_path,
        step_label="assess",
        log_path=iter_dir / "validation_log.json",
    )
    elapsed = time.time() - t0

    if result.invoke.returncode != 0:
        print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
        return "ERROR", 0

    if not feedback_path.exists():
        print(f" FAILED ({elapsed:.0f}s) — no feedback file")
        return "ERROR", 0

    feedback_text = feedback_path.read_text(encoding="utf-8")
    verdict, finding_count = parse_verdict_from_feedback(feedback_text)

    if verdict == "PASS":
        print(f" PASS ({elapsed:.0f}s)")
    else:
        suffix = ""
        if result.attempts > 1:
            suffix = f", {result.attempts} validation attempts"
        print(f" {finding_count} findings ({elapsed:.0f}s{suffix})")

    return verdict, finding_count


def _run_source_integration(
    concept: dict,
    iter_dir: Path,
    new_sources: list[Path],
    analysis_path: Path,
    args: argparse.Namespace,
) -> Path | None:
    """Run source-integration as feedback-producer. Returns output path or None if PASS.

    Extracted from cmd_update_analysis step 1 (run_analysis.py:1111-1158).
    """
    cid = concept["_id"]
    integration_template = (TEMPLATES_DIR / "source_integration.md").read_text(
        encoding="utf-8")

    output_path = iter_dir / "source_integration_output.md"

    prompt = fill_template(integration_template, {
        "concept_name": concept["Concept Name"],
        "analysis_path": str(analysis_path),
        "new_source_paths": format_source_list(new_sources),
        "feedback_path": str(output_path),
    })

    (iter_dir / "source_integration_prompt.md").write_text(prompt, encoding="utf-8")

    if args.dry_run:
        print(f"  dry-run {cid}: source-integration prompt saved to {iter_dir}")
        return output_path  # pretend it worked for dry-run flow

    from lib.validators import validate_feedback_verdict

    print(f"  source-integration {cid} ({len(new_sources)} new sources) ...",
          end="", flush=True)
    t0 = time.time()
    result = invoke_claude_validated(
        prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
        validator=validate_feedback_verdict,
        output_path=output_path,
        step_label="source-integration",
        log_path=iter_dir / "validation_log.json",
    )
    elapsed = time.time() - t0

    if result.invoke.returncode != 0:
        print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
        return None

    if not output_path.exists():
        print(f" FAILED ({elapsed:.0f}s) — no output file")
        return None

    feedback_text = output_path.read_text(encoding="utf-8")
    verdict, finding_count = parse_verdict_from_feedback(feedback_text)

    if verdict == "PASS":
        print(f" PASS ({elapsed:.0f}s) — no material additions")
        return None

    print(f" {finding_count} findings ({elapsed:.0f}s)")
    return output_path



def _get_prior_feedback(concept_dir: Path, iter_num: int) -> Path | None:
    """Return the feedback file from the prior iteration, if it exists."""
    if iter_num <= 1:
        return None
    prior = concept_dir / f"iter-{iter_num - 1}" / "feedback.md"
    return prior if prior.exists() else None


def _has_revise_status(analysis_path: Path) -> bool:
    """Check if analysis.md has Review-Status: revise."""
    if not analysis_path.exists():
        return False
    fm = parse_frontmatter(analysis_path)
    return fm.get("Review-Status") == "revise"


def _get_review_feedback(concept_dir: Path) -> str | None:
    """Extract F-N findings from review.md as feedback text for stage1.

    Returns feedback text content (caller writes to iter-N/feedback.md),
    or None if review.md has no extractable corrective actions.
    """
    from lib.validators import REVIEW_VERDICT_RE, CORRECTIVE_ACTIONS_RE

    review_path = concept_dir / "review.md"
    if not review_path.exists():
        return None

    text = review_path.read_text(encoding="utf-8")

    # Verify this is a REVISE review
    verdict_match = REVIEW_VERDICT_RE.search(text)
    if not verdict_match or verdict_match.group(1) != "REVISE":
        return None

    # Extract everything from "## Corrective Actions" to end or next ## section
    ca_match = CORRECTIVE_ACTIONS_RE.search(text[verdict_match.end():])
    if not ca_match:
        return None

    ca_start = verdict_match.end() + ca_match.end()
    # Find next ## header (not ###) or end of file
    next_section = re.search(r"^## ", text[ca_start:], re.MULTILINE)
    ca_text = text[ca_start:ca_start + next_section.start()] if next_section else text[ca_start:]

    if not ca_text.strip():
        return None

    # Format as feedback — VERDICT: FINDINGS so the analysis agent's
    # feedback-pass parser recognizes it
    return f"VERDICT: FINDINGS\n\n{ca_text.strip()}\n"


def _update_canonical_files(concept_dir: Path, iter_dir: Path) -> None:
    """Copy iteration model files to concept root for downstream consumers (FR-5).

    Also ensures analysis.md at concept root is current (FR-4).
    """
    # Model files
    iter_model = iter_dir / "model_setup.py"
    if iter_model.exists():
        shutil.copy2(iter_model, concept_dir / "model_setup.py")

    iter_output = iter_dir / "model_output.txt"
    if iter_output.exists():
        shutil.copy2(iter_output, concept_dir / "model_output.txt")
