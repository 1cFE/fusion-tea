"""The record template's digest shape matches what the tools emit.

`scripts/study/common.tool_source_digest` emits ``{recipe, digest, files[]}`` and the
verification-summary schema requires ``files`` (cold-pickup gap G1). The template
shows the shape a snapshot must carry in two places -- the oracle's digest under
`manifest.content_used.oracle` and the generic tools' digests under `tools[]` -- and
both must show the full shape, or a record written from the template omits the file
list that says which sources the digest covers.
"""

import json
import re

TEMPLATE = ".claude/skills/run-study/record-template.md"
SCHEMA = "scripts/study/schemas/verification_summary.v1.schema.json"


def _source_digest_blocks(text: str) -> list[str]:
    """Every `"source_digest": { ... }` block in the template, braces balanced."""
    blocks = []
    for match in re.finditer(r'"source_digest":\s*\{', text):
        depth, i = 1, match.end()
        while depth:
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        blocks.append(text[match.start() : i])
    return blocks


def test_template_shows_the_emitted_digest_shape_in_both_places(repo_root):
    text = (repo_root / TEMPLATE).read_text()
    blocks = _source_digest_blocks(text)
    assert len(blocks) == 2, [b[:60] for b in blocks]
    for block in blocks:
        assert '"recipe": "tool-source-digest/v1"' in block, block
        assert '"digest"' in block, block
        assert '"files"' in block, block
        assert '"path"' in block and '"sha256"' in block, block


def test_emitted_schema_requires_files(repo_root):
    schema = json.loads((repo_root / SCHEMA).read_text())
    digest = json.dumps(schema)
    assert '"required": ["recipe", "digest", "files"]' in digest
