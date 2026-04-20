"""Shared format constants and output validators for the concept analysis pipeline.

Provides:
- Compiled regex constants used by both validators and existing parsers
- ValidationResult dataclass and Validator type alias
- Concrete validators for feedback and review output formats
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

# ---------------------------------------------------------------------------
# Shared regex constants
# ---------------------------------------------------------------------------

# Feedback format (assessment, source-integration)
FEEDBACK_VERDICT_RE = re.compile(r"^VERDICT:\s*(PASS|FINDINGS)\s*$", re.MULTILINE)
FINDING_HEADER_RE = re.compile(r"^### F-\d+:", re.MULTILINE)
FINDING_CATEGORY_RE = re.compile(
    r"^\-\s+\**Category:?\**:?\s*(analysis|model)", re.MULTILINE
)


def _split_finding_blocks(text: str) -> list[str]:
    """Split feedback text into individual F-N finding blocks."""
    blocks = re.split(r"(?=^### F-\d+:)", text, flags=re.MULTILINE)
    return [b for b in blocks if FINDING_HEADER_RE.match(b)]


# Review format
REVIEW_VERDICT_RE = re.compile(r"^VERDICT:\s*(PROCEED|REVISE)\s*$", re.MULTILINE)
CORRECTIVE_ACTIONS_RE = re.compile(r"^## Corrective Actions", re.MULTILINE)
PROPOSED_ACTION_RE = re.compile(r"^### (PA-\d+):\s*(.+)$", re.MULTILINE)

# ---------------------------------------------------------------------------
# Validation protocol
# ---------------------------------------------------------------------------


@dataclass
class ValidationResult:
    """Result of validating LLM output."""

    valid: bool
    fix_message: str | None = None
    details: str = ""  # human-readable explanation for logging


Validator = Callable[[str], ValidationResult]

# ---------------------------------------------------------------------------
# Concrete validators
# ---------------------------------------------------------------------------


def validate_feedback_verdict(text: str) -> ValidationResult:
    """Validate feedback output format (assessment / source-integration).

    Checks:
    1. VERDICT line exists (PASS or FINDINGS)
    2. If FINDINGS: at least one ### F-N: block
    3. If FINDINGS: each finding has a Category field (analysis|model)
    """
    verdict_match = FEEDBACK_VERDICT_RE.search(text)
    if not verdict_match:
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your feedback file is missing the required verdict line. "
                "The file MUST contain exactly one line reading either "
                "`VERDICT: PASS` or `VERDICT: FINDINGS` (on its own line, "
                "at the start of the line, with no extra text). "
                "Please re-write the feedback file with the correct format."
            ),
            details="No VERDICT line found matching ^VERDICT:\\s*(PASS|FINDINGS)$",
        )

    if verdict_match.group(1) == "FINDINGS":
        findings = FINDING_HEADER_RE.findall(text)
        if not findings:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "Your feedback has `VERDICT: FINDINGS` but no finding blocks. "
                    "Each finding MUST use a `### F-N:` header (e.g., `### F-1: Title`). "
                    "Please re-write the feedback file with properly formatted findings."
                ),
                details="VERDICT: FINDINGS but no ### F-N: blocks found",
            )

        # Check Category field on each finding
        finding_blocks = _split_finding_blocks(text)
        missing_cat = []
        for block in finding_blocks:
            cat = FINDING_CATEGORY_RE.search(block)
            if not cat:
                header = block.split("\n", 1)[0].strip()
                missing_cat.append(header)

        if missing_cat:
            headers = "; ".join(missing_cat)
            return ValidationResult(
                valid=False,
                fix_message=(
                    f"The following findings are missing a valid Category field: {headers}. "
                    "Each finding MUST include `- **Category:** analysis` or "
                    "`- **Category:** model` on its own line. "
                    "Please re-write the feedback file with Category fields on all findings."
                ),
                details=f"Missing Category on: {headers}",
            )

    verdict_type = verdict_match.group(1)
    return ValidationResult(
        valid=True,
        details=f"Feedback format valid (verdict: {verdict_type})",
    )


def validate_review_verdict(text: str) -> ValidationResult:
    """Validate review output format.

    Checks:
    1. VERDICT line exists (PROCEED or REVISE)
    2. If REVISE: ## Corrective Actions section exists
    3. If REVISE: at least one ### F-N: block under Corrective Actions
    """
    verdict_match = REVIEW_VERDICT_RE.search(text)
    if not verdict_match:
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your review is missing the required verdict line. "
                "The review MUST contain exactly one line reading either "
                "`VERDICT: PROCEED` or `VERDICT: REVISE` (on its own line). "
                "Please re-write the review file with the correct verdict."
            ),
            details="No VERDICT line matching ^VERDICT:\\s*(PROCEED|REVISE)$",
        )

    if verdict_match.group(1) == "REVISE":
        ca_match = CORRECTIVE_ACTIONS_RE.search(text)
        if not ca_match:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "Your review has `VERDICT: REVISE` but is missing the "
                    "`## Corrective Actions` section. When the verdict is REVISE, "
                    "you MUST include a `## Corrective Actions` section containing "
                    "`### F-N:` findings that describe what needs to change. "
                    "Please re-write the review file with corrective actions."
                ),
                details="VERDICT: REVISE but no ## Corrective Actions section",
            )

        # Check for F-N blocks after Corrective Actions
        ca_text = text[ca_match.start():]
        findings = FINDING_HEADER_RE.findall(ca_text)
        if not findings:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "Your `## Corrective Actions` section has no findings. "
                    "It MUST contain at least one `### F-N:` finding block. "
                    "Please re-write the review with corrective action findings."
                ),
                details="## Corrective Actions exists but contains no ### F-N: blocks",
            )

    verdict_type = verdict_match.group(1)
    return ValidationResult(
        valid=True,
        details=f"Review format valid (verdict: {verdict_type})",
    )


# ---------------------------------------------------------------------------
# New validators (FR-9, FR-10, FR-11)
# ---------------------------------------------------------------------------


def validate_non_empty(text: str) -> ValidationResult:
    """Minimum viable validator — reject empty/whitespace-only output.

    Used when all we can check is that Claude produced *something*. Downstream
    validators (format, syntax) compose on top of this.
    """
    if not text.strip():
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your output was empty. Please re-read the instructions "
                "and produce the requested output."
            ),
            details="Output is empty or whitespace-only",
        )
    return ValidationResult(
        valid=True,
        details=f"Non-empty ({len(text)} chars)",
    )


def validate_python_syntax(text: str) -> ValidationResult:
    """Check that output is parseable Python source.

    Uses ``compile(..., 'exec')`` so the text must be a complete module — the
    exact shape required for ``model_setup.py``. An empty string *is* valid
    Python; pair this with ``validate_non_empty`` if you need both.
    """
    try:
        compile(text, "<model_setup>", "exec")
    except SyntaxError as exc:
        lineno = exc.lineno if exc.lineno is not None else "?"
        return ValidationResult(
            valid=False,
            fix_message=(
                f"The Python file has a syntax error on line {lineno}: {exc.msg}. "
                f"Please fix the syntax error and re-write the file."
            ),
            details=f"SyntaxError line {lineno}: {exc.msg}",
        )
    return ValidationResult(valid=True, details="Valid Python syntax")


def make_file_modified_validator(path: Path) -> Validator:
    """Factory: returns a validator that checks file bytes actually changed.

    Snapshots the file's SHA-256 at construction time, then on each call
    re-reads raw bytes from disk and compares. The ``text`` argument passed by
    ``invoke_claude_validated`` is deliberately ignored — hashing the encoded
    string can disagree with the disk snapshot after a ``read_text`` round-trip
    that normalizes CRLF line endings or strips a BOM, producing a false pass
    on an unchanged file. We read bytes directly to avoid that trap.

    The returned callable's ``__name__`` is set to ``"validate_file_modified"``
    so validation log entries read naturally.

    Usage::

        validator = make_file_modified_validator(analysis_path)
        result = invoke_claude_validated(
            ..., validator=validator, output_path=analysis_path)
    """
    original_hash = hashlib.sha256(path.read_bytes()).hexdigest()

    def _check(_text: str) -> ValidationResult:
        # Re-read bytes directly — NOT text.encode("utf-8"). The caller's
        # ``text`` has been through ``read_text(encoding="utf-8")`` which
        # normalizes line endings and may strip BOMs. Hashing the encoded
        # string can therefore disagree with ``read_bytes()`` even when the
        # file on disk is byte-identical to the snapshot.
        if not path.exists():
            # Should be unreachable — ``invoke_claude_validated``'s H-01 branch
            # handles file-missing before calling the validator — but keep the
            # check for defense in depth.
            return ValidationResult(
                valid=False,
                fix_message=f"Expected file was not found at {path}.",
                details="File missing during file-modified check",
            )
        current = hashlib.sha256(path.read_bytes()).hexdigest()
        if current == original_hash:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "The file was not modified. You MUST apply the requested "
                    "changes using the Edit tool. Read the file, identify "
                    "what needs to change, and use Edit to make the changes."
                ),
                details="File content unchanged (SHA-256 match)",
            )
        return ValidationResult(valid=True, details="File content changed")

    _check.__name__ = "validate_file_modified"
    return _check


def chain_validators(*validators: Validator) -> Validator:
    """Run validators in order; return first failure or final success."""

    def _chain(text: str) -> ValidationResult:
        for v in validators:
            result = v(text)
            if not result.valid:
                return result
        return ValidationResult(valid=True, details="All validators passed")

    _chain.__name__ = "+".join(v.__name__ for v in validators)
    return _chain


def has_model_category_findings(feedback_text: str) -> bool:
    """Check if any findings in the feedback are tagged Category: model.

    Returns True if at least one model finding exists, or if any finding
    lacks a Category field (conservative: assume model-targeted).
    """
    if not feedback_text:
        return False

    finding_blocks = _split_finding_blocks(feedback_text)
    if not finding_blocks:
        return False

    for block in finding_blocks:
        cat_match = FINDING_CATEGORY_RE.search(block)
        if cat_match is None:
            return True  # Missing category → conservative, treat as model
        if cat_match.group(1) == "model":
            return True

    return False
