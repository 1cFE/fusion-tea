"""Pytest configuration for proof_of_concept tests."""

import sys
from pathlib import Path

# Add project root to path so proof_of_concept can be imported
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
