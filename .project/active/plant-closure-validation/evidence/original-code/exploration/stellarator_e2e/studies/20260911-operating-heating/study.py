"""PreparedListStrategy study definition. Importing does not execute anything.

Parent-authorized execution follows fresh critique, native baseline/preflight, and a
formal oracle window scan. The preparation proposal remains the deposited contract.
"""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route

HERE = Path(__file__).resolve().parent
PROPOSAL = json.loads((HERE / 'preparation/execution-proposal.json').read_text())
CHANNELS = json.loads((HERE / 'preparation/required-channels.json').read_text())


def labelled_proposals():
    """Preserve arm labels and proposal order separately from native case IDs."""
    return [dict(arm_id=arm['arm_id'], **case)
            for arm in PROPOSAL['arms'] for case in arm['cases']]


def run_all(output_directory):
    """Execute all arms in one stock store for the single package fingerprint."""
    return study_route.run_points(
        PROPOSAL['study_id'],
        [case['point'] for case in labelled_proposals()],
        Path(output_directory),
        required_channels=CHANNELS,
    )
