"""One reusable acceptance execution for production evidence and kept pytest cases."""
import json
import subprocess
import sys
from pathlib import Path
from common import H, ROOT, PRODUCTION, hashes


def run_acceptance(destination):
    destination=Path(destination).resolve()
    destination.mkdir(exist_ok=False)
    before=hashes(PRODUCTION)
    for name in ('native','direct','standalone','cli_checks','report'):
        command=['.codex-test/run','bash','-c',
                 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; exec .codex-test/run python "$@"',
                 'wi051',str(H/(name+'.py')),str(destination)]
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        (destination/(name+'.log')).write_text(result.stdout+result.stderr)
        with (destination/'commands.jsonl').open('a') as log:
            log.write(json.dumps({'command':command,'exit':result.returncode})+'\n')
        assert result.returncode==0, f'{name} failed: {destination/(name+".log")}'
    assert hashes(PRODUCTION)==before
    (destination/'package-hashes.json').write_text(json.dumps(before,indent=2)+'\n')
    print('PASS native, both production callers, standalone and CLI; package unchanged')
    return destination

if __name__=='__main__':
    run_acceptance(Path(sys.argv[1]) if sys.argv[1:] else H/'acceptance-attempt-1')
