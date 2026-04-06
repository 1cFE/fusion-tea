"""Shared format constants and output validators for the concept analysis pipeline.

Provides:
- Compiled regex constants used by both validators and existing parsers
- ValidationResult dataclass and Validator type alias
- Concrete validators for feedback and review output formats
"""

from __future__ import annotations

import re
from dataclasses import dataclass
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
        finding_blocks = re.split(r"(?=^### F-\d+:)", text, flags=re.MULTILINE)
        finding_blocks = [b for b in finding_blocks if FINDING_HEADER_RE.match(b)]
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

    return ValidationResult(valid=True, details="Feedback format valid")


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

    return ValidationResult(valid=True, details="Review format valid")
