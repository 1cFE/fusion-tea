"""Goal-owned entry point; stock predecessor exporter and native lifecycle unchanged.

Invoke only after coordinator release of the reviewed comparison and preparation.
"""
import argparse
from pathlib import Path
import runpy
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from exploration.aries_integrated.studies import study_route as route

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--record',type=Path,required=True)
parser.add_argument('--integration-return',type=Path,required=True)
args=parser.parse_args()
route.MANIFEST_PATH=(args.record/'manifest.json').resolve()
execute=runpy.run_path(str(ROOT/'exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/execute_study.py'))['execute']
execute(args.record,args.integration_return)
