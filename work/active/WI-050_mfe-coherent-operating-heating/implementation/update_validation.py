"""Update only the four WI-050 verification rows after their evidence passes."""
import subprocess
from pathlib import Path
h=Path(__file__).resolve().parent
assert '364 passed, 13 skipped' in (h/'tests-models.log').read_text()
assert '9 passed' in (h/'focused-final.log').read_text()
with (h/'validation-row-commands.log').open('w') as log:
 for identifier in ['SV-079','SV-080','SV-081','SV-082']:
  command=['.codex-test/run','agentic-mbse','pm','update-validation',identifier,'--status','passing']
  log.write(repr(command)+'\n');log.flush();subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
