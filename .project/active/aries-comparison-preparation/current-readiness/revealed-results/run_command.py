"""Run a recorded command in restored r3 with inherited licensed runtime."""
import datetime, json, os, pathlib, shlex, subprocess, sys
BASE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path('/tmp/aries-r3-execution-20260920')
def run(label, args, cwd=ROOT):
    logs = BASE / 'logs'
    logs.mkdir(exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out, err = logs / f'{stamp}-{label}.stdout', logs / f'{stamp}-{label}.stderr'
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([str(ROOT),str(ROOT/'scripts'),str(pathlib.Path(env['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')])
    env['STUDY_REQUIRE_TEAX'] = '1'
    command = [sys.executable if a == '@python' else a for a in args]
    with out.open('w') as stdout, err.open('w') as stderr:
        result = subprocess.run(command,cwd=cwd,env=env,stdout=stdout,stderr=stderr)
    record = dict(utc=stamp,cwd=str(cwd),argv=command,command=shlex.join(command),exit_status=result.returncode,stdout=str(out.relative_to(BASE)),stderr=str(err.relative_to(BASE)))
    with (BASE/'commands.jsonl').open('a') as stream: stream.write(json.dumps(record)+'\n')
    print(json.dumps(record))
    if result.returncode: print(err.read_text()[-4000:])
    return result.returncode
if __name__ == '__main__':
    raise SystemExit(run(sys.argv[1],sys.argv[2:]))
