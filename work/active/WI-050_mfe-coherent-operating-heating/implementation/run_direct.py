"""Execute the direct runner against the declared isolated production package."""
from pathlib import Path
import shutil,subprocess,json
h=Path(__file__).resolve().parent
scratch=Path((h/'scratch.txt').read_text().strip());runner=scratch/'direct-consumer';runner.mkdir(exist_ok=True)
for name in ['run_stellaris.py','run_stellaris_single.py','verify_stellaris.py']:
 shutil.copyfile(Path('exploration/stellarator_e2e')/name,runner/name)
link=runner/'generated'
if not link.exists():link.symlink_to(scratch/'generated',target_is_directory=True)
command=['.codex-test/run','python',str(runner/'run_stellaris_single.py')]
with (h/'direct-runner.log').open('w') as log:
 log.write(repr(command)+'\n');log.flush();result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
(h/'direct-runner-command.json').write_text(json.dumps({'command':command,'package':str(scratch/'generated'),'exit':result.returncode},indent=2)+'\n')
assert result.returncode==0
