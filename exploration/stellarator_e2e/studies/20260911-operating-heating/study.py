"""PreparedListStrategy study definition. Importing does not execute anything.

Parent-authorized execution follows fresh critique, native baseline/preflight, and a
formal oracle window scan. The preparation proposal remains the deposited contract.
"""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route

HERE = Path(__file__).resolve().parent
PROPOSAL = json.loads((HERE / 'preparation/proposal.json').read_text())
CHANNELS = json.loads((HERE / 'preparation/required-channels.json').read_text())


def run_arm(arm_id, output_directory):
    """Run the named prepared arm through the strict stock study lifecycle."""
    arm = next(a for a in PROPOSAL['arms'] if a['arm_id'] == arm_id)
    return study_route.run_points(
        PROPOSAL['study_id'] + '-' + arm_id,
        [case['point'] for case in arm['cases']],
        Path(output_directory),
        required_channels=CHANNELS,
    )
