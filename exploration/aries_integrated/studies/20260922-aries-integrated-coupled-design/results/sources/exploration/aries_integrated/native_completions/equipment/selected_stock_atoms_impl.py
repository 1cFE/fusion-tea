"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def run_selected_stock_atoms(inputs):
    v = values(inputs)
    require(v['stock_kg']>=0 and v['atom_mass']>0, 'invalid selected stock')
    result=dict(atoms=v['stock_kg']/v['atom_mass'],stock_kg=v['stock_kg'])
    return finish('selected_stock_atoms', result)
