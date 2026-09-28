"""Actual branch endpoints; mixed source return remains independently controlled."""
AUTO_IMPLEMENTED=False
INPUTS=dict(primary_hot=0.,primary_exchanger_return=0.,secondary_in=0.,secondary_out=0.)
OUTPUTS=['hot_gap','cold_gap']
def calculate(x):return dict(hot_gap=x['primary_hot']-x['secondary_out'],cold_gap=x['primary_exchanger_return']-x['secondary_in'])
