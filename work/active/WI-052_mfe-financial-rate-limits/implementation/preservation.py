"""Check canonical/family equality and unchanged calendar physical AST statements."""
import ast
import hashlib
import json
from pathlib import Path
from regenerate import HERE,ROOT,PRODUCTION,hashes,MFE
old=HERE/'entering/package/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py'
new=PRODUCTION/'handwritten/mfe_lifecycle/lifecycle_calendar_impl.py'

def function_shapes(path):
    result={}
    for node in ast.parse(path.read_text()).body:
        if not isinstance(node,ast.FunctionDef) or node.name=='_crf':continue
        if ast.get_docstring(node):node.body=node.body[1:]
        omit={'lifecycle_calendar_held':{'s','pv','disc_pow_n','crf','cost'},'lifecycle_calendar_live':{'pv'},'_dated_energy_ratio':{'disc'}}.get(node.name,set())
        class Strip(ast.NodeTransformer):
            def visit_Assign(self,statement):
                if any(isinstance(t,ast.Name) and t.id in omit for t in statement.targets):return None
                return self.generic_visit(statement)
        node=Strip().visit(node)
        result[node.name]=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()
    return result
before,after=function_shapes(old),function_shapes(new)
assert before==after,(before,after)
family={}
for logical in MFE.owned:
    canonical=ROOT/'models'/logical if logical.startswith('designs/') else ROOT/'models/library'/logical
    mirror=MFE.twin/logical
    assert canonical.read_bytes()==mirror.read_bytes()
    family[logical]=hashlib.sha256(canonical.read_bytes()).hexdigest()
assert hashes(PRODUCTION)==json.loads((HERE/'production-hashes.json').read_text())
(HERE/'preservation.json').write_text(json.dumps({'calendar_nonfinance_function_ast':before,'canonical_equals_family':family,'production_inventory_unchanged':True},indent=2)+'\n')
print('PASS calendar nonfinance AST unchanged, all 23 family copies exact, production inventory unchanged')
