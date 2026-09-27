"""WI-096 balanced counterflow relation, selected installed UA and actual flow."""
import math
AUTO_IMPLEMENTED = False
INPUTS=dict(ua=60.,flow=2000.,cp=5193.)
OUTPUTS=['capacity_rate','effectiveness']
def calculate(x):
    if any(not math.isfinite(v) for v in x.values()) or x['ua']<0 or min(x['flow'],x['cp'])<=0:
        raise ValueError('recuperator needs nonnegative UA and positive flow/cp')
    c=x['flow']*x['cp']/1e6
    return dict(capacity_rate=c,effectiveness=x['ua']/(x['ua']+c))
