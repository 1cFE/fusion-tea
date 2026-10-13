"""fusion-tea's supplement to the installed integration guide keeps fusion-tea's own facts.

The general operator guide ships with sysml-codegen in the run-study bundle, and
sysml-codegen's suite holds it to the seam's code: every condition slug, environment
variable, exit code, flag and gate. This repository's supplement,
`docs/integration_seam_operator_guide.md`, carries what is true only here. These tests keep
the two facts a stranger could find nowhere else: where the sealed wheels live, and the
decision of record.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GUIDE = REPO_ROOT / "docs" / "integration_seam_operator_guide.md"
ADR = REPO_ROOT / ".project" / "adr" / "0009-integration-is-a-fixed-point-proof.md"


def guide() -> str:
    return GUIDE.read_text()


def test_guide_records_the_sealed_wheel_home():
    body = guide()
    assert "stop-parser-sealed-wheels" in body
    assert "WHEEL_HASHES" in body


def test_the_decision_of_record_is_filed_and_indexed():
    assert ADR.is_file()
    index = (REPO_ROOT / ".project" / "adr" / "INDEX.md").read_text()
    assert re.search(r"^- 0009 · ", index, re.M), "0009 missing from the register index"
    assert ADR.name in guide()
