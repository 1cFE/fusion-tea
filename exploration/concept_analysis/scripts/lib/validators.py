"""Shared format constants and output validators for the concept analysis pipeline.

Provides:
- Compiled regex constants used by both validators and existing parsers
- ValidationResult dataclass and Validator type alias
- Concrete validators for feedback and review output formats
"""

from __future__ import annotations

import ast
import hashlib
import io
import re
import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from lib.canonical_accounts import fit_grade_band

# ---------------------------------------------------------------------------
# Shared regex constants
# ---------------------------------------------------------------------------
# The verdict / finding-header / proposed-action MULTILINE-regex constants were
# retired in Item 8 Phase 4 (FR-28) in favour of the line-anchored helpers
# below; only these two remain, for the few callers that still want a plain
# pattern.

# Category tag on a finding bullet (`- **Category:** analysis|model`).
FINDING_CATEGORY_RE = re.compile(
    r"^\-\s+\**Category:?\**:?\s*(analysis|model)", re.MULTILINE
)
# Review "## Corrective Actions" section heading.
CORRECTIVE_ACTIONS_RE = re.compile(r"^## Corrective Actions", re.MULTILINE)

# ---------------------------------------------------------------------------
# Line-anchored parsing helpers (Item 8, Phase 2)
# ---------------------------------------------------------------------------
# These are the internals of the five named parsers (parse_verdict_from_feedback,
# has_model_category_findings, validate_feedback_verdict, validate_review_verdict,
# parse_proposed_actions): simple per-line scanning instead of MULTILINE regex.
# Item 8 Phase 4 deleted the legacy verdict/header/proposed-action constants and
# rewired their last direct users (loop.py / run_analysis.py review paths) onto
# these helpers, discharging Item 7's FR-9. Behavior and return shapes are
# preserved per signal_contract.md — only the mechanism changed.


def _header_id(line: str, kind: str) -> str | None:
    """If ``line`` is a ``### <kind>-N:`` header, return ``"<kind>-N"`` else None.

    ``kind`` is ``"F"`` (findings) or ``"PA"`` (proposed actions). Line-anchored:
    matches the stripped line, the digits between the prefix and the colon must
    be all-digits and non-empty.
    """
    s = line.strip()
    prefix = f"### {kind}-"
    if not s.startswith(prefix):
        return None
    rest = s[len(prefix):]
    num, sep, _ = rest.partition(":")
    if sep != ":" or not num.isdigit():
        return None
    return f"{kind}-{num}"


def _verdict_token(text: str, allowed: frozenset[str]) -> str | None:
    """Return the first ``VERDICT: <TOKEN>`` token (TOKEN in ``allowed``).

    Line-anchored, ``search``-equivalent to the old ``^VERDICT:\\s*(...)\\s*$``
    constants: scans line by line, the stripped line must read exactly
    ``VERDICT: <token>`` (any inter-token whitespace, nothing trailing). A
    ``VERDICT:`` line whose token is not in ``allowed`` (e.g. trailing prose) is
    skipped, not matched — so ``VERDICT: PASS — all goals met`` is rejected and a
    later well-formed verdict line still wins.
    """
    for raw in text.splitlines():
        key, sep, val = raw.strip().partition(":")
        if sep == ":" and key.strip() == "VERDICT" and val.strip() in allowed:
            return val.strip()
    return None


def _split_finding_blocks(text: str) -> list[str]:
    """Split feedback text into individual ``### F-N:`` finding blocks.

    Line-anchored: a block runs from one finding header line up to (but not
    including) the next finding header line, or end of text.
    """
    lines = text.splitlines(keepends=True)
    starts = [i for i, ln in enumerate(lines) if _header_id(ln, "F")]
    blocks: list[str] = []
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
        blocks.append("".join(lines[start:end]))
    return blocks


def _count_findings(text: str) -> int:
    """Count ``### F-N:`` finding headers in ``text`` (line-anchored)."""
    return sum(1 for ln in text.splitlines() if _header_id(ln, "F"))


def _finding_category(block: str) -> str | None:
    """Return the ``analysis`` / ``model`` Category of a finding block, or None.

    Line-anchored and tolerant of the bold-marker variants the old
    ``FINDING_CATEGORY_RE`` accepted (``- **Category:** model`` and
    ``- **Category**: model``). The first token after the colon is the value.
    """
    for raw in block.splitlines():
        s = raw.strip()
        if not s.startswith("-"):
            continue
        body = s.lstrip("-").replace("*", "").strip()
        key, sep, val = body.partition(":")
        if sep == ":" and key.strip().lower() == "category":
            first = val.strip().split()[0].lower() if val.strip() else ""
            if first in ("analysis", "model"):
                return first
    return None

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
    verdict = _verdict_token(text, frozenset({"PASS", "FINDINGS"}))
    if verdict is None:
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your feedback file is missing the required verdict line. "
                "The file MUST contain exactly one line reading either "
                "`VERDICT: PASS` or `VERDICT: FINDINGS` (on its own line, "
                "at the start of the line, with no extra text). "
                "Please re-write the feedback file with the correct format."
            ),
            details="No VERDICT line found matching `VERDICT: PASS|FINDINGS`",
        )

    if verdict == "FINDINGS":
        findings = _count_findings(text)
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
            if _finding_category(block) is None:
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

    return ValidationResult(
        valid=True,
        details=f"Feedback format valid (verdict: {verdict})",
    )


def validate_review_verdict(text: str) -> ValidationResult:
    """Validate review output format.

    Checks:
    1. VERDICT line exists (PROCEED or REVISE)
    2. If REVISE: ## Corrective Actions section exists
    3. If REVISE: at least one ### F-N: block under Corrective Actions
    """
    verdict = _verdict_token(text, frozenset({"PROCEED", "REVISE"}))
    if verdict is None:
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your review is missing the required verdict line. "
                "The review MUST contain exactly one line reading either "
                "`VERDICT: PROCEED` or `VERDICT: REVISE` (on its own line). "
                "Please re-write the review file with the correct verdict."
            ),
            details="No VERDICT line matching `VERDICT: PROCEED|REVISE`",
        )

    if verdict == "REVISE":
        lines = text.splitlines()
        ca_idx = next(
            (i for i, ln in enumerate(lines)
             if ln.strip().startswith("## Corrective Actions")),
            None,
        )
        if ca_idx is None:
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

        # Check for F-N blocks after the Corrective Actions heading.
        ca_text = "\n".join(lines[ca_idx:])
        if _count_findings(ca_text) == 0:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "Your `## Corrective Actions` section has no findings. "
                    "It MUST contain at least one `### F-N:` finding block. "
                    "Please re-write the review with corrective action findings."
                ),
                details="## Corrective Actions exists but contains no ### F-N: blocks",
            )

    return ValidationResult(
        valid=True,
        details=f"Review format valid (verdict: {verdict})",
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
        category = _finding_category(block)
        if category is None:
            return True  # Missing category → conservative, treat as model
        if category == "model":
            return True

    return False


# ---------------------------------------------------------------------------
# Structural validators for the reworked model_setup.py (Item 7)
#
# These read the *shape of the code* via AST, not the prose of an LLM verdict,
# so they survive the prompt-format change Item 8 makes. They are pure
# functions over their text inputs (no LLM, no network) and are NOT wired into
# the live loop by Item 7 — Item 8 chains the output gates at loop.py:638.
# See .project/active/concept-rework-helpers-validators/design.md.
# ---------------------------------------------------------------------------

_REQUIRED_OVERRIDE_FIELDS = {
    "account", "value", "enabled", "provenance", "source", "rationale",
}
_VALID_PROVENANCE = {"direct", "derived"}


def _target_names(node: ast.expr) -> list[str]:
    """Flatten an assignment target into the simple ``Name`` ids it binds.

    Handles tuple/list unpacking (``native, result_1gw = ...``); ignores
    attribute/subscript targets (they bind no bare name).
    """
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, (ast.Tuple, ast.List)):
        names: list[str] = []
        for el in node.elts:
            names.extend(_target_names(el))
        return names
    return []


def _module_bindings(tree: ast.Module) -> list[tuple[list[str], ast.expr]]:
    """Return ``(bound_names, value_node)`` for each module-level assignment.

    Direct ``Module`` children only — nested assignments (inside ``if`` /
    functions) are intentionally ignored; the contract is about module level.
    """
    out: list[tuple[list[str], ast.expr]] = []
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            names: list[str] = []
            for tgt in stmt.targets:
                names.extend(_target_names(tgt))
            out.append((names, stmt.value))
        elif isinstance(stmt, ast.AnnAssign) and stmt.value is not None:
            out.append((_target_names(stmt.target), stmt.value))
    return out


def _is_call_to_name(node: ast.expr, name: str) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == name
    )


def _is_forward_call(node: ast.expr) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "forward"
    )


def _kwarg_equals(call: ast.Call, key: str, expected) -> bool:
    """True if ``call`` has keyword ``key`` whose literal value == ``expected``."""
    for kw in call.keywords:
        if kw.arg == key:
            try:
                return ast.literal_eval(kw.value) == expected
            except (ValueError, SyntaxError, TypeError):
                return False
    return False


def _default_comment_linenos(text: str) -> set[int]:
    """Line numbers carrying a ``# DEFAULT:`` comment (the re-passed-default smell)."""
    out: set[int] = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT and "DEFAULT:" in tok.string:
                out.add(tok.start[0])
    except (tokenize.TokenError, IndentationError):
        pass  # advisory only — never block on a tokenizer hiccup
    return out


def _forward_kwarg_linenos(tree: ast.Module) -> set[int]:
    """Line numbers of keyword args passed to any ``forward`` / helper call."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and (
            _is_forward_call(node) or _is_call_to_name(node, "run_native_and_1gw")
        ):
            for kw in node.keywords:
                # kw.arg is None for **splat; those have no own kwarg line.
                if kw.arg is not None and hasattr(kw.value, "lineno"):
                    out.add(kw.value.lineno)
    return out


def validate_model_setup_contract(
    text: str,
    *,
    strict_helper_only: bool = False,
    warn_on_default_comments: bool = True,
) -> ValidationResult:
    """Enforce the module-level contract of a ``model_setup.py`` via AST.

    Requires module-level ``model``, ``generic``, ``native``, and ``result_1gw``
    bindings (the three-forward contract). ``generic`` MUST be bound by
    ``generic = generic_reference(...)`` (forward 1, overrides off — the
    reference a relative override is written against). ``native`` and
    ``result_1gw`` (forwards 2 & 3, overrides on) must be reached by one of two
    recognized forms:

    - **helper form** — ``native, result_1gw = run_native_and_1gw(...)``
    - **inline form**  — ``result_1gw = <model>.forward(net_electric_mw=1000,
      ...)`` with ``native`` bound separately

    ``strict_helper_only=True`` (Item 8 flips this on) accepts only the helper
    form, so a generated file can't silently regress to a hand-rolled forward.
    ``warn_on_default_comments`` adds an advisory ``details`` note (never
    affects ``valid``) when a ``forward`` kwarg line carries a ``# DEFAULT:``
    comment — the signature of a re-passed library default.
    """
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        lineno = exc.lineno if exc.lineno is not None else "?"
        return ValidationResult(
            valid=False,
            fix_message=(
                f"model_setup.py has a syntax error on line {lineno}: {exc.msg}. "
                f"Fix the syntax error and re-write the file."
            ),
            details=f"SyntaxError line {lineno}: {exc.msg}",
        )

    bindings = _module_bindings(tree)
    bound = {name for names, _ in bindings for name in names}
    missing = [
        n for n in ("model", "generic", "native", "result_1gw") if n not in bound
    ]
    if missing:
        return ValidationResult(
            valid=False,
            fix_message=(
                f"model_setup.py is missing required module-level name(s): "
                f"{', '.join(missing)}. The file MUST bind `model`, `generic`, "
                f"`native`, and `result_1gw` at module level (the three-forward "
                f"contract: `generic` overrides-off, `native` overrides-on at "
                f"design scale, `result_1gw` overrides-on at 1 GWe)."
            ),
            details=f"Missing module-level binding(s): {', '.join(missing)}",
        )

    # `generic` MUST be the standalone overrides-off forward, bound via
    # generic_reference() — not a hand-rolled forward. It is the reference a
    # relative override is written against, so it must precede the registry.
    generic_ok = any(
        names == ["generic"] and _is_call_to_name(value, "generic_reference")
        for names, value in bindings
    )
    if not generic_ok:
        return ValidationResult(
            valid=False,
            fix_message=(
                "model_setup.py must bind `generic` via the shared helper: "
                "`generic = generic_reference(model, spec, P_native)` (the "
                "overrides-off forward a relative override references). A "
                "hand-rolled `generic = model.forward(...)` is not accepted."
            ),
            details="generic not bound via generic_reference()",
        )

    # Classify how native / result_1gw are bound.
    form: str | None = None
    for names, value in bindings:
        if "native" in names and "result_1gw" in names:
            if _is_call_to_name(value, "run_native_and_1gw"):
                form = "helper"
                break
    if form is None and not strict_helper_only:
        for names, value in bindings:
            if names == ["result_1gw"] and _is_forward_call(value):
                if _kwarg_equals(value, "net_electric_mw", 1000):
                    form = "inline"
                    break

    if form is None:
        if strict_helper_only:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "model_setup.py must bind `native` and `result_1gw` via the "
                    "shared helper: `native, result_1gw = run_native_and_1gw("
                    "model, spec, overrides, P_native)`. A hand-rolled inline "
                    "`forward(...)` is not accepted in strict mode."
                ),
                details=(
                    "native, result_1gw not bound via run_native_and_1gw "
                    "(strict mode)"
                ),
            )
        return ValidationResult(
            valid=False,
            fix_message=(
                "model_setup.py must bind `native` and `result_1gw` either via "
                "`native, result_1gw = run_native_and_1gw(...)` or via an inline "
                "`result_1gw = model.forward(net_electric_mw=1000, ...)` call "
                "(with `native` bound separately). Neither was found (an inline "
                "forward must pass `net_electric_mw=1000`)."
            ),
            details=(
                "native/result_1gw bound by neither the helper tuple-unpack nor "
                "an inline forward(net_electric_mw=1000)"
            ),
        )

    details = f"model_setup contract valid (result_1gw via {form} form)"

    if warn_on_default_comments:
        hits = sorted(_default_comment_linenos(text) & _forward_kwarg_linenos(tree))
        if hits:
            details += (
                f"; WARNING: # DEFAULT:-commented forward kwarg on line(s) "
                f"{hits} — re-passed library default? Let the library carry it."
            )

    return ValidationResult(valid=True, details=details)


def _dict_literal_fields(node: ast.Dict) -> dict[str, ast.expr]:
    """Map a dict literal's string-constant keys to their value nodes."""
    out: dict[str, ast.expr] = {}
    for key, value in zip(node.keys, node.values):
        if isinstance(key, ast.Constant) and isinstance(key.value, str):
            out[key.value] = value
    return out


def _const_numeric(node: ast.expr) -> int | float | None:
    """Fold a constant numeric expression to a number, or return None.

    Handles numeric literals and the arithmetic an override ``value`` may use
    to document its own derivation — unary ``+``/``-`` and binary
    ``+``/``-``/``*``/``/`` over numeric constants (e.g. ``260.0 * 1.34``).
    Returns None for anything that is not a pure numeric constant expression
    (strings, booleans, names, calls, unsupported operators). ``**`` is
    deliberately unsupported so the validator never evaluates large powers.
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            return None
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        v = _const_numeric(node.operand)
        if v is None:
            return None
        return +v if isinstance(node.op, ast.UAdd) else -v
    if isinstance(node, ast.BinOp) and isinstance(
        node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)
    ):
        left = _const_numeric(node.left)
        right = _const_numeric(node.right)
        if left is None or right is None:
            return None
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        return None if right == 0 else left / right
    return None


def validate_override_registry(text: str) -> ValidationResult:
    """Enforce the shape of the ``overrides`` registry via AST.

    Requires a module-level ``overrides = [ {...}, ... ]`` list of dict
    literals where **every** entry (regardless of ``enabled``) has all six
    fields and ``provenance ∈ {direct, derived}``, with no two entries
    sharing an ``account``. ``value`` may be a number, a constant numeric
    expression (e.g. ``260.0 * 1.34``), or an expression over ``generic``
    (a *relative* override, e.g. ``0.70 * generic.costs.cas21``); it MUST NOT
    reference ``native``, ``result_1gw``, or ``result`` (wrong reference
    frame — a relative override is written against the bare library value,
    not an overrides-on forward or the removed two-forward name). For
    ``generic``-referencing values the numeric type is enforced at runtime
    when ``model_setup.py`` executes — provenance, not literal-ness, is what
    makes an override legitimate (see the design doc, Override Entry).
    """
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        lineno = exc.lineno if exc.lineno is not None else "?"
        return ValidationResult(
            valid=False,
            fix_message=(
                f"model_setup.py has a syntax error on line {lineno}: {exc.msg}."
            ),
            details=f"SyntaxError line {lineno}: {exc.msg}",
        )

    overrides_node: ast.expr | None = None
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and "overrides" in [
            t.id for t in stmt.targets if isinstance(t, ast.Name)
        ]:
            overrides_node = stmt.value
        elif (
            isinstance(stmt, ast.AnnAssign)
            and isinstance(stmt.target, ast.Name)
            and stmt.target.id == "overrides"
            and stmt.value is not None
        ):
            overrides_node = stmt.value

    if overrides_node is None:
        return ValidationResult(
            valid=False,
            fix_message=(
                "model_setup.py has no module-level `overrides` assignment. "
                "Define `overrides = [ ... ]` as a list of six-field registry "
                "entries (use `overrides = []` if there are none)."
            ),
            details="No module-level `overrides` binding found",
        )
    if not isinstance(overrides_node, ast.List):
        return ValidationResult(
            valid=False,
            fix_message="`overrides` MUST be a list literal of dict entries.",
            details=f"`overrides` is {type(overrides_node).__name__}, not a list literal",
        )

    accounts: list[str] = []
    for i, el in enumerate(overrides_node.elts):
        label = f"overrides[{i}]"
        if not isinstance(el, ast.Dict):
            return ValidationResult(
                valid=False,
                fix_message=f"{label} is not a dict literal. Each entry MUST be a "
                f"`{{...}}` mapping with the six override fields.",
                details=f"{label} is {type(el).__name__}, not a dict literal",
            )
        fields = _dict_literal_fields(el)
        missing = _REQUIRED_OVERRIDE_FIELDS - set(fields)
        if missing:
            return ValidationResult(
                valid=False,
                fix_message=(
                    f"{label} is missing required field(s): "
                    f"{', '.join(sorted(missing))}. Every override entry MUST have "
                    f"all six: account, value, enabled, provenance, source, rationale."
                ),
                details=f"{label} missing: {', '.join(sorted(missing))}",
            )

        # value: a number, a constant numeric expression (e.g. 260.0 * 1.34),
        # or an expression over `generic` (relative overrides, e.g.
        # 0.70 * generic.costs.cas21). Provenance — not literal-ness — is what
        # makes an override legitimate (design doc, Override Entry).
        value_node = fields["value"]
        referenced = {
            n.id for n in ast.walk(value_node) if isinstance(n, ast.Name)
        }
        bad_frame = referenced & {"native", "result_1gw", "result"}
        if bad_frame:
            return ValidationResult(
                valid=False,
                fix_message=(
                    f"{label} `value` references `{sorted(bad_frame)[0]}`. A "
                    f"relative override must reference `generic` — the overrides-off "
                    f"library value at the n_mod=1 / P_native reference frame — not "
                    f"an overrides-on forward (`native` / `result_1gw`) or the "
                    f"removed two-forward `result`."
                ),
                details=(
                    f"{label} value references {sorted(bad_frame)} (frame error)"
                ),
            )
        if not referenced:
            # No runtime references → must be a statically-numeric literal or a
            # constant arithmetic expression. (Catches strings, lists, dicts,
            # booleans, and typoed values.)
            if _const_numeric(value_node) is None:
                return ValidationResult(
                    valid=False,
                    fix_message=(
                        f"{label} `value` must be a number, a constant numeric "
                        f"expression (e.g. 260.0 * 1.34), or an expression over "
                        f"`generic` (e.g. 0.70 * generic.costs.cas21). Strings "
                        f"and non-numeric literals are not allowed."
                    ),
                    details=f"{label} value is not numeric and references no runtime value",
                )
        # else: references `generic` (or another runtime name) → relative
        # override; numeric type is enforced at runtime on module execution.

        # provenance: one of the allowed tokens.
        try:
            provenance = ast.literal_eval(fields["provenance"])
        except (ValueError, SyntaxError, TypeError):
            provenance = None
        if provenance not in _VALID_PROVENANCE:
            return ValidationResult(
                valid=False,
                fix_message=(
                    f"{label} `provenance` must be one of "
                    f"{sorted(_VALID_PROVENANCE)} (got {provenance!r})."
                ),
                details=f"{label} provenance invalid: {provenance!r}",
            )

        # account: a string, for duplicate detection.
        try:
            account = ast.literal_eval(fields["account"])
        except (ValueError, SyntaxError, TypeError):
            account = None
        if not isinstance(account, str):
            return ValidationResult(
                valid=False,
                fix_message=f"{label} `account` must be a string CAS code.",
                details=f"{label} account is not a string literal",
            )
        accounts.append(account)

    duplicates = sorted({a for a in accounts if accounts.count(a) > 1})
    if duplicates:
        return ValidationResult(
            valid=False,
            fix_message=(
                f"The override registry has duplicate account(s): "
                f"{', '.join(duplicates)}. Each account MUST appear at most once "
                f"(disable an entry with `enabled: False` rather than duplicating)."
            ),
            details=f"Duplicate account(s): {', '.join(duplicates)}",
        )

    return ValidationResult(
        valid=True,
        details=f"Override registry valid ({len(accounts)} entries)",
    )


# ---------------------------------------------------------------------------
# Coherence checks (Item 7) — multi-input, NOT chained, NOT loop-wired here.
#
# These take more than one input (CSV row + code text + grade) so they can't
# fit the Callable[[str], ValidationResult] gate signature. They ship as
# standalone library functions; Item 8 (assess stage) / Item 9 (model_critic)
# wire them. Pattern-match comparables_sanity_check.py — flags as input to the
# LLM reviewer, not hard gates.
# ---------------------------------------------------------------------------

# Relative tolerance for P_native agreement (so 233 == 233.0 but 400 != 233).
_PNATIVE_REL_TOL = 0.001

_ACCOUNT_RE = re.compile(r"\b(C\d{6}|CAS\d{2})\b")
_PROVENANCE_TOKEN_RE = re.compile(r"\b(direct|derived)\b")
_ANALYSIS_PNATIVE_RE = re.compile(r"P[_\s]?native\D*?(\d+(?:\.\d+)?)", re.IGNORECASE)


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= _PNATIVE_REL_TOL * max(abs(a), abs(b), 1.0)


def _module_pnative(tree: ast.Module) -> float | None:
    """Read the module-level ``P_native`` literal from a model_setup AST."""
    for names, value in _module_bindings(tree):
        if "P_native" in names:
            try:
                lit = ast.literal_eval(value)
            except (ValueError, SyntaxError, TypeError):
                return None
            if isinstance(lit, (int, float)) and not isinstance(lit, bool):
                return float(lit)
    return None


def _override_provenance_map(tree: ast.Module) -> dict[str, str]:
    """Map ``account -> provenance`` from the module-level overrides registry."""
    out: dict[str, str] = {}
    for stmt in tree.body:
        node = None
        if isinstance(stmt, ast.Assign) and "overrides" in [
            t.id for t in stmt.targets if isinstance(t, ast.Name)
        ]:
            node = stmt.value
        elif (
            isinstance(stmt, ast.AnnAssign)
            and isinstance(stmt.target, ast.Name)
            and stmt.target.id == "overrides"
        ):
            node = stmt.value
        if not isinstance(node, ast.List):
            continue
        for el in node.elts:
            if not isinstance(el, ast.Dict):
                continue
            fields = _dict_literal_fields(el)
            try:
                account = ast.literal_eval(fields.get("account"))
                provenance = ast.literal_eval(fields.get("provenance"))
            except (ValueError, SyntaxError, TypeError):
                continue
            if isinstance(account, str) and isinstance(provenance, str):
                out[account] = provenance
    return out


def _analysis_provenance_map(analysis_md_text: str) -> dict[str, str]:
    """Per-account provenance scraped from an analysis.md leg.

    PROVISIONAL FORMAT: a line mentioning a CAS account and a `direct`/`derived`
    token associates them. The exact analysis.md Design Point block is Item 8's
    to finalize; this minimal line-level association is intentionally forgiving
    and is only consulted when ``analysis_md_text`` is supplied.
    """
    out: dict[str, str] = {}
    for line in analysis_md_text.splitlines():
        acct = _ACCOUNT_RE.search(line)
        prov = _PROVENANCE_TOKEN_RE.search(line)
        if acct and prov:
            out[acct.group(1)] = prov.group(1)
    return out


def validate_design_point_coherence(
    concept_id: str,
    model_setup_text: str,
    design_point_row: dict,
    analysis_md_text: str | None = None,
) -> ValidationResult:
    """Check ``P_native`` (and provenance) agreement across artifacts.

    Two legs are always checked: the ``P_native`` literal in ``model_setup.py``
    (parsed via AST) must agree — within ≤0.1% — with ``design_point_row
    ["p_native_mwe"]`` (the caller reads the CSV, keeping this function pure
    over data). The third leg activates only when ``analysis_md_text`` is
    supplied: any ``P_native`` it states must also agree, and every override
    account appearing in **both** ``model_setup.py`` and the analysis text must
    carry the same provenance. The analysis.md format is provisional (Item 8).

    This catches the Phase 0 operator error directly: a ``model_setup.py`` with
    ``P_native=400`` against a design-point row of ``233`` fails.
    """
    try:
        tree = ast.parse(model_setup_text)
    except SyntaxError as exc:
        return ValidationResult(
            valid=False,
            fix_message=f"model_setup.py has a syntax error: {exc.msg}.",
            details=f"SyntaxError: {exc.msg}",
        )

    code_pnative = _module_pnative(tree)
    if code_pnative is None:
        return ValidationResult(
            valid=False,
            fix_message=(
                "model_setup.py has no module-level numeric `P_native`. The "
                "design-point coherence check needs `P_native = <MWe>` at module "
                "level."
            ),
            details=f"{concept_id}: no module-level P_native literal",
        )

    try:
        csv_pnative = float(design_point_row["p_native_mwe"])
    except (KeyError, TypeError, ValueError):
        return ValidationResult(
            valid=False,
            fix_message=(
                "design_point_row is missing a numeric `p_native_mwe`. The caller "
                "must pass the parsed design_point.csv row for this concept."
            ),
            details=f"{concept_id}: design_point_row lacks numeric p_native_mwe",
        )

    if not _close(code_pnative, csv_pnative):
        return ValidationResult(
            valid=False,
            fix_message=(
                f"P_native disagreement for {concept_id}: model_setup.py says "
                f"{code_pnative:g} MWe but the design-point table says "
                f"{csv_pnative:g} MWe. These MUST match — fix whichever is wrong "
                f"(this is the Phase 0 operator error)."
            ),
            details=(
                f"{concept_id}: P_native mismatch model_setup={code_pnative:g} "
                f"vs design_point={csv_pnative:g}"
            ),
        )

    if analysis_md_text is not None:
        ana_pnative = None
        m = _ANALYSIS_PNATIVE_RE.search(analysis_md_text)
        if m:
            ana_pnative = float(m.group(1))
        if ana_pnative is not None and not _close(code_pnative, ana_pnative):
            return ValidationResult(
                valid=False,
                fix_message=(
                    f"P_native disagreement for {concept_id}: model_setup.py says "
                    f"{code_pnative:g} MWe but analysis.md states "
                    f"{ana_pnative:g} MWe."
                ),
                details=(
                    f"{concept_id}: P_native mismatch model_setup={code_pnative:g} "
                    f"vs analysis.md={ana_pnative:g}"
                ),
            )

        code_prov = _override_provenance_map(tree)
        ana_prov = _analysis_provenance_map(analysis_md_text)
        mismatches = sorted(
            a for a in (set(code_prov) & set(ana_prov)) if code_prov[a] != ana_prov[a]
        )
        if mismatches:
            detail = ", ".join(
                f"{a} (model_setup={code_prov[a]}, analysis.md={ana_prov[a]})"
                for a in mismatches
            )
            return ValidationResult(
                valid=False,
                fix_message=(
                    f"Provenance disagreement for {concept_id} on shared override "
                    f"account(s): {detail}. The same account MUST carry the same "
                    f"provenance in model_setup.py and analysis.md."
                ),
                details=f"{concept_id}: provenance mismatch — {detail}",
            )

    legs = "2-leg" if analysis_md_text is None else "3-leg"
    return ValidationResult(
        valid=True,
        details=f"{concept_id}: P_native coherent at {code_pnative:g} MWe ({legs})",
    )


def check_override_count_vs_fit_grade(
    fit_grade: str, enabled_count: int
) -> ValidationResult:
    """Advisory smell check: archetype-fit grade vs. number of enabled overrides.

    Flags when the enabled-override count falls **outside** the expected band for
    the concept's archetype-fit grade. The band is ``FIT_GRADE_OVERRIDE_BAND``
    (via ``fit_grade_band``) — the single source also rendered into the analyze /
    assessment prompt rubric (``fit_grade_band_line``), so this automated flag and
    the instruction the LLM was given ("expect L–H; flag if outside this band")
    cannot disagree. This is **advisory** — ``valid`` is always ``True``; a flag
    rides in ``details`` (prefixed ``FLAG:``) for the LLM reviewer / model_critic
    to weigh. It never hard-fails a run.

    - Count **above** the band (e.g. High fit with > 4): a better-fit concept
      needing this many corrections suggests the archetype is wrong or the
      overrides over-reach.
    - Count **below** the band (e.g. Low fit with < 6): a poorer-fit concept with
      this few corrections suggests the library default is being trusted where the
      archetype says it shouldn't be. (High's band floor is 0, so High never
      flags for too-few.)

    A ``"None"`` / unknown grade (freeform-routed concepts) has no band and stays
    quiet.
    """
    band = fit_grade_band(fit_grade)
    if band is None:
        return ValidationResult(
            valid=True,
            details=(
                f"Override count ({enabled_count}) — no fit-grade band for "
                f"{fit_grade or 'unknown'} fit"
            ),
        )

    low, high = band
    if enabled_count > high:
        return ValidationResult(
            valid=True,
            details=(
                f"FLAG: {fit_grade} archetype fit with {enabled_count} enabled "
                f"overrides (expected {low}–{high}) — a better-fit concept needing "
                f"this many corrections suggests the archetype is wrong or the "
                f"overrides over-reach."
            ),
        )
    if enabled_count < low:
        return ValidationResult(
            valid=True,
            details=(
                f"FLAG: {fit_grade} archetype fit with {enabled_count} enabled "
                f"overrides (expected {low}–{high}) — a poorer-fit concept with "
                f"this few corrections suggests the library default is being "
                f"trusted where the archetype says it shouldn't be."
            ),
        )

    return ValidationResult(
        valid=True,
        details=(
            f"Override count ({enabled_count}) consistent with {fit_grade} "
            f"archetype fit (expected {low}–{high})"
        ),
    )
