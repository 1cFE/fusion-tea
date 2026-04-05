"""Template engine for prompt generation.

Supports {{variable}} substitution, {{#if var}}...{{/if}} conditionals,
and {{@path}} config file inclusion.
"""

import re
from pathlib import Path


def fill_template(template_text: str, replacements: dict[str, str],
                  templates_dir: Path | None = None) -> str:
    """{{variable}} substitution with {{#if var}}...{{/if}} conditionals
    and {{@path}} config file inclusion."""
    if templates_dir is None:
        from lib.paths import TEMPLATES_DIR
        templates_dir = TEMPLATES_DIR

    result = template_text

    # Process file inclusions first: {{@config/analysis_goals.md}}
    def replace_inclusion(m):
        rel_path = m.group(1)
        file_path = templates_dir / rel_path
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return f"[CONFIG FILE NOT FOUND: {rel_path}]"

    result = re.sub(r"\{\{@([^}]+)\}\}", replace_inclusion, result)

    # Process conditionals
    def replace_conditional(m):
        var_name = m.group(1)
        content = m.group(2)
        return content if replacements.get(var_name) else ""

    result = re.sub(
        r"\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}",
        replace_conditional,
        result,
        flags=re.DOTALL,
    )

    # Then substitute variables
    for key, value in replacements.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result
