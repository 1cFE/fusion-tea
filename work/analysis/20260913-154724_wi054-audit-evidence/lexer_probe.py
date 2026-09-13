"""In-memory sensitivity checks; does not edit a model or expected receipt."""
import json,runpy
from pathlib import Path
h=Path('work/active/WI-054_faithful-model-equations-and-citations/evidence')
lex=runpy.run_path(str(h/'preservation.py'))['lexical']
base="attribute 'quoted // name' : Real = 1.0 + 2.0; doc /* documented */ // trailing\n"
for changed in (base.replace('1.0','1.1'),base.replace(' + ',' - '),base.replace(': Real',': Integer'),base.replace('quoted // name','quoted // changed'),base.replace(' = ',' := ')):
 assert lex(base)!=lex(changed)
assert lex(base)==lex(base.replace('documented','different documentation').replace('trailing','changed trailing'))
p=Path('models/library/analyses/mfe_plasma_scaling.sysml')
text=p.read_text();mutant=text.replace('in attribute B_axis_in : Real;', 'in attribute B_axis_changed : Real;',1)
assert mutant!=text and lex(mutant)!=lex(text)
print(json.dumps({'numeric_operator_type_quoted_identifier_binding_mutations':'rejected','conductor_calculation_input_mutation':'rejected','comment_only_change':'accepted'}))
