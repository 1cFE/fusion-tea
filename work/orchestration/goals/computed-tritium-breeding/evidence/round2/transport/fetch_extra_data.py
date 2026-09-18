"""Fetch material-completeness data with the same pinned source as runtime subset."""
import importlib.util
import json
from pathlib import Path

here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('fetch',here.parent/'runtime/fetch_data.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.SELECTION=here/'data-selection-extra.json'
module.main()
# The downloader's output manifest describes this extension, not the initial set.
records=json.loads((module.RUNTIME/'data/manifest.json').read_text())
(here/'data-manifest-extra.json').write_text(json.dumps(records,indent=2)+'\n')
