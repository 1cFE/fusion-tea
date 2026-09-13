"""Execute the actual production CLI with only its output directory isolated."""
import runpy
import sys
from pathlib import Path
root=Path.cwd()
sys.path.insert(0,str(root/'exploration/stellarator_e2e'))
import run_stellaris
scratch=Path(sys.argv.pop(1))
run_stellaris.E2E=scratch
sys.argv[0]=str(root/'exploration/stellarator_e2e/run_stellaris_single.py')
runpy.run_path(sys.argv[0],run_name='__main__')
