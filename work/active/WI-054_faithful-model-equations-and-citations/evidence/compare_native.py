"""Compare exact entering and candidate native channels and all verdicts."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
before=json.loads((HERE/'baseline-native.json').read_text());after=json.loads((HERE/'candidate-native.json').read_text())
assert before==after
rows=after['cases'];assert len(rows)==10 and all('error' not in row for row in rows.values())
report={'exact_equal':True,'cases':len(rows),'scalar_channels_per_case':sorted({len(row['outputs']) for row in rows.values()}),'complete_inputs_responses_reports_equal':True}
(HERE/'native-comparison.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
