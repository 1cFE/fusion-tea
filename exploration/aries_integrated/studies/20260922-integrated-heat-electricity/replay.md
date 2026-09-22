# Safe replay

Run from a repository checkout with the recorded native package and study source identities, using the documented `.codex-test/run` environment. `results/sources/` retains the source files; `results/sealed-package.tar.gz` retains the generated package. The original execution checkout is recorded in `snapshot.json`; use a separate checkout if restoring it is necessary. Do not reset an active checkout or replace its model files. The commands below write only to a fresh temporary directory and refuse an existing study result directory.

```bash
export ARIES_REPLAY_ROOT="$(mktemp -d /tmp/aries-study-replay.XXXXXX)"
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python - <<'"'"'PY'"'"'
import os
import shutil
from pathlib import Path
from exploration.aries_integrated.studies import study_route

fresh = Path(os.environ["ARIES_REPLAY_ROOT"])
study = fresh / "20260922-integrated-heat-electricity"
study.mkdir()
shutil.copyfile(
    "exploration/aries_integrated/studies/20260922-integrated-heat-electricity/proposed-points.json",
    study / "proposed-points.json",
)
study_route.execute_baseline(fresh / "baseline")
print(fresh)
PY'
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m exploration.aries_integrated.studies.execute_study --record "$ARIES_REPLAY_ROOT/20260922-integrated-heat-electricity" --integration-return exploration/aries_integrated/studies/20260922-integrated-heat-electricity/results/integration/integration_return.json'
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python scripts/study/verify.py --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/manifest.json --identity "$ARIES_REPLAY_ROOT/baseline/package_identity.json" --store "$ARIES_REPLAY_ROOT/20260922-integrated-heat-electricity/results/native/20260922-integrated-heat-electricity.db" --sample-size 14 --out "$ARIES_REPLAY_ROOT/verification_summary.json"'
```

Compare replay inputs, outputs and verdicts with `results/cases.json`, matching the complete input map rather than relying on SQLite bytes or candidate order. SQLite identities and temporary path strings are not numerical comparison targets. The package route contains no oracle input substitution. The separate verifier uses the documented residual-only absolute tolerance and checks all ten exact verdicts.

The original source execution script is not used here because its main function writes the author baseline evidence path. These replay commands leave the committed record and author baseline evidence untouched.
