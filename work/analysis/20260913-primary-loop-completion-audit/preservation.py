"""Check actual historical item directories and qualified IFE tracked files."""
import json,subprocess
from pathlib import Path
root=Path.cwd();out=Path(__file__).parent
paths=[str(p.relative_to(root)) for prefix in ('WI-050_','WI-051_','WI-052_','WI-053_','WI-054_','WI-055_') for p in (root/'work/active').glob(prefix+'*')]
assert len(paths)==6
ife=subprocess.check_output(['git','ls-files','models','exploration'],text=True).splitlines()
ife=[p for p in ife if '/ife_' in p or '/generic_ife/' in p]
assert ife
changed=subprocess.check_output(['git','diff','--name-only','cea6bc1a','--',*paths,*ife],text=True).splitlines();assert not changed,changed
(out/'preservation.json').write_text(json.dumps({'historical_paths':paths,'qualified_IFE_tracked_files':ife,'changed':changed},indent=2)+'\n')
