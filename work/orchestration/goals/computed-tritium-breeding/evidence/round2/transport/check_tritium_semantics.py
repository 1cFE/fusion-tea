"""Bounded paired check of MT205 alias and H3-production score on installed runtime."""
import json
from pathlib import Path
import openmc

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[6]
RUNTIME=ROOT/'.codex-test/breeding-transport'
model=openmc.Model.from_model_xml(RUNTIME/'plant/table-node-t0.8/model.xml')
original=next(t for t in model.tallies if t.name=='recoverable_lithium_components')
paired=openmc.Tally(name='paired_H3_production')
paired.filters=original.filters
paired.nuclides=original.nuclides
paired.scores=['H3-production']
model.tallies.append(paired)
model.settings.batches=5;model.settings.particles=2000;model.settings.seed=9300029
model.settings.statepoint={'batches':[5]}
out=RUNTIME/'plant/tritium-semantics'
out.mkdir(exist_ok=False)
try:
 sp_path=model.run(cwd=out,threads=2)
 with openmc.StatePoint(sp_path) as sp:
  a=sp.get_tally(name='recoverable_lithium_components')
  b=sp.get_tally(name='paired_H3_production')
  result={'status':'EXECUTED','MT205_means':a.mean.ravel().tolist(),'H3_production_means':b.mean.ravel().tolist(),'difference':(a.mean-b.mean).ravel().tolist(),'MT205_std_error':a.std_dev.ravel().tolist(),'H3_production_std_error':b.std_dev.ravel().tolist()}
except RuntimeError as error:
 result={'status':'ENGINE_REFUSED','reason':str(error)}
(HERE/'tritium-semantics-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
