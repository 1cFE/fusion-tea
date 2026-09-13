"""Serialize every issue identity, including those truncated by the CLI summary."""
import json
import sys
from pathlib import Path
from agentic_mbse.validation.level1_syntax import validate_syntax
from agentic_mbse.validation.level2_structure import validate_structure
from agentic_mbse.validation.level3_dataflow import validate_dataflow
from agentic_mbse.validation.level4_constraints import analyze_constraints
from agentic_mbse.validation.level5_traceability import validate_traceability
from agentic_mbse.validation.level6_architecture import validate_architecture

def capture(path):
    rows=[]
    for fn in (validate_syntax,validate_structure,validate_dataflow,analyze_constraints,validate_traceability,validate_architecture):
        r=fn(str(path))
        rows.append({'level':r.level,'success':r.success,'issues':[str(i) for i in r.issues],'warnings':[str(i) for i in r.warnings],'metrics':r.metrics})
    return rows
if __name__=='__main__':
    Path(sys.argv[2]).write_text(json.dumps(capture(Path(sys.argv[1])),indent=2,default=str)+'\n')
