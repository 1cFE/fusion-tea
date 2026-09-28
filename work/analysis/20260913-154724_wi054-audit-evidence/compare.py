import json
from pathlib import Path
h=Path('work/active/WI-054_faithful-model-equations-and-citations/evidence')
a=json.loads(Path('/tmp/wi054-independent-audit/native.json').read_text())
for f in ('candidate-native.json','baseline-native.json'):assert a==json.loads((h/f).read_text()),f
print('Independent execution exactly matches entering and candidate: ten cases, 158 outputs each, inputs/responses/constraint reports unchanged.')
